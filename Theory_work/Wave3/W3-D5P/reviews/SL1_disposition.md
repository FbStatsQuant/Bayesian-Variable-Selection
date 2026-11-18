# SL1 — disposition (lead), 2026-11-17

| finding | decision | change (STATEMENT v1.0) |
|---|---|---|
| SL1-1 (MAJOR) exact-branch NA for `log_Z_list` in (C3)(ii) | ACCEPT | B₃(t) := {`log_Z_list` not NA and \|log_Z_list − log Z\| > 2t}; the t_n display qualified "when `log_Z_list` is not NA"; (iii) likewise |
| SL1-2 (MINOR) t = ½ endpoint and the strict median rule | ACCEPT (the reviewer's 3-model example is correct) | t, t_n ∈ (0, ½); the median/hpm failure bound uses P(ε_n ≥ ½) |
| SL1-3 (MINOR) p ≥ 2 not carried into the threshold conclusion | ACCEPT | rate clause headed "If p ≥ 2 for all large n"; the fixed-t bounds of (ii) and (iii) need only E ε_n → 0 |
| table: "C3 preamble — reader assumptions are sufficient forms, not equivalent" | ACCEPT | "implied by the reader assumptions (A1)–(A6) … through B6.1–B6.4" |
| table: "C3(ii) name the events individually" | ACCEPT | B₁–B₄ |
| table: L1 must include the TV step for PIPs; L2 must spell out cache invariance and the deterministic scan/tie rules | ACCEPT (proof obligations) | PLAN steps 1–2 |

No finding rejected. All changes are corrections of the draft before the lock (changelog row v1.0, EQUAL). LOCK.
