# E — Theorem 1-VIS: (F_λ) away from S₀ replaced by an identifiability margin (W3-POST2, Claim E; stretch)

Status: **PROVED (by this seat, unchecked)**. **Check record [C1B-2]:** v1 line check K-AE (VERIFIED-WITH-AMENDMENTS); v2 (ridge-loss E1) line check K2: VERIFIED-WITH-AMENDMENTS (applied); M01: sound; S01: remark fixes; council C1 (PASS). Kill budget: v1 was the one proof attempt; v2 is a sharpness-gate restatement under its own line check (K2) — HQ to rule on the budget [C1B-1]. v2 (STATEMENT v1.2): Lemma E1 stated with the ridge loss
L_S := μ_cᵀ(I − M_S)μ_c ≥ Δ_S (R03b §D), so the hypothesis is (ID^M; c), implied by (ID; c). Notation: `../STATEMENT.md`; [P1], [P3],
[T03R]; `A_occam.md` ((G3′), (C4′), (C5′), Υ′_n). Kill budget (brief item 5): statement lock + one proof attempt.

## Statement
In R1 under G, (E), (F₀), (OS) and (ID^M; c): L_S ≥ cσ*² log n for every S ∈ 𝔉 (below), with c > c₁ — implied by (ID; c)
because L_S ≥ Δ_S (M_S ⪯ P_S, [P3] `lem:smoother`(b)); L_S = min_ϑ{‖μ − X_Sϑ‖² + ϑᵀ(G_S + I)ϑ/n} = min_ϑ B_S(ϑ)
([P1] `lem:slab` with Y = μ_c) —
  c₁ := (√(2C_x) + √(2C_x + C_A j₀ + (2/log 2)(s₀(A+1) + 2)))²,  C_x := Aj₀ + s₀ + log(j₀ + 1) + 2:
(1) δ_n = O_P(r_n); (2)–(4) the conclusions 2–4 of [W3P] Theorem 1; (5b′) for j ∈ S₀ with (ID^M_j; c) (L_S ≥ cσ*² log n for S ∈ 𝔉 with j ∉ S), c > c₁:
π(S ∌ j) = O_P(r_n) (without (ID^M)); (6) the random-design transfer of [W3P] item 6 with common constants.

## E0. A bookkeeping fact [C1B-5]
**Lemma E0.** For every fixed integer B ≥ s₀ + 1 there is n₀(s₀, A, B) such that m♯_n ≥ min(B, K) for n ≥ n₀, uniformly
in 2 ≤ p ≤ n^A. *Proof.* Let s₀ ≤ m < min(B, K). Then m + 1 ≤ K, so by [T03R] E1(a) R_m ≥ q_{m+1}/w(s₀) =
C(p, s₀)Π_{i=s₀}^{m}ρ_i with ρ_i = (p − i)/(2p − 1 − i). For i ≤ m < K ≤ p, p − i ≥ 1; if p ≥ 2B each ρ_i ≥ (p − B)/(2p) ≥ 1/4,
otherwise ρ_i ≥ 1/(2p) ≥ 1/(4B). Hence R_m ≥ (4B)^{−B} > n^{−(s₀+2)/2} for n ≥ n₀, so m is not admissible in the definition of
m♯_n, and m♯_n ≥ min(B, K). ∎ (Used with B = j₀ in E1(b) and B = s₀ + j₀ in `D_hellinger.md` D3.)

## E1. The floor-free comparison lemma
Let 𝔉 := {S ∈ Ω : S₀ ⊄ S, |S∖S₀| ≤ j₀} and S′ := S ∪ S₀. Let 𝒢⁵_n be the event
|eᵀ(I − M_S)μ_c| ≤ σ*√(2x_nL_S) for all S ∈ 𝔉 (v1 used (I − P_S) and Δ_S), x_n := Aj₀ log n + s₀ + log(j₀ + 1) + log(2n).

