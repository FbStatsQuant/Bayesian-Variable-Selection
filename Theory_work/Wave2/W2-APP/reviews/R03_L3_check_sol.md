**Theorem LOC: VERIFIED-WITH-AMENDMENTS.**

**LOC-B: GAP for target STATEMENT claim (C); VERIFIED-WITH-AMENDMENTS for the narrower theorem actually stated in L3.8B.** The gap is the omitted enlarged-Q hypothesis in the target, not a demonstrated counterexample to consistency. No FATAL defect was found in the window-innovation argument.

1. **MAJOR — Target LOC-B omits a hypothesis required by its proof.** Location: `Theory_work/Wave2/W2-APP/STATEMENT.md:68–70`, versus `lemmas/L3_LOC.md:167` and `181–184`.

   The target assumes only s₀(g_n−1) ≤ (1−δ₀)log n, then claims NA via GROW L2.3(a). After enlargement, however, the chi-square rank in that argument is |Q∖S₀| = p−s₀, not |Q⁰∖S₀|. The lemma correctly adds p−s₀ ≤ (1−δ₀)log n in this branch; the target does not.

   This is a real difference between the hypotheses. Take s₀=1, g_n=⌊0.9 log n⌋, two deterministic equicorrelated groups of size g_n with correlation 1/2, one truth in the first group, and p=2g_n. The target's assumptions hold with δ₀=0.1, λ_min=1/2 and automatic PTV. Here |Q⁰|=g_n, so p<2|Q⁰|+33 forces Q=[p], while |Q∖S₀|∼1.8 log n. GROW L2.3(a)'s size hypothesis fails for every fixed positive slack. This example establishes failure of the advertised implication to G4-χ; it does not establish failure of NA itself.

   **Concrete repair:** add the enlarged-case bound to claim (C), and to any family-map statement invoking this version of LOC-B. Equivalently, require |Q∖S₀| ≤ (1−δ₀)log n after the enlargement rule. Keeping the broader target requires a new NA proof exploiting group structure; the present conditional invocation of L2.3(a) does not supply it. With the lemma's actual added hypothesis, its conditional NA proof is valid.

2. **MINOR — Explicitly remove raw means before using centered Gaussian innovations.** Location: `lemmas/L3_LOC.md:13`, `101–102`, `117–130`; also the transfer at `80–84`.

   The setting permits iid N(m,Σ_n) raw rows. As defined, e_A=W_l−W_Aβ_A has mean m_l−m_Aβ_A, and D_{T,l}=W_Tβ_T−W_{T′}β_{T′} generally has a nonzero mean. Thus “iid N(0,τ_A²)” and “iid N(0,v_{T,l})” are false literally. In particular, the uncentered assertion ‖D_{T,l}‖²/v_{T,l}∼χ²_n is false. For an AR(1) singleton T={v} outside the window, T′=∅ and D=ρ^{|l−v|}W_v; if m_v=3, then ‖D‖²/v_{T,l}=‖W_v‖² has a noncentral χ² distribution and its ratio to n tends to 10, contradicting the asserted 4n bound with probability tending to one. Such pairs can occur in the stated deterministic lattice.

   The residual identity, variance formula and theorem survive; centering removes these means exactly.

   **Concrete repair:** before all delta arguments, write “Replace the raw matrix by W−1mᵀ and henceforth call this W. This leaves CW, X, Y, the partition and every scored model unchanged, so assume m=0.” All subsequent Gaussian regression and norm assertions then hold as written. Alternatively, use affine regression innovations and bound ‖CD_{T,l}‖, whose squared norm divided by v_{T,l} is χ²_{n−1}, rather than ‖D_{T,l}‖. No bound on m is needed.

