# W7-SEP — PROOF.md: the separation theorem, what it separates, and what it does not

Run W7-SEP, branch `theory/W7-SEP`. Every result is a **candidate**: not reviewed, not adopted. Status words follow
`theory_campaign/PROTOCOL.md` and are never upgraded. Notation: `Docs/Theory/theorems/00_COMMON.md`, W1-EXP §4 (LH),
W3-PXN (LH-iid), W4-T38FULL `T38_PROOF.md` §3 (Lemma M, Lemma LS-score, Prop. LH-LAT).

Short labels for sources: [E] = W1-EXP, [PXN] = W3-PXN, [T38] = W4-T38FULL, [T37R] = W1-T37R, [VT37R] = W3-VT37R,
[WS] = O-WSTAB, [SH] = W4-SHARE, [BG] = O-BGIBBS, [FD] = F-DRAFT.

---

## §0 Setting

**Score, start, posterior.** F(S) = log ϖ(S) + log m(S) on Ω = {S : |S| ≤ K}, K = min(p, ⌊n/2⌋); π ∝ e^F; the
composite start π₀ ∝ ϖ ∏_b r_b(S ∩ C_b) on the v3 partition (00_COMMON §1). Budgets (00_COMMON): ℓ = ⌈log₂(n+p+1)⌉,
L = max(4, ⌈log₂(n+1)⌉), N₀ = max(2500, n, p), Q_f = 4N_e(T+L+5) with 4N_e(L+6) ≤ Q_f ≤ 4N_e(T_e+L+5).
Population residual Δ(T) := ‖(I − P_T)μ‖²/(n−1) (μ = Xθ*, columns centred and standardised).

**Families.**
- **LH** (exact Gram) = the family of [T38] Cor. b1-LH: X′X = (n−1)Σ_LH, p ≤ n−1, groups of size g with
  equicorrelation ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1), c ≥ 1 linked pairs (a_i, b_i, ψ_i) with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i}),
  fixed nonzero coefficients θ_{a_i} = β_i, θ_{b_i} = −ψ_iβ_i, v ≥ 0 visible hubs, g ≤ B_n < 2g eventually, s₀ = 2c + v
  fixed, p ≤ n^A. Masked set M = {b_1, …, b_c}, reference S° = S₀ ∖ M.
- **LH-iid** = [PXN] §0: rows iid N(0, Σ_LH), 9 ≤ g ≤ 16, n^a ≤ p ≤ n^A (p ≫ n allowed).
- **Cancellation depth** := c = |M|, the number of masked hubs (the task's "c"). It equals the masking exponent of T27:
  π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}.

**Inputs used (status as recorded by their runs).**

| Label | Statement | Source | Status |
|---|---|---|---|
| I1 | LH: 1 − π₀(S°) = O_P(2^B n^{−1/2}); S̃₀ = S° w.p. → 1 | [E] Thm 5(a); [T38] b1.7 | PROVED (VERIFIED W3-VEXP) |
| I2 | LH: Mstat := log π₀(S₀) + c log p + (c/2) log n = O_P(1) (both sides) | [E] Thm 5(b), Thms 3–4 | PROVED (VERIFIED W3-VEXP) |
| I3 | LH: 1 − π(S₀) = O_P(√(log n/n)) | [E] Thm 5(d) via locked T03 | PROVED (citation of PROVED-LOCKED) |
| I4 | LH: blocks = groups w.p. → 1, so each linked pair is split across two blocks | [E] Lemma 4.2 | PROVED (VERIFIED) |
| I5 | Lemma M (uniform score comparison under population margins) | [T38] §3.2 | PROVED (same-family VERIFIED, not cross-family) |
| I6 | λ_min(Σ_LH) ≥ (1 − max|ψ_i|)(1 − ρ₊) =: φ₀² | [E] Lemma 4.1(a); [T38] (M3) | PROVED |
| I7 | LH-iid: P1–P8 (partition, SE family, 1 − π₀(S°) = O_P(√(log n/n)), Mstat →_d limit, S̃₀ = S°, TD′ at S°, π(S₀) → 1) | [PXN] | PROVED by a single run, **unverified** |
| I8 | T38(b1-LH): with LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 | [T38] Cor. b1-LH | PROVED-UNDER the above (unreviewed) |
| I9 | BG1 + Prop. LH: original method (no LS0), pilot stage 1 scores S₀ on LH, every fixed c, if n/(T_e log(p√n)) → ∞ | [BG] | structure PROVED; score estimates PROOF SKETCH; unverified |
| I10 | WS7: ESS_∞ ≤ π₀(S₀)/π(S₀)²; KL ≥ π(S₀) log(1/π₀(S₀)) − log 2; reweighting cannot create the truth | [WS] §7 | PROVED (single run) |
| I11 | T32(i): score-evaluation ceiling O((n+p)(p+B) log² n) of the SMC branch | T32 | CONJECTURE (checked as a valid loose bound by W3-VT38E) |

