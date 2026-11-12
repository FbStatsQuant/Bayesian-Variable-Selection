# DESIGN_v1 — many-island SMC-BVS on NOTS, from measured numbers (W3-SCALE leg A)

**Status:** design only. It replaces the extrapolations of `Pause_2026-11/SCALING_DESIGN_v0.md` by leg A's measurements
and keeps v0's notation and tags ([OP-bit], [OP-law], [Δ𝒞], [Δlaw], UNVERIFIED). Nothing here changes the method;
the two questions reserved for the owner are only framed (§7). Sources: `CHECKPOINT_1.md` (tables),
`results/` (TSV files), `LOG.md`. All times are one thread on a NOTS sapphirerapids node (Xeon Platinum 8468), GCC
14.3.0, R 4.5.2, pinned flags.

## 1. What changed since v0 (measured)

| v0 statement | leg A measurement | consequence |
|---|---|---|
| elementary step ≈ 3 µs (local i7) | **0.90–1.16 µs** in the bridge, **1.64–1.90 µs** at φ = 1 (burn-in, measured rounds), p = 1k, 2k, 20k | islands cost a third of v0's estimate |
| T = 30, UNVERIFIED | final grids **26–40 stages** (24 PROD-H units; median 32.5 at p = 500, 31 at p = 1000); 33 at 2k; 29 at 20k (island with N = 2,500); pilots 16–30 | T grows slowly with p; v0's 30 was right |
| calibration ≈ 2.6 final-island equivalents (I = 3) | rebuild count **I = 2–10** (median 4 at p = 500, 6 at p = 1000), **8 at 2k**; calibration is **45% / 56% / 62%** of fit time at p = 500 / 1000 / 2000 | the sequential rebuild loop is the first wall of the N = p rule (§2) |
| setup dominated by complete linkage; Gram 11 s at 10k | v3.1 at 20k: Gram 16 s, blocks 25 s, **neighbour graph 59 s**, tables 0.5 s; setup peak **9.45 GB** = 24 p² | the neighbour graph was the setup cost; fixed bit for bit (§3) |
| preflight refusal from p ≈ 2.3k (by reading) | confirmed: v3.1 charges 53 h at 5k, 231 h at 10k, 930–1,370 h at 20k against 24 h; passes at 2k (11.2 h) | fixed in v3.2-dev (delivery only); new refusal point ≈ 25k (§3) |
| σ̂ = sd(log Ẑ_r): no data | N = 2,500: median **0.065** (p = 500), **0.088** (p = 1000), 0.042 (2k, one fit); tail to 0.70; escalated fits (N = 10,000) 0.82 and 1.00; diagnostic islands (H = 512): median 0.15–0.22 | evidence weights are far from degenerate at p ≤ 2k; nothing measured at fixed N beyond 2k (§4) |

One island costs, to within 5% on the three profiles,

  **t_island(N, p, T) ≈ N·(p + B + 2)·(T·c_b + 12·c_1), c_b ≈ 1.0 µs, c_1 ≈ 1.8 µs** (12 = L + 4 terminal rounds at n = 200),

i.e. ≈ 52 µs per particle and predictor at T = 30. A v3.1 fit is 4 + 0.2 + 0.82·I island-equivalents (4 final
islands, the pilot, 4 diagnostic islands of H = 0.2048 N per rebuild): 8.3 at I = 5 (measured 8.2 at 1k), 10.8 at I = 8
(measured 10.7 at 2k).

## 2. The walls, re-ranked

1. **Sequential depth of the N = p rule.** With N_e = max(2500, n, p) every island costs Θ(p²·T) and a fit is 8–15 of
   them in sequence. Measured or implied by the formula (T = 35): 5k: 0.42 h per island, 4.6–6.3 h per fit (5k profile:
   see CHECKPOINT_1); 10k: 1.7 h per island, **18–25 h per fit**, at or over the 24 h commons limit; 20k: 6.8 h per
   island, 3–4 days per fit. An escalation (N × 4) multiplies everything by at least 4. Leg A's bit-identical changes
   do not touch this: they remove setup and delivery obstacles only.
2. **Calibration rebuild loop.** I approaches its cap ℓ = ⌈log₂(n + p + 1)⌉ as p grows (ℓ = 10, 11, 12, 13 at
   p = 500, 1k, 2k, 5k; observed maxima 8, 10, 8). An unconverged loop fires the escalation trigger. This loop is
   pure sequential depth today (4 diagnostic islands in sequence per rebuild).
