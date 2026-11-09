# R01 — W2-UNI statement-lock review

**Verdict: LOCK-WITH-CHANGES.**

Reviewer: Codex gpt-6.1-sol, high. Date: 2026-11-09. Reviewed STATEMENT.md v1 and PLAN.md against the three inherited protocols and all sources named in the review brief. Additional source checks: GEN STATEMENT §(C5) and APP STATEMENT §(F)/L6_ENUM.

The target has the right ordering: general population conditions first, named designs as applications. The metric extension and the one-factor extension appear mathematically viable. I found no counterexample to UNI-0 or UNI-1 under their complete stated assumptions. This is a statement lock, not verification of the proposed new lemmas.

The draft is not ready to lock unchanged. Its posterior hypothesis is incompletely specified; its containment/corollary claims confuse all-subset PTV with actual-block visibility; R3(c) contains an unfinished bound; OBS-k lacks a quantifier that determines whether it is true; and the polynomial-decay row invokes PLR outside PLR's scope. These can be repaired without changing the production method or the main growth exponent.

## Required changes

### 1. Specify LSF exactly and separate the random and fixed posterior statements

**Locations:** STATEMENT lines 38–40, 77–79. APP L1_POST defines specific j₀ and k̄_n; an unspecified O(log n) cutoff is not that hypothesis. A cutoff chosen too small can miss the weak-eigenvalue sets needed by the posterior proof. APP L1_POST(b) is a random-design result; (c) handles exact Grams. Merely imposing a population LSF on the comparison matrix in (E), without controlling its discrepancy from the actual Gram, does not imply the required sample eigenvalues.

For example, take the comparison matrix Σ=I, but take two equal standardised columns in X. Then (E) holds with δ_n=1, and Σ satisfies every population LSF. With S₀={1}, the equal-prior models {1} and {2} have identical likelihoods. Consequently π(S₀)≤1/2 for every response. Thus (i) must not be read as including unrestricted (E).

**Replace A1-post with:**

> (A1-post, random-design posterior.) Let j₀=⌈(2A+1)s₀⌉+1, m̄_n=⌈[s₀(A log n+log 2)+log 2+((s₀+2)/2)log n]/log(3/2)⌉, and k̄_n=min{p,s₀+max(j₀,m̄_n)}. For fixed φ>0, require λ_min(Σ_{n,S})≥φ² whenever |S|≤min(p,s₀+j₀), and λ_min(Σ_{n,S})≥ψ_n whenever |S|≤k̄_n, where ψ_n√n/(log n)^{3/2}→∞. No upper spectral bound is imposed. These are the sufficient LSF conditions of APP L1_POST; they are not asserted necessary.

**Replace the first and last sentences of (i) with:**

> Under design (R), (A1-post), polynomial dimension, fixed sparsity and the signal bounds of (A3), without PTV, the joint-law posterior rate is 1−π(S₀)=O_P(√(log n/n)), with the SL1 corollaries in APP L1_POST(b). This is APP L1_POST(b), independent of any factor representation. Fixed exact-Gram designs are covered separately under APP L1_POST(c). Approximate fixed Grams require verification of the T03♯ sample-design hypotheses and are not covered by population LSF alone.

If retaining the parenthetical BM-∞ relaxation, explicitly retain the bounded-energy requirement and cite T03♯ for that relaxation rather than calling it a verbatim restatement of APP L1_POST(b).

### 2. Use the weakest visibility hypothesis already supported by the factor engine

**Locations:** A3; UNI-1 lines 89–95; PLAN step 5. All-subset PTV is suitable for UNI-0 and is a convenient partition-free sufficient condition for UNI-1. It is stronger than FAC-A needs. FAC-A L2 uses TV on actual blocks. FAC-A L5.1 uses TV-pop on a deterministic family covering the realised blocks with probability tending to one. Its S5 certificates concern unions of at most three whole groups, not every subset of size at most 16 (L5.2–L5.3).

Concrete strictness: take compound symmetry ρ=1/2, θ=(1,−3,0,…), and singleton method blocks. Both truths have nonzero marginal partial signals, respectively −1/2 and −5/2, so actual-block TV holds. But conditioning truth 1 on any null gives partial covariance zero: (1−ρ)[1+ρ(−2)/(1−ρ+ρ)]=0. This sequence is allowed by FAC-A's fixed-design theorem but excluded by the draft's PTV. It can have any growing p below the factor exponent.

