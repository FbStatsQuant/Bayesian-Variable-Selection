# A1 — Proposition F adversarial audit

**Verdict: HOLDS-WITH-AMENDMENTS.** No counterexample found to Proposition F with its stated LS0 cap `ell_n`. The fallback eliminates the remaining delivery obstruction in the stipulated ideal machine/configuration. The requested combination with C-GROW needs an amended resource bound and allocation; the current quantitative Lemma R does not cover that combination verbatim. No FATAL finding.

## Findings

1. **MAJOR — C-GROW preserves polynomial resources, but the existing score-count and time envelopes cannot simply be reused.** C-DLV fixes LS0's cap at `ell_n` (`Theory_work/Wave1C/C-DLV/STATEMENT.md:12`, `:32`; `lemmas/L1_resources.md:25`, `:43`, `:50–52`). C-GROW instead requires `a_n = ell_n + |S_tilde_0| <= ell_n + K` (`Theory_work/Wave1C/C-GROW/METHOD_REQUIREMENTS.md:3–18`). Thus LS0 can perform up to `ell_n + K + 1` scans, not `ell_n + 1`. The corresponding line in the delivery proof is also specific to the smaller cap (`Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:38`). The implementation performs the extra complete scan even at the move cap (`Scripts/SMC_BVS/core/cpp/v3_engine.h:384–411`).

   Let `q(p) = p + p^2/4`. A sufficient correction is

   ```text
   score_requests_G <= Sigma_bar + K q(p),
   W_G := W_bar + C K q(p) [n^3 + p(n+2)],
   M_G := M_bar + C K(K+1),
   ```

   with a sufficiently large implementation-dependent constant `C`, using raw dimension in the envelopes as in L1 R.4. The work increment charges the extra requests at L1's own worst-case score-plus-cache/store cost (`lemmas/L1_resources.md:32–43`); the memory increment covers the additional LS0 path/scan-centre archive (`Scripts/SMC_BVS/core/cpp/v3_engine.h:46–52`, `:406–411`). `M_G` still has order `O((n+p)^2 + Cert_M)`. `W_G` remains polynomial, but the displayed old time shape is not justified by the old counting proof after this change: at `p` proportional to `n`, its core term is order `n^5 log^3 n`, while this sufficient extra-work term is order `n^6`. This comparison is a gap in the unchanged upper-bound argument, not a constructed runtime lower bound.

   **Required amendment:** update CONFIG, the LS0 row, score count, work/memory bounds and Corollary R's allocation together. In particular use `time_n >= 2(tau W_G + tau_0)`, as well as the exact-branch preflight-time bound. Merely saying that the new cap is polynomial does not establish that the old declared allocation prevents a guard stop. The fallback itself does not increase the stage bound.

## Independent exit audit

I re-traced the entry, setup, calibration, final engine, R assembly and supporting headers. The following checks did **not** yield another obstruction under the stated premises. Unqualified implementation paths are relative to `Scripts/SMC_BVS/core/`; `C-DLV/` and `W1-GEN/` abbreviate their ticket directories named above.

