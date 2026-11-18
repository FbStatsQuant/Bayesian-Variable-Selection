| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

Review file: [R1_council_sol.md](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/reviews/R1_council_sol.md).

These decisions concern the formal claims with their stated conditional inputs. They do not approve the reader draft or promote any unchecked input. I found no blocking defect in the four formal proofs. Three faithfulness findings in READER_DELTA prevent acceptance of this manifest.

Findings

1. **F — The reader asserts necessity of a stronger, full-response condition.** [READER_DELTA.md:57-59](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:57) calls the response condition in (A0) necessary and sufficient for the exact reduction when the noise is Gaussian. But (A0), at `:25-27`, specifies the entire conditional response vector as independent normal observations. [STATEMENT.md:71-74](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:71) proves necessity only of the Gaussian **contrast** condition (OV^c), under (N); the full-vector form is sufficient ([STATEMENT.md:67-70](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:67)). These are different conditions. For example, take iid Gaussian candidate rows, independent Gaussian noise epsilon, deterministic intercept zero, and an omitted contribution H*1 with H an independent Rademacher variable. Then U^T(H*1) = 0, so (OV^c), the exact contrast reduction, and the posterior reduction hold. Nevertheless, the response conditional on the candidates is a two-component Gaussian mixture with a shared random shift, and fails (A0). This also works with a fixed sparse nonzero candidate coefficient satisfying the population floor and signal conditions. **Fix:** describe (A0) as a sufficient full-response condition. If necessity is discussed, state it for the conditional contrast law under (N), as in CorG-min(c), and distinguish exact contrast-law reduction from full-response Gaussianity.

2. **F — The Gaussian omitted-predictor example uses an inverse that need not exist.** [READER_DELTA.md:41-45](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:41) asserts the example and displays Sigma_CC^{-1} without assuming Sigma_CC positive definite. The reader's restricted correlation floor at `:30-31` does not imply global invertibility; the master explicitly permits singular candidate covariance (`STATEMENT.md:81-83,96-102`). This can occur even under the reader's other hypotheses: take p = n, A = s = 1, Sigma = R with diagonal 1 and off-diagonal -1/(p-1), beta^C = e_1 and residual variance 1. Every principal submatrix of size k has minimum eigenvalue (p-k)/(p-1), so the reader's O(log n) floor holds eventually with c = 1/2. Energy and diverging beta-min hold, but Sigma is singular. Append an independent Gaussian omitted predictor with nonzero coefficient and split the residual variance between it and independent Gaussian noise to obtain the stated omitted-predictor setting. The displayed inverses remain undefined. **Fix:** use the Moore-Penrose formulas from CorG-min(E1), or explicitly restrict this example to Sigma_CC positive definite. Keep the singular case available in the theorem.

