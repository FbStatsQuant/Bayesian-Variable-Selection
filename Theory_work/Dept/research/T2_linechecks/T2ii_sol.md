# T02(ii♯) → W3-POST Theorem 1, 5(a): fresh line check
Aliases: P1 = [PROOF_v3.tex](/home/fb31/BVS-wt/W3-T03ACC/Theory_work/Wave3/W3-T03ACC/sources/P1/PROOF_v3.tex); T03R = [PROOF.md](/home/fb31/BVS-wt/W3-T03ACC/Theory_work/Wave3/W3-T03ACC/sources/W1-T03R/PROOF.md); W6 = [W6-FIXREV2_STATEMENTS.md](/home/fb31/BVS-wt/W3-T03ACC/Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md).
Aliases: COMMON = [00_COMMON.md](/home/fb31/BVS-wt/W3-T03ACC/Theory_work/Wave3/W3-T03ACC/sources/common/00_COMMON.md); POST = [STATEMENT.md](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave3/W3-POST/STATEMENT.md); BRIDGE = [L1_POST.md](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Wave2/W2-APP/lemmas/L1_POST.md).
VERIFIED — Both P1 and W6 match [inputs.sha](/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/T2_linechecks/inputs.sha):1–2. T03R SHA-256 = 1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4 (additional input, not pinned there).
VERIFIED — Scope: W6:48–49 and T03R:149 state strict-superset exclusion; “5(a)” is POST:87–88, not a numbered subitem of W6's T02(ii♯).
VERIFIED — COMMON:9–14; P1:42–58,242: deterministic contrasts preserve Gram matrices and signal norm; ε_c is unconditionally N(0,σ*²I); s_y>0 almost surely.
VERIFIED — P1:68–87,155–170: completing the square gives D and Q; the IG integral gives the common exponent ν=0.51+(n−1)/2 and the stated marginal ratio.
VERIFIED — P1:101–110 (lem:spec): functional calculus proves smoother bounds, inverse order proves nesting, and interlacing of the increasing f gives D_S/D_S₀≥[(n+1)/(1+1/g)]^j.
VERIFIED — P1:148–150 (lem:chi): MGF/Markov, variance/Cauchy–Schwarz, and explicit truncated-density integration give (a)–(c); Γ(x+1)≥∫_x^∞t^xe^(−t)dt≥x^xe^(−x) justifies the last bound.
VERIFIED — P1:123–136 (lem:prior): beta integral normalises the prior; consecutive weight ratios yield the product in :134; its factors give ≤2·2^(−j), and C(s₀+j,j)≤(j+1)^s₀. The cap cancels from model ratios.
VERIFIED — T03R:22–36,44–59,152; P1:387–391: q-ratio multiplication and log(1−x)≤−x establish E1(b), hence E2(i), m♯≤m_n=O(log n), and δ_n log n→0 (here s₀≥1).
VERIFIED — T03R:132,139,143,153: SE_w alone proves B1's full rank, rank-j projection difference, exact χ²_j law, and determinant bound. SE_λ, although bundled into Lemma B's header :138, is unused in B1's proof and is unnecessary here.
VERIFIED — P1:399,409 (lem:good/G1), T03R:154: Chebyshev gives 2/log²n with the substituted cutoff; no conditioning on the good event occurs.
VERIFIED — P1:400,409–413 (G2): 2k log2+4x_k≤C_A k log n; rank≤k and ≤p^k sets give Σe^(−k)/n≤1/n, then |T|≤m♯ gives the advertised threshold.
VERIFIED — P1:401,413 (G3): B1 supplies the exact χ²_j law for the required deterministic J; the same union bound gives ≤1/n. Thus P(G_nᶜ)≤2/log²n+2/n.
VERIFIED — P1:425–426 (lem:onG/a): δ_n→0 permits the deterministic thresholds; G1 and ‖μ‖²≤nM imply ‖y_c‖²≤4n(M+σ*²).
VERIFIED — P1:427 (lem:onG/b): Q_S≥‖(I−P_S)ε_c‖²; G1 and G2 give (n−1)σ*²(1−δ_n)>0 for S⊇S₀, |S|≤m♯.
VERIFIED — P1:428–429 (lem:onG/c): nesting gives nonnegativity; the lower smoother bound uses only R on S₀, retaining η_n=1/[(n+1)(n−1)φ₀²]. Projection cancellation gives the stated χ²_J upper bound.
VERIFIED — P1:440 (lem:one): for x≥y>0, ∂_b[(2b+x)/(2b+y)]=2(y−x)/(2b+y)²≤0; taking its b↓0 bound is legitimate without defining a rate-zero prior.
VERIFIED — P1:442–444: substitution into ν(Q_S₀−Q_S)/Q_S reproduces ϑ_n and ρ_n exactly; ϑ_n≥1 and G3 give ϑ_nχ²_J/2≤χ²_J/2+jζ_n.
VERIFIED — T03R:155; P1:435,444: replace only the determinant factor by (n+1)^(−j/2)(1+1/g₀)^(j/2); the prior ratio and all quadratic-form bounds remain valid.
VERIFIED — P1:445; T03R:152,155: ζ_n→0 follows from δ_n log n→0, and ρ_n=O(n^(−1)) from η_n=O(n^(−2)); weakening the superset floor does not alter η_n.
VERIFIED — P1:174–208,454: z_S^c=s_y z_S and Q_S^c=s_y²Q_S give an S-independent marginal factor; hence posterior odds equal contrast odds at b=b₀s_y². The bound holds for every b>0, including this random value.
VERIFIED — P1:452–459; T03R:151,156: split at m♯≤K; π(S₀)≤1 bounds T₁ by posterior odds; deterministic truncation defining V_n equals one on G_n and remains available for unconditional expectations.
VERIFIED — P1:459–461: truncated χ² moments and lem:prior(e) give E V_n≤2Σ(j+1)^s₀ r̄_n^j; dependence among different J is irrelevant to this first-moment bound.
VERIFIED — T03R:156; P1:463: r̄_n²≤e^(2ζ_n)eC_A(1+1/g₀)r_n²/4≤c₂²r_n² eventually. Fixed g₀ makes c₂ constant; r̄_n≤1/2 and K_s₀<∞ give E V_n≤2K_s₀c₂r_n.
VERIFIED — P1:465,469: Markov plus P(G_nᶜ)→0 yields T₁=O_P(r_n); e^ρ_n→1 justifies its omission after limsup in the final display.
VERIFIED — T03R:89–91; P1:325–359: R bounds the truth smoother bias; restricting v/σ*² to [1,1+n^(−1/2)] gives exponent ≥−Λ_n, interval length σ*²/√n, and EΛ_n≤C_Λ. No superset eigenvalue floor enters this denominator.
VERIFIED — T03R:93–97; P1:317–321,213–221,234–250,255–264: fixed-rate numerator densities give EΘ^(1)=1; pointwise mixed-endpoint transfer and den′ retain the exact prior ratio R_m; two Markov bounds and the scale-event estimate give the stated uniform-in-m tail probability bound.
VERIFIED — T03R:46–47,80–85,97,156; P1:467–469: the deterministic cutoff gives T₂≤(1+1/n)^(s₀/2)n^(−1/2)Θ♯=O_P(n^(−1/2))=O_P(r_n); R_m=0 gives T₂=0. Combining T₁,T₂ proves T03R:149 under exactly its hypotheses.
VERIFIED — POST:63–88,120–122: fixed-design 5(a) reproduces T03R:149 and W6:48–49, using G, energy, the truth floor and F_w only. Neither beta-min nor F_λ is needed; swaps and arbitrary false-positive models are not asserted to be controlled.
VERIFIED — POST:95–100,114–118 cites an additional random-design form, beyond the source's fixed-design statement. Common constants and noise independent of (X,θ*) permit conditioning/integration: the bounds above are uniform in admissible designs. BRIDGE:49–57 supplies floors/energy without its beta-min step; :58–66 explains the transfer. This checks the use of 5(a), not the separate Gaussian-design concentration citation.
Findings: C=0, S=0, F=0, E=0. No proof repair required. No scratch created; no git commands or git-state changes; only this report written.
T02ii-5a: VERIFIED
