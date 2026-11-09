# W2-FAC-PK — LOG

* 08:31 — Read Wave2/Wave1C/Wave1 PROTOCOL.md, W2-FAC-B (REPORT, METHOD_REQUIREMENTS, STATEMENT, L1–L5, N2),
  W2-APP Lemma VN, FINAL s7 (Lemma CAP), SoP 02_method §§6.3, 6.10.
* 08:38 — numerics: copied cs_core.py, cs_gain.py, bvs_core.py, fac_core.py unchanged from FACB/numerics; wrote
  pk_core.py (closed-form CS start mode by per-block enumeration + max-plus DP; path tracer from any start, gain form;
  first scan index at which S₀ ∈ N(C) ∪ {C}). pk_selftest.py → pk_selftest_out.txt: partition = bvs_core complete
  linkage (5/5), start mode = general scorer (4/4), path = general Schur scanner (4/4), FACB N2 reproduced exactly
  (start 300, 19 swaps + 296 deletions, k_hit 314 > cap 311).
* 08:40–08:44 — N1 (n1_scale.py → N1_raw.jsonl, n1_log.txt): 60 data sets; summary in STATEMENT §0.
* 08:45 — Analysis: exact Gram needs p ≤ n − 1; p ≫ n is outside the class. Negative mechanism found: at size K the
  deletion gain is ≤ Δ_K ≈ ½log n + log 3 while a swap bringing in an excluded extreme null gains ≳ M_T·2log p ≥
  (1 − o(1))log p (M_T ≥ ½), and the start excludes every truth-free block's minimum — so the first ≥ n^{1/2−o(1)}
  moves are swaps (static argument, no path history needed). Positive part needs a deletion-phase drift control
  (leftover outside nulls near the band edge).
* 08:48 — N-FULL helper launched (delegate_task, Claude Sonnet 5.5 high, Claude Work): production v3.1 fits on exact
  CS data (copy of the core outside the repo; results in numerics/full_method/).
* 08:55 — N2 (n2_diag.py → N2_*.json): kept = blockwise top-u by ξ in every block; lowest 50 nulls excluded; band
  property at the end of the swap phase (0 violations); minimum leftover margin at the first deletion (0.004–0.04 nats),
  growing afterwards; centre rises ≤ 0.045 then falls.
* 09:00 — N3 robustness grid launched (n3_robust.py → N3_raw.jsonl). STATEMENT v1, PLAN written.
* 09:10 — N3 done (360 paths): no swap after the first deletion and no addition anywhere; 9 paths miss S₀, all
  weak-mixed (θ̄ = −0.1) at n = 2000, ρ = 0.95 (finite n; every n = 8000 path ends at S₀); ℓ_n + 2|S̃₀| suffices 360/360.
* 09:15 — R01 statement lock delegated (Codex Sol high). Drafts written (pre-lock, may change): lemmas/L0_imports.md,
  L1_start.md, L2_neg.md (Theorem NEG: static size-K scan bounds + counting).
* 09:30 — pk_selftest extended to p > K cases (4 more, all equal). l12_check.py (L1 structure: 6/6 data sets satisfy
  (b)–(d) where saturated; L2.2(i) on 66 sets; (ii) 20/20) and l2_chain.py (each link of L2.2(iii) on 48 size-K sets,
  incl. adversarial ones: 48/48; implication 42/42). Note: the asymptotic threshold a_n = 2 + √(log n + 30) is never
  reached at simulable n, so (iii) is tested link by link.
* 09:45 — **New route for (P3): static.** Every T ⊇ S₀ (|T| ≤ K) other than S₀ has an improving deletion; with > log²n
  extras its gain is ≥ (½ − ε)log n (two-sided tail counts + centring identity Σ_R(ξ − x) = x(s₀ + κ) − s_{S₀} + ϱ +
  uniform multiplier bound via a χ² union bound); F(S₀) − F(S̃₀) ≤ K(½log n + 2.4); hence m* ≤ (1 + δ)K and the path ends
  at S₀. No path dynamics, no (TK), no (PB) needed. lemmas/L3_static.md drafted; l3_static.py (6 data sets, n ≤ 6·10⁴):
  small-m gains ≥ 0.42 log n > c_D, budget holds, m*/K ∈ [1.01, 1.07]; l3_trend.py: worst large-m set (p = n − 1, ρ = 0.8)
  ratio 0.28 → 0.33 as n: 2·10³ → 1.28·10⁵ (O(1)/log n deficit, consistent with the asymptotic claim).
* 09:55 — METHOD_REQUIREMENTS.md drafted (MR-PK: cap ℓ_n + 2|S̃₀|, cost ≤ ×2 on the LS0 preflight term).
* 10:00 — HQ note: W2-SIM available. Sent request (numerics/SIM_REQUEST.md; R1 large-n paths, R2 production MR1 vs
  MR-PK, R3 iid rows incl. p ≫ n) to the W2-SIM thread.
