# W7-PART — PROOF: the partition-recovery lemma for iid Gaussian designs

Run of 2026-11-02, branch `theory/W7-PART`. Every result here is a **candidate**: not reviewed, not adopted.
Status words: PROVED, PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN (PROTOCOL.md). Scripts: `scripts/`; outputs:
`results/`.

---------------------------------------------------------------------------------------------------------

## 0. The algorithm, the setting, the notation

### 0.1 What the code does (read from `Scripts/SMC_BVS/core/cpp/v3_blocks.h`, `v3_score.h`, `v3_preprocess.R`)

The partition is `make_blocks(D, B)`:

1. `correlation_matrix(D)`: r̂_jl = G_jl/√(G_jj G_ll), where G = XᵀX is the Gram matrix of the **standardised
   columns of X** (`Data::G`, built in `data_init` from X only). This is the Pearson sample correlation of columns j and
   l, up to rounding.
2. `complete_linkage(D)`: agglomerative complete linkage on d_jl = 1 − |r̂_jl|, Lance–Williams update
   d(a∪b, x) = max(d(a,x), d(b,x)). Ties between candidate merges: the pair whose sorted union is lexicographically
   smallest (R13). Left child = child with the smaller minimum index.
3. Top-down cut: from the root, every node with more than B members is replaced by its two children (left first);
   nodes with ≤ B members are retained as clusters.
4. Next-fit packing of the retained clusters, in that order, into bins of capacity B, whole clusters only.
5. B = min(⌊√n⌋, ⌊√p⌋, 16) (`v3_preprocess.R` line 22; M §3). B = 14 at (n, p) = (200, 500) and (200, 1000).

**y does not enter.** `Data::G` is XᵀX; y enters only `Data::z = Xᵀy` and the block tables, which are built *after*
the partition. Preprocessing touches X only through dropping exactly-constant columns (probability 0 here) and
standardisation, which leaves every r̂_jl unchanged. Hence the partition is σ(X)-measurable, and for a design whose
rows are independent of ε it is independent of the noise vector ε. The only thresholds are B (cut and bin capacity);
the neighbour-graph threshold √(2 log p/n) belongs to M §6.4, not to the partition. Partition-building is skipped
entirely on the exact branch (M §6.2: p ≤ 17 for n ≥ 22), so every statement below concerns p ≥ 18.

The port in `scripts/part_core.py` was checked against the **compiled, unmodified engine header** (driver
`scripts/engine_blocks.cpp`): 70/70 identical partitions, including exact-tie designs (`results/check_port.txt`).

### 0.2 Setting

- Rows of X^r ∈ ℝ^{n×p} iid N(μ, Σ), Σ positive definite. Correlations are scale invariant, so take Σ with unit
  diagonal.
- 𝒢 = {C_1, …, C_G} a partition of [p] into **groups** of sizes g_h ∈ [g_min, g_max].
- **(GRP(ρ, ψ̄))**: |Σ_jl| ≥ ρ for j ≠ l in a common group, and |Σ_jk| ≤ ψ̄ for j, k in different groups, with
  0 ≤ ψ̄ < ρ < 1.
- **(SIZE)**: g_max ≤ B < 2 g_min, with B = B(n, p) the method's block size.
- **(IND)** (Theorem C only): the groups are mutually independent, Σ = blockdiag(Σ_h).

Examples. LH-iid (W3-PXN §0): equicorrelated groups (ρ), hub-linked pairs; the cross correlations are
ψ (hub–hub), ρψ (hub–member), ρ²ψ (member–member) and 0 elsewhere, so ψ̄ = |ψ|. The block-orthogonal benchmark:
ψ̄ = 0, (IND). The S5-type global factor Σ = ψ11ᵀ + blockdiag((ρ−ψ)J + (1−ρ)I): ψ̄ = ψ, not (IND).

### 0.3 Notation

- r̂_jl: sample correlation; d_jl = 1 − |r̂_jl|.
- For a group h: T_h = the complete-linkage dendrogram of h **alone** (computed on the |h| × |h| matrix
  (d_jl)_{j,l∈h}). For a node A ∈ T_h: ht(A) = its merge height (0 for a leaf), π(A) = the height of its parent in
  T_h (π(root) := +∞), σ(A) := 1 − π(A) (σ(root) := −∞).
