# Council R2 — sol — diff review

Reviewed MANIFEST fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e against my R1 review and the supplied R2 diff. I read TARGET.md, READER_DELTA.md, ERRATA.md and DEPS.tsv, and compared the changed assertions with the unchanged STATEMENT.md. I independently recomputed the manifest identifier and all 21 input hashes (14 local, seven external), verified complete local input coverage, and checked all 18 populated hash fields in the 11 DEPS rows. All match. Comparing the two manifests confirms that only TARGET.md, READER_DELTA.md and DEPS.tsv changed, with ERRATA.md added; no input was removed.

This is the requested diff round: the R1 mathematical checks and unchanged-proof conclusions carry forward. I did not reread the unchanged proofs, other seats' reviews, dispositions, LOG or checkpoints. No git operations or subagents were used. Only this output file was written.

| id | decision |
|---|---|
| W3-PSHARP-R:AE | ACCEPT |
| W3-PSHARP-R:A2C | ACCEPT |

**Overall score: 9.5/10.0 (C/S/F only). Gates: PASS.**

## R1 finding status

**F1 — RESOLVED.** Both offending derived copies now respect the lower-bound scope of the master.

- TARGET.md:28 explicitly states `E δ_n ≥ (1 − o(1)) C_{p,s₀} r_n`, gives `C_{p,s₀} = (s₀+1)[2(p−s₀)/(2p−1−s₀)]/√(2π)`, and expressly disclaims an upper bound. This is exactly STATEMENT.md:83–84, with the constant collected into one symbol. It no longer implies the false unconditional two-sided fixed-p rate identified in R1.
- READER_DELTA.md:22–23 now distinguishes the expectation lower bound for every admissible p from exactness where a matching expectation upper bound is available. It agrees with the proposed reader text at :45–47 and STATEMENT.md:104–113, :121–123. In particular, the fixed-p upper half remains unchecked rather than being advertised as proved.

R1 contained no C or S findings and no other F findings of mine.

For completeness, my existing editorial findings E1, E2 and E3 remain unapplied and are recorded in ERRATA.md:7, :11 and :14 respectively. Their status is **deferred editorial correction**, not resolution by this diff. They do not affect the score or gates. No new E findings are added.

## Does the diff break anything?

**No new C/S/F problem found.** Besides F1's repair, READER_DELTA.md:48–50 narrows the growing-s₀ expectation-rate consequence to orthogonal null columns, or Gaussian null columns with the truth columns fixed. Its bridge B3.7 at :75 makes the same restriction explicitly using deterministic `X^r_{S₀}`. This matches the spherical structure in STATEMENT.md:52–57 inherited by Corollary A2-E at :88–91. It does not extend the random-(X_{S₀}, θ*) clause of Proposition A-E to that corollary. The existing all-nulls and `s₀ ≤ p/2` conditions are retained in the reader's consequences paragraph and bridge. Thus the additional narrowing is compatible with the master and introduces no unsupported random-design corollary.

The DEPS additions/updates describe derived texts and their existing STMT dependency, with no claim depending on either changed text. All proof and master hashes are unchanged. ERRATA records editorial work and proposals; it changes no claim, hypothesis, proof status or mathematical dependency. No downstream proof needs rechecking because of this diff. A2C's statement, proof, scope and reporting are unchanged, so its R1 acceptance carries forward.

## Gate verdicts on R2

| gate | verdict | reason |
|---|---|---|
| G1 correctness | PASS | R1's checked AE and A2C proofs and their consumed mathematical inputs are unchanged. The changed lower-bound constant agrees exactly with A1-E(b). No new incorrect assertion was found in the diff. |
| G2 hypotheses used = stated | PASS | The corrected summaries preserve the master's admissibility and upper-bound provisos. The narrowed growing-s₀ reader consequence and B3.7 agree with A2-E's deterministic spherical truth-design scope and retained all-nulls conditions. |
| G3 no hidden assumptions | PASS | No proof assumptions changed. The reader now states the relevant deterministic truth-column restriction for the Gaussian growing-s₀ consequence; no new conditional extension is asserted. R1's checks otherwise carry forward. |
| G4 statuses, citations, records | PASS | The master, proofs, REPORT and inherited records are unchanged and hash-verified. The updated DEPS hashes match their files and introduce no claim dependency on the changed derived texts. The existing editorial status note remains queued in ERRATA. |
| G5 constants and rates | PASS | The fixed-p coefficient in TARGET is exactly the coefficient of STATEMENT:84. The reader now distinguishes an expectation lower bound from a two-sided rate conditional on a matching upper bound. No theorem constant, normalisation or limiting mode changed. |
| G6 faithfulness | PASS | F1 is resolved in both locations. The changed reader scope agrees with the master. No new C/S/F mismatch was found; unchanged material retains R1's substantive checks. |

Outstanding findings of my own: **C=0, S=0, F=0**. My three previously recorded E findings remain deferred and nonblocking.

COUNCIL-VERDICT round=R2 manifest=fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e seat=sol score=9.5 gates=PASS
