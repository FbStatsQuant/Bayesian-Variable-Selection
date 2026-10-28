# test_scoring.R: unit tests of score.R and aggregate.R on hand-made fixtures (thread S).
# Usage: Rscript --vanilla tests/test_scoring.R   (from the code folder, or with an absolute path)
#
# Fixture study: p = 500, four datasets (S1 r1, S1 r2, S2 r1, S2 r2), method ids F5 and A1.
#   D1 S1 r1: F5 ebic1 exact, ebic05 extra_only, bic mixed;  A1 pip05 exact, cslead missed_only, bfdr10 null.
#   D2 S1 r2: F5 every rule failed (support_audit kept);    A1 all rules exact but diag_flag (elbo_drop).
#   D3 S2 r1: F5 ebic1 exact, CSV altered after hashing;    A1 y_sha256 wrong, pip05 differs from the RDS PIPs.
#   D4 S2 r2: F5 missing (no files);                        A1 exact on all rules; a stray temp file.
# A second run adds a duplicate rule row, which the aggregation must refuse.

code_dir <- local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(dirname(normalizePath(sub("^--file=", "", a[1])))) else getwd()
})
source(file.path(code_dir, "registry.R"))
source(file.path(code_dir, "score.R"))
source(file.path(code_dir, "aggregate.R"))

n_pass <- 0; n_fail <- 0
check <- function(cond, label) {
  if (isTRUE(cond)) { n_pass <<- n_pass + 1 } else { n_fail <<- n_fail + 1; cat("FAIL:", label, "\n") }
}

p <- 500L
active <- c(3L, 37L, 74L, 106L, 145L, 178L, 213L, 247L, 284L, 316L, 355L, 388L, 423L, 457L)  # §II.3, p = 500
beta <- numeric(p); beta[active] <- rep(c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6), 3)[1:14]
key <- function(idx) paste(sort(idx), collapse = ";")

root <- file.path(tempdir(), "scoring_fixture")
unlink(root, recursive = TRUE)
dir.create(root)
datasets <- data.frame(dataset_id = c("p0500_S1_r001", "p0500_S1_r002", "p0500_S2_r001", "p0500_S2_r002"),
                       scenario = c(1, 1, 2, 2), replicate = c(1, 2, 1, 2), stringsAsFactors = FALSE)
datasets$x_sha256 <- paste0("x", 1:4); datasets$y_c100_sha256 <- paste0("y", 1:4)
datasets$foldid_sha256 <- paste0("f", 1:4); datasets$file_sha256 <- paste0("i", 1:4)
datasets$data_seed <- 1410000 + 10000 * datasets$scenario + datasets$replicate
datasets$fold_seed <- 3410000 + 10000 * datasets$scenario + datasets$replicate
datasets$method_seed <- datasets$data_seed + 4000000
datasets$p <- p

# Truth files and manifests.
dir.create(file.path(root, "truth", "p0500"), recursive = TRUE)
tm <- data.frame(dataset_id = datasets$dataset_id, file_sha256 = NA, active = key(active), stringsAsFactors = FALSE)
for (i in 1:4) {
  f <- file.path(root, "truth", "p0500", paste0(datasets$dataset_id[i], ".rds"))
  saveRDS(list(active = active, beta = beta, dataset_id = datasets$dataset_id[i]), f)
  tm$file_sha256[i] <- file_sha256(f)
}
utils::write.csv(tm, file.path(root, "truth_manifest.csv"), row.names = FALSE)
man <- datasets[, c("dataset_id", "p", "scenario", "replicate", "data_seed", "fold_seed", "method_seed",
                    "file_sha256", "x_sha256", "foldid_sha256", "y_c100_sha256")]
utils::write.csv(man, file.path(root, "inputs_manifest.csv"), row.names = FALSE)

