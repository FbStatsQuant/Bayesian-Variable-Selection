# Final council, round 1 — Sol

**Verdict: CHANGES REQUIRED.** The new CAP argument and the corrected Proposition F assembly survive this review. The remaining objections concern the chapter's transcription of imported results: probability spaces, the EP tail cutoff, a missing random-design alternative, and the allocation hypothesis of Theorem D. These matter in a document that promises paper-ready statements with their hypotheses written out. I found no blocking counterexample to the new mathematics under its stated contracts.

Paths below are repository-relative; `FINAL/`, `C-MIS/`, `C-DLV/`, and `C-PACK/` abbreviate the corresponding directories inside `Theory_work/Wave1C/`. I read the brief, the chapter, F1 and its disposition, the cited statement/proof passages, the eight ticket reports, the relevant SoP cards/method/notation, and the supplied Song–Liang main-text PDF. I did not read the other final-council seat's report. No git commands were run. Only this file was written.

## Gate verdicts

| Gate | Verdict | Reason |
|---|---|---|
| G1 | **FAIL** | The EP tail-discharge statement omits the source's prescribed cutoffs and their accompanying eigenvalue hypothesis; GEN(C4) omits its favourable alternative. N1's fixed-data probability convention and Theorem D's sufficient allocation need explicit restoration. Findings 1–4. |
| G2 | **PASS** | Ticket statuses and council scores/rounds agree with the reports. C-DLV remains PARTIAL; its original fallback result is distinguished from A1's corrected assembly. CAP and the corrected assembly are explicitly identified as not previously councilled. Candidate, AUTHOR-ONLY and LH SAME-FAMILY-ONLY dependencies are not silently promoted. |
| G3 | **PASS** | CAP(a)–(c) are correct under L1–L4 and the exact-branch convention. The positive transfer list is valid, with the stated cost/flag/negative-result exclusions. Proposition F includes the total fallback, complete-grid preservation, amended work/memory allocation, machine premises and inherited statistical qualifications. See the independent checks below. |
| G4 | **PASS** | The main-text map correctly distinguishes Hellinger/density results from exact-support results, sensitivity from specificity, and posterior statements from estimates produced by a sampler. The positive-power lower-growth assumption, fixed-subset misspecification scope, binding-cap caveat, parallel accounting and uninspected Theorem S qualification are retained. I checked printed pp. 950–959, 968–970 in the supplied PDF. No claim to have inspected the supplement is warranted or made. |
| G5 | **PASS** | The chapter discloses asymptotic onsets, polynomial dimension, fixed sparsity, the S5/factor frontier, practical finite-n gaps, shipped-calibration delivery, pooled-PIP limitations, EP/GR limitations, quadratic memory, exact-arithmetic idealisation and unshipped LS0/integration obligations. Proposition F is expressly about the abstract allocated machine and is not extended to the GROW class. |
| G6 | **FAIL** | The sampler identities do not identify their fixed-data probability space, the favourable random-design branch used by the study-coverage paragraphs is missing from the displayed GEN(C4), and Theorem D does not explicitly import its allocation inequalities. The two MR1 names and the original/enlarged LS0 caps are otherwise clearly distinguished. |

## Independent checks of the new mathematics

**CAP.** I checked `Scripts/SMC_BVS/core/cpp/v3_engine.h:370-418` against `Theory_work/State_of_Project/sections/02_method.tex:463-506`. The relevant order is scan, strict-improvement test, cap test, then move. Thus at cap (a) the search has moved (a) times but still scans (C_a); if it finds another improvement, its returned neighbour need not be a scanned centre. The chapter handles this correctly: the returned neighbour is already in (N(C_a)), and certification is asserted only when the terminal centre has actually been scanned without an improvement. Exact score ties do not induce a move; deterministic lexicographic neighbour selection makes both paths identical before the smaller cap.

For finite integer caps, induction gives precisely the chapter's scored-set formula. If the smaller search certifies, the larger one stops at the same iteration. On completed SMC branches the pre-LS0 set is common; exact enumeration already scores all feasible models; a schedule-limit branch executes neither LS0. GUARD-W then supplies the actual/potential coupling needed by part (c). The argument does **not** require the smaller-cap actual fit to have delivered when the larger one delivers. This is why use of the smaller-cap *potential* discovery event is correct.

