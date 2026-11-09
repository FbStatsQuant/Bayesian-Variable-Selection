# R02 — fresh statement-lock review (Codex Sol)

Verdict: **LOCK-WITH-CHANGES**.

The revised target is a credible statement-lock candidate, conditional on the required corrections below. I found no new asymptotic counterexample to the substantive discovery claim or to the revised best-deletion domination claim. This is not verification of C2: its uniform addition margin and growing-dimensional path control remain substantial proof obligations. Do not mark the statement unconditionally locked until these corrections are applied.

Reviewed STATEMENT v2 and PLAN against Wave-2 and its two predecessor protocols, the requested FINAL posterior/HPM/delivery/implementation sources, the SoP score/prior/block/start/search specification and shared premises, and the supplied diagnostic summaries and scanner/invariant scripts. Only this review file was written; no git state was changed.

## Required changes

1. **Define the interval endpoints for every retained set, including one-sided configurations.** Evidence: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:89-90,97-105`.

   The definition currently starts with “with retained nulls on both sides of x_T”. C2(iii), however, applies at every visited nonterminal set, including the penultimate set with exactly one retained null. Such a set cannot have nulls on both sides, so its a_T and b_T are outside the stated definition. This is a mandatory case whenever m0>0, not an exceptional event whose probability can be discarded. The parenthetical infinity convention suggests the intended repair but contradicts the domain restriction.

   Delete the two-sided restriction and define explicitly

   `a_T = max({xi_j : j in T\S0, xi_j <= x_T} union {-infinity})`,

   `b_T = min({xi_j : j in T\S0, xi_j > x_T} union {+infinity})`.

   State that the rank interval uses these extended endpoints and is asserted before each move, including the initial state; exclude exact equalities on the probability-one nondegeneracy event. This also covers an empty deleted interval initially and a half-infinite interval with one extra remaining. Do not replace the invariant by a requirement that both endpoints be finite.

2. **Correct the signed-coordinate energy bound in the automatic-H0 paragraph.** Evidence: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:65-69,77-78`; `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:6-12`.

   Sigma_n is defined as the signed Gram, while vartheta is already sign-corrected. Consequently the displayed choice `M > vartheta^T Sigma_{S0,S0} vartheta` need not bound the actual signal energy. For example, take s0=2, signs (+1,-1), original theta*=(1,-1), and hence vartheta=(1,1). FS holds. The displayed quadratic form is 2(1-rho), whereas `||mu||^2/(n-1)=2(1+rho)`. A fixed M strictly between these numbers satisfies the stated prescription and fails T03's energy hypothesis eventually.

   Introduce `barSigma=(1-rho)I+rho 11^T` and use `M > vartheta^T barSigma_{S0,S0} vartheta`, equivalently `M > theta*^T Sigma_{S0,S0} theta*`. Alternatively explicitly adopt the sign-corrected coordinates before this paragraph. H0 itself is automatic: all principal normalized eigenvalues are at least 1-rho, all corresponding unnormalized eigenvalues are at least (n-1)(1-rho), p<=n gives A=1, fixed nonzero coefficients give BM-infinity, and s0<=K eventually. The correction is to the claimed verification, not an obstruction to H0.

3. **Handle bounded p separately in the plan, and qualify the relevance-set exclusion.** Evidence: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:29-31,67,78-79`; `Theory_work/Wave2/W2-FAC-B/PLAN.md:11-16`.

   The statement explicitly includes bounded p, but the planned high-probability end-phase balance `|N_+ - N_-| <= 1` cannot hold for all such sequences if these are the positive/negative retained-null counts used in `numerics/n5_invariants.py:47-54`. Take fixed p=3, singleton blocks, one positive truth, and two nulls. At the initial set the two independent null xi's have the same sign with probability 1/2, giving imbalance 2 for every n. That initial configuration is already in the diagnostic's end phase (m<20). Fixed-coordinate order-statistic bounds cannot turn this into a probability-tending-to-one balance event.

   Add a bounded-p argument: null gain terms are O_P(1), addition/deletion size penalties have leading (1/2)log n, and truth losses are order n. Use the extreme-tail/end-phase balance argument only in its proved growing-p regime. For arbitrary p_n not necessarily convergent or divergent, state the subsequence argument or a uniform alternative. Eventual enumeration alone proves the reported-model consequence but does not prove the literal deterministic-path clauses C1/C2 that are also claimed for bounded p.

   Replace “Bounded or O(log n) relevance-set hypotheses ... are not satisfied” by “are not automatic on this class and do not cover the substantive p >> log n regime.” For bounded p, taking the relevance set to be [p] does satisfy its size requirement; the current blanket exclusion is false. This completes, rather than reverses, R01's request to distinguish H0 from relevance assumptions.

4. **Complete the diagnostic part of R01's invariant correction before claiming all seven requests are applied.** Evidence: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:4-6,103-104`; `reviews/R01_disposition.md:6-11,28-32` in the same ticket; `numerics/n3_cs.py:31-42`; `numerics/n5_invariants.py:33-61`; `PLAN.md:19-21`.

   N3 still checks only contiguity of deleted ranks. N5 checks nearest-point deletion, the centre drift identity, tail structure and imbalance; it does not compare the deleted set with the actual open gap `(a_T,b_T)` or assert `a_T < x_T < b_T` at each pre-move set. Thus neither directly falsifies the revised C2(iii). N5 also always initializes [p], so it does not exercise the N0 exclusion. Add a direct assertion of the revised invariant, including the initial state and one/two-extra states, and a truth-complete-block case started at S* with nonempty N0. The latter must keep N0 eligible for additions and swaps. Preserve these as diagnostics, not proofs.

   The scanner's lexicographic tie selection has been repaired (`numerics/cs_gain.py:62-77`, and the analogous cs_core block), and swap-minus-deletion is now the appropriate diagnostic for C2(ii). Those portions of R01 item 7 are applied. The direct revised-invariant test requested in R01 item 2 is still missing; the disposition should not imply otherwise.

