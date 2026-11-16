# R4 — Printed outputs are consistent: assembly for card row 3.6 (Theorem 10) (W3-READER bridge leg, 2026-11-16)

Status: **PROVED (by this seat, unchecked)**. An assembly; no new probability. Input statuses [S2-F7, S3]:
`W3-START2:IF-START`, `W3-START2:START-R` "PROVED-CHECKED"; `W3-SAMP:C@1.1.3` "PROVED-CHECKED, conditional on
SOP:TH09" [REG-33e1]; `W2-APP:POST@1.0.6` "PROVED-CHECKED,
conditional on SOP:TH09" [REG-33e1]; `W3-POST:Thm-1` item 6 "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF
VERIFIED (A-REV2)"; this ticket's bridges R1 (B2.1, B6.1) "PROVED (by this seat, unchecked)". Scope: the sampler branch; the (C-v) statements
concern the potential records on $\mathcal A$ and equal the printed fields on completed runs (Lemma PC) [S2-F3].

## Inputs (statuses verbatim, registry)
- `W3-SAMP:C@1.1.1` (Theorem C, `Theory_work/Wave3/W3-SAMP/STATEMENT.md:149-163`), "PROVED-CHECKED". Clause (C-v): under the
  N1 premises (`W3-SAMP/STATEMENT.md` §1 = `Theory_work/Wave1/W1-N1/STATEMENT.md` §2: EX-A, H-U, START, KERNEL, CAL, SI,
  MEAS, POT), if $1_{\mathcal A}\bar\delta\to0$ in probability then for every $\epsilon>0$:
  $P(\mathcal A\cap\{|\hat Z/Z-1|>\epsilon\})\to0$, $P(\mathcal A\cap\{|\log\hat Z-\log Z|>\epsilon\})\to0$,
  $P(\mathcal A\cap\{\|\mathrm{pip\_primary}-\mathbf 1_{S_0}\|_\infty>\epsilon\})\to0$, $P(\mathcal A\cap\{\mathrm{MPM}\neq S_0\})\to0$,
  $P(\text{completed}\cap\{\hat S\neq S_0\})\to0$; and if $1_{\mathcal A}\bar\delta=O_P(r_n)$ (deterministic $r_n\downarrow0$)
  then, localised to $\mathcal A$, $\hat Z/Z-1$, $\log\hat Z-\log Z$ and $\|\mathrm{pip\_primary}-\mathbf 1_{S_0}\|_\infty$ are
  $O_P(r_n)$ (:158-162). Here $\bar\delta:=\max(o_0,o_1)$, $o_1=\delta/(1-\delta)$, $o_0=\delta_0/(1-\delta_0)$,
  $\delta=1-\pi(S_0)$, $\delta_0=1-\pi_0(S_0)$ (:26-27); $\mathcal A$ = calibration returns "ok" (fallback grid included),
  $\{\text{completed}\}\subseteq\mathcal A$ (:38-41).
- `W3-START2:IF-START@1.0.0` (`W3-START2/STATEMENT.md:176-180`), "PROVED-CHECKED": under (T3⁺)(b) with $Q=S_0$,
  $1_{\mathcal A}o_0=O_P(\rho_n)$ with $\rho_n:=n^{-1/2}\exp(C_R\sqrt{\log n})$ for every event $\mathcal A$.
- Theorem 2 (`W3-POST:Thm-1@1.0.0` item 6 + `W2-APP:POST@1.0.1`, "PROVED (by this seat, unchecked); R02
  VERIFIED-WITH-AMENDMENTS, applied"): $\delta=O_P(\sqrt{\log n/n})$ under the joint law.

## Claim (R4)
Assume Setting R with the standardised-signal convention ($\theta^*$ deterministic,
$\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on $S_0$, $s_0\ge1$ fixed, $s_0<p\le n^A$), the population floor
$\lambda_{\min}(\Sigma_{n,S})\ge c$ for $|S|\le5(A+1)(s_0+1)\log n$, visibility (V-R) and no leakage ((L-R⁺) with $Q=S_0$),
and the N1 premises. Then $1_{\mathcal A}\bar\delta=O_P(\rho_n)$, and all conclusions of (C-v) hold with rate $\rho_n$.

*Proof.* (1) *Posterior.* The floor gives LSF with $\psi_n=c$ (R1, B2.1); `W2-APP:POST` covers the standardised-signal
convention (`L1_POST.md:11, 15-18`), so Theorem 2 gives $\delta=O_P(\sqrt{\log n/n})$. As $\delta\to0$ in probability,
$P(\delta\le\tfrac12)\to1$ and on that event $o_1\le2\delta$; so $o_1=O_P(\sqrt{\log n/n})$ (as noted at
`W3-SAMP/STATEMENT.md:75-76`). (2) *Start.* The floor covers (FL-R16) ($16+s_0\le5(A+1)(s_0+1)\log n$, R1, B6.1);
(V-R) and (L-R⁺) at $Q=S_0$ are assumed; $p>s_0$; so (T3⁺)(b) applies and IF-START⁺ gives $1_{\mathcal A}o_0=O_P(\rho_n)$.
(3) Since $e^{C_R\sqrt{\log n}}\ge\sqrt{\log n}$ for large $n$, $\sqrt{\log n/n}\le\rho_n$ eventually, so
$1_{\mathcal A}\bar\delta\le\max(o_1,1_{\mathcal A}o_0)=O_P(\rho_n)$; in particular $1_{\mathcal A}\bar\delta\to0$ in probability.
(4) (C-v) applies with $r_n:=\rho_n$ (deterministic, $\downarrow0$ eventually; $O_P$ is insensitive to finitely many $n$). ∎

**Common setting.** Theorem 2 and Theorem 5 are both stated for Gaussian rows with a correlation matrix $\Sigma_n$; the
conventions agree once Theorem 2 is read in the standardised-signal convention, which its input covers. No other
compatibility condition is needed: SAMP's $\pi$, $\pi_0$, $Z$ are the coded target, start law and evidence (SAMP §0),
the same objects as in Theorems 2 and 5 (`NOTATION.md` §4–§5).

**Not claimed.** $P(\mathcal A)\to1$ (calibration success) is not asserted by (C-v); under the delivery conventions (S4)
(on $\mathfrak D$, or for every $n$ under A:IDEAL-W⁺ [FUNI-N]) runs complete with probability one (F-UNI Step 2, "design-free"), which would remove the localisation to $\mathcal A$ —
recorded as a remark, not used. No claim about the estimated PIPs' distance to the *exact* posterior PIPs beyond what
the triangle inequality with Theorem 2 gives.
