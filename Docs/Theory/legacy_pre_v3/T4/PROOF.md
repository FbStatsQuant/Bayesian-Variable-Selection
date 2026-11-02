# Proof of Theorem T4 (two-state switch: the schedule is cheap)

Thread: T4. Prover: Fable 5.1 (lead), 14 October 2026. Status: proof complete for (i)–(iii); constant in (ii) explicit; numerical sanity checks in `check_T4.py` (not part of the proof).

Assumed from the draft: only the definitions of Section 2 (bridge, $\chi^2$, greedy population-ESS schedule, path length). Lemma L4(i) is proved inline for the two-point space (Lemma 2). No other numbered result is used.

---

## 0. Setting, conventions and notation

**The two-point bridge.** The space is $\{0,1\}$. For $\phi\in\mathbb R$,
$$
q_\phi(1)=u(\phi):=\operatorname{logistic}\big(\ell_0+\phi\Delta\big),\qquad q_\phi(0)=1-u(\phi),\qquad \Delta:=\ell_1-\ell_0>0,
$$
where $\operatorname{logistic}(x)=1/(1+e^{-x})$. Put $u_0:=u(0)$ and $u^\ast:=u(1)$. (The statement writes $u_1$ for the endpoint $u(1)$; we write $u^\ast$ so that $u_1$ cannot be confused with the element of index $1$ of the sequence $(u_t)$ in (1.1), and we read the hypothesis "$u_1\ge\varepsilon$" of (ii) as $u^\ast\ge\varepsilon$.) The threshold is $\rho\in(0,1)$ and $c:=\rho^{-1}-1>0$, so $\rho=1/(1+c)$.

**Relation to Section 2.** A bridge of Section 2 on $\{0,1\}$ is $\gamma_\phi(x)=\gamma_0(x)e^{\phi d(x)}$, $q_\phi=\gamma_\phi/\bar Z_\phi$, with $\gamma_0>0$. Then
$$
\log\frac{q_\phi(1)}{q_\phi(0)}=\log\frac{\gamma_0(1)}{\gamma_0(0)}+\phi\,\big(d(1)-d(0)\big),
$$
and since $\log\frac{\operatorname{logistic}(x)}{1-\operatorname{logistic}(x)}=x$, the two descriptions coincide exactly when
$$
\ell_0=\log\frac{\gamma_0(1)}{\gamma_0(0)},\qquad \Delta=d(1)-d(0). \tag{0.1}
$$
The hypothesis $\ell_1>\ell_0$ says that state $1$ is the state gaining mass along the bridge (relabel the two states otherwise). Only part (iii) uses $d$, through (0.1).

**Facts about $u$ (Lemma 0).** $u$ is $C^\infty$, strictly increasing, a bijection $\mathbb R\to(0,1)$, and
$$
u'(\phi)=\Delta\,u(\phi)\big(1-u(\phi)\big). \tag{0.2}
$$
*Proof.* $\operatorname{logistic}'(x)=\operatorname{logistic}(x)(1-\operatorname{logistic}(x))>0$, $\operatorname{logistic}$ maps $\mathbb R$ onto $(0,1)$, and $\Delta>0$. $\square$

In particular $0<u_0<u^\ast<1$.

