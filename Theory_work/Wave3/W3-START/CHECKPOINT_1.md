# W3-START — CHECKPOINT 1 (target fixed) — 2026-11-11

Lead: Claude Fable 5.2 (Claude Personal, effort high). Worktree `C:/Users/felip/BVS-wt/W3-START`, no git state changed.
**Nothing is proved yet.** This checkpoint fixes the target: STATEMENT v1.2 is locked, the sharpness gate has run, and
three improvements are recommended for HQ's decision. No proof work has been done beyond sketches.

## 1. Locked statement (`STATEMENT.md` v1.2)
π₀ = the start exactly as `main` computes it (pins in §1; CORE identical at d6da494 and fe9a066). o₀ := start odds
against S₀.
* **Table identities (deterministic).** T₁ ≤ o₀ ≤ T₁ + R₂ + [∏_b(1 + Ξ_b) − 1](1 − U)^{−(16s₀+1)}, and o₀ ≥ c_sΞ. T₁ = the
  prior-weighted sum of the single-null block Bayes factors; Ξ = the prior-weighted table mass of every
  configuration of a truth's block that misses a truth. Lattice version for a leakage set Q.
* **Floor (deterministic).** Every model with |S| < K has 1 − π₀(S) ≥ ⅓(n + 1)^{−1/2} on every data set. So with at
  least one null, no condition gives a start-mass rate better than n^{−1/2}.
* **Fixed design (START-F).** Under an energy bound, small-set eigenvalue floors, visibility, and an averaged leakage
  condition (AL) on (X, θ*): o₀ = O_P(n^{−1/2}𝔏⁰_n + n^{−1}𝔏_n(S₀)²) + o_P(n^{−κ}) for every κ below the visibility
  exponent; o₀/T₁ → 1 under slightly more; lattice mass 1 − π₀(𝓛(Q)) = O_P((|Q| + 1)n^{−1/2}𝔏_n(Q)) + o_P(n^{−κ}).
  The leakage functionals are deterministic and of order 1 to √log n when nothing leaks. Uniform over the class.
* **Gaussian rows (START-R), p ≫ n allowed.** Under W3-RM's population visibility and no-leakage conditions:
  π₀(S₀) ≥ 1 − n^{−1/2}e^{C√log n} with probability → 1, hence π₀(S₀) ≥ 1 − n^{−c} for every c < ½.
* **Limits (NEC).** One null with normalised gain above (1 + 2Ā) log n, or one truth below (1 + 2A̲) log n, sends
  π₀(S₀) → 0. Masked truths and strong-factor designs at p > K are outside the hypotheses (decision D1 not covered).
* **Interfaces.** P-START for W3-SAMP with an explicit rate; a deterministic inequality and a corollary for P-OVL;
  the misspecified-candidate form (C-MIS) by a locally re-proved reduction.
All theorem hypotheses are partition-free conditions on (X, θ*) or (Σ_n, θ*); no design family anywhere; blocks only
in the labelled component lemmas about the coded tables.

## 2. Review record
| round | seat | manifest digest | verdict | file |
|---|---|---|---|---|
| SL1 | Sol (blind) | 53849ef3… | DO NOT LOCK: 4 CRITICAL, 3 MAJOR, 1 MINOR | `reviews/SL1_statement_lock_sol.md`, `SL1_disposition.md` |
| RC2 | Sol (reconciliation) | 3c89e73a… | all SL1 CRITICAL/MAJOR resolved | `reviews/RC2_reconciliation_sol.md` |
| SL2 | Sol (fresh, blind) | 3c89e73a… | LOCK WITH CHANGES: 1 CRITICAL (a summary sentence), 2 MINOR, 3 optional — all applied verbatim | `reviews/SL2_statement_lock_sol.md`, `SL2_disposition.md` |
| BT1 | Astra (blind) | b3fafa79… | 3 proposals: 2 ADOPT NOW, 1 WORTH A TICKET | `reviews/BT1_better_theorem_astra.md`, `BT1_disposition.md` |
`manifest.py bind` passes for SL2, RC2 and BT1; `verify` passes on the current tree for MANIFEST_BT1.
SL1's criticals were real errors in v1.0 (a floor claimed for saturated models; an odds bound without the leakage
hypothesis; a headline that dropped two terms; a ratio undefined at p = s₀). v1.2 is the corrected statement.
One protocol note: the first statement-lock round did not lock, so a second round was run (fresh blind seat plus
reconciliation seat); no layer was skipped.

