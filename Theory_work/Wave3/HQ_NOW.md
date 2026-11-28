# HQ now (resume card; HQ keeps this current)

Refreshed 2026-11-28. Rules: `POLICIES.md` (v2.0). Decisions and their history: `HQ_DECISIONS.md`. Entries older
than this refresh are in git history.

## CURRENT PRIORITIES (owner; see HQ_DECISIONS 2026-11-25 to 2026-11-28)
1. **Top priority: assumptions and proofs (Theory).** Done when (1) every assumption is accepted company-wide as
   reasonable and adequate, and (2) every targeted theorem (density, selection, misspecification) has at least a
   partial, promising, council-reviewed proof. Until then Theory gets accounts and agents first, with one dedicated
   Fable 5.2 (Claude Personal) and one Astra 6.2 adviser. Definitive proofs and Lean follow.
2. **Theory scope:** Song–Liang 1-to-1 only (true model, true distribution, misspecification). Other extensions wait
   until these have proofs and Lean code.
3. **Writing:** PAPER-DRAFT (one LaTeX project, 3 Opus leads). CITE-AUDIT of the theory citations runs alongside.
4. **Engineering:** SMC-PERF deep dive and CAMPAIGN-OPS (S2 ASI completion, S2 final, hygiene).
5. Simulation suite is S1 + S2 only. The p = 10⁶ project comes last.

## DEPARTMENTS / ACTIVE THREADS
All departments run on the Owls environment `b18966a3-98dd-4510-a488-d5dfb1650daa`.

| thread | id | worktree | branch | manager model |
|---|---|---|---|---|
| SMC - Engineering | `mcp:launch:81cb86a5dee3bab7b1224fda192e57da97f15ffbd65a7b15c351bf4bb92291c0` | `/home/fb31/BVS-wt/P1M` | `exp/P1M` | Opus 5.5 (Claude Work) |
| SMC - Theory | `mcp:launch:9b7e3aec8c798b6db80b42cfd9a4c8a8235538d4ae909a408a45a6c955c7b3b9` | `/home/fb31/Bayesian-Variable-Selection/_wt/THEORY-DEPT` (old path symlinked) | `dept/theory` | Orchestrator (Neon) |
| SMC - Writing | `mcp:launch:3533e1d6e710c91c7fe41094cfbeec715ffc82883e32a6386d64d9b4845b06e5` | `/home/fb31/Bayesian-Variable-Selection/_wt/WRITING` (old path symlinked) | `writing/main` | Orchestrator (Neon) |

- **HQ:** `mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e`, desktop environment `1fde6176-4453-43b0-82cc-70fda5110037`,
  Claude Work, Opus 5.5 high.
- **Peer:** BNP Lean HQ, `mcp:0a4bc001-e5d5-40be-b36a-3d4f45984c49`.
- No Lean department yet; Lean work belongs to Theory.

## ACCOUNT ALLOCATION (owner sets; HQ relays to all managers)
- **Manager threads:** as in the roster above (owner sets per department).
- **Task leads:** Claude Personal by default (the owner adjusts by usage). Engineering currently runs its leads (and
  its Claude workers and reviewers) on Claude Third.
- **HQ:** Claude Work.

## CODEX PACING LEVEL (owner sets; POLICIES §14): **1 (light pacing)** since 2026-11-16 late (owner: "let's have a surplus to burn when we actually need it"; Codex at 95% with the weekly reset in 6d20h). Previously 0.