3. **Setup memory.** 8 p² for the Gram plus 8 p² for the linkage distances (v3.2-dev; v3.1 holds 24 p²): 6.4 GB at
   20k, 40 GB at 50k, 160 GB at 100k (one job per 257 GB node), impossible at 1M.
4. **LS0 preflight.** After the v3.2-dev fix the worst-case charge at 24 h still refuses fits from p ≈ 25k at n = 200
   (18.8 h charged at 20k), although the measured LS0 takes 0.1–2 s. Delivery only.
5. **Per-step O(p) terms** (particle bitset copies, `v3_engine.h:120,152,172`): not visible up to 20k (0.90 µs per
   step there against 1.14 at 1k). UNVERIFIED beyond 20k; v0's estimate (overtakes scoring near 200k) stands.

## 3. v3.2-dev after leg A (shipped on the branch, all [OP-bit])

`Scripts/SMC_BVS/core_v32dev/`, verified in `CHECKPOINT_1.md` §3. Setup at 20k: 85.6 s → 23–24 s, peak 9.45 → 6.41 GB;
neighbour graph 59 → 3.6 s; Gram 39 → 6.6 s (both including the copy of the Gram to R); tables 0.50 → 0.12 s. LS0
preflight charge at 24 h: 5k 53 h → 5.8 h, 10k 231 h → 13.7 h, 20k 1,372 h → 18.8 h (admitted). Still O(p²) memory and
unchanged islands.

## 4. The parallel unit: fixed-size islands, evidence-weighted merge

### 4.1 Pipeline (unchanged from v0 §3.1)
J0 build → J1 setup (once) → J2 calibration with census (once) → J3 final islands as a job array, one island per
task, no communication → J4 merge (pooled Ẑ, PIPs, union stores and HPM, final local search, LS0, card).
Island r is a deterministic function of (X, y, seed, r, binary, 𝒞): a failed task is replayed, never dropped.
Islands keep the v3 serial stream per island, so island-level parallelism needs **no** counter-based generator (O5 is
only needed for threads inside an island).

### 4.2 Costs with N_isl = 2,500 (the law-changing choice of §7(i); numbers only)

| p | t_island (T = 30) | calibration at H = 512, serial (I = 5 … 13) | R′ = 64 | R′ = 256 | status |
|---|---|---|---|---|---|
| 5k | 0.18 h | 0.8–1.9 h | 12 core-h | 46 core-h | formula |
| 10k | 0.36 h | 1.5–3.9 h | 23 core-h | 92 core-h | formula |
| 20k | **0.66 h (measured)** | 2.9–7.2 h (pilot at H = 2,500 measured: 0.61 h) | 42 core-h | 170 core-h | measured island |
| 100k | ≥ 3.6 h | ≥ 15 h | ≥ 230 core-h | ≥ 920 core-h | UNVERIFIED; needs the Gram-free core (80 GB Gram) |
| 1M | ≥ 36 h | — | — | ≥ 9,200 core-h | UNVERIFIED; needs Phase 2 and no per-step bitset copy |

Against the N = p rule at 20k: one island 6.8 h, a fit 3–4 days of sequential depth. Calibration's four diagnostic
islands can run concurrently (depth ÷ 4), see leg B.

### 4.3 Merge estimators (fixed island order, long double, as `v3_run.R:154`)
- log Ẑ = LSE_r(log Ẑ_r) − log R′; W_r = Ẑ_r / Σ_s Ẑ_s.
- PIP_Z,j = Σ_r W_r ĥ_rj (the v3.1 *specified* primary) and PIP_eq,j = mean_r ĥ_rj (the *shipped* primary,
  `v3_run.R:162`). Both are always reported; which one is primary is §7(ii).
- General declared h: μ̂(h) = Σ_r W_r H_r(h). Standard error of PIP_Z by the delta method:
  SE_j² = Σ_r W_r² (ĥ_rj − PIP_Z,j)².
- HPM and top store from the union of all scored models (strict order `hpm_better`; Lemma S), then one final local
  search and LS0 at the merge.

