# Item 2 (LH-iid unconditional) — discharging GEN (C5)(b)'s conditions "W7-PART Theorem B (candidate)" and "[CONC]"

Author: C-PACK lead (Claude Opus 5.5). Status: PROVED (by this seat); cross-family check R35 (`reviews/R35_item2_check_sol.md`) VERIFIED-WITH-AMENDMENTS, all 3 amendments applied (v2).
Aliases: `W1/` = `Theory_work/Wave1/`; `PX` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`.

## 1. What GEN uses (verbatim)
GEN (C5)(b), `W1/W1-GEN/lemmas/L6_instances.md`:
- U1 (`:68-69`): "ℛ_n := {blocks = groups}; P(ℛ_nᶜ) → 0 by Theorem R = W7-PART Theorem B (**candidate**; A-REV6 "VERIFIED
  on SIZE"; PROOF.md:77-100)."
- U2 (`:70-74`): "𝒞_n := {λ_min(R̂_T) ≥ λ₀/2 ∀|T| ≤ min(p, m♯_n + s₀ + j₀ + |𝒱| + 1); ‖μ‖²/n ≤ M; θ\*²_min ≥ b₀} with
  λ₀ := (1 − max|ψ|)(1 − ρ₊), … P → 1 by [CONC] (max|r̂_jk − Σ_jk| ≤ C√(log p/n), operator error O(log n)·C√(log p/n)
  = o(1) at these orders) and the SLLN for the fixed signal columns"; "m♯_n = O(log n)".
- Conclusion (`:83`): "(C4) gives (C3) under the joint law, **conditional on W7-PART Theorem B (candidate)** and [CONC]."
- Setting (`:44`, `W1/W1-GEN/STATEMENT.md:128-131`): LH-iid as in PX:36-60, SIZE, 18 ≤ p ≤ n^A; blocks = the method's
  partition "complete linkage on 1 − |r̂|, top-down cut at B, next-fit packing; B = min(⌊√n⌋, ⌊√p⌋, 16)"
  (`W1/W1-GEN/STATEMENT.md:37-38`); A ≥ 1 fixed (`W1/W1-GEN/STATEMENT.md:30-31`).

So GEN needs exactly two probability facts: (U1) P(blocks ≠ groups) → 0; (U2) P(𝒞_n) → 1, of which only the
eigenvalue part uses [CONC] (the other two parts are SLLN on finitely many fixed columns).

## 2. What W1-PXN verified (verbatim)
- Theorem R, repaired (`W1/W1-PXN/lemmas/R_branch_repair.md:7-16`): "Under (SIZE) at n and n ≥ 5: (R-a) for every
  t ∈ (ψ̄, ρ): P(𝒜_nᶜ) ≤ S(t) …; (R-b) with t = t\*: P(𝒜_nᶜ) ≤ S(t\*) ≤ K_n := (2/(√π(1−ρ))) p²√n e^{−(n−4)I\*}. (R-c) For
  every fixed A ≥ 1, C > 0: P(𝒜_nᶜ) ≤ p^{−C} once n ≥ max(5, n₁) and (n−4)I\* ≥ log(2/(√π(1−ρ))) + ((2+C)A + ½) log n;
  and P(𝒜_nᶜ) ≤ (2/(√π(1−ρ))) e^{4I\*} n^{2A+½} e^{−nI\*}, which is summable in n with no lower growth bound on p."
  Here 𝒜_n := {blocks = groups} (`W1/W1-PXN/FINAL_PROOF.md:14-15`). Status in the W1-PXN report
  (`W1/W1-PXN/REPORT.md`, §3 row "Report item 4"): "XF VERIFIED incl. Hotelling density, W7 Lemma 2 and the Corollary B
  constant, after splitting the false "every t" display (E-15); W7 A0(c) bypassed by a direct margin argument (E-17);
  independent cruder route (R′) XF VERIFIED" — evidence R14, R19, R21; W1-PXN council C1 passed (8.6/8.3).
- Independent route (R′) (`W1/W1-PXN/lemmas/CR_corr_tails.md`, "Corollary (R′)"): for every n ≥ 3 at which SIZE holds,
  P(𝒜_nᶜ) ≤ 3p² exp(−(n−1)(ρ−ψ̄)²/4096) (XF VERIFIED R19).
- [CONC′] (`W1/W1-PXN/lemmas/CR_corr_tails.md`, "Corollary [CONC′]"): for rows iid N(0, Σ), Σ a correlation matrix, any p,
  δ ∈ (0, 2]: P(max_{j<k}|r̂_jk − Σ_jk| > δ) ≤ 3p² e^{−(n−1)δ²/1024}; with p ≤ n^A and δ_n := 32√(2(A+1) log n/(n−1)):
  ≤ 3n^{−2}. "‖R̂_T − Σ_T‖_op ≤ |T|·δ_n". Status: "PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)".
- Family, partition and SIZE in PXN: LH-iid = PX:36-60 (same source lines as GEN); SIZE "g ≤ B_n < 2g for all n ≥ n₁,
  with B_n = min(⌊√n⌋, ⌊√p⌋, 16)" (PX:52-53); partition = complete linkage + top-down cut + next-fit (PX:87-91); A ≥ 1 fixed.

## 3. Comparison (hypotheses and constants)
| item | GEN (C5)(b) | W1-PXN verified | match |
|---|---|---|---|
| design | LH-iid, PX:36-60 | LH-iid, PX:36-60 | identical source |
| p | 18 ≤ p ≤ n^A, p → ∞, A ≥ 1 | same (PX:41; STATEMENT) | identical |
| partition | complete linkage on 1−\|r̂\|, top-down cut at B, next-fit, B = min(⌊√n⌋,⌊√p⌋,16) | same algorithm and B_n | identical |
| SIZE | g ≤ B_n < 2g | g ≤ B_n < 2g for n ≥ n₁ | identical |
| conclusion needed | P(blocks ≠ groups) → 0 | (R-c): ≤ n^{2A+½}·const·e^{−nI\*} → 0 (I\* > 0 fixed); also (R′) | stronger than needed |
| cited display | PX:77-100 (original, "every t" chain) | split display (R-a)/(R-b)/(R-c) | GEN uses only the limit, which the repaired (R-b)/(R-c) give; the false part of the original display is not used |
| A0(c) of W7 Thm A | not used | bypassed (direct strict-margin argument, R_branch_repair §2) | n/a |
| [CONC] rate | C√(log p/n) (classical, cited) | [CONC′]: δ_n = 32√(2(A+1) log n/(n−1)), prob ≥ 1 − 3n^{−2} | different rate (log n vs log p); see §4 |

## 4. Lemma (GEN (C5)(b) without the candidate inputs)
**Convention (exact branch; R35 #1).** Throughout this lemma, blocks mean the deterministic `make_blocks(X,B_n)` partition,
defined for every design, hypothetically when the production run dispatches to exact enumeration, as in W1-PXN
`lemmas/R_branch_repair.md` §3 and `FINAL_PROOF.md` §0. The events ℛ_n and PXN's 𝒜_n concern this same data function;
equality of partitions ignores their enumeration labels. Block tables and start objects used for the theoretical argument
have the same hypothetical interpretation. On the exact branch, once s₀ ≤ K, enumeration already scores S₀, so that branch
contributes zero to D_n; no actual block construction or LS0 execution is needed for that conclusion. (GEN's own good-design
event, also written 𝒜_n at `L6_instances.md:67`, is a different event — an intersection of five events — and is not
PXN's 𝒜_n.) Without this convention the literal identity "ℛ_n = PXN's 𝒜_n" fails for very slowly growing p (e.g.
p_n = 9 max{9, ⌈log₂log₂ n⌉}), where the production run takes the exact branch and builds no partition (R35 #1).

**Lemma I2.** Under GEN's (C5)(b) setting (LH-iid, SIZE, 18 ≤ p_n ≤ n^A, p_n → ∞, A ≥ 1 fixed):
(i) P(ℛ_nᶜ) → 0; indeed P(ℛ_nᶜ) ≤ (2/(√π(1−ρ))) e^{4I\*} n^{2A+½} e^{−nI\*} for n ≥ max(5, n₁).
(ii) For every sequence L′_n = O(log n), P(λ_min(R̂_T) ≥ λ₀/2 for all T with 1 ≤ |T| ≤ L′_n) ≥ 1 − 3n^{−2} once
L′_n δ_n ≤ λ₀/2 and δ_n ≤ 2, with λ₀ := (1 − ψ̄)(1 − ρ) ≤ λ_min(Σ).
Hence P(𝒞_n) → 1 with [CONC′] in place of [CONC], and GEN's conclusion (C5)(b) holds **without** the conditions "W7-PART
Theorem B (candidate)" and "[CONC]".

*Proof.* (i) ℛ_n is PXN's 𝒜_n (same family, same partition algorithm, same B_n, same SIZE; §3). Apply (R-c), second
display, verified as cited in §2; I\* = I(t\*; ψ̄) > 0 is a fixed constant (PX:79-82), so n^{2A+½}e^{−nI\*} → 0.
(Alternatively (R′): 3p²e^{−(n−1)(ρ−ψ̄)²/4096} ≤ 3n^{2A}e^{−(n−1)(ρ−ψ̄)²/4096} → 0.)
(ii) λ₀ ≤ λ_min(Σ) is (F4) (PX:56, "λ₀ := λ_min(Σ) ≥ (1 − ψ̄)(1 − ρ) > 0"; GEN writes the same constant
(1 − max|ψ|)(1 − ρ₊) with ρ ∈ (0, 1), so ρ₊ = ρ). For T with |T| ≤ L′_n, Σ_T is a principal submatrix, so
λ_min(Σ_T) ≥ λ₀ (Cauchy interlacing). On {max_{j<k}|r̂_jk − Σ_jk| ≤ δ_n} (diagonals are exactly 1 for R̂ and Σ):
‖R̂_T − Σ_T‖_op ≤ ‖R̂_T − Σ_T‖_{∞→∞} ≤ |T|δ_n ≤ L′_nδ_n (row-sum bound; symmetric matrix), so by Weyl
λ_min(R̂_T) ≥ λ₀ − L′_nδ_n ≥ λ₀/2. [CONC′] bounds the complement by 3n^{−2}. For GEN's 𝒞_n take
L′_n := m♯_n + s₀ + j₀ + |𝒱| + 1 = O(log n) (GEN's own statement m♯_n = O(log n); s₀, j₀, |𝒱| = g(2c+v) fixed); the
minimum with p only shrinks the family. L′_nδ_n = O((log n)^{3/2} n^{−1/2}) → 0, so the onset is eventually met. The two
remaining parts of 𝒞_n (‖μ‖²/n ≤ M, θ\*²_min ≥ b₀) are SLLN statements on the finitely many fixed signal columns, as
in GEN, unaffected. ∎
*Finite-n remark (council C1-opus #3).* The onset L′_nδ_n ≤ λ₀/2 is far beyond practical n (≈ 10¹⁰ for g = 10, c = 1,
ρ = .7, ψ̄ = .5, A = 1, council estimate); (ii) is an asymptotic statement only.

**Rate difference, (C5)(b).** GEN's parenthesis "max|r̂ − Σ| ≤ C√(log p/n)" is replaced by "≤ δ_n = O(√(log n/n))"; for
slowly growing p this is a weaker rate than written, but (C5)(b) uses it only through "operator error … = o(1)", which
(ii) gives. No other step of L6(b) uses the rate (the Beta-law, tail and moment steps use exact distributions).

**Same replacement for (C5)(d)** (R37 #2 text). Rows are iid N(0, Σ_s), so put 𝒢_n := {max|r̂ − Σ_s| ≤ δ_n} with δ_n = 32√(2(A+1)log n/(n−1)); P(𝒢_nᶜ) ≤ 3n⁻² eventually. Throughout L6(d), replace the concentration-derived √(log p/n) error bounds by O(√(log n/n)), and the concentration-derived log p/n bounds in :159, :163 and :165 by O(log n/n). This also replaces the sample-error term at :189. The new rates may be weaker when p grows slowly, but every required error still vanishes or has the required domination; in particular ω_n = O((log n)^{3/2}/√n) → 0. No equivalence between log p and log n is needed. (R35's line table covers L6:123-191; alternatively Lemma CR at δ = 32√(3 log p/(n−1)) gives failure ≤ 3/p → 0 and recovers the original rate O(√(log p/n)).) Whether L6(d) is otherwise correct is item 3's check (R31).

## 5. Status change proposed (HQ's call; nothing upgraded here)
GEN (C5)(b): "conditional on W7-PART Theorem B (candidate) and [CONC]" → "uses Theorem R as repaired and XF-verified in
W1-PXN (R14, R19, R21; route (R′) R19) and [CONC′] (W1-PXN Lemma CR, XF VERIFIED R19); no candidate input". The
remaining dependencies of (C5)(b) are GEN's own L6(b) argument (status 'PROVED (by this seat, unchecked)'; R07 recorded (a)–(c) VERIFIED-WITH-AMENDMENTS) and the W1-PXN items, whose ticket-level
status is "PROVED-CHECKED" (W1-PXN REPORT §1; Wave-1 result, not adopted by HQ).
