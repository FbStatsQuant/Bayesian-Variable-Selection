# LITGAP: primary-source pass on composite likelihood / diagnostics / importance tempering

Date: 2026-11-03. Scope: 10 verified works (A1-A5, B1-B5 incl. optional, C1; B2/B3/B4 also verified). Nothing UNVERIFIED in the final list.
Method: bibliographic data cross-checked against Crossref (api.crossref.org) and/or the publisher or journal page; quotes taken from the arXiv full text I downloaded and converted with pdftotext (arXiv version numbers given, because equation numbers can differ from the published version). Statements marked [INFERENCE] are mine, not the authors'.
Each quote below was read in the cited text. Quoted equations are transcribed from pdftotext output (symbols may be flattened).

Headline finding (read this first):
1. None of A1-A5 addresses composite posteriors as IS proposals or SMC starts. They concern calibration of the composite posterior as the final answer. Our design (π₀ is only a start, the SMC corrects it exactly) sidesteps their problem, so they are context rather than precedent. A4 (Theorem 2) is the only one that treats an approximate posterior as an IS proposal.
2. B1 (Chatterjee-Diaconis) gives a necessary-and-sufficient sample-size scale exp(KL(π||π₀)) for a one-shot π₀→π correction. This is the right quantity for the "how many particles / why bridge" argument.
3. C1 (Gramacy et al.) is simulated tempering with importance reweighting of all temperatures; it is not an SMC bridge. It supplies one reusable result: the ESS-optimal combination of IS estimators across temperatures (Prop 2.1).

---------------------------------------------------------------------

## A1. Ribatet, Cooley & Davison (2012)
- Citation: M. Ribatet, D. Cooley, A. C. Davison. "Bayesian inference from composite likelihoods, with an application to spatial extremes." Statistica Sinica 22(2) (2012), 813-845. DOI 10.5705/ss.2009.248. Preprint arXiv:0911.5357 (v2, 6 Jul 2011; author order there: Cooley, Davison, Ribatet).
- Verified: web search plus https://www3.stat.sinica.edu.tw/statistica/j22n2/J22N217/J22N217.html (title/authors/vol/pp/DOI); full text read from https://arxiv.org/pdf/0911.5357 (v2).
- Quotes (arXiv v2; numbering may differ in the published version):
  - Abstract: "We establish that using a composite likelihood results in a proper posterior density, though it can differ considerably from that stemming from the full likelihood. Building on previous work on composite likelihood ratio tests, we use asymptotic theory for misspecified models to propose two adjustments to the composite likelihood to obtain appropriate inference."
  - Eq (8), magnitude adjustment: "ℓmagn(θ; y) = k ℓc^tot(θ; y), θ ∈ Θ, where k is a positive constant", with k = p / Σλi, λi the eigenvalues of H(θ0)^-1 J(θ0).
  - Eq (10), curvature adjustment: "ℓcurv(θ; y) = ℓc^tot(θ*; y), θ* = θ̂c + C(θ − θ̂c)".
  - Eq (13)-(14): "πmagn(θ | y) ∼ N(θ0, (np)^-1 tr{H(θ0)^-1 J(θ0)} H(θ0)^-1)" and "πcurv(θ | y) ∼ N(θ0, n^-1 H(θ0)^-1 J(θ0) H(θ0)^-1)" (asymptotic normality; the unadjusted composite posterior has the wrong variance).
  - Sec 2.3: "only the curvature adjustment ensures that the convergence to a χ2 distribution is met; the magnitude adjustment only gets the first moment correct."
  - Sec 1.3: Pauli et al. (2011) "independently suggest the adjustment to the composite likelihood called by us the magnitude adjustment".
