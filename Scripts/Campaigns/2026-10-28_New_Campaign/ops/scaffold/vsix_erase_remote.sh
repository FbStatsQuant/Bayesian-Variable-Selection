#!/bin/bash
# vsix_erase_remote.sh : (NOTS, via ssh nots "EXPECT_SHA=<sha> bash -s" < this) HQ D74 option A: erase the 4 cached VSIX files listed at
# 2026-11-02T17:34:24Z (ops/evidence/ops_d74_vsix_list_20261102.txt, LISTING_SHA c708bf06…b2e5) in ~/.vscode-server/data/CachedExtensionVSIXs.
# No archive (HQ D74: regenerable cache). Deletes exactly those 4 regular files by name; keeps the directory; touches nothing else.
# Refuses (no deletion, exit 3) if: not running as fb31; the target is not the canonical non-symlink directory; the anchored directory's
# dev:inode changes across the listing; the listing (same command as the reviewed listing) differs; any entry is not a regular fb31 file;
# the /proc scan (python3, errno-aware) finds an fd or cwd inside the target, or meets any error other than "process/fd vanished" (ENOENT/ESRCH)
# on a fb31-owned process (permission denial is NOT treated as disappearance). Deletion is anchored to the validated directory (cd + pwd -P +
# dev:inode, relative ./name operands). Exit 0 only on ERASE VERIFIED (successful final enumeration with zero entries).
# R3 (2026-11-02) after Sol rounds 1-2 (review/SOL_REVIEW_D74_VSIX_ERASE.md).
set -u
: "${EXPECT_SHA:?EXPECT_SHA required}"
T=/home/fb31/.vscode-server/data/CachedExtensionVSIXs
NAMES=(anthropic.claude-code-2.1.312-linux-x64 github.copilot-chat-0.48.1 openai.chatgpt-26.51021.22027-linux-x64 openai.codex-audio-26.1021.22027)
refuse() { echo "REFUSED: $1 (nothing deleted)"; exit 3; }
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
[ "$(id -un)" = fb31 ] && [ "$(id -u)" = "$(stat -c %u /home/fb31)" ] || refuse "not running as fb31 (id -un=$(id -un))"
[ -d "$T" ] && [ ! -L "$T" ] || refuse "target missing or a symlink"
[ "$(realpath -e -- "$T")" = "$T" ] || refuse "target is not canonical"
cd -- "$T" || refuse "cd failed"
[ "$(pwd -P)" = "$T" ] || refuse "cwd resolves to $(pwd -P), not $T"
I0=$(stat -c %d:%i .) || refuse "stat of anchored dir failed"
L=$(cd "$T" && find . -mindepth 1 -printf '%y\t%s\t%TY-%Tm-%TdT%TH:%TM:%.2TS\t%p\n' | LC_ALL=C sort -t$'\t' -k4)
I1=$(stat -c %d:%i "$T") || refuse "stat of target failed"
[ "$I0" = "$I1" ] || refuse "target directory identity changed during listing ($I0 -> $I1)"
SHA=$(printf '%s\n' "$L" | sha256sum | cut -c1-64)
echo "anchored_dir=$I0 listing_sha=$SHA expected=$EXPECT_SHA"
[ "$SHA" = "$EXPECT_SHA" ] || { printf '%s\n' "$L"; refuse "listing changed since review"; }
[ "$(printf '%s\n' "$L" | wc -l)" = 4 ] || refuse "entry count is not 4"
for n in "${NAMES[@]}"; do [ -f "./$n" ] && [ ! -L "./$n" ] && [ "$(stat -c %U -- "./$n")" = fb31 ] || refuse "$n is not a regular fb31 file"; done
# errno-aware, fail-closed scan of every process on this node owned by our uid
T="$T" python3 - <<'PY' || refuse "proc scan refused (see above)"
import errno, os, sys
T = os.environ['T']; me = os.getuid(); self_pids = {os.getpid(), os.getppid()}
GONE = (errno.ENOENT, errno.ESRCH)
def inside(l): return l == T or l.startswith(T + '/')
def rd(path):
    try:
        with open(path) as f: return f.read().strip()
    except OSError: return None
