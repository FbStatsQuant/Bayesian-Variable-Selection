#!/usr/bin/env bash
# Slurm validation ONLY. sbatch owns persistence; no SSH, arrays or production.
set -euo pipefail
[[ $# == 3 ]] || exit 64
SNAPSHOT=$(realpath "$1"); OUT=$(realpath "$2"); RECEIPT=$(realpath "$3")
CODE=/projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022/code
SCRATCH=/scratch/fb31/smcbvs_v3_deploy_20261022/A_build
[[ "$SNAPSHOT" == "$CODE"/snapshots/v* && "$OUT" == "$SCRATCH"/* && "$RECEIPT" == "$CODE"/validation/* ]] || exit 65
[[ $(basename "$SNAPSHOT") != v1 ]] || exit 65
[[ ${SLURM_JOB_ID:-} =~ ^[0-9]+$ && ${SLURM_CPUS_PER_TASK:-} == 1 && -z ${SLURM_ARRAY_TASK_ID:-} ]] || exit 65
# Before module loading, compilation, logging or working-copy creation: re-read
# every reviewed instruction, including absent candidates. Changes fail closed.
python3 -B - "$OUT/remote_agents.json" <<'PY'
import hashlib, json, pathlib, sys
for row in json.loads(pathlib.Path(sys.argv[1]).read_text()):
    p = pathlib.Path(row['path'])
    if row.get('absent'):
        if p.exists(): raise SystemExit('New remote AGENTS; re-observe before work: '+str(p))
    elif not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        raise SystemExit('Changed remote AGENTS; re-observe before work: '+str(p))
PY
exec > "$OUT/job.log" 2>&1
finish() {
  rc=$?
  trap - EXIT
  set +e
  if (( rc )); then rm -f -- "$OUT/VALIDATION_PASS.json"; fi
  printf '%s\n' "$rc" > "$OUT/exit_status.txt"
  date -u +%FT%TZ > "$OUT/finished_utc.txt"
  printf '%s\n' "$rc" > "$RECEIPT/job_exit_status.txt"
  # Always revalidate frozen source, even after a failing build/test.
  python3 -B - "$SNAPSHOT" "$OUT/launch.json" <<'PY'
import hashlib, json, pathlib, sys
r=pathlib.Path(sys.argv[1]); config_path=pathlib.Path(sys.argv[2]); c=json.loads(config_path.read_text())
roots=[r]
if (config_path.parent/'work').is_dir(): roots.append(config_path.parent/'work')
for root in roots:
    for name, key in [('manifest.json','manifest_sha256'), ('SHA256SUMS','inventory_sha256')]:
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != c[key]:
            raise SystemExit('Pinned source identity changed: '+str(root/name))
PY
  pin_rc=$?
  if ! (cd "$SNAPSHOT" && sha256sum --strict -c SHA256SUMS) > "$OUT/source_validation_final.log" 2>&1; then pin_rc=1; fi
  if [[ -d "$OUT/work" ]]; then
    if ! (cd "$OUT/work" && sha256sum --strict -c SHA256SUMS) > "$OUT/work_validation_final.log" 2>&1; then pin_rc=1; fi
  fi
  if (( pin_rc )); then
    rc=1
    printf '%s\n' "$rc" > "$OUT/exit_status.txt"
    printf '%s\n' "$rc" > "$RECEIPT/job_exit_status.txt"
    rm -f -- "$OUT/VALIDATION_PASS.json"
  fi
  # Close the job log before hashing. Slurm streams remain mutable until job end.
  exec 1>&- 2>&-
  python3 -B - "$OUT" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
excluded = {'output_sha256.json'}
files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(root.rglob('*')) if p.is_file() and p.name not in excluded
         and not p.name.startswith('slurm-')}
(root/'output_sha256.json').write_text(json.dumps({'files':files,
    'excluded':['output_sha256.json', 'slurm-* (hash after scheduler completion)']}, indent=2)+'\n')
PY
  audit_rc=$?
  if (( audit_rc )); then
    rc=1
    printf '%s\n' "$rc" > "$OUT/exit_status.txt"
    printf '%s\n' "$rc" > "$RECEIPT/job_exit_status.txt"
    rm -f -- "$OUT/VALIDATION_PASS.json"
  fi
  exit "$rc"
}
trap finish EXIT
date -u +%FT%TZ > "$OUT/started_utc.txt"
printf '%s\n' "$$" > "$OUT/process_id.txt"
printf '%s\n' "$SLURM_JOB_ID" > "$OUT/job_id.txt"
printf '%q ' "$0" "$@" > "$OUT/launch_command.txt"
printf '\n' >> "$OUT/launch_command.txt"
python3 -B - "$OUT/launch.json" > "$OUT/settings.sh" <<'PY'
import json, shlex, sys
c=json.load(open(sys.argv[1]))
for key in ('module_init','r_library'):
    print(key.upper()+'='+shlex.quote(c[key]))
PY
source "$OUT/settings.sh"
python3 -B - "$OUT/launch.json" <<'PY'
import json, os, sys
c=json.load(open(sys.argv[1]))
if os.environ.get('SLURM_CLUSTER_NAME') != c['cluster']:
    raise SystemExit('Wrong Slurm cluster: '+str(os.environ.get('SLURM_CLUSTER_NAME')))
PY
[[ -r "$MODULE_INIT" && -d "$R_LIBRARY" ]] || { echo 'Explicit module-init/package library missing'; exit 66; }
source "$MODULE_INIT"
type module
module purge
module load GCC/14.3.0 R/4.5.2
module -t list > "$OUT/modules.txt" 2>&1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 FLEXIBLAS_NUM_THREADS=1 MAKEFLAGS=-j1
export R_LIBS_USER="$R_LIBRARY" R_LIBS_SITE=/nonexistent
export SLURM_EXPORT_ENV=ALL
# Never reuse an Owls/user/site compiler cache or user Makevars for the probe.
unset R_MAKEVARS_USER R_MAKEVARS_SITE PKG_CPPFLAGS PKG_CXXFLAGS R_LIBS
export TMPDIR="$OUT/tmp"
mkdir "$TMPDIR"
{
  hostname -f; date -u; uname -a; lscpu
  module -t list; command -v R Rscript gcc g++ python3
  gcc --version; g++ --version; R --version; Rscript --version; python3 --version
  ulimit -a; cat /proc/self/limits
  env | sort | grep -E '^(SLURM_|LOADEDMODULES=|MODULEPATH=|PATH=|LD_LIBRARY_PATH=|R_|OMP_|OPENBLAS_|MKL_|BLIS_|FLEXIBLAS_|MAKEFLAGS=|TMPDIR=)'
} > "$OUT/environment.txt" 2>&1
[[ $(gcc -dumpfullversion) == 14.3.0 && $(g++ -dumpfullversion) == 14.3.0 ]] || exit 67
for language in CXX CXX11 CXX14 CXX17 CXX20; do
  compiler_text=$(R CMD config "$language")
  printf '%s=%s\n' "$language" "$compiler_text" >> "$OUT/R_compilers.txt"
  # Compiler configuration is a command plus flags; reject shell syntax/wrappers.
  read -r -a compiler <<< "$compiler_text"
  [[ ${compiler[0]} == g++ || ${compiler[0]} == /*/g++ ]] || { echo 'Unexpected R compiler'; exit 67; }
  [[ $("${compiler[@]}" -dumpfullversion) == 14.3.0 ]] || exit 67
done
(cd "$SNAPSHOT" && sha256sum --strict -c SHA256SUMS) > "$OUT/source_validation_initial.log"
# v3.R's sourceCpp cache writes under the core, so compile ONLY this private copy.
cp -R "$SNAPSHOT" "$OUT/work"
chmod -R u+rwX "$OUT/work"
WORK="$OUT/work"
cd "$WORK"
/usr/bin/time -v -o "$OUT/build.time.txt" Rscript --vanilla build/nots_build.R "$WORK" "$OUT" "$OUT/launch.json" "$R_LIBRARY"
[[ -s "$OUT/TOOLCHAIN_PASS.json" ]] || exit 67
/usr/bin/time -v -o "$OUT/regression.time.txt" bash build/nots_regression.sh "$SNAPSHOT" "$OUT"
# This marker means toolchain/build/regression only. It is never production GO.
python3 -B - "$OUT" <<'PY'
import json, pathlib, sys
from datetime import datetime, timezone
r=pathlib.Path(sys.argv[1]); s=json.loads((r/'tests/SUITE_SUMMARY.json').read_text())
assert s['complete'] and s['ok'] and len(s['rows']) == 32
assert all(x['ok'] for x in s['rows'])
c=json.loads((r/'launch.json').read_text())
(r/'VALIDATION_PASS.json').write_text(json.dumps(dict(
    status='build_and_prototype_regression_pass', production_go=False,
    snapshot=c['tag'], manifest_sha256=c['manifest_sha256'],
    inventory_sha256=c['inventory_sha256'], GCC='14.3.0', R='4.5.2',
    job_id=__import__('os').environ['SLURM_JOB_ID'],
    finished_utc=datetime.now(timezone.utc).isoformat()), indent=2)+'\n')
PY
