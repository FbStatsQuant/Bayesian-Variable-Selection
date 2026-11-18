"""Builder of the API blind-audit card D5P1 (ticket W3-D5P, track D #5') for HQ — pattern of API_AUDIT/audit1 (dept/theory).

Blind Fable referee of the three W3-D5P claims (LIST-K, LIST-CODE, LIST-R): "Break the proof; findings only."
Every excerpt is taken with `git show <commit>:<path>` at the pinned commits below (byte-reproducible), numbered with its
original line numbers, and scrubbed of status words and review markers; the build FAILS if a forbidden word survives.
No API call is made here and no key is read. Submission: HQ, with API_AUDIT/audit_batch.py (count / submit / wait).

Usage (from the repository root of the W3-D5P worktree):
    python Theory_work/Wave3/W3-D5P/reviews/api_card/d5p_card_build.py build [--commit <sha>]
writes SYSTEM.md, REQ_d5p.md, requests.json, REQUESTS.tsv, MANIFEST.tsv, USAGE.txt next to this file.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = 'Theory_work/Wave3/W3-D5P'
MODEL, MAX_TOKENS, SAMPLES = 'claude-fable-5-2', 32000, 2
FORBID = ['PROVED', 'CHECKED', 'CODE-READ', 'council', 'PASS', 'VERIFIED', 'AUDITED', 'Opus', 'Fable', 'Astra', 'Sol ',
          'seat', 'LC1', 'SL1-', 'MANIFEST', 'REFUTED', 'disposition']
CLAIMS = ['LIST-K', 'LIST-CODE.i', 'LIST-CODE.ii', 'LIST-CODE.iii', 'LIST-CODE.iv', 'LIST-CODE.v',
          'LIST-R.i', 'LIST-R.ii', 'LIST-R.iii']

SYSTEM = """You are a blind, independent referee of mathematical proofs about a Bayesian variable-selection method
(Gaussian linear regression, p ≤ n^A, often p ≫ n) and of a code reading of its implementation. You receive, verbatim
with their original line numbers: a statement file with three claims, their three proof files, the definition of the
output fields the claims are about, the excerpts of the earlier results the proofs consume (as stated; take their
statements as given), and the excerpts of the source code that the code-reading proof cites. Status labels and review
markers have been removed. Bracketed tags such as [R-1] are editorial; ignore them.

Your job is to break the proofs. For each claim listed in the task, either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason: a step that does not follow (say which line and why), a counterexample, a quantifier
  error (every run / one data event / every n; which branch), a hypothesis used but not stated, a citation that does not
  say what the proof needs (exact file:line), or — for the code reading — a code path the proof misses (quote the line).
- UNCLEAR only when the texts given cannot settle it; name the passage or fact you would need.
Judge only the texts given; do not rely on memory of other documents. All results are asymptotic in n unless marked
deterministic; exact arithmetic is assumed throughout (a named idealisation, not a defect). Do not report style,
wording, presentation or possible improvements, and do not propose stronger theorems.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR claim, a short section headed by its claim id with the problem, the exact
   references and the counterexample or missing passage. Write nothing for a NO FINDING claim.
