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
