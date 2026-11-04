<!-- Filed by the chair: verbatim final message of PC1 (gpt-6.1-sol, Codex), session ~/.codex/sessions/2026/11/03/rollout-2026-11-03T21-30-48-01a1a49b-f777-7a73-aa31-33f69570e86c.jsonl. -->

# CHK_INHERITED — Proof checker 1

Cross-family review by gpt-6.1-sol (Codex), following `CHECK_INHERITED_BRIEF.md`. `git fetch origin` completed. No registry status was changed; no commit or push was made. All review artifacts are under this evidence directory.

The requested proof lines were checked in the prescribed order. Locked inputs were checked for statement and hypothesis compatibility; their proofs were not independently re-reviewed. Author-only concentration inputs were replaced, where needed below, by an explicit orthogonal calculation. These are checker verdicts, not adoption decisions.

| Item | Verdict | Qualification |
|---|---|---|
| OWS-WS6(d) | VERIFIED WITH AMENDMENT | The lower bound and divergence argument check. For the accompanying TV conclusion, make the bounded-block setting explicit, or separately assume start concentration. The shipped block cap supplies this setting. |
| OWS-WS7 | VERIFIED WITH AMENDMENT | Clarify initial versus subsequent particle presence; qualify the restricted-set stage-count approximation and its degenerate endpoint. The ESS/KL/TV obstruction is unchanged. |
| OWS-WS3 | VERIFIED | VERIFIED (PC1, cross-family, line by line). |
| OWS-WS4 | VERIFIED | VERIFIED (PC1, cross-family, line by line). |
| N9-KERNEL §§0–3 | VERIFIED WITH AMENDMENT | The elementary kernels, random round, normaliser and start sampler check under the stated idealisations. Correct the prose treating sufficient order conditions as necessary, and make stationarity explicit in REPORT's RB consequence. |

## Sources and reproducibility

| Source | Pinned revision |
|---|---|
| O-WSTAB PROOF.md | `2ec30992adb12335e3cef3b0d9a88ca71c282d63` |
| N9-KERNEL PROOF.md, REPORT.md, CHECK.md | `c20059db8513f27772787347bab059c83cc78908` |
| Registry index | `b1600857783b5a4dd90e74849f3af4b24199d24b` |
| METHOD_v3.1_FINAL.md and AMENDMENT_HQ_01.md | `f70b0f5c9ade8eadf091c63280ad3c21d4a3530f` |
| Production C++ code | `39db138170e7bde0f3ebedef8b38fd76d1444ae3` |
| Other dependency snapshots | Exact revisions and paths in `scripts/sources/MANIFEST.tsv`. |

`python3 theory_campaign/MEET-THM/evidence/CHK_INHERITED/scripts/check_math.py` reproduces the independent mathematical checks. `scripts/run_n9_checks.sh` reproduces the C++ checks against extracted, unchanged production headers. Raw numerical outputs are in `scripts/`. All runs were local, used fixed seeds, and finished within five minutes each. Ten Python seeds and two C++ design seeds were used.

## 1. OWS-WS6(d): noise-chasing obstruction

| Field | Finding |
|---|---|
| Verdict | VERIFIED WITH AMENDMENT. The displayed single-null lower bound is correct. The full statement's TV conclusion needs an explicit bounded-block concentration scope; the proof's cited concentration results do not establish unrestricted growing-block scope. |
| Model/design hypotheses | G: fixed centered, standardised design and Gaussian noise with fixed positive variance. ORTH. Fixed nonempty truth and fixed nonzero coefficients. The specified score, positive inverse-gamma hyperparameters, capped BB(1,p) prior and state space are essential. |
| Partition and growth | Partition fixed in X, independent of response noise. Truth-free null count m tends to infinity; log m=O(log n). For divergence: m≥p/2 and the displayed growth condition. ORTH forces p≤n−1. Feasibility of every S₀+l holds eventually. |
| Additional TV scope | Use blocks of size at most a fixed B, in particular the shipped B≤16. Alternatively assume π₀(S₀)→1 explicitly. That alternative is a distributional conclusion used as a premise, not a model/design condition. |
| Non-model idealisations | EX-A: exact scores, tables, sums and probabilities. No algorithmic RNG hypothesis is needed for the divergence itself. Interpreting χ² as iid importance-sampling variance uses exact iid π₀ draws. |
| Exact scope | Asymptotic mathematical start and target laws under ORTH. No H-ORTH restriction p log p=o(n) is used. No ideal-grid or production-grid result is proved here. |
| Numerical sanity | Ten seeds, n=65,536, p=n−1, two separated truths, population R²=0.8. Exact single-null log odds obeyed the proof's logarithmic lower bound. Maximum uniform expansion error across nulls and seeds was 0.148. No full-space χ² was numerically enumerated. |

