# O-DILUTE — statements and proofs

Branch `theory/O-DILUTE`, 2026-11-02. Notation: `00_COMMON.md`, METHODOLOGY_v3 §§5, 6.3, the locked T22 STATEMENT
(`Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md`), and F-DRAFT `NEW_TARGETS.md` §0. Every proof here is a
**candidate**: it has not been reviewed or adopted. Status words follow the campaign PROTOCOL.

## 0. Objects and new symbols

- Partition C₁, …, C_J (the v3 partition, X-dependent; every statement below holds for **any** partition with |C_b| ≤ K
  unless said otherwise). S_b := S ∩ C_b, S₀_b := S₀ ∩ C_b, s₀ = |S₀| ≤ K.
- Tables r_b(U) = BF(U), U ⊆ C_b (v3), or any positive tables when said so. γ₀(S) = w(|S|) ∏_b r_b(S_b) on Ω
  (W_K cancels in π₀ and is dropped), Z̄₀ = Σ_Ω γ₀, π₀ = γ₀/Z̄₀.
- **Tilt.** For t > 0: e_b(t) := Σ_{U⊆C_b} r_b(U) t^{|U|}; the *tilted block law* π_b^t(U) := r_b(U) t^{|U|}/e_b(t);
  P_t := ⊗_b π_b^t (independent blocks), N := Σ_b |S_b| under P_t.
- **Size correction.** g_t(k) := log w(k) − log w(s₀) − (k − s₀) log t, A_t(k) := π₀(|S| = k)/P_t(N = k).
- **Block visibility and competition** (blocks with S₀_b ≠ ∅): λ_b := log r_b(S₀_b) + |S₀_b| log t, and
  η_b := [e_b(t) − 1 − e^{λ_b}]/(1 + e^{λ_b}) ≥ 0; for blocks with S₀_b = ∅: η_b := e_b(t) − 1.
  softplus(x) := log(1 + eˣ).
- **Prior odds interval at s₀.** I₀ := [w(s₀)/w(s₀−1), w(s₀+1)/w(s₀)] = [s₀/(2p − s₀), (s₀+1)/(2p − s₀ − 1)];
  t₀ := (s₀+1)/(2p − s₀ − 1) ∈ I₀ (the value used in all numerics).
- **Near-truth region** (T37): R_d = {U ∪ P : U ⊆ S₀, P ∩ S₀ = ∅, |P| ≤ d}; **Hamming ball** B_d = {S : |S Δ S₀| ≤ d}.
- **Dilution quantities** (population; standardised columns, Σ = population correlation, θ = cβ, σ² = 1):
  v := σ² + θᵀΣθ (Var y); ρ_j := (Σθ)_j/√v (population marginal correlation of x_j with y);
  x_j := θ_j² Var(x_j | x_{S₀∖j}) / (σ² + θ_j² Var(x_j | x_{S₀∖j})) (population partial R² of j given S₀∖j, the
  posterior's keep-j statistic); κ_j := 1 − ρ_j²/x_j (the **dilution fraction** of truth j; under population block
  orthogonality with independent truths κ_j = Σ_{k≠j}θ_k²/v, F-DRAFT's κ_b at T = ∅ with j's own signal removed);
  ω_j := θ_j²/θᵀθ (the **signal share**; the c → ∞ limit of ρ_j² for independent truths).
- Single-variable Bayes factor (any standardised column x, W3-VEXP Prop D): with H := (n+1)(n−1) + 1,
  BF₁(r²) := (H/n)^{−1/2} [(2b₀ + Q(r²))/(2b₀ + n − 1)]^{−ν}, Q(r²) := (n−1)(1 − n(n−1)r²/H). BF({x}) = BF₁(r_xy²),
  strictly increasing in r_xy². With a known plug-in s²: BF₁^{s²}(r²) := (H/n)^{−1/2} exp{n(n−1)² r²/(2H s²)}, also
  strictly increasing.

## 1. Theorem E (exact block factorisation of the start). Status: **PROVED**

