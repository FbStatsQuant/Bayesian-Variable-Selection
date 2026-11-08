# ERRATA — corrections to API-PXNGAP PROOF.md adopted in this ticket (each from a reviewer finding)

PROOF = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`. Status of each line: the
correction is accepted by the lead; "re-check" names the reviewer that must confirm it (or that proposed it verbatim).

| # | PROOF line | correction | source | re-check |
|---|---|---|---|---|
| E-1 | 166 | first term of P(𝒟_nᶜ ∩ ℰ) is 2e^{−n^{1/3}} (from (d1)), not e^{−n^{1/3}} | R12 #1 | proposed verbatim by R12 |
| E-2 | 162-167 | Lemma E is stated on ℰ* := ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn} (or any X-measurable subevent), fixed φ₀ > 0, 𝔉 deterministic or X-measurable with |𝔉| ≤ Cn^D, conclusions for n ≥ n₀; applications use ℰ_n (P2) / ℰ♯_n (P8♯) | R12 #2 | proposed verbatim by R12 |
| E-3 | 207 | remark (4) replaced by: "The signal-norm bound is used to control ‖Y‖² and hence the standardised RSS floor in E3, and to obtain the uniform n^{2/3} approximation in E5. The raw-scale RSS lower bound itself does not require it." | R12 #3 | proposed verbatim by R12 |
| E-4 | 198-199 | admissible C₂ = 4σ√(M(D+1)) + σ²[5 + 8(D+1)] (explicit; onset may depend on J, φ₀) | R12 table | proposed by R12 |
| E-5 | 319-321 | Λ(a): indices with A₀ = ∅ or Λ_{A_s} = 0 are removed from the Beta family (their increments are 0); for n−1 ≥ gs₀, Λ_{A_s} = 0 iff S₀ ⊆ A_s a.s., a deterministic index set; Tr-J(c) is applied to the rest | R11 #1 (also R13) | proposed verbatim by R11 |
| E-6 | 153, 156 | table: "P3 start mass (§5)" → "P3′ start mass (§6)"; "u is fixed" → "u is uniformly bounded by a fixed constant" | R11 #2 | proposed verbatim by R11 |
| E-7 | 225, 230-233 | Lemma B(ii) restricted to |A| ≤ n−3; Haar calculation requires |U| + |W| ≤ n−2 (ERROR in the original; unused downstream) — lemmas/B_ii_domain.md | R13 #1 | NEW reviewer (repair re-check) |
| E-8 | 379-391 | Lemma LS(i) needs ℓ ≥ c for arrival after exactly c moves; restated (lemmas/LS_P6_repair.md) | R15 #1 (ERROR) | NEW reviewer |
| E-9 | 395-399, 441 | P6′ event includes 𝒵_n ((L)) and ℓ_n ≥ c; sharp cost 1 + Σ_{t=0}^{c}[p+(s+t)(p−s−t)] ≤ 1+(c+1)(p+s₀p); the false "max_{k≤K} ≤ p+s₀p" removed; (K)'s c+1 scans on the joint event | R15 #2 (ERROR) | NEW reviewer |
| E-10 | 286-288 | P5: bypasses (does not prove) N3; EX-A incl. exact DP arithmetic retained | R15 #3 | NEW reviewer |
| E-11 | 445-446 | closure cites GUARD (G2)/Lemma RO and R̄⁺'s definition; production bridge stays an implementation obligation | R15 #4 | NEW reviewer |
| E-12 | 363-367 | (L) addition step replaced by lemmas/L_strict_localmax.md (original was an ERROR: (E3) gives factor 1, not ½, before Z_l²) | R17 #1 (ERROR in original; repair VERIFIED by R17 and arithmetic by R19) | done (R17, R19) |
| E-13 | 343-344 | cross-component swaps: "If the destination is an incomplete pair i′ ∈ I, its gain is at most G_i′ ≤ G_i* (hub: G_i′; proxy: G_i′η_i′; a-group non-hub: zero). In a complete pair, visible component, or null group its gain is zero." | R17 #2 | proposed verbatim by R17 |
| E-14 | 333-334, 360-361, 369 | min ∅ := +∞ (v = 0); line 369 "failure probability is of order …" → "a first-order heuristic for addition failure is …" (threshold 2 log((2p−s₀−1)/(s₀+1)) + log(n+1), W3-PXN PROOF:330-331); the proof gives only P((L) fails) → 0 | R17 #3 | proposed verbatim by R17 |
| E-15 | 79-85 | Theorem R display split: (R-a) S(t) for every t; (R-b) S(t*) ≤ K_n; (R-c) p^{−C} onset and summable form (lemmas/R_branch_repair.md §1) | R14 #1 (ERROR) | NEW reviewer |
| E-16 | 98-100 | "≈ 0.17" is not the displayed bound (≈ 1.13·10⁶ at (200,500)); delete or relabel | R14 #5 | proposed by R14 |
| E-17 | (W7:77-89 used at PX:89-92) | A0(c) false for absorbed groups; the use goes through the direct strict-global-margin argument (R_branch_repair.md §2) | R14 #2 | proposed verbatim by R14 |
| E-18 | §0, §10 | exact-branch convention: partition/start/LS0 objects are data functions on every branch; (C) handles the exact branch (R_branch_repair.md §3) | R14 #3 | NEW reviewer |
| E-19 | 270-271 | delete "and is sharp in order" (no matching lower bound; for slowly growing p the rate √(log p/n) is attainable) | R16 #5 (GAP) | NEW reviewer (deletion only) |
| E-20 | 241, 254 | "on {q < 1}" prepended to the T22(i-a) inequality (P(q < 1) → 1 gives the O_P statement); write ã_hj 1_{𝒢_n} ≤ … | R16 #4 | proposed verbatim by R16 |
| E-21 | 475-477 | "(probability of order n^{−1/2}(log n)^{−1/2})" → "(a first-order heuristic gives order n^{−1/2}(log n)^{−1/2}; the proof gives only P((L) fails) → 0)" | R30 #3 (GAP) | proposed by R30 |
| E-22 | 483-484 | finite-n illustration: with ρ = .7, ψ = .5, β = 1, v = 0, c = 1: η = .3675/.8775, c₂ = G(1−η) = 0.10897, and with σ² = 1 (M = 2θᵀΣθ + 1 = 2.5, 4(σ²+M) = 14) (n/2) log(1 + c₂/14) ≈ 0.775 at n = 200 (C1 Opus #6; ≈ 0.904 if σ² = 0.5) (not 0.07 and 0.58); conclusion (vacuous vs (2A+1) log n ≈ 20) unchanged | R30 #7 | proposed by R30 |
