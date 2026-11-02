#!/bin/bash
# test_accept.sh -- accept_bench.R (PROD_L_BENCH DESIGN.md section 6; Sol R1 defects I1-I4): laptop acceptance of the downloaded benchmark records (single R process at a time, R 4.4.1, reads RDS only).
#   bash test_accept.sh WORKDIR
# accept_bench.R --results <downloaded results folder> --lists <units.tsv> --code <code/bench_lowp> --r2-manifest <BENCH_LOWP_MANIFEST_SHA256_r2.txt>
#                --inputs-manifest <sealed inputs_manifest_lowp.csv> --out <dir> [--local-test]    exit 0 ACCEPTED / 2 FAIL / 3 INCOMPLETE ; writes ACCEPT_BENCH.md + accept_bench.csv.
# Positive controls: (a) the manager's REAL live records (3 cases, 24 records) in --local-test mode; (b) REAL records produced here by the frozen CLI on the laptop test library (1 case, 8
# methods), unpatched in --local-test mode and with provenance rewritten to what the pinned sealed run records in non-local mode.
# Negative controls: each ONE mutation on a COPY of real records (csv and .sha256 sidecars re-sealed, so only accept_bench can catch it), checked for the exit code, the method(s) failing and the
# reason given:  I1 (registry/derived rules/roles)  I2 (D42.5 coefficients, PIP, beta)  I3 (identity, seeds, scale, run id, hashes vs the sealed manifest)  I4 (code anchoring to r2, provenance).
# The supplied --code tree with one byte changed / one extra file must FAIL. D54.3: the ABESS exact size check is NOT performed and is DISCLOSED in the report.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_accept
SRCB=${PRODL_B_SRC:-$B}
RS="/c/Program Files/R/R-4.4.1/bin/Rscript.exe"
LIBW="C:/Users/felip/AppData/Local/Temp/lowp_Rlib"
STUDY="C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/inputs/lowp_study"
INMAN="$STUDY/manifests/inputs_manifest_lowp.csv"
CODE="$CAMP/code/bench_lowp"
R2="$CAMP/code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt"
ACC="$SRCB/accept_bench.R"
FIX="$T_LIB_DIR/make_accept_fixture.R"
LIVEW=/c/Users/felip/AppData/Local/Temp/prodlb_live/w
LIVER="$LIVEW/scr/results/20261030T0001Z_lowp_benchres"
LIVEU="$LIVEW/units.tsv"
STAMP=20261030T1900Z; RUNID=${STAMP}_lowp_benchres
[ -f "$ACC" ]; t_cond "AC00 accept_bench.R exists in the bundle" $?
[ -x "$RS" ] && [ -d "/c/Users/felip/AppData/Local/Temp/lowp_Rlib" ] && [ -f "$INMAN" ] && [ -f "$R2" ] && [ -d "$CODE" ]; t_cond "AC01 prerequisites present (R 4.4.1, laptop test library, sealed inputs manifest, r2 manifest, bench_lowp code)" $?

