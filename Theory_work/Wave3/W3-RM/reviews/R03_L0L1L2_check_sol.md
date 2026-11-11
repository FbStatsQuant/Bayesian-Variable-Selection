# R03 — independent line-by-line check of L0, L1 and L2

Reviewer: Codex gpt-6.1-sol, high effort. Scope: locked STATEMENT v1.1, (C0), (C1), (B1)–(B6), and the specified source contracts. No source file or git state changed. E4 is used only at its statement/integration interface; its proof is outside this review.

## Verdicts

- Theorem RM-0(a): VERIFIED.
- Theorem RM-0(b): VERIFIED.
- Lemma B1: VERIFIED.
- Lemma B2: VERIFIED.
- Lemma B3: VERIFIED.
- Corollary B3′: VERIFIED.
- Lemma B4: VERIFIED.
- Bridge B6: VERIFIED, conditional on the cited T03♯ input with its recorded status.
- Lemma NA-F (B5): VERIFIED-WITH-AMENDMENTS (minor empty-family convention only).
- Lemma N-loc ⇒ (N-D)(i): VERIFIED-WITH-AMENDMENTS (same minor empty-family convention).
- Theorem RM-F: VERIFIED, conditional on the cited inputs and E4 contract.

No FATAL or MAJOR findings. These are verdicts on the arguments reviewed here, not upgrades to any cited result's recorded status.

## 1. Theorem RM-0(a) — VERIFIED

No adverse finding.

At `lemmas/L0_core.md:30-34`, E4 supplies membership in the set of maximisers, and Sand is explicitly about **every** maximiser. Thus no uniqueness or prescribed lexicographic maximiser is needed. The resulting centre belongs to the whole feasible lattice since |Q| ≤ K.

The cap satisfies ℓ_n + |S̃₀| ≥ |S̃₀| ≥ |S̃₀ ∖ S₀|. GROW `lemmas/L1_descent.md:42-56` explicitly covers both the path and the extra terminal scan at a cap equal to the move count. Here the positive ℓ_n even gives spare cap. The zero-extra case is covered by GROW L1.1(b), L1.2(ii)'s emitted-centre clause, and E4's integration statement: zero moves, S₀ already scored, and the initial completed scan finds no improvement. This proves the complement inclusion with the stated hypothetical-search convention on enumeration branches.

The source pointer to GROW line 10 in the introductory input list is one line before the actual setting at line 11; the intended contract is unambiguous and no correction is needed for the mathematics.

## 2. Theorem RM-0(b) — VERIFIED

No adverse finding.

At `lemmas/L0_core.md:45-54`, the pathwise premises have distinct, sufficient roles:

1. GUARD-W excludes an interrupted LS0 on an output run; the configured OP-LS0 supplies execution from the emitted coded centre and complete scans.
2. E4 identifies this centre, its emission, and its determinism from the data/tables. The deterministic search and fixed options give the same hypothetical score set for all admissible run parameters. A different random scored set from the surrounding SMC does not matter.
3. OP-LS0 puts every LS0-scored model in the all-scored set. On the exact branch feasibility of S₀ is sufficient instead.
4. EX-A/EX-S/SR make reporting a maximum of the exact F score over that scored set. For the posterior normalised over Ω, π(S)/π(S₀) = exp(F(S) − F(S₀)). If π(S₀) > 1/2, every other posterior mass is at most 1 − π(S₀) < π(S₀), so the maximiser is strict. No tie issue remains.

DLV `lemmas/L4_delivery.md:65-77` states and proves exactly this inclusion and explicitly removes CAL from this pathwise route. GEN `lemmas/L5_assembly.md:11-16` supplies the matching operational closure, including the exact branch. The Markov inequality and union bound in L0 are correct. The common good data event avoids taking a measurable uncountable union over calibration outcomes. The last probability identity concerns each admissible run's own output event; it asserts no delivery result. CAL is unnecessary here; the optional M5(0) route retains its own recorded premises.

E4 `lemmas/L5_E4.md:90-111` has the maximiser/integration contract consumed here, under H1⁺, H2, H3, H4, with the integration cap satisfying H3. This review does not certify its proof.

## 3. Lemma B1 — VERIFIED

No adverse finding.

At `lemmas/L1_fixed.md:13-17`, each block subset has at most 16 elements and each conditioning subset at most 15. Truth-containing conditioning sets are allowed by (V), and (L-gain) quantifies over more conditioning sets than (G3c). FL-16 ensures all directions used here exist. GROW `STATEMENT.md:92-95` confirms the quoted G3 quantifiers. FL-Q is carried separately, as required by the definition of FL_b; it is not purportedly deduced from FL-16.

## 4. Lemma B2 — VERIFIED

No adverse finding. I rechecked the whole GROW L3 proof, rather than only its four displayed citations.

