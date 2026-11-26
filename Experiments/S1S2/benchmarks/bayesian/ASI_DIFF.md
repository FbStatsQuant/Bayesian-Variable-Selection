# ASI: the authors' original MATLAB code vs the PARNI-repo R code

> **Decision (owner, 2026-11-25, relayed by the manager).** Because of the differences below, ASI is run as the authors' original `ASI_sampler.m` v3.0, unmodified, under user-space GNU Octave 10.3.0 (`fit_asi.R` with the driver `asi_octave/run_asi.m`; built and tested the same day, no shims needed). The PARNI R `ASI()` is the comparison code (`fit_asi_parni.R`, not registered), not the code that runs. Where this file says "Used" or "HQ ruled that the PARNI R code runs", that describes the state before this decision.

| Option | What it runs | Fidelity to the paper's own code | Status |
|---|---|---|---|
| PARNI R `ASI()` @3b95d66, script settings | R, on Owls as shipped | not a line-by-line match: D-1 to D-10, seven not reachable through arguments | withdrawn as the ASI benchmark; kept as `fit_asi_parni.R`, not registered |
| R port of `ASI_sampler.m` | our code | would be a reimplementation | withdrawn by HQ ("No R port") |
| Original `ASI_sampler.m` v3.0 under Octave | the authors' file, unmodified | exact, by construction | **chosen and built**: `fit_asi.R`, sampler sha256 `4705c795…3b10dddb` checked before every run |


## Decision table, D-1 to D-10

Text = Griffin, Łatuszyński & Steel (2021), Biometrika; pages are PDF pages 1–17. "Tested" refers to the one sensitivity run made (section "How large the differences are"): PARNI run with the original's κ, ζ start and step exponent changed a PIP by at most 0.001 (S1-like) and 0.096 (S2 SNR 6), against a seed-to-seed change of 0.003 and 0.147; selections were the same. Every other effect was untested when this table was written, because the `.m` had not been run then; the first runs of the `.m` are in the section "The `.m` under Octave against PARNI" at the end. D-1 to D-8 change how the proposal is tuned, not the posterior; D-9 changes the prior; D-10 changes the run length.

| # | Item | Biometrika text | `.m` line | PARNI file:line | Follows the text | Effect on PIPs and on the PIP > 0.5 selection | Recommendation |
|---|---|---|---|---|---|---|---|
| D-1 | κ | "We use κ = 0.001", Sec 2.4 p.9 | 0.0001, m.160 | 0.001, r.378, e.71 | PARNI | immaterial; tested (with D-3 and the exponent of D-2) | keep each code's own value |
| D-2 | ζ step | eq (11) p.9; φ_i = O(i^−λ), 1/2 < λ ≤ 1, p.7 | 2/it^0.55, after every chain move, 0 for an empty proposal, m.251 | it^−0.7, once per iteration, empty proposal counts as accepted, r.386–387, r.260–261 | both exponents are inside the stated range; the factor 2, the timing and the empty-proposal rule are not in the text | exponent: immaterial, tested. Rest: untested | cannot be set in PARNI without editing `ASI.R` |
| D-3 | ζ start | not stated | ν/(hp), 0.1 here, m.92–95 | 0.5, e.77 | text silent | immaterial; tested | keep each code's own value |
| D-4 | lower bound on ζ | Δ = 2Σ min(π_j, 1 − π_j); ζ = 1/Δ if ζΔ < 1, Sec 2.4 p.9 | min, m.412–420 | **max**, s.213–215, r.392–398; almost never binds | `.m` | untested. The bound matters when most π_j are near 0 or 1, as in sparse problems | the one PARNI line that contradicts the text; needs a code edit |
| D-5 | range of ζ | ζ in (ε, 1 − ε), eq (11) p.9 | logit ζ clamped to [−3, 3], m.422–427 | no clamp; ζ can sit at 1 − ε, s.360–361 | PARNI (the clamp is not in the text) | untested. In PARNI the S1-like runs end with ζ at its upper limit, acceptance 0.65; the `.m` would stop at 0.953 | needs a code edit |
| D-6 | π after burn-in | "Rao–Blackwellised updates of π were only calculated during the burn-in", Sec 4.3 p.14 | π keeps moving with the plain γ draws when `adap_type = 1`, m.259–261 | π frozen after burn-in, r.374 | both fit the sentence; the text does not say what π does afterwards | untested | needs a code edit, or `adap_type = 0` on the `.m` side |
| D-7 | when π, ζ are updated | chains "share the same proposal parameters", p.7; Algorithm 2 is for one chain | after each chain's move, m.143–144, m.249–427 | after all chains have moved, r.373–412 | text silent | untested; expected small | needs a code edit |
| D-8 | κ in the bound; first move | π̃_j = κ + (1 − 2κ)π̂_j in A and D, Algorithm 2 p.9 | κ in the proposal only; first proposal empty, m.159–160, m.412–415 | κ-shrunk π in both; first move real, r.63, r.378, r.392 | PARNI | untested; expected negligible (one move, and κ ≤ 0.001) | leave |
| D-9 | scaling of X | not stated | none in the sampler; run scripts centre only | unit-sd columns, h.13–14 | text silent | none in this study: the adapter scales X before either code sees it | settled by the preprocessing ruling |
| D-10 | run settings | Sec 4.1 pp.11–12: g = 9, h = 10/p, 5 and 25 chains; no run length, no τ. Sec 4.3 p.14: τ = 0.234, 500 + 2500 | demos: τ = 0.25, 100 + 200, 25 chains | script: τ = 0.2, 2000 + 4000, 25 chains, e.67–79 | neither is the Sec 4.1 run; the PARNI script is the only author file for that design | untested; a 100 + 200 run would be the largest change of all | owner's choice; the `.m` takes any of these as arguments |

