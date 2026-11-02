"""Compare a NOTS sha256 list (sha256sum format, paths relative './...') with a local folder.

Usage: py -3 verify_against_local.py NOTS_LIST LOCAL_BASE [--strip PREFIX] [--add PREFIX] --out REPORT.json

For each NOTS entry, the local path is LOCAL_BASE / add / (path with strip removed).
Reports counts of match / mismatch / missing, and writes every non-match to the report.
Exit 0 only if every NOTS file has a local copy with the same sha256.
"""
import argparse, hashlib, json, os, re, sys

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

ap = argparse.ArgumentParser()
ap.add_argument('nots_list'); ap.add_argument('local_base')
ap.add_argument('--strip', default=''); ap.add_argument('--add', default='')
ap.add_argument('--out', required=True)
a = ap.parse_args()

ok = bad = miss = 0; nbytes = 0; problems = []; seen = set()
with open(a.nots_list, encoding='utf-8', errors='surrogateescape') as f:
    for line in f:
        line = line.rstrip('\n')
        if not line:
            continue
        h, rel = line[:64], line[66:]
        if not re.fullmatch(r'[0-9a-f]{64}', h) or line[64:66] != '  ' or not rel.startswith('./') or chr(92) in rel:
            sys.exit(f'malformed list line: {line!r}')
        rel = rel[2:]
        if rel in seen or any(c in ('', '.', '..') for c in rel.split('/')):
            sys.exit(f'duplicate or non-confined path: {rel!r}')
        seen.add(rel)
        if a.strip:
            if not rel.startswith(a.strip):
                problems.append({'path': rel, 'status': 'unmapped'}); miss += 1; continue
            rel = rel[len(a.strip):]
        lp = os.path.join(a.local_base, a.add, *rel.split('/'))
        if not os.path.isfile(lp):
            miss += 1; problems.append({'path': rel, 'status': 'missing'}); continue
        lh = sha(lp)
        if lh == h:
            ok += 1; nbytes += os.path.getsize(lp)
        else:
            bad += 1; problems.append({'path': rel, 'status': 'mismatch', 'nots': h, 'local': lh})
import datetime as _dt
res = {'nots_list': a.nots_list, 'nots_list_sha256': sha(a.nots_list), 'verifier_sha256': sha(__file__),
       'time_utc': _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
       'local_base': a.local_base, 'strip': a.strip, 'add': a.add,
       'match': ok, 'mismatch': bad, 'missing': miss, 'matched_bytes': nbytes,
       'verdict': 'VERIFIED' if bad == 0 and miss == 0 and ok > 0 else 'NOT_VERIFIED',
       'problems': problems[:5000], 'problems_truncated': len(problems) > 5000}
with open(a.out, 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(f"{os.path.basename(a.nots_list)}: match={ok} mismatch={bad} missing={miss} bytes={nbytes} -> {res['verdict']}")
sys.exit(0 if res['verdict'] == 'VERIFIED' else 1)
