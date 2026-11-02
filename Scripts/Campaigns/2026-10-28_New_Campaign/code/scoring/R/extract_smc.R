# extract_smc.R -- the ONLY place that knows native SMC-BVS field names.
# Input: one study-adapter record (INTERFACES I3 / study SCHEMA.md; RDS envelope with $fit = native return).
# Output: a flat list of normalised fields; absent fields are NA (scalars) or NULL (vectors/tables).
#
# FIELD_MAP: name | candidate paths (tried in order, first non-NULL wins) | status | meaning
#   status "code"        = verified by reading the v2.2 core / adapter source (field exists in the fit object)
#   status "provisional" = name guessed; replace when conformance/OUTPUT_FIELDS.md exists
FIELD_MAP <- data.frame(stringsAsFactors = FALSE,
  name = c(
    "native_status", "estimates_available", "runtime_s", "method_seed",
    "log_Z", "log_Z_r", "log_Z_lower95", "log_Z_rel_m0", "log_m0",
    "pip_primary_full", "pip_primary_retained", "pip_r", "mpm", "hpm", "hpm_F",
    "pip_plain_full", "pip_plain_retained", "pip_plain_r", "mpm_plain",
    "kept",
    "flag_escalated", "flag_checks_passed_final", "flag_E1", "flag_E2", "flag_E3", "flag_low_ess",
    "flag_local_limit", "flag_grid_unconverged", "flag_near_tie_truncated", "flag_cut_group", "flag_local_certified",
    "stage_table", "score_fresh", "score_logical", "tier", "n_stages_final", "blocks",
    "log_mass_scored", "n_distinct_scored", "scored_set", "truth_trace"),
  paths = c(
    "native_status|fit$status", "estimates_available|fit$estimates_available", "runtime_s", "case$method_seed|fit$seed",
    "fit$log_Z", "fit$log_Z_r", "fit$log_Z_lower95", "fit$log_Z_rel_m0", "fit$log_m0",
    "pip|pip_primary_original", "fit$pip_primary", "fit$pip_r", "fit$mpm|mpm", "fit$hpm|hpm", "fit$hpm_F",
    "pip_plain", "fit$pip_plain", "fit$pip_plain_r", "mpm_plain|fit$mpm_plain",
    "fit$preprocessing$kept",
    "fit$flags$escalated", "fit$flags$checks_passed_final", "fit$flags$E1", "fit$flags$E2", "fit$flags$E3", "fit$flags$low_empirical_ESS",
    "fit$flags$local_limit|fit$local_limit", "fit$flags$grid_unconverged", "fit$flags$near_tie_truncated", "fit$flags$cut_group|fit$cut_group", "fit$local_certified",
    "fit$stage_table", "fit$score_counts$fresh", "fit$score_counts$logical", "fit$settings$tier", "instrumentation$stages$final|fit$instrumentation$stages$final", "fit$blocks",
    "instrumentation$scored$log_sum_exp_F|fit$instrumentation$scored$log_sum_exp_F|fit$log_mass_scored",
    "instrumentation$scored$n_distinct|fit$instrumentation$scored$n_distinct",
    "instrumentation$scored_set|fit$instrumentation$scored_set",
    "instrumentation$truth_trace|fit$instrumentation$truth_trace|fit$truth_trace"),
  status = c(
    "code", "code", "code", "code",
    "code", "code", "code", "code", "code",
    "code", "code", "code", "code", "code", "code",
    "code", "code", "code", "code",
    "code",
    "code", "code", "code", "code", "code", "code",
    "code", "code", "code", "code", "code",
    "code", "code", "code", "code", "code", "code",
    "code (v2.2 registry; name of the derived scalar log_mass_scored is provisional)", "code (v2.2 registry)", "code (v2.2 registry)", "provisional"),
  note = c(
    "adapter native_status (completed/exact/failure statuses)", "logical", "wall seconds around the core call", "data seed + 4e6 (+1000 m for repeat m)",
    "pooled log Z-hat, full working scale", "4 island log Z-hat_r", "native log(0.05)+log_Z", "relative to m(empty)", "log m(empty)",
    "record$pip: length-p vector, zeros for dropped columns", "retained-column named vector (names = original index)", "retained-p x R matrix, rownames = original index",
    "strict PIP > 1/2 on the RB PIP", "sorted original-index support", "F of the HPM",
    "plain (non-Rao-Blackwellised) PIP, length-p; NA for exact fits", "retained vector", "retained-p x R matrix", "plain-PIP MPM",
    "retained original indices",
    "tier 1 used", "FALSE = a final check failed", "final E1", "final E2", "final E3", "any final-stage ESS < 0.5 N_e",
    "local search hit its move cap", "calibration grid not converged", "near-tie store truncated", "a correlated group spans >= 2 blocks", "returned HPM is a scanned centre with no improving neighbour",
    "phase,tier,iter,island,...,ess,... (final rows phase == 'final_bridge')", "mechanism matrix of fresh scores (final ledger)", "mechanism matrix of logical scores (final ledger)", "final tier", "number of final bridge stages", "packed blocks (original indices)",
    "log sum over DISTINCT scored S of exp F(S) (v2.2 registry, exact mode p <= 64); = log_mass_scored", "distinct scored models", "data.frame key (bitmask over retained positions), size, first_phase, first_mech, first_tier, first_iter, first_island, first_stage (p <= 32)",
    "PROVISIONAL: in-fit trace of the truth model if the sibling thread adds one: list(scored, first_phase, first_mech, ...). Truth never enters fits, so by default scoring derives it from scored_set."))

