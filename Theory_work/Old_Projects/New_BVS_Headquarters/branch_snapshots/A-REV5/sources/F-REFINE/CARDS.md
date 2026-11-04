# F-REFINE — CARDS: best believed versions of the eight paper targets (phase P6)

Lead: F-REFINE (Fable 5.1), 2026-11-02, branch `theory/F-REFINE`. Companion files: `ARCHITECTURE.md` (dependency
graph, with/without LS0, journal cuts) and `NEXT_TASKS.md` (ready-to-run Opus specs).

**What this is.** For each of the eight frozen targets (`Docs/THEORY_PRIORITIES.md` §1) I give the *best believed
version*: the strongest statement I believe is true and provable at reasonable cost, consistent with every verified
result and every counterexample produced by the campaign (branches `origin/theory/W1-*` … `W4-*`, read in full,
including the verifier reports and repairs). Nothing here is adopted; every campaign proof is a candidate until
cross-family review (A-REV1/A-REV2 are assigned but had pushed nothing when this was written).

**Inputs read.** W1-T37R + W3-VT37R; W1-T24G + W2-VT24G + W2-PREM; W1-T38E + W3-VT38E; W1-EXP + W3-VEXP; W3-PXN;
W3-PGD (PROOF only; its REPORT is a stub); W1-T03R + W2-VT03R; W2-T26; W2-BOOK; W4-T38FULL; W4-SHARE (PROOF + NOTES,
no REPORT yet); the frozen list, both consultant reviews, T37–T39, PROTOCOL and LEDGER.

**Conventions.**
- Status words are the protocol's and are never upgraded. "VERIFIED (Wx)" means one adversarial verifier of the
  *same* model family checked it line by line; that is not cross-family review.
- **P(true)** is my probability that the refined statement is true as written. **P(provable)** is my probability
  that a complete, reviewable proof exists at reasonable cost (one Opus run plus a verifier); "done" means a
  candidate proof already exists and only review is left.
- Notation follows `Docs/Theory/theorems/00_COMMON.md` and the branch PROOF files. Φ(S) = |S Δ S₀|, m(S) = |S₀∖S|,
  e(S) = |S∖S₀|, Lat(S°) the lattice between S° and S₀, D_S the one-state progress event, R̄ the potential
  uninterrupted run, 𝒪 the output-available event, δ₁ = 1 − π(S₀).

## 0. Summary table

| Paper # | Target | Best believed version (one line) | Status of the believed version | P(true) | P(provable) | Method change |
|---|---|---|---|---|---|---|
| Thm 1 | T03 (+T01, T02) | T03♯: selection consistency under anchored, size-restricted SE_λ(j₀) + SE_w(m♯; g₀) and BM-∞ or BM(c), plus the exact BB tail T02(i♯) | PROVED (W1-T03R), VERIFIED (W2-VT03R) | 0.95 | done | no |
| Prop 1 | T07 (+T06(i)) | Bayes rules; sharp size-prior ceiling (iff S*_{s₀} = S₀); same-size-swap certificate; tie criterion X_SX_Sᵀ | PROVED-LOCKED + W2-BOOK (i′)(iii′) | 0.98 | done | no |
| Thm 2 | T22 + T27 | EXP′ is a theorem; favourable start under BO/zero-leakage (reference S° allowed); masked start under CL(L) at the p^{−c}n^{−c/2} rate; LH realises both jointly | PROVED (W1-EXP), VERIFIED (W3-VEXP); LH-iid p ≫ n PROVED by W3-PXN, unverified | 0.95 / 0.85 (p ≫ n) | done / review | no |
| Thm 3 | repair (T37 → Theorem A + Theorem W; T24 → Theorem B′/B♯) | (i) greedy repair ⇔ TD′ (exact, finite n); (iii) TD′ w.p. → 1 under PGD(η) + LD♭; Gibbs-path inequality β_H(x) with no factorial | (i) PROVED, VERIFIED; (iii) PROVED (W3-PGD), unverified; B′ PROVED, VERIFIED | 0.97 / 0.85 / 0.95 | done / review / done | no |
| Thm 4 | T21 | P(𝒪, Ŝ ≠ S₀) ≤ 2E₀δ₁ + P(𝒪̄, S₀ ∉ 𝒮̄) for every n, on R̄ under GUARD; routes (a), (d)/(d⁺), (e′)/(e-M); H24 retired | PROVED (W2-BOOK, W4-T38FULL (0)); (e′) VERIFIED (W2-VT24G) | 0.97 | done | no |
| Thm 5 | T38 | two-regime HPM consistency: (a) favourable; (b1) masked with LS0, all premises proved on LH (p < n), LH-iid (p ≫ n) pending verification; (b1′) D2 conditional; (b2) envelope route conditional | (0)(a)(b1) PROVED (W4-T38FULL), same-family verified; (b2) inputs OPEN | 0.9 (b1) / 0.5 (b2 instance) | review / 0.3 | **LS0 for (b1)** |
| Thm 6 | T26 (i)–(ii) | evidence and PIP consistency under one premise (T_n+1)Δ_n → 0 (P2 redundant), favourable regime, output-form, never conditioning on completion | PROVED (W2-T26), unverified | 0.95 | done | no |
| Prop 2 | T12 (+T31(i)) | islandwise identities on R̄; pooled island product unbiased; pooled × pooled bias = −¾Cov (not an identity); output-level 95% bound under GUARD; VAL-FP contract | PROVED-LOCKED + W2-BOOK, unverified | 0.97 | done | no |

**The two headline facts for Felipe's gate.**
1. Every target has a believed version with a candidate proof. The literal T37, H24 and the brief's eligibility
   condition are false and must disappear from the paper; their replacements are proved.
2. The only *method-change dependency* is LS0, and it carries the only masked-regime consistency instance whose
   premises are all proved on an explicit family (Thm 5(b1) on LH). Without LS0 the masked regime is conditional
   (routes (b1′), (b2)). Nothing proved describes the n = 200 numbers: the study's start is dilution-masked, its
   misses are posterior misses, and the T03 proof thresholds begin near n ≈ 2·10⁶.

---

## Card 1 — Theorem 1: T03 selection consistency (with T01 contrast reduction and T02 dimension control)

### Refined statement (T03♯, W1-T03R, with W2-VT03R's R1/R2 wording)
Regime R1 (triangular array, s₀ fixed, p_n ≤ n^A), G, R. Let K = min(p, ⌊n/2⌋), q_k = C(p,k)w(k), R_m = Σ_{m<k≤K}
q_k/w(s₀) (exact BB(1,p) class ratio), m♯_n = min{m ≥ s₀ : R_m ≤ n^{−(s₀+2)/2}}, j₀ = ⌈(2A+1)s₀⌉+1.
- **SE_λ(j₀):** λ_min(R_{S₀∪J}) ≥ φ₀² for all J ⊆ S₀ᶜ, |J| ≤ j₀.
- **SE_w(m♯_n; g₀):** λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ > 0 for all |J| ≤ m♯_n (unnormalised non-degeneracy).
- **Beta-min:** BM-∞, or BM(c) with c > c₀(s₀, A) (unnamed constant; the proof gives L*).

Then:
- (T02(i♯)) Π(|S| > m | y) = R_m (n+1)^{s₀/2} √n · Θ♯_{n,m}, with sup_m P₀(Θ♯ > L) ≤ (8+24M/σ*²)/(n−1) + L^{−1/2} +
  C_Λ/log(√L/c♯); hence Π(|S| > m♯_n | y) = O_P(e^{−ω_n}) with m♯_n ≤ min(K, m_n^{old}). (No SE.)
