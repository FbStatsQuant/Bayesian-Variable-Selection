# L4 — Key lemma of Tier 1 (claim (C2-R)): under the centre condition the LS0 path from S* is Π and ends certified at S₀

Status: **PROVED-CHECKED** (Tier 1: lemma checks, mid-point CONTINUE, sweep fixed, council round 2 passed — R09 Sol 8.8, R10 Opus 8.8, all gates PASS); key-lemma check R03 (Codex Sol xhigh, reviews/R03_L4_check_sol.md):
VERIFIED-WITH-AMENDMENTS, no fatal/major; items 1–3 applied (reviews/R03_disposition.md). Falsification numerics:
numerics/s1_exh/ + S1X_summary.txt and the tie-rule rerun s1_exh2/ + S1X2_summary.txt (0 exact ties) (15 complete-scan S5 paths: pure null deletion to S₀; best swap ≤ chosen deletion −
0.436 log n), numerics/s1_out/ (27 candidate-restricted paths), numerics/S3_summary.txt (gain formula; CC e-part along
the path); R03's own 24-path complete scan at n = 10¹⁴ incl. N₀ ≠ ∅ and m₀ = 0 (reported in R03).

Setting: STATEMENT v2 §1–3; (P_α) with α < 1/2; L1–L3. Notation: L1's (c_u, s_u²) are STATEMENT's (a_u, ψ_u); τ_j(T)
means τ_{j|T∖j} for j ∈ T and τ_{l|T} for l ∉ T. Fix δ ∈ (0, 1). The centre condition, as in STATEMENT v2 §3:
**CC_n(δ)**: for every set T_i of Π (k := |T_i|) and every T′ ∈ {T_i} ∪ {T_i ∖ j : j ∈ T_i ∖ S₀}:
  (H_q + κ₀|e_{T′}|)² ≤ (1 − δ)·Λ_k,  Λ_k := log n + 2 log((2p − k)/(k + 1)).
(Exact requirement: κ₀|e_{T′}| ≤ √((1 − δ)Λ_k) − H_q. If log p/log n → a, then at k ≍ p a positive leading-order
allowance for e requires a < (1 − δ)/2, and a ≤ (1 − δ)/2 is necessary at leading order; R03 item 3.)

**Lemma L4.** For n ≥ n₀(α, δ, ρ_b, ρ_w, q̄, ϑ, σ, s₀), on E_n ∩ CC_n(δ) the uncapped §6.10 search started at S*
coincides with Π: at every T = T_i ≠ S₀ (k = |T|, m := k − s₀ ≥ 1)
(a) the best null deletion has gain ≥ (δ/8) log n;
(b) every addition and every swap whose outgoing variable is a null has gain ≤ (best null deletion gain) − (δ/8) log n;
(c) every move that removes a truth (truth deletion, truth-out swap) has gain ≤ −c_θn;
hence the chosen move is the best null deletion (the move defining Π, same tie rule). After exactly m₀ moves T = S₀, and
every feasible neighbour of S₀ has strictly smaller F. LS0 with any cap a ≥ m₀ ends at S₀ as a certified search
endpoint; with a ≥ m₀ − 1 it scores S₀.

## L4.1 Thresholds (R03 item 1: bounded p allowed)
Put b_n := 2p/((n − 1)d) = o(1) (the determinant remainder of (L1.4.1), uniform for k ≤ p ≤ n^α). Uniformly for
T ⊇ S₀, |T| = k:
* null deletion from T: 2Δ(T, j) = 2 log((2p − k)/k) + log(n + 1) ± b_n ≥ Λ_k − b_n ((2p − k)/k ≥ (2p − k)/(k + 1));
* feasible addition to T (so k ≤ p − 1): 2Δ(T ∪ l, l) = 2 log((2p − k − 1)/(k + 1)) + log(n + 1) ± b_n ≥ Λ_k − 2/p − b_n
  (log(1 − 1/(2p − k)) ≥ −1/(2p − k − 1) ≥ −1/p);
