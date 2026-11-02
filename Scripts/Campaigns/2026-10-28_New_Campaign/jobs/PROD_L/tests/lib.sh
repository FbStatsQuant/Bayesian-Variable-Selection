#!/bin/bash
# lib.sh -- shared helpers of the PROD-L black-box acceptance suite. Written from DESIGN.md ALONE (the builder's scripts were not read).
# Sourced by every tests/test_*.sh:   source "$(dirname "$0")/lib.sh"; t_init "$1" SUITE_NAME
# Provides: PASS/FAIL counters (t_ok t_bad t_eq t_cond t_summary), work dir guard, stub bin dir (sbatch squeue sacct scancel scontrol stat python3 ...),
# a fake NOTS tree builder (t_mkfix), the driver runner (t_run_driver) and the vector checker wrapper (t_vec).
# Rules encoded here: work dirs only under C:/Users/felip/AppData/Local/Temp/prodl_tests/ ; at most 6 concurrent R processes (no R is used here).

T_LIB_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
B=$(cd "$T_LIB_DIR/.." && pwd)
CAMP=$(cd "$B/../.." && pwd)
T_ALLOWED_ROOT=/c/Users/felip/AppData/Local/Temp/prodl_tests
T_PASS=0; T_FAIL=0; T_SUITE=${T_SUITE:-suite}

# ---- counters ------------------------------------------------------------------------------------------------------------
t_ok()  { T_PASS=$((T_PASS + 1)); echo "PASS  $1"; }
t_bad() { T_FAIL=$((T_FAIL + 1)); echo "FAIL  $1${2:+  -- $2}"; }
t_eq()  { if [ "$2" = "$3" ]; then t_ok "$1"; else t_bad "$1" "expected [$2] got [$3]"; fi; }   # t_eq NAME EXPECTED GOT
t_cond() { local n=$1 rc=$2; shift 2; if [ "$rc" = 0 ]; then t_ok "$n"; else t_bad "$n" "$*"; fi; }   # t_cond NAME RC [detail]; RC 0 = ok
t_summary() { echo; echo "$T_SUITE: $T_PASS passed, $T_FAIL failed"; [ "$T_FAIL" = 0 ]; }
t_win() { cygpath -m "$1"; }
t_count_lines() { if [ -f "$1" ]; then wc -l < "$1" | tr -d ' '; else echo 0; fi; }

# ---- work dir ------------------------------------------------------------------------------------------------------------
# t_init WORKDIR SUITE : WORKDIR must lie under prodl_tests/ (refused otherwise); it is emptied and recreated.
t_init() {
  local w=${1:-}; T_SUITE=${2:-suite}
  [ -n "$w" ] || { echo "usage: $T_SUITE WORKDIR (under C:/Users/felip/AppData/Local/Temp/prodl_tests/)" >&2; exit 64; }
  local wm; wm=$(cygpath -m "$w" 2>/dev/null || echo "$w"); wm=${wm,,}
  case "$wm" in c:/users/felip/appdata/local/temp/prodl_tests/?*) ;; *) echo "REFUSED: work dir $w is not under C:/Users/felip/AppData/Local/Temp/prodl_tests" >&2; exit 64;; esac
  case "$wm" in *..*) echo "REFUSED: work dir contains .." >&2; exit 64;; esac
  w=$(cygpath -u "$w" 2>/dev/null || echo "$w")
  chmod -R u+rwx "$w" 2>/dev/null; rm -rf "$w"; mkdir -p "$w"; W=$(cd "$w" && pwd)
  T_BIN="$W/bin"; T_STUB="$W/stub"; mkdir -p "$T_BIN" "$T_STUB"
  export STUB_DIR="$T_STUB" GUARD_LOG="$T_STUB/guard_calls.txt"
  t_make_stubs
  export PATH="$T_BIN:$PATH"      # the stubs (also the sha256sum text-mode wrapper) are on PATH for the fixture builders as well
}

