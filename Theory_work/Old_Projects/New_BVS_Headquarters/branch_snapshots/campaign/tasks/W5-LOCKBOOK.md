# W5-LOCKBOOK: Lock the low-risk half. T32(i); the GUARD/OUT/SR code audit; referee W2-BOOK and W2-T26; one STATEMENTS.tex for Prop 1, Prop 2, Thm 4, Thm 6

**Paper role:** Prop 1, Prop 2, Thm 4, Thm 6 and Thm 5(c). All are PROVED candidates from single runs with no
referee, and three implementation facts (GUARD, OUT, SR) are used as hypotheses without an independent code check.

Fetch and read: `origin/theory/W2-BOOK` (REPORT, PROOF §§0–4, STATEMENTS.tex, scripts), `origin/theory/W2-T26`
(REPORT, PROOF §§1–6), `origin/theory/W2-VT24G` (REPORT §6: the (e′) edits), `origin/theory/W1-T24G` (Theorem B,
Cor B-M), `origin/theory/W4-T38FULL` (`T38_STATEMENT.md` Part I (0), (c); `T38_PROOF.md` §§1, 6), locked T07,
T06, T12, T31, T21, T11(iii), T14, T15, T23, T25, T32 (`Docs/Theory/proofs/`, `COLLECTED_PROOFS_v2.tex`,
`LOCKED_PROOFS.md`), and the engine: `v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`, `v3_ledger.h`, `v3_calib.h`,
`v3_run.R` (read only; R cannot be run).

Goals, in order:
1. **Referee W2-BOOK**: Lemma RO and its counterexample (conditioning on completion), Prop 2 (a)–(f) including the
   ¾-covariance formula and the locked island independence it uses, Prop 1 (i′) sharpness and (iii′) certificate,
   Thm 4's (e′)/(e-M)/(d⁺) wiring against W2-VT24G's three edits, the run/output split edits for T11(iii), T14(i),
   T15, T23(ii), T25(iv), T31, T34. Reproduce the exact-law numbers (`frozen_run_exact.py`) with your own code.
2. **Referee W2-T26**: Lemma 1 (Δ_n exact), Lemma 2 (ρ̄ exact), **Lemma 3's use of T15 at a terminal-round prefix
   (T12(i.b))**, Theorem A (A-0)–(A-ii) including the output form, Theorem B's composition, Prop C (ORTH) as a
   sketch. Reproduce the p = 18 premise scan at three sizes.
3. **Code audit (read-only), as a referee of implementation facts.** (a) GUARD: list every code path that can set
   `resource_limit` after the final run starts and confirm none touches an RNG, a setting, the inherited store or
   the cache; confirm the stop-only coupling. (b) OUT: can any failure mode (`resource_limit` after allocation,
   `numerical_failure` in the final run) return a *partial* evidence or PIP differing from the potential run's? (c)
   SR: `step_gibbs` scores both configurations and offers both to the HPM, including when the flip is infeasible at
   the cap. (d) IND-T's premise: one sequential stream per island, read at state-dependent rates, no per-particle
   streams. (e) The scan-before-limit rule of `local_search` and the `emit_centre` flag. Write each as a one-line
   implementation lemma with file:line evidence.
4. **Prove T32(i)** (the score-evaluation ceiling of the SMC branch) from METHODOLOGY_v3 §§6.5–6.10 and the engine
   loops, as a deterministic count: per round ≤ m = p + B + 2 evaluations, per stage one round per particle, the
   pilot and final budgets, the local searches (≤ 2ℓ + 3 of them, each ≤ (ℓ+1)max_k[p + k(p−k)] scores). This makes
   Thm 5(c) a theorem.
5. **STATEMENTS.tex**: paper-ready statements of Prop 1, Prop 2, Thm 4 (with routes (a), (d)/(d⁺), (e′)/(e-M)) and
   Thm 6 (with (P1) in the realised-T_n form), each with the hypotheses named and the run/output split applied, plus
   the n = 200 disclosure sentences they need (P(U) = 6/2,400 with Wilson interval; "never given completion").

Deliverable: `theory_campaign/W5-LOCKBOOK/REPORT.md` (verdict tables for W2-BOOK and W2-T26; the implementation
lemmas; the T32(i) proof in PROOF.md), `STATEMENTS.tex`, scripts, results, confidence card.

---

_Source: theory_campaign/F-REFINE/NEXT_TASKS.md on branch theory/F-REFINE (Fable, 2026-11-02). Read F-REFINE's CARDS.md and ARCHITECTURE.md first: `git fetch origin theory/F-REFINE`._
