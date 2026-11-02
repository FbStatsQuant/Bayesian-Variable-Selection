#!/bin/bash
# guard_check.sh -- refuse to proceed unless the OPS-owned guard.sh enforces the charter section 2 / D7 limits, then record a receipt.
#   bash guard_check.sh PLANNED_MB RECEIPT_FILE
# guard.sh is NOT edited or bypassed here. It does not print its limits, so this script (1) refuses test overrides in the environment,
# (2) extracts the two LIMIT assignments from guard.sh itself and requires campaign <= 0.5 GiB (524288 KB) and home <= 9.6 GiB (10066329 KB),
# (3) probes the guard's behaviour: a planned add of 513 MB must be refused for the campaign limit; an add that pushes home usage past 9.6 GiB
# must be refused for the home limit; (4) calls the guard with the planned add and requires exit 0 and status OK without TEST_LIMITS.
# Receipt: guard sha256, parsed limits, every call with its output and exit status. Exit 0 = D7 limits confirmed and the planned add admitted.
set -uo pipefail
PLANNED=${1:?usage: guard_check.sh PLANNED_MB RECEIPT_FILE}; REC=${2:?}
GUARD="${GUARD:-/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh}"
CAMP_REQ=${REQUIRED_CAMP_LIMIT_KB:-524288}; HOME_REQ=${REQUIRED_HOME_LIMIT_KB:-10066329}
[[ "$PLANNED" =~ ^[0-9]+$ ]] || { echo "planned MB must be a whole number" >&2; exit 2; }
say() { echo "$*" | tee -a "$REC"; }
: > "$REC"
fail() { say "GUARD_CHECK_FAILED: $*"; exit 1; }
say "# guard receipt $(date -u +%FT%TZ) by $(id -un) on $(hostname); guard $GUARD; planned add ${PLANNED} MB"
for v in GUARD_ALLOW_TEST GUARD_TEST_CAMP_LIMIT_MB GUARD_TEST_HOME_LIMIT_MB; do [ -z "${!v:-}" ] || fail "test override $v is set in the environment"; done
[ -r "$GUARD" ] || fail "guard not readable: $GUARD"
say "guard_sha256 $(sha256sum "$GUARD" | cut -d' ' -f1)"
# (2) the limits as written in guard.sh (only plain integer arithmetic is evaluated)
lim() { local line rhs; line=$(grep -E "^$1=" "$GUARD" | head -n 1) || return 1; rhs=${line#*=}; rhs=${rhs%%#*}; rhs=$(echo "$rhs" | sed 's/[[:space:]]*$//')
        [[ "$rhs" =~ ^\$\(\([0-9[:space:]*/+-]+\)\)$ ]] || return 1; echo $(( ${rhs:3:${#rhs}-5} )); }
CAMP_LIM=$(lim CAMP_LIMIT_KB) || fail "cannot read CAMP_LIMIT_KB from guard.sh (format changed?)"
HOME_LIM=$(lim HOME_LIMIT_KB) || fail "cannot read HOME_LIMIT_KB from guard.sh (format changed?)"
say "guard_limits campaign_kb=$CAMP_LIM home_kb=$HOME_LIM (required campaign <= $CAMP_REQ, home between 10000000 and $HOME_REQ)"
[ "$CAMP_LIM" -le "$CAMP_REQ" ] || fail "campaign limit $CAMP_LIM KB exceeds the charter 0.5 GiB ($CAMP_REQ KB)"
[ "$HOME_LIM" -le "$HOME_REQ" ] && [ "$HOME_LIM" -ge 10000000 ] || fail "home limit $HOME_LIM KB is not the charter 9.6 GiB (<= $HOME_REQ KB)"
# (4) the real call
out=$("$GUARD" "$PLANNED" 2>&1); rc=$?; say "call planned=$PLANNED rc=$rc :: $out"
[ $rc = 0 ] || fail "guard refused or failed (exit $rc) for a planned add of ${PLANNED} MB"
case "$out" in *TEST_LIMITS*) fail "guard output says TEST_LIMITS";; esac
case "$out" in *"| OK"*) ;; *) fail "guard status is not OK";; esac
# (3) behaviour probes
out=$("$GUARD" 513 2>&1); rc=$?; say "probe campaign add=513 rc=$rc :: $out"
{ [ $rc = 1 ] && case "$out" in *"campaign+add>limit"*) true;; *) false;; esac; } || fail "a 513 MB add was not refused for the campaign limit: the guard does not enforce 0.5 GiB"
used_gb=$(echo "$out" | sed -n 's/.*| home \([0-9.]*\) GB of.*/\1/p')
[ -n "$used_gb" ] || fail "cannot read home usage from the guard output"
over=$(awk -v u="$used_gb" 'BEGIN{printf "%d", (9.6 - u) * 1024 + 40}')
if [ "$over" -gt 0 ]; then
  out=$("$GUARD" "$over" 2>&1); rc=$?; say "probe home add=$over rc=$rc :: $out"
  { [ $rc = 1 ] && case "$out" in *"home+add>limit"*) true;; *) false;; esac; } || fail "an add of $over MB (past 9.6 GiB) was not refused for the home limit"
else say "probe home skipped: home usage ${used_gb} GB is already above 9.6 GiB"; fail "home usage already above the limit"; fi
say "GUARD_CHECK_OK campaign_limit_kb=$CAMP_LIM home_limit_kb=$HOME_LIM planned_mb=$PLANNED"
exit 0