3. **MINOR — The AR(1) radius-one remark is false for the window defined here.** Location: `lemmas/L3_LOC.md:145–146`; compare `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md:395–411`.

   L6 uses the nearest members of T on either side of l, which may be arbitrarily far from l. It does not use T∩{d(·,l)≤1}. For example, with ρ=1/2, l=2 and T={4}, a radius-one window gives T′=∅ and reference g=CW₂, while the true residual removes its population correlation ρ² with W₄. The limiting conditional variance of the difference of the two normalized noise statistics is

   2[1−√(1−ρ⁴)] > 0.

   Thus the present window construction with r_n=1 does not even give a pointwise o_P(1) comparison in this example. The growing-window proof at lines 103–142 is unaffected.

   **Concrete repair:** replace the remark by “For AR(1), L6 uses at most two nearest conditioned neighbours, selected by their positions in T, giving at most p(|Q|+1)² reference innovations; their distances need not be one.”

4. **MINOR — Correct the measurability label in the posterior input.** Location: `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:13` and `53–54`; used by `lemmas/L3_LOC.md:158–159`.

   β=D_x⁻¹θ* is measurable in the raw design, but generally not in the standardized X: column standardization discards the raw scales D_x. This does not invalidate the transfer, because μ=Xθ* is X-measurable and ε is independent of both the raw and standardized designs. The proof already conditions on the raw design where it introduces β.

   **Concrete repair:** change the parenthetical to “raw-design-measurable”; state that conditional on X the standardized model is directly Y=Xθ*+Cε. Keep the uniform posterior argument indexed by standardized designs x and their fixed standardized coefficients. No assumption about recovery of D_x from X is needed.

I read L6 in full, including its spherical-tail conditioning, global ladder, NA argument and assembly, and checked all the requested C-GROW inputs, L1_POST, L2_CT, both statements and the paper's GROW premises. The following are affirmative checks, not additional findings.

- **L3.6's exact identity and variance formula pass.** After the zero-mean reduction, CW_l−Ce_{T′}=CW_{T′}β_{T′} lies in span(X_T), and t_l>0, so the normalized residual direction is exactly h/‖h‖. For F=T∖T′, residualizing W_F on W_{T′} gives covariance M, and the incremental fitted value is cᵀM⁻¹V. Consequently Var(D)=cᵀM⁻¹c. CD(b) gives M≽cI, and CD(a), together with at most two indices at each distance, gives

  Var(D) ≤ [2K₂²/{c(1−e^(−2t₂))}]e^(−2t₂r_n) = O((log n)⁻²).

  There is no missing factor |T| in this summation.

- **The NA unions and sigma-fields pass, with the mean amendment above.** Fix a deterministic witness π_n for the deterministic covariance sequence. Then Q, B_l, 𝔓 and 𝒲 are deterministic. Their cardinalities are respectively bounded by p2^{|Q|}=n^{O(1)} and p2^{2r_n+1}=p·polylog(n). For E1, condition on the entire raw W: g is fixed and ε remains Gaussian. For E2, use the marginal isotropic law of Ce_A, or condition only on W_A; the chi-square norm law is not conditional on the entire W. For E3(i), condition separately on each W_T, under which e_T is independent Gaussian and P_T is fixed. E3(ii) is an unconditional chi-square bound for each deterministic pair. Finally, conditional on X, the P_Q noise bound is valid. These events can be intersected by a union bound; their independence is unnecessary. The phrase “conditionally in law” at line 114 should explicitly name W_A or be changed to “in distribution.”

- **The uniform comparison and threshold pass.** Lines 135–139 give the deterministic bound on the stated high-probability intersection

  max_{T,l}|Z_{T,l}−Z′_{l,T′}| = O((log n)^(−1/2)+(log n)/√n) = o(1).

  This uses one common ‖P_Qε‖=O_P(√log n), not a separate noise bound for exponentially many T. Multiplying this error by max|Z′|=O_P(√log n) costs only O_P(1)+o(1) in the squared maximum. Hence max Z² ≤ 2log p+O(log log n)+O(1) on suitable events of probability tending to one. GROW L2.2's exact c_n is 2log p+log n−2log(|Q|+1)−4κ_E−2+o(1); its excess tends to infinity. The strict NA conclusion follows with the same κ_E and lattice score event. No stronger r_n is required. An empty pair family is simply a vacuous NA case.

