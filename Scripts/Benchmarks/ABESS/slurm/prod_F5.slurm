#!/usr/bin/env bash
# Production task of F5 (ABESS), c050 copy: 3 datasets of one p at scale C050_SCALE (default c100), or the
# task-th id of C050_IDS (ids separated by ":") if set (see run_task.R for the task map).
# Submitted only by slurm/submit_prod.sh, from the read-only snapshot; time and memory are set
# on the sbatch command line there. Args: <snapshot code dir> <run_id>. Env from submit_prod.sh:
# F5_TREE (code snapshot hash), F5_IMH (input-manifest snapshot hash), F5_LIBH and F5_LIBTREE
# (library manifest and installed-file hashes), F5_ONLY (empty, or one dataset id for the smoke).
#SBATCH --job-name=F5_prod
#SBATCH --partition=commons
#SBATCH --account=commons
#SBATCH --cpus-per-task=1
set -euo pipefail
SNAP=${1:?snapshot code dir}; RID=${2:?run id}
B=/projects/ml75/fb31/BVS/bench20261019
RUN=$(dirname "$SNAP")
# One status directory per scheduler job, so a retry never overwrites an earlier attempt's
# records (Astra prod follow-up, point 7). sacct remains the record for SIGKILL/OOM.
STATUS=$B/logs/prod/F5_ABESS/status/$RID/job_${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:?}}
TASK=${SLURM_ARRAY_TASK_ID:?}
mkdir -p "$STATUS"
date -u +%FT%TZ > "$STATUS/task_${TASK}.started"
trap 'rc=$?; printf "%s exit %s job %s\n" "$(date -u +%FT%TZ)" "$rc" "${SLURM_JOB_ID:-}" > "$STATUS/task_${TASK}.exit"' EXIT
# Refuse to run unless code, input manifests and library are exactly what was submitted.
cd "$SNAP"
sha256sum -c --quiet ../code.sha256 || { echo "code snapshot hash mismatch" >&2; exit 3; }
[[ "$(sha256sum ../code.sha256 | cut -d' ' -f1)" == "${F5_TREE:?}" ]] || { echo "code tree != submitted" >&2; exit 3; }
(cd "$RUN/input_manifests" && sha256sum -c --quiet ../input_manifests.sha256) || { echo "input manifest mismatch" >&2; exit 3; }
[[ "$(sha256sum "$RUN/input_manifests.sha256" | cut -d' ' -f1)" == "${F5_IMH:?}" ]] || { echo "input manifest tree != submitted" >&2; exit 3; }
[[ "$(sha256sum "$B/lib/environment_manifest.txt" | cut -d' ' -f1)" == "${F5_LIBH:?}" ]] || { echo "library manifest changed" >&2; exit 3; }
LIBTREE=$(cd "$B/lib/R452" && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1)
[[ "$LIBTREE" == "${F5_LIBTREE:?}" ]] || { echo "installed library files changed" >&2; exit 3; }
source "$SNAP/slurm/env.sh"
{ hostname; date -u +%FT%TZ; echo "task $TASK scale ${C050_SCALE:-c100} code $F5_TREE manifests $F5_IMH library $LIBTREE"; } >&2
Rscript --vanilla "$SNAP/run_task.R" --task "$TASK" --data-root "$B" --manifest-dir "$RUN/input_manifests" \
  --out-root "$B" --run-id "$RID" --code-root "$SNAP" --status-dir "$STATUS" --scale "${C050_SCALE:-c100}" \
  ${C050_IDS:+--ids "$C050_IDS"} ${F5_ONLY:+--only "$F5_ONLY"}
