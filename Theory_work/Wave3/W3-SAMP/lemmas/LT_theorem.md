# Theorem LT♯ — corrected lower-tail transfer for the coded outputs

Status: PROVED (by this seat, unchecked). v2, 2026-11-09 (v1 → v2: Step 2′ weighted uniform bound and LT-b′, LT-e′ with a
vanishing threshold, from BT1 §4.1, §5, re-derived). Statement: STATEMENT.md v3 §2 "Theorem LT♯". Uses Lemma MR
(`MR_identities.md`), Lemma ST (`ST_stay.md`), Lemma PC (`PC_completed.md`), CC3 (`CC_code_check.md`).

Throughout: fixed data; island r; everything "given 𝓒 on 𝒜" in the localised form (STATEMENT §0); W := W_r.
For q = 1..4 (measured round q), let
- B_q := 1 − A_{r,q−1} (fraction of particles **not** at S₀ when entering measured round q; A_{r,0} = after the L
  burn-in rounds), B̄ := ¼Σ_{q=1}^{4} B_q;
- Λ_q := (1/N_e)·#{i : particle i enters measured round q at S₀ and is away from S₀ at some time of that round},
  Λ̄ := ¼Σ_q Λ_q.

## Step 1 (pathwise decomposition)

Fix j. For a pair (q, i) call it *good* if particle i enters measured round q at S₀ and is at S₀ at every time of the round.
For a good pair, Y^i_{q,j} = S₀ (the state immediately before its Gibbs-j step is S₀), so its recorded value is o_j(S₀) and
|o_j(Y^i_{q,j}) − 1{j ∈ S₀}| ≤ κ₀. For any other pair the term is ≤ 1 (o_j ∈ [0, 1]). The bad pairs of round q are those
entering away from S₀ (fraction B_q) or entering at S₀ and leaving (fraction Λ_q). By CC3,
p̂_r(j) − 1{j ∈ S₀} = (4N_e)⁻¹Σ_{q,i}[o_j(Y^i_{q,j}) − 1{j ∈ S₀}], hence for **every** j simultaneously
  |p̂_r(j) − 1{j ∈ S₀}| ≤ κ₀ + B̄ + Λ̄.                                                        (1)
The good/bad classification does not depend on j; this is why no union over coordinates (no factor p) appears.

## Step 2 (the two expectations)

(a) *Weighted.* By MR-b with h = 1{S ≠ S₀} (data-only, bounded) and s = L + q − 1 (q = 1..4):
E[W·B_q | 𝓒] = 1 − π(S₀) = δ, so E[W·B̄ | 𝓒] = δ. Likewise E[W(1 − A_{r,q}) | 𝓒] = δ for q = 0..4.
(b) *Unweighted.* Fix c (Step 1 of MR). Let H_q be everything before measured round q. By ST-c, applied to each particle
entering at S₀ (its order is uniform and independent of H_q, and its path given H_q and the order is the Markov chain of
T12 (R3)), P(particle i leaves during round q | H_q) ≤ λ₀ on {X^i entering = S₀}. Summing over i,
E_c[Λ_q | H_q] ≤ λ₀(1 − B_q) ≤ λ₀, so E_c[Λ̄] ≤ λ₀ ≤ 19·o₁. Λ̄ is a bounded measurable function of the augmented record
(orders and within-round paths are in Φ; MR Step 2), so by the freezing lemma E[Λ̄ | 𝓒] ≤ λ₀ ≤ 19·o₁ in localised form.

## Step 2′ (weighted uniform bound; LT-b′)

Let E_r := ‖p̂_r − 1_{S₀}‖_∞ and g := min{1, κ₀ + δ + (1 − δ)λ₀}. W is measurable with respect to H_q (the evidence is not
updated after stage T), and E_c[Λ_q | H_q] ≤ λ₀·(1 − B_q) = λ₀A_{r,q−1} (Step 2(b)). Hence, by MR-b with h = 1{S = S₀},
E[W Λ_q] = E[W·E[Λ_q | H_q]] ≤ λ₀E[W A_{r,q−1}] = λ₀(1 − δ). With (1), E_r ≤ min{1, κ₀ + B̄ + Λ̄}, so
E[W E_r] ≤ min{E W, κ₀E W + E[W B̄] + E[W Λ̄]} ≤ min{1, κ₀ + δ + (1 − δ)λ₀} = g        (2)
(E W = 1). Markov on {W ≥ η}: (LT-b′) P(E_r ≥ u | 𝓒) ≤ g/(uη) + P(W < η | 𝓒) for u, η > 0 (non-strict tail;
Markov applies to {W E_r ≥ uη}). Since g ≤ 21·o₁, this bound
needs only one Markov step and no κ₀ offset; LT-b and LT-b′ are both valid and the minimum may be used.

