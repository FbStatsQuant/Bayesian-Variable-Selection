# MEET-THM · Final theorem list for paper 1 (assembled by the clerk)

Assembled from the decisions in `theory_campaign/MEET-THM/MINUTES.md` §2 (binding). The clerk copied; nothing here is a new statement and no mathematics was rewritten.

**Conventions.**
- Blocks between `<!-- BEGIN VERBATIM … -->` and `<!-- END VERBATIM -->` are copied from the file and lines named in the "Source" line above them. Everything outside those blocks is clerk text (headers, integration notes, decision notes).
- "Chair's integration note" is written only where MINUTES §2.2/§2.3 changes something in a card as the seat filed it.
- Card-internal statuses, verdict-row citations and the seats' own labelling (e.g. clause letters) are the seats'. Where a seat's clause lettering differs from the final card's, the final card governs.
- Where two seats state the same card differently, the chair's editorial choice is recorded in the final section "Chair's choices".

## Header table

### Main text (MINUTES §2.1; unanimous in Round 3)

| # | Theorem | K-IDs (MINUTES §2.1) | Final card source | HQ charter | Wave (§2.5) |
|---|---|---|---|---|---|
| M1 | Theorem V/H: validity of v3.1 and accuracy of reported bounded functionals | K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47 | `R3_A.md` §S2 M1 | `HQ_CHARTERS/M1.md` | 1 |
| M2 | Theorem WS, the §5.3 package: (a) discrepancy; (b) bridge-form stability with Q5 content; (c) Proposition ONE-SHOT | K102, K10, K11, K25, K53; K103/K104 as used | `R3_B.md` §S2 M2 | `HQ_CHARTERS/M2.md` | 2 |
| M3 | Theorem START | K15, K17, K18, K10 (K16 supplementary clause) | `R3_C.md` §S2 M3 | `HQ_CHARTERS/M3.md` | 1 |
| M4 | Theorem Z𝒯 and the certificate card, with the masked-regime statement (HQ Q3) | K42, K43, K45, K44; K36, K78 output-event clauses | `R3_B.md` §S2 M4 | `HQ_CHARTERS/M4.md` | 3 |
| M5 | Theorem HPM | K72, K69, K65, K68; K63 hypothesis; K70 labelled no-LS0 variant | `R3_D.md` §S2 M5 | `HQ_CHARTERS/M5.md` | 3 |
| M6 | Theorem SEP + Lemma KL | K19, K106, K105 | `R3_C.md` §S2 M6 | `HQ_CHARTERS/M6.md` | 2 |
| M7 | Theorem STG | K26, K25, K27, K30, K33 (deterministic termination/count form); K28 cited | `R3_A.md` §S2 M7 | `HQ_CHARTERS/M7.md` | 2 |
| M8 | Proposition D (work, depth, width at the island level) | K87, K88, K89, K06, K64; K90 remark | `R3_D.md` §S2 Prop D | `HQ_CHARTERS/M8.md` | 3 |

Thesis CD (K96): a scoped remark after the main theorems (Part III).

### Supplement cards (MINUTES §2.2)

| Card | Content (K-IDs) | Statement source in Part II | HQ (lemma pack) | Wave (§2.5) |
|---|---|---|---|---|
| S-T | Theorem 1, target consistency T03♯ (K93, K04) | R2_C C9 (with A/B/D deltas) | cited; registered with LP-FOUND, no HQ work | 1 (cited) |
| S-TARGET | Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95) | R2_C C12 + A/B/D | LP-FOUND | 1 |
| S-BLOCKS | Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06) | R2_C C11 + A/B/D | LP-FOUND | 1 |
| S-KERNEL | N9 kernel facts, graph, start sampler, minorisation (K20, K21, K08, K09, K22, K103) | R2_B S5, R2_C C10 + A/D | LP-FOUND | 1 |
| S-IDENT | Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause (K25 lemma, K104, K55, K103) | R2_C C15-TV/KL/CI + A/B/D | LP-IDENT | 2 |
| ~~S-STGI~~ | **Dissolved** (MINUTES §2.2): K30 = M7(d); K29 → FW23 (its conditional implication is citable as an attributed lemma) | — | — | — |
| S-CERT | Local search, certificate semantics, B&B soundness, perturbation lemma (K64, K73 w/o region clause, K74, K05, K108) | R2_A S8, R2_B S8, R2_D S9 | LP-AUDIT | 3 |
| S-OUT | Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63) | R2_C C13 + A/D | LP-AUDIT | 3 |
| S-Z | Evidence variance, masked tails (K37–K41, K53) | R2_A S4, R2_B S4, R2_D S6 | LP-REST | 4 |
| S-POOL | Pooling rules, P1, R_eff (K49, K50, K54, K56, K57-P1) | R2_A S7, R2_B S10, R2_D S5/S7 | LP-REST | 4 |
| S-LIM | Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark | R2_A S9, R2_B S6, R2_D S11 | LP-REST | 4 |
| S-REP | Run-card reporting corollary: Ĵ and ε̂_× with companions | R3_C S-REP | LP-REP | 4 |
| S-LEAK | B's leakage clauses (F), (S) as a supplementary corollary to M2 | R2_B (b5)(b6) fragments, R2_D | LP-REP | 4 |

S-D (Proposition D) is now M8 (R3-1). Waves: 1 = M1, M3, LP-FOUND; 2 = M2, M7, M6, LP-IDENT; 3 = M5, M4, M8, LP-AUDIT; 4 = LP-REST, LP-REP (MINUTES §2.5).

---

# Part I · Main cards M1–M8

## Shared definitions and premises used by the final cards

### R3_C shared definitions (D0, score, prior, start/bridge, G, LH, W, EX-A, MC contract, output contract)

Used by M3, M6 and S-REP (and by the other cards where they cite LH, W, G, EX-A).


**Source:** `theory_campaign/MEET-THM/R3_C.md:130–142` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:130-142 -->
| Shared definition | Exact scope |
|---|---|
| D0: data/target | \(n\ge3,p\ge1\); nonconstant columns and response, centered and standardized. \(K=\min(p,\lfloor n/2\rfloor)\), \(\Omega=\{S:|S|\le K\}\). Use the shipped \(g=n,\tau=1,a_0=b_0=.01\) score and normalized capped BB\((1,p)\) prior. |
| Score | \(G_U=X_U^\top X_U,\ z_U=X_U^\top y,\ H_U=(n+1)G_U+I,\ Q_U=y^\top y-nz_U^\top H_U^{-1}z_U,\ \nu=.01+n/2\). \(m(U)=c_n[\det H_U/\det(G_U+I)]^{-1/2}(.02+Q_U)^{-\nu}\). The common positive \(c_n\) cancels from posterior ratios. |
| Prior | \(w(k)=[2\binom{2p-1}{k}]^{-1}\), \(W_K=\sum_{k\le K}\binom pk w(k)\), \(\varpi(S)=w(|S|)/W_K\). |
| Start/bridge | Actual blocks \(C_b\), \(r_b(U)=m(U)/m(\varnothing)>0\). \(\gamma_0(S)=\varpi(S)\prod_b r_b(S_b)\), \(\pi_0=\gamma_0/\bar Z_0\), \(\pi=\varpi m/Z\), \(d=\log BF-\sum_b\log r_b\), \(q_t\propto\gamma_0e^{td}\). |
| G: sampling model | Fixed raw design; \(y^r=\alpha\mathbf1+X^r\beta+\epsilon\), \(\epsilon\sim N(0,\sigma^2I)\), fixed \(\sigma^2>0\). Standardize afterwards. Standardized errors are not assumed independently Gaussian. |
| LH: design | \(p=9\lfloor n^{1/3}/9\rfloor\), groups of nine, within-group correlation \(0.4\). Two disjoint cross-group links have correlation \(0.2\); remaining cross-group correlations vanish. Each linked pair has coefficients \((1,-0.2)\); others zero; \(\sigma^2=1\). Centered Gram: \(X^\top X=(n-1)\Sigma\). |
| LH: non-vacuity | \(\lambda_{\min}(\Sigma)\ge0.4\), \(p<n\), support size four. For \(n\ge9^6\), \(9\le B\le16<18\); separation and SIZE give actual blocks equal groups. Two true coordinates have zero population marginal covariance with the response. W1P2 “Shared · LH family”; W2P2 C5/C11. |
| W: reporting exhibit | Same \(p\), groups of nine; within correlation \(1/4\), cross correlation \(\varepsilon_n=1/(np)>0\). Two coefficients \(n^{-1/4}\) in different groups; \(\sigma^2=1\). Also retain the checked stronger exhibit \(\varepsilon_n=n^{-1/2}/p\). Actual blocks equal groups for \(n\ge9^6\); \(D_*=O_P(1)\). W2P2 §1, IC3/scale rows. |
| EX-A | Exact mathematical scores, arithmetic, sums and comparisons. This is an idealisation, not a validated floating-point property. |
| MC contract | Exact iid start draws, multinomial resampling, actual invariant move rounds, independent ideal uniforms; successful full calibration \(\mathcal C\) frozen before final randomness; independent final islands; common \(N\); \(R'=4k\) declared in advance. These are computational premises. |
| Output contract | Potential uninterrupted final run first. GUARD-W identifies delivered statistical records with potential records on \(\mathcal O\). Its integrated audit remains open. Bounds transfer by intersection with \(\mathcal O\), never by conditioning on delivery. |
<!-- END VERBATIM -->


### R3_D shared implementation premises (EX-A, EX-S, CAL, IND-T, GUARD-W, SR, OP-LS0, e4, complete scans, 𝒪)

Used by M5 and Prop D.


**Source:** `theory_campaign/MEET-THM/R3_D.md:139` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:139-139 -->
Shared implementation premises (named once, used by both cards): **EX-A** exact scores and arithmetic; **EX-S** fresh independent ideal uniforms (H-U); **CAL** a successful frozen calibration record 𝒞 on streams 0–9; **IND-T** final streams 10..9+R′ independent of 𝒞 and of each other, R′ = 4k declared before stream 10; **GUARD-W** stop-only guard (operational interruption ⇒ no output); **SR** the method's stop/return rule as in the T38 hypotheses; **OP-LS0** LS0 integrated as specified (METHOD §2 #8); **e4** emitted LS0 centre = the prescribed smallest-size, lexicographically smallest start-mode maximiser (DP invariant N3 OPEN); **complete scans** no operational interruption of any search. 𝒪 is the output event; statements are P{𝒪 ∩ ·}; D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) in potential-run notation (the overbar is the potential run, not set complement; W2PC1:122).
<!-- END VERBATIM -->


---

## M1 · Theorem V/H

**Chair's integration note.**
1. K-ID header: the card's own header line lists "K46, K32, K86, K85, K36, K78, K51, K52, K48, K62; cited K20, K21, K08, K35, K47"; MINUTES §2.1 lists K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47. The registry (`REGISTRY_PAPER1.md`) follows MINUTES. The card body is unchanged.
2. Growth rates (MINUTES §2.3 §2.6, confirmed by all four): clause (i) is the first stacking configuration, R′_n = 4⌈log₂(n + p + 1)⌉, for a fixed finite set of declared summaries on families with D_* = O_P(1); the second optional configuration R′_n = 4⌈(n + p)⁶/4⌉ for simultaneous control over ≤ (n + p)² declared summaries is added to the statement of (i). ℓ, L and N need no edit; shipped R′ = 4 carries only the fixed-R statements. d is a default member of the declared list 𝓗 (A, B; AMENDMENT_HQ_02).
3. Binding §13.1: if N1's general record identity fails, the narrower theorem ships and §13.1 escalates (MINUTES §2.3 §2.7; the card's own fallback agrees). K63 (worker equivalence) and K86 (IND-T) are named premises here and proved in S-OUT (R3-4).


**Source:** `theory_campaign/MEET-THM/R3_A.md:112–137` (verbatim)

<!-- BEGIN VERBATIM R3_A.md:112-137 -->
### M1 · Theorem V/H (validity of v3.1 and accuracy of reported bounded functionals)

K-IDs: K46, K32, K86, K85, K36, K78, K51, K52, K48, K62; cited K20, K21, K08, K35, K47.

| Field | Content |
|---|---|
| Model/design hypotheses | Admissible standardised (X, y), n ≥ 3; h ∈ 𝓗 with 0 ≤ h ≤ 1, measurable in (X, y, 𝓒), declared before stream 10 (M9). For (i) only: T03♯'s hypotheses (R1, G, R, SE_λ, SE_w, BM-∞ or BM(c)) on a family with osc d ≤ D_* = O_P(1) (M2(a)), p ≤ n^A. |
| Implementation premises (named) | EX-A exact arithmetic; H-U/EX-S exact iid uniforms and exact start sampler (N9); CAL: 𝓒 frozen on streams 0–9; IND-T: streams 10..9+R′ independent (audited for R′ = 4; extension audit pending, S-OUT); R′ = 4k declared before stream 10; multinomial resampling; GUARD-W and Lemma RO for (d); M9 accumulator; stacking configuration R′_n for (i). |
| Statement | (a) Validity [cited]: each elementary move is γ_φ-reversible, the uniformly random-order round q_φ-invariant and self-adjoint under N9's sufficient conditions, draw_pi0 and Z̄₀ exact; each island is a Feynman–Kac model, so E[Ẑ_r \| 𝓒] = Z and E[Ẑ_r PIP̂_rj \| 𝓒] = Z·PIP_j with the RB record before the Gibbs draw (weighted identity; no terminal stationarity claimed). (b) Lemma N1: E[Ẑ_r H_r(h) \| 𝓒] = Z·π(h), H_r the plain measured-endpoint average. (c) Contract: (a),(b) hold conditionally on any successful frozen 𝓒; any R′ declared before stream 10 keeps them; adaptive R′ or conditioning on completion **need not** preserve them (CEX-guard). (d) Output event: P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, never conditional on 𝒪. (e) Islandwise, every regime and frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝓒] ≤ 2δ₁, δ₁ = 1 − π(S₀). (f) Finite R′, M₂ = E[W_r² \| 𝓒]: P(\|μ̂(h) − π(h)\| > ε \| 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)}; P(\|μ̂(h) − h(S₀)\| > t \| 𝓒) ≤ exp{−R′(1−s)²/(2M₂)} + 2δ₁/(st); vacuous at R′ = 4, informative under stacking; fixed data: μ̂(h) → π(h) a.s. as R′ → ∞ [cited]. (g) Declared classes: joint inclusions h_A = 1{A ⊆ S} on ≤ 2pB declared pairs (plain averages); interval probabilities h_I(S) = P(β_j ∈ I \| S, X, y) for a finite declared list, union bound; posterior-content error only, no quantile claim (HQ Q2). (h) Decision transfer: exact PIPs ≥ δ from ½ and uniform error < δ ⇒ reported MPM = exact MPM. (i) Asymptotic, with R′_n = 4⌈log₂(n+p+1)⌉: μ̂(h) → h(S₀) in probability, jointly with output; liminf P(𝒪 ∩ correct) = 1 − limsup P(U_n). |
| Verdict rows per clause | (a) W1PC1:109–110 TRUE; W2PC1:92 TRUE; CHK:94, 140–142 (N9 amendments adopted); RB wording per W2PC1:106. (b) W1PC1:110, W2PC1:92 TRUE; N1 PROOF SKETCH. (c) W1PC1:127 AMBIGUOUS → "need not" (W2PC1:92 REPAIRED). (d) W1PC1:126 TRUE. (e),(f),(g),(h) W1PC1:118, 120; W2PC1:93 TRUE (interval claim narrowed, W1PC1:263); W1PC1:240 (0 ≤ h ≤ 1); (h) W1PC1:302 TRUE. (i) W2PC1:94 TRUE on C's family; liminf form W1PC1:170. |
| Guarantee | Whatever the correlation, every island's unnormalised outputs are exactly unbiased given any frozen calibration, every reported bounded summary is right on the islands that carry evidence weight, and pooling enough declared islands by Ẑ makes it right. |
| Serves | Objective (1); proposal §5.1, §5.2, §5.4 (PIP, joint-PIP, posterior-content error), §13.1 (binding); Song–Liang Thm 3 (reported PIPs), UQ of merged output; INV rows 4, 6, 8, 10. |
| Status (verbatim) | T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT; N1: PROOF SKETCH; A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'; MA-PropP: PROVED (elementary), author-only; IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); CEX-guard: COUNTEREXAMPLE; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); (h), (i): PROVED (by this seat, unchecked). |
| Fidelity to v3.1 | (a)–(h) as shipped (LS0 alters no particle; any frozen grid; Ẑ-weighted primary). (i) uses the optional stacking configuration (AMENDMENT_HQ_02), not the default four islands. |
| Self-checked flag | N1 unchecked (PROOF SKETCH, numerically TRUE-AS-WRITTEN); MA-PropP author-only; N9 candidate plus cross-family CHK. |
| Novelty | (a), (f) fixed-data limits KNOWN—CITE: Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022 (LIT-SMC rows 1, 21–22). (d) Markov KNOWN—CITE Grosse et al. 2015; the output-event discipline "genuinely non-standard" (LIT-SMC). (b), (e), (g), (h): NEW-COMP (M9 mechanism, measured-record identity). Checked against LIT-SMC/LIT-PAR digests only; citation checker to confirm volumes. |
| Route / key lemma | N1: finite-state resample–move recursion; the state before each measured record is Zπ-weighted because the prefix of a uniformly random order is state-independent (terminal-round prefix identity, N9 §3). (e): \|H_r − h(S₀)\| ≤ fraction of measured particles off S₀, then N1 on 1{S ≠ S₀}. (f): Chebyshev with the denominator event ≥ ½ (PC1 claim 3); Maurer/Hoeffding. (i): M₂ ≤ e^{D_*} (M2(b)) and R′_n → ∞. Key lemma: N1. |
| Difficulty | M (N1 one page; the rest assembly). |
| Lean core | T12Core `unbiased_of_step` with `hstep` discharged for multinomial resampling + an invariant kernel; detailed balance of the four kernels (finite matrices); (e) deterministic step; (f) finite inequality on abstract nonnegative weights; (h) finite; CEX-guard as a two-point example. |
| Dependencies | S-KERNEL (N9), S-OUT (Lemma RO, GUARD-W, IND-T extension), S-TARGET (propriety), M2(b)(iv) and S-T (T03♯) for (i); feeds S-POOL, S-REP, M4(d), M8. |
| Risk | N1 fails (binding §13.1); GUARD-W or IND-T extension audit fails (then (c),(d) stay potential-run statements). |
| Fallback + stop rule | Fallback: (a), (c), (d) plus (e)–(i) for marginal PIPs only (locked RB identity; no general h). Stop: one HQ wave on N1; if not closed, ship the fallback and **escalate §13.1 to HQ** (never dropped). |
| IC3 design, exhibited | (a)–(h): any admissible X, including duplicate columns (W1PC1 D0/E1 finite enumeration, W1PC1:69, 110). (i): C's family W (within 1/4, ε_n = 1/(np) > 0, two n^{−1/4} signals, blocks = groups for n ≥ 9⁶), D_* = O_P(1), checked with the method's own partition (W2PC2:53–58); also at ε = n^{−1/2}/p. |
| Numerical companion (≤ 20 seeds) | N9-KERNEL CHECK (DB ≤ 2.3·10⁻¹²); PC1 E1 two-state exact enumeration (exists). For the HQ: exact enumeration on p ≤ 8 of E[Ẑ_r H_r(h)] against Z·π(h) and of E[W_r\|H_r − h(S₀)\|] against 2δ₁ on a coded-grid replica, 10 seeds. |

