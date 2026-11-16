# W3-READER leg 2 — strength gates for the five-pillar theorem rows (LIFECYCLE §4.2) — v0.1, 2026-11-16

Scope: `BRIEF_LEG2_GATES.md` (rows 1.1–1.4, 3.1–3.3, 3.5–3.7 of `CLAIMS_CARD.md` v0.5). Detailed tables (hypothesis by
hypothesis, with file:line evidence) are in the helper files, read and spot-checked by the lead:
`helpers/GATES_G1.md` (rows 1.1–1.4, 3.7; helper G1, Opus 5.5) and `helpers/GATES_G2.md` (rows 3.1–3.3, 3.5, 3.6;
helper G2, Opus 5.5). This file gives each row's three verdicts, the lead's resolutions of the items the helpers left
OPEN, and the dispositions. The recorder's file is `gates_staged.tsv`.

**Sub-par signal: none.** No literature dominance on any row; every easy strengthening proposed by a blind sharpness
review has a recorded triage disposition or a rider ticket (G1 :9-29; G2 :20-41).

## Summary
| Row | Masters | lit | necessity | better |
|---|---|---|---|---|
| 1.1 | `W3-POST2:C`, `W3-POST2:E` (re-base, H5-1); `W3-POST:Thm-1`=`SOP:TH09` ($O_P$ form) | PASS | PASS | PASS for Thm-1 (sharp1 f15, class B); **re-based masters: in-ticket R03b, 4 proposals awaiting HQ disposition; blind verdict requested (SHARP3 addendum g05–g06)** |
| 1.2 | `W2-APP:POST` (+ Thm-1 item 6) | PASS | PASS | PASS (sharp1 f06, class B) |
| 1.3 | `W3-PSHARP:A`, `:B` | PASS | PASS | PASS (sharp2 f02: A → A1 adopted, rider T12; B SHARP) |
| 1.4 | `W3-MISR:MIS(i)`, `MIS(i')`, `MIS(ii)`; reader version `Cor-G(b)` | **PASS (resolved here)** | PASS | PASS (sharp2 f00/f01; A2 → rider T13) |
| 3.1 | `W3-RM2:RM2-R` + `W3-RM:RM-0` + `W2-UNI:F-UNI` | PASS | PASS | PASS (sharp2 f03 D/B/C; sharp1b f19 B → T2; sharp1 f14 B) |
| 3.2 | `W3-RM2:RM2-F` (+ RM-0, F-UNI) | PASS | PASS | PASS (sharp2 f03 A1 → rider T4) |
| 3.3 | `W3-START2:START-R`, `W3-START:FLOOR` | PASS | PASS | PASS (sharp2 f09 A2 → T10; f04 SHARP) |
| 3.5 | `W1-N1:Thm-N1` (+ `W3-READER:PoolZ`) | PASS (credit Del Moral) | PASS | PASS (sharp1 f01, class B park) |
| 3.6 | `W3-SAMP:C`, `TR`, `LT#`, `D` | PASS | **PASS (resolved here)** | **PENDING (SHARP3 g00–g03, submitted)** |
| 3.7 | `W3-SCR:A1` | **PASS (resolved here; comparators partly recalled)** | PASS | **PENDING (SHARP3 g04, submitted)** |

---

## Row 1.1 — posterior concentration, fixed design (Thm 1, 1′)
- **lit: PASS.** G1 :31-55 (vs Song–Liang 2015, Narisetty–He 2014, Yang–Wainwright–Jordan 2016, Castillo–Schmidt-Hieber–van
  der Vaart 2015, Johnson–Rossell 2012; dominance NO; input TH128 carries LIT-STAT "modest extension of Rossell 2022").
  Re-base addendum (lead): the expectation form $E[1-\pi(S_0\mid y)]\le C\sqrt{\log n/n}$ uniformly over designs is
  *stronger in mode* than the convergence-in-probability statements compared there; Theorem 1′'s residual-signal
  margin is the same kind of condition as Narisetty–He's identifiability (their Condition 4.4, residual signal on
  underfits; G1 row 1.1 table and `W3-POST/ASSUMPTION_MAP.md:76-87`), here with a ridge residual and the coded prior.
  No result compared covers the coded prior; no dominance.
- **necessity: PASS.** G1 :56-65 per hypothesis (Gaussian noise OPEN-but-standard; $p\le n^A$ NECESSARY-FOR-ROUTE /
  ARTEFACT (both readings compatible); fixed $s_0$ near-NECESSARY by W3-PSHARP B; energy ARTEFACT with a numerical
  counterexample to removal (MISR N5); floors: anchored part NECESSARY at the beta-min scale (numerics), rest ARTEFACT;
  beta-min order necessary by numerics, constant ARTEFACT). Re-based masters (lead): (OS) — its unweighted feasible part
  is NECESSARY (POST2 A2, deterministic), weights ARTEFACT; (F₀) ARTEFACT (N8; R03b E-floor+); (ID$^M$) constant $c_1$
  ARTEFACT, no converse proved (`W3-POST2/ASSUMPTION_MAP.md`, rows POST2-OS, POST2-F0, POST2-ID).
