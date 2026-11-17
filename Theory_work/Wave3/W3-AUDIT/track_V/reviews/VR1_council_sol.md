# V-R1 blind council review — sol

## Verdict summary

**ACCEPT V1. All six gates PASS.** No C, S, or F finding is held. The lemma supplies a margin uniform in n under its stated joint design/signal hypotheses. In particular, the generic route uses the closure of directions over the whole sequence and a positive distance from its fixed bad set; it does not substitute pointwise noncancellation for a uniform margin.

The prescribed verification returned `verify: OK MANIFEST c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98`. This review concerns that frozen content. I read only the brief and its permitted evidence, changed no git state, and started no subagents.

## Gates

| Gate | Result | Basis |
|---|---|---|
| G1 Correctness of every step | PASS | Schur-complement reduction, signed Stieltjes inverse argument, distance bound, compactness/closedness, and local-pattern closure arguments are valid. |
| G2 Hypotheses used = stated | PASS | Global positive definiteness is required for VIS-a; local floors suffice elsewhere. VIS-d explicitly assumes the larger uniform local floor. Alignment and the uniform separation hypothesis are stated. |
| G3 No hidden assumptions | PASS | The stationary argument uses fixed r with decay to zero; the finite-type argument uses a fixed finite collection. Truth coordinates are identified by rank. Limit local matrices retain the positive floor. |
| G4 Theorem hypotheses and notation | PASS | The permitted origin/main excerpts agree with the population partial covariance, conditioning cardinality, visibility assumptions, and distinction between global positive definiteness in Theorem 6 and local floors in Theorems 5/10. |
| G5 Scope | PASS | The constants are uniform once the stated floors and signal/separation bounds are uniform. The n >= n0 qualification and theorem floor thresholds are explicit. The generic route excludes approach to limit hyperplanes. |
| G6 Design and example fidelity | PASS | IND, signed AR, nonnegative equicorrelation, one-factor and block examples have the stated sign structures and floors. The B8 and track C references preserve the aligned/mixed-sign distinction and the stated population cancellation cases. |

## Claim table

| Claim | Decision |
|---|---|
| V1 | ACCEPT |

## Numbered findings

None. No C, S, F, or E finding; no repair requested.

## Mathematical assessment

1. **VIS-0 and VIS-a.** `V1_VIS/PROOF.md:22-39`: bilinearity gives the stated visibility vector, and the inverse-diagonal formula on U union {j} gives the local variance floor without requiring invertibility of the full covariance. For VIS-a, the signed precision principal submatrix is positive definite with nonpositive off-diagonals, so its inverse is entrywise nonnegative. Different precision components have zero conditional covariance. The alignment hypothesis therefore prevents cancellation and retains the own-truth variance term. Conditioning can split a component without invalidating this sufficient alignment condition.

2. **VIS-b and VIS-c.** `V1_VIS/PROOF.md:42-56`: compactness of the closed direction set makes the union of orthogonal hyperplanes closed, by the stated subsequence argument. Distance to that union equals the attained minimum of the absolute inner products with unit directions. The norm of each visibility vector is at least its own-truth coordinate, hence at least c16. This proves the quantitative bound and its uniform version. When the closed direction set is countable, the union is null; closedness then makes it nowhere dense. Countability of the unclosed set alone is never used as a substitute.

3. **VIS-d.** `V1_VIS/PROOF.md:59-78`: there are finitely many matrix sizes and label patterns. Correlation entries are bounded and the positive floor is closed, so the relevant local closure is compact and normalization remains continuous. Finite block/row types give finitely many local matrices. For stationary designs, a finite tuple of integer gaps compactified by infinity has a countable compact domain; decay of r makes its matrix map continuous. This establishes countability of the closure, including limits with separated clusters. The block-stationary extension only adds finitely many sharing/type labels.

4. **Examples and theorem use.** `V1_VIS/PROOF.md:81-103` and `V1_VIS/STATEMENT.md:53-73`: the AR signing works for either sign of rho, and the spectral bound is uniform in dimension. The equicorrelation inverse and Sherman–Morrison formula give the claimed signs and floors. The alternating two-truth example correctly shows that VIS-a need not satisfy VIS-b's separation premise. The theorem floor transfer is conservative and sufficient. B8 lines 222-228 support the separate s5/fac2 computations; track C's empirical results are not needed to prove the lemma.

## Overall score

**9.5 / 10**, assessed on C/S/F issues only. No blocking issue found.

## Checks performed

- Ran the exact manifest verification command specified by the brief; it passed.
- Read STATEMENT.md, PROOF.md, CITECHECK.txt, and citecheck.py; checked the four cited input ranges against the allowed source text. Did not execute citecheck.py because it rewrites CITECHECK.txt.
- Read B8 lines 209-233 and track C RESULTS.md, and fetched only the permitted theorem/notation excerpts with read-only `git show origin/main:...`.
- Checked all proof steps analytically, including the distinction between countability and countable closure, stationary gap limits, singular global covariances, and uniform-in-n quantifiers.
- Ran in-memory NumPy checks on p=6 matrices, enumerating all 32 conditioning subsets for each of three truths: AR(-0.8), AR(0), AR(0.8), equicorrelation 0.7, and a one-factor model with mixed loading signs including zero. All 480 sign-route inequalities held to floating-point tolerance; the smallest normalized ratio was approximately 1.
- Checked the two-truth equicorrelation-0.5 cancellation example: theta=(1,-2) has distance and minimum visibility zero. For theta=(1,1), distance is 1, minimum visibility is 0.75, and the generic lower bound is 0.5.
- Checked the globally singular 17-dimensional correlation matrix (17/16)I-(1/16)J: the size-16 floor is 1/16, and conditioning a truth on the other 15 null columns gives visibility vector (0.53125,-0.53125), consistent with VIS-0. These numerical checks supplement the proof, rather than certify its universal claims.

## Not checked

No Lean formalization, external references, forbidden audit/review files, or design definitions outside the permitted evidence were inspected. I did not reproduce track C simulations, certify their reported numerical minima, or audit the other hypotheses/conclusions of Theorems 5, 6, and 10. No claim of sample-level visibility was assessed.

COUNCIL-VERDICT round=R1 manifest=c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98 seat=sol score=9.5 gates=PASS