Split note (if R3-1 (ii) were chosen instead): Proposition V+ = clauses (a)–(d) with the same premises; Theorem H = (e)–(i) with "Setting V+". Nothing else changes.
<!-- END VERBATIM -->


---

## M2 · Theorem WS (the §5.3 package)

**Chair's integration note.** No change.
(B's leakage clauses (F), (S) are already outside this card; they are the supplement S-LEAK, R3-5. The §5.3 escalation safeguard of MINUTES §2.3 §2.7 matches the card's fallback row.)


**Source:** `theory_campaign/MEET-THM/R3_B.md:151–187` (verbatim)

<!-- BEGIN VERBATIM R3_B.md:151-187 -->
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
<!-- END VERBATIM -->


---

## M3 · Theorem START

**Chair's integration note.** No change. (K16 stays a supplementary conditional lemma, as the card states.)


**Source:** `theory_campaign/MEET-THM/R3_C.md:144–177` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:144-177 -->
### M3 — START

| Card field | Final content |
|---|---|
| IDs | **M3: K15, K17, K18, K10**; K16 is an attributed supplementary conditional lemma. |
| Hypotheses | D0 and EX-A. Deterministic clauses allow any fixed partition with \(|C_b|\le K\) and the stated positive tables. Score-coupling clauses require production tables. The masked clause additionally uses G on the exhibited LH family. |
| Implementation premises | Tables, size cap and prior are those specified above. No calibration, random-number, LS0, pooling or delivery premise is needed for the mathematical start-law claims. Actual execution fidelity remains distinct from these identities. |
| AGG definitions I | For feasible reference \(S^\circ\), \(s=|S^\circ|\), \(U_b^*=S^\circ\cap C_b\), define \(a_{bj}=\sum_{U\supseteq U_b^*,\,|U\setminus U_b^*|=j}r_b(U)/r_b(U_b^*)\), \(D_b=\max_{j\ge1}(j!a_{bj})^{1/j}\), empty maximum zero. |
| AGG definitions II | Set \(q=(p-s)^{-1}\sum_bD_b\) for \(s<p\), otherwise zero. Set \(e=2p\max_{b,U:\,a=|U_b^*\setminus U|>0}[r_b(U)/r_b(U\cup U_b^*)]^{1/a}\), empty maximum zero. |
| M3(a): deterministic mass | If \(q<1\), \(\pi_0(S^\circ)\ge(1-q)^{s+1}/(1+e)^s\). For feasible \(S_0\), \(\pi_0(S_0)/\pi_0(S^\circ)=[w(|S_0|)/w(s)]\prod_b r_b(S_{0b})/r_b(U_b^*)\). **Evidence:** W1P1 §5, A.C8(a–e)/B.D4/D.M6; source T22(i),(ii). |
| M3(b): bridge mass | For feasible \(S_0\), \(\inf_{0\le t\le1}q_t(S_0)\ge\min\{\pi_0(S_0),\pi(S_0)\}\). This is a finite-law mass bound, not a particle-discovery assertion. **Evidence:** same W1P1 §5 row; T22(iv). |
| M3(c): exact factorization | \(B_b=\sum_{U\subseteq C_b}r_b(U)\), \(q_b(U)=r_b(U)/B_b\), \(A(k)=\varpi(k)\prod_bB_b/\bar Z_0\). Then \(\pi_0(S)=A(|S|)\prod_bq_b(S_b)\). **Evidence:** W1P2 cluster 5, “D2 · exact factorisation”; W2P2 §2, C5. |
| Dilution definitions | For nonempty \(S_{0b}\), let \(\lambda_b=\log r_b(S_{0b})\), \(\eta_b=[B_b-1-r_b(S_{0b})]/[1+r_b(S_{0b})]\). For empty \(S_{0b}\), let \(\eta_b=B_b-1\). Production tables have \(r_b(\varnothing)=1\), so \(\eta_b\ge0\). |
| M3(d): dilution | \(V=\sum_{b:S_{0b}\ne\varnothing}\log(1+e^{-\lambda_b})\), \(C=\sum_b\log(1+\eta_b)\). Then \(-\log\pi_0(S_0)=V+C-\log A(|S_0|)\). **Evidence:** W1P1 §5, dilution clause; DIL-E/E1, here at tilt \(t=1\). No sign claim for \(-\log A\). |
| Coupling definitions | Let \(\bar Q=.02+y^\top y\), \(x_b=nz_{S_b}^\top H_{S_b}^{-1}z_{S_b}/\bar Q\), \(x=\sum_bx_b\). Define \(d_\sigma(S)=\nu[\sum_b\log(1-x_b)-\log(1-x)]\) when \(x<1\), and \(d_X=d-d_\sigma\). |
| M3(e): shared variance | Under block orthogonality, \(x<1\), \(d_X=0\), and \(0\le d_\sigma\le\nu\sum_{b<c}x_bx_c/(1-x)\). Equality \(d_\sigma=0\) holds exactly when at most one block has positive fit fraction. **Evidence:** CHK §3, WS3(b),(c); W2P1 D.M6. |
| Correlated extension interface | On M2’s matrix domain, the same split satisfies \(0\le d_\sigma\le C_\sigma\), \(|d_X|\le b_X\). The quantitative perturbation theorem belongs to M2. **Evidence:** W2P2 §1, “C2(a) · split”. |
| M3(f): masked law | Under G on LH, \(\log\pi_0(S_0)+2\log p+\log n=O_P(1)\), whereas \(\pi(S_0)\to1\). **Evidence:** W1P2 cluster 5, “D2 · LH masking law”; W2P2 §2, C5. Posterior concentration uses S-T. |
| Conditional-law safeguards | T27(i) retains a fixed feasible completion chain, jointly two-sided tight successive log-table ratios and a normalized reference-mass lower bound. LH supplies the application; cancellation alone does not discharge these premises on another design. |
| K16 placement | Cite T22(iii), **PROVED-LOCKED CONDITIONAL**, with G, R, within-block SE, EXP′, VIS, NL\(_\eta\), NL\(_{\rm avg}(\kappa)\) retained. Its favourable rate is a separate regime. It is not an additional unconditional assertion in M3. |
| Guarantee | The shipped start has an exact mass decomposition and can assign vanishing mass to truth on a correlated family whose full posterior concentrates on truth. |
| Goals | Objectives (1), (3); proposal §5.3 discrepancy and §5.4 start approximation; Song–Liang Thm 4 comparison only, plus statistical context for Thm S. No identification of \(\pi_0\) with Song–Liang’s final output. |
| Status: deterministic | T22(i)(ii)(iv): **PROVED-LOCKED**. DIL-E: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. DIL-E1: **PROVED; SF: none; XF: VERIFIED* (A-REV9)**. |
| Status: statistical | T27(i): **PROVED-LOCKED, CONDITIONAL**. Thm3/4-EXP: **PROVED; SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)**. Thm5-LH: **PROVED; SF: VERIFIED (W3-VEXP); XF: none; SAME-FAMILY-ONLY**. |
| Status: coupling/assembly | OWS-WS3: **PROVED; SF: none; XF: none; AUTHOR-ONLY** in the inherited ledger; CHK separately records **VERIFIED (PC1, cross-family, line by line)**. Final assembly: **PROOF SKETCH, unchecked**. |
| Fidelity/self-check flag | Actual v3.1 target, tables, cap and partition. No altered start or known-variance substitution. Not self-check-only at the ingredient level; Thm5-LH’s qualification and the absence of a full assembly proof check remain explicit. |
| Novelty/citation | **NEW-COMP**, centered on this start’s masking and shared-variance distortion. Block computation is established precedent: [Papaspiliopoulos–Rossell (2017), §§3.1–3.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC5975653/). DIL-E/E1 and OWS-WS3 are the internal predecessors. |
| Proof route/key lemma | Import T22 and DIL identities; match production normalization. For LH, verify actual partition equality, then import the joint ratio/reference-mass application of Thm5-LH and S-T. Shared-variance algebra is CHK WS3. |
| Difficulty/Lean core | Moderate assembly; substantial qualification audit. Lean: finite products, prior ratios, logarithmic dilution identity, endpoint Hölder inequality and scalar shared-variance bounds. Gaussian asymptotics remain cited prose. |
| Dependencies | S-TARGET; S-BLOCKS; S-T for \(\pi(S_0)\to1\). The M2 perturbation clause is a cross-reference, not a prerequisite for the BO or LH clauses. |
| Risk | Losing normalized reference mass; treating the capped start as independent blocks; confusing sample and population cancellation; exporting exact-Gram results to adaptive random packing. |
| Fallback/stop rule | Retain deterministic mass, factorization, dilution and BO coupling if the LH application fails its full check. After one proof-and-repair cycle, move the failed statistical extension to FUTURE_WORK. Notify M5/M6 and HQ of any resulting loss of required masked accuracy or Q1(c) coverage. |
| IC3 exhibit/check | LH above supplies genuine cross-block correlation and the masked conclusion; W1P2 shared-family/cluster-5 rows and W2P2 C5/C11 verify the stated scope. BO components allow correlated columns within blocks; CHK §3 checks them. |
| Numerical companion | None newly run. Proposed companion: at most ten Gaussian seeds; compute exact start mass by block convolution on LH and compare its log scaling. Use small enumerable component cases for factorization; label forced/component dispatch explicitly. |
<!-- END VERBATIM -->


---

## M4 · Theorem Z𝒯 and the certificate card, with the masked-regime statement

