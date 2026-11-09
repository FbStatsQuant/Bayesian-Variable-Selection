"""C-PACK citation check: open every backticked `path:line[-line]` citation in the ticket's own files, confirm the file and
lines exist, and confirm that any "quoted text" on the same source line appears in the cited file near the cited lines.
Usage: python -B -X utf8 citecheck.py  (writes ../reviews/CITECHECK.txt)."""
import re, os, sys, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
TICKET = os.path.join(ROOT, 'Theory_work', 'Wave1C', 'C-PACK')
ALIASES = {
    'W1/': 'Theory_work/Wave1/', 'SoP/': 'Theory_work/State_of_Project/sections/',
    'NBH/': 'Theory_work/Old_Projects/New_BVS_Headquarters/',
    'CODE/': 'Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/',
    'NBH = ': 'NBH = ',
    'PX:': 'Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md:',
}
# files whose citations are checked (the lead's own deliverables)
FILES = ['STATEMENT.md', 'SONG_LIANG_MAP.md', 'METHOD_REQUIREMENTS.md', 'lemmas/I1_e4_replacement.md',
         'lemmas/I2_LHiid_unconditional.md', 'lemmas/I4_SL_corollaries.md', 'patches/P_e4_consumers.md',
         'patches/P_GEN_LHiid.md', 'patches/P_SEL_L6d.md', 'patches/P_L8_certificate.md',
         'item5_PXN_consolidated/00_statement_and_conventions.md', 'item5_PXN_consolidated/01_tools.md',
         'item5_PXN_consolidated/02_design_events.md', 'item5_PXN_consolidated/03_start.md',
         'item5_PXN_consolidated/04_search.md', 'item5_PXN_consolidated/05_posterior_output.md',
         'item5_PXN_consolidated/06_A_dependence_and_scope.md', 'item5_PXN_consolidated/INDEX.md',
         'item5_PXN_consolidated/MAP.md', 'item5_PXN_consolidated/APPLIED_ERRATA.md',
         'item5_PXN_consolidated/OPEN_QUESTIONS.md']
SECTION_BASE = {'## PXN': ['Theory_work/Wave1/W1-PXN/'], '## GEN': ['Theory_work/Wave1/W1-GEN/'],
                '## M5': ['Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W6-FIXREV1/']}
for _f in [x for x in FILES if x.startswith('item5')]:
    pass
# relative names used inside a file without alias -> base dir (by context)
CTX_BASE = {
    'patches/P_GEN_LHiid.md': ['Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1/W1-GEN/lemmas/'],
    'patches/P_SEL_L6d.md': ['Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1/W1-GEN/lemmas/'],
    'patches/P_L8_certificate.md': ['Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1/W1-GEN/lemmas/'],
}
SPECIAL = {'T38_PROOF.md': 'Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W6-FIXREV1/T38_PROOF.md',
           'API-PXNGAP/PROOF.md': 'Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md'}
CIT = re.compile(r'`([^`\s]+?\.(?:md|tex|h|R|cpp|py|txt|tsv)):(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)`')
PXC = re.compile(r'PX:(\d+)(?:-(\d+))?')
QUOTE = re.compile(r'"([^"]{12,})"')

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('\\', '').replace('*', '').replace('`', '')
    return re.sub(r'\s+', ' ', s).strip()

CUR_SECTION = {}
def resolve(path, src):
    for a, b in ALIASES.items():
        if path.startswith(a):
            return os.path.join(ROOT, b + path[len(a):])
    if path in SPECIAL:
        return os.path.join(ROOT, SPECIAL[path])
    cands = [os.path.join(ROOT, path)]
    for b in CTX_BASE.get(src, []) + SECTION_BASE.get(CUR_SECTION.get(src, ''), []):
        cands.append(os.path.join(ROOT, b, path))
    cands.append(os.path.join(TICKET, path))
    for base in ['Theory_work/Wave1/W1-GEN/', 'Theory_work/Wave1/W1-PXN/', 'Theory_work/Wave1/W1-N3/',
                 'Theory_work/Wave1/W1-GEN/lemmas/', 'Theory_work/Wave1/W1-PXN/lemmas/']:
        cands.append(os.path.join(ROOT, base, path))
    for c in cands:
        if os.path.isfile(c):
            return c
    return cands[0]

def check(out):
    n_ok = n_miss = n_q_ok = n_q_miss = 0
    for f in FILES:
        fp = os.path.join(TICKET, f)
        lines = open(fp, encoding='utf-8').read().splitlines()
        for ln, text in enumerate(lines, 1):
            for key in SECTION_BASE:
                if text.startswith(key):
                    CUR_SECTION[f] = key
            if text.startswith('## Additions after mid-point'):
                CUR_SECTION[f] = ''
            cites = []
            for m in CIT.finditer(text):
                rngs = [(int(m.group(2)), int(m.group(3) or m.group(2)))]
                for extra in re.findall(r'(\d+)(?:-(\d+))?', m.group(4) or ''):
                    rngs.append((int(extra[0]), int(extra[1] or extra[0])))
                cites.append((m.group(1), rngs))
            for m in PXC.finditer(text):
                cites.append(('PX:', [(int(m.group(1)), int(m.group(2) or m.group(1)))]))
            if not cites:
                continue
            quotes = [norm(q) for q in QUOTE.findall(text)]
            for path, rngs in cites:
                target = resolve(path if path != 'PX:' else 'PX:', f) if path != 'PX:' else os.path.join(ROOT, ALIASES['PX:'][:-1])
                if not os.path.isfile(target):
                    out.append(f'MISS-FILE {f}:{ln} -> {path}')
                    n_miss += 1
                    continue
                tl = open(target, encoding='utf-8', errors='replace').read().splitlines()
                bad = [r for r in rngs if r[1] > len(tl) or r[0] < 1 or r[0] > r[1]]
                if bad:
                    out.append(f'MISS-LINE {f}:{ln} -> {path}:{bad} (file has {len(tl)} lines)')
                    n_miss += 1
                    continue
                n_ok += 1
                lo = max(0, min(r[0] for r in rngs) - 6); hi = min(len(tl), max(r[1] for r in rngs) + 6)
                window = norm(' '.join(tl[lo:hi])); whole = norm(' '.join(tl))
                segs = []
                for q in quotes:
                    segs += [x.strip() for x in re.split(r'\.\.\.|…', q) if len(x.strip()) >= 12]
                for q in segs:
                    key = q[:60]
                    if key in window:
                        n_q_ok += 1
                    elif key in whole:
                        out.append(f'QUOTE-ELSEWHERE {f}:{ln} -> {path}:{rngs}: "{key}"')
                        n_q_miss += 1
                    else:
                        # quote may belong to another citation on the same line; only flag if no cite on the line has it
                        found = False
                        for p2, r2 in cites:
                            t2 = os.path.join(ROOT, ALIASES['PX:'][:-1]) if p2 == 'PX:' else resolve(p2, f)
                            if os.path.isfile(t2) and key in norm(open(t2, encoding='utf-8', errors='replace').read()):
                                found = True
                        if not found:
                            out.append(f'QUOTE-NOTFOUND {f}:{ln} -> {path}:{rngs}: "{key}"')
                            n_q_miss += 1
    out.append(f'SUMMARY citations ok={n_ok} miss={n_miss}; quotes near-cite ok={n_q_ok} flagged={n_q_miss}')

if __name__ == '__main__':
    out = []
    check(out)
    dst = os.path.join(TICKET, 'reviews', 'CITECHECK.txt')
    open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('\n'.join(out))
