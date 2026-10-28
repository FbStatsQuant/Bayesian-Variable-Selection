# DROPPED.md — candidates that did not survive, and why

Everything here is recorded so later work can return to it. Sources: council\PROPOSAL_v1.md §5 (council drops), review\PROPOSAL_v2.md §6 and CHANGES_v1_to_v2.md (review drops), judge\PROPOSAL_v3.md "Dropped or replaced items" and CHANGES_v2_to_v3.md (judge drops), RULINGS.md (lead). Reasons: LF = likely false; UR = unprovable or unworkable route; TR = trivial or vacuous; UA = unreasonable, insufficient or unverifiable assumptions; DM = demoted/merged (survives inside another item).

## Dropped at the council stage (PROPOSAL_v1 §5, kept as recorded there)
- Early candidates merged into T1–T23 (see council\PROPOSAL_v1.md §5 for the list). DM.

## Dropped by the review group (send-back O1–O6; PROPOSAL_v2 §6)
- T19 Tier A (uniform coupling at the pair): hypotheses refuted on every dataset by the addition floor (ζ ≥ h_{s₀}) and COVER-pair's ε_C ≳ n^{−1/2}. TR/UA. Survives as the reflected benchmark T18 (B-RP).
- Tier B′ uniform coupling bound and "alternatively restrict W": vacuous for bounded W. TR.
- T5(iii) additive band as the main statement: false for slowly growing p. LF. Replaced by the √λ-scale band (T05).
- T11(ii) "no ordering constant for a = 1": false (counterexample). LF.
- T17(iii)(a) over-tempered route (concentration up to w_T): needed concentration beyond 1 + δ with the binding point max_t w_t. UR. Replaced by the first-moment route (T14, T26).
- "TWO"/"valley-protected two-move set" as the negative regime: neither necessary nor sufficient. LF.
- T21(iv) "MISS with η_n → 0 fails": it is D_nη_n → 0 that fails; "≈ 20 entries" withdrawn as a number. LF.
- T22(iv) existence claim for usable upper bounds: false as stated (P8 counterexample). LF.
- Inventory: MASS (replaced by T22(ii)); ζ-EXIT (refuted); AGG-stat as a hypothesis (now a conclusion); OP's numerics clause; NL_η₀/TL as the stated hypotheses (kept as sufficient cases); "VIS follows from G, R, SE, BM" (cancelled variables); HIT's "only non-trivial instance"; "S̃₀ scanned as a centre". UA/LF.
- Demotions: T13 to a remark (now T36 at secondary); T20(i), T20(iii) to remarks; the "+2" in d⋆.

## Dropped or replaced by the judge (PROPOSAL_v3), adopted by the lead
- Separate T14-D: merged into T11 (L-LED/T14-D). DM.
- T15(i′), SE-only "every best move is a true move": signal-bearing proxies invalidate it (J3: correlations 0.65, S₀ = {1,2}, proxy wins the first improvement; a certified wrong local maximum at n = 128). LF.
- T18′ slot constants 1/(s₀!d!) and EXIT_d as internal-change control: internal non-Gibbs moves change the greedy maximiser without exiting (J4). UR. Replaced by the conservative ordering constant and segmented leakage accounting (T24).
- Endpoint-only pathwise RB bounds in T18: replaced by recording-prefix bounds (T23). UR.
- RET+OCC evidence-variance rate (T19 Tier B), automatic transfer of pair refresh to the actual run, automatic cancellation of Φ_t: missing particle-history control (J10 counterexample in an abstract two-state system). UR. PW2 recorded as a research target (T25(iv)).
- Blanket working-set / full-space vacuity claims (T12, L-RC): d ≡ 0 is a benign full-space case; a large union bound proves no impossibility. LF.
- T12's logarithmic-uniform concentration rate: unsupported transfer to the particle system. UR. Replaced by the conservative V_Z/V_R bounds (T19, optional, unvalidated).
- Start concentration without EXP; unconditional BO factorisation; the over-tempered clause T16(iv) under V≤: analytic premises not established. UA. EXP is now an explicit hypothesis (T22).
- T14-H's one-move-addition iid-cheap clause for all polynomial p: factor-n error (J7). LF. Corrected scale N_e(T+L+5)/(p√n) in T21.
- Initial-base cancellation products, normalised mass inferred from mode status, unqualified V_δ window: normalisation and sequential conditioning missing (J7). UA. Replaced by T27's sequential law.
- BOCC-only emptiness theorem (T21-X) and its universal contrapositive "every loss instance violates SE, BM or bounded occupancy": BOCC supplies neither LK, EXIT nor multi-extra GAIN. UA. Kept only in the T24-conditional form (T30, optional; lead's ruling 61).
- T21-E's necessary temperature threshold φ*_n (via the slot argument): route broken by J4. UR. Returnable once an interference-controlled repair argument exists (lead's ruling 58).
- Selected-model fixed-atom certificate exp(−Q_fπ₀(Ŝ)) as a competitor certificate; fixed final E2; "checks pass" inferred from coupling alone: selection and information restrictions missing (J7, J8). LF. Replaced by the simultaneous certificates (T31(v)).
- Universal memory ceiling p_max = Θ(√M₀) (T23-S): the exact branch precedes Gram construction (J9). LF. Replaced by branch-specific statements (T34).
- Discrepancy range bound (n+K) log(n+1) and the "unreachable below 10¹⁷" cutoff; gap-only STIFF: duplicated predictors across blocks accumulate gains; mass matters (J9). LF. Replaced by T35.
- T8's NUM-based completion-conditioned coverage: NUM gives no coverage for implemented evidence. UA.
- Automatic population-to-empirical stage-count transfer; clean flags; schedule completion: retained as obligations (OP-s), not consequences. UA.
- Old non-crossing-kernel negative arguments; the no-grid ablation rate (−½ log n): not results about the actual hybrid v3 method. UR.
- External minimax/literature-transfer claims without opened primary sources: only the stated benchmark comparisons remain. UA (UNVERIFIED).

## Remarks without theorem files (returnable)
- R-T20(i), fixed-p start masses: with a normalised mass law n^{−c/2}e^{O_P(1)}, iid discovery is certain for c ≤ 2 and fails for c ≥ 3; exponential deficits fail for every polynomial budget. Counterfactual: fixed p eventually takes the exact branch. The "no proxies / proxy" classifications do not establish the mass law for v3.
- R-T20(iii), cap crowd-out: the cap blocks additions but not swap proposals or their scores (probability 1/(p−K) per uniform swap for a specified outside coordinate; scans score every feasible swap). The old singleton-block construction is incompatible with the actual partition; no family adopted. Open construction.

## Optional research ideas recorded, not theorems
- V≤ (deletion-loss ordering), OT-lb (over-tempered mass floor), NA(ψ̄) (noise alignment, UNVERIFIED): optional rate routes for the no-switch evidence; superseded by the first-moment route.
- The random-design lemma for NL_avg in iid Gaussian designs (UNVERIFIED).
- The design-to-partition lemma (CHANGE_PLAN 16).
- PW2 for the actual hybrid particle system; a complete regression loss family satisfying calibration avoidance and coupling; schedule-completion probabilities under the finite bisection; validated numerical error bounds; a genuinely useful external evidence bound.
