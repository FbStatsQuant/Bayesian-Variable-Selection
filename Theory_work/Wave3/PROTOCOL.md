# Theory Wave 3 — protocol (binding)

Extends `Theory_work/Wave2/PROTOCOL.md` (which extends Wave1C and Wave1): three review layers (statement lock;
lemma-by-lemma cross-family checks with falsification numerics; independent mid-point; exhaustive sweep; council of one
OpenAI seat + one Claude seat, both ≥ 8.0 with all six gates in the same round, max 3 rounds), anti-hallucination rules
(no claim without a file; citation-check script; statuses verbatim; reviewers briefed to break). Folder:
`Theory_work/Wave3/<TICKET>/`. Read `Theory_work/Wave3/PROGRAM.md` first: it defines the target package.

## Changes in Wave 3
1. **Effort cap:** every agent, Claude or OpenAI, at effort/reasoningEffort `high` at most — never xhigh/max/ultrathink.
   Strong OpenAI reviewer = gpt-6-astra (high); routine = gpt-6.1-sol (high).
2. **Providers (until further notice):** Claude Personal (`claude-personal`) runs **only Claude Fable 5.2**. Every
   Opus/Sonnet/Haiku agent, including your subagents and council seats, runs on **Claude Work** (`claudeAgent`).
   OpenAI agents on `codex`.
   **Amended 2026-11-10 (owner):** about 2/3 of all Claude inference on Claude Personal and 1/3 on Claude Work;
   Fable 5.2 still only on Claude Personal. Leads keep a running tally in LOG.md.
   **Amended 2026-11-11 evening (owner, supersedes the above):** every Claude agent — Fable 5.2 included, leads,
   subagents, council seats, scheduled runs — runs on **Claude Work** (`claudeAgent`). Claude Personal is not used.
   OpenAI agents stay on `codex`. (The Console API credits for the batch audit are a separate account, not a thread.)
   **Amended 2026-11-11 (owner), supersedes the 2026-11-10 line until further notice:** Claude Personal runs **only
   Fable 5.2**; every other Claude agent (Opus/Sonnet/Haiku, incl. subagents and council seats) on **Claude Work**.
3. **Sharpness gate (before heavy proving):** after the statement lock, write `ASSUMPTION_MAP.md` — one page: where
   each assumption enters the proof sketch and whether it looks necessary; run **boundary-violation numerics** (simulate
   just outside each assumption; if the conclusion still holds, flag the assumption `improvable`); and get one fresh
   **"better theorem" review** (Astra high) asked only to propose a strictly better provable statement. Record the
   outcome; HQ decides whether to strengthen the target before proving.
4. **Design-agnostic statements:** no design family in any theorem statement; families only as examples.
5. **Interface properties:** a shared assumption A enters through one bridge lemma A ⇒ P; theorems consume P.
6. Token efficiency: grep and targeted reads; summarise; do not paste long files into replies.
7. Final report as before, plus: assumptions list with ids, `implies` relations to existing results, and the
   sharpness record (for the registry being built in `Theory_work/INFRA/`).
