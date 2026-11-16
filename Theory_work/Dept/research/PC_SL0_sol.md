# PC review — C-PACK:SL0

Read-only review of fetched `origin/main`, initially `637c4d284d5d44e94ab1a9776a89353821c51bda`, revalidated at `5751f76e1fa913e1b0f9451df52d8dee2df1ddf4` (2026-11-16). The C-PACK tree is identical at both commits; intervening registry updates leave SL0's statement location unchanged. This reviewer changed no acceptance record or registry and wrote only this file.

**Answer: yes.** SL0's statement and proof are the C1-reviewed ones up to editorial changes. This conclusion is authenticated by the I4 snapshot hash, independently of the package-history limitation below.

## Snapshot provenance

For each of the ten paths I walked `git log origin/main --format=%H -- <file>` and compared SHA-256 of `git show <commit>:<path>` with the supplied manifest. Every path has only introducing commit `3b1d79555886e58ce9d6455fec22ecf6fdb0d1c2` in ordinary main path history. Full-history traversal additionally visits merge `4676af6918ee878821f651c02d5dd14dd8da376e`; its ten blobs equal those in the introducing commit and current main. Only STATEMENT and METHOD_REQUIREMENTS match their raw manifest hashes. Neither all-ref/full-history traversal nor a read-only search of all available blob objects supplied the missing reviewed versions, including LF counterparts of the missing snapshots.

The literal raw-byte comparison finds **eight mismatches**, not five. Three are explained exactly by CRLF → LF conversion: restoring CRLF to the current P_GEN_LHiid, P_SEL_L6d and P_L8_certificate blobs reproduces their manifest hashes. Five files have additional content changes. **No matching reviewed commit exists in the available history for those eight raw hashes.** In particular, `3b1d795` contains post-council bytes for the five content-changed files; it must not be reported as their snapshot-matching reviewed commit.

I recovered complete I4, I2 and P_e4 snapshot text in memory by reversing council-documented edits and restoring CRLF; each reconstruction matches its complete manifest SHA-256. No reconstructed source files were written. I could not recover hash-matching SONG_LIANG_MAP or I1 text. Their changes below are documented by the council records, but a complete authenticated hunk inventory for those two files is unavailable. This limits the requested package-wide audit; the complete I4 comparison conclusively answers the SL0-only question.

Paths below are relative to `Theory_work/Wave1C/C-PACK/`. Coordinates use LF-normalised text. CRLF → LF is EDITORIAL for each of the eight raw mismatches.

| file | reviewed commit | changed hunks | class | note |
|---|---|---|---|---|
| STATEMENT.md | `3b1d79555886e58ce9d6455fec22ecf6fdb0d1c2` | 0 | EDITORIAL (no change) | Raw snapshot hash matches; full-history merge also matches. |
| METHOD_REQUIREMENTS.md | `3b1d79555886e58ce9d6455fec22ecf6fdb0d1c2` | 0 | EDITORIAL (no change) | Raw snapshot hash matches; MR1 already mentions replacements. |
| SONG_LIANG_MAP.md | NONE — raw hash absent | Reading paragraph, current :30–32, documented; CRLF → LF | EDITORIAL | Clarifies selection results versus selection counterparts of Thm 1–2. Full reviewed text/diff unavailable. |
| lemmas/I1_e4_replacement.md | NONE — raw hash absent | Header, current :5, documented | EDITORIAL | Re-check/council status trail; old header not fully recovered. |
| lemmas/I1_e4_replacement.md | NONE — raw hash absent | P7 and G9/G10/S1 rows, current :28, :37–39, documented | EDITORIAL | Adds occurrence/citation inventory for existing contracts; no additional deduction. |
| lemmas/I1_e4_replacement.md | NONE — raw hash absent | e4′(i), current :145–147, documented | SUBSTANTIVE (outside SL0) | Allows MR1 replacement routines and substitutes MR1's unique-maximiser property for the original proof input. |
| lemmas/I1_e4_replacement.md | NONE — raw hash absent | CRLF → LF; full content diff unavailable | EDITORIAL (newlines) | Documented regions above are not a certified exhaustive hunk inventory. |
| lemmas/I2_LHiid_unconditional.md | NONE — raw hash absent; exact text reconstructed | H1 `@@ -77,6 +77,8 @@`; CRLF → LF | EDITORIAL | Adds practical-onset warning to an already asymptotic claim; no hypothesis, conclusion or proof step changes. |
| lemmas/I2_LHiid_unconditional.md | NONE — raw hash absent; exact text reconstructed | H2 `@@ -87,5 +89,5 @@` | EDITORIAL | Corrects status attribution to GEN L6(b) versus its R07 review. |
| lemmas/I4_SL_corollaries.md | NONE — raw hash absent; exact text reconstructed | H1 `@@ -3,7 +3,7 @@`; CRLF → LF | EDITORIAL | Only review-status prose at :6 changes; all text from §0 onward is identical. |
| patches/P_e4_consumers.md | NONE — raw hash absent; exact text reconstructed | H1 `@@ -50,3 +50,11 @@`; CRLF → LF | EDITORIAL | Adds report/premise/measurability pointers for contracts already present in e4′(ii)–(iii). |
| patches/P_GEN_LHiid.md | NONE — raw hash absent; CRLF encoding matches | 0 content hunks; CRLF → LF | EDITORIAL | Entire current text equals snapshot after newline normalisation. |
| patches/P_SEL_L6d.md | NONE — raw hash absent; CRLF encoding matches | 0 content hunks; CRLF → LF | EDITORIAL | Entire current text equals snapshot after newline normalisation. |
| patches/P_L8_certificate.md | NONE — raw hash absent; CRLF encoding matches | 0 content hunks; CRLF → LF | EDITORIAL | Entire current text equals snapshot after newline normalisation. |