- **better.** Thm-1: sharp1 f15 IMPROVABLE-EASY, triage class B (A residual → W3-PSHARP, now PROVED-CHECKED); its
  proposals (F_w)→(OS), (F_λ)→margin, expectation rate are exactly POST2 A1/E/C, now adopted as the re-base (G1 :66-76).
  **Re-based masters POST2 C/E:** in-ticket better review R03b (gpt-6-astra high; `W3-POST2/REPORT.md:173`), proposals C+
  and D+ adopted (HQ approval noted pending), A+ (weaker (OS)), E+ ($c_1\approx54$), E-floor+ ((F₀) → bounded ridge
  cost), B+ open (`W3-POST2/REPORT.md:184-187`) → **HQ to disposition**. Blind API verdict: sharp1/1b f18 returned no
  text; **SHARP3 addendum g05–g06 requested** (manager, 2026-11-16). Gate: PASS for the $O_P$ form; PENDING-DISPOSITION
  for the re-based form.

## Row 1.2 — random Gaussian design (Thm 2)
lit PASS, necessity PASS, better PASS — G1 :80-123 (sharp1 f06 class B; superseded parts covered by POST2; T5
Corollary 1R v2 not launched). Correctness note (not a gate): `W2-APP:POST` Sol line check HQ-queued.

## Row 1.3 — the rate cannot be improved (Thm 3)
lit PASS, necessity PASS, better PASS — G1 :127-170. Rider T12 (expectation lower bound for every $p$) will make
Theorem 3(b) STRONGER; READER_DELTA expected (row thm3 "Pending delta").

## Row 1.4 — omitted variables (Thm 4)
- **lit: PASS (resolved by the lead).** G1 :174-189 compares with Song–Liang Theorem 4 (STRONGER: rate, no fixed
  variance) and C-MIS; open was Rossell (2022). Lead's comparison, from the text of arXiv:1806.04071 (Bayesian Analysis
  17(2) 2022), §3.5, Proposition 6 (read in `pdftotext` output of the arXiv PDF, pp. 15-17):

  | item | Rossell (2022), Prop. 6 | ours (MIS(i), Cor-G(b)) | vs |
  |---|---|---|---|
  | truth | $f^*=N(W\beta^*,\xi^*I)$, $X$ misses columns of $W$ or non-linear terms (fixed $X$, $W$) | GR$^c$: centred residual $N(0,vI)$ about $x\beta$, any intercept; Gaussian rows in Cor-G | comparable (both Gaussian, mean misspecification) |
  | prior | Zellner's prior $N(0,\phi\tau n(X_k^\top X_k)^{-1})$, general model prior | the shipped ridge $g$-prior ($g=n$) and capped BB(1, p) | incomparable (different priors) |
  | variance | needs $\phi_t^*/\xi^*\ll\log\lambda_{tm}$ ("holds in standard cases where $\xi^*$ and $\phi^*_t$ are constant") | **any** residual variance $v>0$, constants free of $v$ | **ours stronger** |
  | conclusion | per-model bounds on $E_{f^*}p(M_m\mid y)$: polynomial for spurious, $e^{-\lambda^\gamma_{tm}/2}$ for non-spurious | $\sup_\kappa E[1-\pi(S_0\mid y)]\le C\sqrt{\log n/n}$ (total mass, uniform), HPM/MPM/PIP rates | incomparable form; ours gives a total-mass uniform rate |
  | covariance misspecification | Prop. 7 (heteroscedastic / correlated errors) | not covered (scalar covariance; (PR) total-variation remark only) | **theirs broader** |
  | dimension | $p$ growing under their conditions B1–C2 | $p\le n^A$, $s$ fixed | incomparable |

  **literature dominance: NO** (different prior; their variance-ratio condition excludes our arbitrary-$v$ regime; their
  covariance results are broader and should be cited as such). Recommend one sentence in the paper crediting Rossell's
  KL-projection framework and his Proposition 7 for covariance misspecification.
- **necessity: PASS** — G1 :190-213 (energy relative to $v$ cannot be dropped: MISR N5; margin/beta-min order as row 1.1;
  GR$^c$ scalar covariance needed for the mean-only target).
- **better: PASS** — G1 :214-221 (sharp2 f00/f01; A2 cosmetics → rider T13; MIS(i)/(i′) IMPROVABLE-HARD items are upstream
  POST2, class B).

## Row 3.1 — main theorem, reported model, Gaussian rows (Thm 6)
lit PASS, necessity PASS, better PASS — G2 :43-115. Notes: RM2's own in-ticket better gate (BT2 P1–P5, P7 "ADOPT in
v1.5") awaits HQ at RM2's CP3 (G2 :36-41); rider T2 (delivery and mode interface) would make the delivery clause
unconditional on output. Correctness/registry notes (not gates): F-UNI correctness gate PENDING (recorder); audit
adjudication of F-UNI's (S) wording in progress.

