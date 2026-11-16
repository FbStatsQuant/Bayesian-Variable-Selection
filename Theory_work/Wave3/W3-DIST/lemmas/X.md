# Lemma X and Lemma X′ — in-sample exponential core (W3-DIST, stream A; lead: Claude Fable 5.2)

Status: **DRAFT (unchecked)**. v0.2, 2026-11-15. Statement: `../STATEMENT.md` §3 (Lemma X, Lemma X′); target clauses
TC2–TC4, TC6 depend on it.

**Provenance and choice of route.** §0–§8 are the API proof attempt `../work/api_attempts/dist1/X-b-1.md` (Fable batch run
by HQ; proof material under PROTOCOL_v4 H3, not a review), adopted by the lead as the main proof because it is the
cleanest of the five available derivations: a fractional moment (λ < 1) of the Bayes factor replaces the truncated
moments, so no truncation event, no rank bookkeeping and no factor exp(‖P_{S₀}e‖²/2σ²) are needed; it is self-contained
modulo the locked [P1] (it proves the instances of Lemma V(a), of the size tail and of the good-model bound that it
uses), so Lemma X no longer depends on stream C's files. The text of §0–§8 is reproduced unchanged apart from this
header. Independent derivations of the same statement, for the line checker to compare: the lead's truncated-moment
proof `X_route_a.md` (written before the attempts arrived), and the attempts `X-a-1.md`, `X-a-2.md`, `X-b-2.md` in
`../work/api_attempts/dist1/`. All five reach c = ½ and a size cut s₀ + C′t/log n (C′ = 32 here; C′ = 12A + 68 in route a).
The adversarial attempt `X-d-1.md` found no counterexample and records that (C) cannot be dropped.
§9 (Lemma X′) and §10 (the lead's check notes) are the lead's.

[P1] = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`.
The route: Markov on the λ-th moment of the Bayes factors, λ = (4A+1)/(4A+2) < 1, untruncated, with Lemma V(a).

Notation: σ := σ*, z := e/σ ~ N_N(0, I), B := M + M′, s := s₀^r. ρ′ := θ*ᵀ(G_{S₀}+I)θ*/n = (‖μ‖² + ‖θ*‖²)/n ≤ B (ρ′ = 0 if s₀ = 0), and L_{S₀} ≤ ρ′. For every S ⊆ [p] (not only Ω) put ℓ(S) := w(|S|)D_S^{−1/2}(2b + Q_S)^{−ν}, with Q_S := Q^c_S, so π(S) = ℓ(S)/Σ_Ω ℓ. WLOG c_D ≤ 1, since (ND; c_D) implies (ND; min(c_D, 1)).

## 0. External facts and constants

- **(F1) Gamma/χ² tails.** For G ~ Gamma(ν, 1), ν > 0, x > 0: P(G ≥ ν + √(2νx) + x) ≤ e^{−x} and P(G ≤ ν − √(2νx)) ≤ e^{−x}. (Boucheron–Lugosi–Massart, *Concentration Inequalities*, 2013, §2.4: Gamma is sub-gamma with (v, c) = (ν, 1) on the right and (ν, 0) on the left; from log E e^{u(G−ν)} = −ν log(1−u) − νu ≤ νu²/(2(1−u)) for 0 < u < 1 and ≤ νu²/2 for u < 0.) With ν = N/2 this is Laurent–Massart (2000, Ann. Statist. 28, Lemma 1): P(χ²_N − N ≥ 2√(Nx) + 2x) ≤ e^{−x}, P(N − χ²_N ≥ 2√(Nx)) ≤ e^{−x}.
- **(F2)** [P1] `lem:chi`(a): r ≤ d ⇒ P(χ²_r ≥ 2d log 2 + 4x) ≤ e^{−x}.
- **(F3)** P(|N(0,1)| > √(2x)) ≤ 2e^{−x}.
- **(F4)** For symmetric A ≺ I_N: E exp(zᵀAz/2) = det(I − A)^{−1/2}.
- **From [P1]:** `thm:T01i`, `lem:slab`, `lem:spec`(b),(d),(e), `lem:prior`(b),(c),(e), `lem:num`, `thm:Ta`, the proof of `lem:den`; constants b_±, κ, c_IG, c♯ = κ²/(c_IGσ²), event 𝓑_n.

**Constants** (depending only on (s, A, σ², M, M′, c_D, κ₀); all nondecreasing in s₀, so stated with s):
- C_A′ := 4A + 6; C_m := 2s + 1 + (s(A+2) + 5)/log 2; C_d := s + 33; C_x := (A+1)C_d + 2; C_P := C_A′C_d + 4.
- Λ := max{32C_x, 8C_P, 8B/σ², 48/log 2}; C_Q := C_P + 2√(2C_xΛ) + Λ; b̄ := 0.04(M + σ²); C_β := b̄/σ² + 5 + C_Q; C_v := 2(C_β + 6).
- **C := max{4(2C_d + 4 + C_P + Λ), C_v}; λ := (4A+1)/(4A+2); C′ := 32; c := ½.**
- K_s := Σ_{i≥0}(1+i)^s2^{−i}; C₅ := 4^{s+1}e^{3B/(2σ²)}(8A+4)^{s/2}K_s; **M₀ := max{16, (A+1)s, log C₅}.**

Since log n ≥ log 3 > 1, on the range: t ≥ M₀, log n ≤ t, n^{(A+1)s₀} ≤ e^t. Also t/N ≤ 1.5n^{−κ₀}.

Put j₁ := ⌈32t/log n⌉, d_t = s₀ + j₁, and
- ε₁ := 2√(t/N) + 2t/N;
- ε₂ := ε₁ + (C_A′C_m + 4) t log n/N;
- 1 + ε₃ := (n + 0.02)/(N(1 − ε₂)).

All three are deterministic, nondecreasing in t, and tend to 0 at t = n^{1−κ₀}.

**n₀** is the least n such that, at t = n^{1−κ₀} (hence for all smaller t):
- (a) n ≥ e⁸;
- (b) ε₁ + 12t/N ≤ ½;
- (c) ε₂ < 1 and ε₃ ≤ 1/(8A+2);
- (d) n^{1/8} ≥ e^s(8A+4)^{1/2}c_D^{−1/2};
- (e) b̄ + B + Nσ²(1 + ε₁) ≤ 2Nσ² and t ≤ 8n/Λ;
- (f) C_v n^{−κ₀/2} ≤ 1;
- (g) √n ≥ 2c♯e^{1+B/(2σ²)}.

By (a), 32/log n ≤ 3/log 2, so min(d_t, K) ≤ m_n(t).

## 1. Lemma V(a), re-proved

For T ⊆ [p], c > 0, u ∈ ℝ^N let
Q_T^{(c)}(u) := min_φ{‖u − X_{c,T}φ‖² + cφᵀ(G_T+I)φ/n} = uᵀ(I − M_T^{(c)})u, M_T^{(c)} := X_{c,T}(G_T + c(G_T+I)/n)^{−1}X_{c,T}ᵀ
(complete the square; M_T^{(1)} = M_T). By the SVD, M_T^{(c)} has eigenvalues g/(g + c(g+1)/n) ∈ [0, 1) (g the eigenvalues of G_T) and range col X_{c,T}.

**Lemma V(a).** For J ⊆ [p]∖S₀, S = S₀ ∪ J, and D′_J := M_S^{(1/2)} − M_{S₀}^{(2)}:
(i) 0 ≤ Q_{S₀} − Q_S ≤ eᵀD′_Je + 3ρ′ for every e;
(ii) 0 ⪯ D′_J, all eigenvalues of D′_J lie in [0, 1), and rank D′_J ≤ s₀ + |J|.

*Proof.*
- (i) Lower bound: `lem:spec`(d). Upper bound: write φ = θ* + φ′ (zero-padded), so y_c − X_cφ = e − X_cφ′. Young's inequality gives (x+y)ᵀA(x+y) ≤ 2yᵀAy + 2xᵀAx and (x+y)ᵀA(x+y) ≥ ½yᵀAy − xᵀAx for A ⪰ 0. With A = G_{S₀}+I, resp. G_S+I, and θ*ᵀ(G_S+I)θ* = θ*ᵀ(G_{S₀}+I)θ* = nρ′:
  Q_{S₀}(y_c) ≤ Q_{S₀}^{(2)}(e) + 2ρ′ and Q_S(y_c) ≥ Q_S^{(1/2)}(e) − ρ′. Subtract.
- (ii) Q_T^{(c)} is nondecreasing in c and nonincreasing in T (zero-padding), so Q_S^{(1/2)} ≤ Q_S^{(2)} ≤ Q_{S₀}^{(2)}, i.e. D′_J ⪰ 0. Also D′_J ⪯ M_S^{(1/2)} ≺ I. Both terms vanish on (col X_{c,S})^⊥, which gives the rank bound. ∎

No floor is used; (C; M′) enters only through ρ′ ≤ B.

## 2. X1 — noise event

Let 𝓔_t be the intersection of:
- **(N1)** |‖e‖² − Nσ²| ≤ σ²(2√(Nt) + 2t);
- **(N2)** ‖P_Te‖² ≤ σ²(C_A′|T| log n + 4t) for all T ⊆ [p] with 1 ≤ |T| ≤ min(p, m_n(t) + s₀);
- **(N3)** |eᵀ(I − M_S)μ_c| ≤ σ√(2x_{|S|}L_S), x_k := k(log p + 1) + t + 1, for all S ⊆ [p] with |S| ≤ m_n(t) (S = ∅ included).

**P(𝓔_tᶜ) ≤ 5e^{−t}.**
- (N1): (F1), failure ≤ 2e^{−t}.
- (N2): ‖P_Te‖²/σ² ~ χ²_r with r ≤ |T| = k. Apply (F2) with x = k log p + k + t; the threshold is 2k log 2 + 4x ≤ C_A′k log n + 4t. Union: Σ_{k≥1}p^ke^{−x} ≤ e^{−t}.
- (N3): eᵀ(I − M_S)μ_c ~ N(0, σ²‖(I − M_S)μ_c‖²) and ‖(I − M_S)μ_c‖² ≤ L_S (0 ⪯ I − M_S ⪯ I). By (F3) and the union bound, failure ≤ Σ_{k≥0}p^k·2e^{−x_k} = (2/(e−1))e^{−t} ≤ 2e^{−t}.

**Consequences on 𝓔_t, n ≥ n₀:**
- **(E1)** ‖e‖² ∈ Nσ²[1 − ε₁, 1 + ε₁].
- **(E2)** σ²/2 ≤ s_y² ≤ 2(M + σ²), so 𝓔_t ⊆ 𝓑_n and 0 < 2b ≤ b̄.
  Ns_y² = ‖μ‖² + 2μ_cᵀe + ‖e‖², and (N3) at S = ∅ gives 2|μ_cᵀe| ≤ 4σ‖μ‖√t. Using 4σ‖μ‖√t ≤ ‖μ‖² + 4σ²t: Ns_y² ≥ Nσ²(1 − ε₁ − 4t/N) ≥ Nσ²/2. Using 4σ‖μ‖√t ≤ ‖μ‖²/3 + 12σ²t and ‖μ‖²/N ≤ 1.5M: s_y² ≤ 2M + σ²(1 + ε₁ + 12t/N) ≤ 2M + 2σ². Both by (b).
- **(E3)** For J ⊆ [p]∖S₀ with 1 ≤ |J| ≤ min(m_n(t), p − s₀), S = S₀ ∪ J: since μ_c ∈ col X_{c,S}, `lem:spec`(b) gives Q_S ≥ ‖(I − P_S)e‖² = ‖e‖² − ‖P_Se‖² ≥ Nσ²(1 − ε₂) > 0. Here (N2) is applied with |S| ≤ m_n(t) + s₀ ≤ C_m t, so ‖P_Se‖² ≤ σ²(C_A′C_m + 4)t log n. Hence ν/Q_S ≤ (1 + ε₃)/(2σ²).
- **(E4)** For S ∈ Ω with |S| ≤ d_t (so |S| ≤ m_n(t), and |S| log n ≤ (s₀ + 1) log n + 32t ≤ C_d t): ‖P_Se‖² ≤ σ²C_P t and x_{|S|} ≤ C_x t.

## 3. X4(b),(c) — sizes in (d_t, m_n(t)]: untruncated fractional moment

For J ⊆ [p]∖S₀ with 1 ≤ |J| = j ≤ min(m_n(t), p − s₀) let S_J := S₀ ∪ J and
BF_J := ℓ(S_J)/ℓ(S₀) = [w(s₀+j)/w(s₀)](D_{S₀}/D_{S_J})^{1/2}((2b + Q_{S₀})/(2b + Q_{S_J}))^ν.

**Step 1 (pointwise, on 𝓔_t).** Since Q_{S₀} ≥ Q_{S_J} > 0, (2b + Q_{S₀})/(2b + Q_{S_J}) ≤ Q_{S₀}/Q_{S_J}. With (1 + ξ)^ν ≤ e^{νξ}, (E3) and Lemma V(a):
BF_J ≤ [w(s₀+j)/w(s₀)](D_{S₀}/D_{S_J})^{1/2} exp{(1 + ε₃)(zᵀD′_Jz/2 + 3ρ′/(2σ²))}.

**Step 2 (λ-th moment).** Put λ₁ := λ(1 + ε₃). By (c), λ₁ ≤ 1 − 1/(8A+4), because (1 − 1/(8A+4))/λ = 1 + 1/(8A+2). Since D′_J ⪰ 0 has eigenvalues < 1 and rank ≤ s₀ + j, (F4) gives
E exp(λ₁zᵀD′_Jz/2) = det(I − λ₁D′_J)^{−1/2} ≤ (1 − λ₁)^{−(s₀+j)/2} ≤ (8A+4)^{(s₀+j)/2}.
Hence
E[1_{𝓔_t}BF_J^λ] ≤ e^{3B/(2σ²)}(8A+4)^{(s₀+j)/2}[w(s₀+j)/w(s₀)]^λ(D_{S₀}/D_{S_J})^{λ/2}.

**Step 3 (sum over |J| = j, using (ND)).**
- By Jensen (x ↦ x^λ concave) and (ND): Σ_{|J|=j}(D_{S₀}/D_{S_J})^{λ/2} ≤ C(p−s₀, j)[c_D(n+1)]^{−λj/2}.
- By `lem:prior`(e) (s₀ + j ≤ p) and p ≤ n^A: [w(s₀+j)/w(s₀)]^λ C(p−s₀, j) = [C(p−s₀, j)w(s₀+j)/w(s₀)]^λ C(p−s₀, j)^{1−λ} ≤ 2(j+1)^{s₀}n^{Aj(1−λ)}.
- Therefore T_j := Σ_{|J|=j}E[1_{𝓔_t}BF_J^λ] ≤ 2e^{3B/(2σ²)}(8A+4)^{s₀/2}(j+1)^{s₀}q^j, with
  q := (8A+4)^{1/2}c_D^{−1/2}n^{A(1−λ)−λ/2} = (8A+4)^{1/2}c_D^{−1/2}n^{−1/4},
  because A(1−λ) − λ/2 = A/(4A+2) − (4A+1)/(2(4A+2)) = −¼.
- By (d), e^{s₀}q ≤ n^{−1/8} ≤ ½. Using j₁ + 2 + i ≤ (j₁+2)(1+i) and j₁ + 2 ≤ e^{j₁+1}:
  Σ_{j>j₁}(j+1)^{s₀}q^j ≤ K_s(e^{s₀}q)^{j₁+1} ≤ K_s n^{−(j₁+1)/8} ≤ K_s e^{−4t}.

**Step 4 (non-supersets through S ∪ S₀).** Let S ∈ Ω with S₀ ⊄ S and d_t < |S| ≤ m_n(t); put J′ := S∖S₀, S′ := S ∪ S₀ = S_{J′} (possibly ∉ Ω). Then j₁ < |J′| ≤ min(m_n(t), p − s₀), and
ℓ(S)/ℓ(S′) = [w(|S|)/w(|S′|)](D_{S′}/D_S)^{1/2}((2b + Q_{S′})/(2b + Q_S))^ν ≤ (2p)^{s₀}(n+1)^{s₀/2}:
- w(k)/w(k+1) = (2p−1−k)/(k+1) ≤ 2p (`lem:prior`(b), |S′| ≤ p);
- D_{S′}/D_S ≤ (n+1)^{|S′|−|S|}: by Cauchy interlacing λ_i(G_{S′}) ≤ λ_i(G_S), and f < n + 1 in `lem:spec`(e);
- Q_{S′} ≤ Q_S (`lem:spec`(d)).

Each S′ arises from fewer than 2^{s₀} such S. Supersets S_J ∈ Ω with d_t < |S_J| ≤ m_n(t) have j₁ < |J| ≤ m_n(t) − s₀. Since π(S) ≤ ℓ(S)/ℓ(S₀) (S₀ ∈ Ω), for every data set:
π(d_t < |S| ≤ m_n(t)) ≤ A_nV, V := Σ_{J: j₁<|J|≤min(m_n(t),p−s₀)}BF_J, A_n := 1 + 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} ≤ 2·4^{s₀}n^{(A+1)s₀} ≤ 2·4^{s₀}e^t.

**Step 5 (Markov at power λ).** Let 𝓕₂ := {A_nV ≤ e^{−t}}. By (Σa_i)^λ ≤ Σa_i^λ:
P(𝓔_t ∩ 𝓕₂ᶜ) ≤ e^{λt}A_n^λ Σ_{j>j₁}T_j ≤ e^t·2·4^{s₀}e^t·2e^{3B/(2σ²)}(8A+4)^{s₀/2}K_se^{−4t} ≤ C₅e^{−2t} ≤ e^{−t} (t ≥ log C₅).

(ND) is used only for j₁ < j ≤ min(m_n(t), p − s₀), and only through its λ-power mean.

## 4. X4(a) — sizes above m_n(t) (the instance of Lemma S needed)

Let m := m_n(t). If m = K the mass is 0. Otherwise m = s₀ + ⌈x/log 2⌉ with x = s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t.
- **Prior ratio.** R_m := ϖ(|S| > m)/ϖ(S₀) ≤ 2^{−m}/w(s₀) ≤ 2(2p)^{s₀}2^{−m} (`lem:prior`(c): Σ_{k>m}q_k ≤ 2^{−m}; 1/w(s₀) = 2C(2p−1, s₀)). With D_{S₀} ≤ (n+1)^{s₀}: R_m√(D_{S₀})√n ≤ 2n^{−1/2}e^{−3t}.
- **Numerator.** N_m := Σ_{S∈Ω,|S|>m}ϖ(S)m^c_{b₋}(S)/f₀(y_c) has E N_m = ϖ(|S| > m) (`lem:num`). Let 𝓕₁ := {N_m ≤ e^tϖ(|S| > m)}; P(𝓕₁ᶜ) ≤ e^{−t}.
- **Denominator.** Q_{S₀} ≤ ‖y_c − X_{c,S₀}θ*‖² + nρ′/n = ‖e‖² + ρ′ (`lem:slab`). The proof of `lem:den` with R_n replaced by ρ′ (it uses only Q_{S₀} ≤ σ²E′ + nonnegative term; this is `B_tail_approx.md` Steps 2–3 with r = 0) gives
  m^c_{b₊}(S₀)/f₀(y_c) ≥ D_{S₀}^{−1/2}c_IGσ²n^{−1/2}e^{−Λ″}, Λ″ := |E′ − N|/(2√n) + E′/(2n) + ρ′/(2σ²), E′ = ‖e‖²/σ².
- **Assembly.** On 𝓔_t ⊆ 𝓑_n, `thm:Ta` gives π(|S| > m) ≤ κ²I_{b₋}/(ϖ(S₀)m^c_{b₊}(S₀)). On 𝓔_t ∩ 𝓕₁, by (N1), Λ″ ≤ √t + t/√n + 1 + B/(2σ²) ≤ t/2 + 1 + B/(2σ²) (t ≥ 16, n ≥ 16), so
  π(|S| > m_n(t)) ≤ c♯e^te^{Λ″}R_m√(D_{S₀})√n ≤ 2c♯e^{1+B/(2σ²)}n^{−1/2}e^{−1.5t} ≤ e^{−1.5t} by (g).

## 5. X3 — small far models

Far := {S ∈ Ω : |S| ≤ d_t, L_S > Λσ²t}. Work on 𝓔_t and write L_S = λ_Sσ²t with λ_S > Λ.
- Q_S = L_S + 2eᵀ(I − M_S)μ_c + eᵀ(I − M_S)e ≥ L_S − 2σ√(2C_xtL_S) + ‖e‖² − σ²C_Pt, by (N3), (E4), M_S ⪯ P_S.
- Q_{S₀} ≤ ‖e‖² + B.
- So Δ := Q_S − Q_{S₀} ≥ σ²t[λ_S − 2√(2C_xλ_S) − C_P − B/σ²] ≥ σ²tλ_S/4 ≥ Λσ²t/4 > 0, using λ_S ≥ 32C_x (so 2√(2C_xλ_S) ≤ λ_S/2), λ_S ≥ 8C_P, λ_S ≥ 8B/σ², t ≥ 1.
- By (e), 2b + Q_{S₀} ≤ 2Nσ². With log(1 + u) ≥ (log 2)min(u, 1) and ν ≥ n/2:
  ν log(1 + Δ/(2b + Q_{S₀})) ≥ min{(n/2) log 2, (log 2)Λt/16} = (log 2)Λt/16 ≥ 3t (by (e), and Λ ≥ 48/log 2).
- With D_S ≥ 1, D_{S₀} ≤ (n+1)^{s₀}, Σ_{S∈Ω}w(|S|)/w(s₀) ≤ 1/w(s₀) ≤ 2(2p)^{s₀} and π(S₀) ≤ 1:
  **π(Far) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−3t} ≤ 2^{s₀+1}e^{−2t} ≤ e^{−t}** (n^{(A+1)s₀} ≤ e^t; t ≥ M₀ ≥ (s₀+1) log 2).

## 6. X2 — good models

Good := {S ∈ Ω : |S| ≤ d_t, L_S ≤ Λσ²t}. Work on 𝓔_t, n ≥ n₀; the bounds hold simultaneously for all good S.
- **Centre.** M_Sy_c − μ_c = M_Se − (I − M_S)μ_c, ‖M_Se‖ ≤ ‖P_Se‖, ‖(I − M_S)μ_c‖² ≤ L_S. So ‖M_Sy_c − μ_c‖² ≤ 2σ²(C_P + Λ)t.
- **Scale.** |Q_S − ‖e‖²| ≤ ‖P_Se‖² + 2|eᵀ(I − M_S)μ_c| + L_S ≤ σ²C_Qt. With β_S := b + Q_S/2, (N1), 2b ≤ b̄ and t ≤ √(nt):
  |2β_S/(nσ²) − 1| ≤ [b̄/σ² + 1 + (C_Q + 4)√(nt)]/n ≤ C_β√(t/n).
- **v.** Given (S, y), β_S/v ~ Gamma(ν, 1). By (F1), with conditional probability ≥ 1 − 2e^{−t}, |2β_S/v − n| ≤ 0.02 + 2√((n+0.02)t) + 2t ≤ 6√(nt). Then v/σ² = (1 + a)/(1 + g) with |a| ≤ C_β√(t/n), |g| ≤ 6√(t/n) ≤ ½ (by (f)), so |v/σ² − 1| ≤ 2(C_β + 6)√(t/n) = C_v√(t/n), and v ≤ 2σ².
- **θ.** Given (v, S, y), X_{c,S}(θ − θ̂_S) ~ N(0, vM_S), so ‖X_{c,S}(θ − θ̂_S)‖²/v is stochastically at most χ²_r, r = rank M_S ≤ |S|. By (F2), with conditional probability ≥ 1 − e^{−t} it is ≤ 2|S| log 2 + 4t ≤ (2C_d + 4)t.
- **Together.** With conditional probability ≥ 1 − 3e^{−t}: |v/σ² − 1| ≤ C_v√(t/n) and
  ‖μ̂ − μ‖² = ‖X_{c,S}θ − μ_c‖² ≤ 2·2σ²(2C_d + 4)t + 2·2σ²(C_P + Λ)t ≤ Cσ²t.

So sup_{S∈Good} Π(‖μ̂ − μ‖² > Cσ²t or |v/σ² − 1| > C√(t/n) | S, y) ≤ 3e^{−t}.

## 7. Assembly

Every S ∈ Ω is in {|S| > m_n(t)}, {d_t < |S| ≤ m_n(t)}, Far or Good. On 𝓔_t ∩ 𝓕₁ ∩ 𝓕₂, n ≥ n₀, M₀ log n ≤ t ≤ n^{1−κ₀}:
Π(Bad | y) ≤ e^{−1.5t} + e^{−t} + e^{−t} + 3e^{−t} ≤ 6e^{−t} ≤ e^{−t/2},
and P((𝓔_t ∩ 𝓕₁ ∩ 𝓕₂)ᶜ) ≤ 5e^{−t} + e^{−t} + e^{−t} = 7e^{−t} ≤ 2e^{−t/2} (t ≥ 16).

This is Lemma X with c = ½, C′ = 32 and the C, M₀, n₀ of §0. The single n₀ is uniform in t because conditions (a)–(g) are monotone in t and imposed at t = n^{1−κ₀}. ∎

## 8. Remarks on the route

**R1. The literal X-b cannot give d_t.** Lemma V(b) is correct, and the helper's argument for it checks: with Σ_T^{(c)} := (I − M_T^{(c)})^{−1} ⪰ I,
det(I − D′) ≥ det(I − Σ₀^{(c)1/2}D′Σ₀^{(c)1/2}) = det Σ₀^{(c)}/det Σ_S^{(1/c)},
and the eigenvalue-wise comparisons det Σ_S^{(1/c)} ≤ c^{|S|}D_S, D_{S₀} ≤ c^{s₀}det Σ₀^{(c)} give the bound (1+η)^{s₀+j/2}. But at λ = 1 the factor (D_{S₀}/D_S)^{1/2} is consumed by the moment. For s₀ = 0, E[D_S^{−1/2}e^{zᵀM_Sz/2}] = 1 exactly, whatever the design. So first-moment Markov gives Σ_{|J|=j} ≲ 2(j+1)^{s₀}(√(1+η)/2)^j: (ND) never enters. The variance surcharge then has to be paid separately through (N2), ε₃‖P_Se‖²/(2σ²) = o(t). The resulting cut is j₁ ≈ (3t + (A+1)s₀ log n)/log(2/√(1+η)), no better than m_n(t). That is the Lemma X′ form (radius t·log n), not Lemma X.

**R2. Size cut compared with X-a.** The fractional moment gives the Occam factor c_D^{−1/2}n^{−1/4} per extra variable, against X-a's (C log n/n)^{1/2}. The cut has the same order s₀ + C′t/log n, with C′ about twice X-a's. Taking 1 − λ ≍ 1/log n should recover q ≍ (log n/n)^{1/2}, since ε₃ log n → 0 uniformly on the range; I did not write this out.

**R3. S1-06 budget.**
- Factor (1), exp(‖P_{S₀}e‖²/2σ²): absent, replaced by the constant (8A+4)^{s₀/2}.
- Factor (3), variance surcharge: free, absorbed in λ₁ < 1.
- Factor (2), multiplicity A_n: remains, paid by M₀ ≥ (A+1)s.
- No truncation event χ²_J ≤ τ_j, no rank bookkeeping d_J and no weights a_J are needed.

**R4. Hypotheses actually used.** (ND) is used only for j > ⌈32t/log n⌉ and only as the weaker power-mean condition C(p−s₀, j)^{−1}Σ_J(D_{S₀}/D_{S_J})^{λ/2} ≤ [c_D(n+1)]^{−λj/2}. (C; M′) is used only through ρ′ ≤ B. p ≤ n^A is used in (N2), (N3), Step 3 and A_n.

## 9. Lemma X′ (without (ND)) — lead
Statement (STATEMENT §3): under (E; M), (C; M′) only, for n ≥ n₀′ and M₀ log n ≤ t ≤ n^{1−κ₀}, with ℓ_n := log(p_raw ∨ n) ≥ log n:
P_e[Π(‖μ̂ − μ‖² > Cσ²tℓ_n or |v/σ² − 1| > C√(t/n) or |S| > m_n(t) | y) > e^{−ct}] ≤ 2e^{−ct}.
*Proof.* Use the event 𝓔_t of §2 and 𝓕₁ of §4 unchanged; §3 is not used ((ND) never enters). Put t′ := t·log n ≤ tℓ_n and
replace d_t by m := m_n(t) and, in the *thresholds* only, t by t′:
- (E4′) For S ∈ Ω with |S| ≤ m: |S| ≤ m ≤ C_m t (§2 (E3)), so by (N2), ‖P_Se‖² ≤ σ²(C_A′C_m + 4)t′ =: σ²C_P′t′, and
  x_{|S|} ≤ C_m t((A+1) log n + 1) + t + 1 ≤ C_x′t′ with C_x′ := C_m(A + 2) + 2.
- Far′ := {S ∈ Ω : |S| ≤ m, L_S > Λ′σ²t′}, Λ′ := max{32C_x′, 8C_P′, 8B/σ², 48/log 2}. The computation of §5 with (C_x, C_P, Λ, t)
  replaced by (C_x′, C_P′, Λ′, t′) in the three bounds on Q_S, Q_{S₀}, Δ gives Δ ≥ Λ′σ²t′/4, and then
  ν log(1 + Δ/(2b + Q_{S₀})) ≥ min{(n/2) log 2, (log 2)Λ′t′/16} ≥ 3t′ ≥ 3t provided t′ ≤ 8n/Λ′, which holds for n ≥ n₀′ uniformly in
  t ≤ n^{1−κ₀} (n^{−κ₀} log n → 0). Hence π(Far′) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−3t} ≤ e^{−t} as in §5.
- Good′ := {S ∈ Ω : |S| ≤ m, L_S ≤ Λ′σ²t′}. As in §6: ‖M_Sy_c − μ_c‖² ≤ 2σ²(C_P′ + Λ′)t′; |Q_S − ‖e‖²| ≤ σ²C_Q′t′ with
  C_Q′ := C_P′ + 2√(2C_x′Λ′) + Λ′; so |2β_S/(nσ²) − 1| ≤ [b̄/σ² + 1 + C_Q′t′ + 4√(nt)]/n ≤ (b̄/σ² + 5 + C_Q′)√(t/n), using
  t′/n = √(t/n)·√(t/n) log n ≤ √(t/n) for n ≥ n₀′ (√(t/n) log n ≤ n^{−κ₀/2} log n ≤ 1). The v-step is unchanged (level t). The
  θ-step: ‖X_{c,S}(θ − θ̂_S)‖²/v ≤ 2|S| log 2 + 4t ≤ (2C_m + 4)t ≤ (2C_m + 4)t′ with conditional probability ≥ 1 − e^{−t}. Together,
  with conditional probability ≥ 1 − 3e^{−t}: ‖μ̂ − μ‖² ≤ C_1′σ²t′ ≤ C_1′σ²tℓ_n and |v/σ² − 1| ≤ C_v′√(t/n).
- {|S| > m}: §4, on 𝓔_t ∩ 𝓕₁: π(|S| > m) ≤ e^{−1.5t}.
Assembly as in §7: on 𝓔_t ∩ 𝓕₁, Π(Bad′ | y) ≤ e^{−1.5t} + e^{−t} + 3e^{−t} ≤ e^{−t/2}; P((𝓔_t ∩ 𝓕₁)ᶜ) ≤ 6e^{−t} ≤ 2e^{−t/2}. So Lemma X′ holds
with c = ½; constants depend on (s₀^r, A, σ², M, M′, κ₀). ∎ (DRAFT, unchecked.)

## 10. Lead's check notes on §0–§8 (not a review)
Checked by the lead, line by line: Step 1–3 and 5 of §3 (the pointwise bound, the determinant formula and the bound
(1 − λ₁)^{−(s₀+j)/2}, Jensen with (ND), the exponent A(1 − λ) − λ/2 = −¼, the geometric sum); Step 4 (union device, same as
route a §3(a)); §5 and §6 (same structure as route a §2 and the input (I-X2) there); §7. Citations of [P1] verified to
exist with the quoted content: `lem:chi`(a) (line 139), `lem:prior`(b), (c), (e) (line 113), `lem:num` (317), `thm:Ta`
(255; needs the event 𝓑_n = {b₋ ≤ b₀s_y² ≤ b₊}, b₋ = b₀σ²/2, b₊ = b₀(2(σ² + M) + 1), line 58 — implied by (E2) of §2),
`lem:spec`(b), (d), (e) (90), `lem:slab` (68). **Not yet checked by the lead and flagged for the line check:**
(1) §4's use of the proof of `lem:den` with R_n replaced by ρ′ and the constants c_IG, c♯ (the same step as
`W3-POST2/lemmas/B_tail_approx.md` Step 3); (2) condition (g) and the definition of n₀ at t = n^{1−κ₀} (monotonicity
in t of every condition); (3) the WLOG c_D ≤ 1; (4) §2 (E2)'s lower bound on s_y² (uses (N3) at S = ∅ with L_∅ = ‖μ‖²);
(5) s₀ = 0 throughout (ρ′ = 0, S₀ = ∅). The statement proved is Lemma X as fixed at CP1 (no change request).
