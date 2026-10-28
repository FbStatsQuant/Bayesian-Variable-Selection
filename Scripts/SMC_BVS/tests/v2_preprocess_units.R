# Production-only R-5/B-N1/B-N2 units. Source after changed_units.R with the
# production core and add()/exact()/need() loaded. Every fixture is local, so
# this file neither replaces worker ctx/setup nor consumes any RNG stream.

add("r5_preprocess_ordinary_prototype_bits", local({
  legacy <- function(x) {
    mx <- max(abs(x)); x1 <- x / mx; mu <- mean(x1); x2 <- x1 - mu
    s <- sqrt(sum(x2^2) / (length(x) - 1))
    list(z = x2 / s, max = mx, mean = mu, sd = s)
  }
  ordinary <- list(0:3, c(-3, -1, 0, 2, 7), sin(seq_len(32) * .37),
    c(-1, 0, 1, 2) * 2^900, c(-1, 0, 1, 2) * 2^-900,
    c(1, 1, 1 + 2^-20, 1))
  for (xx in ordinary) exact(v3_standardise(xx), legacy(xx))
  pp <- v3_preprocess(matrix(0:3, 4, 1), setNames(3:0, letters[1:4]))
  exact(pp$y, legacy(3:0)$z)
  need(is.null(pp$stable_centering), "ordinary input acquired fallback metadata")
  list(fixtures = length(ordinary), ordinary_bit_checks_unchanged = TRUE)
}))

add("r5_preprocess_B_N1_hand_Q_and_affine_score", local({
  almost <- c(1, 1, 1 + 2^-52, 1)
  expected <- c(-.5, -.5, 1.5, -.5)
  evidence <- list()
  for (target in c("X", "y")) {
    xx <- matrix(if (target == "X") almost else 0:3, 4, 1)
    yy <- if (target == "y") almost else 0:3
    pp <- v3_preprocess(xx, yy, dup_components = FALSE)
    zz <- if (target == "X") pp$X[, 1] else pp$y
    exact(zz, expected)
    need(abs(mean(zz)) <= 2e-15 && abs(sum(zz^2) - 3) <= 2e-14,
      "B-N1 standardized vector is not centred/sample-scaled")
    cc <- v3_context(pp$X, pp$y, orig = pp$kept)
    sc <- v3_score(cc, 1L)
    need(abs(sc$Q - 57/20) <= 5e-12, "B-N1 hand Q != 2.85")
    differences <- numeric()
    for (mul in c(1, -1, 2^900, -2^-900)) {
      # The shift is exactly representable; no invariance claim is made for
      # affine transformations that erase the input contrast by rounding.
      shifted <- (almost - 1) * mul
      tt <- v3_preprocess(if (target == "X") matrix(shifted, 4, 1) else xx,
        if (target == "y") shifted else yy, dup_components = FALSE)
      ss <- v3_score(v3_context(tt$X, tt$y, orig = tt$kept), 1L)
      differences <- c(differences, abs(sc$log_m - ss$log_m))
      need(abs(sc$Q - ss$Q) <= 5e-12 && tail(differences, 1) <= 1e-9,
        "B-N1 score changed under a represented nonzero affine transform")
    }
    evidence[[target]] <- list(z = zz, Q = sc$Q, log_m = sc$log_m,
      max_affine_log_m_error = max(differences))
  }
  evidence
}))

add("r5_preprocess_nearconstant_multi_ulp_scales_and_permutations", local({
  # The oracle works on small exact integer contrasts, independently of the
  # large offset, arbitrary max|x| division and fallback's contrast scaling.
  offsets <- list(c(0, 0, 1, 0), c(0, 1, 3, 7, 2, 6, 4),
    c(rep(0, 16), 1), c(7, 1, 3, 0, 2, 6, 4))
  worst <- 0
  for (oo in offsets) {
    centered <- oo - mean(oo)
    oracle <- centered / sqrt(sum(centered^2) / (length(oo) - 1))
    for (anchor in c(1, 1.5)) for (scale in c(1, -1, 2^900, -2^-900)) {
      xx <- (anchor + oo * 2^-52) * scale
      ss <- v3_standardise(xx)
      err <- max(abs(ss$z - sign(scale) * oracle))
      worst <- max(worst, err)
      need(err <= 3e-14 && all(is.finite(ss$z)), "nearconstant contrast was lost")
      need(abs(mean(ss$z)) <= 3e-15 &&
        abs(sum(ss$z^2) - (length(xx) - 1)) <= 5e-13,
        "nearconstant two-pass centring/scaling failed")
      need(!is.null(ss$centering), "nearconstant fallback was not used")
      # SD on the max|x| scale, without squaring a huge/tiny raw number.
      expected_sd <- (2^-52 / max(abs(anchor + oo * 2^-52))) *
        sqrt(sum(centered^2) / (length(oo) - 1))
      need(abs(ss$sd / expected_sd - 1) <= 3e-14, "scaled SD map is wrong")
    }
  }
  list(max_oracle_error = worst, contrast_fixtures = length(offsets))
}))

