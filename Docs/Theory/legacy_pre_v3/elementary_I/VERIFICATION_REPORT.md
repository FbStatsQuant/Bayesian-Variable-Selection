# VERIFICATION REPORT — elementary_I thread (P1, T1, L1, L2, L3, L7, L5)

Compiled by the operator (Opus, high) on 2026-10-15 from `FINDINGS.md`, `STATUS.md`, `PROOF.md` (header and Section 9), `check_elementary_I.out` and the verdict lines and severity labels of the review reports. The operator does not judge the mathematics; everything below is quoted or counted from those files.

## Status

The lead's statement: **Phase 1 closed at the three-round cap; no reviewer found an error in the proof of any of the seven statements; all findings in remarks, flags, conventions, symbol clashes and editing artefacts, all accepted and applied; final text v4 differs from the reviewed v3 by wording only and is not re-reviewed.**

Statements covered: Proposition P1 (i)–(iii) and its last sentence, Theorem T1 (i)–(iii), Lemmas L1, L2, L3, L7, L5 of the draft of 14 October 2026. Lemma L4 is assumed (by the brief).

**Pending:** Opus C's round-3 report (fresh agent) had not arrived when this file was written. *To be appended by the lead.*

## Rounds run: 3

Counts are fatal / gap / exposition, **as each reviewer labelled its own findings**. The two families calibrate differently: Astra labels a false sentence in a remark "fatal" to that sentence, while Opus labels the same kind of item "gap". Verdict lines are quoted from the reports.

### Round 1 — v1 (`review/PROOF.md`)

| Reviewer | Verdict line (quoted) | F / G / E |
|---|---|---|
| Opus A (line by line) | "**Not verified**, strictly. The fatal and gap findings are:" … "No fatal finding." | 0 / 4 / 12 |
| Opus B (structure) | "**Not verified.** Two gap findings, both fixable and neither touching the core of any proof:" | 0 / 2 / 15 |
| Opus C (adversarial) | "**Not verified.** Fatal findings: none. Gap findings:" (F1, F3, F4) | 0 / 3 / 6 |
| Astra A (line by line) | "**Verdict: not verified.** Fatal findings: **1** (false necessity claim), **2** (false determinant-sign claim), **3** (false global sub-Gaussian scaling claim). Gap findings: **4** (missing cap restriction in proposed P1 wording), **5** (unresolved empty-model domain for L2)." | 3 / 2 / 5 |
| Astra B (structure) | "**Verdict: not verified. Fatal findings: F2–F6. Gap findings: F1 and F7.**" | 5 / 2 / 7 |
| Astra C (adversarial) | "**Verdict: not verified.**" (preceded by "Fatal findings: **F3, F4, F5**. Gap findings: **F1, F2, F6, F8**.") | 3 / 4 / 2 |

### Round 2 — v2 (`review/PROOF_v2.md`, diff `review/diff_v1_v2.txt`)

| Reviewer | Verdict line (quoted) | F / G / E |
|---|---|---|
| Opus A | "**Not verified**, strictly. The gaps are:" (G2′, G5) … "There is no fatal finding." | 0 / 2 / 8 |
| Opus B | "**Not verified.** One gap finding: **B2-1** …" … "No fatal findings." | 0 / 1 / 12 |
| Opus C | "**Not verified.** Fatal: none. Gap: **R2-3** …" | 0 / 1 / 3, plus 4 findings (R2-5 to R2-8) with no severity label |
| Astra A | "**Verdict: not verified.** No fatal findings in the new principal proofs. Gap findings: **1** (omitted BB restriction), **2** (omitted block-count restrictions), **3** (unjustified upper-tail application), and **4** (cap boundary error)." | 0 / 4 / 5 |
| Astra B | "**Verdict: not verified. Fatal findings: R2-1 and R2-2. Gap findings: R2-3 and R2-4.**" | 2 / 2 / 8 |
| Astra C | "**Verdict: not verified.**" (preceded by "There are no fatal findings in the revised theorem proofs. Gap findings: **R2-F1, R2-F2, R2-F3, R2-F4**.") | 0 / 4 / 3 |

