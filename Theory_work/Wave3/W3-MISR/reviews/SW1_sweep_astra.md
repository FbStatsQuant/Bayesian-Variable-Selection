# SW1 exhaustive sweep — Astra

Reviewed digest: **MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d**.

The prescribed `git diff --stat 2f360ed -- Theory_work/Wave3/W3-MISR ':!Theory_work/Wave3/W3-MISR/reviews' ':!Theory_work/Wave3/W3-MISR/LOG.md' ':!Theory_work/Wave3/W3-MISR/CHECKPOINT_*.md'` returned no output. The code-folder diff against 16a7f85 also returned no output; its last change at that pin is 72785fe.

Scope: all package files specified in the brief, excluding REPORT §2; cited source interfaces and proof steps checked, with W3-POST2 treated as declared hypotheses. No other review files were read except the permitted CITECHECK.txt (174 checks, 0 failures). Scripts were inspected, not executed or regenerated. Findings below use paths relative to Theory_work/Wave3/W3-MISR unless qualified otherwise.

1. **MINOR — substantive: N5's claimed margin verification uses a false constant comparison.**
   Evidence: `numerics/N5_energy_obstruction.py:4-7` says `200 > c_1(1..2, 1)` and that every underfit has ridge loss at least `200 log n`; the experiment has support size **two**. The formula at `../W3-POST2/STATEMENT.md:130` gives j₀=7, C_x=13.07944154 and **c₁(2,1)=258.90463899**, not approximately 161 (the latter is for s=1). The blanket premise assertion is also false for the bounded-energy control a=0: for the underfit retaining coordinate 1, L/log n tends to 200. `ASSUMPTION_MAP.md:15` uses N5 as an all-other-hypotheses-held obstruction.
   Exact fix: remove the false comparison and restrict that premise verification to the obstruction a=1. Supply the actual ridge calculation: with h=n(n−1)/n²=(n−1)/n, `L_{ {1} }=(n−1)n + 200(n−1)log(n)/n` when coordinate 1 is the huge signal; the other singleton has loss at least `(n−1)n²`, and the empty model has still greater loss. Thus min_underfit L/log n→∞ and any fixed c>258.90463899 is eventually admissible. State that the a=0 and a=1/2 runs are numerical controls, not verified instances of the ridge-margin class with c=200>c₁. This repairs a premise-verification step; it does not refute the a=1 obstruction or the principal theorem.

2. **MINOR — editorial: scalar covariance is asserted to be necessary, beyond what the example establishes.**
   Evidence: `ASSUMPTION_MAP.md:13,50-52` and `REPORT.md:71-73` say scalar covariance is necessary/needed for a named deterministic target. C-MIS `lemmas/L5_frontier.md:80-88` proves failure for one common-random-slope construction, not necessity of scalar covariance. Moreover `STATEMENT.md:97-100` expressly permits PR examples whose contrast covariance is not scalar while retaining the same named reference target and model-posterior law.
   Exact fix: replace these necessity descriptions by “arbitrary non-scalar residual laws cannot be admitted with the same mean-only target: E2 is a counterexample; scalar covariance itself is not necessary under PR.” Distinguish a conditional-mean target from the reference target used under PR. No theorem or proof change is needed.

3. **MINOR — editorial: N1's listed variances do not match the script.**
   Evidence: `ASSUMPTION_MAP.md:14` and `REPORT.md:55` give v_n∈{n⁻²,1/n,1,n,n²}. In `numerics/misr_numerics.py:99-103,115-116,134-135`, v is sigma²+tau², so the actual five variances are **2, 1+n, 1+n², 2/n, n⁻²**. The output labels at `numerics/misr_numerics_out.txt:10-29` agree with the script.
   Exact fix: list the actual five variances in both descriptions, or explicitly say that only their orders are being listed. Also add n⁻² to the script's introductory list at line 6 if that list is retained.