- (T02(ii♯)) Π(S ⊋ S₀ | y) = O_P(√(log n/n)) under SE_w alone.
- (i) 1 − π(S₀) = O_P(√(log n/n)); (ii) max_j|PIP_j − 1{j∈S₀}| ≤ 1 − π(S₀) for every data set and P₀(MPM = S₀) → 1;
  (iii) P₀(HPM ≠ S₀) ≤ 2E₀δ₁ → 0, and S₀ is the strict global maximiser of F on {π(S₀) > ½}; (iv) without beta-min,
  the signals with θ*_j² ≥ cσ*² log n/(nφ₀²), c > c₀, get PIP → 1; (v) scale invariance.
- Deterministic clauses that hold at every n (F1): the PIP inequality in (ii); and if π(S₀) > ½ then HPM = MPM = S₀
  strictly.
- Optional further weakening (PROOF SKETCH, W2-VT03R Prop. W): SE_λ(j₀) + BM may be replaced by SE_w + a direct
  signal-separation condition SIG(c), c ≥ L*.

### Data evidence
- **All 565 completed wrong HPMs in the p ≫ n study are posterior misses** (F(S₀) ≤ F(HPM)); 0 search misses
  (THEORY_PRIORITIES §5). At c = 1 mostly supersets, at c = 0.5 same-size swaps and subsets. This is the regime the
  theorem speaks to, but it does not quantify it at n = 200.
- At n = 200: the old SE ranged over 215–229 columns (rank-impossible); SE_w now ranges over ≤ 114 columns because
  the cap K = 100 binds, **not** because of the exact tail (uncapped m♯ = 146/168). Greedy-adversarial eigenvalues
  (one draw each): λ_min(G) ≤ 0.40 (S1), ≤ 0.22 (S4) at |S₀ ∪ J| = 114; feasibility of g₀ is unverified.
- Beta-min: the proof constant needs θ*² ≥ 27.5/φ₀² (p = 500), executed θ*² = 0.64 / 0.16: a ≥ 43× shortfall; the
  orthogonal-design scale (log n + 2 log p)/n ≈ 0.09 is 7× *below* the executed signal, so the shortfall is the
  constant, not the signal.
- Proof thresholds: the geometric-series condition q_n ≤ ½ first holds at n ≈ 2.1·10⁶ (p = n^{1.17}); W1's
  "1.2·10⁵" was an ERROR (W2-VT03R R1).
- Exact checks: E1/E2 on 2,779 (p, n, s₀) triples; Prop. D (duplicated columns) reproduced analytically and
  numerically; deterministic inequalities on 60 adversarial designs.

### Proof status and sources
| Claim | Source | Verifier |
|---|---|---|
| T01, T02, T03 (locked) | `LOCKED_PROOFS.md`, wave 3 | external review queued |
| E1 exact tail; E2/E3 location of m♯ and barrier | W1-T03R PROVED | W2-VT03R VERIFIED |
| T02(i♯), T02(ii♯), T03♯ | W1-T03R PROVED (candidate) | W2-VT03R VERIFIED, no GAP/ERROR in the mathematics |
| Prop. D: m_n = s₀ + O(s₀ log n/log p) is false under G, R alone | W1-T03R COUNTEREXAMPLE | reproduced (W2-VT03R) |
| Lemma A1: anchored SE ⇔ unanchored up to s₀ columns | W2-VT03R PROVED | — |
| Prop. W (SIG replaces SE_λ) | W2-VT03R PROOF SKETCH | — |
| π(S₀) → 1 on LH-iid via T03 + de-randomisation | W3-PXN P8 PROVED | unverified |

### Proof skeleton and crux
Markov numerator over an S₀ denominator (locked `lem:den` body = Lemma den′) with the exact class ratio R_m factored
out; supersets via the determinant penalty and an exact χ² under SE_w; underfitting models with |J′(S)| ≤ j₀ via the
signal lemma under SE_λ(j₀); |J′(S)| > j₀ via a crude bound needing no eigenvalue condition (C6)(a). **No crux
remains.** Prop. E3 shows the technique cannot push m♯ − s₀ below ≍ s₀ log n; whether the posterior itself needs it
is OPEN (irrelevant once SE holds, Prop. D′).

### Risk
- Validity: low. Relevance at n = 200: nil, and this must be disclosed (W1-T03R §5 paragraph with R1/R2 applied).
- Overstatement risk: "anchoring" is cosmetic (Lemma A1); the real relaxation is size (m♯ instead of m_n) and
  normalisation (g₀ instead of (n−1)φ₀²). FROZEN_LIST's sentence "cuts m_n to s₀ + O(s₀ log n/log p)" is false
  (class ratio is ½, not k/2p) and must be corrected.
- Downstream: T04 cites the old H-T02/m_n (not re-derived).

### Method change needed? No.
### P(true) 0.95 · P(provable) done (candidate + same-family verification; cross-family review pending)

---

## Card 2 — Proposition 1: T07 size-prior ceiling and Bayes decisions (+ T06(i) ties)

### Refined statement (locked T07(i)–(iii), T06(i)(a); W2-BOOK Prop 1 (i′), (iii′))
For the target posterior π and the ≺-least maximiser S*_k of the marginal likelihood among size-k models:
1. The HPM is a Bayes rule under 0–1 loss on supports; the MPM {j : PIP_j > ½} under Hamming loss (unique iff no
   PIP_j = ½; with the cap K keep the min(K, N₊) largest PIPs above ½).
2. A plug-in Hamming rule from any PIP estimate p̂ has excess posterior risk ≤ 2‖p̂ − PIP‖₁.
3. **Sharp ceiling:** some positive size-only prior has global HPM S₀ **iff** S*_{s₀} = S₀. A within-size ranking
   error (|S| = s₀, m(S) ≥ m(S₀)) is exactly the error no size-prior retuning can fix; this covers every truncated
   BB(a, b).
4. **Certificate:** a scored S′ with |S′| = s₀ and F(S′) > F(S₀) proves that no size-only prior recovers S₀ on
   those data.
5. (T06(i)) Two supports have equal posterior score for every y iff X_SX_Sᵀ = X_{S′}X_{S′}ᵀ (outer products, not
   projections); they then have equal size and nothing separates them.

### Data evidence
Every c = 0.5 same-size swap miss in the study is a certified ceiling by clause 4. HQ still owes the count of strict
same-size posterior misses by scenario (ANALYSIS-H2). Subset misses (different size) are not covered by the ceiling.

### Proof status and sources
Locked T07/T06(i) (wave 3); W2-BOOK Prop 1 (i′)/(iii′) PROVED (single run; an explicit ε-prior and a one-line
corollary). The T06 wording fix (outer products) is W2-BOOK's.

### Proof skeleton and crux
Finite, deterministic. The sharpness direction constructs a size prior putting almost all mass on size s₀. No crux.

### Risk
Low. Novelty is modest (Astra); it is a remark in the Biometrika cut. Astra's caveat stands: size-prior retuning
*can* move the different-size (superset/subset) errors, so the ceiling must be stated only for within-size errors.

### Method change needed? No.
### P(true) 0.98 · P(provable) done

---

## Card 3 — Theorem 2: T22 + T27, the start (upper and lower bounds)

### Refined statement
Setting: G, R-lite(A, M) (p ≤ n^A, ‖μ‖² ≤ Mn), the v3 partition, blocks of size ≤ 16, ν = 0.01 + n/2.

**(i) Deterministic (locked T22(i)(ii)(iv)).** The composite start puts mass ≥ (1−q)^{s+1}/(1+e)^s on any feasible
reference model S° (S° ≠ S₀ allowed); the odds from a reference to S₀ are exact; the tempering bridge keeps
sup_φ[1 − q_φ(S₀)] ≤ max of the endpoint deficits (so Δ_n = max{1−π₀(S₀), 1−π(S₀)} exactly, W2-T26 Lemma 1).

