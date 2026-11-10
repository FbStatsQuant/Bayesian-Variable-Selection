DO-NOT-LOCK

# R05 — independent v3 delta proof check and statement re-lock

The central new inequalities survive independent derivation. The unrepaired v3 statement nevertheless contains false or inadequately qualified consequences (M6, the L5 interpretation, and a coded-flag assertion in SCR-G). These are local repairs; I found no counterexample to SCR-M, EC′, the directional bridges, or the screening conclusions of SCR-G. Re-lock should follow the repairs below, rather than certify the present text unchanged.

Scope: STATEMENT v3; every line of L7 and rewritten L5; the specified L2/L3/L4/L6 edits; L1 as an algebraic dependency; CC6 against the actual C++ and R export/assembly paths; PROGRAM item 5. I read the disposition and R04's counterexample as context, but independently re-derived the inequalities below. No subagents, Git commands, Python, simulations, or edits outside this report were used. Source locations below give a file and an exact quotation, supplemented with code line numbers where useful. Paths starting `lemmas/` are relative to `Theory_work/Wave3/W3-SCR/`.

## Item verdicts

| Item | Verdict |
|---|---|
| CC6 | CORRECT-WITH-MINOR-FIX |
| SCR-M theorem | CORRECT |
| M1 | CORRECT |
| M2 | CORRECT-WITH-MINOR-FIX |
| M3 | CORRECT |
| M4 | CORRECT-WITH-MINOR-FIX |
| M5 | CORRECT |
| M6 | WRONG (STATEMENT summary); L7 example CORRECT |
| SCR-G | WRONG (top-level flag assertion); screening conclusions correct after minor proof clarification |
| L5 facts | CORRECT |
| L5.1 | CORRECT |
| L5 reading | WRONG |
| L5.2 | CORRECT |
| SCR-C still valid | CORRECT |
| SCR-R | CORRECT |
| B2d | CORRECT |
| A1/A1° edits | CORRECT |
| L6 edits | CORRECT-WITH-MINOR-FIX |
| L2 edits | CORRECT |

## Numbered findings and verification record

1. **MAJOR — The statement's M6 drops essential signal/growth conditions.**

   Location: `STATEMENT.md`, SCR-M (M6): “when the residualised true columns do not depend on S, M1 holds up to size K−1 with no entropy term.”

   Geometry alone does not make the deterministic gaps positive. Take S₀={1}, p=2, x₁ orthogonal to x₂, fixed σ=1, and θ*₁=1/n. For the entire family of models of size ≤K−1=1 missing truth 1, R_S x₁=x₁, and the witness directions coincide. But γ(1|S)=(n−1)²(n+1)/n⁴~1/n. For fixed x>0 the positive noise threshold b_H(x) is bounded below away from zero, so G_S=0 eventually and δ_S=−B_S<0. In fact SCR-N with x_n=√log n gives P(∅ LO)→1 in this example. Thus there really are small LO models missing truth despite the stated geometric condition.

   L7 M6 does not have this defect: its example explicitly assumes θ*₁≠0 and σ fixed and log p=o(n). The summary must retain those conditions (and specify fixed x, or an appropriate growth condition on x). Alternatively say only that a low-dimensional witness span reduces b_H and that M1 applies **when the resulting gaps are positive**. Do not state automatic screening from geometry.

2. **MAJOR — A capped search does not force the top-level `local_certified` flag to be FALSE.**

   Location: `STATEMENT.md`, SCR-G(ii): “in particular Ŝ ⊇ S₀ when Ŝ = N, although `local_certified` is FALSE”. Compare `Scripts/SMC_BVS/core/v3_run.R:179-197`, especially `out$local_certified <- cert_final || cert_ls0`.

   The capped search's own archive has `local_certified=FALSE`. The other search can have certified exactly N. For example, the final search can certify N and LS0 can stop one scan before reaching that same N, returning it on its cap. Conversely, LS0 can certify a model returned by a capped final search. The top-level flag then is TRUE when N remains the reported HPM. The code explicitly permits `local_limit=TRUE` together with `local_certified=TRUE`; CODE_CHECK already explains this distinction.

   Fix: “even if the top-level `local_certified` is FALSE (the capped search itself is uncertified).” The containment conclusion remains valid either way. Identify a capped archive by its own `termination == "move_limit"` or its own `local_limit`; the aggregate flag alone does not identify which search capped.