* addition after a null deletion from T (base T ∖ j, size k − 1): 2Δ = 2 log((2p − k)/k) + log(n + 1) ± b_n ≥ Λ_k − b_n;
* log n − 2/p ≤ Λ_k ≤ log n + 2 log(2p) (at k = p, Λ_p = log n − 2 log(1 + 1/p)).

## L4.2 Statistics on E_n ∩ CC_n(δ)
For T = T_i and T′ as in CC: every null j retained in T has (L3 (c3), with R = T ∖ j) |τ_j(T)| ≤ H_q + κ₀|e_{T∖j}|, and
every null l ∉ T — including the nulls of N₀, which are outside from the start — has |τ_l(T)| ≤ H_q + κ₀|e_T| and, for
every retained **null** j ∈ T ∖ S₀, |τ_l(T ∖ j)| ≤ H_q + κ₀|e_{T∖j}|. Hence all of these (null j only; truth-removing
moves are handled separately in L4.4, R03 item 2) satisfy τ² ≤ (1 − δ)Λ_k. With ε from L3 (c4) (|ε| ≤ n^{−1/2}) and
M = ½(1 + η), |η| ≤ η_n (L3 (c1′)):
  M(τ + ε)² ≤ ½(1 + η_n)((1 − δ)Λ_k + 3n^{−1/2}Λ_k^{1/2}) ≤ ½(1 − δ/2)Λ_k  (n ≥ n₀).   (L4.2.1)
Also x := M(τ + ε)² = O(log n) uniformly, so the absolute corrections x²/ν of L1.4 are O((log n)²/n) = o(1).
(In L4.3 the o(1) terms absorb: the determinant remainder b_n, the multiplier error η_n·Λ_k-relative terms already in
(L4.2.1), the ε cross terms 3n^{−1/2}Λ_k^{1/2}, the log-nonlinearity x²/ν, and log((n + 1)/n); R08 suggestion.)

## L4.3 Proof of (a), (b)
(a) Let j be any retained null of T (exists since m ≥ 1). By L1.4, (L4.2.1) and L4.1:
G_del(j | T) ≥ Δ(T, j) − ½(1 − δ/2)Λ_k − o(1) ≥ ½Λ_k − b_n/2 − ½(1 − δ/2)Λ_k − o(1) = (δ/4)Λ_k − o(1) ≥ (δ/8)log n
for n ≥ n₀, since Λ_k ≥ log n − 2/p ≥ log n − 2 (the case k = p, the full model, included). (L4.3(b) in fact gives an addition margin of (δ/4) log n − o(1)
against the chosen deletion; δ/8 is claimed for uniformity with swaps; R10 suggestion 3.)
So the best null deletion G* satisfies G* ≥ (δ/8)log n.
(b) *Additions* of a null l ∉ T (the only variables outside T are nulls: T ⊇ S₀): by L1.4 and (L4.2.1),
G_add(l | T) ≤ −Δ(T ∪ l, l) + ½(1 − δ/2)Λ_k + o(1) ≤ −(δ/4)Λ_k + 1/p + o(1) ≤ −(δ/8)log n ≤ G* − (δ/8)log n
(n ≥ n₀; Λ_k = O(log n) makes the relative error of (L4.2.1) an additive o(1)).
*Null-out swaps* (j retained null out, l null in): F(T ∖ j ∪ l) − F(T) = G_del(j | T) + G_add(l | T ∖ j) (exact,
L1.4); T ∖ j ⊇ S₀, so the same computation at T′ = T ∖ j (size k − 1, the CC bound for τ_l(T ∖ j), L4.1) gives
G_add(l | T ∖ j) ≤ −(δ/8)log n, and G_del(j | T) ≤ G*. ∎(a,b)

