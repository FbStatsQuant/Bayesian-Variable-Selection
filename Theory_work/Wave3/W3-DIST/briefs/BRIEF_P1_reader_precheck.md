# W3-DIST — same-family pre-check P1 of the reader versions and bridges — Claude Opus 5.5, Claude Third, effort high

You are an independent checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one output
file `Theory_work/Wave3/W3-DIST/reviews/P1_opus_precheck.md`.** Run no git command, start no agents, effort high at most.
This is a same-family pre-check (a filter before a cross-family review); it does not count as a review layer.

## What to check
`Theory_work/Wave3/W3-DIST/STATEMENT.md` v1.2: §1R (reader versions: Setup, assumptions (A1)–(A6), Theorem A,
Theorem B, Corollary C, Remarks) and §3 "Bridges" (B0, B1, B1′, B2-core, B2, B3). Nothing is proved yet; these are
candidate statements. The claim to test is **faithfulness**: reader version = master theorem + bridges, i.e.
- Theorem A ⇐ DIST-1 display (1.1) (and its second sentence ⇐ DIST-2 display (1.2)) + B0 + B1 + B2;
- Theorem B ⇐ DIST-3 + B0 + B1 + B2 + B3 + W3-POST Theorem 1 (a consumed premise);
- Corollary C ⇐ DIST-C (C-0), (C-i), (C-ii)(α) + Theorem A.
Take the master statements (1.1), (1.2), DIST-3, DIST-C as given (do not review them).

You may read: `Theory_work/Wave3/W3-DIST/STATEMENT.md`, `ROUTES.md` (§2b), `TARGET.md` (§6);
`Theory_work/Wave3/W3-POST/STATEMENT.md` (§0, §2: hypotheses (E), (F_λ), (F_w), (BM), item 6, Corollary 1R);
`Theory_work/Wave3/W3-POST2/STATEMENT.md` (interfaces (ADG), (DG); Implications); `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`
(Lemma A0); `Theory_work/Wave3/W3-MISR/STATEMENT.md` §1 (Lemma R′); `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`.
Do not read `reviews/` of W3-DIST, its LOG.md, CHECKPOINT_*.md or BRIEF.md.

## Questions (try to break each; give explicit counterexamples where you can)
1. **B1.** Does (A3) for single coordinates plus (A5) give, with the stated probability, ½ ≤ ŝ_j²/Var(x_j) ≤ 2 for all
   j ≤ p, no dropped column, (E; 2s²b̄²) and (C; 2sb̄²) in units of σ*²? Check the triangle-inequality step and the
   probability (4p·exp(−c₁n/K⁴)); look for a law satisfying (A3) as written for which it fails (atoms, K close to 1, …).
2. **B2-core and B2.** Is B2-core true as stated under (A3) (ψ₂–L₂ form on q-sparse directions), including the
   intercept and degenerate directions? Is the chain λ_min(G_T) ≥ c_ψ/8 correct, and does it give [W3P] (F_w; g₀), then
   (DG), then (ADG) = (ND; c_D, m) with c_D = g₀/(1 + g₀), on the range needed by (1.1) at t = M log n — i.e. is
   q_n = ⌈C_q M log n⌉ with C_q = 2(s(A + 2) + 4)/log 2 at least m_n(M log n) + s for M ≥ 1 and all large n? Is the
   requirement q log(ep/q) ≤ c₂n/K⁴ met for all M ≤ √n?
3. **B0.** Does W3-MISR Lemma R′ (a′), (b) give what B0 claims for the *parameter* posterior under a random design, and
   is d_H invariant as claimed? Is "σ* > 0 arbitrary, not fixed" justified, with (A5) in units of σ*?
4. **Theorem A's display.** From (1.1) at t = M′ log n with remainder ≤ 5p·exp(−cn/K⁴): is
   P*[Π(d_H > √(M log n/n) | D_n) > n^{−cM}] ≤ n^{−cM} for M₀ ≤ M ≤ √n correct after renaming constants (one n₀ for the
   whole range of M)? Is "depending only on (s, A, K, c_ψ, b̄)" right? Is the range M ≤ √n inside t ≤ n^{1−κ₀}?
5. **Theorem B and B3.** Do the stated assumptions give the events of W3-POST Theorem 1 item 6 with common constants
   (check (F_λ) set sizes against "(2A + 3)s + 2", (F_w) range against q_n = ⌈C_q log n⌉, BM-∞ with a deterministic
   envelope, s₀ ≥ 1, fixed σ*² vs B0) and (TR₀)?
6. **Corollary C.** Is the display a correct consequence (note the event is a data event, the premise π(𝒯) ≥ n^{−cM/2}
   is about the run)? Is the description of what the sampler returns accurate as a reader-level statement?
7. **Readability and honesty.** Is any assumption in (A1)–(A6) non-standard, ambiguous, or stronger/weaker than what the
   bridges use? Is anything needed by the bridges missing from the list (e.g. p ≥ 2, n large, exactly s vs at most s,
   positive variances)? Do the "why / necessary?" lines in TARGET.md §6 overclaim?

## Output (`reviews/P1_opus_precheck.md`)
Findings with id, severity (CRITICAL / MAJOR / MINOR / NIT), the clause, the argument or counterexample in full, and the
minimal repair; a verdict per clause (Theorem A, Theorem B, Corollary C, B0, B1, B2-core, B2, B3):
SOUND-AS-STATED / REPAIRABLE / FALSE-AS-STATED; one final line with an overall verdict. Do not soften findings.
