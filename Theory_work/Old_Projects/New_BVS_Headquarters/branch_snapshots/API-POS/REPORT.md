# API-POS — REPORT (referee task R3, MIX-POS: positioning against the rapid-mixing literature)

Run of 2026-11-02, branch `theory/API-POS`. The task file names the deliverable `theory_campaign/MIX-POS/REPORT.md`. The run
instructions restrict writing to `theory_campaign/API-POS/`, so the deliverable is this file.
Status words are the campaign's (PROVED / PROOF SKETCH / COUNTEREXAMPLE / CONJECTURE / OPEN). Everything here is a
**candidate**: it has not been reviewed.
Scripts are in `scripts/` (seed 20261102), raw output is in `results/cond1_lh.md`, and the source log is in `NOTES.md`.

## 1. Headline

1. **On LH, the masking is a property of the method's start law π₀, not of the posterior π.** The target posterior has
   the property every rapid-mixing proof rests on: every underfitted model has a missing true variable whose addition
   raises π by a large factor (ZYVR Condition 1(b)). Exact enumeration of the paper's own target at p = 16 and p = 20
   shows S₀ as the **unique local mode** under add/delete/swap moves on the whole capped space. It also shows the YWJ
   random-walk MH chain hitting S₀ from the empty model in a median of about 70–140 iterations, flat in n
   (n = 200 to 102,400). For p = o(n), PROOF SKETCH; the p ≤ 20 enumeration is evidence only.
2. **With their own priors, both theorems apply to LH** in the iid realisation (p ≥ n, p ≤ n^A, fixed beta), so
   polynomial-time recovery of S₀ on LH is **not new**. This is a PROOF SKETCH, since the hypotheses are checked by
   standard arguments, not line by line.
   - Yang–Wainwright–Jordan (YWJ) Thm 2 / Cor 2: an add/delete/swap MH chain reaches S₀ and mixes in
     O(α p n s₀² log p) iterations from **any** start in M(s₀).
   - Zhou–Yang–Vats–Roberts–Rosenthal (ZYVR) Thm 1: an informed MH chain mixes in O(n) iterations, each scoring O(p) neighbours.

   The referee's suspicion (M6) is correct in substance.
3. **For the paper's own target, neither theorem applies as stated.** Each condition below fails for an identified reason:
   - **Prior strength.** The prior penalty is too weak: g = n, κ_eff ≈ 1 against ZYVR's explicit κ ≥ 18. When p ≍ n,
     Condition 1(a) holds only with c₀ ≈ ½, not the required c₀ = 2 (PROOF SKETCH).
   - **Size cap.** The cap K = ⌊n/2⌋ breaks YWJ's D(s₀) (s₀ ≲ n/log p).
   - **Regime.** Exact-Gram LH (p ≤ n − 1, possibly fixed p) lies outside both papers' stated regime.

   So no published theorem covers the SMC-BVS output on LH. This is a formal gap, not a substantive one.
4. **Zanella–Roberts (2019) §4.5 and Griffin–Łatuszyński–Steel (2021) say nothing quantitative about LH.** ZR §4.5
   treats only diagonal and fully collinear X; GLS proves ergodicity and an SLLN with no rate.
5. **Citations.** All four citations check out against Crossref and the full text, with one correction. ZYVR has
   **five** authors (Zhou, Yang, Vats, Roberts, **Rosenthal**), JRSS-B 84(5):1751–1784. Their sampler is "locally
   informed and thresholded" (LIT-MH). It is not one of Zanella's locally balanced samplers, which ZYVR use only as
   comparators.

## 2. Sources read, and citation check

