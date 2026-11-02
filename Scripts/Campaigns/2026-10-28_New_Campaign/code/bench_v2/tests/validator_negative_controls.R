root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
code <- file.path(root, "F3_AdaptiveLasso")
prefix <- file.path(root, "tests", "runner_output", "results", "v2_local_e2e", "p0500", "dev_p0500_S1_r001_c100", "F3")
rds <- readRDS(paste0(prefix, ".rds"))
rows <- read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE, na.strings = "NA",
  colClasses = c(support = "character", support_audit = "character", diag_codes = "character"))
cfg <- new.env(); sys.source(file.path(code, "config.R"), cfg)
engine <- new.env(parent = asNamespace("stats")); sys.source(file.path(code, "common.R"), engine)
validator <- new.env(); sys.source(file.path(code, "tests", "validate_outputs.R"), validator)
settings <- cfg$study_settings()
stopifnot(length(validator$validate_payload(rds, rows, settings, engine)) == 0L)
for (fault in c("schema", "id", "role", "extra", "coefficient", "metadata", "support", "retired", "code")) {
  bad <- rds; rr <- rows
  if (fault == "schema") bad$schema_version <- 1L
  if (fault == "id") rr$rule_id[1] <- "bogus"
  if (fault == "role") rr$role[1] <- "S0"
  if (fault == "extra") rr$pilot_k <- NULL
  if (fault == "coefficient") bad$coefficients[[1]]$beta_pen <- numeric()
  if (fault == "metadata") bad$coefficients[[1]]$index <- -999L
  if (fault == "support") rr$support[1] <- "999"
  if (fault == "retired") bad$fit$diagnostics$ridge <- TRUE
  if (fault == "code") rr$diag_codes[1] <- "kappa_edge"
  errors <- validator$validate_payload(bad, rr, settings, engine)
  cat(fault, if (length(errors)) "rejected" else "NOT REJECTED", paste(errors, collapse="; "), "\n")
  if (!length(errors)) stop("validator missed ", fault)
}
