# INDEX — consolidated proof of the W1-PXN theorem (Theorem PXN)

One self-contained proof document, in the order of the definitive map of the ticket (§0 conventions → §7 A-dependence), with the 22 errata applied in place, the replacement lemma
files substituted for the superseded steps, and no cross-references to the old candidate proof. External results (T22, T03♯, W7 Theorems A/B, the operational premises, Lemma RO, W3-PXN)
are cited with their statements and statuses (00 §0.7), not re-proved.

## Files

| File | Content |
|---|---|
| 00_statement_and_conventions.md | setting LH-iid, notation, target and method, the theorem (R)(S)(E)(T)(P)(C)(K), conventions (exact branch, onset), Lemma T, external results |
| 01_tools.md | [LM]; Lemma CR and [CONC′]; Lemma Tr-J; Lemma E with the events 𝒟_start, 𝒟_search |
| 02_design_events.md | Lemma K (m♯_n ≤ k_n, L_n); event ℰ♯_n; Theorem R ((R-a), (R-b), (R-c), Lemma R0); route (R′) |
| 03_start.md | Lemma B; P3′ (start mass); P4 (masking); P5 (eligibility). (S), (E) |
| 04_search.md | Lemma Λ; Lemma U; (D_S); (L); Lemma LS; Theorem P6′. (T), (K) |
| 05_posterior_output.md | T03♯ input; de-randomisation; P8♯ (P); output composition (C); assembly of the theorem |
| 06_A_dependence_and_scope.md | A-dependence; obstructions (O1)–(O5); scope; note on the excluded Lean-readiness assessment |
| MAP.md | correspondence table (old lines/lemma files ↔ new sections), may contain old-file references |
| APPLIED_ERRATA.md | where each of E-1..E-22 was applied, other corrections, dropped passages, notation changes |
| OPEN_QUESTIONS.md | ambiguities and judgement calls for the lead |
| selfcheck.txt | grep output for forbidden cross-references |

## Dependency of the sections

00 → 01 → 02 → 03 → 04 → 05 → 06. In particular: Lemma T (00) and Lemma E (01) feed 03 and 04; ℰ♯_n (02) is the working event of Lemma E and of 05; Theorem R (02) feeds Lemma T-transfers in 03–04;
Lemma Λ, Lemma U, (D_S), (L), Lemma LS (04) give (T); P8♯ (05) gives (P); Theorem 6.3 (05) composes everything.

## Review record of the components (copied from the ticket's definitive map; not part of the proofs)

Lemma CR/[CONC′]: XF VERIFIED (R19). Lemma Tr-J: XF VERIFIED (R11). Lemma E: XF VERIFIED (R12). ℰ♯_n and Lemma K: XF VERIFIED (R19). Theorem R: XF VERIFIED (R14, after the display split; repairs re-checked R21).
Lemma B: XF VERIFIED (R13) for (i), (i′), (iii); (ii) restricted and unused (repair VERIFIED R21). P3′, P4: XF VERIFIED (R16). P5: XF VERIFIED (R15). Lemma Λ: XF VERIFIED (R13, incl. the Haar-span step).
Lemma U, (D_S), (L): XF VERIFIED (R17; arithmetic R19). Lemma LS, P6′: XF VERIFIED (R15 for (ii), (iii); repaired (i) R21). P8♯: XF VERIFIED (R19). (C): VERIFIED under (OP) (R15; exact-branch cases R21).
Council round 1 of the ticket: all gates PASS (8.6 / 8.3), with the request that a single consolidated text be produced — this document. The consolidation subsequently received the R36 fidelity review recorded below; that review is distinct from the baseline theorem's council pass and does not constitute a council pass of C-PACK's new addenda.

## Notation changes with respect to the sources (details in APPLIED_ERRATA.md §D)

masked set 𝓜 (constant M unchanged); Theorem R uses q_R; score margin mar_n(c′); Mills threshold u_n; thresholds t_{n,D}, τ_{n,D}; b_min; ℰ♯_n, 𝒟_start, 𝒟_search; T03♯; [CONC′].
The letter A keeps both its meanings (exponent; generic subset), as in the sources (00 §0.2).

## Status and addenda (lead, 2026-11-08)
Fidelity check: R36 (`../reviews/R36_item5_fidelity_sol.md`, Codex gpt-6.1-sol xhigh): FAITHFUL-WITH-FIXES (0/0/4/2), all six
fixes applied in place. This supplement transcribes the council-passed W1-PXN result (status "PROVED-CHECKED", Wave 1,
not adopted by HQ) and nothing newer. **Separate addenda, not incorporated here** (their own review status): C-PACK item 1
(`../lemmas/I1_e4_replacement.md`: Lemma UM replaces "N3 bypassed" in §3.4; §1.1 replaces the off-event centre clause of
Lemma T(i) for the coded routine) and C-PACK item 2 (not used by PXN).
