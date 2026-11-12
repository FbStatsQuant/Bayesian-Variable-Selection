# W3-MISR — CHECKPOINT 1 (target fixed), 2026-11-11 23:20 CST

Lead: Claude Fable 5.2 (Claude Work, high). Branch `theory/W3-MISR`. Per the run instructions legs CP1 → CP2 are
pre-approved when reviews are clean, so the run continues after this file is committed; HQ can redirect at CP2.

## Locked statement
`STATEMENT.md` v1.2. v1.0 → statement lock L01 (Sol): **REJECT**, 0 FATAL / 1 MAJOR / 3 MINOR — the MAJOR was in a
side remark (Remark P: C-MIS Theorem F's BM-∞ was not normalised by the variance; analytic counterexample), no
finding against the main theorem. One fix round → v1.1 → re-check L02 (fresh Sol): **LOCK**, 0/0/0/0, every finding
RESOLVED. v1.2 = v1.1 + two adoptions from the better-theorem review (new clauses only).

What the statement says:
- **Lemma R′.** The coded posterior is exactly invariant under y ↦ a1 + c·y (c ≠ 0); the parameter posterior is
  equivariant; so under a Gaussian contrast residual of any variance v > 0 the law of the posterior is that of a
  unit-noise well-specified model with coefficient β/√v. Code path pinned (`v3_preprocess.R`, `v3_fit.R`,
  `cpp/v3_score.h` @ 16a7f85) and run: 25 rescaled fits of the compiled code, status/HPM unchanged, max |ΔPIP| 1.3·10⁻¹⁰.
  (c): only the law of the contrast *direction* matters, with a total-variation stability bound.
- **MIS-R (i).** sup over a configuration class of E[1 − π_𝒞(S₀^𝒞)] ≤ C·√(log n/n), for n ≥ n₀; constants free of the
  variance. Hypotheses in signal-to-noise form: energy (E^σ), floor on S₀ (F₀), superset Occam sum (OS),
  identifiability margin (ID^{M,σ}) — the W3-POST2 interface. Rates for HPM, MPM, PIPs follow.
- **MIS-R (i′).** Without a margin, in expectation: no strict-superset mass; strong coordinates are included
  (Song–Liang Cor. 2 counterpart); localisation on small-loss bounded models.
- **MIS-R (ii).** Random designs by conditioning: E[δ_n | 𝓕_n] ≤ C r_n on the good event (uniform), variance and
  coefficient measurable in the design, slices in s, tight (η-dependent) constants.
- **Cor G** (Gaussian rows, any n-dependence of σ², τ²; C-MIS's "τ_n² fixed" caveat removed). **Cor H** (in-sample
  Hellinger contraction around the projected law: the Song–Liang Theorem 4 analog; added beyond T1 items (a)–(d)).
- **Remarks.** W3-POST Theorem 1 and W3-POST2 A1, B, C, D, E hold with n-dependent σ*² in SNR form (item (d) of the
  brief); C-MIS Theorem MIS and Theorem F likewise.

## Necessity reading (ASSUMPTION_MAP.md; numerics/misr_numerics_out.txt, N5_out.txt)
| hypothesis | reading | evidence |
|---|---|---|
| fixed σ², τ² (v1) | **removed** | exact invariance; N1 (posteriors agree to 5·10⁻¹⁴ across v_n = n⁻² … n²) |
| Gaussian contrast residual | weakened to the direction law (R′(c)); Gaussianity itself looks improvable (t₃: no effect), hard, upstream | N3(i) |
| scalar covariance | needed for a named target; heteroscedastic residual degrades the rate; a random slope changes the target unless conditioned on | N3(ii), (iii); C-MIS E2 |
| margin relative to v | the relative form is the right one (v1's "R02 counterexample" is a margin failure) | N2 |
| (E^σ) energy | **cannot be dropped** (Astra's obstruction, confirmed: E π(S₀) 0.87 → 0.003); weakenable | N5, N4 |
| (F₀), (OS), c₁, fixed s, p ≤ n^A | inherited from W3-POST2 (improvable / partly necessary / artefact / hard) | W3-POST2 map |

## Better-theorem review (BT1, Astra, blind) — dispositions (`reviews/BT1_disposition.md`)
| proposal | disposition |
|---|---|
| A1 direction-law form of GR^c + TV stability | adopted (v1.2 §1(c), §2) |
| A3 localisation without margin; first (OS) inequality for supersets | adopted (v1.2 §3(a), (d)) |
| A2 Corollary H in expectation with posterior-tail rates | recommend a ticket on W3-POST2:D (upstream; transfers through R′) |
| B1 empty projection s = 0 at growing p | recommend a ticket (new lemma; upstream first) |
| B2 fresh-covariate (out-of-sample) Hellinger | recommend a ticket, low priority |

## For HQ
1. **Input assurance.** W3-POST2:A0/A1/C/D/E are ACTIVE and council-passed, but their registry status is still
   "PROVED (by this seat, unchecked)" (HQ_DECISIONS:48-49 says PROVED-CHECKED). Under rule 11 every MIS-R status
   carries "conditional on W3-POST2:…" until the acceptance record exists.
2. **Scope.** Corollary H and the adoptions A1, A3 go beyond T1 items (a)–(d); each has its own status and can be
   struck without touching the rest.
3. **Supersession.** MIS-R implies the main clauses of C-MIS:Thm-MIS(i), (ii); the decision is HQ's (LIFECYCLE §5.3).
4. Whether BT1 must be repeated on v1.2 (the changes are its own class-A proposals).

Commit: see LOG.md. Agents so far: Sol ×2 (L01, L02), Astra ×1 (BT1), all codex, reasoningEffort high.
