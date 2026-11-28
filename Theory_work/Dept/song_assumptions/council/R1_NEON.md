# COUNCIL REVIEW — Round 1 — Seat: NEON (TH-SONG-ASSUMPTIONS)

**Package reviewed:** v1.1 (commit `5b62aaa9`, branch `dept/theory`, Astra R2 edits applied): `THEOREM_DEFINITIONS.md`, `ASSUMPTIONS_AND_PROOF_PATHS.md`, `SIMULATION_DATA_ANALYSIS.md`, `OWNER_DEFENSIBILITY_DOSSIER.md`.
**Overall score:** **7.5 / 10** — high-discipline, honest package with a strong mathematical architecture, held back from immediate delivery by **2 blockers** (`A-MARGIN-U` when $B_{Dm} \le 0$; `A-NEC` precedent mischaracterisation) and **7 substantive fixes**.

---

## 1. Assumption score table

| Assumption | D | R | One-line reason |
|---|---:|---:|---|
| **A-GL** | 9 | 8 | Precedents and S1/S2 match; minor scope clash ("every theorem" vs TM-a0) and determinant exponent typo on `ASSUMPTIONS` l.49. |
| **A-SPARSE** | 7 | 9 | Well-used and justified via `rem:sharp`(a), but mis-cites SL Thm 4 as using (4), cites bare `SC11` (growing $s_n$), and overclaims growing $s_0$ in Dossier l.61. |
| **A-DIM** | 9 | 9 | Verified precedents (SBJ, JR12, SL Cor S1) and S1/S2/user regimes ($A \le 1.77$); cleanly drives `prop:dist(i)` and union bounds. |
| **A-DIM′** *(conj.)* | 9 | 3 | Admirably honest about failed testing step and high risk, but proof route fails at the proposed rate (insufficient) and formula degenerates at $s = 0$. |
| **A-SUBG** | 7 | 9 | Cleanly yields sparse isometry and Hellinger conversion (rightly distinct from SL Cond. 3), but falsely claims arbitrary bounded predictors with variance bounded below imply `A-SUBG`. |
| **A-NEC** | 5 | 8 | Sound role in Occam penalty, ridge control, and TS-b converse; **BLOCKER**: falsely claims dominance over NH14 4.5 / SBJ A4 and mislabels SL (26) as a "fixed-type sample floor". |
| **A-BS / A-BS′** | 8 | 7 | Verified on S1/S2 and honest about `prop:dist(i)` tie-in, but omits that YWJ/SC11 upper bounds grow with $g/\varphi_n$ and fixed coordinatewise $\bar b$ is stronger than aggregate energy. |
| **A-MARGIN-H** | 9 | 6 | Exact SL Thm 3 analogue and honest on 9/136 S1/S2 coverage, but quantifying over $|S| \le q_n$ is stronger than step 2 ($|S| \le J$) and exceeds `A-SUBG`'s $q_n$ window on $S \cup S_0$. |
| **A-MARGIN-U** | 8 | 6 | Strong deletion/converse core and S1/S2 diagnostics, but **BLOCKER**: stays active when $B_{Dm} \le 0$ (forcing unneeded $\sqrt{2m\log p}$ floor), $C$ unquantified, and Dossier misstates S2 denominator (`11,466` vs `10,666`). |
| **A-MIS(iii)** | 7 | 8 | Exact reduction to `A-GL` is clean and balanced by `TM-a0`/remarks, but E7 $\sigma^2/\sigma_C^2$ uses data-selected MPM (caveat omitted in Dossier scorecard), Rossell Prop. 6 is fixed-design, and discrete-$y$ note is misplaced here. |
| **A-MOM** | 9 | 10 | Exact match to SL Cond. 4 + fixed-subset proof; minimal and plausibly sufficient via SLLN (density) and LIL under $E[Z_j^2 u^2] < \infty$ (exact support a.s.). |

---

## 2. Overall score and 1-to-1 Song & Liang (2015) map verdict