**Replace UNI-1's visibility/design clause with:**

> Assume the fixed-sparsity and coefficient bounds of (A3). Under (R), assume TV-pop of FACA STATEMENT §3 for a deterministic family 𝔅_n covering every realised method block on a design event of probability tending to one. All-subset PTV(a₀) is a sufficient partition-free condition, obtained by taking 𝔅_n to be all subsets of size at most 16. Under (E), assume δ_n√(p log log n)→0 and TV on the actual blocks, as defined in FACA STATEMENT §3. PTV is not additionally required for (E).

**Replace the containment sentence with:**

> The structural class includes every FACA representation with bounded idiosyncratic blocks; for its group partition, c_𝒢=c_min and κ_UNI=κ_FACA, so the exponent is unchanged. With the same TV or TV-pop hypotheses, UNI-1 includes FAC-L. The extension beyond bounded idiosyncratic blocks is a new target requiring U-LOC.

**Replace PLAN step 5's random-design clause with:**

> Use FACA L5.1 with TV-pop on a deterministic family covering the actual blocks; use all-subset PTV as a sufficient special case. Retain the certified smaller covering families when importing FACA's instances.

This preserves a general main theorem and avoids adding an unnecessarily strong condition just to call it design-agnostic.

### 3. Replace the unfinished factor-entropy statement with a quantified bound

**Locations:** STATEMENT R3(c), PLAN step 4(c), risk concerning a hidden 2^p union. The route works, but there really is a union over all subsets, paid for by a size-dependent threshold. It must be counted explicitly. Independence across F_T is neither available nor needed.

**Replace R3(c) and PLAN step 4(c) with:**

> For G=|𝒢|, b=2^{γ̄}−1 and 1≤h≤G, the number of nonempty T with h_𝒢(T)=h is at most C(G,h)b^h. Put x_h=log C(G,h)+h log b+2 log(h+1)+log log n+log 2. With probability at least 1−1/log n, simultaneously for all nonempty T, |F_T|≤√(2x_{h_𝒢(T)}), where F_T=λ_TᵀΨ_TT⁻¹ζ_T/√s_T is marginally N(0,1). Therefore |λ_TᵀΨ_TT⁻¹ζ_T|/s_T≤√(2x_h/(c_𝒢h)). In particular this is at most c_𝒢^{-1/2}[√(2 log(eγ̄p/|T|))+O(1+√log log n)], uniformly over nonempty T. Constants depend only on γ̄. The empty set is handled separately using s_∅=0 and W_∅=ξ₀.

Indeed, the Gaussian two-sided tail followed by this union gives a failure bound at most (log n)^{-1}Σ_{h≥1}(h+1)^{-2}. The within-group patterns contribute O(h), which becomes O(1) after division by h. Thus the leading constant and α₀ are preserved. A union over group supports alone would omit b^h choices; a uniform threshold based on 2^p would lose the desired rate for small sets.

**Replace PLAN's corresponding risk sentence with:**

> The factor bound unions over all subsets with an explicit h-dependent entropy budget; it does not require a subexponential total number of subsets. The idiosyncratic bound unions only over local references and coordinate atoms. Both bounds must have deterministic uniform remainders o(√log n).

### 4. Make the metric toolkit and idiosyncratic remainder specifications valid for non-unit Ψ

**Locations:** STATEMENT R1/R3(b), PLAN steps 2 and 4(b). The pseudometric extension is sound in principle: restricted balls obey the same growth bound, and i↦δ(i,j) is 1-Lipschitz by the triangle inequality. No Euclidean property is needed in LOC2 L3's conjugation argument. However, separation was used to start shells at 1, and LOC2's regression bound also used unit diagonal. Ψ is not generally unit diagonal.

**Add to R1 and PLAN step 2:**

> All shell sums begin at m=0, with shell counts bounded by C₀(m+2)^{d₀}. For matrices with spectrum in [c,C], use Var(ζ_l|ζ_T)≤C, not ≤1, and hence (B^{-1})_{ll}≥1/C in the regression formula. Constants in RB_M, TAIL_M and LOCL may depend on C. Prove the bounds uniformly for principal submatrices and conditional covariances. In the correlation factor setting Ψ_jj≤1 is available as an additional simplification.

