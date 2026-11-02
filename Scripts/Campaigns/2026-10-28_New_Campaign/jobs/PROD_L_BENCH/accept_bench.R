#!/usr/bin/env Rscript
# accept_bench.R -- laptop acceptance of the downloaded PROD-L benchmark results (DESIGN.md section 6). One R process; reads RDS records, the sealed
# INPUTS manifest and the frozen code; fits nothing; touches no truth.
#   Rscript accept_bench.R --results <downloaded <STAMP>_lowp_benchres folder> --lists <units.tsv> --code <code/bench_lowp>
#                          --r2-manifest <code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt>
#                          --inputs-manifest <sealed study>/manifests/inputs_manifest_lowp.csv --out <dir> [--local-test]
# Every check is against an AUTHORITATIVE source, never learned from the records themselves (Sol PROD_L_BENCH R1, I1-I4):
#   code     the supplied --code tree must equal the r2 manifest (34 files); its runner fingerprint files are hashed here.
#   I1 rules the exact ordered (rule_id, role) sequence = frozen registry (config_lowp.R) + the deterministic transformation of
#            R/common.R::lowp_derive: F1-F5 roles of ebic1/ebic05/bic -> secondary; F4/F5 append <a>_K37 for a in (ebic1, ebic05, bic)
#            present (ebic1_K37 primary, others S0) then ebic1_lam005 (F4) / sic_smax (F5) as S0; A1-A3 = registry exactly. No missing, extra
#            or reordered rule; statuses ok/warning/failed; a failed rule selects nothing.
#   I2 D42.5 F1-F5: `coefficients` identical to fit$coefficients, one entry per rule in row order, rule_id/status equal to the row; for a
#            non-failed rule beta_pen numeric, length p, finite, its support = the row's support; beta_ols numeric length p and, by the SPEC
#            contract (bench_v2 SPEC section 3), all NA for the CV rules of F1-F3 (cv_min, cv_1se) and otherwise finite with no nonzero
#            entry outside the penalized support; for a failed rule lengths p (NA allowed). EBIC/K37 pairs equal in support, k, criterion.
#            A1-A3: a fit with at least one non-failed rule has fit$beta numeric, length p, finite; A1 (SuSiE) additionally fit$pip numeric,
#            length p, finite, in [0, 1]; A2/A3 have no PIP output (if one is present it must satisfy the same bounds).
#   I3 identity every row: dataset/case/method ids, p/scenario/replicate from the id, production seeds derived with the frozen CLI formulas
#            (data 1210000|1310000 + 10000 s + r; fold 3210000|3310000 + 10000 s + r; method = data + 4,000,000) and equal to the sealed inputs
#            manifest row; scale_key = the list's scale and scale = 1 | 0.5; run_id = the results folder name; inputs/x/y(scale)/fold hashes =
#            the manifest's; record$input$hashes identical to the manifest's eight hashes. All required fields present and nonmissing.
#   I4 provenance  rows$source_sha256 = record$code$source_sha256 = the runner's fingerprint recomputed from record$code$files, and
#            record$code$files = the supplied r2 tree's hashes (same names and values); environment identity nonmissing and = the rows'.
#            Unless --local-test: R 4.5.2; test_library FALSE (record and rows); sealed_library = the pinned path; package provenance
#            nonempty, containing every pinned package of the method (and digest) at its pinned version; a package may lie in R's own
#            library only if it is base or recommended, every other one directly in the pinned library.
# D54.3: the ABESS exact size check is NOT performed here; it is deferred and disclosed.
# --local-test (laptop runs with the test library) skips ONLY the environment checks of I4 (R version, test_library, pinned library,
# package versions/locations); I1-I3 and the code anchoring always apply.
# Exit 0 ACCEPTED; 2 FAIL; 3 INCOMPLETE (a record missing or unreadable). Writes <out>/ACCEPT_BENCH.md and <out>/accept_bench.csv.
PINNED <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
METHODS <- c("F1","F2","F3","F4","F5","A1","A2","A3")
BASE_RECOMMENDED <- c("base","compiler","datasets","graphics","grDevices","grid","methods","parallel","splines","stats","stats4","tcltk","tools",
  "utils","boot","class","cluster","codetools","foreign","KernSmooth","lattice","MASS","Matrix","mgcv","nlme","nnet","rpart","spatial","survival")
