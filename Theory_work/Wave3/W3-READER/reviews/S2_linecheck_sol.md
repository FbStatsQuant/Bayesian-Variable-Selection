# S2 line check and fidelity diff — W3-READER bridge leg

Tier B, PROTOCOL_v4; one pass, gpt-6.1-sol (high). Reviewed the S2 frozen files against the cited masters, registry and production core. No style/readability review. No source or git-state mutation; this review is the sole output.

**Integrity.** `sha256sum -c MANIFEST_S2.txt` passed for all 11 entries. Both supplied diffs exactly reproduce the S1-frozen → S2-frozen changes, excluding their timestamp headers. All reader/lemma/card locations below refer to S2 frozen copies. Master and registry locations refer to this checkout. An input's existing status is not upgraded by this review.

**Result.** The arithmetic and regression claims, posterior rebase, and PoolZ linearity argument are sound. R4's probability calculation is sound under its explicitly assumed N1 contract and the master's potential-record convention. The delivery contract is still incompletely stated, and Theorem 10 and its card summary need scope/premise repairs. No FATAL finding; five MAJOR, three MINOR, one NIT.

## Findings

### F1 — MAJOR — R3 attributes parts of MACH/CONFIG to (S4) that (S4) does not state

**Location:** [R3:31–34](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/lemmas/R3_delivery_assembly.md:31), [RV:27–36](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:27), delivery conclusions [RV:477](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:477) and [RV:585](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:585).

R3's MACH row says that (S4) supplies time and memory proportional to operations and words. It does not: (S4) gives exact unit-cost arithmetic and allocation success, but no wall-time/peak-byte bounds with MACH's conversion constants. R3's CONFIG row also says certificate budgets are declared, which is absent from (S4). These omissions matter to the allocation step: operation counts alone do not exclude a clock-based resource stop, and certificate work/storage must be included separately.

The required contract is explicit in [C-DLV:28–46](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave1C/C-DLV/STATEMENT.md:28): time ≤ τ·work+τ₀, bytes ≤ β·words+β₀, fixed concurrency, and polynomial Cert/Cert_M budgets included in allocation. [F-FAC:7–16](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md:7), imported by F-UNI, expressly retains MACH conversion constants and certificate bounds. The generic phrase “the method's polynomial envelopes … listed in the paper's appendix” does not state these missing machine/configuration premises or identify their full mathematical contract.

**Minimal fix:** incorporate MACH(τ,τ₀,β,β₀), CONFIG and the complete amended allocation contract by exact source reference in (S4), including certificate budgets, concurrency factors, W_G/M_G, P₀/P₁/P̄_t and the extra LS0 time/archive bounds. Alternatively write those inequalities explicitly. Keep TDP-IMPL's operation/storage contract explicit as well; “within its stated cost” needs the contract it refers to. The common-data-event clauses of Theorems 6–7 survive; unconditional delivery is not discharged as written. S1-F2 is only partially fixed.

### F2 — MAJOR — Theorem 10's (S5) does not supply the complete N1 premise set assumed by R4

**Location:** [RV:38–41](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:38), [RV:712](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:712), versus [R4:7–8,25](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/lemmas/R4_printed_outputs.md:7).

R4 assumes the N1 premises. The reader instead lists a shorter convention without proving that it entails them. Most concretely, N1's START asserts both exact π₀ sampling **and** the exact reported normalizer Z̄₀; (S5) asserts only sampling. Correct π₀ draws do not establish the evidence normalization: multiplying the initialization normalizer by two preserves every draw/kernel but doubles the evidence estimate. The inherited KERNEL premise also includes the uniform state-independent order, not just realization of the elementary kernels. MEAS and the potential-run interpretation must be supplied or derived.

These are explicit in [N1:70–88](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave1/W1-N1/STATEMENT.md:70). N1's [code bridge:33–55](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md:33) derives measurability/control flow under the full START/KERNEL premises; it does not remove the normalizer premise. [SAMP:64–70](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SAMP/STATEMENT.md:64) retains their inherited qualifications.

