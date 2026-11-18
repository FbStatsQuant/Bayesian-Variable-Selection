# R1 — Visibility at the level of the actual p: (D3) relation, VIS-c⁺⁺, VIS-m⁺⁺, (T1⁺⁺) START-F

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Citations: BASE `path:lines` is a file of BASE := `Theory_work/Wave3/W3-START/` (v1.3.4); PARENT `path:lines` is a file
of PARENT := `Theory_work/Wave3/W3-START2/` (v1.4.1); a path with neither word is this ticket's. Both parents are read-only.
Statement proved: `STATEMENT.md:51-68` ((D3): the two implications of its relation paragraph and the comparisons stated
there); `STATEMENT.md:101-106` [VIS-c] (B-V1⁺⁺); `STATEMENT.md:108-111` [VIS-m] (B-V2⁺⁺); `STATEMENT.md:113-127`
[START-F] (T1⁺⁺)(a)–(d); and, for the supersession table, the rows START-F, VIS-c, VIS-m of `STATEMENT.md:271-273`.
Uses: BASE `lemmas/L2_TK.md:32-98` (𝓔^blk, Lemma L2.1, n₁, (TK-a), (TK-d), (TK-e), (TK-f), κ_E, ω_n ≤ ω̄_n);
BASE `lemmas/L4_VIS.md:7-87` (copied below with changes); BASE `lemmas/L1_AGG_FLOOR.md:103-109` (AGG-d);
BASE `lemmas/L3_LEAK.md:34` ((B1)(i)); BASE `lemmas/L5_ASM_STARTF.md:11` ((e1)), BASE `lemmas/L5_ASM_STARTF.md:37-89`
(L5.2, L5.3); BASE `lemmas/L6_COROLLARIES.md:9-26` (L6.0, L6.0′); PARENT `lemmas/P1_LEADING.md:80-126` (P1.4, P1.5).
Interface claims consumed: W3-START:TK, :LEAK, :AGG (through the cited proof lines); W3-START2:START-F (structure of its
proof). No registry claim outside `STATEMENT.md:260-264` is consumed.
**Marking.** Sections R1.2 and R1.3 are copies of BASE L4.1 and L4.2; every line whose content differs from the BASE text
carries a tag `[R-k]` at its end. Untagged lines are BASE text (notation adapted only where (V-m), (V-c) are renamed).

**ISSUES FOR THE LEAD:** none — no clause of the files' scope looked false or needed an unstated hypothesis. Two
remarks (no clause changes): (1) the thresholds n₃, n₄ of the interface forms depend, besides the listed constants, on
the [TK] envelopes ω̄_n, ϑ̄_n; in the quantitative form of BASE `STATEMENT.md:187-191` these are functions of (n, A)
only, so the stated dependence is exact; (2) the word PARENT (six letters) is not matched by the abbreviation pattern
`[A-Z0-9]{2,5}` of the parents' citation checkers; the copy for this ticket needs `{2,6}` and a PARENT entry.

## R1.0 (D3): relation to version 1.4 (`STATEMENT.md:63-68`)

