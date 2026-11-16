# R2 — Necessity at the level log n + 2 log p: NEC-b⁺⁺ (C2⁺⁺), NEC⁺⁺ (T4⁺⁺), Corollary F4⁺⁺

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of BASE := `Theory_work/Wave3/W3-START/` (v1.3.4); PARENT `path:lines` is a file
of PARENT := `Theory_work/Wave3/W3-START2/` (v1.4.1); a path with neither word is this ticket's. Both parents are read-only.
Statement proved: `STATEMENT.md:145-152` [NEC-b] (C2⁺⁺)(i), (ii), fixed and drifting constants; `STATEMENT.md:154-165`
[NEC] (T4⁺⁺) (N1), (N2⁺⁺) with its scope, (N3⁺⁺) with the sentence on the constant 1, (N4); `STATEMENT.md:134-143` [F4]
(F4⁺⁺: the bound, n_F, the (AL) consequence); and, for the supersession table, the rows F4, NEC-b, NEC of
`STATEMENT.md:277-279`.
Uses: BASE `lemmas/L2_TK.md:32-98` (𝓔^blk, Lemma L2.1, n₁, (TK-a), (TK-d), (TK-e), (TK-f), κ_E, ω_n ≤ ω̄_n);
BASE `lemmas/L1_AGG_FLOOR.md:15-16` ((P1), (P2)); BASE `lemmas/L7_NEC.md:8-65` (copied below with changes);
BASE `lemmas/L3_LEAK.md:18-19` ((J2)), BASE `lemmas/L3_LEAK.md:95-105` (copied below with changes);
PARENT `lemmas/P3_NEC.md:13-36` (Lemma P3.1, the witness of P3.2), PARENT `lemmas/P3_NEC.md:44-64` (Example P3.3);
`lemmas/R1_VIS.md` R1.5 ((T1⁺⁺)). Interface claims consumed: W3-START:TK, :NEC-b, :F4, :FLOOR, W3-START2:NEC (through the
cited proof lines). No registry claim outside `STATEMENT.md:260-264` is consumed. One external standard fact is used,
only in Example R2.6 (a design for the sentence of (N3⁺⁺)): the Gaussian smallest-singular-value bound (R2.6, (G)).
**Marking.** Sections R2.1, R2.2 and R2.7 are copies of BASE L7.1, L7.2 and L3.5; every line whose content differs from
the BASE text carries a tag `[R-k]` at its end. R2.3–R2.6 and R2.8 are new (every line new; tagged per paragraph).

**ISSUES FOR THE LEAD:** none — no clause of this file's scope looked false or needed an unstated hypothesis. Remarks
(no clause changes): (1) in (C2⁺⁺)(ii) with c fixed the constant c may be negative (the premise then needs
2 log p ≥ |c| log n); the proof covers it, which is why ε₁ is taken against |c|. (2) The sentence "cannot be lowered, for
every sequence p_n ≤ n^A" of (N3⁺⁺) is proved for every sequence with 2 ≤ p_n ≤ n^A (p > s₀ is part of (E); the design
has s₀ = 1); for p_n > n − 2 the design is obtained by a probabilistic existence argument using (G). (3) n_F = 16 (absolute;
"depending only on A" holds trivially). (4) PARENT citations: see the remark in `lemmas/R1_VIS.md` (citecheck pattern).

## R2.0 Setting and conventions

Setting F, (E), [TK] in the quantitative form of BASE `STATEMENT.md:187-191` (which (E) and (GF-16) deliver), the actual
partition (blocks ≤ 16), s₀ fixed. Used of [TK]: the event 𝓔^blk with P((𝓔^blk)ᶜ) → 0; on 𝓔^blk, for n ≥ n₁, (TK-a), (TK-d),
(TK-f) on the block family with ω_n ≤ ω̄_n ≤ ½, ω̄_n log n → 0, ϑ_n ≤ ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)) − 1 (so ϑ̄_n log n → 0)
and the constant κ_E; (TK-e) everywhere. Of Setting F: p ≤ n^A and the Gaussian law of ε.
π₀(S₀) ≤ γ₀(S₀)/γ₀(S′) for every S′ ∈ Ω, S′ ≠ S₀ (BASE `lemmas/L7_NEC.md:9-10`). **Pointwise level:** for numbers c_n,
  **G_n := c_n·log n + 2 log p**   (G_n := c log n + 2 log p when c_n ≡ c).
