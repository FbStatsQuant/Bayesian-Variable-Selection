# Adversarial tests of the LOWP verifiers (Sol review REVIEW_b_spec_generator_sol.md, findings 1-5, 7, 8).
#   Rscript test_adversarial.R <sealed STUDY root> <original gen_dev_data.R or "none"> [scratch dir]
# Every probe must be REJECTED (or, for controls, accepted) as stated; writes ADVERSARIAL_TESTS.md next to this file and exits 1 on any failure.
# Part A: function-level probes of the local verifier, the manifest validator, the sigma gate, the seed check and the truth-lock algorithm
#         (on a modelled POSIX tree; the real chmod test is test_truth_lock_linux.sh).
# Part B: command-line probes of lowp_verify_nots.R: exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE or malformed.

a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) >= 1L)
study <- normalizePath(a[[1L]], winslash = "/", mustWork = TRUE)
here <- local({ f <- grep("^--file=", commandArgs(FALSE), value = TRUE); dirname(normalizePath(sub("^--file=", "", f[1L]), winslash = "/")) })
rdir <- normalizePath(file.path(here, "..", "R"), winslash = "/")
scratch <- if (length(a) >= 3L) a[[3L]] else file.path(tempdir(), "adv"); dir.create(scratch, recursive = TRUE, showWarnings = FALSE)
source(file.path(rdir, "lowp_generate.R")); source(file.path(rdir, "lowp_seal.R")); source(file.path(rdir, "lowp_verify.R")); source(file.path(rdir, "lowp_verify_nots.R"))
stopifnot(requireNamespace("digest", quietly = TRUE))

res <- data.frame(id = character(), probe = character(), expected = character(), observed = character(), ok = logical(), stringsAsFactors = FALSE)
rec <- function(id, probe, expected, observed, ok) { res[nrow(res) + 1L, ] <<- list(id, probe, expected, observed, isTRUE(ok)); cat(sprintf("%-5s %-4s %s\n", id, if (isTRUE(ok)) "ok" else "FAIL", probe)) }
rd <- function(f) utils::read.csv(f, stringsAsFactors = FALSE, colClasses = "character")

## ---------------------------------------------------------------- Part A
dev_b <- file.path(study, "dev"); id <- "dev_p0020_S2_r003"; p <- 20L; s <- 2L; r <- 3L
inp0 <- readRDS(file.path(dev_b, "inputs", "p0020", paste0(id, ".rds"))); tr0 <- readRDS(file.path(dev_b, "truth", "p0020", paste0(id, ".rds")))
mi_d <- rd(file.path(dev_b, "manifests", "inputs_manifest_lowp.csv")); mt_d <- rd(file.path(dev_b, "manifests", "truth_manifest_lowp.csv"))
mrow0 <- mi_d[mi_d$dataset_id == id, ]; trow0 <- mt_d[mt_d$dataset_id == id, ]
np <- function(r_) sum(lengths(r_$problems))
r0 <- lowp_check_dataset(inp0, tr0, mrow0, trow0, p, s, r, "dev")
rec("A0", "control: untouched sealed dev dataset passes every per-dataset gate", "0 problems", sprintf("%d problems", np(r0)), np(r0) == 0L)

i1 <- c(inp0, list(active = tr0$active, beta = tr0$beta))
r1 <- lowp_check_dataset(i1, tr0, mrow0, trow0, p, s, r, "dev")
rec("A1", "input object carries truth fields active/beta", "schema problem naming them", paste(r1$problems$schema, collapse = "; "), length(r1$problems$schema) > 0L && grepl("active", r1$problems$schema[1L]))
i1b <- c(inp0, list(signal = tr0$signal, eps = tr0$eps)); r1b <- lowp_check_dataset(i1b, tr0, mrow0, trow0, p, s, r, "dev")
rec("A1b", "input object carries truth fields signal/eps", "schema problem", paste(r1b$problems$schema, collapse = "; "), length(r1b$problems$schema) > 0L)

