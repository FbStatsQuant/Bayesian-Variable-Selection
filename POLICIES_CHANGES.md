# POLICIES v2.0 (2026-11-28): changes from v1

Section numbers in the old text are those of POLICIES v1 (commit b790a6b9).

## (a) Dropped as obsolete

1. **§8 department charters** (W3-DIST, W3-READER, riders, premise tickets, parallel-SMC campaign; Engineering p = 10⁶
   mandate with its plan-or-impossibility proof; Writing chapter v2.0 and advisor report; Lean charter). Superseded by
   the Song–Liang 1-to-1 scope (11-27), "1M comes last" (11-25) and PAPER-DRAFT (11-28). Current priorities live in
   `HQ_NOW.md`. The general rule on engineered variants is kept (§4).
2. **§5 account table** (CP default since 11-16, Claude Third retired for SMC, Claude Work for Writing). Out of date:
   Engineering runs on Claude Third (11-27), HQ on Claude Work (11-24). Replaced by rule 4 and a pointer to `HQ_NOW.md`.
3. **§7 budget envelopes** (Theory ≤ 3 leads + an audit Fable; Engineering ≤ 4 concurrent agents; Codex priority
   W3-DIST). Replaced by the pace rule (2–3 leads per department).
4. **§3b model roles** ("managers are always Opus", "Astra HQ-only", phase rule, Fable as "VP"). Replaced by the
   model table and rule 8; the step-down / right-model idea is kept in one line.
5. **§10 top-level thread exception** for large independent work, and "threads already top-level finish where they
   are". Transitional or in conflict with the new thread rule.
6. **§11 overnight mode.** HQ-internal and in conflict with "every Fable/Astra goes to the owner" (see (c)5).
7. **§4 "public for now; the owner will make it private"**: the repo is public by owner choice.
8. **§4 restore-point cron** (`~/.config/bvs-hq/snap/`, every 15 min): its paths predate the 11-25 REORG and it can't
   be verified from here; replaced by "commit meaningful states often" (see (c)6).
9. **§4 "LAYOUT.md"** reference: no such file is in the repo.
10. **§5 NOTS SSH key details**: setup detail, not a rule for managers.
11. **§12.3 laptop as the heavy-data destination**: replaced by desktop-primary offload (old §12.13, `HQ_NOW.md`).
12. **§12.8–12.9 folder names** (`~/SMC_Engineering_Department`, `SMC_<Name>_Department`): superseded by the 11-25
    REORG layout (`_local/<dept>/`, `~/SMC-BVS`).
13. **§14 Codex pacing table**: reduced to one line (level set by the owner, recorded in `HQ_NOW.md`).
14. **§14 "managers check pending approval requests after 2 h"**: managers no longer watch agents; this is the
    lead's job (the stuck-seat rule is kept in §7).
15. **HQ-internal material**: HQ consultant as second signature (H5), the external adviser, Fable use in the daily
    brief, the board/cadence prose, the "no weekly digest" note. Managers don't act on these.
16. **All dated amendment tags and history.**

## (b) Conflicts found and how they were resolved

1. **Task lead account.** Log 11-27 (org rule): leads on Claude Work, Claude Third as overflow. Old §1a and today's
   rules: Claude Personal. **Resolved:** Claude Personal default; the owner adjusts, HQ relays.
2. **Theory council.** Log 11-28 ("TOP PRIORITY"): Opus + Sol + Opus. Old §1b (b790a6b9) and today's rules: Opus +
   Sol + Neon. **Resolved:** Opus + Sol + Neon.
3. **What happens after failed rounds.** Log 11-27: two fresh judges (Astra + Fable), one round, then finalize.
   PROTOCOL_v4 §5.7–5.8: R1 + one diff round + an optional HQ-ordered round, then CP3-EXHAUSTED; "same finding twice →
   HQ decides". Old §1b and today's rules: 3 rounds, then one Fable arbiter. **Resolved:** the Fable arbiter,
   company-wide. The handbook declares PROTOCOL_v4's council rules replaced.
