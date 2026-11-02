# LIT-SMC — REPORT: the SMC-sampler literature against our evidence, stage-count and discovery results

Run of 2026-11-02, branch `theory/LIT-SMC` (Opus 5.5). This is a literature task. Status words follow `PROTOCOL.md`, and
there is **no new mathematics** here. Each literature claim below cites the file or URL I actually read and quotes its key
statement. Anything I saw only second-hand is marked **UNVERIFIED**. Working quotes are in `NOTES.md`.

Our-side IDs follow `W8-SYNTH · BRIEF.md/SYNTHESIS.md`, `T38-RECORD · T38_STATEMENT.md`, `F-REFINE · ARCHITECTURE.md`,
`O-STAGES · REPORT.md`, `API-POS · REPORT.md` and `O-PW2` (as summarised in SYNTHESIS §4).

## 0. Headline

1. **Threat: O-STAGES Theorem G(i) is already in the literature.** It says the greedy ESS grid is the shortest valid grid.
   Štefankovič–Vempala–Vigoda (SVV; arXiv cs/0612058, J. ACM 2009) define a "B-Chebyshev cooling schedule" by
   Z(2β_{i+1}−β_i)Z(β_i)/Z(β_{i+1})² ≤ B. That is exactly our step rule exp Φ(u,v) ≤ 10/9 with w = 2v − u. They state
   that "the optimal Chebyshev cooling schedule can be obtained in a greedy manner", and they justify it by the convexity
   of ln Z, which is our Lemma 1 argument. Lemma 0 (Φ = Rényi-2 = the log Chebyshev ratio) is also there implicitly. The
   paper must cite SVV and present G(i) as known. G(ii), the pilot-refinement sandwich, is a routine v3-specific
   extension.
2. **Threat: the dense-schedule part of O-STAGES (item 4: √c·T* → L = ∫ sd_{q_φ}(d)dφ) is the "global barrier" Λ.** This
   is Syed–Bouchard-Côté–Chern–Doucet (arXiv:2408.12057). With MCMC kernels on the geometric path, their local barrier is
   λ(β) = sd_{π_β}(V), and lim T·Var[Ẑ/Z] = E(φ)/N ≥ Λ²/N. Present item 4 as a corollary or analogue, not as new.
   **Theorem M** (masked crossing T* = log₂A₀ + O(1)) and **Theorem F**/T* = O(1) in the favourable regime were not
   found in anything I read. They look new as BVS-specific statements, but they are elementary given SVV.
3. **Threat: two pieces of Prop 2 (T12 + T31(i)) are standard.** Frozen-run unbiasedness, together with the advice to
   freeze an adaptive run, is in Dai–Heng–Jacob–Whiteley 2022. The one-sided bound "0.05·Ẑ is a 95% lower bound" is
   Markov's inequality, as used in Grosse–Ghahramani–Adams 2015. The genuinely non-standard items in Prop 2 are the
   negative ones: pooled × pooled is not an identity, and E[Ẑ | completed] ≠ Z. The second is consistent with Dai et
   al.'s warning that adaptation "may not preserve the unbiasedness".
4. **Gap: nobody proves discovery.** In everything I read, no SMC theorem addresses whether the run *scores* a given state,
   or whether the reported best-scored model is correct. The general finite-sample theory (Marion–Mathews–Schmidler 2023;
   Mathews–Schmidler 2024; Le Fay–Chopin–Vihola 2026; Paulin–Jasra–Thiery 2019) needs two things: bounded successive χ²
   or weight ratios, and mixing times. The multimodal versions also need every mode to keep non-negligible mass along
   the whole path (μ⋆ bounded below).
   - Our masked regime is exactly a violation of that premise: π₀(S₀) ≈ e^{−A₀}.
   - It is what Woodard–Schmidler–Huber (EJP 2009) call *low persistence*. They prove that low persistence plus low
     conductance near β = 1 makes tempering torpid.
   - On LH the second ingredient is absent: S₀ is the unique local mode (API-POS). That gives a clean literature
     framing for W7-SEP's "moving off the start is needed, not tempering".
   - Thm 4 (T21), T38 (a)/(b1)/(b1′)/(b2) and the masked-regime Ẑ results (F-MASKPIP M1–M3) are therefore outside
     the existing SMC theory, not implied by it.
