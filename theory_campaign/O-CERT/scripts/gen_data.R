# O-CERT: regenerate selected production study datasets (p = 500) with the study generator, bit-identical seeds.
# Usage: Rscript gen_data.R <repo_root> <study_root> <dataset_id> [...]
a <- commandArgs(TRUE); repo <- a[1]; root <- a[2]; ids <- a[-(1:2)]
g <- new.env(); gen <- file.path(repo, "Scripts", "Data_generators")
src <- readLines(file.path(gen, "gen_prod_data.R"))
src <- src[seq_len(grep("^main <- function", src) - 1)]          # definitions only, no main()
src <- sub("file.path(here(), ", "file.path(gen, ", src, fixed = TRUE)
assign("gen", gen, envir = g); eval(parse(text = src), envir = g)
for (id in ids) {
  m <- regmatches(id, regexec("^p([0-9]{4})_S([0-9])_r([0-9]{3})$", id))[[1]]
  d <- g$generate_prod_dataset(as.integer(m[2]), as.integer(m[3]), as.integer(m[4]))
  for (k in c("inputs", "truth")) {
    dir <- file.path(root, k, sprintf("p%04d", as.integer(m[2]))); dir.create(dir, recursive = TRUE, showWarnings = FALSE)
    saveRDS(d[[k]], file.path(dir, paste0(id, ".rds")))
  }
  cat(id, "active:", d$truth$active, "\n")
}
