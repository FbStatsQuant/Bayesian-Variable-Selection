# R01 — C-MIS statement-lock review

Reviewer: Codex gpt-6.1-sol, adversarial statement review. Reviewed STATEMENT v1 and PLAN. Read-only review; only this output file was written. No git commands were used.

Evidence abbreviations: ST = Theory_work/Wave1C/C-MIS/STATEMENT.md; PLAN = its PLAN.md; TH = Theory_work/State_of_Project/sections/04_theory.tex; METHOD = the sibling 02_method.tex; T03R = Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/A-REV5/sources/W1-T03R/PROOF.md; P3 = Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex; P1 = Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex; GEN = Theory_work/Wave1/W1-GEN/STATEMENT.md; L5 = its lemmas/L5_assembly.md. PDF page numbers below are physical pages of the supplied Song–Liang attachment.

The core GR result is worth pursuing, and the fixed-design extension looks viable with its explicit tail hypothesis. This draft is not lockable verbatim: it overstates Song–Liang, leaves a conditional-noise assumption unstated, promises automatic Gaussian hypotheses too broadly, and understates changes to the fixed-design proof. These are repairable without changing the principal research direction.

## 1. Target and best approximating support

**Right research target, but inaccurate description of its precedent.** Song–Liang Theorem 4 is consistency of posterior densities around the KL minimizer f₀, almost surely. Corollary 2 gives posterior inclusion of the projection support, π(s̃ ⊆ ξ | data) → 1 in probability. Neither displayed result asserts π(ξ = s̃ | data) → 1. See the supplied PDF, physical page 11 / printed page 957, Theorem 4, equation (18), and Corollary 2. ST:12–15 says that the posterior concentrates on s̃, incorrectly strengthening the cited result. C-MIS's exact-support claim is a stronger, method-specific conclusion under stronger assumptions; describe it that way. Its no-beta-min inclusion claim is the closest counterpart to Corollary 2. Do not claim a density-contraction analog unless one is actually proved.

The support definitions are appropriate with qualifications:

* Under GR, β^C = β_C + γ is the coefficient in the conditional Gaussian candidate regression. Under iid Gaussian rows with an intercept, it equals Σ_CC⁻¹ cov(x_C,y), so its support agrees with SL's s̃. This is a population projection, not the generally dense finite-sample projection of the realized full mean. ST:50–52,71–73 gets this distinction right.
* Under EP, the projected mean P_C μ_full is the fixed-design least-squares/KL mean target. Its sparse coefficient support is an appropriate distinguished model. It is not a universally defined population s̃. Moreover, KL alone does not select a unique model: supersets representing the same projected mean have the same optimal likelihood/KL value. Distinguish the projected mean from its sparse support and from posterior preference for the smaller model. With collinearity the projected mean is unique but its coefficient representation need not be; the anchored eigenvalue and tail assumptions do substantive identification work.
* The actual method must be rerun with p = p_C, its corresponding size weights and cap, not obtained by conditioning the full-p posterior on S ⊆ C. ST:31–35 correctly specifies this, matching METHOD:84–106. Keep that explicit.

Thus this is a Gaussian-residual, sparse-support analog with polynomial candidate dimension, not a general replacement for SL's fixed-dimensional KL theorem. Full-model fixed sparsity alone does not imply fixed candidate projection sparsity: one omitted signal can have a growing number of Gaussian graph neighbors.

## 2. MIS(i): reduction and hidden assumptions

**For a fixed candidate design, the reduction is valid.** Conditional on that fixed design, GR and independent Gaussian ε imply ε + ξ ~ N(0,σ_C² I). T03R:162–203 uses the resulting Gaussian contrast experiment, deterministic design, sparse mean, energy/eigenvalue conditions, and shipped score. It does not require the selected coefficient support to have been the support in some larger generating system. P3:55–85 explicitly performs the contrast reduction. No additional causal or full-design assumption is needed.