**Minimal fix:** make (S5) incorporate the entire N1/SAMP algorithm contract, including fresh iid uniforms, the exact start normalizer and order law. Cite the existing code bridge for MEAS and the relevant production code facts, with their inherited premise statuses. R4 then applies without an unstated hypothesis. This does not invalidate R4 when its own N1 assumptions are retained.

### F3 — MAJOR — Theorem 10 calls potential records “printed” and leaves the SMC branch restriction implicit

**Location:** [RV:717–727](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:717); [NOTATION:127–134](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/NOTATION.md:127).

Calibration success does not imply completion under (S1)–(S3),(S5). On A the master defines **potential uninterrupted** estimates; only on completion do they equal reported fields. The reader instead defines the variables as printed estimates on all of A. Those variables need not exist there: [v3_run.R:143–148](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_run.R:143) suppresses estimates for a stopped final run. Consequently the first display is not a statement about defined printed random variables as written. SAMP [§0:29–41](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SAMP/STATEMENT.md:29) and [PC:90–95](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SAMP/STATEMENT.md:90) make this distinction explicit.

Also, SAMP's A is `{SMC branch and calibration status ok}`. The reader allows bounded p and describes A as containing every completed run, while the exact branch produces estimates without calibration ([v3_fit.R:120–131](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_fit.R:120)); SAMP expressly excludes that branch ([SAMP:186](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SAMP/STATEMENT.md:186)). For example p=2, s₀=1 satisfies the dimension range and uses exact enumeration for all large n. “Completed” must either mean the specific SMC status or receive a separate exact-branch argument.

**Minimal fix:** state the SMC scope and define potential estimates on A, with arbitrary extensions off A; identify them with printed fields only on `{status=completed}` via PC. State the printed-field rate/error events intersected with completion. If the theorem is intended to cover exact outputs too, add that branch separately (evidence exact; posterior PIP/MPM/HPM conclusions from Theorem 2). Do not silently redefine A; PoolZ's four-island identity has SMC scope.

### F4 — MAJOR — Card row 3.6 strengthens intersection-event convergence to recovery “w.p. → 1”

**Location:** [CLAIMS_CARD:51](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/CLAIMS_CARD.md:51).

The row says “on calibration success” the rate holds and then “printed MPM = S₀ and reported HPM = S₀ w.p. → 1.” Theorem 10 actually gives P(A ∩ {MPM≠S₀})→0 and P(completed ∩ {Ŝ≠S₀})→0. It gives neither unconditional recovery/output nor recovery conditional on A/completion. Even P(A ∩ error)→0 permits P(error|A)=1 when P(A)→0. No lower bound on P(A) or completion is assumed. “On calibration success” must not turn localization into conditioning.

**Minimal fix:** say that the errors, multiplied by 1_A for potential estimates, have the displayed O_P rate, and that the probabilities of “calibration succeeds and MPM is wrong” and “run completes and reported HPM is wrong” tend to zero. For printed fields use completion, as in F3. Do not assert P(A)→1.

### F5 — MAJOR — Card row 3.6 conflates the raw-coefficient and standardized-signal hypotheses

**Location:** [CLAIMS_CARD:31,48,51](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/CLAIMS_CARD.md:31), [RV:710–715](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:710).

“Under the conditions of 1.2 and 3.3 (no leakage)” is not Theorem 10's setting. Row 1.2/Theorem 2 fixes nonzero **raw** coefficients β*, whereas row 3.3/Theorem 5 and Theorem 10 fix **standardized** θ*. APP covers either convention for the posterior, as R4 correctly explains, but that does not transfer Theorem 5's population visibility/leakage hypotheses from deterministic θ* to random Dβ*. The reader itself lists that raw-scale extension as an unproved optional bridge ([RV:778](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:778)).

**Minimal fix:** describe row 3.6 directly as Theorem 10's deterministic standardized-signal setting, with Theorem 2's population floor and Theorem 5's visibility/no-leakage conditions. State that APP covers the posterior under this convention; do not advertise the raw-coefficient extension.

