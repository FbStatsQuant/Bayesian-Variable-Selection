# R06 — Independent mid-point review

**Verdict: CONTINUE.** No FATAL or MAJOR issue found. The locked target is appropriate, the method is faithfully specified under its named implementation premises, and the proof architecture supports continuing to exhaustive review and council. The issues below are local repairs; none requires changing the theorem, the dimensional regime, or the method.

Reviewed independently from W2-FAC-X STATEMENT v3 and X1–X6, W2-FAC-B STATEMENT v3.1 and L1–L5, and the Wave-2 protocol and its inherited protocols. I also checked the cited method, posterior-theorem and delivery statements in the SoP/FINAL sources. I did not read any reviews-folder contents, LOG.md, PLAN.md, CHECKPOINT.md or REPORT.md. X7 was not needed. Status assertions in proof-file headers were not treated as evidence of correctness.

## Target and method

The target addresses the substantive missing step between exact-Gram CS and iid Gaussian CS rows. Raw coefficients are fixed while the standardised coefficients are random; X5–X6 correctly condition on the raw design to handle this distinction. The mean of the rows disappears on centring, and the sign-flip reduction preserves the absolute-correlation partition and all relevant scores.

The score, BB(1,p) prior, size cap, full-response block tables, emitted start-mode centre, strict-improvement move rule and LS0 cap agree with the specified method. The proof does not replace the full score by RSS: X1 controls the determinant, ridge and Q-versus-RSS differences. The larger cap is already part of the target method. Delivery retains Proposition F's total fallback, implementation premises and amended allocation. Thus (C4) is the stated conditional method theorem, with the inherited qualifications, rather than an unqualified claim about arbitrary allocations or implementations.

The generic no-cancellation assumptions are explicit. The theorem does not silently cover masked truths, arbitrary loadings, or the excluded dimension frontier. The sufficient absorption criterion is correctly distinguished from a necessary condition. All statistical conclusions are assessed in the binding asymptotic scope.

## Assessment of the proof architecture

* **X1:** The rotation is an exact joint-law construction. Conditional laws in the rotating orthogonal frame justify the independence of the Gaussian coordinates and Wishart Gram matrix. The Schur identities for q, RSS and the partial statistics are consistent. The reference centre has a set-independent offset and the exact drift needed downstream. The score corrections have the required absolute scale.
* **X2:** The concentration argument is over interval families determined by xi alone, before any adaptive search is selected. Arbitrary band membership is then bounded deterministically by entrywise Wishart control. This avoids conditioning on a selected path as though it were independent of W. The second-order resolvent term is controlled under p < n^(1/2), and the band term can be absorbed because p Hbar sqrt(log n/n) tends to zero. The n^(-1/3) floor absorbs the logarithmic count remainder. One-move closure with at most 17 exceptional indices covers the neighbour statistics, including swaps.
* **X3:** The crossing estimate, distinction between the narrow and wide phases, and prefix formulation supply the required soft hole invariant without assuming future deletions. The exceptional last two kept nulls are handled separately by sparse/end-phase arguments in X4. I found no uncloseable accumulation of deletion errors.
* **X4:** The induction can be read in the stated dependency-table order: established deletion prefix gives band structure, which gives perturbation control and the approximate rule for the best-deletion candidate; B1 then B2 then B3 give the bulk centre bound, and gain comparisons identify the actual move. In the bulk, the restricted dimensional regime gives negative additions even for arbitrary omitted nulls N, and also after a hypothetical deletion; the swap comparison by decomposition is valid. At end-phase entry, D7 bounds the endpoint ranks and D8 eliminates band defects, recovering exact tail sets. The hypothetical-candidate argument avoids assuming the move before proving it. The end-phase margins dominate the O(varpi Hbar + Hbar^6/n + 1/n) score perturbations. Truth-removing moves have an order-n signal loss uniformly over the relevant supersets.
* **X5–X6:** The random partition is dealt with correctly in two distinct places. X4 holds on a common event for every omitted set N of size at most 15; X5 conditions on the raw design for the finitely many zero pairs in the realised truth block. Neither step assumes N0 independent of xi. X6 uses a raw-design event with common constants and an every-deterministic-sequence argument, rather than inferring unconditional convergence from pointwise conditional convergence. Discovery, the cap/prefix argument, output-conditioned consistency and the CAL-free delivery route then fit together.

