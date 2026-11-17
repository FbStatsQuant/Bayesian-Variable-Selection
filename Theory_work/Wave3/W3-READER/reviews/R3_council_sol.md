# W3-READER — council R3, seat sol

Frozen content reviewed: MANIFEST `7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263`.

The required manifest verification was the first check and printed `verify: OK` with this exact digest. This is the requested R2 → R3 diff-only confirmation; it preserves the R2 acceptance of unchanged content. I read the seat brief, the supplied diff, the two permitted R2 reviews, changed text in context, and the relevant master, registry and code passages. I did not read other review files, LOG.md or checkpoints, delegate, commit, or edit deliverable content. The only file created is this review.

**Score: 9.5/10.0 (C, S and F only). Accept as is.** All 14 items are accepted, with no findings. Acceptance preserves every conditional, audit and author-only status already stated; it does not certify additional premises.

## Scope and checks

- The supplied diff is byte-for-byte equal to `git diff ae8acc8e 68443dcc` on the ticket folder with reviews/ and LOG.md excluded.
- Current tracked ticket content, with those exclusions, equals commit `68443dcc`.
- All changed content is accounted for by the 14 items below or the permitted version header, update logs and DEPS bookkeeping. No additional substantive change was found.
- `git diff --check` on the same commit range and paths passes.
- DEPS whole-file hashes for R1–R4, NOTATION and CARD match; all ten reader-row hashes match the complete marked row blocks. Dependencies, previous checked hashes and the pending/stale qualifications are preserved.
- The changed Ex-PolyR quotation was checked against the registry's named `status` field at version 1.0.3; it is an exact prefix with the declared ellipsis convention, including all conditional inputs.

## Per-item decisions

Locations below refer to current R3 line numbers.

| tag | decision (ACCEPT/REJECT) | note |
|---|---|---|
| R2-O1 / R2-E2(sol), single conditioning | ACCEPT | [CLAIMS_CARD.md:73](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:73): removes only the duplicated conditioning phrase. Calibration success, data/calibration conditioning, four potential records, completed-field equality and the exclusion of completion-conditioned unbiasedness remain explicit. |
| R2-O2 | ACCEPT | [READER_VERSIONS.md:148](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:148): the corrected size condition follows from checked Corollary B. For this theorem's s₀ ≥ 1, c(p,s₀) ≥ 1, so δ ≥ 1/(√n+1). No p/2 condition is needed for this weaker n⁻¹ᐟ² obstruction. |
| R2-O3 | ACCEPT | [METHOD_INTUITION.md:71](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/METHOD_INTUITION.md:71), also line 72: both inequalities now say “at least”; both probability-tending-to-one qualifiers and their respective exponent ranges are retained, exactly as START-R. |
| R2-O4 | ACCEPT | [READER_VERSIONS.md:833](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:833): C_Q > max{32,64A+c} is sufficient eventually for the master's BM-Q♭, with c selected as in Remark (a). The strict slack absorbs the n−1 versus n factor and additive constants. It is not asserted for every finite n. |
| R2-O5 | ACCEPT | [STATEMENT.md:43](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/STATEMENT.md:43): adding Theorem 10 accurately records its B2.1/B6.1 uses through R4 and B10.1/B10.2; no bridge or conclusion changes. |
| R2-O6 | ACCEPT | [READER_VERSIONS.md:704](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:704): Ex-PolyR@1.0.3 is quoted verbatim up to the marked ellipsis. The Astra/Opus distinction and POST/BC/IR conditions remain; the example is not promoted to a checked hypothesis. |
| R2-O7 | ACCEPT | [R4_printed_outputs.md:49](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/lemmas/R4_printed_outputs.md:49): completion now cites active deterministic DLV-0, with F-UNI Step 2 explicitly history. S4, IDEAL-W⁺ and the alternative domain 𝔇 remain prerequisites. This remark does not supply an unconditional calibration-success claim to R4. |
| R2-O8 | ACCEPT | [METHOD_INTUITION.md:82](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/METHOD_INTUITION.md:82): the parenthesis restricts the informal mechanism sentence to the uninterrupted final estimate given calibration, consistently with N1 and PoolZ. The surrounding setup retains a successful/fallback frozen schedule. |
| R2-O9 | ACCEPT | [REPORT.md:13](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/REPORT.md:13): the registry-facing conclusion now carries the potential-record, fixed-data and completed-field distinctions already present in PoolZ; it adds no expectation conditional on completion. |
| R2-O10 | ACCEPT | [CLAIMS_CARD.md:7](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:7): restores the requested historical v1.8 wording; v1.11 records its correction and the live row 3.1 retains the correct distinction between original Prop-F, frozen F-UNI and active DLV-0. |
| R2-E1(sol) | ACCEPT | [CLAIMS_CARD.md:69](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:69) and [READER_VERSIONS.md:887](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:887), also line 888: row 3.1 names R2 and B6.6′, labels R3 historical, and the old BM commentary is expressly under former hypotheses. Current width implications remain usable; current truth removal points to B7.2′/B7.3′. |
| R2-E2(sol), exact rate ratio | ACCEPT | [READER_VERSIONS.md:1350](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1350): dividing n⁻¹ᐟ² exp(C√log n) by √(log n/n) gives exactly exp(C√log n)/√log n. This compares reference rates, without claiming exact stochastic orders. |
| R2-L1 | ACCEPT | [READER_VERSIONS.md:1348](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1348): row 3.1 is limited to particular AR/block designs satisfying Theorem 6's conditions. The design-free row 3.5 pointer retains its separate scope. This matches the already-correct card row 3.6. |
| GUARD-W | ACCEPT | [READER_VERSIONS.md:846](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md:846) and [CLAIMS_CARD.md:70](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:70): the time-guard qualification matches Theorem 6 and the code. “No output” means no estimates under NOTATION §5, and does not deny the incomplete diagnostic/model record. No output on stopped runs is promised. |

