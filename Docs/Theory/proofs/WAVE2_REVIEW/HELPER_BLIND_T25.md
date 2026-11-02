# Closing correctness review: T25(iv)

Assigned proof: `T25iv_T19_crossing_evidence/proof/PROOF_v1.tex`.
Review date: 2026-10-22. No proof was edited. No numerical workload was run. No further delegation was used.

## Findings

No fatal, gap, or exposition finding requiring a correction was identified in the assigned proof or its mathematical restatement. No replacement wording is required.

The following are verification records, not defect findings. Line numbers refer to the files as inspected.

### 1. Fidelity to STATEMENT and the source theorem

**Location:** assigned proof lines 18–21, 24–80, 173–184; assigned `STATEMENT.md` lines 5–17, 21–58, 64; original `theorems/T25_T19_crossing_evidence.md` lines 8, 11, 17.

**Claim checked:** the deliverable proves exactly the PW2-conditional assertion of T25(iv), for the actual island system and four-island pooling.

**Evidence:** the proof's PW2 at lines 63–67 and bound at lines 69–78 reproduce the source's inequality, product, and propagated slack sum. The source explicitly calls establishing PW2 with useful constants a missing task. Neither the proof nor STATEMENT claims to establish PW2, revive the withdrawn RET+OCC rate, or prove another part of T25. The scalar `W_t` is the actual evidence ratio, not a reflected-system object or a working set. The statement explicitly specifies nonnegative finite upper-bound coefficients fixed given calibration; the proof uses precisely those coefficients. This makes the conventional coefficient/slack interpretation explicit rather than supplying a condition that implies PW2. The source leaves their signs implicit; the verified result is the precise version in STATEMENT, not an extension to arbitrary signed coefficients.

The exact bridge, per-island particle count, frozen grid, and evidence scaling agree with `00_COMMON.md` lines 18–26, `METHODOLOGY_v3.md` lines 173–177, 187–205, 243–245, 279–282, and `THEORY_BRIEF.md` lines 119–127, 190–191. In particular, `Z_0=m(empty) Zbar_0`, so `W_0=1`, and the terminal normaliser is the full evidence `Z`.

### 2. Finiteness and normalisation

**Location:** assigned proof lines 24–44, 46–58, 83–92; STATEMENT lines 23–40.

**Claim checked:** all expectations in the subsequent identities are defined, and the normalised weight has the required bridge identity.

**Evidence:** positivity and finiteness on finite Omega give finite extrema `d_-` and `d_+`. Each empirical potential mean lies between `exp(Delta_t d_-)` and `exp(Delta_t d_+)`. Multiplication and `sum_{j<=t} Delta_j=phi_t` give exactly the displayed bounds on `Zhat_t/Z_0` at lines 87–88. Division by deterministic positive `Z_t` gives finite moments. Directly from the bridge definition, `q_{t-1}(g_t f)=q_t(f)`, with `g_t=G_t/(Z_t/Z_{t-1})`; no factor of `m(empty)` is lost.

### 3. Unbiasedness and the first-moment induction

**Location:** assigned proof lines 94–127.

**Claim checked:** `E_c W_t=1`, hence `Var_c(W_t)=E_c W_t^2-1`.

**Evidence:** multinomial parent selection followed by fresh mutation has conditional child law proportional to `qhat_{t-1}(G_t K_t f)`, giving lines 100–101. The denominator is strictly positive. The evidence update is already measurable before resampling/mutation. Multiplying cancels the empirical denominator, and the simultaneous induction for all deterministic functions applies to `g_t K_t f`, which is deterministic once data and calibration are fixed. The last step uses the bridge identity and `q_t K_t=q_t`. Taking `f=1` proves the needed mean identity. This does not presume that `W_t` is a martingale, and lines 126–127 correctly distinguish that stronger, generally unavailable assertion.

Exact starts and the exact initial normaliser are explicit premises of STATEMENT, not consequences inferred from exact arithmetic alone. The invariant round is also explicit. They match the T12 setting; the collection's T12 elementary-kernel and prefix proofs establish round invariance at lines 1303–1329.

