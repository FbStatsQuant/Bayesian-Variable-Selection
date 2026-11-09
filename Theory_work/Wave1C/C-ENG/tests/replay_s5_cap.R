# replay_s5_cap.R -- the binding replay design (dev S5 r002, p = 500): LS0 from the start mode with the final core,
# cap ell_n (as in the replay fits, which predate C-GROW) vs ell_n + |S~0| (default), standalone (own ledger, no cache; the
# path equals the integrated one, test_ls0 F1). Compares LS0's best scored model with the replay fit's reported HPM.
# Usage: Rscript replay_s5_cap.R <core_dir> <work_dir> <replay_fit_rds> <out_txt>
args <- commandArgs(TRUE); core <- args[1]; work <- args[2]; fitf <- args[3]; out <- args[4]
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R")); ceng_load(core, work, exports = TRUE)
genv <- new.env(); sys.source(file.path(here, "..", "..", "..", "..", "Scripts", "SMC_BVS", "smoke", "reference", "gen_dev_data.R"), envir = genv)
d <- genv$generate_dev_dataset(500L, 5L, 2L)$inputs; y <- unname(d$Y[, "c100"])
pre <- v3_preprocess(d$X, y, dup_components = FALSE)
st <- v3_setup(v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE))
F <- readRDS(fitf)$fit
sm <- .v3cpp$t_setup_start_mode(st$ptr, 1e6, TRUE)
ell <- st$budgets$ell
a <- .v3cpp$t_local_search(st$ptr, sm$model, ell, TRUE, TRUE)
b <- .v3cpp$t_local_search(st$ptr, sm$model, ell + length(sm$model), TRUE, TRUE)
sink(out, split = TRUE)
cat("dev_p0500_S5_r002: start mode {", sm$model, "} (fit:", F$start_mode$model, "), ell_n =", ell, "\n")
cat("cap ell_n          :", a$termination, "moves", a$moves, "n_eval", a$n_evaluated, "best F", format(a$ledger$hpm$F, digits = 15),
    "; same path as the replay fit's LS0:", identical(a$path, F$ls0$path), "\n")
cat("cap ell_n + |S~0|  :", b$termination, "moves", b$moves, "n_eval", b$n_evaluated, "best F", format(b$ledger$hpm$F, digits = 15),
    "; best {", b$ledger$hpm$model, "}\n")
cat("replay fit HPM F   :", format(F$hpm_F, digits = 15), "{", F$hpm, "}\n")
cat("with the C-GROW cap, LS0's best beats the fit's HPM:", b$ledger$hpm$F > F$hpm_F,
    "; equals it:", identical(b$ledger$hpm$F, F$hpm_F) && identical(b$ledger$hpm$model, F$hpm), "\n")
sink()