| Proof step | Check |
|---|---|
| §§0–2 and WS6(a–c) | Fit-fraction identity, finite exponential-family identities, Cauchy–Schwarz/Kantorovich bounds, integral representations, iid ESS/variance formulas and tilt bounds check. These are mathematical identities, with the stated iid/frozen-calibration assumptions where relevant. |
| Orthogonal score | H_S=n²I and G_S+I=nI, hence D_S=n to the power size(S), and t_S=Σ z_j²/n. |
| Start odds | Adding a truth-free null changes one empty block table. Prior ratio is exactly (s₀+1)/(2p−s₀−1), and its table factor is n⁻¹ᐟ²(1−b_l)⁻ν. |
| Discrepancy increment | Determinants cancel. The increment is ν[log(1−b_l)−log(1−a_l)], with a_l=t_l/(Q̄−t_S₀), b_l=t_l/Q̄ and a_l≥b_l. |
| Logarithmic inequalities | −log(1−a)≥a and −log(1−b)≤b/(1−b) give the displayed lower bound with the correct signs for α>1. |
| Gaussian coordinates | Before dividing by s_y, null projections are independent standard normals. A partition fixed in X makes the truth-free index set deterministic. Standardisation creates common denominator errors, not new independence. |
| Uniform approximation | s_y²(Q̄−t_S₀)=RSS_S₀+O_P(1), RSS_S₀/σ² is χ² with n−1−s₀ degrees of freedom, and s_y²=‖θ*‖²+σ²+O_P(n⁻¹ᐟ²). Multiplying common O_P(n⁻¹ᐟ²) coefficient errors by the Gaussian maximum gives o_P(1). |
| Extreme value and sum | max Z_l²=2 log m−log log m+O_P(1). Keeping only its model in the nonnegative odds sum proves the stated lower bound. The random exponential multiplier is two-sided tight. |
| Divergence | The singleton Rényi identity gives exp((α−1)D_α)≥π(S₀)^α/q_α(S₀). Posterior concentration and the deterministic diverging rate then give divergence in probability. |
| Concentration dependencies | T03 requires H-T02. The locked register explicitly closes it with T02(i) under G,R. ORTH and fixed coefficients imply R, SE and BM-∞. There is no remaining open tail hypothesis in this application. |
| TV conclusion | Bounded-block ORTH supplies start concentration as shown immediately below; posterior concentration then gives TV≤max(1−π(S₀),1−π₀(S₀))→0. |

The minimal scope amendment is: **“For the TV conclusion, assume the method's bounded-block setting, or separately assume π₀(S₀)→1.”** The single-null lower bound and divergence conclusion do not require this extra block-size restriction. This review does not assert the unrestricted growing-block TV statement is false; its cited proof does not cover that scope.

For completeness, start concentration in the shipped setting does not require upgrading the candidate general EXP′ result. Write A_T=‖P_TY‖² on the unstandardised centered scale. Under ORTH,

    s_y²(Q̄−t_T) = RSS_T + A_T/n + 0.02 s_y².

Uniformly over within-block T, A_T/n=O_P(1), s_y²=O_P(1), and RSS_T is bounded below by a positive constant times n with probability tending to one. For the last claim, each fixed T has bounded rank; Gaussian projection tails and a union bound over at most 2^16 p sets suffice. Replacing both exact score denominators by RSS therefore changes an addition log ratio by O_P(1), uniformly. Also log n−log(n+1)=O(1/n). This proves the strict EXP′ needed by locked T22(iii). ORTH gives NL₀ and visibility gain at least (n−1) times the smallest squared true coefficient. All T22(iii) premises hold, giving

    1−π₀(S₀) = O_P(2^B √(log n/n)) → 0.

## 2. OWS-WS7: masked-regime weights

