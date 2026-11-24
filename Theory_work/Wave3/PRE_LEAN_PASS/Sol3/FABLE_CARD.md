# Sol-3 Fable card: W3-D2 (`Thm2X`, `Cor2X`) and W3-D3 (`B3w`, `ExSG`, `Thm2SG`) final text

Sol 6.2: all five claims ACCEPT; Sol's own R1 findings FIXED; D2 9.3 PASS (manifest f76e9dec), D3 9.1 PASS (manifest dff18ca9). Snapshot: `origin/theory/PRE-LEAN` 6850c3a5.

**Verdict:** both tickets confirmed. The three points are stale status or dependency wording in a proof header, a report line and the reader's bridge table. No claim, no recorded statement and no step of a proof is affected.

## Rulings

| Point | Ruling | (a) Kind | (b) Recorded STATEMENT affected? | (c) Exact fix |
|---|---|---|---|---|
| **S3b-2** reader B2.2 row: "Theorems 2, 6 and 10 depend on it" | AGREE on the fact; **reclassify from FLAW to stale dependency wording** | Wording: it claims a dependency the presented Theorem 2 no longer has. Not a mathematical flaw. | No (reader bridge table, `READER_VERSIONS.md:301`) | Replace "Theorems 2, 6 and 10 depend on it; Theorem 4 does not" by "Theorems 6 and 10 depend on it, as did the previous Gaussian proof of Theorem 2 (the presented Theorem 2 uses B2.2′ instead); Theorem 4 does not". |
| **S3b-1** `W3-DIST:B3` listed among checked inputs without its qualifier | AGREE | Status misquote by omission; no mathematical effect | No (reader "Master theorem" paragraph `:295`; `W3-D3/REPORT.md:42`) | Reader `:295`: replace "`W3-DIST:B0/B1/B2core/B2/B3@1.0.2`" by "`W3-DIST:B0/B1/B2core/B2@1.0.2` (and `W3-DIST:B3@1.0.2` as the proof template of B3w only; its last sentence, conditional on `W3-POST:Thm-1`, is not used)". `REPORT.md:42`: take B3 out of the "all PROVED-CHECKED" group and add "`W3-DIST:B3` is the proof template of B3w only". |
| **S3a-1** `W3-D2/PROOF.md:3` header lists the conditions of `CorGb-plus@1.0.1` | AGREE | Stale status header; the registry status and STATEMENT §5 are right (conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P) | No (proof-file header) | Replace "(conditions carried from `W3-MISR-R:CorGb-plus@1.0.1`, STATEMENT §5)" by "(the list carried from `W3-MISR-R:CorGb-plus@1.0.1`, historical; the active conditions, at `CorGb-plus@1.0.3`, are W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P: STATEMENT §5)". |

Notes:
- **S3b-2.** The reader's own next row already says B2.2′ (`W3-D3:B3w`) "replaces B2.2 for the presented statement; B2.2 stays for the Gaussian case". The presented Theorem 2 reaches `W2-APP` only through Theorem 1 item 6, whose proof cites the diagonal step of `L1_POST.md`, not the Gaussian-row events of part (a). The stale sentence errs on the safe side (it names a dependency that is PROVED-CHECKED anyway).
- **S3b-1.** `W3-D3/STATEMENT.md:154-157` already has it right: B3 is "the template of Lemma B3w" and "its last sentence, δ_n → 0, is not used".
- **Link to my T5 card (R3).** The measurability slip in B3's amendment A-2 does not reach B3w: part (c) of B3w defines its event on the completed pair, which is the corrected construction.

## Process

- Reader edits (S3b-1, S3b-2) join the single reader touch already needed for Sol-2, T4 N1 and T5 R4.
- `W3-D3/REPORT.md` and `W3-D2/PROOF.md` are in their tickets' manifests, so each edit needs a CITATION-ONLY re-freeze. Neither is urgent; I would apply them only when those tickets are next opened.
