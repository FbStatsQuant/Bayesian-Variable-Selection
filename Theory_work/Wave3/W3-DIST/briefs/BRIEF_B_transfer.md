# Stream B (Claude Opus 5.5) — folder `work/B_transfer/` — Lemmas H and T, and Theorem DIST-3
Read `briefs/COMMON.md` first. Context: STATEMENT §0, §1 (DIST-3), §3 (Lemma H, Lemma T); ROUTES §2 Steps 1–2 and §3;
API_CARDS card T; `Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md` (D0, D1 — computations to re-derive, not to cite as
premises).
1. `H.md` — Lemma H with a complete proof, including the in-sample identity n⁻¹ΣΔ_i² = ε̄² + ‖μ̂ − μ‖²/n when some true
   columns are constant in the sample.
2. `T.md` — Lemma T exactly as stated (1 ≤ d ≤ min(p_raw, n − 1), the stated remainder η²_n(d, δ)). The relative
   deviation inequality must be **proved in the file** (symmetrisation with a ghost sample, for a class of sets with
   growth function S(·)), or quoted from a reference you can state verbatim with theorem number — if the provable
   constants differ from "4·S(2n)·exp(−nη²/4)", prove the version you can and adjust η²_n in a STATEMENT-CHANGE REQUEST
   (a change of absolute constants only is expected to be acceptable). Include: the growth-function bound for unions
   of two affine half-spaces on at most d coordinates; measurability of the supremum; the layer-cake and
   Cauchy–Schwarz step; the final inequality for all (a, u, c) simultaneously.
3. `DIST3.md` — Theorem DIST-3 (the oracle display with additive δ_n and the in-probability corollary) with a complete
   proof, fixed design first, then integrating over the design; constants explicit in (s₀^r, σ*², M, B, C_T, κ₀).
