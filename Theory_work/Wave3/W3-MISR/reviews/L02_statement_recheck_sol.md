# L02 — independent statement-lock re-check (Sol)

Scope: `Theory_work/Wave3/W3-MISR/STATEMENT.md` v1.1, reconciled against L01 findings 1–4 and the diff from commit `197f557`. Only the brief and its permitted inputs were consulted; no other review, LOG, PLAN or CHECKPOINT files were read. This is a statement-lock assessment conditional on the declared inputs in §8, not a certification of new MIS-R proofs. No code or numerical experiment was executed.

## L01 reconciliation

### 1. Remark P / Theorem F: RESOLVED

Evidence in v1.1: `Theory_work/Wave3/W3-MISR/STATEMENT.md:179-187`. In particular, lines 182–185 explicitly replace the energy and BM-∞ conditions, rule out the old unnormalised alternative, and retain the effective-variance BM(c) and inclusion thresholds. Lines 185–187 retain TAIL on the invariant posterior, identify (TL) as a ratio, and scale the EP coefficient and residual.

Here is the complete scale audit against `Theory_work/Wave1C/C-MIS/STATEMENT.md:124-146`. Put t = σ_n > 0, and use a tilde for objects computed after y^r ↦ y^r/t. The standardised candidate design is unchanged. In contrast coordinates,

    ỹ_c = y_c/t,  μ̃_c = μ_c/t,  ẽ = e/t ~ N_N(0,I),
    θ̃^𝒞 = θ^𝒞/t,  r̃ = r/t,
    Δ̃_n = Δ_n/t²,  σ̃²_{𝒞,n} = σ²_{𝒞,n}/t² = 1 + Δ_n/t².

The dimensional definition Δ_n = ‖r‖²/N is retained in response units; it must not be treated as an invariant numerical value.

| Source hypothesis or conclusion | Check under this map |
|---|---|
| Deterministic full/candidate design, full mean, contrast coordinates, G (MIS1:124-125) | The design and U remain fixed, the full mean divides by t, and Gaussian noise has variance one. Determinism and independence are preserved. |
| EP, its orthogonality and projected mean (MIS1:126-129) | Both sides of the decomposition divide by t; X_{c,𝒞}ᵀr̃ = 0. Support and sparse-representation uniqueness are unchanged. Scaling θ^𝒞 and r is explicit at MISR:187. |
| Δ_n and effective-variance interval (MIS1:129) | From the new full-mean energy condition, Δ_n/t² ≤ Mn/N ≤ 2M, hence 1 ≤ σ²_{𝒞,n}/t² ≤ 1+2M, explicitly MISR:183. In physical units the interval is [t²,(1+2M)t²], replacing the old [σ²,σ²+2M]. There is no surviving absolute 2M bound. |
| Fixed positive s₀^𝒞, polynomial p_𝒞, feasibility, cutoff m_n and C (MIS1:130-132) | These depend on design, support, n and prior, so are invariant, including the eventual feasibility and deterministic cutoff requirements. |
| R^𝒞, including energy of the **full** mean and the floor on S₀^𝒞 (MIS1:130) | MISR:182-183 uses ‖μ_c‖² ≤ Mn t², giving unit-noise energy M. The correlation floor is invariant. It has not inadvertently been replaced by a bound only on the projected mean. |
| SE_λ(j₀), SE_w(m_n;g₀) (MIS1:131) | Design-only, including their anchor and ranges, and invariant. |
| BM-∞ and BM(c) (MIS1:132-133) | The former is now θ^𝒞²_min nφ₀²/(t² log n) → ∞; the latter uses σ²_{𝒞,n}. Both are exactly the unit-noise conditions. Since σ²_{𝒞,n}/t² is uniformly bounded above and below, either denominator gives the same divergent BM-∞ requirement. The old unnormalised alternative is explicitly unavailable at MISR:184. |
| TAIL^𝒞(m_n) (MIS1:133) | Same cutoff and exact posterior under the transformed response; therefore the random tail mass and its O_P(r_n) assertion are invariant. This is explicit at MISR:185-186. |
| Main concentration, deterministic PIP bound, MPM and HPM conclusions (MIS1:134-136) | These involve only the invariant model posterior and the unchanged support. The expectation in the HPM inequality is likewise preserved. No new expectation rate for F is asserted. |
| No-beta-min inclusion (MIS1:136-137) | θ_j² ≥ c σ²_{𝒞,n} log n/(nφ₀²) is unchanged after dividing both squared quantities by t²; the resulting J_n and posterior inclusion mass are unchanged. Explicitly covered at MISR:185. |
| Corollary F(a) (MIS1:138) | Bounded p_𝒞, eventual m♯_n = K and the identically zero tail are unchanged. All other F hypotheses remain required. |
| Corollary F(b), rank d_n, κ, TL, m^T_n and final cutoff (MIS1:139-141) | Rank and cutoffs are unchanged. TL becomes 1/[Δ_n/t² + (1-d_n/N)], exactly the original ratio σ²_n/[Δ_n + σ²_n(1-d_n/N)]. Its eventual onset, κ and cutoff constants are unchanged. The SE_w requirement at the chosen final cutoff is still inherited; TL does not remove it. |