for (fld in c("n", "kind", "scales")) { im <- inp0; im[[fld]] <- NULL; rm_ <- lowp_check_dataset(im, tr0, mrow0, trow0, p, s, r, "dev")
  rec(paste0("A1m_", fld), sprintf("required I1 field `%s` deleted from the input object (all else valid)", fld), "schema problem naming it", paste(rm_$problems$schema, collapse = "; "),
      length(rm_$problems$schema) == 1L && grepl(fld, rm_$problems$schema[1L], fixed = TRUE) && length(rm_$problems$meta) >= 1L) }
im <- inp0; im$n <- NULL; im$kind <- NULL; im$scales <- NULL; rm3 <- lowp_check_dataset(im, tr0, mrow0, trow0, p, s, r, "dev")
rec("A1m_all", "all three required fields n, kind, scales deleted together", "schema problem naming all three", paste(rm3$problems$schema, collapse = "; "),
    length(rm3$problems$schema) == 1L && all(vapply(c("n", "kind", "scales"), grepl, TRUE, x = rm3$problems$schema[1L], fixed = TRUE)))
i2 <- inp0; i2$p <- 999L; i2$n <- 1L; i2$kind <- "prod"; i2$scenario <- 3L; i2$replicate <- 4L; i2$scales <- inp0$scales * 2
r2 <- lowp_check_dataset(i2, tr0, mrow0, trow0, p, s, r, "dev")
rec("A2", "input metadata p=999, n=1, kind=prod, scenario=3, replicate=4, scales doubled (id and seeds untouched)", ">= 6 metadata problems", sprintf("%d metadata problems", length(r2$problems$meta)), length(r2$problems$meta) >= 6L)

tr3 <- tr0; tr3$signal <- tr0$signal + 1; i3 <- inp0
for (k in names(LOWP_SCALES)) i3$Y[, k] <- LOWP_SCALES[[k]] * tr3$signal + tr3$eps
m3 <- mrow0; t3 <- trow0
for (k in names(LOWP_SCALES)) m3[[paste0("y_", k, "_sha256")]] <- f64_sha256(i3$Y[, k]); t3$signal_sha256 <- f64_sha256(tr3$signal)
r3 <- lowp_check_dataset(i3, tr3, m3, t3, p, s, r, "dev")
rec("A3", "signal + 1 with Y rebuilt from it and Y/signal hashes updated (previous gates all pass)", "signal gate fails, response gate passes", sprintf("signal problems %d, response problems %d, hash problems %d", length(r3$problems$signal), length(r3$problems$resp), length(r3$problems$hash)),
    length(r3$problems$signal) == 1L && length(r3$problems$resp) == 0L && length(r3$problems$hash) == 0L)
tr3b <- tr0; tr3b$signal <- tr0$signal * (1 + 1e-9)
r3b <- lowp_check_dataset(inp0, tr3b, mrow0, trow0, p, s, r, "dev")
rec("A3b", "signal scaled by 1 + 1e-9 (tolerance is explicit, 1e-12 relative)", "signal gate fails", sprintf("signal problems %d", length(r3b$problems$signal)), length(r3b$problems$signal) == 1L)

tr3c <- c(tr0, list(active_extra = 1)); r3c <- lowp_check_dataset(inp0, tr3c, mrow0, trow0, p, s, r, "dev")
rec("A3c", "truth object with an extra field", "truth schema problem", paste(r3c$problems$truth, collapse = "; "), length(r3c$problems$truth) > 0L)

