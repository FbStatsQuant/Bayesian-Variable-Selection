# Round 2, Seat B (Fable 5.1, Claude Work, high)

Verbatim final message, extracted by the chair from `/home/fb31/.claude/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/3ff39e71-d6d3-4bd3-88d1-a25641ef7881.jsonl` (completed 2026-11-04 04:04 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

Both checks ran under two seconds each and give me what I needed: Seat C's bound holds on PC1's design with the method's own partition at every tested correlation, and at fixed correlation the oscillation of d grows like n (fixed signals) or √n (signals of order n^{−1/4}) while the one-shot χ² stays small. I now have everything the brief asks for and will write the Round 2 answer.

# MEET-THM · Round 2 · Seat B

**Read:** ROUND2_BRIEF; SYNTH_R1 v2.2 (§0.1–0.5, §2 incl. §2.1, §3, §4); HQ rulings Q1–Q4; W1_PC1 VERDICTS (all 20 clusters, registry ledger S1–S23, GR6 note); W1_PC2 VERDICTS (summary, clusters 2–20, Appendix A); CHK_INHERITED REPORT (§1–§6); R1_A (§E, §H, §I), R1_C (all), R1_D (M2, §E, §F, §H, §I); my R1_B; DOSSIER §1, §4–§11; STATUS, FUTURE_WORK, HQ_QUESTIONS; O-WSTAB PROOF.md §3–§8 statements; registry index rows OWS-*, FD-W1, AREV9-OWSTAB; METHOD_v3.1_FINAL §2 #11–#14, #18, §2.1 (card spec); LIT-STAT row 19, LIT-MCMC rows 1–3, 14, LIT-SMC rows 1, 2, 6, 13, 21–22; PC2 `bvs_common.py`.

**Two local checks (scratch directory, PC2's `bvs_common.py` for target, coded partition and D_*; each < 2 s).**

*Check 1: Seat C's D_* on PC1's design Dε with the method's own partition.* n = 40, p = 8, exact Gram XᵀX = 39Σ, pairs within .6, cross ε, β₀ = .25, β₄ = .2, σ = 1; 10 noise seeds × ε ∈ {10⁻⁵, 10⁻⁴, 10⁻³, 10⁻²}; K = 8, B = 2.

```python
blocks = bc.coded_partition(G, B)             # M §6.3 as replicated by PC2
models, d, lbf = bc.d_table(G, z, Y, n, blocks, K)
out = bc.card_Dstar(G, z, Y, n, blocks, K)    # a, dA, dH, r, shared, bX, D_*
osc = d.max() - d.min(); l1c = Lam(2.0) - 2*Lam(1.0)   # WS1: log(1+chi2(pi||pi0))
```

| ε | blocks = pairs | a (range) | D_* (range) | of which 2b_X (median) | osc d / D_* (range) | log(1+χ²) ≤ osc d |
|---|---|---|---|---|---|---|
| 10⁻⁵ | 10/10 | .08–.43 | .07–3.33 | .001 | .42–.70 | 10/10 |
| 10⁻⁴ | 10/10 | .08–.43 | .07–3.35 | .012 | .42–.69 | 10/10 |
| 10⁻³ | 10/10 | .08–.43 | .14–3.49 | .12 | .33–.63 | 10/10 |
| 10⁻² | 10/10 | .08–.43 | .81–5.02 | 1.27 | .07–.41 | 10/10 |

All hypotheses (a, δ_A, δ_H, r < 1) held in 40/40 cases; osc d ≤ D_* in 40/40; at ε ≤ 10⁻³ the bound is the σ²-coupling term alone.

*Check 2: necessity scale of osc d at fixed ε.* p = 4, blocks {0,1},{2,3}, within .5, cross ε, truths at 0 and 2 with coefficient θ, σ = 1, exact Gram; 5 seeds, medians.

```python
th = .5 if signal == "fixed .5" else n ** -0.25
pred = n * eps * th * th / (2*th*th*(1+eps) + 1.0)        # n·ε·θ1θ2 / s_y^2
rows.append([osc, abs(d[i0]-d[ie]), pred, osc/pred, Lam(2)-2*Lam(1)])
```

| signal | ε | n = 100 / 400 / 1600 / 6400: osc d | osc d / pred | log(1+χ²(π‖π₀)) max |
|---|---|---|---|---|
| fixed .5 | .05 | 1.7 / 5.9 / 22.5 / 81.8 | 2.09 / 1.80 / 1.72 / 1.56 | .055 |
| fixed .5 | .10 | 1.1 / 3.5 / 13.7 / 46.6 | .68 / .54 / .53 / .45 | .43 |
| n^{−1/4} | .05 | .22 / .60 / 1.77 / 3.85 | .53 / .66 / .93 / .99 | .006 |
| n^{−1/4} | .10 | .46 / 1.86 / 4.36 / 8.54 | .57 / 1.03 / 1.15 / 1.10 | .057 |

osc d grows linearly in n at fixed signals and like √n·ε at θ = n^{−1/4}; the one-shot χ² stays small throughout. These are route checks, not evidence of a theorem.

---

## §R1 Rebuttal (one row per disagreement)

| Row | Verdict | Position now | Evidence that would change it |
|---|---|---|---|
| D1 | hold (package), concede (clauses) | Main Proposition V+ with these non-cited clauses: N1 general-h identity at the measured endpoint with random-position RB; the negative pooled-product clause (PC1 §1 "B.D1 final clause" TRUE); output-event form P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05 (needs GUARD-W); frozen-𝓒 contract. Ẑ/RB-PIP unbiasedness, SLLN, N9 kernels: cited lemmas (KERNEL supplement). N9 amendments (CHK_INHERITED §5) adopted verbatim. | Chair applying IC4 to merge V+ into Theorem H as clause (0): acceptable (main count then 7). |
| D2 | concede (to C) | No true sentence of CD is non-corollary: correctness is V+/H, depth is STG + (a), particles is M₂ ≤ e^{osc d}. Monotonicity in ε is false (my R1 table: BO-equivalent bridge sometimes needs more stages; PC1 §11 "not monotone"). CD becomes a scoped remark (§R6 item 6). | A seat exhibiting a provable clause not implied by the parts. |
| D3 | amend | B.D9(b) COUNTEREXAMPLE conceded (PC1 §10): population cancellation x_tᵀμ = 0, sample x_tᵀy = O_P(√n). SL demoted to supplement with (b) restated under SL's IG + λ_s prior at a fixed FDR threshold q ∈ (0,1); adaptive-threshold exclusion is the GAP. IC3 corrected (SIZE: g = 5, B = 7, p = 60). | Check wave 2 passing the repaired (b): then main candidate 9; failing: FUTURE_WORK. |
| D4 | amend (merge) | One package (§R3): (a) = C's D_* (PC2 cluster 4) with WS3/WS4 (CHK_INHERITED VERIFIED); (b) = D's (i)–(iv) with the reversed sandwich, A's (b), C's increment and actual-grid moment bounds, WS6(b), my (F); (c) = WS6(d)/WS7 with amendments. My (N) conceded; q₂ route withdrawn, replaced by m ≥ π₀(S₀)e^{−2 osc d}. | None needed; wave 2 on the merged statement. |
| D5 | amend | K26/K27/K30 main (STG); K28 cited clause; K25 a lemma inside STG and the §5.3 package (A, D use it in main); K29 supplement, conditional on LL; K31 FUTURE_WORK (OPEN). "Exact/minimal" dropped (PC1 §9 COUNTEREXAMPLE); count in PC2's form P + ⌈2/h⌉ + 1 with resolution ≤ h/2. | A proof of Conjecture P (none expected in paper 1). |
| D6 | hold | Theorem D stays a supplement proposition (accounting, IC5 weak). K90 is a remark, not a clause (concede to C): the SL §6 comparison needs worker counts, n-vs-p scaling, T, score cost and a loss criterion (PC1 §13), and finite SMC does not output π exactly. | A matched-workload theorem, which nobody has. |
| D7 | hold | Supplement (IC4: identities cited). Terminal-off clause repaired to the exception-probability form ≤ 2√δ₁ (PC1 §15 COUNTEREXAMPLE conceded); (vi) with D a deterministic full-space range (D_* when (a) holds). | A novelty check clearing (i) against Cérou–Del Moral–Guyader Thm 1.4; still supplement. |
| D8 | amend | K93 moves to the supplement as a short cited input (MODEST; main capped at 8), with "PROVED-LOCKED (wave 3; external review queued)" and n ≳ 2·10⁶ disclosed. | None. |
| D9 | hold | K70 (b2-LH) stays a subfamily clause of HPM; K71 FUTURE_WORK; guarantees in liminf form liminf P(correct output) = 1 − limsup P(U_n) (PC1 §6 conceded); SIZE g_max ≤ B < 2g_min named. | None. |
| D10 | hold (= chair) | Delivery is neither a theorem nor a limitation: FUTURE_WORK (no route); every output theorem joint with 𝒪 in liminf form. | A delivery theorem on a concrete family. |
| D11 | amend (accept chair) | M_n is not a design condition (GR6). On families where osc d = O_P(1) (C's §E family; Dε-type), M₂ ≤ e^{osc d} (PC2 "D14 · actual-grid moment"), so a growth rate exists: R′_n = 4⌈log₂(n+p)⌉ gives R′_n/M₂ → ∞ in probability. Elsewhere, fixed-R statements only. My R1 §I Q2 is withdrawn. | None. |
| D12 | name | Theorem Z𝒯/CARD (b),(c) composed with HPM (b1-LH): on LH, P(𝒪 ∩ {TV(π_𝒯, π) > δ₁}) → 0 (§R4). | None. |
| D13 | concede | Main list of 8 (§R6 item 11). | None. |
| D14 | amend | K16 supplement (hold). K11 is now VERIFIED (CHK_INHERITED §4) and is (a4)/(b1) of the package, not a remark (amend). K57 supplement (hold). | None. |
| D15 | amend | Thm 1: selection concentration only; Hellinger/coefficient contraction FUTURE_WORK; not "exceeded" (C). Thm 2: not applicable, fixed design. Thm 3: matched for π (T03♯ large-signal clause); reported PIP conditional on N1 (was "delivered"). Thm 4/Cor 2: "compared", not exceeded; K17/K18 quantify one block-start distortion; Cor 2's null exclusion is SL's separate GAP. Thm S: covered for π; the reported HPM on LH is additional, with SL's supplementary hypotheses unverified. §6: same units, no speed claim. | None. |
| D16 | amend | K23: supplement lemma inside KERNEL with R₂ = (1/m)ΣP_j² (PC1 §19 TRUE). K80: FUTURE_WORK (no sampling law for the flags; PC1 B.D15(g) NEEDS-HYPOTHESIS). K107: FUTURE_WORK (N16 OPEN; rounding bound NONE-GIVEN); K108 stays. | A validated-arithmetic contract (N16). |
| D17 | per K-ID | K02 supplement, caveat "algorithmic output need not be equivariant, even in law, under index ties" (PC1 §20). K07 supplement with SIZE. K12, K34, K67 drop (hold). K94 → FUTURE_WORK (envelope clause GAP, PC1 §12); its two inequalities a remark. K99: quantitative (d) withdrawn (IMPLAUSIBLE); qualitative barrier a remark via SHARE-PB (D). | None. |
| D18 | per group | Target/envelopes, start machinery, calibration (K33), inherited calculus: supplement (hold); K100 corrected to PIP = E[#selected in group]/d. K44, K36, K78 main inside Z𝒯/V+ (hold). K47 cited; K49/K54/K56 supplement; K59 FUTURE_WORK (my header conflict resolved: defer). K77, K83–K85 supplement; K86 cited inside V+ hypotheses (conflict resolved). K60/K61 cited; K62 inside HPM; K63 supplement lemma cited by HPM (conflict resolved); K64/K73/K74 supplement. | None. |

---

## §R2 Final statements

Conventions: EX-A exact arithmetic, EX-S exact start sampler and ideal uniforms (H-U); 𝓒 frozen before stream 10; R′ = 4k declared; GUARD-W the implementation premise "any worker/LS0/guard stop ⇒ no output"; δ₁ := 1 − π(S₀); W_r := Ẑ_r/Z; M₂ := E[W_r²|𝓒]. Statuses copied with qualifiers.

### M1 · Proposition V+ (K35, K46, K32, K86, K36, K50; cited K20, K21, K08, K47)

| Field | Content |
|---|---|
| Final statement | EX-A, EX-S; 𝓒 frozen on streams 0–9; R′ = 4k, N_e declared before stream 10; IND-T over streams 10..9+R′ (code audit pending for R′ > 4); every elementary move γ_φ-reversible and the uniformly random-order round q_φ-invariant (N9, sufficient conditions). For each island r, conditionally on 𝓒: (a) E[Ẑ_r] = Z [cited]; (b) E[Ẑ_r PIP̂_rj] = Z·PIP_j, RB record before the Gibbs draw, round started in q_φ [cited, FMP-M1]; (c) E[Ẑ_r H_r(h)] = Z·π(h) for every h ∈ 𝓗 measurable in (X, y, 𝓒), plain measured-endpoint averages (N1); (d) with GUARD-W and stop-only coupling, P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, never conditional on completion; (e) the pooled product Ẑ̄·PIP^eq is not generally unbiased: bias −(1−1/R′)Cov. |
| §3 repairs | None required (PC1 §1 rows TRUE-AS-WRITTEN). N9 prose amendments (CHK_INHERITED §5) adopted: order conditions are sufficient; "a fixed order need not be self-adjoint"; stationarity stated in (b). |
| Status | T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N1: PROOF SKETCH; N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); PC1c2: PROVED for the potential run, output form CORRECT WITH AMENDMENT. |
| Placement | main (merge into H as clause (0) acceptable). |
| Rest | unchanged from R1 §D D1 (route, Lean, fallback, IC3 any design). |

### M2 · Theorem H (K51, K52, K48, K46)

| Field | Content |
|---|---|
| Final statement | Setting M1; h: Ω → [0,1] in 𝓗. (a) islandwise, every regime, every frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝓒] ≤ 2δ₁. (b) P(\|μ̂_w(h) − π(h)\| > ε \| 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)}. (c) P(\|μ̂_w − h(S₀)\| > t \| 𝓒) ≤ exp{−R′(1−s)²/(2M₂)} + 2δ₁/(st), 0 < s < 1. (d) joint inclusion h_A = 1{A ⊆ S}, plain averages, declared pairs ≤ 2pB. (e) fixed data: μ̂_w → π(h) a.s. as R′ → ∞ at fixed N_e. (f) n → ∞: on a family satisfying T03♯ and osc d = O_P(1) (e.g. the §R3 IC3 family), with the stacking rate R′_n = 4⌈log₂(n+p)⌉: μ̂_w → h(S₀) in probability, jointly with output (liminf form). On masked families (c) holds at every fixed R′ with M₂ unbounded; no rate is claimed. |
| §3 repairs | GR6 (PC1 §2 row A.C5(d)/B.D2(f)): R_n replaced by the explicit R′_n through M₂ ≤ e^{osc d} (PC2 "D14 · actual-grid moment"); liminf delivery form (PC1 §6). (b) is vacuous at R′ = 4 (PC2 item 4): disclosed. |
| Status | A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), "E[W_r ĥ_r] = π(h) is still a premise"; MA-PropP: PROVED (elementary), author-only; T03♯ as in S2. |
| Placement | main. |
| Rest | unchanged from R1 §D D2; IC3 for (f): C's §E family (PC2 D_* = O_P(1), n ≥ 9⁶). |

