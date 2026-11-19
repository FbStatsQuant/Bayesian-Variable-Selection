# common.sh -- V-N mini-leg ops (F2 default-N identity check; HQ 4a47e8a4). Owls and NOTS share the department path. NOT the precision leg: its own log and dirs.
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}
STG=$D/staging/vn_minileg
LOG=$STG/deploy_F2.log                    # tab-separated: UTC  batch  BUILD_F2  sha256  git_commit  island_isa  libm_pass  home_MB  who
NOTS=nots
F2=e993ece226b355058e26400f05f9faad6daf16ca   # tag p1m-freeze-F2 (exp/P1M-engine: F + #85..#88)
CORE_TREE=61b0a5822019b2737fe415ff15625e410f3227b2
CORE_PATH=Scripts/SMC_BVS/core
BATCH=VN_ID_1
HOME_LIMIT_MB=7900
rs() { nice -n 19 rsync -a --checksum --rsync-path="nice -n 19 rsync" -e ssh "$@"; }
home_mb() { ssh $NOTS "quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'"; }
home_guard() { local mb; mb=$(home_mb); [[ $mb =~ ^[0-9]+$ ]] || { echo "REFUSING: home quota unreadable ('$mb')" >&2; return 1; }
  echo "NOTS home: $mb MB (refuse above $HOME_LIMIT_MB)"; [[ $mb -le $HOME_LIMIT_MB ]] || { echo "REFUSING: home $mb > $HOME_LIMIT_MB" >&2; return 1; }; }
# ---- the V-N mini-leg waves V0 / V1 / V2 (MINILEG_PLAN §4, §6): COPYBIN of the ONE F2 binary (BUILD_F2) ----
OWLS_REC=$D/records/vn_minileg
MASTER=VN_ID_1                              # the batch whose bin/ IS the F2 build (deploy_F2.log BUILD_F2 line)
f2_sha() { awk -F'\t' '$3=="BUILD_F2"{print $4; exit}' "$LOG" 2>/dev/null || true; }
batches_of() { ls -d "$1"/VN_"$2"_* 2>/dev/null | xargs -n1 basename | sort -t_ -k3 -n | tr '\n' ' '; }
log_vn() { printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "${WHO:-ops-sonnet}" >> "$LOG"; }
