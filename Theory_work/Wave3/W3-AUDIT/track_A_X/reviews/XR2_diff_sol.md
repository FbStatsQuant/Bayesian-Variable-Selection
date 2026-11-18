# Council XR2 — sol — diff round

**ACCEPT X1, X3, X5 and T14 within the qualifications accepted in XR1.** No C, S or F finding is held; gates=PASS. The T14 revision supplies a structural size argument independent of T9's arithmetic hypotheses. X1, X3 and X5 are unchanged and retain their XR1 decisions; their unchanged text was not re-reviewed.

Reviewed manifest: `5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6`. The prescribed verifier returned `verify: OK` for this manifest.

## Disposition of this seat's XR1 findings

| XR1 finding | disposition | basis |
|---|---|---|
| 1 — E: X5 amended PoolZ notation | NOT RESOLVED | The diff changes only T14. The requested superscripts in the X5 statement/proof are not repaired. This remains the nonblocking editorial finding recorded in XR1, with the surrounding qualification controlling the claim. |
| 2 — E: X3 informal source-domain summary | NOT RESOLVED | The diff changes only T14. The requested explicit “p ≥ 2” and “integer m” remain unaddressed. This remains nonblocking because the referenced source domain controls the claim. |

Neither outstanding E finding holds a gate open under the prescribed C/S/F standard.

## Diff review

**No new C, S or F finding.**

The revised T14 Step 3 is sufficient for the bound needed at the evaluated cap guard:

- `mode_dp` initializes `kbest` to −1 and assigns it only from the scan over 0 through K (`Scripts/SMC_BVS/core/cpp/v3_start.h:193,220-224`). This remains true regardless of the computed floating-point scores, including failed score comparisons.
- The enumeration subtracts nonnegative block sizes and accepts only a leaf with remaining size zero. Every chosen code comes from `arg[b][j]`, which is populated only from `codes_by_size[b][j]`; those codes have popcount j. Thus every accepted leaf contributes exactly `kbest` entries, using the existing block partition. If no leaf is accepted, `bestS` remains empty. In particular, `kbest = −1` yields no accepted leaf. Truncation selects among accepted leaves and cannot enlarge their size (`v3_start.h:109-111,201-209,279-303`).
- For the fallback, `allowed` records whether a code satisfies the current IN/OUT masks, and `feasible()` computes reachability through tight edges with sizes summing to `kbest` (`v3_start.h:240-258`). The root check rejects a negative `kbest` or infeasible root. At each inclusion attempt, success preserves a witness; on failure, every prior witness excludes that index, so moving it to OUT preserves a witness. After all p indices have been classified, the surviving path's block codes agree with IN on every index. The returned vector therefore has exactly `kbest` entries (`v3_start.h:261-269`). This uses the Boolean reachability and integer size bookkeeping, without requiring optimality or exactness of the floating-point scores.

Consequently a returned `m.S` has size at most K on either branch. Conditional on the guard site being reached, the preceding call has returned, so no termination, allocation or root-feasibility guarantee is needed. The unchanged cap arithmetic therefore still follows from this replacement argument. The replacement removes the use of T9 and its EX-A/H2-FP alternatives; it does not import a new arithmetic premise. The statement's change from [2,32] to [3,32] agrees with the already established lower bound in XR1. The broader wording about “any arithmetic” is read in the claim's retained scope: it removes score-arithmetic idealization, while the explicit exclusion of general native integer safety remains controlling.

The CHECK change updates the frozen hashes, and CITECHECK adds the five new source blocks. Both updated file hash prefixes match, and all five added citation-block SHA prefixes match the source when hashing the joined lines without a terminal newline. A read-only diff of `v3_start.h` against code pin `4676af6` returned exit 0. No dependency propagation is required: the brief specifies that no other package item depends on T14.

## Per-claim decisions

| id | decision |
|---|---|
| X1 | ACCEPT — unchanged; retain XR1 scope and assumptions |
| X3 | ACCEPT — unchanged, VERIFIED; retain XR1 scope |
| X5 | ACCEPT — unchanged, VERIFIED WITH AMENDMENTS; retain the uninterrupted pair/potential-evidence scope, MEAS-J and joint independence for the joint-law form |
| T14 | ACCEPT — revised structural proof supports REP-b without T9's arithmetic hypotheses; retain shipped-default and evaluated-site scope |

## Gates and score

G1–G6 remain PASS within this diff review. No new correctness, hypothesis, import, scope or code-fidelity issue is held. The two unresolved E findings remain nonblocking. **Score: 9.4 / 10.**

Reviewed only this seat's XR1 report, the supplied diff, the input list and the relevant permitted source code; manifest verification hashed the frozen package. Did not open the other seat's review or any disposition, and did not re-read unchanged claim text. No runtime experiments or formal proof-assistant checks were performed. No subagents were started and no git state was changed. The only authored file is this report.

COUNCIL-VERDICT round=R2 manifest=5db04d3a8e3c408d826a0d28af1825dc4cad0abe345df28d55f2b8928d5c64d6 seat=sol score=9.4 gates=PASS
