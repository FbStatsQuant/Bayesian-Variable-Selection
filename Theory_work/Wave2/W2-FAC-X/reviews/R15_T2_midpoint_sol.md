# R15 — Independent Target-2 midpoint review

**Verdict: CONTINUE.** No FATAL or MAJOR issue found. The locked v2.1 claims have a viable proof in the supplied files. The issues below admit local repair; I found no need to change the architecture, strengthen the statistical hypotheses, or narrow the claimed exponent range.

This review uses the locked statement, the requested proof files, X1–X6, FAC-B's statement and L1–L5, and the binding protocols. I did not read other reviews, LOG.md, PLAN.md, CHECKPOINT.md or REPORT.md. Status annotations in proof headers are not evidence for my verdict. The cited posterior-consistency, operational-closure and delivery results are treated as upstream inputs, with their stated premises retained.

## Reasons

**Right target and method fidelity.** FAC-GL covers arbitrary deterministic loading arrays in a fixed compact subset of (0,1), under the explicitly strong population condition (FS-G) and the explicitly restricted exponent A_S. Its proof does not assume finitely many loading values or favourable loading-class proportions. FAC-NCS is a separate iid-row result under the stronger dispersion rate and the CS non-masking hypothesis. This matches v2.1; it does not recover the withdrawn exact-Gram corollary. The score retains the ridge and determinant terms and the BB(1,p) size ratio. The search compares all flips and swaps, allows the production tie rule, and uses the merged MR1 cap. There is no substitution of backward elimination for the actual search: backward elimination is established by comparison with every competing move.

**Exact Gram: the uniform argument closes.** In T2/L4r_path.md §L4r.0, whitening and Sherman–Morrison give the loading-specific statistic and exact gains, including the loading-dependent determinant correction. Consequently the argmin assertion is justified only within a common loading value, exactly as the locked statement says.

The important step is §L4r.2(a):

    sum_{i in K_T} ell'_i tau_i = kappa'_S X_T + varrho.

Positivity of every loading rules out all retained residuals being large in the unfavourable direction. This gives one good deletion at every T, without any path or interval assumption. The split at m = log n in §L4r.3(i) correctly yields deletion coefficient

    d_del = 1/2 - A_1 max(1, gamma_bar) > 0.

For additions, the top-square-sum bound and Cauchy–Schwarz control every possible retained subset. Keeping the size-prior contribution is essential: it supplies the subtractive Z_m^2 term in §L4r.3(ii), leaving

    d_add = 1/2 - A_1 ((1+R)^2 - 1) > 0.

The errors are uniformly o(log n), including when p is bounded. One can choose, for example, c = min(d_del,d_add)/2 for all sufficiently large n. Uniformity over sets is obtained by deterministic inequalities on one probability event, not by an unjustified union bound over exponentially many sets.

Null-out swaps telescope through T minus j, where the same uniform addition bound applies. Truth moves are handled separately by the eigenvalue floor and the uniform projection-noise bound; they are not inferred from null-statistic perturbations. This establishes strict termination at S0 and pure deletion paths from every permitted start. The failed loading-class invariants outside §L4r.0–L4r.3 are not needed.

**Iid rows: the transfer is strong enough.** X9 changes the reference baseline to kappa_0 = N/phi^2 and uses the correctly normalised statistic s_j(T), rather than importing an exact-Gram score identity literally. The operator-norm estimate controls every principal submatrix simultaneously and costs

    delta_bar_n H_bar
      = O((p/sqrt(n) + sqrt(p log(n)/n)
            + sqrt(log(n)/n)) H_bar^2) = o(1).

This is affordable under A_1 < A_S <= 1/6. The denominator normalisation has a positive lower bound depending only on the loading bounds. The change kappa_0 = 1 + O(n^(-1/3)) perturbs the deletion coefficient by o(1); the ridge, determinant and RSS multiplier errors do not consume either logarithmic margin. In particular, X9 does not need the Target-1 band lemma or Gaussian independence of a data-selected set. Its swap comparison remains valid at arbitrary intermediate supersets of S0.

