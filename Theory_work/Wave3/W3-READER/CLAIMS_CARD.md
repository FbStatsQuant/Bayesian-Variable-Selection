# Headline claims card — proposal v0.2, organised by five pillars (W3-READER, CP1, 2026-11-15)

v0.2 = v0.1 regrouped by the five pillars HQ asked for (organisation note, 2026-11-15), with pillar 3 widened to the
sampler outputs and pillars 4–5 added. No statement or status changed from v0.1.

Sources: registry `Theory_work/INFRA/registry/claims.tsv` (headline flags and statuses, base c04db8b), the 11-13
briefing, HQ_NOW. Statuses are verbatim (council suffixes cut after the first clause, marked "…"). "Thm k" refers to
`READER_VERSIONS.md` §k (reader statement, assumptions, master, bridges). Notation: `NOTATION.md`.

Setting for every theorem row: Gaussian linear model with intercept, fixed error variance, $p\le n^A$ ($p\gg n$
allowed), fixed true model size $s_0$, the shipped prior (capped beta-binomial on models, ridge-stabilised $g$-prior with
$g=n$, inverse-gamma noise variance); asymptotic; conditions on the design and the coefficients only, never a design
family.

**Legend.** Reader version: **clean** = numbered primitive assumptions and a 1–3-display conclusion, every bridge
marked · **long** = primitive but lengthy · **limit** = no primitive version; intuition + examples instead ·
**to write** = proposed, not yet in `READER_VERSIONS.md` · **n/a** = not a theorem.

---

## Pillar 1 — The posterior is right about the model