# manifests: exact grid, ids, paths
mi_p <- rd(file.path(study, "manifests", "inputs_manifest_lowp.csv")); mt_p <- rd(file.path(study, "manifests", "truth_manifest_lowp.csv"))
v0 <- lowp_validate_manifests(mi_p, mt_p, "prod"); v0d <- lowp_validate_manifests(mi_d, mt_d, "dev")
rec("A4c", "control: sealed prod and dev manifests validate against the exact grids", "no problems", sprintf("%d / %d", length(c(v0$structure, v0$seed)), length(c(v0d$structure, v0d$seed))), length(c(v0$structure, v0$seed, v0d$structure, v0d$seed)) == 0L)
swap_row <- function(mi, mt, from, to_p, to_s, to_r, kind) {   # replace one dataset by another id, consistent id/path/seeds
  i <- which(mi$dataset_id == from); j <- which(mt$dataset_id == from); nid <- lowp_dataset_id(to_p, to_s, to_r, kind); sd <- lowp_seeds(to_p, to_s, to_r, kind)
  mi$dataset_id[i] <- nid; mi$p[i] <- as.character(to_p); mi$scenario[i] <- as.character(to_s); mi$replicate[i] <- as.character(to_r)
  mi$data_seed[i] <- as.character(sd$data_seed); mi$fold_seed[i] <- as.character(sd$fold_seed); mi$method_seed[i] <- as.character(sd$method_seed)
  mi$file[i] <- sprintf("inputs/p%04d/%s.rds", to_p, nid); mt$dataset_id[j] <- nid; mt$file[j] <- sprintf("truth/p%04d/%s.rds", to_p, nid); list(mi = mi, mt = mt)
}
x <- swap_row(mi_d, mt_d, "dev_p0020_S2_r005", 20L, 2L, 100L, "dev"); v4 <- lowp_validate_manifests(x$mi, x$mt, "dev")
rec("A4", "dev p20/S2/r5 replaced by r100 (60 unique rows, consistent ids/seeds/paths)", "structure problem (grid)", paste(utils::head(v4$structure, 2), collapse = "; "), length(v4$structure) > 0L)
v5a <- lowp_validate_manifests(mi_p[-1L, ], mt_p, "prod"); rec("A5a", "production manifest missing a row", "structure problem", paste(utils::head(v5a$structure, 1), collapse = ""), length(v5a$structure) > 0L)
mi_dup <- mi_p; mi_dup[2L, ] <- mi_dup[1L, ]; v5b <- lowp_validate_manifests(mi_dup, mt_p, "prod"); rec("A5b", "duplicate dataset_id (1,200 rows)", "structure problem", paste(utils::head(v5b$structure, 1), collapse = ""), length(v5b$structure) > 0L)
x <- swap_row(mi_p, mt_p, "p0030_S6_r100", 30L, 6L, 101L, "prod"); v5c <- lowp_validate_manifests(x$mi, x$mt, "prod")
rec("A5c", "out-of-range replicate 101 (consistent id)", "structure problem", paste(utils::head(v5c$structure, 1), collapse = ""), length(v5c$structure) > 0L)
mi_e <- mi_p; mi_e$file[mi_e$dataset_id == "p0020_S1_r001"] <- "inputs/p0030/p0020_S1_r001.rds"; v6 <- lowp_validate_manifests(mi_e, mt_p, "prod")
rec("A6", "non-canonical relative path (right basename, wrong per-p directory)", "structure problem", paste(utils::head(v6$structure, 1), collapse = ""), length(v6$structure) > 0L)
mi_f <- mi_p; mi_f$fold_seed[5L] <- "999"; v6b <- lowp_validate_manifests(mi_f, mt_p, "prod")
rec("A6b", "fold_seed = 999 in one manifest row", "seed problem naming fold_seed", paste(utils::head(v6b$seed, 1), collapse = ""), length(v6b$seed) == 1L && grepl("fold_seed", v6b$seed))
mi_c <- mi_p; names(mi_c)[names(mi_c) == "fold_sha256"] <- "foldid_sha256"; v6c <- lowp_validate_manifests(mi_c, mt_p, "prod")
rec("A6c", "inputs manifest with the benchmark column name foldid_sha256 instead of I1 fold_sha256", "structure problem", paste(utils::head(v6c$structure, 1), collapse = ""), length(v6c$structure) > 0L)

