# toy_fit.R -- environment proof: ONE end-to-end run_one() fit of SMC-BVS on a toy S1-type setting (n = 100, p = 200).
#   Rscript slurm/toy_fit.R --out DIR [--method smcbvs]
# The toy row is S1_03 (rho 0.6, SNR 2, s0 = 10) with n = 100, p = 200, setting_id "TOY_n100_p200", cell 99. It is added
# in memory only (settings.tsv is not touched), so the record is NOT part of any grid. Used to prove a NOTS/Owls
# environment and to measure a NOTS-vs-Owls per-fit speed factor. OURS (operational; no statistical content).
local({
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  source(file.path(dirname(normalizePath(f)), "..", "harness", "run_one.R"))   # defines run_one(); does not run (no --method)
})
.read_settings_orig <- read_settings
read_settings <- function(path) {
  tab <- .read_settings_orig(path)
  toy <- tab[tab$setting_id == "S1_03", ]
  toy$setting_id <- "TOY_n100_p200"; toy$cell <- 99L; toy$n <- 100L; toy$p <- 200L; toy$label <- "TOY n=100 p=200 (env proof)"
  rbind(tab, toy)
}
r <- run_one(OPT$method %||% "smcbvs", "TOY_n100_p200", 1L, OPT$out)
cat(sprintf("TOY %s: status=%s success=%s |sel|=%s runtime=%.1fs host=%s %s\n", r$method, r$status, r$success,
            r$n_selected %||% NA, r$runtime_sec %||% NA, r$host, r$R_version))
quit(status = if (identical(r$status, "ok")) 0 else 1)