## SL0 specifically

The registry's C-PACK:SL0 row (claims.tsv:71) points to I4:20–30 for the statement and :11–18 for its conventions; the proof is I4:32–37. Replacing the current header's `v2 repairs re-read by R38 (blind mid-point, CONTINUE) and R39 (sweep, fixes applied); council C1 passed (Sol 9.0, Opus 8.7)` with `v2 repairs pending re-check` and restoring CRLF recovers the full I4 snapshot, with SHA-256 exactly `bc4ecf63536adbb5477fabcb020807bf42c032346002349b028d766972fa3dd3`. The finite model space, zero extension, empty-max convention, summary-domain convention, all six clauses, and every proof step are therefore unchanged. SL0 uses the off-truth mass bound, oscillation identity, threshold/unique-mode inequalities and feasible two-point swap; it does not use I1, I2, e4′, GEN's asymptotic arguments or Song–Liang's theorems. Its D0 nonattainment caveat uses strict positivity, retained by the current cited D0 score/prior (SoP 04_theory.tex:70–73: positive definite regularised Gram matrices, positive scale and positive prior weights). No changed premise in this package enters SL0's proof.

## Authenticated snapshot-to-main diffs

These are exact content diffs after newline normalisation, rather than git-commit diffs: no available commit contains these raw reviewed blobs. For every old side below, restoring CRLF passes the supplied manifest SHA-256 check. Every hunk is individually classified in the table.

### lemmas/I4_SL_corollaries.md

```diff
--- C1 snapshot (LF-normalised)/lemmas/I4_SL_corollaries.md
+++ origin/main/lemmas/I4_SL_corollaries.md
@@ -3,7 +3,7 @@
 Author: C-PACK lead (Claude Opus 5.5). **v2** after cross-family check R34 (`reviews/R34_item4_check_sol.md`, verdict ERROR
 as written: 0 FATAL / 2 MAJOR / 7 MINOR; SL0(i)–(v), SL1, SL1′, SL2 independently re-derived; the error was SL0(vi)'s
 D0-attainment claim). All findings applied (disposition `reviews/R34_disposition.md`). Status of each statement:
-PROVED (by this seat, unchecked), R34-checked as listed in the disposition; v2 repairs pending re-check. Input statuses
+PROVED (by this seat, unchecked), R34-checked as listed in the disposition; v2 repairs re-read by R38 (blind mid-point, CONTINUE) and R39 (sweep, fixes applied); council C1 passed (Sol 9.0, Opus 8.7). Input statuses
 are quoted in §4; nothing is upgraded. Aliases: `SoP/` = `Theory_work/State_of_Project/sections/`; `W1/` = `Theory_work/Wave1/`;
 `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.
 