3. **F — The fixed-design uniform contraction sentence drops the uniform selection premise.** [READER_DELTA.md:51-53](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:51) gives selection tending to one in probability, an energy bound and a target floor, then says contraction holds uniformly over such configurations. CorH-plus(a') supplies the individual-array conclusion. CorH-U(U-a) supplies uniformity only for classes satisfying **uniform** selection consistency (UP), [STATEMENT.md:139-142](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:139), with common class constants and bounded support size. Pointwise selection consistency across a collection of arrays does not imply (UP): arrays can have arbitrarily delayed selection onsets, and taking a supremum can select a different delayed array at each n. Bridge B4.4 ([READER_DELTA.md:76](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:76)) cites U-a but supplies no (UP) premise for this fixed-design sentence. The ticket itself correctly distinguishes the two in [TARGET.md:17](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/TARGET.md:17). **Fix:** say that the fixed-design result holds for each such array, and holds uniformly over classes with common energy/floor/dimension constants, bounded support size, and uniform selection consistency. In plain language, the probability that posterior mass on the target is below 1-epsilon must tend to zero uniformly over the class, for every epsilon > 0.

4. **E — Existing raw-design notation slip.** [lemmas/G2_corr.md:18](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/lemmas/G2_corr.md:18) writes the original configuration as (X, beta^C, sigma_C^2) although X denotes the standardised design elsewhere. The proof uses the raw design throughout its reduction. This is already recorded as E1 in [ERRATA.md:5](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/ERRATA.md:5). **Fix:** replace X in that configuration by X^r_C. This item does not block and does not affect the score.

Sweep duty 1 — Statement copies and proof coverage

Checked every clause of STATEMENT sections 2-5 against G1-G2-H1-H2. G1 proves sufficiency, the full-vector sufficient form, necessity, the Cramer partial converse, all three examples and the conditional-mean interpretation. G2 proves the two explicit finite-n inequalities for all n beyond its sequence-dependent threshold, their O(r_n) consequences, and the parent implication. H1 covers all three bad-set families in both branches, the deterministic KL identity/bound and the readings. H2 covers U-b, U-a, RD, the eta-family and (G). The lemmas incorporate their statements by section reference; I found no omitted formal clause.

Sweep duty 2 — Quantifiers, constants, measurability and null events

The formal claims preserve the required order of quantifiers. In G2 the fixed beta-min constant c is chosen below c_R*liminf(rho)/16, and n_BM, hence n*, may depend on the array; the finite-n claim does not promise a uniform onset over all beta-min sequences. Column scaling removes any need for a global variance bound. H1's smaller divergent sequences justify the KL inclusions for every prescribed M_n. H2's fillers have common enlarged constants; the b-type threshold C_H depends only on (s,A), so enlargement does not change the needed threshold. The support subsequence and bounded-size union arguments are valid. H2.0 gives jointly Borel posterior masses on support strata, with zero contrasts a Gaussian-null event at each configuration; conditioning makes the random-configuration zero event null as well. Arbitrary classes in U-a cause no additional measurability requirement on a supremum of numerical probabilities. The reader's lost (UP) quantifier is finding 3.

Sweep duty 3 — Lemma scope at downstream uses

G1(a) is sufficient for G2 and H2; G1(b), including its intercept-measurability qualification, is the form used by H1's full-response KL reading. G2's sparse floor suffices for each Gaussian submatrix estimate even when the full covariance is singular. Its measurable design events put the original configuration into the fixed class used by H2(G), and their failure probability tends to zero. H1 is used with legitimate fixed constants in the filler arguments. H2(G) obtains (UP) from the uniform MIS-R(i) expectation bound and Markov, then applies RD; it does not infer conditional contraction from an unconditional selection estimate alone. No downstream use of the four formal lemmas exceeds their scope.

Sweep duty 4 — REPORT, registry blocks and conditionality

The four REPORT statement ranges and premise pointers agree with STATEMENT. Each new registry status matches its lemma's status verbatim, including the additional conditions for CorH-U(G). G2 retains the conditions inherited through MIS(ii), A0 and the cited GD(b) proof; H1 carries D; H2 carries D, C and A0 plus the stated (G) conditions. The parent implications follow by the displayed Gaussian specialisation, covariance-to-correlation inequality, selection premise and singleton classes. C_H can be taken as the explicit increasing function of s supplied by D_hellinger, as used in the singleton b-branch. The W3-DIST paragraph is explicitly HEURISTIC/OPEN, makes its proposed application conditional on an unchecked premise match, and does not assert an additional theorem. I checked the pinned preprocessing/scoring formulas at commit 16a7f85: positive column rescaling preserves the real-arithmetic standardised design and coded target. No blocking REPORT/registry defect found.

Sweep duty 5 — Frozen hashes, DEPS, citations and numerics

All 28 file hashes in MANIFEST_R1 match the files reviewed. I recomputed all ten DEPS rows without invoking the writing main function of deps_hand.py: every sha equals checked_sha. In particular S:CorG-min = 97b1ed2602f41b3b, S:CorH-U = 533cc312b9632e27 and L:H2_uniform = 7757a8986d5306c9. The uses edges correctly track G1 -> G2/H1 and H1/G2 -> H2; external inputs are separately documented. I did not inspect the withheld checked_by files. I inspected citecheck.py and reproduced 151 checks with zero failures by executing an in-memory copy with its output-file write disabled; CITECHECK.txt agrees. This selected citation checker does not validate mathematical entailment and therefore does not resolve findings 1-3. N1's enumerator implements the stated real-arithmetic score and prior, and TARGET's numbers match its saved output. Its boundary observations remain finite-n evidence; no asymptotic robustness claim is inferred. I did not rerun the Monte Carlo experiment. The binary-design rejection of constant-column samples and thresholded empirical BLP support are numerical presentation details, not proofs of theorem hypotheses or exact population support.

Sweep duty 6 — Reader statement and bridges

The headline expectation and HPM rate displays follow from CorGb-plus using B4.0's q=0 construction: a constant conditional Gaussian residual law gives independence from the candidates. B4.1's logarithmic floor size eventually dominates s + max(j0,m#_n), using the cutoff bound in W3-POST STATEMENT lines 37-39 and p <= n^A. B4.2 is the diverging beta-min branch. B4.4 correctly yields the Gaussian-design Hellinger/KL rates through CorH-U(G), with the fixed high-probability design events and uniform MIS(i) bound. However, the accompanying necessity explanation, singular-covariance example formulas, and fixed-design uniformity sentence are not faithful to the masters, for findings 1-3. Thus this duty is completed with blocking findings.

Better-theorem proposals

None required for this review. The listed expectation-contraction and non-Gaussian-candidate extensions remain open and are not findings.

Gates

- correct: PASS — the four formal claims have correct proofs under their declared conditional inputs.
- strength: FAIL — the reader's necessity and uniformity assertions exceed the master conclusions as explained in findings 1 and 3.
- faithful: FAIL — READER_DELTA has the three identified departures from the masters.
- statuses: PASS — new status strings are verbatim and their conditional-on lists are complete.
- sweep: FAIL — all six duties completed; findings 1-3 remain blocking.
- reader: FAIL — the proposed reader text is not yet masters plus correct bridges.

Score: 7.8/10.0. The formal mathematical results are acceptable; the score reduction concerns the three substantive faithfulness defects in the reader proposal. Editorial finding 4 does not lower the score.

COUNCIL-VERDICT round=R1 manifest=fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994 seat=sol score=7.8 gates=FAIL
