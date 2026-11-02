# W6-FIXREV1 — CONSOLIDATED.md: the corrected Theorem B / premise / D2 / E3 package after A-REV1

Run W6-FIXREV1, 2026-11-02, branch `theory/W6-FIXREV1`. Everything here is a **candidate**: not reviewed by another
model family after these edits, and not adopted. Notation: `Docs/Theory/theorems/00_COMMON.md`, and W1-T24G
`PROOF.md` §0 (cited [B]); W2-VT24G (cited [V]); W2-PREM (cited [PREM]); W1-T38E (cited [T38E]); W3-VT38E (cited
[VT38E]); A-REV1 `REVIEW.md` (cited [AR]). Scripts are in `scripts/`, outputs in `results/`.

The T38 statement and proof are in `T38_STATEMENT.md` and `T38_PROOF.md`. This file holds every *other* corrected item.
Each section says what changed, gives the corrected statement in full, and gives the proof of anything new.

Status words: PROVED (complete, checked line by line by this run), PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN.
"PROVED" here never means reviewed or adopted.

---------------------------------------------------------------------------------------------------------

## 1. Proposition U, corrected (replaces [B] §3)

### 1.1 What was wrong ([AR] §3.1; I agree)

[B] §0 defines a step W → W′ (W ∈ 𝓕(x)∖{S₀}) as **bad** if (T1) W′ ∉ 𝓕(x), or (T2) V(W′) > V(W), or (T3) W′ ⊉ W ∩ S₀.
[B] §3 (Prop. U) then makes two shortcut claims that are false:

- (U-a) "an independence acceptance is bad **iff** it lands outside 𝓕(x) or raises V". This drops (T3).
- (U-b) "an extra-for-extra swap is **neutral** (|P| unchanged)". This is false at phase-1 states, where the swap can
  leave 𝒵(x).

**COUNTEREXAMPLE to (U-a)** (A-REV1's construction, re-evaluated here with the actual φ = 1 kernels,
`scripts/propU_check.py`, `results/propU_check.json`). S₀ = {1,2}, x = ∅, A = ∅ (allowed: [B] §0 lets A be any
data-measurable set), so c = a = 0 and 𝒵(x) = 2^{S₀}. At W = {1} the independence draw W′ = {2} stays in 𝒵(x) and has
V(W′) = V(W) = 1, but it removes truth 1. Its probability is π₀({2})·(1 ∧ e^{d({2})−d({1})}) > 0. On a p = 4, n = 40
instance with a weak truth 1 and a strong truth 2 (configuration 1b), this single transition has probability 0.826.
The independence contribution to η₁ is 0.945 with the full definition but only 0.119 with the shortcut.

