# LIT-VENUE — REPORT: what comparable methodology papers prove, and which venue our package supports

Run LIT-VENUE (Opus 5.5), branch `theory/LIT-VENUE`, 2026-11-02. This is a literature task with no new mathematics, so the
campaign's status words apply only where I quote *our* results, and I copy those statuses from their sources. Every claim
about a paper is tied to a file or URL I actually read, listed in `NOTES.md` with line numbers in the text dump. Anything I
saw only second-hand is marked UNVERIFIED. Scripts: `scripts/extract.sh` (PDF → text) and `scripts/crossref.sh` (venue
check via the Crossref API).

Our side, as I read it (sources: `W8-SYNTH/BRIEF.md`, `T38-RECORD/T38_STATEMENT.md`, `F-REFINE/ARCHITECTURE.md`,
`API-POS/REPORT.md`, `API-N200/REPORT.md`, `Docs/THEORY_PRIORITIES.md`, `METHODOLOGY_v3.md` §1–2):
- **Thm 1 (T03♯).** Posterior consistency. Asymptotic, with thresholds ≈ 2·10⁶.
- **Thm 2 (T22/T27, EXP′, chain masking).** The start law: favourable versus masked regime.
- **Thm 3 (T37 Theorems A/B).** Greedy and Gibbs-path repair.
- **Thm 4 (T21) and API-N200 Theorem N200.** Exact error decomposition for every n.
- **Thm 5 (T38).** Consistency of the reported HPM:
  - (a) favourable regime;
  - (b1) masked regime with LS0 on LH;
  - (b1′-LH) and (b2-LH): masked regime without LS0, on an LH subfamily;
  - (c) polynomial cost under T32(i).
- **Thm 6 (T26).** Evidence and PIP consistency.
- **Prop 1 (T07).** The HPM is the Bayes rule.
- **Prop 2 (T12 + T31(i)).** Unbiased evidence and the islandwise PIP identity.
- **W7-SEP.** SEP(A)/(B) and Prop GU.

Study: n = 200, p ∈ {500, 1000}, scenarios S1–S6, two signal scales, s₀ = 14, 2,400 fits.

---

## 1. Headline

1. **Sample.** I read 30 works at primary-source level: the 24 rows of §2 and the 6 certificate rows. Of the 24, 23 are
   2016–2026 work on BVS computation or SMC/MCMC for model spaces; Schäfer–Chopin 2013 is included as the ancestor of our
   method. Across all 30, the venues are JRSS-B (8), AoS (3), JASA (3), Bayesian Analysis (3), Biometrika (2), Bernoulli,
   Statistica Sinica, JCGS, Statistics and Computing, NeurIPS/AISTATS and arXiv. **No paper in the sample proves anything
   about the output of an SMC sampler for BVS.** The SMC-for-BVS papers (Schäfer–Chopin 2013;
   Zhou–Johansen–Aston, JCGS 2016) contain no theorems. The general SMC complexity results (Le Fay–Chopin–Vihola 2026)
   assume a spectral gap and bounded χ² increments, and nobody has verified these for BVS model spaces.
2. **The theory-heavy BVS-computation papers in the top venues all prove one kind of result.** YWJ (AoS 2016), ZYVR (JRSS-B
   2022), Zhou–Chang (AoS 2023) and Chang–Zhou (Bernoulli 2026) each give **an explicit polynomial mixing-time bound for the
   sampler they propose**. It holds with high probability as n, p → ∞, under posterior-concentration conditions, and is
   illustrated by simulations that show trends, not constants. None of them claims finite-n validity at the simulated
   sizes. Our lack of an n = 200 theorem is therefore normal. What we lack, compared with them, is a clean explicit-rate
   theorem for the algorithm as run, holding beyond one constructed design family.
3. **Threats.**
   - Thm 1 is standard in kind: YWJ Thm 1, Shin–Bhattacharya–Johnson 2018, Rossell–Abril–Bhattacharya 2021. Our variant
     differs in its g = n, BB(1, p) prior with the ⌊n/2⌋ cap.
   - Prop 2's unbiasedness is textbook SMC: Del Moral 2004, as cited by ZJA 2016.
   - Polynomial-time recovery of S₀ on LH already follows, with their priors, from YWJ/ZYVR (API-POS). It also follows from
     Chang–Zhou's unimodality condition R > M, since on LH S₀ is the unique local mode.
   So **T38(c), "polynomial cost", is not a selling point on its own.**
