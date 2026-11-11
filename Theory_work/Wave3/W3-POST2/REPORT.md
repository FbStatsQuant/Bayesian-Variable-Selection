# W3-POST2 — REPORT (to Theory HQ)

Ticket W3-POST2 (HQ decision 2026-11-09): improvements to W3-POST's posterior theorem. Lead: Claude Opus 5.5
(claudeAgent, high). Folder `Theory_work/Wave3/W3-POST2/`. No git state changes.

**RESULT.** **COUNCIL-PASSED in round C1**:
- seat A gpt-6-astra high: 8.6;
- seat B Claude Opus 5.5 high (claudeAgent): 8.6;
- all six gates PASS for both seats in the same round.

All five brief items are closed by proof files, and no item was stopped. The full pipeline ran:
- statement lock;
- sharpness gate;
- cross-family line checks of every lemma;
- independent mid-point (CONTINUE);
- exhaustive sweep (all 17 findings fixed);
- council.

The new results are labelled **PROVED (by this seat, unchecked)**, with check records in each lemma file. Under the protocol
this pipeline qualifies for **PROVED-CHECKED**; HQ applies that label. Inherited statuses are unchanged.

**Flags for HQ.**
1. **Scope (sharpness gate).** Two ranked proposals from the better-theorem review R03b were adopted after the lead
   re-derived them. Their effects:
   - item 3: E δ_n = O(r_n), instead of O(n^{−q/2}) for q < 1;
   - item 4: D(b) without (F_λ), with variance at the parametric rate;
   - item 5: through D+'s ridge-loss lemma, Claim E's hypothesis weakened from (ID) to (ID^M), with Lemma E1 restated (v2).

   No other ranked proposal was adopted (`reviews/R03b_disposition.md`). PROTOCOL rule 3 gives HQ the decision on such
   strengthenings. HQ was not consulted beforehand, so **HQ approval is still required**. Each adopted change has its own
   line check (K2), and the mid-point, sweep and council reviewed it. The STATEMENT v1.1 targets can be restored.
2. **Kill budget for item 5.** E1 v1 was the one proof attempt. v2 is a sharpness-gate restatement under its own check.
   HQ to rule whether that is within budget.
3. **LOG.md clock times** after 19:20 were lead estimates that ran ahead of the real clock. They are replaced by step
   numbers, with an erratum line.

## 1. Results (statement: `STATEMENT.md` v1.2.1; proofs in `lemmas/`)

Notation and the coded target π are as in W3-POST STATEMENT §0. Regime R1: s₀ fixed, 2 ≤ p ≤ n^A, A ≥ 1, G.

Brief numbering is that of the delegation brief. In W3-POST REPORT §4 numbering: A = §4.1, B = §4.3, C = §4.4,
D = PROGRAM 1b, E = §4.2 (stretch).

**A — Theorem 1-OS** (item 1; `lemmas/A_occam.md`).

*New interface.* The superset Occam sum
𝒪_n^{>i} = Σ_{j=i+1}^{min(m♯_n, p−s₀)} [w(s₀+j)/w(s₀)] Σ_{|J|=j} (D_{S₀}/D_{S₀∪J})^{1/2} a_J,
with weights a_J = 2^{|J|/2}(eC_A|J| log n/max(d_J, 1))^{d_J/2}, where d_J is the rank gain.
- **(OS)** requires 𝒪_n^{>0} ≤ C_OS r_n and (2p)^{s₀}(n+1)^{s₀/2}𝒪_n^{>j₀} ≤ C_OS r_n.
- Chain of conditions: (F_w) ⇒ (DG) ⇒ (ADG) ⇒ (OS), where
  - (DG) is D_{S₀∪J}/D_{S₀} ≥ [c_D(n+1)]^{|J|};
  - (ADG) is its average over |J| = j.

*A1.* With (F_w) replaced by (OS), all of [W3P] Theorem 1's conclusions 1–6 hold, each with its beta-min qualification
unchanged. 5(a) needs only G, (E), (F₀), (OS). Rank loss costs nothing in the χ² part (Lemma M); it is still charged
through the determinant ratio in (OS).

