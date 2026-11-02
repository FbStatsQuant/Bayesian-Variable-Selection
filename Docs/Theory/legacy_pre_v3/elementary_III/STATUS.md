# STATUS — elementary_III thread (P5, P8, P9, P10, P11)

Date: 2026-10-15. Protocol: theorem proving (`protocols/proof.md`), lead Fable 5.1 (high), reduced per `proofs/THREAD_RULES_wave3.md` (no sign-off round; statements frozen verbatim in PROOF.md Section 0; three Opus + three Astra blind reviewers, at most 3 rounds; no Phase 2, no LaTeX, no Lean handoff).

## Plan

1. Section 0: frozen statements (verbatim from `paper_draft/paper_draft.tex`, 15 Oct), setting, readings.
2. P5 (decisions): (i)–(ii) brief; (iii) capped Hamming minimiser in full (rearrangement argument on $\sum_{j\in a}(1-2\,\mathrm{PIP}_j)$).
3. P8 (certificates): (i)–(iii) direct; (iv) with the shrinkage floor re-derived (push-through identity, valid for every $|S|$); (iv′) via monotone $f(\lambda)=((n+1)\lambda+1)/(\lambda+1)$ and Cauchy interlacing, $\varrho=f(n\varphi^2)$; (v) termwise.
4. P9 (truncation): exact identity $\mathrm{PIP}_j=(1-f)\mathrm{PIP}_{j,V}+\pi(A_j\cap V^c)$; TV $=f$ with $\sup_A$; (ii), (iii) direct.
5. P10 (visited-set bound): set-up with $V=V(y,\zeta)$ and draws independent of $\zeta$ given $y$; (i) $f^M$ plus the exact bias of the safeguards; (ii) $\{Z\le U_V\}=\{f\le f_U\}$, Clopper–Pearson validity proved; conditional coverage is $0$ for $f\in((1-\alpha)^{1/M},1)$; (iii) union bound with P7(ii)(a) under (H0)–(H4) of foundations.
6. P11 (RB PIPs): $\sigma$-field statement, "zero conditional variance" defined, law of total variance, counterexample with post-update weights.
7. `check_elementary_III.py` → `.out` (single seed).
8. Reviews: operator (Opus) builds the packet and runs Astra; 3 Opus reviewers (xhigh); rulings in FINDINGS.md; up to 3 rounds.
9. VERIFICATION_REPORT.md, RETRO.md.

## Strategy in play

Direct proofs; no sub-agents expected (all items elementary). Save PROOF_wip.md after each proposition.

## Log

- 2026-10-15: inputs read (draft Sections 2 and 5; foundations P7 Section 5; T5 mode-loss remark). STATUS.md created. Next: Section 0 of PROOF_wip.md.
- 2026-10-15: Section 1 (P5) proved: Thms 1.1–1.3, Example 1.4, Remark 1.5. Next: Section 2 (P8). Strategy: direct.
- 2026-10-15: Sections 2-6 written (P8, P9, P10, P11, flags) and assembled into PROOF_wip.md (v1 draft). Next: check_elementary_III.py, then review round 1.
- 2026-10-15: check_elementary_III.py: 43 checks, 43 PASS (seed 1). PROOF.md v1 frozen (= review/PROOF.md). Next: operator builds packet (PACKET_README.md, STATEMENTS_FROM_DRAFT.md), runs Astra A/B/C; lead spawns Opus A/B/C (xhigh). Round 1.
- 2026-10-15: Round 1 launched: Opus A/B/C (xhigh) reviewing review/PROOF.md (v1); operator running Astra A/B/C. Lead self-check pass done; pending v2 edits (to apply after round-1 rulings): (e1) P8(iii) presupposes U >= Z, add to reading R2 and Section 6 item 2.
- 2026-10-15: Opus A and B round-1 reports received and saved verbatim (review/opus_A, opus_B). Control-character corruption at Example 1.4 (from a scripted edit) repaired in PROOF_wip.md. Waiting on Opus C and Astra A/B/C before rulings. v2 edit list so far: e1 (U>=Z in P8(iii)); A-G1/B14 (Remark 1.5 at kmax=0); A-G2/B2a/B2b (Theorem 4.8: per-island conditional unbiasedness, Theorem 5.7 given the pilot, (H2) wording); B1 (unconditional reading of P10(iii), restrict what zeta contains for the conditional form); A-E2..E13, B4..B15.
- 2026-10-15 (relaunch): thread relaunched. Found: Opus A, Opus B, Astra A/B/C round-1 reports on disk; Opus C report missing (agent output lost in the crash; only its check scripts survived). Action: re-spawn Opus C (xhigh) on v1; rule on the five reports now (FINDINGS.md); apply v2 edits (parts/edits_v2_batch1.txt plus the new rulings); extend the check script; then round 2 on the changed parts. Strategy unchanged (direct proofs).
- 2026-10-15 (relaunch, cont.): v2 edits applied to PROOF_wip.md (batches parts/edits_v2_batch1.txt, batch2.txt, parts/thm48_v2.md, parts/renames_v2.py). check_elementary_III.py extended (10 new checks): 53/53 PASS. Next: FINDINGS.md (round-1 rulings on Opus A/B, Astra A/B/C); wait for the re-run Opus C (v1) report, rule, patch; freeze PROOF.md v2; round 2 (changed parts) with 3 Opus + 3 Astra. Strategy unchanged.
- 2026-10-15 (relaunch, cont.): FINDINGS.md written (round-1 rulings T1-T29 on Opus A/B, Astra A/B/C; Opus C re-run pending). Round-2 packet prepared in review/round2/ (PACKET_README.md, CHANGES_v2.md, run_astra_round2.sh); PROOF.md v2 not yet frozen (waiting for Opus C's v1 report to rule on it first). Next: rule on Opus C, patch, copy PROOF_wip.md -> PROOF.md and review/round2/PROOF.md, spawn Opus A/B/C (xhigh) + operator (Astra).
- 2026-10-15 (relaunch, cont.): Opus C (re-run, v1) report saved verbatim (review/opus_C/REPORT_C_opus.md): 0 fatal, 2 gaps (both already fixed in v2: T15, T17), 14 exposition items (2 new: E9 tie-rule note, E11 per-particle sigma-field; fixed, parts/edits_v2_batch3.txt). PROOF.md v2 FROZEN, sha256 30e1ef97db4fca93..., copied to review/round2/PROOF.md. Next: launch round 2 (Opus A/B/C xhigh on changed parts; operator runs Astra A/B/C via review/round2/run_astra_round2.sh and updates CITED_RESULTS.md).
