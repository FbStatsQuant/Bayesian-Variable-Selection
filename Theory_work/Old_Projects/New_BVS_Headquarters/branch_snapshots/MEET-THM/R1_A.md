# Round 1, Seat A (Fable 5.1, Claude Personal, high)

Verbatim final message, extracted by the chair from `~/.claude-personal/projects/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-THM/5401076b-a869-4c49-9fbb-aec892f31394.jsonl` (completed 2026-11-04 02:26 UTC). Everything in it is the seat's position; its own arguments are unchecked.

---

The numerical check passed on all 15 cases (ε ∈ {0, 0.002, 0.01}, 5 seeds each): the WS4 discrepancy bound and the transfer bound hold, and the actual ratio is far inside the bound (0.85–1.01 against bounds up to 107). I now have everything needed and am writing the Round 1 answer.

# MEET-THM · Round 1 · Seat A

Conventions: K-IDs from R0_DIFF; registry statuses verbatim; my own arguments are at most "PROVED (by this seat, unchecked)". "C-n" / "S-n" name my theorem cards (§D). IDX n = `REGISTRY_INDEX.md` line n; REG n = `REGISTRY_v2.md` line n; INP n = `THEOREM_REVISION_INPUTS.md` line n; OWS = `origin/theory/O-WSTAB:theory_campaign/O-WSTAB/PROOF.md`.

## §A Coverage sweep (item 1)

### A1 Proposal goals → K-IDs

| Goal | Delivered by | Note |
|---|---|---|
| §5.1 exactness under MH correction | K20, K21, K08 (N9: PROVED (candidate), code-checked) → card C2 | Cited lemma (detailed balance) + N9 certificate about v3.1's step functions. Binding goal met. |
| §5.2 SMC consistency | K47 (cited: Del Moral et al. 2006), K35, K48, K52 → C2, C4 | Fixed-data N → ∞ and R → ∞ consistency; finite-R bound (PC1 claim 3). Met. |
| §5.3 weight stability under weak cross-block dependence | K102 + K11 + K10 (+ K25 first stage, K27, K104, WS7) → C9, §E | Relative form (ε-bridge vs BO-equivalent bridge) PROVED (OWS, no review). Literal one-shot form refuted for the shipped start (WS6(d), author-only). Met in the method's own form; HQ question §I-1. |
| §5.4 PIP error | K51, K52, K46 → C5 | Islandwise 2δ₁ bound; pooled tail bound. |
| §5.4 joint-PIP error | K51 with h = 1{A ⊆ S}, plain averages (c_h = 0); crux N1 → C5 | Declared pairs only (M9); new runs only. |
| §5.4 TV error | New clause in C7: TV(π_𝒯, π) = 1 − Z_𝒯/Z exactly, ≤ δ₁ when S₀ ∈ 𝒯 (K43); Monte Carlo TV: K47/K48 fixed-data limits (cited); K57 (P1) bias ≤ TV of delivered law; K103 minorisation rate (vacuous under masking) | §F. |
| §5.4 KL error | C7: KL(π_𝒯‖π) = log(Z/Z_𝒯) ≤ −log(1−δ₁); merge error KL(π‖π₀) lower bound K105, J identity K104 | §F. |
| §5.4 credible-interval coverage | C5 with h_c(S) = P(β_j ≤ c \| S, X, y) for a finite declared list of c (M9 allows h measurable in (X, y, 𝓒)): Monte Carlo error of posterior intervals | Frequentist coverage of the exact posterior's intervals: not delivered; target-theory property outside objectives (1)–(3); §I-2. |
| §13.1 E_π[h] → truth | K51(d) composed with K93 (T03♯) → C5; N1 crux | R_n ≥ E[W²\|𝓒_n]-type hypothesis stays explicit (N4(iii) OPEN). |
| §4.4 / §8.2 diagnostics | K25 (what restricted ESS certifies: coverage factor a_u a_w/a_v²) → C11; K42, K73 certificates → C3, C16; K79 negative → S3 | Positive flag power: nothing provable (INP row 13, labelled heuristics); reason: flags are computed from the record, E1c (PROVED) shows record-blindness to unqueried mass. |

### A2 Song–Liang (2015) → K-IDs

| SL result | Our item | Verdict |
|---|---|---|
| Thm 1 (Hellinger consistency, bounded predictors) | K93 (T03♯: selection consistency, p ≤ n^A) → C15 | Selection: matched. Hellinger/coefficient contraction: not delivered, reason: a target-posterior rate outside objectives (1)–(3); future work (INV row 1). |
| Thm 2 (Condition 1 tails) | K93 | Our designs are fixed (G, R, SE); the random-predictor tail condition does not arise. |
| Thm 3 (sure screening, PIP → 1) | K93 (large signals PIP → 1 without beta-min) → C15; estimated PIPs: K51 → C5 | Matched for π; exceeded for the reported PIP via C5. |
| Thm 4, Cor 2, eq. (19) (misspecified subset posterior) | K10, K17, K18 (block tables are misspecified subset posteriors; d = d_σ + d_X; dilution; masking) → C8; K97 → C14 | Exceeded: we quantify the subset posterior's failure and correct it exactly. |
| Cor 1 (P_n < e^{Cn^α}, rates) | none | Not delivered: N12 OPEN ("our prior admits it: OPEN, not impossible"); cause is the prior and proof technique, not the sampler (INP 217–218). Future work. |
| Thm S (MAP consistency) | K93 (HPM of π) → C15; K68–K72 (reported HPM) → C17, C18 | Exceeded: SL prove nothing about the merged output. |
| §6 complexity (K_n = √P_n, O(P^{(1+α)/2}) + O(nP)) | K87, K88, K90 → C12 | Same-units comparison; no speed claim. |
| UQ of merged output (SL: "approximate") | K35, K46, K48 → C2, C4 | Exceeded at fixed data; n-indexed accuracy only favourable/LH (C5(d) with hypothesis). |

### A3 THM-INV §1 empty or partial cells

| Row × cell | K-ID / verdict | Reason |
|---|---|---|
| 1 × NONE: finite-n upper bound on Π(X) | K94 → future work | OPEN; no route to explicit constants; vacuous at n = 200 where the exact posterior misses S₀ often (I6). |
| 1 × NONE: contraction rates; growing s₀ | nothing provable in paper 1 | Target-theory; N12 OPEN for growing s₀; not an objective. |
| 1 × C (empty) | K01, K44 → C1, C6 | Propriety for every admissible (X, y); analytic Z bound (N17 PROVED). |
| 2 × NONE | K76 → S1 | Eventual exact dispatch at fixed p (N12, seat-proved); n = 2 extension PROOF SKETCH. |
| 3 × V (empty) | K07, K06 → C18 lemma, C12 | Strict-gap cluster recovery; block count. |
| 3 × NONE: study packing (2g ≤ B) | nothing now | PART-CE2 (COUNTEREXAMPLE, XF ERROR on the unequal header, equal-size example survives): blocks ≠ groups surely; N8 OPEN, Prop Q PROOF SKETCH. Disclose. |
| 3 × NONE: adaptive/overlapping partitions | out of scope | WORKHORSE (M1). |
| 4 × V (no registry row) | K08 → C2 | N9 PROVED (candidate), code-checked (N9-KERNEL rows 7–8). |
| 4 × NONE: start quality on random designs with packing | nothing now | N8/N18; depends on the packing law (OPEN). |
| 5 × NONE: realised masked T_n | K31 → C11 as OPEN (Conjecture P) with fallback T ≤ T_e | No route beyond termination (Seats D, E agree). |
| 5 × NONE: depth vs correlation | K30 (ideal grid), K27 (any grid, range/sd), C9 (ε cost) | As-coded masked law OPEN. |
| 6 × V | K20, K21 → C2 | N9. |
| 6 × NONE: mixing (V10) | nothing provable in paper 1; K23 → S6 lemma | N10 blocked as stated; K24 deferred. |
| 7 × NONE: rebuild convergence, P(schedule_limit), V ∋ pair | nothing provable; K33 (termination, cost) and K25 (coverage identity) → C11 | Adaptive loop on a flat posterior; N5(b) OPEN, not inherent (INP §4.B). |
| 8 × NONE: work–depth | K87, K88, K89 → C12 | Counting; island level. |
| 8 × NONE: R vs N | K59 → defer (v2) | PROOF SKETCH, no checked route. |
| 8 × NONE: island variance vs correlation | K53 (crude e^{2D}) remark in C6; C9 (relative ε cost) | Useful constants need T20-type stability (hard). |
| 8 × NONE: speed-up vs MCMC | nothing provable | Empirical (INP row 8); K91 dropped. |
| 9 × NONE: two-sided masked Ẑ | OPEN (V11) | N4(iii) CONJECTURE; v2. |
| 9 × "upper bound impossible" | K44 → C6 | Corrected by N17. |
| 9 × fp | K108 → S4; N16 OPEN | Deterministic perturbation lemma only. |
| 10 × NONE: joint inclusion | K51, K46 (N1) → C5 | Binding §13.1. |
| 10 × NONE: equal-weight accuracy at fixed R | K49, K57 → C4, S2 | Bias identity; P1. |
| 10 × credible sets | C7 (TV/KL of π_𝒯), C5 (quantile functionals) | §F; frequentist coverage not delivered. |
| 11 × NONE: P(U) → 0 | K82 → limitation (OPEN) | No route (IC2); only I9(e) definitional. |
| 11 × NONE: finite-n Gibbs discovery | nothing | No route. |
| 11 × NONE: study generator | nothing now | As row 3. |
| 12 × NONE: meaning of local_certified | K64, K73 → C16 | Card L1/R deterministic semantics. |
| 12 × LS0 absent | N2(c) engineering | Merged-LS0 replay gates "shipped". |
| 13 × NONE: positive flag power | nothing provable | K80 dropped; E1c (K79) is the limit. |
| 14 × NONE: P(resource_limit) etc. | K82 | As row 11. |
| 14 × NONE: fp theorem | K108 lemma; N16 OPEN | Validated arithmetic is engineering. |

## §B The draft list, item by item (item 2)