**Replace the LOCL specification with:**

> Establish constants B,t>0 such that |β_T^Ψ(l)_v|≤B exp(−tδ(l,v)) uniformly in T,l,v, and a uniform ℓ¹ regression bound L₀. For U=T∩B(l,r), V=T∖U, show β_U−β_{T,U}=Ψ_UU^{-1}Ψ_UVβ_{T,V}, whence ‖β_T−β̄_U‖₁≤(1+L₀)‖β_{T,V}‖₁≤ε(r), with ε(r)=(1+L₀)B C₀Σ_{m≥⌊r⌋}(m+2)^{d₀}e^{-tm}→0. Empty index sets have zero coefficient vectors.

**Add to R3(b)/PLAN step 4(b):**

> For U=T∩B(l,r_n), control the local standard normals (ζ_l−β_Uᵀζ_U)/√ψ_{l|U} over at most p·2^{C₀(1+r_n)^{d₀}} references. Use TAIL_M to compare ψ_{l|U}/ψ_{l|T}=1+o(1) uniformly, and use LOCL with coordinate atoms to bound |(β_T−β̄_U)ᵀζ|≤ε(r_n)max_j|ζ_j|. With r_n=⌈(log log n)²⌉, log(reference count)≤log p+o(log n), max_j|ζ_j|=O_P(√(log p+log log n)), and the resulting uniform idiosyncratic envelope is √(2 log p)+o(√log n).

For completeness, the proposed exact decomposition survives general Ψ. Replace U everywhere in FAC-A U(a)'s ψ, λ̃ and Ξ by T. Then Ξ_{l,T} is independent of (ξ₀,ζ_T), hence of W_T, and the same formula holds. Block-diagonality was used for the local representation and the subsequent block-energy bound, not for the underlying orthogonal decomposition. This is a viable proof obligation, not a new assumption.

### 5. Remove an unnecessary uniform pervasiveness floor; make automatic bounds and feasibility explicit

**Locations:** A2-1, κ′ paragraph, UNI-1, §6. In the unit-diagonal setting, Ψ_jj=1−λ_j²≥c, so |λ_j|≤1. RB_M and ψ_{l|T}≥c then give κ′≤(1+L₀)/√c. Thus κ′ finiteness is not missing, but it does not follow from LOC_M alone if λ is arbitrary.

More substantially, FAC-A does not impose a fixed lower bound on c_min. Take Ψ_n=(1−a_n)I, λ_n=√a_n·1, with a_n>0 tending to zero. FAC-A's ψ₀ can be fixed, κ=1, but c_min=a_n/(1−a_n)→0. With one fixed truth its visibility requirements hold. This is excluded by A2-1, so Required Change 2 alone does not repair the claimed containment. The new union bound needs c_𝒢>0 and a bounded ratio κ, not c_𝒢≥c₁ uniformly: its c_𝒢^{-1/2} factor is multiplied by κ′, giving κ. The ξ₀ term is controlled by the automatic uniform bound on κ′.

**Replace A2-1 and remove c₁ from the fixed constants list:**

> (A2-1, subset exposure ratio.) For a partition 𝒢_n into groups of size at most γ̄, define c_{𝒢,n}=inf_{∅≠T⊆[p]}s_T/h_𝒢(T). Require c_{𝒢,n}>0 at each n and κ_n=κ′_n/√c_{𝒢,n}≤κ̄ for a fixed κ̄≥1. A uniform positive lower bound on c_{𝒢,n} is sufficient but is not required. For singleton groups, a uniform lower bound on every |λ_j| is one sufficient way to obtain that stronger condition.

**Replace the parenthetical after κ′ with:**

> In the unit-diagonal representation Σ=λλᵀ+Ψ, |λ_j|≤1 and ψ_{l|T}≥c; RB_M therefore implies κ′≤(1+L₀)/√c uniformly in n. Finiteness is automatic under the complete representation assumptions, not under LOC_M without a loading bound.

**Add after A2-1:**

> This is a representation-dependent sufficient ratio condition for the full-lattice route. It is not asserted necessary for consistency. The stronger condition c_{𝒢,n}≥c₁>0 would force every loading to be uniformly bounded away from zero by singleton tests; that stronger condition is not imposed here. Neither condition should be identified without qualification with average factor pervasiveness.

**Add to UNI-1:**

