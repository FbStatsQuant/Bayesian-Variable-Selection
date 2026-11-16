# Council R1 — sol

Reviewed the frozen content identified by MANIFEST fd8b32a5540e5afcfdb73b94048ba7a1324f30a89ade786508ea04e9295bfc30. I independently recomputed the manifest digest and all 20 file hashes; all match. No git operations or subagents were used. I did not read other review briefs, reviews, dispositions, scores, LOG.md or CHECKPOINT files. Scratch verification output is confined to `reviews/R1_scratch_sol/`.

| id | decision |
|---|---|
| W3-PSHARP-R:AE | REJECT |
| W3-PSHARP-R:A2C | ACCEPT |

The master AE proposition and both corollaries are mathematically supported. The frozen AE record needs correction because TARGET and the reader change-summary advertise an unconditional two-sided expectation rate beyond the master. A2C is correct and faithfully reported.

**Overall score: 7.8/10.0. Gates: FAIL.** The score reflects F1 only; editorial findings do not reduce it.

## Gate verdicts

| gate | verdict | reason |
|---|---|---|
| G1 correctness | PASS | Both lemma proofs re-derived, including their consumed parent steps. No incorrect or unproved master-claim step found. Details below. |
| G2 hypotheses used = stated | PASS | STATEMENT §3.1–§3.4 are covered with their stated modes, deterministic quantities, conditional extension, and uniformity. A2-E's omitted spherical rank condition is recovered under its conclusion's premise. |
| G3 no hidden assumptions | PASS | Feasibility, dimensions, ranks, conditioning and independence are sufficient. In AE the orthogonal event is decoupled separately for each column; the spherical score vector is independent of the common noise event. No N→∞ is used in the parent steps consumed by AE. |
| G4 statuses, citations, records | PASS | REPORT's proof statuses are verbatim and conservative; its claim/premise pointers, REGISTRY summaries, scope and implies edges agree with the master. The parent citations supply the consumed identities and bounds. The §6 implications are valid. Stale reader metadata is E2. |
| G5 constants and rates | PASS | The master normalisation, both A1-E constants, truncation T=ϵ/(4c_n), assembly slack, and the A2C exponential constants check. The relative-standard-error wording is E1 and does not affect a theorem or its constants. |
| G6 faithfulness | FAIL | F1: TARGET:28 and READER_DELTA:22 advertise exactness of the expectation rate for every/fixed p without the upper-bound proviso required by STATEMENT:110–113. The main reader text §3 preserves that proviso, but these other frozen copies do not. |

## Mathematical re-derivation

### Parent steps and the coded target

The target in W3-POST/STATEMENT:16–39 and the parent's notation agree: K=min(p,⌊n/2⌋), ν=.01+n/2, b₀=.01, H=(n+1)G+I, D=det(H)/det(G+I), Q=yᵀy−nzᵀH⁻¹z, w(k)=1/[2 C(2p−1,k)]. The capped-prior normaliser cancels in every model ratio. The proof never substitutes a different prior or likelihood for this real-arithmetic target.

I checked parent `lemmas/S_one_step.md:7–57` directly. Completing the quadratic with Hessian H/n gives Lemma V and its raw-response scaling. The Schur complements are s=n²−(n+1)²gᵀH⁻¹g and n−gᵀ(G+I)⁻¹g, both positive. The eigenvalue of (n+1)²H⁻¹−n(G+I)⁻¹ is strictly positive for every Gram eigenvalue ≥0; hence D-ratio≤n, with equality exactly at g=0. Block inversion gives ΔQ=n(xᵀρ̃)²/s, and V gives Q≥0. The one-step prior ratio is (s₀+1)/(2p−1−s₀); −log(1−γ)≥γ and distinct feasible supersets give S(4). These identities also cover empty and rank-deficient truth models and do not need N→∞.

In parent `A_log_factor.md:22–37`, the normal truncated mean is the integral of the constant normal-density prefactor. For the sphere, log-convexity of Γ gives c_d√(2π) between (d−1)/d and √((d−1)/d). On t²≤τ≤d/2, −x−x²≤log(1−x)≤−x gives exponent bounds −τ²/(2d) and 3τ/(2d). Those steps need d≥3 and the displayed truncation range, not growing N. Parent :53–63 gives the exact orthogonal score identity and V bound using G, E, C and n≥3 alone. In particular the .06M bound in :62 follows from .04n/(n−1)≤.06.

