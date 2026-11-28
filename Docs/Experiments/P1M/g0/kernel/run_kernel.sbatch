#!/usr/bin/env bash
# run_kernel.sbatch -- P1M gate G0, Part K: kernel benchmark on ONE Sapphire Rapids node (array of one task).
# Builds g0_bench on the compute node (GCC 14.3.0, -march=sapphirerapids, -ffp-contract=off), records the node, then runs
#   g0_bench suite 1000000 1,48,96,24 200000 0.1 40000000 4
# i.e. at p = 10^6 and T = 1, 48, 96, 24 threads: batch class A (v2) and bit form (v0) for 256 distinct supports and for
# S0 alone, direct, perm, bw; bit checks at T = 1 on small samples; pass fractions; store offers at c = 4e7.
# 96 CPUs = 48 cores x 2 hardware threads (NOTS bills per hardware thread): T = 48 is one thread per core, T = 96 uses
# both hyperthreads. Measured on Owls at p = 1e6 (T <= 4): 76 s; expected here about 2 min with the build.
# Worst-case admission: 96 CPUs x 5 min = 8.0 billed core-h.
#SBATCH --job-name=p1m_g0_kernel
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --qos=nots_commons
#SBATCH --array=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=96
#SBATCH --mem=32G
#SBATCH --time=00:05:00
#SBATCH --constraint=sapphirerapids
#SBATCH --export=NONE
#SBATCH --no-requeue
#SBATCH --output=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A_%a.out
#SBATCH --error=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A_%a.err
set -euo pipefail
DEPT=/home/fb31/SMC_Engineering_Department
SCR=$DEPT/scripts/g0/kernel
RUN=$DEPT/scratch/runs/g0/kernel_${SLURM_ARRAY_JOB_ID}
BUILD=$DEPT/scratch/runs/g0/build/kernel_${SLURM_ARRAY_JOB_ID}
export TMPDIR=$DEPT/scratch/tmp/$SLURM_JOB_ID
mkdir -p "$RUN" "$BUILD" "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
LOG=$RUN/kernel.log
{
  echo "# P1M G0 kernel job ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID} (job ${SLURM_JOB_ID})"
  date; date -u +%FT%TZ; echo "node: $(hostname)"
  echo "SLURM_CPUS_PER_TASK=${SLURM_CPUS_PER_TASK:-} SLURM_MEM_PER_NODE=${SLURM_MEM_PER_NODE:-} SLURM_JOB_CPUS_PER_NODE=${SLURM_JOB_CPUS_PER_NODE:-}"
  grep -E "Cpus_allowed_list|Mems_allowed_list" /proc/self/status
  echo "nproc=$(nproc)"
  echo "---- lscpu"; lscpu
  echo "---- numactl -H"; (numactl -H 2>/dev/null || echo "numactl not available")
  echo "---- scripts (sha256)"; ( cd "$SCR" && sha256sum g0_bench.cpp build.sh run_kernel.sbatch core_copy/v3_score.h core_copy/v3_util.h )
  echo "---- build"
} > "$LOG" 2>&1
bash "$SCR/build.sh" nots "$BUILD" >> "$LOG" 2>&1
export OMP_PLACES=cores OMP_PROC_BIND=spread OMP_DYNAMIC=false
TIMEV=(); [[ -x /usr/bin/time ]] && TIMEV=(/usr/bin/time -v)
{
  echo "---- run: OMP_PLACES=$OMP_PLACES OMP_PROC_BIND=$OMP_PROC_BIND; g0_bench suite 1000000 1,48,96,24 200000 0.1 40000000 4"
  rc=0; "${TIMEV[@]}" timeout 240 "$BUILD/g0_bench" suite 1000000 1,48,96,24 200000 0.1 40000000 4 || rc=$?
  echo "---- exit code $rc (124 = stopped by the 240 s in-job timeout)"
  date; date -u +%FT%TZ
} >> "$LOG" 2>&1
cp "$BUILD/build_info.txt" "$RUN/"
