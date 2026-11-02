# Local-only harness for the unchanged F1 runner, compatible with glmnet 4.1-10.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
e <- new.env(parent = globalenv())
sys.source(file.path(root, "F1_Lasso", "run_case.R"), e)
e$normalizePath <- function(path, ...) base::normalizePath(path, winslash = "/", ...)
sys.source(file.path(root, "tests", "local_glmnet_compat.R"), envir = globalenv())
orig_settings <- e$load_settings
e$load_settings <- function(code_dir) {
  s <- orig_settings(code_dir)
  s$GLMNET$pkg_version <- as.character(utils::packageVersion("glmnet"))
  s
}
orig_engine <- e$load_engine
e$load_engine <- function(code_dir) {
  eng <- orig_engine(code_dir)
  install_local_glmnet(eng, list(GLMNET = list()))
  eng
}
status <- tryCatch({ e$run_case(e$parse_args(commandArgs(TRUE))); 0L },
                   error = function(err) { message("FATAL: ", conditionMessage(err)); 1L })
quit(save = "no", status = status)
