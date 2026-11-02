#!/bin/bash
# run_remote_after.sh NOT_BEFORE_UTC OUTFILE REMOTE_SCRIPT : (laptop; detached via detach_run.sh) wait until NOT_BEFORE_UTC (e.g. the end of a
# charter back-off), then ONE ssh through the shim/lock running REMOTE_SCRIPT with `bash -s`; output to OUTFILE, then a final line ssh_rc=<rc>.
set -u
T=${1:?not_before}; OUT=${2:?outfile}; RS=${3:?remote script}
now=$(date +%s); t=$(date -d "$T" +%s) || exit 2
[ "$t" -gt "$now" ] && sleep $((t - now))
MSYS_NO_PATHCONV=1 ssh -o BatchMode=yes -o ConnectTimeout=30 nots 'bash -s' < "$RS" > "$OUT" 2>&1
echo "ssh_rc=$?" >> "$OUT"
