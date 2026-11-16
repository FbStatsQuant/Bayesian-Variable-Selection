# Theory protocol v4 — ADOPTED by HQ 2026-11-15 (binding for W3-DIST and every ticket opened after today)

Source: consultant proposal `PROTOCOL_REVIEW/PROTOCOL_v4_PROPOSAL.md` (evidence `PROTOCOL_REVIEW/EVIDENCE.md`, `MEMO.md`).
Running tickets other than W3-DIST (W3-P6, W3-SCALE: compute tickets) finish under `PROTOCOL.md`. W3-PATH starts under v4.

## HQ amendments (these override the text below)
- **H1. Mode.** NORMAL mode until the owner says otherwise. Owner, 11-15: "keep using codex model for review as we are, I
  will just let you know if we are running out of it". EFFICIENT mode (§2A) is defined and dormant.
- **H2. Owner-gated items — APPROVED by Felipe 2026-11-15 (~17:30 CT, "ok").** (a) tiers adopted and the §10 cut of W3-14 stands (tiers and modes replace case-by-case waivers; any other skip still needs Felipe); (b) the CP2 break review replaces the mid-point (W3-DIST keeps the extra mid-point question already briefed); (c) supersession per §8: HQ decides with owner veto; owner approval for the explicit headline list (to be set with Felipe). Original interim text kept for the record:
  - (a) The old rule "no review layer skipped or replaced without Felipe's explicit approval" (W3-14) STAYS. The §10 cut
    is not adopted. Tier B (§2) is used only once the owner approves tiers; until then every proof ticket is Tier A.
  - (b) Mid-point → key-lemma break review (§3.4): the CP2 review is run as a break review, and its brief also asks
    the old mid-point question (CONTINUE / REDIRECT / STOP, with reasons). That satisfies both rules. No layer is
    dropped.
  - (c) Supersession (§8): LIFECYCLE §0 / §5.3 as now (owner approves headline supersessions) until the owner answers.
- **H5. Headline claim changes (owner, 2026-11-15: "the Fable consultant of yours ... you just run those things by him").**
  Every supersession and every change to a headline statement goes from HQ to the HQ consultant (Fable 5.2) as a one-page
  card: before/after in plain words, what it buys the paper, which assumptions moved, the evidence, HQ's recommendation.
  On AGREE, HQ adopts. On OBJECT, HQ and the consultant settle it, and only an unresolved disagreement goes to Felipe.
  Felipe is informed afterwards in the weekly owner digest. This replaces the owner veto of H2(c) in practice.
- **H6. Reader versions (owner, 2026-11-15).** Every headline theorem has a reader version per PROGRAM.md "Readability":
  numbered primitive assumptions and one-display conclusions, with the interface version as the master and checked
  bridges. It is part of TARGET.md at CP1 and of the council manifest at CP3.
- **H3. API batch proof attempts** (Fable via the Console key, run by HQ) are proof material handed to the lead. They
  are never reviews, never count toward a review layer, and are line-checked like any lemma before use.
- **H4. Tooling.** HQ implements the remote snapshot changes (§8: 15-min cadence, one log line per run, RP labels,
  skipped-file list) and commissions `deps.py` (§4.1). Until `deps.py` exists, the lead keeps DEPS by hand with
  `sha256sum`.


One binding file for every proof ticket opened after adoption. It replaces the rules of `Wave1/PROTOCOL.md`,
`Wave1C/PROTOCOL.md`, `Wave2/PROTOCOL.md` and `Wave3/PROTOCOL.md` (333 lines read as a chain). Running tickets finish
under the rules they started with. `Wave3/PROGRAM.md` (targets, presentation rule, stop list, tie-break) and
`INFRA/LIFECYCLE.md` (registry operations) stay, the latter only where this file points to it.

Tags: **[KEPT]** unchanged in substance · **[MERGED]** several old rules in one · **[NEW]** · **[CUT]** (listed in §10).
Old rules are cited as W1, W1C-n, W2, W3-n (Wave 3 rule n), LC §n. Evidence for each change: `EVIDENCE.md`, `MEMO.md`.

