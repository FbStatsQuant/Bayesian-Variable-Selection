#!/bin/bash
# orphan_pack_remote.sh : (NOTS, via ssh nots 'bash -s' < this) list fb31's remote_pack.sh processes; kill, by explicit PID, only those that hash
# the PROD-L logs folder (orphans of the 16:17Z pull whose ssh was killed by nots_pull's 3600 s timeout). Nothing else is touched.
T=/scratch/fb31/New_Campaign/logs/20261030T1811Z_lowp_prodL
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== fb31 remote_pack / sha256sum / find processes"
ps -u fb31 -o pid=,ppid=,etime=,args= | grep -E 'remote_pack|sha256sum|xargs -0|find \.' | grep -v grep
PIDS=$(ps -u fb31 -o pid=,args= | grep -F "remote_pack.sh" | grep -F "$T" | grep -v grep | awk '{print $1}')
# the _inner child cds into T and runs find/xargs sha256sum: collect those descendants too
ALL=""; for p in $PIDS; do ALL="$ALL $p $(pgrep -u fb31 -P "$p" | tr '\n' ' ')"; for c in $(pgrep -u fb31 -P "$p"); do ALL="$ALL $(pgrep -u fb31 -P "$c" | tr '\n' ' ')"; done; done
ALL=$(echo $ALL | tr ' ' '\n' | sort -un | tr '\n' ' ')
if [ -n "${ALL// /}" ]; then echo "KILL (explicit PIDs, own, PROD-L logs manifest only): $ALL"; kill $ALL; sleep 2; ps -o pid=,args= -p ${ALL// /,} 2>/dev/null || true; echo "kill_done"
else echo "no orphan for $T"; fi
echo "== /tmp fb31_rp work dirs"; ls -d /tmp/fb31_rp.* 2>/dev/null | head
