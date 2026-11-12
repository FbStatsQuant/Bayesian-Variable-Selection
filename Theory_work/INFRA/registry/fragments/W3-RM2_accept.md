# W3-RM2 — acceptance carrier (HQ, 2026-11-12)

Carrier (LIFECYCLE §4.1 "carrier files"): the 18 claims of the REGISTRY block of `Theory_work/Wave3/W3-RM2/REPORT.md`
(R1 snapshot, inside MANIFEST_R1 00bbeab8…), in valid block grammar. Grammar fixes only: one claim per block; statement
/ premises as path:a-b (`(C1)` = STATEMENT.md:206-214, `§1` = 47-95, `§3.1` = 126-171, `§3.2` = 172-202, `(C3)` preamble
220-222, bridge-table rows 247-257, `(C5)` = 259-275, L6 `E2`–`E5` = their sections); `depends_on` use labels without
spaces; content the grammar cannot carry (assumption / property ids not in the registry, sharpness, binding,
assumption-level implies, bracket notes) kept verbatim in `notes`. Changed by HQ decision, not grammar: status and
status_source (CHECKPOINT_4.md), `council` (R1 cell), `correct:PASS` (was PENDING before the council), `implies` over
RM-F / RM-R not recorded (owner's call), rule-11 conditions the acceptance tool requires (@hyp edges, §5 premise span
where the hypothesis is named).

```
REGISTRY
claim: W3-RM2:RM2-F | kind: theorem | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:206-214 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:290-312
name: Theorem RM2-F (fixed design, polynomial leakage)
status: PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:12
conclusion: reported-model: one data event of probability -> 1 on which every admissible output run reports S0 | rate: none claimed | scope: fixed design; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; SOP:TH09@hyp ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-F-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt ; W3-RM2:W-suff@stmt ; W3-RM2:W-conv@stmt
gates: correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md) ; lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ; better:PENDING(reviews/BT1_better_theorem_astra.md)
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
notes: REPORT block assumptions (ids not registered): A:T1-F ; A:FL-16 ; A:FL-Q ; A:V ; A:L-gain ; A:L-feas ; A:BM-W (new | signal floor at the truth-removal width | theta_min^2 (n-1) phi0^2 / (sigma^2 (d_n^2 + log n)) -> infinity | STATEMENT.md §1,§3.1 | shared yes | P2 TL-F^b) ; A:L-size-b (new | polynomial leakage size | |Q| <= n^b, b < beta(eta,A) | STATEMENT.md §3.1 | shared yes | P1 SAND-F^b) ; A:W (new | lattice width gap | w0_n -> -infinity | STATEMENT.md §1,§3.1 | shared yes | P3 NA-W) ;; REPORT block consumes (ids not registered): P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4 ;; REPORT block implies (not recorded: supersession / implies over RM-F is the owner's call): W3-RM:RM-F (special case |Q| polylog, (W) from (N-chi) or (N-D)(i) through W3-RM2:W-suff; claim W3-RM2:Cont-F) ;; REPORT block sharpness: A:W = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_width.md §2, Lemma W-conv: gap -> +infinity obstructs whole-lattice no-addition; not for reporting; bounded gap undetermined) ; A:L-size-b = ARTEFACT (evidence: lemmas/L1_sandF_b.md §3(b); sufficient budget of the junk-exclusion argument; necessity open) ; A:BM-W = NONE (sufficient; necessity not studied) ; A:V, A:L-gain, A:FL = as W3-RM ;; REPORT block binding: A:W route obstruction via W3-RM2:W-conv: gap -> +infinity forces P(NA(Q)) -> 0; gap -> -infinity is sufficient; bounded gap undetermined [whole-lattice route only] ; A:L-size-b enters P:SAND(Q) via the junk-exclusion margin [artefact-threshold]
```