The changed-steps list (MIS1:142-146) also remains valid in the normalised experiment, rather than being reused with dimensional objects held fixed. Specifically:

- G5, |rᵀe| ≤ σ_n‖r‖√(2 log n), divides on both sides by t². The χ² events and δ_n^𝒞 = δ_n + 2 log n/N are dimensionless; the propagated υ_n, ε_n and q_n are read at unit variance and energy M.
- The actual response-dependent IG rate is b = b₀‖y_c‖²/N, so b̃ = b/t². Every Q^c_S, t_S and E_n^𝒞 divides by t²; D_S and the projections/smoothers do not change. Thus E_n^𝒞 ≤ Nσ²_{𝒞,n}(1+δ''^𝒞_n) is an equivalent inequality, with δ'' evaluated using unit-noise energy M. For example, the source formula `(M+σ²)/(Nσ²)` in `lemmas/L4_theoremF.md:53` becomes `(M+1)/N` after the energy constant is normalised, and does not introduce a bound on t.
- The S-versus-S′ and signal-gain ratios V_S/σ²_{𝒞,n} and Δ_S/σ²_{𝒞,n} are invariant. The signal loss uses μ^𝒞/t, not the full mean μ_c/t. The replacement (P_{S′}−P_S)r = 0 is preserved. Assembly and Step 0 → TAIL involve unchanged posterior masses.

These checks agree with the source distinction between true-noise lower bounds and effective-variance upper bounds (`Theory_work/Wave1C/C-MIS/lemmas/L4_theoremF.md:131-135`). The normalisation does not identify those two variances.

The same audit for the other clauses of Remark P gives:

- **MIS (i)** (`MIS1:54-72`): normalise by √σ²_{𝒞,n}. The GR sum ε+ξ becomes unit Gaussian noise after removal of its intercept; β^𝒞, θ^𝒞 and μ^𝒞 divide by that scale. The support, size/cap, polynomial regime, correlation and eigenvalue floors, prior and cutoff are unchanged. The new energy bound is exactly the unit-noise bound. Both BM alternatives and J_n^𝒞(c) already use σ²_𝒞 (`MIS1:62,68`), as MISR:180-181 explicitly notes. Concentration, PIPs, selection, inclusion, proxy/cancellation and wrong-model consequences depend only on the unchanged support/posterior; a positive scaling also preserves cancellations and nonzero coordinates.
- **MIS (ii)** (`MIS1:73-77`): for design-measurable σ²_𝒞(x)>0, normalise conditionally at each x. The standardised residual has the common unit Gaussian conditional law, so the source independence/conditioning argument is applied to that residual. Measurable envelopes, fixed size, common floors, c or the deterministic divergent BM envelope, and P(𝒜_n)→1 retain their original roles. In particular the divergent envelope is still required uniformly on the good sets, not merely pointwise. MISR:179-180 explicitly allows the design-dependent variance; §4:116-132 states the corresponding conditional interface. No fixed upper/lower bound on σ²_𝒞(x) is needed.
- **MIS (ii′)** (`MIS1:78`): the same conditional map with beta-min dropped preserves J_n^𝒞(c) and its inclusion mass. Other envelope requirements are retained; no whole-support recovery is inferred from the no-beta-min clause.

For **Remark SNR's entire list** (`MISR:173-178`), normalise by σ*_n. W3P Theorem 1 items 1–4 concern only posterior probabilities/support; item 5's strict-superset and size-tail claims are invariant and its strong-coordinate threshold is relative already; item 6 is transported conditionally with common constants/envelopes as in the source. The design/prior hypotheses, s, A, feasibility, F₀, F_λ, F_w and OS are invariant. POST2 A1 changes only a design hypothesis. For B, scale the arbitrary mean and reference coefficient by 1/σ*_n; every term of B_T(ϑ) divides by σ*²_n, whereas T, D_T, R^T_m and Θ″ stay unchanged. The replacement B_T(ϑ)≤Bσ*²_n is explicit at MISR:176. C's expectation and E's concentration/inclusion conclusions concern the same posterior, with BM/ID/ID^M already relative. D uses the parameter-posterior map in R′(a′): squared mean thresholds multiply by σ*²_n, coefficient thresholds by σ*_n, and relative variance and Hellinger distances are invariant; MISR:177-178 supplies the dimensional thresholds. All constants are evaluated at unit variance. No further variance-dependent hypothesis or conclusion in this list was left unnormalised.

### 2. Code / floating-point claim: RESOLVED

Evidence: `Theory_work/Wave3/W3-MISR/STATEMENT.md:78-83`. The unrestricted floating-point assertion is gone; the binary64 loss-of-distinction example is valid. The retained code-path references agree with `Scripts/SMC_BVS/core/v3_preprocess.R:123-127`, `v3_fit.R:97,118` and `cpp/v3_score.h:14,55-60,217-223`.

The numerical observation accurately describes the supplied record:

