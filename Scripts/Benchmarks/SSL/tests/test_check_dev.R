# test_check_dev.R -- tests of the validator check_dev.R on correctly recorded failed fits
# (Sol round 2, findings 1-2): a runner-level error (no native path; A2 with a wrong required
# version) and a capped final point (SSL-RS with max_iter = 1; theta/sigma may be unwritten, so
# the audit may be skipped; a variant with the audit marked as skipped is also checked). Both must satisfy every applicable check except
# settings_match_config, which must flag the altered settings of the SSL-RS fit.
# Usage: Rscript tests/test_check_dev.R --code <dir> --out <dir> --dev_input <rds> --manifest <csv>
a <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
code_dir <- normalizePath(get_arg("code")); out <- get_arg("out")
Sys.setenv(A2_CODE_DIR = code_dir)
source(file.path(code_dir, "run_case.R"))
source(file.path(code_dir, "check_dev.R"))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
hook <- function(s, mid) { if (mid == "A2") s$A2$PKG_VERSION <- "0.0.0" else s$A2$MAX_ITER <- 1L; s }
run_case(get_arg("dev_input"), file.path(out, "results"), "t", method_ids = c("A2", "SSL-RS"),
         manifest = get_arg("manifest"), code_dir = code_dir, settings_hook = hook)
d <- readRDS(get_arg("dev_input"))
man <- utils::read.csv(get_arg("manifest"), stringsAsFactors = FALSE)
man1 <- file.path(out, "manifest_one.csv")
utils::write.csv(man[man$dataset_id == d$dataset_id, ], man1, row.names = FALSE)
res <- check_dev(code_dir, file.path(out, "results", "t"), man1, file.path(out, "check"))
r_a2 <- res[res$method_id == "A2", ]; r_rs <- res[res$method_id == "SSL-RS", ]
others <- setdiff(CHECKS, "settings_match_config")
ok <- c(
  a2_all_pass = isTRUE(r_a2$all_pass),
  a2_path_checks_na = all(is.na(unlist(r_a2[PATH_CHECKS]))),
  a2_contract = isTRUE(r_a2$fit_object_contract),
  rs_settings_flagged = identical(r_rs$settings_match_config, FALSE),
  rs_other_checks_pass = all(unlist(r_rs[others]) %in% TRUE),
  rs_rows_failed = all(utils::read.csv(file.path(out, "results", "t", sprintf("p%04d", d$p), paste0(d$dataset_id, "_c100"), "SSL-RS.csv"))$status == "failed"))
# Skipped-audit branch: the same failed SSL-RS output with theta_L set to NaN and the audit marked
# as not run (as the wrapper records when theta or sigma at the final point was not written);
# the .sha256 file is rewritten so that only the audit branch differs.
case_dir <- file.path(out, "results", "t", sprintf("p%04d", d$p), paste0(d$dataset_id, "_c100"))
r <- readRDS(file.path(case_dir, "SSL-RS.rds"))
r$fit$diagnostics$theta_L <- NaN
r$fit$diagnostics$audit <- list(tolerance = r$fit$diagnostics$audit$tolerance, run = FALSE,
                                tail_keys = r$fit$diagnostics$audit$tail_keys, tail_stable = r$fit$diagnostics$audit$tail_stable)
saveRDS(r, file.path(case_dir, "SSL-RS.rds"), compress = FALSE)
env_c <- new.env(); sys.source(file.path(code_dir, "common.R"), envir = env_c)
writeLines(sprintf("%s  %s", c(env_c$file_sha256(file.path(case_dir, "SSL-RS.rds")), env_c$file_sha256(file.path(case_dir, "SSL-RS.csv"))),
                   c("SSL-RS.rds", "SSL-RS.csv")), file.path(case_dir, "SSL-RS.sha256"))
res2 <- check_dev(code_dir, file.path(out, "results", "t"), man1, file.path(out, "check_skipped_audit"))
r2 <- res2[res2$method_id == "SSL-RS", ]
ok <- c(ok, skipped_audit_row_produced = nrow(r2) == 1L, skipped_audit_fp_error_na = is.na(r2$fp_error),
        skipped_audit_other_checks_pass = all(unlist(r2[others]) %in% TRUE))
print(ok)
cat("fp_error recorded for SSL-RS:", r_rs$fp_error, "\n")
cat(sprintf("test_check_dev: %s\n", if (all(ok)) "PASS" else "FAIL"))
quit(status = if (all(ok)) 0L else 1L)