```
REGISTRY
claim: W3-RM2:RM2-R | kind: theorem | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:290-312
name: Theorem RM2-R (Gaussian rows, polynomial leakage)
status: PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:13
conclusion: reported-model: as RM2-F under the joint law of (X, eps) | rate: none claimed | scope: Gaussian rows; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b, |H_l| <= n^rho
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; W2-APP:POST@hyp ; W3-RM2:SAND-R-b@stmt ; W3-RM2:F-to-R@stmt ; W3-RM2:POST-R@stmt ; W3-RM2:D-to-W@stmt ; W3-RM2:W-conv@stmt
gates: correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md) ; lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ; better:PENDING(reviews/BT1_better_theorem_astra.md)
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
notes: REPORT block assumptions (ids not registered): A:T1-R ; A:FL-R ; A:V-R ; A:L-feas ; A:L-gain-R (new in this form | leak bound at every conditioning set | |Cov(W_l, W_j | W_U)| <= varpi_n = o(sqrt(log n/n)), l outside Q, |U| <= 15, truth j outside U | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:L-loc-R (new in this form | localisation without rate | conditional covariances with columns outside H_l at most r_n -> 0 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:L-size-b-R (new | polynomial leakage size, Gaussian rows | |Q| <= n^b, b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:H-size-rho (new | reference neighbourhood size | |H_l| <= n^rho, 15 rho + b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:W-R (new | lattice width on the realised design | exists deterministic t_n -> infinity: P(W0_n intersect {w0_n <= -t_n}) -> 1 | STATEMENT.md §3.2 | shared yes | P8 F-to-R) ;; REPORT block consumes (ids not registered): P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4 ;; REPORT block implies (not recorded: supersession / implies over RM-R is the owner's call): W3-RM:RM-R (special case, (L-R) through the localised sufficient form, (W-R) from (D-R) through W3-RM2:D-to-W; claim W3-RM2:Cont-R) ;; REPORT block sharpness: A:W-R = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_width.md §2 applied conditionally; positive diverging gaps obstruct whole-lattice no-addition; bounded gaps undetermined; no necessity for reporting claimed) ; A:H-size-rho = ARTEFACT (evidence: lemmas/L4_sandR_b.md §4; reference counting) ; A:L-size-b-R = ARTEFACT (evidence: lemmas/L4_sandR_b.md §6(b); sufficient budget; necessity open) ; A:L-gain-R = WEAKENABLE (evidence: lemmas/L4_sandR_b.md §7 item 4; exact scale kappa sqrt(log n/n) not derived) ; A:L-loc-R = NONE (evidence: SHARPNESS.md §3; needed by this proof at r_n -> 0 only) ;; REPORT block binding: A:H-size-rho enters P:SAND(Q) via the reference count n^{15 rho} [artefact-threshold]
```

```
REGISTRY
claim: W3-RM2:Toolkit-b | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:247 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95
name: (P0) Toolkit-b
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:14
depends_on: C-GROW:L0.1@proof ; C-GROW:L0.2@proof
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:SAND-F-b | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:248 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171
name: (P1) SAND-F^b
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:15
depends_on: C-GROW:L3@proof ; W3-RM2:Toolkit-b@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:TL-F-b | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:249 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171
name: (P2) TL-F^b
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:16
depends_on: C-GROW:L2.1@proof ; W3-RM2:Toolkit-b@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:NA-W | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:223-225 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:220-222
name: Lemma NA-W ((C3)(a))
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:17
depends_on: C-GROW:L2.2@proof ; W3-RM2:Toolkit-b@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:W-conv | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:226-230 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:220-222
name: Lemma W-conv ((C3)(b))
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:18
depends_on: W3-RM2:Toolkit-b@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:W-suff | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:231-234 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:220-222
name: Sufficient forms ((C3)(c))
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:19
depends_on: C-GROW:L2.3@proof
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
notes: REPORT block assumptions (ids not registered): A:W-delta (new) ; A:W-unif (new) ; A:W-chi ; A:W-ref (new) ; A:W-loc (new)  [alternatives, not a conjunction: each implies A:W] ;; REPORT block implies (assumption-level, ids not registered): A:W-delta => A:W ; A:W-unif => A:W-delta ; A:W-chi => A:W-delta ; A:W-ref => A:W-unif ; A:W-loc => A:W-ref ; A:BM-Q => A:BM-W
```

