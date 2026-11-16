L2 line check — sha256 P6_DISTC.md 1f28367e39d34090 COR_C.md f0c43732da9acefd

Scope and result

I read both proof files in full, including their final Amendments sections, the permitted target statements, W3-SAMP/STATEMENT.md and CC_code_check.md, the six permitted code files as needed, and the check script and recorded outputs in D_output. I treated DIST-1, DIST-2, DIST-3 and Theorem A as given. I read no other ticket material, ran no git commands, started no agents, and wrote only this report.

No CRITICAL or MAJOR defect was found in the main deterministic transfers or their W3-SAMP delivery route. The findings below concern remaining literal inaccuracies, one short properness argument, and reader wording. Verification is under EX-A and H-ID, with the stated delivery premises; it is not a floating-point or completion-probability guarantee. The proposed corrections to STATEMENT.md must be carried into the statement before its original wording can be accepted literally.

Findings

L2D-01 — MINOR — COR_C.md §5, lines 156–157, unchanged by amendment A-2; also §4 row 1.
The opening still says the method “computes the posterior by a sequential Monte Carlo sampler.” The inspected code returns selected models and summaries; neither the full exact posterior nor the corollary's restricted parameter posterior is computed. The later phrase “Π̂ — not computed by the method” correctly distinguishes the mathematical object, but the opening can still tell an outside reader that the method computes the full posterior. §4's unconditional “OK as worded” does not resolve that overstatement. Minimal repair: say “The method uses sequential Monte Carlo to explore the model space and compute posterior summaries.” Keep the explicit mathematical definition of Π̂ and the statement that it is not computed. Amendment A-2 otherwise gives an understandable, accurate description of the list: final-run scores plus the specific earlier models carried into the final ledger, not everything ever scored in calibration.

L2D-02 — MINOR — P6_DISTC.md §4 Lemma M, lines 219, 237–238; amendment A-3, lines 464–465.
A-3 offers the first initial draw as an alternative justification for “∅ ∈ 𝓜.” Scoring an initial draw establishes that 𝓜 is nonempty, not that its member is the empty model: that draw can be a singleton. The table argument establishes empty-model membership if a valid block table exists; the draw argument does not replace it. Moreover nonemptiness is used later by Corollary R1 and Lemma W, so the needed distinction should not be left as “No proof step depends on it.” Minimal repair: state “𝓜 ≠ ∅ because the first initial draw is scored and offered; if a block table exists, ∅ ∈ 𝓜 as well.” Use only nonemptiness downstream. This leaves retention and every transfer unchanged. This is a defective fallback inference, not a constructed counterexample to empty-model membership for the public setup.

L2D-03 — MINOR — P6_DISTC.md §2 pin P6; COR_C.md RC-2, lines 23–26.
The description of non-completed runs says estimates are NA without qualifying the LS0 setting. v3_run.R:143–148 calls v3_unavailable_estimates only if v31 is true; with LS0 disabled it returns early with unavailable estimate fields absent rather than necessarily present as NA. RC-2 also says completion requires LS0 to finish, although cpp/v3_core.cpp:465 makes LS0 optional. P6 amendment A-7 correctly recognises the latter qualification but does not correct the unconditional pin or COR_C RC-2. Minimal repair: say estimates are unavailable, with explicit NA placeholders when LS0 is enabled, and say “the final local search and, when enabled, LS0.” No completed-run theorem changes.

L2D-04 — NIT — COR_C.md §1, line 84.
The first display is said to hold for “any subset of Ω,” but the restricted posterior is undefined for the empty subset: its weight denominator is zero. Minimal repair: “any nonempty subset of Ω.” The returned store is nonempty, so this does not affect C1.

L2D-05 — MINOR — P6_DISTC.md §0, Positivity.
The sentence infers m(S) ∈ (0,∞) from integration of a strictly positive likelihood against a proper prior. Positivity follows this way; finiteness does not follow from properness alone when likelihoods are unbounded in the variance. The stated IG prior with positive rate does supply the missing bound here. Minimal repair: with a = 0.01 and b = 0.01 s_y² > 0, bound the conditional Gaussian likelihood by (2πv)^(−n/2), integrate the proper coefficient prior, and use E_IG(a,b)[v^(−n/2)] = b^(−n/2) Γ(a+n/2)/Γ(a) < ∞ (or the corresponding centred likelihood dimension). This completes the claimed finiteness without a new assumption. The exclusion of constant responses is accepted from the stated setup; its preprocessing implementation is outside my permitted code list.

