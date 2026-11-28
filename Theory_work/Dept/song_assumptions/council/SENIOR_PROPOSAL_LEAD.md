# Stage 2 — Lead's convergence proposal (Proposers' response to SENIOR_FABLE.md and SENIOR_ASTRA.md)

This is the single discussion round, capped by the owner and Manager.

- **Proposers:** the Task Lead (Opus 5.5), with the original drafting advisors Fable 5.2 (`advisors/FABLE_R1.md`) and Astra 6.2 (`advisors/ASTRA_R1.md`, `ASTRA_R2.md`).
- **Final Council:** the fresh senior judges, Fable 5.2 (`council/SENIOR_FABLE.md`) and Astra 6.2 (`council/SENIOR_ASTRA.md`).
- **How the round runs:** the advisors comment on this proposal. The Lead then applies the agreed text as v1.4, and the Final Council gives one sign-off pass.

Notation for this proposal:
- T = S0 and s = |T|. A ⊊ T is retained, D = T∖A ≠ ∅ with d = |D|, and N is a null set with |N| = m. S = A ∪ N.
- R_n(S) = n·E[(x_Dᵀβ*_D − L(x_Dᵀβ*_D | x_S))²] is n times the population **linear projection error** of the omitted signal on x_S. The Schur-complement formula n·β*_Dᵀ Σ_{DD·S} β*_D holds for any finite-covariance design.
- ϑ(A, N) := 1 − R_n(A ∪ N)/R_n(A) ∈ [0, 1] is the **leakage**: the share of the omitted signal that N explains.

## 0. Points both judges agree on (adopted without discussion)
| # | change | source |
|---|---|---|
| 0.1 | **No S1/S2 number or design family in any statement.** All of them move to the Defence (b) blocks, SIMULATION and the DOSSIER "holds on our data?" items. The D4 rationale is rewritten: the form is chosen on generality grounds, and S1 is then checked against it. | F C-2; A §3 |
| 0.2 | **Credit constant C = 1 by convention**, with the multiplicative constant carried in the tight remainder. The "C ≍ (s0+1)² ≈ 121" claim is withdrawn, and E9b's C = 121 column becomes a sensitivity setting. The single-rival price Pr_n(d, m) and the summed class bound B_Dm are distinguished. | A C-1; F C-3(iii); Sol R3-2 |
| 0.3 | **E9/E9b are qualified.** E9b selects 3 deletion sets D per (cell, d, m) by population residual; these are selected examples. Four designs at zero slack establish no 1 − o(1) event. E9b is rerun with the raw-centred mean μ: d = 1 is identical, and d = 2, 3 change by at most 0.0015 (`tables/e9b_width_ext_s1.tsv`; v1 kept as `_v1_codedmu`). Minima are quoted exactly (2.386, not ≥ 2.39). | A C-2; Sol R3-1/3; Neon R3 |
| 0.4 | **Missing SL counterparts are added to the map and the defences:** SL sparsity (3) → A-BS; the SL p. 951 cap-removal remark (Jiang (38)) → q_n is SL's r̄_n under the BB size tail; SL Condition 3's Gaussian form ch₁{var(x)} ≻ ε_n² → A-NEC; prop:dist(ii) (no floor, singleton SUBG, slower radius) and thm:dist-param → the SL-1/2/3 rows. | F C-4; A C-5 |
| 0.5 | **Two itemwise SL counterparts become explicit targets.** TS-a is stated first for any j satisfying its own margin, then jointly. A new **TM-a0-inc** states Π(S ⊇ S0^C \| data) → 1 a.s. under second moments only: full rank and finitely many underfits give a positive risk gap. It is the direct counterpart of SL Cor 2. Score moments enter only for exclusion. | A C-3; F §3 |
| 0.6 | **The TM tier is stated plainly.** A-MIS(iii) gets its primitive form: x_Oᵀβ*_O = a + x_Cᵀγ + e, with e ~ N(0, τ²) independent of x_C, so β^C = β*_C + γ and σ_C² = σ*² + τ². This is equivalent to the current statement. Pseudo-true sparsity gets a new label, **A-SPARSE-C** (\|supp β^C\| ≤ s_C fixed), with holds/fails examples (local dependence vs pervasive factors). TD-A is the relaxation. TM-a and TM-b are stated as corollaries of TD and TS-b **conditional on each admissible C**, with candidate dimension used throughout. An unconditional result needs uniform constants and almost-sure admissibility, or + P(C inadmissible). | F C-5, A-MIS row; A C-4 |
| 0.7 | **Windows are stated without proof constants.** A-SUBG and A-NEC hold on sets of size ≤ c·log n **for every fixed c > 0**; the q_n(M) and C_q forms move to the proof path. A-DIM′ becomes log p = o(√n), with the product form kept as the proof budget. A-NEC becomes a vanishing sparse-eigenvalue floor n·φ_min(c log n) ≥ c_ψ, "no faster than the ridge scale". | F C-3, table; A table |
| 0.8 | **Converse:** stated under its minimal set (A-GL, isometry and A-NEC on T, A-BS). The boundary-scale remainder is recorded: log odds = Pr_n(1) − (√λ̂ + Z)²/2 + O_P(1) at λ = O(log n). | F C-7; A C-7 |
| 0.9 | **Sieve:** classes restricted to s − d + m ≤ min(K, J) and m ≤ p − s. | A C-7 |
| 0.10 | **Evidence summaries:** E7 is described as a predictive-summary diagnostic. E1's MPM recovery and restricted κ do not test exact posterior mass. | A C-6 |
| 0.11 | **Worked cases.** The dossier promises them; v1.4 supplies closed forms of R_n, κ_n and leakage for orthogonal, AR(1), block and equicorrelated designs (F C-6). | F C-6 |
| 0.12 | **Four blocks** (Model / Design / Signal / Omitted variables) organise the assumption list in DEFINITIONS and the DOSSIER. | F §3 |

