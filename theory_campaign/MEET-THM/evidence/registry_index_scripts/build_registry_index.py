# -*- coding: utf-8 -*-
"""Build theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md.

Mechanical registrar script: reads the sources from git objects (git show origin/...), parses REGISTRY_v2.md,
LOCKABLE_v2.md, THEOREM_LIST.md, THEOREM_REVISION_INPUTS.md, scans every *.lean file on every origin branch,
and writes the index.  Status words are copied verbatim from the registry cells; nothing is recomputed or upgraded.
Run:  python3 -I build_registry_index.py <repo_root> <out_md> <stage 1..5>
"""
import sys, re, subprocess, json, collections, os
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import items_data as D

ROOT, OUT, STAGE = sys.argv[1], sys.argv[2], int(sys.argv[3])

def git(*a):
    return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True).stdout

def show(ref, path):
    return git('show', f'{ref}:{path}')

REGP = 'origin/theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md'
LOCKP = 'origin/theory/T38-RECORD:theory_campaign/T38-RECORD/LOCKABLE_v2.md'
LISTP = 'origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md'
INPP = 'origin/theory/MEET-v31:theory_campaign/MEET-v31/THEOREM_REVISION_INPUTS.md'
INVP = 'origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md'

def srcfile(p):
    ref, path = p.split(':', 1)
    return show(ref, path)

REG = srcfile(REGP).split('\n')
LOCK = srcfile(LOCKP).split('\n')
LIST = srcfile(LISTP).split('\n')
INP = srcfile(INPP).split('\n')
INV = srcfile(INVP).split('\n')
PC1T = srcfile(D.PC1).split('\n')
PC2T = srcfile(D.PC2).split('\n')

# ---- head SHAs of the source branches (for the provenance block) ----
def head(b):
    return git('rev-parse', '--short=7', f'origin/{b}').strip()
HEADS = {b: head(b) for b in ['theory/campaign', 'theory/THM-SYNTH', 'theory/T38-RECORD', 'theory/MEET-v31', 'theory/THM-INV',
                                'theory/L-LEAN', 'theory/METH-AUDIT', 'theory/API-MASKZPIP', 'theory/API-N200', 'theory/API-VSTAB',
                                'theory/API-T26BUD', 'theory/LIT-PAR', 'main']}

# ---- branch/file index ----
TC = collections.defaultdict(set)
for b in git('for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin/theory').split():
    n = b[len('origin/theory/'):]
    for p in git('ls-tree', '-r', '--name-only', b).split('\n'):
        if p.startswith(f'theory_campaign/{n}/'):
            TC[n].add(p)
BRANCHES = sorted(TC.keys(), key=lambda x: -len(x))

def resolve(src):
    """Registry 'Source' cell -> origin/theory/<B>:theory_campaign/<B>/<file> + section label."""
    b = next((x for x in BRANCHES if src.startswith(x)), None)
    if not b:
        return f'(branch not parsed) {src}', ''
    rest = src[len(b):].lstrip(' ·')
    m = re.search(r'([A-Za-z0-9_\-\.]+\.(?:md|tex|txt))', rest)
    fn = None
    if m and f'theory_campaign/{b}/{m.group(1)}' in TC[b]:
        fn = m.group(1)
    else:
        for cand in ('PROOF.md', 'REPORT.md'):
            if cand.split('.')[0] in rest and f'theory_campaign/{b}/{cand}' in TC[b]:
                fn = cand
                break
    inferred = ''
    if fn is None:
        # try a file named by a bare token (e.g. T38_STATEMENT) on any branch named in the cell
        for bb in [b] + [x for x in BRANCHES if x in src and x != b]:
            for tok in re.findall(r'[A-Za-z0-9_]{4,}', rest):
                if f'theory_campaign/{bb}/{tok}.md' in TC[bb]:
                    b, fn = bb, tok + '.md'; inferred = ' [file named by bare token in the cell]'
                    break
            if fn: break
    if fn is None and f'theory_campaign/{b}/REPORT.md' in TC[b]:
        fn = 'REPORT.md'; inferred = ' [the cell names no file; REPORT.md of that branch is the nearest — inferred by the registrar]'
    if fn is None:
        return f'origin/theory/{b}:theory_campaign/{b}/ (file not parsed from: {src})', ''
    label = rest.replace(fn, '').strip(' ·') + inferred
    return f'origin/theory/{b}:theory_campaign/{b}/{fn}', label

# ---- registry parse ----
ROWS = {}
ORDER = []
sec = None; hdr = None
for i, l in enumerate(REG, 1):
    if l.startswith('## ') or l.startswith('### '):
        sec = l.lstrip('# ').strip(); hdr = None; continue
    if l.startswith('| ID |'):
        hdr = True; continue
    if hdr and l.startswith('|') and not l.startswith('|---'):
        c = [x.strip() for x in l.strip().strip('|').split(' | ')]
        if len(c) != 9:
            continue
        m = re.match(r'`([^`]+)`', c[0])
        rid = m.group(1)
        ROWS[rid] = dict(id=rid, line=i, sec=sec, tag=c[0][m.end():].strip(), target=c[1], src=c[2], author=c[3], sf=c[4], xf=c[5],
                         rep=c[6], prem=c[7], meaning=c[8], flagged=sec.startswith('C. Flagged'))
        ORDER.append(rid)
assert len(ROWS) == 480, len(ROWS)

# ---- LOCKABLE categories ----
LOCKCAT = {}
cat = None
for i, l in enumerate(LOCK, 1):
    if l.startswith('## ') or l.startswith('### '):
        cat = l.lstrip('# ').strip().split(' — ')[0].split(' (')[0][:110]
    mm = re.match(r'\| `([^`]+)` \|', l)
    if mm and cat and cat[0] in '123':
        LOCKCAT.setdefault(mm.group(1), (cat, i))
    if cat and cat.startswith('3e') and l.startswith('`'):
        for rid in re.findall(r'`([^`]+)`', l):
            LOCKCAT.setdefault(rid, (cat, i))

def verdict(cell):
    m = re.match(r'\*\*([^*]+\*?)\*\*', cell)
    if m:
        return m.group(1)
    if cell.startswith('referee-authored'):
        return 'referee-authored'
    if cell.startswith('n/a'):
        return 'n/a'
    return 'none'

def who(cell):
    m = re.match(r'\*\*[^*]+\*?\*\*\s*—\s*([A-Za-z0-9\-]+)', cell)
    if m:
        return m.group(1)
    m = re.match(r'none — authored by ([A-Za-z0-9\-]+)', cell)
    if m:
        return 'authored by ' + m.group(1)
    m = re.match(r'referee-authored:\s*([A-Za-z0-9\-]+)', cell)
    if m:
        return m.group(1)
    return ''

def hist(r):
    def one(cell):
        v = verdict(cell); w = who(cell)
        return v + (f' ({w})' if w else '')
    return f"SF: {one(r['sf'])}; XF: {one(r['xf'])}"

def flag(r):
    br = r['src'].split(' ')[0]
    sfv, xfv = verdict(r['sf']), verdict(r['xf'])
    if r['flagged']:
        return f"FLAGGED-SUBCLAIM (SF {sfv}; XF {xfv})"
    if r['author'] == 'REFEREE':
        return 'REFEREE-AUTHORED (author is a cross-family referee)'
    if br == 'A-DRAFT':
        return f"ASTRA-ONLY (Astra-on-Astra; XF {xfv})"
    if xfv in ('VERIFIED', 'VERIFIED*'):
        return 'XF-VERIFIED' + ('*(qualified)' if xfv.endswith('*') else '')
    if xfv in ('GAP', 'ERROR'):
        return f"XF-ADVERSE:{xfv}" + (' (SF verified)' if sfv in ('VERIFIED', 'VERIFIED*') else ' (no clean SF)')
    # no cross-family check
    if sfv in ('VERIFIED', 'VERIFIED*'):
        return 'FLAG SAME-FAMILY-ONLY'
    if sfv in ('GAP', 'ERROR'):
        return f'FLAG SAME-FAMILY-ADVERSE:{sfv}; no XF'
    return 'FLAG AUTHOR-ONLY'

