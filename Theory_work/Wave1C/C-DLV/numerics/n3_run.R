args <- commandArgs(TRUE)
n <- as.integer(args[1]); p <- as.integer(args[2]); seeds <- as.integer(strsplit(args[3], ",")[[1]])
NUM <- "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-DLV/numerics"
setwd(NUM)
source(file.path(NUM, "core_copy/v3.R")); source(file.path(NUM, "dlv_lib.R"))
for (design in c("M", "F")) for (seed in seeds) {
  tag <- sprintf("%s_n%d_p%d_s%d", design, n, p, seed)
  dat <- make_data(design, n, p, seed)
  fit <- v3_fit(dat$X, dat$y, 1000L + seed, allocation = list(mem_gb = 16, hours = 24))
  out <- list(design = design, n = n, p = p, seed = seed, status = fit$status, S0 = dat$S0, cons = list())
  for (tt in fit$calibration$tiers) for (k in seq_along(tt$grids)) {
    gr <- tt$grids[[k]]; sn <- tt$snapshots[[k]]
    out$cons[[length(out$cons) + 1]] <- list(tier = tt$tier, T_e = tt$settings$T_e, label = gr$label, ok = gr$ok,
      reason = gr$reason, intervals = gr$intervals, grid = gr$grid, schedule = tt$pilot$schedule,
      V_size = sn$size, truncated = sn$truncated,
      models = vapply(sn$models, function(m) paste(sort(as.integer(m)), collapse = "+"), ""),
      log_gamma0 = sn$log_gamma0, d = sn$d)
  }
  jsonlite::write_json(out, file.path("n3", paste0(tag, ".json")), digits = NA, auto_unbox = TRUE)
  cat(tag, fit$status, length(out$cons), "constructions\n", flush = TRUE)
}