# ---- stubs ---------------------------------------------------------------------------------------------------------------
# State lives in $STUB_DIR (exported). Reset between scenarios with t_stub_reset.
t_stub_reset() { rm -rf "$T_STUB"; mkdir -p "$T_STUB"; }
t_make_stubs() {
  local b=$T_BIN
  cat > "$b/sbatch" <<'S'
#!/bin/bash
# records argv (one arg per line, calls separated by ---CALL n) and prints incrementing digit ids ID_BASE+n; FAIL_AT=k fails the k-th call; BAD_ID_AT=k prints junk
d=${STUB_DIR:?}
n=$(( $(cat "$d/n" 2>/dev/null || echo 0) + 1 )); echo $n > "$d/n"
{ echo "---CALL $n"; printf '%s\n' "$@"; } >> "$d/sbatch_argv.txt"
printf '%s\n' "$*" >> "$d/sbatch_calls.txt"
if [ "${FAIL_AT:-0}" = "$n" ]; then echo 'fabricated sbatch rejection' >&2; exit 42; fi
if [ "${BAD_ID_AT:-0}" = "$n" ]; then echo 'Submitted batch job (not parsable)'; exit 0; fi
echo $(( ${ID_BASE:-7000} + n ))
S
  cat > "$b/squeue" <<'S'
#!/bin/bash
# prints the fixture $STUB_DIR/squeue.txt (rows id|name|state|cpus); the file squeue_fail makes the scheduler "unreachable"
d=${STUB_DIR:?}
printf '%s\n' "$*" >> "$d/squeue_calls.txt"
if [ -e "$d/squeue_fail" ]; then echo "squeue: error: Unable to contact slurm controller (fabricated)" >&2; exit 17; fi
# `squeue -h -j JOBID -o %e` (job end time, used by batch_runner.sh): the fixture squeue_end.txt, or N/A
case "$*" in *%e*) if [ -f "$d/squeue_end.txt" ]; then cat "$d/squeue_end.txt"; else echo "N/A"; fi; exit 0;; esac
# squeue_mixed: active rows AND an error with a nonzero exit (Sol's R1 reproduction of the "Invalid job id" tolerance)
if [ -s "$d/squeue_mixed" ]; then cat "$d/squeue_mixed"; echo "squeue: error: Invalid job id specified" >&2; exit 1; fi
[ -f "$d/squeue.txt" ] && cat "$d/squeue.txt"
exit 0
S
  cat > "$b/sacct" <<'S'
#!/bin/bash
# sacct stub over the fixture $STUB_DIR/sacct.txt with rows JobID|JobName|State|ExitCode|Elapsed|ElapsedRaw|AllocCPUS|Partition|Account ; honours -o/--format and -j ; sacct_fail makes it fail
d=${STUB_DIR:?}
printf '%s\n' "$*" >> "$d/sacct_calls.txt"
if [ -e "$d/sacct_fail" ]; then echo "sacct: error: slurmdbd unreachable (fabricated)" >&2; exit 18; fi
cols="JobID,State"; ids=""; nohdr=0
while [ $# -gt 0 ]; do case "$1" in
  -o) cols=$2; shift 2;; --format=*) cols=${1#*=}; shift;; -o*) cols=${1#-o}; shift;;
  -j) ids=$2; shift 2;; --jobs=*) ids=${1#*=}; shift;; -j*) ids=${1#-j}; shift;;
  -n|--noheader) nohdr=1; shift;;
  *) shift;; esac; done
