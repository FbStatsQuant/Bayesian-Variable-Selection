# LIT-MCMC — REPORT: BVS samplers and their mixing / discovery guarantees, positioned against our results

Run LIT-MCMC, branch `theory/LIT-MCMC`, 2026-11-02. Status words follow `theory_campaign/PROTOCOL.md`. Everything is a
**candidate**: nothing here has been reviewed. The source log, with verbatim quotes, is `NOTES.md` (entries N1–N13). The
script is `scripts/rz_lh.py` (seed 20261102 + n) and its output is `results/rz_lh.md`. This run builds on API-POS
(`theory/API-POS · REPORT.md`), which already checked YWJ, ZYVR, ZR and GLS hypothesis by hypothesis on LH. That work is
cited here, not redone.

## 0. Headline

1. **(a) Fast discovery of S₀.** Every published polynomial-mixing theorem for BVS rests on one landscape hypothesis:
   - Unimodality with a strong ratio, R ≫ M. Here R is the smallest best-neighbour posterior ratio over all non-modal
     models, and M is the neighbourhood size.
   - The papers using it are YWJ 2016, ZYVR 2022, Zhou–Smith 2022, Zhou–Chang 2023 and Chang–Zhou 2024/25.
   - The theorems also need a prior stronger than ours (g ≍ p^{2α}, p^{−κ|γ|}) and a sparse cap s₀ ≪ n/log p.

   **Exact enumeration of the paper's own target on LH** (`results/rz_lh.md`) finds S₀ as the unique mode with no other
   local mode, so R > 1. But the **sufficient condition R > M fails at n = 200 and n = 1,600** (c = 1 and c = 2), and
   **R > M² (informed samplers) fails at every n tested, up to 102,400**. The binding direction is the *overfitted* side:
   deleting an extra variable from a superset of S₀. That side matters for mixing, not for discovery.

   So: on LH, "rapid mixing" is not certified by any published theorem for our target. "Fast discovery" is supported
   by the landscape (API-POS Prop. U, PROOF SKETCH) but is not stated as a theorem anywhere I read.

2. **(b) No paper I read proves a BVS family where standard MCMC mixes slowly but tempering or SMC provably succeeds.**
   - What exists: a slow-mixing example for untruncated-prior RW-MH (YWJ App. A.2, null truth, saturated-model trap,
     PROVED there). No positive tempering or SMC result accompanies it.
   - Generic continuous-space separations exist (Mathews–Schmidler 2024: SMC is polynomial on mixtures of log-concave
     densities where MCMC is exponential).
   - Generic tempering lower bounds exist too (Woodard–Schmidler–Huber 2009: low *persistence* plus low cold-level
     conductance imply torpid PT/ST).
   - Gamarnik–Zadik give OGP *evidence* of local-search hardness for n < c·s₀ log p, not an MCMC lower bound.
   - Status of "no such BVS separation is published": OPEN as a literature claim. It rests on my search, which is not
     exhaustive.

3. **(c) Value of our masked-regime theorems.**
   - The masked regime is, in WSH's language, *low persistence of the S₀ basin under the start φ₀ = π₀*. In
     Mathews–Schmidler's language it is a tiny µ⋆, which makes their particle bound ∝ 1/µ⋆ ≈ n^{c/2}.
   - No published SMC or tempering theorem covers a start whose mode misses S₀. Our T38 (b1-LH)/(b2-LH) and the
     W7-SEP "moving off the start is needed" result therefore fill a real gap.
   - Their *mechanism*, however, is a unimodal-landscape (YWJ-type) argument, and this is the main threat (§3). On LH a
     plain add-delete-swap chain also finds S₀ (API-POS: ≈ 100 iterations). So the masked theorems say that the method
     fixes a problem the method itself created (the start). They do not say the method beats MCMC.

4. **One gap that is ours to claim.** I found no published result giving a *hitting or scoring time* of S₀ from
   conditions (1b)/(1c) alone, without (1a), without a small cap, and with a BB(1, p)/g = n prior. Our repair theorems
   (T37/GU, T38(b1)) are of this type, for greedy local search. Status of the gap claim: CONJECTURE (literature),
   medium confidence.

---

## 1. Annotated table

Legend for the "holds on ours?" column:
- **LH**: the linked-hub family. LH-G is exact-Gram, p ≤ n − 1; LH-iid is p ≥ n allowed.
- **Study**: n = 200; p ∈ {500, 1000}; s₀ = 14; S1–S6 with λ_min(Σ) ≥ 0.10; the paper's target (g = n, unit ridge,
  IG(0.01, 0.01), BB(1, p), cap K = 100).
