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

---

## 2. Statements

### 2.1 Positioning statements (literature claims; status = how sure I am that they are true of the literature)

- **L1 (rapid-mixing hypotheses).** Every polynomial mixing-time theorem for BVS MCMC that I read (#1–#5, #14, #15)
  assumes either
  - (i) a unimodal-ratio landscape on a sparse space, R > M (RW-MH) or R > M² (informed), together with a sparse cap
    s ≲ n/log p and a prior penalty per extra variable of order p^{κ}·g^{1/2} with κ + α large; or
  - (ii) a warm start whose support contains the truth (#14, #15).

  None assumes BB(1, p) with g = n and cap ⌊n/2⌋. Status: CONJECTURE (literature claim); high confidence for the works
  listed, unknown for unread works.
- **L2 (no BVS tempering separation).** I found no published BVS family on which standard BVS MCMC provably mixes slowly
  while a tempering or SMC method provably succeeds. The only proved BVS slow-mixing example is YWJ App. A.2, which is
  cured by a size cap, not by tempering. Status: OPEN (as a literature claim); medium confidence.
- **L3 (SMC theory needs either global gaps or mode mass along the bridge).** The general SMC finite-sample theorems
  (#18, #19, and Marion–Mathews–Schmidler as recalled in #19) need either a spectral gap γ > 0 for *every* kernel or
  local mixing plus µ⋆ = min mode mass along the bridge, with cost ∝ 1/µ⋆. In the masked regime µ⋆ ≤ π₀(S₀-basin)
  ≍ n^{−c/2} (T27 / Thm 2 masking law). Status: PROVED as a reading of the stated theorems (the hypotheses are quoted
  in N3 and N12). Applying it to our masked start uses Thm 2's masking law (a candidate, not adopted).

### 2.2 Proposition OB (the overfitted-side bottleneck for the paper's prior)

**Setting.**
- The paper's target (`METHODOLOGY_v3.md §5`) on M(s) for some s with s₀ < s ≤ K.
- N = add/delete/swap, M := max_{γ ∈ M(s)} |N(γ)| ≥ p − s.
- G (Gaussian noise) and fixed s₀. Let γ_e := S₀ ∪ {e} for a null e ∉ S₀, k := s₀ + 1.
- T_e := (n − k)·[Q_{S₀} − Q_{γ_e}]/Q_{γ_e}, the partial F-type statistic of e given S₀.

**Claim.**
- (i) Exact prior factor: ϖ(S₀)/ϖ(γ_e) = w(k − 1)/w(k) = (2p − k)/k.
- (ii) π(S₀)/π(γ_e) = [(2p − k)/k] · √(n + 1) · exp(−½T_e) · (1 + o_P(1)), uniformly in e.
- (iii) Suppose further that max_{e ∉ S₀} T_e ≥ (2 − ε) log p with probability → 1. This holds, for instance, when the
  null columns' residuals given S₀ are nearly orthogonal (S1-like). Then with probability → 1, R ≤ max_{y∈N(γ_{e*})}
  π(y)/π(γ_{e*}) ≤ C·p^{ε/2}√n/s₀ for e* = argmax T_e.
- Consequently R/M ≤ C p^{ε/2}√n/(s₀(p − s)) → 0 whenever p^{1−ε/2} ≫ √n.

So the hypothesis R > M of Chang–Zhou Thm 1/4, Zhou–Smith Assumption 1 (ν > α), and the analogous c₀ = 2 in ZYVR's (1a)
**cannot hold for the paper's prior when p ≫ √n**. The study (p ≥ 500 ≫ √200 ≈ 14) is far into this range.

**Status.** (i) PROVED (from w(k) = ½/C(2p − 1, k)). (ii)–(iii) PROOF SKETCH: §3.1 below. The step "the best neighbour of
γ_{e*} is S₀" is used only as an upper bound through max_y and needs the swap neighbours to be controlled too; that step is
not verified.

**What OB does NOT say.** It does not say the chain mixes slowly. R ≤ M is the failure of a *sufficient* condition. The
measured hitting times on LH (API-POS §6: median ≈ 70–140 iterations, flat in n) show that discovery is fast anyway.
What OB says is that **no published unimodal-ratio theorem can certify our target in the study's regime**, for a
structural reason: per extra variable, the prior and g-penalty is ≍ p√n, only one power of p, and the noise maximum eats
that power.

### 2.3 Heuristic used in the table (not a statement)
From OB(ii) with T_{e*} ≈ 2 log p: ZYVR's c₀ on the study is ≈ log_p(2√n/k) ≈ 0.1 at n = 200, k = 15, p ∈ {500, 1000}.
This is a heuristic, not checked.

---

## 3. Proofs or sketches

### 3.1 Sketch of OB
1. **Prior.** w(k+1)/w(k) = (k + 1)/(2p − 1 − k) (from `00_COMMON.md` / API-POS §3). So w(k−1)/w(k) = (2p − k)/k.
2. **Determinants.** Write H_S = (n + 1)G_S + I. By the Schur complement for column e given S₀:
   - det H_{γ_e}/det H_{S₀} = 1 + (n + 1)·x_eᵀ(I − X_{S₀}(G_{S₀} + I/(n+1))⁻¹X_{S₀}ᵀ)x_e;
   - det(G_{γ_e} + I)/det(G_{S₀} + I) = 1 + x_eᵀ(I − X_{S₀}(G_{S₀} + I)⁻¹X_{S₀}ᵀ)x_e.

   With ‖x_e‖² = n − 1 and residual fraction 1 − r_e² bounded away from 0 (RE), the ratio of the two is
   (n + 1)(1 + O(1/n)). Its square root is the √(n + 1) factor.
3. **Residual term.** ((2b₀ + Q_{γ_e})/(2b₀ + Q_{S₀}))^{a₀ + n/2} = (1 − T_e/(n − k + T_e))^{n/2 + a₀}(1 + O(1/n))
   = exp(−½T_e)(1 + o(1)) when T_e = O(log p) = o(√n). This needs log p = o(√n). In the study log p ≈ 7 and √n ≈ 14,
   so the asymptotics are marginal there. **Not verified**: the uniformity in e, and the ridge corrections in Q (the
   unit ridge shifts Q by O(1)).
4. **Noise maximum.** Under S1-like nulls, the T_e are approximately χ²₁ and weakly dependent, so max T_e ≥ (2 − ε) log p
   w.p. → 1 (standard Gaussian-maximum bound). Under strong block correlation (S4, S5) the effective number of
   independent nulls is smaller, by about a factor of the block size, which changes only constants in log p.
5. **R bound.** R = min_x max_{y∈N(x)} π(y)/π(x) ≤ max_{y∈N(γ_{e*})} π(y)/π(γ_{e*}). The neighbours of γ_{e*} are:
   - S₀ (delete e*), with ratio ≤ (2p/k)√(n + 1)p^{−1+ε/2}(1 + o(1));
   - deletions of true variables, whose ratio is exponentially small by beta-min;
   - additions, which add another null, with ratio ≲ (k + 1)/(2p) · n^{−1/2}·exp(½T) ≤ p^{ε'}/√n·O(1);
   - swaps of e* for another null e′, with ratio exp(½(T_{e′} − T_{e*})) ≤ 1 by the choice of e*;
   - swaps of a true variable for a null, which are exponentially small.

   So the maximum is the deletion of e*, and R ≤ C p^{ε/2}√n/s₀. M ≥ p − s. Done, modulo steps 2–4.

### 3.2 Why WSH's torpid bound does not bite on LH (supports L3 and headline 3)
- WSH Thm 3.1 bounds Gap by a maximum over three families of terms: cold-level conductances Φ_{T_k}(A), overlaps, and
  hot-level persistences γ(A, k). Torpid mixing therefore needs all three families small for a single A.
- Take A = the S₀ basin. Its persistence under φ₀ = π₀ is ≍ n^{−c/2} (small). But at the target level, Cheeger gives
  Φ_P(A) ≥ Gap(P) for any A. On LH the target is unimodal (`results/rz_lh.md`: 0 non-x* local modes at every n). So
  at the n where R > M holds, Chang–Zhou Thm 1 gives Gap ≥ 1/(c(ρ)M), and the bound is not small.
- At n where R ≤ M no gap bound is available from the literature. The measured hitting times (API-POS) suggest none is
  needed.
- Status: PROOF SKETCH. The cold levels of v3's bridge are intermediate temperatures between π₀ and π, not π itself; I
  have not checked unimodality of those intermediate targets.

---

## 4. Evidence

**Exact enumeration** (`scripts/rz_lh.py`, output `results/rz_lh.md`, run via owls_run -j 2, a few minutes).
- **Inputs.** The paper's exact target, exact-Gram LH, and the same LH settings as API-POS:
  - c = 1: p = 16, ρ = 0.7, ψ = 0.5;
  - c = 2: p = 20, ρ = 0.85.
- **Quantities.**
  - R = min_{x ≠ x*} max_{y∈N(x)} π(y)/π(x) and M = max|N(x)|, with N = add/delete/swap.
  - Two spaces: M(K), the whole capped space, and M(s), the sparse space with s = 6 or 8.
- **Columns.**
  - log_p R and log_p M.
  - The two published sufficient conditions: R > M (RW-MH, Chang–Zhou Thm 1) and R > M² (informed, Thm 2).
  - x* = S₀?, the state attaining R, and the number of non-x* local modes.

| LH | n | space | log_p R | log_p M | R > M | R > M² | x* = S₀ | flattest state | other local modes |
|---|---|---|---|---|---|---|---|---|---|
| c = 1 | 200 | M(K) | 0.95 | 1.58 | NO | NO | yes | full model (16) | 0 |
| c = 1 | 200 | M(6) | 1.06 | 1.54 | NO | NO | yes | {0,4,5,6,8} ⊇ S₀ | 0 |
| c = 1 | 1,600 | M(K) | 1.16 | 1.58 | NO | NO | yes | {0,4,7,8} ⊇ S₀ | 0 |
| c = 1 | 12,800 | M(K) | 1.70 | 1.58 | yes | NO | yes | full model | 0 |
| c = 1 | 102,400 | M(K) | 2.08 | 1.58 | yes | NO | yes | full model | 0 |
| c = 2 | 200 | M(K) | 0.88 | 1.60 | NO | NO | yes | full model (20) | 0 |
| c = 2 | 200 | M(8) | 0.92 | 1.57 | NO | NO | yes | {0,5,8,12,16} (underfitted swap) | 0 |
| c = 2 | 1,600 | M(K) | 0.92 | 1.60 | NO | NO | yes | {0,4,7,8,12,16} ⊇ S₀ | 0 |
| c = 2 | 12,800 | M(K) | 1.37 | 1.60 | NO | NO | yes | ⊇ S₀ (size 7) | 0 |
| c = 2 | 102,400 | M(K) | 1.93 | 1.60 | yes | NO | yes | full model | 0 |

What it shows:
1. **The target is unimodal on LH at every n**, including n = 200. This agrees with API-POS.
2. **The flattest direction is almost always on the overfitted side.** It is either a superset of S₀ or the saturated
   model, which is YWJ App. A.2's trap, here not a mode but nearly flat. This is the side that matters for mixing, not
   for discovery. It matches OB.
3. **The published sufficient conditions fail at the study's n**, and R > M² fails everywhere.
4. **Caveat.** p ≤ 20 is far from the study's p ≥ 500. OB predicts the failure is much worse there. Not checked beyond
   p = 20, since the space cannot be enumerated.

Discovery, as distinct from mixing, is fast on the same family: API-POS §6 measured YWJ-chain hitting times of S₀ of
about 70–140 iterations from ∅ and from the start mode, flat in n. The study's own data agree: W8-SYNTH / S-ELS report
0 search misses in 2,394 completed fits.

---

## 5. Gaps (what nobody has proved that we prove or could prove)

- **G1. Discovery or scoring guarantees from (1b)/(1c) alone, with no (1a), no sparse cap and a weak prior.**
  - Every published result proves *mixing*, which needs the overfitted-side drain (1a) or R > M on the whole space.
  - Our story needs only that S₀ is *scored*: T21/Thm 4 and N200 make the reported HPM right once S₀ is scored and
    ranked first.
  - Our repair theorems give this kind of statement for local search from a near-truth centre: T37 / Prop. GU
    (W7-SEP), T38(b1-LH) with LS0, and (b2-LH) without LS0 under STAB-LH.
  - Nothing in the literature I read states a hitting-time-of-S₀ theorem under (1b)/(1c) only.
  - Gamarnik–Zadik Thm 2.7 is the closest: local search from any start, but for iid X and n ≥ C k log p.

  Value: **real**. Our discovery-and-scoring decomposition (T21) is a different, weaker and more relevant target than
  mixing, and OB shows mixing theorems cannot reach our prior in p ≫ n.
- **G2. SMC/tempering with a start whose mode misses the truth (masked regime).** The published SMC theory either needs
  global kernel gaps (#19) or pays 1/µ⋆ (#18). Persistence results (#17) are only negative. Our masked-regime T38 parts
  are, as far as I found, the first BVS-specific statements of this kind. They cover the masked regime with a polynomial
  budget and no growth in N with n.
- **G3. Finite-n, design-specific statements at n = 200 (N200, API-N200).** No paper gives anything quantitative at
  n = 200 for correlated block designs. All the theorems are asymptotic with unspecified universal constants (YWJ's c₀,
  GZ's c, C).
- **G4. Composition with the output rule.** The literature concerns the chain's law. Our T07 (HPM = Bayes rule) and T21
  (exact inequality for the reported HPM) concern the *reported best-scored model*. I saw no analogue.

## 6. Threats (results that make one of ours standard, weaker or redundant)

- **Θ1 (strongest). Chang–Zhou Thm 4 together with API-POS Prop. U.** If the target is unimodal with a strong ratio,
  any start costs only log(1/π(x₀)) extra. The masked start has log(1/π₀(S₀)) ≈ (c/2) log n, so the start's masking
  costs a log factor. On LH-iid with the YWJ prior this makes "the masked regime is solvable" a corollary of known
  results (API-POS headline 2).
  - Defence: OB shows these theorems cannot be applied to our prior in p ≫ √n. Our theorems are for the target and
    method actually used.
  - That defence is a formal gap, not a substantive one, which is API-POS's own verdict.
  - Wording advice: present the masked theorems as "the method's own start creates the masking, and the method's own
    moves remove it". Do not present them as "MCMC fails here".
- **Θ2. Gamarnik–Zadik Thm 2.7.** "Local search from any k-sparse start recovers the support when n ≥ C k log p" is
  known for iid Gaussian X. It overlaps T37/GU in spirit. Our versions cover correlated (exact-Gram, block) designs and
  the production search, and state a finite move bound. GZ is a citation we must make.
- **Θ3. YWJ App. A.2 and Atchadé's warm-start theorem.** The facts that a size cap and a start containing S₀ matter are
  known (A.2 is PROVED; Atchadé's zero-start remark is not). Our favourable/masked dichotomy (Thm 2 = T22 + T27) must cite
  both.
- **Θ4. W7-SEP already concedes "moving off the start is needed, not tempering".** The literature agrees: no BVS
  tempering separation exists (L2). Pozza–Zanella cap any multiproposal speed-up at the factor K. A claim that tempering
  is *necessary* would be contradicted by the measured RW-MH hitting times on LH. Do not make it.
- **Not a threat.** ZR 2019, GLS 2021, LLG 2022 and MAdaSub 2024 prove ergodicity or variance comparisons only, with no
  discovery guarantee.

---

## 7. What fails and why

- **Applying ZYVR Thm 1 or Chang–Zhou Thm 1/4 to the paper's target on LH or the study.** Fails: R > M is false (exact at
  n ≤ 1,600 on LH; OB in p ≫ n). This route to "rapid mixing of v3's kernels" is closed.
- **WSH as a lower bound for v3 on LH.** Fails: there is no second metastable mode (§3.2). WSH could bite only on a family
  whose *target* has a competing mode, perhaps the study's dilution or T37-type near-ties. Not pursued (scope).
- **Mathews–Schmidler as a positive theorem for v3 in the masked regime.** It gives N ∝ 1/µ⋆ ≈ n^{c/2}, polynomial, so in
  principle it is usable. But it needs local mixing within each partition element at every bridge level, which nobody
  has checked for binary-space kernels. Its proofs are for continuous log-concave mixtures. Not a shortcut.
- **Using Gamarnik–Zadik's OGP to say n = 200 is "hard".** Fails: the constants are unspecified, and the study sits at
  n/(s₀ log p) ≈ 2. Also 0 search misses were observed.

## 8. Needs escalation

1. **OB(ii)–(iii).** The determinant and residual approximations, uniformity in e, and the swap-neighbour control. It
   needs a careful proof or, better, a numerical check at moderate p (e.g. p = 200–500 by scoring only γ_{e*} and its
   neighbours, which is cheap, then comparing with M). I did not run this, to stay within budget.
2. **The no-separation claim L2** should be checked by a second literature search, ideally by another model family. Two
   targets: (a) any 2024–2026 lower bound for add/delete/swap under correlated designs (my searches found none); (b) any
   SMC/PT result on binary spaces in the Schweizer 2012 / Marion–Mathews–Schmidler line.
3. **Theorem numbers and constants** for YWJ and ZYVR are from arXiv versions, not the journal versions.

## 9. Outside scope

- The flattest direction at n = 200 on M(K) is the **saturated model** (rz_lh, both c). This is YWJ A.2's trap
  structure. With cap K = ⌊n/2⌋ and p ≫ n it is excluded, but any future low-p regime-L theory (p ≤ 30 at n = 200, where
  K = p) should check it.
- Kim–Ročková's CART lower bound suggests a test. A *population-level* isolated signal is impossible in linear
  regression with RE, so any BVS slow-mixing family must come from overfitted traps or finite-n noise. This may be
  useful if a referee asks "why not a masked family where MCMC fails?".

## 10. Confidence card

| Target | Refined statement (this run) | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| T38 (Thm 5), masked parts on LH | Novel for the paper's target and method. A corollary of YWJ/ZYVR/Chang–Zhou under *their* prior (API-POS) | high | n/a (literature position) | OB: their hypotheses fail for our prior | no |
| L2 (no published BVS tempering separation) | as stated | medium | OPEN (needs exhaustive search) | unread 2024–26 work | no |
| Prop. OB | R/M → 0 for the paper's prior when p ≫ √n | medium-high | yes, about 1–2 pages | uniform residual approximation; swap neighbours | no |
| G1 (discovery from (1b)/(1c) alone, our prior) | an MH or greedy chain scores S₀ in poly time without (1a) | medium | medium (greedy: done on LH by GU/T38(b1); MH chain: open) | supersets of S₀ never drained without (1a); scoring needs only Hamming-1 neighbours | no |
