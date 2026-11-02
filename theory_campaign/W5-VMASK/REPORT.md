# W5-VMASK — REPORT: adversarial verification of the masked-regime instance of T38 (W3-PXN, W4-T38FULL)

Run of 2026-11-02, branch `theory/W5-VMASK`, referee of `theory/W3-PXN` (REPORT, PROOF §§0–14, scripts, results) and of
`theory/W4-T38FULL` (T38_STATEMENT, T38_PROOF §§1–3, scripts). Inputs re-read: W1-EXP PROOF §§1, 4; W3-VEXP REPAIRS R3;
W1-T37R PROOF (Lemma 2, Thm A); W1-T38E PROOF (§4 D2, §6 E1–E3, §7); W3-VT38E REPORT (NB′, r*); `00_COMMON.md`;
locked T22 STATEMENT; `v3_blocks.h`, `v3_start.h::start_mode`, `v3_engine.h::local_search` and `::eval`.

**Status words.** These follow PROTOCOL. In the verdict table, **VERIFIED** means checked line by line here.
**GAP** and **ERROR** are qualified as in the task. Every result is a **candidate** pending cross-family review: this
run is the same model family as the two runs it checks.

**Independence of the numerics.** All numbers below come from code written in this run (`scripts/vm_core.py`):
- my own scorer, from the 00_COMMON formulas;
- my own port of the v3 partition, from `v3_blocks.h`: complete linkage on 1−|r|, the R13 union-lex tie rule and
  left-child rule, the top-down cut and next-fit packing;
- my own start law (exact convolution, max-plus mode, T22 q and e);
- my own production local search;
- my own LH generator, using a unit-wise Cholesky factor where PXN used a factor construction.

No PXN or T38FULL code is imported. The library is checked against brute force in `results/sanity.txt`:
- add-scan vs direct scores: 1e-14;
- log π₀ by convolution vs enumeration: 2e-14;
- the mode;
- my linkage port against scipy: 20/20 identical dendrogram cluster sets.

## 1. Headline

1. **Thm 5(b1-LH-iid) survives adversarial verification.** It can be cited as **PROVED (candidate), verified by a
   second same-family run, pending cross-family review**; it no longer has to be a single-run claim. Every step was
   checked line by line and none failed:
   - W3-PXN Lemma B, Lemma Tr, P1–P6 and P8;
   - the general-set use of W1-EXP Lemmas 1.1/1.2/1.4;
   - W4-T38FULL's LS-score, Lemma M, Theorem b1 and LH-LAT.

   The defects found are cosmetic: one wrong numerical constant (R2), one overstated "sharp" (R5), one unlabelled
   s₀ (R4), the inherited NB constant (R3), and an off-by-one in the cost (R7). None affects a conclusion.
2. **The one non-PROVED step of route (b1′), PXN's D2-d (NB), is closed** by a complete proof in `REPAIRS.md` R1
   (PROVED, candidate, this run only). With it, the **original method, with no LS0, scores S₀ in the first pilot round
   w.p. → 1 on LH-iid for c = 1** (Theorem 5(b1′)). For c ≥ 2 the no-tweak route stays OPEN.
3. **The two runs' lattice margins agree.** PXN's c₂ and T38FULL's m₀ are both valid lower bounds on the brute-force
   population margin of LH exact Gram, in all 202 settings checked (0 violations). m₀ is exact on homogeneous pairs
   (108/108). On heterogeneous pairs it can be loose by up to ×500 (R5).
4. **Independent reproduction agrees with both runs to within replicate noise.**
   - LH-iid configs A and B at n ∈ {200, 400, 800}: for example, median log₁₀π₀(S₀) is −3.94/−4.42/−4.89 (A) and
     −7.32/−8.32/−9.23 (B), against PXN's −3.91/−4.38/−4.97 and −7.37/−8.36/−9.27.
   - LH exact Gram (G = 12, g = 9): reproduced cell by cell, now with the actual partition, which equals the groups
     90/90. T38FULL had assumed it.
   - Lemma B KS tests: 16 tests pass, and both negative controls are rejected at p ≈ 0.
   - (L) failure rate: matches the first-order formula.