args <- commandArgs(TRUE)
opt <- list(); i <- 1L
while (i <= length(args)) {
  k <- args[[i]]
  if (k == "--local-test") { opt$local <- TRUE; i <- i + 1L; next }
  if (!k %in% c("--results","--lists","--code","--out","--r2-manifest","--inputs-manifest") || i == length(args)) stop("bad argument: ", k)
  opt[[sub("^--","",k)]] <- args[[i+1L]]; i <- i + 2L
}
for (k in c("results","lists","code","out","r2-manifest","inputs-manifest")) if (is.null(opt[[k]])) stop("missing --", k)
local <- isTRUE(opt$local)
dir.create(opt$out, recursive = TRUE, showWarnings = FALSE)
sha <- function(f) digest::digest(file = f, algo = "sha256")
# ---- the supplied code must be the frozen r2 tree --------------------------------------------------------------------------------------------
r2 <- readLines(opt[["r2-manifest"]], warn = FALSE); r2 <- r2[nzchar(r2)]
r2_hash <- sub("^([0-9a-fA-F]{64}) [ *].*$", "\\1", r2); r2_path <- sub("^[0-9a-fA-F]{64} [ *](\\./)?", "", r2)
code_problems <- character()
if (sha(opt[["r2-manifest"]]) != "85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7") code_problems <- c(code_problems, "r2 manifest hash is not 85a18248...a6b7")
for (j in seq_along(r2_path)) { f <- file.path(opt$code, r2_path[j]); if (!file.exists(f) || sha(f) != tolower(r2_hash[j])) code_problems <- c(code_problems, paste0("code differs from r2: ", r2_path[j])) }
present <- sort(sub(paste0("^", normalizePath(opt$code, winslash = "/", mustWork = TRUE), "/"), "",
  normalizePath(list.files(opt$code, recursive = TRUE, full.names = TRUE), winslash = "/")))
