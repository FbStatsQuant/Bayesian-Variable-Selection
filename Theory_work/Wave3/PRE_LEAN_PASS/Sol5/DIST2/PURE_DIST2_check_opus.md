# PURE check: W3-DIST:DIST-2 delta after R1 (Opus seat)

All four checks pass. The staged ticket is exactly the pre-R1 ticket with the five R1 Old/New pairs applied. No span, premises span or `claim_hash` changes, and the new text adds no claim.

**Manifest verify:** I built a scratch git repo at `<worktree>/.rc_tmp/pure_dist2_opus/verify/`. It holds the 4 files named in `MANIFEST_DIST2_EXT.txt`, copied from the clone at 330b87b4, and `Sol5/DIST2/ticket/` at the same relative path. Running `python3 <worktree>/Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/Sol5/DIST2/ticket MANIFEST_DIST2.txt` printed `verify: OK MANIFEST 578913a683b89917ce47c838cca376e497699b5d5d5c4f665773bb96128f7962`, exit 0.

## (1) The R1 pairs, applied by script, give the staged files exactly

- **Script:** `<worktree>/.rc_tmp/pure_dist2_opus/apply_r1.py`. It parses `R1_council_opus.md` §2 and extracts the `Replace:`/`With:` code spans of F1, E1, E2 and E3.
- **Pairs found:** exactly 5, in the order F1, E1, E2, E3, E3. F1 is in `TARGET.md`; the others are in `STATEMENT.md`.
- **Matching:** each Old string was matched whitespace-flexibly in the pre-R1 ticket `ticket_R1/ticket`.
  - Every Old string matched exactly once, and each also matched exactly, not only flexibly.
  - Where they matched: F1 at `TARGET.md:30`, E1 at `STATEMENT.md:1`, and E2, E3a and E3b at `STATEMENT.md:497`.
- **Result after replacement:**
  - `STATEMENT.md` is byte-identical to the staged file. Lines go 500 → 500, and only lines 1 and 497 changed.
  - `TARGET.md` is byte-identical to the staged file. Lines go 214 → 214, and only line 30 changed.
- **Pre-R1 ticket equals the batch tree:** `cmp` shows the pre-R1 ticket's two files are identical to the clone's `Theory_work/Wave3/W3-DIST/{STATEMENT,TARGET}.md`.

## (2) Spans and claim hashes are unchanged

- **Script:** `<worktree>/.rc_tmp/pure_dist2_opus/hashes.py`. It imports the clone's `bvsreg` without writing bytecode. For the patched tree it swaps in a wrapped `read_lines` that serves the patched copies of the two files.
- **Scope:** `claim_hash` was computed for all 553 rows of `claims.tsv`, on the batch tree and on the patched tree.
- **Rows with a changed hash:** none.
- **The 20 rows whose file or premises name W3-DIST `STATEMENT.md`:** these are DIST-1, DIST-2, DIST-3, DIST-C, Thm-A, Thm-B, Cor-C, H, T, S, V, X, X′, NEC, P6, B0, B1, B2core, B2 and B3. For every one, the registered sha256 equals the batch hash and equals the patched hash. For DIST-2 that value is `7de66dbc…`.
- **DIST-2's own text:** span 93-98 and premises span 17-70 are identical line by line.
- **Why nothing moves:** the highest registered end line in that file is 414. Lines 1 and 497 lie outside every span, and no claim's file or premises point to `TARGET.md`.

## (3) The patch applies to the batch tree and to a scratch copy

- `git -C <clone> apply --check -v DIST2_R1_stage.patch` exited 0 for both files. This was a check only and wrote nothing.
- `patch -p1 -F0` on a scratch copy at `.rc_tmp/pure_dist2_opus/ptree/` exited 0, with no fuzz and no offset reported.
- The patched files are identical (`cmp`) to the staged ticket, at 500 and 214 lines.

## (4) The new texts add no claim, and the constants pointers are right

**E2:** the quoted text in row 1.4.11, minus its closing `; …)`, appears verbatim in `STATEMENT.md:97`. The part the `…` stands for is exactly :97's own pointer `` `lemmas/X.md` §9, `lemmas/DIST12.md` D.6) ``.

**F1:** the new `TARGET.md:30` DIST-2 cell says the same as `:96-97`, with no addition. It contains all eight elements of :96-97:
- "for fixed s₀^r"
- the rate log n·ℓ_n/n
- "(1 + s₀^r)³"
- "for fixed (A, σ*², M, M′)"
- "upper bound"
- "not known to be tight"
- "as proved"
- the same two pointers

The new qualifier "for fixed (A, …)" only narrows the statement. "Not known to be tight" makes no mathematical claim.

**E3a:** this is the reason given for DIST-1 being unaffected, that its radius constant C = (C_X² + C_X/2 + 1 + C_T)^{1/2} does not depend on s. The sources support it:
- C is defined in `DIST12.md` D.4 at :56 and summed at :59.
- D.4 :67-68 states that C_X and C are free of s, citing `X.md` §0 v0.4.
- `X.md` §0 states that C, Lemma X's constant (called C_X in D.4), does not depend on s.
- `DIST12.md` D.1 :35 gives C_T := 4[34(A+7)+8], "which does not depend on s".

**E3b:** each pointer names the right place.
- `X.md` §0 :34 defines C_m := 2s + 1 + (s(A+2)+5)/log 2, which is linear in s.
- `X.md` §9 (:197-221) gives C_P′, C_x′, Λ′, C_Q′, C_v′, C₁′, C = max{C₁′, C_v′} and M₀′ = max{16, (A+1)s}.
- `DIST12.md` D.1 :36 defines C_T′ := 4[(A+7)(s+1+C_m)+8].
- `DIST12.md` D.6 (:83-90) gives C₂² = C_{X′}² + 1 + C_{X′}/2 + C_T′.
- "give only an upper bound of order (1 + s₀^r)³" only narrows the earlier "give (1 + s₀^r)³".

**E1:** the header now reads `v1.4.11, 2026-11-18`, which matches the last changelog row.

## Hygiene

- The worktree has no tracked changes, and I committed nothing and started no subagents.
- The clone is still at 330b87b4. Its only change, `M Theory_work/Wave3/W3-START2-R/reviews/CITECHECK.txt`, was already there before this seat started (my first `git status` showed it) and is not mine.
- No `__pycache__` was written into the clone.
- All scratch is in `<worktree>/.rc_tmp/pure_dist2_opus/`, with nothing in /tmp.

PURE-VERDICT: PURE