For the spherical parent steps :75–99, I checked the spectrum e_i∈(0,1), the fit-score lower bound, and the conditional rotation-invariant score law. The loss Q−‖ρ̃‖² splits into yᵀP_Hy/(n+1)+yᵀP_H(I−P_H)y. The signal part uses e_i(1−e_i)λ_i≤1/(n+1), the noise part uses e_i(1−e_i)≤1/4. Thus the stated numerator bound over σ*²E₂ follows. Since s₀+1≤K≤n/2, m=n−1−r₀≥n/2. Chebyshev, Markov and a union bound give exactly 2/(n−1)+16/n+1/x; on the event, s_y²≤3M+4σ*² and E₂≥n/4 give the stated C₀ and 2x(r₀+1)/n. None of :75–99 invokes N→∞ or either parent logarithmic growth condition.

### AE: every section of the lemma

1. **Lemma T (:16–26).** Monotonicity and y/(1+y)≥y−y² apply because all terms are nonnegative. Independence of U_j from its own G_j is exactly enough for E Y. For the second moment, removing all indicators before using independence of the U_j gives E Y²≤cTL+L². No independence between different G_j, or between G_j and U_k for k≠j, is assumed or needed.

2. **Truncated means (:28–37).** The Gaussian mean is exactly 2√(log T/π). Substituting τ=2 log T into the checked sphere bounds gives lower multiplier (1−1/d)exp[−2(log T)²/d] and upper multiplier exp[3 log T/d]. I independently integrated 18 sphere cases, including d=3 and τ=d/2; all lie within the bounds.

3. **Truncation and assembly (:39–55).** From s₀+1≤K≤p, (2p−1−s₀)/p∈[1,2), ℓ≥½log n, and log T∈[ℓ−log(4/ϵ),ℓ]. Hence cT=ϵ/4 and the a_n comparison is valid after n>(4/ϵ)². In Lemma F the difference divided by Λ is (θb−1)+(ϵ−θα)+Λ(1−θ²). When Λ<1−ϵ it is at least ϵ/2−4|θ−1|−2|1−b|. The stated endpoint tolerances leave slack at least ϵ/8. When Λ≥1−ϵ the desired lower bound is nonpositive. Thus assembly does not require Λ→0. The starting-index dependence in the lemma is included.

4. **Orthogonal proof (:57–82).** C−u_ju_jᵀ is a rank n−2 orthogonal projection, so R_j is χ²_(n−2) and independent of g_j. The scores g_j are jointly independent because the fixed null vectors are orthonormal. Each U_j therefore is independent of its own event G_j, even though R_j includes the other scores. On the truncation event, E≤(n−1)[1+x√(2/(n−1))+2log T/(n−1)]. Multiplication by 1+.04/(n−1) gives exactly the e_n bound with coefficient 1.02. The exponent comparison and Lemma T yield the displayed L_n inequality. With ψ_n=√ω_n+log n/(2√n), x_n=ψ_n^(−1/2), e_n log T=O(√ψ_n+ψ_n²+ψ_n/√n), with the stated parameter dependence. The tail-defined starting index ensures all inequalities hold for every subsequent n, even for nonmonotone envelopes.

5. **Spherical proof (:84–107).** Conditional on ε, the entire ζ vector has the same product sphere law for every ε; integrating the conditional law proves independence of that vector and ε. Thus it is independent of the common G, and its coordinates are iid. The parent event bound gives e′_n exactly. Taking x=(ω′_n)^(−1/2) makes e′_n log T≤C₀ψ_n/√n+2√ω′_n→0 and the event failure probability tends to zero. The chosen starting index ensures d≥3 and 2log T≤(n−1)/2. It also ensures the assembly upper endpoint is ≤2: ψ≤1/4 gives 3log T/(n−1)≤3√n/[4(n−1)]≤1/2 for n≥4. The lower endpoint is positive. All convergence rates depend only on the stated common deterministic envelopes and constants.

6. **Uniform/conditional conclusion (:109–118).** N occurs only through the deterministic Λ. The conditional argument keeps S₀, p and the null-block index set deterministic, so multiplying by P(𝒜_n) is legitimate. If the proposed lower bound is negative, δ≥0 handles it without reversing any inequality. For Λ→0, division by positive Λ and then ϵ↓0 yields the exact liminf conclusion, also when P(𝒜_n)→1.

7. **A1-E (:120–129).** With fixed s₀ and all nulls, orthogonality forces p≤n−1+s₀−r₀≤2n eventually. Thus the new orthogonal growth condition is automatic. The spherical condition directly supplies ℓ=o(n). Consequently Λ→0. The multiplicity factor tends to one when p→∞; ℓ=(a+1/2)log n+O(1) yields √((a+1/2)/π). For fixed p, ℓ=(1/2)log n+O(1), giving precisely [2(p−s₀)/(2p−1−s₀)]/√(2π), times s₀+1. Bounded p need not converge for the main normalised liminf assertion.