# Rule rows of one fit.
make_rows <- function(run_id, d, method_id, rules, supports, status = "ok", flag = FALSE, codes = "",
                      audit = NA_character_) {
  reg <- REGISTRY[[method_id]]
  n <- length(rules)
  r <- as.data.frame(matrix(NA_character_, n, length(BASE_COLUMNS), dimnames = list(NULL, BASE_COLUMNS)),
                     stringsAsFactors = FALSE)
  r$study <- "bench20261019"; r$run_id <- run_id; r$regime <- "H"; r$p <- p
  r$scenario <- d$scenario; r$replicate <- d$replicate; r$scale_key <- "c100"; r$scale <- 1
  r$dataset_id <- d$dataset_id; r$case_id <- paste0(d$dataset_id, "_c100")
  r$data_seed <- d$data_seed; r$fold_seed <- d$fold_seed; r$method_seed <- d$method_seed
  r$inputs_sha256 <- d$file_sha256; r$x_sha256 <- d$x_sha256; r$y_sha256 <- d$y_c100_sha256; r$fold_sha256 <- d$foldid_sha256
  r$method_id <- method_id; r$rule_id <- rules; r$role <- reg$roles[match(rules, reg$rules)]
  r$status <- status; r$diag_flag <- flag; r$diag_codes <- codes; r$n_warnings <- 0
  r$support <- supports
  r$k <- ifelse(is.na(supports), NA, lengths(strsplit(ifelse(is.na(supports), "", supports), ";")))
  r$support_audit <- audit
  r$runtime_s <- 0.5
  r
}

write_fit <- function(results, d, method_id, rows, pip = NULL, alter_csv_after_hash = FALSE) {
  case_dir <- file.path(results, "p0500", paste0(d$dataset_id, "_c100"))
  dir.create(case_dir, recursive = TRUE, showWarnings = FALSE)
  rds <- file.path(case_dir, paste0(method_id, ".rds")); csv <- file.path(case_dir, paste0(method_id, ".csv"))
  saveRDS(list(rows = rows, fit = list(pip = pip)), rds)
  utils::write.csv(rows, csv, row.names = FALSE, na = "NA")
  writeLines(paste0(file_sha256(c(rds, csv)), "  ", basename(c(rds, csv))), file.path(case_dir, paste0(method_id, ".sha256")))
  writeLines("", file.path(case_dir, paste0(method_id, ".done")))
  if (alter_csv_after_hash) cat("\n", file = csv, append = TRUE)
}

run1 <- "20261019T0000Z_bench20261019_prod_TEST"
res1 <- file.path(root, "results", run1)
D <- lapply(1:4, function(i) datasets[i, ])
extra1 <- 1L; miss <- active[3]
pip_exact <- rep(0.01, p); pip_exact[active] <- 0.97; pip_exact[1] <- 0.2
# D1
write_fit(res1, D[[1]], "F5", make_rows(run1, D[[1]], "F5", c("ebic1", "ebic05", "bic"),
          c(key(active), key(c(active, extra1)), key(c(setdiff(active, miss), extra1)))))
write_fit(res1, D[[1]], "A1", make_rows(run1, D[[1]], "A1", c("pip05", "cslead", "bfdr10"),
          c(key(active), key(setdiff(active, miss)), "")), pip = pip_exact)
# D2
write_fit(res1, D[[2]], "F5", make_rows(run1, D[[2]], "F5", c("ebic1", "ebic05", "bic"), rep(NA, 3),
          status = "failed", audit = key(active)))
write_fit(res1, D[[2]], "A1", make_rows(run1, D[[2]], "A1", c("pip05", "cslead", "bfdr10"), rep(key(active), 3),
          flag = TRUE, codes = "elbo_drop"), pip = pip_exact)
# D3
write_fit(res1, D[[3]], "F5", make_rows(run1, D[[3]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3)),
          alter_csv_after_hash = TRUE)