**The schedule and $T$.** The greedy population-ESS schedule is $\phi_0=0$ and, as long as $\phi_{t-1}<1$,
$$
\phi_t=\sup\{\phi\in(\phi_{t-1},1]:\ \chi^2(q_\phi\|q_{\phi_{t-1}})\le c\}, \tag{0.3}
$$
with $\chi^2(q'\|q)=\sum_x q'(x)^2/q(x)-1$. The stage count is $T:=\min\{t\ge1:\phi_t=1\}$. Lemma 3 and Proposition 4 show that (0.3) is a well-defined maximum at every stage and that $T<\infty$, so no appeal to L4 is needed for this.

**Further notation.**
$$
g(w):=w+\sqrt{c\,w(1-w)}\quad(w\in[0,1]),\qquad v_t:=\log(1/u_t),\qquad \log_2^+x:=\log_2\max\{x,1\}.
$$
Note $\log_2^+ x\ge 0$, $\log_2^+ x=\log_2 x$ for $x\ge1$, and $v_0=\log(1/u_0)>0$.

---

## 1. Part (i): the exact recursion

**Lemma 1 ($\chi^2$ between two Bernoullis).** For generic numbers $u,v\in(0,1)$ (in this lemma only, $u$ is not the function $u(\cdot)$),
$$
\chi^2(\mathrm{Bern}(v)\,\|\,\mathrm{Bern}(u))=\frac{(v-u)^2}{u(1-u)}.
$$
*Proof.* By definition $\chi^2=\frac{v^2}{u}+\frac{(1-v)^2}{1-u}-1=\frac{v^2(1-u)+(1-v)^2u-u(1-u)}{u(1-u)}$. The numerator is $v^2-v^2u+u-2uv+uv^2-u+u^2=v^2-2uv+u^2=(v-u)^2$. $\square$

**Lemma 2 (L4(i) on the two-point space).** Fix $\psi\in\mathbb R$ and write $w=u(\psi)$, $s=\sqrt{c\,w(1-w)}>0$. Then:

(a) $\phi\mapsto\chi^2(q_\phi\|q_\psi)=\dfrac{(u(\phi)-w)^2}{w(1-w)}$ is continuous on $\mathbb R$ and strictly increasing on $[\psi,\infty)$; in particular $\delta\mapsto 1+\chi^2(q_{\psi+\delta}\|q_\psi)$ is nondecreasing on $\delta\ge0$.

(b) For $\phi\ge\psi$: $\ \chi^2(q_\phi\|q_\psi)\le c\iff u(\phi)\le w+s$.

*Proof.* (a) The formula is Lemma 1 with $v=u(\phi)$. For $\phi\ge\psi$, $u(\phi)-w\ge0$ is strictly increasing in $\phi$ (Lemma 0), hence so is its square; continuity is that of $u$. (b) For $\phi\ge\psi$, $u(\phi)-w\ge0$, so $(u(\phi)-w)^2\le c\,w(1-w)=s^2$ iff $u(\phi)-w\le s$. $\square$

**Lemma 3 (one greedy step).** Let $\psi\in[0,1)$, $w=u(\psi)$, $s=\sqrt{c\,w(1-w)}$, and $\mathcal A:=\{\phi\in(\psi,1]:\chi^2(q_\phi\|q_\psi)\le c\}$. Then $\mathcal A\neq\emptyset$, $\phi':=\sup \mathcal A$ belongs to $\mathcal A$, $\phi'>\psi$, and
$$
u(\phi')=\min\{u^\ast,\ g(w)\}=\min\{u^\ast,\ w+s\}.
$$
*Proof.* By Lemma 2(b), $\mathcal A=\{\phi\in(\psi,1]:u(\phi)\le w+s\}$.

*Case 1: $u^\ast\le w+s$.* For every $\phi\in(\psi,1]$, $u(\phi)\le u(1)=u^\ast\le w+s$, so $\mathcal A=(\psi,1]$, $\phi'=1\in \mathcal A$, and $u(\phi')=u^\ast=\min\{u^\ast,w+s\}$.

*Case 2: $u^\ast>w+s$.* Since $u$ is continuous and strictly increasing with $u(\psi)=w<w+s<u^\ast=u(1)$, there is a unique $\phi^*\in(\psi,1)$ with $u(\phi^*)=w+s$ (intermediate value theorem and injectivity). By monotonicity of $u$, $\mathcal A=(\psi,\phi^*]$, so $\phi'=\phi^*\in \mathcal A$ and $u(\phi')=w+s=\min\{u^\ast,w+s\}$.

In both cases $\mathcal A\ne\emptyset$ and $\phi'>\psi$. $\square$

**Proposition 4 (Part (i)).** Define the sequence $(u_t)_{t\ge0}$ by
$$
u_0=u(0),\qquad u_{t+1}=\min\{u^\ast,\ g(u_t)\}=\min\{u^\ast,\ u_t+\sqrt{c\,u_t(1-u_t)}\}. \tag{1.1}
$$
Then:

(a) $u_0\le u_t\le u_{t+1}\le u^\ast$ for all $t$, and $u_t=u^\ast$ implies $u_{t+1}=u^\ast$.

(b) $T^*:=\min\{t\ge0:u_t=u^\ast\}$ is finite and $T^*\ge1$. For $t<T^*$, $u_t<u^\ast$; for $t+1<T^*$, $u_{t+1}=g(u_t)$.

(c) The greedy schedule (0.3) is well defined for $t=0,\dots,T^*$, with $u(\phi_t)=u_t$, $\phi_t<1$ for $t<T^*$, $\phi_{T^*}=1$, and $\phi_t<\phi_{t+1}$. Hence $T=T^*$: the schedule produces exactly the recursion (1.1), and $T$ is its hitting time of $u^\ast$.

*Proof.* (a) Induction. $u_0<u^\ast$. If $u_0\le u_t\le u^\ast$ then $g(u_t)\ge u_t$ (the square root is $\ge0$), so $u_{t+1}=\min\{u^\ast,g(u_t)\}\in[u_t,u^\ast]$. If $u_t=u^\ast$ then $g(u_t)\ge u^\ast$ and $u_{t+1}=u^\ast$.

