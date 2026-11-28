#!/usr/bin/env bash
# freeze_check_1e5.sh -- the NOTS part of the campaign-freeze reproduction check (CAMPAIGN_PLAN_1117 §3, H-14): ONE 10⁵ island
# of the T5 fit, re-run with the FREEZE binary on the T5 inputs, must reproduce the T5 island's output hash and every non-meta
# section (optionally also the pilot-code binary, 2cfaa9e5, on the same inputs). Expected cost ≈ 2 core-h (one island, 48 CPUs,
# 1:52-2:33 in T5; the build runs on the login node, not billed). READY TO SUBMIT, NOT SUBMITTED: the manager submits after HQ's GO.
#
#   login node, once (builds the freeze binary and, if PILOT_COMMIT is set, the pilot-code binary; no job, no core-h):
#       CLONE=<clone of the repo on NOTS> bash freeze_check_1e5.sh build <ENGINE_FREEZE_COMMIT> [PILOT_COMMIT=2cfaa9e5...]
#   the job (the only billed step):
#       sbatch freeze_check_1e5.sh run
#   then read $DEPT/scratch/runs/FREEZE_CHECK_1e5/freeze_check.json (verdict PASS/FAIL, exit 0/1).
#
# Inputs it needs (they exist after the T5 gate, 11-17): $DEPT/scratch/runs/T5_1e5/5-AR-n200-r01-V-s1/{data,setup,calib}.bin,
# island_1.bin, and $DEPT/scripts/T5_1e5/{manifests/5-AR-n200-r01-V-s1/island.json,p1m_manifest.py,p1m_stage_cost.py}.
# If island_1.bin was purged, the check falls back to the literal T5 hash (c4fb97717604869d) only.
# What it proves: the freeze binary makes the same class-A island bits (sapphirerapids) as the T5/pilot-era code on the same
# inputs. It does NOT redo setup/calibrate (that would be ≈ 12 core-h more); calibration code is covered by the Owls golden suite.
#SBATCH --job-name=p1m_freeze_check_1e5
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --qos=nots_commons
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --constraint=sapphirerapids
#SBATCH --export=NONE
#SBATCH --no-requeue
#SBATCH --output=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A.out
#SBATCH --error=/home/fb31/SMC_Engineering_Department/scratch/slurm_out/%x_%A.err
# worst case: 48 CPUs x 0.5 h = 24 billed core-h (limit); expected ≈ 2 (one island) + ≈ 0.1 (info) = ≈ 2.1; with PILOT_COMMIT built ≈ 4.2.
set -euo pipefail