- Relevance to us:
  - (i) The magnitude adjustment ℓ_magn = k ℓ_c is a power (tempered) composite posterior. It is the same functional form as one rung of our bridge, π₀^(1−φ)π^φ. Their k is chosen once to fix the posterior width asymptotically; our φ is swept to 1, where the target is exact. [INFERENCE]
  - (ii) The curvature adjustment relies on a Gaussian/regular-parametric asymptotic (H, J matrices). It has no direct analogue on a discrete model space, so it is not transferable to π₀. [INFERENCE]
  - (iii) The paper's finding that unadjusted composite posteriors have the wrong spread is a useful motivation for a correction step. It is a statement about parametric θ, not about model-space posteriors, so cite only as analogy.
  - (iv) No IS-proposal or SMC-start use appears in the paper (it uses Metropolis-Hastings and Gibbs only).

## A2. Pauli, Racugno & Ventura (2011)
- Citation: F. Pauli, W. Racugno, L. Ventura. "Bayesian composite marginal likelihoods." Statistica Sinica 21(1) (2011), 149-164. DOI: not shown on the journal page; I did not look one up (not asserted).
- Verified: https://www3.stat.sinica.edu.tw/statistica/j21n1/J21N16/j21n16.html (title/authors/vol/pp/abstract). Full text NOT read, so no theorem is quoted; the characterization of its content below comes from the abstract and from A1's description of it.
- Quotes (abstract, as shown on the journal page):
  - "This paper proposes and discusses the use of composite marginal likelihoods for Bayesian inference."
  - "The procedure is based on a suitable calibration of the composite likelihood that yields the right asymptotic properties for the posterior probability distribution."
- Relevance: the independent origin of the magnitude adjustment (per A1, Sec 1.3, Pauli et al. also prove asymptotic normality of the adjusted posterior). Same relevance as A1: composite posterior as an end product, not as a proposal.

## A3. Varin, Reid & Firth (2011)
- Citation: C. Varin, N. Reid, D. Firth. "An overview of composite likelihood methods." Statistica Sinica 21(1) (2011), 5-42.
- Verified: https://www3.stat.sinica.edu.tw/statistica/j21n1/J21N11/J21N11.html (title/authors/vol/pp). Full text NOT read; only the abstract line was seen.
- Quote (abstract, as shown): "A survey of recent developments in the theory and application of composite likelihood is provided."
- Relevance: standard reference for the composite likelihood definition and the sandwich (Godambe) variance. I read nothing in it about Bayesian use, so it supports only the "what is a composite likelihood" sentence in a related-work paragraph. Our block-product π₀ is a product over disjoint predictor blocks of exact local posteriors, i.e. a block-independence composite object; the mapping to the standard definition is [INFERENCE] and should be stated carefully in the paper (cross-block dependence is what is dropped).

## A4. Frazier, Nott, Drovandi & Kohn (2023)
- Citation: D. T. Frazier, D. J. Nott, C. Drovandi, R. Kohn. "Bayesian inference using synthetic likelihood: asymptotics and adjustments." J. Amer. Statist. Assoc. 118(544) (2023), 2821-2832. DOI 10.1080/01621459.2022.2086132. arXiv:1902.04827 (v4, 12 Mar 2021).
- Verified: Crossref (title/journal/vol/pp/DOI); full text read from https://arxiv.org/pdf/1902.04827 (v4). (Note: arXiv:1904.04551 is a different paper, Frazier-Drovandi "Robust approximate Bayesian inference with synthetic likelihood"; not used.)
- Quotes (arXiv v4):
  - Abstract: "if the summary statistic satisfies a central limit theorem, then the synthetic likelihood posterior is asymptotically normal and yields credible sets with the correct level of frequentist coverage."
  - Abstract: "compares the computational efficiency of Bayesian synthetic likelihood and approximate Bayesian computation using the acceptance probability for rejection and importance sampling algorithms with a 'good' proposal distribution."
  - Introduction: "We use our asymptotic results to motivate sandwich-type variance adjustments to account for the misspecification and implement these in some examples."
  - Theorem 1 (second part): "For any 0 < γ ≤ 2, if Assumption 4 is satisfied with p ≥ γ + κ, then ∫ ||θ||^γ |π̂(t|Sn) − N{t; 0, W0}| dt = op(1)."
  - Assumption 6(iv), the proposal condition: "for h(θ) = qn(θ)/π(θ), lim sup n→∞ ∫ h²n(θ) π(θ|Sn) dθ < ∞." Remark 5: "Assumption 6 is satisfied if the proposal density qn(θ) is built from vn-consistent estimators of θ0, such as those based on pilot runs."
  - Theorem 2: "If Assumptions 1-6 are satisfied and if ∫k(θ)²π(θ|Sn)dθ < ∞, then for m → ∞ as n → ∞, α̃n = Ξp(1) + Op(1/m)" (the rejection-sampler acceptance probability stays bounded away from 0 and ∞).
