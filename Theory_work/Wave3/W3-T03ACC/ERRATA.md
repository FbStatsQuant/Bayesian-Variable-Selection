# W3-T03ACC — ERRATA (E findings; never blocking; applied later in one editorial batch, v4 §5.3)

| # | location | finding | source | proposed text |
|---|---|---|---|---|
| E1 | `sources/W1-T03R/PROOF.md:168` (conclusion (iv)); `STATEMENT.md` clause 4 (copied verbatim from the record) | J_n^∞ written without "j ∈ S₀"; harmless (θ*_j = 0 off S₀, threshold eventually positive) | LC-C N1 | write $J_n^\infty=\{j\in S_0:\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)\}$ |
| E2 | `sources/W1-T03R/PROOF.md:9` | "for p = 1 every statement below is trivial or void" is inaccurate for T03♯ (p = 1, s₀ = 1 is a genuine case); E1(b),(d), E2(i) are stated for p ≥ 2 | SL1 check 2; LC-A N1; LC-B N1; LC-C N7 | "For p = 1 (then s₀ = K = m♯_n = 1 under R1) E1(b),(d) and E2(i) are not needed: m♯_n ≤ K = 1 ≤ m_n(½ log n) directly; the remaining steps hold as written." |
| E3 | `sources/W1-T03R/PROOF.md:16`, `:79-80` | R_m's sum written from k = m+1 "for every integer m"; q_k undefined for k < 0 | LC-A N2 | lower limit max(m+1, 0), as in STATEMENT §2 (R_m = ϖ(Ω)/ϖ(S₀) for m < 0) |
| E4 | `reviews/BRIEF_LC_A_sol.md` (lead's brief, not a proof file) | "E1(c) is used only by E2(iii)/E3": Prop. D (`PROOF.md:117`) also reuses E1(c)'s argument; neither is on the T03♯ route | LC-A excluded-step row | none needed (record only) |
