# Final council round 3 — Claude seat (opus)

Reviewer: Claude Opus 5.5 (fresh seat). Object: `Theory_work/Wave1C/FINAL/consistency.tex` + `sections/s1–s9` at
d315c1e. The working tree matches HEAD d286a63; that commit changed only the brief. Sources I read: COUNCIL_BRIEF.md and
COUNCIL_BRIEF_R3.md; HQ_AUDIT A1, A2 and A3; C-DLV `lemmas/L1_resources.md`, `L2_degenerate.md` §S.1–S.2 and
`L4_delivery.md`; C-GROW `METHOD_REQUIREMENTS.md`, `STATEMENT.md:84-156` and `lemmas/L4_assembly.md`; W1-GEN
`STATEMENT.md:150-151` and L7; SoP `02_method.tex:486-570`. On the branch I read, with `git show`, at both 8a27652 and the
current head 493579a: `v3_core.cpp:400-500`, `v3_engine.h:360-420` (also compared with PROD and CORE), `v3_calib.R:20-195`,
`v3_fit.R:1-70` and `C-ENG/REPORT.md`. I also extracted the Song–Liang PDF text to spot-check the map. I did not open
any C1/C2 council review before writing the verdict. I read C1_disposition and C2_disposition afterwards (see the end of
this file).

## The three items checked in full

### 1. Lemma CAP (§7.1): **correct**
- **(L3) against the code.** I read `local_search` on the branch at `v3_engine.h:379-419`. It is identical to
  `PROD/cpp/v3_engine.h:378-418` except for the `phase` argument. The CORE cap test is at :415. The loop is:
  1. score the emitted centre;
  2. scan every feasible flip (additions skipped at |C| = K), then every swap;
  3. push C to `scanned`;
  4. if the best neighbour gives no strict F improvement, return C as certified;
  5. otherwise, if `moves >= ell`, return that neighbour with `local_limit`;
  6. otherwise move.

  The cap enters only in step 5. **(a)** follows by induction:
  - The run scans C₀, …, C_{min(a,m\*)}, which is min(a,m\*)+1 scans.
  - At k = m\*, termination is certified *before* the cap is tested. So "certified iff m\* ≤ a" also holds at m\* = a.
  - The scored set is {C₀} ∪ ⋃_{k≤min(a,m\*)} N(C_k), and it is monotone in a.
  - The identity claim for a certified small-cap run holds because nothing after LS0 reads the cap.
- **(L1)/(L2) against `v3_core.cpp:443-481` at 8a27652.** The order is: islands; final local search; guard; then, only
  if the status is `completed`, `start_mode(st, 1e6, tie_dp)`, the cap ℓ + |m.S|, the `INT_MAX` check, LS0 with
  `emit_centre = true` on the same ledger and cache, and the guard at the `ls0` checkpoint. The cap is computed after the
  mode is known, and LS0 is the last scoring step.
- **The scored set does not depend on the cap otherwise.** The certificate card (SoP `02_method.tex:538-569`) is
  evaluated on the returned Ŝ and never changes the status. So **(b)** holds: the potential status is fixed before LS0,
  and $\bar{\mathcal S}^+(a)=\bar{\mathcal S}\cup\mathcal S_{\rm LS0}(a)$ on completed SMC runs. The exact-branch and
  `schedule_limit` bookkeeping is right.
- **(c).** On 𝒪(a) we have 𝒪(a) ⊆ $\bar{\mathcal O}$ by GUARD-W, the delivered set is the potential set, and it contains
  $\bar{\mathcal S}^+(\ell_n)$. π(S₀) > ½ forces S₀ ∈ Ω and F(S₀) > F(S) for every S ≠ S₀, so S₀ is the strict
  (F, −|S|, lex) maximum. Markov gives the factor 2. The final step D_n(ℓ_n) ≤ P(LS0(ℓ_n) misses) is [OP].