For a premise "δ²_{U,v} ≥ τ²_U G_n" with G_n > 0, δ_{U,v} ≠ 0, hence (I − P_U)x_v ≠ 0 and Z_{U,v} = u_{U,v}ᵀε/σ ~ N(0, 1) with a
deterministic unit vector u_{U,v} (BASE `lemmas/L2_TK.md:78-81`). For a premise "δ²_{U,v} ≤ τ²_U G_n", G_n ≥ 0 is forced
(δ² ≥ 0, τ²_U > 0); if (I − P_U)x_v = 0 then RSS_U = RSS_{U∪{v}} and the upper bounds below hold trivially (put Z_{U,v} := 0).
Elementary: (1 + ω)⁻¹ ≥ 1 − ω (ω ≥ 0); log(n + 1) ≤ log n + log(5/4) (n ≥ 4).

## R2.1 (C2⁺⁺)(i), fixed c: one leaking null — copy of BASE L7.1 (BASE `lemmas/L7_NEC.md:12-26`)

**Claim.** Suppose that for all large n there is a null l = l_n with δ²_{U,l} ≥ τ²_U·G_n, G_n = c log n + 2 log p, at          [R-1]
U := U*_{b(l)}, with a fixed c > 1. Then P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (c − 1)/2.                                   [R-2]

*Proof.* Fix κ′ and put 3ϵ := (c − 1)/2 − κ′ > 0, ε₁ := min(½, ϵ/(|c|/2 + A + 1)). Let n be large: n ≥ max(n₁, 2s₀ + 2), so   [R-3]
s₀ < K (a null exists, so p > s₀), and S′ := S₀ ∪ {l} ∈ Ω. Let b := b(l). Then
  log[γ₀(S′)/γ₀(S₀)] = log[(s₀ + 1)/(2p − 1 − s₀)] + log[r_b(U ∪ {l})/r_b(U)]   ((P1)).                                 [R-4]
(Witness: the premise is a statement about the design, so l_n can be chosen deterministically, e.g. the least such
index; G_n > 0, so Z_{U,l} ~ N(0, 1), R2.0.)                                                                          [R-5]
*Event.* 𝒢 := 𝓔^blk ∩ {Z²_{U,l} ≤ 2 log log n}; Z_{U,l} ~ N(0, 1), so P(𝒢ᶜ) ≤ P((𝓔^blk)ᶜ) + 2/log n → 0.
*On 𝒢.* By (TK-d) and (f1): log[r_b(U ∪ l)/r_b(U)] ≥ −½ log(n + 1) + (RSS_U − RSS_{U∪l})/(2τ²_U(1 + ω_n)) − 2κ_E. By (TK-e) and   [R-6]
(a + b)² ≥ (1 − ε₁)a² − (1/ε₁ − 1)b²: RSS_U − RSS_{U∪l} = (δ_{U,l} + σZ_{U,l})² ≥ τ²_U[(1 − ε₁)G_n − 2 log log n/ε₁]. No upper    [R-7]
bound on the gain is used. As RSS_U − RSS_{U∪l} ≥ 0 and ω_n ≤ ω̄_n, the middle term is
≥ [(1 − ε₁)G_n − 2 log log n/ε₁]₊/(2(1 + ω̄_n)) ≥ (1 − ε₁)G_n/(2(1 + ω̄_n)) − log log n/ε₁. Also (s₀ + 1)/(2p − 1 − s₀) ≥ 1/(2p),  [R-8]
kept exactly: its log is ≥ −log(2p). With (1 − ε₁)/(1 + ω̄_n) ≥ 1 − ε₁ − ω̄_n and 0 < G_n ≤ (c + 2A) log n (p ≤ n^A):            [R-9]
  log[γ₀(S′)/γ₀(S₀)] ≥ −log(2p) − ½ log(n + 1) + G_n/2 − (ε₁ + ω̄_n)(c/2 + A) log n − log log n/ε₁ − 2κ_E                     [R-10]
   ≥ [(c − 1)/2 − ε₁(c/2 + A)] log n − [(c/2 + A)ω̄_n log n + log log n/ε₁ + 2κ_E + log 2 + ½ log(5/4)]                      [R-11]
(the terms in log p cancel: −log(2p) + ½·2 log p = −log 2). ε₁(c/2 + A) ≤ ϵ, and the bracket is o(log n) (ω̄_n log n → 0); so   [R-12]
the right side is ≥ [(c − 1)/2 − 2ϵ] log n = (κ′ + ϵ) log n ≥ κ′ log n for large n. Thus π₀(S₀) ≤ γ₀(S₀)/γ₀(S′) ≤ n^{−κ′} on 𝒢. ∎  [R-13]

## R2.2 (C2⁺⁺)(ii), fixed c: one weakly visible truth — copy of BASE L7.2 (BASE `lemmas/L7_NEC.md:28-44`)

