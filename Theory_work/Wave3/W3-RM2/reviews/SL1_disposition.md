# SL1 disposition (lead) — statement-lock review by Codex gpt-6.1-sol (high), blind

Review: `SL1_statement_lock_sol.md`, manifest 1397b036a1eff57d1f6f281c196a9deee176d8da23bab07f86876e8e1e249066.
Verdict: **LOCK WITH CHANGES** — 2 MAJOR, 4 MINOR required; 4 optional. No CRITICAL. All ten items are accepted and
applied; the result is `STATEMENT.md` v1.1 (markers [SL1-#]). No claim (C1)–(C4) was found false; no hypothesis of
(C1) or (C2) changed. What changed in substance: the quantifier on δ₀ in the sufficiency clause (D-R^b) ⇒ (W-R)
(item 1) and the registry block (item 4).

| # | class | finding | action in v1.1 |
|---|---|---|---|
| 1 | MAJOR | (D-R^b) gives (W-R) only for δ₀ < 1 − 2b (example: independent coordinates, Q = [p], p = n^{0.4}, δ₀ = 0.9 fails); Form R constants must not inherit b < β(η, A); (W-unif) could have a negative radicand | §3.2: "(D-R^b) is sufficient for (W-R) **for every fixed δ₀ ∈ (0, 1 − 2b)**"; the same in bridge (P9) and in (C4); §3: constants of Form F and Form R listed separately (Form R: b ∈ (0, ½), no η); (W-unif) now has its own parameter δ ∈ (0, (1 − 2b)/2) and (C3)(c) names it. (C2) keeps an arbitrary fixed δ₀ when (W-R) is assumed directly, as the reviewer allows |
| 2 | MINOR | β_{T∩N_l,l} undefined when T ∩ N_l ∌ S₀ or is empty | §1: β_{B,l} defined for every B ⊆ Q ∖ {l} with invertible Gram, β_{∅,l} = 0, P_∅ = 0; (W-loc) points to it |
| 3 | MINOR | (P0): the contrast set must contain the residual vectors and their differences | (P0): 𝒱𝒱 ⊇ {r_A} ∪ {r_A − r_{A′}}, r_A = (I − P_A)μ, deterministic, nonempty, finite; the events are defined with the new t_n, h_n and their probability bounds are stated |
| 4 | MAJOR | registry block: sufficient alternatives listed as joint assumptions; (L-size-b) called NECESSARY-FOR-ROUTE; no bridge edges; conditions only in prose | §7 rewritten: headline rows list only (W) / (W-R); the sufficient forms are separate rows (W-suff, D-to-W) marked as alternatives; A:L-size-b, A:L-size-b-R, A:H-size-rho = ARTEFACT (sufficient budget; necessity open); A:W = NECESSARY-FOR-ROUTE up to slack, whole-lattice route only; every bridge P0–P9 has a registry id and a `depends_on` edge; the status lines carry "conditional on SOP:TH09 / W2-APP:POST / W1-GEN:L1" |
| 5 | MINOR | polynomial-decay example: sizes are O(n^{1/(2α)}), O(n^{ρ*}) with constants | (C5): b > 1/(2α), ρ > ρ* > 1/(4α), 15ρ + b < ½ (strict slack exactly when α > 17/2); the fixed-design example says "any b > 1/(2α)" |
| 6 | MINOR | statuses of SOP:TH09 and W2-APP:POST quoted as excerpts | §5: full registry statuses copied |
| o1 | optional | "centred Gaussian process" wording | §1: "expected maximum of shifted absolute Gaussian projections" |
| o2 | optional | "0.72" rounding; log(q + 1) ≍ log n only at genuine polynomial order | (W-loc): ν_n ≤ h log n/log 2, h < ½ − b; "when \|Q\| ≥ n^{b′}" |
| o3 | optional | empty pair set; (W-R) on the floor event | §1: 𝔓 = ∅ ⇒ (W) vacuous, no reference family needed; (W-R): 𝒲_n := 𝒲⁰_n ∩ {𝔴_n(δ₀) ≤ 0} with 𝒲⁰_n the floor event |
| o4 | optional | equicorrelated example stays a candidate; fixed-design decay example needs its truth conditions | (C5): "candidate, not verified"; conditions "to be specified with the verification" |

Nothing was declined. The reviewer's checks that matter for the plan (recorded here for the proof legs, not as
evidence of proof): the sandwich's only size-sensitive step is junk exclusion, margin [β(η, A) − b] log n; the toolkit
needs only (q + log n) log n/n → 0 with the same κ_E; the size-dependent level c_n(k) keeps the score margin of
C-GROW L2.2; the converse needs |T| < K (in 𝔓); the median/mean passage for (P9) is legitimate.

Next: the changes go to a reconciliation reviewer (fresh Sol, sees this file and SL1) on a new frozen manifest
(PROTOCOL rule 15: a change to a statement needs a fresh review of the change).
