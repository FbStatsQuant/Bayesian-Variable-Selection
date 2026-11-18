#!/usr/bin/env bash
# freeze_check_stage.sh <F40> <FREEZE_WT> [submit] -- stage the NOTS freeze check (freeze_check_1e5.sh from the freeze branch).
#   <FREEZE_WT>  Owls worktree of F (holds Scripts/SMC_BVS/engine_v4/tools/slurm/freeze_check_1e5.sh)
# WITHOUT `submit`: restore the T5 inputs, deploy the script + clone, build the freeze binary on the login node (nice, -j3).
# WITH `submit` (needs GO=yes): sbatch the one job (48 CPUs, 16G, 30 min limit, worst 24 core-h, expected ~2.1).
# The T5 inputs were OFFLOADED and freed from NOTS on 11-18 (scratch/runs/T5_1e5/<run>/OFFLOADED_group{1,2,3}.txt, scripts/T5_1e5/manifests gone):
# they are restored from the verified Owls copies (records/hygiene_1117/group2|3) and re-checked against the hashes computed on NOTS.
set -euo pipefail; . "$(dirname "$0")/common.sh"
F=${1:?F}; need_full_sha "$F"; WT=${2:?FREEZE_WT}; MODE=${3:-}
R=5-AR-n200-r01-V-s1; H=$D/records/hygiene_1117
FC=$D/scripts/FREEZE_CHECK_1e5; CN=$D/scratch/overlap1e4/clone_${F:0:8}
SCRIPT=$WT/Scripts/SMC_BVS/engine_v4/tools/slurm/freeze_check_1e5.sh
if [[ $MODE == submit ]]; then
  [[ ${GO:-} == yes ]] || { echo "refusing: GO=yes not set" >&2; exit 64; }
  ssh $NOTS "cd $FC && sbatch --parsable freeze_check_1e5.sh run"; exit 0
fi
[[ -f $SCRIPT ]] || { echo "no $SCRIPT: the freeze branch does not carry freeze_check_1e5.sh yet" >&2; exit 2; }
[[ $(git -C "$WT" rev-parse HEAD) == "$F" ]] || echo "WARNING: worktree HEAD is not F" >&2
# 1. the T5 inputs (sizes: data 164 MB, setup 1.0 GB, calib 784 MB, island_1 221 MB = 2.2 GB, one stream, nice)
RUNDIR=$D/scratch/runs/T5_1e5/$R
ssh $NOTS "mkdir -p $RUNDIR $D/scripts/T5_1e5/manifests/$R $FC $D/scratch/runs/FREEZE_CHECK_1e5"
for f in data.bin data.bin.json setup.bin setup.bin.json calib.bin calib.bin.json island_1.bin island_1.bin.json; do
  rs $H/group3/runs/T5_1e5/$R/$f $NOTS:$RUNDIR/$f
done
( cd $H/group3 && grep -E "runs/T5_1e5/$R/(data|setup|calib|island_1)\.bin(\.json)?$" SHA256SUMS_group3_nots.txt | sed 's# runs/T5_1e5/# '"$D"'/scratch/runs/T5_1e5/#' ) \
  | ssh $NOTS "sha256sum --quiet -c - && echo 'T5 inputs verified on NOTS against the 11-18 hashes'"
# 2. the T5 scripts the check reads (manifest template + two helpers), from the NOTS copy kept in group2/home
for f in manifests/$R/island.json p1m_manifest.py p1m_stage_cost.py; do rs $H/group2/home/T5_1e5/$f $NOTS:$D/scripts/T5_1e5/$f; done
( cd $H/group2 && grep -E "home/T5_1e5/(manifests/$R/island\.json|p1m_manifest\.py|p1m_stage_cost\.py)$" SHA256SUMS_group2_nots.txt | sed 's# home/T5_1e5/# '"$D"'/scripts/T5_1e5/#' ) \
  | ssh $NOTS "sha256sum --quiet -c - && echo 'T5 scripts verified on NOTS'"
# 3. the freeze-check script + the clone, then the build (login node, nice, -j3; no core-h)
rs "$SCRIPT" $NOTS:$FC/freeze_check_1e5.sh
rs "$STG/clone_${F:0:8}"/ $NOTS:$CN/
ssh $NOTS "cd $FC && CLONE=$CN nice -n 19 bash freeze_check_1e5.sh build $F 2>&1 | tail -n 12"
echo "staged. Submit (manager, GO=yes):  GO=yes $0 $F $WT submit   -> read $D/scratch/runs/FREEZE_CHECK_1e5/freeze_check.json (verdict PASS|FAIL)"
