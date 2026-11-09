# W2-FAC-S5F — CHECKPOINT (2026-11-09, ~3 h after start)

Lead: Claude Fable 5.1 (Claude Personal). Target: reported-model consistency of the merged method (v3.1, LS0 from the
start mode with cap ℓ_n + |S̃₀|) on block compound symmetry (study S5), growing p, ideally any p ≤ n/2, by a route
different from the two-level gap invariant (W2-FAC-S5, not read, no coordination).

## What is established so far (files)

**Numerics (numerics/):** `bcs_core.py` — exact-Gram block-CS scorer in closed form (per-group aggregates, Schur
updates, differential gains, valid to n = 10¹²), verified against FAC-B's general scanner to 1e-7 and identical paths
(bcs_selftest_out.txt). `N1_raw.jsonl` (29 S5 paths, p ≤ 1000, n ≤ 10¹²) and `N2_raw.jsonl` (p ≤ 5000, log p/log n up
to 0.92): **every uncapped LS0 path from [p] is a pure null-deletion path ending at S₀**; best addition gain ≤ −0.4 log n
along every path; the global-centre bias |δ_T| ≤ 0.13·√(2 log p) over whole paths and ≤ 0.044·√(2 log p) while ≥ 50
variables are kept; the hole's largest add statistic is ≤ 4.2 × the current deletion level (standardized units).

**Exact structural tools (proved in notes, to be written as lemmas/L0–L1; all design-general unless stated):**
1. *Gain reduction.* For T ⊇ S₀, every neighbour gain equals the size term Δ_k = ½log(n+1) + log((2p−k)/k) + o(1)
   minus/plus −(n/2)log(1 + σ²Z²/RSS_T) + O(1), where Z² is the exact RSS increment (projection statistic), using only
   λ_min(Σ) ≥ c_min (Q-vs-RSS sandwich as in FAC-B L1.5(b)).
2. *Pythagoras / jump inequality.* Z²(l; T∖j) ≤ Z²(l; T) + Z²(j; T) for l ∉ T, j ∈ T (nested projections; also for
   the ridge quantity actually used by the score, by monotonicity). Consequence along a deletion path: a hole element's
   add statistic is at most the sum of the deletion statistics of the elements deleted from its own group (block
   designs: ≤ (q − 1) × the running maximum level).
3. *Swap domination.* F(T∖j∪l) − F(T) = G_add(l; T∖j) + G_del(j; T): if no addition improves at any T∖j (j ∈ T), every
   swap is strictly below the best deletion. Swaps reduce to NA at the "one-below" sets.
4. *Drift identity (one global factor).* c̄_T − c̄_{T∖j} = κ_T(j)·r_j(T): the global centre (= E[√a η | retained
   fit]) moves by a positive multiple of the deleted element's residual statistic — FAC-B's drift identity in general
   form (Gaussian conditioning on nested σ-fields).
5. *Block-CS structure.* Exact ANOVA split Φ(T) = Σ_G SSW_G + Q_M(T); for a null l with u retained group-mates,
   r_l = √c(ξ_l − ξ̄_G) + c w_u(ĝ_G − c̄_T), var_l = c(1 + b w_u) + a c² w_u²/(1 + aW); identity ỹ_G(U) ∝ Σ_{j∈U}
   Z^{loc}_j(U) (the retained group mean is proportional to the sum of its members' local statistics).
6. *Level lemma.* With m kept nulls, min kept statistic ≤ (√(2 log(2^{q+1}p/m) + 2L_n) + s|δ′|)² simultaneously for
   all m (counting fully-"large" configurations per group; independence across groups).
7. *Unconditional centre bound at the level scale.* |δ′_T| ≤ (d_max^{3/2}/d_min)[√(2 log(2^{q+1}p/m) + 4L_n) + 1.3]
   + o(1), uniformly over all T with m kept nulls (top-#hit order statistics of the configuration means).

## Diagnosis — where the difficulty sits

Everything except the global centre is handled by 1–7 with Θ(log n) margins. **The entire difficulty of S5 beyond 1/6
is the control of the global centre c̄_T along the path**: FAC-A's 1/6 is exactly "configuration union bound + trivial
centre bound" (θ = 1 in units of the local sd); any exponent > 1/6 needs |δ′_T| ≤ θ·√d₁·√(2 log p) with θ < 1 along the
path. Tool 7 gives this **in the bulk** (|δ′| = O(√log(p/m)) ≪ √log n while m ≥ p n^{−c}), unconditionally. In the
**end phase** (m ≤ p n^{−c}) the trivial bound is useless and the needed mechanism is FAC-B's majority-side/imbalance
analysis at the *group* level (retained singletons form a plain CS problem with κ = d₁/a, plus harmless mates of
retained singletons and a transient of multi-member configurations).

## Plan to completion (locked after statement lock)

* **(C2) BULK theorem — unconditional, every p ≤ n/2:** the uncapped LS0 path from S* makes only null deletions
  (no addition, swap or truth move) while m_t ≥ m_e := ⌈C p n^{−c₀}⌉, with explicit (crude) constants. New: a pervasive
  design with growing p where the one-dimensional reduction is unavailable, all exponents up to 1.
* **(C3) END phase:** (a) exact reduction to a group-level CS problem + the two extra hole types (proved); (b)
  completion under an explicit centre hypothesis (CC-end) [|δ′_t| ≤ θ√d₁√(2 log p) in the end phase]: pure deletion to
  S₀ for log p/log n < A*(θ, q) (A* → (q−1)/(2q−4) = 2/3 for q = 5 as θ → 0; the (q−1) jump factor is the limiting
  constant, numerically nearly attained). (c) Attempt an unconditional proof of (CC-end) via the group-level
  majority-side mechanism if time permits; otherwise report it as the exact obstruction with evidence (numerics N2:
  θ ≤ 0.13 observed).
* **(C4)** D_n and delivery consequences, conditional on completion; start mode (C1) as FAC-B L2 with block-CS
  population covariances (hypothesis (FS-B)).
* Reviews: statement lock → lemma checks (L0–L4) → mid-point at L4 (bulk theorem) → sweep → council.

Honest estimate: (C1), (C2), (C3a), (C3b) PROVED-CHECKED is realistic; an unconditional end phase (full any-p
consistency) is **unlikely** within this ticket by a route avoiding the two-level invariant. All results asymptotic.