3. **MAJOR — The new L5 interpretation overstates what EC′ says.**

   Locations: `lemmas/L5_exact.md`, Reading: “a single excess variable ... is possible only if its conditional length is small” and “larger excess sets need a large ω, i.e. strongly dependent dual directions”; `STATEMENT.md`, excess-set paragraph: “a single excess variable (ω = 1) is possible only if it is nearly collinear with S₀ (α small).”

   The displayed inequality in Reading (ii) IS exactly EC′ at m=1, ω=1. Its verbal interpretation is not a theorem without additional quantitative assumptions. Write A=(1−η_n)(1−1.02/n), L=2log((2p−k)/k), c=(n²−1)/n, and let R denote the RHS of EC′ with ω=1. Only when A>0 does it imply α≤exp(R/A−L)/c; this upper bound need not be small. If A=0, it imposes no condition on α at all. The hypotheses allow this: taking x large makes the inner positive part in the definition of 1−η vanish. Likewise, increasing x′ or the normalized coefficient bias makes the RHS large.

   For any m, the actual restriction is ω≥A(Λ_k(α))_+/R_m. This lower bound can be ≤1, including zero. Therefore EC′ does not generally require large ω for larger sets. For example, take mutually orthogonal columns (ω=1 and α=1+λ₀/(n−1)), with q large enough to include the chosen strict superset, and choose x so that A=0. Every excess set then satisfies EC′ with ω=1 regardless of size. Even aside from this vacuous-event example, α, the entropy term, and the bias all enter the necessary lower bound for ω.

   This is not a universal impossibility of orthogonal LO supersets: at fixed n with enough columns/capacity, sufficiently large noise coefficients in orthogonal excess directions can make such a superset LO on an open set of responses, hence with positive Gaussian probability. The non-asymptotic claim cannot exclude those responses by saying α must be small.

   Fix: keep the exact m=1 inequality, replace its interpretation by “gives an explicit upper bound on α when the prefactor is positive,” and replace (iii) by the quantitative lower bound for ω above. Explain any “small α” or “large ω” conclusion only after imposing conditions making those numerical bounds nontrivial. The deterministic-family statement and Reading (i) are correct.

4. **MINOR — M4 silently uses κ≤1, which need not hold for the new directional floor.**

   Location: `lemmas/L7_master.md`, M4: “u* ≤ 1/26 since κ ≤ 1, b ≤ M ≤ τ_*”.

   Neither A1 nor B2d assumes κ≤1. Unlike an anchored minimum eigenvalue, the directional Rayleigh quotient can exceed 1. For example, q=0, two identical true columns with equal positive coefficients give φ^d_n(0)=2. Choosing κ=2 is legal. This does not invalidate M4's constant, but the printed justification is false.

   Repair without weakening the result: since ∅ belongs to the minimization family, with V=‖θ*‖₂² and L=‖θ*‖₁,

       κ ≤ φ^d_n(q) ≤ ‖Xθ*‖²/((n−1)V) ≤ L²/V ≤ L/b ≤ M/b,

   where V≥bL follows from every nonzero coefficient having magnitude ≥b. Thus κb≤M and u*=κ²b²/(26τ_*²)≤1/26 as needed. Alternatively restrict the lower-bound constant to κ∧1 everywhere. B2d, A1, and A1° themselves do not require κ≤1.

5. **MINOR — Make the strict gap needed by SCR-G explicit.**

   Locations: `lemmas/L7_master.md`, M4: “δ_H ≥ c₂ n”; `STATEMENT.md`, SCR-G(i)-(ii): “`hpm_F` − F(C) ≤ c₂n”; M2 requires “F(Ŝ) − F(C) < δ_C”.

   The displayed weak bound alone does not imply the strict comparison in M2. The proof actually yields a stronger bound: uniformly in S,

       δ_S ≥ n u*/2 − B_S = n u*/2 − o(n) > n u*/4 = c₂ n

   for all sufficiently large n, with infinite δ handled trivially. State this strict version of M4, or explicitly use it when deriving SCR-G. No change to c₂ or the `≤ c₂n` application threshold is necessary.

