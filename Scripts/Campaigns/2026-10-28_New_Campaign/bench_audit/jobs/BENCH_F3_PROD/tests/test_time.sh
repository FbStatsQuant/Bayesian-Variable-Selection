#!/usr/bin/env bash
set -euo pipefail
checker=$1; good=$2; liar=$3; folder=$4
folder=$(cygpath -u "$folder")
tempdir=$(mktemp -d "$folder/time_test.XXXXXX")
cp "$good" "$tempdir/good"
cp "$liar" "$tempdir/liar"
chmod u+x "$tempdir/good" "$tempdir/liar"
good="$tempdir/good"; liar="$tempdir/liar"
out="$tempdir/probe"
trap 'rm -f -- "$out" "$good" "$liar"; rmdir "$tempdir"' EXIT
bash "$checker" "$good" "$out"
rm -f -- "$out"
if bash "$checker" "$liar" "$out"; then echo "FAIL liar accepted"; exit 1; fi
if bash "$checker" relative "$out"; then echo "FAIL relative accepted"; exit 1; fi
echo "PASS GNU time good; liar and relative paths refused"