| Entry | K-ID | Action | Corrected statement / reason | IC |
|---|---|---|---|---|
| V1 | K08, K20, K21, K32, K35, K36, K46, K47, K48, K50 | split | (a1) Ẑ_r, RB-PIP identities: cited lemma (Del Moral 2006; WLH 2016) inside Prop C2 whose content is the hypothesis list (N9, frozen 𝓒, streams, R′ declared) and Lemma N1 (general h); (b) → C3 output-event form; (c), (d) → C4. | IC4 demotes standard parts; IC1 |
| V2 | K63, K83, K84, K86 | demote to supplement (S1) | Engineering/code-audit facts; Lemma S certifiable; executed 3/3 designs (B1 conflict: use CONC's 3/3). | IC5 |
| V3 | K48, K49, K50, K51, K85 | keep → C4 | "secondary" → "primary"; (iii) folded into C5; add PC1 claim 3; R′ declared rule with CEX-guard mechanism. | IC1 |
| V4 | K77, K78 | keep → C3 | Lemma RO as recorded; GUARD-W = hypothesis (N2(e), code audit). | IC1 |
| A1 | K46, K48, K51 | keep → C5 | Restate around M9: plain averages for joint h (c_h = 0), RB for marginal PIPs; h ∈ 𝓗 measurable in (X, y, 𝓒); (d) with R_n as hypothesis; crux N1 to check wave 1. Binding §13.1. | IC2 (N1), IC5 |
| A2 | K35, K36, K38, K39, K40, K41, K42, K53, K79 | keep → C6 | Mandatory PC1 claim 4 wording (never "only downward"); (v) as remark; add N17 upper bound and K37 bounds; K53 crude bound as remark; K79 → S3. | IC1 |
| A3 | K42, K43 | keep → C7 | Add retention lemma (K45, δ₁ < ½ sharp), MPM margin transfer (K62), odds certificate (K95), TV/KL identities (§F). | IC1 |
| A4 | K57, K58 | split | P1 → S2 (supplement, secondary estimator). Thm R → defer (DELIV-POP OPEN, REP vacuous at n = 200). | IC2 |
| D1 | K06, K64, K87, K88, K89, K90 | keep → C12 | Island-level depth only; (c) a v3.2 remark iff C6; scan count p + k*(p − k*), k* = min(K, ⌊p/2⌋); calibration share "seat-derived, unchecked"; K90 accounting, no speed claim. | IC1 (fidelity) |
| D2 | K26, K28, K29, K30, K31 | keep → C11 | (a) as coded with ESS 0.90 hypothesis; (b) STG-F (STG-cexW2 forbids "O(1)" in masked); (c) ideal grid; (d) cited; add K25 coverage identity and K27 interval inequality; Conjecture P OPEN with fallback T ≤ T_e. | IC1 |
| D3 | K96 | keep → C13 | E's scope wording: correlation changes overlap, depth, particles/islands; not the target or the unnormalised identities; not monotone in a coefficient; not conditional on delivery. Exact scope: agenda 6 (R2). | IC1 |
| D4 | K39, K59 | defer (v2) | PROOF SKETCH; v1 states the proved halves in C4. | IC2 |
| S1 | K15, K16, K17, K18 | keep → C8 | Add K10 (d = d_σ + d_X, d_σ ≥ 0; FD-W1 XF VERIFIED for known σ²). (b) supplement. Never combine (b) and (c). Do not cite DIL-DM(i). | IC1 |
| S2 | K19, K105, K106 | keep → C10 | Lemma KL to check wave 1 (two lines). "Moving off the start is needed", not "tempering". | IC1 |
| S3 | K98 | drop | SHARE-M(b), FD-NM ERROR; ADRAFT-PropM COUNTEREXAMPLE. Replacement: C10 + Prop M-LH remark. | IC1/IC2 |
| S4 | K102 | keep, strengthened → C9 | ε-perturbation transfer relative to the BO-equivalent bridge (WS4(e)), first-stage exact variance, depth transfer; IC3 family exhibited (§E). | IC3 |
| C1 | K97 | keep → C14 | (b)'s PIP → 0 under SL's prior is the one proof obligation; re-run the numerical counterexample on LH with g ≥ 2, K ∈ {2, 4, √p}; cite Thm 4 / Cor 2 + eq. (19) + Condition 5. | IC2, IC3 |
| R1 | K93 | keep → C15 | Asymptotic; disclose n ≳ 2·10⁶ and the scope sentence (N12). MODEST, but our prior. | IC4 (passes: our prior's constants) |
| R2 | K60 | demote to cited lemma → S5 | Barbieri–Berger 2004 Thm 1; keep (iii) size-prior ceiling and K101 cap remark as a Proposition. | IC4 |
| R3 | K65 | keep → C16 | New hypotheses: LS0 centre = prescribed start mode (e4; DP invariant N3 OPEN), ℓ ≥ max{Φ(S°) − 1, 0} (N11), completed scans / OP-LS0. | IC1 |
| R4 | K72, K78 | keep → C17 | Output-event form; add PC1 claim 5(a); R′ > 4 transfer only with the extra search; never "first finite-n" (Hou–Wang–Atchadé). | IC1 |
| R5 | K19, K68, K69, K70, K71, K72, K87 | keep → C18 | Headline (b1-LH) with LS0 (shipped); (b2-LH) no-LS0 corollary on the STAB-LH subfamily; (b1-LH-iid) v2 (GAP); (c) → C12; study generator disclosed (N8). | IC1, IC3 |
| R6 | K82 | reject as theorem → OPEN limitation | No route; report 6/2,400 with the allocation; remove "4×". | IC2 |
| R7 | K94 | defer → future work | OPEN; E's fractional-odds route (T34) bounds P₀ over data, not Π(X) given X; no constants. | IC2 |

## §C New candidates (item 3): every K row not in §B

| K-ID | Placement | Reason (≤ 40 words) |
|---|---|---|
| K01 | main → C1 | Propriety for every admissible (X, y), rank-deficient X_S included; finite algebra; Lean-able; feeds every identity. |
| K02 | main (clause of C1) | Invariance/equivariance; per-seed equivariance only in law; ties break it (limitation clause). |
| K03 | main (clause of C1) | Contrast-regression reduction (V1 consensus, to be proved) plus the b₀ → 0 bound; resolve D/E constant (2νb₀ vs n b₀ + 2a₀b₀) in wave 1. |
| K04 | main (clause of C1) | BB(1,p) mass, cap conditioning once, geometric size tails; finite sums. |
| K05 | main (clause of C16) | Leaps-and-bounds superset bound: the certified upper bound card R needs; Furnival–Wilson idea, cited. |
| K07 | main (lemma in C18; IC3 tool for C9) | Strict within/between distance gap ⇒ complete linkage + size cut + packing recover groups; needs the gap, not "block structure"; PART-CE1–3 refute sloppier forms. |
| K09 | supplement → S1 | Tie-aware max-plus DP invariant (N3 sub-obligation); finite; Lean target. |
| K10 | main → C8 and C9 | d = d_σ + d_X with d_σ ≥ 0 exact under BO; three independent derivations (ST2, T12, WS3); FD-W1 XF VERIFIED for known σ². Central to §5.3. |
| K11 | main → C9 | ε-perturbation of d_X (WS4(a)–(d) PROVED, no review; ST4, T12 restate); linear in ε through η_S. |
| K12 | supplement (folded into C9 as test oracle) | σ²-mixture exact Z under BO: oracle for numerical companions at any p; not a guarantee. |
| K13 | defer | Needs TG4-type probability bounds; PROOF SKETCH; BO only. |
| K14 | main (deterministic clause in C16) | Every block sub-model is scored, so the HPM beats every block-local model (trivial); the landscape half inherits PARTLY-FALSE and is dropped. |
| K22 | supplement → S6 | Graph facts (no isolated vertex, ≤ pB edges, positive reverse probabilities); engineering; the spurious-edge count is heuristic, not familywise. |
| K23 | supplement → S6 | Dirichlet form of the random-order round ≥ ½ random-scan mixture; finite inequality; needed later for N10. |
| K24 | defer | N10: YWJ/ZYVR route "blocked as stated"; uses the PARTLY-FALSE landscape row; E deems it implausible. |
| K25 | main → C11 | Full ESS = restricted ESS × a_u a_w/a_v²: the exact statement of what the grid certifies (I9(d)); feeds C9. |
| K27 | main → C11 | Interval inequality (v−u)²Var_ξ(d) ≤ log(10/9) ⇒ stage count ≤ spread/range bound; any grid; feeds C9 depth transfer. |
| K33 | main (clause of C11) | build_grid termination, ρ_V ≥ 0.9 at every appended point, rebuild/cost caps (N15 partial); E's precision caveat as hypothesis. |
| K34 | drop | TI reporting is not in v3.1; biased by-product; no theorem about the method. |
| K37 | main (clause of C3) | Island-minimum bound δ_R min_r Ẑ_r with δ_R = 0.05^{1/R}: valid by Markov per island and independence (seat-checked, unchecked); Hoeffding bracket only with a certified d-range. |
| K44 | main (clause of C6) | N17 PROVED (PC1 claim 1); E's U_rest bracket needs a score envelope (card R region) — remark. |
| K45 | main (clause of C7) | Retention lemma PROVED (PC1 claim 5), ½ sharp; premise of A3 ∘ R5. |
| K52 | main → C4, C5 | PC1 claim 3 PROVED given N1; the finite-R guarantee a referee asks for. |
| K54 | main (clause of C4) | R_eff/R → Z²/E[Ẑ²\|𝓒]; reporting; no coverage at R = 4 (E). |
| K55 | cited lemma | Fixed-grid CLTs (Chopin 2004; Del Moral 2004); remark in C4. |
| K56 | main (one-step clause of C4) | One-step RB variance reduction (conditional variance identity); the multi-round ordering is not claimed (E). |
| K61 | cited lemma → S5 | Posterior-expected FDP of PIP thresholding (Müller–Parmigiani–Rice 2004); exact PIPs only. |
| K62 | main (clause of C7) | Deterministic margin transfer: reported MPM = exact MPM when PIPs are δ from ½ and errors < δ. |
| K66 | drop | Asserts "SE + beta-min ⇒ any local search reaches S₀": C3-PGD, VPGD-PropG, CEX-localmax(A2) refute; no escape offered. |
| K67 | defer (CONJECTURE) | Possible escape: under BO no cross-block suppressor exists and within-block ones are enumerated by tables; must be shown against C3-PGD/CEX-localmax before any placement. |
| K73 | main → C16 | Card R: Lemma M + C4 PROVED, XF VERIFIED; "unresolved" semantics; nothing outside the region. |
| K74 | main (limitation clause of C16) | Restates CEX-localmax(A2), CEX2; local success ≠ global success. |
| K75 | future work (paper 2) | NP-completeness for this fixed score needs its own reduction; D and E disagree. |
| K76 | supplement → S1 | Eventual exact dispatch at fixed p (N12, seat-proved); consistent with T26-exact-branch-paren correction. |
| K80 | drop | No positive flag power (INP row 13); detection "probabilities" presuppose a null model the method does not assume. |
| K81 | supplement → S3 | Genealogical collapse under flat weights restates CEX-ESSneutral(A3); limitation remark. |
| K91 | drop as theorem | "Particles convert depth into work" uses perfect-mixing constants (OPW2-cex warns); speed-up vs MCMC is empirical (INP row 8); remark only. |
| K92 | future work (paper 2) | Built on the unproved moat lemma (NG1); E only conditional. |
| K95 | main (clause of C7) | Exact finite-data odds certificates: π(S₀) = 1/(1 + A(S₀)); A ≤ η ⇒ HPM = MPM = S₀; Lean-friendly. |
| K99 | future work | Saturated-cluster masked contrasts: construction must respect tie rules and the cap; NG13 speculative; relates to SHARE-PB. |
| K100 | supplement → S3 | Duplicate/interchangeable predictors: PIP → 1/d, group inclusion → 1; identifiability limitation; relates to PropD-T03, CEX-ties(A2). |
| K101 | supplement → S3 (with S5) | MPM may exceed K; cap-constrained Hamming action; HPM ≠ MPM in general. |
| K103 | supplement → S6 | Minorisation Q_φ(S,·) ≥ π_φ/(mM_φ) (D) or /M_φ (E): settle the constant in wave 1; textbook (Mengersen–Tweedie 1996); TV rate vacuous under masking. |
| K104 | supplement → S4 | Exponential-family identities, J = ∫Var d, π₀ = π iff d constant; cited (Gelman–Meng 1998); used in C9/§F. |
| K107 | defer (N16 OPEN) | Floating-point contract is engineering; T33-errbound shows the engine's bound is not a bound at large n. |
| K108 | supplement → S4 | Deterministic perturbation lemma (Z̃/Z, TV ≤ tanh ε, winner stability); feeds N16 once a validated ε exists. |

## §D Theorem cards (main and supplement)

### C1 · TARGET (K01, K02, K03, K04, K44)

| Field | Content |
|---|---|
| Statement | For every (X, y) passing preprocessing (n ≥ 3, rank-deficient X_S allowed): (i) m(S) is finite and positive, Z finite, π proper, with envelopes Q_S ≥ yᵀy/(n+1), log BF(S) = −½ log D_S − ν log(1 − x_S), 0 ≤ x_S < 1 (OWS Lemma 0); (ii) π, Z/m(∅), PIPs are invariant under column/response affine maps and permutation-equivariant; per-seed output equivariant in law only; (iii) the working posterior equals the contrast-regression posterior with IG(a₀ + ½, b₀s_y²) noise; (iv) BB(1,p) sums to one, W_K divides once, size masses decay with ratio ≤ p/(2p−1); (v) Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}. |
| Guarantee | The target is a proper, invariant posterior for every admissible input, with computable envelopes. |
| Serves | Objective (1); SL Thm 1–2 premise; INV row 1 × C. |
| Status (verbatim) | (v) N17: PROVED (PC1 claim 1; PC2 C1(c)) [INP 248]. (i)–(iv): D/E proposals (PROOF SKETCH, unchecked); reduction "to be proved, V1" (METHODOLOGY_v3 §5). About v3.1 as shipped: yes (target unchanged, M1). |
| Self-checked? | Yes (N17 cross-family; rest unchecked). |
| Novelty | MODEST (finite algebra; reduction known in kind). Checked: Barbieri–Berger 2004 (not this); no citation claims propriety for this ridge-BB prior at rank deficiency. |
| Route / key lemma | Woodbury for Q_S > 0; OWS Lemma 0; D's TG2 for (iii); E's T03 for (iv). Key lemma: Lemma 0 (fit-fraction form). |
| Difficulty | S. |
| Lean core | All of (i), (ii), (iv) (finite matrices, sums). (iii) prose. |
| Dependencies | None. Feeds C2–C9. |
| Risk | (iii)'s b₀-constant disagreement (K03) between D and E. |
| Fallback / stop | (i), (ii), (iv), (v) only; (iii) stated as a remark. Stop after one wave if (iii) unresolved. |
| IC3 design | Any X, including duplicate columns (n = 20, p = 4, x₁ = x₂). |
| Numerical companion | None needed. |

### C2 · VALID (K20, K21, K08, K35, K46, K32, K86; N9, N1)

| Field | Content |
|---|---|
| Statement | Hypotheses: EX-A, exact iid U[0,1) uniforms (H-U), frozen 𝓒 on streams 0–9, final streams 10..9+R′ independent (IND-T), R′ declared before stream 10, multinomial resampling. Then (a) each elementary move is γ_φ-reversible, the uniformly random-order round is q_φ-invariant and self-adjoint, draw_pi0 and Z̄₀ exact (N9); (b) each island is a Feynman–Kac model, so E[Ẑ_r \| 𝓒] = Z and E[Ẑ_r PIP̂_rj \| 𝓒] = Z·PIP_j (locked T12); (c) Lemma N1: for h ∈ 𝓗 bounded, measurable in (X, y, 𝓒), E[Ẑ_r H_r(h) \| 𝓒] = Z·π(h) with H_r the measured-round plain average. |
| Guarantee | Whatever the correlation, every island's unnormalised outputs are exactly unbiased, conditionally on any frozen calibration. |
| Serves | Proposal §5.1, §5.2, §13.1 (N1); objective (1); INV rows 4, 6, 8 × V. |
| Status (verbatim) | T12: PROVED-LOCKED [IDX 68]; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)) [IDX 60]; N9K: PROVED (candidate), code-checked at 39db138 (N9-KERNEL); N1: PROOF SKETCH [INP 131]; IND-T: PROVED (XF VERIFIED* A-REV1) [IDX 85]. As shipped: yes (step functions unchanged in v3.1; LS0 alters no particle; Ẑ-weighted pooling not used here). |
| Self-checked? | N9 candidate (one audit, needs the escalated line-by-line review); N1 unchecked. |
| Novelty | KNOWN—CITE for (b) (Del Moral et al. 2006; Whiteley–Lee–Heine 2016 §5.1). Ours: (a) as a certificate about the production code, (c) with RB marks and random-order prefix. |
| Route / key lemma | (c): finite-state resample–move recursion; terminal rounds preserve π; the prefix of a uniformly random order is state-independent, so the state before each measured record is π-distributed (N9 §3). Key lemma: "terminal-round prefix identity" (T26 Lemma 3 base case). |
| Difficulty | S–M (N1 one page). |
| Lean core | T12Core `unbiased_of_step` with `hstep` discharged for multinomial + invariant kernel; detailed-balance matrices; permutation reversal. |
| Dependencies | C1. |
| Risk | N1 is binding (§13.1): failure escalates. Prop2 XF GAP on output-Markov wording (handled in C3). |
| Fallback / stop | (a), (b) only; general h demoted to marginal PIPs; stop after check wave 1 verdict on N1 → escalate. |
| IC3 design | Any X. |
| Numerical companion | N9-KERNEL CHECK.md (DB ≤ 2.3e−12, 3 designs); exact enumeration of E[Ẑ_r H_r(h)] on p ≤ 8 (E §5.1 suggestion). |

