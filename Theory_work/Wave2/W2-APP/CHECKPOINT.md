# W2-APP — CHECKPOINT (key lemma proved and checked), 2026-11-09

**Status.** STATEMENT v1.2 locked (R01 LOCK-WITH-CHANGES, 10 changes applied; v1.2 = R03 item 1).
Key lemma: **Theorem LOC** (lemmas/L3_LOC.md) — reported-model consistency for random Gaussian designs whose correlation
is exponentially local along some (unknown) ordering, bounded spectrum, + PTV (population truth visibility), for the
method as merged at 4676af6 (shipped LS0 cap ℓ_n + |S̃₀|; no method requirement). New ingredient: NA without the
Markov property (window innovations, uniform |Z − Z′| = o_P(1)). Check R03 (Sol xhigh): VERIFIED-WITH-AMENDMENTS,
no FATAL; variant LOC-B (growing blocks, small-log regime) V-W-A after adding the enlarged-Q bound.
Other lemmas: L1_POST (posterior level under a log-sparse correlation floor; λ_max never needed) R02 V-W-A;
L2_CT (Combes–Thomas + uniform conditional decay) R02 VERIFIED; L5_VN (visible nulls force large start modes →
GEN/GROW/LOC routes obstructed on STAR, growing blocks, equicorrelation/factor with non-cancelling signal) R04 V-W-A.
Falsification numerics: ct_check PASS, post_check PASS; helper numerics n1–n3 and real-design diagnostics running.

**Headline so far (to be checked):** POST holds for every family asked (incl. equicorrelation/factor) given a fixed
floor of the population correlation matrix. Reported model: covered for iid, AR(1), exponentially decaying Toeplitz /
ARMA, fixed-bandwidth banded Σ or Σ⁻¹, bounded blocks (any size, incl. > 16), growing blocks up to (1 − δ₀)log n/s₀,
each + PTV (automatic with ≤ one truth per independent block). Bounded spectrum alone is NOT enough for any current
route (STAR counterexample); polynomial-decay Toeplitz: unproved; pervasive factor with non-cancelling signal:
route-obstructed (FAC pending).

**Left.** L4_families check; mid-point review; Part 2 (real designs) assembly; sweep; citecheck; council; REPORT.
No narrowing foreseen beyond what R01 imposed.
