Council seat A verdict: **PASS**. Uncapped score: **9.2/10**. All six gates PASS. No required fixes.

Reviewed STATEMENT.md v1.2 and 00_MAIN/L1–L8 against the cited local sources, numerical scripts and saved evidence. I formed my mathematical assessment before reading R01–R06 and their dispositions. I did not read LOG.md or coordinate with another reviewer. References below are relative to Theory_work/Wave2/W2-FAC-A unless another location is named.

1. **Gate 1 — Correctness of every step: PASS.**

   L1's Gaussian innovation decomposition is exact. The local innovation depends on T through U = T ∩ g(l); its independence from the residual-factor variable follows from the stated orthogonal Gaussian decomposition. The deterministic bound correctly dominates partial-group quadratic forms by full-group forms and uses s_T ≥ c_min h_T. The group-subset probability bound pays log binom(G,h) at each h; it does not apply an unpaid fixed threshold to exponentially many models. The perturbation proof controls regression vectors and Schur complements through the unit diagonal and spectral floor, without inserting the growing largest eigenvalue.

   L2 legitimately re-proves the Q = [p], K = p sandwich branch using bounded-size block events from GEN L1. It does not import GROW's logarithmic-size hypothesis. A missing truth gives a feasible, eventually positive start-weight improvement, uniformly over every maximiser.

   L3's determinant and ridge bounds are deterministic over all subsets. Its common RSS floor follows from the single full-design noise projection bound. The NA comparison retains the exact BB ratio and has a uniform strict margin. TL treats truth deletions and truth-removing swaps separately; the cross term is proportional to |θ_i*|√n times the Gaussian envelope, so BM-∞ suffices even for shrinking coefficients. L4 then correctly applies GROW L1.2, operational closure and posterior concentration.

   L5 supplies common design envelopes, a uniform bounded-dimensional partial-signal transfer and a valid diagonal argument for the posterior expectation. The block-CS κ calculation, whole-group partition lemma and exact S5 certificate are valid. The CS signal minimum now ranges over feasible configurations and absolute values.

   L6's noise-selected witness is legitimate under the universal lattice quantifier. Its order-statistic calculation gives Z² ≥ (8 − o(1)) log p, and the separate small-model score comparison gives 2ΔF ≥ (6 − o(1)) log p − log n − O(1). It uses the algebraic E1/E2 identities without importing Part I's subcritical full-model RSS floor. L7 correctly uses the deterministic discovery event 𝒦_n; it never reverses the inequality bounding D_n. L8's exact CS reduction, move identities and conditional GAP invariant are consistent; the remaining path argument is explicitly heuristic and unused by Parts I–II.

2. **Gate 2 — Hypotheses used equal hypotheses stated, per clause: PASS.**

   L1 uses the stated representation and Gram approximation. L2 uses G, energy, AG, P and TV. L3 additionally uses BM-∞ for TL, as supplied by H0. L4 retains TV and the named method premises; AG supplies the anchored eigenvalue conditions, while energy and beta-min remain actual assumptions in the general fixed-design theorem.

   L5 retains fixed nonzero coefficients on the standardised scale, independent Gaussian noise and TV-pop on a deterministic family covering the realised blocks. Its common-envelope design events support the joint-law conclusion. The CS instances retain GC-CS, and the S5 layouts have the required exact visibility certificate. Part II retains exact-Gram CS, fixed a, fixed signals and noise variance. L7 explicitly inherits the stronger delivery premises and complete allocation inequalities, including A4.

   L6 proves the additional range p ≤ n − 1 without needing the locked target's p ≤ K restriction. That strengthening is mathematically justified by its O(log p)-size witness and explicitly identified in its status note; it does not weaken a hypothesis silently.

3. **Gate 3 — No hidden assumptions: PASS.**

   No uniformly positive lower bound on c_min, bounded full-design largest eigenvalue, population partition equality, or independence among the lattice-indexed innovations is smuggled into the proof. κ is representation-dependent, and its upper bound is used consistently. The original-space event in Corollary U is distinguished correctly from the auxiliary latent event on the enlarged space.

   Response normalisation is accounted for in both the block-score expansion and lattice comparisons. TV/TV-pop exclude conditional signal cancellation explicitly; fixed nonzero coefficients alone are not substituted for visibility. The random-design transfer uses common envelopes and every deterministic design sequence, rather than pointwise conditional convergence.

   Delivery is expressly relative to the unit-cost exact-real/unbounded-word machine, MACH, CONFIG, e4/TDP-IMPL, complete fallback freezing and the enlarged raw-dimension allocation. The P1/S.3 audit qualifications remain visible. CAL, candidate restricted-ESS success and a bound on fallback probability are not covertly assumed.

