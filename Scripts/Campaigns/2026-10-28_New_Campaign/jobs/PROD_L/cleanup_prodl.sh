#!/bin/bash
# cleanup_prodl.sh -- remove what ONE pilot put on NOTS and say whether the removal is VERIFIED. Runs on NOTS (through `ssh nots`) as fb31 AFTER every
# result/log folder was pulled, sha256-verified and deleted by ops/transfer/nots_pull.py --delete.
#   bash cleanup_prodl.sh STAMP            dry run: lists the targets, changes nothing
#   bash cleanup_prodl.sh STAMP --yes      removes them
# Everything the pilot staged lives in its own folder HOME/runs/<PID> (code, dev inputs, study copy with truth, job ids); nothing shared is
# touched. Targets (exactly): HOME/runs/<PID>, SCR/runs/<PID>_cache, SCR/runs/<PID>_tmp.
# Exit status: 0 CLEANUP VERIFIED (nothing left, guard OK); 1 removal done but residue or guard problem (UNVERIFIED); 3 REFUSED (results/logs still on
# scratch, ownership marker missing or wrong, a pilot job still queued/running, ids file missing); 4 REFUSED because the scheduler could not be
# inspected (never assume idle).
set -uo pipefail
STAMP="${1:?usage: cleanup_prodl.sh STAMP [--yes]}"; shift || true
YES=0
receipt=
while [ $# -gt 0 ]; do case "$1" in --yes) YES=1; shift;; --receipt) receipt="${2:?}"; shift 2;; *) echo "unknown option $1" >&2; exit 2;; esac; done
[[ "$STAMP" =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || { echo "bad STAMP" >&2; exit 2; }
if [ -n "$receipt" ]; then
  parent=$(realpath -e -- "$(dirname -- "$receipt")") || exit 2
  root=$(realpath -m -- "${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}/runs/${STAMP}_lowp_prodL")
  receipt="$parent/$(basename -- "$receipt")"
  [ ! -L "$receipt" ] || { echo 'receipt must not be a symlink' >&2; exit 2; }
  for target in "$root" "$(realpath -m -- "${NC_SCR_ROOT:-/scratch/fb31/New_Campaign}/runs/${STAMP}_lowp_prodL_cache")" "$(realpath -m -- "${NC_SCR_ROOT:-/scratch/fb31/New_Campaign}/runs/${STAMP}_lowp_prodL_tmp")"; do
    case "$receipt" in "$target"|"$target"/*) echo 'receipt must be outside removed tree' >&2; exit 2;; esac
  done
  if [ "$YES" = 1 ] && [ -z "${CLEANUP_FROM_MEMORY:-}" ]; then
    self=$(cat -- "$0") || exit 2
    for v in NC_HOME_ROOT NC_SCR_ROOT GUARD SQUEUE SACCT; do val=${!v:-}; case "$val" in ""|/*) ;; */*) export "$v=$PWD/$val";; esac; done
    cd / || exit 2
    exec env CLEANUP_FROM_MEMORY=1 CLEANUP_SCRIPT_TEXT="$self" bash -c "$self" cleanup_prodl.sh "$STAMP" --yes --receipt "$receipt"
  fi
  args=("$STAMP"); [ "$YES" = 0 ] || args+=(--yes)
  rc=0
  if [ -n "${CLEANUP_SCRIPT_TEXT:-}" ]; then bash -c "$CLEANUP_SCRIPT_TEXT" cleanup_prodl.sh "${args[@]}" > "$receipt" 2>&1 || rc=$?
  else bash "$0" "${args[@]}" > "$receipt" 2>&1 || rc=$?; fi
  printf 'exit_status=%s\n' "$rc" >> "$receipt"; cat "$receipt"; exit "$rc"
fi
# B3 (D44, OPS-4 pilot 20261030T0313Z): bash keeps reading a script FILE while it runs, and the shell's working directory is held open too. Run from
# HOME/runs/<PID>/code/lowp/pilot/ on NFS, the folder being removed then keeps a silly-renamed .nfs* file and the removal cannot be verified. A --yes
# run therefore re-executes itself FROM MEMORY (bash -c with the script text; no file of the tree stays open) after leaving every directory (cd /).
# (Sol PILOT7D R7D-3) Path-valued overrides given RELATIVE to the caller's directory are resolved against it BEFORE leaving it, and exported
# through the re-exec; bare command names (no "/") stay subject to PATH lookup. The dry run does not change directory at all.
if [ "$YES" = 1 ] && [ -z "${CLEANUP_FROM_MEMORY:-}" ]; then
  self=$(cat -- "$0") || { echo "cannot read $0" >&2; exit 2; }
  for v in NC_HOME_ROOT NC_SCR_ROOT GUARD SQUEUE SACCT; do
    val=${!v:-}
    case "$val" in ""|/*) ;; */*) export "$v=$PWD/$val";; *) ;; esac
  done
  cd / || { echo "cannot leave the working directory" >&2; exit 2; }
  exec env CLEANUP_FROM_MEMORY=1 bash -c "$self" cleanup_prodl.sh "$STAMP" --yes