Setting F: p ≤ n^A (BASE `STATEMENT.md:65-68`), and K ≤ p, |Q| ≤ K (BASE `STATEMENT.md:47-49`, `:80-81`).
**(a) (V-c) ⇒ (V-cp).** Let (V-c) hold with c_V > 1 + 2A. Then 2 log p ≤ 2A log n, so for every j ∈ S₀ and U ⊆ [p] ∖ {j}
with |U| ≤ 15: δ²_{U,j} ≥ c_Vτ²_U log n ≥ τ²_U[(c_V − 2A) log n + 2 log p]. This is (V-cp) with c_V′ := c_V − 2A > 1, and
κ_V′ = (c_V′ − 1)/2 = (c_V − 1 − 2A)/2, the exponent of (V-c) (BASE `STATEMENT.md:125-126`). ∎
**(b) A bound on c_Q/p.** If s₀ ≥ 1: c_Q = |Q| + 15s₀ ≤ p + 15s₀ and p ≥ 1, so **c_Q/p ≤ 1 + 15s₀ ≤ 16s₀**, i.e. p/c_Q ≥ 1/(16s₀).
Hence for n ≥ 256s₀²: **log n + 2 log(p/c_Q) ≥ log n − 2 log(16s₀) ≥ 0.**                                          (R1.0)
**(c) (V-m) ⇒ (V-mp) for n ≥ 256s₀².** If s₀ = 0 both are empty (no V ⊆ S₀ with |V| ≥ 1). Let s₀ ≥ 1; the quantifiers of
(V-m) and (V-mp) range over the same (V, D, R, N), with d = |D|, a = |N|. If d ≥ a: π_n(d, a; Q) = (d − a)(log n + 2 log p)
≤ (1 + 2A)(d − a) log n. If a > d: π_n(d, a; Q) = −(a − d)(log n + 2 log(p/c_Q)) ≤ 0 = (1 + 2A)(d − a)₊ log n by (R1.0). So
π_n(d, a; Q) ≤ (1 + 2A)(d − a)₊ log n in all cases, and the right side of (V-m) dominates that of (V-mp), with the same
(c_m, ε₀) and κ_V = c_m/2. ∎
**(d) The comparisons of `STATEMENT.md:65-68`.** (i) If log p/log n → A, the levels c_V′ log n + 2 log p of (V-cp) and
(c_V′ + 2A) log n of (V-c) (with c_V = c_V′ + 2A) have ratio → 1. (ii) On an instance with a > d and n ≥ 256s₀², the right
side of (V-mp) is smaller than that of (V-m) by (a − d)(log n + 2 log(p/c_Q)) ≥ log n − 2 log(16s₀) > 0 for n > 256s₀²,
for every sequence p_n (in particular when log p/log n → A). (iii) At every n with p < n^A, the level of (V-cp) with
c_V′ = c_V − 2A is below that of (V-c), and on instances with d > a the price π_n is below (1 + 2A)(d − a) log n; so both
forms ask no more than the version-1.4 forms, and strictly less at such n. ∎
**Supersession rows** (`STATEMENT.md:271-273`). A design satisfying (V-c) [resp. (V-m)] at n satisfies (V-cp) with c_V − 2A
[resp. (V-mp) with (c_m, ε₀), n ≥ 256s₀²] at n, with the same κ_V; the conclusions of VIS-c⁺⁺, VIS-m⁺⁺, (T1⁺⁺) are those of
(B-V1), (B-V2) (BASE `STATEMENT.md:235-236`) and (T1⁺) (PARENT `STATEMENT.md:93-110`) word for word; in (T1⁺⁺)(d) the
threshold n₀ in the margin case is ≥ n₃ ≥ 256s₀² (R1.2), so for n ≥ n₀ the implication (c) applies (the implication (a)
needs no condition on n). Hence START-F⁺⁺ ⇒
W3-START2:START-F, VIS-c⁺⁺ ⇒ W3-START:VIS-c, VIS-m⁺⁺ ⇒ W3-START:VIS-m.

## R1.1 Setting, the event 𝓧, and what is used of [TK]

