"""For quotes that are not exact substrings of any source, normalise LaTeX and Unicode math to a
common token form and measure how many of the quote's character 4-grams occur in the best-matching
source file. Low coverage means content may differ (numbers, symbols, words), not just notation."""
import os, re, sys, json, collections
ROOT = sys.argv[1]; files = sys.argv[2:]
SNAP = os.path.join(ROOT, 'archive', 'branch_snapshots')
MAP = [(r'\\le(q)?\b', '≤'), (r'\\ge(q)?\b', '≥'), (r'\\ne(q)?\b', '≠'), (r'\\sum', 'Σ'), (r'\\prod', '∏'), (r'\\pi', 'π'),
       (r'\\lambda', 'λ'), (r'\\eta', 'η'), (r'\\varepsilon|\\epsilon', 'ε'), (r'\\sigma', 'σ'), (r'\\beta', 'β'), (r'\\alpha', 'α'),
       (r'\\gamma', 'γ'), (r'\\delta', 'δ'), (r'\\Delta', 'Δ'), (r'\\theta', 'θ'), (r'\\rho', 'ρ'), (r'\\psi', 'ψ'), (r'\\mu', 'μ'),
       (r'\\tau', 'τ'), (r'\\kappa', 'κ'), (r'\\xi', 'ξ'), (r'\\Omega', 'Ω'), (r'\\omega', 'ω'), (r'\\Phi', 'Φ'), (r'\\phi', 'φ'),
       (r'\\Pi', 'Π'), (r'\\Lambda', 'Λ'), (r'\\Gamma', 'Γ'), (r'\\chi', 'χ'), (r'\\nu', 'ν'), (r'\\zeta', 'ζ'),
       (r'\\infty', '∞'), (r'\\in\b', '∈'), (r'\\notin', '∉'), (r'\\subseteq', '⊆'), (r'\\subset', '⊂'), (r'\\supseteq', '⊇'), (r'\\supsetneq', '⊋'),
       (r'\\cup', '∪'), (r'\\cap', '∩'), (r'\\emptyset|\\varnothing', '∅'), (r'\\to\b|\\rightarrow', '→'), (r'\\Rightarrow|\\implies', '⇒'),
       (r'\\Leftrightarrow|\\iff', '⇔'), (r'\\cdot', '·'), (r'\\times', '×'), (r'\\sqrt', '√'), (r'\\log', 'log'), (r'\\exp', 'exp'),
       (r'\\min', 'min'), (r'\\max', 'max'), (r'\\sim', '∼'), (r'\\approx', '≈'), (r'\\lesssim', '≲'), (r'\\mathbf\s*1|\\mathbb\s*1|\\1', '1'),
       (r'\\ell', 'ℓ'), (r'\\partial', '∂'), (r'\\star', '⋆'), (r'\\dots|\\ldots|\\cdots', '…'), (r'\\prime|′', "'"), (r'\\mid', '|'),
       (r'\\(mathrm|mathcal|mathbb|operatorname|text|textbf|mathit|boldsymbol|bar|hat|tilde|widehat|widetilde|Big|big|Bigg|left|right|tag|quad|qquad|displaystyle|,|;|!)', '')]
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉ᵀ', '01234567890123456789T')
def norm(t):
    for a, b in MAP: t = re.sub(a, b, t)
    t = t.translate(SUP)
    t = re.sub(r'[\s$\\{}^_*`|()\[\]<>]', '', t)
    return t.lower()
idx = collections.defaultdict(list)
for dp, _, fs in os.walk(SNAP):
    for f in fs:
        if f.endswith(('.md', '.tex', '.lean', '.txt')): idx[f].append(os.path.join(dp, f))
raw = {}; nrm = {}
def get(p):
    if p not in raw:
        raw[p] = open(p, encoding='utf-8', errors='replace').read(); nrm[p] = norm(raw[p])
    return raw[p], nrm[p]
allfiles = [p for v in idx.values() for p in v]
def grams(s, k=4): return {s[i:i+k] for i in range(max(0, len(s)-k+1))}
report = []
for f in files:
    lines = open(f, encoding='utf-8').read().split('\n')
    runs = []; cur = []; ctx = ''; lastsrc = ''
    for l in lines:
        m = re.search(r'`([\w@./\-]+\.(?:md|tex|lean|txt))`', l)
        if m and not l.lstrip().startswith('>'): lastsrc = m.group(1)
        if l.lstrip().startswith('>'): cur.append(re.sub(r'^\s*> ?', '', l))
        else:
            if cur: runs.append(('\n'.join(cur), lastsrc)); cur = []
    if cur: runs.append(('\n'.join(cur), lastsrc))
    for body, src in runs:
        t = body.strip()
        if not t or len(t) < 40: continue
        base = os.path.basename(src) if src else ''
        cands = idx.get(base, []) if base else []
        exact = any(t in get(c)[0] for c in cands)
        if exact: continue
        nt = norm(t); g = grams(nt)
        if not g: continue
        best = (0, None)
        probes = [nt[i:i+24] for i in (0, len(nt)//3, len(nt)//2, (2*len(nt))//3, max(0, len(nt)-24))] if len(nt) >= 24 else [nt]
        pool = list(cands)
        for c in allfiles:
            gc = nrm.get(c) if c in nrm else get(c)[1]
            if any(pr in gc for pr in probes): pool.append(c)
        for c in (pool or allfiles):
            gc = nrm.get(c) if c in nrm else get(c)[1]
            cov = sum(1 for x in g if x in gc) / len(g)
            if cov > best[0]: best = (cov, c)
            if cov > 0.999: break
        report.append((best[0], os.path.basename(f), src, best[1] and os.path.relpath(best[1], SNAP), t[:160].replace('\n', ' | ')))
report.sort()
print('non-exact quotes checked:', len(report))
buckets = collections.Counter('>=0.98' if r[0] >= 0.98 else '0.90-0.98' if r[0] >= 0.9 else '<0.90' for r in report)
print(buckets)
for r in report:
    if r[0] < 0.98: print(f"{r[0]:.3f} {r[1]} src={r[2]} best={r[3]} :: {r[4]}")