## 1. The one real design choice: the headline form of A-MARGIN-U
Both judges want a **population-only headline**, with the conditional-width form kept as a technical refinement. They differ only on the shape:
- **Fable P-U:** (U1) deletions κ_n ≥ 1+η; (U2) limited leakage on a small proxy set Q_n; (U2′) a structure-free fallback.
- **Astra:** (i) a simple diverging-ratio condition; (ii) a finite-ratio condition with the sharper geometric coefficient a = √(2(1−√(1−ϑ))).

**Lead proposal: a merged "A-MARGIN-U (population form)"** with one slack η > 0, m̄ := ⌈(2A+1)s⌉ + 1 (the range of delivered `asm:margin`(b)), and the generic price Pr_n(d) := max_{|D|=d} log[π(T)/π(T∖D)] + (d/2)·log(1+g). For BB(1, p) and g = n this is the package's Pr_n(d). For all large n:

- **(U1) Deletions.** R_n(T∖D) ≥ 2(1+η)·σ*²·Pr_n(\|D\|) for every nonempty D ⊆ T.
- **(U2) Substitutions.** There are sets Q_n ⊇ T with log\|Q_n\| = o(log n) such that, for every B ⊆ Q_n with B ⊉ T and \|B∖T\| ≤ m̄, the following hold:
  - (a) R_n(B) ≥ 2(1+η)·σ*²·Pr_n(\|T∖B\|);
  - (b) for every N ⊆ Q_n^c with 1 ≤ \|N\| = m ≤ m̄,
    √(R_n(B ∪ N)/σ*²) ≥ (1+η)·√(2Pr_n(\|T∖B\|)) + a(B, N)·√(2 log C(p−s, m)),  with a(B, N) := √(2(1 − √(1 − ϑ(B, N)))).
