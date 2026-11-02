#!/bin/bash
# test_stage_guard.sh -- HQ D57 regression (OPS-4 hit it on PROD-L): the STAGE was reserved twice. OPS runs guard.sh with the stage size BEFORE staging (correct); the driver must NOT
# ask the guard for the stage size again after extraction, because the stage already counts in home usage. bash test_stage_guard.sh WORKDIR
#   prodl.env: PLANNED_HOME_MB_STAGE = pre-staging reservation (110), PLANNED_HOME_MB_MAIN = growth after extraction (10).
#   (a) capacity-modelling guard (home used + add > limit -> exit 1 'home+add>limit', same line format as ops/guard.sh) seeded at 9.42 GiB: the pre-staging reservation is admitted; the
#       stage is "extracted" (usage += stage); the main wave must be ADMITTED, with the guard called with PLANNED_HOME_MB_MAIN and never the stage size again; the old behaviour (asking the
#       stage size again) would have been refused.
#   (b) guard_check.sh probes the home limit against the guard's OWN HOME_LIMIT_KB (9.70 GiB when HQ raises both guard.sh and REQUIRED_HOME_LIMIT_KB); a guard limit above REQUIRED is refused.
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_stage_guard
ENVF=prodl.env; DRIVER=submit_prodl.sh; STAGE_EXP=110; MAIN_EXP=10; SEED_GIB=9.42; NSUB=10
STAMP=20261030T2200Z
echo "== building the fake NOTS tree =="
t_mkfix "$W/fx" "$STAMP"

# ---- capacity-modelling guard ------------------------------------------------------------------------------------------------------------------
cat > "$T_BIN/guard_cap96" <<'G'
#!/bin/bash
# stub of ops/guard.sh: usage kept in $CAP_USED (KB); refuses when home used + add > HOME_LIMIT_KB (literal limit lines, parsed by guard_check.sh); logs each planned add to $CAP_CALLS
set -uo pipefail
ADD_MB=${1:-0}
echo "$ADD_MB" >> "${CAP_CALLS:-/dev/null}"
CAMP_LIMIT_KB=$((1024 * 1024 / 2))
HOME_LIMIT_KB=$((96 * 1024 * 1024 / 10))
HOME_KB=$(cat "${CAP_USED:?}"); CAMP_KB=${FAKE_CAMP_KB:-20000}
S=OK; RC=0; W=""
if [ $((CAMP_KB + ADD_MB * 1024)) -gt $CAMP_LIMIT_KB ]; then S=REFUSE; RC=1; W=" campaign+add>limit"; fi
if [ $((HOME_KB + ADD_MB * 1024)) -gt $HOME_LIMIT_KB ]; then S=REFUSE; RC=1; W="$W home+add>limit"; fi
echo "2026 | home $(awk -v k=$HOME_KB 'BEGIN{printf "%.2f", k/1048576}') GB of 10.00 GB | campaign_home 0.02 GB | campaign_scratch 0.00 GB (info) | planned_add ${ADD_MB} MB | $S${W:+ (${W# })}"
exit $RC
G
sed 's#^HOME_LIMIT_KB=.*#HOME_LIMIT_KB=$((970 * 1024 * 1024 / 100))#' "$T_BIN/guard_cap96" > "$T_BIN/guard_cap97"
chmod +x "$T_BIN/guard_cap96" "$T_BIN/guard_cap97"
export CAP_USED="$W/cap_used_kb" CAP_CALLS="$W/cap_calls.txt"
seed() { awk -v g="$1" 'BEGIN{printf "%d", g*1048576}' > "$CAP_USED"; : > "$CAP_CALLS"; }
used_kb() { cat "$CAP_USED"; }
calls() { tr '\n' ' ' < "$CAP_CALLS" | sed 's/ $//'; }
read -r STAGE MAIN < <( source "$BUN/$ENVF"; echo "${PLANNED_HOME_MB_STAGE:-unset} ${PLANNED_HOME_MB_MAIN:-unset}" )
t_eq "SG01 $ENVF: PLANNED_HOME_MB_STAGE (pre-staging reservation)" "$STAGE_EXP" "$STAGE"
t_eq "SG02 $ENVF: PLANNED_HOME_MB_MAIN (growth after extraction)" "$MAIN_EXP" "$MAIN"

