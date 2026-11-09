# R09 — check of the final delta 98fac03..72785fe (R08 test fix; +4096 bytes in the LS0 archive allowance), Codex
gpt-6.1-sol, reasoningEffort high, fresh delegate, read-only. Verbatim reply, received 2026-11-09 ~00:20 CST.

---

**RESOLVED.** The archive checks now read the actual `v3_preflight(...)$memory_components[["ls0_archive"]]`. An in-memory mutation setting the production allowance to zero failed all five checks; the intact implementation passed all five.

- **Estimate reasonable:** it includes measured R archive size, C++ model storage, outer-vector spare capacity, parallel arrays, particles, and 2 KiB for shallow list extensions/names. It is not trivially small: estimated peaks include 318,440 B versus 349,312 B allowed, and 24,718,920 B versus 24,998,432 B allowed.
- **Compatibility preserved:** +4096 applies only to enabled SMC LS0 accounting. Controlled probes confirmed exactly that increment at both tiers and identical records with the charge disabled. The public-fit test reports both compatibility switches retain the shipped preflight.
- **Study sizes:** saved output reports 14 PASS, 0 FAIL; no new refusals for n = 200, p = 500/1000 at 8 GiB / 24 h.

**New findings:** none within the targeted delta.

**Verdict: APPROVE.**
