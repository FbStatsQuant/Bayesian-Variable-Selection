# W3-DIST — disposition of council round R1 (MANIFEST c7d74e49a9e5a05fb4c9457f6ccf3bb7c83cb85ca00bf49e47d3d8f4a7c8834d)

Written by the lead, 2026-11-16 05:02 CT. Reviews: `reviews/R1_council_astra.md` (score 7.9, gates=FAIL), `reviews/R1_council_opus.md`
(score 8.6, gates=FAIL). **R1 is not a pass.** Each seat failed its gates on one finding of its own, as the brief requires
for any C, S or F finding; **neither seat holds a C finding**; both re-derived the main arguments and found no wrong or
unproved step; both verified Corollary C's reported-model conclusion against the code (HQ's named point).
Per-claim: opus ACCEPT ×20; astra ACCEPT ×17, REJECT ×3 (S, X, X′: "their present unqualified status, not their
conditional mathematical implication").

| finding | kind | what | disposition |
|---|---|---|---|
| R1-astra-01 | F (G4, G6) | the statuses of Lemmas S, X, X′ in REPORT §1 and in their registry blocks lacked "conditional on SOP:TH09", although their proofs use the locked T01 results of [P1] | **ACCEPTED.** Statuses of S, X, X′ — and, for the same reason, V and NEC — now read "PROVED (by this seat), line-checked, conditional on SOP:TH09"; their dependency is the edge `SOP:TH09@hyp`; REPORT §5 says so. SOP:TH09 is not promoted. No theorem, inequality, target clause or constant changes |
| R1-opus-01 | S (G5) | DIST-1 (c), its proof paragraph and TARGET's P3 row let A vary in the gloss "ε_n² of order (1 + s₀^r) log p_raw/n", which reads as a rate linear in A; the radius constant C grows with A | **ACCEPTED**, the seat's repair (a): "for fixed (A, σ*², M, M′), ε_n² is of order (1 + s₀^r) log n/n", with the remark that C depends on A, in `STATEMENT.md` (c) (v1.4.10), `lemmas/DIST12.md` (v0.3, one sentence) and `TARGET.md` §2 row P3. **TC3's text is not edited**; the seat: "TC3 itself … is proved as written. The finding concerns only the gloss on ε_n²". Changelog tag: EQUAL on TC3; WEAKER on a descriptive sentence of consequence (c), not a target clause (A fixed; log p_raw becomes log n). Manager and HQ informed before the repair (2026-11-16); no early checkpoint. Both diff-round seats are asked to confirm by name that TC3's text is unchanged and that the new gloss is exactly what is proved |
| R1-astra-02; opus E-01 … E-06 | E | editorial | `ERRATA.md` (E2 … E8), not applied in the diff round |

Better-theorem proposals (opus): (1) explicit A-dependence of DIST-1; (2) Corollary C with the broader retention
premise as a proved code lemma. Recorded for HQ; not adopted.

Next (PROTOCOL_v4 §5.5): D5 (Sol) on the two repairs → DEPS OK → new manifest → the same two seat models, fresh threads,
each with its own R1 review and the diff since R1's manifest.
