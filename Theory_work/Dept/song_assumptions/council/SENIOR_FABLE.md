# SENIOR REVIEW — seat FABLE (Stage 1: completeness, generality, naturalness)

Fable 5.2, fresh judge, 2026-11-27. Package v1.3 (after Council R2).

**What I read and ran.**
- In full: the four package files; the delivered statements in `.rc_tmp/song/ms/` (`asm:dist`, `thm:dist`, `prop:dist`, `thm:post-random`, `asm:margin`, `asm:omitted`, `rem:sharp`); SL main text pp. 950–958 (sparsity (3)/(4), prior §2.1.1, Thms 1–4, Conditions 1–5, Cors 1–2).
- Two small checks, no fits and no outcome data, under 1 CPU-minute: `.rc_tmp/senior_fable/leak_check.py` (population) and `lemmaW_check.py` (one simulated design).
- My recomputation of the exact all-deletion κ_n on S1 gives 2.505–2.771 at SNR 2, matching the package.
- Not done: a line-by-line re-derivation of the TS-b proof path. My findings there are at statement level.

**Disclosure.** I derived proposal P-U (§2) from the definition of w_Dm. I then found that it matches, in substance, MARGIN\* of the advisor file `advisors/FABLE_R1.md`, written by the same model family as this seat. Astra's seat is the independent check on it.

**Verdict.** The SL map is complete in coverage and the package is honest about its limits. Eight of the twelve assumptions are general and natural as stated, or need only a cosmetic restatement. The central one, A-MARGIN-U, is not: its hypothesis contains a random, design-conditional quantity, a constant fixed by a proof step, and a rival range set by an inexplicit constant, and its form was chosen to cover S1. A population-only replacement exists, costs little, and is a sufficient condition for the current statement.

---

## 1. Completeness findings

**C-1. BLOCKER for the owner's naturalness mandate (not a mathematical error). A-MARGIN-U has no population-level form between the worst case and "measured on our designs".**
- Location: THEOREM_DEFINITIONS §4.2 (TS-b); ASSUMPTIONS §1 row D4, §2 A-MARGIN-U, §3.3 step 3.
- What is missing: the hypothesis uses w_Dm(X), a functional of the observed design, and is "stated on a design event of probability 1 − o(1)". The only population routes offered are the combinatorial bound √(2 log C(p−s0, m)), which is the worst case, or "a deterministic upper bound holding with design probability 1 − o(1)", which is a lemma left to the reader. No condition on Σ and β* is given that implies a small width.
- Why it matters: a referee will read this as an assumption that a random quantity is small, verified only by Monte Carlo on AR(1) designs (E9). ASSUMPTIONS §1 row D4 records that the form was chosen for "covering the S1 boundary signals". That is the reverse-engineered look the owner wants to avoid.
- Fix: add **Lemma W** and restate the assumption through it (P-U in §2). For B = S0∖D (or any fixed B) and rivals S = B ∪ N, write ϑ̂_S := 1 − R̂(S)/R̂(B), the share of the unexplained signal that the added nulls absorb in sample.
  - (W1) ⟨v_S, v_B⟩ = √(1 − ϑ̂_S), so ‖v_S − v_B‖² ≤ 2ϑ̂_S. Since E⟨v_B, g⟩ = 0, w_Dm(X) ≤ 2·√(max_N ϑ̂_S · log C(p−s0, m)).
  - (W2) On the sparse-isometry event of step 4, ϑ̂_S ≤ ϑ_S + 2δ_n, where ϑ_S is the population share 1 − R_n(S)/R_n(B) and δ_n ≍ √((s0+m)·log p/n).
  - Both are two-line arguments. Under A-DIM, δ_n·log p → 0, so a small population leakage gives a vanishing width.
  - Numerical sanity check (one simulated S1 design, n = p = 500): w = 0.13–0.15 against the W1 bound 0.62–0.71 for nulls outside S0's five nearest neighbours; w = 0.28 against 2.34 when the adjacent null is included (leakage 0.22).