BASE L4.0 (BASE `lemmas/L4_VIS.md:7-20`) unchanged: Setting F, s₀ ≥ 1 (for s₀ = 0: Ξ(Q) = 0 = e_n by definition and
[VIS] is trivial), a deterministic Q ⊇ S₀ with |Q| ≤ K, the actual partition (blocks ≤ 16), ζ_n := 4 log(2^8·3^{16}·s₀·log n),
**𝓧 := {‖(P_W − P_U)ε‖² ≤ σ²ζ_n for every truth block b and all U ⊆ W ⊆ C_b}**, P(𝓧ᶜ) ≤ 1/log n (`:11-15`; the rank of
P_W − P_U is rank X_W − rank X_U ≤ |W ∖ U| ≤ 16 for every design, so no rank condition is needed), and (Q±) (`:16-17`).
**(B1), visibility** (`:19-20`, with (D3)): (V-cp) and (V-mp) quantify over all U ⊆ [p] ∖ {j} with |U| ≤ 15, resp. all
(V, D, R, N) with V ⊆ S₀, R ⊆ Q ∖ S₀, N ⊆ [p] ∖ Q, |V| + |R| + |N| ≤ 16; the sets used below (subsets of one block) are
among them, for every partition with blocks of size ≤ 16.                                                        [R-1]
**[TK] in the quantitative form** (BASE `STATEMENT.md:187-191`) supplies exactly what the proofs below use: the event
𝓔^blk with P((𝓔^blk)ᶜ) → 0 (under (E), (GF-16): ≤ 2e^{−n^{1/3}} + 2/n, BASE `lemmas/L2_TK.md:32`); on 𝓔^blk, for n ≥ n₁,
(TK-a), (TK-d), (TK-f) on the block family with ω_n ≤ ω̄_n, ω̄_n log n → 0, ϑ_n ≤ ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)) − 1
and the constant κ_E (BASE `lemmas/L2_TK.md:44-90`); (TK-e) is an identity valid everywhere (`:78-81`). Under (E) and
(GF-16), ω̄_n, ϑ̄_n, n₁ depend only on (n, A) and κ_E only on (g_*, M, σ²) (`:94-98`). Of Setting F the proofs use
p ≤ n^A, K ≤ p, |Q| ≤ K and the Gaussian law of ε (for 𝓧).                                                         [R-2]

## R1.2 Bridge (B-V2⁺⁺): margin visibility at the exact price — copy of BASE L4.1 (BASE `lemmas/L4_VIS.md:22-55`)

**Proposition R1.2.** Assume (V-mp) at n with constants (c_m, ε₀) for Q, and let κ ∈ (0, c_m/2). There is                [R-3]
n₃ = n₃(κ, A, M, σ², g_*, s₀, c_m, ε₀) such that for n ≥ n₃, on 𝓔^blk ∩ 𝓧:
  **ω^Q(U)·r_b(U)/r_b(T_b(U)) ≤ 2^{−16}n^{−κ} for every truth block b and every U ⊆ C_b with U*_b ⊄ U; hence Ξ(Q) ≤ n^{−κ}.**
Consequently P(Ξ(Q) > n^{−κ}) ≤ P((𝓔^blk)ᶜ) + 1/log n → 0 for every κ < c_m/2: [VIS(κ; Q)] with κ_V = c_m/2.

*Proof.* Fix b and U. Put V := U*_b, D := V ∖ U ≠ ∅, R := (U ∩ Q) ∖ S₀, N := U ∖ Q, d := |D|, a := |N|, T := V ∪ R = T_b(U),
W := V ∪ R ∪ N = U ∪ D. Then U = (V ∖ D) ∪ R ∪ N (as U ∩ S₀ = V ∖ D), |V| + |R| + |N| = |W| ≤ 16, U ⊆ W, T ⊆ W, all inside C_b,
and |U| − |T| = a − d. This is an instance of the quantifier of (V-mp); write L₁ := Λ_U − Λ_W, L₂ := Λ_T − Λ_W and            [R-4]
π := π_n(d, a; Q) (`STATEMENT.md:57-58`), so that (V-mp) reads                                                        [R-5]
  L₁/τ²_U ≥ π + c_m·log n + (1 + ε₀)·L₂/τ²_W.                                                                      (4.1⁺⁺) [R-6]
