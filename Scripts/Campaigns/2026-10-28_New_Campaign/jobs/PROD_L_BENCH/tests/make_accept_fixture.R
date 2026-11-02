# make_accept_fixture.R -- fixtures for test_accept.sh (single R process each, R 4.4.1 on the laptop; never more than one at a time).
#   Rscript make_accept_fixture.R gen   <study> <outroot> <run_id> <lib> <code_dir>
#       run the REAL frozen CLI (code/bench_lowp/run_bench_case.R) for case p0020_S1_r001 / c100, all 8 methods, with the laptop test library
#       (--test-library): real records, test provenance.
#   Rscript make_accept_fixture.R mut   <results_in> <results_out> <variant> <lib> <pinned 0|1> <code_dir>
#       copy a results folder (every case of every p) and apply ONE defect named by <variant> to a copy of the real records; csv and .sha256
#       sidecars are re-sealed so that only accept_bench.R can see the defect. pinned=1 first rewrites the provenance of every record to what
#       the PINNED sealed run records (R 4.5.2, test_library FALSE, sealed library = the pinned path, non-base packages directly in it,
#       base/recommended in R's own library, pinned packages at their pinned versions); pinned=0 leaves the provenance as recorded (local mode).
#   Rscript make_accept_fixture.R manifest_drop <manifest_in> <manifest_out> <dataset_id>   : copy of the sealed inputs manifest without one dataset row
#   Rscript make_accept_fixture.R code_mut <code_in> <code_out> <relative_file> <append|addfile>  : copy of the code tree with one byte changed / one extra file
# variants (scope: first = the first record of the method, all = every record of the method):
#   good                                      nothing
#   old, pinned only: no_coef_entry beta_pen_short beta_ols_short support_mismatch k37_mismatch a_beta_short test_library wrong_sealed wrong_r
#   I1: i1_f4_all i1_f4_first i1_extra_rule i1_a1_roles i1_f5_nosic
#   I2: i2_ebic1_ols_na i2_cvmin_ols_finite i2_betapen_inf i2_a1_nopip i2_a1_pip12 i2_a2_beta_na
#   I3: i3_data_seed i3_fold_seed i3_scale_key i3_scale i3_runid i3_y_sha i3_input_hashes
#   I4: i4_noprov i4_src_null i4_src_wrong i4_files_hash i4_files_refp i4_pin_version i4_glmnet_rlib
#   N1: n1_cvmin_k n1_unsorted n1_dup n1_pplus1 n1_a2_support n1_a_nosel n1_f4_coef_k n1_a1_rows_support
#   N2: n2_f4_bic_crit n2_f5_bic_support n2_f4_bic_k
#   positives (must stay ACCEPTED): pos_null_sel pos_failed_rule
args <- commandArgs(TRUE)
mode <- args[1]
PINNED <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
RLIB <- "/opt/apps/software/R/4.5.2/lib64/R/library"
ZERO64 <- paste(rep("0", 64), collapse = "")
WRONG64 <- paste(rep("ab", 32), collapse = "")
methods <- c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")

if (mode == "gen") {
  study <- args[2]; outroot <- args[3]; runid <- args[4]; lib <- args[5]; code <- args[6]
  rs <- file.path(R.home("bin"), "Rscript")
  st <- system2(rs, c(shQuote(file.path(code, "run_bench_case.R")), "--study", shQuote(study), "--outroot", shQuote(outroot), "--run-id", runid,
                      "--case", "p0020_S1_r001", "--scale", "c100", "--methods", "all", "--library", shQuote(lib), "--test-library"))
  quit(save = "no", status = if (st %in% c(0L, 2L)) 0L else 1L)
}
if (mode == "manifest_drop") {
  m <- utils::read.csv(args[2], colClasses = "character")
  m <- m[m$dataset_id != args[4], , drop = FALSE]
  utils::write.csv(m, args[3], row.names = FALSE)
  quit(save = "no", status = 0L)
}
if (mode == "code_mut") {
  src <- args[2]; dst <- args[3]; rel <- args[4]; how <- args[5]
  dir.create(dst, recursive = TRUE, showWarnings = FALSE)
  ok <- file.copy(list.files(src, full.names = TRUE, all.files = TRUE, no.. = TRUE), dst, recursive = TRUE)
  stopifnot(all(ok))
  if (how == "append") { con <- file(file.path(dst, rel), "ab"); writeBin(as.raw(10L), con); close(con) }
  else writeLines("extra", file.path(dst, rel))
  quit(save = "no", status = 0L)
}