### F6 — MINOR — Theorem 1′'s descriptive claim drops the eigenvalue restriction that remains in (A5)

**Location:** [RV:94–105](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/READER_VERSIONS.md:94), [CLAIMS_CARD:30](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/CLAIMS_CARD.md:30).

The displayed hypotheses correctly retain (A5), an unnormalized eigenvalue floor on all the specified O(log n)-sets, including sets away from S₀. Thus “no eigenvalue condition away from the truth” and the unqualified claim that “the floor off S₀” is replaced are not true of this sufficient reader version. The master with (OS) has that freedom; this reader version uses the stronger (A5) to derive (OS).

**Minimal fix:** say “no bounded-size normalized floor away from the truth,” explicitly retaining (A5); alternatively actually replace (A5) by the stated Occam-sum/determinant condition. The identifiability and expectation conclusions themselves pass.

### F7 — MINOR — R4's opening status description calls its unchecked posterior input checked

**Location:** [R4:3](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/lemmas/R4_printed_outputs.md:3).

“An assembly of checked results” conflicts with R4's own correctly quoted APP status at lines 18–19: `PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied`. The dependency is disclosed later and no registry upgrade has occurred, but this blanket description does not preserve the per-input status rule.

**Minimal fix:** “An assembly conditional on W2-APP:POST; the other cited assembly inputs are checked.” Retain the exact status quote.

### F8 — MINOR — R3's fallback code description overstates its enabling condition

**Location:** [R3:24](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/lemmas/R3_delivery_assembly.md:24).

“On whenever ls0 is on” is not what the cited [v3_fit.R:151](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_fit.R:151) says: it passes `isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))`. LS0 alone does not override a FALSE fallback option. The shipped defaults enable it, so this is a false code description rather than a new obstruction under the intended configuration. Lines 141–151 of calibration describe/pass the option; the actual fallback acceptance and complete-grid freeze are later.

**Minimal fix:** require `ls0=TRUE` and `v3.grid_fallback=TRUE` in the covered configuration, say “on under the shipped defaults,” and cite [v3_calib.R:163–189](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_calib.R:163) for selection/freezing.

### F9 — NIT — R1's introductory decimal bound rounds downward

**Location:** [R1:8](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/lemmas/R1_set_sizes.md:8).

`1/log(3/2) < 2.4663` is false: the value is approximately 2.466303462. The proof at lines 39–40 uses the valid larger bounds 2.4664, 3.6996 and 4.9327, so every set-size conclusion is unaffected.

**Minimal fix:** replace 2.4663 by 2.4664 in line 8.

## Line-check record

### A1 — R1

B1.1 follows from the triangle inequality and ‖x_j‖=√(n−1). B1.2 uses ceil(x)≤x+1, including noninteger A. B1.3 correctly uses the stated E2(ii) cutoff with ω=½log n, p≤n^A and s≤K; its coefficient difference is positive. B2.1's exact simplification `(1+d log 2)/log 3=d` is correct; the resulting coefficient bounds and the j₀ branch fit below 5(A+1)(s+1). B4.1 covers both branches with the constant 3. B6.1 is valid already at n=3,s=A=1 and becomes easier as s,A grow. All feasibility restrictions needed for the cutoff are retained/eventual in the reader uses.

B3.2: independent raw Gaussian null columns become independent uniform directions in 1⊥ after centering/scaling; conditioning on the truth block/coefficient vector preserves their law in the stated model. With N_n≤p≤n^A and rank≤s₀ fixed, both logarithmic restrictions hold. The random-truth extension is authorized by [PSHARP:66–69](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-PSHARP/STATEMENT.md:66); applying its all-null corollary additionally uses p→∞, which Theorem 3 states. Only F9 remains.

### A2 — R2

Both proofs pass. Normal equations give exact orthogonal decompositions. Unit diagonal bounds the quadratic remainder by the squared ℓ¹ gap. Schur complement/interlacing gives v_T≥c; in the sample case the same argument gives residual squared norm ≥(n−1)φ₀². Thus the ratios are ≤1+L²/c and ≤1+L²/φ₀², respectively. With common deterministic L_n→0, η_n is common and tends to zero. The reader's stronger L_n→0 restriction is disclosed rather than attributed to the weaker master.

