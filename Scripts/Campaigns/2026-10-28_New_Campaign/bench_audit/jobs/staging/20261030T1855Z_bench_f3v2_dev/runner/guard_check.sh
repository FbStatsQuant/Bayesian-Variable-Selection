#!/usr/bin/env bash
set -euo pipefail
guard=/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh
for v in GUARD_ALLOW_TEST GUARD_TEST_CAMP_LIMIT_MB GUARD_TEST_HOME_LIMIT_MB; do
  [ -z "${!v:-}" ] || { echo "guard override refused" >&2; exit 1; }
done
grep -Eq '^CAMP_LIMIT_KB=\$\(\(1024 \* 1024 / 2\)\)' "$guard"
grep -Eq '^HOME_LIMIT_KB=\$\(\(96 \* 1024 \* 1024 / 10\)\)' "$guard"
bash "$guard" "${1:?planned MB required}"
set +e
out=$(bash "$guard" 513 2>&1); rc=$?
set -e
echo "$out"
[ "$rc" = 1 ] && [[ "$out" == *"campaign+add>limit"* ]] || exit 1
used=$(sed -n 's/.*| home \([0-9.]*\) GB of.*/\1/p' <<< "$out")
[[ "$used" =~ ^[0-9]+([.][0-9]+)?$ ]] || exit 1
over=$(awk -v u="$used" 'BEGIN {printf "%d", (9.6-u)*1024+40}')
[ "$over" -gt 0 ] || exit 1
set +e
out=$(bash "$guard" "$over" 2>&1); rc=$?
set -e
echo "$out"
[ "$rc" = 1 ] && [[ "$out" == *"home+add>limit"* ]] || exit 1
echo "GUARD_CHECK_OK sha256=$(sha256sum "$guard" | cut -d' ' -f1)"
