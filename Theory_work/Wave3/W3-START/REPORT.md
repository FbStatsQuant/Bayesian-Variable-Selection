# W3-START — REPORT (start-mass rate; PROGRAM item 2)

Lead: Claude Fable 5.2 (effort high). Statement: `STATEMENT.md` v1.3.4. Proofs: `lemmas/L1_AGG_FLOOR.md` …
`lemmas/L11_EXAMPLES.md`. This file is the technical report and is part of the frozen content that the council reads.
It therefore contains **no review record**: the review trail, the council outcome, the final status of each claim
and the registry blocks are in the ticket's final checkpoint file, which is written after the council and is not
part of the frozen content (the acceptance tool requires the frozen content to be unchanged after the council round,
so nothing that depends on the council can be written here).

## 1. Result (author's statement)

Every claim of `STATEMENT.md` §5 has a proof in `lemmas/`; author status of each: "PROVED (by this seat)". Nothing is
left conditional on an unproved input, and **no registry claim is consumed**. Two families of the examples table
(UNI-0, exact-separation AR(1)) are listed as expected and are not verified.

In words:
* **A deterministic floor.** For every data set and every unsaturated model, the coded start gives it mass at most
  1 − ⅓(n + 1)^{−1/2}. With at least one null column, no condition on the design gives a start-mass rate better than
  n^{−1/2}.
* **Fixed design (START-F).** Under an energy bound, a constant floor on the unnormalised Gram matrix of every set of
  at most 16 columns, visibility of the truths, and an averaged leakage condition, the start odds against the true
  model are O_P(n^{−1/2} × a deterministic leakage functional) plus a polynomially small visibility term. To first
  order they equal the prior-weighted sum of the single-null block Bayes factors. The bound is uniform over the class
  with explicit constants.
* **Random design.** The uniform bound transfers to any design law with Gaussian noise given the design, with
  coefficients, support and leakage set that may depend on the design. For Gaussian rows under population visibility
  and population no-leakage conditions, π₀(S₀) ≥ 1 − n^{−1/2}exp(C√log n) with probability → 1 for some constant C, for p ≤ n^A, p ≫ n
  included.
* **Limits.** On the actual partition, one null with normalised gain above (1 + 2Ā) log n given the truths of its
  block, or one truth with normalised gain below (1 + 2A̲) log n given the other truths of its block, sends π₀(S₀) → 0.
* **Interfaces.** W3-SAMP's premise P-START is delivered with a rate; the production form of P-OVL is delivered under
  a bounded leakage set; the misspecified-candidate form follows by an exact reduction.

## 2. The statement as proved, and changes against the ticket brief

Target of the brief (`BRIEF.md`): π₀(S₀) ≥ 1 − n^{−c} with probability → 1 under primitive, design-agnostic no-leakage
conditions, p ≤ n^A, p ≫ n; the conditions that deliver P-START and, if cheap, P-OVL; the misspecified form where it
costs little; an honest statement of where it fails.

| brief | delivered | where |
|---|---|---|
| rate n^{−c} | every c < ½ for Gaussian rows; the exact order n^{−1/2} in a fixed-design example; ½ is optimal | (T3)(b), F2, (T0) |
| primitive, design-agnostic conditions | partition-free conditions on (X, θ*) or (Σ_n, θ*); blocks appear only in the component lemmas | §3, §5.3 |
| p ≫ n | Gaussian rows with p ≤ n^A; the fixed-design theorem also allows p ≫ n, its verified fixed-design examples have p ≤ n − 1 | (T3)(b), (T1), (T7) |
| P-START | with a deterministic rate | IF-START |
| P-OVL "if cheap" | proved in its production form for a bounded leakage set with uniformly bounded levels | Proposition OVL |
| misspecified form | by Lemma R′ (re-proved) | (T6) |
| where it fails | masked truths and strong-factor designs at p > K are outside the hypotheses; with leakage only the lattice mass and the OVL lower bound are claimed | (N4), §6 |

