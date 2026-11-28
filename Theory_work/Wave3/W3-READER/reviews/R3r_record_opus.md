# R3 seat record — opus (HQ carrier; PROTOCOL_v4 §7; CITATION-ONLY; NOT a new review)

Seat reviews: `reviews/R2_council_opus.md` (council round R2, score 9.3, all gates PASS, FIDELITY FAITHFUL; per-claim table below; MANIFEST 3af23c3572d21511fe59fe7a610991eb2b92858e0309a8ee7ac1e8ff43636a4b, bind `reviews/BIND_R2.txt`) and `reviews/R3_council_opus.md` (round R3, the last round: diff-only confirmation of R2 -> R3, score 9.4, all gates PASS; it accepts every tagged change, R4's R2-O7 included, and keeps the R2 acceptance of unchanged content; MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, bind `reviews/BIND_R3.txt`). R3 has no per-claim table; the per-claim decisions are the seat's R2 table, copied verbatim. CITATION-ONLY re-freeze (form fix, HQ item A, H5 card 15): after round R3 only CLAIMS_CARD.md changed, at lines 73 and 74 (rows 3.5 and 3.6): the author label "PROVED (by this seat, unchecked)" quoted for W3-READER:PoolZ and "NEW assembly R4 (unchecked)" are replaced by the registry status recorded at CP3 (verbatim, digest abbreviated as in the card). No statement, proof, bridge or conclusion changes; DEPS.tsv is unchanged (its CARD sha is the reviewed card's). Dropped from the file list (HQ option): EXT:Theory_work/INFRA/registry/claims.tsv (the registry file, frozen as the source of the verbatim status quotes; every registry write changes it, so a manifest that lists it cannot verify after the CP3 ingest; the quotes stay checked against the registry by the recorder at ingest). This carrier binds the seat's R3 outcome to `reviews/MANIFEST_R3r.txt` (MANIFEST de0552c9b596e5ea1138aef104e133aafa6509c01e034f3af77ccb821ec8c8b3), which differs from MANIFEST_R3 only in that file.

| id | decision |
|---|---|
| `W3-READER:PoolZ` | ACCEPT |
| `W3-READER:R1` | ACCEPT |
| `W3-READER:R2` | ACCEPT |
| `W3-READER:R3` | ACCEPT |
| `W3-READER:R4` | ACCEPT |

The seat's R2 table also accepts the reader versions; they are not registry claims (REPORT.md: "The reader-version corollaries ... are not proposed as separate rows here; HQ decides"), so their rows are quoted verbatim below the table (form only: a checkpoint carries registry claim ids only):

- `| `RV/thm1` (Theorems 1, 1′; row 1.1 Form A) | ACCEPT |`
- `| `RV/thm2` | ACCEPT |`
- `| `RV/thm3` | ACCEPT |`
- `| `RV/thm4` | ACCEPT |`
- `| `RV/thm5` | ACCEPT |`
- `| `RV/thm6` | ACCEPT |`
- `| `RV/thm7` | ACCEPT |`
- `| `RV/thm8` (Theorems 8, 8′; row 3.7 form (a)) | ACCEPT |`
- `| `RV/thm9` (9, 9B, 9C) | ACCEPT |`
- `| `RV/thm10` (and remark row 3.5) | ACCEPT |`

Seat note moved out of the decision cell (form only; INFRA R06 reads exactly `ACCEPT`), verbatim; the qualifier is the claim's own registered scope (`lemmas/R3_delivery_assembly.md:3-6` [R1-F2]: historical, the hypotheses of `W3-RM2:RM2-R` / `RM2-F`):

- `W3-READER:R3`: ACCEPT (as the historical lemma it now is: target restricted to the hypotheses of `W3-RM2:RM2-R` / `RM2-F`)

COUNCIL-VERDICT round=R3 manifest=de0552c9b596e5ea1138aef104e133aafa6509c01e034f3af77ccb821ec8c8b3 seat=opus score=9.4 gates=PASS
