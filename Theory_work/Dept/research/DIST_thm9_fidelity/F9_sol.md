# F9 — fidelity review and B9.5 line check
Fresh read of the proposed text against the specified masters; both hashes in `inputs.sha` verified. No scratch used.
References below: Δ = [DELTA_row21_thm9_DIST.md](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/DELTA_row21_thm9_DIST.md); master = [STATEMENT.md](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md).

- [S] Δ:22: “any O(log n) predictors” does not supply the hypotheses for the advertised entire range M₀ ≤ M ≤ √n/log n. Both sparse-direction sub-Gaussianity and the eigenvalue bound must hold through q_n(M) = min{p_raw, ⌈C_q M log n⌉}; this is O(log n) only for fixed M. State the M-dependent window, as Δ:70–82 and master:168–187 do; the upper end can require order √n predictors.
- [F] Δ:22: “Without the collinearity condition: radius larger by …” omits the accompanying weakening of the model-size conclusion. It must not leave the preceding s+C₁M bound apparently in force: the proved threshold is s+C₁M log n (master:200–202; correctly reproduced at Δ:105). State that change or expressly restrict this card sentence to the distance conclusion.
- [S] Δ:224: “Hellinger contraction … rate M_n/√n with selection, log n/n without beta-min” mixes distance and squared-distance rates. The latter is a bound for h̄_n², so its distance radius is √(C′_H log n/n), not log n/n. [W3-POST2/STATEMENT.md:104](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-POST2/STATEMENT.md:104), :111–115 establish the distinction. Label both metrics explicitly.
- [F] Δ:224: “with selection” / “without beta-min” omit required mathematical premises: D(a) assumes R1, G, (E), (F₀), δ_n→0; D(b) assumes R1, G, (E), (F₀), (OS). Both conclusions are in probability. Cite these hypotheses explicitly; the accurately quoted conditional proof status is not a substitute for them. [W3-POST2/STATEMENT.md:107](/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-POST2/STATEMENT.md:107), :112–115.

- [F/check] Δ:45–83: setup, raw/retained dimensions, plug-in intercept, true x-marginal, Hellinger normalization, prior, constants and (A1)–(A5) match master:136–183 under B9.0; no numbered hypothesis dropped.
- [F/check] Δ:89–105: (i), (ii), common exceptional event, uniformity and (iii) exactly match master:185–202. These are posterior-tail probabilities bounded in data probability, not posterior expectations; joint-law scope is preserved.
- [F/check] Δ:112–118: (A6), exactly s≥1, the M=1 window, positive b_n, divergent beta-min envelope, every M_n→∞ and convergence in P*-probability match master:209–215.
- [F/check] Δ:120–138: Corollary 9C matches master:217–238, including exact arithmetic, all completed runs on one data event, returned-list mass premise and conditional kernels. No sampler-discovery probability is asserted.
- [F/check] Δ:16–20, :22, :177–191: SOP:TH09 (T01), W3-POST:Thm-1 for 9B, EX-A for 9C, and the separate delivery conditions are carried honestly; REPORT:14–17 and CHECKPOINT_3:62–68 agree. Council pass is not presented as registry recording. Row 2.2's quoted status matches claims.tsv (W3-POST2:D@1.1.4).

D71 interpretive-sentence inventory and verdicts (references are to Δ):
- :39, :47–48, :53–59 — “recovers the joint distribution,” growing dimension/changing law, exceptional undefined data and p=p_raw, and the distribution attached to a draw: FAITHFUL to master:136–156 and B1; recovery uses the true x-marginal in the defined density.
- :66–72 — larger M gives a larger ball/smaller failure bound; window constrains joint groups and is logarithmic for fixed M: FAITHFUL, with the stated M-dependent hypotheses.
- :85–86 — no beta-min, no fixed eigenvalue floor, correlations up to 1−c_ψ/n: FAITHFUL to master:181–183.
- :98–110 — common exceptional set, uniformity, extra factor without (A4), “contracts … at the rate √(log n/n),” and size control does not identify the true variables: FAITHFUL to master:193–202; rate reading fixes M.
- :112–118 — detectable predictors give the parametric contraction rate: FAITHFUL to master:209–215, with its additional selection-theorem dependency recorded.
- :120–129 — sampler explores models rather than computing the full posterior; completed-run definition, list description, no parameter draws, and reconstructed restricted posterior: FAITHFUL to master:217–227.
- :130–138 — every qualifying completed run inherits the bound; scoring a true model of mass >½ ensures inclusion/reporting; adequate list mass is neither asserted nor certified: FAITHFUL to master:228–238 and DIST-C:297–303. These are implications, not delivery guarantees.
- :140–143 — Gaussian and independent sub-Gaussian examples; fixed-floor, autoregressive and nonnegative equal-correlation examples: FAITHFUL to master:204–207.
- :146–148 — same joint Hellinger distance/exponential form, nε_n²=M log n: FAITHFUL for (i), up to the harmless distance normalization identified in master:50 and TARGET:26–27.
- :149–153 — coded untuned prior, constant rather than diverging rate factor, printed Corollary 1 rate, parametric/output additions, and no lower dimension-growth requirement: FAITHFUL to TARGET:30, :32–34. The displayed Song–Liang Corollary 1 expression is a squared rate, as in TARGET:30; explicitly retaining ε_n² there would improve clarity.
- :154–157 — polynomial dimension, exact sparsity, extra geometric condition, and reduced exponent without it: FAITHFUL to TARGET:29–31, :34–35; arithmetic checked below.
- :158–161 — different predictor-tail assumptions and “overall incomparable”: FAITHFUL synthesis of TARGET:26–35; no unconditional superiority claim.
- :164–166 — correct Gaussian likelihood, closed conditional posterior and response-scale invariance: FAITHFUL to TARGET:200 and master B0:385–390.
- :167 — model-size control relative to s and constants depending on s,A: FAITHFUL to TARGET:201; no sparsity dependence of a rate asserted.
- :168–170 — sub-Gaussianity used for sample-moment events; population-distance transfer needs no tail condition: FAITHFUL to TARGET:202 and master:328–340.
- :171–173 — eigenvalue condition preserves the extra-variable penalty and sharp bounds; dropping it enlarges the radius; necessity for the sharp random-design rate remains open: FAITHFUL to TARGET:203 and CHECKPOINT_3:89–90, without extending the fixed-design counterexample's scope.
- :174–175 — bounded signal excludes large cancelling standardized coefficients; detectable signals yield selection and remove the logarithm: FAITHFUL to TARGET:204–205 and master:409–414.
- :204–208 — size versus identity, uncertified list mass, excluded incomplete/enumeration runs and unrecorded registry status: FAITHFUL. No internal claim IDs occur in the mathematical reader prose (:44–175); source/bridge blocks identify dependencies separately. Asymptotics are not framed as a limitation.

- [C/check, B9.5] Δ:103, :156, :201, :234: let ℓ_n=log(p_raw∨n)>0 and ε_n²=M log n·ℓ_n/n. Then nε_n²/ℓ_n=M log n, so exp(−c nε_n²/ℓ_n)=exp(−cM log n)=n^(−cM), for both the inner threshold and outer bound. This is exactly master:200–202 after B9.0, using its already assembled reader constant c; no new radius constant, factor 3, or replacement of M by Mℓ_n is needed. Preserve n≥n₀, M₀≤M≤√n/log n and remaining assumptions, equivalently M₀ log n·ℓ_n/n≤ε_n²≤ℓ_n/√n. Size remains s+C₁M log n. No sparsity-rate gloss is used.
FIDELITY: NOT-FAITHFUL
B9.5: VERIFIED
