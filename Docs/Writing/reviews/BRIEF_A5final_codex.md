# Brief: final Codex fidelity read of Assignment 5 (Writing, 2026-11-17), diff-scoped

You are an independent reviewer. Report findings only, and edit no file except your report. Paths are relative to
`/home/fb31/BVS-wt/WRITING`. Scratch goes in `.rc_tmp/` only; do not set TMPDIR. **Review only the hunks of the diff
below.** The rest of the manuscript passed earlier reads.

## Diff
`.rc_tmp/a5_final_diff.patch`: the earlier Codex-read snapshot (`.rc_tmp/a5_checked_draft/`) against the current text
(`Docs/Writing/manuscript/`; frozen copy in `.rc_tmp/a5_final_snapshot/`). It contains:
- fixes from earlier reviews;
- the renumbering of the results (1–6), certified screening in the main text, row 3.6 and Cor 9C as remarks;
- four additions from Theory results that are not yet recorded in the registry:
  - Theorem 2, sub-Gaussian form: assumption `(SGR)`, theorem `thm:post-random`, the mixtures sentence;
  - Remark `rem:thm2x` (smaller sets, in expectation);
  - Corollary `cor:list` (list-renormalised estimates), with its definitions and the two sentences after it;
  - Remark `rem:vis` (when visibility holds), now in §5.3.3, and the new scope line of Result 3;
- precedent lines and wording in §5;
- trims.

## Sources
- **New results:** `.rc_tmp/a5b_src/`:
  - `W3-D3_STATEMENT.md` (Thm2SG, ExSG);
  - `W3-D2_STATEMENT.md` and `W3-D2_REPORT.md` §3 (Thm2X card sentence and caveats);
  - `W3-D5P_STATEMENT.md` §1–§5 (LIST-K, LIST-R, remarks);
  - `H5_CARD_PUSH.md` (card text and statuses);
  - `VISIBILITY_SCOPE_2026-11-17.md`, including its HOLD and "Notes for Writing".
- **Statuses:**
  - `.rc_tmp/claims_main_now.tsv`, the registry on main d063cc3e, which does not yet contain the new results;
  - `.rc_tmp/card_v113.md`;
  - `Docs/Writing/results_v2/STATUS_LEDGER_FREEZE.md`.
- **Rules and precedents:**
  - `.rc_tmp/ASSUMPTION_COMPLIANCE.md`;
  - `Docs/Writing/from_theory/PRECEDENTS_2026-11-17.md`;
  - `Docs/Writing/from_theory/TRACK_B_v1.4.md`;
  - the two Song & Liang PDFs in `.rc_tmp/a2_sources/` (journal page = PDF page + 946).
- **Checked base text for moved statements:** `.rc_tmp/a4_checked_draft/sections/`.

## HQ rules to respect
1. Result 3 is "the theorem for block and moderate AR correlation", with no unqualified "AR". Visibility is "no true
   predictor masked by ≤ 15 others".
2. Certified screening (Result 4) is "the guarantee that needs neither condition", with its weaker conclusion:
   - "certified" = the local-optimality flag;
   - nothing is claimed conditionally on certification;
   - no run is claimed to certify;
   - it is not presented as "the result for strong-factor data".
3. Theorem 2's only precedent anchor is Narisetty & He (2014) Lemma 6.1; Song–Liang Condition 1 may appear only as a
   factual remark. The "2b" sentence covers Gaussian rows and correlated bounded mixtures.
4. Thm2X is one remark under Theorem 2, with its conditional status.
5. Corollary 6L is phrased about "the list-renormalised quantities", not what the software prints, until IMPL-LIST is
   committed. Writing deliberately does not claim that it discharges Cor 9C's premise, since the source says "proposed
   at CP3, not claimed here".

## What to check (diff hunks only)
- **A.** Each new or moved statement against its source: hypotheses, conclusions, quantifiers, scope.
- **B.** Each status note: does it match the card and registry, including "not yet recorded" and the pending items?
- **C.** The Song–Liang and precedent sentences against PRECEDENTS, TRACK_B and the PDFs.
- **D.** Any sentence in the diff that contradicts another sentence in the diff.

## Report
Write `Docs/Writing/reviews/A5final_codex_fidelity.md`. It is a table with these columns:
- id;
- manuscript file:line (current text);
- what it says;
- what the source says (file:line or page);
- severity: C = changes a claim, S = scope, F = could mislead, E = editorial.

End with `FIDELITY: FAITHFUL` or `FIDELITY: NOT-FAITHFUL` and the counts. Effort: high.
