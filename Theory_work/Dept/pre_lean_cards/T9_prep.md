# T9 preparation note (HELD: not the T9 card)

Input so far: walk `walks/T9_rest.md` on walkD b5a87cd2 (rows 3.5 and 4.1; WALK COMPLETE to recorded inputs; 2 MINOR, 2 NOTE). Still to come: `walks/T9_Thm10.md` (walkB), T9's Astra review and the blind Sol read. The rulings below are provisional until those are in.

## Provisional rulings on `T9_rest.md`

| Row | Provisional ruling | Kind of fix | Exact text |
|---|---|---|---|
| **F1 (MINOR):** PoolZ is about main's core but its proof cites only `W1-N1:Thm-N1`, which is stated for the frozen v2.2.1 core | AGREE | **Citation and registry-edge fix (recorder). Not a statement change:** the claim sentence and its premises stay as they are. The proof text sits inside PoolZ's registry span (`W3-READER/STATEMENT.md:12-39`), so it is a CITATION-ONLY edit with a version bump. | Insert after the first sentence of the proof: "(N1 is stated for the frozen v2.2.1 core. For the core of record the same identity is `W3-SAMP:MR` (MR-b) with h ≡ 1, `W3-SAMP/STATEMENT.md:107-110`; N1's code bridge is carried to main's island by `W3-SAMP:CC`, `lemmas/CC_code_check.md:9-21`.)" Registry: add `W3-SAMP:MR@stmt:MR-b` (and `W3-SAMP:CC`) to PoolZ's depends_on. |
| **F2 (MINOR):** PoolZ's joint-law clause ("Consequently … E[1_𝒜 Ẑ] = E[1_𝒜 Z]") uses measurability of the records in the data; MEAS covers fixed data only | AGREE | **Statement change of the "tacit premise made explicit" kind, confined to the "Consequently" clause.** The main claim (data fixed, a.s. on 𝒜, E[Ẑ \| 𝒞] = Z) and card rows 3.5 and 4.1 are untouched. | In the Claim, replace "Consequently, under the joint law with the H-U/SI idealisation used in the proof," by "Consequently, under the joint law with the H-U/SI idealisation used in the proof, and assuming that the calibration record, the island records and Z are jointly measurable functions of the data and the streams (MEAS extended to the data),". Append to the display: "(an identity in [0, ∞])". |
| **F3 (NOTE):** "printed evidence" should name the field | AGREE | Card wording only | `CLAIMS_CARD.md:76`: "equals the printed evidence" → "equals $\exp$ of the printed field `log_Z` (not `log_Z_list`, row 3.1L)". `:97`: "(equal to the printed evidence on completed runs" → "(equal to $\exp$(`log_Z`), the printed pooled evidence, on completed runs". Row 4.1 also takes the Sol-2 S2-2 insert. |
| **F4 (NOTE, Lean):** N1's premises can only be hypotheses in Lean | AGREE | None | The Lean content is Lemma P (SMC unbiasedness induction on a finite state space), Lemma F (freezing) and linearity. |

## Why F2 is a premise and not a one-line proof step

- N1 discharges MEAS for the island in its code bridge (`W1-N1/lemmas/L1_bridge.md:119-124`, (B-d)): the record is a finite program whose branches compare Borel functions of "(grid values, data constants, u)". The same argument would give measurability in the data.
- But (B-d) covers the island only. The joint-law clause also needs the calibration record to be measurable in the data, and no recorded result audits that. Writing it as proved would assert an unaudited code fact; stating it as a premise is accurate and is what Lean needs anyway.
- Alternative if HQ prefers no premise: extend (B-d) to the data and to the calibration in a recorded code check, then cite it. That is more work than this pass allows.

## Open questions to settle when the other T9 inputs arrive

- The same tacit measurability in the data underlies every joint-law statement of W3-SAMP (for example LT-e, which Theorem 10 uses). Check whether `walks/T9_Thm10.md`, Astra or Sol raises it there; if so, one sentence in W3-SAMP's "Two probability levels" paragraph (`STATEMENT.md:28-36`) would serve all of them, instead of a PoolZ-only edit.
- Whether the card's "given the frozen calibration and the data" (row 3.5) should read "for each fixed data set, given the frozen calibration", to rule out the conditional-expectation reading.