- **Transfer list.** I checked every bullet:
  - PXN (T), second clause, and (K) on the event: on the event the small-cap run is certified, so (a) makes the two runs
    identical.
  - GEN: τ(C)−1 / τ(C) is the right threshold arithmetic for "scored" / "certified".
  - D′ transfers pathwise because 𝒦_n(a_n) ⊇ 𝒦_n(ℓ_n).
  - The "does not transfer" list is right. (C6) uses distance 2(ℓ_n+1) (W1-GEN STATEMENT:150-151, L7:78-81), and with
    a_n the reach is 2(ℓ_n+|S̃₀|+1), so (C6) is correctly withdrawn. The stores are not monotone because of eviction by
    top_c. U_n depends on the cap through the guard after LS0.

  I found no counterexample, including at the edge cases m\* = a, m\* = 0, a centre with no feasible neighbour, a centre
  of size K, and the exact branch.

### 2. Proposition F (A1's corrected form, §6.2): **correct; faithful to A1:60-75**
- **Delivery.** Theorem D's exit walk (L4:24-40) leaves only 𝒮ℒ_n plus null sets. I checked the total fallback on the
  branch at 8a27652, `v3_calib.R:111-125, 160-170`:
  - The tier stops at the first failed construction: `break` after a failed rebuild, and the loop is skipped after a
    failed preliminary.
  - `g` is the last *successful* construction; the failed `gn` is never assigned to it. Otherwise the pilot schedule is
    used. Partial pilots exit earlier through `fail`.
  - The fallback is validated by `v3_check_grid` and frozen by the ordinary `v3_frozen` with the tier-1 N and L and the
    inherited state.
  - It fires only when the shipped code would return `schedule_limit`.

  A1's pilot argument (k ≤ T₁; endpoints 0 and 1; strictly increasing) keeps the fallback inside Lemma R's
  bridge-stage cap. So 𝒮ℒ_n = ∅ and P(no output) = 0.
- **Amended envelopes.** I re-derived A1's increments:
  - LS0 makes ≤ a_n+1 ≤ ℓ_n+K+1 scans, which is K more than C-DLV assumed. Each scan makes ≤ q(p) requests. So there
    are ≤ Kq(p) extra requests, each costing ≤ κ+ω ≤ C[n³+p(n+2)] (L1 R.2).
  - The LS0 archive grows by ≤ K centres of ≤ K ints, plus O(1) per scan. That fits inside CK(K+1).
  - Σ̄ already over-counts each scan by 1, so Σ̄ + Kq(p) is valid.
  - The guard argument (elapsed + one operation ≤ 2(τW_G+τ₀)) carries over. Start mode plus LS0 is timed as one
    operation, and both are inside W_G.
- **Consistency.** The pathwise inclusion 𝒪∩{Ŝ≠S₀} ⊆ {π(S₀)≤½} ∪ 𝒦_n(a_n)ᶜ, combined with Lemma CAP (𝒦_n(a_n) ⊇
  𝒦_n(ℓ_n)) and P(𝒪) = 1, gives P(Ŝ≠S₀) ≤ 2E[1−π(S₀)] + P(𝒦_n(ℓ_n)ᶜ) → 0 on LH, LH-iid and GEN, with CAL bypassed. The
  e4 centre satisfies e4′ on {π₀(R)>½}, which is what PXN and GEN use.

### 3. Proposition F-GROW (§6.3): **correct**
- **Delivery.** The delivery part does not depend on the class; the only class input is Lemma S.1:
  - GROW's fixed designs: nonconstant columns hold by G.
  - iid AR(1): each raw column is iid N(0,1), so it is nonconstant a.s.
  - Given X, Cε is nondegenerate on 1⊥, so a constant response is a null event.
  - Q_S ≥ y′y/(n+1) needs no rank condition, so p ≫ n is harmless.
- **Consistency.** On Sand_n ∩ NA ∩ TL:
  - e4/TDP emits some maximiser of γ₀, which lies in 𝓛 ⊆ Ω because |Q| ≤ K by (G1).
  - (C1) gives exactly |S̃₀∖S₀| deletions, and the cap a_n ≥ |S̃₀| ≥ |S̃₀∖S₀| > |S̃₀∖S₀|−1. So 𝒦_n(a_n) holds.
  - The chapter correctly refuses to obtain this from D_n → 0.
  - The posterior input is T03♯ under (H0), or L6.2 plus the diagonal argument for iid rows.

  (C4)(b) checks out: |𝒫_n| ≤ (1−δ₀)ln n < log₂ n ≤ ℓ_n. All five A3 amendments are present (s6:47-51).