**C-2. SUBSTANTIVE. S1 numbers sit inside statements.**
- Location: THEOREM_DEFINITIONS §4.2, inside the TS-b statement ("At S1's sizes the implied C ≍ (s0+1)²…", "on S1's AR(1) designs the estimated width is 0.1–0.6") and in its plain-English bullets; ASSUMPTIONS §2 A-MARGIN-U, the "Statement" block (S1 (500, 500) numbers in the worst-case bullet and in the class-restriction paragraph).
- Why it matters: it breaks the owner's rule that S1/S2 appear only as verification evidence, and it makes the assumption read as fitted.
- Fix: move every S1/S2 number to Defence (b) and to SIMULATION_DATA_ANALYSIS. Statements keep symbols only.

**C-3. SUBSTANTIVE. Proof constants and the level M set the range of the assumptions.**
- Location: ASSUMPTIONS header (q_n(M) = min{p, ⌈C_q M log n⌉}, C_q = 2(s(A+2)+4)/log 2); A-SUBG, A-NEC (window q_n(M)); A-MARGIN-H and A-MARGIN-U (J = ⌊s + C_s·M⌋, with C_s "a constant" from prop:dist(i) and M ≥ M₀); A-MARGIN-U (constant C "for which the containing-model bound holds with a tight multiplier").
- What is missing: numerical values, or a statement that avoids them. As written, the set of rivals that A-MARGIN-U constrains cannot be evaluated: J depends on C_s and M₀, which the package does not give. E9/E9b stop at m ≤ 2 for cost reasons, while the text says every m ≤ J is active at S1's sizes.
- Fix: (i) windows "at most c·log n predictors, for every fixed c"; (ii) rival range m ≤ m̄ := ⌈(2A+1)s⌉ + 1, the explicit range of the delivered `asm:margin`(b), which the containing-model credit justifies asymptotically; (iii) drop C and the "B_Dm > 0" class restriction from the statement and keep them as a remark in the proof path.

**C-4. SUBSTANTIVE. Three SL counterparts are absent from the map or not used in the defence.**
- (a) **SL sparsity (3), p. 950: lim Σ_j |β*_j| < ∞.** With standardised predictors and fixed σ*, this bounds every |β*_j|·sd(x_j)/σ*, so it implies A-BS. The package defends A-BS only with YWJ and SC11, and the manuscript says item (e) "has no direct counterpart". SL (3) is the direct counterpart, and under (4) with fixed β* the same bound is implicit. Add it to §3 of THEOREM_DEFINITIONS and to A-BS Defence (a).
- (b) **SL p. 951 remark on removing the size cap** ("this constraint can be removed by imposing … π(|ξ| > r̄_n) → 0 with an appropriate rate", citing Jiang 2007 §7). PRECEDENTS_NEW C7 verifies Jiang's condition (38), π(|γ| > r̄_n) ≤ e^{−4nε_n²}. With the BB(1, p) size tail ≈ 2^{−k} this gives r̄_n ≍ nε_n²/log 2 = M log n/log 2, which is the order and the 1/log 2 factor of our window q_n(M). So q_n is SL's r̄_n under SL's own remark. The map row SL-1/SL-2 says only that SL's (9)–(10) "would fail at r̄_n ≍ n". Using the remark answers "your K = n/2 violates SL's conditions" and gives q_n a natural meaning (the effective cap implied by the prior).
- (c) **SL Condition 3, Gaussian sufficient form (pp. 955–956):** "all predictors are identifiable if ch₁{var(x)} ≻ ε_n²". That is a vanishing population eigenvalue floor, of order above log n/n in our radius. It is the closest SL precedent in genre for A-NEC (floor c_ψ/n, lower still), yet A-NEC's defence cites only SL (26), NH14, SBJ, BRT09. Row SL-5 notes the vanishing floor but maps it to A-MARGIN-H only. Add it to A-NEC Defence (a).