```

### lemmas/I2_LHiid_unconditional.md

```diff
--- C1 snapshot (LF-normalised)/lemmas/I2_LHiid_unconditional.md
+++ origin/main/lemmas/I2_LHiid_unconditional.md
@@ -77,6 +77,8 @@
 minimum with p only shrinks the family. L′_nδ_n = O((log n)^{3/2} n^{−1/2}) → 0, so the onset is eventually met. The two
 remaining parts of 𝒞_n (‖μ‖²/n ≤ M, θ\*²_min ≥ b₀) are SLLN statements on the finitely many fixed signal columns, as
 in GEN, unaffected. ∎
+*Finite-n remark (council C1-opus #3).* The onset L′_nδ_n ≤ λ₀/2 is far beyond practical n (≈ 10¹⁰ for g = 10, c = 1,
+ρ = .7, ψ̄ = .5, A = 1, council estimate); (ii) is an asymptotic statement only.
 
 **Rate difference, (C5)(b).** GEN's parenthesis "max|r̂ − Σ| ≤ C√(log p/n)" is replaced by "≤ δ_n = O(√(log n/n))"; for
 slowly growing p this is a weaker rate than written, but (C5)(b) uses it only through "operator error … = o(1)", which
@@ -87,5 +89,5 @@
 ## 5. Status change proposed (HQ's call; nothing upgraded here)
 GEN (C5)(b): "conditional on W7-PART Theorem B (candidate) and [CONC]" → "uses Theorem R as repaired and XF-verified in
 W1-PXN (R14, R19, R21; route (R′) R19) and [CONC′] (W1-PXN Lemma CR, XF VERIFIED R19); no candidate input". The
-remaining dependencies of (C5)(b) are GEN's own (R07 VERIFIED-WITH-AMENDMENTS) and the W1-PXN items, whose ticket-level
+remaining dependencies of (C5)(b) are GEN's own L6(b) argument (status 'PROVED (by this seat, unchecked)'; R07 recorded (a)–(c) VERIFIED-WITH-AMENDMENTS) and the W1-PXN items, whose ticket-level
 status is "PROVED-CHECKED" (W1-PXN REPORT §1; Wave-1 result, not adopted by HQ).
```

### patches/P_e4_consumers.md

```diff
--- C1 snapshot (LF-normalised)/patches/P_e4_consumers.md
+++ origin/main/patches/P_e4_consumers.md
@@ -50,3 +50,11 @@
     this as a C-PACK addendum.
 These instructions supplement, rather than remove, P-e4's retained EX-A, H1, H3–H4, OP-LS0 and complete-scan contracts.
 Note: on tied (and possibly truncated) instances e4′ specifies the coded output and does not assert the prescribed lex choice.
