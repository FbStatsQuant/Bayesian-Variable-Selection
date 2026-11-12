VERDICT: DESIGN_v1 rev 2 UNSOUND
Section 4.1 does not satisfy the binding output-equivalence ruling and is not yet a complete worker/merge specification.

Reviewed committed HEAD b2c0194345b41a2e85bc81d963e58c114c5ff5c3. No other review file was opened. Paths below are repository-relative unless explicitly absolute; line numbers refer to this commit.

## Findings, most severe first

### 1. CRITICAL — Published fresh counts are excluded from equivalence; aggregate worker records cannot reconstruct them

**Place:** DESIGN_v1.md:84–88, O17.

**Evidence:** `RERUN_SPEC.md:78,156–163,202` requires fresh/logical counts, including phase attribution; `Scripts/Campaigns/2026-10-28_New_Campaign/analysis/H2_20261102/scripts/evidence_h2.py:98–105,139–141` uses fresh totals in `ev_cost.csv`, scaling exponents, and mechanism/phase shares. The lead has already ruled that these must match. O17 is not awaiting a reporting exception.

`Scripts/SMC_BVS/core/cpp/v3_score.h`, `ScoreCache::insert`, clears the entire cache on a **miss insertion when count is already capacity**, not immediately upon reaching capacity. A previously scored model can therefore miss again. `profile_v31_step_cost.tsv` records 479, 565 and 127 clears: this is not a hypothetical corner case. “First scored by another island is a cache hit” is false after eviction.

Distinct sets or first-score counts are insufficient. With capacity 2 and an empty cache, traces `A,B,A,C,A` and `A,B,C,A,A` have identical distinct sets and first-discovery order but respectively 3 and 4 misses. Worker-local cache traces also depend on a different incoming state from the serial island.

**Fix:** require an exact serial-cache replay contract. Record every ordered cache lookup, including worker-local hits, with collision-resolved model identity and phase/mechanism; record scorer route/Q-recomputation information where route totals must be reconstructed. Replay in global island order with the original capacity and eviction rule. Include non-emitting lookups, notably the final-search centre, and continue the replay through both searches. Preserve setup/calibration/inheritance contributions exactly once. Report physical worker work separately from serial-equivalent published totals. Budget trace storage and replay time before calling this build-ready. A serial reference rerun is an exact but expensive alternative; unique-model unions are not.

### 2. CRITICAL — N1 expressly excludes the shipped RB records

**Place:** DESIGN_v1.md:179, O1(c), supporting §4.3.

**Evidence:** `Theory_work/Wave1/W1-N1/STATEMENT.md` §1 defines H as the plain four-endpoint average; §5 explicitly excludes “Rao–Blackwellised records.” The permitted external `f01.md` (b)(i) extends population averages, not Gibbs conditional averages. Thus “the shipped Rao–Blackwellised PIP is covered by N1 only for the four measured rounds” contradicts the cited statement.

**Fix:** distinguish N1's general plain-summary identity from the RB identity. Cite the separate RB theorem/code bridge, or require a bridge for the actual measured Gibbs records too: each prefix kernel preserves the target and the recorded conditional inclusion probability integrates to the marginal. Do not present that bridge as already supplied by N1/f01. Carry exact-arithmetic/ideal-stream premises into §4.3.

### 3. CRITICAL — Leader stores are returned statistical objects, not calibration-only objects

**Place:** DESIGN_v1.md:84–85.

**Evidence:** `v3_ledger.h:100–105` updates both leaders on final events, and `v3_run.R:210` returns `leaders_gamma0` and `leaders_gamma1`. Discarding them contradicts “used only by calibration” and the broad equivalence contract.

**Fix:** emit and merge each worker's top-20p leaders using its own comparator, then update them during the merged tail. Gamma-0 leaders cannot generally be recovered from top-by-F. Gamma-1 uses F with lexicographic ties, whereas the main top store uses size then lexicographic ties; do not silently substitute one order for the other. If proposing removal, identify it as an output-schema change, not an identical implementation.

### 4. CRITICAL — The stated merge memory bound is false for a k-way merge

**Place:** DESIGN_v1.md:80–81.

**Evidence:** A streaming R'-way merge retains a head/cursor (normally a heap entry) per input, in addition to the output. Memory is O(c + R') entries/metadata, with model lengths and I/O buffers also charged, not independent of R'. Lemma S proves retained-set equality, not the memory bound.

