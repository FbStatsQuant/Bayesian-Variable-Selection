# D1 code check (Opus): `methodology/smc_bvs_method.tex` against the shipped serial core

Reviewer: Claude Opus 5.5 (review sub-agent), 2026-11-16. Effort: high. Read-only check. The only file written is this report.

- **Document:** `Docs/Writing/methodology/smc_bvs_method.tex` (670 lines), mtime 09:43:34. The PDF is newer (09:43:53), and `pdftotext` shows that the passages quoted below are in it.
- **Code (the authority):** `Scripts/SMC_BVS/core/` (`v3_*.R`, `cpp/*.h`, `cpp/v3_core.cpp`). In this report, pins are relative to that folder unless a full path is given.
- **Method:** I read every R and C++ file of the core in full. `CODE_FACTS.md` served only as a map; I checked each of its facts in the code myself. I recomputed every example value at n = 200, p = 10,000. One fact about runtime needed a measurement: I timed the shipped scorer (`cpp/v3_score.h`, compiled standalone with the `Makevars.v3` flags in the scratchpad) on a model of size K = 100 at n = 200.

Severity scale: **C** = wrong fact, **S** = misleading omission, **E** = editorial.

---

## 1. Parameter table (Table "Every constant of the method", §6)

Values at n = 200, p = 10⁴: ℓ_n = ⌈log₂ 10201⌉ = 14; L = max(4, ⌈log₂ 201⌉) = 8; K = 100; B = min(14, 100, 16) = 14; N₀ = 10,000; N^c₀ = ⌈512·10⁴/2500⌉ = 2,048; T₀ = max(1000, 196) = 1,000.

