# test_derive.R: unit tests of derive_rules.R on hand-made fixtures (thread S, 2026-10-21).
# Usage: Rscript --vanilla test_derive.R   (from this folder, or with an absolute path)

here <- local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
})
source(file.path(here, "derive_rules.R"))

n_pass <- 0; n_fail <- 0
check <- function(cond, label) {
  if (isTRUE(cond)) n_pass <<- n_pass + 1 else { n_fail <<- n_fail + 1; cat("FAIL:", label, "\n") }
}

p <- 500L
key_of <- function(k, off = 0L) if (k == 0) "" else paste(seq_len(k) + off, collapse = ";")
# Candidate table with stored EBIC columns computed from RSS (as the methods save it).
make_cand <- function(ks, rss, keys = vapply(seq_along(ks), function(i) key_of(ks[i]), "")) {
  cand <- data.frame(key = keys, k = as.integer(ks), rank = as.integer(ks), rss = rss, valid = TRUE, stringsAsFactors = FALSE)
  for (g in names(GAMMA)) cand[[g]] <- ebic_from_rss(cand, p, GAMMA[[g]])
  cand
}

# 1. K cap: EBIC(1) keeps decreasing to k = 100; the K37 pick is the best among k <= 37.
ks <- c(0, 14, 30, 37, 38, 100)
rss <- c(5000, 200, 150, 140, 1e-3, 1e-9)
cand <- make_cand(ks, rss)
tb <- list(cand = cand, occ = data.frame(key = cand$key, ok = TRUE, lambda = rev(seq_along(ks)), stringsAsFactors = FALSE),
           k_path_max = 100L, zmax = 6)
d <- derive_case(tb, "F4", p)
best37 <- which.min(cand$ebic1[cand$k <= 37])
check(d$rules$ebic1_K37$k == cand$k[cand$k <= 37][best37], "K37 pick is the minimiser among k <= 37")
check(d$rules$ebic1_K37$k <= 37 && d$rules$ebic1_K37$k_valid_max == 37, "K37 respects the cap; k_valid_max = 37")
check(pick_rule(cand, cand$ebic1, cand$k <= 100, tb$occ)$k == 100, "cap 100 picks k = 100 on the same table")

# 2. Ties: equal criterion -> smaller k; equal k -> key in C byte order.
cand2 <- data.frame(key = c("", "5", "10", "2;3"), k = c(0L, 1L, 1L, 2L), rank = c(0L, 1L, 1L, 2L),
                    rss = 1, valid = TRUE, stringsAsFactors = FALSE)
crit <- c(10, 5, 5, 5)
check(pick_rule(cand2, crit, rep(TRUE, 4), NULL)$key == "10", "tie: smaller k, then radix key ('10' < '5')")

# 3. Occurrence check: pick fails when no occurrence passes; support_audit keeps it; null always valid.
occ3 <- data.frame(key = c("", "1;2"), ok = c(TRUE, FALSE), lambda = c(2, 1), stringsAsFactors = FALSE)
cand3 <- make_cand(c(0, 2), c(5000, 10), keys = c("", "1;2"))
pk <- pick_rule(cand3, cand3$ebic1, c(TRUE, TRUE), occ3)
check(pk$status == "failed" && is.na(pk$key) && pk$audit == "1;2", "failed pick keeps support_audit")
occ3$ok <- c(FALSE, FALSE)
pk0 <- pick_rule(cand3, c(1, 2), c(TRUE, TRUE), occ3)
check(pk0$status == "ok" && pk0$key == "", "null support always valid")

# 4. lam005: only supports at path points with lambda >= 0.05 * zmax.
occ4 <- data.frame(key = c("", key_of(14), key_of(37), key_of(38)), ok = TRUE, lambda = c(6, 1, 0.31, 0.29),
                   stringsAsFactors = FALSE)