## Substantive assessment and remaining proof obligations

- **C1:** The N0 exception is correctly motivated. FS makes the bounded-block increments nonzero when a truth is missing; once a block contains all truths its null increments are noise-only. Inclusion of truths and leakage nulls must be proved uniformly against the exact prior cost. Exclusion of the at most 15 N0 coordinates needs its separate noise-only argument. PLAN's one-flip summary is acceptable only with this separation, as the disposition acknowledges.

- **C2(i)-(iii):** Removing the swap log-n margin really resolves R01's fixed-p counterexample. For p=3 the remaining null swap can still have O_P(1) gain, while the best null deletion gains (1/2)log n+O_P(1); strict domination is compatible with that example. The displayed centre and k-free offset agree with the algebraic reduction in L1.4. Conditional on nearest-null deletion, the centre update is

  `x_{T\{j}} = x_T + (x_T-xi_j)/(k-1+kappa_n)`.

  Since k>=s0+1 and s0>=1, the denominator exceeds one. The shift away from the removed nearest point cannot cross the closest retained point on the opposite side. This supports the corrected extended-gap invariant, including its initial and one-sided cases. It does not establish score domination or the addition margin.

- **The addition margin needs its own path-uniform proof.** Reversing the preceding deletion only controls that particular re-addition; it does not control every omitted null at the newly shifted centre. In the growing-p end phase, write h=s0+kappa0 with kappa0=(1-rho)/rho. Under the proposed balanced extreme-tail asymptotics, at a set with one extra the largest opposite-tail addition has likelihood gain approximately `(h+2)/(h+1) log p`, against penalty `(1/2)log n+log p+O(1)`. Thus the worst leading gap when log p/log n approaches one is `1/2-1/(h+1)>0`. For s0=1 it becomes small as rho approaches one but remains positive for each fixed rho<1. This calculation does not refute C2(ii); it explains why fixed rho, balanced extremes and lower-order error control matter. It is conditional asymptotic bookkeeping, not a proof that the path satisfies those conditions. The two-extra state and N0 additions need explicit coverage as well.

- **Near k=n/2:** the available full-model residual dimension is n-1-p, approximately n/2 at the boundary. The exact residual and BB ratio must remain in the proof; no uniform replacement of RSS_T by n sigma^2 is justified. L1's all-size gain identities are an appropriate starting point. PLAN's proposed path-restricted control is plausible, but the required simultaneous tail-sum, imbalance and score inequalities have not been established by statement lock.

- **C2(iv), C3 and fidelity:** T03 concentration supplies the terminal strict-neighbour property at S0. The MR1 cap, extra complete scan, distinction between scoring and certification, deterministic exact-branch convention, all-scored HPM, K, and the two different tie rules now agree with the requested specification (`SoP/02_method.tex:463-470,480-500`; `FINAL/s7_impl.tex:38-48`). The legacy-cap miss statement is correctly restricted to the deterministic LS0 scored set. C3 uses [OP] in the correct direction.

- **C4:** The new-class-extension framing and CAL-free formulation are correct. The universal import of all Proposition-F premises includes CONFIG, fixed declared R'=4k and worker count, complete scans, fallback details and retention, even though the parenthesis is not exhaustive. The preflight time/archive amendment is expressly imported (`FINAL/s6_delivery.tex:29-44`). Verify Lemma S for CS and use T03 plus the new deterministic discovery event through D-prime/A2 step 3. Do not silently re-import GEN/GROW's statistical class restrictions or infer discovery from D_n->0. The implementation and unit-cost qualifications are retained.

- **Scope and prior disposition:** The FAC-CS name, exact-Gram restriction, substantive growing-p regime, corrected N1 exceptions, single-data-set interpretation of N2 and technique-only frontier language address R01 item 5. R01 items 1, 4 and 6 are substantively applied; item 3 needs the small corrections above; items 2 and 7 are only partly complete as described. No claim about general factor designs, random-row S5 or p>n/2 follows from this lock.

## Optional suggestions

- Drop auxiliary path invariants from the theorem if the proof ultimately needs only pure deletion and discovery within MR1; certify each stronger invariant separately if retained.
- In `cs_gain.py:60-61,80-81`, max_swap_gain is updated only after the stopping test. Move its recording before that test if it is meant to summarize every scan, including the terminal scan. The current statistic also is not exported by N3.
- Restore the protocol's “after the key lemma or about three hours, whichever is first” checkpoint trigger in PLAN, and put citation checking before council explicitly (`Theory_work/Wave2/PROTOCOL.md:31-34`; `Theory_work/Wave1C/PROTOCOL.md:29-30`).

The plan is viable after the bounded-p split and direct invariant tests. The appropriate next gate is an independent check of L4's actual inequalities; this review does not upgrade that lemma or FAC-CS to a proved status.