DEPT_ROOT=/home/fb31/SMC_Engineering_Department       # the department folder on NOTS (as the driver's --dept default)
DEPT=$(realpath -m "${P1M_DEPT:-$DEPT_ROOT}")
case "$DEPT" in "$DEPT_ROOT"|"$DEPT_ROOT"/*) ;; *) echo "refusing: $DEPT is outside the department folder" >&2; exit 64;; esac
FC=$DEPT/scripts/FREEZE_CHECK_1e5
T5S=$DEPT/scripts/T5_1e5
RUN_ID=5-AR-n200-r01-V-s1
T5RUN=$DEPT/scratch/runs/T5_1e5/$RUN_ID
OUT=$DEPT/scratch/runs/FREEZE_CHECK_1e5
T5_ISLAND1_HASH=c4fb97717604869d            # T5_1e5.md, "D-32 cross-ISA": island 1, sapphirerapids = x86-64-v3, 26 sections
CORE_TREE=61b0a5822019b2737fe415ff15625e410f3227b2      # method-v3.1.1-listpip, Scripts/SMC_BVS/core
CORE_PATH=Scripts/SMC_BVS/core

load_env() {   # the NOTS modules, as the driver's env.sh (errexit/nounset/pipefail off while Lmod runs)
  [[ -z ${P1M_SKIP_MODULES:-} ]] || return 0      # tests on a machine without the NOTS modules only
  local f=$- pf; pf=$(shopt -po pipefail); set +e +u +o pipefail
  type module >/dev/null 2>&1 || source /etc/profile.d/modules.sh
  module use /opt/apps/modules/Core; module purge; module load GCC/14.3.0 CMake/3.31.8
  [[ $f == *e* ]] && set -e; [[ $f == *u* ]] && set -u; eval "$pf"
  command -v g++ >/dev/null && [[ $(g++ -dumpfullversion) == 14.3.0 ]] || { echo "FATAL: GCC 14.3.0 not loaded" >&2; exit 66; }
}

build_one() {   # build_one <commit> <name>: git archive -> $FC/code_<name> -> $FC/bin/smcbvs4_<name>   (sapphirerapids)
  local commit=$1 name=$2 src=$FC/code_$2 b=$FC/build_$2
  [[ -d ${CLONE:-} ]] || { echo "set CLONE to a git clone of the repository on NOTS" >&2; exit 2; }
  local tree; tree=$(git -C "$CLONE" rev-parse --verify "$commit:$CORE_PATH")
  if [[ $name == freeze ]]; then   # the freeze commit must carry the pinned method; the pilot-era commit (2cfaa9e5) predates v3.1.1 and need not
    [[ $tree == "$CORE_TREE" ]] || { echo "FATAL: $commit has core tree $tree, the freeze pins $CORE_TREE" >&2; exit 3; }
  fi
  rm -rf "$src"; mkdir -p "$src" "$b" "$FC/bin"
  git -C "$CLONE" archive "$commit" | tar -x -C "$src"
  nice -n 19 cmake -S "$src/Scripts/SMC_BVS/engine_v4" -B "$b" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF -DV4_ISLAND_ISA=sapphirerapids > "$b/cmake.log"
  nice -n 19 make -C "$b" -j3 smcbvs4
  cp "$b/smcbvs4" "$FC/bin/smcbvs4_$name"
  "$FC/bin/smcbvs4_$name" version | tee "$FC/bin/smcbvs4_$name.version.json" | grep -E '"island_isa"|"island_fma"|"git_commit"|"pass"'
  sha256sum "$FC/bin/smcbvs4_$name" | tee "$FC/bin/smcbvs4_$name.sha256"
  echo "$commit" > "$FC/bin/smcbvs4_$name.commit"
}

run_island() {   # run_island <name>: island 1 of the T5 fit with $FC/bin/smcbvs4_<name> -> $OUT/island_1_<name>.bin
  local name=$1 bin=$FC/bin/smcbvs4_$1
  python3 "$T5S/p1m_manifest.py" fill --template "$T5S/manifests/$RUN_ID/island.json" --out "$OUT/island_1_$name.manifest.json" \
          --bin "$bin" --set params.id=1
  rm -f "$OUT/island_1_$name".ckpt.{a,b}
  "$bin" island --manifest "$OUT/island_1_$name.manifest.json" --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB" \
         --out "$OUT/island_1_$name.bin" > "$OUT/island_1_$name.log" 2>&1
}

case "${1:-}" in
build)
  commit=${2:?usage: build <ENGINE_FREEZE_COMMIT> [PILOT_COMMIT]}
  load_env
  build_one "$commit" freeze
  if [[ -n ${3:-} ]]; then build_one "$3" pilot; fi
  echo "built: $FC/bin (freeze $commit${3:+, pilot $3}); now: sbatch $0 run"
  ;;
run)
  : "${SLURM_JOB_ID:?run this with sbatch}"
  export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-48}
  MEMB=$(( ${SLURM_MEM_PER_NODE:-0} * 1048576 * 9 / 10 ))
  export TMPDIR=$DEPT/scratch/tmp/$SLURM_JOB_ID; mkdir -p "$TMPDIR" "$OUT"; trap 'rm -rf "$TMPDIR"' EXIT
  load_env
  for f in data.bin setup.bin calib.bin; do [[ -s $T5RUN/$f ]] || { echo "FATAL: missing T5 input $T5RUN/$f" >&2; exit 4; }; done
  [[ -x $FC/bin/smcbvs4_freeze ]] || { echo "FATAL: run 'bash $0 build <commit>' first" >&2; exit 4; }
  names=(freeze); [[ -x $FC/bin/smcbvs4_pilot ]] && names+=(pilot)
  for n in "${names[@]}"; do run_island "$n"; done
  python3 - "$T5RUN" "$OUT" "$FC" "$T5_ISLAND1_HASH" "${names[@]}" <<'PY'
import json, os, subprocess, sys
t5run, out, fc, ref_hash, *names = sys.argv[1:]
binf = os.path.join(fc, "bin", "smcbvs4_freeze")
def info(path):
    rec = path + ".info.json"
    subprocess.run([binf, "info", path, "--meta", "1", "--record", rec], check=True, stdout=subprocess.DEVNULL)
    return json.load(open(rec))
def secs(j):
    return {s["name"]: (s["dtype"], tuple(s["dims"]), s["sha256"]) for s in j.get("sections", []) if s["name"] != "meta"}
norm = lambda h: str(h).lower().replace("0x", "")
t5 = os.path.join(t5run, "island_1.bin")
ref = info(t5) if os.path.exists(t5) else None
rep = {"t5_island_hash_literal": ref_hash, "t5_island_file": bool(ref), "runs": {}}
ok = True
for n in names:
    j = info(os.path.join(out, "island_1_%s.bin" % n)); m = j["meta"]
    r = {"output_hash": m.get("output_hash"), "island_isa": m.get("binary", {}).get("island_isa"), "git_commit": m.get("binary", {}).get("git_commit"),
         "status": m.get("status"), "equals_literal": norm(m.get("output_hash")) == norm(ref_hash)}
    if ref:
        d = sorted(k for k in set(secs(j)) | set(secs(ref)) if secs(j).get(k) != secs(ref).get(k))
        r.update(equals_t5_file=norm(m.get("output_hash")) == norm(ref["meta"].get("output_hash")), differing_sections=d, sections=len(secs(j)))
        r["pass"] = r["equals_literal"] and r["equals_t5_file"] and not d
    else:
        r["pass"] = r["equals_literal"]
    ok = ok and r["pass"]; rep["runs"][n] = r
rep["verdict"] = "PASS" if ok else "FAIL"
json.dump(rep, open(os.path.join(out, "freeze_check.json"), "w"), indent=1)
print(json.dumps(rep, indent=1)); sys.exit(0 if ok else 1)
PY
  ;;
*) echo "usage: bash $0 build <ENGINE_FREEZE_COMMIT> [PILOT_COMMIT]   |   sbatch $0 run" >&2; exit 2;;
esac
