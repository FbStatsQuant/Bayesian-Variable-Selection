#!/bin/bash
# home_du3_remote.sh : (NOTS, via ssh nots 'bash -s' < this) HQ D83, READ-ONLY: home growth breakdown after the D79 clean-up. Never descends into
# ~/.claude/remote or ~/.t3-recovery (excluded from du and find). No deletion, no chmod, no file content read.
H=/home/fb31; X1=$H/.claude/remote; X2=$H/.t3-recovery
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== quota"; quota -s 2>&1 | tail -2
echo "== du -x --max-depth=2 (KB, excl. .claude/remote, .t3-recovery) | sort -h | tail -25"
du -x --max-depth=2 --exclude="$X1" --exclude="$X2" -h $H 2>/dev/null | sort -h | tail -25
echo "== MB written since 2026-11-02T21:55Z by 2nd-level dir (files with mtime newer), excl. the two"
find $H -xdev \( -path "$X1" -o -path "$X2" \) -prune -o -type f -newermt '2026-11-02 21:55:00 UTC' -printf '%k %p\n' 2>/dev/null \
  | awk '{n=split($2,a,"/"); d=a[4] (n>5 ? "/" a[5] : ""); k[d]+=$1; c[d]++} END{for(d in k) printf "%8.1f MB %6d files  %s\n", k[d]/1024, c[d], d}' | sort -rn | head -20
echo "== files > 10 MB written since 21:55Z"
find $H -xdev \( -path "$X1" -o -path "$X2" \) -prune -o -type f -size +10M -newermt '2026-11-02 21:55:00 UTC' -printf '%k\t%TY-%Tm-%TdT%TH:%TM\t%p\n' 2>/dev/null | awk -F'\t' '{printf "%7.1f MB\t%s\t%s\n",$1/1024,$2,$3}' | sort -rn | head -20
echo "== campaign / F3 collection writes under home since 21:55Z (projects, ~/.cache, ~/R, ~/.local, /tmp-like dirs in home)"
find $H/projects $H/.cache $H/R $H/.local $H/tmp $H/.tmp -xdev -type f -newermt '2026-11-02 21:55:00 UTC' -printf '%k\t%p\n' 2>/dev/null | sort -rn | head -15
echo "== fb31 processes with cwd under home (excl. the two)"
for p in /proc/[0-9]*; do [ -O "$p" ] || continue; c=$(readlink "$p/cwd" 2>/dev/null) || continue; case "$c" in $X1*|$X2*) continue;; $H*) echo "pid=${p#/proc/} comm=$(cat $p/comm 2>/dev/null) cwd=$c";; esac; done | sort -t= -k4 | uniq | head -20
echo "done"
