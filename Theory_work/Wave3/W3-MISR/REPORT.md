# W3-MISR — REPORT (C-MIS v2: the misspecified-subset theorem without fixed variances)

Lead: Claude Fable 5.2 (Claude Work, effort high). Branch `theory/W3-MISR`, base main 16a7f85. Ticket T1 of
`Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md`. This file is frozen with the round-R1 manifest; the council outcome
is therefore **not** recorded here but in `CHECKPOINT_2.md` and `reviews/` (both outside the manifest).

**RESULT (before the council).** STATEMENT v1.2 locked; every claim PROVED (by this seat, unchecked) and line-checked
by blind Sol reviewers with no open FATAL/MAJOR; conditional on the W3-POST2 inputs as listed per claim (§5).

## 1. What is proved (`STATEMENT.md` v1.2; proofs in `lemmas/`)

| claim | content | proof | status (verbatim, per claim) |
|---|---|---|---|
| Lemma R′ | (a) the coded posterior is invariant under y ↦ a1 + c·y, c ≠ 0; (a′) the parameter posterior is equivariant; (a″) code path pinned; (b) under a Gaussian contrast residual of any variance v > 0 the posterior has the law it has in a unit-noise well-specified model with coefficient β/√v; (c) only the law of the contrast direction matters, with a total-variation stability bound | `lemmas/R_reduction.md` | PROVED (by this seat, unchecked) |
| MIS-R (i) | fixed design: sup over the configuration class 𝒦_n of E[1 − π_𝒞(S₀^𝒞)] ≤ C·r_n for n ≥ n₀, constants free of the variance; rates for HPM, MPM, ξ_q, PIPs; proxies and cancellations | `lemmas/M_misr.md` M.1 | PROVED (by this seat, unchecked), conditional on W3-POST2:C |
| MIS-R (i′) | without a margin, in expectation: (a) no strict-superset mass; (b) strong coordinates included; (c) beta-min form; (d) localisation | `lemmas/M_misr.md` M.2 | PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 |
| MIS-R (ii) | random designs by conditioning: E[δ_n ∣ 𝓕_n] ≤ C r_n on the good event; design-measurable variance and coefficient; slices in s; tight constants | `lemmas/M_misr.md` M.3 | PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 |
| Corollary G(a) | jointly Gaussian rows give the contrast-law condition at each n, for any n-dependence of (m, Σ, β, σ²) | `lemmas/G_corollaries.md` G.1 | PROVED (by this seat, unchecked) |
| Corollary G(b) | Gaussian rows, 2 ≤ p_𝒞 ≤ n^A: E δ_n = O(r_n) under population conditions relative to σ²_𝒞 | G.2 | PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0 |
| Corollary H | in-sample Hellinger contraction of the parameter posterior around the projected law: rate log n/n without a margin, M_n/√n with selection (the Song–Liang Theorem 4 analog) | G.3 | PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C |
| Remark SNR | W3-POST Theorem 1 and W3-POST2 A1, B, C, D, E hold with n-dependent σ*² in signal-to-noise form | G.4 | PROVED (by this seat, unchecked), conditional on W3-POST2:A1, W3-POST2:B, W3-POST2:C, W3-POST2:D, W3-POST2:E |
| Remark P | C-MIS Theorem MIS (i), (ii), (ii′) and Theorem F hold in signal-to-noise form (every variance-dependent hypothesis relative; counterexample to the unnormalised BM-∞) | G.5 | PROVED (by this seat, unchecked) |
| Remark U | two representations in the class at the same law have the same support | G.6 | PROVED (by this seat, unchecked), conditional on W3-POST2:C |

Brief items: (a) Lemma R′ with the code check → R′(a), (a″), (b); (b) MIS(ii) → MIS-R (ii) (design-measurable variance,
tight constants, s-slices, uniform conclusion); (c) re-pointing to W3-POST2 (A1/E/C) → MIS-R (i), (i′), with the
expectation rate; (d) the remark on Theorem 1 → Remark SNR. Beyond the brief (each separately statused): Corollary H,
Remark P, and the two better-theorem adoptions R′(c) and MIS-R (i′)(d).