r <- make_rows(run1, D[[3]], "A1", c("pip05", "cslead", "bfdr10"), rep(key(active), 3)); r$y_sha256 <- "wrong"
pip_off <- pip_exact; pip_off[active[1]] <- 0.4                        # pip05 support would drop active[1]
write_fit(res1, D[[3]], "A1", r, pip = pip_off)
# D4: F5 missing; A1 exact; a stray temp file
write_fit(res1, D[[4]], "A1", make_rows(run1, D[[4]], "A1", c("pip05", "cslead", "bfdr10"), rep(key(active), 3)), pip = pip_exact)
writeLines("x", file.path(res1, "p0500", "p0500_S2_r002_c100", "F5.csv.tmp"))
dir.create(file.path(res1, "p0500", "dev_p0500_S1_r001_c100"))                       # a dev canary bundle
writeLines("x", file.path(res1, "p0500", "dev_p0500_S1_r001_c100", "A1.csv"))
dir.create(file.path(res1, "canary", "p0500", "dev_p0500_S1_r001_c100"), recursive = TRUE)   # nested canary folder
writeLines("x", file.path(res1, "canary", "p0500", "dev_p0500_S1_r001_c100", "F5.csv"))

out1 <- file.path(root, "out1")
res <- score_run(res1, file.path(root, "inputs_manifest.csv"), file.path(root, "truth"),
                 file.path(root, "truth_manifest.csv"), out1, method_ids = c("F5", "A1"), expect = "fixture")
s <- res$scored; pr <- res$problems
row <- function(ds, m, rule) s[s$dataset_id == ds & s$method_id == m & s$rule_id == rule, ]

# Scoring definitions.
x <- row("p0500_S1_r001", "F5", "ebic1")
check(x$tp == 14 && x$fp == 0 && x$fn == 0 && isTRUE(x$exact) && x$error_type == "exact", "exact row")
check(all(unlist(x[sprintf("sel_a%02d", 1:14)]) == 1L), "sel all 1 on exact")
x <- row("p0500_S1_r001", "F5", "ebic05")
check(x$tp == 14 && x$fp == 1 && x$fn == 0 && !x$exact && x$error_type == "extra_only", "extra_only row")
x <- row("p0500_S1_r001", "F5", "bic")
check(x$tp == 13 && x$fp == 1 && x$fn == 1 && x$error_type == "mixed" && x$sel_a03 == 0L && x$sel_a04 == 1L, "mixed row")
x <- row("p0500_S1_r001", "A1", "cslead")
check(x$fp == 0 && x$fn == 1 && x$error_type == "missed_only", "missed_only row")
x <- row("p0500_S1_r001", "A1", "bfdr10")
check(x$tp == 0 && x$fp == 0 && x$fn == 14 && x$error_type == "missed_only" && x$sel_a01 == 0L, "null support row")
x <- row("p0500_S1_r002", "F5", "ebic1")
check(x$error_type == "failed" && identical(x$exact, FALSE) && is.na(x$tp) && is.na(x$sel_a01), "failed row, support_audit not scored")
# PIPs.
x <- row("p0500_S1_r001", "A1", "pip05")
check(all(unlist(x[sprintf("pip_a%02d", 1:14)]) == 0.97) && x$max_pip_null == 0.2, "pip columns and max_pip_null")
check(all(is.na(row("p0500_S1_r001", "F5", "ebic1")[sprintf("pip_a%02d", 1:14)])), "no PIPs for F5")
# Checks.
check(any(pr$check == "case_missing" & pr$case_id == "p0500_S2_r002_c100" & pr$method_id == "F5"), "missing case reported")
check(any(pr$check == "sha256_check" & pr$case_id == "p0500_S2_r001_c100" & grepl("F5.csv hash mismatch", pr$detail)), "hash mismatch reported")
check(sum(pr$check == "y_sha256_mismatch") == 3, "y hash mismatch on the three A1 rows of D3")
check(any(pr$check == "pip05_support_differs_from_rds_pip" & pr$case_id == "p0500_S2_r001_c100"), "pip05 vs RDS PIP check")
check(any(res$extra$rel == "p0500/p0500_S2_r002_c100/F5.csv.tmp" & res$extra$kind == "orphan"), "stray file listed as orphan")
check(any(res$extra$rel == "p0500/dev_p0500_S1_r001_c100/A1.csv" & res$extra$kind == "dev_canary"), "dev canary labelled and excluded")
check(any(res$extra$rel == "canary/p0500/dev_p0500_S1_r001_c100/F5.csv" & res$extra$kind == "dev_canary"), "nested dev canary labelled")
check(sum(res$coverage$state == "missing") == 1 && sum(res$coverage$state == "complete") == 7, "coverage states")
check(!any(pr$check %in% c("x_sha256_mismatch", "run_id_mismatch", "duplicate_rule_row", "k_mismatch",
                           "diag_flag_code_disagree", "seed_mismatch")), "no spurious problems")
