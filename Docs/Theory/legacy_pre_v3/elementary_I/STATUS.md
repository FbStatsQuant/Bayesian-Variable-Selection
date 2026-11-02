# STATUS — elementary_I thread (P1, T1, L1, L2, L3, L7, L5)

Dates: 2026-10-14 to 2026-10-15. Protocol: theorem proving (`protocols/proof.md`), lead Fable 5.1 (high), reduced for a non-interactive coordinated run (no STATEMENT.md sign-off round; the statements are frozen verbatim from the draft in PROOF.md Section 0.3 with readings flagged).

## Current state (2026-10-15)

- **Phase 1 closed** at the protocol's three-round cap. Final text: `PROOF.md` **v4** (frozen as `review/PROOF_v4.md`; v1–v3 in `review/`; diffs `review/diff_v1_v2.txt`, `diff_v2_v3_lf.txt`, `diff_v3_v4.txt`). v4 differs from the reviewed v3 by wording only (the beta-binomial pole sentence, the notation paragraph, three symbol renamings, two added justifications, two Section 9 additions) and has not been re-reviewed.
- **Outcome:** all seven results are true as stated (under the readings of Section 0.3/9). In three rounds of six blind reviewers (3 Opus xhigh + 3 Astra GPT-6 xhigh per round), **no reviewer found an error in the proof of any statement**; every finding concerned remarks, flags for the draft, conventions, symbol clashes or editing artefacts, and all were accepted and applied. Round-3 verdicts: Opus B and Opus C "every step verified"; Opus A, Astra A/B/C "not verified" on the single side sentence about beta-binomial poles (fixed in v4). Rulings: `FINDINGS.md`. Report: `VERIFICATION_REPORT.md`; retrospective draft: `RETRO.md`.
- **Added results:** Theorem 4.4 ($\Delta_{\det}\ge0$, equality iff block-orthogonal, so $d\ge\nu\Psi$); Theorem 6.2's equality $\inf_{[\phi_a,\phi_b]}q_\phi(S^\ast)=\min$ of the endpoints; Corollary 7.3 (L7's hypothesis reduces to the two endpoints); Proposition 2.6(d)–(e) and Remark 2.7 (exactly when the start factorises). Flags for the draft in PROOF.md Section 9 (cap $k_{\max}\le p$; P1 cost and "not a product" wording; L1/L2 readings; L3/L7 sharper forms; L5 note).
- **Numerical checks:** `check_elementary_I.py` → `check_elementary_I.out`, local, seed 1: 36 checks, 36 PASS.
- **Counts:** Fable: 1 (the lead session), prover sub-agents 0. Opus: operator 1 (high), reviewers 4 agents (xhigh; one stalled after delivering its round-2 report and was replaced). Astra: 3 sessions, 9 calls (xhigh). Session ids in `review/astra_X/astra_run*.log`.
- **Not done (by design of the brief):** Phase 2 readability rewrite and its re-check; LaTeX version; LEAN_HANDOFF.md. The Markdown proof is written for the supplement and can go to Phase 2 on request.
- **Adoption:** not adopted; all results provisional until the person walks through PROOF.md.
- **Resume point:** nothing pending. Next steps, if wanted: (i) the person's adoption walkthrough (small chunks, as in `learn-math.md`); (ii) Phase 2 readability pass plus LaTeX; (iii) Lean handoff decomposition; (iv) apply the Section 9 flags to `paper_draft.tex`.

## History

- 2026-10-14: v1 written and checked (29/29); round 1 launched (packet `review/`, Astra via `review/run_astra.sh`).
- 2026-10-14: round 1 rulings; v2 (Theorem 4.4, Prop. 2.6(d)–(e), Prop. 2.4 recount, conventions, Remark 8.4(b) rewritten); checks 33/33; round 2 launched.
- 2026-10-15: round 2 rulings; v3 (Prop. 2.6(d) strengthened to every beta-binomial prior with $p\ge2$; Remark 4.5 corrected; notation); round 3 launched on the v2→v3 diff.
- 2026-10-15: round 3 rulings; v4; checks 36/36; VERIFICATION_REPORT.md and RETRO.md written by the operator; memory note saved.
