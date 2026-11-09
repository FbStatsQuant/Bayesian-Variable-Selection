# R05 — Line-by-line check of L4 assembly

**Verdict: VERIFIED-WITH-AMENDMENTS.** The statistical assembly of (P4), the reading of NEG, and the uniform LS0 scan/request bounds are correct given Theorem PATH. The delivery argument correctly uses discovery and the pathwise scored-set inclusion, rather than reversing the bound on D_n. The resource argument needs an explicit convention/premise for evaluating an arbitrary cap rule. The amendments below also correct cost wording and inconsistencies in METHOD_REQUIREMENTS. No fatal defect found in the assembly for the three explicitly proposed, cheaply evaluated cap rules.

Scope: reviewed `lemmas/L4_assembly.md` against locked STATEMENT v3 (P4)/(P5), METHOD_REQUIREMENTS, FACB L5.1/L5.4, FINAL s3/s6/s7, HQ audits A1/A2/A4, GEN's [OP], C-GROW L4, and production `v3_fit.R:26–70` / `cpp/v3_core.cpp:465–480`. PATH is taken as given; its proof is not re-reviewed. No source, implementation, or git-state changes were made; only this review file was written.

## Numbered issues

1. **MAJOR — Arbitrary measurable cap rules do not by themselves have bounded evaluation cost.** Location: L4:20–22, 36–42; METHOD_REQUIREMENTS:14–15, 40–45.

   The theorem quantifies over any finite-integer-valued measurable data function a. Its deterministic output bound controls the subsequent search, but does not bound the work/memory needed to evaluate that function. Thus “the only count that changes is LS0's” is justified for the three displayed arithmetic rules, but not for an arbitrary implementation of such a rule. A bounded cap function can require arbitrarily expensive computation; measurability does not even imply computability. Lemma CAP establishes path/scored-set properties for abstract measurable cap parameters, not a computational envelope for evaluating them. Lemma R expressly restricts CONFIG and excludes unrestricted user functions (`C-DLV/lemmas/L1_resources.md:100–108`).

   **Fix:** state explicitly that the general measurable rule is an abstract supplied cap parameter, with evaluation outside the charged fit, or require its evaluation work/memory to be included in W_G′/M_G′ and the corresponding allocation. For the three proposed implemented rules, record that their evaluation has bounded arithmetic overhead absorbed by the implementation constants. Parts (i)/(ii) need no computational restriction. This is a resource-scope amendment, not an objection to PATH or the statistical claim.

2. **MINOR — The cost multiplier is an upper bound, not an exact multiplication of every term.** Location: L4:54–58; METHOD_REQUIREMENTS:40–45, 50.

   Put s_0 = ℓ_n+K+1, s_1 = ℓ_n+2K+1, and r = s_1/s_0 ≤ 2. The scan-dependent work and measured-time charges scale linearly. However, score requests include the additive centre request: 1+s_1 q ≤ r(1+s_0 q), with inequality generally strict. Likewise the archive formula is A(s)=c s+d with c,d>0, so A(s_1) ≤ r A(s_0), not equality. Moreover, the deliberately loose memory-envelope increments C·2K(2K+1) and C·K(K+1) have ratio greater than two; the factor claim must concern the underlying LS0 archive charge, not the ratio of these particular envelope increments. L4.4 must also explicitly restrict its cost statement to a ≤ ℓ_n+2K; MR-PK's statistical lower bound alone allows arbitrarily large caps.

   **Fix:** use “for cap rules with a ≤ ℓ_n+2K, each LS0 worst-case charge is bounded by at most r times its MR1 charge”; distinguish these charges from conservative delivery envelopes and total fit runtime. Replace “doubles” in METHOD_REQUIREMENTS:50 by “increases by at most a factor two.” The realised-work identity is correctly restricted to a ≥ MR1 and to data where MR1 already terminates certified.

3. **MINOR — Missing ceiling in the candidate-rule scan bound.** Location: METHOD_REQUIREMENTS:20 (table).

   For a = ℓ_n+⌈(1+δ)|S̃₀|⌉ the deterministic scan bound is ℓ_n+⌈(1+δ)K⌉+1. The displayed ℓ_n+(1+δ)K+1 can be smaller. For example δ=1/4 and K=301 give the integer bound ℓ_n+378, whereas the table gives ℓ_n+377.25. L4's common bound ℓ_n+2K+1 is unaffected because ⌈(1+δ)K⌉ ≤ 2K for 0<δ≤1.

   **Fix:** restore the ceiling in that table cell.

4. **MINOR — METHOD_REQUIREMENTS overstates what transfers through CAP.** Location: METHOD_REQUIREMENTS:28–31.

   “Every result proved under MR1 ... holds verbatim” exceeds CAP's conclusion. FINAL s7 explicitly separates scored-set/HPM transfers from negative statements, flags, metadata, and cap-dependent no-output events. A discovery-failure assertion cannot be transferred to a larger cap by scored-set inclusion. Also a rule below MR1 does not automatically satisfy a ≥ ℓ_n; the example without the max can fall below the legacy cap, so even legacy transfer needs that lower bound.

   **Fix:** enumerate the positive discovery, certified-endpoint-on-event, and joint-HPM conclusions that transfer under their original hypotheses; retain the resource exceptions and cap-dependent events/metadata qualifications. In the parenthesis require a ≥ ℓ_n, for example max(ℓ_n,⌈(1+δ)|S̃₀|⌉). L4 itself correctly avoids transferring a negative result upward.

