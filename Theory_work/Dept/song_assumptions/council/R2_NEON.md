# COUNCIL REVIEW — Round 2 — Seat: NEON (TH-SONG-ASSUMPTIONS)

**Package reviewed:** v1.2 (commit `7c7ca30f`, branch `dept/theory`): `THEOREM_DEFINITIONS.md`, `ASSUMPTIONS_AND_PROOF_PATHS.md`, `SIMULATION_DATA_ANALYSIS.md`, `OWNER_DEFENSIBILITY_DOSSIER.md`, plus `COUNCIL_RECORD.md`, `scripts/e9_width_mc.py`, and `tables/e9_width_s1.tsv`.
**Overall score:** **9.0 / 10** — all five Round 1 blockers (**B-1 … B-5**) are resolved, every assumption clears the ≥ 8.5 bar on both D and R, and no new blockers were introduced. Four minor substantive consistency/precision edits remain (quick, non-blocking polish).

---

## 1. Assumption score table

| Assumption | D | R | One-line reason |
|---|---:|---:|---|
| **A-GL** | 9.5 | 9.5 | Verified precedents (fixed vs random design cleanly distinguished), exact coded determinant and Fubini contrast density restored, and `TM-a0` excluded from scope. |
| **A-SPARSE** | 9.5 | 9.5 | SL Thm 4 mis-citation fixed, bare `SC11` dropped, growing-$s_0$ remark properly hedged alongside `rem:sharp`(a); cleanly controls deletions and localisation. |
| **A-DIM** | 9.5 | 9.5 | Verified precedents and finite-$n$ E6 ratios properly qualified; three-layer hierarchy (`q_n(M)` isometry → `prop:dist(i)` → testing) and exact `C_q` restored. |
| **A-DIM′** *(conj.)* | 9.5 | 9.0 | Scored as an evaluated weaker alternative: `(s+1)` fix applied, high-risk status and testing-step failure ($\log p = n^{1/3}$) plus `A-DIM″` cap diagnosis are exact and honest. |
| **A-SUBG** | 9.5 | 9.5 | False bounded-predictor dominance replaced by exact counterexample; SL Cond. 1 marked absolute-scale; two-sided isometry on $(s_0+J)$-sets and Hellinger conversion cleanly separated from SL Cond. 3. |
| **A-NEC** | 8.5 | 9.0 | Rewritten as object/scale/window comparison, SL (26) corrected, and `prop:dist(i)`/TD tests added to "Used in"; minor D slip on l.109/l.113 ("smaller than each" clashes with NH14's $p_n^{-\kappa}$ caveat three lines above). |
| **A-BS** | 9.5 | 9.0 | Full YWJ (7a) quote restored with growing-vs-fixed caveat for YWJ/SC11; S1/S2 verified; properly kept for TS-b/TM-b since `prop:dist(i)` depends on it. |
| **A-BS′** *(not adopted)* | 9.0 | 9.5 | Scored as an evaluated weaker alternative: accurately recorded as unusable until `prop:dist(i)` is extended, and Astra's $O(n)$ energy pair is distinguished from Fable's $s\bar b_n^2 = o(n)$. |
| **A-MARGIN-H** | 9.5 | 9.5 | Quantifier tightened to effective sieve $|S| \le \min(K, J)$ (inside `A-SUBG` window), fresh $c'_H < c_H$ used in TS-a, and E2 labelled a restricted-search scale diagnostic ($\tau=\sigma$ upper bound). |
| **A-MARGIN-U** | 8.5 | 8.5 | B-1, B-2, B-5 all resolved ($B_{Dm} > 0$ quantifier, $C$ named, worst-case forms labelled, E9 MC checks AR(1) width, `MARGIN*` demoted, S2/price/$E K_1$ fixed); minor D/R deductions for E9 scope wording and §3.3 step 3 log-odds display. |
| **A-MIS(iii)** | 9.0 | 9.0 | Nonsingular $\Sigma_{CC}$ added, omission-only scope explicit, discrete-$y$ moved to `A-MOM`, Rossell/GvO/E7 caveats accurate; one stale `"the special case"` label for `thm:omitted` remains on `ASSUMPTIONS` l.325. |
| **A-MOM** | 9.5 | 9.5 | One fixed law, $p_C \ge 2$, coded centring, raw-unit map, fixed $\mathrm{BB}(1, p_C)$, a.s. empty exceptional event, and split SL Cond. 4 / SLLN–LIL defence are complete and sufficient. |

---

## 2. Overall score and 1-to-1 Song & Liang (2015) map verdict

- **Overall package score:** **9.0 / 10.** Revision v1.2 is unusually disciplined: every R1 blocker and substantive critique across all three seats was addressed cleanly, the new E9 conditional-width Monte Carlo directly answers the S1 SNR-2 mixed-rival question with transparent code and verified numbers, and the package remains scrupulously honest about open risks (`TD′`, `MARGIN*`, TS-b proof obligations, hidden-column evidence).
- **1-to-1 SL map (`THEOREM_DEFINITIONS.md` §§2–3):** **Complete and correct.** All R1 qualification fixes (`SL-3`/`SL-4` partial analogues, `SL-5` threshold/FDR separation, `SL-6/7` previously delivered analogues + non-dominance vs vanishing two-sided sample condition (26), `SL-8` Thm 4 premises without global (4), `SL-9` exact selection vs inclusion) are accurately reflected. Declining a separate row for SLs Lemma 1.2 is reasonable since it is already catalogued inside `SL-8`.

---

## 3. Blocker resolution (R1 B-1 … B-5) and remaining SUBSTANTIVE items

### Round 1 blocker status

| Blocker | Status | Reason |
|---|---|---|
| **B-1** (`A-MARGIN-U` on $B_{Dm} \le 0$; $C$ unnamed) | **Resolved** | Quantifier restricted to nonempty $(D, m)$ with $D \neq \emptyset$, $m \le J$, and $B_{Dm} > 0$ across all four files; $C$ named as the superset-step truncation constant; $B_{Dm} \le 0$ classes dispatched by the containing-model credit (`ASSUMPTIONS` §3.3 step 3). (Minor display slip in step 3 tracked as S2 below.) |
| **B-2** (worst-case forms fail on S1 SNR 2; $m=0$ only) | **Resolved** | Combinatorial width and squared forms explicitly labelled worst-case (factor-proxy) forms that do not cover S1 at SNR 2 (with Opus's arithmetic quoted); design-event quantifier stated for $w_{Dm}(X)$; new E9 MC verifies $w_{Dm}(X) \in [0.10, 0.59]$ and surplus $\ge 3.29$ at SNR 2 on simulated S1 designs. (Minor scope-wording refinement tracked as S3 below.) |
| **B-3** (`A-NEC` dominance claims; SL (26) "fixed-type") | **Resolved** | Rewritten across `ASSUMPTIONS`, `DOSSIER`, and `THEOREM_DEFINITIONS` §3 as an object/scale/window comparison (not dominance); SBJ A4 and NH14 4.5 accurately described as minimum nonzero sample eigenvalues allowing duplicates; SL (26) corrected to a vanishing two-sided sample tail condition. (Minor internal slip tracked as S1 below.) |
| **B-4** (raw-unit map, input domain, `TM-a0` $p_C \ge 2$, prior) | **Resolved** | Raw-unit map $\beta_j = s_y b_j/s_{x_j}$, $\sigma^2 = s_y^2 v$, removed-column / undefined-posterior exceptional event (`or6` l.116), `TM-a0` $p_C \ge 2$, fixed coded $\mathrm{BB}(1, p_C)$ eventually untruncated ($K = p_C$ for $n \ge 2p_C$), coded centring, and a.s. empty exceptional event are all cleanly specified. |
| **B-5** (`TS-b*` lacks testable statement) | **Resolved** | Demoted cleanly to `MARGIN* (open refinement; not a defined target)` across all four files, with the missing mathematical components explicitly enumerated (`THEOREM_DEFINITIONS` l.159, `ASSUMPTIONS` §6 item 2). |

### New / remaining SUBSTANTIVE items (0 blockers; 4 minor precision/consistency fixes)

1. **[SUBSTANTIVE] `A-NEC`: internal contradiction in the precedent floor-value sentence.**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (l.109 vs l.106); `OWNER_DEFENSIBILITY_DOSSIER.md` `A-NEC` Q3 (l.113 vs l.110).
   - *Flaw:* Line 106 (and Dossier l.110) correctly notes that NH14's floor $\gtrsim p_n^{-\kappa}$ can be smaller than $c_\psi/n$ at large $p$, but three lines later l.109 (Dossier l.113) states `"As a floor value on full-rank sets, c_ψ/n is smaller than each [of these]"`, directly contradicting the NH14 exception.
   - *Fix:* Amend both summary lines to `"As a floor value on full-rank sets, c_ψ/n is smaller than each of these except NH14 at large p when p_n^{−κ} < c_ψ/n; as a condition set it is not uniformly weaker."`

2. **[SUBSTANTIVE] `A-MARGIN-U`: §3.3 step 3 log-odds display omits `− γ log n` and `(1+δ)^{-1}`.**
   - *Location:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §3.3 step 3 (l.273).
   - *Flaw:* Line 273 writes `"The log odds of class (D, m) against T are at most B_Dm − ½(√λ̂_S − w_Dm − t_n)₊² (in the notation of A-MARGIN-U)"`. Because $B_{Dm} = \mathrm{Pr}_n(d) - \frac{m}{2}\log(n/(C\log p)) + \gamma\log n$ already includes $+\gamma\log n$, that bound would only yield $O_P(1)$ when $B_{Dm} \le 0$ or when $\frac12(\cdot)_+^2 \ge B_{Dm}$ (and omits the $(1+\delta)^{-1}$ linearisation/$\hat\sigma^2$ factor used in `A-MARGIN-U`).
   - *Fix:* Write `"The log odds of class (D, m) against T are at most (B_Dm − γ log n) − [1/(2(1+δ))](√λ̂_S − w_Dm − t_n)₊² + O_P(1)"`, so that both $B_{Dm} \le 0$ and `A-MARGIN-U` visibly yield $O_P(n^{-\gamma})$.

3. **[SUBSTANTIVE] `A-MARGIN-U`: E9 summary lines overstate $m = 2$ coverage across S1 and omit active $m = 4$ at $p = 5000$.**
   - *Locations:* `THEOREM_DEFINITIONS.md` l.145; `ASSUMPTIONS_AND_PROOF_PATHS.md` ll.174–175, 374; `SIMULATION_DATA_ANALYSIS.md` l.296; `OWNER_DEFENSIBILITY_DOSSIER.md` ll.176, 246.
   - *Flaw:* `scripts/e9_width_mc.py` (l.56) and `SIMULATION_DATA_ANALYSIS.md` l.278 correctly restrict $m = 2$ to the two $p = 500$ cells (`ms = [1, 2] if p == 500 else [1]`), yet the summary sentences in all four files report `"d = 1, m ≤ 2"` on S1 and list only `"d ≥ 2 and m = 3"` as unevaluated. Moreover, at both $p = 5000$ cells ($C=1, \gamma=0$), $B_{D4} > 0$ as well ($1.87$ at $n=500$, $0.83$ at $n=1000$).
   - *Fix:* State `"d = 1, m = 1 (all four S1 cells) and m = 2 (p = 500 cells); not evaluated: d ≥ 2 mixed classes, m = 2 at p = 5000, and active m ∈ {3, 4} at d = 1"`.

4. **[SUBSTANTIVE] `A-MIS(iii)` / `TM-b`: stale `"the special case"` phrasing for `thm:omitted`.**
   - *Location:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §3.5 (l.325).
   - *Flaw:* Line 325 still reads `"The delivered thm:omitted is the special case with Gaussian rows, a fixed floor and diverging per-coefficient signal"`, clashing with `THEOREM_DEFINITIONS.md` ll.192, 197 (`"Previously delivered analogue"`, expectation bound vs in-probability rate) and `ASSUMPTIONS` l.111 (smaller floor window does not imply `A-NEC` on the TD window).
   - *Fix:* Replace `"the special case"` with `"a previously delivered analogue (giving an expectation bound, with a fixed floor on its own window)"`.

---

## 4. NITPICKS (did not lower scores)

1. `SIMULATION_DATA_ANALYSIS.md` §E9 table: two minor rounding slips vs `tables/e9_width_s1.tsv` — l.286 `min surplus` prints `3.30` (table `3.2946` → `3.29`, matching the prose `"≥ 3.29"`) and l.289 `w_Dm(X)` prints `0.11–0.32` (table `0.1046` → `0.10`, matching the prose `"0.10–0.47"`).
2. `THEOREM_DEFINITIONS.md` §4.1 (l.124): `TD′` bullet still prints `q_n ≍ s·M·log₂(p√n)` instead of `(s+1)·M·log₂(p√n)` (fixed on l.122 and `ASSUMPTIONS` ll.81, 226).
3. `ASSUMPTIONS_AND_PROOF_PATHS.md` §5 table (l.363): the `"form invariant?"` cell for `data-free slab V = τ²I` still reads `"**no** for TM"`, whereas the adjacent cells and `THEOREM_DEFINITIONS` l.233 correctly explain it breaks the coded-score route for `TD, TS-b, TM-a/b` without affecting `A-MIS(iii)`.
4. `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (l.49): `(2b₀ + Q_S)^{−(n/2+a₀)}` with `"b₀ data-scaled by s_y²"` briefly blends coded units (`2b₀ + Q_S`) and raw units (`2b₀s_y² + Q_S`, ll.222, 315).
5. `OWNER_DEFENSIBILITY_DOSSIER.md` scorecard (ll.20–30): `A-MOM` has a full Q&A section (ll.215–220) but no row in the summary scorecard table.

---

## 5. Independent spot-checks (Round 2)

### Citations checked directly against `.rc_tmp/song/papers/` and `.rc_tmp/song/ms/` (8 checked)

1. **Jiang (2007) (`Jiang07.txt`, PDF pp. 2–3, 5–6):** Hellinger distance on joint densities (pp. 2–3), bounded covariates `|x_j| ≤ 1` (p. 5), i.i.d. random-pair data `D_n = (x^{(i)}, y^{(i)})` (p. 6) — **PASS**.
2. **Song & Liang (2015) main (`32.txt`, p. 957 / PDF p. 11):** Condition 4, Theorem 4 (fixed subset $s$, no global strict sparsity (4)), Corollary 2 unnumbered inclusion display — **PASS**.
3. **Song & Liang supplement (`32b.txt`, pp. 15–16):** Condition (26) vanishing two-sided sample eigenvalue tail on $|\zeta| = \bar r_n + |t|$, union bound under $\bar r_n \log P_n \prec n$ — **PASS**.
4. **Rossell (2022) (`Rossell22.txt`, arXiv v7 pp. 16–17):** Proposition 6 fixed-design mean misspecification $f^*(y) = N(y; W\beta^*, \xi^* I)$ with omitted columns — **PASS**.
5. **Grünwald & van Ommen (`GvO17.txt`, arXiv v3 pp. 4, 46–47):** Heteroscedastic `"in-liers"` setting (p. 4), discussion that De Blasi & Walker (2013) Thm 1 fails when the model class grows / is misspecified (pp. 46–47) — **PASS**.
6. **Yang, Wainwright & Jordan (2016) (`YWJ.txt`, p. 7):** Verbatim quote `"some form of upper bound on the norm ‖β*‖₂ in terms of the g-hyperparameter is required"` — **PASS**.
7. **Narisetty & He (2014) (`NH14.txt`, p. 17) & Shin, Bhattacharya & Johnson (2018) (`SBJ.txt`, p. 14):** Minimum *nonzero* sample eigenvalues (`p_n^{−κ}` in NH14; `ν_{k*}` in SBJ A4) — **PASS** (surfaced S1 contradiction on l.109/l.113).
8. **Staged manuscript (`or5_assumptions.tex` ll.185–206, `or6_theorems.tex` ll.116–120, `supplement.tex` ll.161–173, `supplement_or.tex` ll.126–160):** Verified `q_n(M)`, `C_q = 2(s(A+2)+4)/log 2`, undefined-posterior exceptional event (`or6` l.116), `prop:dist(i)–(ii)`, and `asm:omitted` starting at l.126 — **PASS**.

### Numbers and code checked directly against `tables/` and `scripts/` (7 checked)

1. **`scripts/e9_width_mc.py` & `tables/e9_width_s1.tsv` (120 rows) vs `harness/generate.R`:** S1 DGP (`COEF`, `RHO=0.6`, $\sigma^2=1$) and orthogonal-projection formulas for $w_{Dm}(X)$ ($m=1, 2$) verified; overall $w_{\text{mc}} \in [0.1046, 0.4703]$ ($m=1$), $[0.2156, 0.5937]$ ($m=2$, $p=500$ only), max SD $0.1208$; min surplus $3.2946$ (SNR 2), $6.6961$ (SNR 3). **PASS** on arithmetic (surfaced S3 scope note & N1 rounding slips).
2. **Direct recomputation of $B_{Dm} > 0$ at $C=1, \gamma=0$ across S1:** Active $m$ at $d=1$ is $\{1,2,3\}$ for $p=500$ and $\{1,2,3,4\}$ for $p=5000$ ($B_{D4} = 1.870$ at $n=500$, $0.829$ at $n=1000$) — surfaced S3.
3. **`e1_margin_by_setting.tsv`:** P1 `price` range `7.6004–10.3610` (matches `7.6–10.4` / `7.60–10.36`); `e2_over_eps2 >= 1` in `9/136` — **PASS**.
4. **Direct recomputation of $\mathrm{Pr}_n(3)$ vs $3\cdot\mathrm{price}$ at S1 `(500, 500)`:** $\mathrm{Pr}_n(3) = 23.4418$ vs $3\cdot\mathrm{price}(s_0-1) = 23.1103$ (`+1.43%`, P1 one-off `23.1072`, `+1.45%`); $\kappa_n(3) = 2.6195$ vs $\kappa_{\text{data}}(3) = 2.6575$ — **PASS**.
5. **Direct recomputation of $E K_1$ and rate term at S1 $(n, p)$:** Displayed formula `0.0306–0.0503` (`0.031–0.050`), $(p-s_0)2\Phi(-\sqrt{L})$ `0.0293–0.0470` (`0.029–0.047`), TS-b rate term $(s_0+1)\sqrt{\log p/n}$ `0.867–1.436` (`0.87–1.44`) — **PASS**.
6. **`e7_E6_sigma2C.tsv` & `e7_bt2diag_crosscheck.tsv`:** $E[\sigma^2\mid\text{MPM}]/\sigma_C^2$ medians `0.987–0.990` (S1), `0.837–0.979` (S2); `bt1, ρ=0.7` adjacent-null share `0.02973` (`2.97%`) — **PASS**.
7. **`e7_failure_composition.tsv`:** S1 SNR $\ge 2$: `41` failures, `40` supersets (`0.9756`), `39` one-null (`0.9512`) — **PASS**.
