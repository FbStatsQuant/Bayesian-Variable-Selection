# R01 — statement-lock review (Codex Sol)

Verdict: **REJECT** the v1 statement as written. A clause of C2 is false even in a fixed-dimensional member of the stated class. This does not refute reported-model consistency, C1, or a suitably weakened pure-deletion theorem. The proposed exact-Gram compound-symmetry subclass is meaningful, but its growing-dimensional path theorem remains a proof obligation.

Reviewed against the requested method and FINAL sources, Wave-2 protocol and its predecessor protocols, C-GROW conventions/frontier, and the supplied diagnostic summaries and relevant scanner/start scripts. Numerics are treated as diagnostics only. No production-code or theorem file was edited.

## Required changes

1. **Remove the logarithmic margin for every swap in C2(iii); it is mathematically false.** Evidence: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:75-80`, especially line 79.

   Counterexample: take fixed p=3, S0={1}, coefficient 1, any fixed rho in (0,1), sigma squared 1, no sign flips, and singleton blocks. These are also the actual blocks: the method's B is floor(sqrt(3))=1 (`Theory_work/State_of_Project/sections/02_method.tex:149,205`). Exact centred designs exist for all sufficiently large n; P, theta and FS hold, N0 is empty, and S*={1,2,3}. Each singleton has nonzero population signal, so its start inclusion has an order-n advantage over the order-log-n penalty; C1 gives the full start here.

   In this fixed-dimensional problem, removing a truth loses order n, deleting a null gains (1/2) log n + O_P(1), and a null-for-null swap changes the score by O_P(1). Thus the first move deletes one of nulls 2 and 3 with probability tending to one. Write A={1,2}, B={1,3}. Their prior terms cancel exactly, as do their determinant terms, because their sizes and Gram spectra agree. Both contain the truth, so their RSS difference is O_P(1) on the unscaled response and their score difference F(A)-F(B)=O_P(1). The first deletion selects the better of A and B. At that visited centre the feasible swap to the other set therefore has gain

   `-abs(F(A)-F(B)) = O_P(1)`.

   For every fixed c>0, the probability that this gain is at most -c log n tends to zero. Consequently no events E_n with probability tending to one can satisfy C2(iii) as stated. This is an asymptotic counterexample, independent of numerical precision. The exact-branch convention permits this deterministic search even though the fit eventually enumerates all models (`Theory_work/Wave1C/FINAL/sections/s7_impl.tex:46`).

   Separate addition margins from swap statements. For pure deletion it suffices to prove that every competing neighbour has score below the best improving null deletion; a log-n gap below the current centre is unnecessary for swaps. If strict non-improvement of all swaps is retained as an additional claim, it needs its own proof and a compatible, potentially vanishing gap.

2. **State and test the actual path invariants, rather than treating the N3 diagnostics as evidence for the whole of C2.** Evidence: `STATEMENT.md:77-79`; `PLAN.md:11-16,19-21`; `numerics/n3_cs.py:27-47`; `numerics/cs_gain.py:58-59`, all under `Theory_work/Wave2/W2-FAC-B/`.

   N3 tests contiguity of deleted ranks. It does not test whether the current centre x_T lies in a defined deleted interval, whether every swap is non-improving, or the proposed end-phase count balance. Its swap statistic is best-swap minus best-deletion, not best-swap minus F(T). These are materially different claims. Define xi and x_T in the locked statement or a precise referenced definition; define the interval as a rank interval or an open gap, specify which pre/post-move centre is used, and handle the initial and first-deletion states. Literally the convex hull of a single deleted coordinate cannot contain a continuously distributed centre with probability one.

   L4 must address s0=1 and rho close to 1, the last one/two extras, omitted N0 coordinates that remain eligible for additions/swaps, and k near n/2. Keep the exact BB ratio `(k+1)/(2p-1-k)` and the actual RSS in the inequalities. At k proportional to n the noise residual dimension is approximately n-1-k; replacing it uniformly by n is invalid. At small k the prior penalty includes log p, which is essential to the end-phase comparison. A new path-restricted proof is plausible after weakening item 1, but GEN/GROW's existing bounds for bounded or O(log n) relevance sets do not supply it (`Theory_work/Wave1C/FINAL/sections/s5_hpm.tex:46,52,63,69`). Do not use their small-set score expansion across the full path without proving an extension.

3. **Keep FS, but write its exact signed increment and distinguish sufficiency from equivalence; delete the claim that relevance-set hypotheses are automatic.** Evidence: `STATEMENT.md:54-66`; `PLAN.md:9-10` in the ticket; `Theory_work/Wave1C/C-GROW/STATEMENT.md:84-98`.

   With sign-corrected columns, U disjoint from l, u=|U| and V=S0\U, the population partial covariance is

   `(1-rho) [vartheta_l + rho*vartheta(V)/(1+(u-1)*rho)]`,

   where vartheta_l=0 for a null. For the original signed column multiply by its column sign. Here covariance means the Sigma-scale partial inner product; the design inner product has an additional factor n-1. This verifies the proposed algebra and shows that FS(a) controls null increments when V is nonempty, and FS(b) controls truth increments. When U contains all truths, V is empty and a null increment is zero: FS does not make these increments visible. This explains the N0 exception and makes C1 plausible. FS is a sufficient generic condition over a possibly larger collection than realizable block triples, rather than a necessary condition for each actual partition.

   L2 must separately show exclusion of N0 by its bounded number of noise-only increments, and inclusion of truths before concluding the global maximizer is S*. For positive increments, uniform sample error and the order-log-p prior cost must both be controlled. A blanket one-flip-positive argument cannot apply to truth-complete null increments.

   The H0 sparse-eigenvalue and beta-min requirements are automatic here: choose A=1, phi0 squared=1-rho, a fixed positive g0 below the eventual unnormalised Gram floor, and M larger than vartheta-transpose Sigma vartheta. Every principal normalized Gram has minimum eigenvalue at least 1-rho, including the anchored sets in SE_w; fixed nonzero coefficients give BM-infinity. Spell out this verification and s0<=K eventually. **Bounded/O(log n) relevance-set hypotheses are not automatic**: pervasive leakage is precisely why this ticket needs a new route. Replace lines 65-66 by the H0 claim alone. Use a different name for the diagonal sign matrix, since D_n is already the discovery-failure probability in C3.

4. **Frame C4 as a new extension using Proposition F's delivery machinery and A2's argument, and remove the CAL ambiguity.** Evidence: ticket `STATEMENT.md:47-49,84-90`; `PLAN.md:17-18`; `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:29-46,54-56,62`.

   F/F-GROW do not already include growing-p compound symmetry outside GEN/GROW. Their allocation and total-fallback machinery can be reused, but the class extension must verify Lemma S for these designs and then combine posterior concentration with the new deterministic LS0 discovery event. PLAN already identifies this correct K_n route; promote it to an explicit proof obligation. Do not infer discovery from D_n tending to zero: [OP] has the opposite inequality (`s5_hpm.tex:5-9`; `s6_delivery.tex:56`).

   Import **all** of F's premises and amended allocation, including the additional LS0 preflight time/archive terms at `s6_delivery.tex:37-44`, not merely the original C-DLV envelope or A1's earlier correction. Preserve the qualifications that exact arithmetic/unit-cost resources and the exit audits are assumptions/statuses, not verified reliability of the binary. C4 currently invokes the hypotheses of C3, whose premise list includes CAL, and then says CAL is not used. State C4 under the statistical hypotheses plus the CAL-free Proposition-F premises and the newly proved path event; do not require C3's CAL premise by reference.

5. **Make scope and frontier assertions match the evidence.** Evidence: ticket `STATEMENT.md:15-30,91-95`; `PLAN.md:25-26`; `Theory_work/Wave2/PROTOCOL.md:15-18,31-34`; `Theory_work/Wave1C/C-GROW/STATEMENT.md:135-156`.

   Exact-Gram CS with p up to n/2 is a nonempty, genuinely pervasive one-factor class and allows p much larger than log n. It is an acceptable meaningful subclass, provided the theorem is called FAC-CS and never presented as covering random-row study S5 or general factors. Fixed-p cases add no discovery coverage beyond eventual enumeration (`02_method.tex:167-170`); identify p much larger than log n as the substantive regime. Replace prospective wording 'fully proved' at statement line 28 by 'targeted for proof' until the pipeline passes.

   Correct the diagnostic assertion that every N1 run at n>=10^6 has a full start. The supplied summary contradicts it: F2,p=200,c=0.5,n=10^6 has size 193 and 0/5 full starts (`numerics/N1_summary.md:111`); S5,p=400,c=0.5,n=10^6 has size 396-397 and 0/3 full starts (`:167`).

   N2's single data set demonstrates a cap failure for that diagnostic, not an asymptotic impossibility for all p>n/2. Its own summary says so (`numerics/N2_summary.md:10-11`). Loss of the one-dimensional reduction, or the fact that a sample Gram is not exactly CS, is an obstruction to this proof technique, not a proved obstruction to consistency. Label these separately. If an exact asymptotic obstruction for an excluded class is promised, supply a checked counterexample/necessary-condition proof or report it as unresolved. A larger cap is a proposed response to the observed swap phase, not yet a sufficient remedy.

6. **Restore the complete search/branch contract in the setting and keep certificates local to the claimed endpoint.** Evidence: ticket `STATEMENT.md:43-49,81-83`; `Theory_work/State_of_Project/sections/02_method.tex:463-470,483,490-506`; `Theory_work/Wave1C/FINAL/sections/s7_impl.tex:38-48`.

   Define ell_n=ceil(log2(n+p+1)); say that a cap a permits a moves followed by one complete further scan and that every scanned neighbour joins the scored set. This extra scan is why 'scores S0 at a>=d-1' is correct while certification requires a>=d. State the deterministic search on every admissible branch and distinguish it from actual execution; on the exact branch enumeration supplies discovery. The production-cap miss assertion concerns this deterministic LS0 scored set, not failure of the full fit.

   The method's start/HPM ties are size-then-lex; scan-neighbour ties are plain lex, with moves only on strict score increase. The current neighbourhood and K definitions agree with the method. Describe 'certified at S0' as a certified search endpoint, without promising the public local_certified flag for the final reported HPM. Also call ell_n the legacy/unaugmented LS0 cap in this comparison: MR1 is already the production target in this ticket.

7. **Fix the diagnostic scanner's fidelity claims before using it to validate revised lemmas.** Evidence: `Theory_work/Wave2/W2-FAC-B/numerics/cs_gain.py:63-74`; `numerics/cs_core.py`'s move-selection block; `numerics/n3_cs.py:27-47`; method tie rule at `02_method.tex:483`.

   cs_gain explicitly takes the first candidate in deletion/addition/swap order on a floating-point tie; it does not implement the production lexicographic rule. Its deletion branch constructs an unused opts list, and taking the first ascending deleted index generally gives the lexicographically larger resulting set. cs_core likewise selects opts[0]. Either implement the prescribed tie rule in these diagnostics or qualify the claim of identical search rules and restrict comparisons to demonstrated tie-free runs. Neither zero observed ties nor a diagnostic self-test proves exact-arithmetic fidelity. Add best-swap-minus-current and the precise revised invariant to the recorded quantities; the existing swap-minus-deletion statistic can validate domination but cannot validate C2(iii).

## Optional suggestions

- Lock the minimal useful theorem first: C1, H0, and discovery within MR1 via best-deletion domination. Treat stronger rank/centre and strict-swap assertions as auxiliary lemmas only if required.
- Record constants' dependence on the fixed rho and signal vector. The endpoint margins may deteriorate as rho approaches 1; the stated class fixes rho, so no uniform-in-rho claim is needed.
- Preserve the existing review pipeline after revising the target. In particular, the key L4 lemma needs independent checking before assembly; numerical path success alone does not validate its inequalities.

The rejection is based on the analytic asymptotic counterexample in item 1, not on a numerical run. The available default Python lacked NumPy, so the supplied NumPy diagnostics were not rerun for this review.
