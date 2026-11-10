# L7 — the master gap theorem SCR-M and its corollaries (geometric noise complexity; uncertified runs)

Origin: proposals 1, 2 and 4 of the better-theorem review R02 (adopted). Notation: g⁻_S denotes the scalar lower bound for the gain defined below (the Gram matrix of L1 is not used here).
Uses L1 (L1.1-L1.4, L1.7), L2 (E2⁺; tools
T1-T3), CODE_CHECK (CC1-CC6). SCR-A and SCR-A° (L3) are special cases (M3 below); their direct proofs are kept.

## Setting
**Family and witnesses.** Let 𝓗 be a family of subsets of [p], each of size ≤ K−1, that is a function of (X, θ*, σ)
only; 𝓗⁻ := {S ∈ 𝓗 : S ⊉ S₀}, M_𝓗 := |𝓗⁻| (if 𝓗⁻ = ∅ everything below is vacuous). For S ∈ 𝓗⁻ let t(S) ∈ S₀∖S be a
witness that is a function of (X, θ*, σ) only. The **default (maximising) witness** is the smallest index maximising
γ(·|S) over S₀∖S (L2); it is the one used in M3, M4 and SCR-G, where γ(t(S)|S) ≥ Γ_n(q) is needed. Write t = t(S),
k = |S|, m_S² = μᵀR_Sμ, and
 d_S := −s_S·R_Sx_t / a(t|S)^{1/2}, s_S := sgn(x_tᵀR_Sμ) (sgn 0 := 1);  e_S := R_Sμ/m_S (e_S := 0 if m_S = 0).
These are centred vectors of R^n with ‖d_S‖ ≤ 1, ‖e_S‖ ≤ 1 (R_S² ⪯ R_S, L1.1).

**Noise complexity.** For a finite set 𝓓 ⊂ R^n of vectors of norm ≤ 1 and g ~ N(0, I_n) let
w(𝓓) := E max_{d∈𝓓∪{0}} dᵀg (Gaussian width; 0 ≤ w(𝓓) ≤ √(2 log(|𝓓| + 1)) and w(𝓓) ≤ √(dim span 𝓓)). For x > 0:
 b_𝓗(x) := min{ √(2 log M_𝓗 + 2x), w({d_S : S ∈ 𝓗⁻}) + √(2x) },
 c_𝓗(x) := min{ √(2 log M_𝓗 + 2x), w({e_S : S ∈ 𝓗⁻}) + √(2x) }.
For 𝓗 = 𝓗_q := {S : |S| ≤ q} (q ≤ K−1): M_𝓗 ≤ N_q, so b_𝓗(x) ≤ r_n(q, x) and c_𝓗(x) ≤ r_n(q, x).

**Deterministic gap.** For S ∈ 𝓗⁻ (with a_x = √(x/(n−1)), τ̄_n(x) = τ_n(1 + 2a_x)):
 B_S := log((2p−1−k)/(k+1)) + ½ log D(t|S)  (≥ 0, since 2p−1−k ≥ k+1 and D ≥ 1);
 g⁻_S := (√γ(t|S) − σ b_𝓗(x))₊²;
 U_S := 1.02 τ̄_n(x)² + (n/(n+1))·[m_S² + 2σ m_S c_𝓗(x) + σ²(n−1)(1 + 2a_x + 2a_x²)];
 Ū_S := min{U_S, (n − 0.98)τ̄_n(x)²};  u_S := n g⁻_S / ((n+1) Ū_S);
 **δ_S := −ν log(1 − u_S) − B_S** if u_S < 1, and δ_S := +∞ if u_S ≥ 1;  δ_𝓗 := min_{S∈𝓗⁻} δ_S.
Conventions: δ_S := +∞ for S ∈ 𝓗∖𝓗⁻; if 𝓗⁻ = ∅, δ_𝓗 := +∞ and b_𝓗, c_𝓗 are not used.
All of these are functions of (X, θ*, σ, x) only.

## Theorem SCR-M (master gap theorem)
Model G, EX-A, x > 0. There is an event 𝓔_M with P(𝓔_M) ≥ 1 − 4e^{-x} on which, for **every** S ∈ 𝓗⁻,
 F(S ∪ t(S)) − F(S) ≥ δ_S,   and S ∪ t(S) ∈ 𝒩(S).