- f_j := σ({j}) = 1 − (height at which j first merges in T_h): the *first-merge similarity* of j.
- m_h := min_{j≠l∈h} |r̂_jl| (the weakest within-group sample correlation); H_h := ht(root of T_h).
- A dendrogram on [p] is **laminar w.r.t. 𝒢** if every node is either a subset of one group or a union of whole
  groups.
- Λ_r(t) := (1−r²)(1−t²)/(1−rt)², I(t; r) := −½ log Λ_r(t) (the large-deviation rate of r̂ at t).
- H₀(s) := P(|r̂| ≥ s) under r = 0, = I_{1−s²}((n−2)/2, ½) (regularised incomplete beta), H₀(s) = 0 for s ≥ 1.
- a_n := √((n−2)/(2π)).

---------------------------------------------------------------------------------------------------------

## 1. Theorem A (deterministic): exact structure of complete linkage on a grouped set — PROVED

Assume all p(p−1)/2 values |r̂_jl| are distinct ("no ties"). Under the setting of §0.2 this holds almost surely:
for distinct pairs, r̂_jl² − r̂_ab² is a non-constant real-analytic function of X^r on the full-measure open set where
no column is constant, so its zero set is Lebesgue-null, and X^r has a density because Σ is positive definite.

**Lemma A0 (monotone heights; interleaving).**
(a) The heights of successive complete-linkage merges are nondecreasing.
(b) Call a merge *bad* if the new node is neither inside one group nor a union of whole groups. Up to the first bad
    merge, the merges performed inside each group h are exactly the merges of T_h, with the same heights and in the
    same order.
(c) If the first bad merge happens at height δ, then at that moment the current clusters inside group h are exactly
    the nodes A of T_h with ht(A) < δ < π(A).

*Proof.* (a) If a, b merge at height δ = d(a, b), the current minimum, then for every other cluster x,
d(a∪b, x) = max(d(a,x), d(b,x)) ≥ δ; all other distances are unchanged and ≥ δ. So the next merge height is ≥ δ.
(b) Induction over the merges before the first bad one. Every current cluster is inside a group or is a union of
whole groups. A merge of two clusters inside h is the global minimum, hence the minimum over pairs of current
h-clusters. Those are, by induction, the current clusters of T_h, and the distance between two h-clusters depends on
the entries of h only. With no ties this is the merge T_h makes next, at the same height.
(c) Let δ be the first bad height. All earlier merges have height ≤ δ by (a), and with no ties < δ, so no T_h merge of
height > δ has been executed. Suppose a T_h merge of height η < δ were not executed. Then, by (b) and the monotonicity
of T_h's own heights, the *next* unexecuted T_h merge has height η' ≤ η < δ. Its pair is available, at distance η'
< δ, which contradicts the minimality of the bad merge. ∎

**Condition (C\*).** For every pair of distinct groups h ≠ h' and every pair of nodes A ∈ T_h, A' ∈ T_{h'} that are
not both roots,

  max_{j∈A, k∈A'} d_jk  >  min(π(A), π(A')),   equivalently   min_{j∈A, k∈A'} |r̂_jk|  <  max(σ(A), σ(A')).

**Theorem A.** Assume no ties.
- **(A1) (C\*) ⇒ laminar.** If (C\*) holds, the complete-linkage dendrogram is laminar w.r.t. 𝒢.
- **(A2) Partial converse.** Suppose no merge of two unions of whole groups occurs at a height below max_h H_h. Then
  laminar ⇒ (C\*).
- **(A3) Laminar ⇒ partition.** If the dendrogram is laminar and g_max ≤ B, every block is a union of whole groups.
  If moreover B < 2 g_min (SIZE), the blocks are exactly the groups. This holds for every tie rule and every leaf order.
- **(A4) Margin ⇒ (C\*).** The *local margin*
  (M) for every h and every j ∈ h, k ∉ h: |r̂_jk| < min(m_h, m_{h(k)})
  implies (C\*). (M) is implied by the *global margin* max_{cross}|r̂| < min_{within}|r̂| used in W3-PXN Lemma P1.