**Chair's integration note.**
1. K95 (the odds certificate, η < 1) lives in S-TARGET (R3-4, unanimous); M4 cites it. No clause of this card changes.
2. The masked statement is clause (f) of this card (Seat D's lettering "M4(e)" in R3_D is the same statement). Per MINUTES §2.3 §2.7 and R3_C §S5, loss of the masked statement without an approved replacement **escalates**; the card's fallback row says HQ "is told … (never silently)", which is to be read as an escalation.
3. N2(e) GUARD-W, the LS0 retention rule/OP-LS0 integration and the N3 DP invariant are named implementation premises of this card (MINUTES §2.3, "Audit obligations").


**Source:** `theory_campaign/MEET-THM/R3_B.md:189–216` (verbatim)

<!-- BEGIN VERBATIM R3_B.md:189-216 -->
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
<!-- END VERBATIM -->


---

## M5 · Theorem HPM

**Chair's integration note.**
1. K70 stays in this card as the labelled no-LS0 variant clause (b2-LH) (A, B, D: clause; C: supplementary attributed variant; MINUTES §2.1 follows the clause form). K63 is a hypothesis here, proved in S-OUT.
2. N2(c) (integrated LS0 replay), the N3 DP invariant (e4 centre), GUARD-W and N14(c) (extra search at R′ > 4) are named implementation premises (MINUTES §2.3, "Audit obligations").
3. If (b1-LH) falls, the §5.4 masked statement rests on M4's regime-free certificate; that loss escalates (MINUTES §2.3 §2.7).


**Source:** `theory_campaign/MEET-THM/R3_D.md:141–158` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:141-158 -->
### Card M5 · Theorem HPM (composition at every n; reported HPM with LS0 on LH; Theorem A) — K72, K69, K65, K68; K63 hypothesis; K70 labelled variant; K82 remark

| Field | Content |
|---|---|
| Final statement | **Hypotheses (model/design):** standardised X, the shipped prior and hyperparameters (ridge/BB(1,p)/cap, IG(a₀, b₀)); for (b1-LH) and (b2-LH): LH exact Gram with p ≤ n − 1, c linked pairs, group size g, within-correlation ρ, link ψ with |ψ| < ρ, fixed β; the T03♯ hypotheses on LH (G, R, SE_λ(j₀), SE_w(m♯; g₀), BM) and SIZE g_max ≤ B < 2g_min (holds on LH for n ≥ 9⁶ with g = 9, W1PC2 D4). **Implementation premises:** EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4, complete scans, ℓ ≥ τ(C) with a completed final scan; IND-T when R′ > 4. **(0) Composition at every n, any X.** Ŝ⁺ the ≻-maximum of the all-scored set 𝒮⁺ under (F, −|S|, lex) (K63). P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, δ₁ := E₀[1 − π(S₀)]. If S₀ ∈ 𝒮⁺ and δ₁ < ½ then Ŝ⁺ = S₀. N200 bracket: P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), with the matching lower bracket, Π(X) measured, not bounded. Transfer to R′ > 4 only with the extra search from c₄ (nested scored set). **(a) Theorem A / LS-score.** Under TD′_∞ on Lat(S°), local search from C ∈ Lat(S°) with ℓ ≥ τ(C) and a completed final scan reaches and certifies S₀ within Φ(C) moves; LS0 scores S₀ within max{Φ(S°) − 1, 0} moves (scoring, not certification). **(b1-LH).** On LH with LS0: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; hence liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). No delivery claim (K82 remark). **(a-fav) labelled variant:** under (F) with iid π₀ draws, D_n → 0. **(b2-LH) labelled variant (K70):** without LS0 on STAB-LH (g = 9, c = 2, ρ = 0.4, ψ = 0.2), any frozen grid, the same conclusion. |
| Guarantee | A wrong reported model means no output, a posterior miss, or a never-scored truth; on an explicit correlated family where the start misses the truth polynomially, the shipped method still reports it, jointly with output. |
| Serves | Objective (3); Song–Liang Thm S ("exact-HPM counterpart plus a separate reported-HPM result on LH"); THM-INV rows 11, 12; feeds M4(e) for §5.4's masked statement (HQ Q3). |
| Status (verbatim) | Thm4-C1 "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)"; T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200 "PROVED (elementary, every n); Π(X) upper bound OPEN" (author-only); TheoremA "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))"; T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))" (registry ⚑ CONFLICT on the iid sub-claim, excluded); Thm-b1 "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; T38-(a) "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; B2E-B2LH "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))"; STAB-cert(A7) "REFEREE (Astra-authored)"; PART-ThmA "PROVED (XF: VERIFIED* (A-REV9))"; N3 "OPEN"; Thm5-LH (input via M3) "PROVED (SF: VERIFIED (W3-VEXP); XF: none)" SAME-FAMILY-ONLY. Assembly: PROOF SKETCH (by this seat, unchecked). **Fidelity:** v3.1 with LS0 (METHOD #8) for (0), (a), (b1-LH); any frozen grid; pooling not involved (scored-set maximum); (b2-LH) is v3 without LS0, labelled; (a-fav) is an iid-draw variant, labelled. |
| Verdict rows used | (0): W1PC1 §7 TRUE-AS-WRITTEN (E1, 1,440 cases), W2PC1:122 TRUE-AS-WRITTEN; R′ transfer W1PC1 §7 TRUE. (a): W1PC1 §6 NEEDS-HYPOTHESIS repaired to ℓ ≥ τ(C) + final scan, W2PC1:122 REPAIRED; W2PC2:127 (scoring vs certification) TRUE-AS-WRITTEN. (b1-LH): W1PC1 §6 TRUE-AS-WRITTEN, W1PC2 D4 TRUE as cited, W2PC1:122, W2PC2:126; liminf form W1PC1 §6. SIZE: W1PC1 §6 (PART-CE2), W2PC2:158. Variants: W1PC1 §6 TRUE-AS-WRITTEN as labelled variants. |
| Self-checked flag | N200 author-only; T38-(a) XF none; Thm5-LH SAME-FAMILY-ONLY; STAB-cert Astra-authored, Claude-verified. Integrated LS0 / emitted-centre / GUARD-W audits open (W2PC2:39; W2PC1:122 GAP). |
| Novelty | NEW for this target and method (NEW-COMP). Checked: Yang–Wainwright–Jordan, AoS 44(6) 2016 Thm 2, Lemma 4 (LIT-MCMC #1); Zhou–Yang–Vats–Roberts–Rosenthal, JRSSB 84(5) 2022 Thm 1 (LIT-MCMC #2): write "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start". Hou–Wang–Atchadé arXiv:2407.20580 Thm 2 (LIT-STAT #19): never "first finite-n". Rossell 2022 Prop 1: the 2E₀δ₁ term is KNOWN—CITE. Barbieri–Berger 2004: HPM/MPM facts (K60, K61 cited lemmas). |
| Route / key lemma | (0) finite-set argument. (a) TD′ lattice descent (TheoremA) with the capped-scan interface. (b1-LH): LH centre law (M3) + LH-LAT margin m₀ > 0 + LS-score with the e4 centre + T03♯ (S-T) + retention (M4(b)). **Key lemma:** LS-score with the emitted centre equal to the prescribed start mode (N3). Difficulty: S (assembly); M for the N3 DP invariant. |
| Lean core | `T37Greedy.lean`, `T37Lattice.lean` (sorry-free); `T21HPM.lean` (`t21_C1` sorry-free). To add: the capped-scan certification interface (ℓ ≥ τ(C), completed scan ⇒ certified return) and (0) as a finite Boolean lemma with the output event. Cited probability: T03♯ (S-T), Thm5-LH masking law (M3). |
| Dependencies | Uses: S-T (δ₁ → 0), M3 (start-mode centre, π₀(S₀) law), S-BLOCKS (SIZE ⇒ blocks = groups, K07/K06), S-CERT (K64 search semantics and scan bound), S-OUT (K77 Lemma RO, K78 GUARD-W, K84 stacking nesting, K63 order). Used by: M4(e), Prop D (search cost term), COVERAGE_MATRIX Thm S row. |
| Risk | N3 OPEN (DP invariant); integrated-LS0 replay (N2(c)) pending; Π(X) only measured (K94 FW); study generator N8 uncovered (the g = 5 study is not the LH exhibit). |
| Fallback + stop rule | Fallback: (0) + (a) + (b2-LH) ship unconditionally; (b1-LH) labelled "conditional on N3" if the DP invariant is unproved after one HQ cycle. Stop: the merged-LS0 replay contradicting LS-score's centre rule, or a counterexample to T38-b1-LH on LH ⇒ (b1-LH) withdrawn, objective (3) coverage reported as (b2-LH) only; the §5.4 masked statement then rests on M4(d) + M4(b) (no binding goal dropped). |
| IC3 design (exhibited) | LH exact Gram, g = 9, c = 2, ρ = 0.4, ψ = 0.2, n ≥ 9⁶ (blocks = groups, SIZE, LH-LAT m₀ = 0.0325 > 0): W1PC2 D4 DESIGN-VERIFIED (`lh_family.py`), W2PC2:126 DESIGN-VERIFIED. (0): any X (W1PC1 §7 DESIGN-VERIFIED, Dε exact branch). |
| Numerical companion (≤ 20 seeds) | Filed: 0/2,394 HPM changes by LS0 (O-LS0 test export). New: forced-dispatch LH replica (PC2's `lh_family.py` + `smc_coded.py`) with LS0 at component size, ≤ 20 seeds, reporting the frequency of Ŝ⁺ = S₀, of S₀ ∈ 𝒮⁺, and of the D_n event; a component check, since production dispatches the exact branch at that size. |
<!-- END VERBATIM -->


---

## M6 · Theorem SEP + Lemma KL

**Chair's integration note.** No change.


**Source:** `theory_campaign/MEET-THM/R3_C.md:179–206` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:179-206 -->
### M6 — SEP + Lemma KL

| Card field | Final content |
|---|---|
| IDs | **M6: K19, K106, K105**. Generic finite-law inequalities are supporting lemmas; the LH consequence is the method-specific package. |
| Hypotheses | Finite \(\Omega\), strictly positive normalized \(\pi,\pi_0\), feasible distinguished \(S_0\). Write \(a=\pi_0(S_0)\), \(b=\pi(S_0)\). Statistical consequences use D0, EX-A and G on LH, with M3(f) and S-T. |
| Implementation premises | Comparison experiment: \(Q\ge1\) exact iid draws from \(\pi_0\), conditionally on data. One-shot estimation uses exact weights. No production-grid, mutation, LS0 or delivery premise enters these comparisons. |
| M6(a): discovery | Conditional on data, \(P(S_0\text{ absent from all }Q\text{ draws})=(1-a)^Q\le e^{-Qa}\). **Evidence:** W1P2 cluster 8, “D3 · miss probability”; W2P2 §2, C6. |
| M6(b): LH threshold | Let \(Q_n^\star=p^2n\). Under LH, \(Q_n/Q_n^\star\to0\) gives miss probability tending to one; \(Q_n/Q_n^\star\to\infty\) gives miss probability tending to zero, over data and comparison draws. **Evidence:** W2P2 §2, “C6 · Q* scale”. |
| Tables qualification | On LH, truth spans several actual blocks, so no block table evaluates the full truth. Adding existing block-table evaluations to this start-only comparison does not change its discovery event. **Evidence:** W1P1 §8, SEP-A scope; checked LH partition. |
| M6(c): singleton second moment | \(1+\chi^2(\pi\Vert\pi_0)\ge b^2/a\). On LH this yields an inverse-start-mass lower bound \(p^2n\exp\{O_P(1)\}\), with a two-sided tight positive multiplier. **Evidence:** W1P2 cluster 8, “D3 · χ² bound”; CHK §2(a),(b). |
| Evidence estimator | Let \(f(S)=\varpi(S)m(S)\), \(Z=\sum_Sf(S)\), and \(\widehat Z_Q^{IS}=Q^{-1}\sum_{i=1}^Qf(S_i)/\pi_0(S_i)\). Then \(\operatorname{Var}(\widehat Z_Q^{IS}\mid X,y)/Z^2=\chi^2(\pi\Vert\pi_0)/Q\). **Evidence:** W1P2 cluster 8, “D3 · IS variance”. |
| Interpretation of variance | Consequently, below the LH discovery scale the one-shot evidence estimator’s relative variance diverges in probability. This is an \(L^2\) obstruction; large variance alone is not a high-probability error lower bound. No matching upper bound is asserted. |
| Lemma KL | \(KL(\pi\Vert\pi_0)\ge b\log(1/a)-\log2\). **Evidence:** W1P2 cluster 8, “D3 · KL bound”; CHK §2(a). |
| KL consequence | On LH, \(KL(\pi\Vert\pi_0)\ge b\log Q_n^\star+O_P(1)-\log2\), hence diverges in probability. The finite singleton bound is the retained theorem; no universal sample-complexity conclusion for arbitrary functionals is attached. |
| Scope boundary | This is not a lower bound for production SMC, start-plus-search, or every one-shot estimator. SEP-taska remains a **COUNTEREXAMPLE**. Ideal logarithmic crossing counts do not imply logarithmic total work. |
| Guarantee | The specified iid start-only comparison needs the LH inverse-mass scale for discovery, while one-shot evidence correction inherits a corresponding second-moment obstruction. |
| Goals | Objective (1), with motivation for objectives (2), (3); proposal §5.3 one-shot obstruction and §5.4 start KL. Song–Liang Thm 4 is contextual comparison only; no analytic SL/FDR separation. |
| Status | SEP-A/SEP-B: **PROVED; SF: none; XF: VERIFIED (A-REV9)**. KL: **PROOF SKETCH (NEW-SYNTH)**, **AUTHOR-ONLY** in IDX. Statement checks remain TRUE-AS-WRITTEN; they do not upgrade KL. Final assembly: **PROOF SKETCH, unchecked**. |
| Fidelity/self-check flag | Actual shipped \(\pi_0,\pi\); explicitly different comparison algorithms. SEP ingredients have filed cross-family checks. KL and the final assembly lack a full proof certificate. SEP-A-iid and broader exponent claims are not imported. |
| Novelty/citation | **NEW-COMP** for the explicit LH start-mass mechanism. [Chatterjee–Diaconis, Thms 1.1–1.3](https://arxiv.org/html/1511.01437v3) supplies the established KL-scale context, with log-weight-tail and estimand qualifications. Finite coarsening and iid variance identities are not novelty claims. |
| Proof route/key lemma | M3 supplies two-sided tightness of \(Q_n^\star a_n\); apply the exact miss formula. Retain the singleton term in the second-moment sum. Binary KL data processing and binary entropy \(\le\log2\) prove Lemma KL. |
| Difficulty/Lean core | Routine after M3. Lean: iid miss probability, singleton second-moment inequality, binary coarsening/log-sum inequality and entropy bound. Probability tightness arguments remain prose unless separately formalized. |
| Dependencies | M3; S-T; S-TARGET. No dependence on M7, a production mixing theorem or Proposition D. |
| Risk | Replacing a lower bound by an asymptotic equality; confusing evidence variance with self-normalized variance; claiming probability failure from variance alone; claiming universal necessity of tempering. |
| Fallback/stop rule | Ship the exact discovery formula and finite singleton/KL/variance statements. If the LH application fails, withhold its scale claim until M3 is repaired. After one repair cycle, classify the extension FUTURE_WORK and notify M2; preserve CHK’s independently verified orthogonal Q1(c) obstruction. |
| IC3 exhibit/check | LH, with actual blocks and \(n\ge9^6\). W1P2 shared-family/cluster-8 rows, W2P2 C6, and CHK §2 supply the checked instantiation and finite inequalities. |
| Numerical companion | None newly run. Proposed: at most ten LH data seeds; compute \(a_n\) by exact convolution and evaluate \((1-a_n)^Q\) analytically. Avoid simulating \(p^2n\) draws. Enumerate small correlated component cases for KL/second-moment inequalities. |
<!-- END VERBATIM -->


---

## M7 · Theorem STG

**Chair's integration note.**
1. K33 enters in its deterministic termination/count form only: the card's clause (a) (termination, ρ_V ≥ 0.9 per appended point, ≤ ℓ rebuilds per tier, T ≤ T_e) and clause (c) (the count). Rebuild convergence N5(b), P(S₀ ∈ V) and P(schedule_limit) → FUTURE_WORK (K31) in either case; Seat D's dissent (K33 in S-IDENT, R3_D §S1) is recorded in MINUTES §2.3.
2. K30 is clause (d), labelled ideal two-state grid, and is stated only here (S-STGI is dissolved). K29 is FUTURE_WORK FW23; its conditional implication may be cited as an attributed lemma.
3. The card's escalation statement: no binding goal rests on STG alone; M2(b) has its own checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1.


**Source:** `theory_campaign/MEET-THM/R3_A.md:139–162` (verbatim)

<!-- BEGIN VERBATIM R3_A.md:139-162 -->
### M7 · Theorem STG (stage laws as coded; coverage identity)

K-IDs: K26, K25, K27, K33, K30 (labelled ideal); K28 cited.

| Field | Content |
|---|---|
| Model/design hypotheses | Admissible (X, y) with positive finite tables, so γ₀ > 0 on Ω; a fixed nonempty V ⊆ Ω; D_V := osc_V d; for (d) a two-state restriction with initial log-odds −A₀ and terminal log-odds bounded away from 0 on the positive side. |
| Implementation premises (named) | EX-A; the coded grid rule (`v3_calib.h`: ESS threshold 0.9 for pilot and grid, P retained pilot targets, 60 halvings, 10⁻¹² snap/validation, T_e cap) equal to its mathematical rule (Python translation checked, no compiled bitwise replay: W1PC1:61); bisection resolution ≤ h_V/2 (2⁻⁶⁰ ≤ h_V/2); "success" is a reported status, with ceiling/snap failures excluded. |
| Statement | (a) Monotonicity and construction: ρ_V(u,v) is nondecreasing in u and nonincreasing in v; bisection accepts only intervals with ρ_V ≥ 0.9; build_grid terminates, every appended point has ρ_V ≥ 0.9, ≤ ℓ rebuilds per tier; T ≤ T_e on success; at exact frontiers the greedy grid is shortest among refinements of the retained pilot targets, up to the 2⁻⁶⁰ slack (no "exact/minimal"). (b) Coverage identity: ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², w = 2v−u, a_t = q_t(V); a_u, a_w ≥ 1−η ⇒ ρ_full ≥ 0.9(1−η)². (c) Interval inequality and count: every accepted interval has (v−u)²·Var_{q_ξ\|V}(d) ≤ log(10/9) for some ξ ∈ [u, 2v−u]; if D_V > 0 every increment ≤ h_V := 2c_ρ/D_V passes (c_ρ = √log(10/9)); with resolution ≤ h_V/2 and absent ceiling/snap failure, T ≤ P + ⌈2/h_V⌉ + 1 = P + ⌈D_V/c_ρ⌉ + 1; a uniform full-space grid (W = Ω) with max{1, ⌈osc_Ω d/(2c_ρ)⌉} stages has full ESS ≥ 0.9 (existence). (c′) Pilot-count clause, cited from M2(b): under a global range bound D_* and 2⁻⁶⁰ ≤ h/2, P ≤ ⌈2/h⌉ + 1, hence T ≤ 2⌈D_*/c_ρ⌉ + 2 ≤ 4 + 2D_*/c_ρ; D_* = 0 ⇒ T = 1 (PROOF SKETCH, Seat C). (d) Ideal grid, labelled, not the coded grid: on the exact-frontier two-state ESS-0.9 grid a dominance crossing of gap A₀ costs log₂A₀ + O(1) stages; separated pair-dominant crossings add; restricted ESS alone forces only log₂(9.5ℓ₀) stages (WS7(d) with the set-mass and endpoint amendments). (e) [cited] √c·T*(c) → Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J as c → 0. (f) The as-coded masked stage count T_n is Conjecture P, OPEN → FUTURE_WORK (K31); the shipped guarantee is T ≤ T_e. Favourable O(1) (K29) → FUTURE_WORK. |
| Verdict rows per clause | (a) W1PC1:190 TRUE; exact/minimal W1PC1:191 COUNTEREXAMPLE repaired; termination/rebuilds W1PC1:198 TRUE; W2PC1:99 TRUE. (b) W1PC1:192 TRUE; PC2 D7 to 10⁻⁸. (c) interval W1PC1:193 TRUE; count W1PC1:194 COUNTEREXAMPLE repaired to P + …; range/resolution W1PC1:195 NEEDS-HYPOTHESIS repaired; W = Ω W1PC1:140; zero range W2PC1:56 repaired max{1,·}. (c′) W2PC2:105, 156 TRUE-AS-WRITTEN (600 coded-pilot runs). (d) W1PC1:197 TRUE; CHK:91 (WS7 amendments). (e) W1PC1:257 (Λ_len renamed). |
| Guarantee | Every accepted stage of the coded grid is certified by an exact restricted-ESS inequality whose full-bridge meaning is the coverage factor; the stage count is bounded by the pilot targets plus the spread of d on V; and on the ideal grid correlation enters depth only through the crossing gap, as log₂A₀. |
| Serves | Objective (2) (island depth); proposal §4.4/§8.2 (what ESS 0.9 certifies); input to M2(b) (sandwich, envelope) and M8 (T); INV rows 5, 7 × C. |
| Status (verbatim) | STG-G, STG-L0, STG-L1: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic (AUTHOR-ONLY, W2PC2:155); STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)), explicit decimal constants GAP (W2PC2 C14); STG-L: PROVED (SF: none; XF: none); ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; OWS-WS7(d): PROVED (SF: none; XF: none) + CHK VERIFIED WITH AMENDMENT; (b), (c): D/E proposals, TRUE-AS-WRITTEN (W1PC1:192–193); (c′): PROOF SKETCH (Seat C, unchecked), W2PC2 TRUE-AS-WRITTEN; STG-F: PROVED (SF: none; XF: none), cited only (K29 FW). |
| Fidelity to v3.1 | (a)–(c), (c′): the coded rule (translation-checked). (d), (e): ideal exact-frontier / fine grid, labelled comparison objects; the gap to the coded grid is K31 (FUTURE_WORK). |
| Self-checked flag | Yes for STG-G/L0/L1/L (author-only) and (b), (c) (statement sanity only); STG-M cross-family VERIFIED*; (c′) unchecked. |
| Novelty | (a)(i) greedy optimality KNOWN—CITE Štefankovič–Vempala–Vigoda 2009 (LIT-SMC row 9); (e) KNOWN—CITE Syed et al. 2024 Thm 3, Gelman–Meng 1998 (LIT-SMC row 15); (b), (c), (d) NEW, elementary (checked LIT-SMC digest; no published restricted-ESS coverage identity found). |
| Route / key lemma | Lemma RS (ρ_V(u,v) = Z_V(u)Z_V(w)/Z_V(v)², convex log-MGF ⇒ monotonicity); second-order mean value for log-sum-exp gives (c); Popoviciu Var ≤ D_V²/4 gives the passing step; bisection invariant keeps the lower endpoint passing; two-point algebra for (d). Key lemma: Lemma RS. |
| Difficulty | S for (a)–(e); (c′) S–M. |
| Lean core | Lemma RS identity; Theorem G optimality among refinements of fixed targets; (b) identity; (c) finite inequality with the Popoviciu step; (d) two-state recurrence bound. |
| Dependencies | S-TARGET (Lemma 0: d finite); M3 (A₀ through π₀(S₀) for (d)); M1(c) (frozen 𝓒); S-IDENT (K25 lemma, K104 for (e)). Feeds M2(b), M8. |
| Risk | The resolution/snap premises; the (c′) pilot-progress lemma unchecked; no compiled replay of the coded rule. |
| Fallback + stop rule | (a), (b), (d), (e) with T ≤ T_e and the interval inequality of (c); drop the counts if the resolution/progress lemma fails. Stop: one wave on (c)/(c′). No binding goal rests on STG alone: M2(b)'s stage-count clause has its own checked fallback T ≤ P + ⌈D_*/c_ρ⌉ + 1. |
| IC3 design, exhibited | (a)–(c): Dε (n = 40, p = 8, built pairs, cross 10⁻⁵–10⁻⁴; W1PC1:71) and my p = 16 exhibit (W2PC1:61), component checks (production dispatches exact); C's family W with the coded pilot replica, 600 adversarial runs (W2PC2:50, 156), SMC-dispatched for n ≥ 9⁶. (d): the truth/start-mode two-state restriction of LH (c = 2), masked (A₀ → ∞). |
| Numerical companion (≤ 20 seeds) | O-STAGES numerics log₂A₀ + 7.7 ± 0.4 (exists); PC2 `c8_pilot.py` (exists); E-pilot 16 cases (W2PC1:55). For the HQ: coded-grid replica on W at n = 9⁶, 10 seeds, T against P + ⌈D_V/c_ρ⌉ + 1 and 2⌈D_*/c_ρ⌉ + 2. |
<!-- END VERBATIM -->


---

## M8 · Proposition D

**Chair's integration note.**
1. K90 is a remark (the card has it as a remark); the Song–Liang §6 comparison is in the same units with no speed claim (MINUTES §2.1).
2. Seat D's note for Felipe (R3_D §S5, MINUTES §2.1): if objective (2) is served by a sentence in the introduction citing the supplement, Prop D moves to the supplement and main = 7. Nothing else changes.
3. The execution-DAG audit (N15) and N14(c) are named implementation premises (MINUTES §2.3).


**Source:** `theory_campaign/MEET-THM/R3_D.md:160–177` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:160-177 -->
### Card Prop D · Proposition D (work, depth and width at the island level) — K87, K88, K89, K06, K64; K90 remark

| Field | Content |
|---|---|
| Final statement | **Units:** sequential elementary-step slots (METHOD §2 #19); score evaluations and memory counted separately. **Hypotheses (design/budget, all explicit functions of (n, p)):** the shipped budgets N₀ = max{2,500, n, p}, H₀ = ⌈512N₀/2,500⌉, L = max{4, ⌈log₂(n + 1)⌉}, ℓ = ⌈log₂(n + p + 1)⌉, T ≤ T_e on success, B = min{⌊√n⌋, ⌊√p⌋, 16}, K; m := p + B + 2; k* := min(K, ⌊p/2⌋); R′ = 4k declared; w island workers. **Implementation premise:** the execution DAG as specified (METHOD §6.8, §8; AMENDMENT_HQ_01 #18, #19, #42); the integrated DAG audit is open. **(a) Final run.** Work = R′·N_e·(T + L + 4)·m slots; island depth = N_e·(T + L + 4)·m, in ⌈R′/w⌉ waves; width R′. With w ≥ R′ the depth does not depend on R′. **(b) Calibration.** Work = Σ_i N_i(T_i + L_i + 4)m over the executed pilot, diagnostic and rebuild trajectories, each with its own grid; per tier at most (1 + 4I_e)H_e trajectories enter work and (1 + I_e)H_e sequential trajectory equivalents enter four-worker depth, I_e ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation). **(c) Searches.** Each local search (final, extra from c₄ when R′ > 4, LS0) scores at most (ℓ + 1)[p + k*(p − k*)] models; each is counted separately. **(d) Polynomial work and scheduling.** For p ≤ n^A, under the budgets above and any permitted polynomial R′, total work is polynomial in n; on w workers, time ≤ W/w + D (Brent). **(e) Ceilings.** Θ(p) slots per round and Θ(p²) Gram memory are not removed by islands or particles. **Remarks (not clauses):** the SL §6 comparison in the same units states worker counts, n-vs-p scaling, T, score cost and the loss criterion, with no same-order, exact-output or speed claim; the single-tier calibration share 0.0512 + 0.2048·I is seat-derived, unchecked; on C's family M7 + M2(b) give T ≤ 4 + 2D_*/c_ρ = O_P(1), so the island depth is O_P(N_e(L + D_*/c_ρ)(p + B)). |
| Guarantee | In a referee's units, islands add width without adding depth; the work is polynomial; accuracy grows with width through M1(b),(d′) at fixed depth; no speed-up over sequential MCMC is claimed. |
| Serves | Objective (2); Song–Liang §6 ("same-unit accounting; speed comparison not established"); THM-INV row 8 (work–depth), I1/I2/I9 ceilings. |
| Status (verbatim) | MA-PropD "PROVED (counting, given the code's structure)" AUTHOR-ONLY; T32(i) "PROVED (SF: VERIFIED (W7-SEC); XF: none)", displayed rate GAP (A-REV5), registry ⚑ CONFLICT marker carried; Cost-T38 "PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))"; calibration share "seat-derived, unchecked" (N15); assembly PROOF SKETCH (by this seat, unchecked). **Fidelity:** island level, v3.1 as shipped; "depth free of N, H, R" struck (MEET-v31 decision 6); K88's particle-parallel critical path is v3.2 and not claimed. |
| Verdict rows used | (a): W1PC2 D6 "final run" TRUE as counting; W2PC2:133 TRUE-AS-WRITTEN (m = p + B + 2; waves); W2PC1:205 TRUE-AS-WRITTEN as corrected accounting. (b): W1PC2 D6 "calibration and LS" TRUE (amendments #18, #42); W2PC2:133; per-trajectory sums repair W1PC1 §13 AMBIGUOUS → REPAIRED (W2PC1:205). (c): W1PC2 D6 TRUE. (d): W1PC1 §13 "polynomial/Brent" TRUE-AS-WRITTEN. (e): W1PC1 §13 first row (memory, block count) DESIGN-VERIFIED on Dε. SL remark: W1PC1 §13 NEEDS-HYPOTHESIS, repaired to a remark (W2PC1:205). |
| Self-checked flag | MA-PropD author-only; T32(i) XF none; calibration share unchecked. Route to a cross-family code read in the charter. |
| Novelty | MODEST (accounting, TCS-standard). Checked: Brent 1974 (cited for W/w + D); Zhou–Yang–Vats–Roberts–Rosenthal 2022 §3 (LIT-MCMC #2): different kernel and per-step cost, no comparison made; Song–Liang 2015 §6 (`theory_campaign/inputs/`): K_n = √P_n, O(P_n^{(1+α)/2}) + O(nP_n), quoted in the remark only. |
| Route / key lemma | Counting over the execution DAG. **Key lemma:** the trajectory inventory (every executed trajectory with its own (N_i, T_i, L_i); every completed search), which is exactly the W1PC1 §13 repair. Difficulty: S (mathematics), M (code audit). |
| Lean core | The counting identity (sum of products over the inventory), the scan bound p + k*(p − k*) ≤ p + p²/4, and Brent's inequality as finite lemmas; low value but certifiable. Nothing rests on probability theory. |
| Dependencies | Uses: M7 (T ≤ T_e; on C's family the M2(b) envelope), S-CERT (K64 search bound), S-OUT (K83 worker equivalence, K84 stacking nesting for the extra search). Used by: the CD remark, COVERAGE_MATRIX §6 row. |
| Risk | The DAG audit finds an uncounted serial component (e.g. a reduction across islands that is not trivially O(R′)), or a calibration path that is not a trajectory sum; then (a)/(b) are restated, not dropped. |
| Fallback + stop rule | Fallback: W and D_PEL as symbolic sums without rates and without the calibration-share remark. Stop: simplification stops at any unaudited component; if the audit shows depth growing with R′ at w ≥ R′, clause (a)'s last sentence is withdrawn and HQ is told (objective (2) wording changes). No binding goal is involved; a p > 2,500 demonstration would fire the C6 trigger and go to HQ. |
| IC3 design (exhibited) | Any admissible input. Checked on Dε (J = 4 blocks, Σ2^{|C_b|} = 16 = p2^B/B; W1PC1 §13 DESIGN-VERIFIED) and on C's family W (W2PC2:133 DESIGN-VERIFIED, any input). |
| Numerical companion (≤ 20 seeds) | Filed: calibration/final ratio predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76 on 3 designs. New: the timing tabulation of AMENDMENT_HQ_01 §4 item 9 (`timings$calibration`, `timings$final`, rebuilds, tier, T) on ≤ 20 saved study fits, compared with (a)–(b) evaluated from the saved budgets; Owls ≤ 8 cores, read-only. |
<!-- END VERBATIM -->


---

# Part II · Supplement cards

For each card: the decision note from MINUTES §2.2, then the statement copied verbatim from the seat card(s) that carry it. Where an R2 seat card says "as R1 §D …" or "unchanged from R1", the pointer to the R1 base card is given; the R1 text is not reproduced.
Seat cards are given in this order: the R3 card if one exists, then C's R2 card (the fullest self-contained statements), then A, B, D.


---

## S-T · Theorem 1, target consistency T03♯ (K93, K04)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:60`):** content = Theorem 1, target consistency T03♯ (K93, K04). Notes and decisions = Unanimous since Round 2; cited in the main text

Registered here as a cited supplement; no HQ work (registered with LP-FOUND). A, B and D file the statement as "unchanged from R1" with scope notes; C filed the full self-contained statement (C9 with its hypotheses table). Compatible; no choice needed.


#### Seat C (R2_C): hypotheses table

**Source:** `theory_campaign/MEET-THM/R2_C.md:148–153` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:148-153 -->
| §R2 — Statistical hypotheses for C9 | Definition |
|---|---|
| R1, R | Fixed-design triangular array, fixed \(s_0\ge1\), \(p\le n^A\) for fixed \(A\), \(s_0\le K\) eventually; G; \(\mu=X\theta^*\), \(\Vert\mu\Vert^2\le Mn\), and normalized truth Gram eigenvalue at least fixed \(\phi_0^2>0\). |
| Tail cutoff | With per-model prior weight \(w(k)\), \(R_m=\sum_{k=\max(m+1,0)}^K\binom pk w(k)/w(s_0)\), and \(m_n^\sharp=\min\{m\ge s_0:R_m\le n^{-(s_0+2)/2}\}\). It is deterministic and data-free. |
| Anchored eigenvalues | \(j_0=\lceil(2A+1)s_0\rceil+1\). SE\(_\lambda(j_0)\): every \(S_0\cup J\), \(\lvert J\rvert\le j_0\), has normalized minimum eigenvalue at least \(\phi_0^2\). SE\(_w(m_n^\sharp;g_0)\): every \(S_0\cup J\), \(\lvert J\rvert\le m_n^\sharp\), has unnormalized minimum eigenvalue at least fixed \(g_0>0\). |
| Signal thresholds | BM-∞: \(\theta_{\min}^{*2}n\phi_0^2/(\sigma^2\log n)\to\infty\). Alternatively BM\((c)\) uses a fixed \(c>c_0(s_0,A)\), with \(c_0=\max\{4C_*,32[s_0(A+1)+2]\}\), \(C_*\) the locked T03 proof constant, exactly as FIX §1.1. |
<!-- END VERBATIM -->


#### Seat C (R2_C): final card C9

**Source:** `theory_campaign/MEET-THM/R2_C.md:155–164` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:155-164 -->
| C9 — K93 | Final card |
|---|---|
| Final statement | Under R1, G, R, SE\(_\lambda(j_0)\), SE\(_w(m_n^\sharp;g_0)\), and BM-∞ or BM\((c>c_0)\), \(1-\pi(S_0)=O_P(\sqrt{\log n/n})\); exact HPM and MPM are consistent. Without beta-min, for \(J_n(c)=\{j\in S_0:\theta_j^{*2}\ge c\sigma^2\log n/(n\phi_0^2)\}\), \(c>c_0\), \(\pi(S\not\supseteq J_n(c))=O_P(\sqrt{\log n/n})\), hence all corresponding exact PIPs converge to one. Empty \(J_n(c)\) gives a vacuous inclusion statement. |
| Repairs | PC1/PC2 statistical clauses: no expectation rate inferred from \(O_P\), no universal onset \(n_0\), no random-design or growing-sparsity extension. |
| Status | T03♯: **PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)**. T02(i♯), T02(ii♯): **PROVED; SF/XF VERIFIED**. |
| Placement | Supplement. |
| Route / key lemma | Cite FIX §1 and the filed exact-prior-tail/selection checks; no re-derivation. |
| Lean core | Finite prior-tail and posterior-to-decision inequalities; Gaussian asymptotics remain prose. |
| Fallback / stop | Fixed-\(p\), uniformly nonsingular correlated design; narrow scope if hypotheses cannot be matched. |
| IC3 | LH satisfies fixed sparsity, bounded energy, positive full Gram eigenvalue and BM-∞. Otherwise unchanged from R1 §D D8. |
<!-- END VERBATIM -->


#### Seat A (R2_A) S1

**Source:** `theory_campaign/MEET-THM/R2_A.md:127` (verbatim) — base statement: R1_A C15 `theory_campaign/MEET-THM/R1_A.md:413`

<!-- BEGIN VERBATIM R2_A.md:127-127 -->
**S1 · Theorem T (K93; K61 remark).** Statement unchanged from R1 §D C15 with the scope sentence (p ≤ n^A from prior and technique; e^{Cn^α} OPEN) and onset n ≳ 2·10⁶. Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement; cited in the main setup. Rest unchanged.
<!-- END VERBATIM -->


#### Seat B (R2_B) S2

**Source:** `theory_campaign/MEET-THM/R2_B.md:165–167` (verbatim) — base statement: R1_B D13 `theory_campaign/MEET-THM/R1_B.md:374`

<!-- BEGIN VERBATIM R2_B.md:165-167 -->
### S2 · Theorem 1, target consistency (K93) · supplement (short)

Final statement unchanged from R1 §D D13 (R1 fixed s₀, p ≤ n^A; G, R, SE_λ, SE_w, BM-∞ or BM(c > c₀); 1 − π(S₀) = O_P(√(log n/n)); HPM/MPM consistent; large-signal inclusion without beta-min). Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued) SAME-FAMILY-ONLY; onset n ≳ 2·10⁶ disclosed. Repairs: none needed (PC1 §12 TRUE). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) M12 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:102` (verbatim) — base statement: R1_D M12 `theory_campaign/MEET-THM/R1_D.md:342`

<!-- BEGIN VERBATIM R2_D.md:102-102 -->
| M12 Theorem 1 (T03♯) — K93, K04 | Unchanged from R1 §D M12; supplement, cited in main text. | "PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))"; T01-T03 "PROVED-LOCKED (wave 3; external review queued)" |
<!-- END VERBATIM -->


---

## S-TARGET · Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:62`):** content = Propriety, invariance, envelopes, exact branch, odds certificate (K01–K05, K76, K95). Notes and decisions = K95 here (R3-4 unanimous)

K95 is here (R3-4, unanimous). Seat statements below are complementary (same content, different packaging).


#### Seat C (R2_C): C12

**Source:** `theory_campaign/MEET-THM/R2_C.md:193–202` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:193-202 -->
| C12 — K01/K02/K03/K04/K05/K76 | Final card |
|---|---|
| Final statement | For finite nonconstant standardized data, \(n\ge3,p\ge1\), the shipped ridge/IG target is proper, including rank-deficient submodels. With \(H_S=(n+1)G_S+I\), \(Q_S=Y-nz_S'H_S^{-1}z_S\), \(Q_S\ge Y/(n+1)\), and \(1\le\det H_S/\det(G_S+I)\le(n+1)^{\lvert S\rvert}\). Thus \(m(S),Z\le U_m=C_n(2b_0+Y/(n+1))^{-\nu}\), where \(C_n\) is the shipped score’s common prefactor. |
| Other clauses | Use the normalized capped prior once. Target probabilities are invariant under admissible affine rescaling and equivariant under column permutation. The contrast reduction uses IG shape \(a_0+1/2\), rate \(b_0s_y^2\). Real-arithmetic exact enumeration returns exact summaries; every fixed-\(p\) sequence eventually enters that branch. |
| Repairs | PC2 status repair; target equivariance only. The pairwise IG perturbation coefficient is \(2\nu b_0\), not universally \(nb_0\). |
| Status | N17: **PROVED**. T01: **PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY**. Remaining assembly: **PROOF SKETCH, unchecked**. |
| Placement | Supplement. |
| Route / Lean | Checked spectral envelope and reduction; finite normalization/enumeration. |
| Fallback / stop | Proper target and exact-arithmetic enumeration; no machine-certification claim. |
| IC3 | C10’s duplicated, rank-deficient correlated design. |
<!-- END VERBATIM -->


#### Seat A (R2_A) S5

**Source:** `theory_campaign/MEET-THM/R2_A.md:135` (verbatim) — base: R1_A C1 `theory_campaign/MEET-THM/R1_A.md:162`

<!-- BEGIN VERBATIM R2_A.md:135-135 -->
**S5 · Proposition TARGET (K01–K05, K76).** As R1 §D C1 with (ii) restricted to the target (affine invariance, permutation equivariance); algorithmic equivariance in law only for a tie-free partition and decision structure (PC1:301); K05 superset bound; K76 eventual exact dispatch (N12 seat-proved, unchecked); (iii) constant 2νb₀ (PC2:216; PC1:300). Status: N17 PROVED; rest D/E proposals, TRUE-AS-WRITTEN (PC1:300); T01 reduction PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement.
<!-- END VERBATIM -->


#### Seat A (R2_A): K95 odds-certificate clause (from A's Z𝒯 card, clause (f))

**Source:** `theory_campaign/MEET-THM/R2_A.md:89` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_A.md:89 -->
(f) odds certificate: π(S₀) = 1/(1+A(S₀)); A ≤ η < 1 ⇒ HPM = MPM = S₀ (PC1:130).
<!-- END VERBATIM -->


#### Seat B (R2_B) S7

**Source:** `theory_campaign/MEET-THM/R2_B.md:185–187` (verbatim) — base: R1_B D17 `theory_campaign/MEET-THM/R1_B.md:438`

<!-- BEGIN VERBATIM R2_B.md:185-187 -->
### S7 · Proposition TARGET (K01, K02, K03, K04, K95, K76) · supplement

Final statement as R1 §D D17 with: target affine-invariant and permutation-equivariant; algorithmic output need not be equivariant, even in law, under index ties (PC1 §20); A(S₀) ≤ η < 1 ⇒ HPM = MPM = S₀ (PC1 §20 NEEDS-HYPOTHESIS conceded); 2νb₀ as the exact pairwise IG constant (PC2 cluster 20). Status: N17: PROVED (PC1 claim 1); T01 reduction: PROVED-LOCKED (wave 3; external review queued); N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) S1 and S3 rows (K95 with "η < 1 stated"), S12 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:105` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:105-105 -->
| S1 target lemmas — K01–K04 (+K76, K95 via S3/S12) | Target invariance and permutation equivariance; algorithmic equivariance in law only without partition/decision ties (cluster 20). | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:107` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:107-107 -->
| S3 decision rules — K62 moved to H′(f); K60, K61 cited; K95, K101 | η < 1 stated (cluster 20). | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:116` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:116-116 -->
| S12 fixed p/tiny n — K76, K02 | unchanged | N12 "seat-proved, unchecked" |
<!-- END VERBATIM -->


---

## S-BLOCKS · Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:68`):** content = Separation ⇒ groups kept; SIZE ⇒ equality (K07, K14, K06). Notes and decisions = —

