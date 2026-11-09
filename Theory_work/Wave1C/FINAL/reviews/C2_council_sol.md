# Final council, round 2 — Sol

Object: `Theory_work/Wave1C/FINAL/consistency.tex`, its nine section files, and the 25-page draft-v2 PDF. Brief: `COUNCIL_BRIEF_R2.md` and `COUNCIL_BRIEF.md`. Independent verdict recorded before reading `C1_disposition.md`; no `FINAL/reviews/C1_council_*.md` was opened. No chapter, source, code, or git state was changed.

**Verdict: the three mathematical items newly submitted to council withstand this review, but the chapter needs two precise statement/consistency repairs before all gates pass.** The threshold-domain omission makes SL1(b) false literally as written. The frontier also contradicts the fixed-design EP theorem already stated in the chapter. Neither finding defeats CAP, corrected Proposition F, or Proposition F-GROW. One additional PDF formatting defect is nonblocking.

## Gate verdicts

| Gate | Verdict | Reason |
|---|---|---|
| G1 | **FAIL** | SL1(b) drops the source's explicit deterministic `q_n in (0,1)` domain, and its unrestricted fixed-q consequence has elementary counterexamples. Finding 1. The other substantive theorem transcriptions checked against the statements, amendments, and SoP cards retain their hypotheses and qualifications. |
| G2 | **PASS** | Ticket statuses and the separate frozen-registry statuses are distinguished. N1's proved ticket is not silently made an adopted registry result; N3's frozen-code failure and the integrated-e4 obligation remain visible. C-DLV remains PARTIAL, its P1/S.3 inputs remain audits, and A1/A2/A3 and CAP are not claimed to have passed this council already. The report trails support the displayed PROVED-CHECKED labels. |
| G3 | **PASS** | CAP, its positive transfers and exclusions, corrected F, and F-GROW are mathematically valid under the named premises. Independent verification is detailed below. No delivery conclusion is inferred from discovery alone, and CAL is not smuggled into the fallback propositions. |
| G4 | **PASS** | I read the supplied Song–Liang PDF, including printed pp. 950 and 952–958 and the time discussion on p. 968. The map correctly distinguishes density/Hellinger contraction from model selection; Condition 1 from the weaker Condition 2 result (16); screening from specificity; the positive-power lower-growth assumption from this chapter's polynomial upper bound; and density-level misspecification from GR/EP selection. Theorem S's uninspected supplementary hypotheses remain expressly uninspected. |
| G5 | **PASS** | The substantive scope is disclosed: polynomial p, fixed sparsity, impractical illustrative onsets, no n=200 selection guarantee, the S5/factor frontier, the shipped-calibration obstruction, no pooled shipped-R'=4 PIP consistency theorem, conditional implementation/precision claims, quadratic-memory envelope, and unmerged LS0/fallback engineering. The EP frontier itself is correctly given in §3.3; the contradictory short summary in §8 is assigned to G6 and Finding 2. |
| G6 | **FAIL** | §8 says exact-model concentration is proved “only under GR,” whereas §3.3 states and sources a fixed-design EP theorem, its two tail-discharge cases, and an EP null-projection result. Finding 2. Other cap, e4/e4-prime, two-MR1, and cross-reference checks passed; no duplicate labels or unresolved LaTeX references were found. |

## Numbered findings

1. **MAJOR — Restore the threshold domain in SL1; the present fixed-q assertion is false at the endpoints.**

   **Evidence:** `FINAL/sections/s1_setting.tex:13` defines `xi_q` without restricting q. `FINAL/sections/s3_posterior.tex:27` states thresholded-model consistency “in particular for fixed q,” without the source's domain. The same unrestricted summary occurs at `FINAL/sections/s2_map.tex:17`. The source explicitly defines `q in (0,1)` at `C-PACK/lemmas/I4_SL_corollaries.md:15` and requires “every deterministic q_n in (0,1)” at `:44`.

   **Counterexample:** Take fixed p=2, S0={1}, centred orthogonal design columns, fixed nonzero signal and Gaussian noise. This is a T03-sharp array, so the antecedent `delta_n=O_P(sqrt(log n/n))` holds. For every admissible finite data set, the D0 posterior gives positive mass both to the empty model and to each singleton. Hence each PIP is strictly between zero and one. Consequently `xi_0={1,2}` and `xi_1=empty` for every n, and neither equals S0. Thus the unqualified fixed-q sentence is false. Allowing q=-1 even satisfies the displayed little-o comparison in the usual ratio definition while also giving `xi_q=[p]`. The open-interval restriction must actually be stated; it cannot be supplied by the definition `PIP_j>q` alone.

   **Exact replacement text:**

   - In `s1_setting.tex:13`, replace

     ```tex
     $\xi_q:=\{j:\mathrm{PIP}_j>q\}$
     ```

     with

     ```tex
     $\xi_q:=\{j:\mathrm{PIP}_j>q\}$ for $q\in(0,1)$
     ```

   - In `s3_posterior.tex:27`, replace clause (b) by

     ```tex
     (b) for every deterministic sequence $q_n\in(0,1)$,
     $\PP(\xi_{q_n}=S_0)\to1$ whenever
     $r_n=o(\min(q_n,1-q_n))$, in particular for every fixed
     $q\in(0,1)$, and $\PP(\mathrm{MPM}=S_0)\to1$;
     ```

   - In `s2_map.tex:17`, replace “for fixed $q$ or $r_n=o(\min(q_n,1-q_n))$” by

     ```tex
     for fixed $q\in(0,1)$ or deterministic $q_n\in(0,1)$ with
     $r_n=o(\min(q_n,1-q_n))$
     ```

   This is a small textual repair to a mathematically necessary hypothesis, not a request for a new proof or a different threshold convention.

