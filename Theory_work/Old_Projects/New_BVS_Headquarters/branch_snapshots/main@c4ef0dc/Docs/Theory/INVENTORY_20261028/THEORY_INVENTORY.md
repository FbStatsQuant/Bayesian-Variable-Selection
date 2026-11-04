# SMC-BVS v3 theory: inventory, alignment with what ran, and what it means (2026-10-28)

For Felipe. Written by HQ (Opus) from these inputs:
- four Sol 6.1 audits (`work/S_A…S_D`);
- a Haiku inventory with a hash check (`work/H1_inventory.md`);
- Sonnet intuition notes (`work/SN_intuition.md`);
- a Sonnet citation check (`verify/SN_citecheck.md`): 396/396 code citations verified, 3/3 planted false citations caught;
- two Astra (high) consults (`consult/`).

HQ re-checked every material finding in the code and statements itself. **Status:** nothing here is adopted, and no theorem was changed.

---

## 0. Bottom line

1. **What we have.** 21 locked results, covering 20 of the 36 conjectures (12 in full, 8 in part). All 38 locked files match their recorded hashes.
2. **The theory describes the method that actually ran, with two caveats.**
   - The code is byte-identical to the production run.
   - The posterior it targets is exactly the one the theorems analyse: same formula, same constants.
   - The start sampler, moves, tempering bridge, resampling, grid rule, islands, RB PIPs, evidence estimate, all-scored HPM and local-search rules all match, up to the standard idealisations (exact arithmetic, ideal random numbers).
   - The 4× escalation is decided by calibration only, so it does not break the frozen-run results.
   - **Caveat 1 (rare in practice, but it narrows the claims).** Production can stop a fit when it hits its time/memory budget. There were 6 such `resource_limit` failures in 2,400 fits; the audits could not tell at which phase each stopped. Several computational theorems assume the final run always finishes. Their guarantees (unbiasedness, coverage, miss probabilities) are about that *potential uninterrupted run*. They do not automatically hold for "the fits that happened to finish": selecting on completion is a different statement. A restatement with a latent uninterrupted run plus a separate "output available" event needs little new mathematics. But it narrows the claim rather than repairing guarantees for the available outputs, and six failures cannot by themselves show the effect is negligible.
   - **Caveat 2 (interpretive).** The statistical theorems (T03, T06, T07) are about the *true* posterior's best model. The method *reports* the best model it ever scored. The bridge between the two is T21, which is proved but conditional.
3. **At our sample size (n = 200), the statistical theorems are asymptotic statements, not numerical guarantees.**
   - The eigenvalue condition SE, used by T02(ii), T03 and T04's sharper parts, *cannot hold* at n = 200, p = 500/1000. It asks for well-conditioned subsets of up to 215/229 columns, but the data have rank ≤ 199.
   - The explicit beta-min constant in T03 asks for squared signals ≥ 55, while ours are 0.64 (c = 1) and 0.16 (c = 0.5).
   - The rates evaluate to numbers that are not small (0.16, 2.9, even 2,667).
   - This does not make the theorems wrong. It means the 2,400-fit results stand on their own: the theory explains the *mechanisms*, not the *numbers*.
4. **What is genuinely meaningful at n = 200** is the exact, finite-sample layer:
   - the posterior identity (T01);
   - the tie and identifiability limits (T06);
   - the HPM/MPM decision theory and the "no size prior can fix a ranking error" ceiling (T07);
   - exact start and valid moves (T09);
   - the addition floor (T10);
   - the iid-draw miss probability (T11(iii));
   - the frozen-run identities: E[Ẑ] = Z, and E[Ẑ·PIP-hat] = Z·PIP. The *unnormalised product* is unbiased, not the ordinary PIP estimate (T12);
   - the grid identity (T13);
   - local-search semantics (T20(i));
   - the composition inequality (T21);
   - the deterministic start bounds (T22(i)(ii)(iv));
   - the 95% evidence lower bound (T31).
5. **The single biggest open gap** is an unconditional proof that the true model gets *scored*. T21 shows that "scored" plus "posterior mass > ½" is enough for HPM = truth, but whether the truth is scored rests on open hypotheses: EXP′/VIS/NL, or H2/H3 together with H24.

