# Round 1, Seat D (Fable 5.1, Claude Personal, high; fresh eyes in Round 0)

Verbatim final message, extracted by the chair from `~/.claude-personal/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/d709bf61-631a-4e8a-a307-4952ff3dad9c.jsonl` (completed 2026-11-04 02:26 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

# R1_D — Seat D, Round 1 (MEET-THM)

## §0 Round 0 positions changed by the registry, the draft list or Advisor E (one line each)

| R0_D item | K | Change and why |
|---|---|---|
| HP3 (landscape) | K66 | Withdrawn. C3-PGD (a null resembling two truths is added first) and CEX-localmax(A2) hold for every beta-min constant, since scaling β scales both gains; no enlarged constant escapes. The provable form is Theorem A + Lemma M (K65). |
| HP4, HP5, KN5 | K67, K14, K24 | Their landscape input is gone. HP4 on orthogonal blocks is the ORTH family of R5(a) (ORTH-joint PROOF SKETCH, registry C9), merged into K68. HP5 keeps only its deterministic half (K14). KN5: N10 "YWJ/ZYVR route blocked as stated"; LIT-MCMC shows R > M fails at n ≤ 1,600: future work. |
| PA1 depth free of N, H, R | K88 | Dropped: INP M13 "Free of N, H, R dropped for v3.1"; island-level depth only (Felipe). |
| NG3 "nothing bounds Z from above" | K44, K79 | Narrowed to T31(c)'s non-implication; N17's analytic bound is PROVED and Advisor E's U_rest bracket is valid. |
| HP6 `global_certified` correct modulo NU1 | K73 | Withdrawn: N7 "rigorous global_certified … not a theorem" (η uses a lower condition-number estimate). The theorem is the region certificate R (OCERT-C4 + Lemma M). |
| CL3 flag power | K80 | Dropped: INP row 13 "positive power → empty (labelled heuristics)"; what I computed is a null firing rate, not power. |
| EV2 perfect mixing, PA5 SMC-vs-MCMC | K39, K91 | EV2 = OWS-WS8(b) (cite, do not re-derive); OPW2-cex refutes a_t = χ²_t for the implemented kernel; PA5 rested on it and INP §5 row 8 makes the speed-up empirical: dropped as a theorem. |
| HP2 scan bound p + K(p−K) | K64 | Corrected to p + k*(p − k*), k* = min(K, ⌊p/2⌋), × (ℓ+1) (INP row 12; Advisor E's p = K = 8 check). |
| TG4 (log p = o(n)) | K93 | Replaced by T03♯ with p ≤ n^A; p ≤ e^{Cn^α} is N12 OPEN for our prior. |
| EV1 "unconditionally for the complete method" | K35 | Wording adopts the output convention M11: joint with 𝒪, never conditional; CEX-guard. |
| KN4 constant 1/(mM_φ) | K103 | Advisor E is right: every order contains the independence step, and the steps after it preserve π_φ, so the round minorises by 1/M_φ. |
| PI3 RB variance "for every kernel" | K56 | Restricted to the one-step statement; no ordering for the four-round ratio-pooled estimator (E §5.2). |
| ST2's guarantee "the bridge is never trivial" | K10 | Weakened by my own check (§E companion): the σ²-coupling shifts d by Θ(n) on S₀ but shifts the whole π₀-mass alike, so the one-shot χ² stays bounded there; instability needs noise chasing (OWS-WS6d) or masking (OWS-WS7). |
| ST2, ST4, BR4, BR3, PI2, KN1/2, HP1, TG1(b), EV1 | K10, K11, K30, K28, K48, K20/21, K63, K44, K35 | Registry rows exist (OWS-WS3/FD-W1, OWS-WS4, STG-M, STG-L, MA-PropP, N9K/T09, MA-LemmaS, N17, T12/T31(i)): I cite them and add only what is not there. Note: the registrar's "No registry row" for K11 is wrong; OWS-WS4 is its row. |
| TG2(b) vs E's T02 constant | K03 | Resolved: 2νb₀ = (n + 2a₀)b₀ already contains E's 2a₀b₀ term; the method text's n·b₀ is the approximation. |
| HP7/NG8, PA6, NG13 | K75, K92, K99 | Kept deferred to paper 2 (E agrees hardness needs its own reduction). |

## §A Coverage sweep

### A1 Proposal goals

| Goal | Delivered by (K-IDs → §D card) | Reason if not delivered |
|---|---|---|
| §5.1 exactness under MH correction | K20, K21, K08 (N9K PROVED (candidate); T09 PROVED-LOCKED) → M1 | — (textbook in kind; the method-specific lemma is N9, a closure gate) |
| §5.2 SMC consistency for the local-to-global sequence | K35, K47, K48 → M1, S5 (cited lemmas: Del Moral et al. 2006; Whiteley–Lee–Heine 2016; Dai et al. 2022) | — (ADRAFT-ThmA is Astra-only: cite instead) |
| §5.3 weight stability under weak cross-block dependence | K102 restated as Theorem WS-ε with K11 (= OWS-WS4), K10 (= OWS-WS3), K25, K103 → M10; H-ORTH results W(a–f), WS6, WS7 as the ε = 0 baseline | Delivered in bridge form; the one-shot form is false in two regimes for reasons unrelated to cross-block correlation (OWS-WS6d, WS7): see §E, §I Q1 |
| §5.4 PIP error | K51, K52 (PC1 claim 3 PROVED), K43, K57 → M2, M3, S7 | — |
| §5.4 joint-PIP error | K51 + K46 (N1 PROOF SKETCH; plain averages, c_h = 0) → M2 | binding §13.1; failure escalates (N1) |
| §5.4 TV error | start-vs-posterior TV: K104, K105, K108 → S8 (card F2); delivered-population TV: K103 (favourable only) → S8; TV of the final pooled estimate in the masked regime: obligation N4(iii)/N10 OPEN (card F3) | the masked-regime TV bound needs E[W²|𝓒] or a mixing input, both OPEN; not dropped: carried as an obligation with fallback |
| §5.4 KL error | K104 (= OWS-WS1 identities), K105 (Lemma KL) → M7, S8 | — |
| §5.4 credible-interval coverage error | transfer lemma (card F1, corollary of K51/K52 with h_I(S) = P(β_j ∈ I \| S, X, y)) → M2 | frequentist coverage of credible sets: not a target (INP row 10 "rejected") |
| §13.1 E_π[h] converges to the truth | K51(d) with T03♯ (K93) and R_n ≫ E[W²\|𝓒_n] → M2 | R_n condition disclosed; E[W²] upper bound OPEN (N4(iii)) |
| §4.4 / §8.2 diagnostics (ESS, local–global discrepancy) | K25 (exact coverage factor of restricted ESS) → M9; K42 (Ẑ < Z_𝒯 certificate) → M3; K104 (Ĵ, J identity) → S8 | positive power of any flag: nothing provable (I5, INP row 13: flags are labelled heuristics by decision) |

### A2 Song–Liang 2015

| SL result | K-IDs → card | Reason it does not apply / what we lack |
|---|---|---|
| Thm 1 (Hellinger consistency, bounded predictors) | K93 (T03♯) → M12 for selection | Hellinger/predictive contraction rates are not a paper-1 target (INV §3b LACK); our prior and technique differ; future work |
| Thm 2 (Condition 1 tails) | K93 | same |
| Cor 1 (rates; P_n < e^{Cn^α}) | K93 with p ≤ n^A | p ≤ e^{Cn^α}: N12 "OPEN, not impossible" for BB(1,p) + g = n + cap; cannot import SL's conditions |
| Thm 3 (sure screening) | K93 (large signals get PIP → 1 without beta-min) → M12; estimated PIPs: K52 (M2), K43 (M3) | — |
| Thm 4 (misspecified subset posterior) | K10, K17, K18 → M6 (our blocks are misspecified-subset posteriors; we quantify the loss) | EXCEED in kind |
| Cor 2 (eq. 19, β₀,t ≠ 0 retention) | K97 → M8 (orthogonal-null zero identity) | — |
| Thm S (MAP consistency) | K93 (HPM of π) + K72, K69 (reported HPM) → M4, M5 | EXCEED: SL has no theorem for the merged output |
| §6 complexity (K_n = √P_n, O(P_n^{(1+α)/2}) + O(nP_n)) | K87, K88, K90 → M13 (same units: work/depth/width) | no accuracy trade-off in SL; ours states depth at island level only |

### A3 THM-INV §1 empty or partial cells

| Row × cell | K-ID / card | "Nothing provable" reason |
|---|---|---|
| 1 Π(X) finite-n upper bound | K94 defer (OPEN; E's T34 fractional-odds route = future work) | envelopes M_{a,b} for this ridge/BB/cap posterior unproved |
| 1 contraction rates; growing s₀ | — | not a v1 target; prior theory is fixed-s₀ (N12) |
| 2 n = 2 extension; eventual exactness | K02, K76 → S1, S12 | — |
| 3 study packing (g = 5, 2g ≤ B) | K07 obligation N8 OPEN (PART-pairing) | — |
| 3 adaptive / overlapping partitions | — | WORKHORSE; outside the fixed method |
| 4 exact start sampler | K08 (N9K PROVED (candidate)) → M1 | — |
| 4 backfit start; start depth comparison | — | rejected (future work); N18 not opened (Outcome 2) |
| 5 as-coded masked T_n | K31 OPEN; fallback T ≤ T_e (K26) → M9 | — |
| 5 depth vs correlation | K30 (ideal grid, log₂A₀) + M10 (η(ε) sandwich) | as-coded law OPEN |
| 6 mixing / spectral gap | K24 future (N10); K103 unconditional Doeblin → S8 | Doeblin constant exponential under masking |
| 7 rebuild convergence, P(S₀ ∈ V), P(schedule_limit) | K31, K33 OPEN obligations → S10 | — |
| 7 V coverage | K25 identity (what ρ_V ≥ 0.9 certifies) → M9 | no probability bound: V's complement is never inspected (I9(d)) |
| 8 work–depth; R vs N; island variance vs correlation; speed-up vs MCMC | K87/K88 (M13); K59 defer; M10 partial + N4(iii) OPEN; — | speed-up vs MCMC empirical (INP §5 row 8) |
| 9 two-sided masked Ẑ; upper bound on Z; fp | V11 OPEN (K53 obligation); K44 (N17) → S6; K107/K108 → S9 | validated SC OPEN (N16) |
| 10 joint inclusion; equal-weight at fixed R; credible sets | K51/K46 (M2); K49/K57 (S5, S7); card F1 (M2) | frequentist credible-set coverage: rejected target |
| 11 P(U) → 0; finite-n Gibbs discovery; study generator | K82 OPEN (not a theorem); —; K07 (N8) | no route for Gibbs discovery |
| 12 meaning of `local_certified`; LS0 in production | K64 (card L1 semantics) → S9; N2(c) engineering | — |
| 13 positive flag power | — | I5; heuristics by decision |
| 14 P(resource_limit) etc.; fp theorem | — ; K108 (perturbation lemma) → S9, N16 OPEN | allocation-dependent (I9(e)) |

## §B The draft list, item by item

| Entry | K-ID | Decision | Corrected statement or reason | IC |
|---|---|---|---|---|
| V1 | K20, K21, K32, K35, K36, K46, K47, K48, K50, K86 | keep, split (a1)/(a2); SMC identities demoted to cited lemmas | Theorem V = N9 lemma (K20/K21, PROVED (candidate)) + frozen-𝓒 contract (K32, K86) + islandwise identities for Ẑ_r, RB-PIP (locked) and general h (N1, PROOF SKETCH) for any R′ declared before stream 10; hypotheses EX-A, EX-S, CAL, (H-U), GUARD-W. → M1 | IC4, IC1 |
| V2 | K63, K83, K84, K86 | keep, supplement | Lemma S + Prop W (3/3 designs executed) + W-cal (not executed) + Cor W-R(b) (extra search from c₄ kept). → S4 | IC5 |
| V3 | K47, K48, K49, K50, K85 | keep, supplement; (iii) merged into A1 | "primary" = Ẑ-weighted; add PC1 claim 3 (K52); (i),(ii) cited (Vergé; WLH). → S5 | IC4 |
| V4 | K77, K78 | keep, supplement | Lemma RO + CEX-guard; GUARD-W = code-audit obligation N2(e); output convention M11. → S4 | IC1 |
| A1 | K51, K52, K46, K48 | keep, main | Restated around M9: plain averages, c_h = 0 for joint h; h measurable in (X, y, 𝓒); (b) with PC1 claim 3; (d) with R_n hypothesis and the lower bound E[W²] ≳ 1/P_𝓒(cross) disclosed; crux N1. → M2 | IC2 (check wave 1) |
| A2 | K35, K36, K38, K39, K40, K41, K42, K53, K79 | split | (i) cited lemma; (ii) OPW2 Thm A as "a form of CDG 2011 Thm 1.4 specialised to v3" (S6); (iii) masked lower tail with PC1 claim-4 wording, never "only downward" (S6); (iv) certificate → M3; (v) remark (S6). | IC4, IC1 |
| A3 | K42, K43, K45 | keep, main (merged with card G1/G2 and N13) | If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯, Z_𝒯/Z ∈ [1−δ₁, 1], \|PIP^𝒯 − PIP\| ≤ δ₁, MPM^𝒯 = S₀ (½ sharp); joint with output, never conditional. → M3 | IC1 |
| A4 | K57, K58 | P1 supplement; Thm R defer (v2) | equal-weight is secondary; Thm R CONDITIONAL on DELIV-POP OPEN. → S7 | IC2 |
| D1 | K87, K88, K89, K90, K64 | keep as a proposition, island level | (b) depth N_e(T+L+4)(p+B+2) step slots + setup + calibration (1+I_e)H_e + LS0 + extra search; (c) struck ("free of N, H, R" is v3.2); (d) SL §6 comparison, accounting only. → M13 | IC1 |
| D2 | K26, K27, K28, K29, K30, K31 | keep, main | (a) Theorem G as-coded, ESS 0.90 a hypothesis; (b) STG-F; (c) STG-M on the ideal two-state grid stated as such; (d) cited; as-coded masked T_n = obligation K31 with fallback T ≤ T_e. → M9 | IC1 |
| D3 | K96 | keep, main; restate | (b) island-level depth; (c) E[W²] lower bound disclosed, upper OPEN; (d) via R5(b1-LH); exact scope at agenda 6. → M11 | IC2 |
| D4 | K59 | defer (v2) | v1 states Prop P(i),(ii) and the "never split N_e" decision (S5). | IC2 |
| S1 | K15, K16, K17, K18, K10 | keep, main; (b) supplement | add (e) the BO discrepancy identity d = d_σ ≥ 0 (OWS-WS3/FD-W1) as the ε = 0 input of M10; never combine (b) and (c). → M6 | IC1 |
| S2 | K19, K105, K106 | keep, main | Lemma KL to check wave 1; (d) "moving off the start is needed". → M7 | IC1 |
| S3 | K98 | drop | SHARE-M(b) ERROR, FD-NM ERROR; replaced by S2 + Prop M-LH remark | IC1/IC2 |
| S4 | K102 (+K10, K11, K25, K103) | restate → main | Theorem WS-ε (§E): deterministic continuity of d, χ², stage count and Doeblin constant in ε with explicit η(ε); H-ORTH W(a–f)/WS6/WS7 as the ε = 0 baseline (supplement). → M10 | IC3 now met |
| C1 | K97 | keep, main | (b)'s PIP → 0 step is the one obligation; re-run on the LH family with g ≥ 2, K ∈ {2, 4, √p}; cite SL Thm 4/Cor 2/eq. (19)/Condition 5. → M8 | IC2 |
| R1 | K93, K04 | keep, main (short) | MODEST; cite Rossell 2022, MGC 2015; novelty = exact BB(1,p) tail and cap ≍ n; disclose n ≳ 2·10⁶. → M12 | IC4 (partly) |
| R2 | K60, K61, K101 | demote to cited lemma + remark | Barbieri–Berger 2004; keep (iii) size-prior ceiling, cap-constrained Hamming action, posterior FDP bound. → S3 | IC4 |
| R3 | K65, K63 | keep (inside M5) | new hypotheses: LS0 centre = prescribed start mode (e4; DP invariant N3 OPEN), ℓ ≥ max{Φ(S°)−1, 0} (N11), completed scans / OP-LS0. | IC1 |
| R4 | K72, K78, K82 | keep, main | add PC1 claim 5(a); output-event form; R′ transfer only with the extra search; no "first finite-n" (Hou–Wang–Atchadé). → M4 | IC1 |
| R5 | K68, K69, K70, K71, K72, K87 | keep, main; (b2-LH) supplement corollary; (b1-LH-iid) defer | headline (b1-LH) for the shipped method with LS0 under OP-LS0, e4, SIZE, GUARD-W; (a) favourable with ORTH family (PROOF SKETCH). → M5 | IC1 (fidelity N2(c), N3) |
| R6 | K82 | reject as theorem; OPEN obligation (delivery) | report P(U) = 6/2,400 with the allocation; remove "4× headroom"; not a limitation (INP §4.B) | IC2 |
| R7 | K94 | defer (v2) | OPEN; E's T34 fractional-odds framework recorded as the route (future work) | IC2 |

## §C New candidates and every K-ID not covered by §B

| K-ID | Place | Reason (≤ 40 words) |
|---|---|---|
| K01 | supplement (S1) | Propriety and envelopes: finite algebra, Lean-able; composed with N17 (PROVED). |
| K02 | supplement (S1) | Invariance/equivariance in law; n = 2 branch seat-derived, unchecked (N12). |
| K03 | supplement (S1) | Reduction identity + IG bound; constants reconciled (§0). |
| K04 | supplement (S1), feeds M12 | BB(1,p) mass/size law/cap conditioning: finite sums, Lean target. |
| K05 | supplement (S9) | Superset bound for the region certificate R; Furnival–Wilson idea, cited; deterministic. |
| K06 | supplement (S2) | Block count and table cost: deterministic counting. |
| K07 | supplement (S2) + obligation N8 | PART-ThmA PROVED XF VERIFIED* for the strict-gap case; study packing OPEN. |
| K08 | main (M1) | N9 closure gate: exact start sampler and Z̄₀, PROVED (candidate), code-checked. |
| K09 | supplement (S2) + obligation N3 | Tie-aware DP invariant OPEN; needed by LS0 centre hypothesis. |
| K10 | main (M6(e), M10 baseline) | = OWS-WS3 / FD-W1 (XF VERIFIED): cite; ε = 0 input of WS-ε. |
| K11 | main (M10) | = OWS-WS4 (author-only PROVED): cite; WS-ε adds the χ²/stage/Doeblin consequences. |
| K12 | drop (engineering) | Test oracle under BO, not a guarantee; useful for check waves only. |
| K13 | future work | Start-mode consistency under BO needs TG4-type tails; superseded by R5(a)/ORTH family. |
| K14 | supplement (S2) | Deterministic half only: every block sub-model is scored, so the HPM beats every block-local model; the "= S₀" half withdrawn (landscape). |
| K22 | supplement (S2) | Graph facts: engineering; spurious-edge count per vertex, not familywise. |
| K23 | future work | Dirichlet comparison has no consumer once K24 is deferred. |
| K24 | future work | N10 OPEN; route blocked (LIT-MCMC: R > M fails at n ≤ 1,600). |
| K25 | main (M9) | Exact coverage factor a_u a_w/a_v² (BR1 = E's T14): what ρ_V ≥ 0.9 certifies; Lean-able. |
| K27 | supplement (S10) | Interval bound (v−u)²Var(d) ≤ log(10/9): analytical, not run-observable; feeds M9 remark. |
| K33 | supplement (S10) | Calibration termination and cost; N15 share seat-derived. |
| K34 | drop | TI evidence is not in v3.1 (reporting proposal only). |
| K37 | supplement (S6) | Island-minimum bound 0.05^{1/R}·min_r Ẑ_r: elementary, valid, better than Markov when islands agree. |
| K44 | supplement (S6 remark) | N17 PROVED; E's U_rest bracket: deterministic from the score envelope. |
| K45 | main (M3) | N13 retention lemma PROVED (PC1 claim 5); premise of A3∘R5. |
| K52 | main (M2) | PC1 claim 3 PROVED given N1; the finite-R statement a referee asks for. |
| K54 | supplement (S5) | R_eff = Kish number; reporting-layer; R = 4 gives no coverage. |
| K55 | cited lemma | CLTs in N (Chopin 2004; Del Moral 2004); IC4. |
| K56 | supplement (S5 remark) | One-step RB variance reduction only. |
| K61 | supplement (S3) | Posterior FDP ≤ q for {PIP > 1−q}: Müller–Parmigiani–Rice-type, exact PIPs only. |
| K62 | supplement (S3) | Margin transfer: estimated MPM = exact MPM when PIP errors < margin; deterministic, Lean. |
| K66 | drop | PARTLY-FALSE; see §0. |
| K67 | drop (merge residue into K68) | PARTLY-FALSE; ORTH family already PROOF SKETCH under R5(a). |
| K73 | supplement (S9) | Region certificate R: OCERT-C4 + Lemma M PROVED XF VERIFIED; `global_certified` stays heuristic. |
| K74 | supplement (S9 remark) | Restates CEX-localmax(A2), CEX2; limitation, consistent with registry. |
| K75 | future work (paper 2) | Needs its own reduction for this score; both fresh seats agree. |
| K76 | supplement (S12) | Fixed p eventually exact (N12, seat-proved, unchecked); corrects T26-exact-branch-paren. |
| K80 | drop | Flag power empty by decision; false-alarm rate uninteresting. |
| K81 | supplement (S11 remark) | Restates CEX-ESSneutral(A3). |
| K91 | drop | Rests on the perfect-mixing formula; speed-up vs MCMC is empirical (INP §5 row 8). |
| K92 | future work (paper 2) | Needs NG1's unproved moat lemma. |
| K95 | supplement (S3) | Finite-data odds identity π(S₀) = 1/(1+A(S₀)) and certificate; Lean-friendly; A sums over Ω. |
| K99 | supplement (S11 remark) via SHARE-PB; quantitative NG1 future work | SHARE-PB COUNTEREXAMPLE already records the barrier; k-way budget bound unproved. |
| K100 | supplement (S11 remark) | Duplicates/identifiability: PropD-T03, CEX-ties(A2) exist; PIP → 1/d is elementary. |
| K101 | supplement (S3) | MPM may exceed K; cap-constrained Hamming action: trivial, worth one line. |
| K103 | supplement (S8) | Doeblin minorisation with E's constant 1/M_φ; textbook (Mengersen–Tweedie); §5.4 TV in the favourable regime only. |
| K104 | supplement (S8) | = OWS-WS1 + Gelman–Meng identities; cite; feeds §5.4 KL and Ĵ. |
| K107 | supplement (S9) + obligation N16 | Rounding bound and validated-arithmetic contract; T33-errbound says error_bound() is not a bound at large n. |
| K108 | supplement (S9) | Deterministic perturbation lemma (Z̃/Z ∈ e^{±ε}, TV ≤ tanh ε, winner gap > 2ε): Lean-able; also gives §5.4 TV of the start. |

## §D Theorem cards

### M1 · Theorem V (validity of v3.1 as shipped) — K20, K21, K08, K35, K46, K32, K86, K85

| Field | Content |
|---|---|
| Statement | Assume EX-A, EX-S, (H-U), CAL (𝓒 frozen on streams 0–9), GUARD-W, R′ = 4k declared before stream 10. (a) Each Gibbs flip, uniform swap, neighbour swap and independence move is γ_φ-reversible; the uniformly random-order round is γ_φ-invariant and self-adjoint; draw_pi0 and Z̄₀ are exact (N9). (b) Conditionally on any frozen 𝓒, E[Ẑ_r] = Z and E[Ẑ_r·PIP̂_rj] = Z·PIP_j (locked); E[Ẑ_r·H_r(h)] = Z·π(h) for h ∈ 𝓗 measurable in (X, y, 𝓒) (N1). (c) Statements hold for the potential run and as P{𝒪, ·}. |
| Guarantee | Whatever the correlation, every island targets π exactly and its evidence-weighted records are unbiased; parallel islands never change this. |
| Serves | §5.1, §5.2; objective (1); SL Thm S input. |
| Status (verbatim) | N9K: "PROVED (candidate)" (code-checked at 39db138); T12, T31(i): "PROVED-LOCKED"; Prop2(a,b,d,e): "PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4))"; N1: "PROOF SKETCH"; IND-T: "PROVED (SF: none; XF: VERIFIED* (A-REV1))". About v3.1 as shipped: kernels yes (N9 audits production step functions); LS0 irrelevant; grid any frozen; pooling: islandwise. |
| Self-checked only? | N9K: author + numerical check, no independent review (escalate); Prop 2: XF GAP; N1 unchecked. |
| Novelty | KNOWN—CITE for the SMC identities (Del Moral et al. 2006; WLH 2016); method-specific lemma N9 and the general-h identity are ours (MODEST). |
| Route / key lemma | N9 PROOF.md Claims R, S; N1 by the resample–move recursion at the measured endpoints (R2C route). Difficulty S–M. |
| Lean core | Detailed balance of the four kernels on a finite space; permutation-reversal self-adjointness; T12Core `hstep` discharge. |
| Dependencies / risk | None / N1 fails → A1 shrinks to marginal PIPs and §13.1 escalates. |
| Fallback + stop rule | (a),(b) for Ẑ_r and RB-PIP (locked) with general h as a PROOF SKETCH remark; stop if N1 is not checked within one HQ cycle. |
| IC3 design | Any finite X: no hypothesis on correlation. |
| Numerical companion | N9-KERNEL CHECK.md (DB rel ≤ 2.3e-12, 3 designs). |

### M2 · Theorem H (Ẑ-weighted bounded functionals, joint inclusion, finite R) — K51, K52, K48, K54; corollary F1

| Field | Content |
|---|---|
| Statement | Setting of M1; h ∈ 𝓗, 0 ≤ h ≤ 1, plain measured-round averages (c_h = 0); W_r = Ẑ_r/Z, M = E[W_r²\|𝓒]. (a) E[W_r\|H_r(h) − h(S₀)\|\|𝓒] ≤ 2δ₁ (M1 mechanism). (b) P(\|μ̂(h) − π(h)\| > ε\|𝓒) ≤ min{1, 4(M−1)/R + 4M/(Rε²)} (PC1 claim 3). (c) h_A = 1{A ⊆ S} gives joint inclusions; h_I(S) = P(β_j ∈ I\|S, X, y) gives credible-interval probabilities with coverage error ≤ the same bound (F1). (d) With T03♯ and R_n(1−s)²/M_n → ∞ in probability, μ̂(h) → h(S₀) jointly with output. (e) Fixed data: μ̂(h) → π(h) a.s. as R′ → ∞ (cited). |
| Guarantee | Every reported posterior summary is right on evidence-carrying islands and pooling enough islands by Ẑ makes it right; (b) says what R buys. |
| Serves | §13.1 (binding), §5.4 PIP/joint-PIP/credible-interval; objective (1). |
| Status (verbatim) | A1new: "PROOF SKETCH (NEW-SYNTH)"; FMP-M1: "PROVED (SF: none; XF: VERIFIED (A-REV9))"; PC1c3: "PROVED (PC1 claim 3)" with E[W_r ĥ_r] = π(h) a premise (N1); MA-PropP: "PROVED (elementary)". Shipped: Ẑ-weighted primary yes; LS0 n/a; grid any frozen. |
| Self-checked only? | PC1 claim 3 Astra-authored, Opus-checked; (a) with general h unchecked. |
| Novelty | NEW-COMP (M1 mechanism ours; SLLN cited). |
| Route / key lemma | N1 identity → M1's proof with h → Prop P(iii)/PC1 claim 3; F1 by data processing on the finite model space. Difficulty M. |
| Lean core | (a)'s deterministic step, (b)'s Chebyshev/denominator argument, F1's inequality: finite. |
| Dependencies / risk | M1 (N1), M12 for (d) / M_n unbounded (N4(iii) OPEN): (d) is hypothesis-laden. |
| Fallback + stop rule | (a)–(c),(e) as theorems; (d) with R_n as a hypothesis and the lower bound M ≳ 1/P_𝓒(cross) disclosed. Stop: if N1 fails, escalate (binding). |
| IC3 design | Any X; (d) on LH (T03♯ hypotheses verified there). |
| Numerical companion | none needed (identities); optional 20-seed check of (b) on p = 8. |

### M3 · Theorem Z𝒯 and the certificate card — K42, K43, K45, K36, K78, K44

| Field | Content |
|---|---|
| Statement | 𝒯 the deduplicated reported store, Z_𝒯 = Σ_𝒯 ϖm. (a) Z_𝒯 ≤ Z surely; Ẑ < Z_𝒯 ⇒ Ẑ < Z. (b) If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 (N13), 1−δ₁ ≤ Z_𝒯/Z ≤ 1, \|PIP^𝒯_j − PIP_j\| ≤ δ₁, MPM^𝒯 = S₀ (½ sharp). (c) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) under Lemma RO + GUARD-W, CAL, EX-S. (d) Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} (N17). |
| Guarantee | The one two-sided, grid-free, mixing-free evidence quantity is the top-store sum; the run's lower bound keeps 95% jointly with output. |
| Serves | §5.4 PIP error (masked), §4.4 diagnostics (positive certificates); objective (1). |
| Status (verbatim) | MZ-C1: "PROVED (C1-C3 per-fit, deterministic)"; MZ-P3: "PROVED (P3 top store, deterministic)"; N13: "PROVED (PC1 claim 5; R2C D7)"; PC1c5: "(a) PROVED, ½ sharp"; N6(a): "PROVED (potential run; output form CORRECT WITH AMENDMENT)"; N17: "PROVED (PC1 claim 1; PC2 C1(c))". Shipped: LS0 yes (𝒯_new = top_c(𝒯_old ∪ 𝒮_added), card L3 premise); grid any; pooling n/a. |
| Self-checked only? | MZ rows "candidate: not reviewed"; PC1 claims cross-checked (Astra→Opus). |
| Novelty | NEW in kind (reported-quantity trick), elementary; Markov part KNOWN—CITE (Grosse et al. 2015). |
| Route / key lemma | finite sums; Lemma S for retention; Markov. Difficulty S. |
| Lean core | (a),(b),(d): entirely finite/algebraic. |
| Dependencies / risk | M5 for S₀ ∈ 𝒮; GUARD-W audit N2(e) / fp label until SC + VAL-FP (N16). |
| Fallback + stop rule | (a),(b),(d) deterministic; (c) for the potential run only if GUARD-W fails. No stop needed. |
| IC3 design | Any X. |
| Numerical companion | none. |

### M4 · Theorem 4 (composition at every n) — K72, K82, K94

| Field | Content |
|---|---|
| Statement | EX-A; Ŝ the ≻-maximum of the scored set on 𝒪. (a) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, D_n = P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). (b) P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), with the matching lower bracket. (c) Ŝ = S₀ if S₀ ∈ 𝒮 and δ₁ < ½. (d) Transfers to R′ > 4 only with the extra search from c₄. |
| Guarantee | A wrong report means no output, a posterior miss, or a never-scored truth; the only inequality non-vacuous at n = 200. |
| Serves | SL Thm S (exceed); objective (3). |
| Status (verbatim) | Thm4-C1: "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)"; T38-(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200: "PROVED (elementary, every n); Π(X) upper bound OPEN"; PC1c5(a) PROVED. Shipped: LS0 yes (scored set enlarged, nested); grid any; pooling n/a. |
| Self-checked only? | N200 author-only (flag; route to a check). |
| Novelty | elementary; 2E₀δ₁ term KNOWN—CITE (Rossell 2022 Prop 1); informal origin García-Donato–Martínez-Beneito 2013; avoid "first finite-n" (Hou–Wang–Atchadé arXiv:2407.20580). |
| Route / key lemma | finite set argument. Difficulty S. |
| Lean core | t21_C1 sorry-free; N200 Lemma 1 certifiable. |
| Dependencies / risk | M12 (δ₁), M5 (D_n) / Π(X) upper bound OPEN (R7 deferred). |
| Fallback + stop rule | (a)–(c) stand; P(U) reported with the allocation, never bounded. No stop. |
| IC3 design | Any X. |
| Numerical companion | study counts (6/2,400; 0/2,394), already filed. |

### M5 · Theorem 5 (reported-HPM consistency with LS0 on LH; Theorem A) — K69, K65, K63, K68, K70 (corollary), K71 (deferred)

| Field | Content |
|---|---|
| Statement | EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, LS0 centre = prescribed start mode (e4), ℓ ≥ max{Φ(S°)−1, 0}, SIZE g_max ≤ B < 2g_min. (a) Theorem A: under TD′_∞ on Lat(S°) the local search from C ∈ Lat(S°) reaches and certifies S₀ in ≤ Φ(C) moves; LS-score: LS0 scores S₀ within max{Φ(S°)−1, 0} moves. (b1-LH) On LH exact Gram (p ≤ n−1, c linked pairs) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical hypothesis. (a-fav) Under (F) with iid draws D_n → 0. (b2-LH) Without LS0, on the STAB-LH subfamily, the same (supplement). |
| Guarantee | The shipped method reports the truth w.p. → 1 − limsup P(U) on an explicit correlated family where the start is masked. |
| Serves | objective (3); SL Thm S; thesis (d). |
| Status (verbatim) | TheoremA: "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score: "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))"; T38-b1-LH: "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))"; Thm-b1: "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; T38-(a): "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; B2E-B2LH: "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))". Shipped: "v3 + LS0" yes, bridge to code N2(c) not done; DP invariant N3 OPEN; grid any frozen. |
| Self-checked only? | (a-fav) XF none; STAB certificate Astra-authored, Claude-verified. |
| Novelty | NEW for this target and method; "corollary of YWJ/ZYVR under their prior" (cite both); Mathews–Schmidler template for (a-fav). |
| Route / key lemma | statement of record exists; new hypotheses only. Difficulty S (assembly); N3 DP invariant M. |
| Lean core | T37Greedy/Lattice sorry-free; LS-score move count short. |
| Dependencies / risk | M6(c), M12 / e4 DP invariant OPEN; study generator N8 uncovered. |
| Fallback + stop rule | (b2-LH) on STAB-LH without LS0 if N3 fails; stop if the merged-LS0 replay contradicts LS-score's centre rule. |
| IC3 design | LH exact Gram, explicit subfamily g = 9, c = 2, ρ = 0.4, ψ = 0.2. |
| Numerical companion | 0/2,394 HPM changes by LS0 (filed). |

