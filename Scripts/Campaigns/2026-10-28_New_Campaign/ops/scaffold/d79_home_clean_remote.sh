#!/bin/bash
# d79_home_clean_remote.sh R2 : (NOTS; started detached by remote_bg.sh) HQ D79 home clean-up (Felipe: "start cleaning what you can, maybe cache
# or something, up to you"). MODE=list : READ-ONLY listing of the exact items below (per-item counts, bytes, listing sha) + combined LIST_SHA +
# mount-table check + fail-closed /proc scan (fd, cwd, exe, maps of every fb31 process on this node). MODE=erase EXPECT_SHA=<LIST_SHA of the
# reviewed list run> : recompute everything, refuse on any difference, failure or reference into an item, then delete each item anchored in its
# parent directory. No archive (D79: caches and program installs are regenerable). Never touched: ~/.claude/remote, ~/.t3-recovery, ~/.t3 other
# than runtime/versions/0.1.6, credentials/config, ~/projects, campaign folders, the live VS Code server Stable-2c33b50… and Stable-e646868…
# (its CLI code-e646868… is the running agent host), ~/.cache/Microsoft and ~/.cache/copilot (possible auth tokens).
# Executor lineage: D74 vsix_erase_remote.sh R4 (Sol rounds 1-3) + the D29-accepted non-dumpable helper rule (sd-pam / sshd).
# R2 after Sol review/SOL_REVIEW_D79_HOME_CLEAN.md: (1) the sftp-server exemption is OFF unless ACCEPT_SFTP=<pid>:<starttime> names exactly one
# process (HQ decision), with byte-exact cmdline + ancestry; for every helper the readable checks (cwd, exe, maps) are still made, only EACCES on
# them is tolerated; (2) final enumeration status checked, absent vs inaccessible distinguished; (3) mountinfo check for mounts at or under any
# item (refuse if mountinfo unreadable), listing pipelines under pipefail with status checked; (4) D29 lifetime discipline: start time recorded
# per pid and re-checked after its scan, ENOENT on fd dir/maps of a still-live non-zombie process refuses; (5) MODE validated; exact fb31 owner.
# R3 after Sol round 2: every listing safety summary from a status-checked assignment (LISTFAIL on failure, nothing computed inside echo); the
# mount parser is one awk with its status and record count guarded; LIST_SHA format checked; /proc/<pid>/stat read errors other than
# ENOENT/ESRCH refuse (unreadable is no longer treated as gone). HQ accepted the pinned sftp-server helper under D79 (2026-11-02 watchdog).
set -u
set -o pipefail
MODE=${MODE:?MODE=list|erase}
case "$MODE" in list|erase) ;; *) echo "REFUSED: MODE must be list or erase (nothing deleted)"; exit 3;; esac
H=/home/fb31
# ITEMS: "<parent>|<name>|<kind>" ; kind entry = remove ./name (file or tree); contents = remove everything inside ./name, keep the directory
ITEMS=(
  "$H/.cache|pip|entry"
  "$H/.cache|matplotlib|entry"
  "$H/.vscode-server/data|CachedExtensionVSIXs|contents"
  "$H/.t3/runtime/versions|0.1.6|entry"
  "$H/.vscode-server/cli/servers|Stable-6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1|entry"
  "$H/.vscode-server/cli/servers|Stable-2d0b7506a36c1d6db9a466440131a8e01eab2289|entry"
  "$H/.vscode-server/cli/servers|Stable-585eba7c0c34fd6b30faac7c62a42050bfbc0086|entry"
  "$H/.vscode-server|code-6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1|entry"
  "$H/.vscode-server|code-2d0b7506a36c1d6db9a466440131a8e01eab2289|entry"
  "$H/.vscode-server|code-585eba7c0c34fd6b30faac7c62a42050bfbc0086|entry"
)
refuse() { echo "REFUSED: $1 (nothing deleted)"; exit 3; }
echo "date=$(date -u +%FT%TZ) host=$(hostname) MODE=$MODE ACCEPT_SFTP=${ACCEPT_SFTP:-none}"
[ "$(id -un)" = fb31 ] && [ "$(id -u)" = "$(stat -c %u $H)" ] || refuse "not running as fb31"
# ---- listing (identical in both modes). Any failed command marks the item LISTFAIL. ----
listing() {
  local spec par name kind t lf
  lf=$(mktemp /tmp/fb31_d79.XXXXXX) || { echo "LISTFAIL mktemp"; return; }
  for spec in "${ITEMS[@]}"; do IFS='|' read -r par name kind <<< "$spec"
    [ -d "$par" ] && [ ! -L "$par" ] && [ "$(realpath -e -- "$par")" = "$par" ] || { echo "ITEM $par/$name BADPARENT"; continue; }
    t="$par/$name"
    if ! st=$(stat -c '%F|%d:%i|%U|%u' -- "$t" 2>&1); then
      case "$st" in *"No such file or directory"*) echo "ITEM $t ABSENT";; *) echo "ITEM $t LISTFAIL stat: $st";; esac; continue; fi
    [ -L "$t" ] && { echo "ITEM $t SYMLINK"; continue; }
    IFS='|' read -r ft di ow ou <<< "$st"
    echo "ITEM $t kind=$kind type=$ft dev_ino=$di owner=$ow uid=$ou"
    if [ -d "$t" ]; then
      if ! ( cd -- "$t" && find . -mindepth 1 -printf '%y\t%s\t%T@\t%u\t%p\n' | LC_ALL=C sort -t$'\t' -k5 ) > "$lf"; then echo "  LISTFAIL find"; continue; fi
      # R3: every safety summary from one status-checked assignment (no command substitution inside echo)
      if ! sums=$(awk -F'\t' '{if($1=="f")f++; else if($1=="d")d++; else o++; if($4!="fb31")u++; b+=$2} END{printf "files=%d dirs=%d other=%d notfb31=%d bytes=%d", f, d, o, u, b}' "$lf"); then echo "  LISTFAIL summary"; continue; fi
      if ! lsha=$(sha256sum < "$lf"); then echo "  LISTFAIL sha"; continue; fi
      lsha=${lsha:0:64}; [[ "$lsha" =~ ^[0-9a-f]{64}$ ]] || { echo "  LISTFAIL sha format"; continue; }
      echo "  $sums list_sha=$lsha"
    else
      if ! fm=$(stat -c 'bytes=%s mtime=%Y' -- "$t"); then echo "  LISTFAIL stat file"; continue; fi
      echo "  file $fm"
    fi
  done
  rm -f "$lf"
}
L=$(listing)
printf '%s\n' "$L"
SHA=$(printf '%s\n' "$L" | sha256sum | cut -c1-64) && [[ "$SHA" =~ ^[0-9a-f]{64}$ ]] || refuse "LIST_SHA computation failed"
echo "LIST_SHA=$SHA"
echo "items_total_MB=$(printf '%s\n' "$L" | grep -oE 'bytes=[0-9]+' | cut -d= -f2 | awk '{b+=$1} END{printf "%.1f", b/1048576}')"
printf '%s\n' "$L" | grep -qE 'BADPARENT|SYMLINK|LISTFAIL|notfb31=[1-9]|other=[1-9]' && refuse "an item failed a structural check (see above)"
printf '%s\n' "$L" | grep '^ITEM ' | grep -v ' ABSENT$' | grep -vE ' owner=fb31 uid=[0-9]+$' | grep -q . && refuse "an item is not owned by fb31"
printf '%s\n' "$L" | grep -oE ' uid=[0-9]+$' | grep -v " uid=$(id -u)\$" | grep -q . && refuse "an item uid differs from fb31's uid"
# ---- mount check: no mount point at or under any item (bind mounts included); mountinfo must be readable ----
ROOTS=""; for spec in "${ITEMS[@]}"; do IFS='|' read -r par name kind <<< "$spec"; ROOTS="$ROOTS$par/$name"$'\n'; done
MI=$(cat /proc/self/mountinfo) || refuse "cannot read /proc/self/mountinfo"
[ -n "$MI" ] || refuse "empty mountinfo"
# R3: one awk, status guarded (pipefail): a parser failure refuses instead of yielding an empty "no mounts" result
bad=$(printf '%s\n' "$MI" | awk -v roots="$ROOTS" 'BEGIN{n=split(roots,R,"\n")} {mp=$5; gsub(/\\040/," ",mp); for(i=1;i<=n;i++) if(R[i]!="" && (mp==R[i] || index(mp,R[i] "/")==1)) print mp} END{print "PARSED " NR}') || refuse "mount parser failed"
# R3.1 (Sol round 3): the COMPLETE parser output must be exactly "PARSED <n>", n >= 1; any mount line or anomaly refuses
[[ "$bad" =~ ^PARSED\ [1-9][0-9]*$ ]] || refuse "mount check: mount point(s) at or under an item, or parser anomaly: [$bad]"
echo "mount_check: no mount point at or under any item ($(printf '%s\n' "$MI" | wc -l) mounts checked)"
# ---- fail-closed /proc scan: fd, cwd, exe, maps of every fb31 process ----
ROOTS="$ROOTS" ACCEPT_SFTP="${ACCEPT_SFTP:-}" python3 - <<'PY' || refuse "proc scan refused (see above)"
import errno, os, pwd, sys
roots = [r for r in os.environ['ROOTS'].split('\n') if r]
accept_sftp = os.environ.get('ACCEPT_SFTP', '')          # "<pid>:<starttime>" or empty (exemption off)
me = os.getuid(); GONE = (errno.ENOENT, errno.ESRCH)
def hit(p): return any(p == r or p.startswith(r + '/') for r in roots)
def rdb(path):
    try:
        with open(path, 'rb') as f: return f.read()
    except OSError: return None