(b) $T^*\ge1$ because $u_0<u^\ast$. Suppose $u_t<u^\ast$ for all $t$. Then $u_{t+1}=\min\{u^\ast,g(u_t)\}<u^\ast$ forces $u_{t+1}=g(u_t)$ for every $t$. The map $x\mapsto x(1-x)$ is concave, so on $[u_0,u^\ast]$ it is at least $\mu:=\min\{u_0(1-u_0),u^\ast(1-u^\ast)\}>0$. Thus $u_{t+1}-u_t=\sqrt{c\,u_t(1-u_t)}\ge\sqrt{c\mu}$ for all $t$, whence $u_t\ge u_0+t\sqrt{c\mu}\to\infty$, contradicting $u_t\le u^\ast<1$. So $T^*<\infty$. The remaining claims: for $t<T^*$, $u_t<u^\ast$ by minimality and monotonicity (a); for $t+1<T^*$, $u_{t+1}<u^\ast$ forces $u_{t+1}=g(u_t)$ as just argued.

(c) We show by induction on $t\le T^*$ that $\phi_t$ is defined, $u(\phi_t)=u_t$, and $\phi_t\in[0,1)$ if $t<T^*$. For $t=0$: $\phi_0=0\in[0,1)$ and $u(\phi_0)=u_0$. Suppose $t<T^*$, $\phi_t\in[0,1)$, $u(\phi_t)=u_t$. Lemma 3 with $\psi=\phi_t$ shows that the supremum in (0.3) is attained, $\phi_{t+1}>\phi_t\ge0$, $\phi_{t+1}\le1$, and $u(\phi_{t+1})=\min\{u^\ast,g(u_t)\}=u_{t+1}$. If $t+1<T^*$ then $u(\phi_{t+1})=u_{t+1}<u^\ast=u(1)$, so $\phi_{t+1}<1$ (strict monotonicity of $u$), i.e. $\phi_{t+1}\in[0,1)$, and the induction continues. If $t+1=T^*$ then $u(\phi_{t+1})=u^\ast=u(1)$, so $\phi_{t+1}=1$ (injectivity of $u$). Since $\phi_t<1$ for $t<T^*$ and $\phi_{T^*}=1$, $T=\min\{t\ge1:\phi_t=1\}=T^*$. $\square$

From now on $T=T^*$, and (1.1) together with Proposition 4(b) is all that is used about the schedule.

---

## 2. Part (ii): the stage count

Throughout, $a:=\tfrac12\log(2/c)\in\mathbb R$, $a^+:=\max\{a,0\}$, $b:=\log(1+\sqrt c)>0$, and
$$
\theta_1:=e^{-1}\min\{1,\ c/2\},\qquad \eta:=\sqrt{c\,\theta_1(1-\rho)}=c\sqrt{\frac{\theta_1}{1+c}}>0.
$$
Note $\theta_1\le e^{-1}<\tfrac12$ and
$$
\log(1/\theta_1)=1+2a^+ . \tag{2.1}
$$
Indeed, if $c\le2$ then $a\ge0$ and $\log(1/\theta_1)=\log(2e/c)=1+\log(2/c)=1+2a$; if $c>2$ then $a<0$ and $\log(1/\theta_1)=1$.

### 2.1 The final step

**Lemma 5 (one step finishes from $u\ge\rho$).** For $w\in(0,1)$: $g(w)\ge1\iff w\ge\rho$. Consequently, if $t<T$ and $u_t\ge\rho$, then $T=t+1$.

*Proof.* $g(w)\ge1\iff\sqrt{c\,w(1-w)}\ge1-w\iff c\,w(1-w)\ge(1-w)^2$ (both sides nonnegative) $\iff c\,w\ge1-w$ (divide by $1-w>0$) $\iff w\ge1/(1+c)=\rho$. If $t<T$ and $u_t\ge\rho$, then $g(u_t)\ge1\ge u^\ast$, so $u_{t+1}=\min\{u^\ast,g(u_t)\}=u^\ast$ and $T\le t+1$; as $t<T$, $T=t+1$. $\square$

### 2.2 The first steps: $\log(1/u_t)$ halves

**Lemma 6 (halving from below).** If $t+1<T$ and $u_t\le\tfrac12$, then $v_{t+1}\le\tfrac12v_t+a$.

*Proof.* By Proposition 4(b), $u_{t+1}=g(u_t)\ge\sqrt{c\,u_t(1-u_t)}\ge\sqrt{c\,u_t/2}$, using $1-u_t\ge\tfrac12$. Taking logarithms, $-v_{t+1}\ge\tfrac12\log(c/2)-\tfrac12v_t$, i.e. $v_{t+1}\le\tfrac12v_t+\tfrac12\log(2/c)$. $\square$

**Lemma 7 (halving from above).** For every $t\ge0$, $v_{t+1}\ge\tfrac12v_t-b$.

*Proof.* By (1.1), $u_{t+1}\le g(u_t)=u_t+\sqrt{c\,u_t(1-u_t)}\le u_t+\sqrt c\sqrt{u_t}\le(1+\sqrt c)\sqrt{u_t}$, using $1-u_t\le1$ and $u_t\le\sqrt{u_t}$ for $u_t\in(0,1]$. Taking logarithms, $-v_{t+1}\le b-\tfrac12v_t$. $\square$

**Lemma 8 (iterating the halving).**

