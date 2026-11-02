# Extrapolation of the full p = 30 time from the 3% subset; reads only the saved timing records (TMP/timing/*.rds).
# ELAPSED (wall clock, includes descheduling on a shared machine) and CPU (process user + sys) are kept apart.
T_DIR <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests"
source(file.path(T_DIR, "helpers.R"))
ld <- function(n) readRDS(file.path(TMP, "timing", paste0(n, ".rds")))
a1 <- ld("p30_block_th1_frac0.03"); a8 <- ld("p30_block_th8_frac0.03"); a14 <- ld("p30_block_th14_frac0.03"); fu <- ld("p30_full_th14")
pc <- function(x) sapply(x, function(t) sum(bitwAnd(t, 2^(0:9)) != 0))
d <- data.frame(task = a1$tasks, pc = pc(a1$tasks), sec = a1$task_elapsed_s)
fit <- lm(sec ~ pc + I(pc^2), d); pcall <- pc(0:1023)
pred <- predict(fit, data.frame(pc = pcall)); tot <- sum(pred)
Xm <- model.matrix(~ pc + I(pc^2), data.frame(pc = pcall)); V <- vcov(fit); se_par <- sqrt(sum(colSums(Xm) * (V %*% colSums(Xm))))
se <- sqrt(se_par^2 + (sigma(fit) * sqrt(1024))^2)
cat(sprintf("subset: %d of 1024 tasks, 1 thread, default recheck_stride 1009 (the production re-checks are INCLUDED in these times); elapsed %.2f s, process CPU %.2f s; per-task elapsed range %.0f-%.0f ms; R2 of the popcount fit %.2f\n", nrow(d), a1$elapsed_s, a1$cpu_s, 1000 * min(d$sec), 1000 * max(d$sec), summary(fit)$r.squared))
cat(sprintf("single-thread ELAPSED projection for all 1024 tasks: popcount regression %.0f s +- %.0f s (conditional 1 se, machine state not included); naive mean x 1024: %.0f s\n", tot, se, mean(d$sec) * 1024))
cat(sprintf("single-thread CPU projection (subset process CPU x 1024/%d): %.0f s\n", nrow(d), a1$cpu_s * 1024 / nrow(d)))
cat(sprintf("subset, sum of task elapsed times: threads 1 %.1f, 8 %.1f, 14 %.1f s (elapsed inflation x%.2f for 8 and x%.2f for 14); process CPU %.1f / %.1f / %.1f s\n", sum(a1$task_elapsed_s), sum(a8$task_elapsed_s), sum(a14$task_elapsed_s), sum(a8$task_elapsed_s) / sum(a1$task_elapsed_s), sum(a14$task_elapsed_s) / sum(a1$task_elapsed_s), a1$cpu_s, a8$cpu_s, a14$cpu_s))
cat(sprintf("MEASURED full run, 14 threads: elapsed %.1f s, process CPU %.1f s (%.2f x the single-thread CPU projection), sum of task elapsed times %.0f s (%.2f x the single-thread elapsed projection); cpu load before the run %s%%\n", fu$elapsed_s, fu$cpu_s, fu$cpu_s / (a1$cpu_s * 1024 / nrow(d)), sum(fu$task_elapsed_s), sum(fu$task_elapsed_s) / tot, fu$env$cpu_load_percent_before))
sched <- function(times, nth) { f <- rep(0, nth); for (t in times) { i <- which.min(f); f[i] <- f[i] + t }; max(f) }
infl <- sum(fu$task_elapsed_s) / tot
cat(sprintf("greedy dynamic-schedule simulation on the predicted task times, 14 threads: no slowdown %.0f s; with the slowdown factor x%.2f taken from the full run itself %.0f s (a retrospective calibration, not an independent prediction)\n", sched(pred, 14), infl, sched(pred * infl, 14)))