### C3 · OUTPUT (K77, K78, K36, K37, K85, K42 part)

| Field | Content |
|---|---|
| Statement | Hypotheses of C2 plus Lemma RO (guard reads only the clock) and GUARD-W (any worker/LS0/guard stop ⇒ no output; code audit N2(e)). Then (a) outputs on 𝒪 equal the potential run's; (b) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05, joint with output, never conditional; (c) P(𝒪 ∩ {δ_R min_r Ẑ_r > Z}) ≤ 0.05 with δ_R = 0.05^{1/R} (independent islands); (d) any R′ declared before final randomness keeps (b); adaptive R′, path-dependent stopping or conditioning on completion break unbiasedness (CEX-guard: E[Ẑ \| output] = 0.974Z). |
| Guarantee | The paper's probability statements are about runs that return, with a 5% false-certificate rate, and the rules that keep them true are named. |
| Serves | Objective (1); INV rows 9, 14 × V; §4.4 diagnostics (certificates). |
| Status (verbatim) | LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)) [IDX 127]; CEX-guard: COUNTEREXAMPLE [IDX 128]; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT) [INP 170]; N14(b) [INP 229]; (c) seat-derived, unchecked. As shipped: Lemma RO audited on the serial v3 guard only; GUARD-W unknown (N2(e)). |
| Self-checked? | (c) by this seat; rest cross-family. |
| Novelty | Markov KNOWN—CITE (Grosse et al. 2015); the output-event discipline and counterexamples are "genuinely non-standard" (LIT-SMC). |
| Route / key lemma | Markov per island; independence of streams; Lemma RO coupling. Key lemma: PC1 claim 2 (i)–(iv). |
| Difficulty | S. |
| Lean core | Finite coupling statement of Lemma RO; the Markov/product inequality; CEX-guard as a finite two-point example. |
| Dependencies | C2. |
| Risk | GUARD-W audit fails → CEX-guard applies to v3.1 (engineering fix). |
| Fallback / stop | Potential-run form only; stop when N2(e) is filed. |
| IC3 design | Any. |
| Numerical companion | Two-point 0/2Z example (E T15). |

### C4 · POOL (K48, K49, K50, K52, K54, K56; cited K47, K55)

| Field | Content |
|---|---|
| Statement | Setting C2, W_r = Ẑ_r/Z, M = E[W_r² \| 𝓒]. (i) Ẑ-weighted μ̂(h) = Σ_r Ẑ_r H_r(h)/Σ_r Ẑ_r → π(h) a.s. as R → ∞ at fixed N; (ii) P(\|μ̂ − π(h)\| > ε \| 𝓒) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}; (iii) the equal-weight mean → E[H_1(h) \| 𝓒] ≠ π(h) in general, and E[Ẑ̄·PIP^eq_j \| 𝓒] − Z·PIP_j = −(1 − 1/R)Cov(Ẑ_1, PIP̂_1j \| 𝓒); (iv) R_eff/R → Z²/E[Ẑ² \| 𝓒]; (v) one-step RB: Var(o_j) ≤ Var(1{j ∈ S}) conditionally; (vi) for fixed R, N → ∞ consistency and CLTs: cited. |
| Guarantee | More islands fix the primary estimates, never the equal-weight ones; the price is R ≳ M/ε². |
| Serves | Proposal §5.2, §5.4 (PIP error); objective (1), (2); INV rows 8, 10. |
| Status (verbatim) | MA-PropP: PROVED (elementary) [IDX 70]; PC1c3: PROVED (PC1 claim 3); 'E[W_r ĥ_r] = π(h) is still a premise' [IDX 114]; Prop2(c): PROVED (SF: VERIFIED; XF: VERIFIED (A-REV4)) [IDX 61]; ADRAFT-ThmA: PROVED (SF: VERIFIED* (A-REV4); XF: none) [IDX 62]; (iv), (v) D/E proposals. As shipped: Ẑ-weighted primary (M4): yes. |
| Self-checked? | MA-PropP author-only (METH-AUDIT); ADRAFT Astra-only (cite Del Moral instead). |
| Novelty | (i) KNOWN—CITE (WLH 2016; Dai et al. 2022); (iii) Vergé et al. 2015; (ii) ours (PC1). |
| Route / key lemma | SLLN on unbiased numerators; Chebyshev + denominator event ≥ ½ (PC1 claim 3). |
| Difficulty | S. |
| Lean core | (iii) identity; (ii)'s finite inequality; (v) conditional-variance identity. |
| Dependencies | C2 (N1 for general h). |
| Risk | M may be exponential (N4(iii) OPEN): (ii) is correctness, not efficiency. |
| Fallback / stop | Drop (iv), (v); none else needed. |
| IC3 design | Any. |
| Numerical companion | E's two-state check (E[ẐH] = 0.9, E[H] = 0.172 vs 0.5). |

### C5 · H (K51, K46, K52; binding §13.1)

| Field | Content |
|---|---|
| Statement | Setting C2, h ∈ 𝓗 with 0 ≤ h ≤ 1, H_r the plain measured-round average (RB only for marginal PIPs), δ₁ = 1 − π(S₀). (a) islandwise, every regime and frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝓒] ≤ 2δ₁ + c_h(ρ̄ + u_π), c_h = 0 for plain averages; (b) pooled: P(\|μ̂(h) − h(S₀)\| > t \| 𝓒) ≤ exp{−R(1−s)²/(2M)} + (2δ₁ + c_h(…))/(st), with the truncation variant M_𝓒(ε); (b′) around π(h): C4(ii); (c) joint inclusion h_A = 1{A ⊆ S} for declared pairs; (d) under T03♯ hypotheses and R_n(1−s)²/M_n → ∞ in probability: μ̂(h) → h(S₀) jointly with output; (e) credible intervals: h_c(S) = P(β_j ≤ c \| S, X, y) for a finite declared list gives posterior CDF values with the same bounds. |
| Guarantee | Every reported summary is right on the islands that carry evidence weight; pooling enough islands by Ẑ makes it right; this is the §13.1 theorem. |
| Serves | Proposal §13.1, §5.4 (PIP, joint-PIP, credible-interval Monte Carlo error); objective (1); INV row 10 "joint inclusion". |
| Status (verbatim) | A1new: PROOF SKETCH (NEW-SYNTH) [IDX 155]; FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 107]; N1: PROOF SKETCH [INP 131]; PC1c3 PROVED given N1. As shipped: yes (M9 accumulator; Ẑ-weighted; any grid). Do not cite FMP-M3 (XF ERROR). |
| Self-checked? | A1 unchecked; crux N1. |
| Novelty | NEW-COMP (M1 mechanism ours; SLLN cited). |
| Route / key lemma | (a): \|H_r − h(S₀)\| ≤ fraction of measured particles off S₀; island identity for 1{S ≠ S₀} (N1). (b): Prop P(iii) with Maurer/Hoeffding. Key lemma: N1. |
| Difficulty | M. |
| Lean core | (a) deterministic step and (b) finite inequality on abstract weights. |
| Dependencies | C2 (N1), C4, C15 for (d). |
| Risk | N1 fails → shrinks to marginal PIPs and §13.1 escalates (binding). (d)'s R_n uncheckable without a bound on M. |
| Fallback / stop | (a)–(c), (e) for marginal PIPs only (locked identity); (d) with R_n hypothesis disclosing M ≳ 1/P_𝓒(cross). Stop: check wave 1 verdict on N1. |
| IC3 design | Any; joint pairs on the neighbour graph. |
| Numerical companion | Exact enumeration on p ≤ 8 of E[W_r \|H_r(h) − h(S₀)\|] vs 2δ₁ (≤ 20 seeds); not yet run. |

