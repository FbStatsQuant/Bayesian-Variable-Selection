# VERIFICATION REPORT — thread P2 (Proposition P2, several switches)

Lead: Fable 5.1 (high). Operator's draft completed and confirmed by the lead, 2026-10-15. Final proof: `PROOF.md` = `PROOF_v4.md`, sha256 `40ba143e17db6cb38342413a7ae88a4cc9aafbd4baa12db3ba82dbaf32c409a3`. Earlier frozen versions: v1 `c8f19477…`, v2 `74889719…`, v3 `b362f3de…`.

## Status

**P2: proved, in the sense of THREAD_RULES_wave3.md §8, with $K_1(c,K,J)$ explicit and the readings R1–R5 flagged. Not adopted by the author.**

Phase 1 (correctness review) outcome, stated precisely:
- Three rounds, six blind reviewers each (3 Opus 5.5 xhigh, 3 GPT-6 Astra xhigh). No reviewer in any round reported a fatal finding or a counterexample to Theorem 0.1, Theorem 2.7, Proposition 2.5, Lemma 4.1 or Theorem 4.2.
- Every load-bearing step of the proof of Theorem 0.1 (= P2) was verified by all six reviewers in round 1 or, where changed, in round 2; Opus B's round-1 verdict on the full proof was already "every step verified".
- Round 3 (changed parts of v3, including the new auxiliary Lemma 4.6): five verdicts "every step verified" (Opus A, B, C; Astra B, C); Astra A: "not verified as literally written, solely because of A1 [an exposition point on the domain of an auxiliary function in Lemma 4.6]. Lemma 4.6's conclusion and all substantive mathematical steps are verified."
- Every finding of every round was accepted by the lead and fixed; none was rejected, none is open, none is disputed. The round-3 findings (all exposition) were fixed in v4, which differs from v3 by wording only (`review/round3_to_v4_DIFF.md`, 55 diff lines) and was not re-reviewed because the three-round cap had been reached. Under the strict letter of proof.md ("every reviewer's verdict is verified"), the proof is therefore *verified for the proof of Theorem 0.1 and all its lemmas*, with one wording-only amendment to the unused Lemma 4.6 made after the final round; the person may call a fourth, wording-only round if they wish.

## Rounds run: 3

| Round | Version | Scope | Fatal | Gap | Exposition | Rulings (FINDINGS.md) |
|---|---|---|---|---|---|---|
| 1 | v1 (`c8f19477`) | full proof, six reviewers | 0 | 15 (Astra 13, Opus 2) | 43 (Astra 14, Opus 29) | every finding accepted and fixed in v2; symbol-overloading items accepted in part (some symbols kept, as flagged in the text); nothing open, nothing disputed |
| 2 | v2 (`74889719`) | changed parts, six reviewers | 0 | 6 (one shared item: a false side claim in Remark 1.3, reported by all six) | 17 Opus + 1 packet item (Astra 0) | all accepted and fixed in v3; the restricted L4(ii) analogue (r2-OC-F2) adopted as the new Lemma 4.6; nothing open, nothing disputed |
| 3 | v3 (`b362f3de`) | changed parts, including Lemma 4.6 in full | 0 | 0 | 19 (Astra 1, Opus 18) | all accepted and fixed in v4 (wording only); nothing open, nothing disputed |

