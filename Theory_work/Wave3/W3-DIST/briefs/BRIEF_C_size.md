# Stream C (Claude Opus 5.5) — folder `work/C_size/` — Lemma S, Lemma V, and steps X1–X2 of Lemma X
Read `briefs/COMMON.md` first. Context: STATEMENT §0, §3 (Lemmas S, V, X); ROUTES §2 Steps 3–4; API_CARDS cards S, V, X;
`Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md` (the proof Lemma S re-runs), `W3-POST/lemmas/L1a_size_tail.md`,
`W3-POST2/lemmas/D_hellinger.md` (D1), `Theory_work/Wave3/W3-DIST/work/prior_probe/REPORT.md` §3 and A2–A3 (Lemma V and
Theorem P, helper-derived, unchecked), and [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
(`lem:num`, `lem:den`, `thm:Ta`, `thm:T01iii`, `lem:slab`, `lem:spec`; locked — may be cited).
1. `S.md` — Lemma S exactly as stated (reference-adaptive; no p ≤ n^A), then the corollary for T = S₀, ϑ = θ*: m = m_n(t)
   qualifies for log n ≤ t ≤ n^{1−κ₀}, any s₀ ∈ {0, …, s₀^r}, with one n₀. Replace every Markov/Chebyshev step of Claim B by
   an explicit χ²/Gaussian tail; give the exponential bound for the s_y-bracket event.
2. `V.md` — Lemma V (a), (b), (c) with a complete proof (verify the helper's A2 line by line; fix what is wrong), valid
   for singular Gram matrices, duplicated columns, s₀ = 0 and |S| up to K.
3. `X12.md` — steps X1 and X2 of Lemma X as in ROUTES §2 Step 3: the noise event 𝓔_t with its four parts and
   P(𝓔_tᶜ) ≤ e^{−t} for all t in [M₀ log n, n^{1−κ₀}] (one n₀), and, on 𝓔_t, for every model with |S| ≤ d and ridge loss
   L_S ≤ C″σ*²t (d any integer with d·log p ≤ C‴t): Π(‖μ̂ − μ‖² > Cσ*²t or |v/σ*² − 1| > C√(t/n) | S, y) ≤ e^{−ct}, with explicit
   constants as functions of (C″, C‴, s₀^r, A, σ*², M, M′). Also give the deterministic bounds on Q^c_S − ‖e‖² and on
   ν/(2b + Q^c_S) that the lead's steps X3–X4 will use (state them as numbered facts).