5. **Adversarial designs confirm the boundaries and do not break the theorems.**
   - ψ = 0.69 against ρ = 0.7: the actual partition ≠ groups in 2/10, 1/10, 0/6 at n = 200, 400, 800. This is a finite-n
     failure of P1 that vanishes as the theorem says.
   - Null groups with within-group correlation 0.95 > ρ: SE-blk drops to 0.03, but every conclusion holds.
   - ψ = 0.8 > ρ (outside the family): the partition co-blocks the hubs and **the masking disappears**
     (π₀(S₀) ≈ 0.6 at n = 400). It is not a failure of the method.

## 2. Verdict table

Abbreviations: "PXN §k" = W3-PXN PROOF.md section k; "T38P §k" = W4-T38FULL T38_PROOF.md section k.

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | **PXN Lemma B(i)**: X_{h,V} ~ Beta(\|V\|/2, (n−1−\|U_h°\|−\|V\|)/2), free of y | VERIFIED | F1 re-derived: Σ[C_b, j_a] = ψΣ[C_b, j_b] ⇒ Cov(X_{C_b}, μ_i) = 0. F3: Cov(C_a, C_b \| x_{j_a}) = ψuvᵀ − u·ψvᵀ = 0. Weak union for U ⊋ {j_a}. W^r = X_W − X_UΓ is uncorrelated with (X_U, μ), hence independent of (X_U, y). span(Π_E W^r) is Haar on the Grassmannian of E, which gives the Beta law. KS (2000 reps): B1–B4 p ∈ [0.21, 0.79] |
| 2 | **Lemma B(ii)** (neutral additions, case β, A ⊇ S°) | VERIFIED | Same argument. Components are independent (F5). The a-group case uses weak union. KS B5, B6: p ∈ [0.07, 0.89] |
| 3 | **Lemma B(iii)** (masked hubs independent of y; (n−1)r̂² → independent χ²₁) | VERIFIED | The c+1 Gaussian vectors are uncorrelated. KS of r̂² ~ Beta(½, (n−2)/2): p = 0.022 at 2000 reps (one of 20 tests), then p = 0.15 at 20,000 fresh reps. Independence χ²: p = 0.42, 0.18 |
| 3′ | Lemma B needs only the LH population identities, not \|ψ\| < ρ | VERIFIED (new) | All KS tests also pass at ψ = 0.9 > ρ; controls N1, N2 are rejected at p ≤ 1e-65 (`results/ks_lemmaB.txt`) |
| 4 | **Lemma Tr(a)** truncated moment | VERIFIED | Exponent (m−j)/2 − 1 − ν = −e₁. Γ(y+a)/Γ(y) ≤ (y+a)^a for integer a and (by Wendel) half-integer a. (2/j)/Γ(j/2) = 1/Γ(j/2+1) |
| 5 | **Lemma Tr(b), (c)** | VERIFIED | X ≤ χ²_j/χ²_{m−j}. With x = t′/2 − √(jt′) − j: j + 2√(jx) + 2x ≤ t′ − j, so the Laurent–Massart bound gives n^{−(A+3)}e^{O(√log n)}. Union over n^{A+1}2^{17} → 0 |
| 6 | W1-EXP L1.1, L1.2, L1.4 never use block membership | VERIFIED | L1.1 uses only λ_min(G_S) ≥ φ²(n−1) and ‖y‖² = n−1. L1.2's *statement* says T ⊆ C_b, but its proof uses only the Schur complement and λ_min. L1.4 uses block size only through the count 2^{16}p and dim W ≤ 17. For sets of size ≤ s₀+2 the count becomes (p+1)^{s₀+2}, dim W ≤ s₀+3 and L > 4A(s₀+3), as PXN says |
| 7 | **PXN P3**: 1 − π₀(S°) = O_P(√(log n/n)) | VERIFIED | Chain telescoping to 1 − X_{h,V}. On 𝒢_n, Lemma Tr(a) with mτ_n ≤ t_n. j!C(g,j) ≤ g^j and Γ(j/2+1) ≥ 0.88. Jensen on E[(j!ã)^{1/j}1_𝒢]. D_b = max ≤ Σ. q̃ sums over p/g groups. The e-term uses the a-group partial covariance β(1−ψ²)Var(x_{j_a}\|X_U) ≠ 0 (re-derived). T22(i-a). Numerics: T22(i) bound ≤ π₀(S°) in 104/104 (A, B) and 158/158 overall; √(n/log n)(1−π₀(S°)) has median 1.5–2.8 |
| 8 | **PXN P1**: partition = groups w.p. → 1 | VERIFIED (given cited C1) | The deterministic part matches `v3_blocks.h` exactly: merge order, R13 union-lex ties, left child by min index, cut "size ≤ B ⇒ retain, else push right then left", next-fit "cur + c > B ⇒ new block". Laminarity needs only D_in < D_out, and any tie rule works. The probabilistic part uses η = (ρ − max\|ψ\|)/3. Actual partition = groups: 104/104 (A, B), 30/30 (null ρ = 0.95), 50/50 (ψ = 0.65), 23/26 (ψ = 0.69) |
| 8′ | "Margin condition used when p > 4300" | VERIFIED (sufficient, not necessary) | It held in 86/104 A/B replicates, and the actual partition was groups in all 104. At ψ = 0.65 it held in 1/50, with the partition still groups in 50/50. Using it at p = 10,120, n = 1600 (where it holds w.p. → 1) is legitimate |
| 9 | **PXN P2** (SE family, R, BM-∞, G) | VERIFIED (given C1) | ‖R̂_T − Σ_T‖ ≤ k_nC₁√(log p/n) = O(log^{3/2}n/√n). Interlacing. The SLLN applies to finitely many columns |
| 10 | **PXN P4** (limit law of Mstat) | VERIFIED | One-column table: G = n−1, H = n², det(G+1) = n, D = n, Q = (n−1) − (n−1)²r̂²/n, so log r + ½log n = −ν log(1 − κ_nr̂²). Prior ratio → Σlog((s+i)/2). Slutsky. Numerics: Mstat medians 0.21 → 0.43 (A, limit 0.63) and 1.69 → 2.15 (B, limit 2.30). The lag equals log π₀(S°), as PXN found |
| 11 | **PXN P5** (S̃₀ = S° w.p. → 1) | VERIFIED | π₀(S°) > ½ ⇒ unique mode. Numerics: mode = S° in 52/52 (A) and 49/52 (B; the misses are at n ≤ 400: one proxy-for-hub, two null extras) |
| 12 | **PXN Lemma U** (U1)–(U3) | VERIFIED; **ERROR (cosmetic)** in (U1) | "ν log(1 + a/RSS^y) ≤ ν(1.02+…)/(c_*n) ≤ 1" is false, since c_* ≤ 1/16 makes it ≈ 0.51/c_* ≥ 8. Only κ₂ = O(1) is used. Repair R2 |
| 13 | **PXN Lemma Λ** (population residuals) | VERIFIED | (a): the null-column removal is Beta(\|A₀\|/2, ·) because nulls are independent of X_𝒮𝒱, and μ is a function of X_𝒮𝒱. (c): every value re-derived, e.g. Var(x_{j_b} \| x_{j_a}, x_l) = (1−ψ²)(1−η) with η = ρ²(1−ψ²)/(1−ψ²ρ²). Brute-force Δ agrees (margins grid) |
| 14 | **PXN P6** (TD′ lattice condition at S°: D_S and (L)) | VERIFIED | Every neighbour class checked, including the truth→truth swap (margin β²(1−ψ²)²) and the visible swap. (L): RSS_{S₀+l}/RSS_{S₀} = 1 − Z_l²σ²/‖Π^⊥_{S₀}Cε‖², max Z² ≤ 2log p + 2loglog n, and −log((2p−s₀−1)/(s₀+1)) + log p → log((s₀+1)/2). Numerics: sample D_S > 0 at all lattice states in 99/104 (A, B). The 5 failures are at n ≤ 400, with margins −0.4 to −3.6 nats |
| 15 | PXN (L) failure rate ≈ (s₀+1)/√(2π(n+1)t_n) | VERIFIED; labelling note | Simulated (config A): 2.47%, 1.47%, 0.80%, 0.67% at n = 200, 400, 800, 1600, against the formula's 2.72%, 1.80%, 1.20%, 0.81%. Config B: 3.60% and 2.93% against 4.18% and 2.76%. PXN's quoted 4%/1.2% are for s₀ = 5 (config B), not stated (R4) |
| 16 | **PXN P7** D2-a, D2-b, D2-c (Dep = O_P(√(log n/n))) | VERIFIED | κ₀ additions: Σ ≤ (s+1)q. κ₀ deletions: ≤ e/s. κ₁ additions: Lemma B(ii) + Lemma Tr with j = 1. κ₁ deletions: Θ(n) loss. Numerics: median Dep 0.63/0.31/0.25 at n = 200/400/800 (PXN: 0.46/0.40/0.31) |
| 17 | **PXN P7 D2-d (NB)** | **GAP (fixable) → repaired, R1** | What was missing: (i) the bound π₀(S ⊉ S°) ≤ 2^{s+1}e_T, which needs the mass between sizes K and K+s (the map S ↦ S ∪ S° leaves Ω), handled by the q-generating function; (ii) the full-set EXP′ and RSS floor over sets of size ≤ s+k₀+1, plus the block-level Beta law for U ⊋ U_h° (Lemma B(i′), R6); (iii) Lemma Tr(c) with family exponent A(k₀+1); (iv) the NB constant 1.925 → r* (R3). All four are written in R1, which is a complete proof |
| 18 | **PXN P8** design de-randomisation lemma | VERIFIED | The sup/contradiction argument is correct. Conditional laws are well defined because ε ⊥ X. T03's hypotheses hold on 𝒜′_n with fixed constants |
| 19 | PXN Cor (b1): T38(b) on LH-iid via LS0, every fixed c | VERIFIED (composition) | [T38E-R] with 𝔅_n = {S°}: ELIG from P5, TD′ from P6, H-T03 from P8 |
| 20 | **T38FULL Lemma LS-score** | VERIFIED | Lattice closure (W1-T37R Lemma 2(a)). Engine facts confirmed in code: the scan precedes `if (A.moves >= ell)`; the centre is scored only through `eval(C, ME_LOCAL, emit_centre)`, whose `emit` flag gates the ledger event; production calls pass `false`. The Φ = 1 case: S₀ is a feasible flip neighbour |
| 21 | **T38FULL Lemma M** | VERIFIED | Every inequality checked: w ratio ∈ [1/(2p), 1]; D ratio ∈ [1/n, n+1]; Q ≥ RSS^y; the Q upper bound under λ_min; E1/E2/E3 counts (L/4 = A(k+s₀)+1); RSS_S expansion with P_Se = P_Sε; RSS_A ≥ ‖(I − P_{A∪S₀})e‖²; s_y² ≤ 2C_R; log x ≥ 1 − 1/x |
| 22 | **T38FULL Theorem b1** | VERIFIED (under M1–M3) | A_S ⊆ S° ∪ S₀ gives the eigenvalue condition. Sizes ≤ s₀+d+1. D_n bound |
| 23 | **T38FULL Prop. LH-LAT** (validity) | VERIFIED | The case list is complete for states without extras. Brute force over 202 settings: m₀ ≤ the true Φ ≥ 2 margin in every case (`results/margins_grid.txt`) |
| 23′ | LH-LAT "m₀ … is sharp" | **GAP (overstatement)** | Sharp in 108/108 homogeneous settings. In heterogeneous settings it is not sharp in 32/94, with m₀/true down to 0.002. Repair R5 gives the exact formula |
| 23″ | Referee remark: the algebra needs only \|ψ\| < 1 | VERIFIED | The pair unit is positive definite iff ψ² < 1, since Σ_a − ψ²uuᵀ ≻ 0 and uᵀΣ_a⁻¹u = 1. Brute-force margins stay positive for ψ ∈ {ρ+0.05, 0.95} |
| 24 | Task 4: P6 margins vs LH-LAT margins on LH exact Gram | **Consistent** | No discrepancy in validity: c₂ ≤ brute and m₀ ≤ brute in 202/202. They bound different state sets: P6 covers all of Lat(S°) ∖ S₀, LH-LAT only Φ ≥ 2. Tightness inside \|ψ\| < ρ: c₂/brute has median 1.00 and minimum 0.25; m₀/brute has median 1.00 and minimum 0.002 |
| 25 | Method faithfulness: LS0 as modelled | VERIFIED, with two IMPL caveats | (i) `local_search(…, emit_centre = true)` must be used for LS0, because every production call passes `false`. (ii) Cost is 1 + (ℓ+1)·max_k[p + k(p−k)]: the "+1" is the emitted centre (R7) |
| 26 | Start mode by max-plus vs `v3_start.h::start_mode` | VERIFIED | Same DP: per-block per-size maxima; ties keep the smaller size (strict `>`), then the lexicographically smallest set among all DP-optimal choices. On {π₀(S°) > ½} the tie rule is never used |

