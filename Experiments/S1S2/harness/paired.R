# paired.R -- paired comparison of SMC-BVS with each benchmark method on the same simulated data sets (never launches fits).
#   Rscript harness/paired.R --suite 1|2 [--methods lasso_cv,scad,susie,bas_mc3,asi] [--reps LO-HI] [--runs DIR]
#                            [--smcbvs DIR] [--out DIR] [--pairing joint|pairwise] [--missing empty|exclude]
# Inputs: <runs>/<method>/S<suite>_xx/rep_RRR.json; SMC-BVS from <smcbvs>/S<suite>_xx/rep_RRR.json (default <runs>/smcbvs).
# Only those paths are read (harness/records.R: never _superseded/ or audit folders; a json whose setting_id / rep /
# method differs from its path, or a duplicate record, stops the script). Defaults: all five benchmarks, reps 1-100,
# runs = S1S2_RUNS (Owls), out = specs/ (paired_* is gitignored).
# Outputs <out>/paired_S<suite>.md and _paired.tsv, _permethod.tsv, _md5.tsv (md5 mismatched / unverified records).
#
# Rules (the same as reports/S1S2/scripts/build_S1_comparison.R, so the numbers agree):
#   * TP / FP / FN / exact are recomputed from `selected` vs `support` and must agree with the record's own fields.
#     Exact = Ŝ == S0. Hamming = FP + FN. F1 per fit = 2TP / (2TP + FP + FN).
#   * Data identity: a benchmark record is paired with the SMC-BVS record of the same (setting, rep) only if both carry a
#     data_md5 and they are equal; mismatches (both present, different) and unverified records (finished benchmark record
#     or SMC-BVS reference without a data_md5) are counted and listed in _md5.tsv. A mismatched record is left out
#     everywhere (as if missing).
#   * Paired tables: SHARED reps only. --pairing joint (default): a rep is shared only if SMC-BVS and EVERY method in
#     --methods have a finished (status ok) record and every benchmark md5 matches (the build_S1_comparison rule);
#     pairwise: SMC-BVS and that one method. Failed records never enter the paired tables.
#     b = SMC-BVS exact and the method not, c = the method exact and SMC-BVS not; McNemar exact p = two-sided binomial
#     test of b vs b + c. Hamming wins / ties / losses from SMC-BVS's side (win = smaller FP + FN); sign-test p = the same
#     binomial test on wins vs wins + losses. — = no discordant pairs.
#   * Per-method tables (every method including SMC-BVS): --missing empty (default; as harness/aggregate.R): the
#     denominator is every expected (setting, rep) and a failed or missing (or md5-mismatched) record counts as Ŝ = ∅
#     (TP = FP = 0, FN = s0, F1 = 0, not exact). --missing exclude: missing reps are left out (failed still = ∅), as in
#     build_S1_comparison.R.
#   * Pooled rows sum over the settings of the group: S1 by (n, p) and by SNR; S2 by (n, ρ, beta-type, ν) (pooled over s);
#     plus "all".
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "methods.R")); source(file.path(BASE, "harness", "generate.R")); source(file.path(BASE, "harness", "records.R"))

opt <- list(suite = NA, methods = "lasso_cv,scad,susie,bas_mc3,asi", reps = "1-100", runs = S1S2_RUNS, smcbvs = NA,
            out = file.path(BASE, "specs"), pairing = "joint", missing = "empty")
a <- commandArgs(TRUE); i <- 1
while (i <= length(a)) {
  k <- a[i]
  if (grepl("=", k)) { key <- sub("=.*", "", k); val <- sub("^[^=]*=", "", k); i <- i + 1 } else { key <- k; val <- a[i + 1]; i <- i + 2 }
  key <- gsub("-", "_", sub("^--", "", key))
  if (!key %in% names(opt) || is.na(val)) stop("bad argument: ", k)
  opt[[key]] <- val
}
su <- as.integer(opt$suite); if (!su %in% 1:2) stop("--suite 1|2 is required")
if (!opt$pairing %in% c("joint", "pairwise")) stop("--pairing joint|pairwise")
if (!opt$missing %in% c("empty", "exclude")) stop("--missing empty|exclude")
rr <- regmatches(opt$reps, regexec("^([0-9]+)-([0-9]+)$", opt$reps))[[1]]
if (length(rr) != 3) stop("--reps LO-HI"); REPS <- seq(as.integer(rr[2]), as.integer(rr[3]))
BENCH <- strsplit(opt$methods, ",")[[1]]
if (!length(BENCH) || !all(BENCH %in% setdiff(names(S1S2_METHODS), "smcbvs"))) stop("--methods: benchmarks only, from ", paste(setdiff(names(S1S2_METHODS), "smcbvs"), collapse = ","))
M <- c("smcbvs", BENCH)
mdir <- function(m) if (m == "smcbvs") (if (is.na(opt$smcbvs)) file.path(opt$runs, "smcbvs") else opt$smcbvs) else file.path(opt$runs, m)
for (m in M) rec_guard_root(mdir(m))