(a) If $m\ge1$ and $v_{t+1}\le\tfrac12v_t+a$ for $t=0,\dots,m-2$, then $v_{m-1}\le 2^{-(m-1)}v_0+2a^+$.

(b) If $v_{t+1}\ge\tfrac12v_t-b$ for $t=0,\dots,n-1$, then $v_n\ge2^{-n}v_0-2b$.

*Proof.* (a) We show by induction on $j\in\{0,\dots,m-1\}$ that $v_j\le2^{-j}v_0+a^+(2-2^{1-j})$. For $j=0$ both sides equal $v_0$. If it holds for $j\le m-2$, then $v_{j+1}\le\tfrac12v_j+a\le2^{-(j+1)}v_0+a^+(1-2^{-j})+a^+=2^{-(j+1)}v_0+a^+(2-2^{-j})$. Finally $a^+(2-2^{1-j})\le2a^+$.

(b) $v_{t+1}+2b\ge\tfrac12(v_t+2b)$ for each $t<n$, so $v_n+2b\ge2^{-n}(v_0+2b)\ge2^{-n}v_0$. $\square$

**Lemma 9 (number of small steps).** Let $m:=\#\{t<T:\ u_t<\theta_1\}$. Then $m\le\log_2^+v_0+1$.

*Proof.* Since $(u_t)$ is nondecreasing (Proposition 4(a)), $\{t<T:u_t<\theta_1\}=\{0,\dots,m-1\}$. If $m\le1$ the claim holds because $\log_2^+v_0\ge0$. Let $m\ge2$. For $t\le m-2$ we have $t+1\le m-1<T$ and $u_t<\theta_1\le\tfrac12$, so Lemma 6 gives $v_{t+1}\le\tfrac12v_t+a$. By Lemma 8(a), $v_{m-1}\le2^{-(m-1)}v_0+2a^+$. On the other hand $u_{m-1}<\theta_1$ gives $v_{m-1}>\log(1/\theta_1)=1+2a^+$ by (2.1). Hence $1<2^{-(m-1)}v_0$, i.e. $2^{m-1}<v_0$. In particular $v_0>1$, so $\log_2^+v_0=\log_2v_0>m-1$. $\square$

### 2.3 The middle steps: $\theta_1\le u_t<\rho$

**Lemma 10 (number of middle steps).** $\#\{t<T:\ \theta_1\le u_t<\rho\}\le1+(\rho-\theta_1)^+/\eta$.

*Proof.* Let $A_2$ be the set in question. If $A_2=\emptyset$ there is nothing to prove. Otherwise $\rho>\theta_1$, and since $(u_t)$ is nondecreasing, $A_2=\{t_1,t_1+1,\dots,t_2\}$ for some $t_1\le t_2<T$. For $t_1\le t<t_2$ we have $t+1\le t_2<T$, so $u_{t+1}=g(u_t)=u_t+\sqrt{c\,u_t(1-u_t)}$, and $u_t\ge\theta_1$, $1-u_t>1-\rho$ give $u_{t+1}\ge u_t+\eta$. Summing over $t=t_1,\dots,t_2-1$: $u_{t_2}\ge u_{t_1}+(t_2-t_1)\eta$. Since $u_{t_2}<\rho$ and $u_{t_1}\ge\theta_1$, $(t_2-t_1)\eta<\rho-\theta_1$, so $|A_2|=t_2-t_1+1<1+(\rho-\theta_1)/\eta$. $\square$

### 2.4 Upper and lower bounds on $T$

**Proposition 11 (upper bound; no condition on $u^\ast$).**
$$
T\le\log_2^+\log(1/u_0)+K_{\rm up}(c),\qquad K_{\rm up}(c):=3+\frac{(\rho-\theta_1)^+}{\eta}.
$$
*Proof.* Let $A_1=\{t<T:u_t<\theta_1\}$, $A_2=\{t<T:\theta_1\le u_t<\rho\}$, $A_3=\{t<T:u_t\ge\rho\}$. Every $t\in\{0,\dots,T-1\}$ lies in at least one of them (if $u_t<\theta_1$ it is in $A_1$; if $u_t\ge\rho$ in $A_3$; otherwise $\theta_1\le u_t<\rho$), so $T\le|A_1|+|A_2|+|A_3|$. By Lemma 5, any $t\in A_3$ satisfies $t=T-1$, so $|A_3|\le1$. Lemmas 9 and 10 bound $|A_1|$ and $|A_2|$:
$$
T\le\big(\log_2^+v_0+1\big)+\Big(1+\frac{(\rho-\theta_1)^+}{\eta}\Big)+1 .\qquad\square
$$