**C-5. SUBSTANTIVE. The TM tier has an unlabelled assumption: sparsity of the pseudo-true vector.**
- Location: THEOREM_DEFINITIONS §4.3 (TM-a, TM-b: "A-SPARSE … for the candidate problem"); the dossier has no question on it.
- What is missing: sparsity of β^C = β*_C + Σ_CC⁻¹Σ_CO β*_O does not follow from sparsity of β*. It holds under local dependence (Gaussian AR(1): an omitted predictor projects on its two neighbours) and fails under pervasive factors (the projection is dense). A referee will ask this first for TM.
- Fix: give it a label (A-SPARSE-C: |supp β^C| ≤ s_C fixed), a "holds / fails" pair of examples, and name TD-A (approximate sparsity) as the relaxation for TM-a.

**C-6. SUBSTANTIVE. Worked cases promised but absent.**
- Location: dossier, A-MARGIN-U item 6 ("We also give worked cases: orthogonal, AR(1), block, equicorrelated"). They are in none of the four files.
- Why it matters: closed forms on standard design families are how a general condition is shown to be natural. Minimal content: R_n(S0∖D), κ_n and the leakage of P-U in each family. For example, one-step AR(1) leakage is ρ²/(1+ρ²) and decays as ρ^{2k} with distance k; for equicorrelation ρ and |B| retained predictors a single null has leakage ρ²/(1+|B|ρ)².

**C-7. MINOR. The converse is stated under more than it uses.**
- Location: THEOREM_DEFINITIONS §4.2 ("Under the same regularity"). The pairwise-odds argument uses A-GL, isometry and A-NEC on S0, and A-BS for the ridge term. Stating the converse under that minimal set makes the sharpness claim stronger.

**C-8. MINOR. Almost-sure versions.** TD-as and TS-a (a.s.) follow from Borel–Cantelli under any coupling of the D_n, so "fix the truth as a sequence" is needed only for TM-a0.

---

## 2. Generality and naturalness, one row per assumption