**(ii) EXP′ is a theorem (W1-EXP Thm 1).** Under G, R-lite and within-block SE (SE-blk: min_b λ_min(R_{C_b}) ≥
φ₀², checkable on the realised blocks), on an event of probability → 1 every within-block addition satisfies
log[r_b(T+l)/r_b(T)] = −½log(n+1) − ν log(1−x_{T,l}) + R, |R| ≤ κ_EXP; at finite n the data-computable certificate
of W3-VEXP R1 replaces κ_EXP. EXP′ is therefore removed from T22(iii)'s hypothesis list, and NL_η can be weakened to
NL_C (W1-EXP Prop 2.1).

**(iii) Favourable regime.** 1 − π₀(S°) → 0 at the reference S° under any of:
(F1) the locked T22(iii) hypotheses minus EXP′ (G, R, SE-blk, VIS, NL_η, NL_avg(κ)): rate O_P(2^B√(log n) n^{−κ});
(F2) BO + BM-blk: O_P(2^B√(log n) n^{−1/2}) (verbatim corollary);
(F3) exact zero leakage ZL(S°), SPREAD, VIS-lin(S°): O_P(2^B n^{−1/2}) (W1-EXP Thm 6, self-contained).
The reference may be S₀ (favourable) or S° ≠ S₀ (masked start that still concentrates near the truth).

**(iv) Masked regime (W1-EXP Thms 3–4, replacing H2).** Along a deterministic addition chain S^{(0)} ⊂ … ⊂ S^{(c)}
= S₀ with bounded chain leakage CL(L) (max_i|δ_{T_i,l_i}| ≤ Lσ), the ratio law is two-sided:
−1 − κ_EXP ≤ log[r(T_i+l_i)/r(T_i)] + ½log n ≤ κ_EXP + 1.01(L + |Z_i|)², and with H3 (π₀(S^{(0)}) ≥ c₀ w.p. → 1),
log π₀(S₀) + c log p + (c/2)log n = O_P(1). With growing L_n the upper side gains 1.01c(L_n + O_P(1))². This is a
bound on iid start draws only, not on the hybrid sampler.

**(v) One family carries both jointly (W1-EXP Thm 5; W3-PXN).** The linked-hub family LH (equicorrelated groups
plus, per masked variable, one suppressor edge ψ between two hubs with θ_{j_b} = −ψθ_{j_a}), with |ψ| < ρ and the two
hubs of each pair in different blocks (g ≤ B < 2g): with S° = S₀∖M, 1 − π₀(S°) = O_P(2^B n^{−1/2}) (so b_n → 1),
π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, VIS fails at S₀, and π(S₀) → 1. Exact Gram (p ≤ n−1): PROVED. iid-Gaussian rows
with n^a ≤ p ≤ n^A (p ≫ n allowed): partition = groups w.p. → 1, 1 − π₀(S°) = O_P(√(log n/n)) **without the 2^B
factor**, and the exact limit law of the masking statistic (W3-PXN P1–P4): PROVED by a single unverified run.

**Regime discipline.** (iii) and (iv)/(v) are never combined on one sequence. On LH the reference in (iii) is S°.

### Data evidence
- Exact computation at p = 16/20 (n from 50 to 1.6·10⁶): √n(1 − π₀(S°)) flat at 1.6; the masking statistic
  converges to its predicted law (median 0.55 vs 0.54); the T22(i) bound held in 300/300 replicates; all reproduced
  independently (W3-VEXP). LH-iid at p ≈ n^{1.25} up to p = 10,120: 186/186 T22(i) checks, Mstat limit law PIT
  p-values 0.43–0.89 (W3-PXN).
- **The study's n = 200 start is not T27-masked; it is dilution-masked** (W3-VEXP Prop. D, W3-PXN Prop. W, both
  exact): tables score against the full y, so each truth sees noise v_T ≈ 7–26σ²; the start mode misses 6–12 of the
  14 truths at *every* signal scale; π₀(𝓡₂) ≈ 0.8 is carried by small subsets of S₀ 6–11 additions from the truth
  (S4: only 0.1–0.3). It vanishes by n ≈ 800–1600 (p = 1000, scale 0.5: start-masked truths 8.4 → 4.2 → 1.4 → 0.1).
  W1-EXP's "weak-signal masking with bounded L" was rejected by both W3 runs (L² ≈ 50–200, CL(0) overshoots by
  17–29 orders of magnitude).
- Population level: S1/S3/S4/S6 have exactly zero block leakage on the actual partition (favourable asymptotically);
  S2/S5 leak in most blocks (neither clean theorem applies). In-sample favourability for iid S3/S4/S6 is a GAP
  (partition depends on the noise column), empirically true (median π₀(S₀) ≈ 1e-10, 4e-4, 0.1, 0.45 at
  n = 200, 400, 800, 1600).
- Rate relevance: 2^B√(log n/n) at B = 14 is 2.7·10³ (n = 200), 497 (n = 10⁴), 61 (n = 10⁶): the (F1)/(F2)/(F3)
  rates are numerically vacuous below n ≈ 10⁹. W3-PXN's 2^B-free rate is the one worth having (and verifying).

### Proof status and sources
| Claim | Source | Verifier |
|---|---|---|
| T22(i)(ii)(iv) | locked (wave 1, full chain) | — |
| T22(iii) | locked, CONDITIONAL on (F1) | — |
| EXP′ theorem; finite-n certificate | W1-EXP Thm 1 PROVED; W3-VEXP R1 PROVED | VERIFIED (W3-VEXP) |
| (F2) Thm 2; (F3) Thm 6; Props 2.1/2.2 | W1-EXP | VERIFIED (W3-VEXP); Thm 2 is a verbatim corollary |
| CL(L) two-sided law; T27(i) given H3; limit law | W1-EXP Thms 3–4 PROVED; limit law PROOF SKETCH | VERIFIED |
| LH exact Gram, Thm 5(a)–(e) | W1-EXP PROVED ((d) by locked T03) | VERIFIED; \|ψ\| < ρ boundary sharp in effect (W3-VEXP row 17) |
| LH-iid, p ≫ n: P1–P4 (exact Beta laws + truncation) | W3-PXN PROVED | **unverified** |
| Co-blocking kills masking when 2g ≤ B | W3-PXN Prop. Q PROOF SKETCH | — |
| ORTH family satisfies (F1) | W2-T26 Prop. C PROOF SKETCH | — |
| dilution ceiling Prop. D; threshold | W3-VEXP PROVED / PROOF SKETCH | — |

### Proof skeleton and crux
EXP′: Q_S = RSS + c_S (bounded), determinant ratio, RSS floor via a χ² union over ≤ 2^{16}p pairs. Favourable: EXP′
+ truncated Beta/χ² moments of each block ratio, summed over blocks (2^B from the block profile). Masked: telescoping
along the chain with the two-sided law. LH: unit additivity of the population residual; Lemma 4.2 forces the
partition. **Remaining crux (relevance, not validity):** the in-sample favourable regime for iid S3/S4/S6 with
≥ 2 groups per block (partition–noise decoupling), and the verification of W3-PXN's Lemma B (exact Beta laws
independent of y) which is what removes 2^B and reaches p ≫ n.

### Risk
- Validity: low for exact-Gram statements; medium for LH-iid (single run, new argument).
- Relevance: the rates are vacuous at the study size, the study is dilution-masked, and T27 bounds iid draws only.
  The paper must present Theorem 2 as mechanism (start finds the truth when blocks see it; provably cannot when
  truths cancel across blocks), and must *not* say the study is in either regime.
- The |ψ| < ρ cliff (beyond it mass moves to R_{g−1}) and the g ≤ B < 2g packing condition must be disclosed.

### Method change needed? No. (Sample-split partitions would close the in-sample GAP but are not proposed.)
### P(true) 0.95 (exact Gram) / 0.85 (LH-iid) · P(provable) done / 0.8 (verification of P3)

---

## Card 4 — Theorem 3: repair. T37 → Theorem A (exact) + Theorem W (asymptotic); T24 → Theorem B′/B♯ (Gibbs path)