### A3 — R3: every F-UNI premise

Checked against [F-UNI:8–40](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:8).

| Requirement | Disposition |
|---|---|
| (V), Gaussian | Derived: positive definite correlation matrix in Theorem 6; nonconstant columns/response a.s. |
| (V), fixed | Carried: Theorem 7 now explicitly states nonconstant raw columns. |
| (S), same deterministic Q and feasible lattice | Derived eventually from RM2's SAND/NA/TL conclusions by union bound. The source's finite-n/eventual wording concern is expressly disclosed; no resolution of that inherited audit is asserted here. |
| (P) expectation consistency | Derived: RM2's [POST] is exactly Eδ→0, with the respective conditional input statuses retained. No expectation rate is inferred from O_P. |
| Exact maximizing start center and complete scans | Maximizer property via E4; full e4 tie rule carried in (S4). Engine lines 394–406 scan all flips/swaps; 408–414 implement strict improvement/certification. |
| LS0 cap and other caps | Verified: core lines 469–476 use the returned mode and cap ℓ+|mode|; final search uses ℓ at 453–458. Shipped settings supply ℓ. |
| Total fallback and complete freezing | Verified under both enabled options; correct code condition needs F8. |
| EX-A, IDEAL-W, EX-S, SR, GUARD-W | Carried by the expanded conventions; these are operational assumptions, not statistical deductions. Full source incorporation is the clean way to avoid further ambiguity. |
| e4/TDP-IMPL | Tie selection/cost asserted as a premise, not proved by E4. Identify the precise cost/storage contract as in F1. |
| MACH, CONFIG, complete allocation | Incomplete: F1. The table cannot establish these by attributing absent text to (S4). |
| Valid seed/allocation | “Valid” carries the input-domain restrictions; the source gives the integer-seed and finite-positive-field definitions. |
| CAL | Not needed by F-UNI; correctly not introduced. |
| [OP], N3, P1/S.3 qualifications | Retained: [OP] unchecked; N3 OPEN in the inherited e4 qualification; P1/S.3 code-reading audits. F-UNI's registry status is PROVED-CHECKED while its gate remains PENDING; both facts are disclosed. |

Hence the statistical/pathwise portion passes, but the full delivery implication does not yet pass.

### A4 — R4

The mathematical assembly passes **with N1 premises assumed**, for potential SMC records. APP [L1_POST:11–18](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:11) explicitly covers deterministic standardized θ*; no raw-coefficient substitution is needed. B2.1 gives LSF with ψ_n=c, and B6.1 gives FL-R16. Thus δ=O_P(√(log n/n)); on δ≤½, o₁≤2δ, so o₁ has the same rate. START2 IF-START⁺ under T3⁺(b), Q=S₀, gives 1_A o₀=O_P(ρ_n). Increase the finite positive constant C_R if necessary: √log n≤exp(C_R√log n) eventually. Taking the maximum therefore gives 1_A δ̄=O_P(ρ_n), exactly with **δ̄=max(o₀,o₁)**, not max(δ₀,δ). The deterministic ρ_n decreases to zero eventually, satisfying C-v's rate premise. Finite sums in Theorem 10 preserve O_P(ρ_n).

A is SMC calibration returning `ok`, fallback included; it supplies no success-probability lower bound. C-v authorizes event intersections, not conditional-on-success probabilities. F2–F3 concern the downstream reader translation; F7 concerns R4's status description. The inherited APP conditionality remains mandatory.

### A5 — PoolZ and REPORT

Pass. [Frozen STATEMENT:12–37](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S2_frozen/STATEMENT.md:12) explicitly assumes N1, R′=4 on A and the potential record. For r=1,…,4, N1:98–104 gives E[W_r|C]=1 a.s. on A; a finite union of exceptional null sets and linearity give E[(Σ_r W_r)/4|C]=1. Independence between islands is unnecessary. Data are fixed for that conditional identity; the separate joint-law paragraph correctly conditions on (data,C) before integrating. There is no unjustified assertion E[Zhat|C]=Z under a joint law with random, unconditioned data.