# sigma gate, per block: S6 with blocks 1 and 4 exchanged has the right pooled mean but wrong blocks
Sw <- scenario_covariance(6L, 20L); ord <- c(16:20, 6:15, 1:5)    # block 4 placed first, block 1 last
Sw <- Sw[ord, ord]; Lw <- chol(Sw); Wm <- NULL; Bv <- numeric()
for (rep_ in 1:100) { RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(777000L + rep_); Xw <- scale(matrix(rnorm(200 * 20), 200) %*% Lw); bc <- lowp_block_corr(Xw); Wm <- rbind(Wm, bc$within); Bv <- c(Bv, bc$between) }
ev <- lowp_sigma_eval(Wm, Bv, 6L, 20L)
rec("A7", "S6 p20 with blocks 1 and 4 exchanged: pooled mean unchanged, blocks wrong", "block gate FAIL while pooled deviation < 0.02", sprintf("pass=%s, max block dev %.3f (block %d), pooled dev %.4f", ev$pass, ev$max_block_dev, ev$worst_block, ev$pooled_dev),
    !ev$pass && ev$max_block_dev > 0.2 && ev$pooled_dev < 0.02)
# control with the true S6
Wc <- NULL; Bc <- numeric(); Lc <- chol(scenario_covariance(6L, 20L))
for (rep_ in 1:100) { set.seed(778000L + rep_); bc <- lowp_block_corr(scale(matrix(rnorm(200 * 20), 200) %*% Lc)); Wc <- rbind(Wc, bc$within); Bc <- c(Bc, bc$between) }
evc <- lowp_sigma_eval(Wc, Bc, 6L, 20L); rec("A7c", "control: correct S6 p20 (100 fresh replicates)", "block gate PASS", sprintf("pass=%s, max block dev %.4f", evc$pass, evc$max_block_dev), evc$pass)

# seed check: colliding p20 base must be caught; broader families
fam_bad <- lowp_seed_families(p20 = list(data = 1410000L, dev = 2210000L, fold = 3210000L, devfold = 4210000L)); cb <- lowp_seed_collision_check(out = NULL, families = fam_bad)
rec("A8", "p20 data base set to master's p500 base 1,410,000", "collision reported", sprintf("pass=%s, %d collisions", cb$pass, length(cb$collisions)), !cb$pass && length(cb$collisions) > 0L)
fam_bad3 <- lowp_seed_families(p20 = list(data = 1210000L, dev = 1220000L, fold = 3210000L, devfold = 4210000L)); cb3 <- lowp_seed_collision_check(out = NULL, families = fam_bad3)
rec("A8b", "p20 dev data base 1,220,000 (shifted by one slot: overlaps the p20 production data set)", "collision reported", sprintf("pass=%s, %d collisions", cb3$pass, length(cb3$collisions)), !cb3$pass)
fam_ok <- lowp_seed_collision_check(out = NULL); rec("A8c", "control: actual families (80 sets, 3,160 pairs; includes dev method/repeat and held-out method/repeat families)", "PASS, 80 sets, 3160 pairs", sprintf("pass=%s, %d sets, %d pairs", fam_ok$pass, fam_ok$n_sets, fam_ok$n_pairs), fam_ok$pass && fam_ok$n_sets == 80L && fam_ok$n_pairs == 3160L)

