# API-RESID: RESID-STEP0, the post hoc start-table check on the 2,400 PROD-H fits

Synthesis task 8 (`W8-SYNTH · SYNTHESIS.md §8`), from `F-SIGMA · REPORT.md §10` Step 0 (and Step 2, the residualised
alternative). **No SMC runs. No regenerated data. No refits.** Every number below is a post hoc recomputation of the
start law π₀ from the production setup (blocks + v3 tables) of the same 2,400 fits that O-LS0 used.

## 0. Answer in brief

- **Common σ̂² (§4.5): settled on the real fits, against.** None of the three feasible plug-ins gives one favourable fit
  (0/2,400 each). The F-SIGMA §10 stop rule fires: C-fix floods to the cap K = 100 in 2,113/2,400 fits, and the oracle and
  s²(S₀) plug-ins flood in essentially all fits. The other two plug-ins do not flood, but they do not help either:
  σ̃²_{S̃₀} destroys π₀(R₂) (median 0.81 → 5·10⁻⁶), and s_y² reproduces v3 to within half a decade. **No SMC pilot for
  common σ̂².**
- **Residualised (backfit) tables, 3 sweeps: the O-DILUTE pilot replicates on the real fits.** Median log₁₀π₀(S₀) goes
  from −15.65 (v3) to −1.07. 1,888/2,400 fits are favourable (O-DILUTE criterion π₀(S₀) ≥ 10⁻⁴), against O-DILUTE's
  378/480 on regenerated data (78.7% vs 78.8%). The start mode equals S₀ in 1,245/2,400 fits, and there is no flooding.
  It is weak in S5 (1–44 favourable per 100) and in S4 at c = 0.5 (74 and 47).
- **But a start change cannot move the study's headline accuracy.** In the study, 1,829 fits recovered S₀ exactly, 565
  were posterior misses (S₀ was scored and lost on the posterior, so no start or search change can report S₀ there), and
  6 stopped on a resource limit, all in S5. The most any start change can add to HPM = S₀ is those 6 fits (0.25%).
  Backfit puts its start mode on S₀ in 2 of the 6.
- **Is it worth an investment-rule pilot?** Only if what Felipe wants is (a) a start that is favourable at the study size
  (for the theorem side: T22(iii)/T38 regime claims), or (b) cheaper or more stable SMC runs. It is **not** worth a pilot
  for the reported recovery numbers. Step 0 caps that gain at 6/2,400, and the change can also cost: in principle it can
  turn an exact recovery into a posterior-mode correction (the same asymmetry S-ELS found for LS0). Two caveats should be
  resolved free, post hoc, before any pilot:
  - 3 sweeps is not shown to be a fixed point (§3.4).
  - Backfit lowers π₀(R₂) sharply in S5 (§3.3).
- **Status, unchanged:** residualised tables remain an **unproven candidate**. No theorem covers them, and T22(iii) would
  need restating. This run adds the real-fit start-law evidence only.

*(Sections 1–5 follow.)*
