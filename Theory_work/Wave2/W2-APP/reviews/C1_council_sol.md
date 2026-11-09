Gate verdicts

- G1 — FAIL. I found no mathematical defect in POST, CT/CD, the LOC window argument and its delta proof, LOC-B with the enlarged-Q condition, or VN and its four population examples. However, the applicability map incorrectly labels a provable growing-block subregion “unproved” (issue 1), and the polynomial-decay summary cells omit the qualification needed for their non-membership claim (issue 2).
- G2 — FAIL. The detailed polynomial non-membership argument assumes a uniform polynomial lower tail and p → ∞; the summary row does not state those hypotheses. The hypotheses used by the new positive proofs otherwise match their statements.
- G3 — PASS. The substantive proofs explicitly retain Gaussian rows, independent Gaussian noise, fixed sparsity/coefficient bounds, uniform spectral/locality constants, PTV or visible-null floors, and the named implementation premises. I found no additional hidden assumption in their arguments.
- G4 — PASS. The principal inputs have adequate recorded checks, and their status strings retain the source qualifications: T03♯, M5(0), GEN/GROW/PXN/MIS, GROW L6, SL0/SL1 and [OP]. CITECHECK is appropriately described as a location/status check, not mathematical verification. The dangling numerical filename in issue 4 should still be repaired.
- G5 — PASS. The logarithmic cutoff, Weyl error O((log n)^{3/2}/√n), explicit CT/CD constants, window radius, polynomial family counts, uniform innovation comparison and NA threshold have the required asymptotic margins. VN correctly requires nκ_n/log n → ∞ and distinguishes the GEN and GROW obstruction regimes.
- G6 — FAIL for the map as delivered. The positive proofs use the shipped LS0 cap and complete-scan rules faithfully, but the stated “unproved” frontier omits an applicable branch of the coded method (issue 1). The numerical certificate wording also needs the distinction in issue 3.

Score: 8.2/10. Council verdict: NOT PASSED, because not all gates pass. This score is independent of the gate requirement; it reflects that the core new proofs appear sound and the substantive required correction concerns the applicability map.

1. MAJOR — lemmas/L4_families.md:124; REPORT.md:58 and :69; STATEMENT.md:91 — The claimed unproved intermediate region includes sequences already covered by POST plus the coded exact-enumeration branch.

   Take s₀ = 1, a fixed nonzero coefficient and fixed noise variance, and two independent equicorrelated blocks with ρ = 1/2, each of size g_n = floor(0.6 log n); put the truth in one block and p_n = 2g_n. All relevant population floors are at least 1/2, and PTV is automatic. Q⁰ is the truth block. Since p_n < 2|Q⁰| + 32s₀ + 1, the stated enlargement gives Q = [p_n]. Thus (p_n − s₀)/log n → 1.2: the enlarged-Q LOC-B bound fails for every fixed δ₀ > 0. Also g_n/log n → 0.6, so the VN superlogarithmic sandwich obstruction does not apply. This is expressly inside the region the map calls unproved.

   Nevertheless, K = p_n eventually, so |Ω| = 2^{p_n}. The production decision is |Ω| ≤ (5H₀ + 4N₀)p_n, with N₀ = max(2500,n,p_n), H₀ = ceil(512N₀/2500) (Scripts/SMC_BVS/core/v3_preprocess.R:18 and :25). Here the threshold is asymptotic to 5.024np_n, while

   2^{p_n}/(np_n) ≤ n^{1.2 log 2 − 1}/p_n → 0.

   Therefore the actual method eventually enumerates all models (v3_fit.R:120), scores S₀, and its reported HPM is consistent jointly with output by POST and the usual posterior-mass comparison. This is an asymptotic conclusion and needs neither a new LS0 argument nor FAC.

   Fix: add an enumeration override to the reported-model map: whenever the coded counting inequality holds eventually, POST supplies reported-HPM consistency jointly with output. At minimum, include p_n ≤ c log n for fixed c < 1/log 2, under POST's other hypotheses. Restrict “unproved” growing-block/factor/Toeplitz statements to the remaining regimes. Keep “LOC-B does not apply” separate from “reported-model consistency is unproved.” The existing GROW source already distinguishes enumeration from the LS0 mechanism; this correction requires no change to LOC-B itself. Independent arithmetic and the asymptotic exponent are recorded in reviews/C1_scratch_sol/independent_checks.txt.

