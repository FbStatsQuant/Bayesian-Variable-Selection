# A-REV6 — independent re-review of later repairs

Felipe's SMC-BVS theory campaign; primary referee GPT-6 Astra, 2026-11-02. Scoped Sol helpers inspected disjoint proof families; Astra integrated their findings and reviewed the replacement proofs. **Overall verdict: GAP, with the original ERROR findings preserved and additional ERROR findings in replacement text.** No source status is upgraded and nothing is adopted. VERIFIED below means the specified mathematical implication checks under its stated assumptions, not that a sketch, conjecture or campaign candidate becomes locked.

The source of record is the fetched origin branch at the immutable head in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). Raw source snapshots and SHA-256 hashes are included under `sources/`. We began with W8-SYNTH §4 and S-REGISTRY; both are maps to claims, not authorities resolving disputes. The review then inspected the original A-REV3/A-REV4 findings and the actual repairs. All writes are confined to this directory. This is a proof/static-source review: **no new simulations, benchmarks or numerical validation were executed**, on the laptop or Owls. Historical saved numerical results are not described as independent reproductions.

Detailed proofs, counterexamples and downstream qualifications are part of this review by reference: [PARTITION.md](PARTITION.md), [SHARE.md](SHARE.md), [BOOK.md](BOOK.md), [WEIGHTS.md](WEIGHTS.md). Every newly supplied repair is explicitly **Astra-authored and pending independent Claude verification**; its original result retains its historical status. Internal checks are not the requested cross-family verification.

## Finding-by-finding table

Branches in this table are `theory/<ID>`; exact heads are in the manifest. “GAP pending Claude” distinguishes a supplied candidate proof from a completed cross-family repair. Rows marked new were absent from the original referee report.

