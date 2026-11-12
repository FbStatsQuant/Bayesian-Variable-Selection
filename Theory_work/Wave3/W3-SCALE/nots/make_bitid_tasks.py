"""Write the task files of the W3-SCALE bit-identity runs (v3.1 vs v3.2-dev on NOTS).

Usage: python make_bitid_tasks.py V32_COMMIT OUT_DIR [SUFFIX]
Without SUFFIX (first round, v3.2-dev revision A): one PROD-H unit per cell (p x scenario x scale), replicate r001,
24 units, each run once per core (48 tasks), split by time limit; the supplementary units and the header-level unit
harness; setup-only comparisons at larger p.
With SUFFIX (a later v3.2-dev revision, e.g. _C): the PROD-H units are run under the new v3.2-dev revision only (the
v3.1 records of the first round are reused); the unit harness, the R-export test, the fingerprint self-test, the
supplementary units (both cores) and the setup-only comparisons (both cores, with the Gram hash) are run again; one
task recomputes the version-2 fingerprints of the first round's saved fits.
"""
import sys, os

v32_commit, out = sys.argv[1], sys.argv[2]
suffix = sys.argv[3] if len(sys.argv) > 3 else ""
BASE = "/scratch/fb31/w3scale"
CORE = {"v31": f"{BASE}/code/v31_613f063/Scripts/SMC_BVS/core",
        "v32": f"{BASE}/code/v32dev_{v32_commit}/Scripts/SMC_BVS/core_v32dev"}
FLAGS = "-std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2"
labels = ("v32",) if suffix else ("v31", "v32")


def fit_cmd(label, units):
    return (f"Rscript --vanilla bitid_fit.R --core-dir {CORE[label]} --label {label} "
            f"--units {','.join(units)} --out-dir $OUT/res")


def write(name, cmds):
    name = name.replace(".tsv", suffix + ".tsv")
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
supp_tasks = [units_cmd] + [fit_cmd(l, [f"supp:{u}" for u in supp]) for l in ("v31", "v32")]
if suffix:
    supp_tasks.append(f"Rscript --vanilla export_units.R --core-dir {CORE['v31']} --out $OUT/res/exports_v31.rds && "
                      f"Rscript --vanilla export_units.R --core-dir {CORE['v32']} --out $OUT/res/exports_v32.rds && "
                      "Rscript --vanilla export_units.R --compare $OUT/res/exports_v31.rds $OUT/res/exports_v32.rds > $OUT/res/exports_verdict.txt")
    first = " ".join(f"{BASE}/out/{r}/res" for r in ("bitid_supp", "bitid_p500", "bitid_p500_S5", "bitid_p1000", "bitid_p1000_S5"))
    supp_tasks.append(f"Rscript --vanilla refingerprint.R {first} > $OUT/res/refingerprint.txt && "
                      f"Rscript --vanilla fingerprint_selftest.R {BASE}/out/bitid_p1000_S5/res/p1000_S5_r001_c100__v31.fit.rds "
                      f"{BASE}/out/bitid_p500/res/p0500_S3_r001_c050__v32.fit.rds {BASE}/out/bitid_supp/res/exact_p10__v31.fit.rds "
                      f"{BASE}/out/bitid_supp/res/tie_dp_p400__v32.fit.rds > $OUT/res/selftest.txt")
write("bitid_supp.tsv", supp_tasks)
write("bitid_p500.tsv", [fit_cmd(l, [u]) for u in cells(500, (1, 2, 3, 4, 6)) for l in labels])
write("bitid_p500_S5.tsv", [fit_cmd(l, [u]) for u in cells(500, (5,)) for l in labels])
write("bitid_p1000.tsv", [fit_cmd(l, [u]) for u in cells(1000, (1, 2, 3, 4, 6)) for l in labels])
write("bitid_p1000_S5.tsv", [fit_cmd(l, [u]) for u in cells(1000, (5,)) for l in labels])
setup = []
for p, mem in ((5000, 12), (10000, 16), (20000, 32)):
    for l in ("v31", "v32"):
        setup.append(f"Rscript --vanilla profile_fit.R --core-dir {CORE[l]} --design s3gen --p {p} --seed 20261111 "
                     f"--mode setup --mem-gb {mem} --hours 1 --out $OUT/res/setup_p{p}_{l}.rds")
write("setup_cmp.tsv", setup)
