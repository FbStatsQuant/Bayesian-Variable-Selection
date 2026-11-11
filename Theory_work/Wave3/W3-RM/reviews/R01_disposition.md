# R01 disposition (statement lock, Codex gpt-6.1-sol high: LOCK-WITH-CHANGES)

Reviewer reply verbatim: `reviews/R01_statement_lock_sol.md`. All required changes applied in STATEMENT v1.1 (markers [R01-#]).

| # | required change | disposition |
|---|---|---|
| 1 | E4 encoding contract must include the inverse maps `st.blk`/`st.pos`, valid `D.p`, caps | applied: (C3) rewritten; nothing claimed on rejected inputs |
| 2 | LS0 options part of the integration statement; quantifiers over admissible runs; EX-A is an idealisation | applied: §1 "Configuration", (C3), §6; the E4 audit covers option parsing and gates |
| 3 | move-count bound only on Sand ∩ NA ∩ TL | applied: (C1) |
| 4 | complete bridge contracts; split NA-R / TL-R; drop "exactly one bridge" | applied: bridge table (B4), (B5), (B8a), (B8b), input map, §2 sentence |
| 5 | no "exact threshold" claim for η_A; "15" wording; converse-or-open step | applied: (C5) rewritten; SHARPNESS.md records proved / observed / open separately |

Optional suggestions: LSF cutoffs copied into (T1-R) (applied); a non-metric (L-R) example for the abstraction diagnostics
(taken up in the lemma-check numerics for SAND-R); κ enlargement in (B10) (applied); E4 pointer (applied).

Reviewer confirmations recorded (no change needed): (B1) quantifiers pass; (B2) every use of |Q| in GROW L3 listed and
log|Q| = o(log n) suffices; (B3) BM-Q is the right floor; (B5) the maximal-Z proof passes with the stated rate and the
(N-loc) bound holds without a factor 2; the Form R inventory matches UNI L2_k0 §4–§6 (key proof detail: response-scale
uniformity); (C0)(b) passes without CAL; the E4 code logic passes given change 1.
