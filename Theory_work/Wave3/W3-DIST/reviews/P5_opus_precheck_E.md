# P5 — same-family pre-check, stream E (bridges B0, B1, B2-core, B2, B3; ASSEMBLY of the reader theorems)

Checker: Claude Opus 5.5 (Claude Third), effort high. Brief: `briefs/PRECHECK_COMMON.md` + `briefs/BRIEF_P5_E_precheck.md`.
Files checked line by line: `work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`, `ASSEMBLY.md`, against
`STATEMENT.md` v1.3.1 (§0, §1R lines 118–244, §3 "Bridges" lines 340–368) and `API_CARDS.md` "Common definitions".
Also read: `W3-MISR/STATEMENT.md` §0–§1 (Lemma R′ (a), (a′)), `W3-POST/STATEMENT.md` §0–§2 (m♯_n, R1, (E), (F_λ), (F_w),
(BM), Theorem 1 items 1 and 6), `W3-POST2/STATEMENT.md` Claim D (posterior on the response scale),
`work/E_bridges/bridges_checks.py` and its output, and the comparison attempts `work/api_attempts/dist1/B-a-1.md`,
`B-b-1.md`, `B-c-1.md` (as material, not authority). I did not read `reviews/` (other than writing this file),
`LOG.md`, `CHECKPOINT_*.md` or `DEPS.*`. I did not run the check script, because it writes its output file into the
ticket folder and this check is read-only; I recomputed every constant it checks by hand (and computed n_B
separately in a scratch shell, see E-04).

Given hypotheses (not checked here, as the brief says): the master displays (1.1), (1.2), DIST-3 and Lemma X′, and
W3-POST Theorem 1 (a consumed premise). Every verdict below is conditional on them.

## Summary

No CRITICAL or MAJOR finding. All five bridges are correct as written. I recomputed every constant: c₁ = 1/576,
c₂ = 10⁻⁵, the net constant 0.5436, the window inequality and B3's size inequality. ASSEMBLY proves Theorem A (i), (ii),
the sentence without (A4), Theorem B (conditional, as labelled) and the Example as they are worded in §1R. The findings
are about precision of wording, almost all in STATEMENT's remarks and quantifier conventions rather than in the
proofs: four MINOR, four NIT.

## Findings

**E-01 — MINOR — ASSEMBLY §0 (R-a); STATEMENT §0 lines 63–64, DIST-3 lines 93–97.**
*Issue.* ASSEMBLY rests on reading convention (R-a): the master constants and n₀ do not depend on the law of the data,
and each display is a statement at each fixed n about every law satisfying (RD) at that n. Theorem A's "one n₀" and
"uniform over all laws" depend on it, and so does Theorem B, which uses DIST-3 with fixed (c₃, C₃) along a triangular
array.
Is (R-a) what STATEMENT says? **Essentially yes, but only implicitly.**
- (1.1) reads "There are constants c, C, C′, M₀, n₀ such that, in (RD), for every n ≥ n₀ …".
- §0 (lines 63–64) lets constants depend only on (s₀^r, A, σ*², M, M′ or B, κ₀) and c_D, so they cannot depend on ν_x,
  on p_raw beyond A, or on β* beyond s₀^r.
- Under this ∃-constants ∀-arrays reading, the per-n form follows: a law at a single n can be embedded in an (RD) array
  whose other rows are arbitrary admissible laws.
- B0 removes σ*², so "σ*² fixed" in (RD) is no obstruction.
Two gaps in the text:
- No sentence states the law-uniform reading explicitly.
- DIST-3 introduces n₀ without quantifying it ("There are c, C such that for every n ≥ n₀"). Its constants must
  depend on C_T, which is not in the §0 dependence list.
ASSEMBLY's (H3) silently adds C_T and n₀₃. The application uses C_T = 2, so this is harmless.
*Repair.*
- Add to STATEMENT §0, after line 64: "Constants and n₀ depend on the listed quantities only, not otherwise on the law
  of the data; each display holds, at each n ≥ n₀, for every law satisfying (RD) at that n."
- In DIST-3 write "There are c, C, n₀, depending on (s₀^r, A, σ*², M, B, C_T, κ₀), such that …".
- Record this reading as an obligation on the proof legs of DIST-1, DIST-2, DIST-3 and X′.

