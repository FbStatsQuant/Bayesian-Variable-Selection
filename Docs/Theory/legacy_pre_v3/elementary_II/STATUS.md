# STATUS — elementary_II thread (Ex1, Ex2, C1, P3, P4, Pb2)

Date: 2026-10-15. Protocol: theorem proving (`protocols/proof.md`), lead Fable 5.1 (high), reduced per `proofs/THREAD_RULES_wave3.md`. First reply states the protocol: theorem proving, because the deliverables are proofs of six draft items headed for the paper.

## Plan
1. Freeze the six statements verbatim (PROOF.md §0). Flag readings.
2. Prove in this order (each item written to PROOF_wip.md when done): P3, P4, Pb2, Ex1, C1, Ex2.
   - P3: order-first argmax decomposition; HPM = \hat S_{\hat k}; W event; supremum over w.
   - P4: orthogonal design algebra from eq:m; neighbour log-odds; top-k; known variance.
   - Pb2: explicit n=10, X orthogonal, y; compute scores exactly (rational/float); show k->max score is 1, 2/3, >4/3 pattern; greedy misses.
   - Ex1: compute gamma_b via Lemma 1(b) of T3_T11; sigma-bar formulas; kappa0>0; single deletion; aligned blocks.
   - C1(i): list hypotheses of T6-T10 from their proofs; show none involves x_j^T y or gamma_b. C1(ii): check (U),(R), constants, gamma, T3(iii) applicability (needs (R): exact cancellation gives R1 = 0 and R2 linear).
   - Ex2: exact finite-sample conditions (p=2, cap 2, BB(1,2)); asymptotic leading terms; L>4kappa_pair equivalence; verify "heuristic" label.
3. Numerical checks: check_elementary_II.py / .out.
4. Review: 3 Opus (xhigh) + 3 Astra (xhigh), angles A/B/C; up to 3 rounds; FINDINGS.md.
5. VERIFICATION_REPORT.md, RETRO.md, CITED_RESULTS.md (researcher), FAILED_ATTEMPTS.md.

## Strategy in play
Direct computation from eq:m and the T3_T11 lemmas (Lemma 1 geometry of sigma-bar, Lemma 4 three regimes). No external results expected beyond the draft's own proofs.

## Log
- 2026-10-15: inputs read (draft §2, §3.3, §4; T3_T11 §0-§6; T6 §0,§7; T7_T8 §0,§6; T9_C9 §0,§8; foundations §3 (L6); elementary_I §0,§9, STATUS, review tooling). STATUS.md created. Next: freeze statements, prove P3.
- 2026-10-15: check_elementary_II.py written and run: 32/32 pass. PROOF_partA.md saved (Sections 0-4: setting, frozen statements, readings, P3, P4, Pb2). Next: PROOF_partB.md (Sections 5-6: Ex1, C1), then partC (Section 7: Ex2 incl. second-order expansion Prop 7.4), then partD (Sections 8-9: flags, numerics); concatenate into PROOF.md. Strategy unchanged.
- 2026-10-15: PROOF_partB.md saved (Sections 5-6: Ex1 Props 5.1-5.6; C1 Thm 6.1, Props 6.3-6.5, Thm 6.6). Next: PROOF_partC.md (Section 7, Ex2: 7.1 identities, 7.2 exact conditions, 7.3 equivalence + strengthening to all rho, 7.4 second-order expansion via (F-dec) + delta method + chi-square CLT, 7.5 status of window paragraph = heuristic label accurate, 7.6 switch possible at n=100 and probability -> 0).
- 2026-10-15: PROOF_partC.md saved (Section 7, Ex2: Props 7.1-7.6, Lemmas 7.4.1-7.4.3; window label confirmed heuristic; strengthening L>4kappa_pair for all rho). Next: PROOF_partD.md (Sections 8-9), concatenate to PROOF.md and PROOF_wip.md, then review packets (round 1: 3 Opus xhigh + 3 Astra xhigh), FAILED_ATTEMPTS.md, CITED_RESULTS.md.
- 2026-10-15: PROOF.md v1 assembled (Sections 0-9), PROOF_wip.md = v1; check rerun 32/32. Next: review round 1 (packets in review/, 3 Opus xhigh agents + 3 Astra via codex), FAILED_ATTEMPTS.md, CITED_RESULTS.md (researcher).
- 2026-10-15: Review round 1 launched: Astra A/B/C via review/run_astra.sh (background), Opus A/B/C reviewers (xhigh) writing to review/opus_X/REPORT_X_opus.md, researcher (Opus high) writing CITED_RESULTS.md. FAILED_ATTEMPTS.md created. Waiting for reports; then rulings in FINDINGS.md, revise PROOF.md (v2), round 2 if needed.
