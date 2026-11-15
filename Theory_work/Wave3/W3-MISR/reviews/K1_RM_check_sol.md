# K1 — blind lemma line check (Sol)

Scope: `R_reduction.md`, `M_misr.md`, against W3-MISR STATEMENT v1.2 §§0–4. POST2 claims are treated as declared inputs; their proofs were inspected only to establish their literal hypotheses, scope and constants. No review files other than the brief were opened. No git operations were performed.

## Per-item verdicts

| Item | Verdict |
|---|---|
| R′(a) | VERIFIED |
| R′(a′) | VERIFIED |
| R′(a″) | VERIFIED |
| R′(b) | VERIFIED |
| R′(c) | VERIFIED |
| R.6 | VERIFIED |
| MIS(i), including consequences and stability | VERIFIED |
| MIS(i′)(a) | VERIFIED-WITH-AMENDMENTS |
| MIS(i′)(b) | VERIFIED-WITH-AMENDMENTS |
| MIS(i′)(c) | VERIFIED |
| MIS(i′)(d) | VERIFIED-WITH-AMENDMENTS |
| MIS(ii)(a) | VERIFIED |
| MIS(ii)(b) | VERIFIED |
| MIS(ii)(c) | VERIFIED |

The amendments concern the common input ledger in M.2; they do not require an additional theorem hypothesis or a changed conclusion.

## Numbered findings

1. **MINOR — Restore the size hypotheses explicitly in the single-n input ledger.** `Theory_work/Wave3/W3-MISR/lemmas/M_misr.md:49` announces that the hypotheses named in each input are the hypotheses at that n, but (I3) at lines 54–55 names only G, (E), (F₀), (I4) at lines 56–57 supplies no replacement size qualification, and (I5) at lines 58–60 again omits R1's size conditions. The cited sources retain R1: `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md:53` explicitly says “under G, (E) and R1 alone”; its (C4′)–(C5′), lines 55–74, continue that setting; `Theory_work/Wave3/W3-POST2/lemmas/E_visibility.md:26` explicitly assumes R1 in E1(b). In particular the thresholds use p ≤ n^A and fixed s₀, A, not merely G, (E), (F₀). **Required change:** introduce M.2's ledger with a standing assumption “s₀ = s ≥ 1 fixed, A ≥ 1 fixed, 2 ≤ p ≤ n^A, s₀ ≤ K, at this n” applying to (I1)–(I6), or repeat these qualifications in (I3)–(I5). Explain that the asymptotic portions of R1 are replaced by these per-n conditions and the common threshold. The applications already impose these conditions at `M_misr.md:67–68`, so this is an input-statement omission, not a gap in the resulting bounds. It affects the presentation of (i′)(a), (b), (d).

Counts: **FATAL 0; MAJOR 0; MINOR 1; NIT 0.**

## Checks answering the brief

### R.1–R.2: deterministic identities and parameter map

`R_reduction.md:17–26`: C1 = 0; the centred vector scales by c, its sample SD by |c|, and its standardised value by sgn(c). Both score quadratic forms are even. All weights and their positive normaliser therefore agree. For u ≠ 0, Uu has zero mean and norm ‖u‖ > 0, hence is non-constant. This establishes (R1) and (R2), including their domains.

`R_reduction.md:30–36` uses exactly the working posterior and response-scale image in W3P STATEMENT:26–28 and POST2 STATEMENT:101–103. For c > 0 the standardised response itself is unchanged; multiplying s_y by c gives the stated joint image map and (R3). Positive c is sufficient for this proof and for the later normalisation by √v. A negative-c extension would require the reflection equivariance of the standardised coefficient posterior; it is not being asserted here. Shift invariance of the joint posterior follows because both the standardised response and s_y are unchanged.

### R.3: code and numerical record

