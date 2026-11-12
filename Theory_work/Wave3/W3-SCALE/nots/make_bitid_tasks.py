"""Write the task files of the W3-SCALE bit-identity runs (v3.1 vs v3.2-dev on NOTS).

Usage: python make_bitid_tasks.py V32_COMMIT OUT_DIR
One PROD-H unit per cell (p x scenario x scale), replicate r001: 24 units, each run once per core (48 tasks), split by
time limit; plus the supplementary units and the header-level unit harness; plus setup-only comparisons at larger p.
"""
import sys, os

v32_commit, out = sys.argv[1], sys.argv[2]
BASE = "/scratch/fb31/w3scale"
CORE = {"v31": f"{BASE}/code/v31_613f063/Scripts/SMC_BVS/core",
        "v32": f"{BASE}/code/v32dev_{v32_commit}/Scripts/SMC_BVS/core_v32dev"}
FLAGS = "-std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2"


def fit_cmd(label, units):
    return (f"Rscript --vanilla bitid_fit.R --core-dir {CORE[label]} --label {label} "
            f"--units {','.join(units)} --out-dir $OUT/res")


def write(name, cmds):
    with open(os.path.join(out, name), "w", newline="\n") as f:
        for i, c in enumerate(cmds, 1):
            f.write(f"{i}\t{c}\n")
    print(name, len(cmds))


def cells(p, scen):
    return [f"prodh:p{p:04d}_S{s}_r001_{c}" for s in scen for c in ("c100", "c050")]


supp = ["exact_p10", "exact_p12_dup_const", "exact_p14_integer", "smc_p40_dup", "smc_p60_n30", "smc_p48_integer",
        "near_constant", "y_constant", "no_predictors", "tie_dp_p400"]
units_cmd = (f"g++ {FLAGS} -I{CORE['v31']}/cpp bitid_units.cpp -o $TMPDIR/u31 && "
             f"g++ {FLAGS} -DHAVE_V31_REFS -I{CORE['v32']}/cpp bitid_units.cpp -o $TMPDIR/u32 && "
             "$TMPDIR/u31 $TMPDIR/d31.bin big > $OUT/res/units_v31.txt && $TMPDIR/u32 $TMPDIR/d32.bin big > $OUT/res/units_v32.txt && "
             "sha256sum $TMPDIR/d31.bin $TMPDIR/d32.bin > $OUT/res/units_sha.txt && cmp $TMPDIR/d31.bin $TMPDIR/d32.bin && "
             "echo UNITS_DUMPS_IDENTICAL > $OUT/res/units_verdict.txt")
write("bitid_supp.tsv", [units_cmd] + [fit_cmd(l, [f"supp:{u}" for u in supp]) for l in ("v31", "v32")])
write("bitid_p500.tsv", [fit_cmd(l, [u]) for u in cells(500, (1, 2, 3, 4, 6)) for l in ("v31", "v32")])
write("bitid_p500_S5.tsv", [fit_cmd(l, [u]) for u in cells(500, (5,)) for l in ("v31", "v32")])
write("bitid_p1000.tsv", [fit_cmd(l, [u]) for u in cells(1000, (1, 2, 3, 4, 6)) for l in ("v31", "v32")])
write("bitid_p1000_S5.tsv", [fit_cmd(l, [u]) for u in cells(1000, (5,)) for l in ("v31", "v32")])
setup = []
for p, mem in ((5000, 12), (10000, 16), (20000, 32)):
    for l in ("v31", "v32"):
        setup.append(f"Rscript --vanilla profile_fit.R --core-dir {CORE[l]} --design s3gen --p {p} --seed 20261111 "
                     f"--mode setup --mem-gb {mem} --hours 1 --out $OUT/res/setup_p{p}_{l}.rds")
write("setup_cmp.tsv", setup)
