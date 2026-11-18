# W3-DIST — diff check D4 (the repairs made after the sweep SW1) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D4_sol_diff.md`.** Run no git command that changes state; start no agents; no cluster jobs; any computation small
and `nice`. **Do not write any file outside the repo clone and set no TMPDIR.** Prefer inline computation with no files.
If you need scratch files, put them only in `/home/fb31/Bayesian-Variable-Selection/.rc_tmp/W3-DIST-D4/` (inside the clone,
at its root; never inside the ticket folder, never in `/tmp`) and delete that folder at the end. Never run a command
that asks for an approval: nobody can answer it. The files change no further while you work; hashes at launch are in
`reviews/D4_hashes.txt`: if one does not match, say so and stop.

An exhaustive sweep (`reviews/SW1_sweep_astra.md`: 0 CRITICAL, 0 MAJOR, 9 MINOR, findings SW1-01 … SW1-09) was run on the
content frozen as `reviews/MANIFEST_SW1.txt`. The lead then made local repairs. The exact diff from the frozen content to
the current files is `reviews/DIFFS_D4.patch` (eight blocks). Read the nine findings, the patch, and as much of the
surrounding text as you need. Decide, finding by finding, whether the repair resolves it and whether the amended text
is correct as it now reads. Do not re-review unchanged, already checked text.

1. **SW1-01** — `STATEMENT.md` §3, Lemma X: the paragraph on the structure of the proof, and the consumes row for
   W3-POST2:A0, A1 (§4). Check the new description against the adopted proof `lemmas/X.md` §1–§7 (the moment order λ, the
   union-with-S₀ comparison and its multiplicity, the size tail derived in the file, no dependence on `work/C_size/`).
   Tag to confirm: EQUAL (a description; the statement of Lemma X is unchanged).
2. **SW1-03** — `STATEMENT.md`, Theorem DIST-C (C-i): the predictive display now reads ε_n² + e^{−(c−λ)t} with ε_n² = C²t/n
   for (1.1) and C²tℓ_n/n for (1.2). Check against `work/D_output/P6_DISTC.md` §6 (C-i) and Remark 6.6. **Tag to confirm or
   contest: EQUAL on TC8** (`TARGET.md` §5: "(C-0) and the deterministic parts of (C-i), (C-iii); every delivery statement
   jointly with {completed} and under its named premise"). If contested, say whether you read it as WEAKER on TC8.
3. **SW1-04** — `work/E_bridges/B3.md` line 11: "b_n > 0" inserted in the copy of (A6)(b). Resolved? Does the rest of the
   file (Step 5 in particular) read correctly with it, and is anything else in the file changed?
4. **SW1-02, SW1-05** — `TARGET.md` §1–§2, §4, `ASSUMPTION_MAP.md`, `API_CARDS.md` Card F: the distinction between the
   coefficient-cost condition (C) (with (E): the bound on ρ′ used by Lemmas X, X′) and the weaker (L₀); the status of the
   stretch item S-FIT after Proposition NEC. Is each amended sentence accurate against `STATEMENT.md` §0, §1 (stretch
   items), §3 (Proposition NEC) and `lemmas/NEC.md` §0? Is anything claimed about NEC beyond its fixed-design, in-sample
   scope? `TARGET.md` §5 (TC1–TC9) and §6 (the reader block) must be untouched: confirm, and confirm that the reader
   block of `TARGET.md` §6 is still identical to `STATEMENT.md` §1R (Setup to Corollary C).
5. **SW1-07, SW1-08** — `REPORT_extra.md` (the source of `REPORT.md`; `@@name@@` fields are filled with STATEMENT line
   ranges, statuses and line numbers by `mkreport.py`): the registry blocks of DIST-1, DIST-2, DIST-3, DIST-C, Thm-A, S,
   P6, B2 and the sections "Relations, strength, sharpness" and "Inputs and assurance". For each of the seven items of
   SW1-07 and the three of SW1-08: resolved? Does every amended conclusion, rate, scope, assumption, dependency and
   sharpness entry say no more than `STATEMENT.md` and the proofs support? (Removed `implies:` and `sharpness:` entries
   are intended.)
6. **SW1-09** — `DEPS.tsv`: the two descriptions now name the historical versions and hashes. Check them against the first
   lines of `reviews/L6_sol_DIST12.md` and `reviews/L7_sol_NEC.md`.
7. **SW1-06** — the new record `PINS.md`. The lead chose not to edit the line-checked proof files; instead this record
   declares the bare `STATEMENT.md:a-b` pins inside the proof files to be historical pins to STATEMENT v1.3.1 (snapshot
   commit `f54bd6f` on branch `theory/W3-DIST`; `git show f54bd6f:Theory_work/Wave3/W3-DIST/STATEMENT.md` is read-only and
   allowed) and maps each to its object and to the current lines. Spot-check at least twelve rows, among them the three
   examples named in SW1-06 (B3 → (TR₀), the DIST-3 events, the cutoff; ASSEMBLY → (1.1), (1.2); B0 → the posterior):
   does the pin, read in v1.3.1, land on the object the citing sentence names, and are the current lines right? Is any
   bare pin in those eleven files missing from the table, or is any pin NOT a v1.3.1 pin (for example in an amendment
   written later)?
8. Does the patch contain any change that answers none of SW1-01 … SW1-09 (apart from version lines, the changelog rows
   1.4.9 and the review-trail rows)? Does any hunk alter a theorem, a lemma, a constant or a proof step?

Output (`reviews/D4_sol_diff.md`): first line `D4 diff check — ` followed by the eight hashes of `reviews/D4_hashes.txt` as
you recomputed them. Findings with id (D4-xx), severity (CRITICAL / MAJOR / MINOR / NIT), place, the error in full,
minimal repair. Verdict lines: per sweep finding SW1-01 … SW1-09, RESOLVED / NOT RESOLVED; the two tags (items 1, 2),
CONFIRMED / CONTESTED; `work/E_bridges/B3.md` as it now stands, VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED; item 8,
VERIFIED / NOT VERIFIED. Final line: overall verdict. Do not soften findings; say exactly what you could not check.