### C6 · Z (K38, K39, K40, K41, K42, K44, K53)

| Field | Content |
|---|---|
| Statement | One island, setting C2. (i) E[Ẑ_r \| 𝓒] = Z, E[log Ẑ_r] ≤ log Z, P(0.05Ẑ > Z) ≤ 0.05; (ii) N·Var(W_T \| 𝓒) = Σ_s(1−1/N)^{T−1−s}(E[W_s²μ_s(h²_{s,T})] − 1) for any invariant kernels; the ideal-refresh product ∏(1 + χ²_t/N) − 1 is stated as an idealisation, never substituted (OPW2-cex); (iii) masked lower tail E1/E2 and N(a): Ẑ_r ≤ √δ₁Z on islands whose terminal population is off S₀; PC1 claim 4 wording: "underestimates with high probability; the complementary rare event carries compensating overestimates; Markov caps them"; (iv) Ẑ < Z_𝒯 ⇒ Ẑ < Z; (v) Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}, gap data-dependent; (vi) favourable: Ẑ/Z → 1 under (P1) (remark); (vii) crude universal bound Var(Ẑ_r/Z \| 𝓒) ≤ (T+1)e^{2D}/N (remark, E T19, unchecked). |
| Guarantee | Ẑ is unbiased everywhere, its failure mode under masking is characterised and partly certifiable; two-sided masked accuracy is not claimed. |
| Serves | Objective (1); INV row 9; §5.4 evidence coverage. |
| Status (verbatim) | T12 PROVED-LOCKED; OPW2-ThmA: PROVED (XF: VERIFIED (A-REV9)) [IDX 169]; MZ-E1E2: PROVED (E1, E2); 'candidate: not reviewed, not adopted' [IDX 184]; FMP-Na: PROVED (XF: GAP (A-REV9)) [IDX 172]; MZ-C1: PROVED [IDX 185]; N17 PROVED; T26-ThmA: PROVED (XF: VERIFIED* (A-REV4)) [IDX 173]; T26 overall CONJECTURE. As shipped: (i)–(v) any grid, frozen 𝓒: yes. |
| Self-checked? | E1/E2 candidate (not reviewed); N(a) GAP. |
| Novelty | (i) KNOWN—CITE; (ii) "same kind as Cérou–Del Moral–Guyader 2011 Thm 1.4" (unchecked, must check); (iii), (iv) NEW. |
| Route / key lemma | Assembly; E1 is the log-odds overshoot on a frozen path. |
| Difficulty | S (assembly); check wave on E1/E2. |
| Lean core | (ii), (iv), (v) identities/inequalities on a finite space. |
| Dependencies | C2, C11 (for (vi)). |
| Risk | Cérou et al. priority on (ii). |
| Fallback / stop | (i), (iii) N(a) GAP removed, (iv), (v); (ii) as cited. |
| IC3 design | Masked LH (c = 2). |
| Numerical companion | OPW2 exact enumeration p ≤ 10 (exists). |

### C7 · Z𝒯 (K43, K45, K95, K62; §F TV/KL)

| Field | Content |
|---|---|
| Statement | 𝒯 the deduplicated reported store, Z_𝒯 = Σ_𝒯 ϖm, π_𝒯 = π(·\|𝒯). Deterministic: (a) Z_𝒯 ≤ Z; TV(π_𝒯, π) = 1 − Z_𝒯/Z and KL(π_𝒯‖π) = log(Z/Z_𝒯) exactly; (b) if S₀ ∈ 𝒯: 1 − δ₁ ≤ Z_𝒯/Z ≤ 1, \|PIP^𝒯_j − PIP_j\| ≤ δ₁, \|π_𝒯(h) − π(h)\| ≤ 2δ₁‖h‖_∞, hence TV ≤ δ₁, KL ≤ −log(1−δ₁); (c) retention: S₀ ∈ 𝒮 and δ₁ < ½ ⇒ S₀ ∈ 𝒯 = top_{40p+1}(𝒮) and MPM^𝒯 = S₀ (½ sharp; holds under LS0 eviction rule); (d) odds certificate: π(S₀) = 1/(1 + A(S₀)); A ≤ η < 1 ⇒ HPM = MPM = S₀, PIPs ≥ 1/(1+η) on S₀ and ≤ η/(1+η) off; (e) margin transfer: exact PIPs δ-away from ½ and uniform error < δ ⇒ reported MPM = exact MPM. |
| Guarantee | The reported top-store posterior is two-sided accurate in TV and KL by an exact, computable-in-principle amount, needing no grid, mixing or moment hypothesis. |
| Serves | §5.4 TV/KL; objective (1), (3); INV rows 9, 10, 11 × A. |
| Status (verbatim) | MZ-P3: PROVED (P3 top store, deterministic) [IDX 201]; PC1c5: (a) PROVED, ½ sharp; (b) 'needs ⅓' FALSE [IDX 202]; N13: PROVED [INP 225]; (a)'s TV/KL identities: PROVED (by this seat, unchecked; two lines); (d), (e): E proposals, unchecked. As shipped: deterministic, any grid, LS0-compatible (M2 eviction): yes. |
| Self-checked? | P3 candidate; TV/KL identity mine. |
| Novelty | NEW in kind ("reported-quantity trick"), elementary. |
| Route / key lemma | π_𝒯 = π/π(𝒯) on 𝒯 gives TV = 1 − π(𝒯); Lemma S for retention. |
| Difficulty | S. |
| Lean core | All (finite store sums; two-line inequalities). Model Lean target. |
| Dependencies | C18 (S₀ ∈ 𝒮), C15 (δ₁ → 0). |
| Risk | A(S₀) sums over all Ω: (d) bounds nothing from the scored set alone (E). |
| Fallback / stop | (a)–(c). |
| IC3 design | Any. |
| Numerical companion | None needed. |

### C8 · START (K15, K16, K17, K18, K10)

| Field | Content |
|---|---|
| Statement | Blocks as built, tables r_b, π₀ = γ₀/Z̄₀. (a) deterministic mass π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s, exact odds, bridge mass ≥ min(π₀(S₀), π(S₀)); (b) favourable rate (supplement); (c) masked law π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} under (H2, H3); on LH no open hypothesis; (d) dilution identity −log π₀(S₀) = V + C − log A; (e) σ²-coupling: d = d_σ + d_X with d_σ(S) = −ν[log(1 − Σ_b x_b) − Σ_b log(1 − x_b)] ≥ 0, zero iff at most one block of S has fit; d_X ≡ 0 under BO; with known σ² the BO start equals the posterior. |
| Guarantee | The merge is exactly computable, carries the truth when blocks see it, loses it polynomially under cancellation, and is wrong even under orthogonal blocks by an explicit σ²-coupling term: the bridge is never trivial. |
| Serves | SL Thm 4/Cor 2; §5.3 input; objective (1); INV row 4. |
| Status (verbatim) | T22(i)(ii)(iv): PROVED-LOCKED [IDX 337]; T22(iii): PROVED-LOCKED CONDITIONAL [IDX 338]; T27(i): PROVED-LOCKED, CONDITIONAL [IDX 339]; Thm3-EXP/Thm4-EXP: PROVED (XF: VERIFIED (A-REV2)) [IDX 321–322]; DIL-E: PROVED (XF: VERIFIED (A-REV9)) [IDX 328]; (e) OWS-WS3 PROVED (no review) [REG 520]; FD-W1: PROVED, XF VERIFIED (A-REV4) [REG 385]; ST2/T12 restate. As shipped: start unchanged (Outcome 2), any partition: yes. |
| Self-checked? | WS3 author-only; D's SC1 and E's one value agree numerically. |
| Novelty | (c), (d) NEW ("strongest novelty claim"); (e) new to D and E, folklore mechanism; block start KNOWN (Papaspiliopoulos–Rossell 2017). |
| Route / key lemma | (e): Lemma 0 fit-fraction form; log-det additivity under BO; Weierstrass product inequality. |
| Difficulty | S (restatement + one new identity). |
| Lean core | (a), (d), (e) finite algebra (DIL identity a good first G4 target). |
| Dependencies | None. Feeds C9, C10, C11, C14, C18. |
| Risk | Do not cite DIL-DM(i). Never combine (b) and (c). |
| Fallback / stop | None needed. |
| IC3 design | LH exact Gram (masked); BO blocks with two signal blocks for (e). |
| Numerical companion | D SC1 (5·10⁻¹⁴); my §E script computes d_σ (4.1–12.4 nats at n = 40). |

### C9 · WS-ε (K102, K11, K10; K25, K27, K104; WS7) — see §E

Card in §E.

### C10 · SEP (K19, K106, K105)

| Field | Content |
|---|---|
| Statement | LH exact Gram, cancellation depth c, Q* = p^c n^{c/2}. (a) Q iid π₀ draws (plus tables) score S₀ w.p. → 0 if Q/Q* → 0 and → 1 if Q/Q* → ∞; general one-sided miss bound (1 − π₀(S*))^Q ≤ e^{−Qπ₀(S*)}; (b) one-shot IS from π₀: 1 + χ²(π‖π₀) ≥ Q*e^{O_P(1)}, relative variance (Q*/Q)e^{O_P(1)}, estimate of π(S₀) exactly 0 w.p. → 1 below Q*; (c) Lemma KL: KL(π‖π₀) ≥ (1−δ₁)log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size exp(KL) is ≥ ½Q*^{1−δ₁}e^{O_P(1)}; (d) "moving off the start is needed", not "tempering" (W7-SEP). |
| Guarantee | Keeping the merge, or correcting it in one shot, costs p^c n^{c/2} draws; this is necessary and sufficient for any one-shot scheme. |
| Serves | §5.4 (merge error, KL); objective (1); SL comparison. |
| Status (verbatim) | SEP-A: PROVED (XF: VERIFIED (A-REV9)) [IDX 352]; SEP-B: PROVED (XF: VERIFIED (A-REV9)) [IDX 354]; KL: PROOF SKETCH [IDX 369]; OWS-WS7(a) gives the same KL bound with π(S₀) in place of 1−δ₁ (PROVED, no review). As shipped: iid draws from the shipped π₀; not the method's run (I4 scope). |
| Self-checked? | Lemma KL author-only (two lines). |
| Novelty | SEP NEW; exp(KL) scale KNOWN—CITE (CD18 Thms 1.1/1.2). |
| Route / key lemma | Data processing on {S₀, S₀ᶜ}. |
| Difficulty | S. |
| Lean core | Lemma KL (finite KL, log-sum inequality): model target. |
| Dependencies | C8(c). |
| Risk | None. |
| Fallback / stop | None needed. |
| IC3 design | LH exact Gram, g = 9, c = 2. |
| Numerical companion | THM-SYNTH `check_lemmas.py` (exists). |

### C11 · STG (K26, K25, K27, K28, K29, K30, K31, K33)

