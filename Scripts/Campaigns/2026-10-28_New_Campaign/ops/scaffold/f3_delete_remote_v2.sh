#!/bin/bash
# f3_delete_remote_v2.sh : (NOTS; started detached by remote_bg.sh, control lane) delete the 8 F3 dev+prod scratch folders listed in
# ops/F3_DELETION_LIST_20261102.md, each with remote_pack.sh delete <folder> <receipt transfer-manifest sha>; stop at the first failure; then
# rmdir the two empty results parents. v2 after Sol review/SOL_REVIEW_F3_DELETION_20261102.md: (blocking) D44 B3 is established with the
# fail-closed /proc scan of the D79 executor (Sol R1-R3; fd, cwd, exe, maps of every fb31 process on this node; D29 helper rule sd-pam/sshd;
# optional HQ-accepted pinned sftp-server via ACCEPT_SFTP) over the 8 targets, in addition to the empty-squeue check; (should-fix) the final
# check refuses on any remaining entry or any enumeration error. This script and its cwd are outside every target (cwd /scratch/fb31/New_Campaign).
set -uo pipefail
cd /scratch/fb31/New_Campaign || { echo "cd failed"; exit 2; }
RP=/home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh
q=$(squeue -h -u fb31 -o '%i %j %T') || { echo "squeue failed"; exit 2; }
[ -z "$q" ] || { echo "REFUSED: fb31 jobs queued/running: $q"; exit 3; }
LIST=(
"/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p0500 344d2713c11b651d1b1df3717da014f6f9f50aac5477ce3b2638ff494a324137"
"/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod/p1000 d13f0dd38bc58d07f14e8339bef8cc39d1810099951b89a49db861e8c7a77381"
"/scratch/fb31/New_Campaign/logs/20261102T1252Z_bench_f3v2_prod 4f69ac3258e85e431f2f3a0a81b0667454353747a20ecb3f3d48f3cec0a6d1e5"
"/scratch/fb31/New_Campaign/upload/20261102T1252Z_bench_f3v2_prod 17cb83e6045f0316e373106cd4da55c462c1e1e3597878dbf599b41a29f0b3fd"
"/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p0500 f79623e9c9d6f4fbaca15c2f88a8548ef573f3e9f5926fb1eb7b3d8596e2dd27"
"/scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev/p1000 f40fbe059dcfae37509e73250c79bdc37015a5fa3ed50a4a735379bc71a2a616"
"/scratch/fb31/New_Campaign/logs/20261030T1855Z_bench_f3v2_dev 2b07896a8aa3cf82abddc998d3709bc4ee97006826b7405e91767f91a6a87ae6"
"/scratch/fb31/New_Campaign/upload/20261030T1855Z_bench_f3v2_dev 171118367cd3207bc643a9886d17e528da17ee1c858be7ebeedd51dd7fdf3dfa"
)
PARENTS=(/scratch/fb31/New_Campaign/results/20261102T1252Z_bench_f3v2_prod /scratch/fb31/New_Campaign/results/20261030T1855Z_bench_f3v2_dev)
ROOTS=""; for row in "${LIST[@]}"; do ROOTS="$ROOTS${row%% *}"$'\n'; done; for p in "${PARENTS[@]}"; do ROOTS="$ROOTS$p"$'\n'; done
case "$(pwd -P)" in /scratch/fb31/New_Campaign) ;; *) echo "REFUSED: cwd $(pwd -P)"; exit 3;; esac
echo "== /proc scan (D79 executor block, unchanged) over the 8 targets + 2 parents $(date -u +%FT%TZ)"
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
for row in "${LIST[@]}"; do
  d=${row%% *}; sha=${row##* }
  echo "== $(date -u +%FT%TZ) DELETE $d"
  out=$(bash $RP delete "$d" "$sha" < /dev/null 2>&1); rc=$?
  printf '%s\n' "$out" | tail -3
  if [ $rc -ne 0 ]; then echo "STOP: delete failed for $d (rc=$rc)"; exit 4; fi
  if s=$(stat -- "$d" 2>&1); then echo "STOP: $d still exists after delete"; exit 4; fi
  case "$s" in *"No such file or directory"*) echo "deleted_rc=0 $d";; *) echo "STOP: cannot confirm absence of $d: $s"; exit 4;; esac
done
for p in "${PARENTS[@]}"; do
  if [ -d "$p" ]; then rmdir -- "$p" && echo "RMDIR $p" || { echo "STOP: $p not empty or rmdir failed: $(ls -A "$p" 2>&1 | head)"; exit 5; }; fi
done
echo "== final check: no entry left for these run IDs under results/ logs/ upload/"
left=$(find /scratch/fb31/New_Campaign/results /scratch/fb31/New_Campaign/logs /scratch/fb31/New_Campaign/upload -mindepth 1 -maxdepth 1 \( -name '*20261102T1252Z_bench_f3v2_prod*' -o -name '*20261030T1855Z_bench_f3v2_dev*' \) -print) || { echo "STOP: final enumeration failed"; exit 6; }
[ -z "$left" ] || { echo "STOP: remaining entries: $left"; exit 6; }
echo "remaining: none"
echo "F3_DELETE_DONE $(date -u +%FT%TZ)"
