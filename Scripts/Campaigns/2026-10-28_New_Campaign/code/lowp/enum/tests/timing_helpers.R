# timing_helpers.R -- timing records that keep ELAPSED (wall clock) and CPU (process user+sys, all threads) apart and carry
# settings, source hashes and the environment.  Sourced by the t6_* scripts after helpers.R.
env_record <- function() {
  ps <- function(cmd) tryCatch(trimws(system2("powershell", c("-NoProfile", "-Command", shQuote(cmd)), stdout = TRUE, stderr = FALSE)), error = function(e) NA_character_)
  list(timestamp = format(Sys.time(), tz = "UTC", "%Y-%m-%dT%H:%M:%SZ"), host = Sys.info()[["nodename"]], r_version = R.version.string,
       cpu = ps("(Get-CimInstance Win32_Processor).Name")[1], logical_cores = parallel::detectCores(),
       cpu_load_percent_before = suppressWarnings(as.numeric(ps("(Get-CimInstance Win32_Processor).LoadPercentage")[1])),
       enum_source_sha256 = vapply(c("lowp_enum.cpp", "lowp_enum.R", "run_enum_dataset.R", "Makevars.lowp"), function(f) lowp_sha256(file.path(LOWP_ENUM_DIR, f)), ""),
       flags = "-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2 -fopenmp")
}
# Run fun() and return list(value, elapsed_s (wall clock of the call), cpu_s (process user + sys, all threads), env)
timed <- function(fun) {
  env <- env_record(); t0 <- proc.time(); v <- fun(); d <- proc.time() - t0
  list(value = v, elapsed_s = d[["elapsed"]], cpu_s = d[["user.self"]] + d[["sys.self"]], env = env)
}
save_timing <- function(name, rec) {
  dir.create(file.path(TMP, "timing"), showWarnings = FALSE)
  saveRDS(rec, file.path(TMP, "timing", paste0(name, ".rds")))
}
