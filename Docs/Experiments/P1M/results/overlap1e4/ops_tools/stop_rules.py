#!/usr/bin/env python3
"""stop_rules.py <probe.txt> --wave W0 --plans <dir with OV_<wave>_T/plan.resolved.json ...> -- evaluate the plan §4 'during' stop rules.
Stdlib only, read-only; prints a table of fits (billed core-h so far, state) and the flags. Exit 0 = no stop rule, 3 = STOP.
Thresholds (OVERLAP_1e4_SUBMISSION_PLAN §4, H-18): T fit > 172 core-h; V fit > 15; cumulative actual > 1,600; projection > 2,500;
wave actual > 2 x quote (W0 quote = 100 expected -> 200); any failed / TIMEOUT / OOM / CANCELLED stage that is not an infrastructure
fault (NODE_FAIL, BOOT_FAIL; SIGKILL by Slurm shows as NODE_FAIL / FAILED with a scheduler reason, judged by the manager);
> 2 failed fits in a wave; any QOS / MaxSubmit / Assoc pending reason; any engine resource_limit / admission / OUTCOME record;
X/y (truth.json X_sha256 + y_sha256: the DATA identity; data.bin content_sha256 also hashes the writing binary's meta block, so it differs between the T and V builds) must be equal across the fits of a dataset (design + rep; T and V and both seeds share it).
"""
import argparse, json, os, re, sys
from collections import defaultdict

T_FIT, V_FIT, CUM, PROJ = 172.0, 15.0, 1600.0, 2500.0
QUOTE = {"W0": 100.0}                      # expected core-h of the wave (plan §3); later waves: --quote
FITS_PER_ARM = 20
INFRA = {"NODE_FAIL", "BOOT_FAIL"}
BAD = {"FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED", "DEADLINE", "PREEMPTED", "REVOKED", "SUSPENDED"}
PEND_BAD = re.compile(r"QOS|Assoc|MaxSubmit|Invalid|Limit", re.I)


