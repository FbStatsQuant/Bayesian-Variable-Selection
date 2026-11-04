# HQ charter · LP-FOUND · foundations lemma pack

| Field | Value |
|---|---|
| HQ | LP-FOUND · foundations lemma pack |
| Wave (MINUTES §2.5) | 1 |
| Covers | S-TARGET + S-BLOCKS + S-KERNEL (S-T cited, no HQ work) |
| K-IDs | S-TARGET: K01–K05, K76, K95; S-BLOCKS: K07, K14, K06; S-KERNEL: K20, K21, K08, K09, K22, K103 (S-T: K93, K04, cited) |
| Final card(s) | `THEOREM_LIST_FINAL.md` Part II: `THEOREM_LIST_FINAL.md:503` (S-TARGET); `THEOREM_LIST_FINAL.md:580` (S-BLOCKS); `THEOREM_LIST_FINAL.md:633` (S-KERNEL); `THEOREM_LIST_FINAL.md:433` (S-T (cited)) |

**[charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]**

## Wave and reason (MINUTES §2.5, verbatim)

**Source:** `theory_campaign/MEET-THM/MINUTES.md:107` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:107-107 -->
| 1 | **M1** V/H; **M3** START; **LP-FOUND** = S-TARGET + S-BLOCKS + S-KERNEL (+ S-T cited) | Foundations. N1 (binding §13.1) is the longest pole and starts first (B, D) |
<!-- END VERBATIM -->

## Dependencies (from the seats' §S3(a) edge lists)

X → Y means Y uses X.