(If Ū_S is replaced by (n − 0.98)τ̄_n(x)² for all S, the event E4_𝓗 below is not needed and the bound is 1 − 3e^{-x}.)

*Proof.* **Events.** E1_𝓗 := {max_{S∈𝓗⁻} d_Sᵀε ≤ σ b_𝓗(x)}; E4_𝓗 := {max_{S∈𝓗⁻} e_Sᵀε ≤ σ c_𝓗(x)}; E2⁺(x) (L2).
P(E1_𝓗ᶜ) ≤ e^{-x}: b_𝓗(x) is the smaller of two deterministic numbers, so it suffices that each of
{max_S d_Sᵀε ≤ σ√(2 log M_𝓗 + 2x)} and {max_S d_Sᵀε ≤ σ(w + √(2x))} has probability ≥ 1 − e^{-x}. First: d_Sᵀε is
N(0, σ²‖d_S‖²) with ‖d_S‖ ≤ 1 (identically 0 if d_S = 0), so P(d_Sᵀε > σ√(2 log M_𝓗 + 2x)) ≤ e^{-x}/M_𝓗 (one-sided
bound P(Z > r) ≤ e^{-r²/(2v²)}); sum over the M_𝓗 sets. Second: ε = σg and f(g) := max_{d∈𝓓∪{0}} dᵀg is 1-Lipschitz
(norms ≤ 1), so by Gaussian concentration (Tsirelson–Ibragimov–Sudakov; Boucheron–Lugosi–Massart 2013, Thm 5.6)
P(f(g) > E f(g) + √(2x)) ≤ e^{-x}. The same argument gives P(E4_𝓗ᶜ) ≤ e^{-x}, and P((E2⁺)ᶜ) ≤ 2e^{-x}. Put
𝓔_M := E1_𝓗 ∩ E4_𝓗 ∩ E2⁺ (intersected with the probability-one event τ̂ > 0).

**Numerator.** Fix S ∈ 𝓗⁻, t = t(S). Since R_Sx_t is centred, x_tᵀR_SCε = (R_Sx_t)ᵀε, and
 s_S·x_tᵀR_Sy_c / a(t|S)^{1/2} = |x_tᵀR_Sμ|/a(t|S)^{1/2} + s_S(R_Sx_t)ᵀε/a(t|S)^{1/2} = √γ(t|S) − d_Sᵀε ≥ √γ(t|S) − σ b_𝓗(x)
on E1_𝓗. If the right side is ≥ 0 this gives g_{y_c}(t|S) ≥ (√γ(t|S) − σ b_𝓗)²; otherwise g⁻_S = 0 ≤ g_{y_c}(t|S). So
g_{y_c}(t|S) ≥ g⁻_S.

**Denominator.** By L1.1, 0.02τ̂² + q_S(y_c) = [0.02 + (n−1)/(n+1)]τ̂² + (n/(n+1))y_cᵀR_Sy_c, and (R_Sμ centred, R_S ⪯ I)
y_cᵀR_Sy_c = m_S² + 2μᵀR_SCε + (Cε)ᵀR_S(Cε) ≤ m_S² + 2m_S·e_Sᵀε + ‖Cε‖² ≤ m_S² + 2σ m_S c_𝓗(x) + σ²(n−1)(1 + 2a_x + 2a_x²)
on E4_𝓗 ∩ E2⁺ (μᵀR_Sε = m_S e_Sᵀε, also when m_S = 0). With τ̂ ≤ τ̄_n(x) on E2⁺: 0.02τ̂² + q_S(y_c) ≤ U_S. Also
0.02τ̂² + q_S(y_c) = (0.02 + Q_S)τ̂² ≤ (n − 0.98)τ̄_n(x)² (Q_S ≤ n−1, L1.1). Hence 0.02τ̂² + q_S(y_c) ≤ Ū_S.

**Gap.** By L1.4 (k ≤ K−1) and L1.2(iii),
 F(S∪t) − F(S) = −B_S − ν log(1 − u),  u := (n/(n+1))·g_{y_c}(t|S)/(0.02τ̂² + q_S(y_c)) = 1 − (0.02 + Q_{S∪t})/(0.02 + Q_S) ∈ [0, 1).
On 𝓔_M, u ≥ n g⁻_S/((n+1)Ū_S) = u_S; in particular u_S < 1 there, and −ν log(1 − u) ≥ −ν log(1 − u_S). So
F(S∪t) − F(S) ≥ δ_S. (If u_S ≥ 1 for some S the event 𝓔_M is empty and the claim is void.) |S| < K gives S∪t ∈ 𝒩(S). ∎

