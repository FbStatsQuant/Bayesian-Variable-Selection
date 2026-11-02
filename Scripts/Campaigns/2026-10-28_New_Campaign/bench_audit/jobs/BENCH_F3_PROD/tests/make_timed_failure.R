args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==2L)
campaign <- normalizePath(args[1],mustWork=TRUE)
out <- normalizePath(args[2],mustWork=TRUE)
wrapper <- file.path(campaign,"code/bench_v2/tests/run_local_runner.R")
expr <- parse(wrapper); scope <- new.env(parent=globalenv())
for(statement in head(expr,-2L)) eval(statement,scope)
rc <- scope$e
original_load <- rc$load_code
# Test-only scheduling delay inside the timed call, before the unchanged
# frozen assert_inputs. Windows' elapsed clock rounded the genuine failure to 0.
rc$load_code <- function(path) {
  result <- original_load(path)
  original_assert <- result$engine$assert_inputs
  result$engine$assert_inputs <- function(...) { Sys.sleep(0.05); original_assert(...) }
  result
}
id <- "fixture_p0005_S3_r001"
prefix <- file.path(out,"results","branch_failure","p0005",paste0(id,"_c100"),"F3")
if(file.exists(paste0(prefix,".done"))) stop("timed failure already exists")
status <- rc$main(c("--input",file.path(out,"inputs","p0005",paste0(id,".rds")),
                    "--out",out,"--run-id","branch_failure","--scale","c100",
                    "--methods","F3","--manifest",file.path(out,"inputs_manifest.csv")))
stopifnot(status==0L)
x <- readRDS(paste0(prefix,".rds"))
stopifnot(all(x$rows$status=="failed"), all(is.na(x$fit$beta)), x$fit$runtime_s>0)
cat("TIMED_FAILURE_PASS",prefix,"runtime_s",x$fit$runtime_s,"\n")
