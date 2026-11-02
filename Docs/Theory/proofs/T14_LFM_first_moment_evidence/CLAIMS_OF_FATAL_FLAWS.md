# CLAIMS_OF_FATAL_FLAWS — T14(i)

Reviewer: Astra (gpt-6-astra, reasoning high), session 01a16418-6bd3-78f1-ad35-0348b23c7968, round 1 on PROOF_v1 (2026-10-22). Verdict: verified.

## Fatal or gap findings

None. Astra raised no fatal and no gap finding.

## Exposition findings (recorded for completeness)

**Finding 1 (exposition), verbatim claim:** "The notation \(q_1,\bar Z_1\) is used both for temperature \(1\) and for stage \(1\). These meanings generally differ when \(T>1\). In particular, the assertion “\(q_T=q_1\)” requires the temperature interpretation of the right-hand side."

**Lead's answer: accepted and fixed.** PROOF_v2.tex defines Z = m(∅)Σγ₀e^{d} (the bridge normaliser at φ = 1), states that a numerical subscript on q or Z̄ is always a stage index, and writes Z = m(∅)Z̄_T and q_T(S°)/q₀(S°) = e^{d(S°)}Z̄₀/Z̄_T in the proof of (i-a). The (i-d) example keeps q₁, Z̄₁ because there T = 1, as now noted. STATEMENT.md §1 was reworded the same way (notation only; change log §4).

---

# Stage B (Protocol Amendment 1), round 1 on PROOF_v2, 2026-10-22

Reviewers: Astra #2 (gpt-6-astra, high, new session 01a1641c-418a-7463-a810-25b59b68de23): verdict verified, no findings. Opus 5.5 (xhigh, Claude Personal, clientRequestId T14i-stageB-opus-personal-r1): verdict verified, three exposition findings.

## Fatal or gap findings

None. Neither Stage B reviewer raised a fatal or gap finding.

## Exposition findings (Opus), all accepted and fixed in the unified PROOF_v3.tex

**Opus finding 1, verbatim claim:** "the statement gives the resampling and move laws "conditionally on the past". The proof conditions on the smaller σ-field F_{t−1} = σ(ξ₀, ζ₁, …, ξ_{t−1}) without saying why that is allowed."
**Lead's answer: accepted.** §1 item (b) now says that laws given on a larger past hold in particular given F_{t−1} (resp. (F_{t−1}, ζ_t)) by the tower property, since μ_t is F_{t−1}-measurable and the law of ξ_t^j depends only on ζ_t^j.

**Opus finding 2, verbatim claim:** "the proof says the islands "share the grid, the kernels, N and S°". Only the grid, γ₀, d and S° are actually needed."
**Lead's answer: accepted.** (i-c) now says both right-hand sides depend only on (q_t)_{0≤t≤T} and S°, which the data and 𝓒 fix.

**Opus finding 3, verbatim claim:** "it cites T12(i) (E[Ẑ_{r,t} q̂_t(f)] = Z_t q_t(f)), which is not in the packet, so I cannot check it against its source."
**Lead's answer: accepted.** The remark now says Proposition 5 is equivalent to the identity in the form in which the project's conjecture T12(i) states it, that the file is not needed, and that the argument uses nothing from T12. (The remark is not used by the proof.)
