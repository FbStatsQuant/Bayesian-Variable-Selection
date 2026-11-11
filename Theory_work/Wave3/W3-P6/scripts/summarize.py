"""W3-P6 summary v3 (v2 = R01 fixes 1, 2, 5, 6, 7, 9; v3 = rerun-aware loader, CP0 risk 4).
Usage: python summarize.py OUT_MD --run TAG DERIVED_JSONL TASKS_TSV [--run ...] [--rerun TAG DERIVED_JSONL TASKS_TSV ...]
       [--group A|B per run via TAG prefix]. A --rerun key must belong to exactly one --run with no record there; it is
       counted once, from the rerun (see load()).

Inputs per run: rederive.R output (one line per fit RDS) and the frozen task table. Every scheduled task is accounted for:
scheduled = tasks in the table; records = derived lines matching a task key; missing = scheduled without a record
(scheduler failure / not finished); duplicates and records not in the table abort the summary (fail closed).

Per cell (design, rho, s0, n, p), arm wide only (arm mr1 = validation pairs):
  sched / compl          scheduled tasks / fits with status "completed"
  as-coded HPM=S0        merged cap ell_n + |S~0| (derived from the wide run's LS0 prefix): k/e [Wilson 95%] over evaluable
                         fits e (completed, derivation status ok); bounds [k/sched, (k + sched - e)/sched] treat every
                         non-evaluable scheduled seed as failure / success
  classes (as coded)     S0 / posterior (F(HPM) > F(S0)) / search (F(S0) > F(HPM): S0 never scored in that run) / NA
  cap2 HPM=S0, classes   same for cap ell_n + 2|S~0| (algorithmic counterfactual; its delivery/preflight is not reproduced)
  wide HPM=S0            the wide run's own report (cap ell_n + K + |S~0|)
  snapshots              HPM == S0 after the SMC islands (before the final local search) and before LS0; a snapshot
                         equal to S0 proves S0 was scored by then; unequal proves nothing unless the class is "search"
  cap changes HPM        fits where the MR1-derived and cap2-derived HPM differ (any change, not only to S0)
Group B runs (TAG starting with "B") are tabulated separately with status counts and the HPM-so-far (truncated runs).
"""
import json, math, sys, statistics as st
from collections import defaultdict, Counter


def wilson(k, m, z=1.96):
    if m == 0: return (float("nan"), float("nan"))
    ph = k / m; d = 1 + z * z / m; c = ph + z * z / (2 * m); h = z * math.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m))
    return ((c - h) / d, (c + h) / d)


def rate(k, e, sched):
    if e == 0: return f"0/0 (sched {sched})"
    lo, hi = wilson(k, e)
    return f"{k}/{e} [{lo:.2f},{hi:.2f}] b[{k / sched:.2f},{(k + sched - e) / sched:.2f}]"


def med(xs, d=0):
    xs = [x for x in xs if x is not None]
    if not xs: return "–"
    m = st.median(xs)
    return f"{m:.{d}f}"


def tkey(kv):
    d = kv["design"]
    rho = float(kv["rho"]) if "rho" in kv else (0.5 if d == "cs" else 0.0)
    return (d, round(rho, 3), int(kv["n"]), int(kv["p"]), int(kv["s0"]), int(kv["rep"]), kv["arm"])


def rkey(r):
    return (r["design"], round(float(r["rho"]), 3), r["n"], r["p"], r["s0"], r["rep"], r["arm"])


def group(tag):
    return "B" if tag.startswith("B") else "A"


def table_keys(tt):
    for l in open(tt):
        if "\t" not in l: continue
        kv = dict(x.split("=", 1) for x in l.strip().split("\t", 1)[1].split() if "=" in x and not x.startswith("$"))
        yield tkey(kv)


