# PRE-LEAN PASS: NEXT_BATCH (staged, PURE-checked, NOT landed; goes out with the re-pins; separate from BATCH_READY_v2)

Sources: manager messages 11-18; the T9 card v2 and addendum (`T9/FABLE_CARD.md`, `origin/dept/theory:.../T9_addendum.md`); the T10 card §1 (`T10/FABLE_CARD.md`). Patches in this folder, applied with `patch -p1` from the repo root. Full-stack check at `-F0` (no fuzz): the BATCH_READY_v2 patches (T8-SA2 included), `MEAS-D/MEAS-D_stage.patch`, and the 12 patches below, **41 patches in the order below, 0 failures**. PURE: round 1 `NEXT_BATCH_PURE_check_opus.md` (8 patches; NB-C3, NB-C4 registry statements corrected, NB-F3 rebuilt stacked), round 2 `NEXT_BATCH_PURE2_check_opus.md` (new and rebuilt patches).

| id | file:line | kind | hashed span touched (recorder rehashes) | apply after |
|---|---|---|---|---|
| NB-C1v2 | `W3-SAMP/STATEMENT.md:36`: theorem-side sentence, potential-pair reading, **no clock clause** (supersedes NB-C1) | wording | W3-SAMP premises span :20-60 (the same 8 claims MEAS-D already rehashes) | `MEAS-D/MEAS-D_stage.patch`. **Lands with or after MEAS-D.** |
| NB-C1r | `W3-SAMP/STATEMENT.md`: new final paragraph after :192, "Remark (actual runs; not part of any claim)": outer probabilities if the clock is not modelled | wording (remark) | none (outside every claim span; no earlier line shifts; +2 lines) | MEAS-D stage, NB-C1v2. **Lands with or after MEAS-D.** |
| NB-C2 | `W3-READER/STATEMENT.md:16` (PoolZ Setting: "the potential pair of the uninterrupted run, erratum E1") | wording | PoolZ span 12-39 (CITATION-ONLY, PoolZ rehash) | none |
| NB-C3 | `W3-READER/lemmas/R4_printed_outputs.md:18` (Inputs: "read as the potential pair by erratum E1") | wording | `W3-READER:R4` span 1-48 (premises :25-29 untouched) | none |
| NB-C4 | `READER_VERSIONS.md:1302` (Thm 10 prose: "in the run taken as if uninterrupted"; theorem side, no clock) | wording | `W3-READER:R1` premise span 1283-1388 (join the R1 bump of BATCH_READY_v2) | none |
| NB-C4r | `READER_VERSIONS.md:1322` (end of line; row 3.5 remark: "Remark (the time guard)": outer probabilities) | wording (remark) | R1 span 1283-1388 (same R1 bump) | none |
| NB-C5log | `READER_VERSIONS.md:1387` (appended to the END of the last bullet of the Thm 10 update log: PL-T9 [E1-TEXT]; §11's line numbers stay fixed) | changelog | R1 span 1283-1388 | none |
| NB-C6err | `ERRATA_W3-SAMP.md` (paragraph appended under E1: "Applied to text 2026-11-18") | changelog | none (errata file is outside every council manifest) | none |
| NB-INT | `W3-READER/STATEMENT.md:32`, PoolZ proof, "(Both sides are finite. … ≤ κ_n.)" (the self-contained v1 (b) sentence; no citation of MEAS-D) | proof completion (Z ≤ κ_n); CORRECTION-ONLY, confirmed by the consultant | PoolZ span 12-39 (PoolZ rehash); the claim sentence is unchanged | none |
| NB-T10-1 | `READER_VERSIONS.md:956`, `CLAIMS_CARD.md:78` ("of size at most q_n + s₀") | wording (overclaim edge case) | none | none |
| NB-T10-2 | `READER_VERSIONS.md:950`, `CLAIMS_CARD.md:78` (bounds fixed, coefficients may vary within them) | wording (understatement) | none | NB-T10-1 |
| NB-F3 | `CLAIMS_CARD.md:76, :97` ("exp of the printed field `log_Z`") | wording | none | `Sol2/Sol2-S2-2`, NB-T10-1, NB-T10-2. **Kept (manager 11-18): the `log_Z` wording was AGREED in the Fable's T9 prep note (F3); not droppable.** |

**Landing rules (manager, 11-18; consultant riders on T9).**
- No row cites MEAS-D before its seats (R3 + Sol-5) pass. NB-C1v2 and NB-C1r are stacked on the MEAS-D stage patch and land WITH or AFTER MEAS-D. No other patch here cites MEAS-D (NB-INT keeps the self-contained sentence).
- The PoolZ citation of MEAS-D (T9 card v2 §A) is NOT staged: it applies only at MEAS-D's recording, if the Fable still wants it after NB-INT.
- The 𝒜 texts follow the addendum's split: theorem-side sentences without a clock clause (NB-C1v2, NB-C2, NB-C3, NB-C4); the clock/outer-probability clause only in remarks (NB-C1r, NB-C4r); changelog lines NB-C5log, NB-C6err.
- Hashed-span summary for the recorder: PoolZ (NB-C2, NB-INT); R4 (NB-C3); R1 (NB-C4, NB-C4r, NB-C5log, with the existing R1 bump); the W3-SAMP premises span (NB-C1v2, with MEAS-D). Not hashed: NB-C1r, NB-C6err, NB-T10-*, NB-F3.

Notes for the recorder / the Fable:
- NB-INT uses c_n, ν, b₀, which are not defined in the PoolZ span (they are in `W3-T03ACC/STATEMENT.md:29-31`; MEAS-D Step 6 writes C_n); the sentence is the card's text, verbatim.
- PURE round 1, NB-C1 note (applies to NB-C1v2): for "intersected with the actual 𝒜" the inclusion that does the work is 𝒜 ⊆ 𝒜° (GW-iv), not only 𝒪 ∩ A ⊆ 𝒪° ∩ A°; the cited GW-iv contains both. The transfer rules cited as `:CAL-C` sit in the T5_CAL "flag" paragraph (:45-54), outside CAL-C's registered span 28-43.
- Recorder-only items already on the list (T12 relabel carrier, row A:IDEAL-W+, Sol-4 S4-3, seat additions, R1 bump) stay in `BATCH_READY_v2.md`.
