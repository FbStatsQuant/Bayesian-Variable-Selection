#!/usr/bin/env bash
# Ordinary-user Linux test of the truth lock (LOWP_SPEC L.5; review finding 1). For the NOTS pilot.
#   bash test_truth_lock_linux.sh <STUDY root> [<lowp R directory>] [--evidence-dir DIR] [--cleanup-temp]
# STUDY root holds truth/ (1,200 files), dev/truth/ (60 files) and manifests/, dev/manifests/ (as sealed by lowp_seal.R).
# Run it on a COPY of the study if fitting jobs may be reading the real one (it locks and unlocks truth/ and dev/truth/).
# It: (1) records the file SHA-256 of every truth file; (2) locks with lowp_truth_lock(root, TRUE); (3) checks, as an ordinary user, that
# both truth trees are mode 000 and unreadable (ls, find, cat, readRDS all fail) while inputs/ and manifests/ stay readable; (4) locks again
# (idempotence); (5) unlocks with ONE call and checks directories 755, files 444, counts and SHA-256 unchanged and readRDS working;
# (6) repeats lock then simulates the two bad states of the review (only the top directory reopened; interrupted lock with the top at 000)
# and checks that one unlock call recovers each. Exit 0 = all pass, 1 = a check failed, 3 = cannot run (root user, missing paths).
# The tree is left UNLOCKED (directories 755, files 444) at the end, also after a failure (trap).
#
# EVIDENCE (always retained): --evidence-dir DIR (default: <STUDY parent>/<STUDY name>_truthlock_evidence_<UTC timestamp>, i.e. next to the
# study copy) receives
#   run.log               every line printed by this script (checks, header, final lines)
#   pre_<tree>.sha        per-file SHA-256 list of each truth tree before locking (production: truth, dev: devtruth)
#   post_<label>_<tree>.sha   the same lists after each unlock (after_unlock, recovery_1, recovery_2), compared with pre_*
#   lock_NN.log / unlock_NN.log   the COMPLETE R output of every lock / unlock call
#   modes_<label>.txt     `stat` mode of every directory and file of both trees at each stage
#   final_status.txt      script SHA-256, failures, final exit status
#   tmp/                  transient stderr of the denied ls/cat/find probes; removed at the end only with --cleanup-temp
# At the end the script prints SOURCE_SHA256 (of this file) and FINAL_EXIT_STATUS.
set -u
ROOT=""; RDIR=""; EVD=""; CLEAN=0; pos=0
while [ $# -gt 0 ]; do
  case "$1" in
    --evidence-dir) [ $# -ge 2 ] || { echo "--evidence-dir needs a directory"; exit 3; }; EVD=$2; shift 2 ;;
    --cleanup-temp) CLEAN=1; shift ;;
    -h|--help) sed -n '2,3p' "$0"; exit 3 ;;
    --*) echo "unknown option $1"; exit 3 ;;
    *) pos=$((pos + 1)); if [ $pos = 1 ]; then ROOT=$1; elif [ $pos = 2 ]; then RDIR=$1; else echo "too many arguments"; exit 3; fi; shift ;;
  esac
done
[ -n "$RDIR" ] || RDIR="$(cd "$(dirname "$0")/../R" && pwd)"
[ -n "$ROOT" ] && [ -d "$ROOT/truth" ] && [ -d "$ROOT/dev/truth" ] && [ -f "$RDIR/lowp_seal.R" ] || { echo "usage: $0 <STUDY root with truth/ and dev/truth/> [<lowp R dir>] [--evidence-dir DIR] [--cleanup-temp]"; exit 3; }
[ "$(id -u)" -ne 0 ] || { echo "run as the ordinary user: root bypasses permissions"; exit 3; }
ROOT=$(cd "$ROOT" && pwd); TRUTHS=("$ROOT/truth" "$ROOT/dev/truth"); TNAME=("truth" "devtruth")
[ -n "$EVD" ] || EVD="$(dirname "$ROOT")/$(basename "$ROOT")_truthlock_evidence_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$EVD/tmp" || { echo "cannot create the evidence directory $EVD"; exit 3; }
EVD=$(cd "$EVD" && pwd); RUNLOG="$EVD/run.log"; : > "$RUNLOG"
RS=${RSCRIPT:-Rscript}
fails=0; ncheck=0; NLOCK=0; NUNLOCK=0
say()  { echo "$*"; echo "$*" >> "$RUNLOG"; }
ok()   { ncheck=$((ncheck + 1)); say "ok    $*"; }
bad()  { ncheck=$((ncheck + 1)); fails=$((fails + 1)); say "FAIL  $*"; }
chk()  { if [ "$1" = 0 ]; then ok "$2"; else bad "$2"; fi; }
SRC_SHA=$(sha256sum "$0" | cut -d' ' -f1)
lock() {   NLOCK=$((NLOCK + 1));     local f; f=$(printf "%s/lock_%02d.log" "$EVD" $NLOCK)
  "$RS" --vanilla -e "source('$RDIR/lowp_seal.R'); r <- lowp_truth_lock('$ROOT', TRUE); print(unlist(r))" >"$f" 2>&1; local rc=$?; { echo "--- $(basename "$f") (exit $rc)"; cat "$f"; } >> "$RUNLOG"; return $rc; }
