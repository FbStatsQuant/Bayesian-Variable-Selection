# Theory Wave 3 — protocol (binding)

Extends `Theory_work/Wave2/PROTOCOL.md` (which extends Wave1C and Wave1): three review layers (statement lock;
lemma-by-lemma cross-family checks with falsification numerics; independent mid-point; exhaustive sweep; council of one
OpenAI seat + one Claude seat, both ≥ 8.0 with all six gates in the same round, max 3 rounds), anti-hallucination rules
(no claim without a file; citation-check script; statuses verbatim; reviewers briefed to break). Folder:
`Theory_work/Wave3/<TICKET>/`. Read `Theory_work/Wave3/PROGRAM.md` first: it defines the target package.

## Changes in Wave 3
1. **Effort cap:** every agent, Claude or OpenAI, at effort/reasoningEffort `high` at most — never xhigh/max/ultrathink.
   Strong OpenAI reviewer = gpt-6-astra (high); routine = gpt-6.1-sol (high).
2. **Providers (until further notice):** Claude Personal (`claude-personal`) runs **only Claude Fable 5.2**. Every
   Opus/Sonnet/Haiku agent, including your subagents and council seats, runs on **Claude Work** (`claudeAgent`).
   OpenAI agents on `codex`.
3. **Sharpness gate (before heavy proving):** after the statement lock, write `ASSUMPTION_MAP.md` — one page: where
   each assumption enters the proof sketch and whether it looks necessary; run **boundary-violation numerics** (simulate
   just outside each assumption; if the conclusion still holds, flag the assumption `improvable`); and get one fresh
   **"better theorem" review** (Astra high) asked only to propose a strictly better provable statement. Record the
   outcome; HQ decides whether to strengthen the target before proving.
4. **Design-agnostic statements:** no design family in any theorem statement; families only as examples.
5. **Interface properties:** a shared assumption A enters through one bridge lemma A ⇒ P; theorems consume P.
6. Token efficiency: grep and targeted reads; summarise; do not paste long files into replies.
7. Final report as before, plus: assumptions list with ids, `implies` relations to existing results, and the
   sharpness record (for the registry being built in `Theory_work/INFRA/`).
8. **Registry block (from 2026-11-10):** every REPORT.md ends with the registry block from
   `Theory_work/INFRA/templates/ASSUMPTION_MAP.md` (on branch `theory/infra` / PR #6 until merged), with per-clause
   statuses — one status per claim, never one status for a bundle of results.
