"""Annotate blockquote runs that are not byte-identical to any source. Quote text itself is untouched.
coverage >= 0.98 -> HTML comment (notation transliteration); < 0.98 -> visible FIDELITY FLAG line."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = sys.argv[1]; files = sys.argv[2:]
SNAP = os.path.join(ROOT, 'archive', 'branch_snapshots')
src = {}
for dp, _, fs in os.walk(SNAP):
    for f in fs:
        if f.endswith(('.md', '.tex', '.lean', '.txt', '.diff')):
            p = os.path.join(dp, f); src[os.path.relpath(p, SNAP).replace('\\', '/')] = open(p, encoding='utf-8', errors='replace').read()
msgs = json.load(open(os.path.join(ROOT, 'messages_all.json'), encoding='utf-8'))
for i in msgs: src['transcript [pos %d]' % i['position']] = i['text']
import importlib.util
spec = importlib.util.spec_from_file_location('fid', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fidelity.py'))
# reuse norm() without running fidelity's main: copy minimal logic
MAP = None
code = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fidelity.py'), encoding='utf-8').read()
ns = {}
exec(code.split('idx = collections.defaultdict')[0].replace('ROOT = sys.argv[1]; files = sys.argv[2:]', 'ROOT="."; files=[]'), ns)
norm = ns['norm']
nsrc = {k: norm(v) for k, v in src.items()}
allraw = '\n'.join(src.values())
ws = lambda s: re.sub(r'\s+', ' ', s)
allws = ws(allraw)
def grams(s, k=4): return {s[i:i+k] for i in range(max(0, len(s)-k+1))}
stats = collections.Counter()
for f in files:
    lines = open(f, encoding='utf-8').read().split('\n')
    out = []; i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('>'):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith('>'): j += 1
            run = lines[i:j]
            body = '\n'.join(re.sub(r'^\s*> ?', '', l) for l in run).strip()
            note = None
            if len(body) >= 40 and not body.startswith(('Summary', 'Source', '⚠')):
                if body in allraw or ws(body) in allws:
                    stats['exact'] += 1
                else:
                    ls = [x.strip() for x in body.split('\n') if x.strip() and not x.strip().startswith(('[…]', '[...]', '…'))]
                    if ls and all(ws(x) in allws for x in ls):
                        stats['linewise'] += 1
                    else:
                        nt = norm(body); g = grams(nt)
                        probes = [nt[k:k+24] for k in (0, len(nt)//3, len(nt)//2, (2*len(nt))//3, max(0, len(nt)-24))] if len(nt) >= 24 else [nt]
                        best = (0.0, None)
                        for k, v in nsrc.items():
                            if any(pr in v for pr in probes):
                                cov = sum(1 for x in g if x in v) / max(1, len(g))
                                if cov > best[0]: best = (cov, k)
                        if best[0] >= 0.98:
                            stats['translit'] += 1
                            note = f"<!-- fidelity: not byte-identical; notation transliterated (4-gram coverage {best[0]:.3f}) from `{best[1]}`; that file is authoritative -->"
                        else:
                            stats['flag'] += 1
                            where = f"`{best[1]}`" if best[1] else "the cited source"
                            note = f"⚠ **FIDELITY FLAG (archive check):** the quote below is not byte-identical to its source and differs beyond notation (content 4-gram coverage {best[0]:.2f}; best match {where}). It may be abridged, reformatted or paraphrased. Use the source file as authoritative."
            if note:
                indent = re.match(r'^(\s*)', run[0]).group(1)
                out.append(indent + note)
            out.extend(run); i = j
        else:
            out.append(lines[i]); i += 1
    open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print(os.path.basename(f), dict(stats)); stats.clear()
