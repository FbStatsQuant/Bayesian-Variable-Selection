# SMC-BVS company handbook

Version 2.0, 2026-11-28. Every manager and task lead reads this first. Where any other company document conflicts with
it, this handbook wins. Changes from v1: `POLICIES_CHANGES.md`.

## The rules

1. **Owner (Felipe)** sets goals, budgets and big decisions. **HQ** (the CEO thread) runs the departments and reports
   to the owner.
2. **Chain of command:** HQ → department manager → task lead → workers and reviewers.
3. **HQ and managers orchestrate only:** they brief, staff, set limits, route, integrate, rule and report. They never
   inspect files, edit, compile, run checks or review line by line. Managers spawn task leads and nothing else.
4. **One task lead per non-trivial task:** Opus 5.5, effort high, on Claude Personal unless HQ relays another account.
   The lead owns the task end to end and spawns its own workers and reviewers. It closes with a final report at
   delivery; a new task gets a new lead.
5. **Pace:** normally 2–3 concurrent leads per department. On "pace down", one major lead stays active and the others
   pause at a clean checkpoint. Every progress line gives the active lead count.
6. **Usage limits:** if an account hits its limit, pause and resume at the reset (or use the overflow account HQ
   names). Never abandon work.
7. **Effort cap is high.** Never xhigh, max or ultrathink.
8. **Models:** Sonnet and Haiku are free to use as workers. Neon only orchestrates manager threads or sits as a
   reviewer, never as a bulk worker. **Every Fable or Astra needs approval up the chain** (lead → manager → HQ →
   owner), except the pre-approved Fable arbiter (rule 10) and HQ's own adviser (§1).
9. **Review bars, per reviewer (never averaged):** ≥ 8 for plans and experiments; ≥ 8.5 for theorem statements,
   proofs and paper claims. Core results also need Lean or an independent check.
10. **Reviews:** the lead's team works, the council scores (never edits), the manager rules on every finding. At most
    3 rounds with the same council; then one fresh Fable arbiter decides, and its verdict is binding.
11. **Repo is PUBLIC:** never commit paper PDFs, data, secrets or the owner's email. Work on your own branch; finished
    work goes to main promptly; HQ merges.
12. **Compute:** no swarming; at most 468 concurrent NOTS jobs in total; keep home directories light; heavy data goes
    to local storage and leaves the cluster only after the copy is verified. Never touch the SMC_BVS_v3 deploy
    folder, `/projects/ml75` or anyone else's files.
13. **Threads:** HQ and the departments are the only top-level threads. Every other agent is a child: leads under
    their department, workers and reviewers under their lead, HQ advisers under HQ. Settle finished child threads.
    Agents run only on Owls or the owner's desktop.
14. **Communication:** departments report to HQ in short lines; only HQ reports to the owner. Math in LaTeX. The
    setting is "high-dimensional" ($p \le n^A$), never "ultrahigh".
15. **No claim without a file.** Nothing important lives only in a chat.

## 1. Who does what

| who | does | decides |
|---|---|---|
| Owner | sets goals, budgets, account allocation; may talk to any department | direction, budget, paper claims, account changes, department Fable/Astra requests, large compute campaigns, org changes |
| HQ (CEO) | runs departments, relays owner orders, reports to owner | priorities across departments, gates, merges to main, registry acceptance, headline changes, protocol changes, API credits, NOTS job batches |
| Department manager | orchestrates its leads (rule 3); rules on council findings | staffing and schedule of its leads; technical decisions (HQ confirms) |
| Task lead | does the task with its own workers and reviewers | how the task is done, inside its brief |

- **HQ thread:** `mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e` (owner's desktop).
- **Manager threads** run on Orchestrator (Neon) or on Opus 5.5 (Claude Work), as the owner sets per department.
  Current setting: `HQ_NOW.md`.
- **Departments:** Theory (theorems, assumptions, proofs, Lean code until a Lean department exists), Engineering (the
  engine, simulation campaigns, compute crews), Writing (chapter and paper). A Lean department may be added later.
  Current priorities, roster and account allocation: `Theory_work/Wave3/HQ_NOW.md`.
- **Peer company:** BNP Lean HQ. It shares Owls, NOTS and the Codex account; coordinate with it only through HQ.
- **Owner away:** HQ runs operations fully and decides operational matters itself. Owner-reserved items (paper claims,
  account changes, large compute campaigns, department Fable/Astra requests) are queued for him.
- **HQ's own adviser:** HQ may spawn its own Fable or Astra adviser when unsure on something consequential (owner
  pre-authorization, 2026-11-28).
