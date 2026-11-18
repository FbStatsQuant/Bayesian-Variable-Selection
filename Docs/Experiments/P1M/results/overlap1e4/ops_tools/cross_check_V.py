#!/usr/bin/env python3
"""cross_check_V.py <records_wave_dir> [--info-bin smcbvs4] -- OV_W0_V2 vs OV_W0_V: every fit output identical except provenance.
Stdlib only. <records_wave_dir> = Owls records/overlap1e4/W0 (after collect_wave.sh). Pairs <run_id> (batch V) with <run_id>.V2 (batch V2),
same plan, same seeds, same shapes, built from `git archive F` (V) vs the git worktree of F (V2): by the same-bits rule every output equal.
For each pair and each file of record:
  * data.bin and other non-container files: sha256 equal.
  * the containers fit.bin / law.bin / eval.bin embed the binary block (git_commit, binary sha256): raw bytes differ BY DESIGN. With
    --info-bin <smcbvs4> (any Owls build that reads the format) their sections (name, dtype, dims, sha256, all but `meta`) are compared
    through `smcbvs4 info <file> --meta 1 --record <json>` (the freeze_check_1e5.sh method); without it only the *.bin.json sidecars are compared.
  * *.json sidecars / manifests: flattened and compared EXACTLY after dropping provenance keys (DROP below: the binary block and git commit,
    file-level input hashes of derived files (they include the binary block), paths, batch names, timings / seconds / cost / hosts / threads /
    timestamps, memory plans). The dropped key paths are listed with --show-dropped so nothing is dropped silently.
Exit 0 = identical outside provenance; 1 = at least one DIFF (printed); 2 = the pairing is incomplete.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile

DROP = re.compile(r"(^|\.)(binary|git_commit|inputs|data|outputs|paths|batch|created_utc|created|start|end|host|node|threads|mem_plan|"
                  r"start_bytes_measured|seconds|[a-z_]*seconds|wall[a-z_]*|elapsed[a-z_]*|timings?|cost|island_bin|run_manifest|resumed_from_step)(\.|$|\[)")
CONTAINERS = ("fit.bin", "law.bin", "eval.bin")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def flat(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, pre + ("." if pre else "") + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, "%s[%d]" % (pre, i))
    else:
        yield pre, o


def norm(v):
    return re.sub(r"OV_W\d_[TV]2?", "OV_BATCH", v) if isinstance(v, str) else v


def sections(binf, path, tmp):
    rec = os.path.join(tmp, os.path.basename(path) + ".info.json")
    subprocess.run([binf, "info", path, "--meta", "1", "--record", rec], check=True, stdout=subprocess.DEVNULL)
    j = json.load(open(rec))
    return {s["name"]: (s["dtype"], tuple(s["dims"]), s["sha256"]) for s in j.get("sections", []) if s["name"] != "meta"}, j.get("meta", {}).get("output_hash")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("wave_dir"); ap.add_argument("--info-bin"); ap.add_argument("--show-dropped", action="store_true")
    a = ap.parse_args()
    pairs = sorted((d[:-3], d, d[:-3] + ".V2") for d in os.listdir(a.wave_dir) if re.search(r"-V-s\d$", d))
    if not pairs:
        sys.exit("no V units in %s" % a.wave_dir)
    bad, miss, tmp = 0, 0, tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(a.wave_dir)))
    for _, d1, d2 in [(x[0], x[1], x[2]) for x in pairs]:
        u1, u2 = os.path.join(a.wave_dir, d1), os.path.join(a.wave_dir, d2)
        if not os.path.isdir(u2):
            print("MISSING unit %s" % d2); miss += 1; continue
        f1 = {os.path.relpath(os.path.join(r, f), u1) for r, _, fs in os.walk(u1) for f in fs if f != "SHA256SUMS" and f != "INCOMPLETE.txt"}
        f2 = {os.path.relpath(os.path.join(r, f), u2) for r, _, fs in os.walk(u2) for f in fs if f != "SHA256SUMS" and f != "INCOMPLETE.txt"}
        # logs, cost records and manifests differ by batch / time / host: only the output files and sidecars are compared
        keep = lambda f: not f.startswith(("log/", "cost/", "manifests/")) and f not in ("run_manifest.json",)
        f1, f2 = {f for f in f1 if keep(f)}, {f for f in f2 if keep(f)}
        for f in sorted(f1 ^ f2):
            print("DIFF %s: file only in %s" % (f, d1 if f in f1 else d2)); bad += 1
        n_ok = n_drop = 0
        for f in sorted(f1 & f2):
            p1, p2 = os.path.join(u1, f), os.path.join(u2, f)
            if f.endswith(".json"):
                a1 = dict(flat(json.load(open(p1)))); a2 = dict(flat(json.load(open(p2))))
                k1 = {k for k in a1 if not DROP.search(k)}; k2 = {k for k in a2 if not DROP.search(k)}
                dropped = sorted((set(a1) | set(a2)) - (k1 | k2)); n_drop += len(dropped)
                if a.show_dropped:
                    print("  dropped in %s/%s: %s" % (d1, f, ", ".join(dropped)))
                for k in sorted(k1 | k2):
                    if norm(a1.get(k, "<absent>")) != norm(a2.get(k, "<absent>")):
                        print("DIFF %s/%s %s: %r != %r" % (d1, f, k, a1.get(k, "<absent>"), a2.get(k, "<absent>"))); bad += 1
                n_ok += 1
            elif f in CONTAINERS:
                if a.info_bin:
                    s1, h1 = sections(a.info_bin, p1, tmp); s2, h2 = sections(a.info_bin, p2, tmp)
                    for k in sorted(set(s1) | set(s2)):
                        if s1.get(k) != s2.get(k):
                            print("DIFF %s/%s section %s" % (d1, f, k)); bad += 1
                    if h1 != h2:
                        print("DIFF %s/%s output_hash %s != %s" % (d1, f, h1, h2)); bad += 1
                    n_ok += 1
                else:
                    print("  note %s/%s: raw bytes not compared (embeds the binary block); pass --info-bin for the section check" % (d1, f))
            else:
                if sha(p1) != sha(p2):
                    print("DIFF %s/%s sha256" % (d1, f)); bad += 1
                n_ok += 1
        print("%s vs %s: %d files compared, %d provenance keys dropped" % (d1, d2, n_ok, n_drop))
    os.system("rm -rf '%s'" % tmp)
    print("RESULT:", "IDENTICAL outside provenance" if not bad and not miss else "%d DIFF, %d missing unit(s)" % (bad, miss))
    sys.exit(2 if miss else (1 if bad else 0))


if __name__ == "__main__":
    main()