At `lemmas/L1_fixed.md:34-44`, the claimed delta is valid:

1. **Counting bound.** GROW `L3_sandwich.md:36-38` gives k̃ ≤ k₀ + B times the number of occupied good junk blocks, k₀ = q + 16s₀. This holds for arbitrary q. At most s₀ bad blocks contribute at most 16s₀ elements; membership in Q accounts for at most q more.
2. **Ladder and its constants.** At GROW lines 54-70, ε₁ is chosen solely from A and η. Since η < η_A, it can be fixed positively, including when η = 0. With ε₂ = (1 + ϑ_n)(1 + ε₁) − 1, eventually ε₂ ≥ ε₁ > 0 and ε₂ has a fixed upper bound. Consequently the geometric-series constant is uniformly bounded in n. The exponent ξ/(1 + ε₂) stays bounded away from zero. The discarded factor k₀^{−ε₂/(1+ε₂)} is at most one for every q. No logarithmic upper bound on q enters this step, and no factor proportional to the number of ladder rungs is lost.
3. **Events and union bounds.** GROW lines 17-26 use only the block families: ≤ 2^16 p models, ≤ 2^20 p directions, and ≤ 3^16 projector pairs per block. Their dimensions stay ≤ 16; none grows with q. The threshold τ_n(k) ≥ 3 follows at lines 54-57 from 1 − η₁ ≥ 2Aε₂ + 2ξ₀ > 0 and log(p/k) ≥ 0 for k ≤ p. Its upper bound is also independent of q. The ladder's count events cover all maximisers simultaneously (lines 71-72). Thus the enlarged 𝒢_n at line 76 still has probability tending to one.
4. **Feasibility and Q = [p].** GROW lines 78-79 need only q ≤ K and the alternative in L-feas. If Q = [p], q = p ≤ K ≤ p, so K = p; a saturated maximiser already contains every truth. If it is not saturated, a truth can be added. For Q ≠ [p], k̃ ≤ 2q + 32s₀ < K. Truth inclusion uses M_n → ∞ and a block Gaussian maximum of order log n, with no further q dependence.
5. **Junk exclusion.** GROW lines 86-93 leave a positive fixed multiple [1/2 − η/2 − √(2Aη)] log n, less log k̃ and terms o(log n). The new bound log k̃ ≤ log(2q + 32s₀) = o(log n) suffices. Q = [p] needs no junk exclusion.

These account for the four uses listed by B2 and the possible hidden dependencies asked about. L0 is indeed used only on the bounded block family here. In particular B2 does not require the lattice toolkit or FL-Q; its weaker listed assumptions suffice.

## 5. Lemma B3 and Corollary B3′ — VERIFIED

No adverse finding.

At `lemmas/L1_fixed.md:54-59`, write f = |𝔉| and v = |𝒱𝒱|. The stated bounds give

    log f ≤ q log 2 + log(1 + (1+s₀)(1+p)) = O(q + log n),
    log v ≤ log 2 + 2 log f,
    t_n + h_n² ≤ 8 log f + 10 log n + 4q + 4 + 2 log 2
                 ≤ C₁(A,s₀)(q + log n).

Thus (1.1) uses actual cardinalities, not the inflated toolkit envelope. Every nonempty family member lies in some Q ∪ {l}; FL-Q and interlacing provide the common floor. The family is deterministic, contains ∅, and the vector family contains both the residuals and all contrasts. All three envelope quantities fit (log n)^{κ+1} eventually. LOC2 `L1_toolkit.md:10-32` therefore applies exactly as stated. Constants multiplying (log n)^κ and the extra +1 are absorbed by the envelope exponent; they do not change the actual t_n and h_n.

At lines 62-69, A contains all truths except i, so r_A = θ*_i(I − P_A)x_i. The Schur complement lower bound uses A ∪ {i} ⊆ Q ∪ {l}, including the swap case. Since (n−1)/n → 1, BM-Q makes L′_n/[σ²(q + log n)] diverge. Hence eventually L′_n ≥ 4σ²(2h_n²+t_n), uniformly over the finite family at that n, and the displayed RSS contrast is ≥ Λ_A/4. BM-Q also implies L′_n/log n → ∞, which pays for the prior and dimensional penalty in the final score comparison.

LOC2 lines 33-36 themselves assert only fixed beta-min, not general BM-∞. B3 correctly supplies the additional domination argument and does not misquote that assertion. GROW L2.1 lines 27-34 supply the rest of the comparison. For q ≤ C log n, q+log n ≤ (C+1)log n, so BM-∞ implies BM-Q and B3′ follows, including q ≤ s₀+log n under N-χ.

## 6. Lemma B4 — VERIFIED

No adverse finding.

