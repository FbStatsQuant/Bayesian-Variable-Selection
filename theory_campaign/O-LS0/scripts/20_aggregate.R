# 20_aggregate.R -- collect the per-fit LS0 records and build the cell tables of REPORT.md.
# Usage: Rscript 20_aggregate.R <OUT dir of 11_run.R> <results dir>
# Writes results/ls0_per_fit.csv (one row per fit), results/cell_summary.csv and results/tables.md.
# Production comparison: Results/SMC_BVS_v3_production/p{0500,1000}/exact_recovery_long.csv, rows method SMCBVS, rule hpm.
#   optional 3rd argument: OUT dir of the lattice-subsample run (LS0_LAT_MAX = 1024, replicates 1..20); table D and the
#   lattice columns of cell_summary.csv come from it, and its LS0 fields are checked against the main run (determinism).
args <- commandArgs(TRUE)
out <- args[1]; res <- args[2]; latdir <- if (length(args) >= 3) args[3] else NA
sd <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
repo <- normalizePath(file.path(sd, "..", "..", ".."))
readrows <- function(dir) {
  fs <- list.files(dir, "\\.rds$", recursive = TRUE, full.names = TRUE)
  x <- do.call(rbind, lapply(fs, function(f) readRDS(f)$row)); x[order(x$p, x$scenario, x$replicate, -x$c), ]
}
d <- readrows(out)
dir.create(res, showWarnings = FALSE, recursive = TRUE)
fitkey <- function(x) paste(x$dataset_id, x$scale_key)
latcols <- c("lat_size", "lat_checked", "lat_n", "lat_DS_fail", "lat_DS_all", "lat_fail_types", "lat_fail_minPhi", "lat_n_phi2", "lat_fail_phi2", "sec_lat")
if (!is.na(latdir)) {
  dl <- readrows(latdir); dl <- dl[dl$replicate <= 20, ]
  m <- match(fitkey(dl), fitkey(d))
  chk <- c("start_size", "Phi_start", "log_pi0_start", "F_S0", "F_best", "ls_moves", "ls_termination", "scored_S0", "certified_S0", "best_eq_S0", "S0_locmax")
  mism <- sum(!vapply(chk, function(v) isTRUE(all.equal(dl[[v]], d[[v]][m], tolerance = 0)), TRUE))
  writeLines(c(sprintf("lattice subsample: %d fits (replicates 1..20), %d matched in the main run", nrow(dl), sum(!is.na(m))),
               sprintf("LS0 fields compared (%s): %d field(s) differ", paste(chk, collapse = ", "), mism)),
             file.path(res, "determinism_check.txt"))
  # lattice columns of the main table: from the subsample where available, else NA (not checked)
  for (v in setdiff(latcols, "lat_size")) { d[[v]] <- NA; d[[v]][m] <- dl[[v]] }
  d$lat_checked[is.na(d$lat_checked)] <- FALSE
}

# ---- production HPM exact recovery (per cell counts)
prod <- do.call(rbind, lapply(c("p0500", "p1000"), function(pp) {
  x <- read.csv(file.path(repo, "Results", "SMC_BVS_v3_production", pp, "exact_recovery_long.csv"))
  # each file carries rows for BOTH p (the other p as empty placeholders) and a "pooled" row: keep this p, per scenario
  x <- x[x$method_id == "SMCBVS" & x$rule_id == "hpm" & x$p == as.integer(sub("^p0*", "", pp)) & x$scenario != "pooled", ]
  data.frame(p = x$p, scenario = as.integer(x$scenario), scale_key = x$scale_key, prod_n = x$n_expected,
             prod_exact = x$exact_all_sum, prod_fail = x$n_fail_total)
}))

# ---- derived per-fit classes
d$harm_possible <- d$best_beats_S0 & d$S0_locmax           # LS0 beats S0 although S0 is a strict local max
d$prod_must_miss <- !d$S0_locmax                           # S0 not a flip/swap local max => production HPM != S0 (see REPORT)
d$fail_class <- ifelse(d$scored_S0, "scored",
                 ifelse(!d$S0_locmax, "posterior: S0 not a local max",
                  ifelse(d$best_beats_S0, "posterior: LS0 found a better model",
                   ifelse(d$ls_moves == 0, "search: S~0 is a strict local max (0 moves)",
                   ifelse(!d$cap_ok & d$path_progress_all, "cap: progress-only path ran out of moves",
                    ifelse(!d$path_progress_all, "search: non-progress move", "search: other"))))))
write.csv(d, file.path(res, "ls0_per_fit.csv"), row.names = FALSE)

