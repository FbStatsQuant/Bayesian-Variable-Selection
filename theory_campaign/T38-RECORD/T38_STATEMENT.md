# T38 (paper Theorem 5): statement of record, v3

Run T38-RECORD, 2026-11-02, branch `theory/T38-RECORD`. Spec: `theory/W8-SYNTH · SYNTHESIS.md §8 task 6`.

**What this is.** One statement of record for Theorem 5. It merges every version and every repair that has landed. It
contains **no new mathematics**: every clause below is copied from a source, with the source's status word. No status is
upgraded. Where sources disagree, the disagreement is marked **⚑ CONFLICT** and both sides are given (Part III).

**What it supersedes.**

| Version | Where | Head | Reviewed by |
|---|---|---|---|
| v0 | `theory/W1-T38E · PROOF.md §7 · T38(b)-R` | 436a712 | W3-VT38E (same family): VERIFIED. A-REV1 (cross family): whole statement GAP, composition and route (b1) VERIFIED, repaired formulation in A-REV1 §7 VERIFIED as a conditional implication |
| v1 | `theory/W4-T38FULL · T38_STATEMENT.md` | a0f9cb5 | W4's own same-family subagent; W5-VMASK (same family) verified LS-score, Lemma M, Theorem b1, LH-LAT; A-REV3 (cross family) reviewed the W3-PXN joint route only |
| v2 | `theory/W6-FIXREV1 · T38_STATEMENT.md` | a7833f3 | **nobody**: same-family repair of A-REV1; cross-family re-review is A-REV5 (in progress) |
| **v3** | this file | — | nobody; no new mathematics |

v3 is the citation target for the paper's Theorem 5 until A-REV5 and A-REV7 report. The proofs stay where they are:
`W6-FIXREV1 · T38_PROOF.md` for parts (0), (0_H), (a), (b1), (b1′), (b2), (c); `W4-T38FULL · T38_PROOF.md §3` for
Lemma LS-score, Lemma M, Theorem b1 and Prop. LH-LAT; `W3-PXN · PROOF.md` with `W5-VMASK · REPAIRS.md` for (b1-LH-iid);
the candidate routes' own PROOF files for Part I.D.

**Status words** follow `theory_campaign/PROTOCOL.md`. "SF" = same-family check (a Claude run checking a Claude run).
"XF" = cross-family check (Astra: A-REV1 to A-REV4). Every PROVED here is a **candidate**: nothing is adopted or locked.

**Cross-family reviews in flight** (fetched at the end of this run; none had pushed a verdict file):
- **A-REV5**: sources W6-FIXREV1, W6-FIXREV2, W4-T38FULL, W3-PXN, W3-PGD, W1-T38E and the A-REV1/A-REV2 reviews. It
  re-reviews v2 against A-REV1 §7, and the LS0 route.
- **A-REV6**: sources W5-B2ENV, W5-VMASK, W5-LOCKBOOK, W7-PART, W7-SEC, F-SHARE, F-MASKPIP, O-BGIBBS, O-DILUTE, O-WSTAB
  and the A-REV3/A-REV4 reviews. It covers the post-A-REV4 results.
- **A-REV7**: sources F-SHARE, O-BGIBBS, W5-B2ENV, W5-VMASK, W7-SEP, W1-EXP, W3-VEXP, W6-FIXREV1, A-REV3. It is the
  cross-family verification of the **no-LS0** masked theorem on LH (W8-SYNTH §8 task 1, XV-NOTWEAK).

---

## Part 0. Change log

### 0.1 v2 (W6-FIXREV1) → v3