### Round 3 — v3 (`review/PROOF_v3.md`, diff `review/diff_v2_v3.txt`; diff-only scope)

| Reviewer | Verdict line (quoted) | F / G / E |
|---|---|---|
| Opus A | "**Not verified**, strictly, because of one gap: **G6** (Section 0.1) … There is no fatal finding. Every changed proof step in v3 is verified, and the renamings introduced no error." | 0 / 1 / 3 |
| Opus B | "**Every step verified.** No fatal and no gap findings in round 3. Findings B3-1 to B3-6 are exposition only." | 0 / 0 / 6 |
| Opus C (fresh agent) | pending — *appended by the lead: Opus C (fresh agent), round 3: verdict "every step verified", 0 fatal / 0 gap / 4 exposition (R3-1 to R3-4), all accepted and applied in v4* | — |
| Astra A | "**Verdict: not verified.** Fatal findings: none. Gap findings: **1**, the general beta-binomial pole assertion." | 0 / 1 / 0 |
| Astra B | "**Verdict: not verified. Fatal finding: R3-1, confined to the auxiliary general-beta pole assertion. Gap findings: none.**" | 1 / 0 / 1 |
| Astra C | "**Verdict: not verified. Fatal findings: none. Gap findings: R3-F1, the false general pole assertion in Section 0.1. The seven main proofs are verified under their stated conventions and the permitted L4 assumption.**" | 0 / 1 / 1 |

## The lead's rulings (from FINDINGS.md)

| Round | Topics ruled | Accepted | Rejected | Open / disputed |
|---|---|---|---|---|
| 1 | 9 substantive rows, 17 exposition items, 2 new Opus C points | all (the symbol-clash item in part) | only the requests to rename the draft's own symbols ($\delta,\rho,T,B,m$; the $c$ clash is disambiguated instead) | none |
| 2 | 13 rows (R1–R13) | 13 | none | none |
| 3 | 6 rows (S1–S6) plus Opus C round 3 (4 exposition) | 6 | none | none |

## Hypotheses added and readings (PROOF.md Section 9, items 1–8, condensed)

1. **Global.** $n,p,L\ge1$, nonempty blocks; $w(k)>0$ for $0\le k\le p$; integer cap $0\le k_{\max}\le p$ (a larger cap is replaced by $p$; draft flagged: $\lfloor n/2\rfloor>p$ once $n\ge2p+2$, and the $\mathrm{BB}(1,p)$ formula has a pole at every integer $k\ge2p$); $W>0$; positive tables; $a_0,b_0>0$. Columns of $X_S$ in block order whenever $G_S$ is compared with $G_{S,0}$. Conventions for empty pieces ($t_\emptyset=0$, $D_\emptyset=1$, $\lambda_{\min}$ of a $0\times0$ matrix $=+\infty$, $g(+\infty)=0$, $\kappa(\emptyset)=0$). In Sections 6–8, $\pi$ means $q_1$; the empty convolution is the unit; $0^0=1$ for a singleton model space.
2. **P1(ii).** $K$ is drawn over $0,\dots,k_{\max}$; the cost is read as an arithmetic count (set-up plus one draw), valid for every $k_{\max}\ge0$ and any bound $B$ on block sizes; per-draw cost $O(k_{\max}+p)$ after preprocessing. The last sentence is read literally (Prop. 2.6(d): every beta-binomial prior with $p\ge2$, every $L\ge1$, $k_{\max}\ge0$; can fail at $p=1$) and in the strong sense (Prop. 2.6(b)–(c): needs $L\ge2$, $k_{\max}\ge1$; Prop. 2.6(e) for a binding cap).
3. **T1.** Nothing beyond the definitions; (ii) requires $x_\Sigma<1$ as stated.
4. **L1.** The first bound needs $\varphi^2(S)>0$ as stated; the uniform $O(|S|/n)$ reading needs a uniform eigenvalue bound (sufficient, not necessary). Added: $\Delta_{\det}\ge0$, with equality iff block-orthogonal (Theorem 4.4).
5. **L2.** As stated ($G_{S,0}\succ0$ over the nonempty blocks, $\kappa<1$); the $O(n\kappa)$ reading needs $\kappa\le\kappa_0<1$ and both residual fractions $\ge\eta>0$ (Corollary 5.3, constants stated).
6. **L3.** $p(S^\ast)>0$ as stated; the "hence" clause holds for deterministic, in-probability and almost-sure convergence.
7. **L7.** The consequence needs $\delta>0$; the identity holds for all real $\delta$; the greedy schedule is used only through "a feasible $\phi'$ gives $\phi_t\ge\phi'$".
8. **L5.** $\sigma_d,\lambda_0,c>0$ as stated; (8.1) is used at $\lambda=2\delta\le2\lambda_0$ for the step bound and as $\lambda\downarrow0$ at every $\phi$ for the variance bound.