As an additional falsification check, I ran an in-memory discrete-landscape check of the coded scan/cap control flow: all feasible starts for p=1,…,5, K=min(p,3), 100 tied integer score landscapes per dimension, and cap pairs 0≤a≤a′≤5. All **115,500** comparisons passed the move-count, scan-prefix, scored-set inclusion, certified-run identity and unique-global-maximum retention checks. This corroborates the proof; it is not a test of merged C-ENG code or of the statistical hypotheses.

The transfer list is appropriately limited. PXN's certified-endpoint and on-event scan-count clauses transfer because the certified runs are identical. GEN discovery needs the original onset or the new cap's own descent threshold. The C-MIS and SL2 compositions transfer through discovery/retention. GEN(C6)'s capped-search failure does not transfer. Stores can evict nontruth models, metadata can change, and actual delivery is not monotone in runtime. The chapter correctly says all of these.

**Corrected Proposition F.** I checked the statement against `C-DLV/lemmas/L1_resources.md:14-52,70-108,129-143`, `L2_degenerate.md:5-35`, `L4_delivery.md:24-41,51-91`, and `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md:37-75`. The completed pilot is a valid fallback because its nonfinal increments are at least (1/T_1), its endpoint is exactly 1, and it has at most (T_1) intervals. A prior successful tier-1 construction also has the required endpoint, strict-progress and interval-cap properties. Neither needs restricted-ESS success for the final frozen-grid run to be defined.

The statement terminates at the first failed tier-1 construction, retains a complete grid rather than the failed prefix, preserves the tier budgets/state and freezes before final randomness. It therefore removes the remaining schedule-limit branch without adding calibration work. The extra LS0 cap adds at most (Kq(p)) score requests and O(K(K+1)) archive words; its work increment charges the score/cache/store bound from L1. The time allocation has both the doubled actual-work bound and the separate exact-preflight bound. The resulting finite-n delivery assertion remains conditional on MACH's allocation-success, dependency and environmental clauses, as it must.

Consistency then follows directly from

`P(output and HPM != S0) <= 2 E[1-pi(S0)] + P(prescribed LS0 misses S0)`.

The last probability decreases under the larger cap, and the class-specific data/search theorems do not depend on the calibration law. This justifies dropping CAL and any probability bound on triggering fallback. It does not prove a statement for arbitrary fixed sparsity/polynomial dimension alone, for physical floating point, or for the GROW statistical class; the chapter preserves those qualifications.

## Findings

1. **MAJOR — N1 omits the fixed-data probability convention of its source.**

   Chapter: `FINAL/sections/s4_sampler.tex:5-18`, especially the conditional expectations at lines 13 and 18. Source: `Theory_work/Wave1/W1-N1/STATEMENT.md:18-25,62-66,98-111` explicitly fixes the data and takes all probabilities over algorithmic streams only.

   The chapter begins with a sampling model and uses joint data/algorithm probabilities elsewhere, but §4 never says that `(X,y)` is fixed for N1 and E. Under that surrounding joint law, conditioning only on the calibration record does not in general make `Z*pi(h)` measurable. Already h=1 requires a distinction between `E[Z_hat | calibration]` and `E[Z_hat | data, calibration]`. Freezing a grid before stream 10 does not itself condition on the data. F1's localisation repair fixes the island-existence issue, not this separate probability-space issue.

   This is a missing qualification in the transcription, not a failure of the source N1 theorem. Exact insertion immediately before the first paragraph of §4.1:

   > Throughout this subsection, fix an admissible standardised data set $(X,y)$, with $n\ge3$ and $p\ge1$. All expectations and almost-sure assertions in Lemma N1 and Corollary E are over the algorithm's streams only; $Z$, $\pi$ and $S_0$ are fixed. If these identities are embedded in the joint sampling law, condition additionally on $(X,y)$, retaining the same localisation on $E_r$.

   Alternatively write every displayed conditioning sigma-field as `sigma(X,y,calibration)`. Keep the current localisation and bounded/measurable-h restrictions.

