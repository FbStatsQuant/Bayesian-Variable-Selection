#!/bin/bash
# pilot_submit_remote.sh (runs ON NOTS via: ssh nots "STAMP=<STAMP> TAR_SHA=<sha> bash -s" < this). LOWP pilot JOB.md rev 7c: unpack, verify, fill pilot.env, submit.
# One connection. Every gate prints GATE <name> OK|FAIL; the first FAIL stops before submission.
set -uo pipefail
: "${STAMP:?}"; : "${TAR_SHA:?}"
PID="${STAMP}_lowp_pilot"
HOME_ROOT=/home/fb31/projects/BVS/New_Campaign
SCR=/scratch/fb31/New_Campaign
TAR=$SCR/runs/pilot_bundle_$STAMP.tar
stop() { echo "GATE $1 FAIL: $2"; echo "NOT SUBMITTED"; exit 1; }
echo "date=$(date -u +%FT%TZ) host=$(hostname) STAMP=$STAMP"

echo "== squeue (our jobs)"; Q=$(squeue -u fb31 -h -o '%i %j %T') || stop squeue "squeue failed"
printf '%s\n' "$Q"
printf '%s\n' "$Q" | grep -q 'lowp_p' && stop squeue "a lowp_p* job already exists: never submit twice"
[ ! -e "$HOME_ROOT/runs/$PID" ] || stop fresh "runs/$PID already exists in home"
[ ! -e "$SCR/logs/$PID" ] || stop fresh "logs/$PID already exists in scratch"
echo "GATE squeue+fresh OK"

V=$(/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time --version 2>&1 | head -1)
echo "time --version: $V"
[ "$V" = "time (GNU Time) 1.9" ] || stop gnu_time "unexpected: $V"
echo "GATE gnu_time OK"

G=$(bash "$HOME_ROOT/code/ops/guard.sh" 30 2>&1); grc=$?
echo "GUARDLINE $G | rc=$grc"
[ $grc -eq 0 ] || stop guard "guard refused (rc=$grc)"
echo "GATE guard OK"

[ "$(sha256sum "$TAR" | cut -c1-64)" = "$TAR_SHA" ] || stop tar_sha "uploaded tar hash differs"
cd "$HOME_ROOT" || stop cd "cd home root"
test ! -e "runs/$PID" && tar -xf "$TAR" -C . && sha256sum --quiet -c "runs/$PID/STAGED_SHA256.txt" && rm -- "$TAR" || stop unpack "extract/verify failed"
echo "GATE unpack+STAGED_SHA256 OK ($(wc -l < "runs/$PID/STAGED_SHA256.txt") files); tar removed from scratch"

E="runs/$PID/code/lowp/pilot/pilot.env"
sed -i 's#^MODULES=""$#MODULES="GCC/14.3.0 R/4.5.2"#; s#^R_LIBS_USER_LOWP=""$#R_LIBS_USER_LOWP="/opt/apps/software/R/4.5.2-gfbf-2025b/lib64/R/library"#; s#^MODULES_BENCH=""$#MODULES_BENCH="GCC/14.3.0 R/4.5.2"#' "$E" || stop pilot_env "sed failed"
grep -E '^(MODULES|R_LIBS_LOWP|R_LIBS_USER_LOWP|MODULES_BENCH|R_LIBS_BENCH|R_LIBS_USER_BENCH)=' "$E"
[ "$(grep -c '^MODULES="GCC/14.3.0 R/4.5.2"$' "$E")" = 1 ] && [ "$(grep -c '^MODULES_BENCH="GCC/14.3.0 R/4.5.2"$' "$E")" = 1 ] || stop pilot_env "MODULES not filled as intended"
echo "GATE pilot_env OK sha256=$(sha256sum "$E" | cut -c1-64)"

echo "== submit_pilot.sh"
cd "$HOME_ROOT/runs/$PID/code/lowp/pilot" || stop cd "cd pilot dir"
STAMP=$STAMP bash submit_pilot.sh < /dev/null; src=$?
echo "submit_rc=$src"
echo "== JOBIDS.tsv"; cat "$HOME_ROOT/runs/$PID/JOBIDS.tsv" 2>&1
echo "== squeue after"; squeue -u fb31 -o '%i %j %T %R' 2>&1 | head -40