### M6 · Theorem 2 (the start: deterministic mass, masking law, dilution, BO discrepancy) — K15, K16, K17, K18, K10

| Field | Content |
|---|---|
| Statement | (a) π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s; exact odds; the bridge never puts less mass on S₀ than min(π₀(S₀), π(S₀)). (b) favourable rate (supplement). (c) Under H2, H3 (LH: no open hypothesis) π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. (d) −log π₀(S₀) = V + C − log A for any data and partition. (e) Under block orthogonality d = d_σ = −ν[log(1−Σ_b u_b) − Σ_b log(1−u_b)] ≥ 0, zero iff at most one active block (OWS-WS3/FD-W1). |
| Guarantee | The merge is exactly computable, carries the truth when blocks see it, loses it polynomially under cancellation and by σ²-dilution at n = 200; even orthogonal blocks leave a σ²-coupling term. |
| Serves | SL Thm 4 (exceed); §5.3 baseline; §5.4 (start approximation). |
| Status (verbatim) | T22(i)(ii)(iv): "PROVED-LOCKED"; T22(iii): "PROVED-LOCKED CONDITIONAL"; T27(i): "PROVED-LOCKED, CONDITIONAL"; Thm3-EXP, Thm4-EXP: "PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2))"; DIL-E: "PROVED (SF: none; XF: VERIFIED (A-REV9))"; OWS-WS3: "PROVED" (SF none, XF none); FD-W1: "PROVED … XF: VERIFIED (A-REV4)". Shipped: start as coded, yes; LS0/grid/pooling n/a. Do not cite DIL-DM(i). |
| Self-checked only? | OWS-WS3 author-only (but FD-W1 covers the identity, XF VERIFIED). |
| Novelty | (c),(d) NEW ("strongest novelty claim", LIT-STAT); (a) block start KNOWN (Papaspiliopoulos–Rossell 2017). |
| Route / key lemma | restatement. Difficulty S. |
| Lean core | (a) product inequality; (d) exact finite identity; (e) scalar identity and Weierstrass product inequality. |
| Dependencies / risk | none / never combine (b) and (c) on one sequence. |
| Fallback + stop rule | none needed (proved). |
| IC3 design | LH exact Gram (c); study tables (d); BO for (e). |
| Numerical companion | SC1 (R0_D, 5·10⁻¹⁴); 480 regenerated fits (filed). |