Seats agree; C11 is the fullest. A files it inside S10 (BLOCKS part), D inside the S2 row.


#### Seat C (R2_C): C11

**Source:** `theory_campaign/MEET-THM/R2_C.md:183–191` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:183-191 -->
| C11 — K07/K06/K22 | Final card |
|---|---|
| Final statement | Suppose every within-group distance is strictly smaller than every between-group distance and every group has size at most \(B\). Complete linkage forms each group before cross-group merging; cutting and whole-cluster packing preserve groups. If additionally \(B<2g_{\min}\), output blocks equal groups. For actual blocks, \(\lceil p/B\rceil\le J\le2\lceil p/B\rceil\), \(\sum_b2^{\lvert C_b\rvert}\le p2^B/B\); the symmetrized capped graph has at most \(pB\) edges and no isolated vertex when \(p>1\). |
| Repairs | PC2 Shared objects and cluster 4: replace unqualified eventual recovery by \(n\ge9^6\) for both nine-variable exhibits. PC1 cluster 6: explicit SIZE. |
| Status | PART-ThmA: **PROVED; SF none; XF VERIFIED***. Counting/graph assembly: **PROOF SKETCH, unchecked**. PART-pairing remains **OPEN**, excluded. |
| Placement | Supplement. |
| Route / Lean | Cite checked separation/packing result; finite partition, bin-count and graph-union arguments. |
| Fallback / stop | Group preservation and deterministic counts only; no size-five pairing law. |
| IC3 | W and LH satisfy strict separation and \(9\le B\le16<18\) for \(n\ge9^6\). Otherwise unchanged from R1 §D D10. |
<!-- END VERBATIM -->


