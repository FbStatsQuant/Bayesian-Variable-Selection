# p1m_competitors.R -- competitor harness (WP5; EXPERIMENT_PLAN §4; ENGINEERING_SPEC §0.3 WP5 item 5).
#
# Runs the competitors on the SAME regenerated dataset (raw.bin from `smcbvs4 gen`, read with tools/v4_read.R) and writes
# one record per method, schema smcbvs4.competitor/1, which `smcbvs4 eval --competitor <record> --data data.bin
# --truth truth.json --out <x>.bin` scores with the same evaluator as the engine (selection, PIPs, W3-DIST metrics).
#
#   Rscript p1m_competitors.R --raw raw.bin --truth truth.json --out-dir DIR [--methods m1,m2,...] [--seed 1]
#                             [--bas-p-max 10000] [--threads 1]
#   Rscript p1m_competitors.R --check-packages [--out-dir DIR]      # which packages exist here (packages.json)
#
# Tuning is fixed before the runs (plan §4): 10-fold CV with fold ids from --seed; SuSiE L = 10; BAS MCMC on p <= 10^4.
# A missing package gives status "package_missing" (the record is still written: every method stays in the table).
# Nothing is installed by this script.
#
# Record (all column indices are ORIGINAL 1-based):
#   {schema, method, package, version, status: completed|package_missing|failed|skipped, reason, wall_s, seed,
#    selected: [j...], pip: {default, idx, val} | null,
#    predictive: {type: "gaussian", intercept, idx, coef, sigma2} | {type: "model_law", models: [[j...]...], weights}
#                | null,
#    note}
# Predictive objects (plan §4 table): penalised fits -> N(a + x'b, sigma2_CV); SuSiE / varbvs -> the Gaussian at the
# posterior mean with their residual variance (an approximation of their mixture predictive; labelled in `note`);
# BAS -> its model law with our conjugate kernels (STATEMENT §2, "any output-measurable law Q"); SIS -> hand-off only.

PKGS <- c(glmnet = "lasso_cv_min,lasso_cv_1se", ncvreg = "mcp_cv,scad_cv", biglasso = "lasso_cv_big",
          L0Learn = "l0learn_cv", susieR = "susie", varbvs = "varbvs", BAS = "bas")
ALL_METHODS <- c("lasso_cv_min", "lasso_cv_1se", "mcp_cv", "scad_cv", "lasso_cv_big", "l0learn_cv", "susie", "varbvs",
                 "bas", "sis_screen", "marg_ols", "ols_oracle")

# ---------------------------------------------------------------------------------------------------------- utilities
args_parse <- function(a) {
  out <- list(); i <- 1
  while (i <= length(a)) {
    k <- sub("^--", "", a[i])
    if (i < length(a) && !grepl("^--", a[i + 1])) { out[[k]] <- a[i + 1]; i <- i + 2 } else { out[[k]] <- "1"; i <- i + 1 }
  }
  out
}
json_str <- function(s) paste0('"', gsub("[\u0001-\u001f]", " ", gsub('"', '\\\\"', gsub("\\\\", "\\\\\\\\", s))), '"')
to_json <- function(x) {   # minimal writer (no dependency): NULL, logical, numeric, character, unnamed / named lists
  if (is.null(x)) return("null")
  if (is.list(x)) {
    if (!is.null(names(x)) && all(names(x) != ""))
      return(paste0("{", paste(vapply(names(x), function(k) paste0(json_str(k), ": ", to_json(x[[k]])), ""), collapse = ", "), "}"))
    return(paste0("[", paste(vapply(x, to_json, ""), collapse = ", "), "]"))
  }
  if (is.character(x)) { if (length(x) == 1 && !inherits(x, "AsIs")) return(json_str(x)); return(paste0("[", paste(vapply(x, json_str, ""), collapse = ", "), "]")) }
  if (is.logical(x)) { v <- ifelse(is.na(x), "null", ifelse(x, "true", "false")); if (length(x) == 1 && !inherits(x, "AsIs")) return(v); return(paste0("[", paste(v, collapse = ", "), "]")) }
  v <- ifelse(is.finite(x), formatC(x, digits = 17, format = "g"), "null")
  v <- gsub(" ", "", v)
  if (length(x) == 1 && !inherits(x, "AsIs")) return(v)
  paste0("[", paste(v, collapse = ", "), "]")
}
arr <- function(x) I(x)   # always a JSON array, even of length 0 or 1
write_record <- function(rec, path) { tmp <- paste0(path, ".tmp.", Sys.getpid()); writeLines(to_json(rec), tmp); file.rename(tmp, path) }
have <- function(p) nzchar(p) && requireNamespace(p, quietly = TRUE)
pkg_version <- function(p) if (have(p)) as.character(utils::packageVersion(p)) else ""

