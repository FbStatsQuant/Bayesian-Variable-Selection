LOCK

Independent statement re-lock review of STATEMENT.md v2, W3-SCR (Sol, high). No subagents; no git commands; no production or statement edits. I read the statement, R01 and its disposition, CODE_CHECK, PROGRAM item 5, PROTOCOL, and the requested production source ranges. I consulted L1-L6 to disambiguate the intended claims and checked the critical statement implications independently; this is not a line-by-line proof approval. No blocker or major issue found. No numerical simulation was needed: the checks below are algebraic, including uniform bounds over the relevant models. The current scr_lib.py prior normalizer was inspected directly; I did not rerun N0 or certify its reported numerical error.

1. **NOTE — SCR-A° has the necessary uniform residual and cross-term correction.**

   **Location:** STATEMENT §1 (residual scale, ϑ° and MC°), SCR-A°, (A°∞).

   **What is wrong:** No defect found. In particular, replacing total response scale by residual scale without a correction would be invalid, but the displayed correction supplies the terms needed here.

   **Independent evidence:** Write d=n−1, E_S=μ'R_Sμ, h=τ̂, and q_S(v)=v'v−n v'X_SH_S^{-1}X_S'v. Directly from the score,

       q_S(y_c)=||y_c||²/(n+1) + n y_c'R_S y_c/(n+1).

   Since R_S²≼R_S and R_S preserves centering, μ'R_SCε is Gaussian with variance at most σ²E_S. A one-sided union bound over at most N_q models gives μ'R_SCε≤σ√E_S r_n simultaneously, with failure at most e^{-x} (in fact at most e^{-x}/2 with the displayed r_n). Combine this with the central noise norm bound and h≤τ̄, whose joint failure is at most 2e^{-x}. Then, uniformly in |S|≤q,

       y_c'R_S y_c
       ≤ E_S + 2σ√E_S r_n + σ²d(1+2a_x+2a_x²)
       ≤ d σ_S²[1+2a_x+2a_x²+r_n/√d].

   The last step uses 2σ√E_S≤σ_S²√d, so the unexplained-mean/noise cross term is included with the correct coefficient. Also

       0.02h² + ||y_c||²/(n+1)
       = [0.02+d/(n+1)]h² ≤ 1.02τ̄².

   Thus neither the 0.02 nor the response-energy part of Q_S is silently discarded. It follows that

       ((n+1)/n)[0.02h²+q_S(y_c)]
       ≤ d σ_S²(1+ϑ°),

   using σ_S²≥σ² for the final term of ϑ°. The exact addition identity has likelihood increment ν[−log(1−u)], where u=[n/(n+1)]g_{y_c}/[0.02h²+q_S(y_c)]. Its prior/determinant cost is at most [2log(2p−1)+log(n+1)]/2. Consequently g_{y_c}>σ_S²T_n(1+ϑ°) is sufficient for improvement. On the witness-noise event, √g_{y_c}≥√γ−σr_n≥σ_S(√Ψ−r_n); MC° gives precisely that strict improvement. The three event costs are e^{-x}+2e^{-x}+e^{-x}, proving the advertised 4e^{-x} exclusion of every offending LO model. No independence between these events is assumed.

   For (A°∞), choose x_n=√log n. The entropy estimate in finding 2 gives r_n/√d→0 from q_n log p=o(n). Further,

       τ̄²/(nσ²)=O(1/n)+O(||μ||²/(n²σ²))=o(1).

   Hence every term of ϑ° vanishes under the two stated side conditions, including when σ varies with n. The strict liminf gap then implies MC°. This addresses uniformity, the cross term, and the scale correction without an unstated bounded-total-signal hypothesis.

   **Proposed fix:** None.