| Field | Content |
|---|---|
| Statement | Grid rule as coded, ESS 0.90 for pilot and grid as hypothesis. (a) Theorem G: ρ_V monotone in both endpoints, bisection finds the frontier, greedy grid shortest, T ≤ T_e on success; build_grid terminates, every appended point has ρ_V ≥ 0.9, ≤ ℓ rebuilds per tier; (b) coverage identity: full ESS = restricted ESS × a_u a_w/a_v², a_t = q_t(V), w = 2v − u: ρ_V ≥ 0.9 certifies the full bridge only up to the missing mass at u and 2v − u; (c) every accepted interval obeys (v−u)²Var_ξ(d) ≤ log(10/9) for some ξ, so T ≤ 1 + 3.08·sup_φ sd_{q_φ\|V}(d); a uniform full-space grid with ⌈range(d)/(2√log(10/9))⌉ stages has full ESS ≥ 0.9; (d) favourable: T* bounded two-sided through q_w(S₀); (e) ideal two-state grid: a crossing of gap D costs log₂D + O(1) stages, crossings add, and restricted ESS alone forces only log₂(9.5ℓ₀) stages (WS7(d)); (f) fine grid: √c·T* → Λ (cited); (g) as-coded masked T_n: Conjecture P, OPEN; the shipped guarantee is T ≤ T_e. |
| Guarantee | Correlation enters the depth only through the spread of d (through A₀ at a crossing), with explicit stage laws on the ideal grid and a deterministic cap as coded. |
| Serves | Objective (2); §4.4; INV rows 5, 7 × C. |
| Status (verbatim) | STG-G/L0/L1: PROVED [IDX 255–257]; T26BUD-G: PROVED, deterministic [IDX 268]; STG-M: PROVED (XF: VERIFIED* (A-REV9)) [IDX 261]; STG-F: PROVED [IDX 259]; STG-cexW2 COUNTEREXAMPLE [IDX 1019]; STG-L: PROVED [IDX 258]; ConjP OPEN [IDX 269]; (b), (c): D/E proposals (BR1/T14 same identity; BR2/T13), unchecked; WS7(d) PROVED (no review). As shipped: (a), (b), (c) as-coded rule and restricted law: yes; (e) ideal grid: no; (d) BO. |
| Self-checked? | (b), (c) unchecked; STG-* author + A-REV9 on M. |
| Novelty | G(i) KNOWN—CITE (Štefankovič–Vempala–Vigoda 2009); (f) KNOWN—CITE (Syed et al. 2024); (b), (c), (e) NEW, elementary. |
| Route / key lemma | Lemma RS (ρ = q_u q_w/q_v²); second-order mean value for log-sum-exp (c); two-point algebra (e). |
| Difficulty | S for (a)–(f); Conjecture P M–L (v2). |
| Lean core | Lemma RS, Theorem G greedy optimality, (b) identity, (e) two-state algebra. |
| Dependencies | C8 (A₀), C2. |
| Risk | E's resolution caveat (60 halvings) and stage ceiling as hypotheses. |
| Fallback / stop | (a), (b), (e), (f); drop (c) if the look-ahead ξ clause fails in wave 1. |
| IC3 design | Two-state masked family (ideal); any V for (a)–(c). |
| Numerical companion | O-STAGES numerics (log₂A₀ + 7.7 ± 0.4). |

### C12 · WORK (K87, K88, K89, K06, K64, K90)

| Field | Content |
|---|---|
| Statement | Units: elementary step slots and score evaluations. (a) work = tables (Σ_b 2^{\|C_b\|} ≤ p2^B/B; ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉) + calibration ((1+4I_e)H_e per tier, ≤ ℓ rebuilds per tier) + R′N_e(T+L+4)(p+B+2) + local searches ((ℓ+1)(p + k*(p−k*)), k* = min(K, ⌊p/2⌋), including LS0 and the extra search) + O(np²) + clustering; polynomial in n under the budgets (T32(i), rate GAP); (b) island-level depth = setup + calibration + N_e(T+L+4)(p+B+2) slots + searches, width R′ (waves above the worker count); "free of N, H, R" not claimed; (c) Brent time ≤ W/P + D; depth Ω((T+T_cal)·m) because a particle's round is sequential (I1); Θ(p²) Gram memory is an implementation ceiling (C7 path); (d) Song–Liang §6 in the same units: wall O(p^{(1+α)/2}) + O(np) with width √p and output restricted to the merged set; no speed claim. |
| Guarantee | An honest work/depth/width account of v3.1 at the shipped (island) level, comparable with SL §6. |
| Serves | Objective (2); SL §6; INV rows 8, 11, 14 × C. |
| Status (verbatim) | MA-PropD: PROVED (counting) [IDX 242]; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none) [IDX 237], rate GAP; Cost-T38: PROVED-UNDER (XF: GAP (A-REV5)) [IDX 238]; N15 calibration share seat-derived [INP 238]; K06 D/E counting (Johnson 1973). As shipped: yes after the LS0 and k* corrections. |
| Self-checked? | T32(i) same-family only. |
| Novelty | Accounting (TCS style); K90 comparison new in units only. |
| Route / key lemma | Count the loop structure; next-fit bound. |
| Difficulty | S. |
| Lean core | Counting identities (low value). |
| Dependencies | C11 (T), S1 (bitwise). |
| Risk | Measured-table placeholder in METH-AUDIT must be filled before citing. |
| Fallback / stop | Drop the displayed rate; keep "polynomial". |
| IC3 design | Any. |
| Numerical companion | 3 logged designs for the calibration share (0.45/0.62/1.76). |

### C13 · CD, the thesis theorem (K96)

| Field | Content |
|---|---|
| Statement (scope proposal; final in R2) | Fix any X, y, EX-A, frozen 𝓒, R′ declared. (a) never correctness: C2 identities and C4/C5 limits hold with no premise on X; (b) depth: T ≤ T_e as coded; on the ideal grid T = O(1) favourable or log₂A₀ + O(1) per crossing (C11); under ε-correlated blocks the full-space depth transfers from the BO-equivalent bridge at threshold 0.9e^{∓8η(ε)} (C9); (c) particles/islands: error ≤ exp{−R(1−s)²/(2M)} + (2δ₁+…)/(st) with M ≳ 1/P_𝓒(cross); (d) selection: on LH the reported HPM equals S₀ w.p. → 1 − limsup P(U) (C18) while split-and-merge loses the hub (C14). Wording per E: correlation changes overlap, depth and the particles or islands needed; not the target, the identities or the limit; not monotone in a coefficient; not conditional on delivery. |
| Guarantee | Correlation is a cost, not a correctness condition; SL's Condition 5 is a correctness condition. |
| Serves | All three objectives; LIT-PAR S-GAP. |
| Status (verbatim) | Assembly: V1 (KNOWN—CITE + locked), A1 (PROOF SKETCH), D1 (PROVED counting), D2 (PROVED ideal grid / OPEN as-coded), R5, C1 [LST 31, 392]; M3 removed (XF ERROR). As shipped: island level; ideal-grid clause flagged. |
| Self-checked? | Inherits its parts. |
| Novelty | NEW-COMP. |
| Route | Assembly. |
| Difficulty | That of C5 and C14. |
| Lean core | None beyond parts. |
| Dependencies | C2, C4, C5, C9, C11, C14, C18. |
| Risk | Overclaim; fixed by E's scope sentence. |
| Fallback / stop | (a), (b) as-coded cap, (d); state (c) with M as a hypothesis. |
| IC3 design | LH exact Gram (masked) and ε-separated blocks (C9). |
| Numerical companion | None. |

### C14 · SL (K97)

| Field | Content |
|---|---|
| Statement | LH exact Gram with c linked pairs, g ≥ 2, uniform random equipartition into K_n subsets. (a) P(masked hub isolated from its partner and group) ≥ 1 − c·g/K_n → 1 when K_n → ∞; (b) on that event the hub is an exactly orthogonal null column in its subset: Condition 5 fails (cov = 0), β₀ = 0 in every iteration, and under SL's priors its PIP → 0, so SL's output omits it; (c) the exact posterior is fine (T03♯); (d) v3.1 on the same family: C2 holds and with LS0 P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (C18); (e) clustered splits retain the hub but SL's theory does not analyse them. |
| Guarantee | In split-and-merge, correlation breaks correctness exactly; in v3.1 it costs depth and particles only. |
| Serves | Objective (3), SL Thm 4/Cor 2 comparison; LIT-PAR G4. |
| Status (verbatim) | C1new: COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH) [IDX 443]; Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP)) [IDX 325]; T38-b1-LH (below). D/E give π₀ ≠ π only. As shipped: (d) yes via C18. |
| Self-checked? | Yes (PROOF SKETCH; numerics on g = 1 only). |
| Novelty | NEW (no analytic SaM failure published; checked LIT-PAR, SL digest). |
| Route / key lemma | Hypergeometric isolation count; x′μ = 0 identity; Bayes factor of an orthogonal null column under IG + Gaussian + λ_s prior is O_P((1+nV)^{−1/2}). |
| Difficulty | M. |
| Lean core | (a) combinatorics; (b) linear algebra on Σ_LH. |
| Dependencies | C8(c), C15, C18. |
| Risk | The FDR threshold step; cite SL Thm 4 / Cor 2 + eq. (19), never "Thm 5". |
| Fallback / stop | Fixed threshold q ∈ (0,1) instead of the FDR rule; re-run numerics on LH g ≥ 2, K ∈ {2, 4, √p}. |
| IC3 design | LH exact Gram, g = 9, c = 2, ρ = 0.4, ψ = 0.2. |
| Numerical companion | LIT-PAR G4 (5/318 vs 20/20); re-run planned (≤ 20 seeds). |

### C15 · SEL (K93; K61, K94 remarks)

| Field | Content |
|---|---|
| Statement | R1 hypotheses (s₀ fixed, p ≤ n^A, G, R, SE, BM-∞ or BM(c)), fixed design: 1 − π(S₀) = O_P(√(log n/n)); HPM, MPM of π equal S₀ w.p. → 1; P(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)]; large signals get PIP → 1 without beta-min; exact BB(1,p) tail T02(i♯). Scope sentence: p ≤ n^A comes from the prior and proof technique; e^{Cn^α} OPEN. |
| Guarantee | The target is right with enough data. |
| Serves | Objective (3); SL Thms 1–3, S. |
| Status (verbatim) | T01-T03: PROVED-LOCKED [IDX 469]; T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)) [IDX 151]; T03-1.2e5 ERROR repaired (n ≳ 2·10⁶). Algorithm-free. |
| Self-checked? | No. |
| Novelty | MODEST (Rossell 2022; Moreno–Girón–Casella 2015); T03♯(3) KNOWN—CITE (Rossell Prop 1). "Do not sell it". |
| Route | Done. |
| Difficulty | S (disclosure sentence). |
| Lean core | T02(i♯) binomial-coefficient inequality. |
| Dependencies | None; feeds C5(d), C7, C14, C17, C18. |
| Risk | Vacuous at n = 200 (disclose). |
| Fallback / stop | None needed. |
| IC3 design | LH exact Gram (SE holds). |
| Numerical companion | None. |

### C16 · REPAIR and certificates (K65, K63, K64, K73, K74, K05, K14)

