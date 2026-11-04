# Fable 5.1 (high) fidelity report: statements of frozen v1

Reviewer: Fable 5.1, read-only Plan agent. Inputs: `packet/` only (SOURCES.md, ASSUMPTIONS.md, lean/*.lean). No commands were run. This is the agent's returned report, saved by the lead.

## Verdict table (condensed: every row was GREEN)

| Group | Lean names | Verdict |
|---|---|---|
| Basic | `post`, `IsArgmax`, `IsLeastArgmax`, `strict_max_of_post_gt_half` | GREEN |
| T21 | `hpm_eq_truth`, `t21_event_subset`, `t21_decomposition`, `t21_decomposition'`, `markov_half`, `measurable_post`, `t21_C1`, `integral_le_eps_add_prob` | GREEN |
| T07 defs | `Ωf`, `sizeClass`, `normW`, `sizePrior`, `PosSizePrior`, `π`, `PIP`, `risk01`, `riskH`, `psi`, `Jplus` | GREEN |
| T07 (i), (i′) | `ceiling`, `no_size_prior_repairs`, `ceiling_sharp` | GREEN |
| T07 (ii), Lemma psi | `risk01_eq`, `risk01_min_iff`, `hpm_min_risk01`, `riskH_eq`, `psi_Jplus_le`, `psi_Jplus_unique_iff`, `mpm_min_riskH`, `mpm_unique_iff`, `psi_capped_le`, `exists_capped`, `capped_mpm_min_riskH` | GREEN |
| T07 (iii) | `reported_eq_hpm_iff`, `reported_min_risk01_iff`, `reported_truth_needs_unscored`, `excess_riskH_le`, `mpm_hat_eq_iff` | GREEN |
| T11(iii) | `t11_pow_le_exp`, `t11_miss_pi`, `t11_miss_pi_real`, `t11_miss_iid` | GREEN |
| T37 abstract | `IsBestImprovement`, `step`, `path`, `exists_bestImprovement`, `path_F_le/_mono/_strictMono`, `TDinf`, `rankAbove`, `theoremA1`, `theoremA1_converse`, `TDP`, `theoremA2`, `theoremA3`, `pd_of_reach` | GREEN |
| T37 lattice | `IsFlipSwap`, `nbhd`, `mis`, `ext`, `Φ`, `Rad`, `Lat`, `Φ_eq`, `mis_ext_le_of_mem_Lat`, `Lat_subset`, `progress_mem_Lat`, `lemma2a`, `TDP'`, `theoremA2_lattice`, `theoremA3_lattice`, `Φ_le_of_mem_Rad` | GREEN |
| T12 partial | `kapply`, `Invariant`, `invariance_step`, `resample_move_step`, `unbiased_of_step` (with `hstep`/`h0` "explicit, honestly labelled hypotheses") | GREEN |

## Objections

None. In Fable's words: "No Lean statement weakens, alters, or trivialises its source claim. Every added hypothesis is either in the source or recorded in ASSUMPTIONS.md. The external step in T12Core.lean (`hstep`) is an explicit hypothesis with an accurate 'Not formalised (TODO)' paragraph, not an axiom."

## Minor remarks (non-blocking), as returned

1. `theoremA3` gives the score-bound part of Lemma 0(c), not the clause "Ŝ = S₀ after the search". Suggestion: add a corollary and reword the docstring.
2. The docstring of `exists_bestImprovement` mentions an injective tie rank, but the theorem takes no rank.
3. `Rad` has no size cap. It coincides with the source R_{a,d} when s₀ + d ≤ K. Suggestion: add a variant with that hypothesis.
4. τ = m + e − σ and τ ≥ max(m, e) are not formalised; only τ ≤ Φ is.
5. Not formalised: the A3 lattice-condition variant (the D_S events), and the remaining A4 clauses.
6. `theoremA1_converse` puts `M S₀ = none` inside the per-S existential. This is harmless.
7. The real-valued exponential corollary exists for the product form only, not for `t11_miss_iid`.
8. (iii)(b) uses F = log(pw·m) without W_K. The argmax is invariant, so this is fine.
9. (iii)(c) allows any real q̂. This is more general and fine.
10. The W2-BOOK (iii′) attribution for `no_size_prior_repairs` is not in SOURCES.md.
11. The convention behind T12 `h0` should be stated in the docstring. `unbiased_of_step` holds for all t ∈ ℕ, which is stronger than needed and harmless.
12. `t21_decomposition'` counts ω ∈ U inside P(S₀ ∉ 𝒮). This is the brief's form and is fine.

OVERALL: GREEN
