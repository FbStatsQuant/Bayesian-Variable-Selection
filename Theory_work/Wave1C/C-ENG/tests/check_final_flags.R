# check_final_flags.R -- on the final-code p = 30 regression LS0-on fits: no grid_fallback flag/field on no-failure fits,
# and LS0 move cap = ell_n + |start mode| (C-GROW MR1). Usage: Rscript check_final_flags.R <regress_dir>
fs <- list.files(commandArgs(TRUE)[1], "_on[.]rds$", full.names = TRUE)
x <- vapply(fs, function(f) {
  z <- readRDS(f)$fit
  c(is.null(z$flags$grid_fallback), is.null(z$calibration$grid_fallback),
    identical(z$ls0$move_cap, as.integer(z$budgets$ell + length(z$start_mode$model))), z$ls0$moves < z$budgets$ell)
}, logical(4))
cat("final-code LS0-on fits:", length(fs), "; no grid_fallback flag:", sum(x[1, ]), "; no calibration fallback field:", sum(x[2, ]),
    "; move_cap == ell_n + |start mode|:", sum(x[3, ]), "; LS0 moves < ell_n (cap rule not binding):", sum(x[4, ]), "\n")