gaussian_pred <- function(a0, b, sigma2) {
  nz <- which(b != 0)
  list(type = "gaussian", intercept = unname(a0), idx = arr(as.integer(nz)), coef = arr(unname(b[nz])), sigma2 = unname(sigma2))
}
sparse_pip <- function(pip, thr = 1e-8) { nz <- which(pip > thr); list(default = 0, idx = arr(as.integer(nz)), val = arr(unname(pip[nz]))) }
ols_on <- function(X, y, cols) {
  if (!length(cols)) return(list(a = mean(y), b = numeric(0), s2 = sum((y - mean(y))^2) / (length(y) - 1)))
  f <- stats::lm.fit(cbind(1, X[, cols, drop = FALSE]), y)
  df <- length(y) - length(cols) - 1
  list(a = f$coefficients[1], b = f$coefficients[-1], s2 = sum(f$residuals^2) / max(df, 1))
}

# ---------------------------------------------------------------------------------------------------------- methods
# Each returns list(selected, pip, predictive, note) with ORIGINAL indices; errors are caught by the driver loop.
run_method <- function(m, X, y, truth, seed, opt) {
  n <- nrow(X); p <- ncol(X)
  set.seed(seed); foldid <- sample(rep(seq_len(10), length.out = n))
  full_b <- function(idx, val) { b <- numeric(p); b[idx] <- val; b }
  switch(m,
    lasso_cv_min = , lasso_cv_1se = {
      cv <- glmnet::cv.glmnet(X, y, foldid = foldid, family = "gaussian", alpha = 1)
      lam <- if (m == "lasso_cv_min") cv$lambda.min else cv$lambda.1se
      cf <- as.numeric(stats::coef(cv, s = lam)); b <- cf[-1]
      list(selected = which(b != 0), pip = NULL, predictive = gaussian_pred(cf[1], b, cv$cvm[cv$lambda == lam]),
           note = sprintf("glmnet cv.glmnet, 10 folds (seed %d), %s", seed, sub("lasso_cv_", "lambda.", m)))
    },
    mcp_cv = , scad_cv = {
      pen <- if (m == "mcp_cv") "MCP" else "SCAD"
      cv <- ncvreg::cv.ncvreg(X, y, penalty = pen, fold = foldid, seed = seed)
      cf <- stats::coef(cv); b <- as.numeric(cf[-1])
      list(selected = which(b != 0), pip = NULL, predictive = gaussian_pred(cf[1], b, min(cv$cve)),
           note = sprintf("ncvreg cv.ncvreg %s, 10 folds (seed %d), lambda.min", pen, seed))
    },
    lasso_cv_big = {
      Xb <- bigmemory::as.big.matrix(X)
      cv <- biglasso::cv.biglasso(Xb, y, nfolds = 10, seed = seed, ncores = opt$threads)
      cf <- as.numeric(stats::coef(cv)); b <- cf[-1]
      list(selected = which(b != 0), pip = NULL, predictive = gaussian_pred(cf[1], b, min(cv$cve)),
           note = sprintf("biglasso cv.biglasso, 10 folds (seed %d), lambda.min", seed))
    },
    l0learn_cv = {
      cv <- L0Learn::L0Learn.cvfit(X, y, penalty = "L0L2", nFolds = 10, seed = seed)
      g <- which.min(vapply(cv$cvMeans, min, 0)); l <- which.min(cv$cvMeans[[g]])
      lam <- cv$fit$lambda[[g]][l]; gam <- cv$fit$gamma[g]
      cf <- as.numeric(stats::coef(cv, lambda = lam, gamma = gam)); b <- cf[-1]
      list(selected = which(b != 0), pip = NULL, predictive = gaussian_pred(cf[1], b, cv$cvMeans[[g]][l]),
           note = sprintf("L0Learn L0L2 cvfit, 10 folds (seed %d), min CV error over (gamma, lambda)", seed))
    },
    susie = {
      s <- susieR::susie(X, y, L = 10)
      cf <- as.numeric(stats::coef(s)); b <- cf[-1]
      list(selected = which(s$pip > 0.5), pip = sparse_pip(s$pip), predictive = gaussian_pred(cf[1], b, s$sigma2),
           note = "susieR::susie L = 10; predictive = N(posterior-mean fit, sigma2) (approximation of the SER mixture)")
    },
    varbvs = {
      f <- varbvs::varbvs(X, NULL, y, family = "gaussian", verbose = FALSE)
      cf <- stats::coef(f); av <- cf[, ncol(cf)]          # last column = averaged over the hyperparameter grid
      a0 <- av[1]; b <- as.numeric(av[-1])
      pip <- as.numeric(f$pip); s2 <- sum(f$w * f$sigma)
      list(selected = which(pip > 0.5), pip = sparse_pip(pip), predictive = gaussian_pred(a0, b, s2),
           note = "varbvs gaussian, default grid; predictive = N(averaged posterior mean, averaged sigma) (approximation)")
    },
    bas = {
      if (p > opt$bas_p_max) stop(sprintf("skipped: p = %d > bas-p-max = %d", p, opt$bas_p_max))
      df <- data.frame(y = y, X)
      f <- BAS::bas.lm(y ~ ., data = df, method = "MCMC", prior = "g-prior", alpha = n, modelprior = BAS::beta.binomial(1, p),
                       MCMC.iterations = 20 * p, initprobs = "marg-eplogp")
      w <- f$postprobs; keep <- order(-w)[seq_len(min(1000, length(w)))]
      models <- lapply(f$which[keep], function(v) arr(as.integer(setdiff(v, 0))))   # BAS index 0 = intercept
      pip <- as.numeric(f$probne0[-1])
      list(selected = which(pip > 0.5), pip = sparse_pip(pip),
           predictive = list(type = "model_law", models = models, weights = arr(unname(w[keep]))),
           note = "BAS bas.lm MCMC, g-prior g = n, BB(1, p) model prior; top 1000 models re-weighted, our conjugate kernels")
    },
    sis_screen = {
      d <- floor(n / log(n))
      r <- abs(drop(stats::cor(X, y)))
      keep <- sort(order(-r)[seq_len(min(d, p))])
      writeLines(as.character(keep), file.path(opt$out_dir, "sis_cols.txt"))
      list(selected = keep, pip = NULL, predictive = NULL,
           note = sprintf("SIS screen, d = floor(n / log n) = %d; hand-off to the engine (sis_cols.txt); not a selection", d))
    },
    marg_ols = {
      k <- max(1, length(truth$S0))
      r <- abs(drop(stats::cor(X, y))); keep <- sort(order(-r)[seq_len(k)])
      o <- ols_on(X, y, keep)
      list(selected = keep, pip = NULL, predictive = gaussian_pred(o$a, full_b(keep, o$b), o$s2),
           note = sprintf("built-in baseline: top-%d marginal correlations, then OLS (no package)", k))
    },
    ols_oracle = {
      keep <- sort(as.integer(unlist(truth$S0)))
      o <- ols_on(X, y, keep)
      list(selected = keep, pip = NULL, predictive = gaussian_pred(o$a, full_b(keep, o$b), o$s2),
           note = "reference only (uses S0): OLS on the true support")
    },
    stop("unknown method ", m))
}
method_pkg <- function(m) {
  for (p in names(PKGS)) if (m %in% strsplit(PKGS[[p]], ",")[[1]]) return(p)
  ""
}

