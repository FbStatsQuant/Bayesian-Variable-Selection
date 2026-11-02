# F-SHARE — PROOF.md: delivery in the masked regime through a closed near-truth class

Notation of `Docs/Theory/theorems/00_COMMON.md`, W1-T38E `PROOF.md` (Lemma A), W4-SHARE `PROOF.md` (D4, D5, X, M, PD) and W1-EXP §4 / W3-PXN §0 (the LH family). Every result is a **candidate**: not reviewed, not adopted. Status words: PROVED / PROOF SKETCH / COUNTEREXAMPLE / CONJECTURE / OPEN, never upgraded.

## 0. Setting, and the one idea

One final-run island given a successful calibration 𝓒 (grid 0 = φ₀ < … < φ_T = 1, T ≤ T_e, N = N_e particles), EX-A, EX-S, CAL, SR. Stage t: reweight the end-of-stage-(t−1) population by G_t = e^{Δ_t d}, multinomial resampling, one round K_{φ_t}. After the stage-T resampling come H′ = L + 5 rounds at φ = 1 (the stage-T round, L burn-in, 4 measured); no reweighting or resampling in between. Total number of rounds: T + L + 4. 𝔉_T is the σ-field at the terminal boundary (after the stage-T resampling, before the stage-T round), as in W6-FIXREV1.

A reference S° ∈ Ω is fixed (data-measurable; in the masked regime S° = S₀ ∖ M, M the masked truths). The **superset class** of S° is

  W(S°) := {x ∈ Ω : S° ⊆ x}.

It contains the whole near-truth lattice above S° (every S° ∪ A, A ⊆ M, in particular S₀) together with every state carrying extras, however many. Its complement is the set of states that **miss a member of S°**.

**The idea.** W1-T38E's C1 kills the near-truth particles by letting an outsider class, posterior-better than the occupied near-truth states (Lemma PD), outgrow them before the within-class move becomes available. Such an outsider must be *reached*: either drawn at the start or entered by a move. If every one-round exit from W(S°) requires deleting a member of S°, and deleting a member of S° is unfavourable **at both endpoints** (start table and posterior), then no particle ever leaves W(S°), with probability 1 − N(T + L + 5)e^{−cn}. There is then nothing to deliver: every particle is near the truth at every time, and route (b2) reduces to repair on W(S°). This is Theorem F1. The masked regime is exactly the regime in which S° ≠ S₀ carries the start mass, so W(S°) ≠ W(S₀); the masked hubs are *added inside* W(S°) during the bridge, once φ exceeds the crossing temperature φ_hub → 0 of Proposition M (W4-SHARE) and O-BGIBBS. On the linked-hub family the two-endpoint keep margins are Θ(n), uniformly over all supersets (Theorem F2). C1-type extinction is therefore impossible there (Corollary F3). Extras (null additions) are the only remaining bookkeeping, and they are handled at the terminal rounds, not during the bridge (§4).

---

## 1. Theorem F1 (closed-class delivery) — PROVED

**Hypothesis KEEP(W, η).** W ⊆ Ω is 𝓒-measurable and, for every x ∈ W and every φ ∈ {φ₁, …, φ_T, 1},

  K_φ(x, Ω ∖ W) ≤ η,

where K_φ is the one-round kernel (random order averaged out).

**Statement.** Under EX-A, EX-S, CAL and KEEP(W, η), for one island,

  P(some particle lies outside W after some initial draw, resampling or round | 𝓒) ≤ N π₀(Ω ∖ W) + N (T + L + 4) η.

Consequently, on the complement of that event, n_t(W) = N for every t ≤ T, every particle at 𝔉_T is in W (DELIV(W) in the sense of W6-FIXREV1 route (b2), with the whole population eligible), and every particle stays in W through the L + 5 terminal rounds. For the 4 islands the bound is multiplied by 4.

**Proof.** Resampling copies existing states, so a particle can be outside W at some time only if (i) one of the N initial draws is outside W, or (ii) at some round a particle starts in W and ends outside W. The expected number of initial draws outside W is Nπ₀(Ω ∖ W). In each of the T + L + 4 rounds at most N particles start in W; given the past, each ends outside W with conditional probability ≤ η by KEEP (fresh uniforms and orders, EX-S). A union bound over the first such event gives the display. ∎

This is Proposition X of W4-SHARE with U = Ω ∖ W. It is stated separately because its reading is new: **a near-truth class that is closed under the kernel needs no delivery theorem.** In D4's terms, h_t = 1_W, η_t = η, and the envelope P_t ≡ ∏(1 − η_s) is deterministic (r_t = 1 whenever every particle is in W, since then Ḡ^h_t = Ḡ_t), so the random hypothesis of D4 is vacuous.

**Remark 1.1 (which exits matter for the superset class).** For W = W(S°) a round leaves W only when a step removes a member of S°: a Gibbs label j ∈ S° that deletes j; a uniform swap or a neighbour swap that deletes j ∈ S°; or an accepted independence proposal y ⊉ S°. Additions never leave W. So KEEP(W(S°), η) follows from the four bounds of Lemma 1.2.

**Lemma 1.2 (exit bound for the superset class) — PROVED.** For x ∈ W(S°) and φ ∈ [0, 1],

  K_φ(x, Ω ∖ W(S°)) ≤ Σ_{j∈S°} max{κ₀(x, j), κ₁(x, j)} + Σ_{j∈S°} max{ρ₀(x, j), ρ₁(x, j)} + π₀(Ω ∖ W(S°)),