## 3. Statements (as they should be cited)

**Thm 5(b1-LH-iid).** Assume:
- LH-iid of W3-PXN §0: c ≥ 1 linked pairs with 0 < |ψ_i| < ρ, v ≥ 0 visible groups, fixed nonzero coefficients,
  groups of size g with g ≤ B_n < 2g (so 9 ≤ g ≤ 16 asymptotically), n^a ≤ p ≤ n^A with 1 ≤ a ≤ A;
- EX-A, EX-S, CAL, SR, and GUARD/OP-LS0;
- LS0 with its centre emitted.

Then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup P(U).
**Status: PROVED (candidate). Verified line by line by W5-VMASK (same family). Pending cross-family review.**
Cited inputs, with their status:
- Lemma C1 (Gaussian correlation concentration; literature);
- locked T03, T22(i)(ii);
- W1-EXP Thm 1 (VERIFIED, W3-VEXP);
- W1-T37R Thm A(A3) (VERIFIED, W3-VT37R);
- W1-T38E E3 and T38(b)-R (VERIFIED, W3-VT38E).

**Extension, recorded as VERIFIED numerically, not separately proved.** The proofs nowhere use a common ρ. Groups
may have their own ρ_h ∈ (0,1), provided min_h ρ_h > max_i |ψ_i|; this is P1's margin. The adversarial design with
three null groups at ρ = 0.95 behaved exactly like the base design.

