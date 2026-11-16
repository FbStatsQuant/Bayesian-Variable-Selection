# W3-DIST — diff check D5 (the two repairs made after council round R1) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D5_sol_diff.md`.** Run no git command that changes state; start no agents; no cluster jobs; any computation small
and `nice`. **Do not write any file outside the repo clone and set no TMPDIR.** Prefer inline computation with no files.
If you need scratch files, put them only in `/home/fb31/Bayesian-Variable-Selection/.rc_tmp/W3-DIST-D5/` (inside the clone,
at its root; never inside the ticket folder, never in `/tmp`) and delete that folder at the end. Never run a command
that asks for an approval: nobody can answer it. The files change no further while you work; hashes at launch are in
`reviews/D5_hashes.txt`: if one does not match, say so and stop. This is a short task (about sixty changed lines).

A council round (R1) on the content frozen as `reviews/MANIFEST_R1.txt` returned two findings: R1-opus-01 (kind S) in
`reviews/R1_council_opus.md` and R1-astra-01 (kind F) in `reviews/R1_council_astra.md`; read those two findings (you need
not read the rest of the reviews). The lead's disposition is `reviews/R1_disposition.md`. The exact diff from the frozen
content to the current files is `reviews/DIFFS_R1_to_R2_draft.patch`.

1. **R1-opus-01** — the gloss on the rate in Theorem DIST-1, consequence (c): `STATEMENT.md` §1 (c); `lemmas/DIST12.md`, the
   paragraph "Dependence on the sparsity" after D.4 (one sentence changed, v0.3); `TARGET.md` §2, row P3.
   (a) Is the new gloss — **"for fixed (A, σ*², M, M′), ε_n² is of order (1 + s₀^r) log n/n"** — exactly what is proved
   (`lemmas/DIST12.md` D.4 with `lemmas/X.md` §0: C = C(A, σ*², M, M′), M₀ ≤ 16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ*²))? Check
   the two facts quoted in the new sentence of `lemmas/DIST12.md`: C_X ≥ 4Λ ≥ 128[34(A + 1) + 2] and C_T = 4[34(A + 7) + 8].
   (b) **Confirm by name that the text of target clause TC3 is unchanged** (`TARGET.md` §5: "Best radius ε_n² = C²M₀ log n/n
   with M₀ = O((1 + s₀^r)(A + 1))") and still proved as written.
   (c) The changelog row 1.4.10 tags the change **EQUAL on TC3; WEAKER on a descriptive sentence of consequence (c), not
   a target clause** (A now fixed; log p_raw becomes log n). CONFIRMED or CONTESTED, with the reason.
   (d) Does any other sentence of `STATEMENT.md`, `TARGET.md`, `REPORT_extra.md` (the source of `REPORT.md`; `@@name@@` fields
   are filled by `mkreport.py`) or `lemmas/DIST12.md` still present the rate as linear in A or as "(1 + s₀^r) log p/n"
   with A free? (Search them.) Is anything else in `lemmas/DIST12.md` changed?
2. **R1-astra-01** — statuses and dependencies: in `mkreport.py` (table of REPORT §1) and `REPORT_extra.md` (registry
   blocks), Lemmas S, V, X, X′ and Proposition NEC now have the status "PROVED (by this seat), line-checked, conditional
   on SOP:TH09" and the dependency `SOP:TH09@hyp`; `REPORT_extra.md` §5 says so. Resolved? Is the condition right for each
   of the five (does each proof file use locked results of [P1]: `work/C_size/S.md`, `work/C_size/V.md`, `lemmas/X.md`
   §0 and §9, `lemmas/NEC.md`)? Is any other claim's status missing a condition it needs by the same rule (H, T, P6,
   B0, B1, B2-core, B2, B3)?
3. Does the patch contain any change that answers neither finding (apart from version lines, changelog and
   review-trail rows, the new file `ERRATA.md` and the version label in `PINS.md`)? Does any hunk alter a theorem display,
   a lemma, a constant or a proof step?

Output (`reviews/D5_sol_diff.md`): first line `D5 diff check — ` followed by the five hashes of `reviews/D5_hashes.txt` as
you recomputed them. Findings with id (D5-xx), severity (CRITICAL / MAJOR / MINOR / NIT), place, the error in full,
minimal repair. Verdict lines: R1-opus-01 RESOLVED / NOT RESOLVED; items 1(a), 1(b) VERIFIED / NOT VERIFIED; the tag of
1(c) CONFIRMED / CONTESTED; item 1(d); R1-astra-01 RESOLVED / NOT RESOLVED; item 3 VERIFIED / NOT VERIFIED;
`lemmas/DIST12.md` as it now stands (DIST-1, DIST-2): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line:
overall verdict. Do not soften findings; say exactly what you could not check.