run_acc() {   # run_acc LABEL RESULTS LISTS MODE(local|pinned) [INPUTS_MANIFEST] [CODE_DIR] : ACC_RC, ACC_OUT
  local lab=$1 res=$2 lst=$3 mode=$4 man=${5:-$INMAN} cdir=${6:-$CODE} extra=""
  [ "$mode" = local ] && extra="--local-test"
  ACC_OUT="$W/acc_$lab"; rm -rf "$ACC_OUT"; mkdir -p "$ACC_OUT"
  "$RS" "$(t_win "$ACC")" --results "$(t_win "$res")" --lists "$(t_win "$lst")" --code "$(t_win "$cdir")" --r2-manifest "$(t_win "$R2")" \
     --inputs-manifest "$(t_win "$man")" --out "$(t_win "$ACC_OUT")" $extra > "$W/acc_$lab.log" 2>&1
  ACC_RC=$?
}
mut() {   # mut ID SRC VARIANT PINNED(0|1) : builds $W/m_ID/<basename SRC> ; MUT_DST ; returns 0 when built
  MUT_DST="$W/m_$1/$(basename "$2")"; rm -rf "$W/m_$1"
  "$RS" "$(t_win "$FIX")" mut "$(t_win "$2")" "$(t_win "$MUT_DST")" "$3" "$LIBW" "$4" "$(t_win "$CODE")" > "$W/mut_$1.log" 2>&1
  local rc=$?
  [ $rc = 0 ] || t_bad "$1 ($3) fixture could not be built (exit $rc): $(tail -n 2 "$W/mut_$1.log" | tr '\n' ' ')"
  return $rc
}
failrows() {  # failrows METHOD|ANY : number of FAIL rows of the last run
  if [ "$1" = ANY ]; then grep -c '","FAIL","' "$ACC_OUT/accept_bench.csv"; else grep -c "\",\"$1\",\"FAIL\",\"" "$ACC_OUT/accept_bench.csv"; fi
}
reason_has() {  # reason_has METHOD|ANY REGEX : some FAIL row of the method mentions the regex
  if [ "$1" = ANY ]; then grep '","FAIL","' "$ACC_OUT/accept_bench.csv" | grep -Eq "$2"; else grep "\",\"$1\",\"FAIL\",\"" "$ACC_OUT/accept_bench.csv" | grep -Eq "$2"; fi
}
neg() {   # neg ID DESC VARIANT PINNED SRC UNITS MODE METHOD NFAIL REGEX [MANIFEST] : single mutation -> exit 2, NFAIL failing records of METHOD, reason matches REGEX
  local id=$1 desc=$2 v=$3 pin=$4 src=$5 units=$6 mode=$7 meth=$8 nf=$9 rx=${10} man=${11:-$INMAN}
  mut "$id" "$src" "$v" "$pin" || return
  run_acc "$id" "$MUT_DST" "$units" "$mode" "$man"
  t_eq "$id $desc: FAIL, exit 2" 2 "$ACC_RC"
  t_eq "$id ... exactly $nf record(s) of $meth FAIL" "$nf" "$(failrows "$meth")"
  reason_has "$meth" "$rx"; t_cond "$id ... the reason names the defect (/$rx/)" $?
}

# ---- (a) the manager's real live records, local mode ----------------------------------------------------------------------------------------------
if [ -d "$LIVER" ] && [ -f "$LIVEU" ]; then
  run_acc live "$LIVER" "$LIVEU" local
  t_eq "AC10 positive control: the 3 real live cases (24 records), --local-test: ACCEPTED, exit 0" 0 "$ACC_RC"
  grep -q 'ACCEPTED' "$ACC_OUT/ACCEPT_BENCH.md"; t_cond "AC11 ACCEPT_BENCH.md says ACCEPTED" $?
  t_eq "AC12 accept_bench.csv: 24 PASS rows, no FAIL / INCOMPLETE" "24/0" "$(grep -c '","PASS","' "$ACC_OUT/accept_bench.csv")/$(grep -c '","FAIL","\|","INCOMPLETE","' "$ACC_OUT/accept_bench.csv")"
  grep -q 'LOCAL TEST' "$ACC_OUT/ACCEPT_BENCH.md"; t_cond "AC13 the report states that the environment checks were SKIPPED in local mode" $?
  run_acc live_nonlocal "$LIVER" "$LIVEU" pinned
  t_eq "AC14 the same live records WITHOUT --local-test (laptop provenance: R 4.4.1 / test library) must FAIL: exit 2" 2 "$ACC_RC"
else
  t_bad "AC10 live records not found ($LIVER / $LIVEU)"; LIVER=""
fi

