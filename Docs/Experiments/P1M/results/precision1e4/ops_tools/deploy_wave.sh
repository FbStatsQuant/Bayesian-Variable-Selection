#!/usr/bin/env bash
# deploy_wave.sh <WAVE> <F40> <SCRIPTS_SRC> <CLONE_LOCAL> <MODE>   -- PRECISION LEG (O-2). Owls -> NOTS. NEVER submits.
#   MODE = build    BUILD the leg's ONE binary in PL_A0_1 (wave A0 only, only while deploy_leg.log has no BUILD line), then COPYBIN the wave's other batches
#          copybin  every later wave: `cp -p` the leg binary from PL_A0_1 into each batch's bin/, verify sha256 == the BUILD line (H-25 (2): no rebuild)
#          buildT   (boundary wave B1 only) like copybin for the V batches, and BUILDS the leg's ONE T binary (law mode, default ISA = portable) in the first T batch
#                   (plan mode law), logged as a BUILD_T line; refused if a BUILD_T line exists (H-25: one T build). Later T batches: `copybin` copies it.
#   BATCHES="PL_P1_1 ..." (env) deploys a subset; default = all batches of the wave found in SCRIPTS_SRC.
# Steps (each fails loudly): local SHA256SUMS ok and plan.code_commit == F -> home guard -> refuse an already submitted batch -> mkdir on NOTS ->
# shallow clone of F (reused: scratch/overlap1e4/clone_<F8>) -> rsync the driver files (no code/bin/build) -> sha256sum -c ON NOTS ->
# [build only] shared worktree code_ws/PL_F<F8>_code (clean, HEAD == F, build dir OUTSIDE the tree) -> build.sh -> `version` (env.sh sourced) git_commit == F exactly
# -> deploy_leg.log line per batch (UTC, batch, MODE, sha256, git_commit, island_isa, libm_pass, home MB, who).
# The leg has ONE arm (V-1M class A, island_isa sapphirerapids); A3 is a runtime `partition` setting of the same binary.
set -euo pipefail; . "$(dirname "$0")/common.sh"
WAVE=${1:?WAVE}; F=${2:?F}; SRC=${3:?SCRIPTS_SRC}; CLONE=${4:?CLONE_LOCAL}; MODE=${5:?MODE build|copybin|buildT}
need_full_sha "$F"; [[ $WAVE =~ ^(A0|P[1-4]|H[1-3]|S[1-9]|S10|FZ|B1)$ ]] || { echo "bad wave" >&2; exit 64; }
[[ $MODE == build || $MODE == copybin || $MODE == buildT ]] || { echo "MODE must be build, copybin or buildT" >&2; exit 64; }
BL=${BATCHES:-$(batches_of "$SRC" "$WAVE")}; [[ -n $BL ]] || { echo "no batches PL_${WAVE}_* in $SRC" >&2; exit 64; }
CN=$D/scratch/overlap1e4/clone_${F:0:8}
LEGSHA=$(leg_sha); LEGSHA_T=$(leg_sha_T)
VBL=""; TBL=""
for B in $BL; do [[ -f $SRC/$B/plan.resolved.json ]] || { echo "no plan.resolved.json for $B in $SRC" >&2; exit 64; }
  if [[ $(batch_mode "$SRC" "$B") == law ]]; then TBL="$TBL $B"; else VBL="$VBL $B"; fi; done