> The strict exponent condition implies p=o(n), so K_n=p eventually and the full lattice is feasible. Under (R), entrywise Gaussian correlation concentration gives ‖R̂−Σ‖_op=O_P(p√(log n/n)); multiplication by √(p log log n) tends to zero under this exponent condition, as in FACA L5.1. No separate p≤K_n assumption or upper bound on λ_max(Σ) is needed.

**Replace §6's phrase about c_𝒢=0 with:**

> Representations with c_{𝒢,n}=0 or without a uniform bound on κ_n. Vanishing common loading scale is not itself excluded when c_{𝒢,n}>0 and κ_n stays bounded.

### 6. Correct the corollary table; distinguish structural membership from a complete instance

**Location:** §5. Exact replacement rows follow. Retain the LOC-d row, but add PTV and spectrum checks. The heading currently promises verbatim statuses without supplying them; state them explicitly.

> | Existing result and source status | Relation to UNI | Exact qualifications |
> |---|---|---|
> | APP POST (inside APP PROVED-CHECKED) | UNI-P under (R) | Exact LSF cutoffs, fixed signal bounds; fixed exact Grams use POST(c). |
> | APP LOC; GROW AR(1); GEN study S1/S3/S4/S6 (source reports PROVED-CHECKED) | UNI-0 for the specified random-design instances | Ordering/block pseudometric and fixed spectral bounds; retain the source's PTV or verify it. For study bounded-block layouts, verify at most one truth per independent group, giving PTV(cθ_lo). This does not import every masked-truth theorem of GEN. |
> | LOC2 LOC-d (PROVED-CHECKED) | UNI-0 | Separated Euclidean sites give polynomial growth; source spectrum and PTV assumptions retained. |
> | LOC2 LOC-BF (PROVED-CHECKED) | Additional PLR instance | Uses the reference/atom construction of LOC2 L4 Part B; no membership of growing groups in fixed-constant LOC_M is asserted. |
> | LOC2 polynomial decay α>17/2 (PROVED-CHECKED) | Separate extension of the engine | Uses LOC2 L6's polynomial-size re-run of the toolkit, NA and assembly; not Theorem PLR directly, whose relevance sets are polylogarithmic. |
> | FACA FAC-L (PROVED-CHECKED) | UNI-1 after Required Change 2 | Bounded idiosyncratic blocks give LOC_M, c_𝒢=c_min and κ_UNI=κ_FACA; retain AG, growth, and actual-block TV or covering-family TV-pop. S5 inherits its certified family of unions of whole groups. |
> | FACB FAC-CS (PROVED-CHECKED) | Overlapping special case below 1/6, otherwise separate | Fixed exact-Gram CS, including column signs, with FACB's signal and method assumptions and p≤n/2. The all-subset PTV subclass below 1/6 is an instance of the original UNI-1. Masked truths under FS′ remain a separate result; they are not instances of a PTV theorem even below 1/6. |
> | APP ENUM (inside APP PROVED-CHECKED) | Separate enumeration override | Require the coded EXB inequality eventually, EX-A, and posterior consistency. LSF alone does not activate enumeration. It gives output-intersected selection consistency, not an independent delivery theorem. |

The S5 source certificate is not an all-subset PTV certificate. The FACB masked exception is real: at ρ=1/2, coefficients (1,−2) have a truth with zero marginal covariance, violating PTV already for U=∅. With its masked truth sharing a block with a null, this is of the FS′ type described in FACB REPORT. Therefore mapping all FACB results below 1/6 to the draft's UNI-1 is false.

### 7. Quantify OBS-k and restrict the conclusion to the proposed route

**Locations:** (iii′)(a), R5, PLAN step 7. The cutoff m has no definition. The assertion is false for general m_n. For even p, take half the loading rows equal to √a e₁ and half equal to √a e₂, Ψ=(1−a)I, fixed a∈(0,1). This is a unit-diagonal two-factor design with bounded loadings. For m_n=p, the infimum has only T=[p], and its normalised information matrix is a/[2(1−a)] I₂, uniformly positive.

**Replace OBS-k's proposed statement with:**