where κ_e(x, j) := γ_e(x − j)/γ_e(x) (e = 0 start, e = 1 posterior) are the endpoint deletion odds and ρ_e(x, j) := max_{l ∉ x} γ_e(x − j + l)/γ_e(x) the endpoint swap-out odds.

*Proof.* Condition on the random order. At the Gibbs label j ∈ S°, executed at a state y ∈ W(S°) (the state at that time; if the round has already left W we are done), the deletion probability is κ_φ(y, j)/(1 + κ_φ(y, j)) ≤ κ_φ(y, j) = κ₀(y, j)^{1−φ}κ₁(y, j)^{φ} ≤ max{κ₀, κ₁}(y, j) (Lemma A of W1-T38E, log-linearity). A uniform swap deleting j ∈ S° and adding l is accepted with probability ≤ γ_φ(y − j + l)/γ_φ(y) ≤ ρ₀(y, j)^{1−φ}ρ₁(y, j)^{φ} ≤ max{ρ₀, ρ₁}(y, j), and the same bound holds for a neighbour swap because its Hastings factor |N(j) ∖ y|/|N(l) ∖ y′| ≤ B does not matter once we bound by the *maximum over l* in ρ_e and absorb the factor into the definition (replace ρ_e by B·ρ_e for the neighbour swaps; to keep the display clean we assume ρ_e already includes it). The independence proposal moves to y ∉ W(S°) only if the exact π₀ draw is outside W(S°), probability π₀(Ω ∖ W(S°)). Summing the first-exit probabilities over the (at most) s + B + 2 labels that can cause an exit and taking the supremum over the states y ∈ W(S°) visited gives the claim, with the suprema over y ∈ W(S°) understood in each term. ∎

So KEEP(W(S°), η) holds with

  η := sup_{x∈W(S°)} [Σ_{j∈S°} max{κ₀, κ₁}(x, j) + (B+1)·Σ_{j∈S°} max{ρ₀, ρ₁}(x, j)] + π₀(Ω ∖ W(S°)).   (1.1)

These are **two-endpoint, single-state quantities**: the start-side ones are block-table ratios (finitely many per block, computable), the posterior ones are score differences at supersets of S°. No particle-system quantity enters.

---

## 2. Corollary F3 (no C1 on a closed class) — PROVED

Lemma PD (W4-SHARE §6b): log π₀(y) + d(y) = F(y) − log m(∅), so an outsider y can out-select an occupied state x over the whole bridge only if F(y) > F(x) + ω (its start deficit must be paid back by its fitness advantage). In C1 the outsider is posterior-better than the occupied near-truth states and *isolated* from them.

**Statement.** Under KEEP(W, η) with Nπ₀(Ω ∖ W) + N(T + L + 4)η → 0, no outsider class can take over: with probability → 1 the population has no outsider at any time, so the W-count equals N at every stage and the realised envelope of D4 for h = 1_W is P_t = ∏_{s≤t}(1 − η_s) ≥ (1 − η)^T → 1 (when Tη → 0). In particular the branching mechanism of C1 (W4-SHARE §5), which needs an initial outsider copy and a per-stage mean offspring e^{Δ_tκ} > 1, cannot start.

*Proof.* Immediate from Theorem F1: the event that some particle is ever outside W has probability → 0, and on its complement H_{t−1} = N for every t, hence r_t = 1 and P_t = ∏(1 − η_s). ∎

**Reading.** C1 is a counterexample to "start mass + bridge mass + zero exits ⇒ delivery" because its class A has start mass but is not *closed under the move kernel at the fitness level*: the outsider o is never entered from A (zero exits) but is *drawn* (Nπ₀(o) ≥ 1) and is fitter. The closed-class condition is the two-sided one: no initial outsider (Nπ₀(Ω ∖ W) → 0) **and** no exit (N(T+L+4)η → 0). The second part is what C1 keeps and the first is what it breaks: in C1, π₀(o) = 4.5·10⁻⁵ and N = 10⁵–10⁶. Under KEEP both fail for every outsider. The condition is sharp in the sense of Proposition SH: with Nπ₀(o) of order 1 and κ ≥ 2 log N + ω(1), extinction has probability → 1 (W4-SHARE §3).

---

## 3. Theorem F2 (the linked-hub family: the superset class is closed) — structure PROVED, Gaussian estimates PROOF SKETCH

### 3.1 The family and its unit structure

LH exact Gram (W1-EXP §4.1–4.2; W3-PXN §0 for the parameters): p columns in independent equicorrelated groups of size g (within-group correlation ρ ∈ (0,1)), c ≥ 1 linked pairs (a_i, b_i) of hubs in different groups with corr(a_i, b_i) = ψ_i, corr(k, b_i) = ψ_iρ for k ∈ C_{a_i}∖{a_i}, corr(k′, a_i) = ψ_iρ for k′ ∈ C_{b_i}∖{b_i}, corr(k, k′) = ψ_iρ², 0 < |ψ_i| < ρ; v ≥ 0 visible hubs j_h in further groups; the remaining groups null. Coefficients θ_{a_i} = β_i ≠ 0, θ_{b_i} = −ψ_iβ_i, θ_{j_h} = β_h ≠ 0, all fixed; σ*² fixed. X′X = (n − 1)Σ_LH exactly, with p ≤ (1 − c₀)n for a fixed c₀ ∈ (0, 1) (W1-EXP needs p ≤ n − 1; the stronger margin is used in Lemma 3.4). Blocks = groups (g ≤ B < 2g, Lemma 4.2 of W1-EXP). S₀ = {a_i, b_i, j_h}, M = {b_i}, S° = S₀ ∖ M, s = |S°| = c + v.