### 4.4 Effective number of islands (reported, never used to switch estimators)
- **R_eff = 1 / Σ_r W_r²**, with R_eff / R′ and max_r W_r; σ̂ = sd_r(log Ẑ_r).
- For log-normal Ẑ_r, R_eff / R′ ≈ exp(−σ²): σ = 0.09 → 0.99; 0.25 → 0.94; 0.70 → 0.61; 1.0 → 0.37; 2.0 → 0.018.
- Measured (R = 4, `results/pip_weighting.tsv`, 25 fits): R_eff / R ≥ 0.60 everywhere; ≥ 0.97 in 20 of 25.
- Measured σ̂ scales like 1/√N between H = 512 and N = 2,500 (0.15–0.18 → 0.065–0.088, ratio 2.2 = √(2500/512)).
  A first-order budget is σ² ≈ κ·T/N with κ ≈ 0.3–0.6 from these medians, which gives σ ≈ 0.07–0.10 at N = 2,500 for
  T ≤ 40. **This is a fit to p ≤ 2,000, not a law**: the tail (0.70 in one S3 fit at p = 1,000; 0.8–1.0 after
  escalation in the S5 and tie designs) comes from islands that differ in which modes they found, not from sampling
  noise, and W3-P6's small-n runs show the E2 flag (σ̂ > 1) rising with p/n at n = 50: 0/137, 2/40, 13/105, 6/16 at
  p = 50, 125, 250, 500.
- **Flag** `merge_degenerate` iff R_eff < R_min (declared, e.g. 30) or the Pareto shape k̂ of the upper weights
  exceeds 0.7 (threshold from the PSIS literature, UNVERIFIED for this use).

### 4.5 Census inside calibration (unchanged idea; now with a concrete size)
After the grid is frozen and before any final stream is read, run R_c census islands of the candidate N_isl on
calibration-side streams; record σ̂ and the cost per island; a **declared** rule fixes (N_isl, R′) from them. Census
islands never enter Ẑ or the PIPs; their scored models may be inherited by the stores. At 20k, R_c = 32 islands of
N = 2,500 cost 21 core-h. No estimate is selected from final outputs, and R′ is never adapted to them.

## 5. Memory: path to O(np)

| step | tag | peak at 20k | peak at 100k | note |
|---|---|---|---|---|
| v3.1 | — | 9.45 GB (measured) | 240 GB | Gram + correlation + distance |
| v3.2-dev (leg A) | [OP-bit] | 6.41 GB (measured) | 160 GB | Gram + distance |
| Gram-free scorer + streamed correlation tiles (v0 S2/S3, G1–G5, B1 streaming) | [OP-bit] by v0's local check; needs the per-particle factor cache to be fast | 3.2 GB (distance only) | 80 GB; 40 GB with the condensed distance | Phase 2; not in leg A by HQ ruling |
| sparse exact-below-threshold partition (v0 B4) | [Δlaw] | O(pB + edges) | same | needed only where the exact linkage does not fit (≈ 150k+) |

Island phase at 20k (N = 2,500): 5.5–6.5 GB resident, of which 3.2 GB is the Gram, about 1 GB the score cache (500p
entries) and the rest tables, stores and their R copies. With the Gram gone and a byte-capped cache (v0 D2) an island
needs 1–2 GB plus the shared read-only tables.

## 6. Theory obligations of the parallel method

IDs as in v0 §4; "f01" = `Wave3/API_AUDIT/sharp1/results/f01.md` (handed to this track by HQ, TRIAGE row 1).

