# LC1 disposition (lemma check, Codex gpt-6.1-sol high) — 2026-11-09

Verdicts: CC VERIFIED WITH AMENDMENTS; PC VERIFIED; MR VERIFIED WITH AMENDMENTS; ST VERIFIED WITH AMENDMENTS; D VERIFIED
WITH AMENDMENTS; LT♯ GAP (LT-f only; LT-a–LT-e verified); C VERIFIED WITH AMENDMENTS. No CRITICAL. Simulator VERIFIED as
a floating-point simulation of T12 §1–§2. The reviewer checked C v1 and LT v1 (before the BT1 amendments); C v2's new
Step 4 and TR are covered by numerics v3 and go to the mid-point/sweep reviewers.

| # | Sev. | Issue | Disposition |
|---|---|---|---|
| 1 | MAJOR | `v3_frozen`'s N/L never reach the engine; wrapper uses budgets | ACCEPTED. STATEMENT §0 "Component vs production" rewritten: arbitrary (N_e, L) = engine component `Engine::run_island`; grid reaches engine via `v3_frozen`; N_e, L always the executed values. CC note updated. No code change. |
| 2 | MINOR | D-iv integrand 1_𝒜 inside exp equals 1 off 𝒜 | ACCEPTED. Q := D_rπ₀(S₀) on 𝒜, ∞ off 𝒜; E[e^{−Q}] → 0. `lemmas/D_theorem.md`. |
| 3 | MAJOR | LT-f "cannot be dropped / not necessary" lack asymptotic witnesses | ACCEPTED (option a). STATEMENT LT-f, `LT_theorem.md` Step 6 and ASSUMPTION_MAP now say necessity is not settled; the probes are finite-n illustrations on artificial targets; asymptotic witnesses left open (REPORT open item). |
| 4 | MINOR | MR overstates engine diff | ACCEPTED. "in the island computation"; other diffs named. |
| 5 | MINOR | ST numerics prose formula lacks 1{j∈S₀} | ACCEPTED (`ST_stay.md`). The simulator computes the right expression. |
| 6 | MINOR | κ₀-sharpness filter omits A_0 = 1 | ACCEPTED: numerical sentence withdrawn; the deterministic equality (ST-b) is cited instead (LT, ASSUMPTION_MAP). |
| 7 | MINOR | W3-POST rate citation moved to :79-80; spell out o₁ = O_P(r_n) | ACCEPTED (STATEMENT P-CONC, `C_theorem.md` Step 6). |

Also noted: sec4b log is a combined log of two invocations (L = 5 and L = 20 rows); labelled as such in RESULTS index.
