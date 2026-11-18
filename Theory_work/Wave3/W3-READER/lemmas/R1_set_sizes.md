# R1 — Set-size and elementary bridges (W3-READER bridge leg, 2026-11-16)

Status: **PROVED-CHECKED** (registry `W3-READER:R1@1.0.4`, council R3). The arithmetic of B1.2, B1.3, B2.1, B4.1, B6.1 was verified analytically
by the S1 fidelity read (`reviews/S1_fidelity_sol.md`, "NEW arithmetic bridges"); this file writes the proofs out for the
line check. Numeric spot check: LOG 2026-11-15 (grid $A\in[1,20]$, $s_0\le39$, $n\in[3,10^{15}]$, 0 violations).

Notation as `READER_VERSIONS.md` / `NOTATION.md`: $n\ge3$ (so $t:=\log n\ge\log3>1$), $A\ge1$, $s:=s_0\ge1$,
$j_0:=\lceil(2A+1)s\rceil+1$, $\ell_2:=1/\log2<1.4427$, $d:=1/\log(3/2)<2.4664$.

## B1.1 (bounded coefficients ⇒ energy)
**Claim.** If $|\theta^*_j|\le\bar\theta$ for all $j$ and $|S_0|=s$, then $\|X\theta^*\|^2\le n\,s^2\bar\theta^2$.
*Proof.* $\|X\theta^*\|\le\sum_{j\in S_0}|\theta^*_j|\|x_j\|\le s\bar\theta\sqrt{n-1}$. ∎ (Same remark at
`Theory_work/Wave3/W3-POST/STATEMENT.md:57`.)

## B1.2 (unanchored small-set floor ⇒ (F_λ))
**Claim.** $s+j_0\le(2A+2)s+2$. Hence a floor on every $S$ with $|S|\le(2A+2)s+2$ covers every $S_0\cup J$, $J\subseteq[p]\setminus S_0$, $|J|\le j_0$, which is (F_λ) = SE_λ($j_0$) (`W3-POST/STATEMENT.md:68-70`).
*Proof.* $\lceil x\rceil\le x+1$ gives $j_0\le(2A+1)s+2$. ∎ (Valid for non-integer $A$.)

## B1.3 (log-size floor ⇒ (F_w))
**Claim.** For $s\le K$: $s+m^\sharp_n\le3(A+1)(s+1)\log n$. Hence (A5) of Theorem 1 covers every $S_0\cup J$ with
$|J|\le m^\sharp_n$, which is (F_w) = SE_w($m^\sharp_n$; $g_0$) (`W3-POST/STATEMENT.md:71-73`).
*Input.* $m^\sharp_n(\omega)\le\min\{K,\ s+\lceil(\log\binom ps+\tfrac{s+1}2\log n+\omega)/\log2\rceil\}$ for $s\ge1$,
$\omega\ge0$, $s\le K$ ([T03R] E2(ii), restated at `W3-POST/STATEMENT.md:38-39`; inside `SOP:TH09@1.0.2`, status
"PROVED-CHECKED (T03♯ only: …)" (main 6cd699dd) [REG-6cd6]), with $m^\sharp_n:=m^\sharp_n(\tfrac12\log n)$.
*Proof.* $\binom ps\le p^s\le n^{As}$, so $\log\binom ps\le Ast$. Then
$s+m^\sharp_n\le 2s+1+\ell_2(As+\tfrac{s+1}2+\tfrac12)t=2s+1+\ell_2(As+\tfrac s2+1)t$. Since $t>1$,
$2s+1<(2s+1)t$, so $s+m^\sharp_n<[(2s+1)+1.45(As+\tfrac s2+1)]t=[1.45As+2.725s+2.45]t$. Finally
$3(A+1)(s+1)-(1.45As+2.725s+2.45)=1.55As+3A+0.275s+0.55>0$. ∎