## 0. Three principles
1. A review blocks only on **correctness** (a step is wrong or unproved), **strength** (the text claims more than is
   proved, or uses a hypothesis it does not state) or **faithfulness** (to the code as pinned, to cited sources, to
   STATEMENT in any derived text). Everything else is editorial: it is recorded and never blocks. [NEW]
2. Text is trusted only in the version that was checked. Any later edit makes it unchecked again. [NEW; was W3-15 in part]
3. Tools guard against honest mistakes, not forgery. A tool refusal about record form is fixed in the record. It never
   triggers a review round. [NEW]

## 1. Roles and workspace
- Owner sets goals and the headline list. HQ runs tickets, answers checkpoints, commits. A lead owns one ticket and
  reports to HQ. [KEPT W1]
- A lead writes only in `Theory_work/<Wave>/<TICKET>/` and changes no git state. One branch `theory/<TICKET>` per
  ticket; HQ merges with a merge commit. [KEPT W1, W3-9]
- Files: `STATEMENT.md` (with its changelog, §4.2), `TARGET.md` (§3.2), `DEPS.tsv` (§4.1), `PLAN.md`, `LOG.md`
  (timestamps from `date`; agents started, with model and role), `lemmas/`, `numerics/`, `reviews/` (each reply
  verbatim, each brief, each disposition), `ERRATA.md` (§5.3), `CHECKPOINT_<k>.md`, `REPORT.md`. [MERGED W1, W3-3, W3-12]
- Models, providers, effort cap, schedules and budgets are on the **ops card** in `HQ_NOW.md`, not here. [CUT from
  protocol: W1/W1C/W2 model sections, W3-1, W3-2 and its four amendments]
- Compute tickets carry their own rules in their `DESIGN.md`. [CUT from protocol: W3-10 compute block]

## 2. Tiers (HQ sets the tier in the BRIEF) [NEW; replaces the waiver clause of W3-14]
- **Tier A — new key lemma.** Full chain §3.
- **Tier B — rider, restatement or re-check of an existing proof** (no new key lemma, about five lemmas or fewer).
  Chain §3 without step 4; step 5's duties go into the council briefs.

## 2A. Operating modes (HQ sets the mode on the ops card) [NEW]
OpenAI review capacity is one shared account; Claude capacity is large. Two modes differ only in **who** reviews and
whether a reviewer **session** may continue. The chain, the gates and the pass rules are the same in both.

| step | tier | NORMAL | EFFICIENT | session |
|---|---|---|---|---|
| 1 statement lock | A, B | Sol | Sol | **fresh, blind first read** |
| statement-change check (§4.2) | A, B | Sol, new agent | the lock session continues | sees only the change and its dependents |
| 2 better-theorem review (CP1; final) | A; B if the statement is new | Astra | Fable | **fresh, blind first read** |
| 3 line checks, lemmas off the key path | A, B | Sol, 2–4 lemmas per review | Fable (Opus for volume); never the lead's session | new agent per batch; blind to LOG and earlier reviews |
| 3–4 key lemma and what it consumes | A | Sol line check, then Astra break review | one OpenAI session: break review and line check together | **fresh, blind first read** |
| re-check of a repaired lemma | A, B | new agent of the finder's family | the finder's session continues | sees the repair and every row DEPS marks STALE |
| 5 sweep | A | Astra | Fable | **fresh, blind first read**; never an agent that has reviewed this ticket |
| 7 council R1, OpenAI seat | A, B | Astra (A), Sol (B) | Sol; Astra for headline-list claims | **fresh, blind first read** |
| 7 council R1, Claude seat | A, B | Opus (Fable if the seat test says so) | same | **fresh, blind first read** |
| diff round (§5.5) | A, B | each seat: new thread + its own R1 review | OpenAI seat: its R1 session continues; Claude seat as NORMAL | – |
| **OpenAI reviews per ticket** | | **A: about 11 (8–14). B: about 4 (3–6)** | **A: 3 sessions. B: 2 sessions** (lock, [key lemma], council seat), plus short continuation turns | record: A 13.3 (9–20), B 6.25 (5–8) |