| Row | Verdict | Correction (value / pin / example) | Evidence |
|---|---|---|---|
| size cap K | OK | — (100 ✓) | `cpp/v3_score.h:40`; `v3_preprocess.R:21` |
| model prior BB(1,p) | OK | — (formula checked: B(k+1,2p−k)/B(1,p) = ½/C(2p−1,k)) | `cpp/v3_score.h:61-70` (`logw` l.65, `logWK` l.68, `logprior` l.70) |
| coefficient prior scale; ridge | OK | — (200 ✓) | `cpp/v3_score.h:175-183` |
| inverse-gamma a₀, b₀ | OK | — (the C_n of (7) matches IG with density ∝ σ^{−2(a₀+1)}e^{−b₀/σ²}; I re-derived it) | `cpp/v3_score.h:14, 57-60` |
| duplicate threshold | OK | — | `cpp/v3_core.cpp:742-760` (test at l.754) |
| small-Q_S recomputation | OK | — | `cpp/v3_score.h:219` (form at 145-160) |
| block size cap B | OK | — (14 ✓) | `v3_preprocess.R:22`; `cpp/v3_core.cpp:145-146` |
| neighbour threshold | OK, with a wording fix (E) | 0.30 ✓ (√(2·ln 10⁴/200) = 0.3035). "1 to B neighbours" holds for the *chosen* partners of each j. After symmetrisation, a degree can exceed B (the text at l.280-281 is correct). | `cpp/v3_blocks.h:146-172` (keep rule l.165-167, symmetrisation l.170-171) |
| start-mode enumeration cap | OK | — | `cpp/v3_core.cpp:469`; `cpp/v3_start.h:271-305` (cap test l.290, tie DP l.303) |
| exact-case threshold | OK | 5.0×10⁸ ✓ ((5·2048 + 4·10⁴)·10⁴ = 5.024×10⁸) | `cpp/v3_core.cpp:71-85`; `v3_fit.R:105-106` |
| islands | OK | — | `v3_run.R:91` (diagnostic islands also hard-coded at `cpp/v3_core.cpp:664-667`) |
| particles per island N_i | OK | 10,000 / 40,000 ✓ | `v3_preprocess.R:25,30`; selected at `v3_run.R:90` |
| burn-in rounds L | OK | 8 ✓ | `v3_preprocess.R:24` |
| measured rounds | OK | — | `v3_run.R:90`; `v3_calib.R:12` |
| resampling | OK; pin incomplete (E) | Lines 316-327 hold the reweighting and the call. The multinomial resampler is at `cpp/v3_engine.h:230-259`; add that pin. | `cpp/v3_engine.h:230-259, 316-327` |
| moves per round | OK | 10,016 ✓ | `cpp/v3_engine.h:111-214` (`nlabels` at l.72) |
| calibration particles N^c_i | OK | 2,048; 8,192 ✓ | `v3_preprocess.R:26,30` |
| stage ceiling T_i | OK | 1,000; 4,000 ✓ | `v3_preprocess.R:27,30` |
| tiers | OK | — | `v3_preprocess.R:30`; `v3_calib.R:150-159` (`e <- 1` at l.158) |
| pilot ESS target | OK (E) | 0.90·2048 = 1,843.2. The code requires ESS ≥ 1,843.2, so write "1,843.2" or "≈1,843". | `cpp/v3_calib.h:31-32` |
| pilot step floor | OK | 0.001 ✓ | `cpp/v3_calib.h:38-43` |
| grid target | OK | — | `cpp/v3_calib.h:79,84,92` |
| bisections | OK | — | `cpp/v3_calib.h:34,82` |
| candidate set V | OK | up to 400,001 ✓ (20p + 20p + 1) | `cpp/v3_core.cpp:699-724`; `cpp/v3_ledger.h:78` |
| rebuild iterations | OK | 14 ✓ | `v3_calib.R:84-119` (loop l.85) |
| triggers E1, E2 | OK, pin imprecise (E) | l.60-61 initialise all seven triggers. E1/E2 are computed at l.101-102 and set at l.109. | `v3_calib.R:60-61, 101-102, 109` |
| grid fallback | OK | — | `v3_calib.R:120-125, 163-169`; `v3_fit.R:151` |
| base move cap ℓ_n | OK | 14 ✓ | `v3_preprocess.R:23` |
| move cap from the start mode | OK | — | `cpp/v3_core.cpp:473`; `v3_run.R:100-101` |
| search from the start mode | OK | — | `v3_fit.R:73`; `cpp/v3_core.cpp:460-481` |
| pooling of islands | OK | — | `v3_run.R:154,162` |
| estimated MPM threshold | OK | — | `v3_run.R:163` (exact branch: `v3_exact.R:12`) |
| stored models | OK | 400,001 ✓ | `cpp/v3_ledger.h:78` (exact branch: `cpp/v3_core.cpp:531`) |
| evidence lower bound | OK | — | `v3_run.R:155` (exact branch: `v3_fit.R:126`) |
| low-ESS flag | OK | 5,000 ✓ | `v3_run.R:201` |
| near-tie window | OK | — | `v3_run.R:171` (exact branch: `v3_exact.R:10`) |
| allocation defaults | OK | — | `v3_fit.R:73,92` |
| score cache | OK; one pin missing (E) | 5×10⁶ ✓. The calibration cache is also 500p: add `v3_calib.R:147`. | `v3_run.R:92`; `v3_calib.R:147`; `cpp/v3_score.h:284` (clear when full) |
| seed | OK | — | `v3_preprocess.R:7-11`; single-value check at `v3_fit.R:88` |
| ceiling on the base move cap | OK in value; wording (E) | `v3_run.R:96` validates the *LS0* base cap (option `v3.ls0_ell`, default ℓ_n), and only when LS0 is on. A violation raises an R error (`stop()`) when the final run starts, after the calibration. The run does not return a status. | `v3_run.R:95-98` |
| integer range of the move cap | OK in value; wording (E) | Same remark: Rcpp `stop()` raises an R error and returns no status. | `cpp/v3_core.cpp:473-474` |

**Code names in parentheses:** all correct. `K`, `logw`, `logWK`, `B_MAX`, `islands`, `N0`, `H0`, `T0`, `ell` and `ls0_cap` exist with these meanings. The `ls0 = TRUE` default is at `v3_fit.R:73`.

**Constants the table omits** (S, because the table claims to list "every constant"):

