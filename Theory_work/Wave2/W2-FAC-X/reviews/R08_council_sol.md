# R08 — Independent council seat: Theorem FAC-CS-iid

**Overall score: 8.8 / 10. Council verdict: NOT PASS, pending the report-only correction in issue 1.**

I found no counterexample or blocking gap in the proof of locked STATEMENT v3, (C1)–(C4). The failed gate below concerns an incorrect generalisation in REPORT §6, which the brief explicitly includes in the deliverable. It does **not** refute FAC-CS-iid or require a new hypothesis for that theorem. The score and the gate decision are independent: this is a strong theorem proof with a small, but substantive, error in its account of the assumptions needed to generalise it.

Scope: STATEMENT.md v3; lemmas X1–X6; REPORT §§1–4 and §6. Target 2, X7 and T2 were not reviewed or certified. Asymptotic scope is respected; neither asymptotics nor the size of the onset is a finding.

## Gate verdicts

| Gate | Verdict | Reasons |
|---|---|---|
| **G1 — Correctness of every step** | **FAIL** | The mathematical argument for (C1)–(C4) survives the checks below. However, REPORT.md:106 incorrectly says that a floor on logarithmic-size sets suffices for truth moves. X4.6 conditions on potentially p-sized models and uses their residual-variance floor. A concrete obstruction to the report's weaker assertion is given in required issue 1. |
| **G2 — Hypotheses used = hypotheses stated** | **PASS** | For FAC-CS-iid itself, Gaussian CS rows, independent Gaussian noise, fixed nonzero raw coefficients, fixed positive rho, fixed s0 >= 1, (FS), and the strict dimension exponent supply the stated inputs. K=p eventually. (FS) is used for the start, rather than silently imported into the path proof; masked-truth (FS-prime) is not claimed. Method and delivery premises are inherited explicitly. |
| **G3 — No hidden assumptions** | **PASS** | X5–X6 condition on the raw design Z, which determines the column scales and random coefficients. X4's event works simultaneously for every omitted set of at most 15 nulls; no independence of the selected N0 and the noise coordinates is assumed. The prefix induction, probability-one nondegeneracy, empty-set cases, and one-sided end configurations are accounted for. The stronger eigenvalue condition used by X4 is actually available under the stated CS-iid hypotheses; issue 1 concerns only the report's proposed generalisation. |
| **G4 — Adequate cited status** | **PASS** | CITECHECK.txt was inspected, its five path/line checks were independently rerun successfully, and the substantive source statements and qualifications were checked. FAC-B and FAC-A are recorded as "PROVED-CHECKED" at package level; their individual lemma headers retain their own author/check qualifications. T03-sharp, T38-(0), [OP], CAP and Proposition F are used with the qualifications listed below. The unchecked X7 is not an input to the reviewed theorem. |
| **G5 — Constants and rates tracked** | **PASS** | The perturbation budget closes with the single deterministic scale, including its n^(-1/3) floor. The second-order bound, band absorption, D7/D8, initial-phase density condition, bulk gain separation and end-phase errors all tend in the required directions for A1<1/2. D3 supplies kappa=kappa_infinity+o(1), preserving c_D>0. The candidate-ordering error is absorbed by the floor. The exceptional sets of size 16/17 used by swap comparisons remain within X2. |
| **G6 — Fidelity to the specified/coded method** | **PASS** | The D0 score, capped BB(1,p) prior, full-response block tables and actual partition match FAC-B §1 and SoP. Production local_search scans all feasible flips/swaps, uses strict improvement and lexicographic neighbour ties, and performs the additional scan at the cap. LS0 uses ell_n+|start mode|. The inspected production search, LS0 integration and preflight files have no diff against merged main 4676af6. The theorem retains EX-A and the other implementation premises; it does not certify floating-point execution. Delivery retains the total fallback and amended allocation, including the current-head preflight terms. |

## Numbered issues

