# Council R2 ? sol ? blind first read

Verdict summary: Accept as checked mathematics on MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885. I independently read the frozen statement, report, assumption map and all eleven proof files, and re-derived the proof chains rather than relying on numerical agreement or another ticket's assurance. I found no blocking mathematical, hypothesis, uniformity, import or code-fidelity defect. The package proves statements about the exact mathematical start distribution, under the stated asymptotic convention and fixed support size. The distinction between a lattice bound and concentration at the truth, and between tightness and a fixed-constant bound with probability tending to one, is maintained. No correction is required before acceptance.

## Gate table

| Gate | Result | Re-derivation and justification |
|---|---|---|
| G1 ? correctness | PASS | Re-derived L1's prior path bound, fibre counting, both odds bounds, AGG-c/d and ridge/Schur-complement floor; L2's Gaussian events, residual identities and score remainder; L3's integrals, linearisation and unconditional truncated-expectation Markov bound; L4.1 Steps 1?7 and L4.2's truth-addition chain; L5's assembly and probability accounting; L6?L8's corollaries, diagnostics and conditional transfer; L9's perturbation/localisation bounds, conditional regression, Gaussian integral and assembly; L10's overlap/reduction arguments; all five L11 examples. No invalid step found. |
| G2 ? stated hypotheses | PASS | Compared each REPORT ?3 claim with STATEMENT ?5 and its proof. In particular, the quantitative TK convention in STATEMENT ?4 supplies the rate used by NEC-b and the bridges; OVL states its bounded number of leaking columns and uniformly bounded levels; transfer states admissible design sets and fixed constants; the Gaussian bridge explicitly assumes p > s?. |
| G3 ? hidden assumptions | PASS | No independence across null columns or across the block Gaussian directions is used. The only independence used in L9.5 is the justified conditional orthogonal Gaussian decomposition after conditioning on W_D. The unnormalised floor suffices for L2. Empty truth support is separately handled in L3?L5; no A ? 1 restriction appears in the fixed-design argument. The partition, targets and levels are fixed given the design; no conditioning on E_cov is substituted for conditioning on W_D. |
| G4 ? imports and interfaces | PASS | The proofs close locally: toolkit, Gaussian-row bridge and misspecified reduction are re-proved. Checked the quoted versions/statuses against the permitted registry and checked SAMP's actual P-START, P-OVL, D-iv and C-v wording. IF-START supplies only the start half of C-v, and OVL supplies the production sufficient form of P-OVL, without asserting posterior concentration, calibration success or general global overlap. |
| G5 ? constants and rates | PASS | Checked ?_E, the O(n^(?1/3)) toolkit envelope, the O(log n) small-gain envelope, truncation budget, visibility slack and all assembly constants. L5.2 has design-independent thresholds and constants; its event failures sum to ? + b_n(h). L6.0 justifies using ?_n = 4/log n. L9's reference count is polylogarithmic; Markov yields tightness when C_L = 0 and the stated exponential-square-root-log envelope otherwise. These suffice for L9.7's high-probability conclusion. |
| G6 ? coded start | PASS | Checked the permitted pinned C++ score/prior/cap, block construction, full-response tables, start weight and truncated convolution against STATEMENT ?1, together with R preprocessing/setup. The factor W_K cancels exactly. The score uses n/2 + 0.01 and the scored response with squared norm n ? 1. Production B ? K for n ? 4, and the partition depends only on X. The theorem's EX-A qualification is explicit. |

## Per-claim table

Every id below is the id in REPORT ?3.

