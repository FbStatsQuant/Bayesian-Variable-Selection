# L2 — Centre law with a general reference S* (generalized T22(iii)); claim (C1)

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol): VERIFIED-WITH-AMENDMENTS, amendments
applied (v2, reviews/R02_R04_disposition.md).
Inputs: T22(i) "PROVED-LOCKED" (`Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md` §2(i): deterministic,
any partition with |C_b| ≤ B ≤ K, positive tables, **any feasible reference S°**); the proof text of T22(iii)
(`Docs/Theory/proofs/T22iii_T16_start_aggregation/PROOF_v2.tex`, "PROVED-LOCKED CONDITIONAL", reference S₀, EXP′
assumed), cited below as [P:line]; L1 of this folder.

## Statement

**Theorem L2.** Assume G; ‖μ‖² ≤ Mn; p ≤ n^A; and (H2) with a deterministic reference S* ∈ Ω, s* = |S*| ≤ v̄ fixed,
s* ≤ K eventually. Let U*_b := S* ∩ C_b and, for p > s*,

  u_n := (p − s*)⁻¹ Σ_{l∉S*} max_{T : (b(l),T,l)∈𝓛(S*)} r_{b(l)}(T ∪ {l})/r_{b(l)}(T),
  e_n := 2p max_{b, U⊆C_b : a := |U*_b∖U| > 0} [r_b(U)/r_b(U ∪ U*_b)]^{1/a}

(u_n := 0 if p = s*; e_n := 0 on an empty index set). Then with a_n := 2^B √(log n) n^{−κ}:
u_n = O_P(a_n), e_n = o_P(n^{−m}) for every fixed m > 0, and 1 − π₀(S*) = O_P(a_n) → 0. On {π₀(S*) > ½} the
maximiser of γ₀ over Ω is unique and equals S*; hence P(S̃₀ = S*) → 1, whatever the tie rule.

## Proof (substitution list against [P])

The proof of [P] uses the truth S₀ only (i) as the reference defining U*_b, the leakage family, u_n, q_n, e_n, and
(ii) through "s₀ fixed, eventually feasible". It never uses μ ∈ span X_{S₀}, nor that leakage indices are nulls, nor
that missing reference variables are true: residual control uses only ‖μ‖² ≤ Mn ([P:149-203]); the leakage integral
allows any δ_{T,l} ([P:249-280]); completion uses VIS only ([P:334-401]). We re-run it with S* in place of S₀:

1. **Setting [P:35-131].** Replace U*_b = S₀ ∩ C_b by U*_b = S* ∩ C_b; 𝓛 := 𝓛(S*) = {(b,T,l) : l ∈ C_b ∖ U*_b,
   U*_b ⊆ T ⊆ C_b ∖ {l}} (note: [P:85] writes l ∉ S₀; here l ∉ S*, which may include true variables — masked truths);
   averages over l ∉ S* with denominator p − s*; VIS (H2b) and E_{T,l}, NL_avg(κ) (H2c)(ii) as in STATEMENT §2.
   The directions u_{T,l} exist for every within-block addition by (H2a) ([P:48-64]).
2. **EXP′ is proved, not assumed.** Apply L1 to 𝔉_blk := {T : T ⊆ C_b for some b}: |𝔉_blk| ≤ p2^B ≤ 2^{16}n^A
   (fixed J = 16 ≥ B_n, C_F = 2^{16}, D = A, C_V = 2·2^{32}, D_V = 2A), Gram floor by (H2a), 𝒱𝒱 := {r_T} ∪ {r_T − r_{T′}} over 𝔉_blk. L1.3 gives, on 𝒟₁ ∩ 𝒟₂ ∩ 𝒟₃
   (probability → 1) and n ≥ n₀, for every within-block addition (b, T, l):
   log[r_b(T ∪ {l})/r_b(T)] = −½ log(n + 1) − ν log(1 − x_{T,l}) + R_{n,b,T,l}, |R_{n,b,T,l}| ≤ 2κ_E.
   With the remainder defined on the whole space as in L1.3 (R := log[r_b(T+l)/r_b(T)] + ½log(n+1) + ν log(1 − x_{T,l}),
   finite a.s. for n large), ρ_n := max|R| satisfies P(ρ_n > 2κ_E) → 0, so ρ_n = O_P(1): the strict version of
   [P]'s EXP′ ([P:73-80]) holds; the score identity holds a.s. by definition, also off the event.