def load(args):
    # --run TAG DJ TT: a run's own tasks. --rerun TAG DJ TT (v3, resume 2026-11-11): DESIGN §5 policy "Slurm failures are
    # rerun once with the same seeds (new RUN_ID)". Every rerun key must be scheduled by exactly one --run, have no record
    # there, be rerun at most once, and stay in the same group; its schedule then moves to the rerun tag, so the key is
    # counted once and only a record from the rerun is accepted. All task tables are read before any record (order-free).
    runs = []; reruns = []
    i = 0
    while i < len(args):
        assert args[i] in ("--run", "--rerun"), args[i]
        (runs if args[i] == "--run" else reruns).append((args[i + 1], args[i + 2], args[i + 3])); i += 4
    sched = {}; recs = {}; problems = []; origin = {}
    for tag, dj, tt in runs:
        for k in table_keys(tt):
            if k in sched: problems.append(f"task key scheduled twice: {k} ({sched[k]} and {tag})")
            sched[k] = tag
    for tag, dj, tt in reruns:
        for k in table_keys(tt):
            if k not in sched: problems.append(f"rerun key not scheduled by any --run: {k} ({tag})"); continue
            if k in origin: problems.append(f"key rerun twice: {k} ({sched[k]} and {tag})"); continue
            if group(sched[k]) != group(tag): problems.append(f"rerun changes group: {k} ({sched[k]} -> {tag})"); continue
            origin[k] = sched[k]; sched[k] = tag
    for tag, dj, tt in runs + reruns:
        for l in open(dj):
            l = l.strip()
            if not l: continue
            r = json.loads(l)
            if r.get("read_error"): problems.append(f"unreadable RDS {r['file']} in {tag}"); continue
            k = rkey(r)
            if k in origin and origin[k] == tag:
                problems.append(f"record in {tag} for a key rerun as {sched[k]}: {k} (a rerun needs no record in its origin)"); continue
            if k not in sched or sched[k] != tag: problems.append(f"record not in task table of {tag}: {k}"); continue
            if k in recs: problems.append(f"duplicate record {k}"); continue
            r["_run"] = tag; recs[k] = r
    return sched, recs, problems, origin


