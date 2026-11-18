#!/usr/bin/env bash
# deploy_wave.sh <WAVE> <F40> <SCRIPTS_SRC> <CLONE_LOCAL> [build]  -- Owls -> NOTS: deploy + (optionally) build. NEVER submits.
#   ARMS="T2 V2" (env) selects the batches OV_<WAVE>_<arm>; default "T V".  Batch ids are flat (driver safe_id refuses '/').
# Steps (each fails loudly): local SHA256SUMS ok and plan.code_commit == F -> home guard (<= 7,500 MB) -> refuse an already submitted batch
# -> mkdir on NOTS -> shallow clone of F to NOTS scratch (once) -> rsync the driver files -> `sha256sum -c` ON NOTS
# -> per-batch git WORKTREE of the clone at F: <scratch>/code_ws/<batch>_code (detached, HEAD == F, clean), scripts/<batch>/code -> it
# -> [build] login node, nice -n 19, make -j3 (generated build.sh); the CMake build dir is $SCR/build in home scripts/<batch>/, OUTSIDE the tree,
#    so the tree stays clean; V: -DV4_ISLAND_ISA=sapphirerapids, T: default -> `version` (env.sh sourced) must show git_commit == F exactly.
# Why a worktree and not `git archive`: v4_git.h embeds `git rev-parse HEAD` (+ -dirty); an archive has no .git -> 'unknown', and theory-mode
# merges refuse it (GUARD-W, provenance.cpp:83-89).
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; SRC=${3:?SCRIPTS_SRC}; CLONE=${4:?CLONE_LOCAL}; DO_BUILD=${5:-}
need_full_sha "$F"; [[ $WAVE =~ ^W[0-9]$ ]] || { echo "bad wave" >&2; exit 64; }
CN=$D/scratch/overlap1e4/clone_${F:0:8}
for arm in $ARMS; do
  B=OV_${WAVE}_$arm
  (cd "$SRC/$B" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS differ in $B" >&2; exit 66; }
  python3 - "$SRC/$B/plan.resolved.json" "$F" "$B" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
assert p["code_commit"] == sys.argv[2], "plan code_commit %s != F %s" % (p["code_commit"], sys.argv[2])
assert p["batch"] == sys.argv[3] and p.get("warnings") in (None, []), p.get("warnings")
print(p["batch"], "OK: code_commit == F; worst", p["worst_case_core_h"], "core-h; cap", p["core_h_cap"], "; fits", len(p["fits"]))
PY
done
home_guard
for arm in $ARMS; do
  ssh $NOTS "[[ ! -e $D/scratch/runs/OV_${WAVE}_$arm/submissions.jsonl ]]" || { echo "REFUSING: OV_${WAVE}_$arm was already submitted" >&2; exit 65; }
  ssh $NOTS "mkdir -p $D/scratch/overlap1e4 $D/scratch/runs/OV_${WAVE}_$arm $D/scripts/OV_${WAVE}_$arm"
done
ssh $NOTS "git -C $CN cat-file -e $F^{commit} 2>/dev/null" && echo "clone on NOTS already holds F" || rs "$CLONE"/ $NOTS:$CN/
ssh $NOTS "set -e; [[ \$(git -C $CN rev-parse $F:$CORE_PATH) == $CORE_TREE ]] && echo 'clone ok: core tree = pin'"
for arm in $ARMS; do
  B=OV_${WAVE}_$arm
  rs --exclude code --exclude bin --exclude build "$SRC/$B"/ $NOTS:$D/scripts/$B/
  ssh $NOTS "set -e; cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS'
    CW=\$(readlink -f $D/scratch)/$CODE_WS_REL/${B}_code; mkdir -p \$(dirname \$CW)
    git -C $CN worktree remove --force \$CW 2>/dev/null || true; rm -rf \$CW code; git -C $CN worktree prune
    git -C $CN worktree add -q --detach \$CW $F; ln -s \$CW code
    [[ \$(git -C \$CW rev-parse HEAD) == $F ]] && [[ -z \$(git -C \$CW status --porcelain --untracked-files=no) ]] && echo \"$B: code = worktree of the clone at $F (clean) in \$CW; code -> it\""
done
if [[ $DO_BUILD == build ]]; then
  home_guard
  for arm in $ARMS; do   # one build at a time (V-type first if both): login node, nice, -j3 (in build.sh)
    B=OV_${WAVE}_$arm
    ssh $NOTS "cd $D/scripts/$B && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 4 build_stdout.log; \
               [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
  done
  # the binary needs the batch's module environment (GCC 14.3.0, CXXABI_1.3.15): env.sh sourced in a subshell. git_commit must be F exactly.
  for arm in $ARMS; do
    B=OV_${WAVE}_$arm
    ssh $NOTS "set -e; ( set +u; source $D/scripts/$B/env.sh; $D/scripts/$B/bin/smcbvs4 version 2>&1 ) > $D/scripts/$B/bin/version.json
      gc=\$(grep -o '\"git_commit\": *\"[^\"]*\"' $D/scripts/$B/bin/version.json | head -1); echo \"$B: version \$gc\"
      [[ \$gc == *'\"$F\"' ]] || { echo \"FATAL: $B git_commit is not $F\" >&2; exit 67; }
      [[ \$(git -C \$(readlink -f $D/scripts/$B/code) status --porcelain --untracked-files=no | wc -l) -eq 0 ]] || { echo 'FATAL: worktree dirty after build' >&2; exit 67; }"
  done
  home_guard
fi
echo "deploy done (not submitted). Next: ARMS=\"$ARMS\" presubmit_check.sh $WAVE $F"