EX-A (exact iid π₀ draws) is assumed throughout, as in every T38 route.

**Method classes compared.** All of them score the block tables (M §6.3) for free.
- 𝔐_iid(Q): score Q iid draws from π₀; report the best scored model.
- 𝔐_IS(Q): one-shot importance correction: from the same Q draws, estimate π-expectations by weights w = γ/γ₀
  (oracle-normalised w̄ = π/π₀, or self-normalised).
- 𝔐_LS(Q): 𝔐_iid(Q), plus the production local search (M §6.10) from each draw and from S̃₀ (LS0).
- v3: the method (with or without LS0).

---

## §1 The Separation Theorem (refined statement)

**Theorem SEP.** Let (X, y) follow LH (exact Gram) with c ≥ 1 fixed, or LH-iid (parts (A), (B) only, through I7).
Put Q*_n := p^c n^{c/2}.

**(A) Start sampling cannot discover the truth below Q\*.** For every deterministic budget sequence Q_n,

  P₀(S₀ is scored by 𝔐_iid(Q_n)) → 0 if Q_n/Q*_n → 0, and → 1 if Q_n/Q*_n → ∞.

In particular, if p ≍ n^a, a polynomial budget Q_n = n^α fails when α < c(a + ½) and succeeds when α > c(a + ½).
**PROVED** (LH exact Gram, from I2, I4; LH-iid from I7, which is unverified).

**(B) One-shot importance correction fails below Q\*.** On LH (or LH-iid):
- (B1) 1 + χ²(π‖π₀) ≥ π(S₀)²/π₀(S₀) = Q*_n e^{−Mstat}(1 + o_P(1)) → ∞, and
  KL(π‖π₀) ≥ (c log p + (c/2) log n)(1 − o_P(1)) − O_P(1).
- (B2) The unbiased one-shot estimator Î_Q := Q⁻¹ Σ_{i≤Q} w̄(X_i) 1{X_i = S₀} of π(S₀) (oracle normalisation) has
  relative variance Var(Î_Q | data)/π(S₀)² = (1/π₀(S₀) − 1)/Q = (Q*_n/Q)e^{−Mstat}(1 + o_P(1)).
- (B3) If Q_n/Q*_n → 0, then Î_Q = 0 and the self-normalised estimator Ĩ_Q = 0 with probability → 1, while π(S₀) → 1:
  the absolute error tends to 1 in probability, not only the variance to ∞.

**PROVED** (given I2, I3; LH-iid via I7).

