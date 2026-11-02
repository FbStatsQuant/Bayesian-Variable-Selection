# Proof of Proposition P2 (several switches)

Thread: P2. Prover: Fable 5.1 (lead), 15 October 2026. Status: v4, final (2026-10-15). v1, v2, v3 each reviewed by six blind reviewers (3 Opus xhigh, 3 GPT-6 Astra xhigh); every finding accepted and fixed; v4 differs from v3 by wording only (FINDINGS.md, round 3). Not adopted by the author..

Read-only inputs: `paper_draft/paper_draft.tex` (statement of P2 and its note; definitions of Section 2), `proofs/T4/PROOF.md`, `proofs/foundations/PROOF.md` (L4), `proofs/elementary_I/PROOF.md` (L3, L5, L7).

---

## 0. Setting, conventions and the frozen statement

### 0.1 The statement, verbatim from the draft

> **Proposition (P2 · Several switches).** Let $\mathcal A_1,\dots,\mathcal A_K$ partition the model space, with $K$ fixed. Write $u_k(\phi)=q_\phi(\mathcal A_k)$ and $q^k_\phi=q_\phi(\cdot\mid\mathcal A_k)$. Assume:
>
> (M1) each $u_k$ is piecewise monotone on $[0,1]$, with at most $J$ monotone pieces;
>
> (M2) $d$ is locally sub-Gaussian under every $q_\phi^k$, in the sense of Lemma L5, with constants $(\sigma_w,\lambda_0)$.
>
> Let $\mathcal U$ be the set of pairs $(k,\phi^\ast)$ at which $u_k$ starts an increasing piece, and let $c'=\sqrt{1+c}-1$. Then
> $$T\le\Big\lceil\max\{1/\lambda_0,\sigma_w\sqrt{2/\log(1+c')}\}\Big\rceil+\sum_{(k,\phi^\ast)\in\mathcal U}\log_2^+\log\frac1{u_k(\phi^\ast)}+K_1(c,K,J).$$

The draft's note adds: the key identity $1+\chi^2(q'\|q)=\sum_k\frac{u_k'^2}{u_k}(1+\chi^2(q'^k\|q^k))\le(1+\max_k\chi^2_k)(1+\chi^2(u'\|u))$; within-mode steps are counted by L5 and mixture steps by a $K$-category version of T4, decreasing pieces contributing $O(1)$ each; the open step is the additivity of the two counts, which "needs a monotonicity property of the mixture $\chi^2$ in its starting point, analogous to L4(ii)"; and the non-monotone example $\mathcal A_1=\{a,c\}$, $\mathcal A_2=\{b\}$, $\gamma_0\propto(1,\varepsilon,\varepsilon^2)$, $d=(0,D,2D)$, $u_1=(1+x^2)/(1+x+x^2)$ with $x=\varepsilon e^{\phi D}$.

### 0.2 The abstract setting

As in `foundations/PROOF.md` §0.1 and `elementary_I/PROOF.md` §0.1, the model space is a nonempty finite set $\mathcal S$ with $\gamma_0:\mathcal S\to(0,\infty)$ and $d:\mathcal S\to\mathbb R$; nothing below uses their regression form. For $\phi\in\mathbb R$,
$$
\gamma_\phi(S)=\gamma_0(S)e^{\phi d(S)},\qquad \bar Z_\phi=\sum_{S\in\mathcal S}\gamma_\phi(S),\qquad q_\phi=\gamma_\phi/\bar Z_\phi,\qquad F(\phi)=\log\bar Z_\phi .
$$
$q_\phi(S)>0$ for every $S$ and $\phi$. For probabilities $q',q$ on a finite set with $q>0$, $\chi^2(q'\|q)=\sum_Sq'(S)^2/q(S)-1\ge0$.

**The partition.** $\mathcal A_1,\dots,\mathcal A_K$ are nonempty, pairwise disjoint, with union $\mathcal S$ (Reading R1). For $\phi\in\mathbb R$ and $k\in[K]:=\{1,\dots,K\}$,
$$
\bar Z^k_\phi:=\sum_{S\in\mathcal A_k}\gamma_\phi(S)>0,\qquad u_k(\phi):=q_\phi(\mathcal A_k)=\frac{\bar Z^k_\phi}{\bar Z_\phi},\qquad q^k_\phi(S):=q_\phi(S\mid\mathcal A_k)=\frac{\gamma_\phi(S)}{\bar Z^k_\phi}\quad(S\in\mathcal A_k). \tag{0.1}
$$
Thus $u(\phi)=(u_1(\phi),\dots,u_K(\phi))$ is a probability vector on $[K]$ with every entry in $(0,1]$, and in $(0,1)$ when $K\ge2$; each $u_k$ is $C^\infty$ on $\mathbb R$ (a ratio of finite positive sums of exponentials of $\phi$); and $q^k_\phi$ is itself the bridge built from the restrictions $\gamma_0|_{\mathcal A_k}$ and $d|_{\mathcal A_k}$ on the finite set $\mathcal A_k$. In particular, for every $\phi,\delta\in\mathbb R$ and $S\in\mathcal A_k$,
$$
q^k_{\phi+\delta}(S)=\frac{q^k_\phi(S)\,e^{\delta d(S)}}{\mathbb E_{q^k_\phi}e^{\delta d}} , \tag{0.2}
$$
because $\gamma_{\phi+\delta}=\gamma_\phi e^{\delta d}$ and $\bar Z^k_{\phi+\delta}=\sum_{S\in\mathcal A_k}\gamma_\phi(S)e^{\delta d(S)}=\bar Z^k_\phi\,\mathbb E_{q^k_\phi}e^{\delta d}$.

**The greedy schedule.** Fix $\rho\in(0,1)$ and $c=\rho^{-1}-1>0$. Put $\phi_0=0$ and, as long as $\phi_{t-1}<1$,
$$
\Phi_t:=\{\phi\in(\phi_{t-1},1]:\chi^2(q_\phi\|q_{\phi_{t-1}})\le c\},\qquad \phi_t:=\sup\Phi_t,\qquad T:=\min\{t\ge1:\phi_t=1\}. \tag{0.3}
$$
By L4(iii) (`foundations/PROOF.md`, Theorem 2.4(a),(b)), $\Phi_t$ is nonempty and contains its supremum, $\phi_t>\phi_{t-1}$, and $T<\infty$. Hence $0=\phi_0<\phi_1<\dots<\phi_T=1$ and $\chi^2(q_{\phi_t}\|q_{\phi_{t-1}})\le c$ for every $t\le T$.

**Constants.** $c':=\sqrt{1+c}-1>0$, so that $(1+c')^2=1+c$. Further,
$$
c'':=\frac{c'}{K},\qquad a:=\tfrac12\log\frac1{c''},\qquad a^+:=\max\{a,0\},\qquad \theta:=e^{-(1+2a^+)}=e^{-1}\min\{1,c''\}\in(0,e^{-1}], \tag{0.4}
$$
$$
C_{\rm inc}(c''):=2+\frac{1-\theta}{\sqrt{c''\theta}},\qquad C_{\rm dec}(c''):=\frac1{c''},\qquad \log_2^+x:=\log_2\max\{x,1\}\ (x\ge0),\ \text{so }\log_2^+0=0. \tag{0.5}
$$
(For (0.4): if $c''\le1$ then $a\ge0$ and $e^{-(1+2a)}=e^{-1}c''$; if $c''>1$ then $a<0$ and $\theta=e^{-1}$.) The function $x\mapsto\log_2^+\log(1/x)$ is defined and nonincreasing on $(0,1]$ and vanishes on $[e^{-1},1]$; in particular it is $0$ at $x=1$.

### 0.3 Readings adopted (flagged)

- **R1 (nonempty parts).** Every $\mathcal A_k$ is nonempty; otherwise $u_k\equiv0$, $q^k_\phi$ is undefined and (M2) is void for that $k$. An empty part can simply be dropped, which lowers $K$.
- **R2 (pieces).** (M1) is read as: for each $k$ there are an integer $J_k\in[J]$ and breakpoints $0=a^k_0<a^k_1<\dots<a^k_{J_k}=1$ such that on each closed piece $[a^k_{i-1},a^k_i]$ the function $u_k$ is monotone (since $u_k$ is continuous, monotonicity on an open piece extends to its closure, so closed pieces are no restriction), and each piece is *declared* nondecreasing or nonincreasing, consistently with its monotonicity (a constant piece may be declared either way). One such decomposition with its declarations is fixed for each $k$. Then $\mathcal U$ is the set of pairs $(k,a^k_{i-1})$ over the pieces declared nondecreasing, and $J$ bounds every $J_k$. The *interior* breakpoints are the labelled pairs $(k,i)$ with $1\le i\le J_k-1$, with value $a^k_i$; there are $\sum_k(J_k-1)\le K(J-1)$ of them (different $k$ may share a value, so the set of distinct values has at most this many elements).
- **R3 (M2).** For every $k\in[K]$, every $\phi\in[0,1]$ and every $\lambda\in[0,2\lambda_0]$, with $U^k_\phi:=d-\mathbb E_{q^k_\phi}d$ on $\mathcal A_k$,
$$
\log\mathbb E_{q^k_\phi}e^{\lambda U^k_\phi}\le\frac{\lambda^2\sigma_w^2}2,\qquad \sigma_w>0,\ \lambda_0>0 . \tag{M2}
$$
This is the hypothesis (8.1) of L5 in `elementary_I/PROOF.md` for the bridge $q^k$ on $\mathcal A_k$, with $\sigma_d=\sigma_w$.
- **R4 ($T$).** $T$ is the stage count (0.3) of the greedy population-ESS schedule with threshold $c$ on the full bridge $q_\phi$, as in Section 2 of the draft.
- **R5 ($K=1$).** Then $u_1\equiv1$; whatever decomposition R2 fixes, every pair $(1,\phi^\ast)\in\mathcal U$ contributes $\log_2^+\log(1/u_1(\phi^\ast))=\log_2^+0=0$, so the sum over $\mathcal U$ is $0$; and the mixture $\chi^2$ is identically $0$. The statement reduces to L5 and the proof below covers it.

### 0.4 What is proved

**Theorem 0.1 (P2, with $K_1$ explicit).** Under R1–R4, (M1) and (M2),
$$
T\le\Big\lceil\max\Big\{\frac1{\lambda_0},\ \sigma_w\sqrt{\frac2{\log(1+c')}}\Big\}\Big\rceil+\sum_{(k,\phi^\ast)\in\mathcal U}\log_2^+\log\frac1{u_k(\phi^\ast)}+K_1(c,K,J),
$$
$$
K_1(c,K,J):=1+K(J-1)+KJ\,C_{\rm inc}(c'')=1+K(J-1)+KJ\Big[2+\frac{1-\theta}{\sqrt{c''\theta}}\Big],\qquad c''=\frac{\sqrt{1+c}-1}{K},\quad\theta=e^{-1}\min\{1,c''\}.
$$
More precisely (Theorem 4.2), $T\le1+|W|+|M|$, where $W$ is the set of greedy steps on which some within-mode $\chi^2$ is at least $c'$ and $M$ the set of greedy steps on which the mixture $\chi^2$ is at least $c'$; $|W|$ is bounded by the first term (Proposition 3.2) and $|M|$ by the sum plus $K_1-1$ (Theorem 2.7).

Numerically, at the paper's default $c=1/9$: $c'=0.054093$; for $K=2$, $c''=0.027046$, $\theta=0.0099498$, $C_{\rm inc}=62.35$ and $K_1(1/9,2,1)=125.7$, $K_1(1/9,2,2)=252.4$. The constant is not optimised (Remark 4.5).

**Structure.** §1 the mixture identity; §2 a $K$-category version of T4 along an *arbitrary* increasing sequence; §3 the within-mode count; §4 the assembly, where the two counts are added. The addition needs no monotonicity of the mixture $\chi^2$ in its starting point; Remark 4.3 shows that such monotonicity is false in general, with the note's own example.

---

## 1. Step 1: the mixture identity and its inequality

**Lemma 1.1 (mixture identity).** Let $q',q$ be probabilities on $\mathcal S$ with $q>0$. Write $u_k=q(\mathcal A_k)$, $u'_k=q'(\mathcal A_k)$, $q^k=q(\cdot\mid\mathcal A_k)$, and, when $u'_k>0$, $q'^k=q'(\cdot\mid\mathcal A_k)$. Then
$$
1+\chi^2(q'\|q)=\sum_{k:\,u'_k>0}\frac{u_k'^2}{u_k}\big(1+\chi^2(q'^k\|q^k)\big). \tag{1.1}
$$
If moreover $u'_k>0$ for every $k$, then
$$
1+\chi^2(q'\|q)\le\Big(1+\max_{k\in[K]}\chi^2(q'^k\|q^k)\Big)\big(1+\chi^2(u'\|u)\big), \tag{1.2}
$$
where $\chi^2(u'\|u)=\sum_ku_k'^2/u_k-1=\sum_k(u'_k-u_k)^2/u_k$ is the $\chi^2$ divergence between the two probability vectors on $[K]$.

*Proof.* Since the $\mathcal A_k$ partition $\mathcal S$, $1+\chi^2(q'\|q)=\sum_k\sum_{S\in\mathcal A_k}q'(S)^2/q(S)$. For $S\in\mathcal A_k$, $q(S)=u_kq^k(S)$ with $u_k>0$ (as $q>0$ and $\mathcal A_k\ne\emptyset$); and $q'(S)=u'_kq'^k(S)$ when $u'_k>0$, while $q'(S)=0$ for all $S\in\mathcal A_k$ when $u'_k=0$. Hence, when $u'_k>0$,
$$
\sum_{S\in\mathcal A_k}\frac{q'(S)^2}{q(S)}=\frac{u_k'^2}{u_k}\sum_{S\in\mathcal A_k}\frac{q'^k(S)^2}{q^k(S)}=\frac{u_k'^2}{u_k}\big(1+\chi^2(q'^k\|q^k)\big),
$$
and the inner sum is $0$ when $u'_k=0$. Summing over $k$ gives (1.1). For (1.2), bound each factor $1+\chi^2(q'^k\|q^k)$ by the maximum over $k$ and use $\sum_ku_k'^2/u_k=1+\chi^2(u'\|u)$. The last expression for $\chi^2(u'\|u)$: $\sum_k(u'_k-u_k)^2/u_k=\sum_ku_k'^2/u_k-2\sum_ku'_k+\sum_ku_k=\sum_ku_k'^2/u_k-1$, since both vectors sum to $1$. $\square$

**Corollary 1.2 (the two budgets).** For real $\phi<\phi'$ put
$$
\chi^2_{k}(\phi,\phi'):=\chi^2(q^k_{\phi'}\|q^k_\phi)\quad(k\in[K]),\qquad \chi^2_{\rm mix}(\phi,\phi'):=\chi^2\big(u(\phi')\,\|\,u(\phi)\big).
$$
If $\max_k\chi^2_k(\phi,\phi')<c'$ and $\chi^2_{\rm mix}(\phi,\phi')<c'$, then $\chi^2(q_{\phi'}\|q_\phi)<c$. Equivalently: if $\chi^2(q_{\phi'}\|q_\phi)\ge c$, then $\max_k\chi^2_k(\phi,\phi')\ge c'$ or $\chi^2_{\rm mix}(\phi,\phi')\ge c'$.

*Proof.* Apply (1.2) with $q=q_\phi$ and $q'=q_{\phi'}$; all $u'_k=u_k(\phi')>0$ by R1. Then $1+\chi^2(q_{\phi'}\|q_\phi)<(1+c')(1+c')=1+c$. $\square$

*Remark 1.3.* The inequality (1.2) is the one in the draft's note; it is not an equality in general. The mixture divergence $\chi^2(u(\phi+\delta)\|u(\phi))$ (defined for all real $\phi,\delta$, since $u>0$ on $\mathbb R$) is in general **not** of the L4(i) form $\exp\{G(\phi+2\delta)+G(\phi)-2G(\phi+\delta)\}-1$ with a single convex $G:\mathbb R\to\mathbb R$ for all real $\phi,\delta$: each $u_k(\phi)=\bar Z^k_\phi/\bar Z_\phi$ is a ratio of two sums of exponentials of $\phi$, and such a vector need not be an exponential family in $\phi$ (an exponential family $u_k\propto\alpha_ke^{\phi t_k}$ would have the form with $G=\log\sum_k\alpha_ke^{\phi t_k}$; that the form can fail is shown below). (It is one when $d$ is constant on every part, say $d\equiv d_k$ on $\mathcal A_k$: then $\bar Z^k_\phi=\bar Z^k_0e^{\phi d_k}$, $u_k(\phi)\propto\bar Z^k_0e^{\phi d_k}$, and the form holds with $G=F$, since $\sum_k\bar Z^k_0e^{\phi d_k}=\bar Z_\phi$; $F$ is convex by L4. Singleton parts are a special case.) That the form fails in general follows from Remark 4.3: if it held, then for fixed $\phi_b$ the exponent of $1+\chi^2(u(\phi_b)\|u(\phi))$ would be $\Gamma(\phi)-2G(\phi_b)$ with $\Gamma(\phi):=G(\phi)+G(2\phi_b-\phi)$, a convex function symmetric about $\phi_b$, hence nonincreasing on $(-\infty,\phi_b]$; so $\phi\mapsto\chi^2(u(\phi_b)\|u(\phi))$ would be nonincreasing on $(-\infty,\phi_b]$, which Remark 4.3 refutes with $\phi_b=1$ and the starting points $0$ and $\tfrac12$. (The same refutation with $\phi_b=\tfrac12+h$ and starting points $\tfrac12-h$, $\tfrac12$, for $0<h\le\tfrac16$, keeps every argument of $G$ inside $[0,1]$, so even a $G$ convex on $[0,1]$ only, with the form assumed only for arguments in $[0,1]$, is ruled out.) So L4 cannot be applied to the mixture weights, and §2 handles them along arbitrary sequences of points instead.

---

## 2. Step 2: a $K$-category version of T4 along an arbitrary increasing sequence

Throughout this section only (M1) is used, in the form R2, together with $u_k(\phi)\in(0,1)$ for all $\phi\in[0,1]$ when $K\ge2$. The threshold is an arbitrary $\tau>0$, and $c'':=\tau/K$; in §4, $\tau=c'$, which gives the $c''$ of (0.4). The constants $a,a^+,\theta,C_{\rm inc},C_{\rm dec}$ are those of (0.4)–(0.5) computed from this $c''$.

**Definition 2.1.** Let $0\le\psi_0<\psi_1<\dots<\psi_m\le1$ be a finite strictly increasing sequence; its *steps* are $t\in[m]$, with closed interval $[\psi_{t-1},\psi_t]$ and open interval $(\psi_{t-1},\psi_t)$. A step $t$ is
- *clean* if no interior breakpoint location $a^k_i$ ($k\in[K]$, $1\le i\le J_k-1$) lies in $(\psi_{t-1},\psi_t)$;
- *$k$-active* ($k\in[K]$) if $\dfrac{\big(u_k(\psi_t)-u_k(\psi_{t-1})\big)^2}{u_k(\psi_{t-1})}\ge c''$;
- a *mixture step* if $\chi^2\big(u(\psi_t)\|u(\psi_{t-1})\big)\ge\tau$.

**Lemma 2.2 (pigeonhole).** Every mixture step is $k$-active for at least one $k\in[K]$.

*Proof.* By Lemma 1.1, $\chi^2(u(\psi_t)\|u(\psi_{t-1}))=\sum_{k=1}^K\big(u_k(\psi_t)-u_k(\psi_{t-1})\big)^2/u_k(\psi_{t-1})$. If every term were $<c''$ the sum would be $<Kc''=\tau$. $\square$

**Lemma 2.3 (non-clean steps).** The number of non-clean steps is at most $\sum_k(J_k-1)\le K(J-1)$.

*Proof.* The open intervals $(\psi_{t-1},\psi_t)$, $t\in[m]$, are pairwise disjoint. Choose for each non-clean step one labelled interior breakpoint $(k,i)$ whose value $a^k_i$ lies in its open interval; distinct steps receive distinct labels, because a given value lies in at most one of the disjoint open intervals. This injects the non-clean steps into the set of labelled interior breakpoints, which has $\sum_k(J_k-1)$ elements. $\square$

**Lemma 2.4 (a clean step lies in one piece of each $u_k$).** Let $t$ be a clean step and $k\in[K]$. Then there is a unique $i=i_k(t)\in[J_k]$ with $(\psi_{t-1},\psi_t)\subseteq(a^k_{i-1},a^k_i)$, and then $[\psi_{t-1},\psi_t]\subseteq[a^k_{i-1},a^k_i]$; so $u_k$ is monotone on $[\psi_{t-1},\psi_t]$, in the direction declared for piece $i$.

*Proof.* Pick $x\in(\psi_{t-1},\psi_t)$ (the interval is nonempty). Since $x\in(0,1)$ and $x$ is not an interior breakpoint location of $u_k$ (the step is clean), $x$ lies in exactly one open piece $(a^k_{i-1},a^k_i)$ of $u_k$. If some $y\in(\psi_{t-1},\psi_t)$ lay in a different open piece of $u_k$, an interior breakpoint location of $u_k$ would lie strictly between $x$ and $y$, hence in $(\psi_{t-1},\psi_t)$, contradicting cleanness. So $(\psi_{t-1},\psi_t)\subseteq(a^k_{i-1},a^k_i)$; taking closures, $[\psi_{t-1},\psi_t]\subseteq[a^k_{i-1},a^k_i]$. Uniqueness of $i$: the open pieces are pairwise disjoint and $(\psi_{t-1},\psi_t)\neq\emptyset$. $\square$

**Proposition 2.5 (active steps on one piece).** Let $K\ge2$. Fix $k\in[K]$ and a piece $i\in[J_k]$, with $\phi^\ast:=a^k_{i-1}$. Let $t_1<t_2<\dots<t_n$ be clean $k$-active steps with $i_k(t_j)=i$ for all $j$ (any such collection, possibly empty, $n\ge0$), and for $n\ge1$ put $w_j:=u_k(\psi_{t_j-1})$, $v_j:=u_k(\psi_{t_j})$; all of these lie in $(0,1)$.

(a) If $u_k$ is nondecreasing on $[a^k_{i-1},a^k_i]$, then
$$
n\le\log_2^+\log\frac1{u_k(\phi^\ast)}+C_{\rm inc}(c''),\qquad C_{\rm inc}(c'')=2+\frac{1-\theta}{\sqrt{c''\theta}} .
$$

(b) If $u_k$ is nonincreasing on $[a^k_{i-1},a^k_i]$, then $n<C_{\rm dec}(c'')=1/c''$.

*Proof.* If $n=0$ there is nothing to prove in either part, both right-hand sides being positive; let $n\ge1$. By Lemma 2.4 each closed interval $[\psi_{t_j-1},\psi_{t_j}]$ lies in $[a^k_{i-1},a^k_i]$, where $u_k$ is monotone. For $j<n$, $t_j\le t_{j+1}-1$ gives $\psi_{t_j}\le\psi_{t_{j+1}-1}$, and both points lie in the piece (the first as a right endpoint, the second as a left endpoint). Also $a^k_{i-1}=\phi^\ast\le\psi_{t_1-1}$.

(a) Monotonicity (nondecreasing) gives $w_j\le v_j$, $v_j\le w_{j+1}$ for $j<n$, and $u_k(\phi^\ast)\le w_1$. The $k$-activity of $t_j$ reads $(v_j-w_j)^2\ge c''w_j$, and as $v_j-w_j\ge0$, $v_j\ge w_j+\sqrt{c''w_j}$. Hence
$$
w_{j+1}\ge w_j+\sqrt{c''\,w_j}\quad(1\le j<n),\qquad w_1\ge u_k(\phi^\ast),\qquad w_j<1\ \ (j\in[n]). \tag{2.1}
$$
In particular $(w_j)$ is nondecreasing. Write $\ell_j:=\log(1/w_j)>0$.

*Phase 1 (small values).* Let $n_1:=\#\{j\in[n]:w_j<\theta\}$; by monotonicity of $(w_j)$, $\{j:w_j<\theta\}=\{1,\dots,n_1\}$. We claim
$$
n_1\le1+\log_2^+\ell_1 . \tag{2.2}
$$
If $n_1\le1$ this holds because $\log_2^+\ell_1\ge0$. Let $n_1\ge2$. For $1\le j\le n_1-1$ (so $j<n$), (2.1) gives $w_{j+1}\ge\sqrt{c''w_j}$, i.e. $\ell_{j+1}\le\tfrac12\ell_j+a$ with $a=\tfrac12\log(1/c'')$. By induction on $j\in[n_1]$, $\ell_j\le2^{-(j-1)}\ell_1+a^+(2-2^{2-j})$: for $j=1$ both sides equal $\ell_1$; and if it holds for some $j\le n_1-1$ then $\ell_{j+1}\le\tfrac12\ell_j+a\le2^{-j}\ell_1+a^+(1-2^{1-j})+a^+=2^{-j}\ell_1+a^+(2-2^{1-j})$, which is the claim at $j+1$. At $j=n_1$: $\ell_{n_1}\le2^{-(n_1-1)}\ell_1+2a^+$. But $w_{n_1}<\theta$ means $\ell_{n_1}>\log(1/\theta)=1+2a^+$ by (0.4). Hence $2^{-(n_1-1)}\ell_1>1$, i.e. $\ell_1>2^{n_1-1}\ge2$, so $\log_2^+\ell_1=\log_2\ell_1>n_1-1$, which is (2.2).

*Phase 2 (values at least $\theta$).* Let $n_2:=n-n_1=\#\{j\in[n]:w_j\ge\theta\}$, the indices $j=n_1+1,\dots,n$. We claim
$$
n_2\le1+\frac{1-\theta}{\sqrt{c''\theta}} . \tag{2.3}
$$
If $n_2\le1$ this is clear. Let $n_2\ge2$. For $n_1+1\le j\le n-1$, (2.1) and $w_j\ge\theta$ give $w_{j+1}\ge w_j+\sqrt{c''\theta}$. Summing over these $j$, $w_n\ge w_{n_1+1}+(n_2-1)\sqrt{c''\theta}\ge\theta+(n_2-1)\sqrt{c''\theta}$. Since $w_n<1$, $(n_2-1)\sqrt{c''\theta}<1-\theta$, which is (2.3).

*Conclusion.* $n=n_1+n_2\le\log_2^+\ell_1+2+(1-\theta)/\sqrt{c''\theta}$, and $\log_2^+\ell_1=\log_2^+\log(1/w_1)\le\log_2^+\log(1/u_k(\phi^\ast))$ because $w_1\ge u_k(\phi^\ast)$ and $x\mapsto\log_2^+\log(1/x)$ is nonincreasing.

(b) Monotonicity (nonincreasing) gives $v_j\le w_j$ and $w_{j+1}\le v_j$ for $j<n$. The $k$-activity of $t_j$ reads $(w_j-v_j)^2\ge c''w_j$, and as $w_j-v_j\ge0$, $w_j-v_j\ge\sqrt{c''w_j}$. Since $v_j>0$, $w_j>w_j-v_j\ge\sqrt{c''w_j}$, so $\sqrt{w_j}>\sqrt{c''}$, i.e. $w_j>c''$, and then $w_j-v_j\ge\sqrt{c''w_j}>c''$. Therefore $w_{j+1}\le v_j<w_j-c''$ for $j<n$. If $n=1$: $c''<w_1<1$ gives $n=1<1/c''$. If $n\ge2$: iterating the strict inequality $n-1$ times, $w_n<w_1-(n-1)c''$; with $w_n>c''$ and $w_1<1$ this gives $nc''<1$, i.e. $n<1/c''$. $\square$

**Lemma 2.6 ($C_{\rm dec}\le C_{\rm inc}$).** For every $c''>0$, $1/c''\le C_{\rm inc}(c'')$.

*Proof.* If $c''\le1$, then $\theta=c''/e$ and $\dfrac{1-\theta}{\sqrt{c''\theta}}=\dfrac{(1-c''/e)\sqrt e}{c''}\ge\dfrac{(1-1/e)\sqrt e}{c''}=\dfrac{\sqrt e-e^{-1/2}}{c''}>\dfrac1{c''}$, since $\sqrt e-e^{-1/2}\approx1.042>1$ (indeed $\sqrt e>1.64$ and $e^{-1/2}<0.61$). If $c''>1$, then $1/c''<1<2\le C_{\rm inc}(c'')$. $\square$

**Theorem 2.7 ($K$-category T4).** Assume (M1) in the form R2, let $\tau>0$ and $c''=\tau/K$. For every finite strictly increasing sequence $0\le\psi_0<\psi_1<\dots<\psi_m\le1$,
$$
\#\big\{t\in[m]:\ \chi^2\big(u(\psi_t)\|u(\psi_{t-1})\big)\ge\tau\big\}\ \le\ \sum_{(k,\phi^\ast)\in\mathcal U}\log_2^+\log\frac1{u_k(\phi^\ast)}+\sum_{k=1}^K(J_k-1)+\Big(\sum_{k=1}^KJ_k\Big)C_{\rm inc}(c'')
\ \le\ \sum_{(k,\phi^\ast)\in\mathcal U}\log_2^+\log\frac1{u_k(\phi^\ast)}+K(J-1)+KJ\,C_{\rm inc}(c'') . \tag{2.4}
$$

*Proof.* If $K=1$, $u\equiv(1)$ and no step is a mixture step; the right side is $\ge0$. Let $K\ge2$, so every $u_k$ takes values in $(0,1)$ on $[0,1]$. Each mixture step is non-clean or clean. By Lemma 2.3 the non-clean steps number at most $\sum_k(J_k-1)$. Assign to each clean mixture step $t$ a pair $(k,i)$: $k$ is the smallest index for which $t$ is $k$-active (it exists by Lemma 2.2) and $i=i_k(t)$ (Lemma 2.4). The steps assigned to a given $(k,i)$ form a collection of clean $k$-active steps lying in piece $i$ of $u_k$, so Proposition 2.5 applies to them: if piece $i$ is declared nondecreasing they number at most $\log_2^+\log(1/u_k(a^k_{i-1}))+C_{\rm inc}(c'')$, and the pair $(k,a^k_{i-1})$ belongs to $\mathcal U$; if it is declared nonincreasing they number less than $C_{\rm dec}(c'')\le C_{\rm inc}(c'')$ (Lemma 2.6). Summing over the $\sum_kJ_k$ pieces and adding the non-clean steps gives the first inequality in (2.4); the second uses $J_k\le J$. $\square$

*Remark 2.8 (relation to T4).* For $K=2$ the mixture $\chi^2$ between the probability vectors $(1-w,w)$ and $(1-v,v)$ is the Bernoulli divergence $(v-w)^2/(w(1-w))$ of T4 Lemma 1, and T4 counts the greedy stages of the two-point bridge with threshold $c$; there every stage $t<T$ is a mixture step with $\tau=c$ (the greedy step is tight, cf. Lemma 4.1 below), so (2.4) recovers T4's upper bound $T\le\log_2^+\log(1/u_0)+O(1)$, where $u_0$ is the start weight $q_0(1)$ of the state gaining mass, with a different constant ($1+2C_{\rm inc}(c/2)$ against T4's $K_{\rm up}(c)$: larger at $c=1/9$, $63.1$ against $61.4$; smaller for small $c$, since $C_{\rm inc}(c/2)$ grows like $1/c$ while $K_{\rm up}$ grows like $c^{-3/2}$). The point of (2.4) is that it holds for *every* increasing sequence, not only for the greedy sequence of the mixture itself: the steps of the full bridge's schedule interleave mixture steps with other steps, and on a monotone piece the other steps can only move $u_k$ further in the same direction, which is all that the phase count of Proposition 2.5 uses.

---

## 3. Step 3: steps on which the within-mode budget binds

**Lemma 3.1 (one-step bound on a part; L5's Lemma 8.1 on $\mathcal A_k$).** Assume (M2) in the form R3. For every $k\in[K]$, $\phi\in[0,1]$ and $0\le\delta\le\lambda_0$,
$$
\chi^2(q^k_{\phi+\delta}\|q^k_\phi)\le e^{2\delta^2\sigma_w^2}-1 .
$$

*Proof.* Write $\mathbb E$ for $\mathbb E_{q^k_\phi}$, $\mu=\mathbb E d$ and $U=U^k_\phi=d-\mu$. By (0.2),
$$
1+\chi^2(q^k_{\phi+\delta}\|q^k_\phi)=\sum_{S\in\mathcal A_k}\frac{q^k_{\phi+\delta}(S)^2}{q^k_\phi(S)}=\frac{\sum_{S\in\mathcal A_k}q^k_\phi(S)e^{2\delta d(S)}}{\big(\mathbb Ee^{\delta d}\big)^2}=\frac{\mathbb Ee^{2\delta d}}{(\mathbb Ee^{\delta d})^2}=\frac{e^{2\delta\mu}\,\mathbb Ee^{2\delta U}}{e^{2\delta\mu}\,(\mathbb Ee^{\delta U})^2}=\frac{\mathbb Ee^{2\delta U}}{(\mathbb Ee^{\delta U})^2}.
$$
By Jensen's inequality and $\mathbb EU=0$, $\mathbb Ee^{\delta U}\ge e^{\delta\,\mathbb EU}=1$. Hence $1+\chi^2\le\mathbb Ee^{2\delta U}\le\exp\{(2\delta)^2\sigma_w^2/2\}=e^{2\delta^2\sigma_w^2}$ by (M2) with $\lambda=2\delta\in[0,2\lambda_0]$. (This is Lemma 8.1 of `elementary_I/PROOF.md`, applied to the bridge on the finite set $\mathcal A_k$; the computation is repeated here because that lemma is stated for the whole space.) $\square$

**Proposition 3.2 (the within-mode count).** Assume (M2). Let
$$
W:=\Big\{t\in[T]:\ \max_{k\in[K]}\chi^2_k(\phi_{t-1},\phi_t)\ge c'\Big\},\qquad \delta_0:=\min\Big\{\lambda_0,\ \frac{\sqrt{\log(1+c')/2}}{\sigma_w}\Big\}>0 .
$$
Then $\phi_t-\phi_{t-1}\ge\delta_0$ for every $t\in W$, and
$$
|W|\le\Big\lfloor\frac1{\delta_0}\Big\rfloor\le\Big\lceil\max\Big\{\frac1{\lambda_0},\ \sigma_w\sqrt{\frac2{\log(1+c')}}\Big\}\Big\rceil .
$$

*Proof.* Let $t\in W$ and $\delta:=\phi_t-\phi_{t-1}>0$; here $\phi_{t-1}\in[0,1)$. If $\delta>\lambda_0$ then $\delta>\delta_0$. If $\delta\le\lambda_0$, Lemma 3.1 applies to every $k$ at $\phi=\phi_{t-1}$, so $c'\le\max_k\chi^2_k(\phi_{t-1},\phi_t)\le e^{2\delta^2\sigma_w^2}-1$, whence $2\delta^2\sigma_w^2\ge\log(1+c')$ and $\delta\ge\sqrt{\log(1+c')/2}/\sigma_w\ge\delta_0$. The half-open intervals $(\phi_{t-1},\phi_t]$, $t\in W$, are pairwise disjoint subsets of $(0,1]$, so $|W|\,\delta_0\le\sum_{t\in W}(\phi_t-\phi_{t-1})\le1$, i.e. $|W|\le1/\delta_0$, and $|W|$ is an integer. Finally $1/\delta_0=\max\{1/\lambda_0,\sigma_w\sqrt{2/\log(1+c')}\}$, and $\lfloor x\rfloor\le\lceil x\rceil$. $\square$

*Remark 3.3.* The bound on $|W|$ is exactly the first term of P2, which is L5's stage bound with $(\sigma_w,c')$ in place of $(\sigma_d,c)$. The proof differs from L5's: L5(a) (Theorem 8.3(a) in `elementary_I/PROOF.md`) implies that every greedy step that does not end at $\phi=1$ is at least $\min\{\lambda_0,\sqrt{\log(1+c)/2}/\sigma_d\}$ long, the analogue of $\delta_0$ with $(\sigma_d,c)$ in place of $(\sigma_w,c')$ (there the full budget is the within budget), whereas here only the steps in $W$ are known to be long, and these are counted by their total length. Steps outside $W$ may be arbitrarily short; except for the last step, they are counted in §2.

---

## 4. Step 4: assembly, and why the counts add

**Lemma 4.1 (greedy steps are tight).** For every $t$ with $1\le t<T$, $\chi^2(q_{\phi_t}\|q_{\phi_{t-1}})=c$.

*Proof.* Fix such a $t$ and put $g(\phi):=\chi^2(q_\phi\|q_{\phi_{t-1}})$ for $\phi\in\mathbb R$. Each $q_\phi(S)=\gamma_0(S)e^{\phi d(S)}/\bar Z_\phi$ is a continuous function of $\phi$ (a finite sum of exponentials divided by a positive one), so $g$ is continuous. Since $\phi_t\in\Phi_t$ (L4(iii)(a)), $g(\phi_t)\le c$. Since $t<T$, $\phi_t<1$. For every $\phi\in(\phi_t,1]$, $\phi\notin\Phi_t$ because $\phi>\sup\Phi_t$; as $\phi\in(\phi_{t-1},1]$, this means $g(\phi)>c$. Letting $\phi\downarrow\phi_t$ and using continuity, $g(\phi_t)\ge c$. $\square$

**Theorem 4.2 (additivity).** Let $W$ be as in Proposition 3.2 and
$$
M:=\big\{t\in[T]:\ \chi^2_{\rm mix}(\phi_{t-1},\phi_t)\ge c'\big\}.
$$
Then $\{1,\dots,T-1\}\subseteq W\cup M$; consequently $T\le1+|W|+|M|$.

*Proof.* Let $1\le t<T$. By Lemma 4.1, $\chi^2(q_{\phi_t}\|q_{\phi_{t-1}})=c\ge c$. By Corollary 1.2 (second form) with $\phi=\phi_{t-1}<\phi'=\phi_t$, either $\max_k\chi^2_k(\phi_{t-1},\phi_t)\ge c'$, i.e. $t\in W$, or $\chi^2_{\rm mix}(\phi_{t-1},\phi_t)\ge c'$, i.e. $t\in M$. So $[T-1]\subseteq W\cup M$ and $T-1\le|W\cup M|\le|W|+|M|$. $\square$

**Proof of Theorem 0.1.** By Theorem 4.2, $T\le1+|W|+|M|$. Proposition 3.2 bounds $|W|$ by the first term of the statement. For $|M|$, apply Theorem 2.7 to the strictly increasing sequence $\psi_t:=\phi_t$, $t=0,\dots,T$ (which satisfies $0=\psi_0<\dots<\psi_T=1$ by (0.3) and L4(iii)), with $\tau:=c'$, so that $c''=c'/K$ is the constant of (0.4): a step $t$ of this sequence is a mixture step exactly when $t\in M$, and (2.4) gives
$$
|M|\le\sum_{(k,\phi^\ast)\in\mathcal U}\log_2^+\log\frac1{u_k(\phi^\ast)}+K(J-1)+KJ\,C_{\rm inc}(c'') .
$$
Adding, $T\le\lceil\max\{1/\lambda_0,\sigma_w\sqrt{2/\log(1+c')}\}\rceil+\sum_{\mathcal U}\log_2^+\log(1/u_k(\phi^\ast))+1+K(J-1)+KJ\,C_{\rm inc}(c'')$, which is the statement with $K_1(c,K,J)=1+K(J-1)+KJ\,C_{\rm inc}(c'')$. $\square$

**Remark 4.3 (the mixture $\chi^2$ is not monotone in its starting point: the global L4(ii) analogue is false).** The note proposed to obtain additivity from a monotonicity property of the mixture $\chi^2$ in its starting point, analogous to L4(ii); in the form L4(ii) takes, this would read: for fixed $\phi_b$, $\phi\mapsto\chi^2(u(\phi_b)\|u(\phi))$ is nonincreasing on $(-\infty,\phi_b]$. This is false, and the note's own example shows it. Take $\mathcal S=\{s_1,s_2,s_3\}$ (the note's $a,b,c$), $\mathcal A_1=\{s_1,s_3\}$, $\mathcal A_2=\{s_2\}$, $\gamma_0=(1,\varepsilon,\varepsilon^2)$, $d=(0,D,2D)$ with $D>0$ and $\varepsilon=e^{-D/2}$. Then $\gamma_\phi\propto(1,x,x^2)$ with $x=x(\phi)=\varepsilon e^{\phi D}=e^{D(\phi-1/2)}$, so $x(0)=e^{-D/2}$, $x(1/2)=1$, $x(1)=e^{D/2}=1/x(0)$, and
$$
u_1(\phi)=\frac{1+x^2}{1+x+x^2},\qquad u_2(\phi)=\frac{x}{1+x+x^2},\qquad u_1(\phi)=u_1(1-\phi)\ \text{(invariance of the formula under }x\mapsto1/x).
$$
Hence $u(1)=u(0)$ and $\chi^2(u(1)\|u(0))=0$, whereas $u_1(1/2)=2/3$ and, by the two-point formula (Lemma 1.1 with $K=2$),
$$
\chi^2\big(u(1)\|u(\tfrac12)\big)=\frac{(u_1(1)-\tfrac23)^2}{\tfrac23\cdot\tfrac13}=\frac92\Big(\frac{(e^{D/2}-1)^2}{3(1+e^{D/2}+e^{D})}\Big)^2=\frac{(e^{D/2}-1)^4}{2\,(1+e^{D/2}+e^{D})^2},
$$
using $u_1(1)-\tfrac23=\dfrac{3(1+e^{D})-2(1+e^{D/2}+e^{D})}{3(1+e^{D/2}+e^{D})}=\dfrac{(e^{D/2}-1)^2}{3(1+e^{D/2}+e^{D})}$. For $D=20$ this is $0.49986$ to five decimals ($0.4998638$). So $\phi\mapsto\chi^2(u(1)\|u(\phi))$ equals $0$ at $\phi=0$, about $\tfrac12$ at $\phi=\tfrac12$, and $0$ at $\phi=1$: it is not nonincreasing on $[0,1]$. What fails is the global property, with the starting point and the target on opposite sides of the breakpoint $\tfrac12$, and it fails at every scale: by the symmetry $u(\tfrac12-h)=u(\tfrac12+h)$, $\chi^2(u(\tfrac12+h)\|u(\tfrac12-h))=0<\chi^2(u(\tfrac12+h)\|u(\tfrac12))$ for every $h\in(0,\tfrac12]$ (the second divergence is positive because $u_1(\tfrac12)=\tfrac23<u_1(\tfrac12+h)$). A version restricted to an interval on which every $u_k$ is monotone does hold (Lemma 4.6 below), but it is not needed here. A comparison-schedule route to additivity would need some such property to show that starting a mixture step later never costs more stages; Theorem 4.2 does not need any: it counts the steps of the actual greedy schedule, and Theorem 2.7 counts mixture steps along *that* sequence, whatever it is. In this example $u_1$ is nonincreasing on $[0,\tfrac12]$ and nondecreasing on $[\tfrac12,1]$, $u_2$ the other way round, so $J=2$ and $\mathcal U=\{(1,\tfrac12),(2,0)\}$ with $u_1(\tfrac12)=\tfrac23$ (contributing $\log_2^+\log\tfrac32=0$) and $u_2(0)=e^{-D/2}/(1+e^{-D/2}+e^{-D})$ (contributing $\log_2^+\log(1/u_2(0))\approx\log_2(D/2)$). Incidentally, the draft's note says that $u_1$ "returns to $1$"; exactly, $u_1(1)=u_1(0)=(1+e^{-D})/(1+e^{-D/2}+e^{-D})<1$, which is $1-e^{-D/2}+O(e^{-D})$.

**Remark 4.4 (how the two counts add).** Every greedy step except the last is tight (Lemma 4.1). A tight step must exhaust one of the two budgets of Corollary 1.2, so the steps split into those that bind the within-mode budget (long, hence few: Proposition 3.2) and those that bind the mixture budget (counted by the $K$-category T4: Theorem 2.7). Both counts are taken along the same sequence, the greedy one, and neither needs the other steps to be absent: Proposition 3.2 only uses that the $W$-steps are disjoint subintervals of $[0,1]$, and Proposition 2.5 only uses that between two active steps on a monotone piece the mode weight moves the right way. This is why the bound is a sum, and why no comparison schedule and no monotonicity in the starting point enter.

**Remark 4.5 (the constant).** $K_1$ is not optimised. The pigeonhole in Lemma 2.2 divides the threshold by $K$; the small phase is counted with the crude threshold $\theta$ as in T4; the middle phase is counted additively. (For $K=2$ and scalars $w,v\in(0,1)$, $(v-w)^2/w=(1-w)\cdot(v-w)^2/(w(1-w))$, so on a mixture step the term of the mode with weight $w\le\tfrac12$ is at least $(1-w)c'$, whose worst case over $w\le\tfrac12$ is the pigeonhole's $c'/2$; no uniform improvement is claimed.)

**Lemma 4.6 (monotonicity in the starting point on a common monotone interval).** Let $I\subseteq\mathbb R$ be an interval on which every $u_k$, $k\in[K]$, is monotone. Then for all $\phi\le\phi'\le\phi_b$ in $I$,
$$
\chi^2\big(u(\phi_b)\|u(\phi')\big)\le\chi^2\big(u(\phi_b)\|u(\phi)\big).
$$

*Proof.* By Lemma 1.1, $\chi^2(p'\|p)=\sum_kr_{p'_k}(p_k)$ for probability vectors $p',p$ on $[K]$ with $p>0$, where $r_y(x):=(y-x)^2/x$ for $x>0$ and $y>0$. For fixed $y>0$, $r_y'(x)=\big(-2(y-x)x-(y-x)^2\big)/x^2=(x^2-y^2)/x^2$, so $r_y$ is nonincreasing on $(0,y]$ and nondecreasing on $[y,\infty)$. Fix $k$ and put $y=u_k(\phi_b)$, $x=u_k(\phi)$, $x'=u_k(\phi')$; all three are positive by R1. Since $u_k$ is monotone on $I\ni\phi\le\phi'\le\phi_b$, $x'$ lies between $x$ and $y$: either $x\le x'\le y$, and then $r_y(x')\le r_y(x)$ on the nonincreasing branch, or $y\le x'\le x$, and then $r_y(x')\le r_y(x)$ on the nondecreasing branch. Summing over $k$ gives the claim. $\square$

In the example of Remark 4.3 the property therefore holds on $[0,\tfrac12]$ and on $[\tfrac12,1]$ separately, and fails only across $\tfrac12$. (This lemma was pointed out by a reviewer; it is not used in the proof of Theorem 0.1.)

---

## 5. Hypotheses used, readings, and flags for the draft

**Where each hypothesis is used.**
- (M1): only in §2 (Lemmas 2.3, 2.4, Proposition 2.5, Theorem 2.7), through R2.
- (M2): only in §3 (Lemma 3.1), at $\phi=\phi_{t-1}\in[0,1)$ and $\lambda=2\delta\le2\lambda_0$.
- $c'=\sqrt{1+c}-1$: only in Corollary 1.2, through $(1+c')^2=1+c$.
- L4(iii) (well-definedness and termination of the greedy schedule): §0.2, Lemma 4.1 and the proof of Theorem 0.1. This is the only external result the proof uses. L3 and L7 are not used. Other results are named only in remarks, flags, readings, titles and Lemma 4.6, none of which carries weight in the proof of Theorem 0.1: L4(i) and L4(ii) (Remarks 1.3 and 4.3, Lemma 4.6 as their analogues, Flag 1, the summary of the note in §0.1), L5 (its hypothesis in R3 and (M2); its stage bound in R5 and Remark 3.3; its part (a) in Remark 3.3), T4 (Lemma 1, Lemmas 6–9, Proposition 11 and its constant $K_{\rm up}$: Remarks 2.8 and 4.5; the phrase "$K$-category T4" in §0.4, the titles of §2 and Theorem 2.7, Remark 4.4 and Flag 1 names this proof's Theorem 2.7, not T4's content). L5's one-step computation is repeated in Lemma 3.1 rather than cited.
- "$K$ fixed" is not needed: the bound is explicit in $K$.

**Flags for the draft.**
1. *The open step is closed, by a different route from the note's.* The additivity holds because every greedy step but the last is tight and therefore binds one of the two budgets (Theorem 4.2); the mixture steps are then counted along the greedy sequence itself by Theorem 2.7, which is a $K$-category T4 valid for every increasing sequence of points. The note's suggested tool, monotonicity of the mixture $\chi^2$ in its starting point (an L4(ii) analogue), fails globally (Remark 4.3, with the note's own example); it holds on any interval on which every $u_k$ is monotone (Lemma 4.6), but this is not needed. Suggested replacement for the note's third bullet: "Additivity: every greedy step but the last is tight, so it exhausts the within-mode budget $c'$ or the mixture budget $c'$; the first kind is long, the second is counted by a $K$-category version of T4 that holds along any increasing sequence of points. No monotonicity of the mixture $\chi^2$ in its starting point is needed, and the global one fails (the example below shows $\chi^2(u(1)\|u(\phi))$ rising and falling on $[0,1]$)."
2. *$K_1$ explicit:* $K_1(c,K,J)=1+K(J-1)+KJ\big[2+(1-\theta)/\sqrt{c''\theta}\big]$ with $c''=(\sqrt{1+c}-1)/K$ and $\theta=e^{-1}\min\{1,c''\}$. At $c=1/9$, $K=2$: $K_1=125.7$ for $J=1$ and $252.4$ for $J=2$.
3. *(M1) should fix a decomposition.* The statement should say that a decomposition of $[0,1]$ into at most $J$ closed pieces per $k$, each declared nondecreasing or nonincreasing, is fixed, and that $\mathcal U$ is the set of left endpoints of the pieces declared nondecreasing (R2). Without this, "starts an increasing piece" is ambiguous for constant pieces and for non-minimal decompositions.
4. *Nonempty parts* (R1) should be stated, or empty parts allowed and dropped.
5. *A sharper intermediate statement* is available and may be worth stating: $T\le1+|W|+|M|$ (Theorem 4.2), with $|W|\le\lfloor1/\delta_0\rfloor$ and $|M|$ bounded by (2.4).
6. *Decreasing pieces* contribute at most $C_{\rm dec}(c'')=K/c'$ steps each (Proposition 2.5(b)), confirming the note's "$O(1)$ each".