st <- read_settings(file.path(BASE, "specs", "settings.tsv")); st <- st[st$suite == su, ]

## ---- records ---------------------------------------------------------------------------------------------------
nz <- function(x) if (is.null(x)) NA else x
read_one <- function(m, s, rp, s0) {
  f <- rec_file(mdir(m), s, rp)
  row <- data.frame(method = m, setting_id = s, rep = rp, state = "missing", status = NA_character_, md5 = NA_character_,
                    TP = NA_real_, FP = NA_real_, FN = NA_real_, exact = NA, stringsAsFactors = FALSE)
  if (!file.exists(f)) return(row)
  r <- rec_read(mdir(m), m, s, rp)
  row$status <- as.character(nz(r$status)); row$md5 <- as.character(nz(r$data_md5))
  if (identical(r$status, "ok")) { cf <- rec_confusion(r, f)
    row$TP <- cf[["TP"]]; row$FP <- cf[["FP"]]; row$FN <- cf[["FN"]]; row$exact <- cf[["FP"]] + cf[["FN"]] == 0; row$state <- "finished"
  } else { row$state <- "failed"; row$TP <- 0; row$FP <- 0; row$FN <- s0; row$exact <- FALSE }
  row
}
D <- do.call(rbind, lapply(seq_len(nrow(st)), function(j) do.call(rbind, lapply(REPS, function(rp)
  do.call(rbind, lapply(M, function(m) read_one(m, st$setting_id[j], rp, st$s0[j])))))))
D <- merge(D, st[, c("setting_id", "n", "p", "s0", "snr", "rho", "nu", "beta_type")], by = "setting_id", sort = FALSE)
D$key <- paste(D$setting_id, D$rep)
ref <- D[D$method == "smcbvs", ]; D$ref_md5 <- ref$md5[match(D$key, ref$key)]
D$md5_state <- ifelse(D$method == "smcbvs", "reference",
               ifelse(!is.na(D$md5) & !is.na(D$ref_md5), ifelse(D$md5 == D$ref_md5, "match", "mismatch"),
               ifelse(D$state == "finished", "unverified", "none")))
D <- D[order(D$setting_id, D$rep, match(D$method, M)), ]
for (m in BENCH) if (!any(D$method == m & D$state != "missing")) message(sprintf("NOTE: no %s records in S%d reps %s", m, su, opt$reps))

## ---- groups ------------------------------------------------------------------------------------------------------
grp <- function(scope, group, ids) list(scope = scope, group = group, ids = ids)
GROUPS <- c(lapply(st$setting_id, function(s) grp("setting", s, s)),
  if (su == 1) c(lapply(split(st$setting_id, paste(st$n, st$p))[unique(paste(st$n, st$p))], function(ids)
                   { r <- st[st$setting_id == ids[1], ]; grp("pooled_np", sprintf("n=%d, p=%d", r$n, r$p), ids) }),
                 lapply(sort(unique(st$snr)), function(v) grp("pooled_SNR", sprintf("SNR=%g", v), st$setting_id[st$snr == v])))
  else { k <- paste(st$n, st$rho, st$beta_type, st$nu); o <- order(st$n, st$rho, st$beta_type, st$nu)
         lapply(unique(k[o]), function(kk) { r <- st[k == kk, ][1, ]
           grp("pooled_n_rho_bt_nu", sprintf("n=%d, ρ=%g, type %s, ν=%g", r$n, r$rho, r$beta_type, r$nu), st$setting_id[k == kk]) }) },
  list(grp("all", sprintf("all S%d", su), st$setting_id)))

