# W6-FIXREV2 — REPORT: applying A-REV2 to T03♯, Theorem A (refined T37), EXP′ and Lemma U

Run of 2026-11-02, branch `theory/W6-FIXREV2` (from `theory/campaign` @ af634b2). Deliverables: this file,
[STATEMENTS.md](STATEMENTS.md) (corrected paper-ready statements with the changed proofs), `scripts/` (fixed seeds),
`results/`. Every PROVED below is a **candidate** (unreviewed after this run, not adopted). A-REV2's "VERIFIED" is quoted
as a referee verdict, never as a status upgrade. No locked file, no source branch and no file outside
`theory_campaign/W6-FIXREV2/` was edited.

## 1. Headline

- **All ten A-REV2 findings in the task list are confirmed and fixed.** Every counterexample A-REV2 relies on was rebuilt
  with independent code and reproduces A-REV2's numbers to 10 digits (CEX-1, CEX-2, the exact-tie example, the C3
  counterexample, the T03 thresholds). I found **no error in A-REV2's mathematics**; I disagree on one wording point and add
  two qualifications (§3).
- **T03♯: PROVED (unchanged mathematics)**, restated with its exact quantifiers (sup_m P, deterministic cutoff, fixed g₀,
  convergence-only for E[1−π(S₀)], vacuous empty strong set). The finite-n disclosure is corrected: the proof's own
  thresholds begin at **n ≈ 2.1·10⁶ / 2.5·10⁶**, not 1.2·10⁵ (independent recomputation agrees with V03 to the integer).
- **Theorem A: PROVED**, now **exact-ties-aware**. TD′_P is defined through the engine's tie-broken map M; the strict
  event D_S is only sufficient (Lemma T). New **Lemma NT (PROVED)**: exact score ties between two models whose union has
  full column rank are P₀-null, so S37's "iff" holds almost surely under that non-degeneracy, but not deterministically.
  Lemma 0(b) is replaced by a delivery inclusion and an **exhaustive three-way failure partition (Prop. F, PROVED)**; both
  S37's posterior-miss inference and V37 R2's two-way dichotomy are special cases with COUNTEREXAMPLES.
- **EXP′ (Theorem 1): PROVED**; the limiting constant is **0.51/c_* = 4.08(M+2σ²)/σ²** (approached from above), not 0.52/c_*.
  Theorems 3/4 keep the deterministic chain and H3; growing leakage gives sufficiency only.
- **Lemma U: PROVED on an explicitly budgeted family (𝔉, 𝓗)**; the C3 upper bound stands; the matching lower bound
  needs μ ∈ span X_{W∖l} (COUNTEREXAMPLE otherwise); a weaker general floor C3-low′ is new (PROVED). **No downstream
  result in the audited branches relied on the false items**; four downstream texts need wording fixes (§2.4).

**Statements and proofs (protocol §§2–3):** the full corrected statements, with hypotheses, and the proofs of every
changed or new step are in [STATEMENTS.md](STATEMENTS.md) §§1–4; unchanged steps cite S03, S37, SEX and SU by section.

## 2. Change log

### 2.1 Main table (item | A-REV2 verdict | my check | fix | downstream)

