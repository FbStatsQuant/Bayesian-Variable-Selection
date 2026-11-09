"""Open every `path:line(-line)` citation in the C-GROW deliverables and print the cited text (for manual confirmation).
Usage: py -3.13 citecheck.py > CITECHECK.txt  (run from the repo root or anywhere)."""
import re, os, glob, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
CG = os.path.join(ROOT, 'Theory_work', 'Wave1C', 'C-GROW')
ALIASES = {'SoP ': 'Theory_work/State_of_Project/sections/', 'GEN/': 'Theory_work/Wave1/W1-GEN/',
           'T37R': 'Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T37R/PROOF.md'}
files = [os.path.join(CG, f) for f in ['STATEMENT.md', 'REPORT.md', 'METHOD_REQUIREMENTS.md']] + sorted(glob.glob(os.path.join(CG, 'lemmas', '*.md')))
pat = re.compile(r'(?:SoP\s+)?`?([A-Za-z0-9_./\-]+\.(?:tex|md|R|py|h|cpp)):(\d+)(?:-(\d+))?`?')
def resolve(path, ctx):
    cands = [path, 'Theory_work/State_of_Project/sections/' + path, 'Theory_work/Wave1/W1-GEN/' + path.replace('GEN/', ''),
             'Theory_work/Wave1C/C-GROW/' + path, 'Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/' + path]
    for c in cands:
        f = os.path.join(ROOT, c)
        if os.path.isfile(f):
            return f
    return None
n_ok = n_miss = 0
for fn in files:
    if not os.path.isfile(fn):
        continue
    text = open(fn, encoding='utf-8').read()
    for m in pat.finditer(text):
        path, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        f = resolve(path, fn)
        rel = os.path.relpath(fn, CG)
        if f is None:
            print(f'MISS  [{rel}] {path}:{a}-{b}  (file not found)'); n_miss += 1; continue
        lines = open(f, encoding='utf-8', errors='replace').read().splitlines()
        if b > len(lines):
            print(f'MISS  [{rel}] {path}:{a}-{b}  (file has {len(lines)} lines)'); n_miss += 1; continue
        snippet = ' | '.join(l.strip()[:160] for l in lines[a-1:min(b, a+2)])
        print(f'OK    [{rel}] {path}:{a}-{b}\n      {snippet}'); n_ok += 1
print(f'\nTOTAL ok={n_ok} miss={n_miss}')
