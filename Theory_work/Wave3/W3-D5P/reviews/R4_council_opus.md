<!-- Council round R4 (HQ-approved single seat), seat opus: Claude Opus 5.5, effort high, Claude Personal (fresh); brief reviews/BRIEF_R4_opus.md; MANIFEST_R3r 64a3ec05…; one call; reply below verbatim -->
I found no genuine C, S or F flaws in the R3 → R3r correction. All three claims are accepted at 9.6, and the gates pass.

**Procedural slip:** the brief said to create no files anywhere, but I wrote one temporary file outside the repo: `/tmp/claude-71711/-home-fb31-BVS-wt-THEORY-DEPT/7960a8bd-ea71-45a2-84ff-4dc0ae46d090/scratchpad/gd.txt`. It holds a diff, created by a shell redirect so I could compare the patch against `git diff`. Nothing in the repository, its files or its git state was touched, and the reviewed content is unaffected. It can be deleted.

**Integrity checks**
- `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-D5P Theory_work/Wave3/W3-D5P/reviews/MANIFEST_R3r.txt` printed `verify: OK MANIFEST 64a3ec05…6c1890`.
- `MANIFEST_R3r.txt` differs from `MANIFEST_R3.txt` (35a027be…) only in DEPS.tsv, the new ERRATA.md and REPORT.md. The R3 REPORT at a2c465a4 hashes to e26a811c…, which matches the R3 manifest.
- `git diff a2c465a4 HEAD` on REPORT.md, DEPS.tsv and ERRATA.md gives exactly the lines of `reviews/R3r_correction.patch`; only the file order differs.
- The core of record is unchanged: `git diff 4676af6 main -- Scripts/SMC_BVS/core` and `git diff 4676af6 HEAD -- Scripts/SMC_BVS/core` are both empty. So "production core on main = 4676af6" is true.

**(1) REGISTRY blocks (REPORT.md §5)**
- **LIST-R assumptions (REPORT.md:65):** the 13 ids from `A:LSF` to `A:DELIV-D` match the master row `W3-RM2-R:RM2-R-plus` (`INFRA/registry/claims.tsv:519`) exactly, in the same order. After them come `A:EX-A` and the new `A:IMPL-LIST`.
  - The IMPL-LIST item says the same thing as STATEMENT.md:59-61: computed as SPEC §2/§4 prescribe, from the returned list of the same run, and no other field or state changes. Its source pointer is STATEMENT.md:59-63, it is marked `shared no`, and the id is not already in `assumptions.tsv`. It matches the parser's grammar (`ingest.py:224-246`).
  - The record no longer says "(clause (iii) only)" after `A:DELIV-D`. The registry definition of `A:DELIV-D` (`assumptions.tsv:136`) already reads "for the unconditional clause only", so the scope of (D) is unchanged.
- **LIST-CODE assumptions (REPORT.md:52):** now `A:OP ; A:EX-A`.
  - The registry statement of `A:OP` covers EX-A, EX-S, SR, GUARD-W and OP-LS0. The registry has no finer id for EX-S or SR.
  - The shipped configuration that the old parenthetical mentioned is still recorded in `scope`.
  - The old parenthetical also named GUARD-W and OP-LS0, so the hypotheses are neither stronger nor weaker than in R3.
- **Conclusion level tags:** each tag is in `CONCLUSION_LEVELS` (`bvsreg.py:169`).
  - LIST-K is `identity`, which fits a deterministic list-algebra lemma.
  - LIST-CODE is `identity`, which fits a deterministic code fact. This is the lowest level, so it does not overclaim.
  - LIST-R is `reported-model`, the same tag as its master, which also carries its own (D) clause. It does not go above what STATEMENT (C3)(i)–(iii) proves.
  - The conclusion texts, rates and scopes are word-for-word unchanged from R3, which accepted them.
- **Method lines:**
  - LIST-CODE now reads `production core on main = 4676af6 | method_commit: 4676af6`. That matches the W3-SAMP:CC precedent and STATEMENT.md:15, and 4676af6 resolves to a commit.
  - LIST-R now has no `method_commit`, and its method line says the list fields' commit is pending. That is accurate: the old value "pending (…)" was not a commit and would have failed `ingest.py:451-452`. Leaving it empty has precedent (the W1-PXN rows). Pinning 4676af6 instead would have been false, because the list fields are not in that commit.
  - LIST-R still reaches the pinned core through `depends_on: W3-D5P:LIST-CODE@stmt`.
- **Pointers** all match STATEMENT v1.1.2:
  - statement spans 67-75, 79-95 and 99-125;
  - premises 39-47, 29-38 ; 49-57, and 29-63 (which includes IMPL-LIST);
  - `status_source` lines REPORT.md:17-19.

**(2) DEPS.tsv LIST-R row**
- `sha` and `checked_sha` are both 71642c061447ba57. That equals the sha256 prefix of `lemmas/L3_listR.md`, both raw and LF-normalised (the file has no CRLF).
- L3 has the same hash in MANIFEST_R3 (35a027be), which is the manifest the row cites as `checked_sha`, so marking the row `OK` is correct.
- The other DEPS hashes also match their files: STATEMENT 5dc11132…, L1 5c4c081b…, L2 b023cafb….
- I couldn't open the R3 review file (the brief limits which review files I may read). The "opus 9.4 PASS" in the row matches commit 21f0111f ("R3 PASS 9.4").

**(3) ERRATA E1–E3**
All three are proposals only and none is applied.
- **E1** changes L3 (0.5) wording. Delivery rests on the step at L3:33, where `finish` (`v3_fit.R:79-87`) does not branch on the clock. With |𝒯| ≤ 40p+1, the added work is far smaller than the LS0 scan envelope that (D) already allows for. So (C3)(iii) is unaffected.
- **E2** fixes a grammatical slip in CARD wording.
- **E3** concerns STATEMENT §5 remark 3. Remarks are "not part of any claim; not registered", and its proposed text is not applied.
- Because of the brief's read limits, I did not check the E1–E3 source citations against the cited review files.

### 1. Per-claim decisions

| id | decision |
|---|---|
| W3-D5P:LIST-R | ACCEPT |
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |

### 2. Genuine findings
None.

### 3. Score
**9.6**

`COUNCIL-VERDICT round=R4 manifest=64a3ec05e9dbb4e0ed609f5d15d6e14198c42a14ef3a553a36c03756ed6c1890 seat=opus score=9.6 gates=PASS`