#### Seat B (R2_B) S11

**Source:** `theory_campaign/MEET-THM/R2_B.md:201–205` (verbatim) — base: R1_B D21 `theory_campaign/MEET-THM/R1_B.md:484`

<!-- BEGIN VERBATIM R2_B.md:201-205 -->
### S11 · Proposition BLOCKS (K07, K14, K06) · supplement

Unchanged from R1 §D D21 (PC1 §19 B.D21 TRUE-AS-WRITTEN; preservation only, equality needs SIZE). Status: PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; PART-CE2: COUNTEREXAMPLE.

Dropped from the list since R1: D10 (CD → remark), D20 (K94 → FUTURE_WORK).
<!-- END VERBATIM -->


#### Seat A (R2_A) S10 (KL/TV and BLOCKS; the BLOCKS part is the last clauses)

Reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_A.md:145`).


#### Seat D (R2_D) S2 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:106` (verbatim) — base: R1_D S2 `theory_campaign/MEET-THM/R1_D.md:391`

<!-- BEGIN VERBATIM R2_D.md:106-106 -->
| S2 start machinery — K06, K07, K09, K14, K22 | Graph "no isolated vertex" for p ≥ 2 (cluster 19); K07 preservation only, equality under SIZE. | unchanged |
<!-- END VERBATIM -->


---

## S-KERNEL · N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:63`):** content = N9 kernel facts, graph (p ≥ 2), start sampler, minorisation (K20, K21, K08, K09, K22, K103). Notes and decisions = N9 with CHK amendments. K09 is the tie-DP proposition (C10)

N9 with the CHK amendments (`evidence/CHK_INHERITED/REPORT.md` §5, VERIFIED WITH AMENDMENT). K09 is the tie-DP proposition, C10 (MINUTES). **K23 (R3-4):** FUTURE_WORK (A, B, D); C dissents and would keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL (R3_C §S1, `theory_campaign/MEET-THM/R3_C.md:59`). Recorded; the HQ of S-KERNEL may cite it as an attributed lemma without a theorem number. The Dirichlet-form clause ℰ_Q ≥ ½ℰ_{R₂} appears in seats A (S10) and B (S5) as filed; it is K23 and is not a numbered supplement claim.


#### Seat B (R2_B) S5

**Source:** `theory_campaign/MEET-THM/R2_B.md:177–179` (verbatim) — base: R1_B D16 `theory_campaign/MEET-THM/R1_B.md:422`

<!-- BEGIN VERBATIM R2_B.md:177-179 -->
### S5 · Proposition KERNEL (K20, K21, K08, K09, K22, K23, K103) · supplement, cited lemma + Lean

Final statement as R1 §D D16 with: reversibility under the sufficient conditions of N9 (a fixed order need not be self-adjoint); the graph clause for p ≥ 2 (PC1 §19); Q_φ(S,·) ≥ π_φ/M_φ (E's constant 1/M_φ, PC1 §19 TRUE; 1/(mM_φ) also valid) and ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/M_φ)^k with M_φ ≤ exp{φ·osc d}; ℰ_Q ≥ ½ℰ_{R₂}, R₂ = (1/m)ΣP_j²; tie-aware DP returns the prescribed maximiser (N3 OPEN, hypothesis). Status: N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. Rest unchanged.
<!-- END VERBATIM -->


#### Seat C (R2_C): C10 (K09, tie-DP proposition)

**Source:** `theory_campaign/MEET-THM/R2_C.md:166–175` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:166-175 -->
| C10 — K09 | Final card |
|---|---|
| Final statement | For positive finite block tables, size-only capped prior and exact comparisons, max-plus convolution gives the best start score at each size. Choose the smallest maximizing size. In ascending index order, include an index exactly when an optimal completion of that size consistent with the existing prefix remains possible. The result is the prescribed lexicographically smallest start maximizer. |
| Repairs | PC2 §0/D9: the new duplicate-column exhibit below puts the tie at the global start mode, not merely somewhere in a table. |
| Status | Proposed finite mathematical proposition: **PROOF SKETCH, unchecked**. Registry N3’s integrated tie-DP invariant remains **OPEN**; it is not being listed as a proved implementation theorem. |
| Placement | Supplement. |
| Route / key lemma | Optimal-completion invariant and prefix induction. |
| Lean core | Finite constrained maximization and lexicographic order. |
| Fallback / stop | Unique-maximizer instances. If the prefix invariant fails, drop the tie proposition and retain the integration gap. |
| IC3 | \(n=40,p=20\); columns 1 and 2 identical; remaining columns mutually orthogonal and orthogonal to them. Standardized \(y\) has squared correlation \(1/2\) with the duplicate direction and zero with other columns. Complete linkage keeps the duplicate pair together; adding zero-score columns decreases the start score. The two singleton duplicates are tied global modes; SMC dispatch holds. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C10 allowed scratch check (reproduction, as filed)

**Source:** `theory_campaign/MEET-THM/R2_C.md:177–181` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:177-181 -->
| C10 — Allowed scratch check | Reproduction |
|---|---|
| Script, Python, `/tmp`, no seeds | `import math`<br>`n,p,Y=40,20,39`<br>`nu=.01+n/2`<br>`z2=Y*Y*.5`<br>`for k in (0,1,2):`<br>`    gain=0 if not k else n*k*z2/(1+(n+1)*k*(n-1))`<br>`    det=1 if not k else (1+(n+1)*k*(n-1))/(1+k*(n-1))`<br>`    logbf=-.5*math.log(det)-nu*math.log1p(-gain/(.02+Y))`<br>`    prior=math.lgamma(k+1)+math.lgamma(2*p-k)-math.lgamma(2*p)`<br>`    print(k, 'log_start_relative_to_empty=', round(logbf+prior,9))`<br>`print('models=',2**p,'dispatch_cutoff=',200000+64*n*p)` |
| Output | `0 log_start_relative_to_empty= 0.0`<br>`1 log_start_relative_to_empty= 7.858020937`<br>`2 log_start_relative_to_empty= 4.91339373`<br>`models= 1048576 dispatch_cutoff= 251200` |
| Interpretation | Scalar sanity check of the exhibit, not a DP implementation audit or an exact floating-point certificate. The singleton equality follows from identical columns. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-TV (K103 minorisation / terminal-law TV)

Reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_C.md:224`–`232`).


#### Seat A (R2_A) S6 (PAR incl. K09) and S10 (minorisation, graph, Dirichlet form)

**Source:** `theory_campaign/MEET-THM/R2_A.md:137` (verbatim) — base: R1_A S1 `theory_campaign/MEET-THM/R1_A.md:489`

<!-- BEGIN VERBATIM R2_A.md:137-137 -->
**S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
<!-- END VERBATIM -->

A's S10 is reproduced verbatim once, under **S-IDENT** below (`theory_campaign/MEET-THM/R2_A.md:145`).


#### Seat D (R2_D) S2 and S8 rows

**Source:** `theory_campaign/MEET-THM/R2_D.md:106` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:106-106 -->
| S2 start machinery — K06, K07, K09, K14, K22 | Graph "no isolated vertex" for p ≥ 2 (cluster 19); K07 preservation only, equality under SIZE. | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:112` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:112-112 -->
| S8 Doeblin/calculus — K103, K104, K108 | TV ≤ (1 − 1/M_φ)^L with the shipped L = max(4, ⌈log₂(n+1)⌉) → ∞; useful iff M₁ = O(1). | PC2 D15-TV TRUE |
<!-- END VERBATIM -->


#### Seat D (R2_D) validity statement (the N9 statement, H′(a))

**Source:** `theory_campaign/MEET-THM/R2_D.md:56` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:56-56 -->
- Statement. Under EX-A, EX-S, CAL, GUARD-W, R′ declared. (a) Validity: each Gibbs flip, uniform swap, neighbour swap and independence move is γ_φ-reversible, the uniformly random-order round is γ_φ-invariant and self-adjoint, draw_pi0 and Z̄₀ are exact (N9, cited); conditionally on frozen 𝓒, E[Ẑ_r] = Z, E[Ẑ_r PIP̂_rj] = Z·PIP_j (locked), and E[Ẑ_r H_r(h)] = Z·π(h) for h ∈ 𝓗 measurable in (X, y, 𝓒) (N1). Potential-run statements; the intersection inequalities P(𝒪 ∩ B) ≤ P_pot(B) transfer by Lemma RO + GUARD-W; expectations do not (D.M1(c) repair). (b) For 0 ≤ h ≤ 1, M₂ = E[W_r²|𝓒]: P(|μ̂(h) − π(h)| > ε | 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)} (PC1c3). (c) Joint inclusions h_A = 1{A ⊆ S} (plain averages, c_h = 0); predeclared h_I(S) = P(β_j ∈ I | S, X, y) for a finite endpoint grid, with a union bound over the grid (cluster 16 repair: no "any interval"). (d′) Growth clause: on any family with osc d = O_P(1) (model/design condition) and R′(n,p) = 4ℓ(n,p), ℓ = ⌈log₂(n+p+1)⌉, under T03♯: μ̂(h) → h(S₀) jointly with output. (e) Fixed data: μ̂(h) → π(h) a.s. as R′ → ∞ (cited). (f) MPM margin: if every exact PIP is ≥ δ from ½ and the estimated PIPs err < δ, the reported MPM equals the exact MPM (K62).
<!-- END VERBATIM -->


---

## S-IDENT · Restricted-ESS coverage identity, TI/KL/TV calculus, C15-CI clause (K25 lemma, K104, K55, K103)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:67`):** content = Restricted-ESS coverage identity, TI/KL/TV calculus, **C15-CI posterior-content credible-set clause, named** (K25 lemma, K104, K55, K103). Notes and decisions = Seat B's "missing" item 1 (R3_B §S4) adopted: HQ Q2's posterior-content reading needs a named clause

