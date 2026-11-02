#!/usr/bin/env bash
set -euo pipefail
GUARD=$1
quota() { printf 'export/nots/home %s 10485760 10485760\n' "$MOCK_QUOTA_KB"; }
export -f quota
export MOCK_QUOTA_KB=9000000
output=$(bash "$GUARD" 513) && { echo "FAIL guard admitted >0.5 GiB"; exit 1; }
case "$output" in *"campaign+add>limit"*) echo "PASS guard refusal over campaign ceiling";; *) echo "FAIL unexpected guard result: $output"; exit 1;; esac
export MOCK_QUOTA_KB=10000000
output=$(bash "$GUARD" 100) && { echo "FAIL guard admitted >9.6 GiB"; exit 1; }
case "$output" in *"home+add>limit"*) echo "PASS guard refusal over home ceiling";; *) echo "FAIL unexpected guard result: $output"; exit 1;; esac