4. **Gate 4 — Adequate cited-lemma status, quoted without upgrades: PASS.**

   The relevant source statuses are preserved:

   - M5(0)/T38-(0): “PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))”.
   - S-T/T03♯: “PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)”.
   - GEN and C-GROW headline results: “PROVED-CHECKED”; the reused operational closure and GROW descent lemma retain “PROVED (by this seat, unchecked)” together with their recorded checks.
   - Lemma CR/[CONC′]: “PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)”.
   - Proposition F's cap-ℓ_n form: “PROVED-CHECKED for the patched calibration law”; A1's corrected form has the separately identified final council check, and A4 retains “OK-WITH-FIXES”.
   - A2: “PROVED (A2), checked by A3”.
   - P1 and S.3 remain “AUDITED (code reading)”; N3's inherited “OPEN” qualification remains explicit in L7.

   I checked the relevant statements in GEN L1/L5, C-GROW L0/L1/L4/L6, PXN CR, FINAL s1/s3/s6, HQ A1–A4 and C-DLV's resource, degeneracy, grid and delivery lemmas. The FAC extension re-proves the new statistical class inputs; it does not claim that the older Proposition F already covered growing factor designs. Historical unmerged-code descriptions in the Wave 1C sources are not used to contradict the explicitly specified merged Wave 2 method.

5. **Gate 5 — Constants, rates and exponential-lattice uniformity: PASS.**

   Corollary U provides a deterministic simultaneous allowance with failure probability at most 4/log n. The class parameters bound κ′_bd uniformly even when c_min varies. The perturbation allowance is O(δ_n√(p log log n)) = o(1), and the remaining envelope error is o(√log n), hence contributes o(log n) after squaring.

   Writing P = log p and x_k = log(p/k), the leading squared envelope minus the prior contribution is bounded by 2P max_{0≤r≤1}[(1 + κ̄r)² − r²]. For κ̄ ≥ 1 the maximum is κ̄(κ̄ + 2), giving α₀ = 1/[2κ̄(κ̄ + 2)] and α₀(1) = 1/6. The strict limsup condition supplies uniform slack; bounded and subpolynomial p are covered by the same log-log allowance, with p = 1 handled vacuously for NA. P also implies p = o(n) and K = p eventually.

   The random-row rate p^(3/2) O(√(log n log log n/n)) vanishes under the stated exponent. The S5 minima are positive exact fractions, 2023/32500 and 7/2080, scaling by c². No expectation rate is inferred from the posterior O_P statement.

6. **Gate 6 — Fidelity to the coded/specified method: PASS.**

   The argument uses the shipped ridge score, IG(0.01,0.01), exact capped BB ratio, actual bounded-size blocks, complete neighbour scans, strict score improvement and the reported maximum of all scored models. The merged LS0 cap is ℓ_n + |S̃₀|; all other caps remain ℓ_n.

   I checked the current code's cap construction and LS0 invocation in Scripts/SMC_BVS/core/cpp/v3_core.cpp:469–480, complete-scan/move-cap semantics in cpp/v3_engine.h:379–425, whole-cluster cutting/packing in cpp/v3_blocks.h:121–140, and fallback recording/freezing in v3_calib.R:120–186. The A4 preflight terms are reflected in v3_fit.R:43–65. The theorem correctly distinguishes reaching S₀ after τ moves from scoring it in the scan after max(τ − 1, 0) moves, and distinguishes the uninterrupted deterministic search from an actual delivered SMC execution or exact enumeration.

**Honesty of scope: PASS.** The replacement of arbitrary polynomial growth and fixed global rank by one global factor with bounded local groups and limsup log p/log n < α₀ is explicit and substantial. It is not presented as solving the original broad brief. Sharpness is confined to full-lattice NA for exact-Gram CS, with no boundary claim and no implication of method inconsistency. Necessity for S5, random rows or approximate Grams is not asserted. Part III remains evidence/conjecture only. All statistical conclusions are assessed asymptotically; finite-n onset is not scored as a limitation.

**Independent checks actually run.** Using py -3.13 -B with an in-memory script from the Windows temporary directory, I checked 12,288 subset/addition pairs for heterogeneous signed-loading factor designs: maximum decomposition error 2.23 × 10^−15 and zero violations of the final deterministic κ-bound. Perturbed noncommuting correlation matrices also satisfied the stated Lipschitz allowance; the maximum observed discrepancy-to-bound ratio was 0.00205. A separate coefficient-symmetry rational enumeration reproduced the S5 minima: 11,060 configurations for s₀ = 4 and 74,890 compressed configurations for s₀ = 14. The two study spacings are equivalent under group/within-group permutations. I also checked the exponent maximisation for κ̄ = 1, 1.1, 1.5, 2 and 4. These are supporting checks, not substitutes for the probability proofs.

**Review-trail audit.** After forming my assessment, I checked R01–R06 and their dispositions against the current files. The substantive fixes are present: exact S5 certification, feasible CS minima, corrected K = p feasibility, normalisation, original-space coupling events, delivery allocation, and the narrowed frontier/evidence wording. The approximate n = 10¹² FNA sampling branch is disclosed in the current summary and L6. I found no unresolved required finding or dishonest disposition.

**Required fixes:**

1. None.

**Optional suggestions:**

1. Update 00_MAIN.md's opening target-version reference from v1.1 to v1.2.
2. Put the approximate-sampling disclosure into fna_check.py's generated summary header as well. The checked-in FNA_summary.md contains it, but running the current writer would overwrite that note.

This is seat A's independent passing verdict; the combined council result still requires the other seat's verdict.