# ---- (a) reproduction -----------------------------------------------------------------------------------------------------------------------------
t_reset_run; seed $SEED_GIB
"$T_BIN/guard_cap96" "$STAGE" > "$W/pre.out" 2>&1; rc=$?
t_eq "SG10 (a) OPS's pre-staging reservation of the stage ($STAGE MB) on a home at $SEED_GIB GiB: admitted, exit 0" 0 "$rc"
echo $(( $(used_kb) + STAGE * 1024 )) > "$CAP_USED"; : > "$CAP_CALLS"                  # the stage is EXTRACTED: it now counts in home usage
"$T_BIN/guard_cap96" "$STAGE" > "$W/again.out" 2>&1; rc=$?
t_eq "SG11 (a) control (the OLD behaviour): asking for the stage size AGAIN after extraction is refused, exit 1" 1 "$rc"
grep -q 'home+add>limit' "$W/again.out"; t_cond "SG12 ... with 'home+add>limit' in the guard's own line format" $?
head -n 1 "$W/again.out" | grep -qE '^[0-9]{4} \| home [0-9.]+ GB of 10.00 GB \| campaign_home .* \| planned_add [0-9]+ MB \| (OK|REFUSE)'; t_cond "SG13 ... same line format as ops/guard.sh" $?
: > "$CAP_CALLS"
DRV_ENV=(GUARD="$T_BIN/guard_cap96" CAP_USED="$CAP_USED" CAP_CALLS="$CAP_CALLS"); t_run_driver main --wave main --profile alone; DRV_ENV=()
t_eq "SG14 (a) the main wave after extraction is ADMITTED: exit 0, $NSUB submissions" "0 $NSUB" "$DRV_RC $(t_nsub)"
grep -qx "$MAIN" "$CAP_CALLS"; t_cond "SG15 ... the guard was called with PLANNED_HOME_MB_MAIN ($MAIN)" $?
grep -qx "$STAGE" "$CAP_CALLS"; [ $? -ne 0 ]; t_cond "SG16 ... and NEVER with the stage size ($STAGE) again (calls: $(calls))" $?
R="$LOGR/launch/main/guard_receipt.txt"
# (only submit_bench.sh records the 'D57 stage_on_disk_kb=... planned_add_mb=...' line in the receipt; PROD-L's driver is checked through the guard calls above)
grep -q 'GUARD_CHECK_OK' "$R" 2>/dev/null; t_cond "SG19 the launch guard receipt says GUARD_CHECK_OK" $?
grep -q "planned add ${MAIN} MB" "$R" 2>/dev/null; t_cond "SG19b ... for the planned add of $MAIN MB (the receipt shows the guard's own line)" $?
# a later wave asks for the (smaller) wave growth only
t_reset_run; seed $SEED_GIB; echo $(( $(used_kb) + STAGE * 1024 )) > "$CAP_USED"
# the growth itself is still checked: a home that cannot take PLANNED_HOME_MB_MAIN more is refused (exit 1), nothing submitted
awk -v lim="$(( 96 * 1024 * 1024 / 10 ))" -v m="$MAIN" 'BEGIN{printf "%d", lim - (m - 3) * 1024}' > "$CAP_USED"; : > "$CAP_CALLS"
DRV_ENV=(GUARD="$T_BIN/guard_cap96" CAP_USED="$CAP_USED" CAP_CALLS="$CAP_CALLS"); t_run_driver tight --wave main --profile alone; DRV_ENV=()
t_eq "SG20 a home with only $((MAIN - 3)) MB of headroom cannot take the $MAIN MB growth: the guard refuses, exit 1" 1 "$DRV_RC"
t_no_submission; t_cond "SG21 ... nothing submitted, nothing created" $?
grep -qx "$MAIN" "$CAP_CALLS"; t_cond "SG22 ... the refused call was the growth ($MAIN)" $?