| Finding | Original verdict | Repair (branch + label) | Re-review verdict | Notes |
|---|---|---|---|---|
| W3-PXN P1, actual random blocks | VERIFIED on restricted family | W7-PART Theorem B | VERIFIED on SIZE and fixed correlation separation | Polynomial p, including p≫n; no need to condition Beta laws on recovery. |
| W3-PXN P2, B, Tr, P3–P5, P8 | VERIFIED in their original scopes | No replacement needed | VERIFIED in those scopes | Tr is not thereby extended to arbitrary fixed dimensions; P8 retains T03. |
| W3-PXN P6/Lambda dimension and family count | GAP | W5-VMASK R2; A-REV6 generalised tail argument in PARTITION | GAP | R2 fixes U1, not Lambda's Tr(c) range. |
| W3-PXN P6 U1 arithmetic | GAP result; false intermediate inequality | W5-VMASK R2 | VERIFIED replacement constant | Use a fixed O(1) constant, not the displayed ≤1. |
| W3-PXN P7 no-tweak pilot route | GAP | W5-VMASK R1/R3/R6 | GAP | Cap injection, summed tail and Beta shape repaired; Tr dimension still must be generalized. c=1 restriction remains. |
| W3 joint T38(b), LS0 route | GAP | W5-VMASK R1–R7 and W7-PART B | GAP | Partition recovery does not close lattice proof bookkeeping or operational assumptions. |
| W4-SHARE D4 | VERIFIED | Original conditional theorem | VERIFIED | Predictable killed Laplace process; fresh independent particle-round randomness. |
| W4-SHARE D5 | VERIFIED | Original exact retention product | VERIFIED | Confinement and TRACK remain inputs. |
| W4 SH(i),(ii), exact (iii) formula | VERIFIED | Original binomial mixture | VERIFIED | Converse needs vanishing no-outsider probability. |
| W4 SH universal transition wording | GAP | A-REV6 candidate SH-star | GAP pending Claude | Needs Na,Nb→∞; rare-outsider counterexample remains. |
| W4 G oscillation identity / ESS-only obstruction | VERIFIED | Original algebra | VERIFIED | Abstract identity and obstruction only. |
| W4 G universal BVS/grid extrapolation | GAP | F-SHARE F1; O-BGIBBS BG3 provide different conditional routes | GAP | Neither proves impossibility for every grid condition on production BVS. |
| W4 M(a) | VERIFIED | Original Schur/Cauchy bound | VERIFIED | Normalized Gram eigenvalue bound. |
| W4 M(b) quadratic expansion | ERROR | A-REV6 candidate M-star | GAP pending Claude; original ERROR retained | Exact log-RSS bound; orthogonal theta=1 counterexample still defeats original equality. |
| W4 M(b) BM-C vanishing crossing | ERROR | W5-B2ENV M-LH; A-REV6 M-star | VERIFIED for fixed-coefficient M-LH; GAP pending Claude for M-star | BM-infinity restriction is essential; theta²=C log n/n gives crossing→3/C. |
| W4 M(b) path reaches S0 / automatic repair | GAP | M-LH, F-SHARE F2, O-BGIBBS LH-lock | GAP | Addition path ends at S0 plus extras; closure, deletion and traversal are separate. |
| W4 §7 conditional B2-W4 | VERIFIED | Original product-form inequality | VERIFIED | Uniform REPAIR on the same region and conditional island independence. |
| W4 §7 coefficient-one exit-loss simplification | ERROR | A-REV6 candidate EXIT-star | GAP pending Claude; original ERROR retained | Keep −sum log(1−eta); 2 sum eta suffices for eta≤1/2. |
| W2-T26 Lemma 1 | VERIFIED | W5-LOCKBOOK retained endpoint identity | VERIFIED | Finite positive bridge and truth feasibility. |
| W2-T26 Lemmas 2–3 | VERIFIED | W5-LOCKBOOK terminal-prefix audit | VERIFIED | Refreshed occupancy avoids an accumulated L factor. |
| W2-T26 actual Theorem A | VERIFIED | W5-LOCKBOOK Thm 6 | VERIFIED | Keep P1-ex, EX-A/EX-S and output intersection. |
| W2-T26 single-premise shorthand | GAP | W5-LOCKBOOK retains P1-ex | VERIFIED replacement; original GAP | The written statement, not the shorthand, is the usable one. |
| W2-T26 Theorem B | VERIFIED | W5-LOCKBOOK composition | VERIFIED | EXP′/VIS/NL and posterior hypotheses retained. |
| W2-T26 Prop C | GAP | A-REV4 proposed ORTH concentration repair; no completed Claude replacement | GAP | Source remains sketch; ORTH cannot cover p>n−1. |
| W2-T26 exact-branch parenthesis | ERROR | A-REV6 BOOK R2 | GAP pending Claude | p=18,n=2^18 selects exact enumeration under actual criterion. |
| W2-BOOK Lemma RO | VERIFIED with qualifications | W5-LOCKBOOK; A-REV6 BOOK R1 | VERIFIED conditional implication; R1 pending Claude | Nonnegative potential values, chosen output projection. |
| W2-BOOK literal GUARD | ERROR | W5-LOCKBOOK audit; A-REV6 BOOK R1 | GAP for operational validation; original ERROR | Statistical stop-only coupling supported; metadata/allocation excluded. |
| W2-BOOK Prop 2 island formula | VERIFIED | W5-LOCKBOOK; A-REV6 BOOK R2 | VERIFIED fixed-data identity | E[Zbar Pbar]=Zp/4+3Z E[P1]/4; island products, not product of means. |
| W2-BOOK Prop 2 probability convention/exact extension | GAP | W5-LOCKBOOK STATEMENTS; A-REV6 BOOK R2 | ERROR in W5 full-output expectation | Exact evidence contributes Z, even though exact branch contributes zero to the error event. |
| BOOK completed wrong HPM means posterior miss | ERROR | W5 strict scored competitor certificate; BOOK R3 | VERIFIED restricted certificate | Completion alone never proves discovery. |
| BOOK size-prior ceiling | VERIFIED tie-aware criterion | W5 Prop 1(iii) paraphrase; BOOK R3 | ERROR in paraphrase | Equal-likelihood competitor may lose tie order to S0. |
| BOOK VAL-FP | GAP operationally; implication VERIFIED | W7-SEC T33-Z/H; BOOK R4 | GAP operationally | Auxiliary frozen fp calibration is useful; exact comparator, rounding and useful epsilon still required. |
| BOOK numerical/provenance qualifications | GAP | Historical A-REV4/W5 results | GAP for interval-certified deployment | No new replay or numerical certification here. |
| F-DRAFT Prop NM | ERROR | A-REV6 candidate NM-R | GAP pending Claude | Four-state normalizer solved; O_P(sqrt n) fluctuation retained; not production SMC at p=2. |
| F-DRAFT Lemma W1 | VERIFIED | O-WSTAB WS3; O-DILUTE L clarification | VERIFIED exact sample-BO identity | Population orthogonality is insufficient. |
| F-DRAFT Lemma W2 | ERROR plus uniformity GAP | A-REV6 candidate W2-R(a),(b) | GAP pending Claude | Exact regularized fraction; narrower ORTH additive uniform expansion. |
| F-DRAFT Prop W4 | GAP; TV implication VERIFIED | O-WSTAB tilted-law identities; A-REV6 complete-state bound | GAP for advertised sharp rates | Multi-extra layers and tilted normalizer cannot be omitted. |
| A-DRAFT §2 A/A1 | VERIFIED | W5 stream audit; BOOK boundary check | VERIFIED | Fixed-data LLN/MSE and numerator identities, not CLT. |
| A-DRAFT §2 D/D1 | VERIFIED | W5/W7 bookkeeping; BOOK boundary check | VERIFIED conditionally | Explicit favorable premise, contraction/continuity, exact branch and output scope. |