Mathematical line checks

• P6(a): each summand is nonnegative; multiplying Q(S) ≤ Lπ(S) by the conditional probability and summing proves the claim. No independence or stream premise enters.
• P6(b): the bad-model threshold is strictly positive; the displayed non-strict lower bound is valid even though the defining conditional probabilities exceed a strictly. Division by a is legitimate.
• P6(c): the piecewise Gaussian parameterisation is jointly measurable for fixed data. Tonelli normalises the predictive mixture; concavity of square root gives the affinity inequality in the correct direction. With the specified convention d_H² = 1 − affinity, the final bound is ε² + Q(A), without an extra factor two. The arbitrary predictor law causes no problem because the reference measure is ν_x ⊗ Lebesgue.
• C-0 and Lemma W: normalisation cancels Z, giving π_𝒯(S) = π(S)/π(𝒯); singleton domination also holds. Only nonempty stores and positive, finite posterior masses are needed for the denominators. Strict inequality π(𝒯) < 1 uses the public SMC branch restriction, not the retention invariant itself.
• C-i° and C-i: on the data event 𝔊_n(t), the failure event is empty for every qualifying completed run. Dividing by π(𝒯) ≥ a gives ϱ_n/a, also for a measurable random threshold by pointwise application. Predictive control follows by P6(c), since being outside B_n implies the distance bound irrespective of the size clause. The probability bound uses only the data marginal. “Any random variable” should retain the usual measurability requirement already stated in SCR-2.
• C-ii(α-det): π(S₀) > 1/2 makes S₀ the unique score maximiser, so its offer guarantees its retention and the reported HPM. This does not require discovery, mixing or an ideal stream. The strict inequality in α′ is correct, including its separate zero-posterior-bad-mass case.
• C-ii(α-disc): completed ⊆ 𝒜 and PC give inclusion in the potential island's missed-model event. Integrating D-i conditional on the data and calibration yields E[1_𝒜(1−π₀(S₀))^D_r]; (1−a)^D ≤ exp(−Da) gives the next bound. Setting Q_D = ∞ off 𝒜 handles unsuccessful calibrations correctly. Convergence in probability of the bounded variables exp(−Q_D) implies convergence of their expectations (boundedness/uniform integrability; no almost-sure convergence is needed). P-OVL, rather than P-MAP, supplies discovery.
• C-ii(β) proves no store-mass guarantee. The reported evidence estimate is not the exact normalising constant. I found no hidden assertion that P-STORE is discharged.
• C-iii(a,b): Markov's inequality over model masses yields π(𝔅_n) ≤ sqrt(ϱ_n). The offered-model threshold makes π(Ŝ) exceed that entire bad-model mass, a contradiction if Ŝ is bad. The argument remains on 𝔊_n(t), and the probabilistic version remains intersected with completed and P-HIT.
• C-iii(c) and C-iv: on the respective equality event the conditional parameter posterior is exactly the oracle posterior. Conditioning on design and then adding the failed-design-event probability gives the stated oracle bound. MPM outside Ω is not assigned a conditional parameter posterior; this is harmless on MPM = S₀ ∈ Ω. PC transfers the potential MPM error bound to the reported completed output.
• The DIST-2 remark is valid with its own constants and stated radius C√(tℓ_n/n). The oracle clauses continue to require DIST-3; they are not supplied by DIST-2.
• COR_C C1 follows directly from Theorem A(i) on the one data event defined in §3; division gives exactly n^(−cM/2). It holds simultaneously for all completed runs without a union over streams. C2 is deterministic retention. The response-scale parameter mapping preserves the attached density. COR_C amendment A-1 properly prevents the illustrative “relation to DIST-C” paragraph from conflating Theorem A's rescaled constants with the raw DIST-1 constants.

Store, cache and counterexample checks

The induction in Lemma R matches the actual sequence of operations: full-store quick rejection, equivalent-entry rejection, insertion, then deletion of the worst entry. With exact deterministic scores, equivalence under TopCmp{true} is precisely equality of models. A previously evicted duplicate cannot re-enter because at least k currently better elements precede it. Equal scores are resolved by size and then lexicographic order; an equal-score but better-ranked new model can enter. The induction's three cases exhaust the offers. HPM and top-store receive the same offers on completed runs: the sole extra offer_hpm call is inside the numerical-failure catch.

