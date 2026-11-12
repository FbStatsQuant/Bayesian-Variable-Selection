# W3-START2 — CHECKPOINT 1 (target fixed) — 2026-11-12

Lead: Claude Fable 5.2, effort high. No git state changed. **Nothing is proved or checked yet.**

**Locked: `STATEMENT.md` v1.4.1** — a delta on W3-START v1.3.4 with all four BT2 improvements:
* P1: for s₀ ≥ 1 the leading functional loses its 15√(2/π)z_n/p term; F2 needs no growth condition on p.
* P2: OVL under (V-m) or (V-c).
* P3: leaking-null limit with 17 − s₀ nulls for 1 ≤ s₀ ≤ 15.
* P4: (T3)(b) for any |Q| ≤ K.

| round | seat | verdict | file |
|---|---|---|---|
| SL1 | Sol, blind | LOCK WITH CHANGES: 4 minor, 2 optional; all applied | `reviews/SL1_statement_lock_sol.md`, `SL1_disposition.md` |
| SC1 | Sol, diff check | LOCKED: editorial only, all resolved | `reviews/SC1_diff_check_sol.md` |

`manifest.py verify` passes on MANIFEST_SC1 (d09644f5…). No holds.

Unreviewed drafts of the four proof files are in `reviews/drafts_CP2/`, outside the frozen tree.

**Next (CP2/final):** move the drafts to `lemmas/`, citecheck, two Sol line checks, REPORT with registry block, council (Sol + Opus) on one manifest.

**For HQ:** the consumed W3-START claims are not registry rows yet; acceptance of this ticket waits on that.
