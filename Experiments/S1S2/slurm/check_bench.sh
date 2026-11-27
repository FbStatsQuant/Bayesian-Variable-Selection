#!/usr/bin/env bash
# check_bench.sh -- run on NOTS (normally via check_batch.sh --method M, which hands over here for any method other than
# smcbvs). Batch health check of a BENCHMARK batch with the HQ benchmark STOP rule (2026-11-26/27). OURS (operational).
#   check_bench.sh --suite 1|2 --method M --batch K --reps LO-HI [--jobs JOBID,...]
#   (--jobs defaults to the array ids logged under "S<suite>bm.<M>.<K>" in _local/engineering/S1S2/logs/submissions.tsv)
# Per rep of the batch (settings of the suite x reps LO..HI): json top-level status ok / failed:<reason> / missing;
# crashed = no record although the array task holding the rep has ended (task_id from tasks_S<suite>_bench_<M>.tsv); once
# no task of the batch is pending/running, every rep without a record counts as crashed.
# DATA IDENTITY: every benchmark record carrying a data_md5 is compared with the SMC-BVS record of the same (suite,
# setting, rep): first the reference index $REF (suite, setting_id, rep, data_md5; built by harness/md5_index.R from the
# SMC-BVS records, installed on NOTS by install_md5_ref.sh), else the live json $RUNS/smcbvs/<setting>/rep_RRR.json.
# Both are NOTS R 4.5.2 records, so equality must be exact. An ok record without data_md5 counts as a mismatch; a failed
# record without one (e.g. the sbatch's "harness wall timeout" json) is reported as unverifiable.
# STOP (benchmarks have no E-flag rule):
#   - failed + crashed reps > 5% of the finished reps (records + crashed), overall or in a class; while tasks are still
#     pending/running the rule applies to a group only once it has >= 20 finished reps (noise guard; at batch end always);
#   - any task OUT_OF_MEMORY or NODE_FAIL (sacct). EXCEPT bas_mc3 (HQ ruling 2026-11-27): an OUT_OF_MEMORY task that
#     requested < 64G is a reported WARNING (its rc=137 reps get one 64G pass, submit_bench.sh --oom-pass); an
#     OUT_OF_MEMORY at >= 64G, and any NODE_FAIL, stay STOP; REFINED by HQ (2026-11-27, option 1): a rep killed at
#     >= 64G (its rc=137 stub sits in an OUT_OF_MEMORY task of a >= 64G job, i.e. the --oom-pass) is a BAS computational
#     failure, reported, and a STOP only if such reps exceed 2% of the batch's S2N50P1000 reps or occur in any other
#     class (S2N100P1000; any S1 class);
#   - the method's billed CPU-h (sacct CPUTimeRAW over ALL its S<suite>bm.<M>.* jobs, every batch) >= budget_cpuh in
#     bench_budget.tsv;
#   - ANY data-identity mismatch, or a record whose SMC-BVS reference is missing although the SMC-BVS rep is ok.
#     A rep whose SMC-BVS fit has not finished (no json / non-ok stub, e.g. a running rerun) is "ref_pending": reported
#     in the verdict line, not a STOP; its identity is checked once the SMC-BVS record exists (re-run this check).
# RUNNING while tasks are pending/running and no STOP condition holds; PASS at batch end otherwise.
# Writes the per-rep table to _local/engineering/S1S2/logs/check_s<suite>bm_<M>_b<K>.tsv and prints the summary.
# Test overrides (default = the NOTS paths): S1S2_ENG, S1S2_RUNS, S1S2_TMP, S1S2_ENV, S1S2_MD5_REF.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ENG=${S1S2_ENG:-/home/fb31/SMC-BVS/_local/engineering}
RUNS=${S1S2_RUNS:-/scratch/fb31/SMC-BVS/runs/S1S2}
TMPB=${S1S2_TMP:-/scratch/fb31/SMC-BVS/tmp/S1S2}
ENVF=${S1S2_ENV:-$ENG/envs/S1S2/env.sh}
REF=${S1S2_MD5_REF:-$ENG/S1S2/ref/smcbvs_data_md5.tsv}
SUBLOG=$ENG/S1S2/logs/submissions.tsv
CONF=$HERE/bench_budget.tsv
suite=""; method=""; batch=""; reps=""; jobs=""
while (($#)); do case "$1" in --suite) suite="$2"; shift 2;; --method) method="$2"; shift 2;; --batch) batch="$2"; shift 2;;
  --reps) reps="$2"; shift 2;; --jobs) jobs="$2"; shift 2;; *) echo "unknown arg $1" >&2; exit 64;; esac; done