VBL=${VBL# }; TBL=${TBL# }
if [[ -n $TBL ]]; then   # T batches exist only in the boundary wave
  [[ $WAVE == B1 ]] || { echo "REFUSING: T (law mode) batches only in wave B1 (ADDENDUM_1), got $TBL in $WAVE" >&2; exit 65; }
  if [[ $MODE == buildT ]]; then
    [[ -z $LEGSHA_T ]] || { echo "REFUSING: the leg already has its T build ($LEGSHA_T): H-25, ONE T build" >&2; exit 65; }
  else
    [[ -n $LEGSHA_T ]] || { echo "REFUSING: T batches need MODE=buildT (no BUILD_T line in $LEG_LOG yet)" >&2; exit 65; }
  fi
fi
if [[ $MODE == buildT ]]; then
  [[ -n $TBL ]] || { echo "REFUSING: buildT with no T batch in the wave" >&2; exit 65; }
  [[ -n $LEGSHA ]] || { echo "REFUSING: the V batches of B1 are COPYBIN: no BUILD line in $LEG_LOG yet" >&2; exit 65; }
elif [[ $MODE == build ]]; then
  [[ $WAVE == A0 && ( $BL == "$MASTER_BATCH" || $BL == "$MASTER_BATCH "* ) ]] || { echo "REFUSING: build only in wave A0, first batch $MASTER_BATCH (H-25: ONE build per arm for the whole leg)" >&2; exit 65; }
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
assert (p.get("island_isa") == "sapphirerapids") == (p["mode"] == "V") and p["mode"] in ("V", "law"), "V plans are sapphirerapids; the B1 T plan is law mode with the default ISA"
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
ver() {   # ver <batch> <V|T>: the binary's version JSON with the batch's env.sh sourced (GCC 14.3.0 runtime); facts in GC / ISA / LIBM
  ssh $NOTS "( set +u; source $D/scripts/$1/env.sh >/dev/null 2>&1; $D/scripts/$1/bin/smcbvs4 version 2>&1 )" > "$STG/.ver.$1" || true
  GC=$(grep -o '"git_commit": *"[^"]*"' "$STG/.ver.$1" | head -1 | grep -o '"[^"]*"$' | tr -d '"')
  ISA=$(grep -o '"island_isa": *"[^"]*"' "$STG/.ver.$1" | head -1 | grep -o '"[^"]*"$' | tr -d '"')
  LIBM=$(grep -c '"pass": *true' "$STG/.ver.$1" || true)
  rm -f "$STG/.ver.$1"
  local want=sapphirerapids; [[ $2 == T ]] && want=portable
  [[ $GC == "$F" ]] || { echo "FATAL: $1 git_commit '$GC' != F $F" >&2; exit 67; }
  [[ $ISA == $want && $LIBM -ge 1 ]] || { echo "FATAL: $1 island_isa '$ISA' (want $want) / libm self-test '$LIBM'" >&2; exit 67; }
}
worktree() {   # the shared worktree of the clone at F (clean, HEAD == F); sets CW
  CW=$(ssh $NOTS "readlink -f $D/scratch")/$CODE_WS_REL/PL_F${F:0:8}_code
  ssh $NOTS "set -e; if [[ -d $CW && \$(git -C $CW rev-parse HEAD 2>/dev/null) == $F && -z \$(git -C $CW status --porcelain --untracked-files=no) ]]; then echo 'shared worktree exists, clean at F'; \\
    else mkdir -p \$(dirname $CW); git -C $CN worktree remove --force $CW 2>/dev/null || true; rm -rf $CW; git -C $CN worktree prune; git -C $CN worktree add -q --detach $CW $F; fi
    [[ \$(git -C $CW rev-parse HEAD) == $F ]] && [[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]] && echo \"worktree $CW at $F (clean)\""
}
do_build() {   # do_build <batch> <V|T> <BUILD|BUILD_T>: build in <batch>, verify, log; sets BUILT_SHA
  local B=$1 K=$2 TAG=$3
  worktree; ssh $NOTS "cd $D/scripts/$B && rm -rf code && ln -s $CW code"
  home_guard
  ssh $NOTS "cd $D/scripts/$B && nice -n 19 bash build.sh > build_stdout.log 2>&1; rc=\$?; tail -n 3 build_stdout.log; [[ \$rc -eq 0 ]] && sha256sum -c bin/smcbvs4.sha256"
  ssh $NOTS "set -e; ( set +u; source $D/scripts/$B/env.sh >/dev/null 2>&1; $D/scripts/$B/bin/smcbvs4 version 2>&1 ) > $D/scripts/$B/bin/version.json || true"
  ver $B $K
  BUILT_SHA=$(ssh $NOTS "sha256sum $D/scripts/$B/bin/smcbvs4" | cut -d' ' -f1)
  ssh $NOTS "[[ -z \$(git -C $CW status --porcelain --untracked-files=no) ]]" || { echo "FATAL: worktree dirty after the build" >&2; exit 67; }
  log_leg $B $TAG "$BUILT_SHA" "$GC" "$ISA" "$LIBM" "$(home_mb)"
  echo "$TAG $B sha256 $BUILT_SHA git_commit $GC isa $ISA (the leg's ONE $K build, H-25)"
}
do_copy() {    # do_copy <batch> <V|T> <master batch> <sha> : cp -p the leg binary, verify sha256, log COPYBIN
  local B=$1 K=$2 M=$3 SH=$4
  ssh $NOTS "set -e; MB=$D/scripts/$M/bin; [[ \$(sha256sum \$MB/smcbvs4 | cut -d' ' -f1) == $SH ]] || { echo 'FATAL: the master binary does not match its BUILD line' >&2; exit 67; }
    mkdir -p $D/scripts/$B/bin; cp -p \$MB/smcbvs4 $D/scripts/$B/bin/smcbvs4; cp -p \$MB/version.json $D/scripts/$B/bin/version.json
    sha256sum $D/scripts/$B/bin/smcbvs4 > $D/scripts/$B/bin/smcbvs4.sha256; echo '$M' > $D/scripts/$B/bin/COPIED_FROM
    [[ \$(sha256sum $D/scripts/$B/bin/smcbvs4 | cut -d' ' -f1) == $SH ]] && echo '$B: bin/smcbvs4 copied from $M, sha256 == the leg $K build'"
  ver $B $K
  log_leg $B COPYBIN "$SH" "$GC" "$ISA" "$LIBM" "$(home_mb)"
}
if [[ $MODE == build ]]; then            # the V build (wave A0, PL_A0_1)
  do_build $MASTER_BATCH V BUILD; LEGSHA=$BUILT_SHA; VBL=${VBL#"$MASTER_BATCH"}; VBL=${VBL# }
fi
if [[ $MODE == buildT ]]; then           # the leg's ONE T build (wave B1): the first T batch
  TM=${TBL%% *}; do_build $TM T BUILD_T; LEGSHA_T=$BUILT_SHA; T_MASTER=$TM; TBL=${TBL#"$TM"}; TBL=${TBL# }
else
  T_MASTER=$(t_master)
fi
for B in $VBL; do do_copy $B V $MASTER_BATCH $LEGSHA; done      # COPYBIN: the leg binaries, unchanged
for B in $TBL; do do_copy $B T $T_MASTER $LEGSHA_T; done
home_guard
echo "deploy done (not submitted). Next: presubmit_check.sh $WAVE $F"