| Path attacked | Result and evidence |
|---|---|
| Entry/input/degeneracy | Seed and allocation errors are explicit (`Scripts/SMC_BVS/core/v3_fit.R:63–71`); data validation and constant-column/response returns are explicit (`v3_preprocess.R:97–115`). The class designs have nonconstant columns; Gaussian noise makes a constant response a null event. This is an almost-sure claim under model G, not delivery for every finite numeric input. |
| Preflight and setup | Both initial preflight and escalation preflight can refuse delivery (`v3_fit.R:88–90`; `v3_calib.R:148`). Corollary R covers them separately from actual memory. The timing context is built before preflight (`v3_fit.R:10–13`, `:83–88`), so allocation success is needed there too; L1 counts it (`lemmas/L1_resources.md:65–68`, `:95`). Setup/table scoring has the numerical-failure return (`cpp/v3_core.cpp:279–294`), excluded by EX-A, not by the fallback. |
| Calibration before grid failure | Pilot, diagnostic, V-rescoring and runtime failures still exist (`v3_calib.R:57`, `:80–81`, `:100`, `:112–113`). They are excluded by EX-A/MACH/allocation. Tier-0 grid failure forces escalation via `grid_failure` (`:82`, `:114`, `:145–149`); it cannot silently leave a tier-0 fit without a grid. |
| Final engine | The final run starts with `completed`; its explicit alternative statuses are `resource_limit` after a partial island or final local-search guard, and `numerical_failure` (`cpp/v3_core.cpp:404`, `:434–453`). These remain real failure paths with a fallback on an ordinary machine. Under Corollary R and EX-A they are excluded. No final ESS, convergence, E1–E3 or `local_limit` rejection is present. |
| Internal exceptions | Inherited indices/models/provenance come from the same calibration exporter (`cpp/v3_core.cpp:24–55`, `:413–430`, `:696–704`); models remain feasible. Setup pointers/classes are constructed internally. The engine's `nth_nonmember` exception requires an index outside the complement, whereas its caller draws below `p-|S|` (`cpp/v3_engine.h:134–151`). Exact enumeration's interrupt is real (`cpp/v3_core.cpp:520`) and excluded by MACH. No additional reachable logical exception was identified. |
| Pooling and assembly | Completed islands supply four finite log-evidence values and four length-`p` PIP vectors; log-sum-exp pooling and equal-weight PIP assembly do not reject a poor grid (`v3_run.R:117–135`). E1–E3, low ESS and `local_limit` only set flags (`:141–156`); completed assembly sets estimates available (`:166`). Under EX-A the bridge weights are positive and finite, so the resampling normalizer is positive (`cpp/v3_engine.h:234–240`, `:317–328`). |
| LS0, workers, merge, certificates, return allocation | These are not all shipped on the audited serial call graph. That graph hardcodes four final islands (`v3_run.R:87–89`) and calls only the global-best search (`cpp/v3_core.cpp:447`), not LS0. Their extension is conditional on CONFIG, OP-LS0/e4, TDP-IMPL and GUARD-W, with MACH excluding worker crashes, failed allocations and external interruptions (`C-DLV/STATEMENT.md:28–42`). Specified worker/merge/LS0 stops imply no output (`Theory_work/State_of_Project/sections/02_method.tex:392–406`, `:490–500`); they are excluded here by the resource/operational premises, not by an audit of a shipped LS0/parallel implementation. Polynomial certificate budgets are explicitly added and exhaustion is unresolved, not a fit stop (`:540–545`). The inventory correctly distinguishes these spec obligations from serial code facts. |

For the numerical exclusion, the key fact is positivity, not a property of calibration: `H=(n+1)G+I` and `A=G+I` are positive definite and `Q >= y'y/(n+1)>0`. Consequently the first Cholesky scoring route succeeds under EX-A (`cpp/v3_score.h:175–188`, `:204–237`; `C-DLV/lemmas/L2_degenerate.md:20–35`). Positive block masses also make every reachable start-sampler categorical well defined (`cpp/v3_start.h:100–174`).

## Pilot-grid and failure-branch attack

The pilot argument survives. In exact arithmetic, each non-final increment is at least `1/T_1`: the unforced branch returns `lo` only when it meets that floor, and the forced branch returns `min(1, phi+1/T_1)`, possibly snapped upward to 1 (`Scripts/SMC_BVS/core/cpp/v3_calib.h:30–45`). If the terminal step passes it returns exactly 1. Thus `0=phi_0<...<phi_k=1` and `(k-1)/T_1 <= phi_(k-1)<1` imply `k<=T_1`. The exporter prepends 0 (`cpp/v3_core.cpp:600–607`). A partial pilot is not a fallback candidate, but partial pilots are excluded here. All three final-grid checks pass (`v3_run.R:77–82`, `:173`); none checks restricted or empirical ESS.

An already successful construction likewise has endpoints 0 and 1, strict progress and at most `T_1` intervals (`cpp/v3_calib.h:68–98`). No L5 dominance/two-model assumption is needed for either fallback. Its restricted-ESS performance can be arbitrarily poor without creating another ideal-arithmetic final-run stop.

The patch must actually preserve a complete grid through the tier return and normal freeze. Currently **any** grid failure sets `out$grid=NULL`, including a failed rebuild after earlier success (`v3_calib.R:114–123`); the outer function then returns `schedule_limit` (`:153`). Changing only the status at `:153` leaves `NULL` for `v3_frozen` and fails validation (`:168`; `v3_run.R:69–80`). Select the last successful **tier-1** grid, or the completed tier-1 pilot if none exists, terminate that tier without retries, retain inherited state/tier budgets, and construct the ordinary frozen record/hash. Do not use the failed construction's partial prefix. This is implementation precision for the hypothesis “froze a valid fallback,” not a counterexample to that hypothesis.

## Calibration-law and nonvacuity attack