For every data set, every partition with |C_b| ≤ K, all positive tables, every t > 0 and every S ∈ Ω,

    π₀(S) = [∏_b π_b^t(S_b)] · A_t(|S|),     A_t(k) = π₀(|S| = k) / P_t(N = k) = e^{g_t(k)} / E_t[e^{g_t(N)} 1{N ≤ K}],

and in particular, at S = S₀ (where g_t(s₀) = 0):

    log π₀(S₀) = Σ_b log π_b^t(S₀_b) + log A_t(s₀),     A_t(s₀) = 1 / E_t[e^{g_t(N)} 1{N ≤ K}].            (E)

*Proof.* For S ∈ Ω, γ₀(S) = w(k) ∏_b r_b(S_b) = w(k) t^{−k} ∏_b e_b(t) · ∏_b π_b^t(S_b) with k = |S|. Summing over Ω,
Z̄₀ = ∏_b e_b(t) · Σ_{k≤K} w(k) t^{−k} P_t(N = k). Dividing, π₀(S) = ∏_b π_b^t(S_b) · w(k)t^{−k}/Σ_{k′≤K} w(k′)t^{−k′}P_t(N = k′).
Summing the same identity over |S| = k gives π₀(|S| = k) = P_t(N = k) · w(k)t^{−k}/Σ_{k′}(…), so the factor is A_t(k).
At k = s₀ write w(k′)t^{−k′} = w(s₀)t^{−s₀}e^{g_t(k′)}. ∎

**Corollary E1 (three deficits). PROVED.** With λ_b, η_b as in §0,

    −log π₀(S₀) = Σ_{b: S₀_b≠∅} softplus(−λ_b)  +  Σ_b log(1 + η_b)  −  log A_t(s₀)
                =        V_t (visibility)        +     C_t (competition)  +  (size correction).

*Proof.* For S₀_b ≠ ∅, e_b(t) = 1 + e^{λ_b} + (rest) = (1 + e^{λ_b})(1 + η_b), so log π_b^t(S₀_b) = λ_b − log(1+e^{λ_b})
− log(1+η_b) = −softplus(−λ_b) − log(1+η_b). For S₀_b = ∅, log π_b^t(∅) = −log e_b(t) = −log(1+η_b). Insert in (E). ∎

V_t is the price of truths that their own block does not see (λ_b < 0); C_t is the mass the block tables put on
everything that is neither ∅ nor S₀_b (nulls, proxies, partial subsets of S₀_b); the size term is the non-product part of
the BB(1, p) prior.

**Corollary E2 (rigorous ceiling). PROVED.** If t ∈ I₀ then g_t ≥ 0 on {0, …, K}, so A_t(s₀) ≤ 1/P_t(N ≤ K) and

    log π₀(S₀) ≤ −V_t − C_t − log P_t(N ≤ K) ≤ −Σ_{b: S₀_b≠∅} softplus(−λ_b) − log P_t(N ≤ K).

*Proof.* log w(k) − log w(k−1) = log(k/(2p − k)) is strictly increasing in k, so log w is convex on {0, …, p}; a line
through (s₀, log w(s₀)) with slope log t ∈ [log(w(s₀)/w(s₀−1)), log(w(s₀+1)/w(s₀))] is a supporting line, i.e.
g_t(k) ≥ 0 for all k. Then E_t[e^{g_t(N)}1{N≤K}] ≥ P_t(N ≤ K). ∎

