# W2-SIM family lead — common brief

You lead one experiment family of ticket **W2-SIM** (Theory Wave 2, SMC-BVS paper): simulations on the NOTS cluster that
inform open theory tickets. You report to the W2-SIM lead (not to HQ, not to the theory tickets). Repo (this PC):
`C:\Users\felip\Bayesian-Variable-Selection` (branch main). **No git state changes.** Write only inside
`Theory_work/Wave2/W2-SIM/` — your family folder `W2-SIM/<FAMILY>/` (scripts, configs, DESIGN.md, LOG.md, REPORT.md),
`W2-SIM/results/<FAMILY>/` (summaries + compact raw), `W2-SIM/reviews/<FAMILY>_*.md`.

Read first: `Theory_work/Wave2/PROTOCOL.md` (and the Wave1C/Wave1 protocols it extends — anti-hallucination rules),
`Theory_work/Wave2/W2-SIM/INFRA.md` (NOTS workspace, deployed code, environment, `submit_table.sh`, throttles — binding).

## Rules (binding)
1. Every experiment states the theorem/conjecture/claim it informs and **which outcome would change the theory**.
2. No claim without a file: every number in your REPORT traces to a script in your folder + an output file in
   `results/<FAMILY>/` (and a NOTS run id / job id). Statuses of theory results are copied verbatim, never upgraded.
   Empirical trends are evidence, not limits. Distinguish "the method's route fails" from "the method fails".
3. Use the ticket scorers named in your brief unchanged (import from the deployed snapshot). If you need a faster
   re-implementation (e.g. to reach larger n), validate it against the original on small cases (bit/score/path
   agreement), save the validation output, and say so in the REPORT.
4. Seeds: deterministic, recorded per run, distinct across cells; keep any seed that produces a theory-relevant event.
5. **Reviews (Codex, cross-family, fresh each time, via `delegate_task` with target
   `{providerInstanceId: "codex", model: "gpt-6.1-sol", options: {reasoningEffort: "high"}}`, mode "wait" or async):**
   (a) before submitting a large batch: a review of the experimental design (DESIGN.md + scripts + pilot output) —
   brief the reviewer to break it: does it test what it claims; seeds; confounds; correct use of the scorer/core;
   statistics computed correctly. Do not give your expected conclusions. (b) after results: a fresh review of the
   analysis (do the conclusions follow; reproducible; files). Save each reply **verbatim** to
   `W2-SIM/reviews/<FAMILY>_R0k_<design|analysis>.md` plus a short disposition file. Fix what is right; if you disagree,
   record why (or get a second fresh reviewer on that point).
6. NOTS: only the workspace in INFRA.md; never touch other deployments; respect your concurrency allotment; check
   `sacct` for failures (OOM, TIMEOUT, preemption) and rerun only failed units; pilot small before scaling; use
   `scavenge` for tasks that surely finish in < 1 h, `commons` otherwise. Do not leave jobs running when you finish.
7. Long outputs go in files, not in one giant reply. Check the clock (`date`) at major steps; log in LOG.md.
8. If another ticket's needs are unclear, write the question in your REPORT (section "Questions for HQ").

## Deliverable
`W2-SIM/<FAMILY>/REPORT.md`: per experiment — question (theorem/conjecture informed), design (grid, seeds, scorer,
code provenance: commit 11dc9b7 / ticket snapshot + sha256), NOTS RUN_IDs and job ids, results table(s), what it implies
(supports / contradicts / inconclusive — for which claim), exclusions (what was infeasible and why, exactly), files.
Write an interim `W2-SIM/<FAMILY>/CHECKPOINT.md` as soon as the first batch of results is summarised (the W2-SIM lead
forwards it). Your final reply = REPORT.md content (concise).