- **Blind first reads are required** at the five places marked: lock, better-theorem, key lemma, sweep, council R1.
  There a reviewer gets the frozen files and sources and nothing else, and has never reviewed this ticket. Everywhere
  else a continued session is allowed in EFFICIENT mode; it is logged, and DEPS records it (`checked_by … +c`).
- **An agent that has reviewed a ticket never becomes its sweep or an R1 seat**, in either mode.
- **OpenAI is never replaced** at the lock, the key lemma and the OpenAI council seat. A Claude seat may stand in for
  the OpenAI seat only where a recorded result of the seat test allows it (MEMO #11), and never on a Tier A ticket or
  on the chapter council.
- **Switch rule.** HQ moves to EFFICIENT when either holds: (a) the OpenAI reviews still owed by all active tickets
  at NORMAL counts (table above, minus those done) exceed what HQ expects to have before the next reset, the other
  project's planned use included; (b) a Codex limit was hit in the last 24 h. HQ returns to NORMAL after a reset once
  (a) holds with a third to spare. The switch is recorded in `HQ_DECISIONS.md` and applies to reviews not yet
  launched; finished reviews stand. Each CHECKPOINT names the mode of each review it relies on.
- **When OpenAI capacity is short even for EFFICIENT**: council seats first, then key lemmas, then locks; headline
  tickets before others. If none is available, work continues on Claude reviews and stops before the council freeze.
  No claim is labelled checked without its OpenAI lock, key-lemma review (Tier A) and OpenAI seat.
- **Catch-up.** For claims on the headline list, HQ may order one Sol batch check of the DEPS rows that only Claude
  reviewers checked, when capacity returns and before the chapter freeze.

## 3. The chain
Who reviews at each step, and whether a session may continue, is set by §2A.
1. **Statement lock.** One cross-family reviewer checks STATEMENT and PLAN against the sources: right target,
   faithfully stated, hypotheses explicit, plan viable. Fix, then lock. [KEPT W1]
2. **Target gate → CP1 (hard).** Finished before any lemma beyond a sketch of the key lemma is written. [MERGED W3-3,
   W3-10 "headline strength", LC §4.2–4.3; timing rule NEW]
   `TARGET.md`, one page, is the evidence file for the `lit:`, `necessity:` and `better:` gates:
   - *Assumption map*: per hypothesis, where it enters, how, and its necessity reading (template `ASSUMPTION_MAP.md`).
   - *Parity table* [NEW]: each main clause compared with (a) the PROGRAM goals (design-agnostic, p ≫ n, method as
     coded), (b) the closest published theorem, item by item (metric, mode of convergence, rate, sparsity, prior,
     scope), (c) our best registered result. Each row says matches / beats / short. A "short" row needs a reason, or
     becomes a stretch item with a kill budget.
   - *Boundary numerics*: simulate just outside each assumption.
   - *Better-theorem review*: one fresh strong reviewer gets the locked statement and this file, and is asked to
     propose a strictly better provable statement and to attack every "matches" row. Each credible proposal gets a
     disposition: adopt / reject with evidence / named open item.
   CP1 lists the **target clauses** (conclusion, rate, scope, the hypotheses of each main theorem). HQ decides the target.
3. **Lemma line checks.** Each lemma is checked line by line by a blind reviewer (family per §2A). Proving and checking
   may run in parallel. The freeze rule §4.1 is the gate. [KEPT W1; ordering clause relaxed]
   Numerics [MERGED W1, W1C-4]: required are the boundary numerics of step 2 and, where an exact small case exists, one
   end-to-end check of each main claim. Per-lemma numerics are the lead's choice. Reviewers raise findings on numerics
   only where a statement or a necessity label cites them.
4. **Key-lemma break review → CP2** (Tier A). The strong reviewer gets STATEMENT, the key lemma and what it consumes,
   and is asked only to break it. [NEW; replaces the mid-point of W1]
5. **Sweep.** One strong reviewer lists every flaw in the whole frozen content. Named duties: statement copies against
   lemma statements; quantifiers and uniformity; each lemma's scope against every downstream use; REPORT and the
   registry block against STATEMENT; DEPS rows spot-checked against review files. Always before the council. [KEPT W1;
   duties NEW]
   If the statement changed in substance since CP1, a second better-theorem review runs **on the same manifest as the
   sweep**. Cheap adoptions go in before the council freeze. [NEW timing; was W3-10]
6. **Citation check** (script, 0 MISS) before the council freeze. [KEPT W1C-2]
7. **Council** (§5), then **CP3**.
8. **Acceptance** by HQ (§7).

Standing rules for every review [KEPT W1, W1C-1,3,5,6]: a new agent each time, except the continued sessions §2A
allows; the brief gives
files, not conclusions, and is saved in `reviews/` before launch; reviewers are asked to break the result; no
"checked" sentence without a review file; statuses verbatim and per clause; a premise below PROVED-CHECKED is an
explicit hypothesis carried as "conditional on …" (W3-11); a dispute on a step goes to a second fresh reviewer.

**REPORT restates nothing.** [NEW] REPORT and the registry block point to STATEMENT lines. They do not re-type a
hypothesis or a conclusion. A sentence in REPORT that asserts mathematics not in STATEMENT or a checked lemma is
labelled HEURISTIC or OPEN. REPORT is written before the sweep and is inside the sweep and council manifests.

## 4. Embedded trace
### 4.1 `DEPS.tsv` [NEW; replaces per-round manifests for line checks and the `as_reviewed_by_*` copies]
One row per object under a claim: statement clause, lemma, bridge, example, REPORT section.
`id | file[:lines] | uses (ids) | sha | checked_sha | checked_by (review file) | state`
- `state` is derived: OK (sha = checked_sha), UNCHECKED, STALE (edited since its check), REFUTED, DOWNSTREAM (uses a
  row that is not OK). A small script computes it (`deps.py status <ticket>`, to be written, standard library; by hand
  with `sha256sum` until then).
- **Freeze rule.** The sweep and council manifests are frozen only when every row under a claim is OK.
- **Refuted lemma.** Mark it REFUTED in the same step; the LOG entry lists its dependents from `uses`. If it is the key
  lemma or a target clause depends on it, write an early checkpoint (§6).
- Manifests (`manifest.py freeze`) are made for the sweep and for each council round only. INPUTS never lists wave
  documents or registry tables. [KEPT W3-15, narrowed]

### 4.2 STATEMENT changelog [NEW]
A table at the foot of STATEMENT.md, one row per change after the lock:
`version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger (review file) | check (review file)`
- Every row that is not EQUAL needs a **statement-change check** before the next freeze: one OpenAI reviewer (§2A) on
  the change and on its dependents per DEPS. The reviewer, not the lead, confirms the tag.
- WEAKER on a **target clause** → early checkpoint. Other WEAKER rows (a used hypothesis made explicit) are reported at
  the next checkpoint.
- STRONGER beyond what CP1 approved needs HQ's go, except adoptions the brief pre-authorised.
- Claims are registered only from the CP3 tree, never from a draft.

## 5. Council
1. **Seats.** One OpenAI seat and one Claude seat. Round R1 is a blind first read of the frozen manifest: statement,
   proofs, needed sources; never earlier reviews, dispositions or scores. [KEPT W1, W3-15]
   Both briefs state that a seat **must** give `gates=FAIL` when it holds a C, S or F finding of its own, whatever
   severity it would give it: in the record the Claude seat found more real items than the OpenAI seat and never
   failed a gate. [NEW]
2. **Each seat returns** [MERGED W3-15, LC §4.1, HQ's seat addendum of 11-12]: a per-claim table `| id | decision |`
   with ACCEPT / REJECT / NOT-EXAMINED; its findings, each tagged **C**, **S**, **F** (principle 1) or **E**
   (editorial: wording, notation, record, citation form, presentation of numerics); the six gates; one
   `COUNCIL-VERDICT` line (template `COUNCIL_BRIEF.md`).
3. **What blocks.** Only a C, S or F finding that names the clause or line and says what fails. The seat's own
   MAJOR/MINOR label does not decide this. E findings never block and never lower the score. They go to `ERRATA.md`
   and are applied later in one editorial batch (in the chapter transcription, or as one version bump with one
   "editorial only" diff check). "A stronger theorem is provable" is not a council finding: it is logged as a
   better-theorem proposal for HQ. [NEW]
4. **Pass** = on one manifest, both seats: every claim ACCEPT, all gates PASS, score ≥ 8.0. The score reflects C, S
   and F only. A claim marked NOT-EXAMINED gets no checked label until a targeted review covers it. [KEPT W1; scope of
   the score NEW]
5. **Diff round** [NEW; replaces blind re-rounds, the reconciliation reviewer and post-council diff checks]. If R1
   leaves any accepted C, S or F finding — blocking or not, whether R1 passed or failed — the lead fixes them, updates
   DEPS and the changelog, and HQ freezes a new manifest. The same two seat models, in fresh threads, each get their
   own R1 review, the diff since R1's manifest and the DEPS dependents of every changed object: every row
   edited in the repair, not only those named in findings. They answer: is each
   of my findings resolved; does the diff break anything; per-claim table; verdict line. They do not re-read unchanged
   text and do not add E findings.
6. **Blind full re-round** only on HQ's order, when a target clause changed (changelog WEAKER or STRONGER) or a
   consumed lemma was re-proved by a new argument. [NEW]
7. **Same finding twice.** If the lead rejects a finding with evidence and the seat raises it again, HQ decides. HQ
   may buy one tie-break review of that step. There is no third exchange. [NEW]
8. **Cap.** R1, one diff round, and at most one HQ-ordered full round. After that the result is CP3-EXHAUSTED: no
   checked label for a failing claim; a narrowed statement is a new target through CP1. [KEPT W3-10, W3-14; cap shape NEW]
9. **Nothing in the passing round's manifest is edited afterwards.** [KEPT W3-15]

## 6. Checkpoints and stop rules
- At a checkpoint the lead writes `CHECKPOINT_<k>.md`. HQ records its decision **once**, in `HQ_DECISIONS.md`, tagged
  with the ticket and the restore-point commit. [KEPT W3-10; the duplicate LOG entry is CUT]
- **CP1 (hard)**: target fixed (§3.2). **CP3 (hard)**: council passed or exhausted. No work past a hard checkpoint
  without HQ's go. [KEPT W3-10]
- **CP2 (soft, Tier A)**: key lemma proved and break-reviewed. The lead continues if no C/S/F finding is open and no
  kill budget is spent; HQ can make CP2 hard in the BRIEF. [changed from W3-10]
- **Early checkpoint** (the lead ends its run): a counterexample to a target clause; a WEAKER change to a target
  clause; a refuted key lemma; a kill budget spent; a hold on a consumed claim. [MERGED W1 "statement changes", W3-11, W3-12]
- **Kill budgets**: a lemma that fails 3 proof attempts, each with a reviewer verdict → STUCK. HQ may set lower
  budgets per item at CP1. [KEPT W1, W3-14]
- **Consumed claims**: only claims ACTIVE in the registry, cited by id and version. HQ compares them with current
  main before each continuation and at acceptance. [KEPT W3-11]

## 7. Acceptance at CP3 (HQ checklist, on the ticket branch merged with current main) [MERGED W3-10 CP3-PASS, LC §4]
1. Both seats' reviews of the passing round: per-claim ACCEPT for every claim to be labelled; `manifest.py bind` OK.
2. `manifest.py verify` passes on the passing round's manifest (nothing edited since).
3. DEPS: every row under a claim is OK.
4. Consumed claims valid on main (`check.py --consumed-vs`); conditional statuses carried.
5. Citation check 0 MISS; staged ingest 0 problems; `check.py --acceptance` 0 ERROR.
6. Headline claims only: TARGET.md has a disposition for every credible better-theorem proposal.

If step 1, 2 or 5 fails on **form** (table layout, line ends, a status file outside the manifest), HQ fixes the record
or files a tool bug, and labels on the council evidence. No council round is run for a form failure. [NEW]
The tools are frozen as they are: no new enforcement, and no further review rounds of the tools unless a real
incident shows a gap. [NEW]

## 8. Rollback and restore points
- **Restore points.** HQ commits the ticket folder at every checkpoint and every manifest freeze, with the message
  `RP <ticket> <CP1|SW1|R1|R2…> <first 12 hex of the digest>`. A ticket on a remote machine is snapshotted every 15
  minutes when changed; the script labels a commit that contains a new `MANIFEST_*` or `CHECKPOINT_*` in the same way,
  writes one log line per run (also "no change" and "push failed"), and lists files it skipped for size. The watchdog
  reads that log. [KEPT W3-9; labels, cadence and logging NEW]
- **Inside a ticket.** To undo work, HQ restores the folder from a named restore point, records it in
  `HQ_DECISIONS.md`, and the lead recomputes DEPS. [NEW]
- **After merge** (LC §3, level table only): SUSPECT → PATCH → CLEAR for a repaired gap; NARROW for an over-strong
  statement; RETRACT for a false one; each priced first with `propagate.py … --dry-run`. Rows are never deleted. [KEPT]
- **Supersession.** A result that implies its parent, with the implication checked by one reviewer, supersedes it at
  acceptance. HQ decides and informs the owner, who can veto. The owner's approval is needed only for claims on the
  owner's explicit **headline list**; tool-set headline flags do not count. [changed from LC §0, §5.3]
- Dormant, kept in LIFECYCLE as reference but not binding and not maintained: `rollback-ticket` and the tombstone git
  recipe, per-claim tags and archive branches, CANDIDATE / promote, re-point proposals, COEXIST, the freeze criterion.
  [CUT from the binding path: LC §3 git steps 1–5, §5.1, §5.3 re-points, §5 freeze]

## 9. Watch
- One watchdog, every 6 h, independent of HQ: flags a checkpoint unanswered > 6 h, a ticket silent > 3 h that is not
  idle by design, a stale snapshot log, compute over its line. It appends holds to `HOLDS.md`; only HQ lifts them.
  [MERGED W3-12 heartbeat + watchdog]
- Leads read `HOLDS.md` at each checkpoint and before each freeze. [changed from "before every step"]
- `run_ci.py` runs on every merge to main and weekly. [changed from daily, W3-13]
- At each wave boundary: one blind batch audit of the wave's new claims (correctness; and "best single improvement,
  and its kind", with the supersession map), then triage. [NEW; replaces the weekly random re-audit of W3-13]

## 10. Rules cut, and why (pointers into EVIDENCE.md)
| cut | reason |
|---|---|
| mid-point review (W1) | 25 of 25 CONTINUE; its real finds are line-check finds (§1). Replaced by step 4 |
| falsification numerics for every lemma (W1, W1C-4) | 0 lemmas refuted in 32 tickets; a source of review findings (§1) |
| manifests for line-check, mid-point and change-check rounds (W3-15) | 32 manifests in 5 tickets; DEPS hashes do this (§6) |
| diff check after every review round (W3-15) | 16 of 20 clean; the 4 real ones followed a statement change, now §4.2 (§1) |
| reconciliation reviewer in rounds ≥ 2 (W3-15) | 3 runs, 0 real; replaced by the diff round |
| post-council edits + PC check (HQ 11-11) | no post-council edits at all under §5.9; fixes go through the diff round |
| blind re-round for REPORT or wording defects (W1, W3-15) | 6 extra W3 rounds, none for a proof error (§2) |
| "no layer skipped without Felipe" (W3-14) | HQ waived layers itself twice; tiers make this a rule (§6) |
| ticket-LOG copy of HQ decisions (W3-10) | 2 watchdog flags and 3 notes, no value (§1) |
| daily CI, weekly Astra re-audit (W3-13) | 1 cosmetic finding in 4 days; re-audit never ran (§1) |
| provider, model and compute rules in the protocol (W3-1, 2, 10) | operations, four amendments in five days (§6) |
| W3-16 (interim hold) | lifted 2026-11-12 |
| LIFECYCLE §4.1 parser grammar as binding text | stays as tool documentation; form failures are handled by §7 |
| "never reuse a reviewer's context" as an absolute rule (W1) | kept at the five blind first reads; relaxed elsewhere in EFFICIENT mode (§2A). No record either way: no session was ever continued (§7.3) |
| "cross-family reviewer" for every line check (W1) | kept in NORMAL; in EFFICIENT only for the key lemma (§7.1) |
