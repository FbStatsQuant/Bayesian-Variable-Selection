# BRIEF — RT1: is DIST-2's "best rate" sentence false or loose? (Theory Department, 2026-11-16) — Sol, effort high, one call

Fresh, read-only reviewer. Do not write any file outside the worktree and set no TMPDIR. Scratch only in
/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/, deleted at the end. Write exactly one file:
`/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/DIST2_rate_check/RT1_sol.md`. Change no git state. Do not edit any W3-DIST file.

## Object
W3-DIST (council R2 passed, MANIFEST c5cd9cdd…; folder `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/`).
Claim W3-DIST:DIST-2, statement span `STATEMENT.md:93-98` (REPORT.md:143). Inside it, lines 96-97:
"Best rate ε_n² ≍ (1 + s₀^r) log n · ℓ_n/n: one logarithm slower than DIST-1 at polynomial p."
The theorem's constants c, C, M₀, n₀ depend on (s₀^r, A, σ*², M, M′, κ₀) (STATEMENT.md:93-95). A council seat noted (outside scoring)
that the proof's constant grows faster in s₀^r than the displayed factor (1 + s₀^r) suggests.

## Questions
1. Confirm the sentence lies inside the registered span 93-98.
2. In the theorem's own setting (is s₀^r fixed in n, or allowed to grow? check STATEMENT §0 and the DIST-2 proof, `lemmas/` / `work/` files
   it cites), is the sentence **FALSE** (asserts an s₀-dependence of the rate, or a two-sided ≍, that is not proved or is wrong), or
   **LOOSE** (true as written once constants may depend on s₀^r, but the explicit factor is decorative/misleading)? Derive the actual
   s₀^r-dependence of the radius ε_n² = C²·t·ℓ_n/n at t = M₀ log n from the proof (track how C and M₀ depend on s₀^r), and say whether
   "≍" (two-sided) is proved at all or only "≲".
3. If FALSE: give a minimal **same-line-count** replacement for lines 96-97 that is true (e.g. "for fixed s₀^r, …", or the proved
   s₀-dependence), keeping the rest of the paragraph.
4. State the true s₀^r-dependence you derived in one line (it goes to HQ's strength list; compare Song–Liang ε_n² ≍ s log p/n).

## Output
`VERDICT: FALSE | LOOSE`, `IN-SPAN: YES | NO`, the derivation (≤ 20 lines, file:line), the replacement text if FALSE, the one-line true dependence.
