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
# vsix_list_remote.sh : (NOTS, via ssh nots 'bash -s' < this) READ-ONLY listing for HQ D74 (erase ~/.vscode-server/data/CachedExtensionVSIXs).
# Prints: canonical-path check, every entry (type, size bytes, mtime, relative path), totals, sha256 of the canonical listing (LISTING_SHA, used by
# vsix_erase_remote.sh to refuse if anything changed after review), and a /proc scan of fb31's processes on this node for open fds or cwd inside it.
T=/home/fb31/.vscode-server/data/CachedExtensionVSIXs
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== target"; ls -ld "$T"; echo "realpath=$(realpath -e -- "$T")"; [ -L "$T" ] && echo "TARGET IS A SYMLINK" || echo "not a symlink"
echo "== parent"; ls -la /home/fb31/.vscode-server/data | head -20
echo "== listing (type size mtime relpath)"
L=$(cd "$T" && find . -mindepth 1 -printf '%y\t%s\t%TY-%Tm-%TdT%TH:%TM:%.2TS\t%p\n' | LC_ALL=C sort -t$'\t' -k4)
printf '%s\n' "$L"
echo "== totals"; printf '%s\n' "$L" | awk -F'\t' '{n[$1]++; b+=$2} END{for(t in n) printf "type %s: %d\n", t, n[t]; printf "bytes=%d (%.1f MiB)\n", b, b/1048576}'
echo "du_MB=$(du -x -s -m "$T" | cut -f1)"
echo "types other than f/d: $(printf '%s\n' "$L" | awk -F'\t' '$1!="f" && $1!="d"' | wc -l)"
echo "entries not owned by fb31: $(find "$T" ! -user fb31 | wc -l)"
echo "nested mounts: $( [ "$(find "$T" | wc -l)" = "$(find "$T" -xdev | wc -l)" ] && echo none || echo PRESENT)"
echo "LISTING_SHA=$(printf '%s\n' "$L" | sha256sum | cut -c1-64)"
echo "== open fds / cwd inside target (fb31 processes on this node)"
hits=0; for p in /proc/[0-9]*; do [ -O "$p" ] || continue
  for f in "$p"/fd/* "$p/cwd"; do l=$(readlink "$f" 2>/dev/null) || continue; case "$l" in "$T"|"$T"/*) echo "OPEN pid=${p#/proc/} $f -> $l"; hits=$((hits+1));; esac; done; done
echo "open_hits=$hits"
echo "done"
