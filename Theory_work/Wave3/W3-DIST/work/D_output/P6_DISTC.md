# Lemma P6 and Theorem DIST-C — complete proofs, with the code pins re-checked

**Status: DRAFT (by this seat, unchecked).** Stream D (Claude Opus 5.5), W3-DIST proof leg, 2026-11-15.
Targets: `STATEMENT.md` v1.3.1 §2 (Theorem DIST-C) and §3 (Lemma P6). DIST-1, DIST-2 and DIST-3 are taken as
**given hypotheses** (brief). Notation: `STATEMENT.md` §0 and `API_CARDS.md` "Common definitions".
Sanity script: `check_store.py` (output `check_store_output.txt`: 3000 random trials of the coded store rule and
2000 random trials of P6 (a), (b), no failure).

---

## STATEMENT-CHANGE REQUEST

None of these changes the substance of DIST-C. SCR-1 and SCR-2 fix wording that is false if read literally; SCR-3
to SCR-5 are editorial.

- **SCR-1 ((C-iii), "premise P-HIT; implied by S₀ ∈ 𝓜 and δ_n < ½").** That implication needs q_n^{1/2} ≤ ½, i.e.
  e^{−ct} ≤ ¼. With π(S₀) > ½ we get π(S₀) > q_n^{1/2} only when q_n^{1/2} ≤ ½. DIST-1's range t ≥ M₀ log n does not
  give ct ≥ log 4 for every choice of constants. **Change to:** "implied by S₀ ∈ 𝓜, δ_n < ½ and e^{−ct} ≤ ¼ (true for
  all n ≥ n₀ once cM₀ log n₀ ≥ log 4)". Proved below in that form (Theorem DIST-C (C-iii)(b)).
- **SCR-2 ((C-i), parenthesis "(λ = 0, π(𝒯) ≥ η: the fixed-fraction case)").** With λ = 0 the displayed event
  requires π(𝒯) ≥ e^{0} = 1, i.e. 𝒯 carries all the posterior mass. On the SMC branch 𝒯 ⊊ Ω always (§2, pin P27),
  so that event is empty. The parenthesis is therefore not an instance of the display. **Change to** the threshold
  form proved below as (C-i)(b): for every a ∈ (0, 1] (a may be any data/output-measurable random variable),
  P⊗({completed} ∩ {π(𝒯) ≥ a} ∩ {Π̂^𝒯(B_n) > e^{−ct}/a}) ≤ 3e^{−ct} + P*(interfaces fail); fixed fraction: a = η.
- **SCR-3 (§0 "P⊗ … as in [SAMP] §1").** The joint law is defined in [SAMP] §0, "Two probability levels"
  (`W3-SAMP/STATEMENT.md:29-36`); [SAMP] §1 holds the premises. §5 below gives the precise definition used here.
- **SCR-4 ((C-i), "on the complementary success event").** The literal complement of
  {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) > e^{−(c−λ)t}} contains the stopped runs and the runs with small π(𝒯), where
  the predictive bound need not hold. **Read and state it as:** on {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}}.
  (Proved in that form.)
- **SCR-5 (notation).** DIST-C's q_n := e^{−ct} clashes with the reader window q_n of §1R. I suggest renaming it
  ϱ_n. Below I write ϱ_n := e^{−ct} and give the §2 name in brackets.
- **Optional strengthening (STRONGER, for HQ).** (C-i) holds pathwise on a data event, not only under P⊗. This is
  Proposition C-i° below: one data event of P*-probability ≥ 1 − 3e^{−ct} − P*(interfaces fail), on which **every**
  completed run satisfies the bound, whatever its streams. Corollary C of §1R already uses this form. I suggest
  stating (C-i) this way.

---

## 0. Scope, inputs, hypotheses

**Scope.** These are statements about the output of the **final SMC run** returned by the public fit `v3_fit`. The
exact-enumeration branch (`v3_fit.R:120-132`) is excluded. So is every run whose status is not `"completed"`.

**Hypotheses (rule 11: inherited premises below PROVED-CHECKED are explicit).**
- **(H-DIST1)** = DIST-1 (1.1), as stated in `STATEMENT.md:68-71`, with its constants c ∈ (0, 1], C, C′, M₀, n₀:
  for n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀},
  P*[Π(B_n(t) | D_n) > e^{−ct}] ≤ 3e^{−ct} + P*(I_n(t)ᶜ), where
  B_n(t) := {(S, θ, v) : d_H(f_{S,θ,v}, f*) > C√(t/n) or |S| > s₀ + C′t/log n} and
  I_n(t) := 𝒟_n ∩ (E; M) ∩ (C; M′) ∩ (ND; c_D, m_n(t)) (the "interfaces").
- **(H-DIST2)** = DIST-2 (1.2) (`STATEMENT.md:86-88`), used only in Remark 6.6. **(H-DIST3)** = DIST-3, second display
  (`STATEMENT.md:93-97`), used only in (C-iii)(c) and (C-iv). To avoid a clash I call its constants c₃, C₃ and its
  design events I³_n := 𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T). The quoted content is: for every design in I³_n, outside a
  noise event of probability ≤ C₃e^{−c₃u}, Π(d_H(f, f*) > C₃√(u/n) | S = S₀, D_n) ≤ C₃e^{−c₃u}, for n ≥ n₀ and
  1 ≤ u ≤ n^{1−κ₀}.
