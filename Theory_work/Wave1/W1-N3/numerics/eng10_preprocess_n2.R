# Asserts that the frozen public preprocessing rejects n = 2 (CODE/v3_preprocess.R:106).
src <- "../../../../Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/v3_preprocess.R"
source(src)
r <- v3_preprocess(matrix(c(1, 2, 3, 5), 2, 2), c(1, 4))
cat("n = 2 status:", r$status, "| reason:", r$reason, "\n")
stopifnot(identical(r$status, "invalid_input"), identical(r$reason, "n < 3"))
r3 <- v3_preprocess(matrix(c(1, 2, 4, 3, 5, 4), 3, 2), c(1, 4, 2))
cat("n = 3 status:", r3$status, "\n")