The pooling and island-count pins are correct: [v3_run.R:91](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_run.R:91) sets four islands and [154](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_run.R:154) computes the log of their equal-weight evidence mean. REPORT's PoolZ statement span 12–37 includes setting, claim, proof and remarks; its status source STATEMENT:13 is exact and matches `PROVED (by this seat, unchecked)`. The block's conclusion and scope match the fixed-data identity. The bridge-file/status spans also exist and cover the advertised objects; this does not make the failing R3 assembly correct.

## S1 diff disposition and reader checks

| S1 finding | S2 check |
|---|---|
| F1 negative C_beta | Fixed: C_beta>0. |
| F2 delivery premises | Partial: major omissions repaired, but F1 above remains; code wording F8 also needs repair. |
| F3 common envelopes | Fixed: deterministic common varpi_n,r_n,nu_n and deterministic neighborhoods are explicit. |
| F4 finite-sample start floor | Fixed: valid data, n≥4 and s₀<K retained. |
| F5 universal-bound domain | Fixed in reader remarks and card row 1.3: |S|≤min(K−1,p/2). |
| F6 witness overgeneralization | Fixed: named fully orthogonal/iid-Gaussian witness sequences with nonzero coefficients and the appropriate upper-bound qualification. |
| F7 leakage exponent | Fixed: c<½ at Q=S₀; c<epsilon for |Q|≤n^(½−epsilon). |
| F8 screening/null correlations | Fixed: integer budget range and “beyond” wording; full floor's null-correlation restriction acknowledged. |
| F9 inherited statuses | Fixed: TH09 and TH128 quoted separately and in full; no conversion to PROVED-CHECKED. |
| F10 intercept prior | Fixed: n-dimensional working likelihood distinguished from flat-intercept integration. |
| F11 public certificate | Fixed: exact enumeration included; public certificate distinguished from LS0 archive certificate. |
| F12 unrelated APP dependency | Fixed: removed from Theorem 4's reduction/dependency summaries. |

**Theorem 1.** B1.1–B1.3 give E,F₀,F_λ,F_w; positive beta-min gives BM(c), c=C_beta²φ₀²>c₀. POST2:C(i) is genuinely uniform at a single n with common constants; choose n₀≥2s₀ for feasibility. Its two bounds P(HPM≠S₀),P(MPM≠S₀)≤2Eδ give the stated joint lower bound 1−4Cr_n by a union bound. The BM-∞ alternative correctly allows an additional envelope-dependent onset, as noted at RV:91–92; it does not supply uniformity over arbitrarily delayed divergent envelopes. No expectation rate is transferred to Theorem 2 by this check.

**Theorem 1′.** A4′ is exactly F₀ plus **ID;c**, with the same Ω, missing-truth condition and excess-size cutoff j₀. Since L_S≥Δ_S, it implies ID^M;c. A5 gives F_w by B1.3; A0 then gives DG→ADG→OS with uniform constants/onset depending only on the fixed parameters. POST2:E and C(iii) therefore apply; retaining A5 is a stronger sufficient version of the master. The mathematical reduction passes; F6 corrects its inaccurate description.

**Theorems 3–5,8.** The changed displays/qualifications follow from the cited masters. Theorem 4's B4.1 covers Cor-G(b)'s floor range; the candidate conditional law, relative energy/beta-min, positive residual variance and allowance for varying omitted variance match that corollary. Both its expectation and HPM-error rates are stated by the master, rather than inferred from an O_P input. Theorem 5 matches FL-R16,V-R,L-R⁺ in the standardized-signal convention, with the repaired floor and separate leakage exponent. Theorem 8 preserves the unconditional output/certification/size/error intersection and the exact budget constant/domain.

