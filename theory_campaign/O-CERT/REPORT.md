# O-CERT — REPORT: a-posteriori certificates for individual fits at finite n

Run of 2026-11-02, branch `theory/O-CERT` (from `theory/campaign`). Lead: Opus 5.5. **Nothing here is reviewed.**
Every PROVED is a candidate that I checked line by line; it is not adopted. Scripts are in `scripts/`, outputs in
`results/`.

## 1. Headline

1. **Direction (task item ii): PROVED.** The locked Markov bound P(Z ≥ 0.05Ẑ) ≥ 0.95 is a *lower* bound on Z, so it
   gives an **upper** bound on π(Ŝ) = e^{F(Ŝ)}/Z, never a lower one. It holds *simultaneously for every model*
   (the bad event is {Z < 0.05Ẑ}, whatever Ŝ is), so selecting Ŝ from the same run costs nothing (Thm C1).
   Combined with the deterministic Z ≥ Z_𝒯 (the sum over the reported top store) it reads
   π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, 0.05Ẑ). A *lower* bound on π(Ŝ) needs an upper bound on Z. That does **not** follow from
   unbiasedness (locked T31(c)), and the 4-island spread cannot supply it (T31(d), T12(iv.e)). Under PW2 (T25(iv)),
   Cantelli gives a two-sided band (Thm C2, PROVED but CONDITIONAL on PW2, which is not data-checkable). T13's
   restricted ESS does not give a lower bound on π(Ŝ) without PW2.
2. **Exact relative certificates (items i, iii): PROVED, deterministic, any n.** On any region R that is fully scored,
   π(Ŝ | R) is computed exactly. Examples are the closed flip/swap neighbourhood behind `local_certified`, the 2^{|Ŝ|}
   subsets of Ŝ, and the best-of-scored gap g, which gives π(S)/π(Ŝ) ≤ e^{−g} for every scored S (Thm C3).
3. **Box certificate (item iv): PROVED (new monotonicity lemma).** As S grows, Q_S decreases and D_S increases
   (Lemma M). So F(S) ≤ Φ(L, U) on every box L ⊆ S ⊆ U, and a branch-and-bound tree over 2^U certifies, from
   (X, y, Ŝ) alone, that **Ŝ is the exact HPM among all 2^{|U|} models built from U**. It also gives a deterministic
   lower bound on π(Ŝ | 2^U). On {S₀ ⊆ U}, any miss is certified to be a posterior miss (Thm C4, Cor C5).
4. **Certificate card (item v): PROVED (candidate).** The run reports local, region and global one-sided items. Then
   P(output and some item on the card is false) ≤ 0.05·P(𝒜) ≤ 0.05 at every n, with no asymptotics and no conditioning
   on completion (Lemma RO). This is the right finite-n statement for n = 200 (Thm C6). The card certifies
   **optimality and uncertainty**: "Ŝ beats every model in an explicit region" and "π(Ŝ) is at most u". It cannot
   certify **confidence**: "π(Ŝ) ≥ ½" or "Ŝ is the global HPM" are out of reach without PW2 or exact enumeration.
5. **Illustration** on 4 regenerated study datasets (p = 500, n = 200, production engine, study seeds; §4). Engine
   and certificate scores agree to 3·10⁻¹². On every fit, Z_𝒯 > 0.05Ẑ, so the G bound is in fact *deterministic*
   (π(Ŝ) ≤ 0.37 even when Ŝ = S₀). The box B&B certifies Ŝ = argmax over 2^{30–31} models in ≤ 38 s. Both c = 0.5
   misses (Ŝ = S₀ + 1 FP) are certified **posterior** misses, by g_del = F(Ŝ) − F(S₀) = 1.19 and 1.89 nats.

(STATUS words follow PROTOCOL.md. "Candidate" = not reviewed.)

## 2. Setting and notation

Notation of `00_COMMON.md` and the T12/T31 statements. Standardised (X, y), ‖x_j‖² = ‖y‖² = n − 1, K = min(p, ⌊n/2⌋),
Ω = {S ⊆ [p] : |S| ≤ K}. For S ∈ Ω, M_S := X_SX_Sᵀ (n × n),

  F(S) := log ϖ(S) + log m(S) = log w(|S|) − log W_K + log C_n − ½ log D_S − ν log(2b₀ + Q_S),

so π(S) = e^{F(S)}/Z and Z = Σ_Ω e^{F}. New symbols:
- 𝒮̄ is the scored set of the potential uninterrupted run R̄ (W2-BOOK). 𝒯 is any *reported* set of distinct scored
  models with their scores; the engine reports the top store `top_store`, the 40p + 1 best scored models, and
  `local_search`. Z_𝒯 := Σ_{S∈𝒯} e^{F(S)}.