| # | Where in v2 | Change in v3 | Source | Effect on status |
|---|---|---|---|---|
| V1 | Objects, "LS0" | LS0 is **part of the method**, no longer a tweak. Felipe approved it on 2026-11-02, conditional on O-LS0's data check. The check passed: LS0 changed the reported HPM in **0 of 2,394** completed fits. The reported model is Ŝ⁺. "v3 as run" (no LS0) is kept as a named variant, because the study's fits were produced without it. | `theory/campaign · HQ/SR_AUDIT.md` "Decision recorded"; `theory/O-LS0 · REPORT.md §1, §6`; `theory/E-SPINE · Docs/Theory/AMENDMENTS_20261102.md §2.1` | none (decision, not mathematics) |
| V2 | Objects, output events | Both conventions are kept. The strict convention 𝒪 stays the default, as in v2. It is now marked as an **open decision** (Part IV, D1), with W8-SYNTH's recommendation (strict). | `W6-FIXREV1 · REPORT.md` escalation 1; `W8-SYNTH · SYNTHESIS.md §4.12` | none |
| V3 | (c) and dependency k1 | T32(i) is cited as **PROVED** (W5-LOCKBOOK), re-checked by W7-SEC ("no error in the count"; same family). v2 listed it as CONJECTURE because v2 predates W5-LOCKBOOK. The W7-SEC fp-pilot addendum is attached: without EX-A the pilot has at most T_e + 1 stages, which adds 1,320,960 to 2.676·10¹¹ at (n, p) = (200, 500). | `W5-LOCKBOOK · REPORT.md` item 4; `W7-SEC · REPORT.md` T32(i) | ⚑ CONFLICT III.1. (c) becomes PROVED-UNDER T32(i), with T32(i) PROVED (SF only) |
| V4 | (b1-LH), LH-LAT | "m₀ … which is sharp" becomes "m₀ is valid; it is sharp when the pairs are homogeneous". The exact Φ ≥ 2 margin is m₀♯ (W5-VMASK R5). Nothing in Theorem b1 uses sharpness. | `W5-VMASK · REPAIRS.md R5`, verdict rows 23, 23′ | none (an overstatement withdrawn) |
| V5 | Dependency map b1.2, b1.4, b1.5, b1.8 | The review column now records W5-VMASK's second same-family verification of Lemma LS-score, Lemma M, Theorem b1 and Prop. LH-LAT (verdict rows 20–23). There is still no XF review. | `W5-VMASK · REPORT.md §2` | none |
| V6 | Not claimed: "A masked p ≫ n family (W3-PXN's LH-iid claim is unverified)" | Replaced by part **(b1-LH-iid)**, with its actual record: PROVED (candidate); SF VERIFIED by W5-VMASK; **XF GAP** (A-REV3: P6, P7 and the joint LS0 route). It is shown separately from the headline. | `W5-VMASK · REPORT.md §3`; `A-REV3 · REVIEW.md` verdict table | none: recorded at its weakest verdict |
| V7 | (M2), sufficient conditions | For (M2) or the lattice condition, cite **W_Lat** (W5-VPGD R6.2) with **Prop. LH-PGD** (R6.3). Do not cite Theorem W in its region form: it fails with an exact tie on masked LH when c ≥ 2 (R6.1). Cor. GU-LH (W7-SEP) is recorded as a second proof of the search step on LH. | `W5-VPGD · REPAIRS.md R6.1–R6.3`; `W7-SEP · PROOF.md §4.2` | none |
| V8 | (b1′) instance, dependency d4 | v2: "LH c = 1: PROOF SKETCH; NB′ the unfinished step". Now there are two candidate instances. **D2-LH** (W5-B2ENV Cor. D2-LH, PROVED given cited candidates, author only) covers LH exact Gram, c = 1, p/√n → ∞. **W5-VMASK R1** (single run) covers LH-iid, c = 1. Both are listed in Part I.D, pending A-REV7. | `W5-B2ENV · REPORT.md §2`; `W5-VMASK · REPAIRS.md R1` | none: candidates, not merged into the headline |
| V9 | (b2) DELIV; Not claimed: "DELIV for any BVS family (OPEN)" | DELIV(𝔛_n) stays **OPEN** in general. On LH there are now candidate delivery results: F-SHARE F1 (PROVED) with F2 (PROOF SKETCH); W5-B2ENV Prop. CONF (PROVED under STAB-LH); O-BGIBBS BG3's lock (L1) via LH-lock (PROOF SKETCH). They are listed in Part I.D. | `F-SHARE · REPORT.md §2`; `W5-B2ENV · REPORT.md §2`; `O-BGIBBS · REPORT.md §2` | none |
| V10 | Not claimed: "Masked-regime consistency without LS0 on an explicit family (OPEN)" | Out of date. It now reads: "**candidates on LH, pending cross-family review (A-REV7)**; none is claimed in the headline." | `W8-SYNTH · SYNTHESIS.md §1, §4.2`; `E-SPINE · AMENDMENTS_20261102.md §2.4` | ⚑ CONFLICT III.2 |
| V11 | Remarks | A new remark, "What the masked half shows", carries the spine correction: **moving off the start is needed, not tempering**. There is also a new "Why it matters" paragraph (Part I.F). | `W7-SEP · REPORT.md §1` items 2–4; `E-SPINE` commit dd0ec8a | none |
| V12 | Remarks (v1 Remark 4, "n = 200") | Rewritten from the per-fit data. S-ELS: 565 posterior misses, 0 search misses, S₀ scored in all 2,394 completed fits, the final local search made 0 moves. O-LS0: the (M1)–(M3) counts. O-DILUTE: dilution. The thresholds come from W2-VT03R R1 and W6-FIXREV2. | `S-ELS · REPORT.md §1, §3`; `O-LS0 · REPORT.md §1` item 6; `O-DILUTE · REPORT.md §7` | none |
| V13 | v1 Remark 3, "Why LS0" (dropped in v2) | Restored with a corrected citation. Lemma 0's delivery inclusion is now `W6-FIXREV2 · Lemma 0(b′)` with the three-way Prop. F, not W3-VT37R R2, which A-REV2 rated ERROR. | `W6-FIXREV2 · STATEMENTS.md`; `A-REV2 · REVIEW.md §2 S37` | none |
| V14 | (P) | The statement of record for T03♯ is now `W6-FIXREV2 · STATEMENTS.md §1.2`. It adds the quantifier sup_m P, a fixed g₀, and the scope note "posterior / global-HPM theory, not the reported HPM". | `W6-FIXREV2 · STATEMENTS.md §1.2`; `A-REV2 · REVIEW.md §2 S03` | none |
| V15 | Labels | Proposed paper labels are added in brackets where campaign labels collide, for example Lemma M (W4-T38FULL) → [Lemma SC]. The full table is in `REGISTRY_v2.md §F`. The old labels stay valid as citations. | `W8-SYNTH · SYNTHESIS.md §4.15` | none |

### 0.2 v1 (W4-T38FULL) → v3

Everything in 0.1 applies, together with v2's own change log S1–S9 (`W6-FIXREV1 · T38_STATEMENT.md Part 0`). In short:
- S1: strict versus HPM output convention, and partial returns counted in U;
- S2: GUARD written as (G1)/(G2), with STATUS derived from it;
- S3: K = min(p, ⌊n/2⌋);
- S4: the (b1′) rate margins, D2-∞;
- S5: the (b2) eligible-set interface, repair certificates, capped β_H, boundary 𝔉_T with H′ = L + 5;
- S6: (0) proved by the direct set argument, with the two-sided form added;
- S7: the LS0 cost includes the "+1" for the emitted centre;
- S8: the A-REV1 verdicts entered in the dependency map;
- S9: (b1) does not use E3(ii).

Two v1 items beyond S1–S9:
- v1's (c) used log²n where v2 and v3 use log²(n+p);
- v1's Remark 3 "Why LS0" cited W3-VT37R R2, which is corrected in V13.

### 0.3 v0 (W1-T38E T38(b)-R) → v3

v0 is the composition proved in W1-T38E §7. v1 and v2 already absorb it. Its differences from v3:
- No GUARD or R̄ formulation. A-REV1 §7.3 required one; v1 introduced it.
- Route (b1′) had no rate margins (A-REV1 §7.1 GAP; repaired by D2-∞ in v2).
- Route (b2) quoted uniform REPAIR on 𝓡_d (A-REV1 §7.2 GAP; repaired by 𝔛_n and repair certificates in v2).
- (b1) was established through E3(ii) without q < 1 (A-REV1 §3.3 ERROR; replaced by E3′(i) with W1-EXP Thm 6 in v2).
- Lemma S's attainment claim was unrestricted (A-REV1 ERROR; Lemma S′ in v2).
- The cost had no "+1" (A-REV1 §6).
- The citation "T11(vii)" is replaced by locked T21(C1).

### 0.4 What v3 does *not* change

Every part's mathematics is v2's. That covers (0), (0_H), (a), (b1), (b1′), (b2), (b1-LH) and (c), apart from V3's
dependency status. Only these change: citations, review columns, the candidate list (Part I.D), the "Not claimed" list,
the remarks and the decision record.

---

## Part I. The theorem

### I.A Objects

As in v2 (`W6-FIXREV1 · T38_STATEMENT.md Part I`), repeated here so this file stands alone.

- **The method.** The method is v3 **with LS0** (V1). **"v3 as run"** denotes the same method without LS0, the variant
  that produced the study's fits. Every statement below says which variant it covers.
