# 10⁴ overlap: budget re-projection after W1 (Opus child, 2026-11-19 UTC; independent model; read-only analysis)

## Decision summary (10 lines)
1. **Expected rung total = 1,534 core-h (P10 / P50 / P90 = 1,231 / 1,508 / 1,853)**, counting the 532.64 spent (W0 254.74 including 91.50 of evidence batches, plus W1 277.90). On the counted-only basis: 1,443 (1,140–1,761). This is below REPROJECTION_W0 (1,816) and below Sonnet's level (1,614), and the band is **wider** than Sonnet's (1,460–1,763).
2. **P(cumulative > 1.6k) = 0.34; P(> 2.1k) = 0.037; P(> 2.5k) = 0.008.** Almost all of the > 2.1k mass (0.0365 of 0.037) comes from draws in which a T calibration hits the 3:00 TIMEOUT and has to be re-run.
3. **W2: expected 400 (P10 / P50 / P90 = 250 / 383 / 557) against the quote of 480.** P(W2 > 480) = 0.22; P(W2 > 960, the wave stop) = 0.005. **W3: 602 (381 / 586 / 835).** Cumulative after W2: 932 (P90 1,090), so the 1.6k line can only bind during W3 (P(> 1.6k after W2) = 0.002).
4. **Per-fit risk:** P(any of the 12 remaining T fits > 172.5, including TIMEOUTs) = **0.22**, and P(a calibrate TIMEOUT at 3:00) = **0.17**. Both rest mainly on an assumption the 3 tier-1 observations cannot test: the share of slow tier-1 grids, φ. The range is 0.11 / 0.05 at φ = 0 up to 0.52 / 0.48 at a φ prior with mean 0.25. Exposure by fit: AR is exposed (7 fits, 0.195 together); ADJ-OPP less so (3 fits, 0.05); ARweak cannot breach either line (k1 ≤ 14 tops out at ≈ 157). By wave: W2 0.083 (TIMEOUT 0.062), W3 0.176.
5. **A T fit > 172.5 is also a criterion C failure (PREREG §3.7, unchanged by ADDENDUM 1), so the outcome would be at best MARGINAL.** The 172 rule is therefore a science-outcome risk of about 1 in 5, as well as a budget issue.
6. **Agreement with Sonnet:** we agree on W2 (400 against 400) and on the geometric tier-1 tail; with φ = 0 my per-fit and TIMEOUT risks are 0.11 / 0.05, against Sonnet's 0.09 / 0.04. We disagree on (a) **AR P(escalate): 0.67 here, 0.88 in Sonnet's model**, which puts my W3 79 lower; (b) **the tail**: Sonnet's P(> 2.1k) of 0.002 does not price the cost of re-running after a TIMEOUT, and it has no slow tier-1 regime.
7. **Recommended W3 quote: keep 640** (wave stop > 1,280; P(W3 > 1,280) = 0.010 at 3:00, 0.0007 with a 5:00 calibrate limit). Re-set it at the W2 read-back if the updated E(W3) is outside 580–700; the scenario range is 524–742.
8. **Option A (2.1k) is sufficient (P(> 2.1k) = 0.037), and HQ should CONFIRM it at the W2 read-back.** The stop at 1.6k would fire with probability 0.34. I recommend pairing A with **a 5:00 T calibrate limit for W3**: the same engine run, so the science does not change, but a slow tier-1 grid then completes instead of timing out and being re-run. That gives P(> 2.1k) 0.017, P(> 2.5k) 0.002 and P(TIMEOUT) 0.064 (only W2, which has already been released at 3:00 and so is left as it is). This needs HQ to accept max_task_hours 5.0 (the 3.0 limit is already a one-off exception to the 2-h rule).
9. **W2 read-back trigger** ("options to HQ if the projection's P90 > 2.1k"): I put this at ≈ 0.06. In practice it fires **if and only if a W2 T calibration TIMEOUTs** (scenarios S4 / S4b give a P90 of 2,402 / 2,292 at 3:00 for W3, or 2,211 / 2,054 at 5:00). A completed breach at k1 = 7–9 gives a P90 of 1,894–1,967 and does not fire it.
10. **If a 172 stop fires on AR or ADJ-OPP:** recommended response (§7): **continue to 40/40, record C as failed (MARGINAL), make no post-hoc change to C, and raise the calibrate limit to 5:00 for every remaining T fit.** Halting saves ≈ 600–700 but leaves AR r02–r04 unmeasured, which are the datasets the precision-study diagnosis needs. If HQ and Theory want C to be tier-aware, the time to decide is **now, before any breach is seen**, not after one. HQ decides.