**Bottom line, the three options asked.**

- **(i) Run PARNI ASI as is.** The authors' code, unedited, with an author script for the S1 design. It is not the paper's code: D-4 contradicts the text, and D-2, D-5, D-6, D-7 differ from the `.m`.
- **(ii) Patch PARNI toward the `.m`.** ctrl knobs reach only D-1, D-3, the exponent of D-2 and D-10. D-2 (factor 2, per-move timing, empty proposals), D-4, D-5, D-6, D-7 and D-8 need edits to `ASI.R`. The result is neither code as shipped.
- **(iii) Port the `.m` to R.** Our code; a reimplementation, with a cross-check against the original still needed.

**Recommendation.** Of the three, (i): it is the only one that runs author code unedited. The owner has since chosen a fourth route, the original `.m` under Octave, which is better than all three on fidelity because nothing is edited or rewritten; (i) is then the fallback if the Octave run cannot be made to work. Not known for either route: whether D-2, D-4 to D-7 change PIPs in S2, where the PARNI run mixes poorly (acceptance 0.12).


Written 2026-11-25 by Fable-B (HQ addendum 2, then the HQ corrected rulings of the same day, point d). Read-only comparison; neither code is edited. This table is the fidelity cross-check: no MATLAB or Octave run and no R port were made (HQ withdrew both).

**Verdict.** The PARNI R `ASI()` is **not** a line-by-line match of `ASI_sampler.m`. Both sample the same posterior with the same proposal family, the same Metropolis-Hastings step, the same Rao-Blackwellised quantity and the same PIP estimator (S-1 to S-9). They differ in ten places (D-1 to D-10), all in how the proposal is tuned or in how X is scaled. Seven of the ten cannot be set through the PARNI arguments. HQ ruled that the PARNI R code runs, with the settings of its own example script, and that these differences are documented here.

## Files compared