- **The delta outside NA passes.** CT's conjugation/Schur bound is uniform on inherited integer positions; CD follows by applying CT to Θ_{VV} without compressing positions. Thus P4's uniform conditional-covariance bound really is replaced for every conditioning set, including selected ones. Bijectivity supplies both linear neighbourhood growth and the summable distance count. The chosen d_n gives e^(−t₂d_n)=O(n^(−1/2)); R_n gives K₂e^(−t₂R_n)≤n^(−2). Therefore L6.3's recursive partial-correlation argument and polylogarithmic reference family carry over. The only use of separation (6.0) outside those covariance controls is the fixed positive truth-visibility margin; PTV supplies it, and sample scaling changes the fixed coefficients by O(ħ_n). No sign assumption or exact AR(1) constant is needed.

- **The spherical-tail and ladder transfers pass.** In L6.4, D=U₀∪S₀ contains every true column, so conditional on W_D and ε the standardized-scale response is fixed. The regression innovation is independent of W_D, and its projected direction is spherical before restriction to A_cov. The W_D-measurable CN_D domination handles that restriction correctly. CD gives ‖α‖=O(e^(−t₂d_n)), τ²∈[c,1], and bounded b_j, so ‖m‖=O(1) and the same tail/count estimates follow. Those counts support the whole dyadic size ladder for every maximizer, including models near K. With k₀=|Q|+16s₀, the ladder gives k≤2k₀; the Q rule then permits truth additions when Q≠[p], since K≥2|Q|+32s₀+1 eventually. When Q=[p], p=O(log n) and K=p eventually. P5's exact-Gram identities are never imported, and P2's nearest-neighbour regression is used only in the NA step that L3.6 replaces.

- **LOC-B needs no global upper spectral bound.** Entrywise Gaussian concentration uses unit marginal variances; the logarithmic-size Gram perturbation is O((log n)^(3/2)/√n), and its lower floor uses only λ_min≥c. Every bounded-size covariance matrix has its own uniform upper bound from its bounded trace. The remaining regression bounds use inverse floors, unit marginal variances and fixed s₀. Group independence makes the far covariances and α exactly zero. Conditional on each X in the regularity event, GROW L2.3(a)'s reference statistics are standard normals and its common projected-noise term has rank |Q∖S₀|. Its two tail failures are at most 2/log n; the eventual threshold comparison and the L0 score-event failures are uniform over those X. Integration is legitimate. Finding 1 is precisely the missing rank control in the broader target.

- **TL and assembly pass under the named premises.** Gram floors give every missing-truth residual signal at least (n−1)(c/2)θ_lo², against O(log n) noise/prior terms, uniformly over the lattice family. NA and TL then imply exactly |S̃₀∖S₀| deletion moves from every maximizing centre. The shipped cap ℓ_n+|S̃₀| suffices for the completed scan at S₀. “Some maximizer” is enough, because the sandwich covers every maximizer and the descent handles every lattice centre; a prescribed tie representative or a unique maximizer is unnecessary. The source supports this: `Scripts/SMC_BVS/core/cpp/v3_core.cpp:473–476` adds m.S.size() to the LS0 cap and emits the centre, while W1-N3 L6(a) proves the enumerated return remains a smallest-size maximizer under its exact-arithmetic/encoding conditions. Retain the complete implementation premises from STATEMENT §1, including GUARD-W/OP-LS0 and the applicable IND-T/extra-search conditions. The posterior transfer plus boundedness gives E[1−π(S₀)]→0, and integrating M5(0) yields the stated joint-output conclusions without any delivery assertion.

Independent numerical algebra checks on a non-AR(1) banded covariance gave residual-identity error 5.6×10⁻¹⁶ and variance-formula error 1.4×10⁻¹⁷, with nonzero incremental variance 0.0514606856801783. They support the algebra only; the verification above is analytic. The scratch check also illustrates the noncentral-mean and radius-one defects. Script: [check_loc.py](C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-APP/reviews/R03_scratch/check_loc.py).

Saved verbatim to [R03_L3_check_sol.md](C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-APP/reviews/R03_L3_check_sol.md).
