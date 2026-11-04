# Synthesis: HPM versus BFDR for SMC-BVS v3 (lead, Opus 5.5, 2026-10-20)

Consultants: O1, O2 (Opus 5.5 high, Plan agents; O1_reply.md, O2_reply.md); A1, A2 (GPT-6 Astra high; astra1/reply.md session 01a159a9-ace5-7fe0-beef-bfa68ce568ea, astra2/reply.md session 01a159a9-ace8-7d03-a437-ec14a1836f22). One independent round; no second round because all four agree on every substantive point. The lead's view written before the replies is LEAD_PRIOR_VIEW.md; the replies confirm it and add the items marked NEW. Everything is a conjecture.

## Unanimous conclusions
1. Theory of the reported output becomes harder, not easier. The HPM is guaranteed by scoring alone (T21, T11(vii)): one score of the truth suffices; no mixing, no PIP accuracy. A BFDR set is a function of the estimated PIPs and inherits the hard half of Part C (T23/T24/T26, no Monte Carlo rate at the actual budgets). NEW (O1): any hypothesis set that gives the BFDR guarantee through T23/T26 also gives the HPM guarantee, not conversely. BFDR is also undefined under `schedule_limit`, where the HPM still exists.
2. Target side: different, not easier. Posterior expected FDP ≤ q is trivial by construction; everything else is a corollary of T03 like the HPM's results.
3. Fixed q breaks exact recovery by design: with perfect PIPs the rule admits ⌊qs₀/(1−q)⌋ nulls; at q = 0.1 it is consistent only for s₀ ≤ 8, knife-edge at s₀ = 9, over-selects for s₀ ≥ 10, and which nulls enter is decided by Monte Carlo noise among near-zero PIPs.
4. BFDR does not close the log n gap of g = n (T05); that gap belongs to the posterior, not to the decision rule.
5. Where BFDR helps: weak or transitional signals when several strong ones exist (budget borrowing), and an honest posterior error statement. It is worse under duplicates and correlated proxies (PIP dilution drops whole proxy groups; HPM keeps one member).
6. Recommendation: keep the HPM as the decision; if anything, add a secondary, constant-free report computed from primary PIPs.

## NEW results worth keeping (checked by the lead)
- Lemma L (O2): for any reported set D, |FDP(D) − postFDP(D)| ≤ max_j|PIP_j − 1{j∈S₀}| and FDP(D) ≤ postFDP(D) + max_{j∉S₀}PIP_j. It gives a frequentist reading to the posterior FDP of the HPM itself, so BFDR's main selling point is available without changing the decision.
- BFDR can exceed the cap: k̂ ≤ K/(1−q) (O2, A1, A2).
- Constant-free alternatives meeting Felipe's no-arbitrary-constants rule: (a) report the whole posterior-FDP path over PIP-ordered prefixes (O1, A2); (b) the ½-PFER set, longest prefix with Σ(1−PIP) < ½: posterior P(no false discovery) > ½ by Markov, contained in the MPM, consistent for every fixed s₀ (O1, O2); (c) HPM-anchored q̂ = postFDP(Ŝ) (O2). A vanishing q_n = 1/log(n+p+…) (O1, A1, A2) is consistent but is a convention, not a principle.
- Implementation note: the boundary test vector (0.95, 0.85, 0.2) sits exactly on q in floating point; any implementation needs an exact-comparison or tolerance rule (O1, O2; the benchmark used 64 machine epsilons).

## Lead's recommendation
Keep the HPM. Add to the output, as secondary and constant-free: postFDP(Ŝ) = |Ŝ|⁻¹Σ_{j∈Ŝ}(1−PIP̂_j) with primary PIPs, the expected number of missed variables Σ_{j∉Ŝ}PIP̂_j, and optionally the posterior-FDP path. If a named BFDR set is wanted, use the ½-PFER set, not q = 0.1. Theory additions, if adopted: a deterministic T07(iv) (BFDR optimality, cap bound, Lemma L, perfect-PIP inflation) and a T03 corollary (BFDR/½-PFER consistency conditions); neither replaces T21. These are recommendations; METHODOLOGY v3 and the theory deliverables are unchanged.
