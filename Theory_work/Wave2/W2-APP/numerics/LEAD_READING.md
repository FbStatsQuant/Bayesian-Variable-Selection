# Lead's reading of the falsification numerics (W2-APP) — v2 (after sweep R07)

Files: ct_check_out.txt (L2), post_check_out.txt (L1), NUMERICS_LOC_VN.md + n1/n2/n3/n3b outputs (L3, L5; helper
Sonnet 5.5), vn_bound_recheck.py → vn_bound_recheck_out.txt (lead, R07 #14). All are finite-n observations; none is
used as proof, and none certifies an asymptotic onset.

**What the n1–n3 numerics run [R07 #15, #16].** A Python *component port* of the method (C-GROW/numerics/bvs_core.py,
imported unedited): complete-linkage ties within 1e-10, start-DP ties within 1e-12, start enumeration cap 2·10⁴
(production: exact equality, tie-aware DP, cap 10⁶); LS0 = the port's §6.10 local search with the shipped cap rule
ℓ_n + |S̃₀|. Sixteen slow n3 runs used a *screened* search (n3b_fastls.py: swaps pre-screened by Cholesky updates,
those within 1e-5 of the approximate maximum rescored exactly; three paths validated identical to the port, the other
decisions unverified, and the screened-out neighbours are not recorded as scored). These are statements about the
port, not production runs.

* **L2_CT / CD:** every observed ratio ≤ 0.48 of the bound over 36 matrix/permutation cases (incl. non-Markov MA(2),
  AR(2), random banded precision, blocks g = 20, random-sign exponential decay). R02 independently re-ran checks.
* **L1_POST:** sample sparse floors (search upper bounds) never below the rigorous Weyl lower bound; m♯ ≤ m̄ in all
  cases (p = 2000, 4000 ≫ n).
* **L3 (n1, window innovations):** the sample part of Z − Z′ scales as √(|T∖T′|/n); the population part decays with the
  window radius r for MA(2)/AR(2)/AR(1) and does not decay for blocks g = 20 while r < g — consistent with L3.6, which
  uses a growing window r_n = ⌈log log n/t₂⌉. For AR(1) a radius-one window is not uniform (R03 item 3).
* **L3 (n2, 96 data sets, local designs L1–L4):** S₀ ⊆ S̃₀ in 96/96; LS0 scored S₀ and certified in 96/96; endpoint S₀
  in 94/96 (two certified local maxima S₀ + one null at n = 800); moves = |S̃₀ ∖ S₀| in 95/96.
* **L5 (n3, 52 data sets: 40 in the VN examples V1 = 12, V2 = 16, V3a = 12, plus 12 cancellation controls V3b)
  [R07 #11, #13, #14]:** every extra in S̃₀ was a visible null; extras grow with n. vn_bound_recheck_out.txt compares the
  STATED bound min(K − s₀, |𝒩| − 15s₀) with the total extras |S̃₀ ∖ S₀|: met in V1 (all 12 runs; bound ≤ 8) and V3a at
  n = 12800 (4/4); not met in V2 and V3a at n ≤ 3200. VN is an asymptotic statement (its proof needs nκ_n ≫ log n plus
  regularity events); a finite-n shortfall is not a falsification and no onset is claimed. V3b (Σ_kθ*_k = 0) is a no-claim
  control: start modes stay small (5–23 over runs).
* **Method behaviour where the routes are obstructed:** in the port, LS0 from the start mode reached S₀ in 40/40 runs of V1/V2/V3a
  (start modes with up to 218 extras) — 24 with complete scans and a certified endpoint, 16 with the screened search, whose
  certified=True flag means no improvement among the retained/rescored candidates, NOT a complete-scan certificate
  [C1-Sol-3] — and in 12/12 controls (complete scans). Component observations,
  consistent with the obstruction concerning the proof routes; method consistency on these designs is UNPROVED; not a
  production statement [C1-Opus-1].
