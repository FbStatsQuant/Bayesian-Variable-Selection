# CW reviewer (Claude Work, Opus 5.5 xhigh), round 1 — reply copied from the task result (clientRequestId T03-review-CW-r1)

**Overall verdict: verified.** I checked every step of PROOF_v1 by hand, and ran numerical checks on the deterministic lemmas. The proof establishes conclusions (i)–(v) of STATEMENT.md from G, R, SE, H-T02 and BM-C (or BM-∞), using no other hypothesis. Conclusion (iv) uses no beta-min condition. No step is false and no step is unjustified. There are 8 findings, all at exposition level.

## Steps checked (no finding)

| Step | What was checked | Evidence |
|---|---|---|
| (eq:mn) | $m_n\le C_m\log n$, using $\log(2p)\le(1+A)\log n$, with the +1 absorbing the ceiling | by hand |
| Lemma 1 (reduction) | (a) $G_S$, $s_yz_S$, $\|w\|^2=Ns_y^2$, $s_y^2Q_S=Q^c_S$, and (score); the $\nu\log s_y^2$ term cancels across models. (b) $w=\mu_c+e$, $e\sim N_N(0,\sigma_\star^2I)$, $\|\mu_c\|=\|\mu\|$, $\mu_c\in\mathrm{col}(X_{c,S_0})$ | by hand; numerically, the identity error is ≤ 7e-14 over 400 pairs $(S,T)$, and $s_y^2Q_S=Q^c_S$ held 320/320 |
| Lemma 2 (smoother) (a)–(d) | $M_S=h(YY^\top)$; $0\preceq M_S\preceq\frac n{n+1}P_S$; the lower bound under $\lambda_{\min}\ge N\varphi_0^2$; operator monotonicity | by hand; 314/314 checks for (a)–(c) and 3396/3396 for (d) on random designs |
| Corollary 3 | upper bound needs (c) on $S$, which follows from interlacing; lower bound needs it only on $T$ | 10188/10188 random quadratic-form checks |
| Lemma 4 (determinants) | $D_S=\prod f(\lambda_i)$; Cauchy interlacing gives both bounds | 3396/3396 checks for the upper and lower bounds; 314/314 for $1\le D_S\le(n+1)^{\vert S\vert}$ |
| Lemma 5 (prior ratios) | ratio formula; (a); (b), including the case $s_0=i=0$ | exhaustive for $p<80$, all $s_0,j$: 0 violations |
| Lemma 6 (signal) | $\Delta_S=\min_\gamma\|X_{c,S'}\vartheta\|^2\ge N\varphi_0^2\|\theta^\star_J\|^2$ | by hand; 248/248 numerical checks |
| Lemma 7 (chi-square) | Chernoff algebra: $\lambda=s/(a+2s)$ gives exponent $-s^2$; lower tail $-t^2/(4d)$; truncated moment $(\tau/2)^{d/2}/\Gamma(d/2+1)$; $\Gamma(z+1)\ge z^ze^{-z}$ | by hand; exact scipy tails and quadrature over a $(d,x,\tau)$ grid: 0 violations |
| Lemma 9 (good event) | G1 needs $N\ge4\log n$, gives $2/n$. G2/G3: $p^ke^{-x_k}=e^{-k}/n$, $\sum_k e^{-k}=0.58\le1$, and $2k+3x_k\le C_Ak\log n$. G4: count $<(j_*+1)p^{j_*}2^{s_0}$, and $2s_0+3x\le C_*\log n$ matches the $C_*$ of STATEMENT. Total $5/n$ | by hand; G2 constant checked numerically over a grid |
| Lemma 10 (consequences of $\mathcal G_n$) (a)–(d) | including $n^3\le(n+1)^2(n-1)$, which is $n^2-n-1\ge0$; $1+n\eta_n\le2$ when $N\varphi_0^2\ge1$; Pythagoras for $V_S$; the arithmetic for $E_n$ and $\delta''_n$ | by hand; $2b+Q^c_S\le E_n+V_S$ held 248/248 |
| Lemma 11 (one superset) | exact ratio form; determinant factor; $(P_S-P_{S_0})w=(P_S-P_{S_0})e$; $\nu n/((n+1)N)=\frac12(1+\frac{0.02n+1}{n^2-1})$; $\theta_n-1\le2(\cdot)$ when $\delta_n\le\frac12$; $\epsilon_n\to0$ | identity error 1e-16; deterministic pre-$\mathcal G_n$ bound 66/66 |
| Proposition 12 (superset sums) | the indicators are built into $U_n$, so expectations are taken without $\mathcal G_n$; $(\theta_n-1)\tau_j/2=j\epsilon_n$; the form of $q_n$; $K_{s_0,j_1}$ bound; Markov | by hand |
| Lemma 13 ($S$ against $S'$) | prior factor; determinant; $0\le x<1$; the three-step lower bound on $\nu x$, including the negative case; $\frac V{E+V}\ge\min(\frac V{2E},\frac12)$; $\frac{n^2}{4(n+1)}\ge\frac n5$ for $n\ge4$ | 248/248 for both "SvsSp step" and "t diff lower"; scalar inequality checked for $n\le10^5$ |
| Lemma 14 (adding the signal) | $\sqrt{V_S}\ge\sqrt{\Delta_S}-\sqrt{N_S}$; $N_S\le\Delta_S/4$; $\log2+\frac12\log(n+1)\le\log n$ for $n\ge5$ | true for all $n\ge5$, false at $n=4$, as the proof states |
| Lemma 15 (assembling) | the map $S\mapsto S'$ is at most $(2^{s_0}-1)$-to-one; $\vert J'\vert\le m_n$; split at $j_*$; $(j_*+1)/2\ge s_0(A+\frac12)+1$ gives $n^{As_0}(n+1)^{s_0/2}n^{-(j_*+1)/2}\le2^{s_0/2}/n$ | by hand |
| Step 0 | $2^{-m_n}\le(2p)^{-s_0}n^{-(s_0+2)/2}$ gives $(1+\frac1n)^{s_0/2}n^{-1/2}\Theta_{n,m_n}$; $m_n$ is a deterministic integer sequence, so H-T02 applies | by hand |
| Step 1, (i)–(v) | $(1-\frac1n)(2L_*+1)\ge L_*$; $L_*/32\ge s_0(A+1)+2$ gives $\kappa_n\le e^{\rho_n}n^{-2}$; three-way partition of $\Omega\setminus\{S_0\}$; the "$Y_n1_{\mathcal G_n}$" device; PIP and MPM argument; strict maximiser and Markov in (iii); covering by $\mathcal U_j$ and a $j$-free bound in (iv); scaling in (v) | by hand |

The scratch scripts are in `<PC_TEMP_PATH>` (`check1.py`, `check2.py`, `check2b.py`). They ran single-seed, on 6 random designs with $n\in\{12,20,40\}$, $p\in\{5,6,7\}$ and $s_0\in\{0,\dots,3\}$. Every printed check had 0 violations.

## Findings

**F1** — Location: §2, Lemma 1(a) and eq. (score); used throughout §§4–6. Severity: exposition. Claim: The symbol $w$ means both the prior weight $w(k)$ and the contrast response $w=U^\top y^r$. Both appear in the same formulas, for example (score) next to $\|w\|^2$, and $\ell(S)=w(|S|)m(S)$. Evidence: Lemma 1(a) uses $w(|S|)$ and $\|w\|^2$ in the same statement. Lemma 13 has "$w(|S|)/w(|S'|)$" next to "$\|w\|^2$". The meaning is always recoverable from context. Verdict: verified (no mathematical effect).

**F2** — Location: throughout. Severity: exposition. Claim: Further notation overlaps: $M$ (the constant in R), $M_S$ (smoother matrix), $M_*$ and $M_n$; $U$ (basis matrix), $U_n$ (random sum) and $\mathcal U$ (set of models); $\theta_n$ (Lemma 11) and $\theta^\star$. Evidence: For example, Lemma 10(a) has "$2nM$" while $M_S$ is also in scope. No formula is ambiguous once read in context. Verdict: verified.

**F3** — Location: §1, "Plan" paragraph. Severity: exposition. Claim: Typo: "bounds the supersets of size at most $m_n$ size by size". Evidence: the sentence as written. Verdict: verified.

**F4** — Location: §6, opening "Throughout $n\ge n_0$", together with (ii) and (iii). Severity: exposition. Claim: STATEMENT (ii) says the PIP bound holds "for every data set", and (iii) states a Markov inequality. Both are written inside a section restricted to $n\ge n_0$. Also, (ii) does not mention the case $s_0>K$ (Reading 5.2), although (iii) does. Evidence: The arguments for (ii) and (iii) are purely deterministic. They hold whenever $S_0\in\Omega$, for any $n$. For $s_0>K$, $\pi(S_0):=0$, so (ii) reads $|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1$, which is trivial. A one-line remark fills this. Verdict: verified (the content is correct; the scope is not stated).

**F5** — Location: §6, Step 0 and eq. (tail). Severity: exposition. Claim: H-T02 gives $\lim_L\limsup_n\sup_mP_0(\Theta_{n,m}>L)=0$, which is tightness in the limsup sense. The proof's convention (§1) is "$X_n/a_n$ is tight". The step between the two is not written out. Evidence: $\Pi(|S|>m_n\mid y)\le1$ always and $a_n=n^{-1/2}>0$. So for the finitely many early $n$, $X_n/a_n\le n^{1/2}$ is bounded, and the two notions coincide. The same remark covers every "for $n\ge n_0$" in an $O_P$ argument. Verdict: verified.

**F6** — Location: §6 (iii), "bounded convergence gives $E_0[1-\pi(S_0)]\to0$". Severity: exposition. Claim: The fact needed is that uniformly bounded variables converging to 0 in probability have expectations tending to 0. The variables live on $n$-dependent models, because the design varies with $n$. That makes it a direct bound rather than the a.s. bounded convergence theorem. Evidence: For any $\epsilon>0$, $E_0[1-\pi(S_0)]\le\epsilon+P_0(1-\pi(S_0)>\epsilon)\to\epsilon$. The claim is correct. Verdict: verified.

**F7** — Location: §3, Lemma 7(a), "(This is the form of Laurent and Massart's Lemma 1; we prove it.)" Severity: exposition. Claim: I have not seen this citation in a source, so it is unverified. The proof does not rely on it: it proves both tail bounds itself. Evidence: I checked the self-contained proof algebraically: the choice $\lambda=s/(a+2s)$ gives exponent exactly $-s^2$, and the lower tail gives $-t^2/(4d)$. Exact $\chi^2$ tails over a grid of $(d,x)$ gave 0 violations. Verdict: verified (the attribution itself is unverified).

**F8** — Location: §1, "Asymptotic conventions" ($n_0$ "depending only on $(s_0,A,\varphi_0,\sigma_\star^2,M)$"), and §4 ("By (mn), $\delta_n\log n\to0$"). Severity: exposition. Claim: $\delta_n$, $\theta_n$, $\epsilon_n$ and $q_n$ depend on $m_n$, and so on $p_n$. The proof does not say explicitly why the thresholds $\delta_n\le\frac12$, $q_n\le\frac12$ and $q_n\le\sqrt{eC_A}\,r_n$ can be taken uniformly in the design sequence. Evidence: $\delta_n$ is increasing in $m_n$, and (mn) gives $m_n\le C_m\log n$, where $C_m$ depends only on $(s_0,A)$. Replacing $m_n$ by $C_m\log n$ gives deterministic dominating sequences that depend only on the listed constants, so the claim holds. Even without this, a $p_n$-dependent $n_0$ would not affect any asymptotic conclusion. Under BM-∞, the extra threshold where $M_n\ge M_*$ is likewise harmless. Verdict: verified.

## Overall verdict

**Verified.** Every step of PROOF_v1 is correct and justified, and the theorem in STATEMENT.md follows from its hypotheses (G, R, SE, H-T02, and BM-C or BM-∞, with (iv) needing no beta-min). The constants $j_*$, $C_*$, $L_*$, $M_*$ and $C_A$ do what is claimed. The good event has probability at least $1-5/n$, and every union bound, expectation and $O_{P_0}$ step is valid. The 8 findings are all exposition-level; F4 and F5 are the most worth a one-line fix.
