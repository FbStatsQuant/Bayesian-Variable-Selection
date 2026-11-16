# SMC - Writing Department: first assignment (HQ, 2026-11-16; owner's request)

Start this when HQ sends the resume message (after the Claude Personal weekly reset). Read `Docs/Writing/BRIEF.md` and
`POLICIES.md` first. The owner will read both documents himself to judge how the method and the theorems look. Write
for a statistician peer: clear, complete, honest.

## Clarity first (owner, binding: "as clearly as possible")
Clarity is the main measure of these documents. Accuracy is the floor; clarity is the goal.
- **Plain language.** Short sentences, one idea per paragraph, no jargon where a plain word works, and no internal
  ids (ticket names, claim ids, file tags) in the text.
- **Build up in order.** Each section opens with a 2–3 sentence summary in words. Every concept is introduced before
  it is used, and every symbol is defined at first use and listed in the notation table.
- **Say it in words, then in symbols.** Every displayed formula gets a sentence saying what it means. Every theorem
  gets a plain-words version before the formal one, and the assumptions are numbered, each with one line on what it
  rules out.
- **Show, don't only state.** Use a small worked example or a picture where it helps: what the prior does to a
  3-variable model, how one SMC step moves particles. Use tables for parameters and assumptions.
- **Clarity check before delivery.** A fresh Opus reader, with no prior context, reads each document as a
  statistician new to the project. It lists every sentence it had to read twice, every symbol it met before its
  definition, and every step it could not follow. Fix them all, then deliver.

## Paper standard (owner, binding: "as if it was the official paper")
Write both documents as sections of the final journal paper, not as internal notes.
- **One notation system, fixed once.** D1 §1 introduces the paper's notation formally ("Notation." paragraph:
  vectors, matrices, models S, |S|, X_S, norms, asymptotic symbols O, o, O_P, ≍, ≲). D2 uses exactly the same
  notation and refers back to it, introducing nothing ad hoc. Where the code or internal docs use other names,
  the paper's notation wins, and the mapping goes in D1's code-location column only.
- **Paper structure and conventions:**
  - numbered sections, definitions, assumptions, theorems, propositions and remarks;
  - assumptions named once and cited by name, e.g. (A1);
  - a citation for every outside result (Song & Liang 2015, etc.) as in a journal bibliography;
  - consistent tense and voice ("we show", "the method").
- **Statements in final form.** Each theorem reads as it would in the published paper: setting, assumptions,
  conclusion, with no hedging prose inside the statement. The status line ("proved and independently checked" etc.)
  sits outside the theorem environment as a marginal note for the owner, so it is easy to drop for submission.
- **Typesetting:** amsthm environments, bibtex, the notation table as an appendix. It should compile cleanly and
  look like a statistics journal manuscript.

## D1. Methodology: "The SMC-BVS method, as coded" (LaTeX → PDF)
Cover the method the theory is about: the shipped serial code at `Scripts/SMC_BVS/core/` (v3.x; R + C++). This is
NOT the p = 10⁶ engine. That engine's changes go in a separate short appendix, taken from
`Docs/Experiments/P1M/ENGINEERING_SPEC.md`, and are labelled as such.

1. **Setup and notation:** data (y, X), n, p, standardisation and centring, the intercept. Every symbol is defined
   before it is used, and a notation table goes at the end.
2. **The model and every prior, written out in full:**
   - the model-size prior BB(1, r): r and any cap K, and how each depends on n and p;
   - the slab N(0, n v (G_S + I)⁻¹): v and how it is set;
   - σ² ~ IG(0.01, 0.01);
   - any other hyperparameters.
   For each: the formula, whether it is fixed or a function of (n, p), and the code location (file:line).
3. **The posterior:** the closed-form marginal likelihood and model posterior π(S | y) the code computes.
4. **The algorithm, step by step:**
   - the start law π₀ and how it is built;
   - the tempering/bridge schedule and calibration (grid, rebuilds, escalation rules);
   - the move kernels (add, delete, swap, local search LS0 and its cap ℓ_n + |S̃₀|);
   - reweighting and resampling, and the ESS rule;
   - the islands (R′ = 4) and how they are pooled;
   - the outputs: HPM, PIPs, the evidence estimate Ẑ, and the printed diagnostics.
5. **The parameter table (the core of D1).** One row per tuning or prior parameter, with columns: symbol, meaning,
   value (fixed / formula in n, p), default, where it is set in the code (file:line), and whether a theorem uses it.
   Include the two code ceilings (`le ≤ 10⁶` in v3_run.R, `ℓ + |S̃₀| ≤ INT_MAX` in v3_core.cpp) as stated facts.
6. **One page of intuition:** why SMC and why this start law, with no formulas. Use
   `Theory_work/Wave3/W3-READER/METHOD_INTUITION.md` as a starting point.

Sources: the code; W3-READER `NOTATION.md` and `METHOD_INTUITION.md` (on branch theory/W3-READER, latest); chapter v1.0
(Wave1C/FINAL); the 11-13 status briefing. **Where a source and the code disagree, the code wins. List each such
disagreement at the end of the document for HQ.**

## D2. The consistency results: "What we prove" (LaTeX → PDF)
Every consistency result we have or are working on, in reader form, grouped by the CLAIMS_CARD pillars:
1. the posterior picks the right model (rows 1.1–1.4);
2. the posterior is right about the distribution (2.1 = W3-DIST Theorem 9; 2.2 as a remark);
3. the coded algorithm delivers it (3.1–3.7);
4. the parallel method (4.x, mostly open; say so).

For each: a plain-words sentence, the theorem with numbered primitive assumptions and a clean conclusion, and the
**status quoted verbatim** from the registry (`Theory_work/INFRA/registry/claims.tsv` on main) in plain words:
"proved and independently checked", "proved and checked, conditional on …", or "in progress". Nothing in progress is
called a theorem. Add the Song–Liang comparison where W3-READER has one, verbatim; those comparisons were checked
against the paper today.

Sources: `READER_VERSIONS.md` and `CLAIMS_CARD.md` on theory/W3-READER (latest head; rows 1.3, 1.4, 2.1, 3.3, 3.7 were
updated today), and claims.tsv on main. Do not restate mathematics beyond the reader versions. If a row is unclear, flag
it for HQ; don't rewrite the theorem.

## Order, timing, checks
- **D2 first:** a draft within about 6 working hours of the resume (it is mostly assembly). **D1** follows within about 24 h.
- **Checks before delivery:**
  - one Opus reader checks every D1 parameter row and formula against the code (file:line);
  - one Sol fidelity read per document, which HQ orders when you tell it a document is ready;
  - every status in D2 checked against claims.tsv.
- Helpers: at most 2 at a time, on Claude Personal, Opus or Sonnet, effort high max.
- Output goes in `Docs/Writing/methodology/` and `Docs/Writing/results/` (.tex + .pdf). Report each PDF path to HQ in ≤ 10
  lines, with open questions. HQ shows the owner.