---

## A. Inventory

### A.1 Counts (`work/H1_inventory.md`; hashes 38/38 MATCH; both planted canaries caught)

| Status | Core | Secondary | Optional | Total |
|---|---|---|---|---|
| Proved, all parts (locked) | 12 | 0 | 0 | 12 |
| Partly proved (locked parts) | 6 | 2 | 0 | 8 |
| Not proved | 4 | 8 | 4 | 16 |
| **Total conjectures** | 22 | 10 | 4 | 36 |

- **Proved, all parts:**

  | Theorem | What it proves |
  |---|---|
  | T01 | contrast reduction |
  | T02 | dimension and supersets |
  | T03 | selection consistency |
  | T04 | contraction |
  | T06 | identifiability and ties |
  | T07 | size-prior ceiling and Bayes decisions |
  | T09 | exact start and valid kernels |
  | T10 | addition floor |
  | T12 | frozen-run identities |
  | T13 | restricted ESS |
  | T15 | occupancy |
  | T21 | HPM composition; route (e) is conditional on the unproved H24 |

- **Partly proved:**

  | Theorem | Proved part | What it proves |
  |---|---|---|
  | T11 | (iii) | iid-draw miss probability |
  | T14 | (i) | evidence, singleton case |
  | T20 | (i)–(ii) | local search |
  | T22 | (i)–(iv) | start aggregation and concentration |
  | T23 | (ii) | pathwise PIP bound |
  | T25 | (iv) | evidence variance under PW2 |
  | T27 | (i) | cancellation mass law |
  | T31 | (i) | evidence lower bound |

- **Not proved:**

  | Rank | Theorems |
  |---|---|
  | Core | T17 (reflection coupling), T28 (evidence loss), T32 (resource counts), T34 (statuses) |
  | Secondary | T05, T16, T18, T24 (terminal repair: the H24 input), T26 (no-switch consistency), T29, T33, T36 |
  | Optional | T08, T19, T30, T35 |

- **Review depth differs by wave:**
  - Wave 1 had 5 reviewers, including Fable and Astra.
  - Wave 2 had Astra/Sol reviews plus a Claude audit.
  - Wave 3 had 2 independent Opus reviewers each; its external OpenAI review is still queued.
  - "Locked" ≠ "adopted"; adoption is your call.

### A.2 Open hypotheses that the proved results still lean on
- **For "the truth gets scored / the start finds it":**
  - EXP′, VIS, NL_η, NL_avg (T22(iii));
  - H2, H3 (T27(i), the opposite regime; never combine with T22(iii));
  - H24 (T21 route (e));
  - exposure/occurrence conditions (T21).
- **For accuracy of the PIPs and the evidence:**
  - BASIN (T23(ii));
  - PW2 (T25(iv); the theorem adds nothing beyond PW2);
  - COVER and pool avoidance (T13).
- **Statistical regime:** G, R, SE, beta-min, DX, NIS, DUP.

---

## B. Does the theory describe what was executed?

**Method of the audit.** Each result was traced through three layers:
- L0 = METHODOLOGY_v3.0, which the theorems were written about;
- L1 = master Part I, as deployed;
- L2 = the code that ran.

Verdicts: MATCH / IDEALISATION (EX-A exact arithmetic, EX-S ideal random streams, CAL, EXEC) / DIVERGENCE-MINOR / DIVERGENCE-MATERIAL / NOT EXERCISED / UNRESOLVED.

**Provenance.** `verify/HQ_PROVENANCE.md`: the local code read by the auditors is byte-identical to the NOTS production code. The manifest's SHA256SUMS matches, and 24/24 core and study files are identical.

### B.1 What matches (checked file:line)

