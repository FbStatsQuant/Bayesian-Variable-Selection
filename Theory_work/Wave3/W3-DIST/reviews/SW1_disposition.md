# W3-DIST — disposition of the sweep SW1 (Astra; `reviews/SW1_sweep_astra.md`; MANIFEST de9ccec7bb2a07d5cc36fa8a0ab13eb4e78ae697d30b4b3ddcd296fde7ac5957)

Written by the lead, 2026-11-16 04:36 CT. Result of the sweep: **0 CRITICAL, 0 MAJOR, 9 MINOR**. Per-claim table of the
sweep: DIST-1, DIST-2, DIST-3, Theorem A, Theorem B, Corollary C (with its strengthened reported-model conclusion),
Lemmas H, T, S, V, X, X′, P6, Proposition NEC, bridges B0, B1, B2-core, B2 and **TC1–TC9: "proved as stated"**; DIST-C
and B3: "proved after the listed repairs" (SW1-03, SW1-04). **No finding touches a target clause in a WEAKER direction.**
All nine findings are ACCEPTED. The repairs are checked by D4 (`reviews/BRIEF_D4_sol_diff.md`, `reviews/DIFFS_D4.patch`).

| id | kind | finding | repair |
|---|---|---|---|
| SW1-01 | F | STATEMENT's paragraph on the structure of Lemma X's proof, and the consumes row for W3-POST2:A0, A1, described an earlier route (truncated moments; Lemmas S, V as inputs) | rewritten to the adopted route of `lemmas/X.md` (fractional moment of order λ, union-with-S₀ comparison, size tail derived in the file; S and V are companion lemmas). Statement of Lemma X unchanged. Changelog 1.4.9, EQUAL |
| SW1-02 | S | TARGET §1 and ASSUMPTION_MAP grouped (C) with (L₀), suggesting (L₀) can replace (C) in DIST-1 | both maps now carry the distinction that STATEMENT §0 makes: (E) + (C) bound ρ′, used by Lemmas X, X′; (L₀) suffices for DIST-3 and the size tail only |
| SW1-03 | C | DIST-C (C-i): the predictive display read C²t/n also for the (1.2) version | display written as ε_n² + e^{−(c−λ)t} with ε_n² = C²t/n for (1.1), C²tℓ_n/n for (1.2), as in the proof (Remark 6.6). Changelog 1.4.9, **EQUAL on TC8**; the reviewer of D4 confirms or contests. *If contested as WEAKER on TC8: early checkpoint* |
| SW1-04 | F | `work/E_bridges/B3.md` line 11: the copy of (A6)(b) omitted b_n > 0 | inserted (one line; the statement of (A6) already had it). DEPS row B3 STALE until D4 |
| SW1-05 | E | the maps and Card F still presented the fixed-design exponential stretch as open | current-status notes: false by Proposition NEC for the fixed-design core; the in-probability form and a random-design counterexample remain open; N4's "improvable" reading is historical |
| SW1-06 | E | about 60 bare line pins `STATEMENT.md:a-b` inside the proof files point to superseded lines | **new record `PINS.md`**: all 65 such pins (11 files) are pins to STATEMENT v1.3.1, the version the proofs were written against; each is mapped to its object and to the current lines (generated mechanically). The line-checked proof files are **not** edited for an editorial finding (an edit would make checked text unchecked). The council briefs name the record. Refreshing the pins in the files themselves: ERRATA, for the editorial batch |
| SW1-07 | F | seven registry summaries in REPORT out of step with STATEMENT (rate without M₀; DIST-3 scope; DIST-C alternatives and DIST-2 edge; Theorem A's common event; Lemma S's reference assumption; P6's clause (c); a too-broad sentence on point masses) | all seven corrected in `REPORT_extra.md`; P6's registry conclusion now lists (a), (b) only (clause (c) is in the proof file and used inside the proof of DIST-C) |
| SW1-08 | S | `implies` and sharpness metadata overstated the evidence | `implies` edges to W3-POST2:D and W3-POST:Cor-1R removed (kept as comparisons in prose); sharpness: Theorem A's entries for (A3), (A4), (A5) removed (no proved necessity or weakening), the coefficient-cost entry based on an unchecked API attempt removed; (ND) stays NECESSARY-FOR-ROUTE for Lemma X and DIST-1's route only |
| SW1-09 | F | two DEPS descriptions attached historical verdicts to the current hash | the historical versions and hashes are now named |

**Unharvested strength (seven items listed by the sweep).** Weaker forms of (ND) in Lemma X (range of j, power mean);
an outer bound δ/2 in Lemma T; a finite-n form of Lemma S; ranks in Lemma V; the constant c_ψ/4 in B2; DIST-3 without
p ≤ n^A; pathwise thresholds in P6. Disposition: **named open items for HQ, not adopted in this leg**: the statements stay
as fixed at CP1 (PROTOCOL_v4 §5.3: "a stronger theorem is provable" is a better-theorem proposal, not a finding; a
STRONGER change needs HQ's go, §4.2). Recorded in `TARGET.md` §4.

**Second better-theorem review (PROTOCOL_v4 §3.5).** Not run as a separate review: the target clauses have not changed
in substance since CP1 (TC3 and TC8 tags EQUAL, confirmed by reviewers; the one STRONGER change, Corollary C's
reported-model conclusion, has HQ's go and was verified by D3 and by the sweep). The sweep's duty 10 covered
unharvested strength on the same manifest.

## D4 — diff check of the repairs above (Sol; `reviews/D4_sol_diff.md`), written 2026-11-16 04:44 CT
Overall VERIFIED-WITH-AMENDMENTS: 0 CRITICAL, 0 MAJOR, 3 MINOR. SW1-01, SW1-03, SW1-04, SW1-05, SW1-07 (all seven
items), SW1-09 RESOLVED. **Tags CONFIRMED: EQUAL (Lemma X's description); EQUAL on TC8 (the predictive display).**
`work/E_bridges/B3.md` VERIFIED (DEPS row B3 → OK). No change to a theorem, lemma, constant or proof step in the patch.
Three findings on records, all ACCEPTED and repaired with the reviewer's own minimal repair:
- **D4-01** (`TARGET.md` §1, the row on (C) and (L₀)): (L₀) bounds min_ϑ B_{S₀}(ϑ), not the cost of the true coefficients;
  the sentence now names the reference "T = S₀ and ϑ minimising B_{S₀}(ϑ)" and keeps the true pair for (E) + (C).
- **D4-02** (`PINS.md`): six rows were citations of other sources (W3-POST2's lemma file, W1-N1's and W3-POST's
  statements) and are removed; four shorthand pins added; objects and current lines corrected where the generated
  label was only the containing block. 63 rows. The proof files are untouched.
- **D4-03** (REPORT §4): the sentence on (A3), (A5) split: numerical evidence exists for (A3) only.
These three repairs are edits to records (a map, a pin table, a report sentence), not to a statement or a proof; they
are **not re-checked by a further diff check before the R1 freeze** (the council reads them). Recorded in CP3.