A **unit** is C_{a_i} ∪ C_{b_i} (a linked pair) or C_{j_h} (a visible group) or a null group. Units are mutually independent (block-diagonal Σ_LH across units), and this is exact in the Gram. Write λ₀ := λ_min(Σ_LH) > 0 (for ρ = 0.7, ψ = 0.5, g = 4: λ₀ = 0.2418, `scripts/lh_design.py`).

**Lemma 3.1 (what a residual sees) — PROVED.** For x ⊆ [p] and a column j ∉ x, let u_{x,j} be the unit residual of x_j on col(X_x). Then u_{x,j} depends on x only through x ∩ unit(j), and for any column l in a different unit, u_{x,j}ᵀx_l = 0.

*Proof.* In the exact Gram, col(X_x) = ⊕_{units U} col(X_{x∩U}) orthogonally, because columns of different units are exactly orthogonal. The projection of x_j onto this orthogonal sum is its projection onto col(X_{x∩unit(j)}), the other summands being orthogonal to x_j. So the residual depends on x ∩ unit(j) only, lies in the span of unit(j), and is orthogonal to every column of another unit. ∎

**Lemma 3.2 (signal seen by a hub) — PROVED.** Let x ∈ W(S°) and b = b_i ∉ x. Then

  δ_{x,b} := u_{x,b}ᵀμ = θ_b ‖(I − P_x)x_b‖,  and  δ_{x,b}² ≥ θ_b²(n − 1)λ₀.

Let x ∈ W(S°) and j ∈ S°. Then with x′ := x − j,

  δ_{x′,j} := u_{x′,j}ᵀμ = θ_j‖(I − P_{x′})x_j‖ + θ_{b(j)}u_{x′,j}ᵀx_{b(j)}·1{j = a_i, b_i ∉ x},

where b(j) = b_i is j's partner (second term absent for visible hubs).

*Proof.* μ = Σ_{h∈S₀}θ_hx_h. For x ⊇ S° the only members of S₀ outside x are masked hubs. (I − P_x)μ = Σ_{b′∉x}θ_{b′}(I − P_x)x_{b′}, and u_{x,b}ᵀ(I − P_x)x_{b′} = u_{x,b}ᵀx_{b′} = 0 for b′ ≠ b (different units, Lemma 3.1), while u_{x,b}ᵀx_b = ‖(I − P_x)x_b‖. The lower bound: ‖(I − P_x)x_b‖² = (n − 1)·Var_Σ(x_b | x_x) ≥ (n − 1)λ_min(Σ_LH). For j ∈ S°: (I − P_{x′})μ = θ_j(I − P_{x′})x_j + Σ_{b′∉x}θ_{b′}(I − P_{x′})x_{b′}; only b′ = b(j) is in j's unit. ∎

**Population condition PK(d*) (proxy keep).** For every linked pair and every x ∈ W(S°) with at most d* members of unit(a_i) outside S₀ (proxies of a_i or of b_i present), and for every visible hub likewise:

  (PK-a) 1 − ψ_i·β_{b_i∼a_i | x−a_i} ≥ c_K > 0, where β_{b∼a|x−a} := Cov_Σ(x_b, x_a | x_{x−a})/Var_Σ(x_a | x_{x−a}) (the population regression coefficient of b on a given the rest of x);
  (PK-s) for every l ∉ x in unit(j): Var_Σ-residual signal of the swapped model x − j + l stays below that of x by a fixed fraction: ‖(I − P_{x−j+l})μ‖² − ‖(I − P_x)μ‖² ≥ c_K θ_j²(n − 1).

PK(d*) is a finite set of population inequalities (≤ 2^{2g} per pair), decidable from (ρ, ψ_i, g) and d*. For single proxies one computes β = ψ (an a-proxy present) and β = ψ(1 − ρ²)/(1 − ψ²ρ²) ≤ ψ (a b-proxy present), so (PK-a) holds with c_K = 1 − ψ²; (PK-s) with one a-proxy k present gives ‖(I−P_{x−a+k})μ‖² ≥ θ_a²(n−1)(1−ψ²)(1 − ρ²(1−ψ²)) against ‖(I − P_x)μ‖² ≤ ψ²θ_a²(n−1)(1−ψ²), which is positive for ρ² (1 − ψ²) + ψ² < 1 (ρ = 0.7, ψ = 0.5: 0.3675 + 0.25 < 1). PK(d*) for all d* ≤ g − 1 (every proxy configuration) is checked exactly at p = 16, 20 in `scripts/f1_exact_lh.py` (results §4 of REPORT); for general (ρ, ψ, g) it is a CONJECTURE that PK(g − 1) holds whenever |ψ| < ρ < 1, and it is **assumed** below.

### 3.2 The two-endpoint keep margins

**Lemma 3.3 (start side) — PROVED (via W1-EXP Thm 1, EXP′).** For x ∈ W(S°), j ∈ S°, with U := x ∩ C_{b(j)}... (block of j) ⊆ C_{b(j)}, the start deletion odds are κ₀(x, j) = [ϖ(|x|−1)/ϖ(|x|)]·r_b(U − j)/r_b(U), and on an event of probability → 1, uniformly over the ≤ 2^{g} block configurations U ∋ j,

  log r_b(U)/r_b(U − j) ≥ −½ log(n + 1) + ν log(1 + δ²_{U−j,j}/Q^{blk}) − κ_EXP ≥ c₁ n,