## 1. What the 8 counted T fits say (W0 T2 + W1; the W0 evidence runs are the same seeds and the engine is deterministic, giving 12 = 12 and 14 = 14 rebuilds, so they are not new observations)
Per-rebuild wall times are taken from the cost-file mtimes (`W1_readback/reproj/rebuild_times.py` → `rebuild_times_output.csv`):

| fit | tier-0 rebuilds K0 | tier-0 s / rebuild | escalated | tier-1 rebuilds k1 | tier-1 s / rebuild | total core-h |
|---|---|---|---|---|---|---|
| AR r01 s1 | 14 (cap) | 246 (evidence run 213) | yes | 1 | 835 | 110.12 |
| ADJ-OPP r01 s1 | **12** | 219 (evidence run 193) | no | – | – | 48.28 |
| ARweak r01 s1 | 14 (cap) | 144 | yes | 1 | 495 | 60.72 |
| ARweak r01 s2 | **1** | 117 | no | – | – | 9.28 |
| IND r01 s1 | **11** | 249 | no | – | – | 50.53 |
| IND r01 s2 | 14 (cap) | 262 | yes | **3** | 932 | 143.96 |
| NULL r01 s1, s2 | 1, 1 | 34 | no | – | – | 2.30, 2.29 |

- **Mechanism (engine `calib.h:221-244, 266-273`):** tier 0 escalates if any trigger fires, and in all 3 escalated fits that trigger was the ℓ = 14 cap (grid_unconverged). The 5 converged fits had no trigger (E1/E2/E3/local_limit) at all. Tier 1 is final whatever happens: if it is also unconverged at 14, the run still ends `ok`. There is no time check inside the engine (`grid_stop` / `preflight_exceeds` are no-op defaults), and **calibration is not checkpointed** (only the islands are), so the only time bound is the SLURM limit of 3:00, and a TIMEOUT means restarting from zero.
- **Tier-0 K is two-regime, not geometric:** it is either 1 (the grid is identical at once: NULL × 2, ARweak s2) or **11–14+** ("slow": 11, 12, and 14+ three times). Nothing has been seen in 2–10. The seeds of one dataset disagree (ARweak 14+ / 1; IND 11 / 14+), so the seed matters more than the dataset.
- **Tier-1 rebuild ≈ 3.46 × a tier-0 rebuild** (3.39 / 3.56 / 3.44); the tier-1 pilot is ≈ 0.8 × a tier-0 rebuild. Node speed moves the per-rebuild time by ≈ ±7 % (213 against 246 s, 193 against 219 s for the same seed).

## 2. The model (my own; not the structure of `w1_projection.py`)
Script: `W1_readback/reproj/reproj_w1.py` (posterior by importance weighting of 1.5 M prior draws, then 3 · 10⁵ posterior draws, seed fixed; ESS 29 k). Output: `reproj_w1_output.txt`; `reproj_w1_quantiles.py` and `reproj_w1_extra.py` give the per-wave quantiles, the 5:00 variants and the k1 thresholds.

