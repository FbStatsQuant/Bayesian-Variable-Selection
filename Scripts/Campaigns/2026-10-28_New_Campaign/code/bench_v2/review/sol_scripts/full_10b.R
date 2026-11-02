V <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
code_dir <- file.path(V,'F1_Lasso')
inputs_root <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs'
cfg <- new.env();sys.source(file.path(code_dir,'config.R'),cfg)
settings <- as.list(cfg);settings$variant <- 'primary'
base500 <- readRDS(file.path(V,'repro/controlled_2a8362b2f348/dev_p0500_S4_r001_c100.rds'))$F1$new$result
local_test <- TRUE
Sys.setenv(BENCH_V2_LOCAL_TEST='1',BENCH_LIB='C:/Users/felip/AppData/Local/R/win-library/4.4')
record <- function(name,expr) {cat('START',name,format(Sys.time(),tz='UTC'),'\n');force(expr);cat('PASS FULL 10b',format(Sys.time(),tz='UTC'),'\n')}
eval(parse(text=readLines(file.path(code_dir,'tests/test_F1_lasso.R'),warn=FALSE)[351:391]))
