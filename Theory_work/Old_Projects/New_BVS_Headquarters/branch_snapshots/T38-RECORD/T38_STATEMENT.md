# T38 (paper Theorem 5): statement of record, v3

Run T38-RECORD, 2026-11-02, branch `theory/T38-RECORD`. Spec: `theory/W8-SYNTH · SYNTHESIS.md §8 task 6`.

**What this is.** One statement of record for Theorem 5. It merges every version and every repair that has landed, and
every cross-family verdict up to A-REV9. It contains **no new mathematics**: every clause is copied from a source, with
the source's status word. Two wording repairs are taken verbatim from cross-family referees and are marked [ref. repair].
No status is upgraded. Where sources disagree, the disagreement is marked **⚑** and both sides are given (Part III).

**What it supersedes.**

| Version | Where | Head | Reviewed by |
|---|---|---|---|
| v0 | `theory/W1-T38E · PROOF.md §7 · T38(b)-R` | 436a712 | W3-VT38E (SF): VERIFIED. A-REV1 (XF): whole statement GAP; composition and route (b1) VERIFIED; A-REV1 §7's repaired formulation VERIFIED as a conditional implication |
| v1 | `theory/W4-T38FULL · T38_STATEMENT.md` | a0f9cb5 | W4's own subagent and W5-VMASK (SF). XF: A-REV3 (W3-PXN joint route only), A-REV8 (§3 lemmas) |
| v2 | `theory/W6-FIXREV1 · T38_STATEMENT.md` | a7833f3 | **A-REV5 (XF)**: interfaces (0), (0_H), b1, b1′, b2 VERIFIED; "T38 statement" overall ERROR, from one clause (V18). **A-REV8 (XF)**: v2 versus A-REV1 §7 VERIFIED |
| **v3** | this file | — | nobody; no new mathematics |

The proofs stay where they are:
- `W6-FIXREV1 · T38_PROOF.md` for (0), (0_H), (a), (b1), (b1′), (b2) and (c);
- `W4-T38FULL · T38_PROOF.md §3` for Lemma LS-score, Lemma M, Theorem b1 and Prop. LH-LAT;
- `W3-PXN · PROOF.md` with `W5-VMASK · REPAIRS.md` for (b1-LH-iid);
- `W5-B2ENV · PROOF.md §2, §4` for (b1′-LH) and (b2-LH);
- `A-REV7 · REVIEW.md §3–§4` for the Astra-authored completions;
- the candidates' own PROOF files for Part I.D.

**Status words** follow `theory_campaign/PROTOCOL.md`. "SF" means a same-family check (a Claude run checking a Claude
run). "XF" means a cross-family check (Astra, A-REV1 to A-REV9). Every PROVED here is a **candidate**: nothing is adopted
or locked.

**Cross-family reviews that landed during this run** (all re-fetched at the end):

| Review | Head | Scope | Bearing on Theorem 5 |
|---|---|---|---|
| A-REV5 | 189770c | W6-FIXREV1/2 repairs, W4-T38FULL, W3-PXN, W3-PGD | v2's interfaces VERIFIED. One ERROR: the (b1-LH) iid-budget clause for c = 2. GAPs: the D3 surrogate's conditioning; (c) must keep its T32(i) qualification |
| A-REV6 | 02d6a4a | post-A-REV4 repairs (W3-PXN, W4-SHARE, W2-T26, W2-BOOK/W5-LOCKBOOK, W7-PART, F-SHARE, O-BGIBBS, …) | P6/P7 GAP retained; P1 VERIFIED via W7-PART B; M-LH VERIFIED; T32(c) rate GAP (log³); GUARD only in statistical scope |
| A-REV7 | 70eadf3 | **no-LS0 masked theorem on LH** | B2-LH VERIFIED under STAB-LH, with an Astra-authored analytic STAB certificate and an explicit growing-p subfamily. D2-LH VERIFIED qualitatively. BG3 VERIFIED. LH-lock VERIFIED as a conditional fixed-p implication; general locking ERROR. F1 VERIFIED, F2 GAP. GU VERIFIED as greedy repair, GAP as a no-LS0 route |
| A-REV8 | 6417192 | **the LS0 route** | Thm b1, LS-score, Lemma M, LH-LAT and exact-Gram (b1-LH) VERIFIED. ERRORs: the move count at C₀ = S₀, and GUARD's literal wording. The c = 2 clause is a GAP. W3-PXN P6/P7 GAP retained |
| A-REV9 | bbadda3 | certificates, masked outputs, dilution, separation, stages | W7-SEP SEP(A)/(B) VERIFIED; GU deferred (GAP in that review); W7-SEC/T32(i) deferred |

---

## Part 0. Change log

### 0.1 v2 (W6-FIXREV1) → v3

