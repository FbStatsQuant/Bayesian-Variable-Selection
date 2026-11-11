# L1 — Form F: bridges (B1)–(B4), (B6) and Theorem RM-F (claim (C1))

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses; lemma check R03
(Codex gpt-6.1-sol high, `../reviews/R03_L0L1L2_check_sol.md`): B1, B2, B3, B3′, B4, B6, RM-F VERIFIED; Lemma B1′ and
the τ-variant `L1b_rss.md` were added after R03 and checked by R06 (Codex gpt-6.1-sol high,
`../reviews/R06_batch2_check_sol.md`: VERIFIED-WITH-AMENDMENTS, applied) [R08-17]. Setting F and
notation: `../STATEMENT.md` §1, §3.1. Sources: GROW `lemmas/L0_toolkit.md`, `L2_NA_TL.md`, `L3_sandwich.md`
("PROVED (by this seat, unchecked)"; checks R03 "VERIFIED" / "VERIFIED-WITH-AMENDMENTS", R02 "VERIFIED");
LOC2 `lemmas/L1_toolkit.md` (Lemma L0′; "PROVED (by this seat, unchecked)"; R02 "VERIFIED-WITH-AMENDMENTS").

## (B1) Partition-free conditions imply the block-relative ones

**Naming [R06-3].** STATEMENT v1.2 writes (L-gain), (L_b) for the τ²_U-normalised conditions. Their v1.1 forms with
σ² in place of τ²_U are written **(L-gain^σ)**, **(L_b^σ)** here; (L_b^σ) is GROW (G3c) verbatim, and
(L-gain^σ) ⇒ (L-gain), (L_b^σ) ⇒ (L_b) because τ²_U ≥ σ². The τ-form does not imply GROW (G3c).

**Lemma B1.** Let C₁, …, C_J be any partition of [p] with |C_b| ≤ 16. Then (FL-16) ⇒ GROW (G3a); (V) ⇒ (V_b) = GROW
(G3b); (L-gain^σ) ⇒ (L_b^σ) = GROW (G3c); and (L-gain) ⇒ (L_b) (τ-forms) — all with the same constants (φ₀, M_n, η, Q).

*Proof.* (G3a) asks λ_min(R̂_T) ≥ φ₀² for nonempty T ⊆ C_b: such T has 1 ≤ |T| ≤ 16, so (FL-16) applies.
(G3b) asks δ²_{U,j} ≥ M_n log n for j ∈ S₀ and U ⊆ C_{b(j)} ∖ {j}: then U ⊆ [p] ∖ {j} and |U| ≤ 15 (U may contain
other truths; (V) allows that), so (V) applies; u_{U,j} exists by (FL-16) applied to U ∪ {j}. (G3c) asks
δ²_{U,l} ≤ ησ² log n for l ∉ Q and U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}: then U ⊆ [p] ∖ {l} and |U| ≤ 15, so
(L-gain^σ) applies (the extra requirement U ⊇ S₀ ∩ C_{b(l)} only restricts the U's that (G3c) quantifies over). The
τ-form is the same argument with the bound ητ²_U log n: the quantifiers over (U, l) are identical. ∎

**Lemma B1′ (converse over all partitions).** If (G3a), (V_b), (L_b) hold for **every** partition of [p] into blocks
of size ≤ 16 (with common φ₀, M_n, η, Q), then (FL-16), (V), (L-gain) hold; the same with (L_b^σ), (L-gain^σ). So the partition-free conditions are
exactly "the block-relative conditions for every admissible partition".
*Proof.* Given T with 1 ≤ |T| ≤ 16, choose a partition having T as a block: (G3a) gives the floor. Given j ∈ S₀ and
U ⊆ [p] ∖ {j}, |U| ≤ 15, choose a partition with the block U ∪ {j}: (V_b) gives δ²_{U,j} ≥ M_n log n. Given l ∉ Q and
U ⊆ [p] ∖ {l}, |U| ≤ 15, choose a partition with the block C := U ∪ {l}; S₀ ∩ C = S₀ ∩ U ⊆ U because l ∉ Q ⊇ S₀, so
(L_b) applies to (U, l). ∎

**Why the block-relative forms are weaker, and the only reason blocks appear.** (L_b) quantifies only over U that
contain all truths of l's own block. A column l whose marginal gain is large but vanishes once a truth j is
conditioned on is harmless if the method puts l and j in the same block (then every relevant U contains j);
otherwise it may have to be included in Q for the leakage condition to hold (whether it is actually selected by the
start mode depends on the score comparisons) [R08-13]. A partition-free condition cannot use this, so (L-gain) asks
every such column to be in Q. The same remark applies to (V_b): only conditioning sets inside the
truth's block matter. Conversely the partition-free forms need no knowledge of the clustering output.

## (B2) SAND-F: the sandwich for log|Q| = o(log n)

**Lemma B2.** Setting F. Assume ‖μ‖² ≤ Mn, p ≤ n^A, a partition with blocks ≤ 16 that is a deterministic function of X,
(G3a), (V_b) with M_n → ∞, (L_b^σ) (= GROW (G3c)) with η < η_A, a deterministic Q ⊇ S₀ with (L-feas), and
log|Q| = o(log n). Then
P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω) → 1.

