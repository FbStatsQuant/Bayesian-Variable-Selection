# X-b-2
stop_reason: end_turn

# Card X, route X-b — attempt

**Result in one line.** The literal X-b (untruncated moment at exponent 1, Lemma V(b), Markov) cannot give the cut d_t = s₀ + C′t/log n; it gives only s₀ + Θ(t). Replacing exponent 1 by a fractional exponent λ = 1 − 1/log n, still without truncated moments, proves Lemma X as stated, with c = ½. The proof below is self-contained modulo [P1] and two standard tail inequalities, and has not been checked by a second reader.

Notation: σ² := σ*², B := M + M′, e ~ N_N(0, σ²I), E′ := ‖e‖²/σ², k = |S|, a_S := (I − M_S)μ_c (so ‖a_S‖² ≤ L_S), D₀ := D_{S₀}, Q_S := Q^c_S, Q₀ := Q_{S₀}.

## 1. Why the literal X-b does not reach d_t

**(1) The exponent-1 moment removes the Occam factor.** Let Σ_S := I + nX_{c,S}(G_S + I)⁻¹X_{c,S}ᵀ. By Woodbury, Σ_S⁻¹ = I − M_S; its eigenvalues are f(λ_i(G_S)) and 1, so det Σ_S = D_S ([P1] `lem:spec`(e)). Put
  B_S := D_S^{−1/2} exp{(‖e‖² − Q_S)/(2σ²)}.
This is the ratio of the N(0, σ²Σ_S) density to the N(μ_c, σ²I) density at y_c, so **E B_S = 1 for every S and every design.**

- For s₀ = 0 the first moment of Σ_{|J|=j}[w(j)/w(0)]B_J equals 2q_j ≍ 2^{−j} exactly, whatever (ND) says.
- Lemma V(b)'s bound (1+η)^{s₀+j/2} is the same phenomenon: the factor (D₀/D_S)^{1/2} is consumed by the moment generating function.
- Hence Markov at exponent 1 gives Σ_{|J|=j} ≤ 2(j+1)^{s₀}(√(1+η)/2)^j · e^{O(t + s₀ log n + ρ′/η)}. The cut must satisfy j₁ log(2/√(1+η)) ≥ O(t + s₀(A+½) log n), so j₁ ≍ t.
- That is the order of m_n(t). (ND) is never used, and the fitted-noise bound becomes σ²(d log p + t) ≍ tℓ_n. So the literal X-b proves Lemma X′, not Lemma X.

The mean of B_S is carried by events of probability about κ^{−1/2} (κ the Occam eigenvalue). X-a removes them by truncation; a fractional power removes them without truncation.

**(2) Side remark.** The exponent actually needed is θ/2 with θ = 2ν/(N(1−δ)) > 1 (variance surcharge). Since λ_max(M_S) ≥ 1 − 1/n for S ≠ ∅ and θ(1 − 1/n) > 1, E exp{θeᵀM_Se/(2σ²)} = ∞. The surplus must be bounded deterministically on a noise event in any version; this is done in Step B.

## 2. Proof of Lemma X by fractional moments

### 2.1 Facts used

- **(F1)** [P1] `lem:chi`(a): P(χ²_r ≥ 2d log 2 + 4x) ≤ e^{−x} for r ≤ d.
- **(F2)** Laurent–Massart (2000, Ann. Statist. 28, Lemma 1): P(χ²_N ≥ N + 2√(Nx) + 2x) ≤ e^{−x} and P(χ²_N ≤ N − 2√(Nx)) ≤ e^{−x}.
- **(F3)** For G ~ Gamma(ν, 1): P(G ≥ ν + √(2νx) + x) ≤ e^{−x} and P(G ≤ ν − √(2νx)) ≤ e^{−x}. Proof: log E e^{s(G−ν)} = −ν log(1−s) − νs ≤ νs²/(2(1−s)), which is sub-gamma (Boucheron–Lugosi–Massart 2013, §2.4); log E e^{−s(G−ν)} ≤ νs²/2, then Chernoff.
- **(F4)** [P1] `lem:prior`:
  - Σ_{k≤p} q_k = 1 and Σ_{k>m} q_k ≤ 2^{−m} for m ≥ 0;
  - 1/w(s₀) ≤ 2(2p)^{s₀};
  - w(l)/w(l+1) ≤ 2p for l ≤ p − 1;
  - C(p−s₀, j)w(s₀+j)/w(s₀) ≤ 2(j+1)^{s₀}2^{−j} for j ≥ 1, s₀ + j ≤ p.
