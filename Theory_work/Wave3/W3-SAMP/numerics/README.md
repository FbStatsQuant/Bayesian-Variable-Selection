# W3-SAMP numerics index (revised after SW1, 2026-11-09)

All scripts: Python 3.13 + numpy, run from this folder (`py -3.13 <script> …`); local, small. Status of every result:
**falsification attempts; no violation detected** — not proofs. "Regression-score component targets" use the T12 §0
score and prior with *prescribed* blocks, B and a ring neighbour graph, and small component budgets; they are not
production preprocessing or production budgets (SW1 #17). Finite-target probes cannot witness sequence-level premises
(P-CONC, NC_r).

| File | Produced by (exact invocation) | Content |
|---|---|---|
| `samp_sim.py` | — | floating-point simulation of T12 §1–§2's frozen island on a small Ω (arbitrary positive γ₀, d); exact kernel matrices; RB recorded before each Gibbs draw (verified as such by LC1) |
| `RESULTS_v1.txt` | `py -3.13 run_checks.py 20261109` | §1 MR identities + ST exact; §2 LT cells at δ = 0.24 (all vacuous: right sides > 1) and the κ₀ good-path check (corrected filter); §3 C v1 bounds and T sweep (T and N vary together); §4 finite-target collapsed-evidence probes ("trap", "near" at L = 5); §5 D equality + conditional discovery counts |
| `RESULTS_v1_sec4b.txt` | `py -3.13 run_checks.py 4 --sections 4 --near-L 5,20` | §4 only, seed 4: "trap" and "near" at L = 5 and L = 20 (single invocation; replaces the earlier combined log and the removed `sec4.py`, SW1 #3) |
| `RESULTS_v2.txt` | `py -3.13 run_checks_v2.py` (seed 7) then `py -3.13 run_checks_v2b.py` (seed 11, appended) | regression-score component targets; pointwise stopped-sum and C-i checks; heavy-tailed W; concentrated n = 400 case |
| `RESULTS_v3.txt` | `py -3.13 run_checks_v3.py` (seed 31) | T-free C (telescoping budget, β), E E_r ≤ g + β/2, bias ≤ β/2 (T and N vary together); TR minorization for 200 random orders; TR bound (vacuous in the "near" case — repair outside TR's regime, SW1 #19) |
| `RESULTS_v4.txt` | `py -3.13 run_checks_v4.py` (seed 404) | 18 non-vacuous cells: 8 LT-a, 3 LT-b′, 7 LT-b with the exact λ₀ (vacuous with the relaxed 19o₁); E[W E_r] ≤ g; C with N fixed at 2 and T ∈ {1, 4, 32, 128}; tolerance 3 Monte Carlo s.e. stated per cell |

Provenance (SHA-256, first 16 hex digits; SW1 #3): samp_sim.py 598bf0326b6e2966; run_checks.py 1bb30cd6d659c185;
run_checks_v2.py 11a1fc4dbc7bc210; run_checks_v2b.py 6b8a4c073e64fb44; run_checks_v3.py 8b4499d4763212fb;
run_checks_v4.py 2cb2edcb83ba40ba; RESULTS_v1.txt 0f4e688b4e26ee13; RESULTS_v1_sec4b.txt a918a59634f61beb;
RESULTS_v2.txt a0b8398900815700; RESULTS_v3.txt f2a0edec99743e19; RESULTS_v4.txt 16e4c6947ef8f977.
RESULTS_v1 and v1_sec4b were regenerated after SW1 from the current `run_checks.py`; sections 1–3 are unchanged from the
first run (same seed and draws), §4/§5 changed because the "near" target parameters had been edited after the first run
(the first-run "near" row, δ = 0.0214, π₀(S₀) = 4.24e-5, came from earlier parameters and is superseded).
Violation counters use integer increments (SW1 #16).
Violation counters in run_checks_v2.py / v3 add numpy booleans, which can merge simultaneous failures in one cell into one count; a reported total of 0 is unaffected (SW1 #16).