### 4. PW2 recursion and its solution

**Location:** assigned proof lines 49–52, 129–158.

**Claim checked:** PW2 implies the asserted finite-stage variance bound without a missing factor or an index shift.

**Evidence:** the pathwise update implies exactly

`M_t-M_{t-1}=E_c[W_{t-1}^2 {(qhat_{t-1}(g_t))^2-1}]`.

PW2 therefore gives `M_t <= alpha_t M_{t-1}+nu_t`, with `alpha_t=1+a_t/N >= 1` and `M_0=1`. The proposed `U_t` at lines 144–146 satisfies `U_t=alpha_t U_{t-1}+nu_t`. Nonnegativity of `alpha_t` justifies the inductive comparison. Subtracting one is justified by the separately proved unbiasedness. Each slack `nu_s` is multiplied only by later-stage factors, with the empty product one. No independence of particles or empirical weights across stages is used in this recursion.

### 5. Pooling and conditioning

**Location:** assigned proof lines 75–80, 160–176; STATEMENT lines 21, 40, 56–58.

**Claim checked:** the whole single-island bound is divided by four for the reported pooled evidence, conditional on calibration.

**Evidence:** each island is generated from the same fixed settings and its own fresh independent ideal stream. Conditional on calibration the evidence ratios are independent copies. Thus the variance of their equal-weight average is `1/16` times the sum of their variances, giving `B_T/4`. This divides both the product-minus-one term and the slack sum; `N` remains the per-island `N_e`. Terminal mutation rounds and local search do not enter the evidence product (`METHODOLOGY_v3.md` lines 243–245, 279–280). The proof conditions on calibration success and fresh final randomness, not final flags or a random selection of completed outcomes. It asserts no unconditional variance bound over random calibration and requires no calibration-uniform coefficients.

### 6. Every wave-1 T12 citation checked against the collection

All collection references below are to `COLLECTED/COLLECTED_PROOFS_v2.tex`.

- **T12(i.a)** — cited at assigned proof lines 94–95 and 180–182; also STATEMENT line 62. The collected statement at line 1225 is exactly the weighted stagewise identity being used. The final proof establishes it at lines 1366–1378. The assigned proof also independently establishes its normalised form at lines 97–124. **Citation verified.**
- **T12(iii)** — cited at assigned proof lines 94–95 and 180–182; also STATEMENT line 62. The collected statement at line 1233 explicitly includes conditional stagewise identities, not just terminal pooled unbiasedness. The final proof's freezing argument is at lines 1404–1417, and its transfer of stagewise identities at line 1421. This supports the stated conditioning on successful frozen calibration. **Citation verified.**
- **T12(iv.c)** — cited at assigned proof lines 161–164 and 180–182; also STATEMENT line 62. The collected statement at line 1240 asserts independence given calibration with common frozen-island law. The final proof at lines 1471–1472 derives the conditional factorisation from the freezing identity. The assigned proof uses only this conditional independence, not independence after averaging over calibration. **Citation verified.**

The exact-start dependency remains explicit in the collected T12 setting (lines 1211, 1287) and in the assigned STATEMENT (lines 32, 40); it has not been silently replaced by EX-A. The reference to T12 as a proved wave-1 result is used consistently with the provided collection, and no other wave-1 citation appears in the assigned proof.

## Procedural limitation

Broad searches and an initially overbroad line range in the permitted collection incidentally exposed embedded review-record snippets. No separate reviewer, helpers, claims, or final-report file was opened, and this assessment does not rely on those snippets. Nevertheless, strict blindness cannot be certified. The mathematical verdict below is an independent correctness assessment with that procedural limitation disclosed.

## Verdict

**T25(iv): VERIFIED** for exactly the explicit hypotheses and conditional conclusion of the assigned STATEMENT, including four-island pooling. Establishing PW2 with useful constants remains outside the result.