I found no structural reason to redirect or stop. In particular, the locked theorem does not require exact ordering of null deletions, negative swap gains relative to the current model, or no-addition over arbitrary nonvisited sets. Those stronger statements would not follow from this argument, and are not asserted here.

## Numbered issues

1. **MINOR — The early template-transfer sentence overstates what a compact bound on kappa supplies.**

   **Location:** `lemmas/X1_representation.md:72–75`; compare `lemmas/X4_path.md:234–248` and FAC-B L4.4.

   X1 says all FAC-B arguments use only the displayed compact range for kappa, the offset bound, drift and scan structure. The specific end-phase constant c_D = 1/2 - 1/(s0 + 1 + kappa_infinity) also needs kappa = kappa_infinity + o(1). A compact range containing kappa_infinity/2 alone does not preserve that particular constant. X4 does supply the stronger fact from D3, so this does not invalidate the theorem.

   **Fix:** Restrict X1's sentence to the algebraic/geometric template and explicitly defer preservation of c_D to D3 and X4.5. Retain the distinction between the perturbed score formulas and FAC-B's exact formulas.

2. **MINOR — Make the end-phase sign/separation invariant explicit when importing FAC-B L4.4.**

   **Location:** `lemmas/X4_path.md:218–239`.

   The no-crossing calculation and the use of Top_+(N_+) and Top_-(N_-) at subsequent steps require retained positive values to remain above x and retained negative values below x, including one-sided configurations. FAC-B spells out this extra centre bound; X4 currently leaves it inside the phrase that L4.4 applies verbatim. It follows from the present hypotheses, but should be displayed before the hypothetical deletion argument.

   **Fix:** Put B = sum_{S0} xi - varrho = O(L_n), m = |K|, and write

       |x| <= (m Hbar + |B|)/(m + s0 + kappa),
       Hbar - |x| >= ((s0 + kappa) Hbar - |B|)/(m + s0 + kappa)
                    >> delta_e + varpi,       m < m1.

   Here Hbar/m1 >> delta_e + varpi and |B|/Hbar -> 0 uniformly in regime (L). Since every retained magnitude is at least H - delta_e >= Hbar - 2 delta_e, this establishes the sign/separation assertion, and the one-sided cases follow as well. Use this as an explicit invariant at entry and after each established deletion. This is a short completion of the existing argument, not a new assumption.

3. **MINOR — Supply the rate behind the unit bound on the sum of deleted negative values in Case B.**

   **Location:** `lemmas/X4_path.md:157–160`.

   The displayed deduction s_D >= -w times #(nulls in (-w,0)) >= -1 uses more than a count being negligible relative to m0: it uses w times that count tending to zero. This is true under the locked regime but currently unstated.

   **Fix:** After applying D6, record

       w #(nulls in (-w,0)) <= C p w^2 + C w log n = o(1).

   Indeed, w = O(Hbar sqrt(p log n/n) + n^(-1/3)), so

       p w^2 = O(p^2 Hbar^2 log n/n + p n^(-2/3)) = o(1)

   under p <= n^A1, A1 < 1/2, while w log n -> 0. This justifies the stated unit bound without strengthening the hypotheses.

## Independent falsification and disposition

As an additional check, an inline standard-library Python calculation used 20 seeds, 600 distinct Gaussian coordinates per seed, tolerance 0.002 and kappa-prime 1.3. At every step it selected the farthest currently admissible approximate-argmin deletion, checked the initial Q/size hypothesis, and checked X3's two-sided band containment through the prefix ending with two kept points. All 11,960 deletions passed. No script or numerical-output file was written; the tool-run result is recorded here. This checks one deterministic mechanism and is not evidence for the full statistical theorem.

**Disposition:** Continue with the same locked target and architecture, incorporate the three local clarifications, then perform the required exhaustive sweep and council. No issue of severity MAJOR or above was identified. This review is a mid-point continuation decision, not an upgrade to PROVED-CHECKED.