### M7 · Theorem SEP + Lemma KL — K19, K106, K105

| Field | Content |
|---|---|
| Statement | LH exact Gram, cancellation depth c, Q* = p^c n^{c/2}. (a) iid π₀ discovery switches at Q*. (b) one-shot IS from π₀: 1 + χ²(π‖π₀) ≥ Q*e^{O_P(1)}. (c) KL(π‖π₀) ≥ (1−δ₁) log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size is ≥ ½Q*^{1−δ₁}e^{O_P(1)}. (d) "moving off the start is needed", not "tempering is needed". |
| Guarantee | Keeping or one-shot-correcting the merge costs p^c n^{c/2} draws; the bridge makes the cost logarithmic in A₀ (M9). |
| Serves | §5.4 KL; SL comparison; objective (1). |
| Status (verbatim) | SEP-A: "PROVED (SF: none; XF: VERIFIED (A-REV9))"; SEP-B: same; KL: "PROOF SKETCH (NEW-SYNTH)". Shipped: iid draws (no LS0); grid n/a. |
| Self-checked only? | Lemma KL unreviewed (two lines). |
| Novelty | SEP NEW; exp(KL) scale KNOWN—CITE (Chatterjee–Diaconis 2018). |
| Route / key lemma | log-sum inequality on {S₀, Ω∖S₀}. Difficulty S. |
| Lean core | Lemma KL entirely (finite KL). |
| Dependencies / risk | M6(c) / INP I4 scope: not a universal lower bound. |
| Fallback + stop rule | (a),(b) stand; (c) stays remark if the check fails. |
| IC3 design | LH exact Gram. |
| Numerical companion | THM-SYNTH `check_lemmas.py` (filed). |

