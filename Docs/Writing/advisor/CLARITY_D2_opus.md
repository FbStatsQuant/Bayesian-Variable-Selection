# Clarity review, D2: "What we prove: consistency of the SMC-BVS method"

Reviewer: Opus 5.5, acting as a statistician new to the project. Draft reviewed: what_we_prove.pdf of 16 Nov 2026 (40 pp.).
I read only the PDF, the section .tex sources and smcbvs.sty.

**Scope note.** The brief said to skip "Appendix C (an internal status ledger)". In this PDF, **Appendix C is "Explicit constants"** (p. 36–37) and the status ledger is **Appendix D** (pp. 37–40). I reviewed Appendix C and skipped Appendix D, Table 1's Status column and footnotes, and all shaded Status boxes.

Page numbers are PDF pages. Locations name the section, theorem or remark.

---

## The 10 most important items

1. **The SMC sampler is never described, yet results depend on it.** §2.6 defines the start law, the local search, the reported model and the islands. It never says what the sampler does: particles, the "sequence of intermediate distributions" (from π₀ to π?), Markov moves, resampling, the "effort level", or what a *failed* calibration or a "fallback" is. Without this, the reader cannot understand the event 𝒜 ("the calibration succeeds", §5.5), Convention (C3), Remark 5.21 ("the sampler has almost no mass to move"), Remark 5.22, or §6 ("particles per island"). *Fix:* add a five-to-eight-line paragraph "The sampler" to §2.6 that defines these objects and says when calibration succeeds or fails.
2. **Theorem 5.17's hypothesis rests on an undefined object.** The noiseless gain γ(t | S) is defined as "the decrease of the method's ridge-regularised residual quadratic form". That form is never defined; the closest object is SS_S in (7). Several other conditions are used in stated results but never stated: the "superset Occam-sum condition" (Remark 3.5(iii), Remark 4.9(b), Open Q1), the "global-overlap condition" (Remark 5.21), the "directional floor" (after Thm 5.16), the "near-orthogonality floor" (Remark 5.18(iii)) and the "general form of the theorem" (§4.5). *Fix:* give γ as a formula (for example SS_S − SS_{S∪{t}} with y replaced by μ, if that is what it is). For each of the other conditions, either state it in one display or delete the claim that depends on it.
3. **Section 4 notation clashes.** §4.1 writes x_j for the j-th *coordinate* and x_i for the i-th *observation*, both as a single subscript on x. Remark 4.9 then uses the §2 objects (y as a vector, π(S₀ | y), R̂_{S₀}, μ, (GL)), although §4.1 says "the standardised data of Section 2.3 do not appear". *Fix:* write coordinates as x_{·j} or x^{(j)}, or write observations as (x^{(i)}, y^{(i)}). Move Remark 4.9 to §3, or open it with "In this remark we return to the notation of Section 2."
4. **The two notions of "no leakage" are different conditions.** §5.1 says "'No leakage' means Q = S₀". Assumption (NL), also titled "No leakage", is a different condition: it uses neighbourhoods H_l, the level C_L n^{-1/2}, and conditioning on U ∩ H_l. Assumption 5.6(a) with Q = S₀ is a third condition: level ϖ_n = o(√(log n/n)), conditioning on U. Example 5.5 depends on the difference ("violates (NL) … while Theorem 5.7 can [apply]"). The symbol r_n is also defined twice: with r_n(n log n)^{1/4} → 0 in (NL)(ii), and only with r_n → 0 in 5.6(a)(ii). *Fix:* rename (NL), for example "(NLS) no leakage for the start law". Say explicitly how it differs from Q = S₀ in Assumption 5.6. Use distinct symbols for the two locality rates.
5. **The dependence map in §1 is incomplete, and two of its dependencies are not explained.** Theorems 3.4, 3.18, 4.7, 5.2 and 5.12 appear nowhere in the map. "The main theorem rests on the random-design theorem": Theorem 3.9 assumes raw-scale signals (FSβ), while Theorem 5.7 (and 5.19) assume standardised-scale signals (FSθ). How can one rest on the other? "Theorem 4.6 rests on Theorem 3.1": Theorem 3.1 is a fixed-design theorem with (BC), (EF), (NC) and (BM) on θ*, whereas Theorem 4.6 is an i.i.d. sub-Gaussian-design result. The reader needs one sentence for each: "the proof applies Theorem 3.1 conditionally on the design, after showing that its sample conditions hold w.p. → 1 under …". *Fix:* give the full dependency list, ideally as a small DAG, with one clause per edge saying what is transferred.
6. **The units of θ\* conflict.** §2.3 says θ\* is "in the units of the raw response". §2.4 says θ_S is "on the standardised scale, like θ\*". These differ by the factor s_y, because the working model is fitted to y = P y^r / s_y. Every beta-min, visibility and leakage condition is stated in θ\*-units, so the reader needs to know which scale applies. *Fix:* in §2.4, write "θ_S is on the scale of the standardised response y; θ\*/s_y is its true counterpart". Also correct "the scale the method sees" in §5.1 (FSθ).
7. **Theorem 4.2 and Proposition 4.3(i): it is unclear what (i) adds.** Theorem 4.2 already holds for every M ≥ M₀ and every n ≥ n₀ with √n/log n ≥ M, and its constants do not depend on M. So "M may depend on n" seems already covered. The constant C₂ is introduced in Theorem 4.2 but used only in (20). *Fix:* move C₂ to Proposition 4.3. Say in one sentence what (i) adds (presumably (20), the common exceptional set and uniformity over laws). If "M may depend on n" is a real extension, say why Theorem 4.2 does not already give it.
8. **The overview and the in-words summaries drop conditions or say the wrong thing.**
   - §1: "the same holds for the list of models that a completed run returns (Corollary 4.7)". This holds only when the list carries posterior mass ≥ n^{-c⋆M/2}.
   - §1: "No design allows a rate faster than n^{-1/2}". This holds only when s₀ ≤ min(K−1, p/2) (Remark 3.14(i)).
   - §1: "two lower bounds … hold for every n". These need n ≥ 3, and n ≥ 4 with s₀ < K.
   - §5.2 in words: the start law's miss is "as small as the posterior's, up to a factor √log n". Both rates are √(log n/n). The factor √log n is relative to the n^{-1/2} lower bound, as the sentence after Theorem 5.2 says.

   *Fix:* restore the conditions, and rewrite the §5.2 sentence as "of the same order √(log n/n) as the posterior miss, which is optimal up to √log n".