| component | form | prior (explicit) | posterior / value |
|---|---|---|---|
| fast regime (K0 = 1) | P = π_d | AR Beta(0.5, 3.5) (B3 / F16: AR rarely easy); ARweak, ADJ, IND Beta(1, 3) | π̄: AR 0.10, ARweak 0.33, ADJ 0.20 |
| slow regime | K = ⌈e^Z⌉, Z ~ N(μ_d, σ²); escalate iff K > 14 | μ_d = μ0 + τ·z_d (+0.15 for AR); μ0 ~ N(log 10, 0.5²); τ ~ HN(0.25); σ ~ HN(0.30) + 0.05 | μ̄: AR 2.87 (e^μ ≈ 17.7), ARweak 2.74, ADJ 2.61 (≈ 13.6), IND 2.65; σ 0.34 |
| non-cap trigger | ε on a converged fit | Jeffreys Beta(½, ½); 0 of 5 observed | ε̄ 0.083 |
| **P(escalate)** | (1 − π)·P(K > 14) + ε | | **AR 0.67 (P10–P90 0.41–0.91), ADJ-OPP 0.41 (0.15–0.68), ARweak 0.44 (0.20–0.70)** |
| tier-1 k1 | mixture: with probability φ the slow regime of that design, otherwise Geometric(p); capped at 14 | **φ ~ Beta(0.25, 4.75) (prior mean 0.05)**; p ~ Beta(1, 1) | φ̄ 0.032; p̄ 0.57; E k1 given escalation = 2.33 |
| tier-0 seconds per rebuild g0 | AR 230, ADJ 206, ARweak 144; o0 (start-up + pilot) 60 / 60 / 37 s | new datasets × lognormal(0, 0.08); node × lognormal(0, 0.06) | |
| calibrate wall | o0 + K0·g0 + esc·(0.8 g0 + k1·3.46 g0); core-h = wall × 48 / 3600 | | |
| islands | N 10⁴: AR 12.3, ADJ 12.57, ARweak 7.14; N 4·10⁴: AR 49.2, ADJ 51.3, ARweak 25.0 | × dataset factor, × lognormal(0, 0.04) | |
| setup + merge + eval | 0.09 | | |
| TIMEOUT | wall > 10,800 s: 144 core-h billed, stage fails; **re-run to completion with a raised limit** (deterministic engine, so the same k1) | | cost = 144 + full fit |
| V | AR 2.42 ± 0.25, ADJ 2.38 ± 0.25, ARweak 1.69 ± 0.12 | | W2 V ≈ 13.0, W3 V ≈ 14.5 |

Why a hierarchy on μ: the single AR cap hit is weak evidence on its own. The pooled slow fits (11, 12, 14+, 14+, 14+) put the cap close to the median of the slow regime, so a design that hit the cap once is not thereby "certain" to hit it again. AR gets a prior shift of +0.15 (≈ 16 % more rebuilds) for B3 / F16. F16's "escalation is certain at p ≥ 5k" was T *as coded* in the old engine; in this engine 5 of 8 T fits did not escalate.

## 3. Cost per T fit and the k1 lines (`reproj_w1_extra_output.txt`)
| design (node speed) | escalated, k1 = 1 | + per k1 | first k1 > 172.5 | first k1 that TIMEOUTs at 3:00 | at k1 = 14 (wall) |
|---|---|---|---|---|---|
| AR (0.92 / 1.00 / 1.08) | 102 / 106 / 111 | 9.8 / 10.6 / 11.5 | 9 / **8** / 7 | 11 / **10** / 9 | 229–260 (3.7–4.4 h) |
| ADJ-OPP | 98 / 102 / 106 | 8.7 / 9.5 / 10.3 | 10 / **9** / 8 | 13 / **11** / 10 | 212–240 (3.4–3.9 h) |
| ARweak | 58 / 61 / 63 | 6.1 / 6.6 / 7.2 | never | never | 137–157 (2.3–2.7 h) |

Not escalated: AR ≈ 47–56 (slow, K0 11–14) or ≈ 16 (fast); ADJ ≈ 44–52 or ≈ 16; ARweak ≈ 29–35 or ≈ 9.5. These lines agree with Sonnet's (AR > 172 at k1 ≥ 7 on a slow node). A TIMEOUT costs **144 wasted plus a re-run of 200–260**. **With a 5:00 limit, no remaining T fit can TIMEOUT** (the worst case is AR at k1 = 14 on a slow node, 4.4 h, and ≤ 4.8 h even with a +8 % dataset factor on top), and the worst single T fit is ≈ 260 core-h.

## 4. Projection (base, 3:00 limit; 532.64 spent)
| quantity | E | P10 | P50 | P90 |
|---|---|---|---|---|
| **W2** (6 T + 6 V; quote 480) | **400** | 250 | 383 | 557 |
| **W3** (6 AR T + 6 V) | **602** | 381 | 586 | 835 |
| cumulative after W2 | 932 | 783 | 915 | 1,090 |
| **rung total** | **1,534** | **1,231** | **1,508** | **1,853** |
| rung, counted-only basis (W0 163.24) | 1,443 | 1,140 | 1,416 | 1,761 |

