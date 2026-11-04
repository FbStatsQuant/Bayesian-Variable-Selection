# Fable 5.1 review of HQ's paper selection (2026-10-28)

Consultant: Fable 5.1 (independent of the second consultant). Inputs: PROPOSAL.md, BRIEFING §2/§4/§5, THEORY_INVENTORY, theorem files T01–T36, THEOREM_MAP. Read-only; no jobs run.

**Verdict in one line: ENDORSE WITH CHANGES.** The story (consistency because the truth is *scored*) is right and sellable. Two of the eight need restating before the campaign, the pool is missing one type of result (a finite-n repair guarantee), and I propose one new conjecture to fill it.

---

## 1. Critique of the selection

**Change A (matters most): Thm 6 = T26 is the wrong main theorem as written.** T26 reaches the HPM through clause (iii): start concentration makes an initial π₀ draw equal S₀ with probability → 1. A referee will ask why the SMC bridge, Gibbs rounds and local search exist, since the block-wise start already solves the problem. In the only regime where the sampler does work (the masked regime of T27, start mass p⁻ᶜ n⁻ᶜ/²), T26 says nothing. Its hypothesis list (G, R, SE, BM, VIS, NL_avg, EXP, OP-a, OP-s, CAL) is also the longest in the pool and the likeliest to be judged unverifiable.

Restate the main theorem as a **two-regime HPM theorem** whose proof uses the moves:
- HPM part: for budgets indexed by n, P(Ŝ ≠ S₀ or no output) ≤ P(U) + o(1), where in the favourable regime (T22(iii)) the truth is scored by the iid start draws (T11(iii)), and in the masked regime (T27 chain, π₀(S^{(0)}) ≥ c₀) a start draw lands in 𝓡_d and the terminal repair (Thm 4) scores S₀; T21 composes; T03 supplies π(S₀) > ½.
- Evidence and PIP part: T26(i)–(ii) as stated, favourable regime only, with EXP named as a hypothesis.

What this gains: the theorem then explains the method's *design*, not just its output, and the masked regime is exactly where the simulations show SMC-BVS beating the coordinate-wise competitors (S3–S6 at c = 0.5; S1 is a tie with SSL).

**Change B: Thm 4 (repair) should have a deterministic, finite-n route.** T24's repair constant c_n = 1/(s₀+d+B+2)! is 1/31! at s₀ = 14, and LK_d fails in correlated designs at states missing a true variable (a look-alike of the missing variable has leakage δ² ≈ (n−1)θ²r², so it is *more* attractive than most nulls). I propose T37 (§2) as the primary repair route: greedy best-improvement local search, which the method already runs three times, reaches S₀ from any 𝓡_d centre under a checkable "truth-dominance" condition, with a finite-n Gaussian bound on that condition. Keep T24 as the Gibbs-path alternative; whichever closes first is Thm 4, the other goes to the supplement. T37 is cheaper to prove and gives numbers at n = 200 for S1–S3.

**Change C: T27 (Thm 3) is a Proposition, merged with T22 as "the start: upper and lower bounds".** Together they say "the start finds the truth in the favourable regime and provably cannot in the masked one", which is the motivation for the sampler in two sentences. Separate theorem status overstates T27, which is a corollary of T10/T11/T22 given the ratio law.

