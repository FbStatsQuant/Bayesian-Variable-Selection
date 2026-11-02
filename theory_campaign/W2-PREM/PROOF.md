# W2-PREM — PROOF.md: the premises of Theorem B (restated T24)

Run of 2026-11-02, branch `theory/W2-PREM`. Nothing here has been reviewed; every PROVED is a **candidate** pending
cross-family review. Notation: `Docs/Theory/theorems/00_COMMON.md`, and W1-T24G `PROOF.md` §0 (branch
`theory/W1-T24G`), cited as [B]. W1-EXP `PROOF.md` (branch `theory/W1-EXP`) is cited as [E]. Method:
`Docs/Methodology/METHODOLOGY_v3.md` (§6.5–6.8) and the engine `Scripts/SMC_BVS/core/cpp/v3_engine.h`,
`v3_core.cpp`, `v3_util.h`, `v3_start.h`.

Status words: PROVED, PROVED UNDER (an explicit extra condition, named), PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE,
OPEN. Never upgraded.

---------------------------------------------------------------------------------------------------------

## 0. What the premises are, exactly

Theorem B ([B] §4) bounds P_x(S₀ not scored within H terminal rounds) by P(Bin(H, c_*) < v) + Hη. Its asymptotic
usefulness needs, uniformly over an eligible set of starts with bounded v:

  (U1) c_* ≥ c > 0 with probability → 1, and (U2) (L+4)·η → 0 in probability (L ≍ log₂ n).

η = η₁ + η₂ is a **sum over labels of sups over a family** of the per-label bad-step probability. The premises named
in [B] §6 and in the task are the asymptotic conditions that make each piece small. Written out:

| code | quantity (all sups over the stated family; all sums over labels) | needed |
|---|---|---|
| τ₂ | Σ_{i∈S₀} sup_{W∈𝒮_a°}(1−o_i(W)) + truth-removing swap acceptances at 𝒮_a° | o_P(1/log n) |
| NL0(a) | Λ₂(a) := Σ_{l∉S₀} sup_{W∈𝒮_a°, l∉W} o_l(W)  (null additions at supersets) | o_P(1/log n) |
| UDEL(a) | ε_del(a) := sup_{W∈𝒮_a°, l∈P(W)} o_l(W) | o_P(1) |
| BTP | ε_add(x) → 0 (one missing truth addable at every phase-1 state with the same missing set) | o_P(1) |
| TS | Σ_{i∈S₀} sup_{W∈𝒵⁺} (1−o_i(W)) (truth removal at incomplete states) | o_P(1/log n) |
| TL(𝒵,A) | junk additions that leave the family at incomplete states | o_P(1/log n) |
| IND (in [B]: "IND(𝓕)") | sup_W Σ_{S′ bad} π₀(S′)(1 ∧ e^{d(S′)−d(W)}) (independence-proposal bad acceptance) | o_P(1/log n) |
| IND (in the task: (R5)) | conditional independence of the terminal trajectories of distinct particles | exact |

**Naming collision (found at the start of this run).** The task file defines IND as conditional independence of
terminal trajectories and calls it "genuinely open in the masked regime". In [B] the code IND(𝓕) is the
*independence-move bad-acceptance* premise (its §6 table, row "independence bad acceptance"; REPORT §4); conditional
independence is the separate fact (R5), which [B] *uses* (Cor. B-M, Cor. P1) but does not list among the premises.
The regime-dependent open item in [B] is IND(𝓕). This file treats both, as **IND-T** (trajectories, §1) and
**IND-M** (move, §6).

Throughout: G (fixed design, ε ~ N(0, σ²I)); **R-lite(A, M)**: p ≤ n^A, ‖μ‖² ≤ Mn; s₀ and a fixed;
**SE(k; φ₀)**: λ_min(R_V) ≥ φ₀² for every nonempty V with |V| ≤ k (k fixed). The project's SE (sizes up to
m_n + s₀ → ∞) implies SE(k) for every fixed k eventually, so SE(k) is weaker. **BM-∞**:
min_{j∈S₀} θ*_j² ≥ M_n σ² log n/(nφ₀²), M_n → ∞. C_R := 2M + 4σ².

---------------------------------------------------------------------------------------------------------

## 1. IND-T: conditional independence of terminal trajectories. PROVED (under EX-S, EX-A)

### 1.1 What the implementation does (read from the code)

- `v3_core.cpp::cpp_final_run`: each final island r = 1..4 gets its own `RngSource` seeded by
  `seed_stream(seed, 9 + r)` (streams 10–13); calibration uses streams 0–9 (`cpp_cal_new`, `stream(k)`).
- `v3_engine.h::run_island_s`: one island = N initial π₀ draws (particle 1..N), then for t = 1..T: weights,
  **multinomial resampling** (N uniforms, purpose "resample"), then `population_round(P, φ_t)`; then L burn-in rounds
  and H_m = 4 measured rounds, each a `population_round(P, 1.0)`. **No resampling after stage T.**
- `population_round` loops i = 1..N and calls `one_round(P[i])`; **all particles of the island read the same stream,
  sequentially**: round h of particle 1, then of particle 2, …, then round h+1 of particle 1, …
