# R2 — Local regressions give the variance clause (W3-READER bridge leg, 2026-11-16)

Status: **PROVED (by this seat, unchecked)**. Population form passed the S1 fidelity read as part of B6.3
(`reviews/S1_fidelity_sol.md`, "B6.3 passes"); the sample form below is the analogue invoked by B7.3, written out here.

## R2.1 (population; bridge B6.3 of Theorem 6)
**Setting.** $W\sim N_p(0,\Sigma_n)$ with $\Sigma_n$ a correlation matrix (unit diagonal). $Q\supseteq S_0$ deterministic,
$\lambda_{\min}(\Sigma_{n,Q\cup\{l\}})\ge c>0$ for every $l\in[p]$. For $l\in[p]$ and $B\subseteq Q\setminus\{l\}$,
$\beta_{B,l}:=\Sigma_{n,BB}^{-1}\Sigma_{n,Bl}$, $\bar\beta_{B,l}$ its zero-padding to $\mathbb R^Q$, and
$v_B(l):=\operatorname{Var}(W_l\mid W_B)=\operatorname{Var}(W_l-W_B^\top\beta_{B,l})$.

**Claim.** If $T\subseteq Q\setminus\{l\}$, $A\subseteq T$ and $\|\bar\beta_{T,l}-\bar\beta_{A,l}\|_1\le L$, then
$$v_A(l)\le\Big(1+\frac{L^2}{c}\Big)v_T(l).$$
Hence (A6) of Theorem 6 (deterministic $N_l$ with $|N_l|\le\nu_n=o(\log n)$; $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$
for all lattice $T\not\ni l$; $L_n\to0$, $L_n^2\log(|Q|+1)=o(\log n)$) together with (A5) implies (D-loc^b)
(`W3-RM2/STATEMENT.md:201-202` = RM (D-loc), `W3-RM/STATEMENT.md:154-156`, with the polynomial-size rate), with
$\eta_n:=L_n^2/c\to0$, uniformly in $(T,l)$.

*Proof.* Put $d:=\bar\beta_{T,l}-\bar\beta_{A,l}$, supported in $T$. The residual $e_T:=W_l-W_T^\top\beta_{T,l}$ is
uncorrelated with $W_T$ (normal equations). Since $W_l-W_A^\top\beta_{A,l}=e_T+W_T^\top d_T$,
$v_A(l)=v_T(l)+d_T^\top\Sigma_{n,TT}d_T$. Unit diagonal and positive semidefiniteness give $|\Sigma_{ik}|\le1$, so
$d_T^\top\Sigma_{n,TT}d_T\le\sum_{i,k}|d_i||d_k|\le\|d\|_1^2\le L^2$. Finally
$v_T(l)=\big(\Sigma^{-1}_{n,T\cup\{l\}}\big)_{ll}^{-1}\ge\lambda_{\min}(\Sigma_{n,T\cup\{l\}})\ge\lambda_{\min}(\Sigma_{n,Q\cup\{l\}})\ge c$
(Schur complement; Cauchy interlacing for $T\cup\{l\}\subseteq Q\cup\{l\}$). So $v_A(l)\le v_T(l)+L^2\le v_T(l)(1+L^2/c)$. ∎

*Remark.* RM's (D-loc) allows a bounded $L_n$ when $|Q|$ is polylogarithmic; there the variance clause is a separate
hypothesis. The reader version asks $L_n\to0$ and gives that case up (S1: "correctly stronger than the master's
polylogarithmic alternative").

## R2.2 (sample; used in B7.3 of Theorem 7)
**Setting.** Fixed standardised design ($\|x_j\|^2=n-1$), $\lambda_{\min}(\hat R_{Q\cup\{l\}})\ge\varphi_0^2$ for every $l$.
$\hat\beta_{B,l}:=(X_B^\top X_B)^{-1}X_B^\top x_l$, zero-padded.

**Claim.** If $A\subseteq T\subseteq Q\setminus\{l\}$ and $\|\bar{\hat\beta}_{T,l}-\bar{\hat\beta}_{A,l}\|_1\le L$, then
$\|(I-P_A)x_l\|^2\le(1+L^2/\varphi_0^2)\|(I-P_T)x_l\|^2$.

*Proof.* As R2.1 with the inner product $\langle u,v\rangle/(n-1)$: $(I-P_T)x_l\perp X_T$, so
$\|(I-P_A)x_l\|^2\le\|x_l-X_A\hat\beta_{A,l}\|^2=\|(I-P_T)x_l\|^2+\|X_Td\|^2$ (in fact equality: $X_A\hat\beta_{A,l}=P_Ax_l$).
$\|X_Td\|^2=(n-1)d^\top\hat R_{TT}d\le(n-1)\|d\|_1^2\le(n-1)L^2$ since $|\hat R_{ik}|\le1$; and
$\|(I-P_T)x_l\|^2\ge(n-1)\lambda_{\min}(\hat R_{T\cup\{l\}})\ge(n-1)\varphi_0^2$. ∎
This is the statement recorded at `W3-RM2/STATEMENT.md:164` ("under (FL-Q) the second inequality follows from the first
with $\eta_n=L_n^2/\varphi_0^2$ whenever $L_n\to0$"), so B7.3's use is covered by the master's own text; R2.2 is the
written proof for the line check.