| # | Item | A-REV2 | My check | Fix (where) | Downstream |
|---|---|---|---|---|---|
| 1 | S03 finite-n claim "deterministic steps hold from n ≈ 1.2·10⁵" | ERROR (confirms V03 R1) | **Confirmed.** Independent code (`t03_thresholds.py`, bracketed tail sums): δ_n ≤ ½ at 115,150 / 130,328; **q_n ≤ ½ at 2,116,048 / 2,457,025**; e^{2ε_n} ≤ 4 at 25,571,897 / 29,755,302; q_n = 5.53·10²² / 7.86·10²⁸ at n = 130,328; m♯ = K = 100 at (200, 500/1000), locked m_n = 201/215 | Disclosure sentence replaced (STATEMENTS §1.2 "Scope"); "not a universal n₀" | CARDS Card 1 (line 80) and W4-T38FULL STATEMENT Remark 4 already use 2×10⁶: **OK**. S03 REPORT §3/§5 still has the old text (source; flagged, not edited) |
| 2 | T03♯ quantifiers / scope (sup_m vs sup inside; deterministic ω_n; R_m for m < 0; empty strong set; fixed g₀; no O(r_n) for E[1−π]; E3 barrier only; posterior not discovery) | VERIFIED with these qualifications | Agree; all are presentation | Written into the statement (STATEMENTS §1) | CARDS Card 1 omits "g₀ fixed", the sup_m quantifier and "posterior, not reported HPM": add (wording) |
| 3 | S37 Lemma 0(b): "in particular on every posterior miss, no search delivers S₀" | ERROR | **Confirmed** (CEX-2 reproduced: F(S_c)−F(S₀) = −2.2863, F(S₀+x₃)−F(S₀) = +7.2110, path S_c → S₀+x₃ certified; E_LS true, posterior miss) | Lemma 0(b′) delivery inclusion with ties and the S_c = S₀ case (STATEMENTS §2.4) | W4-T38FULL Remark 3 uses only the inclusion: **OK**. CARDS Card 4 "0/541 … OPEN" consistent |
| 4 | V37 R2 two-way failure dichotomy | ERROR (omits inferior local maxima and capped searches) | **Confirmed.** CEX-1 from ∅: E_LS true, certified at ∅, F_post − F(S₀) = −20.99. A-REV2's production-table variant reproduced: blocks = groups, all table models below ∅, start mode **argmax π₀ = ∅**, search certifies ∅ (truth +19.92). Random designs: 13 fits fall outside the two-way split (3 certified, 10 at the cap) | **Prop. F**: I = E_LSᶜ, II = search miss (IIa certified inferior local max, IIb cap), III = explored competitor ≥ F(S₀). Exhaustive, PROVED | **CARDS Card 4 lines 267–269 quote R2 verbatim: must be replaced by Prop. F.** W4-T38FULL cites "repaired in R2" for the inclusion only: OK, cite Lemma 0(b′) |
| 5 | S37 A5(a): literal strict TD ⇒ TD′_P (no POS) | ERROR (confirmed false); POS repair VERIFIED | **Confirmed** (literal TD(0,0) strict: 0 failing clauses; best gain at ∅ = −2.2978; π(S₀) = 0.8645; search certifies ∅) | A5 with POS (STATEMENTS §2.3); original T37(i) false at d = 0 too | CARDS Card 4 and W4-T38FULL b1.3 already carry POS: **OK** |
| 6 | S37 definition "TD′_P ⟺ (L) ∧ ⋂ D_S" | ERROR (strict separation sufficient, not necessary, with exact ties) | **Confirmed** (duplicate-column example: TD′_P(R₀) holds, D_∅ fails; gains 7.6308489425, −0.0018640607). Logic check on 6,900 states: D_S^lex ⟺ (M(S) progress) 0 violations; D_S ⇒ D_S^lex 0 violations; all 325 "lex but not strict" states come from duplicate-column designs, none from the others | **Lemma T** (exact equivalence via D_S^lex; strict D_S sufficient) + **Lemma NT** (ties null under G when the union has full rank, so the "iff" holds a.s. there) | **W3-PGD defines TD′_P := (L) ∧ ⋂ D_S** (strict). Its positive results prove this stronger event and imply the tie-aware TD′_P: **survive**. Its negative results (Prop. P4, C-LD) exhibit *strict* reversals (a non-progress neighbour, or S itself, strictly beats every progress neighbour), which refute the tie-aware TD′_P too: **survive**. Its sentence "exact ties have probability 0 under G" is not justified in general (false with duplicates); justified under Lemma NT's non-degeneracy; not needed on its event (keep "up to exact ties"). W4-T38FULL Lemma LS-score and W3-PXN P6 use strict D_S as a sufficient condition: **OK** (could be weakened to D_S^lex). CARDS defines TD′_P through M: **OK** |
| 7 | "Weakest among at-most-Φ-move conditions" prose | ERROR | **Confirmed**; independent PHI-REACH example: S₀ = {0,1,2}, path {2,5} → {1,5} → {0,1,5} → {0,1,2}, Φ = 3, 3 moves, first move neutral | Prose replaced; "weakest" withdrawn (STATEMENTS §2.5) | W3-PGD §6 "What is weakest" makes a different, supported claim (PGD sharp up to the boundary via Prop. P4): OK. CARDS: no "weakest": OK |
| 8 | SEX/SU limit "κ → 0.52/c_*" (4.16 multiplier) | ERROR (minor) | **Confirmed**: κ_EXP(n) ↓ 0.51/c_* strictly from above (σ² = M = φ₀² = 1: 12.2532, 12.2413, 12.24001, 12.240000013 at n = 10³, 10⁴, 10⁶, 10⁹); "≤ 0.52/c_*" holds from n = 56 there | 0.51/c_* = 4.08(M+2σ²)/σ² (STATEMENTS §3.1, §4.1) | W1-EXP REPORT headline 1 "≤ 0.52/c_* + O(1/n)" (valid but should read 0.51/c_* + O(1/n)); W2-PREM PROOF §2 and REPORT ("→ 4.16"). **New downstream finding:** W3-PXN Lemma U (U1) asserts ν(1.02 + 1/(nφ₀²))/(c_*n) ≤ 1; false, since c_* ≤ 1/16 gives ≥ 8.16. Only the constant κ₂ changes (κ₂ ≥ 0.51/c_* + o(1)); every PXN conclusion uses κ₂ only as an O(1) constant: **survives** |
| 9 | SU Lemma U: "and every V of size ≤ k used below" | GAP (no cardinality budget for the extra sets) | **Confirmed** (p = n−1 orthogonal singletons: max projected energy > 0.5 log n in 100% of draws, n = 10³…10⁶) | **Budgeted Lemma U(𝔉, 𝓗)**: 𝓗 contains every set used, |𝓗| ≤ C_H n^{a_H}, L > 4a_H; explicit failure probability (STATEMENTS §4.1) | W2-PREM §3 uses 𝔉_k (all sets of size ≤ k = s₀+a+2): extra quantifier vacuous, **covered**. W4-T38FULL §4.2 step 2 (Lemma U "unverified"): its use is an *upper* (C3-up) bound at S° with δ = 0; the budgeted lemma covers it (that sketch's status is unchanged). W3-PXN's own Lemma U budgets its family correctly (L > 4A(s₀+3) over all sets of size ≤ s₀+2): OK. W3-PGD's "Lemma U" is a different superset lemma (upper bound, μ ∈ col X_A): OK |
| 10 | SU C3 matching lower bound under δ = 0 alone | ERROR (needs μ ∈ span X_T) | **Confirmed** exactly: κ_n = 12.2400132448, ϑ′_n = 0.7028313369, actual 16.2502645682 < claimed 19.5571554183, with E1–E4 checked | **C3-low** under μ ∈ span X_{W∖l} (PROVED); **C3-low′** (new, PROVED) under δ = 0 alone with exponent σ²Z²/(2C_R); C3-up unchanged | The only use of the lower bound found is W2-PREM §3.4 (equicorrelated-null COUNTEREXAMPLE) at W = S₀ + m*, a superset of S₀: **covered by C3-low; survives.** W2-PREM §6.3 (TL♯) uses only C3-up at non-supersets: OK (A-REV2 agrees). W3-PXN (L) and W3-PGD C-LD use their own lower-direction arguments at supersets of S₀: OK |
| 11 | VEX random-design / actual-packing extensions of EXP′ | GAP (keep SKETCH) | Agree | Kept: SEX §1.5 and VEX R3 PROOF SKETCH; B ≥ 2g GAP; κ₁₇ ≥ 0.1 (not 0.15); δ_{∅,j_b} not exactly normal (second moment suffices) (STATEMENTS §3.4) | CARDS Card 3 already lists in-sample favourability for iid S3/S4/S6 as a GAP: OK. W3-PXN's LH-iid results use g ≤ B < 2g (fixed-partition surrogate regime A-REV2 accepts); they were not reviewed by A-REV2: unchanged status |

### 2.2 Further A-REV2 items applied (from its verdict table and §§3–6)

| Item | A-REV2 | Fix | Downstream |
|---|---|---|---|
| SEX Theorem 4 "masking persists iff η < 1/2.02"; VEX R4 "p^{−c} alone forces → 0 whatever η" | ERROR / not justified | Sufficiency statement: log π₀(S₀) ≤ −c log p − c(½ − 1.01η) log n + O_P(√log n); vanishing if η < 1/2.02, or if a + ½ − 1.01η > 0 when p ≥ n^a (STATEMENTS §3.3) | CARDS Card 3 (iv): no "iff": OK |
| Theorem 3 quantifier boundary (deterministic chain) | VERIFIED with boundary | H1-det stated; no response-selected trajectories | CARDS Card 3 (iv) says "deterministic addition chain": OK. W4-T38FULL uses SEX Thm 5(b) (deterministic hub chain on LH): OK |
| Theorem 4 needs H3 (normalised start mass) | VERIFIED with H3 explicit | H3 kept as a hypothesis | CARDS Card 3 states H3: OK |
| Theorem B: response-selected centre, 2^{Φ(S_c)} | VERIFIED inclusions; union must be over data-independent Lat(𝒞) | Stated (STATEMENTS §2.6) | CARDS Card 4 already says "2^{Φ(S_c)} for a fixed centre": OK |
| V37 R4 printed tail p·P(|Z| ≥ u) | ERROR | p·P(|Z| ≥ t) with the original t (STATEMENTS §2.6) | W3-PGD's (★) is derived by its own computation, not from R4's display: OK |
| A4 necessity quantifier (all starts vs one centre) | VERIFIED with quantifier | A4(i)/(ii)/(iii) separated (STATEMENTS §2.3) | none found |
| (A3) "ℓ ≥ a + d needed" | — (V37 R3) | "iff ℓ ≥ τ(S_c)" under TD′_P; ℓ ≥ a + d suffices | CARDS Card 4 already says "ℓ ≥ τ(S_c) is the exact need": OK |
| T03 anchoring wording (V03 R2, Lemma A1) | VERIFIED | Equivalent unanchored forms in the statement | CARDS Card 1 "Risk" already says anchoring is cosmetic: OK |

### 2.3 New items proved in this run (all candidates)

1. **Lemma T** (tie-aware equivalence; PROVED; formalises A-REV2 §4.3) — STATEMENTS §2.2.
2. **Lemma NT** (exact ties are P₀-null when |T′|+|T″| < n−1 and λ_min(G_{T′∪T″}) > 0; PROVED) and Corollary NT
   (S37's "iff" holds P₀-a.s. under that non-degeneracy) — STATEMENTS §2.2.
3. **(A3) "iff ℓ ≥ τ(S_c)"** under TD′_P (PROVED) — STATEMENTS §2.3.
4. **Lemma 0(b′)** with the tie case and the S_c = S₀ case; **Prop. F** (three-way exhaustive failure partition, with
   posterior miss ⟺ I ∪ III and search miss ⟺ II; PROVED) — STATEMENTS §2.4.
5. **Budgeted Lemma U(𝔉, 𝓗)** with an explicit failure probability (PROVED), **C3-low** (PROVED, A-REV2's repair written
   out with constants) and **C3-low′** (PROVED, new) — STATEMENTS §4.

### 2.4 Downstream: what must change in other branches (for HQ; not edited here)

| File | Location | Required change | Severity |
|---|---|---|---|
| F-REFINE `CARDS.md` | Card 4, "(Lemma 0, repaired R2)" bullet | Replace the two-way split by Prop. F (I/II/III); keep the delivery inclusion | wording, but it currently states a false dichotomy |
| F-REFINE `CARDS.md` | Card 1, refined statement | Add "g₀ fixed", "sup_m P₀(Θ♯ > L)", "posterior/global HPM, not reported-HPM discovery"; for (iii) "convergence only" | wording |
| W3-PGD `PROOF.md` | §0 definition of TD′_P; Theorem W last sentence | Call (L) ∧ ⋂ D_S "TD′_P^strict" (a sufficient event); replace "exact ties have probability 0 under G" by "up to exact ties" or assume Lemma NT's non-degeneracy | wording; no result changes |
| W1-EXP `REPORT.md`, W2-PREM `PROOF.md` §2 / `REPORT.md` | κ limit | 0.51/c_* (4.08 multiplier) | constant |
| W3-PXN `PROOF.md` | §9.1 (U1) "≤ 1" | Replace by "≤ ν(1.02 + 1/(nφ₀²))/(c_*n) → 0.51/c_*"; κ₂ := (s₀+2)(1+φ₀^{−2})/(2φ₀²(n−1)) + ν(1.02 + 1/(nφ₀²))/(c_*n) | constant; no conclusion changes |
| W2-PREM `PROOF.md` §2 | Lemma U statement; C3 parenthesis | Budgeted statement; lower bound only under μ ∈ span X_{W∖l} | statement-level; no use breaks |
| W1-T03R `REPORT.md` | headline 4, §3, §5 | "≈ 1.2·10⁵" → "≈ 2·10⁶" (V03 R1) | disclosure |
| W2-T26 | Theorem B | none required (uses locked T03 and strict EXP′ ρ_n = O_P(1); no constant, no T37 item). Optional: T03♯ can replace locked T03 with weaker SE | none |

## 3. Where I disagree with or qualify A-REV2

1. **"The case where the initial centre already is the truth is trivial success" (A-REV2 §2 row "Lemma 0(a), (c)").**
   Disagree with the wording. If S_c = S₀, no *new delivery* is needed, but the final search from S₀ moves away whenever
   M(S₀) ≠ ⊥ (S₀ is not a local maximum of the neighbourhood), and then Ŝ ≠ S₀. Concrete: in the CEX-2 design
   F(S₀ + x₃) − F(S₀) = 7.21 > 0, so a search started at S₀ moves to S₀ + x₃ and the fit fails (category I). The correct
   statement is Lemma 0(b′): with S_c = S₀ the search certifies S₀ iff (L) holds at S₀. A-REV2's §4.2 text ("success needs
   no new-delivery event") is right; only the table's "trivial success" overstates it.
2. **Exact ties (A-REV2 §4.3).** Agree that the deterministic "iff" is false. Qualification: the failure needs a structural
   tie. By Lemma NT, when the two tied models have a jointly full-rank union and |T′| + |T″| < n − 1, ties are P₀-null, so
   under G and such non-degeneracy S37's equivalence holds almost surely. A-REV2's example uses an exact duplicate column,
   which violates this. The tie-aware definition (D_S^lex) is still the right one for a deterministic theorem.
3. **C3 lower bound (A-REV2 §6.3).** Agree it is an ERROR on the stated event. Qualification on magnitude: in A-REV2's own
   family the violation needs Z² ≳ 49 (because κ is loose), i.e. probability ≈ 2·10⁻¹² per comparison; the ERROR is a
   statement-level one with no downstream use affected. A general (weak) floor survives as C3-low′.
4. **Everything else:** agree, after independent reproduction. I found no step in A-REV2's derivations that fails.

## 4. Evidence (all scripts in `scripts/`, outputs in `results/`; core written from 00_COMMON and `v3_engine.h`)

| Script | Seed | What it showed |
|---|---|---|
| `core.py` | — | Exact score from (G, z, yᵀy, n); M, best(·) with the engine's lex tie rule; production local search including the cap's extra scan; D_S, D_S^lex, TD′_P via M |
| `t37_checks.py` → `t37_checks.txt/json` | 1, 3, 20261102 | CEX-1, CEX-2, tie example, inferior local maximum: all A-REV2 numbers reproduced to 10 digits. 300 random designs (p = 7; one third with a duplicate column), 6,900 states of R_{2,1}: Lemma T(a) 0 violations, Lemma T(b) 0 violations, 325 lex-not-strict states (all in duplicate designs). 1,200 simulated fits: categories I 498, IIa 3, IIb 10, III 558, success 131; 13 fits outside V37's two-way split; 0 partition violations |
| `t37_extra.py` → `t37_extra.txt/json` | 20261102 | A-REV2's p = 20, B = 4 suppressor-hub variant (exact Gram; noise ⟂ columns is my choice): blocks = groups (cross distance 0.05 > within 0.01), max table-model gain over ∅ −2.83, start mode ∅, truth +19.92, search certifies ∅. PHI-REACH-without-TD′_P example (§2.1 row 7) |
| `lemmaU_checks.py` → `lemmaU_checks.txt/json` | 20261102 | κ limit 0.51/c (decreasing from above; 12.24 not 12.48). C3 counterexample exact (E1–E4 verified). Repaired links: RSS_T ≤ ‖Cε‖² when μ ∈ span X_T (400 cases) and RSS_T ≤ ‖Y‖² always (1,400 cases), 0 violations. Quantifier counterexample: 100% failure at n = 10³…10⁶. Remainder identity: max error 2.1·10⁻¹³ over 9,280 pairs, max |R| = 0.97, 0 violations of the deterministic bound |
| `t03_thresholds.py` → `t03_thresholds.txt` | none | Thresholds and point values above; matches V03 R1 and A-REV2 §3.5 exactly |

Small-p checks are component-law checks; they do not show SMC discovery, asymptotic rates, or anything about n = 200.

## 5. What fails and why (routes tried)

- **A deterministic "iff" between TD′_P and strict D_S.** Impossible (Lemma T(d)); the best available is a.s. under
  non-degeneracy (Lemma NT). Lemma NT does not cover pairs with |T′| + |T″| ≥ n − 1 (then a nonzero multiple of P_C is
  not excluded by rank); this is irrelevant for bounded model sizes.
- **A sharp general C3 floor (coefficient σ²/(2v_T)).** Needs a uniform event |RSS_U − (n−1)v_U| ≤ n^{3/4} over 𝓗 (as in
  SEX Theorem 6, Step 0 (ii)). I did not add it to Lemma U; C3-low′ (coefficient σ²/(2C_R)) is what follows from (E4) alone.
- **Upgrading "Ŝ = S₀ up to exact ties" to "exactly".** On TD′_P the scan at the last pre-S₀ state can contain a model tied
  with S₀ that is not a neighbour of S₀, so (L) does not exclude it; Lemma NT excludes it a.s. only under non-degeneracy
  on that pair's union. Left as "up to exact ties".

## 6. Needs escalation (independent check by another family)

1. **Lemma NT** (new): the step "a quadratic form constant on the sphere of range(C) is a multiple of P_C there" and the
   rank argument; also whether the HPM tie rule (size, then lexicographic) interacts with any downstream use.
2. **Prop. F's link to the data**: it is exhaustive by construction, but its use on the benchmark requires (i) that the
   final local search is the last scoring event (V37 cites `v3_core.cpp:447`; A-REV2 agrees) and (ii) the per-fit F_pre.
   The extraction F(S₀) − F_pre per failed fit is the one missing data item (OPEN); F_pre is already in the run output
   as `hpm_before$F` (`v3_core.cpp`, recorded just before the final local search, which I confirmed is the last scoring
   call of a completed fit), so only F(S₀) must be scored per failed fit.
3. **C3-low′** (new) and the budgeted Lemma U's failure-probability expression (constants only).

## 7. Outside scope

- W3-PGD's REPORT.md is still a stub ("DRAFT"); CARDS lists Theorem W as unverified. Lemma T makes no change to Theorem W's
  conclusions, but W3-PGD needs its own referee.
- W3-PXN (LH-iid, p ≫ n) was not reviewed by A-REV2; the only A-REV2-related defect I found there is the constant in (U1).
- W2-T26 still cites locked T03; switching to T03♯ would weaken its SE premise at no cost.
- S37's REPORT headline still says the 0/541 repair count is "forced by monotonicity"; Prop. F shows this needs F_pre per
  fit (consistent with V37 and CARDS, which mark it OPEN).

## 8. Confidence card

| Target | Refined statement (STATEMENTS) | True | Provable at reasonable cost | Crux | Method change |
|---|---|---|---|---|---|
| T03♯ (T01–T03 refined) | §1: G, R, SE_λ(j₀), SE_w(m♯_n; g₀) with g₀ fixed, BM-∞/BM(c) ⇒ 1 − π(S₀) = O_P(r_n), PIP/MPM/HPM consequences; T02(i♯) with sup_m quantifier | high (0.95) | done (candidate PROVED; two independent verifications) | none left; relevance at n = 200 nil (thresholds ≈ 2·10⁶, BM constant 43× short) | no |
| Theorem A (refined T37(i)), tie-aware | §2: TD′ via M; Lemma T (TD′_P ⟺ (L) ∧ ⋂ D_S^lex); A1–A4 with quantifiers; A3 iff ℓ ≥ τ; A5 with POS; Lemma 0(b′); Prop. F | high (0.97) | done (elementary; exhaustively checked) | none mathematical; the data split I vs III is OPEN (needs F_pre per fit) | no |
| Lemma NT / a.s. "iff" | §2.2 | high (0.9) | done; needs an independent check | rank of A_{T′} − kA_{T″} vs n − 1 | no |
| EXP′ (Theorem 1) + Cor. R1; Theorems 3/4 | §3: fixed X, deterministic blocks, SE-blk; κ ↓ 0.51/c_*; deterministic chain; H3 explicit; growing leakage sufficiency only | high (0.96) | done for fixed design; random partitions with B ≥ 2g: GAP, not cheap | partition–noise decoupling for B ≥ 2g | possibly (held-out partition) for the GAP only |
| Lemma U (budgeted) | §4: (U), E1–E4 on (𝔉, 𝓗) with |𝓗| ≤ C_H n^{a_H}, L > 4a_H; C3-up; C3-low under μ ∈ span X_{W∖l}; C3-low′ | high (0.96) | done | none; sharp general floor would need an extra uniform RSS event | no |
