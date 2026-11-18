#!/usr/bin/env bash
# stage_F.sh <F40> [<branch-ref>] -- once the freeze lands: worktree of F, shallow clone, W0 plans + driver dry runs, repoint `current`.
# Run in ~ minutes after `git fetch origin` shows the freeze commit. Owls only; touches nothing on NOTS; never submits.
set -euo pipefail; . "$(dirname "$0")/common.sh"
F=${1:?F}; need_full_sha "$F"; E=${F:0:8}; REPO=/home/fb31/Bayesian-Variable-Selection
git -C $REPO fetch -q origin; git -C $REPO fetch -q --tags origin
[[ -d $STG/wt_$E ]] || git -C $REPO worktree add --detach $STG/wt_$E $F
$STG/tools/mk_clone.sh $F
python3 $STG/tools/make_waves.py --wt $STG/wt_$E --code-commit $F --out $STG/F_$E --waves W0
ln -sfn $STG/wt_$E $STG/F_$E/wt; ln -sfn $STG/F_$E $STG/current
echo "current -> F_$E. Next: freeze_check_stage.sh $F $STG/wt_$E ; deploy_wave.sh W0 $F $STG/F_$E/scripts $STG/clone_$E build"