| assumption | natural as stated? | artificial or S1/S2-tied element | proposed general statement | cost |
|---|---|---|---|---|
| A-GL | yes | none | keep | none |
| A-SPARSE | yes | none | keep; growth of s stays a remark | none |
| A-DIM | yes | none | keep | none |
| A-DIM′ | needs re-expression | level M and c_dim inside the condition | "log p = o(√n)" as the conjecture's regime; the product form is a proof budget | none (conjecture only) |
| A-SUBG | needs re-expression | window q_n(M) with proof constant C_q; tied to the level M | **ψ₂–L₂ equivalence on sparse directions:** every predictor has positive variance and, for one L ≥ 1, every fixed c > 0 and all large n, E exp(λuᵀζ) ≤ exp(L²λ²Var(uᵀζ)/2) for all λ and all u with at most c·log n nonzero entries. State the standard sufficient models first: Gaussian rows; x = m + Aη with independent sub-Gaussian η | formally stronger (every c); no named design family is lost; S1/S2 Gaussian, satisfied |
| A-NEC | needs re-expression | "c_ψ/n" reads as a prior artefact; window q_n(M) | **Vanishing sparse-eigenvalue floor:** φ_n²(ℓ) := min_{\|T\|≤ℓ} λ_min(Corr(x_T)) satisfies n·φ_n²(c·log n) ≥ c_ψ for every fixed c and large n: "the sparse eigenvalue may vanish, but no faster than the ridge scale τ/n (τ = 1 as coded)". Cite SL Cond. 3's Gaussian form and SL's own ridge c_n ∝ 1/n (p. 953) | none in strength; S1/S2 satisfied (n × floor 8.8–250) |
| A-BS | yes | none | keep, as "bounded standardised effects"; add SL (3) as counterpart. At fixed s it implies Var(xᵀβ*) ≤ s²b̄²σ*² | none |
| A-BS′ | replace (b) | b̄_n with s·b̄_n² = o(n) is a proof budget | target form: Var(xᵀβ*) ≤ M_μσ*² only ("population R² bounded away from one") | needs the size lemma re-proved; until then A-BS stays |
| A-MARGIN-H | needs re-expression | inexplicit C_H(L), level M, J via C_s, min(K, J) | **Diverging ratio:** for the predictor j and every fixed m̄, inf{R_n(S) : j ∉ S, \|S\| ≤ s + m̄}/(σ*²·log n) → ∞. Conclusion for every fixed M | slightly stronger than a large fixed constant; same form as the delivered `asm:omitted`(c) and Luo–Chen; S1 is outside either way (its ratio is constant in n), as the package already says |
| A-MARGIN-U | **replace the statement** (keep the current form as a lemma-level refinement) | w_Dm(X) random and sample-defined; constant C from a proof step; classes "B_Dm > 0"; J via C_s; three slack parameters δ, γ, t_n; form chosen to cover S1 (D4) | **P-U, below** | see below |
| A-MIS(iii) | needs re-expression | stated on the derived residual u, which hides what is assumed about the omitted predictors; "Σ_CC nonsingular" is stronger than the rest of the set | **Gaussian-linear omitted signal:** with O the omitted true predictors, x_Oᵀβ*_O = a + x_Cᵀγ + e, e ~ N(0, τ²) independent of x_C. Then β^C = β*_C + γ and σ_C² = σ*² + τ². Uniqueness of β^C via "an s_C-sparse representation" plus A-NEC, not full rank. Add A-SPARSE-C (C-5). Present TM-a and TM-b as corollaries of TD and TS-b | none: equivalent to the current statement (Cramér's decomposition theorem); the scope becomes plain |
| A-MOM | yes | "p_C ≥ 2" is a code fact, acceptable | keep | none |

**P-U: proposed general form of A-MARGIN-U (population quantities only).** Define the price for any model prior π and slab scale g by Pr_n(d) := max over D ⊆ S0 with |D| = d of log[π(S0)/π(S0∖D)] + (d/2)·log(1+g); for BB(1, p) and g = n this is the package's Pr_n(d). Let m̄ := ⌈(2A+1)s⌉ + 1. There is η > 0 such that, for all large n:
- **(U1) Deletions.** R_n(S0∖D) ≥ 2(1+η)·σ*²·Pr_n(|D|) for every nonempty D ⊆ S0. This is κ_n ≥ 1 + η.
- **(U2) Substitutions, limited leakage.** There are sets Q_n ⊇ S0 with log|Q_n| = o(log n) and numbers ϑ_n with ϑ_n·log p → 0 such that, for every B ⊆ Q_n with B ⊉ S0 and |B∖S0| ≤ m̄:
  - (a) R_n(B) ≥ 2(1+η)·σ*²·Pr_n(|S0∖B|);
  - (b) R_n(B ∪ N) ≥ (1 − ϑ_n)·R_n(B) for every N outside Q_n with |N| ≤ m̄.
- **(U2′) Substitutions, no structure assumed (fallback).** For every S ⊉ S0 with 1 ≤ m ≤ m̄ added nulls, √(R_n(S)/σ*²) ≥ (1+η)·[√(2Pr_n(d)) + √(2 log C(p−s0, m))].
- TS-b assumes (U1) and either (U2) or (U2′). One inequality interpolates between them: replace the last term of (U2′) by min{2√ϑ, √2}·√(log C(p−s0, m)), with ϑ the leakage of the class.

In words: (U1) the signal left by dropping true predictors exceeds twice their prior-plus-Occam price; (U2) only a few predictors (Q_n) can imitate missing signal, rivals built from them obey the same constant 2, and nothing else explains more than a vanishing share of what is left. With Q_n = S0 this is "no proxies" and reduces to (U1). The manuscript already uses a leakage set in `asm:reported`, so the vocabulary is consistent.

Cost of P-U:
- **Strength.** P-U implies the current A-MARGIN-U through Lemma W (C-1), so it is somewhat stronger: it gives up the containing-model credit and at most a factor √2 on the worst-case width. It uses one slack η in place of δ, γ, t_n, since √(2Pr_n) ≥ √(log n) absorbs each of them.
- **Proof risk.** Low for the added part (W1, W2). The obligations of TS-b steps 2–3 are unchanged. It does not need the conjectured "separated proxies imply a joint proxy" lemma, because (U2b) is assumed jointly over N.
- **S1.** (U1) and (U2) hold for S1 as a sequence, with Q_n = S0 plus its L_n nearest nulls, L_n → ∞ slowly. Population leakage of the null at distance k from S0, maximised over all 1,023 D: 0.265, 0.087, 0.030, 0.011, 0.004, 0.0014 for k = 1…6. (U2a) has minimum ratio 2.51–2.77 at SNR 2, equal to the exact κ_n, and fails at SNR 1, as it should.
- **S1 under the fallback.** (U2′) alone fails at SNR 2 (ratio 0.91–0.93 at m = 1, 0.77–0.79 at m = 2) and holds at SNR 3 for m ≤ 3 (1.05–1.40). The package already reports the same for its combinatorial form.
- **S2.** Not an asymptotic regime (s0 log p/n = 0.69); its status is unchanged.
- **Pervasive factors.** They fail (U2) with small Q_n and fall under the interpolated form or (U2′). This is a real dichotomy, the same one as in the manuscript's Result 3, and should be stated as such.

**Standard-genre corollary to display next to P-U** (C-6). Let φ² be a lower bound on λ_min(Corr(x_T)) over |T| ≤ s + m̄ and θ_min := min_{j∈S0} |β*_j|·sd(x_j)/σ*. Then R_n(S) ≥ n·φ²·d·θ_min²·σ*², and Pr_n(d) ≤ d·log(2p√(n+1)), so
  θ_min ≥ (1+η)·(1 + √m̄)·√(2 log(2p√(n+1))/n)/φ  implies (U1) and (U2′).
For an orthogonal design, (U1) alone reads β_j²·Var(x_j) ≥ 2(1+η)·σ*²·log(2p√(n+1))/n. This is the "sparse eigenvalue plus beta-min" form a reader expects, with explicit constants.

---

## 3. The assumption set as a whole

**Cohesion.** The set is coherent: every condition is on the data-generating law, none on tuning. That is a point in our favour against SL, whose hypotheses mix data conditions (Conditions 1–5, sparsity) with rate conditions on r_n, r̄_n and V_ξ ((8)–(14), (22)–(23)), one of which SL call "hardly satisfied". Twelve labels are too many for a paper. I suggest four blocks:
1. Model: A-GL, A-SPARSE, A-DIM, A-BS.
2. Design: A-SUBG, A-NEC.
3. Signal: A-MARGIN-H for screening, A-MARGIN-U (P-U) for exact selection.
4. Omitted variables: A-MIS in primitive form with A-SPARSE-C; A-MOM for the fixed-dimension result.

**Redundancy and minimality.**
- A-BS with fixed s implies the first half of A-BS′, so A-BS′ is not a separate assumption at fixed s.
- A-MIS(iii) makes the candidate problem an instance of A-GL. TM-a and TM-b are corollaries and should be called that.
- TS-a and TS-b are not redundant. TS-a is a per-predictor result: a strong predictor is found whatever the other signals do, and with no condition on substitutions. Say so; it is the natural partial-recovery statement.
- TD needs no eigenvalue condition if one accepts the extra √log(p∨n) of the delivered prop:dist(ii). SL Thms 1–2 have no eigenvalue condition either, so prop:dist(ii) is the closest like-for-like counterpart and deserves a line in the map.
- The prior enters the assumptions only through Pr_n. Defining Pr_n by prior odds and Occam factor (P-U) makes the margin read as a statement about any multiplicity-correcting prior, with BB(1, p) and g = n as the instance.

**SL benchmark, by genre.**
- Same genre and at least as general: A-GL (model (1)), A-SPARSE ((4)), A-BS (weaker than (3) with fixed σ*), A-SUBG (Condition 1, relative instead of absolute scale), A-NEC (Condition 3's Gaussian form; SL's floor is larger), A-MOM (Condition 4).
- Narrower than SL: A-DIM (SL Cor 1 allows stretched-exponential P_n; Cor S1 is quasi-polynomial), and the high-dimensional TM tier (SL Thm 4 is second-moment only, but at fixed dimension, which TM-a0 matches).
- Wider than SL: no beta-min for TD; an explicit, sharp margin where SL's Theorem S leaves a fixed minimum coefficient implicit; exact selection where SL give inclusion or pairwise odds.
- After the changes in §4 the set reads as general as SL's. Today A-MARGIN-U does not.

**What a referee objects to first.**
1. The width term in A-MARGIN-U: random, design-conditional, checked by simulation.
2. "Consistency under misspecification" that, in high dimension, assumes a Gaussian linear model for the candidates. The dossier has the answer, but the assumption's name and form should make the scope obvious.
3. p ≤ n^A and fixed s, against SL Cor 1, CSV15 and YWJ. The honest TD′ status is the right reply.
4. Assumptions that depend on a level M and on constants taken from proofs.
5. Gaussian homoscedastic noise. This is standard, and the dossier's reply is adequate.

---

## 4. Top 5 changes, by priority

1. **Restate A-MARGIN-U as P-U.** Population quantities only: (U1) plus (U2) or the fallback (U2′), with explicit m̄ and one slack η. Add Lemma W. Keep w_Dm(X), the credit constant C and the B_Dm > 0 classes as proof-path refinements and as the E9 diagnostic. Record that the form is chosen on generality grounds, and that S1 then satisfies it.
2. **Remove S1/S2 numbers from every statement** (C-2) and rewrite row D4's rationale. S1/S2 appear only under Defence (b).
3. **Remove proof constants and the level M from the assumptions** (C-3): windows "c·log n for every fixed c" in A-SUBG and A-NEC; A-MARGIN-H as a diverging ratio; A-DIM′ as log p = o(√n).
4. **Add the standard-genre corollary and the worked cases** (C-6): sparse-eigenvalue floor plus beta-min implies the margins, with explicit constants; closed forms of R_n, κ_n and leakage for orthogonal, AR(1), block and equicorrelated or one-factor designs.
5. **Make the TM tier plain and patch the SL map** (C-4, C-5): A-MIS in primitive form, A-SPARSE-C labelled and defended, TM-a/TM-b as corollaries; add SL (3) for A-BS, the SL p. 951 cap-removal remark for q_n, and SL Condition 3's Gaussian form for A-NEC.

---

## 5. Scores (0–10)

| criterion | score | reason |
|---|---|---|
| Completeness | 7.5 | SL coverage is complete and no mathematical error was found at statement level. Missing: the population bridge for the width (C-1), an evaluable rival range (C-3), three SL counterparts (C-4), pseudo-true sparsity (C-5), the promised worked cases (C-6) |
| Generality and naturalness | 6.0 | Eight of twelve assumptions pass as stated or with a cosmetic restatement. The central margin does not, and S1 numbers sit inside statements. With changes 1–3 I would expect about 8.5 |
| Readiness for the owner's assumption-by-assumption Q&A | 6.5 | The dossier is thorough and candid. The owner's first question on A-MARGIN-U ("why this width, and where does it come from besides our simulations?") has no general answer in v1.3 |
