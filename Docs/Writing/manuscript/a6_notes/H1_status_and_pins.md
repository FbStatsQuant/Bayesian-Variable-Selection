# H1 — Status diff and parameter pins (Assignment 6, item 5)

Research helper note for the Writing manager. Read-only; nothing in the manuscript was edited. Written 2026-11-23.

**Revisions compared.** Registry `Theory_work/INFRA/registry/claims.tsv` at tag `theory-v2026-11-freeze` (= `d40c9780`, committed 2026-11-17 03:03 CST) against origin/main `0f362503` (2026-11-23). The tag is an ancestor of main. Times below are the commit times (CST, −0600). The last commit that touched `claims.tsv` is `97f9c8c3` (2026-11-18 11:47); there is no registry change after 11-18 (Theory is on hold). Code pins in Part B were read in this worktree, whose `Scripts/SMC_BVS/core/` is byte-identical to origin/main (`git diff origin/main -- Scripts/SMC_BVS/core` is empty; last core commit `32c90ac1`, v3.1.1, 2026-11-18).

**Method.** A script (scratch only, `.rc_tmp/`) loaded both TSVs by `id`, and replayed every commit in `theory-v2026-11-freeze..origin/main` that touches the file, so each change below carries its commit. Status strings are quoted verbatim from the TSV (`status` column); a manifest hash is shown in full where a string is quoted in A1.3, and shortened to 8 hex characters (`MANIFEST 420c1cb0…`) in the A3 table only.

## Summary

| Item | Count |
|---|---|
| Rows added to the registry since the freeze | **12** (none removed) |
| Existing rows with *any* changed column | 121 (84 version bumps, mostly re-freezes / re-pins / requotes / council-seat additions) |
| Rows whose **status string** changed | **23** (4 upgrades to PROVED-CHECKED; 8 conditions on W1-N1:B/F dropped; 1 Prop-LB condition dropped; 1 Lemma-BC/IR condition dropped; 8 MISR condition lists rewritten W3-POST2:* → W2-APP:POST; 1 manifest re-point) |
| Manuscript status notes that changed (A3) | **22 of 54** (12 of 30 body notes, 10 of 24 ledger lines); they come from 7 underlying registry events (A3.4) |
| Code pins wrong / moved (Part B) | **0 wrong, 0 moved** (46 of 46 `tab:params-full` rows and 11 of 11 `tab:params` rows OK; all 14 requested hyperparameters found); 3 cosmetic remarks |
| Changes dated after 2026-11-17 | All 14 landing commits are 11-17 14:24 → 11-18 11:47. Eleven are on 11-17 (after the tag, which was cut at 03:03 on 11-17); three are on 11-18 (`b8ad21a4`, `df1f5872`, `97f9c8c3`). |

---

## A1. Registry diff, tag → origin/main

### A1.1 Rows added (12)

| Row id | Version | Status on main (verbatim) | Commit, date | Manuscript use |
|---|---|---|---|---|
| `W3-AUDIT-AW:ISL` | 1.0.0 | `PROVED-CHECKED; council R2, MANIFEST d4f6454099bf4befb7190c555eb2f65a25145ec4e4de2c2884fd8c1c9a580c8e, sol=9.4 PASS, opus=9.3 PASS` | `20d01e52`, 11-17 15:25 | line check of W1-N1:B (island control flow) |
| `W3-AUDIT-AW:FRZ` | 1.0.0 | same string as ISL | `20d01e52`, 11-17 15:25 | line check of W1-N1:F (freezing extension) |
| `W3-D2:Thm2X` | 1.0.3 | `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc2c23f82fca1ebd927b120f8a1788e5da422d61826785b061379c5561, sol=9.2 PASS, opus=9.6 PASS` | `2e0decc8`, 11-17 17:09 | Remark `rem:thm2x` |
| `W3-D2:Cor2X` | 1.0.0 | same string as Thm2X | `2e0decc8`, 11-17 17:09 | Remark `rem:thm2x` |
| `W3-D3:Thm2SG` | 1.0.0 | `PROVED-CHECKED; council R2, MANIFEST 1c14a298ee1cea87f3ffcfbdd37b34985b9adc31c4d040a1c6a7b088fe2b406d, sol=8.5 PASS, opus=9.3 PASS` | `0eb1b6ef`, 11-17 17:34 | Theorem `thm:post-random` (sub-Gaussian form) |
| `W3-D3:B3w` | 1.0.0 | same string | `0eb1b6ef`, 11-17 17:34 | input of Thm2SG |
| `W3-D3:ExSG` | 1.0.0 | same string | `0eb1b6ef`, 11-17 17:34 | Gaussian rows = case L = 1 |
| `W3-AUDIT-V:VIS` | 1.0.1 | `PROVED-CHECKED; council R4, MANIFEST 3326543dc8feed288bfe997ad5349548ae619acb53b8c72eb1589b8809ceada4, sol=9.5 PASS, opus=9.5 PASS (= R4 a125ce4d re-frozen CORRECTION-ONLY as VR4r3 1e298254 and as VR4r4 3326543d)` | `f9db4ee0`, 11-17 18:49 (re-pointed `97f9c8c3`, 11-18) | Remark `rem:vis` (Lemma VIS) |
| `W3-FAMC:Cor-FAMC` | 1.0.0 | `PROVED-CHECKED; council R5, MANIFEST b32ee9dfcb880019211ea2990eb48ace22aa7cb4bbca73bd3759c76d362d2579, sol=10.0 PASS, opus=9.5 PASS` | `8b4d3101`, 11-17 22:57 | Corollary `cor:famc` |
| `W3-D5P:LIST-K` | 1.0.0 | `PROVED-CHECKED; council R4, MANIFEST 0c313200d171ae6c40793fd72d567e4d2647c63ad6ba93b2075e383a809c079e, sol=9.5 PASS, opus=9.6 PASS` | `df1f5872`, 11-18 10:11 | Corollary `cor:list` |
| `W3-D5P:LIST-CODE` | 1.0.0 | `CODE-CHECKED (code reading at core 4676af6); council R4, MANIFEST 0c313200…, sol=9.5 PASS, opus=9.6 PASS` | `df1f5872`, 11-18 10:11 | Corollary `cor:list` |
| `W3-D5P:LIST-R` | 1.0.0 | `PROVED-CHECKED; council R4, MANIFEST 0c313200d171ae6c40793fd72d567e4d2647c63ad6ba93b2075e383a809c079e, sol=9.5 PASS, opus=9.6 PASS` | `df1f5872`, 11-18 10:11 | Corollary `cor:list` |

Notes from the rows (verbatim, abridged): Thm2SG — `HQ API blind audit auditD3 (Fable 5.2, two samples): FINDINGS=0 on all three claims`; `Coexists with row 1.2 (W3-POST:Thm-1 item 6 + W2-APP:POST); its hypotheses contain row 1.2's reader hypotheses (Gaussian rows: L = 1, W3-D3:ExSG)`; `all inputs PROVED-CHECKED, so no inherited condition`. Thm2X — `Tag vs the reader's Theorem 2 (card row 1.2, left untouched; the two COEXIST): MIXED / incomparable (HQ D111)`; `HQ API blind audit auditD2 … FINDINGS=0`. LIST-R — `IMPL-LIST DISCHARGED at method-v3.1.1-listpip (main 7100bb3b) by the D5P lead's code reading … plain PROVED-CHECKED, HQ ruling (i) 2026-11-18`. Cor-FAMC — `plain PROVED-CHECKED (HQ DP1: AR half unconditional; the A3 gates clear because W3-RM2:Ex-PolyR and W2-LOC2 Lemma-BC / Lemma-IR are checked in the same landing)`. VIS — `HQ API blind audit auditV … auditV2 (v1.5: 16/16 NO-FINDING, V:SCOPE included)`.

**Date quirk to know about.** Many registry notes carry the string `(HQ GO real run (task …, 2026-11-23))` inside commits dated 11-17/11-18. Commit `a1d55cef` (11-17 21:26, "track V: date nit 2026-11-23 -> 2026-11-17 in the V carriers … NOTE on the wrong-date strings") records that these are wrong-date strings, corrected only for the V carriers. They do not mean any change on 11-23.

### A1.2 Removed rows

None.

### A1.3 Rows whose status string changed (23), verbatim old → new

Grouped by landing commit. "v a → b" is the row version bump on the same commit.

**`20d01e52` — 2026-11-17 15:25 (CST) — W1-N1:B/F discharge: W3-AUDIT-AW:ISL + :FRZ registered (track A_W, council W-R2 d4f64540); D, MR retargeted; conditions dropped (HQ D111)**

- `W3-SAMP:MR` v1.1.2 → v1.1.3
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
- `W3-SAMP:D` v2.1.5 → v2.1.6
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
- `W3-SAMP:LT#` v2.0.5 → v2.0.6
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
- `W3-SAMP:C` v1.1.5 → v1.1.6
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS`
- `W3-DIST:DIST-C` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic); council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS`
  - NEW: `PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS`
- `W3-DIST:Cor-C` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic); council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS`
  - NEW: `PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS`
- `W3-READER:R4` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS`
  - NEW: `PROVED-CHECKED; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS`
- `W3-AUDIT-A:OVL` v1.0.2 → v1.0.3
  - OLD: `PROVED-CHECKED, conditional on W1-N1:B; council R2, MANIFEST ea8b464a20a950040c81f99c06ce2d195c96fa0806a5b0f1aafb8b063cadfcf0, sol=9.1 PASS, opus=9.3 PASS`
  - NEW: `PROVED-CHECKED; council R2, MANIFEST ea8b464a20a950040c81f99c06ce2d195c96fa0806a5b0f1aafb8b063cadfcf0, sol=9.1 PASS, opus=9.3 PASS`

**`33bfcb9c` — 2026-11-17 15:48 (CST) — W3-POST:Prop-LB relabelled PROVED-CHECKED by an HQ carrier on the C3 evidence (HQ GO); W3-POST2:C loses its condition on Prop-LB**

- `W3-POST:Prop-LB` v1.0.0 → v1.0.1
  - OLD: `PROVED (by this seat, unchecked)`
  - NEW: `PROVED-CHECKED; council C3, MANIFEST 420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS`