- **Overall package score:** **7.5 / 10.** Post-Astra-R2 honesty is a major strength (refuted `TD′` route clearly flagged, `SUBG ≠ Cond. 3` fixed, `E K₁` demoted to diagnostic, `TM-a0` tightened). Fixing the 2 blockers and 7 substantive items below will bring the package cleanly to deliverable quality (~9/10).
- **1-to-1 SL map (`THEOREM_DEFINITIONS.md` §§2–3):** **Complete and substantively correct**, with one qualification needed in §3 row `SL-6, SL-7` (l.82): calling `A-NEC` simply "weaker than SL's own replacement (26)" should be qualified by the differing set-size windows ($q_n$ vs $\bar r_n + |t|$) and population-vs-sample domains (even though $c_\psi/n$ vanishes faster than SL's $l_n \gg \bar r_n \log P_n / n$ and drops the upper bound $l'_n$). Every major SL result (posterior (7)/EBIC, Thms 1–4, Cors 1–2, Conds 1–5, Thm S, Cor S1, Lemma 1.1–1.2, Lemma S2, §3.1, §6 complexity, SAMC) is accurately catalogued and mapped.

---

## 3. BLOCKERS and SUBSTANTIVE criticisms

### BLOCKERS (must fix before delivery)

1. **[BLOCKER] `A-MARGIN-U` imposes an unnecessary $\sqrt{2m\log p}$-scale signal floor when $B_{Dm} \le 0$ (and leaves $C$ unquantified).**
   - *Locations:* `THEOREM_DEFINITIONS.md` §4.2 (ll.140–144); `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (ll.131–137); `OWNER_DEFENSIBILITY_DOSSIER.md` (ll.153–155).
   - *Flaw:* Because `A-MARGIN-U` quantifies over all $m \le J = s + C_s M$ and keeps $w_{Dm} + t_n$ outside $[B_{Dm}]_+$, whenever $B_{Dm} \le 0$ (all $m > j_0 \approx \frac{2(\mathrm{Pr}_n(d)+\gamma\log n)}{\log(n/(C\log p))}$, while $J$ can be much larger), it still demands $\sqrt{(1-\delta)R_n(S)/\sigma^{*2}} \ge w_{Dm} + t_n$. Yet for $B_{Dm} \le 0$, $\mathrm{RSS}_S \ge \mathrm{RSS}_U$ holds deterministically for $S \subset U$, so the class sum $\sum_{|N|=m} F_S/F_T$ is already $O_P(n^{-\gamma})$ with $R_n(S) = 0$ (zero signal needed!). Worse, under the stated combinatorial option $w_{Dm} \le \sqrt{2\log\binom{p-s_0}{m}} \approx \sqrt{2m\log p}$, at $m = J$ this forces $R_n(S)/\sigma^{*2} \gtrsim 2J\log p$, which **fails on S1 and every boundary-signal design**. In addition, the constant $C$ inside $B_{Dm} = \mathrm{Pr}_n(d) - \frac{m}{2}\log(n/(C\log p)) + \gamma\log n$ is never quantified.
   - *Fix:* Impose the `A-MARGIN-U` inequality **only on classes $(D, m)$ with $m \le J$ and $B_{Dm} > 0$** (and state in TS-b step 3 that classes with $B_{Dm} \le 0$ contribute $O_P(n^{-\gamma})$ immediately via $\mathrm{RSS}_S \ge \mathrm{RSS}_U$). Either quantify $C = C(s, A, L, c_\psi, \bar b, M)$ or absorb $(m/2)\log C = O(1)$ into $\gamma\log n$ and write $\log(n/\log(p \vee e))$.

2. **[BLOCKER] `A-NEC` mischaracterises NH14 Cond. 4.5, SBJ A4, and SL (26).**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (ll.105–106); `OWNER_DEFENSIBILITY_DOSSIER.md` scorecard (l.26) & `A-NEC` (ll.108–113); `THEOREM_DEFINITIONS.md` §3 row `SL-6, SL-7` (l.82).
   - *Flaw:* Claiming `A-NEC` is "*weaker* than every verified precedent" and calling SL (26) a "fixed-type sample floor" are both factually wrong (and contradict `PRECEDENTS_2026-11-17.md` B6 l.92):
     - NH14 Cond. 4.5 (pp. 11, 17) bounds the minimum **nonzero** eigenvalue (explicitly allowing exact duplicates/zero eigenvalues on p. 17) and allows floors $\gtrsim p_n^{-\kappa}$, which can be smaller than $c_\psi/n$ at large $p$.
     - SBJ Assumption 4 (p. 14) likewise bounds the minimum **nonzero** eigenvalue $\nu_{k*}$ (allowing exact duplicates outside $t$).
     - SL (26) (SLs p. 15) is a **vanishing** two-sided sample tail condition (Cor S1 uses $l_n = \log^{k_2}(n)/\sqrt{n} \to 0$; Thm S needs $l_n \gg \bar r_n \log P_n / n$), not a "fixed-type sample floor", and applies on sets of size $\bar r_n + |t|$ rather than $q_n$.
   - *Fix:* State accurately that on full-rank submatrices, `A-NEC`'s $c_\psi/n$ rate vanishes faster than BRT09 ($c/\log n$), MY09, SBJ ($\gg (\log p)/n$), and SL (26) ($l_n \gg \bar r_n\log P_n/n$) with no upper eigenvalue bound; admit that unlike NH14 4.5 and SBJ A4 (minimum *nonzero* eigenvalues; NH14's $p_n^{-\kappa}$ can be smaller), `A-NEC` excludes exact duplicates on $q_n$-sets, and domains/window sizes differ. Correct "fixed-type sample floor" for SL (26) to "vanishing two-sided sample tail condition".

### SUBSTANTIVE criticisms

3. **[SUBSTANTIVE] `A-SUBG`: false claim that bounded predictors with variance bounded below imply `A-SUBG` (and dominate SL Thm 1); minor isometry wording slip.**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (ll.92, 99); `OWNER_DEFENSIBILITY_DOSSIER.md` (l.100).
   - *Flaw:* False for correlated bounded predictors. Counterexample: $x_1, x_2 \in [-1,1]$ with $\mathrm{Var}(x_j) \ge 1/8$ and $x_2 - x_1 = \xi/2$ where $P(\xi = \pm 1) = \epsilon/2$, $P(\xi = 0) = 1-\epsilon$ ($\epsilon = 1/n$). This satisfies $|x_j| \le 1$ (SL Thm 1), $\mathrm{Var}(x_j) \ge 1/8$, and `A-NEC`, yet along $u = (-1, 1)^\top$ the variance-relative sub-Gaussian constant diverges as $(\epsilon\log(1/\epsilon))^{-1/2} \to \infty$. Also l.92 claims "lower sparse isometry" on "$(s_0 + j_0)$-sparse $v$" gives the two-sided transfer $(1-\delta)R \le \hat R \le (1+\delta)R$; two-sided transfer needs two-sided isometry on $(s_0 + J)$-sparse $v$.
   - *Fix:* Match `or5_assumptions.tex` ll.133–135: state that independent bounded predictors (or linear mixtures $x = m + B\eta$ of independent bounded features with bounded standardized range) satisfy `A-SUBG`, whereas arbitrary correlated bounded predictors (SL Thm 1) are not dominated. On l.92, write "two-sided sparse isometry on $(s_0 + J)$-sparse $v$".

4. **[SUBSTANTIVE] `A-MARGIN-H` quantifies over $|S| \le q_n$ instead of $|S| \le J = s + C_s M$ (anti-stringency + `A-SUBG` window mismatch), and TS-a reuses $c_H$ verbatim.**
   - *Locations:* `THEOREM_DEFINITIONS.md` §4.2 (ll.134, 136); `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (l.123) & §3.2 (ll.217–220); `OWNER_DEFENSIBILITY_DOSSIER.md` (l.139).
   - *Flaw:* Step 2 already restricts to $|S| \le J = s + C_s M$ via `prop:dist(i)`. Quantifying `A-MARGIN-H` over growing sets $|S| \le q_n \asymp M\log n$ is strictly stronger than needed, AND at $|S| = q_n$ the contrast support $S \cup S_0$ can have size $q_n + s_0 > q_n$, leaving `A-SUBG`'s $q_n$-sparse window. Furthermore, step 3 yields $\Pi(j \notin S \mid D_n) \le 2n^{-c_H M}$ on the TD event, so absorbing the factor $2$ into the exponent requires a slightly smaller constant $c'_H < c_H$ in `THEOREM_DEFINITIONS.md` l.136.
   - *Fix:* Restrict `A-MARGIN-H` to $|S| \le J = s + C_s M$ (guaranteeing $|S \cup S_0| \le 2s + C_s M \le q_n$ for large $n$; under `A-DIM`, $\log n$ also suffices in place of $\log(p \vee n)$). Use $c'_H$ (or explicit $2n^{-c_H M}$) in TS-a's display.

