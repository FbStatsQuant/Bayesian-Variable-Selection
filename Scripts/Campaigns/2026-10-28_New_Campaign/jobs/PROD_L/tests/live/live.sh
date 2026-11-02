#!/bin/bash
# Live local integration of PROD-L's batch_runner.sh with the REAL CLIs (run_case.R v2.2.1, run_enum_dataset.R) on production ids of the sealed
# study. Throwaway staged layout under W; nothing outside W is written (the frozen tree and the sealed study are COPIED in).
set -euo pipefail
W=/c/Users/felip/AppData/Local/Temp/prodl_live/w
CAMP=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign
SEALED="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study"
STAMP=20261030T0000Z; export STAMP
[ ! -e "$W" ] || { echo "W exists: use a fresh folder" >&2; exit 2; }
RH=$W/home/runs/${STAMP}_lowp_prodL
mkdir -p "$RH/code/core" "$RH/code/lowp" "$W/scr"
cp -R "$CAMP/code/core/v2_2_1" "$RH/code/core/v2_2_1"; cp "$CAMP/code/core/v2_2_1.SHA256SUMS" "$RH/code/core/"
cp -R "$CAMP/code/lowp/enum" "$RH/code/lowp/enum"; cp -R "$CAMP/code/lowp/R" "$RH/code/lowp/R"
cp -R "$CAMP/jobs/PROD_L" "$RH/code/prod_l"
cp -R "$SEALED" "$RH/study"; chmod -R u+w "$RH/study"
export NC_HOME_ROOT=$W/home NC_SCR_ROOT=$W/scr PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN=/c/Users/felip/AppData/Local/Temp/prodl_live/gnutime_shim.sh
export PATH="/c/Program Files/R/R-4.4.1/bin:$PATH"
U=$W/units.tsv
printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$U"
printf 'smc\t0\tp0020_S1_r001_c100\tp0020_S1_r001\tc100\t0\n' >> "$U"
printf 'smc\t0\tp0030_S4_r050_c050\tp0030_S4_r050\tc050\t0\n' >> "$U"
printf 'smcrep\t0\tp0020_S1_r001_c100_rep2\tp0020_S1_r001\tc100\t2\n' >> "$U"
printf 'enum20\t0\tp0020_S1_r001\tp0020_S1_r001\t-\t0\n' >> "$U"
run() {  # run PIECE ARM : what the sbatch script does, then source the runner
  ( set -euo pipefail; PRODL_T0=$(date +%s); HOME_ROOT=$NC_HOME_ROOT
    source "$HOME_ROOT/runs/${STAMP}_lowp_prodL/code/prod_l/prodl.env"
    R_LIBS_USER_LOWP="C:/Users/felip/AppData/Local/R/win-library/4.4"   # laptop only: prodl.env carries the NOTS library path
    source "$PILOT_DIR/slurm/common.sh"
    pilot_init "$2"; pilot_modules lowp; pilot_blas_single
    [ "$1" = enum20 ] || pilot_require_frozen
    PIECE=$1; UNITS_FILE=$U; TASK_ID=0; wv=WALL_$1; bv=BUDGET_$1; PRODL_WALL_S=${!wv}; UNIT_BUDGET_S=${!bv}; P5=0
    source "$PILOT_DIR/batch_runner.sh" ) && rc=0 || rc=$?; echo "RUN $1 rc=$rc"
}
run smc smc
run smcrep smcrep
run enum20 enum20
echo "== second pass (idempotence: every unit must come back skipped). A real resubmission has a NEW job id; the SAME id is refused (R1 F3)"
SLURM_ARRAY_JOB_ID=9002 run smc smc
echo "== third pass with the SAME job tag as the first (local_0): must be refused, start_record_exists, ledger untouched"
run smc smc
cat "$W/scr/logs/${STAMP}_lowp_prodL/refusals/local_0.txt"
echo "== ledger"
find "$W/scr/logs" -path '*ledger*' -type f | sort | while read -r f; do echo "$f: $(cat "$f")"; done
echo "== inventories"; find "$W/scr/logs" -path '*inventory*' -name '*.tsv' | sort | while read -r f; do echo "-- $f"; cat "$f"; done
echo "== results"; find "$W/scr/results" -type f | sort
echo "== reconcile (expect exit 1: only 4 of 15,600 units exist)"
py -3 "$RH/code/prod_l/reconcile_prodl.py" "$STAMP" --home-root "$W/home" --scr-root "$W/scr" --out "$W/inv" > "$W/reconcile.out" 2>&1 || echo "reconcile rc=$?"
cat "$W/inv/INVENTORY.md" | head -30
grep -h -E 'p0020_S1_r001_c100|p0030_S4_r050_c050|p0020_S1_r001\b' "$W/inv/inventory/"*.tsv | head
