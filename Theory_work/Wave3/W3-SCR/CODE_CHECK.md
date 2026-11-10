# W3-SCR — code check: what `local_certified` means in the coded output

Source: `Scripts/SMC_BVS/core/` as read at main @ 2252d57 (identical files copied to `numerics/core_copy/`, hashes in
`numerics/core_copy/SHA256SUMS_source.txt`). The core files were last changed at commit 72785fe and are byte-identical
at the later HEAD 2ac3896 (hashes re-verified by the lead and by the Opus council seat). Every line reference below is to that tree.

## The local search (`cpp/v3_engine.h:379-419`)
`local_search(centre, ell, …)` keeps a current centre C and repeats:
1. **Complete scan of the coded neighbourhood of C** (lines 394-406): every flip j = 1..p — a deletion if j ∈ C, an
   addition if j ∉ C **unless |C| ≥ K, in which case the addition is skipped** (line 397) — then every swap
   (j ∈ C out, l ∉ C in). Every scanned model is scored (`eval`, line 391).
2. `best` = the scanned neighbour with the largest F (exact ties by lexicographic order, line 392).
3. If `best.F > C.F` (strict, line 408): if `moves ≥ ell`, stop with `local_limit = true`,
   `termination = "move_limit"`, `returned = best.S` (a model that was scored as a neighbour but was **not** scanned as a
centre by this search),
   `local_certified` stays false (line 410). Otherwise move to `best` and repeat (line 412).
4. Else (no scanned neighbour has F strictly larger than F(C)): stop with `termination = "no_improvement"`,
   **`local_certified = true`, `returned = C.S`** (line 414).

**CC1.** A search archive has `local_certified = TRUE` if and only if it stopped at a centre C whose complete coded
neighbourhood was scanned and contains no model with F strictly larger than F(C); `returned` is that C.

The two searches of a final run (`cpp/v3_core.cpp:453-481`):
- **final local search** from the best scored model so far, cap ℓ_n (line 456) → archive `fit$local_search`;
- **LS0** from the start mode S̃₀, cap ℓ_n + |S̃₀| (lines 469-476) → archive `fit$ls0`.

## The reported flag (`v3_run.R:143-149, 174-200`)
- `fit$hpm` = the best model of the whole ledger (all scored models), line 142.
- Status ≠ `completed` ⇒ `local_certified <- FALSE` (line 146). Early returns of `v3_fit.R` keep the initial
  `local_certified = FALSE` (`v3_fit.R:76`).
- Completed run (v3.1, `ls0` on): `cert_final` = final archive certified **and** `hpm` identical to its `returned`
  (line 179); `cert_ls0` = LS0 archive certified **and** `hpm` identical to its `returned` (line 193);
  `local_certified = cert_final || cert_ls0` (line 194); `local_certified_by ∈ {both, final, ls0, none}` (line 195).
- `local_limit = final_local_limit || ls0_local_limit` (line 197): a move cap was hit in either search. It is *not*
  the negation of `local_certified` (e.g. LS0 capped while the HPM is the certified final-search endpoint).
- Enumeration branch (`v3_exact.R:15`): `local_certified = (status == "exact")`; the HPM is then the exact maximiser of
  F over Ω = {|S| ≤ K}, hence has no strictly better neighbour in Ω.

**CC2 (the coded meaning).** `fit$local_certified = TRUE` ⇒ (i) the fit has status `completed` or `exact`, so the
output event 𝒪 holds; (ii) the **reported HPM Ŝ = `fit$hpm`** is *locally optimal*: no model obtained from Ŝ by one
deletion, one addition (when |Ŝ| < K) or one swap has F strictly larger than F(Ŝ). The certificate refers to the
reported model itself: a displaced centre's certificate does not transfer to the HPM (e.g. after an exact-F tie
change), and the top-level flag requires one of the certified archives to return the HPM itself (ruling RULINGS_2 #8,
test `tests/changed_units.R:56-72`).

