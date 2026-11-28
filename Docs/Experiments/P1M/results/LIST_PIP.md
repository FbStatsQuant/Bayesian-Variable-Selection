# List-renormalised PIP fields (HQ order 2026-11-17, SPEC_LIST_PIP; WP4, 2026-11-17)

PR #68 (`exp/P1M-list-pip`, stacked on #65), INTERFACES v0.1.27. Code: `core/v3_run.R` (`v3_list_fields`), `core/v3_fit.R` (exact
branch), `engine_v4/include/v4/list_pip.h` + `src/common/list_pip.cpp` (`compute_list_pip`), `src/post/listpip.cpp` (`smcbvs4 listpip`).

(a) v3's exact branch returns the store at `fit$exact$top` (not `fit$top_store`): `log_Z_list` is computed from it; `pip_list = pip_primary`.
(b) v4: the merged ledger's `top` Store (fit.bin `top_*`): capacity 40p + 1, HPM order, one entry per distinct model, internal 0-based indices.
(c) Post-hoc: yes, from any completed fit.bin (it stores the whole merged `top` and `pip_eq`). MEASURED on Owls (probe merges, random scores):
p = 10^4, fit.bin of the pre-change binary: tool = new merge's fields bit for bit; p = 10^4 and 10^5 (full stores 4.0e5 / 4.0e6): matches_stored;
`listpip` at 10^5: 4.3 s, 332 MB. Merge assembly cost: 0.1 s (10^4), 1.05 s (10^5). The pilot's and T5's fit.bin are on NOTS: not touched.

Acceptance: B4-B11 (v3: tests/list_pip_units.R 88 checks; v4: tests/test_list_pip.cpp + merge e2e), B12 + B10 inside the WP4 golden (540,749 checks,
0 failures; 0 comparisons within 1e-9 of 0.5), A (v4): 42/42 existing fit.bin sections identical to the pre-change binary's on the same files, only
meta differs. A1/A2 (v3, 24 PROD-H + 10 supplementary old core vs new core): `tmp/20261117-listpip/ab/summary.txt` when the runs end (Owls, ~7 h per side).
Note: Owls' LS0 worst-case timing exceeds the PROD-H allocation at p = 1000 (and under load at p = 500): those units are re-run with hours = 48 for both cores.