## Corollaries (all on 𝓔_M; "scanned centre" = completely scanned centre of `fit$local_search` or `fit$ls0`
## on a completed run)

**M1 (screening; any deterministic family).** If δ_S > 0 for every S ∈ 𝓗⁻, then every LO model that belongs to 𝓗
contains S₀; in particular every certified model C ∈ 𝒞 ∩ 𝓗, and Ŝ when `local_certified` and Ŝ ∈ 𝓗.
*Proof.* An LO model S ∈ 𝓗⁻ would have F(S∪t(S)) ≤ F(S) with S∪t(S) ∈ 𝒩(S), contradicting the theorem. CC2-CC3. ∎

**M2 (near-best scanned centres; no certificate needed).** Every scanned centre C ∈ 𝓗⁻ satisfies
F(Ŝ) − F(C) ≥ δ_C. Hence every scanned centre C ∈ 𝓗 with F(Ŝ) − F(C) < δ_C (in particular with F(Ŝ) − F(C) < δ_𝓗)
contains S₀.
*Proof.* If C ∈ 𝓗⁻ then |C| ≤ K−1, so the addition C∪t(C) ∈ 𝒩(C) was scanned, scored and reached the ledger; hence
F(Ŝ) ≥ F(C∪t(C)) ≥ F(C) + δ_C (CC6 and the theorem). ∎

**M5 (the coded search does not drop truths; capped searches).** Assume δ_S > 0 for every S ∈ 𝓗⁻. Let C be a
scanned centre with C ⊇ S₀ (C need not belong to 𝓗), and let N be the best scanned neighbour of C, with F(N) > F(C)
(the model the search moves to, or returns when it stops on its move cap). If N ∈ 𝓗, then N ⊇ S₀. Consequently: (i) along the path of a
search, once a scanned centre contains S₀, every later model of the path that belongs to 𝓗 — as long as all models in
between do — contains S₀; (ii) if a search stops on its move cap with last scanned centre C ∈ 𝓗, returned model N ∈ 𝓗
and F(Ŝ) − F(C) < δ_C, then C ⊇ S₀ and N ⊇ S₀ — in particular when Ŝ = N, a reported model that this capped search
did not certify (N was scored as a neighbour of C but not scanned as a centre of this search).
*Proof.* N arises from C by one addition, deletion or swap. If N ⊉ S₀ while C ⊇ S₀, N is a deletion C∖{t} or a swap
C∖{t}∪{l} with t ∈ S₀, and S₀∖N = {t}, so t(N) = t. Then N∪t is C (deletion) or C∪{l} (swap). F(C) < F(N); and for
a swap |C| = |N| ≤ K−1, so C∪{l} ∈ 𝒩(C) was scanned and F(C∪{l}) ≤ F(N) (N is the best scanned neighbour of C). In
both cases F(N∪t(N)) ≤ F(N), contradicting F(N∪t(N)) ≥ F(N) + δ_N > F(N) (N ∈ 𝓗⁻). (i) is induction; (ii) is M2
followed by the first statement (CC6: `returned` on a capped search is that best neighbour). ∎

**M3 (SCR-A and SCR-A° are special cases).** Let 𝓗 = 𝓗_q, q ≤ K−1, with the default witness. If MC(q, x) holds, or
if MC°(q, x) holds, then δ_S > 0 for every S ∈ 𝓗⁻.
*Proof.* Put L′ := 2 log(2p−1) + log(n+1), so T_n = (n+1)L′/n, and note 1 − e^{-B_S/ν} ≤ B_S/ν ≤ (L′/2)/ν = L′/(n+0.02)
(L1.3). δ_S > 0 iff u_S ≥ 1 or u_S > 1 − e^{-B_S/ν}; so it suffices that u_S > L′/(n + 0.02).
Under MC: √γ(t|S) − σ b_𝓗 ≥ √Γ_n(q) − σ r_n > τ̄_n(x)√T_n > 0, so g⁻_S > τ̄_n(x)²T_n and, using Ū_S ≤ (n − 0.98)τ̄_n(x)²,
u_S > nT_n/((n+1)(n − 0.98)) = L′/(n − 0.98) > L′/(n + 0.02).
Under MC°: √γ(t|S) − σ b_𝓗 ≥ σ_S(√Ψ_n(q) − r_n) > σ_S√(T_n(1 + ϑ°_n)) (σ ≤ σ_S), so g⁻_S > σ_S²T_n(1 + ϑ°_n). By AM–GM
(2σ m_S ≤ σ_S²√(n−1)), m_S² + σ²(n−1) = (n−1)σ_S², σ ≤ σ_S and c_𝓗 ≤ r_n:
U_S ≤ 1.02τ̄_n(x)² + (n/(n+1))(n−1)σ_S²(1 + 2a_x + 2a_x² + r_n/√(n−1)) ≤ (n−1)σ_S²(1 + ϑ°_n). Hence
u_S > nT_n/((n+1)(n−1)) = L′/(n−1) > L′/(n + 0.02). ∎

