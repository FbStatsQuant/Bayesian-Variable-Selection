# W5-FAVIID — working plan (run of 2026-11-02, branch `theory/W5-FAVIID`)

Inputs read: PROTOCOL, task file, THEORY_PRIORITIES, 00_COMMON, locked T22(i)/(iii) statements, W3-PXN PROOF/REPORT,
W3-VEXP REPORT/REPAIRS, W1-EXP PROOF §§1–2, W2-T26 PROOF §§0–1 and REPORT §4, METHODOLOGY_v3 §§3, 6.3–6.9,
`v3_blocks.h`, `gen_dev_data.R`.

## Route (decided after reading)

1. **One-sided chain-free table bound (new, deterministic).** For U ⊂ A inside a block with SE,
   r(A)/r(U) ≤ (n+1)^{−|A∖U|/2}(RSS_A/RSS_U)^{−ν}·e^{O(|A∖U|/n)}: the EXP′ remainder is ≤ O(1/n) in the *upper*
   direction (W1-EXP Lemma 1.1's a_S is monotone in S up to O(1/n)). Removes κ_EXP (≈ 100 nats at study SNR) from
   every upper bound.
2. **Exact Beta law for any fixed (group, truth-conditioning set) pair** — PXN Lemma B, with y an arbitrary function
   of (X_{S₀}, ε).
3. **Moment bound with a B-free constant.** max_j Y_j ≤ λ(1 + Σ_j (Y_j/λ)^j) plus the Mittag-Leffler sum gives
   E D_b ≤ 3.83·|C_b∖U_b*|·ξ_n, no 2^B and no Σ_j.
4. **Fixed partition (goal 1):** T22(i) ⇒ 1 − π₀(S₀) = O_P((s₀+1)·√(log n/n)) with explicit constant.
5. **Random union-of-groups partition (goal 2):** subspace-sum inequality across population-independent groups ⇒
   D_b ≤ (1+o(1))Σ_{K⊆b} D′_{K,W}, W = truths co-blocked with K ⇒ partition-free bound, constant ×|𝒲(m)|.
6. **Dilution threshold (goal 3):** population plug-in prediction of log π₀(S₀) (null-addition mass, deletion odds,
   proxy-swap odds) vs exact π₀ at n ∈ {200,…,3200}.
7. **(P1) (goal 4):** Δ_n = max(1 − π₀(S₀), δ₁); simulate the pilot ESS rule to get T_n.