stopifnot(mode == "mut")
res_in <- args[2]; res_out <- args[3]; variant <- args[4]; lib <- args[5]; pinned <- identical(args[6], "1"); code <- args[7]
.libPaths(c(lib, .libPaths()))
suppressMessages(library(digest))
dir.create(res_out, recursive = TRUE, showWarnings = FALSE)
stopifnot(all(file.copy(list.files(res_in, full.names = TRUE), res_out, recursive = TRUE)))
base_pkgs <- rownames(installed.packages(priority = c("base", "recommended")))
sha <- function(f) digest::digest(file = f, algo = "sha256")
fingerprint <- function(files) digest::digest(paste(names(files), files, sep = "  ", collapse = "\n"), algo = "sha256", serialize = FALSE)
cfg <- new.env(); sys.source(file.path(code, "R", "config_lowp.R"), cfg)
pins_of <- function(mid) {
  if (mid == "A3") return(unlist(cfg$LOWP_PRODUCTION$A3$A3$PKG_VERSIONS))
  m <- cfg$LOWP_PRODUCTION[[mid]]$METHODS; m <- m[m$method_id == mid, , drop = FALSE]
  setNames(as.character(m$pkg_version), as.character(m$package))
}

fix_provenance <- function(rec, mid) {
  rec$rows$test_library <- if (variant == "test_library") TRUE else FALSE
  rec$environment$test_library <- if (variant == "test_library") TRUE else FALSE
  rec$environment$sealed_library <- if (variant == "wrong_sealed") "/home/someone/else/lib" else PINNED
  si <- rec$environment$sessionInfo
  if (variant != "wrong_r") si <- gsub("4\\.4\\.1", "4.5.2", si)
  rec$environment$sessionInfo <- si
  prov <- rec$environment$package_provenance
  # non-base packages live directly in the pinned library; base / recommended ones in R's own `.../R/library` on NOTS
  for (nm in names(prov)) prov[[nm]]$path <- if (nm %in% base_pkgs) paste0(RLIB, "/", nm) else paste0(PINNED, "/", nm)
  pn <- pins_of(mid)
  for (nm in names(pn)) if (!is.null(prov[[nm]])) prov[[nm]]$version <- unname(pn[[nm]])
  rec$environment$package_provenance <- prov
  cl <- rec$environment$command_line
  cl <- cl[cl != "--test-library"]
  rec$environment$command_line <- gsub(gsub("\\\\", "/", normalizePath(lib, winslash = "/")), PINNED, cl, fixed = TRUE)
  lp <- rec$environment$lib_paths
  if (!is.null(lp)) lp[1] <- PINNED
  rec$environment$lib_paths <- lp
  rec
}
# coefficient edits keep rec$coefficients and rec$fit$coefficients identical (accept requires that; only the intended defect remains)
edit_coef <- function(rec, rule, fn) {
  rec$coefficients[[rule]] <- fn(rec$coefficients[[rule]])
  rec$fit$coefficients <- rec$coefficients
  rec
}
drop_rule <- function(rec, rule) {
  rec$rows <- rec$rows[rec$rows$rule_id != rule, , drop = FALSE]
  rec$coefficients[[rule]] <- NULL
  rec$fit$coefficients <- rec$coefficients
  rec
}
first_live_rule <- function(rec) {
  cf <- rec$coefficients
  for (nm in names(cf)) {
    e <- cf[[nm]]
    if (!identical(e$status, "failed") && !is.null(e$beta_pen) && !anyNA(e$beta_pen)) return(nm)
  }
  NULL
}

