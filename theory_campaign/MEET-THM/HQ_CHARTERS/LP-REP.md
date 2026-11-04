# HQ charter · LP-REP · reporting corollaries lemma pack

| Field | Value |
|---|---|
| HQ | LP-REP · reporting corollaries lemma pack |
| Wave (MINUTES §2.5) | 4 |
| Covers | S-REP + S-LEAK |
| K-IDs | S-REP: K104/K11 reporting corollary (using K46/K52/K102); S-LEAK: B's (F), (S) clauses |
| Final card(s) | `THEOREM_LIST_FINAL.md` Part II: `THEOREM_LIST_FINAL.md:1192` (S-REP); `THEOREM_LIST_FINAL.md:1138` (S-LEAK) |

**[charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]**

## Wave and reason (MINUTES §2.5, verbatim)

**Source:** `theory_campaign/MEET-THM/MINUTES.md:110` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:110-110 -->
| 4 | **LP-REST** = S-Z + S-POOL + S-LIM; **LP-REP** = S-REP + S-LEAK | Consequences and reporting corollaries. Nothing binding waits on them |
<!-- END VERBATIM -->

## Dependencies (from the seats' §S3(a) edge lists)

X → Y means Y uses X.

**A §S3(a)** (`theory_campaign/MEET-THM/R3_A.md:166–172`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_A.md:170` — M1 → S-REP
- `R3_A.md:170` — S-IDENT → S-REP
- `R3_A.md:170` — M2(a) → M1(i), S-REP, S-Z (D bound)
- `R3_A.md:170` — M2(b)(iv) → S-REP (Ĵ tail)
- `R3_A.md:170` — S-LEAK → M2 (supplement corollary).
- `R3_A.md:172` — M4 → S-REP (card labels)

**B §S3(a)** (`theory_campaign/MEET-THM/R3_B.md:222–237`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_B.md:228` — M1 → S-REP
- `R3_B.md:228` — N1 → S-REP
- `R3_B.md:230` — M3 → S-LEAK
- `R3_B.md:232` — T03♯ (S-T) → M2 (c1), M5, M4 (f), M1 (f), S-LEAK
- `R3_B.md:233` — M2 → S-REP (eta-hat domain, D_* in the J-hat bound)

**C §S3 (edge list)** (`theory_campaign/MEET-THM/R3_C.md:254–281`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_C.md:281` — M1 → S-REP
- `R3_C.md:281` — M2 → S-REP
- `R3_C.md:281` — M3 → S-REP
- `R3_C.md:281` — S-OUT → S-REP

**D §S3(a)** (`theory_campaign/MEET-THM/R3_D.md:183–205`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_D.md:183` — Gelman–Meng 1998 → S-REP, M6
- `R3_D.md:186` — S-KERNEL → S-REP
- `R3_D.md:187` — S-TARGET → S-REP
- `R3_D.md:193` — S-IDENT → S-REP
- `R3_D.md:197` — M2(a) → S-REP
- `R3_D.md:197` — M2 → S-LEAK(F,S)
- `R3_D.md:198` — M1 → S-REP

## Binding goal and escalation safeguard (MINUTES §2.3)

None. MINUTES §2.5, wave 4: "Nothing binding waits on them." Failure inherited from N1 or M2 triggers their binding-goal escalation, not a silent waiver (S-REP card, fallback row).

## Named implementation premises / audit obligations (MINUTES §2.3)

Read-only initial and measured-endpoint discrepancy accumulators; integrated accumulator and extended-stream fidelity require audit (S-REP card); AMENDMENT_HQ_02 definitions (Ĵ, ε̂_× with companions, d in 𝓗, the two R′ growth rates).

General rule (MINUTES §2.3, verbatim):

**Source:** `theory_campaign/MEET-THM/MINUTES.md:87` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:87-87 -->
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM -->

## Charter [charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]

| Item | Text |
|---|---|
| Goal | Prove/close the listed supplement statements: S-REP + S-LEAK. |
| Statement | The cards in `THEOREM_LIST_FINAL.md` Part II named above (K-IDs: S-REP: K104/K11 reporting corollary (using K46/K52/K102); S-LEAK: B's (F), (S) clauses). Statements are as filed by the seats; seat variants and the chair's editorial choices ("Chair's choices") are in that file. |
| First lemma | (none specified by the seats for the pack; each card's route is in its seat card) |
| Fallback | Each card's own fallback (verbatim below where a seat card states one). **Chair's generic rule (IC7), for every card in this pack:** the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded. |
| Stop rule | Each card's own stop rule (below where stated); otherwise one proof attempt plus one cross-family check-and-repair cycle per card, then the generic rule above. |
| Escalation | As in the Binding goal / safeguard section above; otherwise none. |

## Cards' own fallback / stop rows (verbatim, where a seat card states them)

Card S-REP (R3_C §S2):

**Source:** `theory_campaign/MEET-THM/R3_C.md:241` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:241-241 -->
| Fallback/stop rule | Retain precisely labelled descriptive fields if quantitative proof closure fails. If records are unavailable, report NA. Stop after one failed proof/audit repair cycle; remove quantitative reporting claims. Failure inherited from N1 or M2 triggers their binding-goal escalation, not a silent waiver. |
<!-- END VERBATIM -->

**Chair-specified fallback for S-LEAK (IC7, final audit #8):** the finite-law exact identity 1 + χ²(π‖π₀) = π(S₀)²/(π₀(S₀)·q₂(S₀)), plus the data-dependent bound m ≥ π₀(S₀)·e^{−2·osc d}. No design-uniform lower bound on m. (F) is dropped if its leakage route fails. Stop rule: the generic rule.
