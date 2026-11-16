# Raw logs behind WP3_ARCH_REVIEW.md (Owls, 2026-11-16, 3 threads, nice 19)

| file | run |
|---|---|
| `transient_1e6.log` | 10⁶, N = 256, G = 256: stage 1 + 2 burn-in rounds, stopped with a checkpoint (prototype v1, bounded scoring on) |
| `var_ref.log`, `var_bounded.log` | rounds 4–5 resumed from that checkpoint: dense scoring / bounded scoring (prototype v1, commit 88fa644a) |
| `var_v2.log`, `var_v2gram.log`, `var_v2gramfma.log` | the same rounds with the bounded scan and Philox multiply; + Gram rows (600 slots); + FMA products (commit 0c98bea3) |
| `bridge_ref.log`, `bridge_gram.log`, `bridge_gram_leaders.log` | 10⁵, N = 256, adaptive bridge (25 stages + 2 + 2): dense; bounded + Gram rows; the same with leader stores |
| `early1e6_ref.log`, `early1e6_arch1.log`, `early1e6_arch4b.log` | 10⁶, N = 24, stages φ = 0.01, 0.02, 0.03: dense; bounded + Gram rows; the same with 4 flip groups per call |
| `spr_script_dryrun_variant_gram.log` | `tools/nots_bench_arch.sh` dry run at p = 2·10⁴ (script check only) |

Read the `[round]` and `[arch]` lines; round 4 of a resumed run includes one-time allocations, so the tables use round 5.