# ---- (b) real records from the frozen CLI -------------------------------------------------------------------------------------------------------------
mkdir -p "$W/real"
"$RS" "$(t_win "$FIX")" gen "$STUDY" "$(t_win "$W/real")" "$RUNID" "$LIBW" "$(t_win "$CODE")" > "$W/gen.log" 2>&1; rc=$?
t_eq "AC20 the frozen CLI ran case p0020_S1_r001/c100 with all 8 methods on the laptop test library (exit 0 or 2 mapped to 0)" 0 "$rc"
RR="$W/real/results/$RUNID"; CASE=p0020_S1_r001_c100
n=$(ls "$RR/p0020/$CASE"/*.done 2>/dev/null | wc -l | tr -d ' '); t_eq "AC21 8 method units (.done) were written" 8 "$n"
printf 'piece\ttask\tunit\tdataset\tscale\trepeat\nbench\t0\t%s\tp0020_S1_r001\tc100\t0\n' "$CASE" > "$W/units1.tsv"
if [ "$n" = 8 ]; then
  run_acc real_local "$RR" "$W/units1.tsv" local
  t_eq "AC22 the unpatched real records, --local-test: ACCEPTED, exit 0" 0 "$ACC_RC"
  run_acc real_unpatched "$RR" "$W/units1.tsv" pinned
  t_eq "AC23 the unpatched real records WITHOUT --local-test (R 4.4.1, test_library TRUE, laptop library) must FAIL provenance: exit 2" 2 "$ACC_RC"

  mut P_good "$RR" good 1; t_eq "AC30 (fixture) provenance rewritten to the pinned run: build exit" 0 "$?"
  PG="$MUT_DST"
  run_acc good "$PG" "$W/units1.tsv" pinned
  t_eq "AC31 real records with pinned provenance, non-local: ACCEPTED, exit 0" 0 "$ACC_RC"
  [ -s "$ACC_OUT/ACCEPT_BENCH.md" ] && [ -s "$ACC_OUT/accept_bench.csv" ]; t_cond "AC32 ACCEPT_BENCH.md and accept_bench.csv are written" $?
  grep -q 'ABESS' "$ACC_OUT/ACCEPT_BENCH.md" && grep -q 'D54.3' "$ACC_OUT/ACCEPT_BENCH.md"; t_cond "AC33 the report discloses the ABESS D54.3 decision" $?
  grep -qiE 'not performed|not checked|is NOT|was not' "$ACC_OUT/ACCEPT_BENCH.md"; t_cond "AC34 ... stating that the exact size check is NOT performed" $?
  t_eq "AC35 accept_bench.csv has a PASS row for each of the 8 methods of the case" 8 "$(grep -c '","PASS","' "$ACC_OUT/accept_bench.csv")"

  # ---- old content / provenance controls (pinned fixture), one defect each -------------------------------------------------------------------------------
  for v in no_coef_entry beta_pen_short beta_ols_short support_mismatch k37_mismatch a_beta_short test_library wrong_sealed wrong_r; do
    case $v in
      no_coef_entry)    d="F1 coefficients without the entry of one rule";;
      beta_pen_short)   d="F1 beta_pen of length p-1";;
      beta_ols_short)   d="F1 beta_ols of length p-1";;
      support_mismatch) d="penalized support (beta_pen) differs from the row's support";;
      k37_mismatch)     d="EBIC / K37 pair differs in k";;
      a_beta_short)     d="A1 fit\$beta of length p-1";;
      test_library)     d="test_library TRUE";;
      wrong_sealed)     d="sealed_library is not the pinned path";;
      wrong_r)          d="R version is not 4.5.2";;
    esac
    mut "O_$v" "$RR" "$v" 1 || continue
    run_acc "neg_$v" "$MUT_DST" "$W/units1.tsv" pinned
    t_eq "AC40 negative control ($d): FAIL, exit 2" 2 "$ACC_RC"
  done
  # incomplete: a listed case without results / a missing method record
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat\nbench\t0\t%s\tp0020_S1_r001\tc100\t0\nbench\t0\tp0020_S1_r002_c100\tp0020_S1_r002\tc100\t0\n' "$CASE" > "$W/units2.tsv"
  run_acc incomplete_case "$PG" "$W/units2.tsv" pinned
  t_eq "AC50 a listed case with no result folder: INCOMPLETE, exit 3" 3 "$ACC_RC"
  mut P_missing "$RR" good 1; rm -f "$MUT_DST/p0020/$CASE"/A3.*
  run_acc missing_method "$MUT_DST" "$W/units1.tsv" pinned
  t_eq "AC51 a case with a missing method record (A3): INCOMPLETE, exit 3" 3 "$ACC_RC"
  # accept reads RDS only and never writes into the results folder
  before=$(find "$PG" -type f | LC_ALL=C sort | xargs sha256sum | sha256sum)
  run_acc good_again "$PG" "$W/units1.tsv" pinned
  t_eq "AC60 the results folder is not modified by the acceptance run" "$before" "$(find "$PG" -type f | LC_ALL=C sort | xargs sha256sum | sha256sum)"
else
  t_bad "AC2x real records could not be produced ($n of 8 methods): $(tail -n 3 "$W/gen.log" | tr '\n' ' ')"
  PG=""
fi

# ---- I1 : the exact ordered (rule_id, role) registry + lowp_derive structure (live records, local mode) ------------------------------------------
if [ -n "$LIVER" ]; then
  neg ACI1a "I1: F4 ebic1_lam005 removed from rows AND both coefficient lists in EVERY F4 record"   i1_f4_all   0 "$LIVER" "$LIVEU" local F4 3 'rule ids/roles differ'
  neg ACI1b "I1: F4 ebic1_lam005 removed (rows + both coefficient lists) in the FIRST record only"  i1_f4_first 0 "$LIVER" "$LIVEU" local F4 1 'rule ids/roles differ'
  neg ACI1c "I1: F2 gets one extra rule (rows + coefficient entry)"                                 i1_extra_rule 0 "$LIVER" "$LIVEU" local F2 1 'rule ids/roles differ'
  neg ACI1d "I1: A1 roles all S0"                                                                    i1_a1_roles 0 "$LIVER" "$LIVEU" local A1 1 'rule ids/roles differ'
  neg ACI1e "I1: F5 sic_smax missing (rows + coefficients)"                                         i1_f5_nosic 0 "$LIVER" "$LIVEU" local F5 1 'rule ids/roles differ'
  # ---- I2 : D42.5 coefficient evidence -----------------------------------------------------------------------------------------------------------------
  neg ACI2a "I2: F1 ebic1 beta_ols all NA (the SPEC wants finite OLS for EBIC rules)"               i2_ebic1_ols_na 0 "$LIVER" "$LIVEU" local F1 1 'beta_ols missing/non-finite'
  neg ACI2b "I2: F1 cv_min beta_ols finite (the SPEC says NA for CV rules)"                          i2_cvmin_ols_finite 0 "$LIVER" "$LIVEU" local F1 1 'CV rule must be NA'
  neg ACI2c "I2: F1 beta_pen with an Inf"                                                            i2_betapen_inf 0 "$LIVER" "$LIVEU" local F1 1 'beta_pen not finite'
  neg ACI2d "I2: A1 fit\$pip deleted"                                                                i2_a1_nopip 0 "$LIVER" "$LIVEU" local A1 1 'pip missing'
  neg ACI2e "I2: A1 pip value 1.2"                                                                   i2_a1_pip12 0 "$LIVER" "$LIVEU" local A1 1 'pip not numeric length p in'
  neg ACI2f "I2: A2 beta NA on a successful fit"                                                     i2_a2_beta_na 0 "$LIVER" "$LIVEU" local A2 1 'fit.beta missing'
  # ---- I3 : identity vs the sealed manifest ------------------------------------------------------------------------------------------------------------
  neg ACI3a "I3: data_seed 1 / method_seed 4000001"                                                  i3_data_seed 0 "$LIVER" "$LIVEU" local F1 1 'seeds differ'
  neg ACI3b "I3: fold_seed changed"                                                                  i3_fold_seed 0 "$LIVER" "$LIVEU" local F1 1 'seeds differ'
  neg ACI3c "I3: scale_key c050 in a c100 folder"                                                    i3_scale_key 0 "$LIVER" "$LIVEU" local F1 1 'scale_key/scale differ'
  neg ACI3d "I3: scale 0.5 in a c100 folder"                                                         i3_scale 0 "$LIVER" "$LIVEU" local F1 1 'scale_key/scale differ'
  neg ACI3e "I3: run_id different from the results folder name"                                     i3_runid 0 "$LIVER" "$LIVEU" local F1 1 'run identity'
  neg ACI3f "I3: y_sha256 zeros"                                                                     i3_y_sha 0 "$LIVER" "$LIVEU" local F1 1 'hashes differ from the sealed manifest'
  neg ACI3g "I3: record\$input\$hashes changed"                                                      i3_input_hashes 0 "$LIVER" "$LIVEU" local F1 1 'input.hashes differ'
  # dataset absent from the sealed manifest: records untouched, manifest copy without the first dataset
  "$RS" "$(t_win "$FIX")" manifest_drop "$(t_win "$INMAN")" "$(t_win "$W/inputs_manifest_drop.csv")" p0020_S1_r001 > "$W/manifest_drop.log" 2>&1
  t_eq "ACI3h (fixture) manifest copy without p0020_S1_r001" 0 "$?"
  run_acc ACI3h "$LIVER" "$LIVEU" local "$W/inputs_manifest_drop.csv"
  t_eq "ACI3h I3: dataset absent from the sealed inputs manifest: FAIL, exit 2" 2 "$ACC_RC"
  t_eq "ACI3h ... its 8 method records FAIL (the other cases still PASS)" "8/16" "$(failrows ANY)/$(grep -c '","PASS","' "$ACC_OUT/accept_bench.csv")"
  reason_has ANY 'dataset not in the sealed inputs manifest'; t_cond "ACI3h ... the reason is 'dataset not in the sealed inputs manifest'" $?
  # ---- I4 : code anchoring (local mode: only the environment checks are skipped) --------------------------------------------------------------------
  neg ACI4a "I4: code\$source_sha256 NULL"                                                           i4_src_null 0 "$LIVER" "$LIVEU" local F1 1 'code fingerprint/files missing'
  neg ACI4b "I4: code\$source_sha256 = one common wrong 64-hex in EVERY record (rows consistent)"   i4_src_wrong 0 "$LIVER" "$LIVEU" local ANY 24 'not the runner fingerprint'
  neg ACI4c "I4: record\$code\$files with one hash changed (fingerprint not recomputed)"             i4_files_hash 0 "$LIVER" "$LIVEU" local F1 1 'not the runner fingerprint'
  neg ACI4d "I4: one files hash changed AND the fingerprint (record + rows) recomputed: only the r2 comparison sees it" i4_files_refp 0 "$LIVER" "$LIVEU" local F1 1 'differ from the frozen r2 code'
fi
pos() {   # pos ID DESC VARIANT SRC UNITS MODE : a legitimate edge case built consistently must stay ACCEPTED with every record PASS
  local id=$1 desc=$2 v=$3 src=$4 units=$5 mode=$6
  mut "$id" "$src" "$v" 0 || return
  run_acc "$id" "$MUT_DST" "$units" "$mode"
  t_eq "$id $desc: ACCEPTED, exit 0" 0 "$ACC_RC"
  t_eq "$id ... 24 PASS rows, 0 FAIL" "24/0" "$(grep -c '","PASS","' "$ACC_OUT/accept_bench.csv")/$(failrows ANY)"
}
if [ -n "$LIVER" ]; then
  # ---- N1 (Sol R2): selections --------------------------------------------------------------------------------------------------------------------
  neg ACN1a "N1: F1 cv_min k = 999"                                                                  n1_cvmin_k 0 "$LIVER" "$LIVEU" local F1 1 'k is not the size of the selected support'
  neg ACN1b "N1: F1 ebic1 support '16;3;7;14' (unsorted), k 4"                                       n1_unsorted 0 "$LIVER" "$LIVEU" local F1 1 'not a canonical sorted set'
  neg ACN1c "N1: F1 ebic1 support with a duplicate index '3;7;7;14', k 4"                             n1_dup 0 "$LIVER" "$LIVEU" local F1 1 'not a canonical sorted set'
  neg ACN1d "N1: F1 ebic1 support with index p+1 (21), k 3"                                           n1_pplus1 0 "$LIVER" "$LIVEU" local F1 1 'not a canonical sorted set'
  neg ACN1e "N1: A2 ssl_final support '20' k 1 (beta unchanged)"                                      n1_a2_support 0 "$LIVER" "$LIVEU" local A2 1 'differ from fit.rules|A2 selection != which'
  neg ACN1f "N1: support and k columns removed from the A1/A2/A3 rows"                                n1_a_nosel 0 "$LIVER" "$LIVEU" local ANY 3 'support/k columns missing'
  neg ACN1g "N1: F4 coefficient entry k differs from its row"                                         n1_f4_coef_k 0 "$LIVER" "$LIVEU" local F4 1 'coefficient entry support/k differ from the row'
  neg ACN1h "N1: A1 row support differs from fit\$rules"                                              n1_a1_rows_support 0 "$LIVER" "$LIVEU" local A1 1 'differ from fit.rules'
  # ---- N2: the bic / bic_K37 pair ------------------------------------------------------------------------------------------------------------------
  neg ACN2a "N2: F4 bic_K37 crit_value 99999"                                                         n2_f4_bic_crit 0 "$LIVER" "$LIVEU" local F4 1 '(^|[^e])bic / bic_K37 pair differs'
  neg ACN2b "N2: F5 bic_K37 support differs from bic"                                                 n2_f5_bic_support 0 "$LIVER" "$LIVEU" local F5 1 '(^|[^e])bic / bic_K37 pair differs'
  neg ACN2c "N2: F4 bic_K37 k differs from bic"                                                       n2_f4_bic_k 0 "$LIVER" "$LIVEU" local F4 1 '(^|[^e])bic / bic_K37 pair differs'
  # ---- positives that must stay ACCEPTED -----------------------------------------------------------------------------------------------------------
  pos ACN3a "legitimate NULL selection (F1 ebic1 + ebic1_K37: support '', k 0, beta_pen and beta_ols all zeros)" pos_null_sel "$LIVER" "$LIVEU" local
  pos ACN3b "legitimate FAILED rule (F1 ebic05 + ebic05_K37: status failed, support NA, k NA, coefficient entry failed with NA vectors)" pos_failed_rule "$LIVER" "$LIVEU" local
fi
# ---- I4 : provenance (non-local, pinned fixture) --------------------------------------------------------------------------------------------------
if [ -n "$PG" ]; then
  neg ACI4e "I4: package_provenance removed (non-local)"                                             i4_noprov 1 "$RR" "$W/units1.tsv" pinned F1 1 'provenance missing or empty'
  neg ACI4f "I4: a pinned package (glmnet) at the wrong version (non-local)"                         i4_pin_version 1 "$RR" "$W/units1.tsv" pinned F1 1 'version differs from the pin: glmnet'
  neg ACI4g "I4: a non-base package (glmnet) located in R's own library (non-local)"                i4_glmnet_rlib 1 "$RR" "$W/units1.tsv" pinned F1 1 "non-base package in R's library"
  # the same code-anchor defects in non-local mode (the pinned fixture passes everything else)
  neg ACI4h "I4: wrong common source_sha256 in the pinned fixture (non-local)"                       i4_src_wrong 1 "$RR" "$W/units1.tsv" pinned ANY 8 'not the runner fingerprint'
fi

# ---- the supplied --code tree must be the frozen r2 tree --------------------------------------------------------------------------------------------
SRC_FOR_CODE="${PG:-$LIVER}"; UNITS_FOR_CODE="$W/units1.tsv"; MODE_FOR_CODE=pinned
[ -z "$PG" ] && { UNITS_FOR_CODE="$LIVEU"; MODE_FOR_CODE=local; }
if [ -n "$SRC_FOR_CODE" ]; then
  "$RS" "$(t_win "$FIX")" code_mut "$(t_win "$CODE")" "$(t_win "$W/code_byte")" R/common.R append > "$W/code_byte.log" 2>&1
  t_eq "ACI4i (fixture) copy of the code tree with one byte appended to R/common.R" 0 "$?"
  run_acc ACI4i "$SRC_FOR_CODE" "$UNITS_FOR_CODE" "$MODE_FOR_CODE" "$INMAN" "$W/code_byte"
  t_eq "ACI4i I4: the supplied --code tree with ONE BYTE changed: FAIL, exit 2" 2 "$ACC_RC"
  reason_has ANY 'code differs from r2: R/common.R'; t_cond "ACI4i ... the reason names the changed file (code differs from r2: R/common.R)" $?
  "$RS" "$(t_win "$FIX")" code_mut "$(t_win "$CODE")" "$(t_win "$W/code_extra")" R/extra_file.txt addfile > "$W/code_extra.log" 2>&1
  run_acc ACI4j "$SRC_FOR_CODE" "$UNITS_FOR_CODE" "$MODE_FOR_CODE" "$INMAN" "$W/code_extra"
  t_eq "ACI4j I4: the supplied --code tree with ONE EXTRA FILE: FAIL, exit 2" 2 "$ACC_RC"
  reason_has ANY 'holds files not in r2'; t_cond "ACI4j ... the reason is 'code tree holds files not in r2'" $?
  # the same unmodified inputs with the genuine code tree are ACCEPTED (control for the two runs above)
  run_acc ACI4k "$SRC_FOR_CODE" "$UNITS_FOR_CODE" "$MODE_FOR_CODE"
  t_eq "ACI4k control: the genuine code tree with the same records: ACCEPTED, exit 0" 0 "$ACC_RC"
  # a missing required argument is refused (nonzero), never silently skipped
  "$RS" "$(t_win "$ACC")" --results "$(t_win "$SRC_FOR_CODE")" --lists "$(t_win "$UNITS_FOR_CODE")" --code "$(t_win "$CODE")" --inputs-manifest "$(t_win "$INMAN")" --out "$(t_win "$W/acc_noargs")" --local-test > "$W/acc_noargs.log" 2>&1
  [ $? != 0 ]; t_cond "AC70 without --r2-manifest the script refuses (nonzero exit)" $?
  "$RS" "$(t_win "$ACC")" --results "$(t_win "$SRC_FOR_CODE")" --lists "$(t_win "$UNITS_FOR_CODE")" --code "$(t_win "$CODE")" --r2-manifest "$(t_win "$R2")" --out "$(t_win "$W/acc_noargs2")" --local-test > "$W/acc_noargs2.log" 2>&1
  [ $? != 0 ]; t_cond "AC71 without --inputs-manifest the script refuses (nonzero exit)" $?
fi

t_summary
