# L10 — Interface corollaries (T5): IF-START, Proposition OVL; Corollary MIS (T6)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §5.3 (T5) (IF-START, Proposition OVL) and (T6) (Lemma R′ and Corollary MIS); the rows
P-START, P-OVL of §4. Uses `lemmas/L1_AGG_FLOOR.md` ((AGG-c)), `lemmas/L2_TK.md`, `lemmas/L3_LEAK.md` (L3.4),
`lemmas/L4_VIS.md` (𝓧, L4.2), `lemmas/L5_ASM_STARTF.md` ((T1)(b)), `lemmas/L8_TRANSFER.md`, `lemmas/L9_BR.md` ((T3)(b)).
Consumers' wording is quoted from `Theory_work/Wave3/W3-SAMP/STATEMENT.md` (lines 76–77, 82–83, 103–105, 158–162).

## L10.1 IF-START

**(a) Fixed design.** Under (T1) with (AL) at Q = S₀ and level vector h, let 0 < κ < κ_V and
r_n := n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)² + n^{−κ} (deterministic; r_n → 0 by `lemmas/L5_ASM_STARTF.md` L5.3(b)). By (T1)(b) applied
with an exponent κ₁ ∈ (κ, κ_V): o₀ = O_P(n^{−1/2}𝔏⁰_n(h) + n^{−1}𝔏_n(S₀; h)²) + o_P(n^{−κ₁}) = O_P(r_n). For any event 𝒜,
0 ≤ 1_𝒜o₀ ≤ o₀, so **1_𝒜o₀ = O_P(r_n)** and in particular 1_𝒜o₀ → 0 in probability: this is P-START
("1_𝒜·o₀ → 0 in probability, i.e. π₀(S₀) → 1 on 𝒜", SAMP `STATEMENT.md:76`).
**(b) Gaussian rows.** Under (T3)(b) with Q = S₀: with probability → 1, 1 − π₀(S₀) ≤ ρ_n := (s₀ + 1)n^{−1/2}exp(C_R√log n) → 0; on
that event and for n large (ρ_n ≤ ½), o₀ = (1 − π₀(S₀))/π₀(S₀) ≤ 2ρ_n. So 1_𝒜o₀ = O_P(n^{−1/2}exp(C_R√log n)): the same with
r_n := n^{−1/2}exp(C_R√log n).
**(c) What the consumer gets.** SAMP Theorem C (C-v) reads: "if moreover 1_𝒜δ̄ = O_P(r_n) (deterministic r_n ↓ 0) then,
localised to 𝒜, Ẑ/Z − 1, log Ẑ − log Z and ‖pip_primary − 1_{S₀}‖_∞ are O_P(r_n)", and "1_𝒜·δ̄ → 0 in probability
(⇔ 1_𝒜o₁ → 0 and P-START …)". IF-START supplies the start half of that premise with a deterministic rate; if P-CONC
holds with a deterministic rate r^{post}_n, SAMP's own clause applies with the rate max(r_n, r^{post}_n) (replace r_n by
sup_{m≥n}r_m if a nonincreasing rate is wanted). P-CONC, P-MAP and SAMP's algorithm premises are not supplied here, and
no statement is made about δ̄ beyond what SAMP's (C-v) derives from its two premises. ∎

## L10.2 Proposition OVL

**Hypotheses.** Setting F, (E), (GF-16), (V-c) (c_V > 1 + 2A); Q ⊇ S₀ deterministic with |Q ∖ S₀| ≤ q̄ (fixed) and |Q| ≤ K;
(AL) for Q with a level vector h; deterministic levels a_l = a_{n,l} with 0 ≤ a_{n,l} ≤ ā < ∞ for a fixed ā, uniformly in n
and l ∈ Q_n ∖ S₀, with δ²_{U,l} ≤ a_l·τ²_U·log n for every l ∈ Q ∖ S₀ and U ⊆ [p] ∖ {l}, |U| ≤ 15. (Q = Q_n may change with n; the
uniform bound ā is what the proof uses.)
**Claim.** For every ε > 0: P(π₀(S₀) ≥ n^{−E_n−ε}) → 1, E_n := Σ_{l∈Q∖S₀}[(a_l − 1)/2 − log p/log n]₊.

*Proof.* By (AGG-c), whenever U_Q < 1:
  1/π₀(S₀) ≤ (1 + e_n)^{s₀}·(1 − U_Q)^{−(|Q|+1)}·∏_{l∈Q∖S₀}(1 + |Q|m_l/p),                                  (10.1)