Lemma M's cache argument is sound with amendment A-2. The final cache begins empty; every cache insertion is in eval. Its only final-run non-emitting evaluation is of the already-offered running HPM. Initial particles and accepted proposals originate from emitting evaluations; resampling copies such particles. A rejected scored proposal also reaches the ledger, and a cache clear cannot remove an already-made offer. Table ingestion and inherited rescoring feed the same ledger. There is no path here by which a first-time island evaluation is silently omitted from the offered set.

I attempted a counterexample through adversarial sequences of offers, including duplicates after eviction, full capacity, exact score ties across different sizes, lexicographic ties within a size, and a unique maximiser arriving late. I reran the supplied script: 3000 store/retention trials and 2000 P6(a,b) trials passed, matching the recorded output. I additionally enumerated all 3-valued score assignments on the four models ∅, {0}, {1}, {0,1}, every length-five offer sequence, and capacities 0 through 4: 414720 sequences and 2073600 prefix checks passed. This is an in-memory model of the inspected comparator/offer code, not a compiled-C++ or full-regression run. The written induction supplies the general-capacity argument. I found no sequence contradicting retention under EX-A. The first-draw singleton exposes L2D-02's inference, not the retention claim.

Independent code-pin sample

All paths below are relative to Scripts/SMC_BVS/core. These checks exceed the required twelve pins.

| Pins | Inspected code | Result |
|---|---|---|
| P1 | v3_run.R:142 | HPM copied from ledger. |
| P2, P3 | v3_run.R:159–163 | Equal-island PIP average; MPM uses strictly > 0.5. |
| P4 | v3_run.R:150–154 | Pooled evidence is the arithmetic mean on the evidence scale. |
| P5 | v3_run.R:210 | Returned top_store is led$top. |
| P6 | v3_run.R:143–149 | Early return and partial ledger confirmed; NA wording needs L2D-03. |
| P7 | cpp/v3_core.cpp:358–366 | Comparator-order models, stored values, capacity/full metadata. |
| P8, P10 | cpp/v3_ledger.h:43–64 | Empty init and offer/eviction operations agree with induction. |
| P9 | cpp/v3_ledger.h:76–79 | Capacity 40p + 1 and HPM-order comparator. |
| P11 | cpp/v3_ledger.h:35–42 | Score, then size, then lexicographic order. |
| P12, P13 | cpp/v3_ledger.h:84–112 | Same offers to HPM and top; fresh-only store updates. |
| P14 | cpp/v3_util.h:117–126 | Lexicographic comparison and HPM order agree. |
| P15, P16 | cpp/v3_engine.h:89–105 | Cache/score formula, emission and nonfresh held event. |
| P17 | cpp/v3_engine.h:379–382 | Centre emission flag is passed to eval. |
| P18, P19 | cpp/v3_core.cpp:372–409 | Table ingestion, new ledger, empty final cache. |
| P20 | cpp/v3_core.cpp:418–429 | Inherited models checked against K, rescored and offered. |
| P21 | cpp/v3_core.cpp:443–452; v3_run.R:90–91 | Four final islands, streams 10–13, nullptr initial states; partial run stops. |
| P22 | cpp/v3_core.cpp:453–484 | Final search, optional LS0, guards and failure status. |
| P23 | cpp/v3_core.cpp:488–507 | Extra HPM update occurs only on numerical failure. |
| P28 | v3_fit.R:120–132; cpp/v3_core.cpp:536,556 | Separate exact status and return. |
| P29 | v3_fit.R:154–171 | Unsuccessful calibration prevents final run; final fields copied. |
| P30 | v3_run.R:121,218 | Raw status copied; available-estimates flag on completed path. |
| P31 | cpp/v3_core.cpp:341–348 | Summary records returned, no particle states. |
| P33 | cpp/v3_engine.h:116,397 | Gibbs/local additions respect K. |

The current SHA-256 hashes of all six permitted code files match their entries in pins_sha256.txt. I did not independently recheck pins P24–P27 or P32 at their excluded source files (v3_score.h, v3_preprocess.R, v3_start.h), or v3_setup.R's orig validation. Their relevant facts are inherited from the supplied setup/CC statement where available, not newly code-verified here. v3_fit.R:118 and cpp/v3_core.cpp:24–41 do independently confirm the retained-index input and returned-index conversion. I did not verify historical commit identity.

