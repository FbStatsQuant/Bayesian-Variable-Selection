# RIBOFLAVIN_ETA: expected run time of the 5 running fits (ribo-s1..s5), 2026-11-19 15:10 CST (Sonnet, read-only; HQ owns the decision)

**Bottom line.** Each fit has run ≈ 30.1 h (start 11-18 08:37:53). Two outcomes, split by whether calibration escalates to tier 1:
**no escalation → 25–42 h total (P10–P90; median ≈ 33 h → done between now and 11-20 ≈ 02:40);** **escalation → 63–142 h (median ≈ 84 h ≈ 11-21 ≈ 21:00).**
Because all five are still running, escalation is the likelier case (≈ 70–90 % by my priors). Finish before the 120 h limit (11-23 08:38) is **likely, not clear: P(< 120 h) ≈ 0.85, but the P90 ≈ 130–145 h exceeds the limit.** Judged by CPU/wall alone, the 60 h re-plan point is informative: a unit still running at 60 h is escalated with near certainty; its median ETA is then ≈ 86 h (P10–P90 67–146 h; P(< 120 h) ≈ 0.84).

## 1. Settings read from the frozen core (tag method-v3.1.1, `core/v3_fit.R`, `v3_preprocess.R`, `v3_calib.R`, `v3_run.R`)
n = 71, p = 4,088, K = 35, B = 8, ℓ = 13 (rebuild cap), L = 7, N0 = 4,088, H0 = 838, T0 = 1,000 (a cap, the real grid is ≈ 30–60 stages). Tier 1 = 4× (N, H, T). **Single-threaded** (one core each, pinned, OMP/BLAS = 1).
Structure: pilot (1 island, H0) → up to ℓ diagnostic rebuilds (4 islands × H0 each) → [E1/E2/E3/grid_unconverged → **escalate once** to 4×(H, N), whole calibration repeated] → 4 final islands of N. One round = every particle × (p + B + 2) = 4,098 moves; `rb_fit.R` prints no progress by design.
Island time = N · (p+16) · (G·c_b + (L+4)·c_post); fit = pilot + I·4·island(H) [+ pilot(4H) + I1·4·island(4H) + 4·island(4N)] (formula of W3-SCALE DESIGN_v1 §1, fit on 3 measured islands to ±11 %).

## 2. Calibration of the per-move cost
| Source | where | p, n | µs per move (bridge) | stages G (final grid / pilot) | rebuilds I |
|---|---|---|---|---|---|
| rr2400, 120 NEW fits (own extraction, `tmp/20261119-riboeta/rr_summary.csv`) | NOTS SPR | 500 / 1,000, 200 | 1.40 / 1.62 (all phases) | 32 / 25 | 4 / 6 (median) |
| W3-SCALE profile (`profile_v31_step_cost.tsv`, `profile_v31_stages.tsv`) | NOTS SPR | 1k–20k, 200 | 0.90–1.19 bridge, 1.6–1.9 terminal | 26–33 / 20–28 | 5 (1k), 8 (2k), 11 (5k, then escalated) |
| W3-SCALE p = 5k fit | NOTS SPR | 5,000, 200 | — | 33 | 11 + 1; total **12.2 h** (cal 5.4 h, final tier-1 6.8 h) |
| Same paired fit, Owls vs NOTS (`RERUN_2400_PLAN.md:60` vs `rerun2400/verdict/per_fit.csv`) | Owls ≈ load 21 | 500 / 1,000, 200 (S1 r001 c100) | 691 s vs 357 s; 1,781 s vs 917 s | | **Owls = 1.93×** |
| **This probe: seed-1 tier-0 pilot on riboflavin** (`probe.R`, `probe.log`) | **Owls, now (load 20–29), nice 19** | **4,088, 71** | **8.1** (1,367 s for 1.68e8 moves) | **pilot 49 stages** (study 19–30) | n/a |

Probe: a separate single-core process in a private core copy, 23 min; ribo-s1..s5 untouched. Seed 1 and the same code, so the pilot is the first step of `ribo-s1`.
Scaling used: moves ∝ N · p per round (N0 = max(2500, n, p) grows with p), per-move cost taken as **measured on riboflavin on Owls (8.1 µs)**, terminal rounds 1.0–1.8× that; final grid G ≈ 8 + 0.97 · pilot length ≈ 55 (±6; fitted on the 120 rr2400 fits, R² = 0.74).

