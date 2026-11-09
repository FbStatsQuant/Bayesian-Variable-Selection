a <- commandArgs(TRUE); core <- a[1]; testdir <- a[2]
source(file.path(testdir, "common.R"))
load_test_core(core, tempfile("w"), testdir)
src <- readLines(file.path(testdir, "v2_runtime_units.R"))
i0 <- which(startsWith(src, 'add("v2_inherited_rescore_failure')); i1 <- which(startsWith(src, 'add("v2_V_rescore_failure'))[1] - 1
add <- function(label, expr) withCallingHandlers(expr, error = function(e) {
  cat("ERR:", conditionMessage(e), "\n"); calls <- sys.calls()
  for (cl in tail(calls, 8)) cat("  >", substr(paste(deparse(cl), collapse=" "), 1, 200), "\n") })
eval(parse(text = src[1:(which(startsWith(src, 'add('))[1]-1)]))

body <- src[i0:i1]
body <- sub("exact(z$ledger$logical, injected$ledger_before$logical)", "{ cat('logical z dim/rn:', dim(z$ledger$logical), rownames(z$ledger$logical), '| before:', dim(injected$ledger_before$logical), rownames(injected$ledger_before$logical), '\n'); lz <- z$ledger$logical; lz <- lz[rownames(lz) != 'ls0', , drop=FALSE]; exact(lz, injected$ledger_before$logical) }", body, fixed=TRUE)
body <- sub("exact(z$ledger$fresh, injected$ledger_before$fresh)", "{ cat('fresh rn:', rownames(z$ledger$fresh), '| before:', rownames(injected$ledger_before$fresh), '\n'); lz <- z$ledger$fresh; lz <- lz[rownames(lz) != 'ls0', , drop=FALSE]; exact(lz, injected$ledger_before$fresh) }", body, fixed=TRUE)
body <- sub('need(is.null(a$pip_primary) && is.null(a$log_Z), "failed inheritance exposed estimates")', '{ cat("pip_primary:", format(a$pip_primary), "| log_Z:", format(a$log_Z), "| estimates_available:", a$estimates_available, "\n"); need(all(is.na(a$pip_primary)) && all(is.na(a$log_Z)), "estimates not all NA") }', body, fixed=TRUE)
r <- eval(parse(text = body)); cat('REST OF UNIT PASSED
')
