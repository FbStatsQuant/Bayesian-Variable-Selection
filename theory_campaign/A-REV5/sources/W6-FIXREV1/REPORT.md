# W6-FIXREV1 — REPORT: applying the cross-family review A-REV1 to the Theorem B and T38 package

Run of 2026-11-02, branch `theory/W6-FIXREV1`, from `theory/campaign` at 06408a0. Sources read (branch heads used): A-REV1
`REVIEW.md` @ 26815e8; W1-T24G @ 9e210a3; W2-VT24G @ dba6ff4; W2-PREM @ 988c5f5; W1-T38E @ 436a712; W3-VT38E @ 3e4b732;
W4-T38FULL @ a0f9cb5; W2-BOOK @ 57eb3d0; and the parts of W3-PXN (@ 4aebea3) and W1-EXP (A-REV1's pinned copy) that use
E3/T22(i) or Lemma U. The first five match A-REV1's pinned commits. Everything here is a **candidate**: nothing is reviewed after these
edits, and nothing is adopted.

**Deliverables.**
- `T38_STATEMENT.md`: the corrected statement. It **supersedes** W4-T38FULL's, and its Part 0 is the T38 change log.
- `T38_PROOF.md`: the corrected proof (supersedes W4-T38FULL's).
- `CONSOLIDATED.md`: every other corrected item. These are Prop. U′, the Theorem B conventions, Lemma P (multi-target),
  Lemma S′, D2-∞ with rates, E3′ with its downstream check, Lemma U's constant, NL0's quantifier form, and CE1-narrow.
- `scripts/` (fixed seeds; independent code that imports nothing from other runs) and `results/`.

## 1. Headline

1. **Every A-REV1 finding is incorporated, and I agree with all of them.** I have no substantive disagreement. I add
   two precision notes (§3): part of A-REV1 §7 was already repaired in W4-T38FULL, which A-REV1 did not review; and the
   single-particle (b2) form still needs the Markov half of IND-T.
2. **Proposition U: ERROR confirmed, repaired (Prop. U′, PROVED).** Both A-REV1 counterexamples are reproduced with the
   actual kernels. In one instance the shortcut misses a single bad independence transition of probability 0.83. **Theorem
   B is unaffected (PROVED)**: its proof and W1's constant code use the full three-test definition, never the shortcut.
3. **Lemma S′ (PROVED):** the inequality holds everywhere, and equality with positive weights holds iff f > 1 − e. **E3′
   (PROVED):** (ii) carries q < 1. The p = 2 counterexample is reproduced to every digit, and E3(ii) is used nowhere
   downstream. **Lemma U:** κ_n ↓ 0.51/c_E (PROVED), with no downstream effect. **NL0:** the correct form is the
   sum-over-labels-of-sups Λ₂(a). Its cost is the PG(a) design condition of W2-PREM, which is a genuine extra
   assumption. **CE1:** narrowed to an explicit sequence (COUNTEREXAMPLE, PROVED from Lemma E and Lemma U(C5)).
4. **T38 rewritten.** The changes are: the D2-∞ rate margins for (b1′); the eligible-set and repair-certificate interface
   with the capped β_H for (b2); the strict versus HPM output conventions, with the explicit usable-but-unexecuted term
   D_n^{sl}; the potential-uninterrupted-run execution model (GUARD as (G1)–(G2)); K = min(p, ⌊n/2⌋); the T11(vii)
   citation replaced; and the LS0 cost including the centre call. T38 is **PROVED as a conditional theorem**. Its
   masked-regime instance without a method change is still OPEN (DELIV), and with LS0 on LH exact Gram all premises are
   proved (not cross-family reviewed).

## 2. Change-log table (item | A-REV1 verdict | fix | downstream effects)

| # | Item | A-REV1 verdict | Fix (where) | Downstream effects | Agree? |
|---|---|---|---|---|---|
| 1 | Prop. U (W1-T24G §3) | ERROR: independence "iff" drops truth removal; extra-for-extra swap need not stay in the phase-1 family | **Prop. U′** ([CON] §1.2): Bad(W) by all three tests for every label; extra-for-extra swap neutral iff it stays in the family, with the exact phase-1 condition (k ∈ A, l ∈ J, junk budget full; 𝒵♯ analogue); β_I(W) bound on the corrected set. Status PROVED | **Theorem B unaffected** ([CON] §1.3): its proof uses only the §0 definition; W1's `progress_bounds.py` implements the full definition (checked); W2-PREM IND-M and its §5.2 neutral list use the full definition. W2-VT24G's "Prop. U VERIFIED as bookkeeping" must be downgraded | Yes (both counterexamples reproduced, `results/propU_check.json`) |
| 2 | Theorem B (finite) | VERIFIED after F′ | Boundary conventions (C-0)–(C-5) and capped β_H written into the statement ([CON] §2) | β_H is the quantity T38 (b2) carries | Yes |
| 3 | Lemma P, multi-target sentence | GAP, fixable | Explicit bound s_min(\|C\|/k)[1 − Q/(k+1)] with proof ([CON] §3). PROVED | none (P1 and c_poly are special cases) | Yes (re-derived) |
| 4 | Cor. B-M wording | VERIFIED; "no η → 0" only for fixed H | Corrected wording; past-measurable selection; IND-T boundary H′ = L+5 vs H = L+4 ([CON] §2) | T38 (b2) boundary fixed at 𝔉_T | Yes |
| 5 | Lemma S (W1-T38E §3) | Inequality VERIFIED; "attained by two-level weights" ERROR on the full domain | **Lemma S′** ([CON] §4): ω ≥ max(0, f − √(f(1−f)c)); attained iff 1 − e < f < 1; for 0 < f ≤ 1 − e the infimum is 0 and not attained. PROVED | D2 uses only the inequality, at f > 0.1 = 1 − e: no change | Yes |
| 6 | E3(ii) (W1-T38E §6.3) | ERROR: omits q < 1 of locked T22(i-a); p = 2 counterexample | **E3′** ([CON] §6): (ii) requires 0 ≤ q < 1 (or u < 1 via (i-b)); centre emission written into LS0; score count 1 + (ℓ+1)max_k[p + k(p−k)]. PROVED | Downstream check ([CON] §6 table): W1-T38E §7 (b1) sufficient condition needs q < 1 (superseded); W4 uses only E3(i); W3-PXN P3 states q < 1 explicitly; W1-EXP Thm 5/6 use u < 1; W2-BOOK §4.3 wording | Yes (reproduced to all printed digits; 726/2,095 random q ≥ 1 cases break the conclusion) |
| 7 | Lemma U limit (W2-PREM §2, from W1-EXP) | ERROR: 0.51/c_E, not 0.52/c_E | κ_n strictly decreasing, ↓ 0.51/c_E = 4.08(M+2σ²)/σ², ≤ 0.52/c_E for n ≥ n₁ (explicit) ([CON] §7). PROVED. Family-count convention added | None: every use needs only a finite κ. Also correct W1-EXP Thm 1 and Remark (b), and W2-PREM REPORT's "4.16" | Yes |
| 8 | NL0 quantifier (W1-T24G §6) | GAP: sup of sum ≠ sum of sups | Correct form Λ₂(a) = Σ_l sup_W o_l(W), plus the general rule (labels outside, states inside, destinations of one label inside) ([CON] §8) | Costs PG(a) and a factor (eD_n+1)^a in the rate (W2-PREM Prop. NL0); EQ COUNTEREXAMPLE shows it is a genuine assumption; W2-PREM's results are unchanged (already in this form); wording fixes in W1 §6 and W2-VT24G §6 | Yes |
| 9 | CE1 broad wording | GAP as a blanket claim | **CE1-narrow** ([CON] §9): explicit sequence p = ⌈n^{1/3}⌉, one truth, one proxy at correlation r, exact Gram, any fixed d ≥ 1: (L+4)η_n → ∞. COUNTEREXAMPLE, PROVED from Lemma E and Lemma U(C5). The broad sketch stays PROOF SKETCH | T38 Remark 4 and dependency row g6 reworded; "H24 is false" must not be cited | Yes (numerics: floor ≈ 0.09–0.14, `results/ce1_sequence.json`) |
| 10 | D2 (finite) | VERIFIED (potential first pilot stage) | Unchanged; execution qualification written out (T38_PROOF §4.1) | — | Yes |
| 11 | T38(b)-R route (b1′) | GAP: rate margins missing | D2-∞ with fixed b₀ > 0.1, bounded k_D, Dep ≤ 1 − c₀, P(NB′ᶜ) → 0, or a general-rate version ([CON] §5; T38_PROOF §4.3). PROVED (implication) | T38 statement (b1′) replaced | Yes |
| 12 | T38(b)-R route (b2) | GAP: eligible-set interface, binomial bound | Repair certificate; data-measurable 𝔛_n; capped β; boundary 𝔉_T with H′ = L+5; DELIV to 𝔛_n with aggregate D3(𝔛) rates; single (IND-T(b)) and product (IND-T(a)) forms (T38_PROOF §5). PROVED (implication) | T38 (b2) replaced; DELIV still OPEN | Yes (precision note §3.2) |
| 13 | T38 execution / output | GAP: U vs usable-but-unexecuted; T21-style execution | Strict convention 𝒪 = {exact, completed} plus HPM convention with D_n^{sl}; GUARD as (G1)–(G2) on R̄; relation to A-REV1's actual-run form with the E term (T38_PROOF §§0, 1.2, 1.3) | Under the HPM convention routes (a), (b2) carry P(SMC ∩ 𝒜ᶜ); (b1), (b1′) do not | Yes |
| 14 | T38: "T11(vii)" citation; K | Replace by T21(C1); K = min(p, ⌊n/2⌋) | Done (T38_PROOF §1.1; Objects) | — | Yes |
| 15 | IND-T | VERIFIED for the uninterrupted process | Boundary convention stated; first-fresh sets excluded; no completion conditioning ([CON] §2) | — | Yes |
| 16 | Lemma F, F′, O, C, B1, B2, c₂ floor, B1′/B2′, P1, Lemma E | VERIFIED | none | — | Yes |

## 2b. Statements and proofs (full text in the deliverable files)

Every refined statement is written in full, with its hypotheses named, in these places:
- **Prop. U′, and Theorem B's unaffected status:** [CON] §1. **Theorem B with conventions and β_H, Cor. B-M, IND-T
  boundary:** [CON] §2. **Lemma P (multi-target):** [CON] §3.
- **Lemma S′:** [CON] §4. **D2-∞ with rates:** [CON] §5. **E3′:** [CON] §6. **Lemma U (corrected constant and
  family-count convention):** [CON] §7. **NL0 (Λ₂ form):** [CON] §8. **CE1-narrow:** [CON] §9.
- **Theorem 5 (T38), parts (0), (0_H), (a), (b1), (b1′), (b2), (b1-LH), (c):** `T38_STATEMENT.md` Part I.
  Proofs: `T38_PROOF.md` §§1–7.

Every new proof is given in full in those sections (U′ (iii-2)/(iii-3), Lemma P, Lemma S′ attainment, D2-∞, the κ_n
monotonicity and n₁, CE1-narrow, T38 §§1.1–1.3, 4.3, 5.1, 5.2). No proof in this run is a sketch except the two that
are marked PROOF SKETCH and inherited: the D2 instance on LH, and W2-PREM's Theorem L.

## 3. Where I add to or qualify A-REV1 (no disagreement)

1. **A-REV1 §7 reviewed W1-T38E's T38(b)-R, not W4-T38FULL.** Several §7 repairs were already in W4:
   - the R̄/GUARD execution model and the "never condition on completion" rule;
   - the eligible set 𝔛_n with a sup-β REP condition;
   - the boundary 𝔉_T with H′ = L + 5;
   - a D2-∞ corollary with "b fixed".

   A-REV1's GAP verdict therefore applies in full to W1-T38E's statement. For W4 it applies only to the residual items,
   which this run fixed: the statement-level (b1′) rates; the β conventions, capping and certificate; the usable output
   convention; T11(vii); K; the LS0 count; and DELIV's aggregate.
2. **The single-particle (b2) form is not IND-T-free.** A-REV1 §2 says route (b2) needs "select the smallest eligible
   index using only the past, then integrate its conditional failure bound". The particles of an island read one shared
   stream, so even one particle's trajectory being a K̄₁-chain given 𝔉_T needs the stopping-time argument. That is
   IND-T(b). Only the product form needs IND-T(a). This is a statement of what is used, not an objection.
3. **CE1-narrow at accessible n.** On A-REV1's sequence the Lemma E floor is ≈ 0.09–0.14, and (L+4)·floor ≈ 1.7–1.9 at
   n ≤ 10⁵. It diverges only like (L+4)/21, because B reaches 16 only at n ≈ 1.7·10⁷. So the asymptotic failure shows up
   at practical n as "(L+4)η is not small", not as visible divergence. This is consistent with A-REV1.
4. **An inconsistency between campaign documents.** W2-BOOK defines 𝒪_H := (no usable HPM)ᶜ and leaves the
   schedule_limit convention open. W4 uses 𝒪 = {exact, completed}. A-REV1 §7.3 reads U as "no usable HPM". T38 now
   states both conventions with their exact discovery terms. **HQ must pick one for the paper.**

## 4. Evidence (all scripts in `scripts/`, outputs in `results/`)

| Script | What it shows |
|---|---|
| `bvs_core.py` | Independent implementation of the v3 target (00_COMMON §1): score, size prior, cap K = min(p, ⌊n/2⌋), block start law, d, Gibbs o_j, exact-Gram designs |
| `e3_check.py` (seed 20261103/4) | Part A reproduces A-REV1 §3.3: r₁ = 0.2236068, r₂ = 1.9355178·10¹², e = 17.888544, formula 1.983334·10²³ vs π₀({1}) = 9.441608·10⁻¹⁴, mode {2}. Part B: 300 random instances, 4,146 references. T22(i-a) held in all 2,051 q < 1 cases (worst ratio 1.0001). With q ≥ 1, the formula exceeded the mass in 864/2,095 cases and gave a false "> ½" in 726 |
| `propU_check.py` (seed 20261106–8) | Config 1 (S₀ = {1,2}, A = ∅): the missed transition {1} → {2} by I stays in the family with V = 1 → 1. Config 1b (weak truth 1): that transition has probability 0.826; η₁'s I term is 0.945 (full) vs 0.119 (shortcut). Config 2 (A = {2}, junk 3): the swap 2 → 3 leaves 𝓕 with probability 0.091; η₁'s U term is 0.112 (full) vs 0 (shortcut) |
| `lemmaS_lemmaU_check.py` (seed 20261105) | Lemma S′: positivity ⟺ f > 1 − e in all cells; e = 0.9, f = 0.05 gives low weight −0.453; range-(b) witnesses; worst slack −1.2·10⁻¹⁴ in 20,000 cases; r* exact. Lemma U: κ_n decreasing; κ_{10⁹} − 0.51/c_E < 1.2·10⁻⁷; κ_n ≤ 0.52/c_E from n = 71–289 |
| `ce1_sequence.py` (seed 20261109) | A-REV1 §5 sequence, d = 1, r ∈ {0.3, 0.6}, n = 200 … 10⁵: o₂(Y) = 1.000 for n ≥ 1000 (r = 0.3) and for all n (r = 0.6); Lemma E floor 0.09–0.14 |

All computations are floating point (mpmath at 60 digits for the E3 start law). They are checks, not proofs.

## 5. Line-by-line rechecks done in this run (not done by A-REV1)

- **Lemma M (W4-T38FULL §3.2).** I re-derived the RSS decomposition, using ⟨(I−P_S)μ, Cε⟩ = ⟨(I−P_S)μ, ε⟩ because
  (I−P_S)μ ⊥ 1. I also re-derived the Q-vs-RSS sandwich, which uses λ_min(G_A) ≥ φ₀²(n−1) and gives
  ‖β̂‖² ≤ 1/φ₀²; the determinant ratio in [1/n, n+1]; the prior ratio; the union-bound exponent (L/4 = A(k+s₀) + 1);
  and log x ≥ 1 − 1/x. No error found.
- **Lemma LS-score (W4-T38FULL §3.1).** I checked lattice closure of progress moves, that the move limit never binds at
  Φ ≥ 2, and the Φ = 1 scan, including feasibility s₀ − 1 < K. No error found.
- **Theorem B's dependence on Prop. U.** I read [B] §4 and W1's `progress_bounds.py` (the phase-1 and phase-2
  classification). Result: [CON] §1.3.
- **T38 (5.1).** Islands are joined through ∨_r 𝔉_T^{(r)}. The four streams are independent given (data, 𝓒). A particle
  at S₀ at the boundary is already scored. The argmin-β selection is 𝔉-measurable.

## 6. What fails, and why

- **Re-reading Prop. U as "commentary only".** That would leave the false sentences in place. They have to be corrected,
  even though no inequality used them.
- **Keeping E3(ii) with the remark "s+1 even makes (1−q)^{s+1} ≥ 0 anyway".** This fails: the bound becomes huge when
  q ≫ 1 (the counterexample).
- **Making the actual-run form GUARD-free.** A-REV1's E-term form still needs the coupling "actual = potential until
  interruption". That coupling is (G1)–(G2). No version without some stop-only coupling is possible, because a guard that
  consumed randomness would change the law.
- **Deriving DELIV(𝔛_n).** Not attempted beyond D3(𝔛). C1 blocks the bridge-mass route, and SHARE is near-circular. It is
  OPEN.

## 7. Needs escalation

1. **HQ decision: the output convention** (strict 𝒪 vs HPM 𝒪_H). This changes which routes carry P(SMC ∩ 𝒜ᶜ).
2. **Cross-family review of items A-REV1 did not see:**
   - Lemma M, Lemma LS-score, Theorem b1 and Prop. LH-LAT (W4-T38FULL §3, the only fully proved masked route);
   - W2-BOOK Lemma RO and the GUARD code reading;
   - W2-PREM's Theorem B♯, Prop. B1′ (argmin independence) and Lemma CMP.
3. **Independent code check of GUARD (G1)–(G2)** in `v3_runtime.h`, `v3_engine.h` and `v3_core.cpp`. The whole
   execution side of T38 rests on it.
4. **Edits to source branches** (this run writes only under W6-FIXREV1):
   - W2-VT24G's Prop. U verdict;
   - W1-EXP's and W2-PREM's "0.52/c_E" and "4.16";
   - W1-T24G §6's NL0 row;
   - W2-BOOK §4.3's T22(i) wording.
5. **NB′ on LH (c = 1):** the only unfinished step of the no-method-change masked route (b1′).

## 8. Outside scope (found, not pursued)

- **Name collision.** W3-PXN has its own "Lemma U" (§9.1, uniform score approximation on small sets). It is not
  W2-PREM's Lemma U. Their constants differ, and they should be renamed before the paper.
- **Label clash.** "(e′)" means Theorem B in W1-T24G/W2-BOOK and T37 in FABLE_REVIEW (already flagged by W2-BOOK).
- In the HPM convention, routes (a) and (b2) need P(SMC ∩ 𝒜ᶜ) → 0, that is, the calibration succeeds w.p. → 1. No
  campaign result addresses the probability of `schedule_limit`.

## 9. Confidence card

| Target | Refined statement | P(true) | P(provable at reasonable cost) | Crux | Method change? |
|---|---|---|---|---|---|
| Prop. U′ | [CON] §1.2 | 0.98 | done | full Bad set; phase-1 swap condition | no |
| Theorem B (finite, with conventions) | [CON] §2 | 0.95 | done (A-REV1 VERIFIED) | — | no |
| Lemma P multi-target | [CON] §3 | 0.98 | done | — | no |
| Lemma S′ | [CON] §4 | 0.99 | done | positivity ⟺ f > 1 − e | no |
| D2 finite / D2-∞ with rates | [CON] §5; T38_PROOF §4 | 0.96 | done (implication) | — | no |
| D2 masked instance (LH, c = 1) | Dep, NB′, b₀ w.p. → 1 | 0.6 | 0.4 | uniform two-sided d bound for NB′ | no |
| E3′ | [CON] §6 | 0.99 | done | q < 1 | LS0 (for its use) |
| Lemma U constant | κ_n ↓ 0.51/c_E | 0.99 | done | arithmetic | no |
| NL0 (Λ₂ form) under PG | W2-PREM Prop. NL0 | 0.9 | done (needs cross-family review of CMP) | partner-graph comparison | no |
| CE1-narrow | [CON] §9 | 0.92 | done | Lemma U(C5) on a fixed family; Lemma E | no |
| T38 (0)/(0_H) | T38_STATEMENT | 0.95 | done | GUARD (IMPL) | no |
| T38 (b1) incl. LH exact Gram | T38_STATEMENT (b1), (b1-LH) | 0.88 | done (not cross-family reviewed) | Lemma M, LH-LAT | **yes (LS0)** |
| T38 (b1′) | rate form | 0.95 (implication) | done; instance 0.4 | NB′ | no |
| T38 (b2) | eligible-set form | 0.93 (implication) | done; **DELIV OPEN** (true 0.5, provable 0.15) | particle-level delivery to 𝔛_n | no |
