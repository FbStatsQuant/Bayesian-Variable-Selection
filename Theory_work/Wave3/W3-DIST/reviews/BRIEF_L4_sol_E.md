# W3-DIST — cross-family line check L4 — stream E: bridges B0, B1, B2-core, B2, B3 and the assembly of the reader theorems — gpt-6.1-sol, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L4_sol_E.md`.** Run no git command that changes state; start no agents.
Proof files: `Theory_work/Wave3/W3-DIST/work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`, `ASSEMBLY.md`, each
including its final "Amendments" section if present. Statements: `Theory_work/Wave3/W3-DIST/STATEMENT.md` §1R (Setup,
assumptions (A1)–(A6), Theorem A (i), (ii) and its sentence without (A4), the Example, Theorem B) and §3 "Bridges". The
master displays (1.1), (1.2), Theorem DIST-3 and Lemma X′ of STATEMENT §1, §3 are **given hypotheses** (do not review
them); W3-POST Theorem 1 is a consumed premise of Theorem B. Also readable: `Theory_work/Wave3/W3-MISR/STATEMENT.md` §1
(Lemma R′), `Theory_work/Wave3/W3-POST/STATEMENT.md` §2, `Theory_work/Wave3/W3-POST2/STATEMENT.md`,
`Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`, `Theory_work/Wave3/W3-DIST/API_CARDS.md` ("Common definitions"), and the
check script and output in `work/E_bridges/`. Read nothing else in the ticket folder (no `reviews/`, `LOG.md`,
`CHECKPOINT_*.md`, `DEPS.*`, other `work/` folders, `lemmas/`).
Check every line and try to break each bridge:
1. B0: the pathwise scale reduction (posterior equivariance from Lemma R′ (a′); the plug-in intercept; invariance of
   the Hellinger distance and of the events), with σ* allowed to depend on n.
2. B1: the constant c₁ and the probability 4p·exp(−c₁n/K⁴); no dropped column; the energy and coefficient-cost bounds.
   Look for a law satisfying (A3) as written for which B1 fails.
3. B2-core: the net argument and the one-sided Chernoff bound with the stated absolute constant; the intercept;
   q > p; degenerate directions; the union over supports. Look for a law satisfying (A3) for which it fails.
4. B2: the chain to the Gram floor; (F_w) ⇒ (DG) by eigenvalue interlacing ⇒ (ADG) = (ND) with c_D = g₀/(1 + g₀), on the
   range needed by (1.1) at t = M log n; the window inequality for every n ≥ 2, M ≥ 1; the file's editorial change request.
5. B3: against W3-POST Theorem 1 item 6 (events measurable in (X, θ*), common constants, exactly s ≥ 1) and (TR₀).
6. ASSEMBLY: the renaming of constants from (1.1), (1.2) to Theorem A (i), (ii) and the sentence without (A4); one n₀ for
   all M₀ ≤ M ≤ √n/log n; constants depending only on (s, A, K, c_ψ, b̄); the reading convention on the master displays
   (constants and n₀ independent of the law of the data — is this what STATEMENT's (1.1), (1.2) say?); Theorem B; the
   Example (jointly Gaussian; AR and equal correlation, including non-contiguous index sets).
7. Faithfulness: does ASSEMBLY prove Theorem A and Theorem B exactly as worded in STATEMENT §1R?
Output: first line `L4 line check — sha256` followed by the first 16 hex of each of the six files. Findings with id,
severity (CRITICAL / MAJOR / MINOR / NIT), file and section, the error or gap in full, minimal repair. Verdict per item
(B0, B1, B2-core, B2, B3, ASSEMBLY/Theorem A, ASSEMBLY/Theorem B): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED.
Final line: overall verdict. Do not soften findings; say exactly what you could not check.
