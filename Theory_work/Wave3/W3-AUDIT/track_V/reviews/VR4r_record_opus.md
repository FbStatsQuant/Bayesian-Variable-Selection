# R4 seat record — opus (HQ carrier; PROTOCOL_v4 §7; CITATION-ONLY; NOT a new review)

Seat record: `reviews/VR4_council_opus.md` (council round R4, score 9.5, all gates PASS), bound to MANIFEST_VR4 (MANIFEST 8a691d2a54c5f13ca164dd0617b68e7bbca893cc3058cfe8d41c0c76d7fe26f0). Opus V-R4 (the last Opus-only diff round, `reviews/VR4_council_opus.md`, 9.5 PASS, V1 ACCEPT) on MANIFEST 8a691d2a…, after V-R1 (opus 8.4 FAIL on F-1, a remark, repaired), V-R2 (9.4 PASS) and V-R3 (9.6 PASS). The seat's claims table names the item by its local id V1; the HQ-DERIVED table maps it to the registry id.. CITATION-ONLY re-freeze as `reviews/MANIFEST_VR4r.txt` (MANIFEST a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248): after R4 only two entries changed: the external input EXT:Theory_work/Wave3/W3-AUDIT/TRACK_B.md (the manager's post-freeze B8 / compliance update for Lemma VIS and the D18 verdict, B8 wording as at theory/W3-AUDIT aab1973c; HQ's Opus faithfulness check of B8: CONFIRMED on TRACK_B.md at that commit; a dossier file the lemma cites in one remark) and V1_VIS/CITECHECK.txt (the ticket's citecheck output, regenerated: the only difference is the short SHA-256 of the cited TRACK_B.md:209-233 block, 70f13b5ab5 → ae91d20f90; all four citations in range); every other entry is byte-identical. TRACK_B.md and track_C/RESULTS.md (EXT inputs cited by the lemma) are brought onto main with this recording (theory/W3-AUDIT aab1973c); they were not on main before.

| id | decision |
|---|---|
| W3-AUDIT-V:VIS | ACCEPT |

The seat's table, verbatim (local id):

- `| V1 | ACCEPT |`

COUNCIL-VERDICT round=R4 manifest=a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248 seat=opus score=9.5 gates=PASS