- `W3-POST2:C` v1.0.6 → v1.0.7
  - OLD: `PROVED-CHECKED, conditional on W3-POST:Prop-LB, W2-APP:POST`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST`

**`5912ce6e` — 2026-11-17 16:27 (CST) — W3-MISR-R:CorGb-plus and :CorH-U: condition lists refreshed to the current statuses of the named inputs (expansion rule; HQ GO)**

- `W3-MISR-R:CorGb-plus` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`
- `W3-MISR-R:CorH-U` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C, W3-POST2:A0, C-MIS:Prop-P; clause (G) also conditional on W3-POST2:E, W3-POST2:A1, C-MIS:GDb; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:Prop-P; clause (G) also conditional on C-MIS:GDb; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`

**`34c8fb4d` — 2026-11-17 19:27 (CST) — W3-MISR family: condition lists refreshed to the current statuses of the named inputs (expansion rule; HQ GO)**

- `W3-MISR:MIS(i)` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
- `W3-MISR:MIS(i')` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
- `W3-MISR:MIS(ii)` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
- `W3-MISR:Cor-G(b)` v1.0.1 → v1.0.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, C-MIS:GDb; input versions C-MIS:Prop-P@1.0.0, C-MIS:GD(b)@1.0.0 (C-MIS:GDb = alias of C-MIS:GD(b)); council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:Prop-P, C-MIS:GDb; input versions C-MIS:Prop-P@1.0.0, C-MIS:GD(b)@1.0.0 (C-MIS:GDb = alias of C-MIS:GD(b)); council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
- `W3-MISR:Cor-H` v2.1.1 → v2.1.2
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT)`
- `W3-MISR-R:CorH-plus` v1.0.2 → v1.0.3
  - OLD: `PROVED-CHECKED, conditional on W3-POST2:D; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`
  - NEW: `PROVED-CHECKED, conditional on W2-APP:POST; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS`

**`8b4d3101` — 2026-11-17 22:57 (CST) — W3-FAMC Cor-FAMC recorded PROVED-CHECKED; RM2 side: Lemma-BC, Lemma-IR and W3-RM2:Ex-PolyR checked; RM2 wording CORRECTION-ONLY (HQ GO)**

- `W2-LOC2:Lemma-BC` v1.0.0 → v1.0.1
  - OLD: `PROVED (by this seat, unchecked)`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST ab5fe0fed285c6ffc9d787f3385273588053cbfd6f950db8ec2aceb7e4337e1e, sol=9.3 PASS, opus=9.1 PASS`
- `W2-LOC2:Lemma-IR` v1.0.0 → v1.0.1
  - OLD: `PROVED (by this seat, unchecked)`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST ab5fe0fed285c6ffc9d787f3385273588053cbfd6f950db8ec2aceb7e4337e1e, sol=9.3 PASS, opus=9.1 PASS`
- `W3-RM2:Ex-PolyR` v1.0.3 → v1.0.5
  - OLD: `PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on W2-APP:POST, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; input versions W2-APP:POST@1.0.1, W2-LOC2:Lemma-BC@1.0.0, W2-LOC2:Lemma-IR@1.0.0`
  - NEW: `PROVED-CHECKED; council R1, MANIFEST c8596ad0676372fae8e5bcadc38debe8265f40da0f8df74c9116d08da4ccbf02, astra=9.5 PASS, opus=9.5 PASS`

**`c9b3b967` — 2026-11-17 23:19 (CST) — W3-RM2:Ex-PolyF status refresh: conditions on Lemma-BC / Lemma-IR dropped (expansion rule; HQ GO)**

- `W3-RM2:Ex-PolyF` v1.0.3 → v1.0.4
  - OLD: `PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; input versions W2-LOC2:Lemma-BC@1.0.0, W2-LOC2:Lemma-IR@1.0.0`
  - NEW: `PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round`

**`97f9c8c3` — 2026-11-18 11:47 (CST) — Pre-Lean correction batch (theory/PRE-LEAN 13d10a94, 28 patches; from Recorder-2's dry run 330b87b4): requotes, rehashes, 17 re-freezes, seat addition**

- `W3-AUDIT-V:VIS` v1.0.0 → v1.0.1
  - OLD: `PROVED-CHECKED; council R4, MANIFEST a125ce4da54949003a1c866ad116ab518cdcc4343e11fb87ff4d2fc762339248, sol=9.5 PASS, opus=9.5 PASS`
  - NEW: `PROVED-CHECKED; council R4, MANIFEST 3326543dc8feed288bfe997ad5349548ae619acb53b8c72eb1589b8809ceada4, sol=9.5 PASS, opus=9.5 PASS (= R4 a125ce4d re-frozen CORRECTION-ONLY as VR4r3 1e298254 and as VR4r4 3326543d)`

### A1.4 All landing commits on `claims.tsv` since the tag

Columns count only the fields watched (`status`, `version`, `depends_on`, `premises`, `superseded_by`, `state`, `state_reason`, `notes`); the `council`, `commit`, `sha256` and `status_sha256` columns also change on re-freezes (121 rows in all). "Added" = new rows; "changed" = existing rows with a watched change; "status" = of these, rows whose status string changed.

| Commit | Date (CST) | Added | Changed | Status | Fields changed (count of rows) | Subject (first 170 characters) |
|---|---|---|---|---|---|---|
| `d8a1334d` | 2026-11-17 14:24 | 0 | 2 | 0 | notes×2 | XR2r: track A_X council manifest re-frozen without INFRA/DECISIONS.md (CITATION-ONLY; HQ D110 GO) |
| `20d01e52` | 2026-11-17 15:25 | 2 | 42 | 8 | depends_on×2, notes×2, status×8, version×42 | W1-N1:B/F discharge: W3-AUDIT-AW:ISL + :FRZ registered (track A_W, council W-R2 d4f64540); D, MR retargeted; conditions dropped (HQ D111) |
| `33bfcb9c` | 2026-11-17 15:48 | 0 | 11 | 2 | depends_on×1, notes×1, status×2, version×11 | W3-POST:Prop-LB relabelled PROVED-CHECKED by an HQ carrier on the C3 evidence (HQ GO); W3-POST2:C loses its condition on Prop-LB |
| `5912ce6e` | 2026-11-17 16:27 | 0 | 4 | 2 | notes×2, status×2, version×4 | W3-MISR-R:CorGb-plus and :CorH-U: condition lists refreshed to the current statuses of the named inputs (expansion rule; HQ GO) |
| `2e0decc8` | 2026-11-17 17:09 | 2 | 0 | 0 |  | W3-D2: W3-D2:Thm2X and :Cor2X recorded PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P (council R2f2; HQ GO) |
| `0eb1b6ef` | 2026-11-17 17:34 | 3 | 0 | 0 |  | W3-D3: W3-D3:Thm2SG, :B3w and :ExSG recorded PROVED-CHECKED (council R2g2; presented Theorem 2, H5 card 17; HQ GO) |
| `f9db4ee0` | 2026-11-17 18:49 | 1 | 0 | 0 |  | W3-AUDIT-V:VIS (Lemma VIS, visibility with a margin uniform in n) recorded PROVED-CHECKED (council R4 -> VR4r; HQ GO) |
| `34c8fb4d` | 2026-11-17 19:27 | 0 | 12 | 6 | notes×6, status×6, version×12 | W3-MISR family: condition lists refreshed to the current statuses of the named inputs (expansion rule; HQ GO) |
| `36b56477` | 2026-11-17 19:35 | 0 | 1 | 0 | version×1 | C-ENG:TDP_E: stale code citation of `rec` fixed (v3_start.h:217-237 -> 281-300 at the pin); track A MANIFEST_R2r re-frozen CITATION-ONLY as R2r2 (HQ GO) |
| `8b4d3101` | 2026-11-17 22:57 | 1 | 3 | 3 | depends_on×1, notes×3, status×3, version×3 | W3-FAMC Cor-FAMC recorded PROVED-CHECKED; RM2 side: Lemma-BC, Lemma-IR and W3-RM2:Ex-PolyR checked; RM2 wording CORRECTION-ONLY (HQ GO) |
| `c9b3b967` | 2026-11-17 23:19 | 0 | 1 | 1 | depends_on×1, notes×1, status×1, version×1 | W3-RM2:Ex-PolyF status refresh: conditions on Lemma-BC / Lemma-IR dropped (expansion rule; HQ GO) |
| `b8ad21a4` | 2026-11-18 03:58 | 0 | 3 | 0 | premises×1, version×3 | W3-READER editorial round: READER folder from theory/W3-READER-ED 84ce4f08 (H5 card 17 swap, requotes), R4@1.0.3 / R1@1.0.4 / W3-D2:Thm2X@1.0.2 pins, R5r7, D2 R2f5 / D3 R |
| `df1f5872` | 2026-11-18 10:11 | 3 | 1 | 0 | notes×1 | W3-D5P v1.1: LIST-K, LIST-CODE, LIST-R recorded (IMPL-LIST discharged at method-v3.1.1-listpip), READER card/RV statuses, option B core-drop CITATION-ONLY re-freezes (HQ  |
| `97f9c8c3` | 2026-11-18 11:47 | 0 | 34 | 1 | depends_on×1, notes×9, status×1, version×27 | Pre-Lean correction batch (theory/PRE-LEAN 13d10a94, 28 patches; from Recorder-2's dry run 330b87b4): requotes, rehashes, 17 re-freezes, seat additions, A:IDEAL-W+ E2 not |

### A1.5 Reading the diff: what moved, in plain terms

1. **New recordings (12 rows).** Sub-Gaussian Theorem 2 (Thm2SG, B3w, ExSG), Remark thm2x (Thm2X, Cor2X), Lemma VIS, Cor-FAMC, the three list-PIP rows (LIST-K, LIST-CODE, LIST-R), and the two line-check rows for W1-N1:B/F (AW:ISL, AW:FRZ). All twelve are `PROVED-CHECKED` (LIST-CODE: `CODE-CHECKED`). Thm2X/Cor2X keep a `conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P` clause.
2. **Upgrades.** `W3-POST:Prop-LB` from `PROVED (by this seat, unchecked)` to `PROVED-CHECKED` (an HQ carrier on the existing C3 evidence, `33bfcb9c`); `W2-LOC2:Lemma-BC`, `W2-LOC2:Lemma-IR` from `PROVED (by this seat, unchecked)` to `PROVED-CHECKED; council R1 … sol=9.3 PASS, opus=9.1 PASS`; `W3-RM2:Ex-PolyR` from `PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on …` to `PROVED-CHECKED; council R1 … astra=9.5 PASS, opus=9.5 PASS` (`8b4d3101`).
3. **Conditions discharged or rewritten.** The two W1-N1:B/F conditions are gone from `W3-SAMP:C`, `:LT#`, `:MR`, `:D`, `W3-DIST:DIST-C`, `:Cor-C`, `W3-READER:R4`, `W3-AUDIT-A:OVL` (`20d01e52`). `W3-POST2:C` lost its Prop-LB condition (`33bfcb9c`). `W3-RM2:Ex-PolyF` lost its Lemma-BC/IR conditions (`c9b3b967`). Eight MISR rows had their condition lists rewritten from `W3-POST2:C/E/A1/A0/D` to `W2-APP:POST` (expansion rule; `5912ce6e`, `34c8fb4d`).
4. **No retraction, narrowing or supersession of any manuscript result** appears in the registry diff (`superseded_by` and `state` columns are unchanged for every row; no row has been removed). The queued RM2-R supersessions (QUEUE.md:52, 68) have not been executed.
5. **Unchanged but worth knowing.** `W1-N1:B` and `W1-N1:F` themselves still read `PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08.`; `W1-N1:Thm-N1` still lists `W1-N1:B;W1-N1:P;W1-N1:F` in `depends_on`. The discharge is recorded in the new `W3-AUDIT-AW:ISL/FRZ` rows and in the dependents' dropped conditions, not by re-labelling W1-N1:B/F. `SOP:TH110` (T12) still reads `PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted (adoption is Felipe's decision) [review record: …]`, although the owner adopted T12 on 11-18 (see A2); its note (`97f9c8c3`) says `T12 (2026-11-18): owner adopted 2026-11-18; PC relabel pending council evidence (notes only; no status change …)`. `W3-SAMP:MR` and `:D` list `SOP:TH110@stmt:T12 …` in `depends_on` (MR) without a corresponding "conditional on" in their status strings.

---

## A2. `Theory_work/Wave3/HQ_DECISIONS.md`, entries dated 2026-11-17 and later

Searched for CP3, accepted, recorded, PROVED-CHECKED, retract, narrow, supersede (and the claim names). Nothing retracts, narrows or supersedes a theorem used by the manuscript. The relevant lines (file line numbers):

| Line | Entry date | Quote (verbatim, short) | Bearing on the manuscript |
|---|---|---|---|
| 705 | 11-16 | `Row 3.6 is to be demoted to a remark once #5′ is proved (HQ, likely).` | Remark `thm:outputs` is already a supplement remark. #5′ (Cor 6L) is now recorded (A1.1). |
| 721 | 11-17/18 | `relabel 2676e71f (only ST → KER; R4/SAMP:C/DIST-C/OVL conditional on W1-N1:B/F, to be line-checked post-freeze);` | Explains the conditions that were dropped on 11-17 15:25. |
| 724, 728 | 11-17 | `THEORY FREEZE at d40c9780, tag theory-v2026-11-freeze (HQ); post-freeze queue from Mon 11-23 08:00 CT.` ; `THEORY FREEZE declared: tag theory-v2026-11-freeze → d40c9780 (card v1.13); entries 40e02ae7.` | The manuscript's "frozen at theory-v2026-11-freeze" refers to this tag. QUEUE.md:8 adds `Freeze tag theory-v2026-11-freeze → d40c9780 stands for recorded statements.` |
| 745 | 11-17 | `GO #3 (sub-Gaussian Thm 2) if it reuses W3-DIST's floor bridge (kill at 3 d; a coexisting claim).` | Thm2SG; recorded `0eb1b6ef`. |
| 756–758 | 11-17/18 | `Certified screening (row 3.7) is promoted to the main text … Row 3.6 → supplement remark; row 3.5 stays main once the W1-N1 discharge is recorded.` ; `Cor 9C → a conditional remark until #5′. Row 1.4 stays in the supplement.` ; `Generic-position lemma required with a margin uniform in n. #3 (sub-Gaussian Thm 2) is now required.` | Governs which results are main text; all three required items (Thm2SG, VIS, W1-N1 discharge) have since been recorded. |
| 760–761 | 11-17 | `W1-N1:B/F line checks done (AW:ISL, AW:FRZ); retarget + W3-SAMP erratum (potential pair) approved; API blind audit submitted.` ; `A1/A2: V2 corrigendum. #5′ statement locked (Corollary 6L).` | Confirms the AW rows. (`A1/A2` here are Engineering acceptance tests, not theorems.) |
| 767 | 11-17 night | `W3-D5P (#5' / Cor 6L), two-seat rule A4: the only Sol record is R1 (7.5, FAIL, LIST-R REJECT on 3 F findings in derived texts, not the maths) … HQ GO (a): one Sol continuation seat …` | History of the Cor 6L recording; the final council round (R4: sol 9.5 / opus 9.6) is in the LIST-R row. |
| 768 | 11-17 night | `OWNER GO: Sol default = gpt-6.2-sol … its false calls are confident (one false REJECT of Thm2X), so its verdicts are input, never decisions` | Thm2X was accepted despite one Sol 6.2 REJECT; the later Sol 6.2 seat on Thm2X is `sol62=9.3 PASS` (`97f9c8c3`). |
| 771 | 11-17 night | `OWNER GO: W3-FAMC, the design-family corollary for core 3 (block + moderate AR, primitive assumptions). Assembly only; … Additive, not a Lean target.` | Cor-FAMC recorded `8b4d3101`. |
| 774 | 11-18 | `#69 MERGED (main e9bac478), tagged method-v3.1-listpip. List-PIP fields (pip_list, mpm_list, log_Z_list) with the legacy fields bit-identical … Method sign-off condition 1 (IMPL-LIST) now waits only on Engineering's code-read note to Theory` | IMPL-LIST is the code-reading condition named in the `cor:list` note; discharged (LIST-R notes). |
| 777, 781 | 11-18 | `OWNER SIGNS THE METHOD AS FINAL …` ; `FROZEN METHOD TAGGED: method-v3.1.1-listpip = main 7100bb3b (PR #80, stopped-run guard). Completed fits are identical in all fields to v3.1` | The method described in the manuscript is the frozen method. |
| 778 | 11-18 | `OWNER ADOPTS T12 (SOP:TH110), the frozen-run evidence and recorded-RB identities. Theory relabels it PC through a v4 HQ carrier … ; Thm 10 (row 3.6) stays unconditional.` | The relabel has **not** happened in the registry (A1.5, item 5). "Thm 10 stays unconditional" matches the new unconditional strings of `W3-SAMP:*`. |
| 793 | 11-18 | `D5P v1.1: GO with option B. 7 accepted manifests failed verify on main because core v3.1/v3.1.1 changed hashed EXT core files … B = CITATION-ONLY re-freeze dropping only the changed core files, carriers stating the code readings remain at 4676af6. A (re-read and re-freeze at method-v3.1.1-listpip) follows as the re-pin batch.` | All "code-checked" results (L2-S3, P1-Inventory, LIST-CODE, AX:FR/REP) are pinned at core `4676af6`, not at the final tag. The re-pin batch (A) is not in the registry; Theory then went on hold (`794`: `OWNER: the Lean conversion is PAUSED …`, `finish-and-hold`; `890`: `SMC-BVS takes a BREAK`). |