4. **Who approves Fable/Astra.** Old §4: HQ approves Fable (owner delegation 11-16); old §3b: Astra is HQ-only; old
   §11: HQ decides Fable requests overnight. Today's rules: up the chain to the owner, every time. **Resolved:** owner
   every time.
5. **NOTS concurrency.** Old §5 and §12.7, and `Docs/Experiments/P1M/PROTOCOL.md`: 150 tasks. Log 11-26 and today's
   rules: 468. **Resolved:** 468.
6. **Manager model.** Old §3b: "managers are always Opus"; log 11-24: managers on Claude Work Opus. Old §1a: manager
   threads run on Neon. **Resolved:** Neon may orchestrate manager threads (today's rules); see (c)1.
7. **Blocking findings.** Old §1b: any blocking flaw is fixed "whatever the score". Today's rules: the manager may
   decline any finding, a declined blocking one is reported to HQ. **Resolved:** adopted blocking findings must be
   fixed; declined ones go to HQ.
8. **Council sessions across rounds.** PROTOCOL_v4 §5.5: same seat models in fresh threads; two seats; pass at 8.0.
   Today's rules: same agents, three seats for theory, 8 / 8.5 bars. **Resolved:** today's rules.
9. **Top-level threads.** Old §10 allowed an exception; today's rules don't. **Resolved:** no exception.
10. **Astra model id.** Old §5: `gpt-6-astra`; log 11-27: `gpt-6.2-astra`. **Resolved:** `gpt-6.2-astra`.
11. **Heavy-data destination.** Old §12.3 (laptop) vs §12.13 (desktop primary). **Resolved:** desktop primary,
    laptop mirror.
12. **Codex mode.** PROTOCOL_v4 H1 says NORMAL; `HQ_NOW.md` says level 1 since 11-16. **Not resolved here:** the
    handbook defers to `HQ_NOW.md`.

## (c) For HQ to decide — all RULED by HQ, 2026-11-28 (applied in v2.0)

1. **Which model runs manager threads:** Neon (old §1a) or Opus on Claude Work (11-24 roster)?
   RULED: whichever the owner sets per department; currently Engineering = Opus 5.5 (Claude Work), Theory and
   Writing = Orchestrator (Neon). Handbook §1 states the rule; `HQ_NOW.md` holds the setting.
2. **Non-theory councils:** Opus + Sol with Neon optional?
   RULED: confirmed. Theory: Opus + Sol + Neon.
3. **Task-specific owner review orders** (PAPER-DRAFT, TH-SONG final pass) override the default for that task?
   RULED: confirmed.
4. **`HQ_NOW.md` stale** (roster, account allocation).
   RULED: refreshed in this commit (roster on Owls environment, manager models, account allocation; stale entries
   removed; Codex level line kept unverified).
5. **Overnight / owner-away mode.**
   RULED: HQ runs operations fully and decides operational matters; owner-reserved items (paper claims, account
   changes, large campaigns, department Fable/Astra requests) are queued for the owner. HQ may spawn its own Fable or
   Astra adviser when unsure on something consequential (owner pre-authorization 2026-11-28). Handbook §1 and rule 8.
6. **Restore-point cron.**
   RULED: dropped; "commit meaningful states often" stands.
7. **Lean work until a Lean department exists.**
   RULED: Theory. Confirmed.
8. **Large campaigns need the owner's GO through HQ.**
   RULED: standing rule (handbook §1 table and §6).
9. **"Everything else is a child of a lead"** wording.
   RULED: "Departments and HQ are the only top-level threads. Every other agent is a child: leads under their
   department, workers and reviewers under their lead, HQ advisers under HQ." (rule 13, §7).
10. **Owls "nothing large or multi-day".**
    RULED: "nothing large or multi-day on Owls without HQ's go" (§6).
11. **Department protocols with old numbers** (`Docs/Experiments/P1M/PROTOCOL.md`, `Theory_work/Dept/PROTOCOL.md`).
    RULED: HQ orders the departments to update them; the handbook (§9) says it wins on any conflict meanwhile.
