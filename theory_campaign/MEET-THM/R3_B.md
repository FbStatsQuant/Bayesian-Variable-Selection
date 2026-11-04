# Round 3, Seat B (Fable 5.1, Claude Work, high)

Verbatim final message, extracted by the chair from `/home/fb31/.claude/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/af57f95a-fc3f-4f95-807d-d6e888de321b.jsonl` (completed 2026-11-04 04:59 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

The local check passed: on the Dε design with the method's own partition, δ_A and δ_H are exactly linear in ε, b_X and D_* obey the explicit Lipschitz constant in all 75 pairs × 5 seeds, and the per-stage χ² transfer between two nonzero ε values held with the four-normaliser modulus (0 violations). I now have everything the brief asks for and am writing the Round 3 answer.

# MEET-THM · Round 3 · Seat B

**Read:** ROUND3_BRIEF; SYNTH_R2 v2 (§0–§6); HQ rulings Q1–Q4 and Q5; W2_PC1 and W2_PC2 VERDICTS (all rows on A, B, D and C); W1_PC1 §§1–5, 16, 20 and W1_PC2 shared objects, clusters 3–4; CHK_INHERITED §§1–6; R2_A, R2_C, R2_D in full; my R1_B (§A, §D D1–D3, §E, §F, §I) and R2_B; DOSSIER §4, §5, §9; HQ_QUESTIONS, STATUS, FUTURE_WORK; THEOREM_REVISION_INPUTS N1–N17; THM-INV §1. Citations: `W2PC1 B.R3(a)` = a row of `evidence/W2_PC1/VERDICTS.md`; `W2PC2 C2(a)·split` likewise; `W1PC1 §3`, `W1PC2 D5`, `CHK §4`.

**One local check (scratch directory, PC2's `bvs_common.py`, 0.9 s, 5 seeds).** Dε (n = 40, p = 8, pairs within .6, β₀ = .25, β₄ = .2, σ = 1, K = 8, B = 2, method's own partition), data fixed at ε = 0 and the cross-block pattern scaled as E = εE₁, ε ∈ {0, 10⁻⁵, 10⁻⁴, 10⁻³, 3·10⁻³, 10⁻²}:

```
seed  dA/eps  dH/eps  lin-dev  a     bX(1e-2) D*(1e-2)  L(bX)   Lip(d_X)  |dX|<=bX
0      3.691   3.749  1.2e-15  0.201  0.4997  1.502     51.41     14.02  True
1      3.691   3.749  1.2e-15  0.252  0.5671  1.982     58.51      8.47  True
2      3.691   3.749  1.2e-15  0.379  0.7855  3.892     81.62      8.77  True
3      3.691   3.749  1.2e-15  0.494  1.0800  6.995    113.19      9.89  True
4      3.691   3.749  1.2e-15  0.187  0.4836  1.398     49.72      3.51  True
pairs: 75  Lipschitz violations b_X: 0  transfer violations (4 sup|d-d'|): 0
```

Reading: δ_A(ε) = εδ_A(1) and δ_H(ε) = εδ_H(1) exactly (homogeneity); b_X(ε) and D_*(ε) satisfy |b_X(ε) − b_X(ε′)| ≤ L|ε − ε′| with the constant L stated in card M2 (b7); the empirical Lipschitz constant of sup_S|d_X(S; ε) − d_X(S; ε′)| is 3.5–14, far below L; and |log(1+χ²(q₁‖q₀))(ε) − (·)(ε′)| ≤ 4 sup_S|d(·; ε) − d(·; ε′)| in every pair. A route check of (b7), not evidence of a theorem.

---

## §S1 Confirm or object

### SYNTH_R2 §2.1 (main)

| Item | Confirm / object | Reason (only if object) | What would change it |
|---|---|---|---|
| M1 Theorem V/H, one theorem with clause (a) = validity | confirm (R3-2: one) | — | For Seat A's card: separate the two RB statements (W2PC1 B.M1(b) AMBIGUOUS): the weighted identity E[Ẑ_r PIP̂_rj\|𝒞] = Z·PIP_j needs no terminal stationarity; the stationary-start qualification attaches only to the unweighted N9 corollary E[o_j] = q_φ(j ∈ S). |
| M2 Theorem WS, parts (a)(b)(c) | confirm | — | My card §S2 adds the Q5(1) Lipschitz constants as clause (b7). |
| M3 START | confirm | — | "zero iff at most one block has positive fit fraction" (W1PC1 §5 zero case; W2PC1 B.M4). |
| M4 Z𝒯 + certificate + masked statement | confirm | — | My card §S2; K95 cited, supplement. |
| M5 HPM, K70 labelled variant, K63 hypothesis | confirm | — | Audits (LS0/GUARD-W/emitted centre) stay named implementation premises (W2PC2 C3 NOT REPAIRED). |
| M6 SEP + Lemma KL | confirm | — | — |
| M7 STG main (K26, K25, K27, K30; K28 cited) | confirm | — | K33 only in its deterministic termination/count form (R3-4); K29 not in STG (R3-8). |
| M8 open slot | choose (i), Proposition D in main | — | See R3-1. |
| SL (K97) → FUTURE_WORK | confirm | — | R3-3. |
| Thesis CD → remark | confirm | — | — |

### §2.2 (supplement)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| S-T (K93, K04) | confirm | — | Onset n ≳ 2·10⁶ and "PROVED-LOCKED (wave 3; external review queued)" printed. |
| S-D (K87–K90, K06, K64) | becomes M8 under R3-1(i) | — | If Round 3 picks (iii), S-D as proposed. |
| S-Z (K37–K41, K53) | confirm | — | Terminal-off clause in exception-probability form ≤ 2√δ₁ (W1PC1 §15); (vii) with D = osc_Ω d ≤ D_*; novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 to the citation checker. |
| S-TARGET (K01–K05, K76, K95) | confirm | — | K02 tie caveat; 2νb₀; K95 with η < 1 (W1PC1 §20 B.D17). |
| S-KERNEL (K20, K21, K08, K09, K22, K103) | confirm | — | CHK §5 amendments verbatim; N3 OPEN carried as hypothesis; K23 to FW (R3-4). |
| S-CERT (K64, K73, K74, K05, K108) | confirm | — | K73 without the region-certificate clause (C:44; W1PC2 D5 region GAP); K107 → FW. |
| S-LIM (K79, K81, K100, K101; K99 remark) | confirm | — | Duplicate clause: PIP = E[#selected in group]/d; 2/3 only for p = 2 (W2PC1 B.S6). |
| S-POOL (K49, K50, K54, K56, K57) | confirm | — | K57: the proved P1 (bias ≤ TV of the one-record marginal) ships; the general fixed-budget equal-weight accuracy statement → FW (C:28). Both. |
| S-IDENT (K25, K104, K55, K103) | confirm, with one addition | — | Name C15-CI (posterior-content error of size-cell credible sets, W2PC2 C15-CI TRUE-AS-WRITTEN) explicitly; it is the HQ Q2 deliverable (§S4). |
| S-BLOCKS (K07, K14, K06) | confirm | — | Preservation only; equality under SIZE g_max ≤ B < 2g_min. |
| S-OUT (K77, K78, K83–K86, K63) | confirm | — | K86 cited inside M1's frozen-𝒞 contract, K63 inside M5's hypotheses, neither a numbered main clause (R3-4). |
| S-STGI (K29 conditional on (LL); K30 ideal) | **object on K29** | (LL)/the over-tilted q_w bound is not a model/design condition and no family satisfying it has been exhibited (W2PC1 A.S11: DESIGN-ASSERTED, GAP). IC3 fails; a list item cannot be conditional on an unexhibited hypothesis. K30 is already M7(d); state it once. | An exhibited design family satisfying (LL), checked in one wave: then K29 returns as a supplement clause. Until then FUTURE_WORK. |
| S-REP (Ĵ, ε̂_×) | confirm | — | C16's bound labelled vacuous at R′ = 4 (W2PC2 §0). |

### §2.3 (the §5.3 package)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| (a) hypotheses, definitions, decomposition, divergences, η-form alternative | confirm | — | Cited in my card rows (a1)–(a3). |
| (b) per-stage χ², transfer, first-stage variance, Doeblin, M₂ ≤ e^{D_*} | confirm | — | M₂ is an upper bound only, no e^{cη} comparison to the BO M₂ (§3 A.R3(b)(iv)). |
| (b) stage count: sandwich with its scope; local constancy; integer bound and envelope; checked fallback | confirm | — | — |
| (b) Q5 condition (1) as statements; Lipschitz constants where supplied | confirm; constants supplied | — | Card M2 (b7): explicit L on the fixed-partition family E = εE₁; local check above. |
| (b) Q5 condition (2) sentence | confirm, verbatim | — | — |
| Removed: A zero range, D jump corollary, B "every constant tends to BO value" for T, A growth exhibit | confirm (my sentence conceded: W2PC1 B.R3(b) continuity NEEDS-HYPOTHESIS) | — | — |
| (c) WS6(d), WS7 with CHK amendments | confirm | — | — |
| Scale disclosure (ε ≲ n^{−1/2}/p; sharp necessity FW) | confirm; my NEC conceded (W2PC1 B.R3 NEC COUNTEREXAMPLE) | — | A necessity statement with an effective beta-min and a scale-dependent remainder, checked: then a supplement proposition. |
| IC3: C's family at 1/(np) and at n^{−1/2}/p; A/B/D finite exhibits as component checks | confirm | — | — |
| Leakage clauses (F), (S) → supplement corollary | confirm (R3-5) | — | — |

### §2.4 (FUTURE_WORK and drops)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| K13, K24, K23, K31, K58, K59, K71, K75, K92, K82, K94, K99-quant, K107, K80 → FW with the stated reasons | confirm (K23: concede FW, no consumer; K80: my position) | — | A consumer for K23 in paper 2 (N10 route). |
| Scope: N12 exponential p; Hellinger/predictive contraction | confirm | — | — |
| New: SL analytic separation; sharp ε-scale necessity | confirm | — | — |
| Add: K29 (R3-8); K57 general fixed-budget equal-weight accuracy (C:28) | add | Both lack IC3/route as list items (above). | — |
| Drops K12, K34, K66, K67, K91, K98 with reasons | confirm | — | — |

### §2.5 (run card)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| Ĵ in the B/C/D form; label "post hoc Monte Carlo estimate"; C16 bound | confirm (R3-6) | — | A's trapezoid form as a supplement alternative only with pre-resampling particles and incremental weights specified (W2PC1 A.R5(i) AMBIGUOUS/GAP). |
| My T5 ("masked regime shows as a large Ĵ") | concede: retain only as a statement about J (W2PC1 B.R5(i) T5 AMBIGUOUS) | — | An estimator-error bound in the masked regime (none expected). |
| ε̂_× `cross_block_rmax`; κ̂; δ̂ = (K−1)ε̂/κ̂ (D's form); ū̂; η̂ "n/a" outside the domain | confirm | — | — |
| Theorems ε_S ≤ (\|S\|−1)ε̂/κ̂; sup\|d − d_σ\| ≤ η(δ̂) on κ̂ > 0, δ̂ < 1, ū̂ < 1, δ̂ū̂ < (1−δ̂)(1−ū̂) | confirm; my T2 repaired exactly so (W2PC1 B.R5(ii)) | — | — |
| Drop D's T6 and V rescaling | confirm | — | — |
| Implementation note: read-only accumulator | confirm; d is a function of (X, y, blocks) fixed before stream 10, so it is a default declared summary (drafting note for AMENDMENT_HQ_02, §S5) | — | — |

### §2.6 (growth rates)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| (i) R′_n = 4⌈log₂(n+p+1)⌉ (D's form), fixed finite set of summaries, families with D_* = O_P(1) | confirm (my ⌈log₂(n+p)⌉ withdrawn for D's) | — | — |
| (ii) R′_n = 4⌈(n+p)⁶/4⌉ for ≤ (n+p)² summaries | confirm; print PC2's note that (n+p)^{4+δ} suffices and that s⁶ is computationally meaningless | — | — |
| No growth for ℓ, L, N; shipped R′ = 4 carries fixed-R statements only | confirm | — | — |

### §2.7 (safeguards)

| Item | Confirm / object | Reason | What would change it |
|---|---|---|---|
| §13.1 escalation if N1 cannot be closed | confirm | — | — |
| §5.3 escalation if both routes fail; orthogonal-only substitute does not close it | confirm | — | — |
| §5.4: Q3 fallback set + masked statement in M4; FW2 not binding | confirm | — | — |

### §3 (repairs)

| Row | Confirm / object | What would change it |
|---|---|---|
| A.R3(b)(iii) zero range → max{1, ⌈·⌉} | confirm | — |
| A.R3(b)(iv) M₂ upper bound only | confirm | — |
| A, B, D necessity propositions removed → FW | confirm (mine conceded) | — |
| A.R3 growth exhibit → C's family | confirm | — |
| B.R3(b) continuity sentence → local constancy at non-critical thresholds | confirm (card M2 (b6′), (b8)) | — |
| D.R3(b)(iii) jump corollary → integer interval | confirm | — |
| SL cards NOT REPAIRED → FW | confirm | — |
| B.R4 M₂ aside removed | confirm (card M4 omits it) | — |
| B.R5(ii) T2 domain | confirm (as above) | — |
| D.R5(i), D.R5(ii) removed | confirm | — |
| A.S9, B.S6 duplicate limit: PIP = E[#selected]/d; 2/3 for p = 2; 3/5 with an orthogonal null | confirm (PC1 also notes the two-duplicate/orthogonal-null limit p/(2p−1)) | — |
| D.M3′ status: restore MZ-C1 "candidate, not reviewed, not adopted", AUTHOR-ONLY | confirm | — |
| C3, C7 audits as named implementation premises in the charters | confirm | — |

### R3-1 to R3-8

| # | My choice | Reason (≤ 60 words) |
|---|---|---|
| R3-1 | **(i) Proposition D in main** (I move from supplement) | IC5: objectives are ordered and (2) is second; with (i) in the supplement no main statement serves it. (ii) duplicates M1(a) (IC4: cited lemmas). Prop D ships as a Proposition at island level, execution DAG as a named premise, K90 a remark, and composed with M2(b5) and H(b): depth is free of R′, error falls in R′. |
| R3-2 | One theorem V/H | IC4: V's cited content is lemmas; N1 and the frozen-𝒞 contract are clause (a) of H. Avoids a main card that is mostly KNOWN—CITE. Add the RB-wording separation above. |
| R3-3 | SL → FUTURE_WORK | My S1(b) is NOT REPAIRED (W2PC1 B.S1): the iteration-uniform null-BF/prior-odds step is an unproved hypothesis about SL's algorithm (ground rule 6). LIT-PAR G4 cited as numerical evidence, labelled. Changes with a checked SL-prior lemma. |
| R3-4 | K63/K86: cited in hypotheses, S-OUT; K23: FW; K80: FW; K12/K34: drop; K33: STG clause in its deterministic termination/count form only; K95: supplement | K33's rebuild-convergence content stays FW (N5(b)); K95 is a one-line odds certificate with η < 1, cited from M4. |
| R3-5 | (F), (S) → supplementary leakage corollary (I concede) | They are non-perturbative and at a different scale; not part of HQ's (a)(b)(c); the main card is long. The m-form of (S) and (F) go together; (b5)'s pathwise bound stays in M2. |
| R3-6 | B/C/D Ĵ form | TRUE-AS-WRITTEN T1–T4 (W2PC1 B.R5(i)); PC2 unbiasedness check; A's form AMBIGUOUS/GAP. |
| R3-7 | Thm 2: C's "fixed-design, fixed-sparsity selection counterpart only; their predictor-tail and prior hypotheses are not transferred" (I move from "not applicable"). Cor 2: C's "no analytic null-exclusion/FDR separation established", adding "LIT-PAR G4 numerical evidence cited, labelled" | My wording and C's say the same thing; C's is a coverage-matrix entry. With SL in FW, D's "only if it ships" is moot. |
| R3-8 | K29: FW (object, above). K30: main M7(d), labelled ideal two-state grid, stated once. K27: main M7. K57: proved P1 supplement, general accuracy FW. K70: labelled no-LS0 variant clause of M5. K73: supplement without region certification. | Reasons in the §2.2 rows. |

---

## §S2 Final cards

### Card M2 · Theorem WS, the §5.3 package · K102, K10, K11, K25, K53; K103/K104 as used; K27 cited for the count; part (c) = Proposition ONE-SHOT (OWS-WS6(d), OWS-WS7)

| Field | Content |
|---|---|
| Setting (model/design; everything computed from (X, y) and the built blocks) | Standardised X, centred nonconstant y, n ≥ 3, p ≥ 1; shipped target (g = n, IG(a₀, b₀), capped BB(1,p), K = min(p, ⌊n/2⌋)); blocks C₁..C_J as built by the method from X; tables r_b from the same (X, y); Ω = {\|S\| ≤ K}; d = log BF − Σ_b log r_b; q_t ∝ γ₀e^{td}; G = XᵀX, G_D its block-diagonal part, E = G − G_D, A_D = G_D + I, H_D = (n+1)G_D + I, z = Xᵀy, Q̄ = 2b₀ + yᵀy, ν = a₀ + n/2 (C:50, 63). |
| H-DOM (matrix domain) | a := nzᵀH_D⁻¹z/Q̄ < 1; δ_A := ‖A_D^{−1/2}EA_D^{−1/2}‖ < 1; δ_H := ‖(n+1)H_D^{−1/2}EH_D^{−1/2}‖ < 1; r := δ_Ha/[(1−δ_H)(1−a)] < 1. C_σ := νa²/[2(1−a)]; b_X := (K/2)[−log(1−δ_A) − log(1−δ_H)] − ν log(1−r); D_* := C_σ + 2b_X; x_b, d_σ(S) := ν[Σ_b log(1−x_b) − log(1−Σ_b x_b)] (C:64–65). |
| Implementation premises (named, not model conditions) | EX-A exact arithmetic; EX-S/H-U exact start sampler and ideal uniforms (for (b3), (b5)); CAL: a successful calibration record 𝒞 frozen on streams 0–9; R′ = 4k declared before stream 10; kernels as coded under N9's sufficient conditions; for (b5)–(b6): ESS .9 for pilot and grid, 2⁻⁶⁰ bisection, 10⁻¹² snap/validation, a successful grid (no ceiling/snap failure), 2⁻⁶⁰ ≤ h/2. No output clause, so GUARD-W is not used. |
| (a1) Decomposition | Under H-DOM, for every S ∈ Ω: d(S) = d_σ(S) + d_X(S) with 0 ≤ d_σ(S) ≤ C_σ and \|d_X(S)\| ≤ b_X; hence osc_Ω d ≤ D_*. The σ²-coupling term C_σ survives E = 0. [W2PC2 C2(a)·split TRUE-AS-WRITTEN, 104 domain designs; W1PC2 D14·deterministic bound; W2PC1 B.R3(a) TRUE-AS-WRITTEN] |
| (a2) Divergences | Under H-DOM: KL(π‖π₀) ≤ D_*, KL(π₀‖π) ≤ D_*, J := KL(π‖π₀) + KL(π₀‖π) = E_π d − E_{π₀} d ≤ D_*; TV(π, π₀) ≤ tanh(osc d/2); 1 + χ²(π‖π₀) ≤ e^{osc d}. [W2PC2 C2(a)·divergences; W1PC1 §16 KL/TV rows TRUE-AS-WRITTEN] |
| (a3) Block-orthogonal case and per-model η-form | If E = 0: d = d_σ ≥ 0, zero iff at most one block has positive fit fraction; with known σ² (tables recomputed under known precision) d ≡ 0. For S with A_S ≻ 0 and ε_S < 1 − x̄_S: \|d_X(S)\| ≤ η_S := νε_Sx̄_S/(1−ε_S−x̄_S) + F_S/(4(1−ε_S)). [CHK §3 WS3 VERIFIED; FD-W1; W1PC1 §5 zero case; CHK §4 WS4 VERIFIED; W2PC1 D.R3(a)] |
| (b1) Per-stage χ² | Under H-DOM, for 0 ≤ u < u+Δ ≤ 1: χ²(q_{u+Δ}‖q_u) ≤ e^{ΔD_*} − 1. [W2PC2 C2(b)·increments TRUE-AS-WRITTEN; W1PC2 D14·one-shot/increment] |
| (b2) Four-normaliser transfer (same data, fixed partition) | With q^σ_t ∝ γ₀e^{td_σ}: e^{−4vb_X} ≤ [1+χ²(q_v‖q_u)]/[1+χ²(q^σ_v‖q^σ_u)] ≤ e^{4vb_X}, 0 ≤ u < v ≤ 1. On any nonempty W ⊆ Ω with η_W := max_W η_S: the same with e^{±4vη_W}, and TV(q_v^W, q_v^{σ,W}) ≤ 1 − e^{−2vη_W}. [W2PC2 C2(b)·continuity; W2PC1 B.R3(b)(1)–(4); CHK §4 WS4(e)] |
| (b3) First stage | Particles iid π₀: 1 + N_e·Var(Ẑ_{stage 1}/(Z̄_{φ₁}/Z̄₀)) = 1 + χ²(q_{φ₁}‖π₀) exactly, and this quantity is within e^{±4φ₁η} of its block-orthogonal value. Transfer of 1 + N_e Var, never of Var. [W2PC1 B.R3(b)(1)–(4); A.R3(b)(i),(ii),(v); W2PC2 C2·variance transfer] |
| (b4) Doeblin constants | M_φ := max_S q_φ(S)/π₀(S) ≤ e^{2φη}M^σ_φ, so the coded round minorises q_φ with constant ≥ e^{−2φη}/M^σ_φ. [W2PC1 B.R3(b)(1)–(4); D.R3(b)(i),(ii),(iv)] |
| (b5) Pathwise island moment | On every successful coded grid, with the kernels as coded: W_r := Ẑ_r/Z ∈ [e^{−osc d}, e^{osc d}] ⊆ [e^{−D_*}, e^{D_*}] pathwise and E[W_r \| 𝒞] = 1, hence M₂ := E[W_r² \| 𝒞] ≤ e^{D_*}. An upper bound only; no comparison to the block-orthogonal M₂. [W2PC2 C2(b)·weights; W1PC2 D14·actual-grid moment (1,600 islands, poor V included); W2PC1 B.R3(b)(5),(6); SYNTH §3 A.R3(b)(iv)] |
| (b6) Stage count: the sandwich | For exact-frontier greedy ESS-.9 grids on a fixed common nonempty V with common pilot targets, same-data block-diagonal baseline d_σ on the fixed partition, and .9e^{4η} < 1: T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}); for the coded grid add the 2⁻⁶⁰ bisection and 10⁻¹² snap/validation qualifications. [W2PC1 B.R3(b)(1)–(4); A.R3(b)(iii)·sandwich; D.R3(b)(iii)·sandwich; E-pilot 16 cases, 0 violations] |
| (b6′) Local constancy, integer bound, envelope | If the baseline is not at a critical threshold, T = T_bd(.9) for all small ε. Under the pilot premises (global range bound D_*, 2⁻⁶⁰ ≤ h/2, h = 2c_ρ/D_*, c_ρ = √log(10/9)): P ≤ ⌈2/h⌉ + 1 and T ≤ 2⌈D_*/c_ρ⌉ + 2 ≤ 4 + 2D_*/c_ρ, a continuous envelope; D_* = 0 ⇒ T = 1. Checked fallback: T ≤ P + ⌈D_*/c_ρ⌉ + 1. [W2PC1 B.R3(b) continuity verdict (local constancy); W2PC2 C2(b)·stage count, C8·pilot extension, 600 adversarial runs] |
| (b7) Q5 condition (1): continuity and Lipschitz statements in ε | On the fixed-partition, same-data family E = εE₁ (E₁ a fixed cross-block pattern): δ_A(ε) = εδ_A(1) =: c_Aε and δ_H(ε) = c_Hε exactly. Hence on [0, ε₁] with c_Aε₁, c_Hε₁ < 1 and r(ε₁) < 1, the functions b_X(ε), D_*(ε), e^{±4vb_X(ε)}, e^{ΔD_*(ε)} − 1, e^{D_*(ε)} and the Doeblin factor are continuous with b_X(0) = 0 and Lipschitz with constant L(ε₁) := (K/2)[c_A/(1−c_Aε₁) + c_H/(1−c_Hε₁)] + νc_Ha/[(1−a)(1−c_Hε₁)²(1−r(ε₁))] (for b_X; e^{·} factors by the chain rule). Per-stage χ²: \|log(1+χ²(q_v‖q_u))(ε) − (·)(ε′)\| ≤ 4v·sup_S\|d(S;ε) − d(S;ε′)\| ≤ 4v[b_X(ε) + b_X(ε′)], so at the baseline the modulus is 4vLε. Status: PROVED (by this seat, unchecked), elementary calculus on the checked formulas; local check above, 0 violations. |
| (b8) Q5 condition (2), verbatim in the theorem | "T(ε) is a step function of ε. It can jump at critical thresholds: PC1 exhibits an actual design (n = 40, p = 2, B = 1) with one-sided baseline counts {2, 4} and T = 3 at ε = 10⁻⁵. 'Stable stage count' means the sandwich (b6), and nothing more." [W2PC1 D.R3(b)(iii)·jump corollary; E-jump] |
| (c1) Zero-dependence obstruction (WS6(d) with CHK amendment) | Under G (Gaussian noise, fixed σ² > 0), ORTH (XᵀX = (n−1)I, p ≤ n−1), fixed nonempty S₀ with fixed nonzero coefficients, the shipped score/prior/state space, partition fixed in X, truth-free null count m → ∞ with log m = O(log n), m ≥ p/2 and p^{(α−1)R̄²}/[√n(log p)^{(1+(α−1)R̄²)/2}] → ∞: D_α(π‖π₀) → ∞ in probability; for α = 2, χ²(π‖π₀) → ∞ and ESS_∞ → 0, while in the bounded-block setting (shipped B ≤ 16) or assuming π₀(S₀) → 1, TV(π, π₀) → 0. Instance: p = n−1, one coefficient 2, σ² = 1. [CHK §1, §6 VERIFIED WITH AMENDMENT; W2PC1 B.R3(c)] |
| (c2) Masked obstruction (WS7 with CHK amendments) | If π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (T27(i)'s conclusion; H3 and the joint-ratio law are non-design premises, instantiated on LH) and π(S₀) → 1: ESS_∞ ≤ π₀(S₀)/π(S₀)² → 0, KL(π‖π₀) ≥ π(S₀)log(1/π₀(S₀)) − log 2 → ∞, TV → 1; the initial population holds S₀ with probability 1 − (1−π₀(S₀))^N ≤ Nπ₀(S₀), later stages only "≤"; restricted-grid lower bounds with the set-mass (log π₀(V) = o_P(c log p + (c/2)log n)) and singleton-endpoint amendments. Neither (c1) nor (c2) refutes the multistage sampler or (b). [CHK §2, §6; W2PC1 B.R3(c)] |
| Scale disclosure (not a theorem) | Useful (O(1)) constants need signal energy O(√n) (νa² = O(1)) and ε ≲ n^{−1/2}/p on the exhibited family; at fixed ε, D_* grows (534 → 6.45·10⁴ on W at ε = .01) and the domain fails. η-form constants are O(1) iff ε = O(1/(nx̄)). A sharp necessity statement is FUTURE_WORK (all three seat forms COUNTEREXAMPLE; C's is a range obstruction only). [W2PC2 C2·ε-scale; W2PC1 B.R3·scale; CHK §4 scale remark] |
| Removed from my R2 card | Prop NEC (W2PC1 B.R3 NEC COUNTEREXAMPLE); "every constant in (b1)–(b5), including T, tends to its BO value" (replaced by (b6′), (b8)); the q₂ tilt-tail route (W1PC1 IMPLAUSIBLE); the m-form of (S) and (F) (to the leakage corollary, R3-5). |
| Guarantee (one sentence) | On the method's own partition, the gap between the block-product start and the posterior, and every bridge quantity (per-stage χ², island weight moments, Doeblin constants, and the stage count through its sandwich and envelope), is controlled by two data-computable terms, the σ²-coupling term and the cross-block term, continuously in the cross-block correlation; and the one-shot importance-weight reading of §5.3 is false even at zero correlation. |
| Objective / goal / Song–Liang | Objective (1); objective (2) through (b5) (island count via M₂ ≤ e^{D_*}) and (b6′) (depth envelope); proposal §5.3 (binding; HQ Q1 (a)(b)(c), Q5); Song–Liang Thm 4/Cor 2 as "specific start-distortion analysis, compared not exceeded" (d_σ quantifies the block-start distortion). |
| Status (verbatim, with qualifiers) | OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) + CHK "VERIFIED (PC1, cross-family, line by line)". OWS-WS6d, OWS-WS7: PROVED (SF: none; XF: none) + CHK "VERIFIED WITH AMENDMENT". OWS-WS1: PROVED, AUTHOR-ONLY. FD-W1: PROVED, XF VERIFIED (A-REV4). AREV9-OWSTAB: "VERIFIED under H-ORTH exactly as stated" (not used beyond H-ORTH). Seat C's D_* decomposition and actual-grid moment: PROOF SKETCH (NEW-COMP); W1PC2/W2PC2 TRUE-AS-WRITTEN (statement sanity, not a proof). (b2)–(b4), (b6) assemblies: PROVED (by Seats A/B/D, unchecked), W2PC1 TRUE-AS-WRITTEN. C8 pilot extension: PROOF SKETCH, unchecked (W2PC2 PLAUSIBLE); T26BUD-G: PROVED, deterministic, AUTHOR-ONLY. (b7): PROVED (by this seat, unchecked). T03: PROVED-LOCKED; T27(i): PROVED-LOCKED, CONDITIONAL. OWS-WS6e: CONJECTURE; OWS-WS8d: OPEN (neither used). |
| Fidelity to v3.1 as shipped | Partition: the method's own (verified computed on W). Kernels: as coded (b5). Grid: coded rule for (b5), (b6′); (b6)'s exact-frontier comparison is a labelled comparison object. (c) concerns the start/target laws, not the sampler. LS0 n/a; pooling n/a; stacking n/a. |
| Self-checked flag | Mixed: WS3/4/6d/7 cross-family checked (CHK); C's D_* route PC2-checked (cross-family to C) but no filed proof; (b7) seat-only; A/B/D's (b) assemblies statement-checked by PC1 only. |
| Novelty, citations checked | NEW-COMP. Nearest predecessor OWS-WS4 (internal; PC2 novelty note). Generic χ² precedent: Frazier et al. 2023, Assumption 6(iv) (via THM-INV §4b; not re-fetched by me, to the citation checker). Cérou–Del Moral–Guyader 2011 Thms 1.4–1.5 (variance theorems; not re-sold). Chatterjee–Diaconis 2018 Thms 1.1–1.3 (exp(KL) scale behind (c2)). Štefankovič–Vempala–Vigoda 2009 (greedy-schedule optimality behind (b6); LIT-SMC #9). Gelman–Meng 1998 (J identity). YWJ/ZYVR not touched. |
| Proof route and key lemma | (a1)–(a2): PC2 Appendix A's four steps (exact split; d_D ∈ [0, νx²/(2(1−x))]; eigenvalues of I + M in [1−δ, 1+δ]; resolvent bound \|t − t_D\| ≤ δ_Ht_D/(1−δ_H)). **Key lemma:** restriction monotonicity of zᵀH⁻¹z and of relative operator norms. (b2): WS1(a) cumulant identity and \|log Z_t − log Z^σ_t\| ≤ \|t\|b_X. (b5): product of stage averages in [e^{Δ_t d_min}, e^{Δ_t d_max}], ΣΔ_t = 1, E W = 1 (T12/N9). (b6): feasibility inclusion plus constrained greedy optimality (Theorem G). (b6′): empirical ESS monotone in Δ (convex log-MGF), Popoviciu, bisection invariant. (b7): homogeneity and chain rule. |
| Difficulty | (a) M; (b1)–(b5), (b7) S; (b6)–(b6′) M (the pilot interface); (c) done (cited). |
| Lean core | Finite-space: WS1(a) cumulant identity; the four-normaliser bound given sup\|d − d′\| ≤ η; the product-of-averages pathwise bound; the scalar log inequalities defining b_X and the Lipschitz algebra of (b7). Not Lean: (c) and the probability-in-the-design clauses. |
| Dependencies (card IDs) | M3 (d_σ, WS3, FD-W1; T27(i) masking law for (c2)); M7 (grid rule, Theorem G count, K25 coverage identity for V ≠ Ω); M1 (T12/N9 E W_r = 1 for (b5)); S-KERNEL (N9 amendments); S-T (T03 concentration in (c1)); M6 (Lemma KL in (c2)); S-BLOCKS (blocks = groups on W); S-REP (η̂, ε̂_×, Ĵ report the constants). |
| Risk | D_* route is a PROOF SKETCH: if the general matrix route stalls, prove on W directly (C's fallback). The useful scale is perturbative (ε ≲ n^{−1/2}/p): disclosed. Pilot-extension envelope unchecked as a proof: the checked fallback count stands. CAL/EX-S premises. |
| Fallback statement and stop rule | If (a1) (D_*) fails: ship (a3) η-form (VERIFIED) with (b2)–(b4) in η_W form, (b5) with osc d, (b6) sandwich, (c); the scale shrinks to ε = O(1/(nx̄)). If (b6′) fails: ship (b1)–(b6) plus the checked count T ≤ P + ⌈D_*/c_ρ⌉ + 1 and (b8). Every fallback keeps (a), a stage-count clause and (c) (PC1: omitting the count would not meet Q1(b)). If both the D_* route and the direct W-family route fail: escalate to HQ as unmet binding §5.3; never dropped (§2.7). Stop: one check wave per half; one HQ cycle for the pilot-extension lemma. |
| IC3 design, exhibited, where checked | **W** (SMC-dispatched): p = 9⌊n^{1/3}/9⌋, groups of 9 at ¼, every cross correlation ε_n = 1/(np) > 0, two n^{−1/4} signals in two groups, σ² = 1, n ≥ 9⁶; own partition computed, blocks = groups for n ∈ {9⁶, 10⁶, 2·10⁷, 10⁸}, H-DOM 10/10 seeds per n, D_* median 1.08 → 1.04, b_X ≈ 5·10⁻⁴ to 3·10⁻⁵ (W2PC2 §0 item 3, `w_family.py`). **W at ε = n^{−1/2}/p**: b_X ≈ 0.35, D_* ≈ 1.73–1.90, blocks = groups, domain 10/10 (W2PC2 §0 item 3). Component checks (exact branch dispatches): Dε, n = 40, p = 8, B = 2 (W1PC1 "Dε"; my R2 check 1, 40/40; W2PC1 B.R3·scale); A's n = 64, p = 16, B = 4. (c1): CHK §6 example XᵀX = (n−1)I, p = n−1, coefficient 2. (c2): LH (W1PC2 shared LH). |
| Numerical companion (≤ 20 seeds) | Existing: W2PC2 `r3_clauses.py` (104 domain designs, 0 violations), `w_family.py` (10 seeds per n), `c8_pilot.py`, W1PC2 `smc_coded.py` (1,600 islands), W2PC1 E-pilot (16 cases), my R2 check 1 (10 seeds × 4 ε), today's Lipschitz check (5 seeds, 75 pairs). For the HQ: ≤ 20 seeds on W at n = 9⁶, reporting (a, δ_A, δ_H, r, b_X, D_*), the sandwich at ε ∈ {1/(np), n^{−1/2}/p}, M₂ on four coded islands, and L(ε₁) against the observed b_X increments. |

### Card M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement · K42, K43, K45, K44; K36, K78 (output-event clauses); K95 cited from S-TARGET

| Field | Content |
|---|---|
| Setting (model/design) | Finite Ω, shipped target π(S) = ϖ(S)m(S)/Z; 𝒯 ⊆ Ω the nonempty deduplicated reported store, Z_𝒯 := Σ_𝒯 ϖm, π_𝒯 := π(·\|𝒯); δ₁ := 1 − π(S₀); h: Ω → [0, 1] (or bounded, scaled by ‖h‖_∞); 𝒮 the set of scored models; 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), c ≥ 1 (the LS0 union-then-top-c rule, METHOD #9). For (f): the LH family (W1PC2 shared LH): p = 9⌊n^{1/3}/9⌋, groups of 9 at .4, two disjoint hub links .2, coefficients (1, −.2), σ² = 1, exact Gram, n ≥ 9⁶, SIZE 9 ≤ B ≤ 16 < 18; G; T03♯'s hypotheses hold on LH (Thm5-LH, SAME-FAMILY-ONLY). |
| Implementation premises (named) | EX-A (exact arithmetic; the card is "numerical" until SC + VAL-FP, N16); SR (all scored candidates enter the winner comparison; union-then-top-c storage); Lemma S and the inheritance merge (PC2 code facts); for (e): Lemma RO + GUARD-W (stop-only coupling, audit N2(e) open), CAL, EX-S, Ẑ = Z on the exact branch, E[Ẑ_r \| 𝒞] = Z; for (f): OP-LS0 (completed scans), the e4 centre rule (tie-aware DP invariant N3 OPEN, carried as hypothesis), ℓ ≥ max{Φ(S°) − 1, 0} (= 1 on LH; shipped ℓ suffices). |
| (a) Deterministic identities | Z_𝒯 ≤ Z; π(S) ≤ ϖ(S)m(S)/Z_𝒯 for every S; TV(π_𝒯, π) = 1 − Z_𝒯/Z; KL(π_𝒯‖π) = log(Z/Z_𝒯); KL(π‖π_𝒯) = ∞ iff π(𝒯ᶜ) > 0; Ẑ < Z_𝒯 ⇒ Ẑ < Z. [W1PC1 §3 A.C7/B.D3(a–d) TRUE-AS-WRITTEN; W1PC1 §16 reverse KL repaired with π(𝒯ᶜ) > 0; W1PC2 D5·TV certificate, D5·underestimation; W2PC1 A.M5, B.M5] |
| (b) Brackets when the truth is stored | If S₀ ∈ 𝒯: 1 − δ₁ ≤ Z_𝒯/Z ≤ 1; TV(π_𝒯, π) ≤ δ₁; \|PIP^𝒯_j − PIP_j\| ≤ δ₁ for all j; \|π_𝒯(h) − π(h)\| ≤ 2δ₁‖h‖_∞; joint inclusions likewise. [W1PC1 §3 B.D3(b) COUNTEREXAMPLE repaired with ‖h‖_∞; W2PC1 B.M5 TRUE-AS-WRITTEN] |
| (c) Retention (N13) | If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀; ½ is sharp; holds under LS0 with 𝒯_new = top_c(𝒯_old ∪ 𝒮_added). Unqualified retention is false. [N13 PROVED (PC1 claim 5); W1PC1 §3; W2PC2 C4·retention TRUE-AS-WRITTEN; W2PC1 B.M5] |
| (d) Analytic envelope (N17) | m(S) ≤ U_m := C_n(2b₀ + yᵀy/(n+1))^{−ν} for every S; hence Z ≤ U := Z_𝒯 + U_m[1 − Σ_𝒯 ϖ] and TV(π_𝒯, π) ≤ 1 − Z_𝒯/U, a computable bound (loose, reported as such). [N17 PROVED (PC1 claim 1; PC2 C1(c)); W1PC2 D5·envelope, 40 designs × 5 stores; W2PC1 A.M5] |
| (e) Output-event certificate | Under Lemma RO + GUARD-W: P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; island-minimum bound 0.05^{1/R′}min_r Ẑ_r at the same level; card level P(𝒪 ∩ {some G2/L/R item false}) ≤ 0.05. Never conditional on completion: P(B \| 𝒪, 𝒞) ≤ α does not follow (CEX-guard). [W1PC1 §3 A.C3(a,b,c)/B.D3(e) TRUE-AS-WRITTEN; W1PC2 D5·LCB, D12; W2PC1 B.M5] |
| (f) Masked-regime statement (HQ Q3) | On LH under M5's hypotheses (b1-LH): for every ε > 0, P(𝒪 ∩ {TV(π_𝒯, π) > ε}) → 0; P(𝒪 ∩ {max_j\|PIP^𝒯_j − PIP_j\| > 1 − π(S₀)}) ≤ P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) + P(π(S₀) ≤ ½) → 0; P(𝒪 ∩ {MPM^𝒯 ≠ S₀}) → 0; and surely Ẑ < Z_𝒯 ⇒ Ẑ < Z. Reading: vanishing P(output and error); not conditional success, and not P(𝒪) → 1. Non-vacuous on a masked family: π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)} → 0 while π(S₀) → 1. [W2PC1 B.R4·Z𝒯/CARD TRUE-AS-WRITTEN; D.R4; W2PC2 §3 §R4 named guarantee TRUE-AS-WRITTEN (assembly)] |
| (g) Definitional facts | For a proper store (π(𝒯ᶜ) > 0), KL(π‖π_𝒯) = ∞; any positive-mass state absent from the records makes KL(π‖π̂) = ∞, surely when \|Ω\| > 4N_eR′. The masked final-estimate TV/KL bound is FW2. [W1PC1 §16; W2PC2 C15-KL] |
| Removed from my R2 card | The M₂ aside "masking forces the actual M₂ to diverge" (W2PC1 B.R4 NEEDS-HYPOTHESIS). |
| Guarantee (one sentence) | The run's own stored record gives deterministic two-sided brackets on the evidence and on every reported probability whenever the truth was scored, a 95% certificate jointly with output, and, on a masked family where the start misses the truth polynomially, the reported restricted posterior is still within δ₁ of the exact one jointly with output. |
| Objective / goal / Song–Liang | Objective (1); proposal §5.4 (PIP/joint-PIP error, deterministic TV, HQ Q3's required masked statement); §4.4/§8.2 diagnostics (what the certificate proves); Song–Liang Thm 3 (estimated PIPs via the restricted store) and Thm S (reported MPM/HPM on LH, additional to the exact-posterior counterpart). |
| Status (verbatim) | MZ-P3: "PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery"; "candidate: not reviewed, not adopted"; AUTHOR-ONLY. N13: PROVED (PC1 claim 5). PC1c5: (a) PROVED, ½ sharp. N17: PROVED (PC1 claim 1; PC2 C1(c)). PC1c2: PROVED for the potential run; N6(a) output form CORRECT WITH AMENDMENT; N6(b) PROVED modulo premise (i) (GUARD-W not audited). LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)). CEX-guard: COUNTEREXAMPLE (XF VERIFIED*). OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording used). T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)). Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none), SAME-FAMILY-ONLY. T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)). (f) assembly: PROOF SKETCH (seat-assembled; W2PC1/W2PC2 TRUE-AS-WRITTEN as an assembly). |
| Fidelity to v3.1 as shipped | LS0: yes (the union-then-top-c rule); coded grid: yes (no grid hypothesis); pooling: n/a; exact arithmetic premise, numerical label until N16; (f) uses v3.1 with LS0 as shipped, integration audit open. |
| Self-checked flag | MZ-P3 AUTHOR-ONLY; (f) seat-assembled; GUARD-W un-audited; N13, N17 PC1/PC2 checked. |
| Novelty, citations checked | NEW in kind (certificates on reported quantities), elementary; Markov lower bound KNOWN—CITE (Grosse–Ghahramani–Adams 2015); the restricted-measure TV identity is elementary (no citation claimed). (f) NEW-COMP (composition with T38-b1-LH), worded "for the paper's own target and start"; Hou–Wang–Atchadé arXiv:2407.20580: never "first finite-n"; YWJ 2016 / ZYVR 2022 cited next to M5. |
| Proof route and key lemma | Finite sums and π_𝒯 = π/π(𝒯) for (a), (b), (d); Lemma S plus the inheritance merge for (c); Markov + Lemma RO + GUARD-W for (e); event containment for (f): {𝒪, TV > ε} ⊆ {𝒪, Ŝ⁺ ≠ S₀} ∪ {π(S₀) ≤ max(½, 1−ε)}. **Key lemma:** N13 retention. |
| Difficulty | S. |
| Lean core | (a)–(d): finite inequalities on a finite Ω; (e): finite event algebra given Lemma RO; (f): the containment is finite; the limits are prose. |
| Dependencies (card IDs) | M5 (b1-LH) for (f); S-T (T03♯, Thm5-LH) for π(S₀) → 1; S-OUT (Lemma RO, GUARD-W) for (e); S-TARGET (N17) for (d); S-CERT (G2/L/R item semantics); M1 (T12 E[Ẑ_r\|𝒞] = Z for Markov); S-BLOCKS (SIZE on LH). |
| Risk | GUARD-W audit (N2(e)); N16 floating point; N3 (e4 DP) hypothesis in (f); SAME-FAMILY-ONLY on LH; MZ-P3 AUTHOR-ONLY. |
| Fallback statement and stop rule | (a)–(d) always ship (deterministic). If the GUARD-W audit fails: (e) in potential-run form only; the output form is withheld and CEX-guard disclosed (engineering fix, not a theorem fix). If LS0 integration (N3/OP-LS0) stays open: (f) ships under the named premises, as now. If (f) were lost altogether: the deterministic (b) plus Ẑ < Z_𝒯 ⇒ Ẑ < Z remain and HQ is told that Q3's named masked statement has shrunk (never silently). Stop: none for (a)–(d); one HQ cycle for the GUARD-W audit; (f) follows M5's stop rule. |
| IC3 design, exhibited, where checked | (a)–(e): any design (W1PC1 D0/E2 finite stores incl. the h = (0, 100) repair; W1PC2 40 designs × 5 random stores incl. duplicate columns). (f): LH exact Gram as above, verified W1PC2 shared LH (λ_min(Σ) = .4212, cov(x_hub, y) = 0 exactly, strict separation .6 < .8, LH-LAT margin m₀ = .0325, B ∈ [9, 16] for n ≥ 9⁶): a genuinely masked family. |
| Numerical companion (≤ 20 seeds) | Existing: W1PC2 `misc_checks.py` (D5U, D5TV); PC2's exact-rational card test (60 cases). For the HQ: ≤ 20 seeds on LH at n = 10⁴ (p = 18) with forced SMC dispatch plus one run at n = 9⁶, recording S₀ ∈ 𝒮, S₀ ∈ 𝒯, 1 − Z_𝒯/Z, max_j\|PIP^𝒯_j − PIP_j\|, MPM^𝒯 = S₀, and the Ẑ < Z_𝒯 flag. |

