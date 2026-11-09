# C-DLV — Codex council seat, round 2

**SCORE: 9.0/10 (uncapped). Verdict: ACCEPT the stated reduction package, with one minor bookkeeping correction.**

Fresh review of the current files; no C1_* council files were opened. This verdict concerns P1–P5, the conditional/joint conclusions C1–C2, and the hypothetical fallback F1. It does not certify target (T).

| Gate | Verdict | Reasons |
|---|---|---|
| G1 — Correctness of proved claims | PASS | The inventory and call-graph invariants support the reduction to tier-1 construction failure under the stated premises. The ESS identity, convexity argument, pilot cap, and two-model insertion proofs are sound. L5 correctly distinguishes appended trials from the possible terminal trial and reserves an additive 1 for the latter. The minor per-draw cost correction below fits inside the existing resource envelope. |
| G2 — Stated versus used hypotheses | PASS | EX-A, IDEAL-W, MACH, CONFIG, GUARD-W, OP-LS0, e4 and TDP-IMPL expose the arithmetic, allocation, implementation and configuration obligations. TDP storage is explicitly an implementation requirement rather than attributed to W1-N3. C2 invokes the design hypotheses of W1-GEN/W1-PXN and uses their data-only conclusions, avoiding an assumption of successful calibration. |
| G3 — No hidden assumptions | PASS | Allocation success, dependencies, interruptions, fixed concurrency, default test functions, and certificate budgets are expressly scoped. No full-space ESS, mixing, candidate-inclusion, or asymptotic two-model hypothesis is silently supplied. The polynomial allocation has unspecified implementation-dependent constants; it is an existence envelope, not an instantiated hardware guarantee. |
| G4 — Citation status and scope | PASS | W1-N3 L7 supplies the stated reference-algorithm operation bound. W1-GEN C1/C2 and T03♯ supply deterministic-search discovery and posterior concentration; W1-PXN T/P supply the LH-iid counterparts under that ticket's hypotheses. L4 D′ gives its own pathwise transfer, so it does not import CAL through an output theorem. The cited sibling reports support the recorded PROVED-CHECKED status, without implying production integration or HQ adoption. |
| G5 — Constants and rates | PASS | The resource bounds distinguish operations, words, preflight bytes, measured preflight time, and the guard's extra just-completed-operation term. The insertion bound's constant 22, the shorter-range correction, the 60-halving threshold, and the rounded-down cutoff n ≤ 2.277·10^8 check out. Finding 1 corrects a subordinate rate without changing the final envelopes. |
| G6 — Code/specification fidelity | PASS | The escalation and sticky grid-failure logic in v3_calib.R supports the exact schedule_limit characterization. The analysis retains the constructor's post-bisection snap and validation, and does not replace the actual pilot by an ideal schedule. LS0 and the e4 fallback are identified as specified components absent from the shipped core. F1 is expressly a proposed change to calibration, not a claim about current production behavior. |

**Classification and open item.** The proved/conditional/finding/open split is honest. In particular, STATEMENT.md:47–48 explicitly withholds (T); :66–73 retains the delivery term; and L4_delivery.md:74–88 confines unconditional delivery to a changed calibration law. The numerical evidence is appropriately limited: the tested fits never reached tier 1, and the selected pairs fail the two-model remainder test. These observations do not establish the required asymptotic event.

The exact open item is correctly stated at STATEMENT.md:76–81:

`P(SL_n) = P(E_n ∩ F¹_n) → 0`,

where E_n is the actual tier-0 escalation-trigger event, and F¹_n is failure of a construction in the realised tier-1 run through interval overflow, non_progress, or failed post-snap validation. A hypothetical tier-1 experiment under an unconditional calibration law would not settle this intersection. Nor is a universal pilot-count slack bound necessary if escalation itself vanishes. The two sufficient routes O-a/O-b preserve these distinctions.

**Numbered findings**

1. **[MINOR] The per-start-draw work bound omits sorting the emitted indices.** Evidence: `Theory_work/Wave1C/C-DLV/lemmas/L1_resources.md:61` gives π₀ draws cost `O(J·B + K)`, but `Scripts/SMC_BVS/core/cpp/v3_start.h:158–174` ends every draw with `std::sort(S.begin(), S.end())` at line 174. Blocks are visited in packing order, which need not be global index order; a general size-k draw therefore requires a sorting allowance `O(k log(k+1))`. **Required fix:** replace the displayed per-draw bound by `O(J·B + K log(K+1))` and explicitly charge the sorting term to the existing per-request envelope. Since `K ≤ min(p,n/2)`, this additional cost is bounded by a constant times `p(n+2)`, already present in L1:39 and :73. Every initial/independence draw is followed by a counted evaluation, so neither the final polynomial allocation nor Theorem D needs to change. No FATAL or MAJOR finding.

**Verification and limits.** I read the required statement, inventory, requirements, five lemmas, numerical summaries, recorded citation audit, production implementation, relevant specification/notation sections, and cited sibling results. Read-only checks found:

- All 18 compared production/copy R and C++ source/build files agree byte for byte.
- The citation checker reports 153 checked references and zero missing/out-of-range references; this checks locations, with theorem scope assessed separately above.
- The supplied pilot-only check, executed using standard-library dependencies, gives 300 runs, zero cap/end-point violations, and maximum k/T_e = 1.
- Independent 70-digit Decimal checks give zero violations in 120 finite-family ESS-identity/variance-envelope trials and 400 two-model closed-form/inequality trials. They also reproduce a passing endpoint in the snap band that fails validation at 1, and non_progress for a sufficiently steep abstract two-model family.
- Independent high-precision recomputation confirms the insertion constant and the stated non-progress cutoff.

The complete supplied N2/N2b suites could not be rerun because the available Python lacks mpmath. Their saved outputs were inspected; no packages were installed and no numerical evidence files were rewritten. The numerical checks supplement the mathematical/code review and do not prove asymptotic delivery.