check_packages <- function(out_dir = NULL) {
  extra <- c("bigmemory", "jsonlite", "digest")
  rows <- lapply(c(names(PKGS), extra), function(p) list(package = p, installed = have(p), version = pkg_version(p),
                                                         methods = if (p %in% names(PKGS)) PKGS[[p]] else ""))
  rec <- list(schema = "smcbvs4.competitor_packages/1", host = Sys.info()[["nodename"]], R = R.version.string, packages = rows)
  for (r in rows) cat(sprintf("%-10s %-8s %-8s %s\n", r$package, if (r$installed) "yes" else "MISSING", r$version, r$methods))
  if (!is.null(out_dir)) write_record(rec, file.path(out_dir, "packages.json"))
  invisible(rec)
}

# ---------------------------------------------------------------------------------------------------------- main
main <- function(a) {
  o <- args_parse(a)
  here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
  if (!is.null(o[["check-packages"]])) { check_packages(o[["out-dir"]]); return(invisible(0)) }
  for (k in c("raw", "truth", "out-dir")) if (is.null(o[[k]])) stop("missing --", k)
  source(file.path(here, "..", "v4_read.R"))
  dir.create(o[["out-dir"]], recursive = TRUE, showWarnings = FALSE)
  seed <- as.integer(if (is.null(o$seed)) 1 else o$seed)
  opt <- list(bas_p_max = as.numeric(if (is.null(o[["bas-p-max"]])) 1e4 else o[["bas-p-max"]]),
              threads = as.integer(if (is.null(o$threads)) 1 else o$threads), out_dir = o[["out-dir"]])
  methods <- if (is.null(o$methods)) ALL_METHODS else strsplit(o$methods, ",")[[1]]
  rb <- v4_read(o$raw, verify = TRUE)
  if (rb$kind != 1) stop("--raw is not a raw.bin (kind 1)")
  ent <- rb$sections[rb$sections$name == "X_cm", ]
  n <- ent$d0; p <- ent$d1
  X <- matrix(rb$get("X_cm"), n, p); y <- rb$get("y")
  truth <- jsonlite_free_read(o$truth)
  for (m in methods) {
    pkg <- method_pkg(m)
    rec <- list(schema = "smcbvs4.competitor/1", method = m, package = pkg, version = pkg_version(pkg), status = "failed",
                reason = "", wall_s = NA_real_, seed = seed, n = n, p = p, selected = arr(integer(0)), pip = NULL, predictive = NULL, note = "")
    if (nzchar(pkg) && !have(pkg)) { rec$status <- "package_missing"; rec$reason <- paste(pkg, "is not installed here")
    } else if (m == "lasso_cv_big" && !have("bigmemory")) { rec$status <- "package_missing"; rec$reason <- "bigmemory is not installed here"
    } else {
      t0 <- proc.time()[["elapsed"]]
      r <- tryCatch(run_method(m, X, y, truth, seed, opt), error = function(e) e)
      rec$wall_s <- proc.time()[["elapsed"]] - t0
      if (inherits(r, "error")) {
        msg <- conditionMessage(r)
        rec$status <- if (grepl("^skipped:", msg)) "skipped" else "failed"; rec$reason <- msg
      } else {
        rec$status <- "completed"; rec$selected <- arr(as.integer(sort(r$selected))); rec$pip <- r$pip
        rec$predictive <- r$predictive; rec$note <- r$note
      }
    }
    write_record(rec, file.path(o[["out-dir"]], paste0("comp_", m, ".json")))
    cat(sprintf("%-14s %-16s %8s s  %s\n", m, rec$status, format(round(rec$wall_s, 2)), rec$reason))
  }
  invisible(0)
}

# truth.json without jsonlite: only S0 is needed here (the evaluator reads the full file)
jsonlite_free_read <- function(path) {
  txt <- paste(readLines(path, warn = FALSE), collapse = " ")
  s0 <- regmatches(txt, regexpr('"S0"\\s*:\\s*\\[[^]]*\\]', txt))
  v <- if (length(s0)) as.integer(strsplit(gsub('.*\\[|\\]|\\s', "", s0), ",")[[1]]) else integer(0)
  list(S0 = v[!is.na(v)])
}

if (sys.nframe() == 0L) main(commandArgs(trailingOnly = TRUE))