| ID | obligation | what leg A adds | route |
|---|---|---|---|
| O1 | merge consistency at fixed N, R′ → ∞: PIP_Z → PIP, μ̂(h) → π(h); CLT | needs the island identity E[Ẑ_r H_r(h) \| ·] = Z π(h) for every final island and every declared h | Generalise Theorem N1 as f01 lays out (edits to three lemmas, no new mathematics): condition on V = all calibration-side streams instead of 𝒞 (stronger by the tower property; admits h measurable in V); drop the uniform bound B_h (Ω finite: prove for indicators, extend by linearity); state it for all L + 5 post-terminal populations and every stage; restate KERNEL as invariance + state-independent order. Then SLLN for the ratio Σ Ẑ_r H_r / Σ Ẑ_r under IND-T (independent final streams). Under IND-T the cross-fitted form E[W_r H_r(h) \| V, U_−r] = π(h) gives orthogonal island errors and a leave-one-island-out HPM frequency. |
| O3 | census inside calibration | census islands and the rule for (N_isl, R′) must be V-measurable | Census streams are calibration-side streams (new ids, disjoint from the final streams 10 … 9 + R′), so (N_isl, R′) is V-measurable and N1-on-V applies with a V-measurable R′ (f01 (a)4: only the event {r ≤ R′} is used). The TH01(c) counterexample (R′ adapted to final outputs) does not apply. The stream map and SI/IND-T must be restated for the larger map. |
| O2 | degeneracy at high p: a bound on E[(Ẑ_r / Z)²], or a lower bound showing exponential growth | first numbers (§4.4): σ̂ ≈ 0.07–0.09 at N = 2,500, p ≤ 2k, 1/√N scaling, heavy tail in masked designs | Open research. f01 names the benchmark results (Cérou–Del Moral–Guyader 2011; Beskos–Crisan–Jasra 2014, as recalled there, not checked here). The census is the empirical instrument. |
| O4 | N decoupled from p (reversal of "N_e is never split") | cost table §4.2; §7(i) | owner decision first; then restate TH01 (e)(f)(i), TH06, TH08 with general (N, R′) |
| O5 | counter-based streams | **not needed** for island-level parallelism (serial stream per island) | only if threads inside an island are adopted |
| O6 | replay fault tolerance; output event "all R′ islands completed" | — | short; plus a code audit of the array driver |
| O10 | union store and HPM over R′ islands | — | covered by Lemma S (re-cite) |
| O14 | preflight change is delivery only | implemented and reviewed (R01 finding 5): it acts at two admission points, the initial preflight and the pre-escalation preflight | record: outputs are identical on equal admission decisions; P(no output) changes |
| O17 (new) | process-parallel islands on one fit: what "same output" means | stores, HPM model and estimates are order-independent; the `fresh` score counters, cache statistics and the HPM provenance depend on which island scored a model first | define provenance by the minimum event key and report `fresh` per island; a reporting ruling, no theorem |

## 7. Reserved for the owner — framing only

**(i) p = 1M with a fixed N per island (reverses the v3.1 ruling "N_e is never split").**
- Keep N_e = max(2500, n, p): one island costs p·(p + 16)·52 µs: 1.4 h at 10k, 5.7 h at 20k, 6 days at 100k,
  **1.6 CPU-years at 1M**, with about 250 GB of particles per island at 1M. No number of islands repairs this.
- Fix N_isl (e.g. 2,500): one island is 0.66 h at 20k (measured), ≥ 3.6 h at 100k, ≥ 36 h at 1M (extrapolated; the
  Gram-free core and bitset-free particles are prerequisites). 256 islands at 1M ≈ 9,200 core-h.
- What is given up: the per-island bias no longer shrinks as p grows, so the equal-weight PIP keeps it for every R′;
  only the evidence-weighted PIP is consistent as R′ → ∞ at fixed N (O1), which ties (i) to (ii). What is unknown:
  σ̂ at fixed N beyond p = 2k (O2). Theorems to restate: O4.
- A middle option keeps the ruling up to some p_max (N = p is affordable to about 10k with parallel calibration) and
  fixes N above it.

**(ii) Primary PIP: equal-weight (`v3_run.R:162`, shipped) or evidence-weighted (the v3.1 specification).**
- On the 25 saved fits (R = 4, N ≥ 2,500): max_j |PIP_Z,j − PIP_eq,j| ≤ **0.0023** (median over fits 0.00009); the
  median-probability model is the same in 25 of 25; R_eff / R ≥ 0.60.
- So at today's settings the switch is invisible in the estimates. It matters in the many-island regime: PIP_eq has
  variance ∝ 1/R′ and no weight degeneracy but keeps the island bias; PIP_Z is consistent in R′ but loses a factor
  R_eff / R′ ≈ exp(−σ²) of efficiency (0.99 at σ = 0.09, 0.37 at σ = 1) and fails when σ is large.
- Switching changes a reported estimate, so it goes through the registry (the published PROD-H study used
  equal-weight PIPs). Either choice keeps both columns in the output.

## 8. After leg A

Leg B proposal with costs: `CHECKPOINT_1.md` §7. Order: bit-identical engine items and process-parallel islands
(what makes 10k–20k fits deliverable under the current law), the island census as a measurement (σ̂ against p at
N = 2,500), then Phase 2 (O(np) memory). Law-changing items wait for §7.

## Appendix: UNVERIFIED items carried forward
Per-step cost beyond p = 20k; every row marked UNVERIFIED in §4.2 and §5; σ̂ at fixed N beyond p = 2k; the Pareto-k̂
threshold; glibc `exp`/`log` variant selection across node types (all leg A runs were pinned to sapphirerapids);
NN-chain linkage equivalence (v0 O16); the literature names quoted from f01.