## 2. Review trail

| step | reviewer (model, provider, effort) | verdict | file | disposition |
|---|---|---|---|---|
| L01 statement lock, v1.0 | gpt-6.1-sol, codex, high, blind | **REJECT** — 0 FATAL / 1 MAJOR / 3 MINOR (MAJOR in Remark P: Theorem F's BM-∞ not normalised; no finding against R′, MIS-R, G, H) | `reviews/L01_statement_lock_sol.md` | all applied → v1.1 (`reviews/L01_disposition.md`) |
| L02 re-check of L01, v1.1 | gpt-6.1-sol, codex, high, fresh | **LOCK** — 0 / 0 / 0 / 0; findings 1–4 RESOLVED | `reviews/L02_statement_recheck_sol.md` | — |
| BT1 better theorem, v1.1 | gpt-6-astra, codex, high, blind | 3 class-A, 2 class-B proposals; an obstruction to dropping (E^σ) | `reviews/BT1_better_theorem_astra.md` | A1, A3 adopted → v1.2; A2, B1, B2 recommended as tickets (`reviews/BT1_disposition.md`) |
| K1 line check: R_reduction, M_misr (v1.2) | gpt-6.1-sol, codex, high, blind | 11 items VERIFIED, 3 VERIFIED-WITH-AMENDMENTS; 0 / 0 / 1 MINOR | `reviews/K1_RM_check_sol.md` | applied (`reviews/K_disposition.md`) |
| K2 line check: G_corollaries (v1.2) | gpt-6.1-sol, codex, high, blind | 10 items VERIFIED, 1 VERIFIED-WITH-AMENDMENTS; 0 / 0 / 2 MINOR | `reviews/K2_G_check_sol.md` | applied (`reviews/K_disposition.md`) |
| citation check | `citecheck.py` | 0 failures | `reviews/CITECHECK.txt` | — |
| council R1 | gpt-6.1-sol (codex, high) + Claude Opus 5.5 (Claude Work, high) | see `CHECKPOINT_2.md` | `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md` | see `CHECKPOINT_2.md` |

Layers. The ticket brief defines the legs as: statement lock, sharpness gate (assumption map, boundary numerics,
better-theorem review), lemma checks, council. The independent mid-point and the exhaustive sweep of the wave
protocol were not run as separate layers (the brief does not list them for this ticket; the reduction is short and
both line checks covered every clause). HQ to confirm or order them (PROTOCOL rule 14).
After-review edits not seen by L01/L02: the v1.2 additions (§1(c), §2 stability, §3(a) parenthesis, §3(d)) — covered
by K1 and the council. After K1/K2: the three MINOR amendments and one-line-per-claim status headers — covered by the
council, which reads the frozen manifest.

## 3. Numerics (falsification and boundary evidence only; never part of a proof)

| id | file | what | outcome |
|---|---|---|---|
| N0 | `numerics/N0_code_invariance.R` → `N0_out.txt` | compiled `v3_fit` on a + c·y (exact branch: 3 data sets × 7 transforms; SMC branch: 4 transforms, same seed) | status and HPM identical in 25 fits; max \|ΔPIP\| 1.304·10⁻¹⁰ |
| N1 | `numerics/misr_numerics.py` → `misr_numerics_out.txt` | residual variance v_n ∈ {n⁻², 1/n, 1, n, n²} with signal-to-noise held | common random numbers: posteriors agree to 5·10⁻¹⁴; independent draws: E δ/r_n ∈ [1.07, 1.42] in every regime |
| N2 | same | fixed raw coefficients, omitted column of variance n^{2a} | a = 0, 0.25: δ/r_n → 1.2; a ≥ 0.4 at these n: δ ≥ 0.98 — the margin must be relative to v |
| N3 | same | outside GR^c | t₃ residual: no effect; heteroscedastic within the design: δ/r_n 1.46 → 2.59; random slope: mean-only target fails, conditional target recovered |
| N4 | same | energy/(nv) ≍ n^b with all signals strong | conclusion holds |
| N5 | `numerics/N5_energy_obstruction.py` → `N5_out.txt` | p = 2 orthogonal, θ₁ = n, θ₂² = 200 log n/n | E π(S₀) = 0.87, 0.18, 0.04, 0.014, 0.007, 0.003 (n = 100 … 102400); = 1.0000 with θ₁ = 1 or √n — (E^σ) cannot be dropped |

## 4. Relations, strength, and what could be strengthened

- **Relation to C-MIS.** MIS-R (i) on 𝒦^λ_n with MIS-R (ii) gives the main clauses of C-MIS:Thm-MIS(i), (ii) (rate,
  PIPs, MPM, HPM) under their hypotheses ((F_w) ⇒ (OS) for large n; BM-∞ ⇒ (BM^σ; c) eventually; fixed σ²_𝒞 a special
  case), now in expectation and with any variance; their inclusion clause is recovered for c > c₁ by MIS-R (i′)(c),
  and for C-MIS's own range c > c₀ by Remark P. No `implies` edge is declared: the supersession decision is HQ's
  (LIFECYCLE §5.3), and Felipe's if C-MIS:Thm-MIS stays a headline.
- **Gap to Song–Liang §2.3 (registry note of C-MIS:Thm-MIS(i)).** "fixed τ²": removed. "no density contraction
  claimed": Corollary H gives an in-sample, in-probability Hellinger analog with a rate (not SL's integrated,
  almost-sure statement). Remaining: Gaussian contrast direction law; fixed s; p ≤ n^A (inherited).