**Thm 5(b1′) on LH-iid, c = 1 (no method change).** Under the same assumptions (no LS0, c = 1), with EX-A, EX-S, SR:
P(S₀ ∉ 𝒮_cal) → 0, and hence the T38 (0) conclusion for the original Ŝ.
**Status: PROVED (candidate).**
- D2-a, D2-b and D2-c are PXN's proofs, VERIFIED here.
- D2-d is R1 of this run, and is **unverified**: a single run.

For c ≥ 2 the no-tweak route stays OPEN.

## 4. Proofs and repairs

The proofs being refereed are in W3-PXN PROOF §§0–12 and W4-T38FULL T38_PROOF §3. `REPAIRS.md` contains:
- **R1**, a full proof of D2-d;
- **R2–R7**, the cosmetic fixes.

The crux of R1 is that the 1/p prior price of touching the masked group C_b exactly pays for H₀ ≍ p draws. The other
bad sets carry exponentially small mass (e_T) or polynomially small mass (q^{k₀+1} with k₀ + 1 > 2A). On the good
set, d moves by O(log n) against a threshold T₀ log r* ≍ log²n.

## 5. Evidence (all reproducible; seeds in each script header)

### 5.1 LH-iid, configs A (c = 1) and B (c = 2)

Source files: `results/table_A.txt`, `table_B.txt`, raw `lh_A.jsonl`, `lh_B.jsonl`. Settings: g = 10, ρ = 0.7, ψ = 0.5,
β = 1 (A) or ±1 (B), one visible hub with β = 1, σ = 1.

