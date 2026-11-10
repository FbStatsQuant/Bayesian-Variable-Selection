"""W3-SCR: summary tables for N1 (production fits: how often the printed condition holds) and N2 (boundary numerics).
Usage: py -3.13 summarise.py > SUMMARY_N1_N2.md"""
import glob, json, collections

rows = []
for f in sorted(glob.glob("n1_raw/*.jsonl") + glob.glob("n1b_raw/*.jsonl")):
    for l in open(f, encoding="utf-8"):
        if l.strip(): rows.append(json.loads(l)); break
print("# N1 — production core (main @ 2252d57, numerics/core_copy): frequency of the printed condition\n")
print("S0 has 4 truths, theta = bscale*(1.4,-1.0,1.8,-1.2), sigma = 1. 'cert' = fit$local_certified; '|S|<=8' = reported model of size <= 8;")
print("'cap' = a move cap was hit (local_limit); 'S0 in S' = reported model contains the truth; '= S0' exact.")
print("'cert&sparse&miss' = certified, size <= 8, and a truth missing (the event of the theorem).\n")
print("| design | n | p | bscale | fits | completed | cert | cert by (both/final/ls0/none) | cap | sizes of reported model (min/med/max) | cert & |S|<=8 | S0 in S | = S0 | cert&sparse&miss | LS0 start size (med) | median sec |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
grp = collections.defaultdict(list)
for r in rows:
    d = r["design"] + (f"({r['rho']})" if r["design"] in ("ar", "cs", "twin", "dupnoise") else f"(k={r['k']})" if r["design"] == "fac" else "")
    grp[(d, r["n"], r["p"], r["bscale"])].append(r)
med = lambda v: sorted(v)[len(v) // 2] if v else None
for key in sorted(grp):
    g = grp[key]; comp = [r for r in g if r["status"] in ("completed", "exact")]
    cert = [r for r in comp if r["local_certified"] is True]
    by = collections.Counter(r.get("local_certified_by") for r in comp)
    sz = [r["hpm_size"] for r in comp]
    cs = [r for r in cert if r["hpm_size"] <= 8]
    print(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {len(g)} | {len(comp)} | {len(cert)} | {by.get('both',0)}/{by.get('final',0)}/{by.get('ls0',0)}/{by.get('none',0)} | "
          f"{sum(1 for r in comp if r['local_limit'] is True)} | {min(sz) if sz else '-'}/{med(sz)}/{max(sz) if sz else '-'} | {len(cs)} | "
          f"{sum(1 for r in comp if r['hpm_contains_S0'])} | {sum(1 for r in comp if r['hpm_eq_S0'])} | {sum(1 for r in cs if not r['hpm_contains_S0'])} | "
          f"{med([r['start_mode_size'] for r in comp])} | {med([r['elapsed_sec'] for r in g])} |")
tot = [r for r in rows if r["status"] in ("completed", "exact")]
print(f"\nAll fits: {len(rows)}; completed {len(tot)}; certified {sum(1 for r in tot if r['local_certified'] is True)}; "
      f"certified and size <= 8: {sum(1 for r in tot if r['local_certified'] is True and r['hpm_size'] <= 8)}.")
print("\nUncertified completed fits (detail):")
for r in tot:
    if r["local_certified"] is not True:
        print(f"- {r['design']} n={r['n']} p={r['p']} bscale={r['bscale']} rep={r['rep']}: |S|={r['hpm_size']}, S0 in S: {r['hpm_contains_S0']}, hpm phase {r.get('hpm_phase')}, "
              f"final search: cert {r['final_search'].get('certified')} limit {r['final_search'].get('limit')} |ret|={r['final_search'].get('returned_size')} contains S0 {r['final_search'].get('contains_S0')}; "
              f"ls0: cert {r['ls0'].get('certified')} limit {r['ls0'].get('limit')} moves {r['ls0'].get('moves')} |ret|={r['ls0'].get('returned_size')} contains S0 {r['ls0'].get('contains_S0')}")
print("\nCertified archive endpoints (all completed fits): ", end="")
ce = [(r, a) for r in tot for a in (r["final_search"], r["ls0"]) if a.get("present") and a.get("certified")]
print(f"{len(ce)} certified endpoints; of size <= 8: {sum(1 for r, a in ce if a['returned_size'] <= 8)}; "
      f"of these missing a truth at bscale = 1: {sum(1 for r, a in ce if a['returned_size'] <= 8 and r['bscale'] == 1 and not a['contains_S0'])}; "
      f"at bscale < 1: {sum(1 for r, a in ce if a['returned_size'] <= 8 and r['bscale'] < 1 and not a['contains_S0'])}.")

print("\n# N2 — boundary numerics (own implementation of the coded search; 10 draws per scenario; n = 100, p = 400 unless noted)\n")
print("Each draw: coded local search (unlimited moves) from 24 starts (empty, truth, proxies, 10 random of size 5, 5 of size 15, 3 of size 30, 3 of size K-2 = 48, no truths in random starts); every endpoint is LO.\n")
print("| scenario | assumption violated | draws with an LO endpoint of size <= 8 missing a truth | ... size <= 16 | ... any size | draws where S0 is an endpoint | draws with an LO strict superset of S0 | endpoint sizes (0-8 / 9-16 / 17-49 / K) |")
print("|---|---|---|---|---|---|---|---|")
mg = "none asymptotically; at n = 100 the visibility margin is not met at the offending model (noiseless ratio 0.8-1.2, n2_out/DIAG_visibility.txt)"
viol = dict(iid_strong="none", cs_strong=mg, fac_strong=mg, ar_strong="none", fac_p1000="none found (p = 1000)", iid_weak="visibility (weak signal)",
            twin90="identifiability margin (twin r=.9)", twin99="identifiability margin (twin r=.99)", twin999="identifiability margin (twin r=.999)",
            masked="visibility only (masked pair; margin holds)", noisecs98="sparse floor only (anchored floor holds)", dupnoise="sparse floor (near-duplicate noise columns); the one miss is a visibility-margin failure at n = 100 (ratio 0.80)")
pairs = []
for f in sorted(glob.glob("n2_out/*.txt")):
    S = None
    for l in open(f, encoding="utf-8", errors="replace"):
        if l.startswith("SUMMARY "): S = json.loads(l[8:])
    if S is None: continue
    if S["scenario"].startswith("pairs"): pairs.append(S); continue
    es = S["endpoint_sizes"]; Kk = [k for k in es if k.startswith("K=")]; mid = [k for k in es if k.startswith("17-")]
    print(f"| {S['scenario']} | {viol.get(S['scenario'], '?')} | {S['draws_with_LO_missing_q8']}/{S['reps']} | {S['draws_with_LO_missing_q16']}/{S['reps']} | {S['draws_with_LO_missing_any_size']}/{S['reps']} | "
          f"{S['draws_S0_is_LO']}/{S['reps']} | {S['draws_with_LO_strict_superset']}/{S['reps']} | {es.get('0-8', 0)} / {es.get('9-16', 0)} / {sum(es[k] for k in mid)} / {sum(es[k] for k in Kk)} |")
print("\nSCR-C boundary: LO supersets of the form S0 + {j, l} (exhaustive over pairs, strong signals):\n")
print("| scenario | draws where S0 is LO | LO pair-supersets per draw | draws with at least one LO strict superset (pair or single) |")
print("|---|---|---|---|")
for S in pairs:
    print(f"| {S['scenario']} | {S['draws_S0_is_LO']}/{S['reps']} | {S['LO_pair_supersets']} | {S['draws_with_LO_strict_superset']}/{S['reps']} |")