hit <- 0L            # number of records actually mutated
once_done <- FALSE   # for the old "first hit overall" variants
mutate <- function(rec, m, ci) {
  first <- ci == 1L
  p <- length(rec$coefficients[[1]]$beta_pen); if (!length(p) || p == 0L) p <- length(rec$fit$beta)
  hit_here <- TRUE
  # ---- old content defects (pinned) ---------------------------------------------------------------------------------------------------------
  if (variant %in% c("no_coef_entry", "beta_pen_short", "beta_ols_short", "support_mismatch") && m == "F1" && first) {
    r <- first_live_rule(rec); if (is.null(r)) stop("F1 has no live rule with coefficients to mutate")
    rec <- switch(variant,
      no_coef_entry = { rec$coefficients[[r]] <- NULL; rec$fit$coefficients <- rec$coefficients; rec },
      beta_pen_short = edit_coef(rec, r, function(e) { e$beta_pen <- e$beta_pen[-length(e$beta_pen)]; e }),
      beta_ols_short = edit_coef(rec, r, function(e) { e$beta_ols <- e$beta_ols[-length(e$beta_ols)]; e }),
      support_mismatch = edit_coef(rec, r, function(e) { j <- which(e$beta_pen == 0)[1]; e$beta_pen[j] <- 0.001; e }))
    return(list(rec = rec, hit = TRUE))
  }
  if (variant == "k37_mismatch" && !once_done && any(grepl("_K37$", rec$rows$rule_id))) {
    i <- which(rec$rows$rule_id == "ebic1_K37"); if (!length(i)) i <- which(grepl("_K37$", rec$rows$rule_id))[1]
    rec$rows$k[i] <- rec$rows$k[i] + 1L
    return(list(rec = rec, hit = TRUE, once = TRUE))
  }
  if (variant == "a_beta_short" && m == "A1" && first) { rec$fit$beta <- rec$fit$beta[-1]; return(list(rec = rec, hit = TRUE)) }
  if (variant %in% c("test_library", "wrong_sealed", "wrong_r")) return(list(rec = rec, hit = TRUE))
  # ---- I1 --------------------------------------------------------------------------------------------------------------------------------------
  if (variant == "i1_f4_all" && m == "F4") return(list(rec = drop_rule(rec, "ebic1_lam005"), hit = TRUE))
  if (variant == "i1_f4_first" && m == "F4" && first) return(list(rec = drop_rule(rec, "ebic1_lam005"), hit = TRUE))
  if (variant == "i1_f5_nosic" && m == "F5" && first) return(list(rec = drop_rule(rec, "sic_smax"), hit = TRUE))
  if (variant == "i1_a1_roles" && m == "A1" && first) { rec$rows$role <- "S0"; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i1_extra_rule" && m == "F2" && first) {
    rec$rows <- rbind(rec$rows, rec$rows[nrow(rec$rows), , drop = FALSE])
    rec$rows$rule_id[nrow(rec$rows)] <- "extra_rule"; rec$rows$role[nrow(rec$rows)] <- "S0"
    e <- rec$coefficients[[nrow(rec$rows) - 1L]]; e$rule_id <- "extra_rule"
    rec$coefficients[["extra_rule"]] <- e
    rec$fit$coefficients <- rec$coefficients
    return(list(rec = rec, hit = TRUE))
  }
  # ---- I2 --------------------------------------------------------------------------------------------------------------------------------------
  if (variant == "i2_ebic1_ols_na" && m == "F1" && first) {
    stopifnot(!identical(rec$coefficients$ebic1$status, "failed"))
    return(list(rec = edit_coef(rec, "ebic1", function(e) { e$beta_ols <- rep(NA_real_, length(e$beta_ols)); e }), hit = TRUE))
  }
  if (variant == "i2_cvmin_ols_finite" && m == "F1" && first) {
    stopifnot(!identical(rec$coefficients$cv_min$status, "failed"))
    return(list(rec = edit_coef(rec, "cv_min", function(e) { e$beta_ols <- e$beta_pen; e }), hit = TRUE))
  }
  if (variant == "i2_betapen_inf" && m == "F1" && first) {
    r <- first_live_rule(rec)
    return(list(rec = edit_coef(rec, r, function(e) { j <- which(e$beta_pen != 0)[1]; if (is.na(j)) j <- 1L; e$beta_pen[j] <- Inf; e }), hit = TRUE))
  }
  if (variant == "i2_a1_nopip" && m == "A1" && first) { stopifnot(!is.null(rec$fit$pip)); rec$fit$pip <- NULL; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i2_a1_pip12" && m == "A1" && first) { stopifnot(!is.null(rec$fit$pip)); rec$fit$pip[1] <- 1.2; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i2_a2_beta_na" && m == "A2" && first) { stopifnot(any(rec$rows$status != "failed")); rec$fit$beta[1] <- NA_real_; return(list(rec = rec, hit = TRUE)) }
  # ---- I3 --------------------------------------------------------------------------------------------------------------------------------------
  if (variant == "i3_data_seed" && m == "F1" && first) { rec$rows$data_seed <- 1L; rec$rows$method_seed <- 4000001L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_fold_seed" && m == "F1" && first) { rec$rows$fold_seed <- rec$rows$fold_seed + 1L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_scale_key" && m == "F1" && first) { stopifnot(all(rec$rows$scale_key == "c100")); rec$rows$scale_key <- "c050"; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_scale" && m == "F1" && first) { rec$rows$scale <- 0.5; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_runid" && m == "F1" && first) { rec$rows$run_id <- "20260101T0000Z_lowp_benchres"; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_y_sha" && m == "F1" && first) { rec$rows$y_sha256 <- ZERO64; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i3_input_hashes" && m == "F1" && first) { rec$input$hashes[["x_sha256"]] <- ZERO64; return(list(rec = rec, hit = TRUE)) }
  # ---- I4 --------------------------------------------------------------------------------------------------------------------------------------
  if (variant == "i4_noprov" && m == "F1" && first) { rec$environment$package_provenance <- NULL; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i4_src_null" && m == "F1" && first) { rec$code$source_sha256 <- NULL; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i4_src_wrong") { rec$code$source_sha256 <- WRONG64; rec$rows$source_sha256 <- WRONG64; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i4_files_hash" && m == "F1" && first) { rec$code$files[1] <- ZERO64; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i4_files_refp" && m == "F1" && first) {   # one file hash changed AND the fingerprint (record + rows) recomputed: only the r2 comparison can see it
    rec$code$files[1] <- ZERO64
    fp <- fingerprint(rec$code$files); rec$code$source_sha256 <- fp; rec$rows$source_sha256 <- fp
    return(list(rec = rec, hit = TRUE))
  }
  if (variant == "i4_pin_version" && m == "F1" && first) { stopifnot(!is.null(rec$environment$package_provenance$glmnet)); rec$environment$package_provenance$glmnet$version <- "0.0.1"; return(list(rec = rec, hit = TRUE)) }
  if (variant == "i4_glmnet_rlib" && m == "F1" && first) { stopifnot(!is.null(rec$environment$package_provenance$glmnet)); rec$environment$package_provenance$glmnet$path <- paste0(RLIB, "/glmnet"); return(list(rec = rec, hit = TRUE)) }
  # ---- N1 (Sol R2): selections ----------------------------------------------------------------------------------------------------------------
  ri <- function(rule) which(rec$rows$rule_id == rule)
  alt_support <- function(sp) {   # a different canonical support of the same size (or "1" for the null model)
    idx <- if (is.na(sp) || !nzchar(sp)) integer() else as.integer(strsplit(sp, ";", fixed = TRUE)[[1]])
    cand <- setdiff(seq_len(p), idx)[1]
    if (length(idx)) paste(sort(c(idx[-length(idx)], cand)), collapse = ";") else as.character(cand)
  }
  if (variant == "n1_cvmin_k" && m == "F1" && first) { rec$rows$k[ri("cv_min")] <- 999L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n1_unsorted" && m == "F1" && first) { i <- ri("ebic1"); rec$rows$support[i] <- "16;3;7;14"; rec$rows$k[i] <- 4L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n1_dup" && m == "F1" && first) { i <- ri("ebic1"); rec$rows$support[i] <- "3;7;7;14"; rec$rows$k[i] <- 4L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n1_pplus1" && m == "F1" && first) { i <- ri("ebic1"); rec$rows$support[i] <- paste0("3;7;", p + 1L); rec$rows$k[i] <- 3L; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n1_a2_support" && m == "A2" && first) {   # selection "20", k 1, beta unchanged
    i <- which(rec$rows$status != "failed")[1]; stopifnot(!is.na(i), !identical(as.character(rec$rows$support[i]), "20"))
    rec$rows$support[i] <- "20"; rec$rows$k[i] <- 1L
    return(list(rec = rec, hit = TRUE))
  }
  if (variant == "n1_a_nosel" && m %in% c("A1", "A2", "A3") && first) { rec$rows$support <- NULL; rec$rows$k <- NULL; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n1_f4_coef_k" && m == "F4" && first) {   # coefficient entry k differs from its row (the row is untouched)
    r <- first_live_rule(rec); stopifnot(!is.null(r), !is.null(rec$coefficients[[r]]$k))
    return(list(rec = edit_coef(rec, r, function(e) { e$k <- e$k + 1L; e }), hit = TRUE))
  }
  if (variant == "n1_a1_rows_support" && m == "A1" && first) {   # row support differs from fit$rules (k unchanged)
    i <- which(rec$rows$status != "failed")[1]; stopifnot(!is.na(i))
    rec$rows$support[i] <- alt_support(as.character(rec$rows$support[i]))
    return(list(rec = rec, hit = TRUE))
  }
  # ---- N2: the bic / bic_K37 pair --------------------------------------------------------------------------------------------------------------
  if (variant == "n2_f4_bic_crit" && m == "F4" && first) { stopifnot("crit_value" %in% names(rec$rows)); rec$rows$crit_value[ri("bic_K37")] <- 99999; return(list(rec = rec, hit = TRUE)) }
  if (variant == "n2_f5_bic_support" && m == "F5" && first) { i <- ri("bic_K37"); rec$rows$support[i] <- alt_support(as.character(rec$rows$support[i])); return(list(rec = rec, hit = TRUE)) }
  if (variant == "n2_f4_bic_k" && m == "F4" && first) { i <- ri("bic_K37"); rec$rows$k[i] <- rec$rows$k[i] + 1L; return(list(rec = rec, hit = TRUE)) }
  # ---- positives that must stay ACCEPTED --------------------------------------------------------------------------------------------------------
  if (variant == "pos_null_sel" && m == "F1" && first) {   # ebic1 and its K37 alias select the null model, consistently everywhere
    for (rule in c("ebic1", "ebic1_K37")) {
      i <- ri(rule); stopifnot(length(i) == 1L, rec$rows$status[i] != "failed")
      rec$rows$support[i] <- ""; rec$rows$k[i] <- if (is.integer(rec$rows$k)) 0L else 0
      rec <- edit_coef(rec, rule, function(e) { e$support <- ""; e$k <- if (is.integer(e$k)) 0L else 0; e$beta_pen <- rep(0, length(e$beta_pen)); e$beta_ols <- rep(0, length(e$beta_ols)); e })
    }
    return(list(rec = rec, hit = TRUE))
  }
  if (variant == "pos_failed_rule" && m == "F1" && first) {   # ebic05 and its K37 alias failed, consistently everywhere
    for (rule in c("ebic05", "ebic05_K37")) {
      i <- ri(rule); stopifnot(length(i) == 1L)
      rec$rows$status[i] <- "failed"; rec$rows$support[i] <- NA_character_; rec$rows$k[i] <- NA
      if ("crit_value" %in% names(rec$rows)) rec$rows$crit_value[i] <- NA
      rec <- edit_coef(rec, rule, function(e) { e$status <- "failed"; e$support <- NA_character_; e$k <- NA
        e$beta_pen <- rep(NA_real_, length(e$beta_pen)); e$beta_ols <- rep(NA_real_, length(e$beta_ols)); e })
    }
    return(list(rec = rec, hit = TRUE))
  }
  list(rec = rec, hit = FALSE)
}

for (m in methods) {
  rds_all <- sort(list.files(res_out, pattern = paste0("^", m, "\\.rds$"), recursive = TRUE, full.names = TRUE))
  if (!length(rds_all)) stop("no ", m, ".rds found")
  for (ci in seq_along(rds_all)) {
    rds <- rds_all[ci]
    rec <- readRDS(rds)
    if (pinned) rec <- fix_provenance(rec, m)
    r <- mutate(rec, m, ci)
    rec <- r$rec
    if (isTRUE(r$once)) once_done <- TRUE
    if (isTRUE(r$hit)) hit <- hit + 1L
    saveRDS(rec, rds)
    d <- dirname(rds)
    csv <- file.path(d, paste0(m, ".csv"))
    utils::write.csv(rec$rows, csv, row.names = FALSE, na = "NA")
    writeLines(paste(c(sha(rds), sha(csv)), c(basename(rds), basename(csv)), sep = "  "), file.path(d, paste0(m, ".sha256")))
  }
}
if (!grepl("^good", variant) && hit == 0L) stop("variant ", variant, " found nothing to mutate")
cat("variant", variant, "mutated records:", hit, "\n")
quit(save = "no", status = 0L)
