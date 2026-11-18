# PRE-LEAN PASS: NEXT_BATCH (staged, PURE-checked, NOT landed; goes out with the re-pins; separate from BATCH_READY_v2)

Source: manager message 11-18 and the T9 and T10 Fable cards (`T9/FABLE_CARD.md` (b), (c); `T10/FABLE_CARD.md` §1). Patches in this folder, applied with `patch -p1` from the repo root. Full-stack check: the 29 BATCH_READY_v2 patches (28 files) plus `MEAS-D/MEAS-D_stage.patch` plus the 8 patches below, applied sequentially on a scratch copy in the order below: **0 failures** (the stacked patches are built on their predecessors). Opus PURE check: `NEXT_BATCH_PURE_check_opus.md`.

| id | file:line | kind | registry span? | apply after |
|---|---|---|---|---|
| NB-C1 | `W3-SAMP/STATEMENT.md:36` (append to MEAS-D's pointer sentence: erratum E1, 𝒜 and 𝓒 read as the potential pair; GW-iii, GW-iv) | wording | premises span of the W3-SAMP claims (rehash with MEAS-D's recording) | `MEAS-D/MEAS-D_stage.patch` |
| NB-C2 | `W3-READER/STATEMENT.md:16` (PoolZ Setting: "(the potential pair of the uninterrupted run, `W3-SAMP` erratum E1)") | wording | inside PoolZ's span 12-39: CITATION-ONLY, the recorder rehashes | none |
| NB-C3 | `W3-READER/lemmas/R4_printed_outputs.md:17-18` (R4 Inputs: "read as the potential pair by erratum E1") | wording | not the claim (proof file of R4) | none |
| NB-C4 | `READER_VERSIONS.md:1301-1302` (Thm 10 prose: "in the run taken as if uninterrupted") | wording | no | none |
| NB-INT | `W3-READER/STATEMENT.md`, PoolZ proof, before "taking expectations": "(Both sides are finite. … ≤ κ_n.)" | proof completion (Z ≤ κ_n) | inside PoolZ's span 12-39: CITATION-ONLY, the recorder rehashes; the claim sentence is unchanged | none (T9-F1 edits line 26, this one line 35) |
| NB-T10-1 | `READER_VERSIONS.md:956`, `CLAIMS_CARD.md:78` ("of size at most q_n + s₀") | wording (overclaim edge case) | no | none |
| NB-T10-2 | `READER_VERSIONS.md:950-951`, `CLAIMS_CARD.md:78` (bounds fixed in n, coefficients may vary within them) | wording (understatement) | no | NB-T10-1 (same card line) |
| NB-F3 | `CLAIMS_CARD.md:76`, `:97` ("exp of the printed field `log_Z`") | wording | no | `Sol2/Sol2-S2-2_correction.patch` (same line :97). **Not in the manager's list; in the T9 card, row F3. Drop if not wanted.** |

**Landing rules (manager, 11-18; consultant riders on T9):**
- **No row cites MEAS-D before its seats (R3 + Sol-5) pass.** Items that mention or depend on MEAS-D land WITH or AFTER MEAS-D, never before: **NB-C1** (appended to MEAS-D's pointer sentence; stacked on `MEAS-D/MEAS-D_stage.patch`). NB-INT deliberately cites nothing: PoolZ keeps the self-contained Z-bound sentence (T9 card v1 (b)); the Z bound is confirmed, CORRECTION-ONLY.
- **HELD for the Fable's addendum:** NB-C1 to NB-C4 (the 𝒜 texts). The addendum splits text C into a theorem sentence plus a remark (outer probabilities if the clock is not modelled) with an erratum-E1 changelog line, and adds row 3.5's h-identity integrability sentence; both are staged when the manager passes them on, and NB-C1..C4 are rebuilt from it.
- NB-T10-1, NB-T10-2 (T10 card column (c)), NB-INT and NB-F3 do not mention MEAS-D.

Notes for the recorder / the Fable:
- NB-INT uses c_n, ν, b₀, which are not defined in the PoolZ span (they are in `W3-T03ACC/STATEMENT.md:30-31`); the sentence is the card's text, verbatim.
- NB-C1 and NB-C2 are the only two that change a hashed span; both are wording-only (E1 already records the reading).
- Recorder-only items already on the list (T12 relabel carrier, row A:IDEAL-W+, Sol-4 S4-3, seat additions, R1 bump) stay in `BATCH_READY_v2.md`.
