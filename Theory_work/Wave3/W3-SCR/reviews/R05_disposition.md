# R05 (v3 delta check + re-lock, gpt-6.1-sol high) — disposition

Verdict received: **DO-NOT-LOCK** for STATEMENT v3 (3 major wording/overclaim findings, 7 minor); the new mathematics
passed: CC6 (with a wording fix), SCR-M, M1, M3, M5, L5 facts, L5.1, L5.2, SCR-C, SCR-R, B2d, A1/A1° edits, L2 edits
CORRECT; M2, M4, L6 edits CORRECT-WITH-MINOR-FIX. Report verbatim: `R05_v3_delta_check_sol.md`. All accepted → v3.1.

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | MAJOR | STATEMENT's M6 summary claimed screening from geometry alone | Fixed: M6 now says a low-dimensional witness span lowers b_𝓗 and M1 applies *provided the gaps are positive*; the L7 example is quoted with its hypotheses. |
| 2 | MAJOR | SCR-G(ii) said the top-level flag is FALSE for a capped search | Fixed: "even if the top-level flag is FALSE (the capped search itself is uncertified; the flag can be TRUE when the other search certified the same model)"; capped archive identified by its own `termination`. |
| 3 | MAJOR | "Reading of L5.1" over-interpreted (EC′) (small α / large ω) | Fixed (L5, STATEMENT): (EC′) is restated as the explicit bounds α ≤ (n/(n²−1))exp(R₁/A − 2 log((2p−k)/k)) (m = 1, A > 0) and ω ≥ A(Λ)₊/R_m, informative only when A is bounded away from 0; no general claim. |
| 4 | MINOR | M4 used κ ≤ 1, false for the directional floor | Fixed with the reviewer's chain κ ≤ φ^d ≤ ‖θ*‖₁²/‖θ*‖₂² ≤ M/b (so κb ≤ M). |
| 5 | MINOR | strict gap needed for SCR-G | Fixed: M4 states δ_S > c₂n; the derivation of SCR-G from M2, M4, M5 is written out after M4. |
| 6 | MINOR | δ_C undefined on 𝓗∖𝓗⁻; empty 𝓗⁻ | Fixed: conventions added (L7, STATEMENT); M2 reformulated; M3 restricted to 𝓗⁻. |
| 7 | MINOR | excess-set paragraph not self-contained | Fixed: m, x, x′, η_n(k, x), U(k, x) given; screening event mentioned. |
| 8 | MINOR | archives exist only for searches that were run; "unscanned" scope | Fixed (STATEMENT §0, CODE_CHECK): "each search that was run (LS0 when enabled)"; "not scanned as a centre by this search"; note on the non-emitting initial centre added to CC6. |
| 9 | MINOR | L6 ratio parenthetical | Fixed. |
| 10 | MINOR | unsupported sentence on the rate of same-truth score differences | Deleted. |

Next: R05b (fresh, sol high) re-lock of v3.1; R06 mid-point (fresh, astra high) in parallel.

## R05b (re-lock of v3.1, gpt-6.1-sol high): DO-NOT-LOCK — one major, three minor; all ten R05 repairs confirmed
Report verbatim: `R05b_relock_v31_sol.md`. All accepted → v3.2.
| # | Sev. | Finding | Disposition |
|---|---|---|---|
| N1 | MAJOR | STATEMENT's M3 omitted the maximising-witness hypothesis that L7's M3 has (counterexample with another witness) | Fixed: the maximising witness is defined in the SCR-M statement; M3, SCR-G and §4 name it; L7 setting clarified. |
| N2 | MINOR | "informative only when A is bounded away from 0" was not a valid gloss | Replaced by the reviewer's wording (L5, STATEMENT). |
| N3 | MINOR | Λ and a_1 not defined in STATEMENT | Defined. |
| N4 | MINOR | §4 interface: gap bound vs gap positivity; bridges need A1/A1° conditions | Reworded as proposed. |
