# CASCADE — registry dependents of the 19 narrowed claims

2026-11-16 05:59 CST, origin/main 967313dd. Source: every claims.tsv row whose `depends_on`, `consumes`, `implies`,
`coexists_with`, `superseded_by`, `acks`, `gates` or `headline` names one of the 19 ids. I also checked aliases.tsv,
sharpness.tsv and HEADLINE_CANDIDATES.md. For each edge: does the narrowed statement still cover the use?
- **clear** = the use is a non-delivery part, or the dependent is narrowed in the same form.
- **stay SUSPECT** = the dependent asserts delivery under plain IDEAL-W on its own and is not in this batch.

## 1. Edges inside the batch (all covered: both ends narrowed in the same form)

| dependent | → uses | covered? |
|---|---|---|
| HQ_AUDIT-W1C:A3 | A2 | yes (A3 :5 re-states A2's narrowed clauses) |
| W2-FAC-A:Thm-FAC-L | Prop-F-FAC (depends_on, implies) | yes (claim (D) = F-FAC, same two clauses) |
| W2-LOC2:F-LOC2, .exp, .poly | W2-FAC-A:Prop-F-FAC@proof:FACA L7 Steps 1-3; parent ↔ parts | yes |
| W2-FAC-B:Thm-FAC-CS | W2-FAC-B:L5 | yes ((C4) narrowed; L5.4 :61 narrowed in place) |
| W2-FAC-PK:Thm-FAC-PK | W2-FAC-B:L5@proof:L5.1 (H0) and L5.4 delivery | yes (PK (iii) narrowed, with its own 𝔇_PK) |
| W2-FAC-S5:Thm-FAC-BCS-R | W2-FAC-B:L5@proof:assembly pattern | yes |
| W2-FAC-S5:L5 | W2-FAC-B:L5@proof:L5.1; W2-FAC-S5:L5.C4-R (stmt, implies) | yes (C4-R narrowed) |
| W2-FAC-S5:L5.C4-R | W2-FAC-B:L5@proof:L5.4 | yes |
| W2-FAC-X:Thm-FAC-CS-iid | W2-FAC-B:Thm-FAC-CS | yes |
| W2-FAC-X:X10 | W2-FAC-B:L5@proof:L5.3 | yes ((C3) part; and X10's (G4) text narrowed at :21) |

## 2. Edges from outside the batch

| dependent (state) | → uses | what it uses | verdict |
|---|---|---|---|
| W2-UNI:F-UNI (SUSPECT) | W2-FAC-A:Prop-F-FAC@proof:FACA L7 Steps 1-2 | delivery steps | **clear once F-UNI v2 lands.** F-UNI v2 (`FUNI_NARROW`, DIFF PASS) has the same two clauses, so the narrowed F-FAC steps cover it. |
| W2-APP:Family-map (ACTIVE) | W2-FAC-A:Thm-FAC-L | applicability table; its span says "none is a delivery claim" (`W2-APP/lemmas/L4_families.md:152-171`) | **clear** |
| W2-FAC-S5:L5.C3-R (ACTIVE) | W2-FAC-B:L5@proof:L5.1 | (H0) | **clear** |
| W2-FAC-X:X6 (ACTIVE) | W2-FAC-B:L5@proof:L5.2 | the 𝒦_n event (consistency) | **clear for this edge**. X6's span 48-50 is (C3). Its `short` mentions delivery: recorder edits it to "delivery: see X6.X6.4". |
| W2-FAC-X:X6.X6.3 (ACTIVE) | W2-FAC-B:L5@proof:L5.2 | 𝒦_n | **clear** |
| W2-FAC-X:X6.X6.4 (ACTIVE) | W2-FAC-B:L5@proof:L5.4 | delivery. Its own span `X6_assembly.md:58-61` extends Proposition F's classes to model R "with exactly Proposition F's method … premises and allocation", and its proof `:65` asserts "for every admissible n ≥ 3, P(no output) = 0" under IDEAL-W | **stay SUSPECT — candidate for the same NARROW** (not in the sweep's 17) |
| W2-FAC-X:X7 (ACTIVE) | W2-FAC-B:L5@proof:L5.4 | Corollary FAC-NCS (`X7_near_cs_loadings.md:19-20`): "(C1)–(C4) of STATEMENT v3 hold for (R)", including (C4) delivery | **stay SUSPECT — candidate.** The related row **W2-FAC-X:Cor-FAC-NCS** (`STATEMENT_T2.md:64-69`, same (C1)–(C4) transfer) is also a candidate. |
| W2-FAC-S5F:C4 (already SUSPECT) | W2-FAC-B:L5@proof:L5.3-L5.4 | "delivery P(Ŝ⁺ = S₀) → 1 under Proposition F's premises (exactly as FAC-B L5.3–L5.4)" (`W2-FAC-S5F/STATEMENT.md:96-99`) | **stay SUSPECT — candidate** (its asymptotic delivery needs A:IDEAL-W⁺) |
| HQ_AUDIT-W2:B1 (ACTIVE) | W2-FAC-A:Prop-F-FAC, Thm-FAC-L | red-team verdict "Theorem FAC-L and Proposition F-FAC survive …" (`B1_facA_redteam.md:1-5`) | **stay SUSPECT — candidate**, the same kind as A3 (an audit verdict that the unnarrowed delivery statement holds). Narrow form: "survive, as narrowed 2026-11-16". |
| HQ_AUDIT-W2:B3 (ACTIVE) | W2-FAC-B:Thm-FAC-CS | verdict "no FATAL or MAJOR defect … in … (C4)" | **stay SUSPECT — candidate** (as B1) |
| HQ_AUDIT-W2:B4 (ACTIVE) | W2-LOC2:F-LOC2 | verdict "no counterexample to … F-LOC2 under their stated inherited premises" | **stay SUSPECT — candidate** (as B1) |
| W3-RM:Examples (already SUSPECT) | W2-UNI:UNI-0@stmt (E-R1) | UNI-0's design class (Form R families), not delivery | **clear w.r.t. this batch.** It is SUSPECT for other reasons, which this batch does not lift. |
| W3-RM:SAND-R (already SUSPECT) | W2-UNI:UNI-0@proof:UNI L2_k0 §3–§6 | the sandwich proof, not delivery | **clear w.r.t. this batch** (as above) |

Other registry files:
- **aliases.tsv:28-30:** `F-GROW` → HQ_AUDIT-W1C:A2 and `A2` → A2. These are covered by the A2 narrowing. FINAL s6's
  F-GROW text is a separate candidate (IMPACT.md).
- **HEADLINE_CANDIDATES.md:20-28** lists Thm-FAC-L, Prop-F-FAC, Thm-FAC-CS, Thm-FAC-CS-iid and F-LOC2 (all "@1.0.0"). After the
  rehash these become @2.0.0, and the delivery parts carry A:IDEAL-W⁺. HQ's card reach is rows 3.1/3.2 delivery only (HQ_DECISIONS
  11-16 ~07:20).
- **sharpness.tsv:80-87:** Prop-F-FAC × assumptions rows. Add a row for Prop-F-FAC × A:IDEAL-W+ (and for the other 18): "NECESSARY
  for the unrestricted every-n clause (TR1 §1 counterexample, n* = 2^(10⁶)); not needed on 𝔇".

## 3. Counts

- **Dependents outside the batch: 13 rows.**
  - **Clear: 7:** F-UNI (with v2), Family-map, S5:L5.C3-R, X6 (edge), X6.X6.3, W3-RM:Examples, W3-RM:SAND-R. The last two are clear w.r.t. this batch only.
  - **Stay SUSPECT: 6:** X6.X6.4, X7, S5F:C4, B1, B3, B4.
- **Edges inside the batch: 10, all covered.**

**Further candidate rows (not registry dependents but the same every-n sentence):**
- W2-FAC-X:Cor-FAC-NCS
- FINAL s6 Proposition F (corrected) and F-GROW text (IMPACT.md)

A follow-up NARROW batch of the same form covers all of them: X6.X6.4, X7 / Cor-FAC-NCS, S5F:C4 and B1/B3/B4.
Recommend HQ add them to this batch's recording or to a second batch before Friday.