**A §S3(a)** (`theory_campaign/MEET-THM/R3_A.md:166–172`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_A.md:168` — Foundations: S-TARGET → M1
- `R3_A.md:168` — S-TARGET → M3
- `R3_A.md:168` — S-TARGET → M4 (N17)
- `R3_A.md:168` — S-TARGET → M2 (Lemma 0)
- `R3_A.md:168` — S-TARGET → M7
- `R3_A.md:168` — S-KERNEL (N9) → M1(a)
- `R3_A.md:168` — S-KERNEL (K103) → S-IDENT
- `R3_A.md:168` — S-BLOCKS (PART-ThmA, SIZE) → M3
- `R3_A.md:168` — S-BLOCKS → M5 (lemma)
- `R3_A.md:168` — S-BLOCKS → M2 (IC3 partition).
- `R3_A.md:172` — Output and selection: S-T (T03♯) → M1(i), M4 (masked statement), M5(0),(2), M6

**B §S3(a)** (`theory_campaign/MEET-THM/R3_B.md:222–237`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_B.md:229` — PART-ThmA → M3, M5, S-BLOCKS
- `R3_B.md:232` — T03♯ (S-T) → M2 (c1), M5, M4 (f), M1 (f), S-LEAK
- `R3_B.md:233` — S-KERNEL (minorisation) → M2 (b4), S-IDENT
- `R3_B.md:236` — S-TARGET → M4 (d), M3 (envelopes)

**C §S3 (edge list)** (`theory_campaign/MEET-THM/R3_C.md:254–281`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_C.md:256` — S-TARGET → L-N9
- `R3_C.md:256` — S-BLOCKS → L-N9
- `R3_C.md:256` — L-N9 → S-KERNEL
- `R3_C.md:258` — S-TARGET → S-T
- `R3_C.md:259` — S-TARGET → L-DIL
- `R3_C.md:260` — S-BLOCKS → L-LH
- `R3_C.md:260` — S-T → M3(f)
- `R3_C.md:262` — S-KERNEL → L-TIE
- `R3_C.md:263` — S-T → M5
- `R3_C.md:267` — S-TARGET → L-ESS
- `R3_C.md:270` — S-T → M6
- `R3_C.md:272` — S-BLOCKS → M8
- `R3_C.md:274` — S-TARGET → M4
- `R3_C.md:275` — S-T → M4(masked)
- `R3_C.md:278` — S-KERNEL → S-IDENT

**D §S3(a)** (`theory_campaign/MEET-THM/R3_D.md:183–205`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_D.md:183` — Barbieri–Berger 2004 → M5, S-TARGET
- `R3_D.md:186` — S-KERNEL(N9) → M1
- `R3_D.md:186` — S-KERNEL → M3
- `R3_D.md:186` — S-KERNEL → S-REP
- `R3_D.md:187` — S-TARGET(K01–K05,N17,K95) → M4
- `R3_D.md:187` — S-TARGET → M3
- `R3_D.md:187` — S-TARGET → S-Z
- `R3_D.md:187` — S-TARGET → S-REP
- `R3_D.md:188` — S-BLOCKS(K07,K06) → M3
- `R3_D.md:188` — S-BLOCKS → M5
- `R3_D.md:188` — S-BLOCKS → M2(IC3)
- `R3_D.md:191` — S-T(K93) → M5
- `R3_D.md:191` — S-T → M4
- `R3_D.md:191` — S-T → M1(d′)
- `R3_D.md:191` — S-T → M6
- `R3_D.md:191` — S-T → M3

## Binding goal and escalation safeguard (MINUTES §2.3)

No binding theorem of its own, but §5.1 "exact correction" rests on S-KERNEL (amended CHK N9) with M1(a): R3_C §S4: "Failure of foundational correction escalates." (`theory_campaign/MEET-THM/R3_C.md:335`).

**Source:** `theory_campaign/MEET-THM/R3_C.md:335` (verbatim)

<!-- BEGIN VERBATIM R3_C.md:335-335 -->
| §5.1 exact correction | M1; S-TARGET; S-KERNEL; amended CHK N9. Numerical fidelity remains N16. Failure of foundational correction escalates. |
<!-- END VERBATIM -->

## Named implementation premises / audit obligations (MINUTES §2.3)

The N3 tie-DP invariant (registry OPEN; S-KERNEL K09 = proposition C10, PROOF SKETCH, unchecked; carried as hypothesis in M5/M4(f)); N9 with the CHK amendments (`evidence/CHK_INHERITED/REPORT.md` §5); N16 numerical fidelity stays FUTURE_WORK. K23: optional attributed lemma without theorem number (MINUTES R3-4, C's dissent).

General rule (MINUTES §2.3, verbatim):

**Source:** `theory_campaign/MEET-THM/MINUTES.md:87` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:87-87 -->
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM -->

## Charter [charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]

| Item | Text |
|---|---|
| Goal | Prove/close the listed supplement statements: S-TARGET + S-BLOCKS + S-KERNEL (S-T cited, no HQ work). |
| Statement | The cards in `THEOREM_LIST_FINAL.md` Part II named above (K-IDs: S-TARGET: K01–K05, K76, K95; S-BLOCKS: K07, K14, K06; S-KERNEL: K20, K21, K08, K09, K22, K103 (S-T: K93, K04, cited)). Statements are as filed by the seats; seat variants and the chair's editorial choices ("Chair's choices") are in that file. |
| First lemma | (none specified by the seats for the pack; each card's route is in its seat card) |
| Fallback | Each card's own fallback (verbatim below where a seat card states one). **Chair's generic rule (IC7), for every card in this pack:** the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded. |
| Stop rule | Each card's own stop rule (below where stated); otherwise one proof attempt plus one cross-family check-and-repair cycle per card, then the generic rule above. |
| Escalation | As in the Binding goal / safeguard section above; otherwise none. |

## Cards' own fallback / stop rows (verbatim, where a seat card states them)

Card `C12 — K01`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:201` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:201-201 -->
| Fallback / stop | Proper target and exact-arithmetic enumeration; no machine-certification claim. |
<!-- END VERBATIM -->

Card `C11 — K07`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:190` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:190-190 -->
| Fallback / stop | Group preservation and deterministic counts only; no size-five pairing law. |
<!-- END VERBATIM -->

Card `C10 — K09`:

**Source:** `theory_campaign/MEET-THM/R2_C.md:174` (verbatim)

<!-- BEGIN VERBATIM R2_C.md:174-174 -->
| Fallback / stop | Unique-maximizer instances. If the prefix invariant fails, drop the tie proposition and retain the integration gap. |
<!-- END VERBATIM -->

