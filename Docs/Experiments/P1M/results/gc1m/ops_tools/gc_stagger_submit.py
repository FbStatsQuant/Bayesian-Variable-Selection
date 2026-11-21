#!/usr/bin/env python3
"""gc_stagger_submit.py <scripts/GC_W<n>> -- STAGGERED island arrays for a 1M PAIR wave (HQ H-51, approved for W2 onward). Writes <dir>/submit_stagger.sh from the driver's own submit.sh with ONE change: the island array of fit i > 1 also waits
`--dependency=...,afterany:<island array job of fit i-1>`, so the 2 x 16 islands of a pair no longer compete for the 1,536-CPU QOS cap (the second fit's islands start only when the first fit's array has ended). Pacing stays 2 fits per wave;
no engine change, no plan or stage-script change (the file is NEW and not in SHA256SUMS; the original submit.sh is untouched). Dry run: prints the diff and `bash -n`. Usage: gc_stagger_submit.py scripts/GC_W<n> [--throttle N]   (--throttle 8: HQ H-52, the %8 island-array throttle per fit when the mean pre-engine wait of the previous wave was > 300 s; default: the plan's %16)"""
import difflib, os, re, subprocess, sys
d = sys.argv[1]; src = open(os.path.join(d, "submit.sh")).read()
thr = None
if "--throttle" in sys.argv:
    thr = int(sys.argv[sys.argv.index("--throttle") + 1]); assert 1 <= thr <= 16
old = 'ji=$("$SB" --parsable --array=1-$rp%16 --dependency=afterok:${jc}_$i stage_islands.sbatch $i); log islands "${RUNS[$((i-1))]}" "$ji"'
assert old in src, "the driver's island line is not as expected"
new = 'ji=$("$SB" --parsable --array=1-$rp%16 --dependency=afterok:${jc}_$i${JIPREV:+,afterany:$JIPREV} stage_islands.sbatch $i); log islands "${RUNS[$((i-1))]}" "$ji"; JIPREV=$ji   # H-51 stagger: fit i>1 waits for fit i-1\'s island array (afterany)'
out = src.replace(old, new, 1)
if thr is not None:
    assert out.count("--array=1-$rp%16") == 1
    out = out.replace("--array=1-$rp%16", "--array=1-$rp%%%d" % thr, 1).replace("# H-51 stagger:", "# H-52 throttle %%%d per fit; H-51 stagger:" % thr, 1)
assert out.count("JIPREV") == 3 and "set -euo pipefail" in out
out = out.replace("# submit.sh -- P1M batch", "# submit_stagger.sh (H-51 stagger of the island arrays; derived from the driver's submit.sh by gc_stagger_submit.py) -- P1M batch", 1)
p = os.path.join(d, "submit_stagger.sh"); open(p, "w").write(out); os.chmod(p, 0o755)
rc = subprocess.run(["bash", "-n", p]).returncode
print("".join(l for l in difflib.unified_diff(src.splitlines(True), out.splitlines(True), "submit.sh", "submit_stagger.sh", n=0) if not l.startswith(("---", "+++"))), end="")
print("bash -n: %s; written %s" % ("ok" if rc == 0 else "FAILED", p)); sys.exit(rc)