def rd(path):
    b = rdb(path); return None if b is None else b.decode(errors='replace')
def stat_fields(pid):
    """R3: None ONLY when the process is gone (ENOENT/ESRCH); any other read error is a fail-closed refusal."""
    try:
        with open(f'/proc/{pid}/stat', 'rb') as fh: s = fh.read().decode(errors='replace')
    except OSError as e:
        if e.errno in GONE: return None
        print(f"SCAN INCOMPLETE /proc/{pid}/stat: {e}"); sys.exit(1)
    rest = s.rsplit(')', 1)[1].split()
    return {'state': rest[0], 'ppid': rest[1], 'start': rest[19]}
def owner(pid):
    try: return pwd.getpwuid(os.stat(f'/proc/{pid}').st_uid).pw_name
    except (OSError, KeyError): return None
def comm(pid): return (rd(f'/proc/{pid}/comm') or '').strip()
def helper(pid, t0):
    """Exact identity of a tolerated non-dumpable helper (D29 rule + HQ-accepted sftp pid), else None. Evaluated once per pid."""
    f = stat_fields(pid)
    if f is None or f['start'] != t0: return None
    c = comm(pid); pp = f['ppid']; fp = stat_fields(pp)
    if fp is None: return None
    pc = comm(pp); pu = owner(pp); gpp = fp['ppid']
    if c == 'sshd' and pc == 'sshd' and pu == 'root': return f'comm=sshd parent={pp}(sshd,root)'
    if c == '(sd-pam)' and pc == 'systemd' and pu == 'fb31' and gpp == '1': return f'comm=(sd-pam) parent={pp}(systemd,fb31) grandparent=1'
    if c == 'sftp-server' and accept_sftp == f'{pid}:{t0}' and rdb(f'/proc/{pid}/cmdline') == b'/usr/libexec/openssh/sftp-server\0' \
       and pc == 'sshd' and pu == 'fb31' and comm(gpp) == 'sshd' and owner(gpp) == 'root':
        return f'comm=sftp-server pid:start={pid}:{t0} (HQ-accepted) parent={pp}(sshd,fb31) grandparent={gpp}(sshd,root)'
    return None
