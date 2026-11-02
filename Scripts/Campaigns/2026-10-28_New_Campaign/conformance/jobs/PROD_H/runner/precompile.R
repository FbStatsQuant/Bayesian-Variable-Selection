# CONF_NOTS_IDENTITY precompile (job-side; the frozen v2.2 sources are not modified).
# Evaluates core/v3.R except its final compile line, then compiles with visible compiler output (quiet = FALSE).
args <- commandArgs(TRUE); core <- normalizePath(args[1], mustWork = TRUE)
Sys.setenv(V3_CORE_DIR = core)
ex <- parse(file.path(core, "v3.R"), keep.source = FALSE)
stopifnot(identical(deparse(ex[[length(ex)]]), "V3_CPP_KEY <- v3_compile()"))
for (e in ex[-length(ex)]) eval(e, globalenv())
key <- v3_compile(quiet = FALSE)
cat("compiled_key ", key, "\n", sep = "")