| Field | Finding |
|---|---|
| Verdict | VERIFIED WITH AMENDMENT. Parts (a),(b), the support obstruction in (c), and the halving inequality in (d) check. Three wording/domain corrections are listed below. |
| Finite-law hypotheses | Finite Ω, strictly positive γ₀, finite discrepancy, exact exponential bridge, S₀∈Ω. Set-form ESS bounds require nonempty A; for A=∅ use the trivial bound rather than 0/0. No Gaussian or orthogonality assumption is used in these identities. |
| Masking hypotheses | Fixed c≥1; π₀(S₀)=p⁻ᶜn⁻ᶜᐟ² exp(O_P(1)); π(S₀)→1. These are assumed mass conclusions, not model/design conditions. To invoke T27(i), retain its feasible completion chain, joint two-sided ratio law and normalised reference-mass hypothesis H3. |
| Other hypotheses | For (c): exact iid initial π₀ particles and operations that only reweight/resample. For (d): fixed V containing S₀, exact restricted ESS, and every interval accepted at the stated level. None supplies coverage of the full state space. |
| Scope | Finite deterministic identities; conditional asymptotic consequences under masking. No ORTH/H-ORTH requirement. No unconditional masked-design theorem and no production-grid stage upper bound. Standard final-run count is 4N_e; optional stacking changes this to R′N_e. |
| Numerical sanity | Arbitrary positive finite bridges over ten fixed seeds satisfied the singleton, ESS, KL and halving checks. The separate resampling example below gives exact probabilities 3/4 initially and 5/8 after resampling. |

| Step | Check and required qualification |
|---|---|
| (a) | Cauchy–Schwarz gives ESS∞≤π₀(A)/π(A)². Binary KL data processing gives KL≥π(S₀)log(1/π₀(S₀))−log 2. The TV set bound is immediate. |
| (b) | Substitution yields the stated ESS, KL and TV limits. CL(L)+H3 is a sufficient route only with the expansion/design premises of the cited W1-EXP theorem; those are not proved by WS7. |
| (c): amendment | State the equality for the initial population, or for ever containing S₀ including initialisation. At a later specified stage, only “≤1−(1−π₀(S₀))^N≤Nπ₀(S₀)” is guaranteed. Resampling can lose existing truth particles. |
| (d): recurrence | Singleton identity and q_w^V(S₀)≤1 give 2ℓ_t≥ℓ_{t−1}−c_ρ. Iteration proves the displayed necessary lower bound whenever its denominator is positive. |
| (d): set-mass amendment | The last comparison with c log p+(c/2)log n additionally needs log π₀(V)=o_P(c log p+(c/2)log n); π₀(V) bounded below suffices. Without this, V={S₀} has ℓ₀=0 despite masking. |
| (d): endpoint amendment | If ρ̄=1 and V={S₀}, both logarithmic numerator and denominator vanish. Treat this trivial singleton case separately. For ρ̄<1 the displayed ratio has a positive denominator. |
| Two-state attainment | With small truth odds o, r=√(0.1/o) gives next odds √(0.1o) and inverse ESS≤1.1(1+o)≤10/9 for o≤0.01. This establishes the early log-log scale in an example; it is not a universal grid upper bound. |

The particle-presence correction has a reproducible elementary witness in `scripts/check_math.py`: take N=2, π₀(S₀)=1/2 and one multinomial resampling with equal weights. Initial presence is 3/4. Subsequent presence is 1/4+(1/2)(3/4)=5/8. The proposition's support-based upper bound survives unchanged.

## 3. OWS-WS3: block orthogonality

| Field | Finding |
|---|---|
| Verdict | VERIFIED (PC1, cross-family, line by line). |
| Hypotheses | Centered, standardised nonzero response; specified Gaussian working-model score and positive inverse-gamma hyperparameters; finite capped state space and positive common prior; tables use the same full response and score. BO for the chosen partition. Part (f) also uses μ=X_S₀θ*. |
| Non-model hypotheses | EX-A is a numerical idealisation. The known-precision comparison requires tables recomputed under that known precision; it is a different working model. No data-noise distribution or posterior-concentration premise is used. |
| Scope | Finite deterministic result for BO, including correlated columns within blocks and even singular within-block Gram matrices. No ORTH, H-ORTH, p-growth or block-size restriction is needed. No grid is involved. |
| Numerical sanity | Ten seeds, 64 models per seed, three two-variable blocks with nonzero within-block correlations. Determinants, fitted quadratic forms, Gamma-MGF representation and discrepancy bounds agreed within 7.11×10⁻¹⁵. |