- **P(rung > 1.6k) 0.34, > 2.0k 0.054, > 2.1k 0.037, > 2.5k 0.008** (counted-only basis: 0.21 / – / 0.026 / –). Without any TIMEOUT the expected total is 1,455; with ≥ 1 TIMEOUT it is 1,915. P(> 2.1k and no TIMEOUT) = 0.0001.
- **Escalations among the 12 remaining T fits: E 6.8 (P10–P90 4–10)**, so ≈ 9.8 of 20 over the rung, of which W3 AR accounts for 4.0 of 6 (P(all 6 escalate) = 0.21).
- **Wave stops:** P(W2 > 960) = 0.005, P(W2 > 480 = quote) = 0.22; P(W3 > 1,280) = 0.010.
- **Per fit** (P(escalate) / E cost / P90 / P(completed > 172.5) / P(TIMEOUT)): ARweak r02 s1, s2: 0.44 / 41 / 73 / 0 / 0.0005. ADJ r01 s2, r02 s1, s2: 0.41 / 69 / 116–120 / 0.005 / 0.013 each. AR r01 s2 to r04 s2: 0.67 / 98 / 133–136 / 0.008–0.010 / 0.029 each. **P(any > 172.5 or TIMEOUT) 0.222; P(TIMEOUT) 0.173; expected number of such fits 0.32.** By wave: W2 0.083 (TIMEOUT 0.062), W3 0.176 (0.136). By design: AR 0.195, ADJ 0.051.

## 5. Sensitivity (the three assumptions that matter; everything else moves E by ≤ 30 and the tails by little: `reproj_w1_output.txt`)
| assumption | E rung | P90 | P > 1.6k | P > 2.1k | P > 2.5k | P(any > 172.5) | P(TIMEOUT) | E W3 |
|---|---|---|---|---|---|---|---|---|
| **base** (φ̄ 0.03, AR esc 0.67, 3:00) | 1,534 | 1,853 | 0.34 | 0.037 | 0.008 | 0.22 | 0.17 | 602 |
| **(1) tier-1 tail** φ = 0 (pure geometric) | 1,487 | 1,729 | 0.27 | 0.012 | 0.002 | 0.11 | 0.05 | 571 |
| φ prior Beta(0.5, 3.5) (φ̄ ≈ 0.07) | 1,597 | 2,013 | 0.42 | 0.075 | 0.020 | 0.34 | 0.30 | 644 |
| φ prior Beta(1, 3) (φ̄ ≈ 0.14) | 1,709 | 2,256 | 0.54 | 0.155 | 0.049 | 0.52 | 0.48 | 720 |
| **(2) AR P(esc)** 0.53 (no shift, π_AR Beta(1, 3)) | 1,432 | 1,750 | 0.22 | 0.021 | 0.004 | 0.19 | 0.14 | 511 |
| AR P(esc) 0.82 (shift +0.35) | 1,630 | 1,945 | 0.48 | 0.055 | 0.012 | 0.25 | 0.20 | 687 |
| AR P(esc) 0.92 ("certain", as Sonnet / F16) | 1,682 | 1,993 | 0.58 | 0.067 | 0.016 | 0.27 | 0.21 | 736 |
| **(3) calibrate limit** 5:00 for W3 only (W2 at 3:00) | 1,510 | 1,784 | 0.31 | 0.017 | 0.002 | 0.22 | 0.064 | 578 |
| 5:00 for W2 + W3 (counterfactual) | 1,500 | 1,762 | 0.30 | 0.008 | 0.0004 | 0.22 | 0.002 | 578 |
| 5:00 + φ prior Beta(1, 3) | 1,591 | 1,947 | 0.46 | 0.045 | 0.004 | 0.53 | 0.009 | 637 |

Minor ones: the prior centre of slow K at 7 or 14 moves E by −27 / +25; ε = 0 by −28; a dataset latent (sd 0.15) by −10; a dataset cost factor sd of 0.15 by +7.
Reading: **(1) the tier-1 tail sets the per-fit and > 2.1k risks** and cannot be learned from 3 observations; the W2 escalations (≈ 2.8 more tier-1 runs expected) are the next data on it. **(2) AR P(escalate) sets the level** (E W3 511–736). **(3) A 5:00 limit removes the cost tail without changing any science.**

## 6. Reconciliation with Sonnet (`W1_READBACK.md` §7, `w1_projection.py`)
| item | Sonnet | this model | verdict |
|---|---|---|---|
| rung E (P10–P90) | 1,614 (1,460–1,763) | 1,534 (1,231–1,853) | **disagree on level (−80) and width** |
| W2 | 400 (309–502) | 400 (250–557) | agree on E; mine is wider (ADJ P(esc) 0.41 against 0.24 and the TIMEOUT tail) |
| W3 | 681 (563–774) | 602 (381–835) | disagree: AR P(esc) |
| P(> 1.6k / 2.1k / 2.5k) | 0.56 / 0.002 / 0 | 0.34 / 0.037 / 0.008 | disagree |
| P(any T > 172) / P(TIMEOUT) | 0.09 / 0.04 (0.34 / 0.21 pessimistic) | 0.22 / 0.17 (0.11 / 0.05 at φ = 0) | agree when φ = 0; the difference is the slow tier-1 regime |

