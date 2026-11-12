# W3-MISR — CHECKPOINT 3 (final), 2026-11-12

Lead: Claude Fable 5.2 (Claude Work, high). Branch `theory/W3-MISR`. The run ends here.

## Outcome: CP3-PASS candidate (HQ's acceptance audit pending)
- **Council R2 PASSED** on `MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103` (`reviews/MANIFEST_R2.txt`;
  STATEMENT v1.3): sol **9.2**, opus **8.9**, six gates PASS in both, 0 FATAL / 0 MAJOR. `manifest.py bind`: OK;
  `manifest.py verify`: OK on the final tree. Council cell:
  `R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)`
- Before it (HQ's CP2 decision): council R1 PASSED on v1.2 (sol 9.3, opus 8.7; manifest d3f5c91f…); exhaustive sweep
  SW1 (Astra, blind, same manifest): 0 FATAL / 0 MAJOR / 8 MINOR / 1 NIT, one item classed substantive by the sweeper
  (the premise description of numerics N5 used a false constant comparison). All R1 and SW1 items were applied in one
  batch → v1.3 (`reviews/R1_SW1_disposition.md`; one optional strengthening, R1-F13, not applied). Because of the
  sweeper's classification, the short council re-round R2 (both seats, blind, diff-first) replaced the Sol
  "editorial only" diff check, as HQ ordered. Mid-point layer: waived by HQ.
- Both R2 seats checked the whole diff v1.2 → v1.3: every changed line correct; the only change of form to a claim is
  §3(a), now stated over the class 𝒦⁰′_n (first (OS) inequality only) that its proof uses.

## What is proved and checked (`STATEMENT.md` v1.3; proofs `lemmas/`)
Lemma R′ (exact invariance of the coded posterior under affine maps of the response; code path pinned at 16a7f85 and
run; reduction to a unit-noise model; direction-law form); Theorem MIS-R (i) (uniform expectation rate C·√(log n/n),
constants free of the variance), (i′) (no-margin clauses), (ii) (random designs by conditioning); Corollaries G, H;
Remarks SNR, P, U. Statuses stay verbatim "PROVED (by this seat, unchecked), conditional on W3-POST2:…": the checked
label is HQ's, after the acceptance audit and the acceptance record of the W3-POST2 inputs.

## Open items from council R2 (not applied: the content is frozen; all wording)
| # | seat | grade | item | proposed fix |
|---|---|---|---|---|
| R2-opus-F1 | opus | MINOR | §3(a) re-uses κ inside a sentence already quantified over κ and does not name its own threshold | give (a) its own "for n ≥ n₁ᵃ and every κ ∈ 𝒦⁰′_n" with its constant (the proof M.2(a) has both) |
| R2-opus-F2 | opus | MINOR | §8 quotes the statuses of SOP:TH128 and SOP:TH09 by their opening words (labelled "status beginning"); the omitted text has an onset-gloss ERROR flag and a same-family-only flag | quote the two statuses in full |
| R2-sol-1 | sol | MINOR | ASSUMPTION_MAP rows still say (E^σ) "cannot be dropped", "confirmed by N5", "the conclusion fails", "needed in some form" — stronger than STATEMENT §9's "numerical, with an analytic sketch" | use the §9 wording in the three places |
| R2-sol-2 | sol | NIT | N5 docstring line 10 still contains "with c = 200 > c_1" inside the sentence about the control arms | reword to "with c = 200 (which is below c_1(2, 1))" |
| R2-opus-F3–F5 | opus | NIT | a citation for "none of these involves c"; "no conclusion changed" understates the §3(a) change; N5 does not say why c₀(2, 1) = 192 | one clause each |
These need one more editorial pass plus a Sol "editorial only" diff check (PROTOCOL rule 15) if HQ wants them in
before acceptance; none affects a gate.

## For HQ's acceptance audit
- `manifest.py bind reviews/MANIFEST_R2.txt reviews/R2_council_sol.md reviews/R2_council_opus.md` → OK (cell above).
- Registry blocks below = `REPORT.md` §7 plus the `council:` line and the `correct:` gate (REPORT.md is inside the
  manifest and was not edited after the round). `ingest.py convert CHECKPOINT_3.md`: 10 claims, 0 problems.
- Inputs W3-POST2:A0/A1/B/C/D/E are declared hypotheses (`@hyp`; statuses "conditional on …"); they need an acceptance
  record before any checked label. C-MIS supersession and tickets BT1-A2, B1, B2: with HQ, as decided.
- Line endings: the ticket folder was re-checked-out before each freeze, so the frozen hashes are those of a fresh
  Windows checkout (autocrlf); a checkout with LF endings will not verify.
- Agents in the whole run: Sol ×7 (L01, L02, K1, K2, council R1, council R2 — codex, high), Astra ×2 (BT1, SW1 — codex,
  high), Opus 5.5 ×2 (council R1, R2 — Claude Work, high; one extra launch died on the rate limit). No Claude Personal.
  HOLDS.md empty at every step.

## Registry blocks (final; template `Theory_work/INFRA/templates/ASSUMPTION_MAP.md`)

```
REGISTRY
claim: W3-MISR:R' | kind: lemma | statement: STATEMENT.md:70-106 | premises: STATEMENT.md:17-43
status: PROVED (by this seat, unchecked) | status_source: lemmas/R_reduction.md:3
assumptions: A:MISR-GRC (new | contrast-law Gaussian residual | U'(y - x beta) ~ N(0, v I), any v > 0; weakened in part (c) to the law of the contrast direction | STATEMENT.md:36-43 | shared yes | bridge W3-MISR:R')
conclusion: identity: the coded posterior is invariant under affine maps of the response; under GR^c its law is that of a unit-noise G-model with coefficient beta/sqrt(v); total-variation stability in the law of the contrast direction | scope: every design, every n >= 3
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-A1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A1=adopted(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(i) | kind: theorem | statement: STATEMENT.md:110-123 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C | status_source: lemmas/M_misr.md:4
assumptions: A:MISR-GRC ; A:MISR-ESNR (new | energy in signal-to-noise form | squared norm of mu at most n M v | STATEMENT.md:47 | shared no | bridge W3-MISR:R') ; A:MISR-IDM-SNR (new | ridge identifiability margin relative to v | L_S >= c v log n on bounded-excess underfits, c > c1 | STATEMENT.md:53-54 | shared no | bridge W3-MISR:R') ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: sup over the configuration class of E[1 - pi_C(S0^C)] <= C r_n, constants free of the residual variance; rates for HPM, MPM, PIPs | rate: r_n = sqrt(log n / n) | scope: fixed candidate design, 2 <= p_C <= n^A, s >= 1 fixed, any residual variance v_n > 0, law GR^c (or its direction-law form)
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp
sharpness: A:MISR-ESNR = WEAKENABLE (evidence: numerics/N5_out.txt:14) ; A:MISR-IDM-SNR = ARTEFACT (evidence: ASSUMPTION_MAP.md:20) ; A:MISR-GRC = WEAKENABLE (evidence: ASSUMPTION_MAP.md:15)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-B1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B1=ticket(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(i') | kind: theorem | statement: STATEMENT.md:127-140 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 | status_source: lemmas/M_misr.md:5
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: without a margin, expected posterior mass of strict supersets, of models missing a strong coordinate, and of models outside the small-loss neighbourhood of the target is at most C r_n | rate: r_n | scope: as W3-MISR:MIS(i), class without margin
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp ; W3-POST2:E@hyp ; W3-POST2:A1@hyp ; SOP:TH128@proof:C6a ; SOP:TH09@proof:P3-ratio-supsum-signal
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT1-A3(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A3=adopted(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(ii) | kind: theorem | statement: STATEMENT.md:144-160 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1 | status_source: lemmas/M_misr.md:6
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:MISR-IDM-SNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E[delta_n | F_n] <= C r_n on the good event, uniformly; E delta_n <= C r_n + P(bad event); O_P(r_n) under tight constants; variance and coefficient measurable in the design | rate: r_n | scope: random candidate designs, any conditioning sigma-field, slices in s
depends_on: W3-MISR:MIS(i)@stmt ; W3-MISR:MIS(i')@stmt ; W3-MISR:R'@stmt
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-G(a) | kind: corollary | statement: STATEMENT.md:164-170 | premises: STATEMENT.md:17-43
status: PROVED (by this seat, unchecked) | status_source: lemmas/G_corollaries.md:4
assumptions: A:IID-GAUSS-ROWS
conclusion: identity: jointly Gaussian rows give the contrast-law condition at each n, with deterministic projected coefficient and variance sigma^2 + tau^2, for any n-dependence of the parameters | scope: example (Gaussian rows)
depends_on: C-MIS:Prop-P@proof:gaussian-conditioning-at-one-n
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-G(b) | kind: corollary | statement: STATEMENT.md:171-174 | premises: STATEMENT.md:164-165 ; STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0 | status_source: lemmas/G_corollaries.md:5
assumptions: A:IID-GAUSS-ROWS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E delta_n = O(r_n) under population conditions relative to the projected variance | rate: r_n | scope: example (Gaussian rows), 2 <= p_C <= n^A
depends_on: W3-MISR:Cor-G(a)@stmt ; W3-MISR:MIS(ii)@stmt ; C-MIS:GD(b)@proof:steps-1-2-5-and-failure-bound ; W3-POST2:A0@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-H | kind: corollary | statement: STATEMENT.md:178-197 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C | status_source: lemmas/G_corollaries.md:6
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: in-sample average Hellinger contraction of the parameter posterior around the projected law; squared distance at rate log n / n without a margin, distance at rate M_n / sqrt(n) with selection | rate: squared Hellinger distance log n / n ; Hellinger distance M_n / sqrt(n) | scope: fixed designs, arrays in the class; in probability
depends_on: W3-MISR:R'@stmt ; W3-MISR:MIS(i)@stmt ; W3-POST2:D@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT1-A2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A2=ticket(reviews/BT1_disposition.md) ; better-proposal:BT1-B2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B2=ticket(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Rem-SNR | kind: remark | statement: STATEMENT.md:201-206 | premises: STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:A1, W3-POST2:B, W3-POST2:C, W3-POST2:D, W3-POST2:E | status_source: lemmas/G_corollaries.md:7
conclusion: posterior: W3-POST Theorem 1 and W3-POST2 A1, B, C, D, E hold with n-dependent noise variance in signal-to-noise form | scope: as the transferred claims
depends_on: W3-MISR:R'@stmt ; W3-POST:Thm-1@stmt ; W3-POST2:A1@hyp ; W3-POST2:B@hyp ; W3-POST2:C@hyp ; W3-POST2:D@hyp ; W3-POST2:E@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Rem-P | kind: remark | statement: STATEMENT.md:207-215 | premises: STATEMENT.md:17-43
status: PROVED (by this seat, unchecked) | status_source: lemmas/G_corollaries.md:8
conclusion: posterior: C-MIS Theorem MIS (i), (ii), (ii') and Theorem F hold with any positive variance when every variance-dependent hypothesis is relative; the unnormalised BM-infinity of Theorem F does not suffice (counterexample) | scope: as the transferred claims
depends_on: W3-MISR:R'@stmt ; C-MIS:Thm-MIS(i)@stmt ; C-MIS:Thm-MIS(ii)@stmt ; C-MIS:Thm-F@stmt ; C-MIS:Cor-F(a)@stmt ; C-MIS:Cor-F(b)@stmt ; C-MIS:Lemma-T@stmt ; C-MIS:LemZ@stmt
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Rem-U | kind: remark | statement: STATEMENT.md:216-220 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C | status_source: lemmas/G_corollaries.md:9
conclusion: target: two representations in the class at the same law have the same support | scope: n >= n0 with C r_n < 1/2
depends_on: W3-MISR:MIS(i)@stmt
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
```