| Part | Line-by-line check |
|---|---|
| (a) | The three relevant matrices are block diagonal after permutation. Their determinants and quadratic forms separate; the fit fraction remains below one by positive regularisation. |
| (b) | Subtracting the block log scores cancels determinants and leaves exactly the stated shared-variance discrepancy. |
| (c) | Successive logarithmic increments equal log(1+s x/(1−s−x)). Positivity, the pairwise upper bound, equality condition and coordinate derivatives all follow on the stated domain. |
| (d) | Gamma shape ν and rate Q̄/2 give the required MGF for every total fitted sum below Q̄. This is the null posterior in the specified working model; its n/2 exponent is intentional despite centering. |
| (e) | The identical size prior and cap cancel from the target/start density ratio. The prior still couples block selections; it contributes no discrepancy term. |
| (f) | The residual direction is in the block span and orthogonal to all out-of-block signal under BO. No out-of-block leakage remains. |

## 4. OWS-WS4: standardised cross-block perturbations

| Field | Finding |
|---|---|
| Verdict | VERIFIED (PC1, cross-family, line by line). |
| Hypotheses | Same exact score, state space, full-response tables and partition as WS3. For each tested model: positive definite block-diagonal A_S and ε_S<1. For the fit/decomposition bounds additionally x̄_S<1−ε_S. Small within-block eigenvalues require the explicitly stated scaling. |
| Transfer hypotheses | Nonempty finite W where all preceding conditions hold; η_W is their maximum. Both bridges use the same γ₀ and the same conditioning set W. The comparison bridge uses d_σ computed from the given data; no separately constructed BO data set is assumed. |
| Non-model hypotheses | EX-A. An independently chosen restriction W is an analytical device, not a property of the sampler. No coverage hypothesis is supplied for W⊊Ω. |
| Scope | Finite deterministic result on genuinely correlated designs. Neither ORTH nor H-ORTH is required. Applies to every real tilt v. A restricted comparison does not become global without additional mass/coverage control. |
| Numerical sanity | Ten seeds and all 64 models, cross-block operator norm 0.1 on the full design. Checked eigenvalue, fit, determinant, discrepancy, χ²-transfer and TV bounds, including restricted W and v=−1, 0.5, 1, 2. Largest positive floating-point violation was 7.78×10⁻¹⁶. |

| Part | Line-by-line check |
|---|---|
| Definitions/(a) | Operator-norm control gives the Loewner sandwich by congruence. Interlacing justifies the optional within-block eigenvalue sufficient condition. |
| (b) | c₁=(n+1)(n−1), H_d=c₁A+I. The conjugated perturbation has norm at most ε; inverse eigenvalue deviations lie in [−ε/(1+ε), ε/(1−ε)]. Multiplication by n gives the claimed fit bound. |
| (c) | Both conjugated perturbations have zero trace. The scalar log bounds give a nonpositive log determinant bounded below by minus its squared Frobenius norm divided by 2(1−ε). Taking a difference gives the stated constant 1/4. |
| Frobenius lemma | The displayed difference is the sum of tr((Y−X)EYE) and tr(EXE(Y−X)). Both are nonnegative because EYE and EXE are positive semidefinite. The proof does not assume commutativity. |
| (d) | h=(x_S−x̄)/(1−x̄); its bound is below one exactly when x̄<1−ε. The positive and negative h cases give the same safe bound with denominator 1−ε−x̄. |
| (e) | Log normalisers differ by at most absolute tilt times η_W. The second difference gives 4 absolute tilt times η_W. The likelihood-ratio lower bound gives the displayed TV estimate. |

For fixed positive explained fraction, this particular η bound tends to zero only if ε=o(1/n). This is a limitation of the uniform perturbation bound; it is not a necessity theorem for actual weight stability, and it does not cover generic sample cross-correlations of order n⁻¹ᐟ².

## 5. N9-KERNEL: production-code audit