## New problems in repair branches

These are restricted findings, not blanket rejection of those branches.

| Repair result | Re-review verdict | Counterexample or missing step |
|---|---|---|
| W7-PART Lemma 3 literal full-vector conditioning | ERROR | Conditioning on both normalized vector collections fixes their cross inner products; a nondegenerate Haar law cannot remain. Condition on within-group Gram matrices instead. |
| W7-PART Theorem C | GAP | Needs the corrected conditioning lemma; B does not use it and survives. |
| W7-PART unequal-size CE2 header | ERROR | Groups of sizes 2 and 5, B=5: 2g_min≤B but next-fit cannot merge the groups. Equal-size study example survives. |
| W7-PART A0(c) | GAP | Completed roots already absorbed into full unions are not current clusters; restrict its quantifier. |
| W5-LOCKBOOK full-output E[1_O Zhat]≤Z P(A) | ERROR | Completed exact branch with A defined SMC-only: Z>0 on left, zero right. |
| W5-LOCKBOOK “same-size m≥m0” certificate | ERROR | Tie with S0 first in prescribed order. |
| W5-LOCKBOOK T32(c), W7 confirmation | GAP | Deterministic count contains (1+4ell); its direct bound is O(max(n,p)p log³(n+p)+p²log²(n+p)). Polynomiality survives. |
| F-SHARE Lemma 1.2 pointwise display | GAP | Intermediate-state suprema and neighbor-swap factor used in proof are absent from display; subsequent (1.1) supplies them. |
| F-SHARE §2 rare-outsider “sharpness” | ERROR | pi0(o)=1/N leaves probability tending to exp(−1) of no outsider at all. |
| F-SHARE §5.2 retention inequality | ERROR | At T=1,eta=1/2, 1−eta<exp(−eta), opposite to printed lower bound. |
| F-SHARE F2/§4 and O-BGIBBS LH-lock | GAP | Explicit population and/or Gaussian/extra-count hypotheses are not discharged by M(b). |

## Does W7-PART close the p ≫ n random-partition GAP?

**Only the restricted recovery premise; not the full result.** For LH-iid with fixed population correlation gap and `g≤B<2g`, Theorem B's margin bound is exponentially small in n times a polynomial in p. Complete linkage finishes each group before cross merges, the capacity cut retains the groups, and packing cannot combine them. This is a valid route even for polynomial p≫n and bypasses W7 Lemma 3. A-REV3 had already VERIFIED P1 in precisely this restricted family; its overall GAP must not be reinterpreted as a rejection of P1.

What remains is distinct: P6/P7 use a projection-tail lemma outside its stated dimension/family range; the LS0 route has its method-change/ledger assumptions; and study groups of five can be packed together. W7's statement that the partition depends only on X does not make its selected blocks independent of X or of y=X theta+epsilon. Establish fixed-group statistics unconditionally, then intersect with recovery. Do not reuse their Beta law after conditioning on successful recovery. No repair here gives a statistical law for arbitrary adaptively packed study blocks.

## Overall verdict per result/package