unlock() { NUNLOCK=$((NUNLOCK + 1)); local f; f=$(printf "%s/unlock_%02d.log" "$EVD" $NUNLOCK)
  "$RS" --vanilla -e "source('$RDIR/lowp_seal.R'); r <- lowp_truth_lock('$ROOT', FALSE); print(unlist(r))" >"$f" 2>&1; local rc=$?; { echo "--- $(basename "$f") (exit $rc)"; cat "$f"; } >> "$RUNLOG"; return $rc; }
lastlog() { tr '\n' ' ' < "$1" | cut -c1-160; }
open_all() { for t in "${TRUTHS[@]}"; do chmod 755 "$t" 2>/dev/null; find "$t" -type d -exec chmod 755 {} + 2>/dev/null; find "$t" -type f -exec chmod 444 {} + 2>/dev/null; done; }
sha_list() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$2"; }
modes() { for i in 0 1; do find "${TRUTHS[$i]}" -printf '%m %y %p\n' 2>/dev/null; done > "$EVD/modes_$1.txt"; }
finish() {
  local rc=$?; open_all
  [ "$rc" = 0 ] && [ "$fails" != 0 ] && rc=1
  say ""; say "SOURCE_SHA256 $SRC_SHA  $(basename "$0")"; say "CHECKS $ncheck FAILED $fails"; say "FINAL_EXIT_STATUS $rc"; say "EVIDENCE_DIR $EVD"
  { echo "script_sha256 $SRC_SHA"; echo "checks $ncheck"; echo "failed $fails"; echo "final_exit_status $rc"; echo "finished_utc $(date -u +%FT%TZ)"; } > "$EVD/final_status.txt"
  [ "$CLEAN" = 1 ] && rm -rf "$EVD/tmp"
  exit $rc
}
trap finish EXIT
say "# truth-lock test on $(hostname) at $(date -u +%FT%TZ) as $(id -un) (uid $(id -u)); study $ROOT; R dir $RDIR; evidence dir $EVD"
say "# SOURCE_SHA256 $SRC_SHA  $(basename "$0")"
say "# filesystem: $(df -PT "$ROOT" 2>/dev/null | tail -n 1)"
first_file() { awk -F, 'NR==2 {gsub(/"/,"",$2); print $2}' "$1"; }   # truth_manifest_lowp.csv: dataset_id,file,...
PROD_F=$ROOT/$(first_file "$ROOT/manifests/truth_manifest_lowp.csv"); DEV_F=$ROOT/dev/$(first_file "$ROOT/dev/manifests/truth_manifest_lowp.csv")
IN_F=$ROOT/$(awk -F, 'NR==2 {gsub(/"/,"",$8); print $8}' "$ROOT/manifests/inputs_manifest_lowp.csv")
[ -f "$PROD_F" ] && [ -f "$DEV_F" ] && [ -f "$IN_F" ] || { say "cannot find the first truth/input files named by the manifests ($PROD_F, $DEV_F, $IN_F)"; exit 3; }

say "== before locking"
n_prod=$(find "$ROOT/truth" -type f | wc -l); n_dev=$(find "$ROOT/dev/truth" -type f | wc -l)
m_prod=$(( $(wc -l < "$ROOT/manifests/truth_manifest_lowp.csv") - 1 )); m_dev=$(( $(wc -l < "$ROOT/dev/manifests/truth_manifest_lowp.csv") - 1 ))
[ "$n_prod" = 1200 ] && [ "$m_prod" = 1200 ] && [ "$n_dev" = 60 ] && [ "$m_dev" = 60 ]; chk $? "file counts: truth $n_prod (manifest $m_prod), dev/truth $n_dev (manifest $m_dev); expected 1200 / 60"
for i in 0 1; do sha_list "${TRUTHS[$i]}" "$EVD/pre_${TNAME[$i]}.sha"; done
modes before_lock
"$RS" --vanilla -e "invisible(readRDS('$PROD_F')); invisible(readRDS('$DEV_F'))" >/dev/null 2>&1; chk $? "readRDS works on a production and a dev truth file before locking"