| # | Where in v2 | Change in v3 | Source | Effect on status |
|---|---|---|---|---|
| V1 | Objects, "LS0" | LS0 is **part of the method**, not a tweak. Felipe approved it on 2026-11-02, conditional on O-LS0's data check, which passed: LS0 changed the reported HPM in **0 of 2,394** completed fits. The reported model is Ŝ⁺. "v3 as run" (no LS0) is kept as a named variant, because the study's fits were produced without LS0 and the no-LS0 parts cover it. | `theory/campaign · HQ/SR_AUDIT.md`; `O-LS0 · REPORT.md §1, §6`; `E-SPINE · AMENDMENTS_20261102.md §2.1` | none (decision) |
| V2 | Output events | Both conventions are kept, with strict 𝒪 as the default. The choice is an open decision (IV, D1). | v2 escalation 1; `W8-SYNTH §4.12` | none |
| V3 | (c), dependency k1 | T32(i) is cited as PROVED (W5-LOCKBOOK) and re-counted by W7-SEC (SF). The fp-pilot addendum is attached. v2's "CONJECTURE" predates W5-LOCKBOOK. A-REV5 requires that (c) keep the T32(i) qualification, and v3 does. | `W5-LOCKBOOK · REPORT.md` item 4; `W7-SEC · REPORT.md`; A-REV5 | ⚑ III.1; (c) stays PROVED-UNDER T32(i) |
| V4 | (b1-LH), LH-LAT | "m₀ … sharp" becomes "valid lower bound; sharp for homogeneous pairs; exact margin m₀♯". | `W5-VMASK · REPAIRS.md R5`; A-REV8 | none (overstatement withdrawn) |
| V5 | Dependency map b1.2–b1.8 | Review columns record W5-VMASK (SF) and **A-REV8 (XF)**, which VERIFIED LS-score, Lemma M, Theorem b1 and LH-LAT. | `W5-VMASK §2`; A-REV8 verdict table | verification recorded; statuses unchanged |
| V6 | Not claimed: "A masked p ≫ n family (unverified)" | Replaced by part (b1-LH-iid) with its record: PROVED (candidate), SF VERIFIED, **XF GAP** (A-REV3, A-REV6, A-REV8). Not in the headline. | W5-VMASK §3; A-REV3/6/8 | recorded at the weakest verdict |
| V7 | (M2) sufficient conditions | Cite W_Lat with LH-PGD (A-REV8 VERIFIED), not Theorem W in region form (fails on LH for c ≥ 2). | `W5-VPGD · REPAIRS.md R6.1–R6.3`; A-REV8 | none |
| V8 | (b1′) masked instance | v2's "LH c = 1: PROOF SKETCH" is replaced by part **(b1′-LH)**, which is W5-B2ENV Cor. D2-LH. A-REV7 VERIFIED its qualitative consistency; its stated rate is a GAP. The LH-iid instance (W5-VMASK R1) stays a GAP (A-REV6, A-REV8). | `W5-B2ENV · PROOF.md §2.3`; A-REV7 §6 | author status unchanged; XF recorded |
| V9 | (b2) DELIV | DELIV(𝔛_n) stays **OPEN** in general. On LH there is now part **(b2-LH)**, W5-B2ENV Theorem B2-LH: confinement (Prop. CONF) plus repair (Lemma R1), VERIFIED by A-REV7 under STAB-LH. A-REV5's D3-surrogate GAP is recorded; (b2) assumes DELIV directly, which avoids it. | `W5-B2ENV · PROOF.md §4`; A-REV7 §4; A-REV5 | author status PROVED-UNDER STAB-LH, unchanged |
| V10 | Not claimed: "Masked-regime consistency without LS0 on an explicit family (OPEN)" | Out of date. There is now an XF-verified no-LS0 statement on an explicit LH subfamily: (b2-LH) together with A-REV7's analytic STAB certificate, which is Astra-authored and not yet checked by a Claude run. Unrestricted LH is not claimed: general locking is false (A-REV7 §5). | A-REV7 §4, §5; `E-SPINE §2.4` | ⚑ III.2 |
| V11 | Remarks | New Remark 6 and a "Why it matters" paragraph: **moving off the start is needed, not tempering.** | `W7-SEP · REPORT.md §1`; `E-SPINE` dd0ec8a | none |
| V12 | n = 200 remark | Rewritten from S-ELS and O-LS0. A-REV8's reading is attached: O-LS0's (M1)/(M2)/(M3) counts are finite-sample diagnostics, not the asymptotic premises. | S-ELS; O-LS0 §1 item 6; A-REV8 | none |
| V13 | "Why LS0" (v1, dropped in v2) | Restored, citing Lemma 0(b′) and Prop. F, both A-REV5 VERIFIED, instead of W3-VT37R R2 (ERROR). | `W6-FIXREV2 · STATEMENTS.md`; A-REV5 | none |
| V14 | (P) | T03♯ statement of record is `W6-FIXREV2 · STATEMENTS.md §1.2`; its core is A-REV5 VERIFIED, and the onset gloss is excluded. | W6-FIXREV2; A-REV5 | none |
| V15 | Labels | Proposed paper labels are given in [ ]; the full table is in `REGISTRY_v2.md §F`. | `W8-SYNTH §4.15` | none |
| V16 | Lean | L-LEAN is final (head cfa78ed). T21(C1) is sorry-free, with fidelity GREEN from Fable and from Astra (round 1 for T21, round 2 for T37). W8-SYNTH §7's "Astra did not finish" predates this. | `L-LEAN · REPORT.md §1` | none (fidelity is not a status word) |
| V17 | (b1), LS-score | "LS0 scores S₀ within Φ(S°) − 1 moves" becomes "within **max{Φ(S°) − 1, 0}** moves" [ref. repair, A-REV8 E1: the literal bound is negative at C₀ = S₀]. No effect in the masked regime, where c ≥ 1. | A-REV8 | wording only |
| V18 | (b1-LH), last clause | "Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞" becomes "**when n^{1−c/2}p^{−c}log²n → 0** (for c = 2: p/log n → ∞), or c = 1 and p/(√n log²n) → ∞" [ref. repair, A-REV5 and A-REV8]. A-REV5 calls the old clause an ERROR; A-REV8 calls it a GAP. SMC applicability is stated separately, because slowly growing p eventually takes exact enumeration. | A-REV5 §2; A-REV8 G1 | ⚑ III.13; masking and LS0 consistency unaffected |
| V19 | (c) | The displayed order O((n+p)(p+B)log²(n+p) + p²log²(n+p)) carries an XF GAP. A-REV6 found that T32(c) misses the calibration-iteration factor; Astra's candidate bound is O(max(n,p)p log³(n+p) + p²log²(n+p)). **Polynomiality survives.** | A-REV6 BOOK (T32 rows, R5) | the displayed rate is GAP; "polynomial" stands |
| V20 | GUARD | (G2)'s transfer holds for **statistical outputs, scored sets, decisions and status semantics**, not for run diagnostics [ref. repair, A-REV8 E2; also A-REV4 and A-REV6 BOOK R1]. A-REV5 and A-REV8 read `RuntimeGuard::check`: it reads elapsed/operation time, uses no RNG and changes no statistical setting. | A-REV5; A-REV8 E2 | GUARD stays IMPL; its literal wording is ERROR |
| V21 | Candidates (I.D) | Every candidate now carries its A-REV7 (and A-REV9) verdict. Two VERIFIED ones are lifted into I.C as parts (b1′-LH) and (b2-LH), with their author status words unchanged. | A-REV7 §1 | none |

### 0.2 v1 (W4-T38FULL) → v3

Everything in 0.1 applies, together with v2's change log S1–S9 (`W6-FIXREV1 · T38_STATEMENT.md Part 0`). A-REV5 VERIFIED
all of them as interfaces:
- S1: strict versus HPM output convention, with partial returns counted in U;
- S2: GUARD as (G1)/(G2), with STATUS derived from it;
- S3: K = min(p, ⌊n/2⌋);
- S4: the (b1′) rate margins (D2-∞);
- S5: the (b2) eligible set, repair certificates, capped β_H, and 𝔉_T with H′ = L + 5;
- S6: the direct set proof of (0) and its two-sided form;
- S7: the "+1" in the LS0 cost;
- S8: A-REV1's verdicts entered;
- S9: no E3(ii).

Two v1 items beyond S1–S9: v1's (c) used log²n; and v1's "Why LS0" cited W3-VT37R R2, which is corrected in V13. A-REV5
notes that **W6-FIXREV1 explicitly supersedes W4's statement**; cite v2 or v3, never v1's unchanged text.

### 0.3 v0 (W1-T38E T38(b)-R) → v3

