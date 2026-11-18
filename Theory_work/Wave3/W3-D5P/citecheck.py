"""Citation check for W3-D5P (copied from W3-RM2-R/citecheck.py, RIDER_RULES §3 step 5; abbreviations and file list adapted).

Syntactic range check of every `path:a(-b)` citation in STATEMENT, REPORT, TARGET, READER_DELTA, PLAN, CARD and lemmas/*.md:
the file exists and 1 <= a <= b <= its number of lines. Whether the lines SAY what is claimed is the reviewers' job.
Resolution: repository-relative paths as given; otherwise the nearest abbreviation before the citation on the line
(else on the previous line): RM2R, RM, W3-RM2, SAMP, DIST, POST (W2-APP), READER, C-DLV/DLV, CORE; code files with no
abbreviation resolve under CORE; otherwise this ticket; then the unique-file fallback. Bare `:a` continuations are
checked only inside backticks right after a full citation on the same line. Exit 1 on any MISS. Writes
reviews/CITECHECK.txt. Run from the repository root: python Theory_work/Wave3/W3-D5P/citecheck.py
"""
import io, os, re, sys, glob

ROOT = os.getcwd()
T = 'Theory_work/Wave3/W3-D5P'
ABBR = {'RM2R': 'Theory_work/Wave3/W3-RM2-R', 'RM': 'Theory_work/Wave3/W3-RM', 'W3-RM2': 'Theory_work/Wave3/W3-RM2',
        'SAMP': 'Theory_work/Wave3/W3-SAMP', 'DIST': 'Theory_work/Wave3/W3-DIST', 'POST': 'Theory_work/Wave2/W2-APP',
        'READER': 'Theory_work/Wave3/W3-READER', 'C-DLV': 'Theory_work/Wave1C/C-DLV', 'DLV': 'Theory_work/Wave1C/C-DLV',
        'CORE': 'Scripts/SMC_BVS/core', 'POLY': 'Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md'}
FILES = [T + '/' + f for f in ('STATEMENT.md', 'REPORT.md', 'TARGET.md', 'READER_DELTA.md', 'PLAN.md', 'CARD.md') if os.path.isfile(T + '/' + f)] + \
        sorted(glob.glob(T + '/lemmas/*.md'))
CITE = re.compile(r'(?P<path>(?:\.\./|[A-Za-z0-9_])[A-Za-z0-9_./\-]*\.(?:md|R|py|cpp|h|txt|tsv|csv|tex)|POLY)?:(?P<a>\d+)(?:[-–](?P<b>\d+))?')
ABBR_RE = re.compile(r"(?<![A-Za-z0-9_/.\-])(C-DLV|W3-RM2|RM2R|RM|SAMP|DIST|POST|READER|DLV|CORE)(?![A-Za-z0-9_\-])")
nlines = {}
FALLBACK = []


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
    if ctx is None and re.search(r'\.(R|cpp|h)$', path):
        ctx = 'CORE'
    base = ABBR.get(ctx, T) if ctx != 'POLY' else 'Theory_work/Wave2/W2-LOC2'
    for cand in (base + '/' + path, base + '/lemmas/' + path, base + '/cpp/' + path, base + '/lemmas/' + os.path.basename(path)):
        if os.path.isfile(cand):
            return cand
    # Fallback (W3-RM2-R): a path not found under its context is tried under every abbreviation's folder (as given,
    # under lemmas/, under cpp/) and under Theory_work/Wave3/; it resolves only if exactly one such file exists.
    found = set()
    for b in list(ABBR.values()) + ['Theory_work/Wave3']:
        for cand in (b + '/' + path, b + '/lemmas/' + path, b + '/cpp/' + path):
            if os.path.isfile(cand):
                found.add(os.path.normpath(cand).replace('\\', '/'))
    if len(found) == 1:
        FALLBACK.append((citing, path, list(found)[0]))
        return list(found)[0]
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
head = 'W3-D5P citecheck: %d citations extracted from %d files; %d MISS; %d resolved by the unique-file fallback' % (n, len(FILES), miss, len(FALLBACK))
out += ['FALLBACK %s: %s -> %s' % x for x in sorted(set(FALLBACK))]
io.open(T + '/reviews/CITECHECK.txt', 'w', encoding='utf-8', newline='\n').write(head + '\n' + '\n'.join(out) + '\n')
print(head)
for o in out:
    print(o)
sys.exit(1 if miss else 0)
