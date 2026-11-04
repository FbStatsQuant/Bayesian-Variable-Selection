# HQ charter · LP-AUDIT · certificate and output-event lemma pack (code-audit wave)

| Field | Value |
|---|---|
| HQ | LP-AUDIT · certificate and output-event lemma pack (code-audit wave) |
| Wave (MINUTES §2.5) | 3 |
| Covers | S-CERT + S-OUT |
| K-IDs | S-CERT: K64, K73 (no region-certification clause), K74, K05, K108; S-OUT: K77, K78, K83–K86, K63 |
| Final card(s) | `THEOREM_LIST_FINAL.md` Part II: `THEOREM_LIST_FINAL.md:927` (S-CERT); `THEOREM_LIST_FINAL.md:965` (S-OUT) |

**[charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]**

## Wave and reason (MINUTES §2.5, verbatim)

**Source:** `theory_campaign/MEET-THM/MINUTES.md:109` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:109-109 -->
| 3 | **M5** HPM; **M4** Z𝒯 + masked statement; **M8** Prop D; **LP-AUDIT** = S-CERT + S-OUT | Code-audit wave: N2, N3, LS0, GUARD-W and the DAG serve M5, M4 and M8 together. M4(f) needs M5 |
<!-- END VERBATIM -->

## Dependencies (from the seats' §S3(a) edge lists)

X → Y means Y uses X.

**A §S3(a)** (`theory_campaign/MEET-THM/R3_A.md:166–172`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_A.md:168` — S-OUT (Lemma RO, GUARD-W, IND-T) → M1(c,d)
- `R3_A.md:168` — S-OUT → M4(d)
- `R3_A.md:168` — S-OUT → M5(0)
- `R3_A.md:168` — S-OUT (K63, K83–K86) → M8
- `R3_A.md:172` — S-CERT (Theorem A, LS-score, Lemma M, Lemma S) → M5(1),(2)
- `R3_A.md:172` — M1, S-OUT → M8

**B §S3(a)** (`theory_campaign/MEET-THM/R3_B.md:222–237`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_B.md:227` — GUARD-W → M1, M4, S-OUT
- `R3_B.md:235` — S-CERT → M8 (search cost), M4 (card semantics)
- `R3_B.md:236` — S-OUT → M4 (e), M1 (a contract)

**C §S3 (edge list)** (`theory_campaign/MEET-THM/R3_C.md:254–281`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_C.md:257` — L-RO → S-OUT
- `R3_C.md:257` — A-STREAM → S-OUT
- `R3_C.md:257` — A-GUARD → S-OUT
- `R3_C.md:263` — S-CERT → L-LS
- `R3_C.md:264` — S-OUT → M5
- `R3_C.md:266` — S-OUT → M1(output clauses)
- `R3_C.md:272` — S-CERT → M8
- `R3_C.md:272` — S-OUT → M8
- `R3_C.md:274` — S-CERT → M4
- `R3_C.md:274` — S-OUT → M4
- `R3_C.md:281` — S-OUT → S-REP

**D §S3(a)** (`theory_campaign/MEET-THM/R3_D.md:183–205`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_D.md:189` — S-OUT(K77,K78,K83–K86,K63) → M1
- `R3_D.md:189` — S-OUT → M4
- `R3_D.md:189` — S-OUT → M5
- `R3_D.md:189` — S-OUT → Prop D
- `R3_D.md:190` — S-CERT(K64,K74,K108) → M5
- `R3_D.md:190` — S-CERT → M4
- `R3_D.md:190` — S-CERT → Prop D

## Binding goal and escalation safeguard (MINUTES §2.3)

No binding theorem of its own, but M1(c),(d), M4(e), M5 and M8 rest on S-OUT (Lemma RO, GUARD-W, IND-T extension, worker equivalence, stacking nesting). The M1 charter escalation evidence applies if the GUARD-W or IND-T extension audit fails.

## Named implementation premises / audit obligations (MINUTES §2.3)

The integrated audits: streams (IND-T extension, N2/N14), LS0 (N2(c)), GUARD-W stop-only coupling (N2(e)), the execution DAG (N15), K84/N14(a) extra-search nesting; N14(c) IND-T extension (independence of streams 10..9+R′, R′ > 4). N7: K73 operational region certification withheld; N16/K107 numerical gap explicit (K108 stays). MINUTES §2.5: "Code-audit wave: N2, N3, LS0, GUARD-W and the DAG serve M5, M4 and M8 together."

General rule (MINUTES §2.3, verbatim):

**Source:** `theory_campaign/MEET-THM/MINUTES.md:87` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:87-87 -->
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM -->

## Charter [charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]

| Item | Text |
|---|---|
| Goal | Prove/close the listed supplement statements: S-CERT + S-OUT. |
| Statement | The cards in `THEOREM_LIST_FINAL.md` Part II named above (K-IDs: S-CERT: K64, K73 (no region-certification clause), K74, K05, K108; S-OUT: K77, K78, K83–K86, K63). Statements are as filed by the seats; seat variants and the chair's editorial choices ("Chair's choices") are in that file. |
| First lemma | (none specified by the seats for the pack; each card's route is in its seat card) |
| Fallback | Each card's own fallback (verbatim below where a seat card states one). **Chair's generic rule (IC7), for every card in this pack:** the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded. |
| Stop rule | Each card's own stop rule (below where stated); otherwise one proof attempt plus one cross-family check-and-repair cycle per card, then the generic rule above. |
| Escalation | As in the Binding goal / safeguard section above; otherwise none. |

## Cards' own fallback / stop rows (verbatim, where a seat card states them)

Card `C13 — K77`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:211` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:211-211 -->
| Fallback / stop | Potential-run theorem while the audit remains open. Never replace it with completion-conditioned validity. |
<!-- END VERBATIM -->

**Chair-specified fallback for S-CERT (IC7, final audit #8):** the deterministic perturbation lemma K108 (Z̃/Z ∈ [e^{−ε}, e^{ε}], TV ≤ tanh ε, and gap > 2ε preserves the winner). Also the exact semantics of the local-search flags (K64, a weak local maximum, with ties allowed). No B&B-soundness, rounding or region-certification claim. Stop rule: the generic rule.