(π may have either sign, and so may π + c_m log n.)                                                                [R-7]
*Constants.* ε₁ := min{ε₀/(2(2 + ε₀)), (c_m − 2κ)/(2[16(1 + 2A) + c_m])} ∈ (0, ½). Then
(1 − ε₁)(1 + ε₀) ≥ (1 + ε₁) + ε₀/2 ≥ (1 + ε₁)(1 + ε₀/3) and **[8(1 + 2A) + c_m/2]·ε₁ ≤ (c_m − 2κ)/4.**                         [R-8]
*Step 1 (table ratio).* By (TK-d): log[r_b(U)/r_b(T)] = ½(d − a) log(n + 1) − (A₁ − A₂) + (R_U − R_T), where
A₁ := ν log(RSS_U/RSS_W) ≥ 0, A₂ := ν log(RSS_T/RSS_W) ≥ 0, |R_U − R_T| ≤ 2κ_E.
*Step 2 (A₁ from below).* By (TK-e), (Q±) and 𝓧: RSS_U − RSS_W = ‖(P_W − P_U)(μ + ε)‖² ≥ (1 − ε₁)L₁ − σ²ζ_n/ε₁. By (f1) and
σ² ≤ τ²_U: A₁ ≥ (1 − ε₁)L₁/(2τ²_U(1 + ω_n)) − ζ_n/(2ε₁).
*Step 3 (A₂ from above).* RSS_T − RSS_W ≤ (1 + ε₁)L₂ + (1 + 1/ε₁)σ²ζ_n; by (f2) and σ² ≤ τ²_W:
A₂ ≤ (1 + ϑ_n)(1 + ε₁)L₂/(2τ²_W) + (1 + ϑ_n)(1 + 1/ε₁)ζ_n/2. (No smallness of the gains of N is needed: (f2) is exact in
this direction, and it is the reason why τ²_W stands on the right of (V-mp).)                                            [R-9]
*Step 4.* Put 1 + ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)) for n ≥ n₁; then ϑ_n ≤ ϑ̄_n → 0, and ϑ̄_n depends only on (n, A).
Multiply (4.1⁺⁺) by (1 − ε₁)/(2(1 + ω_n)) > 0 — this needs no sign of π + c_m log n —, insert in Step 2 and subtract Step 3:  [R-10]
  A₁ − A₂ ≥ (1 − ε₁)(π + c_m log n)/(2(1 + ω_n)) + [L₂/(2τ²_W)]·[(1 − ε₁)(1 + ε₀)/(1 + ω_n) − (1 + ϑ_n)(1 + ε₁)] − C₁ζ_n,   [R-11]
C₁ := 1/(2ε₁) + (1 + 1/ε₁) (for ϑ_n ≤ 1). For n ≥ n₃ we have (1 + ω̄_n)(1 + ϑ̄_n) ≤ 1 + ε₀/3, so the second bracket is ≥ 0
(L₂ ≥ 0), and, with **θ_n := (1 − ε₁)/(1 + ω_n) ∈ [(1 − ε₁)/(1 + ω̄_n), 1]**:                                              [R-12]
  A₁ − A₂ ≥ ½θ_n(π + c_m log n) − C₁ζ_n.                                                                             [R-13]
*Step 5 (price, exact).* Π := log ω^Q(U) + ½(d − a) log(n + 1), ω^Q(U) = (2p)^{(d−a)₊}(c_Q/p)^{(a−d)₊} (BASE `STATEMENT.md:93`).
If d ≥ a: Π = (d − a)[log(2p) + ½ log(n + 1)] = ½(d − a)(log n + 2 log p) + (d − a)[log 2 + ½ log(1 + 1/n)]
  ≤ ½π + C₂,   C₂ := 16(log 2 + ½ log(5/4))   (d − a ≤ |V| ≤ 16, n ≥ 4).                                              [R-14]
If a > d: Π = (a − d)[log(c_Q/p) − ½ log(n + 1)] ≤ −½(a − d)[log n + 2 log(p/c_Q)] = ½π   (log(n + 1) > log n; c_Q ≥ 16 > 0
as s₀ ≥ 1; **the sign of log(p/c_Q) is not used**). In both cases **Π ≤ ½π + C₂**.                                        [R-15]
*Step 6.* log[ω^Q(U)r_b(U)/r_b(T)] = Π − (A₁ − A₂) + (R_U − R_T) ≤ F + C₂ + C₁ζ_n + 2κ_E, where                              [R-16]
  F := ½π − ½θ_n(π + c_m log n) = ½(1 − θ_n)π − ½θ_n c_m log n.                                                      [R-17]