- **(F5)** For S ⊆ S′: D_{S′}/D_S ≤ (n+1)^{|S′∖S|}, and 1 ≤ D_S. Proof: D = Π f(λ_i(G)) with f increasing and 1 ≤ f < n+1. Cauchy interlacing gives λ_i(G_{S′}) ≤ λ_i(G_S) for i ≤ |S| (increasing order), so D_S ≥ Π_{i≤|S|} f(λ_i(G_{S′})).
- **(F6)** Q₀ ≤ ‖e‖² + B and L₀ ≤ B. Proof: put φ = θ*_{S₀} in the min-representations; X_{c,S₀}θ* = μ_c and the penalty is (‖μ‖² + ‖θ*‖²)/n ≤ B.
- **(F7)** For every S:
  - Q_S = eᵀ(I − M_S)e + 2eᵀa_S + L_S, with 0 ≤ eᵀM_Se ≤ ‖P_Se‖²;
  - ‖M_Sy_c − μ_c‖² ≤ 2‖P_Se‖² + 2L_S;
  - π(S)/π(S₀) = [w(k)/w(s₀)](D₀/D_S)^{1/2}((2b + Q₀)/(2b + Q_S))^ν.
- **(F8)** [P1] `thm:Ta` and `lem:num`. On 𝓑_n := {b₋ ≤ b ≤ b₊}, for a model event E: π(E) ≤ κ² I_{b₋}(E)/(ϖ(S₀)m^c_{b₊}(S₀)). And E₀[I_{b₋}(E)/f₀(y_c)] = ϖ(E), with f₀ the N(μ_c, σ²I) density. Here b₋ = 0.005σ², b₊ = 0.01(2(σ² + M) + 1), κ = (b₊/b₋)^{0.51}.

**Lemma F (fractional moment; replaces Lemma V).** For every S ⊆ [p] and λ ∈ (0, 1):
  E B_S^λ ≤ (1 − λ)^{−|S|/2} D_S^{−λ/2} · exp{−λ(1−λ)L_S/(2σ²)}.

*Proof.* With y = μ_c + e and q(y) := λyᵀΣ_S⁻¹y + (1−λ)‖y − μ_c‖²,
  E B_S^λ = D_S^{−λ/2}(2πσ²)^{−N/2}∫e^{−q(y)/(2σ²)}dy = D_S^{−λ/2} det(Λ)^{−1/2} e^{−q_min/(2σ²)},  Λ := λΣ_S⁻¹ + (1−λ)I.
The eigenvalues of Λ are λ/f(g_i) + 1 − λ ≥ 1 − λ on at most |S| directions and 1 elsewhere, so det Λ ≥ (1−λ)^{|S|}. Also q_min = (1−λ)μ_cᵀ[I − (1−λ)Λ⁻¹]μ_c = λ(1−λ)μ_cᵀ(λI + (1−λ)Σ_S)⁻¹μ_c ≥ λ(1−λ)μ_cᵀΣ_S⁻¹μ_c = λ(1−λ)L_S, because λI + (1−λ)Σ_S ⪯ Σ_S. ∎

No eigenvalue condition is used, and S need not contain S₀.

### 2.2 Constants (evaluated at s₀ = s₀^r; all are nondecreasing in s₀)

- C_B := 6A + 7; C_m := s₀ + 1 + 1.45(s₀(A+2) + 5); K_{s₀} := Σ_{l≥0}(l+1)^{s₀}2^{−l}.
- C₀ := log(4K_{s₀}) + B/σ² + C_Bs₀.
- **C′ := 4(C₀ + 13 + s₀(A+4))**.
- C₂ := (8A+9)(s₀+1+C′) + 16.
- C″ := max{4(C₂ + B/σ²), 16(s₀(A+2)+2)/log 2}.
- **M₀ := 15**, so t ≥ 16 and log n ≤ t.
- λ := 1 − 1/log n; m̄ := m_n(t); x_k := k log p + k + 2t; τ_k := 2k log 2 + 4x_k; T_k := τ_k + 2x_k.