## Step 3 (LT-a, LT-b, LT-c)

For ε, η > 0: on {B̄ ≥ ε, W ≥ η}, W·B̄ ≥ εη. Markov (conditional on 𝓒) with Step 2(a):
P(B̄ ≥ ε, W ≥ η | 𝓒) ≤ δ/(εη), so P(B̄ ≥ ε | 𝓒) ≤ δ/(εη) + P(W < η | 𝓒). The same argument with 1 − A_{r,q} in place of B̄
is (LT-a). Markov with Step 2(b): P(Λ̄ ≥ ε | 𝓒) ≤ 19·o₁/ε. By (1), {max_j |p̂_r(j) − 1{j ∈ S₀}| ≥ κ₀ + 2ε} ⊆ {B̄ ≥ ε} ∪
{Λ̄ ≥ ε}; the union bound gives (LT-b).
(LT-c): every particle state is an evaluated model (initial draws and every accepted move were evaluated, CC1–CC2), so
{S₀ ∉ 𝓜_r} ⊆ {A_{r,0} = 0} = {1 − A_{r,0} ≥ 1}; apply (LT-a) with q = 0, ε = 1.

## Step 4 (LT-d: pooled outputs)

pip_primary = ¼Σ_r p̂_r (CC3), so for every j, |pip_primary(j) − 1{j ∈ S₀}| ≤ ¼Σ_r|p̂_r(j) − 1{j ∈ S₀}| ≤ max_r‖p̂_r − 1_{S₀}‖_∞.
*MPM.* MPM = {j : pip_primary(j) > ½}. If MPM ≠ S₀ there is j ∈ S₀ with pip_primary(j) ≤ ½ or j ∉ S₀ with
pip_primary(j) > ½; either way |pip_primary(j) − 1{j ∈ S₀}| ≥ ½ (the strict threshold and the tie at ½ are covered). So
{MPM ≠ S₀} ⊆ ∪_r{‖p̂_r − 1_{S₀}‖_∞ ≥ ½}. If o₁ ≤ ¼, then κ₀ + 2·(1/8) ≤ ½ (κ₀ ≤ o₁, ST-b), so by (LT-b) with ε = 1/8,
P(‖p̂_r − 1_{S₀}‖_∞ ≥ ½ | 𝓒) ≤ 8δ/η + 152·o₁ + P(W_r < η | 𝓒); sum over r ≤ 4 (no independence between islands used).
*HPM.* By Lemma PC and the deterministic step of `D_theorem.md` §3: on {completed} ∩ {δ < ½} ∩ {S₀ ∈ 𝓜}, Ŝ = S₀.

## Step 5 (LT-e: asymptotics under the joint law)

Assume P-CONC and NC_r for r ≤ 4. Fix ε > 0 and η > 0. The conditional bounds are 𝓒-measurable random variables ≤ 1 after
truncation, so integrating over 𝓒 and the data:
- PIPs: {‖pip_primary − 1‖_∞ > ε} ⊆ {κ₀ > ε/3} ∪ ∪_r{‖p̂_r − 1‖_∞ ≥ κ₀ + 2ε/3}; hence
  P(𝒜 ∩ {‖pip_primary − 1‖_∞ > ε}) ≤ P(o₁ > ε/3) + Σ_r E[1_𝒜 min(1, 3δ/(εη) + 57·o₁/ε)] + Σ_r P(𝒜 ∩ {W_r < η}).
  As n → ∞, o₁ = δ/(1 − δ) → 0 and δ → 0 in probability (P-CONC), so the first two terms → 0 (bounded convergence);
  then limsup_n ≤ Σ_r limsup_n P(𝒜 ∩ {W_r < η}), which → 0 as η ↓ 0 by NC_r. So the limit is 0.