---

## §S3 Agenda 12, the HQ plan

### (a) Dependency graph (X → Y: Y uses X)

Key lemmas: N9 (kernels, start sampler), T12 (unbiasedness), N1 (general-h identity), Lemma RO, GUARD-W (audit), WS3, WS4, FD-W1, T27(i)/Thm5-LH (masking law), T03♯ (S-T), PART-ThmA (S-BLOCKS), D_*-lemma (C's decomposition), K25 (coverage identity), Theorem G (count), Lemma KL (K105), N13 (retention), N17 (envelope), T38-b1-LH, LS-score/Theorem A, Lemma S.

```
N9 → M1;  T12 → M1;  N1 → M1;  Lemma RO → M1;  GUARD-W → M1, M4, S-OUT
M1 → M2 (b5: E W_r = 1);  M1 → M4 (e);  M1 → S-POOL;  M1 → S-REP;  N1 → S-REP
WS3 → M3;  FD-W1 → M3;  T27(i)/Thm5-LH → M3;  PART-ThmA → M3, M5, S-BLOCKS
M3 → M2 (a: d_sigma; c2: masking law);  M3 → M6;  M3 → M5 (start mode, centre);  M3 → S-LEAK
WS4 → M2;  D_*-lemma → M2;  K25 → M7, M2 (b6);  Theorem G → M7;  M7 → M2 (b6, b6');  M7 → S-STGI (K30 cited)
T03♯ (S-T) → M2 (c1), M5, M4 (f), M1 (f), S-LEAK;  Lemma KL → M6;  M6 → M2 (c2)
S-KERNEL (minorisation) → M2 (b4), S-IDENT;  M2 (b5) → M1 (f, stacking rate);  M2 → S-REP (eta-hat domain, D_* in the J-hat bound);  M2 (a) → S-Z (D)
N17 → M4 (d);  N13 → M4 (c);  Lemma S → M4 (c);  LS-score/Theorem A → M5;  T38-b1-LH → M5;  M5 → M4 (f);  M5 → M8 (LS0 cost)
M7 → M8 (T in depth);  S-CERT → M8 (search cost), M4 (card semantics);  M2 (b5) + M1 (b) → M8 (objective-2 composition)
S-OUT → M4 (e), M1 (a contract);  S-TARGET → M4 (d), M3 (envelopes);  M4 → S-LIM (cited);  M1, M3 → S-POOL, S-Z
```

### (b) Launch waves

| Wave | Theorems | Reason |
|---|---|---|
| 1 (foundations) | M1 (V/H with N1), M3 (START), S-KERNEL + S-TARGET (N9 amendments, N17, envelopes; Lean), S-BLOCKS (PART-ThmA with SIZE); S-T as a cited input (external review queued) | Everything downstream conditions on N1, d_σ, N9, blocks = groups and T03♯. |
| 2 (binding and masked core) | M2 (WS), M7 (STG: Theorem G, K25, pilot extension), M5 (HPM), M6 (SEP + Lemma KL) | M2 needs M3's d_σ and M7's count; M5 needs S-BLOCKS; M6 feeds M2(c2). The binding §5.3 HQ opens as early as its inputs allow. |
| 3 (reported quantities and accounting) | M4 (Z𝒯 + masked statement), M8 (Proposition D), S-REP (Ĵ, ε̂_×), S-OUT + S-CERT (GUARD-W audit, card semantics) | These compose wave-2 outputs (M5 → M4(f); M7, M5 → M8; M1, M2 → S-REP) and carry the audits M4(e) needs. |
| 4 (supplement closure) | S-Z, S-POOL, S-IDENT (incl. C15-TV/KL/CI), S-LIM, S-LEAK | Cited or short; no main theorem waits on them except through already-locked inputs. |

### (c) Charters

**Charter M2 · Theorem WS (§5.3 package).**
- Goal: ship HQ Q1 (a), (b), (c) with Q5's two conditions, on the method's own partition, with every constant data-computable and reported (S-REP).
- Statement: card M2 above, rows (a1)–(c2) plus (b7), (b8).
- First lemma to attack: C's D_* decomposition (a1) via the restriction-monotonicity lemma (PC2 Appendix A steps 2–4), written as a filed proof; in parallel the pilot-progress lemma behind (b6′) (ESS monotone in Δ, Popoviciu, bisection invariant).
- Lean target: WS1(a) cumulant identity; four-normaliser bound under sup|d − d′| ≤ η; pathwise product-of-averages bound; the scalar log inequalities of b_X and L(ε₁).
- Independent-check plan (cross-family): (a1) proof by an Astra-family prover, checked by Opus/Fable; (b2)–(b7) proof by a Claude-family prover, checked by gpt-6.1-sol; (c) already CHK-verified, re-read only for wording. Numerical: ≤ 20 seeds on W as in the card.
- Fallback and stop: as in the card; one check wave per half; one HQ cycle for the pilot-extension lemma, then the checked count fallback.
- Escalation evidence: a counterexample to (a1) on the matrix domain *and* failure of the direct proof on W; or a design in the domain with a successful coded grid violating (b5). Either reopens §5.3 at HQ as unmet (never dropped).

**Charter M4 · Theorem Z𝒯 and the certificate card.**
- Goal: deterministic two-sided brackets and a joint-output certificate from the stored record, and the masked statement (f) that HQ Q3 requires.
- Statement: card M4 rows (a)–(g).
- First lemma to attack: N13 retention under the coded LS0 rule 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), confirmed against the code (Lemma S, inheritance merge); then the GUARD-W stop-only coupling audit N2(e), on which (e) rests.
- Lean target: (a)–(d) on a finite Ω (store algebra, TV identity, envelope); the event containment of (f).
- Independent-check plan (cross-family): the Claude-authored assembly (f) and the card semantics checked by gpt-6.1-sol; the AUTHOR-ONLY MZ-P3 re-derived by the checker (it is one page). Numerical: ≤ 20 seeds on LH as in the card.
- Fallback and stop: as in the card; (a)–(d) need no stop rule; one HQ cycle for the GUARD-W audit; (f) follows M5.
- Escalation evidence: a path-dependent stop that reaches output (CEX-guard realised in v3.1 code) → engineering decision for HQ/Felipe, output-event clauses withheld meanwhile; a code retention rule differing from the stated union-then-top-c → N13's premise fails → HQ.

