# Outline: "What we prove", v2, the tight version (Writing, Assignment 3, 2026-11-16)

Owner (11-16): tight, core first, niche results motivated or cut, as concise and clear as possible.
Main text ≤ 12 pp, with one summary table up front. Notation: D2 v1 / `shared/smcbvs.sty`, unchanged.
Sources:
- statements: D2 v1 (`results/`, final after the Sol read);
- statuses: registry on main a7fc5093, identical to the v1 ledger (f8a6c2da);
- Theory notes: `from_theory/ANSWERS`, AG, IDEALW, ROW36, AUDIT_NOTE item 1;
- assumptions verdicts: A2 v2.

## Main text (target pages in brackets)

**§1 The results in one page [1.5].** Two lines on the method. Then the five results in plain words, then **Table 1**:
result × plain statement × key assumptions (labels) × status (plain label) × where. One line on what "asymptotic" means,
and that explicit proof constants are conservative.

**§2 Setting, the method as coded, and the assumptions [2.5].**
- Model; standardisation; the prior as coded; posterior and summaries (HPM, MPM, PIPs); Lemma 2.1 (the posterior miss
  controls the summaries). Lemma 2.1 stays: results 1 and 4 use it.
- A run: start law, calibration, islands, returned list, printed fields. Eight lines; D1 has the detail.
- **Assumptions, each defined once**, as compact displays with the v1 labels (GL, DIM, SP, BC, BM, EF, NC, GR, FSβ, FSθ,
  EFΣ, V, NL; the local 5.6). Each one is followed by a pointer: "reasonableness: Section A, §3.x".
- Conventions C1–C3 in one paragraph each; full lists in the appendix.
- (AG) does not appear (fixed-design branch only, AG note).

**Fixed format for each core result:** In words (one paragraph) → **Why it matters** (one sentence) → the theorem in
final form → **Assumptions:** a numbered list of labels, each pointing to §2 and to Section A → the status note in the
margin (`\status`, outside the theorem). Remarks are limited to at most two per result.

**§3 Result 1: the posterior finds the true model (rows 1.1, 1.2) [2].** One theorem in two parts:
- (a) random Gaussian design: 1 − π(S₀|y) = O_P(√(log n/n)), HPM = MPM = S₀ (v1 Thm 3.9). This is the case of our
  designs, so it comes first.
- (b) fixed design: the expectation bound uniform over designs, plus the in-probability form (v1 Thm 3.1).
- Status notes, one per part:
  - (a): "proved and independently checked; reader-form bridge awaits its final check";
  - (b), in-probability form: "proved and independently verified (two independent verification passes)";
  - (b), expectation display: conditional on Prop-LB and [L1a′].
- Remark: the primitive form (A2 §2).
- Remark: at moderate n (ANSWERS item 3, worded as a heuristic: (s₀+1)√(log p/(πn)), measured 0.5–1.2×). It explains
  why our simulations show mass on supersets.

**§4 Result 2: the posterior finds the true distribution (row 2.1) [1.5].** v1 Thm 4.2 (Thm 9, (i)–(iii)) with its own
setting paragraph (i.i.d. rows, Assumption 4.1). Remark: no beta-min is needed; what NC buys (one log factor; Prop 4.3(ii)
goes to the supplement).

**§5 Result 3: the method, as coded, reports the true model (row 3.1) [2.5].**
- Setup: how the signal looks to a block-by-block method; visibility (V); the polynomial leakage set (5.6), with the
  ANSWERS item-2 gloss on 32s₀.
- Then v1 Thm 5.7 and the delivery clause, with the conventions C1/C2⁺.
- The IDEAL-W⁺ line per the IDEALW note: "holds automatically for every input the software accepts (n, p ≤ 2³¹ − 1); to
  be stated in the next revision". The statement of row 3.1 stays as recorded.
- Status: "proved and checked; revision pending (RM2 follow-up, H2); reader-form bridges await their final check".
- The three-predictor example (v1 Ex. 5.x) is kept only if it fits; otherwise it goes to the supplement.

**§6 Result 4: the run's estimates are consistent (rows 3.5 + 3.6) [1.5].** Built so that row 3.6 can become a remark
without rewriting the rest (ROW36 note).
- **6.1** Unbiased evidence estimate, on every design (row 3.5, v1 Rem. 5.22), as a proposition. Per island: proved and
  checked. Pooled: proved, not yet independently checked (H3).
- **6.2** The printed PIPs, MPM and Ẑ are consistent on the calibration-success event, **for designs without leakage**
  (v1 Thm 5.19). The scope sentence comes first: "Of our designs, only the independent ones (S1, IND) qualify. On AR and
  block designs, Result 3 and 6.1 hold, and no theorem yet covers the printed fields." Plus "What is not claimed" (no
  lower bound on P(calibration succeeds)).
