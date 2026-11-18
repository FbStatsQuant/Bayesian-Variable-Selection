#!/usr/bin/env bash
# deploy_wave.sh <WAVE> <F40> <SCRIPTS_SRC> <CLONE_LOCAL> [build]  -- Owls -> NOTS: deploy + (optionally) build. NEVER submits.
#   WAVE          W0 | W1 ...      (batches OV_<WAVE>_T and OV_<WAVE>_V; the driver's batch id is flat, '/' is refused by safe_id)
#   SCRIPTS_SRC   the dir make_waves.py wrote (contains OV_<WAVE>_T/ and OV_<WAVE>_V/ with their SHA256SUMS)
#   CLONE_LOCAL   from mk_clone.sh
# Steps (each one fails loudly): local SHA256SUMS ok and plan.code_commit == F -> mkdir on NOTS -> rsync the driver files
# -> `sha256sum -c` ON NOTS -> shallow clone to NOTS scratch (once) -> git archive F into scripts/<batch>/code -> [build].
# The build is on the LOGIN node, nice -n 19, make -j3 (generated build.sh): V with -DV4_ISLAND_ISA=sapphirerapids, T default.
# Home stays small (guard: refuses above 7,500 MB): scripts + build dirs only (~15 MB per batch). The code tree (git archive, ~360 MB)
# goes to SCRATCH  <scratch>/code_ws/<batch>_code  with the symlink scripts/<batch>/code -> it; the clone (150 MB) and all run data too.
# Refuses a batch that was already submitted (scratch/runs/<batch>/submissions.jsonl exists): never redeploys over a running wave.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; SRC=${3:?SCRIPTS_SRC}; CLONE=${4:?CLONE_LOCAL}; DO_BUILD=${5:-}
need_full_sha "$F"; [[ $WAVE =~ ^W[0-9]$ ]] || { echo "bad wave" >&2; exit 64; }
CN=$D/scratch/overlap1e4/clone_${F:0:8}
for arm in T V; do
  B=OV_${WAVE}_$arm
  (cd "$SRC/$B" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS differ in $B" >&2; exit 66; }
  python3 - "$SRC/$B/plan.resolved.json" "$F" "$B" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
assert p["code_commit"] == sys.argv[2], "plan code_commit %s != F %s" % (p["code_commit"], sys.argv[2])
assert p["batch"] == sys.argv[3] and p.get("warnings") in (None, []), p.get("warnings")
print(p["batch"], "OK: code_commit == F; worst", p["worst_case_core_h"], "core-h; fits", len(p["fits"]))
PY
done
home_guard
for arm in T V; do
  ssh $NOTS "[[ ! -e $D/scratch/runs/OV_${WAVE}_$arm/submissions.jsonl ]]" || { echo "REFUSING: OV_${WAVE}_$arm was already submitted" >&2; exit 65; }
done
ssh $NOTS "mkdir -p $D/scratch/overlap1e4 $D/scratch/runs/OV_${WAVE}_T $D/scratch/runs/OV_${WAVE}_V $D/scripts/OV_${WAVE}_T $D/scripts/OV_${WAVE}_V"
rs "$CLONE"/ $NOTS:$CN/
ssh $NOTS "set -e; [[ \$(git -C $CN rev-parse $F:$CORE_PATH) == $CORE_TREE ]] && echo 'clone ok: core tree = pin'"
for arm in T V; do
  B=OV_${WAVE}_$arm
  rs --exclude code --exclude bin --exclude build "$SRC/$B"/ $NOTS:$D/scripts/$B/
  ssh $NOTS "cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS' \
             && CW=\$(readlink -f $D/scratch)/$CODE_WS_REL/${B}_code && mkdir -p \$(dirname \$CW) && rm -rf code \$CW && mkdir \$CW && ln -s \$CW code \
             && git -C $CN archive $F | tar -x -C code && echo \"$B: code = git archive $F in \$CW (symlinked)\""
done
if [[ $DO_BUILD == build ]]; then
  home_guard
  for arm in V T; do   # one build at a time, login node, nice, -j3 (in build.sh); V = sapphirerapids island ISA, T = default
    B=OV_${WAVE}_$arm
    ssh $NOTS "cd $D/scripts/$B && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 6 build_stdout.log; \
               [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
  done
  # the binary needs the batch's module environment (GCC 14.3.0 libstdc++, CXXABI_1.3.15): source env.sh in a subshell, as the stages do
  ssh $NOTS "for b in OV_${WAVE}_T OV_${WAVE}_V; do echo \$b; ( set +u; source $D/scripts/\$b/env.sh; $D/scripts/\$b/bin/smcbvs4 version 2>&1 | tr -d '\n ' | cut -c1-400 ); echo; done"
  home_guard
fi
echo "deploy done (not submitted). Next: presubmit_check.sh $WAVE"