6. **MINOR — δ_C is undefined on the very models M2 concludes are present.**

   Locations: `lemmas/L7_master.md`, Setting: “For S ∈ H⁻ ... δ_S”; M2: “Every scanned centre C ∈ H with ... < δ_C ... contains S₀”; same issue in `STATEMENT.md` M2 and its “δ_S > 0 for all S” shorthand in M3.

   δ is currently defined only for missing-truth models. Consequently the M2 predicate is not a predicate on all C∈H. Define δ_C=+∞ for C⊇S₀, or formulate the result as: “Every missing-truth scanned centre C∈H⁻ has F(Ŝ)−F(C)≥δ_C; in particular every centre in H within δ_H of the HPM contains S₀.” Restrict M3's “all S” to H⁻. If H⁻ is empty, explicitly set δ_H=+∞ and regard b_H,c_H and the theorem inequalities as unused/vacuous; L7 already says the empty case is vacuous, whereas STATEMENT leaves log M at M=0 unexplained.

7. **MINOR — The excess-set statement is not self-contained about its parameters.**

   Location: `STATEMENT.md`, EC′: “(1 − η_n) ... √(2 log C(p−s₀, m)/m + 2x′)”.

   Set m=|E|, quantify x,x′>0, and identify η_n as η_n(k,x) from L5.1. It is not among the quantities defined in §1, and its dependence on k is relevant to a uniform statement over supersets. Either reproduce the L5 definition (with U(k,x)) or explicitly refer to that precise definition. The probability stated here is the L5.1 noise-event probability; to conclude that **all certified models** have this excess-set representation, also intersect with a screening event as the Reading paragraph does. The displayed EC′ assertion for LO **strict supersets** itself needs no screening event and is correct.

8. **MINOR — Archives for both searches exist only when LS0 is enabled; “unscanned” must be scoped to that search.**

   Locations: `CODE_CHECK.md`, CC6: “Each archive prints its scanned centres”; `STATEMENT.md` §0: “fit$local_search or fit$ls0”; `CODE_CHECK.md`, local search step 3: “a model whose own neighbourhood was not scanned”.

   The fields are indeed exported for both archives when LS0 runs: `v3_core.cpp:350-357` exports `scanned_centres`, `scanned_F`, `scan_complete`, and `scan_size`; final and LS0 calls both use this serializer. R preserves these lists at `v3_run.R:128-139`. But `v3_fit.R:73` permits `ls0=FALSE`, and `v3_core.cpp` exports `ls0` only inside `if (o.ls0)`. Thus answer (3) is yes for the default enabled-LS0 completed run, not for every supported completed run. Say “each search that was run” / “LS0, when enabled.” There is no mathematical problem with quantifying over the searches that exist.

   The capped return's own neighbourhood was not scanned **as a centre of this invocation**. Strictly increasing centre scores prove it cannot equal an earlier centre of that invocation. Its neighbourhood could already have been scanned in the other search or calibration. It was of course scored as a neighbour in the cap-ending scan. Scope the wording accordingly; M5 does not rely on any global never-scanned claim.

9. **MINOR — L6's new parenthetical exact ratio omits the c_θ correction.**

   Location: `lemmas/L6_sharp.md`, Consequence 2: “Δ(√Δ − c_θ)²/(n‖θ*‖₁²) ... asymptotically equal to Γ_n(0) (ratio (n+1)/n → 1)”.

   The ratio (n+1)/n is the ratio to Δ²/(n‖θ*‖₁²), not to the printed full B1 bound. On this sequence,

       c_θ/√Δ = √(n/(n²−1)),
       Γ_n(0) / [Δ(√Δ−c_θ)²/(n‖θ*‖₁²)]
         = ((n+1)/n) / (1−√(n/(n²−1)))² → 1.

   Replace the parenthetical by this expression or simply “ratio →1”. The corrected rate (log n)²/n, the screening counterexample, and the scaling argument are valid.