| Tag | File | Identity |
|---|---|---|
| m.NN | `ASI_sampler.m` v3.0, 587 lines, in `_local/engineering/ext/griffin_asi_original/Version3.0/` (from `https://jimegriffin.github.io/website/Version3.0.zip`, fetched 2026-11-25) | sha256 `4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb` |
| r.NN | `R/sampler/ASI.R`, PARNI repo commit `3b95d669e9bcf6df9e2ba46fb89fc536922e12e2` | md5 `96f5d8da98b5fbcf4b36dcc2e243500c` |
| s.NN | `R/sampler/other_supportive_functions.R`, same commit | md5 `e9dce2640d7e3ea7bad06e560f03dce9` |
| h.NN | `R/make_hyper_par.R`, same commit | md5 `b2a8a525ef31313a9b96ab1b07a52ccf` |
| e.NN | `R/simulation/simulation_example.R`, same commit | the repo's example for the S1-type design |
| paper | Griffin, Łatuszyński & Steel (2021), Biometrika 108(1):53–69, DOI 10.1093/biomet/asaa055 | pages as printed in the advance-article PDF, 1–17 |

**Website copy = supplement copy.** `cmp` on 2026-11-25: all 10 files of the website `Version3.0/` are byte-identical to the owner's supplement copy at `_local/papers/Benchmark_methods/Griffin2021_supplement/code/Version3.0/` (same file list; `ASI_sampler.m` has the sha256 above in both). The supplement's `Code_For_Paper.zip` and the website `Version3.0.zip` have the same sha256, `ce3e9c753c87b71f3fc6b3946a01c90d3fdd1343d9f1b3ee669b1e5319460f42`. The sha256 of every file is in `_local/engineering/ext/griffin_asi_original/PROVENANCE.txt`.

Settings compared: the `.m` as its two run scripts call it (`gprior = 0`, fixed `hparam`, `heat = 1`, `adap_type = 1`, no `data_fixed`, no `updateg`), and the R code as `fit_asi.R` calls it (`prior_type = 1`, fixed `h`, `n_temp = 1`, `full_adap = FALSE`).

## Same in both

| # | Item | Paper (Algorithm 2 and text) | `ASI_sampler.m` line | PARNI file:line |
|---|---|---|---|---|
| S-1 | Marginal likelihood for prior (1), V_γ = gI, flat intercept: −(p_γ/2) log g − ½ log\|X_γ'X_γ + I/g\| − (n/2) log A | exponent −n/2, Sec 2.4 pp.8–9 | m.67–83, m.198–215 (intercept column in the design, unpenalised, m.72–73) | s.295–341 on centred data (h.13–14) |
| S-2 | Model prior: fixed h, independent Bernoulli | (1), Sec 2.1 p.3 | m.219–221 | r.47, r.255 |
| S-3 | Start: γ_j ~ Bernoulli(h) independently in every chain | not stated | m.65 | r.123 |
| S-4 | Proposal: independent flips with A_j = ζ min(1, π_j/(1−π_j)), D_j = ζ min(1, (1−π_j)/π_j) | Algorithm 2, p.9 | m.165–176 | r.241–247, r.380–381, r.411–412, s.384 |
| S-5 | Metropolis-Hastings acceptance. The `.m` sums the proposal log-probability over all p coordinates (m.177–192); the R code sums over the flipped ones only (r.242–249, s.388). The unflipped terms cancel, so the ratio is the same. | Algorithm 2 | m.218–242 | r.253–261, r.274–282 |
| S-6 | Rao-Blackwellised term: P(γ_j = 1 given the other γ and y) = h·BF_j / (1 − h + h·BF_j) | (10), pp.8–9 | m.263–385 | r.377, s.98–208 |
| S-7 | π in burn-in: running mean of the S-6 terms over all chains and iterations; Rao-Blackwellisation stops at the end of burn-in | Sec 4.3 p.14 | m.259–262, m.403–404 | r.374–378 with Nl = Nb (r.27–29) |
| S-8 | ε = 0.1/p and the same logit_ε map | "We use ε = 0.1/p", p.9 | m.49–50, m.96, m.155–157 | e.72, s.363, s.370 |
| S-9 | PIP = plain mean of γ over all recorded draws of all chains, no thinning. Neither code returns a Rao-Blackwellised PIP. | Sec 4.3 p.14 | m.529, m.565 | r.310, r.427, r.460 |

All chains share one π and one ζ in both codes (m.159, m.251, indexed by temperature level, not by chain; r.378, r.387), as on paper p.7.

