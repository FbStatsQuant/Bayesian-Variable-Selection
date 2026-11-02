# W2-BOOK working notes (not reviewed)

Run started 2026-11-02 on branch theory/W2-BOOK. Status words per PROTOCOL.md.

## Sources read
- PROTOCOL.md, tasks/W2-BOOK.md, Docs/THEORY_PRIORITIES.md, 00_COMMON.md, LOCKED_PROOFS.md.
- T12 STATEMENT.md and PROOF_v6 body in COLLECTED_PROOFS_v2.tex (lines 1119-1503).
- METHODOLOGY_v3 §§2, 6.1, 6.8-6.12, 8.6; MASTER Part I §I.1 (in-run time guard, N6), §I.6 (statuses), D2 (secondary PIP removed).
- W1-T24G REPORT.md (Theorem B, route (e')), from origin/theory/W1-T24G.

## Key fact found early
The deployed method's `resource_limit` is NOT only a preflight prediction. MASTER §I.1 (lead ruling N6) adds an
in-run wall-time guard checked after every bridge stage of each final island and after each local search.
So the output-available event depends on final-run randomness (and on hardware timing), and is not
sigma(C)-measurable. Conditioning on it is not covered by T12(iv.d) (launch events) and can break the identities.
