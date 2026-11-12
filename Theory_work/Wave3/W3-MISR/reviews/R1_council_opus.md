# R1 — council review, seat `opus` (Claude Opus 5.5, effort high; blind first read)

Package: `Theory_work/Wave3/W3-MISR/` at HEAD 2f360ed ("freeze MANIFEST_R1 (d3f5c91f...)"); `git status` shows no change
to any package file (only the other seat's untracked review, which I did not open). I did not read the manifest file
itself (it sits under `reviews/`), so the binding to the digest is through that commit. Files read: STATEMENT v1.2,
`lemmas/R_reduction.md`, `M_misr.md`, `G_corollaries.md`, ASSUMPTION_MAP, `numerics/*_out.txt` (and the N0 script header),
`reviews/CITECHECK.txt` (174 checks, 0 failures). Sources opened and checked line by line where the package relies on them:
[W3P] STATEMENT 1-100; [POST2] STATEMENT 1-140; `C_expectation.md` 1-66; `E_visibility.md` 1-90; `A_occam.md` 8-90;
`D_hellinger.md` 1-20, 44-75; [MIS1] STATEMENT 1-145; `L2_gaussian.md` 38-106; `L1_reduction.md` 67-75;
`L5_frontier.md` 78-89; [P3] lines 35-42, 179, 194, 199-203, 225-230, 304-346; [T03R] 185-198; the T03 statement's
conclusion (v); `INFRA/registry/claims.tsv` rows of every cited input; `HQ_DECISIONS.md:46-50`; code `v3_preprocess.R:1-132`,
`v3_fit.R:85-135`, `v3_setup.R:1-25`, `cpp/v3_score.h:10-72, 194-228`, plus a grep of `core/` for raw-scale metadata.

## Gate verdicts

| gate | verdict | reason (evidence below) |
|---|---|---|
| 1 Correctness | **PASS** | Every step re-derived; no error found. R′(a): y′ = sgn(c)·y and both quadratic forms are even (R_reduction.md:18-22). R′(a′): Π^std unchanged, s_y ↦ c·s_y (R.2, consistent with [POST2]:101-103). R′(b): Uᵀy^r = Uᵀxβ + √v W, (R1)+(R2) give Φ(x, Uᵀxβ/√v + W), same law as the unit-noise model (R.4). R′(c): y = √N Uz/‖z‖, yᵀBy = N tr(UᵀBU·T), Q_S linear in T, Q_S ≥ 0 since nXH⁻¹Xᵀ ⪯ I; TV inequality standard (R.5). MIS-R (i) is exactly [POST2] Claim C (iii)/(ii) at σ*² = 1 ([C]:9-15 per-n form verified). (i′)(a)/(b)/(d): I re-did the decompositions and the expectation arithmetic (n^{−1/2} ≤ r_n for n ≥ 3; e^{−N/8} ≤ 8/N; 5/n; the 2^{s₀} grouping; (I4)'s second inequality for the j > j₀ part); the (d) decomposition is correct and indeed does not need Lemma E0 at the decomposition level (E0 is still used inside (I5)). (i′)(c): Δ_S ≥ λ_min(G_{S′})‖θ_{S₀∖S}‖² ≥ Nφ₀²θ_j² ≥ (N/n)c″v log n ≥ cv log n. (ii): freezing lemma, Borel strata, Markov, slices, η-argument all correct. G(a), G(b) (each step against [L2]:88-105), H(a)/(b) (bijection T_{1/√v_n}, Hellinger scale invariance), reference-law paragraph, SNR, P (table rows against [MIS1]:124-141; counterexample: ‖μ_c/t‖² = (n−1)/n² → 0, TV → 0, Lemma Z), U: all correct. |
| 2 Hypotheses used = stated | **PASS** | Table R.6 is an exact per-n dictionary ([POST2]:25, 29-36, 40-42; [W3P]:63-75 verified). Claim C's "at that n" form is used as given ([C]:9-15). (I1)-(I6) hypotheses match their sources ([C]:31-42; [A]:46-74; [E]:23-54; [T03R] (C6)(a)); the K1-1 standing-assumption paragraph handles R1's asymptotic wording correctly. (ID^{M,σ}_j) ≡ [POST2]:42. G(b) population conditions deliver every member of 𝒦^λ_n incl. (F_w; 1) ⇒ (OS) via A0(iii) ([A]:14-27). D(a)/(b) used in R1 with σ*² = 1 as stated ([POST2]:107-116). One presentation issue on (OS) in §3(a): F5. |
| 3 No hidden assumptions | **PASS** | Measurability (strata, Borel classes), p random (disjoint union), non-constancy (a.s. under GR^c; assumed under (PR)), non-uniqueness of β (explicit), tie rules (any; {HPM ≠ S₀} ⊆ {δ ≥ ½} for every rule), σ² = 0 (G needs only σ²_𝒞 > 0), intercept (only contrasts matter), floating point (excluded) are all handled. Only a cosmetic a.s.-definition gap (F7). |
| 4 Cited inputs | **PASS (with MINOR fixes)** | W3-POST2 registry rows verified: all "PROVED (by this seat, unchecked)", ACTIVE, C1 council; D@1.1.0; HQ_DECISIONS.md:48-49 does record PROVED-CHECKED. Lemma-file "conditional on" lines match what each proof consumes (I traced each: (i) → C; (i′) → C (Lemma C2, thresholds), A1 ((G3′), (C5′)), E (E1); G(b) → +A0; H → D, C; SNR → A1, B, C, D, E; U → C). Nothing upgraded. But the C-MIS statuses are paraphrased, not verbatim, and several consumed inputs are missing from §8 (F1, F2). |
| 5 Constants / rates / thresholds | **PASS** | Constants are those of Claim C at σ*² = 1 and do not involve v; n₀′ = max of the internal thresholds of Claim C (iii) (depending on (s, A, M, φ₀, C_OS, c)), of 16 and of e^{ρ_n} ≤ 2 with ρ_n = 8(M + 1)/(Nφ₀²) ([P3]:201 at σ*² = 1); C′_a, C′_b, C′_d depend on (s, M, φ₀, C_OS). c″ ≥ cn/(n−1) is exactly what (N/n)c″ ≥ c needs. C_H = 8(C_A(s + j₀) + c₁ + 1) + 1 at unit variance depends on (s, A) only ([D]:D3). G(b)'s bad events 2n⁻² + 2k_n n⁻² + n⁻¹, k_n = O(log n). c₀ depends on (s, A) only (C_* of [P3]:194). |
| 6 Fidelity to the code | **PASS** | Verified at 72785fe: `v3_fit.R:97` → `v3_preprocess`; `v3_preprocess.R:123-127` stores `y = sy$z` and raw-scale metadata; `v3_fit.R:110, 118` pass only `pre$y` to timing and context; `v3_score.h:14` a0 = b0 = 0.01; `:55-60` z, yty, ν, log C_n, logm0 from standardised y; `:217-223` Q = yty − n·quad, logm. Exact/SMC branch from (n, p) only (`v3_budgets`); the `q_nonneg` switch at `:219` is relative to yty = N (invariant). grep confirms `s_y`, `y_max`, `y_mean`, `y_sd_scaled` occur only at `v3_preprocess.R:126-127`. N0 description verified (25 runs, 3×7 + 4, all same status/HPM, max |ΔPIP| 1.304e-10 exact, 1.037e-11 SMC). Small completeness points: F6, F11. |

Overclaim check. Relative to SL §2.3: STATEMENT §3(c) and §6 state their differences honestly (in-sample, in probability,
fixed design, shipped prior, s fixed); ASSUMPTION_MAP's "inclusion without a margin" is loose (F9). Relative to [MIS1]: the
"Implies" paragraph (STATEMENT.md:228-231) is correct ((F_w) ⇒ (OS) by A0, BM-∞ ⇒ BM^σ(c) eventually, inclusion via §3(c)
for c > c₁ after a c₁ < c′ < c squeeze, and via Remark P for c₀ < c ≤ c₁). "Not claimed" is honest; one item is asserted
as fact without proof (F3). Clauses weaker than they look: the TV stability term (F4); Remark U (F10).

## Findings

**F1 — MINOR (gate 4). Statuses of C-MIS inputs not verbatim.** STATEMENT.md:7-8 says inherited statuses are quoted verbatim
in §8, but STATEMENT.md:223-224 summarises six C-MIS rows as "council R07/R08 PASS (registry)". The registry strings
differ per row, e.g. `C-MIS:Thm-MIS(ii)` "R02 VERIFIED-WITH-AMENDMENTS (applied); council PASS"; `C-MIS:Thm-F`
"R03 (xhigh) VERIFIED / V-W-A (applied); pathwise inequalities corroborated by numerics/check_L4.py (no violation);
council PASS"; `C-MIS:LemZ` "R05 VERIFIED / V-W-A (applied); council PASS". Nothing is upgraded, but the rule is broken.
*Fix:* quote each C-MIS row's `status` field verbatim (one line per id).

**F2 — MINOR (gate 4). §8 input list is incomplete.** (a) Remark P transfers C-MIS Corollary F(a), Corollary F(b) and
therefore Lemma T (STATEMENT.md:207-208 "Corollary F(b)'s (TL) is unchanged"; G_corollaries.md:145-147 "Theorem F,
Corollary F(a), F(b) apply"), but `C-MIS:Cor-F(a)`, `C-MIS:Cor-F(b)`, `C-MIS:Lemma-T` are not listed. (b) §9 makes a claim
about `C-MIS:Cor-H` ("whose first term now has the rate 2C r_n", STATEMENT.md:242) without listing it. (c) The lemma-level
inputs [T03R] (C6)(a) and [P3] `eq:ratio`, `lem:signal` (M_misr.md:50, 71-72, 110-111) are locked and need no
conditionality, but they belong in the consumes list (e.g. via `W3-POST:Thm-1`, which §8 restricts to "Remark SNR only").
(d) STATEMENT.md:219's "conditional on … (as applicable)" list omits W3-POST2:B and W3-POST2:A0, which do occur in the
SNR and G(b) status lines; STATEMENT.md:11's alias list omits `B_tail_approx.md`. *Fix:* add the rows/ids; widen the
W3-POST:Thm-1 row's scope; list all six W3-POST2 ids in the conditional sentence.

**F3 — MINOR (gate 1, honesty of "Not claimed"). The (E^σ) obstruction is asserted as a fact without proof.**
STATEMENT.md:239-241: "with p = 2 orthogonal columns, θ₁ = n and θ₂² = c·log n/n the other hypotheses hold and
π_𝒞(S₀) → 0", supported only by N5 (finite n ≤ 102400) and by a review file. I believe it (heuristic: the g = n ridge
shrinkage of the dominant coefficient leaves Q_{1}, Q_{12} ≍ 1 on the standardised scale, so the log-likelihood gain of
column 2 is ν·O(log n/n²) = O(log n/n) → 0 while its Occam/prior factor is ≍ (2p)n^{−1/2}; hence π({1}) → 1), but a statement
file must not present an unproved limit as established. *Fix:* label it "(numerical, N5, with the heuristic above; not
proved)", or add the four-line proof to `G_corollaries.md`.

**F4 — MINOR (weaker than it looks). The total-variation stability term is non-vanishing for ordinary non-Gaussian
errors.** STATEMENT.md:110-111 ("an approximate (PR) costs its total-variation error") and §9 New (9) (STATEMENT.md:237)
invite reading R′(c) as a robustness result. For iid non-Gaussian residuals (e.g. N3(i)'s t₃) the laws of the contrast
direction separate as N → ∞ (the statistic N·Σ_i u_i⁴ with u = z/‖z‖ has different limits, or diverges for t₃), so
d_TV(Law T(y^r), Law T_G(κ)) → 1 and the bound says nothing; R′(c) is useful essentially for exact (PR) (random units,
as in the example). *Fix:* one sentence after the example: "For iid non-Gaussian residuals the TV term does not vanish
as n → ∞; R′(c) is an exact-invariance extension (e.g. random units), not a robustness bound."

**F5 — MINOR (gate 2). The BT1-A3 trim of §3(a) is announced but not formally stated.** STATEMENT.md:7 says v1.2
"trims the hypothesis of §3(a)", but §3(a) is still quantified over κ ∈ 𝒦⁰_n (full (OS), both inequalities); only a
parenthetical (STATEMENT.md:123-124) says the clause "uses only the first inequality". The proof supports the trimmed
claim (M_misr.md:86-87: (I1)-(I4) with j₁ = 0 only; (I5), hence c, is not used by (a)), but as written the registry
would record the untrimmed hypothesis. *Fix:* define 𝒦⁰′_n := 𝒦⁰_n with (OS) replaced by 𝒪_n^{>0} ≤ C_OS r_n and state
(a) for κ ∈ 𝒦⁰′_n, with its threshold free of c.

**F6 — NIT (gate 6).** STATEMENT.md:77 describes `v3_standardise` as "centre, divide by the sample SD"; the function first
divides by max|y| and has an anchored two-pass branch whose trigger `max(abs(x2)) <= sqrt(.Machine$double.eps)`
(`v3_preprocess.R:47`) depends on the raw shift a. It is neutral in real arithmetic (R_reduction.md:44 says so), and the
anchored branch stores further raw-scale metadata (`centering$anchor` etc., `v3_preprocess.R:62-64, 129-130`, copied into
`fit$preprocessing` at `v3_fit.R:98`) that R.3's grep list does not mention; none reaches a score. *Fix:* one clause in
(a″) and R.3.

**F7 — NIT (gate 3).** G_corollaries.md:32-33: κ_n is a configuration only on the probability-one event that all
candidate columns are non-constant, whereas §4 (STATEMENT.md:138-139) requires an 𝓕_n-measurable random configuration.
*Fix:* set κ_n to a fixed reference configuration off that null event (or allow a.s.-defined κ_n in §4).

**F8 — NIT.** STATEMENT.md:38-39: "[MIS1]'s GR … implies GR^c … for any σ², τ² ≥ 0 with σ² + τ² > 0" — [MIS1]'s GR has
σ² > 0 and τ² fixed ([MIS1]:49, 55). *Fix:* "GR with arbitrary (n-dependent) σ², τ² ≥ 0, σ² + τ² > 0, implies GR^c …".

**F9 — NIT (SL comparison).** ASSUMPTION_MAP.md:44 "Ours: stronger conclusion (… inclusion without a margin …)": the
ticket's inclusion is of J^M_n (coordinate margin) or, with (F_λ), of a relative beta-min set (§3(b)-(c)); SL's Corollary 2
covers all of s̃ without beta-min in their fixed-parameter regime. STATEMENT §3(c) is accurate. *Fix:* "inclusion of every
coordinate with a coordinate margin, without the global margin".

**F10 — NIT (weaker than it looks).** Remark U (STATEMENT.md:210-212): two GR^c representations of one law have equal
Gaussian contrast laws, hence v = v′ and μ(κ) = μ(κ′); U is therefore a statement about distinct coefficient vectors with
the same centred mean. *Fix:* say so in one clause.

**F11 — NIT (numerical observation).** In N0 the SMC data set and exact data set 12 have HPM = ∅ (`N0_out.txt:43`, data 12),
so half of the HPM-invariance observations are on null results. Described correctly in STATEMENT.md:82-85; a non-empty-HPM
SMC case would make the observation more informative.

**F12 — NIT.** M_misr.md:89-101 uses j both for the fixed coordinate and for the summation index of Ξ_j. Rename one.

**F13 — NIT (sharpness).** Corollary G(b)'s "n·min_j Σ_jj(β^𝒞_j)²/(σ²_𝒞 log n) → ∞" (STATEMENT.md:167) is stronger than
the proof uses: step 4 (G_corollaries.md:52-54) needs only liminf ≥ 2(c₀ + 1)/φ₀² = 16C₀(c₀(s, A) + 1)/c_pop. Stating the
fixed-constant form would give a sharper corollary at no cost.

Counts: FATAL 0, MAJOR 0, MINOR 5 (F1-F5), NIT 8 (F6-F13).

## Overall

A clean, well-sourced package. The key idea (exact invariance under y ↦ a1 + cy, then a per-n reduction in law to the
unit-noise G-model) is correct and exactly matches the code's real-arithmetic target. The transfers inherit W3-POST2's
per-n constants faithfully. The (i′) expectation assemblies and the conditional random-design form are correct, and
they add value beyond [MIS1]. The findings are bookkeeping (F1, F2), labelling (F3, F5) and one honesty sentence about the
reach of R′(c) (F4). None affects a proof.

**Score: 8.7 / 10.** All six gates PASS on this content.

COUNCIL-VERDICT round=R1 manifest=d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d seat=opus score=8.7 gates=PASS
