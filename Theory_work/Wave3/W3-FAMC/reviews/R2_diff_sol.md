model: gpt-6.2-sol (provider codex, reasoningEffort high); round=R2; seat=Sol diff round; commit=82fb5122; base=4bb2b603

## R1 resolution

Paths in the tables are relative to `Theory_work/Wave3/W3-FAMC/`.

| ID | Resolution | Reason |
|---|---|---|
| S1 | PARTIAL | §0 defines X and §1R imports the setting, points to the separation bound and conditions delivery on (S4). The group-sign condition and the scope of the delivery guarantee still need correction (N1–N2). |
| S2 | RESOLVED | The ordered visibility vectors and closure match VIS:20–27. Nullity is limited to finite labelled local patterns and fixed AR, and the distance requirement applies only to the generic routes. |
| S3 | PARTIAL | §2 adds explicit classes and correctly sources (S3) and (S4). The floor row misstates its role and scope, and the (S1) citation points to the growth row (N3–N4). |
| S4 | RESOLVED | B.V1 keeps the signed equality and places the lower bound on the magnitude. |
| S5 | RESOLVED | Both files state the magnitude bound and account for sign flips and independence at ρ = 0. |
| S6 | RESOLVED | §3 cites A.assembly B.0 for the cross-group calculation and TRACK_B B9 for the candidate route. |
| S7 | RESOLVED | The three L6 pointers cover the neighbourhood definition, (0.1), the rates and their use in E2. |
| S8 | RESOLVED | §1b distinguishes design groups from capped method blocks and records the conditioning and floor sizes. |
| S9 | RESOLVED | §5 drops the E2 coverage claim for correlations tending to ±1. |
| S10 | RESOLVED | §5 ties failure to a null–truth covariance bounded away from zero. The AR example holds in Theorems 5 and 10 because both require p > s₀, so the column order has an adjacent null–truth pair. |
| S11 | RESOLVED | §5 limits the finite-n exclusion to statistical recovery and preserves the separate delivery guarantee. |

## Findings

| ID | Severity | File:line | Problem | Fix |
|---|---|---|---|---|
| N1 | MAJOR | `STATEMENT.md:38–39` | The reader's group-sign description requires signs that make partial correlations nonnegative but leaves out their compatibility with the true coefficient signs. In a two-column group with correlation ½, using both positive flips makes the stated partial correlations nonnegative even for coefficients (1, −2). Those coefficients cancel the first truth at U = ∅ and fail (BLK-s). | In each group containing multiple truths, require a single system of column flips that makes all partial correlations nonnegative and gives the flipped true coefficients a common sign, as in (BLK-s). For AR, state that negative ρ uses original column-index parity and zero ρ imposes no sign restriction. |
| N2 | MINOR | `STATEMENT.md:41–42` | The delivery sentence switches from “every admissible run” to “every run.” The (S4) reference restores the premise but the reader version omits the admissible-n scope and the bounded-domain and guard qualifications carried by §1 and the reader Theorem 6. | Keep “admissible” in the delivery sentence, scope it to n ≥ 3, and carry §1's qualifications on the lifted integer limits, bounded domain and time guard. |
| N3 | MINOR | `STATEMENT.md:103` | The unqualified floor is grouped under (A1)–(A2) and attributed to Theorem 6 itself. The reader's floors are under (A5) and FAMC obtains them from the design. Compliance line 38 classes the O(log n) floor as 1, while line 41 classes the floor on Q ∪ {l} as 2b. | Leave Gaussian rows and fixed signals in the inherited row. Record the two (A5) floors and their classes explicitly, with the design routes as their source. |
| N4 | MINOR | `STATEMENT.md:104` | Compliance line 20 supports the polynomial growth assumption (S2). The class-1 source for the Gaussian model with independent errors in (S1) is line 18. | Cite lines 18 and 20 for (S1) and (S2), respectively. |
| N5 | MINOR | `STATEMENT.md:179` | DP1 says the check is in the FAMC manifest. At the reviewed commit the Opus report is present and `PLAN.md:35–36` still puts the manifest freeze after R2. | Name the checked-in review as the evidence and describe manifest inclusion as pending until the freeze. |

The eleven input version and status pairs in §4 match both the checked-out registry and the pinned registry at `a779c1df`. The DP1 description matches the Opus report's verdict and its AR-specific cross-check. The DP1 decision records the FAMC result unconditionally while preserving the registry statuses of Ex-PolyR, BC and IR. E2's correctness was outside this review.

VERDICT: PASS WITH CHANGES