9. **Three heuristic remarks have arithmetic that does not add up as written.**
   - Remark 3.7: p − s₀ models, each with odds of order n^{-1/2}/p, sum to order n^{-1/2}. So "together they can weigh as much as S₀ itself" needs the χ²₁ factor and moderate-n numbers to be made explicit.
   - Remark 5.9(i): "the prior-plus-Occam penalty (≈ log p + ½ log n) stops dominating the best of p noise gains (≈ log p)". As written, the penalty always exceeds the gain by ½ log n. The point is presumably that at size k ≈ √n the prior part becomes log{2p/(k+1)} ≈ log p − ½ log n.
   - Theorem 3.1 (11): Lemma 2.1 and Markov's inequality give 1 − 2C₁√(log n/n), not 1 − 4C₁√(log n/n), so a careful reader stops at "Consequently".

   *Fix:* write out each heuristic in one display. Explain the factor 4 or change it to 2.
10. **The labelling conventions and Appendix A contradict the text.**
    - §1 says single-use assumptions are numbered and multi-use ones are named. But Assumption 4.1 serves Thms 4.2 and 4.6, Prop 4.3 and Cor 4.7; Assumption 3.12 serves Thm 3.13 and Rem 3.15; and (FSβ) is named but used once. Appendix A even says "used by one theorem each: … 4.1 (Theorems 4.2 and 4.6)".
    - The symbol table writes W_K for w̄_K.
    - It lists q_n as the "size budget", which is k_n.
    - It places 𝒯 and Π̂ in §4.2; they are in §4.3.
    - It omits many symbols used in theorems: k_n, γ, Γ_n, τ_n, c⋆, C₂, M₀, G_n, φ_b, ϖ_n, r_n, b, b_H, N_l, ω_n, η, η_A, h̄_n and others.
    - Open question 7 cites Remark 5.13; the content is in Remark 5.14.

    *Fix:* align the rule with practice, or renumber. Then correct the table (details in §4 below).

Also high on the list: Remark 3.11 contradicts Remark 3.8 about Song and Liang's dimension (item 4.9 below). The delivery clauses of Theorem 5.7 do not say why (C2) gives only "produces output" and not P(Ŝ = S₀) → 1 (item 3.21 below).

---

## Category 1 — Sentences that needed a second read