**Keep unchanged:** T03 (Thm 1, with T01/T02 as lemmas), T07 (Prop 1), T21 (Thm 5), T12 (Prop 2; fold T31(i)'s Markov bound into it as one sentence so the reported 95% bound is covered).

**Two cheap additions, not main-text items.** (a) Do not drop T05: clause (iii) says the g-prior + BB(1,p) HPM loses a √log n factor to the oracle selector under orthogonal design. Referees from the Castillo–van der Vaart school know this; a supplement remark pre-empts it and explains the S1 parity with SSL at c = 0.5. (b) One sentence of T06(i) next to Prop 1: exact ties and near-duplicates are a ceiling for every method (S4).

**Biometrika cut (5):** Thm 1 (T03), Prop 1 (T07), Thm 4 (T37 or T24), Thm 5 (T21), Thm 6 (two-regime HPM, with evidence/PIP consistency as a remark). T22/T27 become one remark; T12 one remark. Same shape as HQ's cut, with Changes A and B applied.

---

## 2. Holes

**Weak-signal advantage over SuSiE and SSL.** No theorem in the pool, and I recommend *not* conjecturing a comparative one: it would need SuSiE's variational fixed points or SSL's coordinate-ascent path, which no campaign will close, and a toy comparison invites attack. The data say the advantage is a *correlated-design* advantage (S1 at c = 0.5: 79 vs 80), so the honest mechanism statement is: exact joint scoring separates a true variable from a look-alike by a margin of order (n−1)θ²(1−r²)/(2σ²), and the only unfixable error is the within-size swap (T07). T37 makes that margin explicit. Pair it with the same-target comparator the briefing already recommends (MCMC on the same posterior).

**Finite-n guarantee.** The real hole: every discovery route is asymptotic or conditional on abstract codes (LK, EXIT, GAIN, BASIN, HIT). T37 fills it.

**Computational complexity.** Not a hole. Budgets are polynomial by construction (N₀ = max(2500, n, p), T_e = O(log² n), p scores per round), so "polynomial expected cost to score the truth" is a one-line corollary of Thm 6; state it as such.

**Lower bound / optimality.** T05(iii) is the only optimality-type fact and it is negative; disclose it (§1). Minimax is out of scope.

**PIP calibration and misspecification.** T23 stays pathwise and conditional; Regime L is the answer, not a theorem. For non-Gaussian errors, note in Limitations that scores depend on y only through projections, so sub-Gaussian extensions are routine but not done.

### New conjecture T37: finite-n truth dominance and deterministic greedy repair

**Setting and assumptions.** EX-A; the production local search (scan every feasible flip and swap of the centre, move to the best strict improvement, at most ℓ moves, final certifying scan). Fixed design X, truth S₀, 𝓡_d = {U ∪ P : U ⊆ S₀, P ⊆ S₀ᶜ, |P| ≤ d}, s₀ + d ≤ K. Gains g(S, l) = F(S+l) − F(S), h(S, j) = F(S−j) − F(S), swap gains likewise. **TD(d, m)** (truth dominance with margin m ≥ 0): for every S ∈ 𝓡_d with S ⊉ S₀, some missing true variable j has g(S, j) ≥ m + every other feasible move's gain at S; for every S ∈ 𝓡_d with S ⊋ S₀, some extra l has h(S, l) ≥ m + every other move's gain; at S₀ every move has gain ≤ −m. For (ii) add G.

**Statement.** (i) [deterministic] Under TD(d, 0) with strict inequalities, from any centre S ∈ 𝓡_d the local search with ℓ ≥ |S Δ S₀| moves monotonically to S₀ in exactly |S Δ S₀| moves, scores S₀, and reports local_certified at S₀; hence S₀ ∈ 𝒮, and Ŝ = S₀ whenever π(S₀) > ½ (T21, T11(vii)). The path never leaves 𝓡_d. (ii) [finite n] Under G, for fixed X, P₀(TD(d, m) fails) ≤ Σ over the ≤ 2^{s₀} C(p, d)(p + s₀p) distinct move comparisons of P₀(a single score difference falls below m), each a one- or two-dimensional non-central Gaussian event with explicit non-centrality (n−1)δ²_{T,l}/σ*² and penalty ½ log(n+1) + log[(2p−k−1)/(k+1)]. (iii) [corollary, n-indexed] With s₀, d fixed and ℓ_n = ⌈log₂(n+p+1)⌉ ≥ s₀ + d eventually, under G, R, SE and BM-∞ the bound in (ii) → 0, so TD(d, 0) holds with probability → 1 and (i) is an unconditional repair route replacing GAIN_d, LK_d and EXIT_d.

**Why true.** Each gain is a monotone function of one residual projection u_{T,l}ᵀy (two for swaps). Adding a missing true j at T ⊆ S₀ ∪ P gains the full non-centrality (n−1)‖(P_{T+j} − P_T)μ‖²; its look-alike l captures only the r² fraction of the same signal; once S₀ ⊆ S every null has zero leakage and pays the penalty. So the greedy order is "truths in, then extras out", which is T24's prescribed path without the randomness.

**Proof route.** (i) by induction on |S Δ S₀| using TD. (ii) write each comparison as a quadratic-form difference in contrast coordinates (T01), bound the ν log-ratio of the IG marginal by a Gaussian exponent using the bounded-Q_S Taylor control from T02's hint, union bound. (iii) plug T03's beta-min margin.

**Main risk.** The 2^{s₀} union in (ii) makes the finite-n number loose at s₀ = 14 (≈ 10 nats); a dependence-aware bound along the actual greedy path is the research part. Also ℓ = 10 < s₀ + d = 15 at n = 200, so the finite-n clause needs the one-extra-scan rule or a centre within 10 moves; say so. Nothing here is false as stated.

**Where it fits.** Thm 4 (repair) in both journals; its (ii) is the paper's one finite-n statement and the mechanism behind the S3–S6 advantage; its failure event is the within-size swap of T07.

---

## 3. Restatement notes for each selected theorem

- **Thm 1, T03 (+T01, T02).** Replace the 2^{−m} geometric size tail in T02(i) by the exact BB(1,p) tail (ratio ≈ k/2p, not ½); m_n drops from ≈ 200 to s₀ + O(s₀ log n / log p), which makes SE on sets of size ≤ m_n + s₀ ≤ K meaningful at n = 200. Replace M_* by an unnamed C in θ² ≥ C σ² (log n + log p)/n, or use BM-∞. s₀ fixed, p ≤ n^A, K_n = ⌊n/2⌋. Failure point: uniform Gaussian-maximum control over C(p, k) subsets with the (n+1)^{−1/2} determinant penalty. Optional upgrade if T03 closes fast: s₀ → ∞ with s₀ log p = o(n), statistical half only.
- **Prop 1, T07.** None. Add the T06(i) tie sentence and name the look-alike swap as the within-size error.
- **Prop 2 (start), T22 + T27.** T22(iii): state EXP as a hypothesis and prove it in the BO benchmark (T22(v)) where VIS is derivable; B_n ≤ 16 makes 2^B a constant, so the union is over p blocks. T27: replace the assumed ratio law by a bounded-leakage condition |δ_{T,l}| ≤ Cσ* along the chain, from which n^{−1/2}e^{O_P(1)} follows via the (n+1)^{−1/2} determinant factor. Failure point: the composite normaliser in T27(i) (the hint's warning).
- **Thm 4, T37 / T24.** T37 as above. T24 if attempted: evaluate LK_d only at states containing S₀ (zero leakage) and charge look-alike additions at incomplete states to the budget d; replace the full-ordering event (1/(s₀+d+B+2)!) by a one-correct-Gibbs-step-per-round progress argument, giving (1−c′)^{H/(s₀+d)} with c′ ≈ 1/(B+3); H_n = L_n + 4 is already n-indexed. Failure point: EXIT_d bounding a non-Gibbs undo of a just-made correct step.
- **Thm 5, T21.** None mathematically. State (C1) with routes (a), (d), (e′ = T37) only; make U explicit and report P(U) empirically (6/2,400).
- **Thm 6, two-regime HPM + evidence/PIP.** Compose T22(iii)+T11(iii) [favourable] and T27+T37 [masked] through T21 and T03. Methodology tweak needed for the masked regime: an eligible centre must be the best scored model; guarantee it either by proving F(S^{(0)}) > sup_{S ∉ 𝓡_d} F(S) w.h.p. (T02/T03-type, asymptotic) or by a minor tweak, running the local search also from the start mode S̃₀ (deterministic, ≈ ℓ·p extra scores, no change to the sampler). Evidence/PIP clause: n-index Δ_n(T_n + 1) → 0 via T22(iv); failure point is EXP. Polynomial-cost corollary attached.
- **Prop 3, T12 (+T31(i)).** Restate for the run as designed to finish with a separate output-available event; drop the secondary-PIP clause. No risk.

---

## 4. Verdict

**ENDORSE WITH CHANGES.** Final JRSS-B list (8): Thm 1 T03 (T01, T02 lemmas); Prop 1 T07 (+T06(i) sentence); Prop 2 T22+T27 (start, two bounds); Thm 4 T37 (T24 alternative); Thm 5 T21; Thm 6 two-regime HPM with evidence/PIP clause (restated T26) plus polynomial-cost corollary; Prop 3 T12 (+T31(i)). Biometrika (5): Thm 1, Prop 1, Thm 4, Thm 5, Thm 6. Supplement additions: T05 as a disclosed remark. Campaign order: T37 first (cheap, finite-n, feeds Thm 4 and Thm 6), then the T02(i) tail sharpening, then EXP in the BO benchmark, then T24 only if T37 fails.