key <- c("scale_key", "p", "scenario")
cells <- unique(d[, key]); cells <- cells[order(-match(cells$scale_key, c("c050", "c100")), cells$p, cells$scenario), ]
med <- function(x) stats::median(x, na.rm = TRUE)
pct <- function(x) 100 * mean(x, na.rm = TRUE)
summ <- do.call(rbind, lapply(seq_len(nrow(cells)), function(i) {
  cc <- cells[i, ]; x <- d[d$scale_key == cc$scale_key & d$p == cc$p & d$scenario == cc$scenario, ]
  lc <- x[x$lat_checked, ]
  data.frame(cc, n = nrow(x),
    # start
    Phi_start_med = med(x$Phi_start), missed_med = med(x$start_missed), extras_mean = mean(x$start_extras),
    in_R0 = sum(x$start_in_R0), in_R1 = sum(x$start_in_R1), in_R2 = sum(x$start_in_R2), start_eq_S0 = sum(x$start_eq_S0),
    pi0_start_med = med(exp(x$log_pi0_start)), elig = sum(x$elig_start), pi0_R2_med = med(exp(x$log_pi0_R2)),
    pi0_R0_med = med(exp(x$log_pi0_R0)), log10_pi0_S0_med = med(x$log_pi0_S0 / log(10)),
    # LS0
    scored = sum(x$scored_S0), certified = sum(x$certified_S0), ls0_alone = sum(x$best_eq_S0),
    move_limit = sum(x$ls_termination == "move_limit"), moves_mean = mean(x$ls_moves),
    best_beats_S0 = sum(x$best_beats_S0), endpoint_beats_S0 = sum(x$endpoint_beats_S0),
    S0_not_locmax = sum(!x$S0_locmax), harm_possible = sum(x$harm_possible),
    # path
    path_progress = sum(x$path_progress_all, na.rm = TRUE), path_in_R0 = sum(x$path_in_R0), path_in_R1 = sum(x$path_in_R1),
    path_in_R2 = sum(x$path_in_R2), path_in_lat = sum(x$path_in_lat), cap_ok = sum(x$cap_ok),
    cert_given_scored = sum(x$certified_S0) / max(1, sum(x$scored_S0)),
    f_post_notlm = sum(x$fail_class == "posterior: S0 not a local max"),
    f_post_better = sum(x$fail_class == "posterior: LS0 found a better model"),
    f_cap = sum(x$fail_class == "cap: progress-only path ran out of moves"),
    f_zero = sum(x$fail_class == "search: S~0 is a strict local max (0 moves)"),
    f_nonprog = sum(x$fail_class == "search: non-progress move"), f_other = sum(x$fail_class == "search: other"),
    # lattice
    lat_checked = nrow(lc), lat_DS_all = sum(lc$lat_DS_all), lat_fail_frac_med = if (nrow(lc)) med(lc$lat_DS_fail / pmax(1, lc$lat_n)) else NA,
    lat_phi2_fail_frac = if (nrow(lc)) sum(lc$lat_fail_phi2) / max(1, sum(lc$lat_n_phi2)) else NA,
    lat_scored_given_fail = if (sum(!lc$lat_DS_all)) sum(lc$scored_S0[!lc$lat_DS_all]) else NA,
    lam_min_med = med(x$lam_min_RU), lam_min_min = min(x$lam_min_RU),
    # cost
    ls0_neval_med = med(x$ls_n_eval), ls0_sec_med = med(x$sec_ls0), ls0_sec_max = max(x$sec_ls0), setup_sec_med = med(x$sec_setup),
    cpu_sum = sum(x$cpu_total))
}))
summ <- merge(summ, prod, by = key, all.x = TRUE, sort = FALSE)
summ <- summ[order(-match(summ$scale_key, c("c050", "c100")), summ$p, summ$scenario), ]
summ$post_lo <- summ$prod_exact - pmin(summ$harm_possible, summ$prod_exact)
summ$prod_miss <- summ$prod_n - summ$prod_exact
summ$check_notlm_le_miss <- summ$S0_not_locmax <= summ$prod_miss
write.csv(summ, file.path(res, "cell_summary.csv"), row.names = FALSE)

# lattice failure types (pooled counts over checked fits, by scale)
ft <- function(x) {
  v <- unlist(strsplit(x[!is.na(x) & nzchar(x)], ";"))
  if (!length(v)) return(character(0))
  kv <- do.call(rbind, strsplit(v, ":")); tapply(as.numeric(kv[, 2]), kv[, 1], sum)
}