1. **MINOR, substantive report error — REQUIRED for a pass.**

   **Location:** `REPORT.md:106`, last column of the sparse-eigenvalue row; compare `lemmas/X4_path.md:265–276`.

   **Problem:** The sentence “W2-UNI's (A1) floor on log-size sets would suffice for (H0) and truth moves” is incorrect for the truth-move argument being summarised. At T containing S0, X4.6 needs a lower bound on the norm of the truth residual after projecting onto T minus that truth, or onto a swap model. These conditioning sets can have order p elements. A floor on all logarithmic-size submatrices gives no such lower bound.

   **Obstruction:** Let m grow faster than log n, with m=o(sqrt(n)), and choose centred orthonormal vectors u1,...,um in R^n. Define standardised null columns xl=sqrt(n-1) ul and the sole truth column

       x0 = (x1 + ... + xm)/sqrt(m).

   For a subset containing x0 and q nulls, its correlation matrix has minimum eigenvalue `1-sqrt(q/m)` (with the singleton convention); subsets of nulls have eigenvalue 1. Thus every submatrix of size O(log n) has minimum eigenvalue tending to 1, but x0 has **zero** residual after projecting onto all m nulls. The exact lower bound used at X4.6:268 cannot follow from the proposed weaker floor.

   This can even reverse the desired truth-move sign for the shipped score. With independent Gaussian noise, coefficient b on x0, and T containing all m+1 columns, the prior ratio for deleting x0 is 1. The full Gram has nonzero eigenvalues `2(n-1), n-1,...,n-1`; removing x0 leaves m eigenvalues n-1. Writing G_del for this truth deletion, the determinant and data terms give

       n G_del -> (1 - b^2/sigma^2)/4    in probability.

   Here the fitted energy along the unit direction x0/sqrt(n-1), divided by n after response standardisation, tends to `b^2/(b^2+sigma^2)`, and psi_T/n tends to `sigma^2/(b^2+sigma^2)`. Consequently the determinant contribution is `1/(4n)+o(1/n)` and the data loss is `b^2/(4 sigma^2 n)+o_P(1/n)`. For `0<|b|<sigma`, this deletion improves F with probability tending to one despite the logarithmic-size floors and fixed nonzero signal.

   This design is **not CS** and is not a counterexample to the locked theorem. It refutes precisely the report's claim about sufficiency of the weaker eigenvalue ingredient.

   **Fix:** State that logarithmic-size floors suffice for the posterior (H0) inputs, whereas the present truth-move proof needs a residual-variance floor after conditioning on the large models it visits, including the one-move enlargements used for swaps. A full-design eigenvalue floor is the sufficient condition actually supplied by this theorem. Do not claim that X4.6 already works under a logarithmic-size floor alone. No edit to STATEMENT or X1–X6 is needed for this finding.

2. **MINOR — NOT REQUIRED for a pass: correct the provenance of the Gaussian coordinates.**

   **Location:** `REPORT.md:109`.

   **Problem:** The row attributes “xi iid N(0,1), sign symmetry ... E5” to Gaussian noise. Those coordinates are Gaussian because the idiosyncratic design vectors are isotropic Gaussian: conditional on any independent nonzero noise direction e1, their projections onto e1 are iid standard normal. Gaussian noise is used elsewhere, notably for the chi-square noise norm in X1.1, conditional Gaussian noise bounds in X5, and the fixed-design posterior input in X6. This is an inaccurate dependency label, not an unproved theorem extension to other noise laws.

   **Fix:** Move the xi/sign-symmetry attribution to the Gaussian-row ingredient and identify the actual Gaussian-noise uses in that row.

3. **EDITORIAL — NOT REQUIRED for a pass: preserve the Target-2 qualification within §6 itself.**

   **Location:** `REPORT.md:104,110–111`.

   **Problem:** “Population-level restatement: the proof needs ... max|lambda_j-lambda_bar|=O(n^(-c)) (X7)” can be read as a restatement of the checked result, although §5 labels X7 draft/unchecked and the council brief excludes it. STATEMENT remains correctly restricted to CS, so this is not a hidden dependency of (C1)–(C4).

   **Fix:** Label the near-CS parenthetical and concluding sentence explicitly as the unchecked Target-2 extension, outside this council verdict; state the checked population class first.

## Independent proof and source checks