- Ŝ is the reported HPM, and Ẑ = ¼Σ_rẐ_r is the reported pooled evidence.
- g := F(Ŝ) − max_{S∈𝒯∖{Ŝ}} F(S) ≥ 0 is the best-of-scored gap (the engine's top store gives it as top[1] − top[2]).
- 𝒩(c) is the feasible flip-or-swap neighbourhood (T20 §1), and N̄(c) := {c} ∪ 𝒩(c).
- For L ⊆ U ⊆ [p], the box [L, U] := {S ∈ Ω : L ⊆ S ⊆ U}, and
  - Φ(L, U) := log w(|L|) − log W_K + log C_n − ½ log D_L − ν log(2b₀ + Q_U);
  - M(L, U) := log Σ_{k=|L|}^{min(|U|,K)} C(|U|−|L|, k−|L|) w(k) − log W_K + log C_n − ½ log D_L − ν log(2b₀ + Q_U).
- 𝒪 is the output-available event, 𝒪_E ⊆ 𝒪 the event that an evidence value is reported, and 𝒜 the calibration
  success event (W2-BOOK, Prop 2).

Hypotheses (all named in locked results or W2-BOOK): EX-A, EX-S, CAL, START, (H-T12) = T12(iii), GUARD (stop-only
coupling, W2-BOOK). Floating point enters only through VAL-FP(η, ε) (W2-BOOK) and, for the deterministic items, the
score contract SC(η_F) below.

**SC(η_F)** (new code). Every score used by the card, whether computed by the engine or post hoc, is within η_F of
its exact value. This is the deterministic analogue of VAL-FP, and it is checkable by replay in higher precision.

## 3. Statements and proofs

### Lemma M (monotonicity of the score ingredients). PROVED.
For S ⊆ S′ ⊆ [p]: (a) Q_S ≥ Q_{S′}; (b) D_S ≤ D_{S′}; (c) w(k + 1) ≤ w(k) for 0 ≤ k ≤ p − 1, so w is non-increasing on
{0, …, K}. Moreover (d) Q_S = yᵀy/(n+1) + (n/(n+1))·yᵀ(I_n + (n+1)M_S)⁻¹y and
D_S = det(I_n + (n+1)M_S)/det(I_n + M_S).

*Proof.*
- **(d), first formula.** For c > 0 and any n × k matrix A, (I_n + cAAᵀ)A = A(I_k + cAᵀA). Hence
  A(I_k + cAᵀA)⁻¹ = (I_n + cAAᵀ)⁻¹A, and
  A(I_k + cAᵀA)⁻¹Aᵀ = (I_n + cAAᵀ)⁻¹AAᵀ = c⁻¹[I_n − (I_n + cAAᵀ)⁻¹].
  With A = X_S and c = n + 1, n·z_SᵀH_S⁻¹z_S = n·yᵀX_S(I + (n+1)G_S)⁻¹X_Sᵀy = (n/(n+1))·yᵀ[I − (I + (n+1)M_S)⁻¹]y.
  Substituting into Q_S = yᵀy − n z_SᵀH_S⁻¹z_S gives the formula. It also holds for S = ∅, where M_∅ = 0 and Q_∅ = yᵀy.
- **(d), second formula.** Sylvester: det(I_k + cG_S) = det(I_n + cM_S). Apply it with c = n + 1 and c = 1.
- **(a).** M_{S′} = M_S + Σ_{j∈S′∖S} x_jx_jᵀ ⪰ M_S. So I + (n+1)M_{S′} ⪰ I + (n+1)M_S ≻ 0, and inversion reverses the
  Loewner order: yᵀ(I + (n+1)M_{S′})⁻¹y ≤ yᵀ(I + (n+1)M_S)⁻¹y. Use the formula in (d).
- **(b).** It suffices to add one column x. Write M′ = M + xxᵀ. By the matrix determinant lemma,
  det(I + cM′) = det(I + cM)·h(c), with h(c) := 1 + c·xᵀ(I + cM)⁻¹x. So D_{S∪{j}}/D_S = h(n+1)/h(1). For c ≥ 0,
  (d/dc)[c(I + cM)⁻¹] = (I + cM)⁻¹ − c(I + cM)⁻¹M(I + cM)⁻¹ = (I + cM)⁻¹[(I + cM) − cM](I + cM)⁻¹ = (I + cM)⁻².
  Hence h′(c) = xᵀ(I + cM)⁻²x ≥ 0, h is non-decreasing, and h(n+1) ≥ h(1) > 0. Induct over the columns of S′ ∖ S.
- **(c).** w(k+1)/w(k) = C(2p−1, k)/C(2p−1, k+1) = (k+1)/(2p−1−k) ≤ 1 iff k ≤ p − 1. Since K ≤ p, every k + 1 ≤ K
  satisfies k ≤ p − 1. ∎

*Remark.* (a) is the Bayesian analogue of "RSS decreases when variables are added". It holds for this ridge-type Q with
no rank condition, so it holds at p ≫ n. Only (a)–(c) are used below.

### Theorem C1 (one-sided global certificate; selection-proof). PROVED (candidate).
Assume EX-A, EX-S, CAL, START and GUARD (the hypotheses of W2-BOOK Prop 2). Let 𝒯 be any reported set of distinct
models with exact scores, a function of the output. Fix α ∈ (0, 1), and for S ∈ Ω put
u_α(S) := e^{F(S)}/max(Z_𝒯, αẐ).

(a) *Deterministic.* On 𝒪: for every S ∈ Ω, π(S) ≤ e^{F(S)}/Z_𝒯. For every A ⊆ 𝒯, π(A) ≤ Σ_A e^{F}/Z_𝒯. For every
scored S ∈ 𝒯, π(S)/π(Ŝ) = e^{F(S)−F(Ŝ)} ≤ e^{−g}.

(b) *Probabilistic, simultaneous.* Let 𝔅_α := {∃S ∈ Ω : π(S) > u_α(S)} ∪ {∃A ⊆ 𝒯 : π(Ω ∖ A) < 1 − Σ_Ae^{F}/(αẐ)}.
Then 𝔅_α ∩ 𝒪_E = {Z < αẐ} ∩ 𝒪_E, and

  P(𝒪_E ∩ 𝔅_α) ≤ α·P(𝒜) ≤ α,  and, if P(𝒪_E) > 0,  P(𝔅_α | 𝒪_E) ≤ α·P(𝒜)/P(𝒪_E).

In particular, with probability at least 1 − α (output-level, unconditional): π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, αẐ), and the
posterior mass of the *unscored and unreported* models is at least 1 − Z_𝒯/(αẐ).

