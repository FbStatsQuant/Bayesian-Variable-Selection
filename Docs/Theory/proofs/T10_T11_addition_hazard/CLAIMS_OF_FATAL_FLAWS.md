# CLAIMS_OF_FATAL_FLAWS — T10 (old T11)

Every fatal or gap finding, verbatim, with the lead's answer. Exposition findings are handled in the revision log at the end.

## Round 1 (PROOF_v3)

No fatal finding from either reviewer. One gap, raised by both.

### R1-CP-1 (CP reviewer, Finding 1) — gap
> **Location:** §6, paragraph (iv-c), the sentence beginning "By 00_COMMON §2 the final run has…".
> **Severity:** gap (verification only; no error found).
> **Claim:** The proof of (iv-c)(1)–(2) relies on budget definitions that appear neither in STATEMENT.md nor among the cited results: N_e = 4^e·max(2500, n, p); T_e = 4^e·max(1000, ℓ²); ℓ = ⌈log₂(2n+1)⌉; L = max(4, ⌈log₂(n+1)⌉); Q_f = 4N_e(T+L+5). STATEMENT.md gives only the count 4N_e(T+L+4) ≤ 4N_e(T_e+L+4). From the packet I cannot confirm that these formulas are quoted correctly.
> **Evidence:** The conclusion depends on them. Conclusion (2) needs N_e(T_e+L) = o(n^{3/2}), and conclusion (1) needs N_e(T_e+L) = o(n^{5/2}). Both would fail if, for example, N_e grew like n·p = n². Assuming the formulas are as quoted, every inequality in the paragraph checks out (see above).
> **To close it:** confirm the quoted formulas against 00_COMMON §2, or copy them into STATEMENT.md.

### R1-CW-F1 (CW reviewer, F1) — gap
> **Location:** §6 (iv-c), tex lines 212–215. [...] N_e = 4^e max(2500,n,p), T_e = 4^e max(1000,ℓ²), ℓ = ⌈log₂(2n+1)⌉, L = max(4,⌈log₂(n+1)⌉) and Q_f = 4N_e(T+L+5).
> **Severity:** gap.
> **Claim:** (iv-c)(1) and (iv-c)(2) rest on these budget formulas. STATEMENT.md does not contain them. It only says "the declared budgets of 00_COMMON §2" and gives the count 4N_e(T+L+4) ≤ 4N_e(T_e+L+4). I have not seen the source, so the formulas are unverified, and (iv-c) is unverified with them.
> **Evidence:** [...] If N_e were of order n², or T_e of order n, (2) would fail. If the quoted formulas are correct, the proof's arithmetic is right [...]. Repair: put the budget definitions into STATEMENT.md, or check them against 00_COMMON §2.
(Full text: review/REVIEW_R1_CW.md.)

**Lead's answer (both): accepted and fixed.** The lead checked the formulas against `theorems/00_COMMON.md` §2, line 24: "N₀ = max(2500, n, p); H₀ = ⌈512N₀/2500⌉; ℓ = ⌈log₂(n+p+1)⌉; T₀ = max(1000, ℓ²); (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀), e ∈ {0,1}; L = max(4, ⌈log₂(n+1)⌉). Q_f := 4N_e(T + L + 5) […]; 4N_e(L+6) ≤ Q_f ≤ 4N_e(T_e + L + 5)." They match the proof's quotation (with p = n, ℓ = ⌈log₂(n+p+1)⌉ = ⌈log₂(2n+1)⌉). Fix: STATEMENT.md v3 now reproduces this budget block verbatim (definitions only; no conclusion changes), the round structure of the final run (4N_e particles; T stages of one round, L burn-in and 4 measured rounds), and PROOF_v4 (iv-c) quotes the definitions from STATEMENT.md and writes ℓ = ⌈log₂(n+p+1)⌉ before specialising to p = n.

## Revision log for exposition findings (round 1 → PROOF_v4)
- CP-2 / CW-F2 (admissibility, scaling): STATEMENT.md v3 reproduces 00_COMMON §1's data conditions and standardisation (n ≥ 3, finite entries, constant columns dropped, y non-constant; columns centred and scaled to sample SD 1 with divisor n−1). The example now refers to them.
- CP-3 / CW-F2 (exact branch remark): Remark now says plainly that the example does not exhibit the failure in a regime where SMC rounds run in production, and sources the exact-branch rule (quoted in STATEMENT.md v3).
- CW-F3 (comparison chain "β replaced by 0"): the comparison kernels are now defined directly; "because β ≤ 1" dropped.
- CW-F4 (stream variate independence): stopping-time / strong-Markov sentence added.
- CP-4 / CW-F5 (conditional form): 𝓘 allowed random with 1{u∈𝓘} 𝓖-measurable; conditional monotone convergence named; final-run example marked as an illustration.
- CP-5 / CW-F6 ((iv-d)): one-line reason added (swaps preserve size; π₀ is supported on Ω; γ_φ(S) > 0 by T22 Lemma 1).
- CW-F7 (positivity in part (i)): T22 Lemma 1 cited at the point of division and real powers.
- CP-6 / CW-F8 (side remarks on T22's needs): reworded to rest on the in-text sketch only.
- CP-7 / CW-F9 (Remark 6(c)): the reviewers' exact-invariance observation added as a remark (X₅ ~ π₀ exactly in the example, via T09(ii) reversibility), marked as corroboration.
