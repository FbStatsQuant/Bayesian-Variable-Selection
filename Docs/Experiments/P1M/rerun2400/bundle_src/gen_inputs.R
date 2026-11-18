#!/usr/bin/env Rscript
# gen_inputs.R GEN_DIR DATASET_ID STUDY_DIR
# Writes the OLD side's study layer inputs for ONE dataset exactly as gen_prod_data.R::main does: STUDY/inputs/pPPPP/<id>.rds (d$inputs,
# uncompressed, 0444) and a one-row STUDY/manifests/inputs_manifest.csv with the same columns as the cell fragments (file sha256, x, foldid,
# y_<scale> sha256). The v2.2.1 adapter then verifies the file hash and the stored-array hashes against that manifest, as in the original run.
a <- commandArgs(TRUE); stopifnot(length(a) == 3L)
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(here, "common_gen.R"))
g <- load_prod_generator(a[1]); cs <- parse_case(a[2]); study <- a[3]
d <- g$generate_prod_dataset(cs$p, cs$s, cs$r)
di <- file.path(study, "inputs", sprintf("p%04d", cs$p)); dm <- file.path(study, "manifests")
for (x in c(di, dm)) dir.create(x, recursive = TRUE, showWarnings = FALSE)
fi <- file.path(di, paste0(d$inputs$dataset_id, ".rds"))
if (file.exists(fi)) stop("refusing to overwrite ", fi)
saveRDS(d$inputs, fi, compress = FALSE); Sys.chmod(fi, "0444")
SC <- g$SCALES
row <- data.frame(dataset_id = d$inputs$dataset_id, p = cs$p, scenario = cs$s, replicate = cs$r,
  data_seed = d$inputs$data_seed, fold_seed = d$inputs$fold_seed, method_seed = d$inputs$method_seed,
  file_sha256 = digest::digest(file = fi, algo = "sha256"),
  x_sha256 = g$f64_sha256(d$inputs$X), foldid_sha256 = g$f64_sha256(d$inputs$foldid),
  t(setNames(vapply(names(SC), function(k) g$f64_sha256(d$inputs$Y[, k]), ""), paste0("y_", names(SC), "_sha256"))), check.names = FALSE)
utils::write.csv(row, file.path(dm, "inputs_manifest.csv"), row.names = FALSE)
cat("gen_inputs", cs$dataset_id, "x_sha256", row$x_sha256, "\n")
