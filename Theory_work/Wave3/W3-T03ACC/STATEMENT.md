# W3-T03ACC — STATEMENT v1.0 (T03♯ = SOP:TH09, restated verbatim for council acceptance)

Ticket W3-T03ACC, Tier B (re-check of an existing proof; no new mathematics). This file restates the theorem of record
and defines every object in it. It asserts no proof status. The object is fixed by the brief (`BRIEF.md:12-21`); this is
**not** a delta statement (`BRIEF.md:6-7`). All paths below are relative to this folder unless they start with
`Theory_work/` or `Docs/`. Copies and their pins: `sources/PINS.md`.

## 0. Sources and their agreement
| role | file:line | content |
|---|---|---|
| statement of record | `sources/statement/W6-FIXREV2_STATEMENTS.md:15-61` | §1.1 setting/hypotheses, §1.2 T03♯ clauses 1–5 (NBH ID_REGISTRY TH128 names this "statement of record W6-FIXREV2 section 1.2") |
| approved card (SOP:TH09) | `sources/statement/TLF_434-499.md:15-18, 29` (= TLF 448–451, 462) and `sources/statement/SoP_04_theory_767-812.tex:14-23` | Seat C card C9: hypotheses table and final statement |
| registry row | `sources/statement/registry_theory_main_L68.tsv` | short form, status, regime |
| proof's own statement | `sources/W1-T03R/PROOF.md:160-168` (§6 hypotheses/conclusions), `:44-47` (m♯_n), `:127-132` (SE_λ, SE_w) | the text the line checks run against |
| definitions | `sources/common/00_COMMON.md:9-14, 29, 35-38`; `sources/P3/STATEMENT.md:5-27` | data, target, prior, regimes, G, R, constants |

The four sources agree on every hypothesis and conclusion, with the differences listed in §4 (all of them readings or
forms, none a change of content). Where the record and the card differ in wording, §2–§3 follow the record.

## 1. Setting (definitions; `sources/common/00_COMMON.md:9-14`, `sources/P3/STATEMENT.md:7-14`)
- **Data.** Raw $(X^r,y^r)$, $X^r\in\mathbb R^{n\times p}$, $n\ge3$, no constant column, $y^r$ not constant.
  $C=I_n-\mathbf 1\mathbf 1^\top/n$; $D_x$ = diagonal of raw column sample SDs; $s_y^2=\|Cy^r\|^2/(n-1)$. Standardised
  $X=CX^rD_x^{-1}$, $y=Cy^r/s_y$ (so $\|x_j\|^2=\|y\|^2=n-1$).
- **Model space and prior as coded.** $K=\min(p,\lfloor n/2\rfloor)$, $\Omega=\{S\subseteq[p]:|S|\le K\}$.
  $w(k)=\tfrac12/\binom{2p-1}{k}$ (per-model BB(1,p) weight), $W_K=\sum_{k\le K}\binom pk w(k)$, $\varpi(S)=w(|S|)/W_K$.
- **Marginal likelihood as coded.** $G_S=X_S^\top X_S=(n-1)R_S$; $z_S=X_S^\top y$; $H_S=(n+1)G_S+I$;
  $D_S=\det H_S/\det(G_S+I)$; $Q_S=y^\top y-nz_S^\top H_S^{-1}z_S$; $a_0=b_0=0.01$, $\nu=a_0+n/2$;
  $m(S)=\frac{(2b_0)^{a_0}\Gamma(\nu)}{\pi^{n/2}\Gamma(a_0)}D_S^{-1/2}(2b_0+Q_S)^{-\nu}$.
- **Posterior (the target).** $F(S)=\log[\varpi(S)m(S)]$, $Z=\sum_\Omega\varpi m$, $\pi(S)=e^{F(S)}/Z$ on $\Omega$;
  $\Pi(\mathcal A\mid y)=\pi(\mathcal A\cap\Omega)$.
- **Decision objects.** $\mathrm{PIP}_j=\pi(\{S:j\in S\})$; $\mathrm{MPM}=\{j:\mathrm{PIP}_j>\tfrac12\}$; global HPM
  $S^\dagger=\arg\max_\Omega F$ (ties: smallest size, then lexicographic).
- **Truth.** $y^r=\alpha^*\mathbf 1+X^r\beta^*+\varepsilon$; $\mu=CX^r\beta^*=X\theta^*$, $\theta^*=D_x\beta^*$;
  $S_0=\operatorname{supp}\beta^*$, $s_0=|S_0|$. $P_0,E_0$ are over $\varepsilon$ (design fixed).
