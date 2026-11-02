# STATUS (L-LEAN): resume point

Package: `theory_campaign/L-LEAN/SmcBvs/` (Lean `v4.35.0-rc2`, Mathlib rev `065356127b1d`). `lake build` is green: 0 errors, 0 warnings, 0 `sorry`. A per-declaration list (87 declarations) is in `DECL_STATUS.md`, and the `#print axioms` output is in `AXIOMS_RECORD.txt`.

| Target | Lean file | Formalised | Sorry-free | Depends on (hypotheses / external inputs) |
|---|---|---|---|---|
| T21 (C1), abstract finite | `T21HPM.lean` (+ `Basic.lean`) | `hpm_eq_truth`, `t21_event_subset`, `t21_decomposition` (sharp), `t21_decomposition'` (brief form), `markov_half`, `t21_C1` (2E₀δ₁ form), `integral_le_eps_add_prob` | yes | Ŝ is a maximiser of F over 𝒮 on Uᶜ (any tie rule); 𝒮 ⊆ Ω on Uᶜ; for `t21_C1`, each ω ↦ F ω S is measurable. Routes (a)–(f) and the H03 asymptotics are not formalised. |
| T07 (i), (i′), (ii)(a)(b)(c), (iii)(a)(b)(c), Lemma psi | `T07Bayes.lean` | `ceiling`, `no_size_prior_repairs`, `ceiling_sharp`, `risk01_eq`, `risk01_min_iff`, `hpm_min_risk01`, `riskH_eq`, `psi_Jplus_le`, `psi_Jplus_unique_iff`, `mpm_min_riskH`, `mpm_unique_iff`, `psi_capped_le`, `exists_capped`, `capped_mpm_min_riskH`, `reported_eq_hpm_iff`, `reported_min_risk01_iff`, `reported_truth_needs_unscored`, `excess_riskH_le`, `mpm_hat_eq_iff` | yes | Tie order is an injective rank. m > 0 only where the source uses it ((i′), (iii)(b)). No external theorems. |
| T11(iii) | `T11Miss.lean` | `t11_miss_pi`, `t11_miss_pi_real`, `t11_miss_iid`, `t11_pow_le_exp` | yes | Q, S*, π₀ fixed (the conditional-on-𝓒 statement read pointwise; ASSUMPTIONS A-T11-1); the draws are independent with law π₀. |
| T37(i) / Theorem A | `T37Greedy.lean`, `T37Lattice.lean` | abstract: `exists_bestImprovement`, Lemma 0(a) `path_F_strictMono`, A1 `theoremA1` and `theoremA1_converse`, A2 `theoremA2`, A3 with Lemma 0(c) `theoremA3`, A4-PD `pd_of_reach`; concrete lattice: `progress_mem_Lat` (move table), `lemma2a`, `theoremA2_lattice`, `theoremA3_lattice`, `Φ_le_of_mem_Rad` | yes | TD′_∞ / TD′_P as hypotheses (they are the theorem's own assumptions); M any best-improvement map. A5 (relation to literal TD) and Theorems B and C are not formalised. |
| T12(i.a) | `T12Core.lean` | `invariance_step`, `resample_move_step`, `unbiased_of_step` | yes, partial | **The resample–move recursion `hstep` is an explicit hypothesis**: the probabilistic island model is not formalised. Plan: `T12_PLAN.md`. |

Fidelity check (Fable 5.1 and Astra): see `fidelity/`. The result goes in `REPORT.md`.