| Method component | Theorems relying on it | Verdict |
|---|---|---|
| Preprocessing (centring, SD scaling), cap K = min(p, ⌊n/2⌋) = 100, BB(1,p) size prior normalised on the capped space, g = n slab with unit ridge, IG(0.01, 0.01), full marginal likelihood; ridge keeps every model finite | T01–T04, T06, T07 | MATCH up to EX-A: the scorer is exactly the formula the theorems analyse |
| Blocks (B = 14), BF tables, composite start π₀ and its exact backward sampler | T09, T10, T11(iii), T22, T27 | MATCH (EX-A/EX-S) |
| Bridge γ₀·exp(φd); Gibbs, uniform swap, neighbour swap and independence moves; random round order; cap boundary | T09, T10 | MATCH (EX-A/EX-S) |
| Q_f = 4·N_e·(T+L+5) exact iid start draws in the final run | T11(iii), T21(a) | MATCH, for runs that finish |
| Restricted ESS ρ_V, the 0.90 acceptance rule, 60 halvings, frozen grid | T13 | MATCH, with endpoint snapping as a minor wording difference |
| Calibration on streams 0–9; fresh final run on streams 10–13; grid, tier, N and L frozen before the final run; **escalation (4×) triggered by calibration only; final flags never trigger reruns** | T12, T14, T15, T23, T25, T31 | MATCH. HQ re-checked `v3_calib.R:145–149` and `v3_fit.R:133–134` |
| Evidence product per island, pooled arithmetic mean over 4 islands; RB PIP recorded *before* each Gibbs draw, equal-island mean | T12, T14(i), T15, T23(ii), T25(iv), T31 | MATCH (EX-A/EX-S) |
| Reported HPM = best of all scored models, exact ties broken by size and then lexicographically; observer removal did not remove HPM updates | T07(iii), T21 | MATCH |
| Local search over all flips and swaps; strict improvement; `local_certified` only if the returned model is the scanned centre | T20(i)–(ii) | MATCH (EXEC) |
| 95% evidence lower bound log(0.05) + log Ẑ | T31(i) | MATCH (only the separate relative-scale field is not emitted: minor) |

### B.2 Material divergences

1. **Mid-run stops (`resource_limit`).**
   - **The code.** A runtime guard can stop a fit when the time/memory budget is hit, either partway through the final run (`cpp/v3_engine.h:335–337`, `v3_core.cpp:442`; HQ checked) or after the final local search, when all four islands have already finished (`v3_core.cpp:450`; citation check). In both cases the fit reports no evidence or PIPs.
   - **The theory.** T11(iii), T12, T14(i), T15, T23(ii), T25(iv), T27(i)'s retained setting and T31(i) describe a run that always finishes.
   - **What happened.** 6/2,400 fits ended `resource_limit`, all in S5; their stopping phase is not recorded in the summaries.
   - **Effect.** The distributional guarantees (unbiasedness, coverage, probability bounds) are about the potential uninterrupted run given calibration. Pathwise identities hold on completed trajectories. Neither covers the stopped fits, nor statements made "conditional on the fit finishing".
   - **Fix.** Restate them for a latent uninterrupted run plus a separate "output available" event; T21 already does this through its P(U) term. This needs little new mathematics, but it narrows the claim: guarantees *among available outputs* would need control of the stopping event.
2. **Global versus reported quantities.**
   - **The theory.** T03's HPM/MPM/PIP consistency, and T06(ii), concern the *true* posterior.
   - **The code.** It reports the best *scored* model and *estimated* PIPs.
   - **Effect.** Presenting T03 as "the method recovers the truth" is wrong without the computational bridge. That bridge is T21 (scoring) plus T23 (PIP accuracy), and both are conditional.
   - T07 states this distinction correctly.

### B.3 Minor divergences (theorem still applies)

- **D2: secondary PIP removed.** T12's clause on the secondary pooled PIP is now moot. The primary estimator and the strict "> 0.5" rule are unchanged.
- **Grid builder snaps the endpoint to 1** and re-checks ESS afterwards (rulings RC-2/N1–N2). T13's "largest tested endpoint" wording needs a one-line amendment.
- **Diagnostic local search.** L0 says "after each diagnostic island"; deployment runs one search after the set of four. No theorem depends on the count.
- **T09 wording** on per-order reversibility is already corrected in the statement.
- **T31's relative-scale lower bound** is not stored as its own field; it is recoverable from `log_Z_rel_m0 + log(0.05)`.
- **cut_group (D4)** flags any split correlation component, with no size condition, which is broader than "component larger than B". It is informational only (see B.4).

### B.4 Executed, but no theorem covers it

