# common.sh -- 10^5 rung (RUNG_PLAN, HQ H-40). COPYBIN of the ONE F2 binary (BUILD_F2); derived from the V-N mini-leg's common.sh (that one is untouched). Owls and NOTS share the department path.
D=${P1M_OPS_D:-/home/fb31/SMC_Engineering_Department}
STG=$D/staging/rung1e5
LOG=$STG/deploy_rung.log                    # tab-separated: UTC  batch  BUILD_F2|COPYBIN  sha256  git_commit  island_isa  libm_pass  home_MB  who
NOTS=nots
F2=e993ece226b355058e26400f05f9faad6daf16ca   # tag p1m-freeze-F2
BATCH=VN_ID_1
MASTER=VN_ID_1                              # the batch whose bin/ IS the F2 build (the BUILD_F2 line)
HOME_LIMIT_MB=7900
SCRIPTS=$STG/scripts
OWLS_REC=$D/records/rung1e5
rs() { nice -n 19 rsync -a --checksum --rsync-path="nice -n 19 rsync" -e ssh "$@"; }
home_mb() { ssh $NOTS "quota -s 2>/dev/null | grep -A1 export/nots/home | tail -1 | awk '{v=\$1; if (v ~ /G\$/) {sub(/G/,\"\",v); v*=1024} else sub(/M/,\"\",v); printf \"%d\", v}'"; }
home_guard() { local mb; mb=$(home_mb); [[ $mb =~ ^[0-9]+$ ]] || { echo "REFUSING: home quota unreadable ('$mb')" >&2; return 1; }
  echo "NOTS home: $mb MB (refuse above $HOME_LIMIT_MB)"; [[ $mb -le $HOME_LIMIT_MB ]] || { echo "REFUSING: home $mb > $HOME_LIMIT_MB" >&2; return 1; }; }
f2_sha() { awk -F'\t' '$3=="BUILD_F2"{print $4; exit}' "$LOG" 2>/dev/null || true; }
# the rung's waves (RUNG_PLAN §3), submission order: R1 = n400 pilot, the two continuity twins, the T6 restart test; R2 = AR n200 r02-r05, AR n400 r02-r03; R3 = IND n200 x2, ADJ-OPP n200 r02
batches_of() { case "$2" in R1) echo "RG_1a RG_1b RG_T6";; R2) echo "RG_2a RG_2b";; R3) echo "RG_3a RG_3b";; *) return 1;; esac; }
log_rung() { printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "${WHO:-ops-sonnet}" >> "$LOG"; }
