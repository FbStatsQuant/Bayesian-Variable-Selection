"""Open every `path:line(-line)` citation in the W2-FAC-X deliverables and print the cited text (for manual confirmation).
Usage: python citecheck.py > CITECHECK.txt"""
import re, os, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
T = os.path.join(ROOT, 'Theory_work', 'Wave2', 'W2-FAC-X')
files = [os.path.join(T, f) for f in ['STATEMENT.md', 'REPORT.md', 'CHECKPOINT.md']] + sorted(glob.glob(os.path.join(T, 'lemmas', '*.md')))
pat = re.compile(r'`?([A-Za-z0-9_./\-]+\.(?:tex|md|R|py|h|cpp)):(\d+)(?:-(\d+))?`?')
PREF = ['', 'Theory_work/State_of_Project/sections/', 'Theory_work/Wave1C/FINAL/sections/', 'Theory_work/Wave1C/HQ_AUDIT/',
        'Theory_work/Wave1C/', 'Theory_work/Wave1/', 'Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1C/C-GROW/',
        'Theory_work/Wave2/W2-FAC-X/', 'Theory_work/Wave2/W2-FAC-B/', 'Theory_work/Wave2/W2-FAC-B/lemmas/', 'Theory_work/Wave2/W2-FAC-X/lemmas/', 'Theory_work/']
def resolve(path):
    for pre in PREF:
        f = os.path.join(ROOT, pre + path)
        if os.path.isfile(f): return f
    return None
ok = miss = 0
for fn in files:
    if not os.path.isfile(fn): continue
    text = open(fn, encoding='utf-8').read()
    for m in pat.finditer(text):
        path, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        f = resolve(path); rel = os.path.relpath(fn, T)
        if f is None: print(f'MISS  [{rel}] {path}:{a}-{b} (file not found)'); miss += 1; continue
        L = open(f, encoding='utf-8', errors='replace').read().splitlines()
        if b > len(L): print(f'MISS  [{rel}] {path}:{a}-{b} (file has {len(L)} lines)'); miss += 1; continue
        print(f'OK    [{rel}] {path}:{a}-{b}\n      ' + ' | '.join(l.strip()[:170] for l in L[a-1:min(b, a+3)])); ok += 1
print(f'\nTOTAL ok={ok} miss={miss}')