(a) π < 0: (1 − θ_n)π ≤ 0 (θ_n ≤ 1), so F ≤ −½θ_n c_m log n ≤ −(1 − ε₁)c_m log n/(2(1 + ω̄_n)).                              [R-18]
(b) π ≥ 0 (then π + c_m log n > 0, and the lower bound on θ_n is applied to a non-negative quantity): π ≤ 16(1 + 2A) log n —  [R-19]
if d ≥ a, π = (d − a)(log n + 2 log p) ≤ 16(1 + 2A) log n (p ≤ n^A); if a > d, π ≤ 0 by (R1.0) (n ≥ n₃ ≥ 256s₀²), so π = 0.  [R-20]
With 1 − θ_n = (ε₁ + ω_n)/(1 + ω_n) ≤ ε₁ + ω̄_n: F ≤ 8(1 + 2A)(ε₁ + ω̄_n) log n − (1 − ε₁)c_m log n/(2(1 + ω̄_n)).            [R-21]
In both cases, since (1 − ε₁)/(1 + ω̄_n) ≥ 1 − ε₁ − ω̄_n and by the choice of ε₁:                                        [R-22]
  F ≤ −(c_m/2) log n + [8(1 + 2A) + c_m/2](ε₁ + ω̄_n) log n ≤ −((c_m + 2κ)/4) log n + [8(1 + 2A) + c_m/2]ω̄_n log n.            [R-23]
Since (c_m + 2κ)/4 > κ, ω̄_n log n → 0 and ζ_n = o(log n), F + C₂ + C₁ζ_n + 2κ_E ≤ −κ log n − 16 log 2 for n ≥ n₃.            [R-24]
*Step 7.* For fixed T′ the sum defining Ξ_b(Q) has at most 2^{16} terms (U ⊆ C_b), each ≤ 2^{−16}n^{−κ}. ∎
*The threshold.* n₃ := the least m ≥ max(n₁, 256s₀², 4) such that for every n ≥ m: ϑ̄_n ≤ 1, (1 + ω̄_n)(1 + ϑ̄_n) ≤ 1 + ε₀/3,
and ((c_m − 2κ)/4) log n ≥ [8(1 + 2A) + c_m/2]ω̄_n log n + C₂ + C₁ζ_n + 2κ_E + 16 log 2. It exists (the left side grows like
log n, the right side is o(log n)) and depends only on (κ, A, s₀, c_m, ε₀, κ_E) and the envelopes ω̄_n, ϑ̄_n; under (E),
(GF-16) only on (κ, A, M, σ², g_*, s₀, c_m, ε₀).                                                                     [R-25]

## R1.3 Bridge (B-V1⁺⁺): constant level c_V log n + 2 log p — copy of BASE L4.2 (BASE `lemmas/L4_VIS.md:57-73`)

**Proposition R1.3.** Assume (V-cp) at n with c_V > 1; κ_V := (c_V − 1)/2; let κ ∈ (0, κ_V). There is                     [R-26]
n₄ = n₄(κ, A, M, σ², g_*, s₀, c_V) such that for n ≥ n₄, on 𝓔^blk ∩ 𝓧: **e_n ≤ 2^{−16}n^{−κ}**, and therefore, on
𝓔^blk ∩ 𝓧 ∩ {c_QU_Q ≤ 1}: **Ξ(Q) ≤ n^{−κ}**.

