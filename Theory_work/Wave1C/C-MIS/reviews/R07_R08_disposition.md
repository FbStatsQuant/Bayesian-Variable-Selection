# Council round 1 disposition — PASSED (Sol 9.2, Opus 9.0; all six gates PASS for both seats, same round)

R07 (Codex gpt-6.1-sol xhigh): 9.2/10, gates 1–6 PASS; 2 minor.
R08 (Claude Opus 5.5 high): 9.0/10, gates 1–6 PASS; 9 minor.
All minor fixes applied after the round (none changes a hypothesis or conclusion):

| Item | Fix |
|---|---|
| R07-1 / R08-m3 | 00_MAIN: (x_𝒞, x_𝒪) → (x_𝒞, x_𝓜) |
| R07-2 / R08-m4 | GD(b) population floor renamed c_pop (no clash with the beta-min c₀(s, A)) |
| R08-m1 | STATEMENT D0 "valid inputs" made precise (fixed designs: assumed; Gaussian rows: a.s.; MIS(ii): in 𝒜_n) |
| R08-m2 | §6 heading of L5 and 00_MAIN "Checks" column record R05 verdicts |
| R08-m5 | GD(a)/SL Corollary 2 sentence: "in the jointly Gaussian special case; S₀^𝒞 = s̃ for m = 0" |
| R08-m6 | Corollary N added to STATEMENT §2(i) |
| R08-m7 | "LS0 as specified; not in production code — GEN REPORT flag 4" carried in STATEMENT §3 and L3 |
| R08-m8 | Lemma T ρ̃_n constant 3 → 3/2 (cosmetic) |
| R08-m9 | STATEMENT §5: random-design EP versions not claimed |