- **Potential uninterrupted run.**
  - R̄ is the record the method produces under EX-A with the preflight and the in-run guard removed (W2-BOOK §0.1).
  - Its status is st̄ ∈ {exact, completed, schedule_limit}. On the SMC branch, {st̄ = completed} = 𝒜, the calibration
    success event.
  - R̄⁺ is R̄ followed by LS0.
- **Actual run.** The actual status st and the outputs are functions of (R̄, Ξ), where Ξ is the operational element.
  𝒢 := {st = resource_limit} is the stop event.
- **Output events.**
  - *Strict convention (default; Part IV D1):* 𝒪 := {st ∈ {exact, completed}} and U := 𝒪ᶜ. A `schedule_limit`,
    `numerical_failure` or guard-partial return counts as no output.
  - *HPM convention:* 𝒪_H := {an HPM is reported and st ≠ resource_limit} and U_H := 𝒪_Hᶜ.
  - Bars denote the R̄ versions: 𝒪̄ and 𝒪̄_H.
- **Scored sets.**
  - 𝒮 is every model the method scored: tables, initial draws, the pilot, calibration, final rounds (both Gibbs
    configurations and rejected proposals) and local-search scans.
  - 𝒮⁺ := 𝒮 ∪ 𝒮_LS0, and Ŝ⁺ is the best model in 𝒮⁺ under the method's total order. For v3 as run, 𝒮⁺ = 𝒮 and Ŝ⁺ = Ŝ.
  - 𝒮_cal ⊆ 𝒮 is the calibration part.
- **LS0.**
  - One extra production local search (M §6.10), centred at the start mode S̃₀ = argmax π₀, computed exactly by
    max-plus convolution with a deterministic tie rule.
  - **The centre is the first evaluation and is offered to the HPM** (`emit_centre = true`). W5-LOCKBOOK calls this
    "mandatory, not cosmetic".
  - Every scan is completed. LS0 is a deterministic function of the data, and post hoc execution is allowed.
- **Geometry.**
  - K = min(p, ⌊n/2⌋) and Φ(S) := |S Δ S₀|.
  - Lat(S°) := {U′ ∪ P′ : U° ⊆ U′ ⊆ S₀, P′ ⊆ P°} for S° = U° ∪ P°.
  - A progress neighbour of S is a flip or swap neighbour T with Φ(T) < Φ(S).
  - Δ(T) := ‖(I − P_T)μ‖²/(n−1).
- **Terminal boundary.**
  - 𝔉_T is the σ-field up to the end of the stage-T resampling. After it come H′ = L + 5 rounds at φ = 1, with no
    resampling between them.
  - X_{r,i} denotes the state of particle i of island r at 𝔉_T.
- **Repair certificate and β_H.** As in v2 ([CON] §2):
  - β_H(x) := min{1, P(Bin(H, c_*⁺(x)) < v(x)) + H·η(x)};
  - β_H(S₀) := 0;
  - a certificate requires s₀ + a(x) ≤ K.

### I.B Hypotheses

**Operational (all routes).**
- EX-A, EX-S, CAL: declared idealisations.
- **SR** (IMPL): both Gibbs configurations and every proposal are scored. HQ's code reading is in `SR_AUDIT.md`;
  W5-LOCKBOOK's AUDIT is the same family.
- **GUARD** (IMPL): (G1) the resource guard reads only the clock, consumes no random number and changes no setting; (G2)
  a run that no guard check stops performs exactly the R̄ (R̄⁺) computation. Hence, on 𝒢ᶜ, the outputs equal R̄'s
  (Lemma RO). An independent code check is still outstanding (v2 escalation 3).
- **OP-LS0** (routes using LS0): LS0 is executed, with its centre emitted and its scans completed, on every fit counted as
  output. Post hoc execution is allowed, and a stopped LS0 counts in U.

**Posterior (all routes).** (P): δ₁ := 1 − π(S₀) → 0 in P₀-probability on a triangular array R1 (s₀ fixed,
p_n ≤ n^A). Sufficient conditions:
- locked T03 (G, R, SE, BM-C or BM-∞);
- or T03♯ as stated in `W6-FIXREV2 · STATEMENTS.md §1.2` (G, R, SE_λ(j₀), SE_w(m♯_n; g₀) with g₀ fixed, BM-∞ or BM(c)).

**Route (a), favourable.** (F): 1 − π₀(S₀) → 0 in probability. Sufficient: (F1), (F2) or (F3), exactly as in v2.

**Route (b1), LS0.** There is a deterministic reference S° with Φ(S°) ≤ φ̄ such that the following hold.
- **(M1) ELIG(S°):** P₀(π₀(S°) > ½) → 1.
  - Sufficient: W1-EXP Thm 6 at S° under u < 1.
  - Do not establish (M1) through E3(ii) without q < 1.
- **(M2) POP-LAT(S°, m_n):** for every S ∈ Lat(S°) with Φ(S) ≥ 2, some progress neighbour A_S satisfies
  Δ(B) − Δ(A_S) ≥ m_n for every non-progress neighbour B of S, and for B = S. The margin satisfies
  m_n ≥ M_n√(log n/n) with M_n → ∞.
  - Sufficient on LH: Prop. LH-LAT [W4-T38FULL], fixed margin m₀, or exactly m₀♯ [W5-VMASK R5].
  - Alternative lattice route: W_Lat with LH-PGD [W5-VPGD R6.2–R6.3]. **Not** Theorem W in region form (V7).
- **(M3)** λ_min(R_{S°∪S₀}) ≥ φ₀² > 0 and ‖μ‖²/n ≤ M.
- OP-LS0.

**Route (b1′), D2, no LS0.** x°_n Δ S₀ = {j_n}, data-measurable 𝒟_n, and either of the following.
- **Fixed margins:** b₀ > 1/10, k_D < ∞ and c₀ ∈ (0,1] with
  P₀(π₀(x°_n) ≥ b₀, |𝒟_n| ≤ k_D, Dep_n ≤ 1 − c₀) → 1.
- **General rates:** [CON] §5.

In both cases P(NB′ᶜ) → 0 is also required. Here NB′ is the event that S₀ is among the initial pilot draws, or that the
first-stage ESS is ≥ 0.9H₀, with r* = (11 + 2√10)/9.

**Route (b2), Gibbs path, no LS0.** There is a data-measurable 𝔛_n in which every x ≠ S₀ carries a repair certificate,
and:
- **DELIV(𝔛_n):** P(SMC ∩ 𝒜 ∩ {no final-run particle of any island lies in 𝔛_n at 𝔉_T}) → 0;
- **REP(𝔛_n):** E[1_𝒜 1{N_𝔛 ≥ 1} min_{X_{r,i}∈𝔛_n} β_{L+5}(X_{r,i})] → 0, or the product form under IND-T(a).