> Fix k≥2 and a positive integer m independent of n. If p_n→∞, the loading rows are uniformly bounded, and Ψ_n⪰cI for fixed c>0, then inf_{m≤|T|≤p_n} λ_min(Λ_TᵀΨ_TT^{-1}Λ_T)/|T|→0. This obstructs an extension requiring uniform positive information on every subset of size at least that fixed m. It does not obstruct assumptions imposed only on sufficiently large subsets, other proofs for k≥2, or consistency itself.

A bounded-region pigeonhole argument supplies m arbitrarily close loading rows; their Gram approaches rank at most one, and Ψ_TT^{-1}⪯c^{-1}I. If a growing cutoff is intended, state and prove its admissible growth separately. Also replace “would need” by “one proposed extension would impose”: the scalar proof does not establish necessity of that hypothesis for every multifactor argument.

### 8. Remove the circular relevance-set definition and specify the abstract delivery input

**Locations:** UNI-0 line 83; R4 lines 118–119. The enlargement test currently uses the already-enlarged Q. Use Q⁰, as LOC2 L4 does. R4 should specify the interval lattice and exact start-mode premise, since these are what permit the descent argument.

**Replace UNI-0's relevance-set clause with:**

> With the conditional-decay constants (K₂,t₂), let d_n=⌈(½log n+log(1+s₀θ_hiK₂))/t₂⌉ and Q⁰={l:min_{j∈S₀}δ(l,j)≤d_n}. Set Q=Q⁰ if p≥2|Q⁰|+32s₀+1, and Q=[p] otherwise. Then |Q|=O((log n)^{d₀}); eventually Q=[p] or K_n≥2|Q|+32s₀+1.

**Replace R4 with:**

> For a deterministic Q⊇S₀, let 𝓛={T:S₀⊆T⊆Q}⊆Ω. Assume P(Sand_n(Q)∩NA(𝓛)∩TL(𝓛))→1 and E[1−π(S₀)]→0. Under the exact start-mode, complete-scan LS0, cap, input-validity, machine and allocation premises of FACA L7, the deterministic LS0 scores S₀ with probability tending to one and the delivered reported model satisfies P(Ŝ⁺=S₀)→1. Derive this through the LS0-scoring event, not from D_n→0 alone. Check input validity separately in each design setting.

## Plan assessment and optional suggestions

After these changes the plan is viable. CT_M needs only polynomial shell counts and the distance function's 1-Lipschitz property. Zero-distance clusters have uniformly bounded size by N_δ(0)≤C₀; they introduce no singularity because a spectral floor is independently assumed. The block pseudometric example is valid: at radius p its ball is all p coordinates, and p≤γ̄(1+p); below p it contains only its bounded block. No relation to the algorithm's partition is needed for the metric toolkit.

The general one-factor identity, LOCL construction and stratified entropy bound above explain why I do not reject the new theorem target. FACA U(d)'s perturbation proof uses a correlation diagonal and a uniform lower spectral bound, not block-diagonality or a bounded upper factor eigenvalue. Its use here is credible. Keep its common deterministic envelopes and random-design transfer checks in the new proof.

Optional: place the general reference/atom PLR engine alongside UNI-0/UNI-1 as a principal theorem. That would make the owner requirement more transparent and preserve a general home for growing groups, while the polynomial-size extension remains separately identified. Do not describe all of A2 as standard approximate-factor assumptions: exponential metric decay and a bounded subset-exposure ratio are additional sufficient structure.

Optional: strengthen falsification probes by exhaustively enumerating every T at p≤10, including arbitrary signs of λ, a non-unit Ψ diagonal, small positive metric distances, zero-distance clusters, both decay branches and sets chosen to maximise the factor term. Greedy samples alone can miss an entropy or normalisation error. These are tests of asymptotic proof identities and assumptions, not a request for performance guarantees at a particular n.

Two covariance counterexamples above were independently evaluated using Python -B with exact fractions, entirely in memory: singleton-block CS yielded marginal truth covariances −1/2 and −5/2 and conditional covariance 0; the masked CS example yielded marginal covariance 0. Their algebra is given here, so no numerical result is needed as evidence. An initial NumPy import was unavailable; the exact checks used the standard library. No auxiliary files were created, no other file was edited, and no git commands were run.

**Lock disposition:** apply Required Changes 1–8 before locking. Proceed to the metric and U-LOC proofs afterward, retaining the protocol's separate lemma checks, fresh midpoint and final review gates. This review does not upgrade any new W2-UNI result to PROVED-CHECKED.
