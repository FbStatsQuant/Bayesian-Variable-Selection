# smoke.R -- the gate: every method x 6 combos x 1 seed (rep 1); writes harness/smoke_table.tsv.
#   Rscript harness/smoke.R [--methods smcbvs,lasso_cv,...|available] [--jobs 4] [--timeout_hours 24] [--reuse 1] [--out DIR]
# Combos (SPEC.md §5): S1 SNR = 2 at the 4 (n,p): S1_03 (500,500), S1_07 (500,5000), S1_11 (1000,500), S1_15 (1000,5000);
#   S2 rho = 0.35, beta-type 1, nu = 0.71: S2_016 (high-5: 50,1000,5), S2_076 (high-10: 100,1000,10).
# Each fit is a separate `nice -n 19 timeout <T> Rscript run_one.R` process, single-threaded BLAS/OpenMP
# (OMP/OPENBLAS/MKL/FLEXIBLAS threads = 1), at most --jobs at once (Owls rule: <= 4 cores for this build turn).
# --reuse 1 keeps an existing status-ok record (so the all-methods rerun does not refit SMC-BVS). A fit killed by the
# timeout has no record from run_one; smoke.R then writes one with status "failed: timeout".
# PROVENANCE: INTERFACE.md (smoke gate; zero failures required). No statistical content.
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "methods.R")); suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(methods = "available", jobs = "4", timeout_hours = "24", reuse = "1", out = S1S2_RUNS)
for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
COMBOS <- c("S1_03", "S1_07", "S1_11", "S1_15", "S2_016", "S2_076")
methods <- if (opt$methods == "available") Filter(function(m) method_available(m, BASE), names(S1S2_METHODS)) else strsplit(opt$methods, ",")[[1]]
jobs <- min(as.integer(opt$jobs), 4L)
rec_path <- function(m, s) file.path(opt$out, m, s, "rep_001.json")
grid <- expand.grid(setting = COMBOS, method = methods, stringsAsFactors = FALSE)
grid <- grid[order(match(grid$setting, c("S2_016", "S2_076", "S1_03", "S1_11", "S1_07", "S1_15"))), ]   # cheap first
todo <- which(vapply(seq_len(nrow(grid)), function(i) {
  f <- rec_path(grid$method[i], grid$setting[i])
  !(opt$reuse == "1" && file.exists(f) && identical(tryCatch(fromJSON(f)$status, error = function(e) ""), "ok"))
}, TRUE))
cat(sprintf("smoke: %d methods (%s), %d fits to run, %d reused, jobs = %d\n", length(methods), paste(methods, collapse = ","),
            length(todo), nrow(grid) - length(todo), jobs))
logdir <- file.path(opt$out, "_logs"); dir.create(logdir, recursive = TRUE, showWarnings = FALSE)
envs <- c("OMP_NUM_THREADS=1", "OPENBLAS_NUM_THREADS=1", "MKL_NUM_THREADS=1", "FLEXIBLAS_NUM_THREADS=1",
          paste0("TMPDIR=", file.path(S1S2_ROOT, "tmp", "20261125-S1S2")))
run1 <- function(i) {
  m <- grid$method[i]; s <- grid$setting[i]
  log <- file.path(logdir, sprintf("smoke_%s_%s.log", m, s))
  cmd <- sprintf("env %s nice -n 19 timeout %ds Rscript %s --method %s --setting %s --rep 1 --out %s > %s 2>&1",
                 paste(envs, collapse = " "), as.integer(as.numeric(opt$timeout_hours) * 3600),
                 shQuote(file.path(BASE, "harness", "run_one.R")), m, s, shQuote(opt$out), shQuote(log))
  t0 <- Sys.time(); rc <- system(cmd)
  f <- rec_path(m, s)
  if (!file.exists(f) || difftime(file.info(f)$mtime, t0, units = "secs") < 0) {
    dir.create(dirname(f), recursive = TRUE, showWarnings = FALSE)
    writeLines(toJSON(list(setting_id = s, method = m, rep = 1L, success = FALSE,
                           status = if (rc == 124) "failed: timeout" else sprintf("failed: no record (exit %d)", rc)),
                      auto_unbox = TRUE), f)
  }
  rc
}
if (length(todo)) invisible(parallel::mclapply(todo, run1, mc.cores = jobs, mc.preschedule = FALSE))
rows <- lapply(seq_len(nrow(grid)), function(i) {
  r <- tryCatch(fromJSON(rec_path(grid$method[i], grid$setting[i])), error = function(e) list(status = "failed: unreadable record"))
  g <- function(k) if (is.null(r[[k]])) NA else r[[k]]
  data.frame(method = grid$method[i], combo = grid$setting[i], ok = ifelse(identical(r$status, "ok"), "ok", "fail"),
             runtime_sec = round(as.numeric(g("runtime_sec")), 1), success = g("success"), n_selected = g("n_selected"),
             TP = g("TP"), FP = g("FP"), FN = g("FN"), n = g("n"), p = g("p"), status = r$status, stringsAsFactors = FALSE)
})
tab <- do.call(rbind, rows)
tab <- tab[order(tab$method, match(tab$combo, COMBOS)), ]
write.table(tab, file.path(BASE, "harness", "smoke_table.tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
print(tab[, -12], row.names = FALSE)
cat(sprintf("smoke gate: %d/%d ok; failures: %d\n", sum(tab$ok == "ok"), nrow(tab), sum(tab$ok != "ok")))