5. **[SUBSTANTIVE] `A-SPARSE` mis-cites SL Thm 4 and bare `SC11`, and Dossier overclaims growing $s_0$.**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (l.63); `OWNER_DEFENSIBILITY_DOSSIER.md` (ll.58, 61).
   - *Flaw:* Both files state SL strict sparsity (4) is "used by SL Thms 2–4". Direct check of SL p. 957 shows Thm 4 does **not** assume (4); it assumes a fixed candidate subset $s$ and Cond. 4 (already fixed in `THEOREM_DEFINITIONS.md` after `S1_SL_CITATION_CHECK.md` l.53, missed here). Bare `SC11` on l.63 has no label/page and allows growing $s_n \le p_n \le n$ (P17 l.36). Dossier l.61 states "Growing $s_0$ is possible for TS-b if $s_0^2\log p = o(n)$ and $s_0(\log p)^2 = o(n)$", overclaiming Fable's heuristic (Astra R1 Q5 noted the finite-class proof cannot simply be reused).
   - *Fix:* Change "Thms 2–4" to "Thms 2–3" (plus Thm S, SLs p. 13); drop `SC11` from `A-SPARSE`; hedge Dossier l.61 as a heuristic suggestion matching `ASSUMPTIONS_AND_PROOF_PATHS.md` l.66.