**Proposition 12 (lower bound; needs $u^\ast\ge\varepsilon$).** Let $\varepsilon\in(0,1)$ and $u^\ast\ge\varepsilon$. Then
$$
T\ge\log_2^+\log(1/u_0)-K_{\rm low}(c,\varepsilon),\qquad K_{\rm low}(c,\varepsilon):=\max\Big\{0,\ \log_2\big(\log(1/\varepsilon)+2\log(1+\sqrt c)\big)\Big\}.
$$
*Proof.* By Lemma 7 and Lemma 8(b) with $n=T$, $v_T\ge2^{-T}v_0-2b$. Since $u_T=u^\ast$ (Proposition 4(b),(c)) and $u^\ast\ge\varepsilon$, $v_T=\log(1/u^\ast)\le\log(1/\varepsilon)$. Hence $v_0\le2^T\big(\log(1/\varepsilon)+2b\big)$, where $\log(1/\varepsilon)+2b>0$. If $v_0\le1$, then $\log_2^+v_0=0\le T+K_{\rm low}$. If $v_0>1$, then $\log_2^+v_0=\log_2v_0\le T+\log_2(\log(1/\varepsilon)+2b)\le T+K_{\rm low}$. $\square$

**Theorem T4(ii).** For every $\varepsilon\in(0,1)$, whenever $u^\ast\ge\varepsilon$,
$$
\big|T-\log_2^+\log(1/u_0)\big|\le K(c,\varepsilon):=\max\{K_{\rm up}(c),\ K_{\rm low}(c,\varepsilon)\},
$$
with, explicitly,
$$
K_{\rm up}(c)=3+\Big(\frac1{1+c}-\theta_1\Big)^{+}\frac{\sqrt{(1+c)/\theta_1}}{c},\qquad \theta_1=e^{-1}\min\{1,c/2\},
$$
$$
K_{\rm low}(c,\varepsilon)=\max\Big\{0,\ \log_2\big(\log(1/\varepsilon)+2\log(1+\sqrt c)\big)\Big\}.
$$
Two simplifications: since $(\rho-\theta_1)^+\le\rho=1/(1+c)$ and $\theta_1=c/(2e)$ for $c\le2$, one has $K_{\rm up}(c)\le3+\sqrt{2e}\,c^{-3/2}(1+c)^{-1/2}$ for $c\le2$; and $K_{\rm up}(c)=3$ exactly for $c\ge c^*:=(\sqrt{1+8e}-1)/2\approx1.8847$, because $\rho\le\theta_1$ there (for $c^*\le c\le2$ this is $c(1+c)\ge2e$; for $c>2$, $\rho<1/3<e^{-1}=\theta_1$). At the paper's default $c=1/9$: $K_{\rm up}\approx61.4$ and $K_{\rm low}(1/9,\tfrac12)\approx0.34$.

*Proof.* Propositions 11 and 12. $\square$

**Remark 2.1 (the hypothesis $u^\ast\ge\varepsilon$ cannot be dropped).** The upper bound (Proposition 11) holds for all $u^\ast\in(u_0,1)$. The lower bound does not: take any $u_0\in(0,\rho)$ and $u^\ast:=g(u_0)<1$ (Lemma 5). Then $u^\ast=\min\{u^\ast,g(u_0)\}$, so $T=1$, while $\log_2^+\log(1/u_0)\to\infty$ as $u_0\to0$. So the two-sided bound with a $K$ independent of $u^\ast$ is false, and $\varepsilon$ enters only through $K_{\rm low}$.

**Remark 2.2 (the constant is not optimised).** $K_{\rm up}$ counts the middle phase with the crude additive increment $\eta$. Numerically (file `check_T4.py`, not a proof), at $c=1/9$ with $\ell_1=-\ell_0=\Delta/2$ and $\Delta=100\cdot2^k$, $k=0,\dots,7$, one finds $T-\log_2^+\log(1/u_0)=7.36$ in every case, far below $K_{\rm up}\approx61.4$. The note's figure $T=\log_2\Delta+6.36$ is the same observation, since $\log(1/u_0)=\log(1+e^{\Delta/2})\approx\Delta/2$; neither figure is claimed in the theorem.

**Corollary 13 (in terms of the log-mass deficit).** Let $\Delta_0:=\log\frac{q_0(0)}{q_0(1)}=\log\frac{1-u_0}{u_0}=-\ell_0$ be the start's log-mass deficit of the incoming state. If $\Delta_0\ge1$ and $u^\ast\ge\varepsilon$, then
$$
\big|T-\log_2\Delta_0\big|\le K(c,\varepsilon)+1 .
$$
*Proof.* $\log(1/u_0)=\log(1+e^{\Delta_0})$ and, for $x\ge0$, $x\le\log(1+e^x)\le x+\log2$. With $\Delta_0\ge1$, $\log(1/u_0)\ge1$, so $\log_2^+\log(1/u_0)=\log_2\log(1/u_0)\in[\log_2\Delta_0,\ \log_2(\Delta_0+\log2)]$, and $\log_2(\Delta_0+\log2)\le\log_2\Delta_0+\log_2(1+\log2)<\log_2\Delta_0+1$ because $1+\log2<2$. Combine with Theorem T4(ii). $\square$

This is the form used in the paper's introduction ("a switch with log-mass deficit $\Delta_0$ needs $\log_2\Delta_0+O(1)$ stages").

