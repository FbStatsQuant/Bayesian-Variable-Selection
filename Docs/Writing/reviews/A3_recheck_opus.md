# A3 re-check (diff-only), fresh Opus reader, 2026-11-16

Scope: `.rc_tmp/a3_fix_diff.patch` against the 12 rows of `A3_codex_fidelity.md`; sources: v1 `results/sections/*.tex`,
`results/STATUS_LEDGER.md`, `from_theory/TRACK_B_v1.4.md`. Line numbers are in the fixed files under `results_v2/`.

| id | hunk (fixed file:line) | verdict | one-line reason |
|---|---|---|---|
| A3-C01 | supplement.tex:202 | RESOLVED | "for a fixed $\kappa>0$" restored, as in v1 sec5_delivery.tex:303. |
| A3-C02 | supplement.tex:113 | RESOLVED | "where $b_n>0$ and $b_n^2n/\log n\to\infty$" matches v1 sec4_distribution.tex:150 word for word. |
| A3-S01 | supplement.tex:155-157 | RESOLVED | Now opens "keep the other assumptions of Theorem~\ref{thm:start}" (thm:start is the theorem at :146) and adds the "only predictors outside Q" clause, as in v1 sec5_delivery.tex:103-105. |
| A3-S02 | s1_results.tex:45; s3_model.tex:87 | RESOLVED | Both now restrict to models of at most $\min(K-1,p/2)$ predictors, as in v1 sec3_selection.tex:250 and :276. |
| A3-S03 | s1_results.tex:46-47; s3_model.tex:88 | RESOLVED | Both now say "expected posterior miss". The orthogonal exact order inherits "expected", as in v1 sec3_selection.tex:283-288. |
| A3-S04 | what_we_prove_v2.tex:33-34; s1_results.tex:38-40; s6_estimates.tex:7-9, 11-14 | NEW-ERROR | Table row 4 and the §6 In words are now correct. But the §6 Why says "on the event that the calibration succeeds, ... the median and reported models equal the true model with probability tending to one". For the reported model the source uses the completion event, not $\Acal$: P(run completes and $\Shat\neq\Sz$)→0 (v1 sec5_delivery.tex:403, :414). Also, the abstract and the Why lack the "no claim about how likely, or conditional on it" clause that v1 sec1_overview.tex:33 attaches to the same shorthand, contrary to the disposition. |
| A3-S05 | supplement.tex:217 | RESOLVED | The counts are now attributed to equicorrelation $\varrho\in\{0.5,0.7\}$, $p\ge2.5n$, $\sz\in\{4,8\}$, as in v1 sec5_delivery.tex:374-376. "these designs" now refers to that subset. |
| A3-F01 | s2_setting.tex:81-85 | NEW-ERROR | The final scan, the certification flag and "stops uncertified" now match v1 sec2_setting.tex:204-216. But "for at most a fixed number of moves (its move cap)" is new and wrong: the caps are $\ell_n=\lceil\log_2(n+p+1)\rceil$ and $\ell_n+\abs{\tSz}$, which grow with $n$ (v1 :207-208; v2 appendices.tex:35-36). In this document "fixed" means "independent of $n$". Fix: drop "fixed", or write "a capped number of moves (of order $\log(n+p)$)". |
| A3-F02 | s1_results.tex:26, 36, 43, 49-50, 54 | RESOLVED | Footnote $^a$ is on Results 1, 3, 4 (after "Consistency") and 5, matching v1 sec1_overview.tex:84-93 (footnote $^e$) and :109. |
| A3-F03 | s1_results.tex:49-50 | RESOLVED | It now says the orthogonal exact order uses the fixed-design expectation bound and has that bound's status. This is consistent with STATUS_LEDGER.md:18 ("upper half carries Thm 3.1's status") and with H4. |
| A3-F04 | s2_setting.tex:93-94 | RESOLVED | IND, AR and BLK are the planned $p=10^6$ runs, and FAC is "contingent, at $p=10^4$ only" (TRACK_B_v1.4.md:58). Wording nit: "a contingent design run at" can read as already run; "planned at" is safer. |
| A3-F05 | s6_estimates.tex:7, 12; s1_results.tex:39 | RESOLVED | The relative and log error of the evidence are now named, as in v1 sec5_delivery.tex:393 and :404. "converges to the exact evidence" is gone. |

