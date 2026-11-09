**Verdict: NOT PASSED as the complete submitted package. Score: 8.6/10 (uncapped).**

I find P1–P5 and their proofs L0–L4 sound on the stated exact-Gram classes, subject to the named implementation and imported-result qualifications. The blocking issue is a new, overbroad uniformity claim in REPORT §6, which was absent when R07 reviewed the package. It is repairable by narrowing the report; no change to STATEMENT v3.1 or the principal proofs is requested. This is not an objection to asymptotic onsets or a request to solve the declared frontiers.

Locations below are relative to `Theory_work/Wave2/W2-FAC-PK/` unless otherwise specified.

| Gate | Verdict | Reason |
|---|---|---|
| 1. Correctness of every step, L0–L4 | **PASS** | The algebraic imports, saturation/exchange argument, initial-swap counting argument, uniform static gain bounds, endpoint argument, path budget and assembly are valid on their stated events. I found no blocking gap in these proof files. |
| 2. Hypotheses used = hypotheses stated, P1–P5 | **PASS** | PK′ suffices for saturation and PATH; PK and PB enter the stronger block-count and NEG conclusions. Truth keeping, proper-subset no-cancellation and a two-phase path are not assumed. P4 distinguishes statistical discovery from delivery and states the cap-value, evaluation-cost, fallback, allocation and machine premises needed for the latter. |
| 3. No hidden assumptions or out-of-scope imports | **FAIL for REPORT; PASS for P1–P5** | REPORT:92–93 exports the residual floor as design-free under Gaussian noise alone, while its uniform proof needs a bound on the number of models. The omitted dimension restriction matters asymptotically. REPORT:89–91 also carries the CS-specific Δ_k into an assertion about any design. Required fixes 1–2 address these report-level overextensions. |
| 4. Adequate dependency status; no upgrade | **PASS** | The quoted T38-(0), T03♯, [OP], CAP and Proposition F/A1/A2/A4 statuses agree with their sources. The unchecked-by-seat qualification on [OP], the code-reading audits, and the separate post-council preflight check remain visible. FACB's council pass does not substitute for checking its imports outside p ≤ n/2; L0 performs that check explicitly. |
| 5. Constants and rates | **PASS for L0–L4** | The threshold tail, uniform residual-floor constant, small-energy refinement, tail-count interpolation, small/large-m splits and ε-to-δ budget close. All error terms are negligible for fixed ρ, fixed nonzero coefficients and fixed sparsity. REPORT's compressed mechanism needs the corrections in item 3 to describe these actual bounds accurately. |
| 6. Fidelity to the specified/coded method | **PASS** | The code completes its extra scan before the cap exit, tests strict improvement before that exit, and distinguishes scoring from moving and certification. METHOD_REQUIREMENTS now identifies the R option normalization, C++ Boolean, post-mode cap computation, labels, and both preflight call sites that adoption must change. Resource recharging includes work, archives and measured-score preflight; delivery retains its ideal-machine/audit qualifications. |

Because gate 3 fails, the numerical score does not constitute a council pass.

The principal mathematical checks support the following assessment. L0's Gaussian projection representation remains valid at p = n − 1 with r = 0; its determinant, quadratic, neighbour and Q-versus-RSS identities do not need p ≤ n/2. L1's truth-free-block increments are uniformly positive, its within-block exchange is ordered by ξ, and strict population concavity dominates the uniform noise perturbation. These statements apply to every maximiser, so start-mode ties create no missing case.

L2 uses uniform size-K scan bounds rather than a favourable path history. An omitted truth supplies an order-n swap; otherwise an initially excluded extreme block minimum supplies a swap beating every deletion. The regular-block minima are independent because the partition is deterministic. Their lower-tail count is n^{1/2−o(1)}, and each move can absorb at most one. The final cardinality argument excludes S₀ from every scored neighbourhood, including the scan at the cap. It gives no lower bound on D_n and no failure theorem for the full method, as the statement correctly says.

L3's E4 union bound is valid on this ticket's p ≤ n − 1 class, including the rank-boundary case. The centring identity and tail counts control arbitrary truth-containing sets, including one-sided configurations and zero nearest distance. The small-energy multiplier bound is the applicable FACB refinement, rather than its unavailable p ≤ n/2 bulk bound. Endpoint existence is established before F(S₀) is used as an upper budget. The initial truth-recovery phase costs O(log n) moves; the small-region remainder remains bounded even if later additions leave that region. With ε = min(δ/12, c_D/4), these remainders fit the fixed δ slack. L4 then uses posterior concentration and discovery in the correct directions, including the CAL-free pathwise delivery argument.

Required fixes:

