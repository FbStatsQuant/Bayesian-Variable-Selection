# Real CLI parser check (no fit is run): the argument vectors emitted by the ACTUAL bundle scripts (task.sh and p5_task.sh under the stub
# Rscript; recorded in the attempt files by test_shell.sh as vectors_final.txt) are parsed by the real smcbvs_cli_args() of
# code/core/v2_2_1/study/run_case.R, and checked field by field against the specified production vector.
#   Rscript cli_parser.R <path to run_case.R> <vectors_final.txt>
args <- commandArgs(TRUE)
stopifnot(length(args) == 2L)
source(args[[1L]])
lines <- readLines(args[[2L]], warn = FALSE)
lines <- lines[nzchar(lines)]
stopifnot(length(lines) >= 6L)
allowed <- c("case", "scale", "study", "outroot", "run_id", "core_dir", "mem_gb", "hours", "p5_retry")
seen <- list(primary = 0L, p5 = 0L)
for (ln in lines) {
  tok <- strsplit(ln, " ", fixed = TRUE)[[1L]]
  stopifnot(identical(tok[1:2], c("Rscript", "--vanilla")), grepl("/study/run_case\\.R$", tok[3L]))
  v <- tok[-(1:3)]
  parsed <- smcbvs_cli_args(v)                       # the real parser: errors on unknown, duplicate or malformed arguments
  retry <- isTRUE(parsed$p5_retry)
  p <- as.integer(substr(parsed$case, 2L, 5L))
  L <- c(`500` = 6300, `1000` = 24000)[[as.character(p)]]
  stopifnot(setequal(names(parsed), if (retry) allowed else setdiff(allowed, "p5_retry")),   # no seed, no policy, no extra option
            grepl("^p(0500|1000)_S[1-6]_r[0-9]{3}$", parsed$case), parsed$scale %in% c("c100", "c050"),
            identical(parsed$study, "C:/placeholder") || nzchar(parsed$study),
            parsed$mem_gb == "2", isTRUE(all.equal(as.numeric(parsed$hours), L / 3600, tolerance = 1e-9)),
            endsWith(parsed$core_dir, "/code/core/v2_2_1/core"), grepl("_prodH$", parsed$run_id))
  if (retry) seen$p5 <- seen$p5 + 1L else seen$primary <- seen$primary + 1L
  cat(if (retry) "P5     " else "PRIMARY", ": case=", parsed$case, " scale=", parsed$scale, " hours=", parsed$hours, " mem_gb=", parsed$mem_gb,
      if (retry) " --p5-retry" else "", "\n", sep = "")
}
stopifnot(seen$primary >= 4L, seen$p5 >= 2L)
# the parser must reject what the bundle never sends
for (bad in list(c(lines[1L] |> strsplit(" ", fixed = TRUE) |> unlist() |> tail(-3L), "--seed", "1"),
                 c("--case", "p0500_S1_r001")))
  stopifnot(inherits(try(smcbvs_cli_args(bad), silent = TRUE), "try-error"))
cat(sprintf("PASS: real CLI parser accepts %d primary and %d P5 argument vectors of the bundle (hours = L/3600, mem-gb 2, no seed); no fit run\n",
            seen$primary, seen$p5))
