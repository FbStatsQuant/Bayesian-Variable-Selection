# L-LEAN: Lean 4 formalisation of the exact finite results (REPORT)

Branch `theory/L-LEAN`. Lead: Opus 5.5 (Lean formalization protocol, adapted to the HQ brief: see "Process"). Code state reported here is commit `d58493b`. This report itself was committed afterwards.

## 1. Headline

- **Sorry-free: T21 (C1), T07, T11(iii) and T37(i)/Theorem A.** The abstract finite versions are formalised in Lean 4 and compile with `lake build`: 0 errors, 0 warnings, 0 `sorry`. `#print axioms` shows only `propext`, `Classical.choice` and `Quot.sound` for all 56 audited declarations, and no `sorryAx` (`AXIOMS_RECORD.txt`).
- **T12(i.a) is partial.** The invariance algebra, the one-step resample–move identity and the induction are sorry-free. The probabilistic step (the recursion `hstep`, derived from a model of the island) enters as an explicit, labelled hypothesis. The plan is in `T12_PLAN.md`.
- **Fidelity: GREEN from both checkers.**
  - Fable 5.1 (high) found no objections (`fidelity/FABLE.md`).
  - Astra (xhigh), round 1, was GREEN on T21, T07, T11 and T12, and RED on T37 coverage only (`fidelity/ASTRA_round1.md`).
  - New theorems were added in response, with no frozen statement changed. Astra round 2 found all three objections resolved: OVERALL (T37) GREEN (`fidelity/ASTRA_round2.md`).
- Every frozen statement passes `stmtdiff.py` against `frozen/v1/` (`RESULT OK 0` for all 7 files).

## 2. What is formalised (by target)

Library `SmcBvs` under `theory_campaign/L-LEAN/SmcBvs/`. Per-target table: `STATUS.md`. Per-declaration list (101 declarations, 0 sorry): `DECL_STATUS.md`.

### T21 (C1): `SmcBvs/T21HPM.lean`, `SmcBvs/Basic.lean`

Source: `Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md` §3 (C1), PROOF_v3 lines 52–86. Restated in W2-BOOK §4.1.

Setting: a probability space `(Ω, P)` and a finite model space `A`.
- `F ω` is the score and `π = post (F ω) A`.
- `U` is the "no output" event.
- `𝒮 ω ⊆ A` is the scored set on `Uᶜ`.
- On `Uᶜ`, `Ŝ ω` is a maximiser of `F ω` over `𝒮 ω`. Every tie rule satisfies this, the method's included.

Theorems:
- `hpm_eq_truth`: π(S₀) > ½ and S₀ ∈ 𝒮 imply Ŝ = S₀.
- `t21_decomposition`: P(U ∨ Ŝ≠S₀) ≤ P(U) + P(Uᶜ, S₀∉𝒮) + P(Uᶜ, S₀∈𝒮, π(S₀) ≤ ½). No measurability is needed.
- `t21_decomposition'`: the brief's form, with P(S₀ ∉ 𝒮).
- `markov_half`.
- `t21_C1`: P(U ∨ Ŝ≠S₀) ≤ P(U) + 2E δ₁ + P(Uᶜ, S₀∉𝒮), with δ₁ = 1 − π(S₀).
- `integral_le_eps_add_prob`: the finite step of "H03 ⇒ E₀δ₁ → 0".

### T07: `SmcBvs/T07Bayes.lean`

Sources: `T06_T07_identifiability_size_prior/STATEMENT.md` §2 and PROOF_v2 §T07, plus W2-BOOK PROOF.md §3 (i′).

- **(i)** `ceiling`. Its contrapositive is `no_size_prior_repairs`: no positive size-only prior repairs a within-size ranking error, whether S₀ is beaten in m or tied and ≺-preceded.
- **(i′)** `ceiling_sharp`: some positive size-only prior recovers S₀ if S*_{s₀} = S₀.
- **(ii)(a)** `risk01_eq`, `risk01_min_iff`, `hpm_min_risk01`: the HPM minimises the 0–1 loss, and the minimisers are exactly argmax_Ω F.
- **(ii)(b)** `riskH_eq`, `mpm_min_riskH`, `mpm_unique_iff`: the MPM minimises the Hamming loss, uniquely iff no PIP equals ½.
- **(ii)(c)** `capped_mpm_min_riskH`.
- **Lemma psi** `psi_Jplus_le`, `psi_Jplus_unique_iff`, `psi_capped_le`, `exists_capped`.
- **(iii)(a)** `reported_eq_hpm_iff`, `reported_min_risk01_iff`.
- **(iii)(b)** `reported_truth_needs_unscored`.
- **(iii)(c)** `excess_riskH_le`: 0 ≤ ρ_H(â) − ρ_H(a_opt) ≤ 2Σ_{â△a_opt}|q̂−PIP| ≤ 2‖q̂−PIP‖₁. Also `mpm_hat_eq_iff`.