def ppid(pid):
    s = rd(f'/proc/{pid}/status')
    if s is None: return None
    for line in s.splitlines():
        if line.startswith('PPid:'): return line.split()[1]
    return None
def start(pid):
    s = rd(f'/proc/{pid}/stat')
    return None if s is None else s.rsplit(')', 1)[1].split()[19]
def owner(pid):
    try:
        import pwd; return pwd.getpwuid(os.stat(f'/proc/{pid}').st_uid).pw_name
    except (OSError, KeyError): return None
def helper(pid):
    """Return a description if pid is exactly one of the D29-accepted non-dumpable helpers, else None."""
    t0 = start(pid); c = rd(f'/proc/{pid}/comm'); pp = ppid(pid)
    if None in (t0, c, pp): return None
    pc = rd(f'/proc/{pp}/comm'); pu = owner(pp); gpp = ppid(pp)
    desc = None
    if c == 'sshd' and pc == 'sshd' and pu == 'root':
        desc = f'comm=sshd parent={pp}(sshd,root)'
    elif c == '(sd-pam)' and pc == 'systemd' and pu == 'fb31' and gpp == '1':
        desc = f'comm=(sd-pam) parent={pp}(systemd,fb31) grandparent=1'
    if desc and start(pid) == t0: return desc
    return None
scanned = 0
for name in os.listdir('/proc'):
    if not name.isdigit(): continue
    p = '/proc/' + name
    try: st = os.stat(p)
    except OSError as e:
        if e.errno in GONE: continue
        print(f"SCAN ERROR stat {p}: {e}"); sys.exit(1)
    if st.st_uid != me: continue
    try: fds = os.listdir(p + '/fd')
    except OSError as e:
        if e.errno in GONE: continue
        # R4: the two strictly identified non-dumpable helpers already accepted in the D29 executor (Sol R5, HQ D34;
        # ops/scaffold/d29_dbbackups_delete.sh:118-120,161-167) are skipped, logged, on EACCES only, with an unchanged start time;
        # every other unreadable live process still refuses.
        if e.errno == errno.EACCES and helper(name):
            print(f"proc_scan: skipped helper pid={name} ({helper(name)})"); scanned += 1; continue
        print(f"SCAN INCOMPLETE pid {name}: cannot list fd: {e}; comm: {rd(p + '/comm')}"); sys.exit(1)
    # cwd is checked for every process except this scanner and its parent shell, whose cwd is the anchored target by design (R3 fix);
    # their open fds are still checked
    for fd in fds + ([] if int(name) in self_pids else [None]):
        q = p + '/cwd' if fd is None else p + '/fd/' + fd
        try: l = os.readlink(q)
        except OSError as e:
            if e.errno in GONE: continue
            print(f"SCAN INCOMPLETE {q}: {e}"); sys.exit(1)
        if inside(l):
            print(f"OPEN pid {name} {q} -> {l}"); sys.exit(1)
    scanned += 1
print(f"proc_scan: uid {me} processes scanned={scanned}, open_hits=0, incomplete=0")
PY
[ "$(stat -c %d:%i .)" = "$I0" ] && [ "$(pwd -P)" = "$T" ] || refuse "anchored directory changed before deletion"
echo "before: du_MB=$(du -x -s -m . | cut -f1)"; quota -s 2>&1 | sed -n 3p
rc=0; for n in "${NAMES[@]}"; do rm -f -- "./$n" && [ ! -e "./$n" ] && echo "ERASED $T/$n" || { echo "FAILED $T/$n"; rc=1; }; done
if out=$(find . -mindepth 1 2>&1); then enum_ok=1; else enum_ok=0; fi
cd /home/fb31 || true
echo "after: enumeration_ok=$enum_ok remaining=[${out}] du_MB=$(du -x -s -m "$T" | cut -f1)"; ls -ld "$T"; quota -s 2>&1 | sed -n 3p
if [ $rc = 0 ] && [ $enum_ok = 1 ] && [ -z "$out" ]; then echo "ERASE VERIFIED"; exit 0; else echo "ERASE INCOMPLETE"; exit 1; fi