8. **A2-E (:131–152).** The inherited p≥2 and s₀≤p/2 give F1–F2. B1 gives δ≥(s₀+1)/(3√n+s₀+1), so either antecedent implies s₀=o(√n). Since log p=o(√n), this recovers (r₀+1)log(pn)=o(n). Every deterministic sub-block inherits the witness structure and the same growth envelopes. Its increment Δ≤2√(ℓ/(πn))→0. The floor choice approximates min(Λ,1/4) within Δ; the empty-floor case is correctly treated by nonnegativity. Hence Eδ→0 forces Λ→0. The limit form then gives Λ=O(r_n), and ℓ≥½log n forces bounded s₀. This covers both clauses, including bounded p, and does not invoke an in-probability result as an expectation bound.

### A2C: every section of the lemma

For λ=0 both probability assertions and both expectation consequences are trivial. For λ>0, parent :121 applies under all-nulls, p→∞ and s₀/p→0; bounded Λ gives s₀=o(√n). Together with p−s₀→∞ this proves K−s₀→∞ and c_nN→0.

At each orthogonal addition, g=0, so the determinant ratio is exactly n and ΔQ=(xᵀy)²/n independently of previously added nulls. Thus the decrements add, 0≤Σ_Jγ<1, and the prior ratio is the product displayed in :34. Its factors dominate P_n and their denominators stay positive. The target therefore gives ratio≥c_n^j∏_J exp(νγ), and distinct subsets give (2.1).

Parent :64–68 legitimately supplies the common κ-event: N≤n−1 makes the logarithmic correction vanish. The truncation comparison in parent :45–46 applies to each term simultaneously; no independence of κ and scores is needed. The collision inequality follows by a union bound over repeated positions in the ordered tuple expansion, with coefficient C(j,2).

The truncated sum A_n has E A_n=Λ_n exactly. The parent Gaussian weak-law bound, whose proof is Chebyshev with E W²≤N E W, gives the stated lower concentration. Markov gives A_n=O_P(1); consequently B_n≤(c_nN)A_n=o_P(1) and B_ne^{A_n}/2=o_P(1). The latter only uses tightness, not an exponential moment. Every fixed J₀ eventually fits the cap. Choosing the polynomial degree, then the two fixed tolerances, proves odds≥e^λ−1−η with probability tending to one. The reciprocal argument establishes equivalence of the two families of probability statements, with potentially different tolerances. Boundedness of π gives both expectation consequences. No spherical multi-step conclusion is asserted.

## Sweep duties and adversarial cases

1. **Statement copies.** Both lemma claims and downstream corollaries match the master. REPORT points to the master and keeps its prose free of theorem restatements outside the required registry records. TARGET's changed-hypothesis map is consistent, but its parity row at :28 fails (F1). READER §3 gives the A1-E display, unchanged parent probability display, the A2-E consequence, and A2C critical cap with the appropriate witness scope. It explicitly conditions exactness on a matching upper bound. Its §2 summary fails that same limitation (F1). Other reader wording issues are E2–E3.

2. **Quantifiers/uniformity.** Checked every ϵ/η quantifier, eventual index and limiting assertion. The envelopes, not the particular designs or blocks, control AE's n₀. Finite-N truncation never uses a weak law. The parent N→∞ restriction is retained exactly where A2C needs that law. The random conditional extension preserves deterministic normalisers.

3. **Scopes/downstream uses.** A1-E supplies automatic orthogonal growth only after fixing s₀. A2-E recovers spherical rank control before applying AE, and uses its block-uniform n₀ correctly. A2C uses parent :121 with all its hypotheses and only the orthogonal parent κ-event. All consumed parent steps are available under these scopes.

4. **REPORT/registry and implies edges.** Both statuses equal their source proof-file status, `PROVED (by this seat, unchecked)`. AE includes the general-block expectation inequality, fixed-s₀ all-nulls consequence, growing-s₀ obstruction and witness-only scope; A2C includes the critical cap and expectation consequence. The full clauses remain anchored by the statement pointers, including A2-E(i) and its rank exemption. Dependencies account for Lemma V/S, the parent proof steps and B1. The AE implies edge follows because, for fixed s₀ and all nulls with p→∞, the multiplicity factor→1, ℓ≥log p eventually, and the parent's spherical hypotheses imply the new ones. The A2C edge is correctly restricted to finite positive critical limits: the strict gap e^λ−1−λ allows a fixed small η and eventually dominates every fixed (1−ϵ)Λ_n. Neither implies edge asserts a general conversion from expectation to probability. Supersession is left to HQ.

5. **DEPS hashes.** Recomputed all ten listed file hashes, not merely two. Every `sha` and every populated `checked_sha` matches. For example parent S is `261a72f734612e2bb1e227ec82bf202249225c40db0ddfe72e7d51538e540dda`, and AE is `e407d9587679316b300bef44f94e5f0e206300aba6f2c07133a760046fed8ac1`. I did not inspect the prohibited prior review files to assess their historical contents.