*Proof.* Let b be a truth block, U ⊆ C_b, j ∈ U*_b ∖ U. Then U ⊆ [p] ∖ {j}, |U| ≤ 15, so (V-cp) gives δ²_{U,j} ≥ τ²_U·G, with   [R-27]
**G := c_V log n + 2 log p**, 0 ≤ G ≤ (c_V + 2A) log n (1 ≤ p ≤ n^A). By (TK-d),                                        [R-28]
log[r_b(U)/r_b(U ∪ j)] = ½ log(n + 1) − ν log(RSS_U/RSS_{U∪j}) + (R_U − R_{U∪j}). By (TK-e), (Q±), 𝓧:
RSS_U − RSS_{U∪j} = (δ_{U,j} + σZ_{U,j})² ≥ (1 − ε₁)δ²_{U,j} − σ²ζ_n/ε₁ ≥ τ²_U[(1 − ε₁)G − ζ_n/ε₁]. By (f1), since the left side is  [R-29]
≥ 0: ν log(RSS_U/RSS_{U∪j}) ≥ [(1 − ε₁)G − ζ_n/ε₁]₊/(2(1 + ω̄_n)) ≥ (1 − ε₁)G/(2(1 + ω̄_n)) − ζ_n/(2ε₁). With               [R-30]
ε₁ := min{½, (κ_V − κ)/(2(c_V + 2A))}, (1 − ε₁)/(1 + ω̄_n) ≥ 1 − ε₁ − ω̄_n, and **G/2 = (c_V/2) log n + log(2p) − log 2**:    [R-31]
  log[r_b(U)/r_b(U ∪ j)] ≤ ½ log(n + 1) − G/2 + (ε₁ + ω̄_n)G/2 + ζ_n/(2ε₁) + 2κ_E                                      [R-32]
   ≤ −log(2p) − [(c_V − 1)/2 − (κ_V − κ)/4] log n + ((c_V + 2A)/2)ω̄_n log n + ζ_n/(2ε₁) + 2κ_E + ½ log(5/4) + log 2           [R-33]
   ≤ −log(2p) − [κ_V − (κ_V − κ)/2] log n − 16 log 2   for n ≥ n₄.                                                    [R-34]
Now let U ⊆ C_b with a′ := |U*_b ∖ U| ≥ 1; add the missing truths one at a time, U = U⁰ ⊂ U¹ ⊂ ⋯ ⊂ U^{a′} = U ∪ U*_b. Each
step is of the kind just bounded (U^{i} ⊆ C_b ∖ {j_{i+1}}, |U^i| ≤ 15), so                                                  [R-35]
[r_b(U)/r_b(U ∪ U*_b)]^{1/a′} ≤ (2p)^{−1}·2^{−16}n^{−(κ_V+κ)/2}, and e_n ≤ 2p·(2p)^{−1}·2^{−16}n^{−(κ_V+κ)/2} = 2^{−16}n^{−(κ_V+κ)/2}  [R-36]
≤ 2^{−16}n^{−κ}. (The factor 2p of e_n is paid by the term 2 log p of the level, exactly; no use of p ≤ n^A is made here.)   [R-37]
In particular e_n ≤ 1, and (AGG-d) (BASE `lemmas/L1_AGG_FLOOR.md:103-109`, which needs c_QU_Q ≤ 1) gives
Ξ_b(Q) ≤ 2^{16}max(e_n, e_n^{16}) = 2^{16}e_n ≤ n^{−κ}. ∎
*The threshold.* n₄ := the least m ≥ max(n₁, 4) such that for every n ≥ m:
((κ_V − κ)/4) log n ≥ ((c_V + 2A)/2)ω̄_n log n + ζ_n/(2ε₁) + 2κ_E + ½ log(5/4) + 17 log 2. It depends only on (κ, A, s₀, c_V,
κ_E) and ω̄_n; under (E), (GF-16) only on (κ, A, M, σ², g_*, s₀, c_V).                                                 [R-38]
(The bound ε₁(c_V + 2A)/2 ≤ (κ_V − κ)/4 gives the second line; the third holds when the threshold inequality does.)        [R-39]

## R1.4 Corollary L4.3⁺⁺ and the interface claims VIS-c⁺⁺, VIS-m⁺⁺

**Corollary R1.4 (= BASE L4.3, BASE `lemmas/L4_VIS.md:75-78`, under (V-cp)).** If (V-cp) holds for all large n and (AL)
holds for Q with level vector h, and [LEAK(Q)] holds, then P(Ξ(Q) > n^{−κ}) → 0 for every κ < κ_V = (c_V − 1)/2.            [R-40]
*Proof.* (AL): b_n(h) → 0 and ϱ_n(Q; h) → 0. By (B1)(i) (BASE `lemmas/L3_LEAK.md:34`), (|Q| + 1)n^{−1/2}𝔏^b_n(Q; h) ≤ ϱ_n(Q; h)
→ 0, so the premise of [LEAK(Q)] (BASE `STATEMENT.md:183`) holds and U_Q = O_P(n^{−1/2}𝔏^b_n(Q; h)). By (e1) (BASE
`lemmas/L5_ASM_STARTF.md:11`), c_Q ≤ 16s₀′(|Q| + 1), so c_QU_Q = O_P(ϱ_n(Q; h)) → 0 in probability and P(c_QU_Q > 1) → 0. By
Proposition R1.3, for n ≥ n₄: P(Ξ(Q) > n^{−κ}) ≤ P((𝓔^blk)ᶜ) + 1/log n + P(c_QU_Q > 1) → 0. ∎                                  [R-41]