2. MINOR — REPORT.md:55; lemmas/L4_families.md:158 — The summary claims Σ ∉ LOC for “polynomial decay / long memory” without carrying over the detailed lower-tail and dimension qualifications.

   The actual argument at L4:86–91 uses |γ(h)/γ(0)| ≥ c′h^{−β} uniformly, and p → ∞. A polynomial upper envelope alone does not exclude LOC: AR(1) with ρ = 1/2 satisfies 2^{−h} ≤ 2.25/(h+1)² for every h ≥ 1, has a fixed spectral floor, and belongs to LOC. The body has already supplied the appropriate narrower non-membership statement; the tables should match it.

   Fix: label that row “two-sided polynomial tail (uniform lower bound), p → ∞,” or change the LOC cell to “not implied by a polynomial upper envelope; excluded under L4(c)'s lower-tail condition and p → ∞.” Apply the enumeration override from issue 1 to its reported-model cell as well. This is a summary qualification repair, not a defect in the detailed counting proof.

3. MINOR — REPORT.md:27; numerics/LEAD_READING.md:30; numerics/n3b_fastls.py:105 — The headline aggregates screened-search flags as “certified endpoints.”

   LEAD_READING:10–12 correctly discloses that sixteen runs screen swaps, rescore only candidates near the approximate maximum, and have unverified decisions. In n3b_fastls.py:82–106, certified=True consequently means no improvement among the retained/rescored candidates; there is no saved error bound establishing that every screened-out neighbour is worse. The three validation paths do not establish that property for the other runs. The stored 52/52 endpoint/flag totals are accurate as logged, but “certified” has a stronger complete-neighbourhood meaning in the method and theory.

   Fix: say “reached S₀ in all 40 VN-example runs; sixteen used screened search and reported a certification flag without a complete-scan certificate.” Separate the exhaustive-port and screened totals. Alternatively, fully score the terminal feasible neighbourhoods to certify endpoints, and validate any further claim that the screened trajectories equal the complete-search port. Preserve the existing disclosure that these are component-port observations, not production runs. This does not undermine the asymptotic proofs or establish method failure.

4. MINOR — REPORT.md:94 — The evidence row cites numerics/vn_onset_out.txt, which does not exist.

   Fix: replace it with the intended existing script/output, apparently numerics/vn_bound_recheck.py and numerics/vn_bound_recheck_out.txt. Extend the deliverable/citation check to catch named evidence files rather than merely the directory or selected token checks. The existing VN proof and R04 review remain available, so this is not a missing-proof objection.

Score sensitivity: issue 1 is the material score-changing correction; issues 2–3 also affect the assessment of the map and numerical conclusions. Correcting 1–3 throughout the statement, map and report would support reconsideration around 8.8/10 with all gates passing, subject to checking the actual revision. Issue 4 alone would not change my numerical score.

Independent checks: reviews/C1_scratch_sol/independent_checks.txt records an exhaustive 512-conditioning-set check of CD on a non-Markov MA(2) matrix, the exact-branch counterexample arithmetic, and reconstruction of the n2/n3 stored outcome totals. I also compared the diagnostic core copy with the current production files: all 18 executable/source files match; README.md and source_manifest.json differ. The Part 2 eigenvalue/partner/block totals agree with the supplied summary outputs. Its local/factor/near-collinear classifications are acceptable as descriptive resemblance statements, with the stated digits and tecator qualifications; they do not establish population floors or conditional visibility.
