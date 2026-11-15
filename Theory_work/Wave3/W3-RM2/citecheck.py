"""Citation check for W3-RM2 (Wave1C protocol rule 2; modelled on W3-RM/citecheck.py).

Scope and limits. It checks the citations it can EXTRACT from this ticket's markdown files (STATEMENT, REPORT,
SHARPNESS, ASSUMPTION_MAP, PLAN, lemmas/*.md): `path:a`, `path:a-b` (or an en dash), and the alias form `POLY:a-b` used
in lemmas/L6_examples.md. For each one it resolves the file by the fixed rule below and checks that the file exists
and 1 <= a <= b <= number of lines. This is a syntactic range check: whether the cited lines SAY what is claimed is
checked by the reviewers. A continuation such as `:118` after a full citation on the same line inherits its file.

Resolution rule (fixed):
 1. A path starting with Theory_work/ or Scripts/ is repository-relative.
 2. A path starting with ../ is relative to the directory of the citing file.
 3. Otherwise the ticket is the nearest abbreviation (RM2, RM, GROW, GEN, LOC2, UNI, APP, CORE, POLY) standing before
    the citation on the same line; if none, the last abbreviation on the previous line; if none, this ticket.
    Inside that ticket the path is tried as given, then under lemmas/, then (CORE) under cpp/.
 4. A citation that resolves to no existing file is reported MISS (it is never re-resolved in another ticket).
Exit code 1 if any MISS. Writes reviews/CITECHECK.txt. Run from the repository root:
    python Theory_work/Wave3/W3-RM2/citecheck.py
"""
import io, os, re, sys, glob

ROOT = os.getcwd()
T = 'Theory_work/Wave3/W3-RM2'
ABBR = {'RM2': T, 'RM': 'Theory_work/Wave3/W3-RM', 'GROW': 'Theory_work/Wave1C/C-GROW', 'GEN': 'Theory_work/Wave1/W1-GEN',
        'LOC2': 'Theory_work/Wave2/W2-LOC2', 'UNI': 'Theory_work/Wave2/W2-UNI', 'APP': 'Theory_work/Wave2/W2-APP',
        'CORE': 'Scripts/SMC_BVS/core', 'POLY': 'Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md'}
FILES = [T + '/' + f for f in ('STATEMENT.md', 'REPORT.md', 'SHARPNESS.md', 'ASSUMPTION_MAP.md', 'PLAN.md')] + \
        sorted(glob.glob(T + '/lemmas/*.md'))
CITE = re.compile(r'(?P<path>(?:\.\./|[A-Za-z0-9_])[A-Za-z0-9_./\-]*\.(?:md|R|py|cpp|h|txt|tsv|csv)|POLY)?:(?P<a>\d+)(?:[-–](?P<b>\d+))?')
ABBR_RE = re.compile(r"(?<![A-Za-z0-9_/.\-])(RM2|RM|GROW|GEN|LOC2|UNI|APP|CORE|POLY)(?![A-Za-z0-9_\-])")
nlines = {}


def count(p):
    if p not in nlines:
        nlines[p] = len(io.open(p, encoding='utf-8', errors='replace').read().split('\n')) if os.path.isfile(p) else -1
    return nlines[p]


def context(line, pos, prev):
    m = [x for x in ABBR_RE.finditer(line[:pos])]
    if m:
        return m[-1].group(1)
    m = [x for x in ABBR_RE.finditer(prev)]
    return m[-1].group(1) if m else None


def resolve(path, citing, ctx):
    if path == 'POLY':
        return ABBR['POLY']
    if path.startswith('Theory_work/') or path.startswith('Scripts/'):
        return path
    if path.startswith('../'):
        return os.path.normpath(os.path.join(os.path.dirname(citing), path)).replace('\\', '/')
    base = ABBR.get(ctx, T) if ctx != 'POLY' else 'Theory_work/Wave2/W2-LOC2'
    for cand in (base + '/' + path, base + '/lemmas/' + path, base + '/cpp/' + path, base + '/lemmas/' + os.path.basename(path)):
        if os.path.isfile(cand):
            return cand
    return base + '/' + path


out, miss, n = [], 0, 0
for f in FILES:
    prev = ''
    for i, line in enumerate(io.open(f, encoding='utf-8').read().split('\n'), 1):
        last = None
        for m in CITE.finditer(line):
            path = m.group('path')
            if path is None:
                # continuation `:a-b`: only inside backticks right after a full citation on this line
                if last is None or not re.search(r'`:\d', line[max(0, m.start() - 1):m.start() + 3]):
                    continue
                target = last
            else:
                # skip things that are not citations: times (19:01), ratios, registry versions
                target = resolve(path, f, context(line, m.start(), prev))
                last = target
            a = int(m.group('a')); b = int(m.group('b') or a)
            n += 1
            L = count(target)
            ok = L >= 0 and 1 <= a <= b <= L
            if not ok:
                miss += 1
                out.append('MISS %s:%d  ->  %s:%d-%d  (%s)' % (f, i, target, a, b, 'no such file' if L < 0 else 'file has %d lines' % L))
        prev = line
head = 'W3-RM2 citecheck: %d citations extracted from %d files; %d MISS' % (n, len(FILES), miss)
io.open(T + '/reviews/CITECHECK.txt', 'w', encoding='utf-8', newline='\n').write(head + '\n' + '\n'.join(out) + '\n')
print(head)
for o in out:
    print(o)
sys.exit(1 if miss else 0)