8. **Registry block (from 2026-11-10):** every REPORT.md ends with the registry block from
   `Theory_work/INFRA/templates/ASSUMPTION_MAP.md` (on branch `theory/infra` / PR #6 until merged), with per-clause
   statuses — one status per claim, never one status for a bundle of results.

## Resume rules (binding from 2026-11-11; HQ; revised after pipeline review R01, `PIPELINE_REVIEW/`)
Everything above still applies. Rollback, supersession and who-decides are in `Theory_work/INFRA/LIFECYCLE.md` (now on
main); this section wires them into the ticket workflow. Where this section and an older rule differ, this section wins.

9. **One branch per ticket, revertable.** Each ticket runs in its own worktree on branch `theory/<TICKET>`, made by HQ.
   Workers still change no git state. HQ commits on the ticket branch at every checkpoint and before every review round
   (restore points), and merges to `main` with a merge commit (no squash). Rolling back a merged ticket follows
   LIFECYCLE §3. Claim rows are never deleted: retracted or deprecated claims stay as tombstones, so propagation still
   reaches their dependents.
10. **Hard checkpoints (HQ gates).** At each checkpoint the lead writes `CHECKPOINT_<k>.md` and **ends its run** with
    that content as its final message. HQ reviews it, commits, records its decision in the ticket LOG together with the
    checkpoint commit hash, and either continues the lead (same thread) or redirects it. No work past a checkpoint
    without HQ's go. So if HQ is unavailable, proof work stops rather than running on.
    - **CP1: target fixed.** After the statement lock and the sharpness gate (ASSUMPTION_MAP, boundary-violation numerics,
      "better theorem" review). Report the locked statement, each assumption's necessity reading, and the better-theorem
      proposal, with a disposition for each credible improvement (adopt / reject with evidence / defer as a named open
      item). HQ decides whether to strengthen the target before heavy proving.
    - **CP2: key lemma proved.** After the independent mid-point review, whatever its verdict. Report the verdict, what is
      proved and checked (with review files), and what is left, with an honest estimate.
    - **CP3: final.** Two outcomes, never mixed:
      - **CP3-PASS.** Requires both council seats ≥ 8.0 with all gates passing in the same round, on the **same frozen
        manifest** (rule 15). Then comes HQ's acceptance audit, run on the **proposed merged tree**: merge current `main`
        into the ticket branch first. The audit checks:
        - the consumed claims are still valid on current `main` (rule 11);
        - the REPORT registry block goes through the staged ingest, on a copy of the registry, with 0 problems;
        - `check.py` (with `--acceptance <claims>` once available) shows 0 ERROR on the staged registry and again after
          the apply;
        - the citecheck is re-run, with 0 MISS;
        - every "checked" sentence names a review file;
        - `manifest.py verify` passes, or each diff since the freeze went through rule 15.

        Only then: PROVED-CHECKED labels, ingest, `council-pass`, merge.
      - **CP3-EXHAUSTED.** The council did not pass within 3 rounds. The result keeps its actual status: no
        `council-pass`, and no PROVED-CHECKED for any clause that failed a gate. It may be committed on its branch as a
        record. A narrowed statement is a new target: it goes through CP1 again and passes its own council.
    - **Headline strength (finding R05).** A claim enters the paper headline only if its strength gates (`lit:`,
      `necessity:`, `better:`) are recorded and every credible better-theorem proposal has an evidence-backed
      disposition. If the statement changed materially after CP1, the better-theorem review is repeated on the final
      statement. Otherwise the claim can still be accepted as a checked result, labelled `headline-strength pending`.
    - **Compute tickets (W3-P6).**
      - CP0 is HQ's approval of a **representative smoke manifest**: the smallest set that covers both driver versions
        (b1 v2, b2 v3), each n level, and the most expensive calibration regimes (largest p per n).
      - CP1 is the smoke gate: outputs read back, invariants pass, and measured time per cell is reported.
      - The remaining tasks are then released in batches whose projected cost (measured per-cell times) fits within the
        **aggregate ceiling of 1,400 core-hours counted from the resume** (HQ 2026-11-11: NOTS bills 2 CPUs per task; the
        495.88 core-h spent before the pause are sunk), i.e. **1,896 core-hours in total** for all w3p6_ jobs since
        2026-11-09 (sacct CPUTimeRAW), smoke included. Nothing beyond the smoke
        manifest is queued before CP1.
      - **Hard backstop (worst-case admission):** a batch is submitted only if Σ over all queued and running
        w3p6_ tasks of (time limit × cores) + core-hours already used (since 2026-11-09) ≤ 1,896. Slurm time limits then make the
        ceiling hold even if no agent or HQ is watching. The lead logs this ledger in LOG.md at every release.
      - A projected overrun stops further releases and returns to HQ. Invariant failures (wrong HPM bookkeeping,
        corrupt output) stop everything; resource-limit outcomes (time limit, preflight refusal) are logged, follow the
        DESIGN policy, and are not counted as failures.
      - CP2 = all released tasks done, before the analysis. CP3 = REPORT + council, as above.
11. **Consumed claims: validity and assurance.**
    - A ticket uses only claims that are ACTIVE in `INFRA/registry`, cited by registry id with version.
    - A consumed premise below PROVED-CHECKED (author-only, PARTIAL, OPEN, UNSPLIT-STATUS) may be used only if it is
      stated as an explicit hypothesis of the new result and carried into its status text ("conditional on …"). A
      checked descendant never upgrades it silently.
    - Before every continuation and every merge, HQ compares the state and version of each consumed claim on current
      `main` against the ticket's base.
    - When any reviewer, CI run or re-audit raises a finding against an ACTIVE claim, HQ:
      - prices it with `propagate.py --dry-run`;
      - marks it per LIFECYCLE §3;
      - notifies **every running ticket that consumes it**, recording the notification and the lead's acknowledgement in
        that ticket's LOG.

      A lead that hits such a finding stops using the claim and reports at once (an early checkpoint). Felipe approves any
      change to a headline claim.
12. **Heartbeat and watchdog.**
    - `LOG.md` gets a timestamped entry at every step, recording the agents started so far (model, provider, role).
    - HQ checks every ticket's last LOG entry every 3 h while the wave runs.
    - A separate **watchdog** scheduled task, not bound to the HQ thread, runs every 6 h. It reads the ticket LOGs and
      `HQ_DECISIONS.md`, plus the P6 core-hours used so far (NOTS, read-only). It flags:
      - a checkpoint unanswered for more than 6 h;
      - a ticket with no LOG entry for more than 3 h and no report;
      - P6 spending above its ceiling.

      It writes its findings to the HQ thread and to `Theory_work/Wave3/WATCHDOG.md`, for Felipe.
    - **Fail-closed holds (R03 N5).** Containment does not wait for HQ. Any scheduled task (watchdog, daily CI, weekly
      re-audit) that finds a check ERROR, a failed falsification script, or a reviewer finding against an ACTIVE claim, or
      P6 spending above 1,700 core-hours in total (since 2026-11-09), appends one line to the **hold file**
      `C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave3/HOLDS.md` (main checkout, absolute path):
      `HOLD <claim id | P6> <UTC time> <source> <one-line finding>`. Holds never edit the registry.
      - Every lead reads the hold file before each step. If a held claim is among its consumed claims (transitively), or
        it is the P6 lead and P6 is held, it stops using that claim (P6: submits nothing more), writes an early
        checkpoint and ends its run.
      - Only HQ lifts a hold, by appending `LIFT <id> <time> <disposition>` after the rule-11 triage (propagate dry-run,
        LIFECYCLE §3 action, or "no finding"), recorded in `HQ_DECISIONS.md`.
    - The IDs and next run times of the heartbeat, watchdog and CI tasks are recorded in `HQ_DECISIONS.md` **before**
      launch.
13. **Continuous audit.** `INFRA/ci/run_ci.py --steps check,paper,falsify,cite` runs daily, scheduled by HQ. One random
    PROVED-CHECKED claim is re-audited weekly by a fresh Astra (high). Any ERROR or failure opens an issue and follows
    rule 11.
14. **Kill budgets and waivers.**
    - Path-level condition: one Fable attempt and one Astra break review, then stop unless a sketch survives.
    - W3-RM2: 3 failed proof attempts on its key lemma → STUCK at CP2.
    - Council not passed after 3 rounds → CP3-EXHAUSTED.
    - **No review layer may be skipped or replaced without Felipe's explicit approval**, recorded in `HQ_DECISIONS.md`.
15. **Frozen review content and blind first reads.**
    - Before each review round (council, sweep, mid-point), run
      `python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/<T> Theory_work/Wave3/<T>/reviews/MANIFEST_<round>.txt --extra Theory_work/Wave3/<T>/reviews/INPUTS.txt`
      (from the repo root; all paths repo-relative — R03 F9),
      where INPUTS.txt lists every external input the proof relies on: premise sources, inherited proofs, pinned code.
      INPUTS.txt never lists wave documents (PROGRAM, PROTOCOL, LIFECYCLE, templates) or registry tables (`claims.tsv`
      etc.): they are not proof premises and change on `main` between rounds (HQ 2026-11-12, after W3-START CP3).
      HQ commits it on the ticket branch.
    - Each council reviewer ends its reply with exactly one `COUNCIL-VERDICT round=R<k> manifest=<digest> seat=<seat>
      score=<x.y> gates=PASS|FAIL` line (template `Theory_work/INFRA/templates/COUNCIL_BRIEF.md`; LIFECYCLE §4.1); mid-point
      and sweep reviewers quote the digest. At CP3, `manifest.py bind` must pass on both council
      replies of the passing round, and `manifest.py verify` on the final tree; a corrupted manifest fails. Nothing in
      the manifest is edited while that round runs.
    - HQ writes every blind brief to `reviews/BRIEF_<round>_<seat>.md` before launching. That file is the reviewer's
      whole brief and lists the files it may read; listing a prior review, disposition or score in a blind brief is a
      protocol breach.
    - After a round, a substantive change (any change to a statement, a proof step, a premise or a code pin) needs a
      fresh review of the change and of what depends on it. An editorial-only change needs a diff check by an
      independent Sol reviewer, attesting "editorial only".
    - Every scored review is a **blind first read**: the reviewer gets the frozen statement, proofs and the sources it
      needs, and never earlier reviews, dispositions or scores. In rounds ≥ 2, a separate **reconciliation** reviewer
      checks each earlier finding against the new manifest and gives a verdict per finding. Passing a round needs both:
      the blind scores, and every earlier CRITICAL or MAJOR finding resolved.
16. **[LIFTED 2026-11-12 by HQ: R04 fix merged 656982a, Sol RESOLVED, 134/134 on main] Interim, until the INFRA tool fixes for findings R02–R06 are merged and reviewed:**
    - no CP3 ingest or merge;
    - no `propagate.py --apply` on a claim introduced by a merged ticket;
    - every bridge or interface property a claim uses is written as an explicit `depends_on` edge.
