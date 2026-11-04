# HQ charter · LP-REST · consequences lemma pack

| Field | Value |
|---|---|
| HQ | LP-REST · consequences lemma pack |
| Wave (MINUTES §2.5) | 4 |
| Covers | S-Z + S-POOL + S-LIM |
| K-IDs | S-Z: K37–K41, K53; S-POOL: K49, K50, K54, K56, K57-P1; S-LIM: K79, K81, K100, K101 (K99 qualitative remark) |
| Final card(s) | `THEOREM_LIST_FINAL.md` Part II: `THEOREM_LIST_FINAL.md:1009` (S-Z); `THEOREM_LIST_FINAL.md:1047` (S-POOL); `THEOREM_LIST_FINAL.md:1100` (S-LIM) |

**[charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]**

## Wave and reason (MINUTES §2.5, verbatim)

**Source:** `theory_campaign/MEET-THM/MINUTES.md:110` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:110-110 -->
| 4 | **LP-REST** = S-Z + S-POOL + S-LIM; **LP-REP** = S-REP + S-LEAK | Consequences and reporting corollaries. Nothing binding waits on them |
<!-- END VERBATIM -->

## Dependencies (from the seats' §S3(a) edge lists)

X → Y means Y uses X.

**A §S3(a)** (`theory_campaign/MEET-THM/R3_A.md:166–172`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_A.md:170` — M1 → S-POOL
- `R3_A.md:170` — M3 → S-Z
- `R3_A.md:170` — M2(a) → M1(i), S-REP, S-Z (D bound)

**B §S3(a)** (`theory_campaign/MEET-THM/R3_B.md:222–237`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_B.md:228` — M1 → S-POOL
- `R3_B.md:233` — M2 (a) → S-Z (D)
- `R3_B.md:236` — M4 → S-LIM (cited)
- `R3_B.md:236` — M1, M3 → S-POOL, S-Z

**C §S3 (edge list)** (`theory_campaign/MEET-THM/R3_C.md:254–281`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_C.md:276` — L-FK → S-Z
- `R3_C.md:276` — OPW2 → S-Z
- `R3_C.md:276` — M2 → S-Z(range corollary)
- `R3_C.md:277` — M1 → S-POOL
- `R3_C.md:277` — cited SLLN/ratio lemmas → S-POOL
- `R3_C.md:280` — Filed counterexamples → S-LIM

**D §S3(a)** (`theory_campaign/MEET-THM/R3_D.md:183–205`), fragments naming this HQ's cards (verbatim; each edge is split out at ";" or at a sentence end):

- `R3_D.md:187` — S-TARGET → S-Z
- `R3_D.md:197` — M2(a) → S-Z
- `R3_D.md:198` — M1 → S-POOL
- `R3_D.md:200` — M4 → S-Z(envelope)
- `R3_D.md:202` — S-POOL(K47 cited,K49,K50) → M1(b)
- `R3_D.md:203` — S-LIM → (discussion only)

## Binding goal and escalation safeguard (MINUTES §2.3)

None. MINUTES §2.5, wave 4: "Nothing binding waits on them."

## Named implementation premises / audit obligations (MINUTES §2.3)

None named in the cards. S-Z variance clause: both bounds ship ((vii-a) the 1/N form, (vii-b) the pathwise form); see `THEOREM_LIST_FINAL.md` "Chair's choices" item 3.

General rule (MINUTES §2.3, verbatim):

**Source:** `theory_campaign/MEET-THM/MINUTES.md:87` (verbatim)

<!-- BEGIN VERBATIM MINUTES.md:87-87 -->
| Audit obligations | N2(b), N2(c), N2(e), N14(c), the N3 DP invariant, and the integrated streams/LS0/GUARD-W/execution-DAG audits are **named implementation premises in the charters** and are recorded in `REGISTRY_PAPER1.md` (B's "missing" item 2, adopted) | — |
<!-- END VERBATIM -->

## Charter [charter drafted by clerk from cards; confirmed by the chair 2026-11-04, with the generic IC7 rule in the Fallback row]

| Item | Text |
|---|---|
| Goal | Prove/close the listed supplement statements: S-Z + S-POOL + S-LIM. |
| Statement | The cards in `THEOREM_LIST_FINAL.md` Part II named above (K-IDs: S-Z: K37–K41, K53; S-POOL: K49, K50, K54, K56, K57-P1; S-LIM: K79, K81, K100, K101 (K99 qualitative remark)). Statements are as filed by the seats; seat variants and the chair's editorial choices are in that file. |
| First lemma | (none specified by the seats for the pack; each card's route is in its seat card) |
| Fallback | Each card's own fallback (verbatim below where a seat card states one). **Chair's generic rule (IC7), for every card in this pack:** the card ships in the narrowest form its filed checks support. A clause whose proof or cross-family check fails after one repair cycle moves to `FUTURE_WORK.md` with the reason. It is never relabelled as a limitation, and no status is upgraded. |
| Stop rule | Each card's own stop rule (below where stated); otherwise one proof attempt plus one cross-family check-and-repair cycle per card, then the generic rule above. |
| Escalation | As in the Binding goal / safeguard section above; otherwise none. |

## Cards' own fallback / stop rows (verbatim, where a seat card states them)

The seat cards state no fallback/stop row for these supplement cards. The chair supplies them (IC7):

| Card | Fallback (ships if the full card fails) | Stop rule |
|---|---|---|
| S-Z | The exact evidence identities (KNOWN—CITE); clause (vii-b), Var(W_r \| 𝒞) ≤ e^{2·osc d} − 1, from the pathwise bound checked by PC2; the terminal-off clause in exception-probability form. Clause (vii-a), the 1/N form, is dropped if its route fails | Generic rule |
| S-POOL | Prop P(i),(ii) (MA-PropP, "PROVED (elementary)", author-only: checked in the HQ); the recording-marginal P1 comparison as checked (W2_PC1 B.S10); R_eff as the Kish identity (cited) | Generic rule; general K57 accuracy stays FW |
| S-LIM | Each limitation restated with its filed construction: E1c/V12 for K79; duplicates with PIP = E[# selected in group]/d, and numeric limits only with their p qualification | Generic rule; a limitation whose proof fails moves to FW. It is never kept as an assertion |
