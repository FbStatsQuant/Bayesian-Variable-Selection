a <- commandArgs(TRUE); core <- a[1]; testdir <- a[2]
source(file.path(testdir, "common.R")); load_test_core(core, tempfile("w"), testdir)
cat("formals(v3_fit):", names(formals(v3_fit)), "\n")
forbidden <- c("v3_trace", "v3_step_sample", "v3_round_sample", "v3_resample_sample",
    "v3_replicate_final", "v3_observer_prepare", "v3_observer_report", "v3_pilot_schedule", "v3_reference")
need(!any(vapply(forbidden, exists, TRUE, envir = globalenv(), inherits = FALSE)), "excluded R profiling interface remains")
exports <- ls(.v3cpp)
need(!any(grepl("^cpp_(trace|observer|replicate|step_sample|round_sample|resample_sample|reference)", exports)), "excluded C++ profiling export remains")
need(!("hooks" %in% names(formals(v3_context))), "production scorer hook remains")
need(!("B_override" %in% names(formals(v3_setup))), "production B override remains")
cat("REST OF API UNIT PASSES\n")
