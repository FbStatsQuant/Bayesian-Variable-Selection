#!/usr/bin/env bash
# deploy_wave.sh <WAVE> <F40> <SCRIPTS_SRC> <CLONE_LOCAL> <MODE>   -- PRECISION LEG (O-2). Owls -> NOTS. NEVER submits.
#   MODE = build    BUILD the leg's ONE binary in PL_A0_1 (wave A0 only, only while deploy_leg.log has no BUILD line), then COPYBIN the wave's other batches
#          copybin  every later wave: `cp -p` the leg binary from PL_A0_1 into each batch's bin/, verify sha256 == the BUILD line (H-25 (2): no rebuild)
#   BATCHES="PL_P1_1 ..." (env) deploys a subset; default = all batches of the wave found in SCRIPTS_SRC.
# Steps (each fails loudly): local SHA256SUMS ok and plan.code_commit == F -> home guard -> refuse an already submitted batch -> mkdir on NOTS ->
# shallow clone of F (reused: scratch/overlap1e4/clone_<F8>) -> rsync the driver files (no code/bin/build) -> sha256sum -c ON NOTS ->
# [build only] shared worktree code_ws/PL_F<F8>_code (clean, HEAD == F, build dir OUTSIDE the tree) -> build.sh -> `version` (env.sh sourced) git_commit == F exactly
# -> deploy_leg.log line per batch (UTC, batch, MODE, sha256, git_commit, island_isa, libm_pass, home MB, who).
# The leg has ONE arm (V-1M class A, island_isa sapphirerapids); A3 is a runtime `partition` setting of the same binary.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; SRC=${3:?SCRIPTS_SRC}; CLONE=${4:?CLONE_LOCAL}; MODE=${5:?MODE build|copybin}
need_full_sha "$F"; [[ $WAVE =~ ^(A0|P[1-4]|H[1-3]|S[1-9]|S10|FZ)$ ]] || { echo "bad wave" >&2; exit 64; }
[[ $MODE == build || $MODE == copybin ]] || { echo "MODE must be build or copybin" >&2; exit 64; }
BL=${BATCHES:-$(batches_of "$SRC" "$WAVE")}; [[ -n $BL ]] || { echo "no batches PL_${WAVE}_* in $SRC" >&2; exit 64; }
CN=$D/scratch/overlap1e4/clone_${F:0:8}
LEGSHA=$(leg_sha)
if [[ $MODE == build ]]; then
  [[ $WAVE == A0 && $BL == "$MASTER_BATCH "* ]] || { echo "REFUSING: build only in wave A0, first batch $MASTER_BATCH (H-25: ONE build per arm for the whole leg)" >&2; exit 65; }
  [[ -z $LEGSHA ]] || { echo "REFUSING: the leg already has its build ($LEGSHA, $LEG_LOG): H-25 forbids a second one" >&2; exit 65; }
else
  [[ -n $LEGSHA ]] || { echo "REFUSING: no BUILD line in $LEG_LOG yet (deploy A0 with MODE=build first)" >&2; exit 65; }
fi
for B in $BL; do
  (cd "$SRC/$B" && sha256sum --quiet -c SHA256SUMS) || { echo "FATAL: local SHA256SUMS differ in $B" >&2; exit 66; }
  python3 - "$SRC/$B/plan.resolved.json" "$F" "$B" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
assert p["code_commit"] == sys.argv[2], "plan code_commit %s != F %s" % (p["code_commit"], sys.argv[2])
assert p["batch"] == sys.argv[3] and p.get("warnings") in (None, []), p.get("warnings")
assert p.get("island_isa") == "sapphirerapids", "leg plans are V / sapphirerapids"
print(p["batch"], "OK: code_commit == F; worst", p["worst_case_core_h"], "core-h; cap", p["core_h_cap"], "; fits", len(p["fits"]), "; tasks", p["n_tasks"])
PY
done
home_guard
for B in $BL; do
  ssh $NOTS "[[ ! -e $D/scratch/runs/$B/submissions.jsonl ]]" || { echo "REFUSING: $B was already submitted" >&2; exit 65; }
  ssh $NOTS "mkdir -p $D/scratch/overlap1e4 $D/scratch/runs/$B $D/scripts/$B"
done
ssh $NOTS "git -C $CN cat-file -e $F^{commit} 2>/dev/null" && echo "clone on NOTS already holds F" || rs "$CLONE"/ $NOTS:$CN/
ssh $NOTS "set -e; [[ \$(git -C $CN rev-parse $F:$CORE_PATH) == $CORE_TREE ]] && echo 'clone ok: core tree = pin'"
for B in $BL; do
  rs --exclude code --exclude bin --exclude build "$SRC/$B"/ $NOTS:$D/scripts/$B/
  ssh $NOTS "cd $D/scripts/$B && sha256sum --quiet -c SHA256SUMS && echo '$B: SHA256SUMS verified on NOTS'"