### What is false and must go
- **Literal T37 is false.** For d ≥ 1 TD(d, m) is unsatisfiable (W1-T37R Prop 1, VERIFIED): at S = S₀ − j + l the
  swap l→j beats the addition of j whenever F(S₀) > F(S₀+l), so TD(d,0) fails for every d ≥ 1 on {π(S₀) > ½}, i.e.
  under T03's own conclusion (W3-VT38E Prop. V1, PROVED). At d = 0 it is false too, for lack of a positivity clause
  (W3-VT37R CEX-1). T37(ii)'s union bound includes a comparison with the wrong sign (cannot → 0). T37(i)'s "exactly
  |S Δ S₀| moves" is wrong (swaps cut Φ by 2).
- **H24 (T24's uniform exit input) cannot be discharged**: at boundary states of 𝓡_d a look-alike of a missing truth
  exits with probability ≥ (1−o(1))/(B+d+4); measured 0.62–0.98 in S2–S6 at p = 20, exact lower bound ≥ 0.39, and it
  grows with n (W1-T24G CE1, W2-VT24G confirmed + Lemma E). The brief's (1−c′)^{⌊H/(s₀+d)⌋} form is invalid (CE2).
- **PGD is not implied by SE + BM-∞** (combination look-alike, W1-T37R Exp 3, VERIFIED). So the asymptotic repair
  statement needs a genuine extra design hypothesis.

### Refined statement, part A: deterministic, finite n (Theorem A, Lemma 0, Lemma LS-score)
EX-A; fixed X, S₀; F the score; 𝓡 a finite family of feasible models containing S₀; M(S) the production best-move
map (⊥ if no strict improvement); progress moves = add a truth, delete an extra, swap extra→truth.
Conditions: (L) M(S₀) = ⊥; TD′_∞(𝓡): (L) and for every S ∈ 𝓡∖S₀, M(S) ≠ ⊥ and M(S) ∈ 𝓡; TD′_P(𝓡): (L) and M(S) is
a progress move for every S ∈ 𝓡∖S₀; D_S: the best progress neighbour of S strictly beats S and every non-progress
neighbour; R_{a,d} = {S ∈ 𝓡_d : m(S) ≤ a}.
- (A1) TD′_∞(𝓡) holds **iff** the uncapped greedy path from every S ∈ 𝓡 stays in 𝓡 and ends at S₀.
- (A2) Under TD′_P(R_{a,d}) the path from S stays in Lat(S) and reaches S₀ in τ(S) = m + e − #(extra→truth swaps)
  moves, max(m, e) ≤ τ ≤ Φ.
- (A3) Under TD′_P(R_{a,d}) and ℓ ≥ a + d (ℓ ≥ τ(S_c) is the exact need), the production search from any centre in
  R_{a,d} returns S₀ with `local_certified`, without `local_limit`, and then **Ŝ = S₀ with no π(S₀) > ½ premise**
  (Lemma 0(c)). The same holds for one centre under the lattice condition (L) ∧ ⋂_{S ∈ Lat(S_c)∖S₀} D_S.
- (A5, repaired) literal strict TD(d,0) ∧ POS(R_d) ⇒ TD′_P(R_d) ⇒ TD′_∞(R_d); the converse of the second fails.
- (LS-score) If D_S holds on Lat(C₀) ∩ {Φ ≥ 2} and ℓ ≥ Φ(C₀) − 1, the search from C₀ **scores** S₀ (the next scan at
  a flip neighbour scores it; certification not required). This is the form T38 uses.
- (Lemma 0, repaired R2) The final search can deliver Ŝ = S₀ only on E_LS = {S₀ ∉ 𝒮_pre, F(S₀) > F(centre)}. Every
  fit with Ŝ ≠ S₀ is either in E_LSᶜ (forced by monotonicity) or in E_LS with the search climbing past S₀ to a better
  model (a posterior miss, not a search miss).
- (Theorem B, finite-n probability) For a data-independent class 𝒞 ⊆ R_{a,d} with ℓ ≥ max_𝒞 Φ:
  P(search fails) ≤ P(S_c ∉ 𝒞) + P₀(NA_dᶜ) + P₀(TL_dᶜ) + Σ_{S ∈ Lat(𝒞), m ≥ 1} P₀(D_Sᶜ), each term an event in a
  Gaussian vector of dimension ≤ 4 given an independent χ² (ridge O(1/n)); |Lat(𝒞)| ≤ (2s₀)^a(p+1)^d, and 2^{Φ(S_c)}
  for a fixed centre. The 2^{s₀} is avoided only when the centre misses few truths (a delivery fact, R6).

### Refined statement, part B: asymptotic (Theorem W, W3-PGD; replaces T37(iii))
Regime R1; s₀, a ≤ s₀, d fixed; 𝒟 ⊆ S₀ᶜ deterministic. Assume EX-A, G, R, **SE_λ(d+1)** (anchored, λ_min(R_{S₀∪J})
≥ φ₀² for |J| ≤ d+1), BM-∞, **PGD(η)** on R_{a,d}(𝒟) for a fixed η > 0 (at every state missing a truth, the best
non-progress reduction of the population residual is ≤ (1−η) times the best progress reduction), and one of
(H1) d ≤ 1; (H2) (|𝒟|+1)^{d−1} ≤ n^{1/2−ε}; (H3) LD♭(d; B′, ρ*) with τ² < 1 + 1/(2A), τ = (1+ρ*√d)/√(1−ρ*²).
Then P₀(TD′_P(R_{a,d}(𝒟))) → 1, so for every data-dependent centre S_c and all n with ℓ_n ≥ a + d,
P(the search from S_c does not return S₀ certified) ≤ P(S_c ∉ R_{a,d}(𝒟)) + o(1).
- PGD is sharp: a reverse margin ρ⁰ ≥ (1+ε)ρ⁺ on a subsequence forces failure (Prop P4).
- Checkable sufficient conditions: GERC (θ-free, Tropp/OLS exact-recovery type, anchored at visited states) +
  TRC (truth retention; fails under cancellation); under BO with one truth per group, (B1)–(B3) are **iff**; for
  equicorrelated groups η*(d) = min{min_g(1−ρ_g²), min_{g≠h}(θ_h²/θ_g²)(1−κ_h(d))} explicitly. Gaussian random
  designs inherit PGD(η/2) from their population Σ (stability Lemma P5, Cor P6).
- LD cannot be dropped for d ≥ 2 with unrestricted extras (C-LD: equicorrelated nulls r > ½, TD′_P(R_{0,2}) fails
  w.p. → 1); it is unnecessary for d = 1 or for extras from a class of size n^{o(1)} (e.g. the nulls in the truth
  blocks, |𝒟| ≤ 15s₀).

### Refined statement, part C: masked-family instance (W4-T38FULL Lemma M + Prop. LH-LAT)
On LH with S° = S₀∖M: POP-LAT(S°, m₀) holds with explicit sharp margin
m₀ = min{(1−κ_max)R_min, min β_i²(1−ψ_i²)², min θ_h²}, R_i = β_i²ψ_i²(1−ψ_i²), κ_i = ρ²(1−ψ_i²)/(1−ψ_i²ρ²); Lemma M
turns any population margin m_n ≫ √(log n/n) into D_S on the lattice w.p. → 1; hence the search from S° scores S₀ in
c moves. This replaces T37's informal margin (n−1)θ²(1−r²)/(2σ²) by an exact formula on a concrete family.

### Refined statement, part D: the Gibbs path (Theorem B′/B♯, restated T24; supplement and T21 route (e′))
EX-A, EX-S, SR, φ = 1, H′ = L + 5 terminal rounds without resampling (IND-T: trajectories are conditionally
independent across particles, PROVED). For a particle at x with the two-phase potential V (|M| + a while a truth is
missing; |P| on supersets) and the exact data functions c_*(x), v(x), η(x):
P_x(S₀ not scored within H rounds) ≤ P(Bin(H, c′_*) < v) + Hη ≤ v(1−c′_*)^{⌊H/v⌋} + Hη, with
c′₂ ≥ 1/(B+3) deterministically at |P| = 1 and c₁ ≥ 1/|M(x)| from pointwise addability (no BTP). No factorial.
Cor. P1: at Hamming distance one, S₀ is scored in the next round with probability ≥ a₁(x) (≥ 0.14 at B = 4; at
production B = 14 the order factor alone is ≈ 1/17, unmeasured). Cor. B-M: the population failure is the product of
the per-particle bounds. Asymptotic premises (W2-PREM): τ₂, NL0(0), UDEL(1) PROVED; NL0(a)/UDEL(a ≥ 2) PROVED UNDER
a partner-graph condition PG and FALSE without it (equicorrelated nulls); TS PROVED UNDER non-cancellation, FALSE
under a cancellation pair; W1's look-alike family is defective on LH (use B♯); IND-M PROVED UNDER subset-start
concentration SCR + GS, OPEN for superset starts; on LH all premises PROOF SKETCH (two population inequalities only
numerical).

### Data evidence
- Production-scale regenerated data (n = 200, p = 500, s₀ = 14, ℓ = 10): **when S₀ is a flip/swap local maximum,
  every sampled centre in R_{2,2} was repaired and certified (1160/1160 W1; 630/630 W3) in ≤ 5 moves, 99% by
  progress moves only; when S₀ is not a local max, 0/280 and 0/234** (S₀ is a local max in 35/36 datasets at c = 1,
  23/36 at c = 0.5; worst S4–S6). Those failures are posterior misses, which no local search can fix.
- Exhaustive check of Theorem A on 720 designs × 632 states (p = 15): 0 violations. TD′_P(R₂) in 160/720, TD′_∞ in
  328/720; literal TD(2,0) in 0/720.
- The "0 repairs in 541 fits" is explained by Lemma 0 only on E_LSᶜ; at production scale 233/234 non-repaired
  sampled centres had F(S₀) > F(S_c) and the search climbed past S₀ (CEX-2 pattern). **Whether the study's 541
  final centres were in E_LS is OPEN** and needs one ledger extraction (F(S₀) − F(S_c) per fit).
- Gibbs path from raw π₀ draws at p = 20, production packing: 100% score S₀ within 12 rounds in all 12 designs;
  round-1 rates 0.19–0.90; measured per-round progress 0.75–1.0 against proven c₂ = 0.33–0.47 and floor 0.143.
  Single-particle Theorem B is vacuous at n = 200 (Hη ≈ 4–16; v > H possible) and at every n computed (p = 20).
- Move cap: ℓ = 10 is a non-issue for R_{a,d} with a + d ≤ 10; at the study size the start mode is 8–14 moves from
  S₀ (dilution), so the cap binds for LS0 in S4/S6 (W3-PXN).
- PGD on the study's population covariances (Cor P2′, my computation from its formula, unverified): η* = 0.20 (S1),
  0.10/0.08 (S3, d = 1/2), 0.055/0.043 (S4). Positive but small; S2/S5 are not block-orthogonal.
- 98% of fresh scores in the study come from Gibbs flips; the final local search repaired 0 fits. At n = 200 the
  local search is not the delivery mechanism.

### Proof status and sources
| Claim | Source | Verifier |
|---|---|---|
| Prop 1 (literal TD unsatisfiable), Lemma 0, Theorem A (A1–A4), Lemmas 2–3, Theorem B inclusions | W1-T37R PROVED | W3-VT37R VERIFIED (exhaustive); repairs R1 (POS), R2 (Lemma 0(b)), R3 (PHI-REACH), R6 |
| V1: TD(d,0) fails on {π(S₀) > ½} | W3-VT38E PROVED | — |
| Lemma LS-score | W4-T38FULL PROVED | same-family referee VERIFIED |
| Theorem C (PGD + LD) | W1-T37R PROOF SKETCH; W3-VT37R repairs R4, R5 | sketch after repair |
| **Theorem W** (TD′_P w.p. → 1 under PGD + H1/H2/H3), P1–P6, Lemma G/R/S/U, C-LD | W3-PGD PROVED (candidate) | **unverified; REPORT is a stub** |
| Lemma M, Prop. LH-LAT | W4-T38FULL PROVED | same-family VERIFIED (brute-force margins) |
| Theorem B (restated T24), Prop U, P1, B-M, CE1, CE2 | W1-T24G PROVED / COUNTEREXAMPLE | W2-VT24G VERIFIED after Lemma F′; B1′/B2′ added |
| IND-T; Lemma U; B1′ + PA (BTP unnecessary); NL0/UDEL under PG and EQ counterexample; TS; B♯; Theorem L (LH) | W2-PREM PROVED / PROVED UNDER / PROOF SKETCH | unverified |

### Proof skeleton and crux
Part A: induction along the greedy path with Φ as a potential; strict monotonicity of F along the path.
Part B: at states missing a truth, the population gap ηNφ₀⁴θ²_min (Lemma 1.2) beats the noise √(gap·log n)
(Lemma G, pairs with |AΔB| ≤ 2 and the union-model geometric bound) and the O(log n) penalties under BM-∞; at
supersets the population gap is zero and everything is a χ² tail against the penalty ½log n + log p, paid by
(H1)/(H2)/(H3) (Lemma S with the local/far decomposition under LD♭). **Crux for the paper:** PGD/LD♭ are new
hypotheses that must be shown on a named family (LH-LAT does it for the lattice form; Cor P2′ for equicorrelated
groups), and Theorem W has no verifier yet.
Part D: first-failure union over labels, binomial domination of progress rounds, the slot argument for extra
deletions (Lemma F′), and IND-T for the product form. **Crux:** a non-vacuous finite-n single-particle bound needs
multi-step-per-round credit and state-averaged (drift) rates; OPEN, and not needed if the multi-particle product
is used.

### Risk
- Validity: Part A none; Part B medium (unverified; constants in (★) off by 3–4× from C-LD's threshold; GERC's
  external precedent not re-checked); Part D low for the inequality, medium for the asymptotic premises.
- Relevance: high risk of overstatement. Theorem 3 is an asymptotic statement plus a finite-n "works whenever the
  posterior allows" fact. It does not explain the masked-regime successes at n = 200 (scored by Gibbs before the
  search) and the "correlated-design advantage" story through T37's margin is contradicted by the c = 0.5 posterior
  misses in S4–S6. Replace that story by the LH-LAT margin as the mechanism, with no n = 200 claim.