v0 is the composition of W1-T38E §7, absorbed by v1 and v2. Its differences from v3:
- no GUARD or R̄ (A-REV1 §7.3);
- no rate margins in (b1′) (A-REV1 §7.1);
- uniform REPAIR on 𝓡_d in (b2) (A-REV1 §7.2);
- E3(ii) without q < 1 (A-REV1 §3.3 ERROR);
- an unrestricted Lemma S attainment claim (A-REV1 ERROR);
- no "+1" in the cost;
- the citation "T11(vii)" instead of locked T21(C1).

### 0.4 What v3 does *not* change

The mathematics of (0), (0_H), (a), (b1), (b1′), (b2), (b1-LH) and (c) is v2's, apart from two referee wording repairs: V17
(a move count) and V18 (a growth condition in one side clause). The parts (b1′-LH) and (b2-LH) are W5-B2ENV's theorems,
copied with their author status.

---

## Part I. The theorem

### I.A Objects

As in v2 (`W6-FIXREV1 · T38_STATEMENT.md Part I`):

- **The method** is v3 **with LS0** (V1). **"v3 as run"** is the same method without LS0. Each part states which
  variant it covers.
- **Potential uninterrupted run.**
  - R̄ is the record the method produces under EX-A without the preflight or the in-run guard (W2-BOOK §0.1).
  - Its status is st̄ ∈ {exact, completed, schedule_limit}. On the SMC branch, {st̄ = completed} = 𝒜, the calibration
    success event.
  - R̄⁺ is R̄ followed by LS0.
- **Actual run.** The status st and the outputs are functions of (R̄, Ξ). 𝒢 := {st = resource_limit}.
- **Output events.**
  - *Strict convention (default):* 𝒪 := {st ∈ {exact, completed}} and U := 𝒪ᶜ. A `schedule_limit`,
    `numerical_failure` or guard-partial return counts as no output.
  - *HPM convention:* 𝒪_H := {an HPM is reported and st ≠ resource_limit}.
  - Bars denote R̄ versions.
- **Scored sets.**
  - 𝒮 is every model scored: tables, initial draws, pilot, calibration, final rounds (both Gibbs configurations and
    rejected proposals) and local-search scans.
  - 𝒮⁺ := 𝒮 ∪ 𝒮_LS0, and Ŝ⁺ is the best model in 𝒮⁺ under the method's total order. For v3 as run, Ŝ⁺ = Ŝ.
  - 𝒮_cal ⊆ 𝒮 is the calibration part.
- **LS0.**
  - One extra production local search (M §6.10), centred at the exact start mode S̃₀ = argmax π₀ (max-plus convolution,
    deterministic tie rule).
  - **Its centre is the first evaluation and is offered to the HPM** (`emit_centre = true`). An un-emitted centre can
    be cached without being offered, so a later emitted cache hit does not repair this (A-REV8).
  - Scans are completed, and post hoc execution is allowed.
- **Geometry.**
  - K = min(p, ⌊n/2⌋) and Φ(S) := |S Δ S₀|.
  - Lat(S°) := {U′ ∪ P′ : U° ⊆ U′ ⊆ S₀, P′ ⊆ P°}.
  - Progress neighbours T of S satisfy Φ(T) < Φ(S).
  - Δ(T) := ‖(I − P_T)μ‖²/(n−1).
- **Terminal boundary.** 𝔉_T is the σ-field up to the end of the stage-T resampling, followed by H′ = L + 5 rounds at
  φ = 1. BG3 counts the L + 4 rounds after the stage-T mutation; both counts are consistent (A-REV7 §2).
- **Repair certificate and β_H** as in v2 ([CON] §2): β_H(x) := min{1, P(Bin(H, c_*⁺(x)) < v(x)) + H·η(x)},
  β_H(S₀) := 0, and s₀ + a(x) ≤ K.
- **LH family** (W1-EXP §4; W5-B2ENV §2):
  - exact Gram X′X = (n−1)Σ_LH with p ≤ n − 1;
  - groups of size g with g ≤ B_n < 2g eventually, and within-group correlations ρ_h;
  - c linked pairs (a_i, b_i) with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i});
  - v visible groups and null groups;
  - fixed coefficients θ_{a_i} = β_i, θ_{b_i} = −ψ_iβ_i, θ_{j_h} = β_h;
  - S° = S₀ ∖ M, with M the masked hubs.

### I.B Hypotheses

**Operational (all parts).**
- EX-A, EX-S, CAL: idealisations.
- **SR** (IMPL): both Gibbs configurations and every proposal are scored.
  - HQ's `SR_AUDIT.md`, which A-REV7 found "substantively correct".
  - Its blanket "no call passes emit = false" is too strong: the production local-search calls pass false for centres
    that are already scored.
- **GUARD** (IMPL):
  - (G1) the guard reads only the clock, consumes no random number and changes no setting;
  - (G2) an unstopped run performs the R̄ (R̄⁺) computation, so on 𝒢ᶜ the **statistical outputs, scored sets, decisions
    and status** equal R̄'s (Lemma RO).
  - The run diagnostics do not equal R̄'s (V20).
- **OP-LS0** (parts using LS0): LS0 is executed, with its centre emitted and its scans completed, on every fit counted as
  output. A stopped LS0 counts in U.

**Posterior (all parts).** (P): δ₁ := 1 − π(S₀) → 0 in P₀-probability on R1 (s₀ fixed, p_n ≤ n^A). Sufficient:
- locked T03;
- or T03♯ (`W6-FIXREV2 §1.2`: G, R, SE_λ(j₀), SE_w(m♯_n; g₀) with g₀ fixed, BM-∞ or BM(c); A-REV2 and A-REV5 VERIFIED).

On LH exact Gram, (P) holds by W1-EXP Thm 5(d) (A-REV7 §2, A-REV8).

**Route (a).** (F): 1 − π₀(S₀) → 0 in probability. Sufficient: (F1), (F2) or (F3), as in v2.

**Route (b1).** A deterministic S° with Φ(S°) ≤ φ̄, and:
- **(M1)** P₀(π₀(S°) > ½) → 1, via W1-EXP Thm 6 under u < 1. Do not use E3(ii) without q < 1.
- **(M2)** POP-LAT(S°, m_n) with m_n ≥ M_n√(log n/n), M_n → ∞.
  - On LH: LH-LAT (fixed m₀; exact m₀♯).
  - Alternatively W_Lat + LH-PGD.
- **(M3)** λ_min(R_{S°∪S₀}) ≥ φ₀² > 0 and ‖μ‖²/n ≤ M.
- OP-LS0.

**Route (b1′).** x°_n Δ S₀ = {j_n}, with fixed margins (b₀ > 1/10, |𝒟_n| ≤ k_D, Dep_n ≤ 1 − c₀ w.p. → 1) or the general
rates of [CON] §5. Also P(NB′ᶜ) → 0, where NB′ means S₀ is among the initial pilot draws or the first-stage ESS is
≥ 0.9H₀, with r* = (11 + 2√10)/9.

