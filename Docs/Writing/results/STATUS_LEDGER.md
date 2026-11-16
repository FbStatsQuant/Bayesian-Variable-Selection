# D2 status ledger (Writing Department, 2026-11-16; registry = `Theory_work/INFRA/registry/claims.tsv` on main f8a6c2da)

Internal. Each D2 result: the master claim(s) and the registry status **verbatim** (column `status`, all `state` = ACTIVE),
then the plain-words label used in D2's status note. Where the card (CLAIMS_CARD v1.6) quotes an older string, the
registry wins (WD2). Reader-form bridges: W3-READER has not passed its CP3 (stand-down 08:09, LOG), so every NEW bridge
of READER_VERSIONS is "not yet independently checked".

Plain-label vocabulary (assignment): "proved and independently checked" · "proved and checked, conditional on …" ·
"in progress". Supplement used where needed: "proved, not yet independently checked" (never called a theorem).

| Result (reader numbering) | card row | master(s) @version: status verbatim | D2 plain label |
|---|---|---|---|
| Theorem 1, in-probability form (HPM/MPM/PIPs) | 1.1 | `SOP:TH09@1.0.2`: "PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea4…, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C VERIFIED). Not upgraded …: T02(i♯) and T02(ii♯) PROVED, SF/XF VERIFIED; T01–T03 PROVED-LOCKED …" · the card's alias `W3-POST:Thm-1@1.0.0` still reads "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" **[FLAG H1]** | proved and independently verified (two independent verification passes) — HQ ruling H1, 2026-11-16 |
| Theorem 1, expectation display | 1.1 | `W3-POST2:C@1.0.5`: "PROVED-CHECKED, conditional on W3-POST:Prop-LB, [L1a′], W2-APP:POST, W3-POST:Thm-1"; `W3-POST:Prop-LB@1.0.0`: "PROVED (by this seat, unchecked)"; [L1a′] = `W3-POST/lemmas/L1a_size_tail.md`, no registry row (unchecked per READER_VERSIONS); `W2-APP:POST@1.0.7`: "PROVED-CHECKED" | proved and checked, conditional on two supporting lemmas (a size-tail lemma and a lower bound on the posterior miss) that are proved but not yet independently checked |
| Theorem 1′ | 1.1 | `W3-POST2:E@1.0.5`: "PROVED-CHECKED, conditional on W2-APP:POST, W3-POST:Thm-1"; `W3-POST2:A0@1.0.5`: "PROVED-CHECKED"; uses C case (iii) → inherits C's conditions | proved and checked, conditional on the same two supporting lemmas as the expectation display |
| Remark (o) determinant growth | 1.1 | `W3-POST2:A1@1.0.5`: "PROVED-CHECKED, conditional on W3-POST:Thm-1, W2-APP:POST" | (remark) proved and checked |
| Theorem 2 | 1.2 | `W3-POST:Thm-1` item 6 (status as row 1 / FLAG H1) + `W2-APP:POST@1.0.7`: "PROVED-CHECKED"; reader bridge B2.1 NEW | proved and independently checked; reader-form bridge (set-size arithmetic) awaits its final check |
| Theorem 3 | 1.3 | `W3-PSHARP:A@1.0.0`, `W3-PSHARP:B@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …"; `W3-PSHARP-R:AE@1.0.0`, `W3-PSHARP-R:A2C@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST fdfd4562…, sol=9.5 PASS, opus=9.2 PASS"; exactness case B3.8 Sol-checked, upper half carries Thm 3.1's status | proved and independently checked |
| Theorem 4 | 1.4 | `W3-MISR-R:CorGb-plus@1.0.1`: "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS"; `C-MIS:Prop-P@1.0.0`: "R02 VERIFIED; R04 wording fixes checked in R05; council PASS"; `C-MIS:GD(b)@1.0.0`: "R02 VERIFIED-WITH-AMENDMENTS (applied); council PASS"; Example `W3-MISR-R:CorG-min@1.0.1`: "PROVED-CHECKED; council R3, …"; remark `W3-MISR-R:CorH-plus@1.0.1`: "PROVED-CHECKED, conditional on W3-POST2:D; …", `W3-MISR-R:CorH-U@1.0.1`: "PROVED-CHECKED, conditional on W3-POST2:D, W3-POST2:C, W3-POST2:A0, C-MIS:Prop-P; clause (G) also conditional on W3-POST2:E, W3-POST2:A1, C-MIS:GDb; …"; headline masters `W3-MISR:MIS(i)@1.0.1`: "PROVED-CHECKED, conditional on W3-POST2:C; …", MIS(i′), MIS(ii) "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1; …" | proved and checked, conditional on the expectation form of Thm 3.1 (hence on its two supporting lemmas) and on two Gaussian-design lemmas that are verified and council-passed |
| Theorem 9, (i)–(iii) | 2.1 | `W3-DIST:Thm-A@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS" | proved and independently checked |
| Theorem 9B | 2.1 | `W3-DIST:Thm-B@1.0.0`: "PROVED-CHECKED, conditional on W3-POST:Thm-1; council R2, …" | proved and checked, conditional on Thm 3.1 (in-probability form), itself proved and checked (FLAG H1) |
| Corollary 9C | 2.1 | `W3-DIST:Cor-C@1.0.0`: "PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, …" | proved and checked, under exact arithmetic |
| Fixed-design remark (row 2.2) | 2.2 | `W3-POST2:D@1.1.5`: "PROVED-CHECKED, conditional on W2-APP:POST, W3-POST:Thm-1" | proved and checked (inputs checked) |
| Theorem 5 | 3.3 | `W3-START2-R:START-R@1.0.0`, `W3-START2-R:BR@1.0.0`: "PROVED-CHECKED; council R2, MANIFEST 12bb52cd… (= R2 90886d06 re-frozen CITATION-ONLY as R2r), sol=9.0 PASS, opus=9.3 PASS"; `W3-START:FLOOR@1.0.0`: "PROVED-CHECKED" | proved and independently checked |
| Theorem 6, main | 3.1 | `W3-RM2:RM2-R@1.0.3`: "PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab8…, astra=9.5 PASS, opus=8.8 PASS; …"; `W3-RM:RM-0@1.0.0`: "PROVED-CHECKED"; `W3-RM:E4@1.0.0`: "PROVED-CHECKED"; delivery `W2-UNI:F-UNI@2.1.0`: "PROVED-CHECKED"; reader bridges B6.3, B6.6 NEW; pending RM2-R swap **[FLAG H2]** | proved and checked (its one condition, the posterior transfer lemma, is itself proved and checked); reader-form bridges await their final check |
| Theorem 7 | 3.2 | `W3-RM2:RM2-F@1.0.3`: "PROVED-CHECKED; council R1, MANIFEST 00bbeab8…, astra=9.5 PASS, opus=8.8 PASS; …"; RM-0, F-UNI as above; B7.4 NEW; pending RM2-R swap [FLAG H2] | proved and independently checked; reader-form delivery bridge awaits its final check |
| Theorem 8 | 3.7 | `W3-SCR:A1@1.0.0`: "PROVED-CHECKED" | proved and independently checked |
| Theorem 8′ | 3.7 | `W3-SCR:A-inf@1.0.0`: "PROVED-CHECKED"; `W3-SCR:SCR-A@1.0.0`: "PROVED-CHECKED" | proved and independently checked |
| Theorem 10 | 3.6 | `W3-SAMP:C@1.1.4`: "PROVED-CHECKED"; start input `W3-START2-R:IF-START@1.0.0` (repin of `W3-START2:IF-START`, now SUPERSEDED-VALID): "PROVED-CHECKED; council R2, …"; `W2-APP:POST@1.0.7`: "PROVED-CHECKED"; reader assembly B10.3 NEW | proved and independently checked (master); reader-form assembly awaits its final check |
| Remark (row 3.5) per island | 3.5 | `W1-N1:Thm-N1@1.0.0`: "PROVED-CHECKED" | proved and independently checked |
| Remark (row 3.5 / 4.1) pooled $\hat Z$ | 3.5, 4.1 | `W3-READER:PoolZ`: **no registry row on main** (card: "PROVED (by this seat, unchecked)") **[FLAG H3]** | proved (two-line argument), not yet independently checked |
| Pooled PIP error ≤ worst island | 4.1 | `W3-SAMP:LT#@2.0.4`: "PROVED-CHECKED" | proved and independently checked |
| Output-identical parallel engine | 4.2 | no registry row; engineering fact + note in progress | in progress (empirical; no theorem) |
| Many islands / island weighting at 10⁶ | 4.3 | no registry row; "OPEN" | open |

## Flags for HQ — answered 2026-11-16 (HQ, for Theory)
- **H1.** Label Theorem 1 (in-probability form) "proved and independently verified (two independent verification passes)", with a plain-words note on the two passes; never "council". Applied to Theorem 1, and to its dependants' notes (Theorem 2, Theorem 9B, row 2.2).
- **H2.** "Revision pending" for rows 3.1/3.2 until the RM2 follow-up is recorded after the resume. Applied.
- **H3.** Pooled evidence: "not yet independently checked". Applied.
- **H4.** Prop-LB is not logged as implied by PSHARP:B (an unchecked, post-freeze item). The expectation form of Theorem 1, Theorem 1′ and Theorem 4 stay conditional on the lower-bound proposition and lemma [L1a′], not yet independently checked. Applied.
- Constants: $c_1$ copied from `W3-POST2/STATEMENT.md:130` ($C_A$ at :22); $c_0$ from `W3-POST/STATEMENT.md:75`, with the proof constant $C_*$ left as a placeholder for Theory.
- Song–Liang lines: rewritten as full sentences with the same claims (HQ permission). The Codex read checks each one against the card line and the PDF.