**Lemma E1.** (a) P((𝒢⁵_n)ᶜ) ≤ 1/n, and x_n ≤ C_x log n for n ≥ 3. (b) Assume R1, G, (E), (F₀), c > c₁. For n ≥ n₀, on
𝒢^sup_n ∩ 𝒢⁵_n, every S ∈ 𝔉 with L_S ≥ cσ*² log n satisfies ℓ(S)/ℓ(S′) ≤ n^{−2}.

*Proof.* (a) For fixed S, eᵀ(I − M_S)μ_c ~ N(0, σ*²‖(I − M_S)μ_c‖²) and ‖(I − M_S)μ_c‖² ≤ L_S because 0 ⪯ I − M_S ⪯ I
(so (I − M_S)² ⪯ I − M_S). (Δ_S = ‖(I − P_S)μ_c‖² = ‖(I − P^{(n)}_S)μ‖² because X = UX_c, μ = Uμ_c and U is an isometry
onto 1^⊥ ⊇ col X.) P(|Z| > √(2x)) ≤ 2e^{−x}. #𝔉 ≤ 2^{s₀}(j₀ + 1)p^{j₀}
(S is fixed by S∖S₀, at most Σ_{j′≤j₀}C(p, j′) ≤ (j₀+1)p^{j₀} choices, and S ∩ S₀ ⊊ S₀). With p ≤ n^A,
#𝔉·2e^{−x_n} ≤ 2·2^{s₀}(j₀+1)n^{Aj₀}·n^{−Aj₀}e^{−s₀}(j₀+1)^{−1}(2n)^{−1} = (2/e)^{s₀}/n ≤ 1/n. Finally s₀ ≤ s₀ log n,
log(j₀+1) ≤ log(j₀+1) log n and log(2n) ≤ 2 log n for n ≥ 3.
(b) Fix S ∈ 𝔉 with L_S ≥ cσ*² log n; J := S₀∖S ≠ ∅ (|J| ≤ s₀), J′ := S∖S₀ (|J′| ≤ j₀). By [P3] eq. (`eq:score`),
  ℓ(S)/ℓ(S′) = [w(|S|)/w(|S′|)]·(D_{S′}/D_S)^{1/2}·(1 + D/B′)^{−ν},  D := Q^c_S − Q^c_{S′} ≥ 0,  B′ := 2b + Q^c_{S′} > 0
(D ≥ 0 by [P1] `lem:spec`(d), S ⊆ S′). *Prefactor:* w(|S|)/w(|S′|) ≤ (2p)^{|J|} ([P3] `lem:prior`(a); |S′| ≤ p) and
D_{S′}/D_S ≤ (n+1)^{|J|} ([P3] `lem:det`, no condition), so the product is ≤ n^{s₀(A+1)} for n ≥ 5 (as in [P3]
`lem:signalgain`). *Upper bound on B′:* Q^c_{S′} ≤ Q^c_{S₀} ([P1] `lem:spec`(d), S₀ ⊆ S′) and, by the first paragraph of
[P1] `lem:den` (uses (F₀) only), Q^c_{S₀} ≤ ‖(I − P_{S₀})e‖² + R_n with R_n = γ_n‖P_{S₀}y_c‖² ≤ γ_n‖y_c‖²,
γ_n = (1 + 1/(Nφ₀²))/(n+1) ≤ 2/(n+1) once Nφ₀² ≥ 1. On 𝒢^sup_n, ‖y_c‖² ≤ 4n(M + σ*²) and b ≤ 6b₀(M + σ*²) ([P3]
`lem:ongood`(a)), so R_n ≤ 8(M + σ*²) and B′ ≤ 2b + ‖e‖² + R_n ≤ Nσ*²(1 + δ″_n) ([P3] `lem:ongood`(c), the bound on E_n,
with the same constants). *Lower bound on D:* exactly, Q^c_S = y_cᵀ(I − M_S)y_c = L_S + 2eᵀ(I − M_S)μ_c + eᵀ(I − M_S)e ([P1] `lem:spec`(a)), and
eᵀ(I − M_S)e ≥ ‖e‖² − ‖P_Se‖² (M_S ⪯ P_S). Next ‖e‖² − ‖P_Se‖² − ‖(I − P_{S₀})e‖² = ‖P_{S₀}e‖² − ‖P_Se‖²
≥ ‖P_{S₀}e‖² − ‖P_{S′}e‖² = −σ*²χ²_{J′} (col X_{c,S} ⊆ col X_{c,S′} and P_{S′} − P_{S₀} is the projection of (G3′)); on 𝒢^sup_n
(G3′) gives χ²_{J′} ≤ τ_{|J′|} ≤ C_A j₀ log n (χ²_∅ := 0; |J′| ≤ min(j₀, K) ≤ m♯_n for n ≥ n₀ by Lemma E0). With 𝒢⁵_n:
  D ≥ L_S − 2σ*√(2C_xL_S log n) − σ*²C_A j₀ log n − 8(M + σ*²).