Changes of substance made to the target while the ticket ran, each with its reason:
1. The normalised small-set floor was replaced by a constant **unnormalised** Gram floor (GF-16): weaker, same rates;
   the toolkit is re-proved locally (Lemma TK), so the earlier dependence on two registry claims was removed.
2. The leakage functionals carry a **truncation level per null column** within a summable tail budget; Corollary F4
   then reaches every constant leak level below 1 + 2A̲ for a bounded number of columns.
3. The transfer allows **design-measurable** coefficients, support and leakage set.
4. The truth-block functional Ξ and the **margin form (V-m)** of visibility replace the cruder truth-deletion
   functional as the main route; (V-c) stays as a sufficient condition.
5. The partition-free "one leaking null" limit (N2) is **vacuous for s₀ ≤ 15**; the limit is claimed on the actual
   partition through (C2)(i).
6. In the Gaussian-row bridge, the exactly-zero-leakage clause is a **tightness** statement (O_P), not a bound with a
   fixed constant holding with probability → 1; the theorem (T3)(b) is unaffected.
7. (B-R) and (T3)(b) state the hypothesis **p > s₀** explicitly (nothing is claimed at p = s₀, as §6 already said).
8. Proposition OVL assumes levels **bounded uniformly** by a fixed ā.
9. The examples table separates the five families verified here from two expected ones.

## 3. Claims, proofs and author status

Claim ids are `W3-START:<id>`. One status per claim. Lines refer to `STATEMENT.md`.

| id | claim | statement | proof | author status |
|---|---|---|---|---|
| AGG | (C0) table identities (AGG-a)–(AGG-d), one-step floor | `STATEMENT.md:196-210` | `lemmas/L1_AGG_FLOOR.md` L1.1–L1.5 | PROVED (by this seat) |
| FLOOR | (T0) deterministic floor | `STATEMENT.md:240-242` | `lemmas/L1_AGG_FLOOR.md` L1.5 | PROVED (by this seat) |
| TK | (B-TK), [TK]: toolkit under (GF-16) | `STATEMENT.md:232` | `lemmas/L2_TK.md` | PROVED (by this seat) |
| LEAK | (B-L), [LEAK(Q)], Lemma J, (B1) for the functionals | `STATEMENT.md:233` | `lemmas/L3_LEAK.md` | PROVED (by this seat) |
| VIS-c | (B-V1): constant-level visibility ⇒ [VIS] | `STATEMENT.md:234` | `lemmas/L4_VIS.md` L4.2, L4.3 | PROVED (by this seat) |
| VIS-m | (B-V2): margin visibility ⇒ [VIS] | `STATEMENT.md:235` | `lemmas/L4_VIS.md` L4.1 | PROVED (by this seat) |
| ASM | (C1) assembly | `STATEMENT.md:212-218` | `lemmas/L5_ASM_STARTF.md` L5.1 | PROVED (by this seat) |
| START-F | (T1)(a)–(d) fixed-design theorem | `STATEMENT.md:244-263` | `lemmas/L5_ASM_STARTF.md` L5.2, L5.3 | PROVED (by this seat) |
| F1 | (T2) uniform leakage | `STATEMENT.md:267-270` | `lemmas/L6_COROLLARIES.md` L6.1 | PROVED (by this seat) |
| F2 | (T2) strong signals, exact order | `STATEMENT.md:271-274` | `lemmas/L6_COROLLARIES.md` L6.2 | PROVED (by this seat) |
| F3 | (T2) bounded gains | `STATEMENT.md:275-276` | `lemmas/L6_COROLLARIES.md` L6.3 | PROVED (by this seat) |
| F4 | (T2) isolated leaking columns | `STATEMENT.md:277-286` | `lemmas/L3_LEAK.md` L3.5, `lemmas/L6_COROLLARIES.md` L6.4 | PROVED (by this seat) |
| NEC-b | (C2) component diagnostics | `STATEMENT.md:220-225` | `lemmas/L7_NEC.md` L7.1, L7.2 | PROVED (by this seat) |
| NEC | (T4) limits (N1)–(N3); (N4) is a scope statement | `STATEMENT.md:315-330` | `lemmas/L7_NEC.md` L7.3 | PROVED (by this seat) |
| TRANSFER | (T3)(a) random-design transfer | `STATEMENT.md:289-304` | `lemmas/L8_TRANSFER.md` | PROVED (by this seat) |
| BR | (B-R) Gaussian-row bridge | `STATEMENT.md:236` | `lemmas/L9_BR.md` L9.1–L9.6 | PROVED (by this seat) |
| START-R | (T3)(b) Gaussian rows | `STATEMENT.md:305-313` | `lemmas/L9_BR.md` L9.7 | PROVED (by this seat) |
| IF-START | (T5) P-START with a rate | `STATEMENT.md:333-337` | `lemmas/L10_INTERFACES.md` L10.1 | PROVED (by this seat) |
| OVL | (T5) Proposition OVL | `STATEMENT.md:338-343` | `lemmas/L10_INTERFACES.md` L10.2 | PROVED (by this seat) |
| MIS | (T6) misspecified candidate set | `STATEMENT.md:345-356` | `lemmas/L10_INTERFACES.md` L10.3 | PROVED (by this seat) |
| EX | (T7) five example families verify the hypotheses | `STATEMENT.md:358-370` | `lemmas/L11_EXAMPLES.md` | PROVED (by this seat) for F-1, F-2, F-3, G-1, G-2; UNI-0 and AR(1): not verified, nothing claimed |

