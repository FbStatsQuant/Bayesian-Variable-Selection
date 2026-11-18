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
  - Departments are independent in using **Opus 5.5, Sonnet 5.5 and Haiku 5.5** (Claude Personal unless their charter
    says otherwise; effort high max).
  - **A new Fable 5.2 needs HQ's approval** (owner delegated Fable allocation to HQ, 2026-11-16: "be efficient, we
    need to save tokens for future tasks"). If a problem is big enough to need it, the manager reports to HQ: the
    problem, why Opus is not enough, how many Fables, the expected size or duration, and the account. HQ decides,
    with the consultant when it is significant.
    - Fables are **precision tools, not volume tools** (owner, 11-16). They go only to hard key proofs, finding
      improvement opportunities in core results, creative or architect reviews, writing advice, and headline cards. They are
      scoped with a kill budget and reused (the same thread across rounds) rather than re-spawned.
    - Opus is the default everywhere else.
    - HQ reports Fable use to the owner in the daily brief.
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
  - touch the SMC_BVS_v3 deploy folder (`/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`) or `/projects/ml75` on NOTS.
- **Restore points:** HQ's snapshot cron commits each department or ticket folder every 15 min
  (`~/.config/bvs-hq/snap/`). Commit your own meaningful states too.
- **Holds:** read `Theory_work/Wave3/HOLDS.md` before each checkpoint, launch or freeze.

## 5. Resources
**Account allocation is set by the owner** (2026-11-15). Depending on which Claude account is running dry, he tells HQ
which account (Claude Third, Claude Personal, Claude Work) or which proportions to use for new agents, and HQ relays it
to every manager. Managers apply the current allocation, recorded in `HQ_NOW.md` "ACCOUNT ALLOCATION", to every new
agent they start.
- **Claude Personal:** the **SMC default account since 11-16 16:00 CT** (owner): HQ, Theory, Engineering and every
  new SMC agent. Its budget resets Monday 16:00 CT.
