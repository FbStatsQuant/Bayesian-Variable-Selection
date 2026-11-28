# STYLE_A3_R1: advisor note on the outline of "What we prove", v2 (2026-11-16)

Read: `results_v2/OUTLINE.md` against the ledger, the Theory notes (ANSWERS, AG, IDEALW, ROW36, AUDIT item 1), v1.

## (a) Order and structure

Core first, and it answers fast: §1 with Table 1 is right. Five things are misplaced.
1. **Result 5 belongs inside §3.** Its lower bound and the moderate-$n$ heuristic are the same quantity,
   $(s_0+1)\sqrt{\log p/(\pi n)}$. One remark after Result 1 can give the proved bound (witness designs), then the
   numbers, marked as a heuristic with one-draw measurements. The two statuses must stay separate.
2. **§8 is internal and dated.** Like the status notes it should be removable: put it under the `\showstatus` toggle
   or in the status appendix, not in a numbered section.
3. **Local assumptions stay with their result.** Assumption 5.6 needs the leakage vocabulary of §5, and 4.1 needs the
   setting of §4. §2 should hold only the labels used by two or more core results.
4. **Table 1 uses labels before §2 defines them.** Use plain words in the table.
5. **§6's title promises more than it gives.** "The run's estimates are consistent" holds for two of our designs.
   ROW36 asks not to build the story on row 3.6; say "unbiased evidence on every design; consistency without leakage".

## (b) The four questions

1. **One result, two theorems.** The settings, the assumption lists and the statuses differ, and three status notes
   on one theorem are unwieldy. Share one "In words" and one "Why it matters". Gaussian rows first, as proposed.
   In the fixed-design theorem, make the verified in-probability form the statement and give the expectation bound
   as a second display with its own conditional note. HQ's earlier ruling on row 1.1 had the same split.
2. **Defined once in D2, judged in Section A.** Section A should not restate a formula. In D2, give the shared
   assumptions as one table (label, statement, used by, place in Section A). A theorem's list is then a gloss of
   each label in a few words, not a second statement, and the Section A pointers appear once, in that table.
3. **Both stay in the supplement,** but the line for Theorem 3.4 misstates it (see (c)).
4. **Yes,** as the remark of (a)1: five or six lines. It answers the first question a reader of the simulations asks.

## (c) The "why" lines

Not convincing as written; to the cut list unless reworded:
- **Rem 4.9 (row 2.2).** The line says what it is, not why it matters, and part (b) rests on a condition v2 would
  have to define. Cut, or keep part (a) as two lines under Result 2.