## 3. Necessity reading of each assumption (numerics: `numerics/RESULTS.md`, production core, 1018 runs, p = 2n, n ≤ 1600)
| assumption | reading | evidence |
|---|---|---|
| exponent ½ | NECESSARY | deterministic floor; T₁ ≥ f_n in every run (min ratio 1.10) |
| visibility at the constant 1 + 2A | NECESSARY, constant sharp | (N3); mass lost at level ≤ 3, kept at ≥ 4.5 (threshold 3.2) |
| (V-c) over all 15-sets | IMPROVABLE → replaced by Ξ / (V-m) in v1.1 | truths with 15 close correlates: (V-c) level 0.3–1.6, old functional ≈ 10⁴, yet π₀(S₀) = 0.82–0.96 and Ξ → 0 |
| averaged leakage (AL) | tracks the truth when all nulls leak; conservative for isolated leakers | transition at η ≈ 2/3 as the functional predicts (T₁/prediction ≈ 1), versus η_A ≈ 0.09 for the uniform condition; one leaking null is harmless up to 3.2 but (AL) rejects it above ≈ 1.3 |
| one null below (1 + 2A)τ² log n | NECESSARY, constant sharp | (N2); π₀(S₀) = 0.4 at level 3, 0.004 at 4.5 |
| eigenvalue floor (FL-16) | IMPROVABLE | near-twin nulls (λ_min ≈ 1/n): same rate |
| energy bound ‖μ‖² ≤ Mn | IMPROVABLE in the tested direction (θ ∝ n^{1/4}); not removable outright (reviewer) | o₀√n unchanged |
| s₀ fixed | not binding by itself | s₀ ≤ 4 scales as (s₀ + 1); at s₀ = 16, 32 the mass is lost because visibility fails (τ² grows with ‖θ‖²) |
| Gaussian-row leakage scale C_L n^{−1/2} | not a threshold | C_L = 1 converges; C_L = 2, 4 still have U > 1 at n = 1600 (U decreasing); graded just outside |
| Gaussian noise; localisation (L-loc-R) | route assumptions | not tested |
Inside the assumptions: exact order n^{−1/2} in fixed zero-leakage designs (o₀√n flat at ≈ 2.4 and ≈ 1.9), o₀/T₁ → 1,
and the table identities hold in every run (upper bound tight to 0.90). Lattice form: AR(1) rows lose the mass at S₀
but the lattice mass rises (0.66 → 0.81).

