# API-RESID: synthesis task 8 (RESID-STEP0)

This spec is copied verbatim from `theory/W8-SYNTH:theory_campaign/W8-SYNTH/SYNTHESIS.md` §8, task 8. Run `git fetch origin` and read the branches it names.

### 8. RESID-STEP0: the free post hoc start-table check (data, Owls/R; from F-SIGMA §10)
- **Step 0:** recompute the start tables from the saved fits of the 2,400 PROD-H datasets for:
  - common σ̂² ∈ {σ̃²_{S̃₀}, C-fix, s_y²}. Expect flooding; stop if seen.
  - residualised/backfit tables (O-DILUTE `resid`).
- **Report:** π₀(S₀), π₀(R₂), the start mode, per cell.
- **No SMC runs.**
- **Why:** it settles §4.5 on the real fits, and tells Felipe whether a start change aimed at dilution is worth an investment-rule pilot.

**Data location (Owls).** The 2,400 regenerated PROD-H datasets and the LS0 outputs are in `/home/fb31/ls0_work/` (see `theory/O-LS0:theory_campaign/O-LS0/` for the scripts and the file layout). Use them; do NOT regenerate datasets or rerun fits. All computation goes through `/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- <cmd>`.