2. **MINOR — The frontier's “only under GR” contradicts the proved EP results.**

   **Evidence:** `FINAL/sections/s8_scope.tex:11` says “exact-model concentration only under GR.” But `FINAL/sections/s3_posterior.tex:48-49` gives Theorem F under EP and TAIL, removes TAIL for bounded candidate dimension or under TL with the amended cutoff, and states Lemma Z under EP as well as GR. These agree with `C-MIS/STATEMENT.md:123-141`, `:101-105`, and `C-MIS/lemmas/L4_theoremF.md:148-162`. The detailed results and the small-residual open window are sound; the word “only” in the summary is not.

   **Exact replacement text:** Replace the entire item at `s8_scope.tex:11` by

   ```tex
   \item \textbf{Misspecification}: exact-model concentration is proved
   under GR (fixed $\tau^2$, fixed projected sparsity, T03♯ hypotheses
   on the projected truth), and for fixed candidate designs under EP
   with the hypotheses of Theorem~\ref{thm:F}, including its size-tail
   condition or the stated bounded-dimension/TL alternatives; Lemma Z
   also covers the stated bounded-dimension null-projection cases.
   EP with growing $p_{\mathcal C}$ and small residual without a proved
   size tail, approximate projection, non-Gaussian/heteroscedastic
   random omitted parts outside GR, random-design EP and
   $n$-dependent $\tau_n^2$ are open; no density-contraction analog
   of Song--Liang Thm~4.
   ```

3. **MINOR — The title-page byline runs off the right edge of the delivered PDF.**

   **Evidence:** `FINAL/consistency.tex:7` places the entire author/credit sentence on one unbroken author line. `FINAL/consistency.log:1973` reports an overfull box of 181.50388 pt at the title construction. I rendered page 1 in memory and visually confirmed that the line is cut off at the physical right edge after the beginning of “from the Wave...”. This is a byline defect, not a clipped theorem or mathematical premise. No rendered image file was written.

   **Exact replacement text:** Replace the author declaration with

   ```tex
   \author{For Felipe Bedoya and co-authors\\[2pt]
   \small Compiled by the Wave~1C writer (Claude Opus 5.5)\\
   \small from the Wave~1 / Wave~1C record}
   ```

   Rebuild and check the first page; no source or theorem change is needed.

## Independent check of the three new mathematical items

### CAP and the transfer list

I compared §7.1 with SoP `02_method.tex:463-506` and used only read-only `git show` for the engineering branch, particularly `origin/w1c/ls0-merge:Scripts/SMC_BVS/core/cpp/v3_engine.h:370-418` and `cpp/v3_core.cpp:443-480`.

The branch evaluates/emits the centre, completes each feasible flip/swap scan, chooses the best neighbour by F and plain lexicographic tie-breaking, and tests strict improvement before testing the move count. At the move cap it returns the improving neighbour without making that move, but that neighbour was already scored. This is exactly why the scored set consists of the initial centre plus the neighbourhoods of centres C0 through C_min(a,m*), and why scoring truth can require one fewer move than certification. The cap does not enter neighbour selection. Induction proves the prefix property even with score ties. The uncapped path terminates because F strictly increases on a finite state space.

The potential runs share everything before LS0. Exact enumeration already scores every feasible model; a schedule-limit branch executes neither LS0; neither branch invalidates the inclusion. An actual guard-stopped run need not share the other cap's output event, but the lemma uses GUARD-W to identify records only on each method's own output event. This proves the HPM inclusion and the stated Markov bound. It does not assume monotonicity of the actual output event or of bounded stores.

I also ran an independent in-memory control-flow check: **16,800 comparisons passed**, over p=1,...,6, every K=1,...,p, random discrete scores with exact ties, empty and nonempty starts, and eight smaller caps per instance. Checks covered scan prefixes, move counts, scored-set inclusion, certified termination, and identical archives/returns after certification. This validates search semantics, not statistical consistency or floating-point scoring.

The transfer list is correct: PXN certification and its c+1-scan event transfer by identical termination; discovery and the scored-set HPM bounds transfer by inclusion; GEN's onset remains sufficient; C-MIS D/D-prime retain their GEN inputs. The list correctly refuses to transfer GEN C6's negative result, the old worst-case costs, stores, flags, or actual no-output events. The new worst-case search cost is bounded by `1+(ell_n+K+1)q(p)`. Delivery needs W_G/M_G, rather than only a claim of polynomiality. The branch has no stacking/c4 implementation; the chapter explicitly keeps that as a specification/premise issue rather than claiming a branch audit for R'>4.

