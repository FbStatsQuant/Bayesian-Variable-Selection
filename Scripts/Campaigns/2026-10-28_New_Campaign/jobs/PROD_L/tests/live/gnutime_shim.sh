#!/bin/bash
# local-test stand-in for GNU time (Git Bash has none): honours --version and -f FMT -o FILE CMD...; writes "wall user sys maxrss" (user/sys/rss 0/0/1)
if [ "${1:-}" = --version ]; then echo "time (GNU Time) 1.9 [local shim]"; exit 0; fi
fmt=; out=
while [ $# -gt 0 ]; do case "$1" in -f) fmt=$2; shift 2;; -o) out=$2; shift 2;; *) break;; esac; done
t0=$(date +%s.%N); rc=0; "$@" || rc=$?; t1=$(date +%s.%N)
w=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}')
printf '%s\t0.00\t0.00\t1\n' "$w" > "${out:-/dev/stderr}"
exit $rc
