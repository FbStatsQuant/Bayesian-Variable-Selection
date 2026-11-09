# F1 ? adversarial fidelity review

Verdict: **FAITHFUL-WITH-FIXES**.

Severity counts: **FATAL 0 / MAJOR 5 / MINOR 5 / NIT 0** (10 findings).

Lemma CAP: **VERIFIED-WITH-AMENDMENTS** (finding 6). Its finite-integer-cap prefix argument, discovery monotonicity and joint-with-output bound are correct under the stated ideal arithmetic and operational contracts. This is verification of the specified method, not of C-ENG's integration.

Aliases below are those of the chapter. Document locations beginning `sections/` are relative to `Theory_work/Wave1C/FINAL/`. No git commands were run. Only this report was written. Review concerns source fidelity and the new CAP argument; it does not independently re-prove the imported proof packages or certify PDF layout.

1. **MAJOR ? Lemma Z drops its Gram-floor hypothesis and fixed-design scope.**

   Document: `sections/s3_posterior.tex:49` (last sentence).

   Source: `W1C/C-MIS/STATEMENT.md:101-105`; `W1C/C-MIS/lemmas/L6_null.md:6-12`.

   The source requires a fixed candidate design and `lambda_min(X_C^T X_C) >= g_0 > 0` eventually, in addition to bounded candidate dimension. Neither condition appears in the chapter's standalone parenthetical for Lemma Z. The preceding Theorem F conditions cannot safely supply them: F explicitly assumes nonempty projected support, whereas Z is a separate null-projection result. This broadens the imported claim beyond its proved hypotheses.

   Exact replacement for the Lemma Z sentence:

   > `\textbf{Lemma Z} (fixed candidate design): if $s_0^{\mathcal C}=0$, $p_{\mathcal C}$ is bounded, and $\lambda_{\min}(X_{\mathcal C}^{\top}X_{\mathcal C})\ge g_0>0$ eventually, then under GR, or under EP with $\theta^{\mathcal C}=0$, $1-\pi_{\mathcal C}(\varnothing\mid y)=O_P(n^{-1/2})$.`

2. **MAJOR ? GEN's centre hypotheses are not actually transcribed.**

   Document: `sections/s5_hpm.tex:46` (also inherited by the GROW reference to within-block SE at line 64).

   Source: `W1/W1-GEN/STATEMENT.md:65-79`; `W1C/C-GROW/STATEMENT.md:92-95`.

   ?Within-block SE?, ?the leakage family? and ?the averaged-leakage bound? have no mathematical definition in this chapter. In particular the exponential average, its normalization, its constants and its zero-denominator convention disappear. This is a material completeness failure for a document promising written-out hypotheses; it must not be read as replacing NL_avg by the displayed pointwise logarithmic bound alone.

   Exact replacement for H2a and H2c (retain the existing H2b):

   > `(H2a) $\lambda_{\min}(\hat R_T)\ge\phi_0^2$ for every nonempty $T\subseteq C_b$, every $b$. Define $\mathscr L(S^*)=\{(b,T,l):l\in C_b\setminus U_b^*,\ U_b^*\subseteq T\subseteq C_b\setminus\{l\}\}$. (H2c) For fixed $C_L<\infty$, $\kappa>0$, $\varepsilon_0>0$, require $\delta_{T,l}^2\le C_L\sigma^2\log n$ on $\mathscr L(S^*)$ and, if $p>s^*$, eventually $(p-s^*)^{-1}\sum_{l\notin S^*}\max_{T:(b(l),T,l)\in\mathscr L(S^*)}\exp(E_{T,l})\le n^{1/2-\kappa}$, where $h_n=\sqrt{2(A+\varepsilon_0)\log n}$ and $E_{T,l}=\min\{\delta_{T,l}^2/(2\Delta_T),\delta_{T,l}^2/(2v_T)+|\delta_{T,l}|\sigma h_n/v_T\}$; set $E_{T,l}=0$ when $\delta_{T,l}=0$ (in particular when $\Delta_T=0$). Omit the average when $p=s^*$.`

   Replace GROW's ?(G3a) within-block SE? by the explicit H2a inequality above. Restore also GEN's convention at `STATEMENT.md:60`: the SEP maximum is zero when `V=[p]`.

