# P2 — Proposition OVL⁺ (start mass under a bounded leakage set, either visibility condition)

Status: **PROVED (by this seat)**. The check record is kept outside this file (the ticket's final checkpoint file and `reviews/`).
Statement proved: `STATEMENT.md` §3.2 (T5⁺), Proposition OVL⁺ and its consequence for P-OVL. BASE :=
`Theory_work/Wave3/W3-START/`. Uses: BASE `lemmas/L1_AGG_FLOOR.md` ((P3), (CH)), BASE `lemmas/L2_TK.md` (𝓔^blk,
(TK-a), (TK-d), (TK-e), (TK-f)), BASE `lemmas/L10_INTERFACES.md` (steps (iii)–(iv) of L10.2), and (T1⁺)(a)
(`lemmas/P1_LEADING.md` P1.5(a), which is BASE L5.3(a)).

## P2.1 A deterministic identity and inequality (any data)

Valid inputs, n ≥ 4, EX-A; any partition with blocks of size ≤ min(16, K); any reference model S₀ ∈ Ω; Q ⊇ S₀ with
|Q| ≤ K; γ₀, π₀, 𝓛(Q) as in BASE `STATEMENT.md:58`, `:80-81`. For l ∉ S₀ (in particular for l ∈ Q ∖ S₀):
m_l := max{r_b(T ∪ {l})/r_b(T) : U*_b ⊆ T ⊆ C_b ∖ {l}}, b = b(l) (BASE `lemmas/L1_AGG_FLOOR.md:29`). Put
**Z_𝓛 := Σ_{T∈𝓛(Q)}γ₀(T)** and Z_Ω := Σ_{V∈Ω}γ₀(V). All γ₀ are positive (BASE `lemmas/L1_AGG_FLOOR.md:10`).

**Lemma P2.1.** (a) 1/π₀(S₀) = [Z_𝓛/γ₀(S₀)]·[1/π₀(𝓛(Q))]. (b) Z_𝓛/γ₀(S₀) ≤ ∏_{l∈Q∖S₀}(1 + |Q|·m_l/p).

*Proof.* (a) π₀(S₀) = γ₀(S₀)/Z_Ω and π₀(𝓛(Q)) = Z_𝓛/Z_Ω (𝓛(Q) ⊆ Ω because |Q| ≤ K); divide.
(b) The elements of 𝓛(Q) are the sets T = S₀ ⊔ N with N ⊆ Q ∖ S₀, each exactly once. Fix N, a := |N|, N_b := N ∩ C_b.
Then T ∩ C_b = U*_b ⊔ N_b and
  γ₀(T)/γ₀(S₀) = [w(s₀ + a)/w(s₀)]·∏_b r_b(U*_b ∪ N_b)/r_b(U*_b)
(blocks with N_b = ∅ contribute 1; the table entries exist because |U*_b ∪ N_b| ≤ |C_b| ≤ K).
*Tables.* By the chain bound (CH) (BASE `lemmas/L1_AGG_FLOOR.md:29-32`) with T := U*_b and N := N_b (N_b ⊆ C_b ∖ U*_b,
N_b ∩ S₀ = ∅): r_b(U*_b ∪ N_b)/r_b(U*_b) ≤ ∏_{l∈N_b}m_l.
*Prior.* By the path bound (P3) (BASE `lemmas/L1_AGG_FLOOR.md:19-23`) with k := s₀, D := 0 and a (0 ≤ k ≤ p;
k + a = |T| ≤ |Q| ≤ K ≤ p): w(s₀ + a)/w(s₀) ≤ p^{−a}·(s₀ + 1)_a, and (s₀ + 1)_a = ∏_{i=1}^{a}(s₀ + i) ≤ (s₀ + a)^a ≤ |Q|^a.
So γ₀(T)/γ₀(S₀) ≤ ∏_{l∈N}(|Q|m_l/p). Summing over all N ⊆ Q ∖ S₀: Σ_N∏_{l∈N}(|Q|m_l/p) = ∏_{l∈Q∖S₀}(1 + |Q|m_l/p). ∎

(Lemma P2.1(b) is the part of the proof of (AGG-c) with no deleted truth and no column outside Q, BASE
`lemmas/L1_AGG_FLOOR.md:91-101`. Neither e_n nor U_Q appears.)

## P2.2 Proposition OVL⁺

**Hypotheses.** Setting F, (E), (GF-16); visibility: (V-c) (c_V > 1 + 2A), or (V-m) with constants (c_m, ε₀) for this Q;
Q = Q_n ⊇ S₀ deterministic with |Q| ≤ K and |Q ∖ S₀| ≤ q̄ (fixed); (AL) for Q with a level vector h; deterministic levels
a_l = a_{n,l} with 0 ≤ a_{n,l} ≤ ā < ∞ (ā fixed), uniformly in n and l ∈ Q_n ∖ S₀, with δ²_{U,l} ≤ a_l·τ²_U·log n for every
l ∈ Q ∖ S₀ and every U ⊆ [p] ∖ {l}, |U| ≤ 15.
**Claim.** For every ε > 0: P(π₀(S₀) ≥ n^{−E_n−ε}) → 1, E_n := Σ_{l∈Q∖S₀}[(a_l − 1)/2 − log p/log n]₊.

*Proof.* Fix ε > 0.
*Events.* 𝓔^blk (P((𝓔^blk)ᶜ) → 0, BASE `lemmas/L2_TK.md:32`);
𝓨 := {Z²_{T,l} ≤ 2 log log n for every l ∈ Q ∖ S₀ and T ⊆ C_{b(l)} ∖ {l}}, with P(𝓨ᶜ) ≤ q̄·2^{16}/log n (BASE
`lemmas/L10_INTERFACES.md:38`); and **𝓐 := {π₀(𝓛(Q)) ≥ ½}**.
*P(𝓐) → 1.* The hypotheses of (T1⁺)(a) hold — (E), (GF-16), visibility ((V-c), or (V-m) for Q), (AL) for Q with h —
so, for any κ ∈ (0, κ_V), 1 − π₀(𝓛(Q)) = O_P(ϱ_n(Q; h)) + o_P(n^{−κ}), and ϱ_n(Q; h) → 0 by (AL). Hence 1 − π₀(𝓛(Q)) → 0 in
probability. This is the only place where visibility and (AL) are used.
*The columns of Q ∖ S₀.* If q̄ ≥ 1: on 𝓔^blk ∩ 𝓨 and for n large, for every l ∈ Q ∖ S₀,
  **m_l ≤ n^{(a_l−1)/2+ε/(3q̄)}**.
This is step (iii) of the BASE proof of L10.2 (`lemmas/L10_INTERFACES.md:44-50`). It uses, for each T with
U*_b ⊆ T ⊆ C_b ∖ {l}: (TK-e) and 𝓨 for RSS_T − RSS_{T∪l} = (δ_{T,l} + σZ_{T,l})² ≤ τ²_TG_n (the assumed gain bound applies
because |T| ≤ 15); (TK-a) for x ≤ G_n/((n − 1)(1 − ω̄_n)) → 0; and (TK-d), (f3). No visibility condition, no bound on
e_n and no bound on U_Q enters that step. Then, as in step (iv) (`:51-52`), with |Q| ≤ s₀ + q̄:
  ∏_{l∈Q∖S₀}(1 + |Q|m_l/p) ≤ (1 + s₀ + q̄)^{q̄}·n^{E_n+ε/3}.
If Q = S₀ the product is empty and equals 1 (and E_n = 0).
*Conclusion.* On 𝓔^blk ∩ 𝓨 ∩ 𝓐 and for n large, by Lemma P2.1:
  1/π₀(S₀) = [Z_𝓛/γ₀(S₀)]/π₀(𝓛(Q)) ≤ 2·(1 + s₀ + q̄)^{q̄}·n^{E_n+ε/3} ≤ n^{E_n+ε},
and P(𝓔^blk ∩ 𝓨 ∩ 𝓐) → 1. ∎

**Consequence for P-OVL.** As in BASE `lemmas/L10_INTERFACES.md:55-61`, unchanged: if
limsup_n(E_n − max(1, log p/log n)) < 0, take ε with E_n + 2ε ≤ max(1, log p/log n) eventually; then with probability
→ 1, max(n, p)·log₂(n + 1)·π₀(S₀) ≥ n^ε·log₂(n + 1) → ∞ — the production form of P-OVL (SAMP (D-iv)), also when S₀ is not
the start mode.

## P2.3 Remarks
1. Compared with the BASE proof: the factor (1 + e_n)^{s₀}(1 − U_Q)^{−(|Q|+1)} of (AGG-c), which needed (V-c) (through
   Proposition L4.2) and the event 𝓜′, is replaced by the single factor 1/π₀(𝓛(Q)) ≤ 2, which (T1⁺)(a) controls under
   either visibility condition. The proof under (V-c) is covered by the same argument.
2. (V-m) must be the condition for the same Q: its instances with R ⊆ Q ∖ S₀ are what (T1⁺)(a) uses (BASE
   `STATEMENT.md:143-151`).
3. Lattice concentration alone would not give the claim: the mass of S₀ **inside** the lattice is controlled by the
   gain levels a_{n,l} of the columns of Q ∖ S₀, through Lemma P2.1(b).
