# R1 — Seat B position on v3.1 (MEET-v31)

Read-only review of the dossier, PROTOCOL, METH-AUDIT (REPORT + PROOFS), THM-INV, THM-SYNTH (THEOREM_LIST, REPORT, HQ_PLAN), API-RESID, API-AUDIT, O-LS0, S-ELS, O-CERT, O-STAGES, LIT-PAR §3.3, the study briefing (`Docs/Records/STATUS_BRIEFING_20261028/BRIEFING.md`), `METHODOLOGY_v3.md`, and the core driver (`v3_run.R`, `v3_fit.R`, `v3_calib.R`). Two small read-only computations on the per-fit CSVs in `/home/fb31/ls0_work/` (reported in §2.1 and §2.6). ABL-START has no branch yet (`origin/theory/ABL-START` does not exist), so item 1 is from current evidence only.

Status words apply to claims I make myself. "Evidence" means a file; "judgment" means my reading.

## 1. Summary

1. **Start (item 1): accept v3's block start; the irrefutable bar for dropping it is not met and is unlikely to be met.** It is the input (A₀) of two theorem groups and the only start with theorems. Backfit: reject for paper 1 (WORKHORSE, no theorem, headline gain capped at 6/2,400). What would change my mind is stated.
2. **Selection rule (item 2): accept HPM as the only decision rule; add no rule.** HPM's sufficient condition for correctness (δ₁ < ½, given S₀ scored) is weaker than any MPM variant's (δ₁ < ⅓); proof inline. Report the top-store MPM/PIP^𝒯 as POST HOC companions with a deterministic bound; no new flag.
3. **Parallel layer (item 3): accept (a)–(g) with three completions** (guard semantics under concurrency; a declared R′/stacking rule; the block-table stage as an explicitly parallel step) and one correction: LS0 is ADDITIVE but not bitwise-neutral in general. The per-round factor m = p + B + 2 is an inherent limitation of the chosen kernel, not an issue to fix.
4. **Calibration (item 4): keep as is, with a stated contract** (Theorem G cap; IND-T/frozen-run identities; escalation decided before final randomness). Its missing theorems are about efficiency and delivery, not validity.
5. **Primary PIP (item 5): refine.** Make the Ẑ-weighted PIP primary **only if** a POST HOC rescoring of all 2,400 fits shows its MPM accuracy is not below the equal-weight one; otherwise keep equal-weight primary. Both are reported either way.
6. **Flags (item 6): keep the calibration triggers unchanged** (they are part of the method's law; 208 escalations depend on them), keep E1–E3/ESS as final-run diagnostics labelled as such, and add exactly one certificate with a proved positive property (MASKZPIP C1: Ẑ < Z_𝒯 certifies underestimation).
7. **Theory fit (item 7): no v3.1 choice blocks a proposal goal.** LS0 in the shipped core is required for the R5 headline; the "R declared before final randomness" rule must enter the spec.
8. **Other real issues (item 8):** the `fit$log_Z` partial-match hazard (fix), METH-AUDIT §6 evidence is **not in the branch** although REPORT §1–§4 quote it, and "bitwise" must be scoped to one binary and BLAS.

## 2. Agenda items

### 2.1 Local-to-global versus a plain start

**Verdict: accept (keep the block start); reject backfit for paper 1.**

Argument.
- Ground rule 5 puts the burden on dropping. The evidence for dropping would have to show that a Bernoulli or prior start gives equal or better posterior accuracy at matched compute **and** no worse depth. Nothing on file shows that; nothing has measured it (ABL-START task file, "Nobody has measured what the block start buys inside the full SMC").
- What the block start demonstrably does at n = 200 is not "hold the truth" (0/2,400 favourable, median π₀(S₀) = 10^{−15.65}; API-RESID §3.1) but (i) hold a clean sub-model: median π₀(𝓡₂) = 0.81 (API-RESID §3.1), which is the eligibility premise of T38(b) (π₀(R_d) ≥ b_n, API-RESID §3.3); and (ii) set the masking depth A₀ that D2/STG-M turns into a stage count (O-STAGES §1.3; THEOREM_LIST D2(c)).
- **A computed prediction (evidence + heuristic).** From `agg_final/ls0_per_fit.csv` (2,400 fits), A₀ = log π₀(S̃₀) − log π₀(S₀) has median 33.0 nats (IQR 27.6–40.0), log₂A₀ median 5.04 (range 3.1–6.2). For a prior start the analogous depth is log ϖ(∅)/ϖ(S₀) = log C(2p−1, 14) = 71.4 nats (p = 500) and 81.2 nats (p = 1000), log₂ ≈ 6.2–6.3. On the ideal two-state law T* = log₂A₀ + 7.7 (O-STAGES §1.3, PROVED on the ideal grid), the block start saves only **about 1.2 stages** over a prior start through the crossing mechanism. **CONJECTURE (heuristic):** the block start's real depth advantage, if any, comes from the smaller spread of d(S) = log BF − Σ log r_b under the bridge (the bulk ESS mechanism), not from A₀. The study's T ≈ 22 at p = 1000 (METHODOLOGY §8.3) cannot be decomposed without the ablation.
- Theory side: dropping the start removes S1 (Thm 2), S2 (SEP + Lemma KL), the A₀ input of D2, and C1(d)'s contrast (THEOREM_LIST G4, G5). Ground rule 7 counts that against dropping, independently of the ablation.

Backfit start (D): (i) real issue: none under ground rule 2. The headline cannot move by more than 6/2,400 (API-RESID §4); depth and stability gains are unmeasured ("Step 0 cannot evaluate (b)"). (ii) Class: WORKHORSE (changes the start law; T22(iii), T27, DIL, SEP and A₀ all restate). (iii) Effect on the study: a full re-run. (iv) Proof route: none exists (API-RESID §5 "no theorem", "fixed-point convergence unproven", 90/2,400 unsettled at 10 sweeps). (v) Cheapest test if ever pursued: API-RESID §5's paired pilot (S4 p = 500 both c; S5 p = 1000 both c; the 6 stopped fits; 20 datasets per cell; harm criterion). Not for paper 1.

**What ABL-START result would change my verdict.** At matched compute on ≥ 10 paired designs: (a) if arm B or C has stage count T_final ≤ T_A + 2 **and** no worse pooled Ẑ spread and PIP error, the block start keeps its place only as the theorem-bearing default and the paper must not claim a depth advantage; (b) if arm B or C is *better* on objective 1 (smaller |log Ẑ − ref| or PIP error) on a majority of designs, that is a real issue on the first objective and I would move to "change (start = B)", classed WORKHORSE with a full re-run; (c) if T_A ≤ T_C/2 on masked designs, the start earns its place on depth and the paper may say so in O-STAGES units.

Inherent limitation: π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} under masking (T27(i), PROVED-LOCKED CONDITIONAL) and σ²-dilution at n = 200 (DIL-E, XF VERIFIED) are inherent to *any* product-of-blocks start built from block-local scores against the full y: the block cannot see a truth whose signal is cancelled or diluted outside it. This is inherent to the local step, not to the method, because the bridge corrects it (SEP-B says one-shot correction cannot).

