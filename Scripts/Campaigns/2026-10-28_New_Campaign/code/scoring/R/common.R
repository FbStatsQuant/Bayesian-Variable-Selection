# common.R -- shared helpers for the New Campaign scoring pipeline (LOWP thread).
# Scoring is the ONLY code that reads truth (R/truth.R). Fits never see it.

suppressPackageStartupMessages(library(data.table))

`%||%` <- function(a, b) if (is.null(a)) b else a

SC_DIR <- local({  # directory of the scoring tree (parent of R/)
  d <- Sys.getenv("SCORING_DIR", "")
  if (nzchar(d)) normalizePath(d, winslash = "/") else NA_character_
})

# ---- supports ---------------------------------------------------------------------------------
# Text encoding (INTERFACES): "3;7;14", "" = empty model, NA = missing.
# NULL / NA / character(0) = support UNAVAILABLE (NULL); a zero-length numeric/integer vector or "" = a genuine EMPTY support (integer(0)).
parse_support <- function(x) {
  if (is.null(x)) return(NULL)
  if (is.list(x)) { if (!length(x)) return(NULL); x <- x[[1L]]; if (is.null(x)) return(NULL) }
  if (is.numeric(x)) { if (!length(x)) return(integer(0)); if (anyNA(x)) return(NULL); return(sort(as.integer(x))) }
  if (is.character(x)) {
    if (length(x) != 1L || is.na(x)) return(NULL)
    if (!nzchar(x)) return(integer(0))
    v <- suppressWarnings(as.integer(strsplit(x, "[;, ]+")[[1L]])); if (anyNA(v)) return(NULL)
    return(sort(v))
  }
  NULL
}
enc_support <- function(v) if (is.null(v)) NA_character_ else paste(sort(as.integer(v)), collapse = ";")
same_set <- function(a, b) !is.null(a) && !is.null(b) && identical(sort(as.integer(a)), sort(as.integer(b)))
support_mask <- function(S) { S <- as.integer(S); if (!length(S)) 0 else sum(2^(S - 1)) }  # double, exact for p <= 52

file_sha256 <- function(path) digest::digest(file = path, algo = "sha256", serialize = FALSE)

# ---- numerics ---------------------------------------------------------------------------------
lse <- function(x) { x <- x[!is.na(x)]; if (!length(x)) return(-Inf); m <- max(x); if (!is.finite(m)) return(m); m + log(sum(exp(x - m))) }
nzsd <- function(x) if (length(x) < 2L || anyNA(x)) NA_real_ else stats::sd(x)
q90 <- function(x) { x <- x[!is.na(x)]; if (!length(x)) NA_real_ else unname(stats::quantile(x, 0.9, type = 7)) }
safe_max <- function(x) if (!length(x) || all(is.na(x))) NA_real_ else max(x, na.rm = TRUE)
safe_mean <- function(x) if (!length(x) || all(is.na(x))) NA_real_ else mean(x, na.rm = TRUE)

# ---- path walking -----------------------------------------------------------------------------
# get_path(obj, "fit$flags$E1") -> value or NULL (first missing link gives NULL)
get_path <- function(obj, path) {
  for (nm in strsplit(path, "$", fixed = TRUE)[[1L]]) {
    if (is.null(obj)) return(NULL)
    if (is.list(obj) && !is.null(names(obj)) && nm %in% names(obj)) obj <- obj[[nm]] else return(NULL)
  }
  obj
}

# ---- core loader -------------------------------------------------------------------------------
# The SMC core (never modified). Default location = ../core/v2_2/core relative to the scoring tree.
default_core_dir <- function() {
  e <- Sys.getenv("SCORING_CORE_DIR", "")
  if (nzchar(e)) return(e)
  file.path(dirname(SC_DIR), "core", "v2_2", "core")
}
sc_load_core <- function(core_dir = default_core_dir()) {
  if (!exists("v3_score", mode = "function") || !exists(".v3cpp")) {
    if (!file.exists(file.path(core_dir, "v3.R"))) stop("core not found at ", core_dir)
    source(file.path(core_dir, "v3.R"), local = FALSE)
  }
  invisible(TRUE)
}

# Optional low-p enumerator library (written by another worker). Sourced if present.
enum_available <- function() exists("lowp_score_models", mode = "function") && exists("lowp_td", mode = "function")
sc_load_enum <- function(enum_file = NULL) {
  enum_file <- enum_file %||% { e <- Sys.getenv("SCORING_ENUM_FILE", ""); if (nzchar(e)) e else file.path(dirname(SC_DIR), "lowp", "enum", "lowp_enum.R") }
  if (file.exists(enum_file) && !exists("lowp_td", mode = "function")) {
    ok <- tryCatch({ source(enum_file, local = FALSE); TRUE }, error = function(e) { message("enum load failed: ", conditionMessage(e)); FALSE })
    return(invisible(ok))
  }
  invisible(exists("lowp_td", mode = "function"))
}

# ---- scoring context cache and F(S) ------------------------------------------------------------
# A "scorer" wraps one (X, y) pair: preprocessing exactly as v3_fit, a context, and a cached F(S).
make_scorer <- function(X, y) {
  sc_load_core()
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  if (!identical(pre$status, "ok")) stop("preprocess failed: ", pre$status)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  cache <- new.env(hash = TRUE)
  kept <- pre$kept
  F_of <- function(S) {                       # S = original indices; NA if a member was dropped or |S| > K
    S <- sort(as.integer(S))
    if (length(S) > ctx$K || !all(S %in% kept)) return(NA_real_)
    key <- paste0("k", paste(S, collapse = ","))
    v <- cache[[key]]
    if (is.null(v)) { v <- v3_score(ctx, S)$F; cache[[key]] <- v }
    v
  }
  list(ctx = ctx, pre = pre, kept = kept, K = ctx$K, F = F_of, n_cached = function() length(ls(cache)))
}

# F of a list of models; uses lowp_score_models when the enumerator library is loaded and agrees, else the core scorer.
score_models <- function(scorer, models) vapply(models, function(S) scorer$F(S), 0)

# ---- file helpers ------------------------------------------------------------------------------
read_rds_safe <- function(path) tryCatch(readRDS(path), error = function(e) { warning("cannot read ", path, ": ", conditionMessage(e)); NULL })
write_csv_na <- function(dt, path) { dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE); data.table::fwrite(dt, path, na = "NA", quote = TRUE) }

parse_case_id <- function(case_id) {
  m <- regmatches(case_id, regexec("^(p([0-9]{4})_S([0-9])_r([0-9]{3}))_(c[0-9]{3})$", case_id))[[1L]]
  if (length(m) != 6L) return(NULL)
  list(case_id = case_id, dataset_id = m[2L], p = as.integer(m[3L]), scenario = as.integer(m[4L]), replicate = as.integer(m[5L]), scale_key = m[6L])
}
scale_value <- function(scale_key) c(c100 = 1, c075 = 0.75, c050 = 0.5, c035 = 0.35, c025 = 0.25)[[scale_key]]