- **(H-ID)** (identification of the coded score; `STATEMENT.md:390-391` lists it as the only inherited premise of the
  planned results). For every S ∈ Ω, the exact value of the coded score is
  F(S) = log ϖ(S) + log m(S), where ϖ(S) = w(|S|)/W_K, W_K = Σ_{k≤K} C(p, k)w(k), and m(S) is the marginal likelihood
  of the model. Moreover Π(S | D_n) = π(S) := e^{F(S)}/Z with Z := Σ_{S′∈Ω} e^{F(S′)}.
  *Sources.* [CC] CC2 (`W3-SAMP/lemmas/CC_code_check.md:46-47`: "F = log ϖ(|S|-model prior) + log m(S)
  (`cpp/v3_engine.h:97`), so e^F ∝ π(S) on Ω and Σ_Ω e^F = Z"; status "CODE-CHECKED"). Locked T01 identifies
  m(S) with the exact posterior of §0. Re-checked here: `cpp/v3_engine.h:97` `q.F = D.logprior[k] + lm`, and
  `cpp/v3_score.h:65-70` `logprior[k] = log w(k) − log W_K`, w(k) = ½/C(2p − 1, k).
- **(EX-A)** exact scores and arithmetic (W1-N1 premise, `Theory_work/Wave1/W1-N1/STATEMENT.md:70`: "**EX-A** exact
  scores and arithmetic"). Here it is used in two ways only: (i) each score the ledger receives equals the exact F(S);
  (ii) comparisons of scores are exact.
- The other premises of [SAMP] are used only by the delivery statements. §7 lists them for each statement.

**Positivity.** On {completed}, π(S) > 0 for every S ∈ Ω. Proof: completion requires preprocessing status "ok"
(`v3_fit.R:99-103`), which excludes a constant response (`v3_preprocess.R:115`). So s_y² > 0, the IG(0.01, 0.01 s_y²)
prior is proper, the slab N(0, nv(G_S + I)⁻¹) is proper, and m(S) > 0, as the integral of a strictly positive likelihood
against a proper prior. Also m(S) < ∞, by the closed form m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν} ([P1] `prop:closed`), since D_S ∈ (0, ∞), Q_S ≥ 0 and b₀ > 0. Also w(k) > 0. Hence e^{F(S)} ∈ (0, ∞) and π(S) > 0. ∎

## 1. Objects

- Parameter space 𝚯 := ⋃_{S∈Ω} {S} × ℝ^S × (0, ∞), with the σ-field generated by the Borel σ-fields of the pieces.
  Π(· | D_n) is the exact posterior on 𝚯 (§0 of STATEMENT). Π(· | S, D_n) is its conditional law given the model S,
  defined for S ∈ Ω, and π(S) = Π({S} × ℝ^S × (0, ∞) | D_n). Since Ω is finite,
  **(TP)** Π(B | D_n) = Σ_{S∈Ω} π(S) Π(B | S, D_n) for every measurable B ⊆ 𝚯 (law of total probability).
- For a law Q on Ω (Q(S) ≥ 0, Σ_S Q(S) = 1): QΠ(B) := Σ_{S∈Ω} Q(S) Π(B | S, D_n).
- **Index map.** ι : [p_ret] → [p_raw] maps internal column j to the original index `orig[j]` (`cpp/v3_score.h:18`;
  `orig = pre$kept`, `v3_fit.R:118`). ι is strictly increasing (`v3_setup.R:8` requires `orig` strictly sorted).
  Returned models are ι-images (`to_orig`). Below every model is in internal indices. S₀ = supp θ* ⊆ [p_ret], as in §0
  of STATEMENT.
- **Ledger objects of a completed run** (precise definitions in §4): 𝓜 is the set of models offered to the final-run
  ledger's stores; 𝒯 is the returned `top_store`; Ŝ is the returned `hpm`; MPM is the returned `mpm`.
- **Store BMA, plug-ins** (STATEMENT §2): π_𝒯(S) := e^{F(S)}/Σ_{S′∈𝒯} e^{F(S′)} for S ∈ 𝒯, and 0 off 𝒯;
  Π̂^𝒯 := π_𝒯Π; Π̂^H := Π(· | S = Ŝ, D_n); Π̂^M := Π(· | S = MPM, D_n) when MPM ∈ Ω.
- **Predictive densities.** For a probability Q on 𝚯 that may depend on the data, f̄_Q(x, y) := ∫ f_ξ(x, y) Q(dξ), with
  f_ξ = f_{S,θ,v} as in §0. f̄^𝒯 := f̄_{Π̂^𝒯}.
- ϱ_n := e^{−ct} [§2: q_n]. 𝔊_n(t) := {Π(B_n(t) | D_n) ≤ ϱ_n} is the **data success event** of DIST-1. It is a set of
  data sets and involves no stream.

## 2. Code pins (re-verified against the working tree on 2026-11-15)

Folder `Scripts/SMC_BVS/core/`. The commit identity "4676af6, unchanged at fe9a1d7" (`STATEMENT.md:248`) **could not be
re-verified**: the common rules forbid git commands. The full SHA-256 of the eleven files as read is in
`pins_sha256.txt` (this folder), so a later reader can confirm that the line numbers below refer to the same text.
(`source_manifest.json` is dated 2026-10-22 and predates LS0, so it is not used.)

"OK" = the cited lines say what is claimed. "OK (range)" = true, but the cited range is not exact; the exact range
is given.

| # | pin (as cited) | cited in | what the code says (checked) | verdict |
|---|---|---|---|---|
| P1 | `v3_run.R:142` | STATEMENT §2 | `out$hpm <- led$hpm$model; out$hpm_F <- …` | OK |
| P2 | `v3_run.R:159-162` | §2 | `P <- cbind(island pip)` (:159), `pip_r` (:161), `pip_primary <- rowMeans(P)` (:162) | OK |
| P3 | `v3_run.R:163` | §2 | `out$mpm <- as.integer(orig[out$pip_primary > 0.5])` | OK |
| P4 | `v3_run.R:154` | §2 | `out$log_Z <- v3_log_sum_exp(logZr) - log(R)` | OK |
| P5 | `v3_run.R:210` | §2 | `… out$top_store <- led$top` | OK |
| P6 | `v3_run.R:143-149` | here | non-completed: returns early with `out$ledger <- led` (incl. its `top`), no `top_store` field, estimates NA | OK |
| P7 | `cpp/v3_core.cpp:358-366` | §2 | `store_to_list` (:358-362: models in store order, `value` = stored F, `capacity`, `full`); `ledger_to_list` puts `top` = `store_to_list(L.top, D)` (:366) | OK |
| P8 | `cpp/v3_ledger.h:43-56` | §2 | `TopStore`: struct :43-64; `offer` :49-57 | OK (range; struct ends :64) |
| P9 | `cpp/v3_ledger.h:78` | §2 | `top.init(40 * p + 1, true)`, p = `d->p` | OK |
| P10 | `cpp/v3_ledger.h:49-56` | §2 (C-ii) | quick reject unless strictly better than the worst (:52); duplicate reject (:53); insert, then erase the worst if over capacity (:54-55) | OK |
| P11 | `cpp/v3_ledger.h:35-42` | here | `TopCmp`: larger v; if `hpm_order`, smaller size; then `lex_less` | OK |
| P12 | `cpp/v3_ledger.h:84-94` | here | `offer_hpm` replaces iff `hpm_better` (:85); `offer_stores` calls `offer_hpm` and `top.offer(F, S)` (:90-91) | OK |
| P13 | `cpp/v3_ledger.h:104-113` | here | `event`: `if (is_fresh) offer_stores(...)` (:112) | OK |
| P14 | `cpp/v3_util.h:117-126` | here | `lex_less` = `std::lexicographical_compare`; `hpm_better`: larger F, then smaller size, then `lex_less` | OK |
| P15 | `cpp/v3_engine.h:89-101` | [CC] CC2 | `eval`: cache miss → `sc.score`, insert; F = logprior + lm (:97); `if (emit)` → `led->event(…, fresh ‖ !cache, …)` (:98-100) | OK |
| P16 | `cpp/v3_engine.h:103-105` | [CC] | `held`: event with `is_fresh = false` | OK |
| P17 | `cpp/v3_engine.h:379-382` | [CC] | `local_search(centre, …, emit_centre, …)`; `eval(C, ME_LOCAL, emit_centre)` (:382) | OK |
| P18 | `cpp/v3_core.cpp:407-409` | [CC] | final-run `Ledger led` (:407), `ingest_tables(led, *h)` (:408), new empty `ScoreCache` (:409) | OK |
| P19 | `cpp/v3_core.cpp:372-386` | [CC] | `ingest_tables`: every block-table model with a non-NaN score → `led.event(U, F, …, true, …)` (:384) | OK |
| P20 | `cpp/v3_core.cpp:418-429` | [CC] | inherited models: size ≤ K checked (:425); scored by `sc.score`; `led.offer_stores(…)` (:427) | OK |
| P21 | `cpp/v3_core.cpp:443-452` | [CC], [SAMP] | islands r = 1..4 on stream 9 + r (:444), `run_island(r, N, g, L, Hm, tier, nullptr)` (:446); partial → `"resource_limit"` (:451) | OK |
| P22 | `cpp/v3_core.cpp:456, 459, 476, 480, 483-484` | [CC], [SAMP] PC | final local search from `led.hpmS`, centre not emitted (:456); guard → `resource_limit` (:459); LS0, centre emitted (:476); guard (:480); `catch NumericalFailure` → `"numerical_failure"` (:483-484) | OK |
| P23 | `cpp/v3_core.cpp:488-507` | here | only call of `offer_hpm` outside `offer_stores`: inside the `catch` (:502), hence never on a completed run | OK |
| P24 | `cpp/v3_score.h:226-237, 284` | [CC] | scorer throws `NumericalFailure` after the last fallback (:237); the cache is cleared when full (:284) | OK |
| P25 | `cpp/v3_score.h:39-40, 61-70` | here | `D.p = p` (number of columns passed), `D.K = min(p, n/2)`; `logprior[k] = logw[k] − logWK` | OK |
| P26 | `v3_preprocess.R:111-115`; `v3_fit.R:118` | here | constant columns dropped; `p = length(kept)`; context built on the kept columns. So `D.p` = p_ret | OK |
| P27 | `v3_preprocess.R:19-32` | here | SMC branch only if Σ_{k≤K} C(p,k) > (5H₀ + 4N₀)p, with N₀ ≥ 2500 and H₀ ≥ 512. So \|Ω\| > 12560p > 40p + 1 and 𝒯 ⊊ Ω on the SMC branch | OK |
| P28 | `v3_fit.R:120-127` | §2, [SAMP] §3 | exact branch: :120-132 (its status is `e$status` ∈ {"exact", failure}; never "completed") | OK (range; ends :132) |
| P29 | `v3_fit.R:154-160, 162, 171` | [SAMP] §0 | calibration not "ok" → return before the final run; final run (:162); every field of the final run, `status` included, is copied into the fit (:171) | OK |
| P30 | `v3_run.R:121, 218` | here | `out$status = raw$status`; `estimates_available <- TRUE` only on the completed path | OK |
| P31 | `cpp/v3_core.cpp:341-348` | here | `island_to_list` returns summaries (φ, ESS, increments, PIPs, RB accumulators, hashes, timings), **no particle states** | OK |
| P32 | `cpp/v3_start.h:92` | [CC] CC5 | table models with \|U\| > K skipped | OK |
| P33 | `cpp/v3_engine.h:116, 397` | [CC] CC5 | Gibbs adds only below K; local search skips additions at K | OK |

## 3. Lemma P6 (deterministic)

**Lemma P6.** Fix the data D_n. Let B ⊆ 𝚯 be measurable.
- (a) [BT4] If Q is a law on Ω and L ∈ [0, ∞) satisfies Q(S) ≤ Lπ(S) for every S ∈ Ω, then QΠ(B) ≤ LΠ(B | D_n).
- (b) [S1-11] For a > 0 and 𝔅 := {S ∈ Ω : Π(B | S, D_n) > a}: π(𝔅) ≤ Π(B | D_n)/a.

*Proof.* (a) Π(B | S, D_n) ≥ 0 for every S. So QΠ(B) = Σ_{S∈Ω} Q(S)Π(B | S, D_n) ≤ Σ_{S∈Ω} Lπ(S)Π(B | S, D_n) = LΠ(B | D_n),
using (TP) in the last step.
(b) By (TP) and nonnegativity of the terms with S ∉ 𝔅:
Π(B | D_n) ≥ Σ_{S∈𝔅} π(S)Π(B | S, D_n) ≥ Σ_{S∈𝔅} π(S)·a = a·π(𝔅). Divide by a > 0. ∎

**Lemma P6(c) (mixture convexity; used for the predictive bounds).** Let Q be a probability on 𝚯 and let A ⊆ 𝚯 be
measurable with d_H²(f_ξ, f*) ≤ ε² for every ξ ∈ 𝚯 ∖ A. Then f̄_Q is a density with respect to ν_x ⊗ Leb, and
d_H²(f̄_Q, f*) ≤ ∫ d_H²(f_ξ, f*) Q(dξ) ≤ ε² + Q(A).

*Proof.* Write μ := ν_x ⊗ Leb and g_ξ(x, y) := φ(y; â_ξ + xᵀb_ξ, v_ξ), so that f_ξ = g_ξ μ-a.e. and f* = φ(y; α* + xᵀβ*, σ*²).
On each piece {S} × ℝ^S × (0, ∞), the map (θ, v, x, y) ↦ g_ξ(x, y) is continuous: b_ξ is linear in θ, â_ξ = ȳ^r − x̄ᵀb_ξ,
and φ is continuous for v > 0. So (ξ, x, y) ↦ g_ξ(x, y) is jointly measurable, and Tonelli applies to nonnegative
integrands. (1) ∫ f̄_Q dμ = ∫ (∫ g_ξ dμ) Q(dξ) = 1. (2) For each (x, y), √· is concave and Q is a probability, so Jensen
gives √(f̄_Q(x, y)) ≥ ∫ √(g_ξ(x, y)) Q(dξ). Multiply by √f* ≥ 0, integrate in μ and use Tonelli:
∫ √(f̄_Q f*) dμ ≥ ∫ (∫ √(g_ξ f*) dμ) Q(dξ) = ∫ (1 − d_H²(f_ξ, f*)) Q(dξ). Hence d_H²(f̄_Q, f*) = 1 − ∫√(f̄_Q f*) dμ ≤
∫ d_H²(f_ξ, f*) Q(dξ). (3) d_H² ≤ 1 always, because ∫√(fg) ≥ 0. So the last integral is ≤ ε²·Q(𝚯 ∖ A) + 1·Q(A) ≤ ε² + Q(A). ∎

## 4. Code lemmas (what the returned store is)

Fix the data and the streams, assume EX-A, and suppose the run is completed (fit status `"completed"`, P29–P30).

**Definition (order).** For S, S′ ∈ Ω write S ≺ S′ ("S ranks before S′") iff F(S) > F(S′); or F(S) = F(S′) and
|S| < |S′|; or F(S) = F(S′), |S| = |S′| and `lex_less`(S, S′) (models are sorted index vectors; P14). For distinct sorted
vectors exactly one of `lex_less`(S, S′), `lex_less`(S′, S) holds (`std::lexicographical_compare` is a strict total
order on finite sequences). F is real-valued under EX-A. So ≺ is a strict total order on Ω. For A ⊆ Ω and an integer
k ≥ 1, top_k(A) denotes the set of the min(k, |A|) ≺-first elements of A.

**Lemma R0 (the comparators are ≺).** (i) If entries have the form (F(S), S), then `TopCmp{true}`(e, e′) holds iff S ≺ S′
(P11). Entries e, e′ are equivalent for `std::set` (neither compares less) iff S = S′. (ii) `hpm_better`(F(S), S, F(S′), S′)
holds iff S ≺ S′ (P14).
*Proof.* (i) `TopCmp` returns `a.v > b.v` when the values differ, then `a.S.size() < b.S.size()` when the sizes differ,
then `lex_less(a.S, b.S)`. With v = F(S) this is the definition of ≺. Since ≺ is a strict total order, neither
S ≺ S′ nor S′ ≺ S holds iff S = S′. (ii) `hpm_better` makes the same three comparisons in the same order. ∎

Every entry offered to the final-run store has v = F(S) exactly. Offers come from `offer_stores(S, F, …)` with the F
computed by `eval` (P15), from the block tables (P19: `F = logprior[|U|] + logm_tab`), or from inherited models (P20:
`logprior[|S|] + sc.score(S).logm`). Under EX-A each of these is the exact F(S) of (H-ID).

**Definition (𝓜).** 𝓜 is the set of models S for which `offer_stores` is called on the final-run ledger `led`
(P18) during the run. On a completed run `top.offer` is called only inside `offer_stores` (P12; the only other `offer`
call, `cpp/v3_core.cpp:549`, belongs to the exact enumeration on its own store). `offer_hpm` is called only inside
`offer_stores` (P23). So 𝓜 is also exactly the set offered to the running HPM.

**Lemma R (store invariant).** Let A_m be the set of models offered by the first m calls of `top.offer`, and s_m the
set of models in `top.s` after these calls. Then s_m = top_k(A_m) for every m, where k = 40p_ret + 1 ≥ 81. In
particular the returned 𝒯 = top_k(𝓜), listed in ≺-order (P7: `store_to_list` iterates the set in comparator order).

*Proof.* Induction on m. m = 0: s_0 = ∅ = top_k(∅) (`init` builds an empty set, P8). Step: call m + 1 offers e = (F(S), S).
Write A := A_m, s := s_m = top_k(A), A′ := A ∪ {S}. The code (P10) does the following. If |s| ≥ k and not
`cmp`(e, last(s)), it returns. Else, if `s.count(e)` (an equivalent entry is present, i.e. S ∈ s by R0(i)), it returns.
Otherwise it inserts e and, if then |s| > k, erases the ≺-last element. (`*s.rbegin()` and `std::prev(s.end())` are
the ≺-last element of the set.) Note |s| ≤ k always, so "|s| ≥ k" means |s| = k.
- Case 1: S ∈ A. Then A′ = A, and we must show s is unchanged. If the code inserted e, then S ∉ s and (|s| < k or
  S ≺ last(s)). If |s| < k, then s = top_k(A) = A, so S ∈ s: contradiction. If |s| = k and S ≺ last(s): S ∈ A ∖ s and
  s = top_k(A) imply that every element of s ranks before S, in particular last(s) ≺ S: contradiction. So the code
  returned without change, and s_{m+1} = s = top_k(A′).
- Case 2: S ∉ A, |s| = k and not (S ≺ last(s)). Since S ≠ last(s) and ≺ is total, last(s) ≺ S. So S ranks after all k
  elements of s, and top_k(A′) = s. The code returns at the quick-reject line without change.
- Case 3: S ∉ A, and (|s| < k or S ≺ last(s)). S ∉ s, so `count` is 0 and e is inserted. (3a) If |s| < k then s = A, so
  s ∪ {S} = A′ with |A′| ≤ k. Nothing is erased, and s_{m+1} = A′ = top_k(A′). (3b) If |s| = k and S ≺ last(s), then
  |s ∪ {S}| = k + 1 and the code erases the ≺-last element of s ∪ {S}. That element is last(s), because S ≺ last(s).
  So s_{m+1} = (s ∖ {last(s)}) ∪ {S}. This is top_k(A′): every T ∈ A ∖ s ranks after all of s (since s = top_k(A)), so
  at least k elements of A′ rank before T and T ∉ top_k(A′); hence top_k(A′) ⊆ s ∪ {S}, and among these k + 1
  elements the ≺-last one, last(s), is excluded. ∎

**Lemma M (what 𝓜 contains).** On a completed run, 𝓜 = 𝓜_tab ∪ 𝓜_inh ∪ 𝓜_eval, where:
- 𝓜_tab is the set of block-table models with a score (P19, P32);
- 𝓜_inh is the set of inherited models (P20); these are the models of the calibration's three stores
  (`cpp/v3_core.cpp:728-735`);
- 𝓜_eval is the set of models on which the final-run engine calls `eval` (with either value of `emit`) or `held`: the
  islands' initial draws, Gibbs flips and held states, swap and independence proposals (accepted or rejected), and
  every model scanned or used as a centre by the final local search and LS0.

Also ∅ ∈ 𝓜 (the empty code of every block table, P19), so 𝓜 ≠ ∅, and 𝓜 ⊆ Ω.

*Proof.* "⊆": by the Definition, offers are made only by `event` with `is_fresh` true (P13), which `eval`, `held` and
`ingest_tables` call, and by the inherited loop (P20). Each of these offers a model in 𝓜_tab ∪ 𝓜_inh ∪ 𝓜_eval.
"⊇": 𝓜_tab and 𝓜_inh are offered directly (P19 with `is_fresh = true`; P20). Take S ∈ 𝓜_eval, and look at the first
`eval`/`held` call on S in the final run.
- (a) A `held` call re-emits the current state of a particle. That state was set either by `set_model` followed by
  `eval(P[i], ME_INIT)` with `emit = true` (`cpp/v3_engine.h:290-291`), or by copying `tmpQ` (`:131, 158, 179, 191`),
  which was just `eval`ed with `emit = true` (`:122, 153, 174, 186`). So an `eval` with `emit = true` on S precedes it.
- (b) An `eval` with `emit = true` either misses the cache — then `fresh = true` and the event offers S (P15, P13) — or
  hits it. The cache is created empty for the final run (P18) and only `eval` inserts into it (`cpp/v3_engine.h:93`).
  So a hit means an earlier `eval` on S in this run. If that earlier call had `emit = true` and was fresh, it offered
  S. Apply the same reasoning to that earlier call; there are finitely many calls.
- (c) The only `eval` with `emit = false` in the final run is the centre of the final local search (P17, P22: `false`
  at `:456`). That centre is `led.hpmS`, the current running best, which is an offered model.
- (d) A cache clear (P24) only turns a later hit into a fresh evaluation, which offers S again; repeated offers do not
  change the store (Lemma R, Case 1).

Hence every S ∈ 𝓜_eval is offered. Finally, ∅ is offered because each block table has the code 0 (U = ∅, size
0 ≤ K, `cpp/v3_core.cpp:378-384`; its score is set at `cpp/v3_start.h:93-94`). 𝓜 ⊆ Ω is [CC] CC5
(`CC_code_check.md:88-92`), re-checked at P32, P33 and P20 (:425). ∎

**Corollary R1 (retention; HPM = first entry).** On a completed run, under EX-A:
- (i) Ŝ is the ≺-first element of 𝓜, and it is the first entry of 𝒯.
- (ii) If S* ∈ 𝓜 and F(S*) > F(S) for every S ∈ Ω ∖ {S*}, then S* ∈ 𝒯, S* is its first entry, and Ŝ = S*.

*Proof.* (i) `offer_hpm` replaces the running best iff the offered model ranks before it (`has_hpm` false at the
start; P12 with R0(ii)). By induction over the offers, `hpmS` is the ≺-first element of the models offered so far. By
P23 the set offered to `offer_hpm` on a completed run is 𝓜. Lemma R gives 𝒯 = top_k(𝓜) with k ≥ 1 and 𝓜 ≠ ∅
(Lemma M), and top_k(𝓜) contains the ≺-first element of 𝓜, listed first. Finally `out$hpm` is `led$hpm$model` (P1).
(ii) 𝓜 ⊆ Ω (Lemma M), so S* ranks before every other element of 𝓜 (the first clause of ≺ decides). Apply (i). ∎

**Lemma U (posterior majority ⇒ unique maximiser).** If S* ∈ Ω and π(S*) > ½, then F(S*) > F(S) for every
S ∈ Ω ∖ {S*}.
*Proof.* For S ≠ S*: π(S) ≤ Σ_{S′≠S*} π(S′) = 1 − π(S*) < ½ < π(S*). By (H-ID), F(S) = log Z + log π(S) with π(S) > 0
(Positivity), and log is strictly increasing. (Same as C-PACK SL0(iv), re-derived.) ∎

**Lemma W (returned weights).** On a completed run, under EX-A and (H-ID): `top_store$value` lists F(S), S ∈ 𝒯 (P7, with
`top.offer(F, S)` at P12). Hence π_𝒯(S) = π(S)/π(𝒯) for S ∈ 𝒯, and Π̂^𝒯 = Π(· | S ∈ 𝒯, D_n). Also 0 < π(𝒯) < 1.
*Proof.* e^{F(S)} = Zπ(S) by (H-ID). So π_𝒯(S) = Zπ(S)/(Z Σ_{S′∈𝒯} π(S′)) = π(S)/π(𝒯). By (TP) restricted to 𝒯,
Σ_{S∈𝒯} (π(S)/π(𝒯))Π(· | S, D_n) = Π(· ∩ {S ∈ 𝒯} | D_n)/π(𝒯). π(𝒯) > 0 because 𝒯 ≠ ∅ and by Positivity. π(𝒯) < 1 because
𝒯 ⊊ Ω (P27) and Positivity. ∎

## 5. The joint law P⊗ (precise)

Sample point ω = (D_n, U_cal, U_fin): the data; streams 0–9 (pilot and diagnostic calibration streams); final streams
10–13 (island r on stream 9 + r). The calibration record is 𝓒 = 𝓒(D_n, U_cal) (CAL). The run's output is
O = Φ(D_n, U_cal, U_fin), the deterministic realisation map of the code in exact arithmetic (EX-A); MEAS makes Φ
measurable. **P⊗ is any probability on the sample space of ω such that:**
- **(P⊗-1)** the D_n-marginal of P⊗ is P*;
- **(P⊗-2)** (only where a delivery statement of [SAMP] is invoked) **H-U**: "fresh independent ideal U[0,1) uniforms
  within each stream" (`W1-N1/STATEMENT.md:71`; the proof uses the within-stream law of stream 9 + r, `:73-74`). **SI**:
  "Final stream 9 + r is independent of streams 0–9, for each r" (`:80`). Following [SAMP] §0 ("Under the joint law
  the final streams 10–13 are idealised as independent of the data as well as of streams 0–9 (H-U/SI; C1 Opus #7)",
  `W3-SAMP/STATEMENT.md:35-36`), the final streams are independent of (D_n, U_cal). **IND-T** (the four final streams
  are mutually independent) is used only where [SAMP] D-ii is used; it is not used here.

[SAMP]'s asymptotic claims are "under the **joint data/algorithm law** along n → ∞ and are always intersected with 𝒜
(potential quantities) or with {completed} ⊆ 𝒜 (reported outputs)" (`W3-SAMP/STATEMENT.md:33-35`). This is the law
above with (P⊗-1)–(P⊗-2). Here 𝒜 = {SMC branch and `v3_calibrate` returns status "ok"} (`:39-41`), and
**{completed} ⊆ 𝒜** (P29: no final run is made otherwise). The coded uniforms lie on the 2⁻⁵³ grid; H-U idealises
this ([SAMP] §3).

**Lemma J (data-event transfer; no independence).** Let E be an event of ω and G a measurable set of data sets with
E ⊆ {D_n ∉ G}. Then P⊗(E) ≤ P*(Gᶜ) under (P⊗-1) alone. (If E is not known to be measurable, the bound holds for the
outer probability.)
*Proof.* Monotonicity, then (P⊗-1): P⊗(E) ≤ P⊗(D_n ∈ Gᶜ) = P*(Gᶜ). ∎

## 6. Theorem DIST-C — statements and proofs

Throughout: n ≥ n₀, M₀ log n ≤ t ≤ n^{1−κ₀}, B_n := B_n(t), ϱ_n := e^{−ct}, and (H-DIST1). "Completed run" means fit
status `"completed"` (P29–P30). EX-A and (H-ID) hold throughout.

### (C-0) Domination transfer (deterministic) [BT4]
**Claim.** Fix the data. If Q(S) ≤ L_nπ(S) for every S ∈ Ω, then QΠ(B) ≤ L_nΠ(B | D_n) for every measurable B. Store BMA:
L_n = 1/π(𝒯). Single model Ŝ ∈ Ω: L_n = 1/π(Ŝ).
*Proof.* The first sentence is Lemma P6(a). Store BMA: by Lemma W, π_𝒯(S) = π(S)/π(𝒯) on 𝒯 and 0 elsewhere, so
π_𝒯(S) ≤ π(S)/π(𝒯) for every S ∈ Ω. Single model: Q = δ_Ŝ has Q(Ŝ) = 1 = π(Ŝ)/π(Ŝ) and Q(S) = 0 for S ≠ Ŝ. π(Ŝ) > 0
by Positivity. ∎

### Proposition C-i° (pathwise form; no stream premise)
**Claim.** Let λ ∈ [0, c). Fix a data set in 𝔊_n(t). Then **every** completed run (any calibration outcome, any final
streams) with π(𝒯) ≥ e^{−λt} satisfies (1) Π̂^𝒯(B_n) ≤ e^{−(c−λ)t} and (2) d_H²(f̄^𝒯, f*) ≤ C²t/n + e^{−(c−λ)t}.
More generally, for every a ∈ (0, 1], every completed run with π(𝒯) ≥ a satisfies Π̂^𝒯(B_n) ≤ ϱ_n/a and
d_H²(f̄^𝒯, f*) ≤ C²t/n + ϱ_n/a.
*Proof.* By (C-0), Π̂^𝒯(B_n) ≤ Π(B_n | D_n)/π(𝒯) ≤ ϱ_n/a, using Π(B_n | D_n) ≤ ϱ_n (definition of 𝔊_n(t)) and π(𝒯) ≥ a.
With a = e^{−λt} this is e^{−ct}e^{λt} = e^{−(c−λ)t}. For the predictive density apply Lemma P6(c) with Q = Π̂^𝒯,
A = B_n and ε² = C²t/n. Every ξ ∉ B_n has d_H(f_ξ, f*) ≤ C√(t/n) by the definition of B_n. ∎

### (C-i) Store BMA, under P⊗
**Claim.** (a) For every λ ∈ [0, c):
P⊗({completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) > e^{−(c−λ)t}}) ≤ 3e^{−ct} + P*(I_n(t)ᶜ).
On {completed} ∩ {π(𝒯) ≥ e^{−λt}} ∩ {Π̂^𝒯(B_n) ≤ e^{−(c−λ)t}}, d_H²(f̄^𝒯, f*) ≤ C²t/n + e^{−(c−λ)t}.
(b) [SCR-2] For every a ∈ (0, 1] (deterministic, or any random variable of ω):
P⊗({completed} ∩ {π(𝒯) ≥ a} ∩ {Π̂^𝒯(B_n) > ϱ_n/a}) ≤ 3e^{−ct} + P*(I_n(t)ᶜ).
*Proof.* (a) By C-i°, the event is contained in {D_n ∉ 𝔊_n(t)}. Lemma J and (H-DIST1) give
P⊗(·) ≤ P*(Π(B_n | D_n) > ϱ_n) ≤ 3e^{−ct} + P*(I_n(t)ᶜ). The predictive clause: on the stated event, Lemma P6(c) with
Q = Π̂^𝒯, A = B_n, ε² = C²t/n gives d_H²(f̄^𝒯, f*) ≤ C²t/n + Π̂^𝒯(B_n) ≤ C²t/n + e^{−(c−λ)t}. (b) The same argument with
the general-a part of C-i°, applied pointwise in ω. ∎
*Used:* (P⊗-1), (H-DIST1), (H-ID), EX-A (weights), CC5 (𝒯 ⊆ Ω). No H-U, SI, START, KERNEL or overlap premise.

### (C-ii) When does the store hold enough mass?
**(α) With selection.** Write δ_n := 1 − π(S₀), with π(S₀) := 0 if S₀ ∉ Ω.
- **(α-det) Claim.** On {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½}: S₀ ∈ 𝒯, π(𝒯) > ½, and Ŝ = S₀ (first entry of 𝒯).
  *Proof.* S₀ ∈ 𝓜 ⊆ Ω and π(S₀) = 1 − δ_n > ½, so S₀ is the unique maximiser of F over Ω (Lemma U). Corollary R1(ii)
  gives S₀ ∈ 𝒯 and Ŝ = S₀. Then π(𝒯) ≥ π(S₀) > ½. ∎ (Deterministic; uses EX-A, (H-ID), Lemma R, Lemma M; no sampler
  premise.)
- **(α-disc) Claim (discovery).** Assume (P⊗-1), (P⊗-2) and the premises of [SAMP] Theorem D (D-i): EX-A, H-U, START,
  KERNEL (control-flow clause only), CAL, SI, MEAS. Then for each r ≤ 4:
  P⊗({completed} ∩ {S₀ ∉ 𝓜}) ≤ E⊗[1_𝒜 (1 − π₀(S₀))^{D_r}] ≤ E⊗[e^{−Q_D}],
  with Q_D := D_rπ₀(S₀) on 𝒜 and Q_D := ∞ off 𝒜, D_r = N_e(1 + T + L + 4). Under **P-OVL** the right side → 0.
  *Proof.* (1) {completed} ⊆ 𝒜 (§5). On {completed}, Lemma PC (i), (iii) ([SAMP] `STATEMENT.md:90-95`, quoted in §7)
  give 𝓜 ⊇ 𝓜_r, where 𝓜_r is island r's set of evaluated models; on {completed} this set equals the one of the
  potential run on the same stream. So {completed} ∩ {S₀ ∉ 𝓜} ⊆ 𝒜 ∩ {S₀ ∉ 𝓜_r^{pot}}. (2) D-i, quoted in §7: given 𝓒
  on 𝒜, P(S₀ ∉ 𝓜_r | 𝓒) ≤ (1 − π₀(S₀))^{D_r}. In [SAMP] "given 𝓒" means conditional on the data and 𝓒
  (`W3-SAMP/STATEMENT.md:29-30`). Here S₀ is a function of the design, hence fixed under this conditioning; this
  matches [SAMP]'s "a fixed model S₀ ⊆ [p] with s₀ ≤ K" (`:26`). If S₀ ∉ Ω then π₀(S₀) = 0 and the bound is the
  trivial 1. Integrating the conditional bound (≤ 1) over (D_n, 𝓒) on 𝒜 gives the first inequality, exactly as in
  `W3-SAMP/lemmas/D_theorem.md:46-52`. (3) (1 − a)^D ≤ e^{−aD} for a ∈ [0, 1] and D ≥ 0 gives the second. (4) P-OVL:
  "Q_D → ∞ in probability" (`W3-SAMP/STATEMENT.md:82-83`). So e^{−Q_D} → 0 in probability; it is bounded by 1, and
  bounded convergence gives E⊗[e^{−Q_D}] → 0. ∎
  As stated in §2, P-MAP is not needed for discovery; it is needed only to identify Ŝ, and here δ_n < ½ does that
  job in (α-det).
- **(α′) Combined bound (follows from (C-i) and (α)).** Under the premises of (α-disc), for n ≥ n₀ and t in range:
  P⊗({completed} ∩ {Π̂^𝒯(B_n) ≥ 2ϱ_n}) ≤ 3e^{−ct} + P*(I_n(t)ᶜ) + P*(δ_n ≥ ½) + E⊗[1_𝒜(1 − π₀(S₀))^{D_r}].
  *Proof.* Split {completed} by the events 𝔊_n(t), {δ_n < ½}, {S₀ ∈ 𝓜}. On {completed} ∩ 𝔊_n(t) ∩ {δ_n < ½} ∩ {S₀ ∈ 𝓜},
  (α-det) gives π(𝒯) > ½. Then (C-0) gives Π̂^𝒯(B_n) ≤ Π(B_n | D_n)/π(𝒯). If Π(B_n | D_n) > 0, this is < 2Π(B_n | D_n) ≤ 2ϱ_n;
  if Π(B_n | D_n) = 0, it is 0 < 2ϱ_n. So {completed} ∩ {Π̂^𝒯(B_n) ≥ 2ϱ_n} ⊆ {D_n ∉ 𝔊_n(t)} ∪ {δ_n ≥ ½} ∪
  ({completed} ∩ {S₀ ∉ 𝓜}). Lemma J, (H-DIST1) and (α-disc) bound the three pieces. ∎
- **Alternative discovery source (cited, not verified here).** W3-RM2:RM2-F / RM2-R (status in STATEMENT §4:
  "PROVED-CHECKED, conditional on SOP:TH09" / "… conditional on W2-APP:POST"). RM2-F (C1) states, under its premises:
  "there is a data event 𝒢_n with P(𝒢_n) → 1 on which every admissible output run — every seed, N_e, R′ and calibration
  outcome — reports Ŝ⁺ = S₀" (`W3-RM2/STATEMENT.md:206-209`). The reported HPM is always an element of 𝓜
  (Corollary R1(i)). So, on that event and on {completed}, Ŝ⁺ = S₀ gives S₀ ∈ 𝓜, provided 𝒪 ⊇ {completed} (not
  checked here). Rule 11: this source enters only as an explicit hypothesis together with its conditional status.

**(β) Without beta-min.** π(𝒯) ≥ e^{−λt} is a **premise (P-STORE)** about the run. Nothing is proved. The output
does not certify it: π(𝒯) = Σ_𝒯 e^F / Z needs Z, which is not returned (`log_Z` is an estimate, [SAMP] LT-f, quoted in §7).
𝒯 ⊊ Ω (P27).

### (C-iii) HPM plug-in
Let a_n := ϱ_n^{1/2} = e^{−ct/2} and 𝔅_n := {S ∈ Ω : Π(B_n | S, D_n) > a_n}.
- **(a) Claim.** On 𝔊_n(t): π(𝔅_n) ≤ a_n.
  *Proof.* Lemma P6(b) with a = a_n > 0: π(𝔅_n) ≤ Π(B_n | D_n)/a_n ≤ ϱ_n/ϱ_n^{1/2} = a_n. ∎
- **(b) Claim (P-HIT; pathwise).** Fix a data set in 𝔊_n(t). Every completed run whose 𝓜 contains some S′ with
  π(S′) > a_n (**premise P-HIT**) satisfies Ŝ ∉ 𝔅_n, i.e. Π̂^H(B_n) ≤ a_n. Consequently
  P⊗({completed} ∩ P-HIT ∩ {Π̂^H(B_n) > a_n}) ≤ 3e^{−ct} + P*(I_n(t)ᶜ).
  P-HIT holds whenever S₀ ∈ 𝓜, δ_n < ½ and ϱ_n ≤ ¼ [SCR-1].
  *Proof.* By Corollary R1(i), Ŝ ranks first in 𝓜, so F(Ŝ) ≥ F(S′), hence π(Ŝ) ≥ π(S′) > a_n by (H-ID). Suppose Ŝ ∈ 𝔅_n.
  Then a_n < π(Ŝ) ≤ π(𝔅_n) ≤ a_n by (a): contradiction. So Π̂^H(B_n) = Π(B_n | Ŝ, D_n) ≤ a_n. The P⊗ bound is Lemma J
  plus (H-DIST1). Sufficiency: π(S₀) = 1 − δ_n > ½ ≥ ϱ_n^{1/2} = a_n when ϱ_n ≤ ¼. Take S′ = S₀. ∎
- **(c) Claim (with selection; oracle bound).** Under (H-DIST3), for n ≥ n₀ and 1 ≤ u ≤ n^{1−κ₀}:
  P⊗({completed} ∩ {Ŝ = S₀} ∩ {Π̂^H(d_H(f, f*) > C₃√(u/n)) > C₃e^{−c₃u}}) ≤ C₃e^{−c₃u} + P*((I³_n)ᶜ).
  On {completed} ∩ {S₀ ∈ 𝓜} ∩ {δ_n < ½} we have Ŝ = S₀ ((α-det)), so this event is covered.
  P⊗({completed} ∩ {Ŝ ≠ S₀}) → 0 is supplied by [SAMP] D-iv, LT-e, C-v or TR-d, each under its own premises (§7).
  *Proof.* On {completed} ∩ {Ŝ = S₀}, Π̂^H = Π(· | S = S₀, D_n), a function of the data alone. So the event is contained
  in {D_n : S₀ ∈ Ω, Π(d_H > C₃√(u/n) | S = S₀, D_n) > C₃e^{−c₃u}} =: G_u. By (H-DIST3), conditionally on any design in I³_n,
  P*(G_u | X) ≤ C₃e^{−c₃u}. Hence P*(G_u) ≤ E*[1_{I³_n} P*(G_u | X)] + P*((I³_n)ᶜ) ≤ C₃e^{−c₃u} + P*((I³_n)ᶜ). Conclude with
  Lemma J. ∎

### (C-iv) MPM plug-in
**Claim.** On {completed} ∩ {MPM = S₀} (MPM read in internal indices through ι⁻¹; S₀ ∈ Ω): Π̂^M = Π(· | S₀, D_n). Under
(H-DIST3) the bound of (C-iii)(c) holds with {MPM = S₀} in place of {Ŝ = S₀}. Moreover
P⊗({completed} ∩ {MPM ≠ S₀}) ≤ P⊗(𝒜 ∩ {MPM^{pot} ≠ S₀}), which → 0 under [SAMP] LT-e (P-CONC and NC_r for every r ≤ 4),
or C-v (1_𝒜δ̄ → 0), or TR-d (P-CONC and P-OVL∞).
*Proof.* The identity is the definition of Π̂^M. The bound is the proof of (C-iii)(c) word for word. The inclusion is
Lemma PC (ii) ([SAMP]: "the reported pip_primary, MPM and log Z are the functions of these island records given in §0")
together with {completed} ⊆ 𝒜. This is the "Consequence used downstream" of `W3-SAMP/lemmas/PC_completed.md:33-34`:
"P(completed ∩ {reported error}) ≤ P(𝒜 ∩ {potential error})". The limits are the quoted conclusions of LT-e, C-v and
TR-d (§7). ∎

### Honest label (checked item by item)
- (C-0), C-i°, (C-ii)(α-det), (C-iii)(a), (b): deterministic given the data and the run, or Lemma J plus (H-DIST1).
  **No sampler premise.**
- Delivery: discovery of S₀ ((α-disc): D-i, PC, P-OVL), P-STORE (premise), P-HIT (premise, or S₀ ∈ 𝓜 and δ_n < ½ and
  ϱ_n ≤ ¼), Ŝ = S₀ / MPM = S₀ ([SAMP] results). Each is a hypothesis, and each event is intersected with {completed}.
  P⊗(completed) → 1 is neither assumed nor claimed.
- Lemma J: a bad output event inside a bad data event has P⊗-probability at most P* of the data event, with no
  independence used.
- EX-A for floating point. No statement about a particle approximation: P31, no particle states are returned.

### Remarks
- **6.1 (Ŝ is the first entry of 𝒯).** Corollary R1(i) is unconditional on completed runs. It is a cheap consistency
  check on the output, and it is never used as evidence that π(𝒯) is large.
- **6.2 (calibration-evaluated models).** The calibration uses its own ledger with the same `eval` and
  `offer_stores` code (`cpp/v3_core.cpp:608-613`). Its exported inherited set is the union of its three stores
  (`:728-735`), and that set is offered to the final ledger (P20). Lemma R applied to the calibration ledger then
  shows: a unique F-maximiser over Ω that the calibration evaluated is in its top store, hence in 𝓜_inh, hence in 𝒯.
  (Code reading by this seat; not needed for any claim above.)
- **6.3 (floating point).** Outside EX-A, Lemma R still holds with F replaced by the computed scores, provided the
  scorer is deterministic per model (`cpp/v3_score.h:253-254` asserts this). The link e^{F} = Zπ is then approximate,
  and (C-i)'s constants would need an error term. Not attempted.
- **6.4 (dropped columns).** S₀ ⊆ [p_ret] by definition (STATEMENT §0). A true raw column that is constant in the
  sample is not a model coordinate. Theorem DIST-C is about S₀, not supp β*.
- **6.5 (s₀ > K).** Then S₀ ∉ Ω, δ_n = 1, and (α-det), (C-iii)(c), (C-iv) are vacuous. (α′) is trivial.
- **6.6 (DIST-2 version).** Replace B_n(t) by DIST-2's bad set {d_H > C√(tℓ_n/n)} and I_n(t) by 𝒟_n ∩ (E) ∩ (C). Every proof
  above goes through verbatim; Lemma P6(c) is used with ε² = C²tℓ_n/n.

## 7. Delivery statements: the [SAMP] premises used (quoted)

| DIST-C item | [SAMP] result used | its premises (quoted from `W3-SAMP/STATEMENT.md`) |
|---|---|---|
| (C-0), C-i°, (C-i), (α-det), (C-iii)(a)(b) | none | — (only (P⊗-1), (H-DIST1), (H-ID), EX-A) |
| (α-disc) | **Theorem D (D-i)** (`:99-100`): "island r's D_r π₀ draws are iid π₀; P(no π₀ draw of island r equals S₀ \| 𝓒) = (1 − π₀(S₀))^{D_r} (equality), so P(S₀ ∉ 𝓜_r \| 𝓒) ≤ (1 − π₀(S₀))^{D_r}" | "Under EX-A, H-U, START, KERNEL (used only through the control-flow clause of W1-N1 Lemma B (B-b)), CAL, SI, MEAS, given 𝓒 on 𝒜, for the potential run" (`:97-98`) |
| (α-disc) | **Lemma PC** (`:90-95`): "Under EX-A: on {completed}, (i) each final island's statistical record … and the set 𝓜_r of models it evaluated (incl. rejected proposals) equal the potential uninterrupted record computed from the same stream; … (iii) … the reported HPM Ŝ … is the hpm_better-maximum of the final ledger's offered set 𝓜 ⊆ Ω, which contains ∪_r 𝓜_r" | EX-A |
| (α-disc), limit | **P-OVL** (`:82-83`): "Q_D → ∞ in probability, where Q_D := D_r·π₀(S₀) on 𝒜 and Q_D := ∞ off 𝒜, D_r := N_e(1 + T + L + 4)" | interface premise; production sufficient form: "max(n, p)·log₂(n+1)·π₀(S₀) → ∞ in probability" (D-iv, `:104-105`) |
| (C-iii)(c): P(completed ∩ {Ŝ ≠ S₀}) → 0 | **D-iv** (`:104-105`) | "under P-MAP (or P-CONC) and P-OVL", plus D's premises above |
| same | **LT-e** (`:136-138`) | "under P-CONC and NC_r for every r ≤ 4" + "the N1 premises" (EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT; `:64-66`) |
| same | **C-v** (`:158-160`) | "if 1_𝒜·δ̄ → 0 in probability (⇔ 1_𝒜o₁ → 0 and P-START; implied by P-CONC + P-START)" + N1 premises |
| same | **TR-d** (`:170-171`) | "under P-CONC and P-OVL∞" + N1 premises |
| (C-iv): P(𝒜 ∩ {MPM ≠ S₀}) → 0 | LT-e / C-v / TR-d (same lines) + PC (ii) | as in the three rows above |
| (β) | LT-f (`:141-147`): "In general the output does not certify W_r ≥ η, since the top store (40p + 1 models) is a strict subset of Ω" | — (used only as the reason P-STORE stays a premise) |

Premise definitions: P-CONC "δ_n → 0 in probability" (`:73`); P-START "1_𝒜·o₀ → 0 in probability" (`:76`); P-MAP
"P(S† ≠ S₀) → 0" (`:78`); P-OVL∞ (`:79-81`); NC_r "lim_{η↓0} limsup_n P(𝒜 ∩ {W_r < η}) = 0" (`:84`). Statuses:
Theorems D, LT♯, C, TR and Lemma PC are "PROVED-CHECKED" (`W3-SAMP/lemmas/D_theorem.md:3`, `PC_completed.md:3`,
`LT_theorem.md:3`, `C_theorem.md:3`, `TR_theorem.md:3`). [CC] is "CODE-CHECKED". W1-N1 is "PROVED-CHECKED", under
START/KERNEL with inherited status "PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT"
(`W3-SAMP/STATEMENT.md:66-68`).

**Transfer of [SAMP]'s S₀ to W3-DIST's S₀.** [SAMP] fixes a model S₀ with s₀ ≤ K and states its finite-sample claims
conditionally on the data. W3-DIST's S₀ = supp θ* (retained columns) is design-measurable, hence fixed under that
conditioning. Its asymptotic premises (P-CONC, P-OVL, …) are read with this S₀ and δ_n = 1 − π(S₀). On {s₀ > K},
π₀(S₀) = 0, so P-OVL forces P(𝒜 ∩ {s₀ > K}) → 0. Nothing else changes.

## 8. Risks and open points
1. (H-ID) rests on [CC] CC2 ("CODE-CHECKED") and on locked T01. It is an explicit hypothesis here, not re-derived.
2. The commit identity of the code of record could not be verified without git. The SHA-256 values in §2 allow a
   later check.
3. Lemma M (b) relies on "only `eval` inserts into the final-run cache" (grep: the single `cache->insert` is at
   `cpp/v3_engine.h:93`) and on `E.cache = &cache` being the final run's own cache (`cpp/v3_core.cpp:409-411`). A
   future change that shares caches between calibration and final run would break (b). (C-ii)(α-det) would then need
   S₀ to be **offered**, not merely evaluated.
4. The RM2 alternative is cited, not verified (its output event 𝒪 versus {completed} is not checked).
5. Nothing here addresses P-STORE without beta-min (OPEN, as ROUTES §4 says).

## Amendments (lead, 2026-11-15, after the same-family pre-check; they are part of this file)
A-1 (RM2 route, §6 (C-ii) alternative). The alternative discovery route through W3-RM2 is **conditional and not used
by any proof here**: two links are unchecked (whether RM2's output event covers {completed}; whether its Ŝ⁺ is the
reported `hpm`). Every statement of this file that needs discovery uses W3-SAMP Theorem D (D-i) with P-OVL, or assumes
S₀ ∈ 𝓜 explicitly.
A-2 (Lemma M, proof (a), (b)). Completing the case list: a particle state created by resampling is a copy of a state
that entered the particle system through an `eval`, so it was offered when first scored; the only `eval` with
`emit = false` in the final run is the centre of the final local search, which is the current running best and was
offered when first scored (`cpp/v3_core.cpp:456`, `cpp/v3_engine.h:382`). The conclusion of Lemma M is unchanged.
A-3 (Lemma M, "∅ ∈ 𝓜"). This is used only as an illustration; it holds when there is at least one block table, or
because the first initial draw of island 1 is scored and offered. No proof step depends on it.
A-4 (Remark 6.3). `v3_score.h:253-254` is a code comment, cited as documentation of intent, not as an assertion of the
code's behaviour.
A-5 (SCR-1, restated). In (C-iii), "P-HIT is implied by S₀ ∈ 𝓜 and δ_n < ½" holds once e^{−ct} ≤ ¼, i.e. after enlarging n₀ so
that cM₀ log n₀ ≥ log 4.
A-6 (strengthening, not used). If S₀ lies inside one block of the start (for instance s₀ ≤ 1), then S₀ is in the block
tables and hence in 𝓜 on every completed run; no discovery premise is needed in that case.
A-7 (LS0 and aborted fits). The LS0 search runs only when enabled; an Rcpp error aborts the fit and returns no output.
Both are outside {completed} or do not change 𝓜's definition (LS0-scored models are offered to the same ledger).
A-8 (after the cross-family line check; corrects A-3). 𝓜 ≠ ∅ because the first initial draw of island 1 is scored and offered
(that draw need not be the empty model). If a block table exists, ∅ ∈ 𝓜 as well. Downstream (Corollary R1, Lemma W) only
**nonemptiness** of 𝓜 is used.
A-9 (pin P6 and non-completed runs). On a non-completed run the estimates are unavailable; explicit NA placeholders are
returned only when LS0 is enabled (`v3_run.R:143-148`, `v3_unavailable_estimates` is called only if `v31` is true). Completion
requires the final local search and, **when enabled**, LS0 (`cpp/v3_core.cpp:465`). No statement about completed runs changes.
A-10 (§0, positivity and finiteness of m(S)). Positivity follows from integrating a strictly positive likelihood against a
proper prior. Finiteness [corrected, D1-01: the first version paired the N-dimensional likelihood with the shape 0.01 of the
n-dimensional working model]: by the locked identification T01(i) ([P1] `thm:T01i`), m(S) = c·m^c(S) with a factor 0 < c < ∞ that
depends on (n, s_y) only, where m^c(S) is the marginal likelihood of the N-dimensional contrast model (N = n − 1), whose variance
prior is IG(a, b) with shape a = 0.51 (the extra half-power of v in T01(i)) and rate b = 0.01·s_y² > 0 on a completed run. The
contrast Gaussian likelihood is at most (2πv)^{−N/2}; integrating the proper coefficient prior and then
E_{IG(a,b)}[v^{−N/2}] = b^{−N/2}Γ(a + N/2)/Γ(a) gives m^c(S) ≤ (2π)^{−N/2}b^{−N/2}Γ(0.51 + N/2)/Γ(0.51) < ∞, hence m(S) < ∞. No new hypothesis.
