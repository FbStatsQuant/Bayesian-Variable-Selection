# W3-DIST — diff check D1 (re-check of a repaired lemma + statement-change check) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D1_sol_diff.md`.** Run no git command that changes state (read-only git is fine); start no agents; no cluster
jobs; any computation `nice`, small, on at most 2 cores. Any temporary file goes under
`/home/fb31/SMC_Theory_Department/tmp/20261115-W3-DIST-D1/` (never `/tmp`); remove it when done.

This is **not** a blind read: you are given the findings that triggered each change. Your job is to decide, change by
change, whether the edited text is correct and whether the proofs still prove the statements as they now read. Do not
re-review unchanged, already line-checked text except where a change touches it. Do not soften findings.

## Part A — re-check of the repair of finding L6-01 (the important part)

Finding: `reviews/L6_sol_DIST12.md` (L6-01, MAJOR). Lead's disposition: `reviews/L6_disposition.md`.
Diffs: the first two blocks of `reviews/DIFFS_D1.patch` (`lemmas/X.md` v0.3 → v0.4; `lemmas/DIST12.md` v0.1 → v0.2).
Current files: `lemmas/X.md`, `lemmas/DIST12.md`; statement: `STATEMENT.md` §1, Theorem DIST-1, consequence (c);
target clause: `TARGET.md` §5, TC3.

Check every line of the repair and try to break it:
1. `lemmas/X.md` §3 Step 3: the new bound of the geometric sum (2 in place of K_s). Is every inequality right for every
   s₀ ≥ 0, j₁ ≥ 0, including s₀ = 0? Is the hypothesis e^{s₀}q ≤ ½ available where it is used?
2. `lemmas/X.md` (E4): (s₀ + 1) log n ≤ 2t on the range t ≥ M₀ log n, hence C_d := 34. Then follow C_d through the whole
   file (§0–§8): every place that used C_d, C_x, C_P, Λ, C_Q, C_β, C_v, C. Does any step need the old value s + 33, or need
   C_d ≥ a quantity that depends on s? Does any other constant entering C, or any inequality of the form "≤ (constant)·t",
   hide a dependence on s (look in particular at uses of m_n(t), C_m, d_t, the events (N1)–(N3), (E1)–(E4), §5–§7)?
3. The Markov step using C₅: recompute the product and the inequality "≤ C₅e^{−2t} ≤ e^{−t}".
4. The bound M₀ ≤ 16 + 4(1 + s)(A + 1) + 3B/(2σ²): recompute.
5. §9 (Lemma X′) is claimed unchanged and unaffected: does §9 use C_d, K_s or C₅ anywhere?
6. `lemmas/DIST12.md` D.1: d₁ log n ≤ 34t and C_T := 4[34(A + 7) + 8] (this now uses t ≥ M₀ log n; is d₁ used anywhere
   outside that range, e.g. in D.6?). The paragraph "Dependence on the sparsity" after D.4: is
   C = (C_X² + C_X/2 + 1 + C_T)^{1/2} really free of s, and is the displayed bound on ε_n² proved? Is the raw sparsity
   s₀^r the right parameter throughout?
7. Verdict on consequence (c) as it reads in `STATEMENT.md` v1.4.7, and on the changelog tag: **EQUAL on TC3** ("Best
   radius ε_n² = C²M₀ log n/n with M₀ = O((1 + s₀^r)(A + 1))", the O being for fixed (σ*², M, M′)). Say CONFIRMED or
   CONTESTED, with the reason. If contested, say exactly what is proved.

## Part B — amendments made to proof files after their line checks

Blocks 3–7 of `reviews/DIFFS_D1.patch`: `work/C_size/S.md`, `work/D_output/P6_DISTC.md`, `work/D_output/COR_C.md`,
`work/E_bridges/B3.md`, `work/E_bridges/ASSEMBLY.md`. The findings behind them: `reviews/L2_sol_D.md`,
`reviews/L4_sol_E.md`, `reviews/L5_astra_SV.md`; dispositions: `reviews/L4_L5_disposition.md` (it also holds the L2
disposition). For each hunk: does it resolve the finding it answers, is it correct, and does it leave the surrounding
verified proof valid? Report any hunk that answers no listed finding.

## Part C — statement changes, v1.3.1 → v1.4.7

Diff: `reviews/DIFF_STATEMENT_v131_to_v147.patch` (v1.3.1 was the version of the last statement-change check,
`reviews/S2_sol.md`). The changelog table at the foot of `STATEMENT.md` lists the changes, rows 1.4 to 1.4.7, each with a
tag (STRONGER / WEAKER / EQUAL / NEW-CLAIM), a reason and a trigger file (all in `reviews/`).
1. For every changelog row from 1.4 on: is the tag right? Answer CONFIRMED / CONTESTED per row.
2. Is there any change in the diff that no changelog row covers, or that changes meaning while tagged EQUAL?
3. For each changed statement (reader Setup, (A1)–(A6), Theorem A, Theorem B, Corollary C, Remarks, DIST-C (C-ii)(γ),
   Lemma S, bridges B2, B3, DIST-1 (c)): does the proof file named in `REPORT.md` §1 still prove the statement as it now
   reads? (Proof files: `work/E_bridges/ASSEMBLY.md`, `work/D_output/COR_C.md`, `work/D_output/P6_DISTC.md`,
   `work/C_size/S.md`, `work/E_bridges/B2.md`, `work/E_bridges/B3.md`, `lemmas/DIST12.md`.)
4. `TARGET.md` §6 must carry the same reader block as `STATEMENT.md` §1R (Setup to Corollary C): report any difference
   in meaning. `TARGET.md` §5 (TC1–TC9) must be untouched in meaning and still implied by the current statements.

## Output (`reviews/D1_sol_diff.md`)

First line: `D1 diff check — STATEMENT.md sha256 <first 16 hex>; lemmas/X.md <16 hex>; lemmas/DIST12.md <16 hex>`, then the
sha256 (first 16 hex) of the five files of Part B. Findings with id (D1-xx), severity (CRITICAL / MAJOR / MINOR / NIT),
file and place, the error or gap in full, minimal repair. Then verdicts:
- Part A: per item 1–7, VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED; and one line each for `lemmas/X.md` (Lemma X,
  Lemma X′) and `lemmas/DIST12.md` (DIST-1, DIST-2) as they now stand.
- Part B: per file, VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED.
- Part C: per changelog row, CONFIRMED / CONTESTED; items 2–4.
Final line: overall verdict. Say exactly what you could not check.