## Gates

| gate | verdict | reason |
|---|---|---|
| G1 | **PASS** | I spot-checked these statements against their sources: PXN, GEN (C1)–(C6), GROW (C1)–(C5) with (G1)–(G4), Props. F and F-GROW, SL0, SL1 and SL2, and MIS (i)–(iii). Hypotheses and scope match. One added parenthetical in Prop. F has a quantifier wording defect (finding 3). |
| G2 | **PASS** | Statuses are verbatim and nothing is upgraded. A1, A2 and A3 are labelled not councilled. The CAP review trail is stale (finding 2) but understates rather than upgrades. |
| G3 | **PASS** | Lemma CAP (a)–(c), the Prop. F assembly and the F-GROW assembly are all correct (see above). |
| G4 | **PASS** | Spot-checked against the PDF: Thm 3 (p. 956), its "all conditions of theorem 2" premise and the sensitivity-only claim; Thm S being supplementary; Cond 4 vs Thm 4; Cond 5; and §6 time. All are accurate. |
| G5 | **PASS** | §8 lists every required frontier item honestly. Finding 1 concerns implementation currency past the pinned commit, not the scope of the theorems. |
| G6 | **PASS** | The premise lists, the two MR1s, the caps and e4 → e4′ agree throughout. The stale date and review-trail lines are minor (finding 2). |

## Findings

**1. MAJOR — the branch has moved: the chapter's preflight claims are stale, and the implementation now has an
extra no-output exit that Prop. F's allocation does not provably cover.**
- *Evidence.* `origin/w1c/ls0-merge` is now at 493579a. Commit ef33f91 (2026-11-09 00:00:08) was made *before* the v3
  chapter commit (00:10:38), and C2_disposition:"Other necessary changes" records that the writer knew the ref had
  advanced. At that commit `v3_preflight` gained `ls0_worst_case`, which adds two things:
  - a memory component `ls0_archive`;
  - a time estimate `ls0_seconds = 2·(ℓ_n+K+1)·q(p)·ŝ_K`, where ŝ_K is the *measured* seconds per score of a size-K
    model. The fit is refused if this exceeds `hours·3600` (`git show origin/w1c/ls0-merge:Scripts/SMC_BVS/core/v3_fit.R`,
    `v3_preflight`; REPORT.md:63-81 at head).

  The chapter still says "the branch's preflight formula does not include the MR1 (C-GROW) LS0 term … preflight does
  not enforce it" at s6_delivery.tex:55, s7_impl.tex:10, s7_impl.tex:78 and s8_scope.tex:15. That is true at 8a27652 and
  false at the head that will be merged.
- *Why it matters.* Prop. F is about the specified method with C-DLV's preflight bounds P₀, P₁ and P̄_t, so the theorem
  itself is unaffected. But the merged code has a new preflight exit outside the P1 inventory. Under MACH,
  ŝ_K ≤ (τU_K+τ₀)/200. The τ₀ part, s·q(p)·τ₀/100, is not shown to be ≤ 2(τW_G+τ₀) for the implementation-only constant
  C. A Prop. F-compliant allocation could therefore be refused at preflight on the head code.
- *Fix (replacement text).*
  - In s6 Remark (5), replace "the branch's preflight formula does not include the MR1 (C-GROW) LS0 term, so the amended
    allocation must be declared by the user" with: "at the cited head \texttt{8a27652} the preflight formula does not
    include the MR1 (C-GROW) LS0 term; later branch commits (\texttt{ef33f91}--\texttt{493579a}, not reviewed by this
    chapter) add an LS0 worst-case preflight charge (archive bytes and a measured-time estimate $2(\ell_n+K+1)q(p)\hat
    s_K$ checked against \texttt{allocation\$hours}). For that code to inherit Proposition~\ref{prop:F}, the allocation
    must in addition satisfy $\mathrm{time}_n\ge\bar P_{\rm LS0}:=(\ell_n+K+1)q(p)(\tau U_K+\tau_0)/100$ ($U_K$ the
    operation count of the 200 timed size-$K$ scores) and $\mathrm{mem}_n\ge P_e+\text{the }\texttt{ls0\_archive}\text{
    bytes}$ ($e=0,1$)."
  - In s7:10, s7:78 and s8:15, prefix each preflight sentence with "At \texttt{8a27652}," and add a pointer to Remark (5).