*A2 (deterministic converse).* For every n, design and data: δ_n ≥ 𝒪⁰_n/(1 + 𝒪⁰_n), where 𝒪⁰_n is the unweighted sum
over feasible supersets. [LB] is its j = 1 term.

*Brief item 1 answered:*
- The proof uses (F_w) only through (OS). (DG) and (ADG) are the clean sufficient forms.
- (OS) is a sufficient envelope, not a characterisation. Its gap to A2 has four parts (STATEMENT A2):
  - the weights a_J;
  - feasible supersets with j > m♯_n;
  - infeasible comparison unions;
  - the amplified j > j₀ inequality.

**B — Lemma 1a″** (item 2; `lemmas/B_tail_approx.md`). Assume G′: Gaussian noise and an arbitrary centred mean (f ∉ col X
allowed), with ‖μ‖² ≤ nM. For any deterministic reference T and ϑ with cost
B_T(ϑ) = ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B:
- π(|S| > m) = A^T_mΘ″, with A^T_m = R^T_m√(D_T)√n (exact determinant);
- sup_m P(Θ″ > L) ≤ (8 + 24M/σ*²)/(n−1) + L^{−1/2} + C″_Λ(B)/log(√L/c♯);
- the bound is uniform over designs.

Uses:
- dropping weak coefficients from the reference;
- T = ∅ under weak total signal;
- the exact determinant (effective rank);
- misspecified means.

**C — Proposition ER** (item 3; `lemmas/C_expectation.md`). For every n ≥ n₀ at which the hypotheses hold, under any one
of these three sets:
- (i) W3-POST Theorem 1's hypotheses with BM;
- (ii) A1's hypotheses with BM;
- (iii) E's hypotheses,

we have **E[1 − π(S₀)] ≤ C r_n**, uniformly over designs with common constants. (For random designs add P(𝒜_nᶜ).)
- Consequences: P(HPM ≠ S₀), P(MPM ≠ S₀) ≤ 2Eδ_n; P(ξ_q ≠ S₀) ≤ Eδ_n/min(q, 1−q); E max|PIP − 1| ≤ Eδ_n.
- Key step (Lemma C1): a deterministic lower bound on the reference marginal on {E′ ≤ 2N}. It integrates over a window on
  the favourable side of σ*², chosen from the data.
- Sharpness: on [LB]'s domain (1 ≤ s₀ < p, s₀ + 1 ≤ K), E δ_n is between order n^{−1/2} and √(log n/n).

**D — Corollary H** (item 4 = PROGRAM 1b; `lemmas/D_hellinger.md`). This is the working-model posterior of (S, θ, v) on
the original response scale ([P1] `thm:T01i`). The distance is the centred in-sample average Hellinger distance, bounded as
h̄_n² ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²). With the plug-in intercept it gains only an O_P(1/n) term (D4 Remark 0).
- **D(a):** if δ_n → 0 in probability, under (E) and (F₀), then for every M_n → ∞ the following posterior events have
  vanishing mass: ‖μ̂ − μ‖² > M_n, |v/σ*² − 1| > M_n/√n, S ≠ S₀, ‖θ − θ*‖ > M_n/√n.
- **D(b):** under G, (E), (F₀), (OS), with no beta-min and no floor away from S₀: Π(‖μ̂ − μ‖² > C_H log n or
  |v/σ*² − 1| > M_n/√n | y) → 0, hence h̄_n² = O(log n/n).
- Relation to Song–Liang (2015) Thms 1–2: this is their in-sample analog. The differences are recorded in ASSUMPTION_MAP.

**E — Theorem 1-VIS** (item 5, stretch; `lemmas/E_visibility.md`). Hypotheses: R1, G, (E), (F₀), (OS) and **(ID^M; c)**,
with c > c₁. (ID^M; c) means L_S = μ_cᵀ(I − M_S)μ_c ≥ cσ*² log n for every underfit S ∈ Ω with |S∖S₀| ≤ j₀. It is
implied by the projection margin (ID).
- Conclusions: items 1–4 of Theorem 1 and Claim C. Item 5(b) holds under (ID^M_j). Item 6 holds as in W3-POST.
- No eigenvalue condition on any set other than S₀.
- Key step (Lemma E1): a floor-free comparison of S with S ∪ S₀ via Q_{S∪S₀} ≤ Q_{S₀}. Lemma E0 supplies the cutoff
  bookkeeping.

