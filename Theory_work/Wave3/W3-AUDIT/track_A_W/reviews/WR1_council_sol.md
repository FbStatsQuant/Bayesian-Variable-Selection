# Council W-R1 — sol — blind first read

Verdict: **ACCEPT W1 and W2; gates PASS.** No C, S or F finding. The island control-flow and joint-measurability arguments discharge the specified parts of the older bridge at the pinned core. The freezing argument supplies the stated localised identities for the potential calibration pair, with the actual-pair restriction retained. One nonblocking editorial finding concerns source line ranges.

Reviewed manifest: `0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea`. The prescribed verification command returned `verify: OK`. The working core also matches commit `4676af6` (`git --no-optional-locks diff --exit-code 4676af6 -- Scripts/SMC_BVS/core`, exit 0).

## Gates

| gate | decision | basis |
|---|---|---|
| G1 correctness and citations | PASS | Bounds, stopping times, record reconstruction, freezing and evidence inequalities check against the permitted sources and code. Editorial line-range issue below does not invalidate a derivation. |
| G2 used hypotheses = stated | PASS | Fixed valid data, successful setup under the imported execution setting, EX-A, H-U, measurable frozen settings and success set supply the hypotheses used. The h class remains jointly measurable with a deterministic uniform bound. |
| G3 no hidden assumptions | PASS | No regular conditional distribution on E or Polish calibration space is needed. Conditioning follows from the product measurable freezing lemma; no probability of calibration success or clock independence is assumed. |
| G4 imports and statuses | PASS | T1, T4–T7, FR and C1 are used within their stated scope. No imported candidate premise is silently upgraded; FR excludes T12 (iii), and W2 proves the needed conditioning separately. |
| G5 scope | PASS | Potential records, executed N_e and L, Hm = 4, serial final islands r = 1,…,4 and streams 10–13 are consistently used. Actual identities are restricted to T5's transfer rules. |
| G6 fidelity | PASS | Direct code reading agrees with the rechecked older bridge/freezing steps and D-i/MR's required coordinates and integrands. |

## Claims

| id | decision |
|---|---|
| W1 | ACCEPT |
| W2 | ACCEPT |

## Findings

1. **E — MR source ranges miss the named steps.** `Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/STATEMENT.md:15` and `W2_FRZ/PROOF.md:51` identify MR Step 2 using `MR_identities.md:57-65`; the step actually occupies lines 51–58, so the cited range omits the coordinate construction and includes part of Step 4. `W2_FRZ/PROOF.md:70` calls `MR_identities.md:67-70` “Step 3”; the actual bound is at lines 60–62. The analogous broad Steps 2–4 reference at `W2_FRZ/STATEMENT.md:13` should be lines 51–67. **Repair:** update these MR citations to the actual passages (including the repeated Step 2 reference in W1's use description where applicable) and refresh citation reports in a subsequent revision. These are locator corrections: W1 explicitly reconstructs the relevant coordinates, and W2 independently derives the bounds and conditional-expectation identity. No correctness, assumption or fidelity failure follows.

## Substantive checks

- **ISL-0:** `v3_core.cpp:443-446` creates each final source afresh; `RngSource::u` advances that source only. Inspected the elementary steps, order and resampling, deterministic evaluation, full-model cache comparison, scratch use and persistent engine members. The cache and ledger do not feed state transitions. `tmpQ` is initialised before each transition that uses it. Clock values reach timing fields and guard arguments; T1's potential convention removes stopping. The statistical record includes the mathematical execution trace, rather than requiring the full trace to be stored in the returned R object.
- **ISL-st:** independently counted draw_pi0 at most 1 + 2J; Gibbs 1; uniform swap 0 or 3; neighbour swap 0, 1 or 3; independence at most 2 + 2J; order m − 1; resampling N_e. These give the displayed κ_max and κ(c). Every operation's start is determined by a consumed prefix, including zero-read self-loops. At fixed c the starts are bounded stopping times; fresh tails and measurability of earlier draws justify D-i's induction. Exactly one independence label per particle-round gives D_r = N_e(1 + T + L + 4).
- **ISL-d:** the countable measurable partition by integer settings leaves finitely many Borel comparisons on each cell. Variable record dimensions fit a countable disjoint union of Polish components. Initial/stage/terminal populations and the order/path coordinates determine every required pre-step state. The partial evidence is reconstructed using the grid and populations before each reweighting, so no missing intermediate evidence coordinate is assumed.
- **FRZ-a/b:** rechecked T12's rectangle/monotone-class argument. It works for arbitrary measurable E and for one stream. T5 supplies measurable dependence on streams 0–9, hence independence from U_r under H-U. The success event is a measurable pullback; intersecting its representing set with A_s preserves that pullback. Successful v3_frozen construction validates the grid before calibration returns. The production settings and final source creation give O_r = Φ(𝓒°, U_r) on E₀.
- **FRZ-c/d:** tested the localised equality both on and off E₀, and checked the varying-index masks for MR. Positive stage factors telescope to the displayed evidence interval, including t = 0; dividing the upper endpoint by the lower endpoint gives the uniform C_d bound. F and MR integrands are therefore bounded as required. D's fixed-c no-draw value follows from its own iid-draw argument, rather than being attributed to FR. T5's actual/potential distinction is preserved without conditioning on the clock-dependent actual success event.

Overall score: **9.4 / 10**, assessed on C/S/F issues only; the E finding does not reduce the score.

## Checks performed

Prescribed manifest verification; read-only comparison of the core to the pin; both statements, proofs and saved CITECHECK reports; independent in-memory verification of all 73 W1 and 37 W2 extracted citation ranges and saved block hashes without rewriting reports; direct inspection of the relevant pinned R/C++ code; comparison with L1, L3, W1-N1 §2, T12's freezing lemma, the permitted sibling statements/FR proof, and the D/MR consumers. Re-derived the stopping-time, draw-count, measurability, monotone-class and evidence-bound calculations.

## Not checked

No binary64 guarantees, numerical experiments, runtime execution, Lean formalisation, probability of delivery/calibration success, calibration-island analogue of ISL, multi-island D-ii independence proof, or general direct-wrapper options. Imported sibling claims were used as the brief permits, not reopened as separate audits. Did not read INDEX, LOG, CHECK files, checkpoints, API_CARD, other review outputs, or C1's proof. The latter is cited in W2 but its permitted statement and the directly inspected grid-validation code suffice here. No git state was changed; this report is the sole file written; no subagents were started.

COUNCIL-VERDICT round=R1 manifest=0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea seat=sol score=9.4 gates=PASS