### 2.2 Selection rule

**Verdict: accept (HPM only); refine the reporting, not the rule.**

Argument.
- HPM = "best model ever scored" is what makes the finite-n spine hold for every n: N200 / T21(C1) / T38(0) (THEOREM_LIST R4, PROVED, XF VERIFIED). The study: 0 search misses in 2,394 completed fits; all 565 misses are posterior misses (S-ELS §1, §3). So no selection rule applied to the scored set can beat HPM on these data: on every miss F(S₀) < F(Ŝ) strictly.
- Empirically the HPM beats the PIP > ½ model at c = 0.5 (370 vs 338 at p = 500; 340 vs 321 at p = 1000; BRIEFING §4.2), consistent with T07 (0–1 Bayes rule).
- **Sufficient-condition comparison (PROVED, candidate, elementary; proof here).** Let δ₁ = 1 − π(S₀). (a) If S₀ ∈ 𝒮 (scored) and δ₁ < ½, then HPM = S₀: π(S₀) > ½ ≥ π(S) for every S ≠ S₀, and HPM is the argmax of F over 𝒮 ∋ S₀. (b) For the top-store MPM^𝒯 = {j : PIP^𝒯_j > ½} with S₀ ∈ 𝒯: for j ∈ S₀, PIP^𝒯_j ≥ π(S₀)Z/Z_𝒯 ≥ 1 − δ₁; for j ∉ S₀, PIP^𝒯_j ≤ δ₁Z/Z_𝒯 ≤ δ₁/(1 − δ₁). So MPM^𝒯 = S₀ needs δ₁ < ⅓. For the sampled MPMs (equal-weight or Ẑ-weighted) one needs δ₁ plus a Monte Carlo term (A4-P1, A1). Hence the HPM's certificate is the weakest-hypothesis one. At n = 200 none bites: π(Ŝ) ≤ 0.37 on correct fits (O-CERT §1.5), i.e. δ₁ > 0.63.
- An "HPM-vs-MPM disagreement flag" has only this provable content: if π(HPM) > ½ then the true MPM equals the HPM. Since π(Ŝ) ≤ 0.37 on every illustrated fit, the flag would be uninformative at study size and has no power theorem. Do not add it (ground rule 3).
- A "certified local-search HPM" already exists: `local_certified` fired in 2,394/2,394 (S-ELS §1) and is a pure 1-flip/swap local-maximum certificate (O-CERT C3). Nothing to add.

