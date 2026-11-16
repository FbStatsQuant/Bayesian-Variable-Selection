# Theory ↔ Engineering interface (Theory Department writes here; Engineering writes in Docs/Experiments/P1M/REQUESTS.md)

**Owner scope clarification (11-15, POLICIES end of §8):** theory covers the method as coded at 10⁴; the 1M variant is Engineering's, documented and validated on an overlap rung. The premise tickets below are **downgraded to Engineering's choice** (no theory tickets), except T-MERGE's convex-pooling result if islands + merge stay in the theorem-covered method (owner to confirm). PSMC-S0 Part 1 (T-N, T-CAL prelim, D-7) still delivers as Engineering-facing notes; Part 2 (T-PART) cancelled.

Premise table (historical): `Docs/Experiments/P1M/ENGINEERING_SPEC.md` §4.2 (v1 draft 11-15). Theory tickets as first planned:

| ticket | engineering change (class) | theory question | blocks | needed by (our reading; Eng to confirm) | plan |
|---|---|---|---|---|---|
| T-PART | truncated complete linkage at 1 − τ_n + min-index packing (Δ on π₀), OD-5; exact rule THEORY-1 | every consumer in THEORY-1 (tables/π₀; γ₀ and d(S) → bridge path N1/LT♯/C/TR; π₀ draws; leader store → V → grid; start mode → LS0; table models in stores; (V) via B − 1); sub-choice ≥ vs > | WP2 config (coding not blocked: parameters) | 11-25 soft / 12-04 hard | PSMC-S0 Part 2 → CP2 Tue 11-24 |
| T-N | fixed N = 2,500 per island (Δ), OD-1 | TH01(e)(f)(i), TH06, TH08 for general (N, R′); confirm RM-0, LT♯, TR, D need nothing | owner OD-1 batch | **11-20 soft** / 11-23 hard | PSMC-S0 Part 1 → CP1 Thu 11-19 12:00 |
| T-CAL | bounded calibration I_max, no escalation except construction failure (C), OD-2 | preliminary: which delivered results read E2 / tiers / grid convergence; frozen-𝒞 results untouched; C-DLV | owner OD-2 batch | **11-20 soft (prelim)** / 12-04 full | prelim in PSMC-S0 Part 1; full in the campaign |
| T-STREAM | position-addressed counter streams (L), OD-8 | is a counter-based generator acceptable under EX-S / IND-T (O5); independence on the enlarged address map (O18) | WP3 generator + address map (~11-27); T4 at G-A | 11-27 soft / 12-04 hard | campaign: first ticket after the freeze (Mon 11-23) |
| T-MERGE | R′ = 16 process islands + merge (L / new functions) | O1, O10, O19–O21; pooling under evidence-weight degeneracy; OD-4 is a label switch (all PIPs returned) | claims wording before G-C | 11-30 soft / 12-18 hard | campaign (main theory ticket) |
Log of exchanges:
- 2026-11-15 19:34 CT — Theory → Eng: interfaces (1)–(4) asked (exact OD-5 rule + consumers, dates, OD-4 status, contact files).
- 2026-11-15 19:38 CT (received) — Eng → Theory: REQUESTS.md THEORY-1 (exact rules + full consumer list), THEORY-2 (dates), THEORY-3 (OD-4 working assumption; evidence = R6, DESIGN_v1 §4.4, CP2 §3). Protocol (4) agreed. Table above updated; PSMC-S0 brief rev. 1 (T-N + T-CAL prelim first).
- 2026-11-15 19:45 CT — Theory: D-7 (final-run leader stores) is in PSMC-S0 Part 1, with a verdict SAFE TO DROP / NOT SAFE at CP1 (by Thu 11-19 12:00 CT). D-3 (`logical` cost column) and D-8 (PIP_𝒯, log Z_𝒯, law.bin) registry staging: send the specifics (fields, definitions, which registry rows or card items) in REQUESTS.md; our recorder dry-runs them; HQ approves the real runs.
- 2026-11-15 19:46 CT — Eng → Theory: THEORY-4 (Entries A/B wording, Check C). Theory: recorder task E stages A and B (dry run; B(ii) pinned to code or recorded with no theorem status; B(i)/(iii) conditional on DIST-C(i), a CANDIDATE); Check C verdict from PSMC-S0 by Thu 12:00 CT, possibly sooner; the output-list entry waits on it.
- 2026-11-15 19:55 CT — Eng THEORY-5: B(ii) pins (store F, γ₁, Ẑ_r start, Ω) → recorder to verify; B(i)/(iii) conditional on DIST-C(i) agreed; Check C scope clarified (only the returned leaders_gamma0/1 field and final-run structure; inherited models still offered at the merge). Thu 12:00 OK.
- 2026-11-15 — Theory: owner scope clarification applied (see top). Check C (D-7) and the T-N/T-CAL notes still come with PSMC-S0 CP1 (tonight or by Thu 12:00). Entries A/B staging unaffected.
- 2026-11-15 19:57 CT — Eng: scope change acknowledged on their side; THEORY-2 dates void as gates; still useful (non-blocking): Entries A/B, Check C (now about the 10⁴ method's outputs). Consistent with D18.
- 2026-11-15 20:06 CT — Eng THEORY-6: τ_n, ≥/>, packing order are their design choices (overlap-rung validated); PSMC-S0 Part 1 notes feed their spec v2; T-MERGE follows the owner's answer via HQ.
- 2026-11-15 20:34 CT — Eng: bvs_tmp convention (theory/ subfolder; CI via TMPDIR → bvs_tmp/ci). Applied to all Theory leads.