**E-02 — MINOR — STATEMENT §1R Remark (4) (line 241) vs ASSEMBLY §2 and §5.**
*Issue.* Remark (4) says "C₁ = C′/C²". With the sentence without (A4), ASSEMBLY needs a larger constant:
C₁ := max{C′_⋆/C_⋆², 1 + s + (sA + s + 5)/log 2}, so that {|S| > s + C₁M log n} ⊆ {|S| > m_n(t₂)}. I checked this
inclusion: m_n(t₂) ≤ 2s + 1 + (sA + s + 2 + 3M) log n/log 2 ≤ s + C₁^{(2)}M log n. It uses log n ≥ 1 for n ≥ 3 and
(sA + s + 2) + 3M ≤ (sA + s + 5)M for M ≥ 1.
The extra requirement is legitimate: a larger C₁ only weakens Theorem A (ii). So the reader statement, which uses one
C₁ for both clauses, is proved as worded. The Remark is simply inexact.
*Repair.* Remark (4): "C₁ ≥ C′/C² (and C₁ ≥ 1 + s + (sA + s + 5)/log 2 for the sentence without (A4))". Alternatively,
give the sentence without (A4) its own constant.

**E-03 — MINOR — STATEMENT §1R Remark (1) (lines 238–239); ASSEMBLY §1 Remark "general radii".**
*Issue.* Remark (1) claims the general-radius form for every ε_n with M₀ log n/n ≤ ε_n² ≤ n^{−1/2} without saying
which window (A3) and (A4) must hold on. When nε_n² > M log n for the M whose window was assumed, (ND) is needed at
m_n(nε_n²/C²), which can exceed q_n. ASSEMBLY's remark gets this right: the window is replaced by
min{p, ⌈C_q nε_n²⌉}, using B2 (d) with M := nε_n²/log n.
I checked the other two requirements of the general form; both hold for n ≥ n₀ with the same n₀:
- 3e^{−2cnε²} ≤ ½e^{−cnε²}, because nε² ≥ log n gives e^{cnε²} ≥ n^c ≥ 6;
- the remainder is ≤ ½e^{−cnε²}, because nε² ≤ √n.
*Repair.* Remark (1): "… provided (A3), (A4) hold with the window min{p, ⌈C_q nε_n²⌉}." This is not a target clause.

**E-04 — MINOR — ASSEMBLY §1 (n₀ through n_B); `B2.md` (e); STATEMENT changelog v1.3 row "Theorem A, Corollary C:
range M ≤ √n/log n" ("κ₀ = ½ gives a realistic n₀").**
*Issue.* This is a matter of fact, not an error.
- n_B is the least n from which (C_q√n + 1)(1 + A log n) ≤ c₂n/K⁴ holds. With c₂ = 10⁻⁵ it is astronomically large:
  ≈ 1.7·10¹⁵ for (s, A, K) = (0, 1, 1), ≈ 5.7·10¹⁵ for (1, 1, 1), ≈ 1.4·10¹⁷ for (3, 2, 1), ≈ 1.9·10¹⁸ for (1, 1, 2).
  These are bisection values for the explicit inequality.
- The cause is that the window must cover every M up to √n/log n.
- Even for q′ = 1, B2-core needs n ≥ 10⁵K⁴.
The theorem is still correct with this n₀, and nothing in the reader text claims a small n₀. But the changelog's
"realistic n₀" is not supported by the bridges.
*Repair.* Drop "realistic" from that changelog reason, or state that n₀ is not explicit and is large. If HQ wants a
moderate n₀, make n₀ depend on an upper bound for M; do not change the statements.

**E-05 — NIT — `B1.md` Remark (DIST-2 needs less), lines 22–24.**
"J₀ := supp β* ∪ {j₁, j₂} with j₁ ≠ j₂ outside supp β* (or any two indices when |supp β*| ≤ 1)" cannot be met when
p = |supp β*| ≥ 2: then no index lies outside the support. The conclusion still holds, since the Remark only needs
|J₀| ≥ 2 and supp β* ⊆ J₀.
*Repair.* "J₀ ⊇ supp β* with |J₀| ≥ 2." The reader's sentence without (A4) assumes (A3) for every single predictor
anyway, so it does not use this Remark.

