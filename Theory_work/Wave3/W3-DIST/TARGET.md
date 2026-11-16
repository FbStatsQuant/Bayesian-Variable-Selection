# W3-DIST — TARGET (PROTOCOL_v4 §3.2 evidence file for the `lit:`, `necessity:`, `better:` gates; 2026-11-15)

Everything is at candidate level: "matches / beats / short" compares the **candidate statement** (STATEMENT v1.1) with
Song & Liang (2015), assuming the candidate is proved. Nothing here is proved.

## 1. Assumption map (summary; full table `ASSUMPTION_MAP.md` §1–2)
| hypothesis | enters | necessity reading |
|---|---|---|
| Gaussian noise independent of the design | conjugacy, χ² tails | as in [SL] model (1); not a target to weaken |
| i.i.d. rows | Lemma T only | needed for a population distance |
| **no** condition on ν_x in the transfer | Lemma T | strong form; N2, N6 show no degradation with infinite 4th moments |
| strict sparsity, s₀^r fixed | constant M₀ ∝ (1 + s₀^r)(A + 1); Lemma S | approximate sparsity = stretch S-APX |
| p_raw ≤ n^A | constants | proof device; S-EXP stretch |
| 𝒟_n = {p_ret ≥ 2} | remainder | proof device |
| (E; M) energy | s_y bracket, X3, S | some bound on signal energy is needed with the s_y-scaled prior |
| (C; M′) / (L₀; B) coefficient cost | X3, S through L_{S₀} | very weak; replaces the floor on S₀ |
| **(ND)** average determinant growth | X4 only | **not needed for consistency** (DIST-2); needed by this proof for the sharp rate and the full exponent; absent from [SL]; `improvable` (N4; S-FIT open) |
| (TR₀) second moments on supp β* | DIST-3 only | needed by this route at scale 1/n |
| beta-min, identifiability ([SL] Condition 3) | **not assumed** | — |

## 2. Parity table (A1 checklist + PROGRAM goals + our best registered result)
Our best registered result for comparison: W3-POST2:D — fixed design, in-sample average Hellinger, in probability,
D(a) M_n/√n given δ_n → 0, D(b) log n/n under (E), (F₀), (OS) (HQ note: D(b) repaired after council; diff round in progress).
| item | Song–Liang | candidate | vs [SL] | vs PROGRAM goals | vs W3-POST2:D |
|---|---|---|---|---|---|
| **P1 metric** | Hellinger between joint (x, y) densities, x-marginal integrated (d² = 2d_H²) | the same distance, d_H (DIST-1/2/3); sample → population by Lemma H + Lemma T | **matches**; the transfer step needs no condition on the predictor law, where [SL] need bounded predictors or Condition 1/2 | design-agnostic ✓ | **beats** (out-of-sample, random design) |
| **P2 mode (15)** | P*[π(d > ε_n) > e^{−c₁nε_n²}] < e^{−c₁nε_n²} under Condition 1 | DIST-1 (1.1): the same display with remainder P*(interfaces fail); for all ε_n² ∈ [C²M₀ log n/n, C²n^{−κ₀}] | **matches in form**, under (ND). Tail condition: only the probability of (E), (C), (ND) — B1 (weighted sub-Gaussian true coordinates) for (E), (C). **Short** in two respects: needs (ND), which [SL] do not; sequences with ε_n² > n^{−κ₀} get exponent c n^{1−κ₀} only | ✓ | **beats** (exponential vs in probability) |
| **P2 mode (16)** | lim P*[π(d > ε_n) > e^{−c₁nε_n²}] = 0 under second moments (Condition 2) | DIST-1(b) when P*(interfaces fail) → 0; (E), (C) need only second moments of the true signal coordinates (B1) | **matches** given (ND) w.p. → 1; **beats** on the moment condition for the transfer | ✓ | **beats** |
| P2 without (ND) | — ([SL] need no design geometry) | DIST-2 (1.2): exponential form with exponent c nε_n²/ℓ_n | **short**: exponent reduced by ℓ_n. Reason: the coded size prior is ≈ geometric(½), [SL] hard-cap the size at r̄_n; closing it = stretch S-FIT (kill budget: 1 attempt + 1 break review) | ✓ no geometric condition | new |
| **P3 rate** | Thm 2 at polynomial p: any ε_n with r_n → ∞, r̄_n ≥ r_n, r̄_n log n = o(nε_n²) — i.e. ε_n² = ω_n log n/n with ω_n → ∞ tied to the prior's cap; Cor 1 as printed (fixed α ∈ (0, 1)): ε_n² = n^{−(1−α)} log^k n | DIST-1: ε_n² ≍ (1 + s₀^r)(A + 1) log n/n ≍ (1 + s₀) log p/n, no diverging factor, no tuning; DIST-3: √(u/n) oracle/parametric given selection; DIST-2: (1 + s₀^r) log n·ℓ_n/n | DIST-1 **beats** both (constant × log n/n; and beats Cor 1's printed rate for every fixed α). DIST-3 **beats** (parametric; [SL] have none). DIST-2 **beats Cor 1 as printed** but is **short** of Thm 2's best (ω_n log n/n, any ω_n → ∞) by the factor log n/ω_n | p ≫ n ✓ | **beats** D(b) in generality ((OS) → (ND) is stronger, but no (F₀)); equal rate |
| **P4 sparsity** | Thm 2: strict (4). Thm 1: approximate (3) with bounded predictors | strict, s₀^r fixed | **matches** Thm 2; **short** of Thm 1 (approximate sparsity) → stretch S-APX (kill budget: 1 attempt after CP2) | ✓ | equal |
| **P5 prior** | a family of priors: Bernoulli(r_n/P_n) with r_n → ∞, hard cap r̄_n tied to ε_n, V_ξ with envelopes (9)–(14) | the prior **as coded**, no tuning: BB(1, p) capped at K = min(p, ⌊n/2⌋), data-dependent slab and IG rate | **matches the checklist** (coded prior, no tuning). [SL]'s own conditions (9), (10), (11) and "r_n ≻ 1" **fail** for it (cap ⌊n/2⌋; mean size O(1)); their sieve route is incompatible with a geometric size prior when log p → ∞ (H1 §2, unchecked; S1-04 agrees on (9)–(11)). Route that works: conditional on the design, closed-form marginal likelihoods, Occam factor | method as coded ✓ | equal |
| **P6 coded output** | none (exact posterior only) | DIST-C: deterministic domination transfer to any output-defined law Q ≤ L_nπ; store BMA and HPM/MPM plug-ins; delivery premises explicit | **beats** (beyond [SL]); conditional on discovery / P-STORE / P-HIT; **the run returns no distribution**, so P6 is about distributions reconstructed from the returned store/HPM/MPM | method as coded ✓ (jointly with output) | new (extends C-PACK SL2 from PIPs to the joint parameter law) |
| **Scope** | P_n ≻ n^θ, P_n < exp(Cn^α) | 2 ≤ p_ret ≤ p_raw ≤ n^A, p ≫ n | **short** on exponential p → stretch S-EXP (by-product if Lemma X tracks ℓ_n); no lower growth bound needed (**beats** on small p) | ✓ | equal |
| **Design-agnostic** | tail conditions on x only; no eigenvalue/identifiability condition in Thm 1–2 | sample-level interfaces (E), (C), (ND); no identifiability, no beta-min | **short** by (ND) in DIST-1; **matches** in DIST-2 | ✓ (no family in any statement) | — |

