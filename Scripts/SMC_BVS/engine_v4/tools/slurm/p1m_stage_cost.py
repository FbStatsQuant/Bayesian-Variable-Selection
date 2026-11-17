#!/usr/bin/env python3
"""p1m_stage_cost.py -- read D-30 per-step cost records (WP7 O2/O5) and print the per-stage tables the R1 re-size needs.

Inputs (any mix):
  *.jsonl                       a sidecar (IslandConfig::cost_path; calibrate --cost-dir; v4_pilot_island --cost-dir):
                                a {"cost_header": ...} line per job segment, then one row object per step
  *.json                        a record holding meta.cost (`smcbvs4 info --in island_r.bin --meta 1 --out x` -> x.json),
                                or a bare meta.cost object (columns)

Commands:
  p1m_stage_cost.py table FILE...          per-step table of each record, then a summary by stage kind
  p1m_stage_cost.py summary FILE...        the summary only (one block per record)
  p1m_stage_cost.py isa ISLAND_A ISLAND_B [--bin smcbvs4] [--json OUT]
                                       D-32: the same island from two island-ISA builds carries the same science
                                       (meta.output_hash and every non-meta section hash); exit 1 if not
  p1m_stage_cost.py t5 RUN_DIR [--bin smcbvs4] [--json OUT]
                                       T5 report of one fit run directory of the WP5 driver: calibration islands
                                       (RUN_DIR/cost/*.jsonl), final islands (island_*.bin meta.cost through
                                       `smcbvs4 info --meta 1`), the merge record's seconds (merge, tail local search,
                                       LS0) and the stage records' seconds; --json writes the whole report as JSON.

Derived per row: ns_cpu_per_step = wall x threads / (particle_rounds x m) (thread time per elementary step, wall
based, all phases); offers_per_step = offers / (particle_rounds x m). Labels: every number printed is MEASURED by the
run that wrote the record. Standard library only.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

KIND = {0: "init", 1: "bridge", 2: "burn-in", 3: "measured", 4: "exit"}


def denan(r):
    """meta.cost / the progress log write a field the kernel does not measure as the string "NaN" (INTERFACES §5.1)."""
    return {k: (float("nan") if v == "NaN" else v) for k, v in r.items()}


def load(path):
    """-> list of (header, rows) per job segment; rows are dicts."""
    out = []
    if path.endswith(".jsonl"):
        hdr, rows = None, []
        with open(path) as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                j = json.loads(ln)
                if "cost_header" in j:
                    if hdr is not None or rows:
                        out.append((hdr, rows))
                    hdr, rows = j["cost_header"], []
                else:
                    rows.append(denan(j))
        if hdr is not None or rows:
            out.append((hdr, rows))
        return merge_segments(out)
    with open(path) as f:
        j = json.load(f)
    c = j.get("meta", {}).get("cost") if isinstance(j.get("meta"), dict) else None
    if c is None:
        c = j.get("cost", j)
    if "columns" not in c:
        raise SystemExit("%s: no cost record (meta.cost with columns)" % path)
    cols = c["columns"]
    n = int(c.get("rows", len(cols.get("step", []))))
    rows = [denan({k: v[i] for k, v in cols.items()}) for i in range(n)]
    hdr = {k: v for k, v in c.items() if k not in ("columns", "rows")}
    return [(hdr, rows)]


def merge_segments(segs):
    """The progress log is rebuilt at every job segment (one header), so a finished log has unique rows; an older log
    with several headers keeps, per step, the row of the latest segment. meta.cost is the authoritative record."""
    if not segs:
        return []
    hdr = segs[-1][0] or segs[0][0] or {}
    by_step = {}
    for _, rows in segs:
        for r in rows:
            by_step[int(r["step"])] = r
    return [(hdr, [by_step[k] for k in sorted(by_step)])]


def derive(hdr, r):
    m = float(hdr.get("m") or 0)
    th = float(hdr.get("threads") or 1)
    steps = float(r.get("particle_rounds", 0)) * m
    d = dict(r)
    d["ns_cpu_per_step"] = 1e9 * r["wall"] * th / steps if steps > 0 else 0.0
    d["offers_per_step"] = r.get("offers", 0) / steps if steps > 0 else 0.0
    return d


def table(hdr, rows, fh=sys.stdout):
    fh.write("# %s\n" % json.dumps(hdr, sort_keys=True))
    fh.write("%4s %-8s %9s %8s %6s %6s %6s %7s %7s %9s %9s %5s %7s %6s %6s %7s %6s\n" % (
        "step", "kind", "phi", "wall_s", "M", "|S|", "k_st", "fl/st", "act/ps", "offers", "off/step", "cmp", "cmp_s", "chk_s",
        "ckp_s", "ns/step", "hwmGB"))
    for r in rows:
        d = derive(hdr, r)
        fh.write("%4d %-8s %9.5f %8.2f %6.2f %6.2f %6.2f %7.3f %7.1f %9d %9.5f %5d %7.2f %6.2f %6.2f %7.0f %6.2f\n" % (
            d["step"], KIND.get(d["kind"], "?"), d["phi"], d["wall"], d.get("M", 0), d.get("mean_S", 0), d.get("store_mean_k", 0),
            d.get("flips_per_step", 0), d.get("act_cols_per_pass", 0), d.get("offers", 0), d["offers_per_step"], d.get("merges", 0),
            d.get("t_compact", 0), d.get("t_check", 0), d.get("t_ckpt", 0), d["ns_cpu_per_step"], d.get("hwm_kb", 0) / 1048576.0))


def summary(hdr, rows):
    """Per stage kind: steps, wall, wall-weighted means and sums (what R1's per-stage model takes)."""
    out = {}
    for k in (0, 1, 2, 3, 4):
        rs = [derive(hdr, r) for r in rows if int(r["kind"]) == k]
        if not rs:
            continue
        rounds = sum(r.get("particle_rounds", 0) for r in rs)
        s = {"steps": len(rs), "wall_s": sum(r["wall"] for r in rs),
             "M": sum(r.get("sweeps", 0) for r in rs) / rounds if rounds else 0.0,
             "mean_S": sum(r.get("mean_S", 0) for r in rs) / len(rs),
             "flips_per_step": sum(r.get("flips", 0) for r in rs) / (rounds * float(hdr.get("m") or 1)) if rounds else 0.0,
             "act_cols_per_pass": sum(r.get("act_cols", 0) for r in rs) / max(1, sum(r.get("passes", 0) for r in rs)),
             "offers": sum(r.get("offers", 0) for r in rs),
             "offers_per_step": sum(r.get("offers", 0) for r in rs) / (rounds * float(hdr.get("m") or 1)) if rounds else 0.0,
             "compactions": sum(r.get("merges", 0) for r in rs), "compact_s": sum(r.get("t_compact", 0) for r in rs),
             "check_s": sum(r.get("t_check", 0) for r in rs), "ckpt_s": sum(r.get("t_ckpt", 0) for r in rs),
             "phaseA_s": sum(r.get("t_phaseA", 0) for r in rs), "phaseB_s": sum(r.get("t_phaseB", 0) for r in rs),
             "peak_rss_gb": max(r.get("hwm_kb", 0) for r in rs) / 1048576.0}
        steps = rounds * float(hdr.get("m") or 0)
        s["ns_cpu_per_step"] = 1e9 * s["wall_s"] * float(hdr.get("threads") or 1) / steps if steps else 0.0
        out[KIND[k]] = s
    tot = sum(r["wall"] for r in rows)
    out["total"] = {"steps": len(rows), "wall_s": tot, "segments": len({int(r.get("segment", 0)) for r in rows})}
    return out


def print_summary(name, hdr, rows, fh=sys.stdout):
    s = summary(hdr, rows)
    fh.write("## %s  (N %s, p %s, threads %s, G %s, kernel %s, arith %s)\n" % (name, hdr.get("N"), hdr.get("p"), hdr.get("threads"),
             hdr.get("G"), hdr.get("kernel"), hdr.get("arith")))
    fh.write("%-9s %5s %9s %6s %6s %7s %7s %10s %9s %5s %8s %7s %7s %8s %6s\n" % ("kind", "steps", "wall_s", "M", "|S|", "fl/st", "act/ps",
             "offers", "off/step", "cmp", "cmp_s", "chk_s", "ckp_s", "ns/step", "hwmGB"))
    for k in ("init", "bridge", "burn-in", "measured", "exit"):
        if k in s:
            v = s[k]
            fh.write("%-9s %5d %9.2f %6.2f %6.2f %7.3f %7.1f %10d %9.5f %5d %8.2f %7.2f %7.2f %8.0f %6.2f\n" % (
                k, v["steps"], v["wall_s"], v["M"], v["mean_S"], v["flips_per_step"], v["act_cols_per_pass"], v["offers"],
                v["offers_per_step"], v["compactions"], v["compact_s"], v["check_s"], v["ckpt_s"], v["ns_cpu_per_step"], v["peak_rss_gb"]))
    fh.write("total     %5d %9.2f  (job segments %d)\n" % (s["total"]["steps"], s["total"]["wall_s"], s["total"]["segments"]))
    return s


def info_meta(binary, path):
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as d:
        out = os.path.join(d, "info")
        subprocess.run([binary, "info", "--in", path, "--meta", "1", "--out", out], check=True, stdout=subprocess.DEVNULL)
        with open(out + ".json") as f:
            return json.load(f)


def t5(run_dir, binary, json_out):
    rep = {"run_dir": run_dir, "calibration": {}, "islands": {}, "stages": {}}
    for st in ("setup", "calib", "fit", "eval", "law"):
        p = os.path.join(run_dir, st + ".bin.json")
        if os.path.exists(p):
            with open(p) as f:
                r = json.load(f)
            rep["stages"][st] = {k: r[k] for k in ("status", "seconds", "timings", "tier_final") if k in r}
    print("# T5 report: %s" % run_dir)
    ip = os.path.join(run_dir, "isa_check.json")
    if os.path.exists(ip):
        with open(ip) as f:
            rep["isa_check"] = json.load(f)
        print("isa check (D-32): %s" % json.dumps(rep["isa_check"], sort_keys=True))
    for st, v in rep["stages"].items():
        print("stage %-6s %s" % (st, json.dumps(v, sort_keys=True)))
    for p in sorted(glob.glob(os.path.join(run_dir, "cost", "*.jsonl"))):
        for hdr, rows in load(p):
            rep["calibration"][os.path.basename(p)] = print_summary(os.path.basename(p), hdr, rows)
    for p in sorted(glob.glob(os.path.join(run_dir, "island_*.bin"))):
        try:
            j = info_meta(binary, p)
        except Exception as e:   # noqa: BLE001 -- report and continue
            print("%s: cannot read meta (%s)" % (p, e))
            continue
        c = j.get("meta", {}).get("cost")
        if not c:
            print("%s: no meta.cost" % p)
            continue
        for hdr, rows in load_obj(c):
            rep["islands"][os.path.basename(p)] = print_summary(os.path.basename(p), hdr, rows)
    isl = list(rep["islands"].values())
    if isl:
        tot = sum(v["total"]["wall_s"] for v in isl)
        print("final islands: %d, wall sum %.1f s, max %.1f s" % (len(isl), tot, max(v["total"]["wall_s"] for v in isl)))
    if json_out:
        with open(json_out, "w") as f:
            json.dump(rep, f, indent=1, sort_keys=True)
    return rep


def compare_isa(info_a, info_b):
    """D-32 (T2 across ISAs): two `smcbvs4 info --meta 1` records of the same island, built with two island ISAs.
    Equal science = equal meta.output_hash (IslandRun::hash) and, for every non-meta section, the same name, dtype,
    dims and SHA-256. Returns (ok, details)."""
    def secs(j):
        return {s["name"]: (s["dtype"], tuple(s["dims"]), s["sha256"]) for s in j.get("sections", []) if s["name"] != "meta"}
    ma, mb = info_a.get("meta", {}), info_b.get("meta", {})
    sa, sb = secs(info_a), secs(info_b)
    diff = sorted(n for n in set(sa) | set(sb) if sa.get(n) != sb.get(n))
    isa = [m.get("binary", {}).get("island_isa") for m in (ma, mb)]
    ok = bool(sa) and not diff and ma.get("output_hash") is not None and ma.get("output_hash") == mb.get("output_hash")
    return ok, {"output_hash": [ma.get("output_hash"), mb.get("output_hash")], "island_isa": isa, "sections": len(sa),
                "differing_sections": diff, "status": [ma.get("status"), mb.get("status")]}


def load_obj(c):
    cols = c["columns"]
    n = int(c.get("rows", len(cols.get("step", []))))
    return [({k: v for k, v in c.items() if k not in ("columns", "rows")}, [denan({k: v[i] for k, v in cols.items()}) for i in range(n)])]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("table"); a.add_argument("files", nargs="+")
    b = sub.add_parser("summary"); b.add_argument("files", nargs="+")
    c = sub.add_parser("t5"); c.add_argument("run_dir"); c.add_argument("--bin", default="smcbvs4"); c.add_argument("--json")
    d = sub.add_parser("isa"); d.add_argument("island_a"); d.add_argument("island_b"); d.add_argument("--bin", default="smcbvs4")
    d.add_argument("--json")
    args = ap.parse_args(argv)
    if args.cmd in ("table", "summary"):
        for p in args.files:
            for hdr, rows in load(p):
                if args.cmd == "table":
                    table(hdr, rows)
                print_summary(p, hdr, rows)
        return 0
    if args.cmd == "isa":   # exit 0 iff the two island files carry the same science (D-32)
        ok, det = compare_isa(info_meta(args.bin, args.island_a), info_meta(args.bin, args.island_b))
        det["ok"] = ok
        print(json.dumps(det, sort_keys=True))
        if args.json:
            with open(args.json, "w") as f:
                json.dump(det, f, indent=1, sort_keys=True)
        return 0 if ok else 1
    t5(args.run_dir, args.bin, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