6. **[SUBSTANTIVE] Numerical error in Dossier S2 denominator (`11,466` vs `10,666`) and $E K_1$ formula/number mismatch.**
   - *Locations:* `OWNER_DEFENSIBILITY_DOSSIER.md` (l.173); also `THEOREM_DEFINITIONS.md` l.166, `ASSUMPTIONS_AND_PROOF_PATHS.md` l.264, `SIMULATION_DATA_ANALYSIS.md` l.20, `OWNER_DEFENSIBILITY_DOSSIER.md` l.176.
   - *Flaw:* (a) Dossier l.173 says `"Recovery when it fails is 0 on S1 and 9 of 11,466 fits on S2."` In `tables/e1_2x2_predictors.tsv`, S2 has `9 / 10,666` (`9 + 10,657`), while `11,466` is S1 + S2 combined (`800 + 10,666`). (b) All four files attribute `0.033–0.056` at S1's $(n, p)$ directly to the asymptotic $\chi^2$ formula $(s_0+1)/\sqrt{2\pi L(n+1)}$ with $L = 2\log((2p-s_0-1)/(s_0+1)) + \log(n+1)$; that formula evaluates to **`0.031–0.050`** (`0.0503, 0.0440, 0.0348, 0.0306`), whereas `0.033–0.056` is Fable's exact-Beta finite-$n$ evaluation (`FABLE_R1.md` ll.165–166).
   - *Fix:* Correct Dossier l.173 to `"0 of 800 on S1 and 9 of 10,666 on S2 (9 of 11,466 combined)"`. For $E K_1$, state `"0.031–0.050 from the χ² approximation (0.033–0.056 under the exact Beta tail)"`.