### M8 · Theorem SL (separation from split-and-merge) — K97

| Field | Content |
|---|---|
| Statement | LH exact Gram with c linked pairs; SL's uniform equipartition into K_n subsets. (a) P(masked hub isolated) → 1 iff K_n → ∞ (exact hypergeometric). (b) On isolation the hub is an orthogonal null column: Condition 5 fails exactly, β₀ = 0 at every iteration, its subset PIP → 0 under SL's priors, so P(SL output = S₀) ≤ P(E_nᶜ) + o(1). (c) The exact posterior is fine (T03♯). (d) v3.1 on the same family: M1 and M5(b1-LH). |
| Guarantee | In split-and-merge, correlation breaks correctness through a condition violated exactly by a cancelling pair; v3.1 has no such condition. |
| Serves | SL Cor 2/Thm 4; objective (1),(3); ground rule 7. |
| Status (verbatim) | C1new: "COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH"; Thm5-LH: "PROVED (SF: VERIFIED (W3-VEXP); XF: none)". Shipped: (d) via (b1-LH) with LS0. |
| Self-checked only? | PIP → 0 step not verified against SL's prior. |
| Novelty | NEW (no analytic SaM failure published); cite SL Thm 4/Cor 2/eq. (19)/Condition 5, never "Thm 5". |
| Route / key lemma | orthogonal-null Bayes factor O_P(1)(1+nV)^{−1/2}; FDR threshold bounded away from 0 when visible hubs exist. Difficulty M. |
| Lean core | (a) hypergeometric sharing; (b) x′μ = 0 identity; (e) 2×2 inverse. |
| Dependencies / risk | M6(c), M12, M5 / the FDR-rule escalation. |
| Fallback + stop rule | state for a fixed threshold q ∈ (0,1); stop if the orthogonal-null PIP step fails for SL's IG + λ_s prior (then numerical counterexample only). |
| IC3 design | LH exact Gram, g ≥ 2, K ∈ {2, 4, √p}. |
| Numerical companion | LIT-PAR G4 re-run on the LH family (≤ 20 seeds). |

### M9 · Theorem STG (stage laws) with the coverage identity — K26, K25, K30, K28, K29, K27, K31