- Which route is "Thm 3": Theorem A + Theorem W (local search), because T38(b1) uses it and it is exact; Theorem B′
  goes to the supplement as T21's route (e′) (it is a scan route's complement, not route (e) of T37; W2-BOOK).

### Method change needed? No for Theorem 3 itself. LS0 is where Theorem 3 gets its centre (Card 6).
### P(true) 0.97 (A) / 0.85 (W) / 0.95 (B′ inequality) / 0.7 (B′ asymptotic premises on LH)
### P(provable) done (A, B′) / 0.85 (W: one verifier run) / 0.6 (B′ premises on LH written out)

---

## Card 5 — Theorem 4: T21 HPM composition

### Refined statement (W2-BOOK Thm 4; W4-T38FULL (0))
EX-A, EX-S, CAL, SR and **GUARD** (the resource guard is stop-only: on 𝒪 every reported output equals that of the
potential uninterrupted run R̄; no assumption on the law of the stop). U ⊇ {resource_limit} the no-output event,
𝒮̄ the scored set of R̄ (calibration, final run, rejected proposals, both Gibbs configurations, scans), δ₁ = 1 − π(S₀).
For **every n and every data set**:
  (C1) P(no output or Ŝ ≠ S₀) ≤ P(U) + 2E₀δ₁ + P(Ūᶜ, S₀ ∉ 𝒮̄);  equivalently P(𝒪 ∩ {Ŝ ≠ S₀}) ≤ 2E₀δ₁ + P(𝒪̄, S₀ ∉ 𝒮̄).