fi
[ -z "${CLEANUP_FROM_MEMORY:-}" ] || echo "== running from memory (the script file and the working directory hold nothing open in the removed tree)"
HOME_ROOT="${NC_HOME_ROOT:-/home/fb31/projects/BVS/New_Campaign}"
SCR_ROOT="${NC_SCR_ROOT:-/scratch/fb31/New_Campaign}"
GUARD="${GUARD:-$HOME_ROOT/code/ops/guard.sh}"
SQUEUE="${SQUEUE:-squeue}"; SACCT="${SACCT:-sacct}"
PID="${STAMP}_lowp_prodL"
export STAMP
[ ! -r "$HOME_ROOT/runs/$PID/code/prod_l/prodl.env" ] || source "$HOME_ROOT/runs/$PID/code/prod_l/prodl.env"

refuse() { echo "REFUSED: $*" >&2; exit "${2:-3}"; }
# ---- canonical roots and exact targets (no linked ancestor, no linked intermediate directory) -----------------------------
canon() { readlink -f -- "$1"; }
HR=$(canon "$HOME_ROOT") || refuse "cannot canonicalise $HOME_ROOT" 4
SR=$(canon "$SCR_ROOT") || refuse "cannot canonicalise $SCR_ROOT" 4
[ -n "$HR" ] && [ -n "$SR" ] && [ "$(basename "$HR")" = New_Campaign ] && [ "$(basename "$SR")" = New_Campaign ] || refuse "the campaign roots do not resolve to New_Campaign folders ($HR, $SR)" 4
# every target is spelled from the CANONICAL root; a target that resolves anywhere else (a link at runs/, at runs/<PID>, or higher up below the root) is refused
RUN_HOME="$HR/runs/$PID"
TARGETS=("$RUN_HOME" "$SR/runs/${PID}_cache" "$SR/runs/${PID}_tmp")
for dd in "$HR/runs" "$SR/runs"; do
  if [ -e "$dd" ] || [ -L "$dd" ]; then
    [ ! -L "$dd" ] && [ "$(canon "$dd")" = "$dd" ] || refuse "$dd is a link or resolves elsewhere ($(canon "$dd")): refusing to delete below it" 4
  fi
done
for t in "${TARGETS[@]}"; do
  case "$t" in "$HR"/runs/*|"$SR"/runs/*) ;; *) refuse "target outside the campaign runs folders: $t" 4;; esac
  case "$t" in *..*|*bench20261019*|*/BVS/Benchmarks*|"$HR/code"*) refuse "forbidden target $t" 4;; esac
  if [ -e "$t" ] || [ -L "$t" ]; then
    [ ! -L "$t" ] || refuse "target is a symlink: $t" 4
    [ "$(canon "$t")" = "$t" ] || refuse "target resolves to $(canon "$t"), not to $t (linked directory)" 4
  fi
done
if [ -e "$RUN_HOME" ]; then
  [ -r "$RUN_HOME/OWNER" ] && grep -q "lowp_prodL $STAMP" "$RUN_HOME/OWNER" || refuse "$RUN_HOME has no OWNER marker for this pilot: not ours, not deleting" 3
  [ -r "$RUN_HOME/JOBIDS.tsv" ] || refuse "$RUN_HOME/JOBIDS.tsv is missing: cannot establish that no pilot job is active" 3
