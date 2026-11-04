# Astra (GPT-6 Astra, xhigh) Stage C review — verbatim final reply

The mathematical conclusions of all ten scoped results are **verified**, with two exposition findings and no fatal errors or proof gaps.

Line references below are to [COLLECTED_PROOFS_v1.tex](/<PC_TEMP_PATH>). I used only files in this folder and did not use review records or review-history assessments to form verdicts. Computational evidence was inspected in the supplied source and saved certificates; no numerical workloads were rerun.

## T09 — exact start and kernel validity

**No findings.**

The convolution and backward sampler establish the exact start distribution and normalizer (proof §2, lines 333–355). The elementary-kernel arguments include cap boundaries and the neighbour-swap Hastings correction (lines 358–377). Reversing the order proves self-adjointness of the averaged round; the independence minorisation survives the surrounding invariant kernels (lines 381–404). The explicit family supports the remaining negative and mixing claims (lines 417–470).

The proof establishes the stated clauses without importing additional design or statistical assumptions. Its component-level examples respect their disclosed scope.

**Verdict: verified.**

## T11(iii) — iid final-run start draws

**No findings.**

The fresh-uniform and stopping-time arguments justify independence despite adaptive consumption of random variates (proof §§1–3, lines 678–728 and 807–835). Conditioning on calibration is handled through stream separation and measurability (lines 851–864).

The main conclusion concerns absence among the specified iid draws. The separate scoring discussion distinguishes guaranteed scored independence proposals from the additional initialization-scoring premise (lines 884–890); it does not silently identify drawing with scoring.

**Verdict: verified.**

## T12 — frozen-run evidence and Rao–Blackwell identities

**Finding T12-E1**

- **Location:** Proof §8.2, line 1455; Appendix B, line 1501; embedded `certify_instance.py` in the [PDF](/<PC_TEMP_PATH>), page 62.
- **Severity:** exposition.
- **Claim:** Every enclosure width is checked by an “exact endpoint comparison.”
- **Evidence:** Endpoint extraction preserves the binary endpoints, but the width calculation uses ordinary `mpf` subtraction and an ordinary `mpf("1e-52")` threshold. The listing sets interval precision without establishing exactness of those scalar operations. Particular subtractions could nevertheless be exact; this is an unsupported exactness description, not a demonstrated incorrect width. The reported widths are approximately \(1.7\)–\(1.9\times10^{-53}\), and no theorem conclusion depends on this auxiliary width assertion.

The weighted empirical-measure induction, state-independent prefix identities and actual pre-draw reward identity are valid (lines 1349–1398). START is explicitly imported from T09. Calibration conditioning and pooling preserve the asserted identities (lines 1406–1421).

The embedded source and certificates on PDF pages 57–63 support the strict bias and conditional-product inequalities. Their frozen-component scope, including \(N=1\) and an input that production would enumerate, is explicitly disclosed.

**Verdict: verified.**

## T13 — restricted ESS and omitted mass

**No findings.**

The second-moment calculation and omitted-mass substitution give the stated identities, with coverage used at the correct temperatures (proof §§1–4, lines 1747–1815).

The witness construction uses valid standardized data, actual design-dependent blocks, the capped normalizer and the method’s budgets (lines 1820–1893). The embedded interval source and saved endpoint checks support all seven numerical inequalities used in the argument (lines 1909–2032).

The statement openly limits the witnesses to specified candidate pools and pilot-temperature inputs; it does not assert that randomized calibration reaches them. Pool avoidance and the fixed-implementation qualification are explicit and sufficient for the unchanged-grid conclusion (lines 1690, 1705 and 1895–1899).

**Verdict: verified.**

## T14(i) — singleton first-moment evidence bound

**No findings.**

The necessary weighted identity is independently derived, so this proof does not rely on an unproved T12 premise (proof §3, lines 2537–2559). The telescoping argument retains the endpoint correction and establishes both displayed bounds (lines 2571–2621). Pooling uses only the triangle inequality.

The endpoint counterexample has exact \(L^1\) error \(0.18\), exceeding the endpoint-free expression \(0.10909\ldots\) (lines 2629–2642). Its abstract scope is expressly stated at line 2411. The restriction to part (i) is explicit.

**Verdict: verified.**

## T15 — occupancy from an evidence lower tail

**No findings.**

The mean, tail and \(L^1\)-based bounds follow from H-T12 and the stated elementary inequalities (proof §§3–5, lines 2890–2927).

The counterexample uses strictly positive weights and satisfies both required moments. Its population construction establishes the weighted identity for every test function, not merely the outside-set indicator (lines 2932–3016). The conclusion is correctly limited to an abstract non-implication about substituting pooled lower tails.

The recording positions in H-T12 match those proved by T12; no extra stopping-time identity is assumed.

**Verdict: verified.**

## T20(i)–(ii) — local-search semantics

**No findings.**

