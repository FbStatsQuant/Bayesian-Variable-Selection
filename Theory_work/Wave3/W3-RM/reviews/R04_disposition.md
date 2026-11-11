# R04 disposition (cross-family check of SAND-R and SAND-R', Claude Opus 5.5 high on claudeAgent)

Reviewer reply verbatim: `reviews/R04_SANDR_check_opus.md` (scratch numerics in `reviews/R04_scratch/`).
Verdicts: `lemmas/L3_SANDR.md` VERIFIED-WITH-AMENDMENTS (no FATAL/MAJOR); `lemmas/L3b_rate.md` VERIFIED.
The reviewer opened every source of the delta chain and found no unsupplied design property (no hidden use of the
Markov property, an upper spectral bound, large-set floors, remote-remote smallness or block conditions); the scale
treatment is correct in every step involving Y; both example classes satisfy the abstract hypotheses.

| # | sev. | finding | disposition |
|---|---|---|---|
| F1 | MINOR | "never condition on the scales" is literally false for the spherical step (which correctly conditions on (W_D, eps)) | wording fixed in L3_SANDR sections 3, 5 and in the STATEMENT bridge note |
| F2 | MINOR | quantifier "U not containing l", membership of U, U+l in the score family | fixed |
| F3 | MINOR | the Q u {l} floor is a surplus hypothesis of SAND-R | recorded in L3_SANDR section 1 and the STATEMENT note; (FL-R) keeps the floor because NA/TL need it |
| F4 | NIT | range of (2); p = 1 vacuous | note added |
| F5 | NIT | good/bad block split not needed | no change (harmless) |
| F6 | NIT | optional: any leak rate o(sqrt(log n/n)) suffices for this route | recorded in SHARPNESS.md as a free weakening not adopted (statement keeps C_L n^(-1/2)) |
| F7 | NIT | citation G6:203-215 | fixed |
| F8 | NIT | optional: r_n = o((log n/n)^(1/4)) would suffice | recorded in SHARPNESS.md; statement keeps the checked rate r_n = o((n log n)^(-1/4)) |
| F9 | NIT | SHARPNESS.md did not exist yet | file created |
| F10 | NIT | L3b derivation re-derived, correct | none |