**Fix:** state the actual bound, or use bounded-fan-in/pairwise external merging. A sequential running top-c union uses O(c) model storage independent of R', with a different work/I/O tradeoff. Both preserve the exact total tie order.

### 5. MAJOR — The tail and distributed status contract are not specified sufficiently to implement

**Place:** DESIGN_v1.md:69–93; O6/O17/O20/O21.

**Evidence:** `v3_core.cpp:453–481` snapshots `hpm_before_local`, runs final local search from the merged winner, snapshots `hpm_before_ls0`, constructs the start mode, then runs LS0 with the configured cap. `v3_run.R:173–212` derives near ties, certificates and flags from the completed result; E3 excludes LS0. Merely budgeting a “serial tail” does not specify this state transition. The existing complete-fit runtime pointer cannot be transported to separate processes. `v3_run.R:106–116,141–150` suppresses estimates after incomplete output; O6's sentence does not define orchestration statuses or the new fields' suppression.

**Fix:** prescribe that exact tail once, after all manifest islands and store merges, on a fully populated ledger. Preserve inherited HPM provenance replacement, exact start-mode tie handling, final-search cap ell, LS0 cap ell + mode size, and both snapshots. Continue serial-equivalent cache accounting through the tail. Declare task/whole-fit budgets, retry policy, terminal status precedence, handling of killed/missing tasks and merge failure, and atomic publication. Never aggregate only successful islands. Clear every new estimate/SE/weighted-PIP field on non-delivery. State equivalence on common completed runs/potential records; parallel and serial wall-clock guard decisions need not coincide. Physical wall-time tables need explicitly different semantics, not an exact serial-timing claim.

### 6. MAJOR — Worker and stream contracts omit necessary validation and index mapping

**Place:** DESIGN_v1.md:69–77; O18.

**Evidence:** `Ledger::event` indexes `island_best[ev.island]` only when the global id is <= `islands`. A one-island ledger with global id r > 1 silently loses that island's maximum. `v3_run_settings` takes N from setup budgets, rather than simply accepting `frozen$N`. `v3_randomness` hardcodes streams 0:13. A census stream `2^31+c` also exceeds signed R integer range, and no domain for c is given.

**Fix:** declare local slot versus global island id, N/L/Hm/tier source, immutable input schema, and hashes covering data/index mapping, setup, scorer binary/numerical environment, tables, frozen settings and inheritance. Return the full `IslandResult`, terminal records and stream positions, not an ambiguous subset. Require `0 <= c < 2^31`, global uniqueness across census candidate sizes/batches, no reseeding on retry, checked uint64 stream construction and an R representation that retains values above 2^31-1. Generate metadata for the actual manifest. Retain the final bound and O18's independence premise; disjoint labels alone do not prove independence.

### 7. MAJOR — The variance comparison in the reserved decision table is not valid in general

**Place:** DESIGN_v1.md §7(ii), “grows with the dispersion of omega”; §4.3:117.

**Evidence:** The variance coefficient is E[omega^2(H-mu)^2] under the identity. Weight dispersion alone does not order it: constant H gives zero variance for any dispersion; dependence between H and omega matters. This unsupported monotonic claim steers the reserved comparison. The displayed SE squared estimates Var(mu-hat) approximately sigma_h^2/R', not the CLT variance sigma_h^2 itself.

**Fix:** say “depends on the joint law of evidence and the island summary”; retain weight ESS as a diagnostic, not an estimator-specific precision guarantee. Label the variance scale correctly and the bias expansion as asymptotic (the table currently omits its higher-order remainder). The sign/coefficient of the leading bias and the displayed SE formula are otherwise consistent with the iid ratio delta method. Neither N1 nor f01 supplies empirical many-island precision evidence.

### 8. MAJOR — Census inheritance and the localisation event are left ambiguous

**Place:** §4.5; O1(b), O3, O21.