## Unrelated-hunk check
Every hunk maps to one or more findings: abstract → S04; s1 → F02, S04/F05, S02/S03/F03; s2 → F01, F04;
s3 → S02/S03; s6 → S04/F05; supplement → C02, S01, C01, S05. No hunk changes a claim outside the 12 findings.
One note, not counted: the unchanged clause at s6_estimates.tex:7-9 still gives the order-$\rho_n$ rate to all "printed
estimates", median model included. The source gives the median model no rate, only P($\Acal\cap\{\MPMhat\neq\Sz\}$)→0.
This was in the as-read text and lies outside these findings.

## Suggested minimal fixes for the open rows
- S04: in the §6 Why, attach the reported model to completion. For example: "... the median model equals the true model, and a
  completed run reports the true model, with probability tending to one". Then add "(no claim is made about how likely that event is)"
  to the abstract and the Why.
- F01: replace "a fixed number of moves" with "a capped number of moves".

RECHECK: OPEN (A3-S04, A3-F01)

## Round 2 (diff `.rc_tmp/a3_fix2_diff.patch`; same method)

| id | hunk (fixed file:line) | verdict | reason |
|---|---|---|---|
| A3-S04 | s6_estimates.tex:7-11, 13-17; what_we_prove_v2.tex:34 | RESOLVED | The Why now ties the reported model to completion ("a completed run reports the true model"), as in v1 sec5_delivery.tex:403. The abstract and the Why now carry "no claim is made about how likely that event is", as v1 sec1_overview.tex:33 does. Optional nit: v1 also adds "or conditional on it". |
| A3-F01 | s2_setting.tex:82 | NEW-ERROR | "fixed" is gone, but "(of order $\log(n+p)$)" is true only of the base cap $\ell_n$. The search from the start mode has cap $\ell_n+\abs{\tSz}$ (v1 sec2_setting.tex:210-211). Here $\abs{\tSz}\le K=\min(p,\lfloor n/2\rfloor)$ (v1 :102), so that cap can be of order $n$. The phrase came from my own round-1 suggestion, which was wrong. Fix: "for at most its move cap ($\ell_n:=\lceil\log_2(n+p+1)\rceil$ moves, or $\ell_n+\abs{\tSz}$ for the search from the start mode)", or simply "for at most a capped number of moves". |
| A3-F04 (nit) | s2_setting.tex:94 | RESOLVED | "a contingent design planned at $p=10^4$ only" matches TRACK_B_v1.4.md:58. |
| median-rate note | s6_estimates.tex:7-11 | RESOLVED | The $\rho_n$ rate now covers only the evidence (relative and log error) and the inclusion probabilities. The median model gets $P(\Acal\cap\{\MPMhat\neq\Sz\})\to0$ and the reported model gets the completion statement, matching v1 sec5_delivery.tex:388-404. |

Unrelated-hunk check: the round-2 diff has four hunks, and each maps to a row above. Nothing else changes.

RECHECK: OPEN (A3-F01)

## Round 3 (F01; diff `.rc_tmp/a3_fix3_diff.patch`)

| id | hunk (fixed file:line) | verdict | reason |
|---|---|---|---|
| A3-F01 | s2_setting.tex:82-83 | RESOLVED | The caps are $\ell_n:=\lceil\log_2(n+p+1)\rceil$ for the first search (from the best model found) and $\ell_n+\abs{\tSz}$ for the search from the start mode. Both match v1 sec2_setting.tex:209-211. The final scan and the certification rule are unchanged and match :205-216. The one hunk changes nothing else. |

