# R05 — X5/X6 lemma check (Sol)

Reference: STATEMENT.md **v3 — LOCKED**, claims (C1), (C3), (C4). Reviewed the supplied lemma texts and the specified sources; this is a check of X5 and the assembly in X6, not an independent certification of X2–X4. No source or lemma file was edited.

## Verdicts

* **X5: VERIFIED-WITH-AMENDMENTS.** Two MAJOR repairs are required: condition on the raw design (or retain its scales), and make the zero-pair event two-sided. The uniform partial-covariance argument and the unique-mode argument otherwise work.
* **X6: VERIFIED-WITH-AMENDMENTS**, conditional on its cited path lemma and on the X5 amendments. The MAJOR conditioning repair also applies to its posterior de-randomisation. The operational integration and delivery arguments then work with exactly the stated premises and amended allocation.

No FATAL finding: I found no counterexample to the locked asymptotic conclusions. These verdicts do not verify the unamended on-event statements literally as written.

## Numbered issues

### 1. MAJOR — Standardised X does not determine the random signal coefficients

**Locations:** X5:6–7, 12–17, 19, 34, 59–60; X6:7, 24–28, 45–47, and the conditioning in 58–59.

**Reason.** Model R defines X = CX^r D_x^{-1}. Consequently D_x, and therefore theta* = D_x beta, is generally not measurable with respect to this standardised X. X6:27–28 explicitly asserts the contrary. Moreover, the event A_n in X5 includes sample-scale inequalities, so it is not an event in standardised-X space. The supremum over x in A_n and the assertion that a deterministic standardised design sequence fixes the coefficient sequence are not justified as written.

This is substantive rather than merely a random-coefficient notation issue. Already for p = s0 = 1, the Gaussian column's centred direction (hence standardised X) is independent of its nondegenerate chi-distributed length. Given standardised X, sd_1 remains random. Thus Y given X is a mixture of signals X sd_1 beta_1 plus Gaussian noise, not the fixed-mean Gaussian model to which T03-sharp is being applied. Independence of e and standardised X is true, but does not make the mean fixed.

**Fix.** Throughout these two proofs introduce Z := X^r (equivalently, for these calculations, Z := (X,D_x)) and condition on Z. Regard A_n as a raw-design event. Both the partition and theta* are then Z-measurable, while e | Z is N(0,sigma^2 C). Replace the conditional suprema by suprema over z in A_n and the selected deterministic sequences by z_n in A_n, inducing deterministic pairs (X(z_n),theta*(z_n)). All stated constants and beta-min envelopes are common over these pairs. Apply OP/M5 conditionally on Z and integrate over Z. This preserves every locked joint-law conclusion. An H0 statement conditional only on standardised X must be interpreted through this fuller conditioning, not by asserting theta* is X-measurable.

### 2. MAJOR — The zero-pair event is one-sided, but its use is two-sided

**Locations:** X5:37–39 versus 48–50 and the event in Lemma X5:55.

**Reason.** As defined, E_2^X bounds the signed random variables r_l^T e / ||r_l|| only from above. A large negative residual satisfies that event, yet its square need not be at most 2 sigma^2(20+L_n). Thus the displayed bound for P_l^0 in the zero-pair case does not follow. E_1 only supplies an O(log n) squared bound in general; it does not supply the O(log log n) bound used to make the determinant penalty dominate. FACB L2.2 explicitly uses absolute values, which were lost in this adaptation.

**Fix.** Define E_2^Z := { |r_l^T e| / ||r_l|| <= sigma sqrt(2(20+L_n)) for every zero pair in the realised block }. Set it to the whole space if there are no zero pairs. With at most 2^15*16 = 2^19 pairs, the ordinary two-sided Gaussian bound costs at most 2^20 exp(-(20+L_n)), exactly the stated failure allowance. No change of rate, constants in the subsequent bound, or partition assumption is needed. Update the event in Lemma X5 and its use in X6.

### 3. MINOR — Explain the extension of X1.4(g2) to blocks missing truths

**Locations:** X5:21–25; source X1.4 header and (g2).

**Reason.** X1.4 is stated for T containing S0 and its proof bounds the OLS coefficient by writing b(0) = theta*_T/s + G_T^{-1}X_T^T e/s. That representation is not valid for a general block U union {l} missing truths. X5's extension is true, but does not follow verbatim from that particular line of the source proof. The RSS/omega representation for supersets of S0 must not be imported for positive pairs in incomplete blocks.

**Fix.** Add the general argument: for any nonempty T with the eigenvalue bound,

    ||G_T^{-1}X_T^T y|| <= ||y|| / sqrt(lambda_min(G_T))
                           <= 1/sqrt(c0),

since ||y||^2 = n-1. The resolvent and inverse-diagonal bounds in (g2) then give the identical uniform ridge-versus-OLS error for any T, including incomplete blocks. The Schur identity for Q is algebraic and needs no truth-containment assumption. Treat U empty with empty-vector conventions. This repairs the citation without requiring the other standing conditions q_T <= 1/10 or noise/energy bounds from X1.4.

