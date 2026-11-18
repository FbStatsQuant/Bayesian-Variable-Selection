R3 diff-only review, seat `sol`, on manifest `43b2366bf27f0e778853274910883be7587f1a43600e079bb8a83f2d53b1d0ab`.

Both manifests contain the same 28 paths; only `READER_DELTA.md` changed. All 28 current hashes match R3, whose aggregate digest also verifies. Reversing the two supplied diff hunks exactly reproduces the R2 reader-file hash. Unchanged claims, proofs and statuses retain their R2 acceptance; they were not re-reviewed.

(a) Carried findings:

- **F5 — RESOLVED:** [READER_DELTA.md:63](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:63) now specifies centred N(0, σ²_𝒞) contrasts, with the variance of (A0), rather than an unspecified Gaussian mean and common variance.
- **F-R2-1 — RESOLVED:** [READER_DELTA.md:65](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:65) explicitly subtracts the omitted contribution's linear candidate component and gives its centred contrast variance σ²_𝒞 − σ², allowing zero.

(b) **No new C, S or F finding.** The changed explanation matches CorG-min (a)+(c): full-vector (A0) is sufficient, while the required conditional residual-contrast law is N(0, σ²_𝒞 I). Under the stated independent Gaussian noise assumption, this is equivalent to the adjusted omitted-contrast law N(0, (σ²_𝒞 − σ²)I), with σ²_𝒞 − σ² ≥ 0, including the degenerate zero case. The total residual variance remains positive through (A0). The residual's sample mean is unrestricted. These are precisely the contrast-level assertions of [STATEMENT.md:57](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:57), (a) at line 63 and (c) at line 71.

The revised [summary row at line 17](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:17) is faithful in context: it centres the reference mean, requires posterior support mass to converge to one in probability, and requires uniform convergence for the uniform assertion. The common constants, energy/floor conditions and bounded support size are supplied by the detailed reader remark at lines 55–57. Its random-design summary agrees with CorH-U (RD) and the Gaussian-row instance (G); it does not introduce an unconditional uniformity claim. The governing clauses are [CorH-plus (a′)](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:114), [CorH-U (U-a)](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:139), [(RD)](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:143) and [(G)](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:152).

(c) Per-claim decisions, carrying forward R2 acceptance with all stated conditional inputs:

| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

(d) Gates on manifest R3:

- **correct: PASS** — the diff agrees with the permitted masters and leaves the accepted formal claims and proofs unchanged.
- **strength: PASS** — sufficiency, Gaussian-noise equivalence and uniformity have their required qualifications.
- **faithful: PASS** — both carried defects are repaired; the changed reader text matches its masters.
- **statuses: PASS** — status-bearing files are unchanged; the reader retains its proposal and conditional-input qualifications.
- **sweep: PASS** — manifest hashes and the exact two-hunk diff were verified; the scoped review found no C, S or F defect.
- **reader: PASS** — both revised passages accurately express their master clauses in the supplied reader context.

(e) Score: **10.0/10.0**, assessing C, S and F only within this diff-only round. No substantive finding remains. No scratch directory was created.

COUNCIL-VERDICT round=R3 manifest=43b2366bf27f0e778853274910883be7587f1a43600e079bb8a83f2d53b1d0ab seat=sol score=10.0 gates=PASS
