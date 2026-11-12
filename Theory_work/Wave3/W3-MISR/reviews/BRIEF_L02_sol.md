# BRIEF L02 — statement-lock re-check (reconciliation of L01), seat: Sol (codex gpt-6.1-sol, reasoningEffort high)

You are a fresh, independent reviewer. A first statement-lock review (L01) of a mathematical statement found 1 MAJOR and
3 MINOR problems; the author changed the statement (v1.0 → v1.1). Your job: decide, finding by finding, whether each
problem is really resolved, and whether the changes introduced anything wrong. Be adversarial. No proofs exist yet.
Repository root = your working directory. Read-only, except the one output file. No git changes. No subagents.

## Read
- `Theory_work/Wave3/W3-MISR/reviews/L01_statement_lock_sol.md` (the findings) and
  `Theory_work/Wave3/W3-MISR/reviews/L01_disposition.md` (what the author says was changed).
- `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.1). The previous version: `git show 197f557:Theory_work/Wave3/W3-MISR/STATEMENT.md`;
  the diff: `git diff 197f557 -- Theory_work/Wave3/W3-MISR/STATEMENT.md` (read-only git commands are fine).
- Inputs as needed: `Theory_work/Wave1C/C-MIS/STATEMENT.md` (Theorem F, lines 122-146; GR, lines 52-58),
  `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L4_theoremF}.md`, `Theory_work/Wave3/W3-POST2/STATEMENT.md`,
  `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`, `Theory_work/Wave3/W3-POST/STATEMENT.md`,
  `Theory_work/Wave3/W3-MISR/numerics/N0_code_invariance.R`, `numerics/N0_out.txt`, code under `Scripts/SMC_BVS/core/`.
Do not read other files under `reviews/`, nor LOG/PLAN/CHECKPOINT files.

## Tasks
1. For each L01 finding 1–4: RESOLVED / PARTIALLY / NOT RESOLVED, with file:line evidence in v1.1.
   - Finding 1 (Remark P, Theorem F): go through **every** hypothesis and conclusion of C-MIS Theorem F, Corollary F(a),
     F(b) and check that under y ↦ y/σ_n each one is either invariant or is now explicitly stated in relative form.
     Is anything variance-dependent still unnormalised (e.g. the definition of Δ_n, σ²_{𝒞,n} ∈ [σ², σ² + 2M], R^𝒞,
     the changed-steps list)? Do the same for C-MIS Theorem MIS (i), (ii), (ii′) and for Remark SNR's list.
   - Finding 2: is the new (a″) text accurate about what `N0_out.txt` shows (numbers, branches, number of data sets)?
   - Finding 3: is the new "reference law" paragraph of §6 correct in every sentence (the law under GR; the variance
     of (Cy^r)_i; the KL statement in the Gaussian-row setting; what is not claimed)?
   - Finding 4: is the (OS) bridge now stated with the right onset and constant dependence?
2. Check every other changed line of the diff for new errors (the "Conventions" bullet, Corollary G(b), Remark U).
3. Say whether you see any remaining FATAL or MAJOR problem anywhere in STATEMENT.md v1.1.

## Output
Write `Theory_work/Wave3/W3-MISR/reviews/L02_statement_recheck_sol.md`: a verdict per L01 finding, any new findings
graded FATAL / MAJOR / MINOR / NIT with file:line evidence and a required change, and one line
`VERDICT: LOCK | LOCK-WITH-CHANGES | REJECT` (LOCK-WITH-CHANGES only if all remaining items are MINOR/NIT).
Final message: the verdict and counts per grade.
