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

## (c) For HQ to decide

1. **Which model runs manager threads now:** Neon (old §1a, 11-27) or Opus on Claude Work (11-24 roster)?
2. **Non-theory councils:** I wrote Opus + Sol with Neon optional (from old §1a). Confirm, or make all councils
   Opus + Sol + Neon.
3. **Task-specific owner review orders** (PAPER-DRAFT: one Fable + Astra round; TH-SONG final pass) differ from the
   default. I wrote that a specific owner order overrides the default for that task. Confirm.
4. **`HQ_NOW.md` is stale** where the handbook points to it: roster (11-15 thread ids, `BVS-wt` paths), ACCOUNT
   ALLOCATION (11-15 / 11-24 entries). Please refresh it.
5. **Overnight / continuous mode** (HQ decides owner-reserved items while the owner is away): is it still in force,
   and does it cover Fable/Astra approvals?
6. **Restore-point cron:** still running after the REORG? If so, add its current path back.
7. **Lean work** until a Lean department exists: I assigned it to Theory. Confirm.
8. **"Large campaigns need the owner's GO through HQ"** is consolidated from the 11-25 to 11-27 practice (every 100-seed
   grid was owner-signed). Confirm as a standing rule.
9. **Today's rule "everything else is a child of a lead"** literally excludes leads (children of the department) and
   HQ's own advisers (children of HQ). I wrote "everything else is a child".
10. **Owls "nothing large or multi-day"** vs the multi-day riboflavin fits run on Owls: keep the rule, or allow
    exceptions with HQ's go?
11. **Department protocols still carry old numbers:** `Docs/Experiments/P1M/PROTOCOL.md` (≤ 150 tasks, Owls ≤ 16
    cores, refs to POLICIES §14) and `Theory_work/Dept/PROTOCOL.md` (PROTOCOL_v4 council and Codex-seat rules). The handbook wins, but the
    departments should update them.