### T11(iii): `SmcBvs/T11Miss.lean`

Source: `T11_LLED_scoring_ledger/STATEMENT.md`, Claim (iii).

- `t11_miss_pi` and `t11_miss_pi_real`, on the product space ⊗π₀: P(s never drawn in Q draws) = (1 − π₀{s})^Q ≤ exp(−Qπ₀{s}).
- `t11_miss_iid` and `t11_miss_iid_real`: the same for any independent family with law π₀, using `iIndepFun`.
- `t11_pow_le_exp`.
- The conditional-on-𝓒 claim is read pointwise, with Q = Q_f, S* and π₀ fixed by 𝓒 (ASSUMPTIONS A-T11-1).

### T37(i) / Theorem A: `SmcBvs/T37Greedy.lean` (abstract core), `SmcBvs/T37Lattice.lean` (model lattice)

Sources: W1-T37R PROOF.md (Lemma 0, Definitions, Lemma 2(a), Theorem A) and W3-VT37R REPAIRS.md R1 and R3.

**Abstract core.** States carry a neighbourhood `N`, a score `F` and a potential Φ. The greedy map `M` is any best strict-improvement map, with any tie rule; `exists_bestImprovement` shows one exists. The path is the iterate of `M`, and the capped search is `path M S_c ℓ`, certified when `M(returned) = none`.

| Source item | Abstract (`T37Greedy`) | Model lattice (`T37Lattice`) |
|---|---|---|
| Lemma 0(a) | `path_F_strictMono` | — |
| Lemma 0(c) | `lemma0c` (assumes only "reaches S₀ and stops certified"), `lemma0c_hpm` (pre-search ledger, post-search ledger; Ŝ = S₀ up to exact ties, and equal under an injective tie rank) | — |
| A1 | `theoremA1` (TD′_∞ ⇒ reach within r_R(S)), `theoremA1_converse` | — |
| A2 | `theoremA2` (TD′_P ⇒ reach in τ ≤ Φ(S) moves, Φ strictly decreasing) | `theoremA2_lattice` (path stays in Lat(S) ∩ R_{a,d}), `theoremA2_lattice_count` (τ + σ = m + e and max(m, e) ≤ τ ≤ Φ, where σ counts extra→truth swaps by `drop_two_swap` and `swap_extra_truth_drop_two`) |
| A3 | `theoremA3`, `theoremA3_hpm` | `theoremA3_lattice` (ℓ ≥ Φ), `theoremA3_lattice_tau` (ℓ ≥ τ), `theoremA3_lattice_only` ((L) plus the one-state events D_S on Lat(S_c) only) |
| A4, PD part | `pd_of_reach` | — |
| Lemma 2(a) and the move table | — | `progress_mem_Lat`, `lemma2a` |
| Feasibility | — | `Φ_le_of_mem_Rad`, `card_le_of_mem_Rad` (R_{a,d} is feasible when s₀ + d ≤ K) |

### T12(i.a), partial: `SmcBvs/T12Core.lean`

- `invariance_step`: γ_{t−1}(G_t·K_t f) = γ_t(f).
- `resample_move_step`: the fixed-population resample–move algebra.
- `unbiased_of_step`: E_t f = Σ γ_t f, given the stage-0 identity `h0` and the recursion `hstep`.

## 3. What has sorries or is not formalised, and why

- **No sorries anywhere.**
- **T12(i.a): the probabilistic island model is not formalised.** Multinomial resampling, rounds that are conditionally independent given the past, and the tower property would together yield `hstep`. Mathlib has no `PMF.pi`, so the product-law plumbing is the main cost, estimated at 300–600 lines. `T12_PLAN.md` gives the 5-step plan. `unbiased_of_step` is a reduction, not a full unbiasedness theorem.
- **Out of scope by the brief ("abstract, finite").**
  - T21 routes (a)–(f) and the asymptotic H03/H10/H24 statements.
  - T11 as a regular conditional probability given 𝓒.
  - T37's remaining A4 clauses, A5 (relation to literal TD), and Theorems B and C.
  - The SMC-BVS score formula itself: F and m are arbitrary reals, with m > 0 where the source uses it.