## B2.1 (population floor on $O(\log n)$ sets ⇒ LSF)
**Claim.** With $\bar m_n:=\lceil[s(A\log n+\log2)+\log2+\tfrac{s+2}2\log n]/\log\tfrac32\rceil$ and
$\bar k_n:=\min\{p,\ s+\max(j_0,\bar m_n)\}$ (`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:20-21`):
$\bar k_n\le5(A+1)(s+1)\log n$ and $\min(p,s+j_0)\le5(A+1)(s+1)\log n$. Hence a population floor
$\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ on every $|S|\le5(A+1)(s+1)\log n$ gives LSF (i) and (ii) with
$\psi_n:=\varphi^2$ (`L1_POST.md:23-25`; (ii) needs $\psi_n\sqrt n/(\log n)^{3/2}\to\infty$, true for a constant).
*Proof.* The ceiling gives $s+\bar m_n\le(s+1)+d[(As+\tfrac s2+1)t+(s+1)\log2]=d(As+\tfrac s2+1)t+(1+d\log2)(s+1)$.
Since $t\ge\log3$, $(1+d\log2)(s+1)\le\frac{1+d\log2}{\log3}(s+1)t$, and exactly
$\frac{1+d\log2}{\log3}=\frac{\log\frac32+\log2}{\log\frac32\,\log3}=\frac1{\log\frac32}=d$. Hence
$s+\bar m_n\le d\,(As+\tfrac32s+2)\,t<(2.4664As+3.6996s+4.9327)\,t$. Then
$5(A+1)(s+1)-(2.4664As+3.6996s+4.9327)=2.5336As+5A+1.3004s+0.0673>0$ for $A,s\ge1$. And
$s+j_0\le(2A+2)s+2\le[(2A+2)s+2]t$, with $5(A+1)(s+1)-(2A+2)s-2=3(A+1)s+5A+3>0$. ∎

## B4.1 (omitted-variables row)
**Claim.** For $s\le K$: $s+\max(j_0,m^\sharp_n)\le3(A+1)(s+1)\log n$ (here $p=|\mathcal C|$ and $s=|S^{\mathcal C}_0|$).
*Proof.* B1.3 for the $m^\sharp_n$ branch; for the $j_0$ branch, $s+j_0\le(2A+2)s+2<[(2A+2)s+2]t\le3(A+1)(s+1)t$. ∎
(Covers `W3-MISR:Cor-G(b)`'s floor range $|T|\le s+\max(j_0,m^\sharp_n)$, `W3-MISR/STATEMENT.md:171-172`.)

## B6.1 (main-theorem floors)
**Claim.** $16+s\le5(A+1)(s+1)\log n$ for $n\ge3$, $A,s\ge1$. Hence Theorem 6's (A5) gives (FL-R) on small sets
($|S|\le16+s_0$, `W3-RM/STATEMENT.md:134`) and, with B2.1, (T1-R) = LSF.
*Proof.* $5(A+1)(s+1)\log3\ge10(s+1)\cdot1.0986>10.98s+10.98>s+16$ for $s\ge1$. ∎ (The floor on $Q\cup\{l\}$ is assumed
separately in (A5).)

## B3.2 (Gaussian null columns ⇒ (W-sph))
**Claim.** If the raw columns outside $S_0$ have i.i.d. $N(0,1)$ entries independent of $(X^{\mathrm r}_{S_0},\varepsilon)$,
$s_0$ is fixed and $p\le n^A$, then (W-sph) holds conditionally on $(X_{S_0},\theta^*)$ (`W3-PSHARP/STATEMENT.md:56-60`).
*Proof.* Centring and scaling an i.i.d. Gaussian vector gives a direction uniform on the unit sphere of $\mathbf 1^\perp$,
independently across columns (the example at :59-60 of the claim). With $N_n\le p\le n^A$: $(\log N_n)^2\le A^2(\log n)^2=o(n)$
and $(r_0+1)\log N_n\le(s_0+1)A\log n=o(n)$. ∎
