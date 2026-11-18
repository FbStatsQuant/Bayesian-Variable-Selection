# BRIEF R4 — Opus check of the R3 → R3r record correction, ticket W3-D5P — Opus (Claude Opus 5.5, effort high, Claude Personal); fresh

HQ-approved single seat. You have never reviewed this ticket and did not author its R3r patch. Work read-only in
`/home/fb31/BVS-wt/W3-D5P` (paths relative to it); **write, create or delete nothing anywhere**; do not change git state.
Do not read `LOG.md`, any `CHECKPOINT_*`, or files under `reviews/` other than those named here.

## What is frozen
`reviews/MANIFEST_R3r.txt`, digest **64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890**; `python Theory_work/Wave3/tools/manifest.py verify
Theory_work/Wave3/W3-D5P Theory_work/Wave3/W3-D5P/reviews/MANIFEST_R3r.txt` must pass on what you read. It differs from
the previous council manifest `reviews/MANIFEST_R3.txt` (35a027be…, where all three claims were accepted) only in
REPORT.md, DEPS.tsv and the new ERRATA.md.

## Scope (only this)
The R3 → R3r diff: `reviews/R3r_correction.patch` (applied in the frozen state). It changes
(1) the REGISTRY blocks of `REPORT.md` §5 (record format for the registry tool: conclusion level tags, LIST-R assumption
ids, method lines, an assumption-list marker); (2) the `DEPS.tsv` LIST-R row (checked_sha / state); (3) the new
`ERRATA.md` rows E1–E3 (editorial notes, not applied to the claims).
Check that each change is faithful to `STATEMENT.md` (v1.1.2; claims (C1) LIST-K, (C2) LIST-CODE, (C3) LIST-R) and does not
assert more, or less, than STATEMENT and the proofs (`lemmas/L1–L3`) support: in particular that the LIST-R assumption ids
are exactly those of its master W3-RM2-R:RM2-R-plus (registry row, verbatim: "A:LSF; A:IID-GAUSS-ROWS; A:RM-FLR; A:PTV;
A:RM2-LFEAS; A:RM2-LGAIN-R; A:RM2-LLOC-R; A:RM2-LSIZE-B-R; A:RM2-HSIZE-RHO; A:RM2-W-R; A:OP; A:BLOCK-LE-16;
A:DELIV-D") plus A:EX-A and the new A:IMPL-LIST as STATEMENT §1 states it; that conclusions, rates, scopes, statement and
premise line pointers match STATEMENT; that the DEPS row's hashes are those of the files; and that the ERRATA rows are
editorial (they change no claim).
**Acceptance filter.** Report **genuine flaws only** (C: wrong or unproved; S: claims more than proved or an unstated
hypothesis; F: unfaithful to STATEMENT, the proofs, a cited source or the code); no nitpicks, no wording preferences.
**IMPL-LIST.** LIST-R stays conditional on IMPL-LIST (the pending method commit); you are not asked to discharge it.
**Binding rule: you MUST give `gates=FAIL` if you hold any C, S or F finding of your own.**

## Reply format
1. Per-claim table `| id | decision |` (ACCEPT / REJECT) for W3-D5P:LIST-R, W3-D5P:LIST-K, W3-D5P:LIST-CODE.
2. Genuine findings (file:line, C/S/F, fix) or "none". 3. Score 0.0–10.0 (C, S, F only).
4. The verdict line below, exactly once.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890` (round R4, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R4 manifest=64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890 seat=opus score=<x.y> gates=PASS|FAIL
```

- `gates=PASS` only if every gate passes on exactly this manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
