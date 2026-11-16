## W3-RM2-R council R2 (diff round) review — seat sol (codex gpt-6.1-sol, reasoningEffort high; new thread). Reply verbatim below (link targets shortened).

Manifest R2 verified successfully. This review is limited to the authorized diff and dependent text; unchanged theorem decisions carry forward from R1. No files or git state were changed, and no scratch was created.

My R1 findings:

- **R1-sol-1 (F) — RESOLVED.** [TARGET.md:24] withdraws the unsupported Song–Liang attribution and retains the independently accepted YWJ comparison.
- **R1-sol-2 (S) — RESOLVED.** [TARGET.md:10] explicitly labels the order discussion heuristic and states that necessity is not proved.
- **R1-sol-3 (E) — RESOLVED.** [numerics/RESULTS.md:158] now identifies the empty set as the binding truth-removing competitor in these runs.
- **R1-sol-4 (E) — RESOLVED.** [READER_DELTA.md:61] chooses fixed \(D>2+4A\) and a strict coefficient margin, absorbing \((n-1)/n\) for sufficiently large onset.
- **R1-sol-5 (E) — RESOLVED.** TARGET now names statement v1.0 and describes the completed sweep through \(\kappa=32\), including the mode proxy’s limitation. The replacement summary introduces the separate finding below.

The diff introduces one new finding:

**R2-sol-F1 — F: numerical summary incorrectly includes start-mode failures in its low-\(\kappa\) bound.** [TARGET.md:34] follows a list including start-mode inclusion with the unqualified assertion “failures only for κ ≤ 4 (n = 400) and κ ≤ 2 (n = 1600).” Those bounds describe LS0 endpoint and base-set truth-removal failures. They do not describe start-mode inclusion: design G has inclusion in **0/10 and 0/6 runs through \(\kappa=16\)**, and only **5/10 and 5/6 at \(\kappa=32\)**. See [RESULTS.md:194] and the following row.

**Fix:** qualify the sentence explicitly:

> Across the sampled cells, LS0 endpoint and truth-removal-at-\(S_0\) failures occurred only for κ ≤ 4 at n = 400 and κ ≤ 2 at n = 1600. Start-mode inclusion in design G still failed in some runs at κ = 32.

Retain the finite-sample and no-asymptotic-necessity qualifications. No other new C/S/F finding arose within the authorized scope.

The changed REPORT entries correctly separate TL-F-c from POST/MODE-F, retain the latter under the conditional RM2-F-plus claim, and carry SOP:TH09 into Ex-Proxy-d. The added DLV-0 dependency records agree with the permitted STATEMENT dependency text.

| id | decision |
|---|---|
| W3-RM2-R:RM0-plus | ACCEPT |
| W3-RM2-R:DLV-0 | ACCEPT |
| W3-RM2-R:RM2-F-plus | ACCEPT |
| W3-RM2-R:RM2-R-plus | ACCEPT |
| W3-RM2-R:SAND-F-c | ACCEPT |
| W3-RM2-R:TL-F-c | ACCEPT |
| W3-RM2-R:Ex-Proxy-d | ACCEPT |
| W3-RM2-R:Cont-plus | ACCEPT |

These decisions retain SOP:TH09 for Form F and Ex-Proxy-d, W2-APP:POST for Form R, and the inherited audit qualifications for DLV-0.

| gate | result | reason |
|---|---|---|
| correct | PASS | Accepted mathematical claims remain unchanged; checked bridges agree. |
| strength | FAIL | TARGET overstates the scope of the observed failure bounds. |
| faithfulness | FAIL | TARGET’s numerical summary contradicts RESULTS on start-mode inclusion. |
| lit | PASS | The unsupported comparator attribution is withdrawn. |
| necessity | PASS | Necessity is explicitly unproved; numerical limitations are retained. |
| better | PASS | No new issue within the authorized diff changes the R1 assessment. |

Overall score on C/S/F only: **9.0/10.0**. The remaining finding concerns the numerical summary and does not invalidate the accepted theorem claims.

COUNCIL-VERDICT round=R2 manifest=e71637e0a175535f82cf9a86996974e83b968caa5df9981d97bc59b69a88190b seat=sol score=9.0 gates=FAIL
