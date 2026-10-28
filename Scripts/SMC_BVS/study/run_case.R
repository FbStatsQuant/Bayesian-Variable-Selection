#!/usr/bin/env Rscript
# One-call CLI; binding R-1 mapping. --policy accepts only its identical archived copy.
smcbvs_cli_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (args[i] == "--development") { out$development <- TRUE; i <- i + 1L; next }
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad CLI argument: ", args[i])
    key <- gsub("-", "_", substring(args[i], 3L))
    if (!key %in% c("case", "scale", "study", "outroot", "run_id", "policy", "manifest", "core_dir", "mem_gb", "hours")) stop("unknown CLI argument: ", key)
    if (!is.null(out[[key]])) stop("duplicate CLI argument: ", key)
    out[[key]] <- args[i + 1L]; i <- i + 2L
  }
  for (nm in c("case", "scale", "study", "outroot", "run_id"))
    if (is.null(out[[nm]])) stop("missing --", gsub("_", "-", nm))
  out
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
    run_id = a$run_id, policy = policy, allocation = allocation, development = isTRUE(a$development))
  if (!is.null(a$manifest)) call$manifest <- a$manifest
  if (!is.null(a$core_dir)) call$core_dir <- a$core_dir
  result <- do.call(smcbvs_study_fit, call)
  cat(result$prefix, "status=", paste(result$rows$status, collapse = ","),
    "skipped=", result$skipped, "\n")
  if (any(result$rows$status %in% c("failed", "timeout", "not_run"))) 2L else 0L
}
if (sys.nframe() == 0L) {
  code <- tryCatch(smcbvs_cli_main(commandArgs(trailingOnly = TRUE)), error = function(e) {
    message("FATAL: ", conditionMessage(e)); 1L
  })
  quit(save = "no", status = code)
}
