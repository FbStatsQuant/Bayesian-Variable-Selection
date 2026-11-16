# A2C — Proposition A2C: the critical scale on the orthogonal witness (W3-PSHARP-R, claim `W3-PSHARP-R:A2C`)

Status: **PROVED (by this seat, unchecked)**. Statement: `../STATEMENT.md` v1.1 §3.4. PARENT := `Theory_work/Wave3/W3-PSHARP/`;
"P-A :a-b" := PARENT `lemmas/A_log_factor.md` lines a-b; "P-ST :a" := PARENT `STATEMENT.md` line a.
Consumed, unchanged: Lemma S(1) (with its equality case), S(2), S(3) (`W3-PSHARP:S`@1.0.0, P-ST :36-40); from the proof of
`W3-PSHARP:A`@1.0.0: the identity (0) for Λ_n (P-A :8-10), Lemma W and W(i) (P-A :12-24), the first step of the proof of
Lemma R (P-A :45-46), the (W-orth) identities and the κ-event bound (P-A :53-68), and the A2 asymptotics of Λ_n (P-A :121).

**Hypotheses.** Setting of P-ST :48-50 (with N_n → ∞), (W-orth) (P-ST :54-55), 𝒩_n = [p]∖S₀, p → ∞, s₀/p → 0, and
Λ_n → λ ∈ [0, ∞), Λ_n := (s₀ + 1)·[2N/(2p − 1 − s₀)]·√(log N/(πn)), N := N_n = p − s₀. odds := δ_n/(1 − δ_n);
P_n := (s₀ + 1)/(2p − 1 − s₀), c_n := P_n n^{−1/2}.
**Claim.** For every η > 0: P(odds ≥ e^λ − 1 − η) → 1; equivalently P(π(S₀) ≤ e^{−λ} + η) → 1; and
limsup E π(S₀) ≤ e^{−λ}, liminf E δ_n ≥ 1 − e^{−λ}.

If λ = 0 the claim is trivial (odds ≥ 0 > −η; π(S₀) ≤ 1 = e^{0}; E δ_n ≥ 0). Let λ > 0.

## 1. Sizes
By P-A :121, Λ_n = (1 + o(1))(s₀ + 1)√(log p/(πn)). As Λ_n is bounded and log p → ∞, (s₀ + 1)/√n → 0; so s₀ = o(√n).
Hence ⌊n/2⌋ − s₀ → ∞, and p − s₀ ≥ p/2 → ∞ for n large (s₀/p → 0); so **K − s₀ → ∞** and N → ∞. Also
  c_nN = (s₀ + 1)N/((2p − 1 − s₀)√n) ≤ (s₀ + 1)/√n → 0   (N = p − s₀ ≤ 2p − 1 − s₀).                              (1.1)

## 2. Multi-step supersets on the orthogonal block
Let J ⊆ 𝒩_n, |J| = j ≥ 1, s₀ + j ≤ K. Write J = {k_1, …, k_j} and S^{(i)} := S₀ ∪ {k_1, …, k_i} (S^{(0)} = S₀); each
S^{(i)} ∈ Ω. For 1 ≤ i ≤ j, x_{k_i} is orthogonal to every column of S^{(i−1)} ((W-orth): the null columns are mutually
orthogonal and orthogonal to col X_{S₀}), so g := g_{S^{(i−1)},k_i} = X_{S^{(i−1)}}ᵀx_{k_i} = 0. Lemma S applied with
S = S^{(i−1)} (|S| + 1 ≤ K):
- S(1), equality case: D_{S^{(i)}}/D_{S^{(i−1)}} = n;
- S(2): s_{S,k_i} = n² − (n + 1)²gᵀH_S⁻¹g = n², and x_{k_i}ᵀρ̃_S = x_{k_i}ᵀy − (n + 1)gᵀH_S⁻¹X_Sᵀy = x_{k_i}ᵀy, so
  Q_{S^{(i−1)}} − Q_{S^{(i)}} = n(x_{k_i}ᵀy)²/n² = (x_{k_i}ᵀy)²/n.
The same computation with S = S₀ gives Q_{S₀} − Q_{S₀∪{k}} = (x_kᵀy)²/n for each k ∈ 𝒩_n. Summing over i:
  D_{S₀∪J}/D_{S₀} = n^j,   Q_{S₀} − Q_{S₀∪J} = Σ_{k∈J}(Q_{S₀} − Q_{S₀∪{k}}),
so, with γ_k as in P-ST :29, 2b₀ + Q_{S₀∪J} = (2b₀ + Q_{S₀})(1 − Σ_{k∈J}γ_k). The left side is > 0 (Q ≥ 0 by S(2), b₀ > 0),
so Σ_{k∈J}γ_k < 1; and γ_k ≥ 0 (S(3)). The prior ratio is
  w(s₀ + j)/w(s₀) = C(2p − 1, s₀)/C(2p − 1, s₀ + j) = Π_{i=0}^{j−1} (s₀ + 1 + i)/(2p − 1 − s₀ − i) ≥ P_n^j,
each factor being ≥ P_n (numerators increase, denominators decrease and stay ≥ 2p − s₀ − j ≥ p > 0 as s₀ + j ≤ p).
Therefore, by the definition of π (P-ST :21) and log(1 − x) ≤ −x on [0, 1):
  π(S₀∪J)/π(S₀) = [w(s₀ + j)/w(s₀)]·n^{−j/2}·(1 − Σ_{k∈J}γ_k)^{−ν} ≥ c_n^j Π_{k∈J} V_k,   V_k := e^{νγ_k}.
