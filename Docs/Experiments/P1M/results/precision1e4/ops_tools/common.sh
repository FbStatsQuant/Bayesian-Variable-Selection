# common.sh -- shared settings of the PRECISION-LEG ops scripts (sourced). Owls and NOTS share the same department path.
# Derived from the overlap's staging/overlap1e4/tools (left untouched); the leg's deploy log is $LEG_LOG (H-25: ONE build per arm for the leg).
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}   # P1M_OPS_D: tests only
STG=$D/staging/precision1e4
OWLS_REC=$D/records/precision1e4
LEG_LOG=$STG/deploy_leg.log                # tab-separated: UTC  batch  MODE  sha256  git_commit  island_isa  libm_pass  home_MB  who   (MODE = BUILD | COPYBIN | PLANS)
NOTS=nots                                  # ssh alias; ControlMaster auto, ONE connection (NOTS_FACTS usage discipline)
CORE_TREE=61b0a5822019b2737fe415ff15625e410f3227b2
CORE_PATH=Scripts/SMC_BVS/core
MASTER_BATCH=PL_A0_1                       # the batch that is BUILT; every other batch gets a copy of its bin/smcbvs4
CODE_WS_REL=code_ws
HOME_LIMIT_MB=7900                         # NOTS home: refuse above this (hard guard 8,192)
need_full_sha() { [[ ${1:-} =~ ^[0-9a-f]{40}$ ]] || { echo "need a 40-hex commit, got '${1:-}'" >&2; exit 64; }; }
rs() { nice -n 19 rsync -a --checksum --rsync-path="nice -n 19 rsync" -e ssh "$@"; }   # one stream, low priority
# batches of a wave, in order, from the plans/scripts dir: PL_<wave>_<i>
batches_of() { ls -d "$1"/PL_"$2"_* 2>/dev/null | xargs -n1 basename | sort -t_ -k3 -n | tr '\n' ' '; }
# the leg's single build sha256 = the first BUILD line of the deploy log ("" if none yet)
leg_sha() { [[ -f $LEG_LOG ]] && awk -F'\t' '$3=="BUILD"{print $4; exit}' "$LEG_LOG" || true; }
home_mb() { ssh $NOTS "quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'"; }
home_guard() {
  local mb; mb=$(home_mb)
  [[ $mb =~ ^[0-9]+$ ]] || { echo "REFUSING: NOTS home quota unreadable ('$mb')" >&2; return 1; }
  echo "NOTS home: $mb MB used (refuse above $HOME_LIMIT_MB; hard guard 8192)"
  [[ $mb -le $HOME_LIMIT_MB ]] || { echo "REFUSING: NOTS home $mb MB > $HOME_LIMIT_MB MB. Free home first (code trees belong in scratch code_ws/)." >&2; return 1; }
}
log_leg() { printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "${WHO:-ops-sonnet}" >> "$LEG_LOG"; }
# ---- the T arm (boundary wave B1, ADDENDUM_1_BOUNDARY): ONE T build for the leg, logged as a BUILD_T line (law mode, default ISA = portable); T batches = plan mode law ----
batch_mode() { python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['mode'])" "$1/$2/plan.resolved.json"; }   # batch_mode <scripts dir> <batch> -> V | law
leg_sha_T() { [[ -f $LEG_LOG ]] && awk -F'\t' '$3=="BUILD_T"{print $4; exit}' "$LEG_LOG" || true; }
t_master()  { [[ -f $LEG_LOG ]] && awk -F'\t' '$3=="BUILD_T"{print $2; exit}' "$LEG_LOG" || true; }
