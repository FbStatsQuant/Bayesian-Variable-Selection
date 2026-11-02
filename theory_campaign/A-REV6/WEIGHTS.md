# A-REV6: weight and naive-merge repair audit

2026-11-02. Mathematical review only; no numerical workloads were executed. New NM-R and W2-R below are Astra-authored replacement candidates, **pending independent Claude verification**. They do not modify or upgrade the original propositions. EX-A (exact arithmetic) is assumed throughout; none of this proves production floating-point or completion guarantees.

## Sources and preserved verdicts

Read from the following origin branch commits, rather than from working-tree copies:

| Source | Commit SHA | Files used |
|---|---|---|
| A-REV4 | b95948c3f350a225647f110937c3dea403b8443a | `theory_campaign/A-REV4/REVIEW.md`, `DRAFTS_CHECK.md` |
| F-DRAFT | 4de6e4c7fab641f11f1ba8bb9f306beae5103b74 | `theory_campaign/F-DRAFT/NEW_TARGETS.md` |
| O-WSTAB | 2ec30992adb12335e3cef3b0d9a88ca71c282d63 | `theory_campaign/O-WSTAB/PROOF.md`, especially WS1, WS3, WS6 |
| O-DILUTE | abedf99c92a7b818e9fcdb81bded624335f2b741 | `theory_campaign/O-DILUTE/THEORY.md`, especially E, N, L, S |
| F-SHARE | 13bc6654adca4ba4fc3ff85f56c60ccf9f1caa4f | `theory_campaign/F-SHARE/PROOF.md`, especially F2 and §§4–5 |

Applicable campaign protocol and theory priorities were read. The current instruction to write only this file and make no commits controls over the older protocol's commit/push directions.

| F-DRAFT item | Original source status | A-REV4 original verdict (unchanged) | Repair assessment |
|---|---|---|---|
| NM | PROVED modulo T03/EXP′/Cor. P1 | ERROR, with additional GAPs | NM-R supplies a finite four-state candidate; growing-p normalisation and stage-count claims remain OPEN |
| W1 | PROVED candidate | VERIFIED | Exact BO algebra checks; O-WSTAB WS3 gives the same mechanism. Exact sample BO is essential |
| W2 | PROVED modulo candidate EXP′ | ERROR, with uniformity GAP | W2-R(a) fixes the exact identity; W2-R(b) supplies a narrower ORTH additive uniform expansion. Both replacement candidates await Claude |
| W4 | PROOF SKETCH | GAP overall; TV implication VERIFIED | Complete-state KL inequality and tilted-law sufficient conditions check. Advertised KL rate and sharp chi-square law remain unproved |

## W1: what survives, and where it applies

Write c=2b0+y'y, t_S=n z_S'H_S^{-1}z_S and Q_S=y'y-t_S. Under exact sample block orthogonality, H and G split over blocks, so D_S=product_b D_{S_b} and t_S=sum_b t_{S_b}. With xi_b=t_{S_b}/c,

    d(S)=nu [sum_b log(1-xi_b)-log(1-sum_b xi_b)] >= 0.

The sign follows from product_b(1-xi_b)>=1-sum_b xi_b; equality holds exactly when at most one xi_b is positive. A known **common** noise variance makes both determinant and quadratic score additive, hence d=0 and the globally prior-coupled start equals the posterior, including its cap. Independent normalised block posteriors are a different object.

O-DILUTE Lemma L correctly limits transfer of this conclusion: population BO does not give sample BO. Its Lemma N's conditional Beta law follows when the raw Gaussian null column is independent of the full response and other columns. Zero correlation with the truths alone does not imply independence of that column from all other columns. For a block chosen using X, this lemma alone also does not establish a joint law after conditioning on the selected partition. Thus a common-variance replacement is not certified for the study design by W1. O-DILUTE E's size-correction identity and S's ranking ceiling are exact finite-data statements and avoid that transfer problem.

## W2-R: exact regularised identity and an ORTH uniform repair

**Astra-authored candidate; GAP for adoption pending Claude verification.**

(a) For any data satisfying sample BO, any S with |S|<K, and l outside S in block b, set T=S intersect C_b and

    h_{U,l}=(t_{U+l}-t_U)/(2b0+Q_U),  U=T,S.

Then 0<=h<1 and, exactly,

    h_{S,l}=h_{T,l}(2b0+Q_T)/(2b0+Q_S),
    d(S+l)-d(S)=nu[log(1-h_{T,l})-log(1-h_{S,l})].