| Id | Disposition | Basis |
|---|---|---|
| AGG | accepted | L1.1?L1.5: exact prior ratios, injective fibre map, positive-table bounds and scorer floor. |
| FLOOR | accepted | Ridge residual monotonicity and increasing Schur complement give each addition ratio ? (n + 1)^(?1/2); summing feasible additions gives the displayed floor. |
| TK | accepted | L2 re-proves tails and score expansion using only the constant unnormalised Gram floor. |
| LEAK | accepted | J0?J3, domination by partition-free functionals, small-gain consequence, truncated sums and Markov bound. |
| VIS-c | accepted | The truth-block event controls only finitely many directions; addition chain bounds e_n and AGG-d bounds ? once c_QU_Q ? 1. |
| VIS-m | accepted | Two nested residual comparisons through W, with the different ? denominators exactly as stated, absorb substituting-null gain and leave the claimed margin. |
| ASM | accepted | Binomial-series aggregation, quadratic remainder and the deterministic lower bound for T?. |
| START-F | accepted | L5.2 supplies the explicit uniform statement; L5.3 obtains the little-o remainder by using an intermediate exponent. |
| F1 | accepted | J2 gives ?/2 + ?(2A?), and the strict exponent slack absorbs logarithmic constants. |
| F2 | accepted | Truth-Gram Schur complement gives ?_U bounded below; J1 controls the leading functional; the remaining quadratic term is o(n^(?1/2)). |
| F3 | accepted | J2 gives exp(C?log n); the hypothesis for every fixed C? supplies the slack needed by the high-probability form. |
| F4 | accepted | Column-specific ?(4 log log n) truncation has vanishing tail budget for a bounded set; its charge has exponent ?(1 + 2A? ? c)/2 + o(1). |
| NEC-b | accepted | Deterministic witnesses need only one Gaussian tail each. The strong-null lower and weak-truth upper likelihood comparisons have the stated prior price. |
| NEC | accepted | Component diagnostics imply N2/N3 at the block truth subsets; N2's empty premise for s? ? 15 is explicitly retained. N4 is a scope statement. |
| TRANSFER | accepted | Conditional Setting F plus uniform constants, integrated over measurable admissible design sets. The off-domain convention makes the joint statements well-defined. |
| BR | accepted | Covariance event, small-set floors, visibility, localisation, conditional Gaussian regression and integral establish the stated bridge without importing RM's claims. |
| START-R | accepted | L9.7 applies the uniform transfer with ? = 1, ?_V = 3/2 and slowly decreasing ?; logarithmic losses fit in exp(C_R?log n). |
| IF-START | accepted | Start odds have the displayed deterministic rate; localisation by an arbitrary event preserves it. SAMP's additional premises remain explicit. |
| OVL | accepted | AGG-c, finitely many low-tail Gaussian bounds and bounded levels give ??(S?) ? n^(?E_n??) with probability tending to one; the budget comparison is correct. |
| MIS | accepted | Independent Gaussian-sum reduction, followed by the original claims only with all their hypotheses substituted; conditional version uses TRANSFER. |
| EX | accepted | F-1, F-2, F-3, G-1 and G-2 verify the partition-free conditions. UNI-0 and AR(1) are explicitly outside the verified list. |

## Detailed checks on the principal risk points

**Aggregation and toolkit.** In the fibre argument, D ? s? ? |T| makes the deletion path valid, while E ? 15s? bounds the rising factorial by c_Q. Summing the injective image over a larger Cartesian product is legitimate because all weights are positive. Keeping the good-block one-addition term exact produces T?; only the terms of order at least two are replaced by the binomial remainder. The lower bound by c_s? uses feasible single-block replacements, not an inverse of the upper bound. In L2, diagonalisation gives the determinant correction in [?16 log(1 + 1/g_*), 0] and the ridge discrepancy at most 1 + 1/g_*. The energy assumption supplies a scored residual of order n, so the remainder stays bounded even when normalised eigenvalues are of order 1/n.

**Leakage and visibility.** The maximum of the truncated factors is bounded by a sum over at most 2^15 conditioning sets per column. Expectations are taken under the unconditioned Gaussian law; the toolkit and truncation event are used only for pointwise domination. Thus there is no unjustified conditional Gaussian assertion. L4.1's margin has the needed ?_W denominator for the upper comparison. Its ?? choice leaves a nonnegative coefficient on L? after the toolkit errors, and a log n margin strictly larger than ? after paying the dimension/prior price. The O(log log n) truth-block noise bound is essential and is supplied. L5.2 counts the shared events once and the two Markov failures separately. Its c? ensures (c_Q + 1)U_Q ? 1/4 uniformly, including growing Q.

