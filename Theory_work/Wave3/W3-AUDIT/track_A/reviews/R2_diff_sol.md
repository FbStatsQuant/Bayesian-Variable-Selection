# Council R2 diff review — sol — T1–T10

All four of my R1 findings are resolved. I find no new C, S or F defect in the diff or its specified dependent uses. All ten claims are ACCEPT, with the execution premises and potential-run interpretation now stated in the repaired package.

**Frozen content.** Reviewed manifest `93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff`. The prescribed `python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A Theory_work/Wave3/W3-AUDIT/track_A/reviews/MANIFEST_R1d.txt` returned `verify: OK` for that digest. `MANIFEST_R2.txt` and `MANIFEST_R1d.txt` compare byte-for-byte equal. This is a diff review against my own R1 review, not a fresh full review of unchanged proofs.

**Disposition of my R1 findings**

1. **R1 #1 (S, T2 native execution domain): RESOLVED.** T2 STATEMENT v6, lines 32–35 and 46–60, defines C(X) by the abstract cut-and-pack program with unbounded integers and exact reals on the whole design domain. BLK-a–c concern that map. The new BLK-d identifies the native implementation with it only on executions without integer overflow and with successful allocations. PROOF lines 63–69 supplies the corresponding execution argument. The intermediate `2 * p` restriction is correctly retained: native evaluation of `2 * p - 1` requires p < 2³⁰, even though the final mathematical value at p = 2³⁰ would fit. The correlation/distance allocation obligations are explicit. The full-domain partition remains available for hypothetical enumeration-branch objects and asymptotic arguments.

   The dependent repair is present: T4 STATEMENT lines 22–25 carries the execution premise, and T4 PROOF's blocks paragraph invokes BLK-d within that setting. T6 STATEMENT line 22 expressly uses those executions. This removes the unrestricted native identification that caused my objection without restricting the abstract partition theorem.

2. **R1 #2 (C, T8 integration over actual success): RESOLVED.** T8 PROOF v4, lines 37–48, starts from the valid pathwise inclusion

   `completed ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜° ∩ {S₀ ∉ 𝓜°_r})`.

   T1's completion comparison and PC supply equality with the potential island's evaluated set on completion; the ledger contains that set. T5 CAL-b makes 𝒜° measurable with respect to 𝓒°, while CAL-c freezes the potential draw budget. D-i then bounds the conditional miss probability given the data and 𝓒° on 𝒜°. Integrating directly gives the expectation with `1_𝒜°`; no intermediate inequality with actual `1_𝒜` is used. STATEMENT lines 50–55 gives the same repaired argument. The exponential estimate and OVL-b finish the limit by taking limsup for each c > 0 and then c → ∞, with P-MAP controlling the other term. The revised budget wording correctly refers to the frozen uninterrupted run. No clock-independence assumption has been introduced.

3. **R1 #3 (S, T9 omitted H4): RESOLVED.** T9 STATEMENT v3, lines 24–30, restores the representable positive `long` cap, representable counters, successful allocations and completion of depth-J recursion. It distinguishes finite algorithmic correctness/cost from compiled-code return claims. The PROOF v3 preamble applies H4 to the latter throughout. These are the execution obligations of the cited TDP_E and W1-N3 sources. TDP-e, lines 37–40, now states precisely that the root-validation throw does not fire when reached; it does not purport to eliminate allocation or process/stack failures. The cap ≥ 2 restriction and the shipped cap 10⁶ remain intact.

4. **R1 #4 (E, status evidence discoverability): RESOLVED.** The new frozen `STATUS_EXTRACT.md` provides the permitted registry-status extract requested in R1, with source attribution and rows for W3-START2-R:IF-START, W3-START2-R:OVL and W3-RM:E4. T8 points to it. This resolves the evidence-access limitation; I have not independently reopened the underlying council reports or registry. The deferred T3 cross-reference in ERRATA does not prevent a reviewer from finding E4's status in the supplied extract. No new editorial finding is added in this round.

**Diff and dependent-use checks**

