#!/bin/bash
# home_du2_remote.sh : (NOTS, via ssh nots 'bash -s' < this) HQ D79 step 1, READ-ONLY: home usage + clean-up candidates + which T3 runtime /
# VS Code server versions fb31 processes on this node use (/proc/*/exe and /proc/*/maps). No deletion, no chmod, no file content read.
cd /home/fb31 || exit 2
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== quota"; quota -s 2>&1 | sed -n 3p
echo "== home depth 1 (MB)"; du -x -s -m .[!.]* * 2>/dev/null | sort -rn | head -20
echo "== depth 2 of the big dot-dirs (MB)"; du -x -m --max-depth=2 .vscode-server .codex .claude .t3 .cache .local .npm .yarn .config 2>/dev/null | sort -rn | head -40
echo "== ~/.cache (MB)"; du -x -s -m .cache/* .cache/.[!.]* 2>/dev/null | sort -rn | head -20
echo "== ~/.vscode-server/data (MB)"; du -x -s -m .vscode-server/data/* 2>/dev/null | sort -rn
echo "== ~/.vscode-server/cli/servers (MB, mtime)"; for d in .vscode-server/cli/servers/*/ .vscode-server/bin/*/; do [ -d "$d" ] && printf '%s\t%s MB\t%s\n' "$d" "$(du -x -s -m "$d" | cut -f1)" "$(date -u -r "$d" +%FT%TZ)"; done 2>/dev/null
echo "== ~/.vscode-server top-level code-* binaries"; ls -la .vscode-server/code-* 2>/dev/null
echo "== ~/.vscode-server/cli/servers/lru.json"; cat .vscode-server/cli/servers/lru.json 2>/dev/null; echo
echo "== ~/.t3/runtime/versions (MB, mtime)"; for d in .t3/runtime/versions/*/; do printf '%s\t%s MB\t%s\n' "$d" "$(du -x -s -m "$d" | cut -f1)" "$(date -u -r "$d" +%FT%TZ)"; done 2>/dev/null
echo "== ~/.t3 other (MB)"; du -x -m --max-depth=2 .t3 2>/dev/null | sort -rn | head -12
echo "== fb31 processes on this node: exe + mapped files under .t3/runtime/versions or .vscode-server (unreadable = listed)"
me=$(id -u)
for p in /proc/[0-9]*; do [ "$(stat -c %u "$p" 2>/dev/null)" = "$me" ] || continue; pid=${p#/proc/}
  exe=$(readlink "$p/exe" 2>/dev/null || echo "?unreadable"); comm=$(cat "$p/comm" 2>/dev/null)
  m=$(grep -oE '/home/fb31/(\.t3/runtime/versions/[^/ ]+|\.vscode-server/(cli/servers/[^/ ]+|bin/[^/ ]+|code-[0-9a-f]+|extensions/[^/ ]+))' "$p/maps" 2>/dev/null | sort -u | tr '\n' ' '); mrc=$?
  case "$exe$m" in *.t3/*|*.vscode-server/*) echo "pid=$pid comm=$comm exe=$exe maps=[$m]";; esac
  [ -r "$p/maps" ] || echo "pid=$pid comm=$comm maps UNREADABLE exe=$exe"
done
echo "== ~/.npm ~/.yarn ~/.node-gyp crash/core/tmp candidates (MB)"; du -x -s -m .npm .yarn .node-gyp .cache/yarn tmp .tmp 2>/dev/null; find /home/fb31 -xdev -maxdepth 3 \( -name 'core' -o -name 'core.[0-9]*' -o -name '*.dmp' -o -name 'crash*' \) -printf '%k KB\t%p\n' 2>/dev/null | head
echo "== growth: MB written in the last 6 h by top-level dir, and files > 20 MB written in 24 h"
find /home/fb31 -xdev -type f -mmin -360 -printf '%k %p\n' 2>/dev/null | awk '{split($2,a,"/"); k[a[4]]+=$1} END{for(d in k) printf "%d MB\t%s\n", k[d]/1024, d}' | sort -rn | head -10
find /home/fb31 -xdev -type f -size +20M -mmin -1440 -printf '%k\t%TY-%Tm-%TdT%TH:%TM\t%p\n' 2>/dev/null | awk -F'\t' '{printf "%d MB\t%s\t%s\n",$1/1024,$2,$3}' | sort -rn | head -15
echo "done"