- Relevance: the only work in group A that uses an approximate posterior as an IS/rejection proposal with a stated sufficient condition. Assumption 6(iv) is a second-moment condition on proposal/target density ratio, i.e. finite χ² divergence between proposal and posterior. That is the same quantity that controls our ESS (B2/B5). They prove acceptance is non-vanishing asymptotically (parametric, n→∞, Gaussian regime), which is not our discrete-model, finite-n setting. [INFERENCE: use only as an analogy that "the proposal must have a finite χ²-type distance to the target".]

## A5. Syring & Martin (2019)
- Citation: N. Syring, R. Martin. "Calibrating general posterior credible regions." Biometrika 106(2) (2019), 479-486 (Crossref issued date 2018, online first). DOI 10.1093/biomet/asy054. arXiv:1509.00922 (v4, 22 Apr 2018).
- Verified: Crossref (vol/issue/pp/DOI); full text read from https://arxiv.org/pdf/1509.00922 (v4).
- Quotes (arXiv v4):
  - Abstract: "Except in well-specified situations, however, there is no guarantee that such regions will achieve the nominal frequentist coverage probability, even approximately. To overcome this difficulty, we propose a general strategy that introduces an additional scalar tuning parameter to control the posterior spread, and we develop an algorithm that chooses this parameter so that the corresponding credible region achieves the nominal coverage probability."
  - Eq (1): "Πn,ω(dθ) ∝ e^{−ωnRn(θ)} Π(dθ), where Rn(θ) = Pn ℓθ is the empirical version of the risk, ω > 0 is a scale parameter".
  - Calibration condition, eq (3): "cα(ω; P) = 1 − α" (coverage probability function of the region Cω,α, solved for ω by the stochastic-approximation Algorithm 1, eq (4)).
  - Misspecified normal-mean example: "to achieve the desired calibration, one must take ω = σ²/ψ²."
- Relevance: the same power/scale structure as A1's magnitude adjustment. Their ω is selected by bootstrap coverage because the model is misspecified and there is no exact target. We have an exact target at φ=1, so calibration of a scale is unnecessary for the final posterior; there is no theorem in A5 about SMC starts or proposals. Possible use: if a user-facing variant reports the π₀ posterior alone (before the SMC correction) as a cheap approximation, GPC would be the calibration tool. [INFERENCE]

---------------------------------------------------------------------