- **Claude Third:** **retired for SMC** (owner, 11-16). No SMC agent starts or resumes on it.
- **Claude Work:** the Writing Department and its Fable writing advisor (owner, 11-16); otherwise as HQ says.
- **Codex** (Sol `gpt-6.1-sol` (owner 11-17 evening: keep 6.1 as default until HQ's 6.1-vs-6.2 recommendation; 6.2 only in the SOL62 A/B), Astra `gpt-6-astra`, high): one shared Codex Pro account, also used by the owner's BNP
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
| Owner (Felipe) | direction, budget tiers, account allocation (Fable allocation delegated to HQ 11-16), paper claims, framing and competitors, org changes |
| CEO (HQ) | priorities across departments, resource allocation inside the owner's budget, gates (CP3 acceptance, headline cards with the consultant), merges to main, API submission, launching and closing departments and tickets |
| Department manager | technical decisions (HQ confirms), staffing with Opus/Sonnet inside the allowance, ticket planning and schedule, reviews per PROTOCOL_v4 |

Escalation ladder: manager → HQ (CEO) → HQ's Fable consultant for important or hard operational decisions → owner, only for
the overall direction of the paper and for extra resources.

**Budget envelopes** (set by HQ inside the owner's budget, reviewed weekly):
- Claude Personal (since 11-16): HQ, Theory (≤ 3 leads + the audit Fable) and Engineering (≤ 4 concurrent agents).
- Claude Work: Writing.
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
| SMC - Theory | all theory tickets: W3-DIST (top priority: distribution consistency), W3-READER, riders, premise tickets (T-N, T-PART, T-STREAM, T-CAL, T-MERGE), parallel-SMC campaign, strength gates for headline candidates | Claude Personal (Opus/Sonnet/Haiku); up to 3 concurrent leads + the audit Fable; Codex reviews (priority W3-DIST); NOTS read access | CP3 acceptance, headline cards (H5), merges, API submission, new Fables |
| SMC - Engineering | **build the machinery that runs the method at p = 10⁶ on NOTS** (spec, build, ladder 10⁴ → 10⁵ → 10⁶). If that is impossible, **prove it** to HQ, which must approve the proof, with the consultant as needed. Then find the **closest variant of the current strategy that does reach 10⁶**, and if none exists, prove that too (see the mandate below the table) | Claude Personal (Opus/Sonnet/Haiku), ≤ 4 concurrent agents; Owls local runs; NOTS read access; NOTS core-hours per approved batch | job batches, budget tier (owner), paper claim for the parallel method (owner), new Fables, merges |
| SMC - Writing | chapter v2.0, advisor report (~Dec 4–6), later the paper; readable to peers | Claude Work (Opus/Sonnet/Haiku + one Fable writing advisor); LaTeX on Owls | delivery dates, a fidelity check per document, merges |
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

- **Where threads and agents run (owner, 2026-11-15):** only on **Owls** or the **desktop (DESKTOP-955G53S)**, which are
  always on, so work continues 24/7. Never on the laptop (Felipe_Bedoya): it goes on and off. The laptop is only a data
  mirror, reached by its own scheduled pull or by a short, explicitly approved one-off.

## 11. Overnight mode (owner, 2026-11-15; times in US Central)
When the owner says he is going to bed or leaving HQ working overnight, **HQ is in charge of all decisions** until he
says he is back. That includes the owner-reserved items (Fable requests, extra resources, account allocation), which HQ
decides with its Fable consultant for anything important. Limits:
- stay within the budget envelopes and accounts already in use;
- nothing irreversible or outward-facing: no repo visibility change, no deletion, no external publication;
- every decision is logged in `HQ_DECISIONS.md` with a "(overnight)" tag.

When the owner is back, HQ gives a short morning brief: what was decided, what moved, and what needs him.

## 12. Compute discipline on NOTS and Owls (owner, 2026-11-15): "military order and discipline"
1. **Use NOTS as much as needed, 24/7**, professionally: every job batch is sized, logged (ids, actual core-h) and inside an
   approved budget. Never touch the SMC_BVS_v3 deploy folder (now `/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`, moved 11-04; formerly `projects/BVS/SMC_BVS_v3/deploy/`) or `/projects/ml75`.
2. **The home folder never clogs** (10 GB quota). Heavy data is never written to home; it goes to `/scratch/fb31/`. A cleaning
   crew checks home every day (guard threshold 8 GB, target below 7 GB) and cleans caches, logs and temp files.
3. **Heavy experiment data, when an experiment is done**, is downloaded to the owner's laptop (Felipe_Bedoya) at
   `C:\Users\felip\Documents\<folder named by Engineering>`, then removed from NOTS scratch once the copy is verified
   (checksums). HQ sets up the transfer route with the owner before the first heavy dataset. Until then, data stays in scratch.
4. **One unified, indexed SMC-BVS tree on NOTS**, kept organized continuously. No stray or "flying" folders.
   - The tree is in scratch, with home kept minimal. An `INDEX.md` at its root records what lives where and its provenance.
   - Only idle data moves: nothing used by queued or running jobs. Old paths get a symlink or an index entry.
   - The exclusions in rule 1 stay untouched.
5. **Owls is fair game for small-scale computation.** It is a shared server: use `nice`, cap concurrent cores (≤ 16 unless
   HQ approves more), and run nothing large or multi-day. Outputs live in the owning worktree or folder; no clutter in
   `/home/fb31`.
6. **NOTS and Owls must look squeaky clean 24/7.** Every file has an owner and a place, temp files are removed when a job
   ends, and stray files are a defect reported in the daily report.

Owner: the SMC - Engineering Department runs the crews (cleaning, transfer, organization). The Theory Department follows the
same rules for anything it runs.
7. **Be calm on the machines: no swarming** (owner, 2026-11-15; two weeks ago his NOTS account was flagged as possibly
   hacked).
   - SSH: one multiplexed connection per agent session (`ControlMaster auto`, `ControlPersist`), never bursts of
     parallel logins. Polling every 5 minutes at most; prefer one `squeue`/`sacct` call that covers many jobs.
   - Job submission: in planned batches (job arrays, not hundreds of separate `sbatch` calls in a burst), within the
     150-task cap.
   - No port scans, no unusual tools, no scripted login loops, no logins from unfamiliar hosts beyond Owls and HQ's desktop.
   - Owls: no sudden spikes. Ramp up gradually and keep within the core cap.
   - If anything looks like it could trigger a security alert, ask HQ first.
8. **The Engineering Department works only inside its folders** (owner, 2026-11-15):
   - **Owls:** `/home/fb31/SMC_Engineering_Department/`.
   - **NOTS:** `/home/fb31/SMC_Engineering_Department/`, created by the owner, with heavy data under
     `/home/fb31/SMC_Engineering_Department/scratch`, a symlink to `/scratch/fb31/SMC_Engineering_Department/`.

   No Engineering file anywhere else: temp files, logs, job scripts, outputs and crews all live inside. The exceptions are
   its git worktree on Owls (repo code only) and Slurm's own spool. Existing SMC-BVS material is moved in by the
   reorganization plan (idle data only).
9. **Every department gets its own folder on each machine** (owner, 2026-11-15), named `SMC_<Name>_Department` under
   `/home/fb31/` (e.g. `SMC_Lean_Department` at its launch), with a `scratch` link on NOTS when it needs heavy data. Each
   department works only inside its own folders.
10. **Engineering uses NOTS heavily** (owner, 2026-11-15: "they are an engineering department, not theoreticians"). It
    measures rather than estimates. It holds a standing authorization for exploratory batches up to ~200 core-h each inside
    the approved budget, each logged and reported. Bigger batches and the gated stages go to HQ.
11. **Owner preemption of NOTS** (owner to Engineering, 2026-11-15). The fb31 per-user cap (1,536 CPUs, 2,304 GB) is shared
    with the owner's other projects. On his word, departments **clear the way**:
    - no new submissions; pending tasks held;
    - report the running jobs (ids, CPUs, expected end, checkpointed or not);
    - if he needs the capacity now, cancel the blocking jobs (his explicit request);
    - log it as "owner preemption", not a failure;
    - resume when he says the way is clear.

    Design consequence: jobs stay ≤ ~6 h and checkpoint at stage boundaries.
12. **NOTS scratch is not storage** (CRC KB 147975): files untouched for **14 days** are purged (by access time; `mv` keeps
    the old access time; staff may purge earlier; no backup). Nothing of record stays idle in scratch for more than 7 days.
    Records of record are copied (rsync with checksums) to the department's Owls folder (NFS), and later to the owner's
    laptop. `$WORK` `/storage/hpc/work/ml75` is the advisor's group space: never touch it.
13. **Continuous offload** (owner, 2026-11-15): the desktop (always on; path from the owner) and the laptop each have
    about 1 TB. Results of record are pumped off NOTS continuously, after each run or batch: checksummed to the desktop
    (primary), mirrored to the laptop when it is online, then NOTS scratch is freed. Each PC stays under ~70% for our
    data.

## 13. Department protocols: tailored, but in order (owner, 2026-11-15)
Each department may tailor the review, process and rollback protocols to its needs. Order is kept this way:
- **One company baseline:** `Theory_work/Wave3/PROTOCOL_v4.md` and `Theory_work/INFRA/LIFECYCLE.md`. Anything a
  department does not override follows the baseline.
- **One written variant per department,** in its folder: `<dept folder>/PROTOCOL.md` (e.g.
  `Docs/Experiments/P1M/PROTOCOL.md`, `Theory_work/Dept/PROTOCOL.md`). It lists each deviation from the baseline and
  why. A variant that only exists in chat does not count.
- **Company minimums that no variant may remove:**
  - independent review before anything is called checked, validated or done;
  - restore points and a rollback path for every deliverable;
  - a decision log;
  - honest status labels;
  - the escalation rules (§4, §9);
  - the compute discipline (§12).
- **HQ approves each variant and each change to it**, with the consultant when the change is significant, and logs it
  in `HQ_DECISIONS.md`. Until a variant is approved, the baseline applies.

## 14. Codex pacing levels (owner, 2026-11-15)
The owner says "pace to level N"; HQ relays it to every manager the same day. **A pacing level is not a reasoning effort:** Codex reviewers always run at effort high, at every level. Reviews already in flight finish as
started.

| level | Codex (Sol / Astra) used for | moves to Claude (Opus / Fable) |
|---|---|---|
| **0, normal** (default) | all independent reviews | none |
| **1, light pacing** | statement locks, key-lemma line checks, council OpenAI seats, break reviews | line checks off the key path, re-checks of repairs, fidelity reads |
| **2, efficient** (PROTOCOL_v4 §2A) | only locks, key lemmas, council seats; reviewer sessions reused where blind first reads don't matter | everything else |

**No level drops a Codex check on what we call checked:** statement locks, key lemmas and the council OpenAI seat. The current
level is recorded in `HQ_NOW.md`.

**Unattended agents never wait on approvals (HQ, 2026-11-16; from Theory D62):**
- A Codex or other unattended reviewer that triggers a sandbox approval request stalls forever, because no tool can answer it.
- Briefs therefore never set TMPDIR or write outside the agent's own worktree or folder. Scratch goes in `<worktree>/.rc_tmp/` at the worktree root (git-ignored via the shared .git/info/exclude), never inside a ticket folder, because manifest.py walks ticket folders and stray files break freeze and bind. Never add a .gitignore inside a frozen folder.
- **Codex agents never delete anything**, not even their own `.rc_tmp/`, since deletions trigger approval prompts.
  They never write outside their worktree, either: reviews go to `.rc_tmp/`, and the manager copies them and cleans up
  (Engineering, PR #47 incident, 11-16).
- Managers check pending requests when a review runs over 2 h.
