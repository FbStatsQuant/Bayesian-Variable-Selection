# STATEMENT — T03 (A2): selection, screening, PIPs and the global HPM

Source: `Theory_architecture_v3/theorems/T03_A2_selection_consistency.md` with `00_COMMON.md` (SMC-BVS v3.0, method SHA-256 93043758…c44b8019c). Step-1 outcome: **(a) correct as stated**. No hypothesis or conclusion is changed. The readings adopted are listed in §5. The one unproved v3 result used is T02(i), as an explicit hypothesis (H-T02), as the brief allows (T03's file lists T01, T02 as "builds on").

## 1. Data and target (00_COMMON §1; METHODOLOGY_v3 §5)

- Raw data $(X^r,y^r)$, $X^r\in\mathbb R^{n\times p}$, $n\ge3$, $p\ge1$, no constant column, $y^r$ not constant. $C=I_n-\mathbf 1\mathbf 1^\top/n$; $D_x$ = diagonal matrix of the raw column sample SDs (denominator $n-1$); $s_y^2=\|Cy^r\|^2/(n-1)$. Standardised data $X=CX^rD_x^{-1}$, $y=Cy^r/s_y$, so $\|x_j\|^2=\|y\|^2=n-1$. $U\in\mathbb R^{n\times(n-1)}$ with $U^\top U=I_{n-1}$, $UU^\top=C$.
- $K=\min(p,\lfloor n/2\rfloor)$, $\Omega=\{S\subseteq[p]:|S|\le K\}$. For $S\subseteq[p]$: $G_S=X_S^\top X_S$, $R_S=G_S/(n-1)$, $z_S=X_S^\top y$, $H_S=(n+1)G_S+I$, $D_S=\det H_S/\det(G_S+I)$, $Q_S=y^\top y-n z_S^\top H_S^{-1}z_S$; $a_0=b_0=0.01$, $\nu=a_0+n/2$ ($D_\emptyset=1$, $Q_\emptyset=y^\top y$).
- $m(S)=\dfrac{(2b_0)^{a_0}\Gamma(\nu)}{\pi^{n/2}\Gamma(a_0)}D_S^{-1/2}(2b_0+Q_S)^{-\nu}$; $w(k)=\tfrac12\big/\binom{2p-1}{k}$ ($0\le k\le p$); $W_K=\sum_{k\le K}\binom pk w(k)$; $\varpi(S)=w(|S|)/W_K$ for $S\in\Omega$.
- $F(S)=\log[\varpi(S)m(S)]$, $Z=\sum_{S\in\Omega}\varpi(S)m(S)$, $\pi(S)=e^{F(S)}/Z$ on $\Omega$; $\Pi(\mathcal A\mid y)=\sum_{S\in\mathcal A\cap\Omega}\pi(S)$.
- $\mathrm{PIP}_j=\pi(\{S: j\in S\})$; $\mathrm{MPM}=\{j:\mathrm{PIP}_j>\tfrac12\}$; global HPM $S^\dagger=\arg\max_{\Omega}F$, ties broken by smallest size, then lexicographically.
- Statistical model: $y^r=\alpha^\star\mathbf 1+X^r\beta^\star+\varepsilon$; $\mu=CX^r\beta^\star=X\theta^\star$ with $\theta^\star=D_x\beta^\star$; $S_0=\operatorname{supp}\beta^\star$, $s_0=|S_0|$. $P_0$, $E_0$ refer to $\varepsilon$ (the design is fixed).
- $r_n=\sqrt{\log n/n}$. $m_n(\omega)=\lceil(s_0\log(2p)+(s_0+1)(\log n)/2+\omega)/\log2\rceil$, $m_n:=m_n(\tfrac12\log n)$.
- Regime R1: $n\to\infty$, $s_0$ fixed, $p=p_n\le n^A$; design, $\beta^\star$, $S_0$ may vary with $n$.

## 2. Hypotheses

- **G.** Fixed design; $\varepsilon\sim N_n(0,\sigma_\star^2I_n)$, $\sigma_\star^2>0$ fixed.
- **R.** $s_0$ fixed; $p\le n^A$ with fixed $A\ge1$; $\|\mu\|^2/n\le M$ (fixed $M$); $\lambda_{\min}(R_{S_0})\ge\varphi_0^2>0$ (fixed $\varphi_0$); eventually $s_0\le K$.
- **SE.** $\lambda_{\min}(R_T)\ge\varphi_0^2$ for every nonempty $T\subseteq[p]$ with $|T|\le\min(p,m_n+s_0)$.
- **Constants.** $j_*=\lceil(2A+1)s_0\rceil+1$; $C_*=2s_0+3[Aj_*+s_0+\log(j_*+1)+1]$; $L_*=\max\{4C_*,\,32[s_0(A+1)+2]\}$; $M_*=2L_*+1$.
- **BM-C.** $\min_{j\in S_0}\theta^{\star2}_j\ge M_*\sigma_\star^2\log n/(n\varphi_0^2)$.
- **BM-∞.** The same inequality with a sequence $M_n\to\infty$ in place of $M_*$.
- **H-T02 (= T02(i), unproved v3 conjecture, used as hypothesis).** Under G and R, for each deterministic integer sequence $m=m(n)$,
  $\Pi(|S|>m\mid y)\le2^{-m}(2p)^{s_0}(n+1)^{s_0/2}\sqrt n\,\Theta_{n,m}$, with $\lim_{L\to\infty}\limsup_n\sup_mP_0(\Theta_{n,m}>L)=0$.

Convention: a minimum over the empty set is $+\infty$ (so BM-C and BM-∞ hold when $s_0=0$).

## 3. Conclusions (in R1)

Under G, R, SE, H-T02 and BM-C (or BM-∞):

- **(i)** $1-\pi(S_0)=O_{P_0}(r_n)$.
- **(ii)** $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0)$ for every data set (deterministic); and $P_0(\mathrm{MPM}=S_0)\to1$.
- **(iii)** $P_0(S^\dagger\ne S_0)\le2E_0[1-\pi(S_0)]\to0$; on the event $\{\pi(S_0)>\tfrac12\}$, $S_0$ is the strict global maximiser of $F$ on $\Omega$ (the tie rule is not invoked).