At `lemmas/L1_fixed.md:76-78`, N-χ implies q ≤ s₀ + (1−δ₀)log n ≤ (s₀+1)log n eventually, so the source lattice family fits the original logarithmic toolkit. GROW `L2_NA_TL.md:54-65` bounds every direction by at most p reference normal squares plus one common chi-square of rank q−s₀. The resulting leading excess is at most (1−δ₀)log n, leaving δ₀log n to absorb the square-root and log-log terms and the constants in c_n. FL-Q supplies full rank. The NA reduction at source lines 38-46 needs no beta-min. B4's omission of BM-∞ is therefore legitimate.

## 7. Bridge B6 — VERIFIED (conditional on the cited input)

No adverse finding.

At `lemmas/L1_fixed.md:80-82`, T1-F explicitly invokes H0, which GROW `STATEMENT.md:84-88` identifies as the T03♯ hypotheses. GEN L5 line 10 and GROW L4 line 10 record the quoted stochastic rate and the cited status. It tends to zero; since the posterior error lies in [0,1], convergence in probability implies convergence of expectations (e.g. Eδ ≤ ε + P(δ>ε)). No extra uniform integrability assumption is needed. This verifies the bridge using the inherited T03♯ contract, not a fresh proof of T03♯.

## 8. Lemma NA-F — VERIFIED-WITH-AMENDMENTS

1. **MINOR — empty-family branch.** Location: `lemmas/L2_NAF.md:17,28-30`, also `:57,64`. The statement explicitly allows 𝔓 = ∅, but the subsequent proof uses log|𝒰_n| and a maximum over 𝒰_n without defining empty-set conventions. The N-loc construction can actually produce 𝒰_n = ∅. Example: fixed p = s₀ = 1, Q = S₀ = [p], a centred standardised nonzero column, n ≥ 3. FL-Q holds, the lattice is {S₀}, and there are no (T,l). Then N₁ = ∅, ρ_n = 0 satisfy N-loc, but the constructed 𝒰_n is empty and its logarithm is not a real number. This does not refute the NA conclusion: there are no additions, so NA is automatic. **Fix:** handle 𝔓 = ∅ before Step 0, and in N-loc choose an arbitrary deterministic singleton of unit vectors in this branch (the span/approximation condition has no pairs to check). Alternatively state explicit extended-real/empty-maximum conventions. No changed rate or nondegenerate-case proof is required.

Apart from finding 1, Steps 0–4 check out line by line:

- **Step 0, lines 19-21:** interlacing on Q ∪ {l} gives full rank of T ∪ {l}, hence a nonzero residual and a well-defined unit direction. Centring puts that direction orthogonal to the intercept; since T contains S₀, it is orthogonal to μ as well. Thus Z is precisely the standard Gaussian noise coordinate needed for GROW's F2 and the score conversion.
- **Step 1, lines 23-26:** both vectors lie in V_l by hypothesis, so w = Π_lw and wᵀε = wᵀΠ_lε. Cauchy–Schwarz gives (2.1) with the stated ρ_n and no extra constant.
- **Step 2, lines 28-34:** the deterministic unit-vector family gives the normal union bound 1/log n. There are at most p distinct deterministic projectors: p−q outside columns plus the common Π_Q for all q ≥ 1 inside columns. Full rank actually gives d_l = q+1 outside Q and q inside Q; the weaker bound d_l ≤ q+1 suffices. Laurent–Massart applies to ε/σ and the deterministic orthogonal projector. The inequality 2√(dx) ≤ d+x gives d+2√(dx)+2x ≤ 2d+3x, exactly the stated G_n. For n large enough x and all thresholds are positive. Neither union bound uses independence.
- **Step 3, lines 36-42:** a_n² ≤ 2log p + o(log n) and a_n² = O(log n). Meanwhile G_n = O(q+log n), so ρ_n²G_n = o(log n), and the mixed term is o(log n) by its square-root product bound. Thus the entire bound is 2log p + o(log n). The gap in c_n is log n − O(log log n), since q ≤ (log n)^κ, and eventually dominates this deterministic remainder. The displayed probability ≥ 1−2/log n is valid for the maximal-Z assertion once n passes the sequence-dependent onset.
- **Step 4, lines 44-46:** LOC2 `L1_toolkit.md:28-32` supplies the actual lattice-family construction and event. Lines 37-42, specifically, prove the polylogarithmic version of GROW L2.2, including the essential rate ω_n log n → 0 and the final strict score margin −1/2. Thus this is an exact match to the cited conversion, rather than an extrapolation from LOC2's fixed-beta-min TL result. Adding the toolkit failure probability proves P(NA) → 1. The full NA probability is not claimed to be ≥ 1−2/log n without that additional event.