**Theorems 6–7.** Statistical assumptions give the RM2 interfaces. Theorem 6's common envelopes and R2 give D-loc^b→W-R. In Theorem 7(a), |Q|=O(log n) permits arbitrarily small positive b below beta(eta,A), W-chi gives W, and truth-removal width squared is O(log n), so BM-∞ suffices. In (b), local regressions plus R2 give W-loc; the signal condition gives BM-Q→BM-W. RM-0 supplies the common data event for all admissible output runs and calibration outcomes. Only their extra delivery clauses fail F1.

**Statuses.** Registry comparison confirms the quoted per-claim statuses/versions: POST2 C/E/A1/A0 remain `PROVED (by this seat, unchecked)`; APP:POST@1.0.1 retains its full unchecked/amended label; POST:Thm-1 and SOP:TH09/TH128 retain their distinct verified/candidate labels. MISR and RM2 retain their conditional input lists; C-MIS:GDb is the declared alias of C-MIS:GD(b). RM-0/E4, SAMP C/TR/LT#/D, START2 START-R/IF-START/BR, FLOOR and SCR:A1 have the quoted checked statuses; PSHARP's abbreviated council suffix preserves its status. No quoted registry status was found upgraded. R4's blanket header is the exception described in F7, not a registry mismatch. This review does not resolve pending recorder/gate work.

## C — Plain-word card fidelity

Rows 1.1–1.3, 1.4, 3.1–3.3, 3.5, 3.7 and 4.1 otherwise match their reader/master scope and disclosed statuses, subject to the primary-reader delivery finding F1 and the retained-floor wording F6. In particular the universal-bound domain and separate start/leakage exponents are restored; PoolZ's calibration-localized mean is correct. Row 3.6 fails F4–F5 and inherits F2–F3. Row 1.4 identifies the fixed-design headline masters separately from its Gaussian-row reader corollary, so its fixed-design/uniform-residual-variance clause is source-backed. Placeholder/open/empirical rows are not being accepted as theorems here; no readability or literature-novelty assessment was made.

## Per-item verdicts

PASS-WITH-FIXES indicates a nonblocking literal/status-description correction with the mathematical implication intact. FAIL identifies an incomplete primary implication or an overstrong/undefined translated conclusion.

| Item | Verdict | Basis |
|---|---|---|
| A1 — R1 | PASS-WITH-FIXES | All bridges valid; F9 decimal typo. |
| A2 — R2 | PASS | Population and sample variance bounds valid as written. |
| A3 — R3 | FAIL | Statistical premises derived; F1 operational contract incomplete, F8 code wording. |
| A4 — R4 | PASS-WITH-FIXES | Conditional N1/potential-record assembly and rate valid; F7 status description. |
| A5 — PoolZ + REPORT block | PASS | Conditional linearity, code pooling and line/status spans correct. |
| B — Theorem 1 | PASS | Positive beta-min; uniform C(i); joint HPM/MPM bound valid; envelope onset retained. |
| B — Theorem 1′ | PASS-WITH-FIXES | Exact F₀+ID mapping and A0→OS; F6 descriptive scope. |
| B — Theorem 3 | PASS | S1-F5/F6 repaired; lower-bound domain and witnesses preserved. |
| B — Theorem 4 | PASS | Cor-G(b) plus B4.1; statuses and dependency repairs faithful. |
| B — Theorem 5 | PASS | Finite-sample restrictions and leakage exponent repaired. |
| B — Theorem 6 | FAIL | Common-event/statistical clause passes; delivery still needs F1. |
| B — Theorem 7 | FAIL | Both statistical versions pass; delivery still needs F1. |
| B — Theorem 8 | PASS | Screening intersection, floor, budget and certificate scope faithful. |
| B — Theorem 10 | FAIL | F2 complete N1 premises; F3 potential/printed/branch scope. Rate calculation itself passes. |
| C — CLAIMS_CARD v0.5 | FAIL | Row 3.6 overstates localization/recovery and conflates coefficient conventions (F4–F5); F6 wording. |

S2-VERDICT: FAIL AS WRITTEN — repair F1–F5 before acceptance; R1/R2, the POST2 rebase, R4's conditional rate calculation and PoolZ are mathematically sound, with F6–F9 as listed and all inherited statuses unchanged.