Refinement (reporting only): report Z_𝒯 and PIP^𝒯 from the saved 40p + 1 store (A3, MASKZPIP P3, PROVED deterministic). (i) Real issue: the paper needs one two-sided evidence/PIP quantity in the masked regime (THM-INV §5.2); (ii) POST HOC; (iii) no change to any fit; (iv) A3; (v) a script over the saved top stores (`S0_in_store` is already in the S-ELS ledger, so the stores exist).

Inherent limitation: no finite run can certify "Ŝ is the global HPM" or π(Ŝ) ≥ ½ without an upper bound on Z (O-CERT §1.1, T31(c)): inherent to Monte Carlo on a 2^p space.

### 2.3 The parallel execution layer and the v3.2 path

**Verdict: accept with completions and one reclassification.**

Classification check against METH-AUDIT §4 (my reading of PROOFS.md):
- (a) concurrent final islands: ADDITIVE (bitwise) — Prop W PROVED by code reading; executed on smoke + 2 study designs (dossier §5), third running. Agree.
- (b) concurrent diagnostic islands: ADDITIVE (bitwise) — Prop W-cal PROVED by reading, **not executed**. Agree conditionally; see §5.
- (c) parallel scans with lexicographic max-reduction: ADDITIVE (bitwise if the tie rule is kept). Agree.
- (d) stacking R′ = 4k at N_e, R′ declared: ADDITIVE (nested; Cor W-R). Agree, with the extra local search from the R = 4 centre so the HPM is monotone in R′.
- (e) Ẑ-weighted PIP: POST HOC. Confirmed: `v3_run.R:128–129` saves `pip_r` and computes only `pip_primary`; `log_Z_r` is saved (`:120`). Computable on all 2,394 completed fits.
- (f) LS0: **ADDITIVE but not bitwise-neutral in general.** It is a deterministic extra scan on the shared ledger (API-AUDIT §3), so the scored set is nested and the HPM is ⪰; on the study it changed 0/2,394 HPMs with smallest margin 0.002 nats (O-LS0 §1.2). It *can* change the near-tie list and the stores (new models offered), and in principle E3 on a different design. METH-AUDIT §9 says "theorem-neutral for every row"; THM-SYNTH R5 needs it in the shipped core. Keep (f), but the paper's statement must be "HPM unchanged on 2,394/2,394; stores nested", not "bitwise".
- (g) `fit$log_Z` = NA on stopped fits: POST HOC/ADDITIVE on completed fits (they never hit the branch; API-AUDIT §2b).
- v3.2: per-particle counter-based streams LAW-PRESERVING (needs IND-T restated as "distinct (island, stage, particle) triples", METH-AUDIT §3 item 6: a one-line re-proof); Gram-free scorer LAW-PRESERVING up to fp. Agree.
- Rejections C8, C9, C10: agree. C8 is WORKHORSE in effect by Prop P(i) (equal-weight PIP bias set by N). C10 breaks the Gibbs-path theorems (T38(b2), BG3, V5).

