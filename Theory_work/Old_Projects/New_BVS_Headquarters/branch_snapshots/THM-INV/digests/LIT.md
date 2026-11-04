# THM-INV digest: LIT reports (LIT-SMC, LIT-MCMC, LIT-STAT, LIT-VENUE, LIT-PAR) plus API-POS

Working material, not reviewed. Sources: `origin/theory/<ID>:theory_campaign/<ID>/REPORT.md` for LIT-SMC, LIT-MCMC, LIT-STAT, LIT-VENUE, LIT-PAR and API-POS, plus `LIT-PAR/notes/02, 07, 08, 09` and the mapping in `Docs/THEORY_PRIORITIES.md`. I did not re-check any citation myself. All reference strings below are copied from the reports. Where I say "per the report" the claim is the report's, not mine. Verdict labels are verbatim where quoted; where a report gives no label I write its wording in quotes and mark it "(wording, no label)".

Report dates: LIT-SMC, LIT-MCMC, LIT-STAT, LIT-VENUE, API-POS are 2026-11-02; LIT-PAR is 2026-11-03.

Abbreviations: SVV = Štefankovič–Vempala–Vigoda; YWJ = Yang–Wainwright–Jordan; ZYVR = Zhou–Yang–Vats–Roberts–Rosenthal; CZ = Chang–Zhou; MS24 = Mathews–Schmidler 2024; MMS = Marion–Mathews–Schmidler; WSH = Woodard–Schmidler–Huber; CDG = Cérou–Del Moral–Guyader; WLH = Whiteley–Lee–Heine; SaM = Song–Liang split-and-merge.

---

## 1. Novelty verdict table (one row per our result)

"Read?" says what the LIT report states about whether it read the source. "Read" means the report says it read the source (extent in brackets). "UNVERIFIED" is the report's own word for second-hand.

