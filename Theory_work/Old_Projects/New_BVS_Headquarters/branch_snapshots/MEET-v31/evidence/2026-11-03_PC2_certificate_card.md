<!-- Proof check PC2 (Opus 5.5, Claude Work, read-only), 2026-11-03; commissioned by the chair. Filed verbatim. Scripts in 2026-11-03_PC2_scripts/. -->
# PC2: proof check of the O-CERT certificate card, for the MEET-v31 chair

I edited, committed and pushed nothing, and started no subagents or jobs. The checks ran as exact enumeration at p ≤ 12, plus Fraction/Decimal arithmetic for the scorer test. Scripts are in `/tmp/claude-71711/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-v31/14bcdd62-deb0-4c36-99c9-68518a64c746/scratchpad/pc2/` (seeds 20261103–20261108):
- `t1_lemmaM_C4.py`
- `t2_bnb.py`
- `t3_cost.py`
- `t4_C1_C3.py`
- `t4b_flat.py`
- `t5_eta.py`

Every PROVED below is a **candidate** (PROTOCOL).

**How the probability claims are scoped.** PC1 claim 2 fixes the event. Under premises (i)–(iv), the only probabilistic statement is the joint output-event bound P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜):
- (i) Lemma RO / GUARD;
- (ii) a successful 𝓒 with E[Ẑ̄ | 𝓒] ≤ Z;
- (iii) CAL and EX-S;
- (iv) Ẑ = Z on the exact branch.

This bound is not conditional on 𝒪. Every other card item is deterministic: it holds surely on every realised output, under EX-A.

**Code facts used below:**
- **Store merge.** The final run re-offers the calibration's stored models (top store and both leader stores) to the final top store (`v3_core.cpp:409–419`). So 𝒯 is the top-(40p+1) of the run's realised scored set 𝒮, including tables, pilot and calibration. Any model evicted in calibration is ranked below ≥ 40p+1 models that were also offered to the final store.
- **No duplicates.** The store is a `std::set` keyed by (F, S) and offered only fresh evaluations (`v3_ledger.h:41–58, 104`). The scorer is deterministic, so 𝒯 has no duplicates.
- **Q formulas.** The engine's non-negative Q (`v3_score.h:147–160`) equals yᵀy − n zᵀH⁻¹z in exact arithmetic. I checked this algebraically: with β̂ = nH⁻¹z, ‖y−Xβ̂‖² + (‖Xβ̂‖² + ‖β̂‖²)/n = yᵀy − 2β̂ᵀz + β̂ᵀHβ̂/n. This answers O-CERT §6's escalation question in exact arithmetic. By PC1 claim 1, Q_S ≥ yᵀy/(n+1), so in exact arithmetic that branch fires only if n+1 > 10⁸.

---

## Lemma M (monotonicity)
**As written:** for S ⊆ S′: (a) Q_S ≥ Q_{S′}; (b) D_S ≤ D_{S′}; (c) w(k+1) ≤ w(k) for k ≤ p−1; (d) Q_S = yᵀy/(n+1) + (n/(n+1))yᵀ(I+(n+1)M_S)⁻¹y and D_S = det(I+(n+1)M_S)/det(I+M_S).

**Verdict: PROVED.** I checked every line:
- (d): push-through identity with c = n+1, and Sylvester's identity.
- (a): Loewner order reverses under inversion.
- (b): matrix determinant lemma, with h′(c) = xᵀ(I+cM)⁻²x ≥ 0 because the matrices commute.
- (c): w(k+1)/w(k) = (k+1)/(2p−1−k).

Numerically (`t1`): the error in (d) is ≤ 9·10⁻¹³; there were 0 monotonicity violations over 1,200 chains, including p > n.

**Event:** deterministic. **Exact premise:** EX-A. **Floating point:** nothing (it is an identity about exact functions). It enters only as a premise of C4.

## C1(a) (deterministic store bounds)
**As written:** "On 𝒪: for every S ∈ Ω, π(S) ≤ e^{F(S)}/Z_𝒯. For every A ⊆ 𝒯, π(A) ≤ Σ_Ae^F/Z_𝒯. For every scored S ∈ 𝒯, π(S)/π(Ŝ) = e^{F(S)−F(Ŝ)} ≤ e^{−g}."