## 3. Derivation (Owls hours, c_b = 8.1 µs, c_post = 1.4 c_b, G = 55)
| piece | hours |
|---|---|
| pilot tier 0 / one diagnostic rebuild tier 0 / four final islands tier 0 | 0.38 / 2.2 / 10.6 |
| pilot tier 1 / one rebuild tier 1 / four final islands tier 1 | 1.5 / 8.7 / 42.5 |
| **no escalation**, I = 7 / 11 / 13 | 26 / 35 / 39 |
| **escalation**, I0 = 11 (I1 = 1 / 3), I0 = 13 (I1 = 1 / 5) | 77 / 95 / 82 / 116 |
Monte Carlo over c_b (±15 % lognormal), c_post/c_b U(1, 1.8), G ~ N(55, 6), I0 ∈ 7–13 (13 forces escalation), P(escalate) 0.5–0.8, I1 ∈ {1: .5, 2: .2, 3: .1, 5: .1, 13: .1} (`mc.py`): non-escalated P10/50/90 = 25/33/42 h, escalated 63/84/142 h. Priors for I0, I1, P(escalate) are my judgement (W3-SCALE: 1 profile per p; at n = 50, p/n = 5–10 escalation was 103/105 and 16/16 (`p6_E2_by_np.tsv`); riboflavin has p/n = 58 and a pervasive correlated factor).

## 4. Contention and non-invasive evidence
- Cores: ribo-s1..s5 are pinned to CPUs 67, 70, 71, 73, 74 (socket 1). `mpstat` shows ≈ 99.5 % busy each and their **SMT siblings (27, 30, 31, 33, 34) 100 % idle**: no hyper-thread sharing; `ps` CPU time ≈ wall (29.96 h CPU in 30.07 h) → no throttling. nproc = 80 (Xeon Gold 6148, Skylake 2.4 GHz, 2×27.5 MB L3); load 20–29 is mostly other users' R jobs (5 × 99 %, one 267 %) on other cores.
- Memory bandwidth / L3: 5 units each touch a 134 MB Gram + 2×10⁶-entry cache, ≫ L3. Not measurable without a quiet-host A/B; it is part of the Owls penalty above (1.93× at load 21), and the probe saw the same load. Not separable here.
- Progress files: none. `out/` is empty, no DONE_seed*, `log/seed*.log` hold only the start line, the `tmp/Rtmp*` dirs hold only the compiled-cache copy (static since 11-18 08:37). RSS ≈ 0.82 GB (preflight 0.89 GB) does not distinguish tiers. **No non-invasive way to see tier or stage.**

## 5. Why 5–25 h missed (plan: `REAL_DATA_CHECK_PLAN.md` §4: "p^1.6 → ≈ 5 h unescalated at p = 4,088; W3-SCALE p = 5k 12.2–15.5 h; planning 5–25 h NOTS-equivalent, ×1.2–1.5 for Owls")
1. **Per-move cost ≈ 5× too low for this host and data.** The plan's basis is NOTS Sapphire Rapids on synthetic n = 200 data (1.0–1.6 µs). Measured now on Owls on riboflavin: 8.1 µs. Of the ≈ 6.7×, the Owls penalty is ≈ 1.9× (same-fit pairs), not the 1.2–1.5× used (the plan compared an S1 fit with medians); the other ≈ 3.5× is not explained by this analysis (candidates: real data n = 71 with K = 35 models, lower cache-hit rate, 134 MB Gram off-cache on a 2.4 GHz Skylake; untested).
2. **More stages.** Riboflavin's pilot has 49 stages (study 19–30), so the final grid is ≈ 55 vs ≈ 33 (×1.7 on every island). Not in the plan ("T = 30 … how T moves with p is not established", DESIGN_v1 §1).
3. **Escalation is the case, not the tail.** ≈ 29 island-units at tier 0+1 (W3-SCALE p = 5k: 12.2 h NOTS) versus ≈ 15 un-escalated; tier 1 alone (4 islands at 4N) is ≈ 16 island-units, 42 h here. The plan listed it only as a range end.
4. **Calibration is sequential and long**: up to 13 rebuilds × 2.2 h at tier 0 = 29 h before any final island runs; the single-thread design makes the parallel seeds irrelevant to the per-fit time.
5. Not causes: threads (single-threaded as assumed), contention (cores uncontended by SMT, CPU = 99.6 %), LS0 (est. ≤ 0.1 h actual).

## 6. Caveats
Priors for I0/I1/P(escalate) are the weakest part; per-move cost assumes the pilot's 8.1 µs holds for diagnostic/final islands (bridge-like; terminal rounds 1.0–1.8×); different seeds may land on different tiers. A one-off signal: **no DONE by ≈ 11-20 03:00 CST (≈ 42 h) ⇒ that seed has escalated** (≈ 85 % chance, then ETA ≈ 11-21 ≈ 20:00 ± 2 days).
Files: `~/SMC_Engineering_Department/tmp/20261119-riboeta/{probe.R, probe.log, probe_pilot.rds, extract.R, ex3.R, rr_summary.csv, mc.py}` (scratch; no /tmp, no NOTS).
