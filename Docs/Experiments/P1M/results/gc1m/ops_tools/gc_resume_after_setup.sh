#!/usr/bin/env bash
# gc_resume_after_setup.sh -- OPTION B for GC_D (HQ d99c67b4 / manager): the setup 2817052 FINISHED its work (setup.log status completed; setup.bin 9,217,428,672 B and setup.bin.json written 21:34:45Z) but Slurm TIMEOUT-killed the job 1 s later (limit 1:45) and
# cancelled the dependants. This resumes the SAME batch GC_D on its own run dir: calibrate -> islands -> merge -> eval, with the SAME stage scripts and the SAME dependency graph as submit.sh minus the setup stage, and the HQ limits passed as
# sbatch command-line overrides (no script, plan or code change): calibrate 2:00 (unchanged), islands 2:30 / 80G, merge 3:00, eval 1:00. The lost setup stays in D's ledger (84.09 core-h, sacct).
#   bash gc_resume_after_setup.sh            = DRY RUN (default): checks the run dir and prints the exact sbatch commands; runs `sbatch --test-only` (validation only, NO job is created) on NOTS
#   GO=yes CONFIRM=B bash gc_resume_after_setup.sh = submits (only on the manager's ruling "B")
set -euo pipefail; . "$(dirname "$0")/common.sh"
B=GC_D; RID=6-AR-n1000-r01-V-s1; RUN=$D/scratch/runs/$B/$RID; S=$D/scripts/$B
CAL_T=02:00:00; ISL_T=02:30:00; ISL_MEM=80G; MER_T=03:00:00; EVA_T=01:00:00
SUBMIT=0; [[ ${GO:-} == yes && ${CONFIRM:-} == B ]] && SUBMIT=1
echo "== option B for $B ($( [[ $SUBMIT == 1 ]] && echo SUBMIT || echo "DRY RUN: nothing is submitted" ))"
ssh $NOTS "set -u; fail=0
cd $S && sha256sum --quiet -c SHA256SUMS && echo 'scripts/$B SHA256SUMS ok' || { echo 'scripts SHA256SUMS BAD'; fail=1; }
sh=\$(sha256sum $S/bin/smcbvs4 | cut -d' ' -f1); [[ \$sh == $(f2_sha) ]] && echo 'bin sha256 == BUILD_F2' || { echo 'bin sha256 != BUILD_F2'; fail=1; }
st=\$(python3 -c \"import json;print(json.load(open('$RUN/setup.bin.json')).get('status'))\" 2>/dev/null); echo \"setup.bin.json status: \$st\"; [[ \$st == completed ]] || fail=1
python3 - <<PY || fail=1
import json
j = json.load(open('$RUN/setup.bin.json')); b = j.get('binary', {})
print('setup.bin.json binary.sha256 == BUILD_F2:', b.get('sha256') == '$(f2_sha)', '| git', str(b.get('git_commit'))[:8], '| J', j.get('J'), 'C', j.get('C'), 'B', j.get('B'))
assert b.get('sha256') == '$(f2_sha)'
PY
ls -l --time-style=+%FT%TZ $RUN/setup.bin $RUN/data.bin | awk '{print \$5, \$6, \$7}'
for f in calib.bin island_1.bin fit.bin eval.bin OUTCOME; do [[ -e $RUN/\$f ]] && { echo \"UNEXPECTED $RUN/\$f exists\"; fail=1; }; done
echo \"my queue now: \$(squeue -u fb31 -h | wc -l) jobs\"; [[ \$(squeue -u fb31 -h | wc -l) -eq 0 ]] || fail=1
hm=\$(quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'); echo \"home MB used: \$hm (refuse above $HOME_LIMIT_MB)\"; [[ \$hm -le $HOME_LIMIT_MB ]] || fail=1
exit \$fail" || { echo "PRECHECK FAILED: not submitting" >&2; exit 1; }
CMD_C="sbatch --parsable --array=1-1 --time=$CAL_T stage_calibrate.sbatch"
CMD_I="sbatch --parsable --array=1-16%16 --time=$ISL_T --mem=$ISL_MEM --dependency=afterok:\${JC}_1 stage_islands.sbatch 1"
CMD_M="sbatch --parsable --time=$MER_T --dependency=afterok:\${JI} stage_merge.sbatch 1"
CMD_E="sbatch --parsable --time=$EVA_T --dependency=afterok:\${JM} stage_eval.sbatch 1"
echo "-- the exact commands (cd $S; the dependency ids are filled in at submission):"; printf '   %s\n' "$CMD_C" "$CMD_I" "$CMD_M" "$CMD_E"
echo "-- sbatch --test-only (validates script + options, creates NO job; the dependent stages are tested without their dependency):"
ssh $NOTS "cd $S && for c in 'stage_calibrate.sbatch --array=1-1 --time=$CAL_T' 'stage_islands.sbatch --array=1-16%16 --time=$ISL_T --mem=$ISL_MEM' 'stage_merge.sbatch --time=$MER_T' 'stage_eval.sbatch --time=$EVA_T'; do set -- \$c; f=\$1; shift; echo \"== \$f \$*\"; sbatch --test-only \"\$@\" \$f $( : ) 1 2>&1 | head -2; done"
[[ $SUBMIT == 1 ]] || { echo "DRY RUN done: nothing was submitted. Submit with: GO=yes CONFIRM=B bash tools/gc_resume_after_setup.sh"; exit 0; }
ssh $NOTS "set -euo pipefail; cd $S; LOG=$D/scratch/runs/$B/submissions.jsonl
log() { printf '{\"stage\":\"%s\",\"fit\":\"%s\",\"job\":\"%s\",\"submitted_utc\":\"%s\"}\n' \"\$1\" \"\$2\" \"\$3\" \"\$(date -u +%FT%TZ)\" | tee -a \"\$LOG\"; }
echo '{\"note\":\"option B resume after the setup 2817052 TIMEOUT: calibrate/islands/merge/eval resubmitted on the same run dir, limits as sbatch overrides\",\"utc\":\"'\$(date -u +%FT%TZ)'\"}' >> $D/scratch/runs/$B/RESUME_B_NOTE.jsonl
JC=\$($CMD_C); log calibrate all \"\$JC\"
JI=\$(sbatch --parsable --array=1-16%16 --time=$ISL_T --mem=$ISL_MEM --dependency=afterok:\${JC}_1 stage_islands.sbatch 1); log islands $RID \"\$JI\"
JM=\$(sbatch --parsable --time=$MER_T --dependency=afterok:\${JI} stage_merge.sbatch 1); log merge $RID \"\$JM\"
JE=\$(sbatch --parsable --time=$EVA_T --dependency=afterok:\${JM} stage_eval.sbatch 1); log eval $RID \"\$JE\"
echo submitted-B"