10. **MINOR — The added generic same-truth neighbour-rate sentence is unsupported as stated.**

    Location: `STATEMENT.md`, final parenthesis of SCR-G: “score differences between neighbouring models that fit the same truths are of order log(p ∨ n).”

    No quantifier, probability qualification, or meaning of “fit” is specified, and no lemma proves this rate uniformly over the adaptive scanned models under the design-agnostic hypotheses. Even a probabilistic upper-bound interpretation must account for the number and geometry of residual directions selected through conditioning models; a fixed-model Gaussian tail is not a uniform proof over all size-q_n centres. A literal deterministic upper bound is also unavailable from the supplied results. This sentence is not used by SCR-G. Delete it, or state and prove the intended probabilistic rate with its quantifiers and conditions. The order-n lower bound on the missing-truth gap is established and can stand alone.

11. **NOTE — CC6's ledger inequality survives cache hits, clears, inheritance, and the nonemitting initial-centre evaluation.**

    Locations: `Scripts/SMC_BVS/core/cpp/v3_engine.h:85-101`, especially `if (emit)` and `fresh || !cache`; `v3_ledger.h:84-112`, `if (is_fresh) offer_stores(...)`; `v3_core.cpp:395-481`; `v3_score.h`, `ScoreCache::find/insert`.

    Answer (1): yes, under EX-A on completed runs, for every neighbour of every fully scanned centre of either executed search. Every `consider` calls `eval` with emission enabled. A miss computes a deterministic score, inserts it, and emits `is_fresh=true`; `offer_stores` offers it to the monotonically improving HPM. A hit need not re-offer because the model was already offered. Clearing the cache clears only cache slots/pool/count, not the ledger; a later miss re-offers the same score harmlessly. `find` checks hash **and** the actual sorted model, so collisions do not create a false hit.

    The final run constructs a NEW empty `ScoreCache` and ledger together. Calibration's cache is not carried into it. Inherited models are freshly rescored and directly offered to this ledger before the final islands/searches, even though this does not populate the cache. Table models likewise enter through `ingest_tables`. Any calibration-only model that is later scanned and was not inherited must be freshly evaluated on this run before a hit is possible.

    The one important nuance missing from the short CC6 justification is the initial `eval(C,...,false)` of the final search: it can insert into the cache without emitting. This is safe because C is exactly `led.hpmS`, already offered before the call. LS0 emits its initial centre. Thus all cached models needed for this argument were previously offered to the final ledger, although not every cache insertion itself emits a fresh event. Adding this sentence would make the audit justification complete.

    Answer (2): yes. `best` is the maximum-F feasible neighbour (lexicographic tie rule); the cap branch is inside `best.F > C.F`, and assigns `returned=best.S`. `A.scanned`, `A.scanned_F`, and `scan_complete=1` are appended for C before checking the cap. The return need not be the global HPM; other previously scored models can be better.

    Answer (4): no successful path records a partially completed scan as complete. The append occurs only after the entire flip loop and nested swap loops. A thrown numerical failure before the append aborts that invocation; the run is not completed. Runtime checks are after whole searches, and can change status to resource_limit, not turn a partial scan into a completed one. Skipping additions at |C|=K is the defined neighbourhood, not an incomplete scan. These facts suffice for M2/M5 without a certificate.

