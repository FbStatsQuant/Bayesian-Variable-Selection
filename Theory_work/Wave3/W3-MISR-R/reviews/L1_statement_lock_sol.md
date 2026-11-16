# L1 statement-lock review — Sol

Reviewed the frozen inputs named in the brief. This is a statement-level review of v1.0 and the viability of PLAN §1; it does not certify proofs that have not yet been written.

## Findings

**L1-1 — MAJOR — §4, KL(ii), [STATEMENT.md:124](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:124), especially lines 126–127.** The full-design conditional Gaussian/KL statement is correct, but the assertion that jointly Gaussian rows recover BASE's *row-wise* reading is too broad with the permitted intercept α = α(X^r_𝒞). For example, take iid standard Gaussian candidate rows, no omitted columns, independent standard Gaussian noise, and α = (X^r_𝒞)²_{2,1}. Then, conditional on the entire candidate design, y^r has exactly the asserted Gaussian law. However, y^r_1 given its own candidate row is a Gaussian plus an independent χ²₁ shift, hence is not Gaussian. Centring the population candidate rows does not fix this. This satisfies §2(b), including its intercept restriction.

**Concrete fix:** retain the full-design statement and replace the row-wise sentence with: “For jointly Gaussian rows as in (E1), with a deterministic intercept α (and the deterministic parameters of that example), this also gives BASE's row-wise reading.” Alternatively, delete the row-wise sentence. PLAN H1 must justify this restricted reading; currently it only sketches reading (i). The contraction results do not require this restriction on α.

**L1-2 — MINOR — §2(d), [STATEMENT.md:77](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:77).** The displayed partial converse is correctly conditional, but “Neither … the omitted-part contrasts can be non-Gaussian; their covariances …” omits that qualification. With design-dependent v, the centred omitted contrasts can have a non-Gaussian marginal scale-mixture law, and their unconditional covariance need not even exist. For example, let the candidate design encode a non-degenerate Bernoulli B, let UᵀX^r_𝓜β_𝓜 given that design be N_N(0, (1+B)I_N), and take independent N_n(0,I_n) noise and γ=0. Then (GR^c | σ(X^r_𝒞)) holds with v=2+B, while the marginal omitted contrasts are not Gaussian.

**Concrete fix:** say “The noise contrasts are Gaussian, and the centred omitted-part contrasts are Gaussian **conditionally on the candidate design**; their conditional covariances add to v(X^r_𝒞)I_N.” No change to the display is needed.

**L1-3 — MINOR — §2, conditional-mean remark, [STATEMENT.md:88](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:88).** The ordinary integrable-variable notation E[UᵀX^r_𝓜β_𝓜 | X^r_𝒞] needs a convention under the expressly moment-free design assumptions. The conditional Gaussian kernel has a finite first moment at each design, but the random vector need not be integrable unconditionally. For example, X^r_𝒞=Zu for a fixed non-constant column u and a Cauchy Z, X^r_𝓜=X^r_𝒞, β_𝓜=1, γ=1 and τ²=0 satisfy (OV^c); the displayed omitted contrast is not in L¹.

**Concrete fix:** identify the mean as the integral against the regular conditional law, or explicitly adopt the corresponding locally integrable conditional-expectation convention. Do not add a global moment assumption: it is unnecessary for any theorem here.

**L1-4 — MINOR — PLAN H2, (RD), [PLAN.md:14](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/PLAN.md:14).** The proposed g_n feeds an N-dimensional contrast vector to Π(· | x,y^r), whose second argument is an n-dimensional raw response. Also, the proposed function must be defined at the zero-contrast input before it is called Borel on the entire product space. These are repairable formulation gaps, not obstructions to freezing.

**Concrete fix:** use Ψ(x,u):=Π(· | x,Uu), as in BASE (R3), and define

g_n(κ,w):=Ψ(x,Uᵀxβ+√v w)(B_n(κ))

away from zero contrast, with any fixed Borel posterior-kernel extension at zero. For every fixed κ the exceptional w has Gaussian probability zero. Prove joint measurability by integrating the Borel bad-set indicator against the finite-model Gaussian/inverse-gamma posterior kernel on each configuration stratum. Then freeze 1{g_n(κ_n,W_n)>η}.