| Referee's citation | Verified reference | What I read |
|---|---|---|
| Yang, Wainwright & Jordan (2016), AoS 44(6) | Y. Yang, M. J. Wainwright, M. I. Jordan, "On the computational complexity of high-dimensional Bayesian variable selection", *Ann. Statist.* 44(6):2497–2532 (2016), doi:10.1214/15-AOS1417 ✔ | arXiv:1505.07925**v1**: §2.2 (chain (3)), §3.1 (model (5a–d), Assumptions A–D), Thm 1, Cor 1, Thm 2, Cor 2, §3.4.2, §4.1. The published PDF is paywalled. **Theorem numbers are from arXiv v1 and are not checked against the journal version.** |
| Zhou, Yang, Vats & Roberts (2022), JRSS-B 84(5) | Q. Zhou, J. Yang, D. Vats, G. O. Roberts, **J. S. Rosenthal**, "Dimension-free mixing for high-dimensional Bayesian variable selection", *JRSS-B* 84(5):1751–1784 (2022), doi:10.1111/rssb.12546. **Author list corrected.** | arXiv:2105.05719v3 (the library copy `Papers/SMC/10_2022_Zhou_et_al_…pdf`): §2.1–2.3, Condition 1, Def. 1, Props 1–2, Thm 1, Remark 2, §7.1, Supplement S3 (Thm S2 and its proof sketch) |
| Zanella & Roberts (2019) | G. Zanella, G. Roberts, "Scalable importance tempering and Bayesian variable selection", *JRSS-B* 81(3):489–517 (2019), doi:10.1111/rssb.12316 ✔ | arXiv:1805.00541v2 (library copy): §4.1, §4.5 (4.5.1–4.5.3, Thms 2–3, Assumption 1) |
| Griffin, Łatuszyński & Steel (2021), Biometrika | J. E. Griffin, K. Łatuszyński, M. F. J. Steel, "In search of lost mixing time: adaptive Markov chain Monte Carlo schemes for Bayesian variable selection with very large p", *Biometrika* 108(1):53–69 (2021), doi:10.1093/biomet/asaa055 ✔ | arXiv:1708.05678v3: §2.1–2.2 (Props 1–2), §3 (Lemmas 1–2, Thm 1) |

Metadata was checked with the Crossref API (YWJ, GLS) and publisher and repository records (ZYVR, ZR).

The referee's descriptions of the results are accurate. Two details are loose:
- YWJ's chain is "single flip / double flip (swap)", i.e. add/delete/swap. ✔
- YWJ's beta-min condition is min|β_j|² ≥ c₀(L + L̃ + α + κ)σ₀² log p/n with an **unspecified universal** c₀, not a "large" explicit one.

## 3. Setting compared

**LH** (`W1-EXP · PROOF.md §4`): G groups of size g, with within-group equicorrelation ρ_h. Groups are independent except
for c linked hub pairs with corr(j_a, j_b) = ψ, and the truth is θ_{j_a} = β, θ_{j_b} = −ψβ (the suppressor), plus visible
hubs. Two realisations:
- **exact-Gram**: X'X = (n − 1)Σ, p ≤ n − 1;
- **iid**: rows iid N(0, Σ_LH), p ≤ n^A, p > n allowed.

The fixed facts used below are λ_min(Σ) ≥ (1 − ψ₊)(1 − ρ₊) =: φ₀² (W1-EXP Lemma 4.1(a)), fixed nonzero β, and fixed s₀.

**Paper's target** (`00_COMMON.md`): β_S ~ N(0, nσ²(G_S + I)⁻¹), σ² ~ IG(0.01, 0.01), and BB(1, p),
w(k) = ½/C(2p − 1, k), capped at K = min(p, ⌊n/2⌋). Neighbouring prior ratio: w(k+1)/w(k) = (k+1)/(2p−1−k).

**YWJ / ZYVR target**: Zellner g-prior with g ≍ p^{2α} (ZYVR: 1 + g = p^{2κ₁}), π(φ) ∝ 1/φ, and π(γ) ∝ p^{−κ₀|γ|} 1{|γ| ≤ s₀}.
Here s₀ is **their tuning cap** and must satisfy s₀ ≲ n/log p.

## 4. Hypothesis-by-hypothesis tables

Notation: "LH-G" is exact-Gram LH and "LH-iid" is iid LH. "YWJ-prior" means the YWJ posterior with hyperparameters chosen
as the theorem asks. "Paper-prior" means the paper's target above.

### 4.1 YWJ (2016), Theorem 2 (rapid mixing) and Corollary 2 (iterate = γ*)