The discovery term is bounded by each of:
- (a) iid final draws: P(𝒜ᶜ, S₀ ∉ 𝒮_cal) + E[1_𝒜 1{S₀ ∉ 𝒮_cal}(1 − π₀(S₀))^{Q_f}], Q_f = 4N_e(T+L+5);
- (d) tables and scans: P(neither S₀ ⊆ some block, nor any local search of R̄ centred at a flip-or-swap neighbour of
  S₀); (d⁺) with Theorem 3: P₀(TD′ fails on the region) + P(no local-search centre in the region) [+ LS0: the
  start-side event {S̃₀ ∉ region}];
- (e′) Gibbs-path repair at a past-measurable selected state x: P(𝒜ᶜ, S₀ ∉ 𝒮_cal) + P(𝒜, no eligible particle) +
  E[1_{A_F} min{1, β_H(x)}], β_H(x) = P(Bin(H, c′_*(x)) < v(x)) + Hη(x), H ≤ L + 5; (e-M) the product over eligible
  particles (IND-T).
- Route (e) with H24 is retired. The π(S₀) > ½ premise is not needed when the local search certifies S₀ (Lemma 0(c)).
- Report P(U) empirically: 6/2,400 = 0.25% (Wilson 95% [0.11%, 0.54%]); S5 1.5%; S5 at p = 1000 2.5%.

### Data evidence
P(U) above. The decomposition matches the data: all completed misses are posterior misses (the 2E₀δ₁ term), 0 are
discovery misses. The 6 stops are all S5 and were counted as misses (correct convention). Never condition on
completion: a 0.22% stop rate can make E[Ẑ | output] = 0.974Z (W2-BOOK exact counterexample).

### Proof status and sources
Locked T21 (wave 2, full chain). W2-BOOK Thm 4 restated with Lemma RO (PROVED, set inclusions) and GUARD (IMPL,
code reading of `v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`); the (e′) drop-in is VERIFIED as an implication by
W2-VT24G §6 (three edits: statement, asymptotic paragraph, eligibility set); (d⁺) wiring in W2-BOOK §4. W4-T38FULL
(0) is the same inequality with the strict-maximiser step re-derived.

### Proof skeleton and crux
If π(S₀) > ½ then S₀ is the strict global maximiser; on {S₀ scored} ∩ {π(S₀) > ½} the HPM is S₀; Markov on δ₁.
Routes are inclusions. **No crux inside**; the content lives in the inputs: (P) from Thm 1, the route terms from
Thm 2/3/5. Remaining conditional inputs: GUARD (needs an independent code check: no guard path touches an RNG or a
setting), SR (implemented in `step_gibbs`; Felipe's confirmation pending), H03 = (P).

### Risk
Low for the inequality. The useful content of (e′) at n = 200 is only the multi-particle/distance-one form.

### Method change needed? No.
### P(true) 0.97 · P(provable) done

---

## Card 6 — Theorem 5: T38 two-regime consistency of the reported HPM (main theorem)

### Refined statement (W4-T38FULL Theorem 5, with the (b2) inputs replaced by W4-SHARE's envelope hypotheses)
Standing: EX-A, EX-S, CAL, SR, GUARD, regime R1 with the v3 budgets, and (P): δ₁ → 0 (Thm 1). Ŝ⁺ is the best model
in 𝒮⁺ = 𝒮 ∪ 𝒮_LS0 (= Ŝ without LS0). **LS0** := one extra production local search centred at the exact start mode
S̃₀ = argmax π₀ (max-plus convolution), **with its centre emitted as a score event**.

**(0) Composition, every n.** P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). If D_n → 0 then
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, hence liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup P(U). (The brief's "P(Ŝ = S₀) → 1 − limsup P(U)" is
not a well-formed limit.)

**(a) Favourable regime.** D_n → 0, with or without LS0, under (F): 1 − π₀(S₀) → 0, for which (F1)/(F2)/(F3) of
Card 3 are sufficient; the mechanism is T11(iii) (Q_f iid draws). All premises hold jointly on the ORTH family
(p < n).

**(b) Masked regime** (π₀(S₀) → 0 allowed at the T27 rate). D_n → 0 under any one route:
- **(b1) LS0.** A deterministic reference S° with Φ(S°) bounded such that (M1) P₀(π₀(S°) > ½) → 1 (sufficient:
  ZL(S°), SPREAD, VIS-lin(S°)); (M2) POP-LAT(S°, m_n): on Lat(S°) ∩ {Φ ≥ 2} some progress neighbour beats every
  non-progress neighbour and the state itself by m_n ≥ M_n√(log n/n) in population residual; (M3) λ_min(R_{S°∪S₀}) ≥
  φ₀², ‖μ‖²/n ≤ M; (OP-LS0). Then S̃₀ = S° and LS0 scores S₀ after ≤ Φ(S°) − 1 moves (cap ℓ_n ≥ Φ(S°) − 1 suffices).
- **(b1-LH)** On LH (exact Gram, p ≤ n−1, |ψ_i| < ρ, g ≤ B < 2g, fixed coefficients) with S° = S₀∖M: (P), (M1), (M2)
  with fixed margin m₀, (M3) all hold; π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; Q_f π₀(S₀) → 0 for c ≥ 2 (or c = 1 with
  p/(√n log²n) → ∞), so the iid route (a) fails. **With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical input.**
- **(b1-LH-iid)** The same on LH-iid with n^a ≤ p ≤ n^A (p ≫ n): W3-PXN P1–P8 + Cor, PROVED by one unverified run.
- **(b1′) D2, no method change.** If a one-flip neighbour x° = S₀ ⊕ j has π₀(x°) ≥ b > 1/10, dependence Dep ≤ 1 − c₁
  off a bounded set, and the no-blow-up event NB′ (ESS of the initial pilot weights ≥ 0.9H, or S₀ drawn) holds
  w.p. → 1, then the *first stage of the tier-0 pilot* scores S₀: P(S₀ ∉ 𝒮_cal) ≤ e^{−2Ht²} + P(NB′ᶜ) +
  exp{−H(1−Dep)₊g(b−t)/(k_D+B+3)}. Statistical instance: LH with c = 1 (D2-a,b,c PROVED by W3-PXN; NB PROOF SKETCH in
  two runs); c ≥ 2 OPEN.
- **(b2) Gibbs path, no method change.** Replace the bare DELIV by W4-SHARE's checkable envelope hypotheses:
  (TRACK) potentials h_t with h_T ≤ 1_W and (K_t h_t) ≥ (1−η_t)h_{t−1}; confinement sets 𝔛_t with P(Eᶜ) ≤ ε_E;
  fitness oscillation Γ = Σ_tΔ_tκ_t with Γ + Σ_tη_t ≤ log(Nπ₀(h₀)/T_e) − ω(1); and (REP) sup_{x∈W} β_{L+5}(x) → 0
  (Theorem B♯ with its asymptotic premises). Then P(S₀ ∉ 𝒮 | 𝓒) ≤ [ε_E + exp{−Nπ₀(h₀)(1−e^{−c})}]⁴ + ε_rep
  (Theorem B2-W4). No SHARE, no evidence lower tail LT. The threshold log N is sharp up to a factor 2 (Prop SH).
  Prop. M: under T03's hypotheses the within-𝓡_d path to S₀ is downhill in γ_φ for all φ ≥ φ_n → 0 (no
  posterior-level barrier), so the only obstruction is outsider competition plus exits. **No explicit family has
  these inputs verified: OPEN.**

**(c) Cost.** Scores ≤ T32(i)'s ceiling + (ℓ+1)max_k[p + k(p−k)] = O((n+p)(p+B)log²n + p²log²n); T32(i) is a
CONJECTURE (bookkeeping), so (c) is conditional.