---

## 3. Part (iii): the path length

By Section 2, $\Lambda=\int_0^1\operatorname{sd}_{q_\phi}(d)\,d\phi$, where $d$ is the potential of the bridge; on $\{0,1\}$ it satisfies $d(1)-d(0)=\Delta$ by (0.1).

**Lemma 14.** $\operatorname{sd}_{q_\phi}(d)=\Delta\sqrt{u(\phi)(1-u(\phi))}$.

*Proof.* Under $q_\phi$, $d$ takes the value $d(1)$ with probability $u=u(\phi)$ and $d(0)$ with probability $1-u$. Its variance is $u(1-u)\big(d(1)-d(0)\big)^2=u(1-u)\Delta^2$ (variance of a two-point distribution). Take the square root; $\Delta>0$. $\square$

**Lemma 15 (antiderivative).** The function $F(\phi):=2\arcsin\sqrt{u(\phi)}$ is differentiable on $\mathbb R$ with $F'(\phi)=\Delta\sqrt{u(\phi)(1-u(\phi))}$.

*Proof.* $u(\phi)\in(0,1)$, so $\sqrt{u}\in(0,1)$ lies in the interior of the domain where $\arcsin$ is differentiable, with $\arcsin'(y)=(1-y^2)^{-1/2}$, and $(\sqrt u)'=u'/(2\sqrt u)$. By the chain rule and (0.2),
$$
F'=2\cdot\frac{1}{\sqrt{1-u}}\cdot\frac{u'}{2\sqrt u}=\frac{\Delta\,u(1-u)}{\sqrt{u(1-u)}}=\Delta\sqrt{u(1-u)}.\qquad\square
$$

**Proposition 16 (Part (iii), formula and bounds).**
$$
\Lambda=2\big\{\arcsin\sqrt{u^\ast}-\arcsin\sqrt{u_0}\big\},\qquad 0<\Lambda<\pi,\qquad \Lambda\le\pi\sqrt{u^\ast}.
$$
*Proof.* By Lemma 14 the integrand $\Delta\sqrt{u(1-u)}$ is continuous on $[0,1]$, and by Lemma 15 it is the derivative of $F$; the fundamental theorem of calculus gives $\Lambda=F(1)-F(0)$, which is the formula. Since $\arcsin$ is strictly increasing on $[0,1]$ with values in $[0,\pi/2]$, and $0<u_0<u^\ast<1$, we get $0<\Lambda<2(\pi/2-0)=\pi$. For the last bound we use $\arcsin y\le\tfrac{\pi}{2}y$ for $y\in[0,1]$: the function $\sin$ is concave on $[0,\pi/2]$ (it is $C^2$ on $\mathbb R$ with $\sin''=-\sin\le0$ there), so for $\theta\in[0,\pi/2]$, $\sin\theta=\sin\big((1-\tfrac{2\theta}{\pi})\cdot0+\tfrac{2\theta}{\pi}\cdot\tfrac{\pi}{2}\big)\ge(1-\tfrac{2\theta}{\pi})\sin0+\tfrac{2\theta}{\pi}\sin\tfrac{\pi}{2}=\tfrac{2\theta}{\pi}$; with $\theta=\arcsin y\in[0,\pi/2]$ this reads $y\ge\tfrac{2}{\pi}\arcsin y$. Hence $\Lambda\le2\arcsin\sqrt{u^\ast}\le\pi\sqrt{u^\ast}$. $\square$

**Proposition 17 ($T/\Lambda\to\infty$ as $u_0\to0$).** Fix $c>0$. For every $M>0$ there is $\delta_0=\delta_0(c,M)>0$ such that
$$
u_0<\delta_0\ \Longrightarrow\ T/\Lambda\ge M,\qquad\text{for every } u^\ast\in(u_0,1).
$$
In particular, for fixed $u^\ast$ (or for $u^\ast\ge\varepsilon$ fixed), $T/\Lambda\to\infty$ as $u_0\to0$.

*Proof.* Put $\varepsilon:=\min\{(\pi M)^{-2},\tfrac12\}\in(0,1)$ and $\delta_0:=\exp\big(-2^{\pi M+K(c,\varepsilon)}\big)$; note $\delta_0<e^{-1}$. Let $u_0<\delta_0$ and $u^\ast\in(u_0,1)$.

*Case $u^\ast\le\varepsilon$.* By Proposition 16, $\Lambda\le\pi\sqrt{u^\ast}\le\pi\sqrt\varepsilon\le1/M$, and $T\ge1$, so $T/\Lambda\ge M$.

*Case $u^\ast>\varepsilon$.* Since $u_0<\delta_0<e^{-1}$, $\log(1/u_0)>1$ and $\log_2^+\log(1/u_0)=\log_2\log(1/u_0)>\log_2\log(1/\delta_0)=\pi M+K(c,\varepsilon)$. By Theorem T4(ii), $T\ge\log_2^+\log(1/u_0)-K(c,\varepsilon)>\pi M$. By Proposition 16, $\Lambda<\pi$. Hence $T/\Lambda>M$. $\square$