| Field | Content |
|---|---|
| Statement | EX-A, completed scans, tie-broken greedy map, capped lattice. (a) Theorem A: under TD′_∞ on Lat(S°), the local search from C ∈ Lat(S°) with ℓ ≥ τ(C) reaches, scores and certifies S₀ in ≤ Φ(C) moves; LS-score: LS0 from the prescribed start mode scores S₀ within max{Φ(S°) − 1, 0} moves; Lemma M: margins ⇒ TD′ w.p. → 1 under SE; (b) Lemma S: the HPM is the ≻-maximum of the scored set, order-independent; top_c merges; with LS0, 𝒯_new = top_c(𝒯_old ∪ 𝒮_added); (c) local search moves only on strict improvement, ≤ (ℓ+1) scans of ≤ p + k*(p−k*) models; local_certified means a strict flip/swap local maximum at the scanned centre; every block sub-model is scored, so the HPM beats every block-local model; (d) card R: B&B on [∅, U] with the leaps-and-bounds superset bound is exact when complete, "unresolved" on exhaustion, certifies nothing outside U; (e) limitation: a certified local maximum can lie far below the mode (CEX-localmax, CEX2). |
| Guarantee | From a near-truth centre the deterministic search finds the truth in finitely many moves; what the certificates mean is exact. |
| Serves | Objective (3); INV rows 11, 12; §4.4 certificates. |
| Status (verbatim) | TheoremA: PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) [IDX 500]; LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 508]; MA-LemmaS: PROVED (candidate) [IDX 91]; OCERT-LemmaM: PROVED (XF: VERIFIED (A-REV9)) [IDX 744]; OCERT-C4: PROVED (XF: VERIFIED* (A-REV9)) [IDX 748]; N7 L1 CORRECT WITH AMENDMENT [INP 176]; K05 D proposal. As shipped: LS0 route about v3+LS0; bridge to code N2(c) not done; e4 DP invariant N3 OPEN. |
| Self-checked? | Lemma S candidate; K05 unchecked. |
| Novelty | "Unsurprising given YWJ/ZYVR" but deterministic exact finite-n; cite Gamarnik–Zadik Thm 2.7, YWJ Lemma 4. |
| Route / key lemma | Done (T37Greedy/Lattice.lean sorry-free); K05 by monotonicity of Q and log-det in S. |
| Difficulty | S. |
| Lean core | Sorry-free already; Lemma S and K05 feasible. |
| Dependencies | C8(c) (S° ∈ Lat), C15 (Lemma M). |
| Risk | "rigorous global_certified" is not a theorem (N7); keep the heuristic label. |
| Fallback / stop | None needed. |
| IC3 design | LH exact Gram. |
| Numerical companion | LS0 changed 0/2,394 HPMs. |

### C17 · COMP, every n (K72; K82 as limitation)

| Field | Content |
|---|---|
| Statement | EX-A; Ŝ the ≻-maximum of the scored set on 𝒪; S† that of Ω. (a) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, D_n = P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}); (b) P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮) with the matching lower bracket; (c) Ŝ = S₀ if S₀ ∈ 𝒮 and δ₁ < ½ (sharp); (d) Lemma RO; R′ > 4 transfer only with the extra search from c₄; (e) P(U) is OPEN (reported with the allocation), not a theorem. |
| Guarantee | A wrong report means no output, a wrong posterior, or a never-scored truth; the only inequality non-vacuous at n = 200. |
| Serves | Objective (3); INV rows 1, 11, 14. |
| Status (verbatim) | Thm4-C1: PROVED (SF: VERIFIED* (W5-LOCKBOOK)) [IDX 527]; T38-(0): PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)) [IDX 528]; N200: PROVED (elementary, every n); Π(X) upper bound OPEN [IDX 534]; PC1c5(a) PROVED; PC1c6 PROVED with caveat. As shipped: yes (every n, as run). |
| Self-checked? | N200 author-only → route to an independent check. |
| Novelty | Elementary; 2E₀δ₁ KNOWN—CITE (Rossell 2022 Prop 1); do not say "first finite-n" (Hou–Wang–Atchadé 2024/2026). |
| Route | Done (T21HPM.lean sorry-free). |
| Difficulty | S. |
| Lean core | t21_C1 sorry-free; N200 Lemma 1 feasible. |
| Dependencies | C15, C18, C3. |
| Risk | None. |
| Fallback / stop | None needed. |
| IC3 design | Any. |
| Numerical companion | 6/2,400; 565 competitor defeats; 0/2,394. |

### C18 · HPM consistency (K68, K69, K70, K71, K45, K07; K13, K14 excluded)

| Field | Content |
|---|---|
| Statement | Hypotheses EX-A, EX-S, CAL, SR, GUARD + GUARD-W, (P) on R1, OP-LS0, e4 centre rule, ℓ ≥ max{Φ(S°) − 1, 0}, SIZE g_max ≤ B < 2g_min. (0) as C17(a); (a) favourable, iid draws: D_n → 0; (b1-LH) LH exact Gram (p ≤ n − 1, c linked pairs): with LS0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical hypothesis; (b2-LH) without LS0 on the STAB-LH subfamily (g = 9, c = 2, ρ = 0.4, ψ = 0.2), any frozen grid: P(S₀ ∉ 𝒮 \| 𝓒) → 0; (lemma) strict within/between distance gap and groups ≤ B ⇒ clustering + packing return the groups (PART-ThmA on LH-iid, K07); (b1-LH-iid) v2 (GAP); the study generator (2g ≤ B) is disclosed as uncovered (N8, PART-CE2). |
| Guarantee | The reported model is the truth w.p. → 1 − limsup P(U) in both regimes for the shipped method on an explicit correlated family where the start is masked. |
| Serves | Objective (3); LIT-VENUE G1; SL Thm S exceeded. |
| Status (verbatim) | T38-(a): PROVED-UNDER [IDX 548]; Thm-b1: PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8)) [IDX 549]; T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 438]; B2E-B2LH: PROVED-UNDER (XF: VERIFIED* (A-REV7)) [IDX 439]; STAB-cert(A7) REFEREE (Astra-authored) [IDX 568]; T38-b1-LH-iidfail ERROR/GAP (C24) [IDX 553]; PART-ThmA: PROVED (XF: VERIFIED* (A-REV9)) [IDX 768]. As shipped: (b1-LH) v3 + LS0 = v3.1 (M2), code bridge N2(c) pending; (b2-LH) v3 without LS0 (variant); (a) iid draws (variant). |
| Self-checked? | STAB certificate Astra-authored, Claude-verified (fine). |
| Novelty | NEW for this target/method; "corollary of YWJ/ZYVR under their prior" (say both). Mathews–Schmidler 2024 template for (a). |
| Route | Statement of record exists (T38_STATEMENT v3). |
| Difficulty | S (assembly); v2 items M–L. |
| Lean core | Composition sorry-free; Lat moves feasible. |
| Dependencies | C8(c), C15, C16, C3. |
| Risk | e4 tie-DP invariant (N3) OPEN; ℓ for growing support (N11). |
| Fallback / stop | Headline (b2-LH) if N3 fails; stop rule: one HQ wave for N3. |
| IC3 design | LH exact Gram, g = 9, c = 2 (genuinely correlated: ρ = 0.4 within, ψ = 0.2 cross-hub). |
| Numerical companion | 0/2,394 (S₀ ∉ 𝒮); LS0 0 changes. |

### S1 · PAR (K83, K84, K86, K09, K76, K22-part)

| Field | Content |
|---|---|
| Statement | (a) Prop W / W-cal: concurrent islands, diagnostic islands and scans reproduce the serial run bitwise (one binary, single-thread BLAS, process workers, fixed reduction order); (b) Cor W-R: stacking R′ = 4k leaves islands 1–4 unchanged; with the extra search from c₄ the scored set nests and HPM(R′) ⪰ HPM(4); without it, FALSE; (c) stream separation 10..9+R′ (IND-T extended; code audit); (d) tie-aware DP returns the prescribed start mode (N3 sub-obligation); (e) for fixed p the exact branch is eventually taken (N12). |
| Guarantee | The parallel layer changes no number. |
| Serves | Objective (2) (engineering premise). |
| Status (verbatim) | MA-PropW: PROVED (code reading; executed) [IDX 92]; MA-Wcal: PROVED (code reading only; not executed) [IDX 93]; PC1c6 [IDX 652]; IND-T [IDX 85]; (d) OPEN (N3) [INP 146]; (e) seat-proved, unchecked [INP 214]. As shipped: code facts about v3.1. |
| Self-checked? | Code audits. |
| Novelty | None (engineering). |
| Route | Code audit; (d) greedy index-by-index with max-plus feasibility DP (R3A/R3B). |
| Difficulty | S. |
| Lean core | Lemma S (in C16); (d) finite DP invariant: good target. |
| Dependencies | None. |
| Risk | W-cal not executed. |
| Fallback / stop | (b) LAW-PRESERVING if W-cal fails. |
| IC3 design | n/a. |
| Numerical companion | CONC 3/3 designs. |

### S2 · EQ-PIP (K57; K58 deferred)

| Field | Content |
|---|---|
| Statement | P1: \|E[PIP̂_rj] − PIP_j\| ≤ TV(law of the delivered terminal population, π); after locking (all particles at S₀) the bias is ≤ δ₁ and the L¹ error ≤ (L+4)ρ̄ + u_π + δ₁ (LH, fixed p). Thm R (DELIV-POP) deferred. |
| Guarantee | The secondary (equal-weight) PIP is right iff the population is delivered; it does not improve with R. |
| Serves | §5.4 TV (delivered law); INV row 10. |
| Status (verbatim) | MZ-P1P2: P1 PROVED; P2 PROVED as a composition [IDX 224]; OBG-BG3: PROVED (XF: VERIFIED (A-REV7)) [IDX 219]; OBG-LH-lock-general XF ERROR [IDX 1061]: general LH locking is FALSE. As shipped: equal-weight secondary (variant of the primary). |
| Self-checked? | P1 candidate. |
| Novelty | NEW-COMP, elementary. |
| Route | Done. |
| Difficulty | S. |
| Lean core | P1 finite TV bound. |
| Dependencies | C2. |
| Risk | Locking only on LH fixed p. |
| Fallback / stop | P1 only. |
| IC3 design | LH fixed p. |
| Numerical companion | none. |

### S3 · LIMITS (K79, K81, K100, K101, K74 cross-ref)

| Field | Content |
|---|---|
| Statement | (a) E1c/E2: changing an unqueried state's mass leaves the transcript unchanged, so no run diagnostic certifies absence of unseen modes (oracle statement; positive certificates can still detect some failures); (b) flat weights do not prevent genealogical collapse (CEX-ESSneutral); (c) duplicates: equal PIPs, PIP → 1/d with group inclusion → 1, no estimator distinguishes duplicates; \|S₀\| > K has posterior zero; (d) the MPM may exceed K; HPM ≠ MPM in general. |
| Guarantee | The limitations the paper prints are proved or definitional, not missing proofs. |
| Serves | §4.4 (negative), objective (3) scope. |
| Status (verbatim) | MZ-E1E2 PROVED (candidate) [IDX 184]; CEX-ESSneutral(A3) COUNTEREXAMPLE [IDX 1011]; (c), (d) D/E proposals; related PropD-T03, CEX-ties(A2). |
| Self-checked? | (c), (d) unchecked (elementary). |
| Novelty | Known phenomena; cite Chatterjee–Diaconis 2018 Thm 2.1, Vehtari et al. for context. |
| Route | Elementary. |
| Difficulty | S. |
| Lean core | (a) transcript invariance on a finite space; (c) symmetry. |
| Dependencies | None. |
| Risk | Overstating (a) as information-theoretic (D, E both caveat). |
| Fallback / stop | n/a. |
| IC3 design | duplicate columns. |
| Numerical companion | none. |

### S4 · KL/TV lemmas (K104, K108; §F)

| Field | Content |
|---|---|
| Statement | (a) π_φ is an exponential family in d: Λ′ = E d, Λ″ = Var d, log(Z/(m(∅)Z̄₀)) = ∫₀¹E_{π_φ}d, KL(π‖π₀) + KL(π₀‖π) = ∫₀¹Var_{π_φ}(d) = J, J = 0 iff d constant, Λ ≤ √J; (b) if every log mass is perturbed by ≤ ε: Z̃/Z ∈ [e^{−ε}, e^{ε}], TV(π̃, π) ≤ tanh ε, a winner with gap > 2ε is unchanged; kernel errors accumulate by path coupling as Σδ_t. |
| Guarantee | The exact calculus of the merge's error and of score perturbations. |
| Serves | §5.4 KL; N16 (future). |
| Status (verbatim) | D/E proposals (PROOF SKETCH, unchecked); OWS Lemma Λ PROVED (no review). |
| Self-checked? | Unchecked. |
| Novelty | KNOWN—CITE (Gelman–Meng 1998); (b) elementary. |
| Route | Differentiate Λ; log-sum-exp perturbation. |
| Difficulty | S. |
| Lean core | (b) entirely; (a) finite derivatives. |
| Dependencies | C8. |
| Risk | None. |
| Fallback / stop | n/a. |
| IC3 design | any. |
| Numerical companion | none. |

