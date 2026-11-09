# W2-SIM family S5 — DESIGN

## E-S5CC — global error e_T along the uncapped LS0 path on exact-Gram block compound symmetry (W2-FAC-S5 request)

**Informs.** W2-FAC-S5 STATEMENT v2 (LOCKED): Tier 2 **Lemma KL** (claim C5: P(CC_n(δ)) → 1) and the frontier claim C6;
secondarily the path claim C2-R (reached_S0). Request: `Theory_work/Wave2/W2-FAC-S5/numerics/SIM_REQUEST.md`.

**Which outcome changes the theory (from the request, verbatim criteria).**
(a) bulk (m ≥ 30) max κ₀|e|/H does NOT decrease with p (stays ≥ 0.03 at p = 2·10⁵) ⇒ the conjectured KL mechanism
(e_T → 0 relative to H in the bulk) is wrong; (b) |I| ≥ 2 persisting into m ≤ 5 in a positive fraction of runs ⇒ the
end-phase imbalance control of FAC-CS does not transfer; (c) any reached_S0 = false at log p/log n < 1/2 ⇒ candidate
counterexample to the path claim (seed kept). Every cell here has log p/log n ≤ log(2·10⁵)/log(10¹²) = 0.44 < 1/2.

**Model / scorer (unchanged ticket code).** `bcs_core.py` (ticket snapshot `code/tickets_20261109T0943`, sha256
b6c0fb53…ed98c9, identical to the local file) imported unchanged: exact-Gram BCS X'X = (n−1)Σ,
Σ = ρ_b 11ᵀ + ⊕_g(bJ_q + dI_q), noise g = √ρ_b η + √b ζ_{g(j)} + √d ξ_j, closed-form production score F, uncapped
path from the full model T₀ = [p] (pure null deletions by best exact gain; the loop stops at the first non-null or
non-improving best deletion, recorded as reached_S0 = false). Truths: `layout(p, q, s0=4)` (4 truths in distinct
groups spread over the index range, ϑ = (1.4, −1, 1.8, −1.2)), σ² = 1. The path uses deletions only (no
addition/swap check), exactly as s3_cc.py (S1/S1-EXH of the ticket certify pure deletion on p ≤ 2000 with swaps).

**Driver (v2 after design review R01, reviews/S5_R01_design.md + disposition).** `S5/scripts/s5cc.py` = verbatim
s3_cc.py (snapshot sha256 2886c060…8c928b3) loop and RNG (`default_rng(10007·seed + p)`); the only in-loop change is
`gains(swaps=_dosw)` at swap checkpoints (deletion/addition gains computed by identical code; the swap value is recorded,
never acted on). Added read-only fields (full list in the script docstring): in units **H = √(2 log 2p)** (as
requested; the original cc_* fields use H_q) with m = # retained nulls: r(T) := κ₀·max(|e_T|, max_{j retained null}
|e_{T∖j}|)/H (the same `vals` as cc_max), maxima per phase bulk (m ≥ 30) / mid (30 > m ≥ 5) / end (m < 5, incl. S0),
**null if the phase was not visited**; centre-only rT; band maxima; r over m ≥ p/10 and m ≥ √p; single-state r at fixed
m; **admissible δ** min_T [1 − (H_q + κ₀ max|e|)²/Λ_k] and its deterministic e = 0 baseline; **competing moves**
(best addition every step; candidate swap at checkpoints every ⌈p/400⌉ steps and every step with m ≤ 100; terminal state
at S0); `deletion_path_complete` (= reached_S0: the deletion-only path Π reached S0 — **not** a certification of the
LS0 path), `fail_reason`, `m_final`, deletion-sequence sha1; imbalance I(m) = #(τ>0) − #(τ<0) over retained nulls,
τ = τ_{j|T∖j} (`noise_tau()["tau"]`), at m = 30, 10, 5, maxima over m ≤ 5 / 5 < m ≤ 30, unrounded end trace (m ≤ 30).
**Validation** (`S5/validation/`): original 12 fields identical to s3_cc.py in 6/6 cases (`val_compare.txt`);
independent per-state recomputation of every added phase/δ/imbalance/addition field agrees in 5/5 cases incl. one without
a bulk phase (`check_s5cc_states.py` → `val_states_check.txt`).