## ---- per-method ------------------------------------------------------------------------------------------------
pm <- function(d, n_exp) {   # d = the method's rows of the group (all expected reps)
  use <- d$state %in% c("finished", "failed") & d$md5_state != "mismatch"
  den <- if (opt$missing == "empty") n_exp else sum(use)
  x <- d[use, ]; mf <- sum(d$s0[!use])   # missing / mismatched: FN = s0 (empty mode)
  fn <- if (opt$missing == "empty") sum(x$FN) + mf else sum(x$FN)
  data.frame(n_expected = n_exp, n_ok = sum(d$state == "finished"), n_failed = sum(d$state == "failed"), n_missing = sum(d$state == "missing"),
             n_md5_mismatch = sum(d$md5_state == "mismatch"), n_counted = den, successes = sum(x$exact),
             success_rate = if (den) sum(x$exact) / den else NA, hamming_mean = if (den) (sum(x$FP) + fn) / den else NA,
             TP_mean = if (den) sum(x$TP) / den else NA, FP_mean = if (den) sum(x$FP) / den else NA, FN_mean = if (den) fn / den else NA,
             F1_mean = if (den) sum(rec_F1(x$TP, x$FP, x$FN)) / den else NA)
}
PM <- do.call(rbind, lapply(GROUPS, function(g) do.call(rbind, lapply(M, function(m) {
  d <- D[D$method == m & D$setting_id %in% g$ids, ]
  cbind(data.frame(scope = g$scope, group = g$group, method = m, stringsAsFactors = FALSE), pm(d, length(g$ids) * length(REPS))) }))))

## ---- paired ----------------------------------------------------------------------------------------------------------
fin <- D$state == "finished" & D$md5_state %in% c("reference", "match")
okkeys <- function(ms) Reduce(intersect, lapply(ms, function(m) D$key[D$method == m & fin]))
shared_joint <- okkeys(M)
bt <- function(k, n) if (n > 0) binom.test(k, n)$p.value else NA_real_
PR <- do.call(rbind, lapply(GROUPS, function(g) do.call(rbind, lapply(BENCH, function(m) {
  sh <- if (opt$pairing == "joint") shared_joint else okkeys(c("smcbvs", m))
  A <- D[D$method == "smcbvs" & D$setting_id %in% g$ids & D$key %in% sh, ]
  B <- D[D$method == m & D$setting_id %in% g$ids, ]; B <- B[match(A$key, B$key), ]
  dm <- D[D$method == m & D$setting_id %in% g$ids, ]
  n <- nrow(A); b <- sum(A$exact & !B$exact); cc <- sum(!A$exact & B$exact)
  ha <- A$FP + A$FN; hb <- B$FP + B$FN; w <- sum(ha < hb); l <- sum(ha > hb)
  data.frame(scope = g$scope, group = g$group, method = m, n_shared = n,
             md5_mismatch = sum(dm$md5_state == "mismatch"), md5_unverified = sum(dm$md5_state == "unverified"),
             smcbvs_exact = sum(A$exact), method_exact = sum(B$exact), b_smcbvs_only = b, c_method_only = cc, mcnemar_p = bt(b, b + cc),
             hamming_wins = w, hamming_ties = n - w - l, hamming_losses = l, sign_p = bt(w, w + l),
             mean_hamming_smcbvs = if (n) mean(ha) else NA, mean_hamming_method = if (n) mean(hb) else NA,
             mean_F1_smcbvs = if (n) mean(rec_F1(A$TP, A$FP, A$FN)) else NA, mean_F1_method = if (n) mean(rec_F1(B$TP, B$FP, B$FN)) else NA,
             stringsAsFactors = FALSE) }))))
MD5 <- D[D$md5_state %in% c("mismatch", "unverified") | (D$method == "smcbvs" & is.na(D$md5) & D$state == "finished"),
         c("method", "setting_id", "rep", "state", "md5_state", "md5", "ref_md5")]