- `numerics/N0_out.txt:15-40`: three exact-branch data sets (11, 12, 13), seven transformed fits each, including c<0 and |c|=10⁻¹⁵⁰,10¹⁵⁰. All 21 comparisons retain status and HPM; the largest displayed PIP difference is 1.304·10⁻¹⁰.
- `numerics/N0_out.txt:42-48`: one SMC data set, four transformed fits with the same seed, all retaining status and HPM; maximum displayed PIP difference 1.037·10⁻¹¹. The seeds and transform loops are explicit at `N0_code_invariance.R:46-50,56-61`.
- Thus the 25 **transformed comparisons** in the statement have maximum |ΔPIP|≤1.4·10⁻¹⁰. Four baseline fits and the separate preprocessing checks are additional operations, not additional transformed comparisons. The text's count is correct in its stated context; it does not purport to count every function invocation in the script.

This is an observation on the listed inputs, with no inference of general floating-point invariance.

### 3. Corollary H reference law / KL interpretation: RESOLVED

Evidence: `Theory_work/Wave3/W3-MISR/STATEMENT.md:159-169`. Each sentence now has a valid interpretation:

- The constructed vector μ(κ)+√v ε̃ has coordinate law N(μ_i(κ),v) and is the unit-noise comparison vector transported to response units (up to the irrelevant intercept).
- Under MIS1 GR, given x, write m_x=(α+a)1+xβ^𝒞 and ε′~N_n(0,vI). Subtracting n⁻¹Σ_l(m_x)_l from y_i gives (Cxβ^𝒞)_i+ε′_i. Its conditional law is exactly N(μ_i(κ),v). This is centring the conditional mean, not centring the noise.
- In contrast, Cy^r=μ(κ)+Cε′ has conditional covariance vC and coordinate variance v(1−1/n). The variance clause is in the paragraph's stated conditional-on-candidate-design experiment; an unconditional random-design variance would additionally include variation in μ_i(κ).
- In Corollary G, integrating out omitted covariates gives y_i|x_{𝒞,i}~N(α′+x_{𝒞,i}ᵀβ^𝒞,σ²_𝒞), where α′=α+m_𝓜ᵀβ_𝓜−m_𝒞ᵀγ. This follows from the Gaussian conditioning calculation in `Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md:38-45`. The true candidate-conditional density belongs to the candidate linear-Gaussian class, hence minimises conditional KL (and the candidate-design-averaged KL). The SL identification is qualified by centred rows and the intercept convention; the reference itself removes the sample mean of that conditional mean.
- Lines 166–169 explicitly exclude a fixed-realised-full-design KL projection interpretation and distinguish the in-sample, in-probability result from an integrated or almost-sure contraction result. These restrictions are consistent with `L1_reduction.md:69-74`. The quantitative contraction inequalities require none of the optional KL interpretation.

### 4. OS onset and constants: RESOLVED

Evidence: `Theory_work/Wave3/W3-MISR/STATEMENT.md:45-48`. Membership in the per-n class requires the two actual OS inequalities at that n. The sufficient bridge is explicitly separate and requires n≥n_OS. Its constants depend only on (s,A,g₀), or (s,A,c_D) for the DG/ADG route, with c_D=g₀/(1+g₀) on the F_w route. This is precisely `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md:14-27`: the geometric-sum bound and amplified tail bound both need the onset. No dependence on response variance or energy is introduced.

## Other changed lines and remaining-problem check

- **Version/status lines (MISR:1-6):** accurately describe targets and the amendment provenance; they do not newly claim proofs.
- **Contrasts and conventions (MISR:23-28):** deterministic U, zero mass outside Ω, zero-padding and a measurable mode selection make the intended random-configuration statements well-defined. For fixed n the countable union over p has the indicated Borel structure; support indicators, finite score sums, eigenvalue inequalities and the configuration classes are measurable. No problematic new measurable-selection claim is needed, since each model space is finite.
- **Corollary G(b) (MISR:143-145):** explicit p_𝒞≥2 and σ²_𝒞>0 are correct. The existing normalised population energy and beta-min conditions permit the Gaussian-design argument with β^𝒞/σ_𝒞. In particular the source failure bound 2n⁻²+2k_n n⁻²+n⁻¹, k_n=O(log n), in `L2_gaussian.md:91-105` is O(1/n), sufficient for Eδ_n=O(r_n) after conditioning. Allowing bounded p as well as growing p causes no failure of that argument.
- **Remark U (MISR:188-190):** taking the maxima of the two applicable n₀,C pairs is sufficient even if the representations use different classes or constants. Under their common response law, two distinct supports would have expected posterior masses summing to at least 2(1−Cr_n)>1, impossible. No uniqueness of the coefficient vector is inferred.

I see no remaining FATAL or MAJOR problem anywhere in STATEMENT.md v1.1. I also found no remaining MINOR or NIT item requiring a change. The lock remains conditional on the explicitly declared theorem inputs; the new MIS-R proofs are still outstanding as the statement itself says.

New or remaining findings: **0 FATAL / 0 MAJOR / 0 MINOR / 0 NIT**.

VERDICT: LOCK
