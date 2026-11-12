# W3-PSHARP — three sharpness records for the posterior theorem (ticket T3 of sharp1 TRIAGE)

Lead: Claude Fable 5.2, effort high, Claude Work. Branch `theory/W3-PSHARP` in your worktree; folder
`Theory_work/Wave3/W3-PSHARP/`. Work only there; commit on your branch only (HQ merges). Never effort above high.

## Read first
- `Theory_work/Wave3/PROGRAM.md`, `Theory_work/Wave3/PROTOCOL.md` (rules 9–16 bind you), `Theory_work/INFRA/LIFECYCLE.md`
  §4.1, `INFRA/templates/ASSUMPTION_MAP.md`, `templates/COUNCIL_BRIEF.md`. Consume claims by registry id + version.
- Parents: `Theory_work/Wave3/W3-POST/` (Thm-1, Prop-LB `LB` lemma lines 28–31, Lemma-1a′/1a″, REPORT §4 items 8, 10),
  `Theory_work/Wave3/W3-POST2/STATEMENT.md` v1.2.1 (A2, C2, §6 item 6).
- Why: `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md` §1 rows 11–13 and §2 T3; reviewer texts sharp1/results/f15–f17.md.

## Target (T3)
(a) Lower bound on orthogonal designs with p = n^a, a ≤ 1: δ_n ≥ (1 − o_P(1))(s₀+1)√(log p/(πn)), via a truncated weak
law for e^{χ²₁/2} (tail 1/(w√(π log w)), truncated mean 2√(log p/π), variance p/√(π log p) — re-derive, do not trust).
Makes Theorem 1's rate exact; closes the open √(log n) question.
(b) Corollary of POST2:A2: δ_n ≳ (s₀+1)/(2√n) on every design (keep the multiplicity factor the LB proof discards), so
π(S₀) → 1 needs s₀ = o(√n) and rate r_n needs bounded s₀. Correct the recorded growing-s₀ target (W3-POST REPORT §4
item 8) accordingly.
(c) Counterexample showing ridge-cost control of the reference in Lemma 1a″ cannot be dropped (Remark 2; registry flag
A:COEF-REP), with a numeric check (local only).
These are sharpness records (lower bounds / necessity), not new upper bounds. Design-agnostic where a statement is
general; the orthogonal design in (a) is the lower-bound witness, stated as such. All results asymptotic.

## Legs (HQ pre-approved while Felipe is away: advance when reviews are clean — no open FATAL/MAJOR, council ≥ 8.0)
- CP1: PLAN, STATEMENT v1.0, Sol statement-lock review (codex gpt-6.1-sol, high, blind), numerics for (a) and (c),
  Astra break review (codex gpt-6-astra, high, blind) aimed at breaking the lower bound / counterexample.
- CP2: proofs, Sol checks, council (Sol + Opus 5.5 on Claude Work, high; both ≥ 8.0), reconciliation, REPORT.md with
  the registry block (kind: sharpness record / lower bound; links to the claims they sharpen).
Manifests: `python Theory_work/Wave3/tools/manifest.py freeze ...` / `bind` as in PROTOCOL.

## Operating rules
- Read Theory_work/Wave3/HOLDS.md before each step. Subagents via delegate_task: Sol/Astra on `codex`; Claude helpers on
  `claudeAgent` only, effort ≤ high. NEVER claude-personal. No NOTS use.
- Stay in your run while reviewers work (mode wait). At each checkpoint commit, then end your run with the checkpoint
  summary (≤ 200 words) as your final message; HQ replies in this thread.
