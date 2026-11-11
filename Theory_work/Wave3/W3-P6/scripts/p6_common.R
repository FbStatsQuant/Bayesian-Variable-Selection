# W3-P6 shared helpers (sourced by p6_fit.R and rederive.R). No production code is modified.
p6_key <- function(S) paste(sort(as.integer(S)), collapse = ",")

# Truth indices (v2, R01-8): even step so that consecutive truths alternate parity for every p (fac2 sign classes);
# identical to v1 whenever floor(p/s0) is even (all b1 fac2 cells). step >= 6 keeps s5 truths in distinct groups of 5.
p6_truth <- function(p, s0) {
  step <- p %/% s0; if (step %% 2L == 1L) step <- step - 1L
  S0 <- as.integer((seq_len(s0) - 1L) * step + 3L + ((seq_len(s0) - 1L) %% 2L))
  stopifnot(step >= 2L, max(S0) <= p, !anyDuplicated(S0))
  if (s0 >= 2) stopifnot(all(diff(S0 %% 2L) != 0))   # alternating parity
  S0
}

# Production HPM order (cpp/v3_util.h hpm_better): larger F; on exact F ties smaller size, then lexicographic.
p6_hpm_better <- function(F1, S1, F2, S2) {
  if (F1 != F2) return(F1 > F2)
  if (length(S1) != length(S2)) return(length(S1) < length(S2))
  a <- sort(as.integer(S1)); b <- sort(as.integer(S2))
  i <- which(a != b); if (!length(i)) return(FALSE)
  a[i[1]] < b[i[1]]
}

# Prefix derivation of LS0 with cap a from a wide run (cap >= a). Inputs: ls0 archive (path, path_F, returned, returned_F,
# scanned_F, local_limit), hb = hpm_before_ls0 (model, F), first_scoring (1-based scan index whose centre has S0 in
# N(C) U {C}), S0 key. LS0(a) scans centres C_0..C_min(a, m) (v3_engine.h:385-415: at a scan with moves == a and an
# improving neighbour it returns that neighbour without moving). The best model LS0(a) scores is path entry a+1 (if the
# wide run moved at least a+1 times) else the wide run's endpoint. Returns NA outcomes (never guesses) when
#  * censored: cap a needs scans beyond those the wide run performed and the wide run itself stopped on its cap;
#  * exact F tie between distinct candidate models (production HPM order would decide; equal-F neighbours that the
#    archive does not record cannot be excluded — generic uniqueness assumed and checked by the paired validation).
p6_derive <- function(a, ls0, hb, first_scoring, s0k) {
  na <- list(cap = a, scores = NA, model = NULL, F = NA_real_, hpm_eq_S0 = NA, status = "unavailable")
  if (is.null(ls0) || is.null(ls0$scanned_F) || is.null(hb) || is.null(hb$model)) return(na)
  nsc <- length(ls0$scanned_F); m <- length(ls0$path)
  if ((a + 1) > nsc && isTRUE(ls0$local_limit)) { na$status <- "censored"; return(na) }
  scores <- !is.na(first_scoring) && first_scoring <= a + 1
  if (a + 1 <= m) { bm <- ls0$path[[a + 1]]; bF <- ls0$path_F[a + 1] } else { bm <- ls0$returned; bF <- ls0$returned_F }
  hm <- hb$model; hF <- hb$F
  same <- p6_key(bm) == p6_key(hm)
  if (!same && bF == hF) return(list(cap = a, scores = scores, model = NULL, F = bF, hpm_eq_S0 = NA, status = "tie"))
  win <- if (same || bF > hF) bm else hm; wF <- if (same || bF > hF) bF else hF
  list(cap = a, scores = scores, model = sort(as.integer(win)), F = wF, hpm_eq_S0 = p6_key(win) == s0k, status = "ok")
}

# Outcome class of a reported/derived HPM relative to S0 (F_S0 by direct scoring with the core scorer).
#  "S0" | "posterior" (F(model) > F(S0): S0 would not be reported even if scored) |
#  "search" (F(S0) > F(model): S0 was never scored in that run, since the HPM is the best scored model) | NA
p6_class <- function(eq, Fm, FS0, tol = 1e-8) {
  if (is.na(eq) || is.na(Fm) || is.na(FS0)) return(NA_character_)
  if (isTRUE(eq)) return("S0")
  if (Fm > FS0 + tol) return("posterior")
  if (FS0 > Fm + tol) return("search")
  "tie"
}
