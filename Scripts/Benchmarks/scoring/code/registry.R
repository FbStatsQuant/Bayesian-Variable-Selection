# registry.R: the closed lists the scoring step checks against (master §III.3.0, §III.3.1–§III.3.8
# item f, §IV.1.2). Written from the master, not from the method code; cross-checked by eye
# against each method's config.R METHODS rows on 2026-10-19 (identical).

# Registered method ids: rule ids and roles in the order of each method's item f.
REGISTRY <- list(
  "F1"         = list(rules = c("cv_min", "cv_1se", "ebic1", "ebic05"), roles = c("primary", "S0", "S0", "S0")),
  "F2"         = list(rules = c("cv_min", "cv_1se", "ebic1", "ebic05"), roles = c("primary", "S0", "S0", "S0")),
  "F3"         = list(rules = c("cv_min", "cv_1se", "ebic1", "ebic05"), roles = c("primary", "S0", "S0", "S0")),
  "F4"         = list(rules = c("ebic1", "ebic05", "bic"),              roles = c("primary", "S0", "S0")),
  "F4_SCAD"    = list(rules = c("ebic1", "ebic05", "bic"),              roles = c("S1", "S1", "S1")),
  "F5"         = list(rules = c("ebic1", "ebic05", "bic"),              roles = c("primary", "S0", "S0")),
  "A1"         = list(rules = c("pip05", "cslead", "bfdr10"),           roles = c("primary", "S0", "S0")),
  "SuSiE-L100" = list(rules = "pip05",                                  roles = "S1"),
  "A2"         = list(rules = "ssl_final",                              roles = "primary"),
  "SSL-RS"     = list(rules = "ssl_final",                              roles = "S1"),
  "A3"         = list(rules = c("ci95", "km2"),                         roles = c("primary", "S0")),
  # PREREG_c050 R4: A1 with refine = TRUE, an S1 arm at both scales (roles mirror A1's primary/S0/S0).
  "SuSiE-refine" = list(rules = c("pip05", "cslead", "bfdr10"),         roles = c("S1", "S0", "S0"))
)

# Derived rules of PREREG_c050 R1 (scoring/derived_rules/derive_rules.R), merged into the runs' rows
# when a derived file is given. Roles as written by the unit.
DERIVED_REGISTRY <- list(
  F1      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F2      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F3      = list(rules = c("ebic1_K37", "ebic05_K37"),                             roles = c("S0", "S0")),
  F4      = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "ebic1_lam005"), roles = c("primary", "S0", "S0", "S0")),
  F4_SCAD = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "ebic1_lam005"), roles = c("S1", "S1", "S1", "S1")),
  F5      = list(rules = c("ebic1_K37", "ebic05_K37", "bic_K37", "sic_smax"),     roles = c("primary", "S0", "S0", "S0")))
K_SIZE_BOUND <- 37L                  # floor(n / log n), PREREG_c050 R1
SIZE_RULE_PATTERN <- "^(ebic|bic|sic)"  # size rules: k_gt_K counted for these in every method
# PREREG_c050 R1: the flag "selected k > K" is counted for every rule of the F families (CV rules too).
F_FAMILY <- c("F1", "F2", "F3", "F4", "F4_SCAD", "F5")

# Label of a rule row in the tables (PREREG_c050 R1 labels).
rule_label <- function(method_id, rule_id, scale_key) {
  if (method_id == "SuSiE-refine")
    return(if (scale_key == "c100") "arm added after the c = 1 results were seen; fit selection by ELBO"
           else "pre-registered arm (PREREG_c050 R4); fit selection by ELBO")
  d <- DERIVED_REGISTRY[[method_id]]
  if (!is.null(d) && rule_id %in% d$rules)
    return(if (scale_key == "c100") "post hoc (chosen from size diagnostics after the c = 1 run)" else "pre-registered (PREREG_c050 R1)")
  "pre-declared"
}

# Registered plus (when present) derived rules of a method, registered first.
rules_of <- function(method_id, with_derived) {
  reg <- REGISTRY[[method_id]]
  d <- DERIVED_REGISTRY[[method_id]]
  if (with_derived && !is.null(d)) list(rules = c(reg$rules, d$rules), roles = c(reg$roles, d$roles)) else reg
}

# Production run folder suffix (`_prod_<method folder>`) -> the method ids that run writes.
RUN_METHODS <- list(
  F1_Lasso = "F1", F2_ElasticNet = "F2", F3_AdaptiveLasso = "F3",
  F4_MCP_SCAD = c("F4", "F4_SCAD"), F5_ABESS = "F5",
  A1_SuSiE = c("A1", "SuSiE-L100"), A2_SSL = c("A2", "SSL-RS"), A3_Horseshoe = "A3",
  SuSiErefine = "SuSiE-refine"
)

# Method ids whose RDS holds a PIP vector (§IV.1.2: A1 and SuSiE-L100 only).
PIP_METHODS <- c("A1", "SuSiE-L100", "SuSiE-refine")

# T1 companion column (§IV.1.3): ebic1 beside the cv_min primary for F1–F3.
T1_COMPANION <- list(F1 = "ebic1", F2 = "ebic1", F3 = "ebic1")

# Closed vocabularies (§III.3.0, §IV.1.2).
STATUS_VALUES   <- c("ok", "warning", "failed", "timeout", "not_run")
FAILED_STATUSES <- c("failed", "timeout", "not_run")
FLAG_CODES <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                "tail_unstable", "fixed_point", "ess_tau", "ess_ci95", "crn_mismatch")
INFO_CODES <- c("lambda_first", "lambda_last", "alpha_edge", "kappa_edge", "floored_selected",
                "ebic_at_largest", "capped_intermediate")
ERROR_TYPES <- c("exact", "extra_only", "missed_only", "mixed", "failed")

# The §IV.1.2 rule-row columns, in the order the runners write them.
BASE_COLUMNS <- c(
  "study", "run_id", "source_sha256",
  "regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id",
  "data_seed", "fold_seed", "method_seed",
  "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
  "method_id", "method_label", "package", "package_version",
  "rule_id", "role", "status",
  "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
  "k", "support", "support_audit",
  "tp", "fp", "fn", "exact", "error_type",
  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null",
  "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc")
TRUTH_COLUMNS <- c("tp", "fp", "fn", "exact", "error_type",
                   sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")

S0_SIZE <- 14L                      # ⌊√200⌋ signals at p = 500 and 1000 (§II.3)
DESIGN_P <- c(500L, 1000L)
DESIGN_SCENARIOS <- 1:6
REPLICATES_PER_CELL <- 100L          # denominator per (p, scenario) cell (§IV.1.3)

# Writes a CSV in which every double column is printed with 17 significant digits ("%.17g", the
# same digits as format(x, digits = 17)), unquoted, so that a reader recovers the exact double.
# write.csv alone prints 15 digits. Character columns are quoted; integers and logicals are not.
write_table <- function(df, path) {
  real <- vapply(df, is.double, TRUE)
  for (cc in names(df)[real]) df[[cc]] <- ifelse(is.na(df[[cc]]), NA_character_, sprintf("%.17g", df[[cc]]))
  quote_cols <- which(vapply(df, is.character, TRUE) & !real)
  utils::write.csv(df, path, row.names = FALSE, na = "NA", quote = if (length(quote_cols)) unname(quote_cols) else FALSE)
}
