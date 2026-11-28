# Verbatim copy of the claim re-checked by X5 (so that the council manifest contains it)

Source: worktree W3-READER, branch theory/W3-READER, file Theory_work/Wave3/W3-READER/STATEMENT.md lines 12–37 (last changed at commit 68443dcc; file sha256 29696a79d4f0ba14…), copied 2026-11-16. Not edited.

```
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
```