fm_get <- function(record, name) {
  row <- FIELD_MAP[FIELD_MAP$name == name, , drop = FALSE]
  if (!nrow(row)) stop("unknown field-map name: ", name)
  for (pth in strsplit(row$paths, "|", fixed = TRUE)[[1L]]) {
    v <- get_path(record, pth)
    if (!is.null(v)) return(v)
  }
  NULL
}

# ---- validation helpers (review finding 8): never manufacture values from incomplete fields --------------------------------------------
valid_prob_vec <- function(v, n = NULL) is.numeric(v) && (is.null(n) || length(v) == n) && length(v) > 0L && all(is.finite(v)) && all(v >= -1e-9 & v <= 1 + 1e-9)

# Full-length vector (adapter record$pip): canonical original-index order (a named permutation of 1..p is reordered; duplicate / unknown names are
# rejected), valid probabilities, and the confirmed dropped columns (not in `kept`) must be 0.
canon_full_vec <- function(v, p, kept = NULL) {
  if (!valid_prob_vec(v, p)) return(NULL)
  nm <- names(v)
  if (!is.null(nm)) {
    idx <- suppressWarnings(as.integer(nm))
    if (anyNA(idx) || anyDuplicated(idx) || !setequal(idx, seq_len(p))) return(NULL)
    v <- v[order(idx)]
  }
  names(v) <- as.character(seq_len(p))
  if (!is.null(kept)) { dr <- setdiff(seq_len(p), as.integer(kept)); if (length(dr) && any(abs(v[dr]) > 1e-12)) return(NULL) }
  v
}

# Retained-column vector (names = original index) -> length-p vector. The names must cover EXACTLY `kept` (confirmed dropped columns get 0);
# without a kept map only a full-length vector (names 1..p or unnamed) is accepted. Returns NULL when the field cannot be trusted.
expand_pip <- function(v, p, kept = NULL) {
  if (is.null(v) || !is.numeric(v) || !length(v) || !all(is.finite(v))) return(NULL)
  nm <- names(v)
  if (is.null(nm)) {
    if (length(v) != p) return(NULL)
    out <- setNames(as.numeric(v), as.character(seq_len(p)))
  } else {
    idx <- suppressWarnings(as.integer(nm))
    if (anyNA(idx) || anyDuplicated(idx) || any(idx < 1L | idx > p)) return(NULL)
    kp <- if (is.null(kept)) { if (length(v) == p) seq_len(p) else return(NULL) } else as.integer(kept)
    if (!setequal(idx, kp)) return(NULL)
    out <- setNames(rep(0, p), as.character(seq_len(p))); out[as.character(idx)] <- as.numeric(v)
  }
  if (!valid_prob_vec(out, p)) return(NULL)
  out
}
expand_pip_matrix <- function(M, p, kept = NULL, R = 4L) {
  if (is.null(M)) return(NULL)
  M <- as.matrix(M)
  if (!is.numeric(M) || ncol(M) != R || !all(is.finite(M)) || any(M < -1e-9 | M > 1 + 1e-9)) return(NULL)
  rn <- rownames(M)
  if (is.null(rn)) {
    if (nrow(M) != p) return(NULL)
    out <- M; dimnames(out) <- list(as.character(seq_len(p)), NULL); return(out)
  }
  idx <- suppressWarnings(as.integer(rn))
  if (anyNA(idx) || anyDuplicated(idx) || any(idx < 1L | idx > p)) return(NULL)
  kp <- if (is.null(kept)) { if (nrow(M) == p) seq_len(p) else return(NULL) } else as.integer(kept)
  if (!setequal(idx, kp)) return(NULL)
  out <- matrix(0, p, R, dimnames = list(as.character(seq_len(p)), NULL)); out[as.character(idx), ] <- M
  out
}
scalar_or_na <- function(v, type = "numeric") {
  if (is.null(v) || length(v) != 1L) return(if (type == "logical") NA else NA_real_)
  if (type == "logical") as.logical(v) else as.numeric(v)
}
sum_or_na <- function(x) if (is.null(x) || !length(x) || all(is.na(x))) NA_real_ else sum(x, na.rm = TRUE)