# ---- markdown tables
lab <- function(s) paste0("p", s$p, " S", s$scenario)
md <- character(0)
tab <- function(title, cols, hdr, rows) {
  md <<- c(md, "", paste0("#### ", title), "", paste0("| ", paste(c("cell", hdr), collapse = " | "), " |"),
           paste0("|", paste(rep("---", length(hdr) + 1), collapse = "|"), "|"))
  for (i in seq_len(nrow(rows))) md <<- c(md, paste0("| ", paste(c(lab(rows[i, ]), vapply(cols, function(f) f(rows[i, ]), "")), collapse = " | "), " |"))
}
f0 <- function(v) function(r) format(r[[v]])
fr <- function(v, k = 2) function(r) formatC(r[[v]], format = "f", digits = k)
fg <- function(v) function(r) formatC(r[[v]], format = "g", digits = 2)
for (sk in c("c100", "c050")) {
  s <- summ[summ$scale_key == sk, ]
  tot <- function(v) sum(s[[v]])
  md <- c(md, "", paste0("### Scale ", sk, " (c = ", ifelse(sk == "c100", "1", "0.5"), "), 100 fits per cell"))
  tab("A. Start mode S~0 and start masses", list(f0("Phi_start_med"), f0("missed_med"), fr("extras_mean"), f0("in_R0"), f0("in_R1"), f0("in_R2"), f0("start_eq_S0"),
      fr("pi0_start_med", 3), f0("elig"), fr("pi0_R0_med", 3), fr("pi0_R2_med", 3), fr("log10_pi0_S0_med", 1)),
      c("med Φ(S~0)", "med missed", "mean extras", "S~0∈R0", "∈R1", "∈R2", "S~0=S0", "med π0(S~0)", "π0(S~0)>½", "med π0(R0)", "med π0(R2)", "med log10 π0(S0)"), s)
  md <- c(md, sprintf("| **total** | | | | **%d** | **%d** | **%d** | **%d** | | **%d** | | | |", tot("in_R0"), tot("in_R1"), tot("in_R2"), tot("start_eq_S0"), tot("elig")))
  tab("B. LS0 outcome and comparison with production", list(f0("scored"), f0("certified"), f0("ls0_alone"), f0("prod_exact"), f0("harm_possible"),
      function(r) paste0(r$post_lo, "–", r$prod_exact), f0("best_beats_S0"), f0("S0_not_locmax"), f0("prod_miss"), f0("move_limit"), fr("moves_mean", 1)),
      c("LS0 scored S0", "LS0 certified S0", "LS0 alone = S0", "prod HPM = S0", "harm possible", "prod+LS0 exact", "LS0 beats S0", "S0 not loc. max", "prod misses", "move limit", "mean moves"), s)
  md <- c(md, sprintf("| **total** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d–%d** | **%d** | **%d** | **%d** | **%d** | |",
                      tot("scored"), tot("certified"), tot("ls0_alone"), tot("prod_exact"), tot("harm_possible"), tot("post_lo"), tot("prod_exact"),
                      tot("best_beats_S0"), tot("S0_not_locmax"), tot("prod_miss"), tot("move_limit")))
  tab("C. Path geometry (TD′ / Lemma LS-score) and failure classes", list(f0("path_progress"), f0("path_in_R0"), f0("path_in_R1"), f0("path_in_R2"), f0("path_in_lat"),
      f0("cap_ok"), fr("cert_given_scored"), f0("f_post_notlm"), f0("f_post_better"), f0("f_zero"), f0("f_cap"), f0("f_nonprog"), f0("f_other")),
      c("progress-only path", "path ⊂ R0", "⊂ R1", "⊂ R2", "path ⊂ Lat(S~0)", "ℓ ≥ Φ(S~0)−1", "P(cert | scored)", "miss: S0 not LM", "miss: LS0 beats S0", "miss: 0 moves", "miss: cap", "miss: non-progress", "miss: other"), s)
  md <- c(md, sprintf("| **total** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** | | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |",
                      tot("path_progress"), tot("path_in_R0"), tot("path_in_R1"), tot("path_in_R2"), tot("path_in_lat"), tot("cap_ok"),
                      tot("f_post_notlm"), tot("f_post_better"), tot("f_zero"), tot("f_cap"), tot("f_nonprog"), tot("f_other")))
  tab("D. Lattice D_S check on Lat(S~0) ∩ {Φ ≥ 2} (subsample r = 1..20 per cell; checked when |Lat| ≤ 1024) and (M3) on all fits", list(f0("lat_checked"), f0("lat_DS_all"), fr("lat_fail_frac_med"), fr("lat_phi2_fail_frac"),
      f0("lat_scored_given_fail"), fr("lam_min_med"), fr("lam_min_min")),
      c("fits checked", "D_S on all of Lat", "med fraction of states failing", "fraction of Φ=2 states failing", "LS0 scored S0 when D_S failed somewhere", "med λmin(R_{S~0∪S0})", "min λmin"), s)
  ftt <- ft(d$lat_fail_types[d$scale_key == sk])
  if (length(ftt)) md <- c(md, "", paste0("Failing lattice states by best-neighbour type (pooled over checked fits): ",
                                          paste(names(ftt), ftt, sep = " ", collapse = ", "), "."))
  tab("E. Cost", list(fg("ls0_neval_med"), fr("ls0_sec_med", 2), fr("ls0_sec_max", 2), fr("setup_sec_med", 2)),
      c("med LS0 score evaluations", "med LS0 seconds", "max LS0 seconds", "med setup seconds (blocks+tables+π0+graph)"), s)
}
writeLines(md, file.path(res, "tables.md"))
cat(sprintf("fits: %d; total cpu %.2f h\n", nrow(d), sum(d$cpu_total) / 3600))
print(table(d$fail_class, d$scale_key))