check(nrow(s) == 3 * 3 + 3 * 4, "scored row count")

# Aggregation: run 1 has integrity problems, so it must refuse unless explicitly allowed.
check(inherits(try(aggregate_run(out1), silent = TRUE), "try-error"), "aggregation refuses integrity problems")
long <- aggregate_run(out1, allow_problems = TRUE)
cell <- function(m, rule, sc) long[long$method_id == m & long$rule_id == rule & long$scenario == sc, ]
x <- cell("F5", "ebic1", "1")
check(x$exact_all == 1 && x$n_expected == 2 && x$n_failed == 1 && x$n_fail_total == 1 && x$exact_among_success == 1, "F5 ebic1 S1")
x <- cell("F5", "ebic1", "2")
check(x$exact_all == 1 && x$n_missing == 1 && x$n_fail_total == 1 && x$n_success == 1, "F5 ebic1 S2 with a missing case")
x <- cell("F5", "ebic1", "pooled")
check(x$exact_all == 2 && x$n_expected == 4 && x$n_fail_total == 2, "F5 ebic1 pooled")
x <- cell("F5", "ebic05", "1")
check(x$sum_fp == 1 && x$mean_fp == 1 && x$err_extra_only == 1 && x$err_failed == 1, "F5 ebic05 S1 T3")
x <- cell("A1", "pip05", "1")
check(x$exact_all == 2 && x$exact_passing == 1 && x$n_flagged == 1, "A1 all-saved vs passing-only")
x <- cell("A1", "bfdr10", "1")
check(x$mean_fn == 7 && x$sum_fn == 14, "A1 bfdr10 mean FN")
t1 <- utils::read.csv(file.path(out1, "T1.csv"))
check(setequal(paste(t1$method_id, t1$rule_id), c("F5 ebic1", "A1 pip05")), "T1 holds the primary rules only for F5/A1")
t4 <- utils::read.csv(file.path(out1, "T4_by_variable.csv"))
x <- t4[t4$method_id == "F5" & t4$scenario == "1" & t4$signal == "a01", ]
check(x$n_selected == 1 && x$n_expected == 2 && x$abs_beta == 1.4 && abs(x$rho_S6 - 0.4) < 1e-12, "T4 F5 S1 a01")
x <- t4[t4$method_id == "F5" & t4$scenario == "1" & t4$signal == "a06", ]
check(abs(x$rho_S6 - 0.9) < 1e-12 && x$abs_beta == 1.6, "T4 rho/beta pairing a06")
t6 <- utils::read.csv(file.path(out1, "codes_by_rule.csv"))
check(t6$count[t6$method_id == "A1" & t6$rule_id == "pip05" & t6$scenario == "pooled" & t6$code == "elbo_drop"] == 1, "flag code counted")
check(file.exists(file.path(out1, "summary.md")), "summary written")
# Full precision: doubles are printed with 17 significant digits and read back exactly.
tmp <- file.path(root, "prec.csv")
write_table(data.frame(a = 1 / 3, b = 2L, c = "x", d = NA_real_), tmp)
txt <- readLines(tmp)
check(identical(txt[2], '0.33333333333333331,2,"x",NA'), "write_table prints %.17g, unquoted")
check(identical(utils::read.csv(tmp)$a, 1 / 3), "17-digit double reads back identical")
lr <- utils::read.csv(file.path(out1, "rules_long.csv"))
check(all(is.na(lr$mean_fn) | lr$mean_fn == lr$sum_fn / lr$n_success), "means equal sum / n exactly after reading back")
t4g <- utils::read.csv(file.path(out1, "T4_by_group.csv"), colClasses = "character")
check(setequal(unique(t4g$rho_S6), c("0.4", "0.5", "0.6", "0.7", "0.8", "0.9")), "rho labels clean")

