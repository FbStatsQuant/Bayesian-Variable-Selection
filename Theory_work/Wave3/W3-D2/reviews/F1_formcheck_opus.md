# W3-D2 — F1 form check (Opus 5.5 high, fresh agent, 2026-11-17)

Scope: `reviews/F1_brief.md`. Read: F1_form_diff.txt, MANIFEST_R2.txt, MANIFEST_R2f.txt, STATEMENT.md (v1.5), DEPS.tsv,
deps_hand.py (read only, not run: it rewrites DEPS.tsv), POST_CP3_EDITORIAL.md, PROOF.md:50-75, READER_VERSIONS.md:20-35 and
:250-280, NOTATION.md:1-40, `origin/main:…/API_AUDIT/auditD2_results/auditD2-s1.md` and `-s2.md`, reviews/D1_council_opus.md:104,
G2_corr.md:24. LOG.md and CHECKPOINT files not read. Worktree HEAD 2ed27576; `git status` clean before and after; no scratch
files left; no `__pycache__` created.

## (1) Is the STATEMENT change form only?

**Yes. The tag "EQUAL (form only)" is right.**

The change: STATEMENT.md:53, inside the (S1) part of the quoted recorded hypotheses, "σ*² > 0 fixed;" became
"σ*² > 0 fixed, α*, β* non-random;". Nothing else in the Cor2X span (:50-58) changed.

It adds no restriction beyond the recorded model:
- (S1) of the recorded statement is "Model of §1 of the notation" (READER_VERSIONS.md:28). NOTATION.md §1 (:15-27) writes
  the model y^r = α*1 + X^rβ* + ε with α*, β* as the true parameters ("Truth", :27). It says probability refers to ε only
  (fixed design, :21) or to the joint law of (X^r, ε) (random design, :24). For the random-design case it uses no law on α*
  or β*, so they are constants.
- The recorded Theorem 2 states its conclusions "under the joint law of design and noise" (READER_VERSIONS.md:271), and
  its (A2) "fixed signals" puts deterministic bounds b_lo ≤ |β*_j| ≤ b_hi on the true coefficients (:266-267). A random β*
  has no place in that statement.
- PROOF P3 (PROOF.md:62-64) already used this reading to put the recorded model into the §0 setting, which requires
  α, β deterministic (STATEMENT.md:19). The proof does not change. The edit only moves into the statement an assumption
  the proof already used, which is what audit items s1-5 and s2-4 asked for.
- "Non-random" is not "fixed". In this file "fixed" means "not depending on n" (e.g. :33, :52-55). "Non-random" still lets
  α*, β* depend on n, as STATEMENT.md:21 and the recorded model allow. So the edit does not quietly add that the
  parameters are constant in n. The only fixed quantities stay s₀, b_lo, b_hi, φ, A, σ*².
- Random α*: the master would allow it (MISR-R :52-53), but the recorded model does not make α* random. So stating α*
  non-random narrows nothing that Cor2X claims to cover. The corollary's scope stays "the recorded Theorem 2 hypotheses".

Placement is correct: the recorded (S1) is where the notation-§1 model enters, so attaching the clause to (S1) matches the
source. Non-blocking nit (optional, for the editorial batch): the bracket `[RV] :263-270` now quotes, as recorded, a
clause whose text is in NOTATION.md §1 (:15-24) via (S1) at RV :28, not in the cited RV lines. A pointer such as
"(S1) = NOTATION §1" would make the quote fully traceable. This is the same kind of fix as POST_CP3_EDITORIAL item 9 and
does not change meaning.

Changelog row 1.5 (STATEMENT.md:126) and header (:1) describe the change correctly. Neither line is in a registered span.

## (2) Are all other lines unchanged, and do the manifest hashes check out?

**Yes.**
- STATEMENT.md v1.4 (`git show b6e9015b:`, sha256 f7a4e75b…, equal to the MANIFEST_R2 row) compared with v1.5, line by
  line: the only differences are lines 1 (header), 53 (the edit) and 126 (the new changelog row). Every other line is
  identical.
- `reviews/F1_form_diff.txt` equals `git diff b6e9015b HEAD` on DEPS.tsv, POST_CP3_EDITORIAL.md and STATEMENT.md. Only the
  file order differs; the hunks are identical.
- `python -B tools/manifest.py verify W3-D2 reviews/MANIFEST_R2f.txt` → `verify: OK MANIFEST 483928c2…48a0`. I also
  recomputed sha256 of all 15 ticket files and all 10 EXT files by hand; every one matches its R2f row.
