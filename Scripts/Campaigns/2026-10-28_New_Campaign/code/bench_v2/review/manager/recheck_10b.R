# Manager recheck of F1 legacy test 10b (runner end to end, inputs-only tree, idempotent rerun).
# Compares the runner output with the controlled-snapshot in-process F1 v2 fit of the same case.
Sys.setenv(OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1", MKL_NUM_THREADS = "1",
           BENCH_V2_LOCAL_TEST = "1", BENCH_LIB = "C:/Users/felip/AppData/Local/R/win-library/4.4")
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
src <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S4_r001.rds"
tmp <- file.path(root, "review", "manager", paste0("tmp_10b_", format(Sys.time(), "%Y%m%dT%H%M%S")))
if (dir.exists(tmp)) stop("stale tmp dir exists: ", tmp)
dir.create(file.path(tmp, "inputs", "p0500"), recursive = TRUE)
stopifnot(file.copy(src, file.path(tmp, "inputs", "p0500")))
stopifnot(!dir.exists(file.path(tmp, "truth")))
runner <- file.path(root, "tests", "run_local_f1_runner.R")
cmd <- c("--vanilla", runner, "--code-dir", file.path(root, "F1_Lasso"),
         "--input", file.path(tmp, "inputs", "p0500", basename(src)), "--scale", "c100",
         "--out-root", file.path(tmp, "out"), "--run-id", "unit_no_oracle",
         "--lib", "C:/Users/felip/AppData/Local/R/win-library/4.4")
rs <- file.path(R.home("bin"), "Rscript")
rc <- suppressWarnings(system2(rs, shQuote(cmd), stdout = TRUE, stderr = TRUE))
st <- attr(rc, "status"); cat("run 1 status:", if (is.null(st)) 0L else st, "\n"); cat(rc, sep = "\n")
if (!is.null(st) && st != 0) stop("runner failed")
od <- file.path(tmp, "out", "results", "unit_no_oracle", "p0500", "dev_p0500_S4_r001_c100")
f <- file.path(od, paste0("F1", c(".rds", ".csv", ".sha256", ".done")))
stopifnot(all(file.exists(f)))
csv <- read.csv(f[2], stringsAsFactors = FALSE, colClasses = c(support = "character"))
obj <- readRDS(f[1])
ref <- readRDS(file.path(root, "repro", "controlled_2a8362b2f348", "dev_p0500_S4_r001_c100.rds"))
new <- ref$F1$new$result
checks <- c(
  six_rows = nrow(csv) == 6L,
  rule_ids = identical(csv$rule_id, as.character(new$rules$rule_id)),
  no_failed = !any(csv$status == "failed"),
  schema_v2 = identical(obj$schema_version, 2L),
  support_eq_ref = identical(csv$support, as.character(new$rules$support)),
  beta_eq_ref = identical(obj$beta, new$beta),
  coef_present = identical(names(obj$coefficients), as.character(new$rules$rule_id)),
  coef_eq_ref = identical(lapply(obj$coefficients, `[[`, "beta_pen"), lapply(new$coefficients, `[[`, "beta_pen")))
h0 <- tools::md5sum(f)
rc2 <- suppressWarnings(system2(rs, shQuote(cmd), stdout = TRUE, stderr = TRUE))
st2 <- attr(rc2, "status")
checks <- c(checks, rerun_ok = is.null(st2) || st2 == 0L,
            rerun_skipped = any(grepl("skip", rc2)), rerun_bytes_same = identical(h0, tools::md5sum(f)))
print(checks)
cat("RESULT:", if (all(checks)) "PASS" else "FAIL", "\n")
writeLines(if (all(checks)) "0" else "1", file.path(root, "review", "manager", "recheck_10b.script_exit"))
quit(save = "no", status = if (all(checks)) 0L else 1L)