(c) *Non-implication (no lower bound from (H-T12)).* For no constants c > 0, γ > 0 does a bound
P(π(Ŝ) ≥ c·e^{F(Ŝ)}/Ẑ) ≥ γ follow from the properties of Ẑ used in (b) (positivity, finitely many values, E[Ẑ | 𝓒] = Z).

*Proof.*
(a) Z = Σ_{Ω} e^{F} ≥ Σ_{𝒯} e^{F} = Z_𝒯, because 𝒯 ⊆ Ω has distinct elements and every term is positive. Then
π(S) = e^{F(S)}/Z ≤ e^{F(S)}/Z_𝒯, and the same holds for sums over A. The ratio is exact because Z cancels, and the
inequality is the definition of g.

(b) The deterministic identity. π(S) > u_α(S) ⇔ Z < max(Z_𝒯, αẐ). By (a), Z ≥ Z_𝒯 surely, so this is ⇔ Z < αẐ. It
does not depend on S, so the union over all S ∈ Ω (Ŝ included, however it was selected) is {Z < αẐ}. Likewise
π(Ω ∖ A) = 1 − Σ_Ae^F/Z < 1 − Σ_Ae^F/(αẐ) ⇔ Z < αẐ (as Σ_Ae^F > 0). Hence 𝔅_α ∩ 𝒪_E = {Z < αẐ} ∩ 𝒪_E.

The probability bound. The evidence is reported only on 𝒜 ∩ 𝒢ᶜ, and under GUARD the reported Ẑ equals the R̄-value Ẑ̄
on 𝒢ᶜ. By Lemma RO(2), P(𝒪_E, Z < αẐ) ≤ P(𝒪̄_E, Z < αẐ̄) ≤ P(𝒜, Z < αẐ̄). By locked T31(i)(a) (with (H-T12) from locked
T12(iii)), P_c(Z < αẐ̄) ≤ α for every successful c. Integrate over 𝓒 on 𝒜 (CAL, EX-S: P_c is a version of the
conditional law given 𝓒) to get ≤ α·P(𝒜). The conditional form is the only conditional statement Lemma RO allows.

(c) The bound would be equivalent to P(Z ≤ Ẑ/c) ≥ γ. Locked T31(c) gives, for every c₀ > 0 and η, a law in 𝓛(Z)
with P(Ẑ < c₀Z) ≥ 1 − η. Take c₀ < c and η < γ: then P(Z ≤ Ẑ/c) ≤ P(Ẑ ≥ cZ) ≤ η < γ. ∎

*Remarks.*
- **Why "selection-proof" matters.** Ŝ, 𝒯 and Ẑ come from the same streams, so a bound proved for a *fixed* model
  could fail for the selected one. C1 avoids this because the bad event is a statement about Z alone.
- **Which direction is useful.** C1 certifies *uncertainty*. "u_{0.05}(Ŝ) = 0.03" is a rigorous finite-n statement
  that the reported model carries at most 3% posterior mass, so its posterior 0–1 risk (Prop 1) is ≥ 97%. A large
  u is uninformative.