| Field | Content |
|---|---|
| Statement | Grid rule as coded, ESS 0.90 (hypothesis; same for pilot and grid). (a) The ESS criterion is monotone in both endpoints; bisection finds the frontier; the greedy grid is shortest; T ≤ T_e on success. (b) ρ_full(u,v) = ρ_V(u,v)·a_u a_w/a_v², w = 2v−u, a_t = q_t(V): the restricted certificate transfers to the full bridge up to the mass V misses at u and 2v−u. (c) Favourable: T* = O(1) (STG-F). (d) Masked two-state ideal grid: T* = log₂A₀ + O(1). (e) √c·T*(c) → Λ (cited). As-coded masked T_n: obligation K31. |
| Guarantee | Correlation enters depth only through A₀; the production certificate certifies exactly (b). |
| Serves | objective (2); §4.4 diagnostics; thesis (b). |
| Status (verbatim) | STG-G, STG-L0, STG-L1: "PROVED (SF: none; XF: none)"; T26BUD-G: "PROVED, deterministic (Theorem G)"; STG-M: "PROVED (SF: none; XF: VERIFIED* (A-REV9))"; STG-F: "PROVED (SF: none; XF: none)"; STG-L: "PROVED (SF: none; XF: none)"; (b): D/E proposal, PROVED (by this seat, unchecked); ConjP: "OPEN". Shipped: Theorem G as-coded yes; STG-M ideal grid (no); LS0 n/a. |
| Self-checked only? | STG-G/F/L author-only. |
| Novelty | (a)(i) KNOWN—CITE (Štefankovič–Vempala–Vigoda 2009); (e) KNOWN—CITE (Syed et al. 2024; Gelman–Meng 1998); (b),(c),(d) NEW, elementary. |
| Route / key lemma | F_V(t) = F(t) + log a_t; log-affinity ⇒ ρ = q_u q_w/q_v². Difficulty S (v1); M–L for K31. |
| Lean core | Lemma RS, Theorem G(i)–(ii), (b) entirely. |
| Dependencies / risk | M6 (A₀) / as-coded masked law OPEN. |
| Fallback + stop rule | T ≤ T_e deterministic + (d) on the ideal grid; stop K31 after one HQ cycle without a route. |
| IC3 design | two-state masked family; BO favourable. |
| Numerical companion | SC2 (R0_D): log₂D + 6.7 ± 0.5 (filed); §E script confirms (b)'s identity to 1e-12. |

### M10 · Theorem WS-ε (weight stability under weak, non-zero cross-block correlation) — K102, K11, K10, K25, K103 (see §E)

Card in §E.

### M11 · Theorem CD (thesis) — K96

| Field | Content |
|---|---|
| Statement | Any X, EX-A, EX-S, CAL, R′ declared. (a) never correctness: M1 identities and M2(a); (b) costs depth: island-level depth D_PEL (M13) with T ≤ T_e, T = O(1) favourable or log₂A₀ + O(1) on the ideal grid (M9), and T(ε) ≤ T^{bd}(0.9e^{−4η(ε)}) (M10); (c) costs particles/islands: M2(b) with M ≳ 1/P_𝓒(cross); (d) selection: M5(b1-LH) while split-and-merge loses the hub (M8). |
| Guarantee | Correlation enters T, R, N and delivery, never the target, identities or limits. |
| Serves | objective (2); ground rule 7. |
| Status | assembly: weakest links N1 (PROOF SKETCH), C1 (PROOF SKETCH), K31 (OPEN), E[W²] upper bound (OPEN). Never cite FMP-M3 (XF ERROR). Shipped: island level only. |
| Self-checked only? | inherits parts. |
| Novelty | NEW-COMP (LIT-PAR S-GAP). |
| Route | assembly; exact scope at agenda 6 (fixed data for (a),(c); asymptotic for (b),(d)). Difficulty = parts. |
| Lean core | none beyond parts. |
| Dependencies / risk | all above / slogan overclaims: not monotone in correlation, not conditional on delivery (E). |
| Fallback + stop rule | (a),(c),(d) as theorems; (b) with the ideal-grid law and T ≤ T_e. |
| IC3 design | LH; BO; the ε-family of §E. |
| Numerical companion | none. |

### M12 · Theorem 1 (target consistency) — K93, K04

| Field | Content |
|---|---|
| Statement | R1 (s₀ fixed, p ≤ n^A), G, R, SE, BM-∞ or BM(c > c₀), fixed design: 1 − π(S₀) = O_P(√(log n/n)); HPM, MPM of π equal S₀ w.p. → 1; large signals get PIP → 1 without beta-min; exact BB(1,p) size tail (T02(i♯)). |
| Guarantee | The target is right. |
| Serves | SL Thms 1–3, S; objective (3); input to M2(d), M4, M5. |
| Status (verbatim) | T03♯: "PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))"; T01-T03: "PROVED-LOCKED (wave 3; external review queued)". Algorithm-free. |
| Self-checked only? | no. |
| Novelty | MODEST (Rossell 2022; Moreno–Girón–Casella 2015); T03♯(3) KNOWN—CITE; novelty = cap ≍ n via the exact tail and Prop D's lower bound. |
| Route | restatement + scope sentence (N12). Difficulty S. |
| Lean core | T02(i♯) binomial-coefficient inequality; K04 finite sums. |
| Dependencies / risk | none / disclose n ≳ 2·10⁶. |
| Fallback | none needed. |
| IC3 design | LH; BO. |
| Numerical companion | none. |

### M13 · Proposition D (work, depth, width at the island level) — K87, K88, K89, K90

| Field | Content |
|---|---|
| Statement | Units: score evaluations and sequential step slots. Work W as in LST D1(a) with the local-search term (ℓ+1)(p + k*(p−k*)), k* = min(K, ⌊p/2⌋); island-level depth D_PEL = setup + Σ_e(1+I_e)H_e(T+L+4)m + N_e(T+L+4)m + LS0 + extra search, width R′; W polynomial in n (T32(i), displayed rate GAP); Θ(p) per round and Θ(p²) Gram memory are ceilings; SL §6 in the same units. |
| Guarantee | The parallel claim in a referee's units, island level only, with no comparison to sequential MCMC. |
| Serves | objective (2); SL §6. |
| Status (verbatim) | MA-PropD: "PROVED (counting, given the code's structure)"; T32(i): "PROVED (SF: VERIFIED (W7-SEC); XF: none)"; Cost-T38: "PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))"; calibration share "seat-derived, unchecked" (N15). Shipped: island level yes; "free of N, H, R" struck. |
| Self-checked only? | calibration share unchecked. |
| Novelty | accounting (TCS-standard). |
| Route | counting. Difficulty S. |
| Lean core | low value; the counting identity is certifiable. |
| Dependencies / risk | M9 (T) / METH-AUDIT measured-table placeholder must be checked before citing. |
| Fallback | state W and D_PEL without rates. |
| IC3 design | any. |
| Numerical companion | predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76 (filed). |

### S1 · Target lemmas — K01, K02, K03, K04

| Field | Content |
|---|---|
| Statement | Posterior proper for every admissible (X, y) incl. rank-deficient X_S; Q_S ≥ yᵀy/(n+1); invariance under affine maps, permutation equivariance in law; working posterior = contrast regression with IG(a₀+½, b₀s_y²); b₀ → 0 shifts pairwise log BF by ≤ 2νb₀\|1/Q₁ − 1/Q₂\|; BB(1,p) mass one, cap conditioning once, geometric size tails. |
| Guarantee / serves | the object is well defined; objective (1). |
| Status | D/E proposals, PROVED (by this seat, unchecked); N17 "PROVED"; N12 n = 2 clause "seat-derived, unchecked". Shipped: yes. |
| Self-checked only? | yes. |
| Novelty | MODEST/standard. |
| Route; difficulty | finite algebra; S. |
| Lean core | all. |
| Dependencies / risk | none / duplicates kept (ties break equivariance per seed). |
| Fallback | none needed. |
| IC3 | any X. |

### S2 · Start machinery and blocks — K06, K07, K08, K09, K14, K22

| Field | Content |
|---|---|
| Statement | ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉, table cost ≤ p2^B/B; strict within/between distance gap ⇒ complete linkage never splits a group (PART-ThmA); Z̄₀ exact by size convolution, backward sampler exact (N9); max-plus DP returns the prescribed start mode (invariant N3 OPEN); every block sub-model is scored, so the HPM beats every block-local model; graph has no isolated vertex, ≤ pB edges. |
| Guarantee / serves | exact local step; §5.1; N8. |
| Status | PART-ThmA: "PROVED (SF: none; XF: VERIFIED* (A-REV9))"; PART-pairing: "OPEN"; N9K "PROVED (candidate)"; N3 DP invariant "OPEN"; rest D/E proposals unchecked. Shipped: yes (code audited for N9). |
| Self-checked only? | N9K candidate; K06/K14/K22 unchecked. |
| Novelty | engineering/MODEST. |
| Route; difficulty | counting, telescoping; S; N3: M (greedy index-by-index DP). |
| Lean core | convolution, max-plus recurrence, tie order, counting. |
| Dependencies / risk | none / study packing g = 5 not covered (N8). |
| Fallback | N3: keep the 10⁶ enumeration fast path as the stated rule (0/2,400 truncations). |
| IC3 | strict-gap group designs; study generator excluded. |

### S3 · Decision rules — K60, K61, K62, K95, K101

| Field | Content |
|---|---|
| Statement | HPM = 0–1 Bayes rule, MPM = Hamming action (cited); no size-only prior repairs a same-size swap; {PIP > 1−q} has posterior FDP ≤ q; if every exact PIP is ≥ δ from ½ and estimated PIPs err < δ then reported MPM = exact MPM; π(S₀) = 1/(1+A(S₀)) with A ≤ η < 1 ⇒ HPM = MPM = S₀; exact MPM may exceed K (cap-constrained action). |
| Guarantee / serves | objective (3) bookkeeping; joins statistical and MC error. |
| Status | Prop1-T07: "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4))"; T07 "PROVED-LOCKED (wave 3)"; others D/E proposals unchecked. |
| Self-checked only? | K61/K62/K95/K101 unchecked (elementary). |
| Novelty | FOLKLORE (Barbieri–Berger 2004; Müller–Parmigiani–Rice); ceiling and cap rule ours. |
| Route; difficulty | S. |
| Lean core | T07Bayes.lean sorry-free; K62, K95 finite. |
| Risk / fallback | none / cited lemma only. |
| IC3 | any. |

### S4 · Worker equivalence, stacking, output convention — K63, K83, K84, K85, K86, K77, K78

