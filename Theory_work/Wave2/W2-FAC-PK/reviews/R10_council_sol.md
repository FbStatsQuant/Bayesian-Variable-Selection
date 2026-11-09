**W2-FAC-PK — Codex council seat, round 2 (fresh review).**

**Verdict: ACCEPT. Score: 9.4/10 (uncapped). All six gates PASS. Required fixes: none.**

I independently reviewed STATEMENT v3.1, L0–L4, METHOD_REQUIREMENTS and REPORT, checked the relevant source proofs and production code, and verified every required correction in R08 and R09 against the current files. Acceptance covers (P1)–(P5) on their stated exact-Gram classes, with their named implementation premises and inherited dependency qualifications. The broader ticket remains PARTIAL: p ≫ n, the declared boundary regimes and the full-method question (P6) remain open. The proposed cap rules still require the implementation work expressly described in METHOD_REQUIREMENTS. This review does not certify that unimplemented code.

Locations below are relative to `Theory_work/Wave2/W2-FAC-PK/` unless a repository path is given.

**Six gate verdicts**

| Gate | Verdict | Independent assessment |
|---|---|---|
| 1. Correctness of every step, L0–L4 | **PASS** | The score identities, start-mode exchanges, static size-K swap bounds, counting obstruction, uniform deletion bounds, endpoint argument and potential budgets establish the stated claims. The assembly uses posterior concentration and discovery in the correct directions. |
| 2. Hypotheses used = hypotheses stated | **PASS** | P1(a,b) and PATH use PK′ and blocks of size ≤ 16. The regular-block counting used for NEG additionally requires PK and PB. No truth-keeping or proper-subset no-cancellation condition is imported. Delivery alone carries the deterministic cap bound, cap-evaluation restriction, fallback, allocation and implementation premises. |
| 3. No hidden assumptions | **PASS** | The Gaussian events, no-ties event, deterministic block partition and uniformity over retained sets are explicit. The rank boundary p = n − 1 is covered. The corrected report no longer exports the residual floor to p ≫ n. The proposed method's unaudited implementation changes are disclosed. |
| 4. Citations and statuses | **PASS** | The used FACB arguments extend under the hypotheses identified in L0; the unavailable bulk multiplier bound is excluded. The statuses of [OP], CAP, T03♯, T38-(0), Proposition F and its audits are preserved. The citation registry rerun gives 38 checks and zero misses. |
| 5. Constants and rates | **PASS** | The threshold count, deletion/swap margins, residual-floor union bound, small-energy split and path budgets track. The chain c_D → ε → c₀ is consistent, and the initial O(log n) and final O(log² n) move costs fit the fixed δ slack. |
| 6. Fidelity to the coded method | **PASS** | The production loop scans before checking the move cap, giving the prefix and scored-neighbour properties used in both theorems. Current cap selection, option collapse, preflight counts and archive formulas match the descriptions. METHOD_REQUIREMENTS identifies the necessary R/C++ plumbing, both preflight call sites, labels and common base-cap validation. |

**Verification of every round-1 required fix**

1. **R08-1, residual-floor scope: applied.** REPORT §6 G2 now restricts the proved uniform floor to p ≤ n − 1 and truth-containing feasible models. It identifies the ≤ 2ⁿ model count, records the polynomial-dictionary counterexample, and treats a floor for p ≫ n as an additional obligation. The heuristic in §5 now carries that qualification. The disposition correctly rejects R09's optional suggestion that K ≤ n/2 alone suffices for this uniform claim.

2. **R08-2, generic potential budget: applied.** REPORT §6 G1 now uses log[w(s₀)/w(k)] + ½(k − s₀)log(n + 1), followed by the binomial-coefficient bound. This follows from nested Q and the generic determinant-increment bound. The CS-specific sum of Δ_k is identified as the specialization used in L3.4.

3. **R08-3, mechanism summary: all four corrections applied.** REPORT §2 now gives at least p − K − s₀ excluded nulls, uses G_sw ≥ M_T V_{jl} and L2.2(iii)'s actual margin, retains the ε loss in the deletion bound, and applies the principal potential budget after truth recovery. It separately charges the initial O(log n) swaps and the O(log² n) remainder after first entering the small region.

4. **R09-M1, delivery implementation qualification: applied.** Both STATEMENT (P4)(iii) and L4.2(iii) explicitly refer to the method with METHOD_REQUIREMENTS' plumbing added, state that the head code cannot select the proposed rules, and disclose that existing audits do not cover the changed lines. This closes the declaration issue; it does not upgrade those lines to audited status. Proposition F's ideal-machine and code-audit qualifications remain inherited.

5. **R09-E1, deterministic deletion bound: applied.** L3.4's phase A now states that L2.2(i)'s proof uses neither PK nor PB. Reading that proof confirms it is the score identity and p ≤ n − 1 bound, without N1 or N2, that are needed here.

6. **R09-E2, exchange remainder: applied.** L1.3(b) now has |E| ≤ 6H̄. This is a valid uniform bound, and the order-n positive bracket still dominates the O(√n H̄) perturbation.