Every table row agrees with the current code at the cited lines: `v3_fit.R:97,104–118`, `v3_preprocess.R:19–33,37–68,123–127`, `v3_setup.R:7–13`, and `cpp/v3_score.h:14,55–60,217–223`. The C++ link is `cpp/v3_core.cpp:91–96`. In exact arithmetic the anchored standardisation branch also returns Cy/s_y. The scorer's small-Q recomputation, `cpp/v3_score.h:145–159,219`, is the identical penalised minimum formula, so it does not introduce raw-scale dependence. Timing-based resource checks receive the standardised inputs (`v3_fit.R:110`); the target claim is unaffected by such checks.

A recursive search over all `.R`, `.h`, `.cpp` files under the permitted core directory found `s_y|y_sd|y_max|y_mean` only at `v3_preprocess.R:126–127`, as claimed. (`rg` was unavailable; PowerShell Select-String was used.) Metadata can be passed as a whole list without contradicting the narrower statement that these values enter no score.

`N0_code_invariance.R:11–12,46–50,61` gives 3×7 exact transformed fits and four SMC transformed fits. `N0_out.txt:40,48` records the quoted maxima 1.304e−10 and 1.037e−11, with all status/HPM comparisons true. These observations are distinguished from the real-arithmetic claim. No numerical rerun was needed or performed.

### R.4–R.5: laws, kernels and projective stability

The affine Gaussian contrast vector is nonzero almost surely since v > 0. The equality in law in `R_reduction.md:60–71` follows from the same deterministic map of identically distributed standard Gaussian contrasts. The identification with W3P model G has α* = 0, raw slope β/√v and variance 1; D_x has positive diagonal, so support is preserved. This also proves independence of the posterior law from the unspecified intercept law.

Φ is continuous away from zero. For Ψ, the kernel assertion at line 68 is justified by the literal conditionals POST2 STATEMENT:103 (also P1:162,174–178): a finite mixture with continuous weights, Gaussian means/covariances and positive IG rates on that domain. Thus its evaluation on Borel parameter sets is measurable; the induced random probability is measurable. No additional residual decomposition is used.

`R_reduction.md:75–80` has the correct factor nN in Q_S. Positivity follows from P1:93–94 (indeed Q_S ≥ N/(n+1)); H_S is positive definite even for rank-deficient designs. On trace-one projections the displayed affine expression can also be written as the linear functional N tr(T) − nN tr(UᵀX_SH_S⁻¹X_SᵀUT). Normalisation is positive and continuous on that domain. The [0,1]-function form of total variation has constant one, so lines 84–86 are correct. R > 0 cancels pathwise in the example even when dependent on W. The parameter posterior retains contrast magnitude through its IG rate b₀‖z‖²/N, so it is not determined by T. Restricting (c) to model probabilities is justified.

### R.6: translation and regimes

Each row matches the cited source: SZ with POST2:86 and W3P:63–64; E with W3P:67; F₀ with POST2:25; OS with POST2:29–36; the global and coordinate ridge margins with POST2:40–42,128–129; F_λ with W3P:68–70; BM with W3P:74–75. All mean quadratic quantities divide by v; all design quantities and support-dependent index sets remain unchanged.

The theorem fixes s ≥ 1 and A ≥ 1, SZ supplies p ≥ 2 and s ≤ K, and the comparison variance is the fixed value 1. POST2 Claim C explicitly has per-n hypotheses, not an unmentioned onset requirement for OS. For the auxiliary bounds, the cutoff bound W3P:38–39 (T03R:54) yields m♯_n ≤ C(s,A) log n, making the small-sequence thresholds uniform; P3:45–49 expressly explains this threshold mechanism. The missing qualification in the ledger itself is finding 1.

### M.1: expectation, consequences, ties

POST2 STATEMENT:85–94 and C_expectation.md:9–15 give exactly the uniform per-n expectation bound and listed constant dependencies used at `M_misr.md:18–26`. Case (ii) directly covers the λ class; no conversion through c₁ is needed. Taking the supremum after the pointwise bound introduces no dependence on v.