def sections(path):
    cur, out = None, defaultdict(list)
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("### "):
            cur = line[4:].strip(); out[cur]; continue
        if cur and line.strip():
            out[cur].append(line)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("probe"); ap.add_argument("--wave", required=True)
    ap.add_argument("--plans", required=True); ap.add_argument("--quote", type=float)
    ap.add_argument("--prior", help="JSON {run_id: core_h} of fits finished in earlier waves (cumulative.json)")
    a = ap.parse_args()
    S = sections(a.probe); flags = []
    runs = {}                                           # batch -> ordered run ids (plan order = array task order)
    arm = {}
    for b in ("OV_%s_T" % a.wave, "OV_%s_V" % a.wave):
        pr = json.load(open(os.path.join(a.plans, b, "plan.resolved.json")))
        runs[b] = [f["run_id"] for f in pr["fits"]]
        for r in runs[b]:
            arm[r] = b[-1]
    jobmap = {}                                         # (job id) -> (batch, run_id or None for all-fit arrays)
    for key, lines in S.items():
        if key.startswith("SUBMISSIONS "):
            b = key.split()[1]
            for l in lines:
                j = json.loads(l); jobmap[j["job"]] = (b, None if j["fit"] == "all" else j["fit"])
    cost, state, bad_stage, pend = defaultdict(float), defaultdict(set), [], []
    for l in S.get("SACCT", []):
        jid, name, st, el, cpus, cpuraw, lim = l.split("|")[:7]
        base, _, task = jid.partition("_")
        if base not in jobmap:
            continue
        b, fit = jobmap[base]
        if fit is None:
            if not task.isdigit():                      # a pending array row 123_[1-2]: no cost yet
                continue
            fit = runs[b][int(task) - 1]
        cost[fit] += int(cpuraw or 0) / 3600.0
        state[fit].add(st.split()[0])
        if st.split()[0] in BAD:
            bad_stage.append("%s %s %s" % (jid, name, st))
        if st.split()[0] in INFRA:
            flags.append("INFO infrastructure fault (not a stop rule; one rerun allowed, manager): %s %s %s" % (jid, name, st))
    for l in S.get("SQUEUE", []):
        i, n, st, rs = l.split("|")[:4]
        if st == "PENDING" and PEND_BAD.search(rs):
            pend.append("%s %s reason=%s" % (i, n, rs))
    prior = json.load(open(a.prior)) if a.prior else {}
    wave_cost = sum(cost.values()); cum = wave_cost + sum(prior.values())
    for r, c in sorted(cost.items()):
        lim = T_FIT if arm[r] == "T" else V_FIT
        if c > lim:
            flags.append("STOP fit %s cost %.1f core-h > %.0f" % (r, c, lim))
    quote = a.quote or QUOTE.get(a.wave)
    if quote and wave_cost > 2 * quote:
        flags.append("STOP wave %s actual %.1f > 2 x quote %.0f" % (a.wave, wave_cost, quote))
    if cum > CUM:
        flags.append("STOP cumulative %.1f > %.0f" % (cum, CUM))
    allc = dict(prior); allc.update(cost)               # projection: mean of fits whose stages are all COMPLETED x fits left
    done = {r for r, s in state.items() if s == {"COMPLETED"} and len(s) == 1}
    proj, parts = sum(allc.values()), []
    for x in ("T", "V"):
        fin = [allc[r] for r in done if arm.get(r) == x] + [prior[r] for r in prior if "-%s-" % x in r]
        started = sum(1 for r in allc if ("-%s-" % x) in r)
        if fin:
            m = sum(fin) / len(fin); proj += m * max(0, FITS_PER_ARM - started); parts.append("%s mean %.1f (%d fits)" % (x, m, len(fin)))
        else:
            parts.append("%s no finished fit yet" % x)
    if proj > PROJ:
        flags.append("STOP projection %.0f > %.0f" % (proj, PROJ))
    nonI = [x for x in bad_stage]
    if nonI:
        flags.append("STOP non-infrastructure failed stage(s): " + "; ".join(nonI))
    failed_fits = {r for r, s in state.items() if s & BAD}
    if len(failed_fits) > 2:
        flags.append("STOP > 2 failed fits in the wave: %s" % sorted(failed_fits))
    if pend:
        flags.append("STOP admission / QOS pending reason: " + "; ".join(pend))
    eng = [l for l in S.get("ENGINE_FLAGS", [])]
    if eng:
        flags.append("STOP engine record (OUTCOME / resource_limit / admission): " + "; ".join(eng))
    hashes = defaultdict(set)
    for l in S.get("DATA_HASH", []):
        b, r, h = l.split("|"); hashes[re.sub(r"-(T|V)-s\d$", "", r)].add(h)
    for ds, hs in hashes.items():
        if len(hs) > 1:
            flags.append("STOP X/y MISMATCH dataset %s: %d distinct X_sha256+y_sha256" % (ds, len(hs)))
    meta = next((k for k in S if k.startswith("META")), next((k for k in S.keys()), "") )
    meta = meta if meta.startswith("META") else "(no META line)"
    print("probe", meta, "| wave", a.wave)
    print("%-28s %9s  %s" % ("fit", "core-h", "stage states (sacct -X)"))
    for r in sorted(runs["OV_%s_T" % a.wave] + runs["OV_%s_V" % a.wave]):
        print("%-28s %9.2f  %s" % (r, cost.get(r, 0.0), ",".join(sorted(state.get(r, [])))))
    print("wave actual %.1f core-h (quote %s) | cumulative overlap %.1f | projection %.0f [%s]" % (wave_cost, quote, cum, proj, "; ".join(parts)))
    print("datasets with X/y hash seen: %d (all paired: %s)" % (len(hashes), all(len(h) == 1 for h in hashes.values())))
    for f in flags:
        print(f)
    stop = any(f.startswith("STOP") for f in flags)
    print("VERDICT:", "STOP SUBMITTING, tell the manager" if stop else "no stop rule fired")
    sys.exit(3 if stop else 0)


if __name__ == "__main__":
    main()