where m_l := max{r_b(T ∪ {l})/r_b(T) : U*_b ⊆ T ⊆ C_b ∖ {l}}, b = b(l).
*Events.* 𝓔^blk; 𝓧 (if s₀ ≥ 1); 𝓩_h;
𝓨 := {Z²_{T,l} ≤ 2 log log n for every l ∈ Q ∖ S₀ and T ⊆ C_{b(l)} ∖ {l}} (at most q̄·2^{15} standard normal variables, so
P(𝓨ᶜ) ≤ q̄·2^{16}/log n); and 𝓜′ := {U_Q ≤ λ′_n·n^{−1/2}𝔏^b_n(Q; h)} with λ′_n := (n^{−1/2}𝔏^b_n(Q; h))^{−1/2} (if [p] ∖ Q = ∅ then U_Q = 0 and
𝓜′ is the sure event). Since n^{−1/2}𝔏^b_n(Q; h) ≤ ϱ_n(Q; h) → 0, λ′_n → ∞, the premise of L3.4(a) holds for n large, and its
Markov step gives P(𝓜′ᶜ ∩ 𝓔^blk ∩ 𝓩_h) ≤ c_L/λ′_n → 0. So 𝒢 := 𝓔^blk ∩ 𝓧 ∩ 𝓩_h ∩ 𝓜′ ∩ 𝓨 has P(𝒢) → 1 (b_n(h) → 0).
*On 𝒢, n large.* (i) U_Q ≤ (n^{−1/2}𝔏^b_n(Q; h))^{1/2} → 0 and |Q| + 1 ≤ s₀ + q̄ + 1 is bounded, so (1 − U_Q)^{−(|Q|+1)} ≤ 2.
(ii) By Proposition L4.2 (on 𝓔^blk ∩ 𝓧, under (V-c)): e_n ≤ 2^{−16}n^{−κ} ≤ 1 for some κ > 0; so (1 + e_n)^{s₀} ≤ 2^{s₀}.
(iii) Let l ∈ Q ∖ S₀, b = b(l), U*_b ⊆ T ⊆ C_b ∖ {l}. By (TK-e) and 𝓨: RSS_T − RSS_{T∪l} = (δ_{T,l} + σZ_{T,l})²
≤ (1 + ε₁)δ²_{T,l} + (1 + 1/ε₁)σ²Z²_{T,l} ≤ τ²_T[(1 + ε₁)a_l log n + 2(1 + 1/ε₁) log log n] ≤ τ²_T·G_n,
G_n := (1 + ε₁)ā log n + 2(1 + 1/ε₁) log log n, for any ε₁ ∈ (0, 1]. As in `lemmas/L7_NEC.md` L7.2: x ≤ G_n/((n − 1)(1 − ω̄_n)) → 0, and by (TK-d), (f3):
  log[r_b(T ∪ l)/r_b(T)] ≤ −½ log(n + 1) + (1 + ϑ̄_n)(1 + x̄_n)[(1 + ε₁)a_l log n + 2(1 + 1/ε₁) log log n]/2 + 2κ_E
   ≤ [(a_l − 1)/2 + ε₁ā/2 + o(1)] log n,
with o(1) depending only on (n, A, ā, ε₁) and the fixed constants. Choosing ε₁ := min(1, ε/(2q̄ max(ā, 1))): **m_l ≤ n^{(a_l−1)/2+ε/(3q̄)}** for n large, for every l ∈ Q ∖ S₀ (if q̄ = 0 there is nothing
to prove here).
(iv) With |Q| ≤ s₀ + q̄ and p = n^{log p/log n}: 1 + |Q|m_l/p ≤ 1 + (s₀ + q̄)n^{(a_l−1)/2−log p/log n+ε/(3q̄)}
≤ (1 + s₀ + q̄)·n^{[(a_l−1)/2−log p/log n]₊+ε/(3q̄)}. The product over the at most q̄ columns is ≤ (1 + s₀ + q̄)^{q̄}n^{E_n+ε/3}.
(v) Insert (i)–(iv) in (10.1): 1/π₀(S₀) ≤ 2^{s₀+1}(1 + s₀ + q̄)^{q̄}·n^{E_n+ε/3} ≤ n^{E_n+ε} for n large. ∎