**[VIS-c] (B-V1⁺⁺)** (`STATEMENT.md:101-106`). Setting F, Q, (V-cp), [TK] (quantitative), [LEAK(Q)], (AL). For κ < κ_V,
Proposition R1.3 gives, for n ≥ n₄, P(e_n > n^{−κ}) ≤ P((𝓔^blk)ᶜ) + P(𝓧ᶜ) ≤ P((𝓔^blk)ᶜ) + 1/log n → 0, and Corollary R1.4
gives [VIS(κ; Q)]. The refinement is Proposition R1.3 as stated, with the threshold n₄ of R1.3 and P((𝓔^blk ∩ 𝓧)ᶜ)
≤ P((𝓔^blk)ᶜ) + 1/log n (R1.1). ∎
**[VIS-m] (B-V2⁺⁺)** (`STATEMENT.md:108-111`). Setting F, Q, (V-mp) with this Q, [TK] (quantitative). Proposition R1.2: for
κ < κ_V = c_m/2 and n ≥ n₃, Ξ(Q) ≤ n^{−κ} on 𝓔^blk ∩ 𝓧, so P(Ξ(Q) > n^{−κ}) ≤ P((𝓔^blk)ᶜ) + 1/log n → 0: [VIS(κ; Q)]. The
refinement is Proposition R1.2 as stated. ∎
(As in BASE `lemmas/L4_VIS.md:84-85`: both propositions hold on 𝓔^blk ∩ 𝓧, which does not depend on (κ, c_V, c_m, ε₀), and
n₃, n₄ depend only on the fixed constants; this gives the uniformity used in (T1⁺⁺)(d).)

## R1.5 Theorem START-F (T1⁺⁺): PARENT P1.4–P1.5 with (D3)

