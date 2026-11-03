# MEET-v31 · Round 1 · Seat A position

Seat A (Claude Personal, Fable 5.1). Read-only. Evidence cited as `path` or `branch:path` with section. "Judgment" marks claims that rest on my reading, not on a file. Status words per `theory_campaign/PROTOCOL.md`; nothing here is a new proof.

## 1. Summary

1. **Start (L2G):** keep, pending ABL-START. Current evidence says the block start cannot change accuracy at study size (0 search misses), so its value is depth, the local table stage, and the S1/S2 theorems. The ABL-START result that would change my verdict is named in §2.1. Backfit: reject for v1 (no theorem, WORKHORSE, caps gain at 6/2,400).
2. **Selection rule:** accept HPM primary. Add only what is POST HOC and PROVED: MPM from the primary PIP (already in spec), the O-CERT certificate card and the C1 underestimation certificate. No disagreement flag as a rule.
3. **Parallel layer (a)–(g):** accept, with four refinements: GUARD semantics under workers written down; flags defined over all R′ islands; the Cor W-R extra local search dropped as unnecessary; W-cal executed before any bitwise claim. The depth factor m = p+B+2 is an inherent limitation of the kernel, stated, not fixed.
4. **Calibration:** keep as is with a stated contract (frozen 𝓒, Theorem G cap, ℓ-capped rebuilds, P(U) reported as frequency). No change.
5. **Primary PIP:** change to Ẑ-weighted (POST HOC, no re-run). It is the only PIP with a regime-free theorem (Prop P(iii), M1) and it down-weights only islands whose Ẑ_r is a gross underestimate (M2).
6. **Flags:** keep E1–E3 and ESS as calibration triggers (part of the law of 𝓒) and as reported heuristics; add the two deterministic PROVED certificates (MASKZPIP C1; O-CERT card). Drop nothing.
7. **Theory fit:** no method choice blocks a proposal goal; the one choice that makes theory harder is equal-weight PIP as primary (item 5). LS0 must be in the shipped method for T38(b1) to be about it.
8. **Else:** re-run the 6 `resource_limit` fits under PEL; VAL-FP replay at p = 500 (2 fits); fill METH-AUDIT §6 before any measured parallel sentence.

## 2. Agenda items

### 2.1 Local-to-global versus a plain start

**Verdict: keep (accept), conditional on ABL-START; "keep but reframe" if ABL-START shows no depth gain.**

Argument.
- *Accuracy is not the question at study size.* All 565 misses are posterior misses with F(S₀) < F(Ŝ) strictly; 0 search misses; S₀ scored in 2,394/2,394 completed fits (`theory/S-ELS:theory_campaign/S-ELS/REPORT.md` §1, §3). The posterior does not depend on the start, so no start can change the HPM in those fits; the only movable fits are the 6 stops (`theory/API-RESID:…/REPORT.md` §4). So any start comparison on HPM accuracy at n = 200 is a wash by construction. The ablation must be judged on depth and Ẑ/PIP error, not on recovery counts.
- *What the block start is, in evidence.* Median π₀(S₀) = 10^−15.65, favourable in 0/2,400 at the 10⁻⁴ criterion, but π₀(𝓡₂) = 0.81 and the median start mode is 4 truths + 0 extras (API-RESID §2 table, §3.1). It is "never wrong, half right". A prior start under BB(1,p) with cap 100 has π₀(S₀) = 1/(101·C(p,14)) ≈ 10^−28.8 (p = 500) and 10^−33 (p = 1000) (elementary computation, this seat), i.e. 13–17 decades worse, and essentially no mass in 𝓡₂.
- *Depth, theory.* On the ideal two-state grid T* = log₂A₀ + 7.7 ± 0.4 (`theory/O-STAGES:…/REPORT.md` §1.3; STG-M PROVED, XF VERIFIED*). With A₀ ≈ 36 nats (block, median) versus ≈ 66–76 nats (prior), that idealisation predicts T* ≈ 13 versus 14: **almost no depth gain**. I flag this honestly: the two-state model is the wrong model for a prior start (a dense size distribution is an entropy barrier, not a two-state crossing), so the real T under arm C is unknown and is exactly what ABL-START measures. Judgment: I expect arm C to need materially more stages and rebuilds, but I have no file that shows it.
- *The part that is not measurable by ablation.* The tables are the one stage that needs only X_{C_b} and y, embarrassingly parallel over blocks (`theory/METH-AUDIT:…/REPORT.md` §2.1 row 4); every table score counts for the HPM (`Docs/Methodology/METHODOLOGY_v3.md` §6.3); and the paper's "strongest novelty claim" (T27(i), DIL-E, SEP-A/B; `theory/THM-INV:…/REPORT.md` §2 Thm 2 row; THM-SYNTH S1/S2) is a theorem *about this start*. Dropping it drops G4 of the theorem list. That is an argument from theory yield, which ground rule 7 allows, not an irrefutable computational one.