# Post-hoc derived rule (score_derived.R): rows copied from the production ebic1 rows of run 1.
code_dir_saved <- code_dir
source(file.path(code_dir, "score_derived.R"))
code_dir <- code_dir_saved          # score_derived.R sets its own code_dir when sourced
der <- do.call(rbind, lapply(1:3, function(i) {
  case_dir <- file.path(res1, "p0500", paste0(D[[i]]$dataset_id, "_c100"))
  x <- read_rule_csv(file.path(case_dir, "F5.csv")); x <- x[x$rule_id == "ebic1", ]
  x$rule_id <- "ebic1_K37"; x$role <- "S0_posthoc"; x
}))
der$x_sha256[1] <- "tampered"                                            # D1: provenance differs
der_csv <- file.path(root, "derived.csv"); utils::write.csv(der, der_csv, row.names = FALSE, na = "NA")
outp <- file.path(root, "out_posthoc")
rp <- score_derived(der_csv, out1, file.path(root, "inputs_manifest.csv"), file.path(root, "truth"),
                    file.path(root, "truth_manifest.csv"), outp, rule = "ebic1_K37", role = "S0_posthoc",
                    cap = 37, method_ids = "F5")
pcp <- rp$problems
check(any(pcp$check == "provenance_differs_from_production" & pcp$detail == "x_sha256" & pcp$case_id == "p0500_S1_r001_c100"), "posthoc provenance vs production")
check(any(pcp$check == "x_sha256_mismatch"), "posthoc provenance vs manifest")
check(any(pcp$check == "missing_row" & grepl("p0500_S2_r002_c100 F5", pcp$detail)), "posthoc missing case")
check(!any(pcp$check %in% c("rule_id_mismatch", "role_mismatch", "missing_rule_row", "unregistered_rule_row")), "posthoc rule/role accepted")
x <- rp$long[rp$long$scenario == "pooled" & rp$long$p == 500, ]
check(x$exact_all == 2 && x$n_expected == 4 && x$n_failed == 1 && x$n_missing == 1, "posthoc S-table counts")
check(all(rp$changes$n_support_changed == 0) && all(grepl("post hoc", rp$long$label)), "posthoc changes and label")

# Second run: a duplicate rule row must be detected and must block the aggregation.
run2 <- "20261019T0001Z_bench20261019_prod_TEST"
res2 <- file.path(root, "results", run2)
for (i in 1:4) {
  rr <- make_rows(run2, D[[i]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3))
  if (i == 1) rr <- rbind(rr, rr[1, ])
  write_fit(res2, D[[i]], "F5", rr)
}
out2 <- file.path(root, "out2")
r2 <- score_run(res2, file.path(root, "inputs_manifest.csv"), file.path(root, "truth"),
                file.path(root, "truth_manifest.csv"), out2, method_ids = "F5", expect = "fixture")
check(any(r2$problems$check == "duplicate_rule_row") && any(r2$problems$check == "duplicate_case_method_rule"), "duplicate detected")
check(inherits(try(aggregate_run(out2), silent = TRUE), "try-error"), "aggregation refuses duplicates")

