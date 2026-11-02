# Checker: cheap structural checks over all 24 saved controlled cases (own code, no refit).
CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
D <- file.path(CAMP, "code/bench_v2/repro/controlled_2a8362b2f348")
OUT <- file.path(CAMP, "code/bench_v2/review/checker")
files <- sort(list.files(D, pattern = "^dev_p[0-9]+_S[0-9]_r001_c[0-9]+\\.rds$"))
key_of <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
rows <- list()
for (f in files) {
  r <- readRDS(file.path(D, f)); F1 <- r$F1$new$result; F1o <- r$F1$old$result; F2 <- r$F2$new$result; F2o <- r$F2$old$result; F3 <- r$F3$result
  p <- length(F1$beta); n <- 200L
  prov <- function(o) all(vapply(seq_len(nrow(o$rules)), function(i) { rw <- o$rules[i, ]; z <- o$coefficients[[rw$rule_id]]
    identical(key_of(which(z$beta_pen != 0)), if (rw$status == "failed") rw$support_audit else rw$support) }, TRUE))
  four <- c("cv_min", "cv_1se", "ebic1", "ebic05")
  same4 <- function(new, old) { a <- new$rules[match(four, new$rules$rule_id), ]; b <- old$rules; rownames(a) <- NULL; rownames(b) <- NULL
    identical(as.list(a), as.list(b)) && identical(new$beta, old$beta) && identical(new$diagnostics, old$diagnostics) && identical(new$converged, old$converged) }
  cand <- F3$diagnostics$candidates; path <- F3$diagnostics$path
  rp <- function(col, cap) { el <- cand[cand$k <= cap, ]; el$key[order(el[[col]], el$k, el$key, method = "radix")[1]] }
  picks <- c(ebic1 = rp("ebic1", 100), ebic05 = rp("ebic05", 100), ebic1_K37 = rp("ebic1", 37), ebic05_K37 = rp("ebic05", 37))
  repick <- all(vapply(names(picks), function(id) identical(F3$rules$support[F3$rules$rule_id == id], picks[[id]]), TRUE))
  rows[[f]] <- data.frame(case = sub("\\.rds$", "", f), pilot_identical = identical(F3$diagnostics$pilot$beta, F1$beta),
    prov_F1 = prov(F1), prov_F2 = prov(F2), prov_F3 = prov(F3), same4_F1 = same4(F1, F1o), same4_F2 = same4(F2, F2o),
    f3_all_ok = all(F3$rules$status == "ok"), f1_all_ok = all(F1$rules$status == "ok"), f2_all_ok = all(F2$rules$status == "ok"),
    repick_saved_cand = repick, m = F3$rules$pilot_k[1], kmin = F3$rules$k[1], cv_min_idx = F3$rules$index[1], cv_min_last = F3$rules$index[1] == 200L,
    cv_1se_idx = F3$rules$index[2], n_cap_eq_k37_ebic1 = identical(F3$rules$support[3], F3$rules$support[5]), k37_ebic1 = F3$rules$k[5], k_ebic1 = F3$rules$k[3],
    vmax_k37 = F3$rules$k_valid_max[5], sum_v_ok = abs(sum(F3$diagnostics$v) - length(F3$diagnostics$v)) <= 1e-10 * length(F3$diagnostics$v),
    stringsAsFactors = FALSE)
  rm(r); gc(verbose = FALSE)
}
tab <- do.call(rbind, rows); rownames(tab) <- NULL
write.csv(tab, file.path(OUT, "check3b_all24.csv"), row.names = FALSE)
print(tab[, c("case", "pilot_identical", "prov_F1", "prov_F2", "prov_F3", "same4_F1", "same4_F2", "f3_all_ok", "repick_saved_cand", "m", "cv_min_idx", "cv_min_last", "k_ebic1", "k37_ebic1")], row.names = FALSE)
cat("\nn cases:", nrow(tab), "\n")
for (cn in c("pilot_identical", "prov_F1", "prov_F2", "prov_F3", "same4_F1", "same4_F2", "f3_all_ok", "f1_all_ok", "f2_all_ok", "repick_saved_cand", "sum_v_ok"))
  cat(sprintf("%-18s %d/%d TRUE\n", cn, sum(tab[[cn]]), nrow(tab)))
cat("cv_min at last lambda (index 200):", sum(tab$cv_min_last), "/", nrow(tab), "\n")
cat("m (pilot k) range:", range(tab$m), " ebic1 cap k range:", range(tab$k_ebic1), " K37 ebic1 k range:", range(tab$k37_ebic1), "\n")
cat("ebic1 cap support == ebic1_K37 support:", sum(tab$n_cap_eq_k37_ebic1), "/", nrow(tab), "\n")