**ABL-START result that changes my verdict.** If, on ≥ 15 of 20 paired designs, arm B or C has final-grid T and rebuild count ≤ arm A's, with log Ẑ_r island spread and PIP error (against the stacked reference) not worse, then the block start has no measurable computational value at study size and the verdict becomes "keep but reframe": the start is the exactly computable composite merge that the paper corrects, justified by S1/S2, not by speed. Dropping it would still fail ground rule 5's bar, because the theorems about it are the paper's novelty. Conversely, if arm A has ≥ 30% fewer stages on ≥ 15/20 designs, "keep" is settled on evidence.

**Backfit start (API-RESID).** Reject for v1. (i) Real issue: none under ground rule 2; the favourable-regime theorems do not break, they are vacuous at n = 200, which is a wish, not a defect. (ii) Class: WORKHORSE (changes γ₀ and d, hence the bridge and every fit's law). (iii) Study: full re-run. (iv) Proof route: none; the sweep iteration's fixed point is unproven (90/2,400 unsettled at 10 sweeps, API-RESID §3.4), T22(iii)/T27 would need restating. (v) Cheapest test if ever revisited: API-RESID §5's paired pilot (4 cells × 20 datasets + the 6 stops). Note for the chair: it *is* exactly sampleable with a known normaliser (product tables of any positive entries convolve exactly), so ABL-START arm D is feasible; that does not change the verdict.

**Inherent limitation in this item:** none. π₀(S₀) = p^−c n^−c/2 e^{O_P(1)} under masking is a property of any product-form start on a cancelling design (T27(i) PROVED-LOCKED), so "the start is masked" is inherent to local-to-global, and the paper should say so; the bridge exists for that reason (S2).

### 2.2 Selection rule

**Verdict: accept HPM as primary; add POST HOC certificates only.**

- HPM is the 0–1 Bayes rule (T07 PROVED-LOCKED), the composition P(𝒪 ∩ {Ŝ ≠ S₀}) ≤ 2E₀δ₁ + D_n is exact at every n (T38(0) PROVED, XF VERIFIED; N200 PROVED), and the data show D_n = 0/2,394 and E3 = 0 (S-ELS §1, §3). The reported HPM is as accurate as the posterior allows. Nothing to fix.
- *MPM from the primary PIP*: already in the spec (§6.11), POST HOC, Hamming-optimal under the exact posterior (T07). Keep reporting it. Its theorem is Theorem H / P1 (THM-SYNTH A1, A4), which is the item-5 question.
- *Certified local-search HPM*: already shipped (`local_certified` = TRUE in 2,394/2,394). Its meaning is only "no improving flip/swap neighbour" (THM-INV §1 row 12). Keep; do not oversell.
- *HPM-vs-MPM disagreement flag*: do not add as a rule. Under ground rule 3 it needs a provable property; the only clean one is that for the *exact* posterior π(S₀) > ½ forces HPM = MPM (Barbieri–Berger, cited), which the estimated quantities do not inherit. It would be one more heuristic flag (item 6). Report both decisions and let the reader compare.
- *What to add*: the O-CERT card (`theory/O-CERT:…/REPORT.md` §1 items 2–4: exact relative certificates on scored regions, box certificate, P(card false) ≤ 0.05 at every n; PROVED candidate) and MASKZPIP C1 (Ẑ < Z_𝒯 certifies underestimation; PROVED, deterministic). Both are POST HOC from the saved top store and Ẑ; effect on study: rescoring only; proof route: done (candidates needing review); cheapest check: run on the 4 O-CERT fits plus 10 more.

Inherent limitation: π(S₀) ≤ 0.37 even on correct fits at n = 200 (O-CERT §1.5), and a lower bound on π(Ŝ) needs an upper bound on Z, which no run gives (T31(c)). Inherent to finite sampling of a finite space, not to v3.1.

### 2.3 Parallel execution layer and v3.2 path

**Verdict: accept (a)–(g) with refinements; classification correct; two things missing for "scale p".**

Per part (class per METH-AUDIT §4):
- (a) Concurrent final islands: ADDITIVE (bitwise). Prop W PROVED by code reading (`theory/METH-AUDIT:…/PROOFS.md`), executed PASS on smoke + 2 study designs (DOSSIER §5), third running. Refinement: **GUARD under workers must be specified**: the guard reads the run's wall clock, and a stop in any worker voids the whole fit before output; otherwise Lemma RO's "stopped fit is no output" fails (METH-AUDIT §3 row Lemma RO; THM-SYNTH V4). Needs the independent code check METH-AUDIT §8.1 asks for (cheap).
- (b) Concurrent diagnostic islands: ADDITIVE (bitwise) but **W-cal is code reading only** (PROOFS.md). Must be executed before the paper says "bitwise" (3 designs, ~1 h Owls, METH-AUDIT §4 C2).
- (c) Parallel scans: ADDITIVE if the lexicographic tie rule is kept in the reduction (API-AUDIT §4 for the serial rule). Bitwise path comparison settles it.
- (d) Stacking R′ = 4k at N_e, declared in advance: ADDITIVE (nested; Cor W-R). Two refinements. First, **flags over all R′ islands**: E1 and E2 are defined by "some island" and "SD over islands" (`Scripts/SMC_BVS/core/v3_calib.R:101–102`); R′ = 4 recovers v3's flags exactly, no theorem depends on them, and more islands give the heuristics more data. Second, **drop the extra local search from the R = 4 centre**: T38(0) needs the scored set nested (it is), not the post-search HPM monotone in R′; the extra search is bookkeeping for a property no theorem uses (judgment).
- (e) Ẑ-weighted PIP: POST HOC. Confirmed absent from the core: `v3_run.R:126–130` assembles only `pip_r`, `pip_primary`, `mpm`. See item 5.
- (f) LS0: ADDITIVE. It reads no uniforms and runs after the islands on the same ledger and cache (API-AUDIT §3), so the export's computation is exactly what a merged core does; 0/2,394 HPM changes (`theory/O-LS0:…/REPORT.md` §1.2), cost 0.17–0.37 s (§1.5). Place it where the export placed it, after the final local search, so the study path stays bitwise and LS0 only adds scored models. Proof route: T38(b1-LH) PROVED (candidate), XF VERIFIED, becomes about the shipped method.
- (g) `fit$log_Z` = NA on stops: engineering fix of a real hazard (API-AUDIT §2b). Accept.
- v3.2: per-particle streams (LAW-PRESERVING) and Gram-free scorer: accept as declared.

**Missing for "scale p beyond sequential MCMC" (ground rule 4).** With island-level parallelism only, depth is ∝ N_e = max(2500, n, p) and grows like p²·T for p > 2,500 (METH-AUDIT §7). So if the paper demonstrates any p > 2,500, **C6 is not optional**: it must be implemented (as a flag, serial map default) and law-checked (20 seeds × 2 maps, 2 designs, compare log Ẑ and PIP distributions). If the paper stays at p ≤ 1,000 plus R-scaling, C6 stays declared. HQ should decide which. Also missing from the list: the grid construction (≤ 60|V|T_e log-sum-exps, |V| ≤ 40p+1; `METHODOLOGY_v3.md` §6.7) is scalar-sequential in the bisection and must be parallel over V at p ≳ 10⁴; and the clustering is O(p²)–O(p³) sequential (C11). Both are ADDITIVE if exact.

**Depth factor m = p+B+2: inherent limitation, state it.** A random-order Gibbs round over p coordinates is sequential by definition; removing it is C10, WORKHORSE, and breaks the Gibbs-path theorems (METH-AUDIT §4 C10, §7). It is inherent to v3.1's kernel, not to SMC. In wall time it is not what blocks scaling: with C6, depth ≈ (I+2)(T+L+4)·m·s̄ ≈ 50 s at p = 10⁴ and ≈ 25 min at p = 10⁵ (this seat's arithmetic from Prop D with s̄ = 20–60 µs). What blocks scaling first is per-worker memory 8p² (§4 below) and width.

