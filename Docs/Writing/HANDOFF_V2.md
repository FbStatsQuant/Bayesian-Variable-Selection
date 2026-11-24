# SMC - Writing Department: handoff to v2 (HQ, 2026-11-23)

The old thread, "SMC - Writing Department" on Owls (about 1,650 items), is retired to cut cache cost (owner ruling,
HQ_DECISIONS c5c69912). The v2 thread starts from this note and the repo; it has no memory of the old thread.

## Read first
1. `POLICIES.md` (repo root), then `Docs/Writing/BRIEF.md`, then `Docs/Writing/DECISIONS.md`.
2. `Docs/Writing/ASSIGNMENT_1.md`: the clarity rules and the paper standard. They still bind.
3. `Docs/Writing/LOG.md`: the history, especially from 2026-11-17 on.
4. `Docs/Writing/ASSIGNMENT_6.md`: **your current task.**

## State at handoff
- **Delivered:**
  - A1: methodology D1 and results D2;
  - A2: the assumptions report;
  - A3: D2 v2;
  - A4: the unified manuscript;
  - A5: the owner's assumption rule, then the vis/FAMC riders.
- **Latest manuscript:** `manuscript/manuscript.tex` at main 193ede8a, compiled as
  `manuscript/manuscript_A5final_famc_2026-11-17.pdf`, plus the Result 3 scope rider. The main text ends at p. 25.
- **Theory is frozen** at the tag `theory-v2026-11-freeze`. The Theory Department is on hold (owner's break), so
  read its files and don't message it.
- **Open items from the LOG:**
  - the related-work reference list (owner);
  - what Q is in Example 3.2 (Theory);
  - the (AG) question (Theory);
  - the TRACK_B v1.4 slips (Theory).

  Carry them as open questions; don't block on them.
- **Quality tracking:** keep logging the gpt-6.2-sol reads in `SOL62_QUALITY.md`.

## Rules for v2
- **Accounts:** the manager runs on Claude Personal, on Owls. Helpers run on Sonnet by default, Opus only for the
  clarity read, and Codex gpt-6.2-sol for the one fidelity read. Effort is high at most.
- **Reporting:** report to HQ only (thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment 1fde6176): a start line and a delivery line, plus
  blockers. HQ doesn't acknowledge status lines. Helpers report to you, never to HQ.
- **Recurring checks:** none are needed. If you add one, run it as a fresh session.
- **Pushing:** push finished work to main promptly; don't leave a long PR tail. Never force-push.
- **Repo safety:** the repo is public. Never commit `Papers/Own_work` or the Song–Liang PDFs (both are gitignored).