| # | Their condition | Holds on LH? | Proof / counterexample |
|---|---|---|---|
| Y0 | Model (5a–d) | **No** for the paper-prior; yes by construction for the YWJ-prior | The g-prior differs (ridge-modified, g = n), as do the σ² prior (proper IG, not 1/φ) and the size prior (BB(1,p), not p^{−κ\|γ\|}). A truncated size prior with cap s₀ ≪ n is not optional in YWJ: they state it "is necessary for rapid mixing" (§3.1). |
| Y1 | Regime: "throughout … p ≥ n" (§3.1). The probability bound 1 − 4p^{−c₁} needs p → ∞ | LH-G **no** (p ≤ n − 1; BG3 even has p fixed). LH-iid **yes** when p ≥ n | YWJ say the low-dimensional case "is easier" but state no theorem for it. The extension to LH-G with p_n → ∞ is a CONJECTURE (very likely true). |
| Y2 | A, full-β: ‖Xβ*‖² ≤ g σ₀² log p (7a) | YWJ-prior **yes** (g ≍ p^{2α} ≥ n). Paper-prior (g = n) **yes iff** log p ≥ θ'Σθ/σ², so it fails for fixed p | ‖Xβ*‖² = (n − 1)θ'Σθ on LH-G (θ'Σθ(1 + o_P(1)) n on LH-iid). This is YWJ's "information paradox" condition. |
| Y3 | A, off-support: ‖X_{S^c}β*_{S^c}‖² ≤ L̃σ₀² log p | **Yes**, with L̃ = 0 | LH is exactly sparse. Every nonzero coefficient, the suppressor −ψβ included, is fixed, so S(C_β) = S₀ for C_β ≤ min_j\|θ_j\|. |
| Y4 | B, normalisation ‖X_j‖² = n | **Yes**, up to the rescaling n − 1 → n (absorbed into g) | Standardised design. |
| Y5 | B, RE(s₀): min_{\|γ\|≤s₀} λ_min(X_γ'X_γ/n) ≥ ν | LH-G **yes, for every s ≤ p**, with ν = φ₀²(n−1)/n (PROVED: Lemma 4.1(a) and Cauchy interlacing). LH-iid **yes** w.p. → 1 for fixed s₀, or s₀ log p = o(n) (PROOF SKETCH, below) | Sketch: ‖R̂_γ − Σ_γ‖_op ≤ φ₀²/2 for one γ holds except with probability 2·9^{s₀}e^{−c n φ₀⁴}. A union bound over ≤ p^{s₀} sets is o(1) when s₀ log p = o(n). |
| Y6 | B, SI(s₀) (sparse projection) | **Yes**, with L = 4ν⁻¹s₀ | YWJ's own remark (§3.1): it "always holds" with this L. On LH-G, L = O(1) (PROOF SKETCH): (I − Φ_γ)X_k depends only on γ ∩ N(k), where N(k) is k's group plus its linked group. That leaves ≤ p·4^g distinct vectors. |
| Y7 | C: g ≍ p^{2α}; κ + α ≥ C₁(L + L̃ + 2), with C₁ an **unspecified universal** constant | YWJ-prior **yes** by choice. Paper-prior: **cannot be verified as stated, and fails against ZYVR's explicit version** | Paper-prior: g = n gives α = log n/(2 log p). For \|γ\| ≤ s₀ the BB ratio (k+1)/(2p−1−k) gives κ_eff = 1 − O(log s₀/log p), so κ_eff + α ≤ 1.5 + o(1) when p ≥ n. ZYVR's Thm S2 (D) needs κ ≥ 4(C₀ + C₁) + 2 with C₁ζ ≥ 4, i.e. κ ≥ 18. |
| Y8 | D(s₀): (2ν⁻²ω(X) + 1)s* ≤ s₀ ≤ n/(8C₀K log p) − 16L̃σ₀² | YWJ-prior **yes** with a fixed s₀. The paper's cap K = ⌊n/2⌋ **fails** the upper bound for every large n | ω(X) = max_γ ‖(X_γ'X_γ)⁻¹X_γ'X_{γ*∖γ}‖²_op ≤ s*·λ_max(Σ_{S₀})/ν, which is bounded. So a fixed s₀ ≥ (2ν⁻³s*λ_max + 1)s* works. |
| Y9 | beta-min (8)/(9a): min_{j∈S}\|β_j\|² ≥ c₀(α + κ + L)σ₀² log p/n | **Yes**, eventually | β are fixed (the suppressor has \|ψβ\| > 0) and log p/n ≤ A log n/n → 0. The constant c₀ is unspecified, so no explicit first n is available. |
| Y10 | Algorithm: symmetric add/delete/swap MH (3) on M(s₀) | **Not** the paper's algorithm | — |

**Their conclusion on LH-iid (p ≥ n, YWJ-prior, fixed s₀).** This is a PROOF SKETCH of applicability; the conclusions
are theirs. With probability ≥ 1 − 4p^{−c₁}:
- **Mixing time.** τ_ε ≤ c₁ p s₀² (c₂ α (n + s₀) log p + log(1/ε) + 2) = O(α p n log p) iterations. This is the
  **worst case over starts** in M(s₀): it covers the empty model and the paper's start mode S°.
- **Posterior concentration.** π_n(S₀ | Y) ≥ 1 − c₁/p (Thm 1).
- **Discovery.** γ_t = S₀ with probability ≥ 1 − c₂p^{−c₃} for every t ≥ c₁ p s₀²(c₂ α (n + s₀) log p + log p + 2) (Cor. 2).
- **Cost.** Each iteration scores one model, so the cost is O(α p n log p) scores, with unspecified universal constants.
- **Starting state.** None is required. YWJ note that a start at γ* removes the n term.
- **s₀.** Their tuning cap, fixed here.
- **Beta-min constant.** Universal and unspecified.

### 4.2 ZYVR (2022), Theorem 1 (dimension-free mixing of LIT-MH)

| # | Their condition | Holds on LH? | Proof / counterexample |
|---|---|---|---|
| Z0 | Model (3): Zellner g with 1 + g = p^{2κ₁}, π(φ) ∝ 1/φ, p^{−κ₀\|γ\|} on M(s₀) | **No** for the paper-prior | As in Y0. |
| Z1 | n = O(p) | LH-iid with p ≥ n **yes**. LH-G **only if** p ≍ n | — |
| Z2 | s₀ log p = O(n) | **Yes** for their fixed s₀; **no** for the paper's K = ⌊n/2⌋ | — |
| Z3 | κ = O(s₀) | **Yes** (a tuning choice) | — |
| Z4 | Condition 1 with c₀ = 2 and 4 ≤ c₁ ≤ nκ₁ − κ | YWJ-prior on LH-iid: **yes** w.p. 1 − O(p^{−a}), via Thm S2 (A)–(F) (PROOF SKETCH, same checks as Y2–Y9; (F) holds because β is fixed). **Paper-prior: (1b) and (1c) yes, (1a) with c₀ = 2 no** when p ≍ n | (1b): see Prop. U below and §5 (c₁ = 18.6, 181, 1509 at n = 1.6·10³, 1.28·10⁴, 1.02·10⁵, p = 16). (1a): for overfitted γ with \|γ\| = k fixed, max_{j∉γ} log B(γ, γ+j) = log((k+1)/(2p−1−k)) − ½ log(n+1) + max_j χ²₁,j/2 + o_P(1) = −½ log n − ½ log log p + O_P(1). With n ≍ p this is about p^{−1/2}, so c₀ ≈ ½ < 2 (PROOF SKETCH). |
| Z5 | Thm S2 (A): ‖Xβ*‖² ≤ g log p; (B) restricted eigenvalue ζ on M(s₀); (C) sparse projection with C₁ζ ≥ 4; (D) κ₀ ≥ 2, κ₁ ≥ ½, κ ≥ 4(C₀ + C₁) + 2; (E) the s₀ sandwich with Ψ(X); (F) β²_min ≥ 128(κ + C₀ + C₁)log p/(ζ²n). The noise variance is normalised to σ_z² = 1 | As Y2, Y5, Y6, Y7/C, Y8, Y9: **yes** for the YWJ-prior with a fixed s₀ on LH-iid. (D) and (E) **fail** for the paper-prior, as do (A) for fixed p and the cap. | — |
| Z6 | Algorithm: LIT-MH (12)–(14). Informed, thresholded add/delete proposals, plus swaps only at \|γ\| = s₀ | **Not** the paper's algorithm | — |

**Their conclusion on LH-iid (YWJ-prior; PROOF SKETCH of applicability).** T_mix ≤ 800 max{nκ₁/c₁, 3s₀} = O(n) LIT-MH
iterations:
- **Starts.** This is the worst case over starts in M(s₀).
- **Cost.** Each iteration evaluates the posterior on about p neighbours (O(p\|γ\|²) per move, ZYVR §2.3), so the cost
  is O(np) scores. Remark 2: if c₁ grows with n, as it does on LH because β is fixed, the bound can drop to O(s₀) iterations.
- **Constants.** They are explicit here (800). No starting state is required.

### 4.3 Zanella & Roberts (2019), §4.5

| Their condition | Holds on LH? | Why |
|---|---|---|
| §4.5.2: X'X diagonal (so n ≥ p) | **No** | Groups are equicorrelated (ρ > 0) and hubs are linked (ψ ≠ 0). |
| §4.5.3: m regressors perfectly collinear with each other **and with the data vector**, the rest orthogonal; g-prior with a generalised inverse; h ∈ (0,1) fixed; Assumption 1 | **No** | ρ < 1, no column reproduces y, and the paper's prior is BB(1,p) (random h), not fixed h. |
| Thm 1 (TGS vs GS asymptotic variances, any target) | Holds (it is general) | It gives no rate and no statement specific to LH. |

**Conclusion on LH:** none. ZR §4.5 shows relaxation times of wTGS of O(s) in two extreme correlation structures, and
LH is neither of them.

### 4.4 Griffin, Łatuszyński & Steel (2021)

| Their condition | Holds on LH? | Why |
|---|---|---|
| Model (1)–(2): normal linear model, σ⁻² prior, g- or independent prior, Bernoulli(h) size prior, optionally h ~ Be(a,b) | Partly | BB(1,p) is the h ~ Be(1,p) extension they mention. The ridge g = n prior, the IG(0.01, 0.01) prior and the cap K are outside the stated model. The cap is harmless for ergodicity on a finite irreducible space (my reading, not their statement). |
| Thm 1 (ergodicity and SLLN of EIA/ASI): simultaneous uniform ergodicity (Lemma 1) plus diminishing adaptation (Lemma 2) | **Yes**, trivially | Γ is finite and the target is positive. |
| Prop. 1 (optimality of the random-walk proposal for product-form posteriors) | **No** | The LH posterior is not of product form. |

**Conclusion on LH:** only qualitative convergence of their adaptive samplers. No polynomial bound and no
starting-state statement.

## 5. Statements

**Proposition U (underfitted models are never local modes of the paper's target on LH-G).**
- **Hypotheses.** G (fixed design, Gaussian noise σ² > 0 fixed); LH-G with p = p_n ≤ δ n for a small fixed δ (δ < c_U/σ²
  suffices, c_U below); s₀, β, ρ, ψ fixed; the paper's target on M(K).
- **Claim.** There is c_U = c_U(φ₀, β, ψ) > 0 such that, with probability → 1, simultaneously for every γ ∈ M(K) with
  S₀ ⊄ γ and |γ| < K, some j ∈ S₀ ∖ γ satisfies log π(γ ∪ {j})/π(γ) ≥ c n.
- **Consequence.** ZYVR Condition (1b) holds on all of M(K) with c₁ ≍ n/log p.
- **Status.** PROOF SKETCH.

*Sketch.*
1. **Signal.** By RE on all of M(K) (Y5),
   ‖(I − P_γ)μ‖² = ‖(I − P_γ)X_{S₀∖γ}θ_{S₀∖γ}‖² ≥ (n − 1)φ₀²‖θ_{S₀∖γ}‖² ≥ (n − 1)φ₀² min_j θ_j².
2. **Best single addition.** By YWJ's Lemma 8 argument, one j ∈ S₀∖γ has
   ⟨(I − P_γ)x_j, μ⟩²/‖(I − P_γ)x_j‖² ≥ ‖(I − P_γ)μ‖²·φ₀²/s₀ ≥ c_U n.
3. **Noise.** The noise enters through ⟨u, ε⟩ for a unit vector u ∈ span X, and |⟨u, ε⟩| ≤ ‖P_X ε‖ = σ√p(1 + o_P(1))
   uniformly over all (γ, j). So the RSS drop is ≥ (√(c_U n) − σ√p(1 + o(1)))² ≥ c n when p ≤ δ n.
4. **Ratio.** RSS_γ ≤ ‖y‖² = n − 1. Hence
   ν log(RSS_γ/RSS_{γ+j}) ≥ (n/2)·c n/(n − 1) ≥ c n/2.
   This dominates the remaining terms, −½ log(n+1) and the prior ratio ≥ 1/(2p).
5. **Not yet written out.** The constant bookkeeping, and the replacement of y by its standardised version (scale factor s_y).

**Corollary U′.** Under the same hypotheses, every local mode of π under add/delete/swap moves on M(K) is overfitted.
Status: PROOF SKETCH, from U. Whether S₀ is the **unique** local mode on M(K) is OPEN in general. It holds in every case
enumerated in §6 (p ≤ 20). The obstacle is (1a) on very large overfitted models: under cap K, c₀ < 0 at small n (§6),
which is the phenomenon behind YWJ's demand for a small cap.

**Statement R3 (positioning; answers the referee's question).**
- (i) Under the YWJ-prior with a fixed cap, YWJ Thm 2/Cor 2 and ZYVR Thm 1 apply to LH-iid (p ≥ n, p ≤ n^A). They give
  recovery of S₀ and posterior mixing from any sparse start, in O(α p n log p) single-model scores (YWJ) or
  O(n) informed iterations ≈ O(np) scores (ZYVR). PROOF SKETCH (hypothesis checks in §4).
- (ii) For the paper's target, Conditions Y0, Y7, Y8 and Z4(1a, c₀ = 2) fail, and Y1 fails for exact-Gram LH. Neither
  theorem applies as stated (PROVED for the failures Y0, Y8 and Z2, which are definitional; PROOF SKETCH for Z4(1a)).
- (iii) The property that drives both proofs, Condition (1b)/(1c), does hold for the paper's target on LH (Prop. U).
  So the failure in (ii) concerns prior strength and the size cap, not the posterior landscape. A YWJ-style
  canonical-path or drift analysis for the paper's prior on LH would very likely succeed (CONJECTURE, supported by §6).

## 6. Evidence (exact enumeration; `scripts/cond1_lh.py`, output in `results/cond1_lh.md`)

Setup:
- **Model.** The paper's exact target (W1-EXP's `log_m`, copied verbatim as `bvs_exact_W1EXP.py`), on all 2^p models with
  cap K = min(p, ⌊n/2⌋). Exact-Gram LH (W1-EXP's `lh_family_W1EXP.py`).
- **Columns.**
  - c₁ and c₀ are ZYVR's Condition 1 exponents in log_p units, on M(cap). "modes" counts local modes under
    add/delete/swap.
  - log₁₀π₀(S₀) is the start law.
  - The YWJ columns give the hitting time of S₀ for chain (3), 40 replicates each, from ∅ and from the start mode S°.

LH c = 1 (p = 16, ρ = 0.7, ψ = 0.5, S₀ = {0, 4, 8}, masked {4}), cap 6:

| n | log₁₀ π₀(S₀) | π(S₀) | c₁ (1b) | c₁ (1c) | c₀ (1a) | modes M(6) | modes M(K) | YWJ hit from ∅ med/max | from S° med/max |
|---|---|---|---|---|---|---|---|---|---|
| 200 | −2.12 | 0.63 | 2.81 | 4.36 | −0.30 | 1 | 1 | 87 / 284 | 22 / 111 |
| 1600 | −2.60 | 0.92 | 18.55 | 20.33 | 1.12 | 1 | 1 | 86 / 191 | 50 / 169 |
| 12800 | −2.89 | 0.98 | 181.10 | 183.33 | 1.88 | 1 | 1 | 77 / 236 | 36 / 139 |
| 102400 | −3.48 | 0.99 | 1508.66 | 1511.27 | 1.87 | 1 | 1 | 67 / 168 | 41 / 226 |

LH c = 2 (p = 20, ρ = 0.85, ψ = 0.5, S₀ = {0, 4, 8, 12, 16}, masked {4, 12}), cap 8:

| n | log₁₀ π₀(S₀) | π(S₀) | c₁ (1b) | c₁ (1c) | c₀ (1a) | modes M(8) | modes M(K) | YWJ hit from ∅ | from S° |
|---|---|---|---|---|---|---|---|---|---|
| 200 | −3.97 | 0.55 | −0.34 | 0.89 | 0.22 | 1 | 1 | 112 / 475 | 95 / 862 |
| 1600 | −4.75 | 0.79 | 10.58 | 12.03 | 0.14 | 1 | 1 | 142 / 288 | 76 / 207 |
| 12800 | −5.66 | 0.96 | 84.75 | 86.78 | 1.50 | 1 | 1 | 104 / 220 | 93 / 242 |
| 102400 | −6.51 | 0.97 | 775.78 | 778.17 | 1.40 | 1 | 1 | 126 / 247 | 93 / 272 |

What this shows:
- **The start is masked.** π₀(S₀) → 0 at the predicted rate of −½ log₁₀ n per masked variable. The observed slopes are 0.45 (c = 1) and 0.85 (c = 2) per ×8 in n, against 0.45 and 0.90 predicted,
  while π(S₀) → 1. The method's partition equals the groups throughout.
- **The posterior is not masked.**
  - S₀ is the unique local mode of the paper's posterior over the whole capped space in every case, n = 200 included.
  - c₁ grows linearly in n (×8 per ×8 in n), as Prop. U predicts.
  - A plain random-walk MH started at ∅ hits S₀ in O(10²) iterations, independent of n.
- **The difference from YWJ/ZYVR is the overfitted side.** c₀ is small, and negative at n = 200 (and on M(K) at
  n ≤ 1600). With p fixed, log_p units make c₀ look larger than it would be at p ≍ n (§4.2 Z4).
- **Limits.** These are p ≤ 20, fixed-p enumerations, so this is evidence for the qualitative claim only. Hitting times
  are not mixing times.

## 7. What Theorem 5 adds, and what it does not

**It does not add:**
- **Polynomial-time discovery of S₀ on LH by some sampler.** On LH-iid this is implied by YWJ Thm 2/Cor 2 and ZYVR Thm 1
  under their priors (§4). For any prior with Condition (1b), even a greedy search does it; the campaign's own W7-SEP
  Prop. GU and SEP(C) show that the production local search from the start mode suffices.
- **Evidence that LH is computationally hard.** It is not: LH's posterior is unimodal with large gaps. LH is hard only for
  the method's own block-product start law. The masking is a blind spot of π₀ and does not reside in π.
- **Mixing to π.** Theorem 5 is weaker in kind: it concludes P(Ŝ = S₀) → 1 for the HPM over scored models, not
  convergence in TV to π.
- **Any claim of being "first"** to give computational guarantees for BVS samplers.

**It adds, and each item is narrower than the referee feared but genuine:**
1. **It is about the algorithm and the target the paper uses.** That means the BB(1,p) size prior capped at ⌊n/2⌋, the
   ridge g = n prior and the proper σ² prior. The cap and the prior strength are exactly where the YWJ/ZYVR hypotheses fail
   (Y7, Y8, Z4(1a)). YWJ call a cap s₀ ≲ n/log p necessary for *their* mixing proof. Theorem 5 needs no mixing, so it
   needs no such cap. It also covers exact-Gram LH (p ≤ n − 1, p fixed allowed), which is outside both papers' stated regime.
2. **Its output is an estimator, not a chain**: the HPM over all scored models (a deterministic ledger), an unbiased
   evidence estimate Ẑ with a one-sided Markov certificate, and Rao–Blackwellised PIPs (Theorems 4 and 6, and
   Proposition 2). It comes with a deterministic polynomial score count (T32(i), Theorem 5(c)), not a mixing time with
   unspecified universal constants.
3. **The start is exact and proved masked.**
   - Theorem 2 (T27 via W1-EXP Thm 5(b)) proves π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} while π₀(R₀) → 1.
   - W7-SEP SEP(A)/(B) shows that start-only iid draws, and one-shot importance reweighting, need p^c n^{c/2} draws.
   - Theorem 5 shows the method's moves repair this.

   This is a statement about a natural, fast, exactly samplable initialiser and its failure mode, which the MCMC
   literature (worst-case start) does not address.
4. **Neither literature reaches the study's regime.** YWJ explicitly leave the intermediate-signal regime (their (10)) open
   and suspect slow mixing there. Theorem 5 does not reach it either, so this is a shared limitation, not an advantage.

**Honest bottom line.** If the referee's question is "does the mixing literature already imply that a simpler sampler
finds S₀ on LH in polynomial time?", the answer is **yes for their priors** (PROOF SKETCH of applicability) and
**almost certainly yes for ours** (Prop. U plus enumeration; not a published theorem). Theorem 5's contribution is
therefore not computational hardness. It is a guarantee for the SMC-BVS output (HPM ledger, Ẑ, explicit cost) under
the paper's prior, together with a proved diagnosis and repair of its exact start.

## 8. Draft paper paragraph (≤ 250 words; 245 words)

> **Relation to computational guarantees for Bayesian variable selection.** Yang, Wainwright and Jordan (2016) proved that
> an add–delete–swap Metropolis–Hastings sampler mixes in O(pn log p) iterations from any start, for a g-prior posterior
> truncated at a model size s₀ ≲ n/log p, under restricted-eigenvalue, sparse-projection and beta-min conditions; Zhou,
> Yang, Vats, Roberts and Rosenthal (2022) obtained an O(n) bound, free of p, for an informed sampler under the same
> conditions. Both proofs rest on one property of the posterior: every underfitted model has a missing true covariate
> whose addition raises the posterior by a polynomial factor. The linked-hub family of Theorem 5 has this property; its
> masking is a feature of our block-product start law, not of the posterior, and under their priors their theorems apply
> to its random-design version. Polynomial-time recovery of S₀ on this family is therefore not new, and Theorem 5 is not
> a hardness result. What it adds is narrower. It concerns the algorithm and posterior we report (a beta-binomial prior
> capped at ⌊n/2⌋, outside the range those proofs allow); it controls the reported highest-probability model, the
> unbiased evidence estimate and an explicit score count rather than a mixing time; and, with Theorem 2, it shows that an
> exact start whose masking is proved, and which start-only draws or one-shot reweighting cannot repair with fewer than
> p^c n^{c/2} draws, is repaired by the method's own moves. Like those results, it does not reach the weak-signal regime
> of our n = 200 study.

## 9. Draft one-sentence contribution statement

> On an explicit design family where the method's exact block-product start provably misses the true model, we prove
> that the SMC-BVS output — its highest-scored model, reported with an unbiased evidence estimate and a polynomial score
> count — recovers the true model with probability tending to one under the paper's own prior; the family is not hard
> for local MCMC, which under the priors of Yang et al. (2016) and Zhou et al. (2022) mixes rapidly on it.

## 10. What fails and why (routes tried)

- **"LH violates the mixing papers' design conditions"**: false. RE holds on LH-G for every model size, SI holds,
  beta-min holds (β fixed) and ω(X) is bounded. The mismatches are all on the *prior* side (g, κ, cap) and the regime side
  (p ≥ n). None is on the design side.
- **"The masking makes the posterior multimodal, so MCMC is slow on LH"**: false. The masking lives in π₀ only (§6;
  Prop. U). At S° = S₀ ∖ M, adding a masked hub j_b has population gain β²ψ²(1 − ψ²)n > 0, because the residual of μ on
  S° is βψ(ψx_{j_a} − x_{j_b}). So the target sees j_b, while the block-wise start (which regresses y on block C_b alone)
  does not: Cov(X_{C_b}, μ) = 0.
- **"Their theorems apply verbatim to the paper's posterior"**: false (Y0, Y7, Y8, Z4(1a)). The (1a) failure is not
  only slack in the proofs. Under BB(1,p) with g = n the best null addition to an overfitted model costs only about
  n^{−1/2}, against their p^{−2}.

## 11. Needs escalation

1. **Published numbering.** Check YWJ's theorem, assumption and equation numbers against the published AoS PDF (I read
   arXiv v1, May 2015; the AoS version appeared Dec 2016 and may be renumbered). Same check for ZYVR's journal version
   against arXiv v3.
2. **Applicability on LH-iid.** A line-by-line check of YWJ Thm 2 and ZYVR Thm S2 on LH-iid. The RE union bound,
   sparse projection, ω(X), and especially Assumption A with the chosen g are standard, but I sketched them.
3. **Prop. U.** Write it in full, including the s_y standardisation and the uniform noise bound with p ≤ δn. Settle
   whether p up to n − 1 is reachable; the noise bound ‖P_X ε‖ ≈ σ√p is crude there.
4. **The analytic c₀ ≈ ½ claim (Z4).** It uses max_j χ²₁,j/2 ≈ log p − ½ log log p for nearly independent null
   statistics, which an independent check should confirm.
5. **Conjecture (Y1 extension, and (iii)).** A YWJ-type spectral-gap bound for the paper's prior on LH-G, with the cap
   K = ⌊n/2⌋, is OPEN. Unimodality on M(K) beyond p ≤ 20 is OPEN.

## 12. Outside scope

- **A cheaper repair.** Prop. U means a greedy add-only search from ∅ or from S° finds S₀ on LH in ≤ s₀ steps. This is
  consistent with W7-SEP Prop. GU. If the paper wants a family where the SMC bridge is *needed* against local MCMC,
  LH is the wrong family, and a posterior-barrier design (W4-SHARE PB, or YWJ's App. A.2 example) would be the place to
  look. Not pursued.
- **A tuning knob.** The paper's prior has a weak per-addition penalty for overfitted models (c₀ ≈ ½ at p ≍ n). This
  bears on posterior misses towards supersets at n = 200 (F-REFEREE §4: "prefers a superset in most of its misses").
  It is a prior-choice matter fixed by Felipe and is noted only.

## 13. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change needed? |
|---|---|---|---|---|---|
| R3(a), YWJ on LH | Under the YWJ-prior with a fixed cap, YWJ Thm 2/Cor 2 apply to LH-iid (p ≥ n): mixing and discovery in O(α p n log p) scores from any start | high | high (hypothesis checks only) | RE(s₀) for LH-iid and Assumption A with g ≍ p^{2α} | no |
| R3(a′), YWJ on the paper's target | Not applicable as stated (Y0, Y7, Y8; Y1 for LH-G) | high (definitional) | done | — | no |
| R3(b), ZYVR on LH | Same applicability for LIT-MH via Thm S2; O(n) iterations, O(np) scores | high | high | Thm S2 (A)–(F) on LH-iid | no |
| R3(b′), ZYVR on the paper's target | (1b)/(1c) hold (Prop. U); (1a) with c₀ = 2 fails at p ≍ n | medium-high | medium | max-χ² asymptotics at p ≍ n | no |
| Prop. U | Underfitted models are never local modes of the paper's posterior on LH-G, p ≤ δn | high | high | uniform noise bound | no |
| ZR §4.5, GLS | No quantitative consequence on LH | high | done | — | no |
| Paper wording | Theorem 5 is not a hardness or "first" result; it is an output-level guarantee under the paper's prior, with a proved start diagnosis and repair | high | — | — | no |
