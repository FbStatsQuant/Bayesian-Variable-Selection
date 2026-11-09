# L3 — Reported HPM: Corollary H (M5(0) with S₀^𝒞) and Corollary D (never-scored term on the GEN class)

Status (per claim): Corollary H, Corollary D — R02 VERIFIED; Corollary D′ (optional instance) — R02
VERIFIED-WITH-AMENDMENTS (applied). Sweep R06 fixes applied. Council pending.
Inputs (verbatim statuses): M5(0) = T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (SoP
`04_theory.tex:466`); Theorem GEN: "PROVED-CHECKED" (`Theory_work/Wave1/W1-GEN/REPORT.md:20`), with its premises (incl. e4;
N3 "OPEN" as a general invariant, GEN REPORT flag 4).
Notation (M5/T38): 𝒪 output-available event, U = 𝒪ᶜ; 𝒮⁺ the all-scored set; Ŝ⁺ its ≻-maximum under (F, −|S|, lex);
barred objects refer to the potential uninterrupted run (Lemma RO, GUARD-W) — T38 proof
`NBH/branch_snapshots/A-REV5/sources/W4-T38FULL/T38_PROOF.md:16-30`. (The omitted-predictor set is written 𝓜.)

## Corollary H

**Statement.** Fix n, any candidate design and any law of the data supported on valid inputs (non-constant y^r and
candidate columns, so that every score is defined and positive); the M5(0) premises (Lemma RO/GUARD-W coupling,
Ŝ⁺ the ≻-maximum of the all-scored set). Let T be any model in Ω_𝒞, deterministic or a
measurable function of the candidate design (in particular T = S₀^𝒞). With D_n(T) := P(𝒪̄ ∩ {T ∉ 𝒮̄⁺}),
  P(𝒪 ∩ {Ŝ⁺ ≠ T}) ≤ 2E[1 − π_𝒞(T | y)] + D_n(T).
Under Theorem MIS (i)/(ii) (resp. Theorem F) with T = S₀^𝒞 the first term → 0, so
P(𝒪 ∩ {Ŝ⁺ ≠ S₀^𝒞}) ≤ o(1) + D_n^𝒞, D_n^𝒞 := D_n(S₀^𝒞). No discovery or delivery claim.

*Proof.* The T38-(0) proof (`T38_PROOF.md:34-46`) uses, about S₀: (1) Lemma RO(2) (a statement about the run, not about
S₀); (2) on {π(S₀) > ½} every S ≠ S₀ has π(S) < π(S₀) — true for any model T in place of S₀ (π is a probability on
Ω_𝒞, and π(T) > ½ forces T ∈ Ω_𝒞); (3) on 𝒪̄ ∩ {T ∈ 𝒮̄⁺} ∩ {π(T) > ½} the running-best rule returns T (F is
strictly maximised at T; no tie); (4) inclusion of events; (5) Markov's inequality for the [0,1]-variable 1 − π(T),
under whatever law the data have (with T X-measurable, apply it conditionally on the design and integrate, or
directly under the joint law). No property of the data-generating law and no property of S₀ beyond these is used, and
every step is pathwise or Markov. The limit statement: for Y_n = 1 − π_𝒞(S₀^𝒞 | y) ∈ [0, 1], E Y_n ≤ η + P(Y_n > η); convergence in probability
(Theorem MIS (i)/(ii) or Theorem F) and then η ↓ 0 give E Y_n → 0. ∎

## Corollary D

**Statement (fixed candidate design).** Assume GR with fixed X^r_𝒞, the method v3.1 + LS0 as specified (LS0 not in production code — GEN REPORT flag 4) with GEN's
premises (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4, complete scans; IND-T and the c₄ search when R′ > 4), and that
the candidate problem (design X^r_𝒞, coefficients β^𝒞, noise σ_𝒞², truth S₀^𝒞) satisfies GEN's (H0)–(H2) (GEN
`STATEMENT.md` v2.3 §2; (H0) includes BM-∞, so BM(c) alone does not suffice here), or (H0) and (H2) with
S* = S₀^𝒞 — all with σ² := σ_𝒞² **everywhere in GEN** (v_T, E_{T,l}, NL, VIS, BM) and μ := μ^𝒞 (GEN's Δ_T is the residual
energy of μ^𝒞; τ² is not added a second time), on the method's actual candidate-only partition (a function of X_𝒞). Then D_n^𝒞 → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀^𝒞}) → 0, and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀^𝒞}) = 1 − limsup P(U_n). (No delivery claim.)
**Random candidate design:** the same under the joint law, under GEN (C4) (GEN `STATEMENT.md:115`, L5.4) with
the conditional GR of Theorem MIS (ii) (ε′ independent of X^r_𝒞 with law N(0, σ_𝒞²I)).