Two numeric checks on S-1 and S-6 (`.rc_tmp/fableB/probe/probe_bf_check.R`, log `.rc_tmp/fableB/logs/probe_bf_check.log`, n = 80, p = 30):

- The R code's `bf_ind_L` equals the ratio of marginal likelihoods with variable j in and out, which is how the `.m` builds it: largest gap in log BF 1.7e-13 over 20 models.
- The `.m` form of the marginal likelihood (m.81–83, written out in R for this check only) minus the R code's `log_llh_ind_L`, on the same X: constant over models to 8.5e-14.

## Different

"Reachable" says whether a `fit_asi.R` ctrl option can set the R code to the original's behaviour.

| # | Item | Paper (Algorithm 2 and text) | `ASI_sampler.m` line | PARNI file:line | Reachable |
|---|---|---|---|---|---|
| D-1 | κ | "We use κ = 0.001", p.9 | 0.0001, hard-coded: `probstar = 0.0001 + (1 - 0.0002) * probstar` (m.160) | argument `kappa` (r.20, r.378); example 0.001 (e.71) | yes, `ctrl$kappa` |
| D-2 | ζ step | (11): logit ζ + φ_i(a_i − τ), φ_i = O(i^−λ), 1/2 < λ ≤ 1 (pp.7, 9) | `logitzeta0 + 2 / it^0.55 * (change~=0) * (accept - tau)` (m.251). Applied after every chain's move, so 25 times per iteration with 25 chains. A proposal that changes nothing adds 0. | `logit_e(zeta) + iter^phi_prop * (acc_prob - target_prop)` (r.386–387). Applied once per iteration to the mean acceptance over chains (r.307, r.333). A proposal that changes nothing has acceptance 1 (r.260–261) and pushes ζ up. Example exponent −0.7 (e.73). | exponent only, `ctrl$phi_prop`. Not the factor 2, not the per-move timing, not the empty-proposal rule. |
| D-3 | ζ start | not stated for ASI | ν/(h·p), set to 0.1 if above 1 (m.92–95). With ν = 1 and h = 10/p this is 0.1. | `init_zeta` (r.17); example 0.5 (e.77) | yes, `ctrl$init_zeta` |
| D-4 | Lower bound on ζ | Δ = 2Σ min(π_j, 1−π_j); ζ = 1/Δ if ζΔ < 1 (p.9) | E = ζ·2Σ min(π_j, 1−π_j) (m.412–417). If E < 1: logit ζ ← logit ζ − log E (m.418–420). | Δ = 2Σ **max**(π_j, 1−π_j) (s.213–215). If ζΔ < 1: ζ ← 1/Δ (r.392–398). Δ is close to 2p, so this almost never binds. | no |
| D-5 | Range of ζ | (ε, 1−ε) | logit ζ clamped to [−3, 3] (m.422–427): ζ stays in about [0.047, 0.953] | no clamp on the logit. `logit_e` raises ζ below 2ε to 2ε (s.361); its upper guard tests ζ > 2(1−ε), which cannot happen (s.360). Resets r.400–405 apply only after the Δ step. ζ can sit at 1−ε. | no |
| D-6 | π after burn-in | Sec 4.3 p.14: "Rao–Blackwellised updates of π were only calculated during the burn-in" | with `adap_type = 1` (both run scripts) π keeps moving: the plain γ draws are added to the same running mean (m.259–261) | `full_adap = FALSE`: π is frozen at its burn-in value (r.374). `full_adap = TRUE` would keep Rao-Blackwellising, which is not what the `.m` does either. | no |
| D-7 | When π, ζ, A, D are updated | chains "share the same proposal parameters", p.7; Algorithm 2 is written for one chain | inside the chain loop, after each chain's move (m.143–144, m.249–427); the next chain already proposes with the new values | after all chains have moved (r.373–412) | no |
| D-8 | κ in the bound; first move | π̃_j = κ + (1 − 2κ)π̂_j in A and D (Algorithm 2) | κ only in the proposal (m.160); the bound uses the raw π (m.412–415). At the first move `count3 = 0`, so π = 0/0 and the proposal is empty (m.159, m.173–175). | the κ-shrunk π is used in both places (r.378, r.392). π starts at h (r.63), so the first move is a real proposal. | no |
| D-9 | Scaling of X | not stated | none inside the sampler; the run scripts centre X and y (`run_tecator.m` 8–12, `run_concrete.m` 19–23) | `make_hyper_par` scales X to unit sd and centres y (h.13–14). V_γ = 9I then applies to the coefficients of the scaled columns. | no |
| D-10 | Run settings shipped | Sec 4.1 pp.11–12: g = 9, h = 10/p, 5 and 25 chains, no run length, no τ. Sec 4.3 p.14: τ = 0.234, 500 + 2500. | `run_tecator.m` and `run_concrete.m`, lines 16–27 and 27–38: g = 100, h = 5/100, τ = 0.25, ν = 1, burn-in 100, 200 recorded, thin 1, 25 chains. No script for Sec 4.1. | e.67–79 (n = 500, p = 5000, SNR 2, g = 9, h = 10/p): N = 6000, Nb = 2000, 25 chains, τ = 0.2 | yes, `ctrl$N`, `ctrl$Nb`, `ctrl$n_chain`, `ctrl$target_prop` |