- the snap-to-1 tolerance 10⁻¹² in the pilot and the grid (`cpp/v3_calib.h:42, 89`);
- the exact branch's `global_certified` rule and its error factor 64ε (`cpp/v3_score.h:240-246`, `cpp/v3_core.cpp:560-563`);
- the preflight constants (`v3_fit.R:10-14, 26-48`): 200 timed scores, the LS0 worst case of (ℓ_n+K+1) scans of p + p²/4 models, the bookkeeping factor 2, and the memory coefficients;
- the stream map 0–13 (`v3_run.R:8-11`; `cpp/v3_core.cpp:444, 626, 667`);
- the four diagnostic islands per rebuild (`cpp/v3_core.cpp:664`).

---

## 2. Findings in the text (Sections 1–5, Algorithm 1)

| # | Location (tex line) | What the document says | What the code does (file:line) | Sev |
|---|---|---|---|---|
| 1 | §5.7 "Runs without output" (l.519-520); Alg. 1 step 5 (l.442); table row "allocation defaults" | Before the run and before tier 1, the method runs a *memory* check. | In the default configuration (`ls0 = TRUE`, `v3.ls0_cap` ≠ `"ell_n"`), `ls0_wc = TRUE` (`v3_fit.R:114`), so the SMC preflight also charges LS0's worst-case **time**: (ℓ_n+K+1)·(p+p²/4) score requests × 2 × the measured seconds per size-K score, compared with the allocated hours (`v3_fit.R:43-47, 65`). The same check runs again before tier 1 (`v3_fit.R:144-148`). The exact-branch preflight also checks the estimated enumeration time (`v3_fit.R:30-34, 60`). **Consequence at the paper's example size:** at n = 200, p = 10⁴ the memory estimate is about 5.2 GiB < 8 GiB, so the timer runs. The request count is 2.88×10⁹. A size-100 score took 3.5×10⁻⁴ s with the shipped scorer and flags (my measurement), so the estimate is ≈2.0×10⁶ s ≈ 563 h, far above 24 h. **The default `v3_fit` therefore returns `resource_limit` before setup at the table's example size.** To pass, a size-100 score would have to take less than 1.5×10⁻⁵ s. The text and the example column suggest such runs proceed. | **C** |
| 2 | Alg. 1 step 5 (l.443) | "The scored models and the random streams carry over." | The ledger, the leader and top stores, and the score cache carry over (`cpp/v3_core.cpp:571-573, 585-614`). The random streams do **not**: the tier-1 pilot uses stream 5 and the tier-1 diagnostic islands use streams 6–9, each freshly seeded, while tier 0 used 0 and 1–4 (`cpp/v3_core.cpp:626, 667`; stream map at `v3_run.R:8-11`). Streams continue only across rebuild iterations within a tier (`cpp/v3_core.cpp:669`). | **C** |
| 3 | §5.5 after the move list (l.375) | "Swaps keep the model size, so only the inclusion updates can add a predictor, and they enforce the cap." | The independence move replaces S by a fresh π₀ draw of any size ≤ K (`cpp/v3_engine.h:182-192`), so it can also add predictors and change the size. It respects the cap because π₀ lives on Ω. | **C** |
| 4 | Alg. 1 step 2 (l.434-437) | Pilot: adaptive schedule, then "at φ = 1, run a local search from the best model found." | At φ = 1 the pilot first runs L burn-in rounds and 4 measured rounds (`run_island_s`, `cpp/v3_engine.h:342-360`, called at `cpp/v3_core.cpp:632` with L and Hm). The local search comes after (`cpp/v3_core.cpp:642`). The same holds for each diagnostic island (`cpp/v3_core.cpp:670`); "island" covers that case. | S |
| 5 | §5.4 "Triggers" (l.464-468); Alg. 1 step 5 | Triggers fire "if any of these occurs", with no statement of *when* each is evaluated. | E1 and E2 are overwritten at each rebuild iteration, so only the **last completed** diagnostic iteration counts (`v3_calib.R:101-102, 109`). E3 and `local_limit` are OR-ed over the pilot and every iteration (`v3_calib.R:59-61, 110`). | S |
| 6 | §5.6 "Local search" (l.482-483); trigger "a local search that reached its move cap" (l.468) | Stops at the first scan with no strict improvement, "or when it reaches its move cap". | After ℓ moves the search makes one more full scan. It stops with `local_limit` only if that scan still finds a strict improvement, and then it *returns* that improving neighbour (scored but not moved to). A search that makes exactly ℓ moves and then finds no improvement ends `no_improvement` and is certified (`cpp/v3_engine.h:408-415`). The trigger is therefore "still improving after ℓ moves", not "reached ℓ moves". | S |
| 7 | §5.7 "Diagnostics" (l.513-516) | Lists E1–E3, the low-ESS flag and near ties. | Also reported, and omitted here: `local_limit` (either search; `final_local_limit`, `ls0_local_limit`, `v3_run.R:196-197, 202`); `ls0_improved` and `ls0_hpm_changed` (`v3_run.R:198-199`); `cut_group` with its components (components of the uncapped graph \|r̂\| ≥ √(2 log p/n) spanning ≥ 2 blocks; `cpp/v3_core.cpp:794-819`, `v3_fit.R:141-143, 172`); `escalated`, `forced_pilot_steps`, `grid_unconverged`, `grid_fallback` (`v3_fit.R:165-170`). Also: final E3 excludes LS0 (`v3_run.R:186-191`). The text implies this ("the final local search") but does not say it. | S |
| 8 | §5.7 "Runs without output", last sentence (l.521-522) | "On such stops the method returns the best model scored so far, marked incomplete." | `invalid_input` returns no model (`v3_fit.R:89, 99-102`). `no_predictors` and `y_constant` return ∅ but are not marked incomplete (`v3_fit.R:101`). A preflight `resource_limit` returns no model (`v3_fit.R:117`). An invalid allocation and the two integer-limit checks raise R errors and return nothing (`v3_fit.R:91-94`; `v3_run.R:96-97`; `cpp/v3_core.cpp:474`). The sentence holds for stops after setup starts. | S |
| 9 | §5.7 certification (l.499-502); §5.1 exact case | The exact case is certified by enumeration; nothing else is said. | The exact branch also reports `global_certified` = [F(HPM) − η(HPM) > max_{S≠HPM}(F(S)+η(S))], with η the heuristic bound labelled "not a validated interval bound" (`cpp/v3_core.cpp:560-567`; `v3_exact.R:4-17`; `v3_fit.R:128`). In the SMC branch it is always FALSE (`v3_run.R:180`). | S |
| 10 | §5.3 heading and Fig. 1 (stage 3: "start mode S̃₀") | The start mode is computed in stage 3. | The code computes `start_mode` only at the end of the final run, after the final local search, as LS0's centre (`cpp/v3_core.cpp:465-469`). It is not computed if the run stops earlier. It is deterministic, so results do not change. Say "defined" in stage 3, or note when it is computed. | E |
| 11 | §5.6 "Final run" (l.477-478) | Random-number streams "disjoint from those of the calibration". | Streams 10–13 are seeded separately: SplitMix64 of (seed≪32)+stream (`cpp/v3_util.h:47-51`; `cpp/v3_core.cpp:444`). They are distinct seeds of xoshiro256**, not provably non-overlapping subsequences. Prefer "separately seeded" or "independent". | E |
| 12 | §5.5 moves (l.366-371) | Uniform swap and neighbour swap as stated. | Edge cases are omitted. The uniform swap is a self-loop when \|S\| ∈ {0, p} (`cpp/v3_engine.h:148`). The neighbour swap is a self-loop at S = ∅ and rejects without scoring when N(j)∖S = ∅ (`cpp/v3_engine.h:165, 170`). | E |
| 13 | §5.4 "candidate set and grid" (l.461-462) | The construction fails on no numerical progress or more than T_i steps. | Two more failure modes exist: validation failure, ρ_V(u,v) < 0.90 at the appended point after the snap to 1 within 10⁻¹² (`cpp/v3_calib.h:89-92`), and "no target above u" (`:76`, unreachable because the pilot ends at 1). | E |
| 14 | §5 intro (l.228) | "Every model scored anywhere is recorded." | The final ledger keeps the tables, the *inherited* calibration models (top 40p+1 ∪ the two leader stores ∪ the calibration HPM; `cpp/v3_core.cpp:728-735`), the final islands and both searches. Calibration models outside these stores are not carried. §5.7 (l.496-498) states this correctly; the intro sentence overstates it. | E |
| 15 | §3 Occam factor (l.170) | Each extra predictor multiplies m(S) by about (n+1)^{−1/2}. | For orthogonal standardised predictors (G_S = (n−1)I) the determinant ratio is ((n+1)(n−1)+1)/n = n per predictor, so the factor is exactly n^{−1/2}. "About (n+1)^{−1/2}" is acceptable; "about n^{−1/2}" would be exact in that case. | E |
| 16 | §3 numerics (l.172-174) | Three routes; failure only if all three fail. | Correct (`cpp/v3_score.h:227-238`). Precision: a route also fails when it yields a non-finite log m, for example 2b₀ + Q ≤ 0 (`:187, 201, 223`). The QR is an augmented Householder QR of [√(n+1)X_S; I] and [X_S; I] (`:189-202`). | E |

