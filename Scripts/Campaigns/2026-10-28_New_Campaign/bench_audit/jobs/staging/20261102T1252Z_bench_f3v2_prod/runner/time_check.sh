#!/usr/bin/env bash
# A real GNU time must identify itself and actually implement -f and -o.
set -euo pipefail
bin=$1; output=$2
[[ "$bin" = /* ]] && [ -f "$bin" ] && [ -x "$bin" ] || exit 1
"$bin" --version | grep -qi 'GNU time' || exit 1
"$bin" -f $'%e\t%M' -o "$output" /bin/true || exit 1
[ -f "$output" ] || exit 1
awk -F '\t' 'NF==2 && $1 ~ /^[0-9]+([.][0-9]+)?$/ && $2 ~ /^[0-9]+$/ {ok++} END {exit !(NR==1 && ok==1)}' "$output"