add("r5_preprocess_split_center_map_retained", local({
  xx <- c(1, 1, 1 + 2^-52, 1)
  pp <- v3_preprocess(cbind(17, xx, 0:3), xx, dup_components = FALSE)
  map <- pp$stable_centering
  need(!is.null(map) && identical(names(map$columns), c("2", "3")),
    "fallback map lost original predictor indices")
  need(is.null(map$columns[[2]]) && !is.null(map$response), "fallback map scope is wrong")
  recover <- function(raw, m) {
    u <- (raw - m$anchor) / m$difference_max
    ((u - m$difference_mean) - m$mean_correction) / m$difference_sd
  }
  exact(recover(xx, map$columns[[1]]), pp$X[, 1])
  exact(recover(xx, map$response), pp$y)
  need(abs(pp$s_y / (2^-53) - 1) <= 3e-15, "raw response SD map is wrong")
  need(abs(pp$y_sd_scaled / ((2^-53) / max(xx)) - 1) <= 3e-15,
    "max-scaled response SD map is wrong")
  map
}))

add("r5_preprocess_strict_numeric_shapes_without_coercion", local({
  xx <- matrix(0:3, 4, 1); yy <- 3:0
  cases <- list(
    X_vector = list(X = 0:3, y = yy),
    X_dataframe = list(X = data.frame(x = 0:3), y = yy),
    X_array = list(X = array(0:3, c(4, 1, 1)), y = yy),
    X_character = list(X = matrix(as.character(0:3), 4, 1), y = yy),
    X_logical = list(X = matrix(c(TRUE, FALSE, TRUE, FALSE), 4, 1), y = yy),
    X_list = list(X = matrix(as.list(0:3), 4, 1), y = yy),
    X_complex = list(X = xx + 0i, y = yy),
    y_column_matrix = list(X = xx, y = matrix(yy, 4, 1)),
    y_row_matrix = list(X = xx, y = matrix(yy, 1, 4)),
    y_matrix = list(X = xx, y = matrix(yy, 2, 2)),
    y_array = list(X = xx, y = array(yy, 4)),
    y_list = list(X = xx, y = as.list(yy)),
    y_factor = list(X = xx, y = factor(yy)),
    y_character = list(X = xx, y = as.character(yy)),
    y_logical = list(X = xx, y = c(TRUE, FALSE, TRUE, FALSE)),
    y_complex = list(X = xx, y = yy + 0i),
    y_length = list(X = xx, y = yy[-1]),
    n_small = list(X = xx[1:2, , drop = FALSE], y = yy[1:2]),
    p_empty = list(X = matrix(numeric(), 4, 0), y = yy),
    X_nonfinite = list(X = matrix(c(0, 1, Inf, 3), 4, 1), y = yy),
    y_nonfinite = list(X = xx, y = c(0, 1, NA_real_, 3)))
  statuses <- lapply(cases, function(z) {
    a <- v3_preprocess(z$X, z$y, dup_components = FALSE)
    b <- v3_fit(z$X, z$y, 123)
    exact(a$status, "invalid_input"); exact(b$status, "invalid_input")
    c(preprocess = a$status, fit = b$status)
  })
  # Integers are numeric inputs; converting their validated storage for the
  # double-precision core does not turn an unsupported shape into valid input.
  exact(v3_preprocess(xx, yy)$status, "ok")
  exact(v3_preprocess(xx * 1, yy * 1)$status, "ok")
  exact(v3_preprocess(xx, yy), v3_preprocess(xx * 1, yy * 1))
  statuses
}))

add("r5_preprocess_exact_constants_precedence_and_duplicates", local({
  almost <- c(1, 1, 1 + 2^-52, 1)
  xx <- cbind(0, almost, -almost, 17, almost - 1, 0:3)
  colnames(xx) <- NULL
  pp <- v3_preprocess(xx, almost)
  exact(pp$status, "ok")
  exact(pp$kept, c(2L, 3L, 5L, 6L)); exact(pp$dropped, c(1L, 4L))
  need(length(pp$dup_components) == 1L, "wrong duplicate connected components")
  exact(pp$dup_components[[1]], c(2L, 3L, 5L))
  need(pp$p == 4L, "nearconstant or duplicate predictors were removed")
  # A single minimum-subnormal contrast is still not an exact constant.
  tiny <- c(0, 0, 2^-1074, 0)
  tp <- v3_preprocess(matrix(tiny, 4, 1), tiny)
  exact(tp$status, "ok"); exact(tp$kept, 1L)
  exact(tp$X[, 1], c(-.5, -.5, 1.5, -.5))
  exact(tp$y, c(-.5, -.5, 1.5, -.5))
  none <- v3_preprocess(matrix(1, 4, 2), rep(7, 4))
  constant_y <- v3_preprocess(matrix(0:3, 4, 1), rep(7, 4))
  invalid <- v3_preprocess(matrix(1, 4, 2), c(7, 7, NA_real_, 7))
  exact(none$status, "no_predictors"); exact(none$hpm, integer(0))
  exact(constant_y$status, "y_constant"); exact(constant_y$hpm, integer(0))
  exact(invalid$status, "invalid_input")
  list(kept = pp$kept, dropped = pp$dropped, duplicates = pp$dup_components,
    precedence = c(invalid$status, none$status, constant_y$status))
}))
