# MASTER PROOF PLAN: Wave 2 (Lead-S, Lead-M, Lead-D) and the hand-off to Wave 3 (Lead-L) — Lead-A v0.1, 2026-11-28

**Status: DRAFT v0.3 (Astra memo items 3, 6; Fable memo R1–R3 folded in) for the Plan Council.** The statements proved here are those of `LOCKED_STATEMENTS.md` (= [LS]).
Paths are relative to `Theory_work/Wave3/` unless they start with `Theory_work/` or `Docs/`.
Aliases: [P1] = T01/T02 `PROOF_v3.tex`, [P3] = T03 `PROOF_v2.tex` (both pinned under
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/`);
[T03R] = `W3-T03ACC/sources/W1-T03R/PROOF.md` (council-accepted, pinned; `W3-T03ACC/REPORT.md` §2);
[W3P] = `W3-POST/STATEMENT.md`; [DIST] = `W3-DIST/STATEMENT.md`; [B3] = `W3-DIST/work/E_bridges/B3.md`.
Check states: `W3-DIST/DEPS.tsv` and `Theory_work/Dept/wave1_plan/RECONCILIATION.md`. A statement counts as
checked only where its row says so.

## 0. Milestones and what "PROMISING" means (owner's definition of done, Criterion 2)

A theorem's proof is **PROMISING** when four things hold.
1. A forward-written route exists in one file, `Theory_work/Dept/wave2/<lead>/PROOF.md`, in which every key step marked
   **KEY** below is written in full. Other steps may cite a checked source by file:line, with the exact statement
   used quoted.
2. No known fatal gap. Every open sub-step is listed with the reason it is believed true.
3. The lead's own Sol line check of the KEY steps is attached.
4. The route has been reviewed by its council (Opus + Sol + third seat, per POLICIES §1b as in force), with no open
   blocking issue. Its scores are recorded; the 8.5 bar is NOT required at this milestone.

**DEFINITIVE** means every reviewer scores ≥ 8.5 and every step is written or cited as checked (POLICIES §1b, the
headline bar). Lean follows only after DEFINITIVE.

| Lead | Theorem(s) | KEY steps | Target for PROMISING | Then DEFINITIVE |
|---|---|---|---|---|
| Lead-S | Thm S (a), (b); Cor S1 | S-1, S-2, S-3, S-5 | 2–3 days after launch | 3–6 person-days total plus review |
| Lead-M | Thm M (i)–(iii); then Cor M1 | M-1, M-2, M-3, M-4 | 2–3 days | 3–6 person-days plus review |
| Lead-D | Thm D | D-1, D-2, D-3 | 2–4 days | 4–8 person-days plus review |

The three leads are independent. Cor M1 waits for Thm D and Thm S to reach PROMISING; it is one paragraph. Lead-M
writes it.

## 1. Shared lemmas: interface contract

Each shared lemma has one owner. The owner writes it once, in `Theory_work/Dept/wave2/shared/<ID>.md`. Others cite it
by ID@version and never re-prove it. The interface (hypotheses → conclusion) is frozen by this plan. A lead who needs a
change raises it with Lead-A or the Manager; it is not changed silently. "Source" is where a checked proof already
exists.

| ID | Interface (hypotheses → conclusion) | Source (checked) | Owner | Consumers | Lean tier |
|---|---|---|---|---|---|
| **L-POST** posterior summaries | For any probability $\pi$ on the models and any $S_0$: $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0)$; $\pi(S_0)>\tfrac12\Rightarrow\mathrm{HPM}=\mathrm{MPM}=S_0$; $\sup_{h:2^{[p]}\to[0,1]}|\sum_S\pi(S)h(S)-h(S_0)|=1-\pi(S_0)$. Deterministic. | `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md` SL0 (l.20–38), SL1 (l.39–50); L-LEAN `T21HPM.lean` | Lead-S | S, M, M1 | 1 (full proof) |
| **L-SCORE** coded score | The coded model weight is $\pi(S\mid y)\propto\varpi(S)D_S^{-1/2}(2b_0+Q_S)^{-\nu}$, with $D_S=\det H_S/\det(G_S+I)$, $H_S=(n+1)G_S+I$, $\nu=a_0+n/2$ ([W3P] §0, l.16–30), and the conditional law of $(\theta_S,v)$ given $S$ is normal–inverse-gamma. Plus: $1\le D_S\le(n+1)^{|S|}$; $Q_{S'}\le Q_S$ for $S\subseteq S'$; the interlacing bound $D_{S\cup\{j\}}/D_S\ge((n+1)\lambda+1)/(\lambda+1)$ with $\lambda=\lambda_{\min}(G_{S\cup\{j\}})$. | [W3P] §0; [P1] `lem:spec`; [P3] `lem:det`, `lem:smoother`; [DIST] B2 (l.400–408) | Lead-S | S, D, M | 1 |
| **L-SCALE** scale reduction | Pathwise, $\Pi(\cdot\mid x,y)$ is the image of $\Pi(\cdot\mid x,\tilde y)$, $\tilde y=(y-a)/\sigma$, under $(S,\theta,v)\mapsto(S,\sigma\theta,\sigma^2v)$; plug-in intercepts transform affinely; $d_H$ is preserved draw by draw. Here $a,\sigma$ are deterministic (no response-dependent scaling: checklist T-5). | [DIST] B0 (l.385–390), W3-MISR R′(a′) "PROVED-CHECKED; council R2" | Lead-D | D, S, M1 | 1 |
| **L-HELL** Hellinger reduction | For Gaussian conditionals sharing the $x$-marginal: $d_H^2(f_{S,\theta,v},f^\dagger)\le(v/\sigma_\dagger^2-1)^2+E_x\min\{1,\Delta(x)^2/(4\sigma_\dagger^2)\}$, $\Delta$ = the difference of the conditional means. Deterministic; the target $f^\dagger$ may be $f^*$ or $f_0$. | [DIST] Lemma H (l.322–327; "not line-checked", so the owner line-checks it) | Lead-D | D, M(i) | 2 (needs the Gaussian affinity identity, axiom G1) |
| **L-DES** design events | Under A4 (and A3), on an event of probability $\ge1-5p\,e^{-cn/L^4}$: (i) $\tfrac12\le\hat s_j^2/\operatorname{Var}(x_j)\le2$ for all $j$ (no column dropped); (ii) for all $w$ supported on $q$ coordinates and all $a$, $n^{-1}\sum_i(a+w^\top\zeta_i)^2\ge\tfrac12(a^2+\operatorname{Var}(w^\top\zeta))$, provided $q\log(ep/q)\le c'n/L^4$; (iii) with A5 on $q$-sets: $\lambda_{\min}(G_T)\ge c_\psi/8$ for $|T|\le q$; (iv) under A6, $\|\mu\|^2\le2s^2\bar b^2\sigma_*^2n$ and $\|\theta^*\|^2\le2s\bar b^2\sigma_*^2$. | [DIST] B1 (l.391–395), B2-core (l.396–399), B2 (l.400–408); `work/E_bridges/B1.md`, `B2core.md`, `B2.md` | Lead-D | D, S, M1 | 3 (Bernstein and the net argument: axiom P3) |
| **L-FLOOR** two-floor bridge (B3′) | On the L-DES event with $q=q_n(1)$: A7′(a) ⇒ $(F_\lambda;\varphi_0)$ with $\varphi_0^2=\varphi^2/4$ on $S_0\cup J$, $|J|\le j_0$; A5 ⇒ $(F_w;g_0)$, $g_0=c_\psi/8$, on $S_0\cup J$, $|J|\le m^\sharp_n$, clipped at $p$; for each $j$, $\theta^{*2}_j\ge b_j^2/2$. Hence $\varphi b_j\ge C_\beta\sqrt{\log(p\sqrt n)/n}$ with $C_\beta>C_{\rm sel}$ ⇒ $\theta^{*2}_j\ge c\log n/(n\varphi_0^2)$ for a fixed $c>c_0$ (KEY S-2). | [B3] Steps 0, 3, 4 (checked items), Step 5 to be replaced; Amendments A-1, A-2 | Lead-S | S, M1 | 3 |
| **L-T03♯** fixed-design selection core | Regime R1 ($s_0\ge1$ fixed, $2\le p\le n^A$, $s_0\le K$), Gaussian noise G, $(E)$, $(F_\lambda)$, $(F_w)$: (iv) for fixed $c>c_0$, $\Pi(S\not\supseteq J^{\rm samp}_n(c))=O_P(r_n)$, with $J^{\rm samp}_n(c)=\{j:\theta^{*2}_j\ge c\sigma_*^2\log n/(n\varphi_0^2)\}$; under BM$(c)$, (i) $1-\pi(S_0)=O_P(r_n)$ and (ii), (iii). | [T03R] §6 (l.159–209), council-accepted (`W3-T03ACC/REPORT.md` §2: three blind Sol line checks VERIFIED); [W3P] Thm 1 items 1–5 | Lead-S (cite; do not re-prove) | S, M1 | 3 (deterministic assembly; χ² facts as axioms P1, P2) |
| **L-RAND** random-design transfer | If (X, θ*)-measurable events $\mathcal A_n$ with $P(\mathcal A_n)\to1$ carry the L-T03♯ hypotheses with common constants (and a common $c>c_0$), then its conclusions hold under the joint law, with $O_P$ uniform. | [W3P] Thm 1 item 6 (l.95–100); [POST] step (5) (`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`) | Lead-S | S, M1 | 2 |
| **L-SIZE** size tail | Exact BB(1,p) tail (E1), $m^\sharp_n$ bounds; the posterior mass above $m^\sharp_n(\omega)$ is $O_P(e^{-\omega})$ (Lemma 1a/1a′); the exponential version is Lemma S. | [T03R] §1–2 (E1, E2); [W3P] Lemma 1a (l.40–55); [DIST] Lemma S (l.342–354) | Lead-D | D, S | 1 (E1, combinatorial) / 3 |
| **L-FIX** fixed-dimension a.s. score asymptotics (NEW) | Under A8, a.s.: for every $S\subseteq\mathcal C$, $Q_S/(n-1)\to1-\rho_S^2$, where $\rho^2_S$ is the population $R^2$ of the best linear predictor from $(1,x_S)$; $G_S/n\to\operatorname{Corr}(x_S)\succ0$; $\log D_S=|S|\log(n+1)+O(1)$; the ridge changes $Q_S$ by $O(1)$; the sample-moment map to raw units converges. | none (new; SLLN) | Lead-M | M | 2 (SLLN is in Mathlib) |
| **L-LIL** score LIL (NEW) | If $E(Z_j^2u^2)<\infty$ for all coordinates, with $Z=(1,x_{\mathcal C}^\top)^\top$ and $u=\varepsilon_{\mathcal C}$ (so $E(Zu)=0$ by the normal equations), then $\|\sum_{i\le n}Z_iu_i\|=O(\sqrt{n\log\log n})$ a.s. | Hartman–Wintner LIL (named axiom P6) | Lead-M | M(iii) | 3 |

Lean tiers: 1 = deterministic, fully provable now; 2 = needs Mathlib probability that exists (SLLN, Gaussian measure);
3 = consumes a named, cited probability axiom (`LEAN_PLAN.md` §2).

## 2. Lead-S: selection (Thm S, Cor S1)

Route (packet §3.1; Astra Phase 2 §1; Fable Phase 2 §2). This is a **composition** of checked parts plus one modified
bridge. Write it **forward as one proof** (packet §6): no diff chains in the deliverable; cite [T03R] and [P3] by label
for the unchanged fixed-design steps.

- **S-0 (reduction).** By L-SCALE take $\alpha^*=0$, $\sigma_*=1$. Split the sequence $n$ into the finitely many
  subsequences on which $s_0\in\{1,\dots,s\}$ is constant. $O_P$ statements along each subsequence combine into one,
  since there are finitely many. This handles Regime R1's "$s_0$ fixed" against A2's "$s_0\le s$" (checklist T-7).
- **S-1 (KEY: design event).** Define $\mathcal A_n=\mathcal E_1\cap\mathcal E_2(q_n)$ with $q_n=\min\{p,\lceil C_q\log n\rceil\}$
  (L-DES at level $M=1$). Show $P(\mathcal A_n^c)\le5n^Ae^{-c_2n/L^4}\to0$ ([B3] Step 6 (vii)). On $\mathcal A_n$:
  $p_{\rm ret}=p$; $|\operatorname{supp}\theta^*|=s_0$; $(E;2s^2\bar b^2)$; $(F_w;c_\psi/8)$ on $S_0\cup J$ with
  $|S_0\cup J|\le\min\{p,s_0+m^\sharp_n\}\le q_n$ ([B3] Step 0 and Amendment A-1: **clip at $p$**).
- **S-2 (KEY: new B3 step 5 with a fixed $c$).** On $\mathcal A_n$, $\theta^{*2}_j\ge b_j^2/2$. For $j\in J_n$ (the
  population strong set), $\varphi^2b_j^2\ge C_\beta^2\log(p\sqrt n)/n$, and $\log(p\sqrt n)\ge\tfrac12\log n$, so with
  $\varphi_0^2=\varphi^2/4$:
  $$\theta_j^{*2}\,\frac{n\varphi_0^2}{\log n}\ \ge\ \frac{\varphi^2b_j^2}{8}\cdot\frac{n}{\log n}\ \ge\ \frac{C_\beta^2}{8}\cdot\frac{\log(p\sqrt n)}{\log n}\ \ge\ \frac{C_\beta^2}{16}=:c\ >\ c_0$$
  exactly when $C_\beta>C_{\rm sel}=4\sqrt{c_0}$. The constant is common to all $n$ and all $p\ge2$. Hence
  $J_n\subseteq J^{\rm samp}_n(c)$ on $\mathcal A_n$ ($J_n$ is deterministic), and under A7′(b), BM$(c)$ holds with this
  common $c$. This replaces the last sentence of [B3] Step 5 (BM-∞) and the envelope clause of Step 6 (packet §2.2).
- **S-3 (KEY: small-set floor on the tightened window).** On $\mathcal A_n$, A7′(a) (anchored: $S_0\cup J$, $|J|\le j_0$;
  sizes $\le\min\{p,s_0+j_0\}$) gives $(F_\lambda;\varphi_0)$, $\varphi_0^2=\varphi^2/4$, on every $S_0\cup J$ with $|J|\le j_0$ ([B3] Step 3, with
  the window $(2A+3)s+2$ replaced by $\min\{p,s_0+j_0\}$; Step 0(1) still puts these sets inside $q_n$). Check that
  $0<\varphi_0\le\tfrac12$.
- **S-3′ (KEY: fresh line check of the modified bridge B3′).** [B3] is headed "DRAFT (by this seat, unchecked)" and is
  written for BM-∞ and exactly $s$ nonzero coefficients (Fable memo R1). B3′ = [B3] with S-2, S-3 and amendments A-1, A-2
  is a new statement and gets its own cross-family (Sol) line check before the PROMISING review.
- **S-4 (assembly via L-RAND).** *Alternative spine (Fable R1), to be chosen by Lead-S:* drop the diagonal transfer.
  Write one per-$n$ bound conditional on $(X,\theta^*)$ over the design event and integrate, e.g.
  $E\delta_n\le Cr_n+P(\mathcal A_n^c)$ (`W3-POST2/lemmas/C_expectation.md:8-15`, case (i)). Nothing response-dependent
  then enters before conditioning. Part (a) still uses T03♯(iv) per $n$. On $\mathcal A_n$ the hypotheses of L-T03♯ hold with common constants
  $(M,\varphi_0,g_0,c)=(2s^2\bar b^2,\varphi/2,c_\psi/8,C_\beta^2/16)$. By L-RAND, T03♯(iv) gives
  $\Pi(S\not\supseteq J^{\rm samp}_n(c))=O_P(r_n)$, hence $\Pi(S\not\supseteq J_n)\le\Pi(S\not\supseteq J^{\rm samp}_n(c))+\mathbf 1_{\mathcal A_n^c}$,
  which is (a). Under A7′(b), T03♯(i)–(iii) give (b), with L-POST for the PIPs, the HPM and the MPM. Replace the
  replacement-design device of [B3] Amendment A-2 by the same device verbatim (it handles $p_{\rm ret}\ne p$ off
  $\mathcal A_n$).
- **S-5 (KEY: independence and measurability).** Verify that no step uses a response-dependent scaling before
  conditioning on the design (checklist T-5): $\theta^*=D_x\beta^*/\sigma_*$ is design-measurable, $J^{\rm samp}_n(c)$ is
  design-measurable, and $J_n$ is deterministic. Verify that the noise is independent of $(X,\theta^*)$ under A1.
- **S-6 (Cor S1).** $b_{\min}\ge\underline b$ fixed ⇒ $\varphi b_{\min}\ge C_\beta\sqrt{\log(p\sqrt n)/n}$ for all large $n$
  (because $\log(p\sqrt n)/n\le(A+\tfrac12)\log n/n\to0$), for any $C_\beta$. Apply (b).
- **Risks.** Low. Known traps: the window clip at $p$ (T-1); population vs sample strong sets (S-2); $s_0$ varying (S-0).
  The fixed-design core is accepted; nothing new is probabilistic.
- **Not in scope for Criterion 2:** the sharpened constant (packet §5; needs Astra's extra design estimate); $s_0=0$.

## 3. Lead-M: misspecification under A8 (Thm M), then Cor M1

Route (packet §3.2; Fable Phase 1 §B.3; Astra Phase 1; draft Conj. 3.6(a) proof path,
`Theory_work/Dept/song_assumptions/THEOREM_DEFINITIONS.md` l.215–219). The model space is finite: $2^{|\mathcal C|}$
models, and $K=|\mathcal C|$ once $n\ge2|\mathcal C|$, so every model has a fixed positive prior. Write everything on the
a.s. event $\Omega_0$ of L-FIX (and of L-LIL in (iii)), and argue pathwise.

- **M-1 (KEY: L-FIX, a.s. score asymptotics).** By the SLLN, the sample means and covariances of $(x_{\mathcal C},y)$
  converge a.s. On the standardised scale, $Q_S/(n-1)\to(1-\rho_S^2)$. Also $G_S/n\to\operatorname{Corr}(x_S)\succ0$
  (A8 nonsingular), so the ridge terms of $Q_S$ and $D_S$ are $O(1)$, and $\log D_S=|S|\log(n+1)+O(1)$. The
  exceptional event (a constant column or response) eventually fails a.s., since $\operatorname{Var}(x_j)>0$ and
  $\operatorname{Var}(y)\ge\sigma^2_{\mathcal C}>0$. Write the explicit error terms, because M-2 and M-4 need their
  orders.
- **M-2 (KEY: inclusion via a fixed risk gap).** If $S\not\supseteq S_0^{\mathcal C}$, then
  $\sigma_S^2>\sigma^2_{\mathcal C}$ (uniqueness of $\beta^{\mathcal C}$, since $\operatorname{Var}(x_{\mathcal C})\succ0$),
  i.e. $\rho_S^2<\rho^2_{\mathcal C}$. Compare $S$ with $\mathcal C$:
  $\log\frac{\pi(S\mid y)}{\pi(\mathcal C\mid y)}\le O(1)+\tfrac{|\mathcal C|}2\log(n+1)-\nu\log\frac{Q_S}{Q_{\mathcal C}}$,
  where $\nu\log(Q_S/Q_{\mathcal C})=\tfrac n2\log\frac{1-\rho_S^2}{1-\rho^2_{\mathcal C}}(1+o(1))\to\infty$ linearly in $n$. So
  every such $S$ has posterior mass $\to0$ a.s., which proves (ii). This is almost sure, a strengthening of SL Cor 2.
- **M-3 (KEY: density; tied supersets are the crucial case).** Every superset of $S_0^{\mathcal C}$ has the same limiting
  score per observation, so M-2 cannot rank them. Density must therefore be proved separately within each containing
  model, then summed over the finite family (adviser memo, item 6). For $S\supseteq S_0^{\mathcal C}$ the population best linear predictor from $(1,x_S)$ is
  $(\alpha_{\mathcal C},\beta^{\mathcal C}|_S)$, with residual variance $\sigma^2_{\mathcal C}$ (the normal equations for
  $S$ are a subset of those for $\mathcal C$). The conditional NIG posterior given $S$ has mean $\to$ the pseudo-true
  value and spread $O(1/n)$ a.s.; map back to raw units with the a.s. convergent sample moments (continuity). Apply
  L-HELL with $f^\dagger=f_0$ and $E\|x_{\mathcal C}\|^2<\infty$: $\Pi(d_H(f,f_0)>\epsilon\mid S,D_n)\to0$ for each such
  $S$. Combined with M-2 over finitely many models, this proves (i). Care points: the plug-in intercept
  $\bar y-\bar x^\top\beta$; the IG$(a_0,b_0)$ prior on the standardised scale (rate $b_0s_y^2$ in raw units); the
  truncation $\min\{1,\cdot\}$ in L-HELL, which turns the mean error into a bounded dominated quantity.
- **M-4 (KEY: exclusion).** For $S\supsetneq S_0^{\mathcal C}$, with $T=S_0^{\mathcal C}$: in the sample
  $y-\alpha_{\mathcal C}\mathbf 1-X_{\mathcal C}\beta^{\mathcal C}=u$ exactly ($u_i=\varepsilon_{\mathcal C,i}$). Since
  $\alpha_{\mathcal C}\mathbf 1+X_T\beta^{\mathcal C}_T$ lies in both column spans, the exact (ridge-free) gain is
  $\mathrm{RSS}_T-\mathrm{RSS}_S=u^\top(P_{Z_S}-P_{Z_T})u\le u^\top P_{Z_S}u=(Z_S^\top u)^\top(Z_S^\top Z_S)^{-1}(Z_S^\top u)$,
  where $Z_S=[\mathbf 1,X_S]$ is **raw and uncentred**. Then $Z_S^\top u=\sum_iZ_{i,S}u_i$ is an i.i.d. sum with mean 0
  (normal equations), and L-LIL gives $\|Z_S^\top u\|=O(\sqrt{n\log\log n})$. Also $(Z_S^\top Z_S/n)^{-1}\to(EZ_SZ_S^\top)^{-1}$
  (SLLN; nonsingular by A8). So the gain is $O(\log\log n)$ a.s. This form (adviser memo, item 6) avoids applying an
  i.i.d. LIL to empirically centred products. Still to verify: $Q^c_S-\mathrm{RSS}_S=O_{\rm a.s.}(1)$ for the coded
  ridge score. The ridge correction is $O(1)$, the prior
  ratio is $O(1)$, and the Occam factor is $-\tfrac12|S\setminus T|\log n+O(1)$. Hence $\pi(S\mid y)/\pi(T\mid y)\to0$
  a.s.; with (ii), $\Pi(S_0^{\mathcal C}\mid D_n)\to1$ a.s., and L-POST gives HPM = MPM eventually.
  Moment bookkeeping: the intercept coordinate needs $Eu^2<\infty$ (automatic); the others need
  $E(x_j^2u^2)<\infty$, which is exactly the hypothesis of (iii).
- **M-5 (Cor M1).** Under A9′, the rows $(x_{\mathcal C,i},y_i)$ satisfy A1 with $(\alpha_{\mathcal C},\beta^{\mathcal C},\sigma_{\mathcal C})$;
  A10 is A2 for that problem; $|\mathcal C|\le n^A$ is A3. With the candidate A4–A6 (and A7′), apply Thm D and Thm S
  verbatim. Here $f_0$ is the true joint density of $(x_{\mathcal C},y)$. Record that $\mathcal C$ is deterministic
  (checklist T-9).
- **Risks.** Low; everything is elementary (Fable R2 checked the leading terms: the ridge difference between nested
  supersets is $O(\log\log n/n)$ before the factor $\nu/(2b+Q)=O(1)$). Watch: (1) M-1's uniformity over the finitely many $S$ (fine pathwise); (2)
  the ridge in $Q_S$ vs the exact projection in M-4; (3) no use of a Gaussian likelihood identity (e.g. $E^*[m_b/f_0]=1$)
  anywhere, because the law is arbitrary.
- **Optional (not Criterion 2):** the in-probability version for a law that changes with $n$, with a risk gap
  $\ge C\log n/n$ (Fable Phase 1 §D.2 option 4).

## 4. Lead-D: density (Thm D)

Route (packet §3.3). This is a **transcription** of [DIST] Theorem A(i) (l.185–191). Theorem A(i) = DIST-1 (1.1)
(l.74–91) + bridges B0, B1, B2 (l.385–408). The proof chain is checked in `W3-DIST/DEPS.tsv`; Astra Phase 1 re-read
the decisive steps and found no gap (`lemmas/X.md:63–180`, `work/B_transfer/T.md:76–166`, `lemmas/DIST12.md:23–77`,
`B2.md`, `ASSEMBLY.md`).

- **D-1 (KEY: assumption translation).** Map the paper's A1–A6 onto [DIST] (A1)–(A5) (reader version, l.173–180): the
  paper's $L$ is [DIST]'s $K$ (sub-Gaussian constant); the paper's "sparse set for every fixed $c$" covers [DIST]'s
  window $q_n=\min\{p,\lceil C_qM\log n\rceil\}$ at each fixed $M$; the paper's A2+A3 is [DIST] (A2); the paper's A6 is
  [DIST] (A5). State and prove the constant bookkeeping ($c_H$, $M_0$, and $n_0(M)$).
- **D-2 (KEY: the three survival items).** Show explicitly, with line references: (1) the capped comparison window covers
  $\min(p,m+s_0)$, with unions clipped at $p$ (T-1); (2) the sample-mean term $\bar\varepsilon^2$ appears in the
  population distance, via Lemma H's in-sample identity $n^{-1}\sum\Delta_i^2=\bar\varepsilon^2+\|\hat\mu-\mu\|^2/n$
  ([DIST] l.326–327) (T-2); (3) $n_0$ may depend on $M$, so the statement is for each fixed $M\ge M_0$ (T-3).
- **D-3 (KEY: exceptional events and $p_{\rm ret}$).** The domain event $\{p_{\rm ret}\ge2\}$, columns dropped, and a
  constant response: all inside the failure probability, uniformly ([DIST] l.28–33, reader Remark (3), l.264).
- **D-4.** Assemble forward: L-SCALE → L-DES → DIST-1 at $t=M\log n/C^2$ → Theorem A(i). Cite Lemmas X, T, S, V by
  ID@version from DEPS.tsv; write the assembly (Remarks (1)–(4), l.261–267) in full.
- **D-5 (optional).** The a.s. corollary for $c_HM>1$ (Borel–Cantelli), as a remark.
- **Risks.** Low–medium. Fable led W3-DIST, so the D line check must be non-Fable (Sol). The transcription is long (Lemma X is the core), and the proof files' headers must agree with
  DEPS.tsv first (RECONCILIATION.md).

## 5. Common requirements for every Wave 2 proof file

1. A header with: the statement (verbatim from [LS]), the version, and a status line using only these words: DRAFT /
   PROMISING (council-reviewed, scores) / DEFINITIVE (council ≥ 8.5). No "PROVED (by this seat, unchecked)" without a
   check record.
2. A consumes table: every cited result, with its ID@version, its recorded check status, and the exact statement used.
3. A pass against `TRANSCRIPTION_CHECKLIST.md` before review (tick every item or mark it N/A).
4. A Lean annotation per step: tier 1/2/3, and the axiom used (`LEAN_PLAN.md` §2), so Lead-L can start from the paper
   proof.
5. POLICIES §14: scratch only under `.rc_tmp/`; Codex workers never delete and never write outside the worktree.

## 6. Order and staffing (proposal to the Manager)

- Launch Lead-S, Lead-M and Lead-D together as soon as the Plan Council clears (the pace rule allows 2–3 concurrent
  leads). If the Manager wants two, pause Lead-D first: Thm D is already proved and needs only transcription.
- Each lead: Opus 5.5 high, with Sonnet and Sol workers. Reuse the department's dedicated Fable 5.2 and Astra 6.2
  advisers (thread ids in `README.md`); spawn no new adviser.
- Shared-lemma owners (§1) write their lemmas in the first day, so the other leads can cite them by ID@version.