12. **NOTE — SCR-M, checked line by line: the probability and deterministic gap are correct.**

    Location: `lemmas/L7_master.md`, Setting and entire SCR-M proof, from “Family and witnesses” through “|S| < K gives S∪t ∈ N(S)”.

    * Family and witnesses depend only on deterministic inputs, so Gaussian directions are fixed. M counts missing-truth models only, which is the correct union size. For M≥1 all square roots and widths are defined. R_S preserves centredness; R_S²≼R_S gives ‖R_Sx_t‖²/a≤1 and ‖R_Sμ‖²/(μᵀR_Sμ)≤1. Since R_S is positive definite, m_S=0 actually implies μ=0; the e_S=0 convention is consistent.
    * Width is nonnegative because 0 is included. The finite-cardinality bound follows from the exponential-moment bound for M+1 unit-variance-or-smaller Gaussian linear forms. Projection to their span and Jensen give w≤E‖Πg‖≤√r. The maximum over D∪{0} is 1-Lipschitz (Lipschitz constant at most 1 suffices). Concentration therefore gives w+√(2x) with failure e^{-x}.
    * Taking the minimum costs no extra e^{-x}: of the two DETERMINISTIC thresholds choose the smaller one in advance, and use its individual tail bound. This is not a union bound on two random estimates. The one-sided union bound uses e^{-x}/M. The same reasoning applies to c_H. Adding the two E2+ failures gives exactly 4e^{-x}. Omitting E4 when only the crude denominator branch is used gives 3e^{-x}.
    * The minus sign in d_S is essential and correct: s_S x_tᵀR_S y_c/√a=√γ−d_Sᵀε. When √γ−σb≥0 this controls the squared gain; when negative, the positive part sets G=0. Squaring a negative lower bound is never used.
    * The denominator expansion is exact before bounding: [0.02+(n−1)/(n+1)]τ̂²+n y_cᵀR_Sy_c/(n+1). Its first coefficient is ≤1.02. The cross term is 2m_Se_Sᵀε, including m_S=0; noise contraction supplies the E2+ chi-square bound. Both U_S and (n−0.98)τ̄² are upper bounds simultaneously on the chosen event; taking their minimum is legitimate. σ>0 ensures the deterministic denominator bounds are positive.
    * k≤K−1≤p−1 gives 2p−1−k≥k+1, so B_S≥0; L1.3 supplies D≥1. L1.4 and the exact quadratic reduction give exactly −B_S−νlog(1−u), with u=n g_{y_c}/[(n+1)(0.02τ̂²+q_S)]. The ratio of the positive new/old denominators proves 0≤u<1. Numerator lower and denominator upper bounds imply u≥u_S. Thus u_S<1 on the event, and monotonicity of −log(1−u) proves the gap.
    * Defining δ_S=+∞ when deterministic u_S≥1 is harmless: that case forces the constructed event to be empty. Its lower probability guarantee is then uninformative, not contradictory. In particular it cannot occur with a positive claimed lower probability. No infinite score is asserted on a nonempty event.

13. **NOTE — M1, M2, and M5 have valid proofs; M5 does not need C∈H in its first assertion.**

    Location: `lemmas/L7_master.md`, corollary proofs M1, M2 and M5.

    M1 is the immediate improving-addition contradiction, followed by the checked certificate-to-LO implication. For M2, if C misses truth and belongs to H then |C|≤K−1; its witness addition really is scanned. CC6 gives F(Ŝ)≥F(C∪t(C)), regardless of the search start, cache, or certificate. See finding 6 for the domain of δ_C.

    For M5, a move from a truth-containing centre can lose truth only by deleting t∈S₀ or swapping t for l∉C. In each case S₀\N={t}, so ANY permissible witness t(N) equals t. In the deletion case N∪t=C and F(C)<F(N). In the swap case |C|=|N|≤K−1 because N∈H, so C∪{l} is a legal addition and was scanned at C. As N is the maximum-F scanned neighbour, F(C∪{l})≤F(N). This contradicts the positive gap at N, which belongs to H⁻. There is no use of a gap at C in this argument, and C need not belong to H. The size condition on N supplies exactly the addition legality that could otherwise fail at K.

    Induction is valid while all subsequent models remain in H. In the capped case M2 first establishes containment of the last scanned C, then this argument establishes containment of N. The cap-return model does not need its own scan. Only the separate assertion about the top-level flag in STATEMENT is wrong (finding 2).