# ---- (b) guard_check.sh against the guard's OWN home limit -------------------------------------------------------------------------------------------
GC="$BUN/guard_check.sh"
gc() {   # gc LABEL GUARD REQUIRED_HOME_LIMIT_KB : the staged guard_check.sh with used = 9.42 GiB
  seed 9.42
  ( export GUARD="$2" REQUIRED_CAMP_LIMIT_KB=524288 REQUIRED_HOME_LIMIT_KB="$3"; bash "$GC" 5 "$W/gc_$1.rec" ) > "$W/gc_$1.out" 2>&1; GC_RC=$?
}
probe_mb() { sed -n 's/.*probe home add=\([0-9]*\) .*/\1/p' "$W/gc_$1.rec" | head -n 1; }
gc d97 "$T_BIN/guard_cap97" 10171187
t_eq "SG30 (b) a guard enforcing 9.70 GiB with REQUIRED_HOME_LIMIT_KB=10171187: GUARD_CHECK_OK, exit 0" 0 "$GC_RC"
grep -q GUARD_CHECK_OK "$W/gc_d97.rec"; t_cond "SG31 ... the receipt says GUARD_CHECK_OK" $?
p=$(probe_mb d97); [ -n "$p" ] && [ "$p" -ge 300 ] && [ "$p" -le 360 ]; t_cond "SG32 ... the home probe is against ~9.70 GiB: add ~ (9.70-9.42)*1024+40 = 327 MB (got '${p:-none}')" $?
gc d97_req96 "$T_BIN/guard_cap97" 10066329
t_eq "SG33 a guard at 9.70 GiB with REQUIRED_HOME_LIMIT_KB at 9.6 GiB (10066329): REFUSED, exit 1" 1 "$GC_RC"
grep -q 'GUARD_CHECK_FAILED' "$W/gc_d97_req96.rec"; t_cond "SG34 ... GUARD_CHECK_FAILED recorded" $?
gc d96 "$T_BIN/guard_cap96" 10066329
t_eq "SG35 the default 9.6 / 9.6: unchanged, GUARD_CHECK_OK, exit 0" 0 "$GC_RC"
p=$(probe_mb d96); [ -n "$p" ] && [ "$p" -ge 200 ] && [ "$p" -le 260 ]; t_cond "SG36 ... the probe is against 9.6 GiB: add ~ (9.6-9.42)*1024+40 = 224 MB (got '${p:-none}')" $?
gc d96_req97 "$T_BIN/guard_cap96" 10171187
t_eq "SG37 a guard at 9.6 GiB with REQUIRED at 9.7 GiB: the guard's own limit is below REQUIRED but not below the 10,000,000 KB floor: accepted (exit 0)" 0 "$GC_RC"
seed 9.42; sed 's#^HOME_LIMIT_KB=.*#HOME_LIMIT_KB=$((90 * 1024 * 1024 / 10))#' "$T_BIN/guard_cap96" > "$T_BIN/guard_cap90"; chmod +x "$T_BIN/guard_cap90"
gc d90 "$T_BIN/guard_cap90" 10066329
t_eq "SG38 a guard enforcing only 9.0 GiB (below the charter floor): REFUSED, exit 1" 1 "$GC_RC"
t_eq "SG39 a guard that does not enforce the campaign 0.5 GiB limit is still refused" 1 "$( seed 9.42; sed 's#^CAMP_LIMIT_KB=.*#CAMP_LIMIT_KB=$((2 * 1024 * 1024))#' "$T_BIN/guard_cap96" > "$T_BIN/guard_campbad"; chmod +x "$T_BIN/guard_campbad"; GUARD="$T_BIN/guard_campbad" REQUIRED_CAMP_LIMIT_KB=524288 REQUIRED_HOME_LIMIT_KB=10066329 bash "$GC" 5 "$W/gc_camp.rec" > /dev/null 2>&1; echo $? )"

t_summary