## Answers to Q1–Q6

**Q1. CorG-min.** The displayed results (a)–(e) are viable and correctly quantified, subject to the explanatory amendments L1-2 and L1-3.

For (a), α cancels identically under Uᵀ, even if it depends on the noise. Independence in (N) gives conditional convolution, and (OV^c) gives conditional residual covariance (σ²+τ²(x))I_N and zero mean. Division by the positive Borel square root gives the same standard Gaussian kernel at almost every design, hence independence of σ(X^r_𝒞). No candidate moments or row assumptions are needed. The null-event reference configuration is harmless. Applying MIS-R (ii) still requires its inherited class/event hypotheses; its size slices cover bounded positive sizes, not an unconditional selection guarantee for every random support.

For (c), conditional characteristic-function division is valid. On a common full-measure set, use a countable dense set of arguments and continuity. A negative v(x)−σ² would give a characteristic function of modulus greater than one, so v≥σ² almost surely. The proposed positive-part extension of τ² is Borel and satisfies the required global positivity: when σ²=0 it equals v>0, and when σ²>0 the sum is automatically positive.

For (d), conditional independence follows from ε being independent of the pair (X^r_𝒞,X^r_𝓜). At a design outside one null set, the sum of the two independent contrast vectors is a non-degenerate Gaussian vector. Cramér's decomposition theorem, applied to scalar projections, makes the fixed marginal noise-contrast law Gaussian; its mean b and covariance Σ_ε are deterministic. Division then yields the stated conditional omitted-component law and the almost-sure PSD inequality. Degenerate component covariances are allowed. Only the marginally unqualified explanatory sentence needs correction.

For (E1), the Moore–Penrose formulas are correct. Positive semidefiniteness of the joint covariance implies range(Σ_𝒞𝓜)⊆range(Σ_𝒞𝒞); the stated residual is therefore uncorrelated with, and jointly Gaussian independent of, the candidates. Its covariance is the stated generalized Schur complement. Positive individual candidate variances ensure non-constant columns almost surely. No global invertibility is needed.

**Q2. CorGb-plus.** Yes. Positive population column rescaling leaves the standardized X, Ω, prior and scores unchanged, hence leaves the coded target unchanged. Rescaling coefficients by √Σ_jj preserves the support, signal variance and beta-min ratio. The problem can consequently be proved with covariance R and unit diagonal; this uses the actual standardized target rather than an invariance assertion about a raw-design prior.

Every nonempty covariance submatrix needed for the sparse Gaussian concentration argument is positive definite by the stated floor. Joint positive definiteness of the entire candidate covariance is unnecessary. The floor on the support also supplies the positive signal variance needed in the energy step. The same SD and sparse-eigenvalue events give φ₀²=c_R/8 and (F_w;1); A0 supplies a common C_OS. On the SD event,

min_j θ_j² nφ₀²/(σ²_𝒞 log n) ≥ (c_R/16)ρ_n^{BM}.

Thus the strict liminf threshold permits a fixed c>c₀, with the branch in PLAN G2 satisfying the eventual inequality. The sequence-dependent threshold n* is legitimate. C is the class constant at the selected c, so it may depend on the sequence through that choice of c; no uniformity over arbitrary liminf gaps is asserted. Intersecting the three design events gives exactly (2+2k_n)n⁻²+n⁻¹. Conditioning on that intersection gives the stated HPM bound with one copy of this failure probability. Since k_n=O(log n), both bounds are O(r_n).

**Q3. CorH-plus.** Yes for the displayed contraction statements and (KL). After R′(b), the unit-noise array satisfies exactly R1, G, (E), (F₀) and the selection premise of [POST2] D(a); D(a) imposes no (OS). The parameter-posterior scaling also transports the coefficient and variance events correctly. The KL identity has the correct direction of divergence and denominator v. Its quadratic bound holds on |v′/v−1|≤1/2. The slower auxiliary sequence in PLAN H1 proves K^a; taking the auxiliary variance threshold √log n proves K^b with coefficient 1+C_H/2.

