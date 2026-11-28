# W3-READER — CP3 package for HQ (2026-11-16)

**Final:** MANIFEST_R3 `7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263` (92 files, 28 external inputs),
frozen in commit `2714aaca` (content of `68443dcc`); `manifest.py verify` OK; bind record `reviews/BIND_R3.txt`. Card v1.12.

**Council cells** (seats: gpt-6.1-sol high, claude-opus-5-5 high)
| round | manifest | sol | opus | sol FIDELITY | bind |
|---|---|---|---|---|---|
| R1 | `759a7dfd…` | 7.4 FAIL | 7.6 FAIL | NOT-FAITHFUL | — (all findings fixed, `bf4495e8`) |
| R2 | `3af23c35…` | 9.3 PASS | 9.3 PASS | FAITHFUL | OK (`reviews/BIND_R2.txt`) |
| R3 (diff-only, last) | `7aebdf2e…` | 9.5 PASS | 9.4 PASS | FAITHFUL | OK (`reviews/BIND_R3.txt`) |

**Card changes since v1.5** (tag vs the previous text; pointer = commit, section log)
| change | rows | tag | pointer |
|---|---|---|---|
| Row 3.3 / Thm 5 swap to W3-START2-R (faster rate when nulls are uncorrelated with truths; larger locality sets) | 3.3 | STRONGER | `a33d890d`; thm5 v0.3 |
| (A5) scope stated plainly: no leakage outside the true model, e.g. independent predictors; AR/block not covered | 3.6 | EQUAL | `7d24291a`; thm10 v0.9 [AUD-B11] |
| Rows 3.1/3.2 swap to W3-RM2-R (RM2-R-plus/RM0-plus/DLV-0; RM2-F-plus); old masters stay ACTIVE | 3.1, 3.2 | MIXED (STRONGER: Thm 7 constant-level signal/visibility, mode-form core; WEAKER: delivery needs IDEAL-W⁺, valid input) | `ff35f6b0`; thm6 v0.8, thm7 v0.6 |
| Start input repinned to `W3-START2-R:IF-START@1.0.0` (Thm 10's (A5) is now (L-R⁺⁺), covered only by the new master) | 3.6 | STRONGER | `ff35f6b0`; thm10 v1.0 [REPIN] |
| Freeze requote vs main 14892123 (T03♯ accepted: SOP:TH09/TH128 PROVED-CHECKED); abstract Form A | 1.1, 1.2, 1.4, 2.2, 3.1, 3.2, 3.6 | EQUAL | `3b3b0969`; card v1.9 |
| Time-guard sentence [GUARD-W] | 3.1, 3.5, 3.6; 3.2 | EQUAL | `54785728`; `68443dcc` |
| R1 scope restorations: 3.2 case (b) signal clause; 3.3 "with probability →1"; 3.5/4.1 potential-record evidence, nothing conditional on completion; 3.6 AR/block only "particular designs satisfying Thm 6's conditions"; 3.7 "Buys" narrowed; Thm 1 lower-bound domain; Thm 7 limits; moderate-n shape = observation; R3 historical | 3.2, 3.3, 3.5, 3.6, 3.7, 4.1 | WEAKER (restores masters' scope) | `bf4495e8`; card v1.11 [R1-*] |
| Delivery-route sentence corrected (frozen F-UNI@2.1.0 states the shipped cap; only C-DLV Prop-F used ℓ_n) | 3.1, 3.2 | EQUAL | `bf4495e8` [R1-F6] |
| R2 editorial items (13) | 3.1, 3.5, Thms 1, 6, 7, 10 | EQUAL | `68443dcc`; card v1.12 [R2-*] |

**Known pending editorial (post-freeze; not in MANIFEST_R3):**
- R3 opus items 1–2: comma splice in thm10 honest limits; DLV-0 condition note in R4's unused "Not claimed" remark.
- [AUD-S4] (W3-AUDIT v1.3, theory/W3-AUDIT f98cf498, WRITING_DELTA_v1.3.md item 4; EQUAL, concerns Song–Liang's paper):
  card row 3.1 "Buys" — replace "but prove nothing about its selection output" by "their statements on the sampler's output
  are limits in the number of iterations at fixed data (supplement pp. 12–13, 16–17); they prove nothing at a finite
  computational budget or jointly in n"; card row 2.1 "Buys" (Corollary 9C comparison) — "the sampler's output, which they
  do not treat" to be aligned to the same wording.
- RM2-R READER_DELTA F-UNI cap sentence (manager-queued, RM2-R ticket).

## Rows 3.1, 3.2, 3.6 — before (card v1.5) / after (card v1.12), statement column
**3.1 before.** **Main theorem: the reported model is the truth (Gaussian rows).** Under visibility, a leakage set of size $\le n^b$ ($b<\tfrac12$) with locality, population sparse eigenvalue floors and local regressions inside the leakage set: on one data event of probability $\to1$, every admissible run that produces output, for every seed and calibration outcome, reports $S_0$. *Delivery clause (body only until resolved [H5-2]):* the code has two fixed integer limits; under the delivery conventions (idealised machine, covered configuration, sufficient declared allocation) every run produces output on the bounded domain of $(n,p_{\mathrm{raw}})$ where neither limit is reached, and, under IDEAL-W⁺ (the two limits lifted), for every $n$, with $P(\hat S=S_0)\to1$ [FUNI-N]. The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5].

**3.1 after.** **Main theorem: the reported model is the truth (Gaussian rows).** Under visibility, a leakage set of size $\le n^b$ ($b<\tfrac12$) with locality, population sparse eigenvalue floors and local regressions inside the leakage set: on one data event of probability $\to1$, every admissible run that produces output, for every seed and calibration outcome, reports $S_0$. *Delivery clause (body only [H5-2]):* under the delivery conventions (S4) — idealised machine with two code size ceilings lifted, shipped configuration, sufficient declared allocation, valid input — every run produces output and $P(\hat S=S_0)\to1$; the error splits into a posterior-mode term and a search term (remark). The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5]. Neither limit can bind unless $n+p+1>2^{10^6}$ or $n\gtrsim4\times10^9$, that is, at no feasible problem size [RM2R-6]. The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output. [GUARD-W] [RM2R]

**3.2 before.** **Reported model, fixed design**: same conclusion under sample-level visibility and bounded leakage, with $|Q\setminus S_0|\le(1-\delta)\log n$ or $|Q|\le n^b$ plus local regressions.

**3.2 after.** **Reported model, fixed design**: same conclusion under sample-level visibility at a fixed multiple of $\log n$, bounded leakage, beta-min at the standard $\sigma\sqrt{\log n/n}$ scale (constants in remarks), with (a) $|Q\setminus S_0|\le(1-\delta)\log n$, or (b) $|Q|\le n^b$ plus local regressions and beta-min at $\sigma_*\sqrt{(|Q|+\log n)/(n\varphi_0^2)}$ with a sufficiently large fixed constant, as in Theorem 7 (A5)(b); the standard $\sqrt{\log n/n}$ scale applies to case (a) [R1-S2]; same order of clauses as 3.1 [H5-7.3]; delivery clause as 3.1, including its sentence on the two fixed integer limits [RM2R-5]. The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output. [GUARD-W] [RM2R]

**3.6 before.** **The printed outputs are consistent** (Gaussian rows, sampler branch) [S2-F4, S2-F5]: in Theorem 10's setting — signal fixed on the standardised scale, Theorem 2's population floor, Theorem 5's visibility and no-leakage conditions — the errors $|\hat Z/Z-1|$, $|\log\hat Z-\log Z|$ and the sup-norm error of the pooled PIPs, multiplied by the indicator of calibration success, are $O_P(n^{-1/2}e^{C\sqrt{\log n}})$; the probabilities of "calibration succeeds and the MPM is wrong" and of "the run completes and the reported model is wrong" tend to zero. (Intersections, not conditioning: no lower bound on the probability of calibration success is claimed. On completed runs these are the printed fields.)

**3.6 after.** **The printed outputs are consistent** (Gaussian rows, sampler branch) [S2-F4, S2-F5]: for designs with no leakage outside the true model (Theorem 5's (A5)), such as independent predictors — AR and block designs are **not** covered — and in Theorem 10's setting (signal fixed on the standardised scale, Theorem 2's population floor, Theorem 5's visibility condition), the errors $|\hat Z/Z-1|$, $|\log\hat Z-\log Z|$ and the sup-norm error of the pooled PIPs, multiplied by the indicator of calibration success, are $O_P(n^{-1/2}e^{C\sqrt{\log n}})$; the probabilities of "calibration succeeds and the MPM is wrong" and of "the run completes and the reported model is wrong" tend to zero. (Intersections, not conditioning: no lower bound on the probability of calibration success is claimed. On completed runs these are the printed fields.) The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output. [GUARD-W] Outside (A5): for particular AR or block designs that satisfy Theorem 6's visibility, leakage, floor and local-regression conditions, row 3.1 still gives the reported-model result [R1-F5, R1-S1(opus)]; and row 3.5 (unbiased evidence) needs no design condition; consistency of the printed PIPs, MPM and $\hat Z$ is not claimed there [AUD-B11].

Status column after: 3.1 `W3-RM2-R:RM2-R-plus@1.0.0` (+ `RM0-plus`, `DLV-0`), 3.2 `W3-RM2-R:RM2-F-plus@1.0.0` (+ same), each
"PROVED-CHECKED, conditional on C-DLV:L2-S3, C-DLV:P1-Inventory; council R3, MANIFEST 5d6d3c90…, sol=9.5 PASS, opus=9.4 PASS";
3.6 `W3-SAMP:C@1.1.4`, `TR@2.1.4`, `LT#@2.0.4`, `D@2.1.4` "PROVED-CHECKED"; `W3-START2-R:IF-START@1.0.0` "PROVED-CHECKED; council R2, …";
`W2-APP:POST@1.0.7` "PROVED-CHECKED"; NEW assembly R4 (unchecked).
