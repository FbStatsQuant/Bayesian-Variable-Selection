# SMC_LIT: is there prior work on SMC for variable selection, with theory? (Theory Dept, 2026-11-24)

Owner's question (via HQ, 11-24): has anyone published or preprinted variable selection by SMC in a way similar to
ours (`method-v3.1.1-listpip`), and if so with what theory, compared with our Theorems 1–6 and planned P1–P5 (A7 spec)?
Staffing: Opus manager; Claude Work Sonnet workers (2 searchers, 1 retriever, 8 full-text readers). No Fable, no Astra.
Evidence: `notes/` (one file per paper: a coverage log page by page, then model, sampler, theorems, comparison and verdict)
and `search/` (about 120 candidates scored, with queries and citation chains). No PDFs are committed; they are on Owls in
`/home/fb31/SMC_Theory_Department/SMC_LIT/papers/`.

## Verdict

**Theory: novelty risk NONE.** No paper or thesis we found proves anything statistical about an SMC sampler for
variable selection: no posterior or selection consistency, no rate, and no guarantee on what the algorithm reports.
The SMC-for-BVS papers prove nothing (Schäfer–Chopin, Shi–Dunson, Youssfi–Chopin, Vuong, van Assen–Hinne), or only exact
representation identities (Ma 2015), or only the generic law of large numbers for annealed importance sampling (Fan–Pan–McCormick 2026).
The generic SMC complexity theory (Schweizer; Paulin–Jasra–Thiery; Marion–Mathews–Schmidler; Mathews–Schmidler;
Lee–Santana-Gijzen) is never applied to a BVS posterior.

**Method: PARTIAL OVERLAP (low to moderate) on the generic idea only.** Tempered resample-move SMC over inclusion vectors
for Bayesian linear regression is Schäfer & Chopin (2013). Data-sequential SMC over models is Shi & Dunson (2011).
Sequential importance sampling over models is Ma (2015). None has our block-exact start law $\pi_0$, the discrepancy
bridge $\pi_\xi\propto\gamma_0e^{\xi\Delta}$, the pilot-then-frozen grid, Gibbs, swap and neighbour-swap moves inside the
SMC, independent islands, Rao–Blackwellised PIPs, an evidence estimate, the certified reported model, the list outputs,
or $p\gg n$. Their largest $p$: 104 (S–C), 337 (Y–C, $n=47{,}916$), 1,000 (Ma; $n=700$), 100 (S–D). Ours goes to $10^6$.

**Late reads (owner-fetched, 11-24):** Duan (NUS working paper, 2019; SSRN 3377038) and Ročková (2018, *JASA*) were read in
full after the first delivery. Neither has any theorem, so the verdict is unchanged.

## Candidates read in full