**Route (b2).** A data-measurable 𝔛_n with repair certificates, and:
- **DELIV(𝔛_n):** P(SMC ∩ 𝒜 ∩ {no final-run particle of any island lies in 𝔛_n at 𝔉_T}) → 0, assumed directly;
- **REP(𝔛_n):** the single-particle form, or the product form under IND-T(a).

**STAB-LH** (W5-B2ENV): m_STAB := min over S° ⊆ V ⊆ (signal units), t ∈ S°, l ∉ V of
min{Δ(V − t) − Δ(V), Δ(V − t + l) − Δ(V)} > 0.
- **Sufficient (A-REV7 §4, Astra-authored, pending Claude verification):** λ₀b_vis² > R_M, where
  R_M = Σβ_i²ψ_i²(1−ψ_i²), λ₀ = (1 − max|ψ_i|)(1 − ρ_max) and b_vis² = min_{j∈S°}θ_j².
- STAB-LH is a real restriction: it fails at (ρ, ψ) = (0.85, 0.5) (W5-B2ENV; A-REV7 §5).

### I.C Theorem 5 (T38). Two-regime consistency of the reported HPM

Assume EX-A, EX-S, CAL, SR, GUARD and (P), on R1 with the v3 budgets indexed by n.

**(0) Composition, strict convention, for every n**, for both variants:

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n,   D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).

If D_n → 0, then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0. This is a statement about the joint
probability of output and error. It is not P(wrong | output), which need not vanish if P(𝒪) does (A-REV8). Recovery
with probability → 1 also needs P(U) → 0, which is not provided.
- Status: **PROVED**.
- SF: W3-VT38E.
- XF: **VERIFIED** (A-REV1 §7.4; A-REV5 output/execution interface; A-REV8 "W6 versus A-REV1 §7").
- Lean `t21_C1`: sorry-free, fidelity GREEN.

**(0_H) HPM convention.** P(𝒪_H ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n + D_n^{sl}, where
D_n^{sl} := P(SMC ∩ 𝒜ᶜ ∩ {S₀ ∉ 𝒮_cal ∪ 𝒮_LS0}).
- Status: PROVED.
- XF: VERIFIED (A-REV5, which keeps the schedule-limit discovery term). No SF check.

**(a) Favourable regime.** Under (F), D_n → 0 for both variants. Under the HPM convention, add D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ),
which nothing controls.
- Status: **PROVED-UNDER (F)**.
- Inputs: locked T11(iii); locked T22(iii) with EXP′ (A-REV2 and A-REV5 VERIFIED for fixed designs); W1-EXP Thms 2, 6.
- The ORTH joint family stays a PROOF SKETCH (⚑ III.6).
- S3/S4/S6: `W5-FAVIID · Cor. C3`, author only; its REPORT is now complete.

**(b) Masked regime** (π₀(S₀) → 0 allowed). D_n → 0 under any one of the following.
- **(b1) LS0 route; the method.** Assume (M1)–(M3), G and OP-LS0. Then S̃₀ = S°, and LS0 scores S₀ within
  max{Φ(S°) − 1, 0} moves once ℓ_n ≥ Φ(S°) − 1 [V17]. Under the HPM convention D_n^{sl} → 0 as well.
  - Theorem b1: **PROVED-UNDER (M1)–(M3)**.
  - SF: W5-VMASK.
  - XF: **VERIFIED** (A-REV8, which also verified LS-score discovery and Lemma M; A-REV5 direct route).
- **(b1′) D2 route; v3 as run.** The potential first stage of the tier-0 pilot scores S₀, and Ŝ⁺ = Ŝ.
  - Status: **PROVED (implication)** via D2-∞.
  - SF: W3-VT38E (finite D2).
  - XF: **VERIFIED** (A-REV1 finite D2 and D2-∞; A-REV5 rate margins).
  - Under the HPM convention, v2 adds that D_n^{sl} → 0 (⚑ III.8).
- **(b2) Gibbs-path route; v3 as run.** Assume DELIV(𝔛_n) and REP(𝔛_n). Under the HPM convention add
  D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ).
  - Status: **PROVED (implication)**.
  - XF: **VERIFIED** as an interface (A-REV1 §7.2; A-REV5).
  - **DELIV(𝔛_n) is OPEN in general.** A-REV5 rates the D3 surrogate for DELIV a GAP, because SHARE is unconditioned
    while the conclusion is conditional on 𝓒; (b2) assumes DELIV directly.

**(b1-LH) The explicit family, with LS0.**
- **What holds.** On LH with S° = S₀ ∖ M: (P), (M1), (M2) with a fixed margin m₀ > 0 (valid; sharp for homogeneous
  pairs; exact margin m₀♯), and (M3) all hold. π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}, so iid final draws miss S₀
  (Q_fπ₀(S₀) → 0) when n^{1−c/2}p^{−c}log²n → 0, for example c = 2 with p/log n → ∞, or c = 1 with
  p/(√n log²n) → ∞ [V18].
- **Conclusion.** With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no statistical hypothesis left open.
- **Status: PROVED** (candidate).
- **SF:** W5-VMASK (LS-score, Lemma M, Theorem b1, LH-LAT; partition = groups in 90/90 cases); W3-VEXP (W1-EXP Thm 5).
- **XF: VERIFIED** (A-REV8: "exact-Gram b1-LH consistency VERIFIED … with LS0; c = 1 needs only its initial scan"). The
  old iid-failure clause is ERROR (A-REV5) or GAP (A-REV8); it is not needed for consistency (⚑ III.13).
- **Variant:** the method (with LS0).
- Cor. GU-LH (W7-SEP) re-proves the search step. A-REV7 VERIFIED it as a greedy theorem.

**(b1′-LH) No LS0, one masked pair (W5-B2ENV Cor. D2-LH).**
- **Setting.** LH exact Gram with c = 1, p ≤ n − 1 and p/√n → ∞.
- **Conclusion.** P(S₀ ∉ 𝒮_cal) → 0, hence P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for **v3 as run**.
- **Status:** author "PROVED (given D2 [W1-T38E, repaired by W3-VT38E], [E-T1], [E-L4], [E-T5d])", that is, PROVED-UNDER.
  Crux: Theorem NB′-LH via Lemma OF.
- **SF: none.**
- **XF: VERIFIED for qualitative consistency** (A-REV7 §6), with corrected NB′. The stated unconditional O(√n/p) rate is a
  **GAP**: integrate the bound, truncated at one, over the data events.
- The LH-iid analogue (W3-PXN P7 + W5-VMASK R1) stays a GAP (A-REV3, A-REV6, A-REV8).