where δ_{U−j,j} is the block residual signal of j on the block content U − j (Lemma 3.2 restricted to the block: ≥ θ_j²(n−1)λ₀·(1 − ψβ)² under PK-a, since the block of a_i contains no b-proxies) and Q^{blk} ≤ yᵀy = n − 1. Hence κ₀(x, j) ≤ 2p·e^{−c₁n}, uniformly over x ∈ W(S°). The swap-out odds ρ₀(x, j) ≤ κ₀(x, j)·max_{l∉x} γ₀(x − j + l)/γ₀(x − j) and the second factor is an addition at a state missing j: a block ratio ≤ e^{O_P(log n)} for l outside unit(j) (noise, the block of l sees no signal change) and ≤ e^{(1 − c_K)·(gain of j)} for l a proxy of j by (PK-s) restricted to the block; so ρ₀(x, j) ≤ 2p·e^{−c_Kc₁n}.

*Proof.* The table ratio r_b(U)/r_b(U − j) is a within-block single-addition Bayes factor; W1-EXP Theorem 1 (EXP′, under G, R-lite, SE-blk, which hold on LH with SE-blk(λ₀)) gives the expansion with |R| ≤ κ_EXP = O(1), uniformly over the finitely many block pairs (U − j, j) — a finite union over blocks and U, each a Gaussian event. The residual signal within the block is Lemma 3.2 applied to the block design, and (PK-a) gives the factor (1 − ψβ)² ≥ c_K². Note that the block of a_i contains only a_i and its proxies: given a_i ∈ U, the proxies have zero partial covariance with μ (W1-EXP Lemma 4.1 / O-BGIBBS (P1d)), and given a_i ∉ U − j they carry a_i's signal; the first case is the one that enters κ₀. ∎

**Lemma 3.4 (posterior side) — PROOF SKETCH (ridge bookkeeping PROVED; Gaussian uniformity PROVED by a finite union; constants not optimised).** On an event of probability → 1, uniformly over all x ∈ W(S°) with |x| ≤ K and all j ∈ S°,

  F(x) − F(x − j) ≥ c₂ n,  and  F(x) − max_{l∉x} F(x − j + l) ≥ c₂ n.

*Sketch.* Write F(x) = log ϖ(|x|) + log C_n − ½ log D_x − ν log(2b₀ + Q_x). Three pieces.

(i) *Size prior and log-determinant.* log ϖ(|x|−1) − log ϖ(|x|) = log((2p − |x|)/|x|) ∈ [−log(2p), log(2p)] in absolute value ≤ log 2p. ½ log(D_{x−j}/D_x) ∈ [−½ log(n + 1), 0] (W3-VT38E §2, E1(b): the ratio D_x/D_{x−j} lies in [1, n + 1]). Both are O(log(np)).

(ii) *Ridge residual.* Q_x = yᵀy − n z_xᵀH_x⁻¹z_x with H_x = (n+1)G_x + I. Since H_x ≽ (n + 1)G_x, n·H_x⁻¹ ≼ (n/(n+1))G_x⁻¹ and Q_x ≥ yᵀy − ‖P_xy‖² = RSS_x ≥ RSS_{[p]} = ‖(I − P_{[p]})ε‖² ≥ σ*²(n − 1 − p)(1 − o_P(1)) ≥ ½c₀σ*²n w.p. → 1 (p ≤ (1 − c₀)n; a single χ² event). By the Schur complement of H_x in the block (x − j, j), Q_{x−j} − Q_x = n(ỹ_jᵀy)²/(x̃_jᵀx_j + 1/(n+1)) where x̃_j := (I − X_{x−j}((n+1)G_{x−j} + I)⁻¹(n+1)X_{x−j}ᵀ)x_j is the ridge residual of x_j on x − j and ỹ_j the same operator applied to y; the operator A := I − X_{x−j}((n+1)G_{x−j}+I)⁻¹(n+1)X_{x−j}ᵀ satisfies P^⊥_{x−j} ≼ A ≼ P^⊥_{x−j} + ((n+1)(n−1)λ₀)⁻¹ P_{x−j}, so Q_{x−j} − Q_x = (u_{x−j,j}ᵀy)²(1 + O(1/(n²λ₀))) with u the exact unit residual. Hence

  ν log(Q_{x−j}/Q_x) ≥ ν log(1 + (u_{x−j,j}ᵀy)²(1 − O(n⁻²))/Q_{x−j}) ≥ ν·(uᵀy)²(1−O(n⁻²))/(Q_{x−j} + (uᵀy)²) ≥ (n/2)·(uᵀy)²/(2(n−1)) ·(1 − o(1)),

using Q_{x−j} ≤ yᵀy = n − 1 and (uᵀy)² ≤ n − 1.

