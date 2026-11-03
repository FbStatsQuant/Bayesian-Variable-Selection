# MEET-v31 · Format notes (for HQ, to reuse in the theorem meeting)

Written by the chair, 2026-11-03. What worked and what did not in this meeting format: three seats (two Fable 5.1 on separate Claude accounts, one gpt-6-astra on Codex), a non-voting chair (Opus 5.5), two rounds plus settlement, evidence by tests and proof checks.

## What worked

1. **Independent Round 1, then rebuttal against a disagreement table.** The three R1 positions agreed on most items. The table in SYNTH_R1 §2 (item, positions, crux, "settled by test / proof check / decision") focused Round 2. In Round 2, 8 of 10 dispute rows closed on concessions or evidence. Keep the format: *crux* plus *what settles it* per row.
2. **Cross-family seat.** Seat C (Astra) produced most of the claims that changed the outcome, and they held up under checking:
   - the analytic upper bound on Z (refuting a candidate "inherent limitation");
   - max{Z_𝒯, 0.05Ẑ} coverage;
   - the finite-R bound;
   - the A2 counterexample;
   - top stores not nested under eviction;
   - the mutable counters in `Data`;
   - its warning against relabelling missing proofs as inherent limitations.
   The two Fable seats were closer to each other. They were stronger on the repository's internal evidence: the calibration-cost formula, item-9 tables tied to code lines, and the study cross-tabs. Keep one cross-family seat.
3. **Proof checks by a fresh Opus task (PC1, PC2), filed verbatim as evidence**, with scripts and fixed seeds. PC1 settled four disputes in one pass:
   - confirmed 3 of C's claims;
   - refuted B's ⅓ threshold;
   - gave a counterexample to monotonicity in D3a;
   - showed no theorem needs it.
   Batch all math claims from a round into one check, phrased as "verdict per claim, never upgrade".
4. **Fixing the decision rule before the result.** Asking seats in Round 2 for the ABL-START rule *before* the data arrived produced a merged, pre-registered rule (SYNTH_R2 §2). This is the right way to handle evidence that arrives mid-meeting.
5. **A procedural rule for "no open questions"** (SYNTH_R1 §3), amended by the seats. It separates:
   - method questions, which must be closed;
   - theorem obligations, which name the decision they could overturn and why it survives;
   - inherent limitations, which must be PROVED impossible or true by definition.
   Without it, "no open question" invites relabelling. Reuse it verbatim in the theorem meeting.
6. **Verbatim seat files from the transcripts.** The chair extracted each seat's final message from its local session file (Claude: `~/.claude*/projects/<cwd>/<session>.jsonl`; Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`) instead of retyping it. This kept the files exact and saved chair context.
7. **Chair fact-checks marked [chair-checked].** Short code or data checks (counters, J vs ⌈p/B⌉, arm-A bitwise identity, exact-branch boundary) resolved factual disputes faster than another round would have.

## What did not work, and fixes

1. **An amendment arrived after Round 1 was dispatched** (Amendment 01, item 9). It cost item 9 a round of independent positions. Seats answered it only in Round 2, with the R1 texts in view. *Fix:* freeze the agenda before dispatch, or give late items their own independent mini-round.
2. **Evidence that ran outside the meeting failed silently.**
   - The ABL-START SDK worker ended its session while "waiting for fits" ($2.45 spent, no results).
   - Its Owls jobs were then all terminated (rc = 143, cause unrecorded) with 9/48 fits done.
   - The chair relaunched the remaining arms.
   *Fix:* long empirical runs should not depend on an agent session staying alive. Launch the fits as standalone `owls_run` queues with a summary script, and have the agent (or chair) only read results. Log who stops a job.
3. **The study's per-island outputs are not on the machine where the meeting runs** (NOTS/laptop only). So the agreed post hoc PIP rescoring could not run on the 2,394 fits. *Fix:* before a meeting, HQ syncs the small per-fit summaries the agenda needs (`log_Z_r`, `pip_r`, timings) to Owls.
4. **Seats re-derive what another seat already proved.** For example, all three re-proved C's bound. This costs tokens but adds little after a proof check exists. *Fix:* in rebuttal rounds, tell seats which claims have a filed proof check and not to re-derive them.
5. **Seat outputs are long** (22–52 KB in Round 2). The chair's synthesis is then the bottleneck. *Fix:* cap the free text per item, and ask for a fixed table per dispute (concede/hold, evidence that would change the position, class, study effect).
6. **Status words in seat texts.** Seats sometimes wrote PROVED for their own elementary arguments, which no one else had checked. The chair treated these as claims until a proof check confirmed them. *Fix:* the brief should say "PROVED (by this seat, unchecked)" is the only allowed form until a check is filed.

## Costs

- Seats and checks ran on subscription accounts.
- Settlement API spend: see `MINUTES.md` (the chair's paid budget was $20).
- The chair's relaunch of ABL-START used 3 Owls jobs × 2 cores for about 1–1.5 h.
