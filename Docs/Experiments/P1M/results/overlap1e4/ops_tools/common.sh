# common.sh -- shared settings of the overlap-1e4 ops scripts (sourced). Owls and NOTS share the same department path.
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}   # P1M_OPS_D: tests only
STG=$D/staging/overlap1e4
OWLS_REC=$D/records/overlap1e4
NOTS=nots                                  # ssh alias; ControlMaster auto, ONE connection (NOTS_FACTS §usage discipline)
CORE_TREE=61b0a5822019b2737fe415ff15625e410f3227b2
CORE_PATH=Scripts/SMC_BVS/core
need_full_sha() { [[ ${1:-} =~ ^[0-9a-f]{40}$ ]] || { echo "need a 40-hex commit, got '${1:-}'" >&2; exit 64; }; }
rs() { nice -n 19 rsync -a --checksum --rsync-path="nice -n 19 rsync" -e ssh "$@"; }   # one stream, low priority
