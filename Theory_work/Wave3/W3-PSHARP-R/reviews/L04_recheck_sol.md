S2: RESOLVED
LEMMA AE_expectation: CORRECT

Scope: L03 finding S2, the supplied L04 repair diff, Lemma F and its applications in §§4–5, and STATEMENT lines 61–72.

At `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md:81`–82, the revised definition imposes every listed condition for every integer n ≥ n₁. Since ψ_n = √ω_n + log n/(2√n) → 0, those conditions hold on some tail. The admissible integers m therefore form a nonempty subset of the integers bounded below by 3, so their least element exists. This n₁ depends only on ϵ and (ω_n).

At `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md:104`–105, the same reasoning applies jointly to ψ_n → 0 and ω′_n → 0, with m bounded below by 4. Thus the spherical n₁ exists and depends only on ϵ, (ω_n), and (ω′_n). Throughout this tail, T > 1, x_n ≥ 1, d ≥ 3, and 2 log T ≤ √n/2 ≤ (n − 1)/2. The spherical upper endpoint also satisfies θ⁺_n ≤ exp(3√n/[4(n − 1)]) ≤ exp(1/2) < 2 for n ≥ 4, and the lower endpoint is positive. These conditions support the stated application of Lemma F throughout the tail.

The dependence of both indices is permitted by STATEMENT lines 66–68. Taking n₀ = max(n₁, n_rates) as in Lemma F preserves that dependence and the conclusion for every n ≥ n₀. No monotonicity of either bounding sequence is needed.

The diff changes only these two index definitions and the repair annotations. It leaves the estimates and assembly argument intact and introduces no further issue within the requested scope.

Findings: C=0, S=0, F=0, E=0. No fixes required.