Dependence between the claims (no cycle): AGG, FLOOR (deterministic) → TK → LEAK, VIS-c (uses LEAK and AGG-d), VIS-m →
ASM (AGG + interfaces) → START-F → F1–F4, TRANSFER; NEC-b uses TK and the prior ratios; NEC uses NEC-b, FLOOR, F2; BR is
a statement about the design only; START-R uses BR, TRANSFER and START-F(d); IF-START uses START-F and START-R; OVL uses
AGG-c, TK, LEAK, VIS-c; MIS uses Lemma R′ and TRANSFER; EX uses F1, F2, F4, START-F, START-R.

## 4. Assumptions (ids), properties and relations to existing results

| id | name | where stated | shared | bridge |
|---|---|---|---|---|
| A:START-E | energy ‖μ‖² ≤ Mn; p ≤ n^A; s₀ fixed; p > s₀ | `STATEMENT.md:134` | no (new) | Lemma TK |
| A:START-GF | (GF-16): λ_min(X_TᵀX_T) ≥ g_* for 1 ≤ \|T\| ≤ 16 | `STATEMENT.md:135-138` | no (new) | Lemma TK |
| A:START-V | visibility: (V-c) or the margin form (V-m) | `STATEMENT.md:139-150` | no (new) | (B-V1), (B-V2) |
| A:START-AL | averaged leakage with a level vector | `STATEMENT.md:151-156` | no (new) | (B-L) |
| A:START-R-FL | (FL-R16) population floor on sets of size ≤ 16 + s₀ | `STATEMENT.md:159-160` | no (new; the small-set part of W3-RM's (FL-R)) | (B-R) |
| A:START-R-V | (V-R) population visibility PTV(a_V) | `STATEMENT.md:161` | same condition as W3-RM's (V-R) | (B-R) |
| A:START-R-L | (L-R) localised bounded leakage | `STATEMENT.md:162-166` | W3-RM's (L-R) without (L-feas) | (B-R) |
| A:BLOCK-LE-16 | partition is a function of X with blocks ≤ 16 | `STATEMENT.md:168-171` | yes (existing id) | — |
| A:EX-A | exact arithmetic | `STATEMENT.md:168-171` | yes (existing id) | — |

Interface properties delivered (existing ids): **A:P-START** (premise of W3-SAMP:C@1.1.1) by IF-START, with a rate;
**A:P-OVL** (premise of W3-SAMP:D@2.1.1) in its production form by OVL. Interface properties internal to the ticket:
[TK], [LEAK(Q)], [VIS(κ; Q)] (`STATEMENT.md:173-190`).

`implies` relations to existing registry entries (each is a one-line consequence, not a claim about the status of the
other entry):
* START-F with Q = S₀, and START-R with Q = S₀ ⇒ A:P-START (IF-START).
* OVL ⇒ A:P-OVL in the production form max(n, p)·log₂(n + 1)·π₀(S₀) → ∞, when limsup(E_n − max(1, log p/log n)) < 0.
* START-F's conclusion under its hypotheses contains the conclusion of SOP:TH116 clause (iii) (aggregate start
  concentration) without assuming the expansion EXP′ or a uniform leakage bound; the hypotheses are not nested in
  general, so this is recorded as "related", not as an implication.
