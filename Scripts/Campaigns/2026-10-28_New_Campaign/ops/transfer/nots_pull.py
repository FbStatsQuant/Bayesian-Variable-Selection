"""nots_pull.py: download ONE NOTS folder, sha256-verify every file, and only then delete the remote copy.

Usage (from Git Bash or PowerShell, laptop side):
  py -3 nots_pull.py --stage                       # (re)upload remote_pack.sh + guard.sh to NOTS by scp
  py -3 nots_pull.py REMOTE_DIR [--local DEST] [--delete] [--legacy]

- REMOTE_DIR under /scratch/fb31/New_Campaign/ or /home/fb31/projects/BVS/New_Campaign/ mirrors to
  C:\\Users\\felip\\OneDrive - Rice University\\NOTS Data\\New_Campaign\\<same relative path> by default.
  Other BVS paths need --legacy and an explicit --local. Frozen benchmark paths are refused (remote side too).
- Steps: manifest (remote sha256 of every regular file) -> tar stream -> extract -> hash every local file
  -> VERIFIED only if every file matches and counts agree -> with --delete, the remote side recomputes
  its manifest and deletes only if it is byte-identical to the verified one.
- One ssh connection at a time, no retries (after a timeout: back off 15 minutes, then rerun).
- Every run is appended to ops/OPS_LOG.md; the manifest and the verification report go to ops/transfer/receipts/.
"""
import argparse, datetime as dt, hashlib, json, os, re, shlex, subprocess, sys, tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
OPS = os.path.dirname(HERE)
OPS_LOG = os.path.join(OPS, 'OPS_LOG.md')
RECEIPTS = os.path.join(HERE, 'receipts')
HOST = 'nots'
REMOTE_TOOLS = '/home/fb31/projects/BVS/New_Campaign/code/ops'
REMOTE_HELPER = REMOTE_TOOLS + '/remote_pack.sh'
LOCAL_ROOT = r'C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign'
CAMPAIGN_ROOTS = ['/scratch/fb31/New_Campaign/', '/home/fb31/projects/BVS/New_Campaign/']
# Legacy BVS folders approved for transfer-then-delete in ops/CLEANUP_PLAN.md (class A2); nothing else.
LEGACY_OK = ['/scratch/fb31/smcbvs_v3_deploy_20261022', '/projects/ml75/fb31/BVS/v3_profiling_20261020']
FROZEN = ['/projects/ml75/fb31/BVS/bench20261019', '/home/fb31/projects/BVS/Benchmarks']
SSH = ['ssh', '-o', 'BatchMode=yes', HOST]


def now():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def log(line):
    new = not os.path.exists(OPS_LOG)
    with open(OPS_LOG, 'a', encoding='utf-8') as f:
        if new:
            f.write('# OPS log (New Campaign; UTC; one line per event)\n\n')
        f.write(f'- {now()} {line}\n')
    print(line)


def die(msg, code=1):
    log(f'FAIL {msg}')
    sys.exit(code)


def lp(p):
    """Long-path-safe absolute path on Windows."""
    p = os.path.abspath(p)
    if os.name == 'nt' and not p.startswith('\\\\?\\'):
        p = '\\\\?\\' + p
    return p


def sha_file(p):
    h = hashlib.sha256()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def run(cmd, stdout=None, timeout=3600):
    return subprocess.run(cmd, stdout=stdout if stdout is not None else subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout)


def stage():
    for name, src in [('remote_pack.sh', os.path.join(HERE, 'remote_pack.sh')),
                      ('guard.sh', os.path.join(OPS, 'guard.sh'))]:
        want = sha_file(src)
        r = run(['scp', '-o', 'BatchMode=yes', '-q', src, f'{HOST}:{REMOTE_TOOLS}/{name}'])
        if r.returncode:
            die(f'stage scp {name}: {r.stderr.decode(errors="replace").strip()}')
        r = run(SSH + [f'chmod 750 {REMOTE_TOOLS}/{name} && sha256sum {REMOTE_TOOLS}/{name}'])
        got = r.stdout.decode().split()[0] if r.returncode == 0 and r.stdout else ''
        if got != want:
            die(f'stage {name}: remote sha {got} != local {want}')
        log(f'STAGE {name} -> {HOST}:{REMOTE_TOOLS}/{name} sha256={want} (verified)')


def default_local(remote):
    for root in CAMPAIGN_ROOTS:
        if remote.startswith(root):
            return os.path.join(LOCAL_ROOT, *remote[len(root):].strip('/').split('/'))
    return None


