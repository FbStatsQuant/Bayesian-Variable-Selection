# Audit t03acc-1: SOP:TH09
claims: SOP:TH09
stop_reason: end_turn

## SOP:TH09 — Theorem T03♯ (`theory_main.tsv`:2, registry line 68; proof `theory_campaign/W1-T03R/PROOF.md`:160-207, with §1, §2, §4)

**Result:** I found no GAP or ERROR; the theorem is proved as stated, with two local slips that do not affect it. You asked for FATAL/MAJOR/MINOR; I use the mandated scale, where FATAL corresponds to ERROR and MAJOR to GAP, and there are none of either.

### What I checked

**Exact tail and cutoff (PROOF.md:15-61).**
- E1(a): the ratio q_{i+1}/q_i = ρ_i and the identity 2(p−i) = (2p−1−i) − (i−1) are correct.
- E1(b): ρ_i ≤ ½e^{−(i−1)/(2p−2)} holds for 0 ≤ i ≤ p−1, including i = 0. The index sum Σ_{i=s₀}^{k−1}(i−1) is right, including s₀ = 0. Monotonicity of t(t−1) and the geometric sum are right.
- E2(i): m_n(ω) ≥ s₀ for ω ≥ 0, γ_m ≥ 0, and C(p,s₀)2^{s₀} ≤ (2p)^{s₀}, so m♯_n ≤ min{K, m_n(½log n)} ≤ C_m log n. This is the only fact about m♯_n that (C1) needs.
- E1(c), E2(ii)–(iii), E3 and Prop. D are not used by T03♯.

**T02(i♯) and Lemma den′ (PROOF.md:74-97), used in (C9).**
- The proof of [P1] `lem:den` (PROOF_v3.tex:337-359) does give the bound before the factor ϖ(S₀) is applied. I rechecked the exponent chain and E₀Λ_n ≤ C_Λ.
- [P1] `lem:num` needs a data-free rate; b₋ is data-free, so E₀Θ^{(1)} = 1.
- [P1] `thm:Ta` needs 𝓑_n and S₀ ∈ Ω; the proof restricts to 𝓑_n and to n with s₀ ≤ K.
- [P1] `thm:T01iii` needs G and ‖μ‖² ≤ nM (from R); the constant (8+24M/σ*²)/(n−1) is right.
- The constant c♯ = κ²/(c_IG σ*²), the two Markov steps, and the evaluation at m = m♯_n(½log n) giving (1+1/n)^{s₀/2}n^{−1/2}Θ♯ are correct.

**Lemma B (PROOF.md:138-143).**
- (B1): SE_w gives full rank, so χ²_J is exactly χ²_{|J|}. [P1] `lem:spec`(e) is stated for arbitrary g > 0 and k ≥ 0, so it applies with g = g₀.
- (B2): S′ = S₀ ∪ J′(S) with |J′(S)| ≤ j₀ falls under SE_λ; Lemma I passes the bound to S ⊆ S′.
- (B3): uses only [P3] `lem:smoother`(b) (unconditional) and (c) applied to S; P_T − P_S is a projection by column-space nesting alone.

**Every use of SE in [P3].** I located each one and confirmed it is replaced within the new hypotheses.

| [P3] step | SE use | Replacement | Verdict |
|---|---|---|---|
| Paragraph before 𝒢_n; `lem:Gprob` (PROOF_v2.tex:171, 183-195) | exact χ² laws | (B1) for (G3); (G1), (G2), (G4) need only rank ≤ dimension | sound; 5/n stands |
| `lem:ongood`(c) (:220) | λ_min(G_S) ≥ Nφ₀² | (B2), restricted to \|J′(S)\| ≤ j₀ (C3) | sound; (a), (b), (d) use no SE |
| `lem:onesup` (:246-248) | determinant and `cor:diff` on (S₀, S) | (B1) determinant with 1+1/g₀; (B3) with the eigenvalue bound on S₀ from R (C4) | sound; `lem:ongood`(b) covers \|S\| ≤ m♯+s₀ |
| `prop:sup` (:269-277) | via `lem:onesup` | (C5); `lem:prior`(b) needs s₀+j ≤ p, automatic for J ⊆ [p]∖S₀ | sound; q_n² algebra and q_n ≤ min{½, c_q r_n} correct |
| `lem:SvsSp` (:293-300) | `cor:diff` on S ⊆ S′; `lem:ongood`(c) | (C6)(a) crude bound with no eigenvalue condition; (C6)(b) via (B2), (C3) | sound; the crude bound drops e^{ρ_n} correctly |
| `lem:signal`, `lem:signalgain` (:150-151, 310-312) | λ_min(G_{S′}) ≥ Nφ₀² | (B2); applied only where \|J′(S)\| ≤ j₀ (C7) | sound |
| `lem:assemble` (:327-329) | sharp bound on \|J′\| > j_* | (C6)(a) on that branch (C8) | sound; the exponent count (j₀+1)/2 ≥ s₀(A+½)+1 gives the n^{−1} rate |
| Step 1 and (iv) (:342-350, 366-378) | `lem:signal` for all of 𝒰 | only models with \|J′(S)\| ≤ j₀ enter κ_n (C10) | sound |

**Constants and assembly.**
- (C10): (1−1/n)c ≥ L* for n ≥ c/(c−L*). The requirements L* ≥ 4C_*, L*/32 ≥ s₀(A+1)+2 and n/5 ≥ (s₀(A+1)+2)log n give κ_n ≤ e^{ρ_n}n^{−2}.
- BM-∞ reduces to BM(L*+1) eventually; in (iv), J_n^∞ ⊆ J_n(c₀+1) eventually.
- (i): the three-way split of Ω∖{S₀} is exhaustive, each part is O_P(r_n), and P₀(𝒢_n^c) ≤ 5/n. (ii), (iii) and (v) are unchanged from [P3] and correct.
- Models S′ outside Ω (|S′| up to m♯+s₀ > K) enter only through ℓ(·), which is defined on all of [p]; SE_w covers them.

### Findings

- **MINOR — PROOF.md:9.** "For p = 1 every statement below is trivial or void" is not accurate for T03♯: p = 1, s₀ = 1 is a genuine case, and E1(b)/E2 divide by p−1. This is harmless, because for p = 1 one has m♯_n ≤ K = 1 ≤ C_m log n directly, and nothing else in (C1)–(C10) uses p ≥ 2.
- **MINOR — PROOF.md:172 with :50, :59.** (C1) cites E2(i) without its side condition n ≥ 5 when s₀ = 0. This is absorbed by "n ≥ n₀".

AUDIT SOP:TH09 VERDICT=MINOR FINDINGS=0