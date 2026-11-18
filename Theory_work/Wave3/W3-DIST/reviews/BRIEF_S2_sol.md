# W3-DIST — blind read S2 (reader versions, bridges, changelog tags) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent reviewer. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one output
file `Theory_work/Wave3/W3-DIST/reviews/S2_sol.md`.** Run no git command that changes state; start no agents.
You may read only: `Theory_work/Wave3/W3-DIST/STATEMENT.md`, `Theory_work/Wave3/W3-DIST/ROUTES.md` (§2b),
`Theory_work/Wave3/W3-DIST/TARGET.md` (§6), the manifest `Theory_work/Wave3/W3-DIST/reviews/MANIFEST_S2.txt` (quote its
digest in your first line) and the files listed in `Theory_work/Wave3/W3-DIST/reviews/INPUTS_S2.txt`. Do not read any
other file under `reviews/`, nor `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*`, `BRIEF.md`, `briefs/` or `work/` of that ticket.

Nothing is proved yet: these are candidate statements. The master theorems of STATEMENT §1–2 (displays (1.1), (1.2),
DIST-3, DIST-C) are to be **taken as given**; do not review them.

## Part 1 — break the reader versions and the bridges
Object: STATEMENT §1R (Setup, constants, (A1)–(A6), Theorem A (i), (ii) and its sentence without (A4), the Example,
Theorem B, Corollary C, notation table, Remarks) and §3 "Bridges" (B0, B1, B2-core, B2, B3). The claim is
**faithfulness**: Theorem A ⇐ (1.1)/(1.2) + B0 + B1 + B2; Theorem B ⇐ DIST-3 + B0–B3 + W3-POST Theorem 1 (a consumed
premise); Corollary C ⇐ DIST-C + Theorem A. For each clause:
1. Try to construct a counterexample (a law of (x, y) satisfying the assumptions as written for which a bridge or the
   conclusion fails): atoms, degenerate or nearly degenerate sparse directions, triangular arrays, p = 2 or p ≤ q_n,
   s = 0, σ* depending on n, dropped columns, the range M₀ ≤ M ≤ √n/log n, constants "depending only on (s, A, K, c_ψ, b̄)".
2. Check each bridge's stated probability and algebra (B1's triangle step; B2-core with the intercept; the chain to
   λ_min(G_T) ≥ c_ψ/8; (F_w) ⇒ (DG) ⇒ (ADG) with c_D = g₀/(1 + g₀) against `W3-POST2/lemmas/A_occam.md`; the window
   q_n against m_n(M log n) + s; B0 against W3-MISR Lemma R′; B3 against W3-POST Theorem 1 item 6).
3. Clarity: is every symbol in §1R defined before use; is any assumption ambiguous or non-standard; does the text
   say anything about the method or the sampler's output that the code files in INPUTS_S2 contradict?
4. The "why / necessary?" lines of TARGET §6: does any line overclaim?

## Part 2 — statement-change check (changelog at the foot of STATEMENT.md)
For every row of the changelog with a tag other than EQUAL (and any EQUAL row you doubt): say CONFIRMED or CONTESTED,
with the reason, judging the tag (STRONGER / WEAKER / EQUAL / NEW-CLAIM) from the row's description and the current
text. Say explicitly whether any row weakens one of: the metric (joint (x, y) Hellinger, arbitrary predictor law in
the master theorems), display (1.1), its rate, its hypotheses, the use of the coded prior, display (1.2), DIST-3's
oracle display, DIST-C's deterministic transfers, or reader Theorem A. If you cannot assess a row from what you may
read, say so.

## Output (`reviews/S2_sol.md`)
First line: `S2 blind read — manifest <digest>`. Findings with id, severity (CRITICAL / MAJOR / MINOR / NIT), clause,
argument or counterexample in full, minimal repair. A verdict per clause (Theorem A, Theorem B, Corollary C, B0, B1,
B2-core, B2, B3): SOUND-AS-STATED / REPAIRABLE / FALSE-AS-STATED. The table of Part 2. Final line: overall verdict.