**Claim.** Suppose that for all large n there is a truth j = j_n with δ²_{U,j} ≤ τ²_U·G_n, G_n = c log n + 2 log p, at          [R-14]
U := U*_{b(j)} ∖ {j}, with a fixed c < 1 (c may be negative; the premise forces G_n ≥ 0). Then P(π₀(S₀) ≤ n^{−κ′}) → 1 for     [R-15]
every κ′ < (1 − c)/2.                                                                                                [R-16]

*Proof.* Fix κ′, 3ϵ := (1 − c)/2 − κ′ > 0, ε₁ := min(½, ϵ/(|c|/2 + A + 1)). S′ := S₀ ∖ {j} ∈ Ω (n ≥ max(n₁, 2s₀ + 2)). With   [R-17]
b := b(j), U ∪ {j} = U*_b:
  log[γ₀(S′)/γ₀(S₀)] = log[(2p − s₀)/s₀] + log[r_b(U)/r_b(U ∪ {j})]   ((P2)),
and by (TK-d): log[r_b(U)/r_b(U ∪ j)] ≥ ½ log(n + 1) − ν log(RSS_U/RSS_{U∪j}) − 2κ_E.
*Event.* 𝒢 := 𝓔^blk ∩ {Z²_{U,j} ≤ 2 log log n}, P(𝒢ᶜ) → 0.
*On 𝒢.* RSS_U − RSS_{U∪j} = (δ_{U,j} + σZ_{U,j})² ≤ (1 + ε₁)δ² + (1 + 1/ε₁)σ²Z² ≤ τ²_U·Ḡ_n,
Ḡ_n := (1 + ε₁)G_n + 2(1 + 1/ε₁) log log n. Since 0 ≤ G_n ≤ (|c| + 2A) log n, Ḡ_n ≤ ḡ_n := (3/2)(|c| + 2A) log n + 6 log log n/ε₁,  [R-18]
a deterministic sequence. By (TK-a), x := (RSS_U − RSS_{U∪j})/RSS_U ≤ ḡ_n/((n − 1)(1 − ω̄_n)) =: x̄_n → 0, so x ≤ ½ for large n   [R-19]
and (f3) gives ν log(RSS_U/RSS_{U∪j}) ≤ (1 + ϑ̄_n)(1 + x̄_n)Ḡ_n/2 ≤ Ḡ_n/2 + ς_n, ς_n := [(1 + ϑ̄_n)(1 + x̄_n) − 1]ḡ_n/2 → 0      [R-20]
(ϑ̄_n log n → 0 because ω̄_n log n → 0; x̄_n log n → 0). Also (2p − s₀)/s₀ ≥ p/s₀, kept exactly: its log is ≥ log p − log s₀. Hence  [R-21]
  log[γ₀(S′)/γ₀(S₀)] ≥ log p − log s₀ + ½ log n − (1 + ε₁)G_n/2 − (1 + 1/ε₁) log log n − ς_n − 2κ_E                        [R-22]
   = [(1 − c)/2] log n − ε₁G_n/2 − [log s₀ + (1 + 1/ε₁) log log n + ς_n + 2κ_E]                                          [R-23]
   ≥ [(1 − c)/2 − ε₁(|c|/2 + A)] log n − o(log n) ≥ [(1 − c)/2 − ϵ] log n − o(log n) = (κ′ + 2ϵ) log n − o(log n) ≥ κ′ log n  [R-24]
for large n (the log p terms cancel: log p − ½·2 log p = 0). Thus π₀(S₀) ≤ n^{−κ′} on 𝒢. ∎                                    [R-25]

*Remarks* (as BASE `lemmas/L7_NEC.md:46-48`). (1) Each claim uses one Gaussian variable at a deterministic witness. (2) (i) uses
the lower bound (f1), valid for gains of any size; (ii) uses (f3), available because the assumed gain is O(log n) (p ≤ n^A).  [R-26]
(3) Both hold for every partition with blocks ≤ 16 that is a function of X. (4) "For large n" depends only on (κ′, c, A, s₀,
κ_E) and the envelopes, not on the design.                                                                         [R-27]

## R2.3 (C2⁺⁺)(i), drifting: (c_n − 1)√log n → ∞ ⇒ π₀(S₀) → 0 in probability (new)

