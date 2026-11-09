# LC2 disposition (new-lemma check, Codex gpt-6.1-sol high) — 2026-11-09

Verdict: VERIFIED WITH AMENDMENTS. C's telescoping bound, TR's kernel/path arguments, LT Step 2′, D's MAP transfer verified;
reviewer's own exact checks on 12 targets (all orders up to 720, all N_e = 1 bridge paths) found no bound violation.

| # | Sev. | Issue | Disposition |
|---|---|---|---|
| 1 | MAJOR | P-OVL∞ forces P(𝒜) → 1 | Already fixed after MP1 issue 1 (same finding, independent): Q := L/M on 𝒜, ∞ off 𝒜. |
| 2 | MINOR | "= β/2" and "= g" where only ≤ holds (C Step 5, LT Step 2′) | ACCEPTED: changed to ≤ (reviewer's explicit example: E(1−W)⁺ = 0.0905 < β/2 = 0.0952). Constants unchanged. |
| 3 | MINOR | LT-e′ MPM tie at ½ | Fixed after MP1 issue 3 (u = ¼); in addition LT-b′ is now stated for the non-strict tail P(E_r ≥ u). |
| 4 | MINOR | e_0 convention at M = 1, L = 0 | ACCEPTED: e_0 := 1 (STATEMENT TR, TR file). |
| 5 | MINOR | 1_𝒜δ̄ → 0 is localised concentration, not global P-CONC | ACCEPTED: C-v and C Step 6 say "⇔ 1_𝒜o₁ → 0 and P-START; implied by P-CONC + P-START". |
