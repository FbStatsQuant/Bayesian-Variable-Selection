# F-DRAFT: crosswalk from the "Local-to-Global Bayesian Computation" draft to SMC-BVS v3 theory

Run of 2026-11-02, branch `theory/F-DRAFT` (Fable 5.1). Reading and reasoning only; one exact p = 12 check in base R
(`scripts/wstab_check.R`, output `scripts/wstab_check.out`, 10 s through `owls_run -j 1`). Nothing here is reviewed or
adopted. Status words: PROVED / PROOF SKETCH / COUNTEREXAMPLE / CONJECTURE / OPEN, never upgraded; "locked" refers to
`Docs/Theory/proofs/LOCKED_PROOFS.md`; "candidate" refers to the unreviewed campaign branches `theory/W*`.
Precise statements and skeletons are in `NEW_TARGETS.md` (labels W0, W1, W2, W3, W4, W, W′, W″, NM, P, H).

Sources read: the draft (`Local_to_Global_draft.txt`), `METHODOLOGY_v3.md`, `THEORY.md`, `THEORY_PRIORITIES.md`,
`LOCKED_PROOFS.md`, `00_COMMON.md`, the one-pagers T05–T07, T09, T12–T14, T22, T25–T27, T38, the proved STATEMENT files of
T13, T22(i)(ii)(iv), T22(iii), T27(i), T06/T07, and the reports of W1-EXP, W3-VEXP, W2-T26, W2-PREM, W1-T24G, W4-T38FULL.

## 0. The one-sentence verdict

