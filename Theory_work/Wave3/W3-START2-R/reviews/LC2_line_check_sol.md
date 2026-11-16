# LC2 — line check of R3_RATE, R4_TRANSFER_COR, R5_EX — reply of Sol (codex gpt-6.1-sol, high), verbatim
# Brief: reviews/BRIEF_LC2_sol.md. Received 2026-11-15 (see LOG.md).

| file | verdict |
|---|---|
| R3_RATE.md | PASS WITH FIXES |
| R4_TRANSFER_COR.md | PASS |
| R5_EX.md | PASS WITH FIXES |

1. **S — [R3_RATE.md:20](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/lemmas/R3_RATE.md:20): threshold dependence is overstated.**  
   The blanket assertion that “for n large” thresholds never depend on H̄_n is stronger than (D4). That hypothesis requires log H̄_n ≤ κ_H√log n only eventually, with no uniform starting index. Consequently, the envelope substitution at lines 34 and 48, and bounds using it, may require a sequence-dependent starting index. Arbitrarily late finite violations of the envelope remain compatible with (D4).  
   **Proposed fix:** Introduce n_H such that the envelope holds for every n ≥ n_H, and allow thresholds using that envelope to depend on n_H. Keep C_B and the other constants independent of the particular sequence. The asymptotic target conclusions are unaffected.

2. **E — [R3_RATE.md:113](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/lemmas/R3_RATE.md:113): the explanation invokes reference sets absent from this subsection’s hypotheses.**  
   The sentence uses “S₀ ⊆ H_l,” although R3.3 assumes neither (L-R⁺⁺) nor a family H_l. The proof itself correctly works directly with U ⊊ S₀ and needs no such sets.  
   **Proposed fix:** Delete “and S₀ ⊆ H_l.” Explain that localisation is unnecessary because the maximisation already ranges only over proper subsets of S₀.

3. **E — [R5_EX.md:55](/home/fb31/BVS-wt/W3-START2-R/Theory_work/Wave3/W3-START2-R/lemmas/R5_EX.md:55): replace the unsupported “iff.”**  
   The upper bound n^{3/10−2A/5+o(1)} establishes convergence to zero when A > 3/4. An unspecified o(1) exponent does not determine convergence at A = 3/4, and an upper bound does not establish necessity for the quantity bounded. The following parenthetical correctly limits the claim.  
   **Proposed fix:** Write “which tends to zero when A > 3/4,” retaining the parenthetical.

The substantive arguments pass: R3.3 conditions on W_{S₀}, fixes the true-column scales, obtains d̄⁰_n = O(1/√log n), and supplies the required event and first-moment bounds. The 15κ_H contribution to C_B, vanishing failure probabilities, and R3.6’s application of P1.7/P1.4 are correct, subject to finding 1.

R4’s conditional probabilities, finite extrema over support sizes, random-rate decompositions, deterministic-envelope implications, and Gaussian (GR) verification are valid. Its uses of the sibling results stay within their stated scope.

R5’s visibility cases, drifting c_n premise for F4⁺⁺, exponent (1 + 2A)/10, and sufficient first-order range A > 3/4 are correct. No **C** finding or unresolved gap in a target conclusion was identified.

LC2-VERDICT: PASS WITH FIXES