**(C) Start + local search is NOT separated from v3 (negative part; replaces the task's (a) for search methods).**
On LH (exact Gram), w.p. → 1 the production local search scores *and certifies* S₀ from every centre C ⊆ R, where R is
the union of the non-null groups (Proposition GU, §4). Since S̃₀ = S° ⊆ R and π₀(2^R) ≥ π₀(S°) → 1:
- LS0 alone scores S₀ w.p. → 1 (this is also [T38] b1-LH);
- 𝔐_LS(1) — one iid π₀ draw plus the production local search — scores S₀ w.p. → 1, with at most
  (ℓ+1)(p + K(p−K)) = O(p² log n) score evaluations.

So the exception in the task's clause (a) ("unless the greedy basin of S₀ contains S̃₀") holds with probability → 1 on
the task's own family: **clause (a) with local search is false on LH (COUNTEREXAMPLE by proof)**. The exact criterion
for LS0 is Proposition BASIN (§4.1). **PROVED** (Prop. GU; candidate, uses I5, I6).

**(D) v3 succeeds (citation).** With LS0: I8. Without LS0: c = 1 by D2 ([T38] (b1′), NB step PROOF SKETCH); every
fixed c by I9 (PROOF SKETCH, unverified, condition n/(T_e log(p√n)) → ∞). Cost: I11 + LS0 term, polynomial.

**(E) Budget exponents.** With p ≍ n^a (0 < a < 1 on exact-Gram LH; a ≥ 1 allowed on LH-iid):

| Method | Score evaluations needed to score S₀ w.p. → 1 | Exponent of n | Status |
|---|---|---|---|
| 𝔐_iid, 𝔐_IS | ≍ Q* = p^c n^{c/2} (sharp, two-sided) | c(a + ½) | PROVED |
| 𝔐_LS(1) (draw + local search), LS0 | ≤ (ℓ+1)(p + K(p−K)) | ≤ 2a (+ log) | PROVED (Prop. GU) |
| v3 with LS0 (T38(b1-LH)) | ≤ T32 ceiling + LS0 term = O((n+p)(p+B) log² n + p² log² n) | ≤ a + max(1, a) (+ log) | PROVED-UNDER I11 (CONJECTURE) |

The iid exponent exceeds v3's ceiling exponent iff c(a+½) > a + max(1,a); for every a > 0 this holds **iff c ≥ 2**.
It exceeds the 𝔐_LS / LS0 exponent iff c(a+½) > 2a, i.e. always for c ≥ 2, and for c = 1 only when a < ½.
**No super-polynomial gap exists in R1:** c ≤ s₀ is fixed, so Q* is polynomial. A super-polynomial gap needs
c = c_n → ∞, which is outside the frozen setting (s₀ fixed) and outside every proved v3 route.

**What the theorem separates.** Sampling from the start (with or without reweighting) from *any* method that moves
off the start's draws by score-improving local steps. It does **not** separate the tempering bridge from a deterministic
search started at the start mode: on LH both succeed with polynomial cost of degree independent of c (§5).

---

## §2 Proof of (A)

Fix the data. Under EX-A the Q draws are iid π₀ given the data, so

  P(S₀ ∉ {X_1, …, X_Q} | data) = (1 − π₀(S₀))^Q.   (2.1)

Tables: S₀ is a table model only if S₀ ⊆ C_b for one block b. On the event 𝒢_n = {blocks = groups} (I4,
P(𝒢_n) → 1), a_1 and b_1 lie in different blocks, so S₀ is not a table model. Hence

  P(S₀ scored by 𝔐_iid(Q)) ≤ P(𝒢_nᶜ) + E[1 − (1 − π₀(S₀))^Q] ≤ P(𝒢_nᶜ) + E[min(1, Qπ₀(S₀))].   (2.2)

Write Qπ₀(S₀) = (Q/Q*) e^{Mstat_n}. By I2, Mstat_n = O_P(1).

*Upper side.* If Q/Q* → 0 then Qπ₀(S₀) → 0 in probability; min(1, ·) is bounded, so E[min(1, Qπ₀(S₀))] → 0 by
bounded convergence (convergence in probability of a uniformly bounded sequence implies convergence in L¹). With (2.2)
the probability tends to 0.

*Lower side.* If Q/Q* → ∞ then Qπ₀(S₀) → ∞ in probability, and by (2.1) and 1 − x ≤ e^{−x},
P(S₀ not drawn | data) ≤ exp(−Qπ₀(S₀)) → 0 in probability; again bounded convergence gives P(S₀ drawn) → 1.

*Polynomial budgets.* If c₁n^a ≤ p ≤ c₂n^a, then Q* ∈ [c₁^c, c₂^c]·n^{c(a+½)}, so for Q = n^α the ratio Q/Q* tends to
0 if α < c(a+½) and to ∞ if α > c(a+½). ∎

*Remarks.*
1. The statement is two-sided, so Q* is the exact threshold up to the tight factor e^{Mstat}; its limit law is
   Σ_{i≤c} log((s+i+1)/2) + Σ (L_i + Z_i)²σ²/(2v) on exact Gram ([E] Thm 3, PROOF SKETCH for the limit law only).
2. R-T20(i) (DROPPED.md) is the fixed-p special case: Q* = Θ(n^{c/2}) and a budget Q ≍ n·polylog n succeeds for c ≤ 2 and
   fails for c ≥ 3. With p growing the p^c factor makes c = 2 already fail against v3's own Q_f ≍ (n+p) log² n:
   Q_fπ₀(S₀) = O_P((n+p)log²n · p^{−2}n^{−1}) → 0 whenever p → ∞ ([T38] "Masking on LH").
3. The same proof applies to any scheme that only *reweights and resamples* iid π₀ draws (I10(c)).

## §3 Proof of (B)

(B1) For every S, 1 + χ²(π‖π₀) = Σ_S π(S)²/π₀(S) ≥ π(S₀)²/π₀(S₀). By I2 and I3, π(S₀)²/π₀(S₀) =
Q* e^{−Mstat}(1 − O_P(√(log n/n))) → ∞. The KL bound is I10(a) (data processing on {S₀, S₀ᶜ}):
KL ≥ π(S₀) log(1/π₀(S₀)) − log 2 = (1 − o_P(1))(c log p + (c/2) log n − Mstat) − log 2.

(B2) Given the data, the summands w̄(X_i)1{X_i = S₀} are iid with mean π₀(S₀)·π(S₀)/π₀(S₀) = π(S₀) and second moment
π₀(S₀)(π(S₀)/π₀(S₀))² = π(S₀)²/π₀(S₀). Hence Var(Î_Q | data) = Q⁻¹π(S₀)²(1/π₀(S₀) − 1); divide by π(S₀)².

(B3) On {S₀ ∉ {X_1..X_Q}}, every indicator vanishes, so Î_Q = 0 and the self-normalised
Ĩ_Q = Σ w(X_i)1{X_i=S₀}/Σ w(X_i) = 0 (the denominator is positive). By §2, this event has probability → 1 when
Q/Q* → 0, and |Î_Q − π(S₀)| = π(S₀) → 1 in probability by I3. ∎

*Remarks.*
1. (B) is the masked-regime counterpart of [FD] Theorem W, which shows χ² blow-up already in the *favourable* BO regime
   through the single-null layer, 1 + χ² ≥ p^{R²−ε}n^{−1/2}. In the masked regime the blow-up is forced by one atom.
2. The ESS of one-shot reweighting obeys ESS_∞ ≤ π₀(S₀)/π(S₀)² = e^{Mstat}/Q*·(1+o_P(1)) (I10(b)).
3. **PIP version (PROOF SKETCH).** For a single masked hub b_i the start inclusion is π₀(b_i ∈ S) = p^{−1}n^{−1/2}e^{O_P(1)}
   (one step of the T27 chain, [E] Thm 3, plus the mass of supersets of other states, which is smaller by I1); hence with
   Q = o(p√n) draws no draw contains b_i w.p. → 1 and both IS estimates of PIP_{b_i} are 0, while PIP_{b_i} ≥ π(S₀) → 1.
   The bookkeeping of the second term is not written.

---

## §4 Search from the start: Proposition GU and the basin criterion

### 4.1 The exact criterion (Proposition BASIN; PROVED, deterministic)

Fix the data and the tie rule. Let M(C) be the production best-move map (the best strict improvement among feasible
flips and swaps of C, or ⊥), and N̄(S₀) := {S₀} ∪ {feasible flip and swap neighbours of S₀}. The search from C visits
C₀ = C, C_{t+1} = M(C_t) while M(C_t) ≠ ⊥ and t < ℓ, and scans each visited centre (including the last one, M §6.10).
Define the **scoring basin**

  𝔅_ℓ := {C ∈ Ω : some visited centre C_t lies in N̄(S₀)}.

Then: (i) the search from C scores S₀ iff C ∈ 𝔅_ℓ (with the centre emitted); (ii) LS0 scores S₀ iff S̃₀ ∈ 𝔅_ℓ;
(iii) 𝔐_LS(Q) scores S₀ with probability, given the data, 1{S̃₀ ∈ 𝔅_ℓ} ∨ [1 − (1 − π₀(𝔅_ℓ))^Q].

*Proof.* (i) A scan from centre C_t scores exactly the feasible neighbours of C_t, and S₀ is among them iff
C_t ∈ N̄(S₀) ∖ {S₀}; if C_t = S₀ it is scored as the centre (emitted) or as a neighbour of C_{t−1}. The path is
deterministic given the data. (ii) is (i) at C = S̃₀. (iii) The draws are iid π₀ given the data. ∎

Sufficient conditions for C ∈ 𝔅_ℓ already in the campaign: lattice D_S events + ℓ ≥ Φ(C) − 1 ([T38] Lemma LS-score);
TD′_∞(𝓡) ∋ C, uncapped ([T37R] Thm A(A1)); TD′_P(R_{a,d}) ∋ C with ℓ ≥ a + d ([T37R] Thm A(A3)). Proposition GU below
gives a *structural* sufficient condition that covers all relevant centres at once.

### 4.2 Proposition GU (greedy universality on exact-Gram families with an isolated relevant set)

**Hypotheses.**
- (G) Gaussian errors, fixed design, σ² fixed; columns centred and standardised.
- (XG) Exact Gram: X′X = (n−1)Σ, so Δ(T) is the population residual variance.
- (REL) There is R ⊇ S₀ with |R| ≤ r (r fixed) and Σ_{R, Rᶜ} = 0.
- (SE) λ_min(Σ_R) ≥ φ₀² > 0.
- (BM) θ₀ := min_{j∈S₀}|θ*_j| > 0 and θ*′Σθ* ≤ M, both fixed.
- (R-lite) p ≤ n^A, and p ≥ r + 1 (at least one variable outside R; if p = r the proof is the same with K ≥ r).

**Proposition GU.** Under these hypotheses there is an event U_n with P₀(U_n) → 1 on which, for all n ≥ n₁ with
ℓ_n ≥ τ_GU and K ≥ r + 1, the production local search started at **any** C ⊆ R reaches S₀ by strictly improving moves,
scores it, and stops there with `local_certified`, after at most

  τ_GU := 1 + ⌈(2s₀/φ₀²) log(M/(φ₀²θ₀²))⌉ + (r − s₀)

moves. Since ℓ_n = ⌈log₂(n+p+1)⌉ → ∞ and K = min(p, ⌊n/2⌋), the side conditions hold for all large n.
**Status: PROVED** (candidate; uses I5).

**Lemma GU-1 (population descent).** Under (SE) and (BM), for every T ⊆ R with Δ(T) > 0, writing M_T := S₀ ∖ T:
(a) Δ(T) ≥ φ₀²‖θ*_{M_T}‖₂² ≥ φ₀²θ₀², and Δ(T) = 0 iff T ⊇ S₀;
(b) red*(T) := max_{j∈M_T}[Δ(T) − Δ(T + j)] ≥ Δ(T)²/‖θ*_{M_T}‖₁² ≥ (φ₀²/s₀)Δ(T) ≥ φ₀⁴θ₀²/s₀.
Moreover for every T ⊆ [p], Δ(T) = Δ(T ∩ R).

*Proof.* By (XG), all inner products below are (n−1) times population ones; work in population units. Let
μ̃ := (I − P_T)μ = Σ_{j∈M_T} θ_j x̃_j with x̃_j := (I − P_T)x_j (components of S₀ inside T are annihilated).
(a) Δ(T) = θ_{M_T}′ S θ_{M_T}, where S is the Schur complement of Σ_{T} in Σ_{T∪M_T}; its smallest eigenvalue is
≥ λ_min(Σ_{T∪M_T}) ≥ λ_min(Σ_R) ≥ φ₀² (interlacing; T ∪ M_T ⊆ R). If T ⊇ S₀ then μ ∈ span X_T and Δ = 0; otherwise
M_T ≠ ∅ and the bound is positive.
(b) ‖μ̃‖² = ⟨μ̃, Σ_j θ_j x̃_j⟩ = Σ_j θ_j⟨x̃_j, μ̃⟩ ≤ ‖θ_{M_T}‖₁ max_j|⟨x̃_j, μ̃⟩|. Adding j reduces Δ by
⟨x̃_j, μ̃⟩²/‖x̃_j‖² ≥ ⟨x̃_j, μ̃⟩² because ‖x̃_j‖² ≤ ‖x_j‖² = 1. So red*(T) ≥ Δ(T)²/‖θ_{M_T}‖₁². By (a) and
Cauchy–Schwarz (‖θ‖₁² ≤ |M_T|‖θ‖₂² ≤ s₀‖θ‖₂²), Δ(T)/‖θ_{M_T}‖₁² ≥ φ₀²/s₀.
Last claim: by (REL) and (XG), the columns of X_{T∖R} are orthogonal to those of X_R and to μ ∈ span X_{S₀}; so
P_T = P_{T∩R} + P_{T∖R} and P_{T∖R}μ = 0. ∎

(Lemma GU-1(b) is a sharpened form of [SH] Prop. M(a) and of [T37R] Lemma 3.)

**Lemma GU-2 (one addition at a superset).** Let 𝔉 := {S₀ ∪ E : E ⊆ R ∖ S₀}. Define for T ∈ 𝔉 and l ∉ T
W_{T,l} := ⟨r_l, ε⟩²/(σ²‖r_l‖²), r_l := (I − P_T)x_l. Then W_{T,l} ~ χ²₁ for each fixed (T, l), and on Lemma M's event
E_n (I5) with k = r + 1, for n ≥ n₀,

  F(T + l) − F(T) ≤ −½ log(n − 1) + log(1/φ₀) + log((r+1)/p) + ½ W_{T,l}(1 + η_n) + c₀,   (4.1)

with η_n = O(n^{−1/3}) and c₀ = c₀(M, σ², φ₀) of Lemma M.

*Proof.* Three factors, with t = |T| ≤ r.
1. *Prior.* w(t+1)/w(t) = (t+1)/(2p−1−t) ≤ (r+1)/(2p−1−r) ≤ (r+1)/p for p ≥ r + 1.
2. *Determinant.* D_S = det((n+1)G_S + I)/det(G_S + I) (00_COMMON; G_S = X_S′X_S). By Schur complements,
   D_{T+l}/D_T = [(n+1)G_ll + 1 − (n+1)²G_{lT}((n+1)G_T + I)⁻¹G_{Tl}] / [G_ll + 1 − G_{lT}(G_T + I)⁻¹G_{Tl}].
   Since (n+1)((n+1)G_T + I)⁻¹ ≼ G_T⁻¹, the numerator is ≥ (n+1)‖r_l‖² + 1, and the denominator is ≤ G_ll + 1 = n.
   ‖r_l‖² ≥ (n−1)λ_min(Σ_{T+l}) ≥ (n−1)φ₀² (T + l ⊆ R, or l ∉ R and orthogonal to X_T with ‖x_l‖² = n−1).
   So D_{T+l}/D_T ≥ (n+1)(n−1)φ₀²/n ≥ (n−1)φ₀², and −½ log(D_{T+l}/D_T) ≤ −½ log(n−1) + log(1/φ₀).
3. *Fit.* Write Q̄_S := 2b₀ + Q_S. By Lemma M step 2, RSS^y_S ≤ Q̄_S ≤ RSS^y_S + c_φ with c_φ = 1.02 + 1/(nφ₀²) under
   λ_min(R_S) ≥ φ₀². Since T ⊇ S₀, (I − P_T)y_c = (I − P_T)e and RSS_T − RSS_{T+l} = ⟨r_l, e⟩²/‖r_l‖² = σ²W_{T,l}
   (r_l is centred, so ⟨r_l, e⟩ = ⟨r_l, ε⟩). Then
   −ν log(Q̄_{T+l}/Q̄_T) ≤ ν log((RSS^y_T + c_φ)/RSS^y_{T+l}) ≤ ν(σ²W_{T,l} + c_φ s_y²)/RSS_{T+l}.
   On E_n, RSS_{T+l} ≥ σ²(n−1)(1 − n^{−1/3}) − Lσ² log n and s_y² ≤ 2C_R (Lemma M step 4), so with ν = n/2 + 0.01 the
   right side is ≤ ½W_{T,l}(1 + η_n) + c₀.
Summing the three bounds gives (4.1). W_{T,l} ~ χ²₁ because ε ~ N(0, σ²I) and r_l is fixed. ∎

**Proof of Proposition GU.** Let k := r + 1, m_n := √(log n/n)·log n (so m_n ≥ M_n√(log n/n) with M_n = log n → ∞,
and m_n → 0). Let U_n := E_n ∩ V_n, where E_n is Lemma M's event for (k, φ₀, m_n) and

  V_n := {max_{T∈𝔉, l∉T} W_{T,l} ≤ 2 log(2^r p) + ¼ log n}.

*P(V_n) → 1:* there are ≤ 2^r p pairs, and P(χ²₁ > 2x) ≤ e^{−x}, so P(V_nᶜ) ≤ 2^r p · e^{−log(2^r p) − (1/8)log n} = n^{−1/8}.

Fix n ≥ n₁ (all thresholds below) and a centre C ⊆ R. Work on U_n.

*Phase 1 (Δ > 0).* Let S ⊆ R be the current centre with Δ(S) > 0, |S| ≤ r. Choose j* attaining red*(S) and put
A := S + j* ⊆ R (feasible since |S| < r + 1 ≤ K). λ_min(R_A) = λ_min(Σ_A) ≥ φ₀² and |A ∪ S₀| ≤ r ≤ k.
Every feasible neighbour B of S, and B = S, has |B| ≤ r + 1 = k. By Lemma M, F(A) > F(B) for every such B with
Δ(B) ≥ Δ(A) + m_n. Consequences:
- B = S: Δ(S) − Δ(A) = red*(S) ≥ φ₀⁴θ₀²/s₀ ≥ m_n for n ≥ n₁. So F(A) > F(S): a strict improvement exists, and the
  search moves (if fewer than ℓ moves have been made).
- The chosen neighbour T* has F(T*) ≥ F(A), hence Δ(T*) < Δ(A) + m_n = Δ(S) − red*(S) + m_n ≤ Δ(S) − red*(S)/2
  (for n ≥ n₁, m_n ≤ φ₀⁴θ₀²/(2s₀)).
- T* ⊆ R: any neighbour that contains a variable outside R is S + l or S − i + l with l ∉ R; by GU-1,
  Δ(S + l) = Δ(S) and Δ(S − i + l) = Δ(S − i) ≥ Δ(S), so Δ(B) − Δ(A) ≥ red*(S) ≥ m_n and F(B) < F(A).
By GU-1(b), Δ(T*) ≤ (1 − φ₀²/(2s₀))Δ(S). Starting from Δ(C) ≤ Δ(∅) = θ*′Σθ* ≤ M and using GU-1(a)
(Δ > 0 ⇒ Δ ≥ φ₀²θ₀²), phase 1 lasts at most 1 + ⌈(2s₀/φ₀²)log(M/(φ₀²θ₀²))⌉ moves and ends at a centre
S ⊆ R with Δ(S) = 0, i.e. S ∈ 𝔉 (GU-1(a)).

*Phase 2 (supersets).* Let T = S₀ ∪ E ∈ 𝔉. On V_n, (4.1) gives for every l ∉ T:
F(T + l) − F(T) ≤ −½ log(n−1) + log(1/φ₀) + log(r+1) − log p + (log p + r log 2 + ⅛ log n)(1 + η_n) + c₀
≤ −¼ log n for n ≥ n₁ (η_n log p ≤ A η_n log n → 0). Call this (★). Then:
- additions from T lower F by ≥ ¼ log n: not improving;
- deleting an extra e ∈ E: T − e ∈ 𝔉 and T = (T − e) + e, so by (★) F(T − e) − F(T) ≥ ¼ log n > 0;
- swapping an extra e for l ∉ T: F(T − e + l) − F(T − e) ≤ −¼ log n by (★) at the base T − e ∈ 𝔉, so the swap is
  strictly worse than deleting e;
- any move that removes a truth leads to B ⊉ S₀ with |B| ≤ k; by GU-1(a) (and Δ(B) = Δ(B ∩ R)),
  Δ(B) ≥ φ₀²θ₀² ≥ m_n = Δ(T) + m_n; Lemma M with A = T (λ_min(Σ_T) ≥ φ₀², T ⊆ R) gives F(B) < F(T).
Hence at T ≠ S₀ the best move is the deletion of an extra, which keeps the centre in 𝔉 and lowers |E| by one; at
T = S₀ there is no improving neighbour. Phase 2 lasts |E| ≤ r − s₀ moves and ends at S₀, which is a scanned
neighbour of the previous centre (or the centre itself), with `local_certified` if the total number of moves is ≤ ℓ.
The total is ≤ τ_GU. ∎

**Corollary GU-LH.** On LH (exact Gram) the hypotheses hold with R = the union of the 2c + v non-null groups
(r = (2c+v)g), φ₀² = (1 − max|ψ_i|)(1 − ρ₊) (I6), θ₀ = min(|β_i|, |ψ_iβ_i|, |θ_h|), M = θ*′Σθ*. Hence w.p. → 1:
(i) every C ⊆ R lies in 𝔅_ℓ (and the search certifies S₀ from it);
(ii) LS0 scores S₀ (S̃₀ = S° ⊆ R by I1), consistent with [T38] Prop. LH-LAT, which shows the path from S° takes c moves;
(iii) P₀(𝔐_LS(1) scores S₀) ≥ E[π₀(2^R)] − P(U_nᶜ) − o(1) ≥ E[π₀(S°)] − o(1) → 1.
*Proof.* Σ_LH is block-diagonal over units (pair unions, visible groups, null groups) ([T38] §3.4 "Units"), so
Σ_{R,Rᶜ} = 0. The rest is Prop. GU and I1. ∎ **PROVED** (candidate).

*Remarks.*
1. **No PGD needed.** Prop. GU does not assume that greedy moves are progress moves (PGD fails under SE + BM-∞,
   [T37R] C3). It uses only the population descent of Δ (GU-1), which holds for every T ⊆ R under SE. Greedy may take
   look-alikes first; it never gets trapped, because every state with Δ > 0 has a Θ(1) Δ-reduction available and every
   superset with an extra has a Θ(log n) deletion gain. This proves a version of [T37R] Conjecture C4 in the
   exact-Gram, isolated-relevant-set case: TD′_∞ on all of 2^R (C4's region also allows null extras; not covered).
2. **Where the isolation (REL) is used.** Only to keep nulls out of the path (phase 1) and to make phase 2 a union over a
   fixed finite family 𝔉. For LH-iid (random design, p ≫ n) nulls have sample correlations O(√(log p/n)) with R and μ,
   so Δ(S + l) − Δ(S) = O(log p/n) ≪ φ₀⁴θ₀²/s₀ and the same two phases go through with an extra union bound over
   the nulls' sample correlations. **PROOF SKETCH** (not written line by line).
3. **Centres with nulls.** For a centre containing data-chosen nulls, phase 2 needs the deletion gain of each such null
   uniformly over data-chosen sets, which is the NA/LD issue of [T37R] C1. Not covered (OPEN).

---

## §5 What the bridge buys: the honest reading

1. **Separated (PROVED):** sampling-only start methods (𝔐_iid, 𝔐_IS) versus any method that scores S₀ at polynomial cost
   of degree independent of c. The gap in exponents is c(a+½) versus ≤ a + max(1, a) (v3, conditional on T32) or ≤ 2a
   (LS0 alone), and it is a genuine gap for c ≥ 2. This is what "the start is masked" buys the story: start draws, and any
   reweighting of them, cannot find or weight the truth below Q* = p^c n^{c/2}.
2. **Not separated (PROVED on LH, exact Gram):** v3 versus a deterministic search from the start mode. Proposition GU shows
   that on exact-Gram families with an isolated relevant set there is **no posterior-level barrier** between 2^R (which
   carries start mass → 1 on LH) and S₀ (this extends
   [SH] Prop. M from 𝓡_d paths to all of 2^R). Any score-improving local scheme that starts on the start's support finds
   S₀. On LH, LS0 — which is itself a start-only method — is the only fully proved masked-regime route of T38.
3. **Consequence for the paper's spine.** "The sampler is needed in the masked regime" is supported in the form
   "*moving off the start is needed*": the start must be followed by score-driven moves. The data say the same: at n = 200
   about 98% of fresh scores come from Gibbs flips (THEORY_PRIORITIES §5), and Gibbs at any φ ≥ φ_n → 0 is downhill
   toward S₀ inside 𝓡_d ([SH] Prop. M(b)). The *tempering* itself is not shown to be needed for discovery by any
   campaign result, and Proposition GU shows it cannot be on exact-Gram families with an isolated relevant set: there,
   one greedy search from S̃₀ already suffices.
4. **Where a bridge-versus-search separation could live (all outside the frozen setting).**
   - A posterior barrier: S₀ separated from the start's support by states with Δ-level gaps of the wrong sign. Under SE
     and fixed signals this cannot happen (GU-1). [SH]'s design PB (λ_min(R_{S₀}) = 0.004) has one at finite n; LS0 fails
     there, but the bridge also scores S₀ only through a rare gate (82% of islands at n = 4000, 51% at n = 16000), so PB
     is not an asymptotic separation either.
   - Move-limit binding: Φ(S̃₀) > ℓ_n + 1 (the study's S4/S6 at n = 200, [PXN] §5). This is an artefact of the cap ℓ;
     running LS0 to certification removes it.
   - Growing depth c_n → ∞ or weak signals (θ₀ → 0 at rate ≲ (log n/n)^{1/4}, where Lemma M's margin and GU-1 collide).
     Neither has a proved v3 route.
5. **What remains specifically for the bridge.** Calibrated weights for Ẑ and PIPs, which a single search does not
   provide. But on LH π(S₀) → 1, so after S₀ is scored the PIPs are trivially 1{j ∈ S₀} up to o_P(1); a separation for
   evidence/PIP accuracy would need a family where π does **not** concentrate, which T38 explicitly does not claim
   (masked-regime evidence/PIP accuracy is "not claimed").