- **Sharpness record** (`ASSUMPTION_MAP.md`): fixed variance — removed; GR^c — weakened to the direction law (R′(c));
  scalar covariance — needed for a named target (C-MIS E2, N3); margin — the relative form is the right one (N2),
  constant c₁ an artefact; (E^σ) — cannot be dropped (BT1 obstruction, N5), weakenable (N4); (F₀), (OS), fixed s,
  p ≤ n^A — inherited from W3-POST2.
- **Open / could be strengthened** (each with a disposition in `reviews/BT1_disposition.md`): BT1-A2 Corollary H in
  expectation with posterior-tail rates (upstream, W3-POST2:D); BT1-B1 the empty projection s = 0 at growing p (new
  lemma, upstream first); BT1-B2 a fresh-covariate Hellinger statement; a weaker energy condition; a non-Gaussian
  direction law.

## 5. Inputs and assurance (PROTOCOL rule 11)

Consumed, by registry id @ version (all ACTIVE on base main 16a7f85): W3-POST2:C@1.0.0, W3-POST2:E@1.0.0,
W3-POST2:A1@1.0.0, W3-POST2:A0@1.0.0, W3-POST2:D@1.1.0, W3-POST2:B@1.0.0 — registry status "PROVED (by this seat,
unchecked)", council C1 passed, PROVED-CHECKED per `Theory_work/Wave3/HQ_DECISIONS.md:48-49` but with no acceptance
record in the registry; therefore **declared hypotheses** here (statuses "conditional on …", edges `@hyp`), named in
`STATEMENT.md` §8. W3-POST:Thm-1@1.0.0 (Remark SNR), C-MIS:Prop-P@1.0.0, C-MIS:GD(b)@1.0.0 (Corollary G),
C-MIS:Thm-MIS(i)@1.0.0, C-MIS:Thm-MIS(ii)@1.0.0, C-MIS:Thm-F@1.0.0, C-MIS:Cor-F(a)@1.0.0, C-MIS:Cor-F(b)@1.0.0,
C-MIS:LemZ@1.0.0 (Remark P): council-passed (registry). MIS-R (i′) uses the W3-POST2 inputs through steps of their
proof files (Lemma C2, (G3′), (C5′)(a), (b), Lemma E1(b)), listed as (I1)–(I5) in `lemmas/M_misr.md` M.2.
Code pin: `Scripts/SMC_BVS/core/` at 16a7f85 (`v3_preprocess.R`, `v3_fit.R`, `v3_setup.R`, `cpp/v3_score.h`).
HOLDS.md was read before each step: empty throughout.

