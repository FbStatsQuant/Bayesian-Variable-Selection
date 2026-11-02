# LOCKABLE — candidates for locking (Felipe's adoption decision)

Built by S-REGISTRY on 2026-11-02 from `REGISTRY.md`. **Rule** (strict): author status **PROVED** (not PROVED-UNDER) **and** same-family verdict VERIFIED (or VERIFIED after repair) **and** cross-family verdict VERIFIED (or VERIFIED with qualification). Items whose cross-family verdict is GAP/ERROR qualify only through a written repair (§2: W6-FIXREV1/2, same-family, not re-reviewed). This file lists candidates; it does not adopt, lock or upgrade anything, and VERIFIED here is a referee verdict on the stated hypotheses (the table's *Qualification* column must travel with the statement).

**Counts:** 35 strict candidates · 1 repaired by W6 but not re-reviewed · 64 same-family-only · 9 cross-family-only · 6 counterexamples confirmed by both · 2 conditional implications verified by both.

## 1. Strict candidates

| ID | Paper target | Source | Same-family | Cross-family (qualification) | Premises that must stay attached |
|---|---|---|---|---|---|
| `E1` | Thm 1 (T02 lemma) | W1-T03R · REPORT.md §1 · Lemma E1 | W2-VT03R · REPORT.md verdict table rows 1–4, VERIFIED (exact rational check, 2,779 triples) | A-REV2 · REVIEW.md §2 S03 Lemma E1(a)–(d) VERIFIED | p ≥ 2; (c) needs s₀ ≥ 1, m ≤ K−1 |
| `E2` | Thm 1 (T02 lemma) | W1-T03R · REPORT.md §1 · Lemma E2 | W2-VT03R · REPORT.md verdict table rows 6–7, VERIFIED | A-REV2 · REVIEW.md §2 S03 Lemma E2(i)–(iii) VERIFIED | s₀ ≥ 1 (or s₀ = 0 with n ≥ 5) |
| `E3-T03` | Thm 1 (T02 lemma) | W1-T03R · REPORT.md §1 · Prop. E3 | W2-VT03R · REPORT.md verdict table row 8, VERIFIED | A-REV2 · REVIEW.md §2 S03 Proposition E3 VERIFIED, only as a barrier for this cutoff/envelope route | Scope: Markov-numerator / S₀-denominator technique only |
| `den′` | Thm 1 (T02 lemma) | W1-T03R · REPORT.md §2 · Lemma den′ | W2-VT03R · REPORT.md verdict table row 9, VERIFIED | A-REV2 · REVIEW.md §2 S03 den′ and T02(i♯) VERIFIED (constant c♯ = κ²/(c_IG σ²), no stray 4) | G, R |
| `T02(i♯)` | Thm 1 | W1-T03R · REPORT.md §1 · Theorem T02(i♯) | W2-VT03R · REPORT.md verdict table row 10, VERIFIED | A-REV2 · REVIEW.md §2 S03 den′ and T02(i♯) VERIFIED; quantifier is sup_m P(Θ>L), not P(sup_m Θ>L) | G, R; cutoff must be deterministic |
| `LemmaI-B` | Thm 1 | W1-T03R · REPORT.md §1 · Lemma I (interlacing), Lemma B (B1–B3) | W2-VT03R · REPORT.md verdict table row 13, VERIFIED (9,000 random pairs) | A-REV2 · REVIEW.md §2 S03 Lemmas I/B VERIFIED | fixed g₀ > 0 (g₀,n → 0 not covered) |
| `T02(ii♯)` | Thm 1 | W1-T03R · REPORT.md §1 · Theorem T02(ii♯) | W2-VT03R · REPORT.md verdict table row 14, VERIFIED | A-REV2 · REVIEW.md §2 S03 Lemmas I/B and T02(ii♯) VERIFIED | R1, G, R, SE_w(m♯; g₀) |
| `T03♯` | Thm 1 | W1-T03R · REPORT.md §1 · Theorem T03♯ (i)–(v) | W2-VT03R · REPORT.md verdict table rows 12, 15–26, VERIFIED; no GAP/ERROR in the mathematics | A-REV2 · REVIEW.md §2 S03 T03♯(i)–(v) VERIFIED under exactly its fixed-design, fixed-s₀ hypotheses | R1, G, R, SE_λ(j₀), SE_w(m♯; g₀), BM-∞ or BM(c>c₀); fixed s₀; asymptotic only; proof thresholds n ≳ 2·10⁶; beta-min constant ≥ 43× above executed signals |
| `Prop1-TD` | Thm 3 (negative result → supplement) | W1-T37R · REPORT.md §2 · Prop. 1 | W3-VT37R · REPORT.md verdict table row 1, VERIFIED (720 designs, literal TD(2,0) in 0/720) | A-REV2 · REVIEW.md §2 S37 Proposition 1 and swap identity VERIFIED | s₀ ≥ 1, d ≥ 1, s₀+1 ≤ K |
| `Lemma0(a,c)` | Thm 3 | W1-T37R · REPORT.md §2 · Lemma 0 (a),(c) | W3-VT37R · REPORT.md verdict table rows 2, 2e, VERIFIED | A-REV2 · REVIEW.md §2 S37 Lemma 0(a),(c) VERIFIED; W6-FIXREV2 §3.1 disputes only A-REV2's table wording 'initial centre is the truth is trivial success' (needs (L) at S₀) | EX-A; completed scans |
| `TheoremA` | Thm 3 (Theorem A) | W1-T37R · REPORT.md §2 · Theorem A (A1)–(A4) | W3-VT37R · REPORT.md verdict table rows 5–8, VERIFIED (720 designs × 632 states, 0 violations; 'ℓ ≥ a+d is sufficient, exact need is τ(S_c)') | A-REV2 · REVIEW.md §2 S37 Theorem A(A1)–(A4) VERIFIED; A4 necessity must keep its quantifier; 'ℓ ≥ a+d' sufficient not necessary | EX-A; finite family 𝓡; production tie-broken greedy map |
| `A5(b)` | Thm 3 | W1-T37R · REPORT.md §2 · Theorem A (A5) second implication | W3-VT37R · REPORT.md verdict table row 10, VERIFIED (TD′_∞ in 198/200, TD′_P in 0/200 at n=3000) | A-REV2 · REVIEW.md §2 S37 TD′_P ⇒ TD′_∞; converse fails VERIFIED | region closure |
| `ThmB-T37(incl)` | supplement (finite-n union bound) | W1-T37R · REPORT.md §2 · Theorem B (inclusions and union bound) | W3-VT37R · REPORT.md verdict table row 12, VERIFIED (R6: headline '2^Φ states, no 2^{s₀}' only for a data-independent centre) | A-REV2 · REVIEW.md §2 S37 Theorem B union-bound use VERIFIED; response-selected centre needs a covering class | data-independent class 𝒞 ⊆ R_{a,d}; ℓ ≥ max Φ |
| `EXP′` | Thm 2 (ii) | W1-EXP · REPORT.md §Refined · Thm 1 | W3-VEXP · REPORT.md verdict table rows 1–5, VERIFIED (reproduced at p=8–24, n up to 1.6·10⁶) | A-REV2 · REVIEW.md §2 SEX Theorem 1 VERIFIED (exact expansion and bound); limiting constant 0.52 → 0.51 (flagged claim EXP-const) | G, R-lite(A,M), SE-blk; fixed X; uniform over a polynomial family; κ_EXP ≈ 100–1,700 nats at study SNR |
| `Thm3-EXP` | Thm 2 (iv) | W1-EXP · REPORT.md §Refined · Thm 3 | W3-VEXP · REPORT.md verdict table row 12, VERIFIED (needs a deterministic chain) | A-REV2 · REVIEW.md §2 SEX Theorem 3 VERIFIED (1.01 multiplier valid for n ≥ 400; not for a response-selected chain) | fixed deterministic chain, bounded chain leakage CL(L) |
| `Thm4-EXP` | Thm 2 (iv) | W1-EXP · REPORT.md §Refined · Thm 4 | W3-VEXP · REPORT.md verdict table row 13, VERIFIED | A-REV2 · REVIEW.md §2 SEX Theorem 4 (fixed CL, normalised H3) VERIFIED | H3 (π₀ of the chain's first set ≥ c₀ w.p. → 1) stays an explicit premise |
| `Thm4-growL` | Thm 2 (iv) | W1-EXP · REPORT.md §Refined · Thm 4 (growing L_n) | W3-VEXP · REPORT.md verdict table row 13 (wording) | A-REV2 · REVIEW.md §2 §5.3 growing-leakage bound VERIFIED as sufficiency | bound is sufficient only |
| `ThmB-T24` | supplement (Thm B′/B♯); Thm 4 route (e′) | W1-T24G · REPORT.md §1 · Theorem B (restated T24) | W2-VT24G · REPORT.md verdict table rows 'Theorem B': VERIFIED after Lemma F′ repair | A-REV1 · REVIEW.md §2 Theorem B, restated T24, finite inequality VERIFIED after F′ repair; statistical application remains GAP | EX-A, EX-S, SR, φ=1, H terminal rounds without resampling, s₀+a ≤ K; usefulness asymptotic only (vacuous at n=200) |
| `LemmaF` | supplement | W1-T24G · REPORT.md §1 · Lemma F | W2-VT24G · REPORT.md verdict table row Lemma F: GAP (closure hypothesis) fixed by F′ | A-REV1 · REVIEW.md §2 Lemma F as a standalone first-failure lemma VERIFIED; W1's use in B2 slot argument GAP repaired | closure of the family under non-failure (not satisfied in two uses) |
| `LemmaO` | supplement | W1-T24G · REPORT.md §1 · Lemma O | W2-VT24G · REPORT.md verdict table Lemma O VERIFIED | A-REV1 · REVIEW.md §2 Lemma O(i)–(iii) VERIFIED | — |
| `LemmaC` | supplement | W1-T24G · REPORT.md §1 · Lemma C | W2-VT24G · REPORT.md verdict table Lemma C VERIFIED (exact rational check) | A-REV1 · REVIEW.md §2 Lemma C and the block bound VERIFIED | — |
| `LemmaP` | supplement | W1-T24G · REPORT.md §1 · Lemma P | W2-VT24G · REPORT.md verdict table Lemma P VERIFIED | A-REV1 · REVIEW.md §2 Lemma P exact formula and single-target bound VERIFIED; informal multi-target sentence GAP (explicit version supplied) | — |
| `PropB1-B2` | supplement | W1-T24G · REPORT.md §1 · Props. B1, B2 | W2-VT24G · REPORT.md verdict table Prop. B1 VERIFIED; B2 VERIFIED after F′ | A-REV1 · REVIEW.md §2 B1 VERIFIED; B2 VERIFIED after F′ | — |
| `CorB-M` | supplement; Thm 4 route (e-M) | W1-T24G · REPORT.md §1 · Cor. B-M | W2-VT24G · REPORT.md verdict table Cor. B-M VERIFIED; wording GAP ('no η→0 needed' misleading) | A-REV1 · REVIEW.md §2 Corollary B-M VERIFIED under IND-T; does not prove eligible particles exist | (R5)=IND-T; past-measurable selection |
| `CorP1` | supplement | W1-T24G · REPORT.md §1 · Cor. P1 | W2-VT24G · REPORT.md verdict table Cor. P1 VERIFIED (numerics only at B=4) | A-REV1 · REVIEW.md §2 Corollary P1 VERIFIED | a₁ ≥ 0.14 shown only at B = 4; production B=14 order factor ≈ 1/17 unmeasured |
| `LemmaS-ineq` | Thm 5 (b1′) | W1-T38E · REPORT.md · Lemma S (ESS share inequality) | W3-VT38E · REPORT.md verdict table Lemma S VERIFIED (300,000 cases) | A-REV1 · REVIEW.md §2 Lemma S ESS share inequality VERIFIED | ESS ≥ eH |
| `D2` | Thm 5 (b1′) | W1-T38E · REPORT.md · Theorem D2 | W3-VT38E · REPORT.md verdict table Theorem D2 VERIFIED after the r* repair (NB′ weaker event) | A-REV1 · REVIEW.md §2 Theorem D2 with r*=(11+2√10)/9 VERIFIED as a finite uninterrupted-pilot bound | SR; x°ΔS₀={j}; π₀(x°) ≥ b > 1/10; Dep; NB′ (statistical instance unproved for any masked family) |
| `E3-core` | Thm 5 (b1) | W1-T38E · REPORT.md · Theorem E3 (i),(iii) and cost | W3-VT38E · REPORT.md verdict table Theorem E3 VERIFIED | A-REV1 · REVIEW.md §2 Theorem E3 core deterministic implication VERIFIED with centre scoring, completed scans, +1 centre evaluation in the score count | TD′ on the greedy region; T27-H3 constant > ½; LS0 emits its centre |
| `LemmaRO` | Thm 4 / Prop 2 (run/output split) | W2-BOOK · REPORT.md §2 · Lemma RO | W5-LOCKBOOK · REPORT.md verdict tables (W2-BOOK): CORRECT; 𝒪 = 𝒢ᶜ ∩ 𝒪̄ verified in code | A-REV4 · BOOK_CHECK.md 'RO: VERIFIED' for statistics extended by zero off their availability events; the potential statistic must be nonnegative (and bounded) on all of Ō, and RO gives no equality conditional on completion | GUARD (implementation fact: stop-only coupling) |
| `Prop2(c)` | Prop 2 | W2-BOOK · REPORT.md §2 · Prop. 2 (c) | W5-LOCKBOOK · REPORT.md verdict tables: CORRECT; ¾Cov/Z = 0.130481, relative bias −0.131716 reproduced to 10⁻⁵⁸ | A-REV4 · REVIEW.md verdict table: island identity and covariance VERIFIED (fixed data, frozen calibration, four conditionally iid potential islands; bias −¾Cov_C(PIP̂₁ⱼ, Ẑ₁)); A-REV4 Owls 50-digit finite-law reproduction (mpmath 1.3.0, PID 2508546, exit 0) matched −0.1739741778 (primary PIP bias) and −0.1317163950 (pooled relative bias), residuals ~10⁻⁵⁰ (numerical check, not an interval certificate) | — |
| `Prop1-T07` | Prop 1 | W2-BOOK · REPORT.md §2 · Prop. 1 (T07 + T06(i); (i′),(iii′) new) | W5-LOCKBOOK · REPORT.md verdict tables: (i′) sharpness CORRECT; (iii′) certificate CORRECT with amendment 'strict beyond numerical error' | A-REV4 · BOOK_CHECK.md: the sharp size-prior construction and its strict same-size certificate are sound; but see ERROR B5 on the data paragraph (claim Prop1-wrongHPM) | locked parts (T07(i)–(iii), T06(i)(a)); size-prior retuning can still move different-size errors |
| `T26-Lemma1` | Thm 6 | W2-T26 · REPORT.md §2 · Lemma 1 | W5-LOCKBOOK · REPORT.md verdict tables (W2-T26): CORRECT (grid check 66/66) | A-REV4 · REVIEW.md verdict table: W2-T26 Lemma 1 VERIFIED (endpoint identity, positive finite bridge, S₀ feasible) | — |
| `T26-Lemmas2-3` | Thm 6 | W2-T26 · REPORT.md §2 · Lemmas 2, 3 | W5-LOCKBOOK · REPORT.md verdict tables: CORRECT, including the flagged Lemma 3 step (T15 at a terminal-round prefix = T12(i.b)) | A-REV4 · REVIEW.md verdict table: W2-T26 Lemmas 2 and 3 VERIFIED (first departure and refreshed occupancy remove the L factor) | Lemma 3's use of T15 at a terminal-round prefix flagged for review |
| `T26-ThmA` | Thm 6 | W2-T26 · REPORT.md §2 · Theorem A | W5-LOCKBOOK · REPORT.md verdict tables: CORRECT; (A-0) constants 3x/27x/108x checked; OUT verified in code | A-REV4 · REVIEW.md verdict table: Theorem A, actual written statement, VERIFIED (EX-A/EX-S/CAL/START/OUT, feasibility, P1 and P1-ex; output-intersected conclusion only); the advertised single-premise shorthand is GAP (P1 restricted to successful SMC says nothing on the exact branch) | EX-A, EX-S, CAL, START, OUT, (Ω), one premise (P1): (T_n+1)Δ_n → 0 |
| `T38-(0)` | Thm 5 (0) / Thm 4 | W4-T38FULL · REPORT.md §2 · Theorem 5 (0) (= W1-T38E T38(b)-R composition) | W3-VT38E T38(b)-R composition VERIFIED; W4-T38FULL re-derives the strict-maximiser step | A-REV1 §7.4 repaired composition proof VERIFIED (same set argument as locked T21(C1)). Scope: A-REV1 reviewed W1-T38E's T38(b)-R, not W4-T38FULL (W6-FIXREV1 §3.1); the printed T38(b)-R as a whole is GAP; fixed by W6-FIXREV1's T38 files | GUARD, EX-A, EX-S, CAL, SR; (P): δ₁ → 0 (T03) |

### Strict candidates grouped by paper target

- **Thm 1 (T02 lemma)**: `E1`, `E2`, `E3-T03`, `den′`
- **Thm 1**: `T02(i♯)`, `LemmaI-B`, `T02(ii♯)`, `T03♯`
- **Thm 3 (negative result → supplement)**: `Prop1-TD`
- **Thm 3**: `Lemma0(a,c)`, `A5(b)`
- **Thm 3 (Theorem A)**: `TheoremA`
- **supplement (finite-n union bound)**: `ThmB-T37(incl)`
- **Thm 2 (ii)**: `EXP′`
- **Thm 2 (iv)**: `Thm3-EXP`, `Thm4-EXP`, `Thm4-growL`
- **supplement (Thm B′/B♯); Thm 4 route (e′)**: `ThmB-T24`
- **supplement**: `LemmaF`, `LemmaO`, `LemmaC`, `LemmaP`, `PropB1-B2`, `CorP1`
- **supplement; Thm 4 route (e-M)**: `CorB-M`
- **Thm 5 (b1′)**: `LemmaS-ineq`, `D2`
- **Thm 5 (b1)**: `E3-core`
- **Thm 4 / Prop 2 (run/output split)**: `LemmaRO`
- **Prop 2**: `Prop2(c)`
- **Prop 1**: `Prop1-T07`
- **Thm 6**: `T26-Lemma1`, `T26-Lemmas2-3`, `T26-ThmA`
- **Thm 5 (0) / Thm 4**: `T38-(0)`

Caveats that apply to the whole list: every proof is asymptotic or conditional on its stated hypotheses; none speaks to the n = 200 numbers (F-REFINE ARCHITECTURE §6–§7); implementation facts (GUARD, SR, emit_centre) are not audited theorems.

## 2. REPAIRED, not yet re-reviewed (author PROVED + same-family VERIFIED; cross-family GAP/ERROR; W6 repair written, same-family only)

These satisfy the rule through its "or repaired" clause, but the repair has **not** been seen by a second model family; treat as conditional candidates. A-REV re-review of the W6 text would promote them.

| ID | Cross-family finding | Repair |
|---|---|---|
| `PropU` | A-REV1 · REVIEW.md §2 Proposition U as written ERROR (independence moves can remove a truth; extra-for-extra swap can leave the phase-1 family) | corrected classification — applied in W6-FIXREV1 REPORT.md (same-family, not yet reviewed by a second family); Theorem B unaffected (uses the full §0 'bad' definition) |

## 3. NOT lockable under the rule — shown so nothing is mistaken for a candidate

### 3a. Author PROVED + same-family VERIFIED, no cross-family review yet

| ID | Paper target | Same-family | Note |
|---|---|---|---|
| `Lemma2-T37` | Thm 3 | W3-VT37R · REPORT.md verdict table row 3, VERIFIED (193 designs) | cross-family review pending |
| `Lemma3-T37` | Thm 3 | W3-VT37R · REPORT.md verdict table row 4, VERIFIED | cross-family review pending |
| `Lemma2.3` | Thm 2 | W3-VEXP · REPORT.md verdict table row 9, VERIFIED | cross-family review pending |
| `Thm6-EXP` | Thm 2 (iii) | W3-VEXP · REPORT.md verdict table row 11, VERIFIED (flat √n(1−π₀(S°)) ≈ 1.6) | cross-family review pending |
| `Lemma4.1-4.2` | Thm 2 (v) | W3-VEXP · REPORT.md verdict table rows 16–17, VERIFIED; \|ψ\|<ρ boundary sharp in effect | cross-family review pending |
| `Thm5-LH` | Thm 2 (v) | W3-VEXP · REPORT.md verdict table rows 18–21, VERIFIED (config A/B reproduced) | cross-family review pending |
| `PropD-drift` | supplement | W2-VT24G · REPORT.md verdict table Prop. D VERIFIED | cross-family review pending |
| `CorB-unif` | supplement | W2-VT24G · REPORT.md verdict table Cor. B-unif VERIFIED | cross-family review pending |
| `PropA-sweep` | supplement | W2-VT24G · REPORT.md verdict table Prop. A VERIFIED (proof); vacuous numerically | cross-family review pending |
| `T21-e′` | Thm 4 (route e′) | W2-VT24G §6 VERIFIED as an implication; W5-LOCKBOOK · REPORT.md verdict tables: (e′)/(e-M) CONSISTENT with VT24G's three edits, CORRECT given Lemma STREAM; eligibility = feasibility s₀+a(x) ≤ K | cross-family review pending |
| `LemmaA-T38E` | Thm 5 (supplement) | W3-VT38E · REPORT.md verdict table Lemma A VERIFIED (2,048,000 cases) | cross-family review pending |
| `LemmaB-T38E` | Thm 5 (supplement) | W3-VT38E · REPORT.md verdict table Lemma B VERIFIED (deterministic; 3,255 cases) | cross-family review pending |
| `D1` | Thm 5 (supplement) | W3-VT38E · REPORT.md verdict table Theorem D1 VERIFIED | cross-family review pending |
| `E1-T38E` | Thm 5 (supplement) | W3-VT38E · REPORT.md verdict table Prop. E1 VERIFIED (deterministic); margin = PROOF SKETCH | cross-family review pending |
| `Thm4-C1` | Thm 4 | W5-LOCKBOOK · REPORT.md verdict tables: (C1′), routes (a), (d) CORRECT, needs the convention 𝒢 ⊆ U (stopped fits return an incomplete HPM, G1) | cross-family review pending |
| `RO-splits` | supplement | W5-LOCKBOOK · REPORT.md verdict tables: T11(iii), T14(i), T15, T25(iv), T31, T34 edits CORRECT; T23(ii-d) output corollary GAP (false on the exact branch; restrict to SMC branch) | cross-family review pending |
| `T34-(v)` | supplement | W5-LOCKBOOK · REPORT.md verdict tables: split edit for T34 CORRECT | cross-family review pending |
| `PXN-P1` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table rows 8, 8′: VERIFIED given cited C1; margin condition is sufficient not necessary; partition = groups in 213/216 in-family replicates (misses at n ≤ 400 or ψ = 0.69) | cross-family review pending |
| `PXN-P2` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 9: VERIFIED given C1 | cross-family review pending |
| `PXN-LemmaB` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table rows 1–3′: Lemma B(i),(ii),(iii) VERIFIED (re-derived; 16 KS tests pass, negative controls rejected at p ≈ 0); also needs only the LH population identities, not \|ψ\|<ρ | cross-family review pending |
| `PXN-P3` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 7: VERIFIED (T22(i) bound ≤ π₀(S°) in 236/236 replicates) | cross-family review pending |
| `PXN-P4` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 10: VERIFIED (Mstat medians approach the limit from below; lag = log π₀(S°)) | cross-family review pending |
| `PXN-P5` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 11: VERIFIED (mode = S° in 195/216; misses at n ≤ 400) | cross-family review pending |
| `PXN-P6` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table rows 14, 15: VERIFIED (D_S > 0 at all lattice states in 105/110; 5 failures at n ≤ 400); (L) failure formula VERIFIED, 4%/1.2% quoted are for s₀ = 5 (R4) | cross-family review pending |
| `PXN-P8` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 18: VERIFIED | cross-family review pending |
| `PXN-Cor` | Thm 2 (v) / Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 19: composition via LS0 VERIFIED for every c; the no-LS0 branch (c = 1) rests on R1 (unverified) | cross-family review pending |
| `PXN-P7` | Thm 5 (b1′) | W5-VMASK · REPORT.md verdict table rows 16, 17: D2-a, D2-b, D2-c VERIFIED; D2-d (NB) GAP (fixable) → proof written in W5-VMASK REPAIRS R1 (single run, unverified) | cross-family review pending |
| `PGD-L1.1` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Lemma 1.1 VERIFIED | cross-family review pending |
| `PGD-L1.2` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Lemma 1.2 VERIFIED | cross-family review pending |
| `PGD-L1.3` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Lemma 1.3 VERIFIED | cross-family review pending |
| `PGD-P1` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Prop. P1 VERIFIED (the five non-progress types exhaust the moves) | cross-family review pending |
| `PGD-P2` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Prop. P2 (iff) and Cor. P2′ VERIFIED; brute force on block designs | cross-family review pending |
| `PGD-P3` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Prop. P3 VERIFIED | cross-family review pending |
| `PGD-P4` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Prop. P4 VERIFIED | cross-family review pending |
| `PGD-P5` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Lemma P5 VERIFIED; the LD♭ stability sentence is a GAP (G3, minor): true with O(ε/φ₀⁸) | cross-family review pending |
| `PGD-P6` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §1 Cor. P6 VERIFIED given the cited concentration bound; GAP G2 (uniformity of Theorem W's o(1) over designs with the same constants) and covariance→correlation passage not re-derived | cross-family review pending |
| `PGD-LQ` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §2 Lemma Q VERIFIED | cross-family review pending |
| `PGD-LR` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §2 Lemma R VERIFIED | cross-family review pending |
| `PGD-LG` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §2 Lemma G VERIFIED | cross-family review pending |
| `PGD-LU` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §2 Lemma U VERIFIED | cross-family review pending |
| `PGD-LLD` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §3 Lemma LD VERIFIED | cross-family review pending |
| `PGD-LS` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §3 Lemma S VERIFIED (constant not sharp; W5-VPGD STAR.md proves a sharpening ★′) | cross-family review pending |
| `PGD-LA′` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §4 Lemma A′ VERIFIED | cross-family review pending |
| `PGD-CorW′` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §4 Cor. W′(i),(ii) VERIFIED; random designs under (H3) GAP (G2/G3) | cross-family review pending |
| `ThmW` | Thm 3 (asymptotic clause) | W5-VPGD · REFEREE.md §4 and W5-VPGD REPORT.md §2: Theorem W VERIFIED (no ERROR in any step); four minor GAPs repaired in REPAIRS R1–R4, status after repair PROVED (candidate), one same-family referee pass; region form does not cover masked families (R6.1) | cross-family review pending |
| `LS-score` | Thm 3 / Thm 5 (b1) | W5-VMASK · REPORT.md verdict table row 20: VERIFIED by an independent run (code facts confirmed in v3_engine.h); IMPL caveat: LS0 must pass emit_centre = true (row 25) | cross-family review pending |
| `LemmaM` | Thm 5 (b1) | W5-VMASK · REPORT.md verdict table row 21: VERIFIED (every inequality; Lemma M needs λ_min only on A) | cross-family review pending |
| `LH-LAT` | Thm 3 (part C) / Thm 5 (b1-LH) | W5-VMASK · REPORT.md verdict table rows 23, 23″, 24: validity VERIFIED (m₀ ≤ brute-force margin in 202/202 settings; algebra needs only \|ψ\|<1); 'm₀ is sharp' GAP (overstatement): sharp in 108/108 homogeneous, not sharp in 32/94 heterogeneous, down to ×0.002 | cross-family review pending |
| `T38-b1-LH` | Thm 5 (b1-LH) | W5-VMASK · REPORT.md verdict table rows 20–24 and §9: LS-score, Lemma M, Thm b1, LH-LAT assembly VERIFIED by W5-VMASK (independent run) | cross-family review pending |
| `SHARE-D4` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: D4 Steps 1–5 VERIFIED; citation GAP only (conditional-iid step should cite IND-T/Lemma S of W2-PREM) | cross-family review pending |
| `SHARE-D5` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: D5 bound (2.1), consequence and Remarks 2–3 VERIFIED | cross-family review pending |
| `SHARE-G` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: Prop. G VERIFIED as an upper bound; wording GAP: it is not 'grid independence' of Γ | cross-family review pending |
| `SHARE-SH` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: Prop. SH (i),(ii) and exact law VERIFIED; 'transition at log(Nπ₀(a)/π₀(o))' is a heuristic (label it); factor-2 sharpness holds in the two-state example only | cross-family review pending |
| `SHARE-X` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: Prop. X main inequality VERIFIED; 'Moreover' clause GAP (needs a visit-form rate and an independence-proposal term N(T+L+4)π₀(S₀)); 'Use' clause GAP (calibration and final search not bounded) | cross-family review pending |
| `SHARE-M(a)` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: Prop. M(a) VERIFIED (20,000 random instances, 0 violations) | cross-family review pending |
| `SHARE-PD` | Thm 5 (b2) | W5-B2ENV · REFEREE.md verdict table: Lemma PD identity VERIFIED; 'a takeover needs these two premises' is a mean-field heuristic | cross-family review pending |
| `ADRAFT-ThmA` | none (original-draft track) | A-REV4 REVIEW.md table + §4 (Astra checking Astra's A-DRAFT: independent of the author's run, NOT cross-family relative to it): Theorem A and A1 VERIFIED (fixed-data bounded-functional LLN/MSE, unnormalised identities; no CLT, T16 conjecture not upgraded) | cross-family review pending |
| `ADRAFT-CorA1` | none (original-draft track) | A-REV4 REVIEW.md table + §4 (Astra checking Astra's A-DRAFT: independent of the author's run, NOT cross-family relative to it): A1 VERIFIED (pre-resampling identity; pooled product bias −¾Cov) | cross-family review pending |
| `ADRAFT-uniPIP` | none (original-draft track) | A-REV4 DRAFTS_CHECK §A-DRAFT §2 (Astra checking Astra's A-DRAFT: independent of the author's run, NOT cross-family relative to it): D7 checked (elementary detailed balance; no p-union-bound loss); does not prove output availability → 1 | cross-family review pending |
| `ADRAFT-ThmD` | none (original-draft track) | A-REV4 REVIEW.md table + §4 (Astra checking Astra's A-DRAFT: independent of the author's run, NOT cross-family relative to it): Theorem D and D1 VERIFIED with the explicit favourable-start premise (P1) and bounded-function/continuity qualifications; no masked-start or completion guarantee | cross-family review pending |
| `ADRAFT-CorD1` | none (original-draft track) | A-REV4 REVIEW.md table + §4 (Astra checking Astra's A-DRAFT: independent of the author's run, NOT cross-family relative to it): D1 VERIFIED (uniform local continuity and posterior contraction needed) | cross-family review pending |
| `PXN-LemmaTr` | Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table rows 4, 5: VERIFIED | cross-family review pending |
| `PXN-LemmaLambda` | Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 13: VERIFIED (brute-force Δ agrees) | cross-family review pending |
| `PXN-LemmaU` | Thm 5 (b1-LH-iid) | W5-VMASK · REPORT.md verdict table row 12: VERIFIED; ERROR (cosmetic) in (U1), see PXN-LemmaU-U1 | cross-family review pending |

### 3b. Cross-family VERIFIED but no independent same-family check (author = verifier, or no verifier run)

| ID | Paper target | Cross-family | Why not strict |
|---|---|---|---|
| `R1-POS` | Thm 3 | A-REV2 · REVIEW.md §2 §4.1 POS repair VERIFIED | authored by W3-VT37R (the verifier) |
| `R1-cert` | Thm 2 (ii) | A-REV2 · REVIEW.md §2 VEX R1 data-computable EXP′ certificate VERIFIED | authored by W3-VEXP (the verifier) |
| `IND-T` | supplement (Thm B′/B♯) | A-REV1 §5: VERIFIED for the uninterrupted process (stopping-time argument); completion conditioning / fresh-score sets not covered | authored by W2-PREM; no same-family verifier |
| `LemmaU-PREM` | supplement (premise table; shares proof with EXP′) | A-REV1 §3.4/§5 finite uniform expansion VERIFIED; A-REV2 §6 (U) VERIFIED on an explicitly budgeted family (extra-set quantifier GAP; limit constant ERROR; C3 lower bound ERROR — see flagged claims) | authored by W2-PREM; no same-family verifier |
| `C3-upper` | supplement | A-REV2 · REVIEW.md §2 §2 SU C3 zero-leakage upper bound VERIFIED | authored by W2-PREM |
| `LemmaF′` | supplement | A-REV1 · REVIEW.md §2 Lemma F′ VERIFIED | authored by W2-VT24G (the verifier) |
| `B1′/B2′-VT24G` | supplement | A-REV1 · REVIEW.md §2 B1′/B2′ scoring refinements VERIFIED with empty-supremum convention | authored by W2-VT24G (the verifier) |
| `LemmaE` | supplement | A-REV1 · REVIEW.md §2 W2's Lemma E correct | authored by W2-VT24G (the verifier) |
| `FD-W1` | none (original-draft track) | A-REV4 · DRAFTS_CHECK.md 'F-DRAFT W1: VERIFIED' (block-diagonal G, H; d = 0 iff at most one block has signal; with known common variance the globally prior-coupled start equals the posterior, including the cap; not a product of local posteriors) | none |

### 3c. Counterexamples confirmed by a same-family verifier and by A-REV1/A-REV2 (candidates for locking as negative results)

| ID | Statement | Same-family | Cross-family |
|---|---|---|---|
| `PropD-T03` | With duplicated columns the posterior size-tail does not vanish at cutoff s₀+O(1): the target 'm_n = s₀+O(s₀ log n/log p)' is false without SE. | W2-VT03R · REPORT.md verdict table row 11, VERIFIED (reproduced analytically and numerically) | A-REV2 · REVIEW.md §2 S03 Proposition D VERIFIED (G and R only; violates even size-two SE) |
| `C3-PGD` | SE and beta-min do not imply progress-greedy dominance: a null that looks like a combination of two truths is added first. | W3-VT37R · REPORT.md verdict table row 15, VERIFIED (exact population values R⁺=0.090, R⁰=0.130) | A-REV2 · REVIEW.md §2 §4.1 combination-proxy example independently reproduced |
| `CEX1` | At d = 0 literal strict TD can hold while the best addition from ∅ has negative gain: positivity is missing, so the original T37(i) is false even at d = 0. | authored by W3-VT37R; reproduced in-run | A-REV2 · REVIEW.md §2 §4.1 independently reproduced (gain −2.2977998984) |
| `CEX2` | A search can start below S₀, climb to a superset and certify it: a final-search failure does not imply the initial centre already beat S₀. | authored by W3-VT37R; production rerun 233/234 | A-REV2 · REVIEW.md §2 §4.2 independently reproduced (−2.2862503005, +7.2109846558) |
| `CE1` | At boundary states a look-alike of a missing truth exits with probability ≥ (1−o(1))/(B+d+4), so H24's uniform exit input cannot be discharged. | W2-VT24G · REPORT.md verdict table CONFIRMED (MC 0.62–0.98 in S2–S6; exact lower bound ≥ 0.39); wording GAP: 'H24's asymptotic input (L+4)η_n → 0 is false' | A-REV1 · REVIEW.md §2 deterministic exit lower bound and finite obstruction VERIFIED; broad asymptotic wording GAP |
| `CEX-guard` | A guard that stops 0.22% of runs makes E[Ẑ \| output] = 0.974Z: unbiasedness does not survive conditioning on completion. | W5-LOCKBOOK · REPORT.md verdict tables: CONFIRMED, reproduced exactly; also under the engine-faithful cost rule (bias can be upward) | A-REV4 · BOOK_CHECK.md: 'path-dependent stopping can invalidate conditional unbiasedness' VERIFIED qualitatively by an analytic example; BOOK's cost example is stylised and does not establish the size or direction of production bias |

### 3d. Conditional theorems (PROVED-UNDER) whose implication is verified by both families

| ID | Paper target | Premises | Cross-family |
|---|---|---|---|
| `T38b-R(b1)` | Thm 5 (b1) | ELIG (S̃₀ in the basin), TD′ at S̃₀, OP-LS0; LS0 method change | A-REV1 · REVIEW.md §2 route (b1), direct ELIG+TD′+OP VERIFIED |
| `T26-ThmB` | Thm 6 | T03's G,R,SE,BM and T22(iii)'s (F1); deterministic-budget form vacuous below n ~ 10⁸ | A-REV4 · REVIEW.md verdict table: Theorem B VERIFIED as a conditional composition of locked T03 and T22(iii); EXP′/VIS/NL remain assumptions |

### 3e. Headline items with NO verification at all (author only)

`PropD′-T03`, `LemmaA1`, `V1-TDfails`, `PropD-dilution`, `PropT2-PREM`, `NL0(0)/UDEL(1)`, `NL0(a)/UDEL(a≥2)`, `B1′-PREM+PA`, `TS`, `FS/TL♯/ULR`, `ThmB♯`, `IND-M`, `CorA-PREM`, `T32(i)`, `Lemma-STREAM`, `Impl-lemmas`, `ADRAFT-v3exact`, `ADRAFT-SMCcomp`, `FD-W0`, `FD-W(a)`, `FD-W″-two`, `FD-P`, `FD-H`, `OCERT-LemmaM`, `OCERT-C1`, `OCERT-C2`, `OCERT-C3`, `OCERT-C4`, `OCERT-C5`, `OCERT-C6`, `OSWAP-L0`, `OSWAP-P1`, `OSWAP-P2`, `OSWAP-P3`, `OSWAP-T4`, `OSWAP-P5`, `W6F1-PropU′`, `W6F1-ThmB-conv`, `W6F1-LemmaP`, `W6F1-LemmaS′`, `W6F1-D2inf`, `W6F1-E3′`, `W6F1-LemmaU′`, `W6F1-NL0′`, `W6F1-CE1′`, `W6F1-T38`, `W6F2-LemmaT`, `W6F2-LemmaNT`, `W6F2-Lemma0′`, `W6F2-PropF`, `W6F2-ThmA′`, `W6F2-rest`, `VMASK-R1-NB`, `VPGD-R0`, `VPGD-R1`, `VPGD-R2`, `VPGD-R3`, `VPGD-PropT`, `VPGD-WLat`, `VPGD-equiv`, `VPGD-LH-PGD`, `VPGD-PropS′`, `OBG-LemmaR`, `OBG-BG1`, `OBG-CorBG1inf`, `OBG-LH-P1`, `FAV-LemmaX`, `FAV-LemmaBp`, `FAV-LemmaTrp`, `FAV-LemmaM`, `FAV-LemmaS`, `FAV-LemmaG`, `FAV-ThmA`, `FAV-LemmaP1p`, `FAV-ThmB`, `FAV-LemmaXminus`, `FAV-PropF`, `FAV-C1`, `FAV-C2`, `FAV-C3`, `FAV-PropB1`, `OWS-WS1`, `OWS-WS2`, `OWS-WS3`, `OWS-WS4`, `OWS-WS52`, `OWS-WS53F`, `OWS-WS53M`, `OWS-WS53N`, `OWS-WS6abc`, `OWS-WS6d`, `OWS-WS7`, `OWS-WS8abc`, `B2E-LemmaOF`, `B2E-L2.1`, `B2E-L2.2`, `B2E-NBLH`, `B2E-D2LH`, `B2E-MLH`, `B2E-LemmaJ`, `B2E-LemmaT`, `B2E-CONF`, `B2E-LemmaR1`, `B2E-B2LH`

Largest holes (no cross-family review at the last fetch): Prop 1 and Prop 2 beyond the A-REV4 items (`Prop1-T07`, `Prop2*`: A-REV4 reviewed Lemma RO, the island identity and the Markov bound, and found GAP/ERROR items that are NOT yet repaired); `Thm4-C1`, `T21-e′`; the W3-PGD / W5-VPGD family (`ThmW`, `PGD-*`, `VPGD-*`: same-family only); the W3-PXN family and W4-T38FULL lemmas (`PXN-*`, `LS-score`, `LemmaM`, `LH-LAT`: second same-family verdict from W5-VMASK; A-REV3 had not landed); W4-SHARE (`SHARE-*`: same-family W5-B2ENV; A-REV3 not landed); and everything marked author-only in 3e: W5-VMASK R1, the W5-VPGD repairs, O-BGIBBS (Lemma R, BG1), W5-FAVIID, W5-B2ENV PROOF.md, O-WSTAB, O-CERT, O-SWAP.