**E-06 — NIT — ASSEMBLY §2 (ii′), proof line 120.**
"s₀ = |supp β*| ≤ s ≤ K (n ≥ 2s)" is false when s > p, which (A2) allows because s is only an upper bound. What is true
and needed is s₀ ≤ min(s, p) ≤ min(p, ⌊n/2⌋) = K for n ≥ 2s.
*Repair.* Replace with that.

**E-07 — NIT — STATEMENT §1R Example (lines 189–190); ASSEMBLY §4 (E1), (E2).**
- "Gaussian predictors satisfy (A3) with K = 1" holds for **jointly** Gaussian x, which is what (E1) proves.
  Marginally Gaussian predictors need not satisfy (A3) on sparse directions with K = 1.
- "Independent predictors … with the constant K of a single predictor" needs one K valid for every predictor, as
  (E2) assumes.
*Repair.* Write "jointly Gaussian predictors", and "independent predictors satisfy it with K = the largest
single-predictor constant".

**E-08 — NIT — STATEMENT §3 B2 (lines 356–360), assessed against `B2.md`'s STATEMENT-CHANGE REQUEST.**
*The request is justified.* "q_n ≥ m_n(M log n) + s", read as an assertion, is false for small p. Example: p = 2,
s = 1, n ≥ 4, so K = 2; then m_n ≥ s₀ + 1 forces m_n = 2 and m_n + s = 3 > q_n. Comparison attempt B-c §4 item 6 finds
the same.
The requested wording, "⌈C_qM log n⌉ ≥ m_n(M log n) + s for all n ≥ 2, M ≥ 1, hence min{p, m_n(t) + s₀} ≤ q_n for
t ≤ M log n", is what (ND) needs, because (ND) ranges over j ≤ min(m, p − s₀).
- It is editorial and does not weaken any clause.
- I re-derived B2 (d): the bracket (2sA + 4s + 5)M − (sA + s + 2) ≥ sA + 3s + 3 ≥ 3s + 3, and log(n + 1) ≤ 2 log n for
  n ≥ 2.
Also, STATEMENT's chain "(n − 1)λ_min(Σ̂^z_T)/max_j(…) ≥ (n − 1)c_ψ/(4n)" mixes the n⁻¹ and (n − 1)⁻¹ normalisations of
the sample covariance. It is valid as a lower bound, because the (n − 1)⁻¹ version dominates, but B2 (a)'s direct form
λ_min(G_T) ≥ c_ψ/4 is cleaner. Recording it, while keeping g₀ = c_ψ/8, is fine.

**Observation (no finding) — faithfulness of Theorem B.** The reader text of Theorem B (lines 194–200) carries no
conditional label. ASSEMBLY proves it **conditional** on W3-POST:Thm-1@1.0.0 and on DIST-3 (H3). This matches the §1R
preamble (lines 120–123) and ASSEMBLY §3's status line. Whoever cites Theorem B must carry that label.

## Verdicts and checks per file

### B0 — VERIFIED
- **(a): verified.** It is R′(a′) applied to the non-constant ỹ with (a, c) = (α*, σ*); ỹ is non-constant because
  Cỹ = Cy^r/σ*. R′(a′) is the response-scale posterior of [POST2] Claim D, the same object as STATEMENT §0, on the
  same retained columns.
- **(b): verified.** ȳ^r = α* + σ*ỹ̄, and ŝ_j, x̄ depend on x only.
- **(c): verified.** The affine change of variables leaves the Hellinger affinity unchanged pointwise in x, and
  Tonelli applies over ν_x. Both densities share the x-marginal ν_x, and the sample x̄, ŝ are fixed by the data.
- **(d): verified.** It follows from the image-measure identity, with T_{σ*} keeping S, so the event identity covers
  "d_H > r or |S| > k" and δ_n.
- **(e): verified.** It is exactly (RD) with intercept 0, coefficients β*/σ* and unit noise, at each n.
- **(f): verified.** μ, θ* and L_{S₀} are linear or quadratic in β*, so they scale as 1/σ* and 1/σ*², while
  (ND), (TR₀), m_n, 𝒟_n and (A2)–(A4), (A6)(a) depend on x and supp β* only.