def parse_manifest(text):
    files, links, total = {}, [], None
    for line in text.splitlines():
        if line.startswith('#SYMLINK '):
            links.append(line[9:])
        elif line.startswith('#TOTAL '):
            total = dict(kv.split('=') for kv in line[7:].split())
        elif line:
            h, rel = line[:64], line[66:]
            files[rel[2:] if rel.startswith('./') else rel] = h
    return files, links, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('remote', nargs='?')
    ap.add_argument('--local')
    ap.add_argument('--delete', action='store_true')
    ap.add_argument('--legacy', action='store_true')
    ap.add_argument('--stage', action='store_true')
    a = ap.parse_args()
    if a.stage:
        stage()
        if not a.remote:
            return
    if not a.remote:
        ap.error('REMOTE_DIR required')
    remote = a.remote.replace('\\', '/').rstrip('/')
    # Git Bash (MSYS) rewrites '/scratch/...' into 'C:/Program Files/Git/scratch/...'; undo that.
    m = re.match(r'^[A-Za-z]:/(?:.*/)?Git(/(?:scratch|home|projects)/.*)$', remote)
    if m:
        remote = m.group(1)
    if not remote.startswith('/'):
        die(f'{a.remote}: REMOTE_DIR must be an absolute NOTS path', 3)
    if any(remote == f or remote.startswith(f + '/') for f in FROZEN):
        die(f'{remote}: frozen path (charter section 3), refused', 3)
    # campaign paths must sit below a scaffold subfolder (never the scaffold folders themselves)
    in_campaign = any(remote.startswith(r) and len(remote[len(r):].split('/')) >= 2 for r in CAMPAIGN_ROOTS)
    if '/./' in remote + '/' or '/../' in remote + '/' or '//' in remote:
        die(f'{remote}: non-canonical path', 3)
    if not in_campaign and not (a.legacy and remote in LEGACY_OK):
        die(f'{remote}: not an allowed transfer target (campaign: New_Campaign/<sub>/<name>; legacy: {LEGACY_OK})', 3)
    local = a.local or default_local(remote)
    if not local:
        die(f'{remote}: --local is required for legacy paths', 3)
    if os.path.exists(lp(local)) and os.listdir(lp(local)):
        die(f'{remote}: local destination {local} exists and is not empty; refusing to merge', 3)
    env = 'ALLOW_LEGACY=1 ' if a.legacy else ''
    helper = f'{env}bash {REMOTE_HELPER}'
    q = shlex.quote(remote)
    tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + remote.strip('/').replace('/', '__')
    os.makedirs(RECEIPTS, exist_ok=True)

    # 1. manifest
    r = run(SSH + [f'{helper} manifest {q}'])
    if r.returncode:
        die(f'{remote}: manifest failed rc={r.returncode}: {r.stderr.decode(errors="replace").strip()}')
    man_bytes = r.stdout
    man_sha = hashlib.sha256(man_bytes).hexdigest()
    with open(os.path.join(RECEIPTS, tag + '.manifest'), 'wb') as f:
        f.write(man_bytes)
    files, links, total = parse_manifest(man_bytes.decode('utf-8', errors='surrogateescape'))
    if total is None or int(total['files']) != len(files):
        die(f'{remote}: manifest incomplete (TOTAL line missing or count mismatch)')

    # 2. tar stream to a temporary file next to the destination
    os.makedirs(lp(local), exist_ok=True)
    tmp_tar = lp(local) + '.incoming.tar'
    with open(tmp_tar, 'wb') as out:
        r = run(SSH + [f'{helper} tar {q}'], stdout=out, timeout=6 * 3600)
    if r.returncode:
        os.remove(tmp_tar)
        if not os.listdir(lp(local)):
            os.rmdir(lp(local))
        die(f'{remote}: tar stream failed rc={r.returncode} (partial download removed; '
            f'after an ssh timeout wait 15 min): {r.stderr.decode(errors="replace").strip()}')

    # 3. extract regular files and directories only, inside the destination
    skipped = []
    root = os.path.realpath(lp(local))
    with tarfile.open(tmp_tar) as tf:
        for m in tf:
            name = m.name[2:] if m.name.startswith('./') else m.name
            if name in ('', '.'):
                continue
            dest = os.path.realpath(os.path.join(root, *name.split('/')))
            if not dest.startswith(root + os.sep):
                die(f'{remote}: unsafe tar member {m.name}')
            if m.isdir():
                os.makedirs(dest, exist_ok=True)
            elif m.isfile():
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with tf.extractfile(m) as src, open(dest, 'wb') as dst:
                    for b in iter(lambda: src.read(1 << 20), b''):
                        dst.write(b)
            else:
                skipped.append(m.name)
    os.remove(tmp_tar)

    # 4. verify every file
    ok, bad, miss = 0, [], []
    for rel, h in files.items():
        p = os.path.join(local, *rel.split('/'))
        if not os.path.isfile(lp(p)):
            miss.append(rel)
        elif sha_file(p) != h:
            bad.append(rel)
        else:
            ok += 1
    n_local = sum(len(fs) for _, _, fs in os.walk(lp(local)))
    link_names = sorted(l.split(' -> ')[0] for l in links)
    skipped_ok = sorted(skipped) == link_names      # only the manifest's symlinks may be skipped
    verified = ok == len(files) and not bad and not miss and n_local == len(files) and skipped_ok
    rep = {'remote': remote, 'local': local, 'manifest_sha256': man_sha, 'files': len(files),
           'bytes': int(total['bytes']), 'match': ok, 'mismatch': bad, 'missing': miss,
           'local_file_count': n_local, 'symlinks_not_copied': links, 'skipped_members': skipped, 'skipped_equals_manifest_symlinks': skipped_ok,
           'verdict': 'VERIFIED' if verified else 'NOT_VERIFIED', 'time': now()}
    with open(os.path.join(RECEIPTS, tag + '.verify.json'), 'w', encoding='utf-8') as f:
        json.dump(rep, f, indent=1)
    log(f'PULL {remote} -> {local} | files {ok}/{len(files)} bytes {total["bytes"]} | '
        f'mismatch {len(bad)} missing {len(miss)} local_count {n_local} symlinks {len(links)} | '
        f'{rep["verdict"]} | manifest sha256 {man_sha} | receipt transfer/receipts/{tag}.verify.json')
    if not verified:
        die(f'{remote}: not verified; remote copy kept', 1)

    # 5. delete remote only after verification, and only if unchanged since the manifest
    if a.delete:
        r = run(SSH + [f'{helper} delete {q} {man_sha}'])
        if r.returncode:
            die(f'{remote}: remote delete refused rc={r.returncode}: {r.stderr.decode(errors="replace").strip()}')
        log(f'DELETE {remote} (remote manifest re-checked = {man_sha}) | {r.stdout.decode().strip()}')


if __name__ == '__main__':
    main()