**Verdict: CORRECT WITH AMENDMENT (Seat C's correction 2 is upheld).** The third clause is FALSE as written. Take S = Ŝ ∈ 𝒯 with g > 0: the ratio is 1, which is > e^{−g}. In `t4` the ratio is 1 against e^{−g} = 0.443.

**Amended statement:** "Under EX-A, with 𝒯 a set of distinct feasible models:
- Z_𝒯 ≤ Z;
- π(S) ≤ e^{F(S)}/Z_𝒯 for every S ∈ Ω;
- π(A) ≤ Σ_A e^F/Z_𝒯 for every A ⊆ 𝒯;
- π(S)/π(Ŝ) ≤ e^{−g} for every S ∈ 𝒯 ∖ {Ŝ}, where g := F(Ŝ) − max_{𝒯∖{Ŝ}} F;
- in particular, Ẑ < Z_𝒯 ⇒ Ẑ < Z (Seat C's underestimation implication)."

PROVED.

**Event:** surely, on every output. **Floating point:** compute Z_𝒯 over a deduplicated set. Use a validated lower bound Z_𝒯⁻ (each F̃ − η_F, plus the log-sum-exp rounding) and a numerator e^{F̃(S)+η_F}. The ratio clause needs a margin: π(S)/π(Ŝ) ≤ e^{−g̃+2η_F}. The open item in PC1 claim 2 ("Z_𝒯 ≤ Z in floating point") is closed only by SC(η_F) in its *validated* form (see C3/SC).

## C1(b) (simultaneous one-sided global bound)
**As written:**
- 𝔅_α ∩ 𝒪_E = {Z < αẐ} ∩ 𝒪_E;
- P(𝒪_E ∩ 𝔅_α) ≤ αP(𝒜) ≤ α;
- "with probability ≥ 1−α: π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, αẐ), and the posterior mass of the *unscored and unreported* models is at least 1 − Z_𝒯/(αẐ)."

**Verdict, set identity and bound: PROVED.** The identity uses Z ≥ Z_𝒯. The A-clause is never triggered for A = ∅, so the identity holds as stated. The probability bound is the PC1 claim-2 inclusion, so it holds under premises (i)–(iv). Premise (i), Lemma RO and GUARD, is still the unreviewed W2-BOOK premise.

**Verdict, the "unscored" sentence: FALSE (COUNTEREXAMPLE). Seat C's correction 1 is upheld.** The proved object is π(Ω ∖ A) for A ⊆ 𝒯. Ω ∖ 𝒯 contains the scored-and-evicted models, so a lower bound on its mass is not a lower bound on the never-scored mass.

Counterexample (`t4b`, exact enumeration, n = 24, p = 12):
- every model in Ω is scored, Ẑ = Z, so Z ≥ αẐ holds surely;
- 𝒯 = {Ŝ} is a reported set, which C1 allows ("any reported set");
- π(Ŝ) = 0.0483, so the stated bound is 1 − 0.0483/0.05 = +0.035;
- the unscored mass is 0.

With the engine's 40p+1 store, p ≤ 12 cannot reach Z_𝒯 < 0.05Z (`t4`: π(top 481) ≥ 0.97). At p = 500, though, Ω∖𝒯 strictly contains millions of scored models of positive mass, so that reading is unproved there too.

**Amended statement:** "Under the PC1 claim-2 premises, P(𝒪 ∩ {∃S ∈ Ω: π(S) > min{1, e^{F(S)}/max(Z_𝒯, 0.05Ẑ)}} ∪ {π(Ω∖𝒯) < 1 − Z_𝒯/(0.05Ẑ)}) ≤ 0.05·P(SMC ∩ 𝒜). Here Ω∖𝒯 is the mass **outside the reported store** (never-scored or scored-and-evicted). Not P(· | 𝒪)." The same correction applies to O-CERT's remark "the run has seen less than α of the posterior": it should read "the store holds less than α".

**Event:** output event 𝒪, joint. **Floating point:** as for C1(a), plus VAL-FP(η, ε) for Ẑ, which gives the bound 0.05e^{η} + ε (W2-BOOK Prop 2(f), unreviewed; η and ε not measured).

## C1(c) (no lower bound from unbiasedness)
**Verdict: PROVED,** relative to locked T31(c). Take c₀ < c: then {Ẑ ≥ cZ} ⊆ {Ẑ ≥ c₀Z}, which has probability ≤ η < γ.

Note for wording: O-CERT's prose that a lower bound on π(Ŝ) "needs PW2 or enumeration" is too strong. PC1 claim 1 gives the deterministic bound π(Ŝ) ≥ e^{F(Ŝ)}·(2b₀ + yᵀy/(n+1))^{ν}/C_n. It does not contradict C1(c), but it is about 530 nats loose at n = 200. Say "no useful lower bound". This is a non-claim, so it enters only as paper text.

## C2 (two-sided band under PW2)
**Verdict: PROVED, CONDITIONAL on PW2.**
- Cantelli step: Var W ≤ B_T/4 ⇒ P(W − 1 ≤ −ε) ≤ B_T/(B_T+4ε²), checked; the bound is monotone in σ².
- Event identity: {π(S) < (1−ε)e^F/Ẑ} = {W < 1−ε}, checked.
- Union bound and corollary (π(Ŝ) > ½ ⇒ unique HPM and Bayes rule), checked.
- Not re-checked: the T25(iv) pooled-variance clause and the "E_n of T20(ii)" sentence. I did not check those cited results.

**Event:** output event, plus E[1_𝒜B_T/(B_T+4ε²)]. B_T is not data-checkable. **Enters the output:** not at all. A "what-if" row next to certified rows invites misreading.

## C3 (exact relative certificates)
**Main identity:** π(Ŝ | R) = e^{F(Ŝ)}/Σ_R e^F on a fully scored region R. **PROVED.**

- **(a) Local.** *As written:* `local_certified` ⇒ F(S) ≤ F(Ŝ) on 𝒩(Ŝ); exact g_add, g_del, g_swap, ρ_loc. **CORRECT WITH AMENDMENT (minor).**
  - The implication holds because `v3_run.R:146` sets the flag only when hpm = returned, and "no improving neighbour" under the strict ≻ order excludes F(S) > F(Ŝ).
  - Amend: a maximum over an empty class (|Ŝ| = K for additions; Ŝ = ∅ for deletions and swaps) is −∞, so that gap is +∞ and is reported "n/a".
  - Floating point: the engine's check has no margin. The exact claim needs min(g̃_add, g̃_del, g̃_swap) ≥ 2η_F. Otherwise report "local maximum up to a numerical tie".
- **(b) Subsets.** **PROVED** as written.
- **(c) Best-of-scored.** *As written:* "for every S ∈ 𝒮̄ ∖ {Ŝ}, π(S) ≤ e^{−g}π(Ŝ)". **CORRECT WITH AMENDMENT.** 𝒮̄ is the *potential* uninterrupted run's scored set. On a stopped output it contains models never scored, and the claim is then unsupported for them.
  - Amended: "for every S ∈ 𝒮 ∖ {Ŝ}, where 𝒮 is the realised scored set, provided 𝒯 = top-(40p+1)(𝒮) in the HPM order (METH-AUDIT Lemma S together with the inheritance merge above) and |𝒯| ≥ 2."
  - Proof: S ∉ 𝒯 ⇒ F(S) ≤ min_𝒯 F ≤ F(top[2]).
  - `t4`: 602,695 (scored S, store) pairs, caps 2, 5, 4p+1 and 40p+1, 0 violations.
- **The "under SC(η_F)" sentence.** CORRECT WITH AMENDMENT. Add the rounding of the sums. **Seat C's correction 4 is upheld:** O-CERT says SC is "checkable by replay in higher precision", and it is not. A replay bounds |F̃ − F_hp|, not |F̃ − F|. Two implementations agreeing to 3·10⁻¹² is cross-implementation evidence, and O-CERT itself notes they can share rounding. SC is established only by validated (interval or ball) arithmetic on every number the card uses, or by a proved forward-error bound evaluated with rigorous condition bounds. Until then every card number carries the label "numerical implementation of an exact-arithmetic certificate".

**Event:** surely, on every output (EX-A).

## C4 (box certificate)
**As written:** F(S) ≤ Φ(L,U) and Σ_{[L,U]} e^F ≤ e^{M(L,U)}, plus:
- (a) optimality over [∅,U];
- (b) π(Ŝ | [∅,U]) ≥ (1 + Σ_{leaves≠{Ŝ}} e^{M(leaf)−F(Ŝ)})⁻¹;
- (c) refutation.

Under SC, F(Ŝ) is replaced by F(Ŝ) − 2η_F in (a).

**Verdict, bounds and (a): PROVED.** `t1`: 26,894 boxes, max F − Φ = 0 and max(log-sum − M) = 0, with equality only at singletons. `t2`: B&B optimality found no better model in 12 designs. Amendments:
- leaves with |L| > K are empty and are dropped;
- "all 2^{|U|} supports" should read "all S ⊆ U with |S| ≤ K".

**Verdict, (b): PROVED as written. Seat C's correction 3 is NOT a validity correction.** If Ŝ lies in a non-singleton leaf ℓ, that leaf is still in the sum "leaves ≠ {Ŝ}". Its e^{M(ℓ)} bounds the mass of all of ℓ, so Σ_{S≠Ŝ} e^F ≤ Σ_{leaves≠{Ŝ}} e^M still holds: the bound is valid and conservative. The cost of not isolating Ŝ is that e^{M(ℓ)} ≥ e^{F(Ŝ)} double-counts Ŝ, which caps the bound at ≤ ½. So isolating {Ŝ} is needed for *sharpness* (values above ½), not for truth.

In O-CERT's code (`cert_lib.R::bnb`, mass mode with τ = −12), a box containing Ŝ has M ≥ F(Ŝ) > F(Ŝ) + τ, so it is never pruned. Ŝ is therefore always isolated, and `t2` shows identical bounds both ways with 0 violations.

**Verdict, (c): PROVED.** The clause "if moreover S ∉ 𝒮̄" is redundant with realised 𝒮: F(S) > F(Ŝ) already forces S ∉ 𝒮, because Ŝ is the strict maximum over 𝒮. Use 𝒮, not 𝒮̄.

**Floating point:** CORRECT WITH AMENDMENT. SC(η_F) must also cover Φ(L,U) and M(L,U), which are not model scores (they mix D_L, Q_U and w(|L|)). (a) then needs Φ̃ ≤ F̃(Ŝ) − 2η_F, and (b) needs e^{±2η_F} factors plus summation error.

**Event:** deterministic, for any U, including a data-dependent U. **Cost remark** ("tree ~ 2^{#ambiguous variables}"): **not a theorem, so Seat C's correction 5 is upheld.** "Ambiguous" is undefined, and the only guaranteed bound is 2^{|U|+1} − 1 nodes. At p = 12 the trees were small: max 639 of 8,191 nodes (`t3`), and ≤ 3.4% over 30 adverse designs (`t2`). That is an empirical observation, which is the right label.

**Seat C's correction 6** ("16 best additions") **is upheld in the form Seat C wrote.** It changes no target, HPM, PIP or Ẑ, so it is not a sampler setting. It and the B&B node budget and τ are **declared certificate-region settings** of the output layer:
- they must be fixed in the spec and printed with the card;
- if the budget is exhausted, the card reports "unresolved";
- they never invalidate the fit;
- they change the card's content, never its truth;
- the U-rule matters for study-level statements such as C5's P(S₀ ⊄ U).

## C5 (posterior-miss certificate)
**Verdict: CORRECT WITH AMENDMENT.** The displayed probability inequality is PROVED, as an immediate consequence of C4(a).

Amendment: C4(a) gives only F(S₀) ≤ F(Ŝ). With an exact tie and S₀ ≻ Ŝ under the tie rule, "no search can repair it" fails. State it as "F(S₀) < F(Ŝ), or an exact tie with Ŝ ≻ S₀". Also require |S₀| ≤ K.

It needs S₀, so it is a study or paper item and not part of the per-fit output.

## C6 (the card) and "P(card false) ≤ 0.05"
**As written:** "P(𝒪 and some L, R or G claim on the card is false) ≤ α·P(𝒜) ≤ α", plus the paper sentence "claims hold simultaneously with probability at least 95%… whether or not the run completes"; fp version α e^{η} + ε.

**Verdict: CORRECT WITH AMENDMENT.**
1. The G row contains the false "unscored mass" line. Replace it with "mass outside 𝒯" (C1(b)).
2. The L row's best-of-scored claim must use realised 𝒮, not 𝒮̄ (C3(c)).
3. With 1–2 fixed, the L and R claims are surely true on 𝒪 under EX-A. The G claims fail exactly on {Z < 0.05Ẑ}. So P(𝒪 ∩ {some L/R/G item false}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05 under PC1 claim-2 premises (i)–(iv). **PROVED, modulo premise (i) (Lemma RO and GUARD), which is still unreviewed.**
4. The paper sentence reads as P(true | reported) ≥ 0.95. That is **not** proved. The conditional bound is only 0.05·P(SMC ∩ 𝒜)/P(𝒪), which can exceed 0.05. Write instead: "the probability that a run returns a card with a false claim is at most 5%".
5. The fp version is incomplete. VAL-FP covers Ẑ only, and the G claim also needs SC on F(S) and Z_𝒯 (C1(a) floating point). VAL-FP's (η, ε) and SC are unmeasured, so the fp card is **labelled numerical**.

**Remark C6′:** PROVED in exact arithmetic. On {Z_𝒯 ≥ 0.05Ẑ} the G claims hold surely, with no Ẑ involved. In floating point it needs Z_𝒯⁻ ≥ 0.05Ẑ.

## `global_certified` (exact branch; `v3_core.cpp:520–540`)
It computes `hpmF − η(Ŝ) > max_{S≠Ŝ}(F̃(S) + η(S))`. That is a rigorous implication **only if** |F̃(S) − F(S)| ≤ η(S) for every S ∈ Ω. That premise is not established:
- `v3_score.h:240` calls η a "documented heuristic", and the output labels it "heuristic (not a validated interval bound)".
- cond_H and cond_A are a squared Cholesky-diagonal ratio, which the code calls a "cheap *lower* estimate" of the condition number. A first-order bound built on a lower estimate is not an upper bound.
- η has no term for Gram-formation error (which grows with n), for errors in log w(k) and log W_K (which differ across sizes), or for rounding in the comparison itself.

My exact-rational test (`t5`: 60 cases, n ≤ 1000, k ≤ 3) found no violation: the maximum |error|/η was 0.069. That fails to refute the heuristic; it does not prove it.

**Verdict: a heuristic, conditional certificate, not a rigorous one.** It enters as a **labelled numerical** flag. On the SMC branch it is always FALSE (`v3_run.R:147`). A rigorous exact-branch certificate would need validated arithmetic. One route is C4 with U = [p] and validated Φ, which is not adopted here.

---

## Summary table

| item | verdict | enters v3.1 output as | premises |
|---|---|---|---|
| Lemma M | PROVED | rigorous (as C4's premise) | EX-A |
| C1(a) | CORRECT WITH AMENDMENT (exclude Ŝ; Seat C's correction 2 upheld) | rigorous in exact arithmetic; labelled numerical until SC validated | EX-A, distinct 𝒯 |
| C1(b) set identity and bound | PROVED (output event, joint) | rigorous in exact arithmetic / labelled numerical | PC1 claim 2 (i)–(iv); Lemma RO/GUARD unreviewed |
| C1(b) "unscored mass" | FALSE (COUNTEREXAMPLE `t4b`; Seat C's correction 1 upheld); amended to "outside 𝒯" | amended form only | as above |
| C1(c) | PROVED | not at all (paper non-claim) | locked T31(c) |
| C2 | PROVED, CONDITIONAL on PW2 | not at all | PW2 (not data-checkable), T25(iv) |
| C3 main identity, (b) | PROVED | rigorous in exact arithmetic / labelled numerical | EX-A |
| C3(a) | CORRECT WITH AMENDMENT (empty maxima; fp margin 2η_F) | same | EX-A, `local_certified` ∧ hpm = returned |
| C3(c) | CORRECT WITH AMENDMENT (realised 𝒮, not 𝒮̄) | same | EX-A, Lemma S, inheritance merge, \|𝒯\| ≥ 2 |
| SC "checkable by replay" | FALSE as a method of establishing SC (Seat C's correction 4 upheld) | — | validated arithmetic needed |
| C4 bounds, (a), (c) | PROVED, with amendments (\|L\|>K leaves; wording; SC must cover Φ, M; 𝒮 not 𝒮̄) | optional, rigorous in exact arithmetic / labelled numerical; "unresolved" on budget | EX-A, Lemma M, Ŝ ⊆ U |
| C4(b) | PROVED as written (Seat C's correction 3 is sharpness, not validity) | same as C4 | same |
| C4 cost remark | not a theorem (Seat C's correction 5 upheld); empirical | not at all | — |
| "16 best additions" / node budget / τ | declared certificate-region settings (Seat C's correction 6 upheld) | printed with the card | — |
| C5 | CORRECT WITH AMENDMENT (tie case; \|S₀\| ≤ K) | not at all (study level) | C4(a) |
| C6 bound | CORRECT WITH AMENDMENT (items fixed; joint, not conditional; fp incomplete) | rigorous in exact arithmetic / labelled numerical | PC1 claim 2 (i)–(iv), EX-A; fp: SC + VAL-FP |
| C6 paper sentence | FALSE as a conditional reading; amended | amended wording only | — |
| C6′ | PROVED | rigorous in exact arithmetic / labelled numerical | EX-A |
| `global_certified` | heuristic (conditional on an unproved error contract) | labelled numerical | η heuristic, `v3_score.h:236–250` |

## Recommended minimal card for v3.1 (POST HOC)

Every line below is stated in exact arithmetic. Until SC(η_F) is established by validated arithmetic, every computed number carries the label **"numerical implementation of an exact-arithmetic certificate"**, with η printed (`v3_score.h:242–246`). A failed or unfinished certificate computation never changes the fit's status.

**G1 (deterministic).** Let 𝒯 be the deduplicated reported store and Z_𝒯 = Σ_{S∈𝒯} e^{F(S)}. Then:
- Z_𝒯 ≤ Z;
- π(S) ≤ e^{F(S)}/Z_𝒯 for every S ∈ Ω;
- π(A) ≤ Σ_A e^F/Z_𝒯 for every A ⊆ 𝒯;
- π(S)/π(Ŝ) ≤ e^{−g} for every S ∈ 𝒯 ∖ {Ŝ}, with g = F(Ŝ) − max_{𝒯∖{Ŝ}} F;
- Ẑ < Z_𝒯 implies Ẑ < Z.

**G2 (one-sided, output-level).** Simultaneously for all S ∈ Ω:
- π(S) ≤ min{1, e^{F(S)}/max(Z_𝒯, 0.05Ẑ)};
- the posterior mass **outside the reported store**, π(Ω ∖ 𝒯), is ≥ 1 − Z_𝒯/(0.05Ẑ). These are models either never scored or scored and evicted; it is not a bound on never-scored mass.

These fail only on {Z < 0.05Ẑ}, and P(run returns output and G2 is false) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05. Premises: PC1 claim 2 (i)–(iv), with Lemma RO/GUARD unreviewed. The bound is not conditional on output. If Z_𝒯 ≥ 0.05Ẑ, G2 holds surely (C6′).

**L1 (local).** If `local_certified` and Ŝ is the returned centre, then F(S) ≤ F(Ŝ) for every feasible flip or swap S of Ŝ. Report exactly:
- g_add = F(Ŝ) − max_j F(Ŝ∪{j}), with +∞ if |Ŝ| = K;
- g_del = F(Ŝ) − max_i F(Ŝ∖{i}), with +∞ if Ŝ = ∅;
- g_swap, with +∞ if there are no swaps;
- ρ_loc = π(Ŝ | {Ŝ} ∪ 𝒩(Ŝ)).

**L2 (subsets).** Report exactly g_sub = F(Ŝ) − max_{S⊊Ŝ} F(S) and Σ_{S⊊Ŝ} π(S)/π(Ŝ).

**L3 (best-of-scored).** If 𝒯 = top-(40p+1) of the run's realised scored set 𝒮 in the HPM order and |𝒯| ≥ 2, then π(S) ≤ e^{−g}π(Ŝ) for every S ∈ 𝒮 ∖ {Ŝ}, with g = F(Ŝ) − F(top[2]).

**R (optional; declared region rule U(X, y, Ŝ) ∋ Ŝ, node budget and τ printed).** For a completed B&B partition of [∅, U] ∩ Ω (leaves with |L| > K dropped):
- (a) if every leaf has Φ(L, U′) ≤ F(Ŝ) or is a singleton {S} with F(S) ≤ F(Ŝ), then F(Ŝ) = max{F(S) : S ⊆ U, |S| ≤ K};
- (b) π(Ŝ | [∅, U]) ≥ (1 + Σ_{leaves ≠ {Ŝ}} e^{M(leaf) − F(Ŝ)})⁻¹, where a singleton leaf {S} contributes e^{F(S)−F(Ŝ)}. This is valid whether or not {Ŝ} is a leaf, but it exceeds ½ only if {Ŝ} is isolated;
- (c) any S ⊆ U found with F(S) > F(Ŝ) refutes Ŝ as HPM and is necessarily unscored.

If the budget is exhausted, report "unresolved". In floating point, (a) needs Φ̃ ≤ F̃(Ŝ) − 2η_F, with SC covering Φ and M.

**Card-level statement.** P(run returns output and some G2, L or R claim is false) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, in exact arithmetic, under PC1 claim-2 premises (i)–(iv). G1, L and R are true surely. The floating-point version (≤ 0.05e^{η} + ε) needs validated SC and VAL-FP(η, ε), neither of which is established, so it carries the numerical label.

**Excluded from the output:**
- C2 (conditional on PW2);
- C5 (needs S₀);
- the "unscored mass" wording;
- the B&B cost remark;
- any rigorous reading of `global_certified`, which stays a labelled numerical flag.
