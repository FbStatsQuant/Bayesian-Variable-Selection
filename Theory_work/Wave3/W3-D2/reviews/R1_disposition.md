# W3-D2 — council R1 disposition (lead, 2026-11-17)

Manifest R1: MANIFEST 6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243.
- Sol seat (`reviews/R1_council_sol.md`): Thm2X ACCEPT, Cor2X ACCEPT; score 9.2; **gates=FAIL** (faithful, sweep) on F1.
- Opus seat (`reviews/R1_council_opus.md`, claude_third): Thm2X ACCEPT, Cor2X ACCEPT; score 9.6; gates=PASS; E1–E8 only.
R1 does not pass (Sol gates FAIL). Accepted F finding → diff round D1 (Opus-only, per the ticket; new thread on
claudeAgent_personal, per the manager's account check), which also checks the E items applied in the same diff.

| finding | tag | disposition | where |
|---|---|---|---|
| sol F1 N1 grid: lgamma cancellation at p = 10¹⁵ changes m♯_n in 19/150 cases; max 0.3928 not 0.3942 | F | ACCEPT: exact ratio recurrence q_{k+1}/q_k = (p−k)/(2p−1−k), log C(2p−1, s₀) by a short sum; rerun: only the max line changes, 0.3928 (= the seat's independent 0.3928391); m♯_n(10⁵, 10¹⁵, 1) = 76 as the seat computed. TARGET updated. No claim depends on N1 | numerics/, TARGET |
| sol E1 REPORT §3a "B strictly stronger …, per the note" unlabelled | E | ACCEPT: labelled OPEN | REPORT §3a |
| opus E1 k̄_n ≤ 3(…) log n stated without proof | E | ACCEPT: PROOF P5 (remark, not a claim); pointer in STATEMENT §7 | PROOF P5 |
| opus E2 "Σ need not be a correlation matrix" is cosmetic | E | ACCEPT: softened (STATEMENT §7, TARGET) | |
| opus E3 STATEMENT §3 attribution covers only the PIP fact | E | ACCEPT: sentence aligned with PROOF P0 | STATEMENT :63-64 |
| opus E4 "α* may even be random" is about the master | E | ACCEPT: marked as remarks on the master | PROOF P3, P4 |
| opus E5 card: two inputs are wave-1 results | E | ACCEPT (wording for HQ) | REPORT §3 |
| opus E6 "(S1) with σ² allowed to depend on n"; 1 ≤ \|T\| | E | ACCEPT | REPORT §3, READER_DELTA |
| opus E7 "Theorem 4 … plus the deterministic PIP/MPM consequences" | E | ACCEPT | STATEMENT §4(a), REPORT §3, READER_DELTA |
| opus E8 N1 docstring "Lemma D2-B1" | E | ACCEPT | numerics |
Better-theorem proposals (opus 1–4: fixed-level beta-min; random intercept; ξ_q and sup_{T≠S₀} bounds; hypotheses only for
large n): logged for HQ, not adopted (STRONGER beyond CP1 needs HQ's go). Line shifts: STATEMENT §3 is now :60-64, §5 :81-86
(REPORT premises and DEPS updated). Claim spans §1 :29-48 and §2 :50-58 unchanged.