## Mathematical and interpretive confirmation

For R2-O4, put q = |Q| and t = log n. The new signal premise gives λₙ ≥ (1−1/n)C_Q(q+t). Since p ≤ nᴬ, the BM-Q♭ right side is at most

`32q + (64A+c)t + 32 + 64 log 2`.

Choose d = (C_Q−max{32,64A+c})/2 > 0. Eventually (1−1/n)C_Q ≥ max{32,64A+c}+d, and d t ≥ 32+64 log 2. The required inequality therefore follows uniformly in q ≥ 0. Remark (a)'s c > max{16,c_TL⁰} permits c_TL with c_TL⁰ < c_TL ≤ c, as required by the master's sufficient form. This confirms the new example without changing the theorem's asymptotic quantifiers or signal scale.

The Corollary B pointer, both start-mass lower bounds, the calibration-conditioned potential-evidence descriptions, historical/current bridge distinctions, exact rate comparison and conditional AR/block pointer are all supported interpretive sentences. The changed time-guard sentence is supported by the operational code and the established output definition. No changed sentence is overstated or unsupported (D71).

Code confirmation: calibration guard stops propagate `resource_limit` at [v3_calib.R:81](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_calib.R:81) and line 113. The fit's finish path marks such returns partial and clears unavailable estimates at [v3_fit.R:84](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_fit.R:84); calibration failure returns through this path at line 154. Final non-completed runs retain an incomplete model record and clear estimates at [v3_run.R:142](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_run.R:142). Successful runs compute the equal-weight evidence mean at line 154. These checks support the changed code facts without asserting any stochastic identity after selection on completion.

## Findings

C: none. S: none. F: none. E: none.

## Gates

| gate | decision | reason |
|---|---|---|
| G1 correctness | PASS | The corrected lower-bound domain, sufficient constant, evidence scope and exact rate quotient are valid. |
| G2 hypotheses used = stated | PASS | Constant slack is sufficient eventually; S4/DLV-0 prerequisites and potential/calibration scope remain explicit; AR/block coverage requires Theorem 6's conditions. |
| G3 faithfulness | PASS | Every changed item does what the brief specifies and adds no stronger master conclusion. No unlisted substantive change was found. |
| D71 interpretive sentences | PASS | All changed interpretive assertions are supported as detailed above. |
| G4 statuses verbatim | PASS | The changed Ex-PolyR quotation matches the registry with its declared ellipsis and retains all conditional qualifications. No status is upgraded. |
| G5 no hidden finite-n or scope claims | PASS | The constant example is eventual; the universal lower bound retains its domain; potential/completed distinctions and restricted AR/block coverage remain explicit. |
| G6 code fidelity | PASS | Guard status, unavailable estimates, incomplete diagnostic model and completed equal-weight evidence pooling match the code. |

FIDELITY: FAITHFUL

COUNCIL-VERDICT round=R3 manifest=7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263 seat=sol score=9.5 gates=PASS
