# C-R1 — blind council review, seat sol

## Verdict summary

**ACCEPT C1. Score: 9.3 / 10. Gates: PASS.**

Reviewed the frozen C1 STATEMENT v2, PROOF v2.1 and CITECHECK for manifest `221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef`. The prescribed manifest verification passed. The working core and HEAD's core both agree with pin `4676af6`.

The registered audits support the claimed delivery use after A-1–A-7, in the explicitly stated configuration and under the stated idealisations. I found no additional uncovered exit, false internal-invariant exclusion, material relocation error, missing A-7 trigger, or gap in the claimed DLV-0 (E2) exclusion. This accepts amended code-reading audits; it does not upgrade their status to a formal proof or establish binary64 delivery.

## Gates

| gate | decision | basis |
|---|---|---|
| G1 correctness of steps and code citations | PASS | Independently traced the no-estimates returns, explicit errors, relevant implicit conversions and assembly, and the LS0 preflight inequalities. The cited current sites support the steps. Recorded pre-pin locations are identified as historical locations. |
| G2 hypotheses used = stated | PASS | EX-A, IDEAL-W, MACH, valid declared inputs, the default argument and all five named option settings are carried. X7–X8 are separately treated under A:IDEAL-W⁺ or the supported domain; the R dimension bound is used only for the representable-input observation. |
| G3 no hidden assumptions | PASS | Internal objects are built by preceding core calls. T9's execution qualifications are accounted for by IDEAL-W and MACH, including stack allocation; no numerical robustness, statistical success, or adequate default allocation is inferred. |
| G4 imports and statuses verbatim | PASS | P1 and S.3 remain “AUDITED (code reading)”. The argument imports the permitted sibling claims for their stated scope. DLV-0 explicitly imports FIN's enlarged allocation and distinguishes A1's resource envelopes from A4's separately checked preflight addition. No unavailable downstream proof is silently upgraded. |
| G5 configuration, options, branches and tiers | PASS | Exact enumeration, SMC, calibration tiers 0 and 1, the fallback and final LS0 are distinguished. A-7 is confined to the SMC preflight with LS0 on and the merged cap. The cached time test and tier-dependent memory re-preflight are distinguished correctly. |
| G6 fidelity to pinned code and registered texts | PASS | Pin equality, manifest identity, registered inventory/S.3 text, amendments and the consumer at `e78a1055` checked. The old memory-only B1 and exact-only B2 do omit the added LS0 trigger, as C1 states. |

## Claim decision

| id | decision |
|---|---|
| C1 | ACCEPT |

## Findings

None. C: 0; S: 0; F: 0; E: 0. No repair requested.

## Substantive checks

1. **Return completeness.** `C1_AUDITS/PROOF.md:10-34` agrees with `Scripts/SMC_BVS/core/v3_fit.R:76-173`: estimates start unavailable, become available only after successful exact enumeration or the completed final assembly, and are never enabled by `finish`. Seed, preprocessing, initial preflight, enumeration failure, setup failure, calibration failure and incomplete final-run returns map to the indicated rows. `v3_run.R:143-148` and `:218` support the final-run distinction. Guard exits during pilots/diagnostics propagate through calibration to the same no-estimates return.

2. **A-7 is necessary and its amended trigger is sufficient.** `C-DLV/INVENTORY.md:29-31` records memory-only SMC preflight, exact-branch timing, and escalation memory. At the pin, `v3_fit.R:43-47` adds archive bytes and, only when the augmented memory estimate fits, measures the size-K score time; `:61-65` adds the LS0 seconds predicate. These are precisely the additions in `C1_AUDITS/STATEMENT.md:70-75`. The initial site is `v3_fit.R:117`; the escalation path is `:144-148` through `v3_calib.R:157`. Since the timing closure caches by K (`v3_fit.R:107-112`) and the LS0 multiplier is tier-independent, escalation cannot newly fail this time predicate after it passed initially. Its larger population-memory component can newly fail, including with the same archive charge. Thus the B3 treatment does not require another time trigger.