Premise: for all large n a null l = l_n with δ²_{U,l} ≥ τ²_U G_n at U = U*_{b(l)}, G_n = c_n log n + 2 log p, (c_n − 1)√log n → ∞.
Put g := δ²_{U,l}/τ²_U ≥ G_n (deterministic) and L_n := 6(A + 1) log n. Fix ε ∈ (0, 1) and M = M_ε ≥ 1 with P(|Z| > M) ≤ ε,
Z ~ N(0, 1). Let n₅ be such that for n ≥ n₅: the premise holds, c_n > 1, n ≥ max(n₁, 2s₀ + 2) and log n ≥ 16M². Then for
n ≥ n₅: S′ := S₀ ∪ {l} ∈ Ω, G_n ≥ log n ≥ 16M² > 0 (so Z_{U,l} ~ N(0, 1), R2.0), and g ≥ 16M², i.e. 2M√g ≤ g/2.
*Event.* 𝒢_M := 𝓔^blk ∩ {|Z_{U,l}| ≤ M}; P(𝒢_Mᶜ) ≤ P((𝓔^blk)ᶜ) + ε.
*On 𝒢_M.* (δ + σZ)² ≥ δ² − 2|δ|σ|Z| and σ ≤ τ_U give RSS_U − RSS_{U∪l} ≥ τ²_U(g − 2M√g) ≥ τ²_U g/2 ≥ 0, and by (f1)
ν log(RSS_U/RSS_{U∪l}) ≥ (g − 2M√g)/(2(1 + ω_n)). As in R2.1, log[γ₀(S′)/γ₀(S₀)] ≥ −log(2p) − ½ log(n + 1) + ν log(RSS_U/RSS_{U∪l}) − 2κ_E.
* Case A, g ≤ L_n. Then ν log(…) ≥ (g − 2M√g)(1 − ω̄_n)/2 ≥ (g − 2M√g)/2 − ω̄_nL_n/2. The map t ↦ t − 2M√t is nondecreasing on
  t ≥ M², and g ≥ G_n ≥ M², so g − 2M√g ≥ G_n − 2M√G_n; and G_n ≤ g ≤ L_n. Hence
    log[γ₀(S′)/γ₀(S₀)] ≥ −log(2p) − ½ log(n + 1) + G_n/2 − M√L_n − ω̄_nL_n/2 − 2κ_E
     = √log n·[((c_n − 1)/2)√log n − M√(6(A + 1))] − [ω̄_nL_n/2 + 2κ_E + log 2 + ½ log(5/4)] =: m_n^A.
* Case B, g > L_n (gains much larger than log n; **no upper bound on the gain is used**). With 1 + ω_n ≤ 3/2:
  ν log(…) ≥ (g/2)/(2·(3/2)) = g/6 > (A + 1) log n, and log p ≤ A log n, so
    log[γ₀(S′)/γ₀(S₀)] ≥ −log 2 − A log n − ½ log n − ½ log(5/4) + (A + 1) log n − 2κ_E = ½ log n − [log 2 + ½ log(5/4) + 2κ_E] =: m_n^B.
The case is determined by the design (deterministic at each n). m_n := min(m_n^A, m_n^B) is deterministic and m_n → ∞:
ω̄_nL_n → 0, and ((c_n − 1)/2)√log n − M√(6(A + 1)) → ∞. So on 𝒢_M, π₀(S₀) ≤ γ₀(S₀)/γ₀(S′) ≤ e^{−m_n}. For every η > 0:
limsup_n P(π₀(S₀) > η) ≤ limsup_n P(𝒢_Mᶜ) ≤ ε; ε is arbitrary. **π₀(S₀) → 0 in probability.** ∎                             [R-28]

## R2.4 (C2⁺⁺)(ii), drifting: (1 − c_n)√log n → ∞ ⇒ π₀(S₀) → 0 in probability (new)

Premise: for all large n a truth j = j_n with δ²_{U,j} ≤ τ²_U G_n at U = U*_{b(j)} ∖ {j}, G_n = c_n log n + 2 log p,
(1 − c_n)√log n → ∞. Fix ε, M = M_ε as in R2.3; n₅ such that for n ≥ n₅ the premise holds, c_n < 1 and n ≥ max(n₁, 2s₀ + 2).
Then 0 ≤ G_n ≤ (1 + 2A) log n (R2.0; c_n < 1, p ≤ n^A). S′ := S₀ ∖ {j} ∈ Ω; 𝒢_M := 𝓔^blk ∩ {|Z_{U,j}| ≤ M}, P(𝒢_Mᶜ) ≤ P((𝓔^blk)ᶜ) + ε.
*On 𝒢_M.* (δ + σZ)² ≤ δ² + 2|δ|σ|Z| + σ²Z² and σ ≤ τ_U give RSS_U − RSS_{U∪j} ≤ τ²_U·Ḡ_n, Ḡ_n := G_n + 2M√G_n + M²
≤ ḡ_n := (1 + 2A) log n + 2M√((1 + 2A) log n) + M². By (TK-a), x ≤ ḡ_n/((n − 1)(1 − ω̄_n)) =: x̄_n → 0; for large n x̄_n ≤ ½, and
(f3) gives ν log(RSS_U/RSS_{U∪j}) ≤ Ḡ_n/2 + ς_n, ς_n := [(1 + ϑ̄_n)(1 + x̄_n) − 1]ḡ_n/2 → 0. As in R2.2 ((P2), (TK-d)):
  log[γ₀(S′)/γ₀(S₀)] ≥ log p − log s₀ + ½ log n − G_n/2 − M√G_n − M²/2 − ς_n − 2κ_E
   ≥ √log n·[((1 − c_n)/2)√log n − M√(1 + 2A)] − [log s₀ + M²/2 + ς_n + 2κ_E] =: m_n → ∞.