## B1. Chatterjee & Diaconis (2018)
- Citation: S. Chatterjee, P. Diaconis. "The sample size required in importance sampling." Ann. Appl. Probab. 28(2) (2018), 1099-1135. DOI 10.1214/17-AAP1326. arXiv:1511.01437 (v3, 21 Jun 2017).
- Verified: Crossref (vol/issue/pp/DOI); full text read from https://arxiv.org/pdf/1511.01437 (v3).
- Quotes (arXiv v3):
  - Abstract: "a sample of size approximately exp(D(ν||µ)) is necessary and sufficient for accurate estimation by importance sampling, where D(ν||µ) is the Kullback-Leibler divergence of µ from ν."
  - Theorem 1.1 (setup: target ν, proposal µ, ρ = dν/dµ, L = D(ν||µ) = E log ρ(Y), Y~ν): "If n = exp(L + t) for some t ≥ 0, then E|In(f) − I(f)| ≤ ||f||_L2(ν) (e^{−t/4} + 2 sqrt(P(log ρ(Y) > L + t/2)))." Converse: "If n = exp(L − t) for some t ≥ 0, then for any δ ∈ (0, 1), P(In(1) ≥ 1 − δ) ≤ e^{−t/2} + P(log ρ(Y) ≤ L − t/2)/(1−δ)."
  - Theorem 1.2: the same statement holds for the self-normalized estimate Jn(f) of eq (1.1) ("The conclusion is essentially the same").
  - Theorem 2.1 (a warning about variance diagnostics): "Given any ε > 0, there exists n ≤ ε^{-2} 2^{1+ε^{-3}} such that the following is true. Take any µ and ν as in Theorem 1.1, and any f such that ||f||_L2(ν) ≤ 1. Let vn(f) be defined as above. Then P(vn(f) < ε) ≥ 1 − 4ε." (vn(f) is the estimated variance of In(f).) Text: "any diagnostic criterion that is itself dependent on the accuracy of an estimate obtained by importance sampling, is unlikely to be effective as a measure of the efficacy of importance sampling."
  - Their alternative diagnostic: "Define qn := E(Qn), where Qn := max1≤i≤n ρ(Xi) / Σ_{i=1}^n ρ(Xi). The size of qn is our criterion ... if for some value of n the quantity qn is smaller than some pre-specified threshold (say, 0.01), declare that n is large enough for importance sampling to work."
