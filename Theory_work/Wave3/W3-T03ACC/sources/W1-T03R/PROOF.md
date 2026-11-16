# W1-T03R — PROOF.md: exact BB(1,p) size tail, sharpened T02, restated T03

Run W1-T03R, 2026-11-02. Notation of `Docs/Theory/theorems/00_COMMON.md`. Status words are used per the campaign protocol and every status is a **candidate pending cross-family review**.

**References to locked proofs (cited by label, unchanged unless said otherwise).**
- **[P1]** `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` (T01, T02). Labels used: `lem:spec`, `lem:prior`, `lem:chi`, `lem:num`, `lem:den`, `thm:T01iii`, `thm:Ta`, `thm:T02i`, `lem:good`, `lem:onG`, `lem:one`, `thm:T02ii`.
- **[P3]** `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (T03). Labels used: `lem:red`, `lem:smoother`, `cor:diff`, `lem:det`, `lem:prior`, `lem:signal`, `lem:chi`, `lem:Gprob`, `lem:ongood`, `lem:onesup`, `prop:sup`, `lem:SvsSp`, `lem:signalgain`, `lem:assemble`, "Step 0", "Step 1", paragraphs (i)–(v) of §"Proof of the theorem".

Throughout: $N=n-1$, $K=\min(p,\lfloor n/2\rfloor)$, $w(k)=\tfrac12/\binom{2p-1}{k}$, $\varpi(S)=w(|S|)/W_K$, $r_n=\sqrt{\log n/n}$, $m_n(\omega)=\lceil(s_0\log(2p)+(s_0+1)(\log n)/2+\omega)/\log 2\rceil$ (00_COMMON). We assume $p\ge2$ (for $p=1$ every statement below is trivial or void).

---

## 1. The exact BB(1,p) size tail

Put $q_k:=\binom pk w(k)$ ($0\le k\le p$) and, for every integer $m$ and $0\le s_0\le K$,
$$R_m:=\frac{\varpi(\{S\in\Omega:|S|>m\})}{\varpi(S_0)}=\sum_{k=m+1}^{K}\frac{q_k}{w(s_0)}\qquad(\text{empty sum}=0;\ W_K\text{ cancels}).$$
$R_m$ is a data-free number (it depends on $p$, $s_0$, $K$, $m$ only), and $R_m=0$ for $m\ge K$.

### Lemma E1 (exact tail; PROVED)
Let $\rho_i:=\dfrac{p-i}{2p-1-i}$ for $0\le i\le p-1$.

**(a)** $\rho_i=\tfrac12\Big(1-\dfrac{i-1}{2p-1-i}\Big)$, and for $s_0\le k\le p$: $\ q_k/w(s_0)=\binom p{s_0}\prod_{i=s_0}^{k-1}\rho_i$.

**(b)** For every integer $m\ge s_0$:
$$R_m\le\binom p{s_0}\,2^{-(m-s_0)}\,e^{-\gamma_m},\qquad \gamma_m:=\frac{m(m-1)-(s_0-1)(s_0-2)}{4(p-1)} .$$

**(c)** If $s_0\ge1$ and $s_0\le m\le K-1$:
$$R_m\ \ge\ \frac{q_{m+1}}{w(s_0)}\ \ge\ \binom p{s_0}\,2^{-(m+1-s_0)}\exp\Big\{-\frac{m(m-1)-(s_0-1)(s_0-2)}{4(p-m)}\Big\}.$$

**(d)** (comparison with the locked bound) The locked proof of T02(i) bounds the same ratio by $4(2p)^{s_0}2^{-m}$ ([P1] `lem:prior`(c),(d)). For $m\ge s_0\ge 1$, (b) improves this by the factor at least $4\,s_0!\,e^{\gamma_m}$, since $\binom p{s_0}2^{s_0}\le(2p)^{s_0}/s_0!$.

*Proof.* (a) $2(p-i)=(2p-1-i)-(i-1)$ gives the first identity. $q_{s_0}/w(s_0)=\binom p{s_0}$, and $q_{i+1}/q_i=\frac{p-i}{i+1}\cdot\frac{i+1}{2p-1-i}=\rho_i$ ([P1] `lem:prior`(b) and the proof of (c)); multiply for $i=s_0,\dots,k-1$.

(b) First, $\rho_i\le\frac12e^{-(i-1)/(2p-2)}$ for $0\le i\le p-1$. For $i\ge1$ put $x=(i-1)/(2p-1-i)\in[0,1)$; since $2p-1-i\le 2p-2$, $x\ge(i-1)/(2p-2)$, and $\rho_i=\frac12(1-x)\le\frac12e^{-x}$. For $i=0$, $\rho_0=\frac12(1+\frac1{2p-1})\le\frac12e^{1/(2p-1)}\le\frac12e^{1/(2p-2)}$. Next, $\sum_{i=s_0}^{k-1}(i-1)=\sum_{t=s_0-1}^{k-2}t=\frac12[(k-1)(k-2)-(s_0-1)(s_0-2)]$ (valid also for $s_0=0$). Hence by (a), for $m+1\le k\le K$ (so $k>s_0$),
$$\frac{q_k}{w(s_0)}\le\binom p{s_0}2^{-(k-s_0)}\exp\Big\{-\frac{(k-1)(k-2)-(s_0-1)(s_0-2)}{4(p-1)}\Big\}\le\binom p{s_0}2^{-(k-s_0)}e^{-\gamma_m},$$
because $t\mapsto t(t-1)$ is nondecreasing on the integers $t\ge0$ and $k-1\ge m\ge0$. Summing, $\sum_{k\ge m+1}2^{-(k-s_0)}=2^{-(m-s_0)}$.

(c) $R_m\ge q_{m+1}/w(s_0)$ because $m+1\le K$ and all terms are positive. For $1\le i\le m\ (\le p-1)$, $2\rho_i=\frac{2p-2i}{2p-1-i}$ and $\log(2\rho_i)=-\log\big(1+\frac{i-1}{2(p-i)}\big)\ge-\frac{i-1}{2(p-i)}\ge-\frac{i-1}{2(p-m)}$. Since $s_0\ge1$ every index in $\prod_{i=s_0}^m$ is $\ge1$; sum $\sum_{i=s_0}^m(i-1)=\frac12[m(m-1)-(s_0-1)(s_0-2)]$ and use (a) with $k=m+1$.

(d) $\binom p{s_0}\le p^{s_0}/s_0!$, so $\binom p{s_0}2^{s_0-m}e^{-\gamma_m}\le(2p)^{s_0}2^{-m}e^{-\gamma_m}/s_0!$. For $m\ge s_0\ge1$, $m(m-1)\ge s_0(s_0-1)\ge(s_0-1)(s_0-2)$, so $\gamma_m\ge0$. $\square$

**Reading.** By (a) the size marginal of BB(1,p) is geometric with ratio $\rho_i\approx\frac12$; the per-*model* ratio $w(k+1)/w(k)=(k+1)/(2p-1-k)\approx k/(2p)$ is cancelled by the multiplicity $\binom p{k+1}/\binom pk=(p-k)/(k+1)$. The exact tail therefore improves the locked one only by the factor $4\,s_0!\,e^{\gamma_m}$ ($\approx 36$ bits at $s_0=14$, plus $m^2/(4p)$ nats), not by a factor $p^{-(m-s_0)}$.

### Definition (new size cutoff)
For $s_0\le K$ and real $\omega$:
$$m^\sharp_n(\omega):=\min\{m\in\mathbb Z:\ m\ge s_0,\ R_m\le n^{-(s_0+1)/2}e^{-\omega}\},\qquad m^\sharp_n:=m^\sharp_n(\tfrac12\log n).$$
The minimum exists and $m^\sharp_n(\omega)\le K$, because $R_K=0$. It is computable exactly (`scripts/tail_bound.py`).

### Lemma E2 (location of $m^\sharp_n$; PROVED)
Assume $s_0\le K$, $\omega\ge0$, and $s_0\ge1$ in (ii)–(iii) ($n\ge5$ if $s_0=0$ in (i)).

**(i)** $s_0\le m^\sharp_n(\omega)\le\min\{K,\ m_n(\omega)\}$.

**(ii)** $m^\sharp_n(\omega)\le\min\Big\{K,\ s_0+\Big\lceil\dfrac{\log\binom p{s_0}+\frac{s_0+1}2\log n+\omega}{\log2}\Big\rceil\Big\}$.

**(iii)** If $m^\sharp:=m^\sharp_n(\omega)\le K-1$, then
$$m^\sharp-s_0\ \ge\ \frac{\log\binom p{s_0}+\frac{s_0+1}2\log n+\omega}{\log2}-1-\frac{m^\sharp(m^\sharp-1)}{4(p-m^\sharp)\log2}.$$

*Proof.* (i) $m^\sharp\ge s_0$ by definition and $m^\sharp\le K$ was noted. Let $m=m_n(\omega)$. Since $\omega\ge0$ and $\log(2p)\ge\log2$, $m\ge s_0$. By definition $2^{-m}\le(2p)^{-s_0}n^{-(s_0+1)/2}e^{-\omega}$. If $s_0\ge1$: $\gamma_m\ge0$ (E1(d)), so E1(b) and $\binom p{s_0}2^{s_0}\le(2p)^{s_0}$ give $R_m\le(2p)^{s_0}2^{-m}\le n^{-(s_0+1)/2}e^{-\omega}$, hence $m^\sharp\le m$. If $s_0=0$ and $n\ge5$: $m=\lceil(\frac12\log n+\omega)/\log2\rceil\ge2$, so $\gamma_m=[m(m-1)-2]/(4(p-1))\ge0$ and E1(b) gives $R_m\le2^{-m}\le n^{-1/2}e^{-\omega}$; again $m^\sharp\le m$.
(ii) Let $m$ be the right-hand side (when it is $<K$). Then $2^{-(m-s_0)}\le\binom p{s_0}^{-1}n^{-(s_0+1)/2}e^{-\omega}$ and E1(b) with $\gamma_m\ge0$ gives $R_m\le n^{-(s_0+1)/2}e^{-\omega}$.
(iii) At $m=m^\sharp\le K-1$ combine E1(c) with $R_m\le n^{-(s_0+1)/2}e^{-\omega}$, take logarithms and drop $(s_0-1)(s_0-2)\ge0$. $\square$

### Proposition E3 (the exact-tail route cannot give $m_n=s_0+O(s_0\log n/\log p)$; PROVED)
In R1 with $s_0\ge1$ fixed and $n^{a}\le p_n\le n^A$ for some fixed $0<a\le A$: either $m^\sharp_n=K$ or
$$m^\sharp_n-s_0\ \ge\ \frac{s_0\log(p/s_0)+\frac{s_0+2}2\log n}{\log2}-1-o(1)\ \ge\ \frac{(s_0a+\frac{s_0+2}{2})\log n-s_0\log s_0}{\log 2}-1-o(1).$$
Since $s_0\log n/\log p\le s_0/a=O(1)$, the brief's target scale $m_n=s_0+O(s_0\log n/\log p)$ is not reached by any bound of the form "Markov numerator over $S_0$-denominator" (the form of the locked T02(i) and of Theorem T02(i♯) below): such a bound is at least $R_m(n+1)^{s_0/2}\sqrt n\cdot c$ with $R_m$ two-sided-controlled by E1.

*Proof.* E2(iii) with $\omega=\frac12\log n$, $\binom p{s_0}\ge(p/s_0)^{s_0}$, and $m^\sharp\le m_n(\tfrac12\log n)=O(\log n)$ (E2(i), $p\le n^A$) so $m^{\sharp2}/(p-m^\sharp)\to0$ because $p\ge n^a$. $\square$

*Remark (not a claim about the true posterior).* E3 is a barrier for the proof technique. Whether the *true* posterior needs $m_n-s_0\asymp s_0\log p$ under G and R is **OPEN**. Proposition D below shows that *some* growth, $m_n\ge(\tfrac12-o(1))\log_2 n$, is necessary in general.

---

## 2. Theorem T02(i♯): sharpened size tail with explicit constants (PROVED; candidate)

Constants (as in [P1] §1 and `lem:den`): $b_-=b_0\sigma_*^2/2$, $b_+=b_0(2(\sigma_*^2+M)+1)$, $\kappa=(b_+/b_-)^{0.51}$, $\mathcal B_n=\{b_-\le b_0s_y^2\le b_+\}$, $c_{\rm IG}=\min_{v\in[\sigma_*^2,2\sigma_*^2]}\mathrm{IG}(v;0.51,b_+)$, $C_\Lambda=\frac1{\sqrt2}+\frac12+\mathbf 1\{s_0\ge1\}\frac{(1+\frac1{2\varphi_0^2})(M+\sigma_*^2)}{2\sigma_*^2}$, and
$$c^\sharp:=\kappa^2/(c_{\rm IG}\sigma_*^2).$$

**Theorem T02(i♯).** Assume G and R, and let $n$ be such that $s_0\le K$. For every integer $m$ define $\Theta^\sharp_{n,m}\ge0$ by
$$\Pi(|S|>m\mid y)=R_m\,(n+1)^{s_0/2}\sqrt n\;\Theta^\sharp_{n,m}\quad\text{if }R_m>0,\qquad\Theta^\sharp_{n,m}:=0\ \text{ if }R_m=0 .$$
Then for every $L>c^{\sharp2}$,
$$\sup_m P_0(\Theta^\sharp_{n,m}>L)\ \le\ \frac{8+24M/\sigma_*^2}{n-1}+\frac1{\sqrt L}+\frac{C_\Lambda}{\log(\sqrt L/c^\sharp)} .$$
Consequently $\lim_{L\to\infty}\limsup_n\sup_mP_0(\Theta^\sharp_{n,m}>L)=0$, and for every deterministic real sequence $\omega_n$,
$$\Pi(|S|>m^\sharp_n(\omega_n)\mid y)\le(1+\tfrac1n)^{s_0/2}e^{-\omega_n}\,\Theta^\sharp_{n,m^\sharp_n(\omega_n)}=O_{P_0}(e^{-\omega_n}).$$
(When $R_m=0$, $\{S\in\Omega:|S|>m\}=\emptyset$ because $\varpi>0$ on $\Omega$, so $\Pi(|S|>m\mid y)=0$ and the definition is consistent.) The inequality is non-asymptotic: it holds at every $n$ with $s_0\le K$.

**Changed step relative to [P1] `thm:T02i`:** the prior factor. [P1] bounded $\varpi(|S|>m)\le2^{1-m}$ (`lem:prior`(c)) and $\varpi(S_0)\ge\frac12(2p)^{-s_0}$ (`lem:prior`(d)) separately; here the ratio $R_m$ is kept exactly. For this we need the denominator bound of [P1] `lem:den` *before* the factor $\varpi(S_0)$ is bounded; we restate it.

**Lemma den′** (= [P1] `lem:den` without its last factor). Under G, R and $s_0\le K$, with $\Lambda_n$ as in [P1] `lem:den`,
$$\frac{m^c_{b_+}(S_0)}{f_0(y_c)}\ \ge\ (n+1)^{-s_0/2}\,c_{\rm IG}\,\sigma_*^2\,n^{-1/2}e^{-\Lambda_n},\qquad E_0\Lambda_n\le C_\Lambda .$$
*Proof.* This is exactly what the paragraphs "Bound on $Q^c_{S_0}$", "Integral representation", "Lower bound on the exponent" and the first two sentences of "Assembling" in the proof of [P1] `lem:den` establish: restricting the $v$-integral to $[\sigma_*^2,\sigma_*^2(1+n^{-1/2})]$ (length $\sigma_*^2n^{-1/2}$, IG density $\ge c_{\rm IG}$, exponent $\ge-\Lambda_n$) gives $m^c_{b_+}(S_0)/f_0(y_c)\ge D_{S_0}^{-1/2}c_{\rm IG}\sigma_*^2n^{-1/2}e^{-\Lambda_n}$, and $D_{S_0}\le(n+1)^{s_0}$ ([P1] `lem:spec`(e)). The bound on $E_0\Lambda_n$ is the last paragraph of that proof. The factor $\varpi(S_0)\ge\frac12(2p)^{-s_0}$ is not used. $\square$

*Proof of T02(i♯).* Fix $n$ with $s_0\le K$ and an integer $m$ with $R_m>0$ (otherwise there is nothing to prove). Put $E_m=\{|S|>m\}$, $v_m:=\varpi(E_m)=R_m\varpi(S_0)>0$, $N_m:=I_{b_-}(E_m)/f_0(y_c)$ and $\Theta^{(1)}_{n,m}:=N_m/v_m\ge0$. Since $b_-$ is data-free, [P1] `lem:num` gives $E_0N_m=v_m$, i.e. $E_0\Theta^{(1)}_{n,m}=1$. On $\mathcal B_n$, [P1] `thm:Ta` and Lemma den′ give
$$\Pi(E_m\mid y)\le\kappa^2\frac{I_{b_-}(E_m)}{\varpi(S_0)m^c_{b_+}(S_0)}=\kappa^2\frac{v_m\Theta^{(1)}_{n,m}}{\varpi(S_0)\,m^c_{b_+}(S_0)/f_0(y_c)}\le R_m(n+1)^{s_0/2}\sqrt n\cdot c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m}.$$
So on $\mathcal B_n$, $\Theta^\sharp_{n,m}\le c^\sharp e^{\Lambda_n}\Theta^{(1)}_{n,m}$. For $L>c^{\sharp2}$, $\{c^\sharp e^{\Lambda_n}\Theta^{(1)}>L\}\subseteq\{\Theta^{(1)}>\sqrt L\}\cup\{c^\sharp e^{\Lambda_n}>\sqrt L\}$, so
$$P_0(\Theta^\sharp_{n,m}>L)\le P_0(\mathcal B_n^c)+P_0(\Theta^{(1)}_{n,m}>\sqrt L)+P_0\big(\Lambda_n>\log(\sqrt L/c^\sharp)\big)\le P_0(\mathcal B_n^c)+\frac1{\sqrt L}+\frac{C_\Lambda}{\log(\sqrt L/c^\sharp)},$$
by Markov's inequality ($\Theta^{(1)}\ge0$, $\Lambda_n\ge0$). $P_0(\mathcal B_n^c)\le(8+24M/\sigma_*^2)/(n-1)$ by [P1] `thm:T01iii`. The right side does not depend on $m$. For the consequence take $m=m^\sharp_n(\omega_n)$: $R_m\le n^{-(s_0+1)/2}e^{-\omega_n}$, hence $\Pi(|S|>m\mid y)\le n^{-(s_0+1)/2}e^{-\omega_n}(n+1)^{s_0/2}\sqrt n\,\Theta^\sharp_{n,m}=(1+\frac1n)^{s_0/2}e^{-\omega_n}\Theta^\sharp_{n,m}$, and $P_0(\Theta^\sharp_{n,m}>L)\le\sup_{m'}P_0(\Theta^\sharp_{n,m'}>L)$. $\square$

*Remark.* As in [P1], only $\|\mu\|^2\le nM$, $\lambda_{\min}(R_{S_0})\ge\varphi_0^2$ and $s_0\le K$ are used from R; no eigenvalue condition on other models; $p\le n^A$ is not used.

---

## 3. Proposition D: COUNTEREXAMPLE to the target scale without SE (COUNTEREXAMPLE, reproducible)

**Design.** $n\ge3$, $2\le p$ (e.g. $p=n$, so $A=1$), $x\in\mathbb R^n$ fixed with $\|Cx\|^2=n-1$, $X^r=[x,\dots,x]$ ($p$ identical columns), $\beta^*=(\beta_1,0,\dots,0)$ with fixed $\beta_1\ne0$, any $\alpha^*$, $\sigma_*>0$. Then $s_0=1$, $S_0=\{1\}$, $\tilde x:=Cx$ is every standardised column, $\|\mu\|^2/n=\beta_1^2(n-1)/n\le\beta_1^2=:M$, $\lambda_{\min}(R_{S_0})=1$: **G and R hold** (SE fails at size 2).

**Claim.** With $E_n:=\{m(\emptyset)\le m(\{1\})\}$, $P_0(E_n)\to1$, and on $E_n$, for every integer $0\le m\le K-1$,
$$\Pi(|S|>m\mid y)\ \ge\ 2^{-(m+4)}\exp\Big\{-\frac{m(m-1)}{4(p-m)}\Big\}.$$
Consequently, for any deterministic $m_n\le\sqrt p$ with $\Pi(|S|>m_n\mid y)=O_{P_0}(n^{-1/2})$, necessarily $m_n\ge\frac12\log_2n-O(1)$; in particular no cutoff $m_n=s_0+O(s_0\log n/\log p)=1+O(1)$ (here $p=n$) works, and more generally $\Pi(|S|>m_n\mid y)=O_{P_0}(e^{-\omega_n})$ forces $m_n\ge\omega_n/\log2-O(1)$.

*Proof.* Let $S$ have $|S|=k\ge1$. Then $X_S=\tilde x\mathbf 1_k^\top$, $G_S=N\mathbf 1\mathbf 1^\top$ (eigenvalues $kN,0,\dots,0$), so $D_S=\frac{(n+1)kN+1}{kN+1}=:D_k$; $H_S=(n+1)N\mathbf 1\mathbf 1^\top+I$ has $\mathbf 1$ as eigenvector with eigenvalue $(n+1)Nk+1$, so with $c:=\tilde x^\top y$, $z_S=c\mathbf 1$ and $Q_S=N-\frac{nkc^2}{(n+1)Nk+1}=:Q_k$ (using $y^\top y=N$). Hence $m(S)=:m_k$ depends on $|S|$ only, and $\Pi(|S|=k\mid y)=q_km_k/\sum_{k'=0}^Kq_{k'}m_{k'}$ ($W_K$ cancels).

*Two-sided comparison of $m_k$, $k\ge1$, with $m_1$ (deterministic).* $D_k\le n+1$ and $D_1\ge\frac{(n+1)N}{N+1}$, so $(D_1/D_k)^{1/2}\ge(N/(N+1))^{1/2}\ge(2/3)^{1/2}$; and $k\mapsto\frac k{(n+1)Nk+1}$ is increasing, so $Q_k\le Q_1$ and $(2b_0+Q_k)^{-\nu}\ge(2b_0+Q_1)^{-\nu}$. Thus $m_k\ge(2/3)^{1/2}m_1$. Conversely $D_k\ge D_1$, and $0\le Q_1-Q_k\le nc^2\big[\frac1{(n+1)N}-\frac1{(n+1)N+1}\big]\le\frac{n}{(n+1)^2}\le\frac1n$ using $c^2\le\|\tilde x\|^2\|y\|^2=N^2$; with $Q_k\ge\|y\|^2/(n+1)=N/(n+1)$ ([P1] `lem:spec`(b)), $\frac{2b_0+Q_1}{2b_0+Q_k}\le1+\frac{n+1}{nN}\le1+\frac2n$ ($n\ge3$), so $m_k/m_1\le(1+\frac2n)^{\nu}\le e^{2\nu/n}=e^{1+0.02/n}\le e^{1.01}$.

*Tail.* On $E_n$, using $q_0=\frac12$ and $\sum_kq_k\le1$ ([P1] `lem:prior`(a)):
$$\Pi(|S|>m\mid y)\ge\frac{(2/3)^{1/2}m_1\sum_{k>m}q_k}{q_0m_0+e^{1.01}m_1\sum_{k\ge1}q_k}\ge\frac{(2/3)^{1/2}}{\frac12+e^{1.01}}\,q_{m+1}\ge\tfrac14\,q_{m+1}.$$
By E1(a) with $s_0=0$: $q_{m+1}=\frac12\rho_0\prod_{i=1}^m\rho_i$ with $\rho_0\ge\frac12$ and, as in E1(c), $\prod_{i=1}^m\rho_i\ge2^{-m}e^{-m(m-1)/(4(p-m))}$ ($m\le K-1\le p-1$). So $q_{m+1}\ge2^{-(m+2)}e^{-m(m-1)/(4(p-m))}$.

*$P_0(E_n)\to1$.* $m_0/m_1=D_1^{1/2}\big(\frac{2b_0+Q_1}{2b_0+N}\big)^\nu$ and $N-Q_1=\frac{nc^2}{(n+1)N+1}$. With $u:=c^2/N^2\in[0,1]$ (squared sample correlation of $x$ and $y^r$), $\frac{2b_0+Q_1}{2b_0+N}=1-u\frac{nN^2}{((n+1)N+1)(N+2b_0)}\le1-\frac u2$ (the fraction is $\ge\frac12$ for $n\ge3$: $((n+1)N+1)(N+0.02)\le1.01(n+1.5)N^2\le2nN^2$). So $m_0/m_1\le(n+1)^{1/2}e^{-\nu u/2}\le(n+1)^{1/2}e^{-nu/4}$, and $E_n\supseteq\{u\ge2\log(n+1)/n\}$. Now $Cy^r=\beta_1\tilde x+C\varepsilon$, so $u=\frac{(\beta_1N+\tilde x^\top\varepsilon)^2}{N(\beta_1^2N+2\beta_1\tilde x^\top\varepsilon+\|C\varepsilon\|^2)}$ with $\tilde x^\top\varepsilon\sim N(0,\sigma_*^2N)$ and $\|C\varepsilon\|^2/\sigma_*^2\sim\chi^2_N$. By Chebyshev, $\tilde x^\top\varepsilon/N\to0$ and $\|C\varepsilon\|^2/N\to\sigma_*^2$ in probability, so $u\to\beta_1^2/(\beta_1^2+\sigma_*^2)>0$ in probability while $2\log(n+1)/n\to0$.

*Consequence.* If $\Pi(|S|>m_n\mid y)=O_{P_0}(e^{-\omega_n})$ with $m_n\le\min(\sqrt p,K-1)$, then for some $L$ and all large $n$, $P_0(\Pi(|S|>m_n\mid y)\le Le^{-\omega_n})\ge\frac12$, which meets $E_n$ for large $n$, giving $2^{-(m_n+4)}e^{-1/2}\le Le^{-\omega_n}$ (as $m_n(m_n-1)/(4(p-m_n))\le\frac12$ once $\sqrt p\le p/2$), i.e. $m_n\ge\omega_n/\log 2-\log_2L-5$. (If $m_n\ge K$ the tail is $0$; that is consistent: $K=\lfloor n/2\rfloor\gg\frac12\log_2 n$.) $\square$

**Reproduction:** `scripts/duplicate_counterexample.py` (output in `duplicate_counterexample_output.txt`): $2^m\,\Pi(|S|>m\mid y)\in[0.70,1.00]$ for $m\le16$, $n\in\{200,\dots,2\cdot10^5\}$; the smallest $m$ with $\Pi(|S|>m\mid y)\le n^{-1/2}$ is $4,6,8,9$ for $n=200,2000,20000,200000$ ($\approx\frac12\log_2n$); 200/200 replicate data sets at $n=p=2000$ satisfy $\Pi(|S|>m\mid y)\ge2^{-m}/8$ for all $m\le12$.

---

## 4. Restricted eigenvalue hypotheses and bookkeeping

**Hypotheses (new).** Let $j_0:=\lceil(2A+1)s_0\rceil+1$ (this is $j_*$ of [P3]; it depends only on $s_0,A$) and $g_0>0$ a fixed constant.

- **SE$_\lambda(j_0)$** [anchored, normalised, bounded size]: $\lambda_{\min}(R_{S_0\cup J})\ge\varphi_0^2$ for every $J\subseteq[p]\setminus S_0$ with $|J|\le j_0$ and $S_0\cup J\ne\emptyset$.
- **SE$_w(m;g_0)$** [anchored, unnormalised]: $\lambda_{\min}(G_{S_0\cup J})\ge g_0$ (equivalently $\lambda_{\min}(R_{S_0\cup J})\ge g_0/(n-1)$) for every $J\subseteq[p]\setminus S_0$ with $|J|\le m$ and $S_0\cup J\ne\emptyset$.

These are restrictions of SE to the **comparison unions** $S\cup S_0$ used by the proofs. The locked SE (all $T$ with $|T|\le\min(p,m_n+s_0)$, constant $\varphi_0^2$) implies SE$_\lambda(j_0)$ (as $j_0\le m_n$ for large $n$) and SE$_w(m^\sharp_n;\varphi_0^2)$ (as $m^\sharp_n\le m_n$ by E2(i), and $(n-1)\varphi_0^2\ge\varphi_0^2$). So the new hypotheses are weaker.

**Lemma I (interlacing; standard).** If $\emptyset\ne T\subseteq T'$, then $\lambda_{\min}(G_T)\ge\lambda_{\min}(G_{T'})$. *Proof.* For $v\in\mathbb R^T$, $v^\top G_Tv=\tilde v^\top G_{T'}\tilde v$ with $\tilde v$ the zero-padding, and $\|\tilde v\|=\|v\|$. $\square$

**Lemma B (what the proofs need; PROVED).** Assume R, SE$_\lambda(j_0)$ and SE$_w(m^\sharp_n;g_0)$.
- **(B1)** For $J\subseteq[p]\setminus S_0$ with $1\le|J|\le m^\sharp_n$: $\lambda_{\min}(G_{S_0\cup J})\ge g_0>0$, so $X_{c,S_0\cup J}$ has full column rank, $P_{S_0\cup J}-P_{S_0}$ is an orthogonal projection of rank $|J|$, and under G, $\chi^2_J:=\sigma_*^{-2}\|(P_{S_0\cup J}-P_{S_0})e\|^2\sim\chi^2_{|J|}$ exactly; and $D_{S_0\cup J}/D_{S_0}\ge[(n+1)(1+1/g_0)^{-1}]^{|J|}$.
- **(B2)** For underfitting $S$ (i.e. $S_0\not\subseteq S$) with $|J'(S)|\le j_0$, $S'=S\cup S_0$: $\lambda_{\min}(G_{S'})\ge N\varphi_0^2$; if $S\ne\emptyset$, $\lambda_{\min}(G_S)\ge N\varphi_0^2$; $P_{S'}-P_S$ is an orthogonal projection of rank $|J(S)|$; under G, $N_S/\sigma_*^2\sim\chi^2_{|J(S)|}$.
- **(B3)** For $S\subseteq T$, $T\ne\emptyset$, with $S=\emptyset$ or $\lambda_{\min}(G_S)\ge N\varphi_0^2$, and every $u\in\mathbb R^N$: $u^\top(M_T-M_S)u\le\frac n{n+1}\big[\|(P_T-P_S)u\|^2+\eta_n\|P_Su\|^2\big]$. (Upper half of [P3] `cor:diff`, with the eigenvalue condition on $S$ only.)

*Proof.* (B1) SE$_w$; full column rank because $G_{S_0\cup J}\succ0$; then $\mathrm{col}(X_{c,S_0})\subseteq\mathrm{col}(X_{c,S_0\cup J})$ have dimensions $s_0$ and $s_0+|J|$, so the difference of the projections is the projection onto the orthogonal complement, of rank $|J|$; $e\sim N_N(0,\sigma_*^2I)$ ([P3] `lem:red`(b)). The determinant bound is [P1] `lem:spec`(e) with $g=g_0$ (that lemma is stated for arbitrary $g>0$). (B2) $S'=S_0\cup J'(S)$ with $|J'(S)|\le j_0$, so SE$_\lambda$ gives $\lambda_{\min}(R_{S'})\ge\varphi_0^2$, i.e. $\lambda_{\min}(G_{S'})\ge N\varphi_0^2$; Lemma I gives it for $S\subseteq S'$. Ranks: $|S'|-|S|=|J(S)|$ as in (B1). $N_S=\|(P_{S'}-P_S)e\|^2$. (B3) $M_T\preceq\frac n{n+1}P_T$ ([P3] `lem:smoother`(b), no condition); $M_S\succeq(1-\eta_n)\frac n{n+1}P_S$ ([P3] `lem:smoother`(c) applied to $S$; trivial if $S=\emptyset$); $P_T-P_S$ is the orthogonal projection onto $\mathrm{col}(X_{c,T})\ominus\mathrm{col}(X_{c,S})$. $\square$

---

## 5. Theorem T02(ii♯) (PROVED; candidate — changed steps written in full, unchanged steps cited)

**Statement.** In R1 under G, R and SE$_w(m^\sharp_n;g_0)$: $\Pi(\{S\in\Omega:S\supsetneq S_0\}\mid y)=O_{P_0}(r_n)$.

*Proof.* Follow [P1] §`sec:T02ii` with $m_n$ replaced by $m^\sharp_n$ everywhere. Changes:
1. [P1] eq. (`eq:mnlog`) $m_n\le C_m\log n$: holds for $m^\sharp_n$ since $m^\sharp_n\le m_n(\frac12\log n)$ (E2(i)). Hence $\delta_n\log n\to0$ and every threshold placed in $n_0$ is as before.
2. The sentence "SE applies to $S_0\cup J$ … $\chi^2_J\sim\chi^2_{|J|}$ exactly" is replaced by Lemma B(B1).
3. [P1] `lem:good`, `lem:onG` (a)–(c): unchanged (they use R for $S_0$ only and union bounds that do not use SE).
4. [P1] `lem:one`: in the step "SE gives $\lambda_{\min}(G_S)\ge(n-1)\varphi_0^2$; `lem:spec`(e) with $g=(n-1)\varphi_0^2$", use (B1) instead: $(D_{S_0}/D_S)^{1/2}\le(n+1)^{-j/2}(1+1/g_0)^{j/2}$. All other lines of `lem:one` use only `lem:onG` and R. So `lem:one` holds with $(1+\frac1{(n-1)\varphi_0^2})$ replaced by $(1+\frac1{g_0})$.
5. [P1] `thm:T02ii`: $a_n:=(n+1)^{-1/2}(1+1/g_0)^{1/2}e^{\zeta_n}$, $\bar r_n=\frac12a_n\sqrt{eC_A\log n}$, so $\bar r_n^2\le\frac{e^{2\zeta_n}}4\,eC_A(1+\tfrac1{g_0})\,r_n^2\le c_2^2r_n^2$ with $c_2:=\sqrt{eC_A(1+1/g_0)}$ once $e^{2\zeta_n}\le4$, and $\bar r_n\le\frac12$ eventually. The remainder of the term $T_1$ is verbatim. The term $T_2=\Pi(|S|>m^\sharp_n\mid y)\le(1+\frac1n)^{s_0/2}n^{-1/2}\Theta^\sharp_{n,m^\sharp_n}\le2^{s_0/2}r_n\Theta^\sharp_{n,m^\sharp_n}$ by T02(i♯) with $\omega_n=\frac12\log n$. $\square$

---

## 6. Theorem T03♯ (restated selection consistency; PROVED as a candidate: changed steps written in full here, unchanged steps cited by label)

**Hypotheses.** Regime R1 (triangular array, $n\to\infty$, $s_0$ fixed, $p=p_n\le n^A$); **G**; **R**; **SE$_\lambda(j_0)$**; **SE$_w(m^\sharp_n;g_0)$** for a fixed $g_0>0$; and, for (i)–(iii), a beta-min condition in one of the forms
- **BM-∞**: $\min_{j\in S_0}\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)$ with $M_n\to\infty$;
- **BM($c$)**: the same with a fixed constant $c>c_0(s_0,A)$, where $c_0(s_0,A)<\infty$ depends only on $s_0$ and $A$ (the proof gives $c_0=L_*=\max\{4C_*,32[s_0(A+1)+2]\}$ with $C_*$ of [P3]; this value is a proof artefact, not sharp).

No hypothesis H-T02: T02(i♯) (§2) is proved and used directly.

**Conclusions.** (i) $1-\pi(S_0)=O_{P_0}(r_n)$. (ii) $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0)$ for every data set; $P_0(\mathrm{MPM}=S_0)\to1$. (iii) $P_0(S^\dagger\ne S_0)\le2E_0[1-\pi(S_0)]\to0$; on $\{\pi(S_0)>\frac12\}$, $S_0$ is the strict global maximiser of $F$. (iv) [no beta-min] For fixed $c>c_0$ and $J_n(c)=\{j\in S_0:\theta^{*2}_j\ge c\,\sigma_*^2\log n/(n\varphi_0^2)\}$: $\Pi(S\not\supseteq J_n(c)\mid y)=O_{P_0}(r_n)$ and $1-\min_{j\in J_n(c)}\mathrm{PIP}_j=O_{P_0}(r_n)$; the same holds for $J_n^\infty=\{j:\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)\}$ with any $M_n\to\infty$ (as $J^\infty_n\subseteq J_n(c_0+1)$ eventually). (v) Scale invariance as in [P3].

**Proof.** We go through [P3] with $m_n:=m^\sharp_n$. The thresholds $n_0$ now depend on $(s_0,A,\varphi_0,\sigma_*^2,M,g_0)$ and, under BM($c$), on $c$.

**(C1) Setting ([P3] §1).** $m_n:=m^\sharp_n$. [P3] eq. (`eq:mn`) holds: $m^\sharp_n\le m_n(\frac12\log n)\le C_m\log n$ (E2(i)). The sequences $\delta_n,\epsilon_n,q_n$ remain nondecreasing in $m_n$ and dominated as stated there. Also $s_0\le m^\sharp_n\le K$.

**(C2) Ranks and laws ([P3] §`sec:good`, the paragraph before the definition of $\mathcal G_n$).** Replace "Under SE every $T\subseteq[p]$ with $1\le|T|\le m_n+s_0$ has $\lambda_{\min}(G_T)\ge N\varphi_0^2$ …" by Lemma B: (B1) gives that $\chi^2_J$ is exactly $\chi^2_{|J|}$ for $1\le|J|\le m^\sharp_n$; (B2) gives $N_S/\sigma_*^2\sim\chi^2_{|J(S)|}$ with $|J(S)|\le s_0$ for underfitting $S$ with $|J'(S)|\le j_0$, which is the only range in which (G4) is imposed. The event $\mathcal G_n$ ((G1)–(G4)) and [P3] `lem:Gprob` ($P_0(\mathcal G_n^c)\le5/n$) are unchanged: (G1), (G2) use no eigenvalue condition (for (G2) the rank is $\le|T|$), (G3) uses (B1), (G4) uses (B2).

**(C3) [P3] `lem:ongood`(c), restricted.** *Statement:* for $n\ge n_0$, on $\mathcal G_n$, for every underfitting $S$ with $|S|\le m^\sharp_n$ **and $|J'(S)|\le j_0$**: $2b+Q^c_S\le E_n+V_S$, with $E_n$ as in [P3] and the same two-sided bounds on $E_n$. *Proof:* the proof of [P3] `lem:ongood`(c) verbatim, where the one use of SE ("If $S\ne\emptyset$, SE gives $\lambda_{\min}(G_S)\ge N\varphi_0^2$") is supplied by (B2). Parts (a), (b), (d) of `lem:ongood` are unchanged (no SE is used there; (b) uses (G1)–(G2) only).

**(C4) [P3] `lem:onesup`, modified.** *Statement:* for $n\ge n_0$, on $\mathcal G_n$, for every $J\subseteq[p]\setminus S_0$ with $1\le|J|=j\le m^\sharp_n$ and $S=S_0\cup J$:
$$\frac{m(S)}{m(S_0)}\le(n+1)^{-j/2}\Big(1+\frac1{g_0}\Big)^{j/2}\exp\Big\{\frac{\upsilon_n}2\chi^2_J+\rho_n\Big\},$$
with $\upsilon_n,\rho_n,\epsilon_n$ as in [P3] (unchanged). *Proof.* By [P3] eq. (`eq:score`), $\frac{m(S)}{m(S_0)}=\big(\frac{D_{S_0}}{D_S}\big)^{1/2}\big(1+\frac{t_S-t_{S_0}}{2b+Q^c_S}\big)^\nu$ exactly. *Determinant:* (B1) gives $(D_{S_0}/D_S)^{1/2}\le(n+1)^{-j/2}(1+1/g_0)^{j/2}$. *Numerator:* $t_S-t_{S_0}\ge0$ ([P3] `lem:smoother`(d)); (B3) with $(S,T)=(S_0,S)$ — the eigenvalue condition on $S_0$ is R — and $u=y_c$, together with $(P_S-P_{S_0})\mu_c=0$ and (B1), gives $t_S-t_{S_0}\le\frac n{n+1}[\sigma_*^2\chi^2_J+\eta_n\|y_c\|^2]$. *Denominator:* $2b+Q^c_S\ge N\sigma_*^2(1-\delta_n)$ by `lem:ongood`(b) ($|S|\le m^\sharp_n+s_0$). The rest (the bound $\log(1+x)\le x$, `lem:ongood`(d) with $B=2b+Q^c_S$, and the algebra giving $\frac{\upsilon_n}2\chi^2_J$) is verbatim from [P3] `lem:onesup`. $\square$
(The locked proof used the full [P3] `cor:diff`, which assumes $\lambda_{\min}(G_{S_0\cup J})\ge N\varphi_0^2$; only its upper half is needed, and that needs the eigenvalue bound on $S_0$ only.)

**(C5) [P3] `prop:sup`, modified.** Define $\Upsilon_n,\Upsilon_n^{>j_1}$ as in [P3] with $(1+\frac1{N\varphi_0^2})$ replaced by $(1+\frac1{g_0})$, with the $j$-sum over $1\le j\le m^\sharp_n$, and
$$q_n:=\Big[\frac{eC_A\log n}{4(n+1)}\Big(1+\frac1{g_0}\Big)e^{2\epsilon_n}\Big]^{1/2},\qquad c_q:=\sqrt{eC_A(1+1/g_0)} .$$
Then for $n\ge n_0$: (a) on $\mathcal G_n$, $\sum_{j=j_1+1}^{m^\sharp_n}\Xi_j\le e^{\rho_n}\Upsilon_n^{>j_1}$; (b) $q_n\le\min\{\frac12,c_qr_n\}$ and $E_0\Upsilon_n^{>j_1}\le2K_{s_0,j_1}q_n^{j_1+1}$; (c) $\Upsilon_n=O_{P_0}(r_n)$. *Proof.* (a) as in [P3] using (C4). (b) $q_n^2=c_q^2r_n^2\cdot\frac{n}{n+1}\cdot\frac{e^{2\epsilon_n}}4\le c_q^2r_n^2$ once $e^{2\epsilon_n}\le4$, and $q_n\to0$; the expectation bound is the [P3] computation verbatim, which uses only that the weights are deterministic, that each $\chi^2_J$ is exactly $\chi^2_j$ (B1), [P3] `lem:chi`(b) and [P3] `lem:prior`(b). (c) Markov, as in [P3]. $\square$

**(C6) [P3] `lem:SvsSp`, split into a crude and a sharp part.**
*(a) [no eigenvalue condition]* For every underfitting $S$ with $S'=S\cup S_0$ and every data set: $\ell(S)/\ell(S')\le(2p)^{|J(S)|}(n+1)^{|J(S)|/2}\le(2p)^{s_0}(n+1)^{s_0/2}$.
*Proof.* $\ell(S)/\ell(S')=\frac{w(|S|)}{w(|S'|)}\big(\frac{D_{S'}}{D_S}\big)^{1/2}\big(\frac{2b+Q^c_{S'}}{2b+Q^c_S}\big)^\nu$ ([P3] eq. (`eq:score`)). The prior factor is $\le(2p)^{|J|}$ ([P3] `lem:prior`(a), $|S'|\le p$); $D_{S'}/D_S\le(n+1)^{|J|}$ ([P3] `lem:det`, first part, no condition); $Q^c_{S'}\le Q^c_S$ because $t_{S'}\ge t_S$ ([P3] `lem:smoother`(d)), and $2b>0$, so the last factor is $\le1$. $|J(S)|\le s_0$. $\square$
*(b)* For underfitting $S$ with $|S|\le m^\sharp_n$ and $|J'(S)|\le j_0$, on $\mathcal G_n$, $n\ge n_0$: the two displayed inequalities of [P3] `lem:SvsSp`. *Proof:* verbatim, with the eigenvalue condition for [P3] `cor:diff` on the pair $S\subseteq S'$ supplied by (B2), and `lem:ongood`(c) by (C3).

**(C7) [P3] `lem:signal` and `lem:signalgain`.** Unchanged; they are applied only to underfitting $S$ with $|J'(S)|\le j_0$, for which (B2) supplies $\lambda_{\min}(G_{S'})\ge N\varphi_0^2$, and `lem:signalgain` uses (C6)(b) and (G4).

**(C8) [P3] `lem:assemble`, modified.** *Statement:* for $n\ge n_0$ and a collection $\mathcal U$ of underfitting models with $|S|\le m^\sharp_n$, with $\kappa_n(\mathcal U):=\max\{\ell(S)/\ell(S'):S\in\mathcal U,|J'(S)|\le j_0\}$, on $\mathcal G_n$,
$$\sum_{S\in\mathcal U}\frac{\ell(S)}{\ell(S_0)}\le2^{s_0}\kappa_n(\mathcal U)\big(1+e^{\rho_n}\Upsilon_n\big)+2^{s_0}(2p)^{s_0}(n+1)^{s_0/2}e^{\rho_n}\Upsilon_n^{>j_0},$$
and $(2p)^{s_0}(n+1)^{s_0/2}\Upsilon_n^{>j_0}=O_{P_0}\big((\log n)^{(j_0+1)/2}/n\big)$.
*Proof.* As in [P3]: write $\frac{\ell(S)}{\ell(S_0)}=\frac{\ell(S)}{\ell(S')}\frac{\ell(S')}{\ell(S_0)}$; each $S'=S_0\cup J'$ arises from at most $2^{s_0}-1$ underfitting $S$; $|J'(S)|\le|S|\le m^\sharp_n$. For $|J'|\le j_0$ use $\kappa_n(\mathcal U)$ and $\sum_{j=1}^{m^\sharp_n}\Xi_j\le e^{\rho_n}\Upsilon_n$ ((C5)(a), $j_1=0$; plus $1$ for $S'=S_0$). For $|J'|>j_0$ use (C6)(a) — **no eigenvalue condition on $S'$** — and $\sum_{j>j_0}\Xi_j\le e^{\rho_n}\Upsilon^{>j_0}_n$ ((C5)(a)). For the rate: by (C5)(b), $E_0[(2p)^{s_0}(n+1)^{s_0/2}\Upsilon^{>j_0}_n]\le2K_{s_0,j_0}2^{s_0}n^{As_0}(n+1)^{s_0/2}(c_q^2\log n/n)^{(j_0+1)/2}$, and $\frac{j_0+1}2\ge s_0(A+\frac12)+1$ gives $n^{As_0}(n+1)^{s_0/2}n^{-(j_0+1)/2}\le2^{s_0/2}n^{-1}$; Markov. $\square$

**(C9) Step 0 ([P3] eq. (`eq:tail`)).** Replaced by T02(i♯) with $\omega_n=\frac12\log n$: $\Pi(|S|>m^\sharp_n\mid y)\le(1+\frac1n)^{s_0/2}n^{-1/2}\Theta^\sharp_{n,m^\sharp_n}=O_{P_0}(n^{-1/2})$. (Same form as eq. (`eq:tail`); if $m^\sharp_n=K$ the left side is $0$.)

**(C10) Step 1 and (iv): the beta-min constant.** Let $\mathcal U$ be the underfitting $S\in\Omega$ with $|S|\le m^\sharp_n$. For $S\in\mathcal U$ with $|J'(S)|\le j_0$, [P3] `lem:signal` (with (B2)) and BM($c$) give $\Delta_S\ge N\varphi_0^2\min_j\theta^{*2}_j\ge(1-\frac1n)c\,\sigma_*^2\log n\ge L_*\sigma_*^2\log n$ for $n\ge c/(c-L_*)$, because $c>c_0=L_*$. From here Step 1 is verbatim ([P3] `lem:signalgain` with $L=L_*$ gives $\kappa_n(\mathcal U)\le e^{\rho_n}n^{-2}$ on $\mathcal G_n$). Under BM-∞, $M_n\ge L_*+1$ for large $n$, i.e. BM($L_*+1$) holds eventually. In (iv), the same with $\mathcal U_j=\{S\in\Omega:|S|\le m^\sharp_n,\,j\notin S\}$, $j\in J_n(c)$, using only $\theta^{*2}_j$ (verbatim [P3] (iv)).

**Assembly.** [P3] paragraphs (i), (ii), (iii), (iv), (v) are then verbatim, with "$m_n$" read as $m^\sharp_n$, "eq. (`eq:tail`)" as (C9), "`lem:assemble`" as (C8), "`prop:sup`(c)" as (C5)(c), and "`lem:Gprob`" as in (C2). In particular, in (i): every $S\in\Omega\setminus\{S_0\}$ has $|S|>m^\sharp_n$, or is a superset of size $\le m^\sharp_n$ (bounded by (C5)), or lies in $\mathcal U$ (bounded by (C8)+(C10)); each part is $O_{P_0}(r_n)$ and $P_0(\mathcal G_n^c)\le5/n$. $\square$

**Unchanged steps (cited by label, no edit):** [P3] `lem:red`, `lem:smoother`, `cor:diff` (now used only in (C6)(b), with $T=S'$, $|J'(S)|\le j_0$), `lem:det`, `lem:prior`, `lem:signal`, `lem:chi`, `lem:Gprob` (probability computations), `lem:ongood`(a),(b),(d), `lem:signalgain`, paragraphs (ii), (iii), (v). [P1] `lem:spec`, `lem:prior`, `lem:chi`, `lem:num`, `thm:T01iii`, `thm:Ta`, `lem:good`, `lem:onG`, and the body of `lem:den`.

**Changed steps:** [P1] `thm:T02i` (→ T02(i♯), §2; via Lemma den′), [P1] `lem:one` and `thm:T02ii` (→ §5), [P3] §1 definition of $m_n$ (C1), the SE paragraph of §`sec:good` (C2), `lem:ongood`(c) (C3), `lem:onesup` (C4), `prop:sup` (C5), `lem:SvsSp` (C6), `lem:assemble` (C8), Step 0 (C9), Step 1 / (iv) constant (C10).

---

## 7. Remarks

1. **Where the normalised constant $\varphi_0^2$ is really needed.** Only (a) $\lambda_{\min}(R_{S_0})$ (R), and (b) the sets $S\cup S_0$ with at most $j_0$ extra variables, through `lem:signal` (the beta-min scale $1/\varphi_0^2$) and the ridge correction of `cor:diff`. Large supersets need only $\lambda_{\min}(G)\ge g_0$, i.e. a normalised eigenvalue $\ge g_0/(n-1)$: no near-exact collinearity among $\le m^\sharp_n$ extra columns joined to $S_0$.
2. **Cap.** Since $R_K=0$, $m^\sharp_n\le K$ always; the size range of SE$_w$ is $\le K+s_0$. At $n=200$ this is what removes the rank obstruction ($K+s_0=114\le199$), not the exact tail (§8 of REPORT).
3. **Further weakening (CONJECTURE, not proved here).** In (C4) only the determinant ratio $D_{S_0\cup J}/D_{S_0}\ge[c(n+1)]^{|J|}$ and full rank are used; an assumption on determinants alone (a geometric-mean eigenvalue condition) would suffice for (C4)–(C5). Not pursued.