**COUNTEREXAMPLE to (U-b)** (A-REV1's construction, same script). S₀ = {1}, x = ∅, A = {2} (a look-alike of 1),
variable 3 junk, so c = 0 and a = 1. At W = {2} the uniform swap 2 → 3 keeps |P| and V, but {3} ∉ 𝒵(x) (its junk count is
1 > c = 0) and {3} ∉ 𝒮₁, so the step is bad by (T1). Its probability on the instance is 0.091. The uniform-swap
contribution to η₁ is 0.112 with the full definition and 0 with the shortcut.

### 1.2 Corrected statement

**Proposition U′. PROVED (each item is a direct check of [B] §0).** Fix x, the family 𝓕(x) = 𝒵(x) ∪ 𝒮_a of [B] §0 (or
𝓕♯(x) = 𝒵♯(x) ∪ 𝒮_a of [PREM] §5.2), and the potential V. For W ∈ 𝓕(x)∖{S₀} let

  Bad(W) := {W′ ∈ Ω : W′ ∉ 𝓕(x)} ∪ {W′ ∈ 𝓕(x) : V(W′) > V(W)} ∪ {W′ ∈ Ω : W′ ⊉ W ∩ S₀}.

For **every** label e, a step is bad iff its end state lies in Bad(W).

- (i) A Gibbs step cannot be undone by Gibbs within the same round, because each label executes once ([B] (R2)).
- (ii) A non-Gibbs move can undo a correct step: U or N_i can remove a just-added truth, or re-introduce a just-deleted
  extra, and I can jump anywhere.
- (iii) **Charging.**
  - (iii-1) **Truth removal by any label is bad**, by (T3). This includes truth-for-truth swaps and independence jumps
    that keep |M| but change the missing set.
  - (iii-2) **Extra-for-extra swaps.** Let k ∈ P(W) and l ∉ S₀ ∪ W, and W′ = W − k + l. Then V(W′) = V(W) and W′ keeps
    every truth. So the step is neutral iff W′ ∈ 𝓕(x), and bad otherwise. Precisely:
    - at a phase-2 state W ∈ 𝒮_a, always W′ ∈ 𝒮_a (|P| is unchanged and ≤ a): **neutral**;
    - at a phase-1 state W ∈ 𝒵(x), with look-alike set A and junk set J = S₀ᶜ∖A, W′ ∉ 𝒵(x) **iff k ∈ A, l ∈ J and
      |W ∩ J| = c** (a look-alike replaced by junk when the junk budget is full); otherwise neutral;
    - at a phase-1 state W ∈ 𝒵♯(x), with current look-alikes 𝔄(M(W)), W′ ∉ 𝒵♯(x) iff k ∈ 𝔄(M(W)), l ∉ 𝔄(M(W)) and the
      current-junk budget c + |𝔄(M(x))∖𝔄(M(W))| is full.
    A neutral extra-for-extra swap cannot undo V-progress. In phase 2 it can only hide a slot (replace a not-yet-processed
    extra by a processed null); that cost is carried inside c₂ through h(l) ([B] §4, B2), not through η.
  - (iii-3) **Independence.** The independence step at W is bad iff its *accepted* draw S′ lies in Bad(W). Its
    contribution to η is
      β_I(W) := Σ_{S′∈Bad(W)} π₀(S′)(1 ∧ e^{d(S′)−d(W)}) ≤ min{ π₀(Bad(W)), [π₀(W)/π(W)]·π(Bad(W)) }.
  - (iii-4) Every other move is classified by the same three tests. Nothing else is added to the classification.

*Proof of (iii-2), phase 1, family 𝒵(x).* W = U ∪ P ∪ Q with x∩S₀ ⊆ U ⊆ S₀, P ⊆ A, Q ⊆ J, |Q| ≤ c, and M(W) ≠ ∅. The swap
keeps U, keeps |W| (so feasibility), and keeps M(W) ≠ ∅, so W′ ∉ 𝒮_a and W′ ∈ 𝓕(x) iff W′ ∈ 𝒵(x). The new P′ = (P − k + l) ∩ A
is still inside A, and Q′ = (Q − k + l) ∩ J. Four cases: k, l ∈ A gives Q′ = Q; k, l ∈ J gives |Q′| = |Q|; k ∈ J, l ∈ A
gives |Q′| = |Q| − 1; k ∈ A, l ∈ J gives |Q′| = |Q| + 1, which exceeds c iff |Q| = c. The 𝒵♯ case is the same computation
with A replaced by the current look-alikes 𝔄(M(W)) (M is unchanged, so the budget is unchanged). *Proof of (iii-3).*
For S′ ∈ Ω, e^{d(S′)−d(W)} = [γ₁(S′)/γ₀(S′)]·[γ₀(W)/γ₁(W)] = [π(S′)/π₀(S′)]·[π₀(W)/π(W)], because the normalising
constants cancel. Hence π₀(S′)(1 ∧ e^{d(S′)−d(W)}) ≤ min{π₀(S′), π(S′)π₀(W)/π(W)}; sum over S′ ∈ Bad(W). ∎

### 1.3 Theorem B is unaffected, and why (task item 1)

**Claim. PROVED.** Theorem B ([B] §4, with [V] Lemma F′ and Props. B1′/B2′) remains a valid finite inequality.

*Reason.* The proof of Theorem B never cites Prop. U. It uses the classification only through the §0 definition:
1. η₁, η₂ are defined as Σ_e sup_W P_W(e's step is bad) with "bad" = (T1) ∨ (T2) ∨ (T3). Lemma F′ then bounds
   P(some bad step before scoring) ≤ Hη. This needs nothing about *which* moves are bad.
2. Prop. B1 needs "on {no bad, no progress} the missing set is constant": a truth removal is bad by (T3), and a truth
   addition is progress. This is exactly the clause the shortcut (U-a) dropped, and the proof uses the full clause.
3. Prop. B2 needs "on {no bad, no progress} the state stays in 𝒮_a° with |P| constant": leaving is bad by (T1), raising
   |P| is bad by (T2), lowering it is progress.
4. h(l) is defined through "neutral" = not bad and not progress, again with the full definition.

So the shortcuts only misdescribe *which* moves the full definition charges. They never enter an inequality.

**The numbers also stand.** I read W1's constant code `scripts/progress_bounds.py` (branch theory/W1-T24G). In
phase 1 it charges every truth removal (Gibbs, swap, and independence through "good = S′ ∈ 𝒵 keeping every truth of W")
and every swap that leaves 𝒵. So it implements the full definition, not the shortcut. (It also counts an independence
landing in 𝒮_a∖𝒵 as bad, which overestimates η₁. That is conservative.) [V]'s numerics (`b2_check.py`) are phase-2 only
at a = 1, where bad = exit from 𝒮₁, which the shortcut handles correctly. W2-PREM's IND-M (§7(i)) and its neutral-step
list in §5.2 use the full definition. Its list also excludes the look-alike-for-junk-at-budget swap, which it calls bad
(b2). So no W1/W2 numerical or premise result changes.

**Prior verdicts that change.** [V]'s "Prop. U: VERIFIED as bookkeeping" becomes **ERROR in two shortcut sentences,
repaired by U′**. [V]'s confidence card (0.95 for Prop. U) should drop for the printed text. The corrected U′ is PROVED.

---------------------------------------------------------------------------------------------------------

## 2. Theorem B: boundary conventions and the carried quantity ([AR] §4; I agree)

**Theorem B (as carried into T38). PROVED (finite inequality; candidate, VERIFIED by A-REV1 after F′).** Setting of [B]
§4: EX-A, EX-S, SR, φ = 1, H terminal rounds with no resampling, start x, family 𝓕(x) (or 𝓕♯(x)), feasibility
s₀ + a(x) ≤ K with K = min(p, ⌊n/2⌋). Conventions:
- (C-0) If x = S₀, the bound is 0 (S₀ is a visited particle state, so it is scored: [B] (R3)).
- (C-1) For x ≠ S₀, v(x) ≥ 1.
- (C-2) **Empty phase 2.** If a(x) = 0, then 𝒮_0° = ∅, phase 2 is omitted, and c_* := c₁ (resp. c′₁, c₁♯).
- (C-3) **Empty suprema** (over empty sets) are 0. This includes ε′_del(1) and the restricted sup in B1′.
- (C-4) **Nonpositive constants.** Write c_*⁺ := max(0, c_*). If c_*⁺ = 0, the binomial term is 1.
- (C-5) **H = 0** gives the trivial bound 1.

The quantity carried into every composition and product is

  β_H(x) := min{ 1, P(Bin(H, c_*⁺(x)) < v(x)) + H·η(x) }   (x ≠ S₀),   β_H(S₀) := 0.

Here c_* may be any of W1's c_*, W2-VT24G's c′_* (B1′/B2′) or W2-PREM's c_*♯ (with c₁♯ = max{1−ε_add♯, (1−ε_pt♯)/|M(x)|}),
with its matching family. Then P_x(S₀ not scored within H rounds) ≤ β_H(x).

*Proof.* [B] §4 with [V] Lemma F′ for part (a); (C-0)–(C-5) are the trivial cases, and capping at 1 is free. ∎

**Corollary B-M, corrected wording. PROVED given IND-T.** Let I be a set of particles chosen by a rule that uses only the
past at a terminal boundary after which H rounds at φ = 1 run with no resampling. Then
P(no particle of I scores S₀ in those H rounds | boundary past) ≤ ∏_{i∈I} β_H(X_i).
- The selection must be past-measurable. Selecting particles by later success, by diagnostics, or by fresh-score counts is
  excluded.
- No independence of the initial (resampled) states is asserted.
- "No η → 0 is needed" is true only for a **fixed** H with Hη small. If H grows, β < 1 already requires Hη < 1.
- A per-particle bound uniformly below 1 plus a growing eligible count suffices, but the count is a delivery condition
  (T38 DELIV), not a consequence.

**IND-T boundary ([AR] §5; I agree).** Under EX-S, EX-A, the conditional product law holds for the *uninterrupted*
process at the boundary **after the stage-T resampling and before the stage-T move round**, with H′ = L + 5 rounds at
φ = 1. At the boundary **after the stage-T round**, only H = L + 4 rounds remain. Do not combine H′ = L + 5 with states read
after that round. The per-particle outputs are states, logical score evaluations and proposals, and RB records. The set of
*globally first-ever* fresh evaluations is not a per-particle output, because freshness depends on earlier particles. This
does not affect "S₀ ever scored". Conditioning on observed completion or diagnostics is not allowed. Example: independent
fair bits conditioned to be equal give P(00 | equal) = ½, while the product of the conditional marginals is ¼.

---------------------------------------------------------------------------------------------------------

## 3. Lemma P: the multiple-target sentence made precise ([AR] §4; I agree, checked here)

**Lemma P (multi-target form). PROVED.** Fix x and Good outcomes as in [B] §2, with s_e, b_e, q_e = s_e + b_e. Let C ⊆ Λ
be a nonempty set of labels with s_e(x) ≥ s_min for e ∈ C. Let D ⊆ Λ∖C be any set (the "dangerous" labels), and put
Q := Σ_{j∉C∪D} q_j(x), k := |C| + |D|. Then

  P*(x) ≥ s_min·(|C|/k)·[1 − Q/(k+1)].

*Proof.* Realise the order by iid U(0,1) arrival times and couple outcomes at x until the first change ([B] Lemma P). The
event "the earliest label g of C ∪ D lies in C, its outcome is Good, and no label outside C ∪ D arriving before T_g
changes the state" implies the event of P*. (If an outside label before T_g is Good without changing the state, the
first Good-or-change step is Good anyway.) The minimum τ of the k arrival times of C ∪ D has density k(1−t)^{k−1}. The
argmin is uniform on C ∪ D and independent of τ, so it lies in C with probability |C|/k. Given τ = t, each outside label
arrives before t independently with probability t, and then changes the state with probability q_j. So
P(no outside change before t) = ∏_j(1 − tq_j) ≥ 1 − tQ (Weierstrass). The Good outcome of g is independent of all of
this and has probability ≥ s_min. Integrating, ∫₀¹ k(1−t)^{k−1}(1 − tQ) dt = 1 − Q·E[τ] = 1 − Q/(k+1). The bound remains
valid when 1 − Q/(k+1) < 0, because its right side is then negative. ∎

With C = {g} this is [B]'s c_poly(x; g, D).

---------------------------------------------------------------------------------------------------------

## 4. Lemma S, corrected (replaces [T38E] §3; [AR] §3.2; I agree)

**Lemma S′ (ESS share). PROVED.** Let w₁,…,w_H > 0 have ESS (Σw)²/Σw² ≥ eH with e ∈ (0,1], put c := 1/e − 1, and let
A be an index set with |A| = fH. Then

  ω(A) := Σ_A w / Σ w ≥ max{ 0, f − √(f(1−f)c) }.

**Attainment.**
- (a) If 1 − e < f < 1, equality holds for the positive two-level weights w̄_A = 1 − √(c(1−f)/f) on A and
  w̄ = 1 + √(cf/(1−f)) off A. These have mean 1 and ESS exactly eH.
- (b) If 0 < f ≤ 1 − e, the lower bound is ≤ 0. The infimum of ω(A) over admissible positive weights is 0, and it is not
  attained: take weights ε on A and 1 off A, and let ε ↓ 0. The ESS stays ≥ eH for small ε.
- (c) f = 0: ω = 0 = the bound. f = 1: ω = 1 = the bound.
- The two-level low weight is positive **iff** f > 1 − e. At f = 1 − e it is 0, which is excluded.

*Proof.* The inequality: [T38E] §3 (Cauchy–Schwarz), plus ω ≥ 0 trivially.
- (a) The low weight 1 − √(c(1−f)/f) > 0 ⟺ c(1−f) < f ⟺ (1−e)(1−f) < ef ⟺ f > 1 − e. Mean:
  f(1 − √(c(1−f)/f)) + (1−f)(1 + √(cf/(1−f))) = 1. Second moment: 1 + f·c(1−f)/f + (1−f)·cf/(1−f) = 1 + c = 1/e, so
  ESS = H/(1/e) = eH. The share is f − √(f(1−f)c).
- (b) With weights ε on A and 1 off A, ESS/H = (fε + 1 − f)²/(fε² + 1 − f). This tends to 1 − f ≥ e. For 1 − f > e that
  is immediate. For 1 − f = e, (fε + e)² ≥ e(fε² + e) ⟺ fε(fε + 2e − eε) ≥ 0, which holds for ε ∈ (0, 2]. Then
  ω = fε/(fε + 1 − f) → 0, and ω > 0 for positive weights.
- (c) is direct. ∎

*Use in D2.* D2 uses e = 0.9 and f > 1/10 = 1 − e, which is inside range (a). D2 uses only the inequality.
**Numerics** (`scripts/lemmaS_lemmaU_check.py`, `results/lemmaS_lemmaU_check.json`): positivity matches f > 1 − e in all
27 (e, f) cells; at e = 0.9, f = 0.05 the low weight is −0.453 (A-REV1: −0.45297). Range (b) witnesses keep ESS ≥ eH with
ω → 0. The worst slack over 20,000 random cases (smallest-weight subsets) is −1.2·10⁻¹⁴, which is rounding. The
companion r* = (11+2√10)/9 = 1.92495059 gives 4r/(1+r)² = 0.9 exactly; 1.925 gives 0.89999269.

---------------------------------------------------------------------------------------------------------

## 5. D2 and D2-∞ with explicit rates (replaces [T38E] §4 corollary; [AR] §§6, 7.1; I agree)

**Theorem D2 (finite) is unchanged**, with [VT38E] §3.1 applied: NB′ in place of NB, and r* in place of 1.925 in the
sufficient condition. It is PROVED (VERIFIED by W3-VT38E and A-REV1). Three clarifications from A-REV1:
- it is a bound for the **potential first stage of the tier-0 pilot**, conditional on the data;
- the pilot must not be conditioned on its eventual calibration record;
- the bound may exceed 1 and can be capped.

The candidate-grid *restricted* ESS rule is a different object and does not substitute for the empirical pilot step.

**Corollary D2-∞, with rate margins. PROVED (implication).** Along R1, let x°_n, 𝒟_n be data-measurable with
x°_n Δ S₀ = {j_n} (and x°_n ∈ Ω), and let H = H₀ = ⌈512N₀/2500⌉ ≥ 0.2048·max(n, p). Suppose either of the following.
- **(Fixed margins)** There are fixed b₀ > 1/10, k_D < ∞ and c₀ ∈ (0,1] such that the data event
  𝔈_n := {π₀(x°_n) ≥ b₀, |𝒟_n| ≤ k_D, Dep_n ≤ 1 − c₀} has P₀(𝔈_n) → 1, and P(NB′ᶜ) → 0.
- **(General rates)** There are data quantities b_n > 1/10 and t_n ∈ (0, b_n − 1/10) with π₀(x°_n) ≥ b_n, and with
  β_n := (1 − Dep_n)₊/(|𝒟_n| + B + 3), such that H t_n² → ∞ and H β_n g(b_n − t_n) → ∞ in P₀-probability, and
  P(NB′ᶜ) → 0.

Then P(S₀ ∉ 𝒮_cal) → 0.

*Proof.* Fixed margins: take t = (b₀ − 1/10)/2 and β₀ := c₀/(k_D + 19) ≤ β_n on 𝔈_n (B ≤ 16). Since g is increasing on
[1/10, 1), on 𝔈_n the D2 bound is ≤ e^{−2Ht²} + P(NB′ᶜ | data) + exp{−Hβ₀g(b₀/2 + 1/20)}, and g(b₀/2 + 1/20) > 0. Take
expectations and add P₀(𝔈_nᶜ). H → ∞ kills both exponentials. General rates: the same with min{1, ·} and bounded
convergence. ∎

A-REV1's point stands: D2's own hypotheses at each n do not imply this. Finite D2 imposes no Dep < 1, so Dep ≥ 1 gives
β = 0. A pointwise b_n > 1/10 need not give a non-vanishing Hoeffding margin. The rates above are the missing inference.

---------------------------------------------------------------------------------------------------------

## 6. Theorem E3, corrected (replaces [T38E] §6.3; [AR] §3.3; I agree)

**Theorem E3′ (LS0 eligibility). PROVED (deterministic).** LS0 is the production local search (M §6.10) centred at the
start mode S̃₀ = argmax π₀. Its **first evaluation is the centre, offered to the HPM** (`emit_centre = true`, or an
explicit equivalent ledger insertion), and its scans are completed. Let 𝔅 ⊆ Ω be any set such that TD′(𝔅, ℓ) holds: from
every centre in 𝔅, the production local search (≤ ℓ moves, then one further scan) scores S₀. Then S̃₀ ∈ 𝔅 ⇒ S₀ ∈ 𝒮⁺.
- (i) If some x° ∈ Ω has π₀(x°) > ½, then S̃₀ = x°. No other state has mass ≥ ½, so there is no tie.
- (ii) **(corrected)** Let q, e be the T22 reference quantities of x° (locked T22 STATEMENT §1, computed on the actual
  blocks and tables, with π₀ the capped start law on Ω), and s = |x°|. **If 0 ≤ q < 1** and (1−q)^{s+1}/(1+e)^s > ½, then
  π₀(x°) > ½ (locked T22(i-a)), so (i) applies. Equivalently, it suffices that u < 1 with the same inequality in u
  (T22(i-b)).
- (iii) Under T27's H3 with assumed constant c₀ > ½ and S^{(0)} ⊆ S₀, (i) holds with x° = S^{(0)}. H3 is a premise; T27
  does not prove it.

*Proof.* (i) Σπ₀ = 1. (ii) locked T22(i-a), whose hypothesis is q < 1. (iii) substitution. The search is deterministic
given the data, and every scanned model and the emitted centre are scored. ∎

**Counterexample to the printed (ii), reproduced** (`scripts/e3_check.py`, `results/e3_check.json`; independent code).
n = 20, p = 2, orthogonal centred columns, y = x₂, singleton blocks (B = 1), reference x° = {1}, s = 1:
- r₁ = 0.2236068 (= 20^{−1/2}) and r₂ = 1.935517816·10¹²;
- q = r₂ and e = 4/r₁ = 17.888544;
- (1−q)²/(1+e) = 1.983334·10²³, while π₀({1}) = 9.441608·10⁻¹⁴, and the start mode is {2}.

These match A-REV1 to every printed digit. Over 300 random small instances (4,146 references, random partitions), T22(i-a)
held in all 2,051 cases with q < 1 (worst ratio π₀/bound = 1.0001). Among the 2,095 cases with q ≥ 1, the unrestricted
formula exceeded the true mass in 864 cases, and exceeded ½ while π₀(x°) ≤ ½ in 726 cases.

**LS0 score count (accounting clarification, [AR] §6).** There are at most ℓ + 1 scans, each of size
≤ max_{k≤K}[p + k(p−k)]. Counting every score call, LS0 costs at most **1 + (ℓ+1)·max_{k≤K}[p + k(p−k)]**. The 1 is the
emitted centre.

**Downstream uses of E3 (task item 2), checked.**

| Where | Which part of E3 | Affected? |
|---|---|---|
| W1-T38E §7, route (b1), "sufficient: ∃x° … π₀(x°) > ½ (T22(i) / T27-H3)" | (ii) | **Yes**: the T22(i) clause must carry q < 1. Superseded by T38_STATEMENT (b1). |
| W4-T38FULL Theorem b1 step 1, b1.1 row, b1.6/b1.7 (ELIG via W1-EXP Thm 6 / Thm 5(a)) | (i) only | No. W1-EXP Thm 6 / Thm 5(a) apply T22(i-a,b) "on {u_n° < 1}" (W1-EXP PROOF §3, Step 3), i.e. with the hypothesis. |
| W4-T38FULL part (c) LS0 cost | cost sentence | Yes: add 1 for the centre (T38_STATEMENT (c)). |
| W3-PXN Theorem P3 | T22(i-a) directly | No. It states "if q < 1 then …" (PROOF line 214), and q = O_P(√(log n/n)) → 0 makes q < 1 w.p. → 1. |
| W3-PXN Theorem P5, P6 | (i) only | No. |
| W3-PXN P7 (D2 route) | D2-b via P3 | No. |
| W2-BOOK §4.3 (eligibility remark: "a start-side event of T22(i) type") | informal | Wording only: say "T22(i-a) with q < 1". |

---------------------------------------------------------------------------------------------------------

## 7. Lemma U, corrected limiting constant (replaces [PREM] §2 display; [AR] §3.4; I agree)

**Lemma U(𝔉), corrected. PROVED (finite statement unchanged; constant corrected).** The statement of [PREM] §2 holds
verbatim with

  κ_n := (1+φ₀⁻²)/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/(c_E n),   ν = 0.01 + n/2,   c_E = σ²/(8(M + 2σ²)),

and the parenthetical "(κ_n → 0.52/c_E)" replaced by:

  **κ_n is strictly decreasing in n ≥ 2, κ_n ↓ 0.51/c_E = 4.08(M+2σ²)/σ², and κ_n ≤ 0.52/c_E for every
  n ≥ n₁ := 1 + 100[(1+φ₀⁻²)c_E/(2φ₀²) + 0.0102 + 0.51φ₀⁻²].**

*Proof.* (0.5 + 0.01/n)(1.02 + 1/(nφ₀²)) = 0.51 + [0.0102 + 0.5φ₀⁻²]/n + 0.01φ₀⁻²/n². Both summands of κ_n are
positive and strictly decreasing in n. The first tends to 0, and the second tends to 0.51/c_E. Moreover
κ_n − 0.51/c_E ≤ [(1+φ₀⁻²)c_E/(2φ₀²) + 0.0102 + 0.51φ₀⁻²]/((n−1)c_E), which is ≤ 0.01/c_E for n ≥ n₁. ∎

Numerics (`results/lemmaS_lemmaU_check.json`, four (M, σ², φ₀²) settings): κ_n is decreasing on n ∈ [3, 5000];
κ_{10⁹} − 0.51/c_E ≤ 1.2·10⁻⁷; the first n with κ_n ≤ 0.52/c_E is 71–289, below n₁ in each case.

**Family-count convention ([AR] §5; I agree).** The union bound in (E1)–(E4) must count *every* set to which (E1)–(E4)
are applied. For (E2), use span(X_V, X_{S₀}), whose rank is ≤ k + s₀. This changes the multiplicative constant
2^{(k+1)/2} to 2^{(k+s₀)/2}, not the exponent. If (E1) is used "for every V of size ≤ k", then A′ ≥ kA, and L = 4kA + 1
works. A data-dependent family selected using y must be replaced by a deterministic envelope.

**Same correction upstream.** W1-EXP Theorem 1's "(→ 0.52/c_* = 4.16(M+2σ²)/σ²)" and its Remark (b) ("|R| ≤ 0.52/c_* +
o(1)") should read 0.51/c_* = 4.08(M+2σ²)/σ² (or "≤ 0.52/c_* eventually"). W2-PREM REPORT §3's "κ_n → 4.16(M+2σ²)/σ²"
becomes 4.08. **Downstream effect: none.** Every use (EXP′, (C1)–(C6), W3-PXN's κ := sup_n κ_EXP) needs only a finite
bound, and κ_n ≤ κ_3 < ∞ for every n ≥ 3.

---------------------------------------------------------------------------------------------------------

## 8. NL0: the correct quantifier form and its downstream cost ([AR] §4; I agree)

**The gap.** W1 [B] §6 writes NL0(a) as sup_{W∈𝒮_a°} Σ_l o_l(W) = o_P(1/log n). But η₂ contains the null-addition term
**Σ_l sup_W** o_l(W), which is a sum over *labels* of sups over states. In general Σ_l sup_W ≥ sup_W Σ_l, and the
difference can be a factor of p. A-REV1's array, a_l(W_j) = 1/p for l = j and 0 otherwise, has sup-of-sum 1/p and
sum-of-sups 1. This counterexample is to the quantifier exchange; it is not claimed to be a BVS instance.

**Correct form (the rule).** Every η-type premise is a **sum over labels, outside, of a sup over states, inside**. For one
label, its destinations are summed *inside* the sup (as in β_I(W) above). So:

  NL0(a):  Λ₂(a) := Σ_{l∉S₀} sup_{W∈𝒮_a°, l∉W} o_l(W) = o_P(1/log n).

This is exactly W2-PREM §0's definition. The same rule gives τ₂ and TS (Σ_{i∈S₀} sup_W (1 − o_i(W))) and TL♯
(Σ_l sup_{W: l∈J(W)∖W} o_l(W)), all already written this way in W2-PREM §0/§6. UDEL is a single sup (ε_del is a max over
(W, l), not a sum), and IND(𝓕) is one label (sup_W of a sum over destinations). Both were already correct.

**What the correct form costs downstream (W2-PREM).**
1. **A design condition.** W2-PREM Prop. NL0 proves the sum-of-sups form only under the partner-graph condition PG(a):
   c_n log n → 0 and (eD_n+1)^a log^{3/2}n/√n → 0. Its proof replaces sup_W by a sum over the connected sets
   𝒦_a(l) (Lemma CMP), at most (eD_n+1)^a of them per l. That factor is the price of putting the sup inside the sum. The
   rate is Λ₂(a) = O_P((s₀+a+1)(eD_n+1)^a √(log n/n)).
2. **Genuineness.** W2-PREM's COUNTEREXAMPLE EQ (equicorrelated nulls, r = 0.8, p = n^{0.9}) shows Λ₂(1) ≥ 1 − o_P(1)
   under G, R, SE, BM-∞ alone. So NL0(a ≥ 1) is a genuine extra assumption, as A-REV1 says. (My heuristic computation for
   EQ suggests sup-of-sum also behaves like p^r/√n there, so EQ is not a case where the two forms separate. I did not
   check this further, and it is not used.)
3. **What does not change.** W2-PREM's Prop. NL0, UDEL, Corollary A and Theorem L are already stated with the correct
   quantifiers, so their conclusions are unchanged. What changes is the wording of W1 [B] §6 (the NL0(a) row and the
   concluding paragraph), W2-VT24G §6 item 2's "W1 §4's list (NL0, …)", and any T38 dependency row that cites "NL0" without
   the formula. T38_STATEMENT (b2) now cites Λ₂(a).
4. **Not implied.** Neither uniform REPAIR on all of 𝓡_d nor Hη → 0 follows from the finite Theorem B alone ([AR] §4).

---------------------------------------------------------------------------------------------------------

## 9. CE1: the narrow, correct wording ([AR] §5; I agree)

**What is retracted.** The blanket asymptotic claim "H24's uniform exit input fails in correlated designs" (W1 CE1's
asymptotic PROOF SKETCH, W2-VT24G's CE1 consequence) is **not** established as a universal statement. Its two limits
(o* → 1 and Q_T → 0) were never written out for a general class, and it stays PROOF SKETCH. The n = 200 numerics
(S2–S6: exit 0.62–0.98, exact lower bound ≥ 0.39) are finite-n evidence about the size of the constant. They are not an
asymptotic counterexample.

**CE1-narrow. COUNTEREXAMPLE (PROVED from Lemma E and Lemma U(C5), both candidates VERIFIED by A-REV1).** Fix r ∈ (0,1),
θ₁ ≠ 0 and an integer d ≥ 1. Let p_n = ⌈n^{1/3}⌉, S₀ = {1}, θ = θ₁e₁, and let the design be centred with exact Gram
X′X = (n−1)Σ, where Σ has unit diagonal, Σ₁₂ = r, and all other off-diagonal entries 0 (such X exists once
p_n ≤ n − 1). Then G, R (A = 1, ‖μ‖²/n ≤ θ₁²), SE (λ_min(Σ) = 1 − r) and BM-∞ (fixed θ₁) hold. Let
η_n := sup_{x∈𝓡_d} P_x(the next round has an elementary state outside 𝓡_d). Then η_n ≥ (1 − o_P(1))/(B_n + d + 4), and

  (L+4)·η_n → ∞ in P₀-probability   (L = ⌈log₂(n+1)⌉),

so H24's asymptotic input fails on this sequence, for every fixed d ≥ 1.

*Proof.*
1. Take the boundary state Y := {3, …, d+2}. Then Y ∈ 𝓡_d (|P(Y)| = d, |Y| ≤ K for large n), M(Y) = {1} (m = 1), and Y
   contains no truth, so Q_T(Y) = 0 exactly.
2. Lemma E ([V] §3): P_Y(exit) ≥ o*(Y)·[1 − 0]/(B+m+d+3) ≥ o₂(Y)/(B+d+4). Here 2 ∉ Y ∪ S₀ is a null, and adding it
   makes |P| = d + 1, which is an exit.
3. o₂(Y) → 1. Since x₃, …, x_{d+2} are orthogonal to x₁, x₂ and to each other (and p_n ≥ d+2 eventually), the signal gain from adding 2 at Y is
   Δ = ‖(P_{Y+2} − P_Y)μ‖² = (x₂ᵀμ)²/‖x₂‖² = r²θ₁²(n−1). Apply [PREM] Lemma U to the fixed family {(Y, 2)}. That family
   has a bounded number of sets, SE holds on them with φ₀² = 1 − r, and the RSS-floor sets are counted as in §7. Its
   corollary (C5) gives, on an event of probability → 1, odds₂(Y) ≥ (2p)⁻¹(n+1)^{−1/2}e^{−κ_n}e^{Δ/(8C_R)}, which tends
   to ∞ exponentially in n (p = n^{1/3}, κ_n bounded, Δ ≥ 4Lσ² log n eventually). So o₂(Y) → 1 in probability.
4. B_n ≤ 16, so η_n ≥ P_Y(exit) ≥ o₂(Y)/(d+20). Since L → ∞, (L+4)η_n ≥ (L+4)(1 − o_P(1))/(d+20) → ∞. ∎

*Scope.* This refutes the vanishing uniform-exit premise on the original 𝓡_d along one explicit sequence. It does not
refute Theorem B, which charges bad transitions differently. It does not promote W1/W2's broader sketches.

**Numerics** (`scripts/ce1_sequence.py`, `results/ce1_sequence.json`; d = 1, 5 noise replicates per cell, method score):

| r | n | p | B | o₂(Y) (min over reps) | Lemma E floor o₂/(B+5) | (L+4)·floor |
|---|---|---|---|---|---|---|
| 0.3 | 200 | 6 | 2 | 0.235 | 0.034 | 0.40 |
| 0.3 | 1,000 | 10 | 3 | 1.000 | 0.125 | 1.75 |
| 0.3 | 100,000 | 47 | 6 | 1.000 | 0.091 | 1.91 |
| 0.6 | 200 | 6 | 2 | 1.000 | 0.143 | 1.71 |
| 0.6 | 100,000 | 47 | 6 | 1.000 | 0.091 | 1.91 |

The floor stays bounded below. (L+4)·floor grows like (L+4)/(B+5), and so only logarithmically: B reaches 16 only at
p ≥ 256, that is n ≳ 1.7·10⁷. The failure of (L+4)η_n → 0 is therefore an asymptotic statement that is already visible
as "not small" at accessible n, not as divergence.