2. Then exactly one line per claim listed in the task, in the listed order, and nothing after the last one:
AUDIT D5P1 <claim> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>"""

# (key, path, spans or None = whole file, note); paths at the pinned commit
SOURCES = [
    ('ST', f'{T}/STATEMENT.md', None, 'the statement file (claims (C1) LIST-K, (C2) LIST-CODE, (C3) LIST-R)'),
    ('L1', f'{T}/lemmas/L1_listK.md', None, 'proof of LIST-K'),
    ('L2', f'{T}/lemmas/L2_listCODE.md', None, 'proof of LIST-CODE (code reading)'),
    ('L3', f'{T}/lemmas/L3_listR.md', None, 'proof of LIST-R'),
    ('SPEC', f'{T}/sources/SPEC_LIST_PIP_523dda23.md', None, 'definition of the output fields'),
    ('RM2R', 'Theory_work/Wave3/W3-RM2-R/STATEMENT.md', [(33, 60), (116, 163), (177, 182)], 'consumed: RM0-plus, DLV-0, RM2-R-plus (as stated)'),
    ('RM', 'Theory_work/Wave3/W3-RM/STATEMENT.md', [(32, 68), (94, 136)], 'consumed objects, events, configuration, Form R hypotheses'),
    ('RM2', 'Theory_work/Wave3/W3-RM2/STATEMENT.md', [(60, 68), (96, 104), (172, 218)], 'code pins of the local search; interface table; Form R'),
    ('DLV4', 'Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md', [(60, 77)], 'the pathwise reporting step'),
    ('DLV2', 'Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md', [(20, 35)], 'scorer never fails (Lemma S.2)'),
    ('SAMP', 'Theory_work/Wave3/W3-SAMP/STATEMENT.md', [(36, 62)], 'objects of the sampler (𝓜, Ŝ)'),
    ('CC', 'Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md', [(40, 63), (88, 100)], 'consumed code facts CC2, CC5'),
    ('POST', 'Theory_work/Wave2/W2-APP/lemmas/L1_POST.md', [(1, 33)], 'consumed posterior rate (Lemma POST)'),
    ('DIST', 'Theory_work/Wave3/W3-DIST/STATEMENT.md', [(289, 318)], 'context: the two links'),
    ('READER', 'Theory_work/Wave3/W3-READER/READER_VERSIONS.md', [(660, 712), (752, 760)], 'reader Theorem 6 and its bridges'),
    ('C:run', 'Scripts/SMC_BVS/core/v3_run.R', [(84, 163), (205, 229)], 'code'),
    ('C:fit', 'Scripts/SMC_BVS/core/v3_fit.R', [(73, 174)], 'code'),
    ('C:exact', 'Scripts/SMC_BVS/core/v3_exact.R', None, 'code'),
    ('C:pre', 'Scripts/SMC_BVS/core/v3_preprocess.R', [(97, 120)], 'code'),
    ('C:ledger', 'Scripts/SMC_BVS/core/cpp/v3_ledger.h', None, 'code'),
    ('C:engine', 'Scripts/SMC_BVS/core/cpp/v3_engine.h', [(86, 110), (269, 300), (375, 422)], 'code'),
    ('C:core', 'Scripts/SMC_BVS/core/cpp/v3_core.cpp', [(25, 46), (318, 330), (356, 389), (391, 568)], 'code'),
    ('C:score', 'Scripts/SMC_BVS/core/cpp/v3_score.h', [(36, 72), (255, 297)], 'code'),
    ('C:start', 'Scripts/SMC_BVS/core/cpp/v3_start.h', [(75, 97), (165, 178), (255, 308)], 'code'),
    ('C:util', 'Scripts/SMC_BVS/core/cpp/v3_util.h', [(115, 131)], 'code'),
    ('C:blocks', 'Scripts/SMC_BVS/core/cpp/v3_blocks.h', [(136, 144)], 'code'),
]
QUOTE_RE = re.compile(r'"[^"]*?(?:PROVED|CHECKED|AUDITED|council|PASS|MANIFEST|seat)[^"]*?"', re.S)
PAREN_RE = re.compile(r'\s?\((?:[^()]*?\b(?:Opus|Sol|Astra|Fable|LC1|LC1R|SW1|AUDITED|seats?)\b[^()]*?)\)')
TOKEN_RE = re.compile(r'\b(?:SL1|LC1R?|SC1)-\d+:?\s*|\s?\[(?:SL1|LC1R?|SC1|R1|R2|R3|RM2R|REG|S1|S2|H5|D\d+)[^\]]*\]')
WORDS = [('EXISTS-CHECKED', 'EXISTS'), ('PROVED-CHECKED', '[status omitted]'), ('CODE-CHECKED', '[status omitted]'),
         ('HQ disposition', 'HQ note'), ('audit Fable, ', '')]
FALLBACK = '[review record omitted]'
nfallback = []


def keep_newlines(m):
    return '[status omitted]' + '\n' * m.group(0).count('\n')


def git_show(commit, path):
    return subprocess.run(['git', 'show', f'{commit}:{path}'], capture_output=True, check=True).stdout


def scrub_text(t, key):
    t = QUOTE_RE.sub(keep_newlines, t)
    t = PAREN_RE.sub('', t)
    t = TOKEN_RE.sub('', t)
    for x, y in WORDS:
        t = t.replace(x, y)
    out = []
    for i, ln in enumerate(t.split('\n'), 1):
        if any(w in ln for w in FORBID):
            nfallback.append((key, i, ln)); ln = FALLBACK
        out.append(ln)
    return out


def excerpt(commit, key, path, spans, note):
    raw = git_show(commit, path)
    L = scrub_text(raw.decode('utf-8'), key)
    if key == 'ST':   # the statement without its header paragraph (protocol/record) and its changelog
        a = next(i for i, x in enumerate(L, 1) if x.startswith('**Sources'))
        b = next(i for i, x in enumerate(L, 1) if x.startswith('## Changelog')) - 1
        spans = [(1, 1), (a, b)]
    if key == 'SPEC':
        L[0] = '<!-- carrier copy of SPEC_LIST_PIP.md at commit 523dda23 -->'
    spans = spans or [(1, len(L) - (1 if L and L[-1] == '' else 0))]
    out = [f'### [{key}] `{path}` @ {commit[:8]} — {note}']
    for a, b in spans:
        out.append(f'lines {a}–{b}:')
        out.append('```')
        out += [f'{i:5d}| {L[i - 1]}' for i in range(a, min(b, len(L)) + 1)]
        out.append('```')
    return '\n'.join(out), hashlib.sha256(raw).hexdigest()


def build(commit):
    blocks, man = [], ['key\tpath\tcommit\tsha256']
    for key, path, spans, note in SOURCES:
        txt, h = excerpt(commit, key, path, spans, note)
        blocks.append(txt); man.append(f'{key}\t{path}\t{commit[:8]}\t{h}')
    ctx = ('# D5P1 — blind audit of the list-restricted output claims (LIST-K, LIST-CODE, LIST-R)\n\n'
           'Material for a blind referee. Every excerpt is verbatim with its file and original line numbers; status labels '
           'and review markers have been removed.\n\n' + '\n\n'.join(blocks))
    task = ('## Task\nBreak the proof; findings only. Claims to decide, in this order (clause labels as in the statement '
            'file, §2–§4): ' + ', '.join(CLAIMS) + '. For LIST-CODE, open the code excerpts and look for a code path the '
            'proof misses. End with exactly one line per claim: `AUDIT D5P1 <claim> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.')
    full = ctx + '\n\n' + task + '\n'
    bad = [w for w in FORBID if w in ctx]
    if bad:
        for ln in ctx.split('\n'):
            if any(w in ln for w in bad): print('  SURVIVES:', ln[:160])
    if bad:
        sys.exit(f'build FAILED: forbidden words survive the scrub: {bad}')
    (HERE / 'SYSTEM.md').write_text(SYSTEM + '\n', encoding='utf-8')
    (HERE / 'REQ_d5p.md').write_text(full, encoding='utf-8')
    reqs = []
    for s in range(1, SAMPLES + 1):
        reqs.append({'custom_id': f'd5p1-s{s}', 'file': f'{T}/reviews/api_card/REQ_d5p.md', 'claims': CLAIMS, 'params': {
            'model': MODEL, 'max_tokens': MAX_TOKENS, 'output_config': {'effort': 'high'}, 'system': SYSTEM,
            'messages': [{'role': 'user', 'content': [
                {'type': 'text', 'text': ctx, 'cache_control': {'type': 'ephemeral'}},
                {'type': 'text', 'text': task}]}]}})
    (HERE / 'requests.json').write_text(json.dumps(reqs, ensure_ascii=False, indent=0), encoding='utf-8')
    (HERE / 'REQUESTS.tsv').write_text('custom_id\tclaims\n' + ''.join(f"{q['custom_id']}\t{';'.join(CLAIMS)}\n" for q in reqs), encoding='utf-8')
    (HERE / 'MANIFEST.tsv').write_text('\n'.join(man) + '\n', encoding='utf-8')
    tin = int(len(SYSTEM + full) / 3.5); tout = 16000
    usage = (f'Offline estimate (characters / 3.5): input ≈ {tin} tokens per request, {SAMPLES} requests; output ≈ {tout} '
             f'each (max {MAX_TOKENS}).\nBatch rate $4 / MTok in, $20 / MTok out: input ${SAMPLES*tin*4/1e6:.2f}, output '
             f'${SAMPLES*tout*20/1e6:.2f} expected, ${SAMPLES*MAX_TOKENS*20/1e6:.2f} worst case. HQ `count` gives the exact input.\n')
    (HERE / 'USAGE.txt').write_text(usage, encoding='utf-8')
    (HERE / 'SCRUB_LOG.tsv').write_text('key\tline\toriginal (omitted)\n' + ''.join(f'{k}\t{i}\t{x}\n' for k, i, x in nfallback), encoding='utf-8')
    print(f'{len(nfallback)} lines replaced by the fallback (SCRUB_LOG.tsv)')
    print(f'built D5P1 at {commit[:8]}: {len(reqs)} requests, {len(CLAIMS)} claims; ' + usage.split(chr(10))[0])


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] != 'build':
        sys.exit(__doc__)
    c = sys.argv[sys.argv.index('--commit') + 1] if '--commit' in sys.argv else \
        subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    build(c)