# Fifth run (c = 0.5 layout, derived rows): scale detected from folders; derived rows merged.
run5 <- "20261022T0000Z_bench20261019_prodc050_F5_ABESS"
res5 <- file.path(root, "results", run5)
man5 <- man; man5$y_c050_sha256 <- paste0("h", 1:4); utils::write.csv(man5, file.path(root, "inputs_manifest5.csv"), row.names = FALSE)
der5 <- list()
for (i in 1:4) {
  d5 <- D[[i]]; d5$y_c100_sha256 <- man5$y_c050_sha256[i]
  rr <- make_rows(run5, d5, "F5", c("ebic1", "ebic05", "bic"), c(key(c(active, setdiff(1:40, active))), rep(key(active), 2)))
  rr$case_id <- paste0(d5$dataset_id, "_c050"); rr$scale_key <- "c050"; rr$scale <- 0.5
  case_dir <- file.path(res5, "p0500", rr$case_id[1]); dir.create(case_dir, recursive = TRUE)
  rds <- file.path(case_dir, "F5.rds"); csv <- file.path(case_dir, "F5.csv")
  saveRDS(list(rows = rr), rds); utils::write.csv(rr, csv, row.names = FALSE, na = "NA")
  writeLines(paste0(file_sha256(c(rds, csv)), "  ", c("F5.rds", "F5.csv")), file.path(case_dir, "F5.sha256"))
  writeLines("", file.path(case_dir, "F5.done"))
  dd <- rr[c(1, 1, 1, 1), ]; dd$rule_id <- DERIVED_REGISTRY$F5$rules; dd$role <- DERIVED_REGISTRY$F5$roles
  dd$support <- key(active); dd$k <- 14; dd$derived_from <- if (i == 3) "wronghash" else file_sha256(rds)
  if (i != 4) der5[[i]] <- dd                                             # case 4: derived rows missing
}
der5_csv <- file.path(root, "derived5.csv"); utils::write.csv(do.call(rbind, der5), der5_csv, row.names = FALSE, na = "NA")
out5 <- file.path(root, "out5")
r5 <- score_run(res5, file.path(root, "inputs_manifest5.csv"), file.path(root, "truth"), file.path(root, "truth_manifest.csv"),
                out5, method_ids = "F5", expect = "fixture", scale_key = "auto", derived_csv = der5_csv)
pc5 <- r5$problems$check
check(all(r5$scored$scale_key == "c050") && nrow(r5$scored) == 4 * 3 + 3 * 4, "c050 scale detected; derived rows merged")
check(any(pc5 == "derived_from_differs_from_rds_hash") && any(pc5 == "derived_rows_missing"), "derived provenance and missing rows reported")
check(!any(pc5 %in% c("unregistered_rule_row", "role_mismatch", "y_sha256_mismatch")), "derived rules registered; c050 y hash checked")
check(inherits(try(aggregate_run(out5), silent = TRUE), "try-error"), "derived problems block aggregation")
lg5 <- aggregate_run(out5, allow_problems = TRUE)
x <- lg5[lg5$rule_id == "ebic1_K37" & lg5$scenario == "pooled" & lg5$p == 500, ]
check(x$role == "primary" && grepl("^pre-registered", x$label) && x$exact_all == 3 && x$n_missing == 1, "K37 primary row, label, counts")
x <- lg5[lg5$rule_id == "ebic1" & lg5$scenario == "pooled" & lg5$p == 500, ]
check(x$n_k_gt_K == 4 && x$label == "pre-declared", "k_gt_K counted on the cap-100 rule")
t1_5 <- utils::read.csv(file.path(out5, "T1.csv"))
check(setequal(t1_5$rule_id, c("ebic1", "ebic1_K37")), "T1 holds both primary rows for F5")

# Other-scale canary inside a c050 run: excluded and labelled, scoring at the explicit scale.
dir.create(file.path(res5, "p0500", "p0500_S1_r001_c100")); writeLines("x", file.path(res5, "p0500", "p0500_S1_r001_c100", "F5.csv"))
check(inherits(try(score_run(res5, file.path(root, "inputs_manifest5.csv"), file.path(root, "truth"), file.path(root, "truth_manifest.csv"),
                             file.path(root, "out5b"), method_ids = "F5", expect = "fixture", scale_key = "auto"), silent = TRUE), "try-error"),
      "auto scale refuses a run with two scales")
r5b <- score_run(res5, file.path(root, "inputs_manifest5.csv"), file.path(root, "truth"), file.path(root, "truth_manifest.csv"),
                 file.path(root, "out5b"), method_ids = "F5", expect = "fixture", scale_key = "c050", derived_csv = der5_csv)