## Unverified cited results

None. No external result is cited; Lemma L4 is assumed by the brief.

## Numerical checks

`check_elementary_I.py` → `check_elementary_I.out` (local, single seed `default_rng(1)`); last line: "36 checks, 36 PASS, 0 FAIL (33 at v3; three checks added in v4 for Proposition 2.6(d), its p = 1 exception, and the Remark 2.7 extension)". The reviewers' own check scripts are in `review/opus_A/`, `review/opus_B/` and `review/opus_C/`.

## Agents and calls

- Lead: Fable (high), 1 session. Prover sub-agents: 0. Researcher: 0.
- Operator: Opus (high), 1 agent (packet, Astra runs in all three rounds, this report and RETRO.md).
- Opus reviewers (xhigh): 3 agents in round 1, continued in round 2; in round 3, 2 continued (A, B) and 1 fresh (C), because the C agent stalled after delivering its round-2 report. 4 distinct Opus reviewer agents in all.
- Astra (`gpt-6-astra`, reasoning effort xhigh, read-only sandbox): 3 sessions, started in round 1 and resumed in rounds 2 and 3, for 9 calls in all; every call exited 0 and none was retried. Session ids, from the run headers of `astra_run.log`, `astra_run_round2.log` and `astra_run_round3.log`:
  - A: `<uuid>`
  - B: `<uuid>`
  - C: `<uuid>`

## Where the files are

All under `Proposed_project/proofs/elementary_I/`:
- Final proof: `PROOF.md` (v4; frozen copy `review/PROOF_v4.md`). Earlier versions: `review/PROOF.md` (v1), `review/PROOF_v2.md`, `review/PROOF_v3.md`; diffs `review/diff_v1_v2.txt`, `review/diff_v2_v3.txt`, `review/diff_v3_v4.txt`.
- Rulings `FINDINGS.md`; status `STATUS.md`; checks `check_elementary_I.py`, `check_elementary_I.out`.
- Packet: `review/PACKET_README.md`, `review/STATEMENTS_FROM_DRAFT.md`.
- Opus reports: `review/opus_X/REPORT_X_opus.md`, `REPORT_X2_opus.md`, `REPORT_X3_opus.md`.
- Astra reports: `review/astra_X/ASTRA_REVIEW_X.md`, `ASTRA_REVIEW_X_round2.md`, `ASTRA_REVIEW_X_round3.md`; prompts `prompt.txt`, `prompt_round2.txt`, `prompt_round3.txt`; logs `astra_run.log`, `astra_run_round2.log`, `astra_run_round3.log`; scripts `review/run_astra.sh`, `review/run_astra_round2.sh`, `review/run_astra_round3.sh`; master logs `review/run_astra_master.log`, `review/run_astra_master_round2.log`, `review/run_astra_master_round3.log`.

## Adoption

**Not adopted.** The results are provisional until the person adopts them.
