# W2-VT24G — PROOF.md: repairs and additions to W1-T24G

Everything here is a candidate. Nothing has been reviewed. Notation: W1-T24G PROOF.md §0, which uses
`00_COMMON.md`. Labels Λ = 𝔊 ∪ 𝔑 with |𝔑| = B + 2. "Step t" is the t-th elementary step of a round. X_{t−1} is
the state just before step t. σ is the round's label order, and 𝓕_t is the σ-algebra after step t.

---------------------------------------------------------------------------------------------------------

## 1. Lemma F′: union-bound form of Lemma F. PROVED

**Why this is needed (GAP in W1).** W1's Lemma F assumes that "a non-failing step from 𝓕 stays in 𝓕". Two of
its uses do not satisfy this hypothesis.

1. **Prop. B2, slot step.** The family is {W ∈ 𝒮_a : l ∈ W}. Several non-failing steps leave it: a G_l deletion,
   a neutral removal of l after G_l, and any bad step.
2. **Theorem B, part (a).** A non-bad step can reach S₀. From S₀ a further step can be bad, and S₀ is not in
   the family 𝓕∖{S₀} over which the sup is taken. W1 handles this by stopping at scoring, but Lemma F as stated
   does not include stopping.

Both conclusions are still true. The lemma below proves them without the closure hypothesis.

**Lemma F′.** Fix a round. Let 𝓕 ⊆ Ω be any set. For each label e, let f_e(W; σ) ∈ [0,1] be the conditional
probability that a step with label e, executed at state W, is a "failure". The failure rule may depend on σ.
Then

  P(∃t : X_{t−1} ∈ 𝓕 and step t fails) ≤ Σ_{e∈Λ} E[ sup_{W∈𝓕} f_e(W; σ) ].

If f_e does not depend on σ, the right side is Σ_e sup_{W∈𝓕} f_e(W).

*Proof.* Step t uses fresh randomness, and σ is 𝓕₀-measurable (R1). So
P(step t fails | 𝓕_{t−1}) = f_{σ(t)}(X_{t−1}; σ). The union bound and the tower property give

  P(∪_t {X_{t−1}∈𝓕, step t fails}) ≤ Σ_t E[1{X_{t−1}∈𝓕} f_{σ(t)}(X_{t−1};σ)]
                                    ≤ E[Σ_t sup_{W∈𝓕} f_{σ(t)}(W;σ)].

Since σ is a bijection of the steps onto Λ (R2), Σ_t sup_W f_{σ(t)}(W;σ) = Σ_e sup_W f_e(W;σ). ∎

Lemma F is the special case in which non-failing steps stay in 𝓕. In that case "some step fails" equals the
event on the left.

**Repair of Theorem B, part (a).** Take 𝓕 = 𝓕(x)∖{S₀} and failure = bad. Before S₀ is first scored, every
bad step is taken from a state in 𝓕(x)∖{S₀}:
- a visit to S₀ scores S₀ (R3);
- before the first bad step the state stays in 𝓕(x).

So {some bad step before scoring} ⊆ {∃t : X_{t−1} ∈ 𝓕(x)∖{S₀}, step t bad}. Lemma F′ bounds this by
Σ_e sup_{𝒵⁺ ∪ 𝒮_a°} P_W(e bad) ≤ η₁ + η₂, and the rest of the proof is unchanged.

**Repair of Prop. B2, slot step.** Work on {no bad, no progress}. Suppose l ∈ P(W) is absent when G_l
executes. Then some step t with σ(t) ≺ G_l neutrally removed l from a state X_{t−1} ∈ 𝒮_a° that contains l.
Apply Lemma F′ with:
- 𝓕 = {W′ ∈ 𝒮_a : l ∈ W′};
- f_e(W′;σ) = 1{e ≺ G_l}·P_{W′}(e's step is neutral and removes l), for e ∈ 𝔑, and f_e = 0 for e ∈ 𝔊.
  Gibbs labels other than G_l never remove l, and a removal by G_l itself is progress.

This gives the bound Σ_{e∈𝔑} P(e ≺ G_l) sup_{W′} P_{W′}(·) = h(l), by Lemma O(ii). ∎

**Status of W1's Theorem B, Prop. B2 and Prop. D after the repair.** PROVED (candidate; checked line by line,
see REPORT §3). Prop. D's exit term (Lemma F with failure = exit) needs no change: a non-exit step stays in
𝓕(x) by definition.

---------------------------------------------------------------------------------------------------------

## 2. Prop. B2′ and B1′: the scoring sharpening. PROVED

**Definitions.**
- ε′_del(a) := sup{ o_l(W) : W ∈ 𝒮_a°, |P(W)| ≥ 2, l ∈ P(W) }. Set ε′_del(1) := 0.
- c′₂ := 1 − ε′_del(a) − H_a.
- ε′_add(x) is ε_add(x) with the inner sup restricted to W′ ≠ S₀∖{j}. That is, the distance-one state
  W′ = S₀∖{j} is removed from the sup for that j.