So π₀(S₀) ≤ e^{−m_n} on 𝒢_M, and as in R2.3 **π₀(S₀) → 0 in probability.** ∎                                                [R-29]

**(C2⁺⁺) proved.** (i): fixed c > 1 by R2.1, drifting by R2.3; (ii): fixed c < 1 by R2.2, drifting by R2.4. Hypotheses
used: Setting F, (E) (p ≤ n^A, p > s₀), [TK] in the quantitative form. ∎

## R2.5 Proposition NEC (T4⁺⁺) (`STATEMENT.md:154-165`)

Setting F, (E), (GF-16) (which deliver [TK] in quantitative form, BASE `lemmas/L2_TK.md:94-98`).
**(N1).** BASE `lemmas/L7_NEC.md:53-55` and PARENT `lemmas/P3_NEC.md:73-75` with (T1⁺⁺)–(T3⁺⁺) and F2⁺⁺: (T0) (unchanged)
gives o₀ ≥ ½(n + 1)^{−1/2} whenever s₀ < K, for every design and data set, so no hypothesis gives an exponent better than ½;
under F2⁺⁺ (`STATEMENT.md:129-132`) with η′ = 0 and κ_V > ½ the order is exact — this is the exact-order clause of F2⁺⁺,
whose proof (PARENT `lemmas/P1_LEADING.md:140-141` with (T1⁺⁺)(b) of `lemmas/R1_VIS.md` R1.5 in place of (T1⁺)(b)) is in the
lead's file R4 (PLAN §2).                                                                                           [R-30]
**(N2⁺⁺).** Hypothesis: s₀ ≥ 1, r(s₀) = max(1, 17 − s₀); for all large n a deterministic set I_n ⊆ [p] ∖ S₀ of r(s₀) nulls with
δ²_{V,l} ≥ τ²_V G_n for every l ∈ I_n and every V ⊊ S₀ with |V| ≤ 15. Choose the witness l_n ∈ I_n exactly as in PARENT
`lemmas/P3_NEC.md:26-31`: for s₀ ≥ 16, I_n = {l_n} and U*_{b(l_n)} ⊆ C_{b(l_n)} ∖ {l_n} has ≤ 15 < s₀ elements; for 1 ≤ s₀ ≤ 15, Lemma
P3.1 (PARENT `lemmas/P3_NEC.md:15-18`) gives an l ∈ I_n with U*_{b(l)} ⊊ S₀, and l_n is the least one. In both cases l_n is a
function of X and I_n only, and V := U*_{b(l_n)} is a proper subset of S₀ with |V| ≤ 15; the hypothesis at this V is the
premise of (C2⁺⁺)(i) with the null l_n and the same c_n. R2.1 (c_n ≡ c > 1) and R2.3 ((c_n − 1)√log n → ∞) give the two
conclusions. ∎                                                                                                  [R-31]
*Scope* (PARENT `STATEMENT.md:160-166`, with this premise). For s₀ ≥ 16, r(s₀) = 1 and every V ⊆ S₀ with |V| ≤ 15 is proper.
For 1 ≤ s₀ ≤ 15 the premise can hold together with (E) and (GF-16): in Example P3.3 (PARENT `lemmas/P3_NEC.md:44-64`) with
constant c* > 1 one has p = 17, so δ²_{V,l} ≥ c*τ²_V log n ≥ τ²_V(c log n + 2 log 17) for large n whenever c < c* — take
c* := c + 1 for a fixed c > 1, and c* := 3 for a drifting c_n with c_n ≤ 2 eventually (for instance c_n = 1 + (log n)^{−1/4}).
One leaking null is not claimed to be enough when s₀ ≤ 15, and s₀ = 0 is excluded (nothing to prove). ∎                     [R-32]
**(N3⁺⁺).** Let j = j_n be a truth with δ²_{V,j} ≤ τ²_V G_n for every V ⊆ S₀ ∖ {j} with |V| ≤ 15. The set U*_{b(j)} ∖ {j} ⊆ S₀ ∖ {j}
has at most 15 elements (it lies in C_{b(j)} ∖ {j}); so the premise of (C2⁺⁺)(ii) holds with the same c_n. R2.2 (c_n ≡ c < 1) and
R2.4 ((1 − c_n)√log n → ∞) give the two conclusions. ∎ The sentence on the constant 1 is Example R2.6.                     [R-33]
**(N4)** is a statement of scope (PARENT `STATEMENT.md:169-170`, BASE `STATEMENT.md:329-331`); nothing is proved. ∎

