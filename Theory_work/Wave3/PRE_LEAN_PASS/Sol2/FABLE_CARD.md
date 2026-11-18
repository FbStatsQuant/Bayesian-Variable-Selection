# Sol-2 Fable card: READER R4/R5 final text (card live on main)

Sol 6.2: five claims ACCEPT; READER-TEXT REJECT, FIDELITY NOT-FAITHFUL; R5 7.8 gates=FAIL, bound to manifest c867c42e. Snapshot: `origin/theory/PRE-LEAN` 6850c3a5 (reader folder identical to main 668b413f).

**Verdict:** Sol is right on all three points. None touches a recorded statement: the five `W3-READER` claims stand, and every fix is card or reader prose. After the three edits below the reader text should pass.

## Rulings

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **S2-1** Cor 6L ↔ Cor 9C sentence (D121 wording) | AGREE: **it overclaims** | Wording overclaim: the approved sentence dropped a condition that its own source note states | No. Reader remark and card cell only. `W3-D5P` says the Cor 9C consequence is "not claimed here"; `W3-DIST:Cor-C` is unchanged. | See "S2-1 replacement" below; four places. |
| **S2-2** Card row 4.1 omits calibration success | AGREE | Missing qualifier (PoolZ is "almost surely on 𝒜"; row 3.5 has it) | No (`W3-READER:PoolZ` is ACCEPT and unchanged) | `CLAIMS_CARD.md:97`: replace "has expectation $Z$ given the calibration and the data" by "has, on calibration success, expectation $Z$ given the calibration and the data". |
| **S2-3** History bullet quotes `W3-POST2:D` at @1.0.6 | AGREE | Status misquote; I confirmed the registry at 2676e71f has D@1.1.6 | No | `CLAIMS_CARD.md:166`: replace "POST2 C/E/A0/A1/D (@1.0.6: C conditional" by "POST2 C/E/A0/A1 (@1.0.6) and D (@1.1.6) (C conditional". |

### S2-1: why it overclaims

- On Theorem 6's data event 𝒢_n (the mode event intersected with the search events), every run with output has S₀ in its list. That gives π(𝒯) ≥ π(S₀ | y) = 1 − ε_n and nothing more.
- 𝒢_n does not bound ε_n: "S₀ is the unique maximiser" only gives π(S₀) ≥ 1/|Ω|. The rate ε_n = O_P(√(log n/n)) is in probability, not on every point of 𝒢_n. Cor 6L itself adds "when ε_n < ½" where it needs it.
- So Cor 9C's premise π(𝒯) ≥ n^{−cM/2} holds on 𝒢_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}, not on all of 𝒢_n.
- The source note already says exactly this: `W3-D5P/reviews/post_cp3/COR9C_NOTE.md` (N1), "the premise holds on 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}". The short HQ wording compressed that event to "the stated event". The mathematics the consultant agreed is correct; only the compression is wrong.

### S2-1 replacement (exact)

Old: "6L supplies Cor 9C's list-mass premise pathwise (on the stated event); the probability form under Cor 9C's law needs the raw-scale bridge (open)."

New: "6L supplies Cor 9C's list-mass premise pathwise on the part of the stated event where $\pi(S_0\mid y)\ge n^{-cM/2}$ (there the list holds at least that mass); the probability form under Cor 9C's law needs the raw-scale bridge (open)."

Apply in all four places that carry the old sentence:
- `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1443`
- `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:71`
- `Docs/Writing/from_theory/COR6L_9C_NOTE_2026-11-17.md:3` (the "Use this wording (HQ)" line; its "Why" paragraph is already correct)
- `Theory_work/Dept/writing_answers/COR6L_9C_NOTE_2026-11-17.md:3`

I deliberately add no "with probability tending to 1" clause: that note's own "Don'ts" forbid it, because Theorem 6's law and Cor 9C's law differ.

## Reader edits from other cards, to bundle into the same reader touch

- T4 walk N1: second form of (A6) in Theorem 1 (`READER_VERSIONS.md:109-110, 121-122`); wording in `T4.md`.
- T5 R4: the inadmissible-data sentence (`READER_VERSIONS.md:1065-1067`); wording in `T5.md`.
- Optional: T4 walk N5 (what p counts in Theorem 2) and the T4 R2 pointer to Proposition C.