*Proof (delta to GROW L3).* GROW Lemma L3 (`L3_sandwich.md:13`) is this statement with "|Q| ≤ C_Q log n" in (G1)
(`L3_sandwich.md:6`). Its proof uses |Q| at exactly the following places (R01 item 4 lists the same):
1. `L3_sandwich.md:36-38`: k₀ := |Q| + 16s₀ in the counting inequality (3.2) — a definition; no size bound used.
2. `L3_sandwich.md:64-72`, the ladder m_i = 2^{i+1}k₀: the bound uses only k₀ ≥ 1 (it discards the factor
   k₀^{−ε₂/(1+ε₂)} ≤ 1) and p ≤ n^A; the block event family (`L3_sandwich.md:17-26`) consists of sets of size ≤ 16 and has ≤ 2^{16}p
   members, independent of |Q|.
3. `L3_sandwich.md:78-79`: feasibility — if Q = [p] and k̃ = K then K = p and S̃ = [p]; otherwise k̃ ≤ 2k₀ =
   2|Q| + 32s₀ < K by the second alternative of (L-feas). No size bound used.
4. `L3_sandwich.md:88-93`, junk exclusion: the final display is
   [½ − η/2 − √(2Aη)] log n − o(log n) − log k̃ − 2κ_E > 0, and the source uses log k̃ = O(log log n). With
   k̃ ≤ 2k₀ = 2|Q| + 32s₀ and log|Q| = o(log n) we have log k̃ = o(log n), which is all the display needs
   (½ − η/2 − √(2Aη) > 0 is a fixed positive constant because η < η_A).
Nothing else in `L3_sandwich.md` depends on |Q| (the toolkit L0 is applied to the block family only). ∎

Under (L-size), log|Q| ≤ κ log log n = o(log n). So with Lemma B1, (FL-16), (V), (L-feas) and (L-gain^σ) give
[SAND(Q)] for every partition with blocks ≤ 16 by Lemma B2; with the weaker τ-form (L-gain) of STATEMENT v1.2 the same
conclusion is Lemma B2τ (`L1b_rss.md`), which is what Theorem RM-F uses.

## (B3) TL-F: truth removal on a polylogarithmic lattice under BM-Q

**Lemma B3.** Setting F. Assume ‖μ‖² ≤ Mn, p ≤ n^A, deterministic Q ⊇ S₀ with |Q| ≤ K and q := |Q| ≤ (log n)^κ,
(FL-Q), and (BM-Q): θ*²_min nφ₀²/(σ²(q + log n)) → ∞. Then P(TL(𝓛)) → 1.

*Proof (delta to GROW L2.1 through LOC2 L0′).* Let 𝔉 be the lattice family of GROW L2.0 (`L2_NA_TL.md:11-17`):
|A| ≤ q + 1, |𝔉| ≤ 1 + 2^{|Q∖S₀|}(1 + p + s₀ + s₀p), Gram floor φ₀² on nonempty members by (FL-Q) and interlacing,
𝒱𝒱 := {r_A − r_{A′}} ∪ {r_A}, |𝒱𝒱| ≤ 2|𝔉|². By LOC2 `L1_toolkit.md:28-32` Lemma L0′ applies (envelope exponent κ + 1),
with t_n = 4(log|𝔉| + 2 log n + q + 1) and h_n² = 2(log|𝒱𝒱| + log n) defined from the actual cardinalities, so

  t_n + h_n² ≤ C₁(q + log n),  C₁ = C₁(A, s₀),                                                           (1.1)

and the event 𝓔_n := 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃ has P(𝓔_n) → 1. On 𝓔_n, for T ∈ 𝓛, i ∈ S₀ and A = T ∖ {i} or (T ∖ {i}) ∪ {l}
(l ∉ T), exactly as in `L2_NA_TL.md:27-31`: r_A = θ*_i(I − P_A)x_i, Λ_A ≥ (n − 1)φ₀²θ*²_min =: L′_n ((FL-Q), Schur
complement; A ∪ {i} ⊆ Q ∪ {l}), Λ_T = 0, and
  RSS_A − RSS_T ≥ Λ_A − 2σh_n√Λ_A − σ²t_n ≥ Λ_A/2 − 2σ²h_n² − σ²t_n.