(iii) *Gaussian part, uniformly.* u_{x−j,j}ᵀy = δ_{x−j,j} + σ*Z_{x−j,j} with Z_{x−j,j} := u_{x−j,j}ᵀε/σ* ~ N(0,1). By Lemma 3.1, u_{x−j,j} depends on x only through x ∩ unit(j), so **the family {Z_{x−j,j} : x ∈ W(S°), j ∈ S°} has at most s·2^{2g} distinct members** (not 2^p). A union bound gives max |Z| ≤ √(2 log(s 2^{2g}) + 2 log log n) =: z_n = O(√log n) w.p. → 1, while δ_{x−j,j}² ≥ c_K²θ_j²(n − 1)λ₀ by Lemma 3.2 and (PK-a). So (uᵀy)² ≥ (c_K|θ_j|√((n−1)λ₀) − σ*z_n)² ≥ ½c_K²θ_j²λ₀(n − 1) for n large, and

  F(x) − F(x − j) ≥ (n/2)·c_K²θ_j²λ₀/4·(1 − o(1)) − log 2p − ½ log(n + 1) ≥ c₂n.

(iv) *Swaps.* F(x − j + l) − F(x) = [F(x − j + l) − F(x − j)] − [F(x) − F(x − j)]. For l ∈ unit(j) (a proxy of j, or j's partner) the first bracket is controlled by (PK-s): the swapped model's residual signal exceeds x's by c_Kθ_j²(n − 1), and the ridge/Gaussian steps give F(x − j + l) − F(x) ≤ −c₂n. For l in another unit whose truths are all in x, the first bracket is a null-type addition (Lemma 3.1: μ's components in that unit are already fitted), ≤ log(2p) + z_n²/2, so the swap is ≤ −c₂n + O(log n). The remaining case is l = b′ a **missing masked hub of another pair**: then the first bracket is the Θ(n) gain g₁(x − j, b′) of b′, and the swap is unfavourable only under

  **(DOM)** min_{x∈W(S°), j∈S°}[F(x) − F(x − j)] ≥ max_{x∈W(S°), b′∈M∖x}[F(x + b′) − F(x)] + c₄n  for a fixed c₄ > 0,