## 4. Better-theorem proposals and dispositions (lead's recommendations; HQ decides)
| label | proposal | disposition |
|---|---|---|
| P1 (Astra) | constant unnormalised Gram floor λ_min(X_TᵀX_T) ≥ g_* instead of (FL-16) | **ADOPT** — both scalar bounds re-derived by the lead; covers the near-twin numerics; cost: re-prove the toolkit expansion locally (then C-GROW:L0.1/L0.2 are no longer consumed) |
| P2 (Astra) | column-specific truncation levels in the leakage functional | **ADOPT** as the general form of (AL), default unchanged — closes the gap for isolated leakers exactly to the (N2) threshold 1 + 2A |
| P3 (Astra) | transfer to design-measurable θ*(X), S₀(X), Q(X) | **ADOPT** — immediate from the uniform clause |
| G1 (lead) | Ξ and margin visibility (V-m) | already ADOPTED in v1.1, lock-reviewed |
| G2 (lead) | Gaussian rows with a population leakage level η and an explicit exponent | **DEFER** — open item W3-START-O1, decide at CP3 |
| G3 (lead) | isolated leakers through Q | **REJECT** in favour of P2 |
| G4 | no Gram floor among nulls at all | **DEFER** — open item W3-START-O2 (needs a rank-sensitive aggregation) |
| G5 | weaken the energy bound | **REJECT for now** (reviewer's obstruction; numerics cover one direction only) |
| G6 | growing s₀ | **DEFER** — open item W3-START-O3 |
Evidence per row: `reviews/BT1_disposition.md`. Reviewer found no credible improvement for: removing the floor
entirely, dropping 𝔏_n(S₀), a cleaner (V-m), removing e^{C√log n} or localisation, a universal √(log p/n) lower bound.

## 5. What this does and does not give the program
* Gives P-START with a rate under primitive no-leakage conditions, fixed design and Gaussian rows, p ≫ n included.
* Does not cover D1 (strong factors) or masked truths; with leakage only the lattice mass is claimed.
* Finding worth knowing: the start needs each truth visible at (1 + 2A)·τ²·log n, where τ² includes the signal its
  block leaves unexplained — a stronger requirement than the posterior's beta-min when many truths sit in other blocks.
* Observation, stated without judgement: for Gaussian rows with every null leaking at C_L n^{−1/2}, the factor
  e^{C√log n} is large (C_L = 2: π₀(S₀) ≈ 0.1 at n = 1600).

## 6. Plan for CP2 and honest estimate
If HQ adopts P1–P3: (0) STATEMENT v1.3 with the three changes + one fresh Sol check of the change (≈ 1 h).
Then, each lemma with a cross-family line check and falsification numerics:
L1 AGG incl. Ξ and FLOOR (deterministic; enumeration tests exist) · L2 toolkit under the new floor, τ-form RSS bounds ·
L3 Lemma J and bridge (B-L) · L4 visibility bridges (B-V1), (B-V2) · L5 assembly and START-F with the uniform clause.
CP2 = L1–L5 written and line-checked, then the independent mid-point review.
Estimate: **7–10 hours of lead run time** (about 4 h writing, 4 lemma checks, numerics, mid-point). Main risk in this
part: the uniform (finite-n) form of START-F and the stochastic remainders in (B-V2).
After CP2 (to CP3): corollaries, NEC, OVL, MIS, transfer, and the Gaussian-row bridge (B-R) — the largest single
obligation and the main risk of the ticket (the averaged maximum over selected 15-sets). Estimate 8–12 hours more. If
(B-R) fails after one attempt and one break review, (T3)(b) is narrowed to what the transfer clause gives and
returns through CP1, as PROTOCOL rule 10 requires.

## 7. Decisions requested from HQ
1. Adopt P1, P2, P3 (recommended), or lock the target at v1.2 as is.
2. Keep Proposition OVL (the "if cheap" item) in the target, or drop it to an open item.
3. Confirm the deferrals O1–O3.

## 8. Record
Agents: lead (Claude Fable 5.2, Claude Personal); SL1, SL2, RC2 (Codex gpt-6.1-sol, high); BT1 (Codex gpt-6-astra,
high). Claude tally: CP 1 / CW 0. No NOTS use. `HOLDS.md` read before each step from 12:17 on: no holds.
Consumed claims: C-GROW:L0.1@1.0.0, C-GROW:L0.2@1.0.0 (both PROVED-CHECKED, ACTIVE; not consumed any more if P1 is
adopted). Files: `STATEMENT.md`, `PLAN.md`, `ASSUMPTION_MAP.md`, `numerics/` (scripts, raw and summary CSV, RESULTS.md),
`reviews/` (4 briefs, 3 manifests, 4 reviews, 3 dispositions, INPUTS.txt), `LOG.md`. Everything is uncommitted; HQ commits.