*Proof of (A1).* Suppose a bad merge occurs, and take the first one, between current clusters P and Q at height
δ = max_{P×Q} d. Each of P and Q is either *partial* (a proper subset of a group) or *full* (a union of whole groups).
Since P ∪ Q is bad, at least one of them is partial, say P ⊊ h. Q is not inside h, because then P ∪ Q ⊆ h. By A0(c),
P is a node of T_h with π(P) > δ.
- If Q is partial, Q ⊊ h' with h' ≠ h, then Q is a node of T_{h'} with π(Q) > δ. Hence
  max_{P×Q} d = δ < min(π(P), π(Q)), which violates (C\*) for (P, Q). They are not both roots.
- If Q is full, Q ⊇ h' for some group h' ≠ h. Then max_{P×h'} d ≤ max_{P×Q} d = δ < π(P) = min(π(P), π(h')), since
  π(h') = ∞. This violates (C\*) for (P, h'), and P is not a root.
∎

*Proof of (A2).* Suppose (C\*) fails at (A, A'): max_{A×A'} d < min(π(A), π(A')) (strict, since there are no ties).
Without loss of generality π(A) ≤ π(A'), so A is not a root. Suppose, for contradiction, that the run is laminar.
Then every group's internal merges are those of T_h (the induction of A0(b) applies to the whole run). So A is current
from ht(A) until its parent merge at π(A), and A never merges with anything outside h before that.

Let k ∈ A', and let B' be the node of T_{h'} containing k that is current just before height π(A). This node exists
because ht({k}) = 0 < π(A). B' is a descendant of A' or an ancestor of A':
- If ht(A') < π(A), then B' ⊇ A', and B' = A' since π(A') ≥ π(A).
- Otherwise B' ⊊ A'.

In both cases B' ⊆ A', so max_{A×B'} d ≤ max_{A×A'} d < π(A).
- If B' is partial, it is a current cluster just before π(A).
- If B' = h' is full, the hypothesis of (A2) keeps h' unmerged with other groups below max_h H_h ≥ H_h ≥ π(A), so h'
  is itself a current cluster.

Either way, the pair (A, B') is available just before the merge at height π(A), with distance < π(A). This
contradicts the minimality of that merge. ∎

*Proof of (A3).* The cut retains, on every root-to-leaf path, the first node with ≤ B members. Let c be a retained
cluster. By laminarity c is either inside a group or a union of whole groups. Suppose c ⊊ h. The node h lies on the
path from the root to c, and h has g_h ≤ g_max ≤ B members, so the cut stops at h or above, never at c. This is a
contradiction, so every retained cluster is a union of whole groups. Packing concatenates whole retained clusters, so
every block is a union of whole groups.

Under B < 2 g_min a block cannot hold two groups (2 g_min > B), so it holds exactly one. Every group node has size
≤ B, and its parent has size ≥ 2 g_min > B. Hence every group is itself retained and packed alone: blocks = 𝒢.
∎

*Proof of (A4).* For a non-root A ∈ T_h, π(A) ≤ H_h. The root height of complete linkage is the diameter
max_{j,l∈h} d_jl: heights are monotone, and the diameter pair is merged at some node whose height is at least its
distance. So σ(A) ≥ 1 − H_h = m_h. Take (A, A') not both roots, say A non-root. Then
max(σ(A), σ(A')) ≥ σ(A) ≥ m_h ≥ min(m_h, m_{h'}) > |r̂_jk| for every j ∈ A, k ∈ A', by (M). Hence
min_{A×A'} |r̂| < max(σ(A), σ(A')). ∎

**Remarks.**
1. (C\*) is much weaker than (M), and that is the whole story at n = 200.
   - (M) asks every cross correlation to lose to the weakest within-group correlation.
   - (C\*) asks a cross pair (j, k) to lose only to max(f_j, f_k), the level at which j or k has already joined its own
     group.
   - A cross *node* pair needs **all** |A||A'| cross correlations to be large simultaneously.
   - Example (`results/check_thmA.txt`): in 320 hard replicates (M) held 15 times, while (C\*) and laminarity held
     261 times.
2. Laminarity can fail while blocks = 𝒢 still holds (for instance when the cut splits a bad node of size > B back
   into its parts). This never happened in the 320 replicates, but (A3) is only a sufficient direction.
3. Floating point: the engine compares rounded distances. A rounding flip requires two |r̂|'s within about 1e-15 of
   each other, an event of probability O(p²·1e-15) under a bounded density. We ignore it.

Numerical check: `scripts/check_thmA.py` → `results/check_thmA.txt`. In 320 replicates over 8 hard configurations
(indep / LH near the ψ = ρ boundary / global factor), (C\*) ⟺ laminar held 320/320, laminar ⟺ blocks = groups held
320/320, and (M) ⇒ (C\*) held without exception.

---------------------------------------------------------------------------------------------------------

## 2. Pair laws

**Lemma 1 (regression representation; PROVED).** Let (u_i, v_i), i ≤ n (n ≥ 3), be iid bivariate normal with
correlation r ∈ (−1, 1), and let k = n − 2 and a = r/√(1−r²). Then

  T := √k · r̂/√(1−r̂²)  =_d  (Z + a√W)/√(V/k),   with Z ~ N(0,1), W ~ χ²_{n−1}, V ~ χ²_{n−2} independent.

*Proof.* Without loss of generality the variances are 1 and the means 0, since r̂ is invariant under affine maps of
each coordinate with positive slope. Write v = r u + √(1−r²) w, where w is iid N(0,1) and independent of u. Let C be
the centring matrix. The OLS slope of v on (1, u) is b̂ = (Cu)ᵀv/‖Cu‖² = r + √(1−r²) Z/‖Cu‖, with
Z := (Cu)ᵀw/‖Cu‖. The residual sum of squares is (1−r²)V, with V := ‖P^⊥ w‖² and P^⊥ the projection onto
span(1, u)^⊥ (rank n − 2 almost surely). Conditionally on u, Z ~ N(0,1) and V ~ χ²_{n−2} are independent, since they
are projections of w onto orthogonal subspaces. Their joint law does not depend on u, so (Z, V) is independent of
W := ‖Cu‖² ~ χ²_{n−1}. The slope t-statistic is b̂‖Cu‖/√(RSS/k) = (a√W + Z)/√(V/k). The classical identity
t = √k r̂/√(1−r̂²) finishes the proof. ∎

**Corollary 1 (monotonicity; PROVED).** P_r(|r̂| ≥ t) is nondecreasing in |r|, and P_r(|r̂| ≤ t) is nonincreasing
in |r|.
*Proof.* By symmetry (flip the sign of v) take r ≥ 0. Given (W, V),
P(|T| ≤ τ) = P(|Z + c| ≤ x) with c = a√W ≥ 0 and x = τ√(V/k). We have
∂_c[Φ(x−c) − Φ(−x−c)] = φ(x+c) − φ(x−c) ≤ 0 for c, x ≥ 0, and c is increasing in r. Take expectations, and note
|r̂| ≤ t ⟺ |T| ≤ √k t/√(1−t²). ∎

**Lemma 2 (explicit tails; PROVED, given Hotelling's classical density).** For n ≥ 4, m := (n−4)/2, and
−1 < r < 1:

  (U) for t ≥ r:  P_r(r̂ ≥ t) ≤ a_n (1+|r|)^{3/2}(1−|r|)^{−1} (1−t) Λ_r(t)^m;
  (L) for t ≤ r:  P_r(r̂ ≤ t) ≤ a_n (1+|r|)^{3/2}(1−|r|)^{−1} (1+t) Λ_r(t)^m.

Consequently:
- for |r| ≤ ψ̄ < t, P_r(|r̂| ≥ t) ≤ 2 a_n (1+ψ̄)^{3/2}(1−ψ̄)^{−1}(1−t) Λ_ψ̄(t)^m;
- for 0 < t < ρ = r, P(|r̂| ≤ t) ≤ a_n (1+ρ)^{3/2}(1−ρ)^{−1}(1+t) Λ_ρ(t)^m.

*Proof.* Hotelling's density (Hotelling 1953, JRSS-B 15; the standard exact form) is
f(x) = (n−2)Γ(n−1)(1−r²)^{(n−1)/2}(1−x²)^{(n−4)/2} / (√(2π) Γ(n−½) (1−rx)^{n−3/2}) · ₂F₁(½, ½; n−½; (1+rx)/2).
`scripts/check_pairlaw.py` verifies it numerically: it integrates to 1, and its tails agree to about 1e-9 relative
error with the independent Lemma-1 route (noncentral-t quadrature), and with Monte Carlo. The steps:

1. **Bound the hypergeometric factor.** The ₂F₁ series has positive coefficients, so for z ∈ [0, 1] it is at most its
   value at z = 1. By Gauss's theorem (c − a − b = n − 3/2 > 0) that value is Γ(n−½)Γ(n−3/2)/Γ(n−1)².
2. **Bound the constant.** f(x) ≤ A_n (1−r²)^{(n−1)/2}(1−x²)^m(1−rx)^{−(n−3/2)}, with
   A_n = (n−2)Γ(n−3/2)/(√(2π)Γ(n−1)). Wendel's inequality Γ(x+½) ≤ x^{1/2}Γ(x), at x = n − 2, gives A_n ≤ a_n.
3. **Factor out Λ.** By exponent bookkeeping,
   (1−r²)^{(n−1)/2}(1−x²)^m(1−rx)^{−(n−3/2)} = (1−r²)^{3/2} Λ_r(x)^m (1−rx)^{−5/2}.
4. **Use the monotonicity of Λ.** ∂_x log Λ_r(x) = 2(r−x)/((1−x²)(1−rx)), so Λ_r is increasing on (−1, r) and
   decreasing on (r, 1). On [t, 1] with t ≥ r, Λ_r(x) ≤ Λ_r(t), and (1−rx)^{−5/2} ≤ (1−|r|)^{−5/2}. Integrating
   gives (U). (L) is identical on [−1, t].
5. **Two-sided cross bound.** For the two-sided form, P_r(r̂ ≤ −t) = P_{−r}(r̂ ≥ t). Also
   ∂_r log Λ_r(t) = 2(t−r)/((1−r²)(1−rt)) > 0 for r < t, so Λ_r(t) ≤ Λ_ψ̄(t) for |r| ≤ ψ̄. The prefactor is
   increasing in |r|.
6. **Within-group bound.** For the within form, |r̂| ≤ t implies r̂ ≤ t.

A grid check over 224 (n, r, t) triples gives no violation; the bound is at most 2.9–1100 times the exact tail
(`results/check_pairlaw.txt`). ∎

---------------------------------------------------------------------------------------------------------

## 3. Theorem B (the partition-recovery lemma, general cross correlation) — PROVED

**Theorem B.** Assume §0.2 with (GRP(ρ, ψ̄)) and (SIZE), and n ≥ 5. Write N_w for the number of within-group pairs
and N_× = p(p−1)/2 − N_w for the number of cross pairs. Then for every t ∈ (ψ̄, ρ):

  P(blocks ≠ 𝒢) ≤ Σ_{within (j,l)} P_ρ(|r̂| ≤ t) + Σ_{cross (j,k)} P_{|Σ_jk|}(|r̂| ≥ t)                       (B-exact)
               ≤ N_w a_n (1+ρ)^{3/2}(1−ρ)^{−1}(1+t)Λ_ρ(t)^{(n−4)/2} + N_× 2a_n(1+ψ̄)^{3/2}(1−ψ̄)^{−1}(1−t)Λ_ψ̄(t)^{(n−4)/2}.   (B-explicit)

**Corollary B (closed form and p^{−C}).** Let q := √((1−ψ̄²)/(1−ρ²)), t* := (q−1)/(qρ−ψ̄) ∈ (ψ̄, ρ), and
I* := I(t*; ψ̄) = I(t*; ρ) > 0. Then

  P(blocks ≠ 𝒢) ≤ (2/(√π (1−ρ))) · p² √n · e^{−(n−4) I*}.

Hence, if p ≤ n^A, then P(blocks ≠ 𝒢) ≤ p^{−C} for every n ≥ n₀(A, C, ρ, ψ̄), the smallest n with

  log(2/(√π(1−ρ))) + ((2 + C)A + ½) log n ≤ (n − 4) I*.

Special cases:
- ψ̄ = 0: t* = tanh(½ artanh ρ), the Fisher-z midpoint, and I* = −½ log(1 − t*²).
- ρ = 0.7, ψ̄ = 0: I* = 0.0912, t* = 0.408.
- ρ = 0.7, ψ̄ = 0.5 (LH): I* = 0.0126.
- ρ = 0.85, ψ̄ = 0: I* = 0.185.

Table of n₀ in `results/union_bound.txt`.

*Proof.* Under (M), Theorem A (A4 ⇒ A1 ⇒ A3) gives blocks = 𝒢 almost surely (no ties). The complement of (M) is
contained in

  {∃ within (j,l): |r̂_jl| ≤ t} ∪ {∃ cross (j,k): |r̂_jk| ≥ t}

for any t, because (M) holds whenever every within |r̂| > t > every cross |r̂|. Apply the union bound with the exact
pair laws (each pair is bivariate normal with correlation Σ_jl) to get (B-exact). Corollary 1 replaces |Σ_jl| ≥ ρ by
ρ and |Σ_jk| ≤ ψ̄ by ψ̄; Lemma 2 then gives (B-explicit).

For the corollary:
- At t*, Λ_ρ(t*) = Λ_ψ̄(t*), since (1 − ψ̄t)/(1 − ρt) = q has the unique root t*. The root lies in (ψ̄, ρ) because
  log Λ_ρ − log Λ_ψ̄ is negative at t = ψ̄ and positive at t = ρ.
- Both prefactors are ≤ 2^{5/2}/(1−ρ), using 1 + t ≤ 2, 1 − t ≤ 1, ψ̄ < ρ, and (1+·)^{3/2} ≤ 2^{3/2}.
- N_w + N_× ≤ p²/2, and ½ · 2^{5/2}/√(2π) = 2/√π.

For the p^{−C} statement, bound c p^{2+C} √n e^{−(n−4)I*} ≤ c n^{(2+C)A+½} e^{−(n−4)I*}. ∎

**What Theorem B buys, and what it does not.**
- It is exactly the task's lemma, with explicit constants in (n, p, g, ρ, ψ̄); g enters only through (SIZE), since
  the pair counts are bounded by p²/2.
- It covers any cross structure with |Σ_jk| ≤ ψ̄ < ρ, including the dependent LH linked pairs and the S5-type global
  factor.
- It does not use y. Its event is σ(X)-measurable, so it holds conditionally on nothing and jointly with any statement
  about ε.
- Its exponent I* is the margin exponent, and it is pessimistic (§4). At the study size it is non-vacuous for
  independent groups with ρ ≥ 0.7 but weak for LH (§5).
- The asymptotic rate is not sharp for the actual algorithm: Corollary C below doubles it for independent groups.

---------------------------------------------------------------------------------------------------------

## 4. Theorem C (sharp bound for independent groups) — PROVED; Corollary C (analytic evaluation) — PROVED

**Lemma 3 (rotation invariance; PROVED).** Let h ≠ h' be groups with X_h independent of X_{h'}. Let
u_j := Cx_j/‖Cx_j‖ ∈ S := the unit sphere of 1^⊥ ⊂ ℝⁿ (dimension n − 1). Then, conditionally on
(U_h, U_{h'}) := ((u_j)_{j∈h}, (u_k)_{k∈h'}), there is a random vector v uniform on S such that, for each fixed
k ∈ h', (r̂_jk)_{j∈h} =_d (⟨u_j, v⟩)_{j∈h}. Precisely, (r̂_jk)_{j∈h} has the law of (⟨u_j, O u_k⟩)_{j∈h} with O Haar
on the stabiliser of 1, independent of (U_h, U_{h'}).

In particular:
- for any unit w that is a function of (U_h, U_{h'}), P(|⟨w, v⟩| ≥ s | U_h, U_{h'}) = H₀(s);
- the conditional law of (r̂_jk)_{j∈h} given both within-group correlation matrices depends on R̂_h only.

*Proof.* For orthogonal O with O1 = 1 we have OC = CO. Also X_h = 1μ_hᵀ + Z L_hᵀ with Z iid N(0,1), and OZ =_d Z.
Hence OX_h =_d X_h and OU_h =_d U_h. With X_h ⊥ X_{h'}, (U_h, U_{h'}) =_d (O U_h, U_{h'}) for O Haar independent of
both, and r̂_jk = ⟨u_j, u_k⟩ for j ∈ h, k ∈ h'. Given (U_h, U_{h'}), Oᵀu_k is uniform on S, because the stabiliser
acts transitively on S. Finally, if v is uniform on the sphere of ℝ^{n−1}, then ⟨w, v⟩² ~ Beta(½, (n−2)/2), which is
the null law of r̂² (P(r̂² ≥ s²) = I_{1−s²}((n−2)/2, ½)). ∎

**Theorem C.** Assume no ties and (SIZE). Let 𝒟 be the set of unordered group pairs {h, h'} with X_h, X_{h'}
dependent. For an ordered pair (h, h'), define

  Φ_A(s) := min{ H₀(s), Σ_{ε∈{±1}^A, ε_{min A}=+1} H₀(|A| s/‖U_A ε‖) },       ‖U_A ε‖² = εᵀR̂_A ε,
  S_L(h,h') := Σ_{A∈T_h} Σ_{k∈h'} Φ_A(max(σ(A), f_k)),
  S_N(h,h') := Σ_{A∈T_h, |A|≥2} Σ_{A'∈T_{h'}, |A'|≥2, (A,A') not both roots} Φ_A(max(σ(A), σ(A'))).

Here Φ_A is evaluated with R̂_h, and it is a function of (R̂_h, R̂_{h'}) through the thresholds. Then

  P(blocks ≠ 𝒢) ≤ Σ_{{h,h'}∈𝒟} P((C\*) fails for (h,h')) + Σ_{(h,h') ordered, {h,h'}∉𝒟} E[ S_L(h,h') + S_N(h,h') ].

*Proof.* By Theorem A (A1, A3), blocks ≠ 𝒢 implies that (C\*) fails for some ordered group pair. For dependent pairs,
keep the event as it is. For an independent pair, suppose (C\*) fails at (A, A'): every |r̂_jk| on A × A' is
≥ s := max(σ(A), σ(A')).
- If A' = {k} is a leaf, this is a term of S_L(h, h'), with s = max(σ(A), f_k).
- If A is a leaf and A' is not, it is a term of S_L(h', h).
- If both are non-leaves, it is a term of S_N(h, h') (use any fixed k ∈ A').

In every case the event implies {∀ j ∈ A: |⟨u_j, u_k⟩| ≥ s} for one fixed k. By Lemma 3, conditionally on both
within-group matrices, (⟨u_j, u_k⟩)_{j∈A} =_d (⟨u_j, v⟩)_{j∈A} with v uniform. So the conditional probability is at
most Φ_A(s):
- *one pair:* the bound H₀(s);
- *sign union:* if all |⟨u_j, v⟩| ≥ s, put ε_j := sign⟨u_j, v⟩·sign⟨u_{min A}, v⟩. Then
  |⟨U_A ε, v⟩| = Σ_j |⟨u_j, v⟩| ≥ |A| s, and for each fixed ε, U_Aε/‖U_Aε‖ is a fixed unit vector given R̂_h.

Take expectations and apply the union bound. ∎

**Corollary C (fully analytic; PROVED).** Assume (IND) and |Σ_jl| ≥ ρ within groups, with all g_h = g.
Let K_g := (2g−1)g + (g−1)². For any grid τ₀ > τ₁ > … > τ_L = 0,

  P(blocks ≠ 𝒢) ≤ G(G−1) · K_g · [ H₀(τ₀) + Σ_{i<L} H₀(τ_{i+1}) · min{1, g(g−1) P_ρ(|r̂| < τ_i)} ].

*Proof.* Let μ := min(m_h, m_{h'}). Every threshold s appearing in S_L and S_N satisfies s ≥ μ:
- in S_L, s ≥ f_k ≥ m_{h'}, since a leaf is not a root and so π({k}) ≤ H_{h'};
- in S_N, s ≥ σ of the non-root member ≥ its m.

Hence S_L + S_N ≤ K_g H₀(μ). Split on {μ ≥ τ₀} and on {μ ∈ [τ_{i+1}, τ_i)}. Use H₀ decreasing, and
P(μ < τ) ≤ 2·C(g,2)·P_ρ(|r̂| < τ), by the union bound over the 2·C(g,2) within pairs of the two groups and Corollary 1. ∎

**Exponent.** The peeling sum behaves like exp(−n min_τ [I(τ; 0) + I(τ; ρ)]): a cross pair must beat a *deviant*
within-group correlation, so both deviations are paid. Let κ_C(ρ) := min_τ [I(τ;0) + I(τ;ρ)]. Then
**κ_C(ρ) = 2 I\*(ρ, 0) exactly** (PROVED):
- I(τ;0) + I(τ;ρ) = −log(1−τ²) − ½log(1−ρ²) + log(1−ρτ);
- its derivative 2τ/(1−τ²) − ρ/(1−ρτ) vanishes iff ρτ² − 2τ + ρ = 0, i.e. at τ = (1−√(1−ρ²))/ρ = t\*(ρ, 0);
- at that point I(t\*;0) = I(t\*;ρ) = I\*.

So Corollary C doubles Theorem B's exponent. The table is in `results/thmC_analytic.txt`. The asymptotic statement
"P ≤ poly(n, p)·e^{−n κ_C}" follows by taking a grid of mesh 1/n. That last step is a PROOF SKETCH, since the mesh
bookkeeping is not written out. The finite-n numbers do not depend on it.

**Remark (MC check of Theorem C).** `scripts/sharp_bound.py` evaluates E[S_L + S_N] by Monte Carlo over pairs of
group Gram matrices, with the exact H₀. The point estimate is far smaller (about 1e-21 per pair at ρ = 0.7,
n = 200). That estimate is not rigorous: E[S] is dominated by rare groups whose within correlations are low, so a
plain Monte Carlo average underestimates it. The MC-plus-Hoeffding upper bound coincides with Corollary C
(3.389e-9 in both at (200, 500, g = 8)). Only Corollary C is quoted as a bound.

---------------------------------------------------------------------------------------------------------

## 5. Counterexamples and boundaries (the lemma is false outside its hypotheses)

**CE1. g > B_n (COUNTEREXAMPLE, deterministic).** If some group has g_h > B, the cut always splits that group's node,
so blocks ≠ 𝒢 with probability 1, whatever the correlations. At the study's n = 200, B = 14. So the task's range
"9 ≤ g ≤ 16" fails for g ∈ {15, 16} at n = 200. The range is right only once B = 16, i.e. n ≥ 256 and p ≥ 256.
- At n = 200: valid g ∈ [8, 14].
- In general: g ∈ [⌊B/2⌋ + 1, B].

`sim_partition.py`: g = 15, 16 at n = 200 gave blocks ≠ groups in 50/50 replicates per cell. No algorithm change is
needed; the hypothesis must read g_max ≤ B(n, p).

**CE2. 2 g_min ≤ B (COUNTEREXAMPLE, deterministic for G ≥ 2).** Next-fit packing puts ⌊B/g⌋ ≥ 2 whole groups into
every bin, except possibly the last. So blocks ≠ 𝒢 surely. This is the study's own design (g = 5, B = 14). What
remains true, with the same probability bounds (Theorems B and C, which only use (A3)'s first part), is:

  **blocks are unions of whole groups**, with P ≥ 1 − (the bound of Theorem B or C).

*Which* groups share a block is decided by cross-group sample correlations. Those are σ(X)-measurable and independent
of ε, but they depend on the null columns. This is exactly W3-VEXP's GAP (b) ("partition–noise decoupling"), and it is
not addressed here.

**CE3. |ψ| > ρ (COUNTEREXAMPLE).** In LH with |ψ| > ρ, the hub pair (a, b) has r̂_ab → ψ almost surely while
f_a ≤ max_{l∈h(a)} |r̂_al| → ρ. So w.p. → 1, |r̂_ab| > max(f_a, f_b), and (C\*) fails at the leaf pair. Whether that
failure is visible in the blocks:
- With no early merge of two whole groups, A2 applies and the dendrogram is not laminar. Since ψ > ρ, the hub pair
  merges before either hub joins its group.
- Blocks ≠ 𝒢 is then observed in simulation (W3-VEXP row 17; here, ψ = 0.75: `results/sim_partition.txt`). The step
  "not laminar ⇒ blocks ≠ 𝒢" is not proved in general (Remark 2 of §1). The COUNTEREXAMPLE status rests on the
  reproducible simulation, and on the proved mechanism (the hub pair merges first).

**Finite-n boundary (not a counterexample to the lemma).** At n = 200 the lemma's probability is close to 1 only in
part of the parameter range. Recovery collapses below ρ ≈ 0.35 for independent groups of 10 (p = 1000). It also
collapses for the global factor with ρ = 0.5 and ψ = 0.2–0.3, and for LH as ψ → ρ (ψ = 0.65: about half the
replicates fail). See REPORT §4. These are the finite-n failures of an asymptotically true statement. **No small
algorithm change is needed for the stated regime.** The only failures that are not finite-n are hypothesis failures
(CE1–CE3).

---------------------------------------------------------------------------------------------------------

## 6. What is used from outside, and what is not proved

- Hotelling's exact density (classical). It is used only in Lemma 2, and checked numerically two independent ways.
- Gauss's ₂F₁(1) theorem and Wendel's inequality (classical).
- Nothing from the locked register is used.
- Not proved:
  - the mesh bookkeeping behind the κ_C asymptotic exponent (PROOF SKETCH);
  - "not laminar ⇒ blocks ≠ 𝒢" (false in general; Remark 2);
  - any statement about *which* groups share a block when 2g ≤ B (OPEN, W3-VEXP GAP b).