The sufficient conditions are as in v2.

### I.C Theorem 5 (T38). Two-regime consistency of the reported HPM

Assume EX-A, EX-S, CAL, SR, GUARD and (P), on R1 with the v3 budgets indexed by n.

**(0) Composition, strict convention, for every n.** For both variants of the method:

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n,   D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).

If D_n → 0, then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0. Recovery with probability → 1 also
requires P(U) → 0, which this theorem does not provide.
- Status: **PROVED**.
- SF: W3-VT38E VERIFIED (v0).
- XF: A-REV1 §7.4 VERIFIED, as the same set argument as locked T21(C1). Lean: `t21_C1` (L-LEAN, Fable fidelity GREEN;
  the Astra fidelity run did not finish).

**(0_H) Composition, HPM convention.**

  P(𝒪_H ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n + D_n^{sl},   D_n^{sl} := P(SMC ∩ 𝒜ᶜ ∩ {S₀ ∉ 𝒮_cal ∪ 𝒮_LS0}).

Status: PROVED (v2, "new, unreviewed").

**(a) Favourable regime.** Under (F), D_n → 0 for both variants. Under the HPM convention, the term
D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ) must be added, and nothing controls it.
- Status: **PROVED-UNDER (F)**.
- Inputs: locked T11(iii); locked T22(iii) with EXP′ (W1-EXP Thm 1; SF VERIFIED by W3-VEXP; XF VERIFIED* by A-REV2);
  W1-EXP Thms 2 and 6.
- The ORTH joint family stays a **PROOF SKETCH** (⚑ CONFLICT III.6).
- Study-like designs S3/S4/S6: `W5-FAVIID · Cor. C3`, author only. Its REPORT still has placeholders.

**(b) Masked regime** (π₀(S₀) → 0 allowed). D_n → 0 under any one of the following.
- **(b1) LS0 route; the method.** Assume (M1), (M2), (M3), G and OP-LS0. On these events S̃₀ = S°, and LS0 scores S₀
  within Φ(S°) − 1 moves once ℓ_n ≥ Φ(S°) − 1. Under the HPM convention, D_n^{sl} → 0 as well.
  - Theorem b1: **PROVED-UNDER (M1)–(M3)**.
  - SF: VERIFIED by W4's subagent and by W5-VMASK (row 22).
  - XF: **none** for Theorem b1, Lemma LS-score or Lemma M. A-REV1 VERIFIED only "route (b1), direct ELIG + TD′ + OP".
    A-REV5 is pending.
- **(b1′) D2 route; v3 as run (no LS0).** The potential first stage of the tier-0 pilot scores S₀, and Ŝ⁺ = Ŝ. Under
  the HPM convention D_n^{sl} → 0 as well (v2; ⚑ CONFLICT III.8).
  - Status: **PROVED (implication)** via D2-∞.
  - SF: finite D2 VERIFIED (W3-VT38E).
  - XF: finite D2 and D2-∞ VERIFIED under their uniform hypotheses (A-REV1).
  - Instances: Part I.D, N1 and N2.
- **(b2) Gibbs-path route; v3 as run (no LS0).** Assume DELIV(𝔛_n) and REP(𝔛_n). Under the HPM convention,
  D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ) must be added.
  - Status: **PROVED (implication)**.
  - XF: A-REV1 §7.2 VERIFIED the repaired interface as a conditional implication.
  - **DELIV(𝔛_n) is OPEN in general**. LH candidates are in Part I.D, N3–N5.

**(b1-LH) The explicit family, with LS0 (the headline masked instance).**
- **Family.** LH in exact Gram:
  - X′X = (n−1)Σ_LH and p ≤ n − 1;
  - c ≥ 1 linked pairs with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i});
  - g ≤ B_n < 2g eventually;
  - fixed nonzero coefficients.
- **Reference.** S° = S₀ ∖ M, with M the masked hubs.
- **What holds.** (P), (M1), (M2) with a fixed margin m₀ > 0 (valid; sharp for homogeneous pairs; exact margin m₀♯), and
  (M3) all hold. π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞, or when c = 1 and
  p/(√n log²n) → ∞.
- **Conclusion.** With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no statistical hypothesis left open.
- **Status: PROVED** (candidate).
- **SF:**
  - inputs VERIFIED by W3-VEXP (W1-EXP Thm 5);
  - LS-score, Lemma M, Theorem b1 and LH-LAT VERIFIED by W5-VMASK, which also checked that the actual v3 partition equals
    the groups (90/90);
  - Cor. GU-LH (W7-SEP) re-proves the search step: every C ⊆ R reaches, scores and certifies S₀ (PROVED, candidate;
    uses Lemma M).
- **XF: none** (A-REV5 pending).
- **Variant covered:** the method (with LS0).

**(b1-LH-iid) The p ≫ n family, with LS0. Not in the headline until its XF GAP is resolved.**
- **Family.** LH-iid of W3-PXN §0: iid Gaussian rows with LH correlation, c ≥ 1, 0 < |ψ_i| < ρ, g ≤ B_n < 2g, and
  n^a ≤ p ≤ n^A with 1 ≤ a ≤ A.
- **Conclusion.** With LS0 and OP-LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 for every fixed c.
- **Status: PROVED** (candidate).
- **SF:** VERIFIED line by line by W5-VMASK, with cosmetic repairs:
  - R2: the U1 constant;
  - R3: r*;
  - R4: the (L)-failure labelling;
  - R7: the "+1" in the cost.
- **XF: GAP** (A-REV3):
  - P6: Lemma Λ(a) calls Tr(c) beyond its stated range;
  - P7: D2(d) only a sketch, and a Beta shape off by ½;
  - the joint LS0 route: "finish P6 bookkeeping".
- A-REV3 did not read W5-VMASK, and no counterexample to the lattice conclusion exists (⚑ CONFLICT III.4).
- Partition input: W7-PART Theorem B / Cor. B can replace P1's cited concentration lemma (PROVED, candidate, author
  only).

**(c) Cost.** The number of score evaluations is bounded deterministically by T32(i)'s ceiling plus
1 + (ℓ+1)·max_{k≤K}[p + k(p−k)] for LS0. Under the v3 budgets this is
O((n+p)(p+B)log²(n+p) + p²log²(n+p)).
- **Status: PROVED-UNDER T32(i)**, where T32(i) is **PROVED** (W5-LOCKBOOK) and re-checked by W7-SEC (SF). There is no
  XF check (⚑ CONFLICT III.1).