**C15-CI is named as a clause of this card** (MINUTES; B's "missing" item 1, R3_B `theory_campaign/MEET-THM/R3_B.md:314`; C's required correction, R3_C `theory_campaign/MEET-THM/R3_C.md:318`). It is the HQ Q2 deliverable: posterior-content error, not frequentist coverage (FW1). K33 is not here (M7; D's dissent recorded in MINUTES §2.3). The minorisation constant is 1/M_φ in A, B, C and D (B notes 1/(mM_φ) is also valid); compatible.


#### Seat C (R2_C): C15-TV

**Source:** `theory_campaign/MEET-THM/R2_C.md:224–232` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:224-232 -->
| C15-TV — K103 | Final card |
|---|---|
| Final statement | Under A, \(M_\phi=\max_Sq_\phi(S)/\pi_0(S)\). The complete production round minorizes \(q_\phi\) by \(1/M_\phi\), without a \(1/m\) factor. Thus a terminal particle’s marginal law after \(L\) terminal rounds has TV at most \(q^L\), \(q=1-1/M_1\). For a predeclared partition into \(d_0\) cells, \(P(TV(\widehat\pi_{\rm cell},\pi_{\rm cell})>\epsilon\mid\mathcal C)\le\min\{1,4(M_2-1)/R'+4d_0M_2/(R'\epsilon^2)\}\). |
| Repairs | PC2 cluster 16 and §0 item 4: distinguish marginal law from realized empirical law; label default-\(4\) bound vacuous. Full-state TV uses singleton cells and may be useless. |
| Status | Production-round/record assembly: **PROOF SKETCH, unchecked**. Independence-sampler foundation: **KNOWN—CITE**. |
| Placement | Supplement, one package with C15-KL/CI. |
| Route / Lean | Cite PC2’s checked minorization/vector-ratio clauses; compose minorization through invariant kernels. |
| Fallback / stop | Coarsened TV and bounded-functional error; no useful masked full-TV claim. |
| IC3 | W gives \(M_1\le e^{D_*}=O_P(1)\); §R6 supplies explicit \(L,R'\). |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-KL

**Source:** `theory_campaign/MEET-THM/R2_C.md:234–242` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:234-242 -->
| C15-KL — K103/K104 | Final card |
|---|---|
| Final statement | Under C15-TV, \(\lambda_L=(1-q^L)\pi+q^L\nu_L\). Consequently \(KL(\pi\Vert\lambda_L)\le-\log(1-q^L)\) and \(KL(\lambda_L\Vert\pi)\le q^L\log(1/\pi_{\min})\). Also \(KL(\widehat\pi\Vert\pi)\le4TV(\widehat\pi,\pi)^2/\pi_{\min}\), with the corresponding minimum cell mass for coarsenings. If any positive-posterior state is absent, \(KL(\pi\Vert\widehat\pi)=\infty\); in particular this occurs surely when \(\lvert\Omega\rvert>4NR'\). |
| Repairs | PC2 cluster 16; HQ Q3: reverse empirical KL obstruction retained, useful masked final-TV/KL not claimed. |
| Status | **PROOF SKETCH, unchecked** assembly; elementary divergence foundations cited. |
| Placement | Supplement, C15 package. |
| Route / Lean | Cite checked mixture/log-sum clauses; finite support and convexity. |
| Fallback / stop | Fixed-data directional bounds. No forward-KL convergence rate without controlling \(\pi_{\min}\); no silent smoothing. |
| IC3 | Every finite admissible correlated design for inequalities; W for terminal reverse-KL convergence. Otherwise unchanged from R1 §F D15-KL. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15-CI (the named posterior-content credible-set clause)

**Source:** `theory_campaign/MEET-THM/R2_C.md:244–253` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:244-253 -->
| C15-CI — K103 | Final card |
|---|---|
| Final statement | Under C15-TV, for any possibly output-selected union \(C\) of the chosen cells and nominal content \(1-\alpha\), \(\lvert\pi(C)-(1-\alpha)\rvert\le TV(\widehat\pi_{\rm cell},\pi_{\rm cell})+\lvert\widehat\pi(C)-(1-\alpha)\rvert\). Therefore the probability, jointly with \(\mathcal O\) under GUARD-W, that the left side exceeds \(\epsilon\) plus the observed nominal-content discrepancy is bounded by C15-TV’s tail bound. |
| Available interval | Use model-size cells, \(d_0=K+1\), and an interval selected from the existing size distribution. Discrete overshoot is retained explicitly; estimated content need not equal nominal content. |
| Repairs | HQ Q2 and PC1/PC2 cluster 16: absolute posterior-content deviation, not frequentist coverage. A pointwise fixed-\(h\) bound does not validate arbitrary selected sets. |
| Status | **PROOF SKETCH, unchecked**. |
| Placement | Supplement, C15 package. |
| Route / Lean | Simultaneous cell-law control and deterministic set-mass inequality. |
| Fallback / stop | Predeclared interval endpoints with simultaneous CDF bounds; unavailable historical records remain unavailable. |
| IC3 | W with §R6’s stacking rate and actual size-distribution records. |
<!-- END VERBATIM -->


#### Seat C (R2_C): C15 empirical TV/content and terminal-law rows (agenda 7)

**Source:** `theory_campaign/MEET-THM/R2_C.md:324` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:324-324 -->
| C15 empirical TV/content | The same \(R'_n\) handles any predeclared coarsening with \(d_0\le s^2\), including model size. It does not make singleton full-state TV informative when \(\lvert\Omega\rvert\) is exponential. |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_C.md:325` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:325-325 -->
| C15 terminal law | On W, \(M_1\le e^{D_*}=O_P(1)\); the existing logarithmic \(L\) gives terminal marginal TV and reverse-KL convergence in probability. Forward-KL convergence additionally needs control of \(\log(1/\pi_{\min})\), which is not supplied. |
<!-- END VERBATIM -->


#### Seat B (R2_B) S9

**Source:** `theory_campaign/MEET-THM/R2_B.md:193–195` (verbatim) — base: R1_B D19 `theory_campaign/MEET-THM/R1_B.md:460`

<!-- BEGIN VERBATIM R2_B.md:193-195 -->
### S9 · Proposition IDENT (K25, K104, K54, K55) · supplement

Final statement as R1 §D D19 with Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J (the length, not the cumulant Λ(1); PC1 §16 AMBIGUOUS). Status: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none); PC1 §14, §16 TRUE-AS-WRITTEN. Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S10 (exponential-family identities, Λ_len, minorisation, Dirichlet form)

**Source:** `theory_campaign/MEET-THM/R2_A.md:145` (verbatim) — base: R1_A S4 `theory_campaign/MEET-THM/R1_A.md:546`

<!-- BEGIN VERBATIM R2_A.md:145-145 -->
**S10 · Proposition KL/TV and BLOCKS (K104, K103, K07, K14, K22).** Exponential-family identities with the length Λ_len := ∫sd_{q_φ}(d)dφ ≤ √J (renamed; PC1:257); minorisation Q_φ(S,·) ≥ π_φ/M_φ (constant 1/M_φ, PC1:290; PC2:184), vacuous under masking; Dirichlet form ℰ_Q ≥ ½ℰ_{R₂} with R₂ = (1/m)ΣP_j² (PC1:289); graph: ≤ pB edges, no isolated vertex for p ≥ 2 (PC1:291); strict-gap preservation (PART-ThmA) and the SIZE equality clause; every block sub-model is scored. Supplement. Status: D/E proposals TRUE-AS-WRITTEN at the cited rows; OWS-WS1 PROVED (no review).
<!-- END VERBATIM -->


#### Seat D (R2_D) S8 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:112` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:112-112 -->
| S8 Doeblin/calculus — K103, K104, K108 | TV ≤ (1 − 1/M_φ)^L with the shipped L = max(4, ⌈log₂(n+1)⌉) → ∞; useful iff M₁ = O(1). | PC2 D15-TV TRUE |
<!-- END VERBATIM -->


---

## ~~S-STGI~~ · DISSOLVED (MINUTES §2.2, corrected): K30 is M7(d); K29 → FUTURE_WORK FW23. Seat texts are kept below for reference only; they are not list claims

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:70`):** content = Ideal two-state crossing depth (K30 restated); **K29 only as a cited conditional implication** under (LL) or the over-tilted q_w bound. Notes and decisions = Its unconditional favourable application → FW. B (FW) and C (conditional cited) prevail over A and D (supplement conditional), whose substance is the same conditional implication

Placement per MINUTES: B (FW) and C (conditional cited) prevail over A and D (supplement conditional), whose substance is the same conditional implication. The unconditional favourable application is FUTURE_WORK (see `FUTURE_WORK.md`). K29 is stated here only as a cited implication under (LL) or the over-tilted q_w bound. Where seats word the K29 implication or K30 differently, all are shown. Wording: see "Chair's choices" items 1–2 at the end of this file.


#### K30 as stated in the main card M7(d) (R3_A §S2 M7), labelled ideal grid

**Source:** `theory_campaign/MEET-THM/R3_A.md:147` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R3_A.md:147 -->
(d) Ideal grid, labelled, not the coded grid: on the exact-frontier two-state ESS-0.9 grid a dominance crossing of gap A₀ costs log₂A₀ + O(1) stages; separated pair-dominant crossings add; restricted ESS alone forces only log₂(9.5ℓ₀) stages (WS7(d) with the set-mass and endpoint amendments).
<!-- END VERBATIM -->


#### Seat C (R2_C): C14 (K30)

**Source:** `theory_campaign/MEET-THM/R2_C.md:214–222` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:214-222 -->
| C14 — K30 | Final card |
|---|---|
| Final statement | For the ideal positive two-state exponential bridge, initial log odds \(-A\), \(A\to\infty\), and terminal log odds on the positive side bounded away from zero, use the exact maximal-increment ESS-.9 grid in STG-M’s scope. Its crossing cost is \(\log_2A+O(1)\). |
| Repairs | PC1/PC2 cluster 9: retain ideal-grid and endpoint qualifications; do not assert exact/minimal coded-grid equality. |
| Status | STG-M: **PROVED; SF none; XF VERIFIED*** for logarithmic order; explicit decimal constants **GAP**. |
| Placement | Supplement. |
| Route / Lean | Cite checked two-state recurrence; finite normalizer algebra and recurrence bounds. |
| Fallback / stop | This ideal comparison theorem only. K31 remains FUTURE_WORK. |
| IC3 | The truth/start-mode two-state restriction on LH has the needed odds reversal. This is explicitly a comparison object, not the full regression posterior or coded grid. Otherwise unchanged from R1 §D D13. |
<!-- END VERBATIM -->


#### Seat A (R2_A) S11 (K29 under (LL); K30)

**Source:** `theory_campaign/MEET-THM/R2_A.md:147` (verbatim)

<!-- BEGIN VERBATIM R2_A.md:147-147 -->
**S11 · STG-ideal (K29, K30).** K30: ideal two-state exact-frontier grid, log₂A₀ + O(1) (STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); crossings add only when separated and pair-dominant, PC1:197). K29: favourable T* = O(1) under STG-F **with (LL)** or the over-tilted q_w bound as hypothesis (PC1:196; STG-F: PROVED (SF: none; XF: none); STG-Wp: PROVED-UNDER, conflict C22). Supplement, labelled ideal grid.
<!-- END VERBATIM -->


#### Seat B (R2_B): STG card M7 final-statement row, clauses (d) K30 and (f) K29

**Source:** `theory_campaign/MEET-THM/R2_B.md:139` (verbatim) — clause (f) is the K29 supplement clause

<!-- BEGIN VERBATIM R2_B.md:139-139 -->
| Final statement | Grid rule as coded, ESS threshold ρ̄ = 0.9 on V for pilot and grid (hypothesis), P pilot targets, D_V := osc_V d > 0. (a) ρ_V(u,v) is nonincreasing in v; the coded bisection accepts only intervals with ρ_V ≥ 0.9; T ≤ T_e on success. (b) [Lemma K25] ρ_full(u,v) = ρ_V(u,v)a_u a_w/a_v², w = 2v−u. (c) every accepted interval satisfies (v−u)²Var_{q_ξ\|V}(d) = log(1/ρ) ≤ log(10/9) for some ξ ∈ [u, 2v−u]; every increment ≤ h := 2√log(10/9)/D_V passes; with bisection resolution ≤ h/2 the coded grid has T ≤ P + ⌈2/h⌉ + 1 insertions, absent ceiling/snap failure. (d) ideal two-state exact-frontier grid (not the coded grid): a dominance crossing of log-odds gap A₀ costs log₂A₀ + O(1) stages. (e) [cited] √c·T*(c) → Λ_len as c → 0. (f) [supplement] favourable O(1) stages under STG-F's over-tilted q_w bound or LL. |
<!-- END VERBATIM -->


#### Seat D (R2_D): STG′ statement (K30 as (c); K29 conditional on (LL) or the over-tilted q_w bound)

**Source:** `theory_campaign/MEET-THM/R2_D.md:82` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:82-82 -->
- Statement. Grid rule as coded, ESS 0.90 pilot and grid (hypothesis). (a) The ESS criterion is monotone in both endpoints (increasing in u, decreasing in v); each accepted interval satisfies ρ_V ≥ 0.9; bisection terminates; T ≤ T_e on success. Optimality only among refinements of the retained pilot targets, with 2^{−60} slack (cluster 9: "exact/minimal" dropped). (b) ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², w = 2v−u, a_t = q_t(V); a_u, a_w ≥ 1−η ⇒ ρ_full ≥ 0.9(1−η)². (c) Masked two-state ideal grid: T* = log₂A₀ + O(1) (STG-M, ideal grid, labelled). (d) √c·T*(c) → Λ_len = ∫sd_φ(d)dφ ≤ √J (cited; the length, not the cumulant Λ). Favourable O(1) stages (K29) only under (LL) or the over-tilted q_w bound: supplement. As-coded masked T_n: FUTURE_WORK (K31); fallback T ≤ T_e.
<!-- END VERBATIM -->


#### Seat D (R2_D) S10 row (calibration K33, K27; K29 conditional)

**Source:** `theory_campaign/MEET-THM/R2_D.md:114` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:114-114 -->
| S10 calibration — K33, K27 | unchanged; obligations → FUTURE_WORK (K31). | N5(b) "OPEN" |
<!-- END VERBATIM -->


#### Round 3 objections to K29 as a numbered item (for the record)

**Source:** `theory_campaign/MEET-THM/R3_A.md:43` (verbatim)

<!-- BEGIN VERBATIM R3_A.md:43-43 -->
| S-STGI (K29, K30) | **object: dissolve.** K30 → M7(d) labelled ideal grid (the chair's M7 row already lists it); K29 → FUTURE_WORK | K29 fails IC3: (LL) is not a model/design condition and no family exhibits it (W2PC1:187 DESIGN-ASSERTED, GAP) | A design family on which (LL) or the over-tilted q_w bound is verified; then K29 returns as a supplement clause. |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R3_B.md:61` (verbatim)

<!-- BEGIN VERBATIM R3_B.md:61-61 -->
| S-STGI (K29 conditional on (LL); K30 ideal) | **object on K29** | (LL)/the over-tilted q_w bound is not a model/design condition and no family satisfying it has been exhibited (W2PC1 A.S11: DESIGN-ASSERTED, GAP). IC3 fails; a list item cannot be conditional on an unexhibited hypothesis. K30 is already M7(d); state it once. | An exhibited design family satisfying (LL), checked in one wave: then K29 returns as a supplement clause. Until then FUTURE_WORK. |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R3_C.md:40` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:40-40 -->
| §2.2 S-STGI | Object to K29 as a numbered contribution | Its LL/over-tilted input lacks an exhibited model/design route: W2P1 A.S11 is DESIGN-ASSERTED/GAP. Cite the conditional implication; defer its unconditional favourable-regime application. Keep K30 as the ideal-grid result. | A checked IC3 family establishing the missing input. |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R3_D.md:45` (verbatim)

<!-- BEGIN VERBATIM R3_D.md:45-45 -->
| S-STGI (K29 conditional on (LL), K30 ideal) | confirm K29 here; K30 also stated as M7's labelled clause (c) (R3-8) | — | none |
<!-- END VERBATIM -->


---

## S-CERT · Local search, certificate semantics, B&B soundness, perturbation lemma (K64, K73 without region-certification clause, K74, K05, K108)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:64`):** content = Local search (weak local maximum, ties allowed), certificate semantics, B&B soundness, perturbation lemma (K64, K73 without the region-certification clause, K74, K05, K108). Notes and decisions = K73 per C's withdrawal (R3-8)

K73 per C's withdrawal of the operational region certification (R3-8). K107 (rounding bound) is FUTURE_WORK (N16 OPEN); K108 (deterministic perturbation lemma) stays. Seats A and B state the same card; D files it as the S9 row.


#### Seat B (R2_B) S8

**Source:** `theory_campaign/MEET-THM/R2_B.md:189–191` (verbatim) — base: R1_B D18 `theory_campaign/MEET-THM/R1_B.md:449`

<!-- BEGIN VERBATIM R2_B.md:189-191 -->
### S8 · Proposition CERT (K64, K73, K05, K108) · supplement

Final statement as R1 §D D18 with: `local_certified` = no strictly improving feasible flip or swap at the scanned centre (weak local maximum; ties allowed) (PC1 §17 COUNTEREXAMPLE conceded); B&B exact when it completes, "unresolved" otherwise, in exact arithmetic; log-mass perturbation ε ⇒ Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, winners with gap > 2ε unchanged. The rounding bound (K107) is withdrawn to FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). Status: N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*). Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S8

**Source:** `theory_campaign/MEET-THM/R2_A.md:141` (verbatim) — base: R1_A C16 `theory_campaign/MEET-THM/R1_A.md:432`

<!-- BEGIN VERBATIM R2_A.md:141-141 -->
**S8 · Proposition CERT (K64, K73, K74, K05, K108).** `local_certified` = no strictly improving feasible flip/swap neighbour at the scanned centre (weak local maximum; ties allowed; PC1:272); ≤ (ℓ+1) scans of ≤ p + k*(p−k*) models per search; card R (OCERT-C4 + Lemma M) exact on completion, "unresolved" on exhaustion, nothing outside U; perturbation lemma (Z̃/Z ∈ e^{±ε}, TV ≤ tanh ε, winner gap > 2ε); limitation CEX-localmax(A2), CEX2. K107 → FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). Status unchanged from R1 §D C16/S4. Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S9 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:113` (verbatim) — base: R1_D S9 `theory_campaign/MEET-THM/R1_D.md:475`

<!-- BEGIN VERBATIM R2_D.md:113-113 -->
| S9 search/certificates — K64, K73, K74, K05, K108 | K107 rounding bound → FUTURE_WORK (cluster 17); K108 deterministic perturbation lemma stays. | N16 "OPEN" |
<!-- END VERBATIM -->


---

## S-OUT · Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:69`):** content = Output-event validity, worker equivalence, stacking (K77, K78, K83–K86, K63). Notes and decisions = K63/K86 are also named as premises in M1/M5

K63/K86 are also named as premises in M1 and M5. Seat B has no S-OUT card in Round 2 (R3_B places K63/K86 in hypotheses, `theory_campaign/MEET-THM/R3_B.md:60`). Cards below are complementary.


#### Seat C (R2_C): C13

**Source:** `theory_campaign/MEET-THM/R2_C.md:204–212` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:204-212 -->
| C13 — K77/K78 | Final card |
|---|---|
| Final statement | Under A and stop-only statistical coupling GUARD-W, a potential-run event \(B\) satisfying \(P(B\mid\mathcal C)\le\alpha\) gives \(P(\mathcal O\cap B\mid\mathcal C)\le\alpha\). It does not imply \(P(B\mid\mathcal O,\mathcal C)\le\alpha\). |
| Repairs | PC2 cluster 3; preserve actual statistical-output scope and the unaudited integrated coupling. |
| Status | LemmaRO: **PROVED; SF VERIFIED; XF VERIFIED***. CEX-guard: **COUNTEREXAMPLE; XF VERIFIED***. N6 potential-run: **PROVED**; output form: **CORRECT WITH AMENDMENT**. GUARD-W: **not audited**. |
| Placement | Supplement. |
| Route / Lean | Cite filed coupling/event-containment result; finite probability core. |
| Fallback / stop | Potential-run theorem while the audit remains open. Never replace it with completion-conditioned validity. |
| IC3 | Any admissible correlated input; unchanged from R1 §D D12 apart from explicit audit qualification. |
<!-- END VERBATIM -->


#### Seat D (R2_D) S4 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:108` (verbatim) — base: R1_D S4 `theory_campaign/MEET-THM/R1_D.md:420`

<!-- BEGIN VERBATIM R2_D.md:108-108 -->
| S4 worker/stacking/output — K63, K83–K86, K77, K78 | "Adaptive R′ need not preserve the bounds" (cluster 3). | unchanged |
<!-- END VERBATIM -->


#### Seat A (R2_A) S6 (PAR)

**Source:** `theory_campaign/MEET-THM/R2_A.md:137` (verbatim) — base: R1_A S1 `theory_campaign/MEET-THM/R1_A.md:489`

<!-- BEGIN VERBATIM R2_A.md:137-137 -->
**S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
<!-- END VERBATIM -->


---

## S-Z · Evidence variance, masked tails (K37–K41, K53)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:61`):** content = Evidence variance, masked tails (K37–K41, K53). Notes and decisions = Terminal-off clause only in the exception-probability form

