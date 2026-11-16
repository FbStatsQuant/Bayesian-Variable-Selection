# BRIEF — independent review of the p = 10⁶ experiment plan + engineering spec skeleton (Fable 5.2, high)

Commissioned by: Experiment department (P1M), at the request of Theory HQ and the owner (Felipe Bedoya), 2026-11-15.
You are an **independent reviewer**. Form your own view from the files; the authors' documents are inputs to be
challenged, not conclusions to adopt. Be creative where it helps: alternative algorithms, data layouts and
experiment designs are welcome.

## Repository and rules
- Clone: `/home/fb31/Bayesian-Variable-Selection` (branch `main`). **Write only these two files:**
  `Docs/Experiments/P1M/REVIEW_fable.md` and `Docs/Experiments/P1M/SPEC_SKELETON_fable.md`.
- Change no git state (no commit, checkout, branch, stash). Edit no other file. No job submission; no cluster access
  (you have none). Read-only analysis: do not run builds or benchmarks.
- Do not touch `Theory_work/Wave3/W3-DIST/` or `Theory_work/Wave3/PROTOCOL_REVIEW/` except to read
  `W3-DIST/STATEMENT.md`.
- Read `Theory_work/Wave3/HOLDS.md` first.
- Start no sub-agents.

## Read (all of these)
1. `Docs/Experiments/P1M/BRIEF.md`: the department's mandate, the goals and the owner's requirements.
2. `Docs/Experiments/P1M/EXPERIMENT_PLAN.md`, `ENGINEERING_STRATEGY.md`, `OWNER_DECISIONS.md`, `NOTS_FACTS.md`: the
   plan under review and measured cluster facts.
3. W3-SCALE (the scaling ticket), via `git show origin/theory/W3-SCALE:<path>`:
   `Theory_work/Wave3/W3-SCALE/CHECKPOINT_1.md`, `CHECKPOINT_2.md`, `DESIGN_v1.md`, and `results/*.tsv` (list them with
   `git ls-tree -r --name-only origin/theory/W3-SCALE | grep W3-SCALE/results`).
4. The code: `Scripts/SMC_BVS/core/` (R drivers `v3_*.R`; C++ `cpp/*.h`, `cpp/v3_core.cpp`, `cpp/Makevars.v3`).
5. Theory context: `Theory_work/Wave3/PROGRAM.md`; `Theory_work/Wave3/BRIEFING/theory_status_2026-11-13.tex`;
   `Theory_work/Wave3/W3-DIST/STATEMENT.md` (distribution consistency; read §0 and §2 for what the code returns);
   optional: `Theory_work/Pause_2026-11/SCALING_DESIGN_v0.md`, `Theory_work/Wave3/BRIEFING/lit_review_large_p_BVS.md`.

## Theory hooks you must respect
- The theorems are about **the method as coded**. The paper must also cover the **parallel method** (many islands +
  merge). Any engineering change has to be classified: does it preserve the output bit for bit, preserve the law of
  every output, or change the law (and then which theorem premises must be re-checked)?
- Results are asymptotic and design-agnostic. Design families appear only as examples in experiments.
- Distribution consistency (W3-DIST) concerns distributions built from the run's output. **The code currently returns
  no posterior draws and no predictive.** Assess, **as an option, not a default**, returning posterior draws (of models
  and/or (β, σ²)) or a predictive distribution: what it would be, what it costs at p = 10⁶, and what it would buy the
  theory and the experiment.

## Mandate (a) — `REVIEW_fable.md`: improvement opportunities
Rank the most impactful ways to make p = 10⁶ **feasible and convincing**, by impact on feasibility, cost and risk. For
each: what, why (with file:line or table evidence), expected effect (numbers where you can), output-preservation class,
cost to build. Areas to examine, at least:
- memory and I/O at 10⁶ × n;
- screening-free versus screened designs;
- the evidence-variance problem (σ̂(log Ẑ_r) ≈ 0.09 at p = 2k and ≈ 1 at p ≥ 5k), its consequences for island
  pooling (evidence-weighted versus equal-weight PIPs, union stores) and for the calibration's escalation rule;
- the calibration cost (sequential depth, rebuilds, escalation);
- what to measure so the result is credible to referees (baselines, diagnostics, controls, reproducibility).

Also include: risks and blind spots of the plan, anything in the plan you think is wrong (with evidence), and the
questions you would put to the owner.

## Mandate (b) — `SPEC_SKELETON_fable.md`: an engineering spec skeleton that removes ambiguity
Sections, each concrete enough to build from (tables welcome; mark guesses as such):
1. components and their interfaces (inputs, outputs, file formats);
2. data layout and a memory budget per component at p = 10⁴ / 10⁵ / 10⁶ (state n);
3. parallel decomposition (islands, threads, nodes) and communication;
4. the **output-preservation contract**: what must be byte-identical to the current engine, what must be equal in
   distribution, what may differ (and how each is tested);
5. invariants and test gates;
6. failure modes, checkpoint/restart, statuses;
7. performance targets per stage at p = 10⁴ / 10⁵ / 10⁶.

## Output
- The two files above. Plain Markdown, concise, numbers with units, evidence by file:line.
- Your final message: at most 15 lines: your top 5 recommendations and the file paths.