RECHECK: ALL-RESOLVED

## A2 renumbering (`assumptions/assumptions.tex`; diff `.rc_tmp/a2_renumber_diff.patch`)

Maps checked: v1 numbers from `results/what_we_prove_v1.pdf`; v2 numbers from `results_v2/what_we_prove_v2.aux`; v2 text from `results_v2/sections/*.tex`.

| v1 ref | v2 ref (assumptions.tex line) | same object? |
|---|---|---|
| Thm 3.1 (fixed design, beta-min, expectation bound) | Thm 3.2 (71, 177, 181, 185, 191, 223, 289) | yes (thm:post-fixed) |
| Thm 3.4 (identifiability margin) | Thm A.3 (101) | yes (thm:post-margin) |
| Thm 3.9 (random Gaussian design) | Thm 3.1 (71, 101, 108, 177, 192, 221) | yes (thm:post-random) |
| Thm 3.13(a) (every-design bound) | Rem 3.3(a) (170) | yes: rem:sharp(a) is the same display, with $\abs{S}\le\min(K-1,p/2)$ |
| Rem 3.2(ii) (without beta-min; specificity can fail) | Rem A.1 (184) | yes (rem:no-betamin) |
| Asm 3.3 (floor on the true model + margin) | Asm A.2(a) (187) | yes (asm:margin). It narrows to item (a), the floor, which the heading is about. |
| Asm 4.5(a) (floor ψ on (2A+3)s+2 sets) | "the floor of Theorem A.7" (187) | yes: inlined in thm:dist-param (supplement.tex:111-112), as the coordinator noted |
| Prop 4.3(ii) (no collinearity condition) | Prop A.6(ii) (209) | yes (prop:dist(ii), extra $\log(\praw\vee n)$ factor) |
| Cor 4.7 (sampler output) | Cor A.8 (288, 290) | yes (cor:dist-output) |
| Thm 5.7 (reported model, Gaussian rows) | Thm 5.3 (71, 103, 177, 221) | yes (thm:reported; assumes GR) |
| Asm 5.6(a); 5.6(b),(c) | Asm 5.2(a); 5.2(b),(c) (243, 256) | yes (asm:rr-leak, rr-floor, rr-local) |
| Thm 5.12, case (d1) | Thm A.11, case (d1) (262) | yes (thm:reported-fixed; (d1) is in Asm A.10(d), as v1's (d1) was in Asm 5.11(d)) |
| Thm 5.19 (estimates consistent) | Thm 6.2 (71, 104, 177, 221) | yes (thm:outputs) |
| Rem 5.21 (alternative argument, global overlap) | Rem A.13 (294) | yes (rem:alt-route; its premise is open) |
| Rem 5.22 (pooled evidence unbiased) | Prop 6.1 and Sec 6.1 (45) | yes: Prop 6.1 is per island; the pooled form is the text after it in Sec 6.1 |
| Thm 4.2, Lemma 2.1, Asm 4.1(c),(d),(e) | unchanged | yes: same numbers and items in v2 (asm:dist (c)-(e), lem:summaries) |

Changes other than a number or a reference:
- line 100 adds "(second version)" after "What we prove". It is harmless, but it is the only change that is not a number or a reference.
- line 187 has "the floor of Theorem A.7" in place of a number (the mapping the coordinator gave), and "3.3" becomes "A.2(a)". Both are acceptable.

v1 numbers still in assumptions.tex: the summary table keeps v1's **5.6(a)** (line 84, "Polynomial leakage set, 5.6(a)") and
**5.6(b),(c)** (line 86, "Floor and local regressions, 5.6(b),(c)"). Both should read 5.2. No other v1 number remains;
"Theorem 1/2/3", "Cor. 1" and "Condition 3" are Song and Liang's.

RECHECK: OPEN (A2: lines 84, 86 still cite v1 Assumption 5.6)