Using p ≤ n^A and log n ≥ log 3:
- T_k ≤ C_Bk log n + 12t;
- τ_k + 4x_k ≤ (8A+9)k log n + 16t;
- m̄ ≤ C_mt.

Further:
- δ_{n,t} := [2√(Nt) + C_Bm̄ log n + 12t]/N;
- θ := 2ν/(N(1 − δ_{n,t})) ≥ 1.

On t ≤ n^{1−κ₀}, sup_t δ_{n,t} · log n → 0. "n ≥ n₀" below means finitely many conditions of this uniform type, depending only on the listed constants; this gives one n₀ for the whole t-range. In particular, for n ≥ n₀: δ_{n,t} ≤ ½ and θ − 1 ≤ 2δ_{n,t} + 2.04/N ≤ 1/log n, so θ ≤ 2 and θ − λ ≤ 2/log n.

### 2.3 Noise event 𝓔_t

- (i) |E′ − N| ≤ 2√(Nt) + 2t.
- (ii) ‖P_Se‖² ≤ σ²τ_k for all S with k ≤ m̄.
- (iii) |eᵀa_S| ≤ σ‖a_S‖√(2x_k) for all S with k ≤ m̄ (k = 0 included: a_∅ = μ_c).

By (F2), (F1) and the Gaussian tail, with at most p^k sets of size k:
P(𝓔_tᶜ) ≤ 2e^{−t} + Σ_{k≥1}p^ke^{−x_k} + 2Σ_{k≥0}p^ke^{−x_k} ≤ 2e^{−t} + 3.8e^{−2t}.

Consequences on 𝓔_t, for n ≥ n₀:

- **(N1)** 𝓔_t ⊆ 𝓑_n. Indeed ‖y_c‖² ≥ ‖e‖² + ‖μ‖² − 4σ‖μ‖√t ≥ ‖e‖² − 4σ²t, so s_y² ≥ σ²/2. And ‖y_c‖² ≤ 2nM + 2‖e‖², so s_y² ≤ 2(σ² + M) + 1. Hence 2b ≤ 2b₊.
- **(N2)** For k ≤ m̄, by (F7), (ii), (iii) and L − 2σ√(2xL) ≥ −2σ²x:
  Q_S ≥ ‖e‖² − σ²T_k ≥ Nσ²(1 − δ_{n,t}).
  That is, a_S⁎ := ‖e‖² − Q_S ≤ σ²T_k.
- **(N3)** For k ≤ m̄, using 2σ√(2xL) ≤ L/2 + 4σ²x: Q_S ≥ ‖e‖² − σ²(τ_k + 4x_k) + L_S/2.
- **(N4)** For k ≤ m̄: |Q_S − ‖e‖²| ≤ σ²T_k + 2L_S.

### 2.4 Partition of Ω

With d_t := s₀ + ⌈C′t/log n⌉:
- 𝒜₁ := {k > m̄};
- 𝒜₂ := {d_t < k ≤ m̄};
- 𝒜₃ := {k ≤ min(d_t, m̄), L_S > C″σ²t};
- 𝒢 := {k ≤ min(d_t, m̄), L_S ≤ C″σ²t}.

Every S with k > d_t lies in 𝒜₁ ∪ 𝒜₂. Throughout π(𝒜) ≤ π(𝒜)/π(S₀) (S₀ ∈ Ω).

### Step A: 𝒜₁ (prior tail; no (ND))

If m̄ = K there is nothing to prove. Otherwise 2^{−m̄} ≤ 2^{−s₀}(2p)^{−s₀}(n+1)^{−(s₀+2)/2}e^{−3t}. By (F4), ϖ(𝒜₁)/ϖ(S₀) ≤ 2(2p)^{s₀}2^{−m̄}, and with D₀ ≤ (n+1)^{s₀}:
  [ϖ(𝒜₁)/ϖ(S₀)]√D₀√n ≤ 2n^{−1/2}e^{−3t}.

*Denominator* (body of [P1] `lem:den` with (F6)). 
  m^c_{b₊}(S₀)/f₀ = D₀^{−1/2}∫exp{−(N/2)log(v/σ²) + E′/2 − Q₀/(2v)} IG(v; 0.51, b₊)dv.
