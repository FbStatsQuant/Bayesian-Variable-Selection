# L01 disposition (lead) — statement lock by Sol on STATEMENT v1.0

Review: `L01_statement_lock_sol.md`. Verdict REJECT; 0 FATAL / 1 MAJOR / 3 MINOR / 0 NIT. The reviewer found no
counterexample to Lemma R′, MIS-R (i), (i′), (ii), Corollaries G, H, Remarks SNR, U within their hypotheses (its
answers 2–8, 11). All findings accepted and applied → STATEMENT v1.1. This is the one fix round allowed by the run
instructions; the changes are re-checked by a fresh Sol reviewer (L02).

| # | grade | finding | disposition | where in v1.1 |
|---|---|---|---|---|
| 1 | MAJOR | Remark P: Theorem F's BM-∞ (`C-MIS/STATEMENT.md:132-133`) is not relative to σ²; with σ²_n arbitrary the literal extension is false (orthogonal p = 2, θ = (1, 0), σ²_n = n²). | **Accepted.** Remark P now says every variance-dependent hypothesis of Theorem F is read relative to σ²_n: BM-∞ as θ²_min nφ₀²/(σ²_n log n) → ∞ (the unnormalised form is declared unavailable, with the reviewer's example); BM(c) and the inclusion threshold with σ²_{𝒞,n}; TAIL^𝒞 on the same posterior; (TL) is a ratio; EP coefficients and residual divided by σ_n. The main theorem is unaffected. | §7 Remark P |
| 2 | MINOR | R′(a″): "in floating point the outputs agree up to rounding" is not a consequence of (a) and is false in general (y = (−1, 0, 1) + 2⁵⁵; overflow); "numerics N0" was not an identified file. | **Accepted.** The floating-point sentence is deleted; (a″) claims only the real-arithmetic target; the numerical run is cited as an observation on listed inputs, with its files. | §1 (a″) |
| 3 | MINOR | Corollary H: "the (centred) conditional law of y_i" and "the KL projection" were not defined (centring of the mean vs of the response; which variables are integrated). | **Accepted.** The reference is defined as the unit-noise comparison law in response units; its meaning under GR is stated (response minus the sample average of its conditional mean; not the law of (Cy^r)_i); the KL reading is restricted to the Gaussian-row setting of Corollary G and to the conditional law given the candidate covariates; no KL statement for fixed designs. | §6 "The reference law" |
| 4 | MINOR | (OS) "implied by (F_w), (DG), (ADG)" in a per-n list hides the onset n ≥ n_OS. | **Accepted.** The class uses the two (OS) inequalities at that n; the bridge is stated separately with its onset and constant dependence. | §0 (OS) |

Conventions the reviewer asked to make explicit (its answer 1), all added in §0 "Conventions": Borel structure on the
configuration space (countable union over p), a fixed deterministic U at each n, a measurable HPM tie rule,
π_𝒞(T) := 0 for T ∉ Ω, zero-padding of θ. Also from its answers 7 and 9: Corollary G(b) now states p_𝒞 ≥ 2 and
σ²_𝒞 > 0; Remark U names the applicable constants.

Not changed: the reviewer's answer 2 notes that (a′) extends to c < 0 with a signed coefficient map; not needed, not added.