3. **MAJOR ? GROW weakens the strict descent events to non-improvement.**

   Document: `sections/s5_hpm.tex:68`, C1 parenthesis.

   Source: `W1C/C-GROW/STATEMENT.md:102-106`.

   ?No addition improves? and ?no truth-removing move improves? express non-strict inequalities. The source requires strictly smaller scores. Strict NA is essential: reversing an addition gives a strictly improving deletion. With equal scores, the advertised exact number of deletions does not follow because the coded search never moves on a tie. The chapter has not defined NA or TL elsewhere to resolve this ambiguity.

   Exact replacement for the parenthesis:

   > `where $\mathrm{NA}(\mathcal L)=\{F(T\cup\{l\})<F(T):T\in\mathcal L,\ |T|<K,\ l\notin T\}$ and $\mathrm{TL}(\mathcal L)=\{F(A)<F(T):T\in\mathcal L,\ A\text{ a feasible neighbour of }T,\ S_0\not\subseteq A\}$.`

4. **MAJOR ? GROW's subsidiary claims lose their hypothesis lists and fixed-constant restrictions.**

   Document: `sections/s5_hpm.tex:64-68`.

   Source: `W1C/C-GROW/STATEMENT.md:89-98,107-113`.

   C2 and C3 are printed without the source's antecedents, although C4 explicitly states its antecedents. G4-chi also omits `delta_0 in (0,1)` fixed; G3c omits `eta >= 0` and fixedness. Without a fixed positive delta_0, the chi-square argument's margin is not the source's claim. This cannot be repaired merely by saying all clauses assume H0--G4, which would silently add unnecessary hypotheses to the minimal subsidiary statements.

   Exact replacements:

   > `In (G1), $C_Q$ is fixed. In (G3b), $M_n\to\infty$ is deterministic; in (G3c), $\eta\in[0,(\sqrt{2A+1}-\sqrt{2A})^2)$ is fixed. In (G4-chi), $\delta_0\in(0,1)$ is fixed.`

   > `(C2) Under G, $\|\mu\|^2\le Mn$, $p\le n^A$, $|Q|\le C_Q\log n$, $|Q|\le K$, (G2) and BM-\infty, $\PP(\mathrm{TL}(\mathcal L))\to1$. Under the same hypotheses without BM-\infty, and with (G4), $\PP(\mathrm{NA}(\mathcal L))\to1$. (C3) Under G, $\|\mu\|^2\le Mn$, $p\le n^A$, (G1) and (G3), $\PP(S_0\subseteq\tilde S\subseteq Q\text{ for every maximiser }\tilde S\text{ of }\gamma_0\text{ on }\Omega)\to1$.`

5. **MAJOR ? AR(1) instances omit coefficient/noise assumptions and the corrected relevance-set construction.**

   Document: `sections/s5_hpm.tex:70`, instances (a), (c).

   Source: `W1C/C-GROW/STATEMENT.md:119-126,139-149`.

   The source requires `0<|rho|<1`, fixed nonzero standardized coefficients and fixed positive noise variance. The iid-row instance uses independent Gaussian noise in `Y=X theta*+C epsilon`; merely describing Gaussian design rows does not specify that model. Moreover the radius-only summary omits the v2.1 piecewise enlargement to all columns needed when the radius set violates G1's capacity margin. The chapter currently says the stated radius yields G1 for any `p<=n-1`, which is not the corrected construction.

   Exact insertion replacing ?relevance envelope of radius ...? in (a), to be inherited explicitly by (c):

   > `Assume fixed $\rho\in(-1,1)\setminus\{0\}$, fixed nonzero $\theta^*$ and fixed $\sigma^2>0$. Set $d_n=\lceil\log n/(2\log(1/|\rho|))\rceil$, $\mathcal P_n^0=\{l\notin S_0:\min_{k\in S_0}|l-k|\le d_n\}$ and $Q_n^0=S_0\cup\mathcal P_n^0$. Use $\mathcal P_n=\mathcal P_n^0$ if $Q_n^0=[p]$ or $p\ge2|Q_n^0|+32s_0+1$, and $\mathcal P_n=[p]\setminus S_0$ otherwise.`

   Exact insertion in (c):

   > `Raw rows are iid $N(0,\Sigma)$ with $\Sigma_{ij}=\rho^{|i-j|}$ and $0<|\rho|<1$ fixed. On standardized columns, $Y=X\theta^*+C\varepsilon$, with fixed nonzero $\theta^*$, $\varepsilon\sim N(0,\sigma^2I_n)$ independent of the raw design and fixed $\sigma^2>0$; the score uses $y=Y/(\|Y\|/\sqrt{n-1})$. Assume the separation inequality of (a), use its piecewise relevance set, and retain the implementation premises and MR1.`

