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
| B-2 | Opus B1(ii)–(iii) | Worst-case width and squared forms fail on S1 at SNR 2; evidence covers only m = 0 | **Fixed.** Both forms are labelled worst-case (factor-proxy) forms that do not cover S1 at SNR 2, and the Opus arithmetic is quoted. New **E9** Monte Carlo of the conditional width on simulated S1 designs (no fits; ≈ 2 CPU-min, nice, single thread): w_Dm(X) = 0.10–0.47 (m = 1), 0.22–0.59 (m = 2); the surplus is ≥ 3.29 at SNR 2 and ≥ 6.7 at SNR 3 for every d = 1 class; d ≥ 2 mixed and m = 3 are marked not evaluated. The design-event quantifier for w_Dm(X) is stated. |
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