7. **R09-E3, bounded gain constant: applied.** L2.2(ii) defines c₅ := min(c₄²/8, ½), so c₅ ∈ (0, 1) is justified before the logarithmic gain bound is used.

8. **R09-E4, saturation hypothesis: applied.** L1.3(a) identifies p ≥ K + 16s₀ + 1 as PK′ and explicitly states that PB is unused in (a,b).

9. **R09-E5 and R08's citation-count suggestion: applied.** REPORT §3 now says 38 checked, matching CITECHECK and my independent registry rerun. Although R09's opening summary says four editorial fixes, its numbered list contains E1–E5; I checked all five.

The adopted optional changes are also present: METHOD_REQUIREMENTS requires a common validated LS0/preflight base cap, and L3.5 explains the trend diagnostic. They are not substitutes for any required correction.

**Independent mathematical assessment**

L0's representation and algebra remain valid at p = n − 1, where r is identically zero. The imported small-energy bound follows from the projection identity and the stated energy condition; it does not require FACB's p ≤ n/2 bulk bound.

For START, every undersaturated model leaves an available truth-free-block null under PK′. Its positive population increment dominates the logarithmic penalty uniformly. Within a truth-free block, the exchange factorization orders kept and excluded coordinates on the no-ties event. Strict population concavity dominates the uniform noise errors across bounded blocks, and PK/PB then exclude a fully retained regular block. The argument applies to every maximizer, without requiring start-mode uniqueness or truth retention.

For NEG, regular-block minima are independent because the partition and truth positions are deterministic. Their threshold probability gives a mean n^{1/2−o(1)}, which dominates every fixed n^β with β < ½. At every size-K set, a missing truth gives an order-n improving swap; otherwise an available threshold null gives a swap strictly better than every deletion. The induction consumes at most one initially excluded minimum per move. The final size argument excludes S₀ from every scanned neighbourhood, including the scan performed at the cap. This proves failure of the LS0 route, without reversing [OP] or asserting full-method failure.

For PATH, E4's chi-square union bound remains valid at the rank boundary: n − 1 − K supplies a linear residual dimension, and the ≤ 2ⁿ model count controls the simultaneous event. No independence across models is required. The centring identity and uniform tail counts control arbitrary truth-containing sets, including one-sided configurations and zero nearest distance. The small-energy and large-m splits establish the respective deletion margins with all displayed remainder terms dominated.

L3.4 establishes the endpoint before using F(S₀) as an upper budget. Missing-truth centres remain at size K until truth recovery. Afterward, improving moves preserve every truth; any remaining extra permits an improving deletion. The main truth-containing budget gives (1 + 6ε)K moves. Later additions need not preserve the small region, but the remaining potential budget still bounds all subsequent moves by O(log² n). With ε = min(δ/12, c_D/4), these costs and the initial O(log n) phase imply the claimed (1 + δ)K bound.

L4 verifies the posterior theorem's anchored eigenvalue, signal-energy and beta-min assumptions with fixed constants and A = 1. Delivery uses discovery plus D′'s pathwise scored-set inclusion, rather than inferring discovery from D_n → 0. The re-charged score, work, archive and measured-preflight terms cover caps ≤ ℓ_n + 2K under the explicitly restricted evaluation and implementation premises. The ×2 statements concern LS0 worst-case charges, as declared.

**Checks performed**

I read the relevant FACB L1/L2/L4/L5 arguments, FINAL s3/s6/s7, GEN's model/H0/[OP], HQ audits A1/A2/A4, SoP's search/HPM rules, and production `v3_engine.h`, `v3_core.cpp`, `v3_run.R` and `v3_fit.R`. I checked the cited review verdicts and the FAC-CS council statuses.

Independent checks in `reviews/R10_scratch/audit.py`, with output in `audit_output.txt`, produced:

- 30,426 neighbour-gain comparisons against direct matrix scoring; maximum absolute discrepancy 4.228 × 10⁻¹³. Cases include mixed-sign truths, three correlations and p = n − 1.
- 611 complete-scan cap-prefix checks, including cap zero and the final scan at the cap.
- 60 generic nested-Q/determinant checks, including p > n, corroborating corrected G1.
- 38 citation-registry checks, zero misses; both frozen numerical SHA256 hashes match.
- Recomputed headline aggregates: N1 has 60 rows, 55 saturated starts, 53 MR1 discovery misses and zero doubled-cap misses; N3 has 360 rows, nine nontruth endpoints and zero doubled-cap discovery misses. Scoring S₀ and ending at S₀ remain correctly distinguished.

These checks corroborate identities, control flow and reporting; the asymptotic conclusions rest on the proofs. No finite-n bound or onset is required for acceptance.

**Required fixes:** none.

**Optional suggestion:** once both round-2 replies are available, replace REPORT's pending council summaries with the actual round-1 and round-2 outcomes and file pointers, retaining PARTIAL relative to the broader brief. This is final reporting housekeeping, not a failed gate.

Only this reply and `reviews/R10_scratch/` were written. The audit verified unchanged hashes for the eight statement/proof/report/method files and four inspected production-code files during its run. No git-state-changing command was used.
