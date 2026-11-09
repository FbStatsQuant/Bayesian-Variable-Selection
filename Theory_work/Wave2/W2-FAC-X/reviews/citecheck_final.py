"""Final citation check for W2-FAC-X (successor lead, 2026-11-09).
(1) Opens every `path:line(-line)` citation in STATEMENT.md, STATEMENT_T2.md, REPORT.md, CHECKPOINT.md, lemmas/*.md, T2/*.md
    and prints the cited lines (OK) or MISS.
(2) Confirms that every verbatim status string quoted in the deliverables occurs in its source file.
(3) Confirms that every review file named in REPORT.md exists.
Usage: python citecheck_final.py > CITECHECK_FINAL.txt"""
import re, os, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
T = os.path.join(ROOT, 'Theory_work', 'Wave2', 'W2-FAC-X')
files = [os.path.join(T, f) for f in ['STATEMENT.md', 'STATEMENT_T2.md', 'REPORT.md', 'CHECKPOINT.md']] \
    + sorted(glob.glob(os.path.join(T, 'lemmas', '*.md'))) + sorted(glob.glob(os.path.join(T, 'T2', '*.md')))
pat = re.compile(r'`?([A-Za-z0-9_./\-]+\.(?:tex|md|R|py|h|cpp)):(\d+)(?:-(\d+))?`?')
PREF = ['', 'Theory_work/State_of_Project/sections/', 'Theory_work/Wave1C/FINAL/sections/', 'Theory_work/Wave1C/HQ_AUDIT/',
        'Theory_work/Wave1C/', 'Theory_work/Wave1/', 'Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1C/C-GROW/',
        'Theory_work/Wave2/', 'Theory_work/Wave2/W2-FAC-X/', 'Theory_work/Wave2/W2-FAC-B/', 'Theory_work/Wave2/W2-FAC-B/lemmas/',
        'Theory_work/Wave2/W2-FAC-X/lemmas/', 'Theory_work/']
def resolve(path):
    for pre in PREF:
        f = os.path.join(ROOT, pre + path)
        if os.path.isfile(f): return f
    return None
ok = miss = 0
print('## (1) path:line citations')
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
print(f'TOTAL ok={ok} miss={miss}\n')

print('## (2) verbatim status strings')
TW = os.path.join(ROOT, 'Theory_work')
STAT = [
    ('Wave1/W1-PXN/lemmas/CR_corr_tails.md', 'PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)'),
    ('State_of_Project/sections/04_theory.tex', 'T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"'),
    ('Wave2/W2-FAC-B/STATEMENT.md', 'S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R)'),
    ('Wave2/W2-FAC-B/STATEMENT.md', '[OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"'),
    ('Wave1C/FINAL/sections/s6_delivery.tex', 'PROVED (A2), checked by A3'),
    ('Wave1C/FINAL/sections/s7_impl.tex', 'PROVED (by this seat)'),
    ('Wave2/W2-FAC-B/REPORT.md', '**PROVED-CHECKED** — Theorem FAC-CS'),
    ('Wave2/W2-FAC-A/REPORT.md', '**PROVED-CHECKED**'),
    ('Wave2/HQ_AUDIT/B3_facB_redteam.md', 'HOLDS-WITH-AMENDMENTS'),
    ('Wave2/W2-FAC-B/lemmas/L4_path.md', 'Status: **PROVED (by this seat, unchecked)**'),
    ('Wave1C/FINAL/sections/s3_posterior.tex', 'Random designs.'),
]
sok = smiss = 0
for rel, s in STAT:
    f = os.path.join(TW, rel)
    hit = os.path.isfile(f) and s in open(f, encoding='utf-8', errors='replace').read()
    print(('OK   ' if hit else 'MISS ') + f'{rel}  ::  {s}'); sok += hit; smiss += (not hit)
print(f'STATUS TOTAL ok={sok} miss={smiss}\n')

print('## (3) review / numerics files named in REPORT.md')
rep = open(os.path.join(T, 'REPORT.md'), encoding='utf-8').read()
names = sorted(set(re.findall(r'(?:reviews|numerics|lemmas|T2)/[A-Za-z0-9_./\-]+\.(?:md|txt|py|jsonl)', rep)))
fok = fmiss = 0
for nme in names:
    hit = os.path.isfile(os.path.join(T, nme))
    print(('OK   ' if hit else 'MISS ') + nme); fok += hit; fmiss += (not hit)
print(f'FILE TOTAL ok={fok} miss={fmiss}')