say "== lock (one call)"
lock; chk $? "lowp_truth_lock(root, TRUE) exits 0 ($(lastlog "$EVD/lock_01.log"))"
modes locked
for i in 0 1; do t=${TRUTHS[$i]}
  m=$(stat -c %a "$t"); [ "$m" = 0 ]; chk $? "$t is mode 000 (stat says $m)"
  ls "$t" >/dev/null 2>"$EVD/tmp/ls_$i.err"; [ $? -ne 0 ]; chk $? "ls $t fails"
  find "$t" -type f 2>"$EVD/tmp/find_$i.err" | grep -q .; [ $? -ne 0 ]; chk $? "find $t lists no file"
done
cat "$PROD_F" >/dev/null 2>"$EVD/tmp/cat_prod.err"; [ $? -ne 0 ]; chk $? "cat of a production truth file fails"
cat "$DEV_F" >/dev/null 2>"$EVD/tmp/cat_dev.err"; [ $? -ne 0 ]; chk $? "cat of a dev truth file fails"
"$RS" --vanilla -e "r <- try(readRDS('$PROD_F'), silent = TRUE); q(status = if (inherits(r, 'try-error')) 0 else 1)" >"$EVD/tmp/rds_prod.out" 2>&1; chk $? "readRDS of a production truth file fails (R process)"
"$RS" --vanilla -e "r <- try(readRDS('$DEV_F'), silent = TRUE); q(status = if (inherits(r, 'try-error')) 0 else 1)" >"$EVD/tmp/rds_dev.out" 2>&1; chk $? "readRDS of a dev truth file fails (R process)"
cat "$IN_F" >/dev/null 2>&1; chk $? "inputs/ file still readable while truth is locked"
cat "$ROOT/manifests/truth_manifest_lowp.csv" >/dev/null 2>&1; chk $? "manifests still readable while truth is locked"
say "== lock again (idempotence)"
lock; chk $? "second lock call exits 0"
[ "$(stat -c %a "$ROOT/truth")" = 0 ] && [ "$(stat -c %a "$ROOT/dev/truth")" = 0 ]; chk $? "both trees still mode 000"

say "== unlock (one call)"
unlock; chk $? "lowp_truth_lock(root, FALSE) exits 0 ($(lastlog "$EVD/unlock_01.log"))"
check_open() {   # $1 = label
  for i in 0 1; do t=${TRUTHS[$i]}
    bd=$(find "$t" -type d ! -perm 755 | wc -l); bf=$(find "$t" -type f ! -perm 444 | wc -l); nf=$(find "$t" -type f | wc -l)
    [ "$bd" = 0 ] && [ "$bf" = 0 ]; chk $? "$1: $t has $bd directories not 755 and $bf files not 444 ($nf files)"
    sha_list "$t" "$EVD/post_$(echo "$1" | tr ' ' '_')_${TNAME[$i]}.sha"
    cmp -s "$EVD/post_$(echo "$1" | tr ' ' '_')_${TNAME[$i]}.sha" "$EVD/pre_${TNAME[$i]}.sha"; chk $? "$1: $t file SHA-256 identical to before locking"
  done
  modes "$(echo "$1" | tr ' ' '_')"
  "$RS" --vanilla -e "invisible(readRDS('$PROD_F')); invisible(readRDS('$DEV_F'))" >/dev/null 2>&1; chk $? "$1: readRDS works on a production and a dev truth file"
}
check_open "after unlock"

say "== bad state 1: only the top directories reopened (review finding 1)"
lock; chk $? "lock"
chmod 755 "$ROOT/truth" "$ROOT/dev/truth"
unlock; chk $? "one unlock call from 'top open, descendants 000' exits 0"
check_open "recovery 1"

say "== bad state 2: interrupted lock, top directories 000 and some files/directories still open"
lock; chk $? "lock"
chmod 755 "$ROOT/truth"; chmod 755 "$ROOT/truth/p0020"; chmod 444 "$PROD_F" 2>/dev/null; chmod 000 "$ROOT/truth"
unlock; chk $? "one unlock call from a mixed state exits 0"
check_open "recovery 2"

say ""
if [ "$fails" = 0 ]; then say "ALL PASS (ordinary-user Linux truth lock/unlock on production and dev truth trees)"; exit 0; else say "$fails CHECK(S) FAILED"; exit 1; fi
