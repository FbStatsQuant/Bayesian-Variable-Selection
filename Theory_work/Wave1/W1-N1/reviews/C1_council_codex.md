# W1-N1 — independent council review, Codex seat

**Verdict: PASS. Overall score: 9.3/10.** I would sign off on N1 and Corollary E as **PROVED under the named premises, cross-family checked by this seat**. All six gates pass. This is one independent council verdict; it does not certify that both council reviewers passed the same round or that every FR04 deliverable is complete.

I read `Theory_work/Wave1/PROTOCOL.md` first. I did not read W1-N1's LOG.md or any file in its reviews directory. I reviewed the locked statement, all six proof files, the numerical sources and archived outputs, and the cited primary sources. I changed only this output file. No state-changing git command was used.

Path abbreviations below:

- `N1/` = `Theory_work/Wave1/W1-N1/`.
- `CODE/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.
- `T12/` = `Docs/Theory/proofs/T12_T8_frozen_run_identities/`.
- `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`.
- `SOP/` = `Theory_work/State_of_Project/sections/`.

## Gate verdicts

**G1 — PASS: correctness of every step.**

The core argument is valid. Lemma P starts from exact iid starts, applies the weighted resampling identity, then bridge transport and kernel invariance; the induction legitimately applies to the fixed function G_t K_phi f (`N1/lemmas/L2_post_terminal.md:31-40`). Post-terminal rounds preserve the evidence-weighted population identity by conditional expectation and invariance, without assuming stationarity (`:42-49`). This agrees with the actual locked conclusions `T12/STATEMENT.md:59-60` and their proof at `T12/PROOF_v6.tex:119-131`.

The code bridge supplies the necessary execution law: sequential consumption at finite stopping times gives fresh iid tails; the argument then derives iid starts, multinomial ancestors, and the conditional product law of particle paths (`N1/lemmas/L1_bridge.md:63-93`). The permutation argument is correct despite repeated neighbour-swap mechanisms: their labels remain distinct.

Lemma F applies the bounded measurable freezing identity to the localised integrand, including calibration-dependent h (`N1/lemmas/L3_freezing.md:27-39`; source `T12/PROOF_v6.tex:157-162`). N1 fixes c before using Lemma P and subsequently averages four identities (`N1/lemmas/N1_theorem.md:19-25`). This avoids both adaptive-h selection and an invalid exchange involving a random test function.

Corollary E follows from the pointwise indicator domination and positivity of W, followed by N1 on the off-S0 indicator (`N1/lemmas/E_corollary.md:14-21`). The case S0 outside the capped support is explicitly correct. I found no mathematical counterexample or missing inference in these arguments.

**G2 — PASS: hypotheses used match hypotheses stated.**

The statement fixes the data and specifies finite support and positive masses (`N1/STATEMENT.md:20-25`); gives finite integer parameter domains and the terminal grid (`:29-35`); and requires jointly measurable h with a deterministic uniform bound (`:62-66`). Exact arithmetic, exact start sampling, ideal within-stream randomness, kernel identification, calibration, single-island independence, measurability, potential-run scope, and worker equivalence are named (`:70-90`). These cover the proof's uses.

Full independence between final islands is unnecessary for this single-island identity. The proof correctly isolates SI and does not purport to discharge the stacking-stream audit (`N1/lemmas/L3_freezing.md:41-43`; `N1/lemmas/N1_theorem.md:31-35`). The stronger full-stream wording in STATEMENT is explicitly qualified by its exposition note (`N1/STATEMENT.md:71-74`). There is no concealed design, concentration, or mixing assumption.

**G3 — PASS: no hidden assumptions.**

The bridge addresses shared cache and ledger history rather than assuming islands are operationally isolated: cache hits resolve model equality and return the same deterministic score, while bookkeeping and RB accumulation do not affect transitions (`N1/lemmas/L1_bridge.md:52-61`; checked against `CODE/cpp/v3_score.h:271-291` and `CODE/cpp/v3_ledger.h:105-114`). Wall-clock fields and guards are excluded from the statistical record (`N1/lemmas/L1_bridge.md:14-21`), consistent with potential-run scope.

The measurable record construction is justified on countably many finite-parameter cells (`N1/lemmas/L1_bridge.md:103-109`). Localisation on A intersect {r <= R'} is explicit in Lemma F and N1 (`N1/lemmas/L3_freezing.md:11-15`; `N1/lemmas/N1_theorem.md:14-15`). No positive probability of successful calibration is required to assert that localised conditional identity. No guarantee conditional on output/completion is inferred.

**G4 — PASS: dependencies have adequate status and are not upgraded.**

The package preserves the source statuses: T12 is **PROVED-LOCKED**; N9 is **PROVED (candidate), code-checked**; CHK_INHERITED is **VERIFIED WITH AMENDMENT** (`N1/lemmas/N1_theorem.md:38-39`). These agree with `SOP/04_theory.tex:102,122-126`, `NBH/branch_snapshots/N9-KERNEL/REPORT.md:5-11,17-24`, and `NBH/branch_snapshots/MEET-THM/evidence/CHK_INHERITED/REPORT.md:134-152`.

START and KERNEL are explicit premises, rather than silently promoted unconditional theorems. I checked the inherited kernel balance arguments and start-sampler telescoping (`NBH/branch_snapshots/N9-KERNEL/PROOF.md:87-92,116-120,153-161,184-188,222-231,266-284`) against the corresponding production operations. The inherited amendments concern overstatements about necessity of order conditions and stationarity; this proof uses sufficient conditions and evidence-weighted identities, avoiding those overstatements. Corollary E proves the sharper constant directly; it does not borrow proved status from the **PROOF SKETCH (NEW-SYNTH)** entry TH412 (`NBH/ID_REGISTRY.md:560`).

**G5 — PASS: constants, bounds, and numerical tolerances are tracked.**

For fixed data, Z0, min d, and max d are independent of calibration. Positive grid increments summing to one give

`Z0 exp(min d) <= Zhat <= Z0 exp(max d)`.

The bound is uniform over grids, particle counts, and burn-in lengths, so multiplying by the deterministic B_h establishes the bounded integrand needed for freezing (`N1/lemmas/L3_freezing.md:34-36`; source `T12/PROOF_v6.tex:172`). It is legitimate here because the blocks/start tables are fixed data functions, not random calibration choices (`T12/STATEMENT.md:17-21`).

The exact constant in E is delta1, implying the card's 2 delta1. Equality for h = 1{S != S0} establishes sharpness (`N1/lemmas/E_corollary.md:14-28`; card `SOP/04_theory.tex:117`).

Numerical thresholds are explicit: N1 residual 1e-10, round checks 1e-12, negative controls above 1e-6, and MC rules |z| <= 4 and z_E <= 4 (`N1/numerics/n1_exact.py:211-220`; `N1/numerics/make_results.py:120,140,155-165`). Reported worst N1 residual 9.3e-15 and MC maxima 3.48 and 2.79 match regeneration (`N1/numerics/RESULTS.md:153,230`). These are numerical checks, not certified arithmetic or rigorous simultaneous confidence bounds; the report explicitly states the arithmetic limitation (`:7`).

**G6 — PASS: fidelity to the method as coded.**

I checked these correspondences directly:

- Starts, evidence initialisation, pre-resampling increments, multinomial resampling, and one stage round: `CODE/cpp/v3_engine.h:287-300,318-332`; bridge `N1/lemmas/L1_bridge.md:37-50`.
- Resampling uses N fresh uniforms and inverse cumulative selection, not systematic resampling: `CODE/cpp/v3_engine.h:235-259`; bridge `N1/lemmas/L1_bridge.md:75-80`. The u=0 adjustment is null under the stated continuous-uniform premise.
- Uniform, state-independent Fisher–Yates order and particle-by-particle rounds: `CODE/cpp/v3_engine.h:196-217`; bridge `N1/lemmas/L1_bridge.md:81-93`.
- Measurements occur after each complete terminal round, following L burn-in rounds: `CODE/cpp/v3_engine.h:344-360`. Plain counts are normalised by N times Hm at `:371`. These are distinct from the pre-Gibbs RB records at `:129`.
- Final streams are 9+r and starts are not supplied from calibration: `CODE/cpp/v3_core.cpp:468-471`. The literal measured-round and island counts are four: `CODE/v3_run.R:87-88`.
- Successful grid construction starts at zero, progresses strictly, and reaches exactly one: `CODE/cpp/v3_calib.h:71-95`.

The general-h average agrees with the adopted specification (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:159`). The package correctly discloses that arbitrary-h accumulation is spec-only in this frozen core (`N1/STATEMENT.md:51-57`). Likewise stacking is conditional on named stream/worker premises, not an audit result (`:80-90`; specification `METHOD_v3.1_FINAL.md:142`).

