# R4 seat record — sol (HQ carrier; PROTOCOL_v4 §7; CITATION-ONLY re-freeze, three core EXT files dropped; NOT a new review)

Seat record: `reviews/R3S_council_sol.md` (score 9.5, all gates PASS). Sol continuation seat, filed as R3S, bound as council round R4. Sol's R1 (MANIFEST 952d9840, `reviews/R1_council_sol.md`) was 7.5, gates=FAIL, LIST-R REJECT on three F findings in derived texts (formal statement and L3 proof valid conditional on IMPL-LIST); all were fixed. The Sol continuation seat, filed as R3S (`reviews/R3S_council_sol.md`, gpt-6.1-sol high, one call, on the lead's MANIFEST_R3r 64a3ec05…), returned LIST-R ACCEPT (conditional on IMPL-LIST), LIST-K ACCEPT, LIST-CODE ACCEPT, R1 F1-F3 RESOLVED, no new finding, score 9.5, gates PASS; its own verdict line reads `round=R3S` (the bind grammar needs round=R<k>), so by HQ's labelling decision (label only) it is bound as council round R4. CITATION-ONLY re-freeze as `reviews/MANIFEST_R3r2.txt` (MANIFEST 0c313200d171ae6c40793fd72d567e4d2647c63ad6ba93b2075e383a809c079e) of the lead's MANIFEST_R3r (MANIFEST 64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890): after R3r (a) the external inputs EXT:Theory_work/Wave3/W3-READER/CLAIMS_CARD.md and READER_VERSIONS.md changed (READER requotes of registry statuses since the W1-N1:B/F discharge, the Prop-LB relabel, the W3-MISR condition-list refreshes and the READER editorial round b8ad21a4, and this recording's replacement of 'pending recording' in card row 3.1L and READER_VERSIONS §11.2 by the recorded statuses; Opus PURE check `reviews/D5P11_requote_check_opus.md`); (b) the three core files EXT:Scripts/SMC_BVS/core/README.md, Scripts/SMC_BVS/core/v3_fit.R, Scripts/SMC_BVS/core/v3_run.R are dropped from this manifest's file list (MANIFEST_R3r records their hashes): core inputs dropped from the frozen set after method v3.1/v3.1.1; the code readings remain AT 4676af6; the re-pin to method-v3.1.1-listpip follows (re-pin ticket); LIST-CODE's status stays 'code reading at core 4676af6'; every other entry is byte-identical. The seats' ACCEPT of LIST-R is conditional on IMPL-LIST; the condition has since been DISCHARGED at `method-v3.1.1-listpip` (main 7100bb3b) by the lead's code reading (`reviews/IMPL_LIST_codeprint.md` §5: 'IMPL-LIST: DISCHARGED at method-v3.1.1-listpip (7100bb3b)'), a premise discharge, not a council round and not part of any seat's verdict; the registry status of LIST-R is therefore the plain PROVED-CHECKED (HQ ruling (i), 2026-11-18). The HQ-DERIVED table below reads the seat's decision cells as exactly ACCEPT; the seat's own table is quoted verbatim under it.

| id | decision |
|---|---|
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |
| W3-D5P:LIST-R | ACCEPT |

The seat's table, verbatim:

- `| id | decision |`
- `|---|---|`
- `| W3-D5P:LIST-R | ACCEPT |`
- `| W3-D5P:LIST-K | ACCEPT |`
- `| W3-D5P:LIST-CODE | ACCEPT |`

COUNCIL-VERDICT round=R4 manifest=0c313200d171ae6c40793fd72d567e4d2647c63ad6ba93b2075e383a809c079e seat=sol score=9.5 gates=PASS
