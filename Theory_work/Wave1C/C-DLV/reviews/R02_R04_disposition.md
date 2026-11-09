# R02 (L1+L2) and R04 (L4) — dispositions by the lead, 2026-11-08 ~22:25

## R02 (Codex gpt-6.1-sol high) — verdict GAP (L1), L2 survives with S.3 extension. Verbatim: R02_L1L2_codex.md.
1. MAJOR cache probing / clearing / key comparison / Start::comp / store costs missing — FIXED: per-request overhead
   ω(n,p) ≤ C p(n+2) added to R.2 and to W̄ (L1 v2).
2. MAJOR allocation dropped the (n+p)²p log³ term — FIXED: Corollary R's displayed time_n keeps it (and the new p²n²,
   pn-terms).
3. MAJOR spec tie-aware DP had no resource proof — FIXED by a method requirement: the e4 fallback must be W1-N3's TDP
   (PROVED; XF-checked; O(p·Σ_b(2^{|C_b|} + (K+1)²)) operations) or any algorithm within that bound
   (METHOD_REQUIREMENTS A.2); enumeration fast-path traversal charged (≤ J·10⁶ nodes, each completion O(J + K log K)).
4. MINOR memory additions not reconciled — FIXED: M̄ now lists island/RB archives, search archives, snapshots, guard
   records, grids, worker caches, timing context, serialisation (factor 2); each shown O((n+p)²).
5. MINOR S.3 incomplete — FIXED: invariants (i)–(vii) incl. `setup required`, model validation, provenance enum,
   nth_nonmember, class assertions.
6. MINOR timing size k_t = min(K, ⌈p/2⌉) and timed-loop cost — FIXED (U₂₀₀, P̄_t).
Status of L1 after fixes: PROVED (by this seat); a re-check is folded into the exhaustive sweep (fresh reviewer).

## R04 (Codex gpt-6.1-sol high) — verdict VERIFIED-WITH-AMENDMENTS. Verbatim: R04_L4_codex.md.
1. MAJOR Corollary D′'s CAL justification — FIXED with the reviewer's pathwise argument: 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆
   {π(S₀|y) ≤ ½} ∪ {prescribed LS0 misses S₀}, under the unconditioned data law; CAL not used; also covers the exact
   branch (where 𝒪 ⊄ {calibration ok}, as the reviewer noted). Proposition F's consistency claim now cites D′.
2. MINOR cutoff — FIXED: n_β ≈ 2.28·10⁸ (reviewer's recomputation), ν = n/2 + 0.01 kept.
3. MINOR attainability of (β) — FIXED: "this crude bound no longer excludes (β)"; attainability neither claimed nor
   excluded.
Also recorded: fallback grid keeps the T_e cap but not the restricted-ESS property; implementation should keep budgets,
inherited models, frozen hash, and label the source.
