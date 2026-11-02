# Check 10: crash-safe completion protocol, manifest requirement and concurrent writers of run_enum_dataset.R
# (failure injection through LOWP_ENUM_FAIL_AT; obstructed rename; corrupted RDS; lock handling; two simultaneous jobs).
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
rs <- "C:/Program Files/R/R-4.4.1/bin/Rscript.exe"; script <- file.path(LOWP_ENUM_DIR, "run_enum_dataset.R")
root <- file.path(TMP, "fake_study10"); unlink(root, recursive = TRUE); dir.create(file.path(root, "inputs/p0020"), recursive = TRUE); dir.create(file.path(root, "manifests"))
X <- gen_design(20, "block", seed = 3); Yc <- gen_response(X, c(3, 7, 14, 16), c(1.4, -1, 1.8, -1.2), cs = c(c100 = 1, c075 = .75, c050 = .5, c035 = .35, c025 = .25))
f <- file.path(root, "inputs/p0020/p0020_S3_r007.rds"); saveRDS(list(X = X, Y = Yc, foldid = rep(1:10, 20), dataset_id = "p0020_S3_r007", p = 20L), f, compress = FALSE)
man <- file.path(root, "manifests/inputs_manifest_lowp.csv")
write.csv(data.frame(dataset_id = "p0020_S3_r007", file = "inputs/p0020/p0020_S3_r007.rds", file_sha256 = lowp_sha256(f)), man, row.names = FALSE)
man_ok <- readLines(man)
out <- file.path(TMP, "fake_out10"); unlink(out, recursive = TRUE)
ds <- "p0020_S3_r007"
run <- function(rid, extra = character(), env = NULL, study = root, dataset = ds) {
  if (!is.null(env)) { old <- Sys.getenv(names(env), unset = NA); do.call(Sys.setenv, as.list(env)) }
  r <- suppressWarnings(system2(rs, c(shQuote(script), "--dataset", dataset, "--study", shQuote(study), "--outroot", shQuote(out), "--run-id", rid, "--threads", "2", extra), stdout = TRUE, stderr = TRUE))
  if (!is.null(env)) for (k in names(env)) Sys.unsetenv(k)
  st <- attr(r, "status"); list(status = if (is.null(st)) 0L else st, out = r)
}
dest <- function(rid) file.path(out, "results", rid, "p0020", ds)
state <- function(rid) { d <- dest(rid); list(done = file.exists(file.path(d, "EXACT.done")), rds = file.exists(file.path(d, "EXACT.rds")), sha = file.exists(file.path(d, "EXACT.sha256")),
  lock = dir.exists(file.path(d, ".lock")), tmp = length(list.files(d, pattern = "tmp", all.files = TRUE)) > 0) }
consistent <- function(rid) { d <- dest(rid); a <- tolower(substr(readLines(file.path(d, "EXACT.sha256"), 1), 1, 64)); b <- substr(readLines(file.path(d, "EXACT.done"), 1), 1, 64); h <- lowp_sha256(file.path(d, "EXACT.rds")); identical(a, h) && identical(b, h) }
res <- list(); chk <- function(name, ok, note = "") { res[[length(res) + 1]] <<- data.frame(test = name, pass = isTRUE(ok), note = note); cat(sprintf("%-4s %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", name, note)) }

r <- run("A"); chk("fresh run completes", r$status == 0 && state("A")$done && consistent("A") && !state("A")$lock && !state("A")$tmp)
rec <- readRDS(file.path(dest("A"), "EXACT.rds")); chk("record has input_mode sealed, status exact, labels, normalised size masses",
  identical(rec$extra$input_mode, "sealed") && rec$extra$manifest_checked && identical(rec$extra$status, "exact") && identical(rec$scales$c100$certificate_bound_kind, "heuristic (not a validated interval bound)") && abs(log(sum(exp(rec$scales$c100$size_logmass)))) < 1e-12)
