#!/usr/bin/env bash
# gc_t2thr_deploy.sh -- GC_T2THR (HQ H-47): deploy the ONE-task two-thread-count check: COPYBIN of the F2 binary (BUILD_F2 in deploy_gc.log), NO build, NEVER submits. Like gc_deploy_wave.sh for a hand-written batch.
set -euo pipefail; . "$(dirname "$0")/common.sh"
B=GC_T2THR; SHA=$(f2_sha); [[ -n $SHA ]] || { echo "REFUSING: no BUILD_F2 line in $LOG" >&2; exit 65; }
(cd "$SCRIPTS/$B" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS differ in $B" >&2; exit 66; }
home_guard
st=$(ssh $NOTS "if [[ -e $D/scratch/runs/$B/submissions.jsonl ]]; then echo EXISTS; else echo FRESH; fi" 2>/dev/null || true)
[[ $st == FRESH ]] || { echo "REFUSING: state of $B is '$st'" >&2; exit 65; }
ssh $NOTS "mkdir -p $D/scratch/runs/$B $D/scripts/$B"
rs --exclude bin "$SCRIPTS/$B"/ $NOTS:$D/scripts/$B/
ssh $NOTS "cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS'"
ssh $NOTS "set -e; M=$D/scripts/$MASTER/bin; [[ \$(sha256sum \$M/smcbvs4 | cut -d' ' -f1) == $SHA ]] || { echo 'FATAL: master binary != BUILD_F2' >&2; exit 67; }
  mkdir -p $D/scripts/$B/bin; cp -p \$M/smcbvs4 $D/scripts/$B/bin/smcbvs4; cp -p \$M/version.json $D/scripts/$B/bin/version.json
  sha256sum $D/scripts/$B/bin/smcbvs4 > $D/scripts/$B/bin/smcbvs4.sha256; echo '$MASTER' > $D/scripts/$B/bin/COPIED_FROM
  [[ \$(sha256sum $D/scripts/$B/bin/smcbvs4 | cut -d' ' -f1) == $SHA ]] && echo '$B: bin/smcbvs4 copied from $MASTER, sha256 == BUILD_F2'"
ssh $NOTS "( set +u; source $D/scripts/$B/env.sh >/dev/null 2>&1; $D/scripts/$B/bin/smcbvs4 version 2>&1 )" > "$STG/.ver.$B" || true
GC=$(grep -o '"git_commit": *"[^"]*"' "$STG/.ver.$B" | head -1 | grep -o '"[^"]*"$' | tr -d '"'); ISA=$(grep -o '"island_isa": *"[^"]*"' "$STG/.ver.$B" | head -1 | grep -o '"[^"]*"$' | tr -d '"'); LIBM=$(grep -c '"pass": *true' "$STG/.ver.$B" || true); rm -f "$STG/.ver.$B"
[[ $GC == "$F2" && $ISA == sapphirerapids && $LIBM -ge 1 ]] || { echo "FATAL: version check failed (git '$GC', isa '$ISA', libm '$LIBM')" >&2; exit 67; }
log_gc "$B" COPYBIN "$SHA" "$GC" "$ISA" "$LIBM" "$(home_mb)"
echo "deploy done (not submitted). Next: submit with ssh $NOTS 'cd $D/scripts/$B && CONFIRM=yes bash submit_t2thr.sh'"