Cited as limits, not consumed: W1-PXN:Thm-PXN(S)@1.0.0, status "XF VERIFIED". Sources of arguments, not consumed:
C-GROW:L0.1@1.0.0, C-GROW:L0.2@1.0.0 "PROVED-CHECKED" (toolkit), GEN `lemmas/L1_lemmaE.md`, C-MIS:LemR@1.0.0
"R02 VERIFIED; council R07/R08 PASS" (reduction), W3-RM:SAND-R@1.0.0 "PROVED (by this seat, unchecked)" (route of the
Gaussian-row bridge).

## 5. Sharpness record

| assumption / feature | reading | evidence |
|---|---|---|
| exponent ½ | NECESSARY (for every design with a null column) | (T0), `lemmas/L1_AGG_FLOOR.md` L1.5 |
| T₁ → 0 | NECESSARY for π₀(S₀) → 1 | (AGG-b): o₀ ≥ T₁ |
| Ξ → 0 (visibility interface) | NECESSARY when s₀ + 16 ≤ K | (AGG-b): o₀ ≥ c_sΞ |
| visibility level 1 + 2A | NECESSARY on the actual partition, and partition-free for a single truth | (C2)(ii), (N3), `lemmas/L7_NEC.md` |
| leak level 1 + 2A for one column | NECESSARY on the actual partition; partition-free form vacuous for s₀ ≤ 15 | (C2)(i), `lemmas/L7_NEC.md` L7.3; reached from below by F4 |
| A:START-AL (the functional itself) | NECESSARY-FOR-ROUTE: sufficient; the necessity of the truncated-expectation functional and of the maximum over all conditioning sets is not established | `ASSUMPTION_MAP.md` §2 |
| A:START-V, form (V-c) | WEAKENABLE: superseded in generality by (V-m) | example F-2, `lemmas/L11_EXAMPLES.md` L11.3 |
| A:START-GF | NECESSARY-FOR-ROUTE: enters only Lemma TK; a floor-free version needs a rank-sensitive aggregation | open item O2 |
| A:START-E, energy part | NECESSARY-FOR-ROUTE: used only for RSS^y ≥ c_En in the score remainder | `lemmas/L2_TK.md` L2.3; numerics (f) of `numerics/RESULTS.md` |
| s₀ fixed | ARTEFACT of the bookkeeping (the table identities are explicit in s₀) | open item O3 |
| Gaussian noise | NECESSARY-FOR-ROUTE (exact Gaussian integrals) | Lemma J |
| A:START-R-L, scale C_Ln^{−1/2} | ARTEFACT-threshold: a population leakage level with an explicit exponent is the natural statement | open item O1; numerics (h) |
| A:START-R-L, localisation | NECESSARY-FOR-ROUTE (reduces all 15-sets to polylogarithmically many reference sets) | `lemmas/L9_BR.md` L9.4, L9.8 |
| factor exp(C√log n) in (T3)(b) | not known to be sharp; produced by a bounded mean shift at the critical Gaussian moment | `lemmas/L9_BR.md` L9.5 |