For v = σ²u with 1 ≤ u ≤ 1 + n^{−1/2}, using Q₀ ≤ σ²E′ + B, log u ≤ u − 1 and 1/u ≥ 2 − u, the exponent is at least −Λ, where
  Λ := |E′ − N|/(2√n) + E′/(2n) + B/(2σ²).
Hence m^c_{b₊}(S₀)/f₀ ≥ D₀^{−1/2}c_IGσ²n^{−1/2}e^{−Λ}, with c_IG := min_{[σ²,2σ²]}IG(·; 0.51, b₊). On 𝓔_t, Λ ≤ B/(2σ²) + ½ + 2√t + 2t/√n.

*Numerator.* Θ^{(1)} := I_{b₋}(𝒜₁)/(f₀ϖ(𝒜₁)) has mean 1 by (F8), so P(Θ^{(1)} > e^t) ≤ e^{−t}.

*Conclusion.* On 𝓔_t ∩ {Θ^{(1)} ≤ e^t}, by (F8) and (N1), with c♯ = κ²/(c_IGσ²):
  π(𝒜₁) ≤ 2n^{−1/2}e^{−3t} · c♯e^{B/(2σ²) + ½ + 2√t + 2t/√n} · e^t ≤ e^{−t}
for n ≥ n₀, since t ≥ 16 gives 2√t ≤ t/2 and n ≥ 16 gives 2t/√n ≤ t/2.

### Step B: 𝒜₂ (supersets and non-supersets together; fractional moment + (ND))

**B1 (pointwise, on 𝓔_t).** Let S ∈ 𝒜₂. If Q₀ ≥ Q_S, then (1+ξ)^ν ≤ e^{νξ} with ξ = (Q₀ − Q_S)/(2b + Q_S) ≤ (Q₀ − Q_S)/(Nσ²(1 − δ_{n,t})) by (N2). If Q₀ < Q_S the factor is ≤ 1. So
  ((2b + Q₀)/(2b + Q_S))^ν ≤ exp{θ(Q₀ − Q_S)₊/(2σ²)}.
By (F6), (Q₀ − Q_S)₊ ≤ B + (a_S⁎)₊. By (N2), for 0 < a_S⁎ ≤ σ²T_k,
  e^{θa_S⁎/(2σ²)} ≤ e^{(θ−λ)T_k/2}e^{λa_S⁎/(2σ²)}.
Using D_S^{−1/2}e^{λa_S⁎/(2σ²)} = D_S^{−(1−λ)/2}B_S^λ ≤ B_S^λ and D_S^{−1/2} ≤ D_S^{−λ/2}:
  π(S)/π(S₀) ≤ e^{θB/(2σ²)} [w(k)/w(s₀)] D₀^{1/2} [D_S^{−λ/2} + e^{(θ−λ)T_k/2}B_S^λ].

**B2 (moment).** Let V := Σ_{S∈𝒜₂}[w(k)/w(s₀)]D₀^{1/2}e^{(θ−λ)T_k/2}B_S^λ; its weights are deterministic. By Lemma F,
  E V ≤ Σ_{k=d_t+1}^{m̄} g_k Z_k,  g_k := e^{(θ−λ)T_k/2}(1−λ)^{−k/2},  Z_k := Σ_{|S|=k}[w(k)/w(s₀)]D₀^{1/2}D_S^{−λ/2}.
No truncation is used: the full untruncated λ-moment is finite and carries the factor D_S^{−λ/2}.

**B3 (the Occam sum under (ND)).** For |S| = k write J := S∖S₀, j := |J|, i := |S ∩ S₀| = k − j. Then j ≥ k − s₀ ≥ 1 and j ≤ min(m̄, p − s₀).

- By (F5), D_S^{−λ/2} ≤ (n+1)^{λs₀/2}D_{S₀∪J}^{−λ/2}, so D₀^{1/2}D_S^{−λ/2} ≤ (n+1)^{s₀/2}(D₀/D_{S₀∪J})^{λ/2}.
- By Jensen (x ↦ x^λ concave) and (ND; c_D, m̄): Σ_{|J|=j}(D₀/D_{S₀∪J})^{λ/2} ≤ C(p−s₀, j)[c_D(n+1)]^{−λj/2}.
- By (F4): w(i+j) ≤ (2p)^{s₀−i}w(s₀+j) and C(p−s₀, j)w(s₀+j)/w(s₀) ≤ 2(j+1)^{s₀}2^{−j}.

