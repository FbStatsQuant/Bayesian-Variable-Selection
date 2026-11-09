# Part 6 — Dependence on A, obstructions, and what is not claimed

## 7 Dependence on the exponent A

Every step of Theorem PXN holds for each fixed A ≥ 1 (A > 1 included). No step uses p ≤ n or a lower growth bound on p; only Gram matrices of size O(log n) are inverted.
All rates are √(log n/n) for each fixed A; A enters constants and onsets only. In detail:

- **Lemma Tr-J and Lemma E families (§1.3, §1.4).** D = A (P3′: family X_{h,V}, size G_n2^g ≤ 2^{16}n^A) and D = A(s₀+2) (Lemma Λ(a): |𝔉_n| ≤ 2^{s₀+2}n^{A(s₀+2)}); thresholds
  t_{n,D} = 8(D+1) log n, τ_{n,D} = t_{n,D}/n; failure ≤ Cn^{−1}e^{O(√log n)}. For Lemma E: P(𝒟ᶜ ∩ ℰ*) ≤ 2e^{−n^{1/3}} + Cn^D[n^{−4(D+1)}e^{√(8J(D+1)log n)} + 2n^{−2(D+1)}], and the constant
  C₂(σ², M, D) in (E5). c_E and κ_E have no direct dependence on A.
- **Theorem R (§2.3).** The onset ((2+C)A + ½) log n + log(2/(√π(1−ρ))) ≤ (n−4)I* (I* and the density constant do not depend on A); (R′): log 3 + (2+C)A log n ≤ (n−1)(ρ−ψ̄)²/4096. Summability needs no lower growth
  bound on p.
- **ℰ♯_n (§2.2).** δ_n = 32√(2(A+1) log n/(n−1)), L_n = s₀ + max{m_n, k_n, j₀, g, s₀+2} with k_n and j₀ depending on A; the SE event over sets of size L_n = O(log n) needs L_nδ_n = O((log n)^{3/2}/√n) → 0,
  and log p = o(n).
- **P3′ (§3.2).** t_{n,A} = 8(A+1) log n; C_q ∝ C_e g e^{2κ_E}√(A+1); p√n e^{−c₆n} = o(√(log n/n)) for every fixed A, with an A-dependent onset; c₆ does not depend on A.
- **Lemma Λ(a) (§4.1).** Needs Mτ_{n,D} = 8M(A(s₀+2)+1) log n/n ≤ c₂/8 (so that the projection loss is o(n)).
- **Lemma U and (D_S) (§4.2, §4.3).** The penalty (2A+1) log n in mar_n(c′); mar_n(c₂/2) > 0 needs n ≳ (4A+2)(4(σ²+M)/c₂) log n. Population constants c₂, c₄, c₅ and κ_E do not depend on A.
- **(L) (§4.4).** F(S₀+l) − F(S₀) ≤ −½ log n + log log n + O(1), with Z_l² ≤ 2 log p + 2 log log n ≤ 2A log n + 2 log log n and RSS_{S₀}/(nσ²) = 1 + O(n^{−1/3}) by (E5); the remainder
  O(A n^{−1/3} log n + A²(log n)²/n) is o(1) for fixed A. P(𝒵_nᶜ) does not depend on A.
- **(P) (§5.3).** j₀ = ⌈(2A+1)s₀⌉ + 1; cutoff m♯_n ≤ k_n := max{s₀, ⌈1 + s₀ + (As₀ + (s₀+2)/2) log₂ n⌉}; T03♯'s unnamed onset.
- **Composition (§6)** and the deterministic search (Lemma LS) introduce no A-dependent constant; the search thresholds ℓ_n ≥ c − 1 (scoring) and ℓ_n ≥ c (arrival, certification) do not involve A.

No uniformity over growing A is claimed. All onsets are asymptotic; there is no finite-n guarantee (the proven margins are vacuous at n = 200, §8 (O5)).

## 8 Obstructions, boundaries, and what is not claimed

**(O1) (SIZE) is necessary for this family (counterexample, deterministic; W7-PART CE1/CE2).** If g > B_n, the cut splits every group: blocks ≠ groups surely. If 2g ≤ B_n (the study's groups of 5
with B = 14), next-fit packs ≥ 2 whole groups per bin (equal sizes), so blocks ≠ groups surely; moreover W3-PXN Proposition Q (proof sketch there) indicates the linked pair is co-blocked and masking
disappears. So the masked-regime theorem on LH-iid needs 9 ≤ g ≤ 16 (asymptotically) and does **not** describe the study's own generator (groups of 5). The strongest statement for 2g ≤ B is W7's
"blocks are unions of whole groups"; what the start law and the masking look like then is OPEN.

**(O2) p-range.** The theorem is for p_n ≤ n^A with any fixed A: the only places where polynomial p enters are T03♯ (stated for p_n ≤ n^A), [CONC′] (log p = o(n)), Theorem R (p²e^{−nI*} → 0), and the
union bounds of Tr-J and Lemma E (families of size n^{O(1)}). The discovery half (R, S, E, T) survives log p = o(n) with thresholds t_n ∝ log|family| (CONJECTURE, not written); the posterior half (P)
does not, because T03♯ is not available there. No restriction p ≤ n^A with a specific A is needed.

**(O3) What the (L) failure means.** When some S₀ + l beats S₀ (a first-order heuristic gives order n^{−1/2}(log n)^{−1/2}; the proof gives only P((L) fails) → 0), LS0 still *scores* S₀ (Lemma LS(ii)) and
the posterior term 2E₀δ₁ of (C) accounts for the resulting wrong report; this is a posterior miss, not a discovery miss. Certification fails; recovery is governed by (P).

**(O4) Not claimed.** P(U) → 0; completion of the schedule; masked-regime PIP or evidence accuracy; anything about the original method without LS0 (the earlier no-tweak route is restricted to c = 1 and remains GAP as reviewed;
Lemma Tr-J removes its range objection only; it is not claimed here); anything about adaptive packing of groups of 5; comparative claims; any statement that the rate in (S) is sharp.

**(O5) Finite n.** The margins in (D_S) are (n/2) log(1 + c₂/(4(σ²+M))) − (2A+1) log n − O(1). Illustration: ρ = 0.7, ψ = 0.5, β = 1, v = 0, c = 1: G = 0.1875, η = 0.3675/0.8775, c₂ = G(1−η) = 0.10897; with σ² = 1
(M = 2θᵀΣθ + 1 = 2.5, 4(σ²+M) = 14) one gets (n/2) log(1 + c₂/14) ≈ 0.775 at n = 200 (≈ 0.904 if σ² = 0.5), against (2A+1) log n ≈ 20. The proven margin is therefore vacuous at n = 200 (the conclusion
does not depend on the exact values). The theorem is asymptotic; exact checks of the lattice route at n ∈ {100, 200, 400} (numerical scripts of the source project) succeed because the actual margins are far larger than the
proven lower bound.

**Dependency points of the original candidate (both resolved in this text).** The posterior step uses T03♯ (a fixed-design theorem) with the random-design extension of §5, not the locked T03 (which needs the further
hypothesis H-T02 and is restricted to its own family). The explicit constant of (R) is Theorem R with its display split (§2.3), with the independent summable route (R′) (§2.4) as a fallback; (C) and (P) use only the
summable form.

## Appendix A — Note on the Lean-readiness assessment (not part of the proof)

The source ticket also contains a Lean-readiness assessment of this theorem (assessment only, no formalisation). It contributes no step or premise to the proof above and is excluded from it.