Binding map: visibility is forced by (AGG-b) (o₀ ≥ c_sΞ) and by (C2)(ii); T₁ → 0 by (AGG-b); the exponent ½ by (T0);
(GF-16), the energy bound, Gaussian noise and localisation only by the proof route.

## 6. Numerics (observations, not proofs)

* `numerics/RESULTS.md`: production core, 1018 runs, p = 2n, n ≤ 1600 (sharpness-gate numerics on the earlier statement;
  its labels are corrected where the statement changed).
* `numerics/lemmas/RESULTS_LEMMAS.md`: falsification attempts for L1–L11 with an independent base-R transcription of
  the scorer; 0 violations of the asserted checks; what each script does not test is listed there.
* `citecheck.py`: every `path:line` citation of this ticket resolves (existence and range only; not semantics).

## 7. Open items and recommended next steps

| id | item | recommendation |
|---|---|---|
| W3-START-O1 | Gaussian rows with a population leakage level η and an explicit exponent, instead of the scale C_Ln^{−1/2} | a small follow-up once (B-R) is accepted: one parameter changes in the Gaussian integral of L9.5 |
| W3-START-O2 | no Gram floor at all | needs a rank-sensitive aggregation; low priority |
| W3-START-O3 | growing s₀ | the identities are explicit in s₀; the visibility condition must be re-normalised |
| — | a fixed-constant, probability → 1 bound when C_L = 0 | needs concentration across columns; not attempted |
| — | UNI-0 and exact-separation AR(1) as verified examples | needs (V-R), (L-R) verified from checked sources |
| — | the decision-relevant gap | strong-factor designs at p > K (PROGRAM decision D1) and masked truths remain outside: the start then needs a different mechanism, not a sharper analysis of this one |

For the paper: present (T0) and START-F with the first-order form as the description of what the block-product start
does; present (T3)(b) as the p ≫ n statement; say plainly that the start needs each truth visible at
(1 + 2A)·τ²·log n with τ² including the signal its block leaves unexplained.

## 8. Files (all under `Theory_work/Wave3/W3-START/`)

* Top level: `STATEMENT.md` (v1.3.4), `PLAN.md`, `ASSUMPTION_MAP.md`, `BRIEF.md`, `REPORT.md`, `citecheck.py`; `LOG.md` and
  the checkpoint files are outside the frozen content.
* Proofs: `lemmas/L1_AGG_FLOOR.md`, `lemmas/L2_TK.md`, `lemmas/L3_LEAK.md`, `lemmas/L4_VIS.md`, `lemmas/L5_ASM_STARTF.md`,
  `lemmas/L6_COROLLARIES.md`, `lemmas/L7_NEC.md`, `lemmas/L8_TRANSFER.md`, `lemmas/L9_BR.md`, `lemmas/L10_INTERFACES.md`,
  `lemmas/L11_EXAMPLES.md`.
* Numerics, production-core runs: `numerics/run_start.R`, `numerics/start_common.R`, `numerics/summarise.R`,
  `numerics/results_raw.csv`, `numerics/summary.csv`, `numerics/RESULTS.md`.
* Numerics, lemma falsification: `numerics/lemmas/lem_common.R`, `numerics/lemmas/falsify_L1.R`,
  `numerics/lemmas/falsify_L2_L3.R`, `numerics/lemmas/falsify_L4_L5.R`, `numerics/lemmas/falsify_L6_L11.R`, their outputs,
  and `numerics/lemmas/RESULTS_LEMMAS.md`.
* Reviews: `reviews/` (briefs, frozen manifests, reviews, dispositions, `reviews/INPUTS.txt`, `reviews/CITECHECK.txt`).
* Git: nothing outside the ticket folder was modified; the lead changed no git state.