### M3 · Theorem WS, the §5.3 package (K102, K10, K11, K25, K27, K53, K104)

See §R3 (the card is the final statement).

### M4 · Theorem 2, the start (K15, K17, K18, K10; K16 supplement clause)

| Field | Content |
|---|---|
| Final statement | Blocks any partition; tables r_b; π₀ = γ₀/Z̄₀. (a) π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s; the odds π₀(S₀)/π₀(S°) exact; bridge mass ≥ min(π₀(S₀), π(S₀)). (b) Under BO: d = d_σ = ν[Σ_b log(1−x_b) − log(1−x̄_S)] ≥ 0, zero iff at most one block has positive fit fraction x_b > 0; with known σ² the start equals the posterior (FD-W1). (c) Masked chain (T27(i)'s H1–H3): π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; on LH exact Gram (g ≤ B < 2g, \|ψ\| < ρ) no open hypothesis. (d) −log π₀(S₀) = V + C − log A for any data and partition. (e) [supplement] 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}) under EXP′, VIS, NL (T22(iii), conditional), and under G, R, SE-blk, EBM(M_n), CBL(η), η < η_A (WS53F). |
| §3 repairs | (b) "active" → "positive fit fraction" (PC1 §5 AMBIGUOUS). |
| Status | T22(i)(ii)(iv): PROVED-LOCKED; T22(iii): PROVED-LOCKED CONDITIONAL; T27(i): PROVED-LOCKED, CONDITIONAL; Thm3/4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none) SAME-FAMILY-ONLY; DIL-E: PROVED (XF: VERIFIED (A-REV9)); OWS-WS3: PROVED (SF: none; XF: none) + CHK_INHERITED VERIFIED (PC1, cross-family); FD-W1: PROVED, XF VERIFIED (A-REV4); OWS-WS53F: PROVED-UNDER (SF: none; XF: none), PC1 B.D6(F) TRUE-AS-WRITTEN. |
| Placement | main. |
| Rest | unchanged from R1 §D D4. |

