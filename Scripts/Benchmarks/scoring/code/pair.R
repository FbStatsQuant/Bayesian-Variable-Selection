# pair.R: paired exact recovery at c = 1 and c = 0.5 on the same datasets (thread S, 2026-10-21).
# The two scales share X and the noise (y_c = c * X beta + eps, master §II.6), so each dataset gives one
# pair per (method_id, rule_id). Every rule present at both scales is paired, pre-declared and derived.
#
# Usage: Rscript --vanilla pair.R --c050 <dir of scored c050 runs> --c100 <dir of scored c100 runs> --out <dir>
# Each run folder holds scored_rows.csv (score.R). Runs are matched by their method folder suffix.
# Output: <out>/paired_c100_c050.csv (per method, rule, p, scenario and pooled) and paired_c100_c050.md.

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))

method_folder <- function(run_id) sub("^.*_prod(c[0-9]{3})?_", "", run_id)

read_exact <- function(run_dir) {
  s <- utils::read.csv(file.path(run_dir, "scored_rows.csv"), colClasses = "character", na.strings = "NA")
  s[, c("dataset_id", "p", "scenario", "scale_key", "method_id", "rule_id", "role", "exact", "status")]
}

pair_runs <- function(dir050, dir100, out_dir) {
  r050 <- list.dirs(dir050, recursive = FALSE); r100 <- list.dirs(dir100, recursive = FALSE)
  f100 <- setNames(r100, method_folder(basename(r100)))
  out <- list()
  for (d5 in r050) {
    d1 <- f100[[method_folder(basename(d5))]]
    if (is.null(d1)) { cat("no c = 1 run for", basename(d5), "\n"); next }
    a <- read_exact(d5); b <- read_exact(d1)
    stopifnot(all(a$scale_key == "c050"), all(b$scale_key == "c100"))
    key_a <- paste(a$dataset_id, a$method_id, a$rule_id); key_b <- paste(b$dataset_id, b$method_id, b$rule_id)
    stopifnot(!anyDuplicated(key_a), !anyDuplicated(key_b))
    common_rules <- unique(paste(a$method_id, a$rule_id)[paste(a$method_id, a$rule_id) %in% paste(b$method_id, b$rule_id)])
    for (mr in common_rules) {
      m <- sub(" .*$", "", mr); rule <- sub("^[^ ]* ", "", mr)
      for (p in DESIGN_P) for (sc in c(DESIGN_SCENARIOS, NA)) {
        sa <- a[a$method_id == m & a$rule_id == rule & as.integer(a$p) == p & (is.na(sc) | as.integer(a$scenario) == sc), ]
        sb <- b[b$method_id == m & b$rule_id == rule & as.integer(b$p) == p & (is.na(sc) | as.integer(b$scenario) == sc), ]
        ids <- intersect(sa$dataset_id, sb$dataset_id)
        ea <- sa$exact[match(ids, sa$dataset_id)] == "TRUE"; eb <- sb$exact[match(ids, sb$dataset_id)] == "TRUE"
        out[[length(out) + 1]] <- data.frame(
          method_id = m, rule_id = rule, role_c050 = sa$role[1], label_c100 = rule_label(m, rule, "c100"),
          label_c050 = rule_label(m, rule, "c050"), p = p, scenario = if (is.na(sc)) "pooled" else as.character(sc),
          n_pairs = length(ids), n_unpaired = length(union(sa$dataset_id, sb$dataset_id)) - length(ids),
          exact_c100 = sum(eb), exact_c050 = sum(ea), both = sum(ea & eb), c100_only = sum(eb & !ea),
          c050_only = sum(ea & !eb), neither = sum(!ea & !eb),
          run_c100 = basename(d1), run_c050 = basename(d5), stringsAsFactors = FALSE)
      }
    }
  }
  out <- do.call(rbind, out)
  # Method order of the tables (SuSiE-refine beside A1 and SuSiE-L100), then rule, p, scenario.
  ORDER <- c("F1", "F2", "F3", "F4", "F4_SCAD", "F5", "A1", "SuSiE-L100", "SuSiE-refine", "A2", "SSL-RS", "A3")
  out <- out[order(match(out$method_id, ORDER), out$run_c050, seq_len(nrow(out))), ]
  write_table(out, file.path(out_dir, "paired_c100_c050.csv"))
  pooled <- out[out$scenario == "pooled", ]
  md <- c("# Paired exact recovery, c = 1 vs c = 0.5 (same datasets)", "",
          "Provisional (G5). c = 1 from combined_v2; c = 0.5 from combined_c050. Labels per PREREG_c050 R1 (derived rules: post hoc at c = 1, pre-registered at c = 0.5).",
          "Counts out of the paired datasets (600 per p when complete); c050_only = exact at c = 0.5 but not at c = 1.", "",
          "| method | rule | role (c050) | p | pairs | exact c=1 | exact c=0.5 | both | c=1 only | c=0.5 only | neither |",
          "|---|---|---|---|---|---|---|---|---|---|---|",
          sprintf("| %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | %d |", pooled$method_id, pooled$rule_id, pooled$role_c050,
                  pooled$p, pooled$n_pairs, pooled$exact_c100, pooled$exact_c050, pooled$both, pooled$c100_only,
                  pooled$c050_only, pooled$neither), "",
          "Per-scenario rows: paired_c100_c050.csv.")
  writeLines(md, file.path(out_dir, "paired_c100_c050.md"))
  cat("pair: wrote", nrow(out), "rows to", out_dir, "\n")
  invisible(out)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(TRUE)
  get <- function(k) a[which(a == k) + 1]
  pair_runs(get("--c050"), get("--c100"), get("--out"))
}