# truth lock algorithm on a modelled POSIX tree (owner bits only; operations need search permission on every ancestor)
mk_fs <- function(paths_dirs, paths_files, fail_chmod = character()) {
  st <- new.env(); for (d in paths_dirs) assign(d, list(dir = TRUE, mode = strtoi("755", 8L)), st); for (f in paths_files) assign(f, list(dir = FALSE, mode = strtoi("444", 8L)), st)
  reach <- function(p) { par <- dirname(p); while (par != "." && par != "/" && par != dirname(par) && exists(par, st, inherits = FALSE)) { if (bitwAnd(get(par, st)$mode, strtoi("100", 8L)) == 0L) return(FALSE); par <- dirname(par) }; TRUE }
  list(env = st,
    chmod = function(path, mode) { if (path %in% fail_chmod || !exists(path, st, inherits = FALSE) || !reach(path)) return(FALSE); o <- get(path, st); o$mode <- strtoi(mode, 8L); assign(path, o, st); TRUE },
    ls = function(dir) { if (!exists(dir, st, inherits = FALSE) || !reach(dir)) return(NULL); o <- get(dir, st); if (bitwAnd(o$mode, strtoi("500", 8L)) != strtoi("500", 8L)) return(NULL)
      ks <- ls(st, all.names = TRUE); unique(basename(ks[dirname(ks) == dir])) },
    isdir = function(path) { if (!exists(path, st, inherits = FALSE) || !reach(path)) return(NA); get(path, st)$dir },
    mode = function(path) { if (!exists(path, st, inherits = FALSE) || !reach(path)) return(NA_integer_); get(path, st)$mode },
    can_read = function(path) { if (!exists(path, st, inherits = FALSE) || !reach(path)) return(FALSE); bitwAnd(get(path, st)$mode, strtoi("400", 8L)) != 0L })
}
dirs <- c("/s/truth", "/s/truth/p0020", "/s/truth/p0030", "/s/dev/truth", "/s/dev/truth/p0020"); files <- c("/s/truth/p0020/a.rds", "/s/truth/p0020/b.rds", "/s/truth/p0030/c.rds", "/s/dev/truth/p0020/d.rds")
fs <- mk_fs(dirs, files)
lk <- lowp_truth_lock("/s", TRUE, fs)
modes_locked <- vapply(c(dirs, files), function(z) get(z, fs$env)$mode, 0L)
rec("A9a", "modelled POSIX tree: lock gives mode 000 on every directory (both trees) and file; contents unreachable; one call", "all 9 modes 000, root unlistable", sprintf("modes: %s; ls(/s/truth) = %s", paste(sprintf("%o", modes_locked), collapse = ","), if (is.null(fs$ls("/s/truth"))) "NULL" else "listed"),
    all(modes_locked == 0L) && is.null(fs$ls("/s/truth")) && is.na(fs$mode("/s/truth/p0020/a.rds")))
ul <- lowp_truth_lock("/s", FALSE, fs)
modes_open <- vapply(c(dirs, files), function(z) get(z, fs$env)$mode, 0L)
rec("A9b", "modelled POSIX tree: ONE unlock call after a full lock restores dirs 755 and files 444 (root first, each directory before descending)", "dirs 755, files 444", sprintf("modes: %s", paste(sprintf("%o", modes_open), collapse = ",")),
    all(modes_open[seq_along(dirs)] == strtoi("755", 8L)) && all(modes_open[length(dirs) + seq_along(files)] == strtoi("444", 8L)))
fs2 <- mk_fs(dirs, files, fail_chmod = "/s/truth/p0030/c.rds"); e2 <- tryCatch({ lowp_truth_lock("/s", TRUE, fs2); "no error" }, error = function(e) conditionMessage(e))
rec("A9c", "a failing chmod on one file during locking is not ignored", "error naming the path", e2, grepl("c.rds", e2))
fs3 <- mk_fs(dirs, files); lowp_truth_lock("/s", TRUE, fs3); lowp_truth_lock("/s", TRUE, fs3); lowp_truth_lock("/s", FALSE, fs3); lowp_truth_lock("/s", FALSE, fs3)
rec("A9d", "idempotence: lock, lock, unlock, unlock", "final modes 755/444", sprintf("root %o, file %o", get("/s/truth", fs3$env)$mode, get("/s/truth/p0020/a.rds", fs3$env)$mode), get("/s/truth", fs3$env)$mode == strtoi("755", 8L) && get("/s/truth/p0020/a.rds", fs3$env)$mode == strtoi("444", 8L))
# partially locked tree (e.g. an interrupted lock) is repaired by one unlock
fs4 <- mk_fs(dirs, files); invisible(fs4$chmod("/s/truth/p0020/a.rds", "000")); invisible(fs4$chmod("/s/truth/p0020", "000")); invisible(fs4$chmod("/s/truth", "000"))
lowp_truth_lock("/s", FALSE, fs4); rec("A9e", "partially locked tree (truth, truth/p0020, one file at 000) repaired by one unlock call", "dirs 755, files 444", sprintf("root %o, p0020 %o, file %o", get("/s/truth", fs4$env)$mode, get("/s/truth/p0020", fs4$env)$mode, get("/s/truth/p0020/a.rds", fs4$env)$mode),
    get("/s/truth", fs4$env)$mode == strtoi("755", 8L) && get("/s/truth/p0020", fs4$env)$mode == strtoi("755", 8L) && get("/s/truth/p0020/a.rds", fs4$env)$mode == strtoi("444", 8L))