- **X1:** Re-derived the rotation independence, Sherman–Morrison RSS identity, Schur deletion statistic, determinant identities, ridge/OLS correction and reference swap algebra. Independence of xi and W is exact; replacing ridge gains by RSS gains without controlling their errors would not be legitimate, but X1 controls those errors explicitly.
- **X2–X3:** D5 ranges over intervals determined by xi while W is independent of xi, so its conditional union bound is legitimate. The adaptively selected exterior bands are controlled crudely, not treated as independent Gaussian sums. The soft-gap crossing estimate bounds the minimum distance, not necessarily the opposite-side distance. Its initial-phase argument uses only the established prefix and has sufficient slack for the 4.3 band.
- **X4:** Checked the order structure -> perturbation -> candidate rule -> move comparison -> next prefix. B1 uses the previous centre bound, B2 then uses the established geometry, and B3 uses full-sample sign balance plus D7. Bulk swaps use a separate addition bound at T minus j, not a false no-addition claim over the entire structured family. At end-phase entry, D7 places finite band endpoints in the top separated tails; D8 eliminates band defects. Candidate deletions are tested hypothetically before being identified with the production move. Majority-side dynamics, one-sided sign separation and the c_D margins then survive o(1) score errors. X4.6 uses the available full-design floor uniformly over large sets.
- **X5–X6:** The nonzero population increments are uniformly separated by (FS). Exact zero pairs are confined to the one block containing all truths and handled by a two-sided conditional event. The raw-design event supplies common posterior constants and a common beta-min envelope. The every-sequence contradiction justifies the uniform conditional expectation limit; this is stronger than simply integrating a pointwise conditional asymptotic statement. D_n is bounded in the correct direction. Delivery uses the direct LS0-discovery event and the scored-set inclusion, not a reverse inference from D_n -> 0.
- **Source qualifications:** T38-(0) is quoted as `"PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"`; T03-sharp as `"PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"`; [OP] as `"PROVED (by this seat, unchecked)"` within the checked GEN package; CAP as `"PROVED (by this seat)"` with its recorded council checks. F-GROW's `"PROVED (A2), checked by A3"` and Proposition F's A1/A4 allocation/audit qualifications are preserved. Lemma CR's source status is `"PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)"`. The reused audit qualifications are not upgraded into implementation proofs.

## Independent computational falsification

Python 3.13 was run through stdin in `reviews/R08_scratch/`, without importing the ticket's numerical scorer or writing numerical artifacts. These checks support the algebra; they do not establish the asymptotic theorem.

1. **Raw-row identity checks:** 12 independently generated centred Gaussian designs, p=5, n=60,...,170, rho in {0.01,0.3,0.7,0.99}; every model containing the two truths. Across **96 model sets, 144 null-deletion edges and 144 null swaps**, compared the representation RSS with direct projection, q differences with squared Schur statistics, determinant and ridge-partial differences, exact deletion/swap gains and the reference swap identity. Maximum absolute discrepancy: **2.23e-12**; no failed identity.
2. **Adversarial X3 checks:** 20 seeds, eight configurations per seed, 256 coordinates with a deliberately tight cluster around the initial centre, kappa-prime in {1.01,1.1,2,5}. Verified the stated initial-density hypothesis, then repeatedly chose the farthest eligible deletion under R_varpi. Across **160 prefixes and 40,640 steps**, including **seven actual crossings**, no violation of the crossing bounds, non-crossing endpoint monotonicity or the 4.3-varpi containment was found. Each final two-point state was checked too.
3. **Issue-1 score calculation:** Stable closed-form evaluation of the redundant-column design with b=0.2, sigma=1 and a noise vector orthogonal to its span gives n times the truth-deletion gain **0.239982290955, 0.239999822908, 0.239999998229** at n=10^4,10^6,10^8, respectively, agreeing with the analytic limit 0.24. This checks the report-only obstruction, not the CS-iid theorem.
4. **Citations/code:** `citecheck.py` rerun with UTF-8 stdout: **5 OK, 0 MISS**. The status strings were additionally checked against the cited sources rather than inferred from the script. Read production `v3_engine.h:370–418`, the LS0 integration in `v3_core.cpp`, and `v3_fit.R` preflight; `git diff 4676af6 --` those three files is empty.

**Required fixes: issue 1 only.** After correcting REPORT §6's truth-move eigenvalue assertion, I have no remaining blocking objection to Theorem FAC-CS-iid on the evidence reviewed here. This review does not independently confer PROVED-CHECKED status on Target 2 or supply the other council seat's verdict.
