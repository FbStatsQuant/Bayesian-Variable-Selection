# Theory Department: handoff to v2 (HQ, 2026-11-24; owner's order)

The v2 thread "SMC - Theory Department v2" (Claude Work, Opus 5.5 high, Owls) replaces the old Theory thread
(mcp:launch:21e33dae…). The old manager was restarted with a fresh context on 11-24, so it has no handoff of its own.
This note and the files below are your context.

## State (2026-11-24)
- **SMC-BVS is on the owner's BREAK** (HQ_DECISIONS 0a146138, 11-21). **Theory is on HOLD**: start nothing without HQ
  passing on the owner's word.
- The theory is frozen at tag `theory-v2026-11-freeze` (d40c9780, card v1.13). The method is final:
  `method-v3.1.1-listpip` = 7100bb3b.
- Schedules: the Theory heartbeat and the daily report are DISABLED (they were bound to the old thread). Do not
  re-create them unless HQ says so.
- Lean is paused until the three-way sign-off (owner + HQ + VP).

## Done most recently
- **MIS_KL assessment** (11-24, 3258f580), at `Theory_work/Dept/assess/MIS_KL/`. Fable and Astra, working
  independently, both said "pursue a narrow version": a fixed-p KL-projection selection and contraction result as a
  supplement, plus Fable's Target N boundary; no growing-p promise. The manager recommends one Tier B rider on
  W3-MISR-R after the break, about 2–3 lead-weeks. **Owner: the Fable and Astra assessors stay stopped until he calls
  them again through Theory.**

## Queued, on the owner's word only (nothing starts now)
1. The MIS_KL rider (above), once the owner picks it as a theory goal.
2. The large-scale experiment-design survey (HQ_DECISIONS 11-21: read JMLR 21 paper 19-536, then survey large-scale BVS
   experiment designs and extend to 1M; Sonnet/Haiku readers, Opus synthesis).
3. The Monday 11-23 plan, which was paused by the break: item 7, NA_DROP v1.6, dry run, A re-pin, SUMMARY. See
   `QUEUE.md` on dept/theory for the resume order.
4. The owner is setting the **theory goals for a presentation around 12-08**. Input: the A7 spec
   (`Docs/Writing/manuscript/spec/spec.tex`: Theorems 1–6 proved; P1–P4 planned with open choices in App. B) plus P5
   (MIS_KL). He may ask Theory for statement-level work through HQ.

## Read first
1. `POLICIES.md` (repo root) and `Theory_work/Dept/BRIEF.md` (charter).
2. `Theory_work/Wave3/HQ_DECISIONS.md`, the tail from 2026-11-17 on.
3. On branch **dept/theory** (`git fetch origin; git show origin/dept/theory:Theory_work/Dept/<file>`): `QUEUE.md`,
   `LOG.md`, `DECISIONS.md` (they are newer than the copies on main).
4. `Theory_work/Dept/assess/MIS_KL/SYNTHESIS.md`.
5. HQ memory rules, as the owner set them: effort high max; token-lean staffing (serial work; Opus only for hard cores;
   Sonnet bulk; Haiku chores; Codex gates); no swarming on NOTS/Owls; all results asymptotic (never a limitation);
   design-agnostic statements; readable headline theorems; push finished work to main promptly.

## Machines and paths
- Worktree: `/home/fb31/BVS-wt/THEORY-DEPT` (branch dept/theory). Department folders: Owls
  `/home/fb31/SMC_Theory_Department/`, and the same on NOTS (read-only queries only; submissions need HQ).
- Ticket worktrees: `/home/fb31/BVS-wt/<TICKET>`.

## Accounts and reporting
- Manager: Claude Work (owner 11-24). Child agents: Claude Personal unless HQ says otherwise. Codex (Sol gpt-6.2-sol /
  Astra) at effort high. Never a Fable without the owner's word (through HQ).
- Report to HQ only: thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment
  1fde6176-4453-43b0-82cc-70fda5110037. Send short lines, and no status-only messages.