5. **Threat to the significance of discovery on LH (already raised by API-POS).** Yang–Wainwright–Jordan's Lemma 4 builds
   a Hamming-progress map G with π(γ)/π(G(γ)) ≤ p^{−2} (overfitted) or ≤ p^{−3} (underfitted) for all γ ≠ γ* in the
   truncated space. That is the same structure as Thm 3-A (greedy repair) and Lemma M. Under YWJ's prior and truncation,
   any single-flip hill-climb from any centre therefore reaches γ*. Our LS0 route is new only because our target (g = n,
   cap K = ⌊n/2⌋, exact-Gram LH) lies outside YWJ's stated hypotheses, which is a formal gap, not a substantive one
   (API-POS §1.3).

## 1. Annotated table

Legend for the "Our designs?" column:
- **LH** = linked-hub family, exact Gram;
- **ST** = the study designs: n = 200, p ∈ {500, 1000}, S1–S6, groups of 5, B = 14, dilution-masked start (6–12 of 14
  truths missing).

Relation to ours: **O** = overlaps, **I** = implies ours (a threat), **C** = complementary, **Ø** = no contact.

### 1A. Normalising constant: unbiasedness, variance, non-asymptotic bounds

| # | Work | Venue/year | What is PROVED (exact, with conditions) | Our designs? | Relation to ours |
|---|---|---|---|---|---|
| 1 | Del Moral, Doucet, Jasra, "Sequential Monte Carlo samplers" | JRSSB 68 (2006) 411–436 [local PDF read] | Prop 1: optimal backward kernels. Prop 2: a CLT for SMC-sampler estimates "under the weak integrability conditions" of Chopin (2004) / Del Moral (2004), for the no-resampling and resample-every-step cases. ESS-triggered resampling is introduced as practice. Unbiasedness of Ẑ is classical (Del Moral 2004 book, **UNVERIFIED**, not read). | Integrability holds trivially on a finite space. These are N → ∞ results at fixed data. | **C/O** with Prop 2 (a): the unbiasedness behind T12 is classical. The CLT is a fixed-data, N → ∞ statement; T26 is n-indexed. |
| 2 | Cérou, Del Moral, Guyader, "A nonasymptotic theorem for unnormalized Feynman–Kac particle models" | AIHP 47(3) (2011) 629–649 [numdam PDF read] | Thm 1.5: if G(x) ≤ δG(x′) for all x, x′ and M^m(x,·) ≤ βM^m(x′,·), then for N > (n+1)βδ^m, E[(γ_n^N(1) − γ_n(1))²] ≤ γ_n(1)²·4(n+1)βδ^m/N. That is, relative variance is linear in the number of steps. Thm 1.4 gives an explicit variance decomposition for α = 0. | **No** for ST/LH. For tempering on {0,1}^p, G = e^{Δφ·d(S)}, so δ = exp(Δφ·range d) and range d = O(n). The uniform minorisation M^m(x,·) ≤ βM^m(x′,·) across modes fails in the masked regime. | **C** to O-PW2. O-PW2 Theorem A ("exact variance identity, no mixing assumption") should be checked against CDG's Thm 1.4 decomposition, because it may be a special case. Not checked: **needs escalation**. |
| 3 | Whiteley, Lee, Heine, "On the role of interaction in SMC algorithms" | Bernoulli 22(1) (2016) 494–529 [arXiv:1309.2918 read: abstract and §1] | αSMC framework. Gives "conditions which ensure unbiased approximation of marginal likelihoods", with time-uniform convergence under ESS control. Proves time-uniform convergence of the adaptive-resampling particle filter. Per Dai et al. 2022: "when the path is fixed, adaptively resampling whenever the ESS falls below a threshold does not alter unbiasedness (Whiteley et al. 2016)". | Fixed path holds in v3's final runs (frozen grid). | **I** for the frozen-run unbiasedness in T12 when resampling is adaptive. |
| 4 | Dai, Heng, Jacob, Whiteley, "An invitation to SMC samplers" | JASA 117(539):1587–1600 (2022), doi:10.1080/01621459.2022.2087659 [arXiv:2007.11936 read] | (i) Ẑ is "an unbiased and consistent normalizing constant estimator". (ii) Adaptive tuning "may not preserve the unbiasedness property … one can run an adaptive SMCS, record the obtained tuning parameters and run a second, non-adaptive sampler". (iii) Bisection for the ESS-based λ_t, because ρ̂_t(λ_t) "is strictly decreasing (Beskos et al. 2016, Lemma 3.1)". (iv) Under perfect kernels (their Assumption 3.1), Var[Z^N/Z] = Π_t(1 + χ²(π_t\|π_{t−1})/N) − 1. (v) Averaging R independent runs is unbiased. | (ii) is exactly v3's pilot/calibration → frozen final run. (iv) holds only under perfect mixing, false in the masked regime. | **I** for T12 frozen-run unbiasedness and islandwise averaging (Prop 2 (a)). **O** with O-PW2 (iv is the idealised version of PW2). |
| 5 | Grosse, Ghahramani, Adams, "Sandwiching the marginal likelihood using bidirectional Monte Carlo" | arXiv:1511.02543 (2015) [read §"Obtaining stochastic lower bounds"] | "because ML estimators are nonnegative estimators of a nonnegative quantity, Markov's inequality implies that Pr(Ẑ > aZ) < 1/a". Hence Pr(log Ẑ > log Z + b) < e^{−b}. | Holds for any unbiased Ẑ ≥ 0, so for v3's frozen run. | **I**: the "0.05Ẑ is a one-sided 95% lower bound" in Prop 2 / T31(i) is this with a = 20. It is standard; cite it. |
| 6 | Vergé, Dubarry, Del Moral, Moulines, "On parallel implementation of SMC methods: the island particle model" | Stat. Comput. 25(2):243–260 (2015; online 2013), doi:10.1007/s11222-013-9429-x [arXiv:1306.3911 read: abstract, statements] | Islands of sub-populations form a Feynman–Kac model at the island level. LLN/CLT (Thms 1–9) for interacting and non-interacting islands. Unbiasedness of the island-level unnormalised estimator (proof §, eq. (62)). | Applies to v3 islands, since R independent islands is the non-interacting case. | **O** with Prop 2's islandwise identities. Those are the non-interacting special case and standard. "Pooled × pooled ≠ identity" was not found stated. It is elementary but useful. |
| 7 | Lee & Whiteley, "Variance estimation in the particle filter" | Biometrika 105(3):609–625 (2018), doi:10.1093/biomet/asy028 [local PDF; index only, not read in depth] | Unbiased estimator of Var(Ẑ) from one run (**statement not verified here; UNVERIFIED**). | Would apply to frozen runs. | **C**: it could make the O-PW2 bound data-computable per fit. |
| 8 | Le Fay, Chopin, Vihola, "On the complexity of standard and waste-free SMC samplers" | arXiv:2604.03352v2 (Apr 2026) [local PDF read] | Recalls MMS (Thm 2.3): if K_t leaves π_{t−1} invariant, 1+χ²(π_t\|π_{t−1}) ≤ χ̄², M ≥ log(8Tη^{−2})·max(18χ̄², ε^{−2}/2) and P ≥ τ(η/(2MT), 2), then Pr(\|π̂(f) − π(f)\| < ε) ≥ 1 − η. Adds waste-free analogues (Thm 3.2) and tempering with T = Θ(d^{1/2}) for log-concave targets (Thm 5.2). Claims "no finite-sample complexity bounds for normalising constants have previously been derived within the SMC literature" and gives Õ(d²ε^{−2}) for MALA/tempering (Thm 6.2). | χ² condition: v3's ESS ≥ 0.9 gives 1+χ² ≤ 10/9 **on the candidate set V** (a COVER statement, not on Ω). Mixing-time premise: unknown for v3 kernels; on LH, API-POS suggests rapid mixing of the target, but not of v3's specific kernels. | **C**: the best general template for a finite-N Ẑ bound. Plugging in is blocked by mixing times. |

