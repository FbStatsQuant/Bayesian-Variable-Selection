#!/bin/bash
# home_detail_remote.sh : (NOTS, via ssh nots 'bash -s' < this) READ-ONLY: what is in ~/.t3 and ~/.vscode-server, and which versions running
# processes use (all login nodes' processes are not visible; this node only). No deletion, no chmod, no file content read.
cd /home/fb31 || exit 2
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== ~/.t3 (MB, depth 2)"; du -x -m --max-depth=2 .t3 2>/dev/null | sort -rn | head -20
echo "== ~/.t3/runtime/versions (MB, mtime)"; for d in .t3/runtime/versions/*; do printf '%s\t%s MB\t%s\n' "$d" "$(du -x -s -m "$d" | cut -f1)" "$(date -u -r "$d" +%FT%TZ)"; done 2>/dev/null
echo "== ~/.vscode-server (MB, depth 2)"; du -x -m --max-depth=2 .vscode-server 2>/dev/null | sort -rn | head -20
echo "== ~/.vscode-server/cli/servers (MB, mtime)"; for d in .vscode-server/cli/servers/* .vscode-server/bin/*; do [ -e "$d" ] && printf '%s\t%s MB\t%s\n' "$d" "$(du -x -s -m "$d" | cut -f1)" "$(date -u -r "$d" +%FT%TZ)"; done 2>/dev/null
echo "== fb31 processes on this node using .t3 or .vscode-server (pid, start, exe path)"
ps -u fb31 -o pid=,lstart=,args= | grep -E '\.t3/|\.vscode-server/' | grep -v grep | cut -c1-220 | head -30
echo "done"
