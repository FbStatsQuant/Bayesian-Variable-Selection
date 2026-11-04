# G3 digest: W6 repairs, W7 credits, and O-/F- theory branches

Scope: W6-FIXREV1, W6-FIXREV2, W7-PART, W7-SEC, W7-SEP, F-SHARE, O-BGIBBS, O-STAGES, O-PW2, O-WSTAB (with
review_CHECK_SEP_W.md). Source: scratchpad `src/<ID>/` = `theory_campaign/<ID>/` on `origin/theory/<ID>`.
I read every REPORT, NOTES, CONSOLIDATED, STATEMENTS and BRIEF file in full, and grepped the PROOF files for labels and statuses.
The status words below are copied exactly from the files and are never upgraded. All results are "candidate", meaning not reviewed after the run and not adopted,
unless the entry says otherwise. "[CON]" = W6-FIXREV1/CONSOLIDATED.md.

---------------------------------------------------------------------------------------------------------------------

## W6-FIXREV1 — head a7833f3 (2026-11-02T19:06Z)

**Task.** Apply the cross-family review A-REV1 (GPT-6 Astra) to Theorem B, Prop U, Lemma S, D2, E3, Lemma U, NL0, CE1
and T38(b)-R. Produce one consolidated package, plus a new `T38_STATEMENT.md` and `T38_PROOF.md` that supersede W4-T38FULL.
Files: REPORT.md, CONSOLIDATED.md, T38_STATEMENT.md, T38_PROOF.md.

**Agreement with A-REV1.** The report says: "Every A-REV1 finding is incorporated, and I agree with all of them. I have no
substantive disagreement." Two precision notes, not objections, are in §3:
(i) "A-REV1 §7 reviewed W1-T38E's T38(b)-R, not W4-T38FULL". Several §7 repairs (R̄/GUARD, 𝔛_n with sup-β REP, 𝔉_T with
H′ = L+5, D2-∞ "b fixed") were already in W4. So the GAP verdict applies in full only to W1-T38E's statement.
(ii) "The single-particle (b2) form is not IND-T-free". It needs IND-T(b) (the Markov half). Only the product form needs IND-T(a).

### A-REV1 objections: repair, how it was done, and what remains

| # | Item | A-REV1 verdict | Repair (location) / new status | What remains |
|---|---|---|---|---|
| 1 | Prop U (W1-T24G §3) | ERROR. Shortcut (U-a): the independence "iff" drops truth removal (T3). Shortcut (U-b): an extra-for-extra swap is not neutral at phase-1 states | **Proposition U′** [CON] §1.2, **PROVED**. Bad(W) = all three tests for every label. The phase-1 swap is bad iff k ∈ A, l ∈ J and \|W∩J\| = c. Independence charge is β_I(W). Both counterexamples were reproduced with the actual kernels: a missed transition of prob 0.826; η₁ I-term 0.945 (full) vs 0.119 (shortcut); swap-out prob 0.091, U-term 0.112 vs 0 | **Theorem B unaffected (PROVED)**: its proof uses only the §0 three-test definition, and W1's `progress_bounds.py` implements the full definition. W2-VT24G's "Prop. U VERIFIED as bookkeeping" must be downgraded to "ERROR in two shortcut sentences, repaired by U′" |
| 2 | Theorem B (finite) | VERIFIED after F′ | Conventions (C-0)–(C-5) added. Capped quantity β_H(x) := min{1, P(Bin(H,c_*⁺) < v) + Hη}, β_H(S₀) = 0 ([CON] §2) | — |
| 3 | Lemma P multi-target sentence | GAP, fixable | Explicit bound P* ≥ s_min(\|C\|/k)[1 − Q/(k+1)], **PROVED** ([CON] §3) | none |
| 4 | Cor B-M wording | VERIFIED. "No η → 0" holds only for fixed H | Wording corrected. Selection must be past-measurable. IND-T boundary: H′ = L+5 after stage-T resampling vs H = L+4 after the stage-T round | — |
| 5 | Lemma S (W1-T38E §3) | Inequality VERIFIED. "Attained by two-level weights" is an ERROR on the full domain | **Lemma S′**, **PROVED**: ω ≥ max(0, f − √(f(1−f)c)). Attained iff 1 − e < f < 1. For 0 < f ≤ 1 − e the infimum is 0 and not attained | D2 uses only the inequality at f > 0.1 = 1 − e, so no change |
| 6 | E3(ii) (W1-T38E §6.3) | ERROR: drops q < 1 of the locked T22(i-a). p = 2 counterexample | **Theorem E3′** ([CON] §6), **PROVED (deterministic)**: (ii) requires 0 ≤ q < 1 (or u < 1). Centre emission is part of LS0. LS0 cost is 1 + (ℓ+1)max_k[p + k(p−k)]. Counterexample reproduced "to every digit": formula 1.983334·10²³ vs π₀({1}) = 9.441608·10⁻¹⁴. In random cases, 726 of 2,095 with q ≥ 1 gave a false "> ½" | Downstream check: E3(ii) is "used nowhere downstream" (W4 uses only E3(i); W3-PXN P3 states q < 1; W1-EXP Thm 5/6 use u < 1). W1-T38E §7's (b1) sufficient condition is superseded. W2-BOOK §4.3 needs a wording fix |
| 7 | Lemma U limit | ERROR: 0.51/c_E, not 0.52/c_E | κ_n strictly decreasing, κ_n ↓ 0.51/c_E = 4.08(M+2σ²)/σ², and ≤ 0.52/c_E for n ≥ n₁ (explicit). **PROVED**. Family-count convention added | "Downstream effect: none." Upstream text fixes needed: W1-EXP Thm 1/Remark (b) "0.52/c_E" and "4.16"; W2-PREM REPORT "4.16" |
| 8 | NL0 quantifier (W1-T24G §6) | GAP: sup of sum ≠ sum of sups | Correct form Λ₂(a) := Σ_{l∉S₀} sup_{W∈𝒮_a°, l∉W} o_l(W) = o_P(1/log n). Rule: "labels outside, states inside, destinations of one label inside" ([CON] §8) | Costs the PG(a) design condition (W2-PREM Prop. NL0) and a factor (eD_n+1)^a in the rate. W2-PREM's EQ COUNTEREXAMPLE shows NL0(a ≥ 1) is "a genuine extra assumption". W2-PREM's results are unchanged. Wording fixes in W1 §6 and W2-VT24G §6 |
| 9 | CE1 broad wording | GAP as a blanket claim | **CE1-narrow**: COUNTEREXAMPLE, "PROVED from Lemma E and Lemma U(C5)". Sequence: p = ⌈n^{1/3}⌉, S₀ = {1}, one proxy at correlation r, exact Gram, any fixed d ≥ 1. Then (L+4)η_n → ∞ | The broad sketch stays PROOF SKETCH. "'H24 is false' must not be cited." Numerics: Lemma E floor ≈ 0.09–0.14; (L+4)·floor ≈ 1.7–1.9 up to n = 10⁵. Divergence is only logarithmic, since B = 16 is reached only at n ≈ 1.7·10⁷. At n = 200, r = 0.3: o₂(Y) = 0.235, floor 0.034, (L+4)·floor 0.40 |
| 10 | D2 finite | VERIFIED (potential first pilot stage) | Unchanged. Execution qualification written out | — |
| 11 | T38(b)-R route (b1′) | GAP: rate margins missing | **Corollary D2-∞, with rate margins. PROVED (implication)**. Fixed b₀ > 1/10, k_D < ∞, Dep ≤ 1 − c₀ w.p. → 1 plus P(NB′ᶜ) → 0, or general rates (H t_n² → ∞, Hβ_n g(b_n − t_n) → ∞) | The masked instance (LH, c = 1) is still a PROOF SKETCH; NB′ is the unfinished step. Card: true 0.6, provable 0.4 |
| 12 | T38(b)-R route (b2) | GAP: eligible-set interface, binomial bound | Repair certificate, data-measurable 𝔛_n, capped β, boundary 𝔉_T with H′ = L+5, DELIV to 𝔛_n with aggregate D3(𝔛) rates. Single (IND-T(b)) and product (IND-T(a)) forms. **PROVED (implication)** | "**DELIV(𝔛_n)** … **OPEN**" for every BVS family (C1 blocks the bridge-mass route; SHARE is "near-circular"). Card: DELIV true 0.5, provable 0.15 |
| 13 | T38 execution / output | GAP: U vs usable-but-unexecuted outputs | Strict convention 𝒪 = {exact, completed} plus an HPM convention 𝒪_H with the new term D_n^{sl}. GUARD written as (G1)–(G2) | **HQ must pick the output convention.** Under 𝒪_H, routes (a) and (b2) carry P(SMC ∩ 𝒜ᶜ), which no campaign result controls |
| 14 | "T11(vii)" citation; K | Replace by T21(C1); K = min(p, ⌊n/2⌋) | Done | — |
| 15 | IND-T | VERIFIED for the uninterrupted process | Boundary convention stated. First-fresh sets excluded. No completion conditioning | — |
| 16 | Lemmas F, F′, O, C, B1, B2, c₂ floor, B1′/B2′, P1, Lemma E | VERIFIED | none | — |

### T38 after repair (T38_STATEMENT.md Part I, "Theorem 5 (T38)"). Overall: "T38 is PROVED as a conditional theorem"

Assumptions for all parts: EX-A, EX-S, CAL (idealisations); SR; **GUARD** = (G1) the guard reads only the clock and
consumes no RNG, (G2) a run no guard stops performs exactly the R̄ (or R̄⁺) computation, classed as "IMPL"; (P) δ₁ = 1 − π(S₀) → 0
on R1 (s₀ fixed, p_n ≤ n^A). (P) is supplied by locked T03 or by T03♯.

- **(0) Composition, strict convention**: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, with D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). Two-sided form:
  P(𝒪, Ŝ⁺ = S₀) − (1 − P(U)) → 0. "Recovery with probability → 1 additionally requires P(U) → 0, which this theorem does
  not provide." Status: PROVED (T38_PROOF §1.1, via locked T21(C1)).