6. **MINOR ? CAP needs integer caps, admissible inputs and explicit skipped-branch bookkeeping.**

   Document: `sections/s7_impl.tex:26,36-49`.

   Source: `CORE/cpp/v3_engine.h:385,413-420`; `PROD/cpp/v3_engine.h:378,406-413`; `W1C/C-PACK/item5_PXN_consolidated/00_statement_and_conventions.md:126-133`; `W1C/C-DLV/lemmas/L4_delivery.md:26-39,65-69`.

   The cap argument uses `k>=a iff k=a`, so it presupposes a finite nonnegative integer cap; a general measurable real data function does not satisfy the stated move-count formula. The coded argument is an `int`. Also not every branch executes LS0: exact enumeration and calibration failure need separate bookkeeping in part (b). This is readily repaired and does not defeat monotonicity.

   Exact replacement for the cap-domain sentence:

   > `Let $a,a'$ be finite integer-valued measurable functions of the admissible data, with $\ell_n\le a\le a'$. Couple the two methods with the same valid seed and ideal uniforms. The deterministic LS0 search is defined on every admissible data set even on branches that do not execute it; its scored set is distinguished from the set actually scored by the fit.`

   Exact insertion replacing the unconditional union argument in (b):

   > `On a completed SMC potential run, $\bar{\mathcal S}^+(a)=\bar{\mathcal S}\cup\mathcal S_{\rm LS0}(a)$, with the same pre-LS0 set. On the exact branch all feasible models have already been scored and the sets coincide for both caps. On a schedule-limit branch neither fit executes LS0 and their actual scored sets coincide; this branch is outside $\bar{\mathcal O}$. Thus the inclusions and the bound on $D_n$ hold on every branch.`

   The proof then verifies (a)--(c). Certification here is the local archive's certified endpoint; it does not independently assert the public finally-reported-model flag.

7. **MINOR ? The transfer list reverses a logical implication.**

   Document: `sections/s7_impl.tex:60`.

   Source: `W1/W1-GEN/STATEMENT.md:99-113`; CAP(a) at `sections/s7_impl.tex:38`.

   `a_n>=ell_n` does not imply `ell_n>=2^{vbar}-2`. The positive conclusion survives because the original onset eventually supplies the latter inequality, or because the new cap itself meets the descent threshold. This is a proof/exposition error, not a counterexample to transfer.

   Exact replacement:

   > `GEN (C2), (C3), (C3-fav), (C4) and the instances (C5)(a)--(d) retain their hypotheses and onsets. Whenever $\ell_n\ge2^{\bar v}-2$, also $a_n\ge2^{\bar v}-2$, so the discovery conclusion transfers. More directly, the capped search scores $S_0$ when $a_n\ge\tau(C)-1$ and has certified endpoint $S_0$ when $a_n\ge\tau(C)$.`

8. **MINOR ? The global finite-n disclaimer contradicts genuine finite-n results.**

   Document: `sections/s8_scope.tex:6` (?Everything is asymptotic. No finite-n guarantee is proved.?).

   Source: `W1C/C-PACK/item5_PXN_consolidated/00_statement_and_conventions.md:109-119`; `W1C/HQ_AUDIT/A1_propF_redteam.md:75`; `W1/W1-N1/STATEMENT.md:98-111`.

   The chapter includes deterministic all-n SL0/CAP, finite-n N1 identities and composition inequalities, and Proposition F's all-admissible-n delivery claim. The intended qualification is about quantitative finite-n statistical selection consistency on the study, not every theorem.

   Exact replacement:

   > `\textbf{Selection consistency is asymptotic.} No quantitative finite-$n$ selection-consistency guarantee is proved for the study. Deterministic inequalities, sampler identities and the ideal-machine delivery statement of Proposition~\ref{prop:F} retain their stated finite-$n$ scope.`