| cfg | n | p | reps | partition = groups | med log₁₀π₀(S₀) (PXN) | Mstat med (limit) | med π₀(S°) (PXN) | mode = S° | T22(i) ok | LS0 scored S₀ | LS0 certified at S₀ | (L) holds | D_S > 0 at all lattice states | med Dep (PXN) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 200 | 750 | 20 | 20 | −3.94 (−3.91) | 0.21 (0.63) | 0.66 (0.70) | 20 | 20 | 20 | 19 | 20 | 19 | 0.63 (0.46) |
| A | 400 | 1790 | 20 | 20 | −4.42 (−4.38) | 0.30 | 0.81 (0.75) | 20 | 20 | 20 | 20 | 20 | 20 | 0.31 (0.40) |
| A | 800 | 4260 | 12 | 12 | −4.89 (−4.97) | 0.43 | 0.83 (0.82) | 12 | 12 | 12 | 12 | 12 | 12 | 0.25 (0.31) |
| B | 200 | 750 | 20 | 20 | −7.32 (−7.37) | 1.69 (2.30) | 0.54 (0.65) | 18 | 20 | 19 | 17 | 19 | 17 | – |
| B | 400 | 1790 | 20 | 20 | −8.32 (−8.36) | 1.82 | 0.72 (0.71) | 19 | 20 | 20 | 18 | 19 | 19 | – |
| B | 800 | 4260 | 12 | 12 | −9.23 (−9.27) | 2.15 | 0.78 (0.79) | 12 | 12 | 12 | 12 | 12 | 12 | – |