### 2.4 Calibration

**Verdict: accept (keep as is) with a stated contract.**

- Validity needs nothing from calibration: every identity is conditional on a 𝓒 fixed before the final streams, for *any* 𝓒 (T12, Prop P(v); METH-AUDIT §3 row Prop 2). So "no convergence theorem" is not a theorem breaking down (ground rule 2).
- What is PROVED about it as coded: Theorem G, T = N^pil + k^bis with k^bis ≤ ⌈log₂(1/η_n)⌉ when S₀ ∈ V, and T ≤ T_e always (`theory/API-T26BUD:…/REPORT.md` §1); greedy optimality (O-STAGES Theorem G); the rebuild loop is capped at ℓ iterations (`v3_calib.R:85`); Prop W-cal makes the 4 diagnostic islands concurrent.
- Depth is small once (b) is in: H₀ = 512 against N₀ = 2,500 (`METHODOLOGY_v3.md` §3), so calibration depth is (1+I_e)·512·(T+L+4)·m versus 2,500·(T+L+4)·m for the final run; at I_e ≤ 3 it is below the final run. Judgment: "most sequential part" is true in structure (I_e sequential rebuilds), false in cost.
- Study facts: escalation in 208/2,400, `grid_unconverged` in 4/2,400 (`Docs/Records/STATUS_BRIEFING_20261028/BRIEFING.md` lines 107, 384); the flags E1–E3 are the *triggers*, so they are part of the law of 𝓒 and cannot be dropped without changing the method (WORKHORSE).
- Contract to print: 𝓒 frozen before final randomness; T ≤ T_e deterministic, Theorem G when S₀ ∈ V; ≤ ℓ rebuilds; P(schedule_limit), P(grid_unconverged) reported as frequencies (R6 limitation, THM-SYNTH R6).
- Simplify or change: no. C9 touches T38(b1′) (H₀), Theorem G (S₀ ∈ V) and (0_H) (METH-AUDIT §3 list item 5) and would re-run the study.

