# LC1 — line check of R1_VIS, R2_NEC + statement-change check (SL1 rows) — reply of Sol (codex gpt-6.1-sol, high), verbatim
# Brief: reviews/BRIEF_LC1_sol.md. Received 2026-11-15 (see LOG.md).

| file | verdict |
|---|---|
| `lemmas/R1_VIS.md` | PASS |
| `lemmas/R2_NEC.md` | PASS |

| row | confirmed tag | OK? |
|---|---|---|
| v1.5 — VIS-c, VIS-m, NEC-b use quantitative [TK]; explicit visibility refinements retain (E), (GF-16) | STRONGER | Yes |
| v1.5 — (D3) relation remark | EQUAL | Yes |
| v1.5 — definition of R^♯_n off {Q = S₀}; deterministic-envelope consequence (a3) | EQUAL | Yes |
| v1.5 — §4 scope wording; PLAN section reference | EQUAL | Yes |

Findings: none. No C, S, F or E correction is required for the requested mathematical and statement-change checks.

R1 checks:

- **(D3) and supersession.** The substitution c_V ↦ c_V − 2A preserves the old visibility exponent. The bound c_Q/p ≤ 16s₀ makes log n + 2 log(p/c_Q) nonnegative for n ≥ 256s₀², proving (V-m) ⇒ (V-mp) with unchanged margin constants. The comparison correctly distinguishes agreement of the constant-level thresholds from the persistent negative-price improvement in the margin form.
- **Exact margin price.** R1.2 correctly obtains Π ≤ π/2 + C₂ for d ≥ a and Π ≤ π/2 for a > d. Neither calculation requires log(p/c_Q) ≥ 0. Multiplying the visibility inequality by θ_n/2 preserves its direction even when π + c_m log n is negative. For π < 0, θ_n ≤ 1 gives the favorable sign; for π ≥ 0, the stated uniform upper bound on π supplies the required error control. The constants, summation and threshold n₃ yield the claimed bound.
- **Constant-level visibility.** R1.3 retains log(2p), including its log 2 correction. The 2 log p contribution cancels the factor 2p in e_n exactly. The stated n₄ inequality supplies sufficient slack, and the application of AGG-d includes its required condition c_QU_Q ≤ 1.
- **START-F and uniformity.** The cited BASE and PARENT arguments support the substitutions in R1.5. Visibility changes the exponent, admissibility condition and visibility thresholds; the leakage estimates, assembly constants and probability arguments remain applicable. BASE L6.0 and the PARENT high-probability form retain their stated dependence on ε. Both displays of (T1⁺⁺)(d) have constants and thresholds depending only on the listed quantities, uniformly over admissible designs, Q and h. The case s₀ = 0 is covered separately.
- **Interface hypothesis.** VIS-c⁺⁺ and VIS-m⁺⁺ use only the quantitative toolkit and their other stated premises. Their proofs do not require an additional partition-free Gram floor or energy hypothesis. The explicit refinements under (E), (GF-16) follow from the cited toolkit construction.

R2 checks:

- **Fixed necessity bounds.** R2.1 and R2.2 retain the exact log p contributions from the prior and cancel them against the pointwise level. The lower bound for leaking nulls imposes no upper bound on their actual gains. The weak-truth argument permits negative fixed c whenever its premise is feasible and justifies the small-ratio expansion uniformly.
- **Drifting constants.** R2.3 correctly separates gains of order log n from larger gains. In the first case, the stipulated gap dominates the Gaussian cross term; in the second, the toolkit lower bound gives divergence without linearizing the gain. R2.4 bounds the weak-truth gain by (1 + 2A) log n and controls the expansion remainder. Both arguments establish convergence in probability under precisely the stated drifting conditions.
- **NEC and the pigeonhole.** The cited PARENT counting argument supplies a deterministic witness with a proper truth subset in both ranges of s₀. NEC-b⁺⁺ then proves both conclusions of N2⁺⁺. The witness set for N3⁺⁺ is also within its quantified family. N1 and N4 faithfully retain their cited content.
- **Example R2.6.** The coefficient choice gives the exact gain-to-variance ratio G*_n. Orthogonality gives zero null gains and hence (AL), while the Gaussian construction supplies the required small-set Gram floor for every allowed polynomially bounded sequence p_n, including p_n > n − 2. The singular-value estimate, Laurent–Massart application and union bound have sufficient constants. The example supports the stated sharpness of the coefficient 1.
- **F4⁺⁺.** The level vector and tail budget are valid. The J2 calculation retains e^{G_n/2} = p n^{c_n/2} exactly. The prefactor absorption is valid for n_F = 16, yielding C_A = 2√(1 + 2A) + 1 uniformly over c_n ≤ 1. The displayed bound and both stated (AL) consequences follow.
- **Supersession.** Each old necessity premise implies its new premise with the stated limsup/liminf slack. Taking η sufficiently small recovers every old necessity exponent. For F4, a slowly vanishing slack recovers the old n^{o(1)} bound, and a fixed sufficiently small slack recovers its (AL) condition.

Statement-change check:

All four v1.5 changes are present as described. STRONGER is correct for restoring the quantitative [TK] hypotheses: R1/R2 prove the interface claims under those premises, while retaining the explicit visibility refinements under (E), (GF-16). The other changes preserve mathematical content: the relation remark is corrected, R^♯_n is fully defined, (a3) follows by substitution of O_P envelopes into (a2), and the scope wording matches the stated reference-set restrictions. No dependent clause breaks.

LC1-VERDICT: PASS
