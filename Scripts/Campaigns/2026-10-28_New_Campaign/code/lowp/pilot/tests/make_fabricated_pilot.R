#!/usr/bin/env Rscript
# make_fabricated_pilot.R -- LOCAL TEST ONLY, SELF-CONTAINED (no external templates). Builds a complete, schema-shaped, FABRICATED pilot output tree
# under <root>: results/<PID>_{enum20,enum30,scale_t08,scale_t16,scale_t32,smc,bench}/..., logs/<PID>/... (timing, launch receipt, P0 report, truth-lock
# evidence, wave lock/unlock records, bit-identity report, scaling subset, sacct snapshots, jobids). Records are built from the documented interfaces
# (INTERFACES I2-I4); p20 and p30 envelopes differ in p, K, model count, pip and size_logmass lengths. All runtimes, memory and sacct values are
# FABRICATED and mean nothing; they exist to exercise summarize_pilot.R (see run_negative_tests.R).
#   Rscript make_fabricated_pilot.R <root> [bench_lib]
a <- commandArgs(trailingOnly = TRUE); root <- a[1]; bench_lib <- if (length(a) > 1) a[2] else "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
stopifnot(!is.na(root))
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); dirname(normalizePath(f, winslash = "/")) })
lists <- file.path(here, "..", "lists")
sha <- function(f) digest::digest(file = f, algo = "sha256")
PID <- "20261029T0900Z_lowp_pilot"; res <- file.path(root, "results"); logs <- file.path(root, "logs", PID)
for (d in c("timing", "launch", "p0_verify", "truthlock/evidence", "bitid", "scaling", "accounting")) dir.create(file.path(logs, d), recursive = TRUE, showWarnings = FALSE)
set.seed(7)
enum20 <- trimws(readLines(file.path(lists, "enum20.txt"))); enum30 <- trimws(readLines(file.path(lists, "enum30.txt")))
smc <- read.delim(file.path(lists, "smc_cases.tsv"), stringsAsFactors = FALSE); bench <- read.delim(file.path(lists, "bench_cases.tsv"), stringsAsFactors = FALSE)
METHODS <- c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")
pnum <- function(ds) as.integer(substr(sub("^dev_", "", ds), 2, 5)); pdir <- function(ds) sprintf("p%04d", pnum(ds))
# job ids and array indices
jobs <- data.frame(step = c("s0_build", "s0_verify", "s0_truthlock", "s0_lock", "s1_enum20", "s1_enum30", "s1_scale", "s1_bitid", "s2_smc", "s3_bench", "s8_unlock", "s9_collect"),
                   id = 5000 + 1:12, n = c(1, 1, 1, 1, 1, 6, 1, 1, 28, 24, 1, 1), stringsAsFactors = FALSE); jobs$array <- ifelse(jobs$n > 1, paste0("0-", jobs$n - 1), "-")
jid <- function(step) jobs$id[jobs$step == step]
rows <- list(); addt <- function(arm, unit, thr, wall, rss_mb, step, task = 0, rc = 0, cpu = NULL)
  rows[[length(rows) + 1]] <<- data.frame(arm = arm, unit = unit, threads = thr, rc = rc, wall_s = wall, user_s = if (is.null(cpu)) wall * thr * 0.9 else cpu, sys_s = 0.1,
                                          maxrss_kb = round(rss_mb * 1024), host = "node1", jobid = jid(step), taskid = task, start_utc = "2026-10-29T10:00:00Z", stringsAsFactors = FALSE)