## Row 3.2 — reported model, fixed design (Thm 7)
lit PASS, necessity PASS, better PASS — G2 :119-169 (sharp2 f03 RM2-F: A1 → rider T4, which will weaken (A1)/(A3) of
Theorem 7; READER_DELTA expected).

## Row 3.3 — start law (Thm 5)
lit PASS, necessity PASS, better PASS — G2 :173-221 (FLOOR SHARP; START-R A2 → T10 within START2 v1.5; READER_DELTA
expected).

## Row 3.5 — unbiased evidence (Thm 10 remark; PoolZ)
lit PASS, necessity PASS, better PASS — G2 :225-271. **Lead's adoption of G2 caution 1:** N1 is Del Moral's
unbiasedness of SMC normalising-constant estimates instantiated for the coded method (calibration frozen first); the
card and the paper must credit Del Moral and present the contribution as "for the method as coded, calibration
included" (card v0.6 change). `W3-READER:PoolZ` adds only the equal-weight pooling (linearity).

## Row 3.6 — printed outputs consistent (Thm 10)
- **lit: PASS** — G2 :275-295 (no published result about the coded fields; SMC consistency literature compared).
- **necessity: PASS (resolved by the lead).** G2 :296-311 classifies every hypothesis; one item was left OPEN:
  **P-START ($\mathbf 1_{\mathcal A}o_0\to0$) for the $\hat Z/Z\to1$ clause → ARTEFACT** (keeps `improvable`). Written
  reason: P-START is the regime that Theorem C's T-free route needs (W3-SAMP STATEMENT.md:163, "the regime in which the
  start already concentrates on S₀; the bridge has no mass to transport"); it is not a property any consistent evidence
  estimator requires — SMC evidence ratios are consistent along tempering paths without start concentration under
  stability conditions on the kernels (the standard SMC route; Del Moral 2004, **recalled, not re-read**), which the
  project has not proved for the coded kernels. The trap example (`sharpness.tsv:213`, $\pi_0(S_0)=1.5\cdot10^{-8}$ with
  P-CONC true, failing at fixed small $L$) is finite-$n$ and shows that *some* start or mixing condition is needed in
  kind, not that P-START is. For the PIP/MPM/HPM clauses P-START is ARTEFACT already (TR route under P-OVL∞).
  G2 caution 2 (registry `sharpness.tsv:208` reads `W3-SAMP:LT# / P:POST-CONC = NECESSARY`, its source says sharpness of
  the bound only) → recorder: correct to NECESSARY-FOR-ROUTE.
- **better: PENDING** — SHARP3 g00–g03 (submitted by HQ); sharp1b f20 partial items (P-MAP localisable to $\mathcal A$;
  pooled non-collapse may suffice in LT♯) to be confirmed there.

## Row 3.7 — certified screening (Thm 8)
- **lit: PASS (resolved by the lead; part of the comparators recalled).** G1 :225-240 compares with Song–Liang
  Theorem 3 (sure screening of posterior PIPs; incomparable object). Lead's addition for the open screening /
  L0-local-optimum comparators:

  | item | ours (A1) | SIS, Fan–Lv (2008) (**recalled, not re-read**) | best-subset / splicing, Zhu et al. (2020, PNAS) (**conditions not re-read**) | vs |
  |---|---|---|---|---|
  | object | certified local optimum of the coded Bayesian score (the software's certificate) | marginal-correlation screening set of size $d\asymp n$ | output of a polynomial-time L0 algorithm | incomparable objects |
  | guarantee | one-sided: certified models of size $\le q_n$ contain $S_0$ w.p. $\to1$ | sure screening (contains $S_0$) | exact support recovery | incomparable (theirs two-sided for splicing) |
  | design | sparse floor on $(q_n+s_0)$-sets (master: directional floor) | conditions on $\Sigma$ incl. bounded spectrum and marginal-signal strength | SRC/eigenvalue-type conditions | ours needs no marginal-signal condition |
  | signal | fixed $\theta_{\min}$ (A1° at $\sigma\sqrt{L_n/n}$) | minimal signal $\gtrsim n^{-\kappa}$ | beta-min | comparable |

  **literature dominance: NO** (no compared result is about a Bayesian method's certificate; the two-sided splicing
  guarantee is about a different algorithm). Flag for the manager: the SIS and splicing comparisons are from memory /
  abstracts, not re-read; a re-read would upgrade this to a fully cited table (≤ 1 h; not blocking).
- **necessity: PASS** — G1 :241-250.
- **better: PENDING** — SHARP3 g04 (submitted).

## Recorder notes (from the helpers; not gates)
`sharpness.tsv` inconsistencies (G1 :21-26): FIXED-S0 "NONE" although W3-PSHARP proves bounded $s_0$ necessary for the
rate; ENERGY "NONE" although MISR N5 is a numerical counterexample; no rows for `W3-MISR:Cor-G(b)`; `W3-SCR:A1` "NONE";
`W3-SAMP:LT#` POST-CONC "NECESSARY" → NECESSARY-FOR-ROUTE (G2 caution 2).