4. **Gaps that are genuinely ours.** I found nothing in the sample that does any of the following:
   - (i) gives an exact, algorithm-agnostic finite-n split of the reported-model error into a posterior-miss term and a
     search-miss term that can be measured per run (Thm 4 / N200);
   - (ii) proves a lower bound for an independent-draw start law (Thm 2 masked / SEP(A)), paired with a repair theorem that
     restores consistency (Thm 3, T38(b));
   - (iii) proves consistency of an SMC-BVS output at all.
   Machine-checked (Lean) proofs are also absent from this literature.
5. **Venue verdict (judgement, not a status word).** The package **realistically supports Biometrika, the 5-result cut,
   only if** the referee's major point is met: Thm 5(b) for the algorithm as run, with the transition shown at growing n.
   It supports **JCGS, Bayesian Analysis, EJS or Statistics and Computing comfortably** if the numerics are strengthened.
   JRSS-B is a stretch. AoS is not realistic.
   **Typical expectations we do not yet meet:**
   - real-data analyses;
   - head-to-head comparisons with current samplers (LIT-MH, PARNI, MAdaSub, TGS) and with SuSiE/SSL;
   - simulations at growing n that show the theory's regime;
   - a main theorem not tied to the constructed LH family;
   - and, for us specifically, external human review of proofs that are now AI-checked only.

---

## 2. Annotated table

Legend for "Our designs":
- **NO-n200**: the conditions are asymptotic or require posterior concentration w.h.p. At n = 200 the study has 565
  posterior misses in 2,400 fits (S-ELS), and Π(X) is 5–75% per cell (API-N200). So no concentration-based premise can
  hold uniformly over the study cells.
- **LH?**: whether the premise plausibly holds on the linked-hub family.

"Relation" uses our registry IDs.