*Brief item 5 answered:* **yes, the floor set size is improvable.** (F_λ) is not needed.

## 2. Relation to W3-POST results (for the registry; one label per row)

| new | relation | to | reason |
|---|---|---|---|
| A1 | **implies** | [W3P] Theorem 1 | (F_w) ⇒ (OS) (Lemma A0) |
| A2 | **implies** | [W3P] Prop. LB | LB is A2's j = 1 term with D-ratio ≤ n + 1 |
| B | **implies** | [W3P] Lemma 1a′ and Lemma 1a | exact reference: r = 0 recovers C′_Λ; Θ^T, Θ♯ ≤ Θ″ |
| C | **implies** | [W3P] Theorem 1 item 1 (under its hypotheses) | Markov; also strengthens item 3's "no expectation rate claimed" |
| D(a), D(b) | **new** | — | PROGRAM 1b |
| E | **supersedes** (for c > c₁; coexists for c₀ < c ≤ c₁) | [W3P] Theorem 1 items 1–4, A1 items 1–4 | (F_λ) ∧ BM(c) ⇒ (ID; c(1−1/n)) ⇒ (ID^M; c′) for c₁ < c′ < c; c₀ < c₁ checked numerically on s₀ ≤ 20, A ∈ [1, 10] |

## 3. Assumptions (ids; `ASSUMPTION_MAP.md` v1.3)

**New ids.**
- POST2-OS — superset Occam sum.
- POST2-ADG / DG — averaged / pointwise determinant ratio.
- POST2-F0 — floor on S₀.
- POST2-ID / ID^M — identifiability margin, projection or ridge form.
- POST2-GP — Gaussian noise with an arbitrary centred mean.
- POST2-AR — bounded reference cost.

**Implications.**
- (F_w) ⇒ (DG) ⇒ (ADG) ⇒ (OS).
- (F_λ) ⇒ (F₀).
- (F_λ) ∧ BM(c) ⇒ (ID; c(1−1/n)) ⇒ (ID^M).
- (F₀) ∧ (E) ⇒ the coefficient bound.
- An exact representation implies bounded cost.

## 4. Sharpness record

Numerics: `numerics/post2_checks.py` v2 → `post2_checks_out.txt`, exact enumeration at p = 10, 20 seeds. These are
finite-n observations at fixed p, and do not probe growing p.

- **Supersets.**
  - (OS) is sufficient. Its unweighted feasible part is necessary (A2).
  - N1 exact: δ_n ≈ 0.7, not → 0. A2 had 0 violations across all runs.
  - N2 (duplicated null pair): consistent with strict weakening (ADG) → (OS); no asymptotic proof is given for this
    example.
- **(F_λ):** not needed (E).
  - N1 κ = ½: φ₀² ≍ n^{−1/2}, yet δ_n/r_n stays between 0.80 and 1.20.
  - N1 κ = 1: the full (ID) minimum falls to 0.22 log n and δ_n ≈ 0.6 — a small-margin obstruction. This is an
    illustration; no converse is proved.
- **(F₀):** still assumed, but looks improvable. N8: λ_min(R_{S₀}) → 0, yet δ_n/r_n is 0.80 at n = 6400.
- **Margin constant:** c₁ ≈ 161 is a proof artefact.
  - N4 at coefficient scale c = 4: achieved margins 3.67–3.99 log n, δ_n/r_n 0.75–1.18. No universal smaller constant is
    proved.
  - R03b proposes c₁ ≈ 54 by local retuning, and notes that about 2a_p + 2 is an obstruction at p = n^A.
- **Expectation rate:** O(r_n) proved; ≥ (1 + √(n+1))⁻¹ on LB's domain. N5: mean δ_n√n ∈ [2, 6].
- **Predictive:** D(a)'s 1/n mean scale is argued, not proved as a lower bound (D4 Remark 2). D(b)'s log n/n is consistent
  with N7.
- **Reference cost (B):**
  - Bounded cost is sufficient, not necessary (N6b: Θ″ stays bounded with B = n − 1).
  - A mean ⊥ col X is fine.
- **Not tested:** non-Gaussian noise (the inherited chain assumes G); growing p.