- **Escalation (208 fits).** It is calibration-triggered, so it is *safe* for the theory, but no theorem says it *helps*.
- **Warnings E1–E3 and low ESS.** No theorem says they detect wrong answers. Across 2,400 fits, E1 and E3 never fired. E2 fired 29 / 3 / 45 / 6 times and low-ESS 12 / 5 / 23 / 9 times, in the order c=1 p500 / c=0.5 p500 / c=1 p1000 / c=0.5 p1000. Recovery was *not* worse in flagged fits at c = 1.
- **cut_group fired in 2,398 of 2,400 fits** (599/599/600/600). The threshold is √(2 log p / n) ≈ 0.25 at n = 200; probably chance correlations at that level link variables across blocks in almost every dataset (HQ's reading, not checked). Either way, in this design the flag discriminates very poorly. Cluster separation (D4) is a *condition* of T26, which is not proved; the flag cannot verify it.
- **Others:** resource guards and partial outputs, near-tie truncation, the stable-centring numerical fallback, and forced pilot steps (0 occurrences).
- **The heuristic exact-branch "global certificate"** is not exercised at p = 500/1000. It is labelled a heuristic; L0 had asked for a validated bound.

### B.5 Per-result verdict

"Applicable" = the theorem describes the executed method, given its stated hypotheses.

| Result | Describes what ran? | Main qualification |
|---|---|---|
| T01 | Yes (EX-A) | Statistical clauses need G, R |
| T02 | Target: yes. At n = 200: (i) vacuous (m_n > K), (ii) premise SE impossible | Asymptotic only |
| T03 | Target: yes. As a guarantee for *reported* outputs: no | Needs T21/T23; SE impossible at n = 200 |
| T04 | Target: yes; it does not concern reported outputs (no coefficients reported) | Only the fallback branch survives SE failure |
| T06 | Yes (EX-A) | Deterministic parts meaningful at any n |
| T07 | Yes | Correctly separates global from reported |
| T09 | Yes (EX-A, EX-S) | No mixing rate |
| T10 | Yes (EX-A, EX-S) | Visit bounds, not discovery |
| T11(iii) | Partly | Assumes the final run finishes (B.2.1) |
| T12 | Yes, for the potential uninterrupted run | B.2.1; secondary-PIP clause moot (D2); unbiasedness is of the products, not of the normalised PIPs |
| T13 | Yes, with snapping wording | COVER is unverified |
| T14(i) | Yes for completed runs | Needs mass concentrated near one model for a useful bound |
| T15 | Yes for completed runs | Island lower-tail input open |
| T20(i)–(ii) | Yes (EXEC) | (ii) needs H03 and reaching a neighbour of S0 |
| T21 | Yes, as a conditional composition | H03, H24 and exposure open |
| T22(i)(ii)(iv) | Yes (EX-A) | (iv-c) needs T03 and T22(iii) premises |
| T22(iii) | Correct object | EXP′, VIS, NL unverified; rate vacuous at n = 200 |
| T23(ii) | Yes for completed runs | BASIN open |
| T25(iv) | Yes for completed runs | PW2 open |
| T27(i) | Correct object | H2, H3 unverified |
| T31(i) | Yes for completed runs | Coverage is not conditional on completion or flags |

---

## C. What the statistical theorems say at n = 200 (`work/S_D_regime.md`; HQ re-derived SE and BM-C)

| Item | Value at n = 200, p = 500 / 1000 | Meaning |
|---|---|---|
| SE (global eigenvalue condition) | Needs subsets up to 215 / 229 columns; rank ≤ 199 | **Impossible here.** T02(ii), T03 (all clauses) and T04's SE branches lose this premise at this n: T04(ii), (iv), and the improved part of (iii). T04(i) and T04(iii)'s fallback variance result do not use SE. A version over models of size ≤ K + s0 = 114 would avoid the rank obstruction, but needs a proof review, and feasibility alone does not give a useful bound. |
| BM-C (T03 beta-min, explicit constant) | Needs θ² ≥ 55.0 / 61.1 (even with the most optimistic eigenvalue constant 1); ours are 0.64 (c = 1) and 0.16 (c = 0.5); the largest is 3.24 | Fails by about 100×, so T03(iv)'s screened set of strong signals contains *none* of the executed signals. The constant (M* ≈ 2,076 / 2,307) is called conservative in the statement itself. |
| Posterior-mass rate √(log n / n) | 0.163 | Not small; multiplied by an unknown constant |
| T02(i) size cutoff m_n | 201 / 215 > K = 100 | Vacuous: the cap already does more |
| T04 fallback prediction rate ε₂² | 2.90 / 3.58 (times an unknown C) | Larger than the noise variance (1): not informative |
| T22(iii) start-concentration rate | ≥ 2,667 (B = 14) | Vacuous at this n |
| T27(i) cancellation scale p^(-d) n^(-d/2), d = number of masked true variables | d = 1: 1.4e-4 / 7.1e-5; d = 2: 2e-8 / 5e-9 | Potentially severe *if* H2/H3 hold; not established |
| Regime conditions | G, R, NIS, DX, within-block SE: plausible. VIS, NL_η: doubtful. EXP′, NL_avg, BM-∞: unknown | From the population covariances, not the realised designs. R needs the experiment embedded with s0 = 14 *fixed* as n grows; the generator's own rule s0 = ⌊√n⌋ would violate it |

**Link to the 2,400 fits (suggestive, not tests).**
- **At c = 1, 90–92% of wrong answers are "truth plus one or more extra variables", with nothing missed.** That is the direction T02(ii)'s superset rate (0.16, not negligible) points to. But the data do not show whether the posterior actually ranked the superset above the truth, or the truth was never scored. The posterior-score check proposed earlier settles this.
- **At c = 0.5, HPM beats PIP > 0.5** (370 vs 338; 340 vs 321). This is consistent with T07: HPM is the Bayes rule for exact recovery, MPM for Hamming loss. Part of the gap may be PIP estimation error.
- **No locked theorem explains SMC-BVS's weak-signal advantage over the competitors.** T03(iv) and T04 are only conceptually related.

---

## D. Relevance and intuition (short form; the full notes are `work/SN_intuition.md`)

The theory has two halves. The **statistical half** asks: does the posterior put its mass on the truth? The **computational half** asks: does the algorithm find, score and report what the posterior says? The key structural fact is that the reported HPM is the best model *ever scored*. So the computational half reduces largely to a *scoring* question ("was the truth ever evaluated?"), not a convergence question. That is why the HPM can work well before the sampler has mixed.

**Statistical half**
- **T01.** Standardising y slips a data-dependent scale into the prior. T01 shows the posterior is *exactly* a contrast-model posterior with that data-dependent rate. Bounds transfer from fixed-rate posteriors only by using a *lower* rate in one place and a *higher* rate in the other, at a bounded cost. It also shows that a single fixed rate cannot be compared with the posterior up to a constant factor. This sandwich is what lets textbook proofs apply to the real method.
- **T02.** Large models get geometrically little mass. Supersets of the truth have vanishing mass, at rate √(log n / n). This is the "no overfitting" guarantee.
- **T03.** With enough signal, the posterior concentrates on the truth, so HPM = MPM = truth and PIPs → 0/1. Without beta-min, the strong signals are still found. This is the headline consistency theorem, asymptotic.
- **T04.** Even when individual variables can't be identified, predictions and the noise level are still estimated well.
- **T06.** If two variable sets look identical to the data, no method can tell them apart. Exact ties otherwise have probability zero, and the tie rule is harmless. This sets the limits of what is achievable.
- **T07.** A size-only prior (like our Beta-Binomial) can never fix a ranking mistake within a model size. HPM is the right report for exact recovery and MPM for variable-by-variable accuracy. Better PIPs mean provably better MPM risk.

**Computational half**
- **T09.** Under exact arithmetic and ideal random numbers, the start sampler is exact and every move leaves its tempered target invariant. The building blocks are correct. It does *not* say a finite run has reached the posterior, and it gives no mixing rate. It is the foundation for everything else.
- **T10.** Below the size cap, adding any variable is never hopeless, only polynomially unlikely, on every dataset. This gives a universal entry floor. Its visit bounds do not guarantee discovery within the budget.
- **T11(iii).** It is coupon collecting: a model the start law gives probability π₀(S) is missed by all Q_f final draws with probability (1−π₀)^Q_f. Q_f ≥ 140,000 here. So for an uninterrupted final run, any model fixed in advance with π₀ ≥ 2.1×10⁻⁵ is scored with probability ≥ 95%.
- **T12.** For a frozen run, the evidence estimate is exactly unbiased, and so is the *unnormalised* product Ẑ × PIP-hat. The ordinary, normalised PIP estimate is not claimed unbiased; the statement gives a bias example. Conditioning on "the run looked good" breaks these identities.
- **T13.** The grid rule checks smoothness only on models already scored. T13 gives the exact price of that blind spot. If those models carry nearly all the mass at every evaluation point, including the extrapolated temperatures above 1, the check is trustworthy. Without that coverage, the check *can* be fooled; it need not be.
- **T14(i).** When the tempered laws sit near one model, the evidence error is bounded by how far they stray from it.
- **T15.** It bounds the expected share, and the tail probability, of an island's particles in a bad region. The bound uses the posterior mass of that region and the chance that the island's evidence ratio falls below a threshold. This links evidence to occupancy. It is a probability statement, not a certificate for an already-realised population.
- **T20(i)–(ii).** `local_certified` means only "no better neighbour among those checked". If the truth is the unique summit, a scan from any neighbour finds it.
- **T21.** HPM ≠ truth requires one of: no output; the posterior's mass on the truth ≤ ½; or the truth never scored. Six routes (a)–(f) bound the last. This is where the two halves join.
- **T22.** The start puts provable mass on a reference model. The bridge can't lose the truth halfway if both ends sit on it. Under favourable assumptions, the start itself concentrates on the truth.
- **T23(ii).** An island's PIP error is at most the fraction of particle-rounds spent away from the truth, plus a term for the Gibbs probabilities *at* the truth. That term is at most (1−π(S0))/π(S0): even paths that stay at the truth need not give 0/1 values. Under BASIN this gives explicit error bounds.
- **T25(iv).** If the one-step condition PW2 holds, the evidence variance is bounded. The bound follows by unrolling PW2, so it adds nothing beyond it.
- **T27(i).** Suppose the conditions H2 and H3 hold: true variables are masked along an addition chain, and the reference model keeps start mass. Then the start gives the truth only about p^(-d) n^(-d/2) mass. Masking alone does not establish H2/H3, and the result draws no discovery conclusion: enough start draws can still find the truth. This is the unfavourable regime.
- **T31(i).** 0.05 × Ẑ is a valid 95% lower bound on the evidence, by Markov's inequality. It is one-sided and very conservative, and "flag not raised" is not a certificate.

---

## E. What would add the most (HQ recommendation, in order)

1. **Cheap empirical check (run on Owls).** For each c = 1 miss, compare the exact posterior score of the truth with that of the reported model, including numerical and tie checks.
   - If the truth scores *higher*, it was a search failure: the truth was never scored.
   - If it scores *lower*, the target misranks it (prior/statistics). That does not exclude a concurrent search failure.
2. **Small restatements with no new mathematics**, as one bookkeeping pass:
   - the completion/availability event for T11(iii), T12, T14, T15, T23, T25, T31;
   - T13 snapping wording;
   - dropping T12's secondary-PIP clause.
3. **A finite-n version of the statistical half:**
   - measured premise checks on the realised designs;
   - a proof review of SE restricted to models of size ≤ K + s0;
   - a sharper or explicit beta-min constant.
   This is what would let T02/T03 speak to n = 200. Feasibility alone does not guarantee useful bounds.
4. **The main open gaps.**
   - **For the HPM:** an unconditional route to "the truth is scored", through EXP′/VIS/NL in the favourable regime, or H2/H3 plus T24 (H24) in the masked regime.
   - **For PIPs and evidence:** BASIN and PW2, kept as separate priorities.
   These are the natural targets for the Fable-guided deep theory audit, when you order it.
5. **Method note for you.** cut_group is on in 2,398/2,400 fits, so it discriminates poorly at n = 200. Investigate why before deciding whether to redefine its threshold or drop it from reports. This is a method decision, not a theorem.