Entries 11-19 … 11-23 (lines 795–896) concern Engineering, the 1M campaign, NOTS and Writing; none mentions a theorem.

---

## A3. Every status note in the manuscript against the registry on main

Legend: **SAME** = the manuscript's status wording still matches the registry on main. **CHANGED** = the registry has moved; the change is quoted. **NOT IN REGISTRY** = by design no row. Registry strings are shown up to the first `;` (the council cell after it is as in A1.1 or unchanged); manifests are shortened. Row numbers 1.x–4.1 are the card/reader numbers of `results_v2/status_ledger_freeze.tex`.

### A3.1 Body notes (30: 29 numbered + rem:moderate-n)

| # | Where | Result | Manuscript status wording (verbatim) | Registry row(s) and current status on main | Verdict |
|---|---|---|---|---|---|
| 1 | s4:23-24 (Table `tab:results`, Result 1) | Result 1 | `Proved and checked for Gaussian rows; the sub-Gaussian form proved and reviewed, not yet recorded; the fixed-design expectation bound rests on one supporting result not yet checked.` | `W3-D3:Thm2SG` `PROVED-CHECKED` (v1.0.0, `0eb1b6ef`); `W3-POST2:C` `PROVED-CHECKED, conditional on W2-APP:POST`; `W3-POST:Prop-LB` `PROVED-CHECKED` | **CHANGED** (both clauses): see #7 and #17 |
| 2 | s4:29 (table, Result 2) | Result 2 | `Proved and checked.` | `W3-DIST:Thm-A` `PROVED-CHECKED` (v1.0.1 → 1.0.3) | SAME |
| 3 | s4:34 (table, Result 3) | Result 3 | `Proved and checked; no open condition.` | `W3-RM2-R:RM2-R-plus`, `RM0-plus`, `DLV-0` `PROVED-CHECKED` (v1.0.2); `C-DLV:L2-S3`, `P1-Inventory` `CODE-CHECKED (… holds at pin 4676af6 …)`; `W3-RM2:RM2-R` `PROVED-CHECKED, conditional on W2-APP:POST` (unchanged) | SAME |
| 4 | s4:40 (table, Result 4) | Result 4 | `Proved and checked.` | `W3-SCR:A1`, `A-inf`, `SCR-A` `PROVED-CHECKED` | SAME |
| 5 | s4:44 (table, Result 5) | Result 5 | `Proved and checked.` | `W1-N1:Thm-N1` `PROVED-CHECKED`; `W3-READER:PoolZ` `PROVED-CHECKED` (v1.0.3); `W3-AUDIT-AX:FR` `PROVED-CHECKED` | SAME |
| 6 | s4:50-51 (table, Result 6) | Result 6 | `Proved and checked; the exact order on orthogonal designs uses the fixed-design expectation bound and has its status.` | `W3-PSHARP:A`, `:B`, `W3-PSHARP-R:AE`, `:A2C` `PROVED-CHECKED` (unchanged) | SAME (the dependence on the expectation bound now rests on a row that is no longer conditional on Prop-LB; wording stays true) |
| 7 | s4:124-126 | Theorem `thm:post-random` (sub-Gaussian Thm 2) | `Sub-Gaussian form, as stated: proved, and passed its independent review; not yet recorded in the registry (HQ acceptance and an external blind audit pending; the note is requoted when it is recorded). Its inputs are proved and independently checked. The Gaussian case L=1 is the recorded row 1.2: proved and independently checked.` | `W3-D3:Thm2SG`, `W3-D3:B3w`, `W3-D3:ExSG`: `PROVED-CHECKED; council R2, MANIFEST 1c14a298…, sol=8.5 PASS, opus=9.3 PASS`. Notes: `HQ API blind audit auditD3 (Fable 5.2, two samples): FINDINGS=0 on all three claims`; `all inputs PROVED-CHECKED, so no inherited condition`. Row 1.2 (`W3-POST:Thm-1`, `W2-APP:POST`, `W3-READER:R1`) unchanged strings | **CHANGED**: `not yet recorded` → recorded `0eb1b6ef` (11-17 17:34); blind audit done; a Sol 6.2 seat (`sol62=9.1 PASS`) was added `97f9c8c3` (11-18) with `the existing seats and the status are unchanged` |
| 8 | s4:143-145 | Remark `rem:thm2x` (Thm2X/Cor2X) | `Conditional: it rests on the inputs of Theorem~omitted, one of which (a deterministic rate lower bound used in the expectation route) has not yet had an independent check, and two others are earlier-wave results; passed its independent review, not yet recorded in the registry.` | `W3-D2:Thm2X` v1.0.3 and `W3-D2:Cor2X` v1.0.0: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc…, sol=9.2 PASS, opus=9.6 PASS` (`2e0decc8`, 11-17 17:09). `C-MIS:GD(b)` `R02 VERIFIED-WITH-AMENDMENTS (applied); council PASS`; `C-MIS:Prop-P` `R02 VERIFIED; R04 wording fixes checked in R05; council PASS` | **CHANGED**: recorded; the clause "a deterministic rate lower bound … has not yet had an independent check" is obsolete (`W3-POST:Prop-LB` is now `PROVED-CHECKED`). The "conditional" part still holds, now naming `W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P` |
| 9 | s4:203 | Theorem `thm:dist` | `Proved and independently checked. Registry: row 2.1.` | `W3-DIST:Thm-A` `PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS` | SAME |
| 10 | s4:308-311 | Theorem `thm:reported` | `Proved and independently checked, with no open condition … Registry: row 3.1.` | as #3 | SAME |
| 11 | s4:353-356 | Corollary `cor:list` (Cor 6L) | `Proved, and passed its independent review; not yet recorded in the registry; recorded on the card as conditional on a code reading of the method commit that adds the corresponding output fields (pending) …` | `W3-D5P:LIST-K` `PROVED-CHECKED`; `W3-D5P:LIST-CODE` `CODE-CHECKED (code reading at core 4676af6)`; `W3-D5P:LIST-R` `PROVED-CHECKED` — all `council R4 … sol=9.5 PASS, opus=9.6 PASS` (`df1f5872`, 11-18 10:11). Note: `IMPL-LIST DISCHARGED at method-v3.1.1-listpip (main 7100bb3b) … plain PROVED-CHECKED, HQ ruling (i) 2026-11-18` | **CHANGED**: recorded; the pending code reading is done and the status is plain `PROVED-CHECKED`. Caveat in LIST-CODE note: `the status stays 'code reading at core 4676af6', its re-pin to the tag is a later step` |
| 12 | s4:392 | Theorem `thm:screen` | `Proved and independently checked. Registry: row 3.7.` | `W3-SCR:A1`, `A-inf`, `SCR-A` `PROVED-CHECKED` | SAME |
| 13 | s4:423-425 | Proposition `prop:unbiased` | `Proved and independently checked (registry). It uses two results on the coded sampler, recorded as proved under their named premises and independently checked under an earlier protocol; their final line check is running, and the status will be requoted when it is recorded. Registry: row 3.5.` | `W3-AUDIT-AW:ISL`, `W3-AUDIT-AW:FRZ` `PROVED-CHECKED; council R2, MANIFEST d4f64540…, sol=9.4 PASS, opus=9.3 PASS` (`20d01e52`, 11-17 15:25). `W1-N1:B`, `W1-N1:F` strings unchanged (see A1.5 item 5) | **CHANGED**: the line check is no longer "running"; it is recorded and passed |
| 14 | s4:432-433 | Pooled form of `prop:unbiased` | `Pooled form: proved and independently checked; the frozen-run identities behind both forms are proved and independently checked against the code of record. Registry: row 3.5.` | `W1-N1:Thm-N1` `PROVED-CHECKED`; `W3-READER:PoolZ` `PROVED-CHECKED` (v1.0.3; `depends_on` gained `W3-SAMP:MR@stmt:MR-b; W3-SAMP:CC` in `97f9c8c3`); `W3-AUDIT-AX:FR` `PROVED-CHECKED` | SAME. ("the code of record" is the code at core `4676af6`, not at `method-v3.1.1-listpip`; see A2 line 793.) |
| 15 | s4:483-486 | Remark `rem:sharp` | `(a) and (b): proved and independently checked; the exact-order statement after (b) uses the expectation bound and has its status. Registry: row 1.3. (c): a heuristic calculation … no registry row.` | `W3-PSHARP:A`, `:B`, `W3-PSHARP-R:AE`, `:A2C` `PROVED-CHECKED` | SAME for (a),(b); (c) **NOT IN REGISTRY** (by design) |
| 16 | s5:242 | Remark `rem:vis` (Lemma VIS) | `Lemma VIS: proved, and passed its independent review; recording in the registry pending.` | `W3-AUDIT-V:VIS` v1.0.1 `PROVED-CHECKED; council R4, MANIFEST 3326543d…, sol=9.5 PASS, opus=9.5 PASS (= R4 a125ce4d re-frozen CORRECTION-ONLY as VR4r3 1e298254 and as VR4r4 3326543d)` | **CHANGED**: recorded `f9db4ee0` (11-17 18:49); first string had `MANIFEST a125ce4d…` (re-pointed `97f9c8c3`, 11-18). Notes: `auditV2 (v1.5: 16/16 NO-FINDING, V:SCOPE included)`; `visibility stays a hypothesis of Theorem 6 (A3) …; no status change of any existing row` |
| 17 | supp:50-53 | Theorem `thm:post-fixed` | `The in-probability conclusions: proved and independently checked. The expectation bound: proved and checked, conditional on one supporting result (a proposition giving a lower bound on the posterior miss) that is proved but not yet independently checked; its other input, a lemma bounding the tail of the posterior model size, is now independently checked. Registry: row 1.1.` | `W3-POST2:C` v1.0.7 `PROVED-CHECKED, conditional on W2-APP:POST` (was `…, conditional on W3-POST:Prop-LB, W2-APP:POST`); `W3-POST:Prop-LB` v1.0.1 `PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7 PASS` (was `PROVED (by this seat, unchecked)`) — `33bfcb9c`, 11-17 15:48. In-probability rows (`SOP:TH09`, `W3-POST:Thm-1`, `W3-READER:R1`) same strings | **CHANGED** (expectation bound only): the "proved but not yet independently checked" clause is obsolete |
| 18 | supp:85-86 | Remark `rem:no-betamin` | `Part of the posterior concentration result, with the status of the in-probability form of Theorem~post-fixed.` | as #17, in-probability rows | SAME |
| 19 | supp:106-108 | Theorem `thm:post-margin` | `The in-probability conclusions: proved and independently checked. The expectation bound: proved and checked, conditional on the same supporting result (the lower-bound proposition, not yet independently checked) as the expectation bound of Theorem~post-fixed.` | `W3-POST2:E` v1.0.7 and `W3-POST2:D` v1.1.7 `PROVED-CHECKED, conditional on W2-APP:POST` (strings unchanged); `W3-POST2:C` and `Prop-LB` as #17 | **CHANGED** (same clause as #17) |
| 20 | supp:144-146 | Theorem `thm:omitted` | `Proved and checked, conditional on the expectation bound of Theorem~post-fixed (hence on the lower-bound proposition, not yet independently checked) and on two lemmas on Gaussian designs that are independently verified. Registry: row 1.4.` | `W3-MISR-R:CorGb-plus` v1.0.3 and `W3-MISR:MIS(i)` v1.0.2: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P` (CorGb-plus; was `… conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P`) and `PROVED-CHECKED, conditional on W2-APP:POST` (MIS(i); was `… conditional on W3-POST2:C`) — `5912ce6e`, `34c8fb4d`, 11-17 | **CHANGED**: the "hence on the lower-bound proposition, not yet independently checked" clause is obsolete; the registry now names `W2-APP:POST` instead of the expectation bound |
| 21 | supp:175 | Proposition `prop:dist` | `Proved and independently checked (part of the same result as Theorem~dist). Registry: row 2.1.` | `W3-DIST:Thm-A` | SAME |
| 22 | supp:188 | Theorem `thm:dist-param` | `Proved and independently checked. Registry: row 2.1.` | `W3-DIST:Thm-B` `PROVED-CHECKED` (v1.0.1 → 1.0.3) | SAME |
| 23 | supp:207-208 | Remark `cor:dist-output` | `Proved and checked, conditional on exact arithmetic and on [two results on the coded sampler …, themselves proved under their named premises and independently checked]; the description of the output was checked against the code. Registry: row 2.1.` | `W3-DIST:Cor-C` v1.0.3 `PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c817…` (was `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic); …`) — `20d01e52`, 11-17 15:25 | **CHANGED**: the sampler-results condition is dropped; only exact arithmetic remains. Note added `97f9c8c3`/`df1f5872`: `Cor 6L supplies this corollary's list-mass premise pathwise …; the probability form under this corollary's law needs the raw-scale bridge READER B6.7 (open). (The class 'designs inside both Theorem 9 and Theorem 6' is empty for s0 >= 1: ERRATA E3 of W3-D5P.)` |
| 24 | supp:226 | Theorem `thm:start` | `Proved and independently checked. Registry: row 3.3.` | `W3-START2-R:START-R` v1.0.1, `:BR` `PROVED-CHECKED`; `W3-START:FLOOR` `PROVED-CHECKED` | SAME |
| 25 | supp:267-268 | Theorem `thm:reported-fixed` | `Proved and independently checked, with no open condition … Registry: row 3.2.` | `W3-RM2-R:RM2-F-plus` v1.0.2 `PROVED-CHECKED`; `W3-RM2:RM2-F` `PROVED-CHECKED` (unchanged); `C-DLV` rows as #3 | SAME |
| 26 | supp:291-292 | Corollary `cor:famc` | `Proved and independently checked (recorded on main at 8b4d3101): an assembly of recorded results, with no new assumption. Registry: claim W3-FAMC:Cor-FAMC.` | `W3-FAMC:Cor-FAMC` v1.0.0 `PROVED-CHECKED; council R5, MANIFEST b32ee9df…, sol=10.0 PASS, opus=9.5 PASS` (`8b4d3101`, 11-17 22:57) | SAME (already requoted as recorded) |
| 27 | supp:332 | Remark `thm:outputs` (row 3.6) | `Proved and checked, conditional on [two results on the coded sampler …]. Registry: row 3.6.` | `W3-SAMP:C` v1.1.6, `:LT#` v2.0.6, `:D` v2.1.6: `PROVED-CHECKED; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS` (were `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; …` and, for D, `… conditional on W1-N1:B; …`); `W3-READER:R4` v1.0.3 `PROVED-CHECKED` (was `… conditional on W1-N1:B, W1-N1:F; …`); `W3-SAMP:TR`, `W3-START2-R:IF-START` unchanged — `20d01e52`, 11-17 15:25 | **CHANGED**: no sampler-results condition remains on any of these rows |
| 28 | supp:340-341 | Remark `thm:outputs`(iii), row 4.1 | `proved and checked, conditional on the same two sampler results as Remark~thm:outputs; registry row 4.1` | `W3-SAMP:LT#` v2.0.6 `PROVED-CHECKED; council R1 …` (was `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; …`) | **CHANGED** (as #27) |
| 29 | supp:368-369 | Remark `rem:alt-route` | `Proved and independently checked; its global-overlap premise is a named open premise. Registry: row 3.6.` | `W3-SAMP:TR` v2.1.6 `PROVED-CHECKED; council R1 …` (unchanged string; `W3-SAMP:TR` summary still names `P-CONC + P-OVL∞`); `W3-AUDIT-A:OVL` `PROVED-CHECKED` (was `… conditional on W1-N1:B; …`) | SAME |
| — | supp:66 | Remark `rem:moderate-n` | `a heuristic, not a theorem` (no status block) | no row | **NOT IN REGISTRY** (by design) |

Result of A3.1: **12 body notes CHANGED** (#1, 7, 8, 11, 13, 16, 17, 19, 20, 23, 27, 28), 17 SAME, 1 NOT IN REGISTRY. (Several of the 12 are the same underlying change quoted in different places.)

### A3.2 The five items the assignment asked about ("passed its independent review; not yet recorded")

| Item | Recorded since the freeze? | Registry row and string |
|---|---|---|
| Sub-Gaussian Theorem 2 form | **Yes** | `W3-D3:Thm2SG`, `W3-D3:B3w`, `W3-D3:ExSG`: `PROVED-CHECKED; council R2, MANIFEST 1c14a298ee1cea87f3ffcfbdd37b34985b9adc31c4d040a1c6a7b088fe2b406d, sol=8.5 PASS, opus=9.3 PASS` (`0eb1b6ef`, 11-17 17:34) |
| Remark `thm2x` | **Yes** | `W3-D2:Thm2X`, `W3-D2:Cor2X`: `PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc2c23f82fca1ebd927b120f8a1788e5da422d61826785b061379c5561, sol=9.2 PASS, opus=9.6 PASS` (`2e0decc8`, 11-17 17:09) |
| Corollary `cor:list` | **Yes** | `W3-D5P:LIST-R`: `PROVED-CHECKED; council R4, MANIFEST 0c313200d171ae6c40793fd72d567e4d2647c63ad6ba93b2075e383a809c079e, sol=9.5 PASS, opus=9.6 PASS`; `LIST-K` same; `LIST-CODE`: `CODE-CHECKED (code reading at core 4676af6); council R4, …` (`df1f5872`, 11-18 10:11) |
| Lemma VIS | **Yes** | `W3-AUDIT-V:VIS`: `PROVED-CHECKED; council R4, MANIFEST 3326543dc8feed288bfe997ad5349548ae619acb53b8c72eb1589b8809ceada4, sol=9.5 PASS, opus=9.5 PASS (= R4 a125ce4d re-frozen CORRECTION-ONLY as VR4r3 1e298254 and as VR4r4 3326543d)` (`f9db4ee0`, 11-17 18:49; re-pointed `97f9c8c3`) |
| Cor-FAMC | Yes, after the tag; the manuscript already says so | `W3-FAMC:Cor-FAMC`: `PROVED-CHECKED; council R5, MANIFEST b32ee9dfcb880019211ea2990eb48ace22aa7cb4bbca73bd3759c76d362d2579, sol=10.0 PASS, opus=9.5 PASS` (`8b4d3101`, 11-17 22:57). Not in the tag, so "recorded" is a post-tag fact the manuscript already carries. |

### A3.3 Appendix "Status ledger" (`appendices.tex:206-241`, table from `results_v2/status_ledger_freeze.tex`)

The ledger's own heading says `claims.tsv at tag theory-v2026-11-freeze`; every cell below is therefore a statement about the tag. Verdict is against main.

| # | Ledger row (result, card row) | Registry rows quoted at the tag | Verdict on main |
|---|---|---|---|
| L1 | Theorem 3.1 random design, 1.2 | `W3-POST:Thm-1@1.0.1`, `W2-APP:POST@1.0.7`, `W3-READER:R1@1.0.2`: all `PROVED-CHECKED…` | SAME strings (Thm-1 v1.0.2, R1 v1.0.5 re-pins). Adds the new coexisting `W3-D3:Thm2SG` |
| L2 | Theorem 3.2, in-probability, 1.1 | `SOP:TH09@1.0.2`, `W3-POST:Thm-1`, `W3-READER:R1` | SAME |
| L3 | Theorem 3.2, expectation bound, 1.1 | `W3-POST2:C@1.0.6`: `PROVED-CHECKED, conditional on W3-POST:Prop-LB, W2-APP:POST`; `W3-POST:Prop-LB@1.0.0`: `PROVED (by this seat, unchecked)`; label `proved and checked, conditional on one supporting result (Prop-LB) not yet independently checked` | **CHANGED**: `W3-POST2:C@1.0.7` `PROVED-CHECKED, conditional on W2-APP:POST`; `Prop-LB@1.0.1` `PROVED-CHECKED; council C3, …` (`33bfcb9c`) |
| L4 | Remark 3.3 (Result 5), 1.3 | `W3-PSHARP:A`, `:B`, `W3-PSHARP-R:AE`, `:A2C` | SAME |
| L5 | Theorem 4.2, 2.1 | `W3-DIST:Thm-A@1.0.1` | SAME (v1.0.3) |
| L6 | Theorem 5.3, 3.1 | `W3-RM2-R:RM2-R-plus`, `RM0-plus`, `DLV-0`, `C-DLV:L2-S3`, `C-DLV:P1-Inventory`, `W3-RM2:RM2-R`, `W2-APP:POST`, `W3-READER:R2`, `W3-AUDIT-AX:REP` | SAME strings |
| L7 | Proposition 6.1 and pooled form, 3.5 | `W1-N1:Thm-N1`, `W3-READER:PoolZ`, `W3-AUDIT-AX:FR` | SAME strings (see #13 for the line-check change) |
| L8 | Theorem 6.2, 3.6 | `W3-SAMP:C@1.1.5` `PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; …`; `W3-SAMP:LT#@2.0.5` same; `W3-SAMP:D@2.1.5` `… conditional on W1-N1:B; …`; `W3-SAMP:TR`; `W3-START2-R:IF-START`; `W3-READER:R4@1.0.1` `… conditional on W1-N1:B, W1-N1:F; …`; `W1-N1:B/F` `PROVED under the named premises …`; label `proved and checked, conditional on W1-N1:B, W1-N1:F (themselves proved under named premises and independently checked)` | **CHANGED**: SAMP:C, LT#, D and READER:R4 now plain `PROVED-CHECKED; council …` (`20d01e52`). W1-N1:B/F strings unchanged |
| L9 | Remark 6.3(iii), 4.1 | `W3-SAMP:LT#@2.0.5` `… conditional on W1-N1:B, W1-N1:F; …` | **CHANGED** (as L8) |
| L10 | Theorem A.3, 1.1 | `W3-POST2:E@1.0.6` (same); `W3-POST2:C@1.0.6` (as L3) | E: SAME; C: **CHANGED** (as L3) |
| L11 | Theorem A.5, 1.4 | `W3-MISR-R:CorGb-plus@1.0.1` `… conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; …`; `W3-MISR:MIS(i)@1.0.1` `… conditional on W3-POST2:C; …`; `C-MIS:GD(b)`, `C-MIS:Prop-P` | **CHANGED**: CorGb-plus `… conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; …`; MIS(i) `… conditional on W2-APP:POST; …`; the C-MIS rows are unchanged |
| L12 | Proposition A.6, 2.1 | `W3-DIST:Thm-A` | SAME |
| L13 | Theorem A.7, 2.1 | `W3-DIST:Thm-B` | SAME |
| L14 | Corollary A.8, 2.1 | `W3-DIST:Cor-C@1.0.1` `… conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic); …` | **CHANGED**: `… conditional on EX-A (exact arithmetic); …` |
| L15 | Theorem A.9, 3.3 | `W3-START2-R:START-R`, `:BR`, `W3-START:FLOOR` | SAME |
| L16 | Theorem A.11, 3.2 | `W3-RM2-R:RM2-F-plus`, `W3-RM2:RM2-F`, `RM0-plus`, `DLV-0`, `C-DLV:*` | SAME |
| L17 | Theorem A.12, 3.7 and Remark A.13, 3.6 | `W3-SCR:A1`, `A-inf`, `SCR-A`; `W3-SAMP:TR@2.1.5` | SAME (premise `P-OVL∞` still open) |
| P1 | Paragraph "What changed at the freeze" (last sentence): `Remark~thm:outputs, Remark~cor:dist-output and the worst-island bound now carry two explicit conditions, results on the coded sampler …` | | **CHANGED**: those conditions are discharged (L8, L9, L14) |
| P2 | "What remains" item 1: `The lower-bound proposition behind~(post-exp) awaits its independent check.` | | **CHANGED**: Prop-LB `PROVED-CHECKED` (L3) |
| P3 | item 2: `The two results on the coded sampler behind Result~5, Remark~cor:dist-output and Remark~thm:outputs (W1-N1:B, W1-N1:F) await their final line check` | | **CHANGED**: line checks recorded (`W3-AUDIT-AW:ISL`, `:FRZ`) |
| P4 | item 3: `The superseded masters of Theorems~reported and~reported-fixed are retired in the registry (deferred past the freeze …)` | | SAME: still not retired (no `superseded_by` change; QUEUE.md:52, 68) |
| P5 | item 4: `The global-overlap premise of Remark~alt-route stays a named open premise.` | | SAME |
| P6 | item 5: `Planned: if the store-restricted result (track D, #5′, Corollary 6L) is recorded, it would supply the premise of Remark~cor:dist-output and the consistency of the summaries computed from the returned list on every design of Result~3; Remark~thm:outputs is a remark until then.` | | **CHANGED**: Cor 6L is recorded (`df1f5872`). Qualification in the registry: it supplies the list-mass premise only pathwise; the probability form needs `READER B6.7` (open); and the class of designs inside both Theorem 9 and Theorem 6 is empty for s0 ≥ 1 (ERRATA E3 of W3-D5P) |
| P7 | Paragraph "Assumptions on mathematical objects" | | SAME |

Ledger result: **10 CHANGED lines** (L3, L8, L9, L10, L11, L14, P1, P2, P3, P6), 14 SAME.

### A3.4 Tally

| Part | Notes / lines | CHANGED | SAME | NOT IN REGISTRY |
|---|---|---|---|---|
| Body status notes (`s4`, `s5`, `supplement`; A3.1) | 30 | **12** | 17 | 1 (`rem:moderate-n`; also part (c) of `rem:sharp`, a heuristic by design) |
| Appendix status ledger (A3.3) | 24 lines (17 table rows, 7 prose lines) | **10** | 14 | 0 |
| **Total** | 54 | **22** | 31 | 1 |

The 22 reduce to **seven underlying registry events**: (1) `W3-POST:Prop-LB` checked and `W3-POST2:C` unconditional on it (`33bfcb9c`); (2) the two W1-N1:B/F line checks recorded and their conditions dropped from the sampler rows (`20d01e52`); (3) sub-Gaussian Theorem 2 recorded (`0eb1b6ef`); (4) Thm2X / Cor2X recorded (`2e0decc8`); (5) Lemma VIS recorded (`f9db4ee0`); (6) Cor 6L (LIST-K/CODE/R) recorded (`df1f5872`); (7) the MISR condition lists rewritten from `W3-POST2:*` to `W2-APP:POST` (`5912ce6e`, `34c8fb4d`). Cor-FAMC was recorded at `8b4d3101` and the manuscript already says so.

**Manuscript wording that is now stale (for the manager's edit list).** Each is a sentence that says "not yet recorded", "not yet checked", "pending" or "running" for something the registry now records: `s4:23-24`, `s4:124-126`, `s4:143-145`, `s4:353-356`, `s4:423-425`, `s5:242`, `supplement:50-53`, `supplement:106-108`, `supplement:144-146`, `supplement:207-208`, `supplement:332`, `supplement:340-341`, and the appendix ledger paragraph "What changed at the freeze" (last sentence) and "What remains" items 1, 2, 5. The `\samplerconds` macro text (`manuscript.tex:30`) and its uses are in the same group.

**Do not overstate.** Three things remain true and should stay in the text: (a) the code-checked rows (`C-DLV:L2-S3`, `P1-Inventory`, `W3-D5P:LIST-CODE`, `W3-AUDIT-AX:FR/REP`) are pinned at core `4676af6`, not at `method-v3.1.1-listpip` (A2 line 793); (b) Cor 6L supplies the list-mass premise only pathwise (the probability form needs `READER B6.7`, open; the class of designs inside both Theorem 9 and Theorem 6 is empty for s0 ≥ 1, ERRATA E3); (c) the thm2x "conditional" remains, now on `W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P`.

**Registry inconsistencies the manager should know about (not manuscript errors).** (i) About 20 rows still read `conditional on W2-APP:POST` although `W2-APP:POST` is plain `PROVED-CHECKED`; the manuscript says "proved and independently checked" for these, which is what the registry says for the row itself, so no wording change is needed, but a reader who opens `claims.tsv` will see the clause. (ii) `SOP:TH110` (T12) still says `not adopted`, although the owner adopted it on 11-18 (HQ_DECISIONS:778); the relabel is pending. `W3-SAMP:MR` depends on it. The manuscript does not quote this row's status.

---

## A4. Named open items in `Theory_work/Dept/QUEUE.md`

`QUEUE.md` is headed `Updated 2026-11-15 19:40 CT`, with three later hand edits dated 11-16/11-17, so it predates the whole post-freeze landing (A1) and Theory's hold (HQ_DECISIONS:794, 890). Items that A1 shows as discharged are marked **[DONE since]**; they are listed because the queue still shows them as open. Housekeeping (editorial batches, recorder tasks, tool work, relabelling, NOTS moves, supersessions, citechecks, acceptance paperwork) is excluded; the excluded groups are named at the end.

### A4.1 Open theory problems, premises and bridges

| # | Item (plain description) | Source line |
|---|---|---|
| 1 | **READER B6.7, raw-scale search bridge.** Needed to turn Cor 6L's pathwise statement into a probability statement ("Cor 6L supplies Cor 9C's list-mass premise"). Declared a follow-up paper / open item, not a ticket. Registry note on `W3-DIST:Cor-C` repeats it. | QUEUE:111 |
| 2 | **RM2-R aggregated leak (D).** The leak term of the reported-model result when aggregated over blocks; open in the queue's shorthand (D = not done). | QUEUE:112 |
| 3 | **START MIS with a general μ (D).** The start-law mis-specification result for a general prior mean/mode μ; not done. | QUEUE:112 |
| 4 | **Ex-Equi for b < 3/8 (O4′).** The equicorrelated example below the 3/8 threshold, "if not done in W3-RM2-R"; the registry has the 3/8 case only (`W3-RM2-R` rows). | QUEUE:112 (also QUEUE:16-17 "Ex-Equi 3/8 optional") |
| 5 | **START2-O1 count (17 − s₀).** Open count in START2's visibility/credit argument (shorthand). | QUEUE:112 |
| 6 | **Global-overlap premise P-OVL∞** of Remark `rem:alt-route` / `W3-SAMP:TR` stays a named open premise (not in QUEUE; confirmed by the registry row text and the manuscript ledger). Listed for completeness. | not in QUEUE (registry `W3-SAMP:TR`) |
| 7 | **SAMP-R1.** Truth-free D; total-variation re-centring of C; hybrid TR bound; LT rate under NC_r (sampler-result improvements). | QUEUE:71 |
| 8 | **POST2-O1.** A design-free sufficient condition for the (OS) premise, which would make "no eigenvalue condition off S₀" literally true. | QUEUE:72 |
| 9 | **POST2-O3 (E-floor+).** Bounded ridge cost in place of the floor on S₀, for design-agnosticism; first post-freeze item by owner tie-break. | QUEUE:73 |
| 10 | **POST2-O2 (E+).** Lower the constant c₁; if c₁ < c₀, the inclusion-range result MIS(i′) covers C-MIS, giving a C-MIS → MISR supersession. | QUEUE:74 |
| 11 | **POST2-R1.** A matching expectation lower bound E δ_n ≳ √(log n/n) on every design with a floor (Theorem 1 two-sided); "one unverified step". | QUEUE:75 |
| 12 | **SCR-R1.** Corollary of SCR-A + B2d with κ_n b_n²(n²−1) ≥ 4M_n²; plus dropping the "fixed" signals, ℓ¹ → total signal, exponential rate. | QUEUE:76 |
| 13 | **C-PACK e4′(i) re-check.** A substantive post-C1 change to the tie-rule step e4′(i) (allows MR1 replacement routines, uses MR1's unique-maximiser property) is unchecked; tied to NARROW item M55 (`C-PACK:I1-e4prime`). Not under an abstract row. | QUEUE:80 |
| 14 | **DIST sharpness review.** (1) (A4) via the narrower (ND) with a design-agnostic tie-break; (2) 8(a) + 10: log(p∨n) rate with explicit A; (3) 9: linear s₀ in (iii), uniform in s₀; 8(b). | QUEUE:93 |
| 15 | **DIST item 9, true s₀-dependence.** True dependence of the rate is (1+s₀^r)³ against the Sparse-Linear-style s log p / n; item 8 = ε_n² ≍ (1+s₀) log p / n with a constant free of A. | QUEUE:96-97 |
| 16 | **Rider P1 (MISR).** Contraction at log n / n without beta-min, Gaussian candidate rows; feeds pillar 2. | QUEUE:104 |
| 17 | **Representability lemma (D88).** If it holds, a STRONGER card for row 3.1. Status after 11-15 not stated in the queue; Lemma VIS (`W3-AUDIT-V:VIS`) and Cor 6L were recorded afterwards and may have taken this role (the queue does not say). | QUEUE:65 |
| 18 | **Parked: parallel-SMC theory (T-MERGE, EVAR/POOL)** and the Lean readiness of the deterministic cores of the consistency results. | QUEUE:118 |

### A4.2 Items the queue still lists as open that the registry shows discharged **[DONE since]**

| Item | Source line | Discharged by |
|---|---|---|
| W1-N1:B (island control flow, stopping time, B-0/B-d, B-d MEAS) and W1-N1:F (freezing extension beyond fixed c, T12 (iii)) Tier B line checks; "when checked, R4 / DIST-C / OVL discharge" | QUEUE:56, 9 | `W3-AUDIT-AW:ISL`, `:FRZ` (`20d01e52`); the conditions are gone (A3.1 #13, #23, #27) |
| Check X: does CorGb-plus + design transfer cover Theorem 2's setting (candidate master for row 1.2)? | QUEUE:105 | `W3-D2:Thm2X`, `Cor2X`; HQ D111: `MIXED / incomparable`, the two coexist |
| Sub-Gaussian Thm 2 (T-D3) | QUEUE:48, 8 | `W3-D3:Thm2SG` (`0eb1b6ef`) |
| Store-restricted clause #5′ / Cor 6L; IMPL-LIST discharge | QUEUE:7, 8, 48 | `W3-D5P:LIST-K/CODE/R` (`df1f5872`) |
| Generic-position / visibility lemma (D112) | QUEUE:10 | `W3-AUDIT-V:VIS` (`f9db4ee0`) |
| Relabel `W3-POST:Thm-1`; W3-SAMP:C accept record → discharges READER:R4's two `@hyp` conditions (row 3.6) | QUEUE:59 | `W3-SAMP:C` and `W3-READER:R4` now unconditional (`20d01e52`) |
| Lemma `W3-POST:Prop-LB` unchecked / "W2 Lemma 1a′ registry label 'unchecked' is stale" | QUEUE:64, 81 | `Prop-LB` `PROVED-CHECKED` (`33bfcb9c`); Lemma-BC/IR (`W2-LOC2`) `PROVED-CHECKED` |
| Tier B Sol check of `C-DLV:L2-S3` and `P1-Inventory` ("last unchecked input on row 3.1") | QUEUE:61 | Both read `CODE-CHECKED (… holds at pin 4676af6 …)` and row 3.1 is plain `PROVED-CHECKED`; their re-pin to the final tag is not done (A2 line 793) |
| Row 3.6 demotion to a remark after #5′ | QUEUE:62 | Done in the manuscript (Remark `thm:outputs`) |

### A4.3 Excluded as housekeeping (not listed above)

Editorial and citation batches (QUEUE:47, 52-54, 56 tools, 58, 60, 63-64, 66-67, 83, 86-89, 91-92, 94-95, 98-103, 106-108); supersession and relabel paperwork (QUEUE:52, 68, 84, 90); recorder and tool tasks (QUEUE:55, 57, 88, 89, 92, 107); acceptance paperwork (QUEUE:81, 82, 85); the NARROW batch (QUEUE:77); the errata batch (QUEUE:79); "Not ours" W3-PATH, T7, P6/D1 (QUEUE:115); operational items for Engineering/HQ (QUEUE:49, 67).

---

## B. Parameter-table pins against `Scripts/SMC_BVS/core/` on origin/main

All cited lines were opened in this worktree. `git diff origin/main -- Scripts/SMC_BVS/core` is empty; the last commit touching `core/` is `32c90ac1` (v3.1.1, 2026-11-18). "OK" = the value or formula is as in the table and the cited line(s) contain it. No pin has moved.

### B1. `tab:params-full` (`appendices.tex:44-99`), row by row

| # | Row (symbol) | Value in the table | Code pin in the table | Found at the pin | Verdict |
|---|---|---|---|---|---|
| 1 | size cap (K) | min(p, ⌊n/2⌋); 100 | `cpp/v3_score.h:40`; `v3_preprocess.R:21` | `D.K = std::min(p, n / 2)` (n, p integers, so floor); `K <- min(p, n %/% 2)` | OK |
| 2 | model prior BB(1,p) (w(k)) | ½/C(2p−1,k), renormalised to Ω | `cpp/v3_score.h:61-70` | `D.logw[k] = -M_LN2 - lchoose_d(2.0*p - 1.0, k)` (line 65); `logWK = log_sum_exp(terms)` (68); `logprior[k] = logw[k] - logWK` (70). Algebra: the BB(1,p) per-model weight B(1+k, 2p−k)/B(1,p) = 1/(2·C(2p−1,k)) | OK |
| 3 | g, ridge | g = n; unit ridge; 200 | `cpp/v3_score.h:175-183` | `H = (n+1) G_S + I`, `A = G_S + I` (lines 175, 181-182). The literal `g = n` does not appear: it enters as `n+1` in H (posterior precision = g·G + G + I with g = n) and as the ridge `+I`; a derived location | OK (cosmetic remark 2) |
| 4 | a₀, b₀ | 0.01, 0.01 | `cpp/v3_score.h:14` | `a0 = 0.01, b0 = 0.01` | OK |
| 5 | duplicate threshold | \|r̂_jl\| ≥ 1−10⁻¹⁰ (reported only) | `cpp/v3_core.cpp:742-760` | `cpp_dup_components`, test at line 754 `>= 1 - 1e-10` | OK |
| 6 | small-S_S recomputation | S_S < 10⁻⁸ yᵀy | `cpp/v3_score.h:219` | `if (Q < 1e-8 * D->yty) { Q = q_nonneg(...) }` | OK |
| 7 | block size cap (B) | min(⌊√n⌋, ⌊√p⌋, 16); 14 | `v3_preprocess.R:22`; cap at `cpp/v3_core.cpp:145-146` | `B <- min(v3_isqrt(n), v3_isqrt(p), 16)`; `B_MAX = 16`, `check_B` | OK (n=200: ⌊√200⌋ = 14) |
| 8 | neighbour threshold | \|r̂_jl\| > √(2 log p / n); 1 to B neighbours before symmetrisation; 0.30 | `cpp/v3_blocks.h:146-172` | `rn = sqrt(2 log p / n)` (154); `above` counts `> rn` (166); `keep = min(B, max(1, above))` (167); symmetric union (170-171). 0.30 = √(2·ln 10⁴/200) = 0.3035 (shown to 2 d.p.) | OK |
| 9 | start-mode enumeration cap | 10⁶, then tie-aware recursion | `cpp/v3_core.cpp:469`; `cpp/v3_start.h:271-305` | `start_mode(st, 1000000, o.ls0_tie_dp)`; `cap = 1000000` default and `mode_tie_dp` on truncation (303) | OK |
| 10 | exact-case threshold | enumerate if \|Ω\| ≤ (5Nc₀+4N₀)p; 5.0×10⁸ | `cpp/v3_core.cpp:71-85`; `v3_fit.R:105-106` | `thr = (5*H0 + 4*N0) * p` (line 75); `exact_branch = !saturated` (84); `v3_fit.R:105-106` is the branch decision. Example: H0 = 2048, N0 = 10⁴ ⇒ thr = 5.024×10⁸ | OK |
| 11 | global certificate margin | 64 machine epsilons × conditioning factor; heuristic | `cpp/v3_score.h:240-246`; `cpp/v3_core.cpp:560-567` | `error_bound`: `64 * eps * (...)`, comment "documented heuristic"; `certified = (status == "exact") && (hpmF - hpm_eta > runner_up)` (563); `hpm_error_bound_kind = "heuristic (not a validated interval…"` (566) | OK |
| 12 | islands | 4 | `v3_run.R:91` | `islands = 4L` | OK |
| 13 | particles per island (N_i) | 4^i max(2500, n, p); 10,000 / 40,000 | `v3_preprocess.R:25,30` | `N0 <- max(2500, n, p)`; `tiers: N = c(N0, 4*N0)` | OK |
| 14 | burn-in rounds (L_bi) | max(4, ⌈log₂(n+1)⌉); 8 | `v3_preprocess.R:24` | `L <- max(4, v3_ceil_log2(n + 1))`; ⌈log₂ 201⌉ = 8 | OK |
| 15 | measured rounds | 4 | `v3_run.R:90`; `v3_calib.R:12` | `measured_rounds = 4L`; `Hm = 4L` | OK |
| 16 | resampling | multinomial, every step | `cpp/v3_engine.h:230-259` (resampler), `:316-327` (use) | "Multinomial resampling" at 230; returns `a` at 258; use `resample(lw)` at 324 inside the final-bridge loop 316-327 | OK |
| 17 | moves per round | p inclusion updates, 1 uniform swap, B neighbour swaps, 1 independence move; 10,016 | `cpp/v3_engine.h:111-214` | `one_round`, m = p + B + 2 labels (comment 201; lines 208-211: gibbs `lab < p`, `uswap` `lab == p`, `nswap` `lab <= p+B`, `indep`). 10,000 + 1 + 14 + 1 = 10,016 | OK |
| 18 | calibration particles (Nc_i) | 4^i ⌈512 N₀/2500⌉, N₀ := max(2500,n,p); 2,048; 8,192 | `v3_preprocess.R:26,30` | `H0 <- (512 * N0 + 2499) %/% 2500` (exact integer ceiling); `H = c(H0, 4*H0)` | OK |
| 19 | step ceiling (T_i) | 4^i max(1000, ℓ_n²); 1,000; 4,000 | `v3_preprocess.R:27,30` | `T0 <- max(1000, ell^2)`; `T = c(T0, 4*T0)` | OK |
| 20 | tiers | i ∈ {0,1}, factor 4^i, at most one move to tier 1 | `v3_preprocess.R:30`; `v3_calib.R:150-159` | tier table (30); `repeat` loop with `e <- 1` "one escalation at most" (150-159) | OK |
| 21 | pilot ESS target | 0.90 Nc_i; 1,843.2 | `cpp/v3_calib.h:31` | `const double thr = 0.90 * H` (0.9 × 2048 = 1843.2) | OK |
| 22 | pilot step floor | 1/T_i; 0.001 | `cpp/v3_calib.h:38-43` | `lo - phi < 1.0 / Te` → floor step (38-43) | OK |
| 23 | grid target | ρ ≥ 0.90 | `cpp/v3_calib.h:79,84,92` | `rb >= 0.90` (79), `>= 0.90` (84), `!(rv >= 0.90)` (92) | OK |
| 24 | bisections | 60 | `cpp/v3_calib.h:34,82` | `for (int i = 0; i < 60; ++i)` at both lines | OK |
| 25 | candidate set V | ∅, best 20p by γ₀, best 20p by F; up to 400,001 | `cpp/v3_core.cpp:699-724`; `cpp/v3_ledger.h:78` | `cpp_cal_V` unions `{∅}`, `lead0`, `lead1`; ledger `lead0.init(20*p, false); lead1.init(20*p, false)`. 1 + 2·20p = 400,001 (the comment at 699 says "top 20p by log γ₁"; the table's "by F" matches the ledger's ordering key as the manuscript defines it) | OK |
| 26 | rebuild iterations | ≤ ℓ_n; 14 | `v3_calib.R:84-119` | `for (it in seq_len(cs$ell))` (85), `ell = b$ell` | OK |
| 27 | triggers E1, E2 | gap 1 in log score; s.d. 1 of log Ẑ_r | `v3_calib.R:101-102` | `E1 <- any(island_best < best_after_local$F - 1)`; `E2 <- sd(log_Z_r) > 1` | OK |
| 28 | diagnostic islands per rebuild | 4 | `cpp/v3_core.cpp:664` | `List isl(4)`; loop `r = 1..4` (666) | OK |
| 29 | snap to ξ = 1 | within 10⁻¹² | `cpp/v3_calib.h:42,89` | `f >= 1.0 - 1e-12` (42); `v >= 1.0 - 1e-12` (89) | OK |
| 30 | grid fallback | on | `v3_calib.R:120-125,163-169`; `v3_fit.R:151` | fallback grid recorded (120-125), applied (163-169); `grid_fallback = isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))` | OK |
| 31 | base move cap (ℓ_n) | ⌈log₂(n+p+1)⌉; 14 | `v3_preprocess.R:23` | `ell <- v3_ceil_log2(n + p + 1)`; ⌈log₂ 10201⌉ = 14 | OK |
| 32 | move cap from the start mode | ℓ_n + \|S̃₀\| | `cpp/v3_core.cpp:473`; `v3_run.R:100-101` | `cap_ll = o.ls0_ell + (o.ls0_cap_plus_mode ? m.S.size() : 0)`; `ls0_cap <- "ell_n_plus_mode"` default | OK |
| 33 | search from the start mode | on | `v3_fit.R:73`; `cpp/v3_core.cpp:460-481` | `ls0 = getOption("v3.ls0", TRUE)`; the LS0 block | OK |
| 34 | pooling of islands | equal weights | `v3_run.R:154,162` | `log_Z <- log_sum_exp(logZr) - log(R)`; `pip_primary <- rowMeans(P)` | OK |
| 35 | estimated MPM threshold | PIP-hat_j > ½ | `v3_run.R:163` | `mpm <- orig[pip_primary > 0.5]` | OK |
| 36 | stored models | best 40p+1 by F; 400,001 | `cpp/v3_ledger.h:78` | `top.init(40 * p + 1, true)` | OK |
| 37 | evidence lower bound | 0.05 Ẑ | `v3_run.R:155` | `log_Z_lower95 <- log(0.05) + log_Z` | OK |
| 38 | low-ESS flag | below 0.5N at some step; 5,000 | `v3_run.R:201` | `any(stage_table$ess < 0.5 * ro$N)` | OK |
| 39 | near-tie window | 10⁻⁹ in log score | `v3_run.R:171` | `top$value >= out$hpm_F - 1e-9` | OK |
| 40 | allocation defaults | 8 GiB (8·2³⁰ bytes), 24 h | `v3_fit.R:28,47,60,73,92` | `mem_gb %\|\|% 8, hours %\|\|% 24` (28, 92); `mem_gb * 2^30` (47, 60); `allocation = list(mem_gb = 8, hours = 24)` (73) | OK |
| 41 | score cache | 500p models, cleared when full; 5×10⁶ | `v3_run.R:92`; `v3_calib.R:147` | `cache_capacity = 500 * p` at both | OK (clear-when-full is not in these lines; it is the cache's behaviour, unverified here) |
| 42 | check before the run | memory; exact: 200 timed scores × count; sampler: 2(ℓ_n+K+1)(p+p²/4) × time of a size-K score; 2.9×10⁹ | `v3_fit.R:10-14,26-68,114-117,144-148` | `cpp_time_scores(…, 200)` (13); `ls0_requests <- ls0_scans * (p + p^2/4)`, `ls0_scans <- ell + K + 1` (44); `ls0_seconds <- 2 * ls0_requests * ls0_s` (47). Example: 115 × 25,010,000 = 2.876×10⁹ | OK |
| 43 | random streams | 0–4 (tier 0), 5–9 (tier 1), 10–13 (final) | `v3_run.R:8-11`; `cpp/v3_core.cpp:444,626,667` | `stream_map` 0:13 with the phases (8-11); `seed_stream(seed, 9 + r)` for final r = 1..4 (444); `sid = tier == 0 ? 0 : 5` (626, 667) | OK |
| 44 | seed | integer in [1, 2³¹−1] | `v3_preprocess.R:7-11` | `seed < 1 \|\| seed > 2^31 - 1` | OK |
| 45 | ceiling on the base move cap | ℓ_n ≤ 10⁶, else error | `v3_run.R:96` | `le > 1e6` ⇒ `stop(...)`; `le` defaults to `b$ell` | OK |
| 46 | integer range of the move cap | ℓ_n + \|S̃₀\| ≤ 2³¹−1, else error | `cpp/v3_core.cpp:474` | `cap_ll > numeric_limits<int>::max()` ⇒ `stop("LS0 move cap out of range")` | OK |

**Result for `tab:params-full`: 46 of 46 rows OK; 0 wrong, 0 moved.**

### B2. `tab:params` (`s3_method.tex:223-245`)

The table has no code pins; its values were compared with B1 and with the lines above.

| Row | Value in `tab:params` | Matches |
|---|---|---|
| size cap K; 100 | min(p, ⌊n/2⌋) | B1 #1 |
| model prior w(k) | ½/C(2p−1,k), renormalised to Ω | B1 #2 |
| g; ridge; 200 | n; unit ridge | B1 #3 |
| a₀, b₀ | 0.01, 0.01 | B1 #4 |
| block size cap B; 14 | min(⌊√n⌋, ⌊√p⌋, 16) | B1 #7 |
| particles N_i; 10⁴; 4·10⁴ | 4^i max(2500, n, p) | B1 #13 |
| burn-in L_bi; 8 | max(4, ⌈log₂(n+1)⌉) | B1 #14 |
| exact-case threshold; 5.0×10⁸ | (5Nc₀+4N₀)p | B1 #10 |
| base move cap ℓ_n; 14 | ⌈log₂(n+p+1)⌉ | B1 #31 |
| move cap from the start mode | ℓ_n + \|S̃₀\| | B1 #32 |
| returned list T; 400,001 | best 40p+1 by F | B1 #36 |

**Result for `tab:params`: 11 of 11 rows OK.**

### B3. The requested hyperparameters, with file:line

| Hyperparameter | Value | Where (file:line) |
|---|---|---|
| K = min(p, ⌊n/2⌋) | 100 at (200, 10⁴) | `cpp/v3_score.h:40`; `v3_preprocess.R:21`; also `cpp/v3_core.cpp:74` (exact count) |
| w(k) = 1/(2·C(2p−1,k)), i.e. BB(1,p) | per-model weight | `cpp/v3_score.h:65` (`logw`), renormalisation over sizes ≤ K at `:68`, `:70` |
| g = n, unit ridge; slab N(0, nσ²(G_S+I)⁻¹) | | `cpp/v3_score.h:175-183` (`H = (n+1)G_S + I`, `A = G_S + I`); no literal `g = n` and no explicit slab covariance line in the code; the slab form is the manuscript's reading of H and A |
| σ² ~ IG(0.01, 0.01) | a₀ = b₀ = 0.01 | `cpp/v3_score.h:14`; the normalising constant `logCn` at `:59` |
| N₀ = max(2500, n, p) | 10⁴ | `v3_preprocess.R:25` (tier table `:30`) |
| B = min(⌊√n⌋, ⌊√p⌋, 16) | 14 | `v3_preprocess.R:22`; hard cap `cpp/v3_core.cpp:145-146` |
| L_bi = max(4, ⌈log₂(n+1)⌉) | 8 | `v3_preprocess.R:24` |
| ℓ_n = ⌈log₂(n+p+1)⌉ | 14 | `v3_preprocess.R:23` |
| returned list 40p + 1 | 400,001 | `cpp/v3_ledger.h:78` |
| exact-case threshold | (5·H₀ + 4·N₀)·p | `cpp/v3_core.cpp:75` (formula), `:71-85` (function); branch decision `v3_fit.R:105-106` |
| ESS 0.90 | pilot target 0.90·Nc_i | `cpp/v3_calib.h:31` |
| four islands | final: 4; diagnostic: 4 | `v3_run.R:91`; `cpp/v3_core.cpp:664` |
| tier multiplier 4 | N, H, T all ×4 at tier 1 | `v3_preprocess.R:30` (`c(N0, 4 * N0)`, `c(H0, 4 * H0)`, `c(T0, 4 * T0)`) |
| 8 GiB / 24 h defaults | `mem_gb = 8`, `hours = 24` | `v3_fit.R:28`, `:73`, `:92` |

All 14 hyperparameters verified. The calibration particle count Nc₀ appears in the code as `H0` (`v3_preprocess.R:26`); the manuscript's name for it is Nc.

### B4. Remarks (all cosmetic; no value is wrong and no pin has moved)

1. **Stale comment at `cpp/v3_core.cpp:144`.** It reads "Block width supported by the table codes … 1 <= B <= 20 (code review R-6)", while the enforced limit at `:145-146` is `B_MAX = 16`. The manuscript cites `:145-146` and says 16, which is correct. The queue already carries this as an Engineering item (QUEUE:67). It matters only if a reader opens line 144.
2. **The `g = n` pin is derived.** `cpp/v3_score.h:175-183` shows `H = (n+1) G_S + I` and `A = G_S + I`; the prior scale `g = n` and the slab covariance nσ²(G_S+I)⁻¹ are the manuscript's reading of those matrices (g·G_S + G_S + I is the posterior precision for g = n). There is no line in the code that states `g = n`. If the manager wants a pin that names it, the header comment of `v3_score.h:1` points to CORE_SPEC v2 §2 / M §5, not to a code line.
3. **The exact-case threshold pin is two-part.** `tab:params-full` cites `cpp/v3_core.cpp:71-85; v3_fit.R:105-106`. The formula `(5*H0 + 4*N0) * p` is at `cpp/v3_core.cpp:75`; `v3_fit.R:105-106` is only the branch decision (`exact_branch` → "exact"/"smc"). Both are correct; a reader looking for the threshold on `v3_fit.R:105-106` will not find the number there.

All example-column values reproduce at the shown precision: 100, 200, 14, 10,000/40,000, 8, 0.30 (0.3035), 5.0×10⁸ (5.024×10⁸), 14, 400,001, 2,048/8,192, 1,000/4,000, 1,843.2, 0.001, 10,016, 5,000, 2.9×10⁹ (2.876×10⁹).

Not verified by reading code (flagged, not wrong): "cleared when full" for the score cache (row 41), and the lines of `v3_run.R`/`v3_fit.R` for the "Runs without estimates" paragraph (`appendices.tex:120-128`), which are outside the two tables.