- **Level: AR escalation 0.88 against 0.67.** Sonnet updates a prior mean of 0.85 (ESS 4) with 1 / 1. My hierarchy also uses the four other designs: slow fits converge at 11–12 as often as they hit 14, and a fast regime exists (ARweak s2 at k = 1 on the same X structure). With AR P(esc) set to 0.92, my model gives W3 736 and a rung of 1,682, so **Sonnet's level sits inside my AR sensitivity range**. Neither value can be ruled out with 1 AR observation; the AR r01 s2 fit in W2 is the next observation.
- **ADJ-OPP 0.41 against 0.24:** the one ADJ fit converged at 12 of 14, which my K model reads as being near the cap; a pure Beta update counts it only as "did not escalate". This adds ≈ +25 to W2.
- **Tail: Sonnet's model has P(TIMEOUT) = 0.04 but bills a timed-out fit at its full escalated cost.** In reality the stage fails at 144, and the engine (deterministic, calibration not checkpointed) must be re-run with a raised limit, so it costs 144 + 200–260. Sonnet's tier-1 is also a single geometric with an informative Beta(3, 2) prior; my mixture adds a slow-grid regime (φ̄ 0.03) that 0 of 3 observations cannot exclude (P(0 / 3 | φ = 0.1) = 0.73). These two together explain 0.037 against 0.002.
- **Agreed:** the k1 lines (AR > 172 at k1 ≥ 7–8, ADJ ≥ 8–9, ARweak never), the W2 expectation, about 10 escalations over 20, W3 being the wave that decides 1.6k, and that the monitor's 1,194 is not comparable.

## 7. Decision support for the W2 read-back (HQ decides; stopping T escalation is NOT allowed)
**7a. Option A (cumulative stop 1.6k → 2.1k).** Sufficient: P(> 2.1k) = 0.037 at 3:00, and 0.017 with W3 at 5:00. Without A, the 1.6k stop fires with probability 0.34, always during W3. **Recommend CONFIRM A.** If the W2 read-back shows a TIMEOUT (P90 > 2.1k, §8), A alone is no longer enough, and the 5:00 limit for W3 is what brings the scenario P90 down (S4: 2,402 → 2,211; S4b: 2,292 → 2,054).

**7b. The per-fit 172.5 line is also criterion C.** PREREG §3.7: "Pass iff every fit … T ≤ 172.5"; ADDENDUM 1 kept it on purpose (test `escalated_T_cost` gives MARGINAL). One breach therefore makes the best outcome **MARGINAL** (§4 rule 3: the precision study is the diagnosis, and 10⁵ stays blocked). P ≈ 0.22 base (0.11–0.52). The 5:00 limit does **not** change this, because a slow tier-1 grid gives a fit > 172.5 whether it completes or times out and is re-run.