- Without EX-A, add the W7-SEC fp-pilot addendum: at most T_e + 1 pilot stages.
- The LS0 term is PROVED (E3′; A-REV1 VERIFIED the scan budget "with accounting clarification").
- At p = 1,000 the LS0 term is about 1.7·10⁵ scores. Measured: median 0.17–0.37 s per fit, under 0.1% of a production
  fit (O-LS0 §1 item 5).

### I.D Candidate no-LS0 masked statements (pending A-REV7; none is part of Theorem 5 as stated)

These candidates would make Theorem 5(b) a theorem about **v3 as run**, which is what F-REFEREE's main objection (M2)
asks for. Each status is the author's word. None has an XF review. They are not merged into I.C, because merging them
would claim a closure that no second family has checked.

| # | Statement (short) | Family and range | Route of I.C | Status (author) | SF | Soft spot | Source |
|---|---|---|---|---|---|---|---|
| N1 | **Cor. D2-LH**: P(S₀ ∉ 𝒮_cal) = O(√n/p) + o(1) → 0, hence (0) for the original Ŝ | LH exact Gram, c = 1, p/√n → ∞ (with p ≤ n − 1) | (b1′) | "PROVED (given [D2], [E-T1], [E-L4], [E-T5d])"; Theorem NB′-LH PROVED (crux: Lemma OF) | none (author only) | single run; c ≥ 2 not covered | `W5-B2ENV · REPORT.md §2`, `PROOF.md §2.3` |
| N2 | **Thm 5(b1′) on LH-iid, c = 1**: P(S₀ ∉ 𝒮_cal) → 0 | LH-iid, c = 1 | (b1′) | PROVED (candidate). D2-a, b, c are W3-PXN's, SF VERIFIED; D2-d is W5-VMASK R1, "unverified: a single run" | D2-a/b/c: W5-VMASK | XF: A-REV3 rated W3-PXN P7 GAP, without seeing R1 | `W5-VMASK · REPORT.md §3`, `REPAIRS.md R1` |
| N3 | **Theorem B2-LH**: P(S₀ ∉ 𝒮 \| 𝓒) ≤ Nπ₀(𝒩ᶜ) + NT_ea_n + (1 − c₀ + o(1))^N → 0, for every c, any grid | LH exact Gram, every c ≥ 1 | (b2) (DELIV by Prop. CONF; repair by Lemma R1, an order event) | "PROVED under STAB-LH" | none; the author asks for an XF check of CONF and R1 | STAB-LH is a finite numerical premise. It **fails** at (ρ, ψ) = (0.85, 0.5) for every g tested and in config B, and holds in 38/46 c = 2 settings | `W5-B2ENV · REPORT.md §2, §6` |
| N4 | **Theorem BG3** (locked start set + terminal downhill) with **Prop. LH-lock**: P(S₀ ∉ 𝒮) → 0 from the final run alone | LH exact Gram, **p fixed**, every fixed c | (b2)-type; final run alone | BG3 PROVED (deterministic given (L1), (L2)); LH-lock **PROOF SKETCH** (the γ₁ gaps C1–C3 are checked by exhaustive enumeration for two designs only); the composite is therefore a PROOF SKETCH | none | the LH-lock sketch; p → ∞ CONJECTURE | `O-BGIBBS · REPORT.md §2, §3.7` |
| N5 | **Theorem F1** (closed-class delivery) with **Theorem F2** (LH): DELIV(W(S°)) with the whole population eligible | LH exact Gram, p ≤ (1 − c₀)n, under PK and DOM | (b2), DELIV only | F1 PROVED; F2 PROOF SKETCH (structure PROVED); REP on W(S°) PROOF SKETCH (CONJECTURE 4.3) | none | DOM failed marginally (+4.7 nats) in one LH20 replicate at n = 1,600; REP unfinished | `F-SHARE · REPORT.md §2` |
| N6 | **Prop. GU / Cor. GU-LH**: from every C ⊆ R the production search reaches, scores and certifies S₀ | exact Gram, isolated R (Σ_{R,Rᶜ} = 0), LH | (b1) re-proof (with LS0). A no-LS0 use, via the final local search from Ŝ_pre when Ŝ_pre ⊆ R, is a **CONJECTURE** | PROVED (candidate); uses Lemma M (SF only) | none | as a no-LS0 route it needs a start already inside R, which is unproved | `W7-SEP · REPORT.md §2`, `PROOF.md §4.2`, §7 |

Related, not listed as routes:
- O-BGIBBS BG1 / Prop. LH: PROOF SKETCH, every fixed c, pilot only.
- W5-B2ENV Prop. M-LH: PROVED, author only. Its standing after A-REV3's ERROR on W4-SHARE M(b) is unchecked
  (⚑ CONFLICT III.3).
- O-MIX Theorem B3 is a *start change* (B-merge), not "no method change". It is PROVED-UNDER and not adopted.

**What A-REV7 must decide** (W8-SYNTH §8 task 1):
- (a) D2-LH for c = 1;
- (b) whether Prop. M-LH survives A-REV3's M(b) ERROR;
- (c) BG3 as a deterministic statement, and LH-lock's γ₁ gaps;
- (d) B2-LH's dependence on STAB-LH.

If at least one of N1–N5 is VERIFIED, F-REFEREE R1 and W8-SYNTH's Decision 1 apply: make the no-LS0 LH theorem the
headline, with LS0 as a remark. Until then the headline is (b1-LH), with LS0 (Part IV, D2).

### I.E Not claimed

- P(U) → 0, or any law of 𝒢 or of calibration failure.
- Under the HPM convention: any control of P(SMC ∩ 𝒜ᶜ).
- Evidence or PIP accuracy in the masked regime. F-MASKPIP M1–M3 are one-sided only; DELIV-POP is OPEN.
- Any statement conditional on completion or on diagnostics.
- Comparative superiority over other methods.
- Finite-n error rates at n = 200, or any quantitative statement at the study size (I.F).
- A masked p ≫ n theorem: (b1-LH-iid) carries an XF GAP.
- Masked-regime consistency of **v3 as run** (no LS0) on an explicit family: **candidates on LH, pending A-REV7**
  (I.D). Not OPEN, not closed.
- DELIV(𝔛_n) for any family other than LH: OPEN.
- **That tempering, or the sampler, is necessary for discovery.** W7-SEP refutes this on LH (I.F).

### I.F Remarks for the paper text

1. **Execution.** Every discovery statement is about R̄ (R̄⁺). GUARD transfers it to the reported output on 𝒢ᶜ, and
   everything else is in U. Conditioning on observed completion is never used, and it is not a valid repair (Lemma RO(5);
   W2-BOOK §0.3).