## 5. Review trail (verbatim replies in `reviews/`)

| layer | reviewer | verdict | file | disposition |
|---|---|---|---|---|
| Statement lock L01 | gpt-6.1-sol high (codex) | LOCK-WITH-AMENDMENTS (0/3 MAJOR/2/1) | `L01_statement_lock_sol.md` | `L01_disposition.md`: all applied → v1.1 locked |
| Better theorem R03b (sharpness gate) | gpt-6-astra high | 7 ranked proposals | `R03b_better_theorem_astra.md` | `R03b_disposition.md` |
| Line check K-AE (A, E v1) | gpt-6.1-sol high | VERIFIED-WITH-AMENDMENTS (0/1/4/1) | `K_AE_check_sol.md` | `K_AE_disposition.md` |
| Line check K-BC (B, C v1) | gpt-6.1-sol high | VERIFIED-WITH-AMENDMENTS (0/0/3/1) | `K_BC_check_sol.md` | `K_BC_disposition.md` |
| Line check K-D (D v1) | gpt-6.1-sol high | VERIFIED-WITH-AMENDMENTS (0/1/2/1) | `K_D_check_sol.md` | `K_D_disposition.md` |
| Line check K2 (C v2, D v2, E1 v2) | gpt-6.1-sol high | C VERIFIED; D, E VERIFIED-WITH-AMENDMENTS (0/0/1/1) | `K2_v2_check_sol.md` | `K2_disposition.md` |
| Mid-point M01 | gpt-6-astra high, fresh, files only | **CONTINUE** (0/0/2/1) | `M01_midpoint_astra.md` | `M01_disposition.md` |
| Exhaustive sweep S01 | gpt-6.1-sol high, fresh | 0 / 2 MAJOR / 13 / 2; no analytic defect | `S01_sweep_sol.md` | `S01_disposition.md`: all 17 fixed (numerics v2) |
| Citation check | `citecheck.py` (ranges, P1/P3 \\label, tokens, statuses) | see `reviews/CITECHECK.txt` (0 failures at close) | `CITECHECK.txt` | — |
| **Council C1** | seat A gpt-6-astra high; seat B Opus 5.5 high (claudeAgent) | **A 8.6, B 8.6, all gates PASS — PASSED** (A 0/0/2/1; B 0/0/5/7) | `C1_council_astra.md`, `C1_council_opus.md` | `C1_disposition.md`: all applied post-council (wording/bookkeeping; Lemma E0; intercept remark) |

## 6. Open items and recommendations
1. R03b A+: exact truncated-moment weights and completion costs give a strictly weaker (OS). Low risk.
2. R03b E+: c₁ ≈ 54. Low–medium risk.
3. R03b E-floor+: replace (F₀) by a bounded ridge cost. Medium risk; N8 suggests it is worth doing.
4. R03b B+: explicit growing-cost payment. Low risk.
5. D-transfer: out-of-sample Hellinger under an explicit design-law interface.
6. Open questions:
   - Does the √(log n) factor in E δ_n appear?
   - A lower bound for D(b)'s log n.
   - A converse for (ID^M).
   - Asymptotic strictness of (OS) vs (ADG) for an explicit design.

## 7. Files
- `STATEMENT.md` (v1.2.1), `PLAN.md`, `LOG.md`, `ASSUMPTION_MAP.md` (v1.3), `REPORT.md`.
- `lemmas/A_occam.md`, `B_tail_approx.md`, `C_expectation.md`, `D_hellinger.md`, `E_visibility.md`.
- `numerics/post2_checks.py` → `post2_checks_out.txt`.
- `citecheck.py` → `reviews/CITECHECK.txt`.
- `reviews/` — all reviewer replies, scratch directories and dispositions.

## 8. Registry blocks (INFRA template format; rule 8 applies from 2026-11-10, included anyway)

