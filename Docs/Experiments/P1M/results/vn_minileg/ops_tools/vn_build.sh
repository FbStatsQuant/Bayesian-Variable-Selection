#!/usr/bin/env bash
# vn_build.sh -- build the F2 campaign binary ONCE on NOTS (HQ 4a47e8a4): shallow clone of e993ece2 (tag p1m-freeze-F2) in scratch, shared worktree
# code_ws/VN_e993ece2_code (clean, HEAD == F2), out-of-tree build (build dir in scripts/VN_ID_1/build), V sapphirerapids via the driver's build.sh (nice, -j3,
# the standard flags), `version` (env.sh sourced) must show git_commit == F2. Writes ONE `BUILD_F2` line to staging/vn_minileg/deploy_F2.log (refused if one exists).
# NEVER submits. The precision leg's deploy_leg.log and binaries are not touched.
set -euo pipefail; . "$(dirname "$0")/common.sh"
awk -F'\t' '$3=="BUILD_F2"{f=1} END{exit f?0:1}' "$LOG" 2>/dev/null && { echo "REFUSING: $LOG already has a BUILD_F2 line (one F2 build)" >&2; exit 65; }
SRC=$STG/scripts/$BATCH; CL=$STG/clone_e993ece2
(cd "$SRC" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS" >&2; exit 66; }
python3 - "$SRC/plan.resolved.json" "$F2" <<'PY'
import json, sys
p = json.load(open(sys.argv[1])); assert p["code_commit"] == sys.argv[2] and p["batch"] == "VN_ID_1" and p["island_isa"] == "sapphirerapids" and not p.get("warnings"), p
print("plan OK: code_commit == F2; fits", len(p["fits"]), "; worst", p["worst_case_core_h"])
PY
home_guard
st=$(ssh $NOTS "if [[ -e $D/scratch/runs/$BATCH/submissions.jsonl ]]; then echo EXISTS; else echo FRESH; fi" 2>/dev/null || true); [[ $st == FRESH ]] || { echo "REFUSING: state of $BATCH: '$st'" >&2; exit 65; }
CN=$D/scratch/vn_minileg/clone_e993ece2
ssh $NOTS "mkdir -p $D/scratch/vn_minileg $D/scratch/runs/$BATCH $D/scripts/$BATCH"
ssh $NOTS "git -C $CN cat-file -e $F2^{commit} 2>/dev/null" && echo "clone already holds F2" || rs "$CL"/ $NOTS:$CN/
ssh $NOTS "set -e; [[ \$(git -C $CN rev-parse $F2:$CORE_PATH) == $CORE_TREE ]] && echo 'clone ok: core tree = pin'"
rs --exclude code --exclude bin --exclude build "$SRC"/ $NOTS:$D/scripts/$BATCH/
CW=$(ssh $NOTS "readlink -f $D/scratch")/code_ws/VN_e993ece2_code
ssh $NOTS "set -e; cd $D/scripts/$BATCH && sha256sum --quiet -c SHA256SUMS && echo 'SHA256SUMS verified on NOTS'
  mkdir -p \$(dirname $CW); git -C $CN worktree remove --force $CW 2>/dev/null || true; rm -rf $CW; git -C $CN worktree prune; git -C $CN worktree add -q --detach $CW $F2
  [[ \$(git -C $CW rev-parse HEAD) == $F2 ]] && [[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]] && echo \"worktree $CW at $F2 (clean)\"
  rm -rf $D/scripts/$BATCH/code; ln -s $CW $D/scripts/$BATCH/code"
home_guard
ssh $NOTS "cd $D/scripts/$BATCH && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 3 build_stdout.log; [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
ssh $NOTS "( set +u; source $D/scripts/$BATCH/env.sh >/dev/null 2>&1; $D/scripts/$BATCH/bin/smcbvs4 version 2>&1 ) > $D/scripts/$BATCH/bin/version.json || true"
V=$(ssh $NOTS "cat $D/scripts/$BATCH/bin/version.json")
GC=$(echo "$V" | grep -o '"git_commit": *"[^"]*"' | head -1 | grep -o '"[^"]*"$' | tr -d '"'); ISA=$(echo "$V" | grep -o '"island_isa": *"[^"]*"' | head -1 | grep -o '"[^"]*"$' | tr -d '"'); LIBM=$(echo "$V" | grep -c '"pass": *true' || true)
echo "version: git_commit=$GC island_isa=$ISA libm_selftest_pass=$LIBM"
[[ $GC == "$F2" && $ISA == sapphirerapids && $LIBM -ge 1 ]] || { echo "FATAL: version check failed (git_commit '$GC', isa '$ISA', libm '$LIBM')" >&2; exit 67; }
ssh $NOTS "[[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]]" || { echo "FATAL: worktree dirty after the build" >&2; exit 67; }
SHA=$(ssh $NOTS "sha256sum $D/scripts/$BATCH/bin/smcbvs4" | cut -d' ' -f1); HM=$(home_mb)
printf '%s\t%s\tBUILD_F2\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$BATCH" "$SHA" "$GC" "$ISA" "$LIBM" "$HM" "${WHO:-ops-sonnet}" >> "$LOG"
echo "BUILD_F2 $BATCH sha256 $SHA git_commit $GC isa $ISA (the F2 campaign binary, built ONCE); home ${HM} MB"