The PIP, alternative-model-mass, HPM, MPM and ξ_q inequalities at lines 33–40 hold deterministically, including threshold equality cases. Item 3 follows from support membership and the convention of zero mass outside Ω; it needs no additional MIS1 input beyond the representation explicitly posited in the statement.

For stability, 1−π(S₀) is a posterior functional. A measurable mode selection from the data need not itself be a function of the posterior. Line 30 correctly restricts that particular functional argument to posterior-based tie rules; the theorem's error bounds for arbitrary measurable tie rules nevertheless follow from {HPM ≠ S₀} ⊆ {δ ≥ 1/2}. Under arbitrary response laws one can apply R′(c) to the posterior functional 1{δ ≥ 1/2}, or use Markov with the stable expectation bound. Thus no additional tie hypothesis is needed for the stated selection-rate conclusions, and no equality in law for every data-dependent tie selection is established or required.

### M.2: input bounds and assembly

Apart from finding 1, (I1)–(I6) match their sources. I1 is C2:34,41–42 at m♯_n; I2 is A:52–53 and E:26,31–34; I3–I4 are A:64–74 with the stated enlarged threshold; I5 is E:26–27,35–54 per model; I6 is T03R:187–189 for every data set. Comparison scores ℓ(S′) remain defined when S′ is outside Ω (P3:39), and the sum ranges correctly extend through min(m♯_n,p−s₀).

(a) The superset/tail split is exhaustive. Only the first OS inequality enters. The stated elementary inequalities absorb the tail and bad-event terms into a constant times r_n.

(b) Each deficient S is J′ united with a proper subset of S₀, giving at most 2^s−1 preimages. A coordinate margin suffices for I5 on precisely the small-excess models being summed. The empty J′ term is 1; the two ranges, e^{ρ_n} ≤ 2 threshold and amplified OS expectation are applied correctly. The displayed expectation bound includes both bad-event probabilities and the size tail. The union bound over at most s strong coordinates gives the claimed s factor.

(c) P3:146–151 is the cited signal lemma. The floor on S∪S₀ gives Δ_S ≥ (n−1)φ₀²θ_j². Thus c″ ≥ cn/(n−1), with a non-strict inequality, is exactly sufficient for the non-strict ridge margin. L_S ≥ Δ_S is POST2:41/E:9. No missing factor of n or v occurs.

(d) The three-family decomposition is exhaustive. The same per-model I5/I6 split applies to the far family without any global margin. The expectation display counts the tail once and charges the union of the two bad events by 5/n. Models in 𝔉 have size at most s+j₀−1; S₀ has size s, and j₀ > 0. The claimed size-event inclusion follows. No application of E0 to place all near models below m♯_n is required.

### M.3: measurability and conditioning

On each fixed-p, fixed-support stratum the score weights are continuous off the zero-contrast set; extension there by g_n = 1 is Borel. The classes are Borel: Gram inverses H_S⁻¹ are continuous, support strata and ranks are Borel, and m♯_n depends only on the discrete indices (n,p,s). The finite sums/inequalities defining OS and the margins preserve measurability. Random p is handled by the specified countable disjoint union; W_n always has deterministic dimension N = n−1, with the fixed U of the statement.

The zero-contrast exceptional event has probability zero by independence and Gaussian integration. Thus δ_n = g_n(κ_n,W_n) a.s. even without an intercept restriction. Freezing the bounded jointly Borel function against an independent standard Gaussian is valid on the stated probability space and requires no regular conditional law. The latter is mentioned only as an interpretation in the final remark.

For (a), class membership is an F_n event; restricted expectations, complement penalties and deterministic selection-error inclusions give the stated unconditional bounds. The other posterior masses and strong-coordinate membership are also jointly Borel, so the same freezing argument applies. (b) uses finitely many measurable slices, allowing maxima of constants and thresholds. (c) first fixes η, then sends L to infinity, then η to zero; no uniformity of C^η in η is needed. The selection limsup bound follows separately by fixing η and letting n grow. These arguments cover every clause of STATEMENT §§1–4; none of their conclusions requires an additional assumption beyond the ledger clarification above.
