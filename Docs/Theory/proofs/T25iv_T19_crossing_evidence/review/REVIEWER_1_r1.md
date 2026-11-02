No findings.

The proof establishes precisely the conditional T25(iv) variance statement and four-island pooling in `STATEMENT.md`.

- **Finiteness (§2):** The finite state space and finite bridge scores give deterministic bounds on the evidence ratios, justifying all expectations and second moments used.
- **First moment (§2, equations (5)–(7)):** The conditional resampling-and-mutation identity, weighted empirical-measure induction, and kernel invariance correctly establish \(\mathbb E_c W_t=1\). This argument does not assume that \(W_t\) is a martingale.
- **Variance bound (§3, equations (8)–(9)):** The pathwise evidence update gives the stated second-moment increment exactly. PW2 yields the affine recursion, whose displayed solution correctly propagates each slack term through only subsequent stages. Subtracting one therefore gives \(B_T\).
- **Island pooling (§4):** Conditional independence eliminates covariance terms. Averaging four island ratios divides the entire bound, including the slack sum, by four, while retaining \(N=N_e\).

The argument keeps PW2 as a hypothesis, introduces no additional substantive premise, and does not condition on final diagnostics. The PDF and TeX contain the same mathematical argument. No step within the requested scope remains unverified.

Verdict: verified