The seats differ on the variance clause: A (clause (vii)) and B (clause (vi)) state Var(Ẑ_r/Z | 𝒞) ≤ (T+1)e^{2D}/N with D = osc_Ω d; D (S6 row) states Var(W_r|𝓒) ≤ e^{2·osc_Ω d} − 1 (pathwise bound, PC2 D14), "replaces the (T+1)e^{2D}/N form". R3_D §S1 confirms D's form (`theory_campaign/MEET-THM/R3_D.md:36`); R3_B §S1 keeps "(vii) with D = osc_Ω d ≤ D_*" (`theory_campaign/MEET-THM/R3_B.md:52`). Wording: see "Chair's choices" item 3 (both bounds ship). The terminal-off clause is in the exception-probability form in all three (MINUTES).


#### Seat A (R2_A) S4

**Source:** `theory_campaign/MEET-THM/R2_A.md:133` (verbatim) — base: R1_A C6 `theory_campaign/MEET-THM/R1_A.md:257`

<!-- BEGIN VERBATIM R2_A.md:133-133 -->
**S4 · Proposition Z (K37–K41, K53).** (i) E[Ẑ_r \| 𝓒] = Z, E[log Ẑ_r] ≤ log Z, P(0.05Ẑ > Z) ≤ 0.05 (cited). (ii) exact variance identity (OPW2 Thm A, as a specialisation of CDG 2011 Thm 1.4 in kind); the exact-refresh product never substituted (OPW2-cex). (iii) masked lower tail: islands whose terminal population is off S₀ have Ẑ_r ≤ √δ₁Z **except on an event of probability ≤ 2√δ₁** (source form, PC1:247; divided by κ if conditioned on an off-event of probability κ); PC1 claim 4 wording mandatory. (iv) Ẑ < Z_𝒯 ⇒ Ẑ < Z. (vi) favourable Ẑ/Z → 1 under (P1) (remark). (vii) Var(Ẑ_r/Z \| 𝓒) ≤ (T+1)e^{2D}/N with D := osc_Ω(d), deterministic, bounded by §R3(a) (PC1:249). Status unchanged from R1 §D C6 (FMP-Na: PROVED (XF: GAP (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; (vii) E proposal unchecked). Supplement.
<!-- END VERBATIM -->


#### Seat B (R2_B) S4

**Source:** `theory_campaign/MEET-THM/R2_B.md:173–175` (verbatim) — base: R1_B D12 `theory_campaign/MEET-THM/R1_B.md:355`

<!-- BEGIN VERBATIM R2_B.md:173-175 -->
### S4 · Theorem Z, evidence variance (K39, K40, K38, K37, K41, K53) · supplement

Final statement as R1 §D D12 with: (ii) in the exception-probability form, P(Ẑ_r > √δ₁Z on a terminal-off island) ≤ 2√δ₁ (÷κ if conditioned on an off event of probability κ) (PC1 §15 COUNTEREXAMPLE conceded); the E1/E2 path-tail clause imported with its full hypotheses (A, x_m, τ_A, D_A, exceptions) or omitted; (vi) Var(Ẑ_r/Z\|𝓒) ≤ (T+1)e^{2D}/N with D a deterministic full-space range bound (D = osc d ≤ D_* under §R3(a)). Status: OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE. Novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 unchecked (LIT-SMC §3A: "needs escalation"). Rest unchanged.
<!-- END VERBATIM -->


#### Seat D (R2_D) S6 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:110` (verbatim) — base: R1_D S6 `theory_campaign/MEET-THM/R1_D.md:446`

<!-- BEGIN VERBATIM R2_D.md:110-110 -->
| S6 evidence variance — K37–K41, K53 | Terminal-off clause in exception-probability form; Var(W_r|𝓒) ≤ e^{2·osc_Ω d} − 1 (pathwise bound, PC2 D14) replaces the (T+1)e^{2D}/N form; envelope per M3′(d). | OPW2-ThmA "PROVED (SF: none; XF: VERIFIED (A-REV9))"; MZ-E1E2 "PROVED (E1, E2)" candidate |
<!-- END VERBATIM -->


---

## S-POOL · Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1)

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:66`):** content = Pooling rules, the checked recording-marginal equal-weight bias comparison P1, R_eff (K49, K50, K54, K56, K57-P1). Notes and decisions = General K57 accuracy → FW (B, C; R3-8)

General K57 accuracy → FUTURE_WORK (B, C; R3-8). C has no R2 card (cites). Seats are compatible; P1 is stated for the uniformly sampled recording-state / one-record marginal in all three.


#### Seat B (R2_B) S10

**Source:** `theory_campaign/MEET-THM/R2_B.md:197–199` (verbatim) — base: R1_B D14 `theory_campaign/MEET-THM/R1_B.md:393`

<!-- BEGIN VERBATIM R2_B.md:197-199 -->
### S10 · Proposition PIP-eq (K49, K50, K57; K59 FUTURE_WORK) · supplement

Final statement as R1 §D D14 with the TV clause on the uniformly sampled one-record marginal of the delivered population (PC1 §14 AMBIGUOUS) and the splitting clause labelled exact-refresh idealisation. Status: MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH. Rest unchanged.
<!-- END VERBATIM -->


#### Seat A (R2_A) S7

**Source:** `theory_campaign/MEET-THM/R2_A.md:139` (verbatim) — base: R1_A C4 `theory_campaign/MEET-THM/R1_A.md:219`; S2 `theory_campaign/MEET-THM/R1_A.md:508`

<!-- BEGIN VERBATIM R2_A.md:139-139 -->
**S7 · Proposition POOL (K49, K50, K54, K56, K57; K47, K55 cited).** As R1 §D C4 (i), (iii)–(vi) and S2 P1, with (ii) moved to M2(b) and 0 ≤ h ≤ 1 (PC1:240); P1 stated for the uniformly sampled recording-state marginal (PC1:237); "iff delivered" dropped. Status unchanged (MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); ADRAFT-ThmA Astra-only, cite Del Moral; MZ-P1P2: P1 PROVED; OBG-LH-lock-general: XF ERROR). Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S5 and S7 rows

**Source:** `theory_campaign/MEET-THM/R2_D.md:109` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:109-109 -->
| S5 pooling — K47 cited, K48–K50, K54, K56 | unchanged | unchanged |
<!-- END VERBATIM -->

**Source:** `theory_campaign/MEET-THM/R2_D.md:111` (verbatim) — base: R1_D S5 `theory_campaign/MEET-THM/R1_D.md:434`, S7 `theory_campaign/MEET-THM/R1_D.md:457`

<!-- BEGIN VERBATIM R2_D.md:111-111 -->
| S7 equal-weight P1 — K57 | unchanged (bias ≤ TV of the one-record marginal, cluster 14) | MZ-P1P2 "P1 PROVED; P2 PROVED as a composition" |
<!-- END VERBATIM -->


#### Seat C (R3_C §S1) objection to unrestricted K57 accuracy (for the record)

**Source:** `theory_campaign/MEET-THM/R3_C.md:36` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:36-36 -->
| §2.2 S-POOL | Object to unrestricted K57 accuracy | Retain the checked recording-marginal bias comparison; general fixed-budget equal-weight accuracy remains FUTURE_WORK. W2P1 B.S10 verifies that narrower scope. | A checked estimator-level theorem for the actual records and budgets. |
<!-- END VERBATIM -->


---

## S-LIM · Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:65`):** content = Limitations as theorems (K79, K81, K100, K101); K99 qualitative remark. Notes and decisions = Duplicates: PIP = E[# selected in group]/d; numeric limits only with their p qualification

Duplicates clause (MINUTES; SYNTH_R2 §3): PIP = E[# selected in group]/d; the numeric limit 2/3 only for p = 2; with an orthogonal null it is 3/5; numeric limits only with their p qualification. The seats distribute clauses differently (A puts the weak-local-maximum limitation CEX-localmax in S-CERT; B has it as (b) here and K74 here; MINUTES places K74 in S-CERT); the duplicates clause is identical. C cites these.


#### Seat B (R2_B) S6

**Source:** `theory_campaign/MEET-THM/R2_B.md:181–183` (verbatim) — base: R1_B D15 `theory_campaign/MEET-THM/R1_B.md:406`

<!-- BEGIN VERBATIM R2_B.md:181-183 -->
### S6 · Proposition LIM (K79, K74, K81, K100, K101; K99 remark) · supplement

Final statement: (a) no transcript diagnostic certifies absence of an unqueried mode; (b) a certified weak local maximum can be far below the mode; (c) ESS = N throughout is compatible with genealogical collapse; (e) d exact duplicates: by symmetry PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise it is 2/3, group inclusion → 1; (f) MPM may exceed K; (g′) qualitative barrier: SHARE-PB's k-way contrast construction, as a remark. Repairs: (e) corrected (PC1 §18 COUNTEREXAMPLE conceded); (d) withdrawn (IMPLAUSIBLE); (g) withdrawn with K80 (FUTURE_WORK). Status: CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED. Rest unchanged from R1 §D D15.
<!-- END VERBATIM -->


#### Seat A (R2_A) S9

**Source:** `theory_campaign/MEET-THM/R2_A.md:143` (verbatim) — base: R1_A S3 `theory_campaign/MEET-THM/R1_A.md:527`

<!-- BEGIN VERBATIM R2_A.md:143-143 -->
**S9 · Proposition LIM (K79, K81, K100, K101).** (a), (b), (d) unchanged from R1 §D S3. (c) duplicates: d interchangeable columns have equal PIPs with PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise the limit is 2/3 (PC1:281); group inclusion → 1. Supplement.
<!-- END VERBATIM -->


#### Seat D (R2_D) S11 row

**Source:** `theory_campaign/MEET-THM/R2_D.md:115` (verbatim) — base: R1_D S11 `theory_campaign/MEET-THM/R1_D.md:493`

<!-- BEGIN VERBATIM R2_D.md:115-115 -->
| S11 limitations — K79, K81, K99 (qualitative), K100 (corrected) | Duplicates: PIP = E[#selected in group]/d (cluster 18). | unchanged |
<!-- END VERBATIM -->


---

## S-LEAK · B's leakage clauses (F), (S) as a supplementary corollary to M2

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:71`):** content = B's leakage clauses (F), (S) as a supplementary corollary to M2. Notes and decisions = R3-5, unanimous

R3-5, unanimous. (F), (S) are non-perturbative / different scale; they are not part of HQ's (a)(b)(c); (b5)'s pathwise bound stays in M2 (R3_B `theory_campaign/MEET-THM/R3_B.md:142`). R3_C: "Preserve all inherited hypotheses; no positive uniform q₂(S₀) conclusion" (`theory_campaign/MEET-THM/R3_C.md:123`). Seats B and D state (S) differently: B adds the lower bound m ≥ π₀(S₀)e^{−2·osc d}; D states the exact identity 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)) and that m has no design-uniform lower bound. Only B states (F). See "Chair's choices" item 4 (compatible; both ship).


#### Seat B (R2_B): clause (S) — the m-form, a fragment of the (b5) clause in the §R3 card

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
and max_t χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1, m := min{π₀(S₀), q₂(S₀)} ≥ π₀(S₀)e^{−2·osc d}.
<!-- END VERBATIM -->


#### Seat B (R2_B): clause (F) — fragment (b6) of the same row

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
(b6) Favourable start under leakage: G, R, SE-blk(φ₀), EBM(M_n), CBL(η), η < η_A ⇒ 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}).
<!-- END VERBATIM -->


#### Seat B (R2_B): status fragments for (S), (F), m-bound (third column of the same row)

**Source:** `theory_campaign/MEET-THM/R2_B.md:216` (verbatim fragments of the line; the line carries other clauses not reproduced here, marked […])

<!-- BEGIN VERBATIM FRAGMENT R2_B.md:216 -->
OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; […] the m lower bound: PROVED (by this seat, unchecked; q₂(S₀)/π₀(S₀) = e^{2d(S₀)}/E_{π₀}e^{2d}). […] (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B).
<!-- END VERBATIM -->


#### Seat D (R2_D): the non-perturbative layer (its form of (S))

**Source:** `theory_campaign/MEET-THM/R2_D.md:136` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:136-136 -->
Non-perturbative layer (any ε, every grid; Seat B's (S), PC1 TRUE-AS-WRITTEN): χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1 with m = min{π₀(S₀), q₂(S₀)}, exact 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)q₂(S₀)); m has no design-uniform lower bound (q₂ route IMPLAUSIBLE uniformly, PC1).
<!-- END VERBATIM -->


#### Seat A (R2_A) D4 row (A places B's (F),(S) in a leakage supplement; states no clause)

**Source:** `theory_campaign/MEET-THM/R2_A.md:20` (verbatim)

<!-- BEGIN VERBATIM R2_A.md:20-20 -->
| D4 | amend | One merged package (§R3): WS3/WS4 route, now VERIFIED cross-family (CHK:13–14), with C's pathwise M₂ ≤ e^{osc d} clause (PC2:125) and B's (F),(S) clauses as a leakage supplement. Concede A.C9(c) "hence within" (PC1:138), the exhibit (PC1:142), the (e) "iff" (PC1:141). B's (N) and q₂ lemma not adopted (PC1:145, 147). | A proof of B's q₂ tilt-tail lemma would add a non-perturbative clause. |
<!-- END VERBATIM -->


---

## S-REP · Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions

**Decision note (MINUTES §2.2, `theory_campaign/MEET-THM/MINUTES.md:72`):** content = Run-card reporting corollary: Ĵ (B/C/D form) and ε̂_× with companions. Notes and decisions = Final card `R3_C.md` §S2 S-REP. **ū̂ is D's global block-table envelope ū̂ = Σ_b max_{U⊆C_b} x_b(U)**, not a maximum over V (C's objection, R3_C §S1, adopted, since a maximum over V ⊊ Ω does not bound all fits)

Final card is R3_C §S2 S-REP (R3-6, unanimous: A withdrew its TI form). **ū̂ is D's global block-table envelope** ū̂ = Σ_b max_{U⊆C_b} x_b(U), not a maximum over V (C's objection, R3_C §S1, adopted; a maximum over V ⊊ Ω does not bound all fits). The card below already states the global envelope ("a conservative global envelope, not a maximum over V"); the earlier R2 wording "maximal fit fraction on V" (SYNTH_R2 §2.5; D:182) is withdrawn. Growth rates for the informative regime: the two stacking configurations of MINUTES §2.3 §2.6. d is a default member of 𝓗 (AMENDMENT_HQ_02). The accumulator is read-only (HQ Q4).


#### Final card (R3_C §S2 S-REP)

**Source:** `theory_campaign/MEET-THM/R3_C.md:208–243` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:208-243 -->
### S-REP — run-card reporting corollary

| Card field | Final content |
|---|---|
| IDs | **S-REP: K104/K11 reporting corollary**, using M1/K46/K52 and M2/K102. |
| Hypotheses | D0, EX-A and the MC contract. \(d\) is fixed from data, blocks and tables before final randomness. Let \(D=\max_\Omega d-\min_\Omega d\), \(W_r=\widehat Z_r/Z\), \(M_2=E(W_r^2\mid\mathcal C)\). |
| Implementation premises | Read-only initial and measured-endpoint discrepancy accumulators; no new draws, transitions or scores; no feedback. Existing values are read when available. Missing historical records yield NA. Integrated accumulator and extended-stream fidelity require audit. |
| Initial records | \(A_r=N^{-1}\sum_{i=1}^Nd(S^{(0)}_{ri})\), using each final island’s initial iid start particles. Initial particles are not reweighted by final island evidence. |
| Endpoint records | \(B_r=(4N)^{-1}\sum_{k=1}^4\sum_{i=1}^Nd(S^{(k)}_{ri})\), at the four prescribed measured endpoints. These are plain discrepancies, not marginal RB PIP records. |
| Estimator | \(\displaystyle\widehat J=\frac{\sum_{r=1}^{R'}\widehat Z_rB_r}{\sum_{r=1}^{R'}\widehat Z_r}-\frac1{R'}\sum_{r=1}^{R'}A_r.\) Preserve its signed value. **Evidence:** W2P2 §4, “§R5 · Ĵ definition”, COMPLIANT; W2P1 B.R5(i), T1–T4. |
| Target identity | \(J=KL(\pi\Vert\pi_0)+KL(\pi_0\Vert\pi)=E_\pi d-E_{\pi_0}d\). **Evidence:** W2P2 §4, “C16 · Ĵ theorem”; W1P1 §16. |
| Finite-\(R'\) statement | For \(\epsilon>0\), \(P(|\widehat J-J|>\epsilon\mid\mathcal C)\le\min\{1,4(M_2-1)/R'+16D^2M_2/(R'\epsilon^2)+D^2/(R'N\epsilon^2)\}\). **Evidence:** W2P2 §4, C16 theorem; W2P1 D.R5(i), T1–T3. |
| Limits and zero range | Fixed data/calibration: \(\widehat J\to J\) almost surely under independent stacking. If \(D=0\), both equal zero. On W, the adopted explicit stacking configurations yield consistency using \(D\le D_*=O_P(1)\), \(M_2\le e^{D_*}\). **Evidence:** W2P2 §4 and §6, C16. |
| Bound disclosure | The bound can equal one at default \(R'=4\), as in W2P2’s check; there is no default-budget accuracy or diagnostic-power promise. A large true \(J\) does not ensure a large observed \(\widehat J\). |
| Output form | Under GUARD-W, replace the failure event by \(\mathcal O\cap\{|\widehat J-J|>\epsilon\}\) with the same upper bound. **Evidence:** W1P2 cluster 3, D12; W2P2 §6, C16. |
| Numerical label | **“Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated.”** Report nats. The exact branch may report NA for this bridge diagnostic. |
| Correlation proxy | \(\displaystyle\widehat\varepsilon_\times=\max_{b\ne c,\ j\in C_b,\ k\in C_c}|X_j^\top X_k|/(n-1)\), empty maximum zero; field `cross_block_rmax`. **Evidence:** W2P2 §4, proxy definition, COMPLIANT. |
| Proxy label | **“Descriptive maximum cross-block correlation proxy; not signal leakage or a confidence bound; floating-point error unvalidated.”** |
| Global companions | \(\widehat\kappa=\min_b\lambda_{\min}(G_{C_b}/(n-1))\). If positive, \(\widehat\delta=(K-1)\widehat\varepsilon_\times/\widehat\kappa\). Let \(\widehat{\bar u}=\sum_b\max_{U\subseteq C_b}x_b(U)\), using already available block-score gains. This is a conservative global envelope, not a maximum over \(V\). |
| Companion domain | Require \(\widehat\kappa>0,\ \widehat\delta<1,\ \widehat{\bar u}<1,\ \widehat\delta\widehat{\bar u}<(1-\widehat\delta)(1-\widehat{\bar u})\). Otherwise print derived \(\widehat\eta\) as **“n/a”**. **Evidence:** W2P1 D.R5(ii), T4/T5; B.R5(ii) repair; SYNTH_R2 §3. |
| Derived envelope | Put \(\widehat r=\widehat\delta\widehat{\bar u}/[(1-\widehat\delta)(1-\widehat{\bar u})]\), \(\widehat\eta=K\log(1/(1-\widehat\delta))+\nu\log(1/(1-\widehat r))\). On the domain, \(\sup_{S\in\Omega}|d(S)-d_\sigma(S)|\le\widehat\eta\). **Evidence:** W2P1 D.R5(ii), T4/T5. |
| Per-model norm clause | For nonempty \(S\), the standardized cross-block relative norm obeys \(\varepsilon_S\le(|S|-1)\widehat\varepsilon_\times/\widehat\kappa\). Treat the empty model separately with norm zero. **Evidence:** W2P1 D.R5(ii), T4/T5. |
| Regularized proxy bounds | With \(G_D\) block diagonal, \(E=G-G_D\), \(A_D=G_D+I\), \(H_D=(n+1)G_D+I\): \(\delta_A\le\frac{(n-1)(p-1)\widehat\varepsilon_\times}{1+(n-1)\widehat\kappa}\), \(\delta_H\le\frac{(n^2-1)(p-1)\widehat\varepsilon_\times}{1+(n^2-1)\widehat\kappa}\). **Evidence:** W2P2 §4, C16 proxy theorem. |
| Scope of derived bounds | M2 still requires its full matrix/residual domain. Restricted-set calculations remain restricted-set calculations. Neither a lower bound of order \(n\widehat\varepsilon_\times|\beta_j\beta_k|\) nor global rescaling from \(V\) survives W2P1. |
| Guarantee | The permitted reporting fields have precise mathematical targets and qualified error bounds without influencing the sampling procedure. |
| Goals | Objective (1); proposal §5.3 discrepancy reporting, §5.4 approximation and §13.1 bounded expectations; HQ Q4. No separate Song–Liang theorem-equivalence claim. |
| Status/self-check flag | Reporting assembly: **PROOF SKETCH, unchecked**. N1: **PROOF SKETCH**. PC1c3: **PROVED**, with N1 as premise. W2P2 C16 and repaired W2P1 T4/T5 are statement/route checks, not a full proof upgrade. |
| Fidelity | Reporting amendment authorized by Q4, to be recorded in AMENDMENT_HQ_02. Per-particle \(d\) values exist during execution but are not currently retained. Historical availability is not inferred. No machine-certified bound is claimed. |
| Novelty/citation | **MODEST/NEW-COMP** reporting consequence. Independent-system evidence weighting is established in [Dai–Heng–Jacob–Whiteley, §4.2](https://arxiv.org/html/2007.11936v3). The Jeffreys identity and norm inequalities are foundations; matching the prescribed initial and endpoint records is the contribution. |
| Proof route/key lemma | Apply M1 to globally range-scaled \(d\); split the error between endpoint ratio and initial mean. Use Popoviciu, Chebyshev and a union bound without assuming independence between those two estimates. Proxy bounds use row sums and block eigenvalues. |
| Difficulty/Lean core | Routine mathematics; moderate accumulator audit. Lean: finite ratio bound, variance/union inequalities, range scaling, empty-set conventions and row-sum norm bounds. |
| Dependencies | M1; M2 for informative W rates; M3 for discrepancy definitions; S-KERNEL for exact initialization; S-OUT for delivered-event transfer. |
| Risk | Wrong endpoint timing; final-evidence weighting of initial particles; using \(V\)-range globally; invalid residual domain; interpreting a descriptive proxy as coefficient leakage or flag power. |
| Fallback/stop rule | Retain precisely labelled descriptive fields if quantitative proof closure fails. If records are unavailable, report NA. Stop after one failed proof/audit repair cycle; remove quantitative reporting claims. Failure inherited from N1 or M2 triggers their binding-goal escalation, not a silent waiver. |
| IC3 exhibit/check | W has \(\widehat\kappa=3/4\), bounded discrepancy/moments and actual SMC dispatch. W2P2 `w_family.py` checks its proxy bounds; `jhat_mc.py` checks the estimator on a coded-grid component replica. W2P1 T4/T5 checks the global-envelope version. |
| Numerical companion | None newly run. Proposed: at most ten seeds on enumerable correlated component designs; compare exact \(J\), accumulated endpoint/start means and analytic proxy bounds. Replay identical streams with reporting enabled/disabled to test zero feedback. Report NA rather than reconstruct absent historical accumulators. |
<!-- END VERBATIM -->


---

# Part III · Remarks and cited lemmas

## Thesis CD (K96): scoped remark after the main theorems

MINUTES §2.1: "a scoped remark after the main theorems, unanimous since Round 2." The R3 files only reconfirm (R3_A:26; R3_B:44; R3_C:28; R3_D:28). The scoped wording is in the Round 2 files; four wordings, labelled by seat. See "Chair's choices" item 5 (C's wording).

### Seat A (R2_A, agenda item 6)


**Source:** `theory_campaign/MEET-THM/R2_A.md:204` (verbatim)

<!-- BEGIN VERBATIM R2_A.md:204-204 -->
**Item 6, thesis scope (CD).** Fixed data: M1 identities, M2(a)–(f), M5, M3(b) (all finite inequalities). Asymptotic: M2(g), M6(b1-LH), S1, S2, the ideal-grid depth laws. Favourable vs masked: M1, M2(a), M3, M5 are regime-free; depth laws differ by regime (M7(d) vs S11); selection is proved only on masked LH (M6). The sentence not a corollary of other cards: none. CD is a **remark** ("correlation enters the guarantees only through (δ₁, osc d_σ, η_Ω, A₀), each computable from (X, y); it enters no identity and no limit"), placed after M8.
<!-- END VERBATIM -->


### Seat B (R2_B, agenda item 6)

**Source:** `theory_campaign/MEET-THM/R2_B.md:252` (verbatim)

<!-- BEGIN VERBATIM R2_B.md:252-252 -->
**Item 6, thesis scope.** Remark only (concede D2). Scope of the remark: fixed data for (a) identities and (c) particle cost (M₂ ≤ e^{osc d}, R′ ≍ e^{osc d}/ε²), both for every X; depth (b) is a fixed-data bound T ≤ P + ⌈osc_V d/0.3246⌉ + 1 plus the ideal-grid crossing law log₂A₀ + O(1); selection (d) is asymptotic, favourable (b6 start, T03♯) or masked (HPM b1-LH) on separate sequences. Candidate non-corollary sentence "correlation increases depth and M₂" is false (non-monotone: R1 check, PC1 §11); the true non-monotone sentence is Proposition NEC's cancellation point. So: no theorem.
<!-- END VERBATIM -->


### Seat C (R2_C, §R6 agenda 6 table)

**Source:** `theory_campaign/MEET-THM/R2_C.md:312–317` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:312-317 -->
| §R6 — Agenda 6: thesis scope | Final wording |
|---|---|
| K96 disposition | **Remark only.** There is no retained non-corollary thesis sentence. |
| Fixed data | For each admissible finite input and successful frozen calibration, the idealized start, kernels and unnormalized identities target the specified posterior. Normalized finite-run posterior estimates are not generally unbiased or exact. Independent stacking gives fixed-data consistency for the stated records. |
| Asymptotic accuracy | Exact-target selection uses C9’s model/design conditions. Growing-dimensional summary accuracy is established by the proposed C1/C2 assembly on W with explicit stacking. Masked output/store accuracy uses LH and LS0 with output/retention premises. These are separate scopes. |
| Correlation and cost | Dependence affects the start discrepancy, available bounds and search difficulty. The results do not prove that correlation only increases cost, that all correlated designs admit polynomial accuracy budgets, or that the posterior itself remains statistically consistent under arbitrary correlation. |
<!-- END VERBATIM -->


### Seat D (R2_D, agenda item 6)

**Source:** `theory_campaign/MEET-THM/R2_D.md:186` (verbatim)

<!-- BEGIN VERBATIM R2_D.md:186-186 -->
**Item 6, thesis theorem.** Scope: fixed data for the identities and finite-R′ bounds (H′(a),(b)); asymptotic for depth and selection (STG′(c), Theorem 5(b1-LH), SL′), with favourable and masked families kept on separate sequences. There is no sentence of CD that is not a corollary of H′, STG′, WS′, Theorem 5 and SL′ (the candidate "ε ↦ (d, χ²_t, T, M_φ) is continuous at 0 while ε ↦ P(𝒪 ∩ {Ŝ ≠ S₀}) is bounded through the same quantities" is WS′(b) plus Theorem 5(0)). **Remark only**, placed as the organising paragraph of the main text. "Never correctness" = H′(a); "costs depth" = STG′ + WS′(b)(iii); "costs particles/islands" = H′(b) with M₂ ≥ 1/P_𝓒(cross) disclosed and M₂ ≤ e^{osc d} where (a) applies; not monotone in correlation, never conditional on output.
<!-- END VERBATIM -->



## Cited lemmas (not numbered claims of paper 1)

Collected from the final cards and Round 3 files. Each is cited in the main text or inside a card; none is a theorem number of paper 1 unless said so.

| Cited result | Used in | Source (path:line) |
|---|---|---|
| N9 kernel facts: γ_φ-reversibility of each elementary move, q_φ-invariance and self-adjointness of the uniformly random-order round, exact draw_pi0 and Z̄₀ (K08, K20, K21), with the CHK amendments (VERIFIED WITH AMENDMENT) | M1(a), S-KERNEL | `R3_A.md:114,120`; `MINUTES.md:39,64` |
| K47 (pooling, cited) | M1; S-POOL | `MINUTES.md:39`; `R3_A.md:114` |
| SMC identities and fixed-data limits: Del Moral 2004; Del Moral–Doucet–Jasra 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022 | M1(a), (f) | `R3_A.md:127`; `R3_D.md:183` |
| Markov lower bound: Grosse–Ghahramani–Adams 2015 | M1(d), M4(e) | `R3_A.md:127`; `R3_B.md:208` |
| Greedy-schedule optimality: Štefankovič–Vempala–Vigoda 2009 | M7(a), M2(b6) | `R3_A.md:154`; `R3_B.md:179` |
| K28: √c·T*(c) → Λ_len (Syed et al. 2024 Thm 3; Gelman–Meng 1998) | M7(e) (cited) | `R3_A.md:147,154`; `MINUTES.md:45` |
| Chatterjee–Diaconis 2018 Thms 1.1–1.3 (exp(KL) scale; with log-weight-tail qualifications) | M6, M2(c2) | `R3_C.md:199`; `R3_B.md:179`; `R3_D.md:183` |
| Cérou–Del Moral–Guyader 2011 Thms 1.4–1.5 (variance theorems; novelty of S-Z (i) to the citation checker) | M2, S-Z | `R3_B.md:179`; `R2_B.md` S4 |
| Frazier et al. 2023, Assumption 6(iv) (generic χ² precedent; not re-fetched) | M2 | `R3_B.md:179` |
| Papaspiliopoulos–Rossell 2017 §§3.1–3.2 (block computation precedent) | M3 | `R3_C.md:170` |
| Dai–Heng–Jacob–Whiteley §4.2 (independent-system evidence weighting) | S-REP | `R3_C.md:236` |
| K60, K61: Barbieri–Berger 2004 HPM/MPM facts (cited lemmas) | M5, S-TARGET | `R3_D.md:151,183`; `R2_D.md:46` |
| Rossell 2022 Prop 1 (the 2E₀δ₁ term) | M5(0) | `R3_D.md:151` |
| Yang–Wainwright–Jordan 2016; Zhou–Yang–Vats–Roberts–Rosenthal 2022 (context next to M5; "with their priors LH is covered by rapid mixing; ours is for the paper's own target and start") | M5, M4 | `R3_D.md:151`; `R3_B.md:208` |
| Hou–Wang–Atchadé arXiv:2407.20580 (never "first finite-n") | M5, M4 | `R3_D.md:151`; `R3_B.md:208` |
| Brent 1974 (W/w + D scheduling) | M8(d) | `R3_D.md:170,183` |
| T22(iii) (K16) PROVED-LOCKED CONDITIONAL, with G, R, within-block SE, EXP′, VIS, NL_η, NL_avg(κ) retained | M3 (supplementary clause) | `R3_C.md:163` |
| CHK-verified WS3, WS4 (M2(a), M3(e)); WS6(d), WS7 with amendments (M2(c)) | M2, M3 | `R3_B.md:160,170–171`; `MINUTES.md:23` |
| T03♯ (S-T) target consistency, T01–T03 PROVED-LOCKED (external review queued) | M1(i), M3, M4(f), M5, M6 | `R2_C.md` C9; `MINUTES.md:60` |
| Lemma RO (event containment), GUARD-W (stop-only coupling; audit open) | M1(d), M4(e), S-OUT | `R3_B.md:194`; `R2_C.md` C13 |
| Furnival–Wilson 1974 (leaps-and-bounds superset bound, K05) | S-CERT | `R0_DIFF.md` K05 row (line 74) |
| K23 squared-kernel Dirichlet comparison, as an attributed lemma without theorem number (C's dissent; optional for the S-KERNEL HQ) | S-KERNEL | `MINUTES.md:79`; `R3_C.md:59` |
| LIT-PAR G4 (Song–Liang numerical comparison), cited as labelled numerical evidence; the analytic separation K97 is FUTURE_WORK | Coverage Cor 2 | `MINUTES.md:78,84` |

## Notes for the registrar/chair (not choices)

- N2 sub-labels: the R3 files identify N2(c) = integrated LS0 replay (`R3_D.md:155`) and N2(e) = GUARD-W stop-only coupling (`R3_B.md:213`). The label N2(b) is used in MINUTES §2.3 and R3_B §S4 (`R3_B.md:315`) but is not defined in any R3 file; its definition is in `THEOREM_REVISION_INPUTS.md` (N2), which is not on this branch. The charters name it as MINUTES does.
- M1 K-ID header: see the integration note under M1.


## Chair's choices (editorial; MINUTES §2 decides content, these fix wording only)

The chair does not vote. Each choice below keeps every clause the checks found TRUE-AS-WRITTEN. Where two seats' forms are compatible, both ship. Where they say the same thing, one wording is chosen and the other is kept in the cited R2 file.

1. **K29.** Superseded by the corrected MINUTES §2.2: S-STGI is dissolved and K29 is FUTURE_WORK FW23. Its conditional implication, under (LL) or the over-tilted q_w bound, may be cited as an attributed lemma. B's STG(f) wording is the reference text. Dissent: D.
2. **K30.** Stated once, as M7(d) in the final M7 card (`R3_A.md` M7, labelled ideal two-state grid). The other seats' wordings (C14, A S11, D STG′(c)) are references for the M7 HQ.
3. **S-Z, variance.** **Both bounds ship**, as two clauses:
   - (vii-a) Var(Ẑ_r/Z | 𝒞) ≤ (T+1)·e^{2D}/N, with D = osc_Ω d, the deterministic full-space range (A S4(vii), B S4(vi); wave-1 repair);
   - (vii-b) Var(W_r | 𝒞) ≤ e^{2·osc_Ω d} − 1 (D S6; it follows from the pathwise bound W_r ∈ [e^{−osc d}, e^{osc d}] checked by PC2, W2_PC2 C2 rows).

   Their minimum is the reported bound. (vii-b) is the checked fallback if (vii-a)'s 1/N route fails in the LP-REST HQ.
4. **S-LEAK, (F) and (S).** Ship:
   - (F) as B states it (`R2_B.md` §R3 (b));
   - (S) as D's exact identity 1 + χ²(π‖π₀) = π(S₀)² / (π₀(S₀)·q₂(S₀)), **plus** B's data-dependent bound m ≥ π₀(S₀)·e^{−2·osc d}, **with** D's caveat that m has no design-uniform lower bound.

   These are compatible. W2_PC1 B.R3(b)(5),(6) finds the m bound TRUE pointwise, and the q₂ route withdrawn. No uniform positive q₂(S₀) conclusion is made (R3_C).
5. **Thesis CD (K96), remark wording.** Use **Seat C's** scoped wording (`R2_C.md` §R6 agenda 6 table): "Remark only; there is no retained non-corollary thesis sentence", with its fixed-data / asymptotic / not-claimed scopes. All seats conceded D2 to C's position. The other three wordings are kept above for the paper's authors.
