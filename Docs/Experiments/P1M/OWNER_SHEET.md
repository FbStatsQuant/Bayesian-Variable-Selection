# OWNER SHEET — p = 10⁶ experiment (Engineering manager, 2026-11-15)

> **DECIDED (HQ, 11-15, delegated by the owner):** budget A + D ≈ 24.6k (the D cell conditional on the 10⁵ π̂(S₀) trend);
> §2, §3 and §4 approved as written. Recorded in DECISIONS.md H-1 to H-4.

These are the items the owner keeps (POLICIES §7–§8); technical items are decided in `DECISIONS.md`. Basis:
- `ENGINEERING_SPEC.md` v2 §0-v2;
- `FEASIBILITY_fable.md` (verdict: **a plan exists**; no NOTS obstruction);
- `FEASIBILITY_disposition.md`.

The Sol review of EXP-CP1 is still pending. If it changes a number below, the sheet is updated.

## The answer to "can p = 10⁶ run?"
**Yes, as an engineered variant (V-1M).** Same target posterior on all 10⁶ variables, no screening, 16 islands + merge.
The main enabler is a batched kernel measured on Owls at 8–15× the current step speed. A precise 1M fit is ≈ 963
billed core-h and ≈ 2.2 h of wall time at your 1,536-CPU cap. Three measurements come first (gate G0: ≤ 5 + ≈ 60
core-h on NOTS). If the kernel turns out slower on NOTS, the fallback is a "baseline precision" 1M with 3 fits.

## 1. Budget tier (OD-7)
| option | core-h | what it buys | recommendation |
|---|---|---|---|
| **A: plan** | **≈ 20.5k** (16.4k + 25% contingency) | gates; 5k anchor; 10⁴ overlap (10 datasets × 2 seeds, T vs V); precision study; 10⁴ science (n-trend, designs, ablations, null); 10⁵ rung (12 fits); **1M: 5 precise fits (AR × 3, ADJ-OPP, AR-weak) + one N = 10⁴ check**; competitors | **recommended** |
| B: plan + 10⁵ overlap with the theory's method | ≈ 26.6k | as A, plus one dataset where the theorem-covered method itself runs at 10⁵ (≈ 6.1k: it escalates and needs N = 10⁵) | only if you want the anchor one rung higher |
| C: minimal | ≈ 7k (5.1k + 25%) | gates, anchor, 10⁴ overlap, 2 precise fits at 1M | if the budget must stay small |

**Option D (add-on to A or B): one or two 1M cells at larger n**, so that a "recovers S₀" statement with a concentrated
posterior becomes possible (HQ request, 11-15).
- **Cost per precise 1M fit, by n.** Planning; the n-dependence is a guess until G0.
  - Step cost c ≈ 3·c_s + 30 ns, with the products growing linearly in n: c_s ≈ 30 + 60·(n/200) ns. So c ≈ 300 ns at
    n = 200, ≈ 570 at n = 500 and ≈ 1,020 at n = 1,000.
  - At n ≥ 256 the block size rises from 14 to 16, so the start tables grow ≈ 10× (≈ 2·10⁹ codes: ≈ 50 GB shared per
    node, 64 GB per island task). X is 4 GB at n = 500 and 8 GB at n = 1,000.

| cell | core-h per precise fit | wall time at the cap | memory (16 tasks) |
|---|---|---|---|
| n = 200 (plan) | ≈ 963 | ≈ 2.2 h | 512 GB |
| n = 500 | ≈ 1,800 | ≈ 4 h | ≈ 1 TB |
| n = 1,000 | ≈ 3,300 | ≈ 7 h | ≈ 1 TB |

- **What it buys.** Theory gives 1 − π(S₀) = O_P(√(log n / n)), so concentration is slow. The expert's draw at n = 200
  gave π(S₀) ≈ 0.3–0.45. Scaling the null-inclusion mass like n^{−1/2} gives roughly 0.45–0.6 at n = 500 and 0.55–0.7
  at n = 1,000 **(guess)**; π(S₀) ≥ 0.9 needs n in the low thousands.
- **What already holds at n = 200.** HPM = S₀ (the reported-model theorem) can hold while π(S₀) < ½, as long as S₀ is
  the single most probable model. The 10⁵ rung measures π̂(S₀) and P(HPM = S₀) at n = 200 and 400, before any 1M cell is
  committed.
- **Recommendation.** Add **one 1M cell at n = 1,000** (AR-strong, 1 fit ≈ 3.3k; ≈ 4.1k with contingency), conditional
  on the 10⁵ rung. It is the strongest single addition to the paper. With A this totals ≈ 24.6k; with B ≈ 30.7k (just
  over the 30k limit, so B + D would need n = 500 instead: ≈ 28.9k).

Released stage by stage at the gates; each gate re-sizes the rest from measured costs.

## 2. What "validated against the theorem-covered method" means in the paper (scope rule (c))
Recommendation:
- **bits at p ≤ 5k**: the existing unmodified code against the new engine;
- **law and output agreement at 10⁴**: same datasets, 2 seeds; selection, PIPs, evidence and the predictive within
  stated tolerances;
- **exact agreement at p ≤ 25** with full enumeration;
- **a 1M self-consistency check** (N = 2,500 vs 10⁴).

The theory's method as coded cannot run at 10⁴ inside 24 h (its calibration escalates at p ≥ 5k), so at 10⁴ it runs in
the new engine with the same law.

## 3. Evidence at 1M (paper wording)
The tempered SMC evidence is imprecise across islands at large p (sd ≈ 1 at 5k–20k). Recommendation: report a
**store/occupancy evidence** (precise, consistent, but no theorem yet), together with a **deterministic lower bound**
and the unbiased SMC estimate, and label each clearly. Selection, PIPs and the predictive do not depend on it.

## 4. Competitors and framing (OD-10)
- **Competitors:**
  - lasso / MCP (biglasso), L0Learn, SuSiE and varbvs at all rungs;
  - BAS / MCMC at 10⁴;
  - SIS → our method;
  - millipede on CPU at ≤ 10⁵.
- **Framing:** "joint model-space SMC with PIPs at p = 10⁶ on individual-level data". The literature has 7.5·10⁵ (GPU
  MCMC, synthetic columns), 2·10⁶ (mixture Gibbs, not model-space) and 5·10⁵ (split-and-merge). So the wording is
  "not found in the literature", never "first".
- One caveat for the wording: at n = 200 and p = 10⁶ the posterior is not concentrated on one model (π(S₀) ≈ 0.3–0.45
  on a synthetic draw). Claims at 1M are worded as accurate posterior summaries (PIPs, HPM, predictive), not as
  "recovers S₀ with probability 1".

## Decisions requested
1. Budget option A, B or C, and whether to add D (a 1M cell at n = 1,000, or n = 500).
2. Approve the meaning of "validated" in §2.
3. Approve the evidence wording in §3.
4. Approve the competitors and framing in §4.