The single LS0 miss (B, n = 200, rep 8) is a finite-n D_S failure at a Φ = 2 lattice state, even though the mode was
S°. With 20 replicates, every difference from PXN is within the replicate spread.

n = 1600, p = 10,120 confirmation runs (A, B; 3 replicates each, actual partition, not the margin condition): see §5.6.

### 5.2 LH exact Gram, W4-T38FULL §3.5 design

Design: G = 12, g = 9, p = 108, ρ = 0.7, ψ = 0.5, β = (1.4, −1.0, 1.2), visible θ = 1. Source: `results/lh_gram_ls0.txt`.

| c | n | partition = groups | mode = S° | med π₀(S°) (T38FULL) | LS0 scores S₀ | moves | D_S > 0, all lattice states | min lattice margin (T38FULL) | S₀ best among LS0-scored (T38FULL) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 200 | 10/10 | 10/10 | 0.88 (0.88) | 10/10 | 1–2 | 10/10 | 9.3 (11.3) | 9/10 (8/10) |
| 1 | 800 | 10/10 | 10/10 | 0.94 (0.94) | 10/10 | 1 | 10/10 | 50.0 (58.4) | 10/10 (9/10) |
| 1 | 3200 | 10/10 | 10/10 | 0.97 (0.97) | 10/10 | 1 | 10/10 | 260.8 (266.1) | 10/10 |
| 2 | 200 | 10/10 | 10/10 | 0.85 (0.84) | 10/10 | 2 | 10/10 | 2.1 (−1.1) | 10/10 (9/10) |
| 2 | 800 | 10/10 | 10/10 | 0.92 (0.92) | 10/10 | 2 | 10/10 | 21.7 (23.9) | 10/10 |
| 2 | 3200 | 10/10 | 10/10 | 0.96 (0.96) | 10/10 | 2 | 10/10 | 121.9 (133.6) | 10/10 |
| 3 | 200 | 10/10 | 10/10 | 0.78 (0.79) | 10/10 | 3 | 9/10 | −0.9 (−2.9) | 9/10 (9/10) |
| 3 | 800 | 10/10 | 10/10 | 0.91 (0.90) | 10/10 | 3 | 10/10 | 22.1 (29.5) | 10/10 |
| 3 | 3200 | 10/10 | 10/10 | 0.95 (0.95) | 10/10 | 3 | 10/10 | 106.3 (135.4) | 10/10 |

The new information is that the actual v3 partition equals the groups in 90/90 runs, even though exact Gram makes
the within-group correlations equal up to rounding, so the R13 tie rule is exercised.

### 5.3 Lemma B KS tests

Settings: n = 120, 2000 reps per statistic, ψ ∈ {0.5, 0.9}. Source: `results/ks_lemmaB.txt`.
- **Lemma B statistics (B1–B7).** 16 tests in total. All p > 0.05 except one at 0.022 (B7a, ψ = 0.5), which a
  20,000-rep re-test cleared at p = 0.15. The masked-hub independence χ² has p = 0.42 and 0.18.
- **Controls.**
  - N1: an a-group non-hub given ∅, which carries signal.
  - N2: a proxy of the masked hub given S°, a non-neutral addition the lemma excludes.

  Both are rejected at p ≤ 3e-65.