**Evidence:** v0 O3 explicitly includes census models inherited into stores for G1/G2/L3. Rev 2 gives no such transfer/provenance policy. In addition, f01(a)(1) uses E0 = calibration success intersect {r <= R'}, not the delivered-output event. `W1-N1/lemmas/L3_freezing.md:8–16,34–42` makes this distinction explicit. Integrability only on delivered output is not the cited justification for potential-run conditional identities.

**Fix:** define the enlarged calibration record, whether census models belong to the all-scored set, and their canonical inherited provenance and counters. If they do, merge their stores before final work; if excluded, restate certificate semantics. Replace “on the output event” by the explicit E0 condition, or explicitly choose the regular-conditional-law interpretation. O19's Markov bound is correct for potential evidence with calibration-measurable R'; it does not license conditioning on delivery. Keep the ideal infinite-island asymptotic distinct from the finite implemented stream namespace. O7/O9/O12 from v0 are not triggered by the proposed unchanged kernel/scorer but should be labelled inactive rather than silently disappearing from the obligation inventory.

### 9. MAJOR — Some empirical conclusions exceed the measurements

**Place:** DESIGN_v1.md:21,55, §8.

**Evidence:** The calibration share median is 0.4536 at p=500; the tier-0 ranges are 0.3132–0.6395 and 0.2997–0.6881 (`leg_a_units_calibration_summary.tsv`). “Calibration is half of a fit or more” is not a general consequence. Aggregate per-step timings do not isolate bitset-copy cost, so “not visible up to 20k” is not an attribution measurement. §8 says process-parallel islands make 10k–20k fits deliverable, although only one final N=2500 island was measured at 20k and calibration remains a sequential bottleneck.

**Fix:** give the observed shares, say no separate copy-cost measurement was made, and make delivery at 10k–20k a validation target with task decomposition/budgets. Keep the existing qualifications on one seed/design, R=4, 5k diagnostic versus final islands, and the unfinished 5k final run. No final 5k dispersion result can be inferred from the calibration.

### 10. MINOR — Scan counts, source precision and per-fit ratios need correction/definition

**Place:** DESIGN_v1.md:23,89–90,135.

**Evidence:** `v3_engine.h:394–399` skips infeasible additions at k=K. Thus p+k(p-k) is an upper bound; the actual full scan is k+k(p-k) there. LS0 also emits its initial centre. The 109k/2.2M scanned-model counts are absent from the permitted TSVs; the phase table supplies times only. The claimed 0.3–13 ratios reproduce **last same-tier diagnostic/final** ratios (0.312715–13.426621), not per-fit median-diagnostic/final ratios (maximum 16.879689). Round C's minimum timed score is 134.0 us, not 135; including the profile gives a 20k LS0 charge of 933.703 h, below the quoted 936 lower endpoint.

**Fix:** label the scan expression an upper bound, provide scan-count source rows, define the diagnostic iteration used in the ratio, and label the setup-only versus all-run ranges. These small discrepancies do not explain the architectural failures above.

## Field-by-field equivalence required by 3(c)

“Yes” below assumes identical deterministic scores, streams, settings and completed tails; it is not a claim of matching wall-clock admission. “No consumer found” is limited to the permitted published-study sources, not proof of absence elsewhere. Paths `core/*` below mean `Scripts/SMC_BVS/core/*`.

| Field | Published table or theorem check? | Exact in independent workers plus specified merge? | Required record/action |
|---|---|---|---|
| log_Z, log_Z_r, lower95, PIPs, RB, MPM | Yes: RERUN_SPEC A1; TH01 | Yes, with canonical island ordering and unchanged R arithmetic; weighted PIP is an additional output | Full island summaries, RB arrays, log increments and manifest; retain shipped primary pending owner decision |
| score_counts$logical | Yes: RERUN_SPEC:78,163; extract_h2.R:65 | Yes for islands; tail underspecified | Phase/mechanism matrices; count tables once and replay exact tail; inherited offers are not ledger events |
| score_counts$fresh | Yes: ev_cost.csv and phase/mechanism shares, evidence_h2.py:98–105,139–141 | No | Ordered collision-resolved lookup trace and serial-cache replay, including tail and non-emitting centre calls |
| cache | No direct table/theorem consumer found; required to reconstruct fresh cost | No | Replay capacity, hits, misses, inserts, clears, terminal cache state; label physical cache totals separately |
| numerical_routes, q_recomputed, failures | No direct H2 table consumer found; numerical implementation audit/identity diagnostics | No | Per-model route/Q data on replay misses, plus once-only setup/calibration/inherited scorer calls; include scorer calls outside ledger events (`v3_fit.R:83`, `Scorer::score`) |
| hpm/model/F/provenance | Yes: extract_h2.R:58–60; TH05/SR | Pre-tail yes under the interpretation below; full output needs tail | Winner EventCtx plus mechanism, exact inherited provenance restoration, deterministic tie order, search events |
| top_store, near_ties/F/truncated | Yes: TH04/SR; RERUN_SPEC:65 | Pre-tail yes; full output needs tail | Sorted top-c with full/cap metadata, exact comparator/deduplication; recompute near ties after LS0 |
| hpm_before_local / hpm_before_ls0 | Yes: RERUN_SPEC:75,89; extract_h2.R:76–78 | Not specified completely | Snapshot merged HPM before final search and again before LS0 |
| island_best | Yes: feeds E1 and recovery diagnostics | Yes with correct global-id/local-slot mapping | Own-island maximum across all logical scored events, including hits/held states; never copy worker ledger HPM into it |
| flags E1/E2/E3, low ESS, local-limit/certificates | Yes: RERUN_SPEC:65,75,156; local certification theorems | Not completely specified | E1 against post-LS0 HPM; E2 across all final evidences; E3 pre-LS0 versus pre-local; exact archives/caps and completion states |
| stage_table / terminal_table | Yes: min_ess, A1; stage/kernel checks | Yes if complete records retained | Stage moves, distinct counts, ESS, grid/rho labels, terminal moves, global ids; prepend calibration records once (`v3_fit.R:163`) |
| leaders_gamma0/1 | No direct H2 table consumer found; returned statistical stores | No: deliberately discarded | Merge both leader stores by their own total orders and run tail updates |
| timings / status | Yes: runtime column in ev_cost.csv; GUARD-W output event | No | Actual per-task/total wall and CPU times, explicit parallel budget/status semantics; no promise of identical measured serial elapsed time |

## HPM and top-store edge cases: what the specified rule can actually establish

For the **pre-tail winner**, no counterexample to canonical provenance was found under the deterministic scorer and identical initial ledger. `hpm_better` (`v3_util.h:121–125`) is the strict order F, smaller size, lexicographic model; the same model does not replace its provenance. A worker that encounters the global winning model cannot finish with a strictly better worker HPM, since that would contradict global maximality. Select the earliest *actual source* of that winning model, not the smallest id of a worker carrying an inherited/table copy.

Tables precede inheritance in `cpp_final_run`; inherited HPM provenance is explicitly restored from calibration (`v3_core.cpp:428–440`). This restoration must survive the merge, even though its event phase/id looks like a calibration event. If the winner first occurs in island r and no earlier island scored it, use r's first event, not an earlier worker's maximum. Cache clears do not change first-winning provenance: stores persist, and repeated evaluations cannot replace the same HPM. Held states were already evaluated. A new winner found inside final local search or LS0 must instead receive that tail event's provenance; the pre-tail formula alone does not cover it.

Truncation at c is safe **including ties across the cut**, provided every worker uses the identical strict total comparator. Any discarded model has c distinct models ahead of it in that worker alone, so cannot enter global top-c. Duplicates in other workers do not invalidate those c distinct witnesses. Keep exact model identity for deduplication, not a hash alone. Fresh-only ledger updates do not break this argument: every cached model was previously offered to the same persistent ledger. Do not prepopulate a worker/tail cache with models that have never been offered to its corresponding ledger.

## Numerical reconciliation

Recomputed from the permitted TSVs and stated formulas; rounding is treated as rounding, not as a new error. This inventory separates numerical agreement from the unsupported interpretations above.

| Claims | Recomputed values / source |
|---|---|
| §1 step costs, fit approximation | Bridge 1.1360/1.1637/0.8958 us; terminal 1.638/1.899/1.803. Formula errors -3.1994%, -10.7704%, +6.2715%; 51.6/126=0.409524. Total/island 1028/124.9=8.2306, 3293/308.4=10.6777; approximate formula 8.30/10.76. |
| §1 stages/rebuilds/shares | 24-unit T range 26–40; medians 32.5/31; pilot range 20–30; rebuild ranges 2–8/2–10 and medians 4/6. Tier-0 share medians .4536/.5642; profiles .5096/.6240. `leg_a_units_calibration*`, `profile_v31_stages.tsv`. |
| §2 depth | T=35, N=p: .394313/1.574738/6.293920 h at 5k/10k/20k. Multiplying by 10.76–14.86 gives 4.243–5.859, 16.944–23.401, 67.723–93.528 h. Caps ceil(log2(n+p+1)) = 10/11/12/13. |
| 5k incomplete run | Total calibration 19443.8/3600=5.40106 h in phase TSV. Tier split 13261 and 6181 seconds is checkpoint-only (3.6836/1.7169 h); rounded split sums differ from total by 1.8 seconds. “Still running after 3 h” is checkpoint status, not a completed-fit measurement. |
| Setup/Gram and admission | §1/§3 values reproduce round A/C setup TSVs. v32 charges 5.792–7.018, 9.237–13.747, 18.760–18.789 h. Profile actual LS0 times .1079/.1591/2.0594 s. Refusal at 20–30k is an extrapolation, not an observed run. |
| §4.2 fixed-N hours | .179740, .358907, .717240, 3.583907, 35.833907. Calibration = island hours*(512/2500)*(1+4I): .7730–1.9510, 1.5436–3.8957, 3.0847–7.7852. 64/256 core-hour columns reproduce rounding; 1M*256=9173.4801. Measured 20k 2382.6/3600=.661833 h; pilot 2184/3600=.606667 h. |
| Census | 32*.661833=21.1787 core-h using the measured island; formula at T=30 gives 22.9517. Label which basis is used. |
| §4.4 dispersions | Final medians .06447695/.08756481/.04217928; maxima .16570382/.70312363; escalated .99730149/.82303727. Diagnostic medians .15413695/.18243994/.21878044; tie 5.7495–6.0779 and 4.1508. 5k .49260040–2.52041557, median 1.38501484, tier 1 1.55953769. Ratio of pooled medians 2.3906/2.0835; 2k 5.1870; sqrt(2500/512)=2.2097. |
| Weight diagnostics/PIP comparison | Rounded TSV minimum R_eff/4=.5975 (claimed .597 is compatible with unavailable unrounded precision); 20/25 >=.97; max weight .583; max difference .00230, median .0000903; maximum reported diff/SE=1.3335; all 25 MPMs equal. The SE ratio is evaluated at each fit's largest absolute-difference coordinate, not maximised over all coordinates (`analysis/pip_weighting.R`). |
| Log-normal approximation/P6 | exp(-sigma^2)=.991933/.939413/.612626/.367879/.018316; at 1.4=.140858. P6 n=50 counts 0/137, 2/40, 13/105, 6/16; flagged/escalated intersections at p>=250 are 13 and 6. |
| Memory | 24/16/8 p^2 at 20k =8.940697/5.960464/2.980232 GiB; at 100k =223.517418/149.011612/74.505806, condensed 37.252903. 16*(50k)^2=37.252903 GiB. 251 GiB distance-only ceilings 183545/259571 predictors. Profile peaks 5531.6/1024=5.4020 and 6455.6/1024=6.3043 GiB. |
| §4.1 arrays and §7 costs | At p=1M,R'=256: 10,240,000,256 store entries; PIP=1.907349 GiB, five RB arrays=9.536743 GiB. Two particle bit arrays: 232.830644 versus .582077 GiB. T=30,N=p hours at 10k/20k/100k/1M: 1.435627/5.737920/143.356267/14333.562667 (5.973 days/1.636 years). 24h thresholds approximately 40912 and 669751 predictors. |

Source limitations: the 109k/2.2M scan counts and their per-model timings lack inspectable count rows in the supplied tables; 251 GiB node capacity is a planning input rather than a benchmark measurement; hardware/toolchain claims and the 5k tier timing/status split rely on the narrative checkpoint. The TSVs are rounded exports, not raw fits. The final 5k fit remains incomplete in this review's evidence. No contrary many-island or high-p precision conclusion follows from their arithmetic.

## Concrete replacement for the next engineering step

First freeze a no-census, unchanged-N, unchanged-primary R'=4 worker-equivalence contract. Use immutable worker inputs and full island records, exact store/provenance merges, and a dedicated canonical cache-accounting replay followed by the two serial searches. Include adversarial checks for inherited/table winners, later-island winners, exact ties across top-c cuts, repeated cache clears, hidden centre lookups, both search phases and stopped tasks. Expand R' only after that contract passes. This preserves the owner's two decisions while making the already-authorised implementation and published cost equivalence reviewable.