2. **MAJOR — Theorem F's tail-discharge clause loses the cutoff required by Corollaries F(a)/F(b), and its local hypotheses need to be defined.**

   Chapter: `FINAL/sections/s3_posterior.tex:48-49`. Sources: `C-MIS/STATEMENT.md:124-141`; `C-MIS/lemmas/L4_theoremF.md:13-20,60-62,148-162,193-194`.

   The theorem first allows a general cutoff `s <= m_n <= min(K,C log n)` and assumes `SE_w(m_n;g0)` and `TAIL(m_n)`. It then says the tail assumption is discharged for bounded candidate dimension or under TL, without changing `m_n`. That is not the source's statement. For bounded dimension the source selects `m_n=m_sharp=K` eventually. Under TL it proves the tail at `m_n^T`, then uses `m_n=min(K,max(m_sharp,m_n^T))`, with the eigenvalue hypothesis imposed at **that enlarged cutoff**. A tail bound above a larger threshold does not establish a tail bound above an arbitrary smaller threshold. Naming Lemma T without its cutoff does not carry this hypothesis into the printed theorem.

   The same line leaves `kappa` in TL without its source restriction, a fixed `kappa in (0,1)`. It also uses undefined `R^C`. Here `R^C` bounds the **full** mean `||mu_c||^2`, not just the projected candidate mean; compare the different candidate substitution used for H-MIS at chapter line 41. The F proof uses this full-mean energy bound explicitly at L4.4(a).

   Exact insertions/replacement, using the chapter's notation:

   > Put $N=n-1$. Let $U^\top U=I_N$, $UU^\top=C$, $\mu_c=U^\top X^r\beta$, and $X_{c,\mathcal C}=U^\top X_{\mathcal C}$. Here $R^{\mathcal C}$ means $\|\mu_c\|^2\le Mn$ and $\lambda_{\min}(\hat R_{S_0^{\mathcal C}})\ge\phi_0^2$ for fixed constants; the energy bound is on the full mean.

   Replace the sentence beginning “TAIL is discharged” by:

   > TAIL$^{\mathcal C}$ may be removed (a) for bounded $p_{\mathcal C}$, taking $m_n=m_n^\sharp=K$ eventually; or (b) if, for a fixed $\kappa\in(0,1)$, (TL) $\sigma^2/[\Delta_n+\sigma^2(1-d_n/N)]\le\frac34(1-\kappa)$ eventually. In (b), Lemma T supplies a deterministic $m_n^T=s_0^{\mathcal C}+\lceil C_{\kappa,s_0^{\mathcal C},A}\log n\rceil$ with $\pi_{\mathcal C}(|S|>m_n^T\mid y)=O_P((\log n)^{s_0^{\mathcal C}}/n)$. Take $m_n=\min(K,\max(m_n^\sharp,m_n^T))$ and require SE$_w(m_n;g_0)$ at this cutoff; all other hypotheses of Theorem F remain.

   This restores the proved corollaries without suggesting that TL supplies TAIL at every cutoff admitted by the conditional theorem.

3. **MAJOR — GEN(C4) drops the favourable random-design alternative that the chapter subsequently uses.**

   Chapter: `FINAL/sections/s5_hpm.tex:52,54,56` and the study-coverage table at lines 95–99. Source: `Theory_work/Wave1/W1-GEN/STATEMENT.md:112-120`; proof: `Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md:66-77`.

   The chapter states C3-fav correctly, but its C4 quantifier requires every design sequence to satisfy H0–H2. The source has a second branch requiring only H0 and H2 when `S*=S0`, and transfers C3-fav on that branch. The study instances are then described as favourable cases “via (C4)”, although this branch is absent from the printed C4. Silently retaining H1 would narrow the result and defeat the advertised reason for using C3-fav; silently omitting it while applying the printed C4 would change that statement's hypotheses.

   Exact replacement for C4:

   > (C4) Random designs: let $X^r$ be independent of $\varepsilon$, with $\beta$, $\mathcal V_n$ and $S_n^*$ allowed to be $X$-measurable. If every deterministic sequence in measurable design sets $\mathcal A_n$ with $\PP(\mathcal A_n)\to1$ satisfies (H0)–(H2), respectively (H0), (H2) with $S^*=S_0$, with the same fixed constants and the same deterministic beta-min and VIS envelopes, then the conclusions of (C3), respectively (C3-fav), hold under the joint law.

   The full-class constants/envelopes can remain those already cited. No new random-design proof is necessary.

