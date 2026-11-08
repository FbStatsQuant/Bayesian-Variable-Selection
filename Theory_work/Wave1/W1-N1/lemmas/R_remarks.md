# Remarks: scope, sharpness and what breaks N1

Status: remarks (no new claims beyond those cited). v2, 2026-11-08 (numbers from RESULTS.md v2).

1. **Route.** The charter route (resample–move recursion; the "terminal-round prefix identity") is used only in its
   κ ≡ m (full-round) form. Measured endpoints are read after complete rounds (`v3_engine.h:357-360`), so the within-round
   prefix identity (T12 (i.c)), which the Rao–Blackwellised record needs, plays no role. Seat A's reading — "(a2) for the
   plain average is the base case of the same terminal-round unbiasedness [...] so N1 should be a short extension of the
   locked lemma" (`NBH/branch_snapshots/MEET-v31/R3_A.md:38`) — is confirmed: N1 = T12 (i.b) + Lemma B (code bridge) +
   Lemma F (conditioning with 𝓒-dependent h) + linearity.

2. **Non-triviality.** The identity is for the evidence-weighted endpoint average. The unweighted average H_r(h) is biased
   for π(h) (exact bias up to 0.16, `numerics/RESULTS.md` §3); E[Ẑ_r H_r(h)] = Zπ(h) holds to ≤ 9.3e-15 on the same cases. "Neither normalised estimate is generally unbiased at a finite budget" (`METHOD_v3.1_FINAL.md:158`) is
   consistent with this.

3. **What breaks it.** Exhibited numerically (`numerics/RESULTS.md` §4–§5): the first three items. The conditioning
   items are supported by the cited locked results, not by this companion.
   - A terminal kernel that is not π-invariant (NC1, rounds with the φ = ½ kernel): discrepancy 3e-3 to 0.77.
   - Measuring without the final reweighting to φ = 1 (NC2): discrepancy ≥ 3e-3 even after L + 4 invariant rounds at φ = 1.
   - An h chosen after the run (NC3, the indicator of the island's most frequent endpoint): N1-centred discrepancy
     E[W H(h_ω) − π(h_ω)] up to +0.17, resolved (|z| > 6) on 18 of 20 runs; the other two runs do not detect a discrepancy. This is why the M9 declaration requires h fixed before stream 10 and excludes "the measured-round
     frequency of the returned HPM" (`METHOD_v3.1_FINAL.md:159`).
   - Conditioning on completion need not preserve it (clause (c), CEX-guard); conditioning on a favourable final
     diagnostic breaks the evidence identity (T12 (iv.e)). N1 is a potential-run statement.

4. **Sharper constant in (e).** For the plain average the islandwise bound is δ₁, attained by h = 1{S ≠ S₀}; the card's
   2δ₁ is implied (`lemmas/E_corollary.md`).

5. **Downstream (not proved here).** Clauses M1(f), (g), (i) take N1 as their premise ("PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r]
   = π(h) is still a premise'", card TH01). With N1 proved, that premise is discharged **islandwise** (given 𝓒, on 𝒜 ∩ {r ≤ R′}) for every bounded declared h
   under the named premises; pooled clauses keep their own premises; the clauses' own proofs, statuses and remaining premises (IND-T extension for R′ > 4, GUARD-W,
   stacking, T03♯ for (i)) are unchanged by this ticket.
