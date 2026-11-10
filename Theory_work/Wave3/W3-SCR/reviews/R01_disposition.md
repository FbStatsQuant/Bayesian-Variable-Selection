# R01 (statement lock, gpt-6.1-sol high) — disposition

Verdict received: **DO-NOT-LOCK** (1 blocker, 3 major, 3 minor, 5 notes). Report: `R01_statement_lock_sol.md`
(verbatim, written by the reviewer). All findings accepted; STATEMENT.md → v2.

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | BLOCKER | A1 with q_n = 0 has no control of log p (counterexample with log p ~ n²) | **Fixed.** A1 now requires (q_n + 1)·log p + log n ≤ c₁n with explicit c₁ = κ²b²/(200(M² + σ²)) (L3). |
| 2 | MAJOR | SCR-C with growing s₀: LO supersets exist under the displayed floor (size prior charges log((2p−k)/k)) | **Fixed by restriction.** SCR-C now assumes s₀ = O(1) (as in the chapter); the size-aware non-asymptotic inequality (EC) of L5.1 is kept for general s₀ and uses the exact log((2p−k)/k). The statement records that the floor is not sufficient for growing s₀, citing the reviewer's construction. |
| 3 | MAJOR | SCR-N: c_n(x) undefined when u_n > 2 | **Fixed.** SCR-N is now stated with the exact threshold B_n = ((n+1)/n)(n − 0.98)(1 − exp(−L_n/(n+0.02))) (reviewer's suggestion); no Taylor truncation; n ≥ 3. |
| 4 | MAJOR | (A∞) drops log s₀ from r_n while allowing growing s₀ | **Fixed.** Deterministic witness t(S) (L2): one Gaussian per S, r_n = √(2 log(2N_q) + 2x). No log s₀ anywhere in SCR-A / (A∞). |
| 5 | MINOR | 𝒞, empty intersections, empty floor family, integer q | **Fixed** in STATEMENT §0-§1. |
| 6 | MINOR | "Changes vs the card" overstated primitive ⇒ visibility | **Fixed**: Lemma B gives lower bounds; A1 / A1° carry the coefficient and growth conditions. |
| 7 | NOTE | CC1-CC5 pass; exact branch is "enumerated maximiser", not a scanned centre | Wording adopted in STATEMENT §0 (CODE_CHECK CC2 already says so). |
| 8 | NOTE | Independent derivation agrees with T_n, MC and the probability | — |
| 9 | NOTE | B1, B2 hold (independent ridge proof) | — |
| 10 | NOTE | SCR-R valid; it is about a refit the method does not output | Label added to the corollary. |
| 11 | NOTE | SCR-N algebra sound; consequences need explicit sequences; transfer to the coded output not automatic | L6 now proves both consequences on explicit sequences (the reviewer's), and states that they concern LO models, not the reported model. |
| 12 | MINOR | Scope: fixed standardised design; σ; p = retained columns; n ≥ 3; Gaussian-row example needs the correlation matrix; `scr_lib.py` prior normaliser | **Fixed**: STATEMENT §0, §3; `scr_lib.py` now uses the core's W_K = Σ C(p,k)w(k) and N0 was rerun (max abs F difference 6.0e-13 over 16,004 models, `numerics/n0_out.txt`). |

Additional change made by the lead in v2 (not requested by R01): the self-normalised refinement **SCR-A°**
(normalised visibility Ψ_n, residual scale σ_S), bridge B2°, Corollary A1° (beta-min at the rate σ√(log p/n)).
Reason: N3's end-to-end check showed MC is driven by the total scale τ_n; the refinement replaces it by the residual
scale of the model at hand. v2 goes to a fresh re-lock (R01b) and to the "better theorem" review (R02).