- c′₁ := 1 − ε′_add(x).

**Prop. B2′.** For W ∈ 𝒮_a°: P_W(no bad and no progress step in the round) ≤ ε′_del(a) + H_a.

*Proof.* On {no bad, no progress}, |P| stays equal to |P(W)| and every state is in 𝒮_a° (W1 Prop. B2).

- **Case |P(W)| ≥ 2.** This is W1's proof verbatim. The sup in ε_del can be restricted to states with
  |P| = |P(W)| ≥ 2, because every state at which a G_l step acts on this event has that size.
- **Case |P(W)| = 1.** Every state on the event has the form S₀ ∪ {l′}.
  - Slot bound: if G_l executes at a state that contains l, that state is S₀ ∪ {l}. Its G_l evaluation scores
    S₀ whatever the draw (R4, SR), so the step is progress. The event therefore needs l to be removed before
    G_l. By §1 that has probability ≤ h(l).
  - Order bound: suppose the first label of C ∪ 𝔑 (with C = {G_l}) is G_l. Then G_l acts at W = S₀ ∪ {l}, and
    this is progress with probability 1.

  So the bound is min{h(l), (B+2)/(B+3)} ≤ H_a, with no ε_del term. ∎

**Prop. B1′.** For W ∈ 𝒵⁺: P_W(no bad and no progress) ≤ ε′_add(x).

*Proof.* Follow W1 Prop. B1. At the G_j step, if the state is W′ = S₀∖{j}, the evaluation scores S₀ (R4), so
the step is progress whatever the draw. Otherwise the conditional failure probability is 1 − o_j(W′), and this
is at most the restricted sup. ∎

**Theorem B′.** Theorem B holds with c₁, c₂ replaced by c′₁ ≥ c₁ and c′₂ ≥ c₂. In particular:
- for a = 1 (the start S₀ ∪ {l}, or any start whose phase-2 family is 𝒮₁), c′₂ = 1 − H₁ ≥ 1/(B+3) with no
  statistical premise at all;
- for x = S₀∖{j}, A = ∅ and c = 0, c′₁ = 1.

*Proof.* Theorem B's proof uses B1 and B2 only through these two bounds. ∎