[[ ( "$suite" == 1 || "$suite" == 2 ) && "$method" =~ ^[a-z0-9_]+$ && "$method" != smcbvs && "$batch" =~ ^[0-9]+$ &&
   "$reps" =~ ^([0-9]+)-([0-9]+)$ ]] || { echo "usage: --suite 1|2 --method M --batch K --reps LO-HI [--jobs ...]" >&2; exit 64; }
lo=${BASH_REMATCH[1]}; hi=${BASH_REMATCH[2]}
budget=$(awk -F'\t' -v s="$suite" -v m="$method" 'NR > 1 && $1 == s && $2 == m { print $4 }' "$CONF")
[[ "$budget" =~ ^[0-9]+(\.[0-9]+)?$ ]] || { echo "no (suite $suite, $method) budget in $CONF" >&2; exit 65; }
TASKS=$HERE/tasks_S${suite}_bench_${method}.tsv; [[ -f "$TASKS" ]] || { echo "no task list $TASKS" >&2; exit 65; }
bkey=S${suite}bm.${method}.${batch}; mkey=S${suite}bm.${method}.
OUT=$ENG/S1S2/logs/check_s${suite}bm_${method}_b${batch}.tsv
[[ -z "$jobs" && -f "$SUBLOG" ]] && jobs=$(awk -F'\t' -v b="$bkey" '$2 == b || $2 == b "m" { print $3 }' "$SUBLOG" | paste -sd, -)   # + its --oom-pass
alljobs=""; [[ -f "$SUBLOG" ]] && alljobs=$(awk -F'\t' -v k="$mkey" 'index($2, k) == 1 { print $3 }' "$SUBLOG" | sort -u | paste -sd, -)
mkdir -p "$(dirname "$OUT")" "$TMPB"
tmp=$(mktemp -d "$TMPB/checkbm.XXXXXX"); trap 'rm -rf "$tmp"' EXIT
: > "$tmp/sacct_x"; : > "$tmp/sacct_b"; used=0

echo "== suite $suite method $method batch $batch, reps $lo-$hi, jobs ${jobs:-<none logged>}  ($(date -u +%FT%TZ))"
if [[ -n "$jobs" ]]; then
  sacct -j "$jobs" -X -n -P -o JobID,JobName,State,ExitCode,Elapsed,ReqMem > "$tmp/sacct_x" || true
  sacct -j "$jobs" -n -P -o JobID,MaxRSS,Elapsed,State | grep '\.batch|' > "$tmp/sacct_b" || true
  echo "-- Slurm states (array tasks)"
  awk -F'|' '{ n = split($2, a, "_"); cls = a[n]; st = $3; sub(/ .*/, "", st); c[cls "|" st]++ } END { for (k in c) print k "|" c[k] }' "$tmp/sacct_x" | sort | column -t -s'|'
fi
if [[ -n "$alljobs" ]]; then used=$( { sacct -j "$alljobs" -X -n -P -o CPUTimeRAW 2>/dev/null || true; } | awk '{ s += $1 } END { printf "%.2f", s / 3600 }'); fi
echo "-- billed CPU-h, all S${suite}bm.${method}.* jobs (${alljobs:-none}): $used of budget $budget"

