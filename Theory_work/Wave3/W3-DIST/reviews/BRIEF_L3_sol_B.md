# W3-DIST — cross-family line check L3 — stream B: Lemma H, Lemma T, Theorem DIST-3 — gpt-6.1-sol, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L3_sol_B.md`.** Run no git command that changes state; start no agents.
Proof files: `Theory_work/Wave3/W3-DIST/work/B_transfer/H.md`, `T.md`, `DIST3.md`. Statements:
`Theory_work/Wave3/W3-DIST/STATEMENT.md` §3 (Lemma H, Lemma T — the stated range 1 ≤ d ≤ min(p_raw, n − 1) and remainder
η²_n(d, δ) are what must be proved; the "Route" sentence under Lemma T is not part of the statement) and §1 (Theorem
DIST-3 with (TR₀), (L₀) and notes (i)–(iii)), with §0 for the setting. Common definitions:
`Theory_work/Wave3/W3-DIST/API_CARDS.md` ("Common definitions"). Also readable: the check scripts and outputs in
`work/B_transfer/`. Read nothing else in the ticket folder (no `reviews/`, `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*`, other
`work/` folders, `lemmas/`).
Check every line and try to break each result:
1. Lemma H: the affinity formula for two normals, the pointwise bound, the integration over x, and the in-sample
   identity n⁻¹ΣΔ_i² = ε̄² + ‖μ̂ − μ‖²/n when true columns are constant in the sample.
2. Lemma T: the one-sided inequality of T.md (ghost sample with Cantelli's bound; random swaps with Hoeffding; union
   over traces on 2n points) — recompute every constant and the conditioning; Sauer–Shelah and the VC bound for
   half-spaces as proved in the file; the growth-function bound for unions of two affine half-spaces on at most d of
   p_raw coordinates; measurability; the layer-cake step to the truncated quadratic loss simultaneously in (a, u, c); the
   final statement with the exact η²_n(d, δ). Try to find a law of x (atoms, heavy tails), a d near n, or a parameter
   choice that violates the lemma or a step.
3. DIST-3: the fixed-design oracle bound (conditional posterior given S₀: mean, fitted-mean fluctuation, variance),
   the noise event and its probability, the use of (TR₀) and (L₀), the additive δ_n, the integration over the design,
   the in-probability corollary, notes (i)–(iii), the constants (c = 1; what C and n₀ depend on), s₀ = 0.
4. Each file's "STATEMENT-CHANGE REQUEST" or wording request: justified? does any weaken the statement?
Output: first line `L3 line check — sha256 H.md <16 hex> T.md <16 hex> DIST3.md <16 hex>`. Findings with id, severity
(CRITICAL / MAJOR / MINOR / NIT), file and section, the error or gap in full, minimal repair. Verdict per result
(Lemma H, Lemma T, Theorem DIST-3): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict.
Do not soften findings; say exactly what you could not check.