### 1B. Adaptive tempering, ESS schedules, stage counts

| # | Work | Venue/year | What is PROVED | Our designs? | Relation to ours |
|---|---|---|---|---|---|
| 9 | Štefankovič, Vempala, Vigoda, "Adaptive simulated annealing: a near-optimal connection between sampling and counting" | arXiv cs/0612058 (2006); FOCS'07 183–193; J. ACM 56(3):1–36 (2009), doi:10.1145/1516512.1516520 (journal version not read) [arXiv PDF read] | Def 2.3, the B-Chebyshev schedule: Z(2β_{i+1}−β_i)Z(β_i)/Z(β_{i+1})² ≤ B. Cor 2.4: such a schedule of length ℓ gives (1±ε)Z w.p. ≥ 3/4 with 16Bℓ²/ε² perfect samples. Thm 4.1: an e²-Chebyshev schedule of length O(√(ln A)·ln n·ln ln A) exists (A = Z(0)). Lemma 4.7: Z = (1+e^{−β})^n needs ≥ √(n/(20 ln B)) steps. Non-adaptive schedules need Ω(ln A). Text after Thm 4.1: "The optimal Chebyshev cooling schedule can be obtained in a greedy manner … if we can step from β to β′, then for any γ ∈ [β, β′] we can step from γ to β′ … follows from the convexity of f." | Purely deterministic (population) statements, so they apply verbatim to v3's population grid (V = Ω) and to any finite V. | **I** for O-STAGES Theorem G(i), Lemma 1(b)(c) and Lemma 0. **C** for Theorem M (instance-specific, B = 10/9) and Theorem F. |
| 10 | Schäfer & Chopin, "SMC on large binary sampling spaces" | Stat. Comput. 23(2):163–184 (2013), doi:10.1007/s11222-011-9299-z [local PDF read] | Methodology, with no theorem on schedule, consistency or HPM. §4.3: "We pick a step length α such that the effective sample size η(α) equals a fixed value η* … Since η is continuous and monotonously increasing in α, we solve … using bi-sectional search". Experiments use η* = 0.9 and BVS examples. | It *is* the ancestor of v3's grid rule (ESS 0.9, bisection). | **O**: v3's grid rule is theirs. All our stage-count, discovery and HPM theory is beyond it. |
| 11 | Beskos, Jasra, Kantas, Thiery, "On the convergence of adaptive SMC methods" | AAP 26(2):1111–1146 (2016), doi:10.1214/15-AAP1113 [arXiv:1306.6462 read: abstract, lemma] | WLLN and CLT for adaptive SMC. The asymptotic variance is "identical to a so-called 'perfect' SMC algorithm" with ideal kernels. Lemma: "λ ↦ ESS(η, e^{−λV}) is continuous and decreasing on [0, ∞)", and strictly decreasing under a non-degeneracy condition. | N → ∞ at fixed data. Monotonicity is in the forward endpoint only. | **O** with O-STAGES Lemma 1 (forward half). **C** with T26: it supplies N → ∞ consistency of the adaptive pilot, not our n-asymptotics. |
| 12 | Beskos, Crisan, Jasra, "On the stability of SMC methods in high dimensions" | AAP 24(4):1396–1445 (2014), doi:10.1214/13-AAP951 [arXiv:1103.3965 read: abstract] | For i.i.d.-product targets on R^d, with O(d) tempering steps and fixed N, the ESS converges to a non-degenerate random variable, at cost ∝ Nd². | Product structure fails for BVS posteriors. | **C**: the "T must grow with dimension" baseline. Our favourable-regime T* = O(1) (O-STAGES/Theorem F) contrasts with it, because the start is already close to the posterior. |
| 13 | Giraud & Del Moral, "Nonasymptotic analysis of adaptive and annealed Feynman–Kac particle models" | Bernoulli 23(1) (2017) 670–709 [arXiv:1209.5654 read: abstract, Thm 1] | Thm 1: uniform-in-time concentration if sup_p g_p ≤ M and sup_p b_p ≤ a/(M(1+a)), where g_p are potential oscillations and b_p Dobrushin coefficients. Adaptive models: "an open research problem"; they treat a simplified adaptive model. | Dobrushin contraction fails for local moves on {0,1}^p at the masked mode. | **C**. |
| 14 | Marion, Mathews, Schmidler, "Finite sample bounds for SMC and adaptive path selection using the L2 norm" | arXiv:1807.01346v3 (2025) [read: abstract, Thms 1–2] | Thm 1: if ‖μ_s/μ_{s−1}‖²_{L²(μ_{s−1})} ≤ E^{−1} and the mixing times are τ_s, then N, t as displayed give an ε-accurate estimate w.p. ≥ 3/4. Thm 2: the adaptive relative-ESS step selection gives a randomized approximation scheme under AS3–AS5. They show standard data tempering fails these conditions. | The L²/χ² condition is v3's ESS rule (on V). Mixing times: unknown. | **O** with O-STAGES/T13 (COVER): the closest published justification of ESS-adaptive grids. **C** to T26. |
| 15 | Syed, Bouchard-Côté, Chern, Doucet, "Optimised annealed SMC samplers" | arXiv:2408.12057v2 (Dec 2025) [local PDF read] | Under a "performance model" (Assumptions 1–4: integrability; temporal and particle independence; "efficient local exploration"; the authors say they are "not expected to hold exactly in practice"): Thm 1(a), Var[Ẑ/Z] = Π_r(1 + (e^{D(B_T,τ_{r−1},τ_r)} − 1)/N) − 1 with D the Rényi-2 discrepancy. Thm 3: lim_T T·Var[Ẑ/Z] = E(φ)/N ≥ Λ²/N with Λ = ∫λ, the global barrier. For MCMC kernels on the linear path, δ(β) = Var_β[V], so λ = sd_β(V). | The idealisation is off in the masked regime, where local exploration is not efficient. | **I/O** for O-STAGES item 4 (√c·T* → L = Λ) and Lemma 0 (Φ = D₂). **O** with O-PW2 (Thm 1(a) is a PW2-type product formula under idealisation; consistent with O-WSTAB's "PW2 under IID idealisation PROVED"). |
| 16 | Chopin, Crucinio, Korba, "A connection between tempering and entropic mirror descent" | arXiv:2310.11914v3 (venue ICML 2024: UNVERIFIED) [read: abstract, Props] | Tempering iterates = entropic mirror descent on KL(·\|π). Convergence rates for the tempering iterates (Prop 1). Adaptive step rules derived (Prop 2 recipe). | Population-level. | **C** (an alternative to the ESS rule; no stage-count overlap). |

### 1C. Multimodality, mixing, discovery

| # | Work | Venue/year | What is PROVED | Our designs? | Relation to ours |
|---|---|---|---|---|---|
| 17 | Marion, Mathews, Schmidler, "Finite sample complexity of SMC estimators" | AoS 51(3):1357–1375 (2023), doi:10.1214/23-AOS2295 [arXiv:1803.09365v3 read: Thm 1, §5.3.1] | Thm 1: if sup w_s ≤ W, z_{s−1}/z_s ≤ Z, N ≥ ½·log(128S)·max(9W²Z², ε^{−2}) and t ≥ max_s τ_s(1/(8NS), 2), then \|f̂ − π(f)\| ≤ ε w.p. ≥ 3/4. §5.3.1 (finite spaces): an O*(ρ^{−1}·ε^{−2}·log(1/π₀)·log log(1/π₀)) bound, with ρ the spectral gap. | The bounded-weight W fails (d ranges over O(n)). The spectral gap of v3 kernels is unknown. Within a factor log of MCMC, it cannot beat a slow chain. | **C** to T26/T38(c). |
| 18 | Mathews & Schmidler, "Finite sample complexity of SMC estimators on multimodal target distributions" | AAP 34(1B):1199–1223 (2024), doi:10.1214/23-AAP1989 [arXiv:2208.06672 read: A1, Thm 1 setup] | Bounds that need only **local** mixing within a partition {A_j}. Assumption A1 bounds density ratios. The bound depends on μ⋆ := min_v min_j μ_v(A_j), and its application assumes μ⋆ decays at most polynomially. SMC can be an FPRAS where MCMC is exponentially slow. | **Masked regime violates μ⋆**: the S₀-basin has start mass ≈ π₀(S₀) = e^{−A₀}. On LH, A₀ = c log p + (c/2) log n, so μ⋆ is polynomially small: borderline, not excluded. In ST (dilution) it is far smaller. | **C**, and the key positioning: the literature handles multimodality only when every mode is visible throughout the path. Our masked results (T38 b-routes, W7-SEP) live where that fails. |
| 19 | Paulin, Jasra, Thiery, "Error bounds for SMC samplers for multimodal distributions" | Bernoulli 25(1):310–340 (2019), doi:10.3150/17-BEJ988 [arXiv:1509.08775 read: abstract, Thms 3.1–3.3] | Asymptotic-variance bounds under global mixing (Thm 3.1) and multimodal mixing (Thm 3.2, Γ_g < ∞ the density-ratio constant). "Interpolation to independence" gives polynomial cost on the Potts model. | Γ_g is a sup-ratio, hence huge here. | **C**. |
| 20 | Woodard, Schmidler, Huber, "Sufficient conditions for torpid mixing of parallel and simulated tempering" | EJP 14 (2009) 780–804 [EMIS PDF read: §1, §3] | Persistence γ(A, β) = min{1, π_β[A]/π[A]}. A set with low conductance at β ≈ 1 and small persistence "guarantees tempering will mix slowly for any choice of temperatures" (Thm 3.1, Cor 3.1). Undetectable by swap-rate diagnostics. | Our masking *is* low persistence of {S₀} under the start bridge. On LH the low-conductance ingredient is absent (S₀ unique local mode, API-POS). In ST it is unknown. | **C, framing**: a published mechanism matching W7-SEP SEP(A) (start-only discovery fails) and O-STAGES Theorem M (log₂A₀ stages for the crossing). It also explains why moves fix LH but might not fix ST. |
| 21 | Yang, Wainwright, Jordan, "On the computational complexity of high-dimensional Bayesian variable selection" | AoS 44(6):2497–2532 (2016), doi:10.1214/15-AOS1417 [arXiv:1505.07925v1 read: Thm 2, Lemmas 1, 4] | Thm 2: under Assumptions A–D (with truncation s₀ ≲ n/log p), the add/delete/swap MH mixing time is ≤ c₁ps₀²(c₂α(n+s₀)log p + log(1/ε) + 2) w.p. ≥ 1 − 4p^{−c₁}. Lemma 4: for all γ ≠ γ*, π(γ)/π(G(γ)) ≤ p^{−2} (overfitted) or ≤ p^{−3} (underfitted), with G a Hamming-progress map (Lemma 1). | Already audited by API-POS. With YWJ's priors LH qualifies (PROOF SKETCH there). With our g = n and K = ⌊n/2⌋ it does not, formally. | **O/I-in-spirit** with Thm 3-A, Lemma M, LH-LAT and T38(b1). Unimodality along Hamming-progress paths is YWJ's mechanism. See threats §3. |
| 22 | Zhou, Yang, Vats, Roberts, Rosenthal, "Dimension-free mixing for high-dimensional BVS" | JRSSB 84(5) (2022) [local PDF; via API-POS's audit, not re-read] | Informed MH mixes in O(n) iterations under Condition 1 (per API-POS). | As in API-POS. | Same as #21. |

### 1D. Divide-and-conquer / local-to-global

| # | Work | Venue/year | What is PROVED | Our designs? | Relation |
|---|---|---|---|---|---|
| 23 | Lindsten, Johansen, Naesseth, Kirkpatrick, Schön, Aston, Bouchard-Côté, "Divide-and-Conquer with SMC" | JCGS 26(2):445–458 (2017), doi:10.1080/10618600.2016.1237363 [arXiv:1406.4993 read: abstract] | Method: tree-structured sub-problems, merging independent populations. Unbiased Ẑ and consistency (proofs in their paper/supplement; **statements not verified here**). | v3's composite start (blocks → tables → max-plus convolution π₀) is a deterministic local-to-global start, not population merging. | **C**: the closest methodological relative of the block start. No overlap with our theorems. |
| 24 | Kuntz, Crucinio, Johansen, "The divide-and-conquer SMC algorithm: theoretical properties and limit theorems" | AAP 34(1B):1469–1523 (2024), doi:10.1214/23-AAP1996 [arXiv:2110.15782v2 read: abstract] | LLN, L^p inequalities, CLTs for DaC-SMC. Bias of normalised estimates characterised. Unnormalised estimates unbiased (their Thm 3). | As #23. | **C**. |

## 2. Gaps: what nobody has proved that we prove or could prove

G1. **Discovery / "the run scores the truth".** No SMC paper I read treats the event {S₀ ∈ 𝒮} or the best-scored output Ŝ.
   The finite-sample theory (#8, #14, #17–19) controls π̂(f) or Ẑ, and does so only through mixing times. Thm 4 (T21, the
   exact decomposition 2E₀δ₁ + P(never score S₀)), T38 (0), (a), (b1), (b1′), (b2), Theorem B (Gibbs-path repair) and
   W7-SEP are outside that literature. YWJ's split ("posterior concentration need not imply rapid mixing") is the
   nearest conceptual analogue. Theirs is about mixing time; ours is about one hitting event, plus a deterministic
   output rule.
G2. **Masked start = low persistence, with an exact cost.** WSH (#20) give a qualitative torpidity criterion for MCMC
   tempering. Mathews–Schmidler (#18) assume masking away (μ⋆). We prove three things there:
   - a quantitative separation: iid start draws need Q* = p^c n^{c/2} (W7-SEP SEP(A), A-REV9 VERIFIED);
   - an exact stage cost for the crossing, log₂A₀ + O(1) (O-STAGES Theorem M);
   - that moves off the start repair it on LH.
   None of these is in the literature I read.
G3. **n-indexed (statistical) consistency of Ẑ and PIPs.** Every Ẑ result in the literature is N → ∞ at fixed data, or a
   finite-N bound via mixing times. T26/Thm 6, with (P1): (T_n+1)Δ_n → 0, ties accuracy to posterior concentration
   instead. That is a different premise, and I found no analogue. F-MASKPIP M1–M3 (one-sided masked statements) sit
   where the general bounds are vacuous.
G4. **Stage counts in the favourable regime, T* = O(1).** The general results say T grows with dimension: Θ(d^{1/2}) in #8,
   O(d) in #12, √ln A in #9. O-STAGES's favourable sandwich (Theorem F, through q_w(S₀), w ∈ [1, 2]) is BVS-specific
   and new as far as I can tell. The underlying identity (Lemma 0) is not new (#9, #15).
G5. **A posteriori certificates with guarantees.** I found no SMC certificate of the O-VCERT kind (C1–C6: Lemma M
   monotone bounds, box certificates, posterior-miss certificates). BDMC (#5) gives stochastic sandwich bounds on log Z,
   but needs exact posterior samples for the upper side, which is unavailable for real data. Our certificates look novel
   in kind. Caveat: I did not search the stochastic-search/BVS certificate literature (for example Hans–Dobra–West
   2007), which is outside the SMC scope.

## 3. Threats: results that make one of ours standard, weaker, or redundant

T1. **O-STAGES Theorem G(i) + Lemma 1 = SVV (#9).** Same object, same proof idea. *Action:* cite SVV. Keep G(ii) (the
   pilot-refinement sandwich) and the COVER transfer G(iii) as v3-specific. Lemma 1's forward half is also in Beskos et al.
   2016 (#11), and Schäfer–Chopin (#10) assert it.
T2. **O-STAGES item 4 (dense limit √c·T* → L) = Syed et al.'s global barrier Λ (#15),** with λ = sd_β(V). *Action:* present
   it as a known analogue. Our observation that L does not determine T_n at the production c (two-state family: L ≤ π
   while T* → ∞) is a useful complement. Syed's own analysis is a dense-limit, idealised one.
T3. **Prop 2 / T12 / T31(i).** Frozen-run unbiasedness is standard: classical, plus Dai et al.'s two-pass recipe (#4) and
   Whiteley et al. (#3). The 0.05·Ẑ Markov lower bound is standard (#5). Islandwise averaging is standard (#4, #6).
   *Action:* present these as known. The contribution is the bookkeeping for v3's actual run (strict 𝒪, GUARD) and the
   negative results.
T4. **O-PW2.**
   - Theorem A (exact variance identity) may be a special case of the Feynman–Kac variance decompositions (CDG 2011
     Thm 1.4 #2; coalescent-tree expansions). Not checked.
   - Under idealisation, PW2-type product formulas are in Dai et al. (#4) and Syed et al. (#15, Thm 1(a)).
   - Theorem B (two-sided non-asymptotic) is plausibly closest to CDG Thm 1.5, but with different premises.
   *Action:* **escalate** a line-by-line comparison.
T5. **Discovery on LH is unsurprising given YWJ/ZYVR (#21–22).** API-POS already concluded: "polynomial-time recovery of S₀
   on LH is not new" (with their priors), and the gap for our target is formal. My extra observation: YWJ Lemma 4 *is*
   a greedy-repair statement (a Hamming-progress neighbour with a posterior gain ≥ p²). So Thm 3-A/TD′ and Lemma M are
   close analogues of YWJ's canonical-path lemma; the difference is that ours are deterministic and exact at finite n.
   *Action:* cite YWJ Lemma 4 next to Thm 3-A. Present T38(b1) on LH as "the SMC-BVS output inherits the unimodality
   that rapid-mixing proofs use", not as a new phenomenon.
T6. **Schäfer–Chopin (#10)** already ran ESS-0.9 adaptive SMC on BVS. Every methodological novelty claim about the grid
   rule must be dropped. The novelty is in the start, the HPM ledger, LS0 and the theory.

## 4. What fails and why (routes I tried)

- *Plugging our designs into the general finite-sample theorems* (#8, #14, #17) fails at the mixing-time premise and, for
  #17 and CDG, at bounded weight ratios: e^{Δφ·range d}, range d = O(n). On ST, the dilution-masked start also breaks
  μ⋆ (#18). None of these theorems gives a non-vacuous statement at n = 200, which is consistent with O-PW2's "valid but
  vacuous at study scale".
- *Searching for a 2023–2026 SMC-for-BVS theory paper*: two web searches found none. The recent theory (#8, #14, #15, #18)
  is general SMC. Absence of evidence: I did not do an exhaustive search.

## 5. Needs escalation

1. **O-PW2 versus Cérou–Del Moral–Guyader 2011 (Thm 1.4/1.5) and Del Moral's coalescent-tree variance formulas**: is
   O-PW2 Theorem A a special case? This needs someone to read CDG §1–3 and O-PW2 line by line.
2. **SVV Theorem 4.1 applied to v3's population grid.** It would give an *upper* bound T* = O(√(ln A)·…) with B = e²; our
   B is 10/9. Check whether SVV's proof gives a B-dependent constant that recovers or improves O-STAGES's
   T* ≤ T_e = O(log²(n+p)), or Theorem M's log₂A₀. Note: for the two-state family, ln A ≈ A₀, so SVV's √A₀ upper bound
   is *weaker* than Theorem M's log₂A₀. That is consistent, not a contradiction.
3. **Journal versions.** Theorem numbers above are from the arXiv versions read (SVV 2006 v1; YWJ v1; MMS v3). Check them
   against the published versions before citing in the paper.

## 6. Outside scope

- Le Fay–Chopin–Vihola's waste-free complexity results (#8, Thm 3.2) could bear on v3's cost theorem T32/T38(c) if v3's
  final rounds are read as waste-free style. I did not pursue this.
- BDMC (#5) could give a *two-sided* Ẑ check on simulated data, where exact posterior draws are obtainable by
  enumeration at small p. That could serve as a validation experiment for Prop 2/Thm 6.

## 7. Confidence card

| Our target | Refined literature statement | Conf. it is true | Conf. it is cheap to settle | Crux | Method change? |
|---|---|---|---|---|---|
| O-STAGES Theorem G(i), Lemma 0/1 | Known (SVV 2009; Beskos et al. 2016 for monotonicity) | high | high (cite) | none | no |
| O-STAGES item 4 (dense limit) | Known analogue (Syed et al. Λ) | high | high | idealised versus exact | no |
| O-STAGES Theorem M, Theorem F | Not found in the literature read: plausibly new, elementary | medium | medium (needs a wider search in the counting/annealing literature) | SVV-style examples | no |
| Prop 2 / T12 / T31(i) | Standard (unbiasedness, two-pass, Markov) except the negative items | high | high | none | no |
| O-PW2 Thm A/B | Possibly a special case of Feynman–Kac variance formulas | low–medium (that it is subsumed) | medium | CDG Thm 1.4 comparison | no |
| T21 / T38 discovery, Theorem B, W7-SEP | No SMC literature overlap. Closest: YWJ Lemma 4 (structure), WSH persistence (mechanism) | high (that it is a gap) | — | — | no |
| T26 / Thm 6 n-indexed Ẑ | No analogue found | medium–high | — | — | no |
| Masked-regime Ẑ (F-MASKPIP) | Outside all general bounds (μ⋆, mixing) | high | — | — | no |
| Certificates (O-VCERT) | No SMC analogue found. BDMC is the nearest | medium | low (the BVS stochastic-search literature was not searched) | — | no |

## 8. Sources actually read

Local (pdftotext, targeted sections):
- `Papers/SMC/Del_Moral_Doucet_Jasra_2006_Sequential_Monte_Carlo_samplers.pdf`
- `Papers/Core_bibliography/07_2013_Schafer_Chopin_…pdf`
- `…/02_2026_Syed_et_al_Optimized_annealed_…pdf`
- `…/24_2026_Le_Fay_Chopin_Vihola_…pdf`

Downloaded to /tmp (arXiv/HAL/EMIS PDFs, targeted sections):
- https://arxiv.org/pdf/cs/0612058 (SVV)
- https://arxiv.org/pdf/1803.09365 (MMS 2023)
- https://arxiv.org/pdf/2208.06672 (Mathews–Schmidler)
- https://arxiv.org/pdf/1807.01346 (MMS L2)
- https://arxiv.org/pdf/1509.08775 (PJT)
- https://arxiv.org/pdf/1306.6462 (BJKT 2016)
- https://arxiv.org/pdf/1103.3965 (BCJ 2014)
- https://arxiv.org/pdf/1209.5654 (Giraud–Del Moral)
- https://arxiv.org/pdf/1309.2918 (WLH)
- https://arxiv.org/pdf/1306.3911 (Vergé et al.)
- https://arxiv.org/pdf/2007.11936 (Dai et al.)
- https://arxiv.org/pdf/1406.4993 (Lindsten et al.)
- https://arxiv.org/pdf/2110.15782 (Kuntz et al.)
- https://arxiv.org/pdf/2310.11914 (CCK)
- https://arxiv.org/pdf/1511.02543 (BDMC)
- https://arxiv.org/pdf/1505.07925 (YWJ)
- http://www.numdam.org/item/10.1214/10-AIHP358.pdf (CDG)
- https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/638/870.pdf (WSH)

Second-hand only (UNVERIFIED):
- Del Moral (2004) book, the classical unbiasedness;
- Lee–Whiteley 2018 statement;
- Lindsten 2017 theorem statements;
- ZYVR (via API-POS);
- ZYVR's venue is taken from API-POS.

**Venue check.** Venues, volumes, pages and DOIs in §1 were checked against the Crossref API (api.crossref.org,
2026-11-02), except:
- DMDJ (from the PDF header);
- WLH and Giraud–Del Moral (from the arXiv headers);
- CDG (from numdam);
- WSH (from the EMIS PDF);
- CCK (venue UNVERIFIED);
- BDMC (arXiv only).

Theorem numbers are from the versions read, and may differ in the journal versions (escalation 3).