- **(0_H) HPM convention**: adds D_n^{sl} := P(SMC ∩ 𝒜ᶜ ∩ {S₀ ∉ 𝒮_cal ∪ 𝒮_LS0}) ("usable-but-unexecuted"). PROVED, "new,
  unreviewed".
- **(a) Favourable**: under (F) (1 − π₀(S₀) → 0), D_n → 0 with or without LS0. Sufficient conditions F1/F2/F3 (locked T22(iii)+EXP′, etc.).
  Under 𝒪_H, D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ) must be added, "and nothing here makes it vanish".
- **(b1) LS0 route**: (M1) ELIG(S°): P₀(π₀(S°) > ½) → 1, from W1-EXP Thm 6 under u < 1, "Do not establish (M1) through
  the printed E3(ii) without q < 1". (M2) POP-LAT(S°, m_n) with m_n ≥ M_n√(log n/n). (M3) λ_min ≥ φ₀², ‖μ‖²/n ≤ M. G and OP-LS0
  (LS0 executed, centre emitted, scans completed on every output fit; post hoc allowed; a stopped LS0 counts in U). Then D_n → 0.
  Theorem b1: "PROVED-UNDER (M1)–(M3)". Lemma LS-score, Lemma M and Prop. LH-LAT are each PROVED, not cross-family reviewed. W6 says it
  rechecked Lemma M and LS-score line by line, "No error found".
- **(b1′) D2 route, no method change**: fixed margins or general rates plus P(NB′ᶜ) → 0. Then the potential first tier-0 pilot
  stage scores S₀. PROVED (implication). Masked instance (LH c = 1): PROOF SKETCH. c ≥ 2: OPEN.
- **(b2) Gibbs path, no method change**: DELIV(𝔛_n) plus REP(𝔛_n) (single or product form). PROVED (implication). DELIV is OPEN.
  REP premises (W2-PREM) are "PROVED UNDER named conditions; on LH PROOF SKETCH (Theorem L)".
- **(b1-LH)**: LH exact Gram (p ≤ n − 1, c ≥ 1 linked pairs with 0 < |ψ_i| < min ρ, g ≤ B_n < 2g, fixed coefficients),
  S° = S₀∖M. Then (P), (M1), (M2) with a fixed margin m₀, and (M3) all hold. π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. "With LS0,
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no statistical hypothesis left open." Card: 0.88, "done (not cross-family reviewed)",
  method change **yes (LS0)**.
- **(c) Cost**: T32(i) ceiling plus 1 + (ℓ+1)max_{k≤K}[p + k(p−k)] for LS0; O((n+p)(p+B)log²(n+p) + p²log²(n+p)).
  Dependency k1: "T32(i) | CONJECTURE (checked as a valid loose bound by W3-VT38E)". Proof §6: "PROVED UNDER T32(i) (CONJECTURE)".
- **Not claimed (verbatim list)**: P(U) → 0; masked-regime evidence/PIP accuracy; anything conditional on completion; comparative
  superiority; "Finite-n error rates at n = 200"; "A masked p ≫ n family (W3-PXN's LH-iid claim is unverified)";
  "Masked-regime consistency without LS0 on an explicit family (OPEN)"; "DELIV for any BVS family (OPEN)".
- Remark 4: "H24 is not used." CE1-narrow is the reason.

**LS0.** LS0 is "the only fully proved masked route" (W4 §3; the dependency map marks it so). It must emit its centre as the
**first** evaluation: "Caching an un-emitted centre and relying on a later cache-hit emission does not update the ledger."
W6 records W3-PXN's interim n = 200 study data: "LS0 from the exact start mode on regenerated study designs at n = 200,
p ∈ {500, 1000}, S1 and S3. S₀ was scored in 48/49 fits, from start distances 5–14. These are recorded as interim data only."
LH numerics, copied from W4 and not re-run: LS0 scores S₀ in 10/10 for every c ∈ {1,2,3} and n ∈ {200, 800, 3200}.
"S₀ best among scored" is 8/10 to 9/10 at n = 200.

**What fails.** Reading Prop U as "commentary only"; keeping E3(ii) on the grounds that "s+1 even"; a GUARD-free actual-run form
("No version without some stop-only coupling is possible"); deriving DELIV(𝔛_n), which is OPEN.
**Needs escalation.** (1) HQ decision on the output convention. (2) Cross-family review of Lemma M, LS-score, Theorem b1,
LH-LAT, W2-BOOK Lemma RO/GUARD, W2-PREM B♯/B1′/CMP. (3) An independent code check of GUARD (G1)–(G2) in v3_runtime.h, v3_engine.h
and v3_core.cpp: "The whole execution side of T38 rests on it." (4) Edits to source branches (W2-VT24G verdict,
0.52/4.16, W1-T24G §6, W2-BOOK §4.3). (5) NB′ on LH (c = 1).
**Outside scope.** Name collision: W3-PXN's "Lemma U" (§9.1) ≠ W2-PREM's Lemma U, so rename them. "(e′)" means different
things in different files. Nothing addresses P(schedule_limit).
**Document inconsistency it flags.** W2-BOOK uses 𝒪_H := (no usable HPM)ᶜ, W4 uses 𝒪 = {exact, completed}, and A-REV1
reads U as "no usable HPM". "HQ must pick one for the paper."
**Confidence card (main rows).** Prop U′ 0.98 done; Theorem B 0.95; Lemma S′ 0.99; D2/D2-∞ 0.96; E3′ 0.99; Lemma U
0.99; NL0 (Λ₂) under PG 0.9; CE1-narrow 0.92; T38 (0)/(0_H) 0.95 (crux GUARD/IMPL); (b1) incl. LH 0.88; (b1′) 0.95
implication / instance 0.4; (b2) 0.93 implication, "**DELIV OPEN** (true 0.5, provable 0.15)".
**Common σ².** Not mentioned.

---------------------------------------------------------------------------------------------------------------------

## W6-FIXREV2 — head be2d456 (2026-11-02T19:07Z)

**Task.** Apply A-REV2 (Astra) to T03♯, the refined T37 (Theorem A), EXP′ and Lemma U. Files: NOTES.md, REPORT.md,
STATEMENTS.md (paper-ready statements). The NOTES record that it was "Pushed to theory/W6-FIXREV2 as instructed by HQ (the
harness-designated claude/ branch was not used)."

**Headline.** "All ten A-REV2 findings in the task list are confirmed and fixed." Every counterexample was rebuilt and "reproduces
A-REV2's numbers to 10 digits". "I found **no error in A-REV2's mathematics**; I disagree on one wording point and add
two qualifications."

### A-REV2 objections: repair, how it was done, and what remains

| # | Item | A-REV2 | Fix | Remaining / downstream |
|---|---|---|---|---|
| 1 | T03 "deterministic steps hold from n ≈ 1.2·10⁵" | ERROR (confirms V03 R1) | Confirmed independently: δ_n ≤ ½ at 115,150/130,328; **q_n ≤ ½ at 2,116,048/2,457,025**; e^{2ε_n} ≤ 4 at 25,571,897/29,755,302. New disclosure: "…hold only from n ≈ 2×10⁶ (p = n^{1.17}) to 2.5×10⁶ (p = n^{1.30}); the O_P constants are unspecified." "not a universal n₀" | S03 REPORT still has the old text (flagged, not edited). CARDS and W4 already use 2×10⁶ |
| 2 | T03♯ quantifiers/scope | VERIFIED with qualifications | Written into the statement: sup_m P, deterministic cutoff, fixed g₀, convergence only for E[1−π(S₀)], vacuous empty strong set | CARDS Card 1 needs "g₀ fixed", "sup_m", "posterior, not reported HPM" |
| 3 | S37 Lemma 0(b) "on every posterior miss, no search delivers S₀" | ERROR | **Lemma 0(b′)** (delivery inclusion, with ties and the S_c = S₀ case). CEX-2 reproduced: F(S_c) − F(S₀) = −2.2863, F(S₀+x₃) − F(S₀) = +7.2110 | W4 Remark 3 uses only the inclusion: OK |
| 4 | V37 R2 two-way dichotomy | ERROR: omits inferior local maxima and capped searches | **Prop. F** (exhaustive 3-way partition: I = E_LSᶜ; II = search miss (IIa certified inferior local max, IIb cap); III = explored competitor ≥ F(S₀)), PROVED. Out of 1,200 sims, 13 fits fall outside the 2-way split | "**CARDS Card 4 lines 267–269 quote R2 verbatim: must be replaced by Prop. F.**" Splitting the data into I vs III is OPEN: it needs F_pre per fit (`hpm_before$F` exists) and F(S₀) |
| 5 | A5(a) literal strict TD ⇒ TD′_P without POS | ERROR (confirmed false) | A5 restated with POS. "original T37(i) false at d = 0 too" | CARDS and W4 b1.3 already carry POS: OK |
| 6 | TD′_P "⟺ (L) ∧ ⋂ D_S" | ERROR with exact ties | **Lemma T** (exact equivalence via D_S^lex; strict D_S only sufficient) PROVED. **Lemma NT** (exact ties are P₀-null when the union has full rank and \|T′\|+\|T″\| < n−1) PROVED [new]. Corollary NT: the "iff" holds a.s. under non-degeneracy | W3-PGD defines TD′_P with strict D_S. Its positive and negative results "survive", but "exact ties have probability 0 under G" is "not justified in general (false with duplicates)" |
| 7 | "Weakest among at-most-Φ-move conditions" prose | ERROR | "weakest" withdrawn; PHI-REACH example given | — |
| 8 | κ → 0.52/c_* (4.16) | ERROR (minor) | 0.51/c_* = 4.08(M+2σ²)/σ², approached from above | **New downstream finding:** W3-PXN Lemma U (U1) asserts ν(1.02 + 1/(nφ₀²))/(c_*n) ≤ 1. This is false: c_* ≤ 1/16 gives ≥ 8.16. Only the constant κ₂ changes; "every PXN conclusion … survives" |
| 9 | Lemma U extra quantifier "every V of size ≤ k used below" | GAP | **Budgeted Lemma U(𝔉, 𝓗)**: \|𝓗\| ≤ C_H n^{a_H}, L > 4a_H, explicit failure probability. PROVED. Budget shown necessary (failure in 100% of draws, n = 10³…10⁶) | W2-PREM's 𝔉_k is covered; W3-PXN budgets correctly |
| 10 | Lemma U C3 matching lower bound under δ = 0 alone | ERROR (needs μ ∈ span X_T) | **C3-low** under μ ∈ span X_{W∖l}, PROVED. **C3-low′** (new, PROVED) under δ = 0 alone, exponent σ²Z²/(2C_R) ("valid but weak floor"). Counterexample exact: 16.2502645682 < 19.5571554183 | Only use found: W2-PREM §3.4 at a superset of S₀, which C3-low covers, "survives" |
| 11 | Random-design / actual-packing EXP′ | GAP (keep SKETCH) | Kept: SEX §1.5 and VEX R3 are PROOF SKETCH. "B ≥ 2g … **GAP**". κ₁₇ ≥ 0.1, not 0.15 | — |