- Header digests: sha256 of the sorted rows equals the header for both MANIFEST_R2 (f62740c7…) and MANIFEST_R2f
  (483928c2…).
- R2 → R2f row diff: only DEPS.tsv (8db36618… → 7dd16df5…) and STATEMENT.md (f7a4e75b… → 7924d66d…) changed, and
  POST_CP3_EDITORIAL.md was added. The `#EXTRA` lists are identical. The R2 hashes for DEPS.tsv and STATEMENT.md equal
  those files at b6e9015b.
- `git diff --stat 687ce819 HEAD` (the commit that added MANIFEST_R2) over the ticket folder minus reviews/ plus every EXT
  path shows only DEPS.tsv, STATEMENT.md, POST_CP3_EDITORIAL.md, LOG.md and CHECKPOINT_3.md. The last two are excluded from
  manifest coverage by design, and I did not read them.

## (3) Is POST_CP3_EDITORIAL.md a faithful list of the remaining MINOR items?

**Yes, with three small wording nits that do not affect it.**

Coverage: the audit MINOR items are s1-1…s1-7 and s2-1…s2-5. s1-5 and s2-4 (α*, β*) are correctly left out as applied.
Every other item appears:

| audit item | editorial # |
|---|---|
| s1-1, s2-1 | 1 |
| s1-2 | 2 |
| s1-3, s2-3 | 3 |
| s1-4 | 4 |
| s2-2 | 5 |
| s1-6 | 6 |
| s1-7, s2-5 (bullet 4) | 7 |
| s2-5 (bullet 1) | 8 |
| s2-5 (bullet 2) | 9 |
| s2-5 (bullet 3) | 10 |

Items 11-13 have non-audit sources and are labelled as such. Line pointers match the audit text.

It asserts no mathematics. Each item is a proposed wording or citation change, and the reasons it gives ("almost surely
under §0", "conservative slip", "outside its hypotheses by its statement") repeat what the audits say. It is marked
**Not applied**, and the manifest confirms nothing else changed.

Nits (none changes what is listed):
- (a) Item 4 says "on the → ∞ branch". The source is "the L = ∞ branch" (s1-4; G2_corr.md:24, L := liminf ρ_n^{BM}).
  Suggest "L = ∞". Also, "cite it in (E)" is the lead's proposed remedy, not the auditor's: s1-4 notes that the proof
  already cites [R-3] and calls the claim correct. That is acceptable for an editorial list, but it could be marked as
  the lead's proposal.
- (b) Item 3 adopts s2-3's remedy (state the domain, drop the appeal to G2's proof). s1-3 offered that or "flag the appeal".
  The merge is fair.
- (c) The column "in a registered span?" says "no" for PROOF.md lines. Those lines are inside DEPS-registered proof spans
  (P:P0 :7-17, P:P1 :18-53, P:P3 :60-83, P:P5 :84-97), e.g. item 6 (:16, P:P0), item 3 (:49-52, P:P1), item 13 (:62-64,
  P:P3). The column evidently means "in a STATEMENT claim span", which is how the audits use "registered spans" (s1-7).
  Suggest renaming the column so the batch editor re-hashes those DEPS rows when the batch is applied.
- (d) Item 11: the D1 seat note (D1_council_opus.md:104) says the ceiling inequality is at [R1] :36 and the identity at
  :37-38. "→ `:36`" is fine if only the inequality is meant, otherwise use `:36-38`.

## (4) Does the DEPS row S:Cor2X sha match STATEMENT.md:50-58?

**Yes.** sha256 of STATEMENT.md lines 50-58 joined by "\n" (the deps_hand.py convention), first 16 hex = 211f1c45aec1e94d,
which equals both sha and checked_sha in the row. The same span at v1.4 gives 0dc7f82d2dbdcb7f, the old row value, so the
row was updated for exactly this edit. I recomputed every other DEPS row against the current files: sha = checked_sha =
the current hash for all 11 rows, state OK. Only the S:Cor2X row changed (per the diff). Its checked_by now points to this
file.

## Summary

The v1.5 edit puts into the Cor2X statement an assumption that the recorded model (NOTATION §1 via (S1); "under the joint
law of design and noise"; fixed-signal bounds) already contains and that PROOF P3 already used. It adds no restriction,
does not confuse "non-random" with "fixed in n", and changes nothing else. The manifest, diff and DEPS all verify. The
editorial list is faithful, with nits (a)-(d) only.

F1-VERDICT: FORM-ONLY