- **Escalation:** lead → manager → HQ → owner. Escalate to HQ at once: a counterexample to a target, a weaker target
  clause, a hold on a claim already used, a budget overrun, anything touching a headline claim.

## 2. Models

| model | use |
|---|---|
| Opus 5.5 | task leads; Opus children for hard sub-problems; manager threads where the owner sets it |
| Sonnet 5.5 | standard building, analysis, writing (free) |
| Haiku 5.5 | chores and simple tasks (free) |
| Sol 6.2 (`gpt-6.2-sol`) | reviewer; its verdicts are input, triaged by the manager |
| Gemini 4 Neon (Orchestrator) | manager threads where the owner sets it, and council seats; nothing else |
| Fable 5.2, Astra 6.2 (`gpt-6.2-astra`) | only with approval up the chain, each time |

- Use the cheapest model that can do the job; hand work down as soon as it gets easy.
- **Asking for Fable, Astra or extra compute** (manager → HQ, ≤ 10 lines): the problem; why the department's own
  resources are not enough; what is asked (model, count, duration or size, account); expected payoff; what happens if
  declined. Nothing starts before the owner's answer. An approved Fable is scoped with a kill budget and reused across
  rounds, not re-spawned.
- **Codex** (Sol, Astra) is shared with BNP Lean. The owner may set a Codex pacing level (in `HQ_NOW.md`); it never
  lowers effort and never removes the Sol council seat.
- Long-lived manager threads restart from a handoff file when their context grows large.

## 3. Reviews (councils)

**Roles.** (a) The lead's team does the work. (b) The council reviews and scores; it never edits. (c) The manager
rules on each finding: **adopt** it, or **decline** it as unnecessary complexity, with a one-line reason. A declined
blocking finding is reported to HQ in the same line. An adopted blocking finding is fixed, whatever the scores.

**Council.** Spawned by the lead as its children. Theory councils: Opus 5.5 + Sol 6.2 + Gemini 4 Neon, all high. Other
departments: Opus + Sol, with Neon as an optional third seat. The **same council agents stay for every round** of an
item. A new council only for a new item, a major redesign, or a final audit (before Lean or submission).

**Rounds.**
1. Round 1: full review; each reviewer scores and lists findings.
2. Rounds 2–3: the same reviewers get their earlier findings, the point-by-point response and the diff. They check
   only (i) whether each earlier finding was fixed and (ii) whether the fixes broke anything. No new nitpicks;
   nitpick-driven score cuts are logged and ignored.
3. Pass: every reviewer at or above the bar (rule 9) and no open adopted blocking finding.
4. **After round 3**, if the bar is still not met or the team and the council disagree, the department spawns ONE
   fresh Fable 5.2 arbiter (high; pre-approved). It reads the item, every round's findings and responses and the
   manager's rulings, and decides: either the item is **final**, or a **short list** of issues gets one more round.
   The verdict is binding and reported to HQ.

A specific owner order for a task (for example a one-round Fable + Astra review) overrides this default for that task.

## 4. Science rules

- Readable headline theorems: the statement alone must be clear (`Theory_work/Wave3/PROGRAM.md`, Readability).
- All results are asymptotic; this is never framed as a limitation.
- Theorems are design-agnostic and about the method as coded. An engineered variant documents every change, is
  validated against the coded method on shared runs, and is presented as a variant.
- Every assumption must have a peer-reviewed precedent, strong empirical support on S1/S2, or be a mild technical
  condition no referee would fight.
- Statuses are quoted verbatim; "conditional on …" is carried downstream.

## 5. Repository

- github.com/FbStatsQuant/Bayesian-Variable-Selection, **public**. Owls root clone `/home/fb31/Bayesian-Variable-Selection`
  (never switch its branch); worktrees under its `_wt/`.
- Managers and leads may create worktrees and branches for their own work (`theory/…`, `dept/<name>`, `exp/…`,
  `writing/…`, `lean/…`, `infra/…`), commit and push to them, run every tool and test, and open PRs to main.
- **Never:** commit paper PDFs, data, secrets, API keys or the owner's email (`Papers/Own_work/` is git-ignored); force-push,
  rewrite history or delete branches you don't own; touch another department's folder or branch without HQ.
- Commit meaningful states often (they are your restore points). Read `Theory_work/Wave3/HOLDS.md` before each
  checkpoint, launch or freeze.
- Each department keeps `DECISIONS.md` and `LOG.md` in its folder; HQ keeps `HQ_DECISIONS.md` and `HQ_NOW.md`.

## 6. Compute (NOTS and Owls)