*Exponent:* log(1 + u) ≥ (log 2) min(u, 1) for u ≥ 0 (concavity on [0, 1], monotonicity beyond), and ν ≥ n/2 ≥ N/2.
If D ≥ B′: ν log(1 + D/B′) ≥ (n/2) log 2 ≥ (s₀(A+1) + 2) log n for n ≥ n₀. Otherwise
ν log(1 + D/B′) ≥ (n/2)(log 2)D/(Nσ*²(1 + δ″_n)) ≥ (log 2/2)·D/(σ*²(1 + δ″_n)). Write L_S = λσ*² log n with λ ≥ c and
φ(λ) := λ − 2√(2C_xλ) − C_A j₀ = (√λ − √(2C_x))² − 2C_x − C_A j₀, increasing for λ ≥ 2C_x; c₁ ≥ 8C_x, so φ(λ) ≥ φ(c).
Then D/(σ*² log n) ≥ φ(c) − 8(M + σ*²)/(σ*² log n), and c > c₁ means φ(c) > (2/log 2)(s₀(A+1) + 2); put
η := φ(c) − (2/log 2)(s₀(A+1) + 2) > 0. For n ≥ n₀ (δ″_n → 0, 1/log n → 0):
(log 2/2)(φ(c) − o(1))/(1 + δ″_n) ≥ s₀(A+1) + 2. In both cases ℓ(S)/ℓ(S′) ≤ n^{s₀(A+1)}n^{−(s₀(A+1)+2)} = n^{−2}. ∎

## E2. Assembly (Theorem 1-VIS)
Let 𝒰 be the underfitting S ∈ Ω with |S| ≤ m♯_n. As in [P3] §main (i):
1 − π(S₀) ≤ π(|S| > m♯_n) + π(S ⊋ S₀, |S| ≤ m♯_n) + π(𝒰).
- Tail: O_P(n^{−1/2}) by T02(i♯) (or [L1a′]) — uses (E), (F₀) only.
- Supersets: on 𝒢^sup_n, ≤ e^{ρ_n}Υ′_n = O_P(r_n) by `A_occam.md` (C5′) — uses (E), (F₀), (OS) only.
- Underfits: [P3] `lem:assemble`'s argument with Υ′_n (that is, (C8′)): for S ∈ 𝒰 write ℓ(S)/ℓ(S₀) = [ℓ(S)/ℓ(S′)]·[ℓ(S′)/ℓ(S₀)];
  each S′ = S₀ ∪ J′ arises from < 2^{s₀} underfits; if |J′| ≤ j₀ then S ∈ 𝔉 and, by (ID^M; c) and Lemma E1(b),
  ℓ(S)/ℓ(S′) ≤ n^{−2} on 𝒢^sup_n ∩ 𝒢⁵_n; if |J′| > j₀ use [T03R] (C6)(a) (no condition): ℓ(S)/ℓ(S′) ≤ (2p)^{s₀}(n+1)^{s₀/2}.
  The second factors sum to ≤ 1 + e^{ρ_n}Υ′_n, resp. ≤ e^{ρ_n}Υ′^{>j₀}_n ((C5′)(a)). Hence on 𝒢^sup_n ∩ 𝒢⁵_n
  π(𝒰) ≤ 2^{s₀}n^{−2}(1 + e^{ρ_n}Υ′_n) + 2^{s₀}e^{ρ_n}(2p)^{s₀}(n+1)^{s₀/2}Υ′^{>j₀}_n = O_P(n^{−2} + r_n) by (C5′)(c).