- The number of uniforms a particle consumes in a round is **state-dependent**: `draw_order` uses m−1; each Gibbs
  step one; `step_uswap` none at |S| ∈ {0,p}, else three; `step_nswap` none at S = ∅, one if N(j)∖S = ∅, else three;
  `step_indep` 1 + (#backward block-size steps) + (#nonempty blocks) + 1 (`draw_pi0`). It is bounded by a
  deterministic constant m_max(p, B, J).
- The grid ends at φ_T = 1 and the stage-T round runs at φ = 1 **after** the last resampling. So the segment without
  resampling has **H′ = L + 5 rounds at φ = 1** (stage-T round, L burn-in, 4 measured), one more than [B]'s L + 4.

So the particles do **not** have separate streams; (R5) of [B] ("per-particle fresh randomness") is not literally what
the code does. The question is whether sequential consumption of one stream still gives independent trajectories.

### 1.2 The lemma

**EX-S (00_COMMON).** The stream of an island is an iid U(0,1) sequence (U_s)_{s≥1}, independent across streams.
**EX-A.** The arithmetic is exact (in particular ⌊u·k⌋ is uniform on {0,…,k−1}).

**Lemma S (shift at a stopping time). PROVED.** Let 𝔊_s = σ(U₁,…,U_s) and let ς be an a.s. finite (𝔊_s)-stopping
time. Then (U_{ς+k})_{k≥1} is iid U(0,1) and independent of 𝔊_ς.

*Proof.* For A ∈ 𝔊_ς and Borel B₁,…,B_m: P(A ∩ ⋂_k{U_{ς+k} ∈ B_k}) = Σ_s P(A ∩ {ς = s} ∩ ⋂_k{U_{s+k} ∈ B_k}) =
Σ_s P(A ∩ {ς = s}) ∏_k λ(B_k) = P(A) ∏_k λ(B_k), because A ∩ {ς = s} ∈ 𝔊_s is independent of (U_{s+k})_k. ∎

**Theorem IND-T. PROVED (EX-S, EX-A).** Fix a final island. Let 𝔉_T be the σ-field generated by the island's stream up
to the end of the stage-T resampling (the last reweighting), together with the data and 𝓒 (𝓒 is a function of
streams 0–9, independent of the island's stream). Let x_i be particle i's state right after that resampling and let
Y_{i,h} (h = 1..H′) be particle i's *extended* round output in the h-th round after it: the end state, every model
scored during the round (held states, Gibbs alternatives, swap and independence proposals), and every recorded o_j.
Then, conditionally on 𝔉_T:

  (a) the N sequences (Y_{i,1},…,Y_{i,H′}), i = 1..N, are independent;
  (b) particle i's sequence is a Markov chain started at x_i whose round transition is the extended round kernel K̄₁
      (the law of one `one_round` at φ = 1, [B] §0), the same for every particle.

The same holds for the 4 islands jointly (different streams), and conditionally on 𝔉_T *including* everything scored
before the terminal segment (so events such as "S₀ not scored during the bridge" may be conditioned on).

*Proof.* Order the round blocks after stage-T resampling lexicographically: (1,1), (1,2), …, (1,N), (2,1), … (round,
particle). Let ς_{h,i} be the stream position at which block (h,i) starts. Block (h,i) reads uniforms starting at
ς_{h,i}+1 and stops after a number τ_{h,i} of reads that is determined by the state Y_{i,h−1} (end state x_{i,h−1})
and the values read so far (the code decides each further read from the current state and earlier reads), and
τ_{h,i} ≤ m_max. Hence ς_{h,i} is an a.s. finite (𝔊_s)-stopping time (by induction: ς_{(next)} = ς + τ∘shift_ς is a
stopping time when ς is and τ is a stopping time of the shifted sequence), and 𝔉_T ∨ σ(Y_{j,g} : (g,j) ≺ (h,i)) ⊆
𝔊_{ς_{h,i}}. The output is Y_{i,h} = Φ(x_{i,h−1}; U_{ς_{h,i}+1}, U_{ς_{h,i}+2}, …) for one fixed measurable Φ (the
code of `one_round`). By Lemma S the shifted sequence is iid U(0,1) and independent of 𝔊_{ς_{h,i}}, so

  P(Y_{i,h} ∈ · | 𝔊_{ς_{h,i}}) = K̄₁(x_{i,h−1}, ·),

which depends on the past only through particle i's own previous state. By the chain rule over the blocks in order,
the conditional joint law given 𝔉_T is ∏_{(h,i)} K̄₁(x_{i,h−1}, dy_{i,h}) = ∏_i [∏_h K̄₁(x_{i,h−1}, dy_{i,h})], a product
over particles of Markov-chain laws. Islands use different streams, independent under EX-S. ∎

**Consequences.** [B]'s Cor. B-M and Cor. P1 hold as stated (with (R5) replaced by Theorem IND-T), and with
H′ = L + 5 instead of L + 4. The masked/favourable regime plays no role: IND-T is a property of the stream
discipline, not of the target.

**What IND-T does not give.** (i) The terminal-start particles x_1..x_N are *not* independent (they come from
multinomial resampling of a common population); the product bound is conditional on the population, and the number
of eligible particles N(𝓧) is T38's delivery question. (ii) EX-S is an idealisation: the production generator
(xoshiro256**, seeded by SplitMix64 of seed·2³² + stream) is deterministic; stream separation is by distinct seeds,
not by a proved jump-ahead. (iii) ⌊u·k⌋ with 53-bit u is not exactly uniform (EX-A).

**Numerical check** (`scripts/ind_streams.py`, `results/ind_streams.txt`): a toy chain with state-dependent uniform
consumption, two particles, one shared sequential stream vs two separate streams, 4·10⁵ replicates: χ² independence
statistic 13.2 on 9 df (5% critical 16.9); total variation between the two joint laws 0.0035 (MC scale 0.006).

---------------------------------------------------------------------------------------------------------

## 2. Lemma U: one uniform log-BF expansion, shared with EXP′. PROVED

**Lemma U(𝔉).** Let 𝔉 be a family of pairs (T, l), l ∉ T, determined by X, with |T + l| ≤ k (k fixed) and
#{T+l, T : (T,l) ∈ 𝔉} ≤ n^{A′}. Assume G, R-lite(A, M) and λ_min(R_V) ≥ φ₀² for every nonempty V ∈ {T, T+l :
(T,l) ∈ 𝔉}. Fix L > 4A′ (in all uses below L = 4kA + 1). There is an event E_n = E_n(𝔉) with P₀(E_n) → 1 on which,
simultaneously for all (T,l) ∈ 𝔉,

  log[BF(T+l)/BF(T)] = −½ log(n+1) − ν log(1 − x_{T,l}) + R_{T,l},   |R_{T,l}| ≤ κ_n,   (U)

  κ_n := (1+φ₀⁻²)/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/(c_E n),  c_E := σ²/(8(M + 2σ²)),

(κ_n → 0.52/c_E; this is [E]'s κ_EXP), with x_{T,l} = (RSS_T − RSS_{T+l})/RSS_T = (δ_{T,l} + σZ_{T,l})²/RSS_T, and
moreover, for every V among these sets and every V of size ≤ k used below:

  (E1) ‖P_V ε‖² ≤ Lσ² log n, hence Z²_{T,l} ≤ L log n;  (E2) RSS_V ≥ ‖(I − P_{V∪S₀})Cε‖² ≥ σ²(n−1)(1 − ϑ_n),
  ϑ_n := n^{−1/3} + L log n/(n−1);  (E3) ‖Cε‖² ≤ σ²(n−1)(1 + n^{−1/3});  (E4) ‖Y‖² ≤ C_R n.

**EXP′ is the instance** 𝔉_blk = {(T,l) : T + l ⊆ C_b for some block b} (k = B + 1 ≤ 17, A′ = A + 1, SE only on
subsets of blocks = SE-blk), because the tables are Bayes factors: r_b(U) = BF(U) for U ⊆ C_b (00_COMMON §2). The
instance used for Theorem B's premises is 𝔉_k := {(T,l) : |T+l| ≤ k}, A′ = kA, with SE(k).

*Proof.* [E] Lemmas 1.1–1.3 (Q_S vs RSS; determinant ratio; exact decomposition) never use that T + l lies in a
block: they use only λ_min(G_{T+l}) ≥ φ₀²(n−1) and, through Cauchy interlacing, the same for T. They give
|R_{T,l}| ≤ (1+φ₀⁻²)/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/min_{U∈{T,T+l}} RSS^y_U. [E] Lemma 1.4 (RSS floor) is a union
bound over the sets U: for each U put W_U = span(X_U, μ) (dimension ≤ k+1); E exp(‖P_{W_U}ε‖²/(4σ²)) ≤ 2^{(k+1)/2},
so P(max_U ‖P_{W_U}ε‖² > Lσ² log n) ≤ n^{A′} 2^{(k+1)/2} n^{−L/4} → 0 for L > 4A′. With ‖Cε‖²/σ² ~ χ²_{n−1}
(so (E3) and ‖Cε‖² ≥ σ²(n−1)(1−n^{−1/3}) w.p. → 1), the contraction step of [E] Lemma 1.4 gives RSS_U ≥
‖Cε‖² − ‖P_{W_U}ε‖², which is (E2) (apply it to W = span(X_{U∪S₀}), which contains μ) and RSS^y_U ≥ c_E n. (E1) is
the same union bound applied to span X_V; Z_{T,l} = u_{T,l}ᵀε/σ with u_{T,l} ∈ span X_{T+l}, so Z² ≤ ‖P_{T+l}ε‖²/σ².
(E4) is [E] Lemma 1.4's last step. ∎

**Corollaries** (on E_n(𝔉_k); W, l with |W ∪ l| ≤ k; k′ := |W∖l|; prior ratio w(k′+1)/w(k′) = (k′+1)/(2p−k′−1)).
odds_l(W) := γ₁(W∪l)/γ₁(W∖l), so o_l(W) = odds/(1+odds).

- **(C1) Gibbs odds.** log odds_l(W) = log[(k′+1)/(2p−k′−1)] − ½log(n+1) + ν log(1 + q/RSS_{W∪l}) + R,
  q := (δ + σZ)², δ = δ_{W∖l,l}, Z = Z_{W∖l,l}.
- **(C2) Floor.** odds_l(W) ≥ (2p)⁻¹(n+1)^{−1/2}e^{−κ_n} always (log(1+t) ≥ 0, (k′+1)/(2p−k′−1) ≥ 1/(2p)).
- **(C3) Zero-leakage ceiling.** If δ = 0 (e.g. W ⊇ S₀ and l ∉ S₀), then
  odds_l(W) ≤ [(k′+1)/(2p−k′−1)](n+1)^{−1/2} e^{κ_n + ϑ′_n} e^{Z²/2}, ϑ′_n := L log n·(ϑ_n + 3/n)/(1−ϑ_n) → 0.
  *Proof.* ν log(1 + σ²Z²/RSS) ≤ νσ²Z²/RSS ≤ Z²(n/2 + 0.01)/((n−1)(1−ϑ_n)) ≤ ½Z²(1 + ϑ_n + 3/n)/(1−ϑ_n) by (E2),
  and Z² ≤ L log n by (E1). ∎ (A matching lower bound with e^{−κ_n−ϑ′_n} holds by (E3) and log(1+t) ≥ t/(1+t).)
- **(C4) Signal gain.** If q ≥ g then odds_l(W) ≥ (2p)⁻¹(n+1)^{−1/2}e^{−κ_n} exp{g/(2C_R)}.
  *Proof.* ν log(1 + q/RSS_{W∪l}) ≥ (n/2)·q/(RSS_{W∪l} + q) and RSS_{W∪l} + q = RSS_{W∖l} ≤ ‖Y‖² ≤ C_R n by (E4). ∎
- **(C5) Gain from a signal gap.** If ‖(P_{W∪l} − P_{W∖l})μ‖² =: Δ ≥ 4Lσ² log n then q ≥ Δ/4 (because
  |δ| = √Δ and σ|Z| ≤ σ√(L log n) ≤ √Δ/2), so odds_l(W) ≥ (2p)⁻¹(n+1)^{−1/2}e^{−κ_n} e^{Δ/(8C_R)}.
- **(C6) Multi-step.** For V ⊂ V′, |V′| ≤ k, Δ := ‖(P_{V′} − P_V)μ‖² ≥ 4Lσ² log n (chain of single additions in any
  order, telescoping (U) and 1 − x = RSS_{after}/RSS_{before}):
  π(V)/π(V′) ≤ (2p√(n+1) e^{κ_n})^{|V′∖V|} exp{−Δ/(8C_R)}.
  *Proof.* log BF(V′) − log BF(V) ≥ −(|V′∖V|/2)log(n+1) − |V′∖V|κ_n + ν log(RSS_V/RSS_{V′}), and
  RSS_V − RSS_{V′} = ‖(P_{V′} − P_V)Y‖² ≥ (√Δ − σ√(L log n))² ≥ Δ/4 (E1 applied to span X_{V′}); then as in (C4).
  The prior ratio is ≤ (2p)^{|V′∖V|}. ∎

Under BM-∞ every "Δ ≥ c·M_n σ² log n" makes these factors **super-polynomially small**: n^{C}·exp{−cM_nσ²log n/C_R}
= o(n^{−r}) for every r.

**Numerical check** (`scripts/lemma_u_check.py`, `results/lemma_u_check.txt`; exact Gram, p = 24, AR(0.5), s₀ = 3,
k = 4, all 49,152 pairs): max |R| = 0.63, 0.80, 0.71, 0.76, 0.76 at n = 200, 10³, 5·10³, 2.5·10⁴, 1.25·10⁵; the
deterministic bound κ_n is ≈ 20 (valid, loose by a factor ≈ 25, as [E] also found).

---------------------------------------------------------------------------------------------------------

## 3. Phase-2 premises (supersets 𝒮_a = {S₀ ∪ P : |P| ≤ a})

Standing hypotheses of this section: G, R-lite(A, M), SE(s₀ + a + 1; φ₀), and E_n := E_n(𝔉_k) of Lemma U with
k = s₀ + a + 2 (the extra 1 is used in §3.1 for swaps). Write N₀ := [p]∖S₀ (nulls). For W ⊇ S₀ and l ∉ W,
μ ∈ span X_W, so **δ_{W,l} = 0** and x_{W,l} = σ²Z²_{W,l}/RSS_W, Z_{W,l} = u_{W,l}ᵀε/σ ~ N(0,1) exactly (u_{W,l} is a
deterministic unit vector).

### 3.1 τ₂: truth removal at supersets, by every label except I. PROVED under G, R-lite, SE(s₀+a+2), BM-∞

**Prop. T2.** On E_n, for every W ∈ 𝒮_a, i ∈ S₀ and l ∉ W:
 (a) 1 − o_i(W) ≤ 2p√(n+1)·e^{κ_n}·exp{−Δ_i/(8C_R)}, Δ_i := ‖(P_W − P_{W−i})μ‖² ≥ φ₀²(n−1)θ_i²;
 (b) γ₁(W−i+l)/γ₁(W) ≤ e^{2κ_n+ϑ′_n} n^{L/2} exp{−Δ_i′/(8C_R)}·√(n+1), Δ_i′ := ‖(P_{W+l} − P_{W+l−i})μ‖² ≥ φ₀²(n−1)θ_i².
Under BM-∞ both are n^{−ω(1)} (super-polynomial) uniformly; so the Gibbs truth-deletion term, the uniform-swap
truth-removal term and the B neighbour-swap truth-removal terms of η₂(a) (the Hastings factor is ≤ p) are
n^{−ω(1)}.

*Proof.* (a) (P_W − P_{W−i})μ = θ_i(I − P_{W−i})x_i (the other truths lie in W−i), and ‖(I−P_{W−i})x_i‖² =
1/(G_W⁻¹)_{ii} ≥ λ_min(G_W) ≥ φ₀²(n−1). 1 − o_i ≤ 1/odds_i(W−i); apply (C5) (Δ_i ≥ M_nσ² log n(n−1)/n ≥ 4Lσ² log n
eventually). (b) Same size, so the prior cancels: γ₁(W−i+l)/γ₁(W) = [BF(W+l−i)/BF(W+l)]·[BF(W+l)/BF(W)]. The first
factor is 1/odds-type for deleting truth i from the superset W+l: ≤ √(n+1)e^{κ_n}e^{−Δ′_i/(8C_R)} by (C5) without the
prior; the second is a zero-leakage addition, ≤ (n+1)^{−1/2}e^{κ_n+ϑ′_n}e^{Z²/2} ≤ e^{κ_n+ϑ′_n}n^{L/2} by (C3)
(without the prior) and (E1). ∎

### 3.2 The comparison lemma and the partner graph

**Definition (partner graph).** For nulls l ≠ m let ϱ_{lm} be the partial correlation of x_l and x_m given X_{S₀}
(cosine of the angle between their residuals on span X_{S₀}). For a threshold c_n, 𝒢_n is the graph on N₀ with an
edge {l, m} iff |ϱ_{lm}| > c_n. D_n := its maximum degree.

**PG(a; c_n, D_n).** c_n log n → 0 and (eD_n + 1)^a log^{3/2}(n)/√n → 0.

(For iid-Gaussian designs with population-uncorrelated nulls, max |ϱ| = O_P(√(log p/n)), so c_n = 1/log² n gives
D_n = 0 w.p. → 1; block designs with bounded groups (S3, S4, S6 type) give D_n ≤ g − 1; AR(ρ) gives
D_n = O(log log n). Common-factor / equicorrelated nulls give D_n = p − s₀ − 1: PG fails.)

**Lemma CMP (comparison). PROVED.** On E_n, let W = S₀ ∪ P (|P| ≤ a), l ∉ W, let P₁ be the set of m ∈ P joined to l
by a path of 𝒢_n inside P ∪ {l}, and P₂ := P∖P₁. Then, with C_a := (1 + a/φ₀²)/φ₀² and ρ² := a C_a² c_n²/φ₀²
(assumed ≤ ¼),

  Z²_{W,l} ≤ Z²_{S₀∪P₁,l} + ϵ_n,   ϵ_n := (2ρ + 3ρ²)·L log n·(1 + 2ρ²)  → 0 under PG.

*Proof.* Put B := S₀ ∪ P₁ and let Π be the orthogonal projection onto span{(I − P_B)x_m : m ∈ P₂}; then
I − P_W = (I − P_B) − Π. With ǔ := u_{B,l} (the unit residual of x_l on B), u_{W,l} = (ǔ − Πǔ)/√(1 − ‖Πǔ‖²), hence

  Z_{W,l} = (Z_{B,l} − ǔᵀΠε/σ)/√(1 − ρ_l²),  ρ_l := ‖Πǔ‖,  |ǔᵀΠε| ≤ ρ_l‖Πε‖ ≤ ρ_l σ√(L log n)

(Πε is a projection of P_Wε; (E1)). *Bound on ρ_l.* Let Ǧ be the Gram matrix of the residuals of X_{P₂} on B: it is
a Schur complement of G_W, so Ǧ ⪰ φ₀²(n−1)I. With ǧ_m := ((I−P_B)x_m)ᵀǔ = ‖(I−P_B)x_m‖·ϱ_{lm|B},
ρ_l² = ǧᵀǦ⁻¹ǧ ≤ Σ_{m∈P₂}ϱ²_{lm|B}/φ₀². *Bound on ϱ_{lm|B}.* Let Γ be the correlation matrix of the residuals on
S₀ of {x_k : k ∈ P₁ ∪ {l, m}}; its off-diagonal entries are the ϱ's, and λ_min(Γ_Q) ≥ φ₀² for every sub-collection Q
(a Schur complement of G_{S₀∪Q} rescaled by norms ≤ √(n−1)). Then ϱ_{lm|B} is the partial correlation of l, m given
P₁ in Γ:

  ϱ_{lm|B} = (Γ_{lm} − Γ_{l,P₁}Γ_{P₁}⁻¹Γ_{P₁,m}) / √((1 − R²_l)(1 − R²_m)),   1 − R² ≥ φ₀².

By construction m ∈ P₂ has no 𝒢_n-edge to l or to any k ∈ P₁, so |Γ_{lm}| ≤ c_n and ‖Γ_{P₁,m}‖ ≤ √a c_n, while
‖Γ_{l,P₁}‖ ≤ √a. Hence |ϱ_{lm|B}| ≤ (c_n + a c_n/φ₀²)/φ₀² = C_a c_n and ρ_l² ≤ aC_a²c_n²/φ₀² = ρ². Finally
(|Z_B| + ρ√(L log n))²/(1−ρ²) ≤ (Z_B² + 2ρL log n + ρ²L log n)(1 + 2ρ²) and Z_B² ≤ L log n (E1). ∎

**Counting.** 𝒦_a(l) := {Q ⊆ N₀∖{l} : |Q| ≤ a, Q ∪ {l} connected in 𝒢_n}. In a graph of maximum degree D the number of
connected vertex sets of size j+1 containing a given vertex is ≤ (eD)^j, so |𝒦_a(l)| ≤ (eD_n + 1)^a.

### 3.3 NL0(a) and UDEL(a). PROVED UNDER PG(a); UDEL(1) PROVED (no extra condition)

**Prop. NL0.** Under G, R-lite, SE(s₀+a+2), PG(a), on E_n:

  Λ₂(a) = Σ_{l∈N₀} sup_{W∈𝒮_a°, l∉W} o_l(W) ≤ e^{κ_n+ϑ′_n+ϵ_n/2}·[(s₀+a+1)/(2p−s₀−a−1)]·(n+1)^{−1/2}·Ξ_n,
  Ξ_n := Σ_{l∈N₀} Σ_{Q∈𝒦_a(l)} e^{Z²_{S₀∪Q,l}/2}·1{Z²_{S₀∪Q,l} ≤ L log n},   E Ξ_n ≤ p(eD_n+1)^a·2√(L log n)/√(2π).

Hence Λ₂(a) = O_P((s₀+a+1)(eD_n+1)^a√(log n/n)) and (L+5)Λ₂(a) → 0 in probability.

*Proof.* o_l ≤ odds_l(W); (C3) gives odds_l(W) ≤ [(|W|+1)/(2p−|W|−1)](n+1)^{−1/2}e^{κ_n+ϑ′_n}e^{Z²_{W,l}/2}, and
Lemma CMP gives e^{Z²_{W,l}/2} ≤ e^{ϵ_n/2}e^{Z²_{S₀∪P₁,l}/2} with P₁ ∈ 𝒦_a(l); bound the sup over W by the sum over
𝒦_a(l). On E_n every Z² ≤ L log n, so the indicator is 1. Each Z_{S₀∪Q,l} is exactly N(0,1) and
E[e^{Z²/2}1{Z² ≤ h²}] = 2h/√(2π) (no independence used). Markov's inequality. ∎

**Prop. UDEL.** (a) a = 1: ε_del(1) = max_l o_l(S₀+l) ≤ (s₀+1)/(2p−s₀−1)·(n+1)^{−1/2}e^{κ_n+ϑ′_n}·p·log n with
probability → 1, so ε_del(1) = O_P(log n/√n): **PROVED** under G, R-lite, SE(s₀+2) alone.
(b) a ≥ 2, under PG(a−1): ε_del(a) = O_P((s₀+a)(eD_n+1)^{a−1} log n/√n) → 0: **PROVED UNDER PG**.

*Proof.* o_l(W) for l ∈ P(W) is the Gibbs probability of keeping l, odds_l(W) with W∖l ∈ 𝒮_{a−1}; (C3) + CMP reduce
the max over (W, l) to the max of N := p(eD_n+1)^{a−1} standard Gaussians Z_{S₀∪Q,l}, Q ∈ 𝒦_{a−1}(l). Union bound and
P(|Z| > t) ≤ e^{−t²/2} (t ≥ 1): P(max Z² > 2 log N + 2 log log n) ≤ 1/log n. So max e^{Z²/2} ≤ N log n. For a = 1,
𝒦₀(l) = {∅} and N = p − s₀. ∎

### 3.4 COUNTEREXAMPLE: NL0(1) and UDEL(2) fail under G, R, SE, BM-∞ alone (equicorrelated nulls)

**Construction (exact Gram, A = 1).** s₀ fixed truths with fixed θ, orthogonal to the nulls; the p − s₀ nulls
equicorrelated with correlation r ∈ (0,1) (so SE holds with φ₀² = min(1, 1 − r), BM-∞ holds, ‖μ‖²/n bounded);
p = ⌊n^β⌋ with β < 1 and rβ > ½ (e.g. r = 0.8, β = 0.9).

**Claim. COUNTEREXAMPLE (asymptotic; PROVED modulo the standard extreme-value facts cited).** With probability → 1,
Λ₂(1) ≥ c·p^{r}(log p)^{−(1+r)}·n^{−1/2}·e^{−O_P(√log p)} → ∞, and ε_del(2) → 1.

*Proof.* Residuals of nulls on S₀ are the nulls themselves (orthogonality), so ϱ_{lm} = r for all pairs and
Z_l := Z_{S₀,l} is an equicorrelated Gaussian vector: Z_l = √r ξ + √(1−r) e_l with ξ, e_l iid N(0,1). For W = S₀+m,
Z_{W,l} = (Z_l − rZ_m)/√(1−r²) (the one-step version of the computation in CMP). Take m* = argmin_m e_m and
l* = argmax_l e_l; w.p. → 1, e_{l*} ≥ √(2 log p) − log log p/√(2 log p) − 1 and e_{m*} ≤ −(same). Then
(Z_{l*} − rZ_{m*})²/(1−r²) ≥ (1+r)[2 log p − 2 log log p − O(1)] − O_P(√log p). The matching lower bound of (C3) gives
odds_{l*}(S₀+m*) ≥ (2p)⁻¹(n+1)^{−1/2}e^{−κ_n−ϑ′_n}e^{Z²/2}, i.e. ≥ c p^{r}(log p)^{−(1+r)}n^{−1/2}e^{−O_P(√log p)}. Since
Λ₂(1) ≥ o_{l*}(S₀+m*), and odds → ∞ forces o → 1, Λ₂(1) does not tend to 0; the same pair (l*, m*) gives
o_{l*}(S₀+m*+l*) → 1, i.e. ε_del(2) → 1. With rβ > ½ the odds diverge polynomially. ∎

So NL0(a) (a ≥ 1) and UDEL(a) (a ≥ 2) are genuine design conditions; PG is a sufficient one. With p > n allowed
(random designs, A > 1) the same computation gives failure as soon as r > 1/(2A) (leading order). **Caveat.** This
falsifies the *premise* (the sum-of-sups bad rate); it does not show that repair fails on this design — the actual
per-round bad frequency is an average over visited states, not a sup.

**Numerics** (`scripts/nl0_equicorr.py`, `results/nl0_equicorr.txt`): see REPORT §4.

---------------------------------------------------------------------------------------------------------

## 4. Phase-1 progress without BTP

[B] Prop. B1 needs ε_add → 0: *one fixed* missing truth j must be addable at every state with the same missing set
(best-target persistence, BTP). BTP can fail when look-alikes in W change which missing truth carries the residual
signal. It is not needed.

**Prop. B1′ (pointwise addability). PROVED (EX-S, EX-A).** Let 𝒲 be any repair family whose phase-1 part is closed
in the sense of [B] (on {no bad, no progress} the missing set is constant and the state stays in the family, and
adding a missing truth at a family state is a progress step). Put

  ε_pt(𝒲) := sup_{W∈𝒲, M(W)≠∅} min_{j∈M(W)} (1 − o_j(W)).

Then for every phase-1 W ∈ 𝒲: P_W(the round has no bad and no progress step) ≤ 1 − (1 − ε_pt)/|M(W)|.
Consequently Theorem B holds with c₁ replaced by c₁⁺ := max{1 − ε_add, (1 − ε_pt)/|M(x)|}.

*Proof.* Realise the round by independent pairs (T_e, ω_e)_{e∈Λ}: T_e iid U(0,1) arrival times (the order σ), ω_e
the randomness consumed by label e's step. By Theorem IND-T's argument (Lemma S applied to the step blocks within the
round) this realisation has the same joint law of the round as the code. Let M′ := M(W), τ := min_{j∈M′} T_{G_j},
J* := the argmin. Let 𝓗 := σ((T_e, ω_e)_{e∉G_{M′}}, τ). The labels executed before τ are the e ∉ G_{M′} with T_e < τ,
in increasing T_e; so the state W_τ just before τ and the event 𝒜_τ := {no bad and no progress before τ} are
𝓗-measurable. J* is uniform on M′ and independent of 𝓗 (exchangeability of the iid (T_{G_j})_{j∈M′}: the argmin is
independent of the minimum and of everything else), and ω_{G_{J*}} is independent of (𝓗, J*). On 𝒜_τ, W_τ ∈ 𝒲 and
M(W_τ) = M′ (an addition of a truth is progress, a removal is bad). If G_{J*} adds J* at time τ, that step is a
progress step. Hence

  P_W(no bad, no progress) ≤ E[1_{𝒜_τ}(1 − o_{J*}(W_τ))] = E[1_{𝒜_τ}·|M′|⁻¹Σ_{j∈M′}(1 − o_j(W_τ))]
                          ≤ 1 − |M′|⁻¹ max_j o_j(W_τ) ≤ 1 − (1 − ε_pt)/|M′|.

The cap is respected because |W_τ ∪ J*| ≤ s₀ + a ≤ K. In the proof of Theorem B ([B] §4, step (b)) only the
inequality P(J_h = 1 | 𝓖_{h−1}) ≥ c_* is used, so c₁ may be replaced by the larger of the two constants. ∎

**Prop. PA (pointwise addability holds). PROVED under G, R-lite, SE(k), BM-∞.** On E_n(𝔉_k), for every W with
|W| + s₀ ≤ k and M(W) ≠ ∅,

  min_{j∈M(W)} (1 − o_j(W)) ≤ 2p√(n+1)e^{κ_n} exp{−φ₀²M_nσ² log n·(n−1)/(8nC_R)},

so ε_pt(𝒲) = n^{−ω(1)} for **every** family of bounded-size states, with no further condition (no BTP, no COH).

*Proof.* Let M = M(W), r := (I − P_W)μ = (I − P_W)X_Mθ_M. By SE on W ∪ M, ‖r‖² ≥ λ_min(G_{W∪M})‖θ_M‖² ≥
φ₀²(n−1)‖θ_M‖². Let Ǔ be the matrix of unit residuals ǔ_j of x_j (j ∈ M) on W; Ǔ'Ǔ is the rescaled Schur complement,
so λ_min(Ǔ'Ǔ) ≥ φ₀², and r ∈ col(Ǔ). Hence Σ_{j∈M}(ǔ_j'r)² = ‖Ǔ'r‖² ≥ φ₀²‖r‖² and
max_j Δ⁺_j(W) = max_j (ǔ_j'r)² ≥ φ₀⁴(n−1)‖θ_M‖²/|M| ≥ φ₀⁴(n−1)θ²_min ≥ φ₀²M_nσ² log n(n−1)/n. Apply (C5) to that j. ∎

**Remark.** The price is the factor 1/|M(x)| (c₁⁺ ≥ 1/|M(x)| − o_P(1) instead of 1 − o_P(1)). BTP itself is not
proved or refuted here; it is simply no longer a premise.

---------------------------------------------------------------------------------------------------------

## 5. The repair family: a defect of [B]'s 𝒵(x), and Theorem B♯

### 5.1 The defect (COUNTEREXAMPLE to "η₁ → 0" with A = the method's neighbour graph)

[B] fixes A = A(x) = ⋃_{j∈M(x)} N(j)∖S₀ and a junk budget c = |x ∩ J|. A swap that replaces an element of A in W by
a junk null raises |Q| and **leaves 𝒵(x)** when |Q| = c, so it is a *bad* step. If that look-alike is *useless* at W
(it carries no residual signal), the swap is accepted with probability of order one.

**On LH this happens at the start itself.** Take an LH design ([E] §4.1) with a masked pair (j_a, j_b), x = S° (so
c = 0). Under the symmetric-union neighbour graph, every k ∈ C_a∖{j_a} is a neighbour of j_b as soon as g − 1 < B
(k's top-B list is its g−1 group-mates and then j_b, at correlation ψρ_a > ρ_n), so k ∈ A. But k is useless at
every W ∋ j_a: its residual on j_a is √(1−ρ_a²)e_k, orthogonal to the residual signal ∝ ξ (the part of x_{j_b}
orthogonal to x_{j_a}). At W* = S° ∪ {k} ∈ 𝒵(x), the uniform swap picks k with probability 1/|W*| and a junk l; with
δ_{S°,k} = δ_{S°,l} = 0, the acceptance is 1 ∧ e^{(Z_l² − Z_k²)/2 + O(κ_n)}, of order one on average over l.
So η₁ ≥ P_{W*}(U bad) ≥ c₀ > 0 and (L+4)η₁ → ∞: **COUNTEREXAMPLE** (numerical and reproducible: P_{W*}(U bad) =
0.088 at n = 1600, configuration B, `scripts/lh_premises.py`; the asymptotic statement is a PROOF SKETCH — the
average over junk l of 1 ∧ e^{(Z_l² − Z_k²)/2} stays bounded below as p grows because junk from independent groups
has iid Z_l). The same mechanism appears whenever a look-alike becomes useless after its truth (or its partner) is
present.

### 5.2 Theorem B♯ (monotone look-alike map). PROVED (as a modification of [B]'s proof; EX-A, EX-S, SR)

A **look-alike map** is a data-measurable 𝔄 : {∅ ≠ M′ ⊆ M(x)} → 2^{N₀} that is monotone (M″ ⊆ M′ ⇒ 𝔄(M″) ⊆ 𝔄(M′)).
For a start x with M(x) ≠ ∅ put E_x := x∖S₀, c := |E_x∖𝔄(M(x))|, a := |𝔄(M(x))| + c, and

  𝒵♯(x) := {W = U ∪ E : x∩S₀ ⊆ U ⊆ S₀, M(W) ≠ ∅, E ⊆ N₀, |E∖𝔄(M(W))| ≤ c + |𝔄(M(x))∖𝔄(M(W))|},
  𝓕♯(x) := 𝒵♯(x) ∪ 𝒮_a,   V as in [B] (|M| + a on 𝒵♯, |P| on 𝒮_a).

("Current junk" E∖𝔄(M(W)) may grow by exactly the look-alikes that stopped being look-alikes.) The constant map
𝔄 ≡ A(x) gives back [B]'s 𝒵(x). Define ε_add♯, ε_pt♯, η₁♯ as in [B]/§4 with 𝒵♯⁺ = 𝒵♯(x) in place of 𝒵⁺, and
c₁♯ := max{1 − ε_add♯, (1 − ε_pt♯)/|M(x)|}. Then **Theorem B holds verbatim**:
P_x(S₀ not scored within H) ≤ P(Bin(H, c_*♯) < v) + H(η₁♯ + η₂(a)), c_*♯ = min(c₁♯, c₂), v = V(x).

*Proof.* [B]'s proof uses the family only through: (F1) x ∈ 𝓕, S₀ ∈ 𝓕, V(W) = 0 iff W = S₀, V ≤ |M(x)| + a on 𝓕;
(F2) "bad" includes leaving 𝓕, raising V, removing a truth (definition); (F3) in phase 1, adding a missing truth at
a family state lands in 𝓕 with smaller V (used in B1, B1′); (F4) phase-2 states are 𝒮_a (B2 unchanged). Check:
(F1) x ∈ 𝒵♯(x) since |E_x∖𝔄(M(x))| = c. *Size bound:* for W ∈ 𝒵♯, monotonicity gives 𝔄(M(W)) ⊆ 𝔄(M(x)), so
|E| ≤ |𝔄(M(W))| + c + |𝔄(M(x))∖𝔄(M(W))| = a; hence |W| ≤ s₀ + a ≤ K and V ≤ |M(x)| + a. (F3) Let W ∈ 𝒵♯, j ∈ M(W),
W′ = W ∪ {j}. If M(W′) = ∅ then W′ = S₀ ∪ E with |E| ≤ a, i.e. W′ ∈ 𝒮_a and V(W′) = |E| ≤ a < |M(W)| + a. Otherwise,
with A₁ := 𝔄(M(W)) ⊇ A₂ := 𝔄(M(W′)): E∖A₂ ⊆ (E∖A₁) ∪ (A₁∖A₂), so |E∖A₂| ≤ c + |𝔄(M(x))∖A₁| + |A₁∖A₂| =
c + |𝔄(M(x))∖A₂| (disjoint pieces, A₂ ⊆ A₁ ⊆ 𝔄(M(x))); and U′ ⊇ x∩S₀. So W′ ∈ 𝒵♯ and V drops by 1. Every other
line of [B] §4 (Lemma F, Lemma C, B2, the main proof, Prop. D) is family-agnostic. ∎

**Which steps are neutral now.** Swapping a current-junk null for another null, a look-alike for a look-alike, junk
for a look-alike, and Gibbs deletions of nulls are neutral; the useless-look-alike swaps of §5.1 are neutral as soon
as 𝔄 does not contain useless look-alikes. The remaining phase-1 bad steps are: (b1) truth removal (Gibbs: §6.1;
swaps: §6.2); (b2) addition of a current-junk null at budget (Gibbs: §6.3) and swaps of a *useful* look-alike for
current junk at budget (§6.4); (b3) independence jumps (§7).

**Choice of 𝔄.** 𝔄 is a proof device (the method never uses it), so it may depend on the design and on S₀. The natural
choice is the *useful-look-alike map*: nulls whose residual, on S₀ minus some subset of the missing truths, has
non-negligible correlation with the missing signal. On LH this is 𝔄_LH(M′) = ⋃_{j_{b_i}∈M′}(C_{b_i}∖{j_{b_i}})
(group-mates of the masked hub, not of the present hub).

---------------------------------------------------------------------------------------------------------

## 6. Phase-1 bad steps

Notation: RSS^μ(V) := ‖(I − P_V)μ‖² (noise-free). For a family 𝒲 of phase-1 states: J(W) := N₀∖𝔄(M(W)) (current
junk).

### 6.1 TS: truth removal by Gibbs at incomplete states

**TS(𝒲).** Δ⁻_i(W) := RSS^μ(W−i) − RSS^μ(W) ≥ M′_nσ² log n for all W ∈ 𝒲, i ∈ W∩S₀, some M′_n → ∞.
Equivalently (up to φ₀²) n·γ_i(W)² ≥ M′_nσ² log n, γ(W) := G_W⁻¹X_W'μ, since Δ⁻_i = γ_i²‖(I−P_{W−i})x_i‖².

**Prop. TS. PROVED UNDER TS(𝒲)** (with G, R-lite, SE(k)): Σ_{i∈S₀} sup_{W∈𝒲}(1 − o_i(W)) = n^{−ω(1)}. *Proof.* (C5). ∎

**COUNTEREXAMPLE (TS is not implied by G, R, SE, BM-∞).** Exact Gram, truths 1, 2 with corr r ∈ (0,1), θ₁ = 1,
θ₂ = −1/r (fixed: BM-∞ and SE hold), other columns orthogonal. At W = {1}, γ₁(W) = θ₁ + rθ₂ = 0, so Δ⁻₁ = 0 and the
G₁ step deletes truth 1 with probability → 1 (it is a zero-leakage null at W∖1 = ∅: odds ≤ e^{O_P(1)}/(p√n)). Every
start containing 1 but not 2 therefore has η₁ ≥ 1 − o_P(1). PROVED (the computation above);
numerics `scripts/ts_cancel.py`: P(G₁ deletes 1 at {1}) = 0.996 → 0.99993 (n = 200 → 6.25·10⁵), while
P(G₂ adds 2 at {1}) = 1.000: repair is not blocked, only the potential's bookkeeping fails (the layered version of
[B] §8 is the fix; OPEN).

Sufficient conditions: COH ([B] §6); and, on LH, §8 (PROVED).

### 6.2 Truth removal by swaps: the few-substitutes condition

The uniform swap removes a uniformly chosen element of W and adds a uniformly chosen outsider; a truth-for-l swap is
bad. If some l *replaces* the truth's contribution (a "substitute"), its acceptance is of order one; only a vanishing
fraction of proposals may hit substitutes.

**FS(𝒲; D′, c₀).** For all W ∈ 𝒲, i ∈ W∩S₀: the set Sub(W,i) := {l ∉ W : RSS^μ(W−i+l) − RSS^μ(W) < c₀(n−1)} has at
most D′ elements, and Sub(W,i) ∩ N(i) = ∅ (no substitute is a neighbour of i in the method's graph).

**Prop. SW. PROVED UNDER FS(𝒲; D′, c₀)** (with G, R-lite(A,M), SE(k), c₀ > 0 fixed): on E_n,
sup_W P_W(U removes a truth) ≤ D′/(p − k) + p·e^{−c₀n/(16C_R)}·e^{2κ_n} and
sup_W P_W(N_b removes a truth) ≤ p·e^{−c₀n/(16C_R)}e^{2κ_n} for each of the B neighbour labels. Hence the swap part of
η₁ is O(D′/p) + e^{−Ω(n)}, and (L+5)·(it) → 0 iff p_n/log n → ∞ (or D′ = 0).

*Proof.* For l ∉ Sub(W,i) put V := W ∪ l. Since W−i+l = V−i and W = V−l, (U) gives
log BF(W−i+l) − log BF(W) = −ν log(RSS_{V−i}/RSS_{V−l}) + R_l − R_i (the −½log(n+1) terms cancel). Write
RSS_{V′} = RSS^μ(V′) + 2r_{V′}'ε + ‖(I−P_{V′})ε‖², r_{V′} = (I−P_{V′})μ. Then RSS_{V−i} − RSS_{V−l} ≥ c₀(n−1) −
2‖r_{V−i} − r_{V−l}‖σ√(L log n) − Lσ² log n, because r_{V−i} − r_{V−l} ∈ span X_V and ‖P_Vε‖² ≤ Lσ²log n (E1); and
‖r_{V−i} − r_{V−l}‖ ≤ 2‖μ‖ ≤ 2√(Mn). So the difference is ≥ c₀(n−1)/2 for large n, and with RSS_{V−l} ≤ C_R n,
ν log(1 + t) ≥ (n/2)t/(1+t) gives an acceptance ≤ e^{2κ_n}e^{−c₀n/(8C_R)·(1−o(1))}. The same size cancels the prior;
the neighbour swap's Hastings factor is ≤ p. U: the proposal hits a given (i, l) with probability 1/(|W|(p−|W|)),
and at most |W∩S₀|·D′ pairs are substitutes. N: substitutes are excluded from N(i). ∎

### 6.3 TL♯: current-junk additions at budget

**TL♯(𝒲).** Λ₁(𝒲) := Σ_{l∈N₀} sup_{W∈𝒲 : l∈J(W)∖W} o_l(W) = o_P(1/log n).

**Prop. TL. PROVED UNDER ZJL + CS(g₀)**, where
- **ZJL(𝒲)** (zero junk leakage): δ_{W,l} = 0 for every W ∈ 𝒲 and l ∈ J(W)∖W;
- **CS(g₀)** (component structure): there are sets 𝒞(l) ∋ l with |𝒞(l)| ≤ g₀ such that x_l ⊥ X_{W∖𝒞(l)} and
  X_{W∩𝒞(l)} ⊥ X_{W∖𝒞(l)} for all W ∈ 𝒲 (so u_{W,l} = u_{W∩𝒞(l),l}).
Then Λ₁(𝒲) = O_P(2^{g₀}(s₀+a+1)√(log n/n)).

*Proof.* With δ = 0, (C3)'s proof applies verbatim (it used only δ = 0 and (E2), which holds for every V, superset of
S₀ or not): odds_l(W) ≤ [(s₀+a+1)/(2p−s₀−a−1)](n+1)^{−1/2}e^{κ_n+ϑ′_n}e^{Z²_{W,l}/2}, and by CS, Z_{W,l} = Z_{W∩𝒞(l),l}
takes at most 2^{g₀} values per l. Then as in Prop. NL0. ∎

ZJL is exact zero leakage; in general designs it should be relaxed to a bounded-leakage version (δ² ≤ ησ² log n with
η < (√(2A+1) − √(2A))², the 00_COMMON NL_η threshold) — PROOF SKETCH only: the extra factor e^{|δ|·|Z|} is
n^{√(2Aη)+η/2} after truncation, which the threshold makes o(√n/ log^{3/2} n). For random designs the max-type
NL_η fails at fixed SNR ([E] REPORT, "What fails"), and an average/Beta argument (as in [E] §4.3) would be needed:
OPEN.

### 6.4 ULR: retention of useful look-alikes

**ULR(𝒲; c₀).** For all W ∈ 𝒲, k ∈ E(W) ∩ 𝔄(M(W)), l ∈ J(W)∖W: RSS^μ(W−k+l) − RSS^μ(W) ≥ c₀(n−1).

**Prop. ULR. PROVED UNDER ULR(𝒲; c₀)** (with G, R-lite, SE(k)): the U- and N-swap probabilities of replacing a
look-alike by current junk are ≤ p·e^{2κ_n}e^{−c₀n/(16C_R)} uniformly. *Proof.* As Prop. SW with k in the role of i. ∎

---------------------------------------------------------------------------------------------------------

## 7. IND-M: independence-proposal bad acceptance

**Prop. IM (reference bound). PROVED.** For any feasible S° and any W,

  β_I(W) := Σ_{S′ bad at W} π₀(S′)(1 ∧ e^{d(S′)−d(W)}) ≤ (1 − π₀(S°)) + 1{S° bad at W}·π(S°)/(π(W)π₀(S°)).

*Proof.* Split S′ = S° from S′ ≠ S°; for the latter use 1 ∧ (·) ≤ 1. For S°: e^{d(S°)−d(W)} =
[γ₁(S°)/γ₀(S°)][γ₀(W)/γ₁(W)] = [π(S°)/π(W)][π₀(W)/π₀(S°)] ≤ π(S°)/(π(W)π₀(S°)). ∎

**SCR(S°)** (start concentration on a reference): S° ⊆ S₀ deterministic, fixed size, 1 − π₀(S°) = o_P(1/log n).
**GS(S°)** (subset gain): for every ∅ ≠ T ⊆ M := S₀∖S°, Δ_T := RSS^μ(S°) − RSS^μ(S°∪T) ≥ M′_nσ² log n.
(For T = M this is automatic from SE: Δ_M ≥ φ₀²(n−1)‖θ_M‖².)

**Prop. IND-M. PROVED UNDER SCR(S°) + GS(S°)** (with G, R-lite, SE(s₀+a+2), BM-∞), for eligible starts x ⊇ S° and
the family 𝓕♯(x) (or [B]'s 𝓕(x)): uniformly over W ∈ 𝓕(x)∖{S₀},

  β_I(W) ≤ (1 − π₀(S°)) + 2(2p√(n+1)e^{κ_n})^{s₀+a}·exp{−M′_nσ² log n/(8C_R)} = o_P(1/log n).

*Proof.* (i) *When is S° bad at W?* x ⊇ S° and W ∩ S₀ ⊇ x ∩ S₀ ⊇ S° (phase 1), or W ⊇ S₀ (phase 2). If W∩M = ∅ then
(phase 1) W∩S₀ = S°, S° removes no truth, M(S°) = M(W), V(S°) = V(W), and S° ∈ 𝒵♯(x) (E = ∅; x∩S₀ ⊆ S°): not bad.
If T := W∩M ≠ ∅ then S° ⊉ W∩S₀: bad. (ii) For T ≠ ∅, W = S° ∪ T ∪ E with E = W∖S₀, |E| ≤ a. Removing the nulls of E
one at a time multiplies π by at most 2p√(n+1)e^{κ_n} each ((C2)), so π(S°∪T)/π(W) ≤ (2p√(n+1)e^{κ_n})^a; and (C6)
with Δ_T gives π(S°)/π(S°∪T) ≤ (2p√(n+1)e^{κ_n})^{|T|}e^{−Δ_T/(8C_R)}. (iii) π₀(S°) ≥ ½ w.p. → 1 by SCR. ∎

**What this does not cover.** (a) Starts not containing S°. (b) A start concentrated on a *superset* S° ⊋ S₀ (the
double-counting supersets [B] observed at n = 200, p = 20 in S3/S4/S6): then at W ∈ 𝒮_a with |P(W)| < |P(S°)| the
draw S° is bad and its acceptance e^{d(S°)−d(W)} need not be small: **OPEN** (plausibly false at finite n).
(c) A start spread over many references: replace 1 − π₀(S°) by 1 − π₀(ℛ) for a finite reference set ℛ and require GS for
each member — same proof (PROOF SKETCH). (d) The favourable regime S° = S₀: then S° is never bad and β_I ≤ 1 − π₀(S₀),
which T22(iii) controls.

---------------------------------------------------------------------------------------------------------

## 8. One family where (almost) every premise is discharged: LH (exact Gram)

Setting: [E] §4.1–4.2, exact-Gram realisation X'X = (n−1)Σ_LH, p ≤ n − 1, groups of size g, g ≤ B_n < 2g,
|ψ_i| < min(ρ_{a_i}, ρ_{b_i}) (so blocks = groups, [E] Lemma 4.2), fixed nonzero coefficients, c linked pairs,
any number of visible and null groups; **plus p_n/log n → ∞**. S° := S₀∖M, M = {j_{b_1},…,j_{b_c}} (masked hubs).
Look-alike map 𝔄_LH(M′) := ⋃_{j_{b_i}∈M′}(C_{b_i}∖{j_{b_i}}). Eligible set 𝓧_LH := {x : S° ⊆ x ⊆ S₀ ∪ 𝔄_LH(M)}
(so c = 0 and a = |𝔄_LH(M(x))| ≤ c(g−1)). Write η = η₁♯ + η₂(a).

Population facts used (all exact in-sample because X'X = (n−1)Σ). Let ξ_i be the unit-variance part of x_{j_{b_i}}
orthogonal to x_{j_{a_i}} (x_{j_b} = ψx_{j_a} + √(1−ψ²)ξ). In a linked pair: ξ ⊥ every column of C_a; a member k of
C_b is ρ_b x_{j_b} + r_k with r_k ⊥ (hubs, C_a); a member k of C_a is ρ_a x_{j_a} + √(1−ρ_a²)e_k with e_k ⊥ (x_{j_a},
x_{j_b}, C_b); and μ restricted to the pair is β(x_{j_a} − ψx_{j_b}) = β√(1−ψ²)·(x_{j_a}-part orthogonal to x_{j_b}).
Columns of different components (pairs, visible groups, null groups) are orthogonal.

| premise | on LH | status | where |
|---|---|---|---|
| SE(k), R-lite, BM-∞ | λ_min(Σ_LH) ≥ (1−ψ₊)(1−ρ₊) ([E] L4.1a); fixed θ | PROVED | [E] |
| IND-T | stream discipline | PROVED | §1 |
| τ₂ | — | PROVED | §3.1 |
| NL0(a), UDEL(a) | partner graph given S₀: group-mates only (given the hubs, linked groups are conditionally independent; other groups orthogonal), D_n ≤ g − 1 | PROVED | §3.3 |
| PA (replaces BTP) | — | PROVED | §4 |
| TS(𝒵♯) | γ_{j_a}(W) ∈ [β(1−ψ²), β] when j_b ∉ W (see below); exact otherwise | PROVED | below |
| FS (swaps) | substitutes only among the other pairs' missing hubs/look-alikes, D′ ≤ (c−1)g; no neighbour substitute | PROVED structurally; the neighbour gap c₀ verified numerically for configuration B | below |
| TL♯ | ZJL exact (current junk has residual ⊥ residual signal); CS with 𝒞(l) = component of l, g₀ = 2g | PROVED | below |
| ULR | equicorrelated look-alikes each carry a unique part of ξ | verified numerically for configuration B (c₀ = 0.0137); general LH: CONJECTURE | below |
| IND-M | SCR(S°): 1 − π₀(S°) = O_P(2^B n^{−1/2}) ([E] Thm 5(a), candidate); GS(S°): Δ_T = Σ_{i∈T}ψ_i²β_i²(1−ψ_i²)(n−1) | PROVED (given [E] Thm 5(a)) | §7, below |

**TS on LH. PROVED.** Let W ⊇ S° (bounded size, any nulls). Components separate, so γ_i(W) is computed inside i's
component. Visible hub j_h: μ_h = β_h x_{j_h} ∈ span(W ∩ C_h), γ = β_h. Pair with j_b ∈ W: μ_pair ∈ span, γ_{j_a} = β,
γ_{j_b} = −ψβ. Pair with j_b ∉ W: W_pair = {j_a} ∪ P_a ∪ P_b (P_a ⊆ C_a∖j_a, P_b ⊆ C_b∖j_b). Regress x_{j_b} on W_pair:
x_{j_b} = ψx_{j_a} + √(1−ψ²)ξ, ξ ⊥ (x_{j_a}, X_{P_a}), and X_{P_b} = ρ_bψx_{j_a}1' + Y with columns y_k = α ξ + r_k,
α = ρ_b√(1−ψ²), Y ⊥ (x_{j_a}, X_{P_a}). So P_W ξ = Σ_k w_k y_k with α Σ_k w_k = ‖P_Wξ‖²/‖ξ‖²·… ∈ [0, 1) (strictly < 1 by
SE), and the coefficient of x_{j_a} in P_W x_{j_b} is c_a = ψ(1 − αΣw_k) ∈ (0, ψ]. Hence γ_{j_a}(W) = β(1 − ψc_a) ≥
β(1 − ψ²) > 0. With ‖(I−P_{W−i})x_i‖² ≥ φ₀²(n−1), Δ⁻_i(W) ≥ min{β_h², β²(1−ψ²)², ψ²β²}φ₀²(n−1): linear in n. ∎

**ZJL and CS on LH. PROVED.** Let W ∈ 𝒵♯(x), l ∈ J(W)∖W. The residual signal (I−P_W)μ lives in the components of the
pairs with j_b ∉ W, where it equals −ψβ√(1−ψ²)(ξ − P_Wξ) and P_Wξ ∈ span(Y) ⊥ C_a. If l is in another component,
x_l ⊥ that component: δ = 0. If l ∈ C_a of such a pair: its residual on W is the residual of √(1−ρ_a²)e_l, and e_l ⊥ ξ,
e_l ⊥ Y, so ⟨(I−P_W)x_l, (I−P_W)μ⟩ = ⟨x_l, (I−P_W)μ⟩ = 0. (C_b members of an incomplete pair are in 𝔄_LH, not junk.)
CS: u_{W,l} depends only on W ∩ comp(l), |comp(l)| ≤ 2g. Numerically max |δ|/(n−1) over all 6,112 phase-1 states of
configuration B is 2·10⁻¹⁶. ∎

**FS on LH (structure). PROVED.** Removing truth i and adding l: if l lies in a component with no residual signal and
not in comp(i), x_l is orthogonal to (I−P_{W−i})μ, so the loss equals Δ⁻_i(W) (linear, by TS). So substitutes lie in
comp(i) or in the incomplete pairs' components: D′ ≤ 2g·c, bounded. That no substitute is a *neighbour* of i (and the
gap c₀) is a finite population computation per component type; for configuration B (`scripts/lh_fs_gap.py`,
`results/lh_fs_gap.txt`): over all 6,112 phase-1 states, D′ = 4 for every c₀ ≤ 0.05 (substitute types: an added
masked hub replaced by the other pair's masked hub or one of its look-alikes), and the minimal loss over neighbours is
0.168 > 0. ULR: minimal loss 0.0137 > 0.

**Theorem L (Gibbs-path repair on LH). PROOF SKETCH** (every component PROVED except the two finite population
inequalities FS-neighbour gap and ULR, which are verified numerically for configuration B, and the cited candidate
[E] Thm 5(a)). Under the setting above, uniformly over x ∈ 𝓧_LH, with H′ = L + 5:

  c_*♯(x) ≥ min{1/|M(x)|, 1/(B+3)} − o_P(1),   η(x) = O_P(4^g(s₀+a+1)√(log n/n) + 2^B n^{−1/2} + (c g)/p),

so (L+5)η → 0 and sup_{x∈𝓧_LH} P_x(S₀ not scored within H′) ≤ P(Bin(L+5, c) < v_max) + o_P(1) → 0, with
v_max = c + c(g−1) = cg. By Theorem IND-T, if N particles of the terminal-start population lie in 𝓧_LH, the
probability that none scores S₀ is ≤ (that bound)^N.

The single-particle rate is slow: P(Bin(L+5, c) < v) ≈ n^{−c/(v ln 2)}·polylog. The multi-particle product is the
operative route, exactly as [B] concluded.

---------------------------------------------------------------------------------------------------------

## 9. Assembly: Theorem B's asymptotic conclusion under explicit premises

**Corollary A. PROVED UNDER the listed premises.** Assume G, R-lite(A,M), SE(2s₀+a+2; φ₀), BM-∞, EX-S, EX-A, SR, a
fixed eligible set 𝓧 of starts with bounded a and v, a monotone look-alike map 𝔄, a reference S° ⊆ S₀, and

  PG(a) [§3.2], TS(𝒵♯) [§6.1], FS(𝒵♯; D′, c₀) with p_n/log n → ∞ [§6.2], TL♯(𝒵♯) [§6.3], ULR(𝒵♯; c₀) [§6.4],
  SCR(S°) + GS(S°) and x ⊇ S° for x ∈ 𝓧 [§7].

Then, uniformly over x ∈ 𝓧, c_*♯ ≥ min{1/|M(x)|, 1/(B+3)} − o_P(1) and (L+5)(η₁♯ + η₂(a)) → 0 in probability; hence
sup_{x∈𝓧} P_x(S₀ not scored within the L+5 terminal rounds) → 0 in probability, and, by IND-T, the multi-particle
product bound of [B] Cor. B-M holds conditionally on the terminal-start population.

*Proof.* Theorem B♯ (§5.2) with c₁♯ ≥ (1 − ε_pt)/|M(x)| (Prop. B1′) and ε_pt = n^{−ω(1)} (Prop. PA); c₂ ≥ 1/(B+3) −
ε_del and ε_del → 0 (Prop. UDEL). η₂(a) ≤ Λ₂(a) + τ₂ + sup β_I (Props. NL0, T2, IND-M; extra-for-null swaps at
supersets are neutral). η₁♯ ≤ TS-term + swap-terms + Λ₁ + ULR-terms + sup β_I (Props. TS, SW, TL, ULR, IND-M; the
classification of §5.2). Each is O_P of a quantity that is o(1/log n) under the stated premises. Finally
P(Bin(L+5, c) < v) → 0 as L → ∞ with v bounded and c > 0 fixed. ∎