| Field | Content |
|---|---|
| Statement | Lemma S (top-c merge order-independent); Prop W bitwise (one binary, process workers; 3/3 designs); W-cal by code reading; Cor W-R(b) with the extra search; pooled bounds hold for any R′ declared before stream 10 and fail for adaptive R′; Lemma RO (stop-only guard); CEX-guard; IND-T stream separation. |
| Guarantee / serves | the study's fits are v3.1 fits; "R fixed in advance". |
| Status | MA-LemmaS: "PROVED (candidate)"; MA-PropW: "PROVED (code reading; executed check in REPORT §6)"; MA-Wcal: "PROVED (code reading only; not executed)"; PC1c6: "Cor W-R with caveat PROVED"; LemmaRO: "PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6))"; CEX-guard: "COUNTEREXAMPLE"; IND-T "PROVED … XF: VERIFIED* (A-REV1)". Shipped: GUARD-W audit N2(e) pending; streams 10..9+R′ audit pending. |
| Self-checked only? | Lemma S candidate; W-cal unexecuted. |
| Novelty | engineering; CEX-guard "genuinely non-standard" (LIT-SMC). |
| Route; difficulty | S. |
| Lean core | Lemma S, the finite coupling of Lemma RO. |
| Risk / fallback | W-cal fails → LAW-PRESERVING, wall-clock capped. |
| IC3 | any. |

### S5 · Pooling rules (Prop P) and R_eff — K47, K48, K49, K50, K54, K56, K59 (deferred)

| Field | Content |
|---|---|
| Statement | Fixed N: Ẑ-weighted pool → π(h) a.s. as R′ → ∞; equal-weight → E[PIP̂_1j\|𝓒] (bias of order 1/N); E[Ẑ̄·PIP^eq] − Z·PIP = −(1−1/R)Cov; fixed R: island estimates → π(h) as N → ∞ (cited); R_eff/R → Z²/E[Ẑ²\|𝓒]; one-step RB variance reduction. |
| Guarantee / serves | why Ẑ-weighting is primary; §5.2. |
| Status | MA-PropP: "PROVED (elementary)"; Prop2(c): "PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED (A-REV4))"; ADRAFT-ThmA: "PROVED (SF: VERIFIED* (A-REV4); XF: none)" (Astra-only: cite Del Moral instead); K54/K56 unchecked. Shipped: Ẑ-weighted primary yes. |
| Novelty | KNOWN—CITE (Vergé et al. 2015; WLH 2016; Dai et al. 2022). |
| Route; Lean | finite identities; (iv) and the N = 2 counterexample certifiable. |
| Risk / fallback | E[W²] may be exponential (V11): correctness, not efficiency. |
| IC3 | any. |

### S6 · Evidence variance, masked tails, lower bounds — K39, K40, K41, K38, K37, K44, K53

| Field | Content |
|---|---|
| Statement | Exact variance identity (OPW2 Thm A, as a form of CDG 2011 Thm 1.4); masked lower tail E1/E2 with PC1 claim-4 wording; favourable Ẑ/Z → 1 under (P1) (remark); E[log Ẑ_r] ≤ log Z; island-minimum bound 0.05^{1/R}min_r Ẑ_r; N17 analytic upper bound and U_rest bracket; CDG-type bound Var ≤ (T+1)e^{2D}/N (vacuous at scale; obligation N4(iii)). |
| Status | OPW2-ThmA: "PROVED (SF: none; XF: VERIFIED (A-REV9))"; OPW2-cex COUNTEREXAMPLE (a_t = χ²_t false); MZ-E1E2: "PROVED (E1, E2)" (candidate); FMP-Na: "PROVED (SF: none; XF: GAP (A-REV9))"; T26-ThmA: "PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4))"; N17 "PROVED"; K37/K53 unchecked. Shipped: frozen grid; never the perfect-mixing formula for the kernel. |
| Novelty | E1/E2 NEW; Thm A "same kind as CDG" (present as specialisation); K37 elementary. |
| Lean | identities on a finite chain; K37 given independence. |
| Risk / fallback | two-sided masked Ẑ is v2 (V11). |
| IC3 | any; masked LH for E1/E2. |

### S7 · Equal-weight PIP (A4) — K57, K58 (deferred)

| Field | Content |
|---|---|
| Statement | \|E[PIP̂_rj] − PIP_j\| ≤ TV(delivered population, π); after locking ≤ δ₁ (LH fixed p). Thm R deferred (DELIV-POP OPEN; general LH locking FALSE per A-REV7). |
| Status | MZ-P1P2: "P1 PROVED; P2 PROVED as a composition"; FMP-ThmR: "PROVED (SF: none; XF: none)" CONDITIONAL; FMP-DELIVPOP: "OPEN". Shipped: secondary estimator. |
| Novelty | NEW-COMP. Lean: P1 finite TV. Fallback: P1 only. IC3: LH fixed p. |

### S8 · Doeblin minorisation; exponential-family and KL/TV identities (§5.4) — K103, K104, K108 (+F2)

| Field | Content |
|---|---|
| Statement | Q_φ(S,·) ≥ π_φ(·)/M_φ with M_φ = max π_φ/π₀ ≤ exp{φ(d_max − E_{π₀}d)}, so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − 1/M_φ)^k; (log Z_φ)′ = E d, ″ = Var d; KL(π‖π₀) + KL(π₀‖π) = ∫Var_φ(d)dφ; TV(π, π₀) ≤ tanh(osc(d)/2), KL ≤ osc(d); lower bounds via K105 and masking (TV → 1 on LH). |
| Status | D/E proposals, PROVED (by this seat, unchecked); OWS-WS1: "PROVED" (author-only); K103 textbook (Mengersen–Tweedie 1996). |
| Novelty | KNOWN—CITE; the method constants ours. Lean: finite minorisation, Jensen, identities. |
| Risk / fallback | rate useless under masking (M_φ exponential); favourable regime only. |
| IC3 | BO favourable; ε-family of §E via M_φ ≤ e^{2φη}M_φ^{bd}. |

### S9 · Local search, certificates, numerics — K64, K73, K05, K107, K108, K74

| Field | Content |
|---|---|
| Statement | Strict-improvement search terminates in ≤ ℓ+1 scans of ≤ p + k*(p−k*) models; L1/L2/L3 exact semantics on the returned Ŝ; region certificate R exact on completion, "unresolved" on budget exhaustion; superset bound; rounding bound ≲ c k κ₂(H_S)u(ν+k) and the perturbation lemma; local maxima can be far below the mode. |
| Status | N7: L1 "CORRECT WITH AMENDMENT", L2 "PROVED", R "PROVED with amendments"; OCERT-LemmaM "PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9))"; OCERT-C4 "PROVED … XF: VERIFIED* (A-REV9)"; N16 "OPEN"; T33-errbound COUNTEREXAMPLE; `global_certified` heuristic by decision. Shipped: LS0 yes (card L1 on the returned Ŝ). |
| Novelty | certificates NEW in kind (LIT-SMC G5); numerics standard. Lean: Lemma M, B&B invariant, perturbation lemma. |
| Risk / fallback | fp label stays until SC + VAL-FP. |
| IC3 | any. |

### S10 · Calibration lemmas and obligations — K33, K27, K31

| Field | Content |
|---|---|
| Statement | build_grid terminates; every appended point has ρ_V ≥ 0.9; ≤ ℓ rebuilds per tier; forced pilot step certifies spread ≳ 0.32·T_e; (v−u)²Var_ξ(d) ≤ log(10/9). Obligations: rebuild convergence, P(S₀ ∈ V), P(schedule_limit) → 0, as-coded masked T_n. |
| Status | D/E proposals unchecked; N5(b): "OPEN"; N15 calibration share "seat-derived, not proof-checked". Shipped: as-coded rule yes. |
| Novelty | engineering. Lean: termination counting. Fallback: T ≤ T_e and the POST HOC tabulation; never printed as a limitation (INP §4.B). |

### S11 · Limitations (registry counterexamples restated) — K79, K81, K99, K100, K89

| Field | Content |
|---|---|
| Statement | No diagnostic from the observed record has a universal detection guarantee for never-visited modes (E1c; positive certificates can still detect some failures); flat weights do not prevent genealogical collapse; a posterior barrier defeats (b2), LS0 and T39 (SHARE-PB); duplicates give PIP → 1/d; Θ(p) rounds and Θ(p²) Gram memory are ceilings (I1, I2, I9). |
| Status | MZ-E1E2 "PROVED"; CEX-ESSneutral(A3), SHARE-PB, PropD-T03, CEX-ties(A2): registry COUNTEREXAMPLE rows; I1/I2/I9 by definition. |
| Novelty | consistent with registry; nothing new. Lean: none. Fallback: n/a. IC3: constructions filed. |

### S12 · Fixed p and tiny n — K76, K02

| Field | Content |
|---|---|
| Statement | For fixed p the exact branch is eventually taken (N₀ ≥ n), returning exact Z, PIPs, HPM in exact arithmetic; n ≤ 5 exact for all p; n = 2 proposed extension. |
| Status | N12 "eventual exact dispatch (R2C §4.4) seat-proved, unchecked"; corrects T26-exact-branch-paren (ERROR). Novelty: trivial. Lean: threshold arithmetic. Fallback: remark. |

## §E Proposal §5.3 — the strongest provable statement with genuinely weak, non-zero cross-block correlation

### Card M10 · Theorem WS-ε — K102, K11 (= OWS-WS4), K10 (= OWS-WS3), K25, K103