- **External theorems entering as hypotheses: none, except T12's `hstep`/`h0`.** These are labelled in the docstring as the not-yet-formalised step, and they are not axioms. All other hypotheses are the theorems' own assumptions, or readings recorded in `ASSUMPTIONS.md`.

## 4. Build instructions and versions

- Lean `v4.35.0-rc2` (`lean-toolchain`); Lake 5.0.0. Mathlib rev `065356127b1dc0016f66b7283ce0ce2c4055aa55` (tag `v4.35.0-rc2`), pinned in `lake-manifest.json`.
- **On Felipe's laptop**, run `cd theory_campaign/L-LEAN/SmcBvs && lake build`. `lakefile.toml` uses `packagesDir = "C:/lean/packages/v4.35.0-rc2"`, the shared Mathlib with built oleans.
  - A clean rebuild of the project's own modules takes ≈5 min (`CLEAN_BUILD.txt`; `.lake/build` deleted first, never `lake clean`). An incremental module build takes ≈20–30 s.
- **Elsewhere**, delete the `packagesDir` line, then run `lake exe cache get` and `lake build`.
- Modules use targeted Mathlib imports, not `import Mathlib`. On this machine, under memory pressure, a full `import Mathlib` took more than 30 min to load (`FAILED_ATTEMPTS.md`, `MATHLIB_NOTES.md`).
- `SmcBvs/Axioms.lean` prints `#print axioms` for every main declaration during the build. The record is in `AXIOMS_RECORD.txt`.

## 5. Process and evidence

- **Statements.** All statements were frozen in `frozen/v1/` before the remaining proofs were written. After each helper return and at the end, `stmtdiff.py` showed `RESULT OK 0` for all files. Later results were added as new declarations only.
- **Fidelity.** Packets are in `fidelity/packet` and `fidelity/packet2`.
  - Fable 5.1 (read-only Plan agent): GREEN, with 12 minor remarks.
  - Astra round 1: RED on T37 coverage, 3 objections.
  - Astra round 2: all three resolved, GREEN.
  - Every decision is listed in `ADVISER_DECISIONS.md`.
- **Agent counts.**
  - Opus 5.5 (high) helpers: 2. H1 proved the T37 lattice module; H2 proved the T07 ψ lemmas.
  - Fable 5.1: 1 call.
  - Astra: 3 codex calls. The first was killed because codex waited on stdin; that is a harness issue, not a model failure.
  - Sonnet, Haiku and Sol: 0.
- **Deviations from the Lean protocol** (HQ brief; ASSUMPTIONS A-P1–A-P3):
  - Location is the repo folder.
  - Helpers were capped at 3 at once, with Opus only.
  - There was no design department and no 5-agent Sol review round. The lead's review, the frozen-statement diff, the axiom audit and the two-model fidelity check stand in for them.
- **Machine note.** During the run, free RAM was about 3.5 GB out of 32 GB. A `find / -iname F1_worker*` process from another session had been running since 09:32 and was left untouched.

## 6. Eight-line summary

1. T21 (C1): sorry-free. Event decomposition, the brief's form, and the 2E₀δ₁ form via Markov; any tie rule.
2. T07: sorry-free. Ceiling and sharpness, 0–1/HPM, Hamming/MPM, capped MPM, ψ lemmas, reported-object results, PIP-error excess-risk bound.
3. T11(iii): sorry-free. (1−π₀(S*))^Q ≤ exp(−Qπ₀(S*)), in both product-space and iid-family forms.
4. T37(i)/Theorem A: sorry-free. Lemma 0(a)/(c), A1⇔, A2 with move count, A3 (Rad, sharp cap, lattice-only D_S), PD, Lemma 2(a).
5. T12(i.a): partial. Invariance, the resample–move step and the induction are proven; the probabilistic recursion `hstep` is an explicit hypothesis (`T12_PLAN.md`).
6. Build: `lake build` green, 0 warnings, 0 sorry, axioms = {propext, Classical.choice, Quot.sound}; Lean 4.35.0-rc2, Mathlib 065356127b1d.
7. Fidelity: Fable GREEN; Astra GREEN after round 2 (round 1 was RED on T37 coverage, fixed by additions only).
8. Code head `d58493b` on `theory/L-LEAN`; this report was committed on top (see the final chat summary for the final SHA).