The models S₀∪J are distinct for distinct J and differ from S₀. So for every J₀ ≤ min(N, K − s₀):
  odds = Σ_{S≠S₀} π(S)/π(S₀) ≥ Σ_{j=1}^{J₀} c_n^j e_j(V),                                                         (2.1)
e_j the j-th elementary symmetric polynomial of (V_k)_{k∈𝒩_n}.

## 3. Truncation (from PARENT)
Under (W-orth), νγ_k = κ_n g_k²/2 for all k ∈ 𝒩_n, with one common κ_n and g_k iid N(0, 1) (P-A :53-59). Let τ := 2 log N
and W_k := e^{g_k²/2}1{g_k² ≤ τ} ≤ N. For fixed ϵ ∈ (0, 1), the event 𝒦_n := {κ_n ≥ 1 − ϵ/τ} has P(𝒦_n) → 1 (P-A :64-68,
which use N ≤ n − 1), and on 𝒦_n, V_k ≥ e^{−ϵ/2}W_k for every k (P-A :46). Since e_j is nondecreasing in each argument on
[0, ∞)^N and homogeneous of degree j, on 𝒦_n: c_n^j e_j(V) ≥ e^{−jϵ/2} e_j(a), a_k := c_nW_k.

## 4. A collision bound
For a ∈ [0, ∞)^N, A := Σ_k a_k, B := Σ_k a_k² and j ≥ 2:  j!·e_j(a) ≥ A^j − C(j, 2)·B·A^{j−2}.
*Proof.* A^j = Σ_{(k_1,…,k_j)∈𝒩^j} Π_i a_{k_i}. The tuples with distinct entries contribute j!e_j(a). Every other tuple has
k_i = k_{i′} for some pair i < i′; for a fixed pair, the tuples with k_i = k_{i′} contribute B·A^{j−2}. All terms are ≥ 0,
so the remaining tuples contribute at most C(j, 2)BA^{j−2}. ∎ (For j = 1, e_1(a) = A.)

## 5. Conclusion
Put A_n := c_nΣ_kW_k and B_n := c_n²Σ_kW_k² ≤ c_n²N·Σ_kW_k = (c_nN)A_n (W_k ≤ N).
- E A_n = c_nN·E W_1 = c_nN√(2τ/π) = Λ_n (Lemma W(i), P-A :23, exact; identity (0), P-A :9). So A_n = O_P(1).
- Lemma W with η = η′ = 0 (P-A :15-17): for ϵ′ ∈ (0, 1), P(A_n < (1 − ϵ′)Λ_n) ≤ √π/(2ϵ′²√(log N)) → 0.
- B_n ≤ (c_nN)A_n = o_P(1) by (1.1).
By §3–§4, on 𝒦_n and for J₀ ≤ min(N, K − s₀) (true for n large, for any fixed J₀, by §1), (2.1) gives
  odds ≥ Σ_{j=1}^{J₀} e^{−jϵ/2}(A_n^j − C(j, 2)B_nA_n^{j−2})/j! ≥ F(A_n) − R_n,
  F(u) := Σ_{j=1}^{J₀}(e^{−ϵ/2}u)^j/j!,   R_n := B_n Σ_{j≥2} C(j, 2)A_n^{j−2}/j! = B_n e^{A_n}/2 = o_P(1).
Fix η > 0. Choose J₀, then ϵ, ϵ′ ∈ (0, 1), such that F((1 − ϵ′)²λ) ≥ e^λ − 1 − η/2 (possible: as J₀ → ∞ and ϵ, ϵ′ → 0 the
left side tends to e^λ − 1). For n large, (1 − ϵ′)Λ_n ≥ (1 − ϵ′)²λ, and F is increasing, so
  {odds < e^λ − 1 − η} ⊆ 𝒦_nᶜ ∪ {A_n < (1 − ϵ′)Λ_n} ∪ {R_n > η/2},
whose probability tends to 0. This is the first claim.
*Equivalence.* π(S₀) = 1/(1 + odds). If odds ≥ e^λ − 1 − η with η < e^λ, then π(S₀) ≤ 1/(e^λ − η), and
1/(e^λ − η) ≤ e^{−λ} + η′ once η ≤ η(η′, λ); conversely π(S₀) ≤ e^{−λ} + η′ gives odds ≥ 1/(e^{−λ} + η′) − 1 ≥ e^λ − 1 − η for
η′ ≤ η′(η, λ). So the two families of statements (over all η > 0, resp. η′ > 0) are equivalent.
*Expectation.* Since 0 ≤ π(S₀) ≤ 1: E π(S₀) ≤ e^{−λ} + η′ + P(π(S₀) > e^{−λ} + η′); take limsup, then η′ ↓ 0:
limsup E π(S₀) ≤ e^{−λ}, i.e. liminf E δ_n ≥ 1 − e^{−λ}. ∎

## 6. Remarks
1. **Comparison.** PARENT Cor A2 gives odds ≥ (1 − o_P(1))Λ_n, i.e. at the critical scale limsup π(S₀) ≤ 1/(1 + λ) in
   probability; here e^{−λ} < 1/(1 + λ). Corollary B's critical cap e^{−λ_B/2} (P-ST :101-102) is on every design, with
   λ_B = lim s₀/√n; the two scales differ by √(log p/π).
2. **Scope.** The proof uses the exact multi-step identities of §2, which need the whole null block orthogonal. On (W-sph)
   the multi-step fit factors are not additive; that version is not attempted (STATEMENT §5).
