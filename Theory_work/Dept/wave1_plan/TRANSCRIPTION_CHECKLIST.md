# TRANSCRIPTION CHECKLIST (Wave 2 proofs → paper and supplement) — Lead-A v0.1, 2026-11-28

Every Wave 2 proof file and every Writing transcription is ticked against this list before council review. T-1 to T-5
are the packet's §4 (they must survive transcription); T-6 onwards are added by Lead-A from the proof plan.

| ID | Item | Applies to | Where it is checked |
|---|---|---|---|
| T-1 | The capped comparison window covers $\min(p,m+s_0)$; comparison unions $S_0\cup J$ are **clipped at $p$** (the false inequality $s+m^\sharp_n\le q_n$ when $q_n=p$: [B3] Amendment A-1) | D, S | D-2(1); S-1 |
| T-2 | The sample-mean (intercept) term $\bar\varepsilon^2$ appears in the population distance | D, M(i) | D-2(2); M-3 |
| T-3 | The starting $n$ may depend on $M$: "for every fixed $M\ge M_0$ and all $n\ge n_0(M)$" | D, M1(i) | D-2(3) |
| T-4 | Selection assumes $s_0\ge1$ ($s_0^{\mathcal C}\ge1$ in Cor M1(ii)); $s_0=0$ is not claimed | S, M1 | S-0 |
| T-5 | No response-dependent scaling before conditioning on the design: the scale reduction uses deterministic $(\alpha^*,\sigma_*)$, and $\theta^*$, $J^{\rm samp}_n$ are design-measurable | S, D | S-5; L-SCALE |
| T-6 | The beta-min constant is strict: $C>C_{\rm sel}=4\sqrt{c_0}/\varphi$ gives a common $c=C^2\varphi^2/16>c_0$ for all $p\ge2$; $c_0$ is maxed over $1\le s_0\le s$ | S | S-2 |
| T-7 | $s_0$ may vary with $n$ in $\{1,\dots,s\}$: the subsequence argument (R1 assumes $s_0$ fixed) | S, M1 | S-0 |
| T-8 | Population strong set $J_n$ (defined by $b_j$) vs sample $J^{\rm samp}_n(c)$ (defined by $\theta^*_j$): $J_n\subseteq J^{\rm samp}_n(c)$ on the design event | S(a) | S-2 |
| T-9 | The candidate set $\mathcal C$ is fixed before the data (or chosen on independent data); Cor M1 is conditional on $\mathcal C$ | M, M1 | M-5 |
| T-10 | $p$ = raw dimension; $p_{\rm ret}=p$ on the design event; exceptional data sets (fewer than 2 non-constant columns, constant $y$) count as failures | all | D-3; S-4 |
| T-11 | Units: $b_j=|\beta^*_j|\operatorname{sd}(x_j)/\sigma_*$ uses **population** sd and $\sigma_*$; coded $\theta^*_j=\hat s_j\beta^*_j/\sigma_*$; $\hat s^2_j\ge\operatorname{Var}(x_j)/2$ on L-DES | S, M1 | S-2 |
| T-12 | Hellinger normalisation: $d_H$ = SL's distance divided by $\sqrt2$; the conversion of SL's $\exp(-c_1n\epsilon^2)$ to $n^{-c_1M}$ | D | statement |
| T-13 | A7′(a) is anchored ($S_0\cup J$, $|J|\le j_0$), window $\le\min\{p,s_0+j_0\}$, $j_0=\lceil(2A+1)s_0\rceil+1$; A5 on the logarithmic window $q_n(1)$; the two floors are not conflated | S | S-3 |
| T-14 | Constants: $c_H,M_0$ depend only on $(s,A,L,c_\psi,\bar b,a_0,b_0)$; $C_{\rm sel}$ only on $(s,A,\varphi)$; the paper states which constants are explicit | D, S | statements |
| T-15 | Under A8 nothing uses a Gaussian-likelihood identity of the truth (e.g. $E^*[m_b/f_0]=1$, exact $\chi^2$ laws) | M | M-3, M-4 |
| T-16 | Thm M(ii) is a.s. (stronger than SL's in-probability Cor 2); (iii)'s moment hypothesis is $E(x_j^2\varepsilon^2_{\mathcal C})<\infty$ for $j\in\mathcal C$ (the intercept needs only $E\varepsilon^2_{\mathcal C}<\infty$) | M | M-2, M-4 |
| T-17 | Terminology: "high-dimensional", $p\le n^A$; never "ultrahigh" | all text | Writing |
| T-18 | Status words in headers: only DRAFT / PROMISING / DEFINITIVE with a check record; reconcile old headers (`RECONCILIATION.md`) before the supplement cites them | all | §5 of the plan |
| T-19 | The old draft Thm 3.2 is not claimed as a special case of Cor S1 (non-nesting note in [LS]) | S, Writing | [LS] Cor S1 |
| T-20 | $C_{\rm sel}$ labelled "not sharp"; the numerical value with its units (≈111.4 uniform; ≈49.8 at $p=n^2$) only in the supplement | S, Writing | [LS] Thm S note 1 |
| T-21 | $f_0$ is defined by the expected Gaussian log score; "KL projection" is used only when a finite-KL working law exists (discrete $y$) | M | [LS] Thm M note 3 |
| T-22 | A8 is one fixed law and one i.i.d. sequence; no $n$-dependent law in Thm M | M | [LS] A8 |