Inherent: no. Rebuild convergence and P(S₀ ∈ V) are OPEN (THM-INV §5.9), not inherent; Theorem G(iii) under a COVER(V) condition is the route (v2 HQ-STAGES-2).

### 2.5 Which PIP is primary

**Verdict: change. Primary := Ẑ-weighted; equal-weight reported alongside; MPM from the primary.**

(i) Real issue: HQ objection 3 is real and is a *theorem* issue: the equal-weight PIP keeps the single-island bias for every R (Prop P(i) PROVED, candidate) and its masked-regime accuracy needs DELIV-POP, OPEN, v2 (THM-SYNTH A4). The Ẑ-weighted PIP has a regime-free non-asymptotic bound (Prop P(iii) with M1, XF VERIFIED) and is consistent in R (T31(i), KNOWN—CITE). Keeping equal-weight primary makes objective 1's theorem (Theorem H) about a secondary quantity. Ground rules 3 and 6 both point one way.
(ii) Class: POST HOC.
(iii) Study: rescoring of 2,400 fits from saved `log_Z_r`, `pip_r` (the SMCBVS.rds records S-ELS read); HPM and Ẑ unchanged; MPM may change in some fits.
(iv) Proof route: V3 (Prop P) PROVED candidate; Theorem H PROOF SKETCH with one crux (the measured-round island identity for general h, THM-SYNTH §9.1).
(v) Cheapest check: compute both PIPs and both MPMs on all 2,400 fits; report max |Δ| and MPM changes. The two designs measured so far give max ΔPIP 2e−4 and 2.3e−3 (DOSSIER §5), so I expect the switch to cost nothing numerically on the study.

