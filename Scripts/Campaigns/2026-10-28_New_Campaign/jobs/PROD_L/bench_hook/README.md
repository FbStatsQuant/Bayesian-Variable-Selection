# Later benchmark wave

Benchmarks are not included in PROD-L. The driver refuses `bench`: BENCH-FIX (b), Sol ACCEPT (D42.7), and re-sizing for revised F3 are required first. A future bundle adds 96 tasks of 25 cases, 1 CPU, 1 GiB, 1 hour, throttled at 32 alone or 16 with PROD-H. It uses `<STAMP>_lowp_bench`, the same stamp and stage if available, otherwise a fresh stage. Submit it as a separate wave only after the smcrep lane is terminal, through the same truth-lock chain and ceiling check. See DESIGN §10 and sizing §4.

**Disclosed limitation (HQ D54.3, added by BENCH-FIX):** the F5 (ABESS) low-p exact best-subset check is DEFERRED and is not a gate for this wave; the enumerator does not save per-size minimum-RSS supports. See `code/bench_lowp/ADAPTATIONS.md`. The benchmark code for this wave is the post-BENCH-FIX `code/bench_lowp/` (manifest in `code/bench_v2/lowp_port/`; see `code/CODE_LEDGER.md`).
