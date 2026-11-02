"""Summarise exp1 / exp2 JSON outputs into markdown tables (stdout)."""
import json, sys, collections
import numpy as np


def exp1(path):
    D = json.load(open(path))
    print(f"\n### {path.split('/')[-1]}  ({len(D)} datasets)\n")
    keys = ["a4_d0", "a4_d1", "a4_d2", "a1_d1", "a2_d1", "a2_d2"] if "a4_d0" in D[0] else \
           ["a5_d0", "a5_d1", "a5_d2", "a1_d1", "a2_d1", "a2_d2"]
    print("| scen | c | S0 locmax | litTD(0) | litTD(1) | " + " | ".join(f"{k} TD'P / TD'inf / PD / path" for k in keys) + " |")
    print("|" + "---|" * (5 + len(keys)))
    groups = collections.defaultdict(list)
    for r in D:
        groups[(r["scenario"], r["c"])].append(r)
    beaten = collections.Counter(); fail0 = collections.Counter(); nonprog = collections.Counter()
    for (s, c), rs in sorted(groups.items()):
        row = [str(s), str(c), f"{np.mean([r['S0_local_max'] for r in rs]):.2f}",
               f"{np.mean([r['literal_TD0'] for r in rs]):.2f}", f"{np.mean([r['literal_TD1_any'] for r in rs]):.2f}"]
        for k in keys:
            row.append("{:.2f} / {:.2f} / {:.2f} / {:.2f}".format(
                np.mean([r[k]["TDP"] for r in rs]), np.mean([r[k]["TDinf"] for r in rs]),
                np.mean([r[k]["PD"] for r in rs]), np.mean([r[k]["path_ok_frac"] == 1.0 for r in rs])))
        print("| " + " | ".join(row) + " |")
        for r in rs:
            if not r["S0_local_max"]:
                beaten[r["S0_beaten_by"]] += 1
            for kk, v in r["TD0_fail_classes"].items():
                fail0[kk] += v
            for kk, v in r[keys[2]]["nonprog"].items():
                nonprog[kk] += v
    print(f"\nS0 beaten by (count of datasets): {dict(beaten)}")
    print(f"literal TD(0) failing states by best-move class (summed over datasets): {dict(fail0)}")
    print(f"non-progress greedy moves on R_(s0,2) states (summed): {dict(nonprog)}")
    # conditional on PD(R_d) / S0 locmax
    for k in keys:
        sel = [r for r in D if r[k]["PD"] and r["S0_local_max"]]
        if sel:
            print(f"{k}: among datasets with PD & S0 locmax ({len(sel)}): TD'P {np.mean([r[k]['TDP'] for r in sel]):.2f}, "
                  f"TD'inf {np.mean([r[k]['TDinf'] for r in sel]):.2f}, max moves {max(r[k]['max_moves'] for r in sel)}, "
                  f"over-Phi paths {sum(r[k]['over_phi'] for r in sel)}")
    ex = [e for r in D for e in r["diag_examples"]]
    ex.sort(key=lambda e: -e["gap"])
    print("\nlargest non-progress-beats-progress examples (state, class, gap nats, delta(missing): (j, delta, noise), delta(in)):")
    for e in ex[:6]:
        print("  ", e["S"], e["lab"], f"gap={e['gap']:.2f}", "m,e=", e["m"], e["e"],
              [(j, round(a, 2), round(b, 2)) for j, a, b in e["delta_missing"]],
              (e["delta_in"][0], None if e["delta_in"][1] is None else round(e["delta_in"][1], 2),
               None if e["delta_in"][2] is None else round(e["delta_in"][2], 2)), "out", e["out"])
    cl = collections.Counter(e["lab"] for r in D for e in r["diag_examples"])
    print("classes among recorded examples:", dict(cl))


def exp2(path):
    D = json.load(open(path))
    print(f"\n### {path.split('/')[-1]}  ({len(D)} datasets)\n")
    print("| scen | c | S0 locmax | S0 beaten by | median best del gain at S0 | median best add gain at S0 | "
          "d0 frac progress | centres: PD | reached | reached given PD | all-progress given reached | max moves |")
    print("|" + "---|" * 12)
    groups = collections.defaultdict(list)
    for r in D:
        groups[(r["scenario"], r["c"])].append(r)
    for (s, c), rs in sorted(groups.items()):
        cents = [x for r in rs for x in r["centres"]]
        pd = [x for x in cents if x["PD"]]
        rc = [x for x in cents if x["reached"]]
        by = collections.Counter(r.get("S0_beaten_by") for r in rs if not r["S0_local_max"])
        print(f"| {s} | {c} | {np.mean([r['S0_local_max'] for r in rs]):.2f} | {dict(by)} | "
              f"{np.median([r['S0_best_del_gain'] for r in rs]):.1f} | {np.median([r['S0_best_add_gain'] for r in rs]):.1f} | "
              f"{np.mean([r['d0_frac_prog'] for r in rs]):.3f} | {np.mean([x['PD'] for x in cents]):.2f} | "
              f"{np.mean([x['reached'] for x in cents]):.2f} | "
              f"{(np.mean([x['reached'] for x in pd]) if pd else float('nan')):.2f} | "
              f"{(np.mean([x['allprog'] for x in rc]) if rc else float('nan')):.2f} | "
              f"{max([x['n'] for x in rc], default=0)} |")
    allc = [x for r in D for x in r["centres"]]
    print(f"\nall centres: {len(allc)}; PD {np.mean([x['PD'] for x in allc]):.3f}; reached {np.mean([x['reached'] for x in allc]):.3f}")
    lm = [r for r in D if r["S0_local_max"]]
    cl = [x for r in lm for x in r["centres"]]
    print(f"datasets with S0 local max: {len(lm)}/{len(D)}; their centres reached S0: {np.mean([x['reached'] for x in cl]):.3f}; "
          f"all-progress among reached {np.mean([x['allprog'] for x in cl if x['reached']]):.3f}")
    nr = [x for x in cl if not x["reached"]]
    print(f"  not reached although S0 local max: {len(nr)}; their PD: {[x['PD'] for x in nr][:20]}; "
          f"end (m,e,gain): {[(x['end_m'], x['end_e'], round(x['end_gain'], 1)) for x in nr][:20]}")
    labs = collections.Counter(l for x in allc if x["reached"] for l in x["labs"])
    print("move classes used on successful paths:", dict(labs))
    labs_f = collections.Counter(l for x in allc if not x["reached"] for l in x["labs"])
    print("move classes used on failed paths:", dict(labs_f))
    d0 = collections.Counter()
    for r in D:
        for k, v in r["d0_classes"].items(): d0[k] += v
    print("greedy move classes at the 105 d=0 states (m<=2), summed:", dict(d0))
    eg = [r["S0_greedy_end_gain"] for r in D if not r["S0_local_max"]]
    if eg:
        print(f"posterior-miss margin lower bounds F(S*)-F(S0) when S0 not local max: median {np.median(eg):.2f}, "
              f"range [{min(eg):.2f}, {max(eg):.2f}]; S* (m,e): {[ (r['S0_greedy_end']['m'], r['S0_greedy_end']['e']) for r in D if not r['S0_local_max']]}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        (exp2 if "exp2" in p else exp1)(p)
