root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/tests"
status <- 1L
tryCatch({
  env <- new.env(parent = globalenv())
  env$quit <- function(status = 0L, ...) {
    if (status != 0L) stop(paste("test runner requested failure exit", status))
    invisible(NULL)
  }
  sys.source(file.path(root, "run_all_tests.R"), envir = env)
  status <- 0L
}, error = function(err) cat("SUITE ERROR:", conditionMessage(err), "\n"))
writeLines(as.character(status), file.path(root, "review1_suite.script_exit"))
if (status != 0L) base::quit(status = status)