| Field | Content |
|---|---|
| Statement | Standardised X; blocks C_1..C_J with any within-block correlation; ε := max_{b≠b'} max_{j∈C_b, l∈C_b'} \|r_jl\|; G^{bd} the block-diagonal part of G = XᵀX; κ := min_{\|S\|≤K} λ_min(G^{bd}_S/(n−1)) > 0; ū := max_{\|S\|≤K} n z_Sᵀ(H^{bd}_S)⁻¹z_S/(2b₀ + yᵀy) < 1; δ := (K−1)ε/κ < 1 with δū < (1−δ)(1−ū); η := K log(1/(1−δ)) + ν log(1/(1 − δū/((1−δ)(1−ū)))), ν = a₀ + n/2. Let d^{bd} be the discrepancy computed from G^{bd} with the same z, y (so d^{bd} = d_σ ≥ 0 by OWS-WS3). Then, deterministically: (i) sup_{\|S\|≤K} \|d(S) − d^{bd}(S)\| ≤ η; (ii) for every V ⊆ 𝕊_K and 0 ≤ u < v ≤ 1: e^{−4vη}(1+χ²_V^{bd}(u,v)) ≤ 1+χ²_V(u,v) ≤ e^{4vη}(1+χ²_V^{bd}(u,v)); (iii) greedy ESS-0.9 stage counts at fixed V: T^{bd}(0.9e^{4η}) ≤ T(0.9) ≤ T^{bd}(0.9e^{−4η}) when 0.9e^{4η} < 1; (iv) M_φ ≤ e^{2φη}M_φ^{bd}, so the round's TV contraction rate is ≥ e^{−2η}/M_φ^{bd}; (v) 1+χ²(π‖π₀) ≤ e^{4η}(1+χ²^{bd}(π‖π₀)): every H-ORTH weight-stability statement (OWS W(a–f), WS6(a–c), WS7) transfers to ε-weak designs with constants multiplied by e^{4η}, and the H-ORTH negative WS6(d) persists. |
| Guarantee | Weak cross-block correlation perturbs the discrepancy, every stage's weight variance, the depth and the mixing constant by an explicit factor controlled by ε through η; it never changes the target or any identity. Weights are bounded per stage by the ESS rule up to the coverage factor (K25); what ε costs is stages. |
| Serves | §5.3 (binding); thesis (b); objective (2). |
| Status (verbatim) | OWS-WS3: "PROVED"; FD-W1: "PROVED … XF: VERIFIED (A-REV4)"; OWS-WS4: "PROVED" (SF none; XF none: "Cross-block dependence ε perturbs SE, t_S and d by explicit factors ε/(1−ε)"); OWS-WS1: "PROVED"; AREV9-OWSTAB W(a–f): "VERIFIED under H-ORTH exactly as stated"; (i)–(v) as stated: PROVED (by this seat, unchecked). About v3.1 as shipped: block tables and d as coded, yes; (iii) is about the greedy rule at fixed V (as-coded rule, rebuild loop outside); LS0 n/a; pooling n/a. |
| Self-checked only? | yes (this seat); OWS rows author-only. |
| Novelty | NEW-COMP: the perturbation (WS4-type) is known in kind; the four-normaliser continuity (ii), the stage-count sandwich (iii) and the H-ORTH transfer (v) are ours; the identity behind (ii) is OWS-WS1/K25. No published analogue for a block-product start (THM-INV §4b: none found). |
| Route / key lemma | (i): E_S = G_S − G^{bd}_S has Gershgorin norm ≤ (n−1)(K−1)ε; relative perturbation of H and G+I ≤ δ; Weyl for log-dets; resolvent identity gives \|Δ − Δ^{bd}\| ≤ (δ/(1−δ))Δ^{bd}; log(a−Δ) step. (ii): Z_φ ∈ e^{±φη}Z_φ^{bd} and 1+χ² = Z_{2v−u}Z_u/Z_v² (K25), exponent (2v−u)+u+2v = 4v. (iii): monotone feasibility + greedy optimality (STG-G). (iv),(v): same bound. Difficulty S for (i)–(v); M for a sharp constant. |
| Lean core | (ii)–(v) entirely (finite sums, exp bounds, monotone greedy); (i) Weyl/Gershgorin partly in Mathlib. |
| Dependencies / risk | K25, STG-G, OWS-WS3/WS4 / the constant is loose by about an order of magnitude on the exhibited family (companion), and η = Θ(nε): "weak" means nε = O(1) in order, which the companion suggests is the true scale of sup\|d − d^{bd}\| (empirical slope 0.05–0.5 per unit nε). The one-shot form of §5.3 is not implied: OWS-WS6(d) (ORTH, PROVED author-only) makes χ²(π‖π₀) → ∞ by noise chasing and WS7 by masking, independently of ε. |
| Fallback + stop rule | Ship (ii)–(v) with η replaced by the exactly computable run-card number η̂_V := max_{S∈V}\|d(S) − d^{bd}(S)\| (finite computation; V-restricted), plus H-ORTH W(a–f) as the ε = 0 case. Stop rule: if (i)'s explicit η cannot be checked in one HQ cycle, ship the η̂_V form; if HQ rules that §5.3 requires the one-shot statement in regimes where WS6(d)/WS7 refute it, escalate (binding goal; §I Q1). |
| IC3 design | Exact-Gram family G/(n−1) = blockdiag(E_ρ(g)) + ε·(off-block ones), p ≤ n−1, realisable for any ρ ∈ [0,1) and 0 < ε < (1+(g−1)ρ)/g (PD by the eigen-decomposition); κ = 1−ρ; genuinely correlated inside blocks (ρ up to 0.9), weak but non-zero across. Checked at n = 40, p = 8, g = 4, ρ = 0.6, ε ∈ {0.02, 0.05, 0.1, 0.2}. |
| Numerical companion | Script `ws_eps.py` + `chi_cont.py` (numpy, < 2 s, 12 runs = 3 seeds × 4 ε; exact d over all 163 models, method score g = n, IG(0.01, 0.01), BB(1,p)). Results: (i) holds 12/12 (sup\|d − d^{bd}\| = 0.04–4.1 vs η = 2.9–30 or ∞ at ε ≥ 0.1); (ii) holds 12/12 with margin (max over 240 (u,v) pairs of \|log(1+χ²) − log(1+χ²^{bd})\| − 4v·sup ≤ −0.007); ESS identity exact to 1e-12; (iii) T = 1–3 on both sides (favourable, one signal block). Control at ε = 0 with signal in two blocks: d(S₀) grows 0.19 → 7.9 over n = 20 → 160 while log(1+χ²(π‖π₀)) stays in [0.09, 0.73]: the σ²-coupling shifts d uniformly on the π₀-mass and does not by itself destabilise the one-shot weights (consistent with WS6(a–c)). |

**Why this and not more.** The registrar's gap ("no bound on E[(Ẑ_r/Z)²] for weak non-zero correlation on the as-coded grid") is real and is not closed by ε-weakness: E[W²] on the implemented kernel is N4(iii) OPEN for every design (OPW2-cex kills the exact-refresh shortcut), and the CDG-type bound (K53) is exponential in osc(d), which is Θ(n) already at ε = 0 when two blocks carry signal (companion: d(S₀) ≈ 0.05n). What ε-weakness does control is everything upstream of the kernel: d, per-stage χ², the schedule and the Doeblin constant. A referee accepts (i)–(v) because each is a finite inequality with explicit constants on an exhibited family; the per-stage weight variance is then bounded by the rule (1/9 on V, (10/9)/((1−η_u)(1−η_{2v−u})) − 1 on the full space by K25), so "weights remain bounded" is delivered in the bridge form. Against the binding goal, nothing is dropped: the one-shot form is refuted by registry results unrelated to correlation (WS6(d), WS7), and I ask HQ (§I Q1) to confirm that the bridge form is the goal's meaning for this method.

## §F Proposal §5.4 — approximation error

The method corrects exactly at φ = 1 (M1), so "approximation error" has two meanings here: (A) the error of the start π₀ (the merge) relative to π, which is what a split-and-merge method would ship; (B) the Monte Carlo error of the delivered estimate relative to π. Both are stated; (B) in the masked regime is an obligation, not a limitation.

| Metric | Card / K-IDs | Statement | Status | Provable? Ships against §5.4 |
|---|---|---|---|---|
| PIP error (B) | M2 (K51, K52), M3 (K43), S7 (K57) | islandwise ≤ 2δ₁ in Ẑ-weighted mean; finite R: PC1 claim-3 bound; top-store \|PIP^𝒯 − PIP\| ≤ δ₁ when S₀ ∈ 𝒯; equal-weight ≤ TV(delivered population) | PC1c3 PROVED (given N1); MZ-P3 PROVED (candidate); MZ-P1 PROVED | yes; ships |
| Joint-PIP error (B) | M2 (K51(c), K46) | h_A = 1{A ⊆ S}, plain averages, declared pairs, same bounds | N1 PROOF SKETCH (binding §13.1) | yes conditional on N1; ships; escalation if N1 fails |
| TV error of the start (A) | S8 (K104, K108, K105, K17): card F2 | TV(π, π₀) ≤ tanh(osc(d)/2) with osc(d) ≤ osc(d^{bd}) + 2η under WS-ε; TV(π, π₀) ≥ (1−δ₁) − p^{−c}n^{−c/2}e^{O_P(1)} on masked LH (→ 1); KL(π‖π₀) ≤ osc(d); KL ≥ (1−δ₁)log(1/π₀(S₀)) − log 2 | K108, K104 D/E proposals PROVED (by this seat, unchecked); KL: "PROOF SKETCH"; T27(i) PROVED-LOCKED CONDITIONAL | yes; ships (it is the error a merge-only method would commit) |
| KL error (A) | M7 (K105), S8 (K104) | as above; J = ∫Var_φ(d)dφ identity | OWS-WS1 PROVED (author-only) | yes; ships |
| TV/KL error of the delivered population (B), favourable regime | S8 (K103) | ‖law(particle after L rounds) − π‖_TV ≤ (1 − 1/M_1)^L with M_1 ≤ exp(d_max − E_{π₀}d), M_1 ≤ e^{2η}M_1^{bd} under WS-ε | D/E proposal PROVED (by this seat, unchecked); textbook | yes but useful only when M_1 = O(1) (favourable BO/ε-weak with the start seeing the truth); ships as a remark |
| TV/KL error of the final pooled estimate (B), masked regime: card F3 | obligation N4(iii)/N10 (K53, K31) | would need E[W²\|𝓒] (V11) or a mixing input (N10), both OPEN; lower bound M ≳ 1/P_𝓒(cross) PROOF SKETCH | "OPEN/CONJECTURE (V11)"; N10 "NONE / OPEN" | not provable now; carried as a theorem obligation with fallback = the fixed-data N → ∞ and R′ → ∞ limits (M1, S5) plus the finite-R PIP/general-h bounds (M2(b)); never printed as a limitation; §I Q2 asks whether HQ treats it as binding |
| Credible-interval coverage error: card F1 | M2 corollary (K51, K52, K62) | For h_I(S) = P(β_j ∈ I\|S, X, y) (exact conditional under the ridge/IG model; = 1{0 ∈ I} off S), \|μ̂(h_I) − π(β_j ∈ I)\| obeys M2(b); sup_I of this ≤ TV(estimated model-space law, π) by data processing, so the coverage error of any credible interval computed from the estimate is bounded by the model-space TV error (deterministic) | PROVED (by this seat, unchecked), conditional on N1 | yes; ships. Frequentist coverage of π's credible intervals is not a target (INP row 10 "rejected"): reason, not a gap |