- **Row 4.1 (pooled error at most the worst island's).** A one-line inequality: fold it into §6.2 as a clause.
- **§6 (parallel engine, many islands).** No result. One sentence in §1 that no theorem covers it; row 4.3 is an
  open question, not a supplement item.

Misstated; keep after correction:
- **Thm 3.4,** "covers designs whose null predictors are nearly collinear". It keeps (NC), which still excludes
  near-exact dependence among $O(\log n)$ predictors, duplicated null predictors included. HQ's rule in v1 was never
  to call it design-free. What it does: a fixed floor on the true model only, and no beta-min.
- **Thm 5.12,** "sample conditions a user can check". They involve $\theta^*$, so a user cannot check them (v1 says
  so). A true line: the only reported-model statement that does not assume Gaussian rows. Per the AG note, the
  approximate-Gram condition is presented here, not in the main text.
- **Thm 4.6:** it also needs a fixed eigenvalue floor, not only a beta-min.
- **Rem 5.21:** an open premise is a weak "why". But the audit records that HQ agreed to keep it, as the only recorded
  route to the reported inclusion probabilities that does not need no-leakage. Say that, and that its premise is not
  yet derived from design conditions.

Convincing: Thm 3.18, Prop 4.3, Cor 4.7 (also the base of the planned #5′), Thm 5.2, Thm 5.16. For Thm 5.16, add that
it is the coded-method guarantee that remains for pervasive-factor designs, which Result 3 excludes.

Cut list, rescue:
- **v1 Remark 3.2(ii)** (without beta-min). Section A cites it; it must survive in the supplement.
- **The visibility example (v1 Ex. 5.5).** Keep it in the main text before the 32$s_0$ gloss; it explains the
  hardest condition in six lines.
- Thm 5.17: I agree with the cut; one sentence under Thm 5.16 is enough.

Not placed anywhere in the outline: the certification counts (v1 §5.4), the open-questions list (v1 §7), and the
appendices (constants, notation, conventions in full, ledger). The constants appendix must stay, since (BM) cites
$c_0$, and ANSWERS item 1 now gives $C_*$ explicitly.

## (d) The 12-page budget

The outline already totals 12.75. My estimate is about 15.

| Section | Outline | Likely | Why |
|---|---|---|---|
| §2 | 2.5 | 3.5–4 | v1 §2 is 6.5 pp; 13 assumptions, 5.6, three conventions, Lemma 2.1 |
| §4 | 1.5 | 2.25 | own setting (data, distance, level, window) and a five-item assumption |
| §5 | 2.5 | 3 | setup, 5.6 (14 lines), delivery clauses, domain, status, example |
| §3 | 2 | 2.25 | two statements, three status notes, two remarks |

Cuts, in order:
1. Fold §7 into §3 (−0.5), and move §8 out of the page count (−0.5).
2. §2: prior and marginal-likelihood formulas by reference to the methodology section; Lemma 2.1 stated, its proof
   to the supplement; assumptions as a table; C2 and C3 in one sentence each (−1 to −1.5).
3. §5: keep the delivery clauses in the theorem, but move the definition of the domain and the two integer limits
   to the appendix (−0.25). The IDEAL-W⁺ line then needs two lines only.
4. §4: display (i) only, as in v1; the distance in three lines (−0.5).

## (e) Against the ledger, the Theory notes and v1 (flags, not fixed)

1. **§7, "(a) holds at every finite $n$, and with it $s_0$ must be fixed".** Part (a) forces $s_0=o(\sqrt n)$ for
   concentration and $s_0=O(\sqrt{\log n})$ for the rate, not a fixed $s_0$. And "cannot be improved" is proved on
   the witness designs only; on every design the proved lower bound is of order $n^{-1/2}$.
2. **§6.1, "as a proposition".** The pooled form is "proved, not yet independently checked" with no registry row, and
   the ledger says such items are never called a theorem. A proposition for the per-island form only, or a remark.
3. **§3, status of part (a).** The outline's label omits the H1 wording. v1's note for this theorem says that its
   fixed-design input is "proved and independently verified (two independent verification passes)" and that the
   transfer is "proved and independently checked".
4. **§8, "at the freeze".** Per the notes, only the reader-form re-pin happens at the freeze. T14 is recorded after
   it, with HQ's GO; #5′ and the Prop-LB check are post-freeze; the RM2 follow-up is "after the resume".
5. **§5, "the conventions C1/C2⁺".** v1 has two delivery clauses: under C2 on the bounded domain, and under C2⁺ for
   every $n$. The IDEALW note says to keep the statement as recorded. Dropping the first clause changes it.
6. **§3, "measured 0.5–1.2×".** In ANSWERS this is the measured total relative to the weight of the true model,
   from single draws on AR(0.6), with 0.52 at $n=400$. It is not a ratio to the heuristic (that would be 1.0–1.6).
7. **§4, "v1 Thm 4.2 (Thm 9, (i)–(iii))".** In v1, Theorem 4.2 is display (i) only; (ii) and (iii) are
   Proposition 4.3. And "what NC buys": the condition there is Assumption 4.1(d), not (NC).
8. **§6.2, scope sentence.** It covers AR and block designs. On the factor designs Result 3 does not hold either;
   only 6.1 and Results 1–2 do.
9. **§3(b), "conditional on Prop-LB and [L1a′]".** Internal names; v1's plain label is "two supporting results, a
   lower-bound proposition and a size-tail lemma".
