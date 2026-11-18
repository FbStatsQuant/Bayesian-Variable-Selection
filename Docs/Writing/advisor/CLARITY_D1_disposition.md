# Disposition of CLARITY_D1_opus.md (manager, 2026-11-16)

**Re-implementation gaps closed from the code:**
- Grid construction: `v3_calib.h:60-98`; the grid refines the pilot temperatures, every rebuild starts from them, and convergence is exact equality (`v3_calib.R:44-130`).
- Calibration control flow: a failed step-3 grid skips the rebuild loop; at tier 1, triggers are only recorded; an unconverged grid is used as it is; the fallback is tier-1 only; with the fallback on, a grid always exists. Search caps ℓ_n, from the best model found so far (`v3_core.cpp:642,689`).
- The three stores (`v3_ledger.h:72-78`).
- Block partition: top-down split of oversized clusters, next-fit packing in leaf order (`v3_blocks.h:121-141`).
- Exact sampler: backward split formula, and the within-block draw restricted to the allotted size (`v3_start.h:136-176`).
- Symmetrisation by union (`v3_blocks.h:146-172`).
- Uniform swap: "full" means [p].
- Random order drawn per particle and per round.
- E2 uses the sample s.d. of 4.
- The non-negative SS form.

**Consistency:**
- Stage numbers removed from the headings; "stage" means pipeline only, "step" means a temperature step.
- Start mode taken out of figure box 3.
- "Evidence" kept for Z, and "marginal likelihood relative to the empty model" used elsewhere.
- N(j) → 𝒩(j); V → 𝒱; ψ, ρ.
- exp{φ(d′−d)}.
- π_φ invariance.
- "With/without estimates".
- The exact case's outputs listed.
- PIPhat added to what is reported.
- "Fixed" → "numerical constant" where it meant independent of (n, p).
- {1,…,2³¹−1}.
- Raw X^r explained.
- "Score" defined.
- Global-certificate wording.
- The "none" rationale given per group.
- Appendix B completed.
- Appendix C marked internal.
- **TAB bug fixed:** a control character from the manager's own edit script; all documents scanned, and none remain.

**Not applied:**
- 2.3 (notation used only in the companion part): a note was added instead of removing the notation.
- 4.11 (the r collisions): r_b, r_{jl} and the island index r are kept, as they are standard and each is defined.
- 4.32 (example reproducibility): it is labelled an illustration.
- 1.7 (rationale for the exact threshold): no source for a rationale, so none was invented.
