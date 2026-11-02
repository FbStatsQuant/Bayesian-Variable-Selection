# STATUS — proof of T7, T8 and T10 (by-product)

Protocol: theorem proving (`proof.md`), reduced for a non-interactive coordinated run: the precise statements are frozen inside PROOF.md §0.2 (no separate sign-off possible); one blind correctness round with three Opus (xhigh) reviewers, angles A/B/C; Astra reviewers not run in this thread (requires the operator/codex step; can be added later).

- 2026-10-14 — Proof written by the lead (Fable 5.1): PROOF.md v1 (Sections 0–6), kept as `review/PROOF_v1_prereview.md`. Strategy: supersets counted size by size with the exact integrated-variance Bayes factor and a truncated chi-square moment (Prop. 4.2); underfitting models compared with S ∪ S0, grouped by S' (Lemma 5.3), large |J'| disposed of by the superset slack, small |J'| by a uniform O(log n) noise bound; T6 made quantitative in Lemma 3.1 for the rates; T10 obtained from the same underfitting step with the beta-min on one coordinate (§5.5).
- 2026-10-14 — Single-seed numerical check of every deterministic identity and inequality: `check_T7_T8.py` (ALL CHECKS PASSED, 40 checks incl. a 200-pair stress test).
- 2026-10-14 — Review round 1 (blind, Opus xhigh ×3): `review/REPORT_{A,B,C}_opus.md`, scripts `review/REVIEW_{A,B,C}_check.py`. Verdicts: A, B, C all **every step verified**; 0 fatal; 1 gap-level item (statement fidelity: the rate needs (SE) at the m_n built with ω_n ≥ ½ log n), ~15 exposition items. Rulings in FINDINGS.md; all accepted items applied → PROOF.md v2 (no mathematical step changed). Check script rerun on v2: all passed.
- Adoption: **not adopted**.

Outcome summary: T7 convergence true as stated for every ω_n → ∞; T7 rate true under (SE$_{1/2}$) (the m_n with ω_n = ½ log n), otherwise O_P(√(log n/n) + e^{-ω_n}); T8(i)–(iii) true, (iii) under the same precision, with beta-min scale σ⋆² in place of σ⋆²+M; T10 true as stated (plus a rate).

Open: Laurent–Massart reference to be checked against the source (CITED_RESULTS.md); the draft should name ω_n in T7 or display (SE$_{1/2}$).

Resume point: PROOF.md v2 is complete and reviewed once. Optional next steps: Astra round (3 reviewers) on v2; Phase 2 readability pass; Lean handoff.