The numerical grid is expressly pilot-derived using an enumerated V, rather than a replay of full production calibration (`N1/numerics/RESULTS.md:9-13`; `N1/numerics/cpp/n1_harness.cpp:282-301`). This is adequate for the arbitrary-frozen-grid claim. The MC hook observes the same measured endpoints and is cross-checked against production pip_plain (`N1/numerics/cpp/n1_harness.cpp:335-346`).

## Independent numerical verification performed

Without writing generated files, I regenerated RESULTS.md in memory from the archive: the text matched exactly and every embedded assertion passed. All 70 available archived files matched their manifest hashes; 120 manifest entries refer to unarchived files. All 10 recorded production-header hashes matched. Removing exactly the two measured_hook lines from the instrumented engine recovered the production engine text.

I additionally checked the multiset order DP against all 120 labelled permutations of a five-label synthetic example, and checked the N=2 weighted/unweighted resampling recursion against explicit enumeration on three states; discrepancies were below 1e-14. These independently exercise `N1/numerics/n1_exact.py:37-58,103-120`.

I did not freshly regenerate the large kernel binaries or the 2.5 million MC island records. The numerical verification above validates archive consistency and the inspected recursions; it is not a fresh end-to-end computational reproduction.

## Remaining issues and concrete fixes

1. **NON-BLOCKING — put the localisation convention beside the locked statement.** `N1/STATEMENT.md:94-107` writes conditional expectations of island quantities undefined off the launch event. The rigorous convention appears in `N1/lemmas/L3_freezing.md:13-15` and `N1/lemmas/N1_theorem.md:14-15`, so the proof is sound. Concrete fix: with the appropriate statement-lock bookkeeping, add the same indicator-based convention immediately before STATEMENT section 3. This is an exposition repair, not a change to the proved claim.

2. **NON-BLOCKING for mathematical sign-off; outstanding FR04 deliverable — Lean.** `SOP/06_open_and_plan.tex:116` includes a Lean file to the registrar in “Done when.” `N1/STATEMENT.md:3-5` records an objection instead. No Lean certificate is supplied in the reviewed package. Concrete fix: HQ should either record an explicit waiver of that milestone or supply/register the requested finite recursion certificate. Do not label the ticket Lean-certified or claim every FR04 acceptance item is complete merely from this council score.

**BLOCKING issues: none.** My sign-off covers N1 and Corollary E for the idealised potential run under the explicitly named premises. It leaves the inherited dependency statuses, stream-extension/concurrency/guard audits, and downstream theorem statuses unchanged.
