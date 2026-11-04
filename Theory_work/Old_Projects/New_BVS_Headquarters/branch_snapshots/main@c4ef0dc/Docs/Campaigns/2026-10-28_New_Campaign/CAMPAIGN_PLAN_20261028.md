# Campaign plan: from scattered results to a proved, Lean-checked paper (DRAFT v1, 2026-10-28)

Written by HQ from Felipe's big picture (conversation of 2026-10-28). Draft for discussion; nothing has been launched.

## Principles (Felipe)

1. **Unify first.** Stop adding pieces; consolidate the variants, benchmarks, simulations and theory into one body of work.
2. **Paper = execution before theory.** The executed method must match the written methodology. If it does not, we fix it and redeploy.
3. **Patch everything we can before the hard theory.**
4. **Let the data talk.** The simulations are also instruments for the theory. They are read together with all prior knowledge of the method.
5. **Each hard theorem ends in one of two outcomes:**
   - it holds, or a comparably strong result holds under reasonable assumptions;
   - it hits a fundamental obstruction, so the method must change.
6. **Investment rule for a method change plus a full rerun.** Do it only if both hold:
   - with the change, all or most of the key results are provable;
   - there is strong evidence, from a pilot, that the method still performs well.

   No large runs on gambles. The benchmarks need no rerun while the datasets are unchanged.
7. **Committed rules.** Settings may differ for low p (n = 200), but only as one committed rule for every p ≪ n case.
8. **Believed versions before the swarm.** Fable leads the refinement of every hard statement. Felipe gives the green light, and only then is the proof swarm released.
9. **Lean last.** Every accepted proof is formalised in Lean.

## Model hierarchy (the company analogy)

| Role | Models | Use |
|---|---|---|
| Managers | Opus 5.5 | Lead every thread: plan, delegate, integrate, decide routine questions. HQ is one of them |
| Consultants (expensive, hired per task) | Fable 5.1, Astra | Fable: statement refinement (leads it) and scoped, very hard mathematics. Astra: adversarial checks, adjudication, second opinions |
| Reviewer | Sol 6.1 | The default thorough reviewer (numbers, conformance, proofs). Worker only with a tight brief |
| Workers (cheap labour) | Sonnet 5.5, Terra 6.1, Haiku 5.5, Luna | The bulk of the volume. Sonnet and Terra take skilled scoped tasks; Haiku and Luna take clerical work (files, logs, Slurm, tables, checksums) |

- **Capacity.** Other multi-day campaigns are running, so at most 2–3 campaign threads run at once and Fable calls are counted.
- **Protocol override.** Opus leads proof threads (an override of `proof.md`), except that Fable leads statement refinement.

## Phases and gates

### Phase 0: Consolidate
**Goal:** one source of truth for what exists.

**Deliverables:**
- a ledger of method versions and variants tested (what, when, outcome, superseded by what);
- one registry of simulations: every campaign, its design, its status, and the location of its data;
- the benchmark state, including the open gates;
- the theory state.

**Inputs:**
- `04_Reports_and_Presentations/STATUS_BRIEFING_20261028/BRIEFING.md`;
- `INVENTORY_20261028`;
- `FROZEN_LIST.md`;
- the experiment folders A–H;
- the memory notes.

**Staffing:** an Opus manager; Sonnet/Terra workers for extraction; Haiku/Luna clerks; a Sol review.

### Phase 1: Conformance
- **1a. Paper-vs-execution audit for p ≫ n.**
  - Compare the methodology as written (METHODOLOGY_v3 and master Part I, i.e. what the paper will describe) with the production code and its outputs.
  - Every deviation is classified as **cosmetic**, **wording fix** or **behavioural**.
  - Pass rule: no behavioural deviation; otherwise patch and redeploy (Phase 3).
  - Builds on the existing alignment audits (`INVENTORY_20261028/work/S_A–S_C`).
  - Staffing: an Opus manager; Sol primary reviewer; Terra/Sonnet workers.
- **1b. Design of the low-p study.**
  - n = 200, p ∈ {10, 20, 30}, S1–S6 (blocks of 5 fit all three p).
  - The exact posterior comes from full enumeration.
  - Outcomes: log Z error, PIP error, agreement of the HPM and PIP > 0.5 model with the exact posterior, and selection.
  - Design decisions needed (Q1–Q6 below).
- **Gate G1 (Felipe):** the conformance verdict and the low-p design.

### Phase 2: Patch
Everything we have, or nearly have:
- **Method and code:**
  - `cut_group`;
  - logging of the stop phase;
  - the stop budget and retry asymmetry;
  - the committed exact-branch rule for small p;
  - optional LS0 (local search also from the start mode);
  - instrumentation for the theory.
- **Spec and theory wording:**
  - the secondary PIP;
  - T13;
  - restatements for the run as designed to finish;
  - T34.
- **Benchmarks:**
  - re-issue the G9 c = 0.5 verdict;
  - G5 disclosure;
  - the full `cv_1se`/`K37` rows;
  - review of the scoring code.

Each patch is tagged by whether it changes outputs.