2. **Regime discipline.** (F) and the masked instances are never combined on one sequence. On LH, VIS fails at S₀
   (W1-EXP Thm 5(c)). The ψ ≥ ρ boundary is a *transition* to the favourable regime, not a cliff. Past it the masking
   disappears (W5-VMASK §1 item 5).
3. **Delivery is part of the theorem.**
   - In (b1), delivery is S̃₀ = S° plus the lattice condition.
   - In (b1′), it is the pilot ESS rule (Lemma S′, used only for f > 1 − e).
   - In (b2), it is DELIV(𝔛_n), which is OPEN in general. COUNTEREXAMPLE C1 shows that start mass, bridge mass and zero
     exits do not imply it.
4. **H24 is not used.** Its asymptotic input fails along the explicit sequence CE1-narrow. This is not claimed for every
   correlated design, and "H24 is false" must not be cited.
5. **Why LS0** (restored from v1; citation corrected, V13).
   - Without LS0, the final local search starts at the running HPM, so it delivers S₀ only through Lemma 0(b′)'s
     inclusion (`W6-FIXREV2 · STATEMENTS.md`, with the three-way Prop. F).
   - The natural eligibility condition fails with probability → 1 under omission masking (W1-T38E Prop. E1: deterministic
     part PROVED, margin PROOF SKETCH).
   - LS0 turns eligibility into a deterministic property of the start law, at a cost under 0.1% of a fit.
   - **At n = 200, LS0 changes nothing.** O-LS0 found 0/2,394 HPM changes and recovery identical in every cell (1,119/1,200
     at c = 1 and 710/1,200 at c = 0.5). This was impossible to improve on, because production has 0 search misses.
6. **What the masked half shows: moving off the start is needed, not tempering** (spine correction, `theory/E-SPINE`).
   - In the masked regime, iid start draws provably fail below the sharp budget Q* = p^c n^{c/2}, and a one-shot
     importance correction fails too (T27; W7-SEP Theorem SEP(A)/(B): PROVED, candidate).
   - Moving off the start fixes this. On LH, one greedy production search from the start mode reaches, scores and
     certifies S₀ (W7-SEP Prop. GU / Cor. GU-LH: PROVED, candidate). That is (b1-LH).
   - In the frozen setting there is **no separation between the tempering bridge and a single greedy search** from the
     start mode, and no super-polynomial separation at all (W7-SEP §1 item 4).
   - The theorem therefore does not say that tempering is needed. v3's bridge Gibbs moves, terminal rounds and local
     search (including LS0) are each a sufficient way to move off the start. The no-LS0 candidates N1–N5 are the bridge
     and terminal routes.
   - The bridge's distinct contribution is calibrated Ẑ and PIPs (Thm 6, Prop 2) and the HPM ledger.
7. **n = 200 disclosure** (W8-SYNTH Decision 3 draft; numbers corrected in `E-SPINE · AMENDMENTS_20261102.md §2.3`). At
   the study size (n = 200, p ∈ {500, 1000}, s₀ = 14) the theorem describes mechanism, not the reported numbers.
   - Of 2,400 fits, 6 stopped on a resource limit and count as failures, 1,829 recovered S₀ exactly, and 565 were
     posterior misses: S₀ was scored, but a scored competitor had higher posterior. There were 0 search misses, and the
     final local search never moved (S-ELS).
   - The (b1) premises mostly fail there (O-LS0 §1 item 6):
     - (M1) holds in 18/2,400 fits;
     - (M2) holds without margin in 17/168 (c = 1) and 1/129 (c = 0.5) checked fits;
     - (M3) holds everywhere;
     - the cap ℓ ≥ Φ(S̃₀) − 1 holds in 1,968/2,400 fits.
   - Lemma LS-score's implication held in all 18 fits that met its premise.
   - The start is masked by *dilution*, not by T27/LH cancellation (O-DILUTE §7; W3-PXN Prop. W).
   - T03♯'s thresholds hold only from n ≈ 2·10⁶, and its beta-min constant exceeds the executed signals by at least 43×.
   - The statement bounds P(reported and wrong), not P(wrong | reported).

**Why it matters (paragraph for the paper).** Theorem 5 is the paper's guarantee about the model the method actually
reports. The reported HPM is the best model the run ever scored. So it is right whenever two things happen: the posterior
ranks the truth first (Theorem 1), and the run scores the truth at least once. Part (0) turns this into one inequality
that holds at every n. In the favourable regime the start draws alone score the truth (part (a)). In the masked regime
they provably cannot at any budget below p^c n^{c/2}. So the run must **move off its start**, and part (b) shows that
moving off the start is enough. On the linked-hub family, where every premise is proved, one deterministic local search
from the exact start mode scores the truth, and the reported model is consistent (b1-LH). The theorem does not say that
tempering is what finds the truth: on this family a single greedy search does it, and the bridge's own role is
calibrated evidence and inclusion probabilities. Whether the unmodified method's own Gibbs moves also suffice is the
content of the candidate routes N1–N5, which are pending cross-family review.

---

## Part II. Dependency map (inputs → sources → status → reviews)

Labels: PROVED-LOCKED (in `LOCKED_PROOFS.md`); PROVED (campaign candidate); PROVED-UNDER [X]; PROOF SKETCH;
CONJECTURE; OPEN; IMPL; IDEAL. "SF" is the same-family verdict and "XF" the cross-family verdict. **Bold** marks what
changed from v2. The proposed paper label is in [ ].

### II.1 Composition and execution

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| C1 | strict maximiser on {π(S₀) > ½} ∩ {S₀ scored}; Markov | locked T21(C1); T38_PROOF §1 | PROVED-LOCKED / PROVED | W3-VT38E VERIFIED | A-REV1 §7.4 VERIFIED; **Lean `t21_C1` GREEN (Fable fidelity; Astra fidelity incomplete)** |
| RO | Lemma RO | W2-BOOK §0.2 | PROVED | **W5-LOCKBOOK VERIFIED** (𝒪 = 𝒢ᶜ ∩ 𝒪̄ checked in code) | **A-REV4 BOOK_CHECK VERIFIED*** (for statistics extended by zero off their availability events; no equality conditional on completion); **GUARD literal claim ERROR** (repair PENDING: restrict to statistical fields; W5-LOCKBOOK convention 𝒢 ⊆ U) |
| GUARD | (G1), (G2) | W2-BOOK §0.1; W5-LOCKBOOK AUDIT G1 | IMPL | code reading, same family | needs an independent code check |
| HPM conv. | D_n^{sl} | v2 T38_PROOF §1.3 | PROVED | none | none (A-REV5 pending) |
| P | δ₁ → 0 | locked T03(i); **T03♯ statement of record W6-FIXREV2 §1.2** | PROVED-LOCKED / PROVED | W2-VT03R VERIFIED | **A-REV2 VERIFIED under exactly its hypotheses** |
| SR | scored set | `SR_AUDIT.md` (HQ code reading) | IMPL | HQ; W5-LOCKBOOK AUDIT | none |