- P((𝒢^sup_n)ᶜ ∪ (𝒢⁵_n)ᶜ) ≤ 5/n. ((G4) is not used anywhere in Claim E.)
So δ_n = O_P(r_n). Items 2–4: [SL] (deterministic consequences of δ_n). (5b′): with 𝒰_j := {S ∈ Ω : |S| ≤ m♯_n, j ∉ S}
(all underfitting), the same bound holds with (ID^M_j; c) in place of (ID^M; c), and π(S ∌ j) ≤ π(|S| > m♯_n) + π(𝒰_j).
(6): [POST] step (5) verbatim along deterministic sequences in the events, with common (M, φ₀, C_OS, n_OS, c). ∎

**Where each hypothesis enters.** (F₀): R_n and η_n (B′ bound; (C4′) numerator; tail). (OS): superset sums. (ID^M): only
Lemma E1 for S ∈ 𝔉. (E): ‖y_c‖², b, R_n, tail. p ≤ n^A: union bounds ((G2), (G3′), 𝒢⁵_n) and j₀. No eigenvalue condition
on S, S′ or S₀ ∪ J for J ≠ ∅.

## E3. Relations and remarks
1. (F_λ) ∧ BM(c) ⇒ (ID; c(1 − 1/n)): for S ∈ 𝔉, (F_λ) gives λ_min(G_{S′}) ≥ Nφ₀² (|S′∖S₀| ≤ j₀), so [P3] `lem:signal`
   gives Δ_S ≥ Nφ₀²‖θ*_{S₀∖S}‖² ≥ (1 − 1/n)cσ*² log n. Hence (ID; c(1 − 1/n)) ⇒ (ID^M; c(1 − 1/n)), and for c > c₁ (strictly, c(1 − 1/n) > c₁ eventually) Theorem 1-VIS
   contains [W3P] Theorem 1 items 1–4 and Claim A1 items 1–4.
2. Constants: c₁ = 160.8 at s₀ = A = 1 (C_x = 8.609, C_A j₀ = 44) vs c₀ = 128; both are proof artefacts. Numerics
   (`../numerics/post2_checks_out.txt` N4, s₀ = 1, fixed p; coefficient scale θ² = c log n/n, achieved full (ID) minimum ≈ c log n) [S01-5]: c = 4, 8: δ/r_n between 0.58 and 1.18, HPM ≥ 0.9;
   c = 2: δ/r_n 3.6 → 8.6; c = 1: δ ≈ 0.86–0.96 (finite-sample observations, n ≤ 6400) [K-AE-6].
3. No converse to (ID) is proved here [K-AE-5]. N1 with κ = 1 illustrates a small-margin obstruction (full (ID) minimum over the j₀-family
   0.38 → 0.22 times log n, (ID^M) minimum 0.80 → 0.45 times log n, δ_n between 0.56 and 0.69 for n = 100 … 6400); W3-POST records a deletion obstruction
   (heuristic) for beta-min below 2a + 1.
4. (F_λ) is not needed (Theorem 1-VIS); numerical illustration N1 with κ = 0.5 (λ_min(R_{S₀∪{3}}) ≍ n^{−1/2} by construction,
   full (ID) minimum 3.2 → 17.5 times log n): δ_n/r_n between 0.80 and 1.20, HPM = S₀ in ≥ 85% of seeds at n = 100 and 100% for n ≥ 400.
5. Answer to "is the floor set size improvable": yes. Besides the floor on S₀ itself, the theorem needs only a
   superset Occam sum (OS) — whose unweighted capped counterpart 𝒪⁰_n is necessary by Claim A2 [K-AE-5] — and an identifiability margin on underfits with at most j₀
   extra variables. The sufficient interface uses the ridge loss L_S; projection masking is measured by Δ_S ≤ L_S, and
   the W3-POST E4 numerics illustrated that projection component (θ²_min nφ₀²/log n for an anchored near-duplicate) [K2-2].