14. **NOTE — M3 constants, M4 constants, and the SCR-G probability/uniformity check pass.**

    Location: `lemmas/L7_master.md`, M3/M4; `STATEMENT.md`, SCR-G(i)-(iii).

    Put L′=2log(2p−1)+log(n+1). L1.3 gives B_S≤L′/2 and ν=(n+0.02)/2, hence 1−exp(−B_S/ν)≤L′/(n+0.02). Positivity of δ is exactly u_S above this threshold (with the infinite convention). Under MC, G_S>τ̄²T_n and the crude denominator gives u_S>L′/(n−0.98)>L′/(n+0.02). All factors n/(n+1) cancel as printed.

    Under MC°, σ≤σ_S and γ/σ_S²≥Ψ imply G_S>σ_S²T_n(1+ϑ°). The AM–GM inequality is 2σm_S≤σ_S²√(n−1). Thus U_S≤1.02τ̄²+[n/(n+1)](n−1)σ_S²(1+2a+2a²+r/√(n−1))≤(n−1)σ_S²(1+ϑ°). The last ϑ° term is deliberately larger than necessary after this simplification. Therefore u_S>L′/(n−1), as claimed. Both implications are valid for the default maximizing witness.

    In M4, A1 gives Γ≥κ²b²n/16. Since r²=o(n), √Γ−σr≥κb√n/5 eventually. τ̄²≤(1+o(1))(M²+σ²), hence Ū≤1.01nτ_*² eventually. This gives u_S≥[n/(n+1)]κ²b²/(25.25τ_*²)≥κ²b²/(26τ_*²) for n≥34: 26n≥25.25(n+1) is equivalent to n≥33 2/3. Also log(2p−1)+(1/2)log(n+1)=o(n) under the additional growth hypothesis. The same bound controls B_S for EVERY S, so there is no hidden nonuniform remainder. The resulting c₂=κ²b²/(104τ_*²) is correct. Findings 4 and 5 repair two proof phrases, not this constant.

    Choose x_n=√log n; the failure probability 4exp(−√log n)→0. This event is uniform over all models of size ≤q_n, hence over all seeds/search paths on a given response. With the strict eventual gap in finding 5, M2 gives SCR-G(i); M2 then M5 gives (ii); M5 induction gives (iii) for either executed path while sizes remain ≤q_n. Completed capped searches produce output and are included; numerical_failure/resource_limit runs are outside the assertion; exact enumeration is outside its “completed run” scope. No claim that these size/gap events occur with high probability is made or needed.

15. **NOTE — The actual L7 M6 example is correct.**

    Location: `lemmas/L7_master.md`, M6: “S₀ = {1} and x_1 orthogonal to all other columns”.

    For S missing 1, X_Sᵀx₁=0, so R_Sx₁=x₁ and a=n²/(n+1). The sign is fixed by θ*₁ and all d_S coincide, with norm √(1−1/n²)≤1. Thus w≤1 (indeed ≤1/√(2π)), and b_H≤1+√(2x), independently of the model count. Direct substitution gives γ=θ*₁²(n−1)²(n+1)/n². For fixed nonzero θ*₁, fixed σ, and fixed x, G is of order n, τ̄² is bounded, and u has a positive constant lower bound, while B=o(n) if log p=o(n). Hence δ>0 uniformly through size K−1 using the crude branch. No model-count entropy term is needed. This verifies the example with its actual hypotheses, not the stronger summary refuted in finding 1.