Standardization is also correct: θ^C = D_x β^C uses candidate sample SDs only. Response standardization is already handled by P3:67–80 through b = b₀ s_y² and exponent ν = 0.01 + n/2; it must not be replaced by a newly chosen raw-data likelihood/prior. The possibly design-dependent intercept α+a disappears under Uᵀ. Neither standardizing omitted columns nor adding an intercept column to the selection space is required.

**The random-design setting is missing a necessary assumption.** ST:37 states only the marginal law ε ~ N(0,σ² I). ST:48 adds conditional independence of ξ and ε, but this does not imply ε | X_C^r ~ N(0,σ² I). Consequently ST:52 and MIS(ii) do not follow as written. Require ε independent of X_C^r, or directly require its conditional Gaussian law, together with conditional independence from ξ. MIS(iii) does explicitly assume independence and is safe on this point.

A concrete failure of the current random-design wording: take ε Gaussian, raw candidate column x₁ = −ε, β₁ = 1, a second independent Gaussian column with zero coefficient, and ω = ξ = 0. Then y^r = 0. GR holds with τ = 0; the candidate Gram, energy, nonempty fixed support and beta-min conditions hold on high-probability design sets. Yet the method encounters a constant response rather than the asserted Gaussian candidate experiment. The draft explicitly permits ω = 0 (ST:38–39). This is not cured by ξ ⟂ ε conditionally.

**Empty support needs an explicit decision.** TH:775 requires fixed s₀ ≥ 1; ST:56 omits the inequality. Exact cancellation and cov(x_C,y)=0 can yield s₀^C = 0, so this is material. Either restrict MIS/F/GEN transfers to s₀^C ≥ 1 and state the excluded null case, or prove the null-support extension separately, with conventions for the empty Gram and coefficient minimum. P3:194,350,380 and P1:334,338 already contain useful null-case machinery, but the TH09 card is not itself a citation for that extension. GEN also explicitly requires s₀ ≥ 1 (GEN:30,49).

The BM scale in MIS is correct: it is σ_C², not the original σ². Using σ² alone could certify a proxy whose signal is inadequate relative to omitted Gaussian noise. The PIP/HPM inequalities and convergence of the expectation follow from bounded posterior miss mass; no expectation rate follows from O_P(r_n), and none should be added. See P3:362–364.

## 3. MIS(ii)/(iii), Gaussian prevalence, and Proposition P

MIS(ii) is viable after the conditional-noise repair. Specify that every deterministic sequence x_n in the admissible sets obeys H-MIS with the same constants and deterministic beta-min envelope. An asymptotic condition such as BM-∞ is a condition on sequences, not on an individual x at one n. The intended diagonal argument for tightness works: failure of uniform tightness supplies a subsequence of designs and diverging thresholds with conditional tail probabilities bounded away from zero; completing that subsequence contradicts the fixed-design O_P result. L5:57–64 supplies the analogous argument for convergence to zero. One cannot merely integrate pointwise convergence at fixed designs.

The Gaussian conditioning formulas in ST:72–74 are correct, including the sign and multiplication order. The missing intercept formula can be recorded as a = m_Oᵀβ_O − m_Cᵀγ. From the block identity Σ_CC Θ_CO + Σ_CO Θ_OO = 0,

γ = −Θ_CO Θ_OO⁻¹β_O,

and the conditional residual variance is β_OᵀΘ_OO⁻¹β_O. For exactly one omitted column k with β_k ≠ 0, γ_j = −Θ_jk β_k/Θ_kk, so supp γ is precisely its candidate neighbors. The nonzero β_k qualification is necessary: otherwise γ is zero even when the graph has edges. With several omitted columns, weighted precision contributions can cancel; there is no unqualified union-of-neighbors identity.