- **Remarks: verified.** Remark 2's identification of the reader's posterior and f holds, since
  â + xᵀb = ȳ + (x − x̄)ᵀb. Remark 3 (constant y^r has probability 0) holds.
- **Pathwise reduction with the plug-in intercept: verified.** This is the P1-05 issue.

### B1 — VERIFIED (c₁ = 1/576 and 4p·e^{−c₁n/K⁴} confirmed)
- **Lemma B1.0: verified.**
  - (ii): E Y^{2k} ≤ 4k·½(2κ²)^kΓ(k) = 2·k!(2κ²)^k.
  - (iii): the cosh argument gives EY² ≤ κ², hence K ≥ 1.
- **Lemma B1.1: verified.**
  - Upper: Σ_{k≥2} ≤ 2(2λK²)²/(1 − 2λK²) ≤ 16λ²K⁴ for 2λK² ≤ ½.
  - Lower: E e^{−μZ²} ≤ 1 − μ + 8μ²K⁴, with EZ⁴ ≤ 16K⁴.
- **Tail exponents: verified.**
  - μ = 1/(64K⁴): −μ/4 + 8μ²K⁴ = −1/(512K⁴).
  - λ = 1/(96K⁴) ≤ 1/(4K²): −λ/3 + 16λ²K⁴ = −1/(576K⁴).
  - Mean: 2e^{−n/(8K²)} ≤ 2e^{−n/(8K⁴)}.
  - On the good event, n(W − Z̄²) ∈ [n/2, 4n/3] ⊆ [(n − 1)/2, 2(n − 1)] for n ≥ 3.
  - Total ≤ 4e^{−n/(576K⁴)}; the union over p gives 4p·e^{−c₁n/K⁴}.
- **(b): verified.**
- **(c): verified.**
  - ‖μ‖ ≤ Σ|β*_j|ŝ_j√(n − 1) ≤ √2·√(n − 1)·s·b̄σ*.
  - ‖θ*‖² ≤ 2sb̄²σ*².
  - L_{S₀} ≤ (‖μ‖² + ‖θ*‖²)/n, from the variational identity, which I re-derived: minimiser nH_S⁻¹Xᵀa, minimum
    aᵀ(I − M_S)a.

### B2-core — VERIFIED (c₂ = 10⁻⁵ confirmed)
- **Intercept: verified.** It is handled by w = (1, z_T), with Γ^w_T = diag(1, Γ_T) because E z = 0. Range Γ contains
  e₁, so r ≥ 1.
- **Degenerate directions: verified.** Whitening on range Γ and the a.s. event 𝓝_T give vᵀŴv = v_RᵀŴv_R. The reduction
  to unit ξ ∈ R is exact.
- **One direction: verified.**
  - EX⁴ ≤ 8a⁴ + 128K⁴σ⁴ ≤ 128K⁴.
  - EX^{2k}/k! ≤ (3/2)(8K²)^k.
  - Lower Chernoff: μ = δ/(128K⁴) gives exponent −δ²/(256K⁴) = −1/6400 at δ = 1/5.
  - Upper Chernoff: λ = 1/(384K⁴) ≤ 1/(16K²) gives −1/(768K⁴).
- **Net: verified.**
  - |𝒩_T| ≤ 21^r.
  - ‖B|_R‖^{1/2} ≤ √2/0.9.
  - (√0.8 − 0.1√2/0.9)² = 0.5436 ≥ ½.
- **Union: verified.**
  - log count ≤ L + (1 + q′)log 21 ≤ (1 + 2 log 21)L, using 1 ≤ q′ ≤ L.
  - (log 2 + 2 + 2 log 21)·10⁻⁵ = 8.78·10⁻⁵ ≤ 1/6400.
- **q > p: verified.** It is covered by q′ = min(q, p), with C(p, p) = 1.
- **"In particular" and Corollary B2c: verified.** They follow with a = −uᵀz̄, and (a + uᵀm, D_σu) has the same
  support.
