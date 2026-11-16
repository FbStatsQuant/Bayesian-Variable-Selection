# SMC-BVS — company handbook (policies, pipeline, access) — HQ, 2026-11-15

Every department and every ticket lead reads this first. It points to the binding documents; where it summarises them,
the documents win.

## 1. Organization (owner, 2026-11-15)
- **Owner: Felipe.** Sets goals, decides budget and big-picture questions; may talk to any department directly.
- **CEO: Theory HQ.** Thread `647bfd65-83bc-403a-b3b0-0a8352044e7f`, environment `1fde6176-4453-43b0-82cc-70fda5110037`
  (owner's desktop). HQ runs all departments and reports to the owner when he asks.
- **Department managers** report to HQ. Current roster: `Theory_work/Wave3/HQ_NOW.md` "DEPARTMENTS / ACTIVE THREADS".
  - SMC - Theory Department: theory tickets.
  - SMC - Engineering Department: engine, p = 1M.
  - SMC - Writing Department: chapter, paper, advisor report.
  - Lean department: certificates.
  - Tickets directly under HQ: W3-DIST, W3-READER.
- **Advisors:** HQ consultant (Fable 5.2), the second signature on headline changes (PROTOCOL_v4 H5).

## 2. Binding policies (read in this order)
1. `Theory_work/Wave3/PROGRAM.md`: goals, presentation rule, **Readability** (clear statements, reader versions, full
   notation; proofs may be as hard as needed if checked).
2. `Theory_work/Wave3/PROTOCOL_v4.md`, with amendments H1–H6: tiers, review chain, council rules, DEPS trace, STATEMENT
   changelog, checkpoints, acceptance, rollback, restore points, NORMAL / EFFICIENT modes.
3. `Theory_work/INFRA/LIFECYCLE.md`: claim registry operations (accept, supersede, patch, narrow, retract, propagate).
4. `Theory_work/INFRA/README.md`: registry tools (`bvsreg`, `check.py`, `ingest.py`, `registry.py`, `propagate.py`,
   `assemble.py`, `test_lifecycle.py`) and CI (`Theory_work/INFRA/ci/run_ci.py`).
5. `Theory_work/Wave3/HQ_NOW.md` (current plan and queue) and `Theory_work/Wave3/HQ_DECISIONS.md` (decision log).
6. Department briefs: `Theory_work/Dept/BRIEF.md`, `Docs/Experiments/P1M/BRIEF.md`, `Docs/Writing/BRIEF.md`,
   `Lean/BRIEF.md`. Each ticket has its own `BRIEF.md`.

Standing rules everywhere:
- effort **high** max (never xhigh / max / ultrathink);
- all results asymptotic (never framed as a limitation);
- design-agnostic theorem statements;
- theorems are about the method as coded;
- statuses quoted verbatim; "conditional on …" carried downstream;
- no claim without a file.

## 3. Pipeline (theory)
BRIEF → statement lock → **CP1** (TARGET.md: assumption map, parity table, boundary numerics, better-theorem review,
reader version) → lemmas with line checks (DEPS.tsv; freeze rule) → **CP2** (key-lemma break review) → sweep →
citation check → council (two seats; only C/S/F block; diff round) → **CP3** → HQ acceptance into the registry → merge.
Engineering and compute tickets follow their own DESIGN.md plus the output-preservation contract. Writing follows
PROGRAM Readability, with a fidelity check of every number.

## 4. Access and autonomy
- **Repo:** github.com/FbStatsQuant/Bayesian-Variable-Selection (public for now; the owner will make it private).
  Clones:
  - Owls `/home/fb31/Bayesian-Variable-Selection` (shared root clone; don't switch its branch);
  - worktrees under `/home/fb31/BVS-wt/`;
  - the desktop (HQ).

  Push credentials are configured on Owls.
- **Department managers and ticket leads may**:
  - create worktrees and branches for their own work (`theory/<TICKET>`, `dept/<name>`, `exp/…`, `writing/…`,
    `lean/…`, `infra/…`);
  - commit and push to **their own branches**;
  - run every tool, test and dry run;
  - open PRs to `main`;
  - start reviewers and helpers within their brief's allowance.
- **HQ only:** merges to `main`, registry acceptance (CP3 / `--record`), headline changes, protocol amendments,
  supersessions, API batch credits (the Console key stays on HQ's desktop: send HQ "API cards"), and NOTS job
  submission unless HQ delegates it for a named ticket.
- **Never:**
  - force-push, rewrite history, or delete branches you don't own;
  - commit secrets, API keys, the owner's email in new files, or unpublished papers (`Papers/Own_work/` is
    gitignored, and so are copyrighted PDFs);
  - touch another department's folder or branch without HQ;
  - touch `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/` or `/projects/ml75` on NOTS.
- **Restore points:** HQ's snapshot cron commits each department or ticket folder every 15 min
  (`~/.config/bvs-hq/snap/`). Commit your own meaningful states too.
- **Holds:** read `Theory_work/Wave3/HOLDS.md` before each checkpoint, launch or freeze.

## 5. Resources
- **Claude Third:** ample; the default for Owls departments; Opus default, Fable for hard proofs or creative reviews.
- **Claude Personal:** HQ and the Writing Department; budget resets Monday 16:00 CT.
- **Claude Work:** as HQ says.
- **Codex** (Sol `gpt-6.1-sol`, Astra `gpt-6-astra`, high): one shared Codex Pro account, also used by the owner's BNP
  Lean project. NORMAL mode until HQ switches it.
- **NOTS:** via HQ, or the Engineering Department per its brief; at most 150 concurrent tasks; commons / scavenge.
- **API credits** (Anthropic Console, Fable batches): HQ only.

## 6. Reporting
**The owner centralizes his conversations through HQ** (owner, 2026-11-15). Departments report to HQ only; HQ relays
to the owner what matters: launches, finished milestones, and decisions he must make. Do not message the owner unless
he talks to you first; if he does, answer him and tell HQ what he decided.
Report to HQ at each checkpoint and daily: at most 10 lines with `t3_thread_send`, mode queue, covering what moved,
what is blocked, and what you need. Escalate at once: a counterexample to a target, a WEAKER change to a target clause,
a hold on a consumed claim, a budget overrun, or anything touching a headline claim.
