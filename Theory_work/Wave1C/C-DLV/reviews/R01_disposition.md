# R01 (statement lock, Codex gpt-6.1-sol high) — disposition by the lead, 2026-11-08 ~21:58 (clock-corrected)

Verdict received: REJECT (1 FATAL, 7 MAJOR, 2 MINOR). Verbatim reply: R01_statement_lock_codex.md.

1. FATAL (target not delivered by the conditional plan) — ACCEPTED. STATEMENT v2 keeps the ticket target (T) verbatim
   as the goal, explicitly NOT claimed, and separates proved reductions (P1–P5), conditional criteria (C1–C2), the
   finding (F1) and the open obstruction (O). The report will flag RESULT = PARTIAL unless (O) is closed. No scope
   change is assumed; HQ decides.
2. MAJOR (grid ≠ pilot schedule because of the 1 − 10⁻¹² snap) — FIXED: L3 Prop. 3.5 now says "points = pilot
   temperatures up to the first in [1 − 10⁻¹², 1], replaced by 1; later targets skipped; ≤ k intervals"; Lemma 3.4(b)
   amended. The snap is kept as a literal instruction (not removed under EX-A).
3. MAJOR (`validation_failed` reachable after a snap) — ACCEPTED; the reviewer's two-state counterexample is recorded.
   INVENTORY D1a v2 lists it as reachable; Theorem D event (γ); L5 Cor. 5.3 carries it.
4. MAJOR (units of the resource envelopes; exact-branch preflight time) — FIXED: L1 R.5 defines separate envelopes
   (operations, words, bytes = βM̄ + β₀, preflight bytes P₀, P₁, seconds, exact preflight estimate P̄_t), adds timing
   context, V snapshots, guard records, serialisation, worker caches/merge state; Corollary R allocates
   mem_n ≥ max{βM̄ + β₀, P₀, P₁}, time_n ≥ max{2(τW̄ + τ₀), P̄_t}.
5. MAJOR (p_raw vs p; malformed inputs; exact-branch bound) — FIXED: L1 R.4 states Lemma R for valid inputs with p_raw;
   p_raw = p a.s. on the classes (L2 S.1); exact enumeration bounded by the branch rule E ≤ (5H₀ + 4N₀)p.
6. MAJOR (inventory omissions) — FIXED: INVENTORY v2 rows F4 (checkUserInterrupt at core/cpp/v3_core.cpp:520, signals,
   worker crash), F5 (R/C++ allocation exceptions), F6 (compile lock, cache copy, `digest`), each with its exclusion
   (MACH) or bound (Corollary R).
7. MAJOR (S₀ ∈ V retention/discovery) — RESOLVED BY REMOVAL: the Ψ_n route (which needed S₀ ∈ V) is demoted to a
   remark; the dominance criterion (L3 Prop. 3.5(a)) and the two-model lemma (L5) use any models of V, not S₀. The point
   "LS0 runs after calibration, so it cannot help pre-calibration discovery" is recorded.
8. MAJOR (failure decomposition incomplete) — FIXED: Theorem D (iii) decomposes construction failure into (α) count,
   (β) non_progress (with its EX-A size condition), (γ) post-snap validation; L5 bounds N_b and non_progress under its
   two-model hypothesis and states that the uniform two-model approximation for the realised V is NOT proved (O).
9. MINOR (F2 citations from auxiliary entry points; "union of A1–G4" wording) — FIXED: F2 replaced by a call-graph
   argument (L2 S.3); INVENTORY scope sentence added (D3–D5, G1, G3, G4 listed as capped/non-stopping, not exits).
10. MINOR (record surviving proofs; IDEAL-W/EX-A cost model) — ACCEPTED: STATEMENT v2 §1 states IDEAL-W as an abstract
   unbounded-word machine keeping the RNG's modular arithmetic, and EX-A as a unit-cost real-arithmetic model; the
   scorer proof and pilot cap are recorded in L2 S.2 and L3 Lemma 3.3.

Lock: STATEMENT v2 locked at ~21:58 with these changes (protocol: "Fix, then lock").
