# Production-only metadata checks. Source after changed_units.R's existing tests.
# Do not call the production stage-table builder: reconstruct from saved archives
# from THIS invocation (not the worker's different raw calibration experiment).
metadata_moves <- c("gibbs", "gibbs_state_changes", "uswap_exec", "uswap_acc", "uswap_self",
  "nswap_exec", "nswap_acc", "nswap_reject_noscore", "nswap_self", "indep_exec", "indep_acc")

metadata_stage <- function(x, phase, tier, iteration, island, temperatures,
                           rho = NULL, grid_label = NA_character_) {
  need(is.list(x), "missing island stage archive")
  exact(x$phase, phase, "archive/phase")
  exact(x$tier, as.integer(tier), "archive/tier")
  exact(x$iter, as.integer(iteration), "archive/iter")
  exact(x$island, as.integer(island), "archive/island")
  need(is.logical(x$partial) && length(x$partial) == 1L && !is.na(x$partial), "missing partial identity")
  n <- length(x$phi)
  exact(x$phi, temperatures[seq_len(n)], "archive/temperatures")
  if (!x$partial) exact(n, length(temperatures), "archive/completed stage count")
  need(is.data.frame(x$stage_moves), "missing mechanism archive")
  exact(names(x$stage_moves), metadata_moves, "archive/mechanism fields")
  exact(nrow(x$stage_moves), n, "archive/mechanism rows")
  for (nm in c("ess", "log_increment", "cum_log_Z", "distinct_resampled", "distinct_moved"))
    exact(length(x[[nm]]), n, paste0("archive/", nm, "/length"))
  if (!n) return(NULL)
  m <- x$stage_moves
  # Part I I.6: boundary U self-loops are excluded from executions; N's
  # no-score attempts remain included. Gibbs measures changes per Gibbs step.
  counts <- lapply(metadata_moves, function(nm) m[[nm]])
  names(counts) <- metadata_moves
  data.frame(phase = rep(phase, n), tier = rep(as.integer(tier), n),
    iter = rep(as.integer(iteration), n), island = rep(as.integer(island), n),
    grid_label = rep(grid_label, n), partial = rep(x$partial, n), stage = seq_len(n),
    phi = x$phi, rho_V = if (is.null(rho)) rep(NA_real_, n) else rho[seq_len(n)],
    ess = x$ess, log_increment = x$log_increment, cum_log_Z = x$cum_log_Z,
    distinct_resampled = x$distinct_resampled, distinct_moved = x$distinct_moved,
    acc_gibbs_change = m$gibbs_state_changes / pmax(m$gibbs, 1),
    acc_uswap = m$uswap_acc / pmax(m$uswap_exec, 1),
    acc_nswap = m$nswap_acc / pmax(m$nswap_exec, 1),
    acc_indep = m$indep_acc / pmax(m$indep_exec, 1), counts)
}
metadata_bind <- function(rows) {
  rows <- Filter(Negate(is.null), rows)
  if (!length(rows)) return(data.frame())
  z <- do.call(rbind, rows)
  rownames(z) <- NULL
  z
}
metadata_final <- function(saved, source, frozen, settings) {
  # Full archive equality includes all stream fields and double bytes, plus
  # nested counts, terminal diagnostics, timings and attributes copied by R.
  exact(saved$stage_record, source$islands, "final/stage_record")
  islands <- Filter(Negate(is.null), source$islands)
  need(length(islands) > 0L, "no final source islands")
  need(is.list(saved$streams) && length(saved$streams) == length(islands), "missing final stream record")
  exact(saved$streams, lapply(islands, function(x) x$stream), "final/streams")
  rows <- list()
  for (r in seq_along(islands)) {
    x <- islands[[r]]
    need(is.list(x$stream) && length(x$stream) > 0L, "missing raw final stream")
    exact(saved$streams[[r]], x$stream, paste0("final/streams/", r))
    exact(x$stream$stream, as.integer(9L + r), "final/stream identity")
    exact(x$stream$position_start, 0, "final/fresh stream position")
    rows[[r]] <- metadata_stage(x, "final_bridge", settings$tier, -1L, r,
      frozen$grid[-1L], frozen$rho_V, frozen$grid_label %||% NA_character_)
  }
  exact(saved$stage_table, metadata_bind(rows), "final/stage_table")
  TRUE
}
metadata_calibration <- function(saved) {
  need(is.list(saved$tiers) && length(saved$tiers) > 0L, "missing calibration tiers")
  rows <- list()
  for (ti in seq_along(saved$tiers)) {
    tier <- saved$tiers[[ti]]
    need(tier$tier == ti - 1L, "calibration tier order differs")
    need(is.list(tier$pilot), "missing pilot archive")
    rows[[length(rows) + 1L]] <- metadata_stage(tier$pilot$stage_record,
      "pilot", tier$tier, 0L, 0L, tier$pilot$schedule[-1L])
    for (j in seq_along(tier$iterations)) {
      it <- tier$iterations[[j]]
      exact(it$iteration, as.integer(j), "calibration/iteration order")
      need(is.list(it$stage_record) && length(it$stage_record) > 0L, "missing diagnostic islands")
      for (r in seq_along(it$stage_record)) {
        rows[[length(rows) + 1L]] <- metadata_stage(it$stage_record[[r]],
          "diag", tier$tier, it$iteration, r, it$grid[-1L], it$rho_V, it$grid_label)
      }
    }
  }
  # Compare the whole table, not selected rows: missing/duplicate/reordered rows,
  # changed identities, extra columns, types and all dataframe attributes fail.
  exact(saved$stage_table, metadata_bind(rows), "calibration/stage_table")
  TRUE
}
metadata_reject <- function(expr) {
  message <- tryCatch({ force(expr); NULL }, error = function(e) conditionMessage(e))
  need(is.character(message) && length(message) == 1L, "metadata mutation was accepted")
  message
}

add("metadata_final_archives_streams_counts_and_rates_exact", {
  metadata_final(final, raw, fr, ro)
})
add("metadata_calibration_every_archived_stage_exact", {
  # Also validate schedule-limit returns; their attempted tiers remain required.
  metadata_calibration(calibration_full)
})
add("metadata_mutations_reject_missing_or_changed_final_stream", {
  metadata_final(final, raw, fr, ro)
  bad <- final; bad$streams <- bad$streams[-1L]
  missing <- metadata_reject(metadata_final(bad, raw, fr, ro))
  bad <- final; bad$streams[[1L]]$position_end <- .v3cpp$test_adjacent(bad$streams[[1L]]$position_end, TRUE)
  changed <- metadata_reject(metadata_final(bad, raw, fr, ro))
  list(missing = missing, changed = changed)
})
add("metadata_mutations_reject_calibration_diagnostics_and_order", {
  metadata_calibration(calibration_full)
  ix <- which(calibration_full$stage_table$phase == "diag")
  need(length(ix) > 1L, "fixture has no diagnostic stages for mutation")
  bad <- calibration_full
  bad$stage_table$ess[ix[1L]] <- .v3cpp$test_adjacent(bad$stage_table$ess[ix[1L]], TRUE)
  ess <- metadata_reject(metadata_calibration(bad))
  bad <- calibration_full; bad$stage_table$nswap_reject_noscore[ix[1L]] <- bad$stage_table$nswap_reject_noscore[ix[1L]] + 1
  count <- metadata_reject(metadata_calibration(bad))
  bad <- calibration_full
  bad$stage_table[ix[1:2], ] <- bad$stage_table[rev(ix[1:2]), ]
  order <- metadata_reject(metadata_calibration(bad))
  list(ess = ess, count = count, order = order)
})