**Numerical check** (`scripts/b2_check.py`, `results/b2_check.json`; p = 20, n = 200, a = 1, all 12 cells).
- c₂ (W1's definition), recomputed from my own laws, reproduces W1's Table T4a values exactly: 0.326, 0.343,
  0.427, 0.423, 0.460, 0.458, 0.469, 0.468, 0.459, 0.457, 0.435, 0.431.
- c′₂ = 0.43–0.50.
- The simulated P_W(no exit and not scored) is ≤ 0.094 in every cell. That is below both bounds, as B2 and B2′
  require: for a = 1, bad equals exit from 𝒮₁.

---------------------------------------------------------------------------------------------------------

## 3. Lemma E: a deterministic exit lower bound for H24. PROVED

This turns W1's CE1 asymptotic sketch into a deterministic inequality plus two named statistical limits.

**Lemma E.** Let Y ∈ 𝓡_d with |P(Y)| = d and m := |M(Y)| ≥ 1. Write:
- Q_T(Y) := Σ_{i∈Y∩S₀} (1 − o_i(Y)), the total deletion probability of the truths present;
- o*(Y) := max_{l ∉ Y∪S₀} o_l(Y), the best null-addition probability.

Then

  P_Y(some elementary state of the next round lies outside 𝓡_d) ≥ o*(Y) · [1 − Q_T(Y)/(B+m+d+4)] / (B+m+d+3).

With one missing truth (m = 1), the denominators are B+d+5 and B+d+4.

*Proof.* Realise σ by iid U(0,1) arrival times T_e. Give each label an independent outcome Y_e ~ K_e(Y,·). The
round agrees with the outcomes Y_e up to and including its first state change (W1 Lemma P coupling).

Let C be the set of Gibbs labels of nulls l ∉ Y ∪ S₀. Since |P(Y)| = d, any change caused by a label in C is
an addition of a null, and therefore an exit.

Let D := 𝔑 ∪ {G_j : j ∈ M(Y)} ∪ {G_q : q ∈ P(Y)}, so |D| = B + 2 + m + d. Let T be the Gibbs labels of the truths in Y, and
put l* = argmax o_l(Y).

Consider the event that Y_{G_{l*}} is an addition and that no label of D ∪ T changes the state before
T_{G_{l*}}. On this event the first state change is caused either by a label in C (an exit), or by G_{l*} itself
acting at Y (also an exit). By Lemma O(iii), its probability is

  o*(Y) ∫₀¹ ∏_{e∈D}(1 − t q_e) ∏_{i∈T}(1 − t(1−o_i(Y))) dt ≥ o*(Y) ∫₀¹ (1−t)^{|D|}(1 − tQ_T) dt.

The inequality uses q_e ≤ 1 and the Weierstrass product inequality. The integral equals
[1 − Q_T/(|D|+2)]/(|D|+1). ∎

**Consequence (CE1, asymptotic form).** Suppose there is a design sequence and boundary states Y_n ∈ 𝓡_d with
o*(Y_n) → 1 and Q_T(Y_n) → 0 in P₀-probability, each Y_n missing exactly one truth (m = 1). Then the uniform
one-round exit bound η_n of H24 satisfies η_n ≥ (1 − o_P(1))/(B+d+4) ≥ (1 − o_P(1))/(d+20). Hence (L+4)η_n → ∞ in probability, and H24's asymptotic input
fails. The two limits are the statistical content:
- o*(Y_n) → 1: a look-alike of a missing truth is attractive. This holds under BM-∞ when a null has a fixed
  correlation r₀ with a missing truth j.
- Q_T(Y_n) → 0: retention of the truths in Y. This holds when there is no cancellation between j and the truths
  in Y, for example one truth per block in a block design.

These two limits are PROOF SKETCH; they are standard Bayes-factor asymptotics, but I have not written them out.

**Numerics.**
- `scripts/ce1_recheck.py`: the exact first-change lower bound P*_exit, which Lemma E bounds from below, is
  ≥ 0.39 in every S2–S6 cell at n = 200.
- `scripts/ce1_scaling.py`: the exit probability does not decrease with n (S2: 0.77 → 0.96 from n = 200 to
  3200; S3: 0.85–0.95 → 0.98).

---------------------------------------------------------------------------------------------------------

## 4. Correction to W1 PROOF.md §6, the NL0(a) row. The W1 sketch contains an ERROR

W1 states: "Equicorrelated nulls (S5, r = 0.3) give inflation ≈ 1.86 in Z², so NL0(1) fails in rate once
p ≳ n^{0.58}". The value 1.86 = (1+r)/(1−r) is what one would get if Z_l and Z_{l′} could take opposite extreme
values ±√(2 log p) independently. For an equicorrelated Gaussian family, Z_l = √r W + √(1−r) ξ_l, so

  max_{l≠l′} (Z_l − rZ_{l′})²/(1−r²) = (1+r)·2 log p·(1 + o_P(1)).

The common factor W enters only at O_P(1). The inflation is therefore 1 + r = 1.3, not 1.86. Numerically
(`scripts/nl0_inflation.py`), the median ratio is 1.08, 1.16, 1.19, 1.19, 1.21 for p = 10², …, 10⁶, slowly
approaching 1.3.

The superset leakage odds are then ≈ k p^{r}/(2√n) up to polylog factors. So NL0(1) fails in rate only when
p ≫ n^{1/(2r)} = n^{5/3} at r = 0.3. Under R (p ≤ n^A) this is inside the scope only when A > 5/3.

Status: the conclusion "NL0(1) can fail in rate for equicorrelated nulls" survives, but its threshold changes
from p ≳ n^{0.58} to p ≳ n^{5/3}. The row is still PROOF SKETCH.

---------------------------------------------------------------------------------------------------------

## 5. A structural limit of Theorem B at production size (observation, PROVED)

P(Bin(H, c) < v) = 1 whenever v > H. In Prop. D, ρ(z) ≥ z⁻¹ (the other two terms are ≥ 0), so
ρ(z)^H z^{v−1} ≥ z^{v−1−H} ≥ 1 whenever v ≥ H + 1. So Theorem B, B′, B-unif, B-M (per particle) and Prop. D all
give nothing for a start x with v(x) > H, whatever the constants c_* and η are.

At production size H = L + 4 = 12 (n = 200), and v(x) = |M(x)| + |A(x)| + c(x) for incomplete starts.
- The look-alike set A(x) contains every neighbour-graph partner of every missing truth, up to B = 14 per truth
  before the symmetric union.
- So a start missing two truths in S3–S6-type blocks of 5 already has v ≥ 2 + 8 = 10, and any extra junk pushes
  it towards H.
- Measured at p = 20 (B = 4) on raw π₀ draws (`results/p1_repair.json`): in S5 at c = 0.5, 10% of draws have
  v > 12.

The one-correct-step-per-round credit is the cause. A single real round deletes all extras (each G_l acts once),
but the proof credits one unit of V per round. W1's Prop. A (whole repair in one round) is the only tool that
credits several steps per round, and it is numerically vacuous. **OPEN:** a multi-step-per-round progress bound
that is not vacuous.
