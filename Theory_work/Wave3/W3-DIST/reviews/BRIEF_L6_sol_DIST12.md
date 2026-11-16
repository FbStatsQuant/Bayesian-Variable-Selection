# W3-DIST — cross-family line check L6 — Theorems DIST-1 and DIST-2 (assembly from Lemmas H, T, X, X′) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L6_sol_DIST12.md`.** Run no git command that changes state; start no agents.
Any temporary file goes under `/home/fb31/SMC_Theory_Department/tmp/20261115-W3-DIST-L6/` (never `/tmp`); remove it when done.
Proof file: `Theory_work/Wave3/W3-DIST/lemmas/DIST12.md`. Statements to be proved: Theorem DIST-1 (display (1.1) and its
consequences (a)–(e)) and Theorem DIST-2 (display (1.2)) in `Theory_work/Wave3/W3-DIST/STATEMENT.md` §1, with §0 (setting
(RD), raw and retained dimensions, the density attached to a posterior draw, the distance, the interfaces, m_n(t)).
**Given inputs (do not review their proofs):** Lemma H, Lemma T, Lemma X and Lemma X′ exactly as stated in STATEMENT §3;
for the constants of Lemmas X, X′ (c = ½, the size cut s₀ + ⌈32t/log n⌉, C_m with m_n(t) + s₀ ≤ C_m t, the form of their bad
sets) you may read `Theory_work/Wave3/W3-DIST/lemmas/X.md` §0, §7 and §9; common definitions in
`Theory_work/Wave3/W3-DIST/API_CARDS.md`. Read nothing else in the ticket folder (no `reviews/`, `LOG.md`, `CHECKPOINT_*.md`,
`DEPS.*`, `work/`), and stop reading STATEMENT.md at "## Changelog".
Check every line and try to break the passage:
1. D.1: the two sparsity levels are deterministic and in Lemma T's range for n ≥ n_T; the bounds on η²_n(d₁, e^{−t}) and
   η²_n(d₂, e^{−t}) with the stated constants C_T, C_T′ (recompute).
2. D.2: the intercept event and its probability; is ε̄ really not controlled by Lemma X?
3. D.3: the pointwise bound — the support of the raw direction u = b − β* (dropped true columns included), Lemma H's
   in-sample identity, the use of Lemma T with c = 4σ² simultaneously for the data-dependent (a, u).
4. D.4: Step 1 (conditioning on the raw design; which quantities are deterministic given X^r; that Lemma X's hypotheses
   hold on G_t; measurability; independence of ε and X^r); Step 2 (inclusion of the bad set of (1.1) in Bad_X, with
   C′ = 33 and C as defined); Step 3 (the probability budget giving exactly 3e^{−t/2} + P*(G_tᶜ); no independence between the
   transfer event and the interfaces). Does this prove (1.1) exactly as displayed, with constants independent of the
   law of the data, for one n₀ and the whole range of t? Consequences (a)–(e).
5. D.6: the same for (1.2) (levels d₂, Lemma X′, radius C₂√(tℓ_n/n), remainder without (ND)).
6. Look for a law in (RD) for which a step fails: atoms, infinite variance of x, a true column constant in the sample,
   p_raw ≠ p_ret, s₀ < s₀^r, s₀^r = 0, p_raw = 2, t at either end of its range.
Output: first line `L6 line check — lemmas/DIST12.md sha256 <first 16 hex>`. Findings with id, severity (CRITICAL / MAJOR /
MINOR / NIT), section, the error or gap in full, minimal repair. Verdict per item (D.1, D.2, D.3, D.4 / DIST-1, D.6 / DIST-2):
VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict. Do not soften findings; say exactly what you
could not check.