**CC3 (the archives).** On a completed run, independently of the top-level flag, `fit$local_search$returned` is
locally optimal whenever `fit$local_search$local_certified`, and `fit$ls0$returned` is locally optimal whenever
`fit$ls0$local_certified` (CC1). These are printed too, so the theorem can be stated for every certified endpoint.

**CC4 (cap).** At |C| = K additions are not scanned. Any statement that uses "no improving addition" needs
|Ŝ| ≤ K − 1; the theorem's size condition |Ŝ| ≤ q_n with q_n ≤ K − 1 ensures it.

**CC5 (score).** F(S) = `logprior[|S|]` + `logm(S)` with `logm = logCn − ½(ldH − ldA) − ν log(2b₀ + Q)`
(`cpp/v3_score.h:223`), ν = a₀ + n/2, a₀ = b₀ = 0.01 (`cpp/v3_score.h:14`, `cpp/v3_score.h:57`), `logprior[k] = log w(k) − log W_K`,
`log w(k) = −log 2 − log C(2p−1, k)` (`cpp/v3_score.h:64-70`). X columns and y are standardised with the (n−1) sample SD
(`v3_preprocess.R:37-68, 118-123`), so ‖x_j‖² = n−1 and y′y = n−1. This is the score of
`Theory_work/Wave1C/FINAL/sections/s1_setting.tex:9-13`. The scorer has numerical branches (Q recomputed in a
non-negative form when Q < 1e-8·y′y, `cpp/v3_score.h:218-219`; Cholesky / refactor / QR routes, `cpp/v3_score.h:231-234`);
under EX-A they return the same Q and determinants, so they do not change F.

**CC6 (scanned models reach the ledger; what the archives print).** Every model evaluated in a scan goes through
`eval` (`cpp/v3_engine.h:391`), which emits a ledger event (`v3_engine.h:89-99`); the ledger offers every freshly
scored model to the HPM running best (`cpp/v3_ledger.h:84-95, 99-112`), and a cache hit is a model that this run's
ledger already processed (`v3_ledger.h:96-98`; the final run builds a new cache and ledger together, inherited models
are rescored and offered to this ledger, and final search and LS0 use the same ledger and cache,
`cpp/v3_core.cpp:395-481`). The one non-emitting evaluation is the initial centre of the final search
(`eval(C, …, false)`), which is the current HPM and was therefore already offered. Hence, on a completed run and under EX-A, **F(Ŝ) ≥ F(N) for every N in the coded
neighbourhood of every completely scanned centre** of each search that was run (the final search; LS0 when
enabled, which is the default — with `ls0 = FALSE` there is no `fit$ls0`). Each archive prints its scanned centres with
their scores and completeness flags (`scanned_centres`, `scanned_F`, `scan_complete`; `cpp/v3_core.cpp:351-353`,
`v3_engine.h:407`), its path, and `returned`. When a search stops on its move cap (`termination = "move_limit"`),
`returned` is the best scanned neighbour of the last scanned centre, with strictly larger F (`v3_engine.h:408-410`).

## Numerical confirmation (N0)
`numerics/n0_fidelity.py` on a production fit (iid design, n = 100, p = 400; `numerics/n0_out.txt`): the independent
Python score agrees with the core's F with
a maximum absolute difference of 6.0e-13 over 16,004 core-scored models of sizes 4-8 (after aligning the prior normaliser W_K = Σ_k C(p,k) w(k)); the reported certified HPM is locally optimal under the
independent Python scan of the coded neighbourhood.

## Consequence for the statement
The theorem is stated for **locally optimal models** (LO) of the coded neighbourhood; CC2-CC3 map the printed flags to
LO. Premise EX-A (exact scores and arithmetic) is needed, as in every reported-model theorem of the chapter. No premise
on uniforms, calibration, the start mode or LS0's centre is used: the argument never looks at how the search arrived.