- **Planned change** (post-freeze, not decided): #5′ would carry consistency of the summaries computed from the returned
  list on every Result-3 design. Not in the text; in the freeze list only.

**§7 Result 5: the rate cannot be improved (row 1.3), as a remark [0.75].** v1 Thm 3.13(a)–(b) stated as a Remark, with
its status. One sentence: (a) holds at every finite n, and with it s₀ must be fixed (A2 §3.1).

**§8 What changes at the freeze (Fri 11-20) [0.5].**
1. Reader-form bridges re-pinned to the W3-READER commit of CP3: bridge notes on Results 1(a), 3, 4.
2. Row 3.1/3.2 revision (RM2 follow-up, H2).
3. T14 recorded (IDEAL-W⁺ costs nothing on real inputs): the Result 3 statement simplifies.
4. Pooled-Ẑ registry row (H3); Prop-LB and [L1a′] checks (H4).
5. Possibly #5′, with row 3.6 → remark (HQ decision pending).

Each item names the place in the text that changes.

Total: about 12.75 pp. The cuts to reach 12: §2 run description, §5 example to the supplement.

## Supplement: every other result, each with one "why it matters" line (draft lines)

| v1 | Result | Why it matters (draft) |
|---|---|---|
| Thm 3.4 | posterior concentration under an identifiability margin (row 1.1, Thm 1′) | Replaces the eigenvalue floor off the true model with a signal margin, so it covers designs whose null predictors are nearly collinear. |
| Thm 3.18 + Ex. 3.19 | omitted variables (row 1.4) | Says what the posterior selects when true predictors are missing from the data: the best linear predictor built from the others. |
| Prop 4.3 | level-M form; the case without NC | Removing the collinearity condition costs only one log factor in the radius. |
| Thm 4.6 | parametric rate when the true predictors are detectable | With a beta-min, the distribution is learned at the parametric rate. |
| Cor 4.7 | the output of the sampler | The distribution guarantee carries over to the list a completed run returns, whenever that list holds a non-negligible share of the posterior. |
| Rem 4.9 | fixed designs, in-sample distance (row 2.2) | The distribution result for a fixed design, in the in-sample distance. |
| Thm 5.2 | the start law concentrates (row 3.3) | The sampler's starting distribution is already right when there is no leakage; this is the first stage of Result 4. |
| Thm 5.12 | reported model, fixed design (row 3.2) | Result 3 without a random-design model, under sample conditions a user can check. |
| Thm 5.16, 5.17 | certified screening (row 3.7) | A certified small model rarely misses a true predictor, under much weaker conditions than Result 3 (no visibility, no leakage set). |
| Rem 5.21 | alternative route for the estimates | A second route to Result 4 that avoids the evidence estimate; its premise is open (one key lemma). |
| row 4.1 | pooled PIP error ≤ worst island | Pooling four islands never makes the PIP error worse than the worst island. |
| §6 | parallel engine, many islands | What carries over to the parallel method (empirical or open). |

## Cut list (for HQ/owner; not in the document): candidates with no convincing "why" line
- v1 Remark (o), determinant growth (row 1.1 remark): a technical consequence; no user-facing reading.
- v1 Thm 5.17 (screening with signals that vary with n): Thm 5.16 already carries the message. Keep only if the
  owner wants the margin form.
- v1 "Output-identical parallel engine" (row 4.2): no theorem, only an engineering fact. It belongs in D1 (methodology),
  not D2.
- v1 "Further consequences" remarks (3.x, 4.x, 5.x): fold the one line each that matters into the result; cut the rest.
- v1 Remark on growing true models (after Thm 3.13): covered by A2 §3.1 (SP).
- Song–Liang comparison remarks: replaced by A2 (assumptions) and by one "conclusions compared" paragraph in §1. The
  per-theorem conclusion comparisons follow WRITING_DELTA v1.4 (i)–(iii), never "stronger" overall.

## Consequences outside D2
- A2 (`assumptions_v2.pdf`) cites v1 numbers (Thms 3.1, 3.4, 3.9, 4.2, 5.7, 5.12, 5.19; Assumptions 3.3, 4.1, 4.5, 5.6;
  Rem 5.21, 5.22). Re-point them to v2 once v2 is final (numbers only, no content change; Opus diff check).

## Questions for the advisor
1. Result 1 as one theorem with parts (a) random, (b) fixed, or two theorems?
2. Should the assumptions be defined in §2 (compact) or only in the assumptions section (Section A), with D2 citing them?
   Proposed: defined once in D2 §2, judged in Section A.
3. Is the Thm 3.4 / Thm 3.18 "why" line convincing enough for the supplement, or should they go to the cut list?
4. Does the moderate-n remark belong in the main text?