ST:76 needs qualified language. Marginal correlation alone is not sufficient to establish a proxy; for one active omitted variable, a candidate that is null in the full model has a nonzero induced coefficient exactly when the relevant partial correlation is nonzero. Nonzero partial correlation does not guarantee selection without beta-min, nor prevent cancellation at a true candidate. Marginal correlation can certainly identify a proxy in special cases, including a single candidate, where marginal and partial correlation coincide. Replace the categorical sentence with the coefficient criterion. PLAN N2 must also specify that the candidate being tested is null in the full model; a non-neighbor that has its own true coefficient is still selected.

**The automatic GD(a) claim is too broad** (ST:77–78; PLAN:13–14). Fixed candidate dimension and Σ_CC ≻ 0 supply asymptotic sample-Gram control; they do not by themselves supply nonempty support, bounded signal energy, beta-min, or fixed σ_C². For a fixed covariance, fixed coefficients, finite fixed residual variance and nonzero projection support, the intended result is straightforward. If triangular arrays are allowed, even one candidate with coefficient n⁻¹ violates beta-min, and coefficients growing with n can violate energy. Dense projection support breaks fixed sparsity when p_C grows. State the parameter and support assumptions, then prove the design conditions. Growing-dimensional prevalence should remain conditional unless a specifically bounded covariance/signal class is given; a singular-value union bound alone cannot prove these coefficient hypotheses.

## 4. Corollaries H and D

**H is distribution-free at the algebraic level.** For any feasible distinguished T, if π_C(T)>1/2 and T is scored, it is the strict global posterior maximizer, hence the scored-set maximum. A wrong reported maximum on the output event therefore requires π_C(T)≤1/2 or failure to score T. Markov gives the displayed 2E[1−π_C(T)] term. This needs neither Gaussian noise nor a model-truth interpretation for T. TH:477–480 explicitly corrects the pointwise δ₁ versus its expectation; TH:484,489 records the composition clause. The same reasoning allows a measurable design-dependent T.

Retain qualifications: positive/defined exact scores, a defined posterior, feasible distinguished model, reported maximum over the all-scored set with the prescribed rule, and the potential-run/output-event coupling used by M5. Literally “any law of y” includes a point mass on constant y, for which sample-standardized scores are undefined (00_COMMON.md:9; P3:85). State “any law supported on valid inputs,” or supply explicit failure-event conventions. The H inequality does not by itself prove discovery or delivery.

**D transfers under GR**, using the effective Gaussian candidate experiment. Substitute σ_C² everywhere in GEN: in v_T, leakage exponents, NL bounds, visibility, and beta-min; recompute μ and the actual candidate-only partition. There is no variance mismatch when τ² is a fixed constant: GEN permits any fixed positive σ². Its Δ_T is the residual energy of μ^C, not the omitted component; adding τ² again there would double-count it. GEN's H0 uses BM-∞, so MIS with merely BM(c) is insufficient for D. The draft's explicit invocation of GEN H0 correctly retains that stronger condition.

For random candidates, invoke C4 with the raw candidate design and measurable candidate coefficients/certificates, a canonical conditional law for ε′, and all GEN envelope conditions, not just MIS(ii)'s eigenvalue conditions. See GEN:115–120 and L5:68–82. Independence of ε′ from X_C follows from its identical conditional Gaussian law after the missing ε assumption is repaired. The liminf identity follows from P(output and correct)=1−P(U_n)−o(1); it is not a delivery theorem. An explicit proxy instance remains a proof obligation.

## 5. Theorem F, changed proof steps, tail, and frontier

**EP is an appropriate fixed-design notion.** It makes the omitted residual orthogonal to every candidate subspace, not merely to the distinguished sparse span. This stronger orthogonality is precisely what makes a uniform comparison across S ⊆ C possible. Use one coordinate convention throughout: ST:98 calls y_c a contrast vector while μ_full = CX^rβ is an n-vector. Either apply Uᵀ to μ_full, r, and X_C, or work entirely in the centered n-dimensional subspace. Norms and identities are preserved.

The proposed identity is exact for the ridge quadratic, not just for least-squares RSS. Put z=μ^C+e, y_c=z+r, and Q̃_S=zᵀ(I−M_S)z. Since M_S r=0 and rᵀμ^C=0,

