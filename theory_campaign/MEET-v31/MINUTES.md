# MEET-v31 · Minutes: "Methodology - Final meeting" (SMC-BVS paper 1)

Amended by HQ on 2026-11-04 (AMENDMENT_HQ_01.md) after independent review.

**Date:** 2026-11-03.
**Chair:** Opus 5.5 (Claude Work), non-voting.
**Seats:**
- A: Fable 5.1, Claude Personal, high effort.
- B: Fable 5.1, Claude Work, high effort.
- C: gpt-6-astra, Codex, high effort.

Every seat answer is a fresh task, committed verbatim.

**Reader:** Felipe, through HQ. Plain language. Status words follow `theory_campaign/PROTOCOL.md`. Every PROVED is a candidate (unreviewed), and a seat's opinion is not evidence.

## 1. Outcome in one paragraph

Paper 1 ships **v3.1 = v3 unchanged as a statistical method**: the target, the composite block start, the tempering bridge and kernel, the calibration law and budgets, and the HPM decision all stay. To this are added:
- a parallel execution layer over islands, local-search scans and block tables, never over variables;
- optional stacking of extra islands at the same per-island population;
- LS0, a local search from the start mode;
- the Ẑ-weighted PIP as primary;
- an estimator for general posterior summaries;
- a POST HOC certificate card;
- explicit unavailable-output fields;
- a set of wording and classification fixes from the (n, p)-generality audit.

No change is WORKHORSE. **The 2,400-fit study is not re-run**: its saved sampler estimates stand as v3.1 at R′ = 4, reusable with stated reporting limitations. Full v3.1 records are not yet produced: LS0 integration and flags, the NA interface, the certificates and the primary rescoring remain pending (POST HOC; no statistical refit is needed for them). The block start is kept; item 1 below records what the start ablation allows the paper to claim about it. The full diff is in `METHOD_v3.1_FINAL.md`. Theorem consequences are in `THEOREM_REVISION_INPUTS.md`.

## 2. Decisions, with reason and evidence

Sources: SYNTH_R1/R2/R3 and the files cited there. "All three" means all three seats accepted.

