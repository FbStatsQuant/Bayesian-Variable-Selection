root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/controlled_2a8362b2f348"
files <- list.files(root, pattern = "^dev_.*[.]script_exit$", full.names = TRUE)
results <- lapply(files, function(f) {
  stem <- sub("[.]script_exit$", "", basename(f))
  rds <- file.path(root, paste0(stem, ".rds"))
  log <- file.path(root, paste0(stem, ".log"))
  exit <- paste(readLines(f, warn = FALSE), collapse = "")
  if (!identical(exit, "0") || !file.exists(rds) || !file.exists(log))
    return(data.frame(case = stem, ok = FALSE, reason = "missing output or nonzero script exit"))
  lines <- readLines(log, warn = FALSE)
  if (any(grepl("FATAL:|Error:|Execution halted", lines)) || !any(grepl("^finish ", lines)))
    return(data.frame(case = stem, ok = FALSE, reason = "unclean log"))
  d <- tryCatch(readRDS(rds), error = identity)
  if (inherits(d, "error")) return(data.frame(case = stem, ok = FALSE, reason = conditionMessage(d)))
  valid <- identical(d$snapshot_tree, "2a8362b2f348f45bbce4a547ed95ef6455cc704e148d1d799adb804f3acdaa67") &&
    all(d$F1$checks) && all(d$F2$checks) &&
    isTRUE(d$pilot_identical) && isTRUE(d$pilot_identity_original_F1) &&
    all(vapply(d$checks, function(x) all(x$support) && all(x$k37), logical(1))) &&
    nrow(d$F3$result$rules) == 6L &&
    all(d$F3$result$rules$status == "ok")
  data.frame(case = stem, ok = valid, reason = if (valid) "" else "saved check failed")
})
tab <- if (length(results)) do.call(rbind, results) else data.frame(case=character(),ok=logical(),reason=character())
write.csv(tab, file.path(root, "verified_capped.csv"), row.names = FALSE)
print(tab, row.names = FALSE)
cat("verified", nrow(tab), "pass", sum(tab$ok), "fail", sum(!tab$ok), "\n")
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/summarise_capped.R", local = new.env(parent = globalenv()))
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/summarise.R", local = new.env(parent = globalenv()))
if (any(!tab$ok)) quit(save = "no", status = 1L)