## L4.4 Proof of (c): moves that remove a truth (TL)
Let T ⊇ S₀ with |T| ≤ p, j ∈ S₀, and T′ ∈ {T ∖ j} ∪ {T ∖ j ∪ l : l ∉ T}. We show F(T′) ≤ F(T) − c_θn on E_n.
*Bias.* (I − P_{T′})μ = ϑ_j(I − P_{T′})x_j (all other truths are in T′), and
‖(I − P_{T′})x_j‖² = (n − 1)(Σ_jj − Σ_{jT′}Σ_{T′T′}⁻¹Σ_{T′j}) ≥ (n − 1)d (L1.2(a) applied to T′ ∪ {j}).
*Noise cross term.* ⟨(I − P_{T′})x_j, e⟩ = σ√(n − 1)·r_j(T′ ∪ j) (the Gaussian residual of g_j given g_{T′}, exact Gram), and
|r_j(T′ ∪ j)| ≤ s_u|A_j(U)| + c_u|e_{T′}| ≤ L_n + G_n + 2L_n = O(√log n) on E1, E3, (c2) of L3.
*Residual sums.* RSS_{T′} = ‖(I − P_{T′})(μ + e)‖² ≥ ϑ_j²(n − 1)d − 2|ϑ_j|σ√(n − 1)O(√log n) + ‖e‖² − σ²gᵀΣ⁻¹g
≥ ‖e‖² + ϑ_j²(n − 1)d/2 − σ²(p + n^{2/3}) for n ≥ n₀, while RSS_T ≤ ‖e‖² (T ⊇ S₀). With Q_{T′} ≥ RSS_{T′}/s² and
Q_T ≤ RSS_T/s² + 2 (L1.4), and p ≤ n^α: Q_{T′} ≥ Q_T + c₃n, c₃ := ϑ²_min d/(4s²_max) > 0; Q_T ≤ n − 1 by
definition, so ψ_T ≤ n − 0.98 < n and ψ_{T′}/ψ_T ≥ 1 + c₃.
*Size terms.* |log w(|T′|) − log w(|T|)| ≤ log(2p) and |L(T′) − L(T)| ≤ 2 log(n + 1) + o(1) (L1.4, f ≤ log(n + 1)).
Hence F(T′) − F(T) ≤ log(2p) + log(n + 1) + o(1) − ν log(1 + c₃) ≤ −(n/4)log(1 + c₃) =: −c_θn. ∎(c)

## L4.5 End of the path and conclusion
By (a)–(c) the chosen move at every T_i ≠ S₀ is a null deletion of maximal gain (the move of Π; the production rule
"best scanned neighbour, exact ties → lexicographically smallest set" is applied to the same candidates as in Π's
definition, all other candidates being strictly smaller), with positive gain, so the search follows Π for m₀ moves to
S₀ (Π deletes one null per step, never a truth; CC_n(δ) is assumed for all of Π's sets). At S₀ (no retained null):
every addition has gain ≤ −(δ/8)log n by the computation of (b) (CC at T_i = S₀, k = s₀), every truth deletion and
truth-out swap has gain ≤ −c_θn by (c), and there are no other feasible neighbours; so S₀ is a strict local maximum.
Caps: single-search prefix property (FACB STATEMENT §1, from the loop rule (L3) of FINAL `s7_impl.tex`). ∎(L4)

## L4.6 Remarks
1. Nothing about the order of deletions, gap structure or within-group jumps is used: for α < 1/2 the union bound E_A
   over all (null, mate-set) pairs controls every group part, and CC_n controls the only cross-group quantity. This is
   why Tier 1 is short; all difficulty is in CC_n (Tier 2, Lemma KL).
2. On lattice sets (not path sets) κ₀|e_T| can be ≈ √(2 log(p/m)) (one-sided retained sets); then the sufficient estimate
   used in (b) fails as soon as log p/log n > 1/6. FACA Prop SHARP proves, for exact compound symmetry, that full-lattice NA fails above 1/6 (an explicit
   addition witness F(T ∪ l) > F(T), `W2-FAC-A/lemmas/L6_sharp.md`); it does not compare a swap with the best deletion, and
   no sharpness of any kind is claimed here for BCS/S5 (R05 item 2, R06 item 5). Conversely, the crude all-set bound |e_R| ≤ G_n + 2L_n (L3 (c2)) already gives P̃(CC_n(δ)) → 1 when
   2a*(1 + κ₀)² < 1 − δ, a* := limsup log p/log n (S5: a* < 0.104 for small δ) — a non-vacuity witness below 1/6 (R05).
3. The legacy cap ℓ_n misses S₀ when m₀ ≥ ℓ_n + 2, as in FACB L5.2 (start = S*, m₀ moves needed).
