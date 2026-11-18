# PR #11 (WP1 skeleton) — disposition of the independent review (`PR11_review.md`), Engineering manager, 2026-11-15

Verdict: ACCEPT-WITH-FIXES (0 CRITICAL, 1 MAJOR, 11 MINOR). Tests reproduced by the reviewer: 28/28 pass in 24 s.

| # | finding | disposition | owner / when |
|---|---|---|---|
| 1 | MAJOR: per-thread Ledgers each with a full top-(40p+1) store do not fit at 10⁶ (≈ 7 GB per store, measured 724 MB at 4·10⁶) | **ADOPT. Contract change before WP3 codes against it**: per-thread *bounded offer buffers* + **one store per island** (merged at stage ends in a deterministic order) + a shared monotone cut-off (the store's current worst F) for quick rejects. INTERFACES §4 and §7(4) amended by WP1 (v0.1.2); WP3 told now | WP1 (contract) + WP3 (implementation); before merge |
| 2 | MINOR: libm guard not enforced; records lack binary/libm data | ADOPT: every command calls the guard at start and writes the binary/libm block into its manifest; `gen` included | WP1, before merge |
| 3 | MINOR: `prep --from-r` untested; 3 inputs unhashed | ADOPT | WP1, before merge |
| 4 | MINOR: golden tests pass when fixtures are missing | ADOPT: missing fixture = FAIL; bounds checks | WP1, before merge |
| 5 | MINOR: header fields outside every hash; `mode` not in meta | ADOPT: the header (incl. mode) is covered by the content hash | WP1, before merge |
| 6 | MINOR: `compat_stream` accepts unmappable tiers | ADOPT | WP1, before merge |
| 7 | MINOR: contract items marked WP1 not implemented | ADOPT: implement, or re-mark the owner in INTERFACES | WP1, before merge |
| 8 | MINOR: slot rule for the independence move ambiguous | ADOPT: fix the wording in INTERFACES §3 (v0.1.2) | WP1, before merge |
| 9 | MINOR: `prep` statuses exit 0 without data.bin | ADOPT: a distinct exit code + status record | WP1, before merge |
| 10 | MINOR: hash verification cost at 10⁶, done twice per job | DEFER to WP5/G-B: measure at 10⁵; allow a verify-once flag recorded in the manifest | WP5 |
| 11 | MINOR: Reader / load_data robustness | ADOPT | WP1, before merge |
| 12 | MINOR: small items | ADOPT as listed | WP1, before merge |

Merge rule: after WP1 pushes the fixes, a short re-check of items 1–9 and 11–12 (the same reviewer, diff only), then merge
into `exp/P1M-engine`.
