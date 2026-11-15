# Protocol review — memo to HQ (consultant, Fable 5.2, 2026-11-15; second pass added the same day)

**Bottom line.** The record of 32 tickets (≈ 320 review launches, 43 council rounds) says the chain is sound where it
reads mathematics early, and wasteful where it re-reads records late. Four layers catch real errors: statement lock,
lemma line checks, sweep, and council round 1. The better-theorem review is the one layer that catches sub-par
targets. The largest single source of late errors is text edited after its last check.

**Second pass (OpenAI capacity is scarce).** OpenAI reviewers did ≈ 211 of the 227 non-council reviews, so the record
shows what they catch in Claude-written proofs and little about what Claude reviewers would catch there. Where the
two families did read the same content (councils), they are complementary: the OpenAI seat enforces the gate, the
Claude seat finds more real items and never fails one. v4 now has two operating modes. In EFFICIENT mode a Tier A
ticket needs 3 OpenAI sessions against 13.3 launches in the Wave 3 record.

Proposal: `PROTOCOL_v4_PROPOSAL.md` (about 240 lines, cut table included, replacing a 333-line chain of four files).
Counts and pointers: `EVIDENCE.md` (§n below). Counts are helper classifications, good to about ±15%.

## Ranked proposals

**1. Track what was checked, and freeze only checked text (DEPS.tsv).**
- Problem: 30 late slips (a real MAJOR found at sweep or later on an already-checked object). About 14 were text
  edited after its last check and 4 were objects never line-checked (§3). The one false step known to survive a
  council pass was a post-council edit (POST2 D(b)). All 3 GAPs of the blind audit sit in never-checked lemmas.
- Change: one file per ticket, one row per clause or lemma: what it uses, its hash, the hash at its last check, the
  review file. A row is OK, UNCHECKED, STALE or REFUTED. Sweep and council manifests are frozen only when every row
  under a claim is OK. A refuted lemma lists its dependents in the same step.
- On HQ's candidate: DEPS with versions — yes. "No lemma consumed before its line check" — no. The record has no case
  it would have prevented, and the fast tickets prove and check in parallel. Gate the freeze, not the order.
- Cost: a ≈ 100-line script (not yet written), one row per lemma. Removes: manifests for line-check rounds (32 in 5
  tickets), the `as_reviewed_by_*` copies, between-round diff checks (16 of 20 clean; they were ≈ 20 of the 105
  OpenAI reviews of Wave 3). Risk: it does not catch glue errors between lemmas; the sweep does, and stays.

**2. Council: block on substance, close findings with a diff round.**
- Problem: of 25 blocking items in 43 rounds, 2 were a wrong step in a proof. The rest were REPORT text, source or
  transcription fidelity, and labels. In Wave 3, 0 of 6 extra rounds existed because of a proof error (§2). The
  Claude seat's 42 real finds were graded MINOR or lower (one was a theorem missing a premise), fixed after the vote
  and not re-checked; three of the resulting edits carried an error (§7.2).
- Change: each finding carries a class: correctness, strength, faithfulness, or editorial. The first three block,
  whatever severity the seat gave them, and a seat holding one must fail the gate. Editorial items go to
  `ERRATA.md` and one later batch. Fixes are closed by a **diff round**: the same two seats read their own review
  plus the diff, on a new manifest. A blind full re-round only on HQ's order, when a target clause changed. Same
  finding twice after an evidence-backed rejection: HQ decides. No edits after the passing round. Both ≥ 8.0 stays.
- What it would have changed: POST C2/C3, RM C2, PSHARP R2 become diff rounds; START R2 and MISR R2 are not run:
  12 blind seat-reviews and 3 reconciliations replaced by about 8 diff reads.
- Risk: narrow re-checks are the weak step in the record. Of 13 repairs re-checked by a fresh agent, 6 later had an
  error in or next to the repair, though none of the three final-stage ones (§7.3). So the diff round covers every
  row DEPS marks stale, not only the rows named in findings. Not verified: that `check.py --acceptance` accepts a
  diff round as "R2" unchanged; test on a fixture first.

**3. Two operating modes: NORMAL and EFFICIENT (new).**
- Problem: one Codex account serves two projects. The Wave 3 record used 13.3 OpenAI reviews per full-chain ticket
  (9–20) and 6.25 per rider (§7.4). Claude capacity is not the constraint.
- What the record supports (§7.1): a lock by the other family than the author finds false claims, in both
  directions. Every counterexample against a Claude-written lemma came from an OpenAI reviewer, but Claude was asked
  only 9 times. Late errors were caught by a fresh whole read, and in 21 of 25 cases by the same model that had
  passed the object. Fable's blind audit found the 3 real gaps in unchecked lemmas (Sol confirmed all 3) and 21 real
  slips in text OpenAI had passed. Astra and Fable both have a good record on better-theorem work.
