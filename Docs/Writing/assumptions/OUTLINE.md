# Outline: advisor-report section "Are the assumptions reasonable?" (Writing, 2026-11-16, Assignment 2)

Source: theory/W3-AUDIT @ 56dafbdd (`AUDIT.md`, `TRACK_B.md` = core, `TRACK_D.md`, `CHECKPOINT_3.md`; `BRIEF.md` = standard).
Notation and labels: those of "What we prove" (D2), via `shared/smcbvs.sty`. Theorem numbers refer to D2.
Length: 3–5 pages plus one table. Owner: "precise and concrete arguments / evidence, not pages upon pages".

## 0. Opening, the answer (≤ ½ page)
Three findings in plain words:
1. **The posterior theorems** (the posterior finds the true model; the posterior finds the true distribution) hold on
   all our simulation designs (the 2,400-fit study, the strong-factor study, the 10⁶ plan), strong factors included.
   Their assumptions are the same as or comparable to Song and Liang (2015). Three are stronger, each mildly: the range of
   $p$, a collinearity floor of order $1/n$, and the law of the rows.
2. **The reported-model theorem** adds two method-specific design conditions, visibility and a bounded leakage set,
   with Song–Liang counterparts (their Condition 5; their remark (a), p. 958). They hold for independent, block and AR
   designs (AR up to correlation 0.8). They can fail for pervasive factors with mixed-sign effects and for
   riboflavin-like data.
3. **The printed-estimates theorem** (row 3.6) is narrower: its no-leakage condition holds on independent designs.
   Elsewhere the reported-model theorem and the unbiasedness of the evidence estimate still hold.

## 1. Our designs (5 lines)
Study S1–S6; strong-factor study (one or two factors; the 2,400-study's S5); 10⁶ plan (IND, AR 0.6, blocks of 20,
factor). Same notation as D2 §2.

## 2. Summary table (one page)
Rows = the assumptions of the core theorems, grouped: (a) model and dimension; (b) signal; (c) design, for the posterior
theorems; (d) design, for the coded-method theorems.
Columns: assumption (D2 label, theorems) · plain meaning (≤ 8 words) · against Song–Liang (same / weaker / comparable /
stronger, with page and equation) · our designs (Study S1 | S2 | S3, S4, S6 | S5 · strong-factor study · 10⁶ IND | AR | BLK
| FAC), as in / out / unclear.

| row | D2 label | dossier |
|---|---|---|
| Gaussian linear model | (GL); Assumption 4.1(a) | B1 |
| dimension $p\le n^A$ | (DIM) | B2 |
| fixed true model size | (SP) | B3 |
| signal size | (BC), (BM), (FS$_\beta$), (FS$_\theta$), 4.1(e) | B4 |
| eigenvalue floor on small sets | (EF), (EF$_\Sigma$), 3.3(a) | B5 |
| no near-exact collinearity | (NC), 4.1(d) | B6 |
| law of the rows | (GR), 4.1(c) | B7 |
| visibility | (V) | B8 |
| bounded leakage set | 5.6(a) | B9 |
| floor on $Q\cup\{l\}$, local regressions | 5.6(b),(c) | B10 |
| no leakage | (NL) | B11 |
| (witness designs of Thm 3.13(b): not an assumption to defend; one footnote) | 3.12 | B12 |

## 3. One paragraph per assumption (≤ ½ page each; most need 5–8 lines)
Fixed layout, as in D2:
- **Verdict** (one line), e.g. "Same as Song–Liang (their model (1)–(2), p. 950)";
- **Evidence** (the single strongest item: an exact citation with equation and page, a proved result, or one
  example or counterexample);
- **Rules out** (one line);
- **Our designs** (one line, matching the table).
Order: B1–B11, grouped as in the table. Each verdict is quoted from TRACK_B, with the citations as there. Lines that
TRACK_B marks "[audit calc]" (unchecked, no verdict) are not used.

## 4. Assumptions on mathematical objects (prior, distributions, kernels, code properties): a short list
- **Proved and checked:** the prior facts, the posterior-summary lemma, the Hellinger facts, and the events of the
  reported-model proof.
- **Pending (named, being checked):** 13 code-level items for the coded-method theorems (in words: the run-guard audit,
  the block-size cap, that the start-mode search is executed as described, the start tables, the calibration's
  measurability, the exact start sampler, the Markov kernels, one overlap line, the tie-aware start-mode recursion, two
  audits by code reading), plus five further claims (two relabellings, three short lemmas).
- **No open item for the posterior theorems** (rows 1.x, 2.1).
- **Idealisations stated as conventions:** exact arithmetic and ideal random numbers. Disclosed, not provable.

## 5. Honest limits (one paragraph)
As fact, not apology:
- Who may be outside core 3: typical real-data designs with strong pervasive factors or masked effects (one sentence
  from the numerical check of the conditions' population quantities: mixed-sign factor, riboflavin-like).
- What still holds for them: cores 1 and 2 (the posterior is right about the model and the distribution).
- Row 3.6 on AR and block designs: the reported-model theorem and the unbiasedness of the evidence estimate hold there.
- No asymptotics-as-limitation framing, and no proof constants presented as limits.

## Open questions for the advisor (style)
1. Table: one wide table (landscape), or two tables (posterior theorems; coded-method theorems)?
2. Per-assumption paragraphs: run-in bold labels (Verdict / Evidence / Rules out / Designs), or a 3-column mini-table each?
3. Should the D2 labels such as (EF$_\Sigma$) appear at all in an advisor-report section, or only plain names, with the
   labels in the table?