"every truth in S° is worth more than every missing hub", a checkable two-sided population condition (on LH: loss(a_i) ≍ β_i²(1−ψ_i²)·Var(a_i|rest) against gain(b′) ≍ ψ_{i′}²β_{i′}²(1−ψ_{i′}²); it holds for equal β's and ψ = 0.5, ρ = 0.7, and it is checked exactly in `f1b_swap_margins.py`). Without DOM the swap j → b′ is accepted at φ close to 1 and lands outside W(S°); the landing state is posterior-worse than x + b′ ∈ W(S°) by ≥ c₂n and returns to W(S°) when j's Gibbs label re-adds it (downhill at both endpoints), but it is **not** in a closed class: from x − j + b′ the proxies of the missing j are Θ(n)-favourable additions (`f1b`, LH20: +175 nats at n = 1600), so no finite enlargement of W(S°) by one-swap neighbours is closed. That case is a *reversible leak* (§5.2, Theorem F1′), not a closure statement.

The constants: c₂ can be taken as min_j c_K²θ_j²λ₀/16 for the deletions; the finite-union step is the only probabilistic input, and it is over O(s·2^{2g}·p) Gaussians (the p enters through the swap partners l, whose Z-family is again finite per unit). ∎ (sketch: the ridge inequalities are elementary; the Gaussian uniformity is a finite union by Lemma 3.1; what is *not* written with explicit constants is the o(1) bookkeeping in (ii)–(iii).)

**Remark 3.5 (why the exact Gram matters).** Lemma 3.1 is what makes the sup over the 2^{p−s} supersets a max over ≤ s·2^{2g} Gaussians. In a random design (LH-iid, W3-PXN) the cross-unit sample correlations are O_P(√(log p/n)), Lemma 3.1 holds only approximately, and the sup over supersets of size up to K is a genuine union over C(p, K) sets. There the class must be cut at a bounded number of extras, W_d(S°) := W(S°) ∩ {|x ∖ S₀| ≤ d}, which is not closed: the (d + 1)-st extra is added at rate O_P(n^{−1/2}·polylog) per round (W3-PXN P3's leakage computation). This is the LH-iid obstruction recorded in REPORT §6 (CONJECTURE F2-iid).

**Remark 3.6 (what the exact check found about enlarging the class).** The first draft of this proof used W⁺(S°) := W(S°) ∪ {x − j + b′}. The exact enumeration (`f1b_swap_margins.py`, REPORT §4.1) shows W⁺ is not closed: from x − j_h + b′ (a visible hub missing, another pair's hub present) the swap b′ → proxy(j_h) is posterior-favourable by +175 nats at n = 1600 (LH20), because the proxies of the missing j_h now carry its signal. Every such state is posterior-worse than x + b′ by Θ(n) and returns to W(S°) downhill, so the correct treatment is the reversible-leak theorem of §5.2, and the closure theorem is stated under DOM. On LH16 DOM holds with margin ≥ 13 nats at n = 400 and ≥ 415 nats at n = 6400 in every replicate; on LH20 it holds at n = 6400 (margin ≥ 52) and fails marginally in one of four replicates at n = 1600 (+4.7 nats at one superset with all a-proxies present), where the simulation nevertheless shows no particle outside W(S°) in 8/8 islands (the swap is accepted only for φ > 0.9 and is undone by j's label).

### 3.3 Theorem F2 — statement and proof

**Theorem F2 (LH exact Gram: closed superset class, delivery for free).** Let LH exact Gram hold with p ≤ (1 − c₀)n, fixed parameters, PK(g − 1) and DOM (DOM is void when c = 1 and |M ∖ x| ≤ 1 is the only case, since then the swap a₁ → b₁ is the same-unit case of PK-s), and EX-A, EX-S, CAL. Let W := W(S°). Then there are constants c, C > 0 (depending on ρ, ψ, g, θ, σ*) such that, on an event of P₀-probability → 1,

  (a) π₀(Ω ∖ W) ≤ C p e^{−cn} and π(Ω ∖ W) ≤ C p e^{−cn};
  (b) KEEP(W, η) holds with η ≤ C p² e^{−cn}, uniformly in φ ∈ [0, 1];
  (c) hence, for the four final islands, P(some particle is ever outside W | data) ≤ 4N[π₀(Ω ∖ W) + (T_e + L + 4)η] ≤ C′ N T_e p² e^{−cn} → 0 along R1/R4 (N = max(2500, n, p), T_e = O(log² n), p ≤ n^A);
  (d) DELIV(W) holds with every particle of every island eligible at 𝔉_T, and every particle stays in W through the terminal rounds.

*Proof.* (a) Every y ∉ W misses some j ∈ S°; let j be the smallest such and y⁺ := y ∪ (S° ∖ y) ∈ W. Then π₀(y)/π₀(y⁺) is a product of ≤ s deletion odds along a chain of supersets of S° ∖ (deleted so far); the first factor κ₀(y⁺, j) is bounded by Lemma 3.3 and the others by 1 ∨ (their own bound) — simpler: π₀(y) ≤ π₀(y⁺)·max_{x∈W}κ₀(x, j)·e^{(s−1)·O(log np)}, using that deleting further members changes the block ratios of *other* blocks by at most their own keep odds (≤ 1) or, within the same block, by a bounded size-prior factor; Lemma 3.3 applied at y⁺ gives κ₀ ≤ 2pe^{−c₁n}; summing over the ≤ |S°| choices of j and using π₀(y + j) ≤ 1 summed over y (the map y ↦ y + j is at most 2^s-to-one on the class), π₀(Ω ∖ W) ≤ s·2^s·2p·e^{−c₁n}. The posterior bound is the same with Lemma 3.4. (b) Lemma 1.2 with Lemmas 3.3–3.4; the swap into another unit's hub is unfavourable at the posterior endpoint by DOM and at the start endpoint by Lemma 3.3 (the hub's start odds are < 1). The uniform-in-φ statement is Lemma A's log-linearity. (c) Theorem F1 times 4 islands. (d) is (c) read at 𝔉_T and after. ∎

**What is PROVED and what is not.** Theorem F1 and Lemma 1.2 are PROVED. Lemma 3.1, 3.2 are PROVED. Lemma 3.3 is PROVED given W1-EXP Theorem 1 (PROVED, VERIFIED by W3-VEXP) and PK. Lemma 3.4 is a PROOF SKETCH (every step is elementary and the finite-union argument is complete in outline; the o(1) constants are not written with explicit remainders). DOM is a checkable condition; it is verified exactly on LH16 (all n) and LH20 (n = 6400) and fails marginally on LH20 at n = 1600 in one replicate (Remark 3.6). PK(g − 1) for (ρ, ψ, g) = (0.7, 0.5, 4) is checked exactly (REPORT §4); in general it is a CONJECTURE. The status of Theorem F2 as a whole is therefore **PROOF SKETCH**, with the structure (why the sup over supersets is finite) PROVED.

---

## 4. From delivery to scoring: extras, the crossing temperature, and repair on W — PROOF SKETCH

Theorem F2 puts every particle in W(S°) at every time. S₀ is scored during the bridge or in the terminal rounds if a particle (i) adds every missing hub and (ii) carries no extra at the moment the last hub label is executed (SR: the Gibbs step evaluates the flipped configuration; if the flipped configuration is S₀ it is scored). The hubs are the slow variables (their addition is uphill for φ < φ_hub and downhill after), the extras the fast ones (re-drawn by their own Gibbs label every round at every φ). This section records the sketch; it is the repair step REP(W) of T38 route (b2) on this family, and it is where the remaining risk sits.

**4.1 Hub crossing.** For x ∈ W(S°), b ∈ M ∖ x: g₁(x, b) := F(x + b) − F(x) ≥ c₃n (Lemma 3.2: δ²_{x,b} ≥ θ_b²(n−1)λ₀, the same ridge/Gaussian steps as Lemma 3.4 with the finite Z-family of Lemma 3.1), and g₀(x, b) := log γ₀(x + b) − log γ₀(x) = log ϖ-ratio + log r_{C_b}(U + b)/r_{C_b}(U) = −log(2p) − ½ log(n+1) + O_P(1) (C_b ⟂ μ: a pure-noise table ratio, finite family). The Gibbs addition odds of b at x and φ are κ_φ = e^{(1−φ)g₀ + φg₁}, so the crossing temperature is φ*(x, b) = −g₀/(g₁ − g₀) ≤ [log(2p) + ½ log(n+1) + O_P(1)]/(c₃n) =: φ_hub → 0, uniformly over x ∈ W(S°) (Proposition M(b) of W4-SHARE in this family). At every stage t with φ_t ≥ 2φ_hub, the addition probability of each missing hub at its label is ≥ 1 − e^{−(φ_t − φ*)(g₁ − g₀)} ≥ 1 − e^{−c₃nφ_hub} = 1 − (2p√n)^{−1}e^{−O(1)}.

**4.2 Extras are fast.** For a null l (null group) and x ∈ W(S°), the addition odds at φ are κ_φ(x, l) = e^{(1−φ)a₀ + φa₁} with a_e := log γ_e(x + l) − log γ_e(x), both of the form −log(2p) − ½log(n+1) + α_e Z_l²/2 + O(1) where Z_l := u_{x,l}ᵀε/σ* is, by Lemma 3.1, one of at most 2^{g−1} Gaussians attached to l (indexed by x ∩ C_l), and α₀ = σ*²/(σ*² + ‖μ‖²/(n−1)) < 1 (the null block sees all the signal as noise), α₁ = σ*²/(σ*² + Δ_x)·ν/(νQ_x/(n−1)) ≤ (1 − |x|/n)⁻¹(1 + o(1)) (Q_x ≥ RSS_x ≈ σ*²(n − |x|) + residual signal). Let τ_n := 2(1 − ε_n) log(2p√(n+1)) with ε_n := [½ log n − g log 2]/log(2p√(n+1)) ∈ (0, 1), so that P(max over the ≤ p2^{g−1} variables of Z² > τ_n) ≤ p2^{g−1}e^{−τ_n/2}/√(πτ_n) → 0 (needs ½ log n > g log 2, i.e. n > 4^{g}: n > 256 for g = 4, n > 4·10⁹ for g = 16: this constant is the price of the group structure and is the reason the finite-n numerics use g = 4). On that event, for x with |x| ≤ n/4 (so α₁ ≤ 4/3 + o(1)):

  κ_φ(x, l) ≤ (2p√(n+1))^{−1 + α(1−ε_n)}e^{O(1)} with α ≤ 4/3, i.e. ≤ (2p√n)^{−ε_n/3}·e^{O(1)} → 0 (ε_n ≥ ⅓ − o(1) for p ≤ n).

So every present extra is deleted at its label with probability ≥ 1 − (2p√n)^{−ε_n/3}e^{O(1)} =: 1 − q_n, at every φ, and the expected number of extras *added* in a round is ≤ Σ_l max_U κ_φ ≤ (2p√n)^{−1}·Σ_l Σ_U e^{α Z_{l,U}²/2}·e^{O(1)} ≤ C(2p√n)^{(α−1)(1−ε_n)−1}·p·2^{g−1}/√τ_n = O((2p√n)^{−2/3+o(1)}) =: ε_add → 0, by the truncated moment E[e^{αZ²/2}1{Z² ≤ τ}] ≤ C e^{(α−1)τ/2}/((α−1)√τ) for α > 1 (Lemma Tr of W3-PXN in the form needed here). Proxies of S°-members and of present hubs are null-like by O-BGIBBS (P1c,d) and are covered by the same bound with their own finite Z-family; proxies of a *missing* hub carry signal and are basin states (O-BGIBBS 𝔅_P): they are deleted once the hub is present ((P1c)), and until then they are harmless (they are in W).

**4.3 Extras count is a supermartingale-like process.** Within a round the number of extras k changes only at Gibbs labels (swaps preserve |x|; the independence proposal replaces x by a π₀-draw, which has k′ extras with P(k′ ≥ m) ≤ (Cn^{−1/2})^m, and is accepted only if fitter). Each extra present when its label comes is deleted w.p. ≥ 1 − q_n; at most B + 1 extras can avoid their label by being moved by a swap after it; the additions number A with E A ≤ ε_add. Hence E[k_end | x] ≤ (B + 1)·1{some swap moved an extra} + q_n k + ε_add, and more precisely P(k_end ≥ m + B + 2 | x, k ≤ n/4) ≤ P(Bin(k, q_n) ≥ m) + P(A ≥ 1)... The resampling step between rounds re-weights by e^{Δ_t d}, and the d-contribution of an extra is (α₁ − α₀)Z²/2 ∈ [0, (1−ε_n)log(2p√n)] per extra; an extra-carrying particle can be up-weighted by a factor ≤ (2p√n)^{Δ_t(1−ε_n)k}. This is where the sketch is incomplete: **the clean statement is that after the Gibbs labels of a round every null is at its local conditional, so the re-weighting only moves the extras' law from the φ_{t−1}-conditional to the φ_t-conditional, both bounded by q_n per null**; a rigorous version needs the within-round order (a swap can re-insert an extra after its label) and the independence proposal to be bookkept, which is a finite-constant exercise (the B + 1 swap labels and the one proposal give at most B + 2 "unequilibrated" positions per round). We record: CONJECTURE 4.3: on the event of 4.2, for every x ∈ W(S°) with |x ∖ S₀| ≤ n/4 and every t, P(the particle has ≥ m extras after the stage-t round | x) ≤ (B + 2)q_n^{⌈m/(B+2)⌉} + ε_add·C_m, uniformly; and P(any particle ever has > n/4 extras) → 0 (a drift argument from k ≤ B + 2 + o(1) per round against the K cap).

**4.4 Scoring S₀.** Given 4.1–4.3: at the first stage t* with φ_{t*} ≥ 2φ_hub (t* = 1 if the first grid point exceeds 2φ_hub; on the method's grid the restricted ESS rule inserts temperatures below the crossing whenever S₀-type models are in V, so t* > 1 typically: O-BGIBBS §5), every particle adds each missing hub at its label w.p. ≥ 1 − (2p√n)^{−1}; a particle whose extras are all deleted by the time the last hub label executes, or which carries no extra, scores S₀ at that label (SR). With the ≤ (B + 2)q_n + ε_add bound on carrying an extra at a given time, P(a given particle scores S₀ during the stage-t* round) ≥ P(O)·(1 − (B+2)q_n − ε_add − c(2p√n)^{−1}) where O is the order event that the hub labels precede the extra labels *of the extras present* — for a particle with no extra, O is trivial, so P ≥ 1 − o(1); with N particles independent given 𝔉_{t*−1}, P(no particle scores S₀ in stage t*) ≤ (o(1))^N·… → 0. If t* > T (the grid never passes 2φ_hub before φ = 1, which cannot happen since φ_T = 1 ≥ 2φ_hub for n large), the same argument runs in the stage-T round at φ = 1. The L + 4 further terminal rounds give (1 − c₀)^{L+4} → 0 with c₀ the one-round probability above, which is bounded below uniformly over x ∈ W(S°) with ≤ B + 2 extras (Lemma R of O-BGIBBS with Λ = (missing hubs) ∪ (present extras), |Λ| ≤ c + B + 2, P(O) ≥ 1/(c + B + 2)!, α_φ → 1, Dep → 0). **Status: PROOF SKETCH**, with CONJECTURE 4.3 as the only non-routine input; the scoring step itself is Lemma R.

**4.5 Comparison with the terminal-repair interface.** W6-FIXREV1's route (b2) wants DELIV(𝔛_n) + REP(𝔛_n) with repair certificates of bounded v. Theorem F2 gives DELIV(W(S°)) with *every* particle eligible; REP on W(S°) with bounded extras is Theorem B's territory (W1-T24G) with the look-alike sets being the proxies; §4.4 is the direct Gibbs-path version. Which one the paper uses is HQ's choice; the delivery half is closed on this family either way.

---

## 5. Where the closed-class route fails, and what then

**5.1 Posterior-barrier designs (W4-SHARE PB).** There S° = {12} ⊂ S₀ and the superset class W({12}) is closed (deleting 12 is unfavourable), delivery to W({12}) holds in 200/200 islands (W4 s3), but S₀ is reached from {12} only through a gate of odds e^{−6.3} (single additions) or e^{−12} (pairs) at *both* endpoints. Theorem F1 applies and says nothing wrong: the class is delivered, repair fails. This is W4's finding restated: outside T03's regime (b2) fails through REPAIR; Theorem F1 does not create a delivery problem where there is none. Under R, Proposition M(a) excludes the barrier among truth-subsets; so the closed-class route + Prop M is the (b2) story in T03's regime.

**5.2 When KEEP fails: a leaky class.** If DOM fails (a missing hub worth more than some truth in S°: the swap j → b′ is then accepted near φ = 1), or if PK fails (a truth deletable at a proxy-rich superset), W(S°) leaks at a rate η ≫ e^{−cn} (for the DOM leak: ≈ 1/(|x|(p − |x|)) per round at φ ≈ 1, i.e. N(T+L+4)η ≫ 1). The leak states miss one truth and are posterior-worse than their W-parents; by Lemma PD they cannot take over unless they are *also* fitter in d, which (Lemma PD again) means posterior-better: impossible for a deletion of a truth with positive partial signal. So the leaks are **reversible leaks** (the truth is re-added downhill), and the right tool is D4 with a potential that counts a leaked particle at a discounted value: h(x) = 1 for x ∈ W, h(x) = ρ for x ∈ leak set, 0 otherwise, with (TRACK) η_t = (probability of leaving W ∪ leak) and the envelope governed by the fitness gap between W and the leak set, which is ≤ 0 (leaks are less fit). This gives delivery with ∏(1 − η_s) ≥ e^{−Tη} as long as Tη → 0, i.e. η = o(1/T_e): a per-round exit rate o(1/log² n) is enough. We record this as **Theorem F1′ (CONJECTURE, routine from D4)**: for a class W whose exits all land in a set 𝓛 with sup_{𝓛} d ≤ inf_W d (less fit), and from which the kernel returns to W w.p. ≥ 1 − η′ per round, D4 with h = 1_W + ρ1_𝓛 gives P(n_T(W ∪ 𝓛) = 0) ≤ exp{−Nπ₀(h₀)(1 − e^{−c})} with 1/c ≤ [1 + (T−1)/(e−1)]/∏(1 − η_s − η′_s). The posterior-worse leak cannot drive the C1 mechanism because it has no fitness advantage (r_t ≥ 1 for the h-weighted subpopulation vs the leak class), which is why only exits to *fitter* states matter, and KEEP's two-endpoint form excludes those.

**5.3 The genuinely open case.** The method fails route (b2) only if the near-truth class has an exit to a **posterior-better** state that is **not closer to S₀** (a C1-type outsider inside BVS). By Lemma PD that outsider must beat the occupied states in the posterior, and by Proposition M (under R, SE) every state missing a truth has a downhill addition towards S₀, so the posterior-better outsider is itself closer to S₀ unless it adds extras that pay for themselves — an extra with F(x + l) > F(x), i.e. a null with Z² > 2 log(2p√n): probability → 0 for the finite Z-families of LH but a union over p^{d} sets in random designs. That is the LH-iid obstruction (Remark 3.5), and it is the sharpest form of the remaining question: **does the sup over bounded-extras supersets of the null leakage stay below the size penalty in a random design?** W3-PXN's Lemma B gives the exact Beta laws per state; what is missing is the uniformity over the states a particle can visit. CONJECTURE F2-iid (REPORT §2) states the expected answer.