**Not claimed.** Masked-regime evidence/PIP accuracy; anything given completion; comparative superiority; any
finite-n rate at n = 200; a masked p ≫ n instance until W3-PXN is verified; masked-regime consistency without LS0 on
any explicit family.

### Data evidence
- Favourable route at the study size: 1/2,394 fits favourable; Q_f ≈ 3·10⁵ against median π₀(S₀) ≈ 10⁻¹²:
  Q_f π₀(S₀) ≈ 3·10⁻⁷. (a) does not act at n = 200.
- Masked route at the study size: the HPM is delivered by Gibbs flips (98% of fresh scores) in the bridge/terminal
  rounds, not by the local search, and the misses are posterior misses. This is route-(b2)-like behaviour that no
  theorem yet covers; it is *not* evidence for (b1).
- Dilution: S̃₀ is 8–14 moves from S₀ at n = 200 (not a bounded Φ(S°)); LS0 post hoc on regenerated study data
  scored S₀ in 113/128 fits with |S̃₀ Δ S₀| ≤ ℓ + 1 and 13/32 beyond (S4/S6 at scale 0.5 fail or end at a
  better-scoring wrong model). LS0 cannot fix posterior misses. O-LS0 (Owls) is running LS0 on the 2,400 real
  datasets; nothing pushed yet beyond scripts.
- LH exact Gram, G = 12, g = 9 (p = 108), c ∈ {1,2,3}, n ∈ {200, 800, 3200}: S̃₀ = S° in 90/90; LS0 scored S₀ in
  90/90 (exactly c moves for n ≥ 800); lattice margin grows linearly in n (11 → 58 → 266 nats, c = 1).
- LH-iid, p ≈ n^{1.25} up to p = 10,120: S̃₀ = S° in 174/186 (all at n ≥ 400); LS0 scored S₀ in 185/186; the (L)
  certification margin fails with probability ≈ (s₀+1)/√(2π(n+1)t_n) (4% at n = 200, 1.2% at n = 1600): a posterior
  event, counted in 2E₀δ₁.
- C1 (delivery counterexample): start mass ≈ 1 on A, uniform bridge mass ≥ 0.9997, zero exits, yet every A particle
  dies in 56% (N = 10⁵) and 100% (N = 10⁶) of islands with a reversible kernel; Ẑ/Z < ½ in every island. In D5's
  terms Γ ≈ 72 ≫ log N, and the branching prediction 1 − exp{−Nπ₀(o)s}, s ≈ 0.153, reproduces 0.50 / 0.999.
- D2 end-to-end on CF(1): S₀ scored in stage 1 in 100/100 (n = 400) and 30/30 (n = 1600); but those instances are
  **not masked** (tier-0 iid miss 0.000); masking of CF(1) needs n ~ 10¹⁵. The honest D2 instance is LH, c = 1.

### Proof status and sources
| Piece | Source | Verifier |
|---|---|---|
| (0) composition; liminf form | W1-T38E T38(b)-R; W4-T38FULL (0) with Lemma RO/GUARD | W3-VT38E VERIFIED; W4 same-family |
| (a) under (F1)/(F2)/(F3); ORTH family | locked T11(iii), T22(iii); W1-EXP Thms 1/2/6; W4-T38FULL §2 | VERIFIED (W3-VEXP) for the inputs; ORTH composition unreviewed |
| E3 (LS0 eligibility, cost) | W1-T38E PROVED | W3-VT38E VERIFIED |
| E1 (brief's eligibility condition fails under omission masking) | W1-T38E PROVED (det.), margin sketch | VERIFIED |
| Lemma LS-score, Lemma M, Theorem b1, Prop. LH-LAT | W4-T38FULL PROVED | same-family referee VERIFIED (20 brute-force parameter cases; m₀ sharp) |
| (b1-LH) all premises on LH exact Gram | W1-EXP Thm 5 + W4-T38FULL | W3-VEXP VERIFIED (inputs); assembly unreviewed |
| (b1-LH-iid) p ≫ n | W3-PXN P1–P8 PROVED | **unverified** |
| D2 with r* and NB′ | W1-T38E + W3-VT38E §3.1 | VERIFIED; instance PROOF SKETCH |
| C0, C1 | W1-T38E COUNTEREXAMPLE | VERIFIED with a reversible kernel |
| Theorem D4/D5 (envelope delivery), Prop SH, Prop X, Prop M(a), Theorem B2-W4 | W4-SHARE PROVED; Prop M(b) PROOF SKETCH | **unverified; no REPORT yet** |
| (c) cost | T32(i) CONJECTURE + E3 | formula checked as a loose valid ceiling (W3-VT38E) |

### Proof skeleton and crux
(0): strict maximiser + Markov + Lemma RO. (a): T11(iii) on R̄. (b1): S̃₀ = S° from (M1); Lemma M converts the
population lattice margin into D_S on Lat(S°) on an event of probability → 1 (uniform χ²/Gaussian event over all
sets of size ≤ k + s₀, RSS floor through span(A ∪ S₀), deterministic prior/determinant/Q-vs-RSS bounds from E1);
Lemma LS-score then gives scoring. (b2): one-stage conditional-independence + convexity gives a supermartingale
of e^{−θ_t H_t/P_t} stopped at the envelope breach; the start term is Nπ₀(h₀). **Cruxes:** (1) verification of
Lemma M / LS-score / LH-LAT and of W3-PXN's Lemma B, which carry the whole masked instance; (2) for the no-change
routes, an explicit family where NB′ (b1′) or the envelope inputs (b2) are proved; the latter is where the n = 200
behaviour (Gibbs delivers) would eventually find a theorem, and F-SHARE is on it.

### Risk
- Validity: medium-low for (b1) (two unreviewed same-family-verified runs); medium for p ≫ n (single run).
- Overstatement: (i) T38 is not an explanation of the study's masking (dilution) or of its numbers; (ii) route (b1)
  is "nearly a restatement" unless POP-LAT is shown on a named family (it is, on LH); (iii) "D2 covers one-cancellation
  masking at p ≫ √n" is conditional and its CF instances are not masked; (iv) the cost corollary rests on a
  conjecture; (v) the LH packing condition g ≤ B < 2g excludes the study's groups of 5 (Prop. Q: co-blocking kills
  LH masking), so LH is a different masked mechanism from anything in the study.
- Method: LS0 is a method change under the investment rule (pilot evidence required); it must emit its centre, fix
  the argmax-π₀ tie rule, label refits; W3-PXN suggests letting LS0 run to certification because ℓ binds at n = 200.

### Method change needed? **Yes, LS0, for (b1)/(b1-LH).** No for (0), (a), (b1′), (b2).
### P(true) 0.98 (0) / 0.95 (a) / 0.9 (b1, b1-LH) / 0.8 (b1-LH-iid) / 0.6 (b1′ instance) / 0.5 (a (b2) instance exists on LH)
### P(provable) done, review pending (0, a, b1) / 0.75 (LH-iid verification) / 0.5 (b1′ NB on LH) / 0.3 (b2 instance)

---

## Card 7 — Theorem 6: T26 (i)–(ii) evidence and PIP consistency, favourable regime

