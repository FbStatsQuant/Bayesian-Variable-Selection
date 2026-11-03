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
#!/bin/bash
# home_du_remote.sh : (NOTS, via ssh nots 'bash -s' < this) READ-ONLY home usage breakdown after the 17:28Z guard refusal (home 9.86 GB).
# No deletion, no chmod. Reads only sizes and names (du/ls/find -printf); the frozen benchmark tree is read, never changed.
cd /home/fb31 || exit 2
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== quota"; quota -s 2>&1 | tail -3
echo "== top level (MB, incl. hidden)"; du -x -s -m .[!.]* * 2>/dev/null | sort -rn | head -25
echo "== ~/.codex (MB)"; du -x -s -m .codex/* .codex/.[!.]* 2>/dev/null | sort -rn | head -15
echo "== ~/.codex/db-backups: count, newest 5, size"; ls -1 .codex/db-backups 2>/dev/null | wc -l; ls -1t .codex/db-backups 2>/dev/null | head -5; du -x -s -m .codex/db-backups 2>/dev/null
echo "== files > 50 MB modified in the last 24 h (path, MB, mtime)"
find /home/fb31 -xdev -type f -size +50M -mmin -1440 -printf '%p\t%k\t%TY-%Tm-%TdT%TH:%TM\n' 2>/dev/null | awk -F'\t' '{printf "%s\t%d MB\t%s\n",$1,$2/1024,$3}' | sort -t$'\t' -k2 -rn | head -20
echo "== MB written in the last 24 h by top-level dir"
find /home/fb31 -xdev -type f -mmin -1440 -printf '%k %p\n' 2>/dev/null | awk '{split($2,a,"/"); k[a[4]]+=$1} END{for(d in k) printf "%d MB\t%s\n", k[d]/1024, d}' | sort -rn | head -15
echo "done"
