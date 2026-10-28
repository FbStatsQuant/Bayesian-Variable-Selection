# Discover an adopted data-only R-1 policy from the frozen A adapter, never construct one.
load_a_r1_policy <- function() {
  candidates <- ls(envir=.GlobalEnv,pattern="^smcbvs_.*policy$")
  for (nm in candidates) {
    fun <- get(nm,envir=.GlobalEnv)
    if (!is.function(fun)) next
    value <- tryCatch(fun(),error=function(e) NULL)
    if (is.list(value) && isTRUE(value$adopted) && identical(value$mapping_status,"adopted") &&
        identical(unname(value$roles[c("hpm","pip05")]),c("primary","S0"))) return(value)
  }
  stop("current A adapter has not published an adopted R-1 policy; do not invent one")
}