## R2.6 Example: the constant 1 cannot be lowered, for every sequence p_n (new)

**Meaning.** For every c₁ < 1 and every sequence p_n with 2 ≤ p_n ≤ n^A there are, for all large n, a design and θ* with s₀ = 1
satisfying (E), (GF-16) (g_* = 1), (AL) at Q = S₀, the visibility inequality of (V-cp) with c₁ in place of c_V, and the
instances D = {j}, N = ∅ of (V-mp) (any Q ⊇ S₀) with c_m replaced by the negative constant c* − 1 > c₁ − 1 — and for which
P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 − c*)/2. So neither 1 in front of log n can be replaced by a smaller constant.
**Construction.** Fix c* ∈ (max(c₁, 0), 1), σ² > 0, and put G*_n := c* log n + 2 log p_n (≤ (1 + 2A) log n < (n − 1)/2 for
large n) and θ_n² := σ²G*_n/(n − 1 − G*_n) > 0. Let x₁ ∈ 1^⊥ with ‖x₁‖² = n − 1, and let x₂, …, x_p ∈ {1, x₁}^⊥ with ‖x_k‖² = n − 1
and λ_min(X_TᵀX_T) ≥ 1 for every T ⊆ {2, …, p} with 1 ≤ |T| ≤ 16 (existence below). The columns are centred with sample
variance 1 (a standardised raw design, D_x = I). θ* := (θ_n, 0, …, 0), S₀ = {1}, μ = θ_nx₁.
* (E): ‖μ‖² = (n − 1)θ_n² = σ²G*_n(n − 1)/(n − 1 − G*_n) ≤ 2σ²(1 + 2A) log n ≤ Mn (any M > 0, large n); p ≤ n^A, p > s₀.
* (GF-16): x₁ is orthogonal to every other column, so X_TᵀX_T = diag(n − 1, X_{T∖1}ᵀX_{T∖1}) if 1 ∈ T; λ_min ≥ 1.
* Gains: for U ∌ 1, x₁ ⊥ span X_U and μ ⊥ span X_U, so (I − P_U)x₁ = x₁, Λ_U = ‖μ‖², δ²_{U,1} = (n − 1)θ_n², τ²_U = σ² + θ_n², and
  δ²_{U,1}/τ²_U = (n − 1)θ_n²/(σ² + θ_n²) = G*_n (by the choice of θ_n). Hence δ²_{U,1} = τ²_U(c* log n + 2 log p) ≥ τ²_U(c₁ log n + 2 log p)
  for every U ⊆ [p] ∖ {1}, |U| ≤ 15: (V-cp) with c₁. For an instance V = D = {1}, N = ∅, R ⊆ Q ∖ S₀ of (V-mp): U = R, T = W = {1} ∪ R,
  L₂ = 0, L₁/τ²_U = G*_n = π_n(1, 0; Q) + (c* − 1) log n.
* Nulls: for l ≠ 1 and any U ∌ l, (I − P_U)x_l ∈ span{x_k : k ≠ 1} ⊥ x₁ if 1 ∉ U, and μ ∈ span X_U if 1 ∈ U; in both cases δ_{U,l} = 0.
  So F1 with η = 0 (BASE `lemmas/L6_COROLLARIES.md:42-44`) gives ϱ_n(S₀) = O(√(log n/n)) → 0: (AL) at Q = S₀.
* The premise of (N3⁺⁺) holds with c_n ≡ c* < 1 (the only V ⊆ S₀ ∖ {1} is ∅, and δ²_{∅,1} = τ²_∅G*_n); so
  P(π₀(S₀) ≤ n^{−κ′}) → 1 for every κ′ < (1 − c*)/2.