---

## §S4 Nothing missing

**Proposal goals.**

| Goal | Where it lives |
|---|---|
| §5.1 exactness under MH correction | S-KERNEL (N9 §§0–3, CHK amendments; cited lemma + Lean) and M1(a). |
| §5.2 SMC consistency | M1 (cited lemmas Del Moral 2006, WLH 2016; N1 method-specific) and H(e) fixed-data SLLN. |
| §5.3 weight stability | M2 (binding; safeguard §2.7); S-LEAK corollary; FW: sharp necessity. |
| §5.4 PIP, joint-PIP error | M1/H(b),(d); M4(b). |
| §5.4 TV | M4(a) deterministic; M2(a) start TV; S-IDENT C15-TV terminal law; FW2 masked final estimate. |
| §5.4 KL | M2(a) bounds; M6 Lemma KL; M4(g) definitional; FW2. |
| §5.4 credible-interval coverage (HQ Q2 reading) | S-IDENT C15-CI posterior-content clause (must be named explicitly, see below); FW1 frequentist half. |
| §5.4 masked accuracy (HQ Q3 requirement) | M4(f), named. |
| §13.1 E_π[h] → truth | M1/H(a),(f) with the §2.6 rate; safeguard §2.7. |
| §4.4/§8.2 diagnostics | M4 (certificate), S-REP (Ĵ, ε̂_×), S-LIM K79 (no universal detection); K80 FW. |