def main():
    out = sys.argv[1]; sched, recs, problems, origin = load(sys.argv[2:])
    L = []
    if problems:
        L += ["**RECONCILIATION FAILED (fail closed):**"] + [f"* {p}" for p in problems[:50]]
        open(out, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(1)
    missing = sorted(k for k in sched if k not in recs)
    L.append(f"Reconciliation: {len(sched)} scheduled tasks, {len(recs)} records, {len(missing)} without a record (not finished or failed before writing).")
    if origin:
        rr = Counter((o, sched[k]) for k, o in origin.items())
        L.append("Reruns (DESIGN §5, same seeds, new RUN_ID; counted once): " + "; ".join(f"{o} -> {t}: {c}" for (o, t), c in sorted(rr.items())) + ".")
    L.append("")
    # ---- validation pairs (exact identity, fail closed) ----
    pairs = [(recs[k], recs.get(k[:-1] + ("wide",))) for k in recs if k[-1] == "mr1"]
    bad = []; npair = 0
    for m, w in pairs:
        if w is None or m["status"] != "completed" or w["status"] != "completed":
            bad.append((rkey(m)[:-1], "unpaired or not completed")); continue
        npair += 1
        checks = {"data/method seed": (m["data_seed"], m["method_seed"]) == (w["data_seed"], w["method_seed"]),
                  "start mode": m["start_mode"] == w["start_mode"],
                  "pre-LS0 HPM": (m["before_ls0"], m["before_ls0_F"]) == (w["before_ls0"], w["before_ls0_F"]),
                  "calibration tier": m["cal_tier_final"] == w["cal_tier_final"],
                  "LS0 first scoring scan (if <= mr1 scans)": (m["ls0_first_scoring"] == w["ls0_first_scoring"]) or (m["ls0_first_scoring"] is None and (w["ls0_first_scoring"] or 10**9) > m["ls0_scans"]),
                  "derivation status ok": w["mr1_status"] == "ok",
                  "HPM model": m["hpm"] == w["mr1_hpm"], "HPM F": m["hpm_F"] == w["mr1_F"]}
        for c, ok in checks.items():
            if not ok: bad.append((rkey(m)[:-1], c))
    if pairs:
        L.append(f"Prefix-derivation validation (arm mr1 vs MR1 derived from arm wide; exact model identity and F, seeds, start mode, "
                 f"pre-LS0 HPM, tier, LS0 first scoring scan): {npair} completed pairs, {len(bad)} disagreements/unusable.")
        L += [f"* {k}: {c}" for k, c in bad[:40]]
        L.append("")
    # ---- group A (completed-fit cells) ----
    cells = defaultdict(list); scells = Counter()
    for k, tag in sched.items():
        if k[-1] != "wide": continue
        ck = (tag[0] if tag.startswith("B") else "A",) + k[:5]
        scells[ck] += 1
        if k in recs: cells[ck].append(recs[k])
    for grp in ("A", "B"):
        keys = sorted(c for c in scells if c[0] == grp)
        if not keys: continue
        L.append(f"### Group {grp}" + (" (completed-fit grid)" if grp == "A" else " (fixed 22.5-h allocation; truncated runs report HPM-so-far)"))
        L.append("")
        L.append("| design | ρ | s0 | n | p | p/n | sched/compl | as-coded HPM=S0 | classes S0/post/search/NA | cap2 HPM=S0 | cap2 classes | "
                 "wide HPM=S0 | snap SMC / pre-LS0 =S0 | cap changes HPM | start size = K | LS0 moves / 1st-scoring / MR1 cap | t_med h | other statuses |")
        L.append("|" + "|".join(["---"] * 18) + "|")
        for c in keys:
            _, d, rho, n, p, s0 = c; rs = cells.get(c, []); S = scells[c]
            comp = [r for r in rs if r["status"] == "completed"]
            def cls(field):
                cc = Counter(r.get(field) for r in comp)
                return f"{cc.get('S0',0)}/{cc.get('posterior',0)}/{cc.get('search',0)}/{sum(v for kk, v in cc.items() if kk not in ('S0','posterior','search'))}"
            ev_m = [r for r in comp if r["mr1_status"] == "ok"]; ev_2 = [r for r in comp if r["cap2_status"] == "ok"]
            km = sum(1 for r in ev_m if r["mr1_eq_S0"]); k2 = sum(1 for r in ev_2 if r["cap2_eq_S0"])
            kw = sum(1 for r in comp if r["hpm_eq_S0"])
            chg = sum(1 for r in comp if r["mr1_status"] == "ok" and r["cap2_status"] == "ok" and r["mr1_hpm"] != r["cap2_hpm"])
            snaps = f"{sum(1 for r in comp if r['before_local_eq_S0'])}/{sum(1 for r in comp if r['before_ls0_eq_S0'])}"
            sat = sum(1 for r in comp if r["start_size"] == r["K"])
            oth = Counter(r["status"] for r in rs if r["status"] != "completed")
            if grp == "B":
                oth = Counter(f"{r['status']}:HPM=S0" if r["hpm_eq_S0"] else f"{r['status']}:{r['reported_class']}" for r in rs if r["status"] != "completed")
            row = [d, f"{rho:.2f}" if d == "cs" else "–", s0, n, p, f"{p / n:g}", f"{S}/{len(comp)}", rate(km, len(ev_m), S), cls("mr1_class"),
                   rate(k2, len(ev_2), S), cls("cap2_class"), rate(kw, len(comp), S), snaps, chg, f"{sat}/{len(comp)}",
                   f"{med([r['ls0_moves'] for r in comp])} / {med([r['ls0_first_scoring'] for r in comp])} / {med([r['cap_mr1'] for r in comp])}",
                   med([r["elapsed_sec"] / 3600 for r in rs], 2), "; ".join(f"{k}×{v}" for k, v in oth.items()) or "–"]
            L.append("| " + " | ".join(map(str, row)) + " |")
        L.append("")
    # provenance of the HPM when it equals S0 (earliest event at which S0 became the running best)
    prov = Counter((r["hpm_prov"] or "NA").split("/")[0] for r in recs.values() if r["arm"] == "wide" and r["status"] == "completed" and r["hpm_eq_S0"])
    L.append(f"Phase in which S0 became the running HPM (wide, completed, HPM = S0): {dict(prov)}")
    nonok = Counter((r["mr1_status"], r["cap2_status"]) for r in recs.values() if r["arm"] == "wide" and r["status"] == "completed" and (r["mr1_status"] != "ok" or r["cap2_status"] != "ok"))
    L.append(f"Derivations not ok (mr1_status, cap2_status): {dict(nonok) if nonok else 'none'}")
    dv = [r["F_direct_vs_ledger"] for r in recs.values() if r.get("F_direct_vs_ledger") is not None]
    L.append(f"max |F_direct(HPM) − F_ledger(HPM)| over {len(dv)} fits: {max(dv) if dv else 'NA'}")
    if missing: L += ["", f"Scheduled without record ({len(missing)}; first 40):"] + [f"* {k}" for k in missing[:40]]
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
