# xeval — cross predictive Hellinger of two law.bin files (eval-only)

`smcbvs4_xeval` is a **separate executable** (target `smcbvs4_xeval`, library `v4_xeval`; `src/xeval/`). It reads two `law.bin`
(the store-BMA laws of `smcbvs4 post`, or the law the eval builds) and the dataset's `truth.json`, and writes
d_H²(f̄_A, f̄_B) = 1 − ∫∫ √(f̄_A f̄_B) dy ν_x(dx): criterion H of the 10⁴ overlap, d_H(V, T)
(`results/overlap1e4/OVERLAP_1e4_PREREG.md` §3.6). The fit binary `smcbvs4` and every fit-side source are untouched; no
`smcbvs4` dispatch line was added.

```
smcbvs4_xeval cross --a V_law.bin --b T_law.bin --truth truth.json --data data.bin --out cross.json \
    --dataset 4-AR-n200-r01 --seed-id 1 --threads 3
smcbvs4_xeval cross --a V_law.bin --b-truth 1 --truth truth.json --out chk.json      # = the engine's d_H(A, f*) (self-check)
tools/xeval/merge_cross.py cross_all.json cross_*_s1.json cross_*_s2.json             # the --cross-file of compare_overlap.py
```

* **Numerics = the eval's** (`dist_metrics`, `predictive`): the same x rows (`make_rows`, rows 0…n_x−1 of the truth's design,
  n_x = 4,000), the same 64-node Gauss–Hermite grid, the same exact top-K (1,000) + stratified-tail estimator of each
  mixture density (8 groups; the group-g tail samples of A and B are paired), eval seed = truth `seed` (low 32 bits) by default.
  The static helpers of `dist.cpp` (comp_at, log_comp, MixAt, Split, tail_sample) are **copied**, not shared, so that
  `dist.cpp` is unchanged; test `xeval_equals_engine_dH_to_truth` asserts that with B = the truth the cross value equals
  the engine's `dist.T.predictive.h2` (and `h2_se_x`, `h2_se_tail`, `h2_topK`) to 1e-12 (measured: bit-equal).
* The GH importance Gaussian is the moment-matched product of the two predictive densities (the eval uses f̄ and f*): symmetric in A, B.
* Two store laws get tail-sample streams 2 and 6 (the engine's T object is 2) assigned by law content hash, so the
  result does not depend on which file is `--a`.
* Guards: the two laws' recorded `inputs.data.bin` hashes must be equal (and equal to `--data`'s), n and p equal.
* Output: `pairs[dataset][seed_id] = {h2, se, se_x, se_tail}` (exactly what `compare_overlap.py` `load_cross` reads; metric
  unchanged) and an `xeval` block (tail masses, dropped masses, `dH_bound_truncation` = √δ_A + √δ_B for the law truncation
  at rel_cut, parameters, wall time), `inputs` hashes and the `binary` block.
* d_H(A, A) is 0 to the quadrature error (measured 2.4e-14 in h2 for a Student mixture, 2.2e-16 for the Gaussian truth), not
  bit-exact: the same GH rule integrates ∫ f̄ dy ≈ 1.
* Cost: per pair ≈ the `predictive` part of one eval object, without KL / draws / test rows (seconds to ~1 min at 3 threads).