Joint law and delivery-premise audit

P6 §5 gives the correct two probability levels: data marginal P*, and, only for delivery, ideal within-stream uniforms and independence of each final stream from data/calibration. Mutual independence of the four final streams is not used. J requires only the marginal identity. The asymptotic errors are joint events, never probabilities conditional on calibration success or completion. No completion probability tending to one is assumed or obtained.

The delivery table matches the supplied W3-SAMP statement: D-i uses EX-A, H-U, START, KERNEL's control-flow clause, CAL, SI and MEAS; PC supplies completed/potential agreement; discovery's limit adds P-OVL. HPM identification via D-iv adds P-MAP or P-CONC. LT-e adds P-CONC and all four NC_r premises to the N1 premises; C-v uses 1_𝒜 δ̄ → 0; TR-d uses P-CONC and P-OVL∞. Their N1 premises include POT as recorded. C-iv uses PC(ii) before passing from potential MPM to a completed reported MPM. The design-measurable retained S₀ is fixed under conditioning on the data. The impossible-model convention gives a trivial discovery bound outside Ω; P-OVL or P-CONC excludes those successful-calibration configurations asymptotically when needed.

The RM2 route is NOT independently verified: neither the event-containment link nor equality of its Ŝ⁺ with the returned hpm was checked, and its source files are forbidden by this brief. Amendment A-1 appropriately removes it from every proof dependency. Acceptance of C-ii below covers the W3-SAMP route and explicit membership premise; it does not validate STATEMENT.md's alternative RM2 citation. No assertion about those unchecked links may be promoted to a proved delivery statement.

SCR-1 through SCR-5

| Request | Disposition and effect |
|---|---|
| SCR-1 | Justified. A majority alone does not imply mass > sqrt(ϱ_n) for all finite n. Adding ϱ_n ≤ 1/4 supplies the implication; enlarge n₀ accordingly. This restricts an originally false sufficient-condition sentence, not P6, C-0, retention, or the P-HIT transfer itself. |
| SCR-2 | Justified. λ = 0 imposes π(𝒯) ≥ 1, not ≥ η. The arbitrary-positive-threshold formulation proves the intended fixed-fraction bound with ϱ_n/η. It extends the valid transfer and does not weaken it. |
| SCR-3 | Correct editorial repair: the probability-level definition is in SAMP §0. |
| SCR-4 | Necessary. The literal complement includes stopped runs and insufficient-mass runs. Restricting the predictive clause to completed ∩ sufficient mass ∩ small restricted bad mass states what the proof establishes. It narrows an invalid literal scope, while preserving the full valid deterministic predictive transfer. |
| SCR-5 | Sensible notation repair; no mathematical effect. |

C-i° is a valid strengthening to a single data event controlling every eligible completed run. None of these requests weakens the domination inequality or the deterministic selection/retention result. The original unamended statement's false threshold and success-event readings should not be described as already proved verbatim.

Verdicts per item

| Item | Verdict |
|---|---|
| Lemma P6(a) | VERIFIED |
| Lemma P6(b) | VERIFIED |
| Lemma P6(c) | VERIFIED |
| DIST-C (C-0) | VERIFIED |
| DIST-C (C-i) | VERIFIED-WITH-AMENDMENTS — SCR-2 and SCR-4 must accompany the statement. |
| DIST-C (C-ii) | VERIFIED-WITH-AMENDMENTS — A-1 excludes the unchecked RM2 route; correct A-3 as in L2D-02. |
| DIST-C (C-iii) | VERIFIED-WITH-AMENDMENTS — SCR-1/A-5 for the majority-to-P-HIT implication. |
| DIST-C (C-iv) | VERIFIED |
| Corollary C | VERIFIED-WITH-AMENDMENTS — apply A-1/A-2 and correct L2D-01/L2D-04; the two principal conclusions are proved. |

The shared positivity proof needs the short completion in L2D-05; it introduces no additional hypothesis. L2D-03 corrects ancillary code descriptions, not the completed-run statements. These verdicts accept the supplied upstream hypotheses and do not upgrade their status or the uninspected code pins.

Overall verdict: VERIFIED-WITH-AMENDMENTS.
