# BATCH READY v2 (final): pre-Lean pass CORRECTION-ONLY / CITATION-ONLY batch, for the recorder

Branch `theory/PRE-LEAN` (from origin/main 668b413f). Every item below has its own Opus PURE check in `PRE_LEAN_PASS/<target>/`. Full detail per item: `CORRECTIONS.md`. Nothing is landed; nothing in the registry was edited.

## Count
- **29 items in 28 patch files** (Sol4 A and B travel in `Sol4/Sol4-AB_combined.patch`): T1-1, T3-1, T4-N1, T4-N1b, T4-R1, T5-R1, T5-R2, T5-R3, T5-R4, T5-R4-reader, T7-1, T7-2, T7-MIN-449, T7-MIN-462, T7-MIN-1424, T7-MIN-CARD57, T8-1, T8-2, T8-3, T8-SA2, T9-F1, Sol2 S2-1/S2-2/S2-3, Sol3 S3a-1/S3b-1/S3b-2, Sol4-A, Sol4-B.
- **Deferred:** T4-R4 (`T4/T4-R4_DEFERRED.patch`, applies only if W3-D3 is reopened).
- **Stack check:** all 27 patch files apply one after another (`patch -p1`) to a scratch copy of the 17 files they touch: no failures; no two patches change the same line; every file keeps its line count except `W3-DIST/STATEMENT.md` 499 → 500 (T5-R1's changelog row 1.4.11, tagged WEAKER, at the foot, after every registered span).

## Registered spans touched (claim id → patch), the recorder rehashes and cascades
| claim id (registry) | span edited | patch(es) | kind |
|---|---|---|---|
| `W3-PSHARP:B` | `W3-PSHARP/STATEMENT.md:100` (claim span :90-114) | T1-1 | CORRECTION-ONLY (λ ≥ 0 made explicit) |
| `W3-POST:Thm-1` (inherited by Thm 1′ item 6, no text change there) | `W3-POST/STATEMENT.md:86` (claim span :61-100) | T4-R1 | CORRECTION-ONLY (definedness of item 4) |
| `W3-DIST:DIST-1` | `W3-DIST/STATEMENT.md:78` (claim span :74-91) | T5-R2 | CORRECTION-ONLY (wording) |
| `W3-DIST:DIST-2` | `W3-DIST/STATEMENT.md:96-97` (claim span :93-98) | T5-R1 | CORRECTION-ONLY (wording; changelog row WEAKER) |
| `W3-START2-R:START-R` | `W3-START2-R/STATEMENT.md:237` (claim span :226-240) | T8-2 | CORRECTION-ONLY (qualifier "with s₀ < K and n ≥ 4") |
| `W3-START2-R:TRANSFER` | `W3-START2-R/STATEMENT.md:187` (convention sentence, lines 186-187; claim span :167-188) | T8-SA2 | CORRECTION-ONLY (ϱ_n, R^♯_n, b_n(h) set to 0 off the admissible designs; EQUAL on admissible designs; patch bump like START-R's) |
| `W3-READER:PoolZ` | `W3-READER/STATEMENT.md:26` (claim span :12-39) | T9-F1 | CITATION-ONLY (+ edges below) |
| **premises spans** (edit is inside a registered premises span, not a claim span) | | | |
| `W3-DIST:Thm-A`, `Thm-B`, `Cor-C`, `B0`, `B1`, `B2core`, `B2`, `B3` | `W3-DIST/STATEMENT.md:152` (shared premises span :136-183) | T5-R4 | CORRECTION-ONLY (convention for inadmissible data) |
| `W3-RM2-R:DLV-0`, `RM0-plus`, `RM2-F-plus`, `RM2-R-plus`, `SAND-F-c`, `TL-F-c`, `Ex-Proxy-d`, `Cont-plus` | `W3-RM2-R/STATEMENT.md:81` (premises spans :52-115, :52-93, :71-93) and the A_IDEALW_PLUS carrier (no span); `W2-UNI/lemmas/L5_delivery.md:48` intentionally untouched (pinned historical quote, correct reading; HQ) | T8-1 | CORRECTION-ONLY (ERRATA E2 wording; DLV-0 gets a patch bump and a citation-only cascade) |
| `W3-READER:R1` | `READER_VERSIONS.md:109, 121-122` (95-253), `:295, :301` (258-320), `:449, :462, :470, :481` (444-564) | T4-N1, Sol3 S3b-1/S3b-2, T7-MIN-449/-462, T7-1, T7-2 | CORRECTION-ONLY reader wording: **bumps `W3-READER:R1` to its next patch version, with the CITATION-ONLY cascade into the W3-D2 and W3-D3 pins** |
No registered span is touched by: T3-1, T5-R3, T8-3 and the proof-file half of T8-SA2 (`P6_DISTC.md`, `B3.md`, `R3_RATE.md`, `R4_TRANSFER_COR.md`); Sol3 S3a-1 (`W3-D2/PROOF.md:3`), S3b-1's `W3-D3/REPORT.md:42`; T4-N1b (`READER_VERSIONS.md:824, :885`), T5-R4-reader (:1065-1067), T7-MIN-1424 (:1424), Sol2 S2-1 (`READER_VERSIONS.md:1443`, `CLAIMS_CARD.md:71`), S2-2, S2-3, T7-MIN-CARD57 (`CLAIMS_CARD.md`: in no registry span); Sol4 A+B (`TRACK_B.md`, an EXT dossier); T5-R1's `TARGET.md:30`.

## Manifest / re-freeze consequences (recorder)
- **W3-DIST:** one re-freeze (`MANIFEST_R2r`) for `STATEMENT.md`, `TARGET.md`, `work/D_output/P6_DISTC.md`, `work/E_bridges/B3.md` (T3-1, T5-R1/R2/R3/R4).
- **W3-START2-R:** one re-freeze (`MANIFEST_R2r`, line 20 for `lemmas/R3_RATE.md`, line 21 for `lemmas/R4_TRANSFER_COR.md`) for T8-2, T8-3 and T8-SA2.
- **W3-RM2-R:** T8-1 (`STATEMENT.md:81`) re-freeze; DLV-0 patch bump + citation-only cascade.
- **Track V (CORRECTION-ONLY) and W3-FAMC (CITATION-ONLY):** `TRACK_B.md` is an EXT input of `MANIFEST_VR4r3` and `W3-FAMC/MANIFEST_R5r2` (Sol4 A+B).
- **W3-D2 / W3-D3:** CITATION-ONLY for `W3-D2/PROOF.md:3` (S3a-1) and `W3-D3/REPORT.md:42` (S3b-1), when those tickets are next opened (card: not urgent), plus the R1 cascade into their pins.

## Recorder-only items (nothing to patch here)
1. **T12-RELABEL:** `SOP:TH110` v4 HQ carrier relabel to PROVED-CHECKED ("owner adoption 2026-11-18 + HQ carrier relabel, precedent Prop-LB"); draft in `T9/T12_relabel_carrier_draft.md`.
2. **`A:IDEAL-W+` registry row** (`assumptions.tsv:116`, `notes` column): the OLD/NEW sentence is in the T8-1 row of `CORRECTIONS.md` (same E2 text as the carrier patch).
3. **Sol-4 S4-3:** `W3-AUDIT-V:VIS` status cell cites digest a125ce4d, council cell 1e298254 (`MANIFEST_VR4r3`): re-point the status cell.
4. **T9-F1 edges:** add `W3-SAMP:MR@stmt:MR-b` and `W3-SAMP:CC` to `W3-READER:PoolZ`'s `depends_on`.
5. **R1 bump** (`RECORDER-NOTE-R1`) and ERRATA E2 "resolved in <batch>" note (W3-RM2-R/ERRATA.md:6).
6. Seat additions (`Sol1-SEAT`, `Sol3-D2-SEAT`, `Sol3-D3-SEAT`) to the council cells of `C-DLV:P1-Inventory`, `C-DLV:L2-S3`, `W3-D2:Thm2X/Cor2X`, `W3-D3:B3w/ExSG/Thm2SG` (`manifest.py bind` OK on 12802ac7, f76e9dec, dff18ca9).

## Not in this batch
T9 F2 (MEAS-D, a new W3-SAMP lemma, in the T9 card), T9 F3 (card wording for "printed evidence"), the T4-R4 deferral, the two `COR6L_9C_NOTE` copies and the paper-draft copies (`Docs/Writing`, `Dept/writing_answers`: the manager's), the re-pin rider (T14 and the three stop rows, post-D5P), research notes and history copies of "treated as true".

## For the SUMMARY (owner)
The owner signed the method as FINAL on 2026-11-18. The frozen method is `method-v3.1.1-listpip`, effective once Engineering's guard merges.

## Notes added 2026-11-18 (after the Recorder-2 dry run 330b87b4)
- `Sol2/Sol2-S2-1` is in this batch (the dry run applied it by phrase substitution on the card :71 / RV :1443 lines that D5P v1.1 moved). The D5P (a) stage therefore carries no a-3 edit (same sentence).
- Landing order: this batch → NA_DROP and MEAS-D (CITATION-ONLY re-freezes on the post-batch tree; see `NEXT_BATCH/NEXT_BATCH.md`, last section) → the A re-pin batch with D5Pa rebased onto the post-NA_DROP main, keeping a-1.

