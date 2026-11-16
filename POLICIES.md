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
  - All theory tickets, including W3-DIST and W3-READER, are under the Theory Department (handover 2026-11-15, owner).
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
- **Models and escalation (owner, 2026-11-15, final).**
  - Departments are independent in using **Opus 5.5, Sonnet 5.5 and Haiku 5.5** (Claude Third unless their charter
    says otherwise; effort high max).
  - **A new Fable 5.2 needs the owner's green light.** If a problem is big enough to need it, the manager reports to HQ:
    the problem, why Opus is not enough, **how many Fables**, the expected size or duration, and the account. HQ passes
    it to the owner, and the owner gives the green light. Fables already approved continue (the W3-DIST lead;
    Engineering's feasibility expert).
  - Big problems are reported to HQ at once.
  - Otherwise every department works on its own: the same repo, the same information, clear goals and resources (charters
    in §8). Technical decisions are the department's, confirmed by HQ.
- **HQ only:** merges to `main`, registry acceptance (CP3 / `--record`), headline changes, protocol amendments,
  supersessions, API batch credits (the Console key stays on HQ's desktop: send HQ "API cards"), and NOTS job
  submission unless HQ delegates it for a named ticket.
- **Self-sufficiency (owner, 2026-11-15):** every department solves its technical problems itself, with its own experts;
  HQ is for gates, budget, merges, API submission and cross-department coordination.
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
- **NOTS:** Owls now has its own login (`ssh nots`, dedicated key `~/.ssh/id_ed25519_nots`, comment "owls-bvs-departments";
  revocable by deleting that line from NOTS `~/.ssh/authorized_keys`). Departments run read-only queries
  (squeue/sacct/sinfo, reading results) themselves. **Job submission still needs HQ's go per ticket** (budget gate); at most 150 concurrent tasks; commons / scavenge.
- **API credits** (Anthropic Console, Fable batches): HQ only.

## 6. Reporting
**The owner centralizes his conversations through HQ** (owner, 2026-11-15). Departments report to HQ only; HQ relays
to the owner what matters: launches, finished milestones, and decisions he must make. Do not message the owner unless
he talks to you first; if he does, answer him and tell HQ what he decided.
Report to HQ at each checkpoint and daily: at most 10 lines with `t3_thread_send`, mode queue, covering what moved,
what is blocked, and what you need. Escalate at once: a counterexample to a target, a WEAKER change to a target clause,
a hold on a consumed claim, a budget overrun, or anything touching a headline claim.

## 7. Operating rhythm (owner, 2026-11-15: "run this like a company")
**Decision rights**

| who | decides |
|---|---|
| Owner (Felipe) | direction, budget tiers, account and budget for every Fable, paper claims, framing and competitors, org changes |
| CEO (HQ) | priorities across departments, resource allocation inside the owner's budget, gates (CP3 acceptance, headline cards with the consultant), merges to main, API submission, launching and closing departments and tickets |
| Department manager | technical decisions (HQ confirms), staffing with Opus/Sonnet inside the allowance, ticket planning and schedule, reviews per PROTOCOL_v4 |

Escalation ladder: manager → HQ (CEO) → HQ's Fable consultant for important or hard operational decisions → owner, only for
the overall direction of the paper and for extra resources.

**Budget envelopes** (set by HQ inside the owner's budget, reviewed weekly):
- Claude Third: Theory and Engineering departments, at most 5 + 3 concurrent leads (Theory 5 until Wed 18:00, then 3).
- Claude Personal: HQ and Writing.
- Codex reviews: priority order W3-DIST > riders > the rest.
- NOTS core-hours: per approved batch.
- API credits: HQ only.

A department that expects to exceed its envelope asks HQ first.

**Cadence**
- **Daily**, by 09:00 CT and whenever a checkpoint lands: each manager sends HQ a report of at most 10 lines. Format:
  done / in progress / blocked / needs (HQ or owner) / budget used.
- **Owner (board):** the owner talks to HQ several times a day, the way a board calls its CEO. HQ is always ready
  with current status (kept in `HQ_NOW.md`). Between calls, HQ messages the owner only for launches, finished milestones
  and decisions he must make. There is no separate weekly digest.
- **Escalation:** a big problem goes to HQ at once (§2 of the memo, §4); anything that needs the owner goes up the same
  day, with a recommendation.

**Records**
- Each department keeps `DECISIONS.md` and `LOG.md` in its folder.
- HQ keeps `HQ_DECISIONS.md` (decisions) and `HQ_NOW.md` (roster, queue, owner batch).
- Nothing important lives only in a chat.

## 8. Department charters (goals and resources)

| department | goal | resources | gates with HQ |
|---|---|---|---|
| SMC - Theory | all theory tickets: W3-DIST (top priority: distribution consistency), W3-READER, riders, premise tickets (T-N, T-PART, T-STREAM, T-CAL, T-MERGE), parallel-SMC campaign, strength gates for headline candidates | Claude Third (Opus/Sonnet/Haiku); up to 5 concurrent leads until Wed 11-18 18:00, then 3; Codex reviews (priority W3-DIST); NOTS read access | CP3 acceptance, headline cards (H5), merges, API submission, new Fables |
| SMC - Engineering | **build the machinery that runs the method at p = 10⁶ on NOTS** (spec, build, ladder 10⁴ → 10⁵ → 10⁶). If that is impossible, **prove it** to HQ, which must approve the proof, with the consultant as needed. Then find the **closest variant of the current strategy that does reach 10⁶**, and if none exists, prove that too (see the mandate below the table) | Claude Third (Opus/Sonnet/Haiku); Owls local runs; NOTS read access; NOTS core-hours per approved batch | job batches, budget tier (owner), paper claim for the parallel method (owner), new Fables, merges |
| SMC - Writing | chapter v2.0, advisor report (~Dec 4–6), later the paper; readable to peers | Claude Personal (Opus/Sonnet/Haiku); LaTeX on Owls | delivery dates, a fidelity check per document, merges |
| SMC - Lean | Lean certificates of headline theorems (launched when material is ready) | to be set at launch | launch, merges |

**Engineering mandate (owner, 2026-11-15, final).** Deliver exactly one of:
1. **A plan** that runs an SMC BVS scheme at p = 10⁶ on NOTS, feasibly and with high precision. Any SMC BVS scheme is
   allowed, modified as needed and validated against the theorem-covered method on an overlap rung (below).
2. **An irrefutable proof that no SMC BVS scheme is feasible at p = 10⁶ on NOTS**, and that the obstruction is NOTS
   infrastructure (a binding resource limit: memory per node or per user, CPUs, wall time, bandwidth, storage), with
   numbers and lower bounds valid for every SMC BVS scheme, not only the current one. Method choices, cost or
   difficulty are not accepted as reasons. HQ approves such a proof, with the consultant, and reports it to the owner.

**Scope of the theory vs the 1M run (owner, 2026-11-15).** The theory stays about the method as described and coded (the
algorithm that runs at 10⁴). To make p = 10⁶ feasible and very precise, Engineering **may modify the algorithm**. That has
no implication for the theory, which is unchanged; the 1M run is the "cherry on top". Requirements on a modified 1M
variant:
- (a) every change from the theory's method is documented;
- (b) on an overlap rung (10⁴, and 10⁵ where possible), the variant and the theory's method are run on the same datasets
  and their outputs compared (selection, PIPs, evidence), so the 1M result is anchored to the method the theorems cover;
- (c) the paper describes the 1M run as an engineered variant validated against the theorem-covered method, not as a
  theorem-covered run.

## 9. Requests for expensive resources (owner controls the traffic, 2026-11-15)
Asking for strong resources to attack a hard problem is **encouraged**: Fable experts, extra NOTS core-hours beyond an
approved batch, API credits, review-heavy campaigns. The owner approves, changes or declines each request; HQ routes it.
A request (from the manager to HQ, ≤ 10 lines) states:
- the problem;
- why the department's own resources (Opus / Sonnet / Haiku, its envelope) are not enough;
- what is asked: model and **count**, duration or size, and the account if the manager has a view;
- the expected payoff;
- what happens if it is declined.

HQ adds its recommendation and forwards it to the owner the same day. Nothing expensive starts before the owner's answer.

## 10. Threads and agents (owner, 2026-11-15)
**Goal: the owner's inbox shows only HQ and the departments.**
- HQ does not start agents on other machines. Work for Owls goes to a department, which starts its own agents.
- Departments start agents **inside their own thread**, either with `delegate_task` on their own environment (a nested
  child of the department) or with native subagents. They never use `t3_thread_launch` for routine work.
- **Departments are the only top-level threads.** A department runs its leads, helpers, reviewers and experts as **its
  own child agents** (`delegate_task` from the department thread), so they stay inside the department and out of the
  owner's sidebar.
- A separate top-level thread is allowed only for a large, independent piece of work: an independent headline theorem,
  or a multi-day campaign the owner may want to talk to directly. The manager says why when launching it.
- Threads already running as top-level finish where they are, no relaunch. New work follows this rule.
- **Let work run; clean up when done** (owner, 2026-11-15). Never cancel, interrupt or delete running work. When a
  **non-department thread** (ticket lead, helper, reviewer, recorder task, expert) has **finished**, its manager
  **settles** it (`t3_thread_organize` action `settle`), so the sidebar shows only HQ, the departments and work in
  progress. Department threads and HQ are never settled. Nothing is archived or deleted unless the owner asks.
