# HQ charter · LP-IDENT · identification and ideal-grid lemma pack

| Field | Value |
|---|---|
| HQ | LP-IDENT · identification and ideal-grid lemma pack |
| Wave (MINUTES §2.5) | 2 |
| Covers | S-IDENT (S-STGI dissolved per corrected MINUTES §2.2: K30 → M7(d), charter `M7.md`; K29 → FW23) |
| K-IDs | S-IDENT: K25 lemma, K104, K55, K103 (C15-TV/KL/CI named). S-STGI dissolved: K30 → M7(d), K29 → FW23 |
| Final card(s) | `THEOREM_LIST_FINAL.md` Part II: `THEOREM_LIST_FINAL.md:724` (S-IDENT); the S-STGI section there is historical (dissolved) |

**[charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]**

## Wave and reason (MINUTES §2.5, verbatim)

**Source:** `theory_campaign/MEET-THM/MINUTES.md:108` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:108-108 -->
| 2 | **M2** WS (binding §5.3); **M7** STG; **M6** SEP + KL; **LP-IDENT** = S-IDENT | The §5.3 package and its inputs (d_σ from M3, the count from M7, the lower bound from M6) |
<!-- END VERBATIM -->

## Dependencies (from the seats' §S3(a) edge lists)

X → Y means Y uses X.

**A §S3(a)** (`theory_campaign/MEET-THM/R3_A.md:166–172`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_A.md:168` — S-KERNEL (K103) → S-IDENT
- `R3_A.md:170` — S-IDENT (K104, K25) → M2
- `R3_A.md:170` — S-IDENT → M7(e)
- `R3_A.md:170` — S-IDENT → S-REP

**B §S3(a)** (`theory_campaign/MEET-THM/R3_B.md:222–237`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_B.md:231` — M7 → S-STGI (K30 cited)
- `R3_B.md:233` — S-KERNEL (minorisation) → M2 (b4), S-IDENT

**C §S3 (edge list)** (`theory_campaign/MEET-THM/R3_C.md:254–281`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_C.md:278` — S-KERNEL → S-IDENT
- `R3_C.md:278` — M1 → S-IDENT
- `R3_C.md:278` — M2 → S-IDENT(W rates)
- `R3_C.md:278` — L-ESS → S-IDENT
- `R3_C.md:279` — STG-M recurrence → S-STGI
- `R3_C.md:279` — cited K28 → S-STGI

**D §S3(a)** (`theory_campaign/MEET-THM/R3_D.md:183–205`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_D.md:193` — S-IDENT(K25,K103,K104) → M7
- `R3_D.md:193` — S-IDENT → M2(b)
- `R3_D.md:193` — S-IDENT → M6
- `R3_D.md:193` — S-IDENT → S-REP
- `R3_D.md:198` — M1 → S-IDENT(TV cell bound)
- `R3_D.md:201` — S-STGI(K29,K30) → M7(c)

## Binding goal and escalation safeguard (MINUTES §2.3)

No binding theorem of its own. S-IDENT's C15-CI is the HQ Q2 deliverable (posterior-content reading of §5.4 credible-interval coverage; the frequentist half is FW1): it must be proved or its loss reported, not silently dropped (MINUTES §2.2, S-IDENT row).

## Named implementation premises / audit obligations (MINUTES §2.3)

No audit obligation in the cards. K29 stays a cited conditional implication; its unconditional favourable application is FUTURE_WORK.

General rule (MINUTES §2.3, verbatim):

**Source:** `theory_campaign/MEET-THM/MINUTES.md:87` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:87-87 -->
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM -->

## Charter [charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]

| Item | Text |
|---|---|
| Goal | Prove/close the listed supplement statements: S-IDENT. (S-STGI rows below are kept for reference only; S-STGI is dissolved.) |
| Statement | The cards in `THEOREM_LIST_FINAL.md` Part II named above (K-IDs: S-IDENT: K25 lemma, K104, K55, K103 (C15-TV/KL/CI named); S-STGI dissolved). Statements are as filed by the seats; seat variants and the chair's editorial choices ("Chair's choices") are in that file. |
| First lemma | (none specified by the seats for the pack; each card's route is in its seat card) |
| Fallback | Each card's own fallback (verbatim below where a seat card states one). **Chair's generic rule (IC7), for every card in this pack:** the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded. |
| Stop rule | Each card's own stop rule (below where stated); otherwise one proof attempt plus one cross-family check-and-repair cycle per card, then the generic rule above. |
| Escalation | As in the Binding goal / safeguard section above; otherwise none. |

## Cards' own fallback / stop rows (verbatim, where a seat card states them)

Card `C15-TV — K103`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:231` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:231-231 -->
| Fallback / stop | Coarsened TV and bounded-functional error; no useful masked full-TV claim. |
<!-- END VERBATIM -->

Card `C15-KL — K103`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:241` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:241-241 -->
| Fallback / stop | Fixed-data directional bounds. No forward-KL convergence rate without controlling \(\pi_{\min}\); no silent smoothing. |
<!-- END VERBATIM -->

Card `C15-CI — K103`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:252` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:252-252 -->
| Fallback / stop | Predeclared interval endpoints with simultaneous CDF bounds; unavailable historical records remain unavailable. |
<!-- END VERBATIM -->

Card `C14 — K30`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:221` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:221-221 -->
| Fallback / stop | This ideal comparison theorem only. K31 remains FUTURE_WORK. |
<!-- END VERBATIM -->