**M4 (the gap is of order n under the hypotheses of A1).** Assume the hypotheses of Corollary A1 (with φ^d_n(q_n) ≥ κ; κ, b, M, σ fixed, not
depending on n — the "for large n" steps below use this) and 𝐋_n := (q_n + 1) log p + log n = o(n). Take 𝓗 = 𝓗_{q_n} with the default (maximising) witness, x_n = √(log n). Then for all large n
 δ_S > c₂ n for every S ∈ 𝓗⁻ (so δ_𝓗 > c₂n),  c₂ := κ²b² / (104(M² + σ²)).
*Proof.* As in A1 (L3): Γ_n(q_n) ≥ κ²b²n/16 for large n and τ_n² ≤ τ_*² := M² + σ². r_n(q_n, x_n)² ≤ 2q_n log p + 2 log 2
+ 2 + 2x_n = o(n), so √(g⁻_S) ≥ √Γ_n(q_n) − σ r_n ≥ κb√n/5 for large n, i.e. g⁻_S ≥ κ²b²n/25. Also
Ū_S ≤ (n − 0.98)τ̄_n(x_n)² ≤ 1.01 nτ_*² for large n. So u_S ≥ (n/(n+1))κ²b²/(25.25τ_*²) ≥ u* := κ²b²/(26τ_*²) for
n ≥ 34. Here u* ≤ 1/26: the directional floor satisfies κ ≤ φ^d_n(q_n) ≤ ‖Xθ*‖²/((n−1)‖θ*‖₂²) ≤ ‖θ*‖₁²/‖θ*‖₂² ≤ ‖θ*‖₁/b
≤ M/b (take S = ∅ in the definition; ‖Xθ*‖ ≤ ‖θ*‖₁√(n−1); ‖θ*‖₂² ≥ b‖θ*‖₁), so κb ≤ M ≤ τ_*. If u_S ≥ 1, δ_S = +∞;
otherwise −ν log(1 − u_S) ≥ νu_S ≥ nu*/2, and B_S ≤ log(2p−1) + ½ log(n+1) = o(n) uniformly in S. Hence
δ_S ≥ nu*/2 − o(n) > nu*/4 = c₂n for all large n, uniformly in S ∈ 𝓗⁻. ∎
(SCR-G of STATEMENT.md follows: with x_n = √(log n) the event 𝓔_M has probability ≥ 1 − 4e^{-√(log n)} → 1; on it,
`hpm_F` − F(C) ≤ c₂n < δ_𝓗 gives (i) by M2; (ii) is M2 followed by M5; (iii) is M5(i). M5 needs δ_S > 0 on 𝓗⁻, which
holds. The statements concern completed runs — a capped search is a completed search — and the searches that were
run.)

**M6 (why the model count is not always the right complexity).** If the witness directions d_S, S ∈ 𝓗⁻, span a
subspace of dimension r, then b_𝓗(x) ≤ √r + √(2x) whatever the number of models. Example of an admissible situation
(illustration only): S₀ = {1} and x_1 orthogonal to all other columns; then R_Sx_1 = x_1 for every S ∌ 1, all d_S
coincide, so b_𝓗(x) ≤ 1 + √(2x) for the family 𝓗 of **all** models of size ≤ K−1; γ(1|S) = θ*_1²(n−1)²(n+1)/n² for
every S ∌ 1; and, using the branch Ū_S ≤ (n − 0.98)τ̄_n(x)², δ_S > 0 for all large n when θ*_1 ≠ 0, σ and x are fixed
(not depending on n) and log p = o(n). So M1 applies up to size K−1, with no entropy term q log p at all.