Q_S^c = Q̃_S + ‖r‖² + 2rᵀe, for every S ⊆ C.

But b=b₀‖y_c‖²/N is also changed relative to the hypothetical z-only data. If comparing full denominators, then

2b+Q_S^c = 2b̃+Q̃_S + (1+2b₀/N)(‖r‖²+2rᵀe).

The score-ratio identity remains valid using the actual common b. This is why direct raw-data likelihood substitution would be unsafe.

**The “unchanged” list in ST:111 is not correct verbatim.** The underlying (G1)–(G4) noise events can stay unchanged at variance σ². However, add G5, for example |rᵀe| ≤ σ‖r‖√(2 log n), with exceptional probability at most 2/n. Completing the square gives

‖r‖²+2rᵀe ≥ −2σ² log n.

Thus the proposed extra subtraction in ongood(b) is legitimate if the baseline is Nσ²(1−δ_n). It is not a lower bound around Nσ²_C,n with only that subtraction: the cross-term can have order √(n log n). For the conservative original-noise baseline, replace δ_n by δ_n+2 log n/N. This still has δ_n log n→0.

That modification propagates into C4's υ_n, C5's ε_n and q_n, their onsets and bounds, and then C8's cited inputs. T03R:180 explicitly uses ongood(b) as the denominator; T03R:183–197 then uses the resulting constants. The combinatorial/expectation argument survives, and the numerator still involves σ²χ²_J because projection differences annihilate r, but C4–C5 cannot be called unchanged without recording the revised sequences. Alternatively derive a stronger effective-variance lower bound with its own revised sequences.

For underfitting, E_n^C in ST:109 is the right upper-bound quantity. G5, G1 and the energy bound yield E_n^C ≤ Nσ²_C,n(1+o(1)), with an explicit error envelope; σ² ≤ σ²_C,n ≤ σ²+2M eventually. Consequently the fixed BM(c) proof appears to retain the same c₀: signal gain is measured against σ²_C,n, while noise in G4 remains σ² ≤ σ²_C,n. P3:295–311 must be rewritten to show this. Define the underfit signal Δ_S using μ^C, not μ_full: otherwise its norm includes ‖r‖², which addition of missing candidate variables cannot recover. In particular P3:311's identity using P_{S′}μ=μ is false for μ_full; its replacement works because (P_{S′}−P_S)r=0. Check the reduction lemma as well as the named comparison lemmas.

The large-signal conclusion inherited by F must explicitly use J_n(c) with σ²_C,n, retain the other hypotheses including TAIL when dropping beta-min, and avoid referring to the undefined fixed GR variance σ_C². Deterministic PIP/HPM consequences then transfer directly. I found no further use of the true density f₀ in the truncated T03 comparison/assembly proof once Step 0 is replaced: f₀ is essential in P1's tail proof, not those algebraic comparisons. The σ² upper bound in G4 remains available; the underfit denominator upper bound is the part that must change.

**Bounded-p tail claim is correct.** Eventually K=p_C. For bounded p_C, finitely many possible (p_C,s₀^C) give a positive lower bound on any nonempty R_m; its threshold n^{−(s₀^C+2)/2} tends to zero. Hence m_n^sharp=K eventually and the tail is identically zero. See T03R:15–17,44–47. This requires a defined cutoff and feasible distinguished model, including whichever null-case convention is adopted.

**Frontier claims need narrowing.**

