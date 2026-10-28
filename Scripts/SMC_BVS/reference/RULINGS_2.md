# Lead's rulings, round 2 (2026-10-22), on the independent verification of Part I (VERIFY_PART_I_r1.md)

Felipe delegated these deployment details to the lead. Apply all of them. Each sourced item cites its source; each ruling is labelled "lead ruling 2026-10-22".

## Gaps

- **G1, preflight (finding 1).**
  - The default allocation is mem_gb = 8, hours = 24 (CORE_SPEC §7). The deployed caller normally passes the job's actual request instead, for example the Slurm --mem and --time.
  - The preflight estimates **memory only**, from quantities known before the run: n, p, K, B, the stores (20p, 40p+1, 500p), the tables, the population N₀ and the cache. Give the formula from the sources and the prototype. Do not adopt the prototype's "50 planned stages / typical size min(K, 10)" wall-time planning assumptions, because they are arbitrary constants.
  - Wall time is instead guarded **while the run goes**: after each stage (pilot, grid or final run), if elapsed time + the duration of the stage just completed > the hours allocation, stop with status `resource_limit` and keep everything produced so far.
  - On the exact branch, the preflight also projects wall time as E × measured s(k), since E is known (M §8.6).
  - Label all of this "lead ruling 2026-10-22: operational guard, not a statistical setting".
- **G2, resampling (finding 2).** The two rules are compatible.
  - Ancestor i is the smallest k with W_k ≥ u_i (CORE_SPEC §4.1), with the N uniforms drawn in stream order.
  - Implement the lookup with a guide (index) table (Chen–Asau inverse-CDF lookup): build it once per resampling, in O(N); each lookup is O(1) expected. This returns exactly the same ancestors as the linear-scan definition, so the result is bit-identical to the prototype.
  - Alias sampling, systematic resampling and any other scheme that changes which ancestor a given u selects are forbidden.
- **G3, φ = 1 rounding (finding 3).**
  - Adopt the verified prototype's RC-2 (ASSUMPTIONS §17) as a labelled numerical convention: a pilot step, or an appended grid point, within 10⁻¹² of 1 is set to exactly 1.
  - After that snap, all the progress and interval checks (v > u, ρ_V ≥ 0.90, etc.) still apply unchanged.
  - Correct the stated reason in Part I. The snap avoids an extra rounding-only stage, which can force too_many_intervals or schedule_limit at T_e in {2000, 4000, 16000}. It bypasses no check.
- **G4, order of random draws (finding 4).** Copy the prototype's consumption order (v3_run.R, variate_order_doc) into §I.4 verbatim in substance:
  - per stage: N resample uniforms; then for particles 1..N, each round: m − 1 order uniforms;
  - then per step type in the drawn order:
    - G: one uniform per coordinate step;
    - U: none when |S| ∈ {0, p}, else uswap_j, uswap_l, uswap_accept;
    - N: none when S is empty, else nswap_j, then (only if N(j)\S is non-empty) nswap_l, nswap_accept;
    - I: the π₀ draw uniforms (in the start sampler's stated order), then indep_accept.
  - Check the exact list in the prototype file, including the Gibbs step, and copy it faithfully. State that this order makes the prototype a bit-level test reference.

## Minor findings: adopt every suggested fix

| # | Topic | Fix |
|---|---|---|
| 5 | Cholesky failure | Rebuild G_S from X_S, then refactor. |
| 6 | Model ordering | Lexicographic with the proper prefix first (R14). |
| 7 | `near_tie_truncated` | Set iff the near-tie store is full and its smallest stored F ≥ best − 10⁻⁹; "within" is inclusive. |
| 8 | `local_certified` | An exact-F tie that changes the reported HPM leaves `local_certified` false. |
| 9 | Exact branch | Setting `local_certified` directly is equivalent to the scan; implementations may skip the scan. |
| 10 | Exact branch | `cut_group` = NA (not applicable; no blocks are used). |
| 11 | Fit record | Add distinct particles and acceptance per mechanism, per stage (CORE_SPEC §6). |
| 12 | Ties | Smaller original index first. |
| 13 | Resampling | A uniform u = 0 is replaced by the smallest positive double, so a zero-weight particle is never selected (prototype convention). |
| 14 | Pilot bisection | Bisect on (φ, 1]; keep the lower end when the midpoint passes; a step is forced iff the bisected step is strictly below 1/T_e. |

Update CHANGES.md (a source column entry "lead ruling 2026-10-22 (RULINGS_2)") and the Revision log. Change nothing else.