*Remarks.* (a) The ceiling sharpens W3-VEXP's Prop D (which keeps only the e^{λ_b} part of each invisible block, since
softplus(−λ) ≥ max(0, −λ)). (b) In the numerics P_t(N ≤ K) = 1 to machine precision (the start's size sits near 5),
so the ceiling is −V − C; the size term log A_t is ≤ −0.29 nats in all 480 fits (it always *lowers* π₀(S₀)): P_t sits at N ≈ 5 < s₀,
where g_t(N) ≈ Σ_{i=N}^{s₀−1} log[(s₀+1)/(i+1)] > 0.

## 2. Theorem R (exact near-truth and Hamming mass). Status: **PROVED**

Let f_b(u, v) := Σ_{U⊆C_b} r_b(U) u^{|U∩S₀|} v^{|U∖S₀|} and F(u, v) := ∏_b f_b(u, v) = Σ_{i,j} F_{ij}u^iv^j. Under π₀ the
pair (I, M) := (|S ∩ S₀|, |S ∖ S₀|) has the exact law P(I = i, M = j) = w(i + j)F_{ij} 1{i+j≤K}/Σ_{i′+j′≤K} w(i′+j′)F_{i′j′}.
Hence, exactly, π₀(R_d) = P(M ≤ d), π₀(B_d) = P(s₀ − I + M ≤ d), π₀(S₀) = w(s₀)∏_b r_b(S₀_b)/Z̄₀, and
π₀(R_d) ≥ 1 − E_{π₀}[M]/(d + 1) (Markov). *Proof.* γ₀ depends on S only through |S| and the block sub-models, so summing
γ₀ over {S: I = i, M = j} gives w(i+j)F_{ij}. ∎ (Computable by a two-variable convolution over blocks: §6.3's size
convolution with one extra counter; `scripts/dilute.py::start_summary`, checked against brute force in `results/sanity.txt`.)

Note R_d ⊇ 2^{S₀}: π₀(R_d) counts every subset of S₀ as near the truth, however many truths it misses. B_d does not.

## 3. Lemma N (the v3 null table is exactly calibrated in Gaussian designs). Status: **PROVED**

Let the raw column x_l^r ~ N(0, s²I_n) be independent of (y^r, X_{−l}^r) (true for every null of S1, every null of a
truth-free group in S3/S4/S6, and for every null whose population correlation with all truths is 0). Then, conditionally on
(y, X_{−l}), r_ly² ~ Beta(½, (n − 2)/2) exactly. Hence r_b({l}) = BF₁(r_ly²) has a law that does not depend on the signal
scale c, on σ², on θ, or on the other blocks; the v3 table scores a null exactly as it would score it in a pure-noise data set.

*Proof.* With C the centring matrix, u := Cy/‖Cy‖ is fixed given y; Cx_l^r is N(0, s²C), i.e. rotationally invariant in the
(n − 1)-dimensional range of C, so (uᵀCx_l^r)²/‖Cx_l^r‖² ~ Beta(½, (n−2)/2) and standardisation does not change r_ly. ∎

**Corollary N1 (null inclusions are O(1) at any signal scale).** Under P_t with t ∈ I₀ or smaller, the expected number of
null inclusions from truth-free blocks is ≤ t Σ_l BF₁(r_ly²) with r_ly² iid-like Beta(½, (n−2)/2); BF₁(r²) ≈ n^{−1/2}e^{(n−1)r²/2},
whose sum over m nulls is m·n^{−1/2}·Θ_P(√(log m)) (index-1 heavy tail: E[e^{χ²₁/2}1{χ²₁ ≤ 2log m}] = 2√(log m)/√π). So the
null count is Θ_P(t m √(log m)/√n) = Θ_P(s₀√(log p)/√n): **about 1 at the study size**, independent of c. Status:
PROVED for the expectation bound given the Beta law; the heavy-tail sum asymptotics are standard (PROOF SKETCH for the
in-probability constant).

## 4. Lemma L (a common plug-in σ² inflates every null by the dilution factor). Status: **PROVED** (identity) +
## PROOF SKETCH (extreme-value consequence)

(a) [identity] For a known-s² table, log r_b({x}) = −½ log(H/n) + n(n−1)² r_xy²/(2H s²) ≈ −½ log n + (n−1)r_xy²/(2s²), for
truths and nulls alike. With the oracle s² = σ²/s_y² = (1 − R²_pop)(1 + O_P(n^{−1/2})) and Lemma N, a null's exponent is
χ²₁/(2(1 − R²_pop)) instead of the v3 table's ≈ χ²₁/2: an inflation by v/σ² (≈ 7 at c = 0.5, ≈ 25 at c = 1).

(b) [consequence] The expected number of null inclusions is ≥ t max_l BF₁^{s²}(r_ly²) ≈ t n^{−1/2} p^{1/(1−R²)}, which is ≫ K
whenever p^{R²/(1−R²)} ≫ √n·K (every study cell, by tens of orders of magnitude). The known-σ² start then fills to the cap.

(c) [why F-DRAFT's Lemma W1 does not transfer] W1 assumes **in-sample** block orthogonality X_{C_b}ᵀX_{C_b′} = 0. The study's
S1/S3/S4/S6 are block-orthogonal only **in population**. In a Gaussian design, x_lᵀX_{−b}θ_{−b}/√(n−1) ~ N(0, ‖θ_{−b}‖²(1+o(1)))
for a null l: the out-of-block signal leaks into every block's sufficient statistic with variance ‖θ_{−b}‖², the same
amount by which the v3 table "dilutes". Seen from a truth, the v3 table's own-σ² integration *dilutes*; seen from a null,
it *calibrates* the leakage (Lemma N). Under exact in-sample BO the null exponent of the v3 table is (1 − κ)χ²₁/2 (F-DRAFT
W2/W5) and the known-σ² table is exact; under population BO it is χ²₁/2 and the known-σ² table over-rewards nulls by v/σ².
In-sample check: the W1 formula for d(S₀) is undefined (Σ_b ξ_b ≥ 1, impossible under in-sample BO) in a large fraction
of fits and differs from the actual d(S₀) by tens of nats where defined (REPORT §4).

## 5. Proposition S (ranking ceiling, for every common table variance). Status: **PROVED**

Let U ⊆ S₀ be the truths that are alone (among S₀) in their block, and F the truth-free blocks. For j ∈ U let
M_j := #{b ∈ F : max_{l∈C_b} r_ly² ≥ r_jy²}. Order U so that r²_{j₍₁₎y} ≥ r²_{j₍₂₎y} ≥ … . Then for the v3 tables **and** for
the known-s² tables with **any** s² > 0,

    π₀(S₀) ≤ 1 / ∏_i (1 + [M_{j₍ᵢ₎} − (i − 1)]₊).

*Proof.* Both tables give single-variable sub-models a score that is the same strictly increasing function of r_xy² for every
column (standardised columns have G = n − 1, so the determinant factor is common). Process j₍₁₎, j₍₂₎, … in order; for each
choose "keep j₍ᵢ₎" or "replace j₍ᵢ₎ by the best null of one F-block counted in M_{j₍ᵢ₎} and not chosen before" (at least
M_{j₍ᵢ₎} − (i−1) choices, since the candidate sets are nested increasing in i). Each choice sequence gives a distinct model S′
with |S′| = s₀ and γ₀(S′)/γ₀(S₀) = ∏ r_{b(l)}({l})/r_{b(j)}({j}) ≥ 1 (each replaced truth's block goes from {j} to ∅, each
chosen F-block from ∅ to {l}; all other blocks unchanged). So Z̄₀ ≥ (count)·γ₀(S₀). ∎

*Meaning.* A common σ² rescales truths and nulls by the same factor, so it moves the inclusion threshold but not the
ranking; the start can be favourable only if the marginal statistics separate the truths from the nulls of other blocks.
At n = 200 they do not: the per-cell median ceiling is 10^{−0.8}–10^{−4.8} (10^{−6.7}–10^{−10.6} in S5) on the
regenerated data (REPORT §5, `results/propS.txt`). So no choice of a common σ² can give π₀(S₀) above ≈ 0.02–0.15 in a
typical study fit. Prop S is a ceiling only; the actual v3 values are 10–20 orders of magnitude lower.

## 6. Proposition D′ (finite-n dilution formula). Status: **PROOF SKETCH** (population limit), numerics in REPORT §3

Setting: Gaussian design, population block orthogonality on the realised partition (W3-VEXP: exact for S1/S3/S4/S6), a truth
j alone in its block. Then

(a) λ_j = log BF₁(r_jy²) + log t, with √(n − 3)(atanh r_jy − atanh ρ_j) →_d N(0, 1), i.e. (n−1)r_jy² ≈ W_j ~ χ²₁(nρ_j²) and

        λ_j ≈ ½W_j − ½ log n − log((2p − s₀ − 1)/(s₀ + 1)).

(b) [dilution = W2 for truths] ρ_j² = (1 − κ_j) x_j, so the table's keep-j gain −ν log(1 − ρ_j²) is the posterior's
    gain −ν log(1 − x_j) scaled by log(1 − (1−κ_j)x_j)/log(1 − x_j) ≤ 1 − κ_j (first order: exactly Lemma W2's factor).
(c) [saturation] ρ_j² = c²θ_j²/(σ² + c²‖θ‖²) increases to ω_j as c → ∞: **no signal scale makes the start favourable at
    fixed n**; truth j is start-visible in population iff (n/2)·(−log(1 − ρ_j²)) > ½ log n + log((2p−s₀−1)/(s₀+1)) (+O(1)).
(d) [assembled] log π₀(S₀) ≈ −Σ_{j∈S₀} E softplus(−λ_j) − Σ_l log(1 + t BF₁(r_ly²)) + log A_t, the three terms of
    Corollary E1 with product blocks (independent λ_j, Lemma N for nulls). Blocks with proxies (S3, S4, S6) add
    competition from the proxies of j, which (d) omits; blocks with ≥ 2 truths use λ_b of the pair.

*Sketch.* (a) Fisher's z for a bivariate Gaussian pair (x_j, y) with correlation ρ_j (y is Gaussian given the design law);
log BF₁ is smooth; (b) algebra from the definitions; (c) monotonicity of c²a/(1 + c²b); (d) Corollary E1, with the λ_b of
different blocks asymptotically independent under population BO (cross-block sample correlations O_P(n^{−1/2}) enter λ_b
through ρ̂_j only at relative order n^{−1/2}). Not every step is verified: the joint (not marginal) law of the λ_j and the
treatment of the BB-size coupling inside (d) are approximations, checked numerically only.

## 7. Paper proposition (proposed wording)

**Proposition DM (start masking by σ²-dilution at finite n).** Let the block tables score each sub-model against the full
response (v3 §6.3). For every data set and partition:

(i) [exact] −log π₀(S₀) = V_t + C_t − log A_t(s₀), with V_t = Σ_b softplus(−λ_b) the cost of truths their own block does not
    see, C_t ≥ 0 the block mass on non-truth sub-models, and −log A_t(s₀) ≥ −log P_t(N ≤ K) ≈ 0 for t ∈ I₀; in particular
    π₀(S₀) ≤ ∏_{b: S₀_b ≠ ∅} σ(λ_b) / P_t(N ≤ K).
(ii) [ranking] π₀(S₀) ≤ 1/∏_i(1 + [M_{j₍ᵢ₎} − i + 1]₊) for the v3 tables and for any common plug-in σ².
(iii) [near-truth] π₀(R_d) = P(M ≤ d) ≥ 1 − E_{π₀}[M]/(d + 1), where M counts non-truths in S.
In Gaussian designs that are block-orthogonal in population, a truth alone in its block has λ_j ≈ ½χ²₁(nρ_j²) − ½ log n
− log(2p/s₀), with ρ_j² = (1 − κ_j)x_j ≤ ω_j (dilution; saturating in the signal scale), while every null of a truth-free
block has λ_l ≈ ½χ²₁ − ½ log n − log(2p/s₀) exactly in law (Lemma N). At the study's n = 200, s₀ = 14, p ∈ {500, 1000}, about
half of the truths have λ_j < 0 (V_t ≈ 20–50 nats) while E_{π₀}[M] ≈ 0.7–3.8: the per-cell median π₀(S₀) is
10^{−11}–10^{−26} while π₀(R₂) has median 0.79 (0.2–0.96 per cell; lowest in S4, where the start keeps proxies of truths,
which R_d counts as extras).
This is the regime of T38(b): the start is masked, but its mass is on the near-truth region R_d — through **subsets** of S₀
that are 6–11 additions from S₀ — so delivery must come from the bridge and the Gibbs/addition moves, not from iid start
draws.