The consistency transfer survives without assuming the shipped calibration law. W1-PXN explicitly identifies (S)/(E)/(T)/(P) as data/deterministic-LS0 statements (`Theory_work/Wave1/W1-PXN/STATEMENT.md:52–68`; `REPORT.md:18–27`). W1-GEN's centre law and descent are likewise data statements (`Theory_work/Wave1/W1-GEN/STATEMENT.md:84–105`), and its posterior input is T03-sharp under (H0). Their assembly steps list CAL, but C-DLV correctly replaces those steps by a direct scored-set argument, rather than citing an unchanged CAL-bearing headline theorem.

Let `K_n` mean that the prescribed deterministic LS0 scores `S_0`. For every delivered run, `K_n` implies that `S_0` belongs to the all-scored set (or exact enumeration already scored it). If also `pi(S_0)>1/2`, its exact score exceeds every competitor's score, hence the reported maximum is `S_0`. Therefore

```text
P(output and HPM != S_0)
  <= 2 E[1-pi(S_0)] + P(K_n^c).
```

This is the pointwise-corrected M5(0) argument (`Theory_work/State_of_Project/sections/04_theory.tex:466`, `:477–484`), involving neither pooling nor grid quality. The longer C-GROW search contains the smaller-cap search's scored set: its greedy scans/path are identical up to the smaller cap. Thus the same LS0-discovery bounds still apply. Carry the original class hypotheses: LH's SIZE and recorded instance-input status; LH-iid's W1-PXN hypotheses including SIZE and `p_n -> infinity`; GEN's (H0)–(H2), or its favourable/random-design versions. “Fixed truth size and polynomial p” alone is insufficient. LH's inherited SAME-FAMILY-ONLY input is not upgraded (`W1-GEN/REPORT.md:64`; `C-DLV/lemmas/L4_delivery.md:56–64`).

The computational premises are strong but are not an assumption of calibration success or output. TDP supplies a terminating polynomial reference algorithm (`Theory_work/Wave1/W1-N3/lemmas/L7_tie_aware_dp.md:7–21`); stage/search/rebuild caps bound the rest; finite polynomial allocations can then be chosen for every finite `(n,p)`. This is nonvacuous as an abstract unit-cost exact-real/unbounded-word theorem. MACH's allocation-success and environmental clauses are essential additional premises, not consequences for physical R/C++ from operation counting. The claim is not an unconditional reliability statement about the shipped binary or fixed default 8-GiB/24-hour allocation.

## Exact corrected statement

**Proposition F (total tier-1 fallback, with the C-GROW cap).** Consider the specified v3.1 method with deterministic LS0 from the exact e4 start mode, complete scans, emitted centre and scored-set HPM retention. Let `ell_n=ceil(log2(n+p+1))`, `K=min(p,floor(n/2))`, and set LS0's move cap to `a_n=ell_n+|S_tilde_0|`; all other local-search caps remain `ell_n`. Keep fixed declared `R'=4k` and fixed worker count, and the other CONFIG restrictions of C-DLV. Assume EX-A with its unit-cost interpretation, IDEAL-W, EX-S, SR, e4, GUARD-W, TDP-IMPL and MACH as stated in C-DLV, and OP-LS0 with the cap replaced by `a_n`, with valid declared seed/allocation and model G on the stated classes.

At the first failed tier-1 grid construction, terminate that tier and select its last successful construction if one exists, otherwise its completed pilot schedule. Preserve the tier-1 budgets and inherited scored state, freeze the selected complete grid through the normal frozen-record construction before final randomness, and continue with the prescribed final run and LS0. Retain the failure/fallback metadata; make no further calibration attempts and do not promote a partial failed grid to a fallback. Leave other branches unchanged.

Use `W_G` and `M_G` defined in finding 1, with constants large enough for the fixed implementation and concurrency, and choose allocations satisfying

```text
mem_n  >= max{ beta M_G(n,p_raw)+beta_0, P_0, P_1 },
time_n >= max{ 2[tau W_G(n,p_raw)+tau_0], P_t_bar },
allocation$mem_gb >= mem_n/2^30,
allocation$hours  >= time_n/3600,
```

where `P_0,P_1,P_t_bar` are Corollary R's preflight bounds, and certificate budgets remain included. Then for every admissible `n>=3`, `P(no output)=0`. On LH exact Gram, LH-iid and the W1-GEN class, under the respective statistical hypotheses and inherited dependency qualifications used in Corollary D-prime, `P(HPM=S_0)->1` under the original unconditioned data law. CAL, restricted-ESS success, and any bound on the probability of triggering the fallback are unnecessary. With the original LS0 cap `a_n=ell_n`, the original Lemma R envelopes suffice.