| Our result (paper slot / registry) | Verdict, as the report gives it | Report | Citing source(s): exact reference and where it points | Read? (per report) |
|---|---|---|---|---|
| **Thm 1 / T03 (T03♯)** posterior consistency, BB(1,p), g = n, cap K = ⌊n/2⌋ | "**Modest extension** of Rossell (2022) and MGC (2015). Not standard for BB(1,p) / g = n / K ≍ n" (LIT-STAT confidence card). Headline: "a modest extension of known results, not a new phenomenon." | LIT-STAT | **Rossell**, *Bayesian Analysis* 17(2), 2022 (arXiv 1806.04071): §5.2 (BB spurious models), §5.4 Prop 9, (B1) needs p̄ ≪ min{n,p,nτ}. **Moreno, Girón & Casella**, *Stat. Sci.* 30(2), 2015: Thm 3. Closest architecture: **Castillo, Schmidt-Hieber & van der Vaart**, *Ann. Statist.* 43(5), 2015: Thms 1, 4, Cor 1 ("Complementary: neither implies the other"). Also Narisetty & He, *Ann. Statist.* 42(2), 2014 (Conditions 4.1–4.5); Johnson & Rossell, *JASA* 107, 2012 (Thm 2, no contradiction); Shin, Bhattacharya & Johnson (venue conflict, see §3 D9) | Rossell: read (Prop 1, Cors 1–2, §2.3, §5.2, §5.4 Prop 9, Lemma 3, supplement Lemmas S15, S21). MGC: abstract and Thm 3. CSvdV, Johnson–Rossell: local PDFs read. Narisetty–He: read, extraction partly garbled |
| Thm 1 / T03, second opinion | "**Standard in kind** ... High for novelty, low for correctness" (LIT-VENUE §5). Advice: "Present it as a needed lemma for our prior and cite YWJ/SBJ. Do not sell it." | LIT-VENUE | **YWJ Thm 1** (AoS 44(6) 2016, arXiv 1505.07925); **Shin–Bhattacharya–Johnson 2018** Thm 1/3; **Rossell–Abril–Bhattacharya**, *JRSS-B* 83 2021, Thm 2; earlier Johnson–Rossell 2012, Narisetty–He 2014 ("not re-read here") | YWJ, SBJ, RAB21 read. Johnson–Rossell and Narisetty–He explicitly not re-read. LIT-VENUE does not cite Rossell 2022 |
| **T03♯(3)**: P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] (also the 2E₀δ₁ term of Thm 4/T21 and Thm 5(0)) | "**KNOWN**": "Rossell (2022) Proposition 1 verbatim", "also holds for the MPM". Severity: "High for novelty, none for correctness" | LIT-STAT | **Rossell (2022), Bayesian Analysis 17(2), Prop 1**: P(k̂ ≠ t) ≤ 2E(1 − p(M_t \| y)), for HPM and MPM | Read (arXiv 1806.04071) |
| **T02(i♯)** exact BB(1,p) tail, size cutoff m♯_n | First draft: "the most distinctive statistical piece". After §12 addendum: "**Modest extension** ... new only in reaching a cap K ≍ n via the geometric size tilt. Low-to-medium confidence in the novelty, pending E1" | LIT-STAT | Nearest: Rossell (2022) §5.2 (BB(1,1), p̄ ≪ n). BB(1,p) is BB(1,1) times a Geometric(½) size tilt (PROVED, elementary, `bb11_vs_bb1p.py`). CSvdV (2.2) not applicable: BB(1,p) dimension ratio (p−s+1)/(2p−s) → ½ (PROVED, `bb_ratios.py`) | Rossell and supplement read. **Not read**: Martin, Mess & Walker (2017) (flagged for a stronger reviewer, E1). Castillo–vdV 2012 §2 lower bounds not read |
| **Prop D** (duplicate columns, lower bound for cutoff growth) | "I found no published analogue of either the upper bound ... or the lower bound (Prop. D) for a non-complexity BB prior" | LIT-STAT | none found | Based on targeted searches, "not a proof of absence" |
| **Prop 1 / T07** HPM = Bayes rule; size-only prior ceiling | "**Standard or folklore.** (i) and (ii)(c) are unstated but trivial". Detail: (ii)(a) "textbook"; (ii)(b) "folklore"; (ii)(c) "a trivial variant that I did not find stated"; (i) "a one-line observation ... **not stated** anywhere". "Prop 1 is correct bookkeeping, not novelty." | LIT-STAT | **Barbieri & Berger**, *Ann. Statist.* 32(3), 2004, Thm 1 and proof (coordinate-wise thresholding at ½; different loss). **Scott & Berger**, *Ann. Statist.* 38(5), 2010. **Berger, García-Donato & Pericchi**, arXiv:2603.19728v2 (Sept 2026): Lemmas 1–3, §2.6, "does not state T07(i)". Barbieri, Berger, George & Ročková, *Bayesian Analysis* 16(4), 2021 (Thm 3.1, venue UNVERIFIED in LIT-STAT; LIT-VENUE gives *Bayesian Analysis* 16 2021 via Crossref) | BB04: read (intro, Thm 1, proof, Cors). BGP: abstract, §2.6, WP/SP, Lemma 3. Scott–Berger: §3 passages. Barbieri et al.: read arXiv v2 Thm 3.1 |
| **Thm 2 / T22 (i)(ii)(iv)** deterministic start-mass clauses; composite block start | "**Threat to novelty of the start** (correlation-clustered exact blocks). Complementary: v3 adds the bridge to the exact posterior" (wording, no label) | LIT-PAR | **Papaspiliopoulos & Rossell**, *Biometrika* 104 2017 (arXiv 1606.03749): Props 3.3–3.4; exact only for block-diagonal XᵀX, otherwise "heuristic optimisation". LIT-VENUE: "Closest precedent for an exact (certified) HPM" under orthogonal blocks. Also Ma 2015 LIPS (*JASA*; arXiv 1403.2397): partial threat to "parallel + exact is new" | P&R: local PDF 12 + arXiv read (abstract, §4 heuristic per LIT-STAT). Ma: local PDF 13. P&R venue "UNVERIFIED by Crossref" (LIT-VENUE, LIT-STAT) |
| **Thm 2 / T22(iii) favourable + T27(i) masked** (start-law dichotomy; masking law π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}) | "**No prior art found** (G2). Strongest novelty claim relative to this literature" (LIT-STAT, for Thms 2, 3, 5(b)). LIT-VENUE G3: "Nobody proves that a natural, exactly sampleable start fails, and then proves which moves fix it" | LIT-STAT, LIT-VENUE | Nearest analogues, to be cited: **Atchadé**, arXiv:1903.11745 (*SIAM J. Math. Data Sci.* 2021, UNVERIFIED), Thm 6 (warm start containing truth; zero-start remark not proved). **YWJ App. A.2** (null truth, untruncated prior, PROVED slow mixing). **Hou–Wang–Atchadé** arXiv:2407.20580, Thm 4 (warm start p^{−α}). **CZ Thm 4** (restricted unimodal, start enters via log(1/π(x₀))). Mechanism label: **WSH**, *EJP* 14:780–804 (2009), Thm 3.1, Cor 3.1 (low persistence) | Atchadé: abstract, H2, Thm 6 read. WSH: EMIS PDF §1, §3 read. HWA: abstract, Thm 2 (LIT-STAT); Thm 4 (LIT-VENUE). CZ: abstract page, §3.1–3.3 |
| Thm 2, W7-SEP SEP(A)/(B): iid start draws need Q* = p^c n^{c/2}; moving off the start needed | "None of these is in the literature I read" (LIT-SMC G2); LIT-MCMC Θ4: "no BVS tempering separation exists (L2)". "A claim that tempering is *necessary* would be contradicted by the measured RW-MH hitting times on LH. Do not make it." | LIT-SMC, LIT-MCMC | WSH 2009 (framing); Mathews & Schmidler (μ⋆); Pozza & Zanella arXiv:2410.23174 Cor 1 (multiproposal speed-up ≤ K) | WSH, MS24 read. Pozza–Zanella abstract and Thm 1/Cor 1 statements read (venue UNVERIFIED) |
| **Thm 3 / T37 (Theorem A greedy repair, TD′, Lemma M, Prop GU, LH-LAT)** | "**Discovery on LH is unsurprising given YWJ/ZYVR**" (LIT-SMC T5). "O/I-in-spirit". Difference: "ours are deterministic and exact at finite n". LIT-MCMC: "Θ2 ... **GZ is a citation we must make**" | LIT-SMC, LIT-MCMC, LIT-VENUE | **YWJ, *AoS* 44(6):2497–2532 (2016)**: Lemma 4 (π(γ)/π(G(γ)) ≤ p^{−2} overfitted / p^{−3} underfitted) with Lemma 1 (Hamming-progress map G). **Gamarnik & Zadik**, arXiv:1711.04952v2 (2019; AoS 2022 companion UNVERIFIED): Thm 2.7 (local search from any k-sparse start recovers support, iid X, n ≥ C·k log p). **Zhou & Chang**, *AoS* 51(3):1058–1085 (2023): consistency of greedy local search on restricted space (LIT-VENUE: low–medium threat) | YWJ: arXiv v1 Thm 2, Lemmas 1, 4 read; "theorem numbers from arXiv versions, not journal". GZ: abstract, §1, LSA, Thm 2.7 read. ZC23: LIT-MCMC "theorem list only"; LIT-VENUE "abstract and §1 read" |
| **Thm 3 / T37 Theorem B (Gibbs-path repair), T38 repair routes** | "Outside that literature" (LIT-SMC G1); LIT-MCMC G1: "Nothing in the literature I read states a hitting-time-of-S₀ theorem under (1b)/(1c) only". Status of that gap claim: "CONJECTURE (literature), medium confidence" | LIT-SMC, LIT-MCMC | Nearest: GZ Thm 2.7; YWJ Lemma 4 | as above |
| **Thm 4 / T21** P(wrong report) ≤ P(no output) + 2E[π off truth] + P(truth never scored) | Split: the 2E₀δ₁ term "**Known**" (Rossell Prop 1, LIT-STAT). "Truth never scored" term: "elementary, but I did not find it stated for a best-ever-scored HPM" (LIT-STAT). LIT-VENUE: "Medium: the **idea** ... is published and informal. The exact inequality ... is not" and "A referee may call it bookkeeping" | LIT-STAT, LIT-VENUE | **García-Donato & Martínez-Beneito**, *JASA* 108 (2013), §4 (local file 28): "best visited model"; "the goodness of the estimation of the HPM only depends upon the ability of the methods to search for good models". **Clyde, Ghosh & Littman** (BAS), *JCGS* 20, 2011, Thm 1. Rossell (2022) Prop 1. LIT-SMC: outside SMC literature | GD–MB: local file read, §4. CGL: cited (LIT-VENUE says "pre-range"); extent of reading not stated |
| **Thm N200 (API-N200)** exact finite-n decomposition into posterior-miss + search-miss | "PROVED (candidate, elementary)" is our status; literature: "**Medium**"; no published split. LIT-STAT: "different kind of result (exact composition, measured Π(X))" and warns H5 | LIT-VENUE, LIT-STAT | Informal precedent: García-Donato & Martínez-Beneito 2013 §4. Threat to "first finite-n" wording: **Hou, Wang & Atchadé**, arXiv:2407.20580, **Thm 2** (Π̌(A_j\|D) ≥ 1 − 2(p^{−u(j+1)/2} + 2e^{−c₂n/4}); complexity prior u ≥ 2). LIT-VENUE gives venue as *AISTATS* 2026 (PMLR 300); LIT-STAT says "venue UNVERIFIED" | HWA local PDF 31, abstract + Thm 2 (LIT-STAT) |
| **Thm 5 / T38** (a), (b1-LH), (b1′-LH), (b2-LH) consistency of the reported HPM with SMC-BVS output | LIT-VENUE G1: "No SMC-BVS paper in the sample has an output theorem" (medium–high). LIT-MCMC: "**Novel for the paper's target and method. A corollary of YWJ/ZYVR/Chang–Zhou under *their* prior (API-POS)**" (high). LIT-SMC: "outside the existing SMC theory, not implied by it". LIT-PAR: "no published guarantee for SMC with a masked start on a correlated BVS family" (medium-high) | LIT-VENUE, LIT-MCMC, LIT-SMC, LIT-PAR | Closest: YWJ Thm 2/Cor 2; ZYVR Thm 1; CZ Thm 1/4; Atchadé Thm 6; Mathews & Schmidler (AAP 34(1B):1199–1223 (2024), doi:10.1214/23-AAP1989); Schäfer–Chopin 2013 (no theorem) | see per-source entries |
| **T38(a) favourable + T32(i)** as BVS instances of a general SMC template | "**TH6 (medium).** Mathews–Schmidler 2024 makes 'SMC needs only local mixing + bounded stage ratios' standard. T38(a) (favourable) and T32(i) should be framed as BVS verifications of that template." "Cite it; check whether T38(a)'s proof could simply invoke their Thm 1." (escalation 2: unresolved) | LIT-PAR | **Mathews & Schmidler**, *AAP* 34(1B) 2024, Thm 1 (arXiv 2208.06672) | read (abstract, §2, Thm 1, §6; LIT-MCMC) |
| **T38(c)** polynomial cost; "poly-time recovery on LH" | "**not a selling point on its own**"; "Do not headline cost" (LIT-VENUE, severity **High**). API-POS: "not new" with their priors | LIT-VENUE, API-POS | YWJ Thm 2, Cor 2; ZYVR Thm 1 (JRSS-B 84(5):1751–1784 (2022), doi:10.1111/rssb.12546); CZ Thm 1 | see §3 |
| **Thm 6 / T26** n-indexed consistency of Ẑ and PIPs (favourable regime) | **Conflict.** LIT-SMC G3: "T26/Thm 6 ... I found no analogue" (medium–high). LIT-VENUE: "Follows the standard pattern: SMC consistency/CLT (DC22) composed with posterior concentration. Medium" | LIT-SMC vs LIT-VENUE | LIT-VENUE: **Dau & Chopin**, *JRSS-B* 84 2022, Thms 1–2 (CLTs for waste-free SMC). LIT-SMC: Beskos–Jasra–Kantas–Thiery, *AAP* 26(2):1111–1146 (2016) supplies N → ∞ only | Dau–Chopin: local PDF 11; BJKT: arXiv 1306.6462 abstract, lemma |
| **Masked-regime Ẑ results (F-MASKPIP M1–M3)** | "Outside all general bounds (μ⋆, mixing)"; "sit where the general bounds are vacuous" (LIT-SMC) | LIT-SMC | MS24 (μ⋆); Marion–Mathews–Schmidler, *AoS* 51(3):1357–1375 (2023), doi:10.1214/23-AOS2295 | read |
| **Prop 2 / T12** unbiased Ẑ (frozen run), islandwise identity | "**Standard** ... except the negative items" (LIT-SMC card). "T12 + T31(i) standard." Negative items (pooled × pooled is not an identity; E[Ẑ \| completed] ≠ Z) are "genuinely non-standard" | LIT-SMC; LIT-VENUE ("Medium" threat: textbook SMC) | **Dai, Heng, Jacob & Whiteley**, *JASA* 117(539):1587–1600 (2022), doi:10.1080/01621459.2022.2087659 (arXiv 2007.11936): Ẑ unbiased; two-pass recipe for adaptive tuning. **Whiteley, Lee & Heine**, *Bernoulli* 22(1):494–529 (2016) (arXiv 1309.2918). **Del Moral (2004) book, UNVERIFIED**. LIT-VENUE: Del Moral 2004 Prop 7.4.1 "as cited by ZJA 2016" (Zhou, Johansen & Aston, *JCGS* 25 2016, l.352) | Dai: arXiv read. WLH: arXiv abstract and §1 (LIT-SMC); §5.1 (LIT-PAR). Del Moral 2004: not read by any report |
| **T31(i)** Ẑ-weighted island pooling consistent as R → ∞ at fixed N (islandwise E[Ẑ_r·PIP̂_rj] = Z·PIP_j) | LIT-PAR TH2 **(high)**: "T31(i) is standard". LIT-SMC T3: "Islandwise averaging is standard (#4, #6)." Only ours: "unbiasedness of v3's Ẑ under the frozen calibration (P6/P7)" | LIT-PAR, LIT-SMC | **Whiteley, Lee & Heine (2016) §5.1**; **Dai–Heng–Jacob–Whiteley (2022) eq. (4.8)** via Andrieu–Doucet–Holenstein (2010) (**not read**, via Dai et al.). **Liang, Lohani, Lukens, Kirby, Searles & Law**, arXiv 2402.06173v2 (2024; peer review UNVERIFIED), Thm 3.1: MSE ≤ C_φ/(NP) (TH3 medium). LIT-SMC also cites **Vergé, Dubarry, Del Moral & Moulines**, *Stat. Comput.* 25(2):243–260 (2015), doi:10.1007/s11222-013-9429-x | WLH §5.1, Dai §4.2, Liang v2 read (LIT-PAR). Vergé: arXiv abstract and statements (LIT-SMC). See §3 D5 on Vergé |
| **"0.05·Ẑ is a 95% lower bound"** (T31(i)/Prop 2 Markov bound) | "**I**" = implied; "standard; cite it" | LIT-SMC | **Grosse, Ghahramani & Adams**, arXiv:1511.02543 (2015): "Pr(Ẑ > aZ) < 1/a" (a = 20) | read (§ on stochastic lower bounds) |
| **O-STAGES Theorem G(i)**, Lemma 0 (Φ = Rényi-2), Lemma 1 (greedy ESS grid shortest valid grid) | "**Threat: ... already in the literature**"; "The paper must cite SVV and present G(i) as known." G(ii) (pilot-refinement sandwich) = "a routine v3-specific extension"; G(iii) COVER transfer v3-specific. Forward half of Lemma 1 also in Beskos et al. 2016; Schäfer–Chopin "assert it" | LIT-SMC | **Štefankovič, Vempala & Vigoda**, arXiv cs/0612058 (2006); FOCS'07 183–193; *J. ACM* 56(3):1–36 (2009), doi:10.1145/1516512.1516520: Def 2.3 (B-Chebyshev schedule), text after Thm 4.1 "The optimal Chebyshev cooling schedule can be obtained in a greedy manner". Beskos et al. *AAP* 26(2) 2016 (Lemma: ESS monotone). Schäfer & Chopin, *Stat. Comput.* 23(2):163–184 (2013), §4.3 | SVV: arXiv PDF read; "journal version not read". Beskos: arXiv abstract, lemma. Schäfer–Chopin: local PDF read |
| **O-STAGES item 4**: dense limit √c·T* → L = ∫ sd_{q_φ}(d)dφ | "**Known analogue**" / "NOT new" | LIT-SMC, LIT-PAR (agree) | **Syed, Bouchard-Côté, Chern & Doucet**, arXiv:2408.12057v2 (Dec 2025): Thm 3, lim T·Var[Ẑ/Z] = E(φ)/N ≥ Λ²/N; Λ = L exactly (LIT-PAR n08, eq. (25)). LIT-PAR also: Gelman–Meng 1998 (**UNVERIFIED**, via Syed et al.). LIT-VENUE gives venue as *JRSS-B* 2026 | Syed: local PDF read (LIT-SMC, LIT-PAR). Gelman–Meng: not read |
| **O-STAGES Theorem M** (masked crossing T* = log₂A₀ + O(1)); **Theorem F** (T* = O(1) favourable); O(log log n) on LH masking | LIT-SMC: "were not found in anything I read. They look new as BVS-specific statements, but they are elementary given SVV." Confidence "plausibly new, elementary", "medium". LIT-PAR: "not in the literature" ("Λ = L ≤ π while T* → ∞ is a clean new observation") | LIT-SMC, LIT-PAR | Contrast references: SVV Thm 4.1 (O(√(ln A)·ln n·ln ln A), weaker than Thm M on the two-state family); Chopin et al. / Beskos–Crisan–Jasra, *AAP* 24(4):1396–1445 (2014) (T grows with d). LIT-SMC escalation 2: check SVV proof's B-dependence | SVV read (arXiv). "needs a wider search in the counting/annealing literature" |
| **O-PW2 Theorem A** (exact variance identity) | "**Same kind as CDG 2011 Thm 1.4** (exact, assumption-free)"; "present Theorem A as 'a form of the exact Feynman–Kac second-moment decomposition ... specialised to v3', not as new." Status: "CONJECTURE-level reading (forms compared, not derived)" | LIT-SMC | **Cérou, Del Moral & Guyader**, *AIHP* 47(3) (2011) 629–649, **Thm 1.4** (α = 0 decomposition), Thm 1.5 (one-sided). Also Del Moral–Doucet–Jasra, *JRSSB* 68 (2006) 411–436, Prop 2 | CDG numdam PDF read, p. 633 (Thm 1.4 quoted "as I parse the pdftotext layout"). DMDJ local PDF read. Del Moral 2004 not read |
| **O-PW2 Theorems B, C** (two-sided O(N^{−3/2}) remainder; constants from v3 primitives; counterexample "PW2 with a_t = χ²_t") | "may carry novelty"; B "plausibly closest to CDG Thm 1.5, but with different premises". Under idealisation, PW2-type product formulas are in Dai et al. (iv) and Syed et al. Thm 1(a) | LIT-SMC | CDG Thm 1.5; Dai et al. 2022; Syed et al. Thm 1(a) | escalated: "line-by-line comparison" not done |
| **Prop M** (naive merge of block-wise fits) | "**Known phenomenon**, cleanly formalised": "a clean COUNTEREXAMPLE for motivation, not a contribution" (Medium for novelty) | LIT-STAT | **Papaspiliopoulos & Rossell**, *Biometrika* 104(2), 2017 (venue UNVERIFIED): block-diagonal exactness; omitted-variable bias. Caveat: "Prop M refutes a naive union, **not** Song–Liang's method (A-DRAFT's own caveat)" | P&R: arXiv 1606.03749v2, abstract and §4 heuristic. Song–Liang: **UNVERIFIED**, second-hand via A-DRAFT §1.2 |
| **LIT-PAR G4: SaM-type splitting fails on an LH-like masked pair** (a LIT-PAR result, not ours) | "COUNTEREXAMPLE (numerical, reproducible) ... + PROOF SKETCH (analytic)": exact posterior recovers S₀ in 20/20; SaM 5/318 separated splits, 265/282 together | LIT-PAR | **Song & Liang 2015**, *JRSSB* 77(5):947–972, Thm 5 (misspecified-subset), (B1), **read from Liang's slides**, https://www.stat.purdue.edu/~fmliang/STAT598Purdue/partI4.pdf ; "paper paywalled" | Slides only. "The step 'PIP → 0' is not verified against the paper." Escalation 1 |
| **Certificates (O-VCERT C1–C6; O-CERT C5 box certificate; Lemma M monotone bounds; posterior-miss certificates)** | LIT-SMC G5: "novel in kind", conf "medium", "cheap to settle: low (the BVS stochastic-search literature was not searched)". LIT-VENUE G4: "Open everywhere. **Could** become a distinctive contribution"; "not yet run on our side (API-N200 item 3)" | LIT-SMC, LIT-VENUE | Nearest: **Grosse–Ghahramani–Adams** BDMC arXiv:1511.02543 (needs exact posterior samples for the upper side). **Bertsimas, King & Mazumder**, *AoS* 44 2016 (MIO certificate for L0, p ≈ 10²). Papaspiliopoulos–Rossell (exact by construction, block-diagonal). Wu arXiv 2605.30722 (continuous, D ≤ 20). Not searched: Hans–Dobra–West 2007 | BKM: arXiv 1507.03133 read. Wu: abstract only. BDMC: read |
| **Islands + exact block start + SMC bridge + unbiased Ẑ, as a composition** | LIT-PAR (c): "Its pieces exist separately (Papaspiliopoulos–Rossell; Schäfer–Chopin), but we found nothing that composes them with theorems." | LIT-PAR | Schäfer–Chopin 2013 (parallel tempered SMC for BVS; no theorem); P&R 2017; Ma 2015 | local PDFs read |
| **Parallel scaling / S-DEPTH (depth = T·L_r·(p+B+2) score evaluations; width R·N; error ∝ 1/R at fixed N)** | "high (accounting)"; masked-regime single-island Var(Ẑ/Z) bound "**OPEN**". TH7 (self): v3's per-round depth is Θ(p), not O(1) | LIT-PAR | WLH 2016; Dai et al. 2022; Liang et al. 2024; Syed et al. NRPT, *JRSSB*, arXiv 1905.02939 | read (LIT-PAR notes 03) |
| **T38 route via general SMC finite-sample theory** (a result that would be a *replacement*, not ours) | "Plugging in is blocked by mixing times" | LIT-SMC, LIT-VENUE, LIT-MCMC | **Le Fay, Chopin & Vihola**, arXiv:2604.03352v2 (Apr 2026): LIT-SMC and LIT-MCMC cite Thms 2.3/3.2; LIT-VENUE cites Thm 2.3 and Thm 3.4 (see §3 D8). LIT-SMC: "no finite-sample complexity bounds for normalising constants have previously been derived" is the paper's own claim | local PDF 24 read |
| **Lean machine-checked proofs (T07, T21)** | "Novel in this literature, but not a statistical contribution. Venue impact uncertain." | LIT-VENUE | none in sample | n/a |
| **Study-scale (n = 200) finite-n relevance of Thm 1** | "No asymptotic theorem in the table has force at n = 200"; YWJ (E) fails for every s₀ ≥ 1; T03♯ thresholds ≈ 2·10⁶ | LIT-STAT, LIT-VENUE, LIT-PAR | YWJ condition as quoted in ZYVR Thm S2 | see §3 D10 |