3. **Errors and added call-graph nodes.** Repeated the explicit `stop`, `stopifnot`, `throw`, and interrupt search across the permitted R/C++ core. The map in `C1_AUDITS/PROOF.md:36-60` accounts for them, including the bare rethrow in auxiliary `cpp_start`, the separate coded LS0 guard, and `get_holder`. Read the added runtime, duplicate-component, cut-group, exact-count and timing paths. Their data access and conversions are valid for internally produced objects; allocation and environment failures retain the X/MACH classification. The timing benchmark catches its `NumericalFailure` internally (`cpp/v3_core.cpp:134`). No additional explicit no-output status was found.

4. **S.3 invariants.** Independently checked the D2 escalation argument (`v3_calib.R:126`, `:153-170`), the coded B bound, successful setup's graph flag, retained-index/model-size and provenance round trips, member/bitset consistency for `nth_nonmember`, feasible scorer inputs, equal-length V exports, context assertions, and frozen-grid/class construction. Checked the T4/T9 hypotheses against their permitted statements and production constructors. The start-mode call passes 10⁶, and the valid finite-table/root-feasibility argument excludes its other throw. The tier-1 fallback selects the last successful grid or completed pilot schedule and passes validation before freezing. With EX-A, the pilot's positive floor and exact endpoint give the required complete increasing schedule. X7–X8 remain outside the invariant claim; the stated R-representability bounds follow from default ell ≤ 32 and mode size ≤ K ≤ 2³⁰−1.

5. **Consumer exclusion.** Read DLV-0's statement and exit walk via `git show e78a1055`, including `lemmas/Q5_dlv0.md:59-67`. Its (E2) explicitly names both SMC LS0 preflight terms. FIN `s6_delivery.tex:37-44` bounds the measured 200-score interval by τU_K+τ₀, hence ŝ_K ≤ (τU_K+τ₀)/200 and 2sq(p)ŝ_K ≤ P̄_LS0. Its archive A is the same expression as `v3_fit.R:45`; memory is bounded by P_e+A for each tier. The allocation dominates these quantities, and strict `>` rejection means equality passes. C1 correctly does not attribute this added time bound to the old exact-only Lemma R preflight bound. The registered input/degeneracy, numerical, process and representability exclusions are kept separate from this resource exclusion.

## Checks performed

- Ran the exact prescribed `python3 -B .../manifest.py verify ...` command: **OK**, matching the requested manifest identifier.
- Read-only `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` and `git diff --exit-code 4676af6 -- Scripts/SMC_BVS/core`: both successful, with no code differences.
- Read C1's frozen files, the permitted input list, registered texts, FIN delivery section, permitted sibling statements and T10 proof, the relevant core code, and the permitted consumer content at `e78a1055`.
- Independently rehashed **224** recorded citation blocks within the read allowlist: all match CITECHECK. Its remaining block refers to the prohibited State-of-Project source and was not read; the historical quotation is available in permitted S.3. Read the citation-checker implementation; did not invoke its file-writing entry point.
- Ran isolated R helper checks using the pinned `v3_preflight` and a controlled timing callback, without sourcing the compiling entry point: added time rejection, archive-only memory rejection, memory-before-timing, cached timing across tiers, escalation memory rejection, and strict byte equality all **PASS**. These checks exercise predicates and orchestration; they do not emulate EX-A or validate runtime envelopes.
- Created only this review file. No git mutation, core build, cache generation, or subagent was used.

## Not checked

- Prohibited INDEX/LOG/CHECK files, other review outputs, other audit items, and the unpermitted T14 proof or State-of-Project source. No prior seat's opinion was consulted.
- Re-proofs of the council-checked sibling results, old Lemma R/Corollary R resource envelopes, or the construction of FIN A1/A4 bounds beyond checking the imported preflight inequalities and code correspondence needed here.
- Actual full-fit execution, native compilation, floating-point reliability, non-default LS0/fallback options, auxiliary public entry points outside the fit call graph, or probability bounds for reachable resource/schedule events.

COUNCIL-VERDICT round=R1 manifest=221ca4e1597f3c3a7cf25a76dc579986b5abdf3f4a52397d5546972677ec3cef seat=sol score=9.3 gates=PASS