- The lower bound on unscored mass is a finite-n *exploration* diagnostic: it is positive exactly when
  Z_𝒯 < αẐ, i.e. when the evidence estimate says the run has seen less than α of the posterior.

### Theorem C2 (two-sided band, conditional on PW2). PROVED (candidate), CONDITIONAL.
Under the hypotheses of C1, assume moreover PW2 with constants (a_t, ν_t) for each final island, as in locked
T25(iv), so that Var_c(Ẑ/Z) ≤ B_T/4. Then for ε ∈ (0, 1):

  P(𝒪_E, ∃S ∈ Ω : π(S) < (1 − ε)e^{F(S)}/Ẑ) ≤ E[1_𝒜·B_T/(B_T + 4ε²)],

and jointly with C1, π(S) ∈ [(1 − ε)e^{F(S)}/Ẑ, e^{F(S)}/max(Z_𝒯, αẐ)] for every S simultaneously, except on an event
of probability ≤ α·P(𝒜) + E[1_𝒜 B_T/(B_T + 4ε²)].
*Corollary (conditional global-HPM certificate).* On the good event, if (1 − ε)e^{F(Ŝ)}/Ẑ > ½, then π(Ŝ) > ½. So Ŝ is
the unique global HPM of π and the Bayes rule for exact recovery (Prop 1), and the event E_n of T20(ii) holds with S₀
replaced by Ŝ.

*Proof.* The event equals {Z > Ẑ/(1 − ε)} = {Ẑ/Z < 1 − ε}, uniformly in S, as in C1(b). Write W = Ẑ̄/Z, so
E_c W = 1 (T12(iii)) and Var_c W ≤ B_T/4 (T25(iv), pooled clause). Cantelli's one-sided inequality gives
P_c(W − 1 ≤ −ε) ≤ (B_T/4)/(B_T/4 + ε²) = B_T/(B_T + 4ε²). Lemma RO(2) transfers this to the output, and integrating
over 𝒜 gives the bound. The joint bound is a union bound. The corollary holds because Σ_{S≠Ŝ} π(S) < ½ < π(Ŝ). ∎

*Why this is not a data certificate.* PW2's constants a_t, ν_t are moments of the unknown particle law. Neither T13
(whose χ² bound concerns the *target* laws q_{φ_t} under COVER, and which explicitly does not derive particle mixing
from ESS) nor the empirical 4-island SD (T31(d2): conditioning on E2 not raised can push coverage below any γ)
supplies them. C2 is a *what-if* statement: "if the run's relative variance were at most v, then π(Ŝ) ≥ …".

### Theorem C3 (exact relative certificates on scored regions). PROVED.
Assume EX-A (or SC(η_F), with the stated changes). Let R ⊆ Ω be any finite region with Ŝ ∈ R whose scores are all
available (scored by the run, or recomputed post hoc from (X, y)). Then exactly
π(Ŝ | R) = e^{F(Ŝ)}/Σ_{S∈R} e^{F(S)}, and π(S)/π(Ŝ) = e^{F(S)−F(Ŝ)} for all S ∈ R. In particular:
- (a) **Local** (T20(i)). If `local_certified`, then F(S) ≤ F(Ŝ) for all S ∈ 𝒩(Ŝ). The local share
  ρ_loc := π(Ŝ | N̄(Ŝ)) and the type gaps
  - g_add := F(Ŝ) − max_j F(Ŝ ∪ {j}),
  - g_del := F(Ŝ) − max_i F(Ŝ ∖ {i}),
  - g_swap := F(Ŝ) − max_{i,j} F(Ŝ ∖ {i} ∪ {j})

  are exact. They need p + |Ŝ|(p − |Ŝ|) scores, the same as one scan.
- (b) **Subset class.** For the 2^{|Ŝ|} − 1 proper subsets of Ŝ, g_sub := F(Ŝ) − max_{S⊊Ŝ} F(S) and
  Σ_{S⊊Ŝ} π(S)/π(Ŝ) are exact (enumeration; 16,383 scores at |Ŝ| = 14).
- (c) **Best-of-scored.** For every S ∈ 𝒮̄ ∖ {Ŝ}, π(S) ≤ e^{−g}π(Ŝ) with g the top-store gap.

Under SC(η_F), each exact equality becomes a two-sided bound with factor e^{±2η_F}, and each certified inequality
F(S) ≤ F(Ŝ) needs the computed gap to be ≥ 2η_F.

*Proof.* Z cancels in every ratio, and π(Ŝ | R) = π(Ŝ)/π(R) = e^{F(Ŝ)}/Σ_Re^{F}. For (a), the meaning of
`local_certified` is locked T20(i): the returned model was a scanned centre with no strictly improving neighbour. ∎

