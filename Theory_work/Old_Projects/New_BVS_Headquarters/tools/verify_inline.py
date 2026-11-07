"""Check inline quotations ("..." or “...”) of >= 25 chars against transcript + snapshots + activity."""
import os, re, sys, json
ROOT = sys.argv[1]; files = sys.argv[2:]
parts = []
for dp, _, fs in os.walk(os.path.join(ROOT, 'archive', 'branch_snapshots')):
    for f in fs:
        if f.endswith(('.md', '.tex', '.lean', '.txt', '.diff')):
            parts.append(open(os.path.join(dp, f), encoding='utf-8', errors='replace').read())
parts.append('\n'.join(i['text'] for i in json.load(open(os.path.join(ROOT, 'messages_all.json'), encoding='utf-8'))))
parts.append('\n'.join((i.get('text') or '') for i in json.load(open(os.path.join(ROOT, 'activity_all.json'), encoding='utf-8'))))
def n(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('**', '').replace('`', '')
    return re.sub(r'\s+', ' ', s).strip().lower()
C = n('\n'.join(parts))
for f in files:
    s = open(f, encoding='utf-8').read()
    qs = re.findall(r'"([^"\n]{25,600})"', s) + re.findall(r'“([^”\n]{25,600})”', s)
    bad = []
    for q in qs:
        qq = n(q)
        if qq in C: continue
        # allow ellipsis-joined fragments
        frags = [x.strip() for x in re.split(r'\.\.\.|…|\[…\]|\[\.\.\.\]', qq) if len(x.strip()) >= 12]
        if frags and all(x in C for x in frags): continue
        bad.append(q)
    print(f"{os.path.basename(f)}: inline quotes {len(qs)}, unmatched {len(bad)}")
    for b in bad[:40]: print('    ', b[:200])