1. Rank(X_C)=N implies r=0 for the unrestricted candidate span, but p_C≥n alone does not imply full row rank. More importantly, the shipped family is capped at K≈n/2. A mean in the full span can still lack any feasible exact representation. Thus “no fixed-design misspecification exists” in ST:114 is false for the capped model class. Say “no residual outside the unrestricted candidate span”; dense representability and sparse/capped representability are different questions. PLAN:21's “rank-N vacuity of EP” is also inaccurate: EP can hold with r=0 and an exactly sparse projected mean.
2. The numerator identity E_true[m_b^c(S)/f_true]=1 remains true under misspecification for every fixed rate b and positive true density (P1:317–321). The well-specified denominator lower bound fails; do not call this failure of the identity or of all change-of-measure arguments.
3. The claimed exp(−c·rank) loss is not a universal statement without conditions on Δ_n and the reference experiment. If d=rank(X_C) and v=σ²+Δ_n, the candidate-span Gaussian KL discrepancy is d[log(v/σ²)+σ²/v−1]/2. Its coefficient vanishes as Δ_n→0. For the full contrast experiment, KL(N(μ^C+r,σ²I_N), N(μ^C,vI_N)) equals N log(1+Δ_n/σ²)/2, which can be order n even at bounded candidate rank. Specify which density/comparison is used and prove the claimed loss, or label it only an obstruction to the particular P1 denominator strategy. P1:337–357 shows precisely where the pure-noise residual was used. None of this proves failure of posterior consistency under EP.
4. Non-GR random-design misspecification is outside the proposed theorem, correctly. Describe SL's fixed-dimensional result as KL-density consistency plus support inclusion, retaining its moment/prior/identifiability assumptions. Do not imply it proves exact support recovery for arbitrary heteroscedastic errors.

## 6. Six-hour viability

The core MIS reduction, repaired random-design transfer, qualified Gaussian formula/prevalence result, and H/D composition are viable. A careful conditional-tail EP theorem is plausible within the budget if prioritized early. The complete PLAN is overcommitted: growing-p Gaussian prevalence, all changed EP steps, a new explicit GEN instance, six numerical scenarios, a precise frontier KL argument, and the serial review/council rounds in PLAN:35–37 leave little repair time.

Freeze GD(b) as a hypothesis now. Prioritize MIS and H/D, then the bounded-p EP theorem and the general EP theorem conditional on TAIL. Use a few targeted exact-posterior checks; simulations cannot establish asymptotic O_P rates or failure of selection at a merely sufficient beta-min threshold. In particular PLAN N3's “below the σ_C² threshold” is not a theorem of failure: c₀ is a conservative sufficient constant. Drop exploratory N5 and the optional GEN instance before shortening the EP audit. The bounded-p fallback still needs proof and correct variance constants; “classical argument” is not sufficient evidence for this specific response-standardized shipped score.

## Required changes before lock

1. Correct the SL attribution: density consistency and support inclusion, not exact-model concentration; describe MIS as stronger under stronger hypotheses and EP as a separate fixed-design target.
2. Add ε | X_C^r ~ N(0,σ²I), conditional independence from ξ, and valid-input/measurability conventions. Explicitly restrict to s₀^C≥1 or supply a separately proved null-support extension; respect GEN's nonempty-support scope.
3. State MIS(ii) in deterministic-sequence/envelope form. Qualify GD(a) with covariance, coefficient, nonempty-support, energy and variance assumptions; do not infer projection sparsity or beta-min from Gaussianity.
4. Qualify Proposition P by one active omitted variable, null-candidate status for proxy claims, cancellation, and beta-min. Replace the categorical marginal/partial-correlation slogan with the coefficient criterion.
5. Correct F's coordinates, effective-variance large-signal conclusion, underfit signal definition, and changed-step inventory. Record the revised denominator error sequences and their propagation through C4/C5/C8; track the response-dependent IG rate. Prove the revised inequalities before promoting F.
6. Correct the frontier: unrestricted span versus capped feasibility; surviving fixed-rate numerator identity versus failed denominator bound; explicit KL experiment and Δ-dependent loss rather than an unqualified exp(−c·rank) assertion.
7. Narrow the six-hour deliverables as above, preserving proof/review time. Treat optional growing-dimensional prevalence, GEN instance, numerical probes and unproved frontier claims as optional or conditional, not prerequisites disguised as completed corollaries.

Verdict: LOCK-WITH-CHANGES (required changes 1–7).