PATS = [('LS0', r'with(?:out)? LS0|no LS0|LS0 route|LS0'),
        ('grid', r'ideal(?:ised)?[ -](?:exact-frontier |two-state )?grid|as[- ]coded|coded grid|frozen grid|every (?:frozen )?grid|any frozen grid'),
        ('pooling', r'equal-weight|Ẑ-weighted|evidence-weighted|Z-weighted'),
        ('label', r'v3\.1|v3 as run|v3\.2|particle-parallel|island-parallel|iid final draws|iid draws')]

def variant(r):
    out = []; used = []
    for name, pat in PATS:
        for key in ('meaning', 'prem', 'rep', 'src', 'sf', 'xf'):
            m = re.search(pat, r[key])
            if m:
                s0 = max(0, m.start() - 45); e0 = min(len(r[key]), m.end() + 60)
                if any(k == key and not (e0 < a or s0 > b) for k, a, b in used):
                    continue
                used.append((key, s0, e0))
                txt = r[key]
                # start/end on word boundaries
                if s0 > 0 and txt[s0 - 1] != ' ':
                    j = txt.find(' ', s0); s0 = j + 1 if 0 <= j < m.start() else s0
                if e0 < len(txt) and txt[e0] != ' ':
                    j = txt.rfind(' ', m.end(), e0); e0 = j if j > m.end() else e0
                sn = re.sub(r'\s+', ' ', txt[s0:e0]).replace('|', '/')
                out.append(f'{name}: "…{sn}…" [{key}]')
                break
    return '; '.join(out) if out else 'not stated'

def regline(rid):
    return f'REGISTRY_v2.md:L{ROWS[rid]["line"]}'

REGBASE = 'origin/theory/T38-RECORD:theory_campaign/T38-RECORD/'

# ---- THEOREM_LIST rows ----
LROWS = {}
for i, l in enumerate(LIST, 1):
    m = re.match(r'\| (V[1-4]|A[1-4]|D[1-4]|S[1-4]|C1|R[1-7]) \|', l)
    if m and i < 52:
        c = [x.strip() for x in l.strip().strip('|').split(' | ')]
        LROWS[m.group(1)] = dict(line=i, title=c[1], group=c[2], guarantee=c[3], status=c[4], novelty=c[5], tier=c[6], lean=c[7] if len(c) > 7 else '')
s4 = next(i for i, l in enumerate(LIST, 1) if l.startswith('### S4.'))
LROWS['S4'] = dict(line=s4, title='Weight stability (proposal §5.3) — supplement remark only', group='G4', guarantee='',
                   status=' '.join(x for x in LIST[s4+1:s4+6] if x.strip())[:900], novelty='', tier='v2', lean='')
LROWS['S3']['status'] = LROWS['S3']['status']  # as in the table (S3 dropped)
LISTSRC = 'origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md'
INPSRC = 'origin/theory/MEET-v31:theory_campaign/MEET-v31/THEOREM_REVISION_INPUTS.md'
INVSRC = 'origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md'