[NEW: the scale.] By (1.1) and (BM-Q), L′_n/(σ²(t_n + h_n²)) → ∞, so 2σ²h_n² + σ²t_n ≤ Λ_A/4 for n ≥ n₀ and
RSS_A − RSS_T ≥ Λ_A/4. (The source has t_n, h_n² = O(log n) and BM-∞; LOC2 `L1_toolkit.md:33-36` has a fixed θ_lo. The
inequality needs exactly Λ_A ≥ 4σ²(2h_n² + t_n).) The final comparison of `L2_NA_TL.md:32-34`,
  F(A) − F(T) ≤ (A + 1) log n + 1 + 2κ_E − L′_n/(8C_R) < 0 for n ≥ n₀,
needs L′_n/log n → ∞, which (BM-Q) contains. ∎

**Corollary B3′.** If q ≤ C log n (in particular under (N-χ), where q ≤ s₀ + log n), BM-∞ implies (BM-Q), and
Lemma B3 is GROW L2.1.

## (B4) NA-χ

**Lemma B4** (= GROW L2.2 + L2.3(a), `L2_NA_TL.md:38-66`). Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, deterministic Q ⊇ S₀ with
|Q| ≤ K, (FL-Q) and (N-χ): |Q ∖ S₀| ≤ (1 − δ₀) log n. Then, with c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2
(κ_E the remainder constant of the score expansion, GROW `lemmas/L0_toolkit.md:19-20`) [R08-14],
P(max_{T∈𝓛, l∉T} Z²_{T,l} ≤ c_n) → 1 and P(NA(𝓛)) → 1.
(The source's hypothesis |Q| ≤ C_Q log n holds with C_Q = s₀ + 1.) No change. [R07-4] Convention for all NA bridges: if
Q = S₀ = [p] there is no pair (T, l), NA(𝓛) holds vacuously, and "max over pairs ≤ c_n" is read as the universal
inequality over (the empty set of) pairs.

## (B6) POST-F
(T1-F) = (H0) ⇒ 1 − π(S₀) = O_P(√(log n/n)) (T03♯, "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"), and
1 − π(S₀) ∈ [0, 1], so E[1 − π(S₀)] → 0: [POST].

## Theorem RM-F (claim (C1))

Setting F, the method as coded, premises and configuration of STATEMENT §1. Assume (T1-F), (FL), (V), (L), (N).

*Proof.* (T1-F) contains ‖μ‖² ≤ Mn, p ≤ n^A and BM-∞. [SAND(Q)]: Lemma B1 and Lemma B2 in its τ-form, Lemma B2τ of
`L1b_rss.md` (STATEMENT v1.2 states (L-gain) with τ²_U; with σ² in place of τ²_U, Lemma B2 itself applies); the coded
partition is a deterministic function of the fixed X. [TL(Q)]: under (N-χ), Corollary B3′; under (N-D), Lemma B3 with (N-D)(ii).
[NA(Q)]: under (N-χ), Lemma B4; under (N-D), Lemma NA-F (`L2_NAF.md`). [POST]: (B6). Theorem RM-0 (`L0_core.md`) with
this Q (|Q| ≤ K by (L-feas)) gives all conclusions. The block-relative variant: replace Lemma B1 by the hypotheses
(V_b), (L_b), (G3a) themselves (Lemma B2τ consumes exactly these). Move count under (N-χ): on Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛), RM-0(a) gives exactly
|S̃₀ ∖ S₀| ≤ |Q ∖ S₀| ≤ (1 − δ₀) log n < log n moves. ∎

**Relation to Theorem GROW.** GROW (`lemmas/00_MAIN.md`) is the block-relative variant with |Q| ≤ C_Q log n and
(G4-χ) or (G4-dir). RM-F (i) states the hypotheses partition-free (Lemma B1), (ii) replaces e4 by Lemma E4,
(iii) extends the size to (log n)^κ under (N-D) (Lemmas B2, B3, NA-F), (iv) states the conclusion for all run
parameters simultaneously (RM-0(b)). `implies`: RM-F with (N-χ) or with (N-D)(i) at ρ_n = 0 and |Q| ≤ C log n
⇐ GROW's hypotheses in block-relative form; GROW's instances (C5)(a), (b) are instances of RM-F (`L7_examples.md`).