- **Comparison with B-a-1, B-b-1, B-c-1: no step disagrees.**
  - All three prove the same statement, with c₂ = 1/98304, 1/409600 and 1/87552 respectively.
  - All three handle degeneracy by whitening on range Γ, as here.
  - B-c-1's A2 shows that sparse-direction (A3) cannot be replaced by single-coordinate (A3) plus (A4). This supports
    the reader's window form of (A3).

### B2 — VERIFIED (change request justified; editorial, does not weaken)
- **(a): verified.** G_T = nΛ_TΣ̂^z_TΛ_T, and on 𝓔₂(q) ∩ 𝓔₁ λ_min(G_T) ≥ (c_ψ/2)·min_j(Var/ŝ_j²) ≥ c_ψ/4.
- **(b): verified.**
  - D_T = Πφ(λ_l), with φ increasing.
  - Cauchy interlacing (μ_l ≥ λ_l, l ≤ k) gives D_{S′}/D_S ≥ φ(λ_min(G_{S′})) ≥ c_D(n + 1).
  - Iteration over any anchor S works, because every intermediate set has size ≤ q.
- **(c): verified.** For j ≤ min(m, p − s₀), s₀ + j ≤ min(m + s₀, p) ≤ q.
- **(d): verified for every n ≥ 2, M ≥ 1, 2 ≤ p ≤ n^A and s₀ ≤ s.** See E-08 for the inequality; m_n is monotone in t.
- **(e): verified.** q_n log(ep/q_n) ≤ (C_q√n + 1)(1 + A log n), and n_B is finite.

### B3 — VERIFIED (against W3-POST Theorem 1 item 6)
- **Step 0: verified.**
  - C_q log 3 = 3.17(sA + 2s + 4) ≥ 2sA + 3s + 2.
  - m♯_n ≤ m_n(log n), from the quoted [T03R] E2(ii) bound with ω = ½ log n, s₀ = s ≥ 1, log C(p, s) ≤ s log(2p),
    ((s + 1)/2 + ½) log n ≤ ((s + 2)/2) log(n + 1).
  - Then B2 (d) with M = 1.
- **(F_λ): verified.** s + j₀ ≤ (2A + 2)s + 2 ≤ (2A + 3)s + 2 ≤ q_n, and λ_min(G_T/(n − 1)) ≥ ψ/4. ψ ≤ 1 because |T| = 1
  is allowed.
- **(F_w): verified** with g₀ = c_ψ/8.
- **BM-∞: verified.** θ*_j² ≥ b_n²/2 in the unit-noise model, giving the envelope M_n = b_n²nψ/(8 log n) → ∞, which is
  deterministic.
- **(TR₀; 2): verified** by B2c.
- **Item 6 conditions: verified.**
  - The events 𝒜′_n are (X, θ*)-measurable: finitely many continuous inequalities, with p_ret read off X.
  - The constants (M_E, φ₀ = √ψ/2 ≤ ½, g₀) are common.
  - |supp θ*| = s₀ = s ≥ 1 on 𝒜_n.
  - R1 holds: p ≤ n^A, s ≤ K for n ≥ 2s, σ*² = 1 after B0, G with ε independent of (X, θ*).
- **(vii): verified.** P(𝒜_nᶜ) ≤ 5n^A e^{−c₂n/K⁴} → 0, using c₂ ≤ c₁.

### ASSEMBLY — VERIFIED-WITH-AMENDMENTS (E-01 to E-04, E-06, E-07; none changes a reader statement)
**Theorem A (i), (ii) — verified.**
- *Renaming.* t = M log n/C_⋆² gives C_⋆√(t/n) = √(M log n/n) and s₀ + C′_⋆t/log n = s₀ + C₁M ≤ s + C₁M.
- *Exponent.* e^{−c_⋆t} = n^{−2c_AM} ≤ n^{−cM}, so the reader's bad event lies inside the master's.
- *Range.* t ∈ [M₀_⋆ log n, √n] = [·, n^{1−κ₀}] at κ₀ = ½, because M₀ ≥ C_⋆²M₀_⋆, C_⋆ ≥ 1 and M ≤ √n/log n.
- *Remainder.* It is contained in (𝓔₁ ∩ 𝓔₂(q_n))ᶜ, by B1 (b), (c) and B2 (d), (e). Its probability is
  ≤ 5n^A e^{−c₂n/K⁴}.