| # | Decision | Reason | Evidence / check | Closed in |
|---|---|---|---|---|
| 1 | **Block (local-to-global) start kept.** The backfit start is rejected for paper 1. Arm D is v2 evidence only. | Ground rules 1, 5 and 7: no irrefutable case for dropping it; it carries the S1/S2 theorems. Backfit is WORKHORSE (full re-run) with no theorem, and no exact sampler with a known normaliser was exhibited for it (why arm D was dropped), so Ẑ unbiasedness is not available. The earlier "headline gain capped at 6/2,400" rationale is withdrawn: a changed start does not nest scored sets. The backfit start is recorded as future work. | ABL-START, read under a rule committed before any arm-C or S4/S5 result was read (some A/B results were already filed; §3) | R1 (all three); R2 rule; R3-6 procedure; result §3 |
| 2 | **HPM stays the only decision rule.** MPMs of both PIPs are reported as descriptions. No HPM-vs-MPM disagreement flag. | HPM is the 0–1 Bayes rule (T07), and the finite-n spine T38(0)/N200 is about it. A disagreement flag has no provable power (ground rule 3). | PC1 claim 5: under δ₁ < ½ the HPM and top-store MPM certificates coincide (the earlier "⅓" was FALSE) | R1 (all three) |
| 3 | **LS0 in the shipped core,** after the final local search. Own provenance and `ls0_improved` flag. Does not fire E3. | Makes T38(b1-LH) a theorem about the shipped method. ADDITIVE. | O-LS0: 0/2,394 HPM changes. Wording fixed by D3c: the scored set is nested; the store is top_c(old ∪ added), not a superset | R2 D3c |
| 4 | **Parallel layer** (each item ADDITIVE / bitwise unless stated): (a) concurrent final islands; (b) concurrent diagnostic islands; (c) parallel scans with lexicographic reduction; (h) the block-table stage in parallel; process workers (threads need private counters); GUARD-W "any worker / LS0 / guard stop ⇒ no output" (an LS0 stop is an operational interruption; a completed LS0 capped at `local_limit` still returns output, with L1 = n/a); (g) estimate fields NA on unavailable output. | Real issue: the parallel orientation (ground rule 2). The axis is islands and scans, not variables (ground rule 4). | Prop W executed bitwise on smoke + **3/3** study designs (`evidence/2026-11-03_concurrency_runs.md`). W-cal is not yet executed (engineering). Mutable counters confirmed at `v3_score.h:20–21` | R1–R2 (D3e, D3f) |
| 5 | **Stacking R′ = 4k at N_e,** declared before stream 10 (streams 10..9+R′). N_e is never split. Extra local search from the R = 4 centre. Baseline and expanded records each carry their own flags and card. | Keeps stacking ADDITIVE (nested). | PC1 claim 6: without the extra search the post-search HPM is **not** monotone in R′ (COUNTEREXAMPLE). No listed theorem needs monotonicity; the extra search costs ≤ ℓ + 1 scans | R2 D3a, D3b |
| 6 | **Depth and cost are stated at the implemented (island) level.** "Free of N, H, R" is removed. Calibration is counted. C6 (per-particle streams) and C7 (Gram-free scorer) are the declared v3.2 path. C6 is implemented and law-checked iff paper 1 claims particle-parallel depth **or** demonstrates any fit with p > 2,500. This trigger is HQ's disposition: the union of the two recorded conditions (Seats A/B: any p > 2,500, R2_A:23, R2_B:21, R3_B:44; Seat C: a particle-parallel depth claim). The narrower trigger was not unanimously adopted. Felipe decided (2026-11-03) that paper 1 claims island-level depth only, and the study has p ≤ 1,000, so neither trigger currently fires. | Honest scaling claim. | Calibration took 0.45×, 0.62× and 1.76× the serial final run on S1, S5 and S4 (concurrency log). Seat A's single-tier ratio 0.0512 + 0.2048·I (rounded: 0.05 + 0.2·I) matches all three (seat-derived, unchecked) | R2 D3d, D4; C6 trigger: HQ (AMENDMENT_HQ_01) |
| 7 | **Calibration kept unchanged, with a contract:** 𝓒 frozen before final randomness; validity holds for any frozen 𝓒; Theorem G cap; ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation); restricted ESS on V only; statuses distinguished. Shortening it (C9) is rejected. | Validity does not depend on calibration converging. The missing theorems concern efficiency and delivery (theorem obligations). | T12 / Prop 2 / IND-T (recorded); concurrency log for cost | R1–R2 (all three) |
| 8 | **Ẑ-weighted PIP is primary,** equal-weight is secondary, and both MPMs and R_eff are reported. POST HOC. | The only PIP with a consistency-in-R theorem (Prop P(ii), T31(i)). Equal weighting keeps the single-island bias for every R. The truth-based gate was withdrawn: closeness to the binary truth is objective 3, not objective 1. | PC1 claim 3 (finite-R bound, given the identity). Rescoring on 3 designs: the MPMs never differ, max\|ΔPIP\| ≤ 1.3·10⁻³ (`evidence/2026-11-03_pip_rescore/`). The full 2,394-fit rescoring is an HQ reporting action (bundles on NOTS) | R2 D5 (all three) |
| 9 | **Flags E1–E3, ESS and grid flags kept** as calibration triggers (they define the law of 𝓒) and as labelled heuristics. No PSIS/R̂ flags. The certificate card never feeds back into calibration. | Removing them is WORKHORSE. Their theory is negative (V12, E1c). | — | R1 (all three) |
| 10 | **Certificate card (POST HOC):** PC2's minimal card. G1 (deterministic store bounds, including Ẑ < Z_𝒯 ⇒ Ẑ < Z); G2 (π(S) ≤ e^{F(S)}/max(Z_𝒯, 0.05Ẑ), joint with output, ≥ 95%); L1–L3 (local, subset and best-of-scored certificates); R optional (box). One declared certificate budget, with "unresolved" on exhaustion. L1 is evaluated on the returned Ŝ (after LS0). Each number carries the label "numerical implementation of an exact-arithmetic certificate" until validated arithmetic (SC) and VAL-FP exist; a long-double replay alone does not remove it. | The only diagnostics with a provable positive property (ground rule 3; HQ objection 8). | PC1 claim 2; PC2 (five of Seat C's corrections upheld in their stated forms; correction 3 concerns sharpness, not validity, and was withdrawn by C as a validity objection; "unscored mass" wording FALSE, amended to "outside the store"; `global_certified` is a heuristic) | R2 D2; R3-1 |
| 11 | **General-h estimator:** H_r(h) after each complete measured round. Ẑ-weighted and equal-weight pools are reported. The default 𝓗 is model size and pairwise inclusion on neighbour-graph edges. h must be fixed from (X, y), or from (X, y, 𝓒) before stream 10. Plain averages for joint h; Rao–Blackwellisation for marginal PIPs only. HPM terminal frequency is descriptive only. ADDITIVE. | Proposal §13.1 needs joint posterior summaries. The marginal RB product is not a joint estimate. | PC1 claim 3 (bound given the identity); the identity is a PROOF SKETCH (obligation N1) | R2 D7; R3-3 |
| 12 | **Output convention:** every estimate on the output event 𝒪 is a function of (X, y, seed, binary). The allocation and hardware decide only whether output is delivered (stop-only guard, Lemma RO). Guarantees are stated for the potential run and as P{𝒪, ·}, never conditional on completion. | Ground rule 9 (`resource_limit` vs "runnable from X, y and one seed"). | PC1 claim 2 (amended output-event form) | R2 item 9 e8 |
| 13 | **Item 9: generality in (n, p).** No setting is class (e) in the method's law. Fixes e1–e8 and wordings w1–w7 are adopted (list in §4). No separate p ≪ n / p ≫ n rule is needed. | Ground rule 9; METHODOLOGY_v3 Requirement (4). | Seat audits R2_A/B/C §4. Chair checks: J vs ⌈p/B⌉; exact branch at n ≤ 5; duplicates are kept | R2–R3-4 |