### Corrected Proposition F

The proposition matches A1's corrected statement, including the previously essential resource amendment. The added K scans cost at most K q(p) requests, each charged at the existing worst-case score/cache/store cost `O(n^3+p(n+2))`; the extra path/scan archive fits `O(K(K+1))` words. With sufficiently large constants, W_G/M_G and the separate P0/P1/Pt preflight bounds support Corollary R's guard argument. MACH includes allocation success, dependencies, and absence of external interruptions; the result is correctly an abstract-machine theorem relative to the recorded exit audits.

A completed pilot has strict endpoints 0 and 1 and at most T1 intervals: every nonterminal increment is at least 1/T1, and the terminal one reaches 1. A previously successful construction has the same validity properties. Either is therefore a valid frozen final-run grid; restricted ESS is unnecessary for delivery. Under the numerical/resource premises, a stopped pilot is excluded before fallback selection. The total fallback removes schedule_limit and does not add retries or stages beyond the existing caps.

I checked the branch's `v3_calib.R:44-57,79-125,151-186`: a failed preliminary construction uses the completed pilot; a failed rebuild retains g, the last successful construction, rather than gn, the failed prefix. The tier ends, preserves its failure metadata and inherited state, validates the selected complete grid, and passes it through ordinary `v3_frozen` with the tier-1 budgets. This supports the implementation description; it is not a claim that physical R/C++ satisfies EX-A/MACH.

For selection, on output and deterministic LS0 discovery, truth is in the scored set (or enumeration has scored it). If pi(S0)>1/2, truth strictly beats every competitor in F. Therefore the error probability is at most `2 E[1-pi(S0)] + P(LS0 misses S0)`. PXN's data/search results or GEN's centre/descent results give the second term tending to zero; T03-sharp supplies the first. CAP transfers discovery to the enlarged cap. No step conditions on calibration success or requires its former law. LH's SIZE/instance-input qualifications, LH-iid's SIZE and p->infinity, and GEN's actual class hypotheses are retained through the stated references.

### Proposition F-GROW

I checked A2 and all five A3 amendments against §6.3, then read GROW L0–L6, including the full iid-AR(1) argument. On the sandwich event the emitted start mode is a maximiser in the feasible lattice. NA makes every extra deletion improve F; every swap removing an extra is dominated by that deletion, while TL excludes truth loss. Thus LS0 deletes exactly one extra per move, reaches truth after `|S_tilde_0 minus S0|` moves and certifies it after the next scan. MR1 more than covers the discovery requirement. The union bound for discovery failure follows directly from sandwich/NA/TL, rather than incorrectly reversing the operational bound for D_n.

For exact-Gram AR(1), the spectrum, conditional covariance bound, separation inequality, piecewise enlargement of Q and nearest-neighbour direction count supply the required hypotheses. For iid AR(1), sample standardisation does not justify exact sample Markov directions or deterministic NEG. L6 instead proves joint-law events: uniform Gram/TV regularity; a selection-uniform far-null statistic reduction; a spherical-tail/count argument covering the global start-size ladder; and approximation of lattice directions by a small family of population innovations. The conditioning used for the spherical tail fixes the true raw columns and noise before exposing the far-null innovation, so the standardised-scale signal causes no independence error. The posterior transfer uses every-sequence/common-envelope design events and a diagonal argument, not conditional convergence alone.

Lemma S's delivery inputs extend independently: fixed GROW columns are nonconstant, iid AR(1) columns are nonconstant almost surely, and conditional Gaussian noise makes a constant centred response null. For every scored feasible model, H and G+I are positive definite and `Q >= y'y/(n+1)>0`; neither p>>n nor growing relevance defeats that exclusion under EX-A. Together with the amended resources and valid fallback grid, the exit walk leaves only null no-output events. Bounded posterior error then gives its expectation limit, and the pointwise scored-set bound gives unconditional reported-HPM consistency. Fixed-p enumeration and the exclusion of random-row S5 are correctly carried through. No additional mathematical obstruction was found.

## Post-verdict check of the round-1 disposition

Only after recording the independent verdict above did I open `FINAL/reviews/C1_disposition.md`. I did not open either round-1 council review. The listed substantive repairs are present: S1's fixed-data convention and localisation for N1/E; S2's contrast coordinates, full-mean energy and explicit EP cutoffs; S3's favourable random-design GEN branch; S4/O1's Corollary-R allocation and distinction between the two LS0 caps; S5's BM(c), empty maxima and coded-routine hypotheses; O4b/O9's distinction between the prescribed tie rule and the weaker maximiser properties; O3/O5's audit/status qualifications; and O6/O12/O13's Song–Liang and PXN wording. The two MR1 labels, updated branch status, non-transfer of cost/flags/stores, and A2/A3 additions are also present. I found no unimplemented repair among those listed in that disposition. The findings in this review are independently identified residual issues.

SCORE: 7.9/10; GATES: G1 FAIL; G2 PASS; G3 PASS; G4 PASS; G5 PASS; G6 FAIL