fi
# ---- downloaded? -------------------------------------------------------------------------------------------------------
left=""
for p in "$SR/results/${STAMP}_lowp_"* "$SR/logs/$PID"; do [ -e "$p" ] && left="$left$p"$'\n'; done
[ -z "$left" ] || { echo "REFUSED: pilot results/logs are still in scratch (pull, verify and delete them first):" >&2; printf '%s' "$left" >&2; exit 3; }
# ---- scheduler inspection (fail closed) ---------------------------------------------------------------------------------
Q=$("$SQUEUE" -h -u "${USER:-fb31}" -o '%i|%j|%T' 2>&1); qrc=$?
[ $qrc = 0 ] || { echo "REFUSED: squeue failed (exit $qrc): $Q" >&2; exit 4; }
if [ -e "$RUN_HOME/JOBIDS.tsv" ]; then
  IDS=$(awk -F'\t' 'NR>1 && $3 ~ /^[0-9]+$/ {print $3}' "$RUN_HOME/JOBIDS.tsv")
  [ -n "$IDS" ] || refuse "no job ids recorded in $RUN_HOME/JOBIDS.tsv" 3
  active=$(printf '%s\n' "$Q" | awk -F'|' -v ids="$(echo $IDS | tr ' ' ',')" 'BEGIN{n=split(ids,a,","); for(i=1;i<=n;i++) want[a[i]]=1} NF>=3 {split($1,b,"_"); if (want[b[1]] || $2 ~ /^lowpL_/) print}')
  [ -z "$active" ] || { echo "REFUSED: pilot jobs are still queued or running (cancel only by explicit id):" >&2; echo "$active" >&2; exit 3; }
  S=$("$SACCT" -X -n -P -j "$(echo $IDS | tr ' ' ',')" -o JobID,State 2>&1); src=$?
  [ $src = 0 ] || { echo "REFUSED: sacct failed (exit $src): $S" >&2; exit 4; }
  nonterm=$(printf '%s\n' "$S" | awk -F'|' -v ids="$(echo $IDS | tr ' ' ',')" 'BEGIN{split(ids,a,",");for(i in a)want[a[i]]=1} NF>=2 {split($1,b,"_");if(want[b[1]])seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|PREEMPTED|BOOT_FAIL|DEADLINE)/)print $0} END{for(i in want)if(!seen[i])print "missing " i}')
  [ -z "$nonterm" ] || { echo "REFUSED: accounting shows non-terminal pilot jobs:" >&2; echo "$nonterm" >&2; exit 3; }
else
  printf '%s\n' "$Q" | grep -q '|lowpL_' && { echo "REFUSED: lowp_p* jobs are queued or running" >&2; exit 3; }
fi
echo "== LOWP pilot clean-up for $PID (yes=$YES); scheduler inspected: no pilot job active"
for t in "${TARGETS[@]}"; do if [ -e "$t" ]; then echo "remove   $t ($(du -sk -- "$t" 2>/dev/null | cut -f1) KB)"; else echo "absent   $t"; fi; done
[ $YES = 1 ] || { echo "(dry run; add --yes to remove)"; exit 0; }

# ---- removal (only the explicit, pilot-owned targets) -----------------------------------------------------------------------
# a failed wave unlock could leave the study copy at mode 000: restore OUR owner access first
if [ -d "$RUN_HOME/study" ]; then
  chmod u+rwx "$RUN_HOME/study" "$RUN_HOME/study/truth" "$RUN_HOME/study/dev" "$RUN_HOME/study/dev/truth" 2>/dev/null
  find "$RUN_HOME/study" -type d ! -perm -700 -exec chmod u+rwx {} + 2>/dev/null
  find "$RUN_HOME/study" -type d -exec chmod u+rwx {} + 2>/dev/null
fi
rm_fail=0
for t in "${TARGETS[@]}"; do if [ -e "$t" ]; then rm -rf -- "$t" || rm_fail=1; fi; done
# ---- verification -------------------------------------------------------------------------------------------------------
unver=""
[ $rm_fail = 0 ] || unver="$unver rm-failed"
# PROD-L: every name this run created starts with "<STAMP>_lowp_" (run folder <STAMP>_lowp_prodL*, result folders <STAMP>_lowp_<piece>)
resid=$(find "$HR" "$SR" -maxdepth 4 -name "${STAMP}_lowp_*" 2>&1); frc=$?
if [ $frc != 0 ]; then unver="$unver residue-search-failed(rc=$frc)"; fi
resid=$(printf '%s\n' "$resid" | grep -v '^find:' || true)
[ -z "$resid" ] || unver="$unver residue-found"
echo "== residue search:"; if [ -n "$resid" ]; then echo "$resid"; else echo "(none)"; fi
echo "== guard after clean-up:"
g=$("$GUARD" 0 2>&1); grc=$?; echo "$g"
[ $grc = 0 ] || unver="$unver guard-rc=$grc"
if [ -z "$unver" ]; then echo "CLEANUP VERIFIED: nothing of the pilot remains and the guard reports OK."; exit 0; fi
echo "CLEANUP UNVERIFIED:$unver" >&2; exit 1