### S5 · BAYES (K60, K61, K101)

| Field | Content |
|---|---|
| Statement | Cited lemma: HPM = 0–1 Bayes rule, MPM = Hamming Bayes action (Barbieri–Berger 2004); PIP threshold 1 − q has posterior-expected FDP ≤ q (Müller–Parmigiani–Rice 2004). Ours: (iii) no size-only prior repairs a same-size swap (sharp); the cap-constrained Hamming action; MPM may exceed K. |
| Guarantee | Why the HPM is the decision and what no size prior can fix. |
| Serves | Objective (3). |
| Status (verbatim) | Prop1-T07: PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) [IDX 482]; Prop1-wrongHPM XF ERROR (do not say a wrong HPM implies a posterior miss). |
| Self-checked? | No. |
| Novelty | FOLKLORE except (iii). |
| Route | Done (T07Bayes.lean sorry-free). |
| Difficulty | S. |
| Lean core | Sorry-free. |
| Dependencies | None. |
| Risk | None. |
| Fallback / stop | n/a. |
| IC3 design | any. |
| Numerical companion | none. |

### S6 · KERNEL lemmas (K23, K103, K22)

| Field | Content |
|---|---|
| Statement | (a) Dirichlet form of the random-order round ≥ ½ that of the random-scan mixture, so gap(Q_φ) ≥ ½gap(R₂); (b) the round minorises: Q_φ(S,·) ≥ π_φ(·)/(mM_φ) (D) or /M_φ (E; via the independence step), M_φ ≤ exp{φ(d_max − E_{π₀}d)}, hence ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1 − ε_φ)^k; (c) the capped symmetric graph has no isolated vertex, ≤ pB edges, positive reverse probabilities. |
| Guarantee | Quantitative kernel facts for later mixing work; the TV rate is useless under masking (M_φ exponential). |
| Serves | §5.4 TV (delivered law, in principle); N10 (future). |
| Status (verbatim) | D/E proposals (unchecked); N10 NONE / OPEN [INP 199]. As shipped: kernel as coded. |
| Self-checked? | Unchecked; D/E constants differ. |
| Novelty | Textbook (Mengersen–Tweedie 1996); (a) possibly folklore. |
| Route | Doeblin through the independence label first w.p. 1/m; two-line Dirichlet inequality. |
| Difficulty | S. |
| Lean core | (a) finite inner-product inequality; (b) minorisation inequality. |
| Dependencies | C2. |
| Risk | Vacuity. |
| Fallback / stop | (b) only with D's constant. |
| IC3 design | any. |
| Numerical companion | none. |

## §E Proposal §5.3 (item 4): the strongest provable statement

**Position.** A paper-1 theorem exists, in the method's own form; the proposal's literal one-shot form does not, and that is provable, not a missing proof.

**Why the literal form fails for the shipped start.** (i) Even with zero cross-block correlation the block product is wrong by the σ²-coupling term d_σ ≥ 0 (K10; FD-W1 XF VERIFIED: equality only with known σ²). (ii) Under ORTH with growing truth-free nulls, χ²(π‖π₀) → ∞ while TV(π, π₀) → 0 (OWS-WS6(d), PROVED, no review): "bounded one-shot weight variance under weak cross-block dependence" is false for this start at p = n − 1 whenever R̄² > ½. (iii) Under masking ESS_∞ ≤ π₀(S₀)/π(S₀)² → 0 (WS7(a), PROVED, no review). So the honest §5.3 object is the *bridge's* weights, and the theorem is *relative*: cross-block correlation perturbs every weight quantity by a factor linear in ε around the block-orthogonal baseline.

### Card C9 · WS-ε (K102, K11, K10; K25, K27, K104; WS7)

| Field | Content |
|---|---|
| Statement | Blocks as built. For S ∈ Ω let A_S be the block-diagonal part of R_S = G_S/(n−1), E_S = R_S − A_S, ε_S = ‖A_S^{−1/2}E_SA_S^{−1/2}‖, F_S = ‖·‖_F², x̄_S = Σ_b x_b(S). Hypotheses (on X, y only): A_S ≻ 0 and ε_S < 1 − x̄_S for all S ∈ W ⊆ Ω; η_W := max_W [νε_Sx̄_S/(1 − ε_S − x̄_S) + F_S/(4(1 − ε_S))]. Then: (a) d = d_σ + d_X with d_σ ≥ 0 exact (C8(e)) and \|d_X(S)\| ≤ η_S; (b) transfer: for every v, e^{−4\|v\|η_W} ≤ [1 + χ²(q_v^W‖π₀^W)]/[1 + χ²(q_v^{σ,W}‖π₀^W)] ≤ e^{4\|v\|η_W}, TV(q_v^W, q_v^{σ,W}) ≤ 1 − e^{−2\|v\|η_W}, where q^σ is the BO-equivalent bridge; per interval (WS1(b)): the restricted or full one-step ESS of the two bridges differ by a factor ≤ e^{8η_W}; (c) first stage: the stage-1 weight variance of a final island is exactly χ²(q_{φ₁}‖π₀)/N_e (particles iid π₀), hence within e^{4φ₁η} of its BO value; (d) depth: the greedy ESS-0.9 grid of the ε-bridge is no longer than the σ-bridge's greedy grid at threshold 0.9e^{8η} (Theorem G optimality), and a uniform full-space grid needs ≤ 1 + ⌈(range(d_σ) + 2η_W)/(2√log(10/9))⌉ stages; (e) sufficient condition: ε_S ≤ \|S\|·max_{cross}\|r_jk\|/λ_min(block Gram), so η_W = O(νKε x̄/((1−ρ)(1−x̄))) and the statement is non-vacuous iff ε = O((1−ρ)/(nKx̄)). |
| Guarantee | Weak non-zero cross-block correlation changes every bridge weight, ESS and the stage count only by an explicit factor linear in ε around the block-orthogonal baseline; what that baseline costs is C8(e)/C11, and masking (WS7) is a transport problem, not a weight problem. |
| Serves | Proposal §5.3 (binding); objective (2); INV rows 5, 8. |
| Status (verbatim) | OWS-WS4: PROVED (SF: none; XF: none) [REG 521]; OWS-WS1/WS2: PROVED (no review) [REG 518–519]; OWS-WS3 PROVED; OWS-WS7 PROVED; AREV9-OWSTAB: W(a)–(f) 'VERIFIED under H-ORTH' [IDX 423] (not WS4); S4 draft: "under H-ORTH and an ideal grid" [LST 503]; (c), (d) PROVED (by this seat, unchecked; (d) by STG-G); K11 D/E restate (ST4, T12). As shipped: bridge law for the method's partition, grid-free: yes; (c) as coded (iid π₀ draws, multinomial): yes; (d) greedy rule as coded on V: yes with V-restriction (coverage K25). |
| Self-checked? | **Yes**: WS1–WS4, WS7 are author-only (O-WSTAB, "no verification at all", LOCKABLE_v2 §3e). Route to cross-family check. |
| Novelty | NEW-COMP: the relative transfer and the σ²-coupling baseline are ours; perturbation inequalities KNOWN (Weyl, resolvent); Frazier et al. 2023 Assumption 6(iv) is the generic χ² precedent (checked INV §4b). |
| Route / key lemma | WS1(a): log(1 + χ²(q_v‖π₀)) = Λ(2v) − 2Λ(v); \|Λ − Λ^σ\| ≤ \|φ\|η; (a) by Woodbury/Weyl on H_S = H_d + c₁E. Credible: two-line exponential-family argument plus standard matrix perturbation; checked numerically below. |
| Difficulty | S–M (restate OWS; (d) one paragraph). |
| Lean core | (a)'s scalar inequalities, (b)'s cumulant identity and transfer on a finite space, (c) exact variance, (d) greedy optimality: all finite/real-analytic. |
| Dependencies | C8(e), C11(a)–(c), S4(a). |
| Risk | Scale: non-vacuous only for ε ≪ n^{−1/2} (below chance correlations of random designs). Honest disclosure; the random-design counterpart is the leakage route WS5.3(F) (favourable start under weak leakage, PROVED-UNDER) and the threshold WS6(e) (CONJECTURE, future work). |
| Fallback / stop | (a) + (c) as a Proposition ("the discrepancy is controlled by cross-block covariance; first-stage weights are stable"); if the cross-family check refutes (b) and it is not repaired in one wave, ship the fallback and escalate §5.3 to HQ (binding). |
| IC3 design | ε-separated exact-Gram family: X with XᵀX = (n−1)Σ, Σ = blockdiag(equicorrelated ρ ∈ (ε, 0.9], sizes ≤ B) + ε off-block, 0 < ε ≤ (1−ρ)/(nK); signal in ≥ 2 blocks. Complete linkage recovers the blocks (K07: within distance 1−ρ < between 1−ε). Genuinely correlated within blocks; cross-block correlation non-zero. |
| Numerical companion | Script below: n = 40, p = 8, two blocks of 4, ρ = 0.5, ε ∈ {0, 0.002, 0.01}, 5 seeds each (15 cases): max\|d − d_σ\| ≤ η_W in 15/15; ratio (1+χ²_ε)/(1+χ²_σ) ∈ [0.853, 1.011] at v ∈ {¼, ½, 1} against bounds e^{4vη_W} ∈ [1.09, 107]; d_σ between 4.1 and 12.4 nats (baseline non-trivial). |

Script (`ws4_check.py`, ≤ 1 min; exact Gram by X = √(n−1)·U·chol(Σ)ᵀ with U orthonormal centred; d, d_σ, η_S per WS4; Λ via log-sum-exp over all \|S\| ≤ 4):

```
rho eps seed | eta_W  max|d-d_sigma| ok?  max d_sigma | v: ratio vs e^{4 v eta_W}
0.5 0.002 1 |  0.211   0.1911 ok  11.808 | v=0.25: 0.995 vs 1.23  v=0.5: 0.982 vs 1.52  v=1.0: 0.968 vs 2.32
0.5 0.010 1 |  1.169   0.9788 ok  12.385 | v=0.25: 0.975 vs 3.22  v=0.5: 0.910 vs 10.35 v=1.0: 0.853 vs 107.21
... (15 rows)  violations: 0
```

**What ships against the binding goal.** C9 (main). The paper states the proposal's direction as: "the divergence between the block-product start and the posterior decomposes into an orthogonal-block σ²-coupling term and a cross-block term bounded linearly by the standardised cross-block Gram; all bridge weight variances and the depth transfer from the orthogonal case by a factor e^{O(ε n x̄)}". Not met and provably so: bounded *one-shot* weight variance (WS6(d), WS7). HQ question §I-1.

## §F Proposal §5.4 (item 5): approximation error

The method corrects exactly at φ = 1 (C2), so "approximation error" refers to three things: (1) the merge's own error (π₀ vs π), which the bridge removes; (2) the Monte Carlo error of the delivered estimates relative to the exact posterior; (3) the error of the *reported* restricted posterior π_𝒯.