*What these give the S₀-type alternatives (task item iii).* The study's misses are supersets at c = 1, and same-size
swaps and subsets at c = 0.5 (THEORY_PRIORITIES §5). If S₀ = Ŝ ∪ {j} or Ŝ ∖ {i}, or a one-swap of Ŝ, then S₀ ∈ N̄(Ŝ),
and the card's g_add, g_del, g_swap bound π(S₀)/π(Ŝ) exactly. If S₀ ⊊ Ŝ (a superset miss at any depth), (b) bounds it
exactly. In each case the bound is computable without knowing S₀, because it holds uniformly over the whole class.

### Theorem C4 (box certificate). PROVED.
Assume EX-A. For L ⊆ U ⊆ [p] with |L| ≤ K, and every S ∈ [L, U]:

  F(S) ≤ Φ(L, U),  and  Σ_{S∈[L,U]} e^{F(S)} ≤ e^{M(L, U)}.

Let 𝔗 be a finite family of boxes partitioning [∅, U] (for example the leaves of a binary tree in which a node [L, U′]
splits into [L ∪ {j}, U′] and [L, U′ ∖ {j}] for some j ∈ U′ ∖ L). Then:
- (a) *Optimality.* If every leaf [L, U′] ∈ 𝔗 satisfies Φ(L, U′) ≤ F(Ŝ), or is a singleton {S} with F(S) ≤ F(Ŝ),
  then F(Ŝ) = max_{S∈[∅,U]} F(S) (when Ŝ ⊆ U). Equivalently, π(S) ≤ π(Ŝ) for all 2^{|U|} supports S ⊆ U with |S| ≤ K.
- (b) *Conditional mass.* With Ŝ ⊆ U, π(Ŝ | [∅, U]) ≥ (1 + Σ_{leaves ≠ {Ŝ}} e^{M(leaf) − F(Ŝ)})⁻¹, where a
  singleton leaf {S} contributes e^{F(S)−F(Ŝ)}.
- (c) *Refutation.* If some S ∈ [∅, U] evaluated in the tree has F(S) > F(Ŝ), then Ŝ is not the HPM of π. If moreover
  S ∉ 𝒮̄, the run made a **search miss** relative to S. The certificate is constructive.

Under SC(η_F), replace F(Ŝ) by F(Ŝ) − 2η_F in (a).

*Proof.* Let S ∈ [L, U] with |S| = k. Then |L| ≤ k ≤ K, so Lemma M(c) gives w(k) ≤ w(|L|). L ⊆ S gives D_S ≥ D_L
(Lemma M(b)), and S ⊆ U gives Q_S ≥ Q_U (Lemma M(a)). Since t ↦ −ν log(2b₀ + t) is decreasing, every term of F(S)
is bounded by the corresponding term of Φ(L, U). For the mass bound, [L, U] has at most C(|U|−|L|, k−|L|) members of
size k. Each has e^{F(S)} ≤ (w(k)/W_K)·C_n·D_L^{−1/2}(2b₀ + Q_U)^{−ν}, by the same two monotonicities with the exact
w(k). Summing over k gives e^{M}. The split rule partitions [L, U′], because every S in it either contains j or does
not. So the leaves partition [∅, U] ∩ Ω, and (a)–(b) follow by taking the maximum and the sum over leaves. (c) is
immediate. ∎

*Remarks.*
- C4 needs only (X, y, Ŝ), not the run. It can certify **any** reported model, including SuSiE's or SSL's, and is
  valid for every choice of U, including a data-dependent one. So there is no selection or multiplicity issue.
- **Cost.** The bound is loose at the root, where the prior factor w(|L|) is evaluated at |L| = 0. Pruning happens
  once L has absorbed the decisive variables. So the tree's size grows like 2^{(number of ambiguous variables in U)},
  not 2^{|U|}. Measured sizes are in §4.

### Corollary C5 (posterior-miss certificate). PROVED.
In the setting of C4(a), on the event {S₀ ⊆ U}: Ŝ ≠ S₀ implies F(S₀) ≤ F(Ŝ). So the miss is a **posterior** miss in
the classification of THEORY_PRIORITIES §5, and by Prop 1 it cannot be repaired by any search, and (for same-size
S₀) by no size-only prior. Hence, for every data-measurable rule U = U(X, y, Ŝ),

  P(𝒪, Ŝ ≠ S₀, F(S₀) > F(Ŝ)) ≤ P(𝒪, C4(a) fails for U) + P(𝒪, S₀ ⊄ U).

*Proof.* Immediate from C4(a). ∎ The last term is a screening probability. It is the only place where statistics (and
hence asymptotics) re-enters. At n = 200 it is measured, not proved, in §4.