- MPM: P(𝒜 ∩ {MPM ≠ S₀}) ≤ P(o₁ > ¼) + Σ_r{E[1_𝒜 min(1, 8δ/η + 152·o₁)] + P(𝒜 ∩ {W_r < η})} → (same argument) 0.
- Endpoints: P(𝒜 ∩ {1 − A_{r,q} > ε}) ≤ E[1_𝒜 min(1, δ/(εη))] + P(𝒜 ∩ {W_r < η}) → 0.
- HPM: {completed} ∩ {Ŝ ≠ S₀} ⊆ {δ ≥ ½} ∪ (𝒜 ∩ {S₀ ∉ 𝓜_1}), so P(completed ∩ {Ŝ ≠ S₀}) ≤ P(δ ≥ ½) +
  E[1_𝒜 min(1, δ/η)] + P(𝒜 ∩ {W_1 < η}) → 0.
By Lemma PC the reported fields on {completed} equal the potential quantities, so the same limits hold for
P(completed ∩ {reported error}). Nothing depends on N_e, T, L, the grid or a rate for δ. ∎(LT-e)

(LT-e′, vanishing threshold.) NC_r may be replaced by: there are σ(data, 𝓒)-measurable η_n > 0 with
1_𝒜·o₁/η_n → 0 and P(𝒜 ∩ {W_r < η_n}) → 0. Then by (LT-b′), P(𝒜 ∩ {E_r > u}) ≤ E[1_𝒜 min(1, 21o₁/(uη_n))] +
P(𝒜 ∩ {W_r < η_n}) → 0 for every u > 0, and the PIP and pooled conclusions follow as above; for the MPM take u = ¼:
{MPM ≠ S₀} ⊆ {‖pip_primary − 1‖_∞ ≥ ½} ⊆ ∪_r{E_r > ¼} (MP1 issue 3, the tie at ½); for the HPM use
(LT-c) with η = η_n (δ ≤ o₁). This allows W_r → 0 provided the collapse is slower than the posterior error. ∎(LT-e′)

## Step 6 (LT-f: the status of NC_r)

- *Necessity is not settled* (LC1 issue 3). NC_r is a sequence-level property; at any fixed finite target
  W ≥ e^{min d − max d} > 0, so a single target can neither violate nor witness it. Two finite-n probes on artificial
  positive targets (not the regression target with its block start) only illustrate the two possibilities:
  "trap" (`numerics/RESULTS_v1_sec4b.txt`; δ = 0.0099, π₀(S₀) = 1.5e-8): W < 0.01 in all 3000 islands and the MPM wrong
  in all — collapsed evidence with wrong outputs; "near" (median W = 3.6e-4): RB error ≥ 0.1 in only 0.9% of islands at
  L = 20 — collapsed evidence with repaired outputs (local moves; Theorem TR is vacuous there, M = 1.3e6). Asymptotic
  witnesses (triangular arrays) are left open.
- *Discharged* by Theorem C (C-iii ⇒ P(𝒜 ∩ {W_r < ½}) → 0).
- *One-sided falsifier.* Under EX-A, Z = Σ_Ω e^{F} (CC2) ≥ Σ_{S ∈ 𝒯} e^{F(S)} for the ledger's top store 𝒯 (a set of
  distinct models, `cpp/v3_ledger.h:43-57`, offered only distinct models in Ω, CC5). Hence Ẑ_r < η·Σ_{𝒯}e^F ⇒ W_r < η.
  No output certifies W_r ≥ η (Z is not computed).
- LT♯ gives no statement about Ẑ/Z: a mean-one W can stay non-degenerate while bounded away from 0 (ADJ_astra §1(d)).

## Numerical falsification

`numerics/RESULTS_v1.txt` §2: empirical left sides of LT-a/LT-b never exceed the right sides (0 violations over 9 (ε, η)
pairs; the bounds are loose there because δ = 0.24). The κ₀ term cannot be removed: deterministically, a measured path that
stays at S₀ throughout records o_j(S₀) at every Gibbs-j step, so its RB error equals κ₀ exactly (ST-b). (The v1 numerical
"sharpness" filter omitted A_0 = 1 and is withdrawn, LC1 issue 6.)