16. **NOTE — L5 facts (a)-(c) and every step of L5.1 pass.**

    Location: `lemmas/L5_exact.md`, from “Two quantities” through Step 3.

    Augmentation makes all involved columns independent even if X is singular. The residualized excess vectors form an m-dimensional basis; M is the positive-definite Schur complement and its inverse diagonal is positive. The block inverse gives a_j=1/(M^{-1})_{jj}, and 0<a_j≤n−1+λ₀<n, giving the stated α range. The inverse correlation matrix is positive definite with trace m, so 1≤ω≤m (strict <m for m>1 is unnecessary). At m=1 it equals 1; inverting the 2-by-2 M gives normalized off-diagonal −ρ, hence ω=1+|ρ| with the **augmented** partial correlation as defined.

    Under a floor φ, a_j≥λ_min(G_S+λ₀I)≥φ(n−1)+λ₀. Schur minimization gives λ_min(M)≥λ_min(G_S+λ₀I). Therefore ω≤λ_max(M^{-1})max_j a_j≤(n−1+λ₀)/(φ(n−1)+λ₀)≤1/φ for 0<φ≤1. Both parts of fact (b) hold.

    In Step 1, for excess j both S and S\j contain the mean's augmented coefficient combination, so the two orthogonality identities (1) hold. The deletion prior has the correct shifted numerator 2p−k. L1.6 after multiplying by τ̂² has exactly (n+1)/(nν) times the new-model denominator. D≥(n+1)a/n and a≥α(n−1) give 2B_j≥Λ_k(α); B_j≥0 justifies the positive part and dropping 0.02τ̂².

    The lower residual bound follows from Pythagoras for augmented noise, the two noise events, and the reverse triangle inequality. The bias normalization is ‖θ*‖₂/(σ√(n²−1)). Taking the outer positive part before squaring is legitimate and necessary. Multiplication gives σ²(n−1)(1−η)B_j/ν. Since (n−1)/(2ν)=(n−1)/(n+0.02)≥1−1.02/n>0, equation (2) follows with exactly the printed coefficient.

    In Step 2, d_j is the dual basis in W, with Gram M^{-1}. Its normalized vectors are the leave-one-out unit directions, up to harmless signs. Consequently the sum of squared inner products is bounded by ω‖P_Wv‖². Insert v=ε̃−b̃, contract the bias, and apply E3b; this yields exactly (3). No projection is accidentally taken in the ordinary rather than augmented space.

    Summing (2) over m indices and dividing (3) by mσ² gives EC′. Since α≥φ, Λ is increasing, and φω≤1, multiplying by φ gives EC. Neither an anchored floor nor any restriction on s₀ is needed for EC′ itself.

17. **NOTE — L5.2, SCR-C, the replacement remark, and SCR-R remain valid.**

    Location: `lemmas/L5_exact.md`, Corollary L5.2 through SCR-R.

    L5.2 intersects exactly the screening events with E2chi, E3a and E3b. The failure sum is 3e^{-x_A}+(1+2q)e^{-x}+e^{-x′}/(1−e^{-x′}), or 4e^{-x_A} for MC°. Violation of EC′ excludes all strict supersets; EC with the actual superset floor is a valid sufficient way to obtain that violation. If q≤s₀ the strict-superset quantifier is empty; no infinite floor needs to be substituted into a logarithm.

    SCR-C still uses only EC, which has been retained unchanged as a consequence. At x_A=√log n, x=2log n, x′=ε log n/8, the total failure goes to zero. Uniformly in k≤q_n, U(k,x)=o(n), and ‖θ*‖₂/σ=O(√n) makes η=o(1). With k=s₀+m≤(s₀+1)m, Λ≥2log(p/m)+log n−O(1); bounded s₀ is essential here. Its RHS is at most 2log(p/m)+2x′+O(√(2log p+log n))+O(1). The floor φ≥2log p/(2log p+log n)+ε supplies a uniform excess of at least ε(2log p+log n) before the o(1) and square-root losses. This dominates them. Thus L5.2 still proves exact recovery for all certified models in range.

    The replacement remark correctly retains BOTH conditional lengths and dual geometry. The cited R04 pair has a~11/n, so α~11/n²; D remains O(1), and the determinant penalty lacks the log n term. This really invalidates an ω-only replacement and is consistent with EC′. The remark does not claim a new asymptotic result.

    SCR-R uses E3a(q_n,2log n), whose failure is ≤2q_n/n²=o(1), and either screening event. Given containment, μ lies in the ordinary span even if X_C is rank-deficient, and P_Cy_c−μ=P_Cε. The ordinary-projector component of E3a gives the exact prediction bound in STATEMENT using log binom(p,k)≤klog(ep/k). No eigenvalue floor is used. With a positive superset floor, invertibility and X_CG_C^{-2}X_Cᵀ≼P_C/λ_min(G_C) give the coefficient bound with denominator φ(n−1). Constants and probability qualifiers match.