| # | Location (p.) | Quote | Why it costs a second read | Proposed wording |
|---|---|---|---|---|
| 1.1 | Abstract (p.1) | "This section collects every consistency result we have…" | The document is introduced as a "section", although it has its own abstract, sections and appendices. | "This paper (or: This part of the paper) collects…" |
| 1.2 | §1, Section 5 paragraph (p.2) | "On the way, the method's start law already concentrates on the true model" | "On the way" to what? "Start law" is not yet defined. | "As an intermediate step, we show that the start law, the distribution from which the sampler starts (§2.6), already concentrates on the true model." |
| 1.3 | §1 "What asymptotic means" (p.2) | "two lower bounds (Theorem 3.13(a) and the floor in Theorem 5.2) hold for every n" | "Floor" elsewhere means an eigenvalue lower bound ((EF), (NC), "floor on the true model"). Here it means a lower bound on 1 − π₀(S₀). | "…and the lower bound 1 − π₀(S₀) ≥ (n+1)^{-1/2}/3 after Theorem 5.2) hold at every finite n (n ≥ 3, resp. n ≥ 4)." |
| 1.4 | §2 intro (p.4) | "a constant that appears in one assumption only is defined there" | "There" can mean that assumption or Appendix A. Appendix A is mentioned in the same sentence. | "…a constant that appears in only one assumption is defined in that assumption and is not listed in Appendix A." |
| 1.5 | §2.3 (p.5) | "We call θ\* the standardised coefficients; they are in the units of the raw response." | "Standardised" plus "raw units" sounds contradictory until one sees that only X is standardised in this display, not y. | "θ\* are the coefficients of the standardised predictors for the centred raw response, so they carry the units of y^r (the method's y is further divided by s_y)." |
| 1.6 | §2.6 Local search (p.8) | "the method runs two local searches: one from the best model found so far, and one from the start mode, with move cap ℓ_n + \|S̃₀\|" | Unclear whether the cap applies to both searches or only the second. The cap of the first search is never given. | "…one from the best model found so far (move cap ℓ_n) and one from the start mode (move cap ℓ_n + \|S̃₀\|), where…" |
| 1.7 | (C1) (p.8) | "a run that meets these conventions is admissible, and so is a sample size n for which valid inputs exist" | Two unrelated definitions of "admissible" (for runs and for n) are joined by "and so is". "Valid inputs" is undefined. | Make it two sentences: "A run that meets these conventions is called admissible. A sample size n is admissible if some data set of that size is a valid input (see Appendix B(iv))." |
| 1.8 | Remark 3.5(i) (p.11) | "when c₀ < C_β²φ₀² ≤ c₁, the two theorems coexist: Theorem 3.1 applies, and Theorem 3.4 is not shown to apply" | "Coexist" suggests both apply. | "…in that range only Theorem 3.1 is known to apply." |
| 1.9 | Remark 3.8 (p.12) | "selection consistency for the full model" | "Full model" usually means the model with all predictors. | "consistency of model selection itself (recovery of S₀), not only screening" |
| 1.10 | After Thm 3.13 (p.14) | "where c > 0 depends only on s₀, and does not depend on s₀ when s₀ ≤ p/2" | Reads as self-contradictory. | "where c > 0 depends on s₀ only through the factor 2(p−s₀)/(2p−1−s₀), which is at least 2/3 when s₀ ≤ p/2; so c can then be taken independent of s₀." (Adjust to the intended meaning.) |
| 1.11 | Remark 3.14(i) (p.14) | "(Without the size restriction, (a) is false: for example S = [p] with p = 2.)" | The reader must work out why. | "(The size restriction is needed: with p = 2, the full model S = {1,2} can carry posterior mass arbitrarily close to one.)" |
| 1.12 | Remark 3.15(i) (p.15) | "let all columns outside S₀ be null columns as in Assumption 3.12(b), or as in Assumption 3.12(c) with the columns in S₀ and the coefficients fixed (nonrandom)" | Hard to parse. "Keep the energy bounds of 3.12(a)" conflicts with 3.12(a)'s own "s₀ fixed". "Posterior mean error" is a new name for the expected posterior miss. | "Assume the energy bounds of Assumption 3.12(a), but let s₀ ≤ p/2 grow with n. Assume either 3.12(b), or 3.12(c) with X_{S₀} and θ\* nonrandom. Then E[1 − π(S₀ \| y)] = O(√(log n/n)) forces s₀ to stay bounded." |
| 1.13 | Example 3.19 (p.16) | "Then the full model is misspecified for the candidate-only fit" | "Full model" again. The sentence's subject is unclear. | "Then no candidate model contains the true regression function: the candidate-only fit is misspecified." |
| 1.14 | Example 3.19, last sentence (p.16) | "…a linear function of the candidates plus Gaussian noise whose rows are i.i.d. and independent of the candidates" | "Whose rows": the noise's rows? Also, Assumption 3.17(a) needs Gaussian candidates. Is that still required here? | "…plus a Gaussian noise matrix with i.i.d. rows independent of the candidates (the candidates themselves still Gaussian)." |
| 1.15 | Remark 3.20(ii) (p.16) | "it holds uniformly over any class of fixed-design configurations with common constants and bounded support size on which this convergence is uniform" | Circular on first reading ("uniform … on which … uniform"). | "If π(S₀^C \| y) → 1 uniformly over a class of fixed designs with common constants and bounded \|S₀^C\|, then the contraction is also uniform over that class." |
| 1.16 | §4.1 Constants (p.18) | "The reader fixes a level M ≥ 1: a larger M gives a larger ball and a smaller exceptional probability." | "The reader" fixes it? "Ball" is not yet defined. | "We fix a level M ≥ 1. The contraction radius is √(M log n/n) and the exceptional probability is n^{-c⋆M}, so a larger M gives a larger radius and a smaller exceptional probability." |
| 1.17 | Assumption 4.1, Rules out (d) (p.19) | "groups of O(log n) predictors that are collinear up to 1 − c_ψ/n" | "Collinear up to 1 − c_ψ/n" has no defined meaning. | "…groups of O(log n) predictors whose correlation matrix has smallest eigenvalue below c_ψ/n…" |
| 1.18 | §4.3 "What a completed run returns" (p.20) | "the best-scoring models among those offered to the final run of the sampler (the models scored in that run, together with models scored earlier and carried into it, …)" | "Offered to" is vague, and the parenthetical is long. | Split: "The list 𝒯 contains the best-scoring models among a pool. The pool is the models scored in the final sampler run plus those carried into it: the precomputed block tables and the models kept from calibration." |
| 1.19 | Remark 4.8(ii) (p.21) | "Theorem 4.2 and Corollary 4.7 concern the exact posterior and need no further input" | Corollary 4.7 concerns a run's output, so the reader stops at "exact posterior". | "Theorem 4.2 and Corollary 4.7 use no result from other sections (Corollary 4.7 concerns the exact posterior restricted to the returned list)." |
| 1.20 | §4.4 opening (p.21) | "For a fixed design, a weaker statement holds in the in-sample distance" | Weaker in what sense? Remark 4.9(a) gives the faster rate M_n/√n. | "For a fixed design, Theorem 4.2 does not apply. Remark 4.9 gives contraction in an in-sample distance instead." |
| 1.21 | §5.3 (pp.25–26) | "The limits are a base move cap of 10⁶ and a 32-bit integer bound 2³¹ − 1 on the move cap…" | 10⁶ is not a move cap. It is a ceiling on the base move cap ℓ_n (Appendix B). | "The limits are a ceiling of 10⁶ on the base move cap ℓ_n and the 32-bit bound 2³¹ − 1 on the move cap ℓ_n + \|S̃₀\|." |
| 1.22 | Remark 5.10 (p.27) | "with p ≫ n and no design family" | Unclear. | "…with p ≫ n and without assuming a particular correlation structure for the design." |
| 1.23 | Assumption 5.11, Rules out (c) (p.27) | "explain more than a fraction η of log n residual-variance units" | Hard to parse. | "…whose signal gain exceeds η τ_U² log n." |
| 1.24 | Before Thm 5.17 (p.29) | "For a predictor t ∉ S and a model S, define the noiseless gain γ(t \| S) of a predictor t ∉ S given a model S:" | Says the same thing twice. | "For a model S and t ∉ S, the noiseless gain γ(t \| S) is …" (then a formula; see 2.31). |
| 1.25 | After Thm 5.16 (p.29) | "The argument needs only a weaker, directional floor, which leaves correlations among null predictors free; the full floor in Assumption 5.15(a) does constrain them." | Undefined term. The point (5.15(a) is stronger than needed) only becomes clear on a second read. | "The proof uses (a) only along directions that involve a true predictor. That weaker condition, unlike (a), puts no constraint on correlations among null predictors." |
| 1.26 | §5.5 (p.30) | "Let 𝒜 be the event that the method uses the sampler and its calibration succeeds (fallbacks included)" | "Fallbacks included" is unexplained. Does a fallback count as success? | Define success and fallback in §2.6 (item 1). Here say "…succeeds, possibly after a fallback (§2.6)". |
| 1.27 | Remark 5.21 (p.31) | "An alternative argument, with no condition on Ẑ, gives the same conclusions…" | A "condition on Ẑ" is an odd phrase, since Ẑ is an estimator. | "An alternative argument, which does not go through the evidence estimate Ẑ, gives…" |
| 1.28 | Open question 1 (p.32) | "Find a sufficient condition … that involves no design quantity. Whether that condition holds without any eigenvalue condition is open." | The second "that condition" could mean the Occam-sum condition or the sought sufficient one. | "Whether the superset Occam-sum condition can hold with no eigenvalue condition on the design is open; a sufficient condition free of design quantities would settle it." |
| 1.29 | Appendix B, end of (C2) (p.36) | "Plain (i) does not give delivery for every n." | "Plain (i)" means (C2)(i) without lifting the limits? | "Under (C2) as stated, with the integer limits in place, delivery is guaranteed only on 𝔇." |