- Relevance for us:
  - (i) With µ = π₀ and ν = π, a one-shot π₀→π importance step needs N ≈ exp(KL(π||π₀)) particles. A tempering bridge splits log-weight variation into K steps, each with a much smaller KL, which is the standard rationale for SMC over IS; B1 gives the single-step cost to compare against. [INFERENCE for the bridge claim; B1 itself covers only single-step IS.]
  - (ii) If π₀ were exactly the product of the block marginals of π, then KL(π||π₀) is the total correlation (multi-information) between blocks. Our π₀ uses within-block local posteriors, so this is only a heuristic lower-bound picture, not an identity. [My derivation, not in B1.] This links the number of particles to the cross-block dependence, which is what the correlation clustering minimises.
  - (iii) Theorem 2.1 shows that ESS/variance-type diagnostics computed from the same weights can certify too early. Pair ESS with a max-weight ratio (their Qn, equivalently Elvira's 1/max w̄, see B4) and with island agreement. Direction of D matters: D(π||π₀), the target-vs-start direction.
  - (iv) All results are for i.i.d. draws from µ; the theorem does not cover resampling/MCMC-moved particle systems directly.

## B2. Vehtari, Simpson, Gelman, Yao & Gabry (2024)
- Citation: A. Vehtari, D. Simpson, A. Gelman, Y. Yao, J. Gabry. "Pareto smoothed importance sampling." J. Mach. Learn. Res. 25(72) (2024), 1-58. arXiv:1507.02646 (v9, 13 Mar 2024). No DOI looked up or asserted.
- Verified: https://jmlr.org/papers/v25/19-556.html (search result: volume/issue/pages); full text read from https://arxiv.org/pdf/1507.02646 (v9). (One copy's running header says 1-57, JMLR page says 1-58.)
- Quotes (arXiv v9):
  - Abstract: "The presented Pareto k̂ finite sample convergence rate diagnostic is useful for any Monte Carlo estimator."
  - Algorithm 1: "If the estimated shape parameter k̂ exceeds min(1 − 1/log10(S), 0.7), report a warning that the resulting importance sampling estimates are likely to be unstable or have high bias. For S > 2000 this threshold is 0.7."
  - Sec 3.1: "Extensive experiments show that for typical moderate sample sizes used in practice, PSIS gives reliable (that is, low bias, low variance) estimators of Ih when k̂h < 0.7."
  - Sec 3: "A simple option would be to use this estimate k̂ and trust importance sampling as reliable if k̂ < 0.5, as it would indicate that the variance is finite and the central limit theorem holds."
  - Sec 6.4: "This resembles the algorithms such as population and sequential Monte Carlo, and particle filtering"; "Analyzing the effect of these in different population and sequential Monte Carlo and particle filter algorithms and applications would be worthy of further study." Also App G: "in sequential and iterative methods such as particle filters ... we may want to use small S for computational speed issues."
- Relevance for us: k̂ can be applied to the importance ratios π/π₀ over the π₀-sample (or to the per-step incremental weights of the bridge) at no extra cost, giving a pass/warn flag (k̂ < 0.5 clean, 0.5-0.7 caution, > 0.7 flag; thresholds as published). Our rebuild flag could be tied to k̂ > 0.7. The authors explicitly list SMC use as unstudied (Sec 6.4), so any claim that k̂ is calibrated for tempered SMC weights would be new and would need our own simulation. In a finite model space the weights are bounded, so the Pareto-tail framing is heuristic. [INFERENCE]

## B3. Vehtari, Gelman, Simpson, Carpenter & Bürkner (2021)
- Citation: A. Vehtari, A. Gelman, D. Simpson, B. Carpenter, P.-C. Bürkner. "Rank-normalization, folding, and localization: an improved R̂ for assessing convergence of MCMC (with discussion)." Bayesian Analysis 16(2) (2021), 667-718. DOI 10.1214/20-BA1221. arXiv:1903.08008 (v5, 22 Jun 2021).
- Verified: Crossref (title/vol/issue/pp/DOI); full text read from https://arxiv.org/pdf/1903.08008 (v5).
- Quotes (arXiv v5):
  - Abstract: "Traditional R̂ will fail to correctly diagnose convergence failures when the chain has a heavy tail or when the variance varies across the chains. In this paper we propose an alternative rank-based diagnostic that fixes these problems."
  - Sec 1/3 (recommendations): "R̂ < 1.01. This threshold is much tighter than the one recommended by Gelman and Rubin (1992)" (the start of that sentence, which sets the 1.01 rule for declaring a sample usable, was cut by the text extraction); "we recommend running at least four chains by default."; "we recommend requiring that the rank-normalized ESS is greater than 400, a number we chose based on practical experience and simulations".
  - Also: bulk-ESS and tail-ESS (5% and 95% quantiles) are introduced; "Convergence diagnostics are most effective when computed using multiple chains initialized at a diverse set of starting points."
- Relevance for us: this is for MCMC chains, not SMC particles. The transferable piece is the multi-run logic. Our independent islands play the role of diverse-start chains, so rank-normalized split-R̂ (on per-island PIP traces or PIP estimates across islands) is a natural "island agreement" statistic, with the 1.01 and 400 values as published reference points. R̂ across SMC islands is a use outside the paper's scope, and the thresholds are not validated for it. [INFERENCE]

## B4. Elvira, Martino & Robert (2022)
- Citation: V. Elvira, L. Martino, C. P. Robert. "Rethinking the effective sample size." Int. Statist. Rev. 90(3) (2022), 525-550. DOI 10.1111/insr.12500. arXiv:1809.04129 (v2, 31 Mar 2022).
- Verified: Crossref (vol/issue/pp/DOI); full text read from https://arxiv.org/pdf/1809.04129 (v2).
- Quotes (arXiv v2):
  - Abstract: "However, we show that the multiple assumptions and approximations in the derivation of ESS-hat makes it difficult to be considered even as a reasonable approximation of the ESS." Eq (1): ESS-hat = 1 / Σ_{n=1}^N w̄_n² (w̄ normalized weights).
  - On ESS-hat (their list): "a good approximation of ESS should never be upper bounded"; "ESS-hat does not depend on the function h"; "ESS-hat does not depend on the set samples {Xn}, but only in their associated (normalized) weights".
  - Huggins-Roy family (Table 1): the β = ∞ member is 1/max[w̄1,...,w̄N] ("[34]"); β = 1 is the perplexity; β = 2 is ESS-hat.
- Relevance for us: the particle ESS = 1/Σw̄² that our SMC uses for resampling triggers is the Kong/Liu rule of thumb, and B4 says it is only a heuristic (not a variance ratio) and is blind to h. Use ESS as a trigger, not a certificate; add the 1/max w̄ (β=∞) member as a conservative companion, matching the max-weight idea in B1. Their scope statement: "This paper does not cover the use of ESS for MCMC algorithms."

## B5. Biswas, Jacob & Vanetti (2019) (optional)
- Citation: N. Biswas, P. E. Jacob, P. Vanetti. "Estimating convergence of Markov chains with L-lag couplings." Advances in Neural Information Processing Systems 32 (NeurIPS 2019). arXiv:1905.09971 (v3, 28 Oct 2019). Pages not asserted.
- Verified: https://papers.nips.cc/paper/2019/hash/aec851e565646f6835e915293381e20a-Abstract.html (venue NeurIPS 2019 / NeurIPS vol. 32 confirmed); full text read from https://arxiv.org/pdf/1905.09971 (v3).
- Quotes (arXiv v3):
  - Abstract: "We introduce L-lag couplings to generate computable, non-asymptotic upper bound estimates for the total variation or the Wasserstein distance of general Markov chains." and "Lastly, we (iv) assess the bias of sequential Monte Carlo and self-normalized importance samplers."
  - Sec 4, eq (7): "dTV(q^(N), π) ≤ E[max(0, (τ^(L) − L)/L)] = E[(1 − α(Ẑ_{L−1})) / (1 − (1 − α(Ẑ_{L−1}))^L)]", where α(Ẑ) := E[min(1, Ẑ*/Ẑ) | Ẑ] is the average acceptance probability of particle independent MH (PIMH) from a state with normalizing-constant estimate Ẑ.
  - "The bound in (7) depends only on the distribution of the normalizing constant estimator Ẑ, and can be estimated using independent runs of the SMC sampler." and "The proposed bound aligns with the common practice of considering the variance of Ẑ as a measure of global performance of SMC samplers."
  - For self-normalized IS (as cited, not re-derived): "Agapiou et al. [2017, Theorem 2.1] shows dTV(q^(N), π) ≤ 6N^-1 ρ for ρ = E_ξ~q[w(ξ)²]/E_ξ~q[w(ξ)]²". (I did not read Agapiou et al. 2017 itself; this is B5's statement of it.)
- Relevance for us (strong): our SMC returns an unbiased Ẑ from independent islands, which is exactly the input to eq (7). Independent-island runs give the distribution of Ẑ, so a computable TV bound on the particle approximation (for the selected-particle law) follows with no new theory, via PIMH coupling. This is a certifying diagnostic rather than a heuristic flag. It requires running the PIMH/coupled-chain machinery (extra compute) and bounds TV of a single particle's law, not PIP error directly. [INFERENCE on the last two points.] The ρ = E[w²]/E[w]² bound is the χ²+1 divergence between π₀ and π when applied to a one-shot correction, so it links to the chi-square diagnostic requested.

---------------------------------------------------------------------

## C1. Gramacy, Samworth & King (2010)
- Citation: R. B. Gramacy, R. J. Samworth, R. King. "Importance tempering." Statistics and Computing 20(1) (2010), 1-7. DOI 10.1007/s11222-008-9108-5. arXiv:0707.4242 (v6, 3 Nov 2008).
- Verified: Crossref (title/journal/vol/pages/authors); DOI resolves to link.springer.com; full text read from https://arxiv.org/pdf/0707.4242 (v6).
- Quotes (arXiv v6):
  - Abstract: "However, the entire chain can be used to estimate expectations under π of functions of interest, provided that importance sampling (IS) weights are calculated. Unfortunately this method, which we call importance tempering (IT), can disappoint. This is partly because the most immediately obvious implementation is naive and can lead to high variance estimators. We derive a new optimal method for combining multiple IS estimators and prove that the resulting estimator has a highly desirable property related to the notion of effective sample size."
  - Eq (3): "ESS(w) = T / (1 + cv²(w))" (cv = coefficient of variation of the weights; following Liu 2001).
  - Proposition 2.1: "Among estimators of the form (5), ESS(w^λ) is maximised by λ = λ*, where, for i = 1,...,m, λ*_i = ℓ_i / Σ ℓ_i, and ℓ_i = W_i² / Σ_j w_ij²" (W_i as defined in the paper, a per-temperature total weight; I did not re-derive its exact definition).
  - Remark 2.2: "ESS(w^λ*) ≥ Σ_i ESS(w_i) − 1/4 − 1/T" and "In practice ... often it is the case that ESS(w^λ*) ≥ Σ_i ESS(w_i)."
- Contrast with our bridge:
  - IT is simulated tempering: a single MCMC chain moves over temperatures π_k ∝ π^k (k in [0,1]), and the whole chain is reweighted by IS. The path runs from a heated tempered target to π with no designed start distribution and with no unbiased Ẑ.
  - Our method is a tempering path from a designed start π₀ to π (π₀^(1−φ)π^φ), propagated by SMC (resampling plus moves) rather than by a chain over temperatures. It gives an unbiased Ẑ and independent islands. Where IT combines estimators from many temperatures after the fact, SMC reweights the whole population stepwise.
  - A reusable idea [INFERENCE]: Prop 2.1's ESS-optimal weighting could combine PIP estimates across the φ rungs or across islands (weights proportional to W_i²/Σ w²), especially if the final-rung ESS is low. This needs the normalizing constants to be unknown-safe, which is the point of their construction (their text says it avoids needing the normalizing constants).
  - IT's own caveat ("can disappoint") is relevant: naive reuse of all temperatures can be worse than using the cold chain only.

---------------------------------------------------------------------

## Cross-cutting summary

| Need | Best-supported piece | Status |
|---|---|---|
| Composite posterior as SMC start / IS proposal | none found in A1-A5; A4 Thm 2 / Assumption 6(iv) is the nearest (proposal as parametric approximation, χ²-type moment condition) | gap confirmed within these works only; a wider search was not done |
| Calibration of composite posterior | A1 (magnitude, curvature), A2 (magnitude), A5 (scale ω by bootstrap) | parametric asymptotics; not transferable to model space as is |
| Particles needed for π₀→π | B1 Thm 1.1/1.2: N ≈ exp(KL(π||π₀)) | one-shot IS, i.i.d.; bridge benefit is [INFERENCE] |
| Weight diagnostics | B2 (k̂, thresholds 0.5/0.7), B4 (1/Σw̄², 1/max w̄), B1 (qn max-weight ratio, Thm 2.1 warning) | k̂ for SMC weights not validated (B2 Sec 6.4 says unstudied) |
| Island agreement | B3 (rank-normalized split-R̂ < 1.01, ≥ 400 ESS) | MCMC thresholds; transfer to SMC islands unvalidated |
| Certified accuracy | B5 eq (7): TV bound from the law of Ẑ via PIMH L-lag coupling; plus SNIS bound 6N^-1 ρ (Agapiou et al., as cited by B5) | strongest fit; extra compute |
| Tempering contrast | C1: simulated tempering + IS reweighting + ESS-optimal combination (Prop 2.1) | different algorithm; combination rule possibly reusable |

Not verified / not done: full text of A2 and A3 (abstracts only); the Agapiou et al. (2017) theorem (cited second-hand via B5); Crossref lookup failed for the Statistica Sinica DOI (A1 DOI taken from the journal page, which I read); no DOIs asserted for A2, A3, B2, B5.
Local working copies of the PDFs and text are in /tmp/litgap (not part of the repo).
