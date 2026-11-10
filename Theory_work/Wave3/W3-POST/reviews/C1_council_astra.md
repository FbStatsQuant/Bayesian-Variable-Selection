# C1 council seat A — independent adversarial review

Reviewer: OpenAI gpt-6-astra, high. Date: 2026-11-09. Package reviewed: STATEMENT v1.2 and the accompanying proof, assumption map, numerical code/output, draft report, citation checker, and R01–R03 trail.

**Verdict: NOT PASSED. Score: 7.5/10 (uncapped).** I found no fatal error or counterexample to Theorem 1 items 1–6 or the formal statements of Lemmas 1a and 1a′. The blocking defects are in the requested sharpness/literature package, not the central posterior proof. Counts: **0 FATAL, 2 MAJOR, 6 MINOR, 1 NIT**. Repair and resubmit; do not mark this round council-passed.

Paths below are relative to `Theory_work/Wave3/W3-POST/` unless an alias from STATEMENT is used. Earlier verdicts were checked as historical records, not used to establish correctness.

## Six gates

| Gate | Verdict | Reason |
|---|---|---|
| G1: correctness of every step | FAIL | The core derivations pass my audit, but the literature and rate conclusions contain unsupported or incorrect implications (F1–F3). |
| G2: hypotheses used = hypotheses stated | FAIL | The formal theorem passes; REPORT drops coefficient restrictions needed by its energy and random-design summaries (F4), and the Song–Liang comparison drops distributional qualifications (F3). |
| G3: no hidden assumptions | FAIL | The package-wide comparisons silently require additional qualifications about design distributions, dimension growth, and what constitutes a rate lower bound (F1–F3). No additional hidden assumption was found in the central proof. |
| G4: cited lemmas have adequate status | PASS | Registry quotations for T03♯ and T02(i♯)/(ii♯) match the source; POST and L1a′ retain “PROVED (by this seat, unchecked)” with separate check records. SL's checked deterministic statements suffice. Pending C1 lines are appropriately pending. |
| G5: constants/rates tracked | FAIL | Core constants and rates check out, including C′_Λ, the g₀ factor in q_n, and the underfit exponent. Package sharpness assertions exceed the proved rate evidence (F1); numerical quantities also need accurate labels (F5). |
| G6: fidelity to the method as coded | PASS | Retained-column p, cap, per-model BB weight, ridge determinant/quadratic, response standardisation, and ν=0.01+n/2 match the real-arithmetic target. Sampler outputs and floating-point equivalence are not asserted. |

## Independent proof audit

**Lemma 1a.** [P1]'s contrast transformation correctly changes the inverse-gamma shape to 0.51, leaving exponent 0.01+n/2. The scale event is used through deterministic mixed-endpoint inequalities, not by conditioning Gaussian noise on response scale. The numerator is a mixture of proper densities at a data-free rate. Keeping the exact prior ratio R_m cancels the reference prior weight. The denominator integral over `[σ², σ²(1+n^−1/2)]` gives the stated √n normalisation and C_Λ. Markov splitting at √L gives precisely the displayed probability bound. The cutoff substitution is valid; even for growing reference size t≤K, `(1+1/n)^(t/2)≤exp(1/4)`.

**Lemma 1a′, line by line (`lemmas/L1a_size_tail.md:20–41`).** The variational objective has penalty θᵀ(G+I)θ/n. Substituting the exact representation gives `Q_T^c≤||ε_c||²+ρ`, with `0≤ρ≤M+M′`; neither rank nor a floor is needed. Replacing R_n by this deterministic nonnegative ρ in the denominator exponent is legitimate. The determinant bound remains valid for singular G_T. The mean bound is `1/√2+1/2+(M+M′)/(2σ²)`. The numerator identity and mixed-endpoint transfer apply with any fixed reference T∈Ω. Their assembly gives the claimed c♯ and tail probability. T=∅ and R_m=0 cause no problem with the stated conventions. Uniformity follows from the common constants, without independence between the numerator variable and Λ′. The coefficient-bounded corollary in STATEMENT correctly retains energy control for growing sparsity.

**Theorem 1 item 1.** I checked [T03R] C1–C10 against the actual [P3] steps. B1 supplies rank and determinant growth on the large anchored unions; B3 needs the normalised floor only on the smaller model S₀. B2 supplies the stronger floor for small-extra-variable underfits. C6(a) uses monotonicity and determinant interlacing with no large-union normalised floor. Comparisons outside Ω are legitimate positive auxiliary weights. The truncated χ² moment gives the factor `(1+1/g₀)^(j/2)` inside q_n; it is not incorrectly absorbed into a constant uniform in j. The large-underfit exponent satisfies `(j₀+1)/2≥s₀(A+1/2)+1`, giving `n^−1 (log n)^((j₀+1)/2)=o(r_n)`. For c>c₀, the factor 1−1/n is absorbed eventually. The tail, supersets, and underfits therefore give the stated O_P(r_n).

