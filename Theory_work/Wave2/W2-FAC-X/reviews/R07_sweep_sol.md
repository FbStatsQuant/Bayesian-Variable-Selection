Counts: **FATAL 0 / MAJOR 0 / MINOR 3 / EDITORIAL 9** — **12 findings**. No FATAL/MAJOR item was found in the proof of (C1)–(C4). The findings below concern the current files, not defects already repaired in earlier rounds. Asymptotic scope is respected; neither asymptotics nor the size of an onset is a finding. X7 is excluded. The quoted dependency-status strings in STATEMENT §7 and X6's input list match the cited sources; no status-mismatch finding is asserted.

1. **MINOR — The lower-band counting display drops its kept endpoint.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X4_path.md:136–138`; band definition at `Theory_work/Wave2/W2-FAC-X/lemmas/X2_perturbation.md:59`.

   **Reason:** For a finite negative endpoint a, the lower band is `(a-w,a]`, whose reflected coordinate interval is `[|a|,|a|+w)`. The display instead uses `(|a|,|a|+w]`. In particular, the kept null at a belongs to the band but is excluded by the displayed counting window. Unless a point happens to sit at the other endpoint, the first inequality undercounts by one. The ultimate D7 bound is obtainable, and the later B3 application only needs deleted band points, so this is a local counting error rather than a failure of the path theorem.

   **Fix:** Use the exact reflected interval `[|a|,|a|+w)` and dominate it by D7's `[|a|,|a|+9ϖ)`. Its comparison tail consists of kept nulls of the relevant sign plus at most 15 omitted points. Alternatively, explicitly count only deleted lower-band points, in which case a is absent. Make the corresponding upper-band convention explicit.

2. **MINOR — Empty maxima have no stated convention in the new concentration event.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X2_perturbation.md:15–17`; compare the admissible dimensions in `Theory_work/Wave2/W2-FAC-X/STATEMENT.md:49–51`.

   **Reason:** The theorem permits p=s₀, including p=s₀=1. Then D4's maximum over all nulls is a maximum over the empty set, and for p=1 D2's off-diagonal maximum is also empty. X2 does not state a convention for either expression. FAC-B L3 explicitly supplies an empty-maximum convention, but that local convention is not stated for X2's newly defined event. As written, 𝔈_n is incompletely defined on allowed bounded-dimension sequences. This is not a complaint about bounded p or asymptotics.

   **Fix:** State that maxima of these nonnegative quantities over empty index sets are zero, or write the conditions as universal inequalities over the indicated indices. Also read eigenvalue assertions about principal submatrices as applying to nonempty submatrices.

3. **MINOR — The fixed signal vector needs an explicit embedding into the moving support.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/STATEMENT.md:50–53`; uses at `Theory_work/Wave2/W2-FAC-X/lemmas/X5_start.md:19` and `:34–37`.

   **Reason:** (θ) defines ϑ as an s₀-dimensional vector indexed by r=1,…,s₀, while (FS) immediately uses ϑ_i for original predictor indices i∈S₀ and sums over subsets of S₀. Support positions are explicitly arbitrary. For example, with S₀={100}, the literal symbol ϑ_100 is not a coordinate of the defined one-dimensional vector. X5 also compares θ*_j to ϑ_j using original predictor indices. The intended identification is clear, and the proof works with it, but the hypothesis and subsequent formulas need that identification stated.

   **Fix:** Define the zero-extended vector ϑ⁽ⁿ⁾ by ϑ⁽ⁿ⁾_{i_r(n)}=ϑ_r and ϑ⁽ⁿ⁾_j=0 off S₀, and use it in support-indexed sums and comparisons; equivalently state explicitly that all support-indexed uses of ϑ mean this embedding. This is a notation clarification of the locked hypothesis, not a new restriction.

4. **EDITORIAL — N denotes both a number of degrees of freedom and an omitted index set.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/STATEMENT.md:59–66`; `Theory_work/Wave2/W2-FAC-X/lemmas/X4_path.md:85–86` and `:265–268`.

   **Reason:** N is defined as n−3, then reused for a subset of null indices. X4 quantifies over the latter N but later writes the numerical lower bound `(1−ρ)N/2` in the truth-move proof. The intended meanings can be recovered from types, but the same symbol has incompatible meanings within the statement/proof chain. There is a related scalar/vector collision: STATEMENT `:68` defines a_T as a gap endpoint, while X1 `:66` uses a_T for the subvector of Gaussian a-coordinates.

   **Fix:** Reserve N (or d_n) for n−3 and use another letter, such as E₀, for the omitted null set. Write the Gaussian subvector as bold a_T or `(a_j)_{j∈T}` so that it cannot be confused with the gap endpoint.

