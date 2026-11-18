# W-R2 seat record — opus (HQ carrier; PROTOCOL_v4 §7; maps the seat's local ids to the registry ids; NOT a new review)

Seat review: `reviews/WR2_council_opus.md` (W-R2, score 9.3, all gates PASS, bound to MANIFEST_WR2 d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e). Council: W3-AUDIT track A_W (W1 ISL, W2 FRZ: line checks of the steps of W1-N1:B and W1-N1:F at the pin 4676af6), round W-R1 on MANIFEST_WR1 0b8b93aa (sol 9.4 PASS ACCEPT; the seat's review is `reviews/WR1_council_sol.md`) and the diff round W-R2 on MANIFEST_WR2 d4f64540 (opus 9.3 PASS ACCEPT; `reviews/WR2_council_opus.md`) = the lead's binding `R2; MANIFEST d4f64540…; opus=9.3 PASS(reviews/WR2_council_opus.md)` (the registry cell points at the HQ carriers, which map the seats' local ids W1/W2 to the registry ids). Sol W-R1 ACCEPT (9.4, MANIFEST 0b8b93aa) carried forward to d4f64540; the W-R1 → W-R2 diff was reviewed by Opus only (Codex pacing level 1, D91); Sol did not see the final text. The seat's claims table names the items by their local ids W1 (ISL) and W2 (FRZ); the HQ-DERIVED table below maps them to the registry ids (the seat's own table is quoted verbatim below it).

| id | decision |
|---|---|
| W3-AUDIT-AW:ISL | ACCEPT |
| W3-AUDIT-AW:FRZ | ACCEPT |

The seat's table, verbatim:

- `| id | decision |`
- `| W1 (ISL) v1.2 | ACCEPT |`
- `| W2 (FRZ) v1.2 | ACCEPT |`

COUNCIL-VERDICT round=R2 manifest=d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e seat=opus score=9.3 gates=PASS