| # | Citation, venue | Method | What is PROVED (quoted or paraphrased from the source, with conditions) | Our designs | Relation to ours |
|---|---|---|---|---|---|
| 1 | Yang, Wainwright, Jordan, *AoS* 44(6) 2016 (arXiv 1505.07925) | Add/delete/swap MH on a truncated sparsity prior | **Thm 1:** πn(γ*\|Y) ≥ 1 − c₁p⁻¹ w.p. ≥ 1 − c₂p^{−c₃}, under beta-min Cβ² ≳ (L+L̃+α+κ)σ² log p/n, the prior g ≍ p^{2α} with κ+α ≥ C₁(L+L̃), restricted eigenvalues, and s* ≲ n/log p. **Thm 2:** ε-mixing time ≤ c₁ p s₀² [c₂α(n+s₀) log p + log(1/ε) + 2] w.h.p. **Cor 2:** after that many iterations, γ_t = γ* w.h.p. Intermediate SNR: "slow mixing due to multimodality" (App. A.2). Main theorems: 2 plus 1 corollary; illustrative simulations with s* = 10. | NO-n200. Our prior (g = n, BB(1,p), cap ⌊n/2⌋ ≫ n/log p) violates C and D (API-POS item 3). LH?: yes with *their* prior, in the iid realisation (API-POS, PROOF SKETCH) | Overlaps **Thm 1** (same kind of result). Implies poly-time recovery on LH under their prior, which **weakens the novelty of T38(c)**. Its intermediate-SNR slow mixing is a posterior-level analogue of our start-level masking (Thm 2), so the two are complementary |
| 2 | Zhou, Yang, Vats, Roberts, Rosenthal, *JRSS-B* 84(5) 2022 | LIT-MH (locally informed, thresholded) | **Thm 1:** if n = O(p), s₀ log p = O(n), κ = O(s₀) and Condition 1 holds with c₀ = 2, 4 ≤ c₁ ≤ nκ₁ − κ, then T_mix ≤ 800 max{nκ₁/c₁, 3s₀}. This is the TV mixing time from the worst start in M(s₀), and it is dimension-free. **Condition 1:** (1a) for overfitted models, adding a variable lowers the posterior by B ≤ p^{−c₀}; (1b) every underfitted γ has some j ∈ γ*∖γ with B ≥ p^{c₁}; (1c) a swap version of (1b). **Thm 2:** general drift-based mixing. Simulations up to n = 1000, p = 5000; real data with n = 5,418, p = 328,129 | NO-n200. On LH, (1b) holds for our target, but (1a) holds only with c₀ ≈ ½ when p ≍ n, with κ_eff ≈ 1 against their κ ≥ 18 (API-POS item 3, PROOF SKETCH) | **Main threat to T38(c)/(b) novelty** (API-POS). Complementary to Thm 4: they bound mixing, we bound error through scoring |
| 3 | Chang & Zhou, *Bernoulli* 32 2026 (arXiv 2404.03867) | Informed and random-walk MH on general discrete spaces | Define R := min_{x≠x*} max_{x′∈N(x)} π(x′)/π(x); "R > 1 ⇒ π is unimodal w.r.t. N". **Thm 1:** if ρ = R/M > 1, then π(x*) ≥ 1 − 1/ρ and relaxation time ≤ c(ρ)M (M = max\|N(x)\|). **Thm 4 (multimodal):** restrict to X₀ with R\|X₀/M > 1, take a warm start x₀ with π(x₀) ≥ η and π(X₀) ≥ 1 − ε²η²/5; then τ_{x₀} ≤ c(ρ)M log(1/(2ε²η²)) | NO-n200. On LH at p ≤ 20, S₀ is the unique local mode, so R > 1 (API-POS, exact enumeration); R > M is not checked | Thm 4's warm-start formulation is the closest published analogue of our **start → repair** story (Thm 2 + Thm 3 + T38(b)). Threat: makes "a good start plus local moves suffices" a known template. Ours differs in using an explicit start law with a masking lower bound, and SMC |
| 4 | Zhou & Chang, *AoS* 51(3) 2023 | RW-GES MCMC on DAG equivalence classes | Rapid mixing of RW-GES under high-dimensional assumptions. A "swap" move is needed so that classes on the boundary of the restricted space are not local modes. Strong selection consistency (Thm 5). Consistency of greedy local search on the restricted space (abstract and §1 read) | Different model space | Methodological template: polynomial-complexity theorem + consistency + greedy local search. Analogue of our **Thm 3 / LS0** |
| 5 | Zanella & Roberts, *JRSS-B* 81 2019 | Tempered Gibbs sampling (TGS), weighted TGS (importance tempering) | **Thm 1:** var(h,TGS) ≤ b² var(h,GS) + b² var_f(h). **Thm 2:** under independent components, t_GS = α₁p, t_TGS = α₂p, t_wTGS = s(1 − q_min). **Thm 3:** in a stylised two-collinear-variable model, t_GS ≥ O(c^{1/2}h⁻¹p) and t_wTGS = O(s). The conjecture t_TGS ≤ O(p) is left open | Stylised models only. API-POS item 4: says nothing quantitative about LH | Complementary. Its "tempering helps on collinear designs" story is the one W7-SEP warns us not to claim; we claim "moving off the start" |
| 6 | Zanella, *JASA* 115 2020 | Locally balanced informed proposals | **Thm 1:** a pointwise informed proposal is locally balanced iff g(t) = t g(1/t). **Thm 2:** Peskun-type ordering, P₁ ≥ cP₂ ⇒ Gap(P₁) ≥ c Gap(P₂). **Thm 4:** weak limit as n → ∞ | n/a (general) | Background. Our moves are not informed proposals |
| 7 | Griffin, Łatuszyński, Steel, *Biometrika* 108 2021 | Adaptive MCMC (ASI, exploiting near-independence) | **Prop 1:** variance of independent and random-walk proposals; **Prop 2:** conditions for approximate posterior independence of γ_j, γ_k; ergodicity section (§3). No rate | n/a | Shows that **Biometrika accepts BVS-computation papers with a light theorem load plus strong numerics** |
| 8 | Liang, Livingstone, Griffin, *Stat. Comput.* 32 2022 | Adaptive random-neighbourhood informed MCMC (PARNI) | **Thm 1:** equivalence of kernels; **Thm 2:** "Ergodicity and SLLN … hold for both the PARNI-KW and PARNI-RM samplers". Real data: n = 506/p = 104, n = 1030/p = 79, n = 96/p = 88 | n/a | Benchmark competitor. Its theory (ergodicity) is far weaker than ours |
| 9 | Staerk, Kateri, Ntzoufras, *Bayesian Analysis* 19(1) 2024 | MAdaSub: adaptive independent MH on subspaces | **Thm 1:** "ergodic for all choices of r⁽⁰⁾ ∈ (0,1)^p, L_j > 0 and ε ∈ (0, 0.5) and fulfils the weak law of large numbers" (via Roberts–Rosenthal 2007). Real data up to p = 22,575, n = 60 | n/a | Bayesian Analysis precedent: ergodicity plus heavy numerics. Competitor |
| 10 | Titsias & Yau, *JASA* 112 2017 | Hamming-ball sampler | No numbered theorem found (grep of the arXiv version). Validity by construction; numerics | n/a | JASA T&M precedent with **zero theorems** |
| 11 | Papaspiliopoulos & Rossell, *Biometrika* 104 2017 (venue UNVERIFIED by Crossref) | Exact BVS/BMA under block-diagonal X′X (Coolblock) | **Props 3.2–3.4:** with block-diagonal X′X and Zellner's prior, the top model of each size is given by ordering scores; Coolblock "outputs a series of models M, each of which has largest p(γ\|y,ω) amongst all models of its size". Simulations with p = 100/n = 150 and p = 500/n = 510 | Our designs are not block-diagonal. Our start law uses exactly enumerated correlation blocks | **Closest precedent for an exact (certified) HPM**, under orthogonal blocks. Complementary to the start construction and to our per-fit certificate ideas (O-CERT C5) |
| 12 | Shin, Bhattacharya, Johnson, *Statistica Sinica* 2018 | Nonlocal priors + S5 stochastic search | **Thm 1/3:** under Assumptions 1–5, a uniform prior on \|k\| ≤ q_n, and σ² known or unknown, "π(t\|y) converges to one in probability as n → ∞". No theorem on S5 | NO-n200 | Overlaps **Thm 1** in kind. Shows the "consistent target + heuristic search + simulations" model, which is the gap our Thm 4 fills |
| 13 | Rossell, Abril, Bhattacharya, *JRSS-B* 83 2021 | Approximate Laplace approximations (ALA) | **Thm 1:** under misspecification (y,z) ~ F*, ALA screening discards variables outside the true model. **Thm 2:** spurious-addition Bayes factors B̃ = O_p(n^{−(p_γ − p_γ̃*)/2}) | NO-n200 | Overlaps **Thm 1**: posterior/BF rates of the standard kind |
| 14 | Hou, (Wang,) Atchadé, *AISTATS* 2026 (PMLR 300; arXiv 2407.20580) | One-step Laplace posterior + MH | **Thm 2:** concentration of Π̌ when c₂n ≥ 2(u+1) log p. **Thm 4:** from δ⁽⁰⁾ with the **warm-start condition** Π̌(δ⁽⁰⁾\|D) ≥ p^{−α}, if N ≥ C(s⋆ + (4α/u) log(1/ζ₀) + α log p)p, then ‖P(δ⁽ᴺ⁾ = ·\|δ⁽⁰⁾) − Π̌‖_TV ≤ max(ζ₀, 4/p^{4u}) | NO-n200 | **Directly parallels** our framing. Their warm-start mass p^{−α} is the quantity our masked regime makes tiny (Q_f π₀(S₀) ≲ 10⁻⁶ at n = 200; API-N200 item 3). Complementary: we prove what happens when the warm start fails |
| 15 | Schäfer & Chopin, *Stat. Comput.* 2013 (pre-range; direct ancestor) | SMC on binary spaces with adaptive parametric proposals | No numbered theorems (grep) | — | **Ancestor of our method.** Confirms that SMC-BVS has no output theory |
| 16 | Zhou, Johansen, Aston, *JCGS* 25 2016 | Adaptive SMC for model comparison | No numbered theorems. Unbiased Ẑ cited to Del Moral (2004, Prop. 7.4.1) (l.352) | — | Makes **Prop 2 (T12) unbiasedness standard**. JCGS precedent with no theorems |
| 17 | Dau & Chopin, *JRSS-B* 84 2022 | Waste-free SMC | **Thms 1–2:** CLTs for waste-free SMC with M = O(P^α) under Assumptions (M), (G); asymptotic in N | General | Supports **Thm 6/Prop 2**-type Monte Carlo consistency. Standard tool |
| 18 | Le Fay, Chopin, Vihola, arXiv 2604.03352 (2026, venue not found) | Standard and waste-free SMC | "finite sample bounds for the error". **Thm 2.3:** sample sizes under A2.1 (K_t is π_{t−1}-invariant) and A2.2 (1 + χ²(π_t\|π_{t−1}) ≤ χ̄²), via mixing times. **Thm 3.4:** with spectral gap γ and χ̄² = 2, P ≥ 2560T/(γε²) gives \|Ẑ_T/Z_T − 1\| < ε w.p. ≥ 3/4 | A2.2 needs a tempering schedule with χ² ≤ 1 per step. A spectral gap for our Gibbs/swap kernels at intermediate φ is **not known**, and in the masked regime it is plausibly exponentially small | **Threat and opportunity for T38(c):** a generic finite-sample SMC complexity theorem exists. Its premises are what is hard for BVS. Our discovery-based route avoids needing a gap |
| 19 | Syed, Bouchard-Côté, Chern, Doucet, *JRSS-B* 2026 | Optimised annealing schedules for SMC | **Thm 1:** variance of Ẑ in terms of the accumulated discrepancy D(B_T); **Thm 2:** smoothness of D | General | Relevant to our calibration schedule; complementary |
| 20 | Wang, Sarkar, Carbonetto, Stephens, *JRSS-B* 82 2020 (SuSiE) | Variational sum of single effects (IBSS) | **Cor 1:** IBSS is coordinate ascent on the ELBO; **Prop 2:** converges to a stationary point; **Prop 3:** exchangeability for identical columns. No consistency theorem; coverage assessed by simulation | n/a | JRSS-B precedent: **weak theorems, very strong numerics and real data.** Main empirical competitor |
| 21 | Ray & Szabó, *JASA* 117 2022 | Mean-field VB with spike-and-slab | **Thm 1:** the VB posterior contracts at minimax rates (ℓ₁, ℓ₂, prediction) | NO-n200 | Theory-for-the-approximation template, but for a different object |
| 22 | Ascolani, Roberts, Zanella, *JRSS-B* 88 2026 | Metropolis-within-Gibbs | **Thm 1:** conductance comparison P_i(∂A) ≥ κ_i(G_i(∂A) − π(A∩K^c)) | Continuous models | Background on 2024–26 JRSS-B mixing theory |
| 23 | Chang, Lee, Luo, Sang, Zhou, *NeurIPS* 2022 | Multiple-try Metropolis for model selection | Mixing time smaller than MH by a factor equal to the number of trials (abstract read) | NO-n200 | Background |
| 24 | Barbieri, Berger, George, Ročková, *Bayesian Analysis* 16 2021 | Median probability model under correlation | **Thm 3.1** ("mini-theorems"): with q = 2, conditions under which the median model is or is not optimal | Fixed design | Complementary to **Prop 1 (T07)**, the HPM versus MPM decision |

