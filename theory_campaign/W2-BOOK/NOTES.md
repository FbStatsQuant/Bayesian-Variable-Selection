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

## Engine facts (read from Scripts/SMC_BVS/core/cpp, 2026-11-02)
- v3_runtime.h: RuntimeGuard::check reads std::chrono::steady_clock only; consumes no random number; sets `exceeded`.
- v3_engine.h ~l.335: guard checked after every bridge stage of an island (final run included); on fire the island returns `partial`.
- v3_core.cpp cpp_final_run: islands r = 1..4 run sequentially, stream seed_stream(seed, 9 + r); if an island is partial -> status
  resource_limit, later islands not run. After the 4 islands, final local search, then ONE MORE guard check: if it fires, status
  resource_limit although every final quantity was computed.
- Burn-in and measured rounds have no guard check.
- So: the output-available event is a function of (potential-run record, clock). Stop-only coupling (GUARD) holds by reading of code.

## scripts/frozen_run_exact.py (exact, 50 digits; results/frozen_run_exact.log)
- Independent re-implementation reproduces T12(iv.b): D = 8.14676240634, a = 0.0279141173179, c0, c1, PIP1 = 0.990618012243,
  E[Pbar_1] - PIP_1 = -0.173974177850 (all digits shown agree with the locked table).
- Identities E Zhat = Z, E[Zhat PIPhat] = Z PIP: residual ~1e-50.
- Pooled x pooled: E[Zhat Pbar_1]/(Z PIP_1) - 1 = -0.13172; equals the closed form Z PIP + (3/4) Z (E Pbar - PIP) to 1e-49.
- Pooled island product (1/4) sum_r Zhat_r PIPhat_r1: unbiased to 1e-49.
- Stylised guard (score cost 1 + k^3, check after stage-1 bridge stage): h = 33 gives P(O) = 0.99783, E[Zhat|O]/Z = 0.9739;
  h = 32 gives P(O) = 0.99067, E[Zhat|O]/Z = 0.798; h <= 30 gives ~0.011. COUNTEREXAMPLE to "unbiased given output".
