# Theory Wave 2 — protocol (binding for every worker thread)

Set by Theory HQ on 2026-11-09, under Felipe Bedoya's greenlight ("I want this to get done; you design the agentic
structure; thorough reviewers and a council; come back with final answers"; providers ≈ 2/3 Claude Personal,
1/3 Claude Work; ample resources).

**This file extends `Theory_work/Wave1C/PROTOCOL.md`, which extends `Theory_work/Wave1/PROTOCOL.md`. Read both
first: every rule there applies here** (three review layers; statement lock; lemma-by-lemma cross-family checks with
falsification numerics; independent mid-point; exhaustive sweep; council = Codex gpt-6.1-sol + Claude Opus 5.5, both
≥ 8.0 with all six gates in the same round, max 3 rounds; anti-hallucination rules: no claim without a file, citation
check script, reviewers briefed to break, statuses verbatim), with the folder `Theory_work/Wave2/<TICKET>/` and the
changes below.

## Goal
The paper's consistency results must apply to the design matrices people actually use. Wave 1/1C proved
reported-model consistency for **local** correlation (bounded or O(log n) relevance sets: GEN, GROW). The gap is
**pervasive** correlation — factor / equicorrelated designs with growing p (study scenario S5) — plus an honest map of
which real designs satisfy the conditions. Ground truth: `Theory_work/Wave1C/FINAL/consistency.pdf` (v1.0,
council-passed) and its sources; `Theory_work/State_of_Project/State_of_Project_v1.1.pdf` (§07).

**Scope rule (Felipe, binding):** all target results are asymptotic. Do not treat "asymptotic only / not at n = 200"
as a limitation, do not pursue finite-n bounds, and do not list them as caveats.

## The method
The target method is the production core **as merged on main at 4676af6** (v3.1: LS0 from the start mode with move
cap ℓ_n + |S̃₀|, tie-aware start-mode DP, tier-1 calibration fallback; `Scripts/SMC_BVS/core/`; spec: SoP
`02_method.tex` + `Theory_work/Wave1C/FINAL/sections/s7_impl.tex`). If a proof genuinely needs a different parameter
of LS0 or of the final local search (not of the prior, SMC kernels, calibration law or tables), specify the minimal
change, show numerically that it matters, flag it at the top of REPORT.md and in METHOD_REQUIREMENTS.md; HQ decides.

## Timeline (HQ wakes on reports; no fixed clock deadline)
Write `CHECKPOINT.md` when your key lemma is proved or after ~3 hours, whichever is first (HQ may redirect). Then run
to completion: PROVED-CHECKED, or the strongest checked partial result with an exact obstruction (a checked
counterexample or a proof that a condition is necessary counts as closing the question).

## Models
Leads as assigned by HQ. **Effort cap (Felipe, 2026-11-09, binding, overrides every earlier protocol): every agent —
Claude or OpenAI — runs at effort/reasoningEffort `high` at most; never xhigh, max, ultrathink or ultra.** Cross-family
reviewers: Codex gpt-6.1-sol at high; where a stronger OpenAI reviewer is needed (key lemma, mid-point, sweep, council
seat), use gpt-6-astra at high. Parallel provers: Codex gpt-6.1-sol or Opus subagents. gpt-6-astra and Claude Fable 5.1: short hard
steps only, ≤ 3 calls per ticket, reason logged. Helpers: Sonnet/Haiku on your own provider. Subagents may spawn
subagents; the lead stays responsible.

## Tickets
| ID | Lead | Target |
|---|---|---|
| W2-FAC-A | Opus, Claude Personal | Reported-model consistency on factor / equicorrelated designs with growing p (S5), route A: low-rank common-component split |
| W2-FAC-B | Opus, Claude Work | Same target, route B (independent): start-mode structure + path-restricted no-addition |
| W2-APP | Opus, Claude Personal | Applicability map: which design classes and real designs satisfy the conditions |
FAC-A and FAC-B do not coordinate; HQ compares and merges. Each must still complete its own review pipeline.