**Existence of x₂, …, x_p.** Let m := n − 2 and O ∈ ℝ^{n×m} with orthonormal columns spanning {1, x₁}^⊥. Draw g₂, …, g_p iid
N(0, I_m) and put x_k := √(n − 1)·Og_k/‖g_k‖. For T ⊆ {2, …, p}, 1 ≤ t := |T| ≤ 16, with G_T := [g_k]_{k∈T}:
λ_min(X_TᵀX_T) ≥ (n − 1)·s_min(G_T)²/max_{k∈T}‖g_k‖². **(G)** (Gaussian smallest singular value; e.g. R. Vershynin, *Introduction
to the non-asymptotic analysis of random matrices*, 2012, Cor. 5.35): P(s_min(G_T) ≤ √m − √t − r) ≤ 2e^{−r²/2}. With
r := √m/4 and m ≥ 256: s_min(G_T) ≥ (3/4)√m − 4 ≥ √m/2 off an event of probability ≤ 2e^{−m/32}. Laurent–Massart (as in BASE
`lemmas/L2_TK.md:36-37`, x = m/8): P(‖g_k‖² > 2m) ≤ e^{−m/8}. Off the union of these events, λ_min(X_TᵀX_T) ≥ (n − 1)(m/4)/(2m)
= (n − 1)/8 ≥ 1. The union has probability ≤ 17p^{16}·2e^{−m/32} + p·e^{−m/8} ≤ 34n^{16A}e^{−(n−2)/32} + n^Ae^{−(n−2)/8} < 1 for
large n (depending on A); so a realisation with the required property exists, and it is fixed. ∎                         [R-34]

## R2.7 Corollary F4⁺⁺ — copy of BASE L3.5 (BASE `lemmas/L3_LEAK.md:95-105`)

Let I_n ⊆ [p] ∖ Q, |I_n| ≤ ī, δ²_{U,l} ≤ τ²_U·G_n, G_n = c_n log n + 2 log p, for l ∈ I_n and all U ⊆ [p] ∖ {l}, |U| ≤ 15; c_n ≤ 1   [R-35]
(any numbers, fixed or not); h_l := min(z_n, √(4 log log n)) for l ∈ I_n, h_l := z_n otherwise.                         [R-36]
* *h is a level vector.* For n ≥ 4: 4 log log n ≥ 4 log log 4 > 1.3 and z_n² > 2 log(2^{21}) > 29, so 1 ≤ h_l ≤ z_n.
* *Budget.* b_n(h) ≤ 1/(32 log n) + 2^{16}ī·max{(log n)^{−2}, 1/(2^{21}p log n)} → 0.
* *Functional.* For l ∈ I_n and |U| ≤ 15: 0 ≤ δ²_{U,l}/τ²_U ≤ G_n ≤ (1 + 2A) log n (c_n ≤ 1, p ≤ n^A). By (J2) with |d|/t ≤ √G_n,      [R-37]
  σ/t ≤ 1 and h_l ≤ √(4 log log n):
  J_{h_l}(δ_{U,l}, τ_U) ≤ √(2/π)·√(4 log log n)·exp(G_n/2 + √G_n·√(4 log log n))                                         [R-38]
   ≤ √(8/π)·√(log log n)·p·n^{c_n/2}·exp(2√(1 + 2A)·√(log n·log log n))   (e^{G_n/2} = p·n^{c_n/2} exactly).                    [R-39]
  For n ≥ n_F := 16: √(8/π)·√(log log n) ≤ exp(√(log n·log log n)). [Put u := log log n ≥ 1 (n ≥ e^e); √(8/π) < e^{1/2} and √u ≤ e^{u/2},  [R-40]
  so the left side is ≤ e^{(1+u)/2}; and √(log n·u) ≥ √(log n) = e^{u/2} ≥ (1 + u)/2, since e^u ≥ 1 + u + u²/2 ≥ (1 + u)²/4.]          [R-41]
  Hence J_{h_l}(δ_{U,l}, τ_U) ≤ p·n^{c_n/2}·exp(C_A√(log n·log log n)), C_A = 2√(1 + 2A) + 1. For l ∉ Q ∪ I_n the terms are those of the   [R-42]
  default functional. Hence, for n ≥ n_F,
  **ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)·n^{−1/2}·p⁻¹·ī·p·n^{c_n/2}e^{C_A√(log n log log n)} = ϱ^{−I}_n(Q) + (|Q| + 1)·ī·n^{−(1−c_n)/2}·exp(C_A√(log n·log log n)).**  [R-43]
  (The factor p of the level cancels the 1/p of the average exactly; no lower bound on p is used.)                       [R-44]