Under G, R, SE and H-T02 only (no beta-min):

- **(iv)** With $J_n=\{j\in S_0:\theta^{\star2}_j\ge M_*\sigma_\star^2\log n/(n\varphi_0^2)\}$: $\Pi(\{S:S\not\supseteq J_n\}\mid y)=O_{P_0}(r_n)$, and $\min_{j\in J_n}\mathrm{PIP}_j\to1$ in $P_0$-probability (with $1-\min_{j\in J_n}\mathrm{PIP}_j=O_{P_0}(r_n)$; the minimum over $\emptyset$ is $1$).

Deterministic remarks:

- **(v)** If $s_0=0$, BM-C and BM-∞ hold vacuously. For every $c>0$, replacing $(\theta^\star,\sigma_\star^2)$ by $(\theta^\star/c,\sigma_\star^2/c^2)$ (in particular $c=s_y$) leaves the BM-C and BM-∞ inequalities and the set $J_n$ unchanged.

## 4. Not claimed

The theorem file's sentences "No frequentist $O(r_n)$ selection-error rate follows from the posterior $O_{P_0}(r_n)$ rate" and "$M_*$ is conservative, not sharp; the sharp general-design constant is open" are interpretive remarks. They are not part of the claim and are not proved.

## 5. Readings adopted (not changes)

1. $O_{P_0}(a_n)$ means $X_n/a_n$ is tight under $P_0$; "$\to$" for random quantities means convergence in $P_0$-probability.
2. In (i)–(iii), $\pi(S_0)$ is defined once $s_0\le K$ (eventually, by R); before that, $\pi(S_0):=0$ and every claim holds trivially or is asymptotic.
3. "The PIPs of $J_n$ tend uniformly to one" is read as $\min_{j\in J_n}\mathrm{PIP}_j\to1$ in probability.
4. (v) is read as the scale invariance stated in §3; $\varphi_0$, $M_*$ and $n$ do not depend on the scale of $y$.
5. Hypotheses that only matter for other theorems (DX, GL, …) are not used.
