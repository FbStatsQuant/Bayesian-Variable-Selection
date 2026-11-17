# W3-D2 — K2 re-check brief (Opus 5.5 high, new agent; saved before launch 2026-11-17)

You re-check repairs for ticket W3-D2 in the git worktree /home/fb31/BVS-wt/W3-D2 (read-only except your reply file; no
git state changes; scratch only in /home/fb31/BVS-wt/W3-D2/.rc_tmp/, deleted at the end). Do not read LOG.md.

**Inputs.** The line check `Theory_work/Wave3/W3-D2/reviews/K1_linecheck_opus.md` (its findings K1-1..K1-4), the lead's
disposition `reviews/K1_disposition.md`, and the current files `Theory_work/Wave3/W3-D2/PROOF.md`, `STATEMENT.md`, `REPORT.md`.
Diffs: `reviews/K1_repair.diff` (PROOF v1.0 → v1.1) and `reviews/STATEMENT_v1.1_to_v1.2.diff` (STATEMENT after its lock).
Sources as cited in those files (e.g. `Theory_work/Wave3/W3-MISR-R/STATEMENT.md`, `Theory_work/Wave3/W3-POST/STATEMENT.md:16-39`,
`Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md`).

**Answer.**
1. Is each of K1-1..K1-4 resolved by the PROOF diff? Does the diff break anything?
2. STATEMENT diff: the §0 posterior gloss (coefficient prior N(0, nσ²(X_SᵀX_S + I)⁻¹) given (S, σ²), inverse-gamma noise
   prior, capped beta-binomial size prior) — is it faithful to [W3P] `Theory_work/Wave3/W3-POST/STATEMENT.md:16-29`? The §7
   caveats (a), (b) — faithful to §5 and §4(b)? Tag EQUAL right for both?
3. REPORT `## 6. Registry blocks`: does each block point to the right STATEMENT lines (claim spans, premises), carry the
   status line of PROOF.md:3, and describe the conclusion without claiming more than STATEMENT §§1–2? Is REPORT §3's card
   sentence faithful to STATEMENT §1 (no extra strength)?
Findings tagged C/S/F/E with line and fix. Write to `Theory_work/Wave3/W3-D2/reviews/K2_recheck_opus.md`, ending with one line
`K2-VERDICT: <RESOLVED | RESOLVED-WITH-AMENDMENTS | NOT-RESOLVED>`. Then end.
