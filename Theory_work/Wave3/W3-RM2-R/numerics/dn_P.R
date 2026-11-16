# dn_P.R -- Monte Carlo value of d_n := E max_{v in D^T_n} |v'g| for design P, against the closed form of STATEMENT section 5(a).
# Family D^T_n (PARENT lemmas/L2_width.md:184): u_{A,1} = (I-P_A)x_1/||.||, A = T\{1} or (T\{1}) + {l}, T in [S0,Q], S0 = {1}.
# In design P (x_j = sqrt(n-1) z_j; z_j = r e_1 + rho e_j (2<=j<=q), rho = sqrt(1-r^2); other columns e_j orthogonal to e_1..e_q):
#  * l outside Q does not change (I-P_A)x_1 (e_l is orthogonal to e_1 and to span{e_j: j in A}), so every direction is u_A with A a
#    subset of the q-1 proxies (T ranges over all of them; l in Q\T gives a subset again);
#  * by symmetry (I-P_A)e_1 = rho^2/D e_1 - (r rho/D) sum_{j in A} e_j, norm^2 = rho^2/D, D = rho^2 + t r^2, t = |A|, so
#        u_A' g = (rho g_1 - r sum_{j in A} g_j) / sqrt(rho^2 + t r^2),  g_1, g_j iid N(0,1) (coordinates of g on e_1, e_j).
#    The max over ALL subsets A of size t is therefore attained by the t largest (or t smallest) g_j: exact, no subset sampling.
# 2000 draws of g. Closed form: d_n <= sqrt(2/pi) (1 + r (q-1)) / sqrt(1-r^2)   (STATEMENT section 5(a)).
set.seed(20261116)
res <- NULL
for (n in c(400, 1600)) for (b in c(0.3, 0.45)) {
  q <- floor(n^b + 1e-9); r <- sqrt(log(n) / n); rho <- sqrt(1 - r^2); m <- q - 1; tt <- 0:m
  D <- sqrt(rho^2 + tt * r^2); draws <- 2000; dv <- numeric(draws); targ <- integer(draws)
  for (i in 1:draws) {
    g1 <- rnorm(1); gj <- sort(rnorm(m)); cs_top <- c(0, cumsum(rev(gj))); cs_bot <- c(0, cumsum(gj))   # sums of the t largest / smallest
    val <- pmax(abs(rho * g1 - r * cs_top), abs(rho * g1 - r * cs_bot)) / D                              # best of both signs per t
    dv[i] <- max(val); targ[i] <- which.max(val) - 1L
  }
  res <- rbind(res, data.frame(n = n, b = b, q = q, r = round(r, 4), d_mc = round(mean(dv), 4), d_mc_se = round(sd(dv) / sqrt(draws), 4),
    d_t0 = round(sqrt(2 / pi), 4), d_closed_bound = round(sqrt(2 / pi) * (1 + r * (q - 1)) / sqrt(1 - r^2), 4),
    d2_over_logn = round(mean(dv)^2 / log(n), 4), frac_argmax_t0 = round(mean(targ == 0), 3)))
}
print(res, row.names = FALSE); write.csv(res, "dn_P.csv", row.names = FALSE)