9. **MINOR ? PXN's explicit constants and quantifier are undefined.**

   Document: `sections/s5_hpm.tex:27-28`.

   Source: `W1C/C-PACK/item5_PXN_consolidated/00_statement_and_conventions.md:25-26,100-105`.

   The chapter uses `s`, `psi_bar`, `I`, `t*`, and `C` without the source definitions/quantifier. In particular the tail statement is for each fixed C with a C-dependent onset, not one unexplained constant.

   Exact insertion before PXN:

   > `Write $s=|S^\circ|=c+v$, $\bar\psi=\max_i|\psi_i|$, $q_R=\sqrt{(1-\bar\psi^2)/(1-\rho^2)}$, $t^*=(q_R-1)/(q_R\rho-\bar\psi)$ and $I(t;r)=-\frac12\log[(1-r^2)(1-t^2)/(1-rt)^2]$. In (R), for every fixed $C>0$ the bound $p^{-C}$ holds for $n\ge\max\{n_1,n_0(A,C,\rho,\bar\psi)\}$, where $n_1$ is the SIZE onset.`

10. **MINOR ? N1's localization event is unnamed and Corollary E does not restate localization.**

    Document: `sections/s4_sampler.tex:10,17`.

    Source: `W1/W1-N1/STATEMENT.md:29-35,94-111`.

    `mathcal A` is not defined in the chapter. The equality for an island that was never run is not an unconditional assertion; the source explicitly defines its localized conditional-expectation meaning. Corollary E should carry the same qualifier, rather than leave that crucial restriction to inference.

    Exact insertion before N1:

    > `Let $\mathcal A\in\sigma(\mathcal C)$ be the successful-calibration event, on which $0=\phi_0<\cdots<\phi_T=1$. Put $E_r=\mathcal A\cap\{r\le R'\}$. An identity $\EE[Y\mid\mathcal C]=b$ almost surely on $E_r$ means $\EE[1_{E_r}Y\mid\mathcal C]=1_{E_r}b$ almost surely; no island record is asserted outside $E_r$.`

    Exact insertion at the beginning of Corollary E:

    > `Under N1's named premises, almost surely on $E_r$ in the same localized sense, `

CAP transfer audit: no counterexample found to the positive PXN discovery/certified-endpoint clauses or its certified-event scan count; GEN discovery and assembly; C-MIS D/D-prime and H; SL2 discovery/retention; or C-DLV's pathwise consistency argument after amended allocation. The GEN(C6) negative result correctly is not transferred. Costs, stores, metadata and actual guard-dependent output events correctly are not asserted monotone. C-DLV D-prime's numerical delivery lower bound requires the amended resource allocation as the chapter later explains. Proposition F matches A1's corrected statement, including total fallback, all other caps unchanged, raw-dimension envelopes, both preflight maxima, machine premises and inherited LH SAME-FAMILY-ONLY qualification. No extension of delivery to GROW's random-AR(1) class is claimed.

Status/provenance audit: compared all eight ticket REPORT files with the chapter's status boxes and provenance council columns. Scores/rounds agree: PXN 8.6/8.3 r1; GEN 9.0/8.9 r1; N1 9.3/8.9 r1; N3 9.3/8.6 r1; C-PACK 9.0/8.7 r1 (items 1--4 only); C-MIS 9.2/9.0 r1; C-DLV 9.0/8.9 r2, with failed r1 7.6/8.6; C-GROW 9.2/9.0 r1. C-DLV remains PARTIAL, A1 remains HOLDS-WITH-AMENDMENTS, CAP remains unchecked in the document, and inherited candidate/AUTHOR-ONLY/SAME-FAMILY-ONLY qualifications are distinguished. No status upgrade found. Commit identities were not verified: git use was prohibited.