---

## Category 2 — Symbols and terms used before their definition, or never defined

| # | First use (p.) | Symbol / term | Defined at | Proposed fix |
|---|---|---|---|---|
| 2.1 | §1 (p.1) | "beta-min condition" | (BM), §3.1 (p.10) | Gloss on first use: "(a lower bound on the smallest true coefficient)". |
| 2.2 | §1 (p.1) | "the Hellinger distance of Song and Liang (2015)" | §4.1, (18) (p.18). Song and Liang is never introduced as the main comparator. | Add one sentence early in §1: "We compare throughout with Song and Liang (2015), the closest prior work: …" |
| 2.3 | §1 (p.2) | "block by block", "start law", "certified", "calibration", "completed run", "islands" | §2.6 (pp.7–8) | Add a pointer, "(these terms are defined in §2.6)", or a one-line gloss for each. |
| 2.4 | Table 1 (p.3) | Rate "almost n^{-1/2}" (Thms 5.2, 5.19) | Never defined. ρ_n appears only in §5.5. | Write "n^{-1/2}e^{C√log n}" or "n^{-c}, every c < ½". |
| 2.5 | Table 2 (p.4) | "SAMC" | Never expanded. Remark 5.10 cites Liang et al. (2007) but does not expand it. | "stochastic approximation Monte Carlo (SAMC)". |
| 2.6 | §2.6 (p.7) | "sequence of intermediate distributions", "effort level", "computing allocation" | Never defined. Allocation is described only in App. B. | See top item 1. |
| 2.7 | §2.6 (p.7) | "valid seed", "valid inputs", "default configuration" (also in (C1)) | The seed range appears only in App. B(iv) (p.36). "Valid inputs" and "default configuration" are never defined. | Define in §2.6 or in (C1). |
| 2.8 | (C2+) (p.8) | "the code's two fixed integer limits on the local-search move caps" | §5.3 (p.25), App. B (p.36) | Forward-reference §5.3, or state the limits here. |
| 2.9 | (C3) (p.8) | "every Markov move" | Never introduced. App. B(iv) speaks of "Markov moves" and "stated kernels". | Introduce the sampler's moves in §2.6 (item 1). |
| 2.10 | Remark 3.5(iii) (p.11); also Rem 4.9(b), Open Q1 | "superset Occam-sum condition" | Never stated ("stated in full with the proof"). | State it in a display here. It is a hypothesis of Remark 4.9(b). |
| 2.11 | Remark 3.5(iii) display (p.12) | Range of T; status of c_D | Not said whether T ranges over subsets of [p] \ S₀, or whether c_D is fixed. | "for a fixed c_D > 0 and every T ⊆ [p] \ S₀ with …" |
| 2.12 | Remark 3.8 (p.12) | P_n, α, C in e^{Cn^α}; "their condition (10)" | Song and Liang's notation, undefined here | "(their number of predictors P_n)". See also 4.10. |
| 2.13 | Assumption 3.17(a) (p.15) | x_C (the candidate design matrix), α₀ | Never defined. Only the rows x_{C,i} are defined. | "x_C = (x_{C,1},…,x_{C,n})^⊤; α₀ ∈ ℝ an intercept". |
| 2.14 | Assumption 3.17(b) (p.15) | R_{TT} | Not defined. Elsewhere sub-matrices are Σ_{n,S}. | Write R_T, and add R_T to §2.1 notation. |
| 2.15 | Assumption 3.17(c) (p.15) | M_C | Not declared fixed. | "for a fixed M_C < ∞". |
| 2.16 | Remark 3.20(ii) (p.16) | "in-sample average Hellinger and Kullback–Leibler distances" | Hellinger only, in Remark 4.9 (p.21) as h̄_n. KL is never defined. | Define both here, or forward-reference Remark 4.9 and add the KL version. |
| 2.17 | Remark 3.22 (p.17) | s̃ ("Song–Liang's s̃"); ε ("for each fixed ε") | Not defined. ε is the noise vector in §2. | Define, or drop s̃. Use another letter for the Hellinger radius. |
| 2.18 | §4.1 Constants (p.18) | Whether s is fixed | Never said. A, L, c_ψ and b̄ are declared fixed; s is not, but constants depend on it and §4.5 Weaker(3) says "s is fixed". | "s ≥ 0 is a fixed upper bound on…" |
| 2.19 | §4.1 (p.18) | "ball" | Implicit in (19). | See 1.16. |
| 2.20 | Theorem 4.2 (p.19) | C₂ | Introduced in Thm 4.2 but used only in (20) of Prop 4.3. | Move it to Prop 4.3. |
| 2.21 | §4.3 (p.20) | "40p + 1" | Unexplained magic number | One clause on where it comes from, or "a list of at most O(p) models (40p+1 in the code)". |
| 2.22 | Remark 4.9(b) (p.21) | C′_H | Prime with no unprimed C_H. Dependence not stated. | "for a constant C_H depending only on …" |
| 2.23 | §4.5 (p.22) | r_n, r̄_n, P_n, ξ, k (in log^{k/2} n), α, θ (in n^θ), "coefficient cost", "≻" | Song and Liang's symbols, undefined. "≻" is not in §2.7, which defines only ≫. "Coefficient cost" is undefined. | Add one line, "Symbols r_n, r̄_n, P_n, ξ, α, θ, k are Song and Liang's", and use ≫. Define or drop "coefficient cost". |
| 2.24 | (V) (p.24) | a | Clashes with p = n^a (Remark 3.14) and with a₀. Minor. | Rename, for example a_V. |
| 2.25 | Theorem 5.2 (p.24) | "valid data set" | Never defined. | See 2.7. |
| 2.26 | Remark 5.4(ii) (p.25) | "reference sets" | Never defined. | "…the size bound on H_l enters only through a union bound over the sets H_l". |
| 2.27 | Assumption 5.6(a) (p.26) | "32s₀" in K ≥ 2\|Q\| + 32s₀ + 1 | Unexplained | One clause on its role, for example "so that the start mode and the search fit within the cap K". |
| 2.28 | Assumption 5.11(d2) (p.27) | h | Not declared fixed. | "for a fixed h ≥ 0". |
| 2.29 | Remark 5.8(iii) (p.26) | α (correlation decay exponent) | Clashes with the intercept α. | Use another letter. |
| 2.30 | Remark 5.18(iii) (p.29) | "near-orthogonality floor" | Never defined | Define it or drop the sentence. |
| 2.31 | Before Thm 5.17 (p.29) | "the method's ridge-regularised residual quadratic form" (hence γ(t \| S), Γ_n) | Never defined | Give the formula; see top item 2. |
| 2.32 | §5.5 (p.30) | "calibration succeeds", "fallbacks", "interrupted"; C₃ ("a suitable constant") | Never defined. C₃ is fixed only by the proof. | Define in §2.6. For C₃: "for a constant C₃ depending only on (…)". |
| 2.33 | Remark 5.21 (p.31) | "global-overlap condition" | Never stated | State it, or drop the remark. |
| 2.34 | §6 (p.31) | "serial engine", "parallel engine", "particles", "spread" of log-evidence estimates | Never defined. Also unclear which n and which statistic (SD? range?) are meant. | Define them, and give the statistic and n. |
| 2.35 | Open Q2 (p.32) | "ridge cost of the true model" | Never defined | Define it or point to a formula. |
| 2.36 | Appendix A (p.34) | Missing from the symbol table: k_n, γ(t \| S), Γ_n, τ_n, G_n, c⋆, C₂, M₀, C_q, L, c_ψ, b̄, ψ, b_n, φ_b, κ_H, C_L, r_n, ϖ_n, b, b_H, N_l, d_n, L_n, ω_n, η, η_A, δ_Q, h, j₀, M_μ, M_θ, h̄_n, M_C, c_C, α₀, ℓ (block) etc. | — | §2 says single-assumption constants are defined in place, but k_n, γ, Γ_n, τ_n, G_n, c⋆, C₂, M₀ and h̄_n are used in theorems and remarks. At least those belong in the table. |
| 2.37 | Appendix B (pp.35–36) | "production core", "tie-aware start-mode fallback", "grid fallback", "preflight bounds", "local-search archive", "stream-identifier", "start-mode enumeration cap", "calibration record", "calibration value" | Never defined | Define each in one phrase, or replace with neutral descriptions. |
| 2.38 | Appendix C (p.37) | C\* in c₀(s₀, A) = max{4C\*, …} | "a constant of the proof"; value not given (internal bracket note) | Give C\*. Until then, Remark 3.5(i)'s "c₀ is explicit" is not true (see 4.31). |