## ---------------------------------------------------------------- Part B: lowp_verify_nots.R command line
rs <- file.path(R.home("bin"), if (.Platform$OS.type == "windows") "Rscript.exe" else "Rscript")
nots <- file.path(rdir, "lowp_verify_nots.R")
fx <- file.path(scratch, "fx"); unlink(fx, recursive = TRUE, force = TRUE); dir.create(file.path(fx, "manifests"), recursive = TRUE); dir.create(file.path(fx, "dev", "manifests"), recursive = TRUE)
for (f in c("inputs_manifest_lowp.csv", "truth_manifest_lowp.csv")) { file.copy(file.path(study, "manifests", f), file.path(fx, "manifests", f)); file.copy(file.path(dev_b, "manifests", f), file.path(fx, "dev", "manifests", f)) }
Sys.chmod(list.files(fx, recursive = TRUE, full.names = TRUE), "0644")
mk_study <- function(dest, drop = character()) {   # only the six pilot cells (inputs + truth)
  unlink(dest, recursive = TRUE, force = TRUE)
  for (p in LOWP_PS) for (sr in LOWP_PILOT_CELLS) { sid <- lowp_dataset_id(p, sr[1L], sr[2L], "prod")
    for (t in c("inputs", "truth")) { dd <- file.path(dest, t, sprintf("p%04d", p)); dir.create(dd, recursive = TRUE, showWarnings = FALSE)
      if (!(sid %in% drop)) file.copy(file.path(study, t, sprintf("p%04d", p), paste0(sid, ".rds")), file.path(dd, paste0(sid, ".rds"))) } }
  Sys.chmod(list.files(dest, recursive = TRUE, full.names = TRUE), "0644"); dest }
sdy <- mk_study(file.path(scratch, "study6"))
run_nots <- function(tag, manifests = file.path(fx, "manifests"), study_ = sdy, dev = NULL, extra = character(), no_dev_default = FALSE) {
  out <- file.path(scratch, paste0("out_", tag)); unlink(out, recursive = TRUE, force = TRUE)
  args <- c("--vanilla", shQuote(nots), "--manifests", shQuote(manifests), "--out", shQuote(out))
  if (!is.null(study_)) args <- c(args, "--study", shQuote(study_)); if (!is.null(dev)) args <- c(args, "--dev-manifests", shQuote(dev)); args <- c(args, extra)
  st <- suppressWarnings(system2(rs, args, stdout = TRUE, stderr = TRUE)); code <- attr(st, "status"); if (is.null(code)) code <- 0L; as.integer(code) }
ex <- function(id, probe, want, code) rec(id, probe, sprintf("exit %d", want), sprintf("exit %d", code), code == want)
ex("B1", "control: full manifests (1,200 + 60), dev manifests, all six pilot copies", 0L, run_nots("b1"))
mk_manifests <- function(tag, edit) { d <- file.path(scratch, paste0("m_", tag)); unlink(d, recursive = TRUE, force = TRUE); dir.create(file.path(d, "manifests"), recursive = TRUE); dir.create(file.path(d, "dev", "manifests"), recursive = TRUE)
  for (f in c("inputs_manifest_lowp.csv", "truth_manifest_lowp.csv")) { file.copy(file.path(fx, "manifests", f), file.path(d, "manifests", f)); file.copy(file.path(fx, "dev", "manifests", f), file.path(d, "dev", "manifests", f)) }
  Sys.chmod(list.files(d, recursive = TRUE, full.names = TRUE), "0644"); edit(d); d }