**Grid (480 runs).** S5 (q, ρ_b, ρ_w) = (5, .3, .7): p ∈ {2·10³, 10⁴, 5·10⁴, 2·10⁵} × n ∈ {10¹², 10²⁰} × seeds 1–50.
CB (3, .2, .6): p ∈ {10⁴, 5·10⁴} × n ∈ {10¹², 10²⁰} × seeds 101–120 (the request says "20 seeds"; 101–120 are used so
that CB streams differ from the S5 streams at the same p). Seeds: rng seed 10007·seed + p (recorded per run);
distinct across p and designs; **identical across the two n values by construction of the ticket driver** (common
random numbers: e_T does not depend on n; n enters only through the path choice — the summary reports the fraction of
seeds whose e-statistics are identical at both n). Hence per (design, p) the e-statistics have 50 (S5) / 20 (CB)
independent replicates, not 100/40. For p = 10⁴ with q = 3 the last group has size 1 (5·10⁴: size 2) — harmless.

**Cost (pilot s5_pilot01, job 2633049, all rc = 0).** Path wall time on NOTS: p = 2·10³ 2 s, p = 10⁴ 13 s;
cost probe (first K steps): 4.6 ms/step at p = 5·10⁴ (path ≲ 230 s), 22 ms/step at p = 2·10⁵ (path ≲ 4400 s,
RSS 116 MB). All 50 seeds are feasible at p = 2·10⁵; no faster re-implementation is needed.

**Analysis** (`S5/scripts/summarise_cc.py` v2, local): integrity check against both task tables (abort on unknown /
duplicate keys or rng mismatch; missing tasks listed); per (design, p, n): complete / incomplete deletion paths (seeds,
reason); competing-move table; δ table (baseline, δ_adm mean/min, pass rates δ ≥ 0, 0.1, 0.25 — cells with negative
baseline cannot diagnose e: at n = 10¹² the baseline is ≤ 0 for large p since H_q² > Λ_k; finite-n only, no bearing on
asymptotic KL); r statistics over runs that visited the phase (N shown; bootstrap CI B = 4000); bulk-proper, fixed-m and
band tables; imbalance events E1 (primary: |I| ≥ 2 at some m ≤ 5), E2 (re-entry after |I| ≤ 1), E3 (|I| ≥ 2 at ≥ 2 of
m ∈ {5..1}) with Wilson 95% intervals (0/50 excludes rates > 7.1%; 0/20 > 16.1%); slopes of log mean vs log p on complete
paths, bootstrap CI only when every cell has ≥ 2 runs; n-pairing via deletion digest and all unrounded e-statistics.
**Decisive statistics:** (a) r_bulk at p = 2·10⁵ vs 0.03 and its p-trend, read with the bulk-proper / fixed-m / band
statistics (the pilot shows r_bulk attained at the m = 30 boundary); (b) E1 (with E2/E3); (c) deletion-path completion
(and any competing-move violation).

**NOTS submission (revised for the swap-checkpoint cost; pilot03 job 2634898 times p = 10⁴, 5·10⁴, 2·10⁵ with the v2
driver).** `s5cc_small` (S5 p ∈ {2·10³, 10⁴} + CB p = 10⁴: 280 tasks) scavenge 1 h, 2 GB, throttle 8; `s5cc_mid`
(S5 p = 5·10⁴ + CB p = 5·10⁴: 140 tasks) commons, 3 h, 4 GB, throttle 7; `s5cc_big` (S5 p = 2·10⁵: 100 tasks)
commons, 10 h, 6 GB, throttle 10 (sum 25 = allotment; throttles raised via scontrol as arrays finish).

**Pilot output (v1 driver; the v2 fields are a superset)** (`results/FAC-S5_CC/pilot01/`): p = 10⁴ seed 1: reached_S0, r_bulk = 0.0377 attained at m = 30,
band [30,100) 0.0377, [100,300) 0.0174, [300,10³) 0.0097, [10³,3·10³) 0.0083, [3·10³,10⁴) 0.0030; identical
e-statistics at n = 10¹² and 10²⁰; I(30) = −2, I(10) = −2, I(5) = −1.