**Checked and correct (no finding):**

- **Preprocessing:** input validity, exact-equality drop, statuses and their precedence, standardisation with max-abs pre-division and the anchored two-pass route, y′y = n−1, duplicates (`v3_preprocess.R:37-68, 97-132`; `cpp/v3_core.cpp:742-760`).
- **Prior and score:** the prior (4) and Example 2.1 (p = 3: ½, 1/10, 1/20, 1/20, sum 1; n = 4: 19/20 ✓); the ratio (k+1)/(2p−1−k); (6)–(7), including C_n and m(∅); F(S) (`cpp/v3_engine.h:97`).
- **Exact case:** the threshold uses N^c₀ = H₀ (`cpp/v3_core.cpp:75`).
- **Blocks and neighbour graph:** complete linkage on 1 − \|r̂\|, top-down cut, next-fit packing in leaf order with whole clusters (`cpp/v3_blocks.h:39-144`); tables for \|U\| ≤ K (`cpp/v3_start.h:76-98`); neighbour rule (`cpp/v3_blocks.h:146-172`).
- **Start law and start mode:** Φ recursion, Z̄₀ and the backward sampler (`cpp/v3_start.h:101-176`); start-mode size tie → smaller, lexicographically smallest set, 10⁶ cap, tie-aware DP (`cpp/v3_start.h:195-305`).
- **Discrepancy and path:** the identity γ₀e^{d} = e^{F}/m(∅) (`cpp/v3_engine.h:97`); the path (`cpp/v3_engine.h:14`).
- **Moves:** Gibbs with o_j recorded before the draw and o_j = 0 at the cap (`:111-132`); the Hastings factor (`:173-175`); independence acceptance (`:187`); random Fisher–Yates order of p+B+2 labels (`:195-214`).
- **Island:** log Ẑ start, reweight, increment, ESS, multinomial resampling every stage, one round per stage, L + 4 rounds, RB-PIP (`:299-364`); island evidence formula.
- **Pilot and grid:** pilot rule (0.90, φ′ = 1 first, 60 bisections, floor 1/T_i, forced count); V; ρ_V; grid rule; rebuild loop with ≤ ℓ_n iterations and convergence on an identical grid (`v3_calib.R:84-119`); the seven triggers; one escalation with a preflight; fallback at tier 1 only (`v3_calib.R:120-125, 163-169`); freeze; no grid → `schedule_limit` (`v3_calib.R:170`).
- **Final run and searches:** streams 10–13 with fresh π₀ draws; final search cap ℓ_n; LS0 cap ℓ_n+\|S̃₀\| with no uniforms (`cpp/v3_core.cpp:443-481`).
- **Outputs:** HPM tie rule (`cpp/v3_util.h:120-126`); local certification on the returned HPM from either search (`v3_run.R:179, 192-195`); equal-weight pooling, MPM > ½, 0.05·Ẑ; final E1/E2/E3 and low ESS on final stages only (`v3_run.R:182-201`).
- **Runtime guard:** checked after every bridge stage, grid construction and local search, including LS0 (`cpp/v3_engine.h:335`; `v3_calib.R:75-76`; `cpp/v3_core.cpp:459, 480, 645, 692`).

