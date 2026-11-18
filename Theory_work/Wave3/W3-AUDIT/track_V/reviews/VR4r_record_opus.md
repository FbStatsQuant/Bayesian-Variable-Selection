# R4 seat record — opus (HQ carrier; PROTOCOL_v4 §7; CORRECTION-ONLY (dossier re-worded after the freeze, see the label paragraph); NOT a new review)

Seat record: `reviews/VR4_council_opus.md` (council round R4, score 9.5, all gates PASS), bound to MANIFEST_VR4 (MANIFEST 8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0). Opus V-R4 (the last Opus-only diff round, `reviews/VR4_council_opus.md`, 9.5 PASS, V1 ACCEPT) on MANIFEST 8a691d2a…, after V-R1 (opus 8.4 FAIL on F-1, a remark, repaired), V-R2 (9.4 PASS) and V-R3 (9.6 PASS). The seat's claims table names the item by its local id V1; the HQ-DERIVED table maps it to the registry id.. CITATION-ONLY re-freeze as `reviews/MANIFEST_VR4r.txt` (MANIFEST a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248): after R4 only two entries changed: the external input EXT:Theory_work/Wave3/W3-AUDIT/TRACK_B.md (the manager's post-freeze B8 / compliance update for Lemma VIS and the D18 verdict, B8 wording as at theory/W3-AUDIT aab1973c, independently checked by an Opus faithfulness review against PROOF.md:96-112, D18_VERDICT.md, STATEMENT.md and auditV2 (HQ condition; FAITHFUL WITH NITS, nits applied, final text CONFIRMED); the lemma's STATEMENT/PROOF are byte-identical; a dossier file the lemma cites in one remark) and V1_VIS/CITECHECK.txt (the ticket's citecheck output, regenerated: the only difference is the short SHA-256 of the cited TRACK_B.md:209-233 block, 70f13b5ab5 → ae91d20f90; all four citations in range); every other entry is byte-identical. TRACK_B.md and track_C/RESULTS.md (EXT inputs cited by the lemma) are brought onto main with this recording (theory/W3-AUDIT aab1973c); they were not on main before.

**Label (HQ, manager message; recorder correction 2026-11-23): CORRECTION-ONLY, not CITATION-ONLY, for TRACK_B.md.** R4 → VR4r: the lemma's STATEMENT/PROOF are byte-identical. The EXT dossier TRACK_B.md B8 (lines 220 and 233) was re-worded by the manager after the freeze to match PROOF.md:107-109 and the HQ-approved scope note (VISIBILITY_SCOPE v2, auditV2 clean). No council seat reviewed that dossier edit. The dossier edit to B8 lines 220/233-234 was checked by an independent Opus faithfulness review against PROOF.md:96-112, D18_VERDICT.md, STATEMENT.md and auditV2 (FAITHFUL WITH NITS; nits applied; final text CONFIRMED); the lemma's STATEMENT/PROOF are byte-identical; Sol V-R1 9.5 carried forward under D99. CITECHECK.txt was regenerated; only the block's short sha changed.

| id | decision |
|---|---|
| W3-AUDIT-V:VIS | ACCEPT |

The seat's table, verbatim (local id):

- `| V1 | ACCEPT |`

COUNCIL-VERDICT round=R4 manifest=a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248 seat=opus score=9.5 gates=PASS
