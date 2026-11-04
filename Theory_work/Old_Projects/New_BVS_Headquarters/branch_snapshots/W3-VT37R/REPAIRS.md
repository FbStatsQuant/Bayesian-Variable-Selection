# W3-VT37R: repairs of the gaps and errors found in W1-T37R

Notation as in W1 PROOF.md and 00_COMMON.md. M(S) is the greedy map, Φ(S) = |S Δ S₀|, m(S) and e(S) count missing truths
and extras, 𝒫/𝒩/ℛ are the progress/neutral/regressive neighbours, R⁺(S) and R⁰(S) are as in W1's PGD. Every repair is a
**candidate**, and its status is stated next to it.

---------------------------------------------------------------------------------------------------------------------

## R1. Theorem A(A5): positivity was missing. Status: PROVED (repair); COUNTEREXAMPLE to the original.

**What was wrong.** W1 A5 claims "literal TD(d,0) strict ⇒ TD′_P(R_d)". Literal TD(1) asks the best missing-truth addition to
beat every *other* move. It never asks the addition to be an *improvement* (gain > 0). So M(S) = ⊥ is possible at
S ≠ S₀. CEX-1 (`scripts/cex1_literalTD_d0_no_positivity.py`, `results/cex1.txt`) gives such a case: n = 100, a suppressor pair
x₂ = 0.95x₁ + √(1−0.95²)e₂, μ = 3x₁ − 2.8x₂, 10 orthogonal nulls, and noise orthogonal to every column.
- Literal TD(0,0) strict holds on R₀, with 0 failing clauses.
- S₀ is the global HPM by enumeration of all 2¹² models, with π(S₀) = 0.86.
- Yet every move at ∅ is non-improving: the best gain is −2.30 (add x₁). The production local search from ∅ ∈ R₀
  returns ∅, flagged `local_certified`.

So **the original T37(i) is false at d = 0 as well**, not only vacuous for d ≥ 1. A5's first claim is false.

**Repaired A5(a).** Let POS(R_d) be the following condition: at every S ∈ R_d∖{S₀}, the move designated by TD(1) or TD(2)
has gain > 0. Then TD(d,0) strict ∧ POS(R_d) ⇒ TD′_P(R_d).
*Proof.* Take S ≠ S₀ in R_d. TD(1) or TD(2) designates a move (add a missing truth, or delete an extra). Both are progress
moves (ΔΦ = −1). Its gain strictly exceeds every other feasible move's gain, so it is the unique maximiser of F over N(S),
and the tie rule plays no part. By POS its gain is > 0, so M(S) is that move. Hence M(S) ≠ ⊥ and Φ(M(S)) < Φ(S).
TD(3) strict gives (L). ∎
The other parts of A5 are unaffected: TD′_P ⇒ TD′_∞ (VERIFIED), and the converse fails (re-checked, see the report §4.3).
Theorem A(A1)–(A4) never used A5(a), and TD′_P contains "M(S) ≠ ⊥" explicitly, so the main theorem stands.

## R2. Lemma 0(b): "in particular on every posterior miss". Status: PROVED (repair); COUNTEREXAMPLE to the inference.

**What was wrong.** The inclusion {S₀ delivered} ⊆ E_LS = {F(S₀) > F(S_c)} is correct. A posterior miss, however, is measured
*after* the search, against the final HPM Ŝ. That does not put the fit in E_LS^c: if F(S_c) < F(S₀) ≤ F(S*) for a model S*
that the search climbs to, the fit is a posterior miss and E_LS held.
- CEX-2 (`scripts/cex2_lemma0b_posterior_miss_with_ELS.py`): S_c = S₀ − x₂ + x₃ with F(S_c) = F(S₀) − 2.29. The search goes
  S_c → S₀ + x₃, which is +7.21 above S₀, and stops there, certified. The fit is a posterior miss with E_LS true.
- The production-scale rerun (report §4.4) shows that this pattern is the common mode of non-repair at n = 200.

**Repaired statement.** (b′) The search can deliver S₀ only on E_LS. Every fit with Ŝ ≠ S₀ is in exactly one of two sets:
- E_LS^c: the miss is forced by monotonicity, and the search could not have helped;
- E_LS ∩ {search ends at S* ≠ S₀ with F(S*) ≥ F(S₀)}: this is a failure of the repair condition at the centre (TD′_path fails),
  and it happens only if S₀ is not the HPM of the explored region.

*Proof.* This is Lemma 0(a) and (c) together with the definition of Ŝ. ∎

**Consequence for the data remark.** "The 0/541 repair count is forced by monotonicity" is established only for those of the
541 fits with F(S₀) ≤ F(S_c), where S_c is the final local-search centre. The data fact needed is the per-fit F(S₀) − F(S_c)
at the final centre, or equivalently whether the final local search improved the HPM. It is a one-line extraction from the
ledger. Until it is extracted, the remark is a GAP and not a theorem about the data.