6. **Adversarial regimes and numerical fidelity.** N=1 is handled by Lemma T and the columnwise decoupling, fixed p gives the stated √(log n) expectation lower bound, and p as large as exp(o(√n)) is allowed by the spherical growth conditions with bounded rank. An orthogonal sub-block may be small even for huge p; its contribution still enters through the exact c_nN normalisation. Growing s₀ is constrained by model feasibility and, in A2-E's implication proof, B1. Rank deficiency causes no singular inverse because H and G+I are positive definite. I directly checked the target and A2C identities on all 31 nonempty null subsets of a rank-deficient truth example. I also reproduced all 20 N1 output rows byte-for-byte at M=400000, including standard errors. The importance weight is the correct product N(0,1)/N(0,V) density ratio; q, Q, D and prior weights match the coded target and all models are enumerated with K=p. The observations are not used as proof. The existing citation-check output was inspected; I did not run its git-based source reader because this review prohibits git operations. Consumed mathematical citations were checked directly against their allowed source files.

## Findings

**F1 — unsupported two-sided rate in derived copies (blocking).**

- **Locations:** `TARGET.md:28`; `READER_DELTA.md:22`.
- **Failure:** The parity row labels A1-E(b) as `E δ_n ≍ r_n at fixed p`, and the reader change-summary says exactness is extended “in expectation for every p.” A1-E(b) proves a lower bound. STATEMENT:110–113 and :121–123 explicitly leave the fixed-p upper half unchecked and assert no upper bound. READER §3:44–46 correctly retains the matching-upper-bound proviso, so its summary is also inconsistent with its proposed text.
- **Concrete refutation of the unrestricted fixed-p reading:** Take p=2, S₀={1}, a fully orthogonal standardised design, σ*²=1 and θ*₁=1/n. All A1-E hypotheses hold with fixed energy/coefficient bounds. The signal score is O_P(1), s_y²→1, and the exact singleton/empty posterior ratio is (1/3)n^(−1/2)exp(O_P(1))→0. Thus π(S₀)≤π(S₀)/π(∅)→0, and boundedness gives Eδ_n→1, rather than Eδ_n=O(r_n). The upper-bound assumptions, including signal strength where needed, cannot be omitted.
- **Exact correction:** Replace TARGET's clause label with `A1-E(b): E δ_n ≥ (1−o(1)) C_{p,s₀} r_n at fixed p`, where `C_{p,s₀}=(s₀+1)[2(p−s₀)/(2p−1−s₀)]/√(2π)`. Replace READER_DELTA §2 item 3 with: `The rate comparison distinguishes probability and expectation: the expectation lower bound holds for every admissible p; exactness is asserted only where a matching expectation upper bound is available.` No master or proof change is required.

**E1 — relative Monte Carlo error misstated (nonblocking).**

- **Location:** `TARGET.md:36`.
- **Failure:** `MC s.e. ≤ 5·10⁻⁴ relative` disagrees with the supplied output. For n=100,p=5,s₀=1, the reported relative error is 4.5·10⁻⁴/0.20422≈2.20·10⁻³. At n=10⁶,p=5,s₀=1 it is about 1.58·10⁻³. The reported absolute errors are all below 5·10⁻⁴.
- **Exact correction:** Replace the parenthesis with `reported absolute MC s.e. ≤ 5·10⁻⁴; relative MC s.e. ≤ 2.3·10⁻³`.

**E2 — stale reader proof-status note (nonblocking).**

- **Location:** `READER_DELTA.md:6–7`.
- **Failure:** “proofs written ... not yet proved or checked” conflicts with the two proof files' verbatim statuses and the reader's own :62 note. It understates the present proof status.
- **Exact correction:** Replace that parenthesis with `proofs in lemmas/, each with status PROVED (by this seat, unchecked); independent council review pending`.

**E3 — misleading explanation of the logarithm (nonblocking).**

- **Location:** `READER_DELTA.md:55–56`.
- **Failure:** “their maximum gives the √(log p)” misdescribes the proof's mechanism. For independent W=exp(Z²/2), max W/(N√log N)→0 in probability (a Gaussian tail bound and a union bound suffice); the truncated sum, whose mean is 2N√(log N/π), supplies the lower bound. This wording is inherited in the quoted reader explanation but should be corrected in the proposed replacement.
- **Exact correction:** Replace `needed (their maximum gives the √(log p))` with `used here (the sum of their truncated fit factors gives the √(log p))`. This describes the established route without claiming necessity beyond that route.

Counts: **C=0, S=0, F=1, E=3.** No stronger-theorem proposals. F1 prevents acceptance of this frozen package even though the two master proofs check.

COUNCIL-VERDICT round=R1 manifest=fd8b32a5540e5afcfdb73b94048ba7a1324f30a89ade786508ea04e9295bfc30 seat=sol score=7.8 gates=FAIL
