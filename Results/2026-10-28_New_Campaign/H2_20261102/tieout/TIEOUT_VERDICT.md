# ANALYSIS-H2 tie-out verdict: PASS

**Worker:** Terra 6.1 (codex, high), working from the raw records with its own code (`terra_code/`).
- Attempt 1 did nothing: Terra looked for the files on a remote host.
- Attempt 2 ran locally and finished 2026-11-02 ~16:00Z.

**Claims:** `CLAIMS.csv`, 51 cells = 46 genuine + 5 planted canaries. The key (`CANARY_KEY.json`) was held outside Terra's paths until it reported.

**Cells covered:**
- SMC recovery: HPM, RB-MPM and plain-MPM.
- Lasso and elastic-net `ebic1_K37`.
- Reproduction counts, old vs new records.
- Stops and escalation.
- Registry mode.
- Local-search moves and HPM provenance.
- RB vs plain PIP agreement.
- Miss shapes.
- Search misses (F(S₀) > F(HPM), via the scorer).
- S₀ strict local maximum (clause c), via Terra's own move enumeration.
- π₀(R₁), as an execution check.

**Result:**

| | count |
|---|---|
| Genuine cells matching | 46/46 |
| Canaries detected | 5/5 |

Each canary was recomputed to its true value:

| Cell | Planted | Recomputed = true |
|---|---|---|
| 5 | 65 | 67 |
| 25 | 2397 | 2400 |
| 37 | 0.01 | 0.0067 |
| 41 | 35 | 32 |
| 42 | 2 | 0 |

No data problems were found. Details: `TIEOUT_REPORT.md` and `TIEOUT_RESULT.csv`.

**Manager's process note:** the first claims draft computed 0 for the miss-shape cells 38–41, because of a pandas `.shape` attribute clash. The manager caught it and fixed it before Terra saw any claims. The analysis tables themselves were unaffected.