4. **MINOR — editorial: N1/N3 label raw coefficients as exact standardized coefficients.**
   Evidence: `numerics/misr_numerics.py:96,117,120,162,168,175` and the corresponding output headers `numerics/misr_numerics_out.txt:3,59` say θ_j²=16v log n/n. The script applies this value to the coefficients of the unstandardized random columns x. By `STATEMENT.md:32`, the standardized coefficient is θ_j=sample_SD(x_j)β_j, and the sample SD is random, not exactly one.
   Exact fix: change both printed headers to “raw β_j²=16v log n/n; standardized θ_j²=sample_SD(x_j)²β_j²” (v=1 for N3). Label numerical ratios without the sample-SD factor as nominal/population ratios rather than achieved standardized margins. Do not change the generated data to repair a description.

5. **MINOR — editorial: finite simulations are described as establishing limits or theorem conclusions.**
   Evidence: `REPORT.md:56-58` uses “δ/r_n→1.2”, “t₃ residual: no effect”, and “conclusion holds”; `ASSUMPTION_MAP.md:15,18` similarly says “keep the conclusion” and uses a limit arrow for the N2 observations. The outputs contain only four sample sizes and 100 replicates (`numerics/misr_numerics.py:29-30`). In particular t₃ is neither tested against an equality null nor shown asymptotically equivalent, and N4 establishes no asymptotic conclusion. The section's general numerical-evidence disclaimer does not make these individual descriptions accurate.
   Exact fix: say “the final sampled δ/r_n values are 1.242 and 1.216”, “no visible deterioration in these t₃ runs”, and “finite-sample behavior is compatible with the conclusion.” Apply the same finite-observation wording in the assumption map.

6. **MINOR — editorial: the heteroscedastic HPM range omits its minimum.**
   Evidence: `ASSUMPTION_MAP.md:13` reports HPM≈0.93–0.95; `numerics/misr_numerics_out.txt:64-67` reports 0.93, **0.92**, 0.94, 0.95.
   Exact fix: change the range to **0.92–0.95**.

7. **MINOR — editorial: registry assumption references point to different hypotheses.**
   Evidence: `REPORT.md:114` locates A:MISR-ESNR at `STATEMENT.md:43`, which is only the introduction to the hypothesis list, and A:MISR-IDM-SNR at `STATEMENT.md:49-50`, which is the design-only OS bridge. The actual definitions are `STATEMENT.md:45` and `STATEMENT.md:51-52`.
   Exact fix: change the ESNR pointer to `STATEMENT.md:45` and IDM-SNR pointer to `STATEMENT.md:51-52`. The existing citecheck result cannot validate the semantic accuracy of these references.

8. **MINOR — editorial: Corollary H's two reported rates refer to different powers of distance.**
   Evidence: `REPORT.md:20,153` describes a Hellinger contraction rate “log n/n without a margin, M_n/√n with selection” without saying the first is for the squared distance. `STATEMENT.md:174,177,180` proves h̄_n² at log n/n and h̄_n at M_n/√n. `ASSUMPTION_MAP.md:43` has the same missing square qualification.
   Exact fix: write “squared Hellinger distance h̄_n²: log n/n without a margin; Hellinger distance h̄_n: M_n/√n with selection.” Alternatively express both rates for h̄_n, using √(log n/n) in the first clause. Update the registry rate field consistently.

9. **NIT — editorial: t denotes two incompatible quantities in the Claim B transfer.**
   Evidence: `lemmas/G_corollaries.md:97` defines t=σ*_n and uses it as a response scale through lines 109-112, while line 108 lists “T, t, D_T, R^T_m, A^T_m” as design/reference objects. Here the imported Claim B's t is |T| (`../W3-POST2/STATEMENT.md:71`), not σ*_n.
   Exact fix: use a distinct scale symbol, e.g. a_n:=σ*_n throughout G.4, and retain t:=|T| only in the Claim B bullet.

Counts: FATAL 0; MAJOR 0; MINOR 8; NIT 1.
SWEEP-VERDICT: SUBSTANTIVE