Other LIT-originated items (not ours, but relevant to the ledger): **Prop OB** (LIT-MCMC): "R/M → 0 for the paper's prior when p ≫ √n", status (i) PROVED, (ii)–(iii) "PROOF SKETCH"; numerical check at study scale 12/12 data sets R < M (`results/ob_check.md`, study-like generator, not the study's own). **Prop U** (API-POS): underfitted models never local modes on LH-G, PROOF SKETCH.

---

## 2. Every result whose novelty is challenged

Each entry names the challenger and the report that raised it.

1. **Thm 1 / T03♯ as a whole**: Rossell 2022 and Moreno–Girón–Casella 2015 make it "a modest extension" (LIT-STAT H2, severity "Medium–High", raised from Medium after §12); "standard in kind" (LIT-VENUE, High for novelty).
2. **T03♯(3)**: KNOWN, Rossell 2022 Prop 1 verbatim (LIT-STAT H1, High for novelty).
3. **T02(i♯) exact BB(1,p) tail**: narrowed to "modest" because BB(1,p) = BB(1,1) × Geometric(½) tilt (LIT-STAT §12). Pending check of Martin–Mess–Walker 2017.
4. **"Anchored SE" wording in Thm 1**: Narisetty–He Δ_n(K), Rossell v_tm show anchored size-restricted identifiability is standard (LIT-STAT H3, Low to medium).
5. **Prop 1 / T07**: standard or folklore (LIT-STAT); Barbieri–Berger 2004 caveat that HPM is not generally the optimal predictive model (H7).
6. **T22 start (clustered exact blocks)**: Papaspiliopoulos–Rossell 2017 (LIT-PAR "threat to novelty of the start"); Ma 2015 (partial).
7. **Thm 2 favourable/masked dichotomy**: must cite Atchadé Thm 6 and YWJ App. A.2 (LIT-MCMC Θ3); CZ Thm 4 + API-POS Prop U make "masked regime is solvable" a corollary on LH-iid under YWJ prior (LIT-MCMC Θ1, "strongest").
8. **Thm 3 / T37 / Lemma M / Prop GU**: YWJ Lemma 4 + Lemma 1 (LIT-SMC T5, headline 5); Gamarnik–Zadik Thm 2.7 (LIT-MCMC Θ2); Zhou–Chang 2023 (LIT-VENUE, Low–medium).
9. **Thm 4 / T21**: 2E₀δ₁ term known (Rossell); "bookkeeping" risk and informal precedent García-Donato–Martínez-Beneito 2013 (LIT-VENUE, Medium).
10. **Thm N200 / any "first finite-n" wording**: Hou–Wang–Atchadé Thm 2 (LIT-STAT H5, Medium).
11. **Thm 5 / T38(c) polynomial cost; poly-time recovery on LH**: YWJ, ZYVR, CZ (LIT-VENUE High; API-POS "not new").
12. **T38(a), T32(i)**: may reduce to Mathews–Schmidler Thm 1 (LIT-PAR TH6, escalation 2).
13. **Thm 6 / T26**: LIT-VENUE "standard pattern" (Medium) versus LIT-SMC "no analogue" (conflict, §3 D6).
14. **Prop 2 / T12 / T31(i)**: standard (Dai et al., WLH, Grosse et al., Andrieu–Doucet–Holenstein via Dai; Liang et al. 2024 for "parallel strong scaling").
15. **O-STAGES Theorem G(i), Lemma 0, Lemma 1**: SVV (known). **Item 4**: Syed et al. Λ (known analogue). Theorem M/F: not found, "elementary given SVV".
16. **O-PW2 Theorem A**: CDG 2011 Thm 1.4 (same kind; not derived). Thm B/C: possibly new.
17. **Prop M**: known phenomenon (Papaspiliopoulos–Rossell; omitted-variable bias).
18. **Certificates**: novelty unchecked against BVS stochastic-search certificate literature (Hans–Dobra–West 2007 not searched; BKM 2016 is the L0 analogue).
19. **Wording claims** (not results): "methods with guarantees are sequential" is FALSE (LIT-PAR); "first parallel exact BVS", "no analogue speed-up for MCMC", "depth = T" without per-round factor should be avoided (LIT-PAR §3.3 item 5); BB(1,p) choice challenged on referee grounds by Berger–García-Donato–Pericchi 2026 §2.6 and Castillo–van der Vaart 2012 (LIT-STAT H8; a prior-choice point, not a theorem).

---

## 3. Disagreements and discrepancies between reports (quoted)

### D1. API-POS vs LIT-MCMC on whether rapid-mixing theorems cover our target (YWJ 2016, ZYVR 2022, Zhou–Smith 2022)

Agreement first: neither says any published rapid-mixing theorem covers the paper's own target as stated.
- API-POS §1.3: "For the paper's own target, neither theorem applies as stated ... So no published theorem covers the SMC-BVS output on LH. This is a formal gap, not a substantive one."
- LIT-MCMC §0.1: "So: on LH, 'rapid mixing' is not certified by any published theorem for our target. 'Fast discovery' is supported by the landscape (API-POS Prop. U, PROOF SKETCH) but is not stated as a theorem anywhere I read."

Where they differ (degree and mechanism, not the sign of the applicability conclusion):
- **API-POS locates the failure on the prior side only and expects the landscape condition to hold.** API-POS §10: "The mismatches are all on the *prior* side (g, κ, cap) and the regime side (p ≥ n). None is on the design side." R3(iii): "the failure in (ii) concerns prior strength and the size cap, not the posterior landscape. A YWJ-style canonical-path or drift analysis for the paper's prior on LH would very likely succeed (CONJECTURE, supported by §6)." Bottom line §7: "**almost certainly yes for ours** (Prop. U plus enumeration; not a published theorem)".
- **LIT-MCMC finds a structural obstruction to the unimodal-ratio route itself** (not just prior strength): "the **sufficient condition R > M fails at n = 200 and n = 1,600** (c = 1 and c = 2), and **R > M² (informed samplers) fails at every n tested, up to 102,400**" (exact enumeration, p = 16, 20; `results/rz_lh.md`). And at study scale: "R < M holds in 12 of 12 data sets, by a factor of at least p^{0.87}. This is a COUNTEREXAMPLE to the applicability of those theorems." Prop OB: "the hypothesis R > M of Chang–Zhou Thm 1/4, Zhou–Smith Assumption 1 (ν > α), and the analogous c₀ = 2 in ZYVR's (1a) **cannot hold for the paper's prior when p ≫ √n**." LIT-MCMC §3.2 also notes that where R ≤ M "no gap bound is available from the literature".
- **Same side of the ledger, different emphasis.** API-POS: "With their own priors, both theorems apply to LH in the iid realisation ... so polynomial-time recovery of S₀ on LH is **not new**" and "The referee's suspicion (M6) is correct in substance." LIT-MCMC Θ1 "Defence: OB shows these theorems cannot be applied to our prior in p ≫ √n ... That defence is a formal gap, not a substantive one, which is API-POS's own verdict." LIT-MCMC adds a distinction API-POS does not draw: OB "does not say the chain mixes slowly ... What OB says is that no published unimodal-ratio theorem can certify our target in the study's regime"; the overfitted-side direction "matters for mixing, not for discovery".
- **A real tension in framing the "unique mode" evidence.** API-POS: "S₀ is the **unique local mode** under add/delete/swap moves on the whole capped space" (R > 1). LIT-VENUE uses this to say CZ's condition covers LH: "It also follows from Chang–Zhou's unimodality condition R > M, since on LH S₀ is the unique local mode" (LIT-VENUE §1.3). LIT-MCMC's computation shows unimodal does not give R > M: "R > 1 everywhere (unique mode S₀). R > M fails at n ∈ {200, 1600}". LIT-VENUE §3 row 3 itself says "R > M is not checked" and escalation 1 asks to check it. So LIT-VENUE's headline sentence is contradicted by LIT-MCMC (which came later in the same campaign day; LIT-VENUE flagged it as an open escalation).
- **Which theorems each report actually read.** LIT-MCMC read ZYVR (local PDF, Condition 1, Thm 1, Remark 2, §7), YWJ (arXiv v1, §3.2–3.3, App. A.2), Chang–Zhou (§3.1–3.3, Thms 1, 2, 4, 5, Cor 5, Example 3), Zhou–Smith (Assumption 1, Lemma 3, Thm 1). LIT-STAT read YWJ only second-hand via Zhou et al. Thm S2 ("UNVERIFIED"), LIT-SMC took ZYVR "via API-POS's audit, not re-read". API-POS read arXiv v1 of YWJ and arXiv v3 of ZYVR in detail but flags that "Theorem numbers are from arXiv v1 and are not checked against the journal version."
- **Zhou–Smith 2022** (AISTATS, PMLR 151, informed importance tempering) is covered only by LIT-MCMC (row 4): "Assumption 1 is R ≥ p^ν > M = p^α. On LH it fails at n ≤ 1,600." API-POS does not treat it.
- **Numbers that do not line up directly.** API-POS Z4/§6 gives ZYVR c₀ (1a) ≈ −0.30 / 1.12 / 1.88 / 1.87 (c = 1, n = 200 … 102,400) in log_p units at fixed p = 16, noting "With p fixed, log_p units make c₀ look larger"; LIT-MCMC §2.3 heuristic c₀ ≈ log_p(2√n/k) ≈ 0.1 at the study scale, "a heuristic, not checked", and says it underestimates measured log_p R_ub (0.2–0.5). API-POS also says c₀ ≈ ½ at p ≍ n. These are different regimes and units, not contradictory, but a reader should not mix them.
- **YWJ's size-cap constant is quoted three ways.** LIT-STAT (via ZYVR Thm S2): "s₀ ≤ n/(32 log p) − C₀/4", so "s₀ ≤ 1.006 (p = 500) or 0.905 (p = 1000)". LIT-PAR: "'s₀ log p ≤ n/32' ... admits no s₀ ≥ 1 at n = 200, p = 1000". LIT-MCMC: "s₀ log p/n = 0.43–0.48 against their ≤ 1/32-type constants". API-POS (YWJ arXiv v1 D(s₀)): "n/(8C₀K log p) − 16L̃σ₀²". Conclusion ("fails at n = 200") is the same, but the constants differ across the YWJ original and ZYVR's restatement. LIT-STAT E2 asks to check YWJ directly.

### D2. LIT-MCMC vs LIT-VENUE on Chang–Zhou Thm 4 severity
- LIT-MCMC Θ1: "**(strongest). Chang–Zhou Thm 4 together with API-POS Prop. U.** ... any start costs only log(1/π(x₀)) extra."
- LIT-VENUE §5 last row: "'Moving off the start is needed' (W7-SEP): HWA Thm 4 and CZ26 Thm 4 already treat warm-start mixing ... **Low** ... Ours is the converse: a warm start is *provably absent*."
- Venue citation also differs: LIT-MCMC "Chang & Zhou, arXiv:2404.03867v2 (2025), 'Accepted by Bernoulli' (listing)"; LIT-VENUE "Chang & Zhou, *Bernoulli* 32 2026 (arXiv 2404.03867)".

### D3. LIT-PAR vs LIT-VENUE on the parallel-BVS gap claim
- LIT-VENUE never evaluates parallelism. A grep of its report finds "parallel" only in the Hou–Atchadé row. Its gaps are G1–G5 on output theory, error decomposition, masking lower bound, certificates, Lean. There is no direct contradiction with LIT-PAR.
- Indirect tension: LIT-VENUE §1.2 characterises the top-venue BVS papers as "an explicit polynomial mixing-time bound for the sampler they propose" and treats poly-time recovery as the threat to T38(c) (High). LIT-PAR goes further and says these results (ZYVR with parallel neighbour scoring) falsify the sentence "methods with guarantees are sequential": "The literal sentence ... is FALSE in the work/depth sense. Do not print it." LIT-VENUE's reading would not have caught this.
- LIT-VENUE, for Schäfer–Chopin 2013, says "Ancestor of our method. Confirms that SMC-BVS has no output theory." LIT-PAR for the same paper: "**Threat to novelty** of 'parallel SMC for BVS'. Do not repeat its claim 'No analogue speed-up ... in the context of Markov chains'". Complementary, not conflicting.
- Related gap-claim difference: LIT-VENUE notes (§8) "'no theorem for the output of SMC-BVS' should be checked by a second literature run with a wider net: particle stochastic search (Shi–Dunson), South–Pettitt–Drovandi BA 2019". LIT-SMC said two web searches found no 2023–2026 SMC-for-BVS theory paper. LIT-PAR does not mention these two.

### D4. LIT-SMC vs LIT-PAR on island pooling
- **Both** call T31(i)/islandwise averaging standard. The sources differ.
  - LIT-SMC: "#4 Dai ... (v) Averaging R independent runs is unbiased"; "#6 Vergé et al. ... Applies to v3 islands, since R independent islands is the non-interacting case ... **O** with Prop 2's islandwise identities. Those are the non-interacting special case and standard."
  - LIT-PAR (row on Vergé et al.): "Independent islands with **plain** averaging: bias O(1/N₁), not reduced by more islands; variance ∝ 1/(N₁N₂) ... Contrast: our pooling is Ẑ-weighted, not plain."
  - So LIT-SMC treats Vergé as covering our islandwise identities, whereas LIT-PAR says Vergé's non-interacting case is plain averaging and our pooling is a different estimator, standard instead through WLH §5.1 and Dai eq. (4.8). Neither verdict changes ("standard"), but the citing source for the Ẑ-weighted pooling should be WLH/Dai, with Vergé as contrast, per LIT-PAR.
- LIT-SMC also says "Pooled × pooled is not an identity ... was not found stated" and "E[Ẑ | completed] ≠ Z" are the non-standard items. LIT-PAR does not address these.
- WLH depth of reading: LIT-SMC "arXiv:1309.2918 read: abstract and §1"; LIT-PAR read §5.1 and quotes it.

### D5. Mathews–Schmidler μ⋆: "polynomially small" vs "exponentially small"
- LIT-SMC #18: "On LH, A₀ = c log p + (c/2) log n, so μ⋆ is polynomially small: borderline, not excluded. In ST (dilution) it is far smaller."
- LIT-MCMC #18: "µ⋆ ≤ π₀(S₀ basin) ≍ n^{−c/2}, so N must grow polynomially in n. Not a fixed-N guarantee"; §7: "It gives N ∝ 1/µ⋆ ≈ n^{c/2}, polynomial, so in principle usable."
- LIT-PAR #2.3: "Under a masked start μ⋆ is **exponentially small**, so the bound is useless there." and headline 6(b): "Generic SMC complexity bounds degrade exponentially there through μ⋆."
- LIT-SMC headline 4: "π₀(S₀) ≈ e^{−A₀}". The sources can be reconciled (exponential in A₀, polynomial in n, p on LH), but LIT-PAR's wording is stronger than LIT-SMC/LIT-MCMC on LH.

### D6. Thm 6 / T26 novelty
LIT-SMC G3: "I found no analogue" (confidence medium–high); LIT-VENUE §5: "Follows the standard pattern: SMC consistency/CLT (DC22) composed with posterior concentration. **Medium** ... Supplement."

### D7. Prop 2 / T12 unbiasedness source
- LIT-SMC: "Unbiasedness of Ẑ is classical (Del Moral 2004 book, **UNVERIFIED**, not read)."
- LIT-VENUE: "Del Moral 2004 Prop 7.4.1, as cited in ZJA16 l.352".
- LIT-PAR: Andrieu–Doucet–Holenstein 2010 "not read; cited via Dai et al.".
- Nobody read Del Moral (2004). The proposition number 7.4.1 comes only from LIT-VENUE's reading of Zhou–Johansen–Aston.

### D8. Le Fay–Chopin–Vihola theorem numbers
- LIT-SMC: "recalls MMS (Thm 2.3) ... waste-free analogues (Thm 3.2) ... tempering ... Thm 5.2 ... Thm 6.2".
- LIT-MCMC: "Thms 2.3/3.2".
- LIT-VENUE: "**Thm 2.3** ... **Thm 3.4:** with spectral gap γ and χ̄² = 2, P ≥ 2560T/(γε²) gives |Ẑ_T/Z_T − 1| < ε w.p. ≥ 3/4".
- LIT-SMC and LIT-MCMC both read the local PDF 24, as did LIT-VENUE and LIT-PAR (header and parallel remarks only). The theorem number for the waste-free spectral-gap result is 3.2 in two reports and 3.4 in one.

### D9. Venues and references that differ across reports (do not copy blindly)
- **Shin, Bhattacharya & Johnson 2018**: LIT-STAT "JASA 113, 2018"; LIT-VENUE "*Statistica Sinica* 2018". LIT-VENUE says it checked venues through Crossref (`scripts/crossref.sh`); LIT-STAT does not report a Crossref check.
- **Chang & Zhou**: see D2.
- **Hou–(Wang–)Atchadé** arXiv:2407.20580: LIT-STAT "(2024; INDEX says 2026, venue UNVERIFIED)"; LIT-VENUE "*AISTATS* 2026 (PMLR 300 ...)" from a search result, not a primary page. LIT-STAT lists authors "Hou, Wang & Atchadé"; LIT-VENUE "Hou, (Wang,) Atchadé".
- **Syed et al. Optimised annealed SMC**: LIT-SMC and LIT-PAR "arXiv:2408.12057v2 (Dec 2025)"; LIT-VENUE "*JRSS-B* 2026".
- **Mathews & Schmidler 2024**: LIT-SMC "*AAP* 34(1B):1199–1223 (2024), doi:10.1214/23-AAP1989"; LIT-MCMC "*AAP* 34(1):1199–1223 (2024)"; LIT-PAR "AAP 34(1)".
- **Papaspiliopoulos & Rossell 2017**: venue "UNVERIFIED" in LIT-STAT and LIT-VENUE (Crossref did not return it), stated as Biometrika 104(2) in LIT-STAT and Biometrika 104 in LIT-PAR/LIT-VENUE.
- **Barbieri et al. 2021 *Bayesian Analysis* 16(4)**: LIT-STAT "venue UNVERIFIED"; LIT-VENUE (Crossref) 16 2021.
- LIT-MCMC (ZYVR): "*JRSS-B* 84(5):1751–1784 (2022)" and API-POS (Crossref/records) the same, with five authors including Rosenthal. LIT-STAT lists ZYVR "venue from INDEX, UNVERIFIED".

### D10. Song–Liang's condition: different readings
- The THM-INV task text says SaM's stage-1 screening needs |cov(x_t, y)| > 0 for every true predictor (Condition 5). LIT-PAR instead reads the guarantee as a nonzero **within-split projection coefficient** (Thm 5 / (B1) "identifiable"; "CHECK in paper"), from Liang's slides, not from the paper. LIT-STAT only has Song–Liang second-hand ("Sure screening (Thm 3), misspecified-posterior consistency (Thm 4)"). The SL digest (separate) should settle this. See §5.
- LIT-STAT's theorem numbers (Thm 3 sure screening, Thm 4 misspecified) differ from LIT-PAR's (Thm 3 sure screening, Thm 4–5 misspecified subset; Thm 5 quoted).

### D11. Prop M vs the SaM counterexample
LIT-STAT H9: "Do not claim it refutes Song–Liang (A-DRAFT's own caveat)." LIT-PAR G4 claims a numerical COUNTEREXAMPLE to "SaM recovers S₀" on an LH-like design from its own implementation of SaM-from-slides (halves, Stage I exact posterior per half, PIP > 0.5; "not the exact v3 target: no unit ridge, improper σ prior"), and the analytic step is "not verified line by line". These can both be true, but the paper cannot cite Prop M against SaM and G4 in the same breath without the caveat.

### D12. T03/T02(i♯) severity inside LIT-STAT
LIT-STAT headline 4 says "The exact BB(1,p) tail (T02(i♯)) is the most distinctive statistical piece" and then carries an inline "Correction after a later check (§12)" that downgrades it to "modest". The report's confidence card uses the downgraded wording. Use the downgraded one.

---

## 4. Coverage of the proposal's five literature themes

Legend: R = report says it read the source; U = report says UNVERIFIED / second-hand.

### Theme 1. Split-and-merge Bayesian variable selection (Song & Liang 2015; Gutierrez & Guhaniyogi 2022)

Covered by: **LIT-PAR** (main), **LIT-STAT** (one row), API-POS (no).
- **Song & Liang 2015**, *JRSS-B* 77(5):947–972: LIT-PAR read "Theorem statements from author slides; paper paywalled" (U for the paper; slides R). Slides: https://www.stat.purdue.edu/~fmliang/STAT598Purdue/partI4.pdf. LIT-STAT: "**UNVERIFIED** (second-hand via A-DRAFT §1.2)". LIT-SMC, LIT-MCMC, LIT-VENUE: not covered. LIT-PAR "Not attempted: reading the Song–Liang paper itself".
- **Gutierrez & Guhaniyogi 2022** (DFP), *Technometrics* (venue UNVERIFIED): LIT-PAR read the technical report UCSC-SOE-21-04 (R); "Supplement not read". LIT-PAR: pseudo-posterior "arbitrarily close to the full posterior as the data size grows", assuming plug-in estimators consistent ("validated empirically").
- Other split/feature-splitting works read by LIT-PAR: Wang, Dunson & Leng 2016 DECO (arXiv 1602.02575; R); Coats, Davies & Gupta 2026 (arXiv 2609.20000; R; no theorem; F1 0.126 at ρ = 0.99); Papaspiliopoulos & Rossell 2017 (R); Ma 2015 LIPS (R).
- **Missing**: the Song–Liang paper itself (all its conditions, Thm 3/5, §6 complexity) is not verified by any LIT report; the SaM (B1)/Thm 5 reading is an "our reading ... CHECK in paper"; Song & Liang's own conditions on correlation (Condition 5 per the task text) are not extracted by a LIT report. No report treats SaM's §6 complexity or MAP consistency. No report covers Song–Liang's 2014 predecessor, which DECO cites (via DECO critique: "Song and Liang, 2014").

### Theme 2. Composite likelihood and approximate posterior calibration (Ribatet et al. 2012; Frazier et al. 2023; Pauli et al.; Varin et al.)

**Not covered.** A grep of all five LIT reports, API-POS and the LIT notes finds no mention of Ribatet, Frazier, Pauli, Varin, or "composite likelihood". The one hit in LIT-SMC was Paulin–Jasra–Thiery (an unrelated name). Closest adjacent items (not this theme): Hou–Wang–Atchadé one-step Laplace approximate posterior (LIT-STAT, LIT-VENUE); Rossell–Abril–Bhattacharya ALA (LIT-VENUE, "approximate Laplace approximations"); Ray & Szabó and Yang–Pati–Bhattacharya VB contraction (LIT-PAR, LIT-VENUE). "Composite start" in our method is a product of block marginal tables, but no LIT report relates it to composite likelihood or calibration of composite posteriors.

### Theme 3. Divide-and-conquer Bayesian computation (consensus MC, WASP, embarrassingly parallel MCMC, Lindsten et al. 2017)

Covered by: **LIT-PAR** (main), **LIT-SMC** (Lindsten, Kuntz), LIT-VENUE (no).
- **Scott et al. 2016** consensus Monte Carlo, *IJMSEM* 11:78–88: LIT-PAR "abstract only; full text NOT read" (U). No theorem seen.
- **Srivastava, Li & Dunson 2018** WASP, *JMLR* (arXiv 1508.05880): selected passages and theorem statements read (R); journal volume "from memory: UNVERIFIED" (notes 04).
- **Minsker et al. 2017** M-posterior, *JMLR* (arXiv 1403.2660): Thm 2.1, 3.1 read (R).
- **Zhang, Lam & Lin 2018**, *CSDA* 127 (arXiv 1610.06194): Thms 1–3 read (R); fixed finite non-nested model set.
- Li, Kang, Liu & Wu 2022, *Electron. Res. Arch.* 30(5): R; no theorem.
- **Lindsten, Johansen, Naesseth, Kirkpatrick, Schön, Aston & Bouchard-Côté**, *JCGS* 26(2):445–458 (2017), doi:10.1080/10618600.2016.1237363: LIT-SMC read arXiv:1406.4993 abstract only; "**statements not verified here**" (U for theorems). LIT-PAR notes 03 read parts.
- **Kuntz, Crucinio & Johansen**, *AAP* 34(1B):1469–1523 (2024): LIT-SMC arXiv abstract only.
- Embarrassingly parallel MCMC as a named work (the proposal's item): not in any report. Parallel SMC islands: Vergé et al. 2015, WLH 2016, Dai et al. 2022, Liang et al. 2024 (R).
- **Missing**: the embarrassingly parallel MCMC literature; consensus MC full text; Lindsten/Kuntz journal versions and theorem statements ("Not attempted" in LIT-PAR); the DFP supplement. LIT-PAR's blanket conclusion is that data-splitting guarantees are fixed-p and say nothing about discrete model spaces.

### Theme 4. Importance tempering and SMC samplers (Zanella & Roberts 2019; Gramacy, Samworth & King 2010; Del Moral et al. 2006)

Covered by: **LIT-SMC** (SMC samplers, main), **LIT-MCMC**, **LIT-PAR**, **LIT-VENUE** (Zanella–Roberts), partly. **Gramacy–Samworth–King 2010 is not covered by any report.**
- **Del Moral, Doucet & Jasra 2006**, *JRSSB* 68:411–436: LIT-SMC read local PDF (Props 1–2). LIT-PAR: not separately.
- **Zanella & Roberts 2019**, *JRSS-B* 81(3):489–517 (arXiv 1805.00541v2): read in LIT-MCMC (Thm 1, Remarks 3–4, §3.3), LIT-VENUE (Thms 1–3), LIT-PAR (arXiv, cost passages), API-POS (§4.1, §4.5, Thms 2–3). Nothing quantitative on LH (API-POS). Zhou & Smith 2022 IIT (LIT-MCMC; arXiv 2107.10827 abstract, Assumption 1, Lemma 3, Thm 1). Jankowiak 2023 (AISTATS; arXiv 2208.01180; LIT-PAR R).
- SMC samplers theory: SVV, Schäfer–Chopin 2013 (R), Beskos et al. 2016, Beskos–Crisan–Jasra 2014, Giraud–Del Moral 2017, MMS 2023/2025, Mathews–Schmidler 2024, Paulin–Jasra–Thiery 2019 (*Bernoulli* 25(1):310–340), WSH 2009, Syed et al., Le Fay–Chopin–Vihola, Dau–Chopin, Chopin–Crucinio–Korba (venue UNVERIFIED), Lee–Whiteley 2018 (index only, U).
- **Missing**: Gramacy, Samworth & King 2010 (importance tempering); "Gramacy" does not appear in any LIT file. No LIT report reads Del Moral 2004 (book) or Andrieu–Doucet–Holenstein 2010. Shi–Dunson particle stochastic search and South–Pettitt–Drovandi (BA 2019) are named as unread in LIT-VENUE §8. Lee–Whiteley 2018 statement unverified.

### Theme 5. Diagnostics for scalable Bayesian computation (ESS, R-hat, PSIS, coupling bounds, Ẑ variance diagnostics)

Covered only thinly, by **LIT-VENUE** (certificates/diagnostics rows) and **LIT-SMC/LIT-PAR** (Ẑ variance). No report treats this theme as a theme.
- **Coupling bounds**: LIT-VENUE C2 Jacob, O'Leary & Atchadé, *JRSS-B* 82 2020 (arXiv 1708.03625; R; Prop 3.1 unbiasedness, "not a run certificate"); C3 Biswas, Jacob & Vanetti, arXiv 1905.09971 (NeurIPS 2019, venue UNVERIFIED), Thm 2.5, d_TV bound "Estimated, not certified" (R).
- **R-hat**: C4 Vehtari et al., *Bayesian Analysis* 16 2021, "Improved R̂", "Diagnostic only"; LIT-VENUE read "header" only (arXiv 1903.08008).
- **Ẑ variance diagnostics**: Lee & Whiteley 2018 (*Biometrika* 105(3):609–625), "Unbiased estimator of Var(Ẑ) from one run (statement not verified here; UNVERIFIED)" (LIT-SMC); Dai et al. 2022 notes asymptotic variance can be estimated as R → ∞ (LIT-PAR n07); Syed et al. barrier Λ; LIT-PAR "Report single-island relative variance of Ẑ". Rao–Blackwellised variance estimators are not read.
- **Spectral-gap certificates**: Wu arXiv 2605.30722 (abstract only); WSH note that swap-rate diagnostics cannot detect low persistence (LIT-SMC #20).
- **Missing / not covered**: ESS (bulk/tail, Vehtari or Gelman–Rubin versions), PSIS (Pareto-smoothed importance sampling), Gelman–Rubin R-hat original, multi-chain diagnostics for discrete model spaces, SMC-specific ESS/genealogy-based variance diagnostics (Lee–Whiteley is only an index entry in LIT-SMC), and diagnostics for our own flags (low_empirical_ESS, grid_unconverged). No report ties diagnostics to the proposal's goal.

---

## 5. LIT-PAR on the gap claim "no BVS method is parallel + correlation-robust + strongly guaranteed"

Verbatim key lines (LIT-PAR REPORT.md):

- Headline 1: "**Verdict on the gap claim: TRUE WITH QUALIFICATIONS.**" Then: "Every parallel BVS method we found that has a theorem needs a design condition that strongly correlated or masked designs violate (§2), or else does not target the model-space posterior." And: "We found **no** published method that combines all three of: (i) the exact model posterior with an unbiased evidence estimate; (ii) communication-free parallel width; (iii) a proved bound on the sequential depth under a correlated design."
- Headline 2: "**The literal sentence 'methods with guarantees are sequential' is FALSE in the work/depth sense. Do not print it.**" The strongest counterexample candidate is ZYVR: "T_mix ≤ 800·max(nκ₁/c₁, 3s₀)", each iteration scoring O(p·s₀) neighbours "can be easily parallelized", so "depth is O(n log p) score rounds under ZYVR Condition 1". "API-POS found that Condition 1 holds on our own linked-hub (LH) family, with ZYVR's priors (PROOF SKETCH there)."
- S-GAP (§4.1), status "**CONJECTURE about the literature; evidence from §2**": among published BVS methods, none simultaneously "(a) targets the exact model posterior with an unbiased evidence estimate, (b) parallelises in communication-free width (islands), and (c) has a proved sequential-depth (stage-count) bound on a correlated design whose start is masked."
- Falsification route 3: ZYVR parallelised "succeeds as a counterexample to 'guarantees ⇒ sequential', but not to the three-part S-GAP (no unbiased Ẑ, no islands, unimodality condition)".
- Wording that survives (§3.3 item 6): "We know of no BVS method that targets the exact posterior, scales out in communication-free width with consistent Ẑ-weighted pooling, and has a stage-count (depth) bound proved on a correlated design with a masked start. Feature-splitting methods with guarantees require cross-split faithfulness or weak correlation."
- Wording to avoid: "methods with guarantees are sequential"; "no analogue speed-up for MCMC"; "first parallel exact BVS"; "depth = T" without the per-round factor.
- Confidence: "medium-high (a literature claim can always be overturned by a missed paper; 2023–2026 coverage was by search, not exhaustive)". "Crux: ZYVR + parallel scoring; Schäfer–Chopin; pSMC".
- Self-critique, headline 4: "v3's per-particle depth is Θ(p) score evaluations per move round, not O(1) ... Counted in score evaluations, the depth is T·L·(p + B + 2). That is worse in p than a parallelised ZYVR chain." Method decision for HQ: Option A (state it) or Option B (informed/tempered-Gibbs moves scoring all p neighbours at once, D = O(T·L_r·log p)).
- Counter-arguments to TH1: "(i) Condition 1 excludes posterior multimodality ... (ii) It gives no unbiased Ẑ and no communication-free width beyond one step. (iii) It does not apply as stated to the paper's prior and cap (API-POS item 3)."
- What is missing: "a bound on the single-island relative variance in the masked regime. Without it, 'R → ∞ fixes everything' may need exponential R (Whiteley et al.'s own warning)." Outside scope item: "Single-island relative variance of Ẑ in the masked regime ... This is the theorem a referee will ask for."

**What LIT-PAR says about Song–Liang's conditions** (table row and notes 02, 09):
- Row: "SaM: split predictors into K groups; Stage-I BVS per group (SAMC, sequential MCMC) in parallel; merge; Stage-II BVS. Depth = one subset MCMC + one merged MCMC". Target: "Posterior **restricted** to the merged set S̃; not the full posterior". Proved: posterior consistency (Hellinger) under rate conditions and (A1); sure screening for "identifiable" predictors (B1), which "controls the severeness of multicollinearity"; "Misspecified-subset Thm 5: on subset s, π(s̃ ⊂ ξ | D_s) → 1, where s̃ = nonzero coordinates of the **projection** of the truth onto X_s. Asymptotic in n".
- Holds for us? "**No** on masked designs. A true variable whose within-split projection coefficient cancels (partner in another split) is screened out at Stage I and is unrecoverable. Random splits separate LH pairs." Relation: "Complementary. Confirms Felipe's belief."
- Notes 02: "CORRELATION CONDITION IMPLICIT IN THE SCREENING GUARANTEE: a true predictor j in subset s is retained only if its coefficient in the POPULATION PROJECTION onto X_s is nonzero ... Stage II's posterior is the posterior restricted to S̃ ... [Our reading of Thm 5; CHECK in paper.]" Also: "Asymptotic in n; no finite-n bound; no computational (mixing) guarantee for SAMC on each subset." And "SaM's theory does not assume or analyse clustering."
- Evidence: G4 numerical COUNTEREXAMPLE (p = 16, n = 200; exact full posterior recovers S₀ in 20/20; SaM 5/318 separated splits, "median Stage-I PIP of the masked variable 0.010", against 265/282 when the pair stays together; at β = 0.6 the separated count is 0/318). Clustered split {0..7},{8..15} recovers 15/20 at β = 1.0 and 3/20 at β = 0.6: "splitting costs power even when it respects correlation". The analytic step "PIP → 0" "is not verified against the paper".
- Escalation 1: "Song–Liang Thm 5 and our reading of it ... needs a check against the JRSSB text. The proposed G4 counterexample on LH depends on it."
- External corroboration (empirical, not theorems): DECO critique of SaM (quoted in LIT-PAR notes 02: "the screening step taken on each subset might select a large number of unimportant but correlated variables (Song and Liang, 2014)"); Coats et al. 2026 F1 falls to 0.126 at Toeplitz ρ = 0.99 and recommend separating correlated columns, "the opposite of our blocks and harmful under masking".

---

## 6. Literature gaps each report lists (open problems)

**LIT-SMC (G1–G5):**
- G1. "Discovery / 'the run scores the truth'": no SMC theorem addresses the event {S₀ ∈ 𝒮} or the best-scored output Ŝ.
- G2. "Masked start = low persistence, with an exact cost" (quantitative separation Q* = p^c n^{c/2}; stage cost log₂A₀ + O(1); moves off the start repair it on LH).
- G3. "n-indexed (statistical) consistency of Ẑ and PIPs": every Ẑ result is N → ∞ at fixed data or via mixing times.
- G4. "Stage counts in the favourable regime, T* = O(1)" (general results: Θ(d^{1/2}), O(d), √ln A).
- G5. "A posteriori certificates with guarantees" for SMC (BDMC needs exact posterior samples; BVS certificate literature not searched).
- Also: "nobody proves discovery"; general SMC theory needs bounded χ²/weight ratios plus mixing times, and multimodal versions need μ⋆ bounded below. Absence claims rest on non-exhaustive searches ("two web searches found none" for 2023–2026 SMC-for-BVS theory).

**LIT-MCMC (G1–G4, L2):**
- G1. "Discovery or scoring guarantees from (1b)/(1c) alone, with no (1a), no sparse cap and a weak prior"; hitting-time-of-S₀ theorem: "Nothing in the literature I read states" it. Status "CONJECTURE (literature), medium confidence".
- G2. "SMC/tempering with a start whose mode misses the truth (masked regime)".
- G3. "Finite-n, design-specific statements at n = 200 (N200, API-N200)": "All the theorems are asymptotic with unspecified universal constants".
- G4. "Composition with the output rule": T07/T21 concern the reported best-scored model.
- L2 (OPEN as a literature claim, medium confidence): "I found no published BVS family on which standard BVS MCMC provably mixes slowly while a tempering or SMC method provably succeeds. The only proved BVS slow-mixing example is YWJ App. A.2, which is cured by a size cap, not by tempering." Needs a second literature search (2024–2026 lower bounds for add/delete/swap under correlated designs; SMC/PT on binary spaces in the Schweizer 2012 / MMS line).
- Open items: OB(ii)–(iii) proof; YWJ/ZYVR theorem numbers from arXiv not journal.
- Remark (LIT-MCMC §9): "A population-level isolated signal is impossible in linear regression with RE, so any BVS slow-mixing family must come from overfitted traps or finite-n noise."

**LIT-STAT (G1–G5):**
- G1. "Concentration under BB(1,p) with a g = n slab and a cap of order n" (narrowed: handling the cap through the geometric tail and exact cutoff m♯_n, plus Prop D). Needs E1 check (Martin–Mess–Walker 2017).
- G2. "Guarantees for the reported HPM of a finite-budget algorithm whose start law masks the truth while the posterior concentrates."
- G3. "Decision-theoretic bookkeeping for a capped model space" (trivial; presentation gap).
- G4. "Finite-n relevance at n = 200": "Nobody has a usable finite-n selection theorem for designs like the study's."
- G5 (not ours). No statistical consistency or coverage theory for SuSiE found.

**LIT-VENUE (G1–G5, certificates):**
- G1. "Consistency of the output of an SMC sampler for BVS, including discovery" (rests on a sample of 30 plus searches; Shi–Dunson, South et al. not read in full).
- G2. "An exact, every-n decomposition of the reported-model error: posterior miss + search miss + no output".
- G3. "A lower bound for an iid start law (masking), together with repair theorems".
- G4. "Per-fit certificates on model space at p ≈ 10³": "no paper in the sample gives an a-posteriori, per-run, verifiable statement for a model-space posterior at p in the hundreds".
- G5. Machine-checked proofs.
- Venue-level gaps in OUR package (not literature): real-data analyses; head-to-head against LIT-MH, PARNI, MAdaSub, TGS, SuSiE/SSL; simulations at growing n; a main theorem not tied to LH; external human review. Verdict: Biometrika 5-result cut "realistic only if" Thm 5(b) is shown for the algorithm as run, with the transition at growing n; JCGS/BA/EJS/Stat. Comput. "comfortably"; JRSS-B "a stretch"; AoS "not realistic". (A judgement, not a status word.)

**LIT-PAR (G1–G4, S-GAP):**
- G1. "A guarantee for an exact-target parallel sampler for BVS whose start is masked ... on an explicit correlated family." (Generic theory needs μ⋆ ≥ 1/poly; Syed et al. assume efficient local exploration; pSMC assumes uniform Doeblin mixing.)
- G2. "Stage-count laws at a coarse, production ESS threshold": T* = O(1) favourable, log₂A₀ + O(1) masked, O(log log n) on LH masking.
- G3. "A theorem tying the depth of a parallel BVS sampler to a design-dependent quantity (A₀)": "Nobody analyses correlation-clustered splitting."
- G4. SaM-type splitting fails on a masked pair (numerical counterexample).
- Open: single-island relative variance of Ẑ in the masked regime; ZYVR Condition 1 on S1–S6 (recommend an O-task); "T38(a) and T32(i) reduce to Mathews–Schmidler Thm 1?"; HQ method decision on depth (Option A vs B).

**API-POS (not a LIT report, for completeness):** Unimodality on M(K) beyond p ≤ 20 is OPEN; YWJ-type spectral-gap bound for the paper's prior on LH-G with cap K = ⌊n/2⌋ is OPEN; Prop U needs a written proof; ZYVR Condition 1 on S1–S6 OPEN (per LIT-PAR); "YWJ explicitly leave the intermediate-signal regime (their (10)) open ... Theorem 5 does not reach it either, so this is a shared limitation". Also: "If the paper wants a family where the SMC bridge is *needed* against local MCMC, LH is the wrong family; a posterior-barrier design (W4-SHARE PB, or YWJ's App. A.2 example) would be the place to look."

---

## 7. Unread or unverified sources that carry weight (collected)

- **Song & Liang 2015 paper itself**: not read by any LIT report (slides only, LIT-PAR; second-hand, LIT-STAT).
- **Del Moral (2004) book**: not read by any report (carries the "classical" unbiasedness of Ẑ).
- **Andrieu–Doucet–Holenstein 2010**, **Gelman–Meng 1998**: via Dai et al. and Syed et al. only (LIT-PAR).
- **Martin, Mess & Walker (2017)**: not read (LIT-STAT; needed to confirm T02(i♯) novelty).
- **Lee & Whiteley 2018**: index only, statement unverified (LIT-SMC).
- **Lindsten et al. 2017, Kuntz et al. 2024**: abstracts only for theorem statements.
- **Scott et al. 2016 consensus MC**: abstract only.
- **YWJ 2016 and ZYVR 2022 journal versions**: all theorem numbers are from arXiv versions (LIT-SMC E3, LIT-MCMC E3, API-POS E1).
- **Gamarnik–Zadik AoS 2022 companion**, **Atchadé SIAM J. Math. Data Sci. 2021**, **Pozza–Zanella Biometrika 2025**, **Chopin–Crucinio–Korba ICML 2024**: venues UNVERIFIED.
- **Hans–Dobra–West 2007** and BVS stochastic-search certificate literature: not searched (LIT-SMC).
- **Shi–Dunson, South–Pettitt–Drovandi 2019**: not read in full (LIT-VENUE).
- **Gramacy–Samworth–King 2010; Ribatet 2012; Frazier 2023; Pauli; Varin; embarrassingly parallel MCMC; PSIS; ESS/R-hat originals**: not covered by any report.