- **Rate.** $r_n=\sqrt{\log n/n}$. $O_{P_0}(a_n)$: tight after division by $a_n$ under $P_0$; "$\to$" for random
  quantities is convergence in $P_0$-probability (`sources/P3/STATEMENT.md:51`).
- **Constants of the locked T03 proof** (`sources/common/00_COMMON.md:38`, `sources/P3/STATEMENT.md:21`):
  $j_*=\lceil(2A+1)s_0\rceil+1$; $C_*=2s_0+3[Aj_*+s_0+\log(j_*+1)+1]$; $L_*=\max\{4C_*,32[s_0(A+1)+2]\}$.

## 2. Hypotheses (record: `sources/statement/W6-FIXREV2_STATEMENTS.md:19-35`; proof: `sources/W1-T03R/PROOF.md:127-132, 162-164`)
- **R1.** Triangular array, $n\to\infty$; $X=X_n$ fixed (non-random); $s_0\ge1$ fixed; $p=p_n\le n^A$ with $A$ fixed
  ($A\ge1$, see §4 item 3); $s_0\le K=\min(p,\lfloor n/2\rfloor)$ for all large $n$. Design, $\beta^*$, $S_0$ may vary with $n$.
- **G.** $y^r=\alpha^*\mathbf 1+X^r\beta^*+\varepsilon$, $\varepsilon\sim N_n(0,\sigma_*^2I)$, $\sigma_*^2>0$ fixed;
  $\mu=X\theta^*$, $S_0=\operatorname{supp}\beta^*$.
- **R.** $\|\mu\|^2\le Mn$ and $\lambda_{\min}(R_{S_0})\ge\varphi_0^2>0$, with $M,\varphi_0$ fixed.
- **Size-tail objects (data-free).** $q_k:=\binom pk w(k)$. For every integer $m$,
  $R_m:=\sum_{k=\max(m+1,0)}^{K}q_k/w(s_0)$ (empty sum $=0$, so $R_m=0$ for $m\ge K$). For real $\omega$,
  $m^\sharp_n(\omega):=\min\{m\in\mathbb Z:m\ge s_0,\ R_m\le n^{-(s_0+1)/2}e^{-\omega}\}$ (exists, $\le K$);
  $m^\sharp_n:=m^\sharp_n(\tfrac12\log n)=\min\{m\ge s_0:R_m\le n^{-(s_0+2)/2}\}$. It is a deterministic function of
  $(n,p,s_0)$.
- **SE$_\lambda(j_0)$** (normalised, anchored, bounded size): $j_0:=\lceil(2A+1)s_0\rceil+1$ $(=j_*)$, and
  $\lambda_{\min}(R_{S_0\cup J})\ge\varphi_0^2$ for every $J\subseteq[p]\setminus S_0$ with $|J|\le j_0$.
- **SE$_w(m^\sharp_n;g_0)$** (unnormalised, anchored): $g_0>0$ a **fixed** constant, and
  $\lambda_{\min}(G_{S_0\cup J})\ge g_0$ for every $J\subseteq[p]\setminus S_0$ with $|J|\le m^\sharp_n$.
- **Beta-min** (for clauses 1–3 only), one of:
  **BM-∞**: $\min_{j\in S_0}\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)$ with a deterministic $M_n\to\infty$;
  **BM($c$)**: the same with a fixed $c>c_0(s_0,A):=L_*$.

## 3. Claims (record: `sources/statement/W6-FIXREV2_STATEMENTS.md:51-61`, verbatim up to notation; proof: `sources/W1-T03R/PROOF.md:168`)
**Theorem T03♯** (claim id `W3-T03ACC:T03S`, one clause per row of the council table). Assume R1, G, R, SE$_\lambda(j_0)$
and SE$_w(m^\sharp_n;g_0)$; for clauses 1–3 also BM-∞ or BM($c$) with $c>c_0(s_0,A)$.
1. **`T03S.1`** $1-\pi(S_0)=O_{P_0}(r_n)$.
2. **`T03S.2`** For every data set, $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0)$; hence $P_0(\mathrm{MPM}=S_0)\to1$.
3. **`T03S.3`** $P_0(S^\dagger\ne S_0)\le2E_0[1-\pi(S_0)]\to0$, where $S^\dagger$ is the global HPM. (Only convergence
   is claimed: boundedness of $1-\pi(S_0)$ turns convergence in probability into convergence of the expectation, not
   into an $O(r_n)$ bound on it.) On the event $\{\pi(S_0)>\tfrac12\}$, $S_0$ is the strict global maximiser of $F$, so
   no tie rule is used.
