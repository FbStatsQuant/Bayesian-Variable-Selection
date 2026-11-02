#!/usr/bin/env Rscript
# One-call CLI; binding R-1 mapping. --policy accepts only its identical archived copy.
# v2.2.1: both regimes (ids p0500/p1000 = H, p0020/p0030 = L); --repeat m (m = 1..5, regime L only): method seed
# = data seed + 4,000,000 + 1,000*m, output basename SMCBVS_rep{m}. --p5-retry (DECISIONS D11): rerun a unit whose
# primary record ended resource_limit, same seed, with double the allocation given by --mem-gb/--hours (pass the
# PRIMARY allocation); written to <case>/P5_retry/{SMCBVS|SMCBVS_rep{m}}_p5retry.*. The last stdout line is
# tab-separated key=value fields, including the stop phase of a resource_limit fit (P2 instrumentation).
smcbvs_cli_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (args[i] %in% c("--development", "--p5-retry")) {
      key <- gsub("-", "_", substring(args[i], 3L))
      if (!is.null(out[[key]])) stop("duplicate CLI argument: ", key)
      out[[key]] <- TRUE; i <- i + 1L; next
    }
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad CLI argument: ", args[i])
    key <- gsub("-", "_", substring(args[i], 3L))
    if (!key %in% c("case", "scale", "study", "outroot", "run_id", "policy", "manifest", "core_dir", "mem_gb", "hours", "repeat")) stop("unknown CLI argument: ", key)
    if (!is.null(out[[key]])) stop("duplicate CLI argument: ", key)
    out[[key]] <- args[i + 1L]; i <- i + 2L
  }
  for (nm in c("case", "scale", "study", "outroot", "run_id"))
    if (is.null(out[[nm]])) stop("missing --", gsub("_", "-", nm))
  out
}
smcbvs_cli_stop_text <- function(stop) {
  if (!is.list(stop)) return("NA")
  v <- vapply(c("where", "phase", "checkpoint", "tier", "iter", "stage"), function(nm)
    if (is.null(stop[[nm]]) || length(stop[[nm]]) != 1L || is.na(stop[[nm]])) "NA" else as.character(stop[[nm]]), "")
  paste(v, collapse = "/")
}
smcbvs_cli_main <- function(args) {
  a <- smcbvs_cli_args(args)
  path <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
  source(file.path(dirname(normalizePath(path)), "adapter.R"), local = FALSE)
  policy <- if (is.null(a$policy)) smcbvs_r1_policy() else readRDS(smcbvs_safe_path(a$policy))
  allocation <- list(mem_gb = if (is.null(a$mem_gb)) 8 else as.numeric(a$mem_gb),
    hours = if (is.null(a$hours)) 24 else as.numeric(a$hours))
  if (any(!is.finite(unlist(allocation))) || any(unlist(allocation) <= 0)) stop("allocation must be positive finite numbers")
  call <- list(case = a$case, scale = a$scale, study = a$study, outroot = a$outroot,
    run_id = a$run_id, policy = policy, allocation = allocation, development = isTRUE(a$development),
    p5_retry = isTRUE(a$p5_retry))
  if (!is.null(a[["repeat"]])) {
    m <- suppressWarnings(as.numeric(a[["repeat"]]))
    if (is.na(m) || m != as.integer(m) || !m %in% 1:5) stop("--repeat must be an integer in 1..5")
    call$repeat_m <- as.integer(m)
  }
  if (!is.null(a$manifest)) call$manifest <- a$manifest
  if (!is.null(a$core_dir)) call$core_dir <- a$core_dir
  result <- do.call(smcbvs_study_fit, call)
  v3 <- if (is.null(result$native_status)) paste(unique(result$rows$v3_status), collapse = ",") else result$native_status
  cat(result$prefix, "status=", paste(result$rows$status, collapse = ","),
    "skipped=", result$skipped, "\n")
  cat(paste0(c("prefix", "skipped", "p5_retry", "v3_status", "stop"), "=",
    c(result$prefix, result$skipped, isTRUE(a$p5_retry), v3, smcbvs_cli_stop_text(result$stop)), collapse = "\t"), "\n", sep = "")
  if (any(result$rows$status %in% c("failed", "timeout", "not_run"))) 2L else 0L
}
if (sys.nframe() == 0L) {
  code <- tryCatch(smcbvs_cli_main(commandArgs(trailingOnly = TRUE)), error = function(e) {
    message("FATAL: ", conditionMessage(e)); 1L
  })
  quit(save = "no", status = code)
}