Which code is closer to the paper, item by item: D-1 the R code (κ = 0.001); D-4 the `.m` (min); D-5 the R code (no extra clamp); D-6 both fit the Sec 4.3 sentence; D-2, D-3, D-7 the paper leaves open; D-8 the R code; D-9 not stated.

## How large the differences are

Measured in the earlier round (`.rc_tmp/fableB/probe/probe_asi_orig.R`): the R code run with the original's κ = 0.0001, ζ start 0.1 and exponent −0.55 (D-1, D-3, part of D-2), against the R defaults.

| Data | max change in a PIP | seed-to-seed change, defaults |
|---|---|---|
| S1-like, n = 200, p = 500, SNR 3 | 0.001 | 0.003 |
| S2 high-5, n = 50, p = 1000, SNR 6 | 0.096 | 0.147 |

Selections were the same. Not measured: D-4 to D-9 and the rest of D-2, because the R code has no argument for them and the `.m` was not run (no MATLAB or Octave on Owls).

## The original code against its own documentation

- `RB_adap` and `RB` are arguments (m.1) but appear nowhere in the body. `prob_inclusion` is always the plain mean (m.565); `prob_inclusion2` is never filled and returns zeros (m.110, m.566). `instructions.pdf` says `prob_inclusion` is the Rao-Blackwellised estimate when RB = 1.
- `instructions.pdf` gives `adap_type = 2` for adaptation in burn-in only. The code tests `adap_type == 1` or `adap_type == 0 && it < burnin` (m.249); with 2, nothing adapts and π stays 0/0.
- Both run scripts call `ASI_sampler` with 16 arguments; the function takes 18 (`data_fixed` first, `updateg` last); `instructions.pdf` prints a 15-argument signature (p.4) and describes 16 inputs in its list (the 15 and `RB_adap`, pp.4-5). The shipped scripts cannot run the shipped sampler as written.
- The run scripts' 100 + 200 iterations match no run reported in the paper (Sec 4.3 reports 500 + 2500 for ASI).

## Run length and τ for S1 (ruling 3)

| Source | Burn-in | Recorded | Thin | Chains | τ | Design |
|---|---|---|---|---|---|---|
| `run_tecator.m` | 100 | 200 | 1 | 25 | 0.25 | Tecator, p = 100, g = 100, h = 5/100 |
| `run_concrete.m` | 100 | 200 | 1 | 25 | 0.25 | concrete data with interactions, g = 100, h = 5/100 |
| Paper Sec 4.3 p.14 | 500 | 2500 | none | not stated there | 0.234 | real data sets |
| PARNI `simulation_example.R` e.67–79 | 2000 | 4000 | none | 25 | 0.2 | the Sec 4.1 design type (g = 9, h = 10/p) |
| Paper Sec 4.1, supplement | not stated | not stated | — | 5 and 25 | not stated | S1 |