---

## 3. The cost sentence in §5.5 (l.396-397)

"One round costs about p + B + 2 score evaluations per particle": **correct as a count of score requests (an upper bound)**, with three precisions.

- **Count per particle and round** (`cpp/v3_engine.h:113-192`): each Gibbs step issues one request for the flipped model, so p in all, fewer when \|S\| = K and the addition is infeasible. The uniform swap issues 1 (0 when \|S\| ∈ {0, p}). The neighbour swaps issue up to B (0 when S = ∅ or N(j)∖S = ∅). The independence move issues 1 and also makes one π₀ draw.
- **Cost of a request:** a request is a Zobrist-hash cache lookup. Only a miss runs the scorer, at O(\|S\|³) from the stored Gram (`cpp/v3_engine.h:89-101`; `cpp/v3_score.h:176-188`). Near φ = 1 most requests are cache hits, so "score evaluations" overstates the number of factorisations. "Score requests" or "candidate models scored (most from the cache)" would be exact.
- **Hidden term:** each proposal copies the particle, including its p-bit membership vector (`tmpQ = P`, `cpp/v3_engine.h:120, 152, 172`). That adds O((p+B+2)·p/64) word copies per particle and round: ≈1.6×10⁶ at p = 10⁴, comparable with the cache-hit work.