5. **EDITORIAL — The closing X1 summary reintroduces an undefined perturbation scale.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X1_representation.md:135–136`.

   **Reason:** The text states `|δ| ≤ β_n = n^{−c}` and refers to β_n-perturbations, although β_n is not defined. The locked statement deliberately reserves β for raw regression coefficients and defines the single perturbation scale ϖ_n. Moreover, the proved relation is an eventual upper bound by a negative power, not an asserted identity of ϖ_n with that power.

   **Fix:** Write that X2, with the band-count absorption in X4, gives `|δ_j(T)| ≤ ϖ_n ≤ n^{−c}` on the relevant structured sets, and refer to ϖ_n-perturbations of the null partial statistics. Keep the separate treatment of truth moves explicit.

6. **EDITORIAL — X1 points to the wrong numerical experiment for perturbation size.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X1_representation.md:6`; actual experiment descriptions in `Theory_work/Wave2/W2-FAC-X/numerics/N1X_summary.md:1` and `Theory_work/Wave2/W2-FAC-X/numerics/N2X_summary.md:1`.

   **Reason:** The header cites “numerics/N2X (perturbation size, lemmas/X2)”. N2X is the heterogeneous-loading/Target-2 experiment. The iid compound-symmetric path perturbation proxy is reported in N1X. This does not affect the analytical perturbation proof, but the evidence cross-reference is incorrect.

   **Fix:** Cite `numerics/N1X_summary.md`, and call the reported fitted statistic an empirical perturbation proxy, as that summary does.

7. **EDITORIAL — The reported self-test upper bound is rounded downward.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X1_representation.md:4–6`; source `Theory_work/Wave2/W2-FAC-X/numerics/iid_selftest_out.txt:5`.

   **Reason:** X1 claims a discrepancy `≤ 4.4·10⁻⁸`, but the output records `WORST over all steps: 4.447e-08`, which exceeds that literal upper bound. A rounded approximation and a rigorous inequality are different assertions, even for evidence-only numerics.

   **Fix:** Use “approximately 4.4·10⁻⁸” or an upward-rounded upper bound such as `≤ 4.5·10⁻⁸`.

8. **EDITORIAL — X2's numerical ratio range does not match its cited table.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X2_perturbation.md:4–5`; source `Theory_work/Wave2/W2-FAC-X/numerics/N1X_summary.md:13–24`.

   **Reason:** The header says the ratio is “2.1–3.1 in all completed runs”. The cited table reports maxima ranging from 1.48 to 3.10 across its rows, with several other values below 2.1 (1.72, 1.84 and 1.91). Also, N1X explicitly describes δ̂ as a fitted empirical proxy, rather than the exact δ_j(T) defined in X1. The header should not suggest that the table directly measured the latter.

   **Fix:** Say that the tabulated maxima of the empirical proxy ratio range from 1.48 to 3.10, and preserve the distinction between that proxy and the analytically defined perturbation.

9. **EDITORIAL — A discarded probability calculation remains inside the D2 proof.**

   **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X2_perturbation.md:30–31`.

   **Reason:** The sentence includes the unfinished expression `P(|W_jl| > √(2N)·√(12 log n)·½…) — precisely`. It is neither a complete probability assertion nor the formula subsequently used. The next line contains the valid conditional Gaussian bound, so the unfinished fragment adds ambiguity without supplying an argument.

   **Fix:** Delete the fragment and start directly with the conditional bound `P(|W_jl| > ‖u_j^⊥‖√(6 log n) | u_j^⊥) ≤ 2n^{−3}`, followed by the stated union bound and norm event.

10. **EDITORIAL — The header mislabels the full soft-gap containment claim.**

    **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X3_softgap.md:5–7`; compare `:34–41` and `Theory_work/Wave2/W2-FAC-X/numerics/N3X_out.txt:2`.

    **Reason:** The header identifies the band containment as “(vi)/(vii)”. Those clauses are the wide-phase deletion bound and the initial-phase statement. The full two-sided band containment used by X4 is (viii), which is also the containment label in the numerical output.

    **Fix:** Refer to “the full band containment (viii), the initial-phase bounds (vii), and the crossing bound (iii)”; mention (vi) separately if its phase-specific bound is intended.

11. **EDITORIAL — The nondegeneracy-event inclusion is reversed.**

    **Location:** `Theory_work/Wave2/W2-FAC-X/lemmas/X4_path.md:286`; definition at `:47–49`.

    **Reason:** The text writes `ND_n ⊆ 𝔊_n`. By definition, 𝔊_n is the intersection of ND_n with the other events, so the correct inclusion is `𝔊_n ⊆ ND_n`. ND_n alone supplies none of the concentration or spacing conditions. The actual proof uses the correct fact that nondegeneracy holds on 𝔊_n.

    **Fix:** Reverse the inclusion, or simply write “since 𝔊_n includes ND_n as an intersected condition”.

12. **EDITORIAL — The locked version is misidentified in the frontier heading.**

    **Location:** `Theory_work/Wave2/W2-FAC-X/STATEMENT.md:105`; current version at `:4–6`.

    **Reason:** The Target-2 heading still says “not part of v2's claims”, although the file is the locked v3 statement. The body correctly keeps Target 2 outside the present theorem, but the stale version reference makes that scope annotation less precise.

    **Fix:** Change the heading to “not part of v3's claims” or, more durably, “not part of Theorem FAC-CS-iid”. No claim or hypothesis needs to change.