Further items applied: Theorem 4's "masking persists iff η < 1/2.02" becomes a sufficiency statement. Theorem 3 needs a deterministic chain (H1-det).
Theorem 4 keeps H3 as a hypothesis. Theorem B's union runs over the data-independent Lat(𝒞). The V37 R4 tail is corrected to p·P(|Z| ≥ t). A4 quantifiers are split into (i)/(ii)/(iii).
New: "(A3) iff ℓ ≥ τ(S_c)".

### Corrected statements (STATEMENTS.md)
- **Theorem T03♯** §1.2. Status: PROVED; "V03 and A-REV2: VERIFIED under exactly these hypotheses". Hypotheses: R1 (X fixed,
  s₀ fixed, p ≤ n^A), G, R, SE_λ(j₀) with j₀ = ⌈(2A+1)s₀⌉+1, SE_w(m♯_n; g₀) with "g₀ > 0 a **fixed constant**", BM-∞ or BM(c).
  (1) 1 − π(S₀) = O_P(r_n). (2) MPM consistency. (3) P(S† ≠ S₀) ≤ 2E[1 − π(S₀)] → 0 (convergence only). (4) Strong-signal
  subset without beta-min. Scope: "posterior / global-HPM theory. It says nothing about the reported HPM Ŝ". **n = 200
  disclosure**: at (200, 500/1000), m♯_n = K = 100 (the cap binds; uncapped 146/168; locked m_n 201/215). "the cap removes the
  dimension-tail term there but does not verify SE_λ, SE_w or BM, and the O_P rate is not numerically informative."
  Card: "relevance at n = 200 nil (thresholds ≈ 2·10⁶, BM constant 43× short)".
- **T02(i♯)**, **T02(ii♯)**: PROVED (A-REV2 VERIFIED).
- **Theorem A (refined T37(i))**, §2.3: PROVED. A1 characterisation; A2 progress paths, τ(S) = m + e − σ; A3 production
  search returns S₀ certified **iff ℓ ≥ τ(S_c)** (ℓ ≥ a + d suffices), "up to exact HPM ties", with no π(S₀) > ½ premise;
  A4 necessity with quantifiers; A5 repaired: literal strict TD(d,0) ∧ POS ⇒ TD′_P. "**Without POS the implication is false**".
  TD′_P is defined through the engine map M (lex tie rule).
- **Lemma T**, **Lemma NT**, **Corollary NT**, **Lemma 0 (corrected)**, **Prop. F**: all PROVED.
- **Theorems B and C (T37)**: status unchanged. B (inclusions) PROVED. C stays PROOF SKETCH (C1–C2), COUNTEREXAMPLE (C3),
  CONJECTURE (C4).
- **EXP′ = Theorem 1** §3.1: PROVED. Fixed X, deterministic blocks, |C_b| ≤ B ≤ 16, SE-blk(φ₀). κ_EXP ↓ 0.51/c_*.
  **Corollary R1** (data-computable certificate): PROVED. "asymptotic κ_EXP does not prove that a given n = 200 data set lies on
  E_n; the certificate is the finite-n statement."
- **Theorem 3**: PROVED (deterministic chain). **Theorem 4**: "PROVED given H3"; PROOF SKETCH when H3 is discharged via
  reference transfer.
- **Lemma U(𝔉, 𝓗)** §4: PROVED (budgeted). C3-up unchanged. C3-low needs μ ∈ span X_{W∖l}. C3-low′ is new.

