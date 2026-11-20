# common.sh -- 1M pilot GC_P (GC_PLAN, HQ H-45). COPYBIN of the ONE F2 binary (BUILD_F2); derived from the V-N mini-leg's common.sh (that one is untouched). Owls and NOTS share the department path.
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}
STG=$D/staging/gc1m
LOG=$STG/deploy_gc.log                    # tab-separated: UTC  batch  BUILD_F2|COPYBIN  sha256  git_commit  island_isa  libm_pass  home_MB  who
NOTS=nots
F2=e993ece226b355058e26400f05f9faad6daf16ca   # tag p1m-freeze-F2
BATCH=VN_ID_1
MASTER=VN_ID_1                              # the batch whose bin/ IS the F2 build (the BUILD_F2 line)
HOME_LIMIT_MB=7900
SCRIPTS=$STG/scripts
OWLS_REC=$D/records/gc1m
rs() { nice -n 19 rsync -a --partial --rsync-path="nice -n 19 rsync" -e ssh "$@"; }   # no --checksum at 1M (60 GB): the sha256 list computed on NOTS is verified on Owls by sha256sum -c
home_mb() { ssh $NOTS "quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'"; }
home_guard() { local mb; mb=$(home_mb); [[ $mb =~ ^[0-9]+$ ]] || { echo "REFUSING: home quota unreadable ('$mb')" >&2; return 1; }
  echo "NOTS home: $mb MB (refuse above $HOME_LIMIT_MB)"; [[ $mb -le $HOME_LIMIT_MB ]] || { echo "REFUSING: home $mb > $HOME_LIMIT_MB" >&2; return 1; }; }
f2_sha() { awk -F'\t' '$3=="BUILD_F2"{print $4; exit}' "$LOG" 2>/dev/null || true; }
# GC waves (GC_PLAN §3): P = the G-C2 pilot GC_P alone (6-AR-n200-r01-V-s1, 1M, F2, N 2,500, I_max 0); later waves (W1..W10, X1, D, S1..S10) are added at their release
batches_of() { case "$2" in P) echo "GC_P";; *) return 1;; esac; }
log_gc() { printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "${WHO:-ops-sonnet}" >> "$LOG"; }
