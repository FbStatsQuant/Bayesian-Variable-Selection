# registry.R -- the expected (method, rule, role) registry is DERIVED from the benchmark code at run time, never hand-copied (re-check N1).
# Source of truth: code/bench_lowp/R/config_lowp.R (LOWP_PRODUCTION$<id>$METHODS: rule ids and roles of the primary-tier arm of F1-F5, A1-A3)
# and code/bench_lowp/R/common.R::lowp_derive (the LA-4 / PREREG R1 overlay: K37 and cap rows). lowp_derive is CALLED on a synthetic fit that has
# only the base rule rows, so the derived rule set is exactly the one the benchmark runner emits (no S1 arms, as LA-4).
# Role semantics: primary = the rule that enters H4; S0 = pre-declared sensitivities / K37 companions / LA-4 additions; secondary = cap rows.
BENCH_IDS <- c(paste0("F", 1:5), paste0("A", 1:3))

default_bench_dir <- function() {
  e <- Sys.getenv("SCORING_BENCH_DIR", ""); if (nzchar(e)) return(e)
  file.path(dirname(SC_DIR), "bench_lowp")
}

# returns data.frame(method_id, rule_id, role) of the benchmark rule set (n = 200, p = 20 stand-in; lowp_derive requires K = p <= 30)
derive_bench_rules <- function(bench_dir = default_bench_dir(), p = 20L, n = 200L) {
  cfg <- file.path(bench_dir, "R", "config_lowp.R"); cm <- file.path(bench_dir, "R", "common.R")
  if (!file.exists(cfg) || !file.exists(cm)) stop("benchmark config not found under ", bench_dir)
  env <- new.env(parent = globalenv())
  sys.source(cfg, env); sys.source(cm, env)
  out <- list()
  for (id in BENCH_IDS) {
    M <- env$LOWP_PRODUCTION[[id]]$METHODS
    M <- M[M$method_id == id, , drop = FALSE]
    if (nrow(M) != 1L) stop("benchmark config: expected exactly one primary-tier row for ", id)
    rid <- as.character(unlist(M$rule_ids[[1L]])); rol <- as.character(unlist(M$roles[[1L]]))
    if (length(rid) != length(rol)) stop("benchmark config: rule/role length mismatch for ", id)
    base <- data.frame(rule_id = rid, role = rol, status = "ok", n_warnings = 0L, diag_codes = "", error = NA_character_, support = NA_character_, support_audit = NA_character_, k = NA_integer_,
                       rss = NA_real_, crit_value = NA_real_, lambda = NA_real_, path_index = NA_integer_, k_valid_max = NA_integer_, k_path_max = NA_integer_, stringsAsFactors = FALSE)   # columns lowp_derive touches
    rows <- env$lowp_derive(list(rules = base, diagnostics = NULL), id, p, n, "c100")
    out[[id]] <- data.frame(method_id = id, rule_id = rows$rule_id, role = rows$role, stringsAsFactors = FALSE)
  }
  do.call(rbind, out)
}

# full registry: SMCBVS (hpm primary, pip05 S0), EXACT references, and the derived benchmark rules. All rows required; H4 = role primary (+ SMC pip05, EXACT).
build_registry <- function(bench_dir = default_bench_dir()) {
  b <- derive_bench_rules(bench_dir)
  r <- rbind(data.frame(method_id = c("SMCBVS", "SMCBVS", "EXACT", "EXACT"), rule_id = c("hpm", "pip05", "hpm", "mpm"), role = c("primary", "S0", "reference", "reference"), stringsAsFactors = FALSE), b)
  r$required <- TRUE
  r$in_h4 <- r$role %in% c("primary", "reference") | (r$method_id == "SMCBVS" & r$rule_id == "pip05")
  r
}