Each J arises from C(s₀, i) sets S of size k. With q := ½[c_D(n+1)]^{−λ/2} (≤ 1 for n ≥ n₀):
  Z_k ≤ (n+1)^{s₀/2}Σ_{i=0}^{s₀}C(s₀, i)(2p)^{s₀−i} · 2(k+1)^{s₀}q^{k−i} ≤ 2(n+1)^{s₀/2}(2p+1)^{s₀}(k+1)^{s₀}q^{k−s₀}.

**B4 (budget).** For n ≥ n₀:
- g_k ≤ e^{C_Bk}e^{12t/log n}(log n)^{k/2};
- (n+1)^{−λ/2} ≤ e^{0.64}(n+1)^{−1/2};
- ρ_n := e^{C_B}√(log n) · q ≤ ½e^{C_B+0.64}max(1, c_D^{−1/2})√(log n/(n+1)), so ρ_n ≤ ½ and log(1/ρ_n) ≥ ¼ log n.

Hence
  E V ≤ 2(n+1)^{s₀/2}(2p+1)^{s₀}e^{12t/log n}e^{C_Bs₀}(log n)^{s₀/2}Σ_{k>d_t}(k+1)^{s₀}ρ_n^{k−s₀} =: Ē,
and Σ_{k>d_t}(k+1)^{s₀}ρ_n^{k−s₀} ≤ K_{s₀}(d_t+2)^{s₀}ρ_n^{d_t+1−s₀} ≤ K_{s₀}(d_t+2)^{s₀}e^{−C′t/4}.

If 𝒜₂ ≠ ∅ then d_t + 2 ≤ n. Also (n+1)^{s₀/2}(2p+1)^{s₀} ≤ n^{s₀(A+2)}, (log n)^{s₀/2} ≤ n^{s₀}, 12/log n ≤ 11 and log n ≤ t. So Ē ≤ 2K_{s₀}e^{C_Bs₀}e^{(s₀(A+4)+11)t}e^{−C′t/4}.

The deterministic part W₁ := Σ_kZ_k is at most Ē as well (g_k ≥ 1). On 𝓔_t ∩ {V ≤ e^tĒ}, an event whose Markov failure probability is ≤ e^{−t}, B1 with θ ≤ 2 gives
  π(𝒜₂) ≤ e^{B/σ²}(1 + e^t)Ē ≤ exp{t[C₀ + 12 + s₀(A+4)] − C′t/4} ≤ e^{−t}.

The three S1-06 budget items appear as follows:
- union multiplicity: (2p+1)^{s₀}(n+1)^{s₀/2};
- reference cost: e^{B/σ²}, deterministic (the factor exp(‖P_{S₀}e‖²/2σ²) of X-a does not arise);
- variance surcharge: e^{(θ−λ)T_k/2} ≤ e^{C_Bk + 12t/log n}.

### Step C: 𝒜₃ (far small models; deterministic on 𝓔_t)

For S ∈ 𝒜₃: k log n ≤ (s₀+1+C′)t. By (N3) and (F6),
  Q_S − Q₀ ≥ L_S/2 − σ²C₂t − B ≥ L_S/4 > C″σ²t/4,
since C″ ≥ 4(C₂ + B/σ²).

By (F6), (i), (N1): 2b + Q₀ ≤ 2Nσ² for n ≥ n₀. So u := (Q_S − Q₀)/(2b + Q₀) ≥ C″t/(8N). With log(1+u) ≥ (log 2)min(u, 1) and ν ≥ n/2 ≥ N/2:
  ((2b + Q₀)/(2b + Q_S))^ν ≤ e^{−C″(log 2)t/16}.
(The case u ≥ 1 needs n ≥ C″t/8, true for n^{κ₀} ≥ C″/8.)

With (D₀/D_S)^{1/2} ≤ (n+1)^{s₀/2} and Σ_{S∈Ω}w(|S|)/w(s₀) ≤ 2(2p)^{s₀} (F4):
  π(𝒜₃) ≤ 2n^{s₀(A+2)}e^{−C″(log 2)t/16} ≤ 2e^{−2t} ≤ e^{−t}.

### Step D: 𝒢 (conditional tails; on 𝓔_t, uniformly in S ∈ 𝒢)