r <- run("A"); chk("rerun verifies marker/sidecar/RDS and skips", r$status == 0 && any(grepl("verified", r$out)) && !any(grepl("^OK ", r$out)))
## corrupted RDS with a present marker
d <- dest("A"); con <- file(file.path(d, "EXACT.rds"), "ab"); writeBin(as.raw(1), con); close(con)
r <- run("A"); chk("corrupted RDS + stale .done: detected, recomputed, valid", r$status == 0 && any(grepl("not valid", r$out)) && any(grepl("^OK ", r$out)) && consistent("A"))
## sidecar edited
writeLines(paste0(strrep("0", 64), "  EXACT.rds"), file.path(d, "EXACT.sha256"))
r <- run("A"); chk("tampered sidecar + .done: detected, recomputed, valid", r$status == 0 && any(grepl("^OK ", r$out)) && consistent("A"))
## failure injection at each commit point on a valid result (forced rewrite)
for (pt in c("before_rds_rename", "after_rds_rename", "after_sha_rename", "before_done")) {
  r <- run("A", "--force", env = c(LOWP_ENUM_FAIL_AT = pt)); s <- state("A")
  chk(paste0("forced rewrite failing at ", pt, ": exit != 0, no .done, no lock, no temp files"), r$status != 0 && !s$done && !s$lock && !s$tmp, paste("status", r$status))
  r2 <- run("A"); chk(paste0("  recovery after ", pt, ": plain rerun recomputes and publishes a consistent result"), r2$status == 0 && any(grepl("^OK ", r2$out)) && consistent("A"))
}
## reviewer scenario: obstruction at the sidecar destination
d <- dest("A"); unlink(file.path(d, "EXACT.sha256")); dir.create(file.path(d, "EXACT.sha256"))
r <- run("A", "--force"); chk("obstructed sidecar rename: forced rewrite fails, no .done left", r$status != 0 && !file.exists(file.path(d, "EXACT.done")) && !dir.exists(file.path(d, ".lock")))
r <- run("A"); chk("  rerun with the obstruction still present does not report completion", r$status != 0 && !file.exists(file.path(d, "EXACT.done")))
unlink(file.path(d, "EXACT.sha256"), recursive = TRUE)
r <- run("A"); chk("  rerun after removing the obstruction recovers", r$status == 0 && consistent("A"))
## lock handling
d <- dest("A"); dir.create(file.path(d, ".lock")); before <- lowp_sha256(file.path(d, "EXACT.rds"))
r <- run("A", "--force"); chk("fresh lock held by another writer: forced job exits with status 3; the existing verified result is untouched", r$status == 3 && identical(lowp_sha256(file.path(d, "EXACT.rds")), before) && file.exists(file.path(d, "EXACT.done")) && consistent("A"), paste("status", r$status))
Sys.setFileTime(file.path(d, ".lock"), Sys.time() - 3600)
r <- run("A", "--force"); chk("stale lock (1 h old) is removed and the forced job completes", r$status == 0 && any(grepl("^OK ", r$out)) && consistent("A") && !dir.exists(file.path(d, ".lock")))
## two simultaneous jobs on one destination
unlink(file.path(out, "results", "C"), recursive = TRUE)
mk <- function(tag) system2(rs, c(shQuote(script), "--dataset", ds, "--study", shQuote(root), "--outroot", shQuote(out), "--run-id", "C", "--threads", "2"), stdout = file.path(TMP, paste0("conc_", tag, ".log")), stderr = file.path(TMP, paste0("conc_", tag, ".log")), wait = FALSE)
mk("1"); mk("2")
t0 <- Sys.time(); repeat { Sys.sleep(1); if (state("C")$done && !state("C")$lock && !any(grepl("Rscript", system("tasklist", intern = TRUE)) )) break; if (difftime(Sys.time(), t0, units = "secs") > 120) break }
Sys.sleep(2)
s <- state("C"); chk("two simultaneous jobs: one valid consistent result, no lock or temp files left", s$done && consistent("C") && !s$lock && !s$tmp)
cat("   concurrent job logs:", paste(substr(c(readLines(file.path(TMP, "conc_1.log")), readLines(file.path(TMP, "conc_2.log"))), 1, 70)[grepl("^OK|another|nothing|verified", c(readLines(file.path(TMP, "conc_1.log")), readLines(file.path(TMP, "conc_2.log"))))], collapse = " | "), "\n")
## manifest requirements
writeLines(man_ok[1], man)   # header only: no row
r <- run("M1"); chk("production run, manifest without the dataset row: refused, no output", r$status != 0 && !dir.exists(dest("M1")) , paste(tail(r$out, 1)))
writeLines(c(man_ok, man_ok[2]), man)
r <- run("M2"); chk("production run, duplicate manifest rows: refused, no output", r$status != 0 && !dir.exists(dest("M2")))
file.remove(man)
r <- run("M3"); chk("production run, manifest absent: refused, no output", r$status != 0 && !dir.exists(dest("M3")), paste(tail(r$out, 1)))
r <- run("M4", "--unsealed-test-input"); chk("explicit --unsealed-test-input without manifest: runs and records input_mode", r$status == 0 && identical(readRDS(file.path(dest("M4"), "EXACT.rds"))$extra$input_mode, "unsealed_test") && !readRDS(file.path(dest("M4"), "EXACT.rds"))$extra$manifest_checked)
writeLines(man_ok, man)
r <- run("M5"); chk("restored manifest: sealed run", r$status == 0 && identical(readRDS(file.path(dest("M5"), "EXACT.rds"))$extra$input_mode, "sealed"))
## ---- resume must validate the whole requested contract (N1) and the I2 envelope (N2) -------------------------------------
writeLines(man_ok, man)
r <- run("N"); d <- dest("N"); rec0 <- readRDS(file.path(d, "EXACT.rds"))
chk("N2: models_expected and complete are at the top level (and in extra)", r$status == 0 && identical(rec0$models_expected, 1048576) && isTRUE(rec0$complete) && identical(rec0$extra$models_expected, 1048576) && isTRUE(rec0$extra$complete))
rewrite <- function(rid, fun) {   # replace the record by fun(rec) with a self-consistent RDS, sidecar and marker (a "prior-version" fixture)
  d <- dest(rid); rec <- fun(readRDS(file.path(d, "EXACT.rds"))); f <- file.path(d, "EXACT.rds"); saveRDS(rec, f, compress = FALSE); h <- lowp_sha256(f)
  writeLines(paste0(h, "  EXACT.rds"), file.path(d, "EXACT.sha256")); writeLines(c(h, "fixture"), file.path(d, "EXACT.done")); invisible(h) }