check(any(r5b$extra$kind == "other_scale_canary") && !any(r5b$extra$kind == "orphan") && all(r5b$scored$scale_key == "c050"),
      "other-scale canary labelled and excluded")

# Paired c = 1 vs c = 0.5 table: c050 rows of run 5 against a c100 copy with known differences.
source(file.path(code_dir, "pair.R"))
pd5 <- file.path(root, "pair", "c050", run5); pd1 <- file.path(root, "pair", "c100", "20261019T0000Z_bench20261019_prod_F5_ABESS")
dir.create(pd5, recursive = TRUE); dir.create(pd1, recursive = TRUE)
s5 <- utils::read.csv(file.path(root, "out5b", "scored_rows.csv"), colClasses = "character")
utils::write.csv(s5, file.path(pd5, "scored_rows.csv"), row.names = FALSE)
s1 <- s5; s1$scale_key <- "c100"
s1$exact[s1$rule_id == "ebic1"] <- "TRUE"                                   # c050 ebic1: 0 exact (k = 40); c100: 4
s1$exact[s1$rule_id == "ebic05" & s1$dataset_id == "p0500_S1_r001"] <- "FALSE"
utils::write.csv(s1, file.path(pd1, "scored_rows.csv"), row.names = FALSE)
pr <- pair_runs(file.path(root, "pair", "c050"), file.path(root, "pair", "c100"), file.path(root, "pair"))
x <- pr[pr$rule_id == "ebic1" & pr$p == 500 & pr$scenario == "pooled", ]
check(x$n_pairs == 4 && x$exact_c100 == 4 && x$exact_c050 == 0 && x$c100_only == 4, "paired counts ebic1")
x <- pr[pr$rule_id == "ebic05" & pr$p == 500 & pr$scenario == "1", ]
check(x$n_pairs == 2 && x$both == 1 && x$c050_only == 1 && x$neither == 0, "paired counts ebic05 S1")
x <- pr[pr$rule_id == "ebic1_K37" & pr$p == 500 & pr$scenario == "pooled", ]
check(x$n_pairs == 3 && x$n_unpaired == 0 && grepl("^post hoc", x$label_c100) && grepl("^pre-registered", x$label_c050), "derived rule paired with labels")

# SuSiE-refine arm (PREREG_c050 R4): registered as S1/S0/S0 with PIPs, labelled by scale.
check(identical(REGISTRY[["SuSiE-refine"]]$roles, c("S1", "S0", "S0")) && "SuSiE-refine" %in% PIP_METHODS &&
      identical(RUN_METHODS[[sub("^.*_prod(c[0-9]{3})?_", "", "20261021T1819Z_bench20261019_prodc100_SuSiErefine")]], "SuSiE-refine"), "SuSiE-refine registered")
check(grepl("^arm added after the c = 1", rule_label("SuSiE-refine", "pip05", "c100")) &&
      grepl("^pre-registered arm", rule_label("SuSiE-refine", "cslead", "c050")), "SuSiE-refine labels")

# A3 ESS-flag listing (a3_flags.R): flagged fits listed; passing counts exclude them.
source(file.path(code_dir, "a3_flags.R"))
mk <- function(sk, flags, exact) {
  d <- file.path(root, "a3", sk); dir.create(d, recursive = TRUE)
  n <- length(flags)
  r <- data.frame(method_id = "A3", rule_id = rep(c("ci95", "km2"), each = n), scale_key = sk, run_id = "R",
                  case_id = rep(paste0("p1000_S1_r00", 1:n, "_", sk), 2), dataset_id = rep(paste0("p1000_S1_r00", 1:n), 2),
                  p = 1000, scenario = 1, replicate = rep(1:n, 2), diag_flag = rep(ifelse(flags, "TRUE", "FALSE"), 2),
                  diag_codes = rep(ifelse(flags, "ess_tau", ""), 2), k = 14, exact = rep(exact, 2), stringsAsFactors = FALSE)
  utils::write.csv(r, file.path(d, "scored_rows.csv"), row.names = FALSE); d
}
af <- a3_flags(mk("c050", c(TRUE, FALSE, FALSE), c("TRUE", "TRUE", "FALSE")), mk("c100", c(FALSE, TRUE, FALSE), c("TRUE", "TRUE", "TRUE")), file.path(root, "a3"))
x5 <- af$cells[af$cells$scale_key == "c050" & af$cells$p == 1000 & af$cells$scenario == "1", ]
check(nrow(af$cases) == 2 && x5$n_flagged == 1 && x5$ci95_exact_all == 2 && x5$ci95_exact_passing == 1 && x5$n_ess_tau == 1, "A3 flag listing and passing counts")