**Items 2–4.** These follow directly from mass outside S₀. In particular the bounded-functional supremum equals δ_n, the threshold condition controls both sides of q_n, and boundedness of δ_n gives expectation convergence without an unjustified expectation rate. The HPM bound is independent of tie-breaking on δ_n<1/2.

**Item 5.** [T03R] §5 and [P1]'s one-superset proof require no beta-min and no F_λ beyond the truth floor. For strong signals, C10 applies to each missing strong coordinate and the union has at most fixed s₀ members; the other coefficients need no lower bound. The specificity counterexample is independently valid: in R03 §5A, with L=1/2 and b²=0.75, the log-weight coefficients for ∅, either truth singleton, the truth pair, proxy singleton, either truth/proxy pair, and the triple are respectively `0, −0.125, −0.25, 0.175, −0.31818…, −0.75`. The proxy has a strict logarithmic gap, stochastic fluctuations are O_P(√log n), and the Gram floor is 1−√0.9>0. Thus the finite p=3 example suffices within R1.

**Item 6, including the lead's extension.** Gaussian sample-correlation concentration followed by size-times-entrywise-error and Weyl gives F_λ and F_w with common constants. Bounded coefficients and fixed s₀ give energy. Raw slopes require the sample-SD event; standardised slopes use the conditional contrast law. Removing only the lower coefficient bound does not affect these steps. Apply the fixed-design 5(a)/(b) bounds over design/coefficient sequences with common upper bounds; the same diagonal contradiction gives joint tightness, including design-dependent J_n(c). Hence the extension is justified, although POST's original setting alone is not its literal statement.

## Findings and fixes

### F1 — MAJOR — rate optimality and YWJ comparison overclaimed

`ASSUMPTION_MAP.md:69–75,97–99`; `REPORT.md:90–92`.

The E0 medians and a heuristic heavy-tail explanation do not establish a uniform lower bound for the stated rate. In particular, the fixed-p experiment does not settle the √log n factor for growing p. A per-model log penalty also cannot by itself establish total superset mass: multiplicity, dependence, and the slab matter. “p^−c is faster” needs a relation between p, n, and c; for fixed p it does not even tend to zero.

