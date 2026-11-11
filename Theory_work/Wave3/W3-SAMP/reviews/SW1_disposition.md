# SW1 disposition (exhaustive sweep, rerun, Codex gpt-6.1-sol high) — 2026-11-09

Counts: CRITICAL 0, MAJOR 4, MINOR 16, EXPOSITION 8 (28). Reviewer: "no false central MR, LT, C, D, or TR inequality …
constants 19, 21, 22, 44, 152 track … correct as a conditional/interface theorem package after the fixes." All 28 accepted.

| # | Sev. | Disposition (where) |
|---|---|---|
| 1 | MAJOR | HPM is the maximum of the final ledger's offered set, not a function of island records (STATEMENT PC (ii)–(iii); `PC_completed.md` (ii), (iii), consequence line). |
| 2 | MAJOR | Three-state example relabelled "abstract positive-target example, not a realisation of the coded target (coded 3-state space has d ≡ 0)"; non-nesting stated only for abstract targets, coded separation open (STATEMENT TR label; `TR_theorem.md` remarks). |
| 3 | MAJOR | Numerics provenance: `run_checks.py` now has a section filter; RESULTS_v1 and RESULTS_v1_sec4b regenerated from it by recorded invocations; `sec4.py` removed; SHA-256 manifest and the superseded first-run "near" parameters recorded (`numerics/README.md`). Sections 1–3 verified identical to the committed first run except the corrected good-path line. |
| 4 | MAJOR | Script/result labels now "finite-target … (illustrations; NOT asymptotic witnesses)"; ASSUMPTION_MAP rows rewritten. |
| 5 | MINOR | "No output certifies" restricted: true when the top store (40p+1) is a strict subset of Ω; exact reconstruction possible otherwise (STATEMENT LT-f; LT Step 6). |
| 6 | MINOR | Ledger bound renamed "observable sufficient condition for the finite-run event {W_r < η}", not evidence against NC_r. |
| 7 | MINOR | κ₀ claim restricted to pathwise sharpness (ASSUMPTION_MAP). |
| 8 | MINOR | Conditional statistic computed: S₀ a terminal endpoint given no draw hit S₀ in 13773/15015 and 30559/31505 islands (RESULTS_v1 §5; ASSUMPTION_MAP). |
| 9 | MINOR | `draw_pi0` uniform count corrected (remaining-size-loop iterations incl. zero-size blocks) (`D_theorem.md`). |
| 10 | MINOR | P-OVL defined through Q_D = D_rπ₀(S₀) on 𝒜, ∞ off 𝒜 (STATEMENT §1). |
| 11 | MINOR | Consequences localised to 𝒜 (`TR_theorem.md`, `C_theorem.md`, ASSUMPTION_MAP implications). |
| 12 | MINOR | Transfer audit extended: v3_score/util/blocks/calib identical; v3_start identical through `draw_pi0` (equal SHA-256), later diffs = LS0 start-mode DP; v3_runtime 4 lines of LS0 event labels (`CC_code_check.md` header; `MR_identities.md`). |
| 13 | MINOR | Component call shown in full with `init_states = nullptr`, Hm = 4, integer budgets, potential run (STATEMENT §0; CC note). |
| 14 | MINOR | ST-c states the T12 (R3) path-law hypothesis and its code realisation (STATEMENT; `ST_stay.md`). |
| 15 | MINOR | Linear-δ̄ remark softened to "possible; no lower-bound family claimed" (`C_theorem.md`). |
| 16 | MINOR | Integer counter in `run_checks.py`; v2/v3 caveat recorded (README); zeros unaffected. |
| 17 | MINOR | "Regression-score component targets" wording (README, `C_theorem.md`). |
| 18 | MINOR | v1 LT cells labelled vacuous; new `run_checks_v4.py` → `RESULTS_v4.txt`: 18 non-vacuous LT-a/b/b′ cells + E[W E_r] ≤ g, no violation (`LT_theorem.md`). |
| 19 | MINOR | TR "near" simulation labelled repair outside TR's regime, bound vacuous (`TR_theorem.md`, README). |
| 20 | EXPO | Stage index renamed k in C Step 2. |
| 21 | EXPO | L3 citation 27–29; A₀ (value space) vs E₀ (event) distinguished (`MR_identities.md`). |
| 22 | EXPO | ST citations T12 25–31, L2 18–20. |
| 23 | MINOR | `citecheck.py` rewritten: labels EXISTS/IN-RANGE, excerpt first/last line + block hash, unsupported forms disclosed, semantic checks documented as manual (`reviews/CITECHECK.txt`: 83/83 in range). |
| 24 | EXPO | ASSUMPTION_MAP rewritten as the live v3 registry + dated gate history. |
| 25 | EXPO | "subjected to falsification attempts; no violation detected" wording (ASSUMPTION_MAP, C numerics). |
| 26 | EXPO | C numerics state 3-s.e. tolerance and that T, N co-vary in v3; v4 adds a fixed-N (N = 2) T sweep. |
| 27 | EXPO | LT-e′: thresholds η_{n,r} for every r; union over islands; endpoint conclusion derived from LT-a (STATEMENT; LT Step 5). |
| 28 | EXPO | TR conditions island by island on the island's own history (STATEMENT; `TR_theorem.md` (TR-b)). |