- "Y-prior" means the theorem's own prior.
- Our IDs are those of `Docs/THEORY_PRIORITIES.md` and the branches named.

| # | Work (venue, year) | Method | What is PROVED (conditions) | Holds on ours? | Relation to our results |
|---|---|---|---|---|---|
| 1 | Yang, Wainwright, Jordan, *AoS* 44(6):2497–2532 (2016) [N1] | Add/delete/swap RW-MH, eq. (3) | **Thm 2.** Under A (design normalisation), B(s₀) (RE + sparse projection), C (beta-min, high or low SNR), D(s₀) (size cap s₀ ≲ n/log p, prior p^{−κ\|γ\|}, g = p^{2α}), w.p. ≥ 1 − 4p^{−c₁}: τ_ε ≤ c₁ p s₀²[c₂α(n+s₀) log p + log(1/ε) + 2]. **Cor 2:** γ_t = γ* after that many steps. **App. A.2:** untruncated prior, p = n, null truth: mixing time exponential in n w.p. ≥ ½ (conductance of {full model}). | LH-iid with Y-prior: yes (API-POS §4.1, PROOF SKETCH). Paper's target: **no**. D(s₀) fails (cap ⌊n/2⌋), and the prior is too weak (API-POS Y0, Y7, Y8). Study: s₀ log p/n = 0.43–0.48 against their ≤ 1/32-type constants: no. | **Threat** to the novelty of T38 discovery on LH (API-POS). Complementary to T03 (posterior concentration), whose analogue is their Thm 1. A.2 is the only BVS slow-mixing proof found; our cap K = ⌊n/2⌋ is exactly the kind of cap A.2 says is needed but D(s₀) says is too large. |
| 2 | Zhou, Yang, Vats, Roberts, Rosenthal, *JRSS-B* 84(5):1751–1784 (2022) [N10] | LIT-MH (locally informed, thresholded) | **Thm 1.** If n = O(p), s₀ log p = O(n), κ = O(s₀), and Condition 1 holds with c₀ = 2 and 4 ≤ c₁ ≤ nκ₁ − κ, then T_mix ≤ 800 max{nκ₁/c₁, 3s₀} (sup over starts in M(s₀)). Each step costs O(p) scores. | LH-iid with Y-prior: yes (API-POS). Paper's target on LH at n = 200: c₁(1b) = 2.81 / −0.34 and c₀ = −0.30 / 0.22 (API-POS §6), so **no**. Study: unverifiable (no enumeration); heuristic §2.3 gives c₀ ≈ log_p(2√n/k) ≈ 0.1. | Same as #1, and stronger. Its Condition (1b) is what API-POS Prop. U checks for our target. |
| 3 | Chang & Zhou, arXiv:2404.03867v2 (2025), "Accepted by Bernoulli" (listing) [N2] | RW-MH and informed MH on general discrete spaces | **Thm 1.** ρ = R/M > 1 ⇒ π(x*) ≥ 1 − ρ⁻¹, Gap⁻¹ ≤ c(ρ)M. **Thm 2.** R > M² ⇒ dimension-free relaxation for informed MH. **Thm 4 (multimodal / restricted).** If ρ on X₀ exceeds 1, π(x₀) ≥ η and π(X₀) ≥ 1 − ε²η²/5, then τ_{x₀} ≤ c(ρ)M log(1/(2ε²η²)): the start enters only through log(1/π(x₀)). **Cor 5:** YWJ setting, unrestricted space, τ = O_p(p²κs log p). | **Computed exactly on LH** (`results/rz_lh.md`). R > 1 everywhere (unique mode S₀). R > M fails at n ∈ {200, 1600}, both c, on both M(K) and M(s); it holds at n ≥ 12,800 (c = 1) and n = 102,400 (c = 2). R > M² fails everywhere. | Their Thm 4 is the cleanest **threat**: with a unimodal target, a bad start costs only log(1/π(x₀)). Their Example 3 (p = 3, X₁ᵀX₂ = −0.8n), where π is unimodal but decreases along some paths towards δ*, is a suppressor example of LH type. |
| 4 | Zhou & Smith, AISTATS 2022 (PMLR 151) [N6] | Informed importance tempering (IIT) | **Lemma 3 / Thm 1.** Assumption 1: \|N(x)\| ≤ p^α; ∃ T with π(T x) ≥ p^ν π(x), ν > α. Then Gap ≥ κ(p, α, ν) min P(x, Tx), and IIT has Gap(Q_h) ≥ κ p^{ν−α}/2 (h = h₊₁). | Assumption 1 is R ≥ p^ν > M = p^α. On LH it fails at n ≤ 1,600 (#3 table). | Same as #3. The "tempering" here is importance re-weighting of a rejection-free chain, not a temperature bridge. |
| 5 | Zhou & Chang, *AoS* 51(3):1058–1085 (2023) [N12] | RW-MH on DAG equivalence classes | A general finite-state mixing bound under a unimodal-ratio condition (Thms 1–2), and rapid mixing for DAGs with p = e^{o(n)}. | Not BVS. | Background for #3. |
| 6 | Li, Smith, Zhou, arXiv:2304.06251v2 (2024) [N7] | Rejection-free MTM / importance MCMC | Asymptotic-variance comparison with the M–H versions (Thm 1, given Gap(P̃) < 1); complexity theory for a non-M–H discrete sampler. | Inherits #3/#4. | Not a discovery result. |
| 7 | Zanella & Roberts, *JRSS-B* 81(3):489–517 (2019) [N12] | Tempered Gibbs sampler (TGS), weighted TGS | **Thm 1.** var(h, TGS) ≤ b² var(h, GS) + b² var_f(h): never much worse than Gibbs. §4.5: quantitative BVS results only for diagonal and fully collinear X (API-POS). | LH and study: no quantitative statement applies. | Complementary. TGS's stated strength ("pairwise and k-wise negative correlations") is the LH suppressor geometry, but nothing about LH or masking is proved. |
| 8 | Griffin, Łatuszyński, Steel, *Biometrika* 108(1):53–69 (2021) [N12, via API-POS] | Adaptive (individual-adaptation) MCMC | Ergodicity and SLLN, no rate. | Holds (ergodicity is generic). | No overlap. Asymptotic only. |
| 9 | Liang, Livingstone, Griffin, *Stat. Comput.* (2022), arXiv:2110.11747 [N12] | Adaptive random-neighbourhood informed (ARNI/PARNI) | **Thm 2.** Ergodicity and SLLN for PARNI-KW/RM, no rate. | Generic. | No overlap. |
| 10 | Staerk, Kateri, Ntzoufras (2024), arXiv:2105.01039 [N12] | MAdaSub (adaptive independence proposals) | **Thm 1.** Ergodic, WLLN, no rate. | Generic. | No overlap. |
| 11 | Zanella, *JASA* 115:852–865 (2020), arXiv:1711.07424 [N12] (pages UNVERIFIED) | Locally balanced informed proposals | **Thm 2/3.** Peskun-type dominance of balanced g̃(t) = min{g(t), t g(1/t)}. **Thm 4.** High-dimensional weak limit for product-type targets. | No BVS mixing claim. | Our Gibbs, swap and neighbour moves are not locally balanced. No overlap. |
| 12 | Gagnon, Maire, Zanella, arXiv:2211.11613v2 (2023; JMLR per search, UNVERIFIED) [N7 area] | Locally balanced multiple-try Metropolis | High-dimensional scaling limits on continuous product targets. Canonical MTM weights are pathological in the transient phase. | Continuous. N/A. | Background only. |
| 13 | Pozza & Zanella, arXiv:2410.23174 (Biometrika 2025, UNVERIFIED) [N11] | Any multiproposal MCMC | **Cor 1.** Gap(P^(K)) ≤ K·Gap(P̃) for arbitrary targets, discrete ones included. | Applies. | It bounds what parallel scoring of neighbours can buy: at most a factor K. It is consistent with W7-SEP's "no super-polynomial separation". |
| 14 | Atchadé, arXiv:1903.11745 (SIAM J. Math. Data Sci. 2021, UNVERIFIED) [N8] | Gibbs sampler, spike-and-slab | **Thm 6.** Polynomial mixing from a warm start ν₀ = Π(·\|δ⁽ⁱ⁾, z) with δ⁽ⁱ⁾ ⊇ δ̃* (a superset of the truth), under H1 (well-specified) and H2 (sparse eigenvalue). It *suggests* the zero start "might result in ... exponential mixing" (not proved). | Our masked start has a mode δ⁽ⁱ⁾ ⊉ S₀, so a Thm 6-type warm start is **not** available in the masked regime. Favourable regime: plausibly yes. | Closest published analogue of our favourable/masked split (Thm 2 = T22 + T27). Complements T38(a). |
| 15 | Jiang, arXiv:2307.05558 (2023) [N9] | Gibbs and stochastic localization, Gaussian spike-and-slab quasi-likelihood | Prop 2.8 (Gibbs rate from a warm start from a frequentist estimator); Thm 3.7 (SL sampler). | Different prior. Warm start again. | Same as #14. |
| 16 | Gamarnik & Zadik, arXiv:1711.04952v2 (2019; AoS 2022 companion, UNVERIFIED) [N5] | Local-search (swap) best improvement | **Thm 2.7.** For iid N(0,1) X, n ≥ C·k log p and σ² ≤ c\|β*\|²_min·min{log p/log log p, k}, LSA from *any* k-sparse start recovers the support. OGP appears for n ≤ c·k log p (evidence of hardness, no MCMC lower bound). | Study S1: n/(s₀ log p) = 2.33 (p = 500), 2.07 (p = 1000). The constants are unspecified, so the study is not certifiably on either side. LH: X is not iid. | Overlaps T37/GU (local search from any centre reaches S₀). It is a **threat** in spirit: "local search from anywhere works when n ≳ k log p" is known for iid X. |
| 17 | Woodard, Schmidler, Huber, *EJP* 14:780–804 (2009) [N4] | Parallel and simulated tempering, general bridges φ_k | **Thm 3.1.** Gap ≤ 12·max over cold levels of the conductance Φ_{T_k}(A), the overlap δ(A, k, l) and the hot-level persistence γ(A, k) = min{1, φ_k[A]/π[A]} (exact grouping in N4). Torpid if A has low persistence hot *and* low conductance cold. | On LH the persistence of the S₀ basin under φ₀ = π₀ is tiny (Thm 2 masking law), but cold-level conductance is **not** small: the target is unimodal (#3 table, 0 local modes). So the bound does not bite on LH. | Gives the masked regime a name (low persistence). Explains why the masking is harmless on LH: no second metastable mode. |
| 18 | Mathews & Schmidler, *AAP* 34(1):1199–1223 (2024) [N3] | SMC with local mixing | **Thm 1.** Error ≤ ε w.p. ≥ ¾ if N ≳ ε⁻² V W Z²/µ⋆ · log(…) and t ≳ the *local* (within partition element) mixing times, where µ⋆ = min over steps and elements of µ_v(A_j). FPRAS for mixtures of log-concave densities where MCMC is exponential. | Masked LH: µ⋆ ≤ π₀(S₀ basin) ≍ n^{−c/2}, so N must grow polynomially in n. Not a fixed-N guarantee; continuous applications only. | Complementary. It is the generic "SMC beats MCMC" theorem, but its price (1/µ⋆) is exactly our masking. Our results avoid it by global moves. |
| 19 | Le Fay, Chopin, Vihola, arXiv:2604.03352v2 (2026) [N12] | Standard and waste-free SMC | **Thms 2.3/3.2.** Finite-sample error bounds when every K_t has spectral gap ≥ γ and 1 + χ²(π_t\|π_{t−1}) ≤ χ̄². Complexity in T and d for tempering. | Needs a global gap of each kernel. On LH at n ≤ 1,600 no published gap bound is available (#3). | Complementary to T32 (cost) and T12 (unbiased Ẑ). It cannot deliver discovery in the masked regime unless the kernels already mix. |
| 20 | Schäfer & Chopin, *Stat. Comput.* 23:163–184 (2013) [N12] (pages UNVERIFIED) | SMC on binary spaces with logistic-conditional proposals | No theorem. Empirical: "global methods ... are often more robust than local methods". | — | Methodological ancestor of SMC-BVS. No guarantee to overlap with. |
| 21 | Kim & Ročková, arXiv:2306.00126 (EJS 19 (2025), UNVERIFIED) [N12, abstract only] | Bayesian CART, grow/prune | Exponential mixing lower bound for "deep isolated signals". | Not BVS. | In linear regression with RE, an isolated signal (zero gain for every single addition) cannot occur at population level: Xᵀμ = Gθ ≠ 0. This is why BVS lower bounds must come from overfitted traps (YWJ A.2) or finite-n noise, not from masking. |

Not read, only seen second-hand (UNVERIFIED): Titsias & Yau 2017, the Hamming ball sampler (local PDF present; no
mixing theorem located in a grep); Schweizer 2012 (SMC in multimodal settings; cited by Le Fay et al.); Marion, Mathews,
Schmidler 2023 (AoS; cited by Le Fay et al. and by #18); Ascolani & Zanella 2025 (probit DA Gibbs, arXiv:2505.14343, search
snippet only).