Here k ≤ (s₀+1+C′)t and L_S ≤ C″σ²t.

*Variance.* v = β_S/G with G ~ Gamma(ν, 1) and 2β_S = 2b + Q_S. With posterior probability ≥ 1 − 2e^{−t} (F3): |G − ν| ≤ √(2νt) + t, so G ≥ n/4 for n ≥ n₀. By (N1), (N4), (i) and 2ν = N + 1.02:
  |2β_S − 2σ²G| ≤ 2b₊ + σ²(T_k + 2C″t) + σ²(2√(Nt) + 2t) + 1.02σ² + 2σ²(√(2νt) + t) ≤ C₆σ²√(nt),
using t ≤ √(nt), where C₆ := C_B(s₀+1+C′) + 2C″ + 22 + 0.02(2M+1)/σ². Hence |v/σ² − 1| ≤ 2C₆√(t/n), which is ≤ 1 for n ≥ n₀, so v ≤ 2σ².

*Mean.* Given (v, S, y), X_{c,S}(θ − θ̂_S) ~ N(0, vM_S) with 0 ⪯ M_S ⪯ P_S. So ‖X_{c,S}(θ − θ̂_S)‖² ≤ vχ²_r under a coupling, with r ≤ k, independent of v. By (F1), with probability ≥ 1 − e^{−t} it is ≤ v(2k log 2 + 4t). By (F7) and (ii), ‖M_Sy_c − μ_c‖² ≤ 2σ²τ_k + 2C″σ²t. Since ‖μ̂ − μ‖ = ‖X_{c,S}θ − μ_c‖:
  ‖μ̂ − μ‖² ≤ 4σ²(2k log 2 + 4t) + 4σ²τ_k + 4C″σ²t ≤ C_μσ²t,
with C_μ := 4[(1.39 + C_B)(s₀+1+C′) + 16 + C″].

So with **C := max(C_μ, 2C₆)**: Π(‖μ̂ − μ‖² > Cσ²t or |v/σ² − 1| > C√(t/n) | S, y) ≤ 3e^{−t} for every S ∈ 𝒢.

### Assembly

On 𝓔_t ∩ {Θ^{(1)} ≤ e^t} ∩ {V ≤ e^tĒ}:
  Π(bad | y) ≤ π(𝒜₁) + π(𝒜₂) + π(𝒜₃) + 3e^{−t} ≤ 6e^{−t} ≤ e^{−t/2}  (t ≥ 16).
The exceptional probability is ≤ 4e^{−t} + 3.8e^{−2t} ≤ 2e^{−t/2}.

This is the card's display with **c = ½**, M₀ = 15, and C′, C, n₀ depending only on (s₀^r, A, σ², M, M′, c_D, κ₀). There is one n₀ for all t ∈ [M₀ log n, n^{1−κ₀}]. The case s₀ = 0 is covered (S₀ = ∅, D₀ = 1, B = 0). ∎

## 3. Comparison of the size cut with X-a, and remarks

1. **Size cut.**
   - Literal X-b (exponent 1): s₀ + Θ(t). Only Lemma X′; (ND) is unusable.
   - Fractional X-b (λ = 1 − 1/log n): d_t = s₀ + ⌈C′t/log n⌉, the same order as X-a.
   - The per-variable factor here is ρ_n ≍ √(log n/(c_Dn)), free of t. X-a's truncated moment gives √(Ct/(c_Dn)) and needs log(n/t) ≥ κ₀ log n, so its C′ ∝ 1/κ₀. Here C′ does not depend on κ₀; κ₀ enters only through n₀ (variance surcharge and Step C).
   - The dependence on s₀(A+1) sits in C′, C″, C rather than in M₀.
2. **Lemma V is not needed.** Lemma F is an exact Gaussian computation and treats non-supersets directly. (C; M′) enters only through (F6).
3. **(ND) enters only in B3**, through the Jensen-averaged λ-power sum.
4. **External inputs:** [P1] `thm:T01i` (as encoded in the common definitions), `thm:Ta`, `lem:num`, `lem:prior`, `lem:chi`(a), `lem:spec`; Laurent–Massart Lemma 1; the sub-gamma tail of BLM §2.4. No Card S or Card V result is consumed: Step A re-proves the needed size tail.

ATTEMPT X/X-b RESULT=PROVED GAPS=0