**2. MINOR — the review trail and date are frozen at round 1 / v2.**
- Lemma CAP's reviewflag (s7_impl.tex:64), the agentnote (consistency.tex:21) and the provenance row
  (s9_prov.tex:28) mention only round 1, and the provenance row stops at "e95adc2 (v2)". Round 2 (10b2090: Sol 7.9 / Opus
  8.8, not passed; per the R3 brief both seats checked CAP, F and F-GROW) and v3 (d315c1e) are missing.
- `\date` (consistency.tex:9) still reads "council round 1; disposition in e95adc2", while the header reads "draft v3
  (council round 3)".
- *Fix.*
  - Reviewflag: replace "round~1 did not pass overall" with "rounds~1 and~2 did not pass overall (round 2: Sol 7.9, Opus
    8.8, commit \texttt{10b2090}; disposition \path{W1C/FINAL/reviews/C2_disposition.md})".
  - Provenance commit cell: "\texttt{5bcde3b} (v1), \texttt{e95adc2} (v2), \texttt{d315c1e} (v3)".
  - `\date`: "…council rounds 1–2; dispositions in \texttt{e95adc2}, \texttt{d315c1e})".
  - Agentnote: "both council-round-1 seats … round~1 did not pass" → "the round-1 and round-2 seats checked it; neither
    round passed".

**3. MINOR — the round-2 insertion in Prop. F has inconsistent quantifiers.** s6_delivery.tex:39 says "model G is
assumed on every realisation: $X^r$ has nonconstant columns almost surely". "Every realisation" and "almost surely"
contradict each other. *Fix:* "(for random-design members of the GEN class, model G is read as: $X^r$ has nonconstant
columns almost surely and $\varepsilon\sim N_n(0,\sigma^2I_n)$ is independent of $X^r$; Lemma S.1 verifies the first for
fixed standardised designs and nonsingular Gaussian rows)".

**4. NIT — definition of 𝒮⁺.** s1_setting.tex:22 says "every model ever scored". The certificate card evaluates models
*after* Ŝ is fixed (SoP 02_method.tex:551). *Fix:* "every model scored by the fit up to and including LS0 (post-hoc
certificate evaluations excluded)".

**5. NIT — the bound in (C6) is loose.** In s7_impl.tex:80, "the reachable distance is $2(a_n+1)\ge2|\tilde S_0|$" should
read "$2(a_n+1)=2(\ell_n+|\tilde S_0|+1)$".

**6. NIT — overfull boxes.** Three pre-existing overfull boxes remain: s3_posterior.tex:41 (24.7 pt), s5_hpm.tex:28
(13 pt) and s9_prov.tex:30. Break the (H-MIS) display and the PXN (R) display.

## Check of the earlier dispositions (read after the verdict)
- **C1.** All 19 rows (S1–S5, O1–O14) and the A2/A3/C-ENG inputs are present in the text at the stated anchors. I
  checked each: N1 data convention s4:59; Thm F cutoffs; GEN (C4) favourable branch; the Allocation paragraph; cap-ℓ_n
  scoping of Theorem D and D′; the transfer list; caps ≥ max(ℓ_n,|S̃₀|); "some maximiser"; MR1 labels; e4 tie rule;
  SL0(vi); the ξ_q quotation; PXN (C). **Fixed.**
- **C2.** All Sol 1–3 and Opus 1–10 changes are present. One defect remains: Opus #1's inserted text has the quantifier
  defect in finding 3. Opus #9 and #10 were correct at v2 but are now stale (finding 2). The optional v3_calib.R
  citation was not applied; that is acceptable.

SCORE: 8.6/10; GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS
