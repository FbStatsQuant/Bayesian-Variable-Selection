VERIFIED-WITH-AMENDMENTS

Review scope: STATEMENT.md §§1–3, L1_lemmaE.md, L3_descent.md, L4_search.md, production semantics in 02_method.tex:459–506, W1-T37R/PROOF.md (Lemma 3, Theorems A/C and C3), and 05_history.tex (RF176). Line references below refer to the reviewed versions. Only this review file was written.

The mathematical claim about centres, the uniform move bound, and the strict local maximum is valid after the local amendments below. No counterexample to that claim was found. The principal contrast estimates are correct. The amendments repair two unjustified restrictions on p, a mistaken size equality whose omitted contribution is favourable, and the distinction between a search endpoint and the method's finally reported HPM/certification.

1. Feasibility condition is unnecessarily strong and need not hold eventually.

   Location: L3:16–17; L4:17; application to STATEMENT (C2)/(C3).

   Problem: vbar + 1 <= K is not implied by the stated hypotheses, even eventually: p may remain bounded, and K <= p. For example, p = |V| = s0 = vbar = 1, a normalized nonconstant column, sigma² = 1, theta_min = n^(-1/4), and phi0 = 1 satisfy the relevant hypotheses, but K = 1 forever. This is a counterexample to the asserted sufficiency of the hypotheses for that intermediate cap condition, not to descent. The actual family contains no two-variable model in this example.

   Concrete fix: in L3 use |A| <= min(p, vbar + 1) and note that min(p, vbar + 1) <= K once floor(n/2) >= vbar + 1. This holds eventually without p -> infinity. In L4 replace vbar + 1 <= K by |V| <= K. If S misses a truth then |S| <= |V| - 1, so the designated truth addition is feasible. Extra deletions are always feasible, swaps preserve size, and outside additions are compared only when feasible. These conditions suffice for the induction. Keep the statement's C ∈ Ω restriction until the eventual regime is entered.

2. The prior bounds require no lower bound on p; remove the unsupported restrictions.

   Location: L3:32–34, 89–94.

   Problem: neither vbar + 1 < p nor p >= 2 vbar + 2 is a hypothesis or a consequence of p <= n^A. Likewise vbar <= p at line 94 need not hold when vbar is a loose upper bound.

   Concrete fix: for an actual addition put k = |T| <= p - 1. Then

       1/(2p) <= (k + 1)/(2p - 1 - k) <= 1,
       2p - 1 - k >= p,
       log[w(k + 1)/w(k)] <= log(vbar + 1) - log p.

   These are exactly the inequalities needed, for every feasible addition including p fixed. For deletion use 1 <= k = |T| <= p, giving (2p - k)/k >= 1. Thus the stated Pi = O(log n) bound, the constant c_v, and L3.3(a),(b) survive unchanged. Capping normalizes the prior by a common factor, which cancels. Pi should be defined explicitly as a nonnegative common upper bound for the absolute size-plus-prior contribution, rather than as a pair-dependent signed term. For P versus an outside swap A, |P| - |A| = 1; hence Pi really does cover the potentially adverse additional size penalty in L3.2(b2).

3. Incorrect size equality in the truth-outside swap comparison; the conclusion remains valid.

   Location: L3.3(c3), lines 99–100.

   Problem: with k = |T|, D = T minus {e} has size k - 1, whereas A = (T minus {i}) union {l} has size k. Thus '|D| = |A|' and 'no size difference' are false.

   Concrete fix: retain the favourable contribution explicitly:

       F(D) - F(A)
       >= log((2p - k)/k) + (1/2)log(n + 1)
          + (1 - c_S)L_n/(8 C_R) - 2 kappa_E.

   The first two terms are nonnegative because k <= p, so the displayed lower bound in the manuscript still follows by dropping them. No enlargement of W_n is necessary. The residual comparison itself is correct: r_D = 0 and ||r_A - r_D|| = sqrt(Lambda_A).

4. Certification must identify the search endpoint, not unconditionally the finally reported HPM.

   Location: L4:10–12, 21–23, 34–36; STATEMENT (C2), final sentence; compare 02_method.tex:468–471, 490–506.

   Problem: the proof establishes that the local-search routine ends at the scanned centre S0, with no improving neighbour and no move-limit termination. LS0 starts from the start mode rather than necessarily the pre-existing global best. The finally reported model is the best over all models ever scored. In particular, 02_method.tex:505–506 evaluates the public local_certified flag on the finally returned HPM, from whichever search ended on it. C2's event controls neighbours of subsets of V; it does not assert that arbitrary previously scored models outside this family lose to S0. Thus an unconditional claim about the reported HPM's flag cannot be substituted for the search-endpoint statement. This is the same scope distinction behind W1-T37R Lemma 0(b); L4's last remark recognizes it but the main wording should do so too.

   Concrete fix: say 'the search endpoint is S0, its completed final scan certifies this endpoint, and this search does not terminate at local_limit.' Reserve the public flag claim for the additional case where the finally reported HPM is that endpoint (for example on posterior dominance pi(S0) > 1/2). This does not weaken the scoring conclusion used to bound D_n. If 'returns ... with local_certified' is intended solely as the routine's archive result, define that local meaning explicitly and distinguish it from the final output flag.

5. Best truth addition: verified, including the Gram-floor use.

   Location: L3.1, lines 39–48.

   Problem checked: the Schur complement could not be bounded from a floor on S alone. Here H1a supplies a floor on S union M ⊆ V, which is the required larger matrix, so there is no such gap.

   Verification/fix: if G >= a I, its Schur complement B satisfies z'Bz = min_b (b,z)'G(b,z) >= a||z||². Thus Lambda_S >= (n - 1)phi0²||theta_M||². Combining Lambda_S <= ||theta_M||_1 max_j |<rho_j,r_S>| with ||rho_j|| <= sqrt(n - 1) gives the phi0^4 bound exactly as written. Cauchy–Schwarz gives ||theta_M||_1² <= |M| ||theta_M||². H1a ensures every rho_j is nonzero. No extra incoherence condition or fixed coefficient lower bound is needed. For completeness, state that S = empty uses B = G_M directly rather than an inverse of an empty block. No substantive fix is required.

6. All three missing-truth contrasts and their constants: verified.

   Location: L3.2, lines 57–72.

   Problem checked: a nonnested residual difference cannot in general be bounded by sqrt(|Lambda_A - Lambda_P|). The proof correctly avoids that shortcut.

   Verification/fix: (a) ||r_S - r_P||² = E2 by nesting. The bound E2/2 - 2 sigma² h_n² - sigma² t_n >= E2/4 follows under the stated, conservative L_n >= 4H_n. For (b1), nesting through S gives ||r_A - r_P|| <= sqrt(zeta_n) + sqrt(E2). For (b2), nesting through S' = S minus {i} gives the valid bound sqrt(zeta_n) + sqrt(E1) + sqrt(E2), with E1 >= 0. SEP must be used at S', and it is: Lambda_A - Lambda_P >= E1 + E2 - zeta_n holds whether i is a truth or an extra.

   Applying 2 sigma h sqrt(x) <= epsilon x + sigma² h²/epsilon separately gives exactly two or three noise remainder terms. With epsilon = (1 - c_S)/4,

       (1 - epsilon) - (1 + epsilon)c_S >= (1 - c_S)/2.

   The remaining E1 term is nonnegative. Since L_n/log n -> infinity, the losses O(log n) are absorbed uniformly, leaving RSS margins E2/4 or (1 - c_S)E2/4. L1.4(b) then gives the stated 1/(8 C_R) constants. E6 and Pi handle all size differences; (b1) has equal sizes and (b2) differs by one. No substantive fix is required beyond item 2.

7. Uniformity, D4, D5, and the null-addition asymptotics: verified.

   Location: L3.0 and L3.3(a),(b), lines 13–29, 83–94; L1.1–L1.4.

   Problem checked: adaptively visited states cannot be treated as a fixed handful of noise statistics. This proof takes the events over deterministic supersets of all possible states instead.

   Verification/fix: |F| <= 2^vbar(p + 1), J <= vbar + 1, and the full residual/contrast family has O(n^(2A)) members. Every outside neighbour has exactly one outside variable, so it is in F even if outside variables are mutually highly correlated. No Gram floor on a union of two outside variables is used. D1–D3 therefore control every contrast simultaneously, including adaptively chosen paths and best truth choices.

   D4 is a deterministic family at each n: X, V, and S0 are fixed, and at most vbar 2^vbar deletion directions occur. The direction can explicitly be chosen as (I - P_(T minus {e}))x_e divided by its norm. The family may change with n; its uniformly bounded cardinality is sufficient. Each statistic is standard normal; neither independence nor a fixed collection of vectors across n is required. The (log log n)² bound is o(log n), so extra deletion wins. Replace 'fixed finite set V' in the remark by 'deterministic sets V_n of uniformly bounded cardinality' to avoid ambiguity.

   D5 covers at most 2^vbar p standard normals and its stated 2/log n failure bound is correct. For supersets in F, RSS >= sigma² n(1 - omega_n), with omega_n = O(n^(-1/3) + log n/n). Consequently x = O(log n/n) uniformly, and the absolute error in the nu log bound is

       O(log n [n^(-1/3) + log n/n]) = o(1).

   This justifies the additive o(1), not merely a relative o(1) multiplying log p. The log p term cancels the actual prior penalty, leaving -0.5 log n + log log n + O(1). No independence or LD assumption is needed. Restrict the introductory sentence 'for T' superset S0' at lines 83–84 to T' in F, since D2 is only asserted on F; every use here is in F.

8. Superset outside swaps and strict local maximum: verified after item 3.

   Location: L3.3(c1)–(d), lines 95–106.

   Problem checked: outside swaps removing a truth must not be treated as pure-noise additions.

   Verification/fix: (c1) loses to the centre and hence to any extra deletion. In (c2), first delete the extra; the intermediate set contains S0, so its outside addition loses by (a). In (c3), deleting truth i creates Lambda_(T minus {i}) >= (n - 1)phi0² theta_i² >= L_n; SEP at that intermediate set yields Lambda_A >= (1 - c_S)L_n. Comparing to an extra deletion with zero residual gives the stated RSS margin and, with item 3, the required score ordering.

   At S0, additions lose by (a). For a truth deletion the exact nested identity is RSS_(S0 minus {i}) - RSS_S0 = (delta + sigma Z)². D3 bounds |Z| <= h_n using r_(S0 minus {i}); eventually |delta| >= 2 sigma h_n, so the lower bound Lambda/4 is legitimate. For any truth-for-null swap, including l outside V, H1a gives the Gram floor on A union {i} = S0 union {l}. Its Schur complement gives Lambda_A >= (n - 1)phi0² theta_i². Comparing r_A with r_S0 = 0 via L1.4 proves strict loss. SEP is not needed for this particular local-maximum swap bound. No missing outside-null case was found.

9. Neighbour coverage, termination, ties, and cap arithmetic: verified with item 1.

   Location: L3.4; L4.1 proof, lines 25–36.

   Problem checked: proving one improving move alone would not prove greedy closure. Here the designated move also strictly beats every possible outside neighbour.

   Verification/fix: at a missing-truth state, the outside possibilities are exactly add outside, swap truth out/outside in, and swap extra out/outside in. L3.2 covers all three. Every deletion and every add or swap whose entering variable lies in V stays in 2^V; their scores need not be bounded separately, even if a winning move removes a truth or adds a proxy. At a strict superset, extra deletion supplies an improvement; L3.3(c) covers outside additions and both classes of outside swaps. Truth deletions and all other swaps remain in V. At S0, (d) covers every feasible type. Thus every maximizer is inside V and strictly improving until S0; internal ties are harmless, and a tie with an outside model is excluded by the strict comparisons.

   Strict score increase prevents revisiting a subset of V. There are at most 2^vbar such subsets, so termination at the only non-improving state S0 occurs after at most 2^vbar - 1 moves. No monotonicity of symmetric-difference distance is used. The scan at the predecessor S^(tau - 1) scores S0, even if it is the extra scan at move count ell; hence ell >= tau - 1 suffices for discovery. The tau-th move and a complete scan at S0 require ell >= tau. For tau = 0 the emitted centre is already scored, and a scan certifies it even at ell = 0. These arithmetic and tie statements are correct, subject to the endpoint/public-flag distinction in item 4.

10. Hidden assumptions and dependence of n0: one small onset qualification.

    Location: L3:5–9, 29, 64–66; STATEMENT (H1b).

    Problem: line 29 lists dependence on constants and the BM-infinity envelope, but SEP is only assumed eventually and may start at an arbitrary sequence-specific index. Its onset is not bounded by those listed constants or by the BM envelope.

    Concrete fix: include the SEP onset n_SEP in n0, or state all assertions for sufficiently large n at which SEP holds and the displayed BM thresholds are satisfied. Include the eventual feasibility threshold from item 1. This is harmless for the asymptotic theorem; no uniform finite-n onset follows from eventual SEP alone.

    The other suggested hidden assumptions are unnecessary. Since V is nonempty and the normalized Gram matrix has trace equal to its dimension, H1a already implies phi0 <= 1. For fixed positive phi0 and sigma², a BM envelope b_n -> infinity gives

        L_n/log n >= sigma² phi0²(1 - 1/n)b_n -> infinity.

    Thus theta_min may tend to zero; fixed beta-min is not being used. The Gaussian and ridge constants in the L3 application depend on vbar as well as the listed fixed parameters. Neither the additional H0 sparse-eigenvalue conditions nor H2/block properties are required for this descent proof.

11. Counterexample attempts and relation to the earlier failures.

    Location: W1-T37R Theorem C(C3); 05_history.tex RF176; L3:108–112 and L4:38–42.

    Problem checked: a null proxy can beat every truth addition, and masked-LH region-form progress dominance can fail through exact ties. These invalidate stronger progress claims, but not the closure argument reviewed here.

    Verification/fix: in the combination-proxy example x3 = a(x1 + x2)/sqrt(2) + sqrt(1 - a²)z, a = 0.85, putting the proxy outside V = {1,2} violates SEP already at the empty set: its decrement exceeds each truth's decrement, hence also exceeds c_S L_n for every c_S < 1. Putting the proxy inside V = {1,2,3}, with other columns orthogonal, satisfies SEP with zeta = 0 and permits the initial proxy move while keeping the entire path in V. The theorem deliberately allows this. Likewise, RF176's ties between progress/non-progress alternatives inside V do not violate strict dominance over outside neighbours. Arbitrary correlations among outside columns do not supply a one-move escape because each scanned neighbour contains at most one such column, and swaps are controlled at the post-deletion subset by SEP. No design counterexample to the amended centre-path claim emerged. Do not strengthen it to per-move truth-distance decrease, a linear move bound, or unconditional dominance over arbitrary pre-search scored models.
