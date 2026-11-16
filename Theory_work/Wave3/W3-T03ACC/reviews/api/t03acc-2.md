# Audit t03acc-2: SOP:TH09
claims: SOP:TH09
stop_reason: end_turn

## SOP:TH09 — Theorem T03♯ (PROOF.md §6, with §§1, 2, 4 as its inputs)

No GAP or ERROR found: the argument goes through as written. There are three MINOR slips, none affecting the claim. The user's FATAL/MAJOR/MINOR scale maps to ERROR/GAP/MINOR here; there are no FATAL or MAJOR items.

### What I checked

**Exact tail, as far as T03♯ consumes it (PROOF.md:20–40, 59).**
- E1(a): the identity for ρ_i and the product formula are correct.
- E1(b): the factor bound ρ_i ≤ ½e^{−(i−1)/(2p−2)} holds for 1 ≤ i ≤ p−1 and separately for i = 0; the exponent sum, the monotonicity of t(t−1) on integers t ≥ 0, and the geometric sum are correct.
- E2(i): m_n(ω) ≥ s₀; γ_m ≥ 0 for m ≥ s₀ ≥ 1, and for s₀ = 0 once m ≥ 2 (n ≥ 5); C(p,s₀)2^{s₀} ≤ (2p)^{s₀}. So m♯_n ≤ min{K, m_n(½ log n)} ≤ C_m log n.
- E1(c), E2(ii)–(iii), E3 and Prop. D are not used by T03♯ and were not audited as part of this claim.

**T02(i♯) and Lemma den′ (PROOF.md:79–97).**
- Lemma den′ is extracted from the proof of [P1] `lem:den`, not from its statement, so I re-derived it from PROOF_v3.tex:337–359. The exponent lower bound, the restriction to an interval of length σ*²n^{−1/2} inside [σ*², 2σ*²], D_{S₀} ≤ (n+1)^{s₀}, and E₀Λ_n ≤ C_Λ all hold. They use only λ_min(R_{S₀}) ≥ φ₀² and ‖μ‖² ≤ nM.
- `lem:num` is applied at the data-free rate b₋, as it requires; E₀N_m = ϖ(E_m) = R_mϖ(S₀).
- `thm:Ta` is applied on 𝓑_n with S₀ ∈ Ω (s₀ ≤ K assumed).
- The algebra giving c♯ = κ²/(c_IG σ*²) is correct. The event split and the two Markov steps need L > c♯², which is stated. P₀(𝓑_n^c) is from `thm:T01iii`. The bound is uniform in m.
- m♯_n(ω_n) is data-free, so the "consequence" is legitimate.

**Lemma I and Lemma B (PROOF.md:136–143).**
- (B1): full rank follows from G ≻ 0; the rank of P_{S₀∪J} − P_{S₀} is |J|; `lem:spec`(e) is applied with g = g₀ and j = |J|, which is within its hypotheses (also for s₀ = 0, k = 0).
- (B2): SE_λ(j₀) on S′ = S₀ ∪ J′(S), then Lemma I passes the bound down to S.
- (B3): re-proved directly from `lem:smoother`(b),(c); only the eigenvalue bound on S is needed.

**(C1)–(C10) and Assembly (PROOF.md:172–203).** I went through every use of SE in PROOF_v2.tex (lines 171, 220, 246–247, 282, 295, 342) and confirmed each is covered:

| Use of SE in [P3] | Replacement | Hypotheses met? |
|---|---|---|
| Exact χ² laws for (G3), `prop:sup`(b) | (B1) | Yes: needs \|J\| ≤ m♯_n, and J′(S) ⊆ S gives \|J′\| ≤ m♯_n |
| (G4) | (B2) | Yes: only rank ≤ s₀ is actually needed |
| `lem:ongood`(c), λ_min(G_S) | (B2) | Yes, restricted to \|J′(S)\| ≤ j₀; consumed only by `lem:SvsSp`, sharp part (C6)(b) |
| `lem:onesup`, determinant | (B1) | Yes |
| `lem:onesup`, numerator | (B3) with S = S₀ | Yes: eigenvalue bound on S₀ is R |
| `cor:diff` lower half on (S, S′); `lem:signal` | (B2) | Yes, only for \|J′(S)\| ≤ j₀ |
| \|J′\| > j₀ branch of `lem:assemble` | crude bound (C6)(a) | Yes: uses only `lem:prior`(a), `lem:det` first part, `lem:smoother`(d) |

Further checks:
- `lem:ongood`(a),(b),(d) and (G1)–(G2) are stated "under SE" in [P3], but their proofs (PROOF_v2.tex:188–190, 216–218, 222) use no eigenvalue condition. (G2) covers |T| ≤ m♯_n + s₀, as (C4) needs.
- (C5): q_n² = c_q² r_n² · n/(n+1) · e^{2ε_n}/4 is correct. With g₀ fixed, q_n → 0, so q_n ≤ ½ can be placed in n₀.
- (C8): the multiplicity 2^{s₀} is right. The second term carries e^{ρ_n} rather than e^{2ρ_n}, correctly, since the crude bound has no e^{ρ_n}. The exponent count (j₀+1)/2 ≥ s₀(A+½)+1 is correct.
- (C9): (1+1/n)^{s₀/2} n^{−1/2} Θ♯ is correct.
- (C10): (1−1/n)c ≥ L* iff n ≥ c/(c−L*). `lem:signalgain` is used with L = L* ≥ 4C*, and L*/32 ≥ s₀(A+1)+2. BM-∞ implies BM(L*+1) eventually. J_n^∞ ⊆ J_n(c₀+1) eventually, and the posterior mass is monotone.
- Assembly: the partition of Ω∖{S₀} is exhaustive; P₀(𝒢_n^c) ≤ 5/n; (ii) and (iii) are elementary given (i).

### Findings

- **MINOR — PROOF.md:9.** The case p = 1 is dismissed as "trivial or void", but E1(b) and E2(i) divide by p−1, and T03♯ with p_n = 1 (allowed in R1) is not void. Repair: for p = 1, K = 1, so m♯_n ≤ K = 1 ≤ m_n(½ log n) directly; nothing else in §§2, 4–6 uses p ≥ 2.
- **MINOR — PROOF.md:79–80 (with :16).** R_m is written as Σ_{k=m+1}^K q_k / w(s₀) "for every integer m", but q_k is defined only for k ≥ 0. For m < 0 it must be read as ϖ(Ω)/ϖ(S₀). The sup over m is unaffected.
- **MINOR — PROOF.md:168.** J_n^∞ is written without "j ∈ S₀". This is harmless because θ*_j = 0 off S₀ and the threshold is positive.

AUDIT SOP:TH09 VERDICT=MINOR FINDINGS=0