- *Collecting the bounds.*
  - 3n^{−2cM} ≤ ½n^{−cM} for n ≥ 6^{1/c}.
  - 5n^A e^{−c₂n/K⁴} ≤ ½e^{−c√n} ≤ ½n^{−cM}, by n_R and M log n ≤ √n.
- *One n₀ for all M₀ ≤ M ≤ √n/log n: verified.* No requirement on n involves M.
- *Dependence: verified.* Only on (s, A, K, c_ψ, b̄), given (R-a), (R-b) and (R-c).
- *(R-b) and (R-c): verified.* Taking the worst constant over s₀^r ≤ s, and the monotonicity in (c, C, C′, M₀, n₀) and
  in the interface constants, are both correct.
- *"On the same data sets": verified.* Both displays come from the single event 𝔈_n.

**Sentence without (A4) — verified**, given (H1.2) and (H-X′), and with E-02 and E-06.
- (i′): the radius C_⋆⋆√(t₂ℓ_n/n) = √(M log n·log(p ∨ n)/n), and the remainder is ≤ P(𝓔₁ᶜ).
- (ii′): the cutoff bound (E-02), then Fubini over the design on 𝓔₁ with H-X′, which is a fixed-design statement.
  This gives 2n^{−2cM} + 5n^A e^{−c₂n/K⁴} ≤ n^{−cM}.
- The reader sentence does not claim "same data sets" for this variant; none is proved, and none is needed.

**Theorem B — verified as a conditional result** (on DIST-3 and W3-POST:Thm-1@1.0.0).
- δ_n is invariant under B0, and δ_n = O_P(r_n) by items 6 and 1.
- With u fixed so that C₃e^{−c₃u} ≤ min{η/2, ϵ}, for large n (M_n ≥ C₃√u, u ≤ √n):
  {Π > η} ⊆ 𝒜_nᶜ ∪ (𝒜_n ∩ N_{n,u}) ∪ {δ_n > η/2}.
- Its limsup is ≤ ϵ.
- (R-a) is needed here too, for constants fixed along the array (E-01).

**Example — verified.**
- (E1) and (E2): see E-07 for the wording.
- (E3): padding T into a block of size q_n ≤ p works.
- (E4): f(ω) = (1 − ρ²)/(1 − 2ρ cos ω + ρ²) has Fourier coefficients ρ^{|h|}. For any finite T ⊂ ℤ, contiguous or not,
  uᵀΓ_Tu = (2π)⁻¹∫f|Σ_{j∈T}u_je^{−ijω}|² ≥ min f·‖u‖². Orthogonality of distinct integer frequencies is all that is
  used, and min f = (1 − |ρ|)/(1 + |ρ|).
- (E5): eigenvalues 1 − ρ and 1 + (|T| − 1)ρ.

**Faithfulness — verified.** ASSEMBLY proves Theorem A (i), (ii), its sentence without (A4), the Example and
Theorem B exactly as worded in §1R. Theorem B carries the conditional status of the §1R preamble.

## What I could not check
- The master displays (1.1), (1.2), DIST-3 and Lemma X′, and W3-POST Theorem 1, are given hypotheses. Whether their
  proofs deliver the law-uniform per-n constants of (R-a) is open until those proofs are checked (E-01).
- The quoted bound on m♯_n ([T03R] E2(ii), as quoted in W3-POST lines 38–39) was taken as quoted. I did not open
  `ARC/W1-T03R/PROOF.md`.
- I did not execute `bridges_checks.py` (read-only rule; it writes into the ticket folder). Every quantity it checks
  was recomputed by hand above.

**Overall verdict: VERIFIED-WITH-AMENDMENTS.** B0, B1, B2-core, B2 and B3 are VERIFIED, and ASSEMBLY is
VERIFIED-WITH-AMENDMENTS. All of it is conditional on the given master displays and on W3-POST Theorem 1. The
amendments (E-01 to E-08) are wording changes, mostly in STATEMENT's remarks and quantifier conventions. None changes a
reader statement, a target clause or a proof step.