wr <- function(d, kind, f, df) utils::write.csv(df, file.path(d, if (kind == "dev") file.path("dev", "manifests") else "manifests", f), row.names = FALSE)
d <- mk_manifests("empty", function(d) for (f in c("inputs_manifest_lowp.csv", "truth_manifest_lowp.csv")) file.create(file.path(d, "manifests", f)))
ex("B2", "empty (0-byte) production manifests", 3L, run_nots("b2", file.path(d, "manifests")))
d <- mk_manifests("hdr", function(d) { wr(d, "prod", "inputs_manifest_lowp.csv", mi_p[0, ]); wr(d, "prod", "truth_manifest_lowp.csv", mt_p[0, ]) })
ex("B3", "header-only production manifests", 3L, run_nots("b3", file.path(d, "manifests")))
d <- mk_manifests("one", function(d) { wr(d, "prod", "inputs_manifest_lowp.csv", mi_p[1L, ]); wr(d, "prod", "truth_manifest_lowp.csv", mt_p[1L, ]) })
ex("B4", "one correct production row only", 3L, run_nots("b4", file.path(d, "manifests")))
ex("B5", "--study points to a nonexistent directory", 3L, run_nots("b5", study_ = file.path(scratch, "no_such_study")))
ex("B6", "--study omitted", 3L, run_nots("b6", study_ = NULL))
d <- mk_manifests("fold", function(d) { m <- mi_p; m$fold_seed[10L] <- "999"; wr(d, "prod", "inputs_manifest_lowp.csv", m) })
ex("B7", "one production row with fold_seed = 999", 1L, run_nots("b7", file.path(d, "manifests")))
d <- mk_manifests("xhash", function(d) { m <- mi_p; m$x_sha256[1L] <- sub("^.", "7", m$x_sha256[1L]); if (m$x_sha256[1L] == mi_p$x_sha256[1L]) m$x_sha256[1L] <- sub("^.", "6", m$x_sha256[1L]); wr(d, "prod", "inputs_manifest_lowp.csv", m) })
ex("B8", "one wrong X hash in the production manifest", 1L, run_nots("b8", file.path(d, "manifests")))
d <- mk_manifests("nodev", function(d) unlink(file.path(d, "dev"), recursive = TRUE))
ex("B9", "dev manifests omitted (no dev/manifests next to the production manifests)", 3L, run_nots("b9", file.path(d, "manifests")))
s5 <- mk_study(file.path(scratch, "study5"), drop = "p0030_S6_r100")
ex("B10", "only five of the six pilot copies present", 3L, run_nots("b10", study_ = s5))
s6 <- mk_study(file.path(scratch, "study6bad")); fcor <- file.path(s6, "inputs", "p0020", "p0020_S4_r050.rds"); o <- readRDS(fcor); o$X[1, 1] <- o$X[1, 1] + 1e-9; saveRDS(o, fcor, version = 3, compress = FALSE)
ex("B11", "a pilot copy whose X differs by 1e-9 in one entry", 1L, run_nots("b11", study_ = s6))
d <- mk_manifests("dupid", function(d) { m <- mi_p; m[2L, ] <- m[1L, ]; wr(d, "prod", "inputs_manifest_lowp.csv", m) })
ex("B12", "duplicated dataset_id (still 1,200 rows)", 3L, run_nots("b12", file.path(d, "manifests")))
d <- mk_manifests("range", function(d) { x <- swap_row(mi_p, mt_p, "p0030_S6_r100", 30L, 6L, 101L, "prod"); wr(d, "prod", "inputs_manifest_lowp.csv", x$mi); wr(d, "prod", "truth_manifest_lowp.csv", x$mt) })
ex("B13", "replicate 101 replacing p0030_S6_r100 (consistent id/seeds/paths)", 3L, run_nots("b13", file.path(d, "manifests")))
d <- mk_manifests("path", function(d) { m <- mi_p; m$file[3L] <- sub("p0020/", "p0030/", m$file[3L], fixed = TRUE); wr(d, "prod", "inputs_manifest_lowp.csv", m) })
ex("B14", "non-canonical relative path in one inputs row", 3L, run_nots("b14", file.path(d, "manifests")))
d <- mk_manifests("devshort", function(d) { wr(d, "dev", "inputs_manifest_lowp.csv", mi_d[-60L, ]); wr(d, "dev", "truth_manifest_lowp.csv", mt_d[-60L, ]) })
ex("B15", "dev manifests with 59 rows", 3L, run_nots("b15", file.path(d, "manifests")))
d <- mk_manifests("devfold", function(d) { m <- mi_d; m$fold_seed[7L] <- "4210001"; wr(d, "dev", "inputs_manifest_lowp.csv", m) })
ex("B16", "dev row with a wrong fold_seed", 1L, run_nots("b16", file.path(d, "manifests")))
d <- mk_manifests("cols", function(d) { m <- mi_p; names(m)[names(m) == "fold_sha256"] <- "foldid_sha256"; wr(d, "prod", "inputs_manifest_lowp.csv", m) })
ex("B17", "wrong inputs-manifest schema (foldid_sha256)", 3L, run_nots("b17", file.path(d, "manifests")))
ex("B18", "bad command line (no --out)", 3L, { st <- suppressWarnings(system2(rs, c("--vanilla", shQuote(nots), "--manifests", shQuote(file.path(fx, "manifests"))), stdout = TRUE, stderr = TRUE)); as.integer(attr(st, "status")) })