**Where visibility enters the parent proofs.** In BASE Proposition L5.2 (BASE `lemmas/L5_ASM_STARTF.md:37-67`), which PARENT
Proposition P1.4 (PARENT `lemmas/P1_LEADING.md:80-104`) takes over with its constants and threshold, visibility enters at
exactly these places: (1) the exponent κ_V (BASE `lemmas/L5_ASM_STARTF.md:39`) and the admissibility clause "the visibility
condition" (`:45`); (2) the threshold n₀ ≥ n₃ or n₄ for the exponent κ′ = (κ + κ_V)/2 (`:49`); (3) "(B1) … the visibility
condition holds for the block instances" (`:51`); (4) the bound Ξ(Q) ≤ n^{−κ′} on 𝒢 by L4.1 or L4.2 (`:61`). Nothing else in
L5.2, L5.3 (`:72-89`), L6.0, L6.0′ (BASE `lemmas/L6_COROLLARIES.md:9-26`), P1.4 or P1.5 (PARENT `lemmas/P1_LEADING.md:80-126`)
refers to visibility: λ, c₀, C, C′, C^♯, the events 𝓔^blk, 𝓧, 𝓩_h, 𝓜, 𝓜₀, 𝓜^♯, their probability bounds, the Markov steps,
(AGG-a), (AGG-b), (e2), (e3) and (1.2) of PARENT do not.
**Proposition R1.5 (= BASE L5.2 = PARENT P1.4, under (D3)).** Replace (1)–(4) as follows and keep every other line.
(1) Fix (A, M, σ², g_*, s₀) and either c_V > 1 (κ_V := (c_V − 1)/2) or (c_m, ε₀) (κ_V := c_m/2); admissibility asks
"(V-cp) with c_V, or (V-mp) with (c_m, ε₀) for this Q" at n.                                                            [R-42]
(2) n₀ ≥ max(n₂, n₃ (R1.2) or n₄ (R1.3) for the exponent κ′, 2s₀ + 2), with the other requirements of BASE
`lemmas/L5_ASM_STARTF.md:49-50` unchanged.                                                                         [R-43]
(3) (B1) for (D3): R1.1.                                                                                         [R-44]
(4) On 𝒢 ⊆ 𝓔^blk ∩ 𝓧, where c_QU_Q ≤ 1 (BASE `lemmas/L5_ASM_STARTF.md:60`): Ξ(Q) ≤ n^{−κ′} by Proposition R1.2 (under (V-mp))
or R1.3 (under (V-cp); c_QU_Q ≤ 1). κ′ ∈ (0, κ_V) as required by R1.2, R1.3.                                          [R-45]
Then the conclusions (i), (ii) of P1.4 hold, with the same C, c₀, C^♯ (depending only on ε, s₀, κ_E) and n₀ depending only
on (ε, κ) and (A, M, σ², g_*, s₀, c_V) or (A, M, σ², g_*, s₀, c_m, ε₀). ∎
**Thresholds that change, and nothing else.** BASE Lemma L6.0 (BASE `lemmas/L6_COROLLARIES.md:11-17`) holds with n₃, n₄ of
R1.2, R1.3 in n*(κ); the requirements in n_ε are unchanged. Corollary L6.0′ (`:19-26`) and its PARENT form (PARENT
`lemmas/P1_LEADING.md:106-111`) hold verbatim (they use only L6.0). No other threshold or constant changes.               [R-46]
**(T1⁺⁺)(a)–(d)** (`STATEMENT.md:113-125`). Setting F, (E), (GF-16) (hence [TK] in quantitative form, BASE
`lemmas/L2_TK.md:94-98`), (V-cp) or (V-mp) (with this Q), (AL) for Q with level vector h; κ ∈ (0, κ_V) with κ_V of (D3).
(a), (b), (c), (d) are PARENT P1.5 (PARENT `lemmas/P1_LEADING.md:113-126`) word for word with Proposition R1.5 in place of
P1.4 and of BASE L5.2: (a) is BASE L5.3(a) (BASE `lemmas/L5_ASM_STARTF.md:76-79`); (b) the argument of P1.5(b) with
R1.5(ii); (c) BASE L5.3(c) (`:84-88`), which uses the event 𝒢 of L5.2 only through the bounds on U and Ξ, here with an
exponent κ′ ∈ (½, κ_V) (possible because κ_V > ½ is assumed for the κ_V of (D3)); (d) Proposition R1.5 with the constant
max(C, C^♯) in both displays: C, c₀ depend only on (ε, s₀, κ_E(g_*, M, σ²)), and n₀ on (ε, κ) and the fixed constants
(A, M, σ², g_*, s₀ and c_V or (c_m, ε₀)) — the visibility constants of (D3) enter only through n₃ or n₄. ∎               [R-47]
(Under (V-mp), the admissible tuples of (d) satisfy (V-mp) with their own Q, and R1.2 is applied with that Q; c_Q is that
Q's. The proof of R1.2 is deterministic in the design, so no uniformity issue arises.)                                  [R-48]

## R1.6 Remarks

1. Under (V-mp), the a > d instances are charged −(a − d)(log n + 2 log(p/c_Q)): Step 5 keeps this exactly and Step 6(a)
   uses only θ_n ≤ 1. The sign of log(p/c_Q) is never used; (R1.0) is used only in Step 6(b) to see that π ≥ 0 forces
   π ≤ 16(1 + 2A) log n, which is where p ≤ n^A enters R1.2.
2. Under (V-cp), p ≤ n^A enters R1.3 only through 0 ≤ G ≤ (c_V + 2A) log n, used to make ε₁G and ω̄_nG negligible; the
   factor 2p of e_n is cancelled by the level exactly, which is why κ_V = (c_V − 1)/2 does not involve A.
3. Count of changed lines: R1.1 2, R1.2 23, R1.3 14, R1.4 2, R1.5 7 — 48 tags in all.
