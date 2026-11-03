#!/bin/bash
# final_delete_remote.sh : (NOTS, via ONE direct control-lane ssh: ssh nots 'bash -s' < this, bounded 5 min; NOT via remote_bg, whose files
# live in upload/ops_bg, a target) HQ D92 final NOTS sweep: delete exactly the list in ops/FINAL_NOTS_DELETION_LIST_20261103.md.
# Archive first (verified): NOTS Data\New_Campaign\nots_home_final\ and nots_scratch_final\. Process-use guard = the D79 executor's fail-closed
# /proc scan block (byte-identical), over every target. cwd /home/fb31 (outside every target). Stops at the first failure.
set -uo pipefail
cd /home/fb31 || { echo "cd failed"; exit 2; }
[ "$(pwd -P)" = /home/fb31 ] || { echo "REFUSED: cwd"; exit 3; }
H=/home/fb31/projects/BVS/New_Campaign; SC=/scratch/fb31/New_Campaign; RP=$H/code/ops/remote_pack.sh
q=$(squeue -h -u fb31 -o '%i %j %T') || { echo "squeue failed"; exit 2; }
[ -z "$q" ] || { echo "REFUSED: fb31 jobs queued/running: $q"; exit 3; }
FOLDERS=(
"$H/jobs/CONF_NOTS_IDENTITY 1428212c068b125b0a0db857e85092614e95936cae285724ce1d8632a6b27cff"
"$H/runs/20261030T0934Z_prodH efd3abe307320ad8f3ada5f7ba8c0c577b5c2126ff4a6d52d5429718c445626b"
"$SC/upload/ops_bg d283478ec9311fec79046e9265d4db6d2e4d61eaf6ba64491962c1839b2202a6"
)
FILES=(
"$SC/README.md 89127fddaf24bfa1fa9c2a9a524abb966cd41c540a0e05cb24a064b51127b38d"
"$SC/upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt 0dc2620c0d6b741257f4ec330a9bef0a2136d998ecd73fd898817e431192dd66"
"$SC/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt 3c0e37eed340b501c9ed99730571cb45ad24a3f1d64da18b7f4befbccb7bc1f5"
"$SC/upload/cleanup_receipt_20261102T2309Z_lowp_bench.txt 4dda357f3d35f2c8482a48c65f06c65efd70d398a0db88df1228a3d6c97161e8"
"$SC/upload/prodH_bundle_20261030T0934Z.tar 845de40ef7286dee691cf3f2fc8a03ebd1408a9a0084ac982911c8e77df4e72e"
)
HOME_EMPTY_DIRS=("$H/jobs" "$H/runs" "$H/logs" "$H/results")
ROOTS="$SC"$'\n'"$H/jobs"$'\n'"$H/runs"$'\n'"$H/logs"$'\n'"$H/results"$'\n'
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== /proc scan (D79 executor block, unchanged) over: $(echo $ROOTS)"
ROOTS="$ROOTS" ACCEPT_SFTP="${ACCEPT_SFTP:-}" python3 - <<'PY' || { echo "REFUSED: proc scan (see above); nothing deleted"; exit 3; }
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
gone() { local s; if s=$(stat -- "$1" 2>&1); then return 1; fi; case "$s" in *"No such file or directory"*) return 0;; *) echo "cannot confirm absence of $1: $s"; return 2;; esac; }
for row in "${FOLDERS[@]}"; do d=${row%% *}; sha=${row##* }
  echo "== $(date -u +%FT%TZ) DELETE folder $d"
  out=$(bash $RP delete "$d" "$sha" < /dev/null 2>&1); rc=$?; printf '%s\n' "$out" | tail -2
  [ $rc -eq 0 ] && gone "$d" || { echo "STOP: folder delete failed $d (rc=$rc)"; exit 4; }
done
for row in "${FILES[@]}"; do f=${row%% *}; sha=${row##* }
  echo "== $(date -u +%FT%TZ) DELETE file $f"
  [ -f "$f" ] && [ ! -L "$f" ] && [ "$(stat -c %U -- "$f")" = fb31 ] || { echo "STOP: $f not a regular fb31 file"; exit 4; }
  h=$(sha256sum -- "$f" | cut -c1-64) || { echo "STOP: hash failed $f"; exit 4; }
  [ "$h" = "$sha" ] || { echo "STOP: $f hash $h differs from archived $sha"; exit 4; }
  rm -f -- "$f" && gone "$f" && echo "DELETED $f ($sha)" || { echo "STOP: rm failed $f"; exit 4; }
done
echo "== scratch root: must hold only empty directories now"
left=$(find $SC ! -type d -print) || { echo "STOP: find failed on $SC"; exit 5; }
[ -z "$left" ] || { echo "STOP: non-directory entries remain under $SC: $left"; exit 5; }
find $SC -depth -type d -empty -delete || { echo "STOP: empty-dir removal failed"; exit 5; }
gone $SC && echo "REMOVED $SC (was empty directories only)" || { echo "STOP: $SC still present"; exit 5; }
echo "== home: remove the now-empty run/staging directories (rmdir: only if empty)"
for d in "${HOME_EMPTY_DIRS[@]}"; do [ -d "$d" ] || continue; rmdir -- "$d" && echo "RMDIR $d" || { echo "STOP: $d not empty: $(ls -A "$d" | head)"; exit 6; }; done
echo "== final campaign home tree"; find $H -maxdepth 2 -printf '%y %p\n' | sort; du -sk $H
echo "== final check"; gone $SC && echo "scratch campaign folder: absent"
echo "FINAL_DELETE_DONE $(date -u +%FT%TZ)"