4. **MAJOR — Theorem D needs the sufficient allocation hypothesis, not merely a valid allocation.**

   Chapter: `FINAL/sections/s6_delivery.tex:4-12,16-17`. Source: `C-DLV/lemmas/L4_delivery.md:6-9` explicitly assumes the declared allocation **as in Corollary R**; `C-DLV/STATEMENT.md:43-46` distinguishes validity of the two positive finite fields from the lower-bound requirement. Corollary R is `C-DLV/lemmas/L1_resources.md:129-143`.

   The chapter's setting says “valid declared seed and allocation”; it never explicitly imposes Corollary R's lower bounds on Theorem D. Saying that the allocation is polynomial is insufficient: a tiny constant allocation is polynomial and valid. If interpreted literally with only the printed assumptions, an allocation with `mem_gb=2^-40` is a counterexample to D(i): the positive preflight byte estimate causes `resource_limit` before calibration, so no schedule-limit event is involved. See `Scripts/SMC_BVS/core/v3_fit.R:17-45,66-69,88-90`. MACH does not turn an insufficient declared memory budget into a sufficient one.

   The setting's citation to C-DLV may be intended to import the stronger allocation definition; this should be made explicit rather than left to distinguish two meanings of “valid/declared”. Proposition F already writes out its amended allocation correctly. Exact insertion before Theorem D:

   > In Theorem D and Corollary D′, the declared allocation satisfies C-DLV Corollary R: $\mathrm{mem}_n\ge\max\{\beta\bar M(n,p_{\rm raw})+\beta_0,P_0,P_1\}$ and $\mathrm{time}_n\ge\max\{2[\tau\bar W(n,p_{\rm raw})+\tau_0],\bar P_t\}$, with $\texttt{allocation\$mem\_gb}\ge\mathrm{mem}_n/2^{30}$ and $\texttt{allocation\$hours}\ge\mathrm{time}_n/3600$. These statements use LS0 cap $\ell_n$; for the GROW cap use A1's amended envelopes as specified in Proposition F.

   Then the resource-path exclusion in the supporting-results paragraph has its actual hypothesis, and D′ has the delivery lower bound claimed. This finding does not invalidate the separately allocated Proposition F.

5. **MINOR — Complete the local definitions and inherited execution conditions used by the statements.**

   Chapter: `FINAL/sections/s3_posterior.tex:11,24`; `FINAL/sections/s5_hpm.tex:13,16`. Sources: `Theory_work/State_of_Project/sections/04_theory.tex:778`; `C-PACK/lemmas/I4_SL_corollaries.md:16-18`; `C-PACK/lemmas/I1_e4_replacement.md:72-79,145-154`; `C-PACK/METHOD_REQUIREMENTS.md:6-10`.

   BM(c) is named but its actual inequality is not defined locally; Lemma UM uses `f` without defining it; the explicit e4′ transcription omits the source's cap/execution restrictions on the coded routine; SL0 uses maxima over possibly empty coordinate sets without the source's zero convention. These are easy repairs, but the chapter's “hypotheses are written out” promise makes the omissions worth fixing.

   Add:

   > BM$(c)$ means $\theta_{\min}^{*2}\ge c\sigma^2\log n/(n\phi_0^2)$ eventually. Every maximum of nonnegative coordinate errors over an empty set is defined as zero. In Lemma UM, $f(S)=\log w(|S|)+\sum_b\log r_b(S\cap C_b)$, up to a model-independent normalising constant. The coded-routine option in e4′ retains W1-N3's encoding/execution conditions H1 and H4, and an enumeration cap at least one (fixed in advance or a specified deterministic measurable data function satisfying H3–H4).

   This does not require the lexicographic tie fallback for positive consistency proofs; it simply states the conditions under which the cited coded-routine result applies.

SCORE: 7.4/10; GATES: G1 FAIL; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 FAIL
