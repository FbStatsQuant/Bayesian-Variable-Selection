# Brief — Sol diff check of the W3-MISR Cor-H KL narrowing (v4: statement change by an OpenAI reviewer)

Prepared 2026-11-16 04:23 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5). Reviewer: gpt-6.1-sol, reasoning high.

## Rules
- You are a **fresh, read-only** reviewer. Do not edit any file except your one reply file below. Do not commit to, or touch,
  any other worktree; do not change the registry; do not apply the patch to the real file.
- **D62 (verbatim):** "Do not write any file outside the worktree and set no TMPDIR. Scratch only in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end."
- Write your reply to `Theory_work/Dept/research/MISR_NARROW/DIFF_sol.md` (inside your worktree). Last line:
  `DIFF: PASS` or `DIFF: FAIL` (FAIL only for a concrete defect, with a concrete repair).

## Inputs (read these; nothing else is needed)
1. **The patch:** `Theory_work/Dept/research/MISR_NARROW/STATEMENT_W3-MISR_v1.1.0.patch` — a unified diff against
   `Theory_work/Wave3/W3-MISR/STATEMENT.md` as on origin/main (`git show origin/main:Theory_work/Wave3/W3-MISR/STATEMENT.md`).
   It changes line 1 (version/changelog header, in place) and rewraps lines 191-195; line count 272 → 272.
2. **The original claim span** W3-MISR:Cor-H@1.0.0 = `Theory_work/Wave3/W3-MISR/STATEMENT.md:178-197` (origin/main); also
   read Corollary G's setting `:162-174` and the standing convention `:36-43` (in particular `:38`: "the intercept may be
   random and dependent on everything"). The proof of the sentence: `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:88-93`.
3. **The counterexample:** `/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/reviews/L1_statement_lock_sol.md:7`
   (finding L1-1; re-confirmed as K1-1 in `.../reviews/K1_linecheck_sol.md`), verdict
   `/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/reviews/post_cp3/BASE_KL_VERDICT.md`.
4. **The rider's council-passed wording** (v1.1a): `/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:123-131`,
   especially "For jointly Gaussian rows as in (E1), with a deterministic intercept α (and the deterministic parameters of
   that example), this also gives BASE's row-wise reading (SL's f₀, centred rows) [L1-1]."

## The change (for convenience; the patch file is authoritative)
Old `:191-195`:
```
interpretation. **Kullback–Leibler reading, in the setting of Corollary G only:** there the conditional law of y_i
given the candidate covariates x_{𝒞,i} (omitted covariates integrated out) is N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞), which belongs to
the candidate linear-Gaussian class and is therefore the Kullback–Leibler minimiser within it (SL's f₀, for centred
rows); the reference is that law with its mean centred over the sample. No KL statement is made for fixed designs
or for the projection given the realised omitted columns ([MIS1] `L1_reduction.md:69-74` keeps these apart).
```
New `:191-195`:
```
interpretation. **Kullback–Leibler reading, in the setting of Corollary G with a deterministic intercept α (and the deterministic parameters of
that example) only [W3-MISR-R L1-1]:** there the conditional law of y_i given the candidate covariates x_{𝒞,i} (omitted covariates integrated
out) is N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞), which belongs to the candidate linear-Gaussian class and is therefore the Kullback–Leibler minimiser within
it (SL's f₀, for centred rows); the reference is that law with its mean centred over the sample. No KL statement is made for a random
intercept, for fixed designs or for the projection given the realised omitted columns ([MIS1] `L1_reduction.md:69-74` keeps these apart).
```
Line 1 gains: version `v1.3, 2026-11-12` → `v1.4, 2026-11-16` and the entry
"; v1.4 = Cor-H's Kullback–Leibler reading restricted to a deterministic intercept [W3-MISR-R L1-1]".

## Questions
(a) Is the patched text **true** under Corollary G's setting as written (random intercept allowed by `:38`, `:164-165`)?
    I.e. once restricted to a deterministic α (and deterministic parameters), is the row-wise conditional law
    N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞) correct, is it in the candidate linear-Gaussian class, and is "KL minimiser within it (SL's f₀,
    for centred rows)" right? Is the added disclaimer "No KL statement is made for a random intercept" accurate?
(b) Does the patch change **anything beyond restricting the reading**? Check that no hypothesis or conclusion of Cor-H's
    display (`:178-186`), of the reference-law paragraph (`:187-191` up to "interpretation."), or of `:196-197` changes,
    that no other line except line 1 changes, and that line 1's edit is a changelog entry only.
(c) Changelog tag: **WEAKER** (an interpretive sentence narrowed; no display changed) — agree? If not, which tag and why.
(d) Anything else that makes the patch unfit to apply (wording ambiguity, the tag `[W3-MISR-R L1-1]` resolvability, wrap).

Answer each with a verdict and a short reason; end with the single line `DIFF: PASS` or `DIFF: FAIL`.