### M5 · Theorem Z𝒯 / CARD (K42, K43, K45, K36, K78, K44)

| Field | Content |
|---|---|
| Final statement | 𝒯 the deduplicated top store, Z_𝒯 = Σ_𝒯 ϖm. (a) Z_𝒯 ≤ Z; π(S) ≤ e^{F(S)}/Z_𝒯; Ẑ < Z_𝒯 ⇒ Ẑ < Z. (b) If S₀ ∈ 𝒯: 1−δ₁ ≤ Z_𝒯/Z ≤ 1, TV(π_𝒯, π) = 1 − Z_𝒯/Z ≤ δ₁, \|PIP^𝒯_j − PIP_j\| ≤ δ₁, \|π_𝒯(h) − π(h)\| ≤ 2δ₁‖h‖_∞. (c) If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀ (½ sharp); holds under LS0 (𝒯_new = top_c(𝒯_old ∪ 𝒮_added)). (d) Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. (e) with GUARD-W: P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05; card-level: P(𝒪 ∩ {some G2/L/R item false}) ≤ 0.05, in exact arithmetic (numerical label until SC + VAL-FP). |
| §3 repairs | (b) scaled by ‖h‖_∞ (PC1 §3 B.D3(b) COUNTEREXAMPLE conceded). |
| Status | MZ-P3: PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery; AUTHOR-ONLY; N13: PROVED (PC1 claim 5); PC1c5: PROVED, ½ sharp; PC1c2: PROVED for the potential run; N6 output form CORRECT WITH AMENDMENT; N17: PROVED (PC1 claim 1); OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording). |
| Placement | main. |
| Rest | unchanged from R1 §D D3. |

### M6 · Theorem HPM (K72, K68, K69, K70, K65, K63, K62)

| Field | Content |
|---|---|
| Final statement | EX-A, EX-S, CAL, SR, GUARD-W, (P), OP-LS0 with completed scans, e4 centre rule (N3 OPEN, carried as hypothesis), ℓ ≥ max{Φ(S°)−1, 0}, SIZE g_max ≤ B < 2g_min. (0) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n; N200 bracket with Π(X). (1) LS-score: under TD′ on Lat(S°), LS0 scores S₀ within max{Φ(S°)−1, 0} moves. (2) (b1-LH): LH exact Gram (p ≤ n−1) with LS0: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; hence liminf P(correct output) = 1 − limsup P(U_n). (3) (b2-LH): without LS0 on STAB-LH (g = 9, c = 2, ρ = .4, ψ = .2), any frozen grid (variant, attributed). (4) margin transfer: exact PIPs ≥ δ from ½ and uniform error < δ ⇒ reported MPM = exact MPM. (5) cost polynomial (T32(i) + LS0 term). |
| §3 repairs | liminf form (PC1 §6); SIZE explicit; K71 (b1-LH-iid) → FUTURE_WORK. |
| Status | T38-(0): PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)); N200: PROVED (elementary, every n), author-only; TheoremA: PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)); LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)); T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); B2E-B2LH: PROVED-UNDER (XF: VERIFIED* (A-REV7)); general LH locking: XF ERROR (not used); Thm5-LH SAME-FAMILY-ONLY. |
| Placement | main. |
| Rest | unchanged from R1 §D D8 (Lean sorry-free cores T21HPM, T37Greedy/Lattice). |

### M7 · Theorem STG (K26, K27, K30, K28; K25 lemma; K29 supplement)

| Field | Content |
|---|---|
| Final statement | Grid rule as coded, ESS threshold ρ̄ = 0.9 on V for pilot and grid (hypothesis), P pilot targets, D_V := osc_V d > 0. (a) ρ_V(u,v) is nonincreasing in v; the coded bisection accepts only intervals with ρ_V ≥ 0.9; T ≤ T_e on success. (b) [Lemma K25] ρ_full(u,v) = ρ_V(u,v)a_u a_w/a_v², w = 2v−u. (c) every accepted interval satisfies (v−u)²Var_{q_ξ\|V}(d) = log(1/ρ) ≤ log(10/9) for some ξ ∈ [u, 2v−u]; every increment ≤ h := 2√log(10/9)/D_V passes; with bisection resolution ≤ h/2 the coded grid has T ≤ P + ⌈2/h⌉ + 1 insertions, absent ceiling/snap failure. (d) ideal two-state exact-frontier grid (not the coded grid): a dominance crossing of log-odds gap A₀ costs log₂A₀ + O(1) stages. (e) [cited] √c·T*(c) → Λ_len as c → 0. (f) [supplement] favourable O(1) stages under STG-F's over-tilted q_w bound or LL. |
| §3 repairs | "exact/minimal" dropped (PC1 §9 COUNTEREXAMPLE); count restated in PC2's form (PC2 cluster 9 "D7 · coded count", resolution ≤ h/2); σ_max replaced by D_V over [0, 2] (Popoviciu); (f) conditional on LL (PC1 §9). |
| Status | STG-G, STG-L0/L1/L: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic; STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); STG-F: PROVED (SF: none; XF: none); STG-Wp: PROVED-UNDER (C22); ConjP: OPEN; T26BUD/PC2 count replica: TRUE-AS-WRITTEN (statement sanity only). |
| Placement | main. |
| Rest | unchanged from R1 §D D7. |