# SACCT_HEADER=1 (test_collect.sh): print the column-name line when -n is absent, like the real `sacct -P`
if [ "${SACCT_HEADER:-0}" = 1 ] && [ $nohdr = 0 ]; then echo "$cols" | sed 's/%[0-9]*//g; s/,/|/g'; fi
[ -f "$d/sacct.txt" ] || exit 0
awk -F'|' -v cols="$cols" -v ids="$ids" 'BEGIN{ nc=split(cols,c,","); ni=split(ids,a,","); for(i=1;i<=ni;i++) want[a[i]]=1
  split("JobID JobName State ExitCode Elapsed ElapsedRaw AllocCPUS Partition Account",h," "); for(i=1;i<=9;i++) idx[tolower(h[i])]=i }
  { id=$1; base=id; sub(/_.*/,"",base); if (ids!="" && !(id in want) && !(base in want)) next
    out=""; for(i=1;i<=nc;i++){ n=c[i]; sub(/%.*/,"",n); k=idx[tolower(n)]; v=(k? $k : ""); out=out (i>1?"|":"") v } print out }' "$d/sacct.txt"
S
  cat > "$b/scancel" <<'S'
#!/bin/bash
printf '%s\n' "$*" >> "${STUB_DIR:?}/scancel_calls.txt"
exit 0
S
  cat > "$b/scontrol" <<'S'