| # | Result, in words | Master and status (verbatim) | Buys vs the literature | Reader version |
|---|---|---|---|---|
| 1.1 (Thm 1) | **Posterior concentration, fixed design.** With a sparse eigenvalue floor on sets of bounded size, no near-collinearity among $O(\log n)$ columns, bounded coefficients and beta-min at $\sqrt{\log n/n}$: $1-\pi(S_0\mid y)=O_P(\sqrt{\log n/n})$, HPM = MPM = $S_0$ w.p. $\to1$, every PIP within $1-\pi(S_0\mid y)$ of the truth. | `W3-POST:Thm-1@1.0.0` = `SOP:TH09@1.0.0`: "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". Council W3-POST C3 passed (8.8/8.7); **registry label not PROVED-CHECKED**. | Song–Liang-type selection consistency for the shipped prior, with an explicit rate and exact HPM/MPM, no tuning, no design family. Narrower in dimension ($n^A$ vs $e^{Cn^\alpha}$). | **clean**; NEW bridges are set-size arithmetic |
| 1.2 (Thm 2) | **Same for random Gaussian designs**: rows i.i.d. Gaussian, fixed nonzero coefficients, population sparse eigenvalues bounded below on $O(\log n)$-sets (no upper bound). | Thm-1 item 6 (as 1.1) + `W2-APP:POST@1.0.1`: "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied". | Song–Liang's random-design setting; $p\gg n$. | **clean**; **unchecked input** (HQ-queued Sol check) |
| 1.3 (Thm 3) | **The rate cannot be improved.** On every design, $\pi(S\mid y)\le(1+(|S|+1)/(3\sqrt n))^{-1}$; with orthogonal or i.i.d. Gaussian null columns, $1-\pi(S_0\mid y)\ge(1-o_P(1))(s_0+1)\sqrt{\log p/(\pi n)}$. | `W3-PSHARP:B@1.0.0`, `W3-PSHARP:A@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …". | "Is your rate optimal?" — yes for $\log p\asymp\log n$; the sparsity frontier $s_0=o(\sqrt n)$. | **clean**, no bridge |

## Pillar 2 — The posterior is right about the distribution

| # | Result, in words | Master and status | Buys | Reader version |
|---|---|---|---|---|
| 2.1 (Thm 9) | **Distribution-level consistency (in progress).** Joint $(x,y)$ Hellinger contraction of the posterior at rate $\sqrt{\log n/n}$, exponential form (Song–Liang Theorems 1–2 analogue). | W3-DIST "Theorem DIST-1": candidate statement at its scoping checkpoint; **not proved; no registry row**. | Song–Liang Theorems 1–2 parity; owner's top priority. | not yet (W3-DIST proposes "master + bridges B0–B2") |
| 2.2 | *Already available, not headline:* in-sample (fixed-design) Hellinger contraction of the parameter posterior, rate $M_n/\sqrt n$ with selection, $\log n/n$ without beta-min. | `W3-POST2:D@1.1.0`: "PROVED (by this seat, unchecked)" (council C1 passed; acceptance stopped 11-15). | Partial Song–Liang parity; input to 2.1. | remark only |

## Pillar 3 — The coded algorithm delivers that posterior

| # | Result, in words | Master and status | Buys | Reader version |
|---|---|---|---|---|
| 3.1 (Thm 6) | **Main theorem: the reported model is the truth (Gaussian rows).** Under visibility, a leakage set of size $\le n^b$ ($b<\tfrac12$) with locality, population sparse eigenvalue floors and local regressions inside the leakage set: every run produces output and $P(\hat S=S_0)\to1$; on one data event of probability $\to1$, every run, for every seed and calibration outcome, reports $S_0$. | `W3-RM2:RM2-R@1.0.0`: "PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab8…, astra=9.5 PASS, opus=8.8 PASS; …" + `W3-RM:RM-0@1.0.0`: "PROVED-CHECKED" + `W2-UNI:F-UNI@1.1.0`: "PROVED-CHECKED". | Consistency of **what the software prints**, $p\gg n$, no design family; no comparable result for an SMC/MCMC BVS implementation known to us. | **long**; 2 NEW bridges (variance clause; delivery assembly); conditional on `W2-APP:POST` |
| 3.2 (Thm 7) | **Reported model, fixed design**: same conclusion under sample-level visibility and bounded leakage, with $|Q\setminus S_0|\le(1-\delta)\log n$ or $|Q|\le n^b$ plus local regressions. | `W3-RM2:RM2-F@1.0.0`: "PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, …" + RM-0, F-UNI as 3.1. | Fixed-design counterpart; version (a) fully explicit. | **limit** (sample-level conditions; masking exists); intuition per condition + examples |
| 3.3 (Thm 5) | **The start law already concentrates**: with Gaussian rows, visibility and no leakage outside $S_0$ (or outside $Q$, $|Q|\le n^{1/2-\epsilon}$), $\pi_0$ puts mass $\ge1-n^{-c}$ on $S_0$ (on the lattice of $Q$) for every $c<\tfrac12$; $\tfrac12$ is optimal. | `W3-START2:START-R@1.0.0`: "PROVED-CHECKED"; `W3-START:FLOOR@1.0.0`: "PROVED-CHECKED". | Explains why the sampler starts in the right place (method-specific). | **long**; body theorem |
| 3.4 (Thm 4) | **Omitted variables**: fitting candidates only (Gaussian rows; omitted part of any size; no fixed residual variance), the posterior concentrates on the support of the best candidate predictor at rate $\sqrt{\log n/n}$ in expectation; HPM error $O(\sqrt{\log n/n})$. | `W3-MISR:Cor-G(b)@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09, SOP:TH128, C-MIS:GDb; …"; inputs `W3-POST2:C/E/A1/A0@1.0.0`: "PROVED (by this seat, unchecked)". | Song–Liang Theorem 4 analogue, with a rate, no fixed variance; the coded method is exactly invariant to shifts and rescaling of $y$. | **clean**; conditional on POST2 |
| 3.5 | **Unbiased evidence and posterior averages.** Given the frozen calibration, each island's evidence estimate is unbiased, $E[\hat Z_r\mid\text{calibration}]=Z$, and $E[\hat Z_r H_r(h)\mid\text{calibration}]=Z\,\pi(h)$ for every bounded model summary $h$; no condition on the design. | `W1-N1:Thm-N1@1.0.0`: "PROVED-CHECKED". | The printed $\hat Z$ is an unbiased estimator of the evidence, for the method as coded (calibration included, because it is frozen first). | **to write** (clean: assumptions are the implementation conventions only) |
| 3.6 | **Printed PIPs, MPM, HPM and $\hat Z$ are consistent.** When the start concentrates and the posterior concentrates, $\hat Z/Z\to1$, the pooled PIPs converge to $\mathbf 1_{S_0}$ in sup-norm and MPM = $S_0$ w.p. $\to1$, with the posterior rate; independent of the ladder length. Alternative route without any condition on $\hat Z$: PIP/MPM/HPM consistency under a global-overlap condition. | `W3-SAMP:C@1.1.1`, `W3-SAMP:TR@2.1.1`, `W3-SAMP:LT#@2.0.1`, `W3-SAMP:D@2.1.1`: "PROVED-CHECKED" (each); start input `W3-START2:IF-START@1.0.0`: "PROVED-CHECKED". | Ties the theory to every number the software prints, not only the reported model. | **to write**: reader version = Thm 2 + Thm 5 (with $Q=S_0$) + `W3-SAMP:C`(C-v); NEW assembly bridge (P-CONC from Thm 2, P-START from Thm 5); implementation premises carried |
| 3.7 (Thm 8) | **Certified screening**: every certified reported model of size $\le q_n$ contains $S_0$ w.p. $\to1$, any $q_n=o(n/\log n)$, under a sparse eigenvalue floor on $(q_n+s_0)$-sets and fixed signals; no start, leakage, block or visibility condition. | `W3-SCR:A1@1.0.0`: "PROVED-CHECKED". | Holds exactly where 3.1–3.2 may fail (strong factors, masking). | **clean**, no bridge |