| Metric | Card / clause | Status and what ships |
|---|---|---|
| TV, merge error | WS7(a): TV(π, π₀) ≥ π(S₀) − π₀(S₀) → 1 under masking; S4(a): J identity | Lower bounds PROVED (no review); ships as the "why a bridge" statement (C8, C10). |
| TV, Monte Carlo | C7(a): TV(π_𝒯, π) = 1 − Z_𝒯/Z exact, ≤ δ₁ if S₀ ∈ 𝒯 → 0 under C15 + C18; S2 P1: PIP bias ≤ TV(delivered law, π); fixed-data TV → 0 a.s. as R → ∞ (C4(i), Ω finite) and as N → ∞ (cited); S6(b) rate (vacuous under masking) | Ships: the exact reported-posterior TV theorem (deterministic, Lean) and the fixed-data limits (cited). Not provable at finite R, N in the masked regime: a TV bound for the delivered law needs mixing (N10 OPEN); not an inherent limitation, an OPEN obligation. |
| KL, merge error | C10(c) Lemma KL: KL(π‖π₀) ≥ (1−δ₁)log(1/π₀(S₀)) − log 2; S4(a) KL sum = J; WS6(c) upper bounds via tilt control (favourable) | Ships (lower bound PROOF SKETCH, two lines; J identity cited). |
| KL, reported posterior | C7(a): KL(π_𝒯‖π) = log(Z/Z_𝒯) ≤ −log(1−δ₁); KL(π‖π_𝒯) = ∞ (support) | Ships (deterministic). The infinite direction is a definitional fact of a restricted store (I9(c)). |
| PIP error | C5(a), (b); C4(ii) | Ships (PC1 claim 3 PROVED given N1; M1 XF VERIFIED). |
| Joint-PIP error | C5(c) with plain averages, declared pairs; crux N1 | Ships conditional on N1 (binding §13.1 escalation if N1 fails). |
| Credible-interval coverage | C5(e): h_c(S) = P(β_j ≤ c \| S, X, y) for a declared finite list of c is an admissible bounded h (M9), so the Monte Carlo error of the reported posterior CDF, hence of any posterior credible interval, obeys C5(a)–(b) and C4(ii); the margin transfer C7(e) gives "reported interval = exact interval" under a quantile margin | Ships as Monte Carlo coverage error. **Not delivered:** frequentist coverage of the exact posterior's credible intervals (a target-theory property of Felipe's model; not an objective; van der Pas–Szabó–van der Vaart 2017 show it is not generally honest). This is not a silent drop: §I-2. |

Binding-goal check: §5.4 is met in the exact-correction reading (error of reported quantities relative to the exact posterior, in TV, KL, PIP, joint-PIP and posterior-interval terms), with the finite-budget masked-regime TV of the delivered law left OPEN (listed as an obligation, not a limitation).

## §G Fidelity (item 8): inherited results relied on in §D

| Registry ID | About v3.1 as shipped? LS0 / coded grid / Ẑ-weighted pooling (path:line) | Gap | Gap lemma to prove |
|---|---|---|---|
| T12, T31(i) [IDX 68–69] | yes (LS0 alters no particle, M2) / yes (any frozen grid) / n/a (islandwise) | none | — |
| Prop2(a,b,d,e) [REG 260] | yes / yes / yes (islandwise numerators) | XF GAP on output-Markov wording | Output-event form: C3(b) (PC1 claim 2). |
| N9K (T09) [IDX 72; N9-KERNEL §2] | yes (step functions unchanged at 39db138) / n/a / n/a | author-only; (H-U), exact arithmetic | Line-by-line review of PROOF.md Claims S, R; add (H-U) hypothesis. |
| IND-T [REG 190] | streams 10–13 only / n/a / n/a | streams 10..9+R′ unknown (N14(c)) | IND-T over distinct (island) stream ids for every declared R′ (one-line re-proof + code audit). |
| LemmaRO [REG 258] | serial v3 guard only / n/a / n/a | GUARD-W for workers, merge, LS0 unknown (N2(e)) | "Any worker/LS0/guard stop ⇒ no output" (code audit, class (iv)). |
| MA-PropP [IDX 70] | yes (Ẑ-weighted primary, M4) / yes / yes | author-only (METH-AUDIT) | Independent check of (ii), (iv). |
| PC1c3 [IDX 114] | yes / yes / yes | N1 premise for general h | Lemma N1 (C2(c)). |
| FMP-M1 [REG 570] | yes (every regime, frozen grid) / yes / islandwise | none | — |
| ADRAFT-ThmA [REG 372] | yes / yes / fixed R | Astra-only | Cite Del Moral 2004/2006 instead. |
| T22(i)(ii)(iv) [IDX 337] | yes (start unchanged, Outcome 2) / n/a / n/a | none | — |
| T27(i), Thm3/4-EXP [IDX 321–322, 339] | start law yes; iid draws (not the method's run) / n/a / n/a | about π₀, not delivery | none needed (used as start law only). |
| DIL-E [REG 709] | yes (any data and partition) / n/a / n/a | DIL-DM(i) ERROR | do not cite DM(i). |
| OWS-WS1–WS4, WS7 [REG 518–521, 529] | bridge law for any partition: yes / grid-free: yes / n/a | author-only, no review | Cross-family check of WS4(e) transfer; WS8(d) (actual particle system) OPEN, not used. |
| FD-W1 [REG 385] | yes (BO) | none | — |
| STG-G, T26BUD-G [IDX 255–257, 268] | yes (as-coded rule; ESS 0.90 pilot = grid as hypothesis) / yes / n/a | E's resolution caveat | Hypothesis: range/2⁶⁰ ≤ h/2 (bisection resolution). |
| STG-M [IDX 261] | n/a / **no** (ideal exact-frontier two-state grid) / n/a | as-coded masked T_n OPEN (Conjecture P) | None in paper 1; stated as ideal-grid law with T ≤ T_e as coded. |
| STG-L [IDX 258] | n/a / no (fine grid c → 0) / n/a | cited remark | — |
| OPW2-ThmA [REG 600] | yes (any invariant kernels, frozen 𝓒) / yes / islandwise | ideal-refresh clause not the method (OPW2-cex) | Never substitute; none needed. |
| MZ-E1E2, MZ-C1, MZ-P3 [IDX 184–185, 201] | yes (per fit; any grid; store with LS0 eviction, M2) / yes / n/a | candidates, not reviewed | Cross-family check of E1/E2. |
| N13, PC1c5 [INP 225] | yes (LS0 eviction rule 𝒯_new = top_c(…)) | none | — |
| TheoremA, LS-score, Lemma M [IDX 500, 508] | yes (v3 + LS0 = v3.1) / n/a / n/a | code bridge N2(c); e4 DP invariant N3 OPEN; ℓ ≥ Φ − 1 (N11) | Merged-LS0 replay; tie-DP invariant; N11 on LH (elementary). |
| T38-(0), Thm4-C1, N200 [IDX 527–528, 534] | yes (as run, every n) / yes / n/a | N200 author-only | Independent check of N200 Lemma 1. |
| T38-(a) [IDX 548] | **no** (iid final draws) / n/a / n/a | delivery under moves | none; stated as the iid-draw regime. |
| T38-b1-LH [IDX 438] | yes (v3 + LS0) / any grid / n/a | N2(c), N3 as above | as above. |
| B2E-B2LH, STAB-cert [IDX 439, 568] | **variant** (v3 without LS0) / any frozen grid / n/a | pending A-REV7 cross-family (C20) | none; stated as the no-LS0 corollary. |
| PART-ThmA [IDX 768] | yes (clustering rule) / n/a / n/a | LH-iid SIZE g ≤ B < 2g; study g = 5 uncovered (N8) | PART-pairing (OPEN) for 2g ≤ B. |
| T03♯, T01–T03 [IDX 151, 469] | target: algorithm-free | n ≳ 2·10⁶ onset | disclose. |
| MA-PropD, T32(i) [IDX 237, 242] | yes after LS0/extra-search terms and k* fix / yes / n/a | rate GAP; calibration share seat-derived | Re-count with LS0 terms; keep "polynomial". |
| MA-PropW/Wcal/CorWR, PC1c6 [IDX 92–94, 652] | code facts for v3.1 | W-cal not executed | Execute W-cal. |
| OCERT-LemmaM, C4 [IDX 744, 748] | yes (card R, POST HOC) / n/a / per record | fp label (N16) | none for exact arithmetic. |
| C1new [IDX 443] | (d) via T38-b1-LH: yes | PROOF SKETCH; numerics g = 1 | PIP → 0 lemma under SL's prior; re-run on LH g ≥ 2. |
| KL (Lemma KL) [IDX 369] | about (π, π₀): yes | author-only | check wave 1. |

## §H My list (ranked, ≤ 20)

| Rank | K-ID (lead; folded) | Name | Main / supplement | One-line reason |
|---|---|---|---|---|
| 1 | K20, K21, K08, K35, K46 (N1), K32, K86 | C2 VALID | main | Foundation of every identity; N1 is the binding §13.1 crux. |
| 2 | K51; K46, K52 | C5 H | main | Objective (1) and §13.1: joint inclusions and functionals; regime-free. |
| 3 | K77, K78, K36, K37, K85, K42 | C3 OUTPUT | main | The probability discipline (joint with output, R declared) a referee needs. |
| 4 | K102, K11, K10; K25, K27, K104 | C9 WS-ε | main | Binding §5.3 in its provable form; genuinely correlated IC3 family. |
| 5 | K43, K45, K95, K62 | C7 Z𝒯 | main | Deterministic two-sided TV/KL/PIP theorem for the reported posterior (§5.4). |
| 6 | K69, K70, K68, K45, K07 | C18 HPM | main | The output theorem on a masked correlated family for the shipped method. |
| 7 | K15–K18, K10 | C8 START | main | Strongest novelty; σ²-coupling term new; feeds §5.3 and depth. |
| 8 | K72 | C17 COMP | main | Only inequality non-vacuous at n = 200. |
| 9 | K48, K49, K50, K52, K54, K56 | C4 POOL | main | What islands buy; finite-R bound. |
| 10 | K26, K25, K27, K28, K29, K30, K31, K33 | C11 STG | main | Depth laws; coverage identity; Conjecture P stated OPEN. |
| 11 | K38–K42, K44, K53 | C6 Z | main | Evidence: what Ẑ can and cannot do, with mandatory wording. |
| 12 | K97 | C14 SL | main | The analytic separation from split-and-merge. |
| 13 | K19, K106, K105 | C10 SEP | main | Why one-shot correction fails; exp(KL) scale. |
| 14 | K65, K63, K64, K73, K74, K05, K14 | C16 REPAIR | main | Exact finite-n search theorem; certificates' semantics; Lean done. |
| 15 | K96 | C13 CD | main | Thesis theorem, scoped per E. |
| 16 | K87, K88, K89, K06, K64, K90 | C12 WORK | main | Objective (2) accounting; SL §6 comparison. |
| 17 | K93; K61, K94 | C15 SEL | main | Target consistency (MODEST, disclosed). |
| 18 | K01–K04, K44 | C1 TARGET | main | Propriety and invariances; Lean; cheap. |
| 19 | K83, K84, K86, K09, K76 | S1 PAR | supplement | Engineering premises of every claim about the study. |
| 20 | K104, K108 | S4 KL/TV lemmas | supplement | §5.4 calculus; feeds N16 later. |

Other supplements with cards (S2, S3, S5, S6) rank below 20.

## §I Questions for HQ

1. **§5.3 reading (binding).** The proposal's literal clause "the variance of importance weights remains bounded when cross-block dependence is sufficiently weak" is refuted for the shipped block-product start in its one-shot form (WS6(d): χ²(π‖π₀) → ∞ under ORTH with growing nulls; WS7: ESS_∞ → 0 under masking; both PROVED, author-only). Seat A proposes to meet §5.3 with C9 (bridge weights, relative to the block-orthogonal baseline, explicit in ε). Does HQ accept this reading, or does the literal one-shot form escalate to Felipe?
2. **§5.4 "credible-interval coverage error" (binding).** Seat A reads it as the Monte Carlo error of posterior credible intervals (delivered by C5(e) with declared CDF functionals, no method change: M9 admits them), not the frequentist coverage of the exact posterior's intervals, which is a target-theory question outside objectives (1)–(3) with no route. If HQ wants frequentist coverage, that is a new target and an escalation.

No method change is requested; no growth rate is needed by any card above (C5(d) carries R_n as an explicit hypothesis because the constant M is OPEN).