## §G Fidelity of inherited results relied on in §D

| Registry ID | About v3.1 as shipped? LS0 / coded grid / Ẑ-weighted pooling (path:line) | The gap | Gap lemma to prove |
|---|---|---|---|
| T12, T31(i) (K35, K36) | n/a / any frozen grid: yes (IDX 68–69) / islandwise: n/a | output-event Markov wording (A-REV4 GAP on Prop 2) | N6(a): P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜) (PC1 claim 2 PROVED; GUARD-W audit N2(e)) |
| Prop2(a,b,d,e) (K46) | n/a / yes / islandwise (IDX 60; REG 260) | XF GAP (A-REV4) on output wording | same as above |
| N9K (K20, K21, K08) | n/a / n/a / n/a; production step functions at 39db138 (N9 REPORT §1) | independent review of PROOF.md Claims R, S; (H-U) and exact arithmetic as hypotheses | Lemma: self-adjointness of a reversal-invariant random order (Claim R), reviewed cross-family |
| IND-T, Lemma-STREAM (K86) | n/a / n/a / streams 10..9+R′ unknown (INP N14(c)) | code audit for R′ > 4 | IND-T restated over streams 10..9+R′ (one-line re-proof + audit) |
| MA-PropP (K48, K49, K85) | n/a / any / Ẑ-weighted: yes (IDX 70; INP M4) | Prop P(ii) author-only (METH-AUDIT) | none mathematical; route to a check |
| PC1c3 (K52) | n/a / any / Ẑ-weighted: yes (IDX 114) | premise E[W_r ĥ_r] = π(h) for general h | N1 (PROOF SKETCH) |
| A1new, FMP-M1 (K51) | n/a / any frozen (IDX 155, 107) / Ẑ-weighted yes | general-h version unchecked; RB terms restricted to marginal PIPs | Lemma: M1's mechanism with h in place of 1{j ∈ S}, c_h = 0 |
| MZ-P3, PC1c5, N13 (K43, K45) | LS0: yes (card L3, INP M10) / any / n/a | deterministic; eviction wording | none |
| Thm4-C1, T38-(0), N200 (K72) | LS0: yes (scored set nested, INP M2) / any / n/a | N200 author-only; R′ transfer only with the extra search (PC1 :197–201) | Lemma: D_n(R′) ≤ D_n(4) under the extra search from c₄ |
| T38-b1-LH, Thm-b1, LS-score, TheoremA (K69, K65) | LS0: "v3 + LS0" yes (IDX 438, 549, 508); bridge to code N2(c) not done / any frozen / n/a | e4 tie-DP invariant OPEN (N3); ℓ ≥ Φ(S°)−1 (N11) | N3: the greedy index-by-index max-plus DP returns the prescribed maximiser |
| B2E-B2LH, STAB-cert (K70) | LS0: no (v3 as run) (IDX 439, 568) / any frozen / n/a | STAB certificate Astra-authored, Claude-verified; A-REV7 pending (index C20) | none; cross-family review |
| T38-(a) (K68) | LS0: no (iid draws) (IDX 548) / n/a / n/a | ORTH joint family PROOF SKETCH (C9) | Prop C: ORTH satisfies Theorem B's hypotheses |
| T22, T27(i), Thm3/4-EXP, DIL-E (K15–K18) | start as coded: yes (IDX 337–339, 321–322, 328) / n/a / n/a | none for paper 1 | — |
| OWS-WS3/FD-W1, OWS-WS4, OWS-WS1 (K10, K11, K25) | tables as coded: yes (REG 520–521, 518) / WS1 any grid / n/a | author-only PROVED (no SF/XF) | route to check wave 1 together with WS-ε(i)–(v) |
| AREV9-OWSTAB W(a–f), W′ (K102 baseline) | n/a / W′ "ideal full-space grid; production-grid transfer remains GAP" (A-REV9 REVIEW.md L135) / n/a | H-ORTH only | WS-ε(v) transfer; production-grid transfer via (iii) at fixed V |
| SEP-A, SEP-B (K19, K106) | LS0: no (iid draws) (IDX 352–354) / n/a / n/a | scope per INP I4 | — |
| STG-G/L0/L1, T26BUD-G (K26) | n/a / as-coded rule at fixed V: yes (IDX 255–257, 268) / n/a | author-only | — |
| STG-M, STG-L, STG-F (K30, K28, K29) | n/a / ideal exact-frontier two-state grid: no (IDX 261, 258–259) / n/a | as-coded masked T_n (Conjecture P OPEN) | K31: realised T_n through a masked crossing on the coded grid |
| T03♯, T01–T03 (K93) | algorithm-free (IDX 151, 469) | onset n ≳ 2·10⁶ (disclose) | — |
| MA-PropD, T32(i) (K87, K88) | LS0 term added (INP N15) / n/a / n/a | displayed rate GAP (A-REV6); calibration share seat-derived | Lemma: calibration trajectory share (1+4I_e)H_e/(4N_e) |
| C1new, Thm5-LH (K97) | (d) via (b1-LH): LS0 yes / n/a / n/a | PIP → 0 step under SL's prior | Lemma: orthogonal-null subset PIP → 0 under IG + Gaussian + λ_s prior |
| LemmaRO, CEX-guard (K77, K78) | GUARD-W for worker/merge/LS0 code: unknown (INP N2(e)) / n/a / n/a | code audit | none mathematical |
| OCERT-C4, OCERT-LemmaM (K73) | LS0: n/a (card after run) / n/a / n/a | fp: SC + VAL-FP (N16 OPEN) | validated arithmetic contract |
| MA-LemmaS, MA-PropW, PC1c6 (K63, K83, K84) | LS0: 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) yes (INP M2) / n/a / n/a | Prop W code-audit fact; W-cal unexecuted | none mathematical |

## §H My list (ranked)

| Rank | K-ID(s) | Name | Main / supplement | One-line reason |
|---|---|---|---|---|
| 1 | K20, K21, K08, K35, K46, K32, K86 | Theorem V (validity as shipped; N9 + N1) | main | foundation; §5.1/§5.2; everything depends on it |
| 2 | K51, K52, K48 (+F1) | Theorem H (bounded functionals, joint inclusion, finite R) | main | binding §13.1; the only regime-free accuracy theorem |
| 3 | K69, K65, K63, K68 | Theorem 5 + Theorem A (LS0 route on LH) | main | the output theorem no SMC-BVS paper has; shipped method |
| 4 | K72 | Theorem 4 (composition at every n) | main | the only inequality non-vacuous at n = 200 |
| 5 | K42, K43, K45, K36, K78 | Theorem Z𝒯 + certificate card | main | two-sided masked evidence; §4.4 positive certificates |
| 6 | K102, K11, K10, K25, K103 | Theorem WS-ε (§5.3) | main | binding goal with an exhibited correlated family |
| 7 | K15, K17, K18, K10 | Theorem 2 (start law) | main | strongest novelty claim; input A₀ and ε = 0 baseline |
| 8 | K26, K25, K30, K28, K29 | Theorem STG (stage laws, coverage identity) | main | depth named; what ESS 0.9 certifies |
| 9 | K97 | Theorem SL (split-and-merge separation) | main | ground rule 7; SL Cor 2 |
| 10 | K19, K106, K105 | Theorem SEP + Lemma KL | main | why one-shot fails; §5.4 KL |
| 11 | K96 | Theorem CD (thesis) | main | assembled; scope at agenda 6 |
| 12 | K93, K04 | Theorem 1 (target consistency) | main (short) | needed input; MODEST, disclosed |
| 13 | K87, K88, K89, K90 | Proposition D (work/depth island level) | main (proposition) | objective (2) in referee's units |
| 14 | K47–K50, K54, K56 | Prop P pooling rules, R_eff | supplement | KNOWN—CITE plus our negatives |
| 15 | K39, K40, K41, K38, K37, K44 | Evidence variance, masked tails, bounds | supplement | identities and the honest masked wording |
| 16 | K63, K83–K86, K77, K78 | Worker equivalence, stacking, output convention | supplement | the study's fits are v3.1 fits |
| 17 | K60–K62, K95, K101 | Decision rules | supplement | cited lemma + ceiling + margin transfer |
| 18 | K64, K73, K05, K107, K108, K74 | Local search, certificates, numerics | supplement | card semantics; fp contract |
| 19 | K103, K104 (+F2) | Doeblin, exponential-family, KL/TV of the start | supplement | §5.4 TV/KL |
| 20 | K01–K04, K06, K07, K09, K14, K22, K57, K33, K27, K76 | Target, start machinery, A4-P1, calibration, fixed p | supplement | lemmas with Lean cores |

Deferred with reason (future work): K24 (N10), K23, K59 (v2), K58 (DELIV-POP OPEN), K71 (XF GAP), K94 (OPEN; E's T34 route), K75, K92, K99 quantitative, K13. Dropped: K66, K67, K98, K12, K34, K80, K91.

## §I Questions for HQ

1. **§5.3 scope (binding goal).** The proposal's "variance of importance weights remains bounded under weak cross-block dependence" is delivered in the bridge form (per-stage χ² bounded by the rule up to the coverage factor; depth and constants continuous in ε with explicit η). Its one-shot form is refuted for this method by registry results independent of correlation (OWS-WS6(d) noise chasing, OWS-WS7 masking; both author-only PROVED, so a check is needed before calling this an inherent limitation). Please confirm that the bridge form is the goal's meaning; if HQ holds that the one-shot form is required, this is a binding-goal escalation to Felipe, not a withdrawal.
2. **§5.4 TV/KL of the final estimate in the masked regime.** Delivered: PIP, joint-PIP, credible-interval transfer, TV/KL of the start, TV of the delivered population in the favourable regime. Not provable now: TV/KL of the final pooled estimate under masking (needs V11 or N10, both OPEN). I carry it as a theorem obligation with a fallback. Does HQ treat this item as binding (then escalation) or as a listed obligation?
3. **N9 review.** N9K is a closure gate PROVED (candidate) by its author with a numerical check; Theorem V (rank 1) rests on it. May the cross-family proof checker review N9 PROOF.md §1–3 inside check wave 1, outside the seat-claim queue?