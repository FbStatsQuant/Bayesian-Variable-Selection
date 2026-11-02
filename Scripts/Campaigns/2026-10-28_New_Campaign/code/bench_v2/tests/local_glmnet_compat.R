# Local-only compatibility for deployed tests with glmnet 4.1-10.
# Production code and its 5.1 version gate remain unchanged.
install_local_glmnet <- function(E, settings) {
  settings$GLMNET$pkg_version <- as.character(utils::packageVersion("glmnet"))
  glmnet::glmnet.control(fdev = 0, devmax = 1)
  E$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
    ss <- sqrt(mean(yd^2)); mult <- alpha + ss * (1-alpha)
    fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha/mult,
      lambda = lam*mult, penalty.factor = pf, intercept = FALSE, standardize = FALSE,
      type.gaussian = G$type_gaussian, thresh = G$thresh, maxit = G$maxit)
    E$check_glmnet_path(fit, lam*mult, G)
    B <- as.matrix(fit$beta); scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
    list(B=B, s=ss, m=mult, a=alpha/mult, jerr=fit$jerr, npasses=fit$npasses,
         kkt=E$kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))
  }
  settings
}