4. **`T03S.4`** (No beta-min.) For fixed $c>c_0(s_0,A)$ let $J_n(c):=\{j\in S_0:\theta^{*2}_j\ge c\sigma_*^2\log n/(n\varphi_0^2)\}$.
   Then $\Pi(S\not\supseteq J_n(c)\mid y)=O_{P_0}(r_n)$ and $1-\min_{j\in J_n(c)}\mathrm{PIP}_j=O_{P_0}(r_n)$, with the
   convention $\min_\emptyset:=1$ (the claim is vacuous when $J_n(c)=\emptyset$). The same holds for
   $J_n^\infty=\{j:\theta^{*2}_j\ge M_n\sigma_*^2\log n/(n\varphi_0^2)\}$ with any deterministic $M_n\to\infty$.
5. **`T03S.5`** Scale invariance as in the locked T03: for every $c>0$, replacing $(\theta^*,\sigma_*^2)$ by
   $(\theta^*/c,\sigma_*^2/c^2)$ (in particular $c=s_y$) leaves the BM-∞ and BM($c$) inequalities and the sets
   $J_n(c)$, $J^\infty_n$ unchanged (`sources/P3/STATEMENT.md:43`, `sources/P3/PROOF_v2.tex:380`).

Card form (approved wording, `sources/statement/TLF_434-499.md:29`): "Under R1, G, R, SE$_\lambda(j_0)$,
SE$_w(m_n^\sharp;g_0)$, and BM-∞ or BM$(c>c_0)$, $1-\pi(S_0)=O_P(\sqrt{\log n/n})$; exact HPM and MPM are consistent.
Without beta-min, for $J_n(c)=\{j\in S_0:\theta_j^{*2}\ge c\sigma^2\log n/(n\phi_0^2)\}$, $c>c_0$,
$\pi(S\not\supseteq J_n(c))=O_P(\sqrt{\log n/n})$, hence all corresponding exact PIPs converge to one. Empty $J_n(c)$
gives a vacuous inclusion statement." Card ↔ record: "exact HPM and MPM are consistent" = clauses 2–3; the
inclusion sentence = clause 4; clause 5 and the "for every data set" inequality of clause 2 are in the record only.

**What the theorem is about.** The exact posterior $\pi$ (algorithm-free). It says nothing about the sampler's
reported HPM. The record's "Scope" paragraph (`sources/statement/W6-FIXREV2_STATEMENTS.md:63-81`: Prop. E3, Prop. D,
the finite-$n$ thresholds of the written proof) is context, not part of the claim, and is not under review here.
No expectation rate is inferred from $O_P$; no universal onset $n_0$; fixed design, fixed $s_0$
(`sources/statement/TLF_434-499.md:30`).

## 4. Readings made explicit (forms of the record, not changes)
1. **$s_0\ge1$.** Record and card state $s_0\ge1$; the proof's R allows $s_0$ fixed (`sources/W1-T03R/PROOF.md:162`).
   The claim is restated for $s_0\ge1$, as recorded. With $s_0\ge1$ the proof's side condition "$S_0\cup J\ne\emptyset$"
   in SE$_\lambda$, SE$_w$ (`PROOF.md:131-132`) is automatic.
2. **$J=\emptyset$ in SE$_\lambda$** gives $\lambda_{\min}(R_{S_0})\ge\varphi_0^2$, i.e. R's eigenvalue condition. Since
   $\operatorname{diag}R_{S_0}=1$, R forces $\varphi_0\le1$.
3. **$A\ge1$.** The proof's R (`sources/common/00_COMMON.md:36`, `sources/P3/STATEMENT.md:19`) has "$p\le n^A$, $A\ge1$";
   record and card say "$A$ fixed". Any $A<1$ is covered by applying the theorem with $\max(A,1)$, at the price of
   $j_0$, $c_0$ computed at $\max(A,1)$. The restatement carries $A\ge1$ explicitly.