Proof: BO makes the two explained increments equal and the determinant addition factors identical. Insert the exact score log BF(U)=-log D_U/2-nu log[(2b0+Q_U)/c]. Prior odds cancel between posterior and start. Positivity of the updated residual denominator gives h<1. No Gaussian assumption is needed. Ordinary RSS partial R-squared cannot replace h.

(b) Consider deterministic centered ORTH designs X'X=(n-1)I_p with p<=n-1, raw contrast response Y=X theta+epsilon, epsilon isotropic N(0,sigma² I) on the contrast space, sigma>0, fixed support size s0 and fixed nonzero coefficients. Use v3 response standardisation, fixed a0=b0=.01, a deterministic partition, and |S0|<K. For l outside S0, define Z_l=x_l'epsilon/(sigma sqrt(n-1)); these are independent standard normals. Let T_b=S0 intersect C_b, Delta_b=sum_{j in S0 outside C_b}theta_j², and kappa_b=Delta_b/(sigma²+Delta_b). Then

    max_{l outside S0}|d(S0+l)-d(S0)-kappa_{b(l)} Z_l²/2|
      = O_P(log n/sqrt(n)+(log n)^2/n)=o_P(1).

Proof: in ORTH, H=n²I, t_U=(n-1)/n times the ordinary explained sum of squares. Undoing response standardisation multiplies every residual denominator by the common sample variance s_Y²; its 2b0 offset becomes 2b0 s_Y²=O_P(1). Gaussian quadratic-form concentration and fixed s0 give, simultaneously over the at most 2^s0 different T_b,

    (2b0+Q_{S0})s_Y²/n=sigma²+O_P(n^-1/2),
    (2b0+Q_{T_b})s_Y²/n=sigma²+Delta_b+O_P(n^-1/2).

The raw-scale null increment is sigma²(n-1)Z_l²/n, independent of the reference U. Since nu=n/2+.01, this yields

    nu h_{S0,l}=Z_l²/2 [1+O_P(n^-1/2)],
    nu h_{T_b,l}=(1-kappa_b)Z_l²/2 [1+O_P(n^-1/2)],

with random error bounds common to all l. A Gaussian union bound gives max_l Z_l²=O_P(log n), hence max h=O_P(log n/n). Uniform Taylor expansion -log(1-h)=h+O(h²) in (a) proves the assertion. This is an additive error, sufficient to exponentiate the single-null discrepancy uniformly; it asserts neither a relative error near Z_l=0 nor control of multi-extra layers. It narrows BO to ORTH and does not certify the original W2.

## NM-R: a complete four-state replacement

**Astra-authored candidate; GAP for adoption pending Claude verification.** Let p=2, K=2, singleton blocks {j},{l}, deterministic centered columns with norms sqrt(n-1) and fixed correlation r satisfying 0<|r|<1. Let Y=theta x_j+epsilon with fixed theta!=0 and sigma>0 and isotropic Gaussian contrast noise. Use v3 preprocessing, exact scores and the capped BB(1,p) prior. Put

    c_l = (1/2)log[(sigma²+theta²)/(sigma²+theta²(1-r²))] > 0.

Then local singleton inclusion probabilities tend to one, the naive union is {j,l} with probability tending to one, pi0({j,l})->1, pi({j})->1, and

    log pi0({j})=-n c_l+O_P(sqrt(n)+log n),
    TV(pi,pi0)->1,
    liminf (1/n)log[1+chi²(pi||pi0)] >= c_l

where the last liminf is in probability (equivalently every smaller constant is an eventual probability-tending-to-one lower bound). This p=2 construction falls on the production exact-enumeration branch. It is a counterexample for naive union and abstract start-based schemes, not a production-SMC execution failure. A polynomial number of iid start draws misses {j} with probability tending to one. An independence-MH chain initialised from pi0 likewise fails to visit {j} in polynomially many proposals with probability tending to one.

Proof: direct singleton scores have n^-1 log BF({l})->c_l and n^-1 log BF({j})->(1/2)log[(sigma²+theta²)/sigma²]>0. Smooth Gaussian quadratic-form expansions give log BF({l})=n c_l-(log n)/2+O_P(sqrt n), which retains the sampling fluctuation omitted in NM. In fixed dimension ridge/offset corrections to the OLS log scores are O_P(1).