### M8 · Theorem SEP + Lemma KL (K106, K105, K19)

| Field | Content |
|---|---|
| Final statement | LH exact Gram, cancellation depth c, Q* = p^c n^{c/2}; comparison objects are IID π₀ discovery and the one-shot unnormalised evidence estimator (not production SMC). (a) P₀(S₀ scored by Q iid π₀ draws + tables) → 0 if Q/Q* → 0, → 1 if Q/Q* → ∞. (b) 1 + χ²(π‖π₀) ≥ π(S₀)²/π₀(S₀) = Q*e^{O_P(1)}; the one-shot evidence estimator has relative variance χ²/Q. (c) KL(π‖π₀) ≥ π(S₀)log(1/π₀(S₀)) − log 2, so exp(KL) ≥ ½Q*^{π(S₀)}e^{O_P(1)}. (d) Q draws miss S* w.p. ≤ exp(−Qπ₀(S*)). |
| §3 repairs | Guarantee restricted to IID discovery and the stated atom losses; no universal one-shot lower bound (PC1 §8; SEP-taska COUNTEREXAMPLE respected); (c) in WS7(a)'s form. |
| Status | SEP-A, SEP-B: PROVED (SF: none; XF: VERIFIED (A-REV9)); SEP-A-iid: PROVED-UNDER; KL: PROOF SKETCH (NEW-SYNTH); OWS-WS7(a): PROVED (SF: none; XF: none) + CHK_INHERITED VERIFIED WITH AMENDMENT. |
| Placement | main. |
| Rest | unchanged from R1 §D D5. |

### S1 · Theorem SL (K97) · supplement

| Field | Content |
|---|---|
| Final statement | LH exact Gram, c linked pairs, groups of g = 5, B = 7 (p = 60, n ≥ 49), ρ = .5, ψ = .2. SL as in JRSS-B §3.1 with uniform equipartition into K_n subsets and a fixed FDR threshold q ∈ (0,1). (a) P(hub isolated from partner and group) ≥ 1 − cg/K_n (hypergeometric). (b) On that event the hub t is a population null in its subset: x_tᵀμ = 0; under SL's IG + Gaussian + λ_s prior its subset posterior inclusion is O_P(λ_s n^{−1/2}·BF_noise) with BF_noise = O_P(1) from x_tᵀε; exclusion at the fixed threshold q then holds w.p. → 1 if λ_s n^{−1/2} → 0 at SL's rate. (c) 1 − π(S₀) → 0 (Thm5-LH; T03♯). (d) v3.1 on the same family: Theorem HPM (b1-LH). |
| §3 repairs | Population covariance (PC1 §10 COUNTEREXAMPLE conceded); SL's actual prior/λ_s rate and a fixed threshold named; iteration-uniform bound is the GAP (fallback: numerical (b) on LH, ≤ 20 seeds). IC3 changed: g = 5 ≤ B = 7 < 10 satisfies SIZE, strict separation 1−ρ = .5 < 1−ψ = .8 gives blocks = groups (PART-ThmA). |
| Status | C1new: COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none) SAME-FAMILY-ONLY. |
| Fallback + stop | (a)+(c)+(d) as theorem, (b) numerical; stop: one check wave; else FUTURE_WORK. |
| Rest | unchanged from R1 §D D9. |

### S2 · Theorem 1, target consistency (K93) · supplement (short)

Final statement unchanged from R1 §D D13 (R1 fixed s₀, p ≤ n^A; G, R, SE_λ, SE_w, BM-∞ or BM(c > c₀); 1 − π(S₀) = O_P(√(log n/n)); HPM/MPM consistent; large-signal inclusion without beta-min). Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued) SAME-FAMILY-ONLY; onset n ≳ 2·10⁶ disclosed. Repairs: none needed (PC1 §12 TRUE). Rest unchanged.

### S3 · Theorem D, work/depth/width (K87, K88, K89, K06, K64; K90 remark) · supplement

Final statement as R1 §D D11 with: per-run trajectory lengths summed at their own T and each completed search counted separately (PC1 §13 AMBIGUOUS); the SL §6 sentence is a remark stating worker counts, n-vs-p scaling, T, score cost and the loss criterion, with no same-order or exact-output claim (PC1 §13 NEEDS-HYPOTHESIS). Status: MA-PropD: PROVED (counting, given the code's structure), author-only candidate; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none), displayed rate GAP (A-REV5); Cost-T38: PROVED-UNDER (XF: GAP). Rest unchanged.

### S4 · Theorem Z, evidence variance (K39, K40, K38, K37, K41, K53) · supplement

Final statement as R1 §D D12 with: (ii) in the exception-probability form, P(Ẑ_r > √δ₁Z on a terminal-off island) ≤ 2√δ₁ (÷κ if conditioned on an off event of probability κ) (PC1 §15 COUNTEREXAMPLE conceded); the E1/E2 path-tail clause imported with its full hypotheses (A, x_m, τ_A, D_A, exceptions) or omitted; (vi) Var(Ẑ_r/Z\|𝓒) ≤ (T+1)e^{2D}/N with D a deterministic full-space range bound (D = osc d ≤ D_* under §R3(a)). Status: OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE. Novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 unchecked (LIT-SMC §3A: "needs escalation"). Rest unchanged.

### S5 · Proposition KERNEL (K20, K21, K08, K09, K22, K23, K103) · supplement, cited lemma + Lean

Final statement as R1 §D D16 with: reversibility under the sufficient conditions of N9 (a fixed order need not be self-adjoint); the graph clause for p ≥ 2 (PC1 §19); Q_φ(S,·) ≥ π_φ/M_φ (E's constant 1/M_φ, PC1 §19 TRUE; 1/(mM_φ) also valid) and ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/M_φ)^k with M_φ ≤ exp{φ·osc d}; ℰ_Q ≥ ½ℰ_{R₂}, R₂ = (1/m)ΣP_j²; tie-aware DP returns the prescribed maximiser (N3 OPEN, hypothesis). Status: N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. Rest unchanged.

### S6 · Proposition LIM (K79, K74, K81, K100, K101; K99 remark) · supplement

Final statement: (a) no transcript diagnostic certifies absence of an unqueried mode; (b) a certified weak local maximum can be far below the mode; (c) ESS = N throughout is compatible with genealogical collapse; (e) d exact duplicates: by symmetry PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise it is 2/3, group inclusion → 1; (f) MPM may exceed K; (g′) qualitative barrier: SHARE-PB's k-way contrast construction, as a remark. Repairs: (e) corrected (PC1 §18 COUNTEREXAMPLE conceded); (d) withdrawn (IMPLAUSIBLE); (g) withdrawn with K80 (FUTURE_WORK). Status: CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED. Rest unchanged from R1 §D D15.

### S7 · Proposition TARGET (K01, K02, K03, K04, K95, K76) · supplement

Final statement as R1 §D D17 with: target affine-invariant and permutation-equivariant; algorithmic output need not be equivariant, even in law, under index ties (PC1 §20); A(S₀) ≤ η < 1 ⇒ HPM = MPM = S₀ (PC1 §20 NEEDS-HYPOTHESIS conceded); 2νb₀ as the exact pairwise IG constant (PC2 cluster 20). Status: N17: PROVED (PC1 claim 1); T01 reduction: PROVED-LOCKED (wave 3; external review queued); N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected). Rest unchanged.

### S8 · Proposition CERT (K64, K73, K05, K108) · supplement

Final statement as R1 §D D18 with: `local_certified` = no strictly improving feasible flip or swap at the scanned centre (weak local maximum; ties allowed) (PC1 §17 COUNTEREXAMPLE conceded); B&B exact when it completes, "unresolved" otherwise, in exact arithmetic; log-mass perturbation ε ⇒ Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, winners with gap > 2ε unchanged. The rounding bound (K107) is withdrawn to FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). Status: N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*). Rest unchanged.

