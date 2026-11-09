# C-MIS — CHECKPOINT (written 2026-11-08 ~22:44 CST, ahead of the 01:30 checkpoint)

**Proved and checked so far (statuses per protocol; nothing is PROVED-CHECKED until the council passes).**
* Statement lock: R01 (Sol high) LOCK-WITH-CHANGES, all 7 applied → STATEMENT v1.1 LOCKED.
* Theorem MIS (main; Song–Liang Thm 4/Cor 2 analog, p_𝒞 ≤ n^A): under a Gaussian-residual condition GR on the omitted
  contribution, the candidate-only problem *is* a well-specified model with truth β^𝒞 = β_𝒞 + γ and noise σ² + τ², so
  T03♯ transfers: 1 − π(S₀^𝒞) = O_P(√(log n/n)), MPM/HPM/PIP consistency, no-beta-min inclusion; random-design version
  via a new uniform-tightness diagonal lemma (DR). Jointly Gaussian rows give β^𝒞 = SL's β₀, S₀^𝒞 = SL's s̃; for one active
  omitted variable the proxies are exactly its Gaussian-graph neighbours among the candidates (Prop P). R02 (Sol high):
  VERIFIED / VERIFIED-WITH-AMENDMENTS (applied).
* Reported HPM: Corollary H (M5(0) with S₀^𝒞, any feasible T) and Corollary D (D_n^𝒞 → 0 on the GEN class with σ² := σ_𝒞²;
  W-family proxy instance D′). R02 VERIFIED / V-W-A (applied).
* Theorem F (fixed design, exact sparse projection EP; T03♯ re-run with every changed step written out: new event G5,
  δ_n^𝒞, E_n^𝒞 with σ²_{𝒞,n} = σ² + Δ_n, signal with μ^𝒞) with a tail hypothesis TAIL^𝒞, discharged for bounded p_𝒞
  (Cor F(a)) and, for growing p_𝒞, under a large-omitted-residual condition TL (Lemma T / Cor F(b), new). R03 (Sol xhigh):
  VERIFIED-WITH-AMENDMENTS (applied); one frontier paragraph (L5 §2) was GAP/FALSE and has been replaced.
* Mid-point R04 (fresh Sol xhigh): **CONTINUE**; 2 major (statement wording of the Gaussian-design part), 7 minor — all
  addressed; added Lemma Z (null projection), Example E1 (analytic target separation), Examples E2/E3 (GR/EP cannot be
  simply deleted).
* Numerics (exact enumeration, p_𝒞 ≤ 10, 20 seeds, n ≤ 6400): N1–N7, N3b — no contradiction; they single out the
  population-projection support (not S₀ ∩ 𝒞, not the dense sample-projection support) and the dilution scale σ²_𝒞.

**Left.** R05 (dedicated check of Lemma Z and E1–E3) and R06 (exhaustive sweep) running; inequality-level check of L4
(check_L4.py) running; then CITECHECK rerun and council (Sol xhigh + Opus high).

**Estimate.** The target closes as PROVED-CHECKED **if** the council passes, in the narrowed form: main theorem under GR
(any p_𝒞 ≤ n^A, s₀^𝒞 ≥ 1 fixed) + fixed-design EP theorem with TAIL discharged for bounded p_𝒞 or under TL. Expected
by ~01:30–02:30.

**Narrowings already made / foreseen.** (1) SL's Cor 2 is support inclusion; ours is exact-model concentration under
stronger hypotheses (GR) — no density-contraction analog. (2) Fixed-design EP for growing p_𝒞 with small omitted residual
(0 < Δ_n ≲ σ²(1/3 + rank/N)) remains open (TAIL^𝒞 unproved there); T02(i♯)'s denominator strategy provably loses an
e^{−cN} factor under EP (Lemma O2). (3) Non-Gaussian/heteroscedastic omitted residual: not covered (E2 shows a common
random slope breaks the transfer). (4) Growing-p null projection (s₀^𝒞 = 0) not claimed. No method requirement for C-ENG.
