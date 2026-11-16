"""mkreport.py — writes REPORT.md for W3-DIST from the table below, filling STATEMENT.md line ranges from text anchors.
Run from the ticket folder: `python3 mkreport.py`. REPORT restates nothing (PROTOCOL_v4 §3): it points to STATEMENT lines.
Statuses and review files are edited HERE (one place), then REPORT.md is regenerated."""
import io, sys
S = open('STATEMENT.md', encoding='utf-8').read().split('\n')

def ln(anchor, start=0):
    for i in range(start, len(S)):
        if S[i].startswith(anchor):
            return i + 1
    raise SystemExit('anchor not found: ' + anchor)

def rng(a, b):
    i = ln(a); j = ln(b, i) - 1
    while j > i and S[j - 1].strip() == '':
        j -= 1
    return f"{i}-{j}"

R = {
 'setting': rng('## 0. Setting and objects', '## 1. Candidate theorems'),
 'DIST-1': rng('**Theorem DIST-1', '**Theorem DIST-2'),
 'DIST-2': rng('**Theorem DIST-2', '**Theorem DIST-3'),
 'DIST-3': rng('**Theorem DIST-3', '**Stretch statements'),
 'setupR': rng('**Setup.** We observe', '**Theorem A (the posterior'),
 'Thm-A': rng('**Theorem A (the posterior', '**Theorem B (parametric'),
 'Thm-B': rng('**Theorem B (parametric', '**Corollary C (the output'),
 'Cor-C': rng('**Corollary C (the output', '**Notation table.**'),
 'code': rng('**Code facts', '**Theorem DIST-C'),
 'DIST-C': rng('**Theorem DIST-C', '## 3. Key lemmas'),
 'H': rng('**Lemma H (', '**Lemma T ('),
 'T': rng('**Lemma T (', '**Lemma S ('),
 'S': rng('**Lemma S (', '**Lemma V.'),
 'V': rng('**Lemma V.', '**Lemma X (in-sample'),
 'X': rng('**Lemma X (in-sample', '**Lemma X′ (the same'),
 "X'": rng('**Lemma X′ (the same', '**Proposition NEC'),
 'NEC': rng('**Proposition NEC', '**Lemma P6'),
 'P6': rng('**Lemma P6', '**Bridges (candidates'),
 'B0': rng('- **B0 (scale', '- **B1 (('),
 'B1': rng('- **B1 ((', '- **B2-core'),
 'B2core': rng('- **B2-core', '- **B2 (('),
 'B2': rng('- **B2 ((', '- **B3 (for'),
 'B3': rng('- **B3 (for', '- Failure probabilities of B1'),
 'consumes': rng('## 4. Consumes table', '## Changelog'),
}
VER = S[0].split('(')[1].split(',')[0]