This proves the final sentence of (iii): the path length stays below $\pi$, and when the endpoint is non-negligible ($u^\ast\ge\varepsilon$) the stage count grows like $\log_2\log(1/u_0)$ (Theorem T4(ii)), so $\Lambda$ does not govern $T$ at a switch. (audit 2026-10-15: without $u^\ast\ge\varepsilon$ only the upper bound on $T$ holds; Remark 2.1 gives $T=1$ for every small $u_0$. The uniform limit $T/\Lambda\to\infty$ still holds: for the endpoints of Remark 2.1, $u^\ast\to0$, so $\Lambda\to0$; for arbitrary endpoints it follows from the two-case argument of Proposition 17.)

---

## 4. Summary of the logical structure (for the Lean handoff)

Dependency graph (arrows = "uses"):

- Lemma 0 (properties of $u$) ← nothing.
- Lemma 1 ($\chi^2$ formula) ← nothing.
- Lemma 2 (two-point L4(i)) ← Lemmas 0, 1.
- Lemma 3 (one greedy step) ← Lemmas 0, 2; intermediate value theorem.
- Proposition 4 (recursion (1.1) $=$ schedule; $T<\infty$) ← Lemma 3; concavity of $x(1-x)$.
- Lemma 5 (final step) ← (1.1), Proposition 4(b),(c) ($T$ is the hitting time of $u^\ast$).
- Lemma 6 (halving from below) ← (1.1), Proposition 4(b).
- Lemma 7 (halving from above) ← (1.1) only.
- Lemma 8 (iteration) ← arithmetic.
- Lemma 9 (small steps) ← Proposition 4(a) (monotonicity), Lemmas 6, 8(a), identity (2.1).
- Lemma 10 (middle steps) ← (1.1), Proposition 4(a),(b).
- Proposition 11 (upper bound) ← Lemmas 5, 9, 10.
- Proposition 12 (lower bound) ← Lemmas 7, 8(b), Proposition 4(b),(c) ($u_T=u^\ast$).
- Theorem T4(ii) ← Propositions 11, 12. Corollary 13 ← T4(ii).
- Lemmas 14, 15 ← Lemma 0, (0.1). Proposition 16 ← Lemmas 14, 15, fundamental theorem of calculus, concavity of $\sin$ on $[0,\pi/2]$.
- Proposition 17 ← Theorem T4(ii), Proposition 16.

Every inequality is between explicit real numbers; the only analysis used is the intermediate value theorem (Lemma 3), the derivative of the logistic function and of $\arcsin$ (Lemmas 0, 15), the fundamental theorem of calculus for a continuous integrand (Proposition 16), and concavity of $\sin$ on $[0,\pi/2]$. Lean hazards to watch: $\log_2^+$ and $\max$; division by $u(1-u)>0$ (never zero because $u\in(0,1)$); $\sqrt{\cdot}$ of nonnegative quantities only; the hitting time $T$ as a `Nat.find` with the finiteness certificate of Proposition 4(b).

---

## 5. Hypotheses added, and steps to double-check

**Hypotheses added or made explicit (none beyond the statement, but the following interpretations were fixed):**

1. $T$ is read as $\min\{t\ge1:\phi_t=1\}$, i.e. the number of greedy stages (so $T=1$ if the first stage already reaches $\phi=1$). Proposition 4 shows this is well defined without invoking L4.
2. For part (iii), the two-point bridge is identified with a Section 2 bridge through (0.1): $d(1)-d(0)=\ell_1-\ell_0$. This is forced by the form $q_\phi(1)=\operatorname{logistic}(\ell_0+\phi(\ell_1-\ell_0))$; it is not an extra assumption, but it is the only way $d$ (hence $\operatorname{sd}_{q_\phi}(d)$ and $\Lambda$) enters.
3. "$T/\Lambda\to\infty$ as $u_0\to0$" is proved in the uniform form of Proposition 17 (uniform over $u^\ast\in(u_0,1)$), which contains the fixed-$u^\ast$ reading.
4. In (ii), the hypothesis $u^\ast\ge\varepsilon$ is used only for the lower bound; the upper bound holds for every $u^\ast$. Remark 2.1 shows the hypothesis is necessary for the two-sided statement.

**Steps I am not fully sure of:** none mathematically; every step above is elementary and was checked line by line. Two points deserve a second pair of eyes:

- The bookkeeping in Lemma 9 (the index range $t\le m-2$ on which Lemma 6 applies, and the use of $u_{m-1}<\theta_1$ to get $v_{m-1}>1+2a^+$), since off-by-one errors are the typical failure here.
- The explicit value of $K_{\rm up}$: it is correct but loose by roughly a factor of eight at $c=1/9$ (Remark 2.2). If a sharper constant is wanted, the middle phase can be counted multiplicatively ($u_{t+1}\ge(1+\sqrt c)u_t$ for $u_t\le\tfrac12$, and $1-u_{t+1}\le(1-\sqrt c)(1-u_t)$ for $\tfrac12\le u_t<\rho$ when $c<1$, both for untruncated steps $u_{t+1}=g(u_t)$, in particular for $t+1<T$; audit 2026-10-15: a step truncated at $u^\ast$ can violate both, e.g. $c=\tfrac19$ with $u_0=\tfrac14,u^\ast=0.26$, or $u_0=\tfrac12,u^\ast=0.51$), which I did not include to keep the proof minimal.

**Numerical checks performed (deterministic, local; `check_T4.py`):** the recursion (1.1) agrees with the schedule (0.3) computed directly by bisection on 175 parameter sets; the bound of Theorem T4(ii) with the explicit $K$ holds on 1593 parameter sets with $u_0$ down to $10^{-256}$ and no violation; the formula of Proposition 16 agrees with numerical integration to six decimals; the note's table at $c=1/9$ is reproduced. These checks support the proof but are not part of it.

---

## 6. Review record

Two blind, independent correctness reviewers (Opus 5.5, xhigh effort; angle A line by line, angle C adversarial) read the pre-review version (`review/PROOF_v1_prereview.md`) and only the frozen statement. Both verdicts: *every step verified*; no fatal finding, no gap. Their reports are `review/REVIEW_A_opus.md` and `review/REVIEW_C_opus.md` (with `review/REVIEW_C_check.py`). Reviewer C recomputed the schedule from its definition with multiprecision arithmetic, with $u_0$ as small as $\exp(-10^{5000})$ in log space and about $7\times10^6$ adversarial parameter triples, and found no violation of (ii); it also reports that $K_{\rm low}$ is asymptotically sharp and that the true excess of $T$ over $\log_2^+\log(1/u_0)$ behaves like $\pi/\sqrt c$ for small $c$ (numerical, unproved), far below $K_{\rm up}$.

Findings and rulings (all exposition; all accepted and applied in this version): the endpoint $u(1)$ is now written $u^\ast$ to avoid the clash with the sequence element $u_1$ (A-F1); symbols $m$, $A$, $\delta$ reused with two meanings were renamed (A-F2, C-F4); "equivalently" corrected to "in particular" in Lemma 2(a) (A-F3, C-F3); a self-contradictory sentence in Proposition 4(b) deleted (A-F4, C-F1); the induction in Proposition 4(c) now carries $\phi_t\in[0,1)$ (A-F5); the bound $\arcsin y\le\pi y/2$ is now derived from the concavity of $\sin$ on the closed interval, where the second derivative exists (A-F6, C-F2); the simplified forms of $K_{\rm up}$ replaced by sharper correct ones, including $K_{\rm up}=3$ for $c\ge c^*$ (A-F7, C-F6); the dependency graph completed and the superfluous hypothesis $t<T$ dropped from Lemma 7 (A-F8, C-F5). References to the draft's prover note and to `check_T4.py` (A-F9, C-F7) carry no step of the proof and were left as informational. Not run in this thread: the Astra reviewers of the theorem-proving protocol.

---

## Audit revisions (2026-10-15)

Adjudicator B (Opus 5.5), after the GPT-6.1 Sol audit (`proofs/_audit/T4/SOL_AUDIT.md`, verdict VERIFIED). The pre-audit text is saved as `PROOF_pre_audit.md`. Rulings are in `proofs/_audit/group_B/RULINGS.md`. No step of the proof changed.

1. **Section 3, sentence after Proposition 17.** Two-sided growth $T\sim\log_2\log(1/u_0)$ is now stated under $u^\ast\ge\varepsilon$. Without it only the upper bound holds, and the uniform limit $T/\Lambda\to\infty$ survives by the two-case argument of Proposition 17 (for the endpoints of Remark 2.1, $u^\ast\to0$ and so $\Lambda\to0$). (Sol finding 1.)
2. **Section 5, optional multiplicative bounds.** They are restricted to untruncated steps $u_{t+1}=g(u_t)$, with Sol's two counterexamples for truncated steps. These bounds are not used in the proof. (Sol finding 2.)

Checks: `check_T4.py` rerun unchanged (`proofs/_audit/group_B/rerun_check_T4.out`): recursion versus definition, 175 cases, 0 mismatches; stage bound, 1593 cases, 0 violations; upper bound without $\varepsilon$, 0 violations; path-length formula agrees with numerical integration to six decimals; offset $7.356$ at $c=1/9$ reproduced. New checks T4.F2 in `proofs/_audit/group_B/check_audit_B.py` PASS.

3. **After Sol's confirmation (exchange 1).** Sol gave the verdict VERIFIED. As it asked, the justification of the uniform limit in item 1 and in Section 3 now cites Proposition 17's two-case argument rather than $\Lambda\le\pi\sqrt{u^st}	o0$, which needs $u^st	o0$. This edit was not re-sent for confirmation.
