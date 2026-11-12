# W3-MISR — CHECKPOINT 4: HQ acceptance record (2026-11-12)

HQ decision 2026-11-12 (PROTOCOL rules 10, 11; INFRA R05 safeguard 1: the ticket's own checkpoint is the status
source). Council cell: `R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)`.
Both seats accepted every claim below in their dated per-claim addenda (R06 rule; no rescoring). Nothing in the
frozen manifest changed. REGISTRY blocks: CHECKPOINT_3.md § Registry blocks, with the status (this file) and the HQ-decided edits only.

Status lines (one per claim; status text, then the claim id):

PROVED-CHECKED; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:R'
PROVED-CHECKED, conditional on W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:MIS(i)
PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; input versions SOP:TH09@1.0.0, SOP:TH128@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:MIS(i')
PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; input versions SOP:TH09@1.0.0, SOP:TH128@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:MIS(ii)
PROVED-CHECKED, conditional on C-MIS:Prop-P; input versions C-MIS:Prop-P@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:Cor-G(a)
PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09, SOP:TH128, C-MIS:GDb; input versions C-MIS:Prop-P@1.0.0, SOP:TH09@1.0.0, SOP:TH128@1.0.0, C-MIS:GD(b)@1.0.0 (C-MIS:GDb = alias of C-MIS:GD(b)); council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:Cor-G(b)
PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) — W3-MISR:Cor-H

## Registry blocks

```
REGISTRY
claim: W3-MISR:R' | kind: lemma | statement: STATEMENT.md:70-106 | premises: STATEMENT.md:17-43
status: PROVED-CHECKED; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:10
assumptions: A:MISR-GRC (new | contrast-law Gaussian residual | U'(y - x beta) ~ N(0, v I), any v > 0; weakened in part (c) to the law of the contrast direction | STATEMENT.md:36-43 | shared yes | bridge W3-MISR:R')
conclusion: identity: the coded posterior is invariant under affine maps of the response; under GR^c its law is that of a unit-noise G-model with coefficient beta/sqrt(v); total-variation stability in the law of the contrast direction | scope: every design, every n >= 3
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-A1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A1=adopted(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(i) | kind: theorem | statement: STATEMENT.md:110-123 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:11
assumptions: A:MISR-GRC ; A:MISR-ESNR (new | energy in signal-to-noise form | squared norm of mu at most n M v | STATEMENT.md:47 | shared no | bridge W3-MISR:R') ; A:MISR-IDM-SNR (new | ridge identifiability margin relative to v | L_S >= c v log n on bounded-excess underfits, c > c1 | STATEMENT.md:53-54 | shared no | bridge W3-MISR:R') ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: sup over the configuration class of E[1 - pi_C(S0^C)] <= C r_n, constants free of the residual variance; rates for HPM, MPM, PIPs | rate: r_n = sqrt(log n / n) | scope: fixed candidate design, 2 <= p_C <= n^A, s >= 1 fixed, any residual variance v_n > 0, law GR^c (or its direction-law form)
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp
sharpness: A:MISR-ESNR = WEAKENABLE (evidence: numerics/N5_out.txt:14) ; A:MISR-IDM-SNR = ARTEFACT (evidence: ASSUMPTION_MAP.md:20) ; A:MISR-GRC = WEAKENABLE (evidence: ASSUMPTION_MAP.md:15)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; lit:PARTIAL(ASSUMPTION_MAP.md) ; necessity:PARTIAL(ASSUMPTION_MAP.md) ; better-proposal:BT1-B1(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B1=ticket(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(i') | kind: theorem | statement: STATEMENT.md:127-140 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; input versions SOP:TH09@1.0.0, SOP:TH128@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:12
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: without a margin, expected posterior mass of strict supersets, of models missing a strong coordinate, and of models outside the small-loss neighbourhood of the target is at most C r_n | rate: r_n | scope: as W3-MISR:MIS(i), class without margin
depends_on: W3-MISR:R'@stmt ; W3-POST2:C@hyp ; W3-POST2:E@hyp ; W3-POST2:A1@hyp ; SOP:TH128@hyp ; SOP:TH09@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT1-A3(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A3=adopted(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:MIS(ii) | kind: theorem | statement: STATEMENT.md:144-160 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128; input versions SOP:TH09@1.0.0, SOP:TH128@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:13
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:MISR-IDM-SNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E[delta_n | F_n] <= C r_n on the good event, uniformly; E delta_n <= C r_n + P(bad event); O_P(r_n) under tight constants; variance and coefficient measurable in the design | rate: r_n | scope: random candidate designs, any conditioning sigma-field, slices in s
depends_on: W3-MISR:MIS(i)@stmt ; W3-MISR:MIS(i')@stmt ; W3-MISR:R'@stmt
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-G(a) | kind: corollary | statement: STATEMENT.md:164-170 | premises: STATEMENT.md:17-43 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on C-MIS:Prop-P; input versions C-MIS:Prop-P@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:14
assumptions: A:IID-GAUSS-ROWS
conclusion: identity: jointly Gaussian rows give the contrast-law condition at each n, with deterministic projected coefficient and variance sigma^2 + tau^2, for any n-dependence of the parameters | scope: example (Gaussian rows)
depends_on: C-MIS:Prop-P@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-G(b) | kind: corollary | statement: STATEMENT.md:171-174 | premises: STATEMENT.md:164-165 ; STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09, SOP:TH128, C-MIS:GDb; input versions C-MIS:Prop-P@1.0.0, SOP:TH09@1.0.0, SOP:TH128@1.0.0, C-MIS:GD(b)@1.0.0 (C-MIS:GDb = alias of C-MIS:GD(b)); council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:15
assumptions: A:IID-GAUSS-ROWS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E delta_n = O(r_n) under population conditions relative to the projected variance | rate: r_n | scope: example (Gaussian rows), 2 <= p_C <= n^A
depends_on: W3-MISR:Cor-G(a)@stmt ; W3-MISR:MIS(ii)@stmt ; C-MIS:GD(b)@hyp ; W3-POST2:A0@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)

REGISTRY
claim: W3-MISR:Cor-H | kind: corollary | statement: STATEMENT.md:178-197 | premises: STATEMENT.md:17-66 ; STATEMENT.md:222-245
status: PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103, sol=9.2 PASS, opus=8.9 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) | status_source: CHECKPOINT_4.md:16
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: in-sample average Hellinger contraction of the parameter posterior around the projected law; squared distance at rate log n / n without a margin, distance at rate M_n / sqrt(n) with selection | rate: squared Hellinger distance log n / n ; Hellinger distance M_n / sqrt(n) | scope: fixed designs, arrays in the class; in probability
depends_on: W3-MISR:R'@stmt ; W3-MISR:MIS(i)@stmt ; W3-POST2:D@hyp
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT1-A2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-A2=ticket(reviews/BT1_disposition.md) ; better-proposal:BT1-B2(reviews/BT1_better_theorem_astra.md) ; better-disposition:BT1-B2=ticket(reviews/BT1_disposition.md)
council: R2; MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
```
