# VERIFICATION REPORT — Pb1 (exact selection error of the HPM under orthogonality)

Date: 2026-10-15. Compiled by the operator from `FINDINGS.md`, `STATUS.md`, `CITED_RESULTS.md`, `PROOF.md`, `check_Pb1.out`, the 18 review reports in `review/round1..3/` and the Astra run logs. The operator does not judge the mathematics; every statement below is copied from those files or from the run logs.

Final text: `PROOF.md` = `review/PROOF_v4.md` (byte-identical). v4 changes only wording relative to the reviewed v3 and was **not re-reviewed** because the round cap was reached (`FINDINGS.md`, Round 3). Diffs: `review/diff_v1_v2.txt`, `review/diff_v2_v3.txt`, `review/diff_v3_v4.txt`.

**Adoption: not adopted.** Under the research-code and theorem rules, the results are provisional until the person adopts them.

---

## 1. Status per item of the brief

| # | Item (STATUS.md plan) | Status | Where |
|---|---|---|---|
| 1 | Known variance: sharp condition on $\lambda_n=n\beta_n^2/\sigma_\star^2$ for $\Prob_0(\HPM=S_0)\to1$ and $\to0$ | **Proved** | Theorem 2.5 (nonasymptotic sandwich), Corollary 2.6 (sharp threshold, trichotomy), Proposition 2.4 (superset event) |
| 2 | Comparison with the minimax threshold for exact support recovery | **Proved** | Theorem 3.1 (every selector; the two oracles), Corollary 3.2 (minimax threshold for fixed $s_0$). The literature statements in `CITED_RESULTS.md` E1–E4 are context only. The fixed-$s$ all-selector lower bound of E1 is absent from the source (`FAILED_ATTEMPTS.md`; `CITED_RESULTS.md` E1.4–E1.5). |
| 3 | The draft's heuristic gap "$\log n+2\log2$" | **Proved in corrected form** | Theorem 3.3 and Section 3.3. The $\log n$ term is sharp. The constant $2\log2$ holds at the level of the leading-order centres for $s_0=1$ and for the $\tau_1$ penalty. The finite-$n$ constant is not determined. |
| 4 | Integrated variance (the paper's prior) | **Proved** under the extra bounded-signal condition | Corollary 5.6 (with Proposition 5.1, Theorem 5.2, Lemmas 5.3–5.4, Theorem 5.5). This is conditional on the provisional, not adopted T7_T8 results quoted in `CITED_RESULTS.md` I1–I8 (I8 = I8a, I8b), which Lemma 5.4 uses. |

---

## 2. Review rounds and verdicts

Three rounds ran, each with six blind reviewers: Opus 5.5 at xhigh on angles A/B/C, and GPT-6 Astra at xhigh on angles A/B/C. Angles: A line by line, B structure, C adversarial. Round 1 reviewed v1, round 2 reviewed v2, round 3 reviewed v3.

**All 18 verdicts: "not verified".**

| Round | Proof | Opus A | Opus B | Opus C | Astra A | Astra B | Astra C |
|---|---|---|---|---|---|---|---|
| 1 | v1 | not verified | not verified | not verified | not verified (findings 1–25) | not verified (1–23) | not verified (F1–F19) |
| 2 | v2 | not verified | not verified | not verified | not verified (R2-1–R2-14) | not verified (F1–F14) | not verified |
| 3 | v3 | not verified | not verified | not verified | not verified (A1–A8) | not verified (B1–B7) | not verified (C1–C9) |

What the reviewers state about the numbered results, quoted or paraphrased from their reports:

- **Round 1.** No reviewer found an error in any numbered theorem, proposition or corollary (`FINDINGS.md`). The three Opus reviewers state explicitly that the main results survive local repairs. The findings concentrate on the Summary, Remarks 2.7–2.8, (1.3), Lemma 1.3(d), the Theorem 3.3(c) example and the "$-2\log s_0$" verdict.
- **Round 2.** `FINDINGS.md` says: "no fatal finding; every reviewer states that all numbered results hold".
  - Opus A, B and C each say this explicitly in their reports.
  - **Operator's note on the source text:** Astra A's round-2 verdict reads "R2-3 leaves Lemma 5.4's large-superset argument and its dependent integrated-variance conclusions unverified; R2-4 independently leaves the claimed superset rate unsupported" (severity gap). These became issue 28, fixed in v3 by quoting I8a/I8b.
- **Round 3.** All three Opus reviewers state that every numbered result is verified step by step, including Lemma 5.4 against the quoted T7_T8 material. The Astra reports phrase it conditionally:
  - Astra A: "no fatal error in the numbered results, taking the supplied cited results as inputs".
  - Astra B: "the principal threshold arguments check out conditional on the supplied provisional citations".
  - Astra C: "no fatal error in the numbered threshold results, conditional on the quoted provisional T7 results".

  The remaining items are prose and scope items.

Prose and scope items still open at the round-3 verdicts (from `FINDINGS.md` Round 3, all ruled):

- **39:** the bracket $[2\log2-2\log s_0,2\log2]$ and the "finite-$n$ centre between $\tau_{s_0}$ and $\tau_1$" wording in the Summary, F2 and the Section 3.3 verdict.
- **40:** "$o(\sqrt{\log n})$ recentring" in F2.
- **41:** the T8 scope overclaim in F5, Section 5.5 and the Summary.
- **42:** "the oracles recover" under arbitrary signs, in Theorem 3.3(c).
- **43:** the sign reduction in Corollary 3.2's false-negative step.
- **44:** the "about 4.8" K3 figure (not in the packet; it is the signed-oracle value).
- **45–46:** overstatements about the random $\hat k$ and the noise maximum.
- **47:** the prior-factor approximation in Remark 2.7.
- **48:** the shrinkage-leakage wording in Section 5.5(b).
- **49:** Lemma 5.4's dependency note, R4 on $s_0=0$, a missing known-variance label, symbol clashes.
- **50:** F4 omits $p_n-s_0\to\infty$.
- **51:** the check-script comment on scale invariance.
- **52:** a tension inside the cited source E1.4.
- **53:** "additive over coordinates".

---

## 3. Findings by severity and ruling (counted from `FINDINGS.md`, issues 1–53)

Each issue is counted once, at the highest severity it was filed with. "fatal/gap" counts as fatal; "gap/exposition" and "exposition/gap" count as gap.

| Round | Issues | Fatal (as filed) | Gap | Exposition | Accepted | Rejected | Noted, no change |
|---|---|---|---|---|---|---|---|
| 1 | 1–23 (23) | 4 (1, 2, 12, 13) | 15 | 4 (10, 17, 21, 23) | 23 | 0 | 0 |
| 2 | 24–38 (15) | 0 | 9 (24–32) | 6 (33–38) | 14 | 0 (36 in part) | 1 (37) |
| 3 | 39–53 (15) | 0 | 7 (39–42, 44, 51, 52) | 8 (43, 45–50, 53) | 13 | 1 (53) | 1 (52) |
| **Total** | **53** | **4** | **31** | **18** | **50** | **1 (+36 in part)** | **2** |

How the 50 accepted issues were handled:
- **47 fixed in the proof text:**
  - v2 fixed 22: round 1 except issue 22.
  - v3 fixed 13: issues 24–36.
  - v4 fixed 12: issues 39–50.
- **1 fixed in `CITED_RESULTS.md`:** issue 38, control characters, by the researcher.
- **1 fixed in the review packets:** issue 22; `check_Pb1.py` and `check_Pb1.out` were added from round 2 on.
- **1 recorded in this report, script left as run:** issue 51.

Rejected:
- **53:** "additive over coordinates" is literally true of (1.5).
- **Part of 36:** Opus C's remark that the false-positive chain "holds only eventually" was rejected, because the chain is an inequality valid for all $p_n$ and $d'_n>0$. The rest of issue 36 was accepted and fixed in v3.

Noted, no change:
- **37:** the Theorem 3.3(c) example falls below the HPM centre only for $\log n>330$; the statement is asymptotic.
- **52:** the tension is in the cited source's own text and does not affect this proof.

All four fatal-as-filed issues are in round 1, and all were accepted and fixed in v2:
- 1: the superset floor needs $s_0<k_{\max}$.
- 2: Remark 2.7's "regardless of $\lambda$".
- 12: Summary hypotheses.
- 13: bounded $M_n^\beta$ in Section 5.5/F5.

**Disputed items: none.** `FINDINGS.md` records "Open: none. Disputed: none" after each round.

---

## 4. Unverified cited results

From `CITED_RESULTS.md`, section "UNVERIFIED (recalled, not opened in this thread)":
- Genovese, Jin, Wasserman, Yao (2012), *JMLR* 13, 2107–2143. Cited by E1 as [12]; not opened.
- Butucea, Ingster, Suslina (2015), ESAIM P&S 19, 115–134, Theorem 2.5 (consistency of exhaustive search). Known only through E1's Remark 4.1.
- The published journal versions (Ann. Statist. 46(5); IEEE TIT 66(4); IEEE TIT 55(12)) were not opened. Theorem numbers and pages are those of the arXiv PDFs.

The internal results I1–I7, I8a and I8b come from `proofs/T7_T8/PROOF.md`. They are quoted verbatim and machine-checked against their source lines, but they are **provisional and not adopted**. Item 4 (Corollary 5.6) is conditional on them through Lemma 5.4.

Also: E1 contains no fixed-$s$ all-selector lower bound, so Theorem 3.1 proves its own (`FAILED_ATTEMPTS.md`).

---

## 5. Assumptions and readings (`PROOF.md` Section 0.5)

- **R1.** Pb1 is a problem, not a theorem; the strongest provable theorem is delivered. Known variance comes first (Sections 2–4), then integrated variance (Section 5).
- **R2.** "Known variance" means $\sigma^2=\sigma_\star^2$, with the draft's normal slab kept and the inverse-gamma layer removed. A misspecified known value is covered by Remark 2.8.
- **R3.** The prior is $\BB(1,p)$ with cap $s_0\le k_{\max}\le p$; a cap above $p$ is read as $p$.
- **R4.** $s_0\ge1$, and $p\ge s_0+1$ wherever a noise coordinate is mentioned. For $s_0=0$, Proposition 2.4(a),(b) apply; part (c) needs $s_0\ge1$.
- **R5.** The threshold is defined through the trichotomy of Corollary 2.6: centre $\tau_n$, window width of order $\sqrt{\tau_n}$, centre determined only up to $o(\sqrt{\tau_n})$. No finite-$n$ centre is defined.
- **R6.** Ties among scores have probability zero, so the tie order plays no role.

---

## 6. Numerical checks (`check_Pb1.py` → `check_Pb1.out`)

- **Setup:** single seed `np.random.default_rng(1)`, local machine; python 3.12.7, numpy 1.26.4, scipy 1.12.0; runtime 228 s.
- **Result: all PASS.**
  - C1(i), C1(ii), C1(iii): formulas, with a real orthogonal $X$.
  - C2: brute-force HPM equals the top-$\hat k$ rule; $\{\HPM=S_0\}$ equals (a)&(b)&(c), draw by draw.
  - C3: sandwich; $B^c$ lower bound; $B^c$ upper bound; strict superset ⇒ $B^c$.
  - C4: integrated-variance upper bound.
  - C6: real $X$ vs the sequence representation.
  - C5 is report only (oracle and gap) and has no PASS/FAIL line.
- **History:** the first run had one FAIL (the C3 superset lower bound). That was a spec error: Proposition 2.4(b) bounds $\Prob(B^c)$, not $\Prob(\HPM\supsetneq S_0)$. The spec was corrected and the script rerun with the same seed; `STATUS.md` records this.
- **Coverage limit (issue 51):** check C4 covers $b_0/\sigma_\star^2=0.01$ only. The script's comment that "the HPM is scale invariant once $\lambda$ is fixed" is false for the integrated-variance HPM, which depends on $2b_0/\sigma_\star^2$. The script is left as run; its C4 results stand for the tested setting only.
- **Not in the script:** the K3 figures cited in Section 3.3 (about 4.8 for the signed oracle, about 3.6 for the absolute oracle) come from the reviewers' scratch outputs. They are labelled in v4 as not part of `check_Pb1.py`.

---

## 7. Agents and calls

| Role | Model (effort) | Agents | Calls / notes |
|---|---|---|---|
| Lead | Fable 5.1 (high) | 1 | 0 prover sub-agents |
| Operator | Opus 5.5 (high) | 1 | Check script, Astra rounds 1–2, this report. Rate-limited during the thread (`STATUS.md`). |
| Researcher | Opus 5.5 (high) | 1 | 3 tasks: CITED_RESULTS.md + LITERATURE.md; Internal I1–I7; I8a/I8b and the control-character repair |
| Reviewers | Opus 5.5 (xhigh) | 9 | 3 per round, fresh each round |
| Stand-in operator | Sonnet (high) | 1 | Astra round 3 |
| Reviewers | GPT-6 Astra (xhigh) | 6 sessions | 9 calls, listed below |

Astra calls (every log header shows `model: gpt-6-astra`, `reasoning effort: xhigh`):

| Round | Angle | Mode | Session id | Log |
|---|---|---|---|---|
| 1 | A | fresh | <uuid> | `review/astra_A/astra_run1.log` |
| 1 | B | fresh | <uuid> | `review/astra_B/astra_run1.log` |
| 1 | C | fresh | <uuid> | `review/astra_C/astra_run1.log` |
| 2 | A | resumed (same session) | <uuid> | see note |
| 2 | B | resumed (same session) | <uuid> | see note |
| 2 | C | resumed (same session) | <uuid> | see note |
| 3 | A | fresh (Sonnet stand-in) | <uuid> | `review/astra3_A/astra_run3.log` |
| 3 | B | fresh (Sonnet stand-in) | <uuid> | `review/astra3_B/astra_run3.log` |
| 3 | C | fresh (Sonnet stand-in) | <uuid> | `review/astra3_C/astra_run3.log` |

Notes on the Astra runs:
- **Round-2 logs are not in the review folders.** All three round-2 resumes exited with code 0, and their replies are in `review/round2/astra_X.md`. The operator was cut off before copying the logs to `review/astra_X/astra_run2.log`. They exist only at `<PC_TEMP_PATH>`, which is outside the project and not durable.
- **Shell reads failed in round 1.** The three sessions were started in parallel, and the sandbox's shell could not start ("helper_unknown_error: setup refresh had errors"). Astra read the files through its `node_repl` tool instead. Round 2 was therefore run one session at a time.

Fable calls: 1 (the lead).

---

## 8. Resume point

Nothing pending. Possible follow-ups, each needing a decision by the lead or the person:
- Adoption by the person.
- Copying the round-2 Astra logs into `review/astra_X/astra_run2.log`.
- Optionally, a C4 rerun at other values of $b_0/\sigma_\star^2$.