**Onset qualification (not an adverse finding).** The n₀ in Step 3 necessarily depends on the deterministic asymptotic envelopes in N-D, on κ and on the fixed constants (including κ_E). There is no universal onset over all sequences satisfying unspecified little-o rates: one can postpone their decay to any prescribed index. The text states only an eventual result for the given sequence and is valid on that reading. For clarity, the author may explicitly say “n₀ depending on the rate envelopes.” Within each sequence it is common to every (T,l), seed and other admissible run parameter.

## 9. Lemma N-loc ⇒ (N-D)(i) — VERIFIED-WITH-AMENDMENTS

Finding 1 above is the only amendment.

At `lemmas/L2_NAF.md:59-64`, N ⊆ T implies nested projector ranges even without appealing to rank. Therefore P_T−P_N is the orthogonal projector onto span X_T minus span X_N, b lies in span X_T, and a is orthogonal to b. FL-Q makes a nonzero. The identity

    ||u_{T,l} − u_{N,l}||² = 2(1 − 1/sqrt(1+t²)),  t = ||b||/||a||,

is exact. Convexity of (1+x)^(−1/2), or its tangent at x=0, gives (1+t²)^(−1/2) ≥ 1−t²/2 for all t ≥ 0, so the bound uses the same ρ_n without a factor 2. The approximant lies in span X_{N∪{l}} ⊆ span X_{Q∪{l}}. For each l it depends on at most 2^{|N_l|} possible intersections. Thus the union has at most p2^{ν_n} vectors, and its log cardinality is ≤ log p + ν_n log 2. Fixed X, deterministic N_l and deterministic Q make the family deterministic; it need not be independent of X in this fixed-design setting.

The special cases at lines 66-69 are correct:

- (a) q=o(log n): N_l=Q∖{l} gives T∩N_l=T for each applicable pair, zero error, and ν_n≤q.
- (b) GROW G4-dir directly supplies the exact family; it is properly distinguished from an N-loc implication. Each exact direction already lies in the required span.
- (c) Write E=span X_Q minus span X_{S₀}. Outside columns are orthogonal to E. The residualised extra columns inside Q are pairwise orthogonal. Adding any eligible extras to S₀ therefore does not change the residual of x_l, either for l outside Q or for an unselected extra inside Q. There are no eligible truth l. Hence u_{T,l}=u_{S₀,l} and at most p directions suffice.

**Independent numerical falsification attempt.** Ran an inline Python/numpy probe using `py -3.13`, without writing a script or output file. Ten independently generated centred Gaussian designs, n=36, p=9, Q={0,…,4}, S₀={0}; enumerated all 16 lattice models and every eligible l, with N=T∩{j∈Q∖{l}: j even}. Total: 960 pairs. Maximum |aᵀb|=3.192e−15; maximum identity error=2.093e−16; no positive violation of the squared-distance bound, decomposition bound, or squared maximal-coordinate bound (to floating-point precision). This supports only the identities/inequalities, not the asymptotic assumptions. Also read the supplied f1 probe and recorded output: its 60 runs report zero violations; I did not rerun it or alter its output.

## 10. Theorem RM-F and locked-statement coverage — VERIFIED

No adverse finding affecting assembly.

At `lemmas/L1_fixed.md:86-93`, every bridge hypothesis is supplied:

1. T1-F supplies energy, polynomial p, BM-∞ and the posterior theorem's full H0 contract. The coded partition is deterministic given the fixed design and has blocks at most 16.
2. B1 supplies G3a/V_b/L_b; L-size implies log q=o(log n); L-feas supplies q≤K and B2's feasibility alternative. B2 yields SAND.
3. FL-Q supplies the common lattice floor. Under N-χ, q=O(log n) and BM-∞ imply BM-Q, so B3′ yields TL. Under N-D, BM-Q is explicitly N-D(ii), so B3 applies. No automatic BM-∞ to BM-Q implication at arbitrary polylog q is used.
4. B4 yields NA under N-χ, and NA-F yields NA under N-D(i). B6 yields POST. The configured RM-0 and E4 contract supply the conclusion.
5. The block-relative variant retains FL-Q via FL_b. Replacing B1 by G3a/V_b/L_b therefore removes none of the lattice assumptions needed by B3–B5.
6. On the stated intersection event, exactly |S̃₀∖S₀| moves occur. Under N-χ this is ≤(1−δ₀)log n<log n; the high-probability assertion follows from the three interfaces. Enumeration is correctly described as hypothetical search.

Consequently the reviewed files prove (C0), (C1) and bridges (B1)–(B6) in locked STATEMENT `:142-162,172-177`, subject to the cited input statuses and the minor empty-family convention above. They do not assert delivery, binary64 correctness, or removal of N; none is needed for these claims. C2 and B7 onward are outside this review. E4's proof and example/sharpness claims are likewise not certified here.

## FATAL / MAJOR findings

None.