### II.2 Route (a)

Unchanged from v1 II.2 (a1–a8). Two additions:
- **(a) on S3/S4/S6: `W5-FAVIID · Cor. C3`, PROVED, author only, REPORT unfinished** (FAVIID-CLOSE is W8-SYNTH task 9);
- a6, the ORTH joint family: PROOF SKETCH (⚑ III.6).

### II.3 Route (b1) and the LH instances

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| b1.1 | E3′(i): π₀(x°) > ½ ⇒ S̃₀ = x°; centre emitted; cost 1 + (ℓ+1)max_k[p + k(p−k)] | [CON] §6 | PROVED | W3-VT38E; W5-VMASK rows 25, 26 (start-mode DP = `v3_start.h::start_mode`) | A-REV1: E3 core VERIFIED; (ii) ERROR as printed, not used |
| b1.2 | Lemma LS-score [**Lemma LS**] | W4-T38FULL §3.1 | PROVED | W4 subagent; **W5-VMASK row 20 VERIFIED** | none |
| b1.4 | Lemma M [**Lemma SC**] | W4-T38FULL §3.2 | PROVED | W4 subagent; **W5-VMASK row 21 VERIFIED**; W6-FIXREV1 recheck | none |
| b1.5 | Theorem b1 | W4-T38FULL §3.3 | PROVED-UNDER (M1)–(M3) | **W5-VMASK row 22 VERIFIED** | none (A-REV1 verified only the direct ELIG + TD′ + OP route) |
| b1.6 | (M1) from W1-EXP Thm 6 | W1-EXP | PROVED | W3-VEXP | none for Thm 6 itself (A-REV2 rated EXP′ VERIFIED* and Thms 3, 4 VERIFIED) |
| b1.7 | LH: ELIG, masking, π(S₀) → 1 | W1-EXP Thm 5 | PROVED | W3-VEXP | **none: the LH exact-Gram theorem has no XF review** |
| b1.8 | Prop. LH-LAT | W4-T38FULL §3.4 | PROVED; **"sharp" withdrawn; m₀♯ exact** | **W5-VMASK rows 23 (VERIFIED), 23′ (GAP: overstatement, repaired R5)** | none |
| **b1.8′** | **W_Lat + LH-PGD** (alternative to b1.8; certification and (L)) | **W5-VPGD REPAIRS R6.2, R6.3** | **PROVED (candidate)** | author = verifier run (W5-VPGD) | none |
| **b1.8″** | **Prop. GU / Cor. GU-LH** (alternative search step) | **W7-SEP PROOF §4.2** | **PROVED (candidate)** | none | none (A-REV7 pending) |
| b1.9 | LH-iid P1–P8 | W3-PXN | PROVED | **W5-VMASK VERIFIED (rows 1–19)** | **A-REV3: P1, P2, Lemma B, P3, P4, P5, P8 VERIFIED; P6 GAP; P7 GAP; joint LS0 route GAP** |
| **b1.9′** | **partition = groups for iid Gaussian designs** | **W7-PART Theorem B, Cor. B** | **PROVED (candidate)** | none | none (A-REV6 pending) |
| b1.11 | TD(d,0) false for d ≥ 1 | W1-T37R Prop 1; W3-VT38E V1 | PROVED (negative) | VERIFIED | — |
| b1.13 | `emit_centre = true` | W3-VT38E §4; W5-LOCKBOOK IMPL-EMIT | IMPL | — | A-REV1 §6 (the centre must be offered to the HPM) |
| **b1.14** | **LS0 on the study fits** | **O-LS0 REPORT** | **data (not a theorem)**: 0/2,394 HPM changes; job B reproduced job A exactly | — | — |

### II.4 Route (b1′)

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| d1 | Lemma S′ [**Lemma ESS**] | [CON] §4 | PROVED | — | A-REV1: inequality VERIFIED; attainment ERROR, corrected |
| d2 | Lemma A | W1-T38E §1 | PROVED | VERIFIED | — |
| d3 | finite D2, NB′, r* | W1-T38E §4 + W3-VT38E §3.1 | PROVED | VERIFIED | A-REV1 VERIFIED (finite uninterrupted pilot) |
| d3′ | D2-∞ with rate margins | [CON] §5 | PROVED (implication) | — | A-REV1 §7.1 repair |
| d4 | masked instance | **N1 (W5-B2ENV D2-LH, LH exact Gram, c = 1); N2 (W3-PXN P7 + W5-VMASK R1, LH-iid, c = 1)**; c ≥ 2 OPEN | **N1: PROVED (given cited candidates), author only. N2: D2-a, b, c PROVED and SF VERIFIED; D2-d PROVED, single run** | W5-VMASK (N2, D2-a/b/c) | **A-REV3: W3-PXN P7 GAP (predates R1)**; A-REV7 pending |

### II.5 Route (b2)

v2 rows g1–g8 are unchanged. One row changes and four are added:

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| g4 | DELIV(𝔛_n) | W1-T38E D3; **on LH: N3 CONF, N4 lock, N5 F1/F2** | **OPEN in general**; on LH, candidates: CONF PROVED under STAB-LH; LH-lock PROOF SKETCH; F2 PROOF SKETCH | none | C1 COUNTEREXAMPLE VERIFIED (W3-VT38E); A-REV7 pending |
| **g4′** | **W4-SHARE D4, D5** (envelope delivery) | **W4-SHARE** | **PROVED** | **W5-B2ENV VERIFIED** | **A-REV3 VERIFIED**; the §7 exit-loss simplification is ERROR (PENDING) |
| **g4″** | **lattice-indicator envelope** | **W5-B2ENV PROOF §4.6** | **PROOF SKETCH (negative: it cannot work at any budget)** | none | none |
| **g5′** | **REP on LH by an order event (Lemma R1)** | **W5-B2ENV §4.4** | **PROVED under the deletion part of STAB-LH** | none | none |
| **g5″** | **REP on W(S°)** | **F-SHARE §4** | **PROOF SKETCH (CONJECTURE 4.3)** | none | none |