Song--Liang map audit: checked all 13 rows against C-PACK's map and the later MIS/GROW/DLV/A1 statements. No additional substantive row-level mismatch found. The chapter retains selection-versus-density distinctions, polynomial dimension, the different lower-growth domains, the uninspected Theorem S warning, the shipped pooled-PIP gap and the patched-calibration qualification. Abbreviated rows must be read with the repaired detailed statements above.

Content citation spot-checks (actual text inspected, not existence checks):

| Chapter citation | Content result |
|---|---|
| consistency.tex -> W1C/PROTOCOL.md:35 | PASS: verbatim-status rule and PROVED-CHECKED definition. |
| s2_map -> W1C/C-PACK/SONG_LIANG_MAP.md:10-12 | PASS: positive-power lower growth and different domains. |
| s2_map -> W1C/C-PACK/SONG_LIANG_MAP.md:14-28 | PASS: all map rows compared. |
| s3_posterior -> SoP/04_theory.tex:774-782 | PASS: anchored eigenvalues, cutoff, beta-min and posterior conclusion. |
| s3_posterior -> W1C/C-PACK/lemmas/I4_SL_corollaries.md:20-48 | PASS: SL0/SL1 inequalities and convergence modes. |
| s3_posterior -> W1C/C-PACK/lemmas/I4_SL_corollaries.md:53-68 | PASS: four instances and large-signal clause. |
| s3_posterior -> W1C/C-MIS/STATEMENT.md:54-58 | PASS: conditional GR, fixed variance and projected truth. |
| s3_posterior -> W1C/C-MIS/STATEMENT.md:64-95 | PASS: MIS, Gaussian projection and GD scope. |
| s3_posterior -> W1C/C-MIS/STATEMENT.md:101-105 | FAIL in transcription: omitted Gram floor (finding 1). |
| s3_posterior -> W1C/C-MIS/STATEMENT.md:126-141 | PASS: EP, TAIL and TL route; source cutoff conditions remain applicable. |
| s4_sampler -> W1/W1-N1/STATEMENT.md:95-111 | QUALIFIED: formulas agree; restore localization (finding 10). |
| s4_sampler -> W1C/C-PACK/lemmas/I4_SL_corollaries.md:90-103 | PASS: SL2 joint-with-output bound and deterministic thresholds. |
| s5_hpm -> W1C/C-PACK/item5_PXN_consolidated/00_statement_and_conventions.md:97-119 | QUALIFIED: main rates/events agree; constants omitted (finding 9). |
| s5_hpm -> W1C/C-PACK/patches/P_L8_certificate.md:7-13 | PASS: epsilon/kappa compatibility inequality. |
| s5_hpm -> W1C/C-PACK/patches/P_SEL_L6d.md:42-44 | PASS: no GEN hypothesis/conclusion change. |
| s5_hpm -> W1C/C-GROW/STATEMENT.md:84-117 | FAIL in compression: findings 3--4. |
| s5_hpm -> W1C/C-GROW/STATEMENT.md:118-149 | FAIL in compression: finding 5. |
| s6_delivery -> W1C/C-DLV/lemmas/L4_delivery.md:13-22 | PASS: reduction, three construction failures, null-set qualification. |
| s6_delivery -> W1C/HQ_AUDIT/A1_propF_redteam.md:60-75 | PASS: corrected Proposition F. |
| s6_delivery -> W1C/HQ_AUDIT/A1_propF_redteam.md:43 | PASS: NULL-grid hazard and preservation of a complete fallback. |
| s7_impl -> CORE/cpp/v3_engine.h:385-425 | PASS: strict improvement, extra scan, cap test, returned neighbour at limit. |
| s7_impl -> PROD/cpp/v3_engine.h:378-418 | PASS: same local-search control flow. |
| s7_impl -> SoP/02_method.tex:490-494 | PASS: LS0 order and no-uniforms contract. |
| s7_impl -> W1C/C-DLV/lemmas/L1_resources.md:24-25 | PASS: original cap-specific accounting. |