---

## Category 3 — Steps, scope or role I could not work out

| # | Location (p.) | What I could not follow | What is missing |
|---|---|---|---|
| 3.1 | §1 "How the results depend on each other" (p.2) | Incomplete map. Unexplained edges 5.7 ← 3.9 (FSθ vs FSβ) and 4.6 ← 3.1 (fixed vs i.i.d. design). | See top item 5. |
| 3.2 | §1 / Table 1 (pp.2–3) | Remark 5.22 is listed as a result, but its hypotheses are not stated. Appendix A says it uses (C3); the remark does not say so. | Make it a Proposition with hypotheses ((C3), on 𝒜), or state them in the remark. |
| 3.3 | §2.6 (p.7) | How the sampler works, and when calibration fails | See top item 1. |
| 3.4 | Theorem 3.1, (11) (p.10) | Why 1 − 4C₁√(log n/n) | Lemma 2.1 and Markov give 2C₁. Explain the 4 or correct it. |
| 3.5 | Theorem 3.1 (p.10) | "every design and θ\* that satisfy these assumptions at that n" | (SP) "s₀ fixed" and (BM)(b), which is a limit, are not properties of a single n. Say which hypotheses are read at each n (for example "(BM)(a) holds at that n") and which along the sequence. |
| 3.6 | Remark 3.2(iii) (p.11) | "this uses a bound on the coefficients instead" | Which bound: (BC)? the energy bound? |
| 3.7 | Remark 3.7 (p.12) | Odds n^{-1/2}/p summed over p models give n^{-1/2}, yet "together they can weigh as much as S₀" | Show how the χ²₁ factor (or moderate n) changes this, with one illustrative number. |
| 3.8 | §3.3 In words (p.13) | "So the rate of Theorem 3.1 cannot be improved under its assumptions" | This needs the witness designs to satisfy Theorem 3.1's assumptions. Remark 3.14(iii) shows this for orthogonal designs only. For the Gaussian null designs (Assumption 3.12(c)), θ\* is random through D, which Theorem 3.1 does not allow. Say which witness family supports the claim. |
| 3.9 | Remark 3.14(iii), Remark 3.15 (p.14) | "(conditional on Theorem 3.1)", "(conditional on Theorems 3.1 and 3.9)" | Internal status language in reader text. A reader takes Theorem 3.1 as proved, so "conditional on" has no meaning. Delete it, or say "using Theorem 3.1". |
| 3.10 | Remark 3.20(iii) (p.16) | "A fixed-design version of the theorem, uniform over the residual variance, also holds." | Not stated. Either state its hypotheses and conclusion, or remove the sentence. |
| 3.11 | Remark 3.20(ii) (p.16) | The contraction "needs only that the posterior mass of S₀^C tends to one … (with the energy bound and a floor on S₀^C)" | Which energy bound (3.17(c)?) and which floor (constant?) |
| 3.12 | Proposition 4.3(i) vs Theorem 4.2 (p.19) | What (i) adds | See top item 7. |
| 3.13 | Theorem 4.6 (p.20) | Why M = 1 in "window q_n of M = 1", when M₀ may exceed 1 | Explain, or write "of M = M₀". |
| 3.14 | Theorem 4.6 / Remark 4.8(ii) (pp.20–21) | How Theorem 3.1 (fixed design, standardised θ\*, (BC), (EF), (NC), (BM)) is used under Assumptions 4.1 and 4.5 | One sentence: "Assumptions 4.1(d)–(e) and 4.5 imply (NC), (BC), (EF) and (BM)(b) for the sample w.p. → 1 (Lemma …), so Theorem 3.1 applies conditionally on the design." |
| 3.15 | Corollary 4.7, second sentence (p.21) | Whether "the model the method reports as most probable" is Ŝ, and why the list must contain the true model | Write Ŝ. Add: "because a model with posterior mass > ½ has the highest score among all scored models". |
| 3.16 | §4.5 Stronger (2), Not the analogue (p.22) | "in the general form of the theorem, where the in-sample signal energy and coefficient cost are bounded by fixed constants" | The general form is not stated, and "coefficient cost" is undefined. A comparison cannot rest on an unstated theorem. State it, or drop the parenthetical. |
| 3.17 | §5.1 "Signals fixed on the standardised scale" (p.24) | (FSθ) restates a model and replaces (GL) for Thms 5.2, 5.7 and 5.19. This is not said. | "(FSθ) replaces (GL) and (SP) in these theorems." |
| 3.18 | Remark 5.3 (p.25) | Which other hypotheses apply? Is (V) still needed? Where exactly is S₀ replaced in (NL)? (It appears several times.) | "Under the other hypotheses of Theorem 5.2, if (NL) holds with S₀ replaced by Q in H_l ⊇ {l} ∪ Q and in j ∈ Q \ U₀, then …" |
| 3.19 | Remark 5.4(i) (p.25) | "The level is sharp in the fixed-design analogue for every p." | Which level? (V) has only a fixed a > 0. Which fixed-design analogue? Assumption 5.11(b)? |
| 3.20 | Remark 5.4(ii) (p.25) | "localisation is needed because the blocks depend on the data" | One more clause on the mechanism would help, for example: data-dependent blocks prevent a union bound over all 15-sets. |
| 3.21 | Theorem 5.7, delivery clauses (p.26) | Why (C2) yields only "produces output with probability one", while (C2+) also gives P(Ŝ = S₀) → 1. Why "probability one" rather than "always", if delivery holds for every data set. What "admissible n" means. | Add: "𝔇 is bounded, so no limit statement can be made under (C2); (C2+) removes the bound. In practice 𝔇 contains every feasible (n, p_raw)." Say what the probability is over (the data? the seed is fixed). |
| 3.22 | Assumption 5.6(a) (p.26) | Role of "(Q = [p] or K ≥ 2\|Q\| + 32s₀ + 1)" | See 2.27. |
| 3.23 | Remark 5.9(i) (p.27) | The penalty heuristic | See top item 9. |
| 3.24 | Theorem 5.12 (p.27) | Why "no raw predictor constant in the sample" is assumed | Presumably so that p = p_raw and 𝔇 is in terms of p. Say so. |
| 3.25 | Remark 5.13(ii) (p.28) | "Theorem 5.7 shows that population analogues imply them with probability tending to one" | Theorem 5.7's statement does not show this; its proof does. "The proof of Theorem 5.7 shows…", plus a pointer. |
| 3.26 | Theorem 5.16 (p.28) | Whether s₀ must be fixed. (SP) is not assumed. | Say "s₀ may vary with n subject to (c)", or add (SP). |
| 3.27 | Numerics after Rem 5.18 (p.29) | "2,394 of 2,394 in the 2,400-fit study" | What happened to the other 6 fits (not completed?). Say so. |
| 3.28 | Theorem 5.19 (p.30) | Theorem 5.2 needs Assumption 5.1; Theorem 5.19 does not list it. | Note that (EFΣ) implies Assumption 5.1 for large n. |
| 3.29 | Remark 5.20(ii) (p.30) | "The rate ρ_n is the start law's rate" | Theorem 5.2 does not state ρ_n; it appears only in Remark 5.3 as (\|Q\|+1)n^{-1/2}e^{C√log n}. Point there. Also ρ_n/√(log n/n) = e^{C₃√log n}/√log n, not e^{C₃√log n}. |
| 3.30 | §6 title and opening (p.31) | What "the parallel method" is | The method already runs four islands. Is the "parallel method" the same method with islands run concurrently, a different engine, or the many-island variant? The abstract asks "what carries over to the parallel version", so define it once in §2.6 or at the start of §6. |
| 3.31 | Open Q9 (p.32) | "Certified screening with signals that vary with n under a sparse eigenvalue floor" | Theorem 5.17 already allows signals that vary with n. Say what is missing (a margin stated through a sparse floor and beta-min rather than through Γ_n?). |
| 3.32 | Appendix C (p.37) | c₀ is called explicit, but C\* is unspecified | See 2.38. |