What is missing for "scale p beyond sequential MCMC":
1. **Guard semantics under concurrency.** Lemma RO/GUARD needs "the guard checks the run's wall clock, and a stop in any worker stops the run before any output" (METH-AUDIT §3 table, row Lemma RO). That is a spec sentence, not code only; without it "a stopped fit is no output" is not a theorem about v3.1. ADDITIVE; no effect on completed fits.
2. **The declared R′ default and the N-versus-R rule** (HQ objection 7): fix "never split N_e; stack at N_e; R′ declared before stream 10 is read" in the spec (Prop P(i),(v)). ADDITIVE.
3. **The block-table stage (row 4 of METH-AUDIT §2.1)**, the one truly local stage, is serial in code and absent from (a)–(g). It is embarrassingly parallel over blocks and bitwise (independent sub-model scores). Cost is small now (2.9 s at p = 1000, METHODOLOGY §8.2) but it is the local-to-global story's own stage; add it as (h). ADDITIVE.
4. **Amdahl check (arithmetic on dossier §5 numbers).** Design p0500_S1_r001: serial 358 s, 4 workers 189 s. If only the final run parallelised, final ≈ 225 s and calibration ≈ 133 s; the cap of (a) alone is 358/133 ≈ 2.7×. p0500_S4_r001: 672 → 352 s gives final ≈ 427 s, calibration ≈ 245 s, same cap ≈ 2.7×. So (b) is on the critical path of any wall-clock claim, and the N-free depth needs C6. The paper's parallel claim therefore rests on W-cal being executed (HQ objection 5) and on C6 being at least demonstrated at one size.

