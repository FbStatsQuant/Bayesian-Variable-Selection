# W3-D3 — F2 form check (Opus 5.5 high; brief `reviews/F2_brief.md`; 2026-11-17)

F2-VERDICT: FORM-ONLY

**(1) Manifest.** `manifest.py verify … MANIFEST_R2g.txt` → `verify: OK MANIFEST c41a5b34…0665f`. R2f → R2g: exactly six
hash lines change (DEPS.tsv, PLAN.md, READER_DELTA.md, REPORT.md, STATEMENT.md, TARGET.md); the #EXTRA list, all 12 EXT:
inputs, API_CARD.md, the three .py tools, lemmas/ASSEMBLY.md, lemmas/B3w.md and all four numerics files are byte-identical.
The six HEAD~1 (057e7b05) files hash to the R2f values, and `git diff HEAD~1 HEAD` on them equals `reviews/F2_form_diff.txt`
byte for byte. (The commit also touches reviews/CITECHECK.txt — outside the manifest; only STATEMENT line numbers ≥147 shift by +1,
all still OK — and LOG.md, not read.)

**(2) Diff.** No change in STATEMENT §§0–3 (claim spans 23–90; header lines 1, 9 and §5, §9 only) or in `lemmas/`. REPORT §6
span hash unchanged (e345cb9a2860d58a; moved 64–91 → 65–92 by the one added §2 line). Mathematical relations unchanged and
still true: NH14's (centred, isotropic) rows are the case Σ = I of (A4) with L a fixed multiple of their ψ₂ constant; (A4) on
single coordinates gives SL Condition 1 for z = x − m_n (convexity: exp{(Σa_i z_i/r)²} ≤ r⁻¹Σ exp{δ²z_i²}, each term bounded
for δ small against L); the converse-failure remark is untouched. Wording: NH14 is named the only anchor and Song–Liang appears
only as a separate factual remark carrying the centring qualifier in STATEMENT §5 (:116–120, bullet :127 labelled "not a
class-1 anchor"), REPORT §2 (:22–25) and §3 card (:37–39), READER_DELTA (:32–37), TARGET class cell (:9, SL not mentioned);
PLAN (:35–36) carries the supersession note.

**Search for remaining anchor sentences** (grep song|liang|SL|anchor|between over every frozen ticket file): none presents SL
Condition 1 as a class-1 anchor. Non-blocking, for the lead's judgement: STATEMENT.md:136–138 (§5 residual bullet: "(A4)
sits between NH14 (identity covariance) and Song–Liang's weaker Condition 1") keeps the "between" bracketing that was
removed from the TARGET class cell; it is a positioning fact, not an anchor claim. PLAN.md:44–46, 50–52 (SL bullet and
"(SG) sits between them" under the old anchors header) are covered by the :35–36 supersession note. TARGET.md:21 (parity row,
"closest published result", qualifier present) is a parity comparison, not a class anchor.

**(3) DEPS.** Recomputed in memory with deps_hand.py's rule (header-located spans, trailing blanks trimmed, sha256[:16]),
on the working tree and on HEAD~1: S:class = STATEMENT.md:113-144, 0bb8d63a49c53d5a (was 113-143, 4da143855dff15dd) —
matches its row; checked_by names this review. The other nine rows have identical sha in both revisions and equal to their
checked_sha (OK); only S:inputs (146-161) and R:registry (65-92) line ranges moved by +1.

**(4) Changelog** row 1.4 (STATEMENT.md:200): tag EQUAL, "outside the claim spans; no mathematical relation changed" —
confirmed by (2).

F2-VERDICT: FORM-ONLY