### Refined statement (W2-T26 Theorem A; Theorem B as the discharged form)
EX-A, EX-S, CAL, START, OUT (on 𝒪 ∩ 𝒢_n the reported outputs equal the potential run's; on 𝒪 ∩ ℰ_n they are exact),
(Ω) P₀(s₀ ≤ K_n) → 1, and **one premise**
  (P1) P(𝒢_n ∩ {(T_n + 1)Δ_n > ε}) → 0 for all ε > 0, with Δ_n = max{1 − π₀(S₀), 1 − π(S₀)} (Lemma 1, exact),
plus its exact-branch twin (P1-ex). Then, never conditioning on completion:
- (A-0) for fixed n and 𝓒: E_𝓒|Ẑ°_r/Z − 1| ≤ b(𝓒) = 2(T+1)Δ_n/(1−Δ_n); occupancy off S₀ at the end of stage T and at
  every measured-round start ≤ min{1, 2δ₁ + 2b}; E_𝓒 max_j|PIP̂°_{rj} − 1{j∈S₀}| ≤ min{1, 2δ₁ + 2b} + ρ̄ + u_π with
  ρ̄ = 1 − ∏_e(1 − K_e(S₀, Ω∖S₀)) ≤ (B+3)u_π; P_𝓒(MPM̂° ≠ S₀) ≤ 2× that;
- (A-i) P(𝒪_n ∩ {|Ẑ/Z − 1| > ε}) → 0 (also islandwise and for log Ẑ);
- (A-ii) P(𝒪_n ∩ {max_j|PIP̂_j − 1{j∈S₀}| > ε}) → 0 and P(𝒪_n ∩ {MPM̂ ≠ S₀}) → 0.
The frozen second premise (L_n+4)ρ*_n → 0 is **redundant** (T15 re-controls occupancy at every terminal prefix).
**Theorem B (discharged):** in R1 under T03's hypotheses and (F1) of Card 3 (EXP′ removed), (P1) holds in the
deterministic-budget form (T^max+1)Δ_n = O_P(log²n [2^B√(log n)n^{−κ} + e_n + √(log n/n)]) → 0. Joint family: ORTH
(Prop. C, PROOF SKETCH).
Not claimed: P(𝒪_n) → 1; masked regime; secondary PIP; HPM; rates in N; completion-selected runs; floating point.

### Data evidence
Exact p = 18 scans (favourable iid and correlated designs, n up to 163,840): Δ_n ≈ c n^{−1/2}; with the realised grid
T ∈ {1, 2}, (T+1)Δ_n ≈ 0.02 at the largest n; **with the deterministic cap T^max = 4,000 it is ≥ 44**, so the
deterministic-budget form needs n ~ 10⁸–10⁹. The frozen P2 quantity is still ≈ 1.7 at n = 163,840 while the term
that enters is ≈ 0.03. All (A-0) bounds hold in exact-score SMC simulations with 30–200× slack. In the masked design
Δ_n → 1 (theorem silent) although the sampler still estimates Z within 1–2%. At n = 200 Δ_n ≈ 1 (dilution).

### Proof status and sources
W2-T26 Theorem A PROVED (composition of locked T14(i), T15, T23(ii-a,b), T22(iv-b), T09(ii), T12(i.a,i.b)); Lemmas
1–3 PROVED; Theorem B PROVED as a composition, CONDITIONAL on T03 + (F1); Prop. C PROOF SKETCH. **Unverified.**
W2-BOOK's Lemma RO/GUARD supplies OUT in the output form.

### Proof skeleton and crux
T14 telescoping for the evidence with η_t ≤ Δ_n; T15 occupancy at the end of stage T and at each measured-round
start; T23 pathwise for the PIPs; Markov. **No crux inside.** The content is (P1): start concentration at rate
o(1/T_n), i.e. Card 3's favourable inputs, and T03. The step to review is Lemma 3's use of T15 at a terminal-round
prefix (T12(i.b)); and OUT needs an implementation check that no failure mode returns a partial Ẑ or PIP.

### Risk
Medium-high on relevance (the longest hypothesis list; vacuous at the study size; deterministic-budget form vacuous
below n ~ 10⁸). Low on validity. Overstatement watch: state (P1) with the realised T_n (random), not with T^max,
and say so; keep "favourable regime only"; no masked-regime evidence claim even though the sampler empirically works
there.

### Method change needed? No.
### P(true) 0.95 · P(provable) done (needs one verifier)

---

## Card 8 — Proposition 2: T12 frozen-run identities (+ T31(i) Markov bound)

### Refined statement (W2-BOOK Prop 2)
Frozen object 𝓒 (tier, grid, T, N_e, L, 4 measured rounds, 4 islands, ℓ, inherited leaders), a function of the data
and streams 0–9; escalation decided before stream 10. On R̄ (the potential uninterrupted run), on the success event 𝒜:
- (a) islandwise: E[Ẑ_r | 𝓒] = Z and E[Ẑ_r · PIP̂_rj | 𝓒] = Z · PIP_j;
- (b) pooled: E[Ẑ | 𝓒] = Z and E[¼Σ_r Ẑ_r PIP̂_rj | 𝓒] = Z · PIP_j;
- (c) **not** an identity: E[Ẑ · P̄_j | 𝓒] = Z·PIP_j − ¾Cov(PIP̂_1j, Ẑ₁ | 𝓒), and E[P̄_j | 𝓒] − PIP_j = −Cov/Z (both
  non-zero in the locked instance: < −0.1275Z and < −0.17);
- (d) P(Z ≥ 0.05Ẑ | 𝓒) ≥ 0.95 (also islandwise); E[log Ẑ | 𝓒] ≤ log Z;
- (e) output level under GUARD: P(bound reported and 0.05Ẑ > Z) ≤ 0.05·P(𝒜); E[Ẑ·1{reported}] ≤ Z·P(𝒜); no
  unbiasedness given completion is claimed (COUNTEREXAMPLE: 0.22% stops give E[Ẑ | output] = 0.974Z);
- (f) floating point under VAL-FP(η, ε): P(reported and 0.05Ẑ^fp > Z) ≤ 0.05e^η + ε, with η, ε measured by replay.
The secondary PIP is removed. Run/output split applied to T11(iii), T14(i), T15, T23(ii), T25(iv), T31, T34 by
statement edits only.

### Data evidence
Exact law propagation (mpmath, 50 digits) reproduces the locked T12(iv.b) numbers; identities to 10⁻⁵⁰; pooled ×
pooled bias −0.13172 equals the ¾ closed form. Stops: 6/2,400, all S5. VAL-FP not measured (needs an R/C++ replay).

### Proof status and sources
Locked T12, T31(i) (wave 1, full chain incl. Fable + Astra review). W2-BOOK Lemma RO (PROVED), Prop 2 (PROVED as a
corollary), ¾-covariance formula (PROVED via locked island independence). GUARD is an implementation fact. Unverified
by a second run, but the new mathematics is a page.

### Proof skeleton and crux
Set inclusions (RO); expansion of Ẑ·P̄_j with island independence; Markov. No crux. The open items are operational:
the GUARD code check and the VAL-FP replay study.

### Risk
Low. Overstatement watch: islandwise wording; never "given completion"; the reported PIP is not unbiased.

### Method change needed? No.
### P(true) 0.97 · P(provable) done

---

## 9. Cross-cutting findings that change wording in several cards

1. **The study is pre-asymptotic in a way no frozen-setting theorem covers.** Dilution masking (6–12 of 14 truths
   absent from the start mode at every signal scale) vanishes for fixed s₀ under BM-∞ (W3-PXN Prop. W), so with
   s₀ = 14 at n = 200 the study sits in a regime the paper's theorems describe only as n → ∞. A fixed-s₀ dilution
   family with π(S₀) → 1 would need a sharp-constant T03 (CONJECTURE W′, P(provable) 0.3). Disclose; do not chase.
2. **Posterior misses, not discovery, are the binding error at n = 200** (565/2,394 vs 0). Every repair statement
   must be worded "whenever the posterior allows".
3. **Same-family verification is not review.** Every "VERIFIED" above is Opus checking Opus (or a fresh Opus
   subagent checking its own run in W4-T38FULL). Cross-family review (Astra) has not started.
4. **The 2^B factor** in the locked start rates makes them vacuous below n ≈ 10⁹ at B = 14–16; W3-PXN's
   Beta-truncation route is the only one without it (unverified).
5. **Implementation facts the theorems lean on:** SR (`step_gibbs` held + eval), GUARD (stop-only), the
   scan-before-limit rule of `local_search`, IND-T's sequential stream reading, and the LS0 `emit_centre` caveat.
   None has had an independent code audit.
