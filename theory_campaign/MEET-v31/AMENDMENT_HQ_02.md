# AMENDMENT_HQ_02 (HQ, 2026-11-04): reporting fields and growth rates from the theorem meeting

Source: MEET-THM close (`theory/MEET-THM` @ 514c8fc), `AMENDMENT_HQ_02_DEFINITIONS.md` (copied here verbatim as `AMENDMENT_HQ_02_DEFINITIONS_from_MEET-THM.md`), HQ ruling Q4. Nothing below changes the method's law, its random numbers, calibration, schedule or decision.

## Adopted
1. **Ĵ (Jeffreys-divergence estimate)**, field `J_hat`, exactly as defined in A1, with its label "Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated". Implementation: a read-only accumulator of the bridge potential d at initialisation and at the four measured endpoints (no new draws, transitions or scores). Historical fits report NA.
2. **d joins the default declared list 𝓗** (§6.11b), recorded raw; theorems use the range-scaled version.
3. **ε̂_× (`cross_block_rmax`) with companions κ̂, δ̂, ū̂ (global block-table envelope), r̂, η̂**, exactly as defined in A2, with its label and its "n/a" domain rule.
4. **Optional stacking configuration (i): R′_n = 4⌈log₂(n + p + 1)⌉**, for consistency of any fixed finite set of declared summaries on families with D_* = O_P(1). The shipped default stays R′ = 4.

## Not adopted as a method configuration
- **Configuration (ii), R′_n = 4⌈(n + p)⁶/4⌉.** HQ keeps it **only as a sufficient rate inside the theorem** (M1's simultaneous-control clause: "for any R′_n ≥ 4⌈(n + p)⁶/4⌉"), not as a runnable configuration of the method. Reason: at study sizes (n + p ≈ 700) it is about 10¹⁷ islands, so listing it as a method setting would misrepresent what the method can run. The theorem is unaffected.

## Status
Reporting fields 1–3 are specified, not yet coded (engineering, with the other v3.1 additions). Every field is POST HOC: it reads no uniforms and never feeds back into the run.