| changed object → dependent | result |
|---|---|
| T2 → T4 blocks | PASS. T4 explicitly assumes the BLK-d execution domain before identifying `st.blocks` with C(X). Encoding and immutability conclusions retain their R1 acceptance. |
| T2/T4 → T6 | PASS. The sampling-law argument uses the same disjoint blocks, finite positive entries and code/set bijection. The explicit execution-domain pointer changes no convolution or telescoping identity. |
| T2 → T10 PROOF §2(i) | PASS. This use is only B ∈ [1,16], derived directly from the shipped minimum and exact integer-square-root computation. It does not require unconditional execution of native clustering. |
| T4 → T3 start mode | PASS. T3's operational assertions concern completed runs and the centre actually returned by `start_mode`. Its disclaimer retains H4 for the separate E4 maximization conclusion. The repair adds no missing maximization requirement to OPC. |
| T4 → T9 setting | PASS. The required encoding is available on T4's stated executions; T9 separately carries the subsequent fallback/enumeration execution obligations. Successful setup is not used as a substitute for them. |
| T9 → T10 X9 | PASS. Cap 10⁶ excludes the explicit cap-validation throw; TDP-e excludes the root-validation throw when reached with the stipulated encoding/arithmetic. X5 and MACH continue to account for allocation and process failures. |
| T8 → W3-SAMP D-iv | PASS. The repaired potential-event bound proves the completed-output conclusion under P-MAP and P-OVL on 𝒜°. It replaces the disputed actual-event D-iii step; it does not assume that step valid. |

I inspected all supplied diff hunks, including CHECK/CITECHECK changes and the new status/errata files. The administrative changes do not alter the mathematical arguments or silently promote the package to a checked registry status. Existing editorial items remain deferred as recorded. No new C, S or F finding.

**Statement-change checks**

| item | repair | tag assessment |
|---|---|---|
| T2 v6 | Abstract full-domain map; conditional native identification | WEAKER for native identification confirmed; the abstract partition/measurability content is preserved. BLK-d explicitly states the restricted implementation bridge. |
| T4 v3 | Native execution premise made explicit | WEAKER confirmed; dependent uses checked above. |
| T6 v2.1 | Pointer to T4's execution domain | EQUAL as a clarification within the inherited T4 setting; the inherited execution restriction is retained. |
| T8 v4 | Potential-event proof and frozen-budget wording | EQUAL for the final bound/interface; the invalid intermediate proof step is replaced. |
| T9 v3 | H4 restored for native return claims | WEAKER confirmed for native claims; algorithmic conclusions and cost envelope remain unchanged. |

**Per-claim decisions**

| id | decision |
|---|---|
| T1 | ACCEPT |
| T2 | ACCEPT |
| T3 | ACCEPT |
| T4 | ACCEPT |
| T5 | ACCEPT |
| T6 | ACCEPT |
| T7 | ACCEPT |
| T8 | ACCEPT |
| T9 | ACCEPT |
| T10 | ACCEPT |

T1, T3, T5, T7 and T10 retain their R1 acceptance; their specified affected uses were checked above. T2, T8 and T9 move from REJECT to ACCEPT after repair. T4 and T6 retain acceptance on their now explicit execution domains.

**Gates**

| gate | decision | basis |
|---|---|---|
| G1 correctness | PASS | Repaired native bridges and potential-run probability argument are valid; no dependent argument breaks. |
| G2 hypotheses used = stated | PASS | Native integer/allocation/recursion obligations and the potential calibration conditioning are explicit. |
| G3 no hidden assumptions | PASS | No independence of the actual success event from final randomness is used; successful setup does not discharge later execution obligations. |
| G4 imports and statuses | PASS | TDP_E's H4 is carried; D-i is used on the potential pair; requested status evidence is supplied in the frozen extract. |
| G5 scope and constants | PASS | Full-domain abstract statements coexist with conditional native claims; production budget and fixed-cap cost conclusions are preserved. |
| G6 fidelity to the method as coded | PASS | Execution qualifications match the pinned integer/allocation and start-mode paths; the core has no diff from 4676af6. |

**Score: 9.1 / 10.** No C, S or F finding remains. Editorial records do not reduce the score.

**Verification and limits.** Besides manifest verification and manifest equality, ran read-only `git diff --exit-code 4676af6 -- Scripts/SMC_BVS/core`, which returned exit 0 with no diff. Checked the changed execution premises against the permitted C-DLV, W1-N3 and TDP_E excerpts and the relevant pinned C++ operations; checked the T8 repair against T5 and SAMP's D/PC interfaces and proof steps. This review does not newly prove unchanged statistical results, binary64 statistical accuracy, resource guarantees or PRNG independence. I did not open the other seat's review or any disposition, start subagents, or change git state. The only file written is this review.

COUNCIL-VERDICT round=R2 manifest=93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff seat=sol score=9.1 gates=PASS