batch <- list()   # (jobid_task or jobid) -> MaxRSS MB
setb <- function(step, task, mb) { k <- if (jobs$n[jobs$step == step] > 1) paste0(jid(step), "_", task) else as.character(jid(step)); batch[[k]] <<- max(batch[[k]], mb, na.rm = TRUE) }
wunit <- function(dir, base, rds_obj, csv = NULL, kind) {
  dir.create(dir, recursive = TRUE, showWarnings = FALSE); f <- file.path(dir, paste0(base, ".rds")); saveRDS(rds_obj, f, compress = FALSE); h <- sha(f)
  if (kind == "enum") { writeLines(paste0(h, "  ", base, ".rds"), file.path(dir, paste0(base, ".sha256"))); writeLines(c(h, "2026-10-29T10:00:00Z"), file.path(dir, paste0(base, ".done"))) }
  else { utils::write.csv(csv, file.path(dir, paste0(base, ".csv")), row.names = FALSE)
         writeLines(c(paste0(h, "  ", base, ".rds"), paste0(sha(file.path(dir, paste0(base, ".csv"))), "  ", base, ".csv")), file.path(dir, paste0(base, ".sha256")))
         writeLines(c(paste("status", paste(csv$status, collapse = ",")), "finished_utc 2026-10-29T10:00:00Z"), file.path(dir, paste0(base, ".done"))) }
}
## ---- enumeration records (p-specific envelopes) ----
hex <- function(tag) digest::digest(tag, algo = "sha256", serialize = FALSE)
KIND <- "heuristic (not a validated interval bound)"
# a record that satisfies the FULL current I2 contract (enum/exact_contract.R::lowp_validate_exact): top-level coverage fields, sealed-input binding,
# retained-column map, normalised size masses (size_logjoint = size_logmass + log Z), 1,000-row top list, named PIPs, mpm = {pip > 1/2}, full exact scope
exact_rec <- function(id, thr, rt, seedtag = id, empty_hpm = FALSE) {
  p <- pnum(id); set.seed(sum(utf8ToInt(seedtag))); ret <- seq_len(p); K <- min(p, 100L); nexp <- sum(choose(p, 0:K))
  # coherent exact posterior: see S() below (one realizable support distribution, everything derived from it)
  S <- function() {
    # ONE realizable support distribution. Listed part: 1,000 distinct models with strictly decreasing scores (the best is the HPM; the empty model in the
    # empty-support control). Unlisted remainder with EXPLICIT support: the empty model if it is not listed, up to five leftover small models, and one model
    # of each size 4..K, all scoring below the listed minimum. Everything stored (log Z, size masses, PIPs, mpm) is DERIVED from this one distribution, so
    # sum(PIP) = sum_k k P(|S| = k) holds, PIP_j lies between the listed share and the listed share plus the unlisted mass, and log Z >= lse(listed scores).
    first <- if (empty_hpm) integer(0) else c(3L, 7L)
    pool <- c(list(integer(0)), as.list(ret), combn(ret, 2, simplify = FALSE), combn(ret, 3, simplify = FALSE))
    pool <- pool[!vapply(pool, function(s) identical(s, first), NA)]
    pick <- sample.int(length(pool), length(pool)); listed <- c(list(first), pool[pick[1:999]]); left <- pool[pick[-(1:999)]]
    big <- lapply(4:K, function(k) ret[seq_len(k)])
    left <- left[order(lengths(left))]     # the empty model, if it is not listed, comes first among the unlisted remainder (size 0 then has mass)
    rem <- c(left[seq_len(min(5L, length(left)))], big)
    Fl <- -90 - (0:999) * 0.5; Fr <- min(Fl) - 1 - 0.1 * seq_along(rem)
    allm <- c(listed, rem); Fa <- c(Fl, Fr); sz <- lengths(allm)
    lse1 <- function(v) max(v) + log(sum(exp(v - max(v))))
    lz <- lse1(Fa); sj <- vapply(0:K, function(k) { f <- Fa[sz == k]; if (length(f)) lse1(f) else -Inf }, 0); sm <- sj - lz
    w <- exp(Fa - lz); pip <- setNames(vapply(ret, function(j) sum(w[vapply(allm, function(m) j %in% m, NA)]), 0), as.character(ret)); hf <- Fl[1]
    list(status = "exact", scope = "full", log_Z = lz, log_m0 = -120, log_Z_rel_m0 = lz + 120, pip = pip, hpm = first, hpm_F = hf, hpm_size = length(first), hpm_eta = 1e-6, hpm_eta_kind = KIND,
         second_F = Fl[2], margin = Fl[1] - Fl[2], certificate_bound = 0.5, certificate_bound_kind = KIND, global_certified = TRUE, certified_over_scored_models = TRUE,
         mpm = as.integer(ret[pip > 0.5]), size_logmass = sm, size_logjoint = sj,
         top = data.frame(rank = 1:1000, F = Fl, size = lengths(listed), model = vapply(listed, function(m) paste(m, collapse = ";"), ""), mask = vapply(listed, function(m) sum(2^(m - 1)), 0), stringsAsFactors = FALSE),
         numerics = list(n_rescale = 10, n_fallback_v3 = 0, max_abs_dF_recheck = 0, recheck_count = 1e6, q_recomputed = 0, recheck_mismatch_F = 0, recheck_mismatch_eta = 0)) }
  list(schema = "lowp_exact_v1", dataset_id = id, p = p, n = 200L, K = K, source_sha256 = hex("src"), v3_score_sha256 = hex("v3score"), runtime_s = rt, host = "node1",
       started_utc = "2026-10-29T10:00:00Z", finished_utc = "2026-10-29T10:01:00Z", models_scored = nexp, models_expected = nexp, complete = TRUE, threads = thr,
       extra = list(input_mode = "sealed", manifest_checked = TRUE, manifest_sha256 = hex("manifest"), input_file_sha256 = hex(id), status = "exact", complete = TRUE, models_expected = nexp, retained_columns = ret),
       scales = list(c100 = S(), c050 = S()))
}
for (i in seq_along(enum20)) { id <- enum20[i]; rt <- runif(1, 0.3, 0.6); wunit(file.path(res, paste0(PID, "_enum20"), pdir(id), id), "EXACT", exact_rec(id, 4L, rt, empty_hpm = (i == 7L)), kind = "enum")
  addt("enum20", id, 4, rt + 9, 200 + runif(1, 0, 20), "s1_enum20", 0); setb("s1_enum20", 0, 260) }
