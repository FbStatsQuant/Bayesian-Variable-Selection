# W3-MISR — C-MIS v2: misspecified-subset theorem without fixed variances (ticket T1 of sharp1 TRIAGE)

Lead: Claude Fable 5.2, effort high, Claude Work. Branch `theory/W3-MISR` in your worktree; folder
`Theory_work/Wave3/W3-MISR/`. Work only there; commit on your branch only (HQ merges). Never effort above high.

## Read first
- `Theory_work/Wave3/PROGRAM.md`, `Theory_work/Wave3/PROTOCOL.md` (rules 9–16 bind you: hard checkpoints, frozen
  manifests + blind first reads, consumed claims by registry id + version, HOLDS.md, heartbeat LOG, kill budget:
  3 failed attempts on the key lemma → STUCK at the checkpoint).
- `Theory_work/INFRA/LIFECYCLE.md` §4.1, `INFRA/templates/ASSUMPTION_MAP.md`, `templates/COUNCIL_BRIEF.md`.
- Parent: C-MIS (Theory_work/Wave1C/C-MIS/ — STATEMENT, lemmas, `L1_reduction.md`), registry rows C-MIS:Thm-MIS(i)/(ii).
- Why this ticket: `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md` §1 rows 4–5 and §2 T1; reviewer text sharp1/results/f05.md.
- New inputs to re-point to: `Theory_work/Wave3/W3-POST2/STATEMENT.md` (v1.2.1: A1, E, C).

## Target (T1)
(a) Lemma R′: exact scale invariance of the coded posterior (y standardised; b = b₀ s_y²), so "σ², τ² fixed" becomes
any σ²_{𝒞,n} > 0 with ‖μ^𝒞‖² ≤ M n σ²_{𝒞,n} and beta-min relative to it; GR on the contrast law only. VERIFY the
invariance against the code path (Scripts/SMC_BVS/core, pin file:line + commit), not only the formulas.
(b) MIS(ii): design-measurable τ²(x), tight (not fixed) envelope constants, s-slicing, and the uniform-over-𝒜_n
conclusion the proof already gives (`L1_reduction.md:114`).
(c) Re-point the input from T03♯ to W3-POST2 (A1/E/C) so MIS inherits (OS)/(ID^M) and the expectation rate.
(d) One remark: Theorem 1 holds with n-dependent σ*² in SNR form.
Goal: remove the recorded gap to Song–Liang Theorem 4. Design-agnostic statements only (families only in examples).
All results asymptotic; p ≤ n^A, p ≫ n the regime that matters.

## Legs (HQ pre-approved while Felipe is away: advance when reviews are clean — no open FATAL/MAJOR, council ≥ 8.0)
- CP1: PLAN, STATEMENT v1.0 (assumption ids, registry block), Sol statement-lock review (codex gpt-6.1-sol, high,
  blind), ASSUMPTION_MAP + boundary numerics (local only, numerics/), Astra better-theorem review (codex gpt-6-astra,
  high, blind). Write CHECKPOINT_1.md.
- CP2: proofs (lemmas/), Sol lemma checks, then council per `.claude` skill "council" practice: Sol + Opus 5.5
  (Claude Work, high) seats ≥ 8.0, reconciliation. Write CHECKPOINT_2.md / REPORT.md with the registry block.
Manifests: `python Theory_work/Wave3/tools/manifest.py freeze ...` / `bind` as in PROTOCOL.

## Operating rules
- Read Theory_work/Wave3/HOLDS.md before each step. Subagents via delegate_task: Sol/Astra on `codex`; Claude helpers on
  `claudeAgent` only, effort ≤ high. NEVER claude-personal. No NOTS use.
- Stay in your run while reviewers work (mode wait). At each checkpoint commit, then end your run with the checkpoint
  summary (≤ 200 words) as your final message; HQ replies in this thread.