| Field | Finding |
|---|---|
| Verdict | VERIFIED WITH AMENDMENT. Claims G, U, N, I, R, Z and S check against code at the named commit. Required prose corrections are below. No kernel or sampler implementation change is indicated. |
| State/target hypotheses | Valid finite input, feasible sorted models, positive finite scores; fixed blocks forming a partition; tables and capped size prior shared by evaluation and sampling. All steps use the same fixed φ. Neighbour graph is symmetric, loop-free and duplicate-free. |
| Non-model idealisations | H-U: fresh independent continuous uniforms; H-A: exact arithmetic; H-D: deterministic score of sorted S. H-U and H-A are idealisations. H-D was checked in scorer buffer use, deterministic route selection, table scoring and collision-resolving cache lookup. |
| Fixed setup/order | Blocks, tables, graph, B and K are fixed before the step; order is state-independent and reversal-invariant. The code uses fixed label counts and Fisher–Yates. Successful evaluation is assumed; a numerical failure aborts execution rather than supplying a transition. |
| Scope | Finite kernel/start identities for arbitrary valid designs, without Gaussian data assumptions, ORTH, H-ORTH or growth conditions. No adaptive temperature-selection theorem. The φ grid may be frozen arbitrarily; reversibility is for each supplied φ. |
| Coded RNG/arithmetic | Exact claims do not hold literally for the 53-bit generator and rounded categoricals. Under ideal independent grid uniforms, acceptance is ceil(α2⁵³)/2⁵³. The actual pseudorandom stream's independence is not proved. Small-design rounding checks are not production-size error guarantees. |
| v3.1 applicability | The audited engine, start, score and block headers have no differences between `39db138` and the pinned MEET-v31 revision. METHOD and HQ-01 retain these laws. Reporting/LS0 additions do not establish stationarity of a finite terminal run. |
| Numerical sanity | Inherited harness recompiled against unchanged pinned headers: n=20,p=6,K=6 and n=8,p=6,K=4; φ=0,1/2,1. Exact extracted kernels and complete state enumeration exercised unequal degrees, empty/full models and the binding size cap. |

| Claim/code | Line-by-line check |
|---|---|
| Target, engine:89–101 | lg0=logprior+composite and d=log BF−composite give γ_φ=ϖ BF^φ(∏r_b)^(1−φ). The proof correctly identifies the extra-prior-factor typo in the task's alternative formula. |
| G, engine:113–132 | Both feasible configurations use the same heat-bath conditional. A forbidden addition at K has inclusion probability zero. A deletion remains feasible. RB is recorded before the draw and does not affect the transition. |
| U, engine:134–159 | The nonmember selector is a bijection. A swap has a unique removed/added pair and symmetric probability 1/(k(p−k)). Size-zero/full states self-loop. |
| N, engine:162–180 | Available degrees are counted on S and S′ respectively. Symmetry ensures the reverse candidate exists. The coded forward/backward degree factor is exactly the Hastings correction. Graph symmetrisation and deduplication are explicit in blocks:170–171. |
| I, engine:182–192 | With exact π₀ proposals, γ₀ cancels and leaves exp(φ(d′−d)). Z̄₀ cancels from this move; its exactness is separately needed for evidence normalisation. |
| R, engine:195–214 | Fisher–Yates yields uniform labelled permutations under H-U. Adjoint reversal of each kernel product and reindexing by reversed permutations establish self-adjointness of the averaged round. Repeated neighbour labels cause no problem. |
| Z, start:101–149 | Block size profiles and nonnegative convolutions enumerate all feasible products. Truncation at K cannot affect any coefficient through K. The size prior is multiplied once. |
| S, start:158–176 | Backward conditional probabilities telescope to ∏e_b(k_b)/F_J(k); within-size draws cancel these factors. Empty blocks contribute one. Early stopping at remaining size zero matches deterministic zero sizes. Thus the full probability is γ₀(S)/Z̄₀. |
| Scorer/cache | Scratch entries read by scoring are assigned first. Counters do not enter scores. Sorted-set keys are compared after hash matches; collisions and cache clearing do not change the score function. |

Required amendments:

| Location | Minimal correction |
|---|---|
| PROOF §2, “exact condition” and “It fails if…” | Call these sufficient conditions. Replace “fails” with “is not guaranteed” when discussing state-dependent or non-reversal-invariant orders. Commuting kernels, for example, can remain reversible under a fixed order. |
| REPORT, fixed-order claim | Replace “A fixed order is not self-adjoint” by “A fixed order need not be self-adjoint.” CHECK already records the counterexample: at φ=0, the final independence step refreshes exactly from π₀, making the canonical product reversible. |
| REPORT §3, RB consequence | State that the round starts in q_φ when asserting q_φ-distributed pre-Gibbs states and E[o_j]=q_φ(j∈S). Invariance alone does not make finite terminal particles exactly stationary or plain normalised RB estimates unbiased. PROOF §2 already states the needed stationary-start qualification correctly. |