### Theorem C6 (the per-fit certificate card). PROVED (candidate).
The **card** of a fit with output is the list of claims:
- **L (local, deterministic):** `local_certified` ⇒ F(S) ≤ F(Ŝ) on 𝒩(Ŝ); the exact values g_add, g_del, g_swap,
  ρ_loc (C3(a)); g_sub and the subset ratio (C3(b)); the best-of-scored gap g (C3(c)).
- **R (region, deterministic):** for the reported U, "Ŝ = argmax_{[∅,U]} F" and π(Ŝ | [∅, U]) ≥ ρ_U (C4), or a
  refutation (C4(c)).
- **G (global, one-sided, level α):** π(Ŝ) ≤ u_α(Ŝ) = e^{F(Ŝ)}/max(Z_𝒯, αẐ); π(S) ≤ u_α(S) for every model; the
  unscored mass is ≥ 1 − Z_𝒯/(αẐ) (C1).
- **C (conditional, flagged as such):** the C2 band for a stated hypothetical B_T. It is not counted as certified.

Under EX-A, EX-S, CAL, START and GUARD:

  P(𝒪 and some L, R or G claim on the card is false) ≤ α·P(𝒜) ≤ α,

for every n, p and data set, with no asymptotics, and without conditioning on completion. Given completion, only the
bound α·P(𝒜)/P(𝒪) is claimed. Under VAL-FP(η, ε) and SC(η_F), with the L and R claims checked at margin 2η_F, the bound
becomes α·e^{η} + ε.

*Proof.* The L and R claims are deterministic functions of (X, y, Ŝ, 𝒯), true surely on 𝒪 under EX-A (C3, C4).
Under SC(η_F), every computed inequality with margin ≥ 2η_F implies the exact one. The G claims fail exactly on
{Z < αẐ} (C1(b)), whose output-level probability is ≤ α·P(𝒜). With floating point, VAL-FP gives
P(𝒪_E, Z < αẐ^{fp}) ≤ P(𝒪_E, Z < αe^{η}Ẑ̄) + ε ≤ αe^{η} + ε, by W2-BOOK Prop 2(f). ∎

*What the card does **not** say.*
- It does not say that π(Ŝ) is large. That needs C2 (PW2) or enumeration.
- It does not say Ŝ = S₀. That needs Thm 1 (asymptotic) and the screening term of C5.
- It does not say that the global HPM was found. That needs [∅, U] = Ω, impossible at p = 500.

The paper sentence: "*Each fit reports a certificate card whose claims hold simultaneously with probability at least
95%, at the actual n, whether or not the run completes.*"

## 4. Illustration (p = 500, n = 200, production engine)

**Setup.** Four production datasets regenerated bit-for-bit with the study generator
(`scripts/gen_data.R`, which calls `Scripts/Data_generators/gen_prod_data.R` with its own seeds): S1 and S3 (r001) at
c = 1, and S4 and S6 (r001) at c = 0.5. Each was fitted with the production v3 engine (`scripts/run_fit.R`, the study
method seed, single-threaded, on Felipe's laptop under Windows/R 4.4.1). The fits took 43–83 min, and all four have
status `completed`. The cards were computed post hoc by `scripts/cert_run.R`, which uses an independent R
implementation of F (`scripts/cert_lib.R`), the reported top store (|𝒯| = 20,001), and U = Ŝ ∪ {the 16 best single
additions}. The full output is in `results/cards.txt`. The truth S₀ is used **only** for the "outcome" row. The card
itself never uses it.

| | S1 c100 | S3 c100 | S4 c050 | S6 c050 |
|---|---|---|---|---|
| outcome (uses S₀) | Ŝ = S₀ | Ŝ = S₀ | Ŝ = S₀ + 1 FP | Ŝ = S₀ + 1 FP |
| score agreement, mine − engine (top 5) | ≤ 1.2e−12 | ≤ 2.8e−12 | ≤ 1.2e−12 | ≤ 8.5e−13 |
| **L** `local_certified` (engine / recomputed) | T / T | T / T | T / T | T / T |
| **L** g_add / g_del / g_swap (nats) | 2.27 / 36.0 / 38.5 | 2.91 / 34.5 / 20.1 | 0.53 / 1.19 / 2.01 | 2.77 / 1.89 / 1.51 |
| **L** exact ρ_loc = π(Ŝ \| N̄(Ŝ)) | 0.459 | 0.460 | 0.211 | 0.264 |
| **L** g_sub; Σ_{S⊊Ŝ} π(S)/π(Ŝ) | 36.0; 2.6e−16 | 34.5; 1.1e−15 | 1.19; 0.305 | 1.89; 0.345 |
| **L** best-of-scored gap g; e^{−g} | 2.27; 0.103 | 2.91; 0.054 | 0.53; 0.590 | 1.51; 0.220 |
| **R** Ŝ = argmax over 2^U (\|U\|, B&B nodes, time) | yes (30, 3,831, 0.8 s) | yes (30, 1,963, 5 s) | yes (31, 9,665, 5 s) | yes (31, 77,083, 38 s) |
| **R** π(Ŝ \| 2^U) ≥ (mass B&B, τ = −12) | 0.698 | 0.728 | 0.278 | not finished (2·10⁵ nodes) |
| log Z_𝒯 vs log(0.05 Ẑ) | −69.80 vs −72.59 | −72.30 vs −75.12 | −180.30 vs −182.70 | −206.97 vs −209.41 |
| **G** π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, 0.05Ẑ) | 0.370 | 0.375 | 0.103 | 0.153 |
| (plug-in e^{F(Ŝ)}/Ẑ, not a certificate) | 0.301 | 0.315 | 0.057 | 0.088 |
| **C** under PW2, B_T = 0.25: π(Ŝ) ≥ 0.5e^{F}/Ẑ except w.p. ≤ 0.2 | 0.150 | 0.157 | 0.029 | 0.044 |
| F(S₀) − F(Ŝ) (uses S₀) | 0 | 0 | −1.19 | −1.89 |