**(b2-LH) No LS0, every c (W5-B2ENV Theorem B2-LH).**
- **Setting.** LH exact Gram, every c ≥ 1, any frozen grid, under **STAB-LH**.
- **Conclusion.**
  P(S₀ ∉ 𝒮 | 𝓒) ≤ Nπ₀(𝒩ᶜ) + NT_ea_n + (1 − c₀ + o(1))^N → 0, with 𝒩 = {S ⊇ S°, ≤ 19 neutral extras},
  a_n = O_P((log n/n)^{3/2}) and c₀ a uniform order-event constant. W5-B2ENV states c₀(x) = g^{−c_x}/C(|Λ_x| + B + 2, B + 2); A-REV7 §4 uses c_* = g^{−c}/C(2cg + 19 + B + 2, B + 2). Hence P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for **v3 as run**.
  Integrate the bound, truncated at one, for unconditional convergence; the conditional O_P rate is not an unconditional
  numerical rate.
- **Status:** author **PROVED-UNDER STAB-LH**.
- **SF: none.** The author asked for a cross-family check of CONF and R1.
- **XF: VERIFIED as a conditional theorem** (A-REV7 §4). Confinement and repair were checked against the actual moves.
  A-REV7 corrected the event rate, η_n = O(n^{−1/3} + √(log n/n)), and the conclusions survive.
- **Explicit instance, Astra-authored, pending Claude verification** (A-REV7 §4).
  - Take g = 9, c = 2, no unlinked visible groups, ρ = 0.4, ψ = 0.2, β = 1 and σ² = 1, with null groups appended and
    p_n = 9⌊n/18⌋.
  - Then the analytic certificate gives STAB margin ≥ 0.4032, and the family is genuinely masked:
    π₀(S₀) = (p√n)^{−2}e^{O_P(1)} against an iid budget O(n log²n).
  - On it, (b2-LH) holds "with no numerical or unproved STAB premise left". This is A-REV7's recommended no-LS0 masked
    theorem.
- **Not covered:**
  - parameters violating STAB-LH;
  - unrestricted LH (general locking is false; A-REV7 §5);
  - LH-iid;
  - the study's random designs.

**(b1-LH-iid) p ≫ n, with LS0. Not in the headline.**
- **Setting.** LH-iid (W3-PXN §0), with g ≤ B_n < 2g and n^a ≤ p ≤ n^A.
- **Conclusion.** With LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 for every fixed c.
- **Status: PROVED** (candidate). **SF:** W5-VMASK, with repairs R2–R7.
- **XF: GAP**:
  - A-REV3: P6, P7 and the joint route;
  - A-REV6 and A-REV8, after W5-VMASK: Λ(a)'s Tr(c) range and dimension are still not generalised, and P7 prints
    (n−3−s)/2;
  - P1 is now VERIFIED via W7-PART Theorem B (A-REV6).
- No counterexample to the conclusion exists (⚑ III.4).

**(c) Cost.** The score evaluations are bounded deterministically by T32(i)'s ceiling plus 1 + (ℓ+1)·max_{k≤K}[p + k(p−k)]
for LS0. The total is **polynomial in n** under the v3 budgets.
- **Status: PROVED-UNDER T32(i)**. T32(i) is PROVED (W5-LOCKBOOK) and re-counted by W7-SEC (SF). XF: A-REV6 says the count
  is "supported by loop accounting" (no verdict word); A-REV9 deferred it.
- The displayed rate O((n+p)(p+B)log²(n+p) + p²log²(n+p)) is a **GAP** (A-REV6; V19). Astra's candidate is
  O(max(n,p)p log³(n+p) + p²log²(n+p)).
- Without EX-A, add the fp-pilot addendum (≤ T_e + 1 pilot stages).
- The LS0 term is PROVED and VERIFIED (A-REV1, A-REV5). At p = 1,000 it is about 1.7·10⁵ scores; measured median
  0.17–0.37 s per fit, under 0.1% of a fit (O-LS0).

### I.D Other candidate no-LS0 statements (none is a part of I.C)

| # | Statement | Range | Author status | XF verdict | Use |
|---|---|---|---|---|---|
| N1 | Cor. D2-LH | LH exact Gram, c = 1, p/√n → ∞ | PROVED-UNDER | A-REV7 VERIFIED (qualitative); rate GAP | **lifted to (b1′-LH)** |
| N2 | Thm 5(b1′) on LH-iid, c = 1 (W3-PXN P7 + W5-VMASK R1) | LH-iid | PROVED (candidate) | GAP (A-REV3, A-REV6, A-REV8) | not cited |
| N3 | Theorem B2-LH | LH exact Gram, every c, STAB-LH | PROVED-UNDER STAB-LH | A-REV7 VERIFIED (conditional) + Astra STAB certificate and subfamily | **lifted to (b2-LH)** |
| N4 | Theorem BG3 + Prop. LH-lock (final run alone) | LH exact Gram, **p fixed**, every c, strict C1–C3 | BG3 PROVED; LH-lock PROOF SKETCH | BG3 VERIFIED. LH-lock VERIFIED as a *conditional fixed-p implication* (A-REV7 §3 supplies the completion, Astra-authored). Unrestricted locking ERROR: C2 fails at g = 4, ρ = 0.85, ψ = 0.5 (A-REV7 §5) | fixed-p **component lemma**: production enumerates at fixed p |
| N5 | Theorem F1 (closure) + Theorem F2 (LH delivery) | LH exact Gram, p ≤ (1−c₀)n, PK, DOM | F1 PROVED; F2 PROOF SKETCH | F1 VERIFIED. F2 GAP (PK coverage, cap mapping, Lemma 3.4 Schur factor ERROR). "DOM void for c = 1" ERROR with visible groups | F1 as an abstract closure lemma; do not cite F2 |
| N6 | Prop. GU / Cor. GU-LH | exact Gram, isolated R | PROVED (candidate) | A-REV7 VERIFIED as greedy repair; GAP as a no-LS0 route (the actual search centre may contain nulls outside R); A-REV9 deferred | supports (b1-LH); not a no-LS0 theorem |

Related items:
- W5-B2ENV Prop. M-LH: author PROVED. XF VERIFIED as a restricted fixed-coefficient replacement (A-REV6). It is
  unaffected by A-REV3's W4-SHARE M(b) ERROR, because it uses exact log-RSS (A-REV7). ⚑ III.3 is resolved.
- O-BGIBBS BG1 / Prop. LH: PROOF SKETCH.
- O-MIX B3: a start change (B-merge), not adopted.

### I.E Not claimed

