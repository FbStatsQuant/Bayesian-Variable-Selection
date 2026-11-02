"""Overall counts across every LH-iid replicate of this run (results/lh_*.jsonl). Output: ../results/overall.txt"""
import json, glob
R = []
for f in sorted(glob.glob("../results/lh_[A-Z]*.jsonl")):
    R += [json.loads(l) for l in open(f)]
inside = [r for r in R if r["cfg"] != "OUT_PSI"]
s = [f"replicates: {len(R)} ({len(inside)} inside LH-iid)",
     f"T22(i) lower bound <= pi0(S°): {sum(r['t22_ok'] for r in R)}/{len(R)}",
     f"inside the family: partition = groups {sum(r['blocks_eq_groups'] for r in inside)}/{len(inside)}; "
     f"mode = S° {sum(r['mode_eq_ref'] for r in inside)}/{len(inside)}; LS0 scored S0 {sum(r['ls_scored'] for r in inside)}/{len(inside)}; "
     f"LS0 certified at S0 {sum(r['ls_cert_S0'] for r in inside)}/{len(inside)}"]
print("\n".join(s)); open("../results/overall.txt", "w").write("\n".join(s) + "\n")
