#!/bin/bash
# Live local run of the PROD-L benchmark wave machinery with the REAL frozen CLI (run_bench_case.R, r2) on production ids of the sealed study.
# Throwaway layout under W, built by EXTRACTING the real staging tar (stage_local.sh), so staging is exercised too. Laptop R 4.4.1 and the
# laptop test library through the local-test hook (PRODL_BENCH_EXTRA="--test-library" + LOWP_SMOKE_ALLOW_VERSION_MISMATCH=1): structure,
# runner wiring, resume, refusal, reconcile and acceptance are tested; provenance (R 4.5.2, pinned library) is NOT (acceptance --local-test).
# One R process at a time.
set -euo pipefail
B=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/jobs/PROD_L_BENCH
W=${LIVE_W:-/c/Users/felip/AppData/Local/Temp/prodlb_live/w}   # rev 2 (HQ D82): LIVE_W selects a fresh folder; the rev-1 folder w is kept (test_accept.sh reads it)
SEALED="/c/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study"
STAMP=20261030T0001Z; export STAMP
[ ! -e "$W" ] || { echo "W exists: use a fresh folder" >&2; exit 2; }
mkdir -p "$W/home" "$W/scr"
bash "$B/stage_local.sh" --sealed "$SEALED" --stamp "$STAMP" --out "$W/bundle"
tar -xf "$W/bundle/prodLB_bundle_$STAMP.tar" -C "$W/home"
( cd "$W/home" && sha256sum --quiet -c "runs/${STAMP}_lowp_bench/STAGED_SHA256.txt" ) && echo "STAGED_OK (extracted tar verifies)"
export NC_HOME_ROOT=$W/home NC_SCR_ROOT=$W/scr PILOT_LOCAL_TEST=1 PILOT_SKIP_MODULES=1 PILOT_TIME_BIN=/c/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/jobs/PROD_L/tests/live/gnutime_shim.sh
export PRODL_BENCH_EXTRA="--test-library" LOWP_SMOKE_ALLOW_VERSION_MISMATCH=1
export PATH="/c/Program Files/R/R-4.4.1/bin:$PATH"
U=$W/units.tsv
printf 'piece\ttask\tunit\tdataset\tscale\trepeat\n' > "$U"
printf 'bench\t0\tp0020_S1_r001_c100\tp0020_S1_r001\tc100\t0\n' >> "$U"
printf 'bench\t0\tp0030_S4_r050_c050\tp0030_S4_r050\tc050\t0\n' >> "$U"
printf 'bench\t0\tp0030_S6_r100_c100\tp0030_S6_r100\tc100\t0\n' >> "$U"
run() {  # what s1_bench.sbatch does, with the laptop library
  ( set -euo pipefail; PRODL_T0=$(date +%s); HOME_ROOT=$NC_HOME_ROOT
    source "$HOME_ROOT/runs/${STAMP}_lowp_bench/code/prod_l_bench/bench.env"
    R_LIBS_BENCH="C:/Users/felip/AppData/Local/Temp/lowp_Rlib"; R_LIBS_USER_BENCH="C:/Users/felip/AppData/Local/R/win-library/4.4"   # laptop only
    source "$PILOT_DIR/slurm/common.sh"
    pilot_init bench; pilot_modules bench; pilot_blas_single; pilot_require_frozen
    PIECE=bench; UNITS_FILE=$U; TASK_ID=0; PRODL_WALL_S=$WALL_bench; UNIT_BUDGET_S=$BUDGET_bench; P5=0
    source "$PILOT_DIR/batch_runner.sh" ) && rc=0 || rc=$?; echo "RUN bench rc=$rc"
}
run
echo "== second pass under a NEW job id (a real resubmission): every method must come back skipped"
SLURM_ARRAY_JOB_ID=9002 run
echo "== third pass with the SAME job tag as the first (local_0): refused (start_record_exists), ledger untouched"
run
cat "$W/scr/logs/${STAMP}_lowp_bench/refusals/local_0.txt"
L=$W/scr/logs/${STAMP}_lowp_bench
echo "== ledger"; find "$L/ledger" -type f | sort | while read -r f; do echo "$(basename "$(dirname "$f")")/$(basename "$f"): $(cat "$f")"; done
echo "== unit logs (method lines)"; grep -h -E '^p00[23]0_S[1-6]_r[0-9]{3}_c[0-9]{3} (F[1-5]|A[1-3]) ' "$L"/units/*.log | sort | uniq -c | head -60
echo "== results"; find "$W/scr/results" -type f | sort
echo "== reconcile (expect exit 1: 3 of 2,400 cases)"
rc=0; py -3 "$B/reconcile_bench.py" "$STAMP" --home-root "$W/home" --scr-root "$W/scr" --lists "$B/lists/units.tsv" --out "$W/inv" > "$W/reconcile.out" 2>&1 || rc=$?
echo "reconcile rc=$rc"; sed -n '1,30p' "$W/inv/INVENTORY.md"; grep -E 'p0020_S1_r001_c100|p0030_S4_r050_c050|p0030_S6_r100_c100' "$W/inv/inventory/bench.tsv"
echo "== acceptance on the 3 cases (--local-test: provenance skipped)"
# rev 2: the authoritative sources accept_bench.R requires since Sol R1 (I3/I4): r2 manifest + sealed INPUTS manifest (no truth)
ACCX=(--r2-manifest "$B/../../code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt" --inputs-manifest "$SEALED/manifests/inputs_manifest_lowp.csv")
rc=0; Rscript "$B/accept_bench.R" --results "$W/scr/results/${STAMP}_lowp_benchres" --lists "$U" --code "$B/../../code/bench_lowp" "${ACCX[@]}" --out "$W/accept" --local-test || rc=$?
echo "accept rc=$rc"; cat "$W/accept/ACCEPT_BENCH.md"
echo "== acceptance WITHOUT --local-test: must FAIL on provenance (laptop R 4.4.1, test library)"
rc=0; Rscript "$B/accept_bench.R" --results "$W/scr/results/${STAMP}_lowp_benchres" --lists "$U" --code "$B/../../code/bench_lowp" "${ACCX[@]}" --out "$W/accept_prov" || rc=$?
echo "accept(provenance) rc=$rc"; grep -c '4.5.2' "$W/accept_prov/accept_bench.csv" || true
echo "== negative control: a copy of one case with a truncated coefficient vector"
NEG=$W/neg/${STAMP}_lowp_benchres; mkdir -p "$NEG/p0020"; cp -R "$W/scr/results/${STAMP}_lowp_benchres/p0020/p0020_S1_r001_c100" "$NEG/p0020/"
NEGW=$(cygpath -m "$NEG")   # Windows R needs a C:/ path
Rscript -e "f <- '$NEGW/p0020/p0020_S1_r001_c100/F1.rds'; r <- readRDS(f); r\$coefficients[[1]]\$beta_pen <- r\$coefficients[[1]]\$beta_pen[-1]; r\$fit\$coefficients <- r\$coefficients; saveRDS(r, f)"
printf 'piece\ttask\tunit\tdataset\tscale\trepeat\nbench\t0\tp0020_S1_r001_c100\tp0020_S1_r001\tc100\t0\n' > "$W/neg/units.tsv"
rc=0; Rscript "$B/accept_bench.R" --results "$NEG" --lists "$W/neg/units.tsv" --code "$B/../../code/bench_lowp" "${ACCX[@]}" --out "$W/accept_neg" --local-test || rc=$?
echo "accept(negative) rc=$rc (expect 2)"; grep -E 'FAIL' "$W/accept_neg/accept_bench.csv" | head -5
echo "== s0_verify for REAL (HQ D82): the staged slurm/s0_verify.sbatch run as the job runs it (frozen check, P0b inputs check, env probe on the staged"
echo "   frozen code). Library = metadata-only packages at the r2 pins (tests/mk_pinlib.R) + a copy of the real digest package; the staged bench.env's"
echo "   R_LIBS_BENCH is pointed at it (bench.env is OPS-edited and outside STAGED_SHA256.txt). Rev 1 failed here on NOTS (job 2510090)."
RB="$W/home/runs/${STAMP}_lowp_bench"; T="$B/tests"
s0() {   # s0 LABEL LIBDIR : run the staged s0_verify.sbatch with R_LIBS_BENCH=LIBDIR under a fresh job tag
  sed -i "s#^R_LIBS_BENCH=.*#R_LIBS_BENCH=\"$(cygpath -m "$2")\"#" "$RB/code/prod_l_bench/bench.env"
  grep -n '^R_LIBS_BENCH=' "$RB/code/prod_l_bench/bench.env"
  rc=0; ( WAVE=main SLURM_JOB_ID=$3 bash "$RB/code/prod_l_bench/slurm/s0_verify.sbatch" ) > "$W/s0_$1.out" 2>&1 || rc=$?
  echo "s0_verify[$1] rc=$rc"; cat "$W/s0_$1.out"; echo "-- unit log:"; cat "$W/scr/logs/${STAMP}_lowp_bench/units/verify.bench_env.$3_0.log" 2>/dev/null || ls "$W/scr/logs/${STAMP}_lowp_bench/units"
}
PINS="glmnet=5.1 ncvreg=3.16.0 abess=0.4.11 susieR=0.14.2 SSLASSO=1.2.3.9001 bayesreg=1.3 pgdraw=1.1 doParallel=1.0.17"
Rscript "$(cygpath -m "$T/mk_pinlib.R")" "$(cygpath -m "$W/pinlib_ok")" $PINS
cp -R "C:/Users/felip/AppData/Local/R/win-library/4.4/digest" "$W/pinlib_ok/"
s0 ok "$W/pinlib_ok" 9101
echo "== s0_verify negative: glmnet at 4.1-10 in the pinned library -> must fail on the pin (not on wiring)"
Rscript "$(cygpath -m "$T/mk_pinlib.R")" "$(cygpath -m "$W/pinlib_bad")" $(printf '%s
' $PINS | sed 's/^glmnet=.*/glmnet=4.1-10/' | tr '
' ' ')
cp -R "C:/Users/felip/AppData/Local/R/win-library/4.4/digest" "$W/pinlib_bad/"
s0 bad "$W/pinlib_bad" 9102
echo "LIVE_DONE"