* *(AL) and (T1⁺⁺).* If ϱ^{−I}_n(Q) → 0 and the second term tends to zero, then ϱ_n(Q; h) → 0 and b_n(h) → 0: (AL) holds with this
  h, and (T1⁺⁺) applies with it under (E), (GF-16), (V-cp) or (V-mp) (`lemmas/R1_VIS.md` R1.5). For a fixed c < 1 and
  (|Q| + 1)n^{−κ₁} → 0 with κ₁ < (1 − c)/2, the second term is
  (|Q| + 1)n^{−κ₁}·ī·exp(−((1 − c)/2 − κ₁) log n + C_A√(log n log log n)) → 0, because √(log n·log log n) = o(log n). ∎        [R-45]
* *The parenthetical of F4⁺⁺* (`STATEMENT.md:142-143`): a column l with δ²_{U,l} ≥ τ²_U(c log n + 2 log p) at U = U*_{b(l)}, c > 1,
  gives π₀(S₀) → 0 by R2.1 (and R2.3 for drifting c_n); F4⁺⁺ admits every c_n ≤ 1 at the same level; the thresholds meet at
  c = 1 for every sequence p_n, since neither proof uses a relation between log p and log n beyond p ≤ n^A.               [R-46]

## R2.8 Supersession: the version-1.4 premises imply the new ones (`STATEMENT.md:277-279`) (new)

Ā := limsup log p/log n ≤ A, A̲ := liminf log p/log n ≥ 0 (p ≥ 1). For every η > 0, for all large n:
(A̲ − η) log n ≤ log p ≤ (Ā + η) log n.
**NEC-b.** (i) Old premise (BASE `STATEMENT.md:223-224`): δ²_{U,l} ≥ c′τ²_U log n, c′ > 1 + 2Ā fixed. For η ∈ (0, (c′ − 1 − 2Ā)/2):
c′ log n ≥ (c′ − 2Ā − 2η) log n + 2 log p for large n, so the new premise holds with the fixed c := c′ − 2Ā − 2η > 1, and R2.1 gives
P(π₀(S₀) ≤ n^{−κ′}) → 1 for κ′ < (c − 1)/2 = (c′ − 1 − 2Ā)/2 − η. Every κ′ < (c′ − 1 − 2Ā)/2 is below this for small η: the old
conclusion. (ii) Old premise (`:225-226`): δ²_{U,j} ≤ c′τ²_U log n, c′ < 1 + 2A̲. For η ∈ (0, (1 + 2A̲ − c′)/2):
c′ log n ≤ (c′ − 2A̲ + 2η) log n + 2 log p for large n; c := c′ − 2A̲ + 2η < 1; R2.2 gives κ′ < (1 − c)/2 = (1 + 2A̲ − c′)/2 − η;
η ↓ 0 gives the old conclusion. Hypotheses: the same ((E), [TK] in quantitative form, BASE `STATEMENT.md:187-191`). ∎
**NEC.** (N2⁺) (PARENT `STATEMENT.md:156-159`) and (N3) (`:167-168`) convert clause by clause as in (i), (ii) (the sets I_n, V
are unchanged); (N1) of version 1.5 contains that of version 1.4 ((T0) is unchanged, and (T1⁺⁺)–(T3⁺⁺), F2⁺⁺ imply (T1⁺)–(T3⁺),
F2⁺ by `STATEMENT.md:271-282`); (N4) is identical. ∎
**F4.** Old premise (BASE `STATEMENT.md:278-280`): δ²_{U,l} ≤ c′τ²_U log n, c′ < 1 + 2A̲ fixed. For η ∈ (0, (1 + 2A̲ − c′)/2) the new
premise holds for large n with c_n ≡ c := c′ − 2A̲ + 2η < 1, and R2.7 gives ϱ_n(Q; h) ≤ ϱ^{−I}_n(Q) + (|Q| + 1)n^{−(1+2A̲−c′)/2+η+o(1)}
(ī and exp(C_A√(log n log log n)) are n^{o(1)}). As η > 0 is arbitrary, a diagonal choice η = η_n ↓ 0 slowly gives the old bound
(|Q| + 1)n^{−(1+2A̲−c′)/2+o(1)}; and for κ₁ < (1 + 2A̲ − c′)/2 = (1 − c)/2 + η, choosing η < ((1 + 2A̲ − c′)/2 − κ₁)/2 gives
κ₁ < (1 − c)/2, so the old (AL) condition gives the new one. The levels h are the same. ∎                                [R-47]

*Count of tags:* R2.1 13, R2.2 14 (incl. remarks), R2.3 1, R2.4 1, R2.5 4, R2.6 1, R2.7 12, R2.8 1 — 47 in all.
