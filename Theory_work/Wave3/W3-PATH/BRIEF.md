# W3-PATH — reported model without the lattice condition (path-level control of LS0) — scoping leg (HQ, 2026-11-12)

You are the **lead** of ticket W3-PATH (Claude Fable 5.2, effort high, provider **claude-personal**). Worktree
`C:/Users/felip/BVS-wt/W3-PATH` (branch `theory/W3-PATH`, from main); folder `Theory_work/Wave3/W3-PATH/`. Work only
inside it. **Change no git state** (HQ commits). Never use effort above high.

## Read first
- `Theory_work/Wave3/PROGRAM.md` (presentation rule), `Theory_work/Wave3/PROTOCOL.md` (rules 9–16: checkpoints, frozen
  manifests + blind first reads, consumed claims, hold file, LOG heartbeat, kill budgets).
- The theorem to strengthen: `Theory_work/Wave3/W3-RM/STATEMENT.md` v1.2.1 (RM-0, RM-F, RM-R; the lattice condition
  (N) l.103–117 and (D-R) l.146; table l.195–205) and its REPORT §6 item 2 ("Dropping (N)/(D-R) — path-level control of
  LS0; HIGH, open research"). Its strengthening W3-RM2 (polynomial leakage; council-passed, not yet recorded):
  branch `theory/W3-RM2`, worktree `C:/Users/felip/BVS-wt/W3-RM2/Theory_work/Wave3/W3-RM2/` (STATEMENT, REPORT,
  lemmas) — read it, cite it as "council-passed, acceptance pending".
- Existing path material (none of it is a proof of what you need; read critically):
  - scoping memo `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM/Theory_work/Wave3/W3-MEMO-SCR-RM/MEMO.md` v2 §2 (potential lemma
    PL, the (N-χ)/(N-D) discussion, l.110–145; Corollary CERT) — unreviewed sketches, scoping input only;
  - `Theory_work/Wave2/W2-FAC-PK/` (Thm-PATH), `Theory_work/Wave2/W2-FAC-A/` (path route beyond log p/log n = 1/6, open);
  - `Theory_work/Wave1/W1-GEN/lemmas/` (descent), `Theory_work/Wave1C/C-GROW/lemmas/` (L1 descent, L2 NA/TL).
- Code: LS0 as coded on `main` (`Scripts/SMC_BVS/core/`; move cap ℓ_n + |S̃₀|) — pin file:line + commit for every code fact.

## Target
Under primitive, design-agnostic conditions on (X, θ*) — Theorem 1's conditions, eigenvalue floors, visibility (V) and
leakage (L) (polylogarithmic, and polynomial as in RM2 if it carries over) — but **without (N)/(D-R)**, the coded method
reports Ŝ⁺ = S₀ with probability → 1, p ≤ n^A, p ≫ n. Replace lattice-wide NA/TL control by control of the **path LS0
actually follows** from the start mode (with the start-mass results of W3-START/START2 as inputs if useful). No design
family in any statement; families only in an examples table. All results asymptotic.

## This leg: scoping to CP1 only (target ≈ half a day; be token-efficient)
1. `PLAN.md` and `STATEMENT.md` v1.0 (candidate theorem + the **key lemma** stated precisely, with assumption ids);
   an honest map of which RM/RM2 steps survive verbatim, which change, and where (N) is used today.
2. `ROUTES.md`: 2–3 candidate proof routes for the key lemma (e.g. potential argument PL, path-restricted NA/TL,
   exit control), each with the exact point where it could fail and a difficulty estimate.
3. Small local numerics (no NOTS) on designs where (N)/(D-R) fails but the method may still recover S₀ — does the
   conclusion survive? (`numerics/`, scripts + RESULTS.)
4. One fresh **Astra** (codex `gpt-6-astra`, reasoningEffort high), blind first read on a frozen manifest
   (`python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/W3-PATH
   Theory_work/Wave3/W3-PATH/reviews/MANIFEST_S1.txt --extra Theory_work/Wave3/W3-PATH/reviews/INPUTS.txt` from the
   worktree root; INPUTS never lists wave documents or registry tables), asked to break the candidate statement and the
   routes (counterexample to the theorem as stated? fatal flaw in each route?). Disposition file.
5. **CP1:** `CHECKPOINT_1.md` — locked candidate statement (or the strongest one that survived), the key lemma, the
   route ranking with failure points, numerics, Astra's verdict and dispositions, and a recommendation: proof leg GO
   (with a kill budget of N attempts on the key lemma and a time estimate) or NO-GO (with the obstruction). **End your
   run** with that content as your final message.

## Operating rules
- Read `C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave3/HOLDS.md` before each step.
- Subagents via `delegate_task`: Sol/Astra on provider `codex`; any Claude helper on provider **`claude-personal`,
  Opus 5.5 (not Fable)**, effort high max. LOG.md heartbeat with real local time from the system clock (`date`).
- Stay in your run while reviewers or numerics work; do not end your turn until CP1 is written.
