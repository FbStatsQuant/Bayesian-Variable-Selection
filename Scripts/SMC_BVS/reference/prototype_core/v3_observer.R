# v3_observer.R -- observer instrumentation (CORE_SPEC v2 §8) and the R11 firewall.
# observer = list(truth = S0, watch = list(name = S, ...), watch_sets = list(name = list(S, ...), ...),
#                 chains = list(list(S^(0), ..., S^(c) = S0), ...), refs = list(...)).
# The start mode S~_0 is always watched. Observer computations use the observer scorer only (C++: a separate
# Scorer instance); they draw no random numbers and write nothing the algorithm reads.

# Every part of `observer` is optional (CORE_SPEC §8); unnamed watch entries are named watch<i>, unnamed sets set<i>.
v3_observer_names <- function(l, prefix) {
  nm <- names(l) %||% rep("", length(l))
  nm[is.na(nm) | nm == ""] <- paste0(prefix, seq_along(l))[is.na(nm) | nm == ""]
  stats::setNames(l, nm)
}
# Parts are read with [[ ]] (exact names): `$` would partially match "watch" to "watch_sets".
v3_observer_prepare <- function(setup, observer) {
  list(truth = if (!is.null(observer[["truth"]])) as.integer(observer[["truth"]]) else NULL,
       watch = v3_observer_names(lapply(observer[["watch"]] %||% list(), as.integer), "watch"),
       watch_sets = v3_observer_names(lapply(observer[["watch_sets"]] %||% list(), function(s) lapply(s, as.integer)), "set"))
}

# §8.1 start quantities (exact, cheap) for every watched model, plus AGG/T22 quantities and completion chains for S0.
v3_observer_start <- function(setup, observer) {
  mode <- v3_start_mode(setup$start)
  watch <- c(if (!is.null(observer[["truth"]])) list(truth = as.integer(observer[["truth"]])), list(start_mode = mode$model),
             v3_observer_names(lapply(observer[["watch"]] %||% list(), as.integer), "watch"))
  chains <- lapply(observer[["chains"]] %||% list(), function(ch) lapply(ch, as.integer))
  r <- .v3cpp$cpp_observer_start(setup$ptr, watch, if (!is.null(observer[["truth"]])) as.integer(observer[["truth"]]) else NULL, chains)
  r$start_mode <- mode
  r
}

v3_observer_report <- function(setup, observer, prepared, raw, rep = raw$observer) {
  rep$start <- v3_observer_start(setup, observer)
  if (!is.null(observer[["refs"]])) {
    rep$refs <- observer[["refs"]]
    if (!is.null(observer[["refs"]][["log_Z"]]) && raw$status == "completed") {
      lz <- v3_log_sum_exp(vapply(raw$islands, function(r) r$log_Z, 0)) - log(length(raw$islands))
      rep$ref_comparison <- list(log_Z_error = lz - observer[["refs"]][["log_Z"]])
    }
  }
  rep
}

# Operational outputs (everything except the observer report and wall-clock quantities), for the R11 invariance test.
# Removes, recursively, every element named observer, timings, seconds, preflight, peak_memory_kb, setup_seconds.
v3_operational <- function(fit) {
  drop <- c("observer", "timings", "seconds", "preflight", "peak_memory_kb", "setup_seconds")
  strip <- function(x) {
    if (!is.list(x) || is.data.frame(x)) return(x)
    if (!is.null(names(x))) x <- x[!(names(x) %in% drop)]
    if (length(x)) { a <- attributes(x); x[] <- lapply(x, strip); attributes(x) <- a }
    x
  }
  strip(fit)
}