4. **$p\ge2$.** The proof assumes $p\ge2$ (`sources/W1-T03R/PROOF.md:9`: "for $p=1$ every statement below is trivial or
   void"). Under R1 with $s_0\ge1$ and $p=1$, $\Omega=\{\emptyset,\{1\}\}$; the reviewers are asked to confirm the
   $p=1$ remark or to name it as a hypothesis.
5. **$\sigma$ vs $\sigma_*$; $\theta^*_{\min}$.** The card's $\sigma^2$ is $\sigma_*^2$ of G; $\theta^{*2}_{\min}=\min_{j\in S_0}\theta^{*2}_j$.
   The card's BM-∞ "$\theta^{*2}_{\min}n\phi_0^2/(\sigma^2\log n)\to\infty$" is the record's BM-∞ with
   $M_n:=\theta^{*2}_{\min}n\varphi_0^2/(\sigma_*^2\log n)$.
6. **$c_0$.** The card writes $c_0=\max\{4C_*,32[s_0(A+1)+2]\}$ "with $C_*$ the locked T03 proof constant"; the record
   writes $c_0=L_*$; §1 gives $C_*$ explicitly from `00_COMMON.md:38`. It is a constant of the proof, not a sharp value.
7. **Thresholds.** The $n_0$ of the proof depend on $(s_0,A,\varphi_0,\sigma_*^2,M,g_0)$, on $c$ under BM($c$), and on the
   sequence $M_n$ under BM-∞ (`sources/W1-T03R/PROOF.md:170`). "$O_{P_0}$" and "$\to0$" are asymptotic statements along
   the triangular array.
8. **$\pi(S_0)$ before $s_0\le K$.** Defined as $0$ for the finitely many $n$ with $s_0>K$ (`sources/P3/STATEMENT.md:52`).

## 5. What the proof consumes (statuses verbatim)
The proof under review is `sources/W1-T03R/PROOF.md` §§1, 2, 4, 6 (E1, E2(i), den′, T02(i♯), Lemma I, Lemma B, (C1)–(C10),
Assembly). §3 (Prop. D), Prop. E3 and §5 (T02(ii♯)) are not used by T03♯ and are out of scope.

| consumed result | where used in PROOF.md | labels | status (verbatim) and source |
|---|---|---|---|
| **[P1]** T01 (locked) | den′ (`:89-91`), T02(i♯) proof (`:93-97`) | `lem:spec`(b),(e), `lem:prior`(a)–(d), `lem:chi`, `lem:slab`/`lem:IGint` via `lem:den`, `thm:T01iii`, `thm:Ta` | SOP:TH09 row: "T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY" (`sources/statement/registry_theory_main_L68.tsv`); NBH TH121: "PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY" (`Theory_work/Old_Projects/New_BVS_Headquarters/ID_REGISTRY.md` TH121) |
| **[P1]** T02(i) machinery (locked) | den′, T02(i♯) | `lem:num`, `lem:den` (body, without its last factor) | NBH TH122: "PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY; the (i) form is superseded for use by TH125 (T02(i-sharp))" |
| **[P3]** T03 (locked) | (C1)–(C10), Assembly | `lem:red`, `lem:smoother`, `cor:diff`, `lem:det`, `lem:prior`, `lem:signal`, `lem:chi`, `lem:Gprob`, `lem:ongood`(a)–(d), `lem:onesup`, `prop:sup`, `lem:SvsSp`, `lem:signalgain`, `lem:assemble`, eqs `eq:mn`, `eq:score`, `eq:tail`, `eq:kappa`, §`sec:main` paragraphs (i)–(v) | NBH TH123: "PROVED-LOCKED (wave 3; statement checker approved; two review rounds, both reviewers verified; external OpenAI review queued); MEET-THM flag SAME-FAMILY-ONLY; numerical check 1958/1958; statement unchanged; conditional on H-T02 which T02(i) closes" |
| T02(i♯) | (C9) | `PROOF.md` §2 | inside the proof under review; checked here (NBH TH125: "PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R row 10); XF VERIFIED (A-REV2 section 2: den-prime and T02(i-sharp); quantifier is sup_m P, not P(sup_m)); final card C9: PROVED, SF/XF VERIFIED") |

[P3] is conditional on H-T02; T03♯ does not use H-T02 (`PROOF.md:166`): its Step 0 is replaced by T02(i♯) via (C9).
Because T01–T03 are SAME-FAMILY-ONLY, the line checks (PLAN.md) cover every [P1]/[P3] step listed above as well as
the changed steps, so that no consumed step stays below a cross-family check.

## 6. Changelog (v4 §4.2)
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| 1.0 | all | — | initial restatement for the lock | — | SL1 (pending) |
