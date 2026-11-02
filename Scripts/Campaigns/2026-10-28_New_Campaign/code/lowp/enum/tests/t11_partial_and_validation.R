# Check 11: partial runs are labelled; lowp_exact / lowp_td argument validation; overflow guards.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load(); cpp <- .lowp$cpp
res <- list(); chk <- function(name, ok, note = "") { res[[length(res) + 1]] <<- data.frame(test = name, pass = isTRUE(ok), note = note); cat(sprintf("%-4s %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", name, note)) }
errs <- function(expr) tryCatch({ force(expr); FALSE }, error = function(e) TRUE)

## --- partial runs -------------------------------------------------------------------------------------------------
p <- 12; X <- gen_design(p, "block", seed = 5); Y <- gen_response(X, c(2, 7, 11), c(1.4, -1, 1.8)); Yl <- list(c100 = Y[, 1], c050 = Y[, 2])
full <- lowp_exact(X, Yl, task_bits = 3)
chk("full run: status exact, scope full, complete, global_certified from the comparison", identical(attr(full, "run")$status, "exact") && isTRUE(attr(full, "run")$complete) && identical(full$c100$scope, "full") && identical(full$c100$global_certified, full$c100$certified_over_scored_models))
w <- NULL; part <- withCallingHandlers(lowp_exact(X, Yl, task_bits = 3, task_subset = 0L), warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") })
run <- attr(part, "run")
chk("task_subset = 0 (the reviewer's case): status partial, 512 of 4096 models, warning", identical(run$status, "partial") && run$models_scored == 512 && run$models_expected == 4096 && !isTRUE(run$complete) && !is.null(w), w)
chk("  scale records: scope restricted, global_certified FALSE, status partial, bound kind kept", all(vapply(part, function(z) identical(z$scope, "restricted_to_scored_models") && identical(z$global_certified, FALSE) && identical(z$status, "partial") && identical(z$certificate_bound_kind, "heuristic (not a validated interval bound)"), TRUE)),
    paste("certified_over_scored_models =", part$c100$certified_over_scored_models))
part2 <- suppressWarnings(lowp_exact(X, Yl, prefix_fraction = 0.25))
chk("prefix_fraction = 0.25: partial, not globally certified", identical(attr(part2, "run")$status, "partial") && !part2$c100$global_certified && attr(part2, "run")$models_scored < 4096)
all_tasks <- lowp_exact(X, Yl, task_bits = 3, task_subset = 0:7)
chk("task_subset covering every task is complete and equals the full run", identical(attr(all_tasks, "run")$status, "exact") && identical(all_tasks$c100$log_Z, full$c100$log_Z) && identical(all_tasks$c100$global_certified, full$c100$global_certified))
pf1 <- lowp_exact(X, Yl, prefix_fraction = 1)
chk("prefix_fraction = 1 is complete", identical(attr(pf1, "run")$status, "exact"))
## K < p: full coverage is |S| <= K
Xs <- gen_design(10, "block", n = 12, seed = 12); Ys <- gen_response(Xs, c(2, 5, 7), c(1.4, -1, 1.8), seed = 3)
small <- lowp_exact(Xs, list(c100 = Ys[, 1]), task_bits = 3)
chk("K < p (n = 12, p = 10, K = 6): complete with sum_{k<=6} choose(10,k) = 848 models", identical(attr(small, "run")$status, "exact") && attr(small, "run")$models_scored == sum(choose(10, 0:6)) && attr(small, "run")$models_expected == 848)

## --- lowp_exact argument validation -----------------------------------------------------------------------------
chk("task_bits = -1 rejected", errs(lowp_exact(X, Yl, task_bits = -1)))
chk("task_bits = 21 rejected", errs(lowp_exact(X, Yl, task_bits = 21)))
chk("task_bits = 2.5 / NA rejected", errs(lowp_exact(X, Yl, task_bits = 2.5)) && errs(lowp_exact(X, Yl, task_bits = NA_real_)))
chk("threads = 0 / negative / NA rejected", errs(lowp_exact(X, Yl, threads = 0)) && errs(lowp_exact(X, Yl, threads = -2)) && errs(lowp_exact(X, Yl, threads = NA)))
chk("top = 1 rejected", errs(lowp_exact(X, Yl, top = 1)))
chk("task_subset out of range / negative rejected", errs(lowp_exact(X, Yl, task_bits = 3, task_subset = 8L)) && errs(lowp_exact(X, Yl, task_bits = 3, task_subset = -1L)))
chk("prefix_fraction 0 / 1.5 rejected", errs(lowp_exact(X, Yl, prefix_fraction = 0)) && errs(lowp_exact(X, Yl, prefix_fraction = 1.5)))
pr <- lowp_prepare(X, Yl)
chk("C++ also rejects task_bits = -3 and threads = 0 when called directly", errs(cpp$cpp_enum(pr$X, pr$Y, pr$orig, 1000L, 1L, -3L, integer(0), 0L, 1e-8, integer(0), FALSE)) && errs(cpp$cpp_enum(pr$X, pr$Y, pr$orig, 1000L, 0L, 3L, integer(0), 0L, 1e-8, integer(0), FALSE)))
Xbig <- matrix(rnorm(200 * 41), 200); ybig <- rnorm(200)
chk("p = 41 rejected (supported domain p <= 30 for the campaign, <= 40 for tests)", errs(lowp_exact(Xbig, list(y = ybig))))
Xwide <- cbind(matrix(rnorm(200 * 3), 200), 1, matrix(rnorm(200 * 2), 200)); Xwide <- cbind(Xwide, matrix(0, 200, 0))
chk("dropped constant column: original-index map kept (names of pip skip the dropped one)", identical(names(lowp_exact(Xwide, list(y = rnorm(200)), task_bits = 2)$y$pip), c("1", "2", "3", "5", "6")))

## --- lowp_td validation (the reviewer's case: n = 10, p = 8, truth {2,4,7}) ----------------------------------------
X8 <- gen_design(8, "block", n = 10, seed = 1); y8 <- gen_response(X8, c(2, 4, 7), c(1.4, -1, 1.8), cs = c(c100 = 1), seed = 2)[, 1]
chk("d = -1 with max_scores = 1000 rejected before counting", errs(lowp_td(X8, y8, c(2, 4, 7), d = -1, max_scores = 1000)))
chk("d = 1.5 / NA / Inf / vector rejected", errs(lowp_td(X8, y8, c(2, 4, 7), d = 1.5)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = NA)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = Inf)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = c(0, 1))))
chk("duplicated truth {2,2,4} rejected", errs(lowp_td(X8, y8, c(2, 2, 4), d = 0)))
chk("duplicated null_pool rejected", errs(lowp_td(X8, y8, c(2, 4, 7), d = 1, null_pool = c(1, 1, 3))))
chk("null_pool intersecting the truth rejected", errs(lowp_td(X8, y8, c(2, 4, 7), d = 1, null_pool = c(1, 2))))
chk("truth / pool outside the columns, NA, non-integer rejected", errs(lowp_td(X8, y8, c(2, 4, 9), d = 0)) && errs(lowp_td(X8, y8, c(2, NA, 4), d = 0)) && errs(lowp_td(X8, y8, c(2, 4.5), d = 0)) && errs(lowp_td(X8, y8, c(2, 4), d = 1, null_pool = c(1, 99))))
chk("empty truth rejected; truth larger than K = 5 rejected", errs(lowp_td(X8, y8, integer(0), d = 0)) && errs(lowp_td(X8, y8, 1:6, d = 0)))
chk("negative margin (-1, -1e-9) rejected in R and in C++", errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = -1)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = -1e-9)) && errs(cpp$cpp_td(lowp_prepare(X8, list(y = y8))$X, y8, 1:8, c(2L, 4L, 7L), c(1L, 3L), 0L, -1, 1L, FALSE)))
chk("margin NaN / Inf / NA / vector rejected", errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = NaN)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = Inf)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = NA_real_)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, margin = c(0, 1))))
chk("threads = 0 / max_scores = -1 / NA / keep_all NA rejected", errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, threads = 0)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, max_scores = -1)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, max_scores = NA)) && errs(lowp_td(X8, y8, c(2, 4, 7), d = 0, keep_all = NA)))
pr8 <- lowp_prepare(X8, list(y = y8))
chk("C++ rejects d = -1, duplicate truth, non-finite margin when called directly", errs(cpp$cpp_td(pr8$X, pr8$Y[, 1], pr8$orig, c(2L, 4L, 7L), c(1L, 3L), -1L, 0, 1L, FALSE)) && errs(cpp$cpp_td(pr8$X, pr8$Y[, 1], pr8$orig, c(2L, 2L, 4L), c(1L, 3L), 0L, 0, 1L, FALSE)) && errs(cpp$cpp_td(pr8$X, pr8$Y[, 1], pr8$orig, c(2L, 4L), c(1L, 3L), 0L, NaN, 1L, FALSE)))
ok <- lowp_td(X8, y8, c(2, 4, 7), d = 2, max_scores = 1e6)
chk("valid call still works: scores used = closed form", !ok$dry_run && ok$scores_used == ok$scores_needed && ok$count_exact)
## overflow guards
Xp <- gen_design(60, "indep", n = 200, seed = 4); yp <- rnorm(200)
dr <- lowp_td(Xp, yp, c(1, 2, 3), d = 30, max_scores = 1e6)
chk("huge d with a small max_scores: dry-run record, count flagged inexact (>= 2^53)", isTRUE(dr$dry_run) && identical(dr$count_exact, FALSE) && dr$scores_needed > 2^53, paste("scores_needed =", format(dr$scores_needed, digits = 4)))
chk("huge d with max_scores = Inf: run refused", errs(lowp_td(Xp, yp, c(1, 2, 3), d = 30)))
chk("C++ guard on the number of pool subsets (d = 30, npool = 57)", errs(cpp$cpp_td(lowp_prepare(Xp, list(y = yp))$X, yp, 1:60, c(1L, 2L, 3L), 4:60, 30L, 0, 1L, FALSE)))
R <- do.call(rbind, res); cat(sprintf("\n%d of %d checks passed\n", sum(R$pass), nrow(R)))