Compared with PXN's check, this one covers more cases: four block statistics with |V| up to 10, two case-β
statistics (one with l in the other pair's a-group), joint independence, power controls, and ψ > ρ.

### 5.4 (L) failure

Source: `results/L_failure_A.txt`, `L_failure_B.txt`. See the R4 table in `REPAIRS.md`. Simulation and first-order
formula agree within Monte Carlo error at every n tested. Certification is slow, as PXN says: 0.7–0.8% still fail at
n = 800–1600.

### 5.5 Adversarial designs

Source: `results/table_<cfg>.txt`. One linked pair, otherwise config A.

| design | n | partition = groups | P1 margin condition holds | med π₀(S°) | mode = S° | LS0 scored S₀ | med log₁₀π₀(S₀) |
|---|---|---|---|---|---|---|---|
| ψ = 0.65 (ρ − ψ = 0.05) | 200 / 400 / 800 | 20/20, 20/20, 10/10 | 0/20, 1/20, 0/10 | 0.32 / 0.80 / 0.84 | 10/20, 20/20, 10/10 | 18/20, 20/20, 10/10 | −4.29 / −4.39 / −4.86 |
| ψ = 0.69 (ρ − ψ = 0.01) | 200 / 400 / 800 | **8/10, 9/10, 6/6** | 0/10, 0/10, 0/6 | 0.36 / 0.72 / 0.85 | 4/10, 8/10, 6/6 | 9/10, 10/10, 6/6 | −4.15 / −4.40 / −4.89 |
| 3 null groups at ρ_null = 0.95 | 200 / 400 / 800 | 10/10, 10/10, 10/10 | 9/10, 10/10, 10/10 | 0.71 / 0.81 / 0.86 | 10/10 each | 10/10 each | −3.85 / −4.35 / −4.92 |
| ψ = 0.8 > ρ (outside LH-iid) | 200 / 400 | **1/10, 0/10** | 0/10, 0/10 | 0.015 / 0.000 | 0/10, 1/10 | 6/10, 10/10 | **−1.30 / −0.19** |

Reading:
1. **P1 binds at finite n near the cliff, as it should.** At ψ = 0.69 the actual partition merges the hub pair in
   2/10 at n = 200. In those runs the masking vanishes (log₁₀π₀(S₀) ≈ −1.6) and LS0 still scores S₀. By n = 800 the
   partition is right in 6/6. The sufficient margin condition fails in every run at ψ ≥ 0.65 while the actual
   partition is right: complete linkage is much more robust than D_in < D_out.
2. **Within the family, LS0 failed in one run.** At ψ = 0.69, n = 200, rep 5, the start mode was {non-hub of C_a,
   visible hub}, a proxy-for-hub substitution, and LS0 from that Φ = 3 centre did not reach S₀. This is the finite-n
   failure of P5 that PXN already reports for B, n = 200. It is not an asymptotic counterexample.
3. **A strongly correlated null group (ρ = 0.95 > ρ) is harmless.** Lemma B makes null statistics exact Beta whatever
   their correlation. SE-blk falls to 0.03–0.04, yet EXP′'s remainder stays bounded and every column matches the base
   design. This probes (M1): its margin is unaffected.
4. **Beyond the cliff (ψ > ρ), the family's masking disappears.** It does not turn into a failure. The hubs are
   co-blocked, so j_b becomes visible in its block and π₀(S₀) is large: about 0.65 at n = 400. (M1) fails, since
   π₀(S°) → 0 (W3-VEXP row 17), but the regime becomes the favourable one.

### 5.6 n = 1600 runs with the actual partition

See the addendum at the end of this report: those runs were still going when this section was written.

## 6. What fails and why (routes tried and abandoned)

- **Breaking Lemma B through dependence between y and the conditioning set.** I tried: case β with l in the *other*
  pair's a-group; ψ > ρ; and conditioning sets containing several components. None breaks it. The only way to break
  it is to add a non-neutral variable (a proxy), and the lemma excludes that explicitly (control N2).
- **Breaking P1 with a null group more correlated than the signal groups.** Higher within-group correlation only
  lowers D_in, so it cannot break P1. The real threat is ψ → ρ; there, P1 holds asymptotically with η = (ρ−ψ)/3, but
  at n = 200 it fails 20% of the time at ρ − ψ = 0.01.
- **Breaking P6/LH-LAT by heterogeneity.** Random heterogeneous pairs (40 settings, ψ up to 0.95, β ∈ [0.3, 2.5])
  never produced a non-positive population margin. The smallest margin inside |ψ| < ρ was 3.1e-4. It is positive
  but tiny, so the n needed for Lemma M's margin m_n ≥ M_n√(log n/n) to bite can be very large for such designs.
  This is a finite-n caveat for the paper, not a gap.
- **Breaking Lemma M through the eigenvalue condition on B.** Lemma M needs λ_min only on A, not on B. I checked that
  RSS_B needs no lower bound: the upper bound on RSS_B and the lower bound on RSS_A suffice. This is correct.

## 7. Needs escalation

1. **Cross-family review of R1** (D2-d). It is the only new proof in this run and has a single author. The step most
   worth an independent look is Step 1's E1 bound across the size cap K (F-a used for sizes K..K+s).
2. **Cross-family review of PXN P3 and Lemma B.** These are now verified by two same-family runs. They remain the
   load-bearing new mathematics of Thm 5(b1-LH-iid).
3. **Lemma C1** is cited from the literature (Bickel–Levina 2008, Lemma A.3, plus the correlation ratio step). A
   reviewer should confirm the constant's dependence: it depends only on A, because Σ_jj = 1.
4. **HQ wording.**
   - Cite Thm 5(b1-LH-iid) as "PROVED (candidate; verified by W5-VMASK)".
   - Cite Thm 5(b1′) on LH-iid, c = 1, as "PROVED (candidate; NB closed by W5-VMASK R1, unverified)".
   - Drop "sharp" from LH-LAT or qualify it (R5).
   - Label PXN's 4%/1.2% as s₀ = 5 (R4).

## 8. Outside scope (recorded, not pursued)

- **Beyond the cliff the method is not hurt.** For ψ > ρ the LH masking is destroyed by the partition itself (as for
  2g ≤ B, PXN Prop. Q). At the numbers here, π₀(S₀) ≈ 0.07–0.7. The statement "(M1) fails at ψ ≥ ρ" (T38FULL §3.4)
  is true but reads as a weakness; in fact it is a transition to the favourable regime. A favourable-regime theorem
  there would need T22(iii) on a two-group block with a hub pair, which has not been checked.
- **Heterogeneous designs have tiny population margins.** Within LH, the population lattice margin can be 3e-4
  (ψ = (0.28, 0.05), β = (2.03, 0.49)). Any finite-n statement derived from Lemma M would be vacuous there at n ≤ 10⁴.
- **P1's sufficient margin condition is far from necessary.** If HQ wants a quantitative finite-n partition claim, the
  right condition is per merge (complete linkage sees max distances), not min-within vs max-cross.

## 9. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Thm 5(b1-LH-iid) | §3 above | 0.95 | done (PROVED, candidate, now verified by 2 same-family runs) | PXN Lemma B + Lemma Tr (P3); P6 margins; P1 | Yes: LS0 with centre emitted |
| Thm 5(b1-LH) (exact Gram, p < n) | T38FULL Cor b1-LH | 0.97 | done (VERIFIED here: LS-score, Lemma M, Thm b1, LH-LAT) | LH-LAT case list | Yes: LS0 |
| Thm 5(b1′), LH-iid, c = 1 | §3 above | 0.9 | done if R1 holds (single run; 0.85) | R1 Step 1 (E1 across the K cap; E2 balancing H₀ ≍ p against 1/p) | No (needs SR) |
| Thm 5(b1′), c ≥ 2 | original Ŝ = S₀ w.p. → 1 − P(U) on LH-iid | 0.6 | 0.15 | delivery at Gibbs distance ≥ 2 (SHARE) | No, but OPEN |
| PXN P3 rate | 1 − π₀(S°) = O_P(√(log n/n)) | 0.97 | done | exact Beta + truncation | No |
| LH-LAT sharp margin | m₀^♯ of R5 | 0.95 | 0.9 (formula given; brute force agrees by construction) | case bookkeeping | No |
| Heterogeneous ρ_h extension of LH-iid | min_h ρ_h > max\|ψ\| | 0.9 | 0.85 (proofs never use a common ρ) | P1 margin; F4 with ρ₊ | No |