The draft's design is realised by v3 exactly: π₀ is the merged product of block-local tables, the bridge
γ_φ = γ₀ e^{φ d} is the draft's eq. (2) with L̃ = ∏_b m(S ∩ C_b)/m(∅)^{J−1}, and the correction is SMC with Gibbs, swap and
an independence (= the draft's MH) move. Every validity target of the draft (Prop 1, Prop 2, the frozen-run estimates) is
locked. The draft's one substantive theory target, §5.3 "weight stability under weak cross-block dependence", is
**not** covered and, as drafted, is **false for v3's tables**: under *exact* block orthogonality the composite start still
differs from the posterior by a Θ(n) term coming from the per-block integration of σ² against the full response
(the "dilution" that W3-VEXP found to mask the start at n = 200). The right statement (NEW_TARGETS Theorem W) is a
dilution theorem: in the favourable block-orthogonal regime the one-step importance weights have
log(1 + χ²(π‖π₀)) ≈ R²_pop · log p − ½ log n, with R²_pop the population R², so one-shot importance correction fails for
p ≫ n even when the start is right, while the adaptive ESS grid needs only a bounded number of stages. That theorem,
a rigorous "naive merge fails" proposition (NM) and a partition remark (P) are the three things worth adding.

## 1. Crosswalk table

Classes: (a) already covered; (b) partly covered; (c) compatible but absent, worth adding; (d) incompatible with v3 or
its story.

| Draft target | Class | v3 theorem(s) and status | What is missing / what to add | Value for JRSS-B / cost |
|---|---|---|---|---|
| **Prop 1** MH exactness (merge proposal inside MH with full posterior ratio) | (a) | **T09(ii)** PROVED-LOCKED (wave 1): every elementary move leaves q_φ invariant; the independence proposal S′ ~ π₀ accepted with 1 ∧ e^{φ[d(S′)−d(S)]} *is* the draft's MH with q = π₀ (at φ = 1 the ratio is π(S′)π₀(S)/(π(S)π₀(S′)) = e^{d(S′)−d(S)}). T09(v): whole-round minorisation. Support condition ⇔ γ₀ > 0 on Ω, derived in T13's proof. | Nothing. Add the one-line remark that the independence move is the draft's correction mechanism (NEW_TARGETS W0(iv): its exact convergence rate is 1 − 1/sup_S(π/π₀), Liu 1996). | Supplement lemma (already planned). Cost 0. |
| **Prop 2** SMC consistency for a local-to-global path | (a)/(b) | **T09** (kernel validity, locked); **T12** (unbiased Ẑ_r, islandwise product identity, locked; JRSS-B Prop 2); **T31(i)** (95% bound, locked); **T14(i)**, **T15** (first-moment and occupancy, locked); **W2-T26 Theorem A** (candidate PROVED: Ẑ/Z → 1 and PIPs → truth under the single premise (T_n+1)Δ_n → 0; JRSS-B Thm 6, favourable regime). Fixed-data N → ∞ weak convergence = **T16**, CONJECTURED and *dropped* from the paper (standard Del Moral et al. 2006 with multinomial resampling, which v3 uses). | The draft itself says the generic theorem is not the novelty; the project agrees (T16 dropped). One citation sentence in the supplement. The *new* input Thm 6 needs is a bound on the realised stage count T_n: see §5.3 row (Theorem W′ supplies it for the ideal grid in the favourable regime). | Covered. Cost 0 beyond W′. |
| **§5.3 Theorem 1** weight stability under weak cross-block dependence | **(b) + (d)** | Ingredients locked: **T13(i)** (1 + χ²(q_v‖q_u) = ρ_V(u,v)⁻¹·a(v)²/(a(u)a(w)); with V = Ω, u = 0, v = 1 this is exactly "one-step importance-weight variance = 1/ESS"); **T22(i)(ii)(iv)** (aggregation quantities q, u, e; exact odds; endpoint propagation); **EXP′** = W1-EXP Thm 1 / W2-PREM Lemma U (candidate PROVED, verified by W3-VEXP); **BO benchmark** (W1-EXP Thm 2, 6); **T27(i)** (masking law, locked conditional). No statement about χ²(π‖π₀), KL(π‖π₀) or the stage count exists anywhere. | The draft's mechanism is incomplete: the divergence is *not* controlled by cross-block covariance. Lemma W1 (PROVED, trivial): under exact BO, d(S) = ν[Σ_b log(1−ξ_b) − log(1−Σ_b ξ_b)] ≥ 0 (ξ_b the block's shrunken R²), zero iff one block carries all the R²; with a *known* σ² the same tables give d ≡ 0 and π₀ = π exactly. So the BO discrepancy is entirely the shared-σ² coupling ("dilution"), of size Θ(n) on signal-bearing models (254 nats at n = 800 in the check). What matters for weights is its *dispersion* over the bulk: Lemma W2 gives log[π(S₀+l)/π(S₀)] − log[π₀(S₀+l)/π₀(S₀)] = κ_b·G_l with κ_b = Δ_{T_b}/v_{T_b} the dilution fraction (00_COMMON's leakage quantities) and G_l the posterior gain; checked to two decimals. **Theorem W** (two-sided rate; lower bound PROVED, upper bound PROOF SKETCH): favourable BO regime ⇒ log(1+χ²(π‖π₀)) = [R²_pop log p − ½ log n]₊ + O_P(log log p). Cross-block correlation enters through a *second* term (Lemma W3, first order in the cross-block correlations among the selected variables, plus the leakage δ_{T,l} of T22(iii)). **W′** (CONJECTURE, skeleton): ideal ESS-0.9 grid has T = ⌈log₂(1 + R²_pop log p / log(√n/9))⌉ + O(1) stages, bounded under p ≤ n^A. **W″**: a masked-regime crossing costs ≈ 3π ≈ 10 stages whatever the odds gap (two-state computation PROVED; window form CONJECTURE). | **High**: it answers "why is the bridge needed and why is it short", and feeds Thm 6's open input (T_n). Cost: W0–W2 trivial; W(a) cheap; W(b) needs a second-moment aggregation lemma (T22(i) with squared odds) = half a day of a strong prover; W′ research-grade (extreme values + the halving recursion); W″ two-state part trivial. |
| **§5.4** approximation error when exact correction is unavailable (KL, TV, PIP error, joint-inclusion error, coverage) | (b) | v3 has no approximate variant: the bridge ends at φ = 1, so the error is Monte Carlo error at a finite budget. Covered: **T12/T31(i)** (unbiasedness, lower bound), **T14(i)/T15** (first moment, occupancy), **T23(ii)** (pathwise PIP bound, locked), **W2-T26 Thm A** (consistency, favourable), **T07(iii)(c)** (PIP error bounds the excess Hamming risk, locked). Not claimed anywhere: a rate in N, a fixed-budget KL/TV bound (T16, T25 dropped; PW2 OPEN). Joint-inclusion error: at the target level it is ≤ 1 − π(S₀) (T03); joint-inclusion estimates are not reported by v3 but are RB-estimable with the same T12 identity. Credible-interval coverage: (d), v3 reports no coefficients (T04 is a remark). | Add **Prop W4** (PROOF SKETCH): in the favourable regime KL(π‖π₀) and TV(π,π₀) are O_P(n^{−1/2}·polylog) while χ²(π‖π₀) can diverge like p^{R²}/√n; "small divergence" does not give "bounded weight variance" (the draft's "consequently" is the whole content). Add the one-line extension of T12 to general h(β_S, σ²) through the conjugate conditionals (**Remark H**). | Medium / cheap. Supplement remark. |
| **§3.2** naive union merge distorts uncertainty (the j/ℓ example) | **(c)** | Not stated. Pieces: **T22(ii-a)** (exact odds π₀(S₀)/π₀(S°), locked) gives the start side in one line; **T07(i)** (no size prior fixes a within-size swap) and the look-alike margin (T37 / W4-T38FULL Prop LH-LAT) give the posterior side; **T06(iii)** is the r = ±1 limit; **T27(i)** is a *different* failure (omission by cancellation, π₀(S₀) → 0 by undercounting), whereas §3.2 is commission (double counting). W1-T24G saw the mechanism in S3/S4/S6 at p = 20: start modes are supersets with 3–7 extras, "double counting of group-mates across split blocks". | **Prop NM** (PROVED modulo T03; all quantities closed-form, so a finite-n version is available): proxy pair split across blocks ⇒ local PIPs of j and ℓ → 1, the union and v3's π₀ put mass → 1 on {j, ℓ}, the posterior puts mass → 1 on {j}; PIP error, joint-inclusion error and TV → 1; 1 + χ²(π‖π₀) ≥ e^{Θ(n)}, so one-shot IS and independence-MH fail at every polynomial budget; but S₀ is one Gibbs flip from the start mode, scored with probability ≥ a₁ per terminal round (W1-T24G Cor. P1), and the ideal grid crosses in O(1) stages (14–16 at p = 12 in the check). Not implied by T06/T07/T27 as statements; corollary of T22(ii-a) + T03. | **High** for the motivation section (it *is* the paper's thesis "easy merge, hard uncertainty" in one proposition) and it links the motivation to the story: the truth is at Hamming distance 1 and gets scored. Cost: half a page. |
| **§13.1** convergence of estimates of E[h(θ)] | (a)/(b) | For h = functionals of S (PIPs, Z, MPM): T12, T23(ii), W2-T26 Thm A. For general h(β_S, σ²): v3 reports none; the conjugate conditional β_S, σ² | S, y is closed-form, so Σ_S π(S) E[h | S] is RB-estimable and T12's product identity extends verbatim (**Remark H**). | Remark only; no new reporting. | Low / trivial. |
| **§13.2** Song & Liang's UQ may be problematic | (c) | METHODOLOGY §11 records the template (S&L prove target results and cite SAMC for the sampler). Prop NM is the precise statement of the UQ defect of a split-and-merge *selection* rule: it overcovers under split proxies. | One paragraph in the literature/motivation section citing Prop NM. | Low / trivial. |
| **§13.3** partition as a random variable, "stochastic scheduling" | (c) | v3's partition is deterministic in X (complete linkage, cut, next-fit). Every finite-sample identity (T09, T12, T13, T21, T22(i)(ii)(iv), T31) is stated for an arbitrary partition and arbitrary positive tables, hence holds conditionally on any partition fixed before the final randomness (CAL). The schedule is adaptive in calibration and frozen for the final run; T12(iv) says a state-dependent schedule *inside* the final run breaks unbiasedness. | **Prop P** (PROVED, elementary): (i) validity is partition-free and the target does not depend on the partition, so the partition is a *design* variable of the start (it governs π₀(S₀), the dilution fractions and the leakage), not a parameter to infer; (ii) a finite mixture of block starts over m partitions is exactly samplable with computable density, the bridge from it is valid, π₀^{mix}(S₀) ≥ max_i λ_i π₀^{(i)}(S₀) and sup π/π₀^{mix} ≤ min_i sup(π/π₀^{(i)})/λ_i: one favourable partition in the mixture undoes masking at the price log(1/λ_i) nats of discovery budget (W3-VEXP: packing both hubs into one block kills LH masking); (iii) "stochastic scheduling" = calibration + frozen final run, justified by T12. (ii) is a method extension (not in the 2,400 fits): investment rule. | Supplement remark; (ii) as future work or as a T39-type contingency. Cost: trivial. |
| **§4.4** when is correction stable: degeneracy, ESS, sensitivity to blocks | (b) | **T13** (restricted ESS identity and the 10/9 bound on an accepted grid under COVER); **T31(i)** (what the evidence bound certifies); T31(ii)–(vii), T12(iv) (what the checks do *not* certify; conjectured / locked "limits"). Sensitivity to blocks: only through T22(iii)'s hypotheses. | Theorem W and Prop P(i) make the block sensitivity explicit: κ_b (dilution) and δ_{T,l} (leakage) are the two block-dependent quantities; Remark W5 notes they act in *opposite* directions (dilution damps null tables, which helps start concentration — W1-EXP Thm 6 needs SPREAD — but inflates π/π₀ on nulls; leakage does the reverse). | Medium / cheap once W exists. |
| **§8.2** novelty devices: adaptive local-to-global tempering; proposal learned from local samples; ESS diagnostics; stable-weight theory | (a)/(b) | Adaptive tempering = pilot + candidate grid (T13 locked; V11/T25 dropped); proposal learned from local tables = the independence move (T09); diagnostics = T31; stable-weight theory = absent (Theorem W). | Theorem W + W′ are the "theory for stable correction weights" the draft asks for. | See §5.3 row. |
| **§3.3 step 1** possibly *overlapping* blocks | (d) | v3's exact convolution sampler and Z̄₀ need a partition (product form over disjoint blocks). | None. Overlap would destroy the exact start; the mixture of partitions (Prop P(ii)) is the compatible substitute. | — |
| **§4.3 item 4** delayed acceptance with cheap local scores | (d) | Not in v3; the score cache and the tables play the cheap-score role differently. | None. | — |
| **§6** comparators: naive split-and-merge; product of local posteriors; one-shot IS | (c), empirical | Comparators 2–3 are the HPM/MPM of π₀ itself; one-shot IS is the T = 1 bridge with ESS ρ_Ω(0,1). | Cheap empirical lines for the paper: report π₀'s HPM and PIPs, and the restricted one-step ESS ρ_V(0,1) (computable exactly from the stored V) or the pilot's first temperature φ₁ as its proxy, per fit. | High persuasion / near-zero cost. |

## 2. The §5.3 target in detail

### 2.1 What the draft's Theorem 1 becomes in v3 terms

- "Product of block posteriors" = π₀ (composite start; tables r_b(U) = BF(U) scored against the full y; global size
  prior ϖ). "Full posterior" = π. "Divergence" = any of KL(π‖π₀), TV, χ²(π‖π₀). "Variance of importance weights" =
  Var_{π₀}(w̄) = χ²(π‖π₀) for the normalised weight w̄ = e^{d}/E_{π₀}e^{d}, and 1/(1+χ²) = ρ_Ω(0,1), the full-space
  restricted ESS of **T13(i)** with V = Ω, u = 0, v = 1 (so w = 2: the law q₂ ∝ π²/π₀ is the one that must be covered).
- The three "correction mechanisms" of the draft's §2 are three norms of the same ratio π/π₀ = e^{d}/E_{π₀}e^{d}
  (NEW_TARGETS **Prop W0**): L² (importance sampling, χ²), L^∞ (independence sampler rate 1 − 1/sup(π/π₀), Liu 1996)
  and the value at S₀ (iid discovery, T11(iii)). All three blow up together in the masked regime
  (1 + χ² ≥ π(S₀)²/π₀(S₀) = p^c n^{c/2} e^{O_P(1)} by T27(i); e^{Θ(n)} in the proxy-split case of Prop NM).

### 2.2 Why "controlled by cross-block covariance" is the wrong mechanism for v3

Exact structure (NEW_TARGETS **Lemma W1**, PROVED by block-diagonality): under BO (X_{C_b}ᵀX_{C_b′} = 0),
D_S = ∏_b D_{S_b} and t_S = Σ_b t_{S_b}, hence with c = 2b₀ + yᵀy and ξ_b = t_{S∩C_b}/c,

    d(S) = ν [ Σ_b log(1 − ξ_b) − log(1 − Σ_b ξ_b) ]  ≥ 0,   ν = a₀ + n/2,

with equality iff at most one block has ξ_b > 0. The determinant part is exactly additive; **the whole BO discrepancy
is the σ² coupling**: with a known σ² the same tables give d ≡ 0 and π₀ = π *exactly*. (Check: min d = 0 in all six BO
runs; d(S₀) = 57 nats at n = 200 and 254 nats at n = 800 with one truth per block; d(S₀) = 0 with both truths in one
block.) So the draft's premise "zero cross-block covariance ⇒ product ≈ posterior" holds for a known-σ² table and fails
for v3's integrated-σ² table by a Θ(n) term. This is the same object as W3-VEXP's dilution (Prop D): each block's table
sees the other blocks' signal as noise, v_T = σ² + Δ_T instead of σ².

What matters for the weights is not d(S₀) but the dispersion of d over the bulk of π and π₀. **Lemma W2** (PROVED up to
O(1/n) ridge terms; checked to two decimals): for a null l in block b and T_b = S₀ ∩ C_b,

    log[π(S₀+l)/π(S₀)] − log[π₀(S₀+l)/π₀(S₀)] = d(S₀+l) − d(S₀) = κ_b · G_l (1 + o(1)),
    κ_b = Δ_{T_b}/(σ² + Δ_{T_b}) ∈ [0,1),   G_l = −ν log(1 − x_{S₀,l}) = Z_l²/2 (1 + o_P(1)),

i.e. the posterior rewards a chance correlation Z_l² with the full exponent Z_l²/2 while the diluted table rewards it with
(1−κ_b)Z_l²/2. Over the p − s₀ nulls, all but at most s₀B of which sit in signal-free blocks where κ_b = R²_pop exactly,
the heavy-tailed sum Σ_l π(S₀+l)·e^{κ_b G_l} ≍ p^{−1} n^{−1/2} Σ_l e^{(1+R²)Z_l²/2} ≍ p^{R²} n^{−1/2} (tail index
1/(1+R²) < 1, the sum is governed by its maximum, max_l Z_l² ≈ 2 log p). Hence **Theorem W**:
log(1 + χ²(π‖π₀)) = [R²_pop log p − ½ log n]₊ + O_P(log log p) in the favourable BO regime. At the study design
(R² ≈ 0.9, p = 500, n = 200) the bracket is 5.5 − 2.6 > 0: one-shot importance correction would have ESS of order
e^{−3}, *even if the start were favourable*; the actual start is dilution-masked (π₀(S₀) ≈ 10⁻¹²), which adds 28 nats.

Cross-block covariance enters as a second, additive term (**Lemma W3**, PROOF SKETCH): with R_S = D_S + E_S (block
diagonal plus cross-block part among the *selected* variables), d(S) = d_BO(S) + (n/2)·Σ_{b≠b′} β̂_bᵀE_{bb′}β̂_{b′}/(1−R²_S)
+ O(n‖E_S‖²), plus the leakage term of the tables (δ_{T,l} ≠ 0 for nulls correlated with other blocks' signal, the
T22(iii) family). So the draft's theorem survives as: "the cross-block part of d is first order in the cross-block
covariance", and the dilution part is what it missed.

### 2.3 Connection to T13, T22, EXP′, the BO benchmark and the regime split

- **T13**: the identity 1 + χ²(q_v‖q_u) = ρ_V(u,v)⁻¹ a(v)²/(a(u)a(2v−u)) is the whole algebraic content; Theorem W
  evaluates ρ_Ω(0,1) statistically. The governing point w = 2v − u reappears in W′: χ²(q_v‖q_u) ≍ p^{R²(2v−u−1)}/√n, so
  the ESS-0.9 grid satisfies 1 − v_t = (1 − v_{t−1} − g)/2 with g = log(√n/9)/(R² log p), which halves the remaining gap
  each stage and reaches 1 after ⌈log₂(1 + 1/g)⌉ stages (4 at the study sizes if the start were favourable).
- **T22**: the proof of W(b) is a second-moment analogue of T22(i): replace a_{bj} = Σ r_b(U)/r_b(U*) by
  a⁽²⁾_{bj} = Σ [posterior odds]²/[table odds] and run the same D_b, q, e aggregation (NEW_TARGETS §W(b) skeleton);
  T22(ii-a) gives the exact S₀-term π(S₀)²/π₀(S₀); T22(iv-b) and W2-T26 Lemma 1 give Δ_n = max{1−π₀(S₀), 1−π(S₀)}.
- **EXP′ / Lemma U**: the expansion log[r_b(T+l)/r_b(T)] = −½log(n+1) − ν log(1 − x_{T,l}) + R with |R| = O(1) is exactly
  what Lemma W2 needs on the table side, and the same expansion at T = S₀ on the posterior side; under BO the two partial
  R²'s share the numerator and differ only in the denominator RSS_T versus RSS_{S₀}, which is the dilution ratio
  1/(1−κ_b). W3-VEXP's finite-n certificate R1 bounds the remainder at the study sizes.
- **BO benchmark**: Theorem W is a BO theorem first (everything explicit), then perturbed by Lemma W3. W1-EXP Thm 2
  supplies 1 − π₀(S₀) → 0 under BO, SE-blk, BM-blk; under BO, SE follows from SE-blk (block-diagonal R_T), so T03 applies
  with the same hypotheses: the favourable BO regime is one joint family (Astra's compatibility requirement is met).
- **Favourable vs masked**: favourable ⇒ Theorem W (χ² ≍ p^{R²}/√n, polynomial, bridge of bounded length W′);
  masked ⇒ 1 + χ² ≥ π(S₀)²/π₀(S₀) → ∞ (T27(i): polynomially; Prop NM: exponentially) and the bridge must cross; a
  two-state crossing has path length ∫ sd_{q_φ}(d) dφ = π exactly, so it costs ≈ 3π stages at ESS 0.9 regardless of the
  odds gap (W″; the legacy T4 "schedule is cheap" in v3 form), *provided* the crossing is in V (T13(iii)) and particles
  occupy S₀ (delivery, T38(b)): weight stability is necessary, not sufficient, and v3's theory already separates the two
  (T13 for weights; T15/T23/W1-T24G Theorem B/W4-T38FULL for occupancy).
- **Opposite directions (Remark W5)**: dilution lowers every null table's exponent from Z²/2 to (1−κ)Z²/2, which makes
  E e^{(1−κ)Z²/2} finite and is what W1-EXP Thm 6 (SPREAD) uses to concentrate the start; the same lowering inflates
  π/π₀ on nulls and is what drives Theorem W. Leakage (δ_{T,l} ≠ 0) does the reverse: it inflates null tables (hurts
  T22(iii) through NL_avg) and lowers π²/π₀ on those nulls (helps χ²). The block partition therefore faces a genuine
  trade-off, which is the precise form of the draft's §4.4 "sensitivity to block construction".

### 2.4 Guidance for O-WSTAB (statement first, then the cruxes)

Prove, in this order: W0 (definitions + T13(i) + Liu 1996), W1 (block-diagonal algebra), W2 (two EXP′ expansions and
the RSS ratio), W(a) (one term, extreme value over the nulls of signal-free blocks), W(b) (second-moment aggregation
over layers, then the heavy-tailed sum), then W′. Cruxes: (1) never take expectations of e^{(1+κ)Z²/2}: they are infinite;
work with high-probability extreme-value bounds and truncation (as W3-VEXP did); (2) do not try to prove "χ² bounded":
it is false when p^{R²} ≫ √n; prove the two-sided rate; (3) the nulls' Z_l are exactly independent across blocks under BO
and at most B-dependent within a block, so the max over p of them behaves as over p/B independent blocks of size ≤ B;
(4) for W′ the only new ingredient is that q_φ(S₀+l)/q_φ(S₀) ∝ e^{(1 − κ(1−φ))Z²/2}, which gives the p^{κ(2v−u−1)}/√n law
for χ²(q_v‖q_u) and the halving recursion; the gap between the ideal full-space grid and the method's V-restricted
pilot grid is a separate (COVER-type) obligation and should be stated, not closed.

## 3. The naive-merge proposition (§3.2 made rigorous)

NEW_TARGETS **Prop NM**. Setting: G; S₀ = {j}, θ_j ≠ 0; a proxy ℓ with r = r_{jℓ}, 0 < |r| < 1, otherwise orthogonal; j
and ℓ in different blocks. Then w.p. → 1: (i) the block-local posteriors give PIP^{loc}_j → 1 and PIP^{loc}_ℓ → 1
(log r_{b(ℓ)}({ℓ}) = (n/2) log[1/(1 − r²θ²/(σ²+θ²))] − ½ log n + O_P(1) → +∞), so the union is {j, ℓ}; (ii) v3's start
inherits it: π₀({j,ℓ})/π₀({j}) = [w(2)/w(1)]·r_{b(ℓ)}({ℓ}) → ∞ by T22(ii-a), so π₀(j, ℓ ∈ S) → 1; (iii) the posterior does
not: π({j,ℓ})/π({j}) = [w(2)/w(1)] n^{−1/2} e^{Z²/2 + O_P(1)} → 0 (the residual of x_ℓ on x_j is orthogonal to μ), and
π({ℓ})/π({j}) = exp{−(n/2) log(1 + θ²(1−r²)/σ²)(1+o_P(1))} → 0 (the look-alike margin), so π({j}) → 1 (also T03);
(iv) PIP error on ℓ, joint-inclusion error on (j, ℓ) and TV(π, π₀) all → 1, and 1 + χ²(π‖π₀) ≥ π({j})²/π₀({j}) = e^{Θ(n)}:
one-shot IS, independence-MH and iid discovery from π₀ fail at every polynomial budget (Prop W0); (v) the correction is
nevertheless cheap: S₀ is one Gibbs flip from the start mode, scored in a terminal round with probability ≥ a₁
(W1-T24G Cor. P1), and the ideal grid crosses from {j,ℓ} to {j} in O(1) stages (14–16 in the exact p = 12 check, where
π₀({1}) = 10⁻⁴¹ at n = 200 and 10⁻¹⁴⁶ at n = 800 while π({1}) = 0.86 and 0.95).

Is it implied by T06/T07/T27? **No.** T06(iii) is the r = ±1 limit (exact unidentifiability); T07(i) is the posterior
side of the within-size swap {j} vs {ℓ} and says no size prior repairs it, which is complementary; T27(i) is omission by
cancellation (undercounting), the opposite failure of the start from commission by double counting. (ii) is a one-line
corollary of T22(ii-a); (iii) is a one-line corollary of T03 or of the explicit formulas. In v3's X-dependent partition a
pair with |r| near 1 is split only when its complete-linkage cluster exceeds B, so the proposition should be stated
for an arbitrary partition that separates j and ℓ, with the remark that v3's clustering makes the split need a cluster
larger than B (the empirical instance: S3/S4/S6 groups of 5 cut at B = 4 in W1-T24G; groups of 5 packed two per block
at B = 14 are *not* split, which is why the study's masking is dilution, not double counting: W3-VEXP).

## 4. The partition as a random variable (§13.3)

Compatible, and cheap (NEW_TARGETS **Prop P**). (i) Every finite-sample result of the register is stated for an
arbitrary partition into blocks of size ≤ K and arbitrary positive tables (T22(i) says so explicitly; T09, T12, T13, T21,
T31 use only the product form and γ₀ > 0), so they hold conditionally on any partition fixed before the final randomness,
even a y-dependent one; the target π does not depend on the partition. "Inferring the partition" is therefore not a
Bayesian inference about the model but an adaptation of the start, exactly like the schedule, and its objects are
π₀^𝒫(S₀) (delivery), κ_b(𝒫) and δ_{T,l}(𝒫) (weight stability), and the start normaliser. (ii) The draft's "multiple random
partitions" (§8.4) becomes a *mixture start* π₀^{mix} = Σ_i λ_i π₀^{(i)}: exactly samplable, density computable with m
table lookups, bridge valid, with π₀^{mix}(S₀) ≥ max_i λ_i π₀^{(i)}(S₀) and sup π/π₀^{mix} ≤ min_i λ_i⁻¹ sup π/π₀^{(i)}.
One favourable partition in the mixture undoes masking at a cost of log(1/λ_i) nats in the discovery budget of T11(iii).
It is a method extension and falls under the investment rule; it is the natural companion of T39 and of W3-VEXP's
observation that packing both hubs of a linked pair into one block kills the LH masking. (iii) "Stochastic scheduling"
is already v3's calibration; its validity theorem is T12 (with T12(iv) as the warning that the schedule must be frozen
before the final run).

## 5. Recommendation: what joins the paper, and where

Consistent with THEORY_PRIORITIES' story ("the truth gets scored"), I recommend:

1. **Main text, motivation (new Proposition 0 = Prop NM).** Two lines of statement, proof in the supplement. It is the
   paper's thesis as a theorem, it is finite-n explicit, and it ends with "the truth is one flip from the merge and gets
   scored", which hands over to Thm 2 (T22+T27) and Thm 3–5. It also disposes of §13.2 (Song–Liang) in one sentence.
2. **Main text, one remark after Thm 2 (favourable regime), supplement Theorem W.** Sentence: "Even when the start is
   favourable, one-step importance correction has weight variance of order p^{R²}/√n (Theorem W), so a tempering bridge
   is needed for p ≫ n; the adaptive ESS grid needs only ⌈log₂(1 + R² log p/log(√n/9))⌉ + O(1) stages (W′)". Put the
   lower bound W(a) and Lemma W1 in the supplement now (cheap, rigorous); upgrade to the two-sided W(b) and W′ if O-WSTAB
   closes them. W′, if proved, is the missing input (T_n bounded) of Thm 6 = W2-T26 Theorem A in the favourable BO
   regime, which would make Thm 6 non-vacuous on a p ≤ n^A family.
3. **Supplement lemma T13: add Prop W0 as clause (v)** ("three faces": χ², sup-ratio, π₀(S₀)). It is the conceptual
   bridge from the draft's IS/MH/SMC trichotomy to v3 and costs nothing.
4. **Supplement remarks:** Prop W4 (KL, TV small; χ² not), Remark W5 (dilution vs leakage trade-off: the block
   sensitivity of §4.4), Prop P (partition), Remark H (general h). Keep W″ as a remark under the candidate-grid
   description (the ≈ 3π stages per crossing explains the grid's design; V11 remains dropped).
5. **Do not add:** delayed acceptance, overlapping blocks, credible-interval coverage, the generic Del Moral theorem
   (cite it), the empirical comparators of §6 as theorems (report them as two cheap lines: π₀'s own HPM/PIPs and the
   one-step restricted ESS ρ_V(0,1) per fit).

## 6. Outside scope: a method note for HQ (not pursued; investment rule)

Lemma W1 says the entire BO discrepancy between the composite start and the posterior is the per-block integration of σ²
against the full-y residual; with a common noise scale (known σ², or a single plug-in σ̂² from a preliminary fit used
in *all* tables) the tables would give d ≡ 0 under BO and π₀ = π exactly, and in general d would be first order in the
cross-block covariance, i.e. the draft's Theorem 1 would hold literally. Such tables are "arbitrary positive tables"
in the sense of T22(i), so T09, T12, T13, T21, T22(i)(ii)(iv), T31 hold verbatim; only the EXP′-dependent statistical
results (T22(iii), W1-EXP) would need redoing. W3-VEXP identified dilution (v ≈ 25σ²) as the reason the start misses
6–12 of the 14 truths at n = 200 at *every* signal scale. A plug-in-σ² table is therefore the one cheap method change
that attacks the n = 200 masking at its cause. It changes the start only, it is not in the 2,400 fits, and whether it
performs is a pilot question (investment rule). I flag it; I do not recommend acting on it inside this campaign.

## 7. Confidence card

| Item | Statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Classification table (§1) | as stated | 0.9 | — | reading fidelity to 39 files | no |
| Lemma W1 (BO structure of d; known σ² ⇒ π₀ = π) | NEW_TARGETS | 0.99 | done (algebra; checked) | none | no |
| Lemma W2 (dilution form of the null log-odds gap) | NEW_TARGETS | 0.95 | 0.95 | O(1/n) ridge terms | no |
| Theorem W(a) lower bound | p^{R²−ε}/√n ≤ 1+χ² w.p. → 1 | 0.95 | 0.9 | extreme value over ≤ B-dependent Gaussians | no |
| Theorem W(b) upper bound | 1+χ² ≤ p^{R²+ε}/√n + o(1) | 0.85 | 0.6 | second-moment aggregation over layers | no |
| W′ ideal grid stage count | ⌈log₂(1 + R² log p/log(√n/9))⌉ + O(1) | 0.75 | 0.4 | χ²(q_v‖q_u) law; ideal vs V-restricted grid | no |
| W″ crossing cost ≈ 3π stages | two-state exact; window form | 0.99 / 0.7 | done / 0.5 | non-two-state mass in the window | no |
| Prop NM | §3 | 0.97 | 0.95 (half a page) | none (T22(ii-a) + T03) | no |
| Prop P | §4 | 0.97 | done | none | (ii) yes, extension |
| Method note §6 helps at n = 200 | plug-in-σ² tables unmask the start | 0.6 | pilot question | performance under false inclusions | yes |
