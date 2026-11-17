# Council R1 — sol — blind first read

Reviewed the frozen manifest `6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243`. All 23 listed file hashes match. Consumed claims are accepted as stated, with the conditional statuses supplied in the brief.

| id | decision |
|---|---|
| W3-D2:Thm2X | ACCEPT |
| W3-D2:Cor2X | ACCEPT |

Both acceptances retain the inherited conditions. The failed overall gate below concerns supporting numerical evidence, not the analytic derivations of these claims.

## Findings

**F1 — Incorrect numerical cutoffs and reported grid maximum.** [numerics/N1_floor_and_e2e.py:27](/home/fb31/BVS-wt/W3-D2/Theory_work/Wave3/W3-D2/numerics/N1_floor_and_e2e.py:27), used at lines 40–41, subtracts nearly equal large `lgamma` values. At p = 10¹⁵ this loses enough precision to change m♯_n. For example, `log_comb(2*p-1, 1)` returns 40.0 instead of log(2p−1) ≈ 35.2319235755.

For the actual grid case A = 3, s₀ = 1, n = 100000, p = 10¹⁵, the script returns m♯_n = 95; the defined cutoff is 76. Independently using 65-digit decimal arithmetic, R₇₅ / threshold ≈ 1.6740958541 and R₇₆ / threshold ≈ 0.8370479270, where threshold = n^{−3/2}. The discarded tail after k = 500 contributes less than 3.9 × 10^{−128} relative to the threshold.

A stable recurrence q_{k+1}/q_k = (p−k)/(2p−1−k), with a short product for w(s₀), changes 19 of the 150 cutoffs. The recomputed maximum ratio is approximately 0.3928391, rather than 0.3942 as reported in [numerics/N1_out.txt:15](/home/fb31/BVS-wt/W3-D2/Theory_work/Wave3/W3-D2/numerics/N1_out.txt:15) and summarised in [TARGET.md:24](/home/fb31/BVS-wt/W3-D2/Theory_work/Wave3/W3-D2/TARGET.md:24). Thus the description “computed exactly in log space” and the stated numerical maximum are inaccurate. Replace the unstable combination calculation and regenerate the numerical evidence and its summaries. The weaker “at most 0.40 on the grid” observation survives, and neither registered claim depends on this computation.

**E1 — Label an unchecked side assertion explicitly.** [REPORT.md:42](/home/fb31/BVS-wt/W3-D2/Theory_work/Wave3/W3-D2/REPORT.md:42) says “B is strictly stronger on LB's domain, per the note.” This is attributed to an unchecked note and sits inside a proposed work estimate, but is not explicitly labelled HEURISTIC or OPEN as REPORT lines 3–5 prescribe. Add that label to distinguish the proposed implication check from this ticket's established results. This editorial finding makes no judgment about the proposed implication.

No C or S finding against either registered claim.

## Proof and scope checks

- **Master instance and posterior identity:** PROOF P1 correctly uses q = 0, a = γ = τ² = 0. The empty omitted contribution has the required degenerate conditional Gaussian law; (N), deterministic parameters, positive residual variance and candidate Gaussian rows hold. With 𝒞 = [p], the two posteriors are the same coded target on the same inputs.
- **Floor and thresholds:** For n ≥ max(3, 2s₀), support membership gives p ≥ s₀ and hence s₀ ≤ K. B4.1 then applies with its required polynomial dimension bound. It covers every nonempty set needed by G2 step 2; the empty set creates no missing condition. Restricting the application to this eventual range is legitimate because the master's proof checks the hypotheses at the current n.
- **Clause (E):** The diverging beta-min branch permits the fixed margin c′ = c₀(s₀,A) + 1. Together with M = 2M₀ + 1, φ₀² = c/8 and C_OS = C_OS(s₀,A), this gives C depending only on (s₀,A,M₀,c). The threshold may depend on the sequence. The remainder and the factors b_n and 2b_n are valid.
- **Deterministic facts and Markov:** P0 proves the PIP and selection-event inequalities, including ties and S₀ outside Ω. These apply to every data set where the posterior is defined; the model gives that domain almost surely. P2 correctly yields all four expectation/probability rates.
- **Corollary:** The recorded constant-floor hypotheses are quoted faithfully. Unit diagonal gives R = Σ_n; the energy bound follows from λ_max ≤ trace = s₀ and the coefficient bound; beta-min diverges. Markov and a union bound yield precisely the recorded O_P and simultaneous-selection conclusions. The replacement floor of size 3(…) is also sufficient.
- **Strength and caveats:** STRONGER is justified against the recorded constant-floor reader statement. Both the conditional-status caveat and the distinction from the old vanishing-floor master are retained. The REPORT registry blocks match STATEMENT, including clause (E), scope and inherited conditions; the proposed card sentence preserves coexistence with row 1.2.
- **Evidence sweep:** All ten DEPS span hashes reproduce their sha and checked_sha fields. The named prior review files were not opened, as the brief expressly prohibits them; their substantive review coverage is therefore not independently attested here. The supplied CITECHECK output was inspected; its script was not executed because it reads the registry and writes a prohibited file. The numerical scorer matches the supplied coded-target formula. The grid calculation was reproduced and independently recomputed as described in F1. No scratch files were created.

## Interpretive sentences within the registered spans

1. **STATEMENT:39, “Then, under the joint law of (X^r, ε)” followed by the display — checked.** The master and P0–P2 give exactly this joint-law conclusion.
2. **STATEMENT:48, “and k_n = O(log n), so b_n = O(r_n)” — checked.** B4.1 and fixed A,s₀ give the size bound; both remainder terms are O(r_n).
3. **STATEMENT:55–56, “Then (A1)–(A3) … hold with …” — checked.** P3 verifies the specified constants and the displayed beta-min lower bound.
4. **STATEMENT:56–57, “Hence the four bounds … and with them the three conclusions …” — checked.** Theorem 2X, Markov and the selection-error union bound establish both parts.
5. **STATEMENT:58, “The same holds with the floor asked only on … 3(…)” — checked.** P3 uses that smaller range directly.
6. **STATEMENT:63, “As [MISR] MIS-R (i) consequence 1 … ‘for every data set’” — checked as attribution of the PIP inequality.** The cited source explicitly supplies that inequality; P0 independently supplies the two selection-event inclusions, on the posterior's domain.

There are no further “reading,” “interpretation,” or “this means” sentences in the specified spans.

## Six gates

| gate | result | reason |
|---|---|---|
| correct | PASS | Both registered claims follow from the consumed inputs; no analytic gap found. |
| strength | PASS | The strengthened reader statement and both caveats are justified. |
| faithful | FAIL | F1: supporting numerical cutoffs and the reported maximum are inaccurate. |
| statuses | PASS | The supplied conditional statuses are faithfully retained. |
| sweep | FAIL | The numerical evidence sweep found F1; claim copies, registry blocks and DEPS hashes otherwise agree. |
| reader | PASS | The registered reader conclusions and coexistence proposal are supported. |

Score: **9.2/10.0**. The analytic claims are accepted; the supporting numerical evidence needs correction before all gates can pass.

Better-theorem proposals: none required for this review.

COUNCIL-VERDICT round=R1 manifest=6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243 seat=sol score=9.2 gates=FAIL
