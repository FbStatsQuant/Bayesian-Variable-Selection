# check_generators.R -- Monte Carlo cross-check of generate.R against the paper formulas; writes specs/generator_check.md.
#   Rscript harness/check_generators.R [--reps 200]
# Per setting, over reps 1..R (the production data seeds for reps <= 100; 101..200 extend the same formula):
#   S2: mean sample SNR  Var_n(X beta)/sigma^2  vs target nu (E Var_n(X beta) = beta' Sigma beta exactly);
#   S1: ||beta||_2 vs SNR sqrt(log p / n) sqrt(65) (deterministic), sigma^2 vs 1, mean sample SNR vs beta' Sigma beta;
#   both: mean Var_n(eps) vs sigma^2; Sigma: mean column variance vs 1 and mean empirical correlation at lags 1, 2, 5
#   (adjacent pairs among columns 1..200) vs E r = rho^k - rho^k (1 - rho^2k)/(2n); support positions vs the papers' rule.
# Verdict per check: PASS if |mean - target| <= 4 * MC SE (SE = sd over reps / sqrt(R)); deterministic checks exact (1e-12).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "generate.R"))
a <- commandArgs(TRUE); R <- if (length(a) >= 2) as.integer(a[2]) else 200L
tab <- read_settings(file.path(BASE, "specs", "settings.tsv"))
ids <- c("S1_03", "S1_15", "S2_001", "S2_016", "S2_076", "S2_120", "S2_046")
res <- list(); add <- function(...) res[[length(res) + 1]] <<- data.frame(...)
for (id in ids) {
  row <- tab[tab$setting_id == id, ]; rho <- row$rho; p <- row$p; n <- row$n
  m <- matrix(NA_real_, R, 7, dimnames = list(NULL, c("nu_s", "veps", "cvar", "c1", "c2", "c5", "sigma2")))
  for (r in seq_len(R)) {
    d <- gen_data(row, r)
    mu <- drop(d$X %*% d$beta); eps <- d$y - mu; q <- min(p, 200)
    C <- cor(d$X[, 1:q])
    lag <- function(k) mean(C[cbind(1:(q - k), (1 + k):q)])
    m[r, ] <- c(var(mu) / d$sigma2, var(eps), mean(apply(d$X[, 1:q], 2, var)), lag(1), lag(2), lag(5), d$sigma2)
  }
  vmu <- quad_ar1(d$beta, rho)
  chk <- function(what, est, se, target) add(setting = id, label = row$label, check = what, estimate = signif(est, 5),
    mc_se = signif(se, 3), target = signif(target, 5), z = round((est - target) / se, 2), verdict = ifelse(abs(est - target) <= 4 * se, "PASS", "FAIL"))
  ex <- function(what, est, target) add(setting = id, label = row$label, check = what, estimate = signif(est, 6), mc_se = 0,
    target = signif(target, 6), z = NA, verdict = ifelse(isTRUE(all.equal(est, target, tolerance = 1e-12)), "PASS", "FAIL"))
  mse <- function(k) c(mean(m[, k]), sd(m[, k]) / sqrt(R))
  if (row$suite == 2) {
    v <- mse("nu_s"); chk("sample SNR Var(Xb)/s2 vs nu", v[1], v[2], row$nu)
    ex("sigma2 vs b'Sigma b/nu", d$sigma2, vmu / row$nu)
    exp_supp <- if (row$beta_type == "1") round(seq(1, p, length = row$s0)) else seq_len(row$s0)
    add(setting = id, label = row$label, check = paste0("support = ", paste(d$support, collapse = ",")), estimate = NA, mc_se = 0,
        target = NA, z = NA, verdict = ifelse(identical(as.numeric(d$support), as.numeric(exp_supp)), "PASS", "FAIL"))
  } else {
    ex("||beta||_2 vs SNR sqrt(log p/n) sqrt(65)", sqrt(sum(d$beta^2)), row$snr * sqrt(log(p) / n) * sqrt(65))
    ex("sigma2 vs 1", d$sigma2, 1)
    v <- mse("nu_s"); chk("sample SNR Var(Xb)/s2 vs b'Sigma b", v[1], v[2], vmu)
    add(setting = id, label = row$label, check = paste0("support = ", paste(d$support, collapse = ",")), estimate = NA, mc_se = 0,
        target = NA, z = NA, verdict = ifelse(identical(d$support, 1:10), "PASS", "FAIL"))
  }
  v <- mse("veps"); chk("Var(eps) vs sigma2", v[1], v[2], d$sigma2)
  v <- mse("cvar"); chk("column variance vs 1", v[1], v[2], 1)
  for (k in c(1, 2, 5)) { v <- mse(paste0("c", k)); rk <- rho^k
    chk(sprintf("corr lag %d vs E r(rho^%d)", k, k), v[1], v[2], rk - rk * (1 - rk^2) / (2 * n)) }
  cat(id, "done\n")
}
out <- do.call(rbind, res)
md <- c("# Generator check (harness/check_generators.R)", "",
        sprintf("Generated %s on %s, R = %d reps per setting (data seeds of INTERFACE.md, reps 1..%d). PASS: |mean - target| <= 4 MC SE; deterministic rows exact to 1e-12.", 
                format(Sys.time(), "%Y-%m-%d %H:%M %Z"), Sys.info()[["nodename"]], R, R),
        "Correlation targets are E r for population correlation r_k = rho^k, to O(1/n): r_k - r_k (1 - r_k^2) / (2n) (the sample correlation is biased toward 0; at n = 50, rho = 0.35 the bias is 0.003, several MC SE).", "",
        sprintf("**Overall verdict: %s** (%d checks, %d FAIL)", ifelse(all(out$verdict == "PASS"), "PASS", "SEE FAILS"), nrow(out), sum(out$verdict != "PASS")), "",
        "| setting | label | check | estimate | MC SE | target | z | verdict |", "|---|---|---|---|---|---|---|---|",
        apply(out, 1, function(r) paste0("| ", paste(trimws(r), collapse = " | "), " |")))
writeLines(md, file.path(BASE, "specs", "generator_check.md"))
cat(sprintf("verdict: %d checks, %d FAIL\n", nrow(out), sum(out$verdict != "PASS")))