## ---------------------------------------------------------------- Part C: lowp_verify.R command line (original-source requirement)
vrs <- file.path(rdir, "lowp_verify.R"); rep_tmp <- file.path(scratch, "rep_nobench.md")
st <- suppressWarnings(system2(rs, c("--vanilla", shQuote(vrs), shQuote(study), "--report", shQuote(rep_tmp)), stdout = TRUE, stderr = TRUE)); code <- attr(st, "status"); if (is.null(code)) code <- 0L
rec("C1", "lowp_verify.R without --bench-gen (no original helper source)", "exit 3 (check 7 INCOMPLETE, no FAIL)", sprintf("exit %d", code), code == 3L && any(grepl("\\| 7 \\| INCOMPLETE", readLines(rep_tmp))))
if (length(a) >= 2L && a[[2L]] != "none") {
  st <- suppressWarnings(system2(rs, c("--vanilla", shQuote(vrs), shQuote(study), "--report", shQuote(rep_tmp), "--bench-gen", shQuote(file.path(scratch, "no_such_gen.R"))), stdout = TRUE, stderr = TRUE)); code <- attr(st, "status"); if (is.null(code)) code <- 0L
  rec("C2", "--bench-gen pointing to a nonexistent file", "exit 3 (INCOMPLETE)", sprintf("exit %d", code), code == 3L)
}

## ---------------------------------------------------------------- report
ok_all <- all(res$ok)
L <- c("# Adversarial tests of the LOWP verifiers", "",
       sprintf("Run %s UTC by `tests/test_adversarial.R`; sealed study `%s`; %s. **%s: %d of %d probes behave as required.**", format(Sys.time(), "%Y-%m-%d %H:%M", tz = "UTC"), study, R.version.string,
               if (ok_all) "ALL PASS" else "FAILURES", sum(res$ok), nrow(res)), "",
       "Probes follow Sol's review (findings 1-5, 7, 8) and the NOTS verifier gate semantics (exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE or malformed). A9* run the truth-lock algorithm on a modelled POSIX tree; the real ordinary-user Linux test is `tests/test_truth_lock_linux.sh` (to be run in the NOTS pilot).", "",
       "| Id | Probe | Required | Observed | Result |", "|---|---|---|---|---|",
       sprintf("| %s | %s | %s | %s | %s |", res$id, res$probe, res$expected, gsub("\\|", "/", substr(res$observed, 1, 160)), ifelse(res$ok, "ok", "**FAIL**")))
writeLines(L, file.path(here, "ADVERSARIAL_TESTS.md"))
cat(sprintf("\n%s: %d of %d probes behave as required\n", if (ok_all) "ALL PASS" else "FAILURES", sum(res$ok), nrow(res)))
quit(status = if (ok_all) 0L else 1L)
