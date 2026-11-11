# W3-RM — ASSUMPTION MAP (sharpness gate, PROTOCOL item 3; registry input, PROTOCOL item 7)

Version 2 (STATEMENT v1.2; rewritten after sweep R08 findings 1, 2, 7, 9, 20). Where each assumption enters the
proof, and what is known about weakening it. "Needed by the route" means: used by the present proof (Sand ∩ NA ∩ TL
+ pathwise reporting). No cell asserts necessity for the conclusion unless a proof is cited; the evidence is in
`SHARPNESS.md` (same section numbers) and `numerics/SUMMARY_SHARPNESS.md` (ids V1, L1, L2, N1; observations only).

## Proof sketch
RM-0: start mode S̃₀ ∈ [S₀, Q] (Sand); on the lattice no addition improves F (NA) and no truth-removing move improves
F (TL) ⇒ LS0's best neighbour is always the deletion of an extra ⇒ S₀ scored after |S̃₀ ∖ S₀| moves (cap never
binding) ⇒ if S₀ is the F-maximiser (sufficient: π(S₀) > ½) every output run reports S₀. Sand: (i) size ladder — an
element outside Q costs ½ log n + log(p/k) in γ₀ and only noise ≥ that can pay for it; (ii) truths in; (iii)
outside columns out.

## Map (ids as in STATEMENT §3)

| id | assumption | enters at (bridge) | what it buys | status of weakening (see SHARPNESS) |
|---|---|---|---|---|
| T1-F | (H0) = T03♯ hypotheses | B6 [POST]; RM-0(b); its components: energy ‖μ‖² ≤ Mn and p ≤ n^A → B2, B3, B4, B5; BM-∞ → B3 under (N-χ) | π(S₀) > ½ w.p. → 1, hence S₀ is the F-maximiser | sufficient input; the pathwise argument needs only "S₀ is the unique F-maximiser among scored models w.p. → 1"; necessity of T1/POST not established (§5) |
| T1-R | (A1-post) = LSF of APP L1_POST(b) | B9 [POST] | as T1-F under the joint law (p = 1 treated directly) | as T1-F |
| FL-16 | floor on all ≤ 16-sets | B1, B2/B2τ | block tables behave like regressions | used; weakening not studied |
| FL-Q | floor on Q ∪ {l} | B3, B4, B5 | lattice regressions well-posed; truth removal costs ≥ nφ₀²θ²_min | used; weakening not studied |
| FL-R | population floor on sets ≤ 16 + s₀ and on Q ∪ {l} | B7 (small sets only), B8a, B8b (Q ∪ {l}) | sample floors; conditional variances | B7 does not use the Q ∪ {l} part (R04 F3) — a bridge-specific surplus, not a weakening of the theorem |
| V | δ²_{U,j} ≥ M_n log n, all \|U\| ≤ 15 | B1, B2/B2τ (truth inclusion at U = S̃ ∩ C_b ∖ {j}) | truths enter the start mode | sufficient; successful masked designs exist (GEN, PXN; V1); block-relative joint visibility recorded (R02 P4); worst-case converse open (§2) |
| V-R | PTV(a₀) | B7 | sample visibility uniformly over \|U\| ≤ 15 | as V |
| "15" | conditioning size | = B − 1, block cap 16 | covers every possible set of block-mates | B1/B1′: equivalence with "block-relative for every partition"; not a necessity theorem (§1) |
| L-gain | δ²_{U,l} ≤ ητ²_U log n off Q, τ²_U = σ² + ‖(I − P_U)μ‖²/(n − 1) (v1.1: σ²) [P2] | B1, B2τ (ladder, junk exclusion) | outside columns do not enter the start mode | η < η_A sufficient; converse heuristic only (§3.1; L2) |
| L-gain-R | leak ≤ C_L n^{−1/2} | B7 (spherical tail) | bounded mean shift | o(√(log n/n)) (R04 F6) and the η-budget (R02 P3b) recorded, not adopted |
| L-loc-R | decorrelation at rate r_n = o((n log n)^{−1/4}) outside H_l (v1.1: n^{−2}) [P3a] | B7 (selection removal) | n^{o(1)} references per column despite the X-measurable partition | used by the route; removal open (§3.3) |
| L-size | \|Q\| ≤ (log n)^κ | B2 (needs only log\|Q\| = o(log n)), B3, B5, B7, B8 | union bounds over the lattice | successful designs with larger sets exist (LOC2 L6, UNI-1; L1); polynomial \|Q\| recommended (R02 P5) (§3.2) |
| L-feas | \|Q\| ≤ K, and Q = [p] or K ≥ 2\|Q\| + 32s₀ + 1 | B2/B7 (ladder end; adding a truth is feasible); through \|Q\| ≤ K also B3, B4, B5, B8a, B8b and RM-0 (the lattice is feasible) | start mode not forced to size K with extras | used; FAC-PK (NEG) is a failing class with saturated start modes and K < p — an existential obstruction for LS0, not a necessity statement (§3.2) |
| N-χ | \|Q ∖ S₀\| ≤ (1 − δ₀) log n | B4 | NA by one common χ² charge | sufficient; optimality of the common-χ² bound for actual residual families not established (§4) |
| N-D(i) | ≤ p·n^h approximating directions, h < ½ (v1.1: p·n^{o(1)}) [P1], error ρ_n | B5 (NA-F) | NA for polylog Q in fixed design | sufficient; not established from (V)+(L); whether needed for the conclusion open (§4; N1) |
| N-loc | each column's dependence on the lattice carried by ≤ ν_n members, ν_n log 2 ≤ h log n | ⇒ N-D(i) (`lemmas/L2_NAF.md`) | a checkable sufficient form | — |
| BM-Q | θ*²_min nφ₀²/(σ²(\|Q\| + log n)) → ∞ | B3 | TL at the lattice scale | follows from BM-∞ when \|Q\| = O(log n); needed by the toolkit bound at polylog \|Q\| |
| D-R | NA-R (R1)–(R3) with latent extension | B8a | NA for Gaussian rows | as N-D(i); entropy budget h < ½ for (R1) recommended (R02 P1) |
| D-loc | N_l with ℓ¹-bounded regression remainder and variance ratio | ⇒ D-R (`lemmas/L4_formR.md`) | a checkable sufficient form | — |
| E4 hyp. | (H1⁺), (H2) = EX-A, (H3), (H4) | Lemma E4 | LS0 centre is a maximiser | binary64 outside scope (N3 (e), PACK UM-FP) |
| run premises | EX-A, EX-S, SR, GUARD-W, OP-LS0 (+ configuration), complete scans | RM-0(b), E4 integration | scored set and reported model as specified | IND-T and the c₄ search are execution conventions and do not enter (C0)–(C2); CAL is not used by the pathwise form |

