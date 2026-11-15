# Blind council review R1 — seat sol

**Score: 9.3 / 10.0. All six gates PASS.** Findings: 0 FATAL, 0 MAJOR, 0 MINOR, 1 NIT.

Reviewed the frozen R1 package identified in the brief as manifest `d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d`. Read the statement, all three proof files, assumption map, all six numerical scripts/outputs, and CITECHECK. Opened the specified upstream statements, proof files, and code; checked the cited interfaces rather than re-auditing the declared W3-POST2 hypotheses. Did not open the excluded reviews, logs, plans, checkpoints, reports, or API_AUDIT material. No source regeneration or git mutation was performed.

Evidence below uses repository-relative paths and physical line numbers. `MISR` denotes `Theory_work/Wave3/W3-MISR`, `POST2` denotes `Theory_work/Wave3/W3-POST2`, `POST` denotes `Theory_work/Wave3/W3-POST`, and `MIS1` denotes `Theory_work/Wave1C/C-MIS`. `ARC` denotes `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots`.

## Six gates

### 1. Correctness — PASS

The deterministic invariance is exact for the stated real-arithmetic target: centring removes the shift, the sample SD scales by the absolute scale factor, and both response-dependent score terms are even. The parameter posterior requires positive scaling, as stated; its image law follows directly from its definition on the standardised scale (`MISR/lemmas/R_reduction.md:10-37`; `POST/STATEMENT.md:18-29`; `POST2/STATEMENT.md:101-105`). This also agrees with the transformed-posterior identity in `ARC/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:173-208`.

The contrast-law reduction uses only the law of the N-dimensional contrasts; no independence or Gaussian assumption on the intercept is needed (`MISR/lemmas/R_reduction.md:61-72`). The projective map is measurable and has positive score denominators. Its TV bound has coefficient one for [0,1]-valued functions, and the random radial multiplier example cancels pointwise even when dependent on the Gaussian direction (`MISR/lemmas/R_reduction.md:76-90`). The parameter-posterior extension is correctly withheld under PR alone.

MIS-R(i) is a direct application of Claim C at unit variance, with the target support preserved. The deterministic PIP, model-mass, HPM, MPM and thresholded-model inequalities are sufficient for every consequence, including proxies and cancellations (`MISR/lemmas/M_misr.md:23-45`). The no-margin expectation assemblies explicitly integrate nonnegative upper bounds on the good events and charge their complements by probability. Their underfit multiplicity is at most 2^s, and comparison unions outside the cap are legitimate score comparisons (`MISR/lemmas/M_misr.md:77-128`; `POST2/lemmas/A_occam.md:64-86`; `POST2/lemmas/E_visibility.md:56-68`; `ARC/W1-T03R/PROOF.md:187-197`). Localisation correctly charges every model above the cutoff to the tail; it does not need to assume that all near models are below that cutoff.

Conditional freezing, finite support-size slicing, and the tight-constants argument are valid (`MISR/lemmas/M_misr.md:132-168`). In particular the order of quantifiers in part (ii)(c) yields tightness by first choosing eta and then L; it does not assert an unconditional expectation rate from merely tight envelopes.

Gaussian conditioning gives G(a), including degenerate omitted/noise components with positive total variance. G(b)'s SD, sparse-eigenvalue, energy and beta-min events imply the claimed class membership (`MISR/lemmas/G_corollaries.md:26-60`). H is the image of the declared D(a)/(b) result, with both mean and variance thresholds scaled correctly (`MISR/lemmas/G_corollaries.md:68-86`). The reference-law paragraph correctly distinguishes a mean-centred response from the random sample-centred response and limits its KL interpretation to G (`MISR/STATEMENT.md:181-191`; `MISR/lemmas/G_corollaries.md:87-92`).

SNR, the MIS and F transfers in P, the vanishing-SNR counterexample, and U's disjoint-model contradiction are sound (`MISR/lemmas/G_corollaries.md:96-161`). For P's counterexample the rescaled mean has squared norm (n-1)/n^2, so comparison to pure noise in TV is legitimate; `MIS1/lemmas/L6_null.md:6-33` supplies exactly the bounded-p null result used.

### 2. Hypotheses used equal hypotheses stated — PASS