- **Special cases (stated, not separate assumptions).**
  - Q_n = T is the "no proxies" case.
  - Uniformly vanishing leakage outside Q_n (max ϑ·log p → 0) makes (b) follow from (a), which is Fable's (U2b).
  - Q_n = T together with a = √2 (ϑ = 1) is the worst-case fallback (Fable U2′, Astra's unit-vector bound).
- **Population sufficient conditions, shown as corollaries.**
  - (C-i) Astra: min R_n(S)/[σ*² log(p∨n)] → ∞ over feasible underfits of size ≤ s + m̄ implies (U1)–(U2) with Q_n = T.
  - (C-ii) Fable: a sparse-eigenvalue floor φ² on sets of size ≤ s + m̄ plus beta-min θ_min ≥ (1+η)(1+√m̄)·√(2 log(2p√(n+1))/n)/φ implies (U1) and the fallback.
- **The bridge (Lemma W, low risk).**
  - (W1) Fable/Astra: ⟨v_S, v_B⟩ = √(R̂(S)/R̂(B)), so w_Dm(X) ≤ max_N ‖v_S − v_B‖·√(2 log C(p−s, m)) ≤ a·√(2 log C), plus a centred term along v_B.
  - (W2) On the sparse-isometry event, the sample leakage ϑ̂ ≤ ϑ + 2δ_n with δ_n ≍ √((s+m̄) log p/n).
  - Hence the population form implies the current conditional-width A-MARGIN-U, at C = 1, on a design event of probability 1 − o(1).
  - The max over B ⊆ Q_n of the centred term is o_P(√log n), since log\|Q_n\|^{m̄} = o(log n). That term is absorbed by η√(2Pr_n) ≳ η√log n.
- **What stays.** The conditional-width A-MARGIN-U (C = 1, B_Dm > 0 classes) is kept as the **refined technical form** in ASSUMPTIONS §3.3 (a remark: "TS-b also holds under the weaker design-conditional form"). E9/E9b are labelled a diagnostic of the refined form.
- **Cost.** The population form is slightly stronger than the refined form: it gives up the containing-model credit and uses at most the factor a ≤ √2. The proof risk added by W1/W2 is low, and the TS-b steps 2–3 obligations are unchanged. On S1 as a sequence (Q_n = T plus its L_n → ∞ nearest nulls), (U1) and (U2a) hold at SNR 2 with ratio 2.51–2.77 (the exact κ_n). Distant leakage decays geometrically: 0.265, 0.087, 0.030, … at distance 1, 2, 3 (Fable's check). The fallback alone fails at SNR 2 and holds at SNR 3. Pervasive factors fail (U2) for small Q_n and fall back to the interpolated form; this is a real dichotomy, stated as such.

**Questions for the advisors (answer each briefly):**
- Q1. Is the merged form correct as written? In particular:
  - (b) uses a common base B for each class;
  - (a) uses the "same constant 2" deletion price for B containing proxies, giving up the cost of added proxies;
  - the uniform-over-B centred term.
- Q2. Is the coefficient a(B, N) = √(2(1−√(1−ϑ))) the right one (Astra), or should we display Fable's simpler 2√ϑ bound?
- Q3. Should A-MARGIN-H be a **diverging ratio** (Fable: inf R/(σ² log n) → ∞; conclusion for every M; same form as `asm:omitted`(c) and Luo–Chen), or a **fixed constant C_L above the inverse Hellinger conversion constant** with the sieve defined once (Astra; sharper)? The Lead proposes the diverging ratio as the headline, with a remark that a fixed large constant suffices at a fixed level M.
- Q4. A-BS′: should it use Astra's exact equivalent pair (Var(xᵀβ)/σ² bounded, and Σ β_j² Var(x_j)/(nσ²) → 0), or Fable's target form (the bounded population R² only)? The Lead proposes stating Astra's pair as the recorded alternative and Fable's as the open target. Its status stays "recorded, not adopted".
- Q5. Anything in §0 you object to, or anything missing that a referee would ask about first?

## 2. Also folded into v1.4 (Round 3 leftovers; superseded R3, but correct)
- The D4 overclaim ("margin holds there") is removed.
- DOSSIER A-NEC: the SBJ duplicates clause is removed and the NH14/SBJ bullets are split; DOSSIER l. 191 "ordinary correlated designs" is fixed.
- TD′: q_n ≍ min{p, (s+1)M log₂(p√n)} everywhere.
- E2 reading: "the ratio is ≥ 1 in 9/136 (max 1.74)".
- §3.2 step 2: \|S ∪ S0\| ≤ min(p, s0+J) ≤ q_n.
- Notation is aligned with the manuscript spec: coded coefficients θ_S/θ*, raw β*.