| Re-run quantity | Result |
|---|---|
| Production/spec log score | Maximum discrepancy 9.78×10⁻¹⁵. |
| Target/spec log bridge | Maximum discrepancy up to a constant 1.19×10⁻¹⁴. |
| Start normaliser | Versus direct enumeration: absolute log error ≤4.77×10⁻¹⁶. |
| Enumerated start law | Maximum relative error ≤6.47×10⁻¹⁴; TV≤2.86×10⁻¹⁶. One leaf per feasible model; no duplicate or zero-mass leaves. |
| Elementary detailed balance | Maximum relative flow error ≤3.04×10⁻¹³. |
| Averaged-round detailed balance | Maximum relative flow error ≤1.55×10⁻¹⁴. |
| Negative controls | Removing neighbour Hastings correction gives relative flow error up to 0.75; treating independence proposals as symmetric gives error approximately 1. These checks detect substantive mistakes. |
| Order enumeration | Every choice vector gives a distinct permutation for m=4 through 8; reversal closure holds. Grid-level uniform-index relative deviation through k=64 is ≤6.03×10⁻¹⁵. |
| Monte Carlo replay | Short AR(1) checks included two small approximate p-values (0.002 and 0.006). A targeted 50,000-round replay gave nine p-values from 0.101 to 0.828; its start-sampler p-value was 0.476. Raw short and longer outputs are retained; deterministic kernel extraction is the primary check. |

These numerical results support the idealised algebra; they do not certify exact detailed balance of the literal finite-precision pseudorandom implementation.

## 6. Does the pair refute one-shot proposal §5.3 for the shipped method?

**Yes, for the mathematical laws of the shipped start and target, with the explicit scope and wording amendments above.** “Weight variance” here means variance of the normalised importance weight g=π/π₀, equivalently the squared coefficient of variation of the unnormalised weights:

    Var_π₀(g) = χ²(π‖π₀),    ESS∞ = 1/(1+χ²(π‖π₀)).

| Route | Exact failure hypotheses and implication |
|---|---|
| Zero-dependence obstruction | G, ORTH, fixed nonempty truth and nonzero coefficients, exact shipped score/prior/start. Truth-free null count m≥p/2 and p^((α−1)r)/(√n (log p)^((1+(α−1)r)/2))→∞. Then D_α→∞. For α=2, weight variance diverges despite exactly zero cross-block correlations. |
| Explicit shipped example | Centered X with XᵀX=(n−1)I, p=n−1; one true coefficient 2, noise variance 1, hence r=4/5. The shipped B≤16 gives m≥p−16. χ² has a lower bound of order n^(3/10)/(log n)^(9/10) times a two-sided tight positive multiplier and π(S₀)²→1. |
| TV in that example | The same model has π₀(S₀)→1 and π(S₀)→1, hence TV→0. Concentration of both endpoints therefore does not bound the second moment of importance weights. |
| Polynomial dimensions | For p=n^(a+o(1)), the strict sufficient divergence condition is a(α−1)r>1/2. ORTH permits a≤1; p=n−1 realises the upper boundary. The lower bound makes no converse claim below or at the threshold. |
| Masking obstruction | If the T27(i) mass conclusion holds for fixed c≥1 and π(S₀)→1, then 1+χ²≥π(S₀)²/π₀(S₀), ESS∞ vanishes, KL diverges and TV→1. H3 and the joint ratio law remain essential non-design premises until established on a concrete family. |
| Limits of the conclusion | WS7 alone does not exhibit a weakly dependent masked family. WS6(d) already refutes a general one-shot weak-dependence guarantee at zero dependence. Neither result proves failure of the actual multistage sampler, nor failure of a bridge-form §5.3 theorem. |

The one-shot refutation survives this check in the shipped bounded-block setting. WS6(e)'s converse threshold remains a conjecture; production-grid transfer and later-stage particle/evidence variance control are not supplied by this review.