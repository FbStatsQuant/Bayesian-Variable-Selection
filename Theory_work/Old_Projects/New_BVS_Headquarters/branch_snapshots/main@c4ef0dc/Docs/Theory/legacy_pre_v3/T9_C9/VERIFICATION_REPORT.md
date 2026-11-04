# VERIFICATION_REPORT.md: thread T9 / C9 (prediction and variance contraction; random-design Hellinger contraction; sharp dimension bound)

Lead and prover: Fable 5.1 (high). Dates: 2026-10-14 to 2026-10-15. Deliverable: `proofs/T9_C9/PROOF.md` (v3, = `review/round2/PROOF_v3.md`).

## Status

**T9 (i), (ii): verified** by all six round-1 reviewers (three Opus 5.5 xhigh, three GPT-6 Astra xhigh), step by step; unchanged in substance since. Round 2 (three Astra) re-confirmed.

**Corollary 5.1 (sharper form of T9(ii)), Theorem 5 (master theorem): verified** in round 1 by all six.

**Corollary T9a(iii), the implication: verified as amended** (the constant depends also on the dimension constant $C_1'$; part (ii) under $\ell_n=o(n)$) by all six in round 1 and three Astra in round 2. The amendment of the wording needs the person's sign-off. Its necessity is not proved.

**Corollary C9: verified as amended** by the three round-2 Astra reviewers (the three round-2 Opus reviewers did not report; see below). Amendments: (R1) centred rows; (R2) sub-Gaussian constant fixed in $n$; (R4) read for T6's $m_n$ with any admissible $\omega_n$. Both design conventions covered. The frozen statement is false if "sub-Gaussian" is read without a uniform constant (Remark 7.3, counterexample confirmed by computation); whether (R1) can be dropped under (R2) is open. The amendments need the person's sign-off.

**Theorem 13 and Corollary 14 (sharp dimension bound for $p\le n^A$ under (SE), standardised columns and $k_{\max}\ge\min\{p,m_n+s_0\}$; hence T9a(iii) at the rate $(s_0+1)\ell_n/n$ in that regime): verified** by the three round-2 Astra reviewers (no fatal or gap finding on the theorem; two side remarks corrected in v3). Not reviewed by Opus. New result, not in the draft.

**Remark 6.2 (the $n^{-1/2}$ term cannot be replaced by a constant; model-free): verified** by Astra C in round 2 (no objection from A, B).

**Overall: not fully verified in the protocol's sense.** The protocol requires six reviewers per round with every verdict "every step verified". Round 1 ended with six "not verified" verdicts whose findings were all accepted and fixed; round 2 ended with three "not verified" Astra verdicts whose findings concern side remarks only and are fixed in v3; the three Opus round-2 reviews were lost to a session reset and v3 has not been re-reviewed (the thread was wrapped up on the person's instruction, with one round of the three-round cap unused). The theorems themselves have no open finding.

## Rounds

| Round | Version | Reviewers | Verdicts | Fatal | Gap | Exposition |
|---|---|---|---|---|---|---|
| 1 | v1 | Opus A, B, C (xhigh); Astra A, B, C (xhigh) | 6 x not verified | 1 (C9 as frozen; Astra B, C) | 9 distinct | 16 distinct |
| 2 | v2 | Astra A, B, C (xhigh); Opus A, B, C launched, interrupted | 3 x not verified | 0 | 5 distinct (all side claims) | 3 distinct |

Rulings: `review/FINDINGS.md` (round 1, 26 items) and `review/FINDINGS_round2.md` (8 items). Every finding accepted; none rejected; none open; no disputes; no rebuttals needed.

## Findings by severity and ruling

- Fatal: 1 (C9 false as frozen without centring, under the per-$n$ reading of sub-Gaussian). Accepted; statement amended; counterexample independently confirmed by computation (`review/round1/check_counterexample_C9.out`).
- Gaps: 14 distinct across the two rounds. All accepted and fixed: general $\omega_n$ cutoff; uniform sub-Gaussian constant; zero-column convention; $C_1'$-dependence recorded as an amendment (and "unavoidable" withdrawn); Section 6 remarks corrected (one replaced by the proof in Section 9, one proved model-free, one deleted); Fact G verified against the source; measurability justification; finite-$n$ scope of $m_n$; super-polynomial extrapolation withdrawn; (H4) corrected.
- Exposition: 19 distinct. All accepted and fixed (notation clashes, wording, quantifiers made explicit).

## Disputed items

None.

## Statement amendments for the draft (need the person's decision)

1. C9: add "centred rows" (or define $\Sigma_x$ as the second-moment matrix and re-derive), and "sub-Gaussian with a constant not depending on $n$"; state which $m_n$ the sparse-eigenvalue condition refers to (any admissible $\omega_n$ works). Without a uniform constant the statement is false (Remark 7.3).
2. T9a(iii): "T9 holds with $\varepsilon_n^2=(s_0+1)\ell_n/n$, with a constant depending also on the constant in the hypothesis; (ii) under $\ell_n=o(n)$". The hypothesis is now a theorem for polynomial $p$ under (SE), standardisation and the cap condition (Theorem 13), with constant $C_1'=2A+2$; the draft can state T9a(iii) unconditionally in that regime and keep it open for super-polynomial $p$.
3. T9: no change needed; (i) holds for every $p$; the sharper form of (ii) (Corollary 5.1) may be quoted.

## Cited results

- Fact D (T6 Theorem 8 and Remark 4.1, `proofs/T6/PROOF.md`): restated correctly, used within hypotheses (all six round-1 reviewers; T6 itself is not adopted).
- L6(i), L6(v): as Lemma 3 of `proofs/T6/PROOF.md`.
- Fact G (Vershynin 2018, Theorem 4.6.1 and display (4.22)): **verified against the source** by the researcher (First Edition PDF; `CITED_RESULTS.md`); the page number in the printed CUP copy is unverified.
- Elementary facts used without citation: Chebyshev, Markov, Chernoff for $\chi^2$ and Gaussian tails, Schur determinant identity, Weyl's inequality, Stirling-type bound $\Gamma(x+1)\ge(x/e)^x$, Pólya's theorem (Remark 6.2 only).

## Assumptions

Listed in PROOF.md Section 8: $n\ge4$; the two statement amendments; (H1) to (H4) for Section 9; the reading of $f_\theta$ under standardisation; the reference measure for the Hellinger distance.

## Agents and calls

- Fable: 1 (the lead; no prover sub-agents).
- Opus 5.5: round 1, 3 reviewers (xhigh); round 2, 3 reviewers (xhigh, interrupted, no report); 2 operators (high); 1 researcher (high). Total 9 agents.
- GPT-6 Astra: 6 calls (xhigh), all successful, no retries, no resumes.
- Harness note: the three round-1 Opus reviewers were blocked from writing their report files; the lead saved their replies verbatim.

## Adoption

NOT ADOPTED. The proof enters the paper only after the person's walkthrough and adoption.
