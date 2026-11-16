## W3-RM2-R council R3 (HQ-ordered re-check) review — seat sol (codex gpt-6.1-sol, reasoningEffort high; new thread). Reply verbatim below (link targets shortened).

Manifest R3 verified successfully: `b06a85885d45ecfe6baa0e6340cb5a43eb1c99b2ec2906b191bd0febb08db9a1`. Review is limited to the authorized diff and dependent text. No files or git state were changed; no scratch was created.

**(1) R2-sol-F1 — RESOLVED.** [TARGET.md:34] now restricts the low-κ failure bounds to truth removal at S₀ and the LS0 endpoint, and separately reports design G’s persistent start-mode inclusion failures, matching [RESULTS.md:190].

**(2) New findings: none.** No new C/S/F finding arises in the changed lines. The replacement sentence correctly distinguishes design P from design G, reports inclusion in 5/10 and 5/6 runs at κ = 32, and retains the numerical limitations and statement that asymptotic necessity is not established.

The REPORT and H5_SUMMARY changes accurately describe this seat’s R2 outcome. The ERRATA annotation introduces no mathematical change. The permitted REPORT registry dependencies and READER_DELTA bridges remain consistent with the specified STATEMENT passages. No E findings are added.

**(3) Per-claim decisions**

These decisions carry forward the accepted R2 theorem assessments; unchanged proofs were not reopened.

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

Acceptance retains SOP:TH09 for RM2-F-plus and Ex-Proxy-d, W2-APP:POST for RM2-R-plus, and the inherited audit qualifications for DLV-0.

**(4) Gates**

Item (4) of the brief names R2, while the mandatory verdict binds R3. Both are distinguished below; the R2 column preserves this seat’s historical assessment.

| gate | R2 | R3 | R3 assessment |
|---|---|---|---|
| correct | PASS | PASS | No mathematical claim or proof changes; checked dependent text remains consistent. |
| strength | FAIL | PASS | The observed failure bounds now apply explicitly to the supported events. |
| faithfulness | FAIL | PASS | TARGET agrees with RESULTS on start-mode inclusion and LS0 recovery. |
| lit | PASS | PASS | The inherited assessment is unaffected by this diff. |
| necessity | PASS | PASS | The sentence expressly denies establishing necessity. |
| better | PASS | PASS | No changed line disturbs the inherited assessment. |

Overall score on C/S/F only: **9.5/10.0**. No C, S, or F finding remains within the authorized review scope.

COUNCIL-VERDICT round=R3 manifest=b06a85885d45ecfe6baa0e6340cb5a43eb1c99b2ec2906b191bd0febb08db9a1 seat=sol score=9.5 gates=PASS
