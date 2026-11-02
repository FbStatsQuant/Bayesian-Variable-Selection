# load_all.R -- source the scoring modules. Usage: Sys.setenv(SCORING_DIR = <scoring dir>); source(file.path(<scoring dir>, "R", "load_all.R"))
local({
  d <- Sys.getenv("SCORING_DIR", "")
  if (!nzchar(d)) stop("set SCORING_DIR to the scoring directory before sourcing load_all.R")
  for (f in c("common.R", "truth.R", "extract_smc.R", "extract_exact.R", "extract_bench.R", "td_slow.R", "metrics_smc.R",
              "theory_measures.R", "registry.R", "metrics_selection.R", "tables.R"))
    source(file.path(d, "R", f), local = FALSE)
})
