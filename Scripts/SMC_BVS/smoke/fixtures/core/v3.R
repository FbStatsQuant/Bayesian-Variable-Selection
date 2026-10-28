# ADAPTER TEST FIXTURE ONLY. No sampler, scorer, compile or numerical inference.
# The tests copy this into a private temporary core tree, never a production snapshot.
v3_fit <- function(X, y, seed, allocation = list(mem_gb = 8, hours = 24)) {
  stopifnot(identical(dim(X), c(200L, 500L)), length(y) == 200L,
    identical(seed, 6420001L), identical(sort(names(allocation)), c("hours", "mem_gb")))
  expected_scale <- Sys.getenv("SMCBVS_ADAPTER_EXPECT_SCALE", "c100")
  stopifnot(expected_scale %in% c("c100", "c050"),
    identical(y, if (expected_scale == "c100") as.double(1:200) else as.double(201:400)),
    identical(unname(X[, 1L]), rep(1, 200L)),
    identical(unname(X[, 2L]), as.double(1:200)),
    identical(unname(X[, 500L]), as.double(1:200)))
  mode <- Sys.getenv("SMCBVS_ADAPTER_FIXTURE", "completed")
  if (mode == "throw") stop("fixture uncaught scorer exception")
  if (mode == "oom") stop("cannot allocate vector of size fixture")
  if (mode == "malformed") return(123)
  p <- ncol(X); kept <- 2:p
  pip <- setNames(rep(0.1, length(kept)), as.character(kept)); pip[c("5", "500")] <- 0.75; pip["3"] <- 0.5
  out <- list(status = mode, seed = seed, n = nrow(X), p = length(kept),
    hpm = c(5L, 500L), mpm = c(5L, 500L), pip_primary = pip,
    preprocessing = list(kept = kept, dropped = 1L), estimates_available = TRUE,
    flags = list(E1 = FALSE, E2 = TRUE, E3 = FALSE, checks_passed_final = FALSE),
    cut_group = TRUE, cut_group_count = 1L,
    cut_group_components = list(list(size = 2L, block_span = 2L, members = c(5L, 500L))),
    hpm_provenance = list(phase = "fixture", mechanism = "fixture"),
    fixture_nested_record = list(sentinel = "must survive unchanged", original_indices = c(5L, 500L)))
  if (mode %in% c("schedule_limit", "numerical_failure", "resource_limit", "invalid_input")) {
    out$estimates_available <- FALSE; out$pip_primary <- NULL; out$mpm <- NULL
  }
  if (mode %in% c("y_constant", "no_predictors")) {
    out$hpm <- integer(); out$estimates_available <- FALSE; out$pip_primary <- NULL; out$mpm <- NULL
  }
  if (mode == "bad_pip") { out$status <- "completed"; out$pip_primary <- unname(pip) }
  if (mode == "bad_mpm") { out$status <- "completed"; out$mpm <- c(3L, 5L, 500L) }
  out
}