**Gaussian bridge and transfer.** The localisation error is ?N times a quadratic covariance error, not a linear error. The assumption r_n(n log n)^(1/4) ? 0 therefore yields the exact o(1/?log n) control needed when comparing F. Conditioning on W_D fixes the truth-column standardisations and ?. The innovation remains isotropic Gaussian, with independent parallel and perpendicular parts, yielding (9.1). On the residual-norm event, monotonicity of F permits replacement by ?_n(? + d?). Integrating ? first gives the denominator 1 ? s??; the residual coefficient on Z? is ?_n(1 ? a)/(a ? ?_n). The displayed ?_n bounds this integral uniformly. The moment bound is integrated without conditioning on E_cov. The union bound and reference count then justify L9.6. The transfer requires no union over random supports because they are fixed under the design conditional law.

**OVL and F-2.** Bounded ? and a bounded number of columns make the noise cross terms o(log n) uniformly in OVL, so summing positive exponent parts produces exactly E_n. For F-2 I re-derived q_k = 0.6/(1 + 0.4(k ? 1)), q_15 = 1/11, and max_k(q_k ? q_(k+1)) = 0.4. With c = 2(1 + 2A), the margin c/12 is smaller than c/11 and the leak level 0.4c is below 1 + 2A. The default-integral lower exponent is ?0.1 ? 0.2A + ?(1.6A + 3.2A?), positive throughout A ? [0.1, 1]. Thus this example actually separates both visibility forms and both truncation choices, as claimed.

## Report, assumption map and scope

The report's claim rows match the statement and the named proofs. Its assumption identifiers and implication relations do not silently consume an unchecked ticket. The necessity statements are appropriately qualified: ? ? 0 needs the feasibility condition; the functional AL itself is not claimed necessary; the polynomial VIS interface is not inferred merely from ? ? 0. The exclusions of growing s?, non-Gaussian noise, response-selected targets, binary64 guarantees and unverified example families are adequate. The numerical file's older N2 references are explicitly corrected by its opening note at numerics/RESULTS.md:3?4; I applied that correction, rather than treating those references as a new partition-free necessity claim. The literature/headline gate remains separately open and is not used as a proof premise.

## Issues

None identified: no BLOCKING issue and no NON-BLOCKING correction requested. Acceptance does not require changing the frozen package. The verification limits below are not additional theorem claims or acceptance conditions.

Overall score: **9.2 / 10**.

## Checks performed

- Manifest verification returned OK for the exact R2 digest above, including the pinned external inputs.
- Read and re-derived every proof file L1?L11 and compared all 21 REPORT ?3 ids with STATEMENT ?5; checked REPORT, ASSUMPTION_MAP, PLAN and the ticket brief within the permitted scope.
- Independently ran an inline Python enumeration on 500 random positive-table cases with p ? 9, blocks ? 4 and feasible caps/reference/lattice sets. There were 524 applicable AGG-a/b/c inequality checks and zero violations. This is a supplementary algebra check, not an asymptotic proof.
- Independently audited all 53 line-number citations found in STATEMENT, REPORT and lemmas against the allowlisted files: zero invalid ranges. Checked the principal code and consumer citations semantically, rather than treating range validity as semantic verification.
- Compared the quoted C-GROW, C-MIS, W3-SAMP, W1-PXN(S), W3-RM and SOP:TH116 assurance/version text with the permitted registry; no assurance upgrade found.
- Inspected the numerical results summaries and recorded violation totals: all five lemma output files report zero violations. The raw production CSV has 1018 data rows and the summary has 106 rows. Numerical results were treated only as observations.
- Changed no git state and wrote only this review file. No subagents were started; no prior review, disposition, LOG or checkpoint was read.

## Not checked

I did not rerun the full production R simulation campaign or the author's complete falsification scripts, validate every numerical CSV value, establish a binary64 theorem, or audit the literature novelty comparisons from their original publications. I did not independently establish the correctness of SAMP's sampler theorems: their stated interfaces and quoted assurance were checked, and their conclusions remain subject to their own premises. No finite-n informativeness threshold is scored as a defect. No prohibited source or earlier review was used.

COUNCIL-VERDICT round=R2 manifest=5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885 seat=sol score=9.2 gates=PASS