## Pillar 4 — The parallel method preserves it (mostly open)

| # | Item | Status | Reader version |
|---|---|---|---|
| 4.1 | **Pooling over the coded 4 islands.** The pooled PIP is the equal-weight island mean, so its sup-norm error is at most the worst island's (`W3-SAMP:LT#` (LT-d), "PROVED-CHECKED"); the pooled $\hat Z=\frac14\sum_r\hat Z_r$ is unbiased given the calibration (one-line corollary of `W1-N1:Thm-N1` by linearity; **not a registered claim — NEW, trivial**). | proved (LT-d); NEW trivial (pooled $\hat Z$) | to write (two lines) |
| 4.2 | **An output-identical parallel engine inherits every guarantee above.** Engineering fact: engine revision D is byte-identical to the serial engine on the tested set (24/24 production-hash cases, 10/10 supplementary; briefing 11-13). The inheritance statement is a note in progress (W3-SCALE). | **empirical + note in progress; no theorem, no registry row** | n/a until the note exists |
| 4.3 | **Many islands, island weighting, fixed $N$ per island at $p=10^6$.** Evidence census: island log-evidence spread grows with $p$ (0.09 at $p=2$k, 0.76–1.15 at 5k–20k; one island held 79% of the weight at 5k); PIPs agree across islands to $\le5\times10^{-4}$. Do not weight islands by $\hat Z$ at $p\ge5$k. | **OPEN** (no theorem; moved to the scaling paper) | n/a |

## Pillar 5 — Scale (empirical, not theorems)

| # | Item | Status | Use in the paper |
|---|---|---|---|
| 5.1 | **The 2,400-fit simulation study**: posterior-estimation accuracy and selection results across designs. | empirical; whether the v3.2 rerun is needed is an open HQ question (HQ_NOW, advisor report) | results section; advisor report item 1 |
| 5.2 | **Strong factors at $p\gg n$ (P6 experiment)**: stage 1 had 0 search failures; every miss was a posterior miss ($F(\mathrm{HPM})>F(S_0)$). | empirical; D1 framing pending (theorem attempt vs stated limit) | examples / limits section, next to 3.7 and the LS0-only negative result |
| 5.3 | **$p=10^6$ experiment** (Experiment department, plan at EXP-CP1). | empirical; planned | scaling section; advisor report item 3 |

---

## Notes for HQ and the consultant

* **Placement of the omitted-variables theorem (3.4).** Placed in pillar 3 as HQ listed it. Lead's view: it is a
  statement about the exact posterior (pillar 1); its only coded-method content is the exact invariance of the code to
  shifts and rescaling of $y$. Recommend moving it to pillar 1 (row 1.4); HQ decides.
* **Abstract-level headlines (proposal):** 3.1 (main), 1.1–1.2, 1.3, 2.1 (when proved), 3.4. Body theorems: 3.2, 3.3,
  3.5–3.7. Pillars 4–5 are honest-status rows, not theorems.
* **What blocks a fully PROVED-CHECKED card** (bookkeeping or line checks, no new mathematics): (1) `W2-APP:POST@1.0.1`
  Sol line check (1.2, 3.1, 3.4) — HQ-queued; (2) POST2 C/E/A1/A0 council diff round (3.4; also 2.2) — HQ-identified;
  (3) registry label for `SOP:TH09`/`W3-POST:Thm-1` (1.1, 3.2) — council-passed C3; (4) the NEW reader bridges
  (`READER_VERSIONS.md` summary table) plus the two new "to write" rows (3.5, 3.6) and 4.1.
* **Left out on purpose:** design-family theorems (`W2-FAC-*`, `W1-PXN`, `W2-LOC2`, `W2-UNI:UNI-0`) are examples under the
  presentation rule; `W3-RM:RM-F/RM-R` are special cases of 3.1–3.2; `W1-GEN`, `C-GROW` are historical routes; delivery
  (`C-DLV:Prop-F`, `W2-UNI:F-UNI`) is folded into 3.1–3.2.
* **Readability (lead's verdict):** 1.1, 1.2, 1.3, 3.4, 3.5, 3.7 read like Song–Liang-level statements; 3.1 is faithful
  but long (the "15" needs one sentence: block size minus one); 3.2 and 3.3 are honest-limit rows.