+
+## Additions after council C1 (opus non-blocking #1; `reviews/C1_council_opus.md`)
+17. `W1/W1-GEN/REPORT.md:16,30,97` and `W1/W1-PXN/REPORT.md:47`: read e4 as e4′ (C-PACK I1 §4); keep the historical verdict
+    text. (`W1/W1-PXN/lemmas/ERRATA.md:17` likewise: historical, append a pointer to Lemma UM and I1 §1.1.)
+18. `SoP/04_theory.tex:84`: after the e4 definition add "C-PACK addendum: for the consistency cards, e4 may be replaced by
+    e4′ (C-PACK I1 §4); N3 status unchanged."
+19. `W1/W1-GEN/lemmas/L5_assembly.md:69`: the start-mode part of "the deterministic tie rules" is the coded centre of e4′ (ii),
+    a deterministic measurable data function on every branch.
```

## Documented changes without authenticated full diffs

**SONG_LIANG_MAP — EDITORIAL (Opus #7).** The council quotes the old phrase “Thm 1–2 at the selection level” and requests distinguishing selection-level results from selection counterparts of Thm 1–2. The current Reading paragraph says:

> Every correctly specified Song–Liang selection-level result (Thm 3, ξ_q, the MAP description of Thm S), and the selection-level counterparts of Thm 1–2, has an analog for the exact posterior that is a one-line consequence of 1 − π(S₀) → 0 (SL0, deterministic) […]

This changes comparison wording. The map is a consumer of SL0, not a premise. The complete old paragraph is unavailable, so this is not presented as an exact diff.

**I1 — EDITORIAL regions.** Council Sol's non-blocking inventory note requests P7 and G9; the disposition explicitly records their insertion after scoring. Opus #1 requests the additional occurrence/measurability inventory, now G10/S1. Opus #5 requests resolving the pending-recheck header, now :5. Current rows point to existing e4′ contracts and preserve historical statuses. The reviews/disposition document these changes; the unavailable original file prevents a complete authenticated diff.

**OTHER-SUBSTANTIVE (outside SL0): I1 e4′(i), :145–147.** Council Opus #2 explicitly describes the reviewed e4′(i) as fixing the centre to the current routine and requests the following extension, now present:

> or a replacement routine satisfying METHOD_REQUIREMENTS MR1; Lemma UM then holds with W1-N3 (c) replaced by MR1's unique-maximiser property, while Lemma UM-FP applies only to the current routine

MR1 already allowed replacements in the unchanged requirements file, so this resolves an existing package inconsistency. Under the requested hunk-level definition, however, changing the operative e4′ clause broadens the admissible routine and names a different proof input: classify it SUBSTANTIVE rather than accepting the disposition's blanket “documentation/wording only” label. It is a valid conditional generalisation when the retained deterministic/measurability and integration contracts hold; it supplies no new binary64 proof. It has no bearing on SL0.

## Reproduction and limits

The required original git search was performed as follows:

```sh
git log origin/main --format=%H -- Theory_work/Wave1C/C-PACK/<file>
git show <commit>:Theory_work/Wave1C/C-PACK/<file> | sha256sum
```

The digests below record all ten raw comparisons. The three newline-only matches and three recovered source snapshots were checked against the supplied hashes, not accepted merely because a disposition calls changes editorial. SONG_LIANG_MAP and I1 remain unauthenticated as complete before/after files; an exhaustive package-wide hunk classification cannot be supplied from the available evidence. The complete hash-verified I4 comparison suffices for the SL0-only verdict.

| file | snapshot SHA-256 | main SHA-256 |
|---|---|---|
| `STATEMENT.md` | `ffbdefeaf3a924dd2c37aa210837553081fda097b635b3935e2344aec93fdf00` | `ffbdefeaf3a924dd2c37aa210837553081fda097b635b3935e2344aec93fdf00` |
| `METHOD_REQUIREMENTS.md` | `53de1abe87e76c0126c42d27f26f0d5d7d7e6a96f12153025da4efd702630acf` | `53de1abe87e76c0126c42d27f26f0d5d7d7e6a96f12153025da4efd702630acf` |
| `SONG_LIANG_MAP.md` | `36a80a53d3b42e3e5f8ee97289e8c939852a58263402f9fd2bfc232e854ee0ba` | `93ba462e74ef5ea82c5e94acf1cee86db29457bd1dfbd637c0db7bfb6e5bca0a` |
| `lemmas/I1_e4_replacement.md` | `aa6cddb24e1ce2a8d40411088bc3d1e15870c5e7aa4641b1afe3702783ac0703` | `400e18bac3e24bbf871195558262f8200fa5906d4eca9e8b2f65a5fa893bfc77` |
| `lemmas/I2_LHiid_unconditional.md` | `d66da36f532dab6a233bba5e5f32fed68a8bd2386f0594d53f0eb92f06e1e6fa` | `0b1160ed33041cdf52462d79022e094a2602f5965f6c4886d0faa415a349fb47` |
| `lemmas/I4_SL_corollaries.md` | `bc4ecf63536adbb5477fabcb020807bf42c032346002349b028d766972fa3dd3` | `8c7f8dadd20252586987580fd2cc3d8a039735bc6060d2da2517522f53a93887` |
| `patches/P_e4_consumers.md` | `d120bf0cb80e8705a1922b5fcd3e147057dccd47b9206512b43d9e0bc1b9ca53` | `bafe818085827dcc91928af8a566d31e7749472a8e02d64876f953521be673ba` |
| `patches/P_GEN_LHiid.md` | `504a716a4ed03858dfc938a0cdeeafd2fbccf05cce7a7419c973200ed033e21e` | `01f3593534d7bdd25463744a2aa0c55563c1206852b8da8063571b55c8e07ddb` |
| `patches/P_SEL_L6d.md` | `2693253dddf10d729bcd8e43cd48a9d24c6e192fc9503a6a6fcac4c38683193f` | `88ad1ae58c01d808e9a2974c7d74b6b6b6b19af8950fb00efd48f96a98e1e10c` |
| `patches/P_L8_certificate.md` | `d6dfae19eca85e5b202074ba7c44ab269d04ede1f348be2953590b6cc5e4821d` | `fb02f03a7c61482a38d80ed4bae57a2c30d3b9ab90ac3a6a86377c0721cf1a9d` |

PC-VERDICT: SL0-EDITORIAL-ONLY
