S1: RESOLVED
LEMMA AE_expectation: CORRECT-WITH-FIXES

Scope: the supplied repair diff, the S1 finding, the repaired assembly lemma and its applications, STATEMENT §3.1, and the downstream uses in §6–§8.

**S2 — Both application indices must be tail indices, rather than first successful indices.**

Locations: `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md:80` and `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md:102`–103.

The sequences ω_n and ω′_n tend to zero but are not assumed monotone. The least n satisfying the listed conditions only guarantees those conditions at that n. A later finite spike in either sequence is allowed. Thus these definitions do not establish the hypotheses for every n ≥ n₁, as required by Lemma F. In particular, the spherical application has not established its truncation condition 2 log T ≤ (n − 1)/2 throughout that range. The issue is the quantifier in the new index definitions; the conditions themselves suffice when imposed throughout the tail.

Exact fix: replace the final sentence of §4, beginning “here the starting index”, with:

> here the starting index of the displayed inequality is n₁ := the least integer m such that, for every integer n ≥ m, n ≥ 3, n > (4/ϵ)² and ψ_n ≤ 1; it is a function of (ϵ, (ω_n)) only [L02-S1].

Replace the definition of n₁ in §5 with:

> n₁ := the least integer m such that, for every integer n ≥ m, n ≥ 4 (so d = n − 1 ≥ 3), n > (4/ϵ)², ψ_n ≤ ¼ (so 2 log T ≤ √n/2 ≤ (n − 1)/2), and ω′_n ≤ 1; it is a function of (ϵ, (ω_n), (ω′_n)) only [L02-S1].

These minima exist by convergence of ψ_n and ω′_n to zero. Their dependence is exactly the permitted dependence in STATEMENT:66–68.

Repair checks:

- Lemma F now proves its conclusion from its hypotheses. The added restriction on n₁ and the choice n₀ = max(n₁, n_rates) resolve the original S1. At the stated tolerances, |θb − 1| + |1 − θ²| ≤ 4|θ − 1| + 2|1 − b| ≤ 3ϵ/8 < ϵ/2, so the algebra yields the required inequality uniformly.
- With the tail-index correction, §4 ensures n ≥ 3, T > 1, a_n > 0, x_n ≥ 1, and [a_n, 1] ⊆ (0, 2]. These are the preliminary conditions needed by the displayed estimate and Lemma F.
- With the tail-index correction, §5 additionally ensures d ≥ 3 and x_n ≥ 1. The claimed chain is correct: log T ≤ ψ_n√n and ψ_n ≤ ¼ imply 2 log T ≤ √n/2, while √n ≤ n − 1 for n ≥ 3. The spherical upper endpoint also meets Lemma F's bound: exp(3 log T/(n − 1)) ≤ exp((3/4)√n/(n − 1)) ≤ exp(1/2) < 2 for n ≥ 4. Its lower endpoint is positive. Moreover, n > (4/ϵ)² > 16 and (r₀ + 1)log(pn) ≤ ω′_n n ≤ n ensure r₀ + 1 ≤ n/log(pn) < n/2, as required for m = n − 1 − r₀ ≥ n/2 in the event estimate.
- The supplied diff changes only the repair annotation in the header, Lemma F's starting-index hypothesis and proof endpoint, and the §4–§5 application indices. After the local index correction above, no downstream change is needed in §6–§8: the resulting common n₀ remains independent of the design and null block, preserving conditional uniformity, the limit statement, and the simultaneous sub-block application in §8.

Finding counts: C=0, S=1, F=0, E=0.