1. **MAJOR, report scope — restrict the purported design-free uniform residual floor.** Location: `REPORT.md:92–93` (G2).

   Gaussian noise and K ≤ n/2 alone do not imply a constant-fraction residual floor simultaneously over all size-K models when p is polynomially larger than n. The proof's union bound over at most 2ⁿ sets uses p ≤ n; it cannot be exported without that restriction or another explicit bound on the model-family size.

   A concrete asymptotic counterexample to the exported claim is available under model G. Take odd n = 2K + 1 and decompose the centred contrast space into K mutually orthogonal two-dimensional planes. In each plane put n deterministic unit directions with angles rπ/n, r = 0,…,n−1, and scale the columns to norm √(n−1). Thus p = Kn ≤ n². Put a fixed nonzero truth on the angle-zero column in the first plane. Select that truth and, in every other plane, the dictionary direction nearest the Gaussian noise direction. This is a truth-containing model T of size K. For independent standard Gaussian plane coordinates Z_b,

   RSS_T/σ² ≤ Z_{1,2}² + [π/(2n)]² Σ_{b=2}^K ‖Z_b‖².

   Consequently RSS_T/(nσ²) → 0 in probability. The design is fixed; only selection of T uses the data, exactly what a uniform-over-T claim must allow. This counterexample concerns G2's generalization, not the exact-Gram CS theorem.

   **Fix:** state G2 for the current p ≤ n − 1 class, or give a separate generic version with an explicit model-count condition, such as p ≤ Cn with constants allowed to depend on C. Restrict to T ⊇ S₀ to reuse the current central-projection argument directly. For p ≫ n, list a uniform residual floor as an additional proof obligation rather than a consequence of Gaussian noise alone. No solution of F1 is required.

2. **MINOR, mathematical wording — replace the CS-specific budget by a genuinely generic one.** Location: `REPORT.md:89–91` (G1).

   The displayed Δ_k contains the CS determinant increment L_k − L_{k−1}. For a general Gram matrix the determinant contribution depends on the model, so that exact quantity cannot be used verbatim in the claimed bound for “any design.” For example, take orthogonal standardized truth/extra columns and a response orthogonal to the extra. Adding the extra leaves Q unchanged and incurs determinant increment log n. In contrast, the CS increment at size two is L₂^{CS} − L₁^{CS} < log n for ρ > 0. Hence the displayed exact budget fails for this family at every n, although the discrepancy tends to zero.

   **Fix:** use the valid generic nested-model bound

   F(S₀) − F(T) ≤ log[w(s₀)/w(k)] + ½(k − s₀)log(n + 1),  k = |T|.

   Nested Q is nonincreasing, and each added column increases the determinant penalty by at most log(n + 1). This gives the intended leading budget with log C(2p − 1, K), without a CS-only Δ_k. Alternatively label G1 explicitly as the CS specialization of a generic potential-budget principle. The scratch calculation confirms the determinant discrepancy; it is an identity check, not an objection about finite-n recovery.

3. **MINOR, proof-summary fidelity — restore the qualifications lost in the mechanism paragraph.** Location: `REPORT.md:40–48`.

   Four compressed statements are stronger than the proof:

   - A saturated start need not contain all truths, so it excludes at least p − K − s₀ nulls, rather than necessarily p − K nulls.
   - The swap bound is G_sw ≥ M_T V_{jl}, with the removal and recentering costs included; it is not generally G_sw ≥ M_T τ_l². Cite L2.2(iii)'s actual lower bound ½log n + 2.
   - L3 gives the small-region deletion bound (c_D − ε)log n for each fixed ε > 0, rather than the unqualified c_D log n written here.
   - The budget K(½log n + 2.4) is applied after the first truth-containing centre C_{i₁}. It is not established for the original start when that start misses truths. The proof separately charges O(log n) truth-recovery moves using its larger K log n + Cn budget.

   **Fix:** make those substitutions and describe the final move count as the main truth-containing budget plus the O(log n) initial phase and O(log² n) remainder. L3.4 already contains the correct argument; only its report summary needs repair.

Optional suggestion: update `REPORT.md:60` from “33 checked” to the current “38 checked.” The registry rerun finds 38 entries and zero misses. This is an editorial count correction, not a failed provenance gate.

I checked the specified FACB imports, FINAL s3/s6/s7, GEN [OP], HQ audits A1/A2/A4, relevant SoP definitions, and the production search/cap/preflight lines. I consulted the earlier review trail after forming the principal proof assessment. Independent direct-matrix checks covered 3,670 feasible neighbour comparisons at p = n − 1, with mixed-sign truths and two correlations; the maximum gain discrepancy was 8.44×10⁻¹⁴. The frozen numerical-file hashes match, and recomputation supports the reported N1/N3 discovery aggregates. These checks corroborate identities and reporting, not asymptotic proofs.

Reproducible checks and output are in `reviews/R08_scratch/audit.py`, `audit_output.txt`, `CITECHECK_rerun.txt`, `aggregates.py` and `aggregates_output.txt`. Only that scratch directory and this review file were written. No proof, method, numerical source or git state was changed.
