# list_pip_ab -- old core vs new core (SPEC_LIST_PIP §7 A1/A2)

The comparator of the list-PIP acceptance: the same fit by the core before the change (`old`) and after it (`new`), for the 24 PROD-H cases, the
10 supplementary units of W3-SCALE and the status paths. `ws_common.R` is W3-SCALE's (theory/W3-SCALE `scripts/ws_common.R`: PROD-H regeneration, the
supplementary units, `ws_strip` = the spec's timing/memory exclusions, the whole-fit fingerprint).

    export AB_GEN_DIR=<repo>/Scripts/Data_generators   # PROD-H data are regenerated; the NOTS input manifest is not available
    run_queue.sh old <old core dir> units.txt <root>    # then, for each of N cores,
    run_queue.sh new <new core dir> units.txt <root>
    Rscript --vanilla summarize.R <root>/out_new <root>/summary.tsv

`units.txt`: lines `prodh:p0500_S1_r001_c050`, `supp:exact_p10`, `stat:resource_limit`, ... For each unit the new run asserts: `identical()` of the whole
fits after the exclusions, equal whole-fit SHA-256 fingerprint, the old fit's field order (`names()`), top-level and per-element attributes, and that the
new fields are the last elements. Old and new cores are plain copies of `Scripts/SMC_BVS/core/` before / after the change (each compiles into its own
`.cpp_cache`).

## v3.1.1 (list fields only on completed final runs)

The old core of this comparison is the v3.1 core (tag `method-v3.1-listpip`, tree 8ff2d876), which already carries the list fields. `ab_run.R new` then
removes the list fields from BOTH fits for the legacy comparison (`identical`, fingerprint, names, attributes) and compares them on their own
(`list_identical`, `whole_order_same`). Expected: completed and exact fits are identical on both counts; status-path fits have identical legacy fields and NO list
field on the new side (the old side had NA + `pip_list_flag = "empty_list"` after a final-run stop, `stat:guard_final`; other status paths never had them).
`AB_RERUN_FILE` applies to every unit kind (`supp:tie_dp_p400` runs at hours = 48).
