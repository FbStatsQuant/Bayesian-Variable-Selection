# common_gen.R -- load the frozen PROD-H generator (gen_dev_data.R + gen_prod_data.R, copied unchanged into the bundle's gen/).
# Same loading trick as list_pip_ab/ws_common.R::ws_prodh (gen_prod_data.R finds gen_dev_data.R through --file=, which would
# point at the calling script, so the directory is given explicitly). Returns an environment with generate_prod_dataset(),
# f64_sha256() and the constants. Nothing is changed in the generator.
load_prod_generator <- function(gen_dir) {
  env <- new.env()
  dev <- new.env(); sys.source(file.path(gen_dir, "gen_dev_data.R"), envir = dev)
  src <- readLines(file.path(gen_dir, "gen_prod_data.R"))
  src <- src[!grepl("^sys\\.source\\(file\\.path\\(here\\(\\)", src)]
  env$gen_dev_env <- dev
  eval(parse(text = sub("^gen_dev_env <- new\\.env\\(\\)$", "", src)), envir = env)
  env
}
parse_case <- function(case) {
  m <- regmatches(case, regexec("^p(0500|1000)_S([1-6])_r([0-9]{3})$", case))[[1]]
  if (length(m) != 4L) stop("bad dataset id: ", case)
  list(p = as.integer(m[2]), s = as.integer(m[3]), r = as.integer(m[4]), dataset_id = case)
}