source "$ENVF"
nice -n 19 Rscript --vanilla - "$RUNS" "$lo" "$hi" "$OUT" "$tmp/sacct_x" "$tmp/sacct_b" "$suite" "$method" "$TASKS" "$REF" "$used" "$budget" <<'REOF'
a <- commandArgs(TRUE); runs <- a[1]; lo <- as.integer(a[2]); hi <- as.integer(a[3]); out <- a[4]; suite <- as.integer(a[7])
method <- a[8]; tasks_f <- a[9]; ref_f <- a[10]; used <- as.numeric(a[11]); budget <- as.numeric(a[12])
`%||%` <- function(x, y) if (is.null(x)) y else x
if (suite == 1) {
  cls_of <- function(cell) c("P500N500", "P5000N500", "P500N1000", "P5000N1000")[(cell - 1) %/% 4 + 1]
  g <- expand.grid(rep = lo:hi, cell = 1:16); g$setting <- sprintf("S1_%02d", g$cell)
} else {
  cls_of <- function(cell) ifelse(cell <= 60, "S2N50P1000", "S2N100P1000")
  g <- expand.grid(rep = lo:hi, cell = 1:120); g$setting <- sprintf("S2_%03d", g$cell)
}
g$class <- cls_of(g$cell)
# rep -> array task id (the block holding it)
tk <- read.delim(tasks_f, colClasses = c("integer", "character", "integer", "integer", "integer"))
tk$cell <- (tk$task_id - tk$rep_lo) %/% 100 + 1
g$task_id <- NA_integer_
for (i in seq_len(nrow(tk))) { j <- g$cell == tk$cell[i] & g$rep >= tk$rep_lo[i] & g$rep <= tk$rep_hi[i]; g$task_id[j] <- tk$task_id[i] }
# Slurm task states: "<array>_<task>" rows only (a pending range "<array>_[..]" is not one task)
sx <- tryCatch(read.delim(a[5], sep = "|", header = FALSE, col.names = c("JobID", "JobName", "State", "Exit", "Elapsed", "ReqMem"),
                          colClasses = "character"), error = function(e) NULL)
ended_ids <- integer(0); unfinished <- 0L; oom_nf <- 0L; bad_states <- 0L; oom_warn <- 0L; hi_oom_tids <- integer(0)
if (!is.null(sx) && nrow(sx)) {
  st <- sub(" .*", "", sx$State)
  unfinished <- sum(st %in% c("PENDING", "RUNNING", "REQUEUED", "SUSPENDED", "CONFIGURING", "COMPLETING", "RESIZING"))
  oom_nf <- sum(st %in% c("OUT_OF_MEMORY", "NODE_FAIL"))
  if (identical(method, "bas_mc3")) {   # HQ ruling 2026-11-27: OOM below 64G = warning (64G pass follows)
    rq <- sub("[nc]$", "", sx$ReqMem); rg <- suppressWarnings(as.numeric(sub("[KMGT]$", "", rq))) *
      c(K = 1 / 1024^2, M = 1 / 1024, G = 1, T = 1024)[sub("^[0-9.]+", "", rq)]
    low <- st == "OUT_OF_MEMORY" & !is.na(rg) & rg < 64
    oom_warn <- sum(low); oom_nf <- oom_nf - oom_warn
    hi <- st == "OUT_OF_MEMORY" & !is.na(rg) & rg >= 64 & grepl("^[0-9]+_[0-9]+$", sx$JobID)   # judged per rep below
    hi_oom_tids <- unique(as.integer(sub("^[0-9]+_", "", sx$JobID[hi]))); oom_nf <- oom_nf - sum(hi)
  }
  bad_states <- sum(st %in% c("FAILED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL", "CANCELLED", "PREEMPTED", "BOOT_FAIL", "DEADLINE"))
  one <- grepl("^[0-9]+_[0-9]+$", sx$JobID)
  ended_ids <- unique(as.integer(sub("^[0-9]+_", "", sx$JobID[one & !(st %in% c("PENDING", "RUNNING", "REQUEUED", "SUSPENDED",
                                                                                  "CONFIGURING", "COMPLETING", "RESIZING"))])))
}
# SMC-BVS reference: index first, live json second
ref <- if (file.exists(ref_f)) read.delim(ref_f, colClasses = c(suite = "integer", setting_id = "character", rep = "integer", data_md5 = "character")) else
  data.frame(suite = integer(0), setting_id = character(0), rep = integer(0), data_md5 = character(0))
ref <- ref[ref$suite == suite, ]
refkey <- setNames(ref$data_md5, paste(ref$setting_id, ref$rep))
md5_of_json <- function(f) if (file.exists(f)) tryCatch(jsonlite::fromJSON(f, simplifyVector = FALSE)$data_md5 %||% NA_character_,
                                                       error = function(e) NA_character_) else NA_character_
