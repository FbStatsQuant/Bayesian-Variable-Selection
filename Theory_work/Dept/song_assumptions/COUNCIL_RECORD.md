# COUNCIL RECORD — TH-SONG-ASSUMPTIONS

Council: Opus 5.5 (claude-opus-5-5, effort high), Neon (gemini-4-neon, thought_level high) and Sol (gpt-6.2-sol, reasoningEffort high).
Bar: every assumption scores ≥ 8.5 on D and R, with no open blockers, in at most 3 rounds. Nitpicks are declined with a one-line reason, and any score penalty driven only by nitpicks is disregarded.

## Pre-council advisor rounds (context)
- **DESIGN_MEMO_R0** → Astra R1 and Fable R1, run independently. Both converged on:
  - the selection margin with a width allowance;
  - dropping the eigenvalue floors;
  - the BB(1, p^u) correction.
- **Astra R2** reviewed the integrated draft and made five substantive corrections, all applied in v1.1 (commit 5b62aaa9):
  - TD′ becomes a high-risk conjecture;
  - A-MARGIN-U is restated in the R2 form;
  - the converse needs A-NEC on T and gives liminf ≥ Φ(−c);
  - the finite-n companion is withdrawn and becomes a diagnostic;
  - SUBG does not imply SL Condition 3, so A-MARGIN-H supplies R;
  - TM-a0 now has one fixed law and uses E[Z_j²u²];
  - A-BS′ is recorded but not adopted.

## Round 1 (package v1.1, commit 5b62aaa9; dispatched 2026-11-27)
Seat reports: `council/R1_SOL.md` (7.5/10), `council/R1_NEON.md` (7.5/10), `council/R1_OPUS.md` (7.0/10). All three judged the SL map complete by coverage, with qualification fixes needed.

### Scores (D / R per assumption)
| assumption | Sol | Neon | Opus | min | < 8.5? |
|---|---|---|---|---|---|
| A-GL | 8.5 / 9 | 9 / 8 | 9 / 9 | 8 | R (Neon: scope, exponent typo) |
| A-SPARSE | 8.5 / 9 | 7 / 9 | 9 / 9 | 7 | D (Neon: Thm 4, SC11, growth overclaim) |
| A-DIM | 8.5 / 9 | 9 / 9 | 9 / 8 | 8 | R (Opus) |
| A-DIM′ (conj.) | 8 / 4 | 9 / 3 | 8 / 5 | 3 | R, by construction (conjecture with a failed route; see note) |
| A-SUBG | 7.5 / 8.5 | 7 / 9 | 7 / 8 | 7 | D (bounded ⇒ SUBG false) |
| A-NEC | 7 / 8.5 | 5 / 8 | 7 / 7 | 5 | D (dominance claims; Neon blocker), R (size lemma omitted) |
| A-BS | 8.5 / 9 | 8 / 7 | 8 / 8 | 7 | R (YWJ/SC11 growth caveat) |
| A-BS′ (not adopted) | 8 / 6.5 | (with A-BS) | (with A-BS) | 6.5 | R, by construction (recorded, not adopted) |
| A-MARGIN-H | 7.5 / 8.5 | 9 / 6 | 8 / 8 | 6 | R (window q_n → min(K, J)); D (E2 label) |
| A-MARGIN-U | 7 / 7.5 | 8 / 6 | 6 / 5 | 5 | D, R (blockers below) |
| A-MIS(iii) | 7.5 / 9 | 7 / 8 | 8 / 8 | 7 | D (rank; E7 scope; Rossell) |
| A-MOM | 8.5 / 8 | 9 / 10 | 8 / 8 | 8 | R (p_C ≥ 2, prior, domain) |

Note on A-DIM′ and A-BS′. These are *weaker alternatives evaluated under the anti-stringency rule* and are labelled as a high-risk conjecture and as "recorded, not adopted". No released target depends on them. Their low R score reflects that labelled status, not a defect to fix; the bar of ≥ 8.5 applies to the assumptions the targets use.