## R3. "What is weakest" (prose after Theorem A). Status: COUNTEREXAMPLE to the prose; A4 itself VERIFIED.

W1 claims that, among statements keeping the move count ≤ Φ, TD′_P is necessary and sufficient. A4 proves necessity only
for the statement "every greedy move decreases Φ". The weaker property PHI-REACH(R) says that every greedy path from every
S ∈ R ends at S₀ within Φ(S) moves. On the exhaustive designs (`scripts/phi_reach_vs_TDP.py`) it held **without TD′_P in 23
of 360 datasets**.
- Example: scenario 2, n = 40, c = 1, rep 7, S₀ = {2,6,13}, centre {5,6,12}, so Φ = 4.
- The path is {5,6,12} → {2,5,12} → {2,5,13} → {2,6,13}: 3 moves ≤ Φ.
- Its first move is a neutral truth→truth swap.

The −2 swaps buy back the neutral move. **Correct prose:** TD′_P is necessary and sufficient for "every greedy move from R
decreases Φ" (A4). For "reach S₀ within Φ moves", TD′_P is sufficient but not necessary.

The phrase "the cap needs ℓ ≥ a + d" should also read "ℓ ≥ a + d suffices". The exact requirement is ℓ ≥ τ(S_c), and
max(m, e) ≤ τ ≤ Φ.

## R4. Theorem C(C1), the NA_d part under LD: the containment is miscomputed. Status: PROOF SKETCH (repaired).

**What was wrong.** W1 writes that the events {Z²_{T,l} ≥ c_k} are contained in {max_l Z²_{S₀,l} ≥ c_{s₀}(1 − o(1/log p))}.
From W1's own perturbation inequality, which is VERIFIED:

  |Z_{T,l}| ≤ (1−ρ²)^{−1/2}(|Z_{S₀,l}| + ρ‖P_Ṽ ε‖/σ),  with ρ² = ρ²(l, P′ | S₀) ≤ κ_n and ‖P_Ṽε‖²/σ² ≤ 2d(1+ε)log p.

From this one only gets Z²_{S₀,l} ≥ c(1 − κ) − 2√(2dκ c log p) − O(κ log p). The relative loss is O(√κ), not o(1/log p).

**Repair.** Write c = c_k ≥ log(n+1) + 2 log((2p−k)/(k+1)), with log p ≤ A log n and c ≤ (1 + 2A + o(1)) log n. Then

  x² := c(1−κ) − 2√(2dκ c log p) − 2 log p ≥ log n · [1 − κ(1 + 2A) − 2√(2dκA(1 + 2A))] − O(1).

Hence p·P(|Z| ≥ x) ≲ n^{−(1/2)[1 − κ(1+2A) − 2√(2dκA(1+2A))]} → 0 whenever κ_n ≤ κ̄(A, d) for a small enough constant κ̄. So
**LD can be weakened** from κ_n log p → 0 to κ_n ≤ κ̄(A, d) for the non-exceptional nulls.
- The step "the union over P′ is absorbed" needs the same uniform χ² bound over ≤ p^d sets, and W1 has that.