```
REGISTRY
claim: W3-RM2:Cont-F | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:126-171
name: Containment, Form F ((C4))
status: PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:20
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt ; W3-RM:RM-F@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:SAND-R-b | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:254 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202
name: (P7) SAND-R^b
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:21
depends_on: C-GROW:L6.4@proof ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-F-b@proof:per-block-optimality-(1.1)-and-count-(2.1)
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
notes: template note edge (HQ 2026-11-12, option (b); not a consumption edge): REPORT block depends_on W3-RM:SAND-R@proof — lemmas/L4_sandR_b.md is self-contained (RM's SAND-R is a template, L4_sandR_b.md:12)
```

```
REGISTRY
claim: W3-RM2:F-to-R | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:255 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202
name: (P8) F->R
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:22
depends_on: W3-RM2:Toolkit-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:D-to-W | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:256 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202
name: (P9) D->W
status: PROVED-CHECKED; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:23
depends_on: —
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
notes: template note edges (HQ 2026-11-12, option (b); not consumption edges): REPORT block depends_on W2-LOC2:NA-R@proof ; W3-RM:D-loc@proof — D-loc is written out in lemmas/L5_formR.md:108-117 and NA-R's conclusion is not consumed; relied-on computations: the pinned proof text Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md:79-85, 102-105 (hashed in MANIFEST_R1) ;; REPORT block assumptions (ids not registered): A:D-R-b (new) ; A:D-loc-b (new)  [alternatives: A:D-loc-b => A:D-R-b => A:W-R for every delta0 in (0, 1 - 2b)] ;; REPORT block depends_on note: [proof templates re-run at polynomial size; no conclusion of them is consumed outside its stated range]
```

```
REGISTRY
claim: W3-RM2:POST-R | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:257 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:47-95 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202 ; Theory_work/Wave3/W3-RM2/STATEMENT.md:290-312
name: (P10) POST-R
status: PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:24
depends_on: W2-APP:POST@hyp
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:Cont-R | kind: lemma | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:236-240 | premises: Theory_work/Wave3/W3-RM2/STATEMENT.md:172-202
name: Containment, Form R ((C4))
status: PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:25
depends_on: W3-RM2:RM2-R@stmt ; W3-RM2:SAND-R-b@proof:section-7-item-1 ; W3-RM2:D-to-W@stmt ; W3-RM:RM-R@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:Ex-PolyR | kind: proposition | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:259-275 | premises: Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md:164-263
name: Example E2 ((C5): Gaussian rows, polynomial covariance decay)
status: PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on W2-APP:POST, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; input versions W2-APP:POST@1.0.1, W2-LOC2:Lemma-BC@1.0.0, W2-LOC2:Lemma-IR@1.0.0 | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:26
depends_on: W3-RM2:RM2-R@stmt ; W3-RM2:D-to-W@stmt ; W2-LOC2:Lemma-BC@hyp ; W2-LOC2:Lemma-IR@hyp
```

```
REGISTRY
claim: W3-RM2:Ex-PolyF | kind: proposition | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:259-275 | premises: Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md:264-329
name: Example E3 ((C5): exact-Gram polynomial decay)
status: PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round; conditional on SOP:TH09, W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR; input versions SOP:TH09@1.0.0, W2-LOC2:Lemma-BC@1.0.0, W2-LOC2:Lemma-IR@1.0.0 | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:27
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt ; W2-LOC2:Lemma-BC@hyp ; W2-LOC2:Lemma-IR@hyp
```

```
REGISTRY
claim: W3-RM2:Ex-Proxy | kind: proposition | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:259-275 | premises: Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md:330-384
name: Example E4 ((C5): one truth with n^b weak proxies)
status: PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:28
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```

```
REGISTRY
claim: W3-RM2:Ex-Equi | kind: proposition | statement: Theory_work/Wave3/W3-RM2/STATEMENT.md:259-275 | premises: Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md:385-474
name: Example E5 ((C5): one equicorrelated group)
status: PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a, astra=9.5 PASS, opus=8.8 PASS; correct:PASS(reviews/C_R1_council_astra.md, reviews/C_R1_council_opus.md, per-claim addenda) | status_source: Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md:29
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt
council: R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)
```