## `implies` relations (for the registry)
* (L-gain^σ) ⇒ (L-gain) [τ-form]; (N-loc) ⇒ (N-D)(i); (D-loc) ⇒ (D-R); BM-∞ ∧ |Q| = O(log n) ⇒ (BM-Q);
  (N-χ) ⇒ |Q| = O(log n); λ_min(Σ_n) ≥ c ⇒ (T1-R) ∧ (FL-R).
* (FL-16) ∧ (V) ∧ (L-gain) ⇔ [(G3a) ∧ (V_b) ∧ (L_b) for every partition into blocks ≤ 16] (Lemmas B1, B1′).
* Theorem GROW's hypotheses (block-relative, σ-form, |Q| ≤ C log n, (G4-χ) or (G4-dir)) ⇒ the block-relative variant of
  RM-F; RM-F ⇒ GROW's conclusion with e4 discharged. Theorem PLR's hypotheses with Sand supplied by SAND-R ⇐ RM-R's
  hypotheses. UNI-0's class ⇒ RM-R's hypotheses (with (D-loc)); LOC-BF's class ⇒ RM-R's hypotheses (with (D-R)).
  GROW (C5)(a) and GEN (C6)'s design ⇒ RM-F's hypotheses (`lemmas/L7_examples.md`, `SHARPNESS.md` §3.2).

## Why Form R is not Form F conditional on X
Under Gaussian rows a block that contains no truth still sees the signal of the truths in other blocks as an extra
N(0, v) term; heuristically (an order-of-magnitude argument for the maximum of p Gaussian projections, not a proof)
the sample δ_{U,l}/τ_U then has maximum over p columns of order √(2A log n)·√(v/(σ² + v)), which is not below
√(η_A log n) in general. The method is not hurt (the add statistic is RSS-normalised and behaves like a t-type
ratio); Form R therefore keeps population conditions and the spherical argument. A distributional (counting) version
of (L-gain) that would cover both forms is recorded in R02 (P2, last paragraph) as a separate ticket.

## Outcome of the "better theorem" review (R02; `reviews/R02_disposition.md`)
Adopted: [P1] entropy budget h < ½ (Form F), [P2] τ-normalised leakage, [P3a] localisation rate, [P7] archive
corollary. Recommended to HQ: polynomial |Q| (P5, highest value), leak budget of order √(log n/n) in Form R (P3b),
joint block visibility (P4), entropy budget for NA-R (P1). Open: dropping (N) (P6); removing localisation.
