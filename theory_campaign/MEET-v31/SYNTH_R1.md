# MEET-v31 · Chair synthesis of Round 1

Chair (Opus 5.5, non-voting). Inputs: `R1_A.md` (Seat A, Fable 5.1, Claude Personal), `R1_B.md` (Seat B, Fable 5.1, Claude Work), `R1_C.md` (Seat C, gpt-6-astra, Codex). The seats wrote independently. Below, "agree" means all three seats; a seat's opinion is not evidence; facts the chair checked are marked **[chair-checked]** with the source.

## 0. New facts since the dossier (chair-checked)

1. **Third concurrency design PASS.** p0500_S5_r002: serial final 413.3 s, R = 4 workers 219.4 s wall, bitwise log Ẑ, PIP and HPM identical; R = 32 × 312 max ΔPIP 5e-4 (eq) / 7e-4 (Ẑ-w). So Prop W is executed bitwise on smoke + **3/3** study designs. File: `evidence/2026-11-03_concurrency_runs.md` (verbatim copy of the METH-AUDIT `results/run_owls.log`). W-cal is still not executed. The final-run speed-up is ≈ 1.9× with 4 workers (sum of island times ≈ serial time), so the log is consistent with only 2 cores in use (Owls `-j 2`); it is not a 4-core speed-up measurement.
2. **Calibration wall time can exceed the final run.** Same log: calibration 161.6 s / 1,184.5 s / 258.1 s versus serial final run 358.2 / 671.8 / 413.3 s (S1, S4, S5). On the masked design S4 (8 rebuilds, T = 34) calibration took **1.8× the serial final run**. This bears on item 4 (Seat A's "most sequential in structure, false in cost" is contradicted on S4; Seats B and C's Amdahl point is supported).
3. **ABL-START arm construction (Seat C's audit question).** `origin/theory/ABL-START:theory_campaign/ABL-START/REPORT.md` (draft, design section fixed before results): every arm keeps the production kernel B (m = p + B + 2) and the production neighbour graph; only π₀ changes (stage-0 draws, the independence move, γ₀). Arm B = singleton factors × capped size prior (correctly described by Seat C as "not independent Bernoulli"); arm C = capped prior; arm D = backfit tables on production blocks, exact normaliser. Designs: 12 at p = 500 (S1–S6 × {c100 r001, c050 r002}) × 1 seed. Reference: leave-one-arm-out pooled Ẑ-weighted. Arm A is checked bitwise against production on a synthetic design. Status: running (first fits in progress, ~17:50 UTC).
4. **Mutable counters in `Data` (Seat C).** Confirmed: `Scripts/SMC_BVS/core/cpp/v3_score.h:20–21` declares `mutable uint64_t routes[3]`, `q_recomputed_count`, `numerical_failures`, incremented in `score()` (`:231–236`). A shared `Data` under C++ threads is a data race on these counters (diagnostic counters only; scores are not affected, but the race is undefined behaviour in C++). Process-level workers (as in the METH-AUDIT harness) are not affected.
5. **Item 5 post-hoc test commissioned by the chair.** A helper (Opus, Claude Work, read-only) is recomputing equal-weight and Ẑ-weighted PIPs and their MPMs on the saved study fits, if the per-island `pip_r`, `log_Z_r` are available locally. Result to be filed in `evidence/` before Round 2 closes.

## 1. Per item: agreement and disagreement

### Item 1 — Local-to-global vs plain start
**Agree:** keep the block start for v3.1 pending ABL-START; the bar to drop it (ground rule 5) is not met by current evidence; the backfit start is rejected for paper 1 (WORKHORSE, full re-run, no theorem; headline gain capped at 6/2,400 by API-RESID §4); any start replacement is WORKHORSE. All three note that HPM counts at n = 200 cannot discriminate the arms (0 search misses), so the decision statistics are depth (T, rebuilds, calibration cost) and Ẑ / PIP error against a reference. All three say the masking of a product start (T27(i)) is inherent to the local step, not to the method.
**Differences:** the decision thresholds differ (A: ≥ 15/20 designs; B: T_B,C ≤ T_A + 2 ⇒ "no depth claim", majority better on objective 1 ⇒ change; C: "material" total critical-path dominance with matched accuracy, no concentrated loss in S4/S5). A and B both compute that the ideal two-state law predicts only ≈ 1–1.2 stages of saving from A₀ (36 vs ≈ 66–81 nats), so any measured advantage must come from elsewhere (B: the bulk spread of d(S)).

### Item 2 — Selection rule
**Agree:** HPM stays the only decision rule; no HPM-vs-MPM disagreement flag as a rule (no provable power; uninformative at π(Ŝ) ≤ 0.37); MPM reported for each named PIP (POST HOC); LS0 included (ADDITIVE); `local_certified` is a 1-flip/swap local certificate only.
**Additions proposed:** A: O-CERT card + MASKZPIP C1 (POST HOC); B: Z_𝒯 and PIP^𝒯 from the 40p+1 store (POST HOC) and a PROVED-candidate comparison (HPM correct when δ₁ < ½ and S₀ scored; top-store MPM needs δ₁ < ⅓); C: the certificate must attach to the returned model after LS0/stacking.

### Item 3 — Parallel layer (a)–(g), v3.2, depth factor
**Agree:** adopt (a)–(g); (a)–(c) ADDITIVE bitwise, (d) ADDITIVE nested, (e) POST HOC, (f) ADDITIVE, (g) interface fix; v3.2 path (C6 LAW-PRESERVING, C7) declared; C8, C9, C10 rejected; GUARD semantics under workers must be written into the spec ("any worker stop ⇒ no output"); R′ default 4, R′ = 4k optional, declared before final randomness, never split N_e; W-cal must be executed before "bitwise" is claimed for (b). The per-round factor m = p + B + 2 is inherent **to the chosen kernel** (not to SMC or BVS) and is stated, not fixed.
**Disagreements:** see table rows D3a–D3f.

### Item 4 — Calibration
**Agree:** keep the rule and budgets; write a contract (𝓒 frozen before final randomness; validity conditional on any frozen 𝓒; Theorem G cap; ≤ ℓ rebuilds; restricted ESS on V only; statuses distinguished); C9 rejected (WORKHORSE); rebuild convergence, P(schedule_limit), P(S₀ ∈ V) are **OPEN, not inherent** (all three); POST HOC tabulation of rebuilds / tier / T / converged from saved fits.
**Disagreement:** D4 (is calibration a cost bottleneck?) — chair fact 0.2 is relevant.

### Item 5 — Primary PIP
**Agree:** both PIPs and both MPMs are reported; the change is POST HOC with no re-run; the Ẑ-weighted PIP is the only one consistent in R (Prop P(ii), T31(i)); equal-weight keeps the single-island bias for every R (Prop P(i)); finite-R precision under masking is OPEN.
**Disagreement:** D5 (unconditional switch vs gated switch, and the gate's criterion).

### Item 6 — Flags
**Agree:** keep E1–E3, ESS and grid flags as calibration triggers (they define the law of 𝓒; removing them is WORKHORSE) and as labelled heuristics ("no certificate"); add the deterministic certificate Ẑ < Z_𝒯 ⇒ Ẑ underestimates Z (MASKZPIP C1, PROVED, POST HOC); no PSIS-k̂ / R̂ flags; the new certificate must not feed back into calibration.
**Difference:** A also adds the O-CERT card (P(card item false) ≤ 0.05); B and C did not discuss it. C requires a rigorous floating-point margin or the label "numerical implementation of an exact-arithmetic certificate".

### Item 7 — Theory fit
**Agree:** no v3.1 choice blocks a proposal goal outright; LS0 must be in the shipped core for R5's headline; "R′, stacking, N_e, 𝓒 declared before the final streams" must be a spec sentence; the rejected options (drop start, backfit, C10, split N_e) would each make the theory harder.
**Disagreement:** D7 (C: the method needs a defined estimator for general bounded h / joint inclusion summaries, and the theorem list overstates A2, D-laws, retention, LH scope; A and B accept the list's fit).

### Item 8 — Other
**Agree:** `fit$log_Z` partial-match hazard is real (API-AUDIT §2b COUNTEREXAMPLE) and must be fixed with explicit NA fields; METH-AUDIT §6 numbers must be committed or struck (now partly answered by chair fact 0.1).
**Proposed additions (single seat):** B: "bitwise" scoped to one binary + BLAS; B: V5 registry row (kernel reversibility); A: VAL-FP replay at p = 500; A: re-run the 6 resource_limit fits under the parallel layer; C: the coverage statement must be on the output event, P{𝒪, 0.05Ẑ > Z} ≤ 0.05, not conditional on completion; C: numerical vs exact certificates distinguished.

### Item 9 — Generality in (n, p) (Amendment 01, received after Round 1 dispatch)
Not answered in Round 1. Added to Round 2 for all seats (`evidence/AMEND_01_general_np.md`).

## 2. Disagreement table

| # | Item | Positions | Crux | Settled by |
|---|---|---|---|---|
| D1 | 1: decision rule for ABL-START | A: keep unless B/C ≤ A on T and rebuilds on ≥ 15/20 with no worse Ẑ/PIP error (then "keep but reframe"); B: if B/C better on objective 1 on a majority ⇒ change to start B (WORKHORSE); C: needs material total-critical-path dominance at matched accuracy, no S4/S5 loss | Whether a measured *non*-advantage of the block start would justify dropping it (B) or only reframing it (A, C: theorem yield, ground rules 5 and 7) | **Test** (ABL-START, running) + Round 2 agreement on the rule *before* the result is read |
| D2 | 2/6: O-CERT card in v3.1 output | A: add; B, C: silent | Is the card's PROVED-candidate status enough for v3.1 output? | Round 2 positions; **proof check** if adopted |
| D3a | 3(d): extra local search from the R = 4 centre when R′ > 4 | A: drop (no theorem uses HPM monotone in R′); B, C: keep (greedy search is not monotone; keeps the old post-search HPM) | Does any shipped claim need "HPM(R′) ⪰ HPM(4)" after local search? | **Proof check** of Cor W-R against the claims that use it |
| D3b | 3(d): flags when R′ > 4 | A: flags over all R′ islands; C: keep baseline (islands 1–4) and expanded diagnostics separate; B: not addressed | Bitwise-baseline claim vs more data for heuristics | Round 2 (spec choice; no test needed) |
| D3c | 3(f): LS0 "bitwise-neutral" | A: placed after the final local search, the study path stays bitwise and LS0 only adds scored models; B, C: ADDITIVE but stores, near-tie list, E3 and certificates can change; claim only "HPM unchanged 2,394/2,394; stores nested" | Wording of the claim | **Test**: merged-core LS0 replay on the 3 replay designs (all seats propose it) |
| D3d | 3: scope of "scale p" claims and C6 | A: C6 must be implemented and law-checked iff the paper shows p > 2,500; B: C6 demonstrated at one size; C: state implemented-level depth (N_e·m with islands only), drop "free of N, H, R", count setup/clustering/reductions | What the paper claims at which execution level | Round 2 + **HQ/Felipe decision** on the paper's p range |
| D3e | 3: extra parallel steps | B: block-table stage as (h) (parallel over blocks, bitwise); A, C: clustering O(p²)–O(p³) and neighbour graph / grid bisection must enter the large-p roadmap (C11) | Completeness only; no one objects | Round 2 (spec) |
| D3f | 3: thread-safety | C: shared `Data` has mutable counters (chair confirmed, fact 0.4) | Process vs thread workers | Spec: process workers or per-worker counters merged deterministically |
| D4 | 4: is calibration a cost bottleneck? | A: no (H₀ = 512 ≪ N₀); B: yes on the critical path (Amdahl cap ≈ 2.7× with (a) only); C: empirical question | Measured share of calibration in wall time | **Evidence**: chair fact 0.2 (S4: calibration 1,184 s vs final 672 s). Rule stays either way (all agree); only the paper's wording and W-cal's priority are affected |
| D5 | 5: primary PIP | A, C: switch to Ẑ-weighted now (POST HOC); B: switch only if the post hoc MPM accuracy (vs truth) is not worse overall nor in any cell by > 2 fits | The criterion: C says closeness to the binary truth is not posterior-PIP accuracy and the comparison should be against a posterior reference (ABL-START subset) | **Test**: chair's post hoc rescoring (running) + ABL-START's reference-based PIP error; Round 2 agreement on the criterion |
| D6 | inherent limitations | (i) XᵀX memory: A inherent; B, C not inherent (C7; but needing all of X is inherent, B). (ii) "No run can upper-bound Z": A, B inherent; C refutes literally with an analytic bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} (PROVED by C, unchecked) and restates it as "no useful tight bound from the run alone". (iii) Markov-only lower bound: A merely unproved; B inherent assumption-free; C refutes literally via max{Z_𝒯, 0.05Ẑ}. (iv) Masked weight variance: A, B inherent; C a failure mechanism, severity OPEN | Exact wording of each limitation | **Proof check** of C's Z upper bound and max{Z_𝒯, 0.05Ẑ} coverage (cheap); then wording in Round 2 |
| D7 | 7: method outputs for theory | C: define the estimator of E_π[h] for general bounded h and joint indicators (fixed measured-round particle averages; ADDITIVE); finite-R bound P(\|μ̂−μ\|>ε) ≤ 4(M−1)/R + 4M/(Rε²) (PROVED by C); A2 "fails only downward" literally false; §5.3 not yet met; LH results do not cover the study generator. A, B: theory fits | Is a joint-summary accumulator a method requirement (proposal §13.1) or a theorem-meeting matter? | Round 2; **proof check** of C's bound if adopted |
| D8 | 8: 6 resource_limit fits | A: re-run under the parallel layer (removes the only measured P(U) mass); C: may be revisited for operational rescue, cannot establish a delivery theorem | Value of the re-run | Round 2 (HQ resource decision; not a method question) |

## 3. Chair's procedural note for Round 2 (for the seats to accept or contest)

Seat C warns against "relabelling missing proofs as inherent limitations". The chair proposes this distinction for closing the meeting: a **method question** is closed when the method decision no longer depends on it (by evidence, a proof check, or because every plausible answer leaves the decision unchanged); an unproved *property* of the decided method (e.g. rebuild convergence, P(schedule_limit), masked weight variance bounds) is then **not** an open method question but a **theorem obligation**, listed in `THEOREM_REVISION_INPUTS.md` with status OPEN; an **inherent limitation** is only a statement that is PROVED impossible or follows by definition from the SMC structure, the prior, or the problem (e.g. T27(i) masking of any product start; no flag computed from the run's weights can detect a never-visited mode, E1c/V12; the posterior misses at n = 200). Round 2 seats are asked to accept or amend this rule.

## 4. Round 2 agenda

Every seat (fresh task): concede or hold on D1–D8 (naming the evidence that would change its mind), answer item 9 (generality in (n, p), Amendment 01) in full, react to chair facts 0.1–0.5, accept or amend §3, and fold in ABL-START if its report is final.