"So a stage costs about N(p+B+2)" is consistent. The appeal to Appendix A as the limit at very large p is fair. The O(p²) Gram, correlation and clustering memory (`cpp/v3_score.h:44-53`; `cpp/v3_blocks.h:53-55, 153`) also binds there.

---

## 4. Appendix D: confirmation and additional disagreements

**The three listed items, checked against the code:**

1. **Confirmed.** The code pools with equal weights (`v3_run.R:154, 162`) and computes no Ẑ-weighted PIP; a grep of the core for a weighted or plain PIP finds nothing (`README.md:16`). Precision: the "earlier method document" should be named. `Theory_work/State_of_Project/sections/02_method.tex:442-443` (v3.1) makes the Ẑ-weighted PIP *primary*. `Docs/Methodology/METHODOLOGY_v3.md:41, 272-274` (v3.0) has it as *secondary*.
2. **Confirmed.** The comment `1 <= B <= 20` is at `cpp/v3_core.cpp:144`; `B_MAX = 16` and the check are at `:145-146`.
3. **Confirmed.** `islands = 4L` is fixed (`v3_run.R:91`), and there is no stacking, `R'` or worker code in the core (grep). Pin: the stacking text is `02_method.tex:374-389`; the parallel layer is at `:391-400`. Widen the cited range from 363-386 to 363-400.

**Additional disagreements between the sources and the code:**