### Phase 3: Deploy (instrumented)
- **The low-p study:** new runs plus exact references.
- **p ≫ n:** first extract everything possible after the fact from the existing 2,400 fits, with no rerun:
  - the truth score against the HPM;
  - T37's TD condition;
  - start masses π₀ (deterministic from the blocks);
  - LS0 after the fact.
- **Rerun the p ≫ n SMC arm only if** Phase 1a or 2 changes outputs, or a theory measurement needs the in-run trace (when and how the truth was first scored; the phase at which a fit stopped).
- **Gate G2 (Felipe):** approve the run sizes and budgets.

### Phase 4: Let the data talk
Analysis joining the measurements with prior knowledge:
- which premises hold;
- where and why the method fails;
- which conjectures the evidence supports or contradicts.

**Output:** an EVIDENCE report that feeds Phases 5–6.

### Phase 5: Theory layer 1
Restate the locked results, finish the near-complete partial ones, and do the bookkeeping:
- T12, T21, T07;
- T26 scope;
- T02 tail sharpening;
- T03 restatement;
- the T05 remark.

**Staffing:** Opus-led, Sol review, Fable only on a specific stuck step.

### Phase 6: Vetting the hard targets
- **Targets:** T37, T22+T27 on one family, T38, T26(i)–(ii); T24 and T39 as fallbacks.
- **Lead:** Fable leads statement refinement.
- **Per target, a confidence card:**
  - the refined statement;
  - the data evidence;
  - exact small-case tests (p ≤ 30);
  - the proof skeleton with its crux isolated;
  - Astra's attack and Sol's review;
  - risk;
  - whether a method change is needed.
- **Gate G3 (Felipe):** green light per card.
- **If a card fails, scenario 2:** a method-change proposal under the investment rule, with a proof sketch and a pilot. If approved, loop back to Phases 2–3, with one redeploy carrying all changes together.

### Phase 7: The swarm
Proofs of the green-lit targets: Opus-managed, worker-heavy, Sol and Astra reviews, Fable only on cruxes. Output: a full proof per target, in the project's usual reviewed form.

### Phase 8: Lean
- Formalise every accepted proof with `lean.md`, Opus-led, then merge them with `lean-merge.md`.
- Scope and cost each theorem first. The exact, finite results (T07, T21, T11(iii), T12, T37(i)) are mechanical; the probabilistic and asymptotic ones need Mathlib groundwork.

### Phase 9: Assembly
One consistent theory section, plus the empirical package, ready for the paper protocol.

## Decisions so far (Felipe, 2026-10-28)

- **p values:** drop p = 10; the low-p study uses **p ∈ {20, 30}**, n = 200. At both p the SMC path runs: 2²⁰ and 2³⁰ exceed the exact-branch threshold of 12,560·p.
- **Generation:** same as p ≫ n. The only changes are the n/p relation and the covariances.
  - The six covariances, built from blocks of 5.
  - Signals placed by the same placement rule, with the same coefficient pattern.
  - X standardised the same way; the same seed scheme.
- **Truth size** (Felipe: "your call"; HQ decided): keep the p ≫ n rule of one signal alone in each block of 5, so s₀ = 4 at p = 20 (all 4 blocks active) and s₀ = 5 at p = 30 (blocks 1–5, as in master §II.3). Coefficients follow the first s₀ values of the same pattern.
- **Phase 0 scope** (Felipe: "manage it yourself, simplify"): one ledger at two depths. One line per superseded item; full detail only for what feeds the paper.
- **Benchmarks at low p** (HQ default; Felipe may override): run the 8 primary panel methods with their primary rules only, no variants. They are cheap at p ≤ 30 apart from the horseshoe.
- **Scales:** c ∈ {1, 0.5} throughout.
- **Purpose:** low p is multi-purpose. It assesses both
  - **SMC accuracy:** Ẑ and the PIPs against the exact posterior;
  - **BVS accuracy:** selection against the truth.
- **Compute:** any run with more than 10 seeds goes to NOTS, under the no-hefty-data rule (copy, verify, delete).

## Open questions for Felipe (low-p design and staging)

- **Q1. Truth at p = 10 and 20.** The master defines s₀ = 5 only at p = 30. Options: keep s₀ = 5 everywhere, or a committed rule (e.g. s₀ = ⌊p/6⌋ → 1, 3, 5).
- **Q2. Exact branch.** At p = 10 the method enumerates exactly (2¹⁰ models fall below its threshold). Options:
  - keep that as the committed small-p rule, so p = 10 checks the exact branch;
  - change the threshold so SMC runs at every low p.
- **Q3. Scales and replicates.** For example c ∈ {1, 0.5} × 100 replicates, or fewer replicates with several SMC seeds per dataset (repeat seeds are cheap once a dataset is enumerated).
- **Q4. Benchmarks at low p.** Run selection benchmarks there too, or SMC-BVS against exact enumeration only?
- **Q5. Compute for the 2³⁰ enumerations.** Owls or NOTS (NOTS only with the no-hefty-data rule). Time one enumeration first.
- **Q6. Phase 0 scope.** Which earlier variants or campaigns must the ledger cover (all of A–H, or only what feeds the paper)?
