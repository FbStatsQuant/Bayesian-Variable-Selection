# Headline claims card — proposal v1.3, organised by five pillars (W3-READER, bridge leg, 2026-11-16)

v1.3 = v1.2 with rows 3.1 and 3.2 updated to the RM2 rider (W3-RM2-R CP3 accepted; H5 card 14 AGREED, HQ D74) — **MIXED**:
STRONGER for Thm 7's signal and visibility conditions at the constant level and for the mode-form core (RM0-plus);
WEAKER for delivery, which now needs IDEAL-W⁺ (two code ceilings lifted) and a narrower (valid, non-degenerate) input
domain, with the implication edge to C-DLV:Prop-F withdrawn. Method drift: Prop-F's method uses LS0 cap $\ell_n$, not the
shipped $\ell_n+|\tilde S_0|$; delivery for the shipped method rests on W3-RM2-R:DLV-0.

v1.2 = v1.1 with row 3.7 swapped to W3-SCR-R2 READER_DELTA v4 (HQ conditional GO, task R main 8875eeba, interim label removed d2b600ba): form (a), plain; row text per H5 card 11 — EQUAL.
v1.1 = v1.0 with row 1.4 swapped to W3-MISR-R READER_DELTA v0.4 (HQ signal, task Q; accepted main 2b54cb3c): reader-version master CorGb-plus, Song–Liang line from the delta — STRONGER (weaker hypotheses).
v1.0 = v0.9 with row 1.3 swapped to W3-PSHARP-R READER_DELTA v0.4 (HQ signal; headline sentence verbatim) — STRONGER
(expectation display for every $p$ on the null-column designs). v0.9 = v0.8 with SL0 cleared (main 33e1f0f5): requoted statuses, SL0 reader wording dropped — EQUAL. v0.8 = v0.7 with the registry status refresh at main f526e45b and the row 1.1 Forms A/B (HQ order) — statuses only,
EQUAL. v0.7 = v0.6 with H5 card 7 consequences (abstract wording of rows 1.1 (Thm 1′), 3.1/3.2; row 3.6 to the body; open-items
list with O1 ranked with O3) — EQUAL (presentation). v0.6 = v0.5 with: row 3.5 credits Del Moral (GATES row 3.5) — EQUAL; H5 card 6 on rows 1.1 and 1.3 — 1.1 EQUAL, 1.3
**WEAKER** (the "optimal" claim narrowed to the witness designs, as `W3-PSHARP/STATEMENT.md:92-110`); Engineering D-17
note — EQUAL; S2-F4/F5 on row 3.6 — **WEAKER** (localisation, not conditioning, `W3-SAMP/STATEMENT.md:158-162`; Theorem
10's standardised-signal setting); S2-F6 and S3-N4/N7/N8 wording on rows 1.1, 1.3 and the D-17 note — EQUAL. Tags
confirmed by the S3 diff check (`reviews/S3_diffcheck_opus.md`).

v0.5 = v0.4 with the H5 card-5 verdict applied (consultant AGREE on the split as the **provisional** headline list;
OBJECT on row 1.1; markers [H5-#]): row 1.1 re-based on the posterior refinements; row 1.4's masters are MIS(i)/(ii);
setting line names the Gaussian-row rows; abstract list updated; row 3.6 has a reader version (Thm 10); row 4.1's
pooled-evidence corollary is a registered claim of this ticket. v0.4 = MISR moved to 1.4 (manager, CP1 answer).
v0.3 = card-level S1 fixes (F2, F5, F7, F8, F12). v0.2 = regrouped by the five pillars (HQ, 2026-11-15).

Sources: registry `Theory_work/INFRA/registry/claims.tsv` (headline flags and statuses, base c04db8b), the 11-13
briefing, HQ_NOW. Statuses are verbatim (council suffixes cut after the first clause, marked "…"). "Thm k" refers to
`READER_VERSIONS.md` §k (reader statement, assumptions, master, bridges). Notation: `NOTATION.md`.

**Setting [H5-4].** Every theorem row: Gaussian linear model with intercept, fixed error variance, $p\le n^A$ ($p\gg n$
allowed), fixed true model size $s_0$, the shipped prior (beta-binomial on models with $p$ = predictors not constant in
the sample, capped at $\min(p,\lfloor n/2\rfloor)$; ridge-stabilised $g$-prior with $g=n$; inverse-gamma noise variance);
asymptotic. Rows 1.1, 1.3, 3.2, 3.7 are fixed-design results with conditions on the design and the coefficients.
**Rows 1.2, 1.4, 3.1, 3.3 and 3.6 assume i.i.d. Gaussian rows** with conditions on their population correlation
matrix. A law of the rows is an assumption on the data, not a design family; no theorem row assumes a design family
(families appear only as examples).

**Legend.** Reader version: **clean** = numbered primitive assumptions and a 1–3-display conclusion, every bridge
marked · **long** = primitive but lengthy · **limit** = no primitive version; intuition + examples instead · **n/a**.

---

## Pillar 1 — The posterior is right about the model

| # | Result, in words | Master and status (verbatim) | Buys vs the literature | Reader version |
|---|---|---|---|---|
| 1.1 (Thm 1, 1′) | **Posterior concentration, fixed design** [H5-1]. With a sparse eigenvalue floor on sets of bounded size, no near-collinearity among $O(\log n)$ columns, bounded coefficients and beta-min at $\sqrt{\log n/n}$: $E[1-\pi(S_0\mid y)]\le C\sqrt{\log n/n}$ **uniformly over such designs**, HPM = MPM = $S_0$ w.p. $\ge1-4C\sqrt{\log n/n}$, every PIP within $1-\pi(S_0\mid y)$ of the truth. Variant (Thm 1′, no eigenvalue condition off $S_0$ beyond the vanishing floor (A5) on $O(\log n)$-sets, which still excludes exact dependence among $O(\log n)$ columns, duplicated nulls included): the bounded-size floor off $S_0$ and beta-min replaced by an identifiability margin (every small model missing a truth leaves residual signal $\ge c\,\sigma_*^2\log n$ with $c>c_1(s_0,A)$, an explicit constant, not optimised) [S3-N7]; the floor on $S_0$ is sufficient, not known to be necessary (open item O3) [H5-6]. | Expectation form and variant (main f526e45b): `W3-POST2:C@1.0.4` "PROVED-CHECKED, conditional on W3-POST:Prop-LB, [L1a′], SOP:TH09, SOP:TH128, W2-APP:POST, W3-POST:Thm-1"; `W3-POST2:E@1.0.4` "PROVED-CHECKED, conditional on SOP:TH128, SOP:TH09, W2-APP:POST, W3-POST:Thm-1" [REG-f526]. $O_P$ form: `W3-POST:Thm-1@1.0.0` = `SOP:TH09@1.0.0`: "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (council C3 passed; label pending). | Song–Liang-type selection consistency for the shipped prior with an explicit, design-uniform expectation rate and exact HPM/MPM; no tuning; Thm 1′ uses a residual-signal identifiability condition (Narisetty–He style) instead of eigenvalue floors off the truth. Narrower in dimension ($n^A$ vs $e^{Cn^\alpha}$). | **clean** (both); NEW bridges: set-size arithmetic (R1) |
| 1.2 (Thm 2) | **Same for random Gaussian designs**: rows i.i.d. Gaussian, fixed nonzero coefficients, population sparse eigenvalues bounded below on $O(\log n)$-sets (no upper bound): $1-\pi(S_0\mid y)=O_P(\sqrt{\log n/n})$, HPM = MPM = $S_0$ w.p. $\to1$. | Thm-1 item 6 (as 1.1) + `W2-APP:POST@1.0.6`: "PROVED-CHECKED, conditional on SOP:TH09" [REG-f526]. | Song–Liang's random-design setting; $p\gg n$. | **clean**; conditional on T03♯ (abstract: Form A/B) |
| 1.3 (Thm 3) | **The rate cannot be improved** [W3-PSHARP-R swap]. The rate of Theorem 1 cannot be improved under its assumptions: on orthogonal or Gaussian null columns, $E[1-\pi(S_0\mid y)]\ge c\cdot(s_0+1)\cdot\sqrt{\log n/n}$, for every $p$. On every design, for every model with $|S|\le\min(K-1,p/2)$, $\pi(S\mid y)\le(1+(|S|+1)/(3\sqrt n))^{-1}$ (order $n^{-1/2}$ only); in probability, $1-\pi(S_0\mid y)\ge(1-o_P(1))(s_0+1)\sqrt{\log p/(\pi n)}$ on these null-column designs when $p\to\infty$. | `W3-PSHARP:B@1.0.0`, `W3-PSHARP:A@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …". Expectation display: `W3-PSHARP-R:AE@1.0.0`, `W3-PSHARP-R:A2C@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST fdfd4562…, sol=9.5 PASS, opus=9.2 PASS". Named exactness case: bridge B3.8 (Sol-checked). | "Is your rate optimal?" — on the witness designs (orthogonal or i.i.d. Gaussian null columns) yes for $\log p\asymp\log n$; on every design the proved lower bound is of order $n^{-1/2}$ (a matching expectation lower bound $\gtrsim\sqrt{\log n/n}$ under a floor on $S_0\cup\{j\}$ is open, rider POST2-R1) [H5-6, S3-N4]; the sparsity frontier $s_0=o(\sqrt n)$. | **clean**, no bridge |
| 1.4 (Thm 4) | **Omitted variables** [H5-3]: fitting candidates only, with any residual variance (fixed, vanishing or growing with $n$), the posterior concentrates on the support of the best candidate predictor at rate $\sqrt{\log n/n}$ in expectation, uniformly over the residual variance (fixed candidate design); with Gaussian candidate rows and, given the candidates, Gaussian responses with mean linear in the candidates (reader version; omitted Gaussian predictors of any size are the leading example) the HPM error is $O(\sqrt{\log n/n})$ [H5-10]. | Headline masters `W3-MISR:MIS(i)@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:C; …"; `W3-MISR:MIS(i')@1.0.0`, `W3-MISR:MIS(ii)@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; …". Gaussian-row reader version `W3-MISR-R:CorGb-plus@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, SOP:TH09, SOP:TH128, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS"; Example `W3-MISR-R:CorG-min@1.0.0`: "PROVED-CHECKED, conditional on SOP:TH09, SOP:TH128; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS"; body remark (Hellinger/KL) `W3-MISR-R:CorH-plus@1.0.0`, `W3-MISR-R:CorH-U@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:D, …" [REG-2b54]. Inputs `W3-POST2:C/E/A1/A0@1.0.4`: "PROVED-CHECKED, conditional on …" (ultimately on SOP:TH09; main f526e45b) [REG-f526]. | Analogue of Song–Liang (2015) Theorem 4 and Corollary 2 in their omitted-Gaussian-predictor setting, where the candidate-only conditional model is correctly specified: exact selection of the best candidate predictor's support with rate $\sqrt{\log n/n}$, no condition on how $\Sigma$, $\beta$, $\sigma^2$ vary with $n$; the coded method is exactly invariant to shifts and rescaling of $y$ [H5-10]. | **clean** (CorGb-plus); conditional on POST2 |

## Pillar 2 — The posterior is right about the distribution

| # | Result, in words | Master and status | Buys | Reader version |
|---|---|---|---|---|
| 2.1 (Thm 9) | **Distribution-level consistency (in progress).** Joint $(x,y)$ Hellinger contraction of the posterior at rate $\sqrt{\log n/n}$, exponential form (Song–Liang Theorems 1–2 analogue); no beta-min and no fixed lower bound on eigenvalues (W3-DIST v1.4 wording). | W3-DIST "Theorem A" (v1.4): **not proved; no registry row**. Abstract only after DIST CP3 [H5-5]. | Song–Liang Theorems 1–2 parity; owner's top priority. | not yet (W3-DIST proposes "master + bridges B0–B2") |
| 2.2 | **Fallback if 2.1 slips [H5-5]:** in-sample (fixed-design) Hellinger contraction of the parameter posterior, rate $M_n/\sqrt n$ with selection, $\log n/n$ without beta-min. | `W3-POST2:D@1.1.4`: "PROVED-CHECKED, conditional on SOP:TH09, SOP:TH128, W2-APP:POST, W3-POST:Thm-1" [REG-f526]. | Partial Song–Liang parity; input to 2.1. | to write if used |

## Pillar 3 — The coded algorithm delivers that posterior

| # | Result, in words | Master and status | Buys | Reader version |
|---|---|---|---|---|
| 3.1 (Thm 6) | **Main theorem: the reported model is the truth (Gaussian rows).** Under visibility, a leakage set of size $\le n^b$ ($b<\tfrac12$) with locality, population sparse eigenvalue floors and local regressions inside the leakage set: on one data event of probability $\to1$, every admissible run that produces output, for every seed and calibration outcome, reports $S_0$. *Delivery clause (body only [H5-2]):* under the delivery conventions (S4) — idealised machine with two code size ceilings lifted, shipped configuration, sufficient declared allocation, valid input — every run produces output and $P(\hat S=S_0)\to1$; the error splits into a posterior-mode term and a search term (remark). The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5]. Neither limit can bind unless $n+p+1>2^{10^6}$ or $n\gtrsim4\times10^9$, that is, at no feasible problem size [RM2R-6]. [RM2R] | `W3-RM2-R:RM2-R-plus` (+ `RM0-plus`, `DLV-0`): CP3 status "PROVED (by this seat, unchecked); conditional on W2-APP:POST@1.0.1; LC-B VERIFIED", conditional on two code-reading audits of the delivery path (`C-DLV:L2-S3`, `C-DLV:P1-Inventory`), which DLV-0 takes as hypotheses [RM2R-7], council R3 PASS (MANIFEST b06a8588…, sol=9.5, opus=9.4) — **requote verbatim once recorded**; it implies `W3-RM2:RM2-R@1.0.2` ("PROVED-CHECKED, conditional on W2-APP:POST; …"), whose input `W2-APP:POST@1.0.6` is "PROVED-CHECKED, conditional on SOP:TH09" [REG-33e1], so the row is conditional on T03♯ and on two code-reading audits of the delivery path [RM2R-7]. **Method drift [D74]:** Prop-F/F-UNI used LS0 cap $\ell_n$, not the shipped $\ell_n+|\tilde S_0|$; delivery for the shipped method rests on DLV-0. | Consistency of **what the software prints**, $p\gg n$, no design family; no comparable result for an SMC/MCMC BVS implementation known to us. | **long**; NEW bridges R2, R3; conditional on `W2-APP:POST`; **MIXED** v1.3 |
| 3.2 (Thm 7) | **Reported model, fixed design**: same conclusion under sample-level visibility at a fixed multiple of $\log n$, bounded leakage, beta-min at the standard $\sigma\sqrt{\log n/n}$ scale (constants in remarks), with $|Q\setminus S_0|\le(1-\delta)\log n$ or $|Q|\le n^b$ plus local regressions; same order of clauses as 3.1 [H5-7.3]; delivery clause as 3.1, including its sentence on the two fixed integer limits [RM2R-5]. [RM2R] | `W3-RM2-R:RM2-F-plus` (+ `RM0-plus`, `DLV-0`): CP3 status "PROVED (by this seat, unchecked); conditional on SOP:TH09@1.0.0; LC-B VERIFIED", conditional on two code-reading audits of the delivery path (`C-DLV:L2-S3`, `C-DLV:P1-Inventory`), which DLV-0 takes as hypotheses [RM2R-7], council R3 PASS (MANIFEST b06a8588…) — **requote verbatim once recorded**; it implies `W3-RM2:RM2-F@1.0.0` ("PROVED-CHECKED, conditional on SOP:TH09; …"). Method drift as 3.1. | Fixed-design counterpart; version (a) fully explicit; signal conditions now at the standard constant level. | **limit** (sample-level conditions; masking exists); intuition per condition + examples; **MIXED** v1.3: STRONGER conditions, WEAKER delivery premises |
| 3.3 (Thm 5) | **The start law already concentrates**: with Gaussian rows, visibility and no leakage outside $S_0$, $\pi_0$ puts mass $\ge1-n^{-c}$ on $S_0$ for every $c<\tfrac12$; with a leakage set $|Q|\le n^{1/2-\epsilon}$, mass $\ge1-n^{-c}$ on the lattice of $Q$ for every $c<\epsilon$; $\tfrac12$ is optimal. | `W3-START2:START-R@1.0.0`: "PROVED-CHECKED"; `W3-START:FLOOR@1.0.0`: "PROVED-CHECKED". | Explains why the sampler starts in the right place (method-specific). | **long**; body theorem |
| 3.4 | *(moved to row 1.4, manager's CP1 decision 6)* | | | |
| 3.5 | **The evidence estimate is unbiased.** Given the frozen calibration, each island's evidence estimate, and hence the printed (equal-weight pooled) $\hat Z$, is unbiased for $Z$; no condition on the design. | `W1-N1:Thm-N1@1.0.0`: "PROVED-CHECKED"; pooled form `W3-READER:PoolZ` (this ticket): "PROVED (by this seat, unchecked)". | The classical unbiasedness of SMC normalising-constant estimates (Del Moral), established **for the method as coded, calibration included** (the calibration is frozen before the final run's randomness) [GATES row 3.5]. | body remark (Thm 10 remark) |
| 3.6 (Thm 10) | **The printed outputs are consistent** (Gaussian rows, sampler branch) [S2-F4, S2-F5]: in Theorem 10's setting — signal fixed on the standardised scale, Theorem 2's population floor, Theorem 5's visibility and no-leakage conditions — the errors $|\hat Z/Z-1|$, $|\log\hat Z-\log Z|$ and the sup-norm error of the pooled PIPs, multiplied by the indicator of calibration success, are $O_P(n^{-1/2}e^{C\sqrt{\log n}})$; the probabilities of "calibration succeeds and the MPM is wrong" and of "the run completes and the reported model is wrong" tend to zero. (Intersections, not conditioning: no lower bound on the probability of calibration success is claimed. On completed runs these are the printed fields.) | `W3-SAMP:C@1.1.3`, `TR@2.1.3`, `LT#@2.0.3`, `D@2.1.3`: "PROVED-CHECKED, conditional on SOP:TH09" (each) [REG-33e1]; start input `W3-START2:IF-START@1.0.0`: "PROVED-CHECKED"; posterior input `W2-APP:POST@1.0.6` (covers the standardised-signal convention): "PROVED-CHECKED, conditional on SOP:TH09". | Ties the theory to every number the software prints. | **clean**; NEW assembly R4; conditional on T03♯; body (H5 card 7) |
| 3.7 (Thm 8) | **Certified screening** [SCR-PC, SCR-R2]: under (A1)–(A3) of Theorem 8 — a sparse eigenvalue floor on $(q_n+s_0)$-sets, with the floor constant κ, the signal minimum b, the coefficient bound M and the noise variance σ² all fixed in $n$, $q_n$ below the model-size cap $\min(p,\lfloor n/2\rfloor)$, and $(q_n+1)\log p+\log n\le c_1n$ (any $q_n=o(n/\log n)$ when $p\le n^A$) — the probability that a run produces output, certifies (sets its local-optimality flag for) a reported model of size $\le q_n$, and that model misses a true predictor tends to zero; no start, leakage, block or visibility condition. Signals varying with $n$ are not covered (open item SCR-R1). | `W3-SCR:A1@1.0.0`: "PROVED-CHECKED" (main d2b600ba, interim label removed; council R3, MANIFEST 19847f54…, sol=10.0 PASS, opus=9.4 PASS) [REG-d2b6]. | The only coded-method guarantee that needs no visibility, leakage, start or block condition, so its assumptions can hold on designs (strong factors included) where those of 3.1–3.2 do not [H5-11]. | **clean**, no bridge |

## Pillar 4 — The parallel method preserves it (mostly open)

| # | Item | Status | Reader version |
|---|---|---|---|
| 4.1 | **Pooling over the coded 4 islands.** The pooled PIP is the equal-weight island mean, so its sup-norm error is at most the worst island's (`W3-SAMP:LT#` (LT-d), "PROVED-CHECKED"); the pooled $\hat Z=\frac14\sum_r\hat Z_r$ is unbiased given the calibration (`W3-READER:PoolZ`, registered claim of this ticket, approved [H5-6c]; "PROVED (by this seat, unchecked)", line check in the bridge leg's Sol review, in the CP3 manifest). | proved (LT-d); PoolZ pending its line check | `STATEMENT.md` (two-line proof) |
| 4.2 | **An output-identical parallel engine inherits every guarantee above.** Engineering fact: engine revision D is byte-identical to the serial engine on the tested set (24/24 production-hash cases, 10/10 supplementary; briefing 11-13). The inheritance statement is a note in progress (W3-SCALE). | **empirical + note in progress; no theorem, no registry row** | n/a until the note exists |
| 4.3 | **Many islands, island weighting, fixed $N$ per island at $p=10^6$.** Evidence census: island log-evidence spread grows with $p$ (0.09 at $p=2$k, 0.76–1.15 at 5k–20k; one island held 79% of the weight at 5k); PIPs agree across islands to $\le5\times10^{-4}$. Do not weight islands by $\hat Z$ at $p\ge5$k. | **OPEN** (no theorem; moved to the scaling paper) | n/a |

## Pillar 5 — Scale (empirical, not theorems)

| # | Item | Status | Use in the paper |
|---|---|---|---|
| 5.1 | **The 2,400-fit simulation study**: posterior-estimation accuracy and selection results across designs. | empirical; whether the v3.2 rerun is needed is an open HQ question (HQ_NOW, advisor report) | results section; advisor report item 1 |
| 5.2 | **Strong factors at $p\gg n$ (P6 experiment)**: stage 1 had 0 search failures; every miss was a posterior miss ($F(\mathrm{HPM})>F(S_0)$). | empirical; D1 framing pending (theorem attempt vs stated limit) | examples / limits section, next to 3.7 and the LS0-only negative result |
| 5.3 | **$p=10^6$ experiment** (Experiment department, plan at EXP-CP1). | empirical; planned | scaling section; advisor report item 3 |

---

## Abstract (provisional headline list; consultant AGREE, H5 card 5; consequences adopted by HQ, H5 card 7)
Gate for every abstract row: strength gates PASS (`GATES.md`, Thu 11-19) **and** PROVED-CHECKED masters; an abstract row
may carry an unchecked "conditional on" input only if the abstract states it [H5-6b].
- **Forms (CP3 picks on W3-T03ACC, Thu 18:00)** [REG-f526]. **Form A** (T03♯ passes its council acceptance): rows 1.1
  ($O_P$ form), 1.2 and 3.1 as below (no further condition: SL0 cleared, main 33e1f0f5). **Form B** (it
  misses): **B1, recommended** — one sentence states the shared condition in reader words, *"conditional on the
  posterior concentration theorem for the coded prior, which has been verified independently by reviewers of the same
  and of a different model family but has not yet passed a council review"*, for rows 1.1, 1.2 and 3.1; ~~B2~~ (rejected by HQ, 2026-11-16). **HQ decision:** Form A if
  W3-T03ACC passes, B1 otherwise; the abstract uses Theorem 1's $O_P$ form; the expectation display and Theorem 1′ stay
  in the body with their conditions.
- **3.1** main theorem. The abstract leads with the clause that needs no delivery convention: *"on one data event of
  probability tending to one, every admissible run that produces output reports $S_0$, for every seed"*; its
  conditions are those of the Forms paragraph above. "Every run produces output" is a
  body statement, with the delivery conventions (S4) of C-DLV [H5-7.3].
- **3.2**, wherever it is cited (body by default): the same order of clauses as 3.1 [H5-7.3].
- **1.1** posterior concentration (expectation form once POST2 is recorded; until then the $O_P$ form), **1.2**, **1.3**.
  Theorem 1′ is never called "the design-agnostic form"; its exact description is: *it drops the fixed floor (A4) off
  $S_0$ but keeps the vanishing floor (A5), which still excludes exact linear dependence among $O(\log n)$ columns,
  duplicated null columns included* [H5-7.1].
- **1.4** omitted variables — states its conditionality on the posterior refinements until they are recorded.
- **3.7** certified screening — **abstract, form (a), plain** (second SCR council round passed; H5 cards 9, 11): the
  clause of `READER_VERSIONS.md` row thm8 "Placements" ($\kappa$, $b$, $M$, $\sigma_*$ fixed in $n$; $q_n$ below the cap;
  $c_1$ by name; "certifies" defined); the body carries Theorem 8′ (plain) [SCR-R2].
- **2.1** only after W3-DIST CP3; fallback **2.2** if it slips [H5-5].
Body: 3.2, 3.3, 3.5 (remark), **3.6** (the consultant withdrew its promotion; its premises do not fit one abstract
clause: Gaussian rows, population floor, visibility, no leakage, and the sampler conventions) [H5-7.4]. Pillars 4–5:
honest-status rows.

## Open items attached to headline rows (post-freeze riders)
- **O1 and O3 rank together** [H5-7.2]: O1 — a design-free sufficient condition for the superset Occam-sum condition
  (OS); **whether (OS) holds without any eigenvalue condition is open**, and O1 is what would make "no eigenvalue
  condition off $S_0$" literally true for Theorem 1′; O3 — the floor on $S_0$ replaced by a bounded ridge cost (the
  floor is sufficient, not known to be necessary).
- O2 — the margin constant $c_1(s_0,A)$ (explicit, not optimised).
- POST2-R1 — a matching expectation lower bound $\gtrsim\sqrt{\log n/n}$ under a floor on $S_0\cup\{j\}$.
- SAMP-R1 (row 3.6) and SCR-R1 (row 3.7) — strengthenings from the SHARP3 triage.

## Notes for HQ and the consultant
* **Placement of the omitted-variables theorem.** Row 1.4 (pillar 1), manager's CP1 decision 6. Row 3.4 left empty so
  other row numbers stay stable.
* **Status refresh (main f526e45b, then 33e1f0f5) [REG-f526, REG-33e1].** `W2-APP:POST` accepted, conditional on SOP:TH09;
  POST2 C/E/A0/A1/D recorded (conditional, ultimately on SOP:TH09); C-PACK:SL0 PROVED-CHECKED, so W3-SAMP C/D/LT♯/TR
  and W3-RM:RM-R read conditional on SOP:TH09 (RM-R also SOP:TH05.0). The single remaining root is T03♯ (W3-T03ACC,
  CP3 Thu 18:00). The list below is superseded where it disagrees.
* **What blocks a fully PROVED-CHECKED card** (bookkeeping or line checks, no new mathematics): (1) `W2-APP:POST@1.0.1`
  Sol line check (1.2, 3.1, 3.6) — HQ-queued; (2) POST2 C/E/A1/A0/D recording (1.1 expectation form, 1.4, 2.2) —
  recorder task D; (3) registry label for `SOP:TH09`/`W3-POST:Thm-1` (1.1 $O_P$ form, 3.2); (4) F-UNI correctness gate
  (3.1–3.2 delivery clause) — recorder; (5) the NEW reader bridges R1–R4 and `W3-READER:PoolZ` — bridge leg's Sol line
  check.
* **Left out on purpose:** design-family theorems (`W2-FAC-*`, `W1-PXN`, `W2-LOC2`, `W2-UNI:UNI-0`) are examples under the
  presentation rule; `W3-RM:RM-F/RM-R` are special cases of 3.1–3.2; `W1-GEN`, `C-GROW` are historical routes; delivery
  (`C-DLV:Prop-F`, `W2-UNI:F-UNI`) is folded into 3.1–3.2.
* **Moderate-$n$ description [ENG-D17].** All rows are asymptotic. At moderate $n$ and large $p$ the posterior and the
  coded output are a mixture over $S_0$ and its many one-variable supersets (individually light, together comparable to
  $S_0$); texts describe this as the shape of the posterior, not as a limitation, and never describe the output as a point
  mass at moderate $n$ (Engineering measurement, `Docs/Experiments/P1M/DECISIONS.md` D-17, on `main` at f237bfa3 or later) [S3-N8].
* **Readability (lead's verdict):** 1.1–1.4, 3.6, 3.7 read like Song–Liang-level statements; 3.1 is faithful but long
  (the "15" needs one sentence: block size minus one); 3.2 and 3.3 are honest-limit rows.