Why the "noisy under masking" worry does not reverse this: the upper tail of W_r is O_P(1) (Markov, T31(i)), while the lower tail is the log-odds overshoot of a late crossing (MASKZPIP E1/E2) and a non-crossing island has Ẑ_r ≤ √δ₁·Z except w.p. 2√δ₁ (F-MASKPIP M2). So Ẑ-weighting can only *down*-weight islands, and only those that did not cross, which are exactly the islands with wrong PIPs (M1). The price is an effective island count near 1 in a masked fit, i.e. the Monte Carlo variance of one island's RB-PIP at N = 2,500 instead of four. That is a variance of order 1/N against a bias of order 1 for equal weighting (judgment on the orders; the inequalities are the cited ones).

Inherent: E[W²|𝓒] can be exponentially large under masking, so the R needed for the pooled bound is not bounded above (METH-AUDIT Prop P caveat; THM-SYNTH §3.2). Inherent to importance-weighted evidence from a masked start (see §4).

### 2.6 Flags and diagnostics

**Verdict: keep as triggers and heuristics; add two PROVED certificates; drop nothing.**

- As triggers (E1–E3, forced steps, grid flags) they decide escalation and so define the law of 𝓒 (`v3_calib.R:101–118`). Removing them is a method change with a 2,400-fit re-run. No real issue justifies it.
- As reported flags the study says: E1 0, E3 0, E2 83/2,394 with 10 among 565 posterior misses (S-ELS §3; this seat's cross-tab: power 1.8%, false-alarm 4.0%); "the warning flags do not identify the wrong answers" (BRIEFING §4.3). This is expected and not a defect: every wrong answer in the study is a posterior miss, and no sampler diagnostic can see a posterior miss. The study contains zero sampler failures, so it cannot measure flag power at all. The negative theory (V12, E1c) is about blind-grid failures the study never exhibited.
- Add, with a provable positive property: MASKZPIP C1 (Ẑ < Z_𝒯 ⇒ Ẑ underestimates; PROVED, deterministic) and the O-CERT card (region optimality and π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, 0.05Ẑ), with P(output and a card item false) ≤ 0.05 at every n; PROVED candidate). Both POST HOC. Also report Z_𝒯 itself (A3, two-sided when S₀ ∈ 𝒯).
- Do not add R̂ or PSIS k̂ now: R̂ inherits E1c's limit; k̂ for SMC weights is unstudied (THM-INV §4b B2, B3). BJV's estimated TV bound is the right v2 candidate (HQ-DIAG).

Inherent: weight-based diagnostics can certify too early (Chatterjee–Diaconis Thm 2.1, THM-INV §4b B1); island agreement is uninformative when the grid is blind (E1c PROVED). Inherent to diagnostics built from the run's own weights.

### 2.7 Theory fit

**Verdict: accept; no choice blocks a proposal goal; one choice makes theory harder and is fixed by item 5.**

