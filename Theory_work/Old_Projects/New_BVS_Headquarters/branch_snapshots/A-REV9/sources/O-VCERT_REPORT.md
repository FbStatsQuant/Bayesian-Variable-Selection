# O-VCERT — referee report on O-CERT (a-posteriori certificates)

Referee: O-VCERT (Opus 5.5), 2026-11-02, branch `theory/O-VCERT`. Object: `origin/theory/O-CERT` at `17e7f15`
(`theory_campaign/O-CERT/REPORT.md`, `scripts/`). Sources checked against: `00_COMMON.md` §1 (score), METHODOLOGY_v3
§§5, 6.10, 6.13, locked T12/T20/T31 STATEMENT.md files, W2-BOOK `PROOF.md` §§0–1 (Lemma RO, GUARD, Prop 2),
`theory_campaign/HQ/SR_AUDIT.md`, and the engine source `Scripts/SMC_BVS/core/cpp/` (ledger, final run, calibration
export). Independent code: `scripts/vcert_check.py`, written from `00_COMMON.md` only (not from O-CERT's `cert_lib.R`).
Output: `results/vcert_check.txt`. No helpers were spawned. Everything below is a referee verdict, not adoption.

## 1. Verdict table

| Item | Verdict | One-line reason |
|---|---|---|
| Lemma M (a) Q_S ↓ | **VERIFIED** | Push-through identity ⇒ Q_S = yᵀy/(n+1) + (n/(n+1))yᵀ(I+(n+1)M_S)⁻¹y; Loewner order reverses under inversion. 0 violations in 476,160 exhaustive (S, S+j) pairs. |
| Lemma M (b) D_S ↑ | **VERIFIED** | Determinant lemma; h(c) = 1 + c·xᵀ(I+cM)⁻¹x has h′ = xᵀ(I+cM)⁻²x ≥ 0 (derivative re-derived). log D rises by ≥ 5.6·10⁻³ per addition in every test, duplicates included. |
| Lemma M (c) w ↓ | **VERIFIED** | w(k) = ½/C(2p−1,k) is exactly the BB(1,p) per-model prior; ratio (k+1)/(2p−1−k) ≤ 1 for k ≤ p−1, and K ≤ p. |
| Lemma M (d) | **VERIFIED** | Both n×n forms agree with the k×k definitions to 8·10⁻¹³. |
| Thm C1 (a) | **VERIFIED** | Z ≥ Z_𝒯 holds deterministically. The engine's 𝒯 has distinct models (TopStore keyed by (F, S), and F is a function of S). |
| Thm C1 (b) identity and simultaneity | **VERIFIED** | {∃S: π(S) > u_α(S)} = {Z < αẐ} does not depend on S, so selecting Ŝ costs nothing. 0 mismatches over a grid of (𝒯, Ẑ, α). |
| Thm C1 (b) probability | **VERIFIED, conditional on W2-BOOK** | It is exactly W2-BOOK Prop 2(e1). The Lemma RO inclusions are elementary and I re-checked them. GUARD is an implementation hypothesis, not checked here. |
| Thm C1 (b), last sentence ("unscored and unreported" mass) | **GAP (wording; counterexample)** | The bound is on the mass **outside 𝒯**, not on the *unscored* mass. Counterexample in §2.1; repair R1. |
| Thm C1 (c) | **VERIFIED** (as a non-implication) | Correct use of T31(c). The prose built on it in §1, §5 and C6 overreaches; see S2. |
| Thm C2 | **VERIFIED (conditional on PW2)** | Cantelli is applied in the right direction. The bound is attained by a two-point law, so it is tight. Transfer to the output goes through Lemma RO(2). |
| Thm C3 (exact relative certificates) | **VERIFIED** | Z cancels. (c) holds for 𝒮̄ = the ledger's logical scored set, checked in the code (§3). |
| "Fully scored region" well defined | **VERIFIED, with a scope note** | C3 allows post-hoc rescoring, so any R is admissible. The run exports only 𝒯, the leader stores, Ŝ and the flags, so "scored by the run" in practice means 𝒯 or a recomputed region. |
| Thm C4 (box certificate) | **VERIFIED** | 0 Φ-violations and 0 M-violations over all 285,712 boxes on 48 designs (including p > n, duplicate and factor designs, and the binding cap K). B&B agrees with brute force 80/80, and the mass lower bound is valid 40/40. |
| Cor C5 | **VERIFIED, with a tie caveat** | Exact tie F(S₀) = F(Ŝ) with S₀ ≺ Ŝ: see S3. It also needs \|S₀\| ≤ K. |
| Thm C6 (card), exact arithmetic | **GAP (repairable)** | The probability space is right: unconditional, output level, via Lemma RO. But the G item "unscored mass ≥ 1 − Z_𝒯/(αẐ)" can be false on the good event (§2.1). With R1 the theorem holds. |
| Thm C6, floating-point clause | **GAP (repairable)** | It omits the SC(η_F) inflation of the G items: Z_𝒯^fp can exceed Z. Repair R2. |
| §4 illustration (p = 500) | **MISSING** | `results/` is not on the branch and §4 is empty at `17e7f15`. There are no reported numbers to reproduce (S4). |

No ERROR was found in the mathematics of Lemma M or C1–C5. The two GAPs that affect a theorem statement (C1(b)'s last
sentence, and C6) are repaired below.

## 2. Counterexamples

### 2.1 "Unscored" mass (C1(b) last sentence; C6 item G3; the C1 remark "the run has seen less than α of the posterior")
On {Z ≥ αẐ}, C1 gives π(Ω ∖ 𝒯) ≥ 1 − Z_𝒯/(αẐ). But Ω ∖ 𝒯 contains the models that were **scored but not reported**,
because 𝒯 is only the top-(40p+1) store. The *unscored* mass can be 0 while the claim is positive.

Instance (`vcert_check.py` §4): factor design, n = 40, p = 10. Every model is scored, so the unscored mass is 0, and
Ẑ = Z, so the good event holds. 𝒯 = the top-m models:

| m | α | claimed "unscored" mass ≥ | true unscored mass | true mass outside 𝒯 |
|---|---|---|---|---|
| 3 | 0.5 | 0.590 | 0 | 0.795 |
| 10 | 0.5 | 0.007 | 0 | 0.504 |

C1 allows any reported 𝒯, so this refutes the sentence as worded. With the engine's 𝒯 the same failure needs a
posterior that is diffuse beyond 40p+1 models, which is plausible at p = 500 under weak signals. O-CERT's own
`cert_run.R` prints the correct phrase ("posterior mass outside the top store"). The REPORT text disagrees with its own
code.

### 2.2 Floating point in the G items (C6 FP clause)
SC(η_F) allows F^fp(S) = F(S) + η_F on every S ∈ 𝒯. If most of the posterior sits in 𝒯 (Z_𝒯 ≈ Z), then
Z_𝒯^fp ≈ e^{η_F}Z > Z, and the "deterministic" bound π(Ŝ) ≤ e^{F^fp(Ŝ)}/Z_𝒯^fp can be false on every run. That leaves
an event outside the claimed α·e^η + ε. This is a logical gap, not an observed failure: η_F is tiny in practice.

## 3. Adversarial points checked (the brief's list)

1. **Direction of every inequality.**
   - Markov: P(Ẑ > Z/α) ≤ α gives a lower bound on Z, hence an upper bound on π(S) = e^F/Z. ✔
   - C1(c): {π(Ŝ) ≥ c·e^F/Ẑ} = {Ẑ ≥ cZ}, and T31(c) makes that event η-small. ✔
   - C2: {π(S) < (1−ε)e^F/Ẑ} = {Ẑ/Z < 1−ε}, a lower-tail event, so Cantelli with Var ≤ B_T/4 applies; x ↦ x/(x+ε²)
     is increasing, so substituting the variance bound is legitimate. ✔
   - Φ(L, U) takes w and D at L and Q at U. That is right, because w and D push F down as S grows, while Q pushes F up. ✔
2. **Lemma M against the actual score.**
   - HQ's premise needs a correction. Under BB(1,p), **both** the per-model weight w(k) and the size marginal
     C(p,k)w(k) are non-increasing in k: the marginal ratio is (p−k)/(2p−1−k) < 1. The object that is *not* monotone is
     the marginal likelihood m(S), and hence F. In the tests, m rises on 185,095 additions and falls on 291,065
     (`results/vcert_check.txt` §1).
   - Endpoint evaluation max(F(L), F(U)) underestimates the box maximum in 2,764 of 6,561 boxes. So the split into
     three separately monotone factors is essential, and O-CERT's Φ does it correctly.
   - Engine Q: the §6.13 branch Q = ‖y − X_Sβ̂‖² + (‖X_Sβ̂‖² + ‖β̂‖²)/n with β̂ = nH_S⁻¹z_S is algebraically the same
     function. Expanding gives yᵀy − 2zᵀβ̂ + β̂ᵀH_Sβ̂/n = yᵀy − zᵀβ̂.
   - Lemma M(d) gives Q_S ≥ yᵀy/(n+1). So the trigger Q < 10⁻⁸yᵀy can never fire in exact arithmetic when n + 1 < 10⁸;
     the branch is a pure floating-point safeguard. (A free corollary; it answers O-CERT §6's second escalation item.)
3. **Simultaneity in C1.** The bad event is S-free. VERIFIED, analytically and on a grid of (𝒯, Ẑ, α).
4. **"Fully scored region" and the ledger** (SR audit plus code):
   - `TopStore::offer` (`v3_ledger.h:47–55`) keeps exactly the top-cap distinct offered models. An evicted model can
     never re-enter, because the store's worst score only increases.
   - `offer_stores` updates the HPM and `top` together, so Ŝ = top[1] under the same total order.
   - Tables are offered through `ingest_tables` (`v3_core.cpp:369–383`).
   - Calibration keeps one persistent `CalState` across tiers (`v3_calib.R:139`). It exports its top-(40p+1) and both
     leader stores (`cpp_cal_export`), which the final run offers as "inherited" (`v3_core.cpp:409–419`).
   - Hence top[2] is the second-best model over the whole logical scored set, and C3(c) holds for 𝒮̄ read as SR's
     "offered at least once". On 𝒪, GUARD makes the reported store equal R̄'s.
   - Scope: no region other than 𝒯 has its scores in the output. Every other "region" certificate (local, subset, box)
     is post-hoc rescoring, which C3 explicitly allows.
5. **The probability space of C6.**
   - Every card claim is a function of (X, y) and the reported outputs.
   - On 𝒪 ⊆ 𝒢ᶜ these equal R̄'s by GUARD, and the deterministic claims hold surely.
   - The G claims fail exactly on 𝒪_E ∩ {Z < αẐ} ⊆ 𝒜 ∩ {Z < αẐ̄} (Lemma RO(2)), whose probability is ≤ α·P(𝒜) by
     T31(i)(a) integrated over 𝓒 (W2-BOOK Prop 2(e1)).
   - Nothing conditions on completion, and the conditional form α·P(𝒜)/P(𝒪) is only Lemma RO(4).
   - "Every data set" is right: P is over the streams and Ξ with the data fixed.
   - **VERIFIED in exact arithmetic, apart from the G3 wording (§2.1).**

## 4. Repairs

- **R1 (C1(b) last sentence, C6 G3, C1 remark).**
  - Replace "unscored and unreported" with "**not in 𝒯**". The claim π(Ω ∖ 𝒯) ≥ 1 − Z_𝒯/(αẐ) is then exactly right.
  - If an *unscored*-mass statement is wanted: let N̄ be any reported upper bound on the number of distinct scored
     models (the engine's score counter is one), and F_min := min_𝒯 F. Then, on the same event,
     π(unscored) ≥ 1 − [Z_𝒯 + (N̄ − |𝒯|)₊·e^{F_min}]/(αẐ).
  - Proof of the bound: every scored model outside a full store has F ≤ F_min. If the store is not full, every scored
     model is in 𝒯 and the correction is 0.
  - Change the remark to "the reported store holds less than α of the posterior".
- **R2 (C6 FP clause).**
  - Under SC(η_F), VAL-FP(η, ε), and a de-duplication of 𝒯 by model before summing, report
    u_α^fp(S) := exp(F^fp(S) + η_F) / max(e^{−η_F}·Z_𝒯^fp, α·Ẑ^fp).
  - The G claims then fail only on 𝒪_E ∩ {Z < αẐ^fp}, whose probability is ≤ α·e^η·P(𝒜) + ε (W2-BOOK Prop 2(f)).
  - The same inflation applies to the "outside 𝒯" item: 1 − e^{η_F}Z_𝒯^fp/(αẐ^fp). (The log-sum-exp rounding is
    absorbed into η_F.)

## 5. Smaller points (no verdict change)

- **S1.** C4(a) should state that leaves with |L| > K are empty and vacuously fine. C4(b)'s bound stays valid when Ŝ lies
  in a non-singleton leaf: it double-counts e^{F(Ŝ)}, which is conservative. Confirmed numerically.
- **S2.** §1 item 1, §5 first bullet and C6 "cannot certify confidence … without PW2 or enumeration" overstate C1(c).
  - C1(c) is a non-implication from the 𝓛(Z) properties only.
  - Any certified upper bound on Z gives a sure lower bound on π(Ŝ): the inventory's UB, a Lemma-M box cover of all of Ω
    (impractical at p = 500, as O-CERT §5 says), or T31's own remark Ẑ ≥ e^{−Δ}Z with Δ = max_Ω d − min_Ω d.
  - Reword as: "not from unbiasedness; it needs an upper bound on Z (PW2, UB, enumeration, or a bound on Δ)".
- **S3.** In C5, "posterior miss" needs F(S₀) < F(Ŝ), or F(S₀) = F(Ŝ) with Ŝ ≺ S₀. Under an exact tie with S₀ ≺ Ŝ,
  scoring S₀ would have changed the report, which makes it a search miss in the tie sense. Certify Φ(leaf) < F(Ŝ)
  strictly, or carry the HPM order. Exact ties are non-generic (T06). Also add |S₀| ≤ K.
- **S4.** §4 is empty and `results/cards.txt` is not committed. Every numeric claim of O-CERT (tree sizes, "cost grows
  like 2^{#ambiguous}", P(S₀ ⊄ U) "measured") is therefore unsupported as it stands. The "2^{#ambiguous}" sentence is a
  heuristic remark, not part of C4.
  - My small-p B&B used a natural variable order and visited a median of 272 nodes for |U| = 13 (8,192 leaves).
  - I did not reproduce the p = 500 runs: R and the study datasets are not on this laptop.
- **S5.** C1 and C6 inherit the unreviewed status of W2-BOOK (Lemma RO, GUARD, Prop 2). Lemma RO(1)–(4) are elementary
  inclusions, and I re-checked them. GUARD itself is a code fact that I did not audit.

## 6. Overall verdict per theorem

| Theorem | Overall |
|---|---|
| Lemma M | **VERIFIED** |
| C1 | **VERIFIED** (conditional on W2-BOOK Lemma RO/GUARD), with the last sentence replaced by R1 |
| C2 | **VERIFIED** as a conditional implication (PW2); not a data certificate, as O-CERT says |
| C3 | **VERIFIED** (with 𝒮̄ read as the SR logical scored set; code-checked) |
| C4 | **VERIFIED** |
| C5 | **VERIFIED** with the tie and K caveats (S3) |
| C6 | **GAP → VERIFIED after R1 and R2** (exact arithmetic: R1 only) |

## 7. Reproduction

- Command: `python -I scripts/vcert_check.py 20261102 results/vcert_check.txt` (about 5 min, 1 core).
- Sections of the script:
  1. Lemma M, exhaustive, on 150 designs: iid, AR(0.9), exact duplicates, near-duplicates, factor;
     n ∈ {5, 6, 12, 30, 40}, p ∈ {8, 9, 10}, so p > n is included.
  2. All boxes, with Φ and M, on 48 designs.
  3. My own B&B against brute force at p = 13.
  4. The C1 identity grid, the §2.1 counterexample, and the Cantelli tightness check.
