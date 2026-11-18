# Outline: the unified manuscript (Writing, Assignment 4, 2026-11-17)

Owner: ONE well-presented manuscript (method + theorems + assumptions), concrete. The main text (§1–6) is ≤ 25 pp.
Notation: `shared/smcbvs.sty`, plus D1's four macros (\code, \Nc, \grid, \grouprow).
Sources:
- D1 v1, `methodology/` (code-checked, Codex-read);
- D2 v2.1, `results_v2/` (statuses at the freeze);
- A2 v2.1, `assumptions/` (TRACK_B v1.4 format);
- `from_theory/`;
- the freeze registry and card v1.13.

Rule: each fact appears once. The three sources overlap in five places (marked ✂ below); each is resolved by keeping
it in one place and pointing to it.

## Front matter (≈ 2 pp)
- **Title:** "Sequential Monte Carlo Bayesian variable selection, as coded: consistency of the posterior and of the
  software's output".
- **Abstract (≤ 200 words):** problem; the method (SMC over models under a fixed BB(1,p) + g-prior, no tuning; a start
  law from block tables; local searches); the five results in one sentence each, with scope (Result 4 without leakage);
  the assumptions discussion (the v1.4 headline in one sentence).
- **§1 Introduction (≤ 1.5 pp).**
  - ¶1 The problem: selection with p ≫ n; what users read (PIPs, MPM, evidence, a reported model), and that theory
    usually covers an idealised posterior, not the software.
  - ¶2 What is new: a theory for the method exactly as coded. The prior, the start law, the calibration and the
    searches are all as the code does them, with a seed-free guarantee for the reported model.
  - ¶3 What we prove: the five results in plain words, with pointers to §4.
  - ¶4 How reasonable the assumptions are: the v1.4 headline, paraphrased in one ¶ (verbatim in §5), and Song and
    Liang (2015) as the reference point.
  - ¶5 Organisation (3 lines).

## §2 Setup and notation (≈ 1.5 pp)
D1 §1 merged with D2 §2.1: notation (including the asymptotic notation); data, raw → retained predictors; model (1);
fixed versus random Gaussian design, W; standardisation (X, y, θ*, μ, θ*_min, G_S, R̂_S, P_S); "fixed" and the
asymptotic convention. ✂ D2 §2.1 and D1 §1 both define these; they are written once here.

## §3 The method, as coded (≤ 6.5 pp)
Condensed from D1 (19 pp → 6.5): keep every definition the theorems use, and every default; drop the D1 worked
example, Figure 2 and the long tier discussion.
- **3.1 The model and every prior:** the working model; Ω, K; BB(1,p) with w(k); the g-prior (g = n, unit ridge);
  IG(0.01, 0.01).
- **3.2 The closed-form posterior:** m(S) display (6), F, π = e^F/Z, the evidence; posterior summaries; Lemma
  (posterior miss controls the summaries). ✂ D2 §2.2 duplicate removed.
- **3.3 Why SMC, and why this start law:** ½ page, from D1 §4.
- **3.4 The algorithm, step by step:** Figure 1 (D1's pipeline, stages 1–7). One paragraph per stage:
  1. exact case, pre-run check, effort tiers;
  2. blocks (≤ B = min(⌊√n⌋, ⌊√p⌋, 16)) and block tables;
  3. start law π₀ (display) and start mode;
  4. the sampler, one island (tempering path, reweight/resample/move; the three moves);
  5. calibration (Algorithm 1 kept, compact);
  6. final run (4 islands) and the two local searches (caps ℓ_n, ℓ_n + |S̃₀|; final scan; certification);
  7. outputs.
- **3.5 What a run reports:** status (exact/completed/stopped), Ŝ and certification, pooled PIP̂, Ẑ, MPM̂, the
  returned list 𝒯; run guard.
- **3.6 Compact parameter table** (≈ ¾ p): symbol | meaning | value or formula in (n, p). The full table with code
  locations goes to Appendix B.
- **Conventions C1–C3** (one paragraph): what "the method" means for the theorems. The full lists go to Appendix B.

## §4 Main results (≈ 9 pp; D2 v2.1 §1, §3–6)
- **4.0 Summary table** (D2 Table 1, frozen statuses) and the reading format: in words → why it matters → statement
  → assumptions (labels pointing to §5) → status box.
- **Shared assumptions** (GL, DIM, SP, GR, EFΣ) defined once, at the start of §4, with the visibility/leakage gloss.
  ✂ A2 §2's "theorem key" is dropped; §4 numbering is the key.
- 4.1 Result 1: Theorem (random), Theorem (fixed).
- 4.2 Result 5 (rate cannot be improved; moderate-n heuristic), as in D2 v2.1 §3.1.
- 4.3 Result 2.
- 4.4 Result 3. ✂ the 32s₀ gloss and the visibility example are kept here; §5 refers back.
- 4.5 Result 4: Prop (unbiased) + Theorem (consistency without leakage), with the scope paragraph.
- Status boxes: D2 v2.1, which is already requoted at the freeze.

## §5 Are the assumptions reasonable? (≈ 5.5 pp; A2 v2.1)
- 5.1 The answer: the v1.4 headline verbatim, plus one ¶ on the coded-method theorems.
- 5.2 Our designs (three classes) and what "inside" means; how the conclusions compare (delta items (i)–(iii)).
- Table (assumption × meaning × Song–Liang by regime × design classes).
- 5.3 One by one (≤ ½ p each).
- 5.4 Who is outside Result 3, and what still holds for them (from A2 §1/§3.3–3.4, gathered in one place).
- ✂ A2 §4 (mathematical objects) moves to §6 and Appendix C, since it is status, not reasonableness.

## §6 Scope and what is not claimed (≤ ½ p)
As fact:
- asymptotic statements; the explicit constants are conservative;
- the posterior and the software are covered, but the parallel engine and many islands are not;
- Result 4's consistency only without leakage;
- the remaining open items (the Prop-LB check, the T11 premise);
- the idealisations C1–C3.

## Supplement (D2 v2.1 Appendix A + D1 Appendix A)
- S.1–S.3: the D2 supplement results, each with its "why" line.
- S.4: the engine for p = 10⁶ (an engineered variant, not covered by the theorems), from D1 App. A, ½ p.
- S.5: open questions.

## Appendices
- A: notation (merged D1 App. B and D2 App. B).
- B: the full parameter table with code locations (D1 §6), and the conventions in full, with 𝔇.
- C: explicit constants (C*).
- D: status ledger at the freeze (STATUS_LEDGER_FREEZE), with "what changed / what remains", under \showstatus.
- Internal, under \showstatus: D1's App. C (where the sources and the code disagree).

## Budget check
2 + 1.5 + 6.5 + 9 + 5.5 + 0.5 = 25.0. It is tight; the levers are the D1 condensation and the A2 one-by-one heads.

## Questions for the advisor
1. Order: is it better to put results (§4) before the assumptions (§5), as planned, or to place each assumption's
   reasonableness note next to its theorem?
2. Should the shared assumptions be defined in §4, or in §2 (setup)?
3. Is the D1 calibration Algorithm worth its ½ page in a 25-page main text, or should it go to the supplement?
4. Title.