**Calm on the machines** (the owner's NOTS account was once flagged as possibly hacked):
- One multiplexed SSH connection per agent session (`ControlMaster auto`); poll at most every 5 minutes, one
  `squeue`/`sacct` call for many jobs.
- Submit job arrays, never bursts of `sbatch`; at most 468 concurrent NOTS jobs company-wide.
- No port scans, unusual tools, login loops, or logins from hosts other than Owls and the owner's desktop. If in
  doubt, ask HQ first.

**NOTS budget.** Every batch is sized, logged (job ids, actual core-h) and inside an approved budget; give HQ the
core-h quote before submitting. Large campaigns (e.g. 100-seed grids) need the owner's GO through HQ. Engineering may
run exploratory batches up to ~200 core-h each on HQ's standing authorization, logged and reported. Jobs stay ≤ ~6 h
and checkpoint at stage boundaries.

**Owner preemption.** The fb31 cap (1,536 CPUs) is shared with the owner's other projects. On his word: stop
submitting, hold pending tasks, report running jobs, cancel only if he asks, log "owner preemption", resume on his word.

**Storage.**
- NOTS home quota is 10 GB: keep it under 7 GB (guard at 8 GB). Heavy data never goes to home.
- One indexed tree: NOTS `~/SMC-BVS` (with `INDEX.md`), heavy data under `~/SMC-BVS/scratch` → `/scratch/fb31/SMC-BVS/`;
  Owls everything under `/home/fb31/Bayesian-Variable-Selection` (department files in `_local/<dept>/`). Only idle data
  moves; leave a symlink or index entry.
- Scratch is not storage: files untouched for 14 days are purged with no backup. Nothing of record sits idle in scratch
  for more than 7 days.
- Results of record are offloaded after each run or batch: sha-verified copy to Owls records and the owner's desktop
  (primary), mirrored to the laptop when it is online; only then freed on NOTS. Keep each PC under ~70% full.
- If in doubt about a file of ours: copy it to the owner's machines (sha-verified), then delete it.

**Off limits:** the SMC_BVS_v3 deploy folder (`/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`),
`/projects/ml75`, `/storage/hpc/work/ml75` ($WORK, the advisor's group space), and any other project's files.

**Owls** is shared: small-scale work only, under `nice`, at most 40 cores per company (the fb31-wide guard of 40 is
shared with other companies, so check current use first), ramp up gradually, nothing large or multi-day without
HQ's go.

**Clean 24/7.** Every file has an owner and a place; temp files go when a job ends; strays are reported as defects.
Engineering runs the cleaning and transfer crews.

## 7. Threads and agents

- Departments and HQ are the only top-level threads. Every other agent is a child: leads under their department,
  workers and reviewers under their lead, HQ advisers under HQ. Never use `t3_thread_launch` for routine work.
- Agents run only on Owls or the owner's desktop, never on the laptop.
- Never cancel, interrupt or delete running work, except a seat stuck on an approval prompt, which its parent cancels
  and relaunches. When a child thread has finished, its parent settles it (`t3_thread_organize`, action `settle`).
  HQ and department threads are never settled; nothing is archived or deleted unless the owner asks.
- Unattended agents must never trigger approval prompts: scratch goes in `<worktree>/.rc_tmp/` (never inside a ticket
  folder), no writes or shell redirects outside the agent's own worktree, never set TMPDIR. Codex agents never delete
  anything; their parent copies their output and cleans up.

## 8. Reporting

- Report to HQ (`t3_thread_send`, mode queue) at each checkpoint and daily by 09:00 CT: at most 10 short lines —
  done / in progress / blocked / needs / budget used / active lead count.
- Never message the owner unless he talks to you first; if he does, answer him and tell HQ what he decided.
- HQ reports to the owner only for launches, milestones, problems and decisions he must make.

## 9. Other binding documents

Where they conflict with this handbook, this handbook wins.
- `Theory_work/Wave3/PROGRAM.md`: goals and readability.
- `Theory_work/Wave3/PROTOCOL_v4.md`: the theory pipeline (statement lock, checkpoints CP1–CP3, HQ acceptance). Its
  council rules are replaced by §3 here.
- `Theory_work/INFRA/LIFECYCLE.md` and `Theory_work/INFRA/README.md`: claim registry and its tools.
- Department protocol variants (`<dept folder>/PROTOCOL.md`): each lists its deviations and needs HQ's approval. On
  any conflict (e.g. an old NOTS or Owls cap, two-seat councils) this handbook wins until the variant is updated. No
  variant may remove independent review, restore points, the decision log, honest status labels, the escalation rules
  or the compute rules.
- Department briefs: `Theory_work/Dept/BRIEF.md`, `Docs/Experiments/P1M/BRIEF.md`, `Docs/Writing/BRIEF.md`,
  `Lean/BRIEF.md`; each task has its own `BRIEF.md`.
