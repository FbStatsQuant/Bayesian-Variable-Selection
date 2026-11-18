# W3-D2 — PLAN v1.0 (2026-11-17)

Cost estimate 1 day; kill budget 1.5 days (HQ). Tier B, NORMAL mode, Codex level 1 (one Codex job at a time).

| step | what | who | hours |
|---|---|---|---|
| 1 | STATEMENT v1.0 (Theorem 2X, Corollary 2X), PROOF v1.0 (short: P0–P3), TARGET, READER_DELTA draft, numerics N1 | lead | 1.0 (done) |
| 2 | Statement lock: one Sol read, fresh, blind (STATEMENT + PLAN + PROOF route + CorGb-plus, R1 B4.1, row thm2) | Sol (codex, gpt-6.1-sol, high) | 0.2 + wait |
| 3 | CP1 (≤ 10 lines), end of run; manager answers | lead | 0.1 |
| 4 | Blind line check of PROOF.md (P0–P3) | Opus 5.5 high (claudeAgent_claude_third), fresh | 0.1 + wait |
| 5 | DEPS.tsv, REPORT.md (REGISTRY blocks), citecheck 0 MISS | lead | 0.5 |
| 6 | Council R1 on a frozen manifest: Sol seat + Opus seat, blind; diff rounds Opus-only | Sol, Opus | 0.3 + waits |
| 7 | CP3, `manifest.py bind`, recording package for the manager | lead | 0.3 |

**Proof route.** P1: STATEMENT §0 is CorGb-plus's setting with q = 0, a = γ = τ² = 0 (N_n(m, 0) := δ_m); (A2) covers
|T| ≤ k_n by `W3-READER:R1@1.0.2` B4.1; (A3) is the → ∞ branch. P0/P2: deterministic PIP/HPM/MPM facts + Markov.
P3: recorded Theorem 2 hypotheses ⇒ (A1)–(A3) (energy by λ_max ≤ trace).
**Kill point.** Stop if any of CorGb-plus's hypotheses is not implied by (A1)–(A3) (or by the recorded Theorem 2
hypotheses for Corollary 2X); record the missing hypothesis. No new lemma is planned; a needed one makes the ticket Tier A
→ early checkpoint.
**Questions for the lock.** (Q1) Is the q = 0 instance inside CorGb-plus's setting (n × 0 matrix, degenerate (OV))? (Q2) Is
the recorded row-1.2 model's (α*, β*) deterministic, as Corollary 2X uses? (Q3) Is the STRONGER tag (STATEMENT §7)
right, given the status caveat and the vanishing-floor remark?
