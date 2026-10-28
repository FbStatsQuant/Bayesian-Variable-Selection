# PART II: small local tables and the product composite likelihood.
# Each block regression uses the same y. SMC later corrects this artificial start.

make_composite_likelihood <- function(context, cfg) {
  set.seed(cfg$seed_blocks)
  permutation <- sample.int(context$p)
  groups <- ceiling(seq_along(permutation) / cfg$block_size)
  blocks <- unname(split(permutation, groups))
  tables <- lapply(blocks, function(columns) {
    block_p <- length(columns)
    codes <- 0:(2^block_p - 1L)
    bits <- vapply(seq_len(block_p), function(j)
      as.integer(bitwAnd(codes, bitwShiftL(1L, j - 1L)) != 0L), integer(length(codes)))
    bits <- matrix(bits, nrow = length(codes), ncol = block_p)
    log_likelihood <- vapply(seq_along(codes), function(i)
      log_marginal_likelihood(columns[bits[i, ] == 1L], context), numeric(1))
    log_weight <- log_likelihood +
      log_model_prior(rowSums(bits), block_p, cfg$inclusion_probability)
    log_Z <- log_sum_exp(log_weight)
    probability <- exp(log_weight - log_Z)
    list(columns = columns, codes = codes, bits = bits,
         log_likelihood = log_likelihood, probability = probability, log_Z = log_Z,
         local_pip = colSums(bits * probability))
  })
  local_pip <- numeric(context$p)
  for (tab in tables) local_pip[tab$columns] <- tab$local_pip
  list(blocks = blocks, tables = tables,
       log_Z0 = sum(vapply(tables, function(tab) tab$log_Z, numeric(1))),
       pip = local_pip)
}

local_codes_from_global <- function(codes, columns) {
  answer <- integer(length(codes))
  for (position in seq_along(columns)) {
    included <- bitwAnd(codes, bitwShiftL(1L, columns[position] - 1L)) != 0L
    answer <- answer + as.integer(included) * bitwShiftL(1L, position - 1L)
  }
  answer
}

composite_log_likelihood <- function(codes, composite) {
  answer <- numeric(length(codes))
  for (tab in composite$tables) {
    local_code <- local_codes_from_global(codes, tab$columns)
    answer <- answer + tab$log_likelihood[local_code + 1L]
  }
  answer
}