rows <- lapply(seq_len(nrow(g)), function(i) {
  f <- file.path(runs, method, g$setting[i], sprintf("rep_%03d.json", g$rep[i]))
  r <- list(status = "missing", success = NA, runtime_sec = NA_real_, data_md5 = NA_character_, ref_md5 = NA_character_,
            ref_src = NA_character_, md5 = NA_character_)
  if (file.exists(f)) {
    j <- tryCatch(jsonlite::fromJSON(f, simplifyVector = FALSE), error = function(e) list(status = "failed: unreadable json"))
    r$status <- j$status %||% "failed: no status"; r$success <- isTRUE(j$success) && identical(r$status, "ok")
    r$runtime_sec <- as.numeric(j$runtime_sec %||% NA); r$data_md5 <- as.character(j$data_md5 %||% NA)
    k <- paste(g$setting[i], g$rep[i])
    if (!is.na(refkey[k])) { r$ref_md5 <- unname(refkey[k]); r$ref_src <- "index" } else {
      sj <- file.path(runs, "smcbvs", g$setting[i], sprintf("rep_%03d.json", g$rep[i]))
      r$ref_md5 <- md5_of_json(sj)
      # SMC-BVS rep not finished (no json, or a non-ok stub such as a timeout whose rerun is still running): the
      # reference does not exist YET -> "ref_pending" (reported, not a STOP; manager 2026-11-27, S1_08 reps 12/17)
      s_ok <- file.exists(sj) && identical(tryCatch(jsonlite::fromJSON(sj, simplifyVector = FALSE)$status, error = function(e) NULL), "ok")
      r$ref_src <- if (!is.na(r$ref_md5)) "live_json" else if (s_ok) "none" else "pending" }
    r$md5 <- if (is.na(r$data_md5)) { if (identical(r$status, "ok")) "absent_in_ok_record" else "unverifiable" } else
             if (is.na(r$ref_md5)) { if (identical(r$ref_src, "pending")) "ref_pending" else "no_reference" } else if (identical(r$data_md5, r$ref_md5)) "match" else "MISMATCH"
  }
  as.data.frame(r, stringsAsFactors = FALSE)
})
tab <- cbind(g[c("task_id", "setting", "rep", "class")], do.call(rbind, rows))
tab$crashed <- tab$status == "missing" & (tab$task_id %in% ended_ids | unfinished == 0)   # at batch end every missing rep
write.table(tab, out, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
tab$failed <- grepl("^failed", tab$status)
summ <- function(d) {
  fin <- sum(d$status != "missing") + sum(d$crashed); bad <- sum(d$failed) + sum(d$crashed)
  data.frame(reps = nrow(d), records = sum(d$status != "missing"), ok = sum(d$status == "ok"), failed = sum(d$failed),
             timeout = sum(grepl("timeout", d$status)), crashed = sum(d$crashed), missing = sum(d$status == "missing" & !d$crashed),
             bad_pct = if (fin) round(100 * bad / fin, 1) else NA, finished = fin, success = sum(d$success %in% TRUE),
             md5_match = sum(d$md5 %in% "match"), md5_MISMATCH = sum(d$md5 %in% c("MISMATCH", "absent_in_ok_record")),
             md5_noref = sum(d$md5 %in% "no_reference"), md5_refpend = sum(d$md5 %in% "ref_pending"), md5_unverif = sum(d$md5 %in% "unverifiable"),
             ref_index = sum(d$ref_src %in% "index"), ref_live = sum(d$ref_src %in% "live_json"),
             rt_med_s = if (any(d$status == "ok")) round(median(d$runtime_sec[d$status == "ok"], na.rm = TRUE), 1) else NA)
}
S <- do.call(rbind, c(lapply(split(tab, tab$class), summ), list(ALL = summ(tab))))
cat("-- records (bad = failed + crashed; bad_pct of finished reps) and data identity vs SMC-BVS\n"); print(S)
fails <- tab[tab$failed | tab$crashed, c("setting", "rep", "task_id", "status")]
if (nrow(fails)) { cat("-- failed / crashed reps\n"); print(utils::head(fails, 30)) }
mm <- tab[tab$md5 %in% c("MISMATCH", "absent_in_ok_record", "no_reference", "ref_pending"), c("setting", "rep", "md5", "data_md5", "ref_md5", "ref_src")]
if (nrow(mm)) { cat("-- DATA IDENTITY problems\n"); print(utils::head(mm, 30)) }
sb <- tryCatch(read.delim(a[6], sep = "|", header = FALSE, col.names = c("JobID", "MaxRSS", "Elapsed", "State")), error = function(e) NULL)
if (!is.null(sb) && nrow(sb)) {
  kb <- function(x) { u <- sub("^[0-9.]+", "", x); v <- as.numeric(sub("[KMG]$", "", x)); v * c(K = 1, M = 1024, G = 1024^2)[u] }
  tid <- as.integer(sub("^[0-9]+_([0-9]+)\\..*$", "\\1", sb$JobID)); cl <- cls_of((tid - 1) %/% 100 + 1)
  cat("-- max RSS (GB) per class (sacct .batch steps)\n"); print(round(tapply(kb(sb$MaxRSS) / 1024^2, cl, max, na.rm = TRUE), 2))
}
grp <- split(tab, tab$class); grp$ALL <- tab
over5 <- vapply(grp, function(d) { fin <- sum(d$status != "missing") + sum(d$crashed); bad <- sum(d$failed) + sum(d$crashed)
  fin > 0 && (unfinished == 0 || fin >= 20) && bad / fin > 0.05 }, TRUE)
nmm <- sum(tab$md5 %in% c("MISMATCH", "absent_in_ok_record")); nnr <- sum(tab$md5 %in% "no_reference")
comp_reasons <- character(0)
if (identical(method, "bas_mc3")) {   # reps killed at >= 64G = BAS computational (HQ 2026-11-27)
  comp <- grepl("rc=137", tab$status) & tab$task_id %in% hi_oom_tids
  if (length(hi_oom_tids)) {
    cc <- tapply(comp, tab$class, sum); nn <- table(tab$class)[names(cc)]
    cat("-- bas_mc3 computational failures (rep killed at >= 64G) per class\n"); print(data.frame(class = names(cc), comp = as.integer(cc), reps = as.integer(nn), pct = round(100 * as.integer(cc) / as.integer(nn), 2)), row.names = FALSE)
    if (any(comp)) { cat("   reps:", paste(tab$setting[comp], tab$rep[comp], collapse = "; "), "\n") }
    for (k in names(cc)) if (cc[[k]] > 0 && (k != "S2N50P1000" || cc[[k]] / nn[[k]] > 0.02))
      comp_reasons <- c(comp_reasons, sprintf("bas_mc3 computational (64G OOM) %d/%d in %s", cc[[k]], nn[[k]], k))
  }
}
reasons <- c(comp_reasons, if (any(over5)) paste0("failed+crashed > 5% in ", paste(names(over5)[over5], collapse = ",")),
             if (oom_nf) paste0(oom_nf, " tasks OUT_OF_MEMORY/NODE_FAIL"),
             if (used >= budget) sprintf("billed CPU-h %.2f >= budget %g", used, budget),
             if (nmm) paste0(nmm, " data_md5 MISMATCH vs SMC-BVS"),
             if (nnr) paste0(nnr, " records without an SMC-BVS reference md5"))
cat(sprintf("-- unfinished Slurm tasks: %d; tasks in a bad Slurm state: %d; billed CPU-h %.2f / %g\n", unfinished, bad_states, used, budget))
nrp <- sum(tab$md5 %in% "ref_pending")
rp_note <- if (nrp) sprintf(" (%d reps await their SMC-BVS reference: SMC-BVS rep not finished; re-check later)", nrp) else ""
if (oom_warn) rp_note <- paste0(rp_note, sprintf("; WARNING: %d tasks OUT_OF_MEMORY below 64G (bas_mc3 ruling: one 64G pass for their rc=137 reps, submit_bench.sh --oom-pass)", oom_warn))
cat(if (length(reasons)) paste0("VERDICT: STOP -- ", paste(reasons, collapse = "; "), "\n") else
    if (unfinished > 0) paste0("VERDICT: RUNNING -- no STOP condition so far", rp_note, "\n") else
    paste0("VERDICT: PASS -- no STOP condition", rp_note, "\n"))
cat("per-rep table:", out, "\n")
REOF
