# R04 (Astra, second break review: DESIGN_v1 revision 2) — disposition by the lead, 2026-11-12

Review: `R04_design_astra.md` (Codex gpt-6-astra, reasoningEffort high; blind first read at b2c0194). Verdict:
**UNSOUND** — §4.1 does not meet the O17 ruling and is not a complete build specification. 4 CRITICAL, 5 MAJOR,
1 MINOR; the numerical reconciliation found no wrong number beyond finding 10. All ten are accepted. DESIGN_v1 is
now revision 3. **Revision 3 is not re-reviewed.** Consequence for leg B: B2 (the worker and merge) is **not built**
on this specification; what B2 owed under the ruling — which of the cases (a), (b) holds — is answered in §4.1 and
goes to HQ at CHECKPOINT_2.

| # | severity | finding | disposition in revision 3 |
|---|---|---|---|
| 1 | CRITICAL | `fresh` counts feed published tables and cannot be reconstructed from worker summaries: the shared cache is cleared when full, so freshness depends on the ordered lookup history | Accepted and verified in `evidence_h2.py:98-105,139-141` and `extract_h2.R:42,65,79-80`. §4.1 "Counters": case (a) of O17 fails; case (b) needs an ordered lookup trace replayed through the serial cache rule (about 6 GB at 1k and 15 GB at 2k for the final run). Not built. |
| 2 | CRITICAL | N1 excludes Rao–Blackwellised records; O1(c) claimed N1 covers the shipped RB PIP | Fixed. O1(c) now says N1 does not cover it and names the separate RB identity as needed. |
| 3 | CRITICAL | Leader stores are returned outputs, not calibration-only | Fixed. §4.1 merges both, each under its own comparator. |
| 4 | CRITICAL | "Peak memory independent of R′" is false for an R′-way merge | Fixed. O(c + R′) entries, or O(c) with a running pairwise union. |
| 5 | MAJOR | Tail and distributed status contract under-specified | Fixed as specification: the tail is `v3_core.cpp:453-481` on the merged ledger with both snapshots; §4.1 "Statuses" lists what must be declared. |
| 6 | MAJOR | Worker and stream contracts: ledger slot versus global id, source of N, hashes, census stream range in R | Fixed in §4.1 "Worker" and "Streams". |
| 7 | MAJOR | Variance comparison in §7(ii) not valid in general; scale of the SE | Fixed in §4.3 and §7(ii). |
| 8 | MAJOR | Census inheritance undefined; E₀ is not the delivered-output event; O7/O9/O12 silently dropped | Fixed: §4.5, O1(b), and an "inactive" row in §6. |
| 9 | MAJOR | Three empirical sentences exceeded the data (calibration share, bitset copies, deliverability) | Fixed in §1, §2 item 5 and §8. |
| 10 | MINOR | Scan expression is an upper bound; scan counts unsourced; ratio definition; 134 µs; 934 h | Fixed in §1, §4.1 and §4.4. |

Adopted from the review's "replacement for the next engineering step": first an R′ = 4, unchanged-N, unchanged-primary,
no-census worker-equivalence contract (§4.1), with adversarial checks, before any larger R′.