| # | Source says | Code does | Pins |
|---|---|---|---|
| D4 | `README.md:19`: "Memory-only SMC preflight … Recheck memory before tier 1." The code comment `v3_fit.R:25` says "ls0_worst_case = FALSE is the shipped preflight." `METHODOLOGY_v3.md:321-324, 403`: memory **and** wall time (score count × s(k)) for both branches. | Default SMC preflight = memory **plus** LS0 worst-case time (`v3_fit.R:114-115, 43-47, 65`), before the run and before tier 1 (`:144-148`). The exact branch checks memory and enumeration time (`:30-34, 60`). All three sources differ from the code, and the code contradicts its own comment. Practical effect: see §2, finding 1 (`resource_limit` at n = 200, p = 10⁴ with 24 h). `02_method.tex:507` quotes an LS0 overhead "under 1 s per fit", while the preflight charges ≈563 h at that size. | `v3_fit.R:25-26, 43-47, 114-117, 144-148` |
| D5 | `02_method.tex:492` (LS0 runs "with the §6.10 rules", i.e. cap ℓ) and `README.md:43` (LS0 "with the production ell") | LS0 move cap = ℓ_n + \|S̃₀\| by default (C-GROW MR1); `"ell_n"` is only an option | `cpp/v3_core.cpp:403-404, 473-479`; `v3_run.R:100-101` |
| D6 | `METHODOLOGY_v3.md:226` and `02_method.tex:324-325`: a failed grid construction at tier 1 gives status `schedule_limit`. The README does not mention a fallback. | Default (v3.1, `ls0 = TRUE`): the method freezes the last successful tier-1 grid, or else the tier-1 pilot schedule, and continues. `schedule_limit` remains only with the fallback off. | `v3_calib.R:120-125, 163-170`; `v3_fit.R:151` |
| D7 | `METHODOLOGY_v3.md:57, 158`: `global_certified` "with numerical comparisons validated" | Heuristic margin with η, explicitly labelled "heuristic (not a validated interval bound)". (02_method.tex:175-178 already records the v3.1 relabel; consistent.) | `cpp/v3_core.cpp:560-567`; `cpp/v3_score.h:240-246` |
| D8 | `02_method.tex:485` (v3.1 e2): an informational near-tie list at max(10⁻⁹, 2η(Ŝ)) | Near ties use 10⁻⁹ only, in both branches | `v3_run.R:171-173`; `v3_exact.R:10-12` |
| D9 | `02_method.tex:452-456`: the code also computes plain PIPs (`pip_plain`, `mpm_plain`), citing the campaign copy `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/v3_run.R:167-169` | The shipped core computes no plain PIP and no plain MPM (grep) | `v3_run.R:150-163` |
| D10 | `02_method.tex:59-62, 619, 685, 784`: v3.1 statuses `degenerate_n`, `unsupported_size`, n = 2 admitted (02 itself labels these proposed) | Not implemented: n < 3 → `invalid_input`; no `unsupported_size` | `v3_preprocess.R:106` |
| D11 | `02_method.tex:427-431, 512-531, 538-576`: certificate card, Z_𝒯, bound max{Z_𝒯, 0.05Ẑ}, μ̂(h), Ĵ, measured-round archive | None implemented ("card not implemented") | `v3_run.R:189` |
| D12 | `02_method.tex` pins cite the campaign copy `…/v2_2_1/core/…`, not `Scripts/SMC_BVS/core/` | Line numbers differ: the exact count is at `cpp/v3_core.cpp:71-85` here vs `:97-110` there; pooling at `v3_run.R:154,162` here vs `:121,129` there. Pins are not transferable between the two copies. | — |
| D13 | `METHODOLOGY_v3.md:38`: allocation default "8 GiB memory" only | Default allocation is 8 GB **and 24 h** | `v3_fit.R:73, 92` |
| D14 | `METHODOLOGY_v3.md` §6.1 and §6.10 (v3.0) have no LS0 and no e4 tie-aware DP | Both are in the code, on by default (v3.1) | `cpp/v3_core.cpp:460-481`; `cpp/v3_start.h:234-305` |

---

## 5. Summary

The parameter table is accurate: every value, every example and every code name checks out. Its pins are right, with three small refinements (resampler location, E1/E2 lines, calibration cache).

Sections 1–5 and Algorithm 1 are faithful on almost every formula and procedural step. Three statements are wrong facts:

1. **The preflight is not memory-only.** The default preflight also charges LS0's worst-case time, and at the example size n = 200, p = 10⁴ this makes the default run stop with `resource_limit` before setup.
2. **The random streams do not carry over between tiers.** Tier 1 uses streams 5–9.
3. **Not only the inclusion updates can add predictors.** The independence move can too.

There are also six misleading omissions: the pilot's burn-in and measured rounds; when E1/E2 are evaluated; the move-cap semantics; the diagnostics list; what a stop returns; the exact branch's `global_certified`. Appendix D items 1–3 are confirmed; eleven further disagreements are listed above.

NOT-CODE-FAITHFUL
