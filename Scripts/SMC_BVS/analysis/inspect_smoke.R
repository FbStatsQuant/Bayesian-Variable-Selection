# Read-only schema inspection; never fits or reads truth.
a <- commandArgs(TRUE)
for(p in c(500,1000)) {
  path <- file.path(a[1],paste0("dev",p),"output","results",sprintf("dev_smoke_p%04d_c100",p),
    sprintf("p%04d",p),sprintf("dev_p%04d_S1_r001_c100",p),"SMCBVS.rds")
  r <- readRDS(path); f <- r$fit
  cat("\nP",p,"RECORD\n"); print(names(r));cat("FIT\n");print(names(f))
  for(nm in names(f)) cat(nm,":",paste(class(f[[nm]]),collapse="/"),"length",length(f[[nm]]),
    "dim",paste(dim(f[[nm]]),collapse="x"),"\n")
  cat("KEYS\n");str(f[intersect(names(f),c("status","branch_run","estimates_available","p","n","hpm","mpm","preprocessing",
    "log_Z","log_Z_rel_m0","log_Z_lower95","logZ_islands","log_Z_islands","flags","timings","islands","exact"))],max.level=2)
  cat("ROW FLAGS\n");print(r$rows[,c("v3_status","v3_flags_json","adapter_mapping_status","role","status","diag_flag","fold_seed","fold_sha256")])
}