2. **NOTE — R01 finding 4 is fixed by the deterministic witness, including q=0 and growing s₀.**

   **Location:** STATEMENT §1 r_n, SCR-A/(A∞); intended witness specified in L2.

   **What is wrong:** No defect found. There is no need for an additional log s₀ term.

   **Evidence:** Before observing ε, choose the smallest maximizer of γ(t|S) over missing true t for each offending S. The same t maximizes γ/σ_S² because σ_S is independent of t. Each witness statistic x_t'R_SCε/√a has variance ≤σ². There are at most N_q such statistics, so 2N_q exp(−r_n²/2)=e^{-x}. Adaptation of a coded search to y causes no problem: this bound already holds over all candidate S.

   For q≥1, N_q≤(p+1)^q, and q log(p+1)≤q log p+1 since q≤p. For q=0, N_q=1 exactly. Thus r_n≤√(2q log p)+√(2log 2+2+2x), valid also at q=0. With x_n=√log n the second term is o(√log n); it is absorbed by the strict liminf gap in both asymptotic theorems. I also rederived SCR-A's addition bound from the exact score; T_n has the correct factors n and n+1.

   **Proposed fix:** None. Keep the witness deterministic in the final proof.

3. **NOTE — B2° and A1° are sufficient and mutually consistent.**

   **Location:** Lemma B, B2°; Corollary A1°.

   **What is wrong:** No false bridge or incompatible hypotheses found. The constant 16 and the support-size condition supply a strict asymptotic margin, rather than merely equality at a critical threshold.

   **Independent evidence:** A direct ridge-energy argument provides a check independent of the augmented-space derivation. Fix an offending S, T=S₀\S, V=||θ*_T||₂², h_T=||θ*_T||₁, and E=μ'R_Sμ. The ridge variational bound gives E≥κ(n−1)V. The identity

       Σ_{t∈T}θ*_t x_t'R_Sμ
       = E − Σ_{j∈S∩S₀}θ*_j x_j'R_Sμ

   and ||X_S'R_Sμ||²≤λ₀E give a lower bound E−c_θ√E. Under √(κ(n−1))θ_min≥2c_θ this is at least E/2. Since a(t|S)<n,

       max_t γ(t|S)/σ_S²
       ≥ E²/[4n h_T²(σ²+E/(n−1))].

   This expression increases with E. Substitute E≥κ(n−1)V, h_T²≤|T|V, and V≥|T|θ_min². This yields the stronger lower bound

       ((n−1)²/n) κ²θ_min²/[4σ²+4κs₀θ_min²],

   so the statement's denominator 4σ²+9κs₀θ_min² is safely conservative. The argument works for any positive lower bound κ≤φ^a, not just the exact value of the floor; alternatively the displayed B2° bound is increasing in its positive floor argument.

   In A1°, the coefficient-norm condition is exactly √(κ(n−1))θ_min≥2c_θ. Using the stated, weaker denominator and (n−1)²≥n²/4, its beta-min and support conditions imply

       Ψ_n(q_n) ≥ (n/8)min{κ²θ_min²/(4σ²), κ/(9s₀)} ≥ 8𝐋_n.

   The squared asymptotic threshold is at most 4𝐋_n, giving ratio at least √2. All remaining side conditions of (A°∞) are explicitly present. Consistency example: centered orthogonal p=n−1 columns, q_n=1, s₀=1, κ=1, σ=1, and θ_min=16√(𝐋_n/n). All the hypotheses hold eventually, including s₀𝐋_n≤n/576, the coefficient-norm condition, and ||μ||=o(n). Thus the conditions are not vacuous.

   **Proposed fix:** None. The heading “no bound on the total signal” should be understood as no fixed O(1) coefficient/total-variance bound; the displayed ||μ||=o(nσ) is still a real growth restriction.

4. **NOTE — R01 finding 1 is fixed in A1, including the q_n=0, huge-p edge.**

   **Location:** Corollary A1 and its explicit c₁.

   **What is wrong:** No remaining dimensionality gap found.

   **Evidence:** Now log p is charged even at q_n=0. Put τ_*²=M²+σ². Eventually the anchored bridge gives Γ_n(q_n)≥κ²b²n/16, whereas

       [τ_n√(2log p+log n)+σ√(2q_n log p)]²
       ≤4τ_*²[(q_n+1)log p+log n]≤4τ_*²c₁n.

   The squared ratio is therefore at least 200/64>1. This verifies the constant and the liminf gap, rather than just excluding the old example. R01's log p≈n² duplicate-column construction violates the revised growth assumption. For polynomial p and q_n=o(n/log n), the assumption holds eventually. No start/discovery hypothesis is introduced, so A1 still supplies PROGRAM item 5 in its intended regime.

   **Proposed fix:** None.

