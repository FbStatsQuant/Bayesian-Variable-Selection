# common.sh -- shared settings of the overlap-1e4 ops scripts (sourced). Owls and NOTS share the same department path.
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}   # P1M_OPS_D: tests only
STG=$D/staging/overlap1e4
OWLS_REC=$D/records/overlap1e4
NOTS=nots                                  # ssh alias; ControlMaster auto, ONE connection (NOTS_FACTS §usage discipline)
CORE_TREE=61b0a5822019b2737fe415ff15625e410f3227b2
CORE_PATH=Scripts/SMC_BVS/core
need_full_sha() { [[ ${1:-} =~ ^[0-9a-f]{40}$ ]] || { echo "need a 40-hex commit, got '${1:-}'" >&2; exit 64; }; }
rs() { nice -n 19 rsync -a --checksum --rsync-path="nice -n 19 rsync" -e ssh "$@"; }   # one stream, low priority
HOME_LIMIT_MB=7500                         # NOTS home guard is 8,192 MB; refuse new deploys above this (manager 11-18, after code trees hit 8,077)
# home_guard: one read-only ssh; prints NOTS home usage in MB, returns 1 above HOME_LIMIT_MB or if it cannot be read
home_guard() {
  local mb; mb=$(ssh $NOTS "quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'")
  [[ $mb =~ ^[0-9]+$ ]] || { echo "REFUSING: NOTS home quota unreadable ('$mb')" >&2; return 1; }
  echo "NOTS home: $mb MB used (refuse above $HOME_LIMIT_MB; hard guard 8192)"
  [[ $mb -le $HOME_LIMIT_MB ]] || { echo "REFUSING: NOTS home $mb MB > $HOME_LIMIT_MB MB. Free home first (code trees belong in scratch code_ws/)." >&2; return 1; }
}
# the code tree (git archive, ~360 MB) lives in SCRATCH; scripts/<batch>/code is a symlink to it (build.sh reads $SCR/code)
CODE_WS_REL=code_ws
ARMS=${ARMS:-T V}                          # batch arms of a wave: T V (original) or T2 V2 (rebuilds from the git clone of F); ARMS="T2 V2" deploy_wave.sh ...