- Change (v4 §2A): OpenAI keeps three reads in both modes: the statement lock, the key lemma, the OpenAI council
  seat. In EFFICIENT mode the other line checks, the sweep and the better-theorem review go to fresh Fable or Opus
  agents, and narrow checks continue an existing OpenAI session. Blind first reads stay mandatory at five places:
  lock, better-theorem, key lemma, sweep, council R1.
- Switch rule: HQ moves to EFFICIENT when the OpenAI reviews still owed at NORMAL counts exceed what is expected
  before the next reset (the other project's plans included), or after a Codex limit hit. Back to NORMAL after a
  reset with a third to spare. Reviews already done stand.
- Cost: none in OpenAI terms; 7 to 10 more Claude reviews per Tier A ticket in EFFICIENT mode.
- Risk, stated plainly: in EFFICIENT mode most lemmas are checked only by the author's family, and the record cannot
  tell us Claude's recall on false lemmas. Mitigations: the OpenAI seat still reads everything blind; DEPS records
  who checked each row; HQ can order a Sol catch-up on headline claims after a reset. Continuing a reviewer session
  has no record at all (it was never done): that part is my judgement.

**4. REPORT restates nothing.**
- Problem: 9 of the OpenAI seat's 25 blocking items were REPORT or summary text, 5 more were chapter transcription
  (§7.2). PSHARP's R2 fixed one dropped hypothesis line in REPORT.
- Change: REPORT and the registry block point to STATEMENT lines. Any other mathematical sentence in REPORT is
  labelled HEURISTIC or OPEN. REPORT is written before the sweep and is in its scope. Cost and risk: none seen.

**5. One target gate, finished before proving, with a parity table.**
- Problem: no ticket-level review compared a target with the paper's goals. The Wave 2 factor program drifted for a
  whole wave until the strategy review. C-MIS carried removable fixed-variance hypotheses for 3 days after its
  council; MIS-R then took under 8 h (§5).
- Timing matters: where the better-theorem review finished before proving (RM2, START, PSHARP), the target changed
  at CP1 with no rework. Where it ran alongside proving (POST2, RM, SAMP, SCR), checked lemmas were rewritten. Where
  it ran after the council, cheap adoptions became a new ticket (START2) or were never applied (RM2 BT2).
- Change: `TARGET.md` at CP1 = assumption map + boundary numerics + better-theorem dispositions + a **parity table**
  (each main clause vs the PROGRAM goals, vs the closest published theorem item by item, vs our best registered
  result). The second better-theorem review, when the statement changed, runs with the sweep.
- On HQ's idea: yes, with the two extra columns. Song–Liang alone would not have caught the factor drift.
- Cost: about an hour per ticket. Risk: box-ticking; the reviewer is asked to attack every "matches" row.

**6. STATEMENT changelog; a weakened target clause stops the run.**
- Problem: SAMP D/TR were narrowed with the disposition saying "no claim changed"; HQ found it at the registry, which
  held a mid-ticket draft. SCR v3.4 added hypotheses after the pass, never checked (§4).
- Change: each change tagged STRONGER / WEAKER / EQUAL / NEW-CLAIM, the tag confirmed by a reviewer. Every non-EQUAL
  row gets a statement-change check before the next freeze. WEAKER on a target clause fixed at CP1 → early
  checkpoint. Claims are registered only from the CP3 tree.
- On HQ's candidate "any weakening triggers a checkpoint": too broad. START had three reviewer-driven narrowings in
  6 h, flagged and checked. Restrict the stop to target clauses.

**7. Two tiers; a key-lemma break review instead of the mid-point; numerics where they decide something.**
- Problem: 25 of 25 mid-points said CONTINUE, including 4 tickets that later stopped. No lead-run lemma numerics
  refuted a lemma in 32 tickets, while reviewers found defects in the numerics in 8 of 10 Wave 3 tickets (§1).
- Change: Tier A (new key lemma) keeps the full chain, with a break review of the key lemma at CP2 (START's BR1
  found 2 CRITICAL). Tier B (riders, restatements) runs lock → line checks → council, as START2 did in 6 reviews.
  Required numerics: boundary numerics at CP1 and one end-to-end check per main claim. CP2 is soft.
- Risk: the 7 real MAJORs that Wave 1–2 mid-points found. The break review covers the key lemma; the sweep the rest.

**8. Acceptance is a six-line checklist; the tools are frozen; a form refusal never costs a council round.**
- Problem: 5 acceptance refusals, 0 mathematical. They cost a council round, three tool fixes with about 8 Sol
  reviews, 8 seat-addendum threads and a carrier file. The tooling drew about 13 review rounds, mostly on synthetic
  fixtures, for features with zero real uses (§4, §6). All of that was OpenAI capacity.
- Change: v4 §7. HQ fixes a form failure in the record. No new enforcement and no further tool reviews unless a real
  incident shows a gap. Risk: weaker machine guarantees against a forged record; the record has no such case.

**9. Rollback: four operations, labelled restore points, a real headline list.**
- Problem: only suspect, patch, clear and narrow have ever been used. Three supersessions have waited on the owner
  since 11-12 because all 43 headline flags were set by a tool (§4). On Owls, W3-DIST had real work on disk and no
  snapshot at 15:56 on 11-15; the script is silent when it fails.
- Change: restore-point commits named by event. Snapshot every 15 min with a log line per run. Supersession by
  implication decided by HQ, owner informed; owner approval only for an explicit headline list.

**10. One watchdog, one decision log, audits at wave boundaries.**
- Problem and change as before: decisions recorded once; CI on merge and weekly; a blind Fable batch audit of new
  claims at each wave boundary (251 claims cost about $64 and no OpenAI capacity) replaces the weekly Astra re-audit.

**11. Seat test: Fable and a stricter brief in the Claude seat (new).**
- Question: the Opus seat found 42 real items and failed 0 gates; the OpenAI seat found 25 and failed 12 (§7.2). Is
  that the model, or the old brief that lets a seat pass while holding real findings?
- Stage 1, replay, no OpenAI cost. Material: the 12 rounds the OpenAI seat failed (25 known blocking items) and 6
  rounds both seats passed that hold known Opus-only real items (SAMP C1, SCR C1, POST2 C1, MISR R1, W1-GEN, C-GROW).
  HQ extracts each round's tree as it stood before the seats replied, without reviews or dispositions. Two blind
  seats read each: Fable 5.2 and Opus 5.5, both with the v4 brief. That is 36 Claude reviews; an Opus helper scores
  them against `mining/SEATS.md` S1 and S2.
- Measures: (a) how many of the 25 known blocking items each seat finds and fails the gate on (old Opus: found 3 of
  23, failed 0); (b) how many of the 41 known Opus-only items each finds; (c) correctness, strength or faithfulness
  findings that turn out wrong, on a sample checked by HQ; (d) gate verdicts on the 6 control rounds.
- Decisions: if new-brief Opus fails the gate on most of what it finds, the leniency was the brief: keep Opus, adopt
  the brief. Fable takes the Claude seat on Tier A if it beats new-brief Opus on (a) and is no worse on (b) and (c).
  A Claude seat may stand in for the OpenAI seat — EFFICIENT mode, Tier B only — only if it finds and gate-fails at
  least 20 of the 25, including both proof-step items (C-DLV r1) and both code items (W2-APP).
- Stage 2, live: on the next three Tier A councils the winner sits as a third, non-voting blind seat. Change seats
  only if stage 2 agrees with stage 1.
- Limits: a replay measures recall on items one seat already found, not on what every seat missed. Fable reviewing a
  Fable lead is the same model; include rounds from both Fable-led and Opus-led tickets and report them apart.

**12. Hygiene.** Providers, models, schedules and compute ceilings move to an ops card; rule 16 goes.

## Keep as is
- Statement lock by a reviewer of the other family (best yield per review; a false claim caught in ≥ 12 of 22 W1–2
  tickets). Blind line check of every lemma; briefs give files, not conclusions.
- Exhaustive sweep before the council (it is the layer that catches glue errors).
- Two-seat blind council on a frozen manifest for round 1, one OpenAI and one Claude seat; both ≥ 8.0, all gates.
- CP1 and CP3 as hard HQ gates; kill budgets (none was ever exceeded; W1-GEN L7 passed on its last attempt).
- Citation check; statuses verbatim and per clause; "conditional on" carried downstream; no claim without a file.
- Workers change no git state; one branch per ticket; merge commits; registry rows never deleted.
- PROGRAM's presentation rule, stop list and tie-break.

## What HQ should know
- **W3-DIST is running under the old rules** and already keeps a `DEPS.md` (seen by name only; I did not open its
  folder). Its brief's addendum A1 is the parity table of proposal 5 in all but name.
- **Sol against Astra.** They fail the council gate at the same rate (28% and 27%), and each found errors after the
  other. The record gives no reason to spend scarce capacity on Astra outside the key lemma, the Tier A sweep and
  the Tier A seat. I do not know how the Codex plan weighs the two models; HQ does.
- **What I did not do.** I re-checked no mathematics. I read the HQ-level record myself and a few ticket cases. The
  per-ticket and per-seat counts come from four Opus helper runs reading dispositions (`mining/`). `deps.py`, the
  snapshot changes and the seat test are specified, not built or run. The EFFICIENT review counts are a design, not
  a measurement.