## 6. Files
`STATEMENT.md` (v1.2), `PLAN.md`, `LOG.md`, `ASSUMPTION_MAP.md`, `REPORT.md`, `CHECKPOINT_1.md`, `CHECKPOINT_2.md`;
`lemmas/R_reduction.md`, `M_misr.md`, `G_corollaries.md`; `numerics/` (table of §3); `citecheck.py` →
`reviews/CITECHECK.txt`; `reviews/` (briefs, reviews, dispositions, INPUTS.txt, MANIFEST_R1.txt).

## 7. Registry blocks (template `Theory_work/INFRA/templates/ASSUMPTION_MAP.md`)

The `council:` line and the `correct:` gate are left for HQ's CP3 step (`manifest.py bind` prints the cell; this
file is inside the frozen manifest and is not edited after the round).

```
REGISTRY
claim: W3-MISR:R' | kind: lemma | statement: STATEMENT.md:67-100 | premises: STATEMENT.md:16-39
status: PROVED (by this seat, unchecked) | status_source: lemmas/R_reduction.md:3
assumptions: A:MISR-GRC (new | contrast-law Gaussian residual | U'(y - x beta) ~ N(0, v I), any v > 0; weakened in part (c) to the law of the contrast direction | STATEMENT.md:33-39 | shared yes | bridge W3-MISR:R')
conclusion: identity: the coded posterior is invariant under affine maps of the response; under GR^c its law is that of a unit-noise G-model with coefficient beta/sqrt(v); total-variation stability in the law of the contrast direction | scope: every design, every n >= 3
gates: lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-A1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A1=adopted(reviews/BT1_disposition.md)

REGISTRY
claim: W3-MISR:MIS(i) | kind: theorem | statement: STATEMENT.md:104-117 | premises: STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C | status_source: lemmas/M_misr.md:4
assumptions: A:MISR-GRC ; A:MISR-ESNR (new | energy in signal-to-noise form | squared norm of mu at most n M v | STATEMENT.md:43 | shared no | bridge W3-MISR:R') ; A:MISR-IDM-SNR (new | ridge identifiability margin relative to v | L_S >= c v log n on bounded-excess underfits, c > c1 | STATEMENT.md:49-50 | shared no | bridge W3-MISR:R') ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: sup over the configuration class of E[1 - pi_C(S0^C)] <= C r_n, constants free of the residual variance; rates for HPM, MPM, PIPs | rate: r_n = sqrt(log n / n) | scope: fixed candidate design, 2 <= p_C <= n^A, s >= 1 fixed, any residual variance v_n > 0, law GR^c (or its direction-law form)
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp
sharpness: A:MISR-ESNR = WEAKENABLE (evidence: numerics/N5_out.txt:14) ; A:MISR-IDM-SNR = ARTEFACT (evidence: ASSUMPTION_MAP.md:18) ; A:MISR-GRC = WEAKENABLE (evidence: ASSUMPTION_MAP.md:13)
gates: lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-B1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B1=ticket(reviews/BT1_disposition.md)

REGISTRY
claim: W3-MISR:MIS(i') | kind: theorem | statement: STATEMENT.md:121-134 | premises: STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 | status_source: lemmas/M_misr.md:5
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: without a margin, expected posterior mass of strict supersets, of models missing a strong coordinate, and of models outside the small-loss neighbourhood of the target is at most C r_n | rate: r_n | scope: as W3-MISR:MIS(i), class without margin
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp ; W3-POST2:E@hyp ; W3-POST2:A1@hyp
gates: better-proposal:BT1-A3(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A3=adopted(reviews/BT1_disposition.md)

REGISTRY
claim: W3-MISR:MIS(ii) | kind: theorem | statement: STATEMENT.md:138-154 | premises: STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 | status_source: lemmas/M_misr.md:6
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:MISR-IDM-SNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E[delta_n | F_n] <= C r_n on the good event, uniformly; E delta_n <= C r_n + P(bad event); O_P(r_n) under tight constants; variance and coefficient measurable in the design | rate: r_n | scope: random candidate designs, any conditioning sigma-field, slices in s
depends_on: W3-MISR:MIS(i)@stmt ; W3-MISR:MIS(i')@stmt ; W3-MISR:R'@stmt

REGISTRY
claim: W3-MISR:Cor-G(a) | kind: corollary | statement: STATEMENT.md:158-164 | premises: STATEMENT.md:16-39
status: PROVED (by this seat, unchecked) | status_source: lemmas/G_corollaries.md:4
assumptions: A:IID-GAUSS-ROWS
conclusion: identity: jointly Gaussian rows give the contrast-law condition at each n, with deterministic projected coefficient and variance sigma^2 + tau^2, for any n-dependence of the parameters | scope: example (Gaussian rows)
depends_on: C-MIS:Prop-P@proof:gaussian-conditioning-at-one-n

REGISTRY
claim: W3-MISR:Cor-G(b) | kind: corollary | statement: STATEMENT.md:165-168 | premises: STATEMENT.md:158-159 ; STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0 | status_source: lemmas/G_corollaries.md:5
assumptions: A:IID-GAUSS-ROWS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E delta_n = O(r_n) under population conditions relative to the projected variance | rate: r_n | scope: example (Gaussian rows), 2 <= p_C <= n^A
depends_on: W3-MISR:Cor-G(a)@stmt ; W3-MISR:MIS(ii)@stmt ; C-MIS:GD(b)@proof:steps-1-2-5-and-failure-bound ; W3-POST2:A0@hyp

REGISTRY
claim: W3-MISR:Cor-H | kind: corollary | statement: STATEMENT.md:172-192 | premises: STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C | status_source: lemmas/G_corollaries.md:6
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: in-sample average Hellinger contraction of the parameter posterior around the projected law; log n / n without a margin, M_n / sqrt(n) with selection | rate: log n / n ; M_n / sqrt(n) | scope: fixed designs, arrays in the class; in probability
depends_on: W3-MISR:R'@stmt ; W3-MISR:MIS(i)@stmt ; W3-POST2:D@hyp
gates: better-proposal:BT1-A2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A2=ticket(reviews/BT1_disposition.md) ; better-proposal:BT1-B2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B2=ticket(reviews/BT1_disposition.md)

REGISTRY
claim: W3-MISR:Rem-SNR | kind: remark | statement: STATEMENT.md:195-200 | premises: STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:A1, W3-POST2:B, W3-POST2:C, W3-POST2:D, W3-POST2:E | status_source: lemmas/G_corollaries.md:7
conclusion: posterior: W3-POST Theorem 1 and W3-POST2 A1, B, C, D, E hold with n-dependent noise variance in signal-to-noise form | scope: as the transferred claims
depends_on: W3-MISR:R'@stmt ; W3-POST:Thm-1@stmt ; W3-POST2:A1@hyp ; W3-POST2:B@hyp ; W3-POST2:C@hyp ; W3-POST2:D@hyp ; W3-POST2:E@hyp

REGISTRY
claim: W3-MISR:Rem-P | kind: remark | statement: STATEMENT.md:201-209 | premises: STATEMENT.md:16-39
status: PROVED (by this seat, unchecked) | status_source: lemmas/G_corollaries.md:8
conclusion: posterior: C-MIS Theorem MIS (i), (ii), (ii') and Theorem F hold with any positive variance when every variance-dependent hypothesis is relative; the unnormalised BM-infinity of Theorem F does not suffice (counterexample) | scope: as the transferred claims
depends_on: W3-MISR:R'@stmt ; C-MIS:Thm-MIS(i)@stmt ; C-MIS:Thm-MIS(ii)@stmt ; C-MIS:Thm-F@stmt ; C-MIS:Cor-F(a)@stmt ; C-MIS:Cor-F(b)@stmt ; C-MIS:LemZ@stmt

REGISTRY
claim: W3-MISR:Rem-U | kind: remark | statement: STATEMENT.md:210-212 | premises: STATEMENT.md:16-63 ; STATEMENT.md:214-224
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C | status_source: lemmas/G_corollaries.md:9
conclusion: target: two representations in the class at the same law have the same support | scope: n >= n0 with C r_n < 1/2
depends_on: W3-MISR:MIS(i)@stmt
```
