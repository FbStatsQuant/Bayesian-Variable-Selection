#!/usr/bin/env Rscript
# P5 scan (DECISIONS D11), array logic of v2.2.1: lists every SMC-BVS unit of one run and its P5 state.
# Usage: Rscript p5_scan.R --run-dir <OUTROOT>/results/<RUN_ID> --out <file.tsv>
# One row per primary unit with a valid .done (SMCBVS or SMCBVS_rep{m}). A unit is `eligible` for the one P5 rerun
# when its primary ended native resource_limit and its P5_retry/ record is not yet valid. The stop phase (P2
# instrumentation, fit$instrumentation$stop) of the primary and of the rerun is logged. Reads results only (no truth).
# Exit 0 = table written; 1 = error. Prints one summary line (units, resource_limit, eligible, retried, retry outcomes).
p5_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad argument: ", args[i])
    key <- gsub("-", "_", substring(args[i], 3L))
    if (!key %in% c("run_dir", "out")) stop("unknown argument: ", key)
    out[[key]] <- args[i + 1L]; i <- i + 2L
  }
  for (nm in c("run_dir", "out")) if (is.null(out[[nm]])) stop("missing --", gsub("_", "-", nm))
  out
}
p5_main <- function(args) {
  a <- p5_args(args)
  here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])))
  source(file.path(here, "..", "study", "adapter.R"), local = FALSE)   # smcbvs_done_valid, smcbvs_safe_path
  run_dir <- smcbvs_safe_path(a$run_dir)
  stop_text <- function(s) {
    if (!is.list(s)) return(c(where = NA, phase = NA, checkpoint = NA, tier = NA, iter = NA, stage = NA,
      elapsed_seconds = NA, allocation_seconds = NA))
    nm <- c("where", "phase", "checkpoint", "tier", "iter", "stage", "elapsed_seconds", "allocation_seconds")
    setNames(vapply(nm, function(k) { v <- s[[k]]; if (is.null(v) || length(v) != 1L || is.na(v)) NA_character_ else as.character(v) }, ""), nm)
  }
  status_of <- function(prefix, is_retry = FALSE) {
    if (!smcbvs_done_valid(prefix, list())) return(list(valid = FALSE))
    rows <- utils::read.csv(paste0(prefix, ".csv"), colClasses = "character", stringsAsFactors = FALSE)
    v3 <- paste(unique(rows$v3_status), collapse = ",")
    # CONF-2b (Sol F3, both directions; Sol review 2 R2-3): EVERY unit's RDS is read and its record$native_status, the field the
    # P5 rerun itself checks (smcbvs_p5_primary), must be present and equal the CSV v3_status. No fallback to fit$status (an
    # adapter_error record legitimately differs from it): a record without native_status is refused / invalid_inspect.
    rec <- readRDS(paste0(prefix, ".rds"))
    native <- rec$native_status
    if (!identical(v3, as.character(native))) return(list(valid = FALSE, why = sprintf("CSV v3_status (%s) differs from the RDS native status (%s)",
      v3, if (is.null(native)) "absent" else paste(native, collapse = ","))))
    stp <- if (is.list(rec$fit) && is.list(rec$fit$instrumentation)) rec$fit$instrumentation$stop else NULL
    alloc <- rec$allocation
    list(valid = TRUE, v3 = v3, rows = rows, stop = stp, allocation = alloc, rec = rec)
  }
  # CONF-2b (Sol F3): a rerun counts as THIS primary's P5 rerun only if it is bound to it: same run/case/seed/source/policy/
  # inputs as the primary's rows, allocation exactly x2 (and its hash), and record$p5 naming this primary's .sha256 lines.
  id_cols <- c("run_id", "method_id", "case_id", "source_sha256", "method_seed", "adapter_policy_sha256", "input_manifest_sha256",
    "inputs_sha256", "x_sha256", "y_sha256")
  bound_why <- function(prim, ret, primary_prefix) {
    for (nm in id_cols) if (is.null(ret$rows[[nm]]) || is.null(prim$rows[[nm]]) || !identical(ret$rows[[nm]], prim$rows[[nm]]))
      return(paste("identity column differs from the primary:", nm))
    rec <- ret$rec; p5 <- rec$p5; pa <- prim$allocation
    if (is.null(pa)) pa <- readRDS(paste0(primary_prefix, ".rds"))$allocation
    if (!is.list(p5) || !identical(p5$role, "p5_retry") || !identical(p5$factor, 2)) return("record$p5 missing or not a P5 rerun")
    if (!identical(p5$primary$files_sha256, readLines(paste0(primary_prefix, ".sha256"), warn = FALSE))) return("record$p5 names another primary")
    if (!identical(as.character(p5$method_seed), prim$rows$method_seed[1L])) return("record$p5 method seed differs from the primary")
    if (!is.list(rec$allocation) || !identical(rec$allocation$mem_gb, 2 * pa$mem_gb) || !identical(rec$allocation$hours, 2 * pa$hours))
      return("rerun allocation is not exactly twice the primary's")
    if (!identical(rec$allocation_sha256, p5$retry_allocation_sha256) || !all(ret$rows$allocation_sha256 == rec$allocation_sha256))
      return("rerun allocation hash inconsistent")
    ""
  }
  out <- list()
  for (pd in sort(list.dirs(run_dir, recursive = FALSE, full.names = TRUE))) {
    if (!grepl("^p[0-9]{4}$", basename(pd))) next
    for (cd in sort(list.dirs(pd, recursive = FALSE, full.names = TRUE))) {
      for (f in sort(list.files(cd, pattern = "^SMCBVS(_rep[1-5])?\\.done$"))) {
        base <- sub("\\.done$", "", f)
        prim <- status_of(file.path(cd, base))
        if (!prim$valid && !is.null(prim$why)) stop("primary ", file.path(basename(cd), base), ": ", prim$why, " (inspect; scan refused)")
        if (!prim$valid) next
        rp <- file.path(cd, "P5_retry", paste0(base, "_p5retry"))
        # CONF-2b (Sol F7): any artefact of the rerun (rds, csv, sha256, done, lock, temporary files) counts as present
        artefacts <- if (dir.exists(dirname(rp))) list.files(dirname(rp), all.files = TRUE, no.. = TRUE) else character()
        artefacts <- artefacts[startsWith(artefacts, paste0(base, "_p5retry."))]
        retry_present <- length(artefacts) > 0L
        locked <- dir.exists(paste0(rp, ".lock"))
        ret <- if (retry_present) status_of(rp, TRUE) else list(valid = FALSE)
        why <- if (isTRUE(ret$valid)) bound_why(prim, ret, file.path(cd, base)) else if (!is.null(ret$why)) ret$why else ""
        bound <- isTRUE(ret$valid) && !nzchar(why)
        state <- if (bound) "done" else if (isTRUE(ret$valid) || !is.null(ret$why)) "invalid_inspect" else if (locked) "locked" else if (retry_present) "incomplete" else "none"
        ps <- stop_text(prim$stop); rs <- stop_text(ret$stop)
        out[[length(out) + 1L]] <- data.frame(
          case_id = basename(cd), base = base, repeat_m = if (base == "SMCBVS") 0L else as.integer(sub("^SMCBVS_rep", "", base)),
          primary_v3_status = prim$v3, primary_status = paste(prim$rows$status, collapse = ","),
          primary_mem_gb = if (is.null(prim$allocation)) NA_character_ else format(prim$allocation$mem_gb, digits = 17),
          primary_hours = if (is.null(prim$allocation)) NA_character_ else format(prim$allocation$hours, digits = 17),
          primary_stop_where = ps[["where"]], primary_stop_phase = ps[["phase"]], primary_stop_checkpoint = ps[["checkpoint"]],
          primary_stop_tier = ps[["tier"]], primary_stop_iter = ps[["iter"]], primary_stop_stage = ps[["stage"]],
          primary_stop_elapsed_s = ps[["elapsed_seconds"]], primary_stop_allocation_s = ps[["allocation_seconds"]],
          retry_state = state, retry_problem = if (nzchar(why)) why else NA_character_,
          retry_artefacts = if (retry_present) paste(artefacts, collapse = ";") else NA_character_,
          retry_v3_status = if (bound) ret$v3 else NA_character_,
          retry_status = if (bound) paste(ret$rows$status, collapse = ",") else NA_character_,
          retry_stop_where = rs[["where"]], retry_stop_phase = rs[["phase"]], retry_stop_checkpoint = rs[["checkpoint"]],
          # eligible = entitled to its one P5 rerun (resource_limit primary, no bound valid rerun). launchable = eligible AND no rerun
          # artefact at all (state none): only these may be launched now; locked / incomplete / invalid_inspect need an operator.
          eligible = prim$v3 == "resource_limit" && !bound,
          launchable = prim$v3 == "resource_limit" && state == "none",
          stringsAsFactors = FALSE)
      }
    }
  }
  tab <- if (length(out)) do.call(rbind, out) else data.frame()
  tmp <- paste0(a$out, ".tmp.", Sys.getpid())
  utils::write.table(tab, tmp, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
  if (!file.rename(tmp, a$out)) stop("could not write ", a$out)
  n <- nrow(tab)
  rl <- if (n) sum(tab$primary_v3_status == "resource_limit") else 0L
  el <- if (n) sum(tab$eligible) else 0L
  done <- if (n) tab[tab$retry_state == "done", , drop = FALSE] else tab
  outcomes <- if (nrow(done)) paste(names(table(done$retry_v3_status)), table(done$retry_v3_status), sep = ":", collapse = ",") else "none"
  cnt <- function(st) if (n) sum(tab$retry_state %in% st) else 0L
  # the first six fields keep their v2.2.1 order (parsed by the pilot); launchable/locked/invalid_inspect are appended
  cat(sprintf("p5_scan units=%d primary_resource_limit=%d eligible=%d retried=%d retry_outcomes=%s incomplete=%d launchable=%d locked=%d invalid_inspect=%d\n",
    n, rl, el, nrow(done), outcomes, cnt("incomplete"), if (n) sum(tab$launchable) else 0L, cnt("locked"), cnt("invalid_inspect")))
  0L
}
if (sys.nframe() == 0L) {
  code <- tryCatch(p5_main(commandArgs(trailingOnly = TRUE)), error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = code)
}