**What the illustration shows.**
1. **The score contract holds to ~10⁻¹² nats.** Two independent implementations (the engine's C++ and my R) agree
   to within 3·10⁻¹² nats on every top-store score checked. This is a cross-implementation check, not a
   high-precision replay, but it makes SC(η_F) with η_F = 10⁻⁹ comfortable. Every certified gap above is ≥ 0.5 nats,
   about 10⁹ times the margin 2η_F.
2. **The global claim was deterministic on every fit.** Z_𝒯 > 0.05Ẑ in all four cases, by 2.4–3.0 nats: the
   reported top store already contains more than 5% of the estimated evidence. So max(Z_𝒯, αẐ) = Z_𝒯, and the G bound
   π(Ŝ) ≤ e^{F(Ŝ)}/Z_𝒯 holds **surely** (C1(a)), with no probability at all. The Markov factor of T12/T31 adds nothing
   at α = 0.05 here. It would become active only for a run whose top store sees less than 5% of Ẑ, the
   exploration-failure case, which is exactly when the "unscored mass ≥ 1 − Z_𝒯/(αẐ)" line becomes non-vacuous.
   Here that line is 0 on all four fits.
3. **Even a correct fit carries little posterior mass at n = 200.** At c = 1, Ŝ = S₀, and yet π(Ŝ) ≤ 0.37 surely.
   The binding alternatives are supersets (g_add = 2.3–2.9 nats ≪ g_del, g_swap ≈ 20–38 nats). This is the
   finite-n face of the "superset misses at c = 1" finding (THEORY_PRIORITIES §5): exact recovery is the posterior
   mode, but not with posterior probability ½. No certificate can say π(Ŝ) ≥ ½, and here even the truth fails it.
4. **The two c = 0.5 misses are certified posterior misses.** In both, S₀ = Ŝ ∖ {FP} is a one-deletion of Ŝ. The
   card's g_del (1.19 and 1.89 nats) is exactly F(Ŝ) − F(S₀), so π(S₀) ≤ e^{−g_del}π(Ŝ) = 0.30π(Ŝ) and 0.15π(Ŝ)
   respectively. The box certificate independently confirms that S₀ ∈ 2^U and that Ŝ = argmax over 2^U (C5). Both
   are posterior misses: no amount of extra search would have returned S₀. The card certifies this **without
   knowing S₀**, because it bounds every model in N̄(Ŝ) and in 2^U uniformly. A reader who suspects that "the truth is
   Ŝ minus one variable" is told by the card that every such model has posterior ratio ≤ e^{−1.19}.
5. **The box certificate is cheap.** The optimality B&B over 2^U with |U| = 30–31 (10⁹ models) closed in
   2·10³–8·10⁴ nodes and at most 38 s, consistent with the "2^{#ambiguous variables}" remark under C4. The mass
   version is costlier (it must bound the whole tail to e^{−12}). It closed on three of the four fits, with
   π(Ŝ | 2^U) ≥ 0.70, 0.73 and 0.28. Note that π(Ŝ | 2^U) ≥ 0.70 > 0.37 ≥ π(Ŝ) is not a contradiction. Conditioning on 2^U
   removes at least 1 − 0.37/0.70 ≈ 47% of the mass of the models that compete with Ŝ (for example, supersets that
   add a variable outside U).
6. **Ẑ's island spread is small (SD of log Ẑ_r 0.02–0.08), but is not used.** By T31(d2), conditioning on a
   small spread can destroy coverage. The C row is printed only as a what-if.

**Not done.** I did not run larger studies, other replicates, or p = 1000. Nor did I enlarge the mass B&B budget for
S6. Four fits are an illustration, not evidence about frequencies.

## 5. What fails and why
- **A lower bound on π(Ŝ) from Ẑ alone.** It is impossible (C1(c)). The Markov direction is fixed: unbiased
  non-negative estimators only give lower bounds on Z, hence upper bounds on every posterior probability.
- **Making it two-sided with the 4-island spread or the empirical ESS.** This fails. T31(d2) and T12(iv.e) show that
  conditioning on a favourable spread can destroy coverage. Empirical ESS is a function of the same streams and
  carries no moment guarantee.
- **T13 restricted ESS.** Its identity concerns the target laws q_φ. It bounds the PW2 constant a_t only in the
  perfect-mixing idealisation, which is exactly PW2. So it cannot replace PW2 as a data certificate.
- **Using islandwise E[Ẑ_r q̂_r(1_{S})] = Zπ(S) to lower-bound π(Ŝ).** It fails twice. Markov again gives only lower
  bounds on Zπ(S), and S = Ŝ is selected from the same streams (T12(i.d)-type failure). Using a calibration-stage
  candidate S_cal ∈ σ(𝓒) repairs the selection, but not the direction.
- **A global box certificate.** Q_{[p]} ≈ yᵀy/(n + 1) when p > n, so Φ(∅, [p]) is astronomically large. Boxes must be
  restricted to a universe U with Q_U bounded away from 0, i.e. |U| ≪ n.

## 6. Needs escalation
- C1 and C6 rely on Lemma RO and GUARD (W2-BOOK, unreviewed). A cross-family check of the output-level step is needed.
- Lemma M is short, but it is the engine of C4. Ask a reviewer to check (b), the determinant monotonicity, and to
  confirm that the engine's Q (with its non-negative recomputation branch, M §6.13) is the same function.
- SC(η_F): the engine and an independent R implementation agree to 3·10⁻¹² nats (§4). A replay in long double or
  mpfr is still needed to fix η_F for the paper, because two double implementations can share a rounding pattern.

## 7. Outside scope
- C4 is a *method-agnostic* post-hoc certificate. Applied to SuSiE, SSL or lasso supports, it would let the paper say
  rigorously "on data set i, the competitor's support is beaten by an explicit model under the working posterior",
  which is a fair, finite-n comparison of *posterior* optimality (not of recovery).
- C4(c) gives a cheap search-miss detector that the engine could run after the local search (a "box scan" around Ŝ).
  That would be a method change, so it falls under the investment rule.

## 8. Confidence card

| Item | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| Lemma M | Q_S ↓ and D_S ↑ in S (Loewner / determinant-lemma) | high | done (PROVED, 1 page) | (b): h(c) = 1 + c xᵀ(I+cM)⁻¹x is non-decreasing | no |
| C1 | π(S) ≤ e^{F(S)}/max(Z_𝒯, αẐ) for all S simultaneously, output level ≤ αP(𝒜) | high | done (corollary of locked T12/T31 + Lemma RO) | the bad event is {Z < αẐ}, free of S, so selection is harmless | no |
| C1(c) | no lower bound on π(Ŝ) from unbiasedness | high | done (from locked T31(c)) | — | no |
| C2 | two-sided band under PW2 via Cantelli | high (as an implication) | done; **useful only if PW2 is proved**, which is open | PW2 constants are not data-checkable | no |
| C3 | exact π(Ŝ \| R) on fully scored R; local/subset/best-of-scored gaps | high | done (trivial, but it is the only exact posterior statement at n = 200) | — | no (post-hoc rescoring, about 7k + 16k scores) |
| C4/C5 | box certificate: Ŝ = argmax over 2^U and π(Ŝ \| 2^U) ≥ ρ_U; posterior-miss certificate on {S₀ ⊆ U} | high | done; cost is empirical (§4) | tree size ~ 2^{# ambiguous variables}; P(S₀ ⊄ U) is statistical | no for post-hoc; yes if built into the engine |
| C6 | the card's L/R/G claims hold jointly w.p. ≥ 1 − αP(𝒜) at every n, no completion conditioning | high | done (candidate), modulo W2-BOOK review of Lemma RO/GUARD | VAL-FP and SC(η_F) must be measured by replay | no |
| "π(Ŝ) ≥ ½ certified" | — | — | **not possible** without PW2 or enumeration (C1(c)) | — | would need a variance-controlled estimator |

Overall: the certificate programme gives the paper a rigorous **finite-n, per-fit** layer. It says "Ŝ is optimal on an
explicit, large region", "Ŝ is a posterior miss, not a search miss, whenever S₀ ⊆ U", and "π(Ŝ) ≤ u". It cannot turn
any of this into "Ŝ is probably right", and the paper should say so.