- P(U) → 0, any law of 𝒢 or of calibration failure, or P(wrong | output) → 0.
- Under the HPM convention: any control of P(SMC ∩ 𝒜ᶜ).
- Masked-regime evidence or PIP accuracy. F-MASKPIP gives one-sided bounds only: A-REV9 VERIFIED M1 and M2, and rated
  M3 an ERROR.
- Any statement conditional on completion or on diagnostics.
- Comparative superiority.
- Finite-n error rates, or any quantitative statement at n = 200.
- A masked p ≫ n theorem: (b1-LH-iid) has an XF GAP.
- No-LS0 consistency on **unrestricted** LH, on LH-iid, or on the study's designs. Covered: (b1′-LH) for c = 1, and
  (b2-LH) under STAB-LH (A-REV7's explicit subfamily).
- DELIV(𝔛_n) outside LH.
- A sharp polynomial cost rate: polynomiality is claimed, the displayed log² rate is not (V19).
- **That tempering, or the sampler, is necessary for discovery** (I.F, Remark 6).

### I.F Remarks for the paper text

1. **Execution.** Discovery statements concern R̄ (R̄⁺). GUARD transfers them to the reported *statistical* outputs on
   𝒢ᶜ (V20). Everything else is in U. Conditioning on observed completion is never used.
2. **Regime discipline.** (F) and the masked instances are never combined on one sequence. On LH, VIS fails at S₀. The
   ψ ≥ ρ boundary is a transition to the favourable regime (W5-VMASK §1 item 5).
3. **Delivery is part of the theorem.**
   - In (b1), delivery is S̃₀ = S° plus the lattice condition.
   - In (b1′), it is the pilot ESS rule (Lemma S′, f > 1 − e).
   - In (b2), it is DELIV(𝔛_n), OPEN in general. COUNTEREXAMPLE C1 applies: start mass, bridge mass and zero exits do not
     imply delivery.
   - In (b2-LH), delivery is **confinement** to a closed bounded-extras superset class (Prop. CONF), which avoids C1.
4. **H24 is not used.** It fails along CE1-narrow, which A-REV5 VERIFIED as an explicit sequence, not as universal failure.
5. **Why LS0.**
   - Without LS0, the final local search starts at the running HPM, so it delivers S₀ only through Lemma 0(b′)'s
     inclusion (with Prop. F; A-REV5 VERIFIED).
   - The natural eligibility condition fails with probability → 1 under omission masking (W1-T38E E1).
   - LS0 makes eligibility a deterministic property of the start law, at under 0.1% of a fit. It is the only route with a
     p ≫ n candidate, and it is the route of (b1-LH).
   - At n = 200 LS0 changed nothing: 0/2,394 HPM changes, and recovery unchanged in every cell (O-LS0). That could not have
     been improved on, because production has 0 search misses.
   - With (b1′-LH) and (b2-LH), LS0 is **no longer the only route on LH**.
6. **What the masked half shows: moving off the start is needed, not tempering** (`theory/E-SPINE`).
   - In the masked regime, iid start draws provably fail below Q* = p^c n^{c/2}, and so does a one-shot importance
     correction (T27; W7-SEP SEP(A)/(B), A-REV9 VERIFIED as implications).
   - Moving off the start fixes this, and several of v3's moves each suffice on LH:
     - one greedy search from the start mode (LS0; (b1-LH); Prop. GU);
     - the pilot's first Gibbs stage for c = 1 ((b1′-LH));
     - the bridge plus the terminal Gibbs rounds, confined to a closed class ((b2-LH)).
   - In the frozen setting there is no separation between the tempering bridge and a single greedy search, and no
     super-polynomial separation (W7-SEP §1 item 4).
   - The theorem therefore does not say that tempering is needed. The bridge's distinct contribution is calibrated Ẑ/PIPs
     (Thm 6, Prop 2) and the HPM ledger.
7. **n = 200 disclosure** (W8-SYNTH Decision 3; `E-SPINE §2.3`). At n = 200, p ∈ {500, 1000}, s₀ = 14, the theorem
   describes mechanism, not the reported numbers.
   - Of 2,400 fits, 6 stopped, 1,829 recovered S₀ exactly, and 565 were posterior misses. There were 0 search misses, and
     the final local search never moved (S-ELS).
   - O-LS0's finite-sample diagnostics:
     - π₀(S̃₀) > ½ in 18/2,400 fits;
     - lattice D_S, without margin, in 17/168 (c = 1) and 1/129 (c = 0.5) checked fits;
     - λ_min > 0 everywhere;
     - the cap ℓ ≥ Φ(S̃₀) − 1 in 1,968/2,400 fits.
     
     These are **not** the asymptotic (M1)–(M3) (A-REV8). LS-score's deterministic implication held in all 18 fits that
     met its premise.
   - The start is masked by dilution (O-DILUTE §7; Thm E and R are A-REV9 VERIFIED, while Prop. DM(i)'s size sign is
     ERROR).
   - T03♯ thresholds hold only from n ≈ 2·10⁶, and its beta-min constant exceeds the executed signals by ≥ 43×.
   - The bound is on P(reported and wrong), not P(wrong | reported).

**Why it matters (paragraph for the paper).** Theorem 5 is the paper's guarantee about the model the method actually
reports. The reported HPM is the best model the run ever scored. So it is right whenever the posterior ranks the truth
first (Theorem 1) and the run scores the truth at least once; part (0) turns this into one inequality valid at every n. In
the favourable regime the start draws alone score the truth. In the masked regime they provably cannot at any budget below
p^c n^{c/2}, so the run must **move off its start**, and part (b) shows that moving off the start is enough. On the
linked-hub family, one deterministic local search from the exact start mode scores the truth (b1-LH). On an explicit
subfamily the unmodified method's own Gibbs moves do so too: in the pilot for one masked pair (b1′-LH), and by confinement
and terminal repair for any number of pairs (b2-LH). The theorem does not say that tempering is what finds the truth: one
greedy search does it as well, and the bridge's own role is calibrated evidence and inclusion probabilities.

---

## Part II. Dependency map (inputs → sources → status → reviews)

Labels: PROVED-LOCKED, PROVED (campaign candidate), PROVED-UNDER [X], PROOF SKETCH, CONJECTURE, OPEN, IMPL, IDEAL.
**Bold** marks a change from v2. Proposed paper labels are in [ ].

### II.1 Composition and execution

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| C1 | strict maximiser on {π(S₀) > ½} ∩ {S₀ scored}; Markov | locked T21(C1); T38_PROOF §1 | PROVED-LOCKED / PROVED | W3-VT38E | A-REV1 §7.4; **A-REV5; A-REV8**; **Lean `t21_C1` sorry-free, fidelity GREEN** |
| RO | Lemma RO | W2-BOOK §0.2 | PROVED | **W5-LOCKBOOK** | **A-REV4 VERIFIED*; A-REV6 VERIFIED (conditional implication)** |
| GUARD | (G1), (G2) | W2-BOOK §0.1 | IMPL | code reading (SF) | **A-REV5, A-REV8 code readings support the statistical stop-only coupling; literal "every output equals" ERROR (A-REV4, A-REV8 E2)** |
| HPM conv. | D_n^{sl} | v2 T38_PROOF §1.3 | PROVED | none | **A-REV5 VERIFIED** |
| P | δ₁ → 0 | locked T03; T03♯ (W6-FIXREV2 §1.2) | PROVED-LOCKED / PROVED | W2-VT03R | A-REV2; **A-REV5 (core; onset gloss ERROR)** |
| SR | scored set | SR_AUDIT.md | IMPL | HQ; W5-LOCKBOOK | **A-REV7: substantively correct; one sentence too strong** |

### II.2 Route (a)

Unchanged from v1 II.2 (a1–a8):
- a6, the ORTH joint family: PROOF SKETCH (⚑ III.6; A-REV6 GAP);
- S3/S4/S6 via `W5-FAVIID · Cor. C3`, author only.

### II.3 Route (b1) and the LS0 instances

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| b1.1 | E3′(i); centre emitted; cost with "+1" | [CON] §6 | PROVED | W3-VT38E; W5-VMASK | A-REV1; **A-REV5 VERIFIED** |
| b1.2 | Lemma LS-score [Lemma LS] | W4-T38FULL §3.1 | PROVED | W5-VMASK row 20 | **A-REV8 VERIFIED (discovery); move-count ERROR at C₀ = S₀ → max{Φ−1, 0}** |
| b1.4 | Lemma M [Lemma SC] | W4-T38FULL §3.2 | PROVED | W5-VMASK row 21 | **A-REV8 VERIFIED** |
| b1.5 | Theorem b1 | W4-T38FULL §3.3 | PROVED-UNDER (M1)–(M3) | W5-VMASK row 22 | **A-REV8 VERIFIED; A-REV5 VERIFIED (direct route)** |
| b1.6 | (M1) via W1-EXP Thm 6 | W1-EXP | PROVED | W3-VEXP | **A-REV8 (joint exact-Gram premises VERIFIED)** |
| b1.7 | LH: ELIG, masking, π(S₀) → 1 | W1-EXP Thm 5 | PROVED | W3-VEXP | **A-REV8 VERIFIED (fixed parameters)** |
| b1.8 | Prop. LH-LAT | W4-T38FULL §3.4 | PROVED; "sharp" withdrawn | W5-VMASK rows 23, 23′ | **A-REV8 VERIFIED (valid lower bound)** |
| b1.8′ | W_Lat + LH-PGD | W5-VPGD R6.2–R6.3 | PROVED (candidate) | author = W5-VPGD | **A-REV8 VERIFIED (lattice scope)** |
| b1.8″ | Prop. GU / Cor. GU-LH | W7-SEP §4.2 | PROVED (candidate) | none | **A-REV7 VERIFIED (greedy); A-REV9 deferred** |
| b1.9 | LH-iid P1–P8 | W3-PXN | PROVED | W5-VMASK | A-REV3: P1–P5, P8 VERIFIED; **P6, P7, joint route GAP, retained by A-REV6 and A-REV8; P1 via W7-PART B VERIFIED (A-REV6)** |
| b1.9′ | partition = groups (iid designs) | W7-PART Thm B | PROVED | none | **A-REV6 VERIFIED (restricted); A-REV9 B-exact VERIFIED, L2 constants GAP** |
| b1.11 | TD(d,0) false for d ≥ 1 | W1-T37R Prop 1 | PROVED (negative) | VERIFIED | — |
| b1.13 | `emit_centre = true` | W3-VT38E; W5-LOCKBOOK | IMPL | — | A-REV1 §6; **A-REV8 (a cached un-emitted centre is not repaired by a later hit)** |
| b1.14 | LS0 on the study fits | O-LS0 | data | — | **A-REV8: zero-change summary VERIFIED as a reading of the saved records; finite diagnostics ≠ asymptotic premises (GAP if equated)** |

### II.4 Route (b1′)

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| d1 | Lemma S′ [Lemma ESS] | [CON] §4 | PROVED | — | A-REV1; **A-REV5 VERIFIED** |
| d2 | Lemma A | W1-T38E §1 | PROVED | VERIFIED | — |
| d3 | finite D2, NB′, r* | W1-T38E §4 + W3-VT38E | PROVED | VERIFIED | A-REV1; **A-REV5 VERIFIED** |
| d3′ | D2-∞ with rate margins | [CON] §5 | PROVED (implication) | — | **A-REV5 VERIFIED** |
| d4 | masked instance, LH exact Gram, c = 1 | **W5-B2ENV Cor. D2-LH, Thm NB′-LH** | **PROVED-UNDER (author)** | none | **A-REV7 VERIFIED (qualitative); rate GAP** |
| d4′ | masked instance, LH-iid, c = 1 | W3-PXN P7 + W5-VMASK R1 | PROVED (candidate) | W5-VMASK (D2-a/b/c) | **GAP (A-REV3, A-REV6, A-REV8)** |

### II.5 Route (b2)

v2 rows g1–g8 are unchanged. The g1 family (Theorem B with conventions, U′, Lemma P, IND-T) is now **A-REV5 VERIFIED**.

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| g4 | DELIV(𝔛_n), general | W1-T38E D3 | **OPEN** | — | C1 COUNTEREXAMPLE VERIFIED; **A-REV5: D3 surrogate conditioning GAP** |
| **g4-LH** | **Prop. CONF (confinement)** | **W5-B2ENV §4.3** | **PROVED under STAB-LH** | none | **A-REV7 VERIFIED (checked against actual moves)** |
| **g5-LH** | **Lemma R1 (repair by an order event), Lemma J, Lemma T** | **W5-B2ENV §4.4** | **PROVED (under STAB-LH where stated)** | none | **A-REV7 VERIFIED (η_n corrected)** |
| **STAB** | **analytic STAB certificate; explicit subfamily** | **A-REV7 §4** | **REFEREE (Astra-authored)** | **none (Sol check only)** | **pending Claude verification** |
| g4′ | W4-SHARE D4, D5 | W4-SHARE | PROVED | W5-B2ENV | A-REV3; **A-REV6 VERIFIED**; §7 exit-loss simplification ERROR |
| g4″ | BG3 / LH-lock | O-BGIBBS | PROVED / PROOF SKETCH | none | **A-REV7: BG3 VERIFIED; LH-lock VERIFIED conditional fixed-p; general locking ERROR** |
| g4‴ | F1 / F2 | F-SHARE | PROVED / PROOF SKETCH | none | **A-REV7: F1 VERIFIED; F2 GAP; DOM c = 1 exemption ERROR** |

### II.6 Cost

| # | Input | Source | Status | SF | XF |
|---|---|---|---|---|---|
| k1 | T32(i) count | W5-LOCKBOOK PROOF §T32 | **PROVED** (v2 said CONJECTURE: stale) | W7-SEC re-count | **A-REV6: "supported by loop accounting" (no verdict word); A-REV9 deferred** |
| k1-rate | T32(c) asymptotic rate | W5-LOCKBOOK | PROVED | W7-SEC | **A-REV6 GAP (log³ calibration factor); polynomial survives** |
| k1′ | fp-pilot addendum | W7-SEC | PROVED | author | **A-REV9 deferred** |
| k2 | LS0 term | [CON] §6; W5-VMASK R7 | PROVED | W5-VMASK | A-REV1; **A-REV5; A-REV8** |

### II.7 Method-change record

| Change | Status | Bearing on Theorem 5 |
|---|---|---|
| **LS0** | **part of the method** (O-LS0: 0/2,394) | needed for (b1), (b1-LH) and (b1-LH-iid); not needed for (b1′-LH) or (b2-LH). Obligations: emit the centre first; HPM tie rule for argmax π₀; label mechanisms; an in-engine integrated test fit is still to run |
| common-σ² start | **rejected** (O-DILUTE §5; F-SIGMA Thm S6) | none |
| B-merge start (O-MIX) | not adopted | — |
| residualised tables | not adopted (F-SIGMA Step 0 first) | — |

---

## Part III. Conflicts (⚑)

| # | Item | Position A | Position B | Recorded as | State |
|---|---|---|---|---|---|
| III.1 | T32(i) | CONJECTURE: v2 k1; W7-SEP I11 | PROVED: W5-LOCKBOOK; W7-SEC re-count | PROVED (SF only). A-REV6: count supported, rate GAP. A-REV9: deferred | open (XF verdict word) |
| III.2 | A masked theorem without LS0? | "OPEN": v1, v2 | A-REV7: available on an explicit exact-Gram LH subfamily (B2-LH + analytic STAB); D2-LH for c = 1 | (b1′-LH), (b2-LH) in I.C. The STAB certificate is Astra-authored, pending Claude verification | **settled toward B** on that subfamily; unrestricted LH not claimed |
| III.3 | W4-SHARE M(b) versus W5-B2ENV M-LH | W5-B2ENV: M-LH PROVED | A-REV3: M(b) ERROR | M(b) ERROR retained; M-LH VERIFIED (A-REV6, A-REV7) | **settled** |
| III.4 | W3-PXN P6/P7 | W5-VMASK: VERIFIED, cosmetic errors only | A-REV3, A-REV6, A-REV8: GAP | GAP | settled toward GAP; A-REV6 supplies a candidate generalised tail lemma (Astra) |
| III.5 | LH-LAT "sharp" | v1 | W5-VMASK R5; A-REV8 | valid lower bound | settled |
| III.6 | ORTH joint family | v1: "no open input" | W2-T26 Prop. C PROOF SKETCH; A-REV4 and A-REV6 GAP | PROOF SKETCH | open |
| III.7 | Output convention | W2-BOOK, A-REV1: 𝒪_H | v1, v3: strict 𝒪 | both stated (A-REV5 VERIFIED both) | open decision (D1) |
| III.8 | (b1′) under 𝒪_H: D_n^{sl} → 0 automatically? | v2: yes | A-REV1 §7.4: add usable no-score output when the pilot stage does not execute | v2's sentence kept, flagged; A-REV5 verified the output interface but did not address this sentence | open |
| III.9 | Theorem W region vs lattice form | F-REFINE | W5-VPGD R6.1; A-REV8 | W_Lat | settled |
| III.10 | Lemma 0(b) | W1-T37R | W3-VT37R, A-REV2 ERROR; S-ELS true on the data; A-REV5 VERIFIED Lemma 0(b′) | cite Lemma 0(b′) + Prop. F | settled; W3-VT37R rerun on PROD-H still useful |
| III.11 | W7-SEP's no-LS0 citation | W7-SEP: BG1 only | O-BGIBBS BG3; A-REV7 | cite B2-LH and D2-LH (A-REV7); BG3 as a fixed-p component | settled |
| III.12 | "9 ≤ g ≤ 16" | W3-PXN, W5-VMASK | W7-PART | g ≤ B_n < 2g | settled |
| III.13 | (b1-LH) iid-failure clause, c = 2 | A-REV5: ERROR (counterexample p ≍ log log n) | A-REV8: GAP (the ceiling does not vanish; not a counterexample to the actual production Q_f) | the weaker verdict (ERROR) on the clause; referee repair applied (V18) | settled (same repair) |
| III.14 | Prop. GU | A-REV7: VERIFIED (greedy) | A-REV9: GAP in its own review (Lemma M not re-audited; A-REV8 VERIFIED Lemma M) | VERIFIED* | scope difference, not a dispute |
| III.15 | LH locking in general | O-BGIBBS: gaps "for general (ρ, ψ, g, c)" open, (C1′)/(C2′) proved for every parameter | A-REV7 §5: C2 is **false** for allowed LH parameters (g = 4 and g = 9 at ρ = 0.85, ψ = 0.5) | general LH-lock ERROR; conditional fixed-p version VERIFIED | settled |
| III.16 | Lean fidelity | W8-SYNTH §7: Astra run "did not finish" | L-LEAN final: Astra round 2 GREEN | GREEN | settled (W8-SYNTH stale) |

---

## Part IV. Decisions this statement depends on

| # | Decision | State | Effect |
|---|---|---|---|
| D1 | Output convention (strict 𝒪 or 𝒪_H) | **open** (HQ and Felipe); W8-SYNTH recommends strict | (0) is the default and (0_H) the alternative |
| D2 | Headline of Theorem 5(b): (b1-LH) with LS0, or a no-LS0 LH theorem | **open, and the condition is met**. SR_AUDIT records "T38 + LS0 as the main theorem and the no-LS0 version as a conditional remark". W8-SYNTH recommends switching to no-LS0 if A-REV7 verifies a route on an explicit family; A-REV7 did ((b2-LH) on its analytic subfamily; (b1′-LH) for c = 1) and recommends B2-LH as the no-LS0 masked theorem. Before switching, a Claude run should verify A-REV7's Astra-authored STAB certificate and subfamily | v3 states both. It does not choose |
| D3 | LS0 | **taken**: part of the method | V1 |
| D4 | Spine wording | **taken**: "moving off the start is needed" | Remark 6; "Why it matters" |
| D5 | Common-σ² start | **taken**: rejected | II.7 |
| D6 | "Favourable from n ≈ …" threshold | **open**; recommendation: omit it, or attribute it to W5-FAVIID | not quoted |