**Song–Liang.** Thm 1: S-T (selection counterpart; Hellinger FW). Thm 2: S-T (R3-7 wording). Cor 1: FW (N12). Thm 3: S-T large-signal clause; estimated PIPs via M1 and M4(b). Thm 4: M3 ("specific start-distortion analysis; compared, not exceeded"). Cor 2: FW (SL analytic separation; LIT-PAR G4 cited as numerical evidence). Thm S: S-T exact-HPM counterpart plus M5 on LH. §6: M8 same-units accounting, no speed claim.

**THM-INV §1 "no theorem" cells.**

| Row | Disposition |
|---|---|
| 1 Π(X) upper bound; contraction rates; growing s₀ | K94 FW; Hellinger FW; N12 FW. |
| 2 | nothing empty; K76 S-TARGET. |
| 3 study packing (g = 5, 2g ≤ B); adaptive/overlapping partitions | N8 FW (PART-pairing OPEN); outside the fixed method, dropped with reason. |
| 4 random-design start with packing; backfit start | N8 FW; rejected by the method, dropped. |
| 5 realised masked T_n; depth vs correlation | K31 FW; served by M2(b6′) envelope and M7(d)/K30 ideal law. |
| 6 mixing of the φ = 1 round | K24, K23 FW (N10); minorisation cited in S-KERNEL/S-IDENT. |
| 7 rebuild convergence, P(S₀ ∈ V), P(schedule_limit) | N5(b) FW; validity for any frozen 𝒞 in M1 (N5(a)). |
| 8 work–depth; R vs N; island variance vs correlation; speed-up | M8; K59 FW; M2(b5) on the domain, masked M₂ FW (N4(iii)/V11); K91 dropped. |
| 9 two-sided masked Ẑ; floating point | V11 FW; K107 FW (N16), K108 S-CERT. |
| 10 joint inclusion; equal-weight accuracy; credible sets | M1(d); S-POOL P1 + K57-general FW; C15-CI + FW1. |
| 11 P(U) → 0; finite-n Gibbs discovery; study generator | K82 FW; dropped with reason (ThmB-T24 vacuous, no route); N8 FW. |
| 12 meaning of `local_certified`; LS0 absent from production | S-CERT K64 (weak local maximum); OP-LS0 named premise in M5; N3 DP invariant FW (C's C10 proposition supplement). |
| 13 positive flag power | K80 FW (no sampling law; heuristics by decision). |
| 14 P(resource_limit) etc.; fp theorem | K82/N5(b) FW; K107 FW. |

**N1–N17.** N1 → M1 (binding safeguard). N2 → implementation premises in M1, M4, M5 charters (audit obligations, see below). N3 → hypothesis in M5; DP invariant FW. N4 → (i) M1/H(b); (ii) S-POOL; (iii) M2(b5) on the domain, masked FW. N5 → (a) M1; (b) FW. N6 → M4(e). N7 → S-CERT and M4(e). N8 → FW; S-BLOCKS conditional. N9 → S-KERNEL. N10 → FW. N11 → M5 hypothesis (ℓ ≥ 1 on LH); growing s₀ FW. N12 → FW; S-TARGET eventual exact dispatch. N13 → M4(c). N14 → (a),(b) S-OUT; (c) audit; (d) card per record. N15 → M8. N16 → FW (K107); K108 S-CERT. N17 → M4(d).

**Named as missing (two items):**

| Item | Where it should go | Why |
|---|---|---|
| C15-CI, the posterior-content credible-set clause (W2PC2 C15-CI TRUE-AS-WRITTEN) | S-IDENT, as a named clause, or its own supplement row | HQ Q2 accepted the posterior-content reading; SYNTH §2.2 lists S-IDENT by K-IDs only, so the §5.4 coverage goal is otherwise served only by FW1, which is the frequentist half. |
| The audit obligations N2(b),(c),(e), N14(c), N3's DP invariant | `HQ_CHARTERS/` (as charter premises) and `REGISTRY_PAPER1.md` | They are not theorems, FW items, lemmas or drops, so the close rule has no slot for them; the charters must record them or they vanish silently. |

Otherwise nothing is missing.

---

## §S5 Questions for HQ

None. One drafting note for AMENDMENT_HQ_02, not a question: Ĵ reads the bridge potential d, a function of (X, y, blocks) fixed before stream 10, so d is a default member of the declared summary list 𝓗; the accumulator reads no random numbers and feeds nothing back.