| paper | what it is | theory | risk |
|---|---|---|---|
| Schäfer & Chopin 2013, *Stat Comput* (arXiv v1–v4) | resample-move SMC on $\{0,1\}^d$; uniform start; geometric bridge $\pi^{\rho_t}$; conditional-ESS bisection; one independence MH kernel with a fitted logistic-conditionals proposal; PIPs = final weighted particle mean; $d\le104$ | none (no theorem; support conditions only) | partial (the precedent) |
| Schäfer 2012, PhD thesis, Paris-Dauphine (154 pp.) | the above + binary-response GLMs ($d\le95$) + SMC/cross-entropy optimisation ($d=250$) | Ch. 3 only: binary-family algebra (Thm 3.3.2: every valid cross-moment matrix is attained by a unique logistic-conditionals family); nothing on SMC or selection | partial (same as 2013) |
| Shi & Dunson 2011, *SPL* (author preprint, 21 pp.) | particle stochastic search: particles = models, prior start, data-sequential targets, resample when ESS $<M/2$, Gibbs/MH rejuvenation; raw frequency PIPs; $p\le100$ | none (Liu's variance inequality is quoted from the literature) | partial (idea only) |
| Youssfi & Chopin 2024, *FoDS* (arXiv v1, 13 pp.) | waste-free tempered SMC for probit bi-level selection; prior start; ESS-adaptive; one nested-logistic independence kernel; Laplace/ALA marginals; $p\le337$ | none (Dau–Chopin cited, not applied) | partial (low) |
| Ma 2015, *JASA* (arXiv v2 with supplement, 49 pp.) | LIPS: SIS over forward-stepwise inclusion paths, $k$-step look-ahead, no resampling, no tempering, no MCMC; independent runs; Horvitz–Thompson PIPs; $p\le1000$ | Thms 1–3: exactness of the path representation; IS consistency only asserted | partial (low) |
| Fan, Pan & McCormick 2026 (arXiv v1, 28 pp.) | annealed IS over partitions of factorial cells (12–36 cells; not variable selection); start law built from an enumerated "Rashomon set"; geometric bridge; adaptive pilot, then a frozen ladder; independent runs | Thm 1 / Cor 1–2: almost-sure consistency of self-normalised AIS as the number of runs grows | partial (closest analogue of our data-driven start + frozen grid; different model space) |
| van Assen & Hinne 2026 (arXiv v1) | anchored reversible-jump SMC, adaptive tempering; variable selection only at $p=4$ | none | none |
| Vuong 2024, MSc project, SFU | annealed SMC from the prior, fixed 10-rung grid, single-flip moves; $p\le6$ | none (an MC CLT quoted) | none |
| Duan 2019, NUS working paper (SSRN 3377038) | best subset of FIXED size $p_s$ by in-sample $R^2$ (optimisation, not a posterior): density-tempered SMC over permutations; start law $\propto$ single-regressor $R^2$; geometric bridge with ESS-adaptive steps; block re-draw moves; reports the best subset only; $p\le900$, $p_s\le20$ | none: informal "global optimum as $M\to\infty$" remarks and a heuristic Weibull approximation of the maximal $R^2$ | partial (method family; low) |
| Ročková 2018, *JASA* (+ 5-page supplement) | Particle EM: a deterministic ensemble optimiser of an entropy-regularised ELBO over $K$ binary models (continuous spike-and-slab, BB(1, p)); inclusion probabilities renormalised over the particle set; a secondary SMC variant on a fixed $v_0$ grid; $p\le200$ | none (supplement: an elementary TV bound $\lVert\pi-\pi_T\rVert\le2\sum_{\gamma\notin S}\pi(\gamma\mid Y)$) | none to partial (precursor of list-renormalised PIPs) |

Not read in full (not SMC over models, or background only): Bottolo & Richardson 2010 (ESS, tempered population MCMC), Zanella & Roberts
2019, Papaspiliopoulos & Rossell 2017 (exact block-diagonal marginals, the nearest precedent for our block tables), Jasra et al.
2008 (trans-dimensional SMC, mixtures).

## Our theory against theirs

| ours (A7) | closest existing result | relation |
|---|---|---|
| Thm 1: $1-\pi(S_0\mid y)=O_P(\sqrt{\log n/n})$, $\mathrm{HPM}=\mathrm{MPM}=S_0$ w.p. $\to1$, sub-Gaussian random design | BVS posterior-concentration literature (Yang–Wainwright–Jordan 2016 for $g$-priors; Song–Liang) | no SMC paper; posterior-level results exist for other priors, already cited by us |
| Thm 2: Hellinger contraction $\sqrt{M\log n/n}$ | none in the SMC literature | none |
| Thm 3: on data events of probability $\to1$, **every** run that produces output reports $\hat S=S_0$, for any seed and calibration | none. Mathews–Schmidler 2024 and Paulin–Jasra–Thiery 2019 bound SMC error via mode-mass conditions, but on generic targets and not for the reported model | **new**; those papers support the form of our visibility/leak assumption and are worth citing as context |
| Thm 4: certified screening | none | none |
| Prop 5: $\mathbb E[\hat Z_r\mid\mathcal C]=Z$ | **classical**: Del Moral (2004); Schweizer 2012a Prop. 2.3 (after Del Moral–Miclo 2000): $\prod_j\eta^N_j(g_{j,j+1})$ is unbiased for $Z_n/Z_0$ | cite as standard; our contribution is only that the coded algorithm (frozen grid, conditional on the calibration record, islands) satisfies it |
| Thm 6: the $\sqrt{\log n/n}$ rate cannot be improved | none | none |
| P1 (trap theorem) | Yang–Wainwright–Jordan 2016 Thm 2 (single/double-flip MH mixes in $\approx p\,s_0^2(n+s_0)\log p$ steps under RE/SNR conditions); Zhou et al. 2022 (LIT-MH mixes fast when the posterior is unimodal under add/delete/swap; their Example 1 is a proved slow case) | **P1 must be positioned against both**: the design family must violate their conditions while our consistency holds. Nothing covers Zanella–Roberts. Schäfer–Chopin (p. 11: local kernels "practically impossible" inside SMC) and the thesis (p. 40) give empirical motivation |
| P2–P4, P5 | none | none |

## What we must cite, and how we differentiate

- **Cite as SMC-over-models precedents:** Schäfer & Chopin 2013 (+ thesis 2012), Shi & Dunson 2011, Ma 2015, Youssfi &
  Chopin 2024, Duan 2019 (tempered SMC for best subset); Ročková 2018 with Clyde–Ghosh for list-renormalised summaries; for the start law, Papaspiliopoulos & Rossell 2017 (block tables) and Fan et al. 2026 (data-driven start,
  frozen ladder); for the SMC machinery, Del Moral–Doucet–Jasra 2006, Del Moral 2004 and Schweizer 2012a (Prop 5).
- **One-sentence differentiation:** *"Tempered SMC over inclusion vectors goes back to Schäfer and Chopin (2013). Their
  sampler and its successors start from the uniform law or the prior, move particles with a single fitted
  independence proposal, and come with no theory. Ours starts from an exactly samplable block-product law, runs Gibbs,
  swap and independence moves on a calibrated frozen grid across independent islands, scales to $p=10^6$, and comes with
  posterior and distribution-level consistency, a guarantee that every run reports the true model on high-probability
  data events, certified screening, and an unbiased evidence estimate."*
- **List-renormalised PIPs ($\mathrm{pip}_{\mathcal T}$): a presentation risk, not a novelty risk.** Clyde & Ghosh 2012
  (Prop 2: the bias of ratio estimators) and García-Donato & Martínez-Beneito 2013 (renormalised PIPs off by up to about 0.6 on
  Ozone65) show that renormalising over visited models can be badly biased. So: keep the Rao–Blackwellised SMC PIP as the
  headline estimate; present $\mathrm{pip}_{\mathcal T}$ as a deterministic function of the list; report the list mass
  next to it; and use the elementary bound $\lvert\mathrm{pip}_{\mathcal T}(j)-\mathrm{PIP}_j\rvert\le1-\pi(\mathcal T\mid y)$
  (manager-checked) as the reason Cor 6L needs the list to carry most of the mass. Cite both papers.

## Limits of this search

- About 120 candidates; Google Scholar and ProQuest only through web search; Semantic Scholar was rate-limited, so the forward citation
  chains of Schäfer–Chopin (106 citing items) and Shi–Dunson were followed through Semantic Scholar plus OpenAlex.
- Versions not obtained: the Schäfer–Chopin journal version and its announced genetics supplement; the JASA versions of
  García-Donato & Martínez-Beneito (arXiv v1 read) and Ma (arXiv v2 with supplement read); the published Shi–Dunson text (preprint read).
  Duan 2019 and Ročková 2018 were obtained by the owner and read in full.
- The readers' typo findings in others' papers (Yang et al. A.2 exponent; Fan et al. eq. (3)) are noted in `notes/`, unverified.