**Consequence for P-OVL.** SAMP (D-iv): "production corollary: P-OVL may be replaced by max(n, p)·log₂(n+1)·π₀(S₀) → ∞ in
probability". max(n, p) = n^{max(1, log p/log n)}. If limsup_n(E_n − max(1, log p/log n)) < 0, take ε with
E_n + 2ε ≤ max(1, log p/log n) eventually; then with probability → 1,
max(n, p)·log₂(n + 1)·π₀(S₀) ≥ n^{ε}·log₂(n + 1) → ∞. So the production form of P-OVL holds, also when S₀ is not the start
mode. With Q = S₀ (q̄ = 0): E_n = 0, and π₀(S₀) → 1 by (T1)(b) already gives it.
(Only the production form is derived; SAMP's general P-OVL involves its own budget D_r, and P-OVL∞ is a different
interface. Proposition OVL is stated under (V-c) only. Used through (T6) or (T3)(a), it carries their conventions.)

## L10.3 Lemma R′ and Corollary MIS (T6)

Setting of MIS (`Theory_work/Wave1C/C-MIS/STATEMENT.md:39-58`): candidate columns 𝒞, omitted columns 𝓜;
y^r = α1 + X^r_𝒞β_𝒞 + ω + ε, ω := X^r_𝓜β_𝓜; the method is re-run on the candidate data (X^r_𝒞, y^r), with p_𝒞 := |𝒞| in the
prior and the cap. (GR): ω = a1 + X^r_𝒞γ + ξ with ξ ~ N_n(0, τ²I), τ² ≥ 0 fixed; ξ and ε independent, ε ~ N_n(0, σ²I); for a
fixed candidate design a and γ are constants, in the random-design form they are measurable functions of X^r_𝒞 and
the distributional statements hold conditionally on X^r_𝒞.

**Lemma R′.** Under (GR): y^r = (α + a)1 + X^r_𝒞β^𝒞 + ε′ with β^𝒞 := β_𝒞 + γ and ε′ := ε + ξ ~ N_n(0, σ_𝒞²I), σ_𝒞² := σ² + τ² > 0
(conditionally on X^r_𝒞 in the random-design form).
*Proof.* Substitute ω; a sum of independent centred Gaussian vectors with covariances σ²I and τ²I is N_n(0, (σ² + τ²)I). ∎
(This is the algebra of MIS Lemma R, status "R02 VERIFIED; council R07/R08 PASS"; it is re-derived here in two lines
and not consumed.)

**Corollary MIS, fixed candidate design.** By Lemma R′ the candidate data follow Setting F with design X^r_𝒞,
(p, β, σ²) := (p_𝒞, β^𝒞, σ_𝒞²), truth S₀^𝒞 := supp β^𝒞 and θ^𝒞 := D_xβ^𝒞. The start π₀^𝒞 of the re-run method is the coded start of
`STATEMENT.md` §1 computed from (X^r_𝒞, y^r). Each of (C0)–(C2), (T0)–(T2), (T4), (T5) is a statement about the coded
start under Setting F (the deterministic ones about any valid data), so each holds for π₀^𝒞 **provided its hypotheses
hold after the substitution**. In particular, under the substituted (E), (GF-16), visibility and (AL) at S₀^𝒞:
π₀^𝒞(S₀^𝒞) → 1 in probability, and for any model S′ ≠ S₀^𝒞 — for example S′ = S₀ ∩ 𝒞 whenever S₀ ∩ 𝒞 ≠ S₀^𝒞 —
π₀^𝒞(S′) ≤ 1 − π₀^𝒞(S₀^𝒞) → 0.
**Random candidate design.** Conditionally on X^r_𝒞: y^r = (α + a(X^r_𝒞))1 + X^r_𝒞β^𝒞(X^r_𝒞) + ε′, ε′ | X^r_𝒞 ~ N_n(0, σ_𝒞²I). This is the
setting of `lemmas/L8_TRANSFER.md` L8.0 with X^r := X^r_𝒞, α := α + a, β := β^𝒞, σ² := σ_𝒞²; S₀^𝒞, Q and h may be measurable
functions of X^r_𝒞. So (T3)(a) applies on design sets 𝒳_n as there (fixed |S₀^𝒞| = s₀ on 𝒳_n, and the other admissibility
conditions). Candidate sets, supports or coefficients selected using the response are not covered (L8.3). ∎
