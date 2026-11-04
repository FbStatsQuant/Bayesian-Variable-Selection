"""make_synthetic.py -- ABL-CONF dry-run inputs: synthetic per_fit.csv / reference.csv tables in the format written by
summarise.R (only the columns apply_rule.py reads, plus a few for readability). Fixed RNG seed; no fits involved.
Usage: python3 make_synthetic.py <out_dir>     -> <out_dir>/<scenario>/{per_fit.csv,reference.csv}
Scenarios (3 designs x 10 seeds x arms A,B,C; reference K=8, se 0.03; guard pool KB=4):
  expected       A cheaper than B on S1/S5 at equal accuracy, B capped on all S4 seeds; C underestimates by ~8 nats
  no_difference  all three arms drawn from the same cost and error distributions
  B_fails_badly  B capped or failed on every seed of every design; A, C as in 'expected'
  C_fails_badly  C off by ~30 nats with huge spread and capped on 3/10 seeds per design; A, B as in 'expected'
  reversed       B cheaper and more accurate than A (A biased by +1.5 nats); C unbiased and more accurate than A
  guard_fails    as 'expected', but the reserved arm-B pool disagrees with the arm-A reference by 2 nats
"""
import csv, os, random, sys

DES = [("p0500_S1_r001 c100", "S1"), ("p0500_S4_r001 c100", "S4"), ("p0500_S5_r001 c100", "S5")]
CAP = 4500.0
COLS = ["name", "design", "scen", "role", "arm", "k", "status", "wall_s", "log_Z", "log_Zref", "se_ref", "err_logZ",
        "pip_zw_max", "sd_logZ_r"]

def scenario(name, rng):
    rows, refs = [], []
    for d, sc in DES:
        lzref = {"S1": -69.6, "S4": -65.8, "S5": -105.4}[sc]; se = 0.03
        refs.append(dict(design=d, scen=sc, K=8, log_Zref=lzref, se_ref=se, KB=4 if sc == "S1" else 0,
                         log_ZrefB=(lzref + (2.0 if name == "guard_fails" else rng.gauss(0, 0.03))) if sc == "S1" else "NA",
                         se_refB=0.04 if sc == "S1" else "NA"))
        for k in range(1, 11):
            base = rng.uniform(500, 1700)
            for arm in "ABC":
                st, wall, err, pip, sd = "completed", base * rng.uniform(0.9, 1.1), rng.gauss(0, 0.08), rng.uniform(0, .004), 0.08
                if name == "no_difference":
                    pass
                elif arm == "B" and name in ("expected", "C_fails_badly", "guard_fails"):
                    if sc == "S4": st, wall = "capped", CAP
                    else: wall = base * rng.uniform(1.1, 2.5)
                elif arm == "B" and name == "B_fails_badly":
                    st, wall = ("capped", CAP) if k % 3 else ("failed", 200.0)
                elif arm == "B" and name == "reversed":
                    wall = base * rng.uniform(0.4, 0.7)
                elif arm == "A" and name == "reversed":
                    err = 1.5 + rng.gauss(0, 0.08); pip = rng.uniform(0.02, 0.06)
                elif arm == "C" and name in ("expected", "B_fails_badly", "guard_fails"):
                    wall = rng.uniform(2000, 3300); err = -abs(rng.gauss(8, 3)); pip = rng.uniform(0, .01); sd = 2.0
                elif arm == "C" and name == "C_fails_badly":
                    if k in (2, 5, 9): st, wall = "capped", CAP
                    else: wall = rng.uniform(3000, 4400); err = -abs(rng.gauss(30, 10)); pip = rng.uniform(0.1, 0.9); sd = 8.0
                elif arm == "C" and name == "reversed":
                    wall = rng.uniform(2000, 3300)
                ok = st == "completed"
                rows.append(dict(name=f"{d.replace(' ', '_')}_{arm}_test{k:02d}", design=d, scen=sc, role="test", arm=arm,
                                 k=k, status=st, wall_s=round(wall, 1), log_Z=round(lzref + err, 4) if ok else "NA",
                                 log_Zref=lzref, se_ref=se, err_logZ=round(err, 4) if ok else "NA",
                                 pip_zw_max=round(pip, 5) if ok else "NA", sd_logZ_r=sd if ok else "NA"))
    return rows, refs

if __name__ == "__main__":
    out = sys.argv[1]; rng = random.Random(20261103)
    for sc in ["expected", "no_difference", "B_fails_badly", "C_fails_badly", "reversed", "guard_fails"]:
        rows, refs = scenario(sc, rng); os.makedirs(os.path.join(out, sc), exist_ok=True)
        with open(os.path.join(out, sc, "per_fit.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
        with open(os.path.join(out, sc, "reference.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(refs[0])); w.writeheader(); w.writerows(refs)