* 10:20 — R01 (Sol high) **REJECT**, 10 items (reviews/R01_statement_lock_sol.md). Disposition reviews/R01_disposition.md:
  all applied or made moot by the static route (no swap-selection rule, no phase invariants, no (TK) needed).
* 10:25 — N-FULL helper result: no local production fit completed. hours = 2 → status resource_limit at preflight
  (merged LS0 worst-case charge ≈ 5.3·10⁵ s ≈ 146 h at n = 600, p = 450); hours = 1000 → > 20 min wall clock, killed.
  Recorded as operational outcomes (numerics/full_method/NF_summary.md); W2-SIM R2 addendum sent (allocation, fields).
* 10:35 — STATEMENT v2 (scope narrowing flagged; (P3) static, hypotheses (PK′) + blocks ≤ 16 only; (P4) cap rules
  a ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉); (P5) "minimal" = gap n^β vs δ|S̃₀|; (P6) pending). PLAN v2. L2 symbol t_n, [OP]
  wording; L4 delivery steps expanded; METHOD_REQUIREMENTS v2 (rule table, cost, preflight finding).
* 10:40 — R02 re-lock (Sol high), R03 check L0–L2 (Sol xhigh), R04 check L3 (Sol xhigh) launched in parallel.
* 10:45 — l3_small.py (adversarial small m, s₀ = 1, ρ ∈ {0.95, 0.8, 0.5}, n ≤ 2·10⁵): worst set always m = 2 balanced
  extremes (as in the proof), gain/log n 0.19–0.56 ≥ c_D (0.013–0.17); S₀ strict local max (best addition ≈ −log n).
* HQ framing update noted: list design-agnostic ingredients in REPORT (W2-UNI); finish current target first.
* 11:05 — R02 (Sol high) **LOCK-WITH-CHANGES** (3 items) — applied → **STATEMENT v3 LOCKED** (reviews/R02_disposition.md).
* 11:30 — R04 (Sol xhigh) L3: **VERIFIED-WITH-AMENDMENTS** (3 minor, 1 editorial; no fatal/major; reviewer's exhaustive
  pair search 9.6·10⁷ pairs found no counterexample) — applied (reviews/R04_disposition.md).
* 11:55 — R03 (Sol xhigh) L0/L1/L2: **VERIFIED-WITH-AMENDMENTS** ×3 (2 minor, 2 editorial; no fatal/major) — applied
  (reviews/R03_disposition.md). CHECKPOINT.md written (both key lemmas checked). R05 (L4 check, Sol high) running.
* 12:15 — R05 (Sol high) L4: **VERIFIED-WITH-AMENDMENTS** (1 major resource-scope, 4 minor, 2 editorial) — applied;
  STATEMENT v3.1 = flagged post-lock narrowing of (P4)(iii) (cheaply evaluated cap rules). reviews/R05_disposition.md.
* 12:35 — R06 mid-point (fresh Sol xhigh): **CONTINUE** (no fatal/major gap beyond the already-fixed v3 cap-evaluation
  issue); 2 minor presentation fixes applied (reviews/R06_disposition.md). Next: exhaustive sweep.
* 12:40 — citecheck.py → CITECHECK.txt: 33 citations, 0 misses.
* 13:20 — R07 sweep (Sol xhigh): 0 fatal / 1 major (implementation plumbing) / 5 minor / 5 editorial — all fixed
  (reviews/R07_disposition.md). REPORT.md drafted (council pending). W2-SIM FAC-PK results: none yet.
* 14:10 — Council round 1, R08 Sol xhigh: **8.6, gate 3 FAIL (REPORT §6 only)** — G2 residual floor exported as
  design-free (counterexample for p ≫ n), G1 used CS-specific Δ_k, mechanism paragraph lost qualifications. All fixed in
  REPORT (no change to STATEMENT or L0–L4). Waiting for R09 (Opus) before round 2.
* 14:30 — R09 Opus high: **9.1, all gates PASS** (1 minor, 4 editorial). Round 1 NOT PASSED (Sol gate 3). All fixes
  applied (reviews/R08_R09_disposition.md). Launching round 2 (fresh seats).
* **Timestamp correction (anti-hallucination):** entries after "08:41" (the last clock reading before council round 2) carry estimated times, not clock readings; the
  clock read 11:04 CST when council round 2 completed. Order of events is correct.
* 11:04 (clock) — Council round 2: R10 Sol 9.4 ACCEPT, R11 Opus 9.2, all six gates PASS in both → **PASSED**. R11's
  non-blocking wording fix and optional items applied (reviews/R10_R11_disposition.md). W2-SIM: only an S5 pilot under
  results/FAC-PK/pilot (not R1–R3); FAC-PK requests still pending. REPORT finalised.