### 4. MINOR — State the source and event conventions precisely

**Locations:** X5:6, 14, 39–40, 62–64.

**Reason/fix.**

* Replace the two references to STATEMENT v2 by v3. The relevant hypotheses remain compatible, but this review is against the locked v3.
* The CR status quotation is not verbatim from CR_corr_tails.md. Its exact status clause is `PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)`. The shorter `... (R19)` is inherited from FACA's abbreviation; either quote the actual source clause or explicitly label it an abbreviation.
* The implication to the s^2 interval uses A_n and E_1 as well as E_3, rather than the chi-square event alone. State the intersection. Indeed, |mu^T e| <= sum_{j in S0}|theta*_j| max_j|x_j^T e| = O(sqrt(n log n)) uniformly on A_n intersect E_1. Combining this with E_3 and ||mu||^2 <= 2(n-1)s0||vartheta||^2 proves the stated interval eventually, with common onset.
* K = p and p <= n/2 hold eventually under (P-1/2), not necessarily at every admissible n. Add “eventually” to Remark (1); the asymptotic proof already allows this onset. The finite-n delivery proof does not require K = p.

## Detailed checks of X5

**Design event (X5.1): passes after Issue 1.** CR/[CONC-prime] gives exactly 3n^{-2} with A = 1 for sufficiently large n, since p <= n eventually. Its affine invariance covers arbitrary raw means. Unit marginal population variances give the sample-sd concentration by chi-square bounds and a union over p. X2.1 implies the asserted minimum eigenvalue on its high-probability event; that event need not itself be design-measurable to establish the marginal probability of the design-eigenvalue event. No independence of the three components is needed. For p = 1 take the off-diagonal condition as vacuous.

**Population versus sample (X5.2): passes.** In sign-corrected coordinates the relevant dimension d is at most 16+s0, independent of p. For correlation matrices the entries are bounded by 1; ||R_UU^{-1}|| <= 1/c0, and

    B^{-1}-A^{-1} = B^{-1}(A-B)A^{-1}.

Consequently the displayed partial-covariance functional is Lipschitz in its matrix and coefficient arguments with constant C(c0,d)||vartheta|| on the bounded coefficient domain supplied by A_n. Use ||Rhat_V-Sigma_V|| <= d delta'_n and ||theta*-vartheta|| <= delta'_n||vartheta||. Both endpoints have inverse bounds (the population eigenvalue is at least 1-rho), so the inverse-difference identity suffices directly. The estimate is simultaneous over all index sets of this bounded size; there is no union-probability cost and no p-dependent Lipschitz constant. Random theta* is harmless once its raw scales are included in the conditioning.