### Blockers (4 distinct; all addressed in v1.2)
| # | seat | blocker | v1.2 disposition |
|---|---|---|---|
| B-1 | Neon B1, Opus B1(i) | A-MARGIN-U binds on classes with B_Dm ≤ 0 (needs √R ≥ w + t_n for no reason); C unnamed | **Fixed.** Imposed only on nonempty classes with D ≠ ∅, m ≤ J, B_Dm > 0. B_Dm ≤ 0 classes are dispatched by the containing-model credit (TS-b step 3). Active m ≤ m*(d). C is named as the superset-step truncation constant. Files: ASSUMPTIONS §2, §3.3 step 3, §4 row 11; DEFINITIONS TS-b; DOSSIER. |
| B-2 | Opus B1(ii)–(iii) | Worst-case width and squared forms fail on S1 at SNR 2; evidence covers only m = 0 | **Fixed.** Both forms are labelled worst-case (factor-proxy) forms that do not cover S1 at SNR 2, and the Opus arithmetic is quoted. New **E9** Monte Carlo of the conditional width on simulated S1 designs (no fits; ≈ 2 CPU-min, nice, single thread): w_Dm(X) = 0.10–0.47 (m = 1), 0.22–0.59 (m = 2); the surplus is ≥ 3.29 at SNR 2 and ≥ 6.7 at SNR 3 for every d = 1, m ≤ 2 class (m = 2 at p = 500 only; corrected in R2); d ≥ 2 mixed and m = 3 are marked not evaluated. The design-event quantifier for w_Dm(X) is stated. |
| B-3 | Neon B2 (+ Opus S5, Sol 6) | A-NEC "weaker than every precedent"; SL (26) called "fixed-type" | **Fixed.** Rewritten as a comparison of object, scale and window, not dominance: SBJ A4 and NH14 4.5 use the minimum nonzero sample eigenvalue (they allow duplicates; NH14's p^{−κ} can be smaller); SL (26) is a vanishing two-sided sample condition. ASSUMPTIONS, DOSSIER and the DEFINITIONS SL-6/7 row are all corrected. |
| B-4 | Sol 1 | Raw-unit map and input domain; TM-a0 admits p_C = 1; prior convention | **Fixed.** Raw-unit map β_j = s_y b_j/s_{x_j}, σ² = s_y² v (DEFINITIONS §1). Undefined posteriors are counted in the exceptional event. TM-a0/A-MOM: p_C ≥ 2, fixed coded BB(1, p_C) eventually untruncated, coded centring, exceptional event a.s. eventually empty. |
| B-5 | Sol 2 | TS-b\* has no testable statement | **Fixed by demotion.** It is now "MARGIN\* (open refinement)" and is removed from the defined targets (DEFINITIONS §4.2, ASSUMPTIONS §2 and §6, DOSSIER weak points). |

### Substantive points (all adopted)
| seat / # | point | v1.2 fix |
|---|---|---|
| Sol 3 | constants and localisation hierarchy; "polynomial" coarse count; testing budget does not absorb it; (s+1) in A-DIM′ | ζ, q_n(M), C_q defined; TD hierarchy (coarse window with isometry, then localisation to J, then testing) in ASSUMPTIONS A-DIM and §3.1 and DOSSIER A-DIM; A-DIM′ uses (s+1); E6 labelled "finite-n ratios" |
| Neon 7 | A-DIM′ degenerates at s = 0 | (s+1) (same fix) |
| Sol 4 / Neon 8 | exact coded score, Fubini for the fixed-endpoint contrast density; determinant exponent; A-GL scope excludes TM-a0 | A-GL rewritten; scope "TD, TS, TM-a/b (not TM-a0)" in the score card |
| Sol 5 / Neon 3 / Opus S4 | bounded predictors do not imply relative A-SUBG; SL Cond 1 is absolute-scale; two-sided isometry on (s0+J)-sets | counterexample added; "same type, different normalisation"; two-sided isometry |
| Sol 6 | "TS-b contains" delivered results; TM-b rate vs the delivered expectation bound | "previously delivered analogue"; the rate difference is stated |
| Opus S6 | A-NEC used by prop:dist(i) and the TD tests | added to "Used in" (ii); the "no floor" claim is scoped to step 1 |
| Sol 7 / Neon 4 | A-MARGIN-H over min(K, J), not q_n; fresh c′_H; E2 is a restricted-search scale diagnostic | adopted in all four files |
| Opus S7 | E2 d_H² formula is the τ = σ affinity (an upper bound) | relabelled in the SIMULATION table and the ASSUMPTIONS defence |
| Sol 8 | fixed M, integer J, empty classes omitted, design event; Q_U − RSS_U = O_P(σ²); truncated-Beta superset bound; finite union | TS-b intro and steps 2–4; §6 item 3 obligations at fixed M |
| Sol 9 / Neon 6 / Opus S3 | 9/10,666 (not 9/11,466 or ≤ 0.0008); "necessary direction is exact"; P1 price one off; price(s0) is smaller; E K₁ 0.031–0.050 (χ²) vs 0.033–0.056 (exact Beta); 39/41 one-null | corrected everywhere; "consistent with"; price note rewritten (Sol's correction); E K₁ attributions fixed |
| Opus S2 | E K₁ does not match the order of the rate term (factor ≍ L); TS-b mass bound uninformative at S1 | "matches the order" deleted from all files; stated as a mode-type diagnostic |
| Opus S8 | data κ vs theorem κ_n (≤ ~1.4% on S1); call the S1 numbers κ_multi | added to SIMULATION (price note) and ASSUMPTIONS A-MARGIN-U (b) |
| Sol 10 / Neon 9(b)(c) | Σ_CC nonsingular; omission-only; E7 is in-sample on the selected MPM; 2.97% cell; (i′) suggested; Rossell fixed-design; GvO does not establish our threshold; discrete-y note moved to A-MOM | adopted in ASSUMPTIONS A-MIS/A-MOM, DOSSIER and the SIMULATION E7 reading |
| Neon 5 | A-SPARSE: SL Thm 4 does not use (4); drop SC11; hedge the growing-s0 claim | adopted (ASSUMPTIONS, DOSSIER) |
| Neon 9(a) | YWJ/SC11 bounds grow with g / φ_n | caveat added (ASSUMPTIONS, DOSSIER) |
| Sol 11 | map qualifications: SL-3/4 partial analogues; SL-5 threshold; Thm 4 premises; split A-MOM defence; Wainwright/FRG scope | adopted in the DEFINITIONS §3 rows and A-MOM |
| Sol 12 | other priors: what can and cannot break; g = max(n, p²) price ≈ 2 log p only when p² ≥ n; plain-English rate wording | adopted in DEFINITIONS §5, ASSUMPTIONS §5 and §4.1 plain English |

### Nitpicks (no score effect; one-line disposition each)
| seat / # | nitpick | disposition |
|---|---|---|
| Sol N1 / Neon N1 / Opus N1 | version strings out of sync | adopted (cheap): all four files now v1.2 |
| Sol N2 / Opus N12 | give SLs Lemma 1.2 its own SL-map row | **declined**: its role is already catalogued inside the SL-8 row, and a separate row would duplicate it without changing any mapping |
| Neon N2 | ζ undefined in A-SUBG | adopted (cheap) |
| Neon N3 | price_n undefined | adopted (cheap): notation line in ASSUMPTIONS and DEFINITIONS |
| Neon N4 / Opus N2 | "Medians over settings" caption | adopted (cheap): "Ranges (min–max)" |
| Neon N5 | TD-as M ≥ M₀ on a common probability space; asm:omitted line | adopted (cheap) |
| Neon N6 | TM-a0 p_C ≥ 2, n ≥ 2p_C | adopted; folded into blocker B-4 |
| Neon N7 | distinguish fixed-design vs random-pair precedents in A-GL | adopted (cheap) |
| Opus N3 | κ_del population row vs P1 sample row mixed in synthesis 2 | adopted (cheap): rows separated |
| Opus N4 | "8.8–250× c_ψ/n" presumes c_ψ = 1 | adopted (cheap): "n × floor = 8.8–250; slack relative to c_ψ/n is this divided by c_ψ" |
| Opus N5 | price range "7.5–10" should be 7.3–10.4 | adopted in part: set to 7.6–10.4, the table range `e1_margin_by_setting.tsv` (7.60–10.36), which Sol checked independently; 7.3 is not in any table |
| Opus N6 | ε_n is P2's √(s0 log p/n), not the TD radius | adopted (cheap): labelled in E2 |
| Opus N7 | Jiang (2007) page and GLM scope | adopted (cheap) |
| Opus N8 | YWJ quote elided | adopted (cheap): full quote restored |
| Opus N9 | TM-a0 "intercept" means coded centring | adopted (cheap) |
| Opus N10 | name C | adopted; folded into blocker B-1 |
| Opus N11 | stale filename `SIMULATION_DATA_ANALYSIS_draft.md`; COUNCIL_RECORD missing | filename fixed; COUNCIL_RECORD now exists (moot) |
| Opus N13 | state the design-event quantifier for w_Dm(X) | adopted; folded into blocker B-2 |

No penalty was driven only by nitpicks: every sub-8.5 score above is tied by its seat to a blocker or substantive point.

### Lead errors caught by the council (for the owner)
v1.1 contained seven over-claims by the Lead, all now withdrawn:
- the testing budget absorbs the coarse count;
- bounded predictors imply A-SUBG;
- A-NEC dominates its precedents;
- "9 of 11,466 on S2";
- E K₁ attributed to the χ² formula and said to "match the order" of the rate term;
- "TS-b contains" the delivered results;
- TS-b\* listed as a target.

### Round 1 outcome
The package was revised to v1.2. Round 2 is dispatched to the same three seats with `briefs/COUNCIL_BRIEF_R2.md`.

### HQ owner ruling (POLICIES §1b, received 2026-11-27 after R2 dispatch)
Round 2+ is **scoped fix-verification**, not a cold re-review. The R2 seats were already running under the fuller R2 brief. Per POLICIES §10 they are not cancelled; the ruling is applied at triage:
- The R2 gate is cleared iff (a) every R1 blocker and substantive point is judged genuinely fixed, and (b) no new substantive flaw or regression was introduced by the v1.2 edits.
- New points that are not regressions of a v1.2 edit, and all new stylistic nitpicks, are logged with a one-line reason and disregarded for the gate. So are score penalties driven by them.
- Point-by-point response: `council/RESPONSE_R1.md`. Diff: `council/R1_TO_R2.diff`. Any Round 3 uses the scoped brief `briefs/COUNCIL_BRIEF_R3_SCOPED.md`.

## Round 2 (package v1.2, commit 7c7ca30f; seats ran under the fuller R2 brief, triaged under POLICIES §1b)

### Scores
| seat | overall | lowest D/R | R1 blockers | new blockers |
|---|---|---|---|---|
| Neon (gemini-4-neon, high) | 9.0 | A-NEC D 8.5; A-MARGIN-U 8.5/8.5 | B-1…B-5 resolved | 0 (4 minor substantive) |
| Opus (claude-opus-5-5, high) | 8.6 | A-NEC D 8.5; A-MARGIN-U 8.5/8.5 | B-1…B-5 resolved | 0 (S-1…S-3) |
| Sol (gpt-6.2-sol, high) | 8.0 | A-MARGIN-U 7.5/8; A-NEC D 8 | B-1, B-4, B-5 resolved; **B-2, B-3 not resolved** | 1 (step-3 rate bound) |

Per-assumption tables: `council/R2_<SEAT>.md` §1.

### Gate (§1b)
**Not cleared.** (a) Sol judges B-2 (E9 scope over-stated) and B-3 (leftover "smaller than each" sentence) partially fixed; Neon S1/S3 and Opus S-2/S-3 flag the same two passages. (b) The step-3 log-odds display introduced in the B-1 fix drops −γ log n (all three seats) and, per Sol, uses a quadratic that is not an upper bound for residuals of order n. These are genuine regressions/partial fixes of v1.2 edits, so they count for the gate.

Override (Manager ruling: Astra 6.2 + Fable 5.2 judges if the last round finds nothing substantive yet scores < 8): **not triggered** — R2 is not the last round, and it found substantive issues. Logged here; no extra judges spawned.

### Triage of R2 points (all fixed in v1.3 unless stated)
| seat / # | point | gate-relevant? | disposition |
|---|---|---|---|
| Sol 1 / Neon S2 / Opus S-1 | step 3: B_Dm includes +γ log n; quadratic not an upper bound for large residuals | yes (regression) | step 3 rewritten in Sol's coded-likelihood form: H_Dm = B_Dm − γ log n, W = (min √λ̂_S − w_Dm − t_n)₊², log Σ odds ≤ H_Dm − (n/2+a₀)log(1+W/V_n) + O_P(1), V_n = n(1+o_P(1)); B ≤ 0 → W = 0; B > 0 → monotonicity at W = 2(1+δ)B_Dm; U through size s0+J, capped by p; C defined as a fixed constant with a tight multiplier. Linearisation paragraph aligned |
| Sol 2 / Neon S3 / Opus S-3 | E9 scope: zero-slack diagnostic, mean widths, C = 1; m = 2 only at p = 500; m ≥ 3 (and m = 4 at p = 5,000) active; d ≥ 2; C ≍ (s0+1)² | yes (B-2 partial) | all four files now say "estimated zero-slack diagnostic"; scope and not-evaluated list (m = 2 at p = 5,000, m ≥ 3, d ≥ 4) everywhere the evidence is summarised; cap m*(d) labelled asymptotic, C ≈ 121 at S1 sizes. New **E9b** (`scripts/e9b_width_mc_ext.py`, `tables/e9b_width_ext_s1.tsv`, 108 rows): d = 1–3, m = 1 (all cells) and m = 2 (p = 500), 3 binding D each; SNR 2 min surplus 2.39 (C = 121) / 2.49 (no credit), d = 2, 3 ≥ 3.6; SNR 3 ≥ 5.8. Agrees with Opus's independent rerun. "Uncorrelated far nulls" replaced by Sol's AR(1) Markov argument (the 40-null search contains an exact minimiser) |
| Sol 4 / Neon S1 / Opus S-2 | A-NEC "smaller than each" contradicts the NH14 caveat; SL (26) lower/upper thresholds; NH14/SBJ wording | yes (B-3 partial) | blanket sentence replaced by "No blanket ordering" in ASSUMPTIONS, DOSSIER and DEFINITIONS SL-6/7; SL (26) described with a vanishing lower and growing upper threshold; NH14 allows exact dependence; SBJ ν_{k*} indexed through min(n, \|k\|) |
| Sol 3 | exact all-deletion κ_n (1,023 D): 0.626–0.693 / 2.505–2.771, gaps 1.1–1.7%; 40/41 & 39/41; E K₁ is an HPM event | yes (fixes the v1.2 "≤ ~1.4%" note) | exact κ_n quoted (Lead reproduced it) in SIMULATION, ASSUMPTIONS, DOSSIER, DEFINITIONS converse; data κ kept as the restricted proxy; counts and HPM wording fixed |
| Neon S4 / Sol 7 (part) | thm:omitted "special case" | yes (stale v1.2 text against a v1.2 fix) | "previously delivered analogue" in ASSUMPTIONS §3.5 and DEFINITIONS SL-9 row |
| Sol 5 | TD′ exact conjecture, (s+1), TS-b′ undefined, "stretched-exponential", TD-A variance proxy | partly (v1.2 TD′/A-DIM′ edits) | adopted: exact display with q_n = min{p, ⌈C′(s+1)M log(p∨n)⌉}, tail exp(−cM log(p∨n)), M range; TS-b′ removed; centred-tail variance proxy |
| Sol 6 | b₀ coded vs raw; A-BS fixed-endpoint bound; raw p on the centring event; ν(dx)dy; candidate-set rule; rank relaxation | partly (candidate rule was weakened in a v1.2 edit) | all adopted (cheap) |
| Sol 7 (rest) | SL-0 EBIC qualification; s0 = 0 / TM-b nonempty pseudo-support; form-invariance qualification | no (unchanged text) — adopted anyway, cheap | adopted in DEFINITIONS SL-0, TM-b, §5 and ASSUMPTIONS §§3.5, 5 |
| Sol 8 | rounding (6.696, SD 0.1208, 1.175); 9/136 is the residual ratio; fixed-variance Hellinger max 0.21; min(p, s0+J) ≤ q_n | partly | all adopted |
| Neon N1 / Opus N1, N2 | E9 table rounding (3.29, 0.10, 6.696) | nitpick | adopted (cheap) |
| Neon N2 / Opus N5 | TD′ (s+1); "uniform summation" vs finite union | nitpick | adopted (cheap) |
| Neon N3 | §5 data-free-slab cell | nitpick | adopted (cheap) |
| Neon N4 | b₀ units blend | nitpick | adopted (with Sol 6) |
| Neon N5 | A-MOM score-card row | nitpick | adopted (cheap) |
| Opus N3 | "(choosing a smaller number is not enough)" unclear | nitpick | adopted (cheap) |
| Opus N4 | E9 mechanism is generic, w_D1 ≈ (log p)/√n | nitpick | adopted as a one-line note in the E9 reading |
| Opus N6 | COUNCIL_RECORD B-2 row "d = 1, m ≤ 2" | nitpick | adopted (row corrected above) |
| Sol nitpick | casing of "E K₁"/"HPM" | nitpick | adopted where touched; no other change |

No R2 point was declined. Score penalties: Sol's A-MARGIN-U 7.5 and A-NEC 8 tie to Sol 1/2/4 (gate-relevant); none are nitpick-driven.

### Lead errors caught in R2 (for the owner)
- step-3 accounting (+γ log n kept; quadratic in place of the coded likelihood);
- "smaller than each" left in after the NH14 caveat;
- the C = 1 "m ≤ 3" example presented as describing S1;
- E9 coverage over-stated ("d = 1, m ≤ 2" on all of S1; actual m = 2 at p = 500 only);
- "uncorrelated far nulls" (AR(1) correlations are nonzero; the Markov property is the right reason);
- "≤ ~1.4%" (exact gaps up to 1.7%);
- rounding of 3.30 / 6.7 / 1.17;
- thm:omitted "special case".

### Round 2 outcome
Package revised to v1.3. Response: `council/RESPONSE_R2.md`. Diff: `council/R2_TO_R3.diff`. Round 3 (last allowed) is scoped fix-verification with `briefs/COUNCIL_BRIEF_R3_SCOPED.md`.

### HQ owner ruling (2026-11-27, after v1.3 push): Round 2 accepted as PASSED
- The owner accepts Council R2 as **passed as-is**: Neon 9.0, Opus 8.6, Sol 8.0. The 8.5 threshold is explicitly waived for Sol ("let's leave it like that").
- The v1.3 fixes above, already applied when the ruling arrived, stand as the final cleanups.
- **No Round 3, and no Astra + Fable override judges.**
  - The three scoped R3 seats had already been dispatched (commit 4bacc09d) before the ruling arrived. Per POLICIES §10 they are not cancelled.
  - When their `council/R3_<SEAT>.md` files arrive, they will be filed as **superseded / informational**. They are not a gate.
- **Gate status: PASSED (owner ruling).** The package is held at v1.3 pending one final theory idea from the owner.

### Round 3 reports (superseded / informational; filed under POLICIES §10)
`council/R3_OPUS.md`, `council/R3_NEON.md`, `council/R3_SOL.md` arrived after the owner ruling. They are filed as superseded and are not a gate. All three returned NOT CLEAR, on the same small set of v1.3 one-line edits that RESPONSE_R2 had claimed but not made. The mathematics was rated sound. The missed edits were:
- the D4 overclaim "margin holds there";
- DOSSIER "SBJ allows duplicates";
- DOSSIER "ordinary correlated designs";
- upward-rounded E9b minima;
- TD′ q_n without min{p, …}.

All five are folded into v1.4 (below). **Lead error:** claiming fixes in RESPONSE_R2 that were not applied. Since then, every claimed fix is grep-checked before it is reported.

## Owner final theory order: Senior Completeness, Generality & Naturalness Review (2026-11-27/28)
**Mandate (owner, via the Manager).** Two fresh senior judges, Fable 5.2 (claude-fable-5-2, effort high) and Astra 6.2 (gpt-6.2-astra, reasoning high), audit completeness and, as the owner's top priority, generality and naturalness. Every assumption must be stated design-agnostically for general high-dimensional linear-regression BVS: no AR(1), no S1/S2 structures or constants in any statement. S1/S2 belong only in the evidence. **Round cap:** one discussion round; a second only with prior Manager approval. It was not needed and not requested.

### Stage 1: independent audit (`briefs/SENIOR_REVIEW_BRIEF.md`)
| judge | completeness | generality/naturalness | readiness | file |
|---|---|---|---|---|
| Fable 5.2 | 7.5 | 6.0 | 6.5 | `council/SENIOR_FABLE.md` |
| Astra 6.2 | 8 | 7 | 7 | `council/SENIOR_ASTRA.md` |

The common core of both reports:
- (i) A-MARGIN-U's headline used a design-conditional width w_Dm(X) and a proof-defined constant C. It read as engineered and carried S1 numbers inside the statement. Both judges asked for a **population-only headline**.
- (ii) S1/S2 numbers and the AR(1) design appeared inside statements and decision rationales (D4, the TS-b statement, "C ≈ 121").
- (iii) Missing SL counterparts:
  - SL (3) → A-BS;
  - the SL p. 951 cap remark → q_n;
  - SL Condition 3's Gaussian form → A-NEC;
  - prop:dist(ii) and thm:dist-param;
  - the itemwise TS-a;
  - the SL Cor 2 inclusion counterpart.
- (iv) The TM tier needed a primitive form, a pseudo-true sparsity label and a statement conditional on C.
- (v) Windows were stated through proof constants.
- (vi) The converse needed its minimal set.
- (vii) The worked cases promised in the dossier were missing.

### Stage 2: Proposers' response (one round)
- **Lead proposal:** `council/SENIOR_PROPOSAL_LEAD.md`, with §0 (12 points both judges agree on) and §1 (the merged A-MARGIN-U population form, questions Q1–Q5).
- **Drafting advisors:** `advisors/SENIOR_RESPONSE_FABLE.md` and `advisors/SENIOR_RESPONSE_ASTRA.md`. Both answered within the single round.
- **Converged canonical text:** `council/V14_CHANGESPEC.md`.

**Lead-proposal errors caught by the advisors** (all corrected in the spec):
- the price ratio was inverted (log[π(T∖D)/π(T)], not its reciprocal);
- the coefficient a was uncapped: ā = min{1, ·}, and the fallback coefficient is 1, not √2;
- slack was mixed between scales (the root-scale form was adopted);
- the proposal wrongly said the population form implies the v1.3 class-level conditional-width form. It implies only the **base-indexed** form, so step 3 is run per base and the class-level form is kept as a parallel sufficient condition;
- the rival range should use m̄_d with total added size k, not m̄ with m;
- the windows wording would have shrunk the delivered thm:dist range (fixed by k_n ≥ q_n(M), with q_n(M_n) for varying M).

**Settled design questions:**
- Q2: Astra's geometric coefficient ā, with √ϑ ≤ ā ≤ √(2ϑ) as a reading aid.
- Q3: A-MARGIN-H as a diverging ratio for every fixed k, with a fixed-level remark.
- Q4: the A-BS′ recorded pair (V = O(1), E = o(1)), with V = O(1) as the open target.
- Weaker variant (proxies pay their own price): a remark, not adopted.

### v1.4 changes (commit 3ee24ea9; diff `council/V14_DIFF.diff`)
- **A-MARGIN-U, population form:**
  - (U1) deletions, κ_n ≥ 1+η;
  - (U2a) bases inside a deterministic accounting set Q_n ⊇ T with log|Q_n| = o(log n);
  - (U2b) outside nulls priced by their leakage ϑ through ā;
  - special cases Q_n = T, vanishing leakage, and the ā ≡ 1 fallback;
  - corollaries C-i (strong separation) and C-ii (sparse eigenvalue plus beta-min);
  - Lemma W (W1–W3) as the bridge to the proof.

  The v1.3 form is kept as the refined design-conditional form, with C = 1 by convention. The "C ≍ (s0+1)² ≈ 121" claim is withdrawn, and C = 121 is a sensitivity setting.
- **No S1/S2 number or design family appears in any statement.** D4 is rewritten on generality grounds.
- **Statement changes:**
  - A-MARGIN-H is now a diverging ratio;
  - the windows are k_n ≥ q_n(M);
  - A-NEC is n·φ_min(k_n) ≥ c_ψ;
  - A-DIM′ is log p = o(√n), with the product form as the proof budget;
  - A-BS′ is the recorded pair plus the open target;
  - A-MIS(iii) has its primitive form;
  - new A-SPARSE-C;
  - TM-a and TM-b are conditional on each admissible C;
  - new target TM-a0-inc, the SL Cor 2 counterpart;
  - the converse uses its minimal set and records the boundary remainder;
  - the sieve is s − d + k ≤ min(K, J).
- **SL map additions:** SL (3); the p. 951 cap remark; the SL Condition 3 Gaussian form; prop:dist(ii) and thm:dist-param; TS-a per predictor; TM-a0-inc for SL-9.
- **Package structure:**
  - four assumption blocks (Model / Design / Signal / Omitted variables);
  - DOSSIER worked cases for orthogonal, AR(1), block and equicorrelation/one-factor designs, checked numerically in `.rc_tmp/lead_v14/worked_cases.py`;
  - TS-b proof path: step 3 is run per base; the k > m̄_d step is an explicit obligation; 3′ is the refined route.
- **Evidence:**
  - U2a check: the minimum over D and ≤ 2 inside proxies equals the exact κ_n, 2.505–2.771 at SNR 2 (`.rc_tmp/lead_v14/u2a_check.py`);
  - AR(1) leakage decay: 0.265, 0.087, 0.030, 0.011;
  - the fallback ā ≡ 1 fails at SNR 2 (minimum −0.692) and holds at SNR 3 (minimum 1.412) on the evaluated classes only;
  - E9/E9b are qualified as diagnostics of the refined form (selected D, four designs, zero slack);
  - E9b is rerun with the raw-centred mean (v1 kept as `_v1_codedmu`; Δ ≤ 0.0015), and all minima are exact (2.3862, not ≥ 2.39);
  - E2, E7 and E1 readings are qualified.
- **R3 leftovers fixed:** D4; DOSSIER SBJ and NH14 split; "ordinary correlated designs"; TD′ min{p, …}; §3.2 step 2 min(p, s0 + J); "every m ≤ J active" withdrawn.
- **Edits by:** the Lead made DEFINITIONS and ASSUMPTIONS. A Sonnet 5.5 worker made DOSSIER and SIMULATION (`briefs/V14_WORKER_BRIEF.md`), and the Lead reviewed its diff.
- **Lead errors caught during application:**
  - the E9 minima were first quoted from E9b (E9 is 3.2946 / 6.6961);
  - "fallback holds at SNR 3" was stated without its coverage, and is now qualified;
  - one "≥ 3.29" was rounded up in the DOSSIER.

### Engine decision (HQ FYI; SMC-PERF closed, memo 1b319090)
v3.1.1, g = n, truncated BB(1, p) and MPM are confirmed. Fix E (output-only) and C1 (compute-only) do not touch the theorems. Proof writing and Lean stay on HOLD. This is recorded in DEFINITIONS §1 and §5, in ASSUMPTIONS header and §5 (the sensitivity table is now a contingency note, with no row triggered), and in the DOSSIER.

### Stage 2 sign-off (Final Council, single pass; `briefs/SENIOR_SIGNOFF_BRIEF.md`)
PENDING
