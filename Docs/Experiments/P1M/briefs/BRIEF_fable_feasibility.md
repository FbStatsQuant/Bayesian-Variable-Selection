# BRIEF — feasibility expert: "Is there a way of making p = 10⁶ feasible?" (Fable 5.2, high)

Commissioned by the SMC - Engineering Department at the request of Theory HQ and the owner (Felipe Bedoya), 2026-11-15.
You are a fresh, **independent expert**. The documents below are inputs to challenge, not conclusions to adopt. The owner
agrees with the 10⁴ → 10⁵ → 10⁶ ladder and wants a direct expert answer.

## The question
Find the most credible way(s) to run **this method — joint Bayesian variable selection on all p, no screening or
splitting of the target** — at p = 10⁶ on NOTS within:
- 1,536 CPUs and 2,304 GB of memory per user (commons partition, Sapphire Rapids nodes, 192 hardware threads = 96 physical
  cores per node, 251 GB);
- 24 h per job; **no multi-day runs**;
- a budget of **at most about 30,000 billed core-hours** for the whole experiment. Billing is per hardware thread:
  2 per single-thread task.

Verdict: **FEASIBLE** (how), **FEASIBLE-IF** (which conditions or measurements), or **NOT-FEASIBLE** (the binding
obstruction). Show the arithmetic.

## Attack the three known blockers with numbers
(a) **Memory bandwidth of the Gram-free step**: about 168 TB of X reads per island at 1M (n = 200).
    Options to assess (and others you find): label-major or batched kernels; low-precision or bit-packed X;
    caching candidate-neighbourhood Gram blocks; sufficient statistics; block sparsity of the neighbour graph.
(b) **Evidence-weight degeneracy across islands**: sd log Ẑ_r ≈ 1 and R_eff 1.6–4.2 of 16 at p ≥ 5k (HQ's R6 answer in
    `REQUESTS.md`), and a calibration that does not converge at p ≥ 10k.
    Options to assess (and others): more particles where it matters; tempering-schedule changes; merging by the union of
    scored models instead of evidence weights; splitting the space so that islands target disjoint parts; a two-level
    design.
(c) **Calibration cost**: sequential depth, rebuilds, escalation.

For each option give:
- the expected gain;
- the cost to build;
- its **output class**: preserves the output bit for bit / equal in law / changes the method. If it changes the method,
  name the theorem premises it touches;
- how to test it cheaply at 10⁴ / 10⁵.

## Measure where you can (encouraged)
Small local benchmarks on Owls, the machine you are on, are allowed and encouraged, to replace guesses with numbers.
Examples:
- memory bandwidth curve vs thread count;
- the current engine's step kernel or a Gram-free prototype at p = 10⁵, and as far as memory allows toward 10⁶;
- block-size and table counts.

Limits:
- at most 8 cores, `nice -n 19`, each run ≤ 15 minutes, total ≤ about 2 core-hours, at most 16 GB of RAM (Owls is shared);
- **no NOTS access** (you have none);
- work only in `/home/fb31/p1m_feas_bench/` (create it). Copy the core there to compile; never compile inside the repo
  (the core's `v3.R` writes a `.cpp_cache` next to itself).
- Report every number with its command and conditions.

## Inputs (read)
In `/home/fb31/Bayesian-Variable-Selection` (branch `main`):
- `Docs/Experiments/P1M/BRIEF.md`, `EXPERIMENT_PLAN.md`, `ENGINEERING_SPEC.md`, `REVIEW_fable.md`, `OWNER_DECISIONS.md`,
  `NOTS_FACTS.md`, `REQUESTS.md` (R6 answer);
- W3-SCALE, via `git show origin/theory/W3-SCALE:<path>`: `Theory_work/Wave3/W3-SCALE/CHECKPOINT_2.md`, `DESIGN_v1.md`,
  `results/*.tsv` (list them with `git ls-tree -r --name-only origin/theory/W3-SCALE | grep W3-SCALE/results`);
- the code: `Scripts/SMC_BVS/core/` (R drivers and `cpp/`);
- theory context as needed: `Theory_work/Wave3/PROGRAM.md`, `Theory_work/Wave3/BRIEFING/theory_status_2026-11-13.tex`,
  `Theory_work/Wave3/W3-DIST/STATEMENT.md` (read only), `Theory_work/Pause_2026-11/SCALING_DESIGN_v0.md`.

## Constraints
The theorems are about the method as coded; the paper must also cover the parallel method (islands + merge). Results are
asymptotic and design-agnostic. Any change to the law has to be labelled with the premises it touches.

## Rules
- **Write only** `Docs/Experiments/P1M/FEASIBILITY_fable.md` in the repo, plus whatever you need under
  `/home/fb31/p1m_feas_bench/`.
- Change no git state. Edit no other repo file.
- Do not touch `Theory_work/Wave3/W3-DIST/` (read STATEMENT.md only) or `Theory_work/Wave3/PROTOCOL_REVIEW/`.
- Read `Theory_work/Wave3/HOLDS.md` first.
- Start no sub-agents.

## Output: `Docs/Experiments/P1M/FEASIBILITY_fable.md`
1. A **10-line answer** to the owner's question, first: the verdict, the path, core-h and wall time per 1M fit, what must
   be measured.
2. The ranked paths (each with arithmetic, output class, build cost, test).
3. The recommended path, with its go/no-go gates on the 10⁴ → 10⁵ → 10⁶ ladder, and the budget against 30k core-h.
4. Measurements made (commands, numbers, conditions).
5. Risks, and questions for the owner.

Final message: at most 12 lines: the verdict, the top 3 points, the file path.