The four start weights are w(0), w(1)BF(j), w(1)BF(l), w(2)BF(j)BF(l). Dividing by the last weight proves pi0(j,l)->1 and the displayed truth-mass rate, with no unbounded normaliser left uncontrolled. Both local blocks have fixed positive prior odds and exponentially growing singleton scores, proving their local selections.

For the posterior, compare all three alternatives directly with {j}. The empty-model ratio is exponentially small. The proxy-only ratio has logarithm

    -(n/2)log[1+theta²(1-r²)/sigma²]+O_P(sqrt n+log n).

The pair-to-truth ratio is n^-1/2 exp[O_P(1)] times the fixed prior ratio: the residualised proxy has zero signal and its one-dimensional Gaussian gain is tight. Therefore pi(j)->1. The event {j} gives TV separation and the single truth term gives 1+chi²>=pi(j)²/pi0(j), proving the exponential bound.

Conditionally on the data, Q iid draws hit truth with probability <=Q pi0(j). For independence-MH, visiting truth requires either initial truth or a truth proposal, so the bound is (Q+1)pi0(j). This proves the stated initial-law result without claiming failure from every initial state. Reweight/resample-only schemes cannot create absent truth. These statements do not themselves prove failure of a specified evidence estimator.

For a terminal Gibbs label l, **conditional on the actual pre-label state being {j,l}**, the flip scores {j} and deletes l with probability 1/(1+pi({j,l})/pi({j}))->1. This is a label-time statement. It does not infer that occupancy from the round-start mode. No O(1) ideal-grid stage count is claimed.

F-SHARE supplies no missing proof of the general NM claim. Its exact-Gram delivery route needs PK and DOM; F2 retains PROOF SKETCH status, and §4 depends on Conjecture 4.3 for extras/order bookkeeping. Its reversible-leak F1′ is itself CONJECTURE. These are useful interfaces for future delivery/repair work, not an unconditional replacement for occupancy or stage-count assumptions.

## W4: complete-state repair, with rates still open

For arbitrary positive finite laws related by pi proportional to pi0 exp(d), any reference a satisfies exactly

    KL(pi||pi0)=log[pi(a)/pi0(a)]+sum_S pi(S)[d(S)-d(a)]
       <=-log pi0(a)+sum_{S!=a} pi(S)[d(S)-d(a)].

This is the sound replacement for dropping all but the single-null layer. Positive contributions from multiple extras and mixed models require bounds. Independently,

    TV(pi,pi0)<=max{1-pi(a),1-pi0(a)}.

The latter follows by separating the singleton a from its complement and is stronger than F-DRAFT's sum bound. Thus the original TV rate is valid conditional on its concentration inputs.

O-WSTAB provides an exact diagnostic: with q_alpha proportional to gamma0 exp(alpha d),

    1+chi²(pi||pi0)=pi(a)²/[pi0(a)q2(a)].

This follows by summing pi(S)²/pi0(S) and cancelling normalisers; endpoint concentration alone leaves q2 uncontrolled. For any theta>0,

    KL(pi||pi0)<=log[pi(a)/pi0(a)]
       +pi(a)/theta [1/q_{1+theta}(a)-1].

To prove it, use x<=exp(theta x)/theta for x>0 and bound the positive part of d-d(a); the full tilted sum over S!=a is exactly pi(a)[1/q_{1+theta}(a)-1]. Hence pi(a),pi0(a),q_{1+theta}(a)->1 suffice for KL->0, but a rate requires rates for all three masses. This controls every state and avoids the omitted-layer error.

WS6(d)'s ORTH single-null extreme-value lower-bound mechanism is compatible with W2-R(b); its all-layer upper threshold is explicitly WS6(e) CONJECTURE. Exact ORTH also imposes p<=n-1, so a formal p=n^A scaling there has A<=1. Neither WS6(e), the F-DRAFT sharp chi-square formula, nor the claimed KL rate has been discharged here. Small TV/KL versus unstable second moments remains a valid conceptual distinction; the advertised v3 sharp rates remain OPEN.

## Verification handoff

Claude should verify NM-R's fixed-dimensional ridge/IG remainder and four-state comparisons, and W2-R(b)'s common-error bounds after response scaling. The original A-REV4 ERROR/GAP verdicts are preserved even if these replacements pass. General sample-BO uniform W2 beyond ORTH, growing-p NM normalisation, positive multi-extra KL contributions, q2 upper control, finite-threshold ideal-grid stage bounds, and production label-time occupancy remain separate obligations.
