# helpers.R -- shared by the validation scripts: synthetic designs, the SMC core copy (compiled in TMP) and paths.
# Usage: source("helpers.R") with LOWP_ENUM_DIR defined (set it, or source lowp_enum.R first).
TMP <- Sys.getenv("LOWP_TMP", unset = "C:/Users/felip/AppData/Local/Temp/lowp_work/enum")
dir.create(TMP, showWarnings = FALSE, recursive = TRUE)
Sys.setenv(LOWP_ENUM_CACHE = file.path(TMP, "cache"))
CAMP_CODE <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code"
CORE_SRC  <- file.path(CAMP_CODE, "core/v2_2/core")
if (!exists("lowp_exact")) source(file.path(CAMP_CODE, "lowp/enum/lowp_enum.R"))

# Synthetic design, n x p: kind "block" (Sigma = 0.85 within blocks of 5), "ar1" (rho = 0.8), "indep".
gen_design <- function(p, kind = "block", n = 200, seed = 1, rho = 0.85) {
  set.seed(seed)
  Sig <- switch(kind,
    block = { S <- diag(p); for (b in seq(1, p, by = 5)) { ix <- b:min(p, b + 4); S[ix, ix] <- rho }; diag(S) <- 1; S },
    ar1 = outer(1:p, 1:p, function(i, j) 0.8^abs(i - j)),
    indep = diag(p))
  X <- matrix(rnorm(n * p), n) %*% chol(Sig)
  X <- scale(X); attributes(X) <- list(dim = dim(X)); X
}
# Response columns for scales c in `cs`: y = c * X beta + eps (same eps for all scales)
gen_response <- function(X, beta_idx, beta, cs = c(c100 = 1, c050 = 0.5), seed = 2) {
  set.seed(seed); eps <- rnorm(nrow(X))
  sig <- as.vector(X[, beta_idx, drop = FALSE] %*% beta)
  sapply(cs, function(c) c * sig + eps)
}
# A copy of the SMC core, compiled in TMP (the core folder itself is never written to).
load_core_ref <- function() {
  dst <- file.path(TMP, "core_copy")
  if (!file.exists(file.path(dst, "v3.R"))) {
    dir.create(dst, recursive = TRUE, showWarnings = FALSE)
    file.copy(list.files(CORE_SRC, full.names = TRUE), dst, recursive = TRUE)
    unlink(file.path(dst, ".cpp_cache"), recursive = TRUE)
  }
  source(file.path(dst, "v3.R"), local = FALSE)
  invisible(dst)
}
bits <- function(x) { x <- as.numeric(x); r <- writeBin(x, raw(), endian = "little"); paste(r, collapse = "") }
same_bits <- function(a, b) identical(writeBin(as.numeric(a), raw()), writeBin(as.numeric(b), raw()))