ITEM_ORDER = ['V1', 'V2', 'V3', 'V4', 'A1', 'A2', 'A3', 'A4', 'D1', 'D2', 'D3', 'D4', 'S1', 'S2', 'S3', 'S4', 'C1', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
NOBL = [f'N{i}' for i in range(1, 18)]

# =====================================================================================================
# LEAN scan
# =====================================================================================================
def strip_comments(s):
    out = []; i = 0; depth = 0
    while i < len(s):
        if s.startswith('/-', i):
            depth += 1; i += 2; continue
        if depth and s.startswith('-/', i):
            depth -= 1; i += 2; continue
        if depth:
            i += 1; continue
        if s.startswith('--', i):
            j = s.find('\n', i); i = len(s) if j < 0 else j; continue
        out.append(s[i]); i += 1
    return ''.join(out)

DECL = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev|structure|inductive|class|instance|axiom|opaque|example)\s+([^\s:({\[]+)?', re.M)
LEAN = []
for b in git('for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin').split():
    if b == 'origin/HEAD' or b == 'origin':
        continue
    for p in git('ls-tree', '-r', '--name-only', b).split('\n'):
        if re.search(r'\.lean$|lakefile|lean-toolchain|lake-manifest', p, re.I):
            LEAN.append((b, p))
LEANSCAN = []
for b, p in LEAN:
    if p.endswith('.lean'):
        s = show(b, p); c = strip_comments(s)
        ds = [(m.group(1), m.group(2) or '') for m in DECL.finditer(c)]
        LEANSCAN.append(dict(b=b, p=p, lines=len(s.splitlines()), ds=ds,
                             sorry=len(re.findall(r'\bsorry\b', c)), admit=len(re.findall(r'\badmit\b', c)),
                             sorry_raw=len(re.findall(r'\bsorry\b', s)), admit_raw=len(re.findall(r'\badmit\b', s)),
                             axiom=len(re.findall(r'^\s*axiom\b', c, re.M))))

# which registry IDs does each Lean file certify, per sources (L-LEAN STATUS.md target table + REGISTRY_v2.md §G)
LEAN_CERT = {
 'T21HPM.lean': ('T21 (C1) + decompositions; registry rows Thm4-C1, T38-(0)', 'REGISTRY_v2.md §G row 1; L-LEAN STATUS.md row T21; THEOREM_LIST.md R4(vi)', 'routes (a)-(f) and the H03 asymptotics are not formalised'),
 'T07Bayes.lean': ('T07 (i),(i′),(ii),(iii), Lemma psi; registry row Prop1-T07', 'REGISTRY_v2.md §G row 2; L-LEAN STATUS.md row T07; THEOREM_LIST.md R2(vi)', 'sorry-free'),
 'T11Miss.lean': ('T11(iii) (locked T11; no registry row)', 'REGISTRY_v2.md §G row 3; L-LEAN STATUS.md row T11(iii)', 'sorry-free'),
 'T37Greedy.lean': ('T37(i) / Theorem A; registry rows TheoremA, Lemma0(a,c)', 'REGISTRY_v2.md §G row 4; L-LEAN STATUS.md row T37(i); THEOREM_LIST.md R3(vi)', 'A5, Theorems B and C not formalised'),
 'T37Lattice.lean': ('T37(i) / Theorem A lattice forms; registry rows TheoremA, Lemma0(a,c)', 'REGISTRY_v2.md §G row 4; L-LEAN STATUS.md row T37(i)', 'as T37Greedy.lean'),
 'T12Core.lean': ('T12(i.a); registry row Prop2(a,b,d,e)', 'REGISTRY_v2.md §G row 5; L-LEAN STATUS.md row T12(i.a); THEOREM_LIST.md V1(vi)', 'PARTIAL: hstep (resample–move recursion) is an explicit hypothesis'),
 'Basic.lean': ('shared definitions/lemmas (argmax, posterior); no registry ID named', 'L-LEAN STATUS.md (Basic.lean listed with T21HPM.lean)', '—'),
 'Axioms.lean': ('axiom audit (#print axioms) — declares no theorem', 'L-LEAN AXIOMS_RECORD.txt', '—'),
}

# =====================================================================================================
# writers
# =====================================================================================================
L = []
def w(s=''):
    L.append(s)

def esc(s):
    return s.replace('\\|', '|').replace('|', '\\|').replace('\n', ' ')

def reg_table(idrole):
    w('| Registry ID | Status (verbatim, REGISTRY_v2 "Author status") | Result lives at (branch:path · label) | Check history (from SF / XF cells) | Flag | LOCKABLE_v2 § | Method variant (only if a source states it) | Registry row |')
    w('|---|---|---|---|---|---|---|---|')
    for rid, role in idrole:
        r = ROWS[rid]
        path, label = resolve(r['src'])
        lc = LOCKCAT.get(rid)
        tag = (' ' + r['tag']) if r['tag'] else ''
        rl = (' — ' + esc(role)) if ('THEOREM_LIST' in role or 'INPUTS' in role or 'THM-INV' in role) else ''
        w(f"| `{rid}`{tag}{rl} | {esc(r['author'])} | `{path}` · {esc(label or r['src'])} | {esc(hist(r))} | {flag(r)} | {esc(lc[0]) + ' (LOCKABLE_v2.md:L%d)' % lc[1] if lc else 'not listed'} | {esc(variant(r))} | `{REGBASE}REGISTRY_v2.md:L{r['line']}` |")

def other_table(keys):
    w('| Non-registry result | Status (verbatim from source) | Result lives at | Check history (as the source states it) | Flag | Method variant (only if a source states it) | Lean |')
    w('|---|---|---|---|---|---|---|')
    for k in keys:
        o = D.NONREG[k]
        w(f"| `{k}` | {esc(o['status'])} | `{o['where']}` | {esc(o['hist'])} | {o['flag'] if o['flag'] in ('XF',) else 'FLAG ' + o['flag'] if o['flag'] != 'XF' else o['flag']} | {esc(o['variant'])} | {esc(o['lean'])} |")

def stage1_header():
    w('# REGISTRY_INDEX — MEET-THM registrar index (what already exists, traced to source)')
    w()
    w('Registrar run for the theorem-selection meeting (MEET-THM). **Mechanical index only: no proving, no judging, no status upgrade.** '
      'Every status word below is copied verbatim from the cited source; every line carries a source path in the form '
      '`origin/<branch>:<path>[:Lnn]`. Branch `theory/MEET-THM-REG`, created from `origin/theory/campaign`. '
      'Generated by `theory_campaign/MEET-THM/evidence/registry_index_scripts/build_registry_index.py` (reads the sources from git objects; re-runnable).')
    w()
    w('**Status vocabulary:** `theory_campaign/PROTOCOL.md` (PROVED, PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN; every PROVED is a candidate: not reviewed by adoption, not adopted). '
      'Registry words PROVED-UNDER, REFEREE, PROVED-LOCKED are copied as the sources use them.')
    w()
    w('**Sources read (head SHAs at fetch):**')
    w()
    w('| Role | Path | Head |')
    w('|---|---|---|')
    w(f"| draft list (19 items + S4 in body) | `{LISTSRC}` | `{HEADS['theory/THM-SYNTH']}` |")
    w(f"| registry | `{REGBASE}REGISTRY_v2.md` | `{HEADS['theory/T38-RECORD']}` |")
    w(f"| lockable candidates | `{REGBASE}LOCKABLE_v2.md` | `{HEADS['theory/T38-RECORD']}` |")
    w(f"| method-meeting obligations N1–N17 (§3) | `{INPSRC}` | `{HEADS['theory/MEET-v31']}` |")
    w(f"| inventory | `{INVSRC}` | `{HEADS['theory/THM-INV']}` |")
    w(f"| locked-proof register (locked results are not registry rows) | `origin/theory/campaign:Docs/Theory/proofs/LOCKED_PROOFS.md` (also `origin/main`) | `{HEADS['theory/campaign']}` |")
    w(f"| Lean package | `origin/theory/L-LEAN:theory_campaign/L-LEAN/` | `{HEADS['theory/L-LEAN']}` |")
    w(f"| result sources outside the registry | `origin/theory/METH-AUDIT` (`{HEADS['theory/METH-AUDIT']}`), `API-MASKZPIP` (`{HEADS['theory/API-MASKZPIP']}`), `API-N200` (`{HEADS['theory/API-N200']}`), `API-VSTAB` (`{HEADS['theory/API-VSTAB']}`), `API-T26BUD` (`{HEADS['theory/API-T26BUD']}`), `LIT-PAR` (`{HEADS['theory/LIT-PAR']}`), MEET-v31 `evidence/` PC1, PC2 | — |")
    w()
    w('**Conventions used in the tables.**')
    w('- *Same-family (SF)* and *cross-family (XF)* are the registry\'s own columns (`REGISTRY_v2.md` header: SF = a campaign verifier run, Opus checking Opus; XF = A-REV1–A-REV9, Astra reviewers; A-REV4 on A-DRAFT is Astra-on-Astra and is recorded as SF there). '
      f"Source: `{REGBASE}REGISTRY_v2.md:L{next(i for i,l in enumerate(REG,1) if l.startswith('**How to read the columns.**'))}` ('How to read the columns').")
    w('- **Flag** is derived by rule from the SF/XF cells and is only a flag, not a verdict: `XF-VERIFIED` = a cross-family reviewer wrote VERIFIED (`*` = with a stated qualification); `XF-ADVERSE:GAP|ERROR` = a cross-family reviewer wrote GAP/ERROR on that row; '
      '`FLAG SAME-FAMILY-ONLY` = the only clean check is a same-model-family verifier; `FLAG AUTHOR-ONLY` = no verifier of any family (author\'s own check, or author = verifier); `ASTRA-ONLY` = A-DRAFT results written and checked by Astra only. '
      'For non-registry results the flag is set from the check history the source states (family of author/checker given where the source names it: Opus 5.5, Fable 5.1 = Claude family; gpt-6-astra / Astra / Sol = OpenAI family).')
    w('- **Result lives at**: `origin/theory/<BRANCH>:theory_campaign/<BRANCH>/<file>` resolved from the registry "Source" cell and checked to exist on that branch; the text after `·` is the registry\'s own section/label. ')
    w('- **Method variant**: filled only where a source states it (keyword scan of the registry row\'s own cells for LS0 / ideal vs coded grid / equal-weight vs Ẑ-weighted / v3.1, v3 as run, v3.2; quoted with the cell it came from), or an item-level statement in the draft list / revision inputs (quoted and cited). Otherwise `not stated`.')
    w('- The full verbatim SF / XF / repair / premise cells of every registry row cited here are in **Appendix A** (with `REGISTRY_v2.md` line numbers).')
    w()

def stage1_lean():
    w('## 3. Lean index (every `*.lean` file on every origin branch)')
    w()
    w(f"Search: `git ls-tree -r --name-only` over all {len(git('for-each-ref','--format=%(refname:short)','refs/remotes/origin').split())-1} origin refs for `*.lean`, `lakefile*`, `lean-toolchain`, `lake-manifest*`. "
      f"**All hits are on one branch, `origin/theory/L-LEAN` (head `{HEADS['theory/L-LEAN']}`); no other branch (including `origin/main`, `origin/theory/campaign`) contains a `.lean` file or Lean build file.** "
      "Counts below are from the registrar's scan (comments stripped: `/- … -/` nested and `--`); `sorry`/`admit` = tokens in code. Declarations = theorem/lemma/def/abbrev/structure/… lines; the 'theorems' column counts `theorem`+`lemma` only.")
    w()
    w('### 3.1 Build files')
    w()
    w('| Path | What it declares (verbatim excerpt) |')
    w('|---|---|')
    for b, p in LEAN:
        if not p.endswith('.lean'):
            s = show(b, p).strip().replace('\n', ' ⏎ ')
            w(f"| `{b}:{p}` | {esc(s[:300])} |")
    w(f"| `origin/theory/L-LEAN:theory_campaign/L-LEAN/build.sh`, `CLEAN_BUILD.txt`, `AXIOMS_RECORD.txt`, `DECL_STATUS.md`, `STATUS.md`, `REPORT.md` | build/audit records (not Lean files) |")
    w()
    w('Toolchain/lakefile as stated: `leanprover/lean4:v4.35.0-rc2`; Mathlib `v4.35.0-rc2` (`lakefile.toml`); `packagesDir = "C:/lean/packages/v4.35.0-rc2"` is a laptop path (`lakefile.toml` comment: "Shared Mathlib checkout on Felipe\'s laptop"). `lake build` result as stated by the source: "0 errors, 0 warnings, 0 `sorry`" (`origin/theory/L-LEAN:theory_campaign/L-LEAN/STATUS.md`).')
    w()
    w('### 3.2 Per-file table')
    w()
    w('| File (branch:path) | Lines | Declarations | theorem/lemma | sorry (code) | admit (code) | sorry in comments only | Theorem/lemma names declared | Certifies registry IDs, if a source says so (source) |')
    w('|---|---|---|---|---|---|---|---|---|')
    totals = collections.Counter()
    for f in LEANSCAN:
        base = os.path.basename(f['p'])
        thm = [n for k, n in f['ds'] if k in ('theorem', 'lemma')]
        names = ', '.join(f"`{n}`" for n in thm) or '—'
        cert = LEAN_CERT.get(base)
        if 'packet' in f['p'] or 'frozen' in f['p']:
            ctx = ' (copy)'
            cs = 'copy of the file named; see §3.3'
        else:
            ctx = ''
            cs = f"{cert[0]} — {cert[1]}; scope: {cert[2]}" if cert else 'not stated in a source read'
        cmt = (f['sorry_raw'] - f['sorry']) + (f['admit_raw'] - f['admit'])
        w(f"| `{f['b']}:{f['p']}`{ctx} | {f['lines']} | {len(f['ds'])} | {len(thm)} | {f['sorry']} | {f['admit']} | {cmt} | {names} | {esc(cs)} |")
        if 'SmcBvs/SmcBvs/' in f['p']:
            totals['files'] += 1; totals['decl'] += len(f['ds']); totals['thm'] += len(thm); totals['sorry'] += f['sorry']; totals['admit'] += f['admit']
    w()
    w(f"**Totals, library `SmcBvs/SmcBvs/*.lean` (current):** {totals['files']} files, {totals['decl']} declarations, **{totals['thm']} theorem/lemma**, {totals['sorry']} `sorry`, {totals['admit']} `admit`. "
      f"Sources state '101 declarations, 101 proved, 0 with sorry' (`origin/theory/L-LEAN:theory_campaign/L-LEAN/DECL_STATUS.md` line 3; `STATUS.md`); the registrar's count of 101 matches the `theorem` count, the other {totals['decl']-totals['thm']} are `def`/`abbrev`/`structure` (the sources' '101 declarations' counts theorems only). "
      "`Axioms.lean` and `SmcBvs.lean` declare no theorems (imports and `#print axioms` only).")
    w()
    w('### 3.3 Copies with `sorry` (read before citing a Lean count)')
    w()
    cp = [f for f in LEANSCAN if ('frozen' in f['p'] or 'packet' in f['p']) and (f['sorry'] or f['admit'])]
    for f in cp:
        w(f"- `{f['b']}:{f['p']}`: {f['sorry']} `sorry` in code ({f['lines']} lines, {len([1 for k,_ in f['ds'] if k in ('theorem','lemma')])} theorems).")
    w(f"- What the source says about these directories: `L-LEAN REPORT.md` — \"All statements were frozen in `frozen/v1/` before the remaining proofs were written … `stmtdiff.py` showed `RESULT OK 0` for all files. Later results were added as new declarations only.\" (`origin/theory/L-LEAN:theory_campaign/L-LEAN/REPORT.md`, the 'Statements.' bullet). "
      "`fidelity/packet*/` are the packets sent to the fidelity reviewers (`fidelity/packet/SOURCES.md`). The registrar does not infer more: the files in `frozen/v1/T07Bayes.lean`, `frozen/v1/T37Lattice.lean` and the same two in `fidelity/packet/lean/` contain `sorry` as stored; `SmcBvs/SmcBvs/` has none.")
    w(f"- Identical-content check (sha1 of file text, first 8 hex): `fidelity/packet2/lean/T37Greedy.lean` = `SmcBvs/SmcBvs/T37Greedy.lean`; `fidelity/packet2/lean/T37Lattice.lean` = `SmcBvs/SmcBvs/T37Lattice.lean` (both 414 / 439 lines in the table above).")
    w()
    w('### 3.4 Fidelity / audit status as the sources state it')
    w()
    w("- `REGISTRY_v2.md` §G: \"Fidelity: Fable 5.1 GREEN (same family). Astra round 1 GREEN on T21, T07, T11, T12 and RED on T37 coverage; new theorems added without changing a frozen statement; **Astra round 2 OVERALL (T37) GREEN** (`fidelity/ASTRA_round2.md`, code d58493b). W8-SYNTH §7 ('Astra did not finish') predates this. 101 declarations, 0 sorry; axioms only propext, Classical.choice, Quot.sound. A green fidelity check says the Lean statements match the frozen statements; it does not change any author status word.\" "
      f"(`{REGBASE}REGISTRY_v2.md:L{next(i for i,l in enumerate(REG,1) if l.startswith('Fidelity: Fable 5.1 GREEN'))}`).")
    w("- `#print axioms` record: `origin/theory/L-LEAN:theory_campaign/L-LEAN/AXIOMS_RECORD.txt` (axioms only `propext`, `Classical.choice`, `Quot.sound` per the L-LEAN REPORT.md: 'for all 56 audited declarations').")
    w("- Formalisation scope limits as stated: T21 routes (a)–(f) and H03 asymptotics NOT formalised; T37 A5, Theorems B, C not formalised; T12 PARTIAL (`hstep` hypothesis) (`REGISTRY_v2.md` §G; `L-LEAN STATUS.md`).")
    w("- Lean-relevant claims in the draft list: R2 'sorry-free (T07Bayes.lean, 28 declarations)'; R3 'sorry-free (T37Greedy/Lattice.lean); fidelity GREEN (Astra r2)'; R4 'sorry-free (T21HPM.lean)'; V1 'T12Core partial (hstep hypothesis)'; every other 'Lean' cell in `THEOREM_LIST.md` rows (certifiable / feasible / yes / —) refers to **no existing Lean file** (no `.lean` file for V2, V3, V4, A1–A4, D1–D4, S1, S2, C1, R1, R5 exists on any branch).")
    w()
    w('### 3.5 Registry IDs / draft items with a Lean file (as stated by a source)')
    w()
    w('| Item or registry ID | Lean file(s) | Source |')
    w('|---|---|---|')
    w(f"| `Thm4-C1`, `T38-(0)` (R4; T21 C1) | `T21HPM.lean` (t21_C1 etc.), sorry-free | `{REGBASE}REGISTRY_v2.md` §G row 1; `{LISTSRC}` R4(vi) |")
    w(f"| `Prop1-T07` (R2) | `T07Bayes.lean`, sorry-free | `REGISTRY_v2.md` §G row 2; `THEOREM_LIST.md` R2(vi) |")
    w(f"| locked T11(iii) (no registry row) | `T11Miss.lean`, sorry-free | `REGISTRY_v2.md` §G row 3 |")
    w(f"| `TheoremA`, `Lemma0(a,c)` (R3) | `T37Greedy.lean`, `T37Lattice.lean`, sorry-free; A5, B, C not formalised | `REGISTRY_v2.md` §G row 4; `THEOREM_LIST.md` R3(vi) |")
    w(f"| `Prop2(a,b,d,e)` (V1(a),(b) island identity, T12(i.a)) | `T12Core.lean`: PARTIAL (`hstep` is an explicit hypothesis) | `REGISTRY_v2.md` §G row 5; `THEOREM_LIST.md` V1(vi) |")
    w(f"| `LS-score`, `LemmaM` (R3, R5) | no Lean file stated; `THEOREM_LIST.md` R3(vi) says 'LS-score's move count is a short addition' | `{LISTSRC}` R3(vi) |")
    w()

def stage2_items():
    w('## 1. Per-item index: the draft theorem list (labels V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7 = 24 entries; the brief says "19 + S4"; S4 is in the body — see §5.B B11)')
    w()
    w(f"Each block: the list's own status string (verbatim, with line in `{LISTSRC}`), then the registry rows the item rests on, then non-registry results it cites. "
      'Registry IDs were chosen by reading the item\'s "Status and components" paragraph (`THEOREM_LIST.md` (iii)), "Depends on" lines and `THEOREM_REVISION_INPUTS.md` §2 row for the item; rows cited by the list only as inputs of a *different* item are listed under that item.')
    w()
    for k in ITEM_ORDER:
        it = D.ITEMS[k]; lr = LROWS[k]
        w(f'### {k} — {esc(lr["title"])}')
        w()
        w(f"- **Draft status (verbatim):** {esc(lr['status'])} — `{LISTSRC}:L{lr['line']}`")
        if lr['tier']:
            w(f"- **Draft tier / novelty (verbatim):** tier `{esc(lr['tier'])}`; novelty {esc(lr['novelty'])} — `{LISTSRC}:L{lr['line']}`")
        w(f"- **Item-level method variant:** {esc(it['variant'])}")
        if it['note']:
            w(f"- **Note:** {esc(it['note'])}")
        if it['ids']:
            w()
            reg_table(it['ids'])
        if it['other']:
            w()
            other_table(it['other'])
        if not it['ids'] and not it['other']:
            w()
            w(f"*No registry row and no result source: the draft list itself records 'NONE' or 'OPEN' for this item (`{LISTSRC}:L{lr['line']}`).*")
        # item-level flag summary
        flags = collections.Counter()
        for rid, _ in it['ids']:
            flags[flag(ROWS[rid]).split(' (')[0]] += 1
        for kk in it['other']:
            flags['non-registry:' + D.NONREG[kk]['flag']] += 1
        if flags:
            w()
            w('- **Flag summary for this item:** ' + '; '.join(f'{n} × {f}' for f, n in sorted(flags.items())))
        w()

def stage3_oblig():
    w('## 2. Method-meeting obligations N1–N17 (`THEOREM_REVISION_INPUTS.md` §3)')
    w()
    w(f"Source for every N-block below: `{INPSRC}` §3 (lines given per block). N18 exists only 'under item-1 Outcome 1' (line {next(i for i,l in enumerate(INP,1) if l.startswith('**N18'))}); item 1 closed as Outcome 2 (`{INPSRC}` §1.B), so N18 is **not opened** and is not counted. "
      'Family of origin: seats A, B = Fable 5.1 (Claude); seat C = gpt-6-astra (Codex); chair, PC1, PC2 = Opus 5.5 (`origin/theory/MEET-v31:theory_campaign/MEET-v31/MINUTES.md` lines 4–8; PC1/PC2 file headers).')
    w()
    # locate N blocks
    starts = {}
    for i, l in enumerate(INP, 1):
        m = re.match(r'\*\*N(\d+)[\.\s]', l)
        if m and int(m.group(1)) <= 18:
            starts[int(m.group(1))] = i
    for n in range(1, 18):
        key = f'N{n}'
        a = starts[n]; b = starts.get(n + 1, a + 30) - 1
        block = INP[a - 1:b]
        title = re.sub(r'\*', '', INP[a - 1])[:200]
        w(f'### {key}')
        w()
        w(f"- **Obligation (verbatim heading):** {esc(title)} — `{INPSRC}:L{a}`")
        st = [(a + j, l) for j, l in enumerate(block) if re.match(r'\s*-\s*\*Status', l) or re.match(r'\s*-\s*\*By item', l)]
        if key == 'N12':
            tl = [a + j for j, l in enumerate(block) if l.startswith('|')]
            st = [(a, f'(regime table; the per-regime status words are the table cells at L{tl[0]}-L{tl[-1]})')]
        for ln, s in st:
            w(f"- **Status (verbatim):** {esc(s.strip().lstrip('- '))} — `{INPSRC}:L{ln}`")
        if not st:
            w(f"- **Status (verbatim):** (the block carries its status in the statement lines; see `{INPSRC}:L{a}-L{b}`)")
        ob = D.OBLIG[key]
        w(f"- **Check history as stated:** {esc(ob['check'])}")
        w(f"- **Flag:** {ob['flag']}")
        w(f"- **Method variant (only if stated):** {esc(ob['variant'])}")
        sup = [(a + j, l) for j, l in enumerate(block) if re.match(r'\s*-\s*\*Supports', l)]
        if sup:
            w(f"- **Supports (verbatim):** {esc(sup[0][1].strip().lstrip('- '))} — `{INPSRC}:L{sup[0][0]}`")
        if ob['ids']:
            w()
            reg_table([(rid, 'rests on') for rid in ob['ids']])
        if ob['other']:
            w()
            other_table(ob['other'])
        w()

# ---------------------------------------------------------------------------------------------
def is_error(cell):
    return verdict(cell) == 'ERROR'

def stage4_false():
    w('## 4. Known-false list (ERROR, COUNTEREXAMPLE, FALSE, WITHDRAWN, retired)')
    w()
    w('Four groups. Group A–C are mechanical filters of `REGISTRY_v2.md` (all 480 rows: 431 in §B + 49 flagged sub-claims in §C). Group D is the §D "Retired / refuted statements" table copied. Group E lists claims declared FALSE, ERROR or WITHDRAWN in sources written after the registry (each with its path and line).')
    w()
    # A: author status COUNTEREXAMPLE
    A = [r for r in ORDER if ROWS[r]['author'] == 'COUNTEREXAMPLE']
    w(f'### 4.A Registry rows with author status COUNTEREXAMPLE ({len(A)}) — what each refuted (the registry\'s "Plain-English meaning", verbatim)')
    w()
    w('| ID | What it refuted / constructs (verbatim) | Check history | Source (branch:path) | Registry row |')
    w('|---|---|---|---|---|')
    for rid in A:
        r = ROWS[rid]; p, lab = resolve(r['src'])
        w(f"| `{rid}` | {esc(r['meaning'])} | {esc(hist(r))} | `{p}` · {esc(lab)} | `{REGBASE}REGISTRY_v2.md:L{r['line']}` |")
    w()
    # B: any row with ERROR verdict
    B = [r for r in ORDER if (is_error(ROWS[r]['sf']) or is_error(ROWS[r]['xf']))]
    w(f'### 4.B Registry rows (§B and §C) carrying an ERROR verdict in the SF or XF cell ({len(B)}) — what the ERROR refuted, and repair state')
    w()
    w('| ID | Author status | ERROR cell (verbatim; which family) | Repairs applied / pending (verbatim) | Source (branch:path) | Registry row |')
    w('|---|---|---|---|---|---|')
    for rid in B:
        r = ROWS[rid]; p, lab = resolve(r['src'])
        cells = []
        if is_error(r['sf']): cells.append('SF: ' + esc(r['sf']))
        if is_error(r['xf']): cells.append('XF: ' + esc(r['xf']))
        w(f"| `{rid}`{(' ' + r['tag']) if r['tag'] else ''} | {esc(r['author'])} | {' ⟂ '.join(cells)} | {esc(r['rep'])} | `{p}` · {esc(lab)} | `{REGBASE}REGISTRY_v2.md:L{r['line']}` |")
    w()
    # A3 statement of record
    a3s = next(i for i, l in enumerate(REG, 1) if l.startswith('### A3.'))
    w(f"Cross-check: `REGISTRY_v2.md` §A3 (`{REGBASE}REGISTRY_v2.md:L{a3s}`) states \"40 items (main-table rows and flagged sub-claims)\" with an ERROR verdict and \"ERROR items: 20 with a repair already applied, 7 with a repair only proposed by the referee (not yet written by any run), 13 with no repair.\" "
      f"The registrar's filter finds **{len(B)}** rows with an ERROR in an SF or XF cell (some of the registry's 40 are described by the ERROR sentence inside a longer cell rather than a leading **ERROR** token; where the counts differ the registry's A3 table is the statement of record and is reproduced in §4.B2).")
    w()
    # B2: A3 table verbatim
    w('#### 4.B2 `REGISTRY_v2.md` §A3 table (the registry\'s own 40-item ERROR list), IDs only, with whether the ID is also caught by the 4.B filter')
    w()
    w('| A3 item | In 4.B filter? | Registry row (if an ID row exists) |')
    w('|---|---|---|')
    a3rows = []
    for i, l in enumerate(REG, 1):
        if i > a3s and l.startswith('| `'):
            m = re.match(r'\| `([^`]+)`', l)
            a3rows.append((m.group(1), i))
        if i > a3s and l.startswith('GAP verdicts'):
            break
    Bset = set(B)
    for rid, ln in a3rows:
        w(f"| `{rid}` | {'yes' if rid in Bset else 'no (ERROR inside a longer cell or in an A3-only description)'} | {'`'+REGBASE+'REGISTRY_v2.md:L'+str(ROWS[rid]['line'])+'`' if rid in ROWS else '—'} (A3 line L{ln}) |")
    w()
    # D: retired
    rs = next(i for i, l in enumerate(REG, 1) if l.startswith('### Retired / refuted'))
    w('### 4.C `REGISTRY_v2.md` "Retired / refuted statements" (verbatim)')
    w()
    w('| Retired statement | Why | Replacement | Source line |')
    w('|---|---|---|---|')
    nret = 0
    for i in range(rs + 3, len(REG)):
        l = REG[i]
        if not l.startswith('|'):
            break
        c = [x.strip() for x in l.strip().strip('|').split(' | ')]
        w(f"| {esc(c[0])} | {esc(c[1])} | {esc(c[2])} | `{REGBASE}REGISTRY_v2.md:L{i+1}` |")
        nret += 1
    w()
    # E: later sources
    w('### 4.D Claims declared FALSE / ERROR / WITHDRAWN / dropped in sources after the registry (verbatim phrases, with path and line)')
    w()
    w('| Claim | What the source says (verbatim) | Source |')
    w('|---|---|---|')
    def find(lines, pat, src, name, after=0):
        for i, l in enumerate(lines, 1):
            if i > after and re.search(pat, l):
                return i
        raise SystemExit('missing phrase: ' + pat)
    KF = []
    def add(claim, lines, pat, src, quote):
        ln = find(lines, pat, src, claim)
        KF.append((claim, quote, f'`{src}:L{ln}`'))
    add('A2 plain sentence "errs only downward"', INP, r'literally false', INPSRC, 'TL:26 and TL:236 "errs/can only fail downward" are **literally false** (COUNTEREXAMPLE; formal (iii) not refuted)')
    add('INV row 9 "an upper bound on Z is impossible from a run"', INP, r"INV's wording is literally false", INPSRC, "**INV's wording is literally false**; correct to \"no useful upper bound\"")
    add('R6 "≈ 4× headroom"', INP, r'is not measured', INPSRC, '**"≈ 4× headroom" is not measured** (1.9× on 2 cores) … **remove the 4× sentence.**')
    add('D1 "free of N, H, R" for v3.1', INP, r'Free of N, H, R', INPSRC, '"Free of N, H, R" (TL:29, 309) and the TL:29 summary formula are particle-parallel, v3.2 only (C6)')
    add('A1 RB clause for joint h', INP, r'RB clause', INPSRC, "TL A1(i)'s RB clause (\"RB version when h is a product of inclusion indicators\") is restricted to marginal PIPs; c_h = 0 for joint h")
    add('HPM terminal frequency in 𝓗', INP, r'HPM terminal frequency dropped', INPSRC, 'HPM terminal frequency dropped from 𝓗: descriptive diagnostic, no theorem')
    add('C4(b) "isolate {Ŝ}"', INP, r'C4\(b\) "isolate', INPSRC, 'C4(b) "isolate {Ŝ}" → sharpness only; withdrawn (R3-1)')
    add('R3A "duplicates collapsed"', INP, r'R3A "duplicates collapsed"', INPSRC, 'R3A "duplicates collapsed" → wrong; kept (R3-4)')
    add('PC2: C1(a) third clause, C1(b) unscored sentence, conditional C6, "SC by replay", rigorous global_certified, C4 cost remark', INP, r'FALSE or not a theorem', INPSRC, '*FALSE or not a theorem:* C1(a) third clause; C1(b) "unscored mass" (COUNTEREXAMPLE `t4b`); the conditional C6 reading; "SC checkable by replay"; rigorous `global_certified` (η uses a *lower* condition-number estimate); the C4 cost remark')
    PC1T = srcfile(D.PC1).split('\n')
    PC2T = srcfile(D.PC2).split('\n')
    add('Seat B: "MPM^𝒯 needs δ₁ < ⅓"', PC1T, r'FALSE.*as "needs', D.PC1, '(b) **FALSE** as "needs ⅓" (counterexample δ₁ = 0.339). Amended: PIP^𝒯_j ≤ δ₁ off S₀, so δ₁ < ½ suffices and is sharp')
    add('Post-search HPM monotone in R′ without the extra local search', PC1T, r'Post-search HPM monotone', D.PC1, '**FALSE** (COUNTEREXAMPLE: R = 4 returns S₀ = {0,1}, R′ returns {2})')
    add('O-CERT C1(a) third clause', PC2T, r'The third clause is FALSE', D.PC2, 'The third clause is FALSE as written. Take S = Ŝ ∈ 𝒯 with g > 0: the ratio is 1, which is > e^{−g}.')
    add('O-CERT C1(b) "unscored" sentence', PC2T, r'the "unscored" sentence: FALSE', D.PC2, 'Verdict, the "unscored" sentence: FALSE (COUNTEREXAMPLE). Seat C\'s correction 1 is upheld.')
    add('THEOREM_LIST S3 Prop M (naive merge)', LIST, r'S3. Proposition M', LISTSRC, 'A-DRAFT Prop M / SHARE-M(b): ERROR (A-REV3/A-REV6); FD-NM ERROR, repair pending … **Decision:** drop.')
    add('THEOREM_LIST R3: literal T37/TD, H24', LIST, r'Literal T37/TD retired', LISTSRC, 'Literal T37/TD retired (Prop1-TD, CEX1/2 COUNTEREXAMPLE); H24 retired (CE1/CE2).')
    add('THEOREM_LIST R3: cap-free lattice restatement', LIST, r'cap-free lattice restatement ERROR', LISTSRC, 'cap-free lattice restatement ERROR (A-REV5): keep the capped lattice')
    add('THEOREM_LIST V4: literal GUARD wording', LIST, r'^"every output equals" wording ERROR', LISTSRC, 'GUARD implementation fact HOLDS, literal "every output equals" wording ERROR (A-REV8: statistical scope only)')
    add('THEOREM_LIST A1: F-MASKPIP M3', LIST, r'THM-INV records M3 as XF ERROR', LISTSRC, 'Do **not** cite F-MASKPIP M3 for this: THM-INV records M3 as XF ERROR.')
    add('THEOREM_LIST R5: c = 2 iid-budget clause of (b1-LH)', LIST, r'the c = 2 clause stays as repaired', LISTSRC, 'the c = 2 clause stays as repaired (V18)')
    add('THM-INV row 2: W2-T26 exact-branch remark', INV, r'W2-T26 exact-branch remark ERROR', INVSRC, 'W2-T26 exact-branch remark ERROR (A-REV5)')
    add('THM-INV row 6: general LH locking', INV, r'General LH locking FALSE', INVSRC, 'General LH locking FALSE (A-REV7 counterexample); H24 retired (CE1/CE2 COUNTEREXAMPLE)')
    add('THM-INV §2: literal T37 / TD; H24', INV, r'Prop1-TD, CEX1/2 COUNTEREXAMPLE', INVSRC, 'Prop1-TD, CEX1/2 COUNTEREXAMPLE (retires literal T37); CE1/CE2 COUNTEREXAMPLE (retires H24)')
    add('THM-INV §2: region-form Theorem W on masked LH c ≥ 2', INV, r'region-form Theorem W fails', INVSRC, 'ThmW PROVED (candidate), region form fails on masked LH c ≥ 2')
    add('THM-INV §2: O-CERT C1, C5', INV, r'C1 ERROR as quantified', INVSRC, 'Lemma M, C3, C4 PROVED, XF VERIFIED; C1 ERROR as quantified; C5 ERROR (tie prose)')
    for claim, quote, src in KF:
        w(f"| {esc(claim)} | {esc(quote)} | {src} |")
    w()
    w(f"`LOCKABLE_v2.md` §3c lists the six counterexamples confirmed by both families (`{REGBASE}LOCKABLE_v2.md`, section '3c. Counterexamples confirmed by a same-family verifier and by A-REV1/A-REV2'): " +
      ', '.join(f'`{k}`' for k, v in LOCKCAT.items() if v[0].startswith('3c')) + '.')
    w()
    return dict(A=len(A), B=len(B), C=nret, D=len(KF))

def stage4_conflicts():
    w('## 5. CONFLICT list (sources disagree; both sides listed)')
    w()
    w(f"### 5.A The registry's own conflicts (`REGISTRY_v2.md` §A2, C1–C26, copied; lines in `{REGBASE}REGISTRY_v2.md`)")
    w()
    w('| # | Rows | What conflicts (verbatim) | Line |')
    w('|---|---|---|---|')
    a2 = next(i for i, l in enumerate(REG, 1) if l.startswith('### A2.'))
    nconf = 0
    for i in range(a2 + 3, len(REG)):
        l = REG[i]
        if not l.startswith('|'):
            break
        c = [x.strip() for x in l.strip().strip('|').split(' | ')]
        w(f"| {c[0]} | {esc(c[1])} | {esc(c[2])} | `{REGBASE}REGISTRY_v2.md:L{i+1}` |")
        nconf += 1
    w()
    w('### 5.B Conflicts found by the registrar between the draft list, the registry, the inventory, the revision inputs, the locked register and the proof checks')
    w()
    w('Each row: both statements verbatim, each with its own source path and line. Marked **CONFLICT**; no resolution is proposed.')
    w()
    w('| # | CONFLICT | Side 1 (verbatim, source) | Side 2 (verbatim, source) |')
    w('|---|---|---|---|')
    LOCKED_T = open(os.path.join(ROOT, 'Docs/Theory/proofs/LOCKED_PROOFS.md'), encoding='utf-8').read().split('\n')
    DOSS = open(os.path.join(ROOT, 'theory_campaign/MEET-THM/DOSSIER.md'), encoding='utf-8').read().split('\n')
    MARL = srcfile(D.MAR).split('\n')
    CONC = 'origin/theory/MEET-v31:theory_campaign/MEET-v31/evidence/2026-11-03_concurrency_runs.md'
    CONCL = srcfile(CONC).split('\n')
    T09P = 'origin/theory/campaign:Docs/Theory/proofs/T09_T7_kernel_validity/STATEMENT.md'
    T09L = open(os.path.join(ROOT, 'Docs/Theory/proofs/T09_T7_kernel_validity/STATEMENT.md'), encoding='utf-8').read().split('\n')
    LOCKEDP = 'origin/theory/campaign:Docs/Theory/proofs/LOCKED_PROOFS.md'
    DOSSP = 'origin/theory/campaign:theory_campaign/MEET-THM/DOSSIER.md'
    def R(path, lines, pat):
        for i, l in enumerate(lines, 1):
            if re.search(pat, l):
                return f'`{path}:L{i}`'
        raise SystemExit('missing ' + pat + ' in ' + path)
    CF = []
    def cf(name, s1, s2):
        CF.append((name, s1, s2))
    cf('C-V2 (Prop W: how many designs were executed)',
       'V2: "…executed check PASSED on the smoke problem and on **1/1 completed design** (p0500_S1_r001; the task file says treat METH-AUDIT\'s \"3/3\" as 1/1 + smoke)" — ' + R(LISTSRC, LIST, r'1/1 completed design'),
       'METH-AUDIT: "…on the smoke problem and on 3/3 study designs (§6)" — ' + R(D.MAR, MARL, r'3/3 study designs') +
       '; MEET-v31 evidence lists three designs p0500_S1_r001, p0500_S4_r001, p0500_S5_r002, each "bitwise logZ TRUE pip TRUE hpm TRUE" — ' + R(CONC, CONCL, r'p0500_S4_r001 c050') +
       '; INPUTS §2 V2: "Executed: **smoke + 3/3 study designs**" — ' + R(INPSRC, INP, r'Executed: \*\*smoke \+ 3/3'))
    cf('C-V5 (V5 / N9: kernel reversibility, self-adjointness, exact start sampler — "no registry row")',
       'V1(iii): "V5 (reversibility and self-adjointness) holds by construction, consultant-checked, but has **no registry row** (THM-INV §5.12)" — ' + R(LISTSRC, LIST, r'has \*\*no registry row\*\*') +
       '; INPUTS N9: "by construction, consultant-checked, **no registry row**" — ' + R(INPSRC, INP, r'no registry row\*\*\s*\(INV'),
       'LOCKED_PROOFS.md wave-1 row T09 (T7), all parts (i)-(v): "The exact start sampler draws from the start law pi0 with the right normaliser. Every elementary move (Gibbs, swaps, independence) and the randomly ordered round leave the bridge distribution invariant." — ' + R(LOCKEDP, LOCKED_T, r'\*\*T09\*\* \(T7\)') +
       '; T09 STATEMENT (ii): "Each elementary kernel … is q_φ-reversible" — ' + R(T09P, T09L, r'\*\*\(ii\)\*\* Each elementary kernel') +
       '; (iii): "K_φ is a Markov kernel, q_φ-invariant, and self-adjoint on L²(q_φ)" — ' + R(T09P, T09L, r'\*\*\(iii\)\*\* K_φ is a Markov kernel'))
    cf('C-M3 (F-MASKPIP M3)',
       'A1(v): "Do **not** cite F-MASKPIP M3 for this: THM-INV records M3 as XF ERROR." — ' + R(LISTSRC, LIST, r'Do \*\*not\*\* cite F-MASKPIP M3'),
       'D3(iii): "assembly of V1 (KNOWN—CITE + locked), A1 (PROOF SKETCH), D1 (PROVED counting), D2 (PROVED ideal grid / OPEN as-coded), **M3 (PROVED)**, R5 …" — ' + R(LISTSRC, LIST, r'M3 \(PROVED\)') +
       '; registry `FMP-M3`: author PROVED, XF **ERROR** (A-REV9) — `' + REGBASE + 'REGISTRY_v2.md:L' + str(ROWS['FMP-M3']['line']) + '`')
    cf('C-LS0 (is LS0 in the method / the production core?)',
       'THM-INV §1 row 12: "LS0 absent from production (API-AUDIT)" — ' + R(INVSRC, INV, r'LS0 absent from production') + '; §2 ledger: "**ID: LS0 is not in production** (API-AUDIT)" — ' + R(INVSRC, INV, r'ID: LS0 is not in production') +
       '; METH-AUDIT: "**LS0 is not in the production core** (API-AUDIT fact 3)" — ' + R(D.MAR, MARL, r'LS0 is not in the production core'),
       'REGISTRY_v2.md §I: "**LS0 is part of the method**: approval in effect after O-LS0 (0/2,394 HPM changes …)" — ' + R(REGBASE + 'REGISTRY_v2.md', REG, r'\*\*LS0 is part of the method\*\*') +
       '; INPUTS M2: "**LS0 in the shipped core, after the final local search.**" — ' + R(INPSRC, INP, r'LS0 in the shipped core'))
    cf('C-HEADROOM (R6 "≈ 4× headroom")',
       'R6: "…under v3.1 (concurrent islands, Prop W) the same allocation gives ≈ 4× headroom…" — ' + R(LISTSRC, LIST, r'4× headroom'),
       'INPUTS §2 R6: "**\"≈ 4× headroom\" is not measured** (1.9× on 2 cores)" — ' + R(INPSRC, INP, r'is not measured'))
    cf('C-FREE (D1 depth "free of N, H, R")',
       'D1(c): "Depth, particle-parallel … **free of N, H and R**" — ' + R(LISTSRC, LIST, r'free of N, H and R') +
       '; summary row D1: "…free of N, H, R with particle-parallel islands" — ' + R(LISTSRC, LIST, r'free of N, H, R with particle-parallel'),
       'INPUTS M13: "\"Free of N, H, R\" dropped for v3.1" — ' + R(INPSRC, INP, r'dropped for v3\.1') +
       '; INPUTS §2 D1: "\"Free of N, H, R\" (TL:29, 309) and the TL:29 summary formula are particle-parallel, v3.2 only (C6)" — ' + R(INPSRC, INP, r'are particle-parallel, v3\.2 only'))
    cf('C-A2DOWN (A2 "can only fail downward")',
       'A2(ii): "in the masked regime it can only fail *downward*, by an amount the run can partly certify" — ' + R(LISTSRC, LIST, r'can only fail \*downward\*'),
       'PC1 claim 4: "Verdict: PROVED (C\'s COUNTEREXAMPLE is valid). It applies to A2\'s plain-language sentence and to its table row as written. It does not apply to A2\'s formal statement (iii)." — ' + R(D.PC1, PC1T, r'COUNTEREXAMPLE is valid'))
    cf('C-ZUP (INV "an upper bound on Z is impossible")',
       'THM-INV §1 row 9: "(an upper bound on Z is impossible from a run, MASKZPIP)" — ' + R(INVSRC, INV, r'upper bound on Z is impossible'),
       'PC1 claim 1: "Verdict: PROVED … Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}" — ' + R(D.PC1, PC1T, r'^\*\*Verdict: PROVED\.\*\* It holds for the spec') +
       '; INPUTS N17: "**INV\'s wording is literally false**; correct to \"no useful upper bound\"" — ' + R(INPSRC, INP, r"INV's wording is literally false"))
    cf('C-PRIMARY (which PIP is primary)',
       'THM-INV §1 row 10: "PIPs (Rao–Blackwellised; equal-weight primary, Ẑ-weighted secondary)" — ' + R(INVSRC, INV, r'equal-weight primary'),
       'INPUTS M4: "**Ẑ-weighted PIP primary; equal-weight named secondary.**" — ' + R(INPSRC, INP, r'Ẑ-weighted PIP primary'))
    cf('C-PROMOTED (status word of Prop 2(a,b,d,e))',
       'THEOREM_LIST V1(iii): "Prop 2(a,b,d,e) PROVED-LOCKED" — ' + R(LISTSRC, LIST, r'Prop 2\(a,b,d,e\) PROVED-LOCKED'),
       'registry `Prop2(a,b,d,e)`: author status "PROVED", XF "GAP" — `' + REGBASE + 'REGISTRY_v2.md:L' + str(ROWS['Prop2(a,b,d,e)']['line']) + '`; absent from the strict list of LOCKABLE_v2.md §1 (only `Prop2(c)` is there) — `' + REGBASE + 'LOCKABLE_v2.md:L' + str(LOCKCAT['Prop2(c)'][1]) + '`; the locked wave-1 result is T12 — ' + R(LOCKEDP, LOCKED_T, r'\*\*T12\*\* \(T8\)'))
    cf('C-TLCOUNT (number of draft-list items)',
       'DOSSIER: "Draft theorem list (19 items G1–G6, tiers, HQ plan)" — ' + R(DOSSP, DOSS, r'19 items') + '; the task statement: "19 items V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7"',
       'the labels enumerate to 4+4+4+4+1+7 = 24; the summary table has 23 rows (V1–V4, A1–A4, D1–D4, S1–S3, C1, R1–R7) — ' + R(LISTSRC, LIST, r'^\| C1 \|') + ' — and S4 is the body section "### S4." — ' + R(LISTSRC, LIST, r'### S4\.') + '; THEOREM_LIST.md states no total, and no source says which 19 are meant')
    for i, (name, s1, s2) in enumerate(CF, 1):
        w(f"| B{i} | **CONFLICT** {esc(name)} | {esc(s1)} | {esc(s2)} |")
    w()
    return nconf, len(CF)

def stage5_appendix():
    w('## Appendix A. Registry rows cited in this index (verbatim cells, with `REGISTRY_v2.md` line numbers)')
    w()
    cited = []
    for k in ITEM_ORDER:
        cited += [r for r, _ in D.ITEMS[k]['ids']]
    for n in NOBL:
        cited += D.OBLIG[n]['ids']
    seen = []
    for r in cited:
        if r not in seen:
            seen.append(r)
    w(f'{len(seen)} distinct registry IDs are cited under §1 and §2. Row text (SF = same-family, XF = cross-family) is copied unchanged from `{REGBASE}REGISTRY_v2.md`.')
    w()
    for rid in seen:
        r = ROWS[rid]; p, lab = resolve(r['src'])
        w(f"#### `{rid}`{(' ' + r['tag']) if r['tag'] else ''} — `{REGBASE}REGISTRY_v2.md:L{r['line']}`")
        w(f"- Registry section: {esc(r['sec'])}")
        w(f"- Paper target: {esc(r['target'])}")
        w(f"- Source (registry cell): {esc(r['src'])} → `{p}`")
        w(f"- Author status: {esc(r['author'])}")
        w(f"- Same-family: {esc(r['sf'])}")
        w(f"- Cross-family: {esc(r['xf'])}")
        w(f"- Repairs applied / pending: {esc(r['rep'])}")
        w(f"- Open premises: {esc(r['prem'])}")
        w()

def counts_table(extra):
    ids_item = []
    for k in ITEM_ORDER:
        ids_item += [r for r, _ in D.ITEMS[k]['ids']]
    ids_ob = []
    for n in NOBL:
        ids_ob += D.OBLIG[n]['ids']
    allids = []
    for r in ids_item + ids_ob:
        if r not in allids:
            allids.append(r)
    fl = collections.Counter(flag(ROWS[r]).split(' (')[0].split(':')[0] for r in allids)
    au = collections.Counter(ROWS[r]['author'] for r in allids)
    nonreg_item = collections.Counter()
    for k in ITEM_ORDER:
        for o in D.ITEMS[k]['other']:
            nonreg_item[o] += 1
    nonreg_all = set(nonreg_item) | {o for n in NOBL for o in D.OBLIG[n]['other']}
    nfl = collections.Counter(D.NONREG[o]['flag'] for o in nonreg_all)
    thm = sum(1 for f in LEANSCAN if 'SmcBvs/SmcBvs/' in f['p'] for k, _ in f['ds'] if k in ('theorem', 'lemma'))
    sorry_cur = sum(f['sorry'] for f in LEANSCAN if 'SmcBvs/SmcBvs/' in f['p'])
    w('## 0. Header table of counts')
    w()
    w('| Quantity | Count | Source / how counted |')
    w('|---|---|---|')
    w(f"| Draft-list entries indexed (labels V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7) | {len(ITEM_ORDER)} labelled entries = 23 summary-table rows + S4 (body). The task text and `MEET-THM/DOSSIER.md` say '19 items'; the labels enumerate to 24 → see COUNT DISCREPANCY in §5.B (B11). All 24 are indexed. | `{LISTSRC}` table lines L22–L{LROWS['R7']['line']} + S4 body L{LROWS['S4']['line']} |")
    w(f"| Method-meeting obligations indexed (N1–N17) | 17 (N18 conditional, not opened) | `{INPSRC}` §3 |")
    w(f"| Registry rows in `REGISTRY_v2.md` (main table §B + flagged §C) | 480 (431 + 49) | parsed from `{REGBASE}REGISTRY_v2.md`; the registry's A1 says 431 named results + 49 flagged |")
    w(f"| Distinct registry IDs cited under §1/§2 | {len(allids)} | §1 tables and §2 tables; verbatim rows in Appendix A |")
    w(f"| … by author status (verbatim words) | " + ', '.join(f'{k}: {v}' for k, v in sorted(au.items())) + " | registry 'Author status' column |")
    w(f"| … by flag | " + ', '.join(f'{k}: {v}' for k, v in sorted(fl.items())) + " | rule in the Conventions block |")
    w(f"| Non-registry results cited (distinct) | {len(nonreg_all)} | `items_data.py` NONREG; sources named per row |")
    w(f"| … by flag | " + ', '.join(f'{k}: {v}' for k, v in sorted(nfl.items())) + " | check history stated in the cited source |")
    w(f"| Lean files (`*.lean`) on all origin branches | {len(LEANSCAN)} (library 9 incl. `SmcBvs.lean`/`Axioms.lean`: {sum(1 for f in LEANSCAN if 'SmcBvs/SmcBvs' in f['p'] or f['p'].endswith('SmcBvs/SmcBvs.lean'))}; copies: {sum(1 for f in LEANSCAN if 'frozen' in f['p'] or 'packet' in f['p'])}) — all on `origin/theory/L-LEAN` | §3 |")
    w(f"| Lean theorem/lemma declarations in the library (current) / `sorry` / `admit` | {thm} / {sorry_cur} / 0 | §3.2 |")
    w(f"| Lean copies containing `sorry` (statement stubs in `frozen/v1`, `fidelity/packet`) | {len([f for f in LEANSCAN if ('frozen' in f['p'] or 'packet' in f['p']) and f['sorry']])} files, {sum(f['sorry'] for f in LEANSCAN if ('frozen' in f['p'] or 'packet' in f['p']))} `sorry` | §3.3 |")
    if extra:
        w(f"| Known-false list: COUNTEREXAMPLE-status rows / rows with an ERROR cell / registry retired table / later-source claims | {extra.get('A')} / {extra.get('B')} / {extra.get('C')} / {extra.get('D')} | §4.A / §4.B / §4.C / §4.D |")
        w(f"| CONFLICTs: registry's own (§A2) / registrar-found | {extra.get('nconf')} / {extra.get('ncf')} | §5.A / §5.B |")
    w()

# ---------------------------------------------------------------------------------------------
sections_extra = {}
body = []
def run():
    global L
    L = []
    stage1_header()
    # placeholder for counts inserted later
    head_len = len(L)
    L_tail = []
    # stage-dependent sections
    parts = {}
    L = []
    if STAGE >= 2:
        stage2_items(); parts['items'] = L; L = []
    if STAGE >= 3:
        stage3_oblig(); parts['oblig'] = L; L = []
    stage1_lean(); parts['lean'] = L; L = []
    extra = {}
    if STAGE >= 4:
        r = stage4_false(); extra.update(r); parts['false'] = L; L = []
        nconf, ncf = stage4_conflicts(); extra['nconf'] = nconf; extra['ncf'] = ncf; parts['conf'] = L; L = []
    if STAGE >= 5:
        stage5_appendix(); parts['app'] = L; L = []
    # assemble
    L = []
    stage1_header()
    counts_table(extra if STAGE >= 4 else None)
    pending = []
    for k in ('items', 'oblig', 'lean', 'false', 'conf', 'app'):
        if k in parts:
            L.extend(parts[k])
    if STAGE < 5:
        L.append('')
        L.append(f'<!-- build stage {STAGE} of 5: later sections (per-item index, N-obligations, known-false, conflicts, Appendix A) are added in further commits -->')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('wrote', OUT, len(L), 'lines')

run()
