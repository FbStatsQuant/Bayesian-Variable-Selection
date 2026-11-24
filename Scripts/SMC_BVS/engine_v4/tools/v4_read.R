# v4_read.R -- read an engine_v4 binary container (INTERFACES §5.1) in base R. v4_read(path) returns a list with
# kind, mode, sections (data.frame) and get(name) returning the section as a numeric / integer vector or parsed json.
v4_read <- function(path, verify = TRUE) {
  sz <- file.size(path); con <- file(path, "rb"); on.exit(close(con))
  raw <- readBin(con, "raw", n = sz)
  u32 <- function(off) { v <- readBin(raw[(off + 1):(off + 4)], "integer", size = 4, endian = "little"); if (v < 0) v + 2^32 else v }
  u64 <- function(off) u32(off) + u32(off + 4) * 2^32
  if (!identical(rawToChar(raw[1:7]), "SMCBVS4")) stop("bad magic: ", path)
  kind <- u32(12); mode <- u32(16); ns <- u32(20)
  if (u64(24) != sz) stop("file size mismatch: ", path)
  secs <- lapply(seq_len(ns), function(i) {
    b <- 128 + (i - 1) * 128
    nm <- rawToChar(raw[(b + 1):(b + 48)][raw[(b + 1):(b + 48)] != as.raw(0)])
    list(name = nm, dtype = u32(b + 48), ndim = u32(b + 52), d0 = u64(b + 56), d1 = u64(b + 64),
         offset = u64(b + 72), length = u64(b + 80), sha = paste(as.character(raw[(b + 89):(b + 120)]), collapse = ""))
  })
  df <- do.call(rbind, lapply(secs, as.data.frame))
  if (verify && requireNamespace("digest", quietly = TRUE))
    for (s in secs) {
      h <- digest::digest(if (s$length > 0) raw[(s$offset + 1):(s$offset + s$length)] else raw(0), algo = "sha256", serialize = FALSE)
      if (!identical(h, s$sha)) stop("section hash mismatch: ", s$name)
    }
  get <- function(name) {
    s <- secs[[match(name, df$name)]]; if (is.null(s)) stop("missing section ", name)
    r <- if (s$length > 0) raw[(s$offset + 1):(s$offset + s$length)] else raw(0)
    switch(as.character(s$dtype),
      "1" = readBin(r, "double", n = s$length / 8, size = 8, endian = "little"),
      "2" = readBin(r, "integer", n = s$length / 4, size = 4, endian = "little"),
      "9" = jsonlite::fromJSON(rawToChar(r), simplifyVector = FALSE),
      stop("dtype ", s$dtype, " not supported by v4_read.R"))
  }
  list(kind = kind, mode = mode, sections = df, get = get)
}