5. **NOTE — R01 finding 2 is fixed by bounded s₀; the floor suffices uniformly over excess-set sizes.**

   **Location:** SCR-C; size-aware interface to L5.1/L5.2.

   **What is wrong:** No fixed-s₀ counterexample found. The earlier growing-s₀ construction is explicitly excluded, and merely holding m fixed is not needed for the replacement argument.

   **Evidence:** For a strict superset with k=s₀+m≤q_n, put ℓ=log(p/m) and φ=φ_n(q_n). If any such superset exists, ε≤φ≤1. The exact deletion penalty contains 2log((2p−k)/k), as it must. Since s₀ is uniformly bounded, k≤(s₀+1)m, so its lower bound is 2ℓ−O(1), uniformly for every m≥1. The determinant penalty supplies log n−O(1). Sparse captured-noise and ridge-bias corrections are uniformly negligible under q_n log p=o(n) and ||θ*||₂=O(σ√n). Summing deletion gains and bounding the joint excess-direction projection by its dimension-m Gaussian tail gives a necessary inequality of leading form

       φ(1−o(1))(2ℓ+log n−O(1))
       ≤ 2ℓ+2ε₁log n+O(√(2log p+log n))+O(1),

   with ε₁>0 arbitrarily small fixed and a failure probability tending to zero. This follows from a union bound over binom(p−s₀,m) excess sets with per-set cost exp(−x'm), so there is no unaccounted factor q_n in the excess-direction bound.

   Crucially the margin is uniform:

       φ(2ℓ+log n)−2ℓ
       ≥φ(2log p+log n)−2log p
       ≥ε(2log p+log n).

   Choose ε₁<ε/4; the lower-order terms cannot close that gap. This excludes m=1, m=2, and m growing with q_n simultaneously. For m=1 or 2 the log k loss is bounded; for growing m it is compensated by the smaller excess-set entropy log(p/m). This is the correction absent in the growing-s₀ counterexample, where k/m need not be bounded. The O(σ√n) hypothesis controls the ridge-bias term after division by σ, also for varying σ.

   **Proposed fix:** None. Preserve s₀=O(1) in the stated asymptotic floor result. The general-size EC assertion remains a separate, size-aware statement.

6. **NOTE — R01 finding 3 and both SCR-N consequences are repaired.**

   **Location:** SCR-N and its consequences; intended explicit sequences in L6.

   **What is wrong:** No domain error or unjustified coded-output sharpness claim remains.

   **Evidence:** At ∅, a=n²/(n+1), determinant ratio D=n, Q_∅=n−1. Exact score comparison gives

       F({j})≤F(∅) iff g_{y_c}(j|∅)≤τ̂²B_n.

   The displayed B_n is positive and real for every allowed n,p. It uses the actual constants n−0.98 and n+0.02. Gaussian union bounds for truths/nontruths cost at most 2e^{-x}. The noncentral response scale has τ̂²≥τ_n²(1−4a_x), except on an event of probability 2e^{-x}; when 0≤4a_x≤1 this implies τ̂≥τ_n(1−4a_x). Together these prove the claimed 1−4e^{-x} lower bound. The equality edge 4a_x=1 makes the premise impossible because σ>0 and the truth set is nonempty, but creates no undefined expression. B_n/L_n→1 under log p=o(n).

   For consequence 1, take p≈n^A, s₀=1, truth orthogonal to all other columns, and choose θ₁ so √γ(1|∅)/[τ_n√(2log p+log n)]=1−δ. This is solvable eventually with θ₁≈√(log n/n). With x=√log n the true-noise allowance is negligible and the nontruth allowance has strict slack √(2A)<√(2A+1). SCR-N makes ∅ LO with probability tending to one for each fixed δ>0. Other columns may be duplicates, so realization at p≫n is no obstruction. This defeats any smaller leading constant in the uniform-LO assertion at q=0, exactly the qualified claim now made.

   For consequence 2, take p=s₀=2, correlation 1−1/n, and θ=(log n,−log n). Then Δ_n(0)∼2(log n)², τ_n→σ, while both γ's are asymptotic to (log n)²/n. With x=√log n the premises hold eventually and ∅ is LO with probability tending to one. The statement correctly does not turn mere existence of a bad LO model into a claim about the actual reported HPM.

   **Proposed fix:** None.

7. **NOTE — R01 findings 5 and 6 are fixed; the code/certificate interface remains faithful.**

   **Location:** STATEMENT §0, §1 floor conventions, §3 “Changes vs the card”; production sources named in the brief.

   **What is wrong:** No substantive defect found.

   **Evidence:** 𝒞 is now explicitly empty on failed statuses, the HPM singleton on exact status, and certified archive endpoints on completed status. The C++ scan freezes the center, evaluates every deletion/feasible addition/swap, and certifies only after no strict improvement; a capped improving exit stays uncertified. The R assembler requires identity of HPM and a certified endpoint before setting the top-level flag. Enumeration supplies a global maximum under EX-A. Thus every member of the declared 𝒞 is LO and a top-level certified HPM belongs to it. This validates the event inclusion, including equal-score ties and disabled LS0. No claim that local_limit is the complement of local_certified is introduced.

   q is explicitly integral and below K, so the improving addition is feasible. The empty intersection is [p]; φ_n=+∞ when q<s₀ is declared. In that case no screened certified model in the size range can exist on the screening event, so the later refit/exactness conclusions are vacuous there, rather than requiring an inverse on a nonexistent superset.

   Section 3 now says the bridges lower-bound Γ/Ψ and that A1/A1° supply the additional coefficient/growth conditions. It no longer asserts that a positive floor or identifiability margin alone implies MC. SCR-R explicitly refers to a refit the method does not output; its simultaneous sparse Gaussian projection bound handles adaptive selection without a conditional-normality claim.

   **Proposed fix:** None.

8. **NOTE — R01 finding 12 is substantively fixed; one optional indexing clarification remains useful.**

   **Location:** STATEMENT Model G, EX-A, §3 illustrative Gaussian-row paragraph; scr_lib.py:36-38; v3_run.R and v3_fit.R original-index output conversion.

   **What is wrong:** No mathematical blocker in the declared retained-design setting. A reader applying the notation directly to raw inputs could still benefit from an explicit relabeling sentence.

   **Evidence:** Model G now states deterministic standardized triangular arrays, retained nonconstant p, n≥3, p≥2 for asymptotics, σ>0 possibly varying, and conditioning with errors independent of random X. EX-A explicitly disclaims numerical margins. The Gaussian illustration now assumes a correlation-matrix floor and is explicitly not proved or used in any theorem. This removes the raw-covariance/standardization counterexample from R01. It should not be promoted to a standalone proved random-design corollary or precise external citation without further work.

   The current numerical normalizer is logsumexp(logw + log binom(p,k)), including the omitted multiplicities; production v3_score.h uses the same formula. I verified the source correction, not the claimed rerun accuracy. The varying-σ remainders in the statements checked above are relative to σ, and SCR-C's norm restriction is explicitly O(σ√n).

   The code reports original raw-column indices through ctx$orig, whereas the mathematical notation [p] indexes the retained design. These coincide when the standardized retained X of Model G is supplied directly. If the paper also discusses raw inputs with constants removed, apply the retained-to-original bijection consistently to S₀, Ŝ and 𝒞 before comparing them; no probability or score claim changes under that bijection.

   **Proposed fix:** Optional editorial sentence: “All reported model indices are identified with [p] through the retained-column map; raw-index output uses the inverse map.” This does not require another statement-lock round in the current fixed retained-design setting.

Verdict rationale: the substantive R01 findings 1–6 and 12 are closed at statement level. The self-normalized extension has sufficient hypotheses, the stated constants leave strict margins, and no new counterexample was found. LOCK authorizes this theorem package as the target for the remaining independent proof reviews; it does not certify all lines of L1–L6, numerical runs, floating-point flags, or an automatic delivery probability for the code.