if (!identical(sort(r2_path), present)) code_problems <- c(code_problems, "code tree holds files not in r2 (or misses some)")
# the runner's fingerprint inputs: every .R file + R/SOURCES_SHA256.txt (run_bench_case.R lines 87-89)
fp_files <- sort(c(list.files(opt$code, pattern = "\\.R$", recursive = TRUE), "R/SOURCES_SHA256.txt"))
code_map <- setNames(vapply(file.path(opt$code, fp_files), sha, ""), fp_files)
# ---- registry and pins from the frozen config ----------------------------------------------------------------------------------------------------
cfg <- new.env(); sys.source(file.path(opt$code, "R", "config_lowp.R"), cfg)
registry <- function(mid) { m <- cfg$LOWP_PRODUCTION[[mid]]$METHODS; m[m$method_id == mid, , drop = FALSE] }
expected_rules <- function(mid) {   # I1: registry + lowp_derive's deterministic structure
  reg <- registry(mid); ids <- as.character(reg$rule_ids[[1]]); roles <- as.character(reg$roles[[1]])
  if (mid %in% c("F1","F2","F3","F4","F5")) {
    roles[ids %in% c("ebic1","ebic05","bic")] <- "secondary"
    if (mid %in% c("F4","F5")) {
      a <- intersect(c("ebic1","ebic05","bic"), ids)
      ids <- c(ids, paste0(a, "_K37"), if (mid == "F4") "ebic1_lam005" else "sic_smax")
      roles <- c(roles, ifelse(a == "ebic1", "primary", "S0"), "S0")
    }
  }
  paste(ids, roles, sep = "=")
}
EXP <- setNames(lapply(METHODS, expected_rules), METHODS)
pins_of <- function(mid) {
  if (mid == "A3") return(unlist(cfg$LOWP_PRODUCTION$A3$A3$PKG_VERSIONS))
  reg <- registry(mid); setNames(as.character(reg$pkg_version), as.character(reg$package))
}
adapt_of <- function(mid) if (mid == "F5") "LA-1;LA-2;LA-4" else if (mid %in% c("F1","F2","F3","F4")) "LA-1;LA-4" else if (mid == "A1") "LA-3" else "none"
# ---- authoritative identity: the sealed inputs manifest ---------------------------------------------------------------------------------------
man <- utils::read.csv(opt[["inputs-manifest"]], colClasses = "character")
man <- man[!duplicated(man$dataset_id), , drop = FALSE]; rownames(man) <- man$dataset_id
units <- utils::read.delim(opt$lists, colClasses = "character")
units <- units[units$piece == "bench", , drop = FALSE]
run_id <- basename(normalizePath(opt$results, winslash = "/", mustWork = TRUE))
out <- list()
add <- function(case, mid, verdict, why) out[[length(out) + 1L]] <<- data.frame(case = case, method = mid, verdict = verdict, reason = why, stringsAsFactors = FALSE)
if (length(code_problems)) add("ALL", "ALL", "FAIL", paste(head(code_problems, 5), collapse = "; "))
supp <- function(b) paste(which(b != 0), collapse = ";")
same <- function(a, b) identical(as.character(a), as.character(b)) || (length(a) == 1L && length(b) == 1L && is.na(a) && is.na(b))
nonmiss <- function(x) length(x) > 0 && !any(is.na(x)) && all(nzchar(as.character(x)))
for (j in seq_len(nrow(units))) {
  u <- units[j, ]; id <- u$dataset; p <- as.integer(substr(id, 2, 5)); dir <- file.path(opt$results, sprintf("p%04d", p), u$unit)
  s <- as.integer(sub("^p\\d{4}_S(\\d)_r\\d{3}$", "\\1", id)); r <- as.integer(sub("^p\\d{4}_S\\d_r(\\d{3})$", "\\1", id))
  data_seed <- (if (p == 20L) 1210000L else 1310000L) + 10000L * s + r; fold_seed <- (if (p == 20L) 3210000L else 3310000L) + 10000L * s + r
  m <- if (id %in% rownames(man)) man[id, ] else NULL
  for (mid in METHODS) {
    f <- file.path(dir, paste0(mid, ".rds"))
    if (!file.exists(f)) { add(u$unit, mid, "INCOMPLETE", "record missing"); next }
    rec <- tryCatch(readRDS(f), error = function(e) NULL)
    if (is.null(rec)) { add(u$unit, mid, "INCOMPLETE", "record unreadable"); next }
    why <- character(); rows <- rec$rows
    chk <- function(ok, msg) if (!isTRUE(ok)) why <<- c(why, msg)
    chk(identical(rec$schema_version, 2L), "schema_version != 2")
    chk(is.data.frame(rows) && nrow(rows) > 0, "rows missing")
    if (length(why)) { add(u$unit, mid, "FAIL", paste(why, collapse = "; ")); next }
    # ---- I1 ---------------------------------------------------------------------------------------------------------------------------------------
    chk(identical(paste(rows$rule_id, rows$role, sep = "="), EXP[[mid]]), "rule ids/roles differ from the frozen registry + lowp_derive structure")
    chk(all(rows$status %in% c("ok","warning","failed")), "invalid rule status")
    # N1 (Sol R2): every method's rows carry its selected model; validate it, never assume the columns exist
    has_sel <- all(c("support","k") %in% names(rows))
    chk(has_sel, "support/k columns missing")
    if (has_sel) {
      chk(all(rows$status != "failed" | (is.na(rows$support) & is.na(rows$k))), "failed rule with a selection")
      for (q in which(rows$status != "failed")) {
        sp <- as.character(rows$support[q]); kk <- suppressWarnings(as.numeric(rows$k[q]))
        idx <- if (!is.na(sp) && nzchar(sp)) suppressWarnings(as.integer(strsplit(sp, ";", fixed = TRUE)[[1]])) else integer()
        canon <- !is.na(sp) && (sp == "" || grepl("^[0-9]+(;[0-9]+)*$", sp)) && !anyNA(idx) && all(idx >= 1L & idx <= p) && !is.unsorted(idx, strictly = TRUE)
        chk(canon, paste0("selection is not a canonical sorted set of indices in 1..p: ", rows$rule_id[q]))
        chk(length(kk) == 1L && is.finite(kk) && kk == round(kk) && kk == length(idx), paste0("k is not the size of the selected support: ", rows$rule_id[q]))
      }
    }
    # ---- I3 ---------------------------------------------------------------------------------------------------------------------------------------
    need <- c("dataset_id","case_id","method_id","run_id","p","scenario","replicate","scale_key","scale","data_seed","fold_seed","method_seed",
              "inputs_sha256","x_sha256","y_sha256","fold_sha256","source_sha256","environment_sha256","adaptation_ids","test_library")
    miss <- setdiff(need, names(rows)); chk(!length(miss), paste0("missing row fields: ", paste(miss, collapse = ",")))
    if (!length(miss)) {
      chk(all(vapply(need, function(k) nonmiss(rows[[k]]), TRUE)), "a required row field is missing (NA/empty)")
      chk(all(rows$dataset_id == id) && all(rows$case_id == u$unit) && all(rows$method_id == mid) && all(rows$run_id == run_id), "dataset/case/method/run identity")
      chk(all(as.integer(rows$p) == p) && all(as.integer(rows$scenario) == s) && all(as.integer(rows$replicate) == r), "p/scenario/replicate differ from the dataset id")
      chk(all(rows$scale_key == u$scale) && all(as.numeric(rows$scale) == if (u$scale == "c100") 1 else 0.5), "scale_key/scale differ from the list")
      chk(all(as.numeric(rows$data_seed) == data_seed) && all(as.numeric(rows$fold_seed) == fold_seed) && all(as.numeric(rows$method_seed) == data_seed + 4e6),
        "seeds differ from the frozen CLI formulas")
      chk(all(rows$adaptation_ids == adapt_of(mid)), "adaptation_ids differ from the runner's assignment")
      if (is.null(m)) chk(FALSE, "dataset not in the sealed inputs manifest") else {
        chk(as.numeric(m$data_seed) == data_seed && as.numeric(m$fold_seed) == fold_seed && as.numeric(m$method_seed) == data_seed + 4e6 &&
            as.integer(m$p) == p && as.integer(m$scenario) == s && as.integer(m$replicate) == r, "sealed manifest identity differs from the derived identity")
        chk(all(rows$inputs_sha256 == m$file_sha256) && all(rows$x_sha256 == m$x_sha256) && all(rows$fold_sha256 == m$fold_sha256) &&
            all(rows$y_sha256 == m[[paste0("y_", u$scale, "_sha256")]]), "input/X/Y(scale)/fold hashes differ from the sealed manifest")
        hk <- c("file_sha256","x_sha256",paste0("y_", c("c100","c075","c050","c035","c025"), "_sha256"),"fold_sha256")
        h <- rec$input$hashes
        chk(!is.null(h) && all(hk %in% names(h)) && all(vapply(hk, function(k) identical(unname(as.character(h[[k]])), m[[k]]), TRUE)),
          "record$input$hashes differ from the sealed manifest")
      }
    }
    # ---- I2 ---------------------------------------------------------------------------------------------------------------------------------------
    ok_rule <- rows$status != "failed"
    if (mid %in% c("F1","F2","F3","F4","F5")) {
      co <- rec$coefficients
      chk(is.list(co) && identical(names(co), as.character(rows$rule_id)), "coefficients missing or not one per rule (D42.5)")
      chk(identical(co, rec$fit$coefficients), "coefficients differ from fit$coefficients")
      if (is.list(co) && identical(names(co), as.character(rows$rule_id))) for (q in seq_len(nrow(rows))) {
        z <- co[[q]]; rid <- rows$rule_id[q]
        chk(same(z$rule_id, rid) && same(z$status, rows$status[q]), paste0("coefficient entry identity: ", rid))
        if (has_sel) chk(same(z$support, rows$support[q]) && same(z$k, rows$k[q]), paste0("coefficient entry support/k differ from the row (N1): ", rid))
        chk(is.numeric(z$beta_pen) && length(z$beta_pen) == p && is.numeric(z$beta_ols) && length(z$beta_ols) == p, paste0("beta_pen/beta_ols not numeric of length p: ", rid))
        if (ok_rule[q] && is.numeric(z$beta_pen) && length(z$beta_pen) == p && is.numeric(z$beta_ols) && length(z$beta_ols) == p) {
          chk(all(is.finite(z$beta_pen)), paste0("beta_pen not finite: ", rid))
          chk(identical(supp(z$beta_pen), as.character(rows$support[q])), paste0("penalized support != row support: ", rid))
          if (mid %in% c("F1","F2","F3") && rid %in% c("cv_min","cv_1se")) chk(all(is.na(z$beta_ols)), paste0("beta_ols of a CV rule must be NA (SPEC): ", rid))
          else chk(all(is.finite(z$beta_ols)) && all(which(z$beta_ols != 0) %in% which(z$beta_pen != 0)), paste0("beta_ols missing/non-finite or outside the support: ", rid))
        }
      }
      for (rid in c("ebic1","ebic05","bic")) {   # N2 (Sol R2): lowp_derive aliases all three for F4/F5 (bic_K37 too)
        x <- rows[rows$rule_id == rid, , drop = FALSE]; y <- rows[rows$rule_id == paste0(rid, "_K37"), , drop = FALSE]
        if (nrow(x) || nrow(y)) chk(nrow(x) == 1L && nrow(y) == 1L && same(x$support, y$support) && same(x$k, y$k) &&
          (!("crit_value" %in% names(rows)) || same(x$crit_value, y$crit_value)), paste0(rid, " / ", rid, "_K37 pair differs"))
      }
    } else {
      # N1 (Sol R2): A1-A3 rows are the wrapper's rules unchanged by lowp_derive: support/k/status must equal fit$rules, and A2's selection is
      # which(beta != 0) by its frozen contract (fit_A2_ssl.R)
      fr <- rec$fit$rules
      chk(is.data.frame(fr) && identical(as.character(fr$rule_id), as.character(rows$rule_id)), "fit$rules missing or not the rows' rules")
      if (has_sel && is.data.frame(fr) && identical(as.character(fr$rule_id), as.character(rows$rule_id)))
        for (q in seq_len(nrow(rows))) chk(same(fr$support[q], rows$support[q]) && same(fr$k[q], rows$k[q]) && same(fr$status[q], rows$status[q]),
          paste0("row support/k/status differ from fit$rules: ", rows$rule_id[q]))
      if (mid == "A2" && has_sel) for (q in which(ok_rule)) if (is.numeric(rec$fit$beta) && length(rec$fit$beta) == p)
        chk(identical(supp(rec$fit$beta), as.character(rows$support[q])), paste0("A2 selection != which(beta != 0): ", rows$rule_id[q]))
    }
    if (!(mid %in% c("F1","F2","F3","F4","F5")) && any(ok_rule)) {
      b <- rec$fit$beta
      chk(is.numeric(b) && length(b) == p && all(is.finite(b)), "fit$beta missing, not length p or not finite")
      pip <- rec$fit$pip
      if (mid == "A1") chk(!is.null(pip), "A1 fit$pip missing (D42.5)")
      if (!is.null(pip)) chk(is.numeric(pip) && length(pip) == p && all(is.finite(pip)) && all(pip >= 0 & pip <= 1), "fit$pip not numeric length p in [0,1]")
    }
    # ---- I4 ---------------------------------------------------------------------------------------------------------------------------------------
    files <- rec$code$files; fp <- rec$code$source_sha256
    chk(!is.null(files) && length(files) > 0 && nonmiss(fp) && grepl("^[0-9a-f]{64}$", fp), "code fingerprint/files missing")
    if (!is.null(files) && length(files) && nonmiss(fp)) {
      chk(identical(digest::digest(paste(names(files), files, sep = "  ", collapse = "\n"), algo = "sha256", serialize = FALSE), fp),
        "source_sha256 is not the runner fingerprint of record$code$files")
      chk(identical(sort(names(files)), sort(names(code_map))) && identical(unname(files[sort(names(files))]), unname(code_map[sort(names(code_map))])),
        "record$code$files differ from the frozen r2 code")
      chk("source_sha256" %in% names(rows) && all(rows$source_sha256 == fp), "rows source_sha256 differ from the record fingerprint")
    }
    env <- rec$environment
    chk(nonmiss(env$identity) && "environment_sha256" %in% names(rows) && all(rows$environment_sha256 == env$identity), "environment identity missing or differs from the rows")
    if (!local) {
      chk(any(grepl("R version 4.5.2", env$sessionInfo, fixed = TRUE)), "R version is not 4.5.2")
      chk(identical(env$test_library, FALSE) && all(as.character(rows$test_library) == "FALSE"), "test_library is not FALSE")
      chk(identical(env$sealed_library, PINNED), "sealed_library is not the pinned library")
      prov <- env$package_provenance
      chk(is.list(prov) && length(prov) > 0, "package provenance missing or empty")
      if (is.list(prov) && length(prov)) {
        pins <- c(pins_of(mid), digest = NA)
        for (pkg in names(pins)) {
          chk(!is.null(prov[[pkg]]), paste0("pinned package missing from the provenance: ", pkg))
          if (!is.null(prov[[pkg]]) && !is.na(pins[[pkg]])) chk(identical(as.character(prov[[pkg]]$version), as.character(pins[[pkg]])),
            paste0("package version differs from the pin: ", pkg))
        }
        for (pkg in names(prov)) {
          d <- dirname(as.character(prov[[pkg]]$path))
          in_r <- basename(d) == "library" && basename(dirname(d)) == "R"
          chk(identical(d, PINNED) || (in_r && pkg %in% BASE_RECOMMENDED), paste0("package outside the pinned library (or a non-base package in R's library): ", pkg))
        }
      }
    }
    add(u$unit, mid, if (length(why)) "FAIL" else "PASS", paste(why, collapse = "; "))
  }
}
tab <- do.call(rbind, out)
utils::write.csv(tab, file.path(opt$out, "accept_bench.csv"), row.names = FALSE)
n <- table(factor(tab$verdict, levels = c("PASS","FAIL","INCOMPLETE")))
verdict <- if (n[["INCOMPLETE"]] > 0) "INCOMPLETE" else if (n[["FAIL"]] > 0) "FAIL" else "ACCEPTED"
md <- c(sprintf("# PROD-L benchmark acceptance: %s", verdict), "",
  sprintf("Records: %d expected (%d cases x 8 methods); PASS %d, FAIL %d, INCOMPLETE %d.", nrow(units) * 8L, nrow(units), n[["PASS"]], n[["FAIL"]], n[["INCOMPLETE"]]),
  sprintf("Code: supplied tree checked against the r2 manifest (%s); runner fingerprint files hashed locally.", if (length(code_problems)) "MISMATCH" else "match"),
  sprintf("Run id (results folder): %s. Identity checked against the sealed inputs manifest %s.", run_id, normalizePath(opt[["inputs-manifest"]], winslash = "/")),
  if (local) "LOCAL TEST: environment checks (R 4.5.2, test_library FALSE, pinned library, package versions and locations) were SKIPPED; rules, coefficients, identity and code anchoring were checked." else
    "Provenance: R 4.5.2, test_library FALSE, pinned library, pinned package versions, package locations (base/recommended only in R's library), code fingerprint anchored to r2.",
  "D42.5 coefficient evidence: F1-F5 per rule (penalized + OLS contract of the SPEC, support consistency, EBIC/K37 pairs); A1-A3 beta, A1 PIP.",
  "D54.3: the ABESS exact size check is deferred and NOT performed by this acceptance (disclosed).", "",
  "## Non-passing records", "", if (any(tab$verdict != "PASS")) paste0("- ", tab$case, " ", tab$method, ": ", tab$verdict, " (", tab$reason, ")")[tab$verdict != "PASS"] else "None.")
writeLines(md, file.path(opt$out, "ACCEPT_BENCH.md"))
cat(verdict, "\n")
quit(save = "no", status = switch(verdict, ACCEPTED = 0L, FAIL = 2L, INCOMPLETE = 3L))
