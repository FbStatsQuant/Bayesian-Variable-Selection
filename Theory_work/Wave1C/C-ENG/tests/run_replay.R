# run_replay.R -- merged-LS0 replay designs (METHOD_v3.1_FINAL §6 item 2: S1 r001, S4 r001, S5 r002) at production
# settings, with the repository dev generator (Scripts/SMC_BVS/smoke/reference/gen_dev_data.R, generate_dev_dataset;
# p = 500, n = 200, scale c100, method seed = data seed + 4e6). Dev inputs, not the study's production datasets.
# Usage: Rscript run_replay.R <core_dir> <work_dir> <mode: on|proto|old> <out_dir> <scenario> <replicate> [p]
args <- commandArgs(TRUE)
core <- args[1]; work <- args[2]; mode <- args[3]; outdir <- args[4]; scen <- as.integer(args[5]); rep <- as.integer(args[6])
p <- if (length(args) >= 7) as.integer(args[7]) else 500L
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R"))
if (mode == "proto") { source(file.path(here, "proto_load.R")); proto_load(core, work) } else ceng_load(core, work, exports = FALSE)
gen <- file.path(here, "..", "..", "..", "..", "Scripts", "SMC_BVS", "smoke", "reference", "gen_dev_data.R")
# pinned SHA-256 of the generator snapshot (smoke/README.md), recomputed on LF-normalised text (the worktree uses CRLF)
gen_sha <- digest::digest(paste0(paste(readLines(gen, warn = FALSE), collapse = "\n"), "\n"), algo = "sha256", serialize = FALSE)
cat("generator sha256 (LF):", gen_sha, " pinned: 36b03c8c8bad0ca30e62fc896f81c8d630078f6567b9448aa493d053e2b1a8c6\n")
genv <- new.env(); sys.source(gen, envir = genv)
d <- genv$generate_dev_dataset(p, scen, rep)$inputs
y <- unname(d$Y[, "c100"])
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
t0 <- proc.time()[["elapsed"]]
fit <- if (mode == "on") v3_fit(d$X, y, d$method_seed, ls0 = TRUE) else v3_fit(d$X, y, d$method_seed)
wall <- proc.time()[["elapsed"]] - t0
saveRDS(list(fit = fit, scenario = scen, replicate = rep, p = p, dataset_id = d$dataset_id, method_seed = d$method_seed,
             mode = mode, wall = wall, gen_sha = gen_sha, x_sha = digest::digest(d$X), y_sha = digest::digest(y)),
        file.path(outdir, sprintf("%s_%s.rds", d$dataset_id, mode)))
cat(sprintf("%s mode=%s status=%s hpm={%s} wall=%.0fs\n", d$dataset_id, mode, fit$status, paste(fit$hpm, collapse = ","), wall))