## ---- write -----------------------------------------------------------------------------------------------------------
dir.create(opt$out, recursive = TRUE, showWarnings = FALSE)
stem <- file.path(opt$out, sprintf("paired_S%d", su))
wt <- function(x, f) write.table(x, f, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
wt(PR, paste0(stem, "_paired.tsv")); wt(PM, paste0(stem, "_permethod.tsv")); wt(MD5, paste0(stem, "_md5.tsv"))
f2 <- function(x, d = 2) ifelse(is.na(x), "—", formatC(x, format = "f", digits = d))
fp <- function(x) ifelse(is.na(x), "—", ifelse(x < 0.001, "<0.001", formatC(x, format = "f", digits = 3)))
mdt <- function(df) c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
                      apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |")))
show <- if (su == 1) function(x) TRUE else function(x) x$scope != "setting"     # S2: per-setting rows in the tsv only
L <- c(sprintf("# Paired comparison S%d: SMC-BVS vs %s (reps %s)", su, paste(BENCH, collapse = ", "), opt$reps), "",
  sprintf("Built %s by harness/paired.R. Records: `%s/<method>/`, SMC-BVS `%s`.", format(Sys.time(), "%Y-%m-%d %H:%M %Z"), normalizePath(opt$runs), normalizePath(mdir("smcbvs"))),
  sprintf("Pairing: **%s**%s. Shared reps (joint) over all settings: %d of %d.", opt$pairing,
          if (opt$pairing == "joint") " (a rep enters only if SMC-BVS and every listed method finished with matching data_md5)" else " (SMC-BVS and that method finished, data_md5 equal)",
          length(shared_joint), nrow(st) * length(REPS)),
  sprintf("data_md5: %d mismatched and %d unverified benchmark records (listed in `%s`); mismatched records are left out everywhere.",
          sum(D$md5_state == "mismatch"), sum(D$md5_state == "unverified"), basename(paste0(stem, "_md5.tsv"))),
  sprintf("Per-method tables: %s F1 per fit = 2TP/(2TP+FP+FN); Hamming = FP + FN.", if (opt$missing == "empty")
    "**a failed or missing (or md5-mismatched) record counts as Ŝ = ∅** (TP = FP = 0, FN = s0, F1 = 0) over all expected reps;"
    else "a failed record counts as Ŝ = ∅; missing reps are left out (--missing exclude);"),
  "Paired: b = SMC-BVS-only exact, c = method-only exact, McNemar exact p (two-sided binomial b vs b + c); Hamming W/T/L from SMC-BVS's side with sign-test p. — = no discordant pairs.", "",
  "## Per-method (success, mean Hamming, TP, FP, FN, F1)", "")
x <- PM[show(PM), ]
L <- c(L, mdt(data.frame(group = x$group, method = x$method, `ok / failed / missing` = sprintf("%d / %d / %d", x$n_ok, x$n_failed, x$n_missing),
  `success / n` = sprintf("%d/%d", x$successes, x$n_counted), Hamming = f2(x$hamming_mean), TP = f2(x$TP_mean), FP = f2(x$FP_mean),
  FN = f2(x$FN_mean), F1 = f2(x$F1_mean, 3), check.names = FALSE)), "")
for (m in BENCH) { x <- PR[PR$method == m & show(PR), ]
  L <- c(L, sprintf("## SMC-BVS vs %s (paired, shared reps)", m), "", mdt(data.frame(group = x$group, n_shared = x$n_shared,
    `md5 ≠ / unverified` = sprintf("%d / %d", x$md5_mismatch, x$md5_unverified), `exact SMC / other` = sprintf("%d / %d", x$smcbvs_exact, x$method_exact),
    `b / c` = sprintf("%d / %d", x$b_smcbvs_only, x$c_method_only), `McNemar p` = fp(x$mcnemar_p),
    `Hamming W/T/L` = sprintf("%d/%d/%d", x$hamming_wins, x$hamming_ties, x$hamming_losses), `sign p` = fp(x$sign_p),
    `mean Hamming SMC / other` = sprintf("%s / %s", f2(x$mean_hamming_smcbvs), f2(x$mean_hamming_method)),
    `mean F1 SMC / other` = sprintf("%s / %s", f2(x$mean_F1_smcbvs, 3), f2(x$mean_F1_method, 3)), check.names = FALSE)), "") }
if (nrow(MD5)) L <- c(L, "## data_md5 mismatched / unverified records", "", mdt(head(MD5[, c("method", "setting_id", "rep", "state", "md5_state")], 200)),
                      if (nrow(MD5) > 200) sprintf("(first 200 of %d; full list in the tsv)", nrow(MD5)), "")
writeLines(L, paste0(stem, ".md"))
cat(sprintf("wrote %s.md and _paired.tsv (%d rows), _permethod.tsv (%d rows), _md5.tsv (%d rows); shared (joint) %d of %d\n",
            stem, nrow(PR), nrow(PM), nrow(MD5), length(shared_joint), nrow(st) * length(REPS)))
