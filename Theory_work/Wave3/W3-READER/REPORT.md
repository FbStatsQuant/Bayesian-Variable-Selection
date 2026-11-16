# W3-READER — REPORT (registry blocks only; v4: the report restates nothing)

Claims and proofs: `STATEMENT.md`, `lemmas/R1`–`R4`. Reader versions: `READER_VERSIONS.md`. Checkpoints:
`CHECKPOINT_1.md` (CP3 to follow). Check records: `reviews/`.

## Registry blocks

```
REGISTRY
claim: W3-READER:PoolZ | kind: corollary | statement: STATEMENT.md:12-37 | premises: Theory_work/Wave1/W1-N1/STATEMENT.md §2
name: Corollary PoolZ (the pooled evidence estimate is unbiased given the calibration)
status: PROVED (by this seat, unchecked) | status_source: STATEMENT.md:13
conclusion: identity: E[Zhat | C] = Z a.s. on the calibration-success event A, Zhat = (1/4) sum_r Zhat_r (equal-weight island mean, v3_run.R:154) | scope: SMC branch, any design, any data, N1 premises
depends_on: W1-N1:Thm-N1@1.0.0@proof:linearity
method: Scripts/SMC_BVS/core/v3_run.R:91,154
gates: correct:PENDING(bridge-leg Sol line check)

REGISTRY
claim: W3-READER:R1 | kind: lemma | statement: lemmas/R1_set_sizes.md:1-59 | premises: READER_VERSIONS.md (Thms 1, 2, 4, 6)
name: Lemma R1 (set-size and elementary bridges to the posterior and main-theorem hypotheses)
status: PROVED (by this seat, unchecked) | status_source: lemmas/R1_set_sizes.md:3
conclusion: identity: s0+j0 <= (2A+2)s0+2; s0+m#_n <= 3(A+1)(s0+1)log n; kbar_n <= 5(A+1)(s0+1)log n; 16+s0 <= 5(A+1)(s0+1)log n (n >= 3); bounded coefficients => energy; Gaussian nulls => (W-sph) | scope: n >= 3, A >= 1, s0 >= 1
depends_on: SOP:TH09@1.0.0@proof:[T03R]E2(ii)
gates: correct:PENDING(bridge-leg Sol line check; S1 verified the arithmetic analytically)

REGISTRY
claim: W3-READER:R2 | kind: lemma | statement: lemmas/R2_local_regression.md:1-43 | premises: lemmas/R2_local_regression.md:6-9
name: Lemma R2 (local regressions give the variance clause, population and sample forms)
status: PROVED (by this seat, unchecked) | status_source: lemmas/R2_local_regression.md:3
conclusion: inequality: Var(W_l | W_A) <= (1 + L^2/c) Var(W_l | W_T) for A subset T with l1 coefficient gap <= L, under unit diagonal and a floor c on Q union {l}; sample analogue with phi0^2 | scope: deterministic, any n
gates: correct:PENDING(bridge-leg Sol line check; S1: population form passes)

REGISTRY
claim: W3-READER:R3 | kind: lemma | statement: lemmas/R3_delivery_assembly.md:1-47 | premises: READER_VERSIONS.md (S4)
name: Lemma R3 (delivery assembly for the reported-model theorems)
status: PROVED (by this seat, unchecked) | status_source: lemmas/R3_delivery_assembly.md:3
conclusion: implication: RM2-R / RM2-F conclusions + (S4) => premises (V), (S), (P) and the method/premise/allocation paragraph of W2-UNI:F-UNI; hence P(no output) = 0 for every admissible n >= 3 and P(Shat = S0) -> 1
depends_on: W2-UNI:F-UNI@1.1.0 ; W3-RM2:RM2-R@1.0.0 ; W3-RM2:RM2-F@1.0.0
gates: correct:PENDING(bridge-leg Sol line check)

REGISTRY
claim: W3-READER:R4 | kind: lemma | statement: lemmas/R4_printed_outputs.md:1-44 | premises: lemmas/R4_printed_outputs.md (Claim)
name: Lemma R4 (printed PIPs, MPM, HPM and evidence estimate are consistent: assembly)
status: PROVED (by this seat, unchecked) | status_source: lemmas/R4_printed_outputs.md:3
conclusion: rate: 1_A max(o0, o1) = O_P(n^{-1/2} exp(C_R sqrt(log n))); hence Zhat/Z - 1, log Zhat - log Z, ||pip_primary - 1_S0||_inf = O_P(that) on A; P(A and MPM != S0) -> 0; P(completed and Shat != S0) -> 0 | scope: Gaussian rows, standardised-signal convention, Q = S0
depends_on: W3-SAMP:C@1.1.1 ; W3-START2:IF-START@1.0.0 ; W3-START2:START-R@1.0.0 ; W3-POST:Thm-1@1.0.0 ; W2-APP:POST@1.0.1
gates: correct:PENDING(bridge-leg Sol line check)
```

Notes for the ingest (HQ / recorder): R4 inherits the conditions of its inputs, "conditional on C-PACK:SL0, SOP:TH09"
(through `W3-SAMP:C@1.1.2` and `W2-APP:POST@1.0.5`, main f526e45b). R3 carries F-UNI's qualifications ([OP] author-only; e4/N3 OPEN; P1/S.3 code-reading audit).
The reader-version corollaries (Theorems 1–8, 10 of `READER_VERSIONS.md`) are not proposed as separate rows here;
HQ decides whether each reader version gets a row (PROGRAM "Readability": "The reader version is a corollary with its
bridges checked").