18. **NOTE — B2d and both A1 edits are valid with the directional floor.**

    Location: `lemmas/L4_bridges.md`, B2/B2°/B2d; `lemmas/L3_screening.md`, A1/A1°.

    The identity Δ(S)=‖(I−P_S)X_Tθ*_T‖² proves φ^d≥φ^a and, directly from its definition, Δ(S)≥φ^d(n−1)‖θ*_T‖₂². B2 uses the anchored floor only here; its remaining steps are monotonicity of Δ(√Δ−c_θ)² on Δ≥c_θ², ‖θ_T‖₁²≤|T|‖θ_T‖₂², and ‖θ_T‖₂≥√|T|θ_min. These remain valid with φ^d.

    B2° similarly uses only this lower bound to put u≥u₀≥2c_θ. It then uses σ_S²≤σ²+(u+c_θ)²/(n−1), u−c_θ≥u/2, u+c_θ≤3u/2, monotonicity of u⁴/(A+Bu²), and of V/(4σ²+9κV). The resulting 4σ²+9κs₀θ_min² denominator is unchanged. No hidden smallest-eigenvalue step remains.

    A1's ‖μ‖≤M√(n−1) and c_θ≤M/√(n+1), followed by B2d, give Γ≥κ²b²n/16. The squared margin denominator is ≤4τ_*²c₁n, giving ρ²≥200/64>2. A1°'s coefficient-size assumption is exactly √(κ(n−1))θ_min≥2c_θ. Applying directional B2° gives Ψ≥(n/8)min{κ²θ_min²/(4σ²),κ/(9s₀)}≥8 L_n using 16 and 576. The comparison denominator squared is ≤4 L_n, giving ρ°≥√2. The new assumptions and constants therefore match the statement. They impose no design family and no start/leakage condition.

19. **NOTE — L2 edits and the substantive L6 edits pass.**

    Location: `lemmas/L2_noise.md`, “Convention: a Gaussian variable with variance 0 is the constant 0” and “Let x′ > 0”; `lemmas/L6_sharp.md`, B_n bounds and Consequence 2.

    The variance-zero convention correctly covers cancelled μ and zero cross terms. All asserted Gaussian exceedance events are then trivial; formulas with a zero variance in a tail denominator should simply be read through that convention. E3b needs x′>0 to sum the geometric series, and it is now stated. Its failure sum and the whole-space case q−s₀<1 are correct.

    For B_n let u=L_n/(n+0.02) and c_n=1−0.98/(n²+0.02n)∈[1−n^{-2},1). Then B_n=c_n(n+0.02)(1−e^{-u})≤c_nL_n≤L_n. For u≥2 the proposed lower bound is nonpositive and automatic; for u<2 the factor 1−u/2 is nonnegative, so multiplying c_n≥1−n^{-2} is legitimate. This fixes the old sign omission. The asymptotic equivalence follows when log p=o(n).

    In Consequence 2, Δ~2(log n)², Γ~(log n)²/n, τ_n→σ, and the SCR-N inequalities hold with x_n=√log n. Both the new B1 rate and the claimed margin-only screening failure are correct. The added scaling argument is valid for a universal positive constant c: θ→tθ makes Γ, Δ and ‖θ‖₁² scale by t², so cΔ/(n‖θ‖₁²) would remain fixed as Γ→0. The homogeneous degree-four numerator is appropriate. Only the exact-ratio parenthetical needs finding 9.

20. **NOTE — Statement/PROGRAM reconciliation and re-lock disposition.**

    Location: `STATEMENT.md` §§3–4; `Theory_work/Wave3/PROGRAM.md`, item 5: “Certified screening ... under a floor on sets of size q_n + s₀; no start/leakage condition; must match the coded meaning of local_certified.”

    After the explicit fixes above, the statements match the proved inequalities and probabilities. A1 supplies the card's certified-screening conclusion under a weaker, coefficient-dependent directional condition implied by the card's sparse floor. Random designs are correctly conditional on X; no named design family is a theorem hypothesis. SCR-M's deterministic family of **models** is not a design-family restriction. Additional finite-sample tools support the asymptotic card rather than replace it. None of the arguments assumes that a small certified model, a small-gap centre, or a capped endpoint occurs with high probability.

    Re-lock requires removing the automatic M6 screening claim, qualifying the EC′ interpretations, and correcting the top-level flag statement, plus the local notation/proof repairs. The central target screening theorem, SCR-M, the no-dropping argument, EC′, SCR-C, and the floor-free refit prediction bound need no substantive mathematical replacement. No new numerical experiment is needed to repair these findings.
