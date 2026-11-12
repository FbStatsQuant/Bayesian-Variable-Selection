# W3-START2 — acceptance carrier (HQ, 2026-11-12)

Carrier file (LIFECYCLE §4.1 "carrier files"): the 9 REGISTRY blocks of `Theory_work/Wave3/W3-START2/CHECKPOINT_2.md` §6
(status source unchanged), with `path:line` spans made repo-relative and the `implies:` rows left out: HQ decision
2026-11-12 — the implies / supersession relations over W3-START claims are not required for acceptance; the
headline replacement is the owner's call.

```
REGISTRY
claim: W3-START2:LEAK-0 | kind: lemma | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:82-89 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Lemma LEAK-0 (leading term of the start odds, sharp functional)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:34
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: for s0 at least 1, P(T1 > 5 lambda (s0+1) n^{-1/2} L^sharp_n(h)) is at most P(toolkit event fails) + b_n(h) + 451 e^{2 kappa_E + 1}/lambda on the stated range of lambda; hence T1 = O_P(n^{-1/2} L^sharp_n(h)) | rate: n^{-1/2} times the sharp leading functional | scope: fixed design, p at most n^A, s0 at least 1 and below K, uniform in the design, the coefficients and the level vector
depends_on: W3-START:TK@proof ; W3-START:LEAK@proof:L3.3
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:START-F | kind: theorem | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:93-110 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Theorem START-F (fixed design, uniform form, sharp leading functional)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:35
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: start odds against S0 are O_P(n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2) + o_P(n^{-kappa}); lattice mass outside {S0 subset T subset Q} is O_P(rho_n(Q; h)) + o_P(n^{-kappa}); o0/T1 tends to 1 when kappa_V exceeds 1/2; uniform finite-n form with exceptional probability eps + b_n(h) | rate: n^{-1/2} times the sharp leading functional | scope: fixed design, p at most n^A (p much larger than n allowed), s0 fixed, partition-free hypotheses
depends_on: W3-START2:LEAK-0@proof ; W3-START:START-F@proof:L5.2 ; W3-START:F1@proof:L6.0 ; W3-START:AGG@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof ; W3-START:VIS-m@proof ; W3-START:ASM@proof
sharpness: A:START-V = NECESSARY (evidence: Theory_work/Wave3/W3-START/lemmas/L7_NEC.md:28)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:F2 | kind: corollary | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:112-117 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Corollary F2 (strong signals; no growth condition on p)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:36
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: o0 = O_P(n^{-(1-eta')/2}) + o_P(n^{-kappa}) for every kappa below kappa_V; if eta' = 0 and kappa_V exceeds 1/2, o0 is of exact order n^{-1/2} | rate: n^{-(1-eta')/2} | scope: fixed design, s0 at least 1, p greater than s0, bounded p allowed
depends_on: W3-START2:START-F@proof ; W3-START:F2@proof:L6.2 ; W3-START:FLOOR@proof
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:TRANSFER | kind: theorem | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:120-133 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Theorem START-R(a) (transfer to random designs, sharp leading functional)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:37
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under any design law with design-measurable coefficients, support, leakage set and levels, 1 - pi0(L(Q)) = O_P(rhobar_n) + o_P(n^{-kappa}); with Q = S0 and n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2 at most rbar_n on the design sets, o0 = O_P(rbar_n) + o_P(n^{-kappa}) | rate: rhobar_n, rbar_n | scope: Gaussian noise given the design; response-selected targets not covered
depends_on: W3-START2:START-F@proof ; W3-START:TRANSFER@proof:L8.2
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:IF-START | kind: corollary | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:176-180 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Corollary IF-START (start interface with the sharp rate)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:38
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1_A o0 = O_P(r_n) with r_n = n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2 + n^{-kappa} tending to 0 (fixed design), or r_n = n^{-1/2} exp(C_R sqrt(log n)) (Gaussian rows, Q = S0); hence P-START with a rate | rate: r_n | scope: only the start interface is supplied
depends_on: W3-START2:START-F@proof ; W3-START2:START-R@proof ; W3-START:IF-START@proof:L10.1
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:OVL | kind: proposition | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:181-189 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Proposition OVL (start mass under a bounded leakage set, either visibility condition)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:39
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(pi0(S0) is at least n^{-E_n - eps}) tends to 1 for every eps > 0, E_n the sum over Q minus S0 of the positive parts of (a_{n,l} - 1)/2 - log p/log n; hence P-OVL in its production form when limsup(E_n - max(1, log p/log n)) is negative | rate: n^{-E_n - eps} | scope: fixed design, bounded number of extra columns in Q with uniformly bounded gain levels
depends_on: W3-START2:START-F@proof ; W3-START:AGG@proof:CH ; W3-START:TK@proof ; W3-START:OVL@proof:L10.2
sharpness: A:START-V = NECESSARY-FOR-ROUTE (evidence: Theory_work/Wave3/W3-START2/lemmas/P2_OVL.md:66)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P2(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P2=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:NEC | kind: proposition | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:154-173 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:38-39
name: Proposition NEC (limits; partition-free leaking-null limit for every s0 at least 1)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:40
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: if max(1, 17 - s0) designated nulls each have gain at least c tau_V^2 log n on every proper subset V of the truth of size at most 15, with fixed c > 1 + 2 Abar, then pi0(S0) is at most n^{-kappa'} with probability tending to 1 for every kappa' below (c - 1 - 2 Abar)/2; (N1), (N3), (N4) as in the base ticket | rate: n^{-kappa'} | scope: fixed design, s0 at least 1; non-vacuous for every s0 from 1 to 15 (example given); fewer than 17 - s0 nulls not claimed
depends_on: W3-START:NEC-b@stmt ; W3-START:NEC@proof:L7.3 ; W3-START:FLOOR@proof ; W3-START2:F2@proof
sharpness: A:BLOCK-LE-16 = NECESSARY-FOR-ROUTE (evidence: Theory_work/Wave3/W3-START2/lemmas/P3_NEC.md:67)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P3(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P3=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:BR | kind: lemma | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:147-152 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:63-73
name: Bridge B-R (Gaussian rows; leakage set of any size at most K)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:41
assumptions: A:START-R-FL ; A:START-R-V ; A:START2-R-L (new | Localised bounded leakage with a leakage set of any size at most K | as (L-R) of the base ticket [A:START-R-L] without the requirement that the size of Q is at most (log n)^{kappa_Q}; the reference sets H_l stay of size at most (log n)^{kappa_Q} | Theory_work/Wave3/W3-START2/STATEMENT.md:63-73 | shared no | bridge W3-START2:BR)
conclusion: target: with probability tending to 1 a Gaussian-row design satisfies the energy bound, the normalised floor on sets of size at most 16 (hence the Gram floor), constant-level visibility for every fixed level, and L_n(Q) at most exp(C_B sqrt(log n)); with zero population leakage L_n(Q) = O_P((log n)^{15 kappa_Q + 1/2}) (tightness only) | rate: exp(C_B sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, any deterministic Q containing S0 with size at most K
depends_on: W3-START:BR@proof:L9.1-L9.6 ; W3-START:LEAK@proof
sharpness: A:START2-R-L = NECESSARY-FOR-ROUTE (evidence: Theory_work/Wave3/W3-START2/lemmas/P4_BR.md:27)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P4(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P4=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:START-R | kind: theorem | statement: Theory_work/Wave3/W3-START2/STATEMENT.md:134-145 | premises: Theory_work/Wave3/W3-START2/STATEMENT.md:63-73
name: Theorem START-R(b) (Gaussian rows; leakage set of any size at most K)
status: PROVED-CHECKED | status_source: Theory_work/Wave3/W3-START2/CHECKPOINT_2.md:42
assumptions: A:START-R-FL ; A:START-R-V ; A:START2-R-L ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) with probability tending to 1; with Q = S0, pi0(S0) is at least 1 - n^{-c} for every c below 1/2; with size of Q at most n^{1/2 - eps_Q}, pi0(L(Q)) is at least 1 - n^{-c} for every c below eps_Q; with zero population leakage the rate is O_P((size of Q + 1) n^{-1/2} (log n)^{15 kappa_Q + 1/2}) | rate: (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed, s0 fixed; the display is trivial where its right side is at least 1
depends_on: W3-START2:BR@proof ; W3-START:TRANSFER@proof:L8.2 ; W3-START:START-F@proof:L5.2(i) ; W3-START:F1@proof:L6.0 ; W3-START:START-R@proof:L9.7
sharpness: A:START2-R-L = NECESSARY-FOR-ROUTE (evidence: Theory_work/Wave3/W3-START2/lemmas/P4_BR.md:101)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P4(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P4=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```
