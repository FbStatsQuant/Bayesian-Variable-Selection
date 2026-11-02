# LIT-MCMC working notes (source log)

Every entry: what I actually read (file/URL), verbatim key statement, conditions. Text extracted with pdftotext
from arXiv PDFs downloaded to /tmp (not committed) or from `Papers/Core_bibliography/` (local copies).
"UNVERIFIED" = seen only second-hand (search snippet / citing paper).

## N1. Yang, Wainwright, Jordan (2016), AoS 44(6):2497–2532 — arXiv:1505.07925v1 (read: abstract, §3.2–3.3, App. A.2)
- Thm 2 (verbatim, v1): "Suppose that Assumption A, Assumption B with s = s0, Assumption C, and Assumption D(s0) all hold.
  Then under either the high SNR condition (9a) or the low SNR condition (9b), there are universal constants c1, c2 such that,
  for any ε ∈ (0, 1), the ε-mixing time of the Metropolis-Hastings chain (3) is upper bounded as
  τε ≤ c1 p s0² [c2 α (n + s0) log p + log(1/ε) + 2] with probability at least 1 − 4p^{−c1}."
- Cor 2: after t ≥ c1 p s0²[c2 α(n+s0) log p + log p + 2] iterations, γ_t = γ* w.p. ≥ 1 − c2 p^{−c3}.
- After Cor 2 (verbatim): "Theorem 2 does not characterize the intermediate regime ... we suspect that the Markov chain
  might be slowly mixing in this regime, but we do not have a proof of this statement."
- App. A.2 "Example of slow mixing" (PROVED in paper): p = n, g = p^{2α}, α > 1, Y = w ~ N(0, I_n) (null truth), UNTRUNCATED
  prior Cp^{−κ|γ|} on {0,1}^p: the MH chain (3) has mixing time exponential in n w.p. ≥ 1/2, by a conductance bound with
  B = {full model} (the saturated model, R² = 1, is a trap). Verbatim: "although a size constraint |γ| ≤ s0 ... is not
  needed for Bayesian model selection consistency, it is necessary for MCMC to mix rapidly."
- Detailed hypothesis-by-hypothesis check on LH: see API-POS REPORT §4.1 (not redone here).

## N2. Chang & Zhou, "Dimension-free relaxation times of informed MCMC samplers on discrete spaces",
## arXiv:2404.03867v2 (28 Jul 2025), "Accepted by Bernoulli" (arXiv listing). Read: §3.1–3.3, §5, Thms 1, 4, 5, Cor 5.
- Definitions: M = max_x |N(x)|; R = min_{x≠x*} max_{y∈N(x)} π(y)/π(x). "If R > 1, we say π is unimodal w.r.t. N."
- Thm 1 (random-walk MH, verbatim): "Assume ρ = R/M > 1. Then, we have π(x*) ≥ 1 − ρ^{−1}, Gap(P0^lazy)^{−1} ≤ c(ρ)M and
  τ(P0^lazy, ε) ≤ c(ρ) M log(1/(ε π_min))."
- Thm 2/3 (informed MH): needs R > M²; relaxation time then free of M ("dimension-free").
- Thm 4 (multimodal / restricted, verbatim): "Let X0 ⊂ X, x0 ∈ X0, η ∈ (0,1) be such that (i) ρ = R|X0 /M > 1,
  (ii) π(x0) ≥ η, and (iii) π(X0) ≥ 1 − ε²η²/5. We have τ_{x0}(P0^lazy, ε) ≤ c(ρ) M log(1/(2ε²η²))."
  So the start enters only through log(1/π(x0)).
- Cor 5: RW-MH on unrestricted add-delete-swap space under YWJ-type (A1)–(A5), start δ0 ∈ V_s with
  π_n(δ0) ≥ 5ε^{−1}p^{−κs/4}: τ_{δ0} = O_p(p² κ s log p).
- Text: "In order to achieve rapid mixing, such unimodal conditions are arguably necessary, since for general multimodal
  targets, the chain can get trapped at some local mode for an arbitrarily large amount of time."
- Text: Example 3 (p = 3, X1'X2 = −0.8n): "π can be unimodal but decrease when we move towards the true model δ* by flipping a
  coordinate different from δ*" — a suppressor-type example, same mechanism as LH linked pairs.