```
REGISTRY
claim: W3-POST2:A1 | kind: theorem | statement: STATEMENT.md:54-57 | premises: STATEMENT.md:27-50
status: PROVED (by this seat, unchecked) | status_source: lemmas/A_occam.md:3
assumptions: A:G ; A:E ; A:Fλ ; A:BM (items 1-4) ; A:OS (new | superset Occam sum | STATEMENT.md:27-36 | shared yes | bridge Lemma A0)
consumes: P:OS
conclusion: posterior: [W3P] Theorem 1 items 1-6 with (F_w) replaced by (OS) | rate: O_P(r_n) | scope: R1, fixed design + random-design transfer
depends_on: W3-POST:T1@proof ; T03R@proof:(C2),(C4),(C5),(C8),(C10)
implies: W3-POST:T1 ((F_w) ⇒ (OS), Lemma A0)
sharpness: A:OS = WEAKENABLE (A+ recorded; evidence reviews/R03b_better_theorem_astra.md) ; unweighted part NECESSARY (A2)
gates: correct:PASS(reviews/C1_council_astra.md, reviews/C1_council_opus.md) ; better:PASS(reviews/R03b_better_theorem_astra.md)

REGISTRY
claim: W3-POST2:A2 | kind: proposition | statement: STATEMENT.md:58-63 | premises: none (deterministic)
status: PROVED (by this seat, unchecked) | status_source: lemmas/A_occam.md:3
conclusion: negative/target: δ_n ≥ 𝒪⁰_n/(1+𝒪⁰_n) for every design and data | scope: any n ≥ 3, s₀ ≤ K
implies: W3-POST:LB (j = 1 term)
gates: correct:PASS(C1 both seats)

REGISTRY
claim: W3-POST2:B | kind: lemma | statement: STATEMENT.md:68-82 | premises: G′, ‖μ‖² ≤ nM, B_T(ϑ) ≤ B
status: PROVED (by this seat, unchecked) | status_source: lemmas/B_tail_approx.md:3
assumptions: A:GP (new | Gaussian noise, arbitrary centred mean) ; A:AR (new | bounded reference cost)
conclusion: posterior: size tail π(|S|>m) = O_P(R^T_m √D_T √n), uniform over designs | scope: any p ≥ 2, n ≥ 3
implies: W3-POST:L1a′ ; W3-POST:L1a
sharpness: A:AR = ARTEFACT (not necessary: numerics N6b; reviews/S01_sweep_sol.md item 1)
gates: correct:PASS(C1 both seats)

REGISTRY
claim: W3-POST2:C | kind: proposition | statement: STATEMENT.md:83-98 | premises: per-n hypotheses (i)/(ii)/(iii)
status: PROVED (by this seat, unchecked) | status_source: lemmas/C_expectation.md:3
conclusion: posterior: E δ_n ≤ C r_n (uniform over designs with common constants) | rate: r_n; lower bound n^{-1/2} on LB's domain
implies: W3-POST:T1 item 1 (Markov)
gates: correct:PASS(C1 both seats) ; better:PASS(R03b, proposal C+ adopted — HQ approval pending)

REGISTRY
claim: W3-POST2:D | kind: corollary | statement: STATEMENT.md:99-125 | premises: D(a): G, E, F0, δ_n → 0 ; D(b): G, E, F0, OS
status: PROVED (by this seat, unchecked) | status_source: lemmas/D_hellinger.md:3
conclusion: posterior: in-sample Hellinger contraction, rate M_n/√n (D(a)), log n/n (D(b), no beta-min) | scope: R1, fixed design + transfer
implies: — (new; PROGRAM 1b)
gates: correct:PASS(C1 both seats) ; better:PASS(R03b, proposal D+ adopted — HQ approval pending)

REGISTRY
claim: W3-POST2:E | kind: theorem | statement: STATEMENT.md:126-139 | premises: G, E, F0, OS, ID^M(c), c > c₁
status: PROVED (by this seat, unchecked) | status_source: lemmas/E_visibility.md:3
assumptions: A:ID^M (new | ridge identifiability margin on bounded-excess underfits | STATEMENT.md:40-42 | bridge E3.1)
conclusion: posterior: [W3P] Theorem 1 items 1-4 + Claim C | rate: O_P(r_n) | scope: R1
implies: W3-POST:T1 items 1-4 for c > c₁ (supersedes)
sharpness: A:ID^M constant = ARTEFACT (N4; R03b E+) ; A:F0 = WEAKENABLE (N8; R03b E-floor+)
gates: correct:PASS(C1 both seats) ; better:PASS(R03b)
```
