#!/bin/bash
# guard.sh: NOTS disk guard for the New Campaign (runs on NOTS).
# Usage: guard.sh [PLANNED_ADD_MB]
#   Prints home usage, the campaign's home usage and its scratch usage, as one line.
#   Exits 1 if (campaign home usage + PLANNED_ADD_MB) > 0.5 GiB,
#   or if (home quota usage + PLANNED_ADD_MB) > 9.6 GiB (charter §2, D7). Exits 2 if any measurement fails (fail closed).
#   /scratch/fb31/New_Campaign usage is reported for information only (no limit).
#   GB here means GiB (1024^3 bytes), the unit `quota` reports.
# Test-only: GUARD_ALLOW_TEST=1 plus GUARD_TEST_CAMP_LIMIT_MB / GUARD_TEST_HOME_LIMIT_MB override the limits;
#   every line printed then says TEST_LIMITS. Without GUARD_ALLOW_TEST=1 the overrides are refused (exit 2).
set -uo pipefail
ADD_MB=${1:-0}
# Decimal, no leading zeros, at most 7 digits (< 10 TB): no octal parsing and no 64-bit overflow in the arithmetic below.
mb_ok() { [[ "$1" =~ ^(0|[1-9][0-9]{0,6})$ ]]; }
mb_ok "$ADD_MB" || { echo "guard: PLANNED_ADD_MB must be a whole number of MB (0..9999999, no leading zeros)" >&2; exit 2; }
CAMP=/home/fb31/projects/BVS/New_Campaign
SCR=/scratch/fb31/New_Campaign
CAMP_LIMIT_KB=$((1024 * 1024 / 2))          # 0.5 GiB = 524288 KB
HOME_LIMIT_KB=$((96 * 1024 * 1024 / 10))    # 9.6 GiB = 10066329 KB (rounded down)
ADD_KB=$((ADD_MB * 1024))
TEST=""
if [ -n "${GUARD_TEST_CAMP_LIMIT_MB:-}${GUARD_TEST_HOME_LIMIT_MB:-}" ]; then
  [ "${GUARD_ALLOW_TEST:-0}" = 1 ] || { echo "guard: test limit overrides set without GUARD_ALLOW_TEST=1" >&2; exit 2; }
  # Each override replaces only its own limit; the other keeps its exact production value.
  if [ -n "${GUARD_TEST_CAMP_LIMIT_MB:-}" ]; then mb_ok "$GUARD_TEST_CAMP_LIMIT_MB" || { echo "guard: bad GUARD_TEST_CAMP_LIMIT_MB" >&2; exit 2; }; CAMP_LIMIT_KB=$((GUARD_TEST_CAMP_LIMIT_MB * 1024)); fi
  if [ -n "${GUARD_TEST_HOME_LIMIT_MB:-}" ]; then mb_ok "$GUARD_TEST_HOME_LIMIT_MB" || { echo "guard: bad GUARD_TEST_HOME_LIMIT_MB" >&2; exit 2; }; HOME_LIMIT_KB=$((GUARD_TEST_HOME_LIMIT_MB * 1024)); fi
  TEST=" | TEST_LIMITS camp=${CAMP_LIMIT_KB}KB home=${HOME_LIMIT_KB}KB"
fi
num() { [[ "$1" =~ ^(0|[1-9][0-9]{0,14})$ ]]; }   # KB values: bounded, decimal
duk() { local out; out=$(du -sk -- "$1") || return 1; out=${out%%[[:space:]]*}; num "$out" || return 1; echo "$out"; }

# Home usage (KB) from the quota system; it is authoritative for the 10 GB limit.
Q=$(quota -w 2>&1) || true     # quota exits non-zero when over a soft limit; parse instead of trusting rc
HOME_KB=$(awk '/export\/nots\/home/ {gsub(/\*/,"",$2); print $2; exit}' <<< "$Q")
QUOTA_KB=$(awk '/export\/nots\/home/ {gsub(/\*/,"",$3); print $3; exit}' <<< "$Q")
num "${HOME_KB:-x}" && num "${QUOTA_KB:-x}" || { echo "guard: cannot parse home quota: $Q" >&2; exit 2; }
CAMP_KB=0; SCR_KB=0
if [ -e "$CAMP" ]; then CAMP_KB=$(duk "$CAMP") || { echo "guard: du failed on $CAMP" >&2; exit 2; }; fi
if [ -e "$SCR" ]; then SCR_KB=$(duk "$SCR") || { echo "guard: du failed on $SCR" >&2; exit 2; }; fi

gb() { awk -v k="$1" 'BEGIN{printf "%.2f", k/1048576}'; }
STATUS=OK; RC=0; WHY=""
if [ $((CAMP_KB + ADD_KB)) -gt $CAMP_LIMIT_KB ]; then STATUS=REFUSE; RC=1; WHY="$WHY campaign+add>limit"; fi
if [ $((HOME_KB + ADD_KB)) -gt $HOME_LIMIT_KB ]; then STATUS=REFUSE; RC=1; WHY="$WHY home+add>limit"; fi
echo "$(date -u +%FT%TZ) | home $(gb $HOME_KB) GB of $(gb $QUOTA_KB) GB | campaign_home $(gb $CAMP_KB) GB | campaign_scratch $(gb $SCR_KB) GB (info) | planned_add ${ADD_MB} MB | $STATUS${WHY:+ (${WHY# })}$TEST"
exit $RC
