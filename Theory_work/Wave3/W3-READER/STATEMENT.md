# W3-READER — STATEMENT (v1.0, 2026-11-16; lead: Claude Opus 5.5, Claude Third, high)

Claims of this ticket that are registered and checked like any claim (manager's H5 card 5 action 6(c); PROTOCOL_v4
Tier B). The reader versions themselves are in `READER_VERSIONS.md` (corollaries = master + bridges); their bridges are
the lemmas below. Statuses are those of the proof files until a check record says otherwise.

## Changelog
| version | date | change | tag |
|---|---|---|---|
| 1.0 | 2026-11-16 | first version: PoolZ; bridge lemmas R1–R4 | — |

## Claim PoolZ (the pooled evidence estimate is unbiased)
Status: **PROVED (by this seat, unchecked)** (line check: bridge-leg Sol review).
**Setting.** The method as coded on the SMC branch, under the N1 premises (`Theory_work/Wave1/W1-N1/STATEMENT.md` §2:
EX-A, EX-S/H-U, START, KERNEL, CAL, SI, MEAS, potential run); calibration record $\mathcal C$, success event
$\mathcal A\in\sigma(\mathcal C)$; on $\mathcal A$ the final run has $R'=4$ islands with evidence estimates
$\hat Z_1,\dots,\hat Z_4$, and the reported evidence is the equal-weight mean $\hat Z:=\tfrac14\sum_{r=1}^4\hat Z_r$
(code: `Scripts/SMC_BVS/core/v3_run.R:154`, `log_Z = log_sum_exp(logZr) - log(R)`, with `islands = 4L` at `:91`;
as recorded at `Theory_work/Wave3/W3-SAMP/STATEMENT.md:52-53`, with $R'=4$ at :42). $Z=\sum_{S\in\Omega}\varpi(S)m(S)$.

**Claim.** Data fixed (probability over the final streams), almost surely on $\mathcal A$: $\ E[\hat Z\mid\mathcal C]=Z$, i.e.
$E[\hat Z/Z\mid\mathcal C]=1$ on $\mathcal A$. Consequently, under the joint law with the H-U/SI idealisation used in the proof,
$E[\mathbf 1_{\mathcal A}\hat Z]=E[\mathbf 1_{\mathcal A}Z]$ [R1-E9]. No condition on the design or the data.

*Proof.* `W1-N1:Thm-N1@1.0.0` ("PROVED-CHECKED"; `W1-N1/STATEMENT.md:98-104`) gives, for each fixed $r\ge1$, almost surely
on $\mathcal A\cap\{r\le R'\}$, $E[W_r\mid\mathcal C]=1$ with $W_r:=\hat Z_r/Z$ (its "in particular" clause, :104). On
$\mathcal A$, $R'=4$, so this holds for $r=1,\dots,4$ simultaneously (four null sets). By linearity of conditional
expectation, $E[\hat Z/Z\mid\mathcal C]=\tfrac14\sum_{r=1}^4E[W_r\mid\mathcal C]=1$ a.s. on $\mathcal A$. In W1-N1's
conditional statement the data are fixed (probability over the final streams), so $Z>0$ is a constant and
$E[\hat Z\mid\mathcal C]=Z$ on $\mathcal A$. Under the joint data/algorithm law, with the final streams idealised as independent of the
data and of streams 0–9 (H-U/SI, as in `W3-SAMP/STATEMENT.md:35-36`), the same identity holds conditionally on
(data, $\mathcal C$); taking expectations of $\mathbf 1_{\mathcal A}E[\hat Z\mid\text{data},\mathcal C]=\mathbf 1_{\mathcal A}Z$
gives the last form. ∎

*Remarks.* (i) No independence between islands is used (N1 uses none; SI is per island). (ii) This concerns $\hat Z$
only; the reported PIPs are an equal-weight mean of the islands' Rao–Blackwellised PIPs, not a $\hat Z$-weighted
average, and are covered by `W3-SAMP:LT#` (LT-d) and `W3-SAMP:C`. (iii) The identity is about the potential
(uninterrupted) record; on completed runs the reported $\hat Z$ equals it (`W3-SAMP:PC`, "PROVED-CHECKED").

## Bridge lemmas (proofs in `lemmas/`)
| id | statement (short) | file | used by |
|---|---|---|---|
| R1 | set-size and elementary bridges B1.1, B1.2, B1.3, B2.1, B3.2, B4.1, B6.1 | `lemmas/R1_set_sizes.md` | Thms 1, 2, 3, 4, 6 |
| R2 | local regressions ⇒ variance clause (population R2.1; sample R2.2) | `lemmas/R2_local_regression.md` | Thms 6, 7 |
| R3 | (historical) delivery assembly: RM2 conclusions ⇒ F-UNI premises (S), (P), (V); operational premises carried as (S4) | `lemmas/R3_delivery_assembly.md` | former Thms 6, 7 only (current ones use B6.6′, B7.5) [R1-F2] |
| R4 | printed outputs consistent: Thm 2 + Thm 5 ($Q=S_0$) + `W3-SAMP:C` (C-v) | `lemmas/R4_printed_outputs.md` | Thm 10 (row 3.6) |
