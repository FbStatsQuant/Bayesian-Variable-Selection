| Finding | Verdict | Reason |
|---|---|---|
| D1-C01 | RESOLVED | §1.2, Table 1 and the disagreements appendix now consistently identify 8 GiB as 8·2³⁰ bytes and distinguish the earlier source’s omission of the time default; this matches [v3_fit.R:28](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/v3_fit.R:28), lines 47, 60 and 73. |
| D1-S01 | RESOLVED | The calibration’s best-model pool now explicitly includes block-table models recorded before the pilot, matching `ingest_tables` at [v3_core.cpp:613](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/cpp/v3_core.cpp:613) and its table offers at lines 372–384. |
| D1-S02 | RESOLVED | The revised paragraph identifies the uninterrupted estimate on calibration success, invokes the full idealising Convention (C3), and states the valid joint-event bound rather than coverage conditional on completion; this matches [Remark 5.22](/home/fb31/BVS-wt/WRITING/Docs/Writing/results/sections/sec5_delivery.tex:432), the estimate definition at lines 385–389, and [Convention (C3)](/home/fb31/BVS-wt/WRITING/Docs/Writing/results/sections/appendices.tex:110), lines 110–122. |
| D1-S03 | RESOLVED | The near-tie description now limits the list to the top-(40p+1) store and identifies its possible truncation and flag, matching [v3_run.R:170](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/v3_run.R:170), lines 170–173. |
| D1-S04 | RESOLVED | The added exception sentence and revised table rows distinguish errors returning nothing from ordinary stop returns, and correctly locate the integer checks after calibration and during the final run; see [v3_fit.R:91](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/v3_fit.R:91), lines 91–94, [v3_run.R:95](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/v3_run.R:95), lines 95–97, and [v3_core.cpp:473](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/cpp/v3_core.cpp:473), lines 473–474 and 483. |
| D1-F01 | RESOLVED | Appendix A now distinguishes the retained per-island top-(40p+1) store from the removed score cache and two 20p leader stores, matching [ENGINEERING_SPEC.md:64](/home/fb31/BVS-wt/WRITING/.rc_tmp/d1_sources/ENGINEERING_SPEC.md:64), lines 141 and 198. |
| D1-E01 | RESOLVED | “Fewer than 10⁶” correctly places the fallback boundary at count ≥10⁶, matching [v3_start.h:290](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/cpp/v3_start.h:290) and line 303. |

New problems introduced by the supplied hunks: none found. All eight hunks match the corresponding current-source ranges. This verdict is limited to these fixes; no full document re-read was performed.

RECHECK: ALL-RESOLVED