- **W3-PXN: GAP.** P1–P5 and P8 survive in scope; P6/P7 and joint route retain the documented gaps.
- **W4-SHARE: GAP with ERROR subclaims.** D4/D5, conditional assembly and M(a) survive; original M(b) and coefficient-one exit simplification do not.
- **W5-B2ENV M-LH: VERIFIED restricted replacement.** Fixed exact-Gram lattice and nonzero fixed coefficients; no general BM-C or extras repair conclusion.
- **W2-T26: VERIFIED conditional A/B and Lemmas 1–3; GAP package.** Prop C is still a sketch and the exact-branch parenthesis remains ERROR.
- **W2-BOOK/W5-LOCKBOOK: GAP with ERROR replacement sentences.** Core conditional identities survive; operational/fp claims and exact-output/tie wording require the specified repairs.
- **W7-SEC as a deployed VAL-FP repair: GAP.** Conditional comparator/margin ideas survive; useful production parameters are not certified.
- **F-DRAFT: ERROR in NM/W2; GAP in W4; VERIFIED W1.** Narrow new replacements await Claude; general claims remain unresolved.
- **A-DRAFT §2: VERIFIED conditional mathematics.** No completion, CLT or arbitrary bounded-measurable generating-value upgrade.
- **W7-PART: VERIFIED B in restricted scope; GAP package with ERROR Lemma 3/CE2 wording.** C needs an explicit repaired lemma.
- **F-SHARE/O-BGIBBS as unconditional downstream closure: GAP.** Conditional first-exit/hazard templates are usable; applications retain premises.
- **O-WSTAB/O-DILUTE as repairs of F-DRAFT: VERIFIED cited exact identities only; GAP for the requested general sharp-rate claims.** This is not a review of every theorem on those branches.

## LOCKABLE list

“LOCKABLE” is a recommendation for the exact qualified statement, never an edit to the register. Existing author candidate/sketch/conjecture labels are preserved. The list excludes every Astra-authored candidate until Claude independently verifies it, and excludes every scope expansion.

1. W4-SHARE D4/D5, SH(i)/(ii)/exact binomial formula, G convex-combination identity, M(a), and product-form conditional B2-W4; attach all frozen-data, confinement, TRACK, REPAIR and island assumptions.
2. Previously VERIFIED W3-PXN P1–P5 and P8 in their original restricted family and lemma ranges; no P6/P7/joint-route lock.
3. W2-T26 written Theorem A, conditional B and Lemmas 1–3, retaining P1-ex and output intersection; omit erroneous exact-branch prose.
4. W2-BOOK fixed-data island-product/covariance identity and qualified output Markov implication; not its full-output expectation with SMC-only A, literal GUARD, or production VAL-FP.
5. F-DRAFT W1 under exact sample BO and the original qualified TV implication; not W2/W4 sharp rates.
6. A-DRAFT §2 A/A1/D/D1 in their explicit fixed-data/asymptotic and boundedness/continuity scopes.
7. W5-B2ENV M-LH's restricted fixed-coefficient lattice implication; explicitly separate it from M(b)'s original false scope.
8. W7-PART Theorem B's strict-margin recovery implication on SIZE, with its stated Gaussian correlation-law input; no C, unequal-size CE2 or arbitrary study-packing transfer.
9. F-SHARE F1 and O-BGIBBS BG3 as conditional first-exit/terminal-hazard templates only; their application sketches are not included.
10. O-WSTAB exact tilted-normalizer identities and O-DILUTE exact size-correction/ranking identities as used in WEIGHTS; no all-layer threshold claim.

## Candidate handoff and audit

Claude must verify: SHARE M-star, EXIT-star, SH-star; WEIGHTS NM-R and W2-R; BOOK R1–R5. PARTITION specifies the generalized-tail and corrected-Gram-conditioning repairs still needing an explicit source-of-record amendment. M-star uses **normalized** Gram eigenvalues, fixed extras d, feasible additions and BM-infinity. NM-R is intentionally a four-state abstract example on a production exact-enumeration size, not a claim of an actual SMC failure. W2-R(b) is ORTH, not general random-design BO. These limitations are part of their statements.

Astra's integration check examined the candidate formulas, supplied the M-star/exit/transition proofs, and reviewed Sol's counterexamples and source readings. Additional internal checks caught and corrected M-star's Gram-normalization wording and added NM-R's production-exact-branch caveat. Historical branches and registry files were not edited. Source hashes identify bytes, not mathematical validation. The final response supplies the pushed A-REV6 head SHA; a self-referential commit hash is not embedded in its own content.

## Eight-line summary

1. Overall GAP; original ERROR/GAP verdicts remain unchanged.
2. D4/D5, conditional T26 and A-DRAFT §2 implications survive.
3. W7-PART B settles restricted recovery, not the full p≫n route.
4. M-star and EXIT-star repair only stated gain/product obligations.
5. NM-R/W2-R and bookkeeping R1–R5 await Claude verification.
6. New exact-branch, tie, conditional-law and retention errors are documented.
7. No new numerical workloads or locked-register changes were made.
8. Reviewed W7-PART head SHA: b2aa940b6d1212c01448fcc4ff1c8851d2bce74b; pushed A-REV6 head is reported with delivery.
