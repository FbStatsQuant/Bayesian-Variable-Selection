<!-- Council round R3S (HQ option (a), Sol continuation seat), seat sol: Sol (codex, gpt-6.1-sol, reasoningEffort high); brief reviews/BRIEF_R3S_sol.md; MANIFEST_R3r 64a3ec05…; one call; reply below verbatim -->
| id | decision |
|---|---|
| W3-D5P:LIST-R | ACCEPT |
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |

LIST-R remains conditional on IMPL-LIST. These decisions cover the R1 findings and changes through R3r, as requested. Manifest verification passed before and after review. All commands were read-only; no files were written, created or deleted.

R1 findings:

1. **RESOLVED — exact-branch definitions.** [READER_DELTA.md:15](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:15) distinguishes sampler list-renormalised summaries from exact-enumeration PIPs and median model; [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10) and its Option B at line 14 preserve that distinction.

2. **RESOLVED — evidence error.** [READER_DELTA.md:26](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:26) gives the relative-evidence sandwich, followed by the logarithmic bound and an explicitly named log-evidence error rate. [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10) and Option B at lines 15–17 separate the PIP, median-model and log-evidence conclusions.

3. **RESOLVED — availability qualifications.** [REPORT.md:66](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/REPORT.md:66) restores “when returned” for exact-store membership and “when `log_Z_list` is not NA” for evidence, including the rate at line 67. [READER_DELTA.md:19](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:19), lines 22, 26 and 30, and [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10), with Option B at line 16, carry the corresponding qualifications.

New genuine findings from R1 → R3r: **none**.

The new [L3 step (0.5)](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/lemmas/L3_listR.md:28) supplies the transfer from the pinned core under IMPL-LIST. The field computation follows the final guard decision; store distinctness excludes the specified duplicate-model error. Its additional polynomial computation and storage fit the delivery envelopes. The revised REPORT blocks and DEPS row introduce no substantive mismatch.

- **correct — PASS:** No new wrong or unproved step affecting the claims.
- **strength — PASS:** Revised conclusions respect the data event, branch definitions, evidence bound and delivery premises.
- **faithfulness — PASS:** The three R1 discrepancies are repaired; IMPL-LIST remains explicit and open.
- **lit — PASS:** Changes introduce no unsupported literature comparison; the R1 assessment stands.
- **necessity — PASS:** Changes introduce no unsupported necessity claim.
- **better — PASS:** Stronger candidates remain explicitly dispositioned; no stronger theorem is required for acceptance.

COUNCIL-VERDICT round=R3S manifest=64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890 seat=sol score=9.5 gates=PASS