### II.6 Cost

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| k1 | T32(i) ceiling | **W5-LOCKBOOK PROOF §T32** | **PROVED** (v2: CONJECTURE, stale; ⚑ III.1) | **W7-SEC re-count: "no error in the count"** | none |
| k1′ | **fp-pilot addendum (≤ T_e + 1 stages without EX-A)** | **W7-SEC** | **PROVED** | author = W7-SEC | none |
| k2 | LS0 term | [CON] §6; W5-VMASK R7 | PROVED | W5-VMASK | A-REV1 §6 ("add one initial centre evaluation") |

### II.7 Method-change record

| Change | Status | Bearing on Theorem 5 |
|---|---|---|
| **LS0** | **part of the method** (approval in effect: O-LS0 0/2,394; SR_AUDIT presentation "a final local search from both the best-scored model and the start mode") | needed for (b1), (b1-LH) and (b1-LH-iid). **Implementation obligations**: emit the centre first; HPM tie rule for argmax π₀; label mechanisms; an integrated (in-engine) test fit is still to run (O-LS0 §6 item 4) |
| common-σ² start | **rejected** (O-DILUTE §5, F-SIGMA Thm S6; E-SPINE §2.2) | none; F-SIGMA Thm S4 (route (a) under common σ̂², BO) is "vacuous as an improvement" |
| B-merge start (O-MIX) | not adopted; needs a pilot | O-MIX Thm B3 would give (b) on LH through route (a) without LS0 (PROVED-UNDER) |
| residualised tables | not adopted; F-SIGMA Step 0 first (W8-SYNTH task 8) | none proved |

---

## Part III. Conflicts (⚑)

| # | Item | Position A | Position B | Recorded as | What settles it |
|---|---|---|---|---|---|
| III.1 | T32(i), hence the status of (c) | CONJECTURE: v2 dependency k1; W7-SEP input I11 | PROVED: W5-LOCKBOOK item 4; W7-SEC re-count, no error; registry | PROVED (author W5-LOCKBOOK), SF only. v2 and W7-SEP are stale, not dissenting: neither re-examined the proof | an XF check of the count (cheap) |
| III.2 | Is there a masked theorem without LS0? | "OPEN": v1 II.9; v2 Not claimed | candidates N1–N6 (W5-B2ENV, W5-VMASK, O-BGIBBS, F-SHARE, W7-SEP) | "candidates on LH, pending A-REV7" | A-REV7 |
| III.3 | W4-SHARE Prop. M(b), and W5-B2ENV Prop. M-LH | SF: W5-B2ENV, sketch argument correct; M-LH PROVED on LH | XF: A-REV3 ERROR on M(b) (quadratic equality used as an expansion; vanishing crossing temperature false under BM-C) | M(b) ERROR; M-LH PROVED (author only), its exposure unchecked | A-REV7 question (b) |
| III.4 | W3-PXN P6/P7 and the (b1-LH-iid) joint route | SF: W5-VMASK VERIFIED, cosmetic errors only, with R1 closing D2-d | XF: A-REV3 GAP (Tr range, Beta shape, D2(d) sketch) | XF GAP (weaker verdict) | A-REV5 with W5-VMASK's repairs in hand |
| III.5 | LH-LAT "m₀ is sharp" | v1 / W4 subagent: sharp | W5-VMASK: sharp only for homogeneous pairs (108/108), not on 32/94 heterogeneous settings | "valid; sharp when homogeneous; exact m₀♯" | settled (R5) |
| III.6 | ORTH joint family for (a) + Thm 6 | v1: "no open statistical input" | W2-T26 Prop. C PROOF SKETCH; A-REV4 GAP | PROOF SKETCH | a proof of W2-T26 Prop. C |
| III.7 | Output convention | W2-BOOK and A-REV1 use 𝒪_H | v1 and v3 use strict 𝒪 | both stated; strict as default | HQ and Felipe (Part IV, D1) |
| III.8 | (b1′) under the HPM convention: is D_n^{sl} → 0 automatic? | v2: yes, "because 𝒮_cal contains the pilot" | A-REV1 §7.4: for the pilot route, "add the probability of usable no-score output when that stage does not execute" | v2's sentence kept, flagged unreviewed | A-REV5 |
| III.9 | Theorem W region form versus lattice form on masked LH | F-REFINE ARCHITECTURE/CARDS: Theorem W is "the general sufficient condition for (M2)" | W5-VPGD R6.1: the region form fails with an exact tie on LH for c ≥ 2 | cite W_Lat | settled (same family) |
| III.10 | Lemma 0(b) "every unrepaired centre is a posterior miss" | W1-T37R: "0/541 forced by monotonicity" | W3-VT37R, A-REV2: ERROR as a logical claim. S-ELS: true on the study data (all 541 forced) | false in general; true on the study data; cite Lemma 0(b′) + Prop. F | W3-VT37R's script rerun on PROD-H (W8-SYNTH task 3) |
| III.11 | W7-SEP's citation of the no-LS0 route | W7-SEP SEP(D): "BG1 (PROOF SKETCH)" only | O-BGIBBS's main result is BG3 (PROVED) + LH-lock (PROOF SKETCH) | cite both | — |
| III.12 | "9 ≤ g ≤ 16" in the LH-iid statement | W3-PXN, W5-VMASK §3 | W7-PART: false at n < 256 (B = 14 at n = 200); the condition is g ≤ B_n < 2g | written as "g ≤ B_n < 2g eventually" | settled |

---

## Part IV. Decisions this statement depends on

| # | Decision | State | Effect on this statement |
|---|---|---|---|
| D1 | Output convention (strict 𝒪 versus 𝒪_H) | **open** (HQ and Felipe). W8-SYNTH recommends strict, since it needs no extra term | (0) is the default; (0_H) is kept as an alternative |
| D2 | Headline: (b1-LH) with LS0, or a no-LS0 LH theorem | **conditional**. SR_AUDIT records "T38 + LS0 as the main theorem and the no-LS0 version as a conditional remark". W8-SYNTH recommends switching to no-LS0 if A-REV7 verifies one of N1–N5 | headline = (b1-LH) until A-REV7 reports |
| D3 | LS0 | **taken**: part of the method (O-LS0 passed) | V1 |
| D4 | Spine wording | **taken**: "moving off the start is needed" (E-SPINE) | Remark 6, "Why it matters" |
| D5 | Common-σ² start | **taken**: rejected | II.7 |
| D6 | Whether to quote a "favourable from n ≈ …" threshold | **open**; W8-SYNTH and E-SPINE: omit it, or attribute it to W5-FAVIID | not quoted here |