**Certificates and verifiable guarantees for individual runs** (the task's second question):

| # | Citation, venue | What it provides | Per-run certificate? | Relation |
|---|---|---|---|---|
| C1 | Bertsimas, King, Mazumder, *AoS* 44 2016 | MIO for best subset. Lower bounds give a "certificate of suboptimality"; "heuristic methods do not provide such a certificate". Gap trajectories for n = 350, p = 64 | **Yes**: a global-optimality gap per run, for the L0 objective, at p ≈ 10² | Closest analogue of a certified HPM. A Bayesian HPM certificate at p = 500–1000 is not in the sample |
| C2 | Jacob, O'Leary, Atchadé, *JRSS-B* 82 2020 | Coupled chains give unbiased estimators with "finite variance, and a finite expected computing time" (Prop 3.1) | No: an unbiasedness guarantee, not a run certificate | Analogue of our Prop 2 |
| C3 | Biswas, Jacob, Vanetti, arXiv 1905.09971 (NeurIPS 2019, venue UNVERIFIED) | **Thm 2.5:** d_TV(π_t, π) ≤ E[max(0, ⌈(τ^(L) − L − t)/L⌉)]. A TV upper bound estimable from coupled runs | Estimated, not certified | Possible diagnostic for our Gibbs rounds |
| C4 | Vehtari et al., *Bayesian Analysis* 16 2021 | Improved R̂ | Diagnostic only | — |
| C5 | Wu, arXiv 2605.30722 (2026) | Spectral-gap certificates for flow-based independence MH. The covering certificate becomes "vacuous as dimension increases"; D = 2–20 | Yes, but continuous and low-dimensional | Shows that per-run certificates are a live 2026 topic, and none targets model spaces |
| C6 | Duan, arXiv 2604.21009 (2026) | A DC algorithm reaches the global mode of the marginal likelihood in latent precisions "under mild compact set conditions" | Global optimisation guarantee (continuous shrinkage), not a per-run certificate | Tangential. Not the model-space HPM |
| (11) | Papaspiliopoulos & Rossell 2017 | Exact top model by size under block-diagonal X′X | Exact by construction | See row 11 |

Bottom line: **no paper in the sample gives an a-posteriori, per-run, verifiable statement for a model-space posterior at
p in the hundreds**, such as "this run scored S₀" or "no unscored model can beat Ŝ". Per-fit certification is what O-CERT
C5 (box certificate) and the scored-set bookkeeping behind N200 aim at. It is a genuine gap, and it is also not yet run
on our side (API-N200 item 3).