- §5.1 exactness, §5.2 SMC consistency: by construction and cited; V5 needs its one-page lemma written (THM-SYNTH V1(v)). No method dependence.
- §5.3 weight stability: matched only under H-ORTH (THM-INV §3a); the ESS-0.9 schedule is the method's answer; v2. Not blocked by any choice.
- §5.4, §13.1 E_π[h] accuracy: Theorem H covers Ẑ-weighted estimates in every regime with R_n as a hypothesis (THM-SYNTH A1). **Equal-weight primary would leave objective 1's theorem about a secondary quantity**: item 5 fixes this.
- Song–Liang "last drop": our lack of Hellinger contraction and of p up to e^{Cn^α} (THM-INV §3b) is a property of the prior (g = n, BB(1,p), Felipe's model, `METHODOLOGY_v3.md` §5), not of the sampler; not on the table.
- Parallel claim: Theorem D/STG/CD are about the layer as proposed; the as-coded masked T_n is OPEN (Conjecture P) regardless of layer choices; the Θ(p) factor must be printed (LIT-PAR §3.3).
- LS0: without it the masked consistency of the shipped method holds only on the STAB-LH subfamily (R5 (b2-LH)); with it, (b1-LH) is about the shipped method. Include LS0 (item 3(f)).
- R declared in advance (Prop P(v)) and GUARD under workers (item 3(a)) are the two hypotheses the layer adds to the theorems; both must be in the spec text.

### 2.8 Anything else

1. **Re-run the 6 `resource_limit` fits under PEL** (all S5 wall-time stops on one CPU; METH-AUDIT §9): ADDITIVE, 6 fits × ≤ 2 h × 4 cores on NOTS, removes the P(U) caveat's only measured mass. Real issue: R6.
2. **VAL-FP at production size**: measured at p ≤ 40 only (API-AUDIT §6), and ε scales with R′/4 (METH-AUDIT §3 row Prop 2(f)). Replay 2 study designs with the long-double core. Cheap; otherwise the paper's floating-point sentence is about p = 40.
3. **METH-AUDIT §6 is a placeholder** ("[filled in after the runs]"); THM-SYNTH REPORT §8 already warns. No measured depth or wall-time sentence may be printed until HQ's replay logs fill it.
4. **R-vs-N rule** (HQ objection 7): N_e per island stays max(2500, n, p) (it sets the equal-weight bias and per-island delivery); R′ = the declared worker count, default 4; scaling experiments at R′ ∈ {8, 16, 32} at fixed N_e. Never split N_e (C8 rejected; Cor V is PROOF SKETCH and DELIV under a split is OPEN).

## 3. HQ's objections (dossier §4)

1. **Block start contributes little.** Partly accept. π₀(S₀) is tiny and the bridge does the work; but π₀(𝓡₂) = 0.81 with no extras in the mode is not "little", and the proposition is untested on depth. The ablation decides; the deciding statistics are T (final and pilot), rebuilds, tier, log Ẑ_r spread and whether S₀ ∈ V, not HPM counts (§2.1).
2. **Backfit favourable far more often; switching is WORKHORSE.** Accept both halves; reject the switch (§2.1). The favourable-count gap is real on 2,400 fits (API-RESID §3.4) and is still not a ground-rule-2 issue.
3. **Two PIPs pull apart.** Accept; resolve by Ẑ-weighted primary (§2.5).
4. **Calibration least theorised, most sequential.** Accept the first, reject the second as a cost statement (H₀ = 512 ≪ N₀ = 2,500; (b) makes diagnostics concurrent). No change (§2.4).
5. **Concurrency evidence thin.** Accept. Require: W-cal executed on 3 designs; the independent code check of scorer statelessness and ledger write-only (METH-AUDIT §8.1); GUARD-under-workers specified. Until then the paper says "code audit + 3 executed designs", not "bitwise in general".
6. **LS0 additive in the production core, not just the export.** Accept the demand; the check is a bitwise replay with the block merged (3 designs, same harness) plus the identity of the export's computation with a merged core (API-AUDIT §3: same ledger, same cache, no uniforms, after the islands). The 0/2,394 result then transfers by construction.
7. **Default R′ and R-vs-N.** Accept; rule in §2.8.4.
8. **Flags have no positive power result.** Accept; and note the study cannot supply one (zero sampler failures). The provable positives are the certificates (§2.6).

## 4. HQ's candidate inherent limitations

- **Per-round Θ(p) sequential steps:** inherent to the Gibbs-round kernel (a systematic scan is sequential by definition), not to SMC; fixable only by a WORKHORSE kernel change that breaks the Gibbs-path theorems. Agree, as "inherent to v3.1".
- **Each worker holds XᵀX (8p²):** inherent to targeting the exact posterior with full-coordinate moves (every round touches every coordinate; METH-AUDIT §2.1 memory paragraph). Agree. Mitigation (shared read-only per node; Gram-free scorer at O(nk²) per score beyond p ≈ 3·10⁴) changes the constant, not the fact that every worker needs all of X, unlike Song–Liang's n × p/K.
- **SMC weight variance through a masked crossing:** inherent to importance-weighted evidence: an island whose population has not reached the truth's basin cannot weight it, so Ẑ_r errs downward by the log-odds overshoot (E1/E2 PROVED), and E[W²|𝓒] ≳ 1/P_𝓒(crossing) (PROOF SKETCH, THM-SYNTH A1(v)). Agree. Not inherent: the *resolved-grid* half (V11, Conjecture) may yet bound it.
- **No run can upper-bound Z:** inherent (T31(c); unvisited states of a finite space carry unbounded mass without structure). Agree; the box certificate (O-CERT C4) gives exact bounds inside an explicit region, which the paper should use.
- **Markov-only Ẑ lower bound:** disagree as stated; it is merely unproved. A second-moment input (O-PW2 Thm B/C with an L² constant, or Cor V made rigorous) would sharpen it. Only in the masked regime, where E[W²] can be exponentially large, is Markov tight in kind.
- **Weight-based diagnostics certify too early:** inherent to diagnostics built from the same weights (CD Thm 2.1; E1c). Agree.
- **Posterior misses at n = 200 (565/2,400):** inherent to the statistical problem; Π(X) is a property of the design and prior, lower-bracketed (N200 Prop 2 PROVED), not of the sampler. Agree; selection accuracy is capped by statistics, and the paper should print the N200 split.

## 5. Open questions to close before theory proving starts

| # | Question | Closes | Evidence or check |
|---|---|---|---|
| Q1 | Does the block start reduce T, rebuilds and Ẑ spread at matched compute? | item 1 | ABL-START paired tables (criterion in §2.1) |
| Q2 | Is W-cal bitwise when executed; are the scorer stateless and the ledger write-only in islands? | item 3(a)(b) | 3-design replay of `v3_calibrate`; independent code read of `v3_score.h:139–255`, `v3_ledger.h:110` |
| Q3 | Is the merged LS0 block bitwise-neutral on the study path and HPM-identical to the export? | item 3(f) | 3-design replay with LS0 merged; compare to O-LS0 records |
| Q4 | Max |Δ| between Ẑ-weighted and equal-weight PIPs and MPM changes on the 2,400 fits? | item 5 | post hoc script on saved `log_Z_r`, `pip_r` |
| Q5 | GUARD semantics under workers (run wall clock; any-worker stop ⇒ no output) written into the spec and code? | item 3(a), Lemma RO | spec text + one forced-stop test per worker |
| Q6 | Does the island identity hold for the measured-round average of a general bounded h? | item 5, Theorem H | referee-level check against locked T12/T15 and W2-T26 Lemma 3 (THM-SYNTH §9.1) |
| Q7 | Do the 6 `resource_limit` fits complete under PEL? | item 8.1, R6 | 6 fits on NOTS, 4 cores each |
| Q8 | R′ default, declaration rule, flags over R′ islands: fixed in the v3.1 spec? | items 3(d), 8.4 | spec text (ADDITIVE; no run) |
| Q9 | METH-AUDIT §6 filled from the replay logs? | item 3, Theorem D | HQ's `evidence/concurrency_runs.log` into the table |
| Q10 | VAL-FP η, ε at p = 500 and the ε scaling with R′? | item 8.2 | long-double replay, 2 designs |
| Q11 | Will the paper demonstrate any p > 2,500? If yes, C6 implemented and law-checked. | item 3, ground rule 4 | HQ/Felipe decision; 20-seed two-map law check |
| Q12 | Ordering of LS0 relative to the final local search fixed (after, as in the export)? | item 3(f) | spec text |

Everything else I raised is either a stated limitation (§4) or v2 (DELIV-POP, Conjecture P, E[W²] bound, HQ-DIAG), and should not hold up theory proving.