*Proof.* By Lemma R (L1.1), the joint law of (X^r_𝒞, y^r, uniforms) — hence of the whole run, 𝒪, 𝒮⁺, Ŝ⁺ — equals its
law under GEN's model G with fixed raw design X^r_𝒞, coefficient β^𝒞 (support S₀^𝒞), noise variance σ_𝒞² > 0 fixed.
GEN's conclusions (GEN `REPORT.md:24-41`: D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, liminf statement) are statements about that
law, with S₀ := S₀^𝒞. Random design: GEN L5.4 (`L5_assembly.md:66-80`) defines f_n(x) by integrating over
e ~ N(0, σ²I) independent of X; here replace σ² by σ_𝒞², legitimate because ε′ is independent of X^r_𝒞 with that law;
β^𝒞, S* and 𝒱 may be X-measurable (GEN allows X-measurable β, `STATEMENT.md:115`). ∎

## Instance (optional): a pure proxy on GEN's W family (Corollary D′)

Candidate design: GEN's W family (GEN `lemmas/L6_instances.md:86-110`): groups of nine at within-correlation ¼,
cross-group ε_n ∈ {1/(np), n^{−1/2}/p}, exact Gram, p = 9⌊n^{1/3}/9⌋, n ≥ 9⁶; two variables j₁, j₂ in different
groups; θ_n := n^{−1/4}. Take X^r_𝒞 := the W design itself (columns already centred with unit sample SD, so D_x = I).
**Full model:** y^r = θ_n x_{j₁} + θ_n x_k + ε with one omitted column x_k := x_{j₂} + (τ/θ_n)z, z ~ N_n(0, I)
independent of ε, τ > 0 fixed. So S₀ = {j₁, k}: the candidate j₂ is a **null** of the full model.
**Projection:** ω = θ_n x_k = θ_n x_{j₂} + τz: GR with a = 0, γ = θ_n e_{j₂}, ξ = τz; β^𝒞 = θ_n(e_{j₁} + e_{j₂}),
S₀^𝒞 = {j₁, j₂} (W's truth), σ_𝒞² = σ² + τ² with σ² := 1.
**Claim.** P(𝒪 ∩ {Ŝ⁺ ≠ {j₁, j₂}}) → 0: jointly with output, the reported HPM contains the proxy j₂ in place of the
omitted k.
*Proof.* Corollary D needs GEN's (H0) and (H2) with S* = S₀^𝒞 for (W, θ_n(e_{j₁} + e_{j₂}), σ_𝒞²). GEN L6(c) verifies
them for σ² = 1; its verification uses σ² only (i) in BM-∞: θ_n²nφ₀²/(σ_𝒞² log n) = √n/(2σ_𝒞² log n) → ∞; (ii) in
VIS: g ≥ θ_n²(n − 1)(¾)(1 − o(1)) ≍ √n against M_nv_U log n with v_U ≤ σ_𝒞² + 3n^{−1/2}, so VIS holds with
M_n := √n/(4σ_𝒞² log n) → ∞ for all large n (any fixed σ_𝒞²; factor-three margin, R02); (iii) in NL: by L6(c),
uniformly over the leakage family, δ² ≤ (16/3)θ_n²(n − 1)ε_n² ≤ (16/3)n^{−1/2}·n·(n^{−1/2}/p)² = O(n^{−7/6})
(p ≍ n^{1/3}; the other ε_n variant is smaller) — a bound not involving σ². Hence NL_η(S*) (δ² ≤ ησ_𝒞² log n) holds
for any fixed σ_𝒞² > 0 and fixed η ∈ (0, (√3 − √2)²); and, with h_n = √(2(A + ε₀)log n),
0 ≤ E_{T,l} ≤ δ²/(2v_T) + |δ|σ_𝒞h_n/v_T ≤ δ²/(2σ_𝒞²) + |δ|h_n/σ_𝒞 = O(n^{−7/12}√log n) → 0 uniformly (v_T ≥ σ_𝒞²),
so NL_avg(κ) holds, e.g. with κ = ¼ and any fixed ε₀ > 0. The partition, spectrum, R and SE parts of L6(c) do not involve σ².
Hence (H0), (H2) hold with σ_𝒞² and Corollary D applies with the fixed candidate design W. ∎
*Remark.* With τ fixed and θ_n → 0 the omitted-proxy correlation corr(x_k, x_{j₂}) ≈ θ_n/τ → 0; a version with fixed
proxy correlation needs σ_𝒞² = σ² + θ_n²c² varying with n, which T03♯/GEN (fixed σ²) do not cover as stated (a
uniform-in-σ² reading of their constants is plausible but not claimed).