extract_smc <- function(record, rep = 0L) {
  cs <- record$case %||% list()
  p <- as.integer(cs$p %||% record$rows$p[1L] %||% length(record$pip))
  st <- as.character(fm_get(record, "native_status") %||% NA_character_)[1L]
  ea <- fm_get(record, "estimates_available")
  ok <- isTRUE(ea) && st %in% c("completed", "exact")
  kept <- fm_get(record, "kept"); kept <- if (is.null(kept)) NULL else as.integer(kept)
  # --- PIPs: the adapter's full-length vector if valid, else the native retained vector expanded through `kept`
  pip_full <- canon_full_vec(fm_get(record, "pip_primary_full"), p, kept); if (is.null(pip_full)) pip_full <- expand_pip(fm_get(record, "pip_primary_retained"), p, kept)
  plain_full <- canon_full_vec(fm_get(record, "pip_plain_full"), p, kept); if (is.null(plain_full)) plain_full <- expand_pip(fm_get(record, "pip_plain_retained"), p, kept)
  pip_r <- expand_pip_matrix(fm_get(record, "pip_r"), p, kept); plain_r <- expand_pip_matrix(fm_get(record, "pip_plain_r"), p, kept)
  if (!is.null(pip_full) && is.null(names(pip_full))) names(pip_full) <- as.character(seq_len(p))
  # --- evidence: four finite islands and a finite pooled value, else unavailable (the HPM may still be valid)
  logZ <- scalar_or_na(fm_get(record, "log_Z")); logZr <- fm_get(record, "log_Z_r"); logZr <- if (is.null(logZr)) numeric(0) else as.numeric(logZr)
  # pooled evidence: finite log Z; for a completed SMC fit it needs four finite islands, the native exact branch has no islands (evidence is exact).
  # Island quantities (per-island errors, SE) need four finite islands and are unavailable on the exact branch.
  islands_ok <- ok && is.finite(logZ) && length(logZr) == 4L && all(is.finite(logZr))
  evidence_ok <- ok && is.finite(logZ) && (identical(st, "exact") || islands_ok)
  hpm <- fm_get(record, "hpm"); hpm <- if (is.null(hpm)) NULL else sort(as.integer(hpm))
  mpm <- fm_get(record, "mpm"); mpm <- if (is.null(mpm)) NULL else sort(as.integer(mpm))
  mpm_plain <- fm_get(record, "mpm_plain"); mpm_plain <- if (is.null(mpm_plain)) NULL else sort(as.integer(mpm_plain))
  if (is.null(mpm) && !is.null(pip_full) && ok) mpm <- as.integer(which(pip_full > 0.5))
  if (is.null(mpm_plain) && !is.null(plain_full) && ok) mpm_plain <- as.integer(which(plain_full > 0.5))
  # --- stage table: FINAL rows only (no fallback to calibration rows)
  stt <- fm_get(record, "stage_table"); min_ess <- NA_real_; nst <- fm_get(record, "n_stages_final")
  if (is.data.frame(stt) && nrow(stt) && "phase" %in% names(stt)) {
    fin <- stt[stt$phase == "final_bridge", , drop = FALSE]
    if (nrow(fin)) {
      if ("ess" %in% names(fin) && any(is.finite(fin$ess))) min_ess <- min(fin$ess[is.finite(fin$ess)])
      if ((is.null(nst) || length(nst) != 1L || is.na(nst)) && "island" %in% names(fin)) nst <- max(table(fin$island))
    }
  }
  nst <- if (is.null(nst) || length(nst) != 1L) NA_real_ else as.numeric(nst)
  fresh <- fm_get(record, "score_fresh"); logical_s <- fm_get(record, "score_logical")
  list(
    case_id = cs$case_id %||% record$rows$case_id[1L], dataset_id = cs$dataset_id %||% record$rows$dataset_id[1L],
    p = p, scenario = as.integer(cs$scenario %||% NA), replicate = as.integer(cs$replicate %||% NA), scale_key = cs$scale_key %||% NA_character_,
    rep = as.integer(rep), method_seed = scalar_or_na(cs$method_seed %||% fm_get(record, "method_seed")),
    native_status = st, ok = ok, runtime_s = scalar_or_na(fm_get(record, "runtime_s")),
    evidence_ok = evidence_ok, islands_ok = islands_ok, hpm_ok = ok && !is.null(hpm), rb_ok = ok && !is.null(pip_full), plain_ok = ok && !is.null(plain_full),
    log_Z = if (evidence_ok) logZ else NA_real_,
    log_Z_r = if (islands_ok) logZr else numeric(0), log_Z_lower95 = if (evidence_ok) scalar_or_na(fm_get(record, "log_Z_lower95")) else NA_real_,
    log_Z_rel_m0 = scalar_or_na(fm_get(record, "log_Z_rel_m0")), log_m0 = scalar_or_na(fm_get(record, "log_m0")),
    pip_rb = if (ok) pip_full else NULL, pip_rb_r = if (ok) pip_r else NULL,
    pip_plain = if (ok) plain_full else NULL, pip_plain_r = if (ok) plain_r else NULL,
    hpm = hpm, hpm_F = scalar_or_na(fm_get(record, "hpm_F")), mpm = if (ok) mpm else NULL, mpm_plain = if (ok) mpm_plain else NULL,
    kept = kept,
    escalated = scalar_or_na(fm_get(record, "flag_escalated"), "logical"),
    checks_passed_final = scalar_or_na(fm_get(record, "flag_checks_passed_final"), "logical"),
    E1 = scalar_or_na(fm_get(record, "flag_E1"), "logical"), E2 = scalar_or_na(fm_get(record, "flag_E2"), "logical"), E3 = scalar_or_na(fm_get(record, "flag_E3"), "logical"),
    low_ess = scalar_or_na(fm_get(record, "flag_low_ess"), "logical"), local_limit = scalar_or_na(fm_get(record, "flag_local_limit"), "logical"),
    grid_unconverged = scalar_or_na(fm_get(record, "flag_grid_unconverged"), "logical"),
    near_tie_truncated = scalar_or_na(fm_get(record, "flag_near_tie_truncated"), "logical"),
    cut_group = scalar_or_na(fm_get(record, "flag_cut_group"), "logical"), local_certified = scalar_or_na(fm_get(record, "flag_local_certified"), "logical"),
    tier = scalar_or_na(fm_get(record, "tier")), n_stages_final = nst, min_ess = min_ess,
    score_fresh = sum_or_na(fresh), score_logical = sum_or_na(logical_s),
    blocks = fm_get(record, "blocks"),
    # scored-set quantities are available only for a completed fit (same policy in every table)
    log_mass_scored = if (ok) scalar_or_na(fm_get(record, "log_mass_scored")) else NA_real_,
    n_distinct_scored = if (ok) scalar_or_na(fm_get(record, "n_distinct_scored")) else NA_real_,
    scored_set = if (ok) fm_get(record, "scored_set") else NULL, truth_trace = if (ok) fm_get(record, "truth_trace") else NULL,
    rows = record$rows)
}

# Rule rows of an SMC record in the common selection frame (hpm, pip05), straight from the adapter rows.
smc_rule_rows <- function(record) {
  r <- record$rows
  if (is.null(r) || !nrow(r)) return(NULL)
  data.frame(case_id = r$case_id, dataset_id = r$dataset_id, method_id = r$method_id, rule_id = r$rule_id, role = r$role,
             status = r$status, support = r$support, runtime_s = r$runtime_s, diag_flag = r$diag_flag, diag_codes = if ("diag_codes" %in% names(r)) r$diag_codes else NA_character_,
             adaptation_ids = NA_character_, stringsAsFactors = FALSE)
}
