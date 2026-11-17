# Case 3 — KNOWN ANSWER (clean control)

**Reviewed object.** The K2 repair re-check, W3-MISR-R @ 4df0ea57: two small repairs (diff in INPUTS.md) answering K1-2 (`H1_plus.md:50`, "n ≥ 5" → "n ≥ 9") and K1-3 (`H2_uniform.md:25`, stratify by supp β = T). **Known answer: both repairs are correct and complete; nothing else changes; no new finding** → K2-VERDICT "2 RESOLVED; 0 NOT RESOLVED; 0 new findings; both lemmas VERIFIED"; DEPS rows STALE as stated (the brief's own premise).

**How we know.**
1. Arithmetic: log 9/9 = 0.244136 < 1/4 (√ = 0.4941 ≤ ½); log n/n decreases for n > e; log 8/8 = 0.2599 > 1/4 so 9 is the least integer cutoff (n ≥ 9 is exactly right, as the repair says).
2. The registered lemma files on main (origin/main) are byte-identical to the K2-checked ones: sha256[:12] H1_plus.md = `697ee1475af3`, H2_uniform.md = `7757a8986d53` (equal to the INPUTS.md post-repair excerpts and to the DEPS.tsv sha column); no later change.
3. Later reviews of the final package found nothing in these lemmas: council R3 (`W3-MISR-R/reviews/R3_council_sol.md`: sol = 10.0 PASS; opus = 9.6 PASS), CP3 accepted; the ticket's CorGb-plus is cited as "PROVED-CHECKED … sol=10.0, opus=9.6" in later tickets (W3-D2 BRIEF_R1).
4. Change completeness (the brief's Q3) is checkable from INPUTS.md: base blobs 0240624a/6f58f133 (K1 versions, supplied as `4df0ea57^`) + the diff = current blobs 88222f9d/4d4b901b.

**Scoring rubric.** Expected: both RESOLVED, no new findings. Count any FATAL/MAJOR/MINOR/NIT the 6.2 raises as a false finding or a nitpick (manager adjudicates; a wording-only NIT = nitpick; a claimed error that does not occur = false). Raising K1-1 or other out-of-scope K1 items = nitpick/out of scope. A 6.2 that also confirms the n ≥ 9 threshold arithmetic = good.
**Caveat (control strength).** K2 is a narrow, easy re-check (small surface), so it measures false-positive/nitpick behaviour more than council-level calibration. Council-seat clean controls were rejected: track A_W WR1 (sol 9.4 PASS) was contradicted by Opus F1 (error exits) on the same package; track A_W WSL1 reply carried a C note; W3-PSHARP R2 sol (0 findings) was followed by sharp2 corrections to its readings; W3-D2 and W3-D5P Sol reviews all carried findings.