The class definitions impose SZ, energy, the floor on the target, and both OS inequalities at the particular n. The normalisation table preserves all these conditions and the bounded-excess family exactly (`MISR/STATEMENT.md:43-61`; `MISR/lemmas/R_reduction.md:94-109`). Claim C explicitly supplies the uniform per-n statement consumed here (`POST2/lemmas/C_expectation.md:9-15`). The more detailed extraction for (i') records the per-n size conditions and common thresholds rather than silently treating an isolated design as an asymptotic array (`MISR/lemmas/M_misr.md:54-75`).

Only the first OS inequality is used for strict supersets; the amplified second inequality is used for large-excess underfits in the coordinate and localisation bounds. The coordinate margin is imposed only on models omitting that coordinate. The conversion from coefficient threshold to margin retains the necessary n/(n-1) factor (`MISR/lemmas/M_misr.md:83-113`). G(b) separately assumes fixed projection sparsity and the required population eigenvalue range; neither is inferred from Gaussianity (`MISR/STATEMENT.md:165-167`; `MISR/lemmas/G_corollaries.md:37-55`). H(b) retains E, F0 and OS, despite dropping the selection margin.

### 3. No hidden assumptions — PASS

Nonconstant retained columns, nonconstant response, positive total residual variance, measurable mode selection, zero padding, random p, and the configuration sigma-field are explicit (`MISR/STATEMENT.md:18-41`). The conditional proof supplies a jointly Borel kernel and identifies measurable class events without requiring regular conditional laws on an arbitrary underlying probability space (`MISR/lemmas/M_misr.md:132-147`). A regular conditional description is only an interpretation of the independent-noise formulation.

Coefficient uniqueness is not presumed. The statements concern a chosen representation, and U establishes support uniqueness only when both representations satisfy the concentration hypotheses and the finite-n error is below one half. Singular candidate designs are allowed where OS and the other stated conditions permit them. Noise variance zero is allowed in G(a) only when the aggregate variance is positive. No raw intercept estimation or floating-point invariance assumption enters the proofs.

### 4. Cited inputs and statuses — PASS

The W3-POST2 inputs remain declared hypotheses, not independently certified conclusions of this review (`MISR/STATEMENT.md:214-224`). The proof-file status lines list the claims actually consumed: C for (i), C/E/A1 for (i') and its conditional extension, A0 additionally for G(b), D/C for H, and all transferred POST2 claims for SNR (`MISR/lemmas/M_misr.md:3-6`; `MISR/lemmas/G_corollaries.md:3-13`). The larger dependency list for G(b) is conservative, not an upgrade. R's identities are proved directly.

Checked the OS bridge against `POST2/lemmas/A_occam.md:14-27`, the size-tail expectation against `POST2/lemmas/C_expectation.md:31-42`, the local comparison against `POST2/lemmas/E_visibility.md:23-54`, and the parameter-posterior transfer against `POST2/STATEMENT.md:101-119`. The inherited C-MIS statements used in P match `MIS1/STATEMENT.md:54-78,124-141` and `MIS1/lemmas/L4_theoremF.md:148-194`. The older T03 scale paragraph says only what the package attributes to it (`ARC/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex:380`). CITECHECK's zero failures were treated as supporting bookkeeping, not a substitute for these checks.

### 5. Constants, rates and thresholds — PASS

The unit-variance constants are selected before the configuration and therefore are free of v. All additional thresholds depend on the listed fixed constants; the onset of the population beta-min envelope in G(b) is explicitly sequence-dependent (`MISR/lemmas/M_misr.md:23-31,73-75`; `MISR/lemmas/G_corollaries.md:39-58`). The expected size tail is O(n^-1/2)+O(1/n); the superset contribution is at most 2 C_OS r_n; the bounded-excess contribution is O(n^-2)(1+O(r_n)); the large-excess contribution is O(r_n); and complement probabilities are at most 5/n. Each is bounded by a constant times r_n (`MISR/lemmas/M_misr.md:81-105,122-125`). The coordinate beta-min conversion uses c'' >= cn/(n-1), not c'' >= c.

For G(b), k_n=O(log n), so 2n^-2+2k_n n^-2+n^-1=O(1/n); the population-to-sample floor and beta-min factors are conservative. C_H is evaluated at unit variance and hence depends only on (s,A), as claimed (`MISR/lemmas/G_corollaries.md:42-58,70-81`; `POST2/STATEMENT.md:112-115`). The Theorem F table correctly scales the full mean and EP residual, uses the effective variance for BM(c), normalises BM-infinity by the true variance, and preserves TL as a ratio (`MISR/lemmas/G_corollaries.md:130-147`). Finding 1 is an ancillary numerical-description typo, not a constant used in a proof or theorem.

### 6. Fidelity to the coded method — PASS

Verified the path from response preprocessing to C++ context and score: `Scripts/SMC_BVS/core/v3_preprocess.R:37-68,111-130`, `v3_fit.R:97-118`, `v3_setup.R:7-12`, `cpp/v3_core.cpp:91-117`, and `cpp/v3_score.h:39-70,204-223`. Standardisation's anchored branch gives the same centred, sample-SD-normalised vector in real arithmetic. The IG rate is the fixed 0.01 on that scale. The raw-scale metadata has no downstream score/prior consumer in the searched core files. Exact/SMC branch selection uses n and retained p; timing/resource guards are correctly kept outside the statistical target claim.

The N0 description matches the script and recorded output: 21 transformed exact fits and four SMC fits; seven exact transformations include both signs and scales 10^-150 through 10^150; the SMC tests use the stated four transformations and common seed. The recorded maxima are 1.304e-10 and 1.037e-11, below the statement's 1.4e-10 (`MISR/numerics/N0_code_invariance.R:11-12,43-62`; `MISR/numerics/N0_out.txt:15-48`). This is correctly described as finite-input observation, with no floating-point theorem.

## Numbered findings

1. **NIT — incorrect threshold comparison in the N5 docstring.** `MISR/numerics/N5_energy_obstruction.py:5` says c=200 exceeds c1 for s=1..2 at A=1. Substitution in `POST2/STATEMENT.md:130` gives c1(2,1)=258.904638985645. Thus 200 does not exceed that threshold. Moreover the comment in lines 5-6 describes all runs as satisfying the same 200-level ridge margin, whereas the bounded-energy control need not satisfy that exact finite-n inequality. This does not invalidate the energy obstruction: its large first signal contributes a diverging ridge loss in the a=1 arm, and the alternative beta-min route has c0(2,1)=192.

   **Exact fix:** replace lines 5-6 of the docstring with: “theta_2 = sqrt(c log n / n), c=200 > c0(2,1)=192 (the beta-min threshold); c1(2,1) is approximately 258.9. In the a=1 obstruction arm, all hypotheses of MIS-R(i) except energy hold eventually: OS is empty, the design floors hold, and every underfit has ridge loss exceeding any fixed multiple of log n.” Keep the numerical outputs unchanged. This is an advisory description correction; no main claim or proof depends on the false comparison.

## Scope, strength and non-claims

The claims are substantive and not vacuous. Orthogonal or well-conditioned Gaussian candidate designs with bounded nonzero signal-to-noise coefficients give nonempty classes for large n. The strong-coordinate clause can be vacuous when its recovered set is empty, and strict-superset exclusion alone does not exclude replacement proxies; both limitations are acknowledged in `MISR/STATEMENT.md:125-134`. Tight constants give an O_P rate, not the stronger unconditional expectation conclusion of G(b).

No overclaim relative to C-MIS was found. The removed fixed-variance restriction is replaced by exactly the relative energy and signal conditions needed by the invariant target. The F transfer does not silently identify the deterministic EP residual with Gaussian omitted noise.

The Song–Liang comparison is appropriately qualified: fixed candidate size and support inclusion there, growing candidate dimension with fixed support here; in-sample Hellinger distance and convergence in probability here, not integrated almost-sure density consistency. Checked the comparison against `MIS1/STATEMENT.md:17-32` and `MIS1/lemmas/L2_gaussian.md:21-25`; the author's [lecture presentation, slides 20–22](https://www.stat.purdue.edu/~fmliang/STAT598Purdue/partI4.pdf) also states the KL-density and inclusion distinction. The journal page could not be fetched, so this review does not claim a fresh independent audit of the journal proof. No mathematical result here relies on that literature comparison.

The non-claims are honest. In particular PR extends only the model-space results, and H keeps GR^c. The energy obstruction can also be checked without treating N5 as proof: with theta_1=n on an orthogonal design, s_y^2/n^2 tends to one, Q_{12} tends to one, and Q_1-Q_{12}=O_P(log n/n^2). Consequently the likelihood ratio for adding variable 2 tends to one while its determinant penalty is asymptotic to n^-1/2; hence pi({1,2})/pi({1}) tends to zero. This supports the stated failure when energy is simply deleted (`MISR/STATEMENT.md:238-243`). Growing support, unrestricted p, sampler delivery, and integrated prediction are not asserted.

**Final finding counts:** FATAL 0; MAJOR 0; MINOR 0; NIT 1. **Overall score: 9.3/10.0.**

COUNCIL-VERDICT round=R1 manifest=d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d seat=sol score=9.3 gates=PASS