def alive_same(pid, t0):
    f = stat_fields(pid); return f is not None and f['start'] == t0 and f['state'] != 'Z'
scanned = helpers = 0
for name in os.listdir('/proc'):
    if not name.isdigit(): continue
    p = '/proc/' + name
    try: st = os.stat(p)
    except OSError as e:
        if e.errno in GONE: continue
        print(f"SCAN ERROR stat {p}: {e}"); sys.exit(1)
    if st.st_uid != me: continue
    f0 = stat_fields(name)
    if f0 is None:
        if os.path.exists(p): print(f"SCAN INCOMPLETE {p}/stat unreadable"); sys.exit(1)
        continue
    t0 = f0['start']
    if f0['state'] == 'Z': continue                                   # zombie: holds no files
    hdesc = None; links = []
    try: links = [p + '/fd/' + x for x in os.listdir(p + '/fd')]
    except OSError as e:
        if e.errno in GONE:
            if alive_same(name, t0): print(f"SCAN INCOMPLETE {p}/fd vanished for a live process"); sys.exit(1)
            continue
        if e.errno == errno.EACCES: hdesc = helper(name, t0)
        if not hdesc: print(f"SCAN INCOMPLETE pid {name}: cannot list fd: {e}; comm={comm(name)}"); sys.exit(1)
    for q in links + [p + '/cwd', p + '/exe']:
        try: l = os.readlink(q)
        except OSError as e:
            if e.errno in GONE and q not in (p + '/cwd', p + '/exe'): continue          # an individual fd closed during the scan
            if e.errno in GONE and not alive_same(name, t0): break                      # the process exited
            if e.errno == errno.EACCES and hdesc: continue                              # helper: unreadable link tolerated
            if e.errno == errno.ENOENT and q == p + '/exe' and alive_same(name, t0): continue   # kernel thread / exe unlinked: no path
            print(f"SCAN INCOMPLETE {q}: {e}"); sys.exit(1)
        if hit(l.replace(' (deleted)', '')): print(f"OPEN pid {name} {q} -> {l}"); sys.exit(1)
    m = None
    try:
        with open(p + '/maps') as fh: m = fh.read()
    except OSError as e:
        if e.errno in GONE:
            if alive_same(name, t0): print(f"SCAN INCOMPLETE {p}/maps vanished for a live process"); sys.exit(1)
            continue
        if not (e.errno == errno.EACCES and hdesc): print(f"SCAN INCOMPLETE {p}/maps: {e}"); sys.exit(1)
    for line in (m or '').splitlines():
        parts = line.split(None, 5)
        if len(parts) == 6 and hit(parts[5].replace(' (deleted)', '').strip()): print(f"MAPPED pid {name} -> {parts[5].strip()}"); sys.exit(1)
    f1 = stat_fields(name)
    if f1 is not None and f1['start'] != t0: print(f"SCAN INCOMPLETE pid {name} replaced during its scan"); sys.exit(1)
    if hdesc: print(f"proc_scan: helper pid={name} ({hdesc}); readable links/maps checked, unreadable tolerated"); helpers += 1
    scanned += 1