#!/bin/bash
printf '%s\n' "$*" >> "${STUB_DIR:?}/scontrol_calls.txt"
# `scontrol update JobId=ID ArrayTaskThrottle=N` rewrites the %N of that job's pending array row in the squeue fixture (unless scontrol_noop exists), like the real scheduler would
if [ ! -e "$STUB_DIR/scontrol_noop" ] && [ -f "$STUB_DIR/squeue.txt" ]; then
  id=""; n=""; for a in "$@"; do case "$a" in JobId=*) id=${a#JobId=};; ArrayTaskThrottle=*) n=${a#ArrayTaskThrottle=};; esac; done
  if [ -n "$id" ] && [ -n "$n" ]; then sed -E "s/^(${id}_\[[^%|]*)%[0-9]+(\])/\1%${n}\2/" "$STUB_DIR/squeue.txt" > "$STUB_DIR/squeue.new" && mv "$STUB_DIR/squeue.new" "$STUB_DIR/squeue.txt"; fi
fi
exit 0
S
  cat > "$b/python3" <<'S'
#!/bin/bash
# the laptop has no python3 on PATH (only the py launcher): forward to py -3 with MSYS paths converted
conv() { case "$1" in /*) if [ -e "$1" ] || [ -d "$(dirname "$1")" ]; then cygpath -m "$1"; else printf '%s' "$1"; fi;; *) printf '%s' "$1";; esac; }
args=(); for a in "$@"; do
  case "$a" in
    --*=/*) a="${a%%=*}=$(conv "${a#*=}")";;
    /*) a=$(conv "$a");;
  esac; args+=("$a"); done
exec py -3 "${args[@]}"
S
  cp "$b/python3" "$b/python"
  cat > "$b/stat" <<'S'
#!/bin/bash
# real stat, except that trees listed in $STUB_DIR/locked_trees report mode 0 for `stat -c %a` (the laptop cannot really chmod 000 a directory)
real=/usr/bin/stat
lt="${STUB_DIR:-/nonexistent}/locked_trees"
if [ -s "$lt" ] && [ "$1" = "-c" ] && [ "$2" = "%a" ]; then
  shift 2; out=""
  for p in "$@"; do
    hit=0; while IFS= read -r t; do [ -n "$t" ] || continue; case "$p" in "$t"|"$t"/*) hit=1;; esac; done < "$lt"
    if [ $hit = 1 ]; then echo 0; else "$real" -c %a "$p"; fi
  done; exit 0
fi
exec "$real" "$@"
S
  # Git Bash's sha256sum defaults to BINARY mode and prints "<hash> *<name>"; Linux (NOTS) and the real adapter/enumerator write "<hash>  <name>" (two spaces).
  # This wrapper makes the laptop behave like Linux: text mode unless the caller chose a mode or is verifying.
  cat > "$b/sha256sum" <<'S'
#!/bin/bash
for a in "$@"; do case "$a" in -c|--check|-b|--binary|-t|--text|--tag|--help|--version) exec /usr/bin/sha256sum "$@";; esac; done
exec /usr/bin/sha256sum -t "$@"
S
  cat > "$b/Rscript" <<'S'
#!/bin/bash
# minimal Rscript stand-in: version/-e calls succeed silently; lowp_truth_lock(STUDY, TRUE|FALSE) creates / removes $STUDY/.locked_marker
all="$*"
# the frozen P5 scanner: p5_scan.R --run-dir <...>_lowp_smc|_lowp_smcrep --out FILE : copies $STUB_DIR/scan_smc.tsv | scan_smcrep.tsv (or a header-only table);
# $STUB_DIR/scan_fail_smc | scan_fail_smcrep make that scan exit 1 without writing
case "$all" in
  *p5_scan.R*)
    run=""; out=""; prev=""
    for a in "$@"; do [ "$prev" = --run-dir ] && run=$a; [ "$prev" = --out ] && out=$a; prev=$a; done
    kind=smc; case "$run" in *_lowp_smcrep) kind=smcrep;; esac
    [ -e "${STUB_DIR:-/nonexistent}/scan_fail_$kind" ] && { echo "p5_scan: fabricated failure" >&2; exit 1; }
    if [ -f "$STUB_DIR/scan_$kind.tsv" ]; then cp "$STUB_DIR/scan_$kind.tsv" "$out"; else printf 'case_id\tbase\trepeat_m\tprimary_v3_status\tprimary_status\tretry_state\tretry_problem\teligible\tlaunchable\n' > "$out"; fi
    echo "p5 scan stub ($kind): wrote $out"; exit 0;;
esac
case "$all" in
  *"lowp_truth_lock('"*", TRUE)"*) st=${all#*lowp_truth_lock\(\'}; st=${st%%\'*}; : > "$st/.locked_marker";;
  *"lowp_truth_lock('"*", FALSE)"*) st=${all#*lowp_truth_lock\(\'}; st=${st%%\'*}; rm -f "$st/.locked_marker";;
esac
echo "R version 4.4.1 (stub)"
exit 0
S
  cat > "$b/gnutime" <<'S'
#!/bin/bash
# GNU-like time: --version ; -f FMT -o FILE cmd... (the stub from the pilot's test_gnu_time.sh)
if [ "${1:-}" = --version ]; then echo "time (GNU Time) 1.9"; exit 0; fi
fmt=""; out=""
while [ $# -gt 0 ]; do case "$1" in -f) fmt=$2; shift 2;; -o) out=$2; shift 2;; *) break;; esac; done
t0=$(date +%s.%N); "$@"; rc=$?; t1=$(date +%s.%N)
el=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}')
line=${fmt//%e/$el}; line=${line//%U/0.02}; line=${line//%S/0.00}; line=${line//%M/2048}; line=${line//\\t/$'\t'}
if [ -n "$out" ]; then printf '%s\n' "$line" > "$out"; else printf '%s\n' "$line" >&2; fi
exit $rc
S
  # fake OPS guard with the D7 limits written exactly like the real guard (guard_check.sh parses the two LIMIT lines); logs each planned add
  cat > "$b/guard_good" <<'G'
#!/bin/bash
set -uo pipefail
ADD_MB=${1:-0}
echo "$ADD_MB" >> "${GUARD_LOG:-/dev/null}"
CAMP_LIMIT_KB=$((1024 * 1024 / 2))          # 0.5 GiB = 524288 KB
HOME_LIMIT_KB=$((96 * 1024 * 1024 / 10))    # 9.6 GiB
HOME_KB=$(awk -v g="${FAKE_HOME_GB:-8.85}" 'BEGIN{printf "%d", g*1048576}'); CAMP_KB=${FAKE_CAMP_KB:-20000}
S=OK; RC=0; W=""
if [ $((CAMP_KB + ADD_MB * 1024)) -gt $CAMP_LIMIT_KB ]; then S=REFUSE; RC=1; W=" campaign+add>limit"; fi
if [ $((HOME_KB + ADD_MB * 1024)) -gt $HOME_LIMIT_KB ]; then S=REFUSE; RC=1; W="$W home+add>limit"; fi
echo "2026 | home $(awk -v k=$HOME_KB 'BEGIN{printf "%.2f", k/1048576}') GB of 10.00 GB | campaign_home 0.02 GB | campaign_scratch 0.00 GB (info) | planned_add ${ADD_MB} MB | $S${W:+ (${W# })}"
exit $RC
G
  printf '#!/bin/bash\necho "GUARD OK"\nexit 0\n' > "$b/guard_simple"
  printf '#!/bin/bash\necho "GUARD REFUSES"\nexit 1\n' > "$b/guard_refuse_always"
  chmod +x "$b"/*
}

# ---- fake NOTS tree ------------------------------------------------------------------------------------------------------
# t_mkfix ROOT STAMP : staged PROD-L run under ROOT/home/New_Campaign/runs/<RID> and scratch ROOT/scr/New_Campaign.
# Sets FH FS RID RUNH BUN LOGR ST T_STAMP. The staged bundle is a copy of B without tests/, review/, PROGRESS.md (DESIGN section 9) with MODULES filled.
t_restage() {   # regenerate STAGED_SHA256.txt exactly as stage_local.sh builds it (find from the home root, excluding the list and prodl.env)
  ( cd "$FH" && find "runs/$RID" -type f ! -name STAGED_SHA256.txt ! -name prodl.env | LC_ALL=C sort | xargs sha256sum > "runs/$RID/STAGED_SHA256.txt" )
}
t_mkfix() {
  local fx=$1 p s r i id nm
  T_STAMP=$2; RID=${T_STAMP}_lowp_prodL
  FH="$fx/home/New_Campaign"; FS="$fx/scr/New_Campaign"; RUNH="$FH/runs/$RID"; BUN="$RUNH/code/prod_l"; LOGR="$FS/logs/$RID"; ST="$RUNH/study"
  chmod -R u+rwx "$fx" 2>/dev/null; rm -rf "$fx"
  mkdir -p "$FH/code/ops" "$FS/results" "$FS/logs" "$FS/runs" "$RUNH/code/core/v2_2_1/core/cpp" "$RUNH/code/core/v2_2_1/study" "$RUNH/code/core/v2_2_1/tools" \
           "$RUNH/code/lowp/enum" "$RUNH/code/lowp/R" "$RUNH/code/lowp/tests" "$ST/manifests" "$ST/dev/manifests" "$ST/dev/inputs" "$ST/dev/truth" "$ST/inputs" "$ST/truth"
  cp -R "${PRODL_B_SRC:-$B}" "$BUN"; rm -rf "$BUN/tests" "$BUN/review" "$BUN/PROGRESS.md" "$BUN/__pycache__"
  sed -i -E 's/^(MODULES[A-Z_]*)=""/\1="fake"/' "$BUN/prodl.env" 2>/dev/null
  for f in core/v2_2_1/core/v3.R core/v2_2_1/core/cpp/v3_score.h core/v2_2_1/study/run_case.R core/v2_2_1/study/adapter.R core/v2_2_1/tools/p5_scan.R core/v2_2_1/CHANGES_v2_2_1.md \
           lowp/enum/lowp_enum.R lowp/enum/exact_contract.R lowp/enum/run_enum_dataset.R lowp/R/lowp_verify_nots.R lowp/R/lowp_seal.R lowp/tests/test_truth_lock_linux.sh; do
    echo fixture > "$RUNH/code/$f"
  done
  ( cd "$RUNH/code/core/v2_2_1" && find . -type f | LC_ALL=C sort | xargs sha256sum > "$RUNH/code/core/v2_2_1.SHA256SUMS" )
  for d in "$ST/manifests" "$ST/dev/manifests"; do echo fixture > "$d/inputs_manifest_lowp.csv"; echo fixture > "$d/truth_manifest_lowp.csv"; done
  for p in 0020 0030; do
    mkdir -p "$ST/inputs/p$p" "$ST/truth/p$p" "$ST/dev/inputs/p$p" "$ST/dev/truth/p$p"
    for s in 1 2 3 4 5 6; do
      for r in $(seq 1 100); do printf -v id 'p%s_S%s_r%03d' "$p" "$s" "$r"; : > "$ST/inputs/p$p/$id.rds"; echo "truth $id" > "$ST/truth/p$p/$id.rds"; done
      for r in 1 2 3 4 5; do printf -v id 'dev_p%s_S%s_r%03d' "$p" "$s" "$r"; : > "$ST/dev/inputs/p$p/$id.rds"; echo "devtruth $id" > "$ST/dev/truth/p$p/$id.rds"; done
    done
  done
  find "$ST/truth" "$ST/dev/truth" -type f -exec chmod 444 {} +
  echo "lowp_prodL $T_STAMP staged fixture" > "$RUNH/OWNER"
  mkdir -p "$FH/code/core/shared" "$FH/code/lowp_shared"; echo keep > "$FH/code/core/shared/x"; echo keep > "$FH/code/lowp_shared/y"
  t_restage
}
# t_mkbundle ROOT STAMP : only the staged bundle (no study) plus empty scratch dirs; sets FH FS RID RUNH BUN LOGR T_STAMP (for tests that need no truth tree)
t_mkbundle() {
  local fx=$1
  T_STAMP=$2; RID=${T_STAMP}_lowp_prodL
  FH="$fx/home/New_Campaign"; FS="$fx/scr/New_Campaign"; RUNH="$FH/runs/$RID"; BUN="$RUNH/code/prod_l"; LOGR="$FS/logs/$RID"; ST="$RUNH/study"
  chmod -R u+rwx "$fx" 2>/dev/null; rm -rf "$fx"
  mkdir -p "$FH/code/ops" "$FS/results" "$FS/logs" "$FS/runs" "$RUNH/code"
  cp -R "${PRODL_B_SRC:-$B}" "$BUN"; rm -rf "$BUN/tests" "$BUN/review" "$BUN/PROGRESS.md" "$BUN/__pycache__"
  sed -i -E 's/^(MODULES[A-Z_]*)=""/\1="fake"/' "$BUN/prodl.env" 2>/dev/null
  echo "lowp_prodL $T_STAMP staged fixture" > "$RUNH/OWNER"
}
# t_find_common : path of the slurm/common.sh of the staged bundle (empty if absent)
t_find_common() { find "$BUN" -maxdepth 2 -name common.sh 2>/dev/null | head -n 1; }
# t_reset_run : forget everything a driver run created (keeps the staged tree); clears stub state; truth open
t_reset_run() {
  chmod -R u+rwx "$LOGR" 2>/dev/null; rm -rf "$LOGR" "$RUNH/resubmit" "$RUNH/p5" "$RUNH/manifests"; rm -f "$RUNH/JOBIDS.tsv"
  t_stub_reset; t_unlock_truth_sim
}
# simulated lock of both truth trees: real chmod 000 where it works (Linux), otherwise a `stat` shim reporting mode 0 (NTFS ignores directory modes)
T_LOCK_MODE=none
t_lock_truth_sim() {
  chmod 000 "$ST/truth" "$ST/dev/truth" 2>/dev/null
  if ls "$ST/truth" >/dev/null 2>&1; then
    chmod 755 "$ST/truth" "$ST/dev/truth" 2>/dev/null
    printf '%s\n%s\n' "$ST/truth" "$ST/dev/truth" > "$T_STUB/locked_trees"; T_LOCK_MODE=shim
  else T_LOCK_MODE=real; fi
}
t_unlock_truth_sim() { chmod 755 "$ST/truth" "$ST/dev/truth" 2>/dev/null; rm -f "$T_STUB/locked_trees"; T_LOCK_MODE=none; }

# ---- driver runner -------------------------------------------------------------------------------------------------------
# t_run_driver LABEL args... ; extra environment via DRV_ENV=(K=V ...), variables to unset via DRV_UNSET=(NAME ...). Result: DRV_RC, DRV_LOG.
DRV_ENV=(); DRV_UNSET=()
t_run_driver() {
  local label=$1; shift
  DRV_LOG="$W/drv_$label.log"
  (
    export NC_HOME_ROOT="$FH" NC_SCR_ROOT="$FS" STAMP="$T_STAMP" GUARD="$T_BIN/guard_good" SQUEUE="$T_BIN/squeue" SACCT="$T_BIN/sacct" SCANCEL="$T_BIN/scancel" \
           SCONTROL="$T_BIN/scontrol" PYTHON="$T_BIN/python3" PATH="$T_BIN:$PATH" STUB_DIR="$T_STUB" GUARD_LOG="$T_STUB/guard_calls.txt"
    local kv v
    for kv in "${DRV_ENV[@]}"; do [ -n "$kv" ] && export "$kv"; done
    for v in "${DRV_UNSET[@]}"; do [ -n "$v" ] && unset "$v"; done
    cd "$W" && bash "$BUN/submit_prodl.sh" "$@"
  ) > "$DRV_LOG" 2>&1
  DRV_RC=$?
}
t_no_submission() { [ ! -s "$T_STUB/sbatch_calls.txt" ] && [ ! -d "$LOGR/launch" ] && [ ! -e "$RUNH/JOBIDS.tsv" ]; }   # nothing created, nothing submitted
t_nsub() { t_count_lines "$T_STUB/sbatch_calls.txt"; }

# t_vec LABEL vec_check.py-args... : run the vector checker and count each PASS/FAIL line it prints
t_vec() {
  local label=$1; shift; local safe=${label//[^A-Za-z0-9_]/_}; local out="$W/vec_${safe}.txt" n=0 line
  py -3 -I "$(t_win "$T_LIB_DIR/vec_check.py")" --argv "$(t_win "$T_STUB/sbatch_argv.txt")" "$@" > "$out" 2>&1
  while IFS= read -r line; do
    case "$line" in PASS*) t_ok "$label ${line#PASS }"; n=$((n + 1));; FAIL*) t_bad "$label ${line#FAIL }"; n=$((n + 1));; esac
  done < "$out"
  [ "$n" -gt 0 ] || t_bad "$label vector checker produced no verdict" "$(head -c 300 "$out" | tr '\n' ' ')"
}

# ---- small fixture writers -----------------------------------------------------------------------------------------------
# t_mk_unitlist FILE PIECE NROWS [TASKSIZE] : a resubmission-style list (units.tsv format, with header) of NROWS smc/enum units, tasks renumbered in chunks
t_mk_unitlist() {
  local f=$1 piece=$2 n=$3 sz=${4:-25} i id task
  mkdir -p "$(dirname "$f")"
  printf 'piece\ttask\tunit\tdataset\tscale\trepeat%s\n' "$([ "$piece" = p5 ] && printf '\tbase_piece')" > "$f"
  for i in $(seq 1 "$n"); do
    task=$(( (i - 1) / sz ))
    printf -v id 'p0020_S1_r%03d' "$i"
    case "$piece" in
      smc)    printf '%s\t%s\t%s\t%s\t%s\t%s\n' smc "$task" "${id}_c100" "$id" c100 0 >> "$f";;
      smcrep) printf '%s\t%s\t%s\t%s\t%s\t%s\n' smcrep "$task" "${id}_c100_rep1" "$id" c100 1 >> "$f";;
      p5)     printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' p5 "$((i - 1))" "${id}_c100" "$id" c100 0 smc >> "$f";;
      *)      printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$piece" "$task" "$id" "$id" - 0 >> "$f";;
    esac
  done
}
