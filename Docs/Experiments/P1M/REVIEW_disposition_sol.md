# REVIEW_disposition_sol — Sol review of EXP-CP1 (`reviews/EXP_CP1_sol.md`), Engineering manager, 2026-11-15/16

Verdict: **GO-WITH-CHANGES** (2 CRITICAL, 8 MAJOR, 1 MINOR). Sol explicitly finds **no NOTS infrastructure obstruction**
to joint SMC-BVS at 10⁶. All 11 findings are **adopted** (two with a stated modification); none is rejected. Sol's
five ranked changes are the priority order.

## Evidence already in hand that bears on the findings (measured after the plan Sol reviewed)
- **F1.** WP2 measured the production truncated partition (PR #13): mean block 13.2 at n = 200, ≈ 850 codes per column,
  so C ≈ 8.5·10⁸ at 10⁶. That is below Sol's full-packing bound of 1.17·10⁹, but ≈ 4× the plan's 210. D-18 (drop the stored
  sampler sections) was already decided.
- **F2.** INTERFACES v0.1.2 (merged in PR #11) already specifies one store per process, bounded per-thread offer buffers
  and a monotone shared cut-off. The reviewer's test showed that threaded = serial ledger. Measured store: 68.5 B per kept
  entry, peak 2.25c → ≈ 5.4 GB at 10⁶.
- **F3.** G0 measured the kernel on NOTS Sapphire Rapids: 87.5 ns per (support, label) for class A at 48 threads. The
  direct Gram-free step is 1,711 ns. This replaces the "c = 2 µs from a Gram-resident engine" basis for the scorer, but
  not an end-to-end stage (still T5).
- **F6.** Sol corrects my R6 summary, and the correction is accepted. At 5k, N = 2,500: 16/16 islands, R_eff 8.93. The
  1.58 was the incomplete 5k N = 10⁴ run. The stage-level re-runs are in progress (G0 jobs 2747372_2, 2747799_1).

## Dispositions
| F | finding | disposition | concrete change | owner, when |
|---|---|---|---|---|
| F1 CRIT | new partition invalidates table memory | **ADOPT + D-19** | (a) `setup --count-only`: block histogram, C and exact byte accounting at every design, at p = 10⁶ for n = 200/400/1000, before allocation; (b) a deterministic `--mem-budget` refusal; (c) streamed table build (logm/routes never global); (d) D-18; (e) **D-19: V-1M caps blocks at B_V = min(B, 14)** at every n (the theory mode keeps the coded B), so C ≤ 1.17·10⁹ even at n = 1,000 (option D) and logr ≤ 9.4 GB; (f) task memory set from the accounting, not a guess | WP2 now; before any 10⁵ setup |
| F2 CRIT | per-thread full stores unbudgeted | **ADOPT** (design done in v0.1.2) | Tests: one worker supplies all winners; flush-order permutations. G ≤ 256 enforced (order arrays ≤ 1 GB at 10⁶). Peak-live accounting of buffers, RB scratch, compaction and checkpoint buffers in `--mem-budget`. Calibration process budgeted with its 3 stores (top + 2 leaders) and 4 diagnostic islands | WP3/WP4; before their PRs |
| F3 MAJ | cost confidence; serial calibration latency; I/O | **ADOPT** | c = 2 µs relabelled as a planning scenario; measured kernel numbers added. T5 becomes an **end-to-end NOTS gate** (one full stage with permutations, all moves, RB, stores, checkpoints; setup and calibration timed separately), ≈ 100–200 core-h. **One costed cell/seed manifest** (`MANIFEST_CELLS.md`) replaces the tier totals. Calibration on a whole node (2 sockets) or 4 concurrent tasks, chosen by measurement. Scratch: two checkpoint generations ≈ 90 GB per 1M fit (no quota; the offload moves records out within 24 h). **Schedule reserve: 4–6 weeks of engineering**, not 3–4 (see below) | Eng manager (manifest); WP3/WP5 (T5) |
| F4 MAJ | RNG, event order, counter contracts incomplete | **ADOPT** | INTERFACES v0.1.5: an injective RNG domain (tier, iteration, island, stage/round, destination particle, position, slot taxonomy; widths and overflow); the event key with tier, iteration and within-step ordinal, provenance by the serial reference traversal, table/inherited multiplicity replayed; logical events by mechanism (a Gibbs step = held + flip); **spec invariant I4 corrected**; Sol's preservation table adopted as the contract wording | WP1 (contract), WP3/WP4 (code) |
| F5 MAJ | T1–T8 gaps | **ADOPT** | T1 edge cases + sampled Gram oracle at p ≥ 10⁵. T2 pins both the archived revision-D records and the chosen reference. T3 on canonical semantic payloads, with late winners and flush orders. T4 splits the RNG substitution from each Δ, with **pre-declared practical margins and power** instead of non-rejection. T5 end-to-end with thresholds. T6 adds kills during checkpoint writes and calibration restarts. **T8 corrected**: tests E[Ẑ_r] = Z and the proved unnormalised RB moment, plus a finite-N bias ladder for PIP_eq, not "PIPs within 3 s.e." | all WPs; spec §5 v3 |
| F6 MAJ | precision not designed | **ADOPT** | The **64-island precision study is mandatory** (moved from the Full tier into the plan) on overlap datasets incl. weak and ADJ-OPP: N ∈ {2,500, 10⁴} × coarse/refined frozen grid, independent calibration and final seeds; stage records, ESS, ancestors, store lower bounds, PIPs, predictive. **Reserve 1–2k core-h** (re-sized from G0 stage costs). The settings are frozen from it before the final runs. Uncertainty is reported across independent fits. No weight clipping, no median log Z, no island selection. **"High precision at 1M" is claimed only if the study supports it** | Eng manager; before G-B |
| F7 MAJ | cells/replication underspecified | **ADOPT** | `MANIFEST_CELLS.md`: exact cells, seeds and costs per rung (ADJ-OPP mandatory at 10⁴ and 10⁵; the 1M second seed a named row or dropped). The pilot counts as replicate 1 only if the frozen config is unchanged. The PIP curve is labelled a repeated-sampling diagnostic, plus exact-PIP error at small p. Dataset-clustered intervals. ADJ-OPP fully specified (adopted WP1 layout). 1M C5 claim = an accuracy point consistent with the lower-rung trend | Eng manager |
| F8 MAJ | competitors unvalidated | **ADOPT** | A harness acceptance run per retained competitor (pinned versions, data path, tuning, prediction, cost counted) at 10⁴ first; R packages installed in the department folder on NOTS (light; list in PR #12); the core comparison set per p as Sol's table; failures and timeouts reported as outcomes; common-refit vs native predictive labelled | WP5 + Eng manager |
| F9 MAJ | DIST evaluator error control | **ADOPT** | Sol's fixture list (identical densities, shifts, zero signal, empty support, centring, unequal scales, finite mixtures, near-constant branch); quadrature/x-draw doubling to a pre-declared absolute tolerance; native log-score validated separately. **Z_𝒯 ≤ Z is the only deterministic bound; Z_𝒯/Ẑ is a noisy diagnostic, never clipped, never a certificate of P-STORE** (wording fixed in OD-15/D-8 and the plan). The omitted mass is reported as a SUM; the law is called a truncated approximation (D-17 already reports the tail mass) | WP5 (PR #12 fixes) |
| F10 MAJ | reference contract vs owner scope | **ADOPT (HQ confirmed)** | **A pinned reference configuration**, separate from V-1M: core at an exact commit (incl. the anchored-standardisation branch), source, compiler, flags and libm hashes, fixtures and manifests. Compat differences recorded against both the archived revision-D outputs and the pinned reference. The overlap compares the **whole V-1M** against it; no claim of theorem transfer from agreement | WP1 (manifest field), Eng manager (spec) |
| F11 MIN | qualifiers | **ADOPT** | "3/3 → one-sided 95% lower bound 0.37 (two-sided: 0.29)"; the graph bound is ≤ pB selections / ≤ 2pB adjacency entries, with no per-column maximum; a hub edge guard | Eng manager (docs), WP2 (guard) |

## Effect on approved numbers (H-1: report a move above 15% before releasing the affected stage)
- **Core-h per fit: no move yet.** The measured kernel supports the plan; T5 will confirm end to end.
- **Additions to the A+D envelope:** precision study 1–2k (was 950, i.e. +0.1 to +1.1k), T5 end-to-end pilots ≈ 100–200,
  competitor acceptance runs ≈ 100. Net change ≈ +0.3 to +1.3k on ≈ 24.6k (+1 to +5%). Below the 15% threshold; it will
  be confirmed by the cell manifest.
- **Memory per task: moves.** Island task ≈ 24–32 GB (logr ≤ 9.4 GB + store 5.4 GB peak + X 1.6 + buffers and RB + order
  ≤ 1 GB + checkpoint buffers); **calibration task ≈ 48–64 GB** (3 stores + 4 diagnostic islands), against the 32 GB
  planned. Within the 2,304 GB user cap. Reported to HQ before 10⁵ (as H-1 asks).
- **Schedule: moves.** Sol estimates 55–80 agent-days (vs 45) and 4–6 working weeks. With 5 builders in parallel since
  11-15, the realistic dates are: 10⁴ pilot ≈ early December, **10⁵ rung ≈ mid-December, first 1M fit at risk for
  "before the holidays"** (late December or early January). Reported to HQ now.