cand4 <- make_cand(c(0, 14, 37, 38), c(5000, 200, 1e-3, 1e-6))
tb4 <- list(cand = cand4, occ = occ4, k_path_max = 38L, zmax = 6)       # 0.05 * 6 = 0.3
d4 <- derive_case(tb4, "F4", p)
check(d4$rules$ebic1_lam005$k == 37, "lam005 excludes the point below 0.05 zmax")
occ4$ok[3] <- FALSE; occ4$key[4] <- key_of(37)                          # k=37 passes only outside the segment
d4b <- derive_case(list(cand = cand4, occ = occ4, k_path_max = 38L, zmax = 6), "F4", p)
check(d4b$rules$ebic1_lam005$status == "failed", "lam005 occurrence must pass inside the segment")

# 5. SIC smax: 19 at p = 500, 17 at p = 1000; sizes above smax excluded.
check(SIC_SMAX(500) == 19 && SIC_SMAX(1000) == 17 && K_CAP == 37, "smax and K values")
cand5 <- make_cand(0:25, c(5000, exp(seq(log(4000), log(1), length.out = 25))))
d5 <- derive_case(list(cand = cand5, occ = NULL, k_path_max = 25L, zmax = NA), "F5", p)
sic <- 200 * log(cand5$rss / 200) + cand5$k * log(p) * log(log(200))
check(d5$rules$sic_smax$k == cand5$k[cand5$k <= 19][which.min(sic[cand5$k <= 19])] && d5$rules$sic_smax$k <= 19, "SIC over sizes 0..19")

# 6. Rows: provenance copied from the ebic1 row, rule fields replaced, k_gt_K, derived_from, roles.
base <- data.frame(study = "bench20261019", run_id = "R", case_id = "p0500_S1_r001_c050", method_id = "F4",
                   rule_id = "ebic1", role = "primary", status = "ok", n_warnings = "0", diag_codes = "ebic_at_largest",
                   support = key_of(100), support_audit = NA, k = "100", error = NA, lambda = "0.1", rss = "1",
                   crit_value = "1", k_valid_max = "100", k_path_max = "100", path_index = "200", x_sha256 = "xh",
                   stringsAsFactors = FALSE)
rows <- make_rows(base, "F4", d$rules, "rdshash", "scripthash", "2026-10-21T00:00:00Z", 100L)
check(nrow(rows) == 4 && identical(rows$rule_id, DERIVED$F4$rules), "four F4 derived rows")
check(rows$role[1] == "primary" && all(rows$role[-1] == "S0"), "F4 ebic1_K37 primary, others S0")
check(all(rows$x_sha256 == "xh") && all(rows$derived_from == "rdshash"), "provenance copied; derived_from set")
check(all(rows$diag_codes == "") && all(is.na(rows$path_index)), "rule-only codes and columns not copied")
check(identical(rows$k_gt_K[1], FALSE), "k_gt_K FALSE for the capped rule")
fr <- failed_rows(base, "F5", "h", "s", "u", "fit failed")
check(all(fr$status == "failed") && all(is.na(fr$support)) && all(fr$role == DERIVED$F5$roles), "failed fit gives failed rows")

# 7. Self-check: cap-100 re-derivation equals the method's own rows on a consistent fixture.
own <- data.frame(rule_id = c("ebic1", "ebic05", "bic"), status = "ok", support = NA, support_audit = NA,
                  crit_value = NA, stringsAsFactors = FALSE)
for (g in own$rule_id) {
  pk <- pick_rule(cand, cand[[g]], cand$k <= 100, tb$occ)
  own$support[own$rule_id == g] <- pk$key; own$crit_value[own$rule_id == g] <- pk$crit
}
sc <- selfcheck_case(tb, own, "F4", p)
check(all(sc$same_support) && all(sc$same_status) && max(sc$crit_absdiff) == 0, "selfcheck agrees on a consistent fixture")
own$support[1] <- key_of(14)
check(!selfcheck_case(tb, own, "F4", p)$same_support[1], "selfcheck detects a different support")

# 8. Run-id forms map to the same method folder.
for (rid in c("20261019T2219Z_bench20261019_prod_F4_MCP_SCAD", "20261022T0100Z_bench20261019_prodc050_F4_MCP_SCAD"))
  check(identical(RUN_DERIVED[[sub("^.*_prod(c[0-9]{3})?_", "", rid)]], c("F4", "F4_SCAD")), paste("run id form", rid))

cat(sprintf("\ntest_derive: %d passed, %d failed\n", n_pass, n_fail))
if (n_fail > 0) quit(status = 1)
