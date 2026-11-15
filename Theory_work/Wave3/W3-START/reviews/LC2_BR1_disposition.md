# LC2 / BR1 disposition (lead, 2026-11-11) — line checks of L6–L8, L10–L11 and the break review of L9

Manifest `053bc169c5da3c032943e217e7bd5ddb76d4268ba821b09579be126d9961a155` quoted by all three reviewers; `manifest.py bind` OK.
Blind first reads (briefs `BRIEF_LC2_A_sol.md`, `BRIEF_LC2_B_sol.md`, `BRIEF_BR1_astra.md`).

| seat | object | verdict | file |
|---|---|---|---|
| LC2-A, Codex gpt-6.1-sol high | L6 (F1–F4, L6.0) | VERIFIED | `LC2_A_line_check.md` |
| LC2-A | L7 ((C2), (T4)) | VERIFIED | `LC2_A_line_check.md` |
| LC2-A | L8 ((T3)(a)) | VERIFIED-WITH-AMENDMENTS (1 MINOR; 1 MINOR on a script comment) | `LC2_A_line_check.md` |
| LC2-B, Codex gpt-6.1-sol high | L10 (IF-START, OVL, MIS) | VERIFIED | `LC2_B_line_check.md` |
| LC2-B | L11 (examples) | VERIFIED-WITH-AMENDMENTS (1 MINOR) | `LC2_B_line_check.md` |
| BR1, Codex gpt-6-astra high | L9 ((B-R), (T3)(b)) | **NOT VERIFIED against the literal locked target** (2 CRITICAL, 1 MINOR); "the main Gaussian-row argument survives this review"; "narrowing the substantive (T3)(b) rate is not warranted" | `BR1_break_review_astra.md` |

## BR1 — reading against the kill budget of (B-R)
The kill budget was one Fable attempt and one Astra break review, with (T3)(b) narrowed on failure. The break review
found **no flaw in the probabilistic argument** (covariance event, localisation, conditional law, Markov step, the use
of the uniform fixed-design bound): each section is re-derived in its "Checks performed". Its NOT VERIFIED verdict
rests on a mismatch between the bridge row and its hypotheses, which has no local repair inside the lemma file:
the row said the design satisfies (E), and (E) contains "p > s₀ for all large n", which the population conditions do
not imply. The attempt therefore **survives with a statement amendment**; the rate of (T3)(b) is not narrowed.

| # | class | finding | action |
|---|---|---|---|
| BR1-1 | CRITICAL (scope) | (B-R) claimed all of (E), including p > s₀, from hypotheses that allow p = s₀ | **statement amended (v1.3.2).** `STATEMENT.md` §6 already says "Not claimed: … any asymptotic claim when p = s₀", so the consistent repair is the reviewer's second alternative: (B-R) and (T3)(b) now state the hypothesis "Setting R with p > s₀ for all large n"; the bridge row says which parts of (E) are proved (the energy bound) and which are assumed. L9.2, L9.6 (summary) and L9.7 changed accordingly; the earlier remark extending (T3)(b) to p = s₀ is removed (not claimed). Examples G-1, G-2 carry p > s₀. This makes explicit an exclusion the locked statement already had; it is reported to HQ as a statement change |
| BR1-2 | MINOR | the constant c_d was printed with an ambiguous denominator | applied: c_d := √15·s₀θ_hi/√(Δ_lo·c_Σ/2) |
| BR1-3 | CRITICAL (false remark, not used in any inequality) | "the summands of Ψ_n have no finite variance" is false at finite n (they are bounded) | applied verbatim: the remark now says that the first-moment estimate and Markov's inequality give tightness and that no concentration across columns is supplied; `RESULTS_LEMMAS.md` corrected the same way |
| A-1 | MINOR | L8.3 proved the O_P/o_P form only for κ > 0 | applied: "First take 0 < κ < κ_V" and the sentence for κ ≤ 0 |
| A-2 | MINOR | script comments said both (C2) chains were asserted | applied: comments and `RESULTS_LEMMAS.md` now say that only the leaking-null chain is asserted |
| B-1 | MINOR | example F-1 did not assume p > s₀ | applied |

The statement change (v1.3.2: one bridge row and one hypothesis line) and all amended lemma files are read afresh by
the exhaustive sweep (next round, new manifest), whose brief asks for the bridge row to be checked against L9.