## 3. Boundary numerics (summary; `ASSUMPTION_MAP.md` §3, `work/numerics/RESULTS.md`)
Exact enumeration at p = 12, n = 50…800, 40 replications per cell; p ≫ n on a restricted family. Nothing contradicts a
candidate statement. Outside each assumption: heavy tails (t₂.₅, Pareto 2.1, spikes) — no degradation, transfer ratio
≤ 1.004; (ND) violated by near-duplicates — selection fails, Hellinger numbers unchanged (flag `improvable`); weak
signals — log n-type growth only. Limits (S1-10): averaged, not nested, tails; the scale τ² ≍ log n/n² is untested.

## 4. Better-theorem review (S1; its brief asked for a strictly better statement)
BT1 (drop (F₀) in DIST-3) — adopted. BT2 (oracle exponential bound with additive δ_n) — adopted. BT3
(reference-adaptive size lemma, no p ≤ n^A) — adopted. BT4 (domination transfer for any output law) — adopted.
Details and evidence: `reviews/S1_disposition.md`. S1 also attacked the comparison rows (S1-04); the table above is
the corrected one.

## 5. Target clauses (proposed for HQ to fix at CP1; a WEAKER change to any of them is an early checkpoint)
- **TC1 (metric).** d_H between the joint (x, y) laws f_{S,θ,v} and f*, x-marginal ν_x integrated; rows i.i.d.; ν_x arbitrary.
- **TC2 (DIST-1, conclusion).** Display (1.1): inner threshold e^{−ct}, outer bound 3e^{−ct} + P*(interfaces fail), radius
  C√(t/n), for all t ∈ [M₀ log n, n^{1−κ₀}].
- **TC3 (DIST-1, rate).** Best radius ε_n² = C²M₀ log n/n with M₀ = O((1 + s₀^r)(A + 1)).
- **TC4 (DIST-1, hypotheses).** (RD) — Gaussian noise independent of the design, strict sparsity, p_raw ≤ n^A — and the
  interfaces 𝒟_n, (E; M), (C; M′), (ND; c_D, m_n(t)). No beta-min, no identifiability, no condition on ν_x beyond the
  probability of the interfaces.
- **TC5 (prior).** The coded prior, unchanged and untuned.
- **TC6 (DIST-2).** Display (1.2), radius C√(tℓ_n/n), hypotheses (RD), 𝒟_n, (E), (C).
- **TC7 (DIST-3).** The oracle display Π(d_H > C√(u/n) | D_n) ≤ δ_n + Ce^{−cu} under (E), (L₀), (TR₀), 1 ≤ u ≤ n^{1−κ₀}.
- **TC8 (DIST-C).** (C-0) and the deterministic parts of (C-i), (C-iii); every delivery statement jointly with
  {completed} and under its named premise.
Not target clauses: bridges B1, B2; the stretch statements S-APX, S-EXP, S-FIT; the internal form of Lemmas T, S, V, X,
X′ (their changes are tracked in DEPS and the changelog).