7. **[SUBSTANTIVE] `A-DIM′` formula degenerates when $s = 0$.**
   - *Locations:* `THEOREM_DEFINITIONS.md` §4.1 (l.121); `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (l.80); `OWNER_DEFENSIBILITY_DOSSIER.md` (l.79).
   - *Flaw:* `A-SPARSE` (`asm:dist`) allows $s = 0$ for TD, where $s\cdot M\cdot\log p\cdot\log(p\vee n) \le c_{\mathrm{dim}} n$ collapses to $0 \le c_{\mathrm{dim}} n$ even though the coarse cutoff $q_n \asymp M\log(p\vee n)$ remains positive (Astra R2 Q1).
   - *Fix:* Replace $s$ by $(s+1)$ in `A-DIM′`.

8. **[SUBSTANTIVE] `A-GL`: garbled marginal-likelihood determinant exponent, and "Every theorem" contradicts `TM-a0`.**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (ll.48–49); `OWNER_DEFENSIBILITY_DOSSIER.md` scorecard (l.22).
   - *Flaw:* Line 49 prints `|I + X_SᵀX_S|^{-1/2} · (n+1)^{…}`, flipping the sign of the exponent on $|I + G_S|$ and omitting $|(n+1)G_S + I|^{-1/2}$ (exact factor is $|I + G_S|^{+1/2}|(n+1)G_S + I|^{-1/2}$, as on l.227). Also "Every theorem" / "all" conflicts with `TM-a0` lying outside `A-GL` (`THEOREM_DEFINITIONS.md` l.185).
   - *Fix:* Print $|I + G_S|^{1/2}|(n+1)G_S + I|^{-1/2}$ on l.49; clarify scope as "TD, TS (and candidate-level via `A-MIS(iii)` for TM-a/b; not TM-a0)".

9. **[SUBSTANTIVE] Precision gaps in `A-BS` precedents and `A-MIS(iii)` statement/evidence.**
   - *Locations:* `ASSUMPTIONS_AND_PROOF_PATHS.md` §2 (ll.118, 167, 170–171); `OWNER_DEFENSIBILITY_DOSSIER.md` (ll.30, 130, 197, 200).
   - *Flaw:* (a) `A-BS` cites YWJ (7a) and SC11 2.7 without noting their upper bounds grow with $g \asymp p^{2\alpha}$ / $\varphi_n$, whereas `A-BS` uses a fixed constant (caveat in P17 B4b l.64). (b) `ASSUMPTIONS` l.167 places "(for a possibly discrete response, $f_0$ is the optimiser of the expected Gaussian log score...)" inside `A-MIS(iii)`, where $u \sim N(0,\sigma_C^2) \perp x_C$ makes $y$ strictly continuous (belongs in `TM-a0`/`A-MOM` only). (c) Dossier scorecard l.30 ("$\sigma^2$ ratio 0.99") omits S2 (`0.84–0.98`) and omits that E7's $C = \mathrm{MPM}$ is outcome-selected (violating `A-MIS(iii)`'s prespecified-$C$ premise, so it is an in-sample variance diagnostic only, per Astra R1 Q6). Also Rossell (2022) Prop. 6 is fixed-design Gaussian mean misspecification (deterministic bias), not random-design independent Gaussian noise.
   - *Fix:* Add the growing-vs-fixed caveat for YWJ/SC11; move the discrete-$y$ parenthetical out of `A-MIS(iii)`; label E7 $\sigma^2/\sigma_C^2$ as an in-sample diagnostic on data-selected MPM (include S2 `0.84–0.98` in scorecard) and note Rossell Prop. 6 is fixed-design.

---

## 4. NITPICKS (did not lower scores)

1. `THEOREM_DEFINITIONS.md` l.3 still reads `"Draft v1 (after advisor round 1...)"` despite containing Astra R2 edits (v1.1).
2. `ASSUMPTIONS_AND_PROOF_PATHS.md` l.90 and `OWNER_DEFENSIBILITY_DOSSIER.md` l.89 use $\zeta$ in `A-SUBG` without defining $\zeta_j = (x_j - Ex_j)/\mathrm{sd}(x_j)$ inside those files.
3. `THEOREM_DEFINITIONS.md` l.154 and `ASSUMPTIONS_AND_PROOF_PATHS.md` l.140 use `price_n` without defining it in §4 (define $\mathrm{price}_n := \mathrm{price}(s_0-1) = \mathrm{Pr}_n(1)$).
4. `SIMULATION_DATA_ANALYSIS.md` l.92 says `"Medians over settings:"` above a table of min–max ranges.
5. `THEOREM_DEFINITIONS.md` l.117 (`TD-as`) should explicitly mention $M \ge M_0$ and "on a common probability space"; l.198 cites `supplement_or l.135–153` where `asm:omitted` starts at l.126.
6. `THEOREM_DEFINITIONS.md` l.185 (`TM-a0`) omits that the coded method requires $p_C \ge 2$ and $n \ge 2p_C$ (so $K = p_C$).
7. `ASSUMPTIONS_AND_PROOF_PATHS.md` l.53 lists NH14 Cond. 4.3 and YWJ p. 7 alongside SL (1) and Jiang (2007) without distinguishing conditional-on-$X$/fixed-design from i.i.d. random-pair formulations.

---

## 5. Independent spot-checks

### Citations checked directly against `.rc_tmp/song/papers/` (9 checked)
1. **Song & Liang (2015) main (`32.txt`, pp. 953–957):** Thm 2 (l.385), Cor 1 (l.396), Cond. 3 (l.468), Cond. 4 (l.578), Thm 4 (l.583), Cor 2 (l.599) verified. **Finding:** Thm 4 does NOT use strict sparsity (4) → **caught S5**.
2. **Song & Liang supplement (`32b.txt`, pp. 6, 13, 15–16):** Lemma 1.2 (l.325), Thm S (l.738), "(22) is hardly satisfied" & (26) (ll.911–928), "Lemma A.2" reference (l.945), Cor S1 (l.949) verified. **Finding:** (26) has vanishing non-increasing $l_n$, not a "fixed-type sample floor" → **caught S2**.
3. **Narisetty & He (2014) (`NH14.txt`, pp. 11, 16–17):** Cond. 4.4 $\Delta_n(K) > 5\sigma^2|t|(1+\delta)\log(\sqrt n \vee p_n)$ (ll.532–534) verified; p. 17 (ll.831–836) confirms Cond. 4.5 bounds minimum *nonzero* eigenvalue $\gtrsim p_n^{-\kappa}$ and explicitly allows exact zero eigenvalues / perfect correlation → **caught S2**.
4. **Shin, Bhattacharya & Johnson (2018) (`SBJ.txt`, pp. 13–14):** Assumps. 1–5 and "continue to hold when $p$ grows polynomially in $n$, i.e., at the rate $O(n^\gamma)$ for some $\gamma > 1$" (ll.690–709) verified; display (8) (ll.679–683) confirms $\nu_{k*}$ is minimum *nonzero* eigenvalue → **caught S2**.
5. **Luo & Chen (2013) (`LC13.txt`, p. 7):** Consistency Condition $\lim \min\{\Delta_n(s)/(p_{0n}\ln p_n) : s_0 \not\subset s, \nu(s)\le k_n\} = \infty$ and Chen–Chen $\gamma > 1 - 1/(2\kappa)$ (ll.178–187) — **PASS**.
6. **Wainwright (2009) (`Wainwright09.txt`, p. 4):** Thm 2 necessary condition $n < (C'/M^2(\beta^*)) \log(p/s)$ (ll.186–191) — **PASS**.
7. **Fletcher, Rangan & Goyal (2009) (`FRG09.txt`, p. 4):** Thm 1 ML failure $m(n) < \frac{2-\delta}{\mathrm{MAR}\cdot\mathrm{SNR}} k\log(n-k) + k - 1$ (ll.211–215) — **PASS** (constant 2 properly flagged as C2's derivation).
8. **Yang, Wainwright & Jordan (2016) (`YWJ.txt`, p. 7):** Quote "some form of upper bound on the norm $\|\beta^*\|_2$ in terms of the $g$-hyperparameter is required" (ll.382–384) verified; bound grows with $g$ → **caught S9(a)**.
9. **Johnson & Rossell (2012) (`JR12.txt`, p. 651) & Rossell (2022) (`Rossell22.txt`, pp. 16–17) & Grünwald & van Ommen (`GvO17.txt`, pp. 1–3):** JR12 Thm 1 ($p \le n$) **PASS**; GvO empirical-only / heteroscedastic setting **PASS**; Rossell Prop. 6 confirmed fixed-design Gaussian mean misspecification → **caught S9(c)**.

### Numbers checked directly against `tables/` (10 checked)
1. **`e1_s1_cells.tsv`:** S1 SNR=1 $\kappa_{\text{pop}} \in [0.636, 0.700]$ (0/100 exact); SNR=2 $\kappa_{\text{pop}} \in [2.543, 2.801]$ (exact 0.92–0.96); $\kappa_{\text{multi}} < \kappa_{\text{del}}$ in 16/16 settings — **PASS**.
2. **`e1_2x2_predictors.tsv`:** P1 sample $\min t^2 > 2\cdot\text{price}$: S1 sens `1.000`, `0/800`; S2 sens `0.9851`, `9/10,666` (`P = 0.000844`); combined `9/11,466` — **FAIL on Dossier l.173** ("9 of 11,466 fits on S2" → **S6**).
3. **`e1_auc.tsv`:** S2 AUCs: $\kappa_{\text{del}} = 0.9798$, $\kappa_{\text{pop}} = 0.9583$, $\Lambda_{\min}/\log n = 0.9666$, $\kappa_{\text{adj,full}} = 0.9724$ — **PASS**.
4. **`e1_margin_by_setting.tsv` (E2):** `e2_over_eps2 >= 1` in `4` (S1) + `5` (S2) = `9/136` settings; S1 SNR=2 ratio `0.7529` — **PASS**.
5. **`summ_E4.tsv`:** $\max|\beta|/\sigma$: `1.175` (S1), `1.095` (S2); $\nu_{\text{pop}}$: $\le 3.938$ (S1), $\le 6.000$ (S2) — **PASS**.
6. **`summ_E5.tsv`:** $n \times \text{floor}$: `125–250` (S1), `8.82–100` (S2); S2 greedy `m2`: `7.07e-6` to `2.43e-4` — **PASS**.
7. **`e6_S1S2_regimes.tsv` & `e6_typical_regimes.tsv`:** $A \in [0.900, 1.371]$ (S1), `[1.500, 1.766]` (S2), $\le 1.736$ (user); $\kappa_{\text{eff}} \in [0.130, 0.221]$ (S1), `[0.326, 0.451]` (S2); $\log p/\sqrt{n} \le 0.977$ — **PASS**.
8. **`e7_failure_composition.tsv`:** S1 SNR$\ge 2$: `41` failures, `97.56%` (40/41) supersets, `95.12%` (39/41) one extra null — **PASS**.
9. **`e7_E6_sigma2C.tsv` & `e7_E4_dH_by_group.tsv`:** $E[\sigma^2\mid\text{MPM}]/\sigma_C^2$ median `0.987–0.990` (S1), `0.837–0.979` (S2); max q90 $d_H/\varepsilon_n = 0.632$ — **PASS** (Dossier l.30 omits S2 range).
10. **Direct check of printed $E K_1$ formula** at S1 $(n,p,s_0=10)$: $(s_0+1)/\sqrt{2\pi L(n+1)} \in [0.0306, 0.0503]$ vs printed `0.033–0.056` (exact-Beta values from `FABLE_R1.md`) — **FAIL (minor misattribution → S6)**.
