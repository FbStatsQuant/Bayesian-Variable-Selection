# check_env.R -- environment checks before the profiling jobs: the pinned compiler flags are really in force, the
# memory-peak reset works, and regenerated PROD-H datasets match the frozen input manifest (x and y sha256).
source("ws_common.R")
core <- commandArgs(trailingOnly = TRUE)[1]
Sys.setenv(R_MAKEVARS_USER = file.path(core, "cpp", "Makevars.v3"))
td <- tempfile("flags"); dir.create(td); writeLines("int f() { return 1; }", file.path(td, "t.cpp"))
out <- system(paste("cd", td, "&& R CMD SHLIB t.cpp 2>&1"), intern = TRUE)
cat("COMPILE:", out[1], "\n")
cat("FLAGS_OK:", grepl("-ffp-contract=off", out[1], fixed = TRUE) && grepl("-march=x86-64-v2", out[1], fixed = TRUE) && !grepl("march=native", out[1], fixed = TRUE), "\n")
cat("MEM_RESET:", ws_mem_reset(), " mem:", ws_mem(), "\n")
cat("CPU:", sub(".*: ", "", grep("model name", readLines("/proc/cpuinfo"), value = TRUE)[1]), "\n")
gd <- "/home/fb31/projects/BVS/Data_Generation/high_p"; mf <- "/home/fb31/projects/BVS/Data_Generation/manifests/high_p/inputs_manifest.csv"
for (id in list(c(1000, 3, 1), c(500, 1, 1), c(1000, 5, 100), c(500, 6, 50))) {
  d <- ws_prodh(id[1], id[2], id[3], "c100", gd, mf)
  d2 <- ws_prodh(id[1], id[2], id[3], "c050", gd, mf)
  cat("PRODH", d$dataset_id, d$manifest_match, d2$dataset_id, d2$manifest_match, "seed", d$method_seed, "\n")
}