Reading (i) is correctly restricted to the contrast law. The main assertion of reading (ii) is correctly restricted to conditioning on the whole candidate design with α measurable in that design. Its additional row-wise identification needs L1-1. The reference marginals remain comparison laws; they are not the marginals of Cy^r, whose variances are v(1−1/n).

**Q4. CorH-U.** Yes; the subsequence-with-fillers argument works. For n sufficiently large, p_f=max(s,2) orthogonal centred columns exist in 1^⊥, meet the size restrictions, have standardized Gram matrix (n−1)I, satisfy (E^σ;s), (F₀;1), (F_λ;1) and eventually (BM^σ;c) for any chosen fixed c. A0 gives n-free filler constants C_f and n_OS depending only on (s,A). Choose one fixed c>c₀ to obtain filler selection consistency from MIS-R (i).

For (U-b), pass to a fixed s slice and enlarge the energy and Occam constants to max(M,s) and max(C_OS,C_f). This does not change C_H: [POST2] D3 explicitly gives, at unit noise, C_H=8[C_A(s+j₀)+c₂]+1, depending only on (s,A). Failure with the barred thresholds implies failure with the corresponding unbarred thresholds on that slice. D(b) applied to the completed array gives the contradiction.

For (U-a), (UP) gives selection consistency on the selected subsequence for every fixed positive probability threshold; the fillers give it on the complement. D(a) then applies to the completed array. Its conclusion contains no constant that could change when the energy bound is enlarged. Arbitrary deterministic classes and empty classes cause no problem.

The (RD) statement is correct once the kernel implementation is written as in L1-4. BASE R′ (R3) and [POST2] D0 show that the entire parameter posterior, including the response-scale factor s_y=‖Uᵀy^r‖/√N, depends on y^r only through Uᵀy^r. All six bad-set indicators are jointly Borel on the finite-model strata. Freezing the bounded event indicator therefore gives the asserted conditional probability, and the supremum bounds it on 𝒜_n. The η″-family argument is valid for the (a)-type sets because their thresholds do not acquire constants depending on η″.

**Q5. Supersession and inputs.** The four rows of §8 recover the displayed contraction/selection conclusions they identify. Row 181 follows from nonsingular (E1). Row 182 uses the valid inequality λ_min(R_TT)≥c_pop/C₀ and the diverging beta-min branch. Row 183 uses MIS-R (i) and the inclusion 𝒦⁰⊆𝒦^F. Row 184 follows by singleton classes for (a′) and by the uniform bound on 𝒦⁰ for (b). Interpret row 183 as implication of BASE's displayed contraction conclusions; it does not validate an unrestricted row-wise narrative with a design-dependent intercept (L1-1).

As dependency declarations, §7 covers the mathematical inputs used in the four proof sketches. The conditional dependence on unchecked POST2 D, C and A0 is preserved; E and A1 are also carried in the quoted parent MIS(ii)/Cor-G(b) statuses. The relevant mathematical file/line citations agree with the reviewed sources. For code provenance of *candidate-column* standardization, [W3-POST STATEMENT.md:18](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-POST/STATEMENT.md:18)–22 is a more direct citation than BASE's response-code discussion at lines 79–81.

Scope of status verification: the POST2 unchecked status is visible in the supplied sources. The full final parent registry-status strings and the ACTIVE-on-origin/main labels are declarations in the frozen delta; I have not independently certified them against a registry snapshot, which is outside the brief's permitted file list. Parent lemma headers still say “unchecked” and separately record checks; that alone does not disprove a later registry promotion. Naming the classical Cramér theorem in §7 as well as PLAN would improve external-input provenance.

**Q6. Required changes before lock.** Apply L1-1–L1-4. No displayed contraction, uniformity, singular-covariance, necessity or finite-n bound needs weakening on the evidence reviewed. The core proof sketches can deliver the claims. In particular, no extra global moment assumption, global covariance invertibility, (OS) premise for (a′), or joint Gaussianity of candidate and omitted rows should be added. The only substantive overstatement found is the row-wise KL interpretation under the allowed design-dependent intercept.

LOCK-VERDICT: LOCK-WITH-AMENDMENTS
