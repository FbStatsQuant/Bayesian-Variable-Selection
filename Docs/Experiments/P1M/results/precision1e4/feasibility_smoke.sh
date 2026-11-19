#!/usr/bin/env bash
# feasibility_smoke.sh -- the F-feasibility checks of LEG_PLAN section 1, on a TINY dataset (n = 100, p = 400; 2 threads, nice; seconds).
# Binary: an Owls build of engine commit dc0474eb, whose engine src (outside src/xeval) is byte-identical to the frozen F = eefcbc4a
# (`git diff eefcbc4a dc0474eb -- src include` = xeval only). Writes only under $D (default: the department tmp). Never touches NOTS.
set -u
B=${B:-$HOME/SMC_Engineering_Department/tmp/20261118-xeval/after_build/smcbvs4}
D=${D:-$HOME/SMC_Engineering_Department/tmp/20261119-precplan/smoke}
mkdir -p "$D" && cd "$D" || exit 1
N="nice -n 19 taskset -c 0-1"
j() { python3 -c "import json,sys; j=json.load(open('$1')); print({k: j.get(k) for k in sys.argv[1:]})" "${@:2}"; }
$N $B gen --design AR --n 100 --p 400 --seed 11 --a 1 --out raw.bin --truth truth.json > gen.log 2>&1; $N $B prep --in raw.bin --out data.bin > prep.log 2>&1
$N $B setup --data data.bin --out setup.bin --file_mode V --threads 2 > setup.log 2>&1
echo "[A3] setup --partition exact_linkage (the manifest's value):"; $N $B setup --data data.bin --out s_exl.bin --file_mode V --partition exact_linkage --threads 2 > s_exl.log 2>&1; echo "  rc=$?"; j s_exl.bin.json status reason
echo "[A3] setup --partition exact:"; $N $B setup --data data.bin --out s_ex.bin --file_mode V --partition exact --threads 2 > s_ex.log 2>&1; echo "  rc=$?"; j s_ex.bin.json status partition
echo "[m, I_max] calibrate --I_max 0 --refine_m 4 / --refine_m 1 (same seed):"
$N $B calibrate --mode V --data data.bin --setup setup.bin --seed 7 --I_max 0 --refine_m 4 --threads 2 --out c_m4.bin > c_m4.log 2>&1; echo "  m4 rc=$?"
$N $B calibrate --mode V --data data.bin --setup setup.bin --seed 7 --I_max 0 --refine_m 1 --threads 2 --out c_m1.bin > c_m1.log 2>&1; echo "  m1 rc=$?"
python3 - <<'PY'
import json
for f in ("c_m4", "c_m1"):
    s = json.load(open(f + ".bin.json"))["settings"]; print("  ", f, "refine_m", s["refine_m"], "I_max", s["I_max"], "N_final", s["tiers"][0]["N_final"])
PY
for c in c_m1 c_m4; do $N $B island --mode V --data data.bin --setup setup.bin --calib $c.bin --island 1 --seed 7 --threads 2 --out i_$c.bin > i_$c.log 2>&1; python3 -c "import json; j=json.load(open('i_$c.bin.json')); print('   island T (grid stages) after $c:', j['T'], 'N', j['N'])"; done
echo "[placeholder names] calibrate --grid_refine_m 4 --calib_seed 5 (the plan's names): ignored?"
$N $B calibrate --mode V --data data.bin --setup setup.bin --seed 7 --I_max 0 --grid_refine_m 4 --calib_seed 5 --threads 2 --out c_ign.bin > c_ign.log 2>&1; echo "  rc=$?"
python3 -c "import json; s=json.load(open('c_ign.bin.json'))['settings']; print('   refine_m', s['refine_m'], '(4 would mean honoured)')"
echo "[B1] island with a seed different from the calibration's:"; $N $B island --mode V --data data.bin --setup setup.bin --calib c_m1.bin --island 1 --seed 8 --threads 2 --out i_bad.bin > i_bad.log 2>&1; echo "  rc=$?"; j i_bad.bin.json status reason
echo "[B2] calibrate --N 10000 (V), then island --N 10000:"
$N $B calibrate --mode V --data data.bin --setup setup.bin --seed 7 --I_max 0 --N 10000 --threads 2 --out c_N.bin > c_N.log 2>&1; echo "  calibrate rc=$?"; python3 -c "import json; print('   N_final', json.load(open('c_N.bin.json'))['settings']['tiers'][0]['N_final'])"
$N $B island --mode V --data data.bin --setup setup.bin --calib c_m1.bin --island 1 --seed 7 --N 10000 --threads 2 --out i_badN.bin > i_badN.log 2>&1; echo "  island rc=$?"; j i_badN.bin.json status reason