Per-round depth m = p + B + 2: **inherent limitation of the single-site Gibbs kernel, to state, not to fix.** It is a definitional fact (Prop D remark; LIT-PAR §3.3 Option A). Fixing it is C10 = WORKHORSE and breaks R5(b2)/BG3/V5. The honest wall-clock reading: at p = 500, one round ≈ p·s̄ ≈ 2–3 ms (METH-AUDIT §7, **uncommitted measurement**; the study's medians, 486 s per fit over ≈ 5·10⁵ particle-rounds, give the same order). Depth = (I + 2)(T + L + 4)·m score evaluations is the statement to print (D1(c)).

Inherent limitations in this item: the per-round Θ(p) factor (kernel); every worker needs all of G or X because every Gibbs round touches every coordinate (price of targeting the exact posterior; METH-AUDIT §2.1 memory paragraph). The 8p² *bytes* are not inherent (C7).

### 2.4 Calibration

**Verdict: accept (keep as is) with a stated contract; no simplification.**

Argument.
- Validity does not depend on calibration: T12/T31 identities hold conditionally on any 𝓒 fixed before the final streams (METH-AUDIT §3 table, Prop 2 row; IND-T PROVED XF VERIFIED*). The missing theorems (rebuild convergence, P(schedule_limit), P(S₀ ∈ V), masked T_n law: THM-INV §1 row 7, §5.9) are about efficiency and delivery (R6), not about the correctness of any reported number.
- What is proved and should be the contract: Theorem G (as-coded greedy rule is optimal among grids refining the pilot points; T ≤ T_e deterministically on success; O-STAGES §1.1, API-T26BUD), the deterministic cap of ℓ rebuilds (`v3_calib.R:85–118`), escalation decided before any final randomness (METHODOLOGY §6.9), and Lemma RO.
- Study evidence: 0 `schedule_limit`, 4/2,400 `grid_unconverged`, 208/2,400 escalations, E1/E3 never fired in the final run (BRIEFING §Compute, §4.3, flagged claim T35). Calibration delivered on 2,394/2,400; the 6 failures were wall-time stops with serial islands (METH-AUDIT §9), which (a)+(b) address.
- Shortening or sharing (C9): no real issue found; touches T38(b1′) through H₀, Theorem G through P(S₀ ∈ V), and (0_H) through 𝒮_cal (METH-AUDIT §3 list item 5). WORKHORSE; reject.
- The sequential depth of calibration, (1 + I_e) island-depths, is addressed by (b) bitwise and by C6 in law; that is the right fix.

Cheapest check that would settle the "contract" wording: tabulate `rebuilds`, `converged`, tier and T from the 2,400 saved fits (fields exist: `v3_calib.R:124`). POST HOC, minutes.

Inherent limitation: the grid controls the *restricted* ESS on V only (METHODOLOGY §6.7 "Limits"); no weight-based construction can certify that a mode never scored is resolved (MASKZPIP E1c PROVED; Chatterjee–Diaconis Thm 2.1, THM-INV §4b B1). This is inherent to any diagnostic built from the sampler's own weights.

### 2.5 Which PIP is primary

**Verdict: refine, gated on one POST HOC check.**

Argument.
- Theory: the Ẑ-weighted PIP is the only one with an R-consistency theorem (T31(i), KNOWN—CITE) and the regime-free non-asymptotic bound Prop P(iii) + M1 (PROVED candidate; THEOREM_LIST V3, A1). The equal-weight PIP keeps the single-island bias b_j(N) for every R (Prop P(i)); its positive result is P1 (bias ≤ TV of the delivered population), which is conditional on delivery (A4, DELIV-POP OPEN).
- Mechanism in the two regimes: favourable, W_r ≈ 1 for all r, so the two estimators nearly coincide (little variance cost); masked, Ẑ-weighting puts the weight on islands that crossed (F-MASKPIP M2/N(a): non-crossing islands have W_r ≤ √δ₁), equal weighting averages in their wrong PIPs. So the "noisy under masking" concern (dossier item 5) is a concern about the case where the largest Ẑ_r is itself an upward outlier; P(W_r > 20) ≤ 0.05 per island by Markov. Judgment: Ẑ-weighted should be primary, but this is exactly the kind of claim ground rule 3 says to test, and the test is free.
- (i) Real issue: the primary estimator has no R-theorem (THM-INV §1 row 10, "equal-weight pooled PIP accuracy NONE"). (ii) POST HOC. (iii) No fit changes; the study's PIP-based numbers (PIP > ½ model accuracy) are rescored. (iv) Proof route: V3(ii),(iii), A1; done. (v) Cheapest test: compute both PIPs on all 2,394 completed fits from saved `log_Z_r` and `pip_r`; tabulate max_j |Δ| by cell and the MPM accuracy of each; cost minutes on the saved fits. Decision rule, declared now: Ẑ-weighted becomes primary iff its MPM accuracy is ≥ the equal-weight one overall and in no cell worse by more than 2 fits; otherwise equal-weight stays primary and the paper gives the mechanism above as the reason both are reported.

Inherent limitation: under masking E[W²|𝓒] can be exponentially large, so the R needed by Prop P(iii) can be impractical (METH-AUDIT PROOFS, Prop P caveat). That is inherent to importance weighting across a masked crossing, not to the pooling rule.

### 2.6 Flags and diagnostics

**Verdict: accept (keep), with one addition and a labelling rule; drop nothing.**

Argument.
- Calibration triggers (E1, E2, E3, forced steps, grid flags, `local_limit`) are part of the escalation *law* of the method as run: 208/2,400 fits escalated on them (BRIEFING §Calibration). Removing or changing them is a WORKHORSE change to the schedule rule and would require re-running at least those 208 fits. Keep.
- As final-run flags they have only negative theory (V12, E1c; THM-INV §1 row 13). Study ledger (`sels_ledger_per_fit.csv`, my count): E1 0/2,394, E3 0/2,394, E2 83/2,394, of which 73 among the 1,829 exact recoveries (4.0%) and 10 among the 565 posterior misses (1.8%). E2 is anti-informative about the miss, which is expected: posterior misses are errors of the posterior, not of the sampler (N200). Keep them as diagnostics, labelled "no certificate".
- Add exactly one positive item: the deterministic certificate Ẑ < Z_𝒯 ⇒ Ẑ underestimates Z (MASKZPIP C1, PROVED), with Z_𝒯 reported (A3). (i) Real issue: the paper has no flag with a proved positive property (HQ objection 8); (ii) POST HOC; (iii) none; (iv) A3/C1, PROVED (candidate); (v) a script over the saved top stores. On the 4 O-CERT fits Ẑ/Z_𝒯 = e^{0.18–0.59}, so it certifies nothing there; that is the honest finding, not a reason to omit it.
- Do not add PSIS-k̂ or R̂-type flags: no power result exists for SMC weights (THM-INV §4b B2, B3), and E1c already shows island agreement is uninformative under a blind grid.

Inherent limitation: any flag computed from the run's own weights or islands cannot detect a mode the kernel never reached (V12 PROVED, E1c PROVED, CD Thm 2.1). This is inherent to self-diagnosis; a positive power theorem can exist only under a visitation hypothesis, i.e. it is conditional by nature.

### 2.7 Theory fit

**Verdict: accept; two spec additions.**

- No v3.1 component blocks a proposal goal (THM-INV §3a). The gaps (joint inclusion §13.1; §4.4 diagnostics) are theory gaps, addressed by A1 (Theorem H) and by the negative-plus-certificate framing, not by a method change.
- **LS0 must be in the shipped core** for R5's headline (b1-LH) to be a theorem about the method (THEOREM_LIST R5(v) "Decision needed"; API-AUDIT §3 "as committed, the production core is v3 without LS0"). This is the one method-level decision the theorem list depends on. Classification as in §2.3(f).
- **"R, the stacking schedule, N_e and 𝓒 are fixed before the final streams are read"** must be a spec sentence (THEOREM_LIST G1 remark; Prop P(v)). ADDITIVE.
- Choices that *would* make the theory harder, all rejected above: dropping the start (removes S1, S2, D2's A₀, C1(d)); backfit (restates S1); C10 (breaks R5(b2), BG3, V5); splitting N_e (DELIV under a split OPEN).
- A caution for the theory, not a method change: the thesis sentence D3 as scoped in THM-SYNTH REPORT §3 rests on A1 (PROOF SKETCH), C1 (PROOF SKETCH) and the as-coded masked T_n law (OPEN). The method already supports it; the proofs do not yet.

### 2.8 Anything else

1. **`fit$log_Z` hazard** (API-AUDIT §2b): on a stopped fit `fit$log_Z` silently returns `log_Zbar0` by partial matching; the fix is not on this branch (`v3_fit.R:55–62` has no NA assignment). Real issue: a consumer can print a wrong evidence on the 6 stopped fits. POST HOC; no effect on completed fits; apply it and re-run API-AUDIT's forced-stop check (10 fits, minutes).
2. **METH-AUDIT §6 is unfilled and `results/` is not in the branch** (`git ls-tree origin/theory/METH-AUDIT` shows only REPORT.md, PROOFS.md, scripts/). REPORT §1.2 "3/3 study designs", §1.4 "2–3 ms per round", §4 C8 "measured in §6 (R = 32 × 312)" cite evidence that is not committed. THM-SYNTH D1(v) already says "check before citing". The dossier's §5 concurrency log is the actual evidence and is also not yet under `evidence/`. Real issue: a paper claim without a file. Fix: commit the logs or strike the numbers.
3. **"Bitwise" is per binary and BLAS.** O-LS0 §2 records last-bit differences between Owls and NOTS inputs. Prop W's bitwise claim holds with pinned flags (`Makevars.v3`) on one machine; state it so.
4. **V5 (kernel reversibility, self-adjoint random-order round) has no registry row** (THM-INV §5.12). It is the hypothesis of V1. Theory item, but cheap and on the critical path.

## 3. HQ's objections (§4, 1–8)

1. **Block start may contribute little.** Partly accept. At n = 200 it does not hold S₀ (0/2,400 favourable) and the A₀ accounting (§2.1) predicts only ≈ 1 stage of crossing-depth advantage over a prior start. Reject the inference "so it contributes little": its measured contribution is π₀(𝓡₂) = 0.81 (T38(b) eligibility) and its theoretical role (S1, S2, D2 input). Whether it reduces T through the bulk-spread mechanism is exactly what ABL-START measures. Position stands until that result.
2. **Backfit is far more often favourable but WORKHORSE.** Accept both halves; reject it for paper 1 (§2.1). Favourability of a start that cannot change more than 6/2,400 headline outcomes is not a real issue under ground rule 2.
3. **The two PIP rules pull in opposite directions.** Accept the description; reject that it is a dilemma. They are different estimators of the same quantity with different theorems (Prop P(i) vs (ii)–(iii)); report both, pick the primary by the declared POST HOC test (§2.5).
4. **Calibration least theorised and most sequential.** Accept the facts; reject the implied need to change it. Its theorems are about efficiency, its depth is fixed by (b) and C6 (§2.4).
5. **Concurrency evidence thin.** Accept, and sharpen: W-cal is on the critical path of the wall-clock claim (Amdahl cap ≈ 2.7× with (a) alone, §2.3), and METH-AUDIT's "3/3" is not supported by committed files (§2.8.2).
6. **LS0 must be shown additive in the production core.** Accept. The O-LS0 pairing is on a side export over regenerated data; a bitwise pairing of the merged core against the export on 10–20 study designs (HPM, stores, E3) is cheap and necessary.
7. **Default R′ and R-vs-N guidance must be fixed before final runs.** Accept; proposal: R′ = 4 for the study (no re-run), stacking only at N_e, never splitting, R′ declared in the spec and in each run's manifest before stream 10 is read; a scaling demonstration at R′ ∈ {4, 16, 64} on ≤ 10 designs if the paper shows weak scaling.
8. **Flags have no positive power result.** Accept as a fact; reject "so drop or replace": none can have one unconditionally (V12, E1c, CD 2.1). Add the one deterministic certificate (§2.6) and label the rest.

## 4. HQ's candidate inherent limitations

- **Per-round Θ(p) sequential steps:** agree, inherent to the single-site kernel (definitional; Prop D remark). Not inherent to SMC-BVS as a class (C10 exists), so state it as "of the chosen kernel, kept because the Gibbs-path theorems need it".
- **Each worker holds XᵀX (8p² bytes):** disagree as stated. Needing all of G or X is inherent (every round touches every coordinate); the 8p² footprint is not (C7 Gram-free scorer, LAW-PRESERVING up to fp). State the former, not the latter.
- **SMC weight variance through a masked crossing:** agree, inherent to importance weighting from a start that misses S₀ (SEP-B and Chatterjee–Diaconis give the one-shot cost p^c n^{c/2}; the bridge spreads it but a crossing absent from V is a one-shot). Conditional on the crossing pair being in V it is the V11 CONJECTURE, i.e. merely unproved there.
- **No run can upper-bound Z:** agree, inherent to the output (T31(c); O-CERT §1.1). A reverse-direction bound would need exact posterior draws, which the method does not have.
- **Markov-only Ẑ lower bound:** agree in the assumption-free sense (unbiased + nonnegative admits nothing sharper, for any R); merely unproved under a second-moment hypothesis (PW2/Cantelli, O-CERT Thm C2). State as "sharper only under a variance bound".
- **Weight-based diagnostics can certify too early:** agree, inherent (CD Thm 2.1; V12; E1c).
- **At n = 200 the posterior often misses S₀ (565/2,400):** agree, inherent to the problem and the fixed prior (T07: no size-only prior repairs a same-size swap; Felipe's model is fixed). The 541 misses within 𝓡₂ at median gap −1.33 nats (S-ELS §4) are statistics, not the sampler.

## 5. Open questions to close before theory proving starts

1. **ABL-START result** (arms A/B/C, ≤ 20 fits): closes item 1 and HQ objection 1 by the rule in §2.1. Already running.
2. **W-cal bitwise replay** of `v3_calibrate` on 3 designs (METH-AUDIT §4 C2, ≈ 1 h on Owls): closes layer part (b); if it fails, (b) is downgraded to LAW-PRESERVING and the wall-clock claim is capped at ≈ 2.7×.
3. **Third concurrency design (p0500_S5_r002) + an independent code check** of scorer statelessness and ledger write-only (METH-AUDIT §8.1; API-AUDIT style, cheap): closes Prop W's executed status.
4. **LS0 merged into `cpp/v3_core.cpp` and paired bitwise** against the O-LS0 export on 10–20 study designs (HPM, stores, E3): closes HQ objection 6 and R5's headline.
5. **Post hoc PIP rescoring** of all 2,394 completed fits (both PIPs, MPM accuracy of each): closes item 5 by the declared rule.
6. **Post hoc Z_𝒯 / PIP^𝒯 / C1 certificate** on the saved stores: closes items 2 and 6's addition and gives the paper its one two-sided masked quantity.
7. **Spec edits (no runs):** guard semantics under concurrency; "R′, stacking, N_e, 𝓒 declared before stream 10"; never split N_e; block tables as the explicit parallel local stage; LS0 as part of the method. Closes items 3 and 7.
8. **Commit or strike METH-AUDIT §6 numbers**; move the dossier's concurrency log under `evidence/`; scope "bitwise" to one binary/BLAS. Closes §2.8.2–3.
9. **Apply the `fit$log_Z` NA fix** and re-run API-AUDIT's forced-stop table (10 fits). Closes §2.8.1.
10. **Tabulate calibration statistics** (rebuilds, converged, tier, T, T_pil) from the 2,400 saved fits: gives item 4's contract its numbers and feeds D2's as-coded T_n evidence.
11. **V5 registry row** (each move γ_φ-reversible; random-order round self-adjoint): hypothesis of V1; one page.

Everything above except 1–3 is a decision or a post hoc computation on saved fits; nothing requires re-running the study, consistent with ground rule 8.
