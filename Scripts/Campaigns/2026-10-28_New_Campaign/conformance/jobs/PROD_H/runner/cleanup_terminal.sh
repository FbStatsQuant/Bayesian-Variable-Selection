#!/usr/bin/env bash
# cleanup_terminal.sh -- TERMINAL cleanup of the artefacts a killed attempt leaves behind (Sol review 2, R2-5). NOTS login node, OPS.
#   bash RUN_DIR/runner/cleanup_terminal.sh [--dry-run]
# A SIGKILLed / OOM-killed / node-lost fit leaves a <prefix>.lock directory (owner.txt) and atomic-write remnants (<prefix>.*.tmp.<pid>), for the
# primary units (SMCBVS.*) and for the P5 retries (P5_retry/SMCBVS_p5retry.*). Neither task.sh nor p5_task.sh removes them from another host, and
# make_manifests.sh refuses a tree that contains them. This script is the single, last-step path (run it after final_accounting.sh, before
# make_manifests.sh; it is safe to run earlier whenever no job of the run is live):
#   0. refuses test hooks; REFUSES unless EVERY job recorded in jobs.tsv is gone from squeue AND terminal in sacct (fail closed: any scheduler
#      error refuses). So no recorded job of this run can still be writing.
#   1. finds every *.lock directory and *.tmp.* / *.tmp file under results/<RUN_ID>. An artefact is PROVEN stale only if (a) its unit has a durable
#      attempt record whose array job is a job of this run (primary: LOGROOT/attempts/<case>/attempt_*.start.json, all of them; P5: LOGROOT/p5_attempts/
#      <case>.start.json AND the unit is in p5/units.tsv), and (b) its owner is not a live process on this host. Anything else is UNPROVEN: it is
#      reported, left untouched, and the exit status is 3.
#   2. each proven artefact is ARCHIVED (moved, with its owner.txt, as <name>.archived; a `.tmp.` name becomes `_tmp.`) under LOGROOT/cleanup/<utc>/
#      <relative path>, with CLEANUP_LOG.tsv (path, kind, owner, size, mtime, attempt job); a small summary goes to RUN_DIR/cleanup/. Only then is the
#      artefact gone from the results tree. Nothing else is touched: result files, .done/.sha256, attempts/ and p5_attempts/ (the durable attempt
#      records) are never modified (their file count is checked before and after), and NO FIT IS EVER RELAUNCHED.
# Exit: 0 clean (nothing unproven) | 3 unproven artefacts remain (inspect by hand) | 2 refusal.
set -euo pipefail
RUNNER_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$RUNNER_DIR/common.sh"
nc_refuse_hooks
[[ $# == 0 || ( $# == 1 && $1 == --dry-run ) ]] || { echo "usage: cleanup_terminal.sh [--dry-run]" >&2; exit 64; }
DRY=${1:-}
RUN_DIR="$HOME_ROOT/runs/$(basename "$(cd "$RUNNER_DIR/.." && pwd)")"
nc_load_run "$RUN_DIR"
TERMINAL='^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)'

# 0. every recorded job is dead
ids_all=$(nc_job_ids "$RUN_DIR")
[[ -n $ids_all ]] || nc_fail "no job ids in $RUN_DIR/jobs.tsv"
live=$(nc_live_jobs "$RUN_DIR") || nc_fail "squeue failed (fail closed)"
[[ -z $live ]] || nc_fail "job(s) of this run still queued, running or held: $(echo $live): a live job may still own these artefacts"
sa=$(sacct -j "$(paste -sd, <<< "$ids_all")" -P -n -X -o JobID,State) || nc_fail "sacct failed (fail closed)"
for j in $ids_all; do
  rows=$(awk -F'|' -v j="$j" '{ split($1, a, "_"); if (a[1] == j) print $2 }' <<< "$sa")
  [[ -n $rows ]] || nc_fail "job $j is missing from sacct: its state cannot be established (fail closed)"
  bad=$(grep -v -E "$TERMINAL" <<< "$rows" || true)
  [[ -z $bad ]] || nc_fail "job $j has a task that is not terminal in sacct ($(head -n 1 <<< "$bad")): refusing to touch anything"
done
echo "== every recorded job ($(echo $ids_all | wc -w)) is out of the queue and terminal in sacct"

array_job_of() { sed -n 's/.*"array_job":"\([0-9]*\)".*/\1/p' "$1" | head -n 1; }
is_run_job() { grep -qx "$1" <<< "$ids_all"; }
HOST_S=$(hostname -s 2>/dev/null || true); HOST_L=$(hostname 2>/dev/null || true)
proof() {   # proof REL : prints "primary|p5 <job>" and returns 0 if the artefact of REL is proven stale; else prints the reason and returns 1
  local rel=$1 case_id kind j f n=0
  IFS=/ read -r -a parts <<< "$rel"
  case_id=${parts[1]:-}
  [[ ${parts[0]:-} =~ ^p(0500|1000)$ && $case_id =~ ^p(0500|1000)_S[1-6]_r[0-9]{3}_(c100|c050)$ ]] || { echo "not under a unit folder (pNNNN/<case_id>/)"; return 1; }
  if [[ ${parts[2]:-} == P5_retry ]]; then
    f=$LOGROOT/p5_attempts/$case_id.start.json
    [[ -s $f ]] || { echo "no P5 attempt record for $case_id"; return 1; }
    awk -F'\t' -v c="$case_id" 'NR > 1 && $2 == c { f = 1 } END { exit !f }' "$RUN_DIR/p5/units.tsv" 2>/dev/null || { echo "$case_id is not a unit selected by p5_submit.sh"; return 1; }
    j=$(array_job_of "$f"); is_run_job "$j" || { echo "the P5 attempt record names job '$j', not a job of this run"; return 1; }
    echo "p5 $j"; return 0
  fi
  for f in "$LOGROOT"/attempts/"$case_id"/attempt_*.start.json; do
    [[ -s $f ]] || continue
    n=$((n + 1)); j=$(array_job_of "$f"); is_run_job "$j" || { echo "attempt record $(basename "$f") names job '$j', not a job of this run"; return 1; }
  done
  (( n > 0 )) || { echo "no attempt record for $case_id"; return 1; }
  echo "primary $j"; return 0
}
owner_alive() {   # owner_alive DIR : 0 if DIR/owner.txt names a live process on THIS host
  local pid host
  [[ -r $1/owner.txt ]] || return 1
  pid=$(awk '$1 == "pid" { print $2; exit }' "$1/owner.txt"); host=$(awk '$1 == "host" { print $2; exit }' "$1/owner.txt")
  [[ $pid =~ ^[0-9]+$ && ( $host == "$HOST_S" || $host == "$HOST_L" ) && -e /proc/$pid ]]
}

n_att_before=$({ find "$LOGROOT/attempts" "$LOGROOT/p5_attempts" -type f 2>/dev/null || true; } | wc -l)   # a run without P5 has no p5_attempts/: find exits 1, which pipefail must not turn into a crash
ts=$(date -u +%Y%m%dT%H%M%SZ); ARCH=$LOGROOT/cleanup/$ts
mapfile -t found < <(find "$RES_RUN" \( -name '*.lock' -o -name '*.tmp.*' -o -name '*.tmp' \) | LC_ALL=C sort)
echo "== ${#found[@]} lock/temporary artefact(s) under $RES_RUN"
proven=0; unproven=0; LOGTSV=$(mktemp "${TMPDIR:-/tmp}/cleanup_log.XXXXXX"); trap 'rm -f "$LOGTSV"' EXIT
printf 'path\tkind\towner\tsize_bytes\tmtime_utc\tstatus\tdetail\n' > "$LOGTSV"
for path in ${found[@]+"${found[@]}"}; do
  [[ -e $path ]] || continue                    # inside a lock directory that was archived a moment ago: it moved with it
  rel=${path#"$RES_RUN"/}
  kind=tmp; [[ -d $path ]] && kind=lock_dir
  owner=""; [[ -r $path/owner.txt ]] && owner=$(tr '\n' ';' < "$path/owner.txt")
  size=$(du -sb "$path" 2>/dev/null | cut -f1 || echo 0); mt=$(date -u -r "$path" +%FT%TZ 2>/dev/null || echo "")
  if ! detail=$(proof "$rel"); then
    unproven=$((unproven + 1)); printf '%s\t%s\t%s\t%s\t%s\tUNPROVEN\t%s\n' "$rel" "$kind" "$owner" "$size" "$mt" "$detail" >> "$LOGTSV"; echo "UNPROVEN $rel: $detail"; continue
  fi
  if [[ $kind == lock_dir ]] && owner_alive "$path"; then
    unproven=$((unproven + 1)); printf '%s\t%s\t%s\t%s\t%s\tUNPROVEN\towner process is alive on this host\n' "$rel" "$kind" "$owner" "$size" "$mt" >> "$LOGTSV"; echo "UNPROVEN $rel: owner alive on this host"; continue
  fi
  proven=$((proven + 1)); printf '%s\t%s\t%s\t%s\t%s\tPROVEN_STALE\t%s\n' "$rel" "$kind" "$owner" "$size" "$mt" "$detail" >> "$LOGTSV"
  name=$(basename "$rel"); dest=$ARCH/$(dirname "$rel")/${name//.tmp/_tmp}.archived
  if [[ $DRY == --dry-run ]]; then echo "WOULD ARCHIVE $rel -> $dest ($detail)"; continue; fi
  mkdir -p -- "$(dirname "$dest")"
  [[ ! -e $dest ]] || nc_fail "archive target $dest exists"
  mv -- "$path" "$dest"
  if [[ $kind == lock_dir ]]; then       # a temporary file inside the lock directory must not keep a *.tmp.* name (make_manifests.sh refuses it)
    while IFS= read -r t; do b=$(basename "$t"); mv -- "$t" "$(dirname "$t")/${b//.tmp/_tmp}"; done < <(find "$dest" -depth -type f \( -name '*.tmp.*' -o -name '*.tmp' \))
  fi
  echo "ARCHIVED $rel -> $dest ($detail)"
done
if [[ $DRY != --dry-run && ${#found[@]} -gt 0 ]]; then
  mkdir -p -- "$ARCH" "$RUN_DIR/cleanup"; cp "$LOGTSV" "$ARCH/CLEANUP_LOG.tsv"; cp "$LOGTSV" "$RUN_DIR/cleanup/cleanup_$ts.tsv"
fi
n_att_after=$({ find "$LOGROOT/attempts" "$LOGROOT/p5_attempts" -type f 2>/dev/null || true; } | wc -l)   # a run without P5 has no p5_attempts/: find exits 1, which pipefail must not turn into a crash
[[ $n_att_before == "$n_att_after" ]] || nc_fail "BUG: the number of durable attempt records changed ($n_att_before -> $n_att_after)"
echo "== cleanup: proven stale $proven${DRY:+ (dry run: nothing moved)}, unproven $unproven; durable attempt records unchanged ($n_att_after files); no fit was launched"
[[ $unproven == 0 ]] || { echo "UNPROVEN artefacts remain: inspect them by hand; make_manifests.sh will refuse until they are resolved" >&2; exit 3; }
exit 0