---

## Category 4 — Inconsistencies

| # | Location (p.) | Inconsistency | Proposed fix |
|---|---|---|---|
| 4.1 | §1 "How to read a result" vs §§3–5 and App. A (pp.2, 35) | The naming rule (named = used by ≥ 2 theorems) is broken by 4.1, 3.12 and (FSβ). App. A says "used by one theorem each: … 4.1 (Theorems 4.2 and 4.6)". | Restate the rule as "used across sections / used within one subsection", or rename. |
| 4.2 | §1 (p.2), (NC) (p.10), Rem 3.6, 4.4, App A | "Floor" means an eigenvalue lower bound ((EF), (NC) "vanishing floor", "floor on the true model", "small-set floor") and also the start-law lower bound "the floor in Theorem 5.2". | Use "floor" only for eigenvalue bounds. |
| 4.3 | §2.1 (p.4) | "A star marks a true parameter value", but c⋆ (§4), P\* (§4.1) and C\* (App C) are not parameter values. | Different decorations for constants, or drop the convention. |
| 4.4 | §2.2 (p.4) vs §5.3 (p.25) | "The raw count p_raw appears only in Section 4 and in the computing conventions", yet 𝔇 and Thm 5.7 use p_raw. | "…in Section 4, in the delivery domain 𝔇 and in the conventions." |
| 4.5 | §2.2 (p.5), (GR) (p.12), App A, §3.4 (p.15) | Σ_n is a general covariance in §2.2, a correlation matrix in (GR), "population correlation matrix" in App A; Σ is a covariance in §3.4. | In §2.2, say "covariance Σ_n (a correlation matrix under (GR))". |
| 4.6 | §2.2, §3.4, §5.1 | Sub-matrix notation: Σ_{n,S} (principal), Σ_{n,UU}, Σ_{n,Ul}, R_{TT} | Define Σ_{n,AB} once in §2.1 and use it throughout. |
| 4.7 | §2.3 vs §2.4 (p.5) | Units of θ\* versus θ_S | See top item 6. |
| 4.8 | §2.6 (p.8), §5.3 (p.25), App. B (p.36) | ℓ_n uses p; 𝔇 uses p_raw. 10⁶ is called "a base move cap" in §5.3 but "a fixed ceiling" on the base cap in App. B. The text says the first limit binds "when n + p + 1 exceeds 2^{10⁶}", using p again. | Use one of p, p_raw throughout (they agree only when no predictor is constant). Use "ceiling on ℓ_n" everywhere. |
| 4.9 | Remark 3.8 vs Remark 3.11 (p.12) | 3.8: Song and Liang allow P_n < e^{Cn^α}. 3.11: "This is the random-design setting of Song and Liang; here p ≫ n is allowed", which implies they do not allow it. | "…as in Song and Liang, p ≫ n is allowed (polynomially here, sub-exponentially there)." |
| 4.10 | Rem 3.8 (p.12), §4.5 (p.22) | "their condition (10)", "their display (15)", "(16)", "their constant c₁" collide with our displays (10), (15), (16) and our c₁(s₀, A). | Prefix theirs, for example "SL(10)" and "SL-c₁". |
| 4.11 | (NC) (p.10), App A | (NC) is titled "No near-exact collinearity" in the text and "vanishing floor" in App A and Remarks 3.6 and 4.9. | Keep both, but put "(the vanishing floor)" in the assumption title. |
| 4.12 | §2.6 (p.7) vs §2.2 | S̃₀ (start mode) looks like S₀ (true model), and the subscript 0 invites a false link. | Use, for example, S_start or Ŝ₀. |
| 4.13 | (C2) (p.8), App. B | "Used only by the clauses 'the run always produces output'". No theorem contains this phrase; theorems say "the run produces output with probability one". | Quote the actual clause. |
| 4.14 | Remark 3.15(i) (p.15) | "posterior mean error" is a third name for the posterior miss, after "posterior miss" and "posterior mass outside the true model". | Use "expected posterior miss". |
| 4.15 | §3.4 (p.15) vs §4.1 (p.18) | s = \|S₀^C\| (exact support size) in §3.4; s = an upper bound on the count in §4. | Use s_C in §3.4. |
| 4.16 | Assumption 3.17 vs Example 3.19 (pp.15–16) | β^C (best linear predictor) and β_C (true coefficients on candidates) differ only in super- versus subscript. | Rename β_C as β\*_C, or β^C as b^C. |
| 4.17 | Thm 3.18 (p.16) | m (mean of the candidate row) collides with m(S) (marginal likelihood). | Use μ_C or m_C. |
| 4.18 | Remark 3.22 (p.17) | "Song–Liang" vs "Song and Liang" elsewhere. "Σ, β, σ²" vs β^C, σ_C² in Thm 3.18. | Harmonise. |
| 4.19 | §4.1 (p.18) | x_j = coordinate and x_i = observation, both single subscripts | See top item 3. |
| 4.20 | §4.1 (p.18) | H²(P, Q) and d_H²(f, g) are two notations for the same quantity. | Keep one, or say they coincide. |
| 4.21 | §4.3 (p.20) | "the logarithm of its unnormalised posterior weight", which is the log score F(S) of §2.5 | Say "its log score F(S)". |
| 4.22 | Remark 4.4 (p.20) | Items numbered (o), (i), (ii), (iii) | Renumber from (i). |
| 4.23 | Remark 4.4(ii) (p.20) | "the prior's penalty for each extra predictor (a factor of order n^{-1/2})". §2.5 calls n^{-1/2} the Occam factor of the marginal likelihood; the prior penalty is (k+1)/(2p−1−k). | "…keeps in force the Occam factor (order n^{-1/2}) for each extra predictor". |
| 4.24 | Remark 4.9 (p.21) | Uses §2 notation inside §4 | See top item 3. |
| 4.25 | Corollary 4.7 (p.21) | "{j : β\*_j ≠ 0}" and "the model the method reports as most probable" instead of S₀ and Ŝ | Use S₀ and Ŝ. |
| 4.26 | §5.1 vs (NL) vs Assumption 5.6(a) (pp.23–26) | Three "no leakage" notions; r_n defined twice | See top item 4. |
| 4.27 | §5.1 (p.23) vs §3.4 (p.15) | "Residual variance" means τ_U² in §5.1 and σ_C² in §3.4. | Call τ_U² the "residual scale" or "noise-plus-unexplained variance". |
| 4.28 | §5.2 in words (p.24) vs text after Thm 5.2 | "as small as the posterior's, up to a factor √log n" vs "(23) is optimal up to the factor √log n" | See top item 8. |
| 4.29 | Assumption 5.11 (p.27) | δ_Q (a constant) vs δ²_{U,l} (signal gain) | Rename δ_Q. |
| 4.30 | Remark 5.22 (p.31) vs App. A | App. A lists (C3) as used by Rem 5.22; the remark does not state it. | State (C3) in the remark. |
| 4.31 | Remark 3.5(i) (p.11) vs App. C (p.37) | "c₀ and c₁ are explicit", but c₀ contains an unspecified proof constant C\*. | Give C\*, or say "c₀ is explicit up to a proof constant C\*". |
| 4.32 | Open question 7 (p.32) | Cites Remark 5.13; the content is in Remark 5.14 (What is not claimed). | Point to Remark 5.14. |
| 4.33 | Appendix A (p.34) | Symbol table errors: "w(k), W_K" should be w̄_K; "q_n, κ, θ, M₁, c_SB: size budget…" should be k_n (q_n is the §4 window); "𝒯, Π̂ … §4.2" should be §4.3; δ, τ, β̂, Cov, Q, ℒ(Q) are listed as "§5" but are in §5.1; π(S \| y), F(S), Z are listed as "§2.5, §2.6" but all are in §2.5. | Correct the entries. |
| 4.34 | §5.5 (p.30) vs §2.8 | 𝒜 (calligraphic, the event) vs A (dimension exponent). They are distinct in print, but both are read aloud as "A", and they sit next to each other in App. A. | Consider 𝓔_cal or G_cal for the event. |
| 4.35 | Brief vs document | The brief calls Appendix C the status ledger; in the PDF it is Appendix D (C is Explicit constants). | Update the brief, or the appendix lettering after the ledger is removed. |