for (i in seq_along(enum30)) { id <- enum30[i]; rt <- runif(1, 60, 90); wunit(file.path(res, paste0(PID, "_enum30"), pdir(id), id), "EXACT", exact_rec(id, 16L, rt), kind = "enum")
  addt("enum30", id, 16, rt + 10, 300, "s1_enum30", i - 1); setb("s1_enum30", i - 1, 330) }
for (thr in c(8L, 16L, 32L)) { id <- "dev_p0030_S4_r001"; rt <- 1100 / thr / 0.9 * (1 + thr / 200); z <- exact_rec(id, thr, rt, seedtag = "S4scale")
  wunit(file.path(res, sprintf("%s_scale_t%02d", PID, thr), "p0030", id), "EXACT", z, kind = "enum"); addt("scale", paste0("full_t", thr), thr, rt + 10, 310, "s1_scale", 0) }
# the enum30 S4_r001 record must equal the scaling records (thread invariance): rebuild it with the same content
id <- "dev_p0030_S4_r001"; z <- exact_rec(id, 16L, 74, seedtag = "S4scale"); wunit(file.path(res, paste0(PID, "_enum30"), "p0030", id), "EXACT", z, kind = "enum")
setb("s1_scale", 0, 330)
for (nm in c("subset_t1_rep1", "subset_t8_rep1", "subset_t1_rep2", "subset_t8_rep2")) addt("scale", nm, ifelse(grepl("t1_", nm), 1, 8), 30, 120, "s1_scale", 0)
## ---- SMC ----
for (i in seq_len(nrow(smc))) {
  ds <- smc$dataset[i]; sc <- smc$scale[i]; rep <- smc$repeat.[i]; p <- pnum(ds); cid <- paste0(ds, "_", sc); base <- if (rep > 0) paste0("SMCBVS_rep", rep) else "SMCBVS"
  data_seed <- 2200000L + match(cid, unique(paste0(smc$dataset, "_", smc$scale)))
  rt <- if (p == 20) runif(1, 4, 8) else runif(1, 17, 26); esc <- cid %in% c("dev_p0030_S4_r001_c050") && rep == 0; if (esc) rt <- rt * 6
  csv <- data.frame(rule_id = c("hpm", "pip05"), role = c("primary", "S0"), status = "ok", case_id = cid, scale_key = sc, regime = "L", study = "newcampaign_lowp", p = p, dataset_id = ds,
                    data_seed = data_seed, method_seed = data_seed + 4000000 + 1000 * rep, runtime_s = rt, v3_status = "completed", stringsAsFactors = FALSE)   # CONF-2b: the shipped adapter always writes v3_status (read by tools/p5_scan.R, which refuses a unit without it); the record also carries native_status = fit$status, as the adapter writes it (Sol review 2, R2-3: the scan no longer falls back to fit$status)
  z <- list(rows = csv, runtime_s = rt, estimates_available = TRUE, native_status = "completed", fit = list(status = "completed", branch_run = "smc", log_Z = -100 + 0.02 * rep + rnorm(1, 0, 0.01), hpm = if (i == 3L && rep == 0L) integer(0) else c(3L, 7L), peak_memory_kb = ifelse(p == 20, 190000, 260000),
            calibration = list(tier_final = as.numeric(esc), escalated = esc), runtime_guard = list(exceeded = FALSE)), case = list(method_seed = csv$method_seed[1]))
  wunit(file.path(res, paste0(PID, "_smc"), pdir(ds), cid), base, z, csv, "smc")
  addt("smc", paste0(cid, if (rep > 0) paste0("_rep", rep) else ""), 1, rt + 11, ifelse(p == 20, 115, 190), "s2_smc", i - 1); setb("s2_smc", i - 1, ifelse(p == 20, 220, 300))
}
## ---- benchmarks ----
mt <- c(F1 = 0.8, F2 = 0.5, F3 = 0.5, F4 = 0.1, F5 = 0.14, A1 = 1, A2 = 0.03, A3 = 36); mr <- c(F1 = 245, F2 = 272, F3 = 245, F4 = 77, F5 = 226, A1 = 266, A2 = 77, A3 = 175)
for (i in seq_len(nrow(bench))) for (m in METHODS) {
  ds <- bench$dataset[i]; sc <- bench$scale[i]; p <- pnum(ds); cid <- paste0(ds, "_", sc); rt <- mt[[m]] * runif(1, 0.8, 1.3) * (1 + (p == 30) * 0.5); ds_seed <- 2300001L + i
  csv <- data.frame(rule_id = c("primary_rule", "s0_rule"), role = c("primary", "S0"), status = "ok", method_id = m, case_id = cid, scale_key = sc, data_seed = ds_seed, method_seed = ds_seed + 4000000,
                    test_library = FALSE, runtime_s = rt, package = "glmnet", package_version = "5.1", adaptation_ids = "LA-1", stringsAsFactors = FALSE)
  z <- list(rows = csv, environment = list(test_library = FALSE, sealed_library = bench_lib, sessionInfo = c("R version 4.5.2 (2025-10-31)", "Platform: x86_64-pc-linux-gnu"),
            package_provenance = list(glmnet = list(path = file.path(bench_lib, "glmnet"), version = "5.1", built = "4.5.2"), digest = list(path = file.path(bench_lib, "digest"), version = "0.6.39", built = "4.5.2"),
            stats = list(path = "/usr/lib/R/library/stats", version = "4.5.2", built = "4.5.2")))) 
  wunit(file.path(res, paste0(PID, "_bench"), pdir(ds), cid), m, z, csv, "bench"); addt("bench", paste0(cid, "_", m), 1, rt + 8, mr[[m]] * 1.1, "s3_bench", i - 1); setb("s3_bench", i - 1, 400)
}
# step timings
addt("build", "compile", 1, 70, 900, "s0_build"); addt("verify", "nots_regen", 1, 6, 150, "s0_verify"); addt("truthlock", "test", 1, 25, 150, "s0_truthlock"); addt("lock", "apply", 1, 5, 120, "s0_lock")
addt("unlock", "apply", 1, 8, 120, "s8_unlock"); addt("bitid", "all", 16, 120, 400, "s1_bitid")
T <- do.call(rbind, rows); utils::write.table(T, file.path(logs, "timing", "all.fab_0.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
## ---- jobids, sacct ----
write.table(data.frame(step = jobs$step, jobid = jobs$id, array = jobs$array, dependency = "-"), file.path(logs, "jobids.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
sac <- do.call(rbind, lapply(seq_len(nrow(jobs)), function(k) {
  keys <- if (jobs$n[k] > 1) paste0(jobs$id[k], "_", 0:(jobs$n[k] - 1)) else as.character(jobs$id[k])
  rbind(data.frame(JobID = keys, JobName = jobs$step[k], State = "COMPLETED", ExitCode = "0:0", MaxRSS = "", stringsAsFactors = FALSE),
        data.frame(JobID = paste0(keys, ".batch"), JobName = "batch", State = "COMPLETED", ExitCode = "0:0", MaxRSS = sprintf("%gM", vapply(keys, function(k) if (is.null(batch[[k]])) 100 else batch[[k]], 0)), stringsAsFactors = FALSE))
}))
`%||%` <- function(x, y) if (is.null(x)) y else x
sac$MaxRSS[!grepl("\\.batch$", sac$JobID)] <- ""
write.table(sac, file.path(logs, "accounting", "sacct_final.tsv"), sep = "|", quote = FALSE, row.names = FALSE)
write.table(sac[!grepl(paste0("^", jid("s9_collect")), sac$JobID), ], file.path(logs, "accounting", "sacct_collector.tsv"), sep = "|", quote = FALSE, row.names = FALSE)
writeLines(c("# disk footprint (fabricated)", "52000\tfake"), file.path(logs, "accounting", "disk_after.txt"))
## ---- launch receipt ----
envf <- file.path(logs, "launch", "pilot.env"); writeLines(c('MODULES="GCC/13.2.0 R/4.4.1"', 'MODULES_BENCH="GCC/13.2.0 R/4.5.2"'), envf); writeLines(paste0(sha(envf), "  pilot.env"), file.path(logs, "launch", "pilot.env.sha256"))
writeLines(c("# effective environment (fabricated)", "STAMP=20261029T0900Z", "MODULES=[GCC/13.2.0 R/4.4.1]", "MODULES_BENCH=[GCC/13.2.0 R/4.5.2]", "PILOT_DRYRUN=[]", "PILOT_SKIP_MODULES=[]", "PILOT_LIMIT=[]",
             "PILOT_BENCH_METHODS=[]", "PILOT_BENCH_EXTRA=[]", "PILOT_TIME_BIN=[]", "PILOT_LOCAL_TEST=[]"), file.path(logs, "launch", "effective_env.txt"))
writeLines(c("# guard receipt (fabricated)", "guard_limits campaign_kb=524288 home_kb=10066329", "GUARD_CHECK_OK campaign_limit_kb=524288 home_limit_kb=10066329 planned_mb=30"), file.path(logs, "launch", "guard_receipt_submit.txt"))
writeLines(sprintf("%s\tsbatch fabricated", jobs$step), file.path(logs, "launch", "sbatch_args.tsv")); writeLines("fab  ./x", file.path(logs, "launch", "STAGED_SHA256.txt"))
## ---- reports ----
writeLines(c("# LOWP check 4(b)", "", "**PASS** (exit status 0). Compared 1200 production and 60 dev datasets (11340 float64 SHA-256 hashes: X, five Y columns, foldid, signal, eps) with the manifests; 0 mismatches; 6 of 6 pilot copies compared (identical() and file SHA-256)."), file.path(logs, "p0_verify", "NOTS_REGEN_REPORT.md"))
ev <- file.path(logs, "truthlock", "evidence")
writeLines(c("# truth-lock test (FABRICATED)", "ok    file counts", "ok    lock", "SOURCE_SHA256 x", "CHECKS 40 FAILED 0", "FINAL_EXIT_STATUS 0"), file.path(ev, "run.log"))
writeLines(c("script_sha256 x", "checks 40", "failed 0", "final_exit_status 0"), file.path(ev, "final_status.txt"))
writeLines("# after: truth 755 dev/truth 755; dirs not 755: 0; files not 444: 0", file.path(logs, "truthlock", "TRUTHLOCK_AFTER.txt"))
writeLines(c("# wave lock", "LOCK_STATE truth_mode=0 devtruth_mode=0 ls_denied=2 files_visible=0", "WAVE_LOCK_VERIFIED LOCK_STATE truth_mode=0 devtruth_mode=0 ls_denied=2 files_visible=0"), file.path(logs, "truthlock", "WAVE_LOCK.txt"))
writeLines(c("# wave unlock", "OPEN_STATE n_truth=1200 n_devtruth=60 dirs_not_755=0 files_not_444=0", "SHA256_AGAINST_PRELOCK equal", "WAVE_UNLOCK_VERIFIED OPEN_STATE n_truth=1200 n_devtruth=60 dirs_not_755=0 files_not_444=0 sha=equal"), file.path(logs, "truthlock", "WAVE_UNLOCK.txt"))
bc <- data.frame(check = c("T1 scores", "T1 decisions", "T1 aggregates", "T2 all models", "T3 random models", "T4 recheck", "T5 thread invariance"), case = "x", n = 10, byte_mismatches = 0, nonfinite = 0, max_abs_diff = 0, pass = TRUE, note = "", stringsAsFactors = FALSE)
utils::write.csv(bc, file.path(logs, "bitid", "bitid_results.csv"), row.names = FALSE); writeLines(c("# Pilot score and aggregate checks (FABRICATED)", "", "**VERDICT: PASS** (7 of 7 rows pass)."), file.path(logs, "bitid", "BITID_REPORT.md"))
ss <- data.frame(dataset = "dev_p0030_S4_r001", threads = c(1, 1, 8, 8), rep = c(1, 2, 1, 2), fraction = 0.03, n_tasks = 1024, tasks_run = 31, models_scored = 32505856, wall_s = c(33, 31, 5.2, 5.0),
                 wall_r_s = c(33, 31, 5.2, 5.0), sum_task_s = c(33, 31, 40, 41), models_total = 2^30, tasks_sha256 = digest::digest("task-subset-seed-1", algo = "sha256", serialize = FALSE), host = "node1")
utils::write.csv(ss, file.path(logs, "scaling", "scaling_subset.csv"), row.names = FALSE)
cat("fabricated pilot under", root, "\n")