The YWJ explanation is incomplete in a consequential way: its hyperparameter condition involves both g of order p^(2α) and κ, and its posterior-concentration and rapid-mixing results use different sparsity conditions. The concentration theorem can use an untruncated model space; a small hard cap is not a universal prerequisite of that theorem. See [Yang–Wainwright–Jordan, Assumptions C/D and Theorems 1/2](https://arxiv.org/pdf/1505.07925).

**Fix:** label the growing-p optimality discussion a conjecture, retain E0 as empirical fixed-p evidence, and either prove a separate lower-bound proposition or remove “not improvable”/“not a weakness of the proof.” Compare rates only in an explicit shared dimension regime. Correct the YWJ cap and hyperparameter description and distinguish its two theorems.

### F2 — MAJOR — Narisetty–He design assumptions misrepresented

`ASSUMPTION_MAP.md:62–67`.

The description suggests a positive restricted minimum-eigenvalue condition analogous to this package's floors. Their Condition 4.5 controls minimum **nonzero** eigenvalues and explicitly permits exact singularity; the separate identifiability Condition 4.4 controls residual signal against underfits. This distinction is central to the requested sharpness comparison, especially E2/E3. The signal threshold is expressed through log(√n∨p_n), not unconditionally just log p_n. See [Narisetty–He, Conditions 4.4/4.5 and §6](https://arxiv.org/pdf/1405.6545).

**Fix:** replace the recollected paragraph with an accurate separation of identifiability, nonzero-eigenvalue regularity, and prior rates. Explain that their singular-design allowance differs materially from F_w. Qualify any simplified beta-min rate by its dimension and residual-signal assumptions.

### F3 — MINOR — Song–Liang comparison omits needed qualifications

`ASSUMPTION_MAP.md:37–49,55–57`; `REPORT.md:99–101`.

I read printed pp. 952–956 of the supplied PDF. Theorem 1 uses bounded predictors and approximate sparsity; Theorem 2 uses strict sparsity and r_n≫1. These should not be merged into one hypothesis list. The covariance-floor implication for Condition 3 on p. 955 is derived for centred bounded predictors; the Gaussian calculation has its own qualification. Covariance control alone does not imply the exponential identifiability condition for arbitrary predictor laws. Also, the Gaussian verification of Condition 1 is for zero means/unit variances; item 6 permits unrestricted means, which disappear on sample centring but need not satisfy Condition 1 on the raw scale. Finally K=min(p,⌊n/2⌋), not always ⌊n/2⌋, and the size-tail proof uses signal/reference control as well as the prior.

**Fix:** state the two theorem settings separately; attach bounded/Gaussian qualifications to the eigenvalue implication; compare centred predictors; restrict the cap objection to p≥n/2; replace “from the prior alone” with “from the exact prior tail and reference-model marginal-likelihood bound.” Condition 2 is a predictor-moment condition, only analogous to energy control under appropriate coefficient bounds.

### F4 — MINOR — report summaries drop coefficient and reference-size conditions

`REPORT.md:24–27,39–40,72–73`.

Fixed s₀ alone does not make energy automatic. For example s₀=1 and θ=√n has coefficient cost ||θ||²/n=1 but signal energy of order n². The random-design summary/implication similarly needs the coefficient upper bound, and items 1–4 need the lower bound (or another valid BM condition). The cutoff is O(log n) under fixed reference size, not arbitrary growing s₀; for general T its definition must use t=|T|.

**Fix:** copy the bounded-coordinate qualification from STATEMENT, identify the T-based cutoff, qualify the logarithmic cutoff by fixed t, and retain upper/lower coefficient conditions in the random-design summary and implication list.

### F5 — MINOR — numerical claims need exact quantities and scope

`ASSUMPTION_MAP.md:15–19`; `REPORT.md:86–88`; `numerics/post_exact.py:109,238`.

The output reports medians of random quantities, not their deterministic values or limits. E5's 0.9882 is a median at n=25600, not a limit “→0.99.” L1a′(b)'s maximum at n=100 is 1.043e−3, exceeding the claimed ≤10^−3. E4 γ=1 has HPM error 15% at n=100, so the full displayed range is 15–50%, not 25–50%. The code applies the advertised coefficients to Xr before standardisation; they are raw slopes, with θ*=D_xβ afterward. That distinction is asymptotically harmless here but makes the literal finite-n θ labels inaccurate.

**Fix:** label medians, use the exact ranges, distinguish empirical trends from proved limits, and label the generating coefficients β or generate the signal after standardising X. Retain the independently valid p=3 proof as the evidence for asymptotic specificity failure.

### F6 — MINOR — simulation dimension exceeds the inherited protocol cap

`numerics/post_exact.py:126`; `numerics/post_exact_out.txt:1`.

The runs enumerate p=12; Wave1 PROTOCOL's compute rule specifies exact enumeration p≤10, and Wave3 inherits it. No exception is recorded in this package.

**Fix:** run a compliant p≤10 version and update its outputs/claims, or have HQ explicitly record an authorised exception. This is a protocol issue, not a mathematical objection to enumerating 4096 models.

### F7 — MINOR — named design family remains inside the theorem

`STATEMENT.md:92–105`.

Item 6 embeds a Gaussian-row design family in Theorem 1, contrary to Wave3 PROTOCOL rule 4 and PROGRAM's presentation rule. The general interface paragraph does not remove that occurrence.

**Fix:** move item 6 to a separately identified sufficient bridge/example and state the joint-law theorem through the high-probability AF/energy/coefficient interface. Preserve the proved Gaussian application and no-beta-min extension.

### F8 — MINOR — general-dimension benchmark suppresses boundary terms

`ASSUMPTION_MAP.md:18,78–81`.

The deletion contribution is `n^(a+1/2−c/2+o_P(1))`, not simply `n^(a+1/2−c/2)`. Moreover log p/log n→a alone does not justify a strict necessity assertion at the boundary c=2a+1 or c=2a+2: a subleading term in log p can dominate √log n fluctuations. For example log p=a log n−(log n)^(3/4) changes the boundary comparison while preserving that ratio limit. At fixed p the stated constant-coefficient boundary obstruction is valid.

**Fix:** state leading-order thresholds with a fixed positive margin, retain o_P(1), and analyse equality using the actual log p sequence. Describe these as deletion obstructions, not a complete sufficiency theorem for arbitrary replacement geometry.

### F9 — NIT — citation checker advertises broader coverage than implemented

`citecheck.py:4–12,33,53–57,109`; `reviews/CITECHECK.txt:1`.

The 52/0 record is real, but most checks establish range existence, and status checking uses three hard-coded entries rather than extracting every status quotation. The alias regex does not implement every advertised citation syntax. It does not establish literature accuracy or validate all reviewer-verdict summaries. I independently checked the quoted registry statuses and review verdicts; no status upgrade was found.

**Fix:** describe this as selected citation/range/token checks, or implement the advertised extraction and coverage report. Keep manual semantic citation review distinct from the zero-failure count.

## Disposition

The formal posterior results are supported by the audited chain, including the new L1a′ denominator argument and item 6's extension. Correct the package's comparative claims and summaries before requesting the next council round. This review does not upgrade any input status and does not certify sampler-level consistency. Only this review and files under the authorised scratch directory were written; no git state changes were made.