The running maximum-score invariant accommodates the distinction between strict search improvement and the HPM tie rule (proof §2, lines 3298–3321). The final improving scan and its potentially unscanned returned model are handled explicitly (lines 3348–3349).

Neighbour symmetry and the stated event give the discovery, move and certification alternatives (lines 3356–3366). The score-margin argument and its probabilistic consequence follow under the explicit H03 premise (lines 3388–3410).

The proof does not assert automatic search entry or independently establish T03.

**Verdict: verified.**

## T22(i), (ii), (iv) — aggregation and endpoint propagation

**No findings.**

The completion bijection, coefficient bound and prior-ratio estimate establish the aggregation bounds, including binding-cap references. Uncapped completions are used only to upper-bound the capped normalizer (proof §2, lines 3771–3848).

The addition floor is proved directly from the score formula, including singular designs; T10 is not silently assumed (lines 3720–3766 and 3863–3879).

Hölder’s inequality establishes endpoint propagation, and the probabilistic conclusion uses exactly the stated endpoint-concentration hypotheses (lines 3890–3926). Feasibility qualifications and the broader deterministic setting are disclosed and justified.

**Verdict: verified.**

## T23(ii) — pathwise PIP and basin bound

**Finding T23-E1**

- **Location:** STATEMENT.md setting, lines 4081–4087; conclusions (ii-a)–(ii-b), lines 4113–4116; proof §1, line 4171.
- **Severity:** exposition.
- **Claim:** The unconditional pathwise statement evaluates \(o_j(S_0,1)\) even when \(S_0\notin\Omega\).
- **Evidence:** The standalone statement defines \(o_j\) only on \(\Omega\). Its convention \(u_\pi=+\infty\) outside \(\Omega\) does not define \(o_j(S_0,1)\). The proof explicitly supplies arbitrary real values outside \(\Omega\) and verifies the inequality for every such choice (lines 4171 and 4249). Thus the needed convention appears in the proof but is omitted from the standalone statement. BASIN already implies \(S_0\in\Omega\), so the expectation and MPM conclusions are unaffected.

The terminal Markov argument, entrance trials and whole-round departure control establish the claimed expectation bound (lines 4203–4328). The bad-round indicators cover the actual pre-draw recordings. Averaging and the MPM conclusion require neither particle independence nor a union bound over coordinates (lines 4348–4362).

**Verdict: verified.**

## T31(i) — Markov coverage and its limits

**No findings.**

Positivity and finite support establish log integrability; H-T12 then supplies precisely the mean identity needed for Markov and Jensen (proof §§1–2, lines 4620–4701).

The rare-tail and final-E2 constructions establish the stated non-implications for the explicitly defined class \(\mathcal L(Z)\), including both SD conventions (lines 4724–4830). They are not presented as realized SMC regression examples.

The fixed-data bound \(e^{-\Delta}Z\le\widehat Z\le e^\Delta Z\) is correctly derived and appropriately limits the interpretation (lines 4841–4859).

**Verdict: verified.**

## Cross-theorem review

No incompatible borrowed hypothesis or circular dependency was found among the reviewed results.

- **T09 → T12:** T09 proves the exact sampler and normalizer required by START. Its kernel results are consistent with the mutation operations used in T12.
- **T12 → T15:** T15’s terminal recording positions match T12’s fixed-prefix and specified-Gibbs-label identities. Arbitrary state-dependent stopping or subsequent diagnostic conditioning is not included.
- **T14 → T15:** T14 supplies an islandwise \(L^1\) bound suitable for T15(iii). A pooled bound alone does not justify substituting a pooled lower tail in the islandwise occupancy inequalities.
- **T22 → evidence accuracy:** Uniform bridge concentration alone does not establish T14’s summability requirement when the number of stages grows. Likewise, T22’s propagation on \([0,1]\) does not supply T13’s coverage at over-tempered points.
- **Statistical premises:** T20 retains H03; T22 retains its endpoint-concentration premises; T23 retains BASIN. These chapters establish conditional implications rather than those statistical or basin hypotheses.
- **Counterexample scope:** T12’s component example proves failure of conditional unbiasedness while retaining Markov coverage there. T31’s conditional-coverage failures concern \(\mathcal L(Z)\). Combining them does not produce an actual-method counterexample to conditional 95% coverage.
- **Normalization notation:** T15 and T23 locally use \(\gamma_1=\varpi m\), whereas the shared bridge uses \(\gamma_1=\varpi m/m(\emptyset)\). Their relevant normalized probabilities and ratios agree; this rescaling does not corrupt an imported identity.

## Summary

| Result | Verdict |
|---|---|
| T09 | verified |
| T11(iii) | verified |
| T12 | verified |
| T13 | verified |
| T14(i) | verified |
| T15 | verified |
| T20(i)–(ii) | verified |
| T22(i), (ii), (iv) | verified |
| T23(ii) | verified |
| T31(i) | verified |