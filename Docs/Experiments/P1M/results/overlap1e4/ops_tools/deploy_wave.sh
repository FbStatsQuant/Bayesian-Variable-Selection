#!/usr/bin/env bash
# deploy_wave.sh <WAVE> <F40> <SCRIPTS_SRC> <CLONE_LOCAL> [build]  -- Owls -> NOTS: deploy + (optionally) build. NEVER submits.
#   WAVE          W0 | W1 ...      (batches OV_<WAVE>_T and OV_<WAVE>_V; the driver's batch id is flat, '/' is refused by safe_id)
#   SCRIPTS_SRC   the dir make_waves.py wrote (contains OV_<WAVE>_T/ and OV_<WAVE>_V/ with their SHA256SUMS)
#   CLONE_LOCAL   from mk_clone.sh
# Steps (each one fails loudly): local SHA256SUMS ok and plan.code_commit == F -> mkdir on NOTS -> rsync the driver files
# -> `sha256sum -c` ON NOTS -> shallow clone to NOTS scratch (once) -> git archive F into scripts/<batch>/code -> [build].
# The build is on the LOGIN node, nice -n 19, make -j3 (generated build.sh): V with -DV4_ISLAND_ISA=sapphirerapids, T default.
# Home stays small: only scripts, code (~12 MB per batch) and build dirs; the clone (150 MB) and all run data are in scratch.
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
ssh $NOTS "mkdir -p $D/scratch/overlap1e4 $D/scratch/runs/OV_${WAVE}_T $D/scratch/runs/OV_${WAVE}_V $D/scripts/OV_${WAVE}_T $D/scripts/OV_${WAVE}_V"
rs "$CLONE"/ $NOTS:$CN/
ssh $NOTS "set -e; [[ \$(git -C $CN rev-parse $F:$CORE_PATH) == $CORE_TREE ]] && echo 'clone ok: core tree = pin'"
for arm in T V; do
  B=OV_${WAVE}_$arm
  rs --exclude code --exclude bin --exclude build "$SRC/$B"/ $NOTS:$D/scripts/$B/
  ssh $NOTS "cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS' \
             && rm -rf code && mkdir code && git -C $CN archive $F | tar -x -C code && echo '$B: code = git archive $F'"
done
if [[ $DO_BUILD == build ]]; then
  for arm in V T; do   # one build at a time, login node, nice, -j3 (in build.sh); V = sapphirerapids island ISA, T = default
    B=OV_${WAVE}_$arm
    ssh $NOTS "cd $D/scripts/$B && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 6 build_stdout.log; \
               [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
  done
  ssh $NOTS "for b in OV_${WAVE}_T OV_${WAVE}_V; do echo \$b; $D/scripts/\$b/bin/smcbvs4 version | tr -d '\n ' | cut -c1-400; echo; done"
fi
echo "deploy done (not submitted). Next: presubmit_check.sh $WAVE"
