# Spinning up the new HQ in GH-Bayesian-Variable-Selection

2026-10-29. Companion to `ASTRA_HANDOFF_PLAN.md`; the cutover steps D1–D10 are there. This file covers only how the new HQ thread is born and takes over. Nothing here runs until all empirical work is done and Felipe calls the break.

## Where it lives
- T3 project: "GH-Bayesian-Variable-Selection" (repo FbStatsQuant/Bayesian-Variable-Selection).
- Thread environment: Owls (linked T3 environment `owls`), workspace `/home/fb31/BVS_GH`. HEAD was `eb75737`, clean, on 2026-10-29.
- Leave the nested older clone `/home/fb31/BVS_GH/Bayesian-Variable-Selection` (`39db138`) untouched. Decide about it separately.
- One HQ, one watchdog. The old HQ goes read-only after takeover; it is not deleted.

## Before the thread is launched (during cutover, after D1–D7)
1. In the repo: root `AGENTS.md` (portable rules), a thin `CLAUDE.md` pointing to it, and `Docs/HQ/{CHARTER,STATUS,DECISIONS,OPERATIONS,WATCHDOG,BOOTSTRAP}.md`. Also `Docs/HQ/Memory/` (a curated snapshot of the Claude memory with its index) and `Docs/HQ/Protocols/` (copies of the protocol files HQ relies on, starting with `misc.md` and `campaign.md`).
2. Claude memory on Owls: Claude on Owls has its own memory directory keyed to the Owls path, so the old memory does not follow automatically. Seed it from `Docs/HQ/Memory/`: same files, updated paths, superseded entries dropped.
3. Global `~/.claude/CLAUDE.md` and `protocols/` on Owls: copy them from the PC (`<PC_HOME>\.claude\`) so the protocol classifier works the same there. Check first whether Owls already has a `~/.claude` that would be overwritten.
4. Tools and access from Owls: `ssh nots` (alias, pinned login node), git push to GitHub, R/Python on Owls for small checks, the T3 orchestration tools, and the Claude Personal, Claude Work and Codex (Astra/Sol/Terra) providers, all reachable from the Owls environment.
5. Bulk-data route (Felipe, 2026-10-29): data from NOTS flows into `/home/fb31/BVS_GH` on Owls, in a git-ignored subfolder (e.g. `_data/`). The Owls user quota is the binding limit, not `df`: 2,124 GB used of 3,482 GB on 2026-10-29, so about 1.36 TB free, shared with Felipe's other projects. Check the size of what will move before sending any bulk data.. It stays on Owls only and does not reach GitHub or the PCs.

## Felipe's answers (2026-10-29)
- Data lands in BVS_GH on Owls (above).
- The repo is **PUBLIC**: everything pushed is world-readable. See the open point below.
- PC clones: two local machines, updated automatically through GitHub Desktop; no manual sync step.
- Budget: 250 MiB tracked / 500 MiB `.git` accepted.
- Open: given the repo is public, which of these may be pushed? Unpublished manuscripts, proofs, reviews, campaign records, publisher PDFs. Otherwise make the repo private. To be decided before cutover step D6.

## Launching it
- Create the thread with `t3_thread_launch` in the GH project, with Owls `environmentId`, title "Headquarters", model Opus 5.5 high, full-access, as the first message the bootstrap brief (Astra plan §D, saved as `Docs/HQ/BOOTSTRAP.md`).
- First turn = capability rehearsal, no authority yet: it reads the rules, the memory and the boards; reports the repo commit; runs `ssh nots` with a harmless `hostname`/quota check; launches one tiny Haiku delegate and reads its result; does a test push on a scratch branch; and records anything missing. Felipe checks it from phone or tablet with both PCs closed.
- Sol 6.1 audits the rehearsal against the old HQ's responsibility table (Astra plan §A): can the new HQ do everything the old one did?

## Takeover
1. The old HQ's watchdog is already disabled (D2). The new HQ records itself as sole writer in `Docs/HQ/STATUS.md`.
2. The new HQ schedules its own 30-min watchdog (`schedule_task`, bound to the GH project on Owls) with the same guardrails (no Fable/Astra launches, no method changes, no unapproved NOTS submissions). Terra watches one real watchdog cycle.
3. Astra does a final handoff review; Felipe accepts.
4. The old HQ gets a last message: "Authority transferred to <new HQ link> at <time>; do not act further." It is then settled and archived. The old local folder becomes read-only (D10).

## Rules carried over
Model roles (Opus PM, Fable delicate, Astra theory, Sonnet/Haiku clerical, Sol/Terra audit), no-clutter policy with one dated folder per campaign, the NOTS 10 GB rules and no heavy data on NOTS, no arbitrary constants, headline-only reporting to Felipe, and settling finished delegates. Learning and stats-learning threads are out of scope; Felipe re-spins those manually.