3. **Lemma residual [P:149-203]** holds verbatim (it uses only ‖μ‖² ≤ Mn, |𝒯| ≤ p2^B and Gaussian tails).
4. **Lemma quad [P:205-245]** with NL_C in place of NL_η: on ℋ_n := {max_𝓛 |Z_{T,l}| ≤ h_n} (probability ≥ 1 −
   2^{17}n^{−ε₀}, [P:220-226]), (H2c)(i) gives max_𝓛 (δ_{T,l} + σZ_{T,l})² ≤ σ²(√C_L + √(2(A + ε₀)))² log n; with
   Lemma residual this gives max_𝓛 x_{T,l} = O_P(log n/n), max n x² = o_P(1), and d_n = o_P(1), exactly as in [P:226-243]
   (only "O(log n)" of the numerator was used there; its constant is irrelevant).
5. **Lemma integral [P:249-280]** is a statement about a single Gaussian and is unchanged.
6. **Proposition u_n [P:282-329]** holds verbatim with the sums over l ∉ S*, denominator p − s*, and the average
   bound (H2c)(ii) in place of [P]'s (eq:avg); at most 2^B terms per l; Markov; the product bound
   u_n ≤ (n + 1)^{−1/2}exp(ρ_n + d_n)V_n on ℋ_n uses EXP′ (step 2) and step 4. Result: u_n = O_P(a_n).
7. **Proposition e_n [P:334-401]** with VIS(S*): for (b, U) with a = |U*_b ∖ U| > 0, P := P_{U∪U*_b} − P_U is a
   deterministic projection of rank a (nested subspaces; rank a by (H2a)), 1 ≤ a ≤ B. The telescoping along a fixed
   ordering of the a missing **reference** variables uses EXP′ (step 2); ‖Pμ‖² = g_{b,U} ≥ M_n v_U log n by (H2b);
   [P:368-399] then gives e_n ≤ 2n^A(n + 1)^{1/2}e^{ρ_n}n^{−cM_n/16} on an event of probability → 1, with
   c = σ²/(8C_R), so e_n = o_P(n^{−m}) for every m. (The words "missing true variables" at [P:362] read "missing reference variables" here.)
8. **Aggregation [P:427-468].** T22(i) with the feasible reference S* (locked; any feasible reference): q_n ≤ u_n and,
   on {u_n < 1}, 1 − π₀(S*) ≤ (s* + 1)u_n/(1 − u_n) + s*e_n. On {u_n ≤ ½}: 1 − π₀(S*) ≤ 2(s* + 1)u_n + s*e_n.
   With s* ≤ v̄ fixed, steps 6–7 give 1 − π₀(S*) = O_P(a_n + e_n) = O_P(a_n) → 0.
9. **Uniqueness of the mode.** On {π₀(S*) > ½}: every S ∈ Ω ∖ {S*} has π₀(S) ≤ 1 − π₀(S*) < ½ < π₀(S*), i.e.
   γ₀(S) < γ₀(S*). So S* is the unique maximiser of γ₀; any tie rule returns it; under premise e4 the emitted LS0
   centre is S*. Hence P(S̃₀ = S*) ≥ P(π₀(S*) > ½) → 1. ∎

**What changed relative to [P], in one list.** Reference S₀ → S*; leakage indices l ∉ S* (may be true variables);
NL_η → (NL_C, NL_avg(κ)) (NL_η implies both for admissible κ and sufficiently small ε₀, [P:404-425]); EXP′ assumed → proved (L1, needs (H2a) and bounded energy);
"s₀ fixed" → "s* ≤ v̄". Nothing else.

**Remark (masking).** A masked truth j ∈ C_b ∖ U*_b is a leakage index: (H2c)(i) asks δ²_{T,j} ≤ C_Lσ² log n for
U*_b ⊆ T ⊆ C_b ∖ {j} — at most O(log n) squared partial signal on the leakage family (exact masking, δ = 0, is the
special case η = 0) — while posterior consistency (H0) and the descent
(L3) still recover it. This is the masked regime of M3(f)/M5 in general form.
