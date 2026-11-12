# K01 disposition (break review, gpt-6-astra high, codex, blind; review `K01_break_astra.md`)

Verdict: **no numbered claim broken** (S, A, A1, A2, A3, B, B1–B3, C.1–C.3 all NOT-BROKEN; each derived
independently by the reviewer). Findings: 0 FATAL / 2 MAJOR / 1 MINOR / 0 NIT; two PROPOSALs.

| finding | disposition |
|---|---|
| F1 MAJOR — experiment E2 of `numerics/a_orth.py` (growing s₀) used θ_j = 1, so ‖μ‖²/n ≈ s₀ → ∞: outside (E) | **Applied** as prescribed: θ_j = 1/√s₀ (‖μ‖² = n − 1, ‖θ*‖² = 1); description changed; the whole script re-run so that `a_orth_out.txt` matches the final script. Claim A2 itself was not affected (reviewer: satisfiable, same example). |
| F2 MAJOR — ASSUMPTION_MAP rows for (W-orth)/(W-sph) promoted a one-step (lower-bound) boundary experiment to "FAILED-REMOVAL … the log factor disappears" | **Applied** with the reviewer's wording: evidence about the one-step mechanism only; failure of Proposition A's full conclusion without the witness condition is "not established". No FAILED-REMOVAL verdict is recorded. |
| F3 MINOR — "equivalently π(S₀) ≤ √n/(√n + c)" drops the higher-order terms | **Applied**: "equivalently π(S₀) ≤ 1/(1 + 𝒪^{lb}_n), and in particular π(S₀) ≤ √n/(√n + c(p, s₀))" (STATEMENT v1.2; `lemmas/B_sparsity.md`). |
| P1 PROPOSAL — at s₀/√n → λ, s₀/p → 0: limsup π(S₀) ≤ e^{−λ/2}, deterministically | **Adopted** (inside brief item (b); a paragraph): STATEMENT v1.2 B1 "critical scale"; proof in `lemmas/B_sparsity.md`. Strictly improves the caps 1/(1 + λ/2), 1/(1 + λ/3). |
| P2 PROPOSAL — in (W-sph) replace (s₀+1) log N = o(n) by (rank X_{S₀} + 1) log N = o(n) | **Adopted** (the proof already bounds the noise term by χ²_{rank}): STATEMENT v1.2; `lemmas/A_log_factor.md` §4. |

Numerical-audit remarks of §5 (no label): "exact" in `a_orth.py` means an exact formula evaluated by quadrature, with
sizes above s₀ + 60 omitted in large runs (disclosed in the script; V2 checks it on affordable cases) — wording kept
as "exact up to quadrature error; lower bound when sizes are truncated" in the lemma files and REPORT. The (c)
simulations use k = 16–22, not ⌈12 log n⌉, and b below the theorem's signal constant: they show the mechanism, not a
finite-n verification of every hypothesis — stated so in `lemmas/C_counterexample.md` §5 and REPORT.

Both adopted proposals change the statement after the lock (v1.1 → v1.2). They are covered by fresh reviews in CP2:
the Sol line checks read the v1.2 statement and the new proof steps, and the council reads the frozen v1.2.
