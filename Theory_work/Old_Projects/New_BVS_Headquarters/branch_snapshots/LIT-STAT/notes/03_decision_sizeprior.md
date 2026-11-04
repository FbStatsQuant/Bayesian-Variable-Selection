# Notes 03: decision theory (HPM/MPM) and size priors

## Barbieri & Berger (2004), Ann. Statist. 32(3) 870–897. READ: Papers/Priors_and_decision_rules/Barbieri_Berger_2004_...pdf
- Intro, quoted: "With the Bayesian approach to model selection it is commonly perceived that the best model will be that with the
  highest posterior probability. This is true under very general conditions if only two models are being entertained ... but is not
  generally true." And: "Initially we had sought to find conditions under which the highest posterior probability model was the optimal
  predictive model. It came as quite a surprise to find that any optimality theorems we could obtain were, instead, for the median
  probability model." "One obvious situation in which [MPM and HPM coincide] is when there is a model with posterior probability greater
  than 1/2."
- Thm 1, quoted: "If Q is diagonal with diagonal elements q_i > 0, condition (17) holds and the models under consideration have
  graphical model structure, then the median probability model is the best predictive model." Proof, quoted: "To minimize (18) among all
  possible models, it is clear that one should choose l_i = 1 if p_i ≥ 1/2 and l_i = 0 otherwise". Cor 1 (all submodels), Cor 2 (nested),
  Thm 3/Cors 3–4 (semi-orthogonal, nested) under Conditions 1–3.
- Loss: PREDICTIVE squared error, not support loss. The coordinate-wise "include iff PIP ≥ 1/2" step is the same algebra as T07(ii)(b)
  (MPM minimises posterior Hamming risk), which is folklore: the Hamming risk is Σ_j [a_j(1−PIP_j) + (1−a_j)PIP_j].
- Bearing on Prop 1 (T07): (ii)(a) HPM = Bayes rule under 0–1 support loss — textbook; (ii)(b) MPM = Bayes rule under Hamming loss —
  folklore / immediate; (ii)(c) capped version (top-ℓ PIPs inside {PIP > ½}, ℓ = min(K, N₊)) is a trivial but, as far as we found,
  unstated variant needed because our model space is capped at K. None is new as mathematics; they are needed bookkeeping.
  (iii) "target vs reported" (Ŝ = S† iff S† scored) is method-specific and not in the literature we read; it is elementary.

## Barbieri, Berger, George & Ročková (2021) "The median probability model and correlated variables" (Bayesian Analysis 16(4),
## 1085–1112 — venue from INDEX only, UNVERIFIED). READ: Papers/Core_bibliography/22_...pdf = arXiv:1807.08336v2 (2018 version)
- Thm 3.1 "Mini-theorems" (q = 2): e.g. quoted "5. In Cases 1 and 2, if M00 or M11 has posterior inclusion probability larger than 0.5,
  it is optimal." Followed by, quoted: "in going to the three-dimensional problem, we were able to develop counterexamples (not shown
  here) to each of the mini-theorems."
- Discusses near-duplicate columns and prior "dilution" (cites George 2010), and argues for g-priors over product priors under
  replicates (§2: a g-prior's marginal likelihood is unchanged by adding replicates — "predictive matching").
- Bearing: Our setting is selection (0–1/Hamming) loss, not prediction; MPM-vs-HPM optimality results do not transfer. The
  "dilution" problem they discuss is the same name as our study's masking mechanism ("dilution", W8-SYNTH); a citation point for the
  phenomenon, not a theorem we duplicate.

## Rossell (2022) Prop 1 (see notes 02): P(HPM ≠ t) ≤ 2E(1 − p(M_t|y)), and the same for MPM. → T03♯(3), T07-adjacent.

## Size-only priors and within-size swaps: what is known
- Scott & Berger (2010), Ann. Statist. 38(5) 2587–2619. READ: Core_bibliography/04_... (arXiv:1011.2333). Quoted: "selecting p = 1/2 does
  not provide multiplicity correction. Treating p as an unknown parameter to be estimated from the data will, however, yield an
  automatic multiple-testing penalty." With a uniform prior on the inclusion probability, the model prior depends only on |γ|.
- Wilson, Iversen, Clyde, Schmidler & Schildkraut (2010), Ann. Appl. Stat. 4(3) 1342–1364 (arXiv:0908.1144). READ local PDF.
  Eq. (2.7) BetaBinomial(a, b) model prior; quoted: "we recommend a = 1 as a default, so that the prior distribution on model size is
  nonincreasing in s_γ. The hyperparameter b can then be chosen to reflect the expected model size". (BB(1, b) with b ∝ p is in this line.)
- Castillo & van der Vaart (2012), Ann. Statist. 40(4) 2069–2101 (arXiv:1211.1197). READ local PDF. Example 2.2: α ~ Beta(κ, λ),
  binomial(n, α) dimension; "The mean dimension is nκ/(κ+λ), which suggests to choose the hyper parameters ... so that κ/(κ+λ) is in the
  range (c/n, Cp_n/n)." CSvdV (2015) l.277: Beta(1, p^u) with u > 1 satisfies the exponential-decrease condition. Theorem 2.8/§2 text,
  quoted: "The above results show that g_S needs to have heavy tails." (sequence model, fixed slab).
- None of these states T07(i). T07(i) is a one-line observation (a size-only prior multiplies every model of size k by the same w(k),
  so within-size ranking is the marginal-likelihood ranking); it is "folklore-level" — consistent with Scott–Berger's framing that
  size priors correct multiplicity, not ranking — but we did not find it stated as a proposition. Status in the literature: NOT FOUND
  (absence after a targeted search, not proof of absence).

## Liang, Paulo, Molina, Clyde & Berger (2008), JASA 103(481) 410–423. READ local PDF (text extraction is garbled in §4.2).
- §4.2 "Model Selection Consistency", definition (21) from Fernández et al. (2001): plim p(M_γ|Y) = 1 under the true model; Theorem 3
  (fixed p): mixtures of g-priors (hyper-g, Zellner–Siow, EB) are consistent. Statement legible only partially → PARTIALLY VERIFIED.
  Fixed p; no bearing on p ≥ n beyond being the classical baseline that g = n (unit information) is consistent for fixed p
  (Fernández–Ley–Steel 2001, NOT read: UNVERIFIED).