**Used (HQ corrected ruling 2026-11-25):** the PARNI `simulation_example.R` row exactly: 2000 burn-in + 4000 recorded, 25 chains, τ = 0.2, with X scaled and y centred as in that script (e.12–13). In `settings` these carry the source "authors' repo R/simulation/simulation_example.R @3b95d66; not stated in the Biometrika text", with tag "author" in suite S1 and "OURS" in suite S2, where the S1 settings are used unchanged. The earlier ruling τ = 0.234 (paper Sec 4.3) is withdrawn. `test_bayesian.R` checks the values the Octave adapter passes (`burnin`, `numbofits`, `numbofreps`, `tau`) and that their `settings` sources cite the repo script; it does not read the PARNI script or compare its `alg_par` fields.

The `fit_asi_parni.R` options that move the R code towards the original (`ctrl$kappa`, `ctrl$init_zeta`, `ctrl$phi_prop`) are off by default. Since the owner's decision the row that runs is the same one, but in the original code: `burnin = 2000`, `numbofits = 4000`, `thin = 1`, `numbofreps = 25`, `tau = 0.2` passed to `ASI_sampler.m`.

## The `.m` under Octave against PARNI (measured 2026-11-25, after the decision)

Harness data S1_03 (n = 500, p = 500, SNR 2), rep 1; both codes at 2000 + 4000 iterations, 25 chains, τ = 0.2, X scaled and y centred; two method seeds each.

| | Original `.m` under Octave | PARNI R `ASI()` |
|---|---|---|
| Selection (two seeds each) | {1,…,10} = the true support, both seeds | the same, both seeds |
| Σ PIP | 10.368, 10.367 | 10.368, 10.367 |
| Largest null PIP | 0.024 (variable 90) | 0.024, 0.025 |
| max abs(ΔPIP), seed to seed, same code | 0.00085 | 0.00121 |
| max abs(ΔPIP), `.m` against PARNI (the four seed pairs) | 0.00064, 0.00072, 0.00151, 0.00185 | |
| Acceptance rate; final ζ | 0.48; 0.952 (clamp) | 0.65; 0.9998 |
| R-hat of the log posterior | 1.000 | 1.000 |
| Wall time, one core | 971 s and 1182 s | 77 s and 77 s |

All four runs (two seeds of each code) selected the same 10 variables, the true support, and their PIPs agree closely: the largest PIP difference between a run of the original and a run of PARNI is 0.00064, 0.00072, 0.00151 and 0.00185 over the four pairs; between the two seeds of the same code it is 0.00085 (Octave) and 0.00121 (PARNI). Two seeds per code do not give a Monte Carlo standard error, so this does not show that the two codes agree to within Monte Carlo error; two of the four cross-code differences are larger than both within-code differences. The original under Octave is 13 to 15 times slower. One data set at one S1 setting; it says nothing about S2, where both codes mix poorly (PARNI adapter on the S2 SNR-6 case: 3 TP 3 FP, R-hat 1.03; the original: next paragraph and the table above).

S2-type data (test case n = 50, p = 1000, 5 signals, SNR 6), original code, two seeds: selections {1,2,4,54,672,755,821} and {1,2,4,54,672,755,821,825}, max abs(ΔPIP) 0.236, R-hat 1.04 and 1.03, acceptance 0.13, final ζ 0.09. PARNI on the same data (earlier round, τ = 0.234): {1,2,4,54,755,821} and {1,2,4,54,755,821,825}, max abs(ΔPIP) 0.147, acceptance 0.17. Both codes are seed-dependent there and agree on the main null variables selected; a code-to-code difference cannot be separated from the seed-to-seed difference with two seeds each.

Cost: the original under Octave takes about 1.7 to 2.1 s × p per fit at the ruled run length (15 min at p = 500, 29 min at p = 1000, 2.85 h measured at n = 1000, p = 5000); PARNI took 77 s to 350 s. At n = 1000, p = 5000, SNR 2 both give the exact support (Σ PIP 10.30 for the original, 10.29 for PARNI). See README, "Test results".
