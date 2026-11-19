#!/usr/bin/env bash
# submit_rescue.sh -- ON NOTS. AR-T2 rescue (HQ e8aab325): the AR calibration escalated to N_final = 40,000; islands 2777597_1..4 were refused
# (manifests carried N = 10^4). Submits for the AR fit ONLY: islands (array 1-4, 24 CPU, 16G, --time 1:30:00) -> merge -> eval, afterok.
# The island / merge fills add params.N=40000 (+ budget.task_seconds=5400 for islands); everything else is the generated template.
# Needs CONFIRM=yes. Never touches OV_W0_T / OV_W0_V or the ADJ-OPP fit.
set -euo pipefail
F=eefcbc4a2ab42fdf52ec1e5d318a956bdd07f463
DEPT=/home/fb31/SMC_Engineering_Department; B=OV_W0_T2; SCR=$DEPT/scripts/$B; RES=$SCR/rescue_AR_N40000
RUN=$DEPT/scratch/runs/$B/4-AR-n200-r01-T-s1; LOG=$DEPT/scratch/runs/$B/submissions.jsonl
[[ ${CONFIRM:-} == yes ]] || { echo "refusing: CONFIRM=yes not set" >&2; exit 64; }
( cd "$RES" && sha256sum --quiet -c SHA256SUMS ) || { echo "FATAL: rescue scripts differ from SHA256SUMS" >&2; exit 66; }
( cd "$SCR" && sha256sum --quiet -c SHA256SUMS ) || { echo "FATAL: batch scripts differ from SHA256SUMS" >&2; exit 66; }
v=$( ( set +u; source "$SCR/env.sh"; "$SCR/bin/smcbvs4" version 2>&1 ) ); gc=$(echo "$v" | grep -o '"git_commit": *"[^"]*"' | head -1)
echo "version: $gc"; [[ $gc == *"\"$F\"" ]] || { echo "FATAL: git_commit is not $F" >&2; exit 67; }
python3 - "$RUN/calib.bin.json" <<'PY'
import json, sys
j = json.load(open(sys.argv[1])); print("calib.bin.json: status", j.get("status"), "N", j.get("N"), "N_final", j.get("N_final"), "git", j.get("binary", {}).get("git_commit", "")[:12])
assert j.get("status") == "completed", "calib.bin is not completed"
PY
[[ ! -e $RUN/OUTCOME ]] || { echo "FATAL: OUTCOME exists in $RUN" >&2; exit 68; }
[[ -z $(squeue -u fb31 -h -n p1m_${B}_islands,p1m_${B}_merge,p1m_${B}_eval -o '%i %T' | grep -E '^2777597|^2777598|^2777599') ]] || { echo "FATAL: old AR jobs still queued" >&2; exit 68; }
[[ ! -e $RUN/manifests.bak_N10000 ]] && cp -a "$RUN/manifests" "$RUN/manifests.bak_N10000" && echo "backup: manifests.bak_N10000"
if [[ ! -d $RUN/refused_islands_2777597 ]]; then mkdir "$RUN/refused_islands_2777597"; cp -a "$RUN"/island_*.bin.json "$RUN"/log/island_*.log "$RUN/refused_islands_2777597/"; echo "backup: refused_islands_2777597"; fi
log() { printf '{"stage":"%s","fit":"%s","job":"%s","submitted_utc":"%s"}\n' "$1" "$2" "$3" "$(date -u +%FT%TZ)" | tee -a "$LOG"; }
cd "$SCR"; FIT=4-AR-n200-r01-T-s1
ji=$(sbatch --parsable --array=1-4 --time=01:30:00 "$RES/stage_islands_rescue.sbatch" 1); log islands_rescue $FIT "$ji"
jm=$(sbatch --parsable --dependency=afterok:$ji "$RES/stage_merge_rescue.sbatch" 1); log merge_rescue $FIT "$jm"
je=$(sbatch --parsable --dependency=afterok:$jm stage_eval.sbatch 1); log eval_rescue $FIT "$je"
echo "rescue submitted: islands $ji merge $jm eval $je; worst case islands 4 x 24 x 1.5 h = 144 + merge 2.7 + eval 4 = 150.7 core-h (expected ~50)"
