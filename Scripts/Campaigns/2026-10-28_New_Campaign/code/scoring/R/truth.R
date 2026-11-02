# truth.R -- THE ONLY truth reader. Scoring calls read_truth() after the fits are frozen.
# truth/p{pppp}/{dataset_id}.rds : list(active, beta, signal, eps, scenario)   (INTERFACES I1)
read_truth <- function(study, dataset_id) {
  p <- as.integer(substr(dataset_id, 2, 5))
  f <- file.path(study, "truth", sprintf("p%04d", p), paste0(dataset_id, ".rds"))
  if (!file.exists(f)) return(NULL)
  t <- readRDS(f)
  list(dataset_id = dataset_id, active = sort(as.integer(t$active)), beta = t$beta, scenario = t$scenario)
}
input_path <- function(study, dataset_id) file.path(study, "inputs", sprintf("p%04d", as.integer(substr(dataset_id, 2, 5))), paste0(dataset_id, ".rds"))
read_inputs <- function(study, dataset_id) {
  p <- as.integer(substr(dataset_id, 2, 5))
  f <- file.path(study, "inputs", sprintf("p%04d", p), paste0(dataset_id, ".rds"))
  if (!file.exists(f)) return(NULL)
  readRDS(f)
}
# All datasets that have truth (the expected case list is truth x scales).
list_truth_datasets <- function(study) {
  f <- list.files(file.path(study, "truth"), pattern = "^p[0-9]{4}_S[0-9]_r[0-9]{3}\\.rds$", recursive = TRUE)
  sort(sub("\\.rds$", "", basename(f)))
}