**Start mode and assembly.** X8's replacement of the CS partial-covariance formula by (FS-G) is appropriate: only fixed-size population/sample functionals enter, and their Lipschitz constants are uniform over block positions. Conditioning on the raw design is the right treatment of the random partition and the zero pairs. The issue in the exact-Gram event wording is listed below, but the increment argument itself survives. The start contains S0; the uniform path statement therefore applies without independence between N0 and the noise. The path length is at most the emitted centre's size, so the MR1 cap supplies a certified endpoint. X10 preserves the separate discovery and posterior-concentration inputs, uses the every-sequence argument for random designs, and retains Proposition F's allocation and fallback premises. It does not infer delivery from D_n -> 0 alone.

**Near-equal loadings: rerunning Target 1 is justified.** X7 retains the CS reference centre and puts the loading discrepancy into the statistic error. Under Delta_n H_bar_n <= n^(-1/3), this is absorbed by a fixed enlargement of Target 1's existing error scale. That scale still satisfies the small-regime spacing bound, the tail-spacing and window-count bounds, band absorption, and p w^2 + w log n = o(1). Thus the transfer does not assume that a small perturbation preserves the exact deletion order. It reruns the approximate-argmin/soft-gap induction. CS non-masking also survives uniformly because the relevant CS values form a finite nonzero list and Delta_n -> 0. Restricting this corollary to iid rows avoids the false exact-Gram multiplier import identified in its own proof header.

## Numbered issues

1. **MINOR — Exact-Gram raw-scale event is incorrectly declared automatic.** Location: lemmas/X8_start_general.md:29–31, importing the event at lemmas/X5_start.md:15–20. That event includes max_j |sd_j - 1| <= delta'_n. Exactness of the *standardised* Gram and fixed theta* do not make raw column standard deviations equal to one. For example, take an admissible centred standardised X, raw design 2X, and raw coefficients theta*/2. All exact-Gram hypotheses hold, but sd_j = 2, so the imported event with delta'_n = 0 fails. **Fix:** define the (G) version of the design event using R_hat = Sigma_n, the eigenvalue floor, and theta* = vartheta directly; omit the raw-sd condition. Then apply the conditional noise bounds and block-increment proof to this event. No raw-scale assumption or theorem narrowing is needed.

2. **MINOR — Make onset dependence on non-masking explicit.** Location: STATEMENT_T2.md:41–42,49–51 and lemmas/X8_start_general.md:26–28. The start proof needs both the onset of (FS-G) and C delta'_n <= c_FS/2, followed by domination of logarithmic penalties by a term of order n c_FS^2. Hence its onset can depend on c_FS and on the prescribed array's hypothesis onsets. These are not controlled solely by the displayed loading bounds and coefficient vector. The explicit disclaimer of simultaneity across arrays prevents a substantive uniformity claim, but the current parameter list is incomplete if read as exhaustive. **Fix:** add c_FS and the hypothesis onsets, or explicitly allow dependence on the fixed array. Keep the path-margin constant independent of c_FS; that part is correctly proved.

3. **MINOR — Frontier wording exceeds the evidence stated.** Location: T2/L4r_path.md:166–169 and STATEMENT_T2.md:72–76. A finite numerical positive-addition example at exponent 0.33 does not prove that a 1/6-type threshold is intrinsic asymptotically, nor that the uniform-over-sets route cannot go much beyond A_S for arbitrary loading arrays. The locked statement subsequently acknowledges the lack of a sharpness proof, but the categorical opening and the lemma's “so ... intrinsic” wording are stronger. **Fix:** say that the present estimates yield A_S and that the numerical examples suggest a limitation of the uniform route; reserve asymptotic necessity or sharpness for a proof. This affects the frontier commentary, not FAC-GL or FAC-NCS.

**MAJOR+ issues: none.** Proceed to the final sweep after the local corrections above. No nonlocal gap or counterexample to the locked v2.1 theorem/corollary was identified.