# k_gt_K (PREREG_c050 R1): counted for every F-family rule, CV rules included; NA for A-family non-size rules.
rk <- data.frame(status = c("ok", "ok", "ok", "failed"), k = c("57", "37", "38", NA), stringsAsFactors = FALSE)
check(count_k_gt_K(rk, "cv_1se", "F1") == 2 && count_k_gt_K(rk, "cv_min", "F3") == 2, "k_gt_K counted on F1-F3 CV rules")
check(count_k_gt_K(rk, "ebic1", "F5") == 2 && is.na(count_k_gt_K(rk, "pip05", "A1")), "k_gt_K on size rules; NA on A1 pip05")

# Fourth run (review reproductions): CSV design columns disagree with the folder, invalid status,
# lower-case diag_flag, header-only CSV, seed written as a double. Each must be reported and block.
run4 <- "20261019T0002Z_bench20261019_prod_TEST"
res4 <- file.path(root, "results", run4)
rr <- make_rows(run4, D[[1]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3)); rr$scenario <- 2
write_fit(res4, D[[1]], "F5", rr)
rr <- make_rows(run4, D[[2]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3)); rr$status[1] <- "error"; rr$diag_flag <- "true"
write_fit(res4, D[[2]], "F5", rr)
rr <- make_rows(run4, D[[3]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3))
write_fit(res4, D[[3]], "F5", rr[0, ])
rr <- make_rows(run4, D[[4]], "F5", c("ebic1", "ebic05", "bic"), rep(key(active), 3))
rr$data_seed <- format(as.numeric(rr$data_seed), scientific = TRUE, digits = 15)
write_fit(res4, D[[4]], "F5", rr)
out4 <- file.path(root, "out4")
r4 <- score_run(res4, file.path(root, "inputs_manifest.csv"), file.path(root, "truth"),
                file.path(root, "truth_manifest.csv"), out4, method_ids = "F5", expect = "fixture")
pc <- r4$problems$check
check(any(pc == "design_mismatch" & r4$problems$case_id == "p0500_S1_r001_c100"), "design mismatch reported")
check(all(r4$scored$scenario[r4$scored$dataset_id == "p0500_S1_r001"] == "1"), "design columns taken from the manifest")
check(any(pc == "status_invalid") && any(pc == "diag_flag_invalid"), "invalid status and flag reported")
check(any(pc == "csv_unreadable_or_empty" & r4$problems$case_id == "p0500_S2_r001_c100"), "header-only CSV reported")
check(!any(pc == "seed_mismatch"), "seed in scientific notation compares equal")
check(inherits(try(aggregate_run(out4), silent = TRUE), "try-error"), "aggregation refuses run 4")

# Third: a truth file that does not match its manifest must stop the scoring.
saveRDS(list(active = active[-1], beta = beta), file.path(root, "truth", "p0500", "p0500_S1_r001.rds"))
check(inherits(try(score_run(res2, file.path(root, "inputs_manifest.csv"), file.path(root, "truth"),
                             file.path(root, "truth_manifest.csv"), file.path(root, "out3"), method_ids = "F5", expect = "fixture"),
                   silent = TRUE), "try-error"), "tampered truth stops scoring")

cat(sprintf("\ntest_scoring: %d passed, %d failed\n", n_pass, n_fail))
if (n_fail > 0) quit(status = 1)
