# Protocol review — consultant brief (HQ, 2026-11-15)

You are HQ's **protocol consultant** (Claude Fable 5.2, effort high, provider **Claude Third**, on Owls). Repo clone
`/home/fb31/Bayesian-Variable-Selection` (`git pull --ff-only` first; no other git commands). Write only under
`Theory_work/Wave3/PROTOCOL_REVIEW/`. HQ (the CEO thread) decides and commits. The owner (Felipe) wants:
> "updated protocols of reviewing when working, both embedded throughout the whole chain and by check points, also strong
> trace / roll back protocols for errors or suboptimal results … we want to also have councils but we want to avoid
> nit picking and complexity overblow for no good reason."

## Goal
Make the review/trace/rollback system **stronger where it catches real errors or sub-par theorems, and lighter
everywhere else**. Evidence first. Every proposal must cite what happened in our own record. Abstract best practice is
not evidence.

## Read
- Rules: `Theory_work/Wave1/PROTOCOL.md`, `Wave2/PROTOCOL.md`, `Wave3/PROTOCOL.md` (binding stack),
  `Theory_work/INFRA/LIFECYCLE.md` (rollback §3, gates §4, supersession §5), `Wave3/PROGRAM.md`,
  `Theory_work/INFRA/templates/` (COUNCIL_BRIEF, ASSUMPTION_MAP).
- Record (the data): `Wave3/HQ_DECISIONS.md`, `Wave3/HQ_NOW.md`, `Wave3/HOLDS.md`, `Wave3/WATCHDOG.md`,
  `Wave3/PIPELINE_REVIEW/`, `Wave3/API_AUDIT/*/TRIAGE.md`.
- Ticket trails (on `main` or `git show theory/<T>:<path>`): W3-POST2, W3-MISR, W3-START, W3-START2, W3-PSHARP,
  W3-RM, W3-RM2, W3-SCALE, W3-P6, plus Wave1C/C-PACK, C-MIS, and Wave2 tickets. Use their `LOG.md`, `REPORT.md`,
  `CHECKPOINT_*.md`, `reviews/` (statement lock, K/line checks, mid-point, sweep, council rounds, dispositions).
- New context: W3-DIST (`Wave3/W3-DIST/BRIEF.md`) runs here on Owls in the root clone. Its restore points are an
  hourly cron snapshot to branch `theory/W3-DIST` (`~/.config/bvs-hq/snap/snapshot_ticket.sh`).

## Questions (answer each with evidence)
1. **Yield per layer.** For each review layer (statement lock; lemma line checks + falsification numerics; mid-point;
   sweep; council; acceptance audit; API audit; CI/re-audit), count findings by severity across the tickets above. Count
   how many were **real** (changed a statement, proof or status) and how many were cosmetic or re-raised. Which layers
   earn their cost, and which mostly produce noise?
2. **Councils without nit-picking.** Look at how council rounds went (scores, rounds, which findings blocked). Propose a
   rule set that keeps two independent seats but blocks only on correctness, strength or faithfulness. For example:
   severity-gated blocking, MINORs batched to the editorial pass, no rescoring on wording, a fixed round cap, and a
   "same finding twice = HQ decides". Say what this would have changed in past rounds.
3. **Embedded review.** Is the per-lemma chain applied consistently? Where did errors slip to late layers, and which
   earlier check would have caught them? Propose the minimal embedded rule. One candidate HQ is considering: a per-ticket
   lemma dependency file (DEPS) with versions, plus "no lemma consumed before its line check". Judge it.
4. **Trace and rollback.**
   - Inside a ticket: a refuted lemma must reach its dependents before CP3. Today this is only enforced by the registry
     at merge.
   - Statement drift: a target silently weakened while proving. Candidate rule: a STATEMENT changelog tagged
     stronger/weaker/equal, where any weakening triggers an early checkpoint.
   - Remote tickets (Owls): judge the restore-point setup.
   - Is LIFECYCLE §3 usable in practice, or too heavy? Name what to cut.
5. **Sub-par results.** Did the sharpness gate (ASSUMPTION_MAP, boundary numerics, better-theorem review) catch
   weak targets early? Cite cases, e.g. RM → RM2, C-MIS → MIS-R, START → START2, and the PSHARP outcome. What would
   catch them earlier or more cheaply? One idea is a literature parity table at CP1 (W3-DIST addendum A1 does this
   for Song–Liang).
6. **Complexity budget.** List the rules, files and tools that cost more than they return: delete, merge or automate.
   Target a **shorter** binding protocol than today, not a longer one.

## Deliverables (in `Theory_work/Wave3/PROTOCOL_REVIEW/`)
- `EVIDENCE.md`: the counts and cases behind questions 1–5 (tables; file:line pointers).
- `MEMO.md`, at most 3 pages: a ranked list of proposals. For each: the problem with evidence, the change, its cost,
  what it removes or simplifies, and the risk. Then a "keep as is" list.
- `PROTOCOL_v4_PROPOSAL.md`: a consolidated, shorter binding protocol that applies your proposals. One file that
  replaces the stack's rules for future tickets, with pointers into LIFECYCLE where needed. Mark every rule as NEW,
  KEPT, MERGED or CUT.

## Rules
- Effort high max. You may use at most 2 helper agents for record mining, on **Claude Third, Opus 5.5, effort high**
  (`delegate_task`, provider `claudeAgent_claude_third`), with narrow briefs. No OpenAI agents. No NOTS.
- Token-efficient: grep and count, don't paste. Target ≈ 3–4 h.
- **End your run** with MEMO.md's ranked list as your final message (≤ 40 lines).