5. **MINOR — Complete the deterministic justification for the p-based cap example.** Location: L4:22–23.

   The parenthesis verifies the lower bound only on {|S̃₀|=K}. That is sufficient for an event-based discovery proof, but the stated general cap-rule hypothesis is a datawise lower bound. The stronger proof is available: under (PK), eventually p ≥ (17/16)K deterministically, since liminf p/K > 16/15 > 17/16. Since |S̃₀|≤K on every admissible input, max(ℓ_n+|S̃₀|,p) ≥ max(ℓ_n,⌈17|S̃₀|/16⌉) for every input at those n. Its deterministic upper bound is valid. No probabilistic saturation event is needed for this example.

   **Fix:** replace the event-qualified lower-bound explanation with this argument; if a hypothesis is required at every early index as well, define a finite-prefix adjustment respecting the common bounds. This matches the locked statement's “eventually” qualification for this example.

6. **EDITORIAL — Extra-request comparison uses a valid but needlessly loose number.** Location: L4:38–39.

   The difference between the displayed new and A2 request bounds is exactly Kq(p), not 2Kq(p). The current “at most 2Kq(p) more” is true. The 2Kq(p) increment used in W_G′ is correctly measured from the legacy-cap envelope W̄, whose LS0 allowance is ℓ_n+1 scans.

   **Fix:** write “Kq(p) more than A2, or 2Kq(p) more than the legacy bound underlying W̄.” Do not subtract the increment from W_G′ on the basis of the A2 comparison.

7. **EDITORIAL — Make delivery provenance and the complete allocation explicit.** Location: L4:5–10, 39–45.

   The statuses actually quoted for T38-(0), T03♯, [OP], GEN, CAP, and A2 match the cited records; no status upgrade was found. The input paragraph should additionally retain A1's “HOLDS-WITH-AMENDMENTS” and A4's “OK-WITH-FIXES” (fixes applied), and distinguish the council's d315c1e statements from the later preflight allocation addition checked by A4. The current text inherits the correct allocation through Proposition F, but does not display the critical sums P_e+A′; an isolated list of archive bytes is not itself an allocation inequality.

   **Fix:** add those provenance qualifications and display the sufficient allocation:

       mem_n ≥ max{βM_G′+β₀, P₀+A′, P₁+A′},
       time_n ≥ max{2(τW_G′+τ₀), P̄_t, P̄_LS0′},
       allocation$mem_gb ≥ mem_n/2^30,
       allocation$hours ≥ time_n/3600.

   Here A′ is L4:41's archive expression, W=⌈p/64⌉, dimensions are raw dimensions (p_raw=p here), and U_K bounds the entire 200-iteration timed interval, including model construction, sorting, and scoring. These are clarifications of the allocation already inherited from FINAL s6:33–44 / A4:7–25, not additional statistical assumptions.

## Checks that pass

- **(H0), L4:12–16:** the extension from p≤n/2 to p≤n−1 is sound. Sign conjugation preserves eigenvalues; all principal normalized Grams have minimum eigenvalue at least 1−ρ. Thus both anchored eigenvalue hypotheses of T03♯ hold, including its deterministic tail cutoff m_n♯ (which exists since R_K=0). Fixed nonzero truth coefficients give BM-∞; fixed truth size and fixed coefficient energy give the signal-energy bound; p≤n gives A=1. Bounded posterior deficit converts convergence in probability into convergence of its expectation, without asserting an expectation rate.
- **(P4)(ii), L4:29–30:** PATH gives a common high-probability event on which the selected cap reaches and scans S₀. The cap-free [OP] argument bounds D_n in the correct direction. T38-(0) is used with CAL as declared. The additional liminf equality follows from P(output and correct)=1−P(U_n)−o(1).
- **Delivery, L4:31–45:** fixed standardized CS designs supply Lemma S's input conditions even at p=n−1; positive Q_S and Gaussian response nondegeneracy suffice. Neither a relevance bound nor p≤n/2 is needed. The deterministic upper cap bound is expressly required on every admissible input, not merely on PATH's event. With issue 1 resolved, Lemma R's counting extends beyond ℓ_n+K by recharging the LS0 terms. P(no output)=0 uses the total fallback, ideal-machine premises, allocation, and audited exit exclusions. Consistency then follows from the displayed pathwise inclusion and P(output)=1, without CAL or any reverse inference from D_n→0.
- **Counts and formulas, L4:37–41:** a+1 complete scans and 1+(a+1)q(p) requests are valid, since feasible flips are at most p and swaps at most k(p−k)≤p²/4. W_G′ is a valid conservative legacy-envelope increment; M_G′ is also conservative (model size remains ≤K). The archive formula exactly matches `v3_fit.R:45` after replacing its scan count by s′. The factor 1/100 in P̄_LS0′ is correct: ŝ_K≤(τU_K+τ₀)/200 and the preflight uses 2s′q(p)ŝ_K. Memory is checked before timing; rejection uses strict >. The current production core still uses MR1 (`v3_core.cpp:473,479`) and the R preflight still uses ℓ_n+K+1; METHOD_REQUIREMENTS correctly presents MR-PK as a proposed implementation change, not an implemented fact.
- **NEG, L4:47–51:** discovery failure under MR1 makes [OP]'s upper bound uninformative and gives no lower bound on D_n. Failure transfers downward to the legacy cap. The full-method question remains open; no SMC-discovery or full-method inconsistency theorem is asserted.
- **(P5) scope:** the allowance gap is supplied by the accepted NEG/PATH inputs; neither L4 nor locked P5 establishes optimality within it. The cost conclusion is valid as an upper-bound comparison of LS0 terms with the wording in issue 2, and says nothing about total fit runtime or empirical speed.