T01 = "SOP:TH09 (its T01 part, \"T01–T03: PROVED-LOCKED\": the coded posterior is the contrast-model posterior)"
# id: (content pointer, proof, status, review)
CLAIMS = [
 ('DIST-1', 'master theorem (1.1): joint Hellinger contraction, exponential form, sharp rate', 'lemmas/DIST12.md D.0–D.5',
  f'PROVED (by this seat); cross-family line check: see §2; conditional on {T01}'),
 ('DIST-2', 'master theorem (1.2): the same without the non-degeneracy interface, one logarithm slower', 'lemmas/DIST12.md D.6',
  f'PROVED (by this seat); cross-family line check: see §2; conditional on {T01}'),
 ('DIST-3', 'oracle bound with an additive selection error; parametric rate', 'work/B_transfer/DIST3.md',
  f'PROVED (by this seat); line-checked (reviews/L3_sol_B.md: VERIFIED); conditional on {T01}'),
 ('DIST-C', 'coded output: domination transfer; store BMA; HPM/MPM plug-ins', 'work/D_output/P6_DISTC.md',
  f'PROVED (by this seat); line-checked (reviews/L2_sol_D.md: VERIFIED / VERIFIED-WITH-AMENDMENTS, applied); deterministic parts conditional on {T01} and EX-A; delivery statements also conditional on W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR under their own premises'),
 ('Thm-A', 'reader Theorem A = DIST-1/DIST-2 + bridges B0, B1, B2', 'work/E_bridges/ASSEMBLY.md §1–§2',
  f'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED-WITH-AMENDMENTS, applied); conditional on {T01}'),
 ('Thm-B', 'reader Theorem B = DIST-3 + bridges B0–B3 + selection consistency', 'work/E_bridges/ASSEMBLY.md §3',
  f'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED-WITH-AMENDMENTS, applied); conditional on W3-POST:Thm-1 and on {T01}'),
 ('Cor-C', 'reader Corollary C = Theorem A + DIST-C (C-0), (C-i), (C-ii)(α)', 'work/D_output/COR_C.md',
  f'PROVED (by this seat); line-checked (reviews/L2_sol_D.md: VERIFIED-WITH-AMENDMENTS, applied); conditional on {T01} and EX-A'),
 ('H', 'Hellinger reduction (deterministic)', 'work/B_transfer/H.md', 'PROVED (by this seat); line-checked (reviews/L3_sol_B.md: VERIFIED)'),
 ('T', 'distribution-free sample-to-population transfer on sparse directions', 'work/B_transfer/T.md', 'PROVED (by this seat); line-checked (reviews/L3_sol_B.md: VERIFIED)'),
 ('S', 'size tail with an exponential tail (reference-adaptive)', 'work/C_size/S.md', 'PROVED (by this seat); line-checked (reviews/L5_astra_SV.md: VERIFIED; amendments applied)'),
 ('V', 'variational split and moment bound for supersets', 'work/C_size/V.md', 'PROVED (by this seat); line-checked (reviews/L5_astra_SV.md: VERIFIED)'),
 ('X', 'in-sample exponential core (key lemma)', 'lemmas/X.md §0–§7', 'PROVED (by this seat); line-checked (reviews/L1_astra_X.md: VERIFIED); break review reviews/BR1_astra_break.md: NOT BROKEN'),
 ("X'", 'the same without the non-degeneracy interface', 'lemmas/X.md §9', 'PROVED (by this seat); line-checked (reviews/L1_astra_X.md: VERIFIED); break review: NOT BROKEN'),
 ('NEC', 'sharpness: the non-degeneracy hypothesis cannot be dropped from Lemma X (fixed design)', 'lemmas/NEC.md', 'PROVED (by this seat); cross-family line check: see §2'),
 ('P6', 'domination transfer; Markov bound over models; convexity for predictive densities', 'work/D_output/P6_DISTC.md', 'PROVED (by this seat); line-checked (reviews/L2_sol_D.md: VERIFIED)'),
 ('B0', 'scale reduction, pathwise', 'work/E_bridges/B0.md', 'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED)'),
 ('B1', 'sample variances; energy and coefficient-cost events', 'work/E_bridges/B1.md', 'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED)'),
 ('B2core', 'sparse lower bound for sample second moments, with an intercept', 'work/E_bridges/B2core.md', 'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED)'),
 ('B2', 'non-degeneracy interface from the population assumptions', 'work/E_bridges/B2.md', 'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED-WITH-AMENDMENTS, statement wording applied)'),
 ('B3', 'the events needed by Theorem B', 'work/E_bridges/B3.md', 'PROVED (by this seat); line-checked (reviews/L4_sol_E.md: VERIFIED-WITH-AMENDMENTS, applied); conditional on W3-POST:Thm-1 for its last sentence'),
]
EXTRA = open('REPORT_extra.md', encoding='utf-8').read()   # §2–§6 prose and the registry blocks, with @@key@@ fields

out = io.StringIO()
w = out.write
w(f"# W3-DIST — REPORT (distribution-level consistency: the joint (x, y) Hellinger contraction of the coded posterior, and what the sampler returns)\n\n")
w("Lead: Claude Fable 5.2 (Claude Third, effort high). Reports to the SMC - Theory Department. Generated by `mkreport.py`\n"
  f"from `STATEMENT.md` {VER}; this file is frozen with each round's manifest, so the outcome of a council round is recorded\n"
  "in `CHECKPOINT_3.md` and `reviews/`, not here. **REPORT restates nothing**: every row points to STATEMENT lines.\n\n")
w(f"## 1. What is proved (`STATEMENT.md` {VER}; setting: lines {R['setting']}; reader setup: lines {R['setupR']})\n\n")
w("| claim | what it is (pointer, not a restatement) | STATEMENT lines | proof | status (per claim) |\n|---|---|---|---|---|\n")
for cid, what, proof, status in CLAIMS:
    w(f"| {cid} | {what} | {R[cid]} | `{proof}` | {status} |\n")
w("\n")
for k, v in R.items():
    EXTRA = EXTRA.replace('@@' + k + '@@', v)
EXTRA = EXTRA.replace('@@VER@@', VER)
assert '@@' not in EXTRA, EXTRA[EXTRA.index('@@'):EXTRA.index('@@') + 40]
w(EXTRA)
open('REPORT.md', 'w', encoding='utf-8').write(out.getvalue())
print('REPORT.md written;', VER, {k: R[k] for k in ('DIST-1', 'Thm-A', 'X', 'NEC')})