recomputed <- function(r, why) r$status == 0 && any(grepl("^OK ", r$out)) && any(grepl(why, r$out, fixed = TRUE)) && consistent("N")
rewrite("N", function(x) { x$source_sha256 <- strrep("0", 64); x })
r <- run("N"); chk("N1: stale source fingerprint (self-consistent hashes) -> recomputed", recomputed(r, "different sources") && identical(readRDS(file.path(dest("N"), "EXACT.rds"))$source_sha256, rec0$source_sha256))
r <- run("N"); chk("  the recomputed record is accepted on the next run", r$status == 0 && any(grepl("verified", r$out)) && !any(grepl("^OK ", r$out)))
## different scales
r <- run("S1", "--scales c100"); recS <- readRDS(file.path(dest("S1"), "EXACT.rds"))
chk("record written with --scales c100 holds only c100", r$status == 0 && identical(names(recS$scales), "c100"))
r <- run("S1"); recS <- readRDS(file.path(dest("S1"), "EXACT.rds"))
chk("N1: two-scale request over a c100-only record -> recomputed, now c100 and c050", r$status == 0 && any(grepl("requested {c100,c050}", r$out, fixed = TRUE)) && identical(names(recS$scales), c("c100", "c050")))
r <- run("S1", "--scales c100")
chk("N1: c100-only request over a two-scale record -> recomputed (exact scale set)", r$status == 0 && any(grepl("^OK ", r$out)) && identical(names(readRDS(file.path(dest("S1"), "EXACT.rds"))$scales), "c100"))
## prior-version records
old_fields <- function(x) { x$models_expected <- NULL; x$complete <- NULL
  for (s in names(x$scales)) { z <- x$scales[[s]]; z$size_logmass <- z$size_logjoint; for (nm in c("size_logjoint", "certificate_bound_kind", "hpm_eta_kind", "status", "scope", "certified_over_scored_models")) z[[nm]] <- NULL; x$scales[[s]] <- z }
  x$extra$status <- NULL; x }
rewrite("N", function(x) { x <- old_fields(x); x$source_sha256 <- strrep("1", 64); x })
r <- run("N"); chk("N1: prior-version record (other source, joint size_logmass, no labels/new fields) -> recomputed", recomputed(r, "not valid") && !is.null(readRDS(file.path(dest("N"), "EXACT.rds"))$scales$c100$size_logjoint))
rewrite("N", old_fields)   # same source fingerprint, old fields only: the reviewer's fixture
r <- run("N"); chk("N1: same fingerprint but old-contract fields (no new fields) -> recomputed", recomputed(r, "missing"))
rewrite("N", function(x) { for (s in names(x$scales)) x$scales[[s]]$size_logmass <- x$scales[[s]]$size_logjoint; x })
r <- run("N"); chk("N1: all fields present but joint-valued size_logmass -> recomputed", recomputed(r, "normalised"))
rewrite("N", function(x) { x$models_scored <- x$models_scored - 1; x })
r <- run("N"); chk("N1: incomplete model coverage -> recomputed", recomputed(r, "models_scored"))
rewrite("N", function(x) { x$extra$status <- "partial"; x$complete <- FALSE; x })
r <- run("N"); chk("N1: status partial / complete FALSE -> recomputed", recomputed(r, "complete is not TRUE"))
rewrite("N", function(x) { x$scales$c050$scope <- "restricted_to_scored_models"; x })
r <- run("N"); chk("N1: a scale with scope restricted -> recomputed", recomputed(r, "scope is not full"))
R <- do.call(rbind, res); cat(sprintf("\n%d of %d checks passed\n", sum(R$pass), nrow(R)))