**Disagreement with A-REV2 (verbatim gist).** A-REV2's table calls S_c = S₀ "trivial success". W6-FIXREV2 says: "Disagree with
the wording … the final search from S₀ moves away whenever M(S₀) ≠ ⊥". In CEX-2, F(S₀+x₃) − F(S₀) = 7.21 > 0, so the fit fails.
"A-REV2's §4.2 text … is right; only the table's 'trivial success' overstates it." Qualifications: exact ties need a structural
tie (Lemma NT). The C3 violation in A-REV2's own family needs Z² ≳ 49, about 2·10⁻¹² per comparison.
**What fails.** A deterministic TD′_P ⟺ strict-D_S "iff" (impossible). A sharp general C3 floor without an extra uniform
RSS event. Upgrading "up to exact ties" to "exactly".
**Needs escalation.** Lemma NT's rank argument (cross-family). Prop F's data link: F(S₀) − F_pre per failed fit is "the one
missing data item (OPEN)". C3-low′ constants.
**Outside scope.** W3-PGD REPORT is still a stub ("DRAFT"), and CARDS lists **Theorem W** (W3-PGD's) as unverified.
W3-PXN was not reviewed by A-REV2. W2-T26 could switch to T03♯. S37's headline "0/541 … forced by monotonicity" needs F_pre.
**Downstream edits for HQ** (§2.4): F-REFINE CARDS (Card 4 false dichotomy; Card 1 wording), W3-PGD §0, W1-EXP/W2-PREM κ,
W3-PXN §9.1 (U1), W2-PREM §2, W1-T03R "1.2·10⁵ → 2·10⁶".
**Card.** T03♯ 0.95 ("relevance at n = 200 nil"); Theorem A tie-aware 0.97; Lemma NT 0.9; EXP′ 0.96 (B ≥ 2g random
partitions GAP, "possibly (held-out partition)"); Lemma U budgeted 0.96.
**LS0 / common σ².** Neither is mentioned.

---------------------------------------------------------------------------------------------------------------------

## W7-PART — head dc08f15 (2026-11-02T20:10Z)

**Task.** Prove the partition-recovery lemma "blocks = groups" for iid Gaussian designs, as used by LH-iid (W3-PXN) and by the iid
EXP′. Files: REPORT.md, PROOF.md.

**Algorithm facts (code-read, PROOF §0.1).** The partition uses only r̂ from G = XᵀX of the standardised columns. It is complete
linkage on 1 − |r̂| with R13 lexicographic ties, a top-down cut at B, then next-fit packing. "**The partition never reads y**", so it is
σ(X)-measurable and independent of ε. The only threshold is B = min(⌊√n⌋, ⌊√p⌋, 16) = 14 at the study size. The exact branch
(p ≤ 17) builds no partition. The Python port matches the compiled engine on 70/70 designs.

**Hypotheses.** GRP(ρ, ψ̄): |Σ_jl| ≥ ρ within groups, ≤ ψ̄ < ρ across, Σ ≻ 0. SIZE: g_max ≤ B(n,p) < 2g_min. IND: groups independent
(Theorem C only).

**Named results (exact labels; note the clash with other branches' Theorem A/B/C):**
- **Theorem A (deterministic) — PROVED**: A0 monotone heights and first-bad-merge structure; A1 (C\*) ⇒ laminar; A2
  laminar ⇒ (C\*) (side condition); A3 laminar + g_max ≤ B ⇒ blocks are unions of whole groups, and with B < 2g_min, blocks = 𝒢; A4 local
  margin (M) ⇒ (C\*). In 320 hard replicates, (M) held 15 times, while (C\*) ⟺ laminar ⟺ blocks = groups held 320/320 (261 successes).
- **L1** (pair-law representation; monotone in |r|) PROVED. **L2** (Hotelling-density tail bound) "PROVED (density cited;
  checked numerically two ways)".
- **Theorem B** — PROVED: P(blocks ≠ 𝒢) ≤ Σ_within P_ρ(|r̂| ≤ t) + Σ_cross P(|r̂| ≥ t), for t ∈ (ψ̄, ρ).
- **Corollary B** — PROVED: P(blocks ≠ 𝒢) ≤ (2/(√π(1−ρ)))p²√n e^{−(n−4)I\*}. With p ≤ n^A this is ≤ p^{−C} for n ≥ n₀. Example n₀: (ρ=0.7, ψ̄=0)
  A=1.25, C=1 gives 282. For LH (0.7, 0.5), A = 1.25, C = 1 gives 2,788.
- **L3** (rotation invariance for independent groups) PROVED. **Theorem C**, **Corollary C** PROVED (exponent 2I\*). **κ**:
  "PROVED (identity); PROOF SKETCH (the mesh-1/n bookkeeping)".
- **CE1** (g_h > B ⇒ failure w.p. 1): COUNTEREXAMPLE. **CE2** (2g_min ≤ B: blocks ≠ 𝒢 surely; blocks are unions of whole groups):
  "COUNTEREXAMPLE / PROVED". **CE3** (|ψ| > ρ): "COUNTEREXAMPLE (mechanism PROVED; blocks ≠ 𝒢 by simulation)".

**Numerics at n = 200, B = 14 (study size, p = 500/1000).**
- Independent groups, ρ = 0.7, g ∈ {8, 10, 14}: Cor C gives a rigorous bound of 3.4e-9 to 1.1e-8 (p = 500) and 1.4e-8 to 4.7e-8 (p = 1000). Theorem B gives
  3.4e-5 to 1.3e-4.
- LH (ρ = 0.7, ψ = 0.5, g = 10, c = 1): the "rigorous bound is only **0.17**", from the dependent linked pair. MC CP95 for the pair is 1.5e-4
  (0/20,000). c = 2 gives 0.33 rigorous, 3.0e-4 MC.
- Actual algorithm: 0 failures in 2,000 replicates in these cells.
- ρ = 0.5 is vacuous (2.4–97), yet the algorithm had 0/300 failures. The algorithm fails at ρ ≤ 0.4 and at ψ ≥ ρ.
**Task-spec disagreement.** The task's "9 ≤ g ≤ 16" is "false at n < 256 (B = 14 at n = 200)". The correct range is g ∈ [⌊B/2⌋+1, B].
"No algorithm change is needed in the stated regime."
**Incompleteness (inconsistency).** REPORT §4.3 has several **"FILL"** cells (the p = 1000 column for most stress rows), and §4.4 (n-sweep) is
just "FILL". The head commit is a report with unfilled numbers.
**What fails.** The margin route (W3-PXN P1's D_in < D_out) "is a poor description at n = 200". Plain MC of E[S_L+S_N] is not a bound.
No rigorous dependent-pair bound beyond the local margin. "Not laminar ⇒ blocks ≠ 𝒢" is false in general.
**Escalation.** Independent check of Theorem A (A0–A2). Hotelling density form/convention. A rigorous n = 200 LH linked-pair bound
(condition on the hubs). κ_C bookkeeping.
**Outside scope.** W3-VEXP GAP (b) (which groups pair up when 2g ≤ B, i.e. the study's g = 5) is still OPEN. W3-PXN P1 can cite Theorem B.
S5-type global factor: 0/300 failures, but Theorem B is vacuous. The neighbour graph was not studied.
**Card.** Partition lemma: "high", done (needs review of A and L2). LH n = 200: MC 1.5e-4, rigorous 0.17. Which groups share a block (2g ≤ B): OPEN,
"maybe (row-split partition)".
**LS0 / common σ²**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## W7-SEC — head 7e33e8a (2026-11-02T19:55Z)

**Task.** Prove T05 (disclosed negative), T33 (floating-point numerical margins) and T32(i) (resource counts; verify W5-LOCKBOOK, don't duplicate).
Files: NOTES.md, REPORT.md, PROOF_T05.md, PROOF_T33.md.
"Every PROVED is a candidate I checked line by line (same-family check only)."

**T05.** Hypotheses: G; ORTH (XᵀX = (n−1)I_p, p ≤ n−1); 1 ≤ s₀ < p, s₀ ≤ K. λ_j := (n−1)θ*_j²/σ*², τ_n := log n + 2 log((2p−s₀)/s₀).
- **Lemma T05-R (exact representation). PROVED.** Q_S = (n−1)V_S/V_tot, D_S = n^{|S|}. "The s_y standardisation cancels exactly."
  **Cor T05-R1**: the HPM is a top-k set. This proves T05(i).
- **Thm T05-U (finite-n failure). PROVED**: P₀(S† = S₀) ≤ e^{−dδ²/4} + ∏_{j∈S₀}[Φ(√λ_j − t_δ) + Φ̄(√λ_j + t_δ)].
- **Cor T05-U∞. PROVED.** **Cor T05-Ŝ (reported HPM)**: "PROVED, given the code reading of `local_search`".
  P(Ŝ = S₀) ≤ bound(U) + P(final local_limit).
- **Thm T05-L**: "PROVED (limit)". liminf ≥ Φ(c)^{s₀}, which gives T05(ii). The explicit n₀ is log n ≈ 227 ("useless").
- **Prop T05-O. PROVED.** **Thm T05-G (= T05(iii)). PROVED.** Gap at p = n^a: [√(1+2a) − √(2a)]√log n.
- **Wording correction**: "**'Loses a √log n factor'** is false as a multiplicative statement at p = n^a, a > 0. It is true
  additively in amplitude, and multiplicatively only when log p = o(log n)." On the energy scale it is a factor (1+2a)/(2a).
- Proposed paper sentence (REPORT §2): oracle 74% vs HPM 2% at n = 10⁹, p = √n, λ = 0.7τ_n.
- n = 200 relevance: "T05's remark does not describe the study design. ORTH needs p ≤ n − 1; the study has p ∈ {500, 1000} > n = 200.
  It is a mechanism remark only."

**T33.** Hypotheses FP, NOUF, LIB(c_L), SMALL. Cited Higham H1–H4.
- **Lemma T33-M. PROVED**: I ≼ H_S, A_S, with explicit upper bounds, also with duplicates. **Lemma T33-Q (new). PROVED**: Q_S ≥ y′y/(n+1).
- **Thm T33-S. PROVED** (given H1–H4, FP, NOUF, LIB, SMALL): Cholesky succeeds; explicit η_H, η_m(S), η_F(S).
- **Cor T33-NF. PROVED**: "**numerical_failure is impossible at n = 200 for every p and y**" (a priori up to n ≈ 1,286 with K = n/2).
- **Prop T33-H. PROVED**: the HPM over a common scored set is within 2η̄′. "exact ties are decided by rounding unless the computed
  scores are bitwise equal".
- **Prop T33-Z**: deterministic part PROVED; "the a-priori ε part **PROVED but vacuous at the study's budgets**". η_Z ≈ 10⁻¹⁰–10⁻⁶.
  ε must be measured by replay. The path-free route is OPEN.
- **COUNTEREXAMPLE (engine heuristic)**: `error_bound()` (`v3_score.h:242`) "is not a bound" at large n. The ratio is 1.17 at n = 10⁵ and 6.2 at
  n = 4·10⁶. It held with about 25× room at n ≤ 4,000 (n = 200 unaffected). R9 `global_certified` on the exact branch inherits it.
  Recommended fix: "**implementation fix recommended** (not a statistical method change)".
- Numerics: the production scorer vs a 60-digit reference. Max |Δlog m| is 1.3e-13 (iid n = 200) to 1.3e-10 (n = 4000).

**T32(i).** "**W5-LOCKBOOK Theorem T32(i) (T32-a) and Corollaries T32(i-lit), T32(c): PROVED (by W5); independently re-checked
here, no error in the count.**" The recount matches W5 exactly: 267,610,872,968 at (200, 500) and 562,428,743,935 at (200, 1000).
**Addendum (fp pilot). PROVED**: without EX-A the pilot has ≤ T_e + 1 stages. This adds +1,320,960 on 2.676·10¹¹ at (200, 500).
There is a harmless slip in W5's corollary proof (1 + 4ℓ ≥ 5ℓ is false for ℓ ≥ 2; the conclusion stands).
**INCONSISTENCY across branches**: W6-FIXREV1's T38 dependency k1 and W7-SEP's I11 still list T32(i) as **CONJECTURE**.
W7-SEC (and W5-LOCKBOOK) say PROVED. T38(c)'s status line should be revisited.

**Escalation.** Demmel's criterion constant (Higham Thm 10.7, "used it from memory"). libm accuracy on NOTS. The engine `error_bound`
decision (Felipe/OPS). The Cor T05-Ŝ code reading. ε of VAL-FP by replay.
**Outside scope.** `error_bound` feeds R9 certificates. T34 can use Cor T33-NF. The `q_nonneg` fallback is dead code for n + 1 < 10⁷.
**Card.** T05(i) 0.99; T05(ii) 0.97; T05(iii) + remark 0.98; T05-Ŝ 0.93; T33(i) 0.99; T33 fp bound 0.9; T33(ii) 0.98; T33+VAL-FP
0.95 (η) / ε OPEN; T32(i) 0.97.
**LS0 / common σ²**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## W7-SEP — head **44ca480** (2026-11-02T20:16Z; "REPORT tables filled from completed exact runs (386 replicates)"; supersedes e8b5416)

**Task.** The Separation Theorem, i.e. what the tempering bridge buys. (a) Start-only methods (iid draws plus local search, or LS0 alone) fail unless the basin
contains S̃₀. (b) One-shot importance correction fails. (c) v3 succeeds, cited. Files: NOTES.md, REPORT.md, PROOF.md.

**Headline disagreement with the task spec (HQ).** "**The task's claim (a), as written, is false on its own family.** On LH,
'start-only + production local search' does **not** fail … The task's exception … is the generic case, not an exception.
**COUNTEREXAMPLE** (by proof, Corollary GU-LH; and numerically in 100% of replicates)." Also: "**There is no super-polynomial
separation in the frozen setting**, because c ≤ s₀ is fixed, and **no separation at all between the tempering bridge and a single
greedy search from the start mode** on LH … What the theory supports is '*moving off the start is needed*', not '*tempering is
needed*'."

**Named results (PROOF.md §1, §4).** Families: LH exact Gram (p ≤ n−1, c ≥ 1 linked pairs, fixed coefficients, g ≤ B_n < 2g) and
LH-iid (W3-PXN, through I7, which is "PROVED by a single run, **unverified**"). Q* := p^c n^{c/2}.
- **Theorem SEP (refined)**:
  - **(A) iid start discovery**: P(S₀ scored by Q iid π₀ draws plus tables) → 0 or 1 as Q/Q* → 0 or ∞. The polynomial budget n^α fails iff
    α < c(a+½). Hypotheses EX-A; LH (W1-EXP Thm 5(b), Lemma 4.2). **PROVED**. "LH-iid: PROVED given W3-PXN P1, P4, unverified."
  - **(B) one-shot importance correction**: 1 + χ² ≥ Q*e^{−Mstat}(1+o_P(1)); KL ≥ (c log p + (c/2)log n)(1−o_P(1)) − O_P(1);
    relvar = (1/π₀(S₀) − 1)/Q; Î_Q = 0 w.p. → 1 below Q*. Adds locked T03 via W1-EXP Thm 5(d). **PROVED** (overlaps O-WSTAB WS7).
  - **(C) start + search (negative)**: on LH every C ⊆ R is in the basin, so LS0 and "one draw + search" succeed at O(p² log n). **PROVED**
    (candidate; uses W4-T38FULL Lemma M, "same-family VERIFIED only"). Task clause (a) for search-augmented methods: **COUNTEREXAMPLE**.
  - **(D) v3 (citation)**: T38(b1-LH) with LS0 is "PROVED-UNDER its premises, unreviewed". Without LS0: D2 for c = 1 ("NB step PROOF
    SKETCH"), and "BG1 for every fixed c (PROOF SKETCH, unverified; needs n/(T_e log(p√n)) → ∞)". Cost: "T32(i) ceiling (CONJECTURE)"
    plus the LS0 term (PROVED).
  - **(E) exponents** (p ≍ n^a): iid/IS need c(a+½) (sharp); LS0 or draw+search ≤ 2a (+log); v3 with LS0 ≤ a + max(1,a)
    (+log, conditional on T32). "Separation iid vs v3 ⇔ c ≥ 2; iid vs LS0 ⇔ c ≥ 2 or a < ½." The PROOF §1 table marks the v3 row
    "PROVED-UNDER I11 (CONJECTURE)".
- **Proposition BASIN** (PROVED, deterministic): LS0 scores S₀ iff S̃₀ ∈ 𝔅_ℓ. Q draws + search succeed with prob 1{S̃₀ ∈ 𝔅_ℓ} ∨
  [1 − (1 − π₀(𝔅_ℓ))^Q].
- **Proposition GU (greedy universality)** (PROVED, candidate): G; exact Gram; isolated relevant set R ⊇ S₀ (Σ_{R,Rᶜ} = 0, |R| ≤ r);
  λ_min(Σ_R) ≥ φ₀²; fixed signals θ₀ > 0; p ≤ n^A. W.p. → 1, from every C ⊆ R the production search reaches, scores and certifies S₀
  within τ_GU = 1 + ⌈(2s₀/φ₀²)log(M/(φ₀²θ₀²))⌉ + (r − s₀) moves. Needs no PGD. "It proves W1-T37R's Conjecture C4 in this case".
  **Lemma GU-1** (population descent) and **Lemma GU-2** (one addition at a superset) are used. **Corollary GU-LH** (PROVED, candidate).
  Remarks: LH-iid version PROOF SKETCH; centres with data-chosen nulls OPEN.
- Inputs table (PROOF §0): I8 T38(b1-LH) "PROVED-UNDER … (unreviewed)"; I9 BG1+Prop LH "structure PROVED; score estimates PROOF
  SKETCH; unverified"; I11 T32(i) "CONJECTURE".

**Numerics (new in 44ca480, §4.1).** Exact enumeration on LH at p ≤ 20, configs B2 (c=2, p=20, Gram and iid), V2 (c=2, p=18), C3
(c=3, p=18), n = 100…409,600, 386 replicates.
- "LS0 scored S₀ in all 386 replicates." min π₀(𝔅_ℓ) ≥ 0.99996 in every replicate.
- From n = 1600 on, "**every** centre in 2^R scores S₀ in every replicate". At n ≤ 400, failures are move-limited or posterior misses, "There was
  **no** genuine search trap". Moves needed plateau at 10–12 while ℓ grows.
- C3 masking: log₁₀π₀(S₀) goes from −5.42 to −10.72 (slope −1.47 vs −1.5). P(hit | Q_f) falls from 0.39 to 7.8·10⁻⁴. For c = 2, Q_f keeps a hit probability of 0.5–0.9
  at fixed p.
- Scaling §4.2 (p up to 864, c = 3, n = 4000): iid needs ≈ 5·10¹² draws; LS0 uses 2·10⁴ evaluations (3/3).
- GU stress §4.3: 40 random designs (24 violate PGD). At n = 200 only 22/40 have every C ⊆ R scoring (18/40 certifying), median π(S₀) 0.48.
  At n ≥ 50,000 it is 40/40.
(The earlier head e8b5416 had "TABLE_PLACEHOLDER" in §4.1. The new head fills it. §§5–8 are unchanged.)

**What fails.** "Start-only + local search fails" is false (GU). "Super-polynomial budget" is false in R1 (Q* is polynomial since c ≤ s₀; R-T20(i)'s
exponential law needs exponential masking, "which LH does not have"). Separating bridge from search is impossible on exact-Gram isolated-R
families. Possible places for a separation are all outside the frozen setting: a posterior barrier (PB: "the bridge also fails there
asymptotically: 82% → 51% of islands"), move-limit binding, growing c, or weak signals. TD′_P needs PGD. GU with data-chosen nulls is OPEN.
**Escalation.** (1) Cross-family check of Prop GU (GU-1(b), the GU-2 determinant, use of Lemma M with data-chosen pairs). "GU is the
result that changes the story". (2) Lemma M is only same-family VERIFIED. (3) **HQ decision on the paper's spine**. Suggested wording:
"Theorem SEP: no method that samples from the start and reweights can find or weight the truth with fewer than p^c n^{c/2}
draws; v3 does it at polynomial cost of fixed degree, by moving off the start." "Avoid 'the sampler is needed' unless 'sampler'
means 'moves'." (4) LH-iid GU.
**Outside scope.** A possible **no-LS0 T38(b) route via GU**: the final local search from Ŝ_pre, if Ŝ_pre ⊆ R. Status: CONJECTURE.
GU answers C4. **n = 200**: "In the study's S4/S6 at n = 200 the start mode is 12–14 moves from S₀ (W3-PXN §5) with ℓ = 10–11, so the
move limit, not a barrier, is what stops LS0 there."
**Card.** SEP(A) 0.97; SEP(A) LH-iid 0.92; SEP(B) 0.98; task (a) with LS "false as a separation (COUNTEREXAMPLE)"; Prop GU 0.93
("needs cross-family check"); GU on LH-iid/general 0.85/0.6; SEP(C) v3 0.9 (LS0) / 0.75 (BG1); exponent separation 0.9 "done given
T32"; super-polynomial separation "false"; bridge-vs-search separation "false on exact-Gram isolated-R families".
**Staleness / inconsistency.** W7-SEP cites O-BGIBBS only as "BG1 (PROOF SKETCH)". It does not cite O-BGIBBS's main result **Theorem BG3**
(PROVED) + **Prop LH-lock** (PROOF SKETCH), the final run alone with no temperature condition. It also treats T32(i) as CONJECTURE, which W7-SEC
contradicts.
**Common σ²**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## F-SHARE — head 13bc665 (2026-11-02T14:06-06:00, i.e. 20:06Z)

**Task (BRIEF, Fable 5.1, laptop).** Find "the RIGHT delivery theorem in the masked regime for the method as it is", for route b2
(no LS0). Give the sharpest counterexample and minimal method change if delivery fails, and compare with LS0 and T39. Work independently of W4-SHARE (Opus cloud).
Files: BRIEF.md, REPORT.md, PROOF.md. Two Opus 5.5 helpers ran the exact checks and simulation.

**Headline.** "**The right delivery theorem is a closure theorem, not an envelope theorem (Theorem F1, PROVED).**" Its class is
the superset class W(S°) = {x : S° ⊆ x}, with KEEP(W, η) at both endpoints.

**Named results.**
- **KEEP(W, η)**: sup_{x∈W} K_φ(x, Ω∖W) ≤ η for every φ ∈ {φ₁,…,φ_T, 1}.
- **Theorem F1 (closed-class delivery) — PROVED**: under EX-A, EX-S, CAL, KEEP: P(some particle ever outside W | 𝓒) ≤ Nπ₀(Ω∖W) +
  N(T+L+4)η per island. On the complement this gives DELIV(W) with the whole population eligible.
- **Lemma 1.2 — PROVED**: the one-round exit bound for W(S°), via endpoint deletion and swap-out odds plus π₀(Ω∖W).
- **Corollary F3 — PROVED**: under KEEP with the bound → 0, the D4 envelope is ∏(1 − η_s) deterministically and "the C1 mechanism cannot start".
- **Lemma 3.1 — PROVED** (LH exact Gram unit structure). **Lemma 3.2 — PROVED** (hub signal δ² ≥ θ_b²(n−1)λ_min).
- **PK(d\*)** (population proxy-keep): checked exactly for (ρ,ψ,g) = (0.7, 0.5, 4); "CONJECTURE in general". **DOM**: every truth in S°
  outweighs every missing hub by c₄n ("Void for c = 1").
- **Lemma 3.3 — PROVED given W1-EXP Thm 1 and PK** (start keep odds ≤ 2pe^{−c₁n}). **Lemma 3.4 — PROOF SKETCH** (uniform posterior keep
  and swap margins).
- **Theorem F2 — "PROOF SKETCH; structure PROVED"**: LH exact Gram, **p ≤ (1−c₀)n**, PK(g−1), DOM. (a) π₀, π of Ω∖W ≤ Cpe^{−cn};
  (b) KEEP with η ≤ Cp²e^{−cn}; (c) the exit probability → 0; (d) DELIV(W) with every particle eligible.
- **§4 (repair on W, crossing temperature φ_hub = O(log(p√n)/n))**: PROOF SKETCH. **CONJECTURE 4.3** (extras bookkeeping across
  resampling) "is the only non-routine step".
- **Theorem F1′ (reversible leaks)**: "CONJECTURE, routine from D4".
- **CONJECTURE F2-iid**: LH-iid with W_d(S°) (≤ d extras), η = O_P(n^{−1/2}polylog). "the crux is the uniformity of the null leakage".
- **Proposition SH** (cited in the headline as the sharp threshold for fitter leaks). **Lemma PD** is used.
**Numerics** (LH16 p=16 c=1; LH20 p=20 c=2; ρ=0.7, ψ=0.5, g=B=4; n = 400…25600). KEEP margins are Θ(n) at both endpoints. The worst state is
S° plus all a-proxies. The exit bound is 10⁻²⁶ at n = 1600. **DOM failed marginally**: "the truth-for-hub swap j → b′ in LH20 at n = 1600, where in one
replicate it is posterior-favourable by 4.7 nats" (unfavourable by ≥ 52 at n = 6400). The enlarged class W⁺ "is **not** closed (+175 nats)".
In simulation (N = 1000, 76 islands) no particle was ever outside W. LH20: S₀ was scored at stage 1 by a Gibbs flip in 8/8 islands, below
φ\*; "S₀ was never first scored in the terminal rounds and never missed".
**What fails.** D4/D5 as the primary tool. W = 𝓡_d leaks at n^{−1/2}polylog per round ("That is why W1/W4's sup-exit bounds on 𝓡_d were
useless"). Uniform keep margins with p near n. Enlarging the class for DOM. PK in general. Extras across resampling.
**Escalation.** Lemma 3.4 remainders (by "a stronger prover", cross-family). Conj 4.3/§4.4 (= REP(W(S°)) on LH). PK as a theorem. F1′.
F2-iid. "Independent check of the reading of C1".
**Outside scope / method change.** "**No method change is needed on LH**". LS0 "delivers eligibility for free but needs TD′". T39
"fails on posterior barriers". "The closed-class route is the only one that uses the bridge, and it is the one consistent with the
n = 200 data (98 % of fresh scores from Gibbs, local search repaired 0 fits)." Paper text: T38(b2) should read "DELIV(W(S°)) by Theorem
F2 (every particle eligible) + REP(W(S°))". **n = 200**: "W3-PXN showed the study's masking is dilution, not LH-type cancellation;
nothing here speaks to n = 200 (the constants in §4.2 need n > 4^g)." O-BGIBBS overlap: BG1 covers φ₁ ≥ φ_hub, and F2 + §4 is the
multi-stage complement.
**Card.** F1 0.99 done; F3 0.98; Lemmas 3.1–3.2 0.99; PK numerics 0.98 / general 0.8; Lemma 3.3 0.95/0.9; Lemma 3.4 0.9/0.8; DOM 0.9
("fails marginally at LH20 n = 1600 in 1/4 replicates"); **Theorem F2 0.9 / 0.75, method change "no"**; §4 REP 0.85/0.5; **T38(b2) on LH
exact Gram, no tweak, every fixed c: 0.85 / 0.5**; F1′ 0.9/0.85; F2-iid 0.75/0.4; route (b2) outside T03's regime "fails through REPAIR".
**Common σ²**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## O-BGIBBS — head 55679ee (2026-11-02T13:54-06:00, i.e. 19:54Z)

**Task (ledger).** "no-LS0 masked theorem via bridge-Gibbs discovery". The server instance drafted Lemma R, BG1 and Prop LH. The laptop added BG1′,
BG2, LH-rate, BG3, LH-lock and the numerics. File: REPORT.md.

**Headline.** "**Main result: the final run alone discovers S₀ on the masked family LH, for every fixed c, with no LS0, no pilot, no
temperature condition and no survival hypothesis (Theorem BG3, PROVED; Proposition LH-lock, PROOF SKETCH for p fixed).**"
"With T38(0): **P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for the original method, without LS0.** This answers W4-T38FULL item 6 on LH with p fixed."

**Named results (exact labels, statuses).**
- **Code fact F (PROVED from code)**: pilot φ₁ ≥ min(1, 1/T_e).
- **Lemma R (multi-flip round lemma) — PROVED**: P_x(round at φ scores z) ≥ P(O)(1 − Dep_φ)₊ α_φ^{|Λ|−1}. "one evaluation suffices" (SR).
- **Theorem BG1 (pilot first-stage bridge-Gibbs discovery) — PROVED**: P(z ∉ 𝒮_cal) ≤ Hπ₀(𝒜) + e^{−Hπ₀(x°)/8} + 1/K +
  exp{−Hβ/(1+2Kρ_𝒩)}. ρ_𝒩 is a two-endpoint quantity. **Corollary BG1-∞ (PROVED given the premises).**
- **Theorem BG2 (cumulative scoring hazard) — PROVED**: P(not scored by t₁) ≤ P(Λ_{t₁} < Λ) + e^{−Λ}. "Discovery is a hazard, not a
  survival event".
- **Corollary BG1′ — PROVED** (temperature-dependent β; final-run stage-1 version with φ_lo = 0; needs only Hβ_* → ∞).
- **Proposition LH — "structure PROVED, score estimates PROOF SKETCH"**: LH exact Gram, every fixed c ≥ 1. (iv) needs n/(T_e log(p√n)) → ∞.
  Conclusion: P(S₀ ∉ 𝒮) → 0 for the original method.
- **Proposition LH-rate — "𝔅_M part PROOF SKETCH; uniform-in-φ proxy part CONJECTURE"**. Scoring temperature φ_sc: = 0 for c = 1, and for c = 2
  if p = o(√n). c = 3 is borderline. For c ≥ 4 it is > 0. "(R1)–(R2) are PROOF SKETCH for p fixed … CONJECTURE" for p → ∞. Obstruction for c ≥ 3
  in the final run (PROOF SKETCH): it needs survival over O(log log n) stages, "This run does not prove it."
- **Theorem BG3 (locked start set + terminal downhill) — "PROVED (deterministic given (L1), (L2))"**: P(z not scored) ≤ Nπ₀(𝒰ᶜ) +
  N(T+L+4)ε_𝒰 + exp{−N(L+4)β₁}. It uses "no resampling" in the terminal rounds (`v3_engine.h:352–373`).
- **Proposition LH-lock — "PROOF SKETCH; the deterministic inputs are checked exhaustively for the two simulated designs"**: LH exact
  Gram, **p fixed**, 𝒰 = {y ⊇ S°}. Population gaps (C1) deletion, (C2) swap, (C3) hub addition, and their γ₀ analogues (C1′, C2′).
  (C1′)/(C2′) are "PROVED in §3.7" for every parameter value. (C4) is automatic. The γ₁ gaps (C1)–(C3) are "verified by exhaustive
  enumeration" only. Example values: c = 2 gives min C1 = 0.218, C2 = 0.030, C3 = 0.086; c = 3 gives 0.238, 0.051, 0.093. "A proof for general (ρ, ψ, g, c) is open". The order constant is 1/m!,
  "deliberately crude".
**Numerics.** LH exact Gram, p = 16 (c = 2) / 18 (c = 3), g = B = 4. Pilot stage 1 scored S₀ in 160/160 replicates (n = 400–25600) with φ₁ ≪ φ_hub.
For c = 3 the stage-1 hazard is Θ(1) and spills into stage 2. In BG3 runs, "min_t N_𝒰/N = 1" in 19/19 islands. The terminal miss bound is ≤ 10⁻³²⁰ (log₁₀ between −321
and −2301).
**What fails.** (L2) fails on W4-SHARE's posterior-barrier design PB. This is a "COUNTEREXAMPLE at finite n … to discovery by any local kernel, and no method
change (LS0, T39) fixes it". (L1) fails if a start-mode member is not supported by its block table (not on LH). For p → ∞, uniform gaps and a polynomial order
constant are CONJECTURE. The ESS-share (D2) route "does not iterate" and needs NB, "which fails whenever a masked proxy is drawn".
**Escalation.** LH-lock's score-level reduction to (C1)–(C4) "is now the **critical path** for the no-LS0 masked theorem". A general-(ρ,ψ)
proof of the γ₁ gaps. An independent check of BG3/BG2 (stopped-count application; terminal rounds have no resampling). Prop LH (ii)–(iv). Code
facts.
**Outside scope.** "BG3 is a general template". W4-SHARE E1a–E1e are candidates, "recommended to HQ as the next task". LH-iid is CONJECTURE.
**Finite-n**: "The BG3 bound is numerically meaningful at n = 400 … the paper can therefore cite it as a finite-n explanation of why the
masked LH runs never miss S₀".
**Card.** BG3 0.97 done; LH-lock p fixed 0.9/0.8; "**T38(b) without LS0 on LH exact Gram, p fixed, every fixed c (final run alone)**
0.9 / 0.8, method change **no**"; p → ∞ 0.75/0.45 CONJECTURE; BG2 0.98; Lemma R 0.97; BG1/BG1′ 0.95; Prop LH/LH-rate 0.85/0.7; c ≥ 3 bridge-stage
without BG3 OPEN 0.75/0.35; PB COUNTEREXAMPLE 0.95.
**Convergence with F-SHARE.** BG3 (locked 𝒰 = {y ⊇ S°}) and F-SHARE F1/F2 (closed W(S°) under KEEP) are the **same superset-class idea**,
found independently. Differences: F2 assumes p ≤ (1−c₀)n plus PK + DOM and leaves REP (Conj 4.3) open. LH-lock assumes p fixed and uses terminal
downhill (C3) for REP. LH-lock's (C2) swap gap includes the truth-for-hub case that F-SHARE calls DOM. F-SHARE observed a marginal *sample-level*
DOM failure at LH20 n = 1600; O-BGIBBS's *population* gap C2 is positive (0.030). These are not contradictory, but it is a finite-n fragility.
**LS0 / common σ²**: the whole branch is "without LS0". Common σ² is not mentioned.

---------------------------------------------------------------------------------------------------------------------

## O-STAGES — head 8d3c142 (2026-11-02T13:52-06:00, i.e. 19:52Z)

**Task (ledger).** Prove a theorem for the realised stage count T_n (F-DRAFT's W′/W″), which is T26's premise and T38's cost exponent. File: REPORT.md.

**Named results.**
- **Lemma 0 (reference-state identity). PROVED**: ρ_V(u,v) = q_u(R)q_w(R)/q_v(R)², with w = 2v − u, for every R ∈ V. (Label clash with W6-FIXREV2's and
  O-WSTAB's "Lemma 0".)
- **Lemma 1 (monotonicity). PROVED**: bisection finds the exact frontier ("settles W′'s open obligation (1)").
- **Theorem G (greedy optimality). PROVED**: the greedy grid is the shortest valid grid. max(T*_V, T_P) ≤ T_grid ≤ T*_V + T_P.
  COVER perturbation bound.
- **Theorem L (path length). PROVED**: √c·T*(c) → L as c → 0. Worst case T* ≤ ⌈1.54D⌉. Not the answer at production c.
- **Halving count** N(w̄) = max{1, ⌈log₂(w̄/(w̄−1))⌉} (proof given; no separate status word).
- **Theorem F (favourable regime: deterministic sandwich). PROVED**: N(w₊) ≤ T*_Ω ≤ N(w₋) when Δ ≤ 0.0513.
- **Corollary W′ (BO favourable). "PROVED conditional on (LL)"**. (LL) is F-DRAFT Theorem W's layer law at general w, "PROOF SKETCH".
  Result: |T* − ⌈log₂(1 + 1/g_n)⌉| ≤ 1; p ≤ n^A ⇒ T* ≤ ⌈log₂(1 + 2AR²)⌉ + 1 = O(1).
- **Theorem M (masked two-state crossing). PROVED**: log₂(A₀ − 1.48) − 0.95 ≤ T* ≤ log₂(A₀ − 2.2) + 11, independent of A₁.
- **Lemma P (perturbation). PROVED.** (Label clash with W6-FIXREV1's Lemma P.)
- **Corollary W″′ (corrected W″). "PROOF SKETCH for the families; PROVED given PAIR"**: T* = log₂A₀ + O(1). Proxy split gives log₂n + O(1).
  LH/T27 gives log₂(c log p + (c/2)log n) + O_P(1), "proved for c = 1 given PAIR. For c ≥ 2 … OPEN". PAIR itself is unproven.
- **COUNTEREXAMPLE to W″ as stated** ("O(1)"): T* = log₂A₀ + 7.7 ± 0.4 numerically. It reproduces F-DRAFT's 14 and 16 and gives 18 at n = 3200.
**T26/T38 consequences.** P1 is automatic in the favourable regime once Δ_n → 0. In the masked regime Δ_n → 1, so P1 fails. T38(c): T_n = O(1) (BO favourable),
log₂n + O(1) (proxy), O(log log n) (LH), ≤ T_e = O(log²(n+p)) always.
**n = 200 numerics** (p = 12 exact): BO favourable T* ∈ {1, 2, 4} at n = 200. Proxy split T* = 14 at n = 200. Cancellation pair (LH-like c = 1) T* = 9–10
for n = 200 to 12800. Layer-model miss: "T* = 2 against 4 … at p = 100, n = 200, R² = 0.9". **Study stage counts unavailable**:
`Results/SMC_BVS_v3_production/` "has no per-fit stage counts". Recommendation: export `length(frozen$grid) − 1` and the pilot count.
**What fails.** Path length at production c. A length lower bound without regularity. Extending T22(iv-b) to pairs.
**Escalation.** (LL) at general w ("O-WSTAB may supply it"). PAIR and c ≥ 2 chains. Pilot fidelity (OPEN). Theorem M constants.
**Card.** Grid structure high/done; T_n vs length done; W′ high/medium (LL); W″ "FALSE as 'O(1)'"; T26 P1 high; T38(c) medium-high.
**Tension with O-WSTAB.** O-STAGES's W′ rests on (LL), F-DRAFT Theorem W's layer law at w ∈ [1,2]. O-WSTAB gives a **COUNTEREXAMPLE to [FD] W(c)
and W(b) on the divergent side** (2Ar > 1). O-WSTAB's own W′ (ORTH) is PROVED independently (T_ideal ∈ {1, 2}), consistent with O-STAGES's g → 1/(2Ar)
reading. So (LL) as quoted from F-DRAFT may need restating for 2Ar > 1. O-STAGES Lemma 0/Theorem F and O-WSTAB Prop L/Prop G are the **same
identity and sandwich, proved independently**. O-STAGES Theorem M and O-WSTAB WS7(d) agree on the log₂(masking depth) stage count.
**LS0 / common σ²**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## O-PW2 — head e685ead (2026-11-02T13:37-06:00, i.e. 19:37Z)

**Task (ledger).** "PW2 / relative-variance bound for Ẑ (two-sided evidence control)". File: REPORT.md. (The labels Theorem A/B/C clash with W6-FIXREV2's
Theorem A, W6-FIXREV1's Theorem B and W7-PART's Theorems A/B/C.)

**Named results.**
- **Theorem A (exact identities). PROVED (candidate).** (A1) a martingale with M_{T−1} = W_T. (A2) Var_c(W_T) = (1/N)Σ_s E[W_s² Var_{μ_s}(h_{s,T})].
  (A3) the (1−1/N)-weighted form. (A4) PW2's left side is exactly V_t − V_{t−1}. "No mixing assumption is used."
- **Theorem B (two-sided non-asymptotic bound). PROVED (candidate).** (B1) |N·V_T − Σ(1−1/N)^{T−1−s}σ²_{s,T}| ≤ Σ_{s≥1}H²_{s,T}√(V_s(1+V_s)).
  (B2) the recursion U_T ≥ V_T, pooled /4. (B3) closed form σ²_T/N + O(N^{−3/2}). "It delivers T25(iv)'s **conclusion** directly … with PW2 removed as a
  hypothesis."
- **Corollary B2 (PW2 itself, explicit)**: PW2 holds with a_t = (S_t − S_{t−1})₊ and ν_t = O(N^{−3/2}). "the rate constant is the increment of
  the asymptotic variance, **not** χ²_t". Card: "done modulo item 7.2" (sign handling).
- **Theorem C (primitive constants). PROVED (candidate).** Recursions in χ²_t, δ²_t, ḡ_t, λ_t (L² mixing defect), ε_t. Exact refresh gives Π(1+χ²/N) − 1.
- **COUNTEREXAMPLE**: "PW2 with a_t = χ²_t (the 'perfect-mixing' guess) is false". At p = 6, Gibbs-only, a_4* = 0.90 vs χ²_4 = 0.111. At p = 8, a* = 4.13.
**Study scale.** "**Not vacuous at the study's N and T only conditionally.**" It needs λ_t(1 + ḡ_tλ_t) ≤ κ < 1 plus BW_W on Ω. "With only locked
T09/T13 inputs, the bound is valid but vacuous at study scale." Under the premise, relative SD ≈ 0.15 worst-case for pooled Ẑ/Z. T13 ESS alone cannot bound
σ²_T. The exact-refresh formula underestimates by up to 20.7×.
**Numerics.** Exact enumeration at p ≤ 10, n = 60 (not n = 200). (A3) holds to 1e-9. U_t ≥ V_t always. Theorem B is within 6–35% of the truth at N = 2500. OPTIONAL_PW2's
B_T is vacuous (≈ 1–223).
**What fails.** The one-step parent-uniform route (OPTIONAL_PW2 (A)–(C)). PW2 with a_t = χ²_t. Removing the sup norm H.
**Escalation.** Check (A3) and B's Cauchy–Schwarz step. Cor B2 sign handling. Per-fit certification of L² mixing (for O-CERT/T26).
**Outside scope.** The pair recursion is an exact E[(Ẑ/Z)²] oracle at p ≤ 12. The M_{s−1} identity is a handle for lower bounds (T26).
**Card.** Thm A high/done; Thm B high/done; Cor B2 high; Thm C high; non-vacuous at study N,T "medium … low–medium", possibly with "a per-fit spectral
diagnostic"; PW2 with a_t = χ²_t **false**.
**Overlap.** O-WSTAB WS8(b) proves PW2 with a_t = χ² under the IID idealisation and lists WS8(d) "PW2 for the actual hybrid particle
system at t ≥ 2" as **OPEN**. O-PW2 shows that this constant is false for actual kernels and supplies the correct a_t. This is consistent: the IID
idealisation is exactly what fails.
**LS0 / common σ² / n = 200**: not mentioned.

---------------------------------------------------------------------------------------------------------------------

## O-WSTAB (incl. review_CHECK_SEP_W.md) — head 2ec3099 (2026-11-02T13:59-06:00, i.e. 19:59Z)

**Task (ledger).** "prove the draft's weight-stability theorem (chi²/KL(pi‖pi0) vs cross-block dependence; ESS; regime dichotomy)".
Files: REPORT.md, PROOF.md (WS1–WS8), review_CHECK_SEP_W.md plus review scripts and outputs.

**PROOF.md (WS series).** WS1 exponential-family identities (PROVED). WS2 one importance step (PROVED). WS3 block-orthogonal case (PROVED).
WS4 cross-block Gram perturbation (PROVED). WS5 leakage and regime dichotomy ("deterministic parts PROVED; favourable conclusion by
composition"; reduction PROVED). WS6 favourable weights: (a)–(c) PROVED, (d) lower bound PROVED, "upper bound CONJECTURE". **WS7 (masked regime; why the sampler must move) PROVED**:
ESS_∞ ≤ π₀(S₀)/π(S₀)²; KL ≥ π(S₀)log(1/π₀(S₀)) − log 2. "(c) *Reweighting cannot create the truth*". "(d) *Accepted grids need only log-log many stages*".
"what the sampler must supply is **transport** (moves), not reweighting". WS8: (a) PROVED; (b) "PROVED under the idealisation IID" (PW2 with
a_t = χ²_t); (c) PROVED; (d) PW2 for the actual system **OPEN**.

**REPORT named results.**
- **Proposition W0 (three faces). PROVED.** A self-contained Doeblin argument for the independence move: TV ≤ (1 − 1/M)^t, and from the worst state ≍ M steps.
  "(The spectral statement … of Liu (1996) is **not** used; I have not seen that source.)"
- **Lemma W1 (= WS3). PROVED.** Under BO, π₀ is π with the shared noise precision replaced by an independent copy per block. "**with known σ² the same
  tables give d ≡ 0, π₀ = π**". This bears directly on the common-σ² start question (F-SIGMA/O-MIX): under BO, the start/posterior mismatch is entirely the
  per-block noise precision.
- **Lemma W2 (exact dilution form). PROVED.** κG ≤ LR ≤ κG/(1−y). No EXP′ needed.
- **Proposition L (ℓ-form of T13). PROVED.** log(1+χ²(q_v‖q_u)) = ℓ(u) + ℓ(2v−u) − 2ℓ(v).
- **Proposition G (ideal-grid sandwich). PROVED.** max{1,⌈log₂(1+1/g₊)⌉} ≤ T ≤ max{1,⌈log₂(1+1/g₋)⌉}.
- **Lemma SEP (separable domination under ORTH). PROVED.** **Lemma SEP′ (integral form). PROVED.** (Not the same as W7-SEP's Theorem SEP.)
- **Theorem W (ORTH; two-sided).** H-ORTH: G; ORTH; s₀ and θ* fixed; r := R²_pop ∈ (0,1); p → ∞ with p log p = o(n); any partition; B fixed or ≤ 16.
  (a) both ends concentrate; (b) uniform upper bound; (c) uniform lower bound; (d) convergent side: lower half needs p^r/√n → 0, and the upper half needs
  "p^r√(log p)/√n → 0" ("review finding F1"); (e) divergent lower bound log(1+χ²) ≥ (1 − o_P(1))e^{(L_n − C₁ − 1)/r}; (g) divergent upper bound;
  (f) KL, TV → 0 in all cases. Headline: "both sides **PROVED**".
- **Theorem W′ (ORTH; ideal grid).** T_ideal = 1 if 2Ar < 1, = 2 if 2Ar > 1, always ≤ 2 w.p. → 1. PROVED "for the ideal full-space grid". The method's
  V-restricted pilot grid is OPEN. General BO with correlated blocks is "PROOF SKETCH", and p ≍ n is "OPEN".
- **Counterexample W(c)** to F-DRAFT Theorem W(c) ("log(1+χ²) = [R² log p − ½ log n]₊ + O_P(log log p)"): on the divergent side
  log(1+χ²) ≥ n^{A−1/(2r)−o(1)}. At n = 10¹⁶, p = n^{0.95}, r = 0.9: "the exact lower bound is 8.8·10³ nats, while W(c) predicts 13". [FD] W(b) is also
  false there. The threshold Ar ≶ ½, W(a), and W(b) on the convergent side are correct.
- Paper consequence: "The draft's 'weak dependence ⇒ stable weights' holds for KL and TV, and for χ² only when 2Ar < 1, even at zero cross-block correlation."

**Review (review_CHECK_SEP_W.md; independent Opus 5.5 checker, same family, at commit b3d89e2).** "It found no fatal flaws."
Verdict table:
- Lemma W2 **verified** (F5 exposition).
- Prop L **verified**.
- Prop G **verified** with the max{1,·} reading (F4).
- Lemma SEP **verified** (F7).
- W(a), (b), (c), (d)-lower and (f) **verified**.
- **W(d) upper half "not verified as stated (verified under p^r√(log p)/√n → 0)" (F1 gap)**.
- W(e) **verified** "in the form … (stated constant off)" (F3).
- W′ **verified** (F6).
- Counterexample: "**verified** against the formula as quoted in REPORT … **not verified** that [FD]'s own statement/hypotheses cover H-ORTH ([FD]
  not seen)" (F8 gap, scope).

Reviewer's key caveat: "the *rigorous* W(e) bound at this (n, p) is only … 8.9 < 13.08: the finite-n contradiction is numerical, the proved
contradiction is asymptotic." The reviewer's independent LB is 7,961 nats vs the author's 8,770.
Author response (REPORT end): F1 is accepted and the statement restricted. F2–F7 are fixed. F8: scope tied to [FD]'s hypotheses, which the author read in NEW_TARGETS §W.
"Not reviewed: Lemma SEP′ and W(g), added after the review began." The review scripts' outputs confirm the Mills/Chernoff margins and the F1 window
(ρ_n(2)√log p grows from 1.08 to 2.41).
**What fails.** [FD] W(c)/W(b) on the divergent side. The expectation route (E e^{(1+r)Z²/2} = ∞). A uniform cross-block perturbation (WS4) needs
ε_S = o(1/n), "too strong", so "W3 (the cross-block term) stays at [FD]'s PROOF SKETCH level, and Theorem W is stated for ORTH". p ≍ n OPEN.
**Escalation.** Line-by-line check of SEP and W(a)–(f). W(e), (g) constants and SEP′. General BO (PROOF SKETCH). Method grid vs ideal grid (OPEN).
**Outside scope.** Masked regime in ℓ-language (WS7). The divergent regime's dominant models are S₀ plus k\* extras ("Worth one sentence in the paper's §4.4").
**Card.** W0 0.99; W1 0.99; W2 0.98; Prop L/G 0.98; Lemma SEP 0.95; Theorem W(a)–(d),(f) 0.93 "done (reviewed once)"; W(e) + counterexample 0.93;
W(g) 0.9; W′ ORTH 0.9; W′ method grid 0.6/0.3; Theorem W general BO 0.85/0.6; p ≍ n 0.8/0.4.
**n = 200**: not addressed. All numerics are at p ≤ 16 or astronomical (n, p).

---------------------------------------------------------------------------------------------------------------------

## Cross-branch notes: disagreements, inconsistencies, label collisions

1. **Verifier vs author / Astra vs Opus.** W6-FIXREV1 agrees with A-REV1 on every item. W6-FIXREV2 agrees with A-REV2 except for the
   "trivial success" wording (S_c = S₀). O-WSTAB's same-family reviewer found one gap (F1), which the author accepted, and one scope gap (F8). There is no
   Opus-vs-Astra mathematical dispute in these ten branches.
2. **Agents vs task specs (HQ).** W7-SEP: task clause (a) is FALSE on LH (COUNTEREXAMPLE via GU), and there is no super-polynomial separation and no bridge-vs-search
   separation. W7-PART: the task's "9 ≤ g ≤ 16" is false at n = 200 (B = 14). O-STAGES: F-DRAFT's W″ "O(1)" is false. O-WSTAB: F-DRAFT Theorem W(c), and W(b)
   on the divergent side, are false.
3. **T32(i) status conflict.** W7-SEC confirms that W5-LOCKBOOK's T32(i) is PROVED. W6-FIXREV1 (T38 k1, §6 "PROVED UNDER T32(i) (CONJECTURE)") and W7-SEP (I11,
   (E)) still call it CONJECTURE. W6-FIXREV1's (c) and W7-SEP's exponent separation are therefore stated more weakly than they need to be. This should be reconciled.
4. **No-LS0 masked route: status drift.** W6-FIXREV1's T38 "Not claimed" includes "Masked-regime consistency without LS0 on an explicit family (OPEN)" and
   "DELIV for any BVS family (OPEN)". Two later branches give candidates on LH exact Gram. Neither is fully PROVED: both bottom out in a PROOF SKETCH.
   - O-BGIBBS: BG3 PROVED plus LH-lock PROOF SKETCH, p fixed, every c. Card 0.9.
   - F-SHARE: F1 PROVED plus F2 PROOF SKETCH (structure PROVED), p ≤ (1−c₀)n. REP is still a sketch (Conj 4.3). Card 0.85/0.5.
   W7-SEP cites only O-BGIBBS's BG1 (PROOF SKETCH) and misses BG3.
5. **Superset-class idea found twice.** O-BGIBBS (BG3/LH-lock, "locked 𝒰 = {y ⊇ S°}") and F-SHARE (F1/F2, "closed W(S°) under KEEP") found it independently. W7-SEP's GU
   is a third, search-based route (LS0 or the final search from Ŝ_pre ⊆ R, the latter CONJECTURE). F-SHARE's sample-level DOM failure (LH20, n = 1600, +4.7 nats)
   vs O-BGIBBS's positive population C2 gap (0.030) is a finite-n fragility, not a contradiction.
6. **Stage counts.** O-STAGES (Lemma 0, Theorem F, Theorem M) and O-WSTAB (Prop L, Prop G, WS7(d)) prove the same identity and halving sandwich
   independently. O-STAGES's W′ is conditional on F-DRAFT's layer law (LL), which O-WSTAB's counterexample undercuts on the divergent side (2Ar > 1). O-WSTAB's ORTH W′ is
   PROVED. Paper text should use one version.
7. **PW2.** O-WSTAB WS8(b) (PW2 with a_t = χ² under IID, PROVED) vs O-PW2 (a_t = χ²_t COUNTEREXAMPLE for actual kernels). This is consistent, because WS8(d) is OPEN. O-PW2's
   Theorem B replaces PW2 in T25(iv), but it is vacuous at study scale with locked inputs only.
8. **Label collisions to resolve before the paper.**
   - "Theorem A": W6-FIXREV2 (refined T37), O-PW2 (variance identity), W7-PART (complete linkage).
   - "Theorem B": W6-FIXREV1/W1-T24G (Gibbs repair), O-PW2, W7-PART.
   - "Theorem C": W6-FIXREV2/T37, O-PW2, W7-PART.
   - "Lemma 0": W6-FIXREV2, O-STAGES, O-WSTAB.
   - "Lemma P": W6-FIXREV1, O-STAGES.
   - "CE1": W6-FIXREV1 (H24), W7-PART (g > B), W1-T38E's C1.
   - "Lemma SEP" (O-WSTAB) vs "Theorem SEP" (W7-SEP).
   - "Theorem W": O-WSTAB/F-DRAFT vs W3-PGD's Theorem W (cited in W6-FIXREV2).
   - "Lemma U": W2-PREM vs W3-PXN (flagged by W6-FIXREV1).
   - "Prop. M": W4-SHARE, cited by several branches.
9. **Incomplete reports at head.** W7-PART REPORT has "FILL" cells (§4.3 p = 1000 column; all of §4.4). W7-SEP was incomplete at e8b5416
   (TABLE_PLACEHOLDER) and is fixed at 44ca480. O-STAGES's summary line 8 says the head SHA is "given in the run's final message".
10. **LS0.** LS0 is the only fully proved masked route in T38 (W6-FIXREV1 b1/b1-LH, "PROVED-UNDER", not cross-family reviewed). LS0 must emit its centre
    first, and its cost includes the +1. W7-SEP: LS0 alone does the job on LH, so "tempering is needed" is not supported. F-SHARE and O-BGIBBS: no LS0 needed on LH. At
    **n = 200** the evidence is W3-PXN's interim 48/49 (quoted in W6-FIXREV1). W7-SEP: in S4/S6 the move limit (ℓ = 10–11 vs distance 12–14) "is what stops
    LS0 there".
11. **Common σ².** It is mentioned only in O-WSTAB Lemma W1/WS3: "with known σ² the same tables give d ≡ 0, π₀ = π". Under BO, the start is π with
    per-block noise precisions. No branch in this group proves anything about a common-σ² start or about T38 route (a) without LS0 via common σ².
12. **n = 200 relevance / disclosures.**
    - T03♯: "relevance at n = 200 nil" (thresholds ≈ 2·10⁶). The cap m♯ = K = 100 binds at (200, 500/1000).
    - T05: ORTH needs p ≤ n − 1, so it is "a mechanism remark only".
    - T33: numerical_failure is impossible at n = 200; the engine heuristic is fine there (25× room).
    - W7-PART: independent groups ≤ 2.3e-8; LH linked pair rigorous only 0.17 (MC 1.5e-4).
    - F-SHARE: "nothing here speaks to n = 200". The study's masking is dilution (W3-PXN).
    - O-BGIBBS: finite-n meaningful from n = 400.
    - O-STAGES: no study stage counts were exported.
    - W6-FIXREV1 "Not claimed: Finite-n error rates at n = 200"; CE1 floor 0.034 at n = 200.
    - W7-SEP GU stress: only 22/40 designs fully succeed at n = 200.
