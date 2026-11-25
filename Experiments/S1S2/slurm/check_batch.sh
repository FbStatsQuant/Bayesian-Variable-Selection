#!/usr/bin/env bash
# check_batch.sh -- run on NOTS. Batch health check for the S1 SMC-BVS run, with the manager's STOP rule.
#   check_batch.sh --batch K --reps LO-HI [--jobs JOBID,JOBID,...]
#   (--jobs defaults to the array job ids logged for batch K in _local/engineering/S1S2/logs/submissions.tsv)
# Reports, per setting class and overall:
#   (1) Slurm: sacct State counts (COMPLETED / FAILED / TIMEOUT / OUT_OF_MEMORY / CANCELLED / NODE_FAIL / RUNNING /
#       PENDING), elapsed (median, max) and MaxRSS (max) of the batch steps;
#   (2) records: json top-level status ok / failed:<reason> / missing, for every (setting, rep) of the batch;
#   (3) engine flags, read from each rds (extra$flags, set by v3_fit; core v3_run.R:182-207, v3_calib.R:101-110):
#       E1 (an island best < HPM F - 1), E2 (sd of island log Z > 1), E3 (final local search raised the best F),
#       low_empirical_ESS (a stage ESS < N/2); checks_passed_final = !(E1|E2|E3|low ESS)  <- the "E-flag" of the STOP
#       rule; also escalated (tier 1, N = 4 N0), checks_passed_calibration, local_limit, ls0_improved; runtime, N, tier.
# STOP rule (manager, 2026-11-25): STOP and report if ANY task failed / timed out / was OOM-killed / has no record after
# its job ended, or if E-flags (checks_passed_final == FALSE) exceed 5% of the finished fits overall or in any class.
# Writes the per-fit table to _local/engineering/S1S2/logs/check_b<K>.tsv (small) and prints the summary.
set -euo pipefail
ENG=/home/fb31/SMC-BVS/_local/engineering
RUNS=${S1S2_RUNS:-/scratch/fb31/SMC-BVS/runs/S1S2}
SUBLOG=$ENG/S1S2/logs/submissions.tsv
batch=""; reps=""; jobs=""
while (($#)); do case "$1" in --batch) batch="$2"; shift 2;; --reps) reps="$2"; shift 2;; --jobs) jobs="$2"; shift 2;;
  *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ "$batch" =~ ^[0-9]+$ && "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "usage: --batch K --reps LO-HI [--jobs ...]" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
[[ -z "$jobs" && -f "$SUBLOG" ]] && jobs=$(awk -F'\t' -v b="$batch" '$2 == b { print $3 }' "$SUBLOG" | paste -sd, -)
OUT=$ENG/S1S2/logs/check_b${batch}.tsv; mkdir -p "$(dirname "$OUT")"
tmp=$(mktemp -d /scratch/fb31/SMC-BVS/tmp/S1S2/check.XXXXXX); trap 'rm -rf "$tmp"' EXIT
: > "$tmp/sacct_x"; : > "$tmp/sacct_b"

echo "== batch $batch, reps $lo-$hi, jobs ${jobs:-<none logged>}  ($(date -u +%FT%TZ))"
if [[ -n "$jobs" ]]; then
  sacct -j "$jobs" -X -n -P -o JobID,JobName,State,ExitCode,Elapsed > "$tmp/sacct_x" || true
  sacct -j "$jobs" -n -P -o JobID,MaxRSS,Elapsed,State | grep '\.batch|' > "$tmp/sacct_b" || true
  echo "-- Slurm states (array tasks)"
  awk -F'|' '{ split($2, a, "_"); cls = a[3]; st = $3; sub(/ .*/, "", st); n[cls "|" st]++ } END { for (k in n) print k "|" n[k] }' "$tmp/sacct_x" | sort | column -t -s'|'
fi

source "$ENG/envs/S1S2/env.sh"
nice -n 19 Rscript --vanilla - "$RUNS" "$lo" "$hi" "$OUT" "$tmp/sacct_x" "$tmp/sacct_b" <<'REOF'
a <- commandArgs(TRUE); runs <- a[1]; lo <- as.integer(a[2]); hi <- as.integer(a[3]); out <- a[4]
cls_of <- function(cell) c("P500N500", "P5000N500", "P500N1000", "P5000N1000")[(cell - 1) %/% 4 + 1]
g <- expand.grid(rep = lo:hi, cell = 1:16); g$setting <- sprintf("S1_%02d", g$cell); g$class <- cls_of(g$cell)
g$task_id <- (g$cell - 1) * 100 + g$rep
flag <- function(f, k) { v <- f[[k]]; if (is.null(v) || length(v) != 1 || is.na(v)) NA else isTRUE(v) }
rows <- lapply(seq_len(nrow(g)), function(i) {
  stem <- file.path(runs, "smcbvs", g$setting[i], sprintf("rep_%03d", g$rep[i]))
  r <- list(status = "missing")
  if (file.exists(paste0(stem, ".json"))) {
    j <- tryCatch(jsonlite::fromJSON(paste0(stem, ".json"), simplifyVector = FALSE), error = function(e) list(status = "failed: unreadable json"))
    r$status <- j$status %||% "failed: no status"
  }
  if (file.exists(paste0(stem, ".rds"))) {
    x <- tryCatch(readRDS(paste0(stem, ".rds")), error = function(e) NULL)
    f <- x$extra$flags
    if (!is.null(f)) for (k in c("E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final", "escalated",
                                 "checks_passed_calibration", "local_limit", "ls0_improved")) r[[k]] <- flag(f, k)
    r$runtime_sec <- x$runtime_sec %||% NA; r$N <- x$extra$N_particles %||% NA; r$tier <- x$extra$tier %||% NA
    r$success <- isTRUE(x$success); r$rds_kb <- round(file.size(paste0(stem, ".rds")) / 1024, 1)
  }
  as.data.frame(r[setdiff(names(r), character(0))], stringsAsFactors = FALSE)
})
cols <- c("status", "E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final", "escalated", "checks_passed_calibration",
          "local_limit", "ls0_improved", "runtime_sec", "N", "tier", "success", "rds_kb")
tab <- do.call(rbind, lapply(rows, function(r) { for (k in setdiff(cols, names(r))) r[[k]] <- NA; r[cols] }))
tab <- cbind(g[c("task_id", "setting", "rep", "class")], tab)
write.table(tab, out, sep = "\t", quote = FALSE, row.names = FALSE)
done <- tab$status != "missing"
ok <- tab$status == "ok"
summ <- function(d) {
  okd <- d[d$status == "ok", ]
  data.frame(tasks = nrow(d), records = sum(d$status != "missing"), ok = nrow(okd), failed = sum(grepl("^failed", d$status)),
             missing = sum(d$status == "missing"), Eflag = sum(okd$checks_passed_final %in% FALSE),
             Eflag_pct = if (nrow(okd)) round(100 * mean(okd$checks_passed_final %in% FALSE), 1) else NA,
             E1 = sum(okd$E1 %in% TRUE), E2 = sum(okd$E2 %in% TRUE), E3 = sum(okd$E3 %in% TRUE), lowESS = sum(okd$low_empirical_ESS %in% TRUE),
             escalated = sum(okd$escalated %in% TRUE), calib_fail = sum(okd$checks_passed_calibration %in% FALSE),
             local_limit = sum(okd$local_limit %in% TRUE), success = sum(okd$success %in% TRUE),
             rt_med_s = if (nrow(okd)) round(median(okd$runtime_sec, na.rm = TRUE)) else NA,
             rt_max_s = if (nrow(okd)) round(max(okd$runtime_sec, na.rm = TRUE)) else NA,
             rds_kb_med = if (nrow(okd)) median(okd$rds_kb, na.rm = TRUE) else NA)
}
S <- do.call(rbind, c(lapply(split(tab, tab$class), summ), list(ALL = summ(tab))))
cat("-- records and engine flags (Eflag = checks_passed_final FALSE among ok fits)\n"); print(S)
fails <- tab[grepl("^failed", tab$status), c("setting", "rep", "status")]
if (nrow(fails)) { cat("-- failed records\n"); print(utils::head(fails, 30)) }
# sacct: states and RSS per class
sx <- tryCatch(read.delim(a[5], sep = "|", header = FALSE, col.names = c("JobID", "JobName", "State", "Exit", "Elapsed")), error = function(e) NULL)
bad_sacct <- 0L; unfinished <- 0L
if (!is.null(sx) && nrow(sx)) {
  st <- sub(" .*", "", sx$State)
  bad_sacct <- sum(st %in% c("FAILED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL", "CANCELLED", "PREEMPTED", "BOOT_FAIL", "DEADLINE"))
  unfinished <- sum(st %in% c("PENDING", "RUNNING", "REQUEUED", "SUSPENDED", "CONFIGURING", "COMPLETING"))
  sb <- tryCatch(read.delim(a[6], sep = "|", header = FALSE, col.names = c("JobID", "MaxRSS", "Elapsed", "State")), error = function(e) NULL)
  if (!is.null(sb) && nrow(sb)) {
    kb <- function(x) { u <- sub("^[0-9.]+", "", x); v <- as.numeric(sub("[KMG]$", "", x)); v * c(K = 1, M = 1024, G = 1024^2)[u] }
    tid <- as.integer(sub("^[0-9]+_([0-9]+)\\..*$", "\\1", sb$JobID)); cl <- cls_of((tid - 1) %/% 100 + 1)
    rss <- tapply(kb(sb$MaxRSS) / 1024^2, cl, max, na.rm = TRUE)
    cat("-- max RSS (GB) per class (sacct .batch steps)\n"); print(round(rss, 2))
  }
}
eflag_pct <- tapply(tab$checks_passed_final[ok] %in% FALSE, tab$class[ok], mean)
reasons <- c(if (bad_sacct) paste0(bad_sacct, " tasks in a bad Slurm state"),
             if (any(grepl("^failed", tab$status))) paste0(sum(grepl("^failed", tab$status)), " failed records"),
             if (unfinished == 0 && any(!done)) paste0(sum(!done), " tasks without a record after their jobs ended"),
             if (any(ok) && mean(tab$checks_passed_final[ok] %in% FALSE) > 0.05) "E-flags > 5% overall",
             if (any(eflag_pct > 0.05)) paste0("E-flags > 5% in class ", paste(names(eflag_pct)[eflag_pct > 0.05], collapse = ",")))
cat(sprintf("-- unfinished Slurm tasks: %d\n", unfinished))
cat(if (length(reasons)) paste0("VERDICT: STOP -- ", paste(reasons, collapse = "; "), "\n") else
    if (unfinished > 0) "VERDICT: RUNNING -- no STOP condition so far\n" else "VERDICT: PASS -- no STOP condition\n")
cat("per-fit table:", out, "\n")
REOF