**7c. Options if a 172 stop fires on AR or ADJ-OPP (W2 or W3):**
| # | option | extra cost (E) | budget risk after it | science / governance |
|---|---|---|---|---|
| **1** | **Continue to 40/40, record C as failed (MARGINAL), and raise the calibrate limit to 5:00 for every remaining T fit** | remaining W3 ≈ 640–680 (S3: 641, P90 816) | S3 (completed AR breach in W2): rung 1,624, P90 1,799, P(> 2.1k) 0.004. S4 (W2 TIMEOUT): 2,013, P90 2,211, P(> 2.1k) 0.25 | Pre-registered consequence; full data for the precision-study diagnosis (AR r02–r04 E1 sign / tier pattern); no deviation except the ops limit (max_task_hours 5.0, HQ) |
| 2 | Continue as in 1 but keep 3:00 | as 1, plus 144 for each TIMEOUT | S3: P(> 2.1k) 0.027; S4: 0.36, P(> 2.5k) 0.07 | Same as 1, but each further TIMEOUT is an infrastructure re-run (plan §4: one per fit) and a D gap until re-run |
| 3 | Halt the rung at the breach | saves ≈ 600–700 (W3) | none | Still MARGINAL (§4 rule 3 comes before D), but E1 is NOT_EVALUATED, there is no AR evidence beyond r01, and the 10⁴ T-vs-V link stays weakest exactly on AR, the near-edge design. Poor value: the precision study would have to cover it later |
| 4 | Pause; ADDENDUM 2 makes C tier-aware (e.g. an escalated T fit judged against 1.5 × a tier-1 model of ≈ 175, i.e. ≈ 260) | 0 | as 1 | **A deviation made after the breach has been seen**; the independent review will discount it. Defensible only if HQ and Theory decide it **before** W2's T costs are read |
| 5 | Scope cut (W3 AR T on s1 only, from W0's option C) | ≈ −300 | low | D 37/40, which weakens E1 on AR; it halves the remaining exposure but does not remove it. Not recommended |
| ✗ | Stop T escalating / cap tier-1 rebuilds | – | – | Not allowed (D-26; it changes the coded rule) |

**Recommendation:** (i) CONFIRM A at the W2 read-back. (ii) Set the **T calibrate limit to 5:00 for W3** at staging, whatever W2 shows. That means max_task_hours 5.0 in the W3 T plan (HQ acceptance) and a W3 T cap of 6 × ≈ 441 = **2,644** (calibrate 240 + islands 192 + small stages; the W2 cap was 6 × 344.7). (iii) **HQ and Theory decide now** whether C should stay as registered for escalated T fits. If it stays (my default reading of ADDENDUM 1), a breach means option 1. (iv) Pre-authorise, for W2 (already released at 3:00), **one re-run at 5:00 of any T calibrate that TIMEOUTs**, so that the fit does not sit undelivered while HQ is asked.
**Early warning for the monitor in W2:** a T calibrate still running at ≈ 2:15 of wall time (8,100 s) is an AR/ADJ fit at k1 ≥ 6. That is the time to prepare the 5:00 re-run and the HQ note.

## 8. Quotes and the W2 read-back triggers
- **W2 quote 480:** my E is 400 (P90 557); P(W2 > 480) 0.22; P(> 960) 0.005. No change needed.
- **W3 quote: keep 640** (between my 602 and Sonnet's 681; ≈ W0's 635). Wave stop > 1,280: P 0.010 at 3:00, 0.0007 at 5:00. At the W2 read-back, re-set it to the updated E(W3), rounded up to 10, if that is outside 580–700. Scenarios: S5 good 524; S1 benign 608; S2 typical-bad 630; S3 / S3b breach completed 666 / 682; S4 / S4b TIMEOUT 742 / 731 (all at 3:00).
- **"Options to HQ if the W2 projection P90 > 2.1k":** P ≈ 0.06 now, essentially P(a W2 TIMEOUT). Scenario P90s at the W2 read-back (W3 at 3:00): S5 1,469; S1 1,674; S2 1,838; S3 (AR k1 = 7, 451 in W2) 1,894; S3b (k1 = 9) 1,967; **S4 (AR TIMEOUT, 805 in W2) 2,402; S4b (ADJ TIMEOUT) 2,292**.

## 9. What this does not do / caveats
- 8 T observations. The tier-1 tail (3 observations) and AR P(escalate) (1 observation) are prior-driven; both priors are stated above and varied in §5. The W2 read-back should re-run `reproj_w1.py` with the W2 outcomes added (the `extra` list in `posterior`, as in the `--scen` block).
- Tier-0 / tier-1 split times come from mtimes (±1 s per file); `calib.bin` is not collected, so "trigger = cap" is inferred (K0 = 14 in all 3 escalations, no trigger in the 5 converged fits).
- Not modelled: queue or requeue failures, ops re-submits other than a TIMEOUT re-run, a tier-1 grid_failure fallback, and island limits (the islands at N 4·10⁴ take ≤ 2,201 s against the 7,200 s cap).
- Read-only. Nothing on NOTS, no BNP files, no git changes. Scripts and outputs: `results/overlap1e4/W1_readback/reproj/` (`rebuild_times.py` and its csv, `reproj_w1.py` and its txt, `reproj_w1_quantiles.py` and its txt, `reproj_w1_extra.py` and its txt). Python: `envs/ci-py313` (numpy 2.3.4, scipy 1.16.3), run with `python -I`. Engine source read from a read-only worktree copy of `engine_v4/include/v4/calib.h` (identical md5 in 3 worktrees; the path given in the brief does not exist in the main clone).