## 3. Item 1: start ablation (ABL-START)

Full record: `ITEM1_ABL_START.md`. Data: `evidence/item1_per_fit.csv` and `evidence/item1_rule_table.csv`. Rule script: `evidence/item1_scripts/apply_rule.py`, committed before any arm-C or S4/S5 result was read. Some arm-A/B results were already filed by then (arms A and B on S1 r001 c100 in `evidence/2026-11-03_pip_rescore/REPORT.md`, commit a240857; arm A's bitwise check, SYNTH_R2 §0.3). The v1 script lacked the recorded absolute gate (fewer than 9 conclusive designs ⇒ Outcome 2). HQ's corrected `evidence/item1_scripts/apply_rule_v2.py` enforces need = max(9, ⌈0.75·complete⌉) and gives the same result, Outcome 2 (`evidence/item1_scripts/HQ_NOTE_v2.md`, commit 8f6051b). v1 is kept unchanged as the committed evidence.

- **Rule.** SYNTH_R2 §2 with the R3-6 conventions (all three seats accepted). Arms: A = block start (production), B = singleton factors, C = prior start. Designs: 12 study designs at p = 500, one seed each.
- **Result: Outcome 2, keep the block start, reframed.** 33 of 36 fits completed, and 9 designs were complete for arms A, B and C. All 9 were **inconclusive** under the > 1 nat clause, because arm C's log Ẑ was 2.6 to 13.3 nats below arms A and B. Fewer than 9 conclusive designs gives Outcome 2 by the agreed convention.
  - Three arm-B fits did not finish: S4 r001 and S4 r002 were still running after more than 4 h of CPU, and S3 r001 was stopped by the chair after 3 h 06 min. Arm A took 10 to 28 min on the same designs.
- **Decision (unchanged under every outcome).** The block start ships. The paper presents it as the exactly computable local step that carries the theorems (S1/S2), with the parallel table stage, and makes **no depth or speed claim** for it.
- **Descriptive observations** (exploratory, not the pre-registered test):
  - The prior start (C) had log Ẑ below arm A's on 12/12 designs, by more than 2.5 nats on 11/12. **Certified count:** on 10/12 designs arm C's log Ẑ is below the best score found by any arm, so Ẑ < Z in exact arithmetic (every scored S gives Z ≥ e^{F(S)}); arms A and B on 0 (`evidence/item1_scripts/HQ_NOTE_v2.md`). Its island spread was larger (median about 8× arm A's), and it escalated to tier 1 on 9/12. This is consistent with the masked-crossing underestimation mechanism; unbiasedness alone does not diagnose the realised mechanism.
  - The singleton start (B) agreed with A's log Ẑ within 0.24 nats (agreement with A, not certified accuracy). It needed at least as many rebuilds as A on 9/9 designs and more wall time on 8/9.
  - All arms returned the best-known mode as the HPM (33/33).
- **What would license a depth or accuracy claim:** a confirmatory paired A-vs-B and A-vs-C test on ≤ 20 seeds, with a reference fixed in advance (not the leave-one-arm-out pool that arm C contaminates). This is an optional HQ action. It is **not an open method question**, because the decision is the same whatever it shows.

## 4. Item 9 resolutions (every class-(e) item)

| id | Setting | Resolution | Class | Study effect |
|---|---|---|---|---|
| e1 | B* = 16 labelled an "implementation limit" | Re-labelled (c): a budget for the exhaustive tables, which keeps tables polynomial in p. W7-PART's g_max ≤ B < 2g_min is a hypothesis of one theorem (B = 14 covers g ∈ 8..14; B = 16 covers 9..16). The study's g = 5 is a theorem obligation (PART-pairing), not a method defect | spec text | none (B = 14) |
| e2 | Near-tie window 10⁻⁹ nat (absolute) can fall below score noise at large n (η depends on k, Q and conditioning, not on n alone; a numerical crossing needs a specified design and model) | Keep the 10⁻⁹ list. Also print η(Ŝ) and a heuristic list at max(10⁻⁹, 2η(Ŝ)); the exact pairwise margin would be η(S) + η(Ŝ). The HPM uses exact equality and is untouched | POST HOC | none |
| e3 | Input domain n ≥ 3 | Admit n = 2 (a proposed extension: current preprocessing still rejects n < 3 and raw p = 0): K = B = 1, exact branch. All singletons tie exactly, so the output is ∅ or the smallest singleton with a p-fold tie, reported as such (R3B's statement, **seat-derived, unchecked**). Duplicates are kept (chair-checked, `v3_core.cpp:715–728`); that code check is not a proof of the n = 2 output. `degenerate_n` for n = 1; `no_predictors` for zero predictors; reject n = 0 | ADDITIVE | none |
| e4 | LS0 start-mode tie-enumeration cap of 10⁶ | Keep the fast path. On truncation, a deterministic tie-aware DP returns the prescribed smallest-size, then lexicographic, maximiser. The DP invariant is obligation N3 | ADDITIVE | none (0/2,400 truncated) |
| e5 | `global_certified` relies on a heuristic error bound | Relabelled as a heuristic numerical margin (field name kept for compatibility; documented as heuristic). "Certified" is reserved for validated arithmetic | POST HOC (interface) | none |
| e6 | Memory preflight assumes ⌈p/B⌉ blocks (the study's J is 46–60 vs 36 at p = 500, and 95–120 vs 72 at p = 1,000) and ignores per-worker memory | Use J ≤ p before setup and the actual J after it. Account shared vs per-worker memory. Label the result "estimate" | ADDITIVE (engineering) | none |
| e7 | Integer, stream and allocation arithmetic unchecked | Checked arithmetic, with explicit status `unsupported_size` | ADDITIVE (engineering) | none |
| e8 | "Seed alone" vs `resource_limit` | Allocation is (c), a declared input. Output convention as in decision 12 | spec text | none |
| w1–w7 | Spec wording | w1: neighbour threshold is √(2 log p / n), not √(log n / n). w2: "all p at n ≤ 5". w3: forced 1-NN graph fallback when p > e^{n/2}. w4: ℓ² > 1,000 exactly when n + p ≥ 2³¹. w5: the clustering cut is by size only; there is no correlation cut. w6: code comment "up to 20" → 16. w7: stream map 10..9+R′, declared before stream 10 | spec text | none |

**Class labels for the other constants.** The 2,500 and 1,000 floors, 512/2,500, R = 4, tier ×4, the 4 measured rounds, 20p and 40p+1, 500p, the exact-branch rule and the one-nat flag thresholds are (c) declared budgets, combined with their (b) formulas. The 60 halvings are (d). These values are conventions, not optima, and changing them is not automatically law-preserving.

ESS 0.90 is recorded as (c) with Seat B's caveat: "it defines the law of 𝓒 and is a hypothesis of Theorem G". Seat B preferred (a). The chair's reasons for (c): Amendment 01 reserves (a) for modelling conventions, and the other (c) budgets also enter the law of 𝓒. This is a label only; no setting changes.

## 5. Inherent limitations, and why each is inherent

Each is either PROVED impossible or true by definition (rule: SYNTH_R1 §3 as amended by the seats). Re-checked under HQ amendment 01: items that do not meet this rule were moved to the "Not inherent" list below.

1. **Per-round sequential factor m = p + B + 2.** True by definition of a random-scan full-coordinate Gibbs round: each update conditions on the previous one. This is inherent to the chosen kernel, not to SMC or BVS. Removing it (C10) is WORKHORSE and breaks the Gibbs-path theorems (T38(b2), BG3, V5).
2. **Every worker needs scoring access to all predictors** (X or sufficient statistics, 8np bytes, local or shared/distributed at a communication cost). True by definition of a full-coordinate round. A private 8p² Gram per worker is **not** inherent (C7).
3. **Masking of the product-of-blocks start built from block-local scores against the full y, under T27(i)'s hypotheses (H2, H3; verified on LH).** T27(i), PROVED-LOCKED (conditional, in its design class). This is a law for that construction and design class; it does not say that every product start is masked on every design. The bridge exists to correct it (SEP-B).
4. **No diagnostic from the observed record (the run's own weights or islands) has a universal detection guarantee for never-visited modes.** V12 and E1c PROVED; Chatterjee–Diaconis Thm 2.1. This does not rule out alerts on particular runs: positive one-sided certificates (decision 10, e.g. Ẑ < Z_𝒯) can still detect some failures.
5. **The properties of Ẑ behind the 95% bound imply no two-sided relative-error bound** (positive, finitely many values, mean Z, iid islands: some such law has P(Ẑ < c₀Z) ≥ 1 − η for any c₀ > 0, η ∈ (0, 1), so {Z ≥ αẐ} places no upper limit on Z/Ẑ) (T31(c), PROVED-LOCKED; PC2 C1(c), PROVED relative to it). This is a non-implication from the estimator's law, not a data-specific impossibility; it excludes neither structural nor record-based bounds. A finite analytic bound exists (PC1 claim 1, PROVED): Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. Its gap to Z is data-dependent; there is no universal looseness figure. The literal "no run can upper-bound Z" was FALSE, and the blanket "no useful upper bound on Z from the run's record alone" is withdrawn as an inherent limitation.
6. *(Moved by HQ amendment 01.)* Markov sharpness ("0.05Ẑ is sharp given only nonnegativity and the mean") is Seat C's argument, **seat-derived, unchecked** (not covered by PC1), so it is no longer listed as inherent; see the list below. Unchanged and PROVED: the assumption-free probabilistic lower bound max{Z_𝒯, 0.05Ẑ} keeps ≥ 95% coverage (PC1 claim 2). Sharper bounds need information beyond positivity and the mean (not necessarily a variance hypothesis).
7. **Posterior misses at n = 200** (565 strict competitor defeats of S₀ among the 2,394 completed fits, with six stops: at least 565 target-mode misses, not the exact count of global-posterior misses on all 2,400 data sets). True by definition of the fixed target: no search can make the HPM equal S₀ when F(S₀) < F(Ŝ) (N200, T07). This is a fact about these data and this prior, not a universal error rate.
8. **The cap K excludes truths with s₀ > K,** by definition of the prior. **A fixed allocation cannot support unrestricted growth of (n, p),** by definition (V13).
9. **The restricted ESS on V cannot bound mass outside V** without further assumptions, by definition of a restricted diagnostic.

**Not inherent (OPEN; must not be presented as limitations):**
- the severity of weight variance through a masked crossing on the production grid (V11);
- rebuild convergence, P(S₀ ∈ V) and P(schedule_limit) → 0;
- the as-coded masked T_n law;
- DELIV-POP;
- weak-dependence stability (proposal §5.3; a binding goal, so the escalation rule of §9 applies);
- subexponential-p theory under our prior;
- the study generator's g = 5 partition theorem;
- the measured-round identity for general h (proposal §13.1; a binding goal, so the escalation rule of §9 applies);
- Markov sharpness of the assumption-free lower bound on Z (moved from item 6: seat-derived, unchecked);
- the blanket "no useful upper bound on Z from the run's record alone" (withdrawn from item 5: "useful" is undefined and the claim is not proved; only T31(c) and PC1 claim 1 stand).

These are theorem obligations in `THEOREM_REVISION_INPUTS.md`, each with the decision it supports and what happens if the obligation fails. Where a failure would leave a binding proposal goal unmet (general h, §13.1; weight stability, §5.3; N9, §5.1), the goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change (§9).

## 6. Record of rounds and tests

| Step | Content | Files |
|---|---|---|
| Round 1 | Independent positions on agenda items 1–8 | `R1_A.md`, `R1_B.md`, `R1_C.md`, `SYNTH_R1.md` |
| Amendment 01 | Ground rule 9 and item 9 (generality in (n, p)); received after Round 1 was dispatched, so answered from Round 2 | `evidence/AMEND_01_general_np.md` |
| Concurrency | Third design p0500_S5_r002 PASSED bitwise (3/3) | `evidence/2026-11-03_concurrency_runs.md` |
| PIP rescoring | Partial: 3 designs; 2,400-fit MPM_eq vs HPM | `evidence/2026-11-03_pip_rescore/` |
| Round 2 | Rebuttals, item 9, procedural rule | `R2_A.md`, `R2_B.md`, `R2_C.md`, `SYNTH_R2.md` |
| PC1 | Proof check: Seat C's bounds, Seat B's MPM threshold, Cor W-R, A2 wording | `evidence/2026-11-03_PC1_proof_check.md` (+ scripts) |
| PC2 | Proof check: O-CERT card, minimal v3.1 card | `evidence/2026-11-03_PC2_certificate_card.md` (+ scripts) |
| Round 3 | Confirmation of the card, D6(i), D7, item-9 table, item-1 procedure; all seats "nothing else open" | `R3_A.md`, `R3_B.md`, `R3_C.md`, `SYNTH_R3.md` |
| ABL-START | HQ's API worker ended at $2.45 before results. Its Owls jobs were all SIGTERMed (rc 143, cause unrecorded) at 9/48 fits. The chair relaunched the remaining arms A–C (27 fits, 3 Owls jobs × 2 cores) with ABL-START's own scripts. The rule script was committed before any arm-C or S4/S5 result was read (some A/B results were already filed, §3); HQ's v2 script adds the absolute 9-design gate and gives the same Outcome 2 | `evidence/item1_scripts/`, §3 |

## 7. Actions handed to HQ (engineering or reporting; none is a method question)

1. **W-cal bitwise replay** on the 3 replay designs. Until it passes, "bitwise" is not claimed for (b).
2. **Merged-LS0 replay** against the O-LS0 export (HPM, stores, flags, E3).
3. **GUARD-W code audit** (worker, merge and LS0 stop paths).
4. **IND-T check** for streams 10..9+R′.
5. **VAL-FP** at production size.
6. **Preflight fixes** (e6) and **checked arithmetic** (e7).
7. **Full POST HOC PIP rescoring** over the NOTS/laptop bundles (script filed).
8. **Calibration timing tabulation** from the saved fits.
9. **Optional:** replay of the 6 `resource_limit` fits under the parallel layer, labelled operational.
10. **Paper-scope decision (made):** Felipe decided (2026-11-03) that paper 1 claims island-level depth only. C6 is implemented and law-checked (20 seeds, two stream maps) iff paper 1 claims particle-parallel depth or demonstrates any fit with p > 2,500 (decision 6, HQ's union trigger). Neither trigger currently fires.
11. **Recorded for HQ:** Seat A's reversal criterion for decision 8, to be read against the full rescoring and the ABL-START reference error. Decision 8 is POST HOC, so a trigger would mean a report to Felipe, not a re-run.
12. **ABL-START follow-up:**
    - append the two arm-B S4 fits when they finish, by re-running `evidence/item1_scripts/` with the v2 rule `apply_rule_v2.py` (reporting only);
    - optionally, the confirmatory start test (§3).
13. **ABL-START branch report:** HQ's `theory/ABL-START` REPORT.md is still a design-only draft. The results are in this meeting's `ITEM1_ABL_START.md`.

## 8. Spend

- Settlement API spend by the chair: **$0** of the $20 budget. All seats, proof checks and helpers ran on the Claude Work, Claude Personal and Codex subscriptions.
- HQ's ABL-START API run spent $2.45 (HQ budget).
- The chair's Owls use for ABL-START: 3 jobs × 2 cores from 18:06 to 18:52 UTC (killed by the T3 restart), then 3 detached jobs × 2 cores from 18:52 to about 23:00 UTC. One job ended at 22:58 UTC. Two jobs, each holding one arm-B S4 fit, are still running for HQ: wrapper PIDs 2975231 and 2975285. HQ may kill them; finished fits are kept.

## 9. Open questions

**Open method questions: none, conditional on N9** (running). If N9 fails, the method question reopens before the theorem meeting.

N9 (kernel reversibility and self-adjointness, exact start sampler; `THEOREM_REVISION_INPUTS.md` §3 N9, status words unchanged) is a **closure gate**, not an ordinary obligation. It is being checked against the code on branch `theory/N9-KERNEL`.

Apart from N9, every method question raised in Rounds 1–3 was closed in one of three ways:
- by evidence: concurrency log, PIP rescoring, ABL-START (§3);
- by a proof check: PC1, PC2;
- by acceptance of all three seats: SYNTH_R1–R3; in Round 3 all three seats answered "nothing else open".

The remaining unproved properties of the decided method are **theorem obligations** in `THEOREM_REVISION_INPUTS.md` §3 (N1–N17). Each names the decision it supports and what happens if the obligation fails. The remaining checks are **engineering or reporting actions** for HQ (§7). Neither kind changes a decision taken here, with two exceptions:
- **N9**, the closure gate above.
- **Binding proposal goals.** For every obligation whose failure would leave a binding proposal goal unmet (N1 / general h, proposal §13.1; S4 weight stability, proposal §5.3; N9, proposal §5.1): if it fails, the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change. "Descriptive summary, no theorem" is never the whole disposition.

Three items are recorded but are not open questions:
- **Seat B's class label (a) for ESS 0.90,** against the recorded (c). This is a label only; no setting changes (§4).
- **The optional confirmatory start test (§3).**
- **The C6 trigger.** Seats A/B recorded "C6 iff p > 2,500"; Seat C and SYNTH_R2 recorded "C6 iff paper 1 claims particle-parallel depth". HQ adopted the union (decision 6). Neither trigger fires for paper 1 as scoped.