print(f"proc_scan: fb31 processes scanned={scanned} (of which tolerated helpers={helpers}) references=0 incomplete=0")
PY
echo "== du before"; du -x -s -m $H 2>/dev/null
[ "$MODE" = list ] && { echo "LIST DONE"; exit 0; }
# ---- erase ----
: "${EXPECT_SHA:?EXPECT_SHA required for erase}"
[ "$SHA" = "$EXPECT_SHA" ] || refuse "LIST_SHA $SHA differs from reviewed $EXPECT_SHA"
rc=0
for spec in "${ITEMS[@]}"; do IFS='|' read -r par name kind <<< "$spec"; t="$par/$name"
  if printf '%s\n' "$L" | grep -qxF "ITEM $t ABSENT"; then echo "SKIP absent at listing $t"; continue; fi
  di=$(printf '%s\n' "$L" | awk -v t="ITEM $t " 'index($0,t)==1 {for(i=1;i<=NF;i++) if ($i ~ /^dev_ino=/) {sub("dev_ino=","",$i); print $i}}')
  [ -n "$di" ] || { echo "FAILED $t: no listed dev_ino"; rc=1; continue; }
  ( cd -- "$par" || exit 5; [ "$(pwd -P)" = "$par" ] || exit 6
    [ "$(stat -c %d:%i -- "./$name")" = "$di" ] || exit 7
    if [ "$kind" = contents ]; then cd -- "./$name" || exit 5; [ "$(pwd -P)" = "$t" ] || exit 6
      find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + || exit 8
      left=$(find . -mindepth 1 -print -quit) || exit 10; [ -z "$left" ] || exit 9
    else rm -rf -- "./$name" || exit 8
      if s=$(stat -- "./$name" 2>&1); then exit 9; else case "$s" in *"No such file or directory"*) ;; *) exit 10;; esac; fi
    fi ); r=$?
  [ $r = 0 ] && echo "ERASED $t ($kind)" || { echo "FAILED $t ($kind) rc=$r"; rc=1; }
done
echo "== du after"; du -x -s -m $H 2>/dev/null
if [ $rc = 0 ]; then echo "ERASE VERIFIED"; exit 0; else echo "ERASE INCOMPLETE"; exit 1; fi