Counts are per reviewer, summed; the same issue reported by several reviewers is counted once per reviewer. RETRO.md §3 maps the duplicates. The gaps of rounds 1 and 2 were: the $n=0$ and $n=1$ edge cases of the per-piece count (Proposition 2.5), three non-load-bearing remarks, and one false side claim in Remark 1.3 (introduced by the lead's round-1 fix). None touched the proof of Theorem 0.1.

## Disputed items

None.

## Unverified cited results

None. CITED_RESULTS.md §D: every result cited or referenced was found in its stated source file and quoted verbatim. The only external result the proof *uses* is L4(iii) (foundations/PROOF.md, Theorem 2.4(a),(b)): well-definedness, strict increase and termination of the greedy schedule. L5's one-step computation is re-proved inline (Lemma 3.1). The draft's status lines for L4, L5 and T4 ("Proved; Sol-audited") are the draft's claims and were not re-checked here.

## Assumptions (readings adopted, PROOF.md §0.3)

- **R1 (nonempty parts):** every $\mathcal A_k$ is nonempty; an empty part can be dropped, which lowers $K$.
- **R2 (pieces):** (M1) is read as a fixed decomposition of $[0,1]$ into $J_k\le J$ closed pieces per $k$, each declared nondecreasing or nonincreasing consistently with its monotonicity (a constant piece may be declared either way); $\mathcal U$ is the set of pairs $(k,\text{left endpoint})$ of the pieces declared nondecreasing. Interior breakpoints are labelled pairs $(k,i)$, $\sum_k(J_k-1)\le K(J-1)$ of them. The bound holds for every admissible decomposition, so this reading is at least as strong as any the draft may intend.
- **R3 (M2):** L5's hypothesis (8.1) for the bridge on each part, with $\sigma_d=\sigma_w$: for all $k$, $\phi\in[0,1]$, $\lambda\in[0,2\lambda_0]$.
- **R4 ($T$):** the stage count of the greedy population-ESS schedule with threshold $c$ on the full bridge.
- **R5 ($K=1$):** every pair of $\mathcal U$ contributes $0$ and the mixture $\chi^2$ vanishes; the proof covers this case.

## Agent and call counts per model and effort

| Role | Model, effort | Count |
|---|---|---|
| Lead | Fable 5.1 (high) | 1 (the session); 0 further Fable calls; 0 prover sub-agents |
| Researcher | Opus 5.5, high | 1 agent, 3 tasks (CITED_RESULTS.md and its two refreshes; counterexample and constants check) |
| Operator | Opus 5.5, high | 1 agent, 6 tasks (check_P2.py and its extension; Astra rounds 1, 2, 3; RETRO and VERIFICATION_REPORT drafts) |
| Opus reviewers | Opus 5.5, xhigh | 3 per round × 3 rounds = 9 calls |
| Astra reviewers | gpt-6-astra, xhigh (codex exec, read-only sandbox, fresh session each round) | 3 per round × 3 rounds = 9 calls; session ids in `review/round*/astra*/SESSION_ID.txt` |

Harness notes: the Opus reviewers could not write their reports (harness block); the lead saved all nine Opus reports verbatim from the replies. The codex shell helper failed in all nine Astra runs; the models read the packets through node_repl, and the operator verified by checksum that no packet file changed.

## Numerical check (check_P2.py → check_P2.out, local, seed 20261015, numpy only)

First run (against the pre-v1 proof): 3221 checks, 3220 PASS, 1 FAIL (θ printed as 0.0099497 where it rounds to 0.0099498; fixed in v1). Checked: identity (1.1) and inequality (1.2) at every greedy step; tightness (Lemma 4.1); $T\le1+|W|+|M|$ and $[T-1]\subseteq W\cup M$; Theorem 2.7 and Proposition 2.5 piece by piece; Lemma 3.1 and Proposition 3.2 with a grid estimate of $\sigma_w$; Theorem 0.1; the constants of §0.4 and Lemma 2.6; Remark 4.3's numbers ($\chi^2(u(1)\|u(\tfrac12))=0.4998638157$ at $D=20$; maximum at $\phi=\tfrac12$). Summary (bound_W, bound_T at $\lambda_0=0.5$):

| example | c | T | \|W\| | \|M\| | \|W∩M\| | J | sum_U | bound_M | bound_W | bound_T | all PASS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 D=10 | 1/9 | 12 | 8 | 4 | 1 | 2 | 2.324 | 253.73 | 62 | 316.73 | yes |
| E1 D=20 | 1/9 | 14 | 7 | 6 | 0 | 2 | 3.322 | 254.73 | 124 | 379.73 | yes |
| E1 D=40 | 1/9 | 15 | 8 | 7 | 1 | 2 | 4.322 | 255.73 | 247 | 503.73 | yes |
| E2 Δ=100 | 1/9 | 13 | 0 | 13 | 0 | 1 | 5.644 | 130.35 | 2 | 133.35 | yes |
| E2 Δ=1600 | 1/9 | 17 | 0 | 17 | 0 | 1 | 9.644 | 134.35 | 2 | 137.35 | yes |
| E3 | 1/9 | 19 | 0 | 19 | 0 | 2 | 11.23 | 383.56 | 2 | 574.22 | yes |
| E4 | 1/9 | 19 | 1 | 17 | 0 | 2 | 11.45 | 383.78 | 7 | 579.45 | yes |
| E5 (20 random × 2 c) | 1/9, 1 | 1–12 | | | | 1–3 | | | | | 40/40 yes |

(the full table, including $c=1$, is at the end of check_P2.out). The bound is loose by one to two orders of magnitude, mostly through $K_1$. Independent numerical checks by the reviewers (scripts in `review/round*/opus*/`) covered extremal sequences for Proposition 2.5 (slack $\ge1.04$ down to $u=10^{-300}$), first-hit mixture sequences and random dense sequences for Theorem 2.7 (no violation), and tens of thousands of admissible triples for Lemma 4.6 (0 violations; thousands of violations without the restriction).

Final run (against v4, with Lemma 4.6, Remark 1.3's sufficient condition and Remark 4.3's every-scale claim added): 3287 checks, 3287 PASS, 0 FAIL, 0 MARGINAL (the earlier theta line now passes). The 66 new checks: the derivative formula of Lemma 4.6 (relative error 2.7e-10 against central differences); Lemma 4.6 on E1 (D = 10, 20, 40; I = [0,1/2] and [1/2,1]; 500 triples each, 0 violations; the computed common monotone intervals are exactly these two; 173-187 violations per 500 unrestricted triples as control) and on 30 random K=3 bridges (40,000 restricted triples, 0 violations; 549/15,000 unrestricted violations as control); Remark 1.3's sufficient condition (d constant on each part: the L4(i) form with G = F holds to 1.4e-14; it fails on E1 as a control); Remark 4.3's every-scale claim (D = 2, 20; six values of h: the symmetric divergence is 0 to 2.7e-15 and the half-step divergence is positive, smallest 8.9e-13). The E1-E5 output is byte-identical to the first run.

## Per-item status (THREAD_RULES_wave3.md §8)

- **P2 (Proposition, several switches): proved**, with $K_1(c,K,J)=1+K(J-1)+KJ\big[2+(1-\theta)/\sqrt{c''\theta}\big]$, $c''=(\sqrt{1+c}-1)/K$, $\theta=e^{-1}\min\{1,c''\}$, and the sharper intermediate statement $T\le1+|W|+|M|$. Readings R1–R5 flagged; flags for the draft in PROOF.md §5 (the note's "open step" closes by a different route; its suggested monotonicity property is false globally and true on common monotone intervals; (M1) should fix a decomposition; parts nonempty; the note's "returns to 1" is only approximate).
- Not adopted by the author; provisional until the walkthrough.
