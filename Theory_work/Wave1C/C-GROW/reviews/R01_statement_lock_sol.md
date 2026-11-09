Statement-lock review: C-GROW v1

The target and composition route are appropriate. I recommend conditional lock after the changes below. I found a definite false instance assertion, several scope/wording defects, and a substantial unproved sandwich step. I did not find a counterexample to the general probabilistic theorem after those repairs. This is a statement review, not verification of the proposed lemmas.

Citation aliases (all relative to the repository root):

- CG = `Theory_work/Wave1C/C-GROW/`; ST = `CG/STATEMENT.md`; PL = `CG/PLAN.md`.
- GEN = `Theory_work/Wave1/W1-GEN/`; M = `Theory_work/State_of_Project/sections/02_method.tex`; TH = `Theory_work/State_of_Project/sections/04_theory.tex`.
- T37 = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T37R/PROOF.md`.
- P1C = `Theory_work/Wave1C/PROTOCOL.md`; DG = `Scripts/Data_generators/gen_dev_data.R`.

1. Target, fidelity, and claim-by-claim assessment

The right target, with a narrower instance scope than the brief suggests.

The reported-HPM error on output, rather than conditional error given output or delivery, is correctly selected. M5's corrected composition inequality is exactly the required bridge, and T03♯ concerns the exact posterior rather than discovery by the algorithm (TH:477–484, 514–521, 767, 775–782). Operational closure is the appropriate discovery interface (GEN/lemmas/L5_assembly.md:11–16, 31–39). ST:11–15 and 69–72 faithfully follow that route. The liminf identity is also appropriate once U_n is defined as the no-output event, as in GEN/lemmas/L5_assembly.md:28–39.

However, the instances are exact-Gram population analogues; random-row S2/S5 remain excluded by ST:81–85. The diagnostics use iid designs (CG/numerics/d_common.py:196), and the actual development generator draws random Gaussian rows (DG:53–61). Also, fixed-p S5 is not an asymptotically growing relevance-set instance. Say explicitly that the ticket provides a growing-relevance theorem, an exact-Gram AR(1) instance, and a fixed-p S5 illustration. It does not yet establish the advertised result for the study generator.

(C1): passes the deterministic adversarial check, subject to feasibility notation.

Let T contain the truth and let a be an extra. NA at T−a gives F(T−a)>F(T). For a swap a→l, NA at T−a gives

    F((T−a)+l) < F(T−a).

Thus every null swap is strictly dominated by its corresponding extra deletion, including swaps outside Q. Additions are negative by NA; all truth-removing moves are negative by TL. Hence every best improving neighbour is an extra deletion. Ties between deletions are harmless. At |T|=K, T−a has size K−1, so the comparison addition is feasible even though additions at T are not. This is exactly the valid argument in T37:110–116, not an inference from “no additions” alone. The scan/move bounds in ST:63–64 agree with GEN/lemmas/L4_search.md:24–40 and M:463–467. “Certified” must refer to the search endpoint; the public flag concerns the finally returned HPM (M:505–506; GEN/lemmas/L4_search.md:26–28).

(C2): plausible; the proposed numerical constants survive the score/prior check.

For k=|T|, the exact per-model prior ratio is

    w(k+1)/w(k) = (k+1)/(2p−1−k).

Using the shipped ridge score (GEN/lemmas/L1_lemmaE.md:54–66), the relevant uniform null-add comparison on O(log n) sets should be proved in the form

    2[F(T+l)−F(T)]
      = Z²_{T,l} − log(n+1)
        − 2 log((2p−1−k)/(k+1)) + O_P(1),

with an explicitly uniform remainder on a high-probability event. The O(1) score remainder suffices for the strict logarithmic margins here; an unproved o(1) remainder is unnecessary. The archived threshold uses 2p−k (T37:223–224); do not copy that as the exact BB ratio.

Writing q=|P_n|, G4-dir gives at most p n^{o(1)} Gaussian events and k=O(log n). The union-bound scale is

    p N_n exp(−[log n+2 log p−O(log log n)]/2)
      = n^{−1/2+o(1)}.

This works for every fixed A; the p factor cancels. An unstructured union over p2^q would only yield the stricter sufficient bound q log 2 < (1/2)log n, so it cannot establish the stated G4-chi constant (ST:54–56; PL:10–11).

The proposed Pythagorean improvement does plausibly establish it: set E=span((I−P_{S0})X_P), and let Q_l=Q\{l}. Every u_{T,l} lies in E plus the single orthogonal direction u_{Q_l,l}; therefore

    Z²_{T,l} ≤ ||P_E ε/σ||² + Z²_{Q_l,l}.

The first term is one common chi-square variable with rank at most q. Under q≤(1−δ0)log n it is at most (1−δ0/2)log n with probability tending to one. Meanwhile max_l Z²_{Q_l,l}≤2log p+o(log n) with probability tending to one. The remaining δ0 log n margin absorbs O(log log n), score errors, and variance estimation. This avoids the incorrect substitution of a union over all lattice projections. G2 supplies the needed nondegenerate residuals (ST:48).

TL also looks viable: the family of truth-removing neighbours has polynomial size, G2 covers the swapped outside column, and the lost signal is of order n φ0² θ_min*², which dominates log n by H0/BM-∞. This is the growing-family extension of T37:221–222, not a result already proved there.

(C3): the main proof risk; NEG's constant is credible, but a local deletion argument is insufficient.

The threshold has the right algebra. If a=log p/log n≤A, a block null increment has leading upper scale

    [a + η/2 + sqrt(2aη) − 1/2] log n.

At a small global model, subtracting the BB log p penalty leaves η/2+sqrt(2Aη)−1/2<0, precisely the displayed strict bound on η (ST:51–52). This agrees with the predecessor's sufficient NL_eta threshold (GEN/STATEMENT.md:69–75). Bounded energy is needed for the block RSS controls; C3 does state it (ST:67–68).

But this does not exclude a maximiser near K: its prior deletion reward is log((2p−k)/k), potentially only O(1), not log p. Nor can TV simply add a missing truth at a saturated mode. The predecessor's centre theorem has a fixed-size reference and its aggregation bound contains that reference size; it does not already prove the desired sandwich for a growing Q (GEN/lemmas/L2_centre.md:12–20, 54–63).

A concrete viable size-ladder obligation is available. Let H be Q together with every block meeting S0, so |H|=O(log n). For l outside H, NEG applies to every within-block conditioning set because its block has no truth. Define

    V_n = sum_{l outside H} max_{U subset C_b(l)\{l}}
                         r_b(U+l)/r_b(U).

Prove V_n/p=o_P(1), preferably at a polynomial rate, using the truncated Gaussian integral/Markov argument underlying GEN/lemmas/L2_centre.md:40–48. Do not use an untruncated expectation of exp(Z²/2), which is infinite. At any global maximiser of size k, deletion optimality implies each selected l outside H has table ratio at least (2p−k)/k. Consequently

    (k−|H|)_+ (2p−k)/k ≤ V_n,

and 2p−k≥p gives k≤|H|/(1−V_n/p)=O(log n), simultaneously for all maximisers. After that, TV can insert truths without the n/2 cap obstruction, and NEG can exclude outside-Q variables with the correct small-k prior penalty. When K=p, a saturated model already contains all truths. This is a proposed proof route, not a checked lemma. Until an equivalent global argument is proved, C3 remains the likeliest failure point.

(C4): MR1 and the cap comparison are sound, conditional on C2–C3.

On the sandwich/descent event, |S~0\S0|≤|S~0|, so MR1 more than covers all deletion moves and the final scan. Under G4-chi, |P_n|<(log n)/log 2≤ell_n eventually, so the production-cap corollary is valid (ST:36–38, 60–72). The cap may depend on the data through |S~0|: LS0 still reads no uniforms and operational closure is pathwise (M:492–498; GEN/lemmas/L5_assembly.md:11–16). Changing this unshipped parameter is explicitly permitted, with reporting obligations (P1C:40–46). This says nothing about delivery or the already-shipped core.

(C5)(a): the AR(1) mechanisms are plausible, but the instance needs precise growth and radius statements.

Exact AR(1) conditioning depends only on the nearest selected index on each side of l. Thus with |Q|=O(log n), there are at most O((|Q|+1)²) residual directions per l, sufficient for G4-dir. This is an exact-Gram argument; the archived general LD argument explicitly leaves its neighbour-reduction step unwritten (T37:225–231), so that sketch is not a completed proof of this instance.

After alternating sign transformation when rho<0, conditional covariances have the positive AR(1) structure. The natural bounds to prove are |Cov(j,k|U)|≤|rho|^{|j−k|} and Var(j|U)≥v_rho=(1−rho²)/(1+rho²). The displayed separation condition then leaves at least |theta_j*|v_rho/2 in the partial-signal numerator. For fixed nonzero coefficients this gives TV of order n, uniformly over within-block U. Far-null partial signal is bounded by C n |rho|^{2d_n}; hence the explicit choice

    d_n = ceil(log n / [2 log(1/|rho|)])

makes it O(1), and NEG holds with any fixed admissible η>0 eventually. Merely saying d_n asymp log n/(2log(1/|rho|)) is insufficient: half that radius still satisfies asymp but can leave leakage of order sqrt(n), violating NEG (ST:73–77).

H0 is credible from the uniform full-Gram floor (1−|rho|)/(1+|rho|), bounded fixed-support energy, and fixed nonzero coefficients; this verifies both normalized and unnormalized eigenvalue requirements, including the prior-defined tail cutoff (TH:775–778). But p≤n−1 alone neither makes |P_n| grow like log n nor ensures G1. Fixed p is allowed as written. Specify the intended p_n regime and distinguish an O(log n) upper bound from actual logarithmic growth.

(C5)(b): false as written because of G1.

Here P=[p]\S0, so Q=[p] and s0+|P|+1=p+1>K for every n, since K≤p. Thus C5(b)'s assertion that G1 holds eventually is impossible (ST:29, 46–47, 78–80). This is a formal counterexample to an instance assertion, independent of any statistical proof. Use the predecessor's boundary treatment: require |Q|≤K and require |Q|+1≤K only when Q≠[p], equivalently min(p,|Q|+1)≤K (GEN/lemmas/L5_assembly.md:34–36).

After that repair, fixed-p S5 has full-Gram floor at least 0.3 because Sigma=0.3I+0.4H+0.3 11', consistent with the generator formula (DG:20–28). H0 and G2 are therefore straightforward; NEG is vacuous, and G4-chi eventually holds for the fixed 96 nulls. TV still requires its promised finite computation; it is not supplied by D1–D3. Specify the actual coefficients and partition/tie algorithm. The cited production generator defines truth only at p=30,500,1000, with s0=5 or 14, whereas these diagnostics deliberately use four truths at p=100 (DG:33–41; CG/numerics/d_common.py:3, 11, 196). Call this a diagnostic layout using the study covariance, rather than an already-defined “study theta*”.

2. Numerical evidence and time feasibility

The stated LS0 scoring totals and cap obstruction agree with D2:6–12, 15–20 and D3:17–22. The deletion-only S2 observation is supported by D3:29–35. S5 has occasional swaps even at n=12800 (D3:39, 43), so the diagnostics do not establish uniform NA on the lattice; they only motivate a limiting result.

Replace “the exact posterior concentrates” in ST:18 by “the finite-chain diagnostics are consistent with posterior concentration.” D1:8, 12, 16, 20 reports finite MC3 occupancy and best-visited models, not an exact posterior calculation or a mixing certificate. Also, at n=800 S5 the start does not always contain the truth (D2:14, 18); the clean superset-descent interpretation starts later.

The entire seven-lemma programme plus falsification, independent checks, sweep, and council is ambitious for a few hours (PL:5–21). C1 and assembly are short; C2 and exact-Gram locality are manageable. C3 is the critical path because global size control is new. Prioritize its size ladder before scheduling downstream instance checks. A meaningful few-hour fallback is C4 conditional on the sandwich event having probability tending to one, as already contemplated in PL:23–24. That fallback must be labelled a discovery theorem conditional on a new centre hypothesis, not closure of the S2/S5 target.

3. Required changes

1. Repair G1's feasibility boundary using min(p,|Q|+1)≤K. Reason: C5(b) otherwise violates G1 for every n; the predecessor already handles this boundary correctly (ST:46–47, 78–80; GEN/lemmas/L5_assembly.md:34–36).
2. Make the global size ladder an explicit C3 proof obligation, including saturated modes and simultaneous control of every maximiser. Reason: the NEG threshold only supplies the desired exclusion once the BB penalty is evaluated at small k; fixed-reference centre concentration cannot simply be reused (ST:67–68; PL:12–13; GEN/lemmas/L2_centre.md:54–63).
3. State the exact BB ratio and uniform null-add expansion, and give separate probability arguments for G4-chi and G4-dir. Reason: the archived threshold is not the exact ratio, and a lattice union bound loses the advertised chi constant (T37:223–224; ST:54–56; PL:10–11).
4. Replace the AR(1) radius asymp specification by an explicit sufficient radius, and specify the p_n regime. Reason: asymp permits radii with excessive far-null leakage, and p≤n−1 permits fixed or slowly growing dimensions (ST:73–77).
5. Define the S5 diagnostic coefficients/layout and supply the finite TV check before claiming the instance. Reason: the p=100, s0=4 layout is not the production generator's declared truth, and D1–D3 do not verify TV (ST:78–80; DG:33–41; CG/numerics/d_common.py:3, 11).
6. Correct the scope and diagnostic language: exact-Gram analogues, fixed-p S5, finite MC3 evidence, and no random-design closure. Reason: these distinctions materially limit the target achieved (ST:11–18, 77–85; D1:3, 8, 16; CG/numerics/d_common.py:196).
7. Make the inherited hypotheses self-contained or precisely incorporated: write out H0's tail cutoff and fixed constants; specify A≥1, sigma²>0 fixed, response centering/standardization, and the actual partition/tie rules; define U_n and “expansion events”. Reason: these are substantive model/method premises, currently partly hidden behind broad GEN references (ST:27–34, 45, 70–71; GEN/STATEMENT.md:26–54; TH:775–778).
8. Fix MR1's reference to “C3(b)” to C4(b), use endpoint certification terminology, and carry MR1 into METHOD_REQUIREMENTS.md and the top of REPORT.md. Reason: the reference does not exist, public certification has different semantics, and the protocol requires concrete engineering communication (ST:36–38; M:505–506; P1C:40–46).
9. Amend PL's “only constants change” for L1 reuse. Reason: J=O(log n) changes the chi-square rank factor 2^{J/2}; adjust the Gaussian event thresholds and recheck the RSS floor and remainder uniformly, rather than cite the fixed-J result verbatim (PL:6–7; GEN/lemmas/L1_lemmaE.md:19–36, 57–61, 74–86).

Optional suggestions: prove truth inclusion and the size ladder separately; retain the strict eta margin rather than optimize its boundary; record a separate exact-Gram direction-count identity so approximate random-design locality is never silently substituted; distinguish finite-n cap failure of LS0 from failure of the full method's D_n, as the predecessor explicitly does (GEN/STATEMENT.md:150–154).

LOCK-WITH-CHANGES