done
ver() {   # ver <batch>: the binary's version JSON with the batch's env.sh sourced (GCC 14.3.0 runtime), one line of facts to stdout
  ssh $NOTS "( set +u; source $D/scripts/$1/env.sh >/dev/null 2>&1; $D/scripts/$1/bin/smcbvs4 version 2>&1 )" > "$STG/.ver.$1" || true
  GC=$(grep -o '"git_commit": *"[^"]*"' "$STG/.ver.$1" | head -1 | grep -o '"[^"]*"$' | tr -d '"')
  ISA=$(grep -o '"island_isa": *"[^"]*"' "$STG/.ver.$1" | head -1 | grep -o '"[^"]*"$' | tr -d '"')
  LIBM=$(grep -c '"pass": *true' "$STG/.ver.$1" || true)
  rm -f "$STG/.ver.$1"
  [[ $GC == "$F" ]] || { echo "FATAL: $1 git_commit '$GC' != F $F" >&2; exit 67; }
  [[ $ISA == sapphirerapids && $LIBM -ge 1 ]] || { echo "FATAL: $1 island_isa '$ISA' / libm self-test '$LIBM'" >&2; exit 67; }
}
if [[ $MODE == build ]]; then
  B=$MASTER_BATCH
  CW=$(ssh $NOTS "readlink -f $D/scratch")/$CODE_WS_REL/PL_F${F:0:8}_code
  ssh $NOTS "set -e; if [[ -d $CW && \$(git -C $CW rev-parse HEAD 2>/dev/null) == $F && -z \$(git -C $CW status --porcelain --untracked-files=no) ]]; then echo 'shared worktree exists, clean at F'; \\
    else mkdir -p \$(dirname $CW); git -C $CN worktree remove --force $CW 2>/dev/null || true; rm -rf $CW; git -C $CN worktree prune; git -C $CN worktree add -q --detach $CW $F; fi
    [[ \$(git -C $CW rev-parse HEAD) == $F ]] && [[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]] && echo \"worktree $CW at $F (clean)\"
    cd $D/scripts/$B && rm -rf code && ln -s $CW code"
  home_guard
  ssh $NOTS "cd $D/scripts/$B && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 3 build_stdout.log; [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
  ssh $NOTS "set -e; ( set +u; source $D/scripts/$B/env.sh >/dev/null 2>&1; $D/scripts/$B/bin/smcbvs4 version 2>&1 ) > $D/scripts/$B/bin/version.json || true"
  ver $B
  SHA=$(ssh $NOTS "sha256sum $D/scripts/$B/bin/smcbvs4" | cut -d' ' -f1)
  ssh $NOTS "[[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]]" || { echo "FATAL: worktree dirty after the build" >&2; exit 67; }
  log_leg $B BUILD "$SHA" "$GC" "$ISA" "$LIBM" "$(home_mb)"
  LEGSHA=$SHA
  echo "BUILD $B sha256 $SHA git_commit $GC isa $ISA (the leg's ONE build, H-25)"
  BL=${BL#"$MASTER_BATCH"}; BL=${BL# }
fi
for B in $BL; do   # COPYBIN: the leg binary, unchanged
  ssh $NOTS "set -e; M=$D/scripts/$MASTER_BATCH/bin; [[ \$(sha256sum \$M/smcbvs4 | cut -d' ' -f1) == $LEGSHA ]] || { echo 'FATAL: the master binary does not match the BUILD line' >&2; exit 67; }
    mkdir -p $D/scripts/$B/bin; cp -p \$M/smcbvs4 $D/scripts/$B/bin/smcbvs4; cp -p \$M/version.json $D/scripts/$B/bin/version.json
    sha256sum $D/scripts/$B/bin/smcbvs4 > $D/scripts/$B/bin/smcbvs4.sha256; echo '$MASTER_BATCH' > $D/scripts/$B/bin/COPIED_FROM
    [[ \$(sha256sum $D/scripts/$B/bin/smcbvs4 | cut -d' ' -f1) == $LEGSHA ]] && echo '$B: bin/smcbvs4 copied from $MASTER_BATCH, sha256 == the leg build'"
  ver $B
  log_leg $B COPYBIN "$LEGSHA" "$GC" "$ISA" "$LIBM" "$(home_mb)"
done
home_guard
echo "deploy done (not submitted). Next: presubmit_check.sh $WAVE $F"