The compound-symmetry covariance formula is the FACB population identity, including U empty. FS-a covers null l with missing truths; FS-b covers truth l. There are only finitely many values as the truth positions and p change, so c_FS > 0 is a common constant. If U contains S0, the sample signal is annihilated exactly; one must use this exact identity, rather than an O(delta'_n) approximation, for zero pairs. X5 does so correctly.

**Noise and realised partition: passes after Issue 2.** For any A of size at most 16, ||P_A e||^2 <= ||X_A^T e||^2/[c0(n-1)], proving the claimed uniform bound even for adaptively selected U. The coordinate Gaussian union bound is uniform over all standardised designs. Conditional on Z, each zero-pair residual direction is fixed, centred, and has Gaussian variance sigma^2. There is at most one truth-containing block because s0 >= 1. Its conditional number of pairs is bounded by an absolute constant; no independence of these pairs or independence of the partition and xi is required. The chi-square law is also uniform. L_n = log log n is supplied by X1 and tends to infinity while being o(log n).

**Single flips and maximisation (X5.3–X5.4): passes with the repairs above.** The normalisation is correct: P_l^0 uses y = Y/s, explaining the s^2 denominators in both bounds. The positive-pair signal is order n and dominates the noise uniformly, giving P_l^0 >= c2 n eventually with the stated conservative c2. The ridge correction is negligible, psi_U <= n, and the prior ratio is at least 1/(2p). For zero pairs, RSS_U = ||e||^2-||P_U e||^2 and the repaired two-sided event give an O(L_n) data contribution against a -(1/2)log n determinant contribution. The addition prior ratio is at most 1; the reverse removal ratio is at least 1. FACB L2.4 then excludes every S different from S*, including when no block contains all truths and when N0 is empty. Finite Omega guarantees existence and uniqueness. The uniform conditional failure bound integrates over Z. The emitted mode follows from uniqueness, without a new tie-rule claim.

## Detailed checks of X6

**H0 and T03-sharp (X6.1): passes after Issue 1.** The constants phi0^2 = c0, g0 = c0, A = 1/2 and M = 2s0||vartheta||^2 are common for all sufficiently large n. Every principal submatrix has the lower bound, so both anchored requirements hold, including j0 = ceil((2A+1)s0)+1 and the tail-cutoff m_n^sharp. The latter exists since R_K = 0; it is deterministic and data-free under the fixed prior and dimensions. The same eigenvalue bound covers all its anchored sets, including their intersection with the available coordinates. BM-infinity has the common lower envelope (min|vartheta|/2)^2 c0 n/(sigma^2 log n). The coefficient sequence is allowed to vary deterministically after fixing z_n; T03-sharp does not require a constant coefficient vector.

With deterministic raw-design sequences, the contradiction argument is valid: failure of the supremum expectation limit selects a subsequence bounded below; extend choices to the remaining indices in the events. T03-sharp along that deterministic triangular array yields convergence in probability, hence convergence of the bounded expectation, a contradiction. This follows the quantified argument in FACA L5.1 and FINAL s3's Random designs paragraph; it does not infer an expectation rate or a universal onset from O_P. The common eventual onset may depend on the fixed class parameters and the (P-1/2) envelope.

**Path and cap (X6.2): passes as an assembly from X4.** Lemma X4 quantifies simultaneously over every null subset N with size <= 15, so substitution N = N0 requires no independence from xi or W. Intersect its joint-law event with the repaired X5 start event. The nondegeneracy event has probability one: for fixed n there are finitely many l,T, and the centre equality is a nontrivial continuous Gaussian equation after conditioning on its independent centre parameters. CAP(a) includes a scan at the terminal centre; equality a_n = m0 would already suffice for certification. The m0 = 0 case is included. The legacy-cap size bound accounts for the final scanned neighbours and is correctly limited to the LS0 route.

**OP/M5 integration (X6.3): passes after Issue 1.** OP is a pathwise inclusion, and conditional fixed-raw-design M5 applies with the fixed induced signal. Define D_n(z) using the potential-run event, not the actual-output event. Then E_Z D_n(Z) = D_n and D_n <= P(K_n^c). Exact branches only add the truth when it is feasible. Integration needs no uniform OP constant; the bound has coefficient 1. The posterior term is controlled by X6.1, and the output/no-output identity gives the claimed liminf equality. CAL is included on this route as required by the cited premises.

**Delivery (X6.4): passes with the specified qualifications.** For each finite n,p, nonsingular Gaussian marginal columns are finite and nonconstant almost surely. Conditional on the raw design, the centred Gaussian response has no atom at zero in 1-perp. Thus no columns are dropped and p_raw = p. The PSD ridge argument Q_S >= y^T y/(n+1) > 0 applies even without full rank or K = p; it is exactly the class-independent part of A2 step 1. The remaining Lemma S structural invariants are reused with their code-reading-audit qualification, not newly proved here.

The total tier-1 fallback and the full amended allocation (including current-head preflight terms) are explicit premises. A2 step 2's class-independent exit walk therefore excludes no-output events conditionally on every admissible raw design outside the stated null set, and integration gives P(no output)=0 at every admissible n >= 3. This finite-n argument does not invoke the asymptotic design event A_n. It is an extension of Proposition F's argument, not an assertion that its original list of classes already included this model.

For consistency, A2 step 3 explicitly reuses the pointwise D-prime argument with K_n for the cap a_n. On output, K_n implies truth was scored (or exact enumeration scored it); if pi(S0)>1/2, truth uniquely wins the all-scored HPM. Hence the stated inclusion and Markov bound are correct. No use of the converse of OP, no inference of discovery from D_n -> 0, and no CAL or calibration-success assumption occur on this delivery route.

## Source-status and numerical audit

FACB L2 and L5 retain their local `PROVED (by this seat, unchecked)` headers with recorded checks; they serve as templates, not random-design theorems. FACA L5.1 supplies the every-sequence/common-envelope reasoning, not permission to treat D_x as measurable in standardised X. X1, X2 and X4 currently have `PROVED (by this seat, unchecked)` status; this review does not upgrade them.

The quoted T38-(0), T03-sharp, OP, CAP, and A2 status clauses in X6 agree with their cited recorded clauses (T38 checked also against SoP's TH05.0 registry row). `PROVED (A2), checked by A3` is recorded in FINAL s6; the standalone A2 file itself opens with `EXTENDS`. X6 properly retains the OP, e4/N3 and S.3 qualifications and disclaims inherited council approval. The CR quotation needs the verbatim repair in Issue 4. Proposition F's original class restrictions are extended by supplying its inputs, not silently discarded.

Read N5X_out.txt and n5x_start.py as evidence only: the recorded 48/48 matches, 24/24 at n=10^8, use the realised sample-correlation partition and production start-mode routine, including cases with N0 nonempty. These runs do not test uniform conditional quantifiers or prove either lemma. No numerical rerun was needed, and no scratch files were created.

**Required disposition:** repair Issues 1–2 before treating X5 or X6 as verified proofs; apply the local clarifications in Issues 3–4. No change to locked claims (C1), (C3), or (C4) is required by this check.