### S9 · Proposition IDENT (K25, K104, K54, K55) · supplement

Final statement as R1 §D D19 with Λ_len := ∫₀¹ sd_{q_φ}(d)dφ ≤ √J (the length, not the cumulant Λ(1); PC1 §16 AMBIGUOUS). Status: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none); PC1 §14, §16 TRUE-AS-WRITTEN. Rest unchanged.

### S10 · Proposition PIP-eq (K49, K50, K57; K59 FUTURE_WORK) · supplement

Final statement as R1 §D D14 with the TV clause on the uniformly sampled one-record marginal of the delivered population (PC1 §14 AMBIGUOUS) and the splitting clause labelled exact-refresh idealisation. Status: MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH. Rest unchanged.

### S11 · Proposition BLOCKS (K07, K14, K06) · supplement

Unchanged from R1 §D D21 (PC1 §19 B.D21 TRUE-AS-WRITTEN; preservation only, equality needs SIZE). Status: PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; PART-CE2: COUNTEREXAMPLE.

Dropped from the list since R1: D10 (CD → remark), D20 (K94 → FUTURE_WORK).

---

## §R3 The §5.3 package (HQ Q1): Theorem WS · main · K102, K10, K11, K25, K27, K53, K104

Setting A (standardised data; v3.1 target; partition C_1..C_J fixed from X; EX-A); Ω = {|S| ≤ K}; d = log BF − Σ_b log r_b(S_b); G_D the block-diagonal part of G = XᵀX, E = G − G_D, H_D = (n+1)G_D + I, A_D = G_D + I; ν = a₀ + n/2; Y = yᵀy; z = Xᵀy; q_φ ∝ γ₀e^{φd}; d_σ := d computed from G_D with the same z, Y (= WS3's noise-sharing term).

| Part | Final statement | Status (verbatim, with qualifiers) and verdict rows |
|---|---|---|
| **(a) Discrepancy half** | (a1) If E = 0 then d = d_σ = ν[Σ_b log(1−x_b) − log(1−x̄_S)] ∈ [0, νΣ_{b<c}x_bx_c/(1−x̄_S)], zero iff at most one block has x_b > 0; with known σ², d ≡ 0. (a2) Let a := nzᵀH_D⁻¹z/(2b₀+Y), δ_A := ‖A_D^{−1/2}EA_D^{−1/2}‖, δ_H := ‖(n+1)H_D^{−1/2}EH_D^{−1/2}‖, r := δ_Ha/[(1−δ_H)(1−a)]. If a, δ_A, δ_H, r < 1: osc d ≤ D_* := νa²/[2(1−a)] + 2b_X, b_X := (K/2)[−log(1−δ_A) − log(1−δ_H)] − ν log(1−r). The first term is the σ²-coupling term (it bounds osc d_σ), the second the cross-block term. (a3) Every partition, every ε: KL(π‖π₀) ≤ osc d; J := KL(π‖π₀) + KL(π₀‖π) = π(d) − π₀(d) ≤ osc d; 1 + χ²(π‖π₀) ≤ e^{osc d}; TV(π, π₀) ≤ tanh(osc d/2). (a4) Per model, A_S ≻ 0, ε_S < 1 − x̄_S: \|d(S) − d_σ(S)\| ≤ η_S := νε_Sx̄_S/(1−ε_S−x̄_S) + F_S/(4(1−ε_S)), ε_S ≤ \|S\|·max_cross\|r_jl\|/φ₀². | (a1) OWS-WS3: PROVED (SF: none; XF: none) + CHK_INHERITED §3 VERIFIED (PC1, cross-family, line by line); FD-W1: PROVED, XF VERIFIED (A-REV4). (a2) Seat C D14: PROOF SKETCH (NEW-COMP), PC2 cluster 4 "D14 · deterministic bound" TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE (Appendix A route); my check 1 on Dε. (a3) PC2 "D14 · one-shot"; PC1 §16 rows (TI identity; KL ≤ osc d; TV ≤ tanh) TRUE-AS-WRITTEN. (a4) OWS-WS4: PROVED (SF: none; XF: none) + CHK_INHERITED §4 VERIFIED; PC1 §4 A.C9(a,b) TRUE on Dε. |
| **(b) Bridge-form stability** | W ⊆ Ω nonempty (Ω or V), η_W := max_W η_S; 0 ≤ u < v ≤ 1, w = 2v−u. (b1) e^{−4vη_W}[1+χ²^σ_W(u,v)] ≤ 1+χ²_W(u,v) ≤ e^{4vη_W}[1+χ²^σ_W(u,v)]; TV(q_v^W, q_v^{σ,W}) ≤ 1 − e^{−2vη_W}. (b2) Greedy ESS-0.9 grids with common pilot targets and resolution, 0.9e^{4η} < 1: T^σ(0.9e^{−4η}) ≤ T(0.9) ≤ T^σ(0.9e^{4η}). (b3) Doeblin constant M_φ ≤ e^{2φη}M^σ_φ. (b4) Stage-1 evidence variance = χ²(q_{φ₁}‖π₀)/N_e exactly; 1 + N_e·Var within e^{4φ₁η} of its BO value. (b5) At every ε: χ²(q_{u+Δ}‖q_u) ≤ e^{Δ·osc d} − 1 ≤ e^{ΔD_*} − 1; on every successful coded grid W_r ∈ [e^{−osc d}, e^{osc d}] pathwise and E[W_r\|𝓒] = 1, so M₂ ≤ e^{osc d} ≤ e^{D_*}, kernels as coded, no grid-quality or mixing premise; and max_t χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1, m := min{π₀(S₀), q₂(S₀)} ≥ π₀(S₀)e^{−2·osc d}. (b6) Favourable start under leakage: G, R, SE-blk(φ₀), EBM(M_n), CBL(η), η < η_A ⇒ 1 − π₀(S₀) = O_P(2^B√log n·n^{−κ}). Continuity: at fixed (n, blocks, y), η_W → 0 and b_X → 0 as ε → 0, so every constant in (b1)–(b5) tends to its block-orthogonal value. | (b1) PC1 §4 D.M10(ii), A.C9(b) TRUE-AS-WRITTEN on Dε; WS4(e) VERIFIED. (b2) PC1 D.M10(iii) COUNTEREXAMPLE repaired to this order. (b3) D.M10(iv) TRUE. (b4) A.C9(c) first equality TRUE; "hence within" COUNTEREXAMPLE repaired (transfer 1 + N_e Var). (b5) PC2 "D14 · one-shot / increment χ²" and "D14 · actual-grid moment" TRUE / DESIGN-VERIFIED (1,600 islands, good and poor V); OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; the m lower bound: PROVED (by this seat, unchecked; q₂(S₀)/π₀(S₀) = e^{2d(S₀)}/E_{π₀}e^{2d}). (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B). (b1)–(b4) are Seats A/D: PROVED (by that seat, unchecked). |
| **(c) One-shot refutation** (ships: Q1(c) check passed) | Proposition. (c1) G; ORTH (XᵀX = (n−1)I); fixed nonempty S₀ with fixed nonzero coefficients; the shipped score, IG(a₀,b₀), capped BB(1,p), state space; partition fixed in X; truth-free null count m → ∞ with log m = O(log n), m ≥ p/2 and p^{(α−1)R̄²}/[√n(log p)^{(1+(α−1)R̄²)/2}] → ∞. Then D_α(π‖π₀) → ∞ in probability; for α = 2, Var_{π₀}(π/π₀) = χ²(π‖π₀) → ∞ and ESS_∞ → 0, while, in the bounded-block setting (shipped B ≤ 16) or assuming π₀(S₀) → 1, TV(π, π₀) → 0. Explicit instance: p = n−1, one coefficient 2, σ² = 1 (R̄² = 4/5). (c2) If π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (T27(i)'s conclusion; H3 and the joint ratio law remain non-design premises) and π(S₀) → 1: ESS_∞ ≤ π₀(S₀)/π(S₀)² → 0, KL(π‖π₀) ≥ π(S₀)log(1/π₀(S₀)) − log 2 → ∞, TV → 1; the initial population holds S₀ with probability 1 − (1−π₀(S₀))^N ≤ Nπ₀(S₀) (initial; at later stages only "≤" is guaranteed); accepted grids need only T ≥ log₂[(ℓ₀+c_ρ)/(ℓ_T+c_ρ)] stages when π₀(V) is bounded below (set-mass and endpoint amendments). Neither result refutes the multistage sampler or (b). | OWS-WS6d, OWS-WS7: PROVED (SF: none; XF: none) + CHK_INHERITED §1, §2, §6 VERIFIED WITH AMENDMENT (PC1, cross-family): amendments above adopted verbatim; T03: PROVED-LOCKED; T27(i): PROVED-LOCKED, CONDITIONAL. |

| Field | Content |
|---|---|
| §3 repairs | B.D6(N) conceded (PC1 §4 COUNTEREXAMPLE); q₂ lemma route withdrawn (IMPLAUSIBLE), replaced by (b5)'s m bound; A/D repairs as listed; A.C8 guarantee: "the bridge need not be trivial" (z = 0 BO counterexample). |
| Placement | main (rank 3). Novelty: NEW-COMP (D_* decomposition and actual-grid moment bound are Seat C's; cite OWS-WS4 as nearest prior, PC2 novelty note; Frazier et al. 2023 Assumption 6(iv) as the generic χ² precedent). |
| Route / key lemma | (a2): PC2 Appendix A four steps (exact split; d_D ∈ [0, νx²/(2(1−x))]; eigenvalues of I + M in [1−δ, 1+δ]; resolvent bound \|t − t_D\| ≤ δ_H t_D/(1−δ_H)). (b1): WS1(a) and \|Λ − Λ^σ\| ≤ \|φ\|η_W. (b5): product of stage averages in [e^{Δ_t d_min}, e^{Δ_t d_max}], ΣΔ_t = 1 (coded snap ends at 1), E W = 1 (T12/N9). Key lemma: restriction monotonicity of zᵀH⁻¹z. |
| Lean core | (a3), (b1), (b5) on a finite space (cumulant identity, product-of-averages bounds, e^{−2osc d} bound); (a2)'s scalar log inequalities. |
| Fallback + stop | If (a2) fails in wave 2: (a1)+(a3)+(a4) with η_W (VERIFIED) and (b1)–(b4) ship; the ε-scale shrinks to ε = O(1/(nx̄)). If (b1)–(b4) fail: (b5)+(b6)+(c) ship with M₂ ≤ e^{osc d}. If both fail: escalate to HQ as unmet (never dropped). Stop: one check wave per half. |
| Honest ε-scale | Validity: every ε below the stated thresholds (a, δ, r < 1; ε_S < 1 − x̄_S). Usefulness (O(1) constants): (a2)/(b5) need νa² = O(1), i.e. signal energy O(√n), and b_X = O(1), i.e. ε ≲ λ_min/(p·νa) ≍ n^{−1/2}/p (PC2 item 3); with fixed signals the σ²-term alone is Θ(n) (WS3 scale remark) at any ε, including ε = 0. (b1)–(b4): η ≈ (n/2)εx̄/(1−x̄) = O(1) iff ε = O(1/(n x̄)) (CHK_INHERITED §4). Non-perturbative clauses: (b5)'s m form, (b6) at ψ_n = .001√(log n/n) ≫ n^{−1}, the exact identities; their constants are data quantities reported on the run card (§R5). |
| Necessity | Provable for osc d, false for weights. **Proposition NEC** (PROVED by this seat, unchecked): two blocks carrying truths j₁ ∈ C₁, j₂ ∈ C₂ with coefficients θ₁, θ₂, cross-correlation ε between them, exact Gram, SE-blk. With d = d_det + d_fit + d_σ (WS4 decomposition): osc d ≥ \|d(S₀) − d(∅)\| ≥ \| d_σ(S₀) − \|d_fit(S₀)\| \| − \|d_det(S₀)\|, where d_σ(S₀) = ν[Σ_b log(1−x_b) − log(1−x̄)] ≍ nθ₁²θ₂²/s_y⁴ (ε-free to first order), \|d_fit(S₀)\| = nεθ₁θ₂/(s_y²(1−x̄))·(1 + O(ε) + O_P(n^{−1/2})) (first-order term −cᵀM_Hc of WS4(b)'s identity, Gaussian LLN for z), \|d_det\| ≤ F_{S₀}/(4(1−ε)) = O(ε²). Hence at fixed ε and fixed signals osc d ≍ n except at one cancelling ε; at θ ≍ n^{−1/4}, osc d ≳ √n·ε − O(1) once ε > θ₁θ₂/(2s_y²) ≍ n^{−1/2}. So any bound of the D_*/η_W type is necessarily ≳ nεθ₁θ₂ in that regime: the (a2) scale is intrinsic up to the factor p. Route: WS3(c), WS4 proof identities, LLN. Companion: check 2 (osc d linear in n; ≈ √n·ε at θ = n^{−1/4}). The "weights unbounded at fixed ε" form is **not** provable: check 2 has log(1+χ²(π‖π₀)) ≤ 0.43 while osc d = 47–82, and my R1 table has χ² = .03 at ε = .2 with max\|d − d_σ\| = 25. Necessity concerns osc d and bounds built from it, not weight stability. |
| IC3 exhibit (method's own partition) | **Dε** (PC1 §"Dε"): n = 40, p = 8, exact Gram XᵀX = 39Σ, within .6, cross ε ∈ {10⁻⁵, 10⁻⁴, 10⁻³} (and 10⁻² in my check), β₀ = .25, β₄ = .2, σ = 1; K = 8, B = 2; complete linkage and the B = 2 cut recover {0,1},{2,3},{4,5},{6,7} (PC1 E2; my check 1, 40/40). Hypotheses: (b1)–(b4)'s A ≻ 0, ε_S < 1 − x̄_S, δ < 1, 0.9e^{4η} < 1, common pilot targets (PC1 E2, cross ≤ 10⁻⁴); (a2)'s a, δ_A, δ_H, r < 1 (check 1, all ε ≤ 10⁻²; D_* = .07–5.0 nats, osc d ≤ D_*). Two signal blocks, so d_σ > 0 and the baseline is non-trivial. Asymptotic family for (f)-type uses: C's §E family (groups of 9 at ¼, ε_n = 1/(np), two n^{−1/4} signals) with blocks = groups for n ≥ 9⁶ (PC2 cluster 4 AMBIGUOUS → "n ≥ 9⁶"). (b6): D_B (PC1 E4): p = 9⌊√n/9⌋, groups of 9 at .6, cross ψ_n = .001√(log n/n), truths .2, .25 in distinct groups, B = 16 eventually, 9 ≤ 16 < 18. |

---

## §R4 Masked-regime accuracy statement (HQ Q3)

**Named:** Theorem Z𝒯/CARD (K43, K45; with K42), card M5 clauses (b),(c), composed with Theorem HPM (b1-LH), card M6(2). Statement: on LH exact Gram with LS0, under M6's hypotheses, P(𝒪 ∩ {S₀ ∉ 𝒯}) → 0, hence with probability → 1 jointly with output the reported restricted posterior satisfies TV(π_𝒯, π) = 1 − Z_𝒯/Z ≤ δ₁ = O_P(√(log n/n)), |PIP^𝒯_j − PIP_j| ≤ δ₁ for all j, MPM^𝒯 = S₀, and Ẑ < Z_𝒯 certifies underestimation surely. **Why non-vacuous on a masked family:** LH is masked (π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)}, M4(c)), so every importance-weight quantity degenerates (M₂ unbounded, ESS_∞ → 0 by §R3(c2)); the statement bypasses the weights: S₀ enters 𝒯 through LS0 (T38-b1-LH, XF VERIFIED*), and (b),(c) are deterministic functions of the stored record, with no M₂, grid-quality or mixing premise. Statuses: MZ-P3 PROVED (P3 top store, deterministic) AUTHOR-ONLY; N13 PROVED (PC1 claim 5); T38-b1-LH PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); Thm5-LH SAME-FAMILY-ONLY. Fallback set for §5.4 confirmed as HQ listed it; reverse KL(π‖π̂) = ∞ whenever a positive-mass state is unrecorded (definitional, PC2 cluster 16; requires π(𝒯ᶜ) > 0, PC1 §16); masked final-estimate TV/KL = FW2 (V11, N10 OPEN).

---

## §R5 Run-card definitions (HQ Q4)

Both are POST HOC, computed from stored quantities only (X, blocks, tables, the final islands' initial and measured-endpoint particles, Ẑ_r, V), read no random numbers and feed nothing back.

| | (i) Jeffreys estimate Ĵ | (ii) Cross-block leakage proxy ε̂_× (companion η̂_V) |
|---|---|---|
| Definition | d(S) = log BF(S) − Σ_b log r_b(S_b) is the bridge potential already evaluated for every particle (N9 target audit, engine:89–101). d̄₀ := (R′N_e)⁻¹Σ_rΣ_i d(ξ⁽⁰⁾_{r,i}) over the initial particles (exact iid π₀ draws); H_r(d) := (4N_e)⁻¹Σ_{q,i}d(S_{rqi}) over the measured endpoints; μ̂_w(d) := Σ_rẐ_rH_r(d)/Σ_rẐ_r. **Ĵ := μ̂_w(d) − d̄₀.** | **ε̂_× := max_{b≠b′} max_{j∈C_b, l∈C_{b′}} \|r_{jl}\|**, r = G/(n−1) the standardised sample correlation, blocks as built. Companion: η̂_V := max_{S∈V}\|d(S) − d_σ(S)\|, d_σ from G_D with the same z, Y, over the calibration set V. |
| Numerical label | "Ĵ (nats): post hoc estimate of the Jeffreys divergence J = KL(π‖π₀) + KL(π₀‖π) between the start and the posterior; parts μ̂_w(d), d̄₀; conditional on N1." | "ε̂_× ∈ [0,1]: maximum absolute cross-block sample correlation after blocking"; "η̂_V (nats): discrepancy from the block-orthogonal bridge on V". |
| Theorems stated about it | (T1) J = π(d) − π₀(d) = ∫₀¹Var_{q_φ}(d)dφ ≥ 0 (PC1 §16 TRUE). (T2) E[d̄₀\|𝓒] = π₀(d), Var ≤ osc d²/(4R′N_e) (exact start, N9 S VERIFIED WITH AMENDMENT). (T3) Theorem H(b),(e) for h_d := (d − d_lo)/(d_hi − d_lo) ∈ [0,1] with the deterministic envelope d_hi − d_lo ≤ D̄_n := 2[ν log((2b₀+Y)/(2b₀+Y/(n+1))) + (K/2)log(n+1)] (TARGET envelopes, PC1 §20 TRUE): P(\|μ̂_w(d) − π(d)\| > εD̄_n \| 𝓒) ≤ min{1, 4(M₂−1)/R′ + 4M₂/(R′ε²)}, and μ̂_w(d) → π(d) a.s. as R′ → ∞; d must be in the declared list 𝓗 (§R7). (T4) 0 ≤ J ≤ osc d ≤ D_* under §R3(a2), and J ≥ 4TV(π,π₀)² (Pinsker twice): Ĵ reports the merge's divergence that (a) bounds. (T5) under §R3(c2), J ≥ (c log p + (c/2)log n)(1 − o_P(1)) − O_P(1): the masked regime shows as a large Ĵ. | (T1) ε_S ≤ \|S\|ε̂_×/φ₀² for every S (WS4 VERIFIED), so η_S, η_W in §R3(a4),(b1)–(b4) are explicit functions of (ε̂_×, K, φ₀, x̄). (T2) sup_{\|S\|≤K}\|d − d_σ\| ≤ η(ε̂_×) := K log(1/(1−δ)) + ν log(1/(1 − δū/((1−δ)(1−ū)))), δ = (K−1)ε̂_×/κ (D.M10(i), PC1 §4 TRUE on Dε). (T3) δ_A ≤ (n−1)(p−1)ε̂_×/λ_min(A_D), δ_H likewise (Gershgorin): §R3(a2)'s hypotheses are checkable from ε̂_×. (T4) ε̂_× = 0 ⇔ BO ⇒ d = d_σ exactly (WS3 VERIFIED). (T5) Under strict separation, ε̂_× ≤ max between-group \|r\| (BLOCKS, PC1 §19 TRUE). (T6) (b1)–(b3) hold with W = V and η_W replaced by η̂_V exactly (the proof uses only \|d − d_σ\| ≤ η on W). |

---

## §R6 Agenda items

**Item 6, thesis scope.** Remark only (concede D2). Scope of the remark: fixed data for (a) identities and (c) particle cost (M₂ ≤ e^{osc d}, R′ ≍ e^{osc d}/ε²), both for every X; depth (b) is a fixed-data bound T ≤ P + ⌈osc_V d/0.3246⌉ + 1 plus the ideal-grid crossing law log₂A₀ + O(1); selection (d) is asymptotic, favourable (b6 start, T03♯) or masked (HPM b1-LH) on separate sequences. Candidate non-corollary sentence "correlation increases depth and M₂" is false (non-monotone: R1 check, PC1 §11); the true non-monotone sentence is Proposition NEC's cancellation point. So: no theorem.

**Item 7, growth rates.** (1) Theorem H(f): R′_n = 4⌈log₂(n+p)⌉ (stacking configuration, R′ = 4k kept) on families with osc d = O_P(1); for simultaneous control over ≤ (n+p)² declared summaries, C's R′_n = 4⌈(n+p)⁶/4⌉. Method edit to record: "the asymptotic clause of Theorem H uses the stacking rate R′_n; the default R′ = 4 is unchanged". (2) HPM: ℓ = ⌈log₂(n+p+1)⌉ as shipped already ≥ c − 1; no edit. (3) STG: success requires T_e ≥ P + ⌈osc_V d/0.3246⌉ + 1; a hypothesis on reported numbers, no edit (schedule_limit is a status). (4) KERNEL/D15-TV terminal-law TV: L_n → ∞ with L_n ≥ e^{osc d}log(1/ε) would be needed for a rate; supplement remark only, no edit. (5) N: nothing. **D11 settled** as in §R1.

**Item 9, scope.** p ≤ n^A throughout (T03♯; polynomial budgets; (c1) at p = n−1 is a = 1). Exponential p (Song–Liang Cor 1, N12): FUTURE_WORK with reason: T03♯'s route needs the BB(1,p) prior tail and SE on sets of size j₀ uniformly over p = e^{Cn^α}, neither proved (N12 OPEN); the start's masking loss p^{−c} is polynomial, so the start theorems would survive but the target theorem would not. Nothing in reach.

**Item 10, novelty risks** (citations checked to the extent of the LIT report rows named):

| Overlap | Citation checked | Theorem touched | Wording |
|---|---|---|---|
| Hou–Wang–Atchadé | arXiv:2407.20580 Thm 2 (LIT-STAT row 19; venue UNVERIFIED) | HPM (0), N200 | no "first finite-n" claim; N200 is a composition with measured Π(X) |
| YWJ 2016 | AoS 44(6) Thm 2, Lemma 4 (LIT-MCMC row 1, LIT-SMC row 21) | HPM (b1-LH), LS-score | "for the paper's own target and start"; cite Lemma 4 next to Theorem A |
| ZYVR 2022 | JRSS-B 84(5) Thm 1, Condition 1 (LIT-MCMC row 2) | HPM, Theorem D remark | Condition 1 fails for our prior/cap; no mixing claim |
| Atchadé 2021 | SIMODS Thm 6 warm start (LIT-MCMC row 14) | Theorem 2 (favourable/masked) | cite as closest analogue |
| Del Moral–Doucet–Jasra 2006; Del Moral 2004 | JRSS-B 68 Prop 2; book UNVERIFIED (LIT-SMC row 1) | V+ (a),(b) | cited lemmas |
| Vergé et al. 2015 | Stat. Comput. 25(2) (LIT-SMC row 6) | PIP-eq | cited; Ẑ-weighting is the contrast |
| Cérou–Del Moral–Guyader 2011 | AIHP 47(3) Thm 1.4/1.5 (LIT-SMC rows 2, §3A) | Theorem Z(i) | novelty unchecked → citation checker |
| Chatterjee–Diaconis 2018 | AAP Thm 1.1/1.2; Thm 2.1-type (R1_B D5, D15) | SEP (c), LIM (a) | exp(KL) scale cited |
| Frazier et al. 2023 | Assumption 6(iv) (THM-INV §4b via A) | WS package | generic χ² precedent |
| Mengersen–Tweedie 1996; SVV 2009; Syed et al. 2024 Thm 3; Barbieri–Berger 2004; Papaspiliopoulos–Rossell 2017; Rossell 2022 Prop 1; Gelman–Meng 1998; Chopin 2004 | as in R1_B cards | KERNEL, STG, R2, Theorem 2, T03♯, IDENT | cited lemmas |

**Item 11, final lists.**

| Rank | Main (≤ 8) | K-IDs |
|---|---|---|
| 1 | Proposition V+ (general-h identity N1) | K35, K46, K32, K86, K36, K50 |
| 2 | Theorem H | K51, K52, K48 |
| 3 | Theorem WS (§5.3 package (a)(b)(c)) | K102, K10, K11, K25, K27, K53, K104 |
| 4 | Theorem 2 (start, masking, dilution) | K15, K17, K18, K10 |
| 5 | Theorem Z𝒯 / CARD (masked-regime statement) | K42, K43, K45, K36, K78, K44 |
| 6 | Theorem HPM | K72, K68, K69, K70, K65, K63, K62 |
| 7 | Theorem STG | K26, K27, K30, K28 |
| 8 | Theorem SEP + Lemma KL | K106, K105, K19 |

Supplement: S1 SL (K97); S2 Theorem 1 (K93); S3 Theorem D (K87–K89, K06, K64); S4 Theorem Z (K37–K41, K53); S5 KERNEL (K20, K21, K08, K09, K22, K23, K103); S6 LIM (K79, K74, K81, K100, K101); S7 TARGET (K01–K04, K95, K76); S8 CERT (K64, K73, K05, K108); S9 IDENT (K25, K104, K54, K55); S10 PIP-eq (K49, K50, K57); S11 BLOCKS (K07, K14, K06); Theorem 2(e) favourable rate (K16); STG(f) (K29). Remark: CD (K96). FUTURE_WORK with reason: K31, K58, K59, K71, K24, K75, K92, K13, K80, K94, K107, K99 quantitative, N12, Π(X), V11 (FW2), FW1. Dropped: K98, K66, K67, K12, K34, K91.

**Item 1 closure.** THM-INV cells marked "nothing provable" (paper 1), each with reason: (1) coefficient/Hellinger contraction: no contraction theorem for the ridge/IG target (FUTURE_WORK, SL Thm 1); (1) growing s₀: T03♯ needs fixed s₀ (N12); (4) backfit start: rejected by the method; (7) rebuild convergence, P(S₀ ∈ V), P(schedule_limit): V is a data-and-MC-dependent top set with no stability theorem; (8) speed-up vs MCMC: no accuracy-matched comparator theorem; (11) P(U) → 0: no route (every result joint with 𝒪, liminf form); (11) finite-n Gibbs discovery: ThmB-T24 vacuous at n = 200; (13) positive flag power K80: no sampling law for the flags; (14) validated numerics K107: N16 OPEN. D16 disposition: K23 provable (supplement lemma), K80 and K107 "nothing provable now". Song–Liang wording: §R1 row D15.

---

## §R7 Questions for HQ

1. Ĵ requires d to be a default member of the declared list 𝓗 (METHOD §6.11b, fixed from (X, y) before stream 10, reads no uniforms). Please confirm this is covered by AMENDMENT_HQ_02 as a reporting addition. No other question.