**Exceptional nulls (W1's acknowledged gap).** As stated, LD(d) does not control an exceptional l given the far part of P′.
Replace LD(d) by:

LD*(d, B″, κ̄). Every null l has a data-independent neighbour list N(l) with |N(l)| ≤ B″. For every P′ ⊆ S₀ᶜ with |P′| ≤ d,
ρ²(l, P′∖N(l) | S₀ ∪ (P′∩N(l))) ≤ κ̄.

Then Z_{T,l} is controlled by Z_{S₀∪(P′∩N(l)), l}, through the same inequality with S₀ replaced by S₀ ∪ (P′∩N(l)). The
number of distinct controlling events is ≤ p·2^{B″}, and the bound above gives a total probability → 0. COH implies LD* with
B″ = 0 and any κ̄. Status: PROOF SKETCH. The chain of inequalities is checked; the uniform χ² bound and the O(1/n) ridge
term are routine but not written out.

## R5. Theorem C(C2): the noise-variance bound is false; repaired bound. Status: PROOF SKETCH (repaired); COUNTEREXAMPLE to the original inequality.

**What was wrong.** W1 bounds the standard deviation of the linear noise term 2μᵀ(P_{S′} − P_{S″})ε/v by
Cσ√(n(|Δ_{S′} − Δ_S| + |Δ_{S″} − Δ_S|)) ≤ Cσ√(nR⁺(S)). Both inequalities fail (`scripts/c2_noise_bound.py`).
- First inequality, general neighbour pair: take S = {x₁}, S′ = S + x₃, S″ = swap x₁→x₂, orthogonal design, θ = (1, 1, 0.1).
  Then ‖(P_{S′} − P_{S″})μ‖² = 2.01(n−1), while |ΔΔ′| + |ΔΔ″| = 0.01. The ratio is 201, and it is unbounded as θ₃ → 0.
- Second inequality: a regressive S″ (for example deleting a large truth) has |Δ_{S″} − Δ_S| ≫ R⁺(S). Example: θ = (3, 0.2),
  S = {x₁}, where R⁺ = 0.04 and |Δ_∅ − Δ_S| = 9. In 400 random designs the ratio ‖(P_π − P_B)μ‖²/R⁺ reached 1,896.
- With S′ = π(S) (the best progress move), the first inequality was empirically bounded (max ratio 5.2), but W1 does not prove
  that.

**Repaired bound (PROVED, elementary).** For any A, B with U = A ∪ B:

  ‖(P_A − P_B)μ‖² ≤ 2(n−1)[(Δ_A − Δ_U) + (Δ_B − Δ_U)].

*Proof.* (P_A − P_B)μ = (P_U − P_B)μ − (P_U − P_A)μ, so the claim follows from ‖a − b‖² ≤ 2‖a‖² + 2‖b‖². For A ⊆ U, P_U − P_A
is a projection, so ‖(P_U − P_A)μ‖² = ‖P_Uμ‖² − ‖P_Aμ‖² = (n−1)(Δ_A − Δ_U); the same holds for B. ∎
Empirically the ratio was ≤ 0.963 over 400 random designs.

**Repaired bound for C2 (PROVED given SE on S ∪ S₀, |M| = m(S) ≤ a).** Take A = π(S), B ∈ N(S). Then:
- Δ_A − Δ_U ≤ Δ_S, and Δ_B − Δ_U ≤ (Δ_B − Δ_S)₊ + Δ_S.
- Δ_S ≤ ‖X_Mθ*_M‖²/(n−1) ≤ λ_max(R_M)‖θ*_M‖² ≤ |M|‖θ*_M‖².
- By Lemma 3, R⁺(S) ≥ φ₀⁴‖θ*_M‖²/|M|.

Hence

  ‖(P_π − P_B)μ‖² ≤ 2(n−1)[2a²R⁺(S)/φ₀⁴ + (Δ_B − Δ_S)₊].

On the population side, Δ_B − Δ_π = (Δ_B − Δ_S) + R⁺(S). If Δ_B ≥ Δ_S this is ≥ R⁺ + (Δ_B − Δ_S)₊. If Δ_B < Δ_S it is
≥ R⁺ − R⁰ ≥ ηR⁺ under PGD(η). So the population gap of the score difference is
≥ (n/2v_max)[ηR⁺ + (Δ_B − Δ_S)₊] − O(log n + log p), using log v_b − log v_a ≥ (v_b − v_a)/v_b.

The linear noise has sd ≤ Cσ√(n[a²R⁺/φ₀⁴ + (Δ_B − Δ_S)₊]) (with C absorbing v_min⁻¹). The quadratic noise is O_P(log p)
uniformly over the ≤ (2s₀)^a p^{d+1}(K+1) comparisons. Since nR⁺ ≥ nφ₀⁴θ²_min ≥ M_nφ₀²σ*² log n with M_n → ∞ (BM-∞), the gap
beats the noise times √(log #comparisons) and the penalties, uniformly. The constants depend on (a, φ₀, η), which are fixed.

Status: PROOF SKETCH. The uniform linearisation of ν log(2b₀ + Q) around (n−1)v_T, including the ridge term, is still owed,
as W1 already said.

## R6. Headline of Theorem B: "2^{Φ(S_c)} states (no 2^{s₀})". Status: GAP (presentation); the theorem as written in PROOF.md is VERIFIED.

The lattice union |Lat(S_c)| = 2^{Φ(S_c)} is usable only for a data-independent centre. The production centre is the running
HPM, which is data-dependent. For it, (B1) correctly sums over Lat(𝒞) for a data-independent class 𝒞, and for 𝒞 = R_{a,d}
that is all of R_{a,d}, with |R_{a,d} ∩ {m ≥ 1}| = Σ_{i=1}^{a} C(s₀, i) Σ_{e≤d} C(p−s₀, e).
- 2^{s₀} is avoided **only if a is fixed and small**, i.e. if the delivered centre misses few truths. That is a T38 delivery
  fact, not something T37 provides.
- The headline should say "C(s₀, ≤a)·p^d states for centres missing ≤ a truths; 2^{Φ} for a fixed centre".
