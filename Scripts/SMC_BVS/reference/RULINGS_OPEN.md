# Lead's rulings on the 2 OPEN items (2026-10-22; Felipe delegated these decisions to the lead)

## OPEN-1 (DP2 D4): the cut-group flag predicate
- **Correlated group** = a connected component of the neighbour graph that the method already builds (vertices j in [p]; edge j–k when |r_jk| ≥ ρ_n = √(2 log p / n), where r is the sample correlation of the standardised columns). This is the same graph and the same threshold as the method's neighbour step. There is no new constant.
- **Flag `cut_group`**: raised when some connected component C is split across two or more composite-start blocks. Every component with |C| > B is necessarily split, so it is always flagged.
- **Report**, for each flagged component: its size |C|, the number of blocks it spans, and its member indices (original column indices, as in R12). Also report the count of flagged components.
- The flag is informational. It changes no setting, no status and no budget. B is unchanged.
- If the method's neighbour-graph definition differs in any detail (for example, whether it uses the per-variable capped neighbour lists), use the *uncapped* threshold graph for this flag and state that. Record your reading in CHANGES.md.

## OPEN-2 (R9/R16): the numerical error bound behind `global_certified`
- Deploy the verified prototype's rule unchanged. The error bound of log m(S) is the documented heuristic in prototype_core/cpp/v3_score.h (lines ~241–247):
  - η(S) = 64 ε [ ν (y'y/Q)(1 + k κ_H) + k (κ_H + κ_A) + |log C_n| + ν |log(2b₀ + Q)| ]
  - ε is the machine epsilon of double precision.
  - κ_H and κ_A are the cheap condition estimates (max/min Cholesky diagonal)² used there.
  - Take the exact definitions of C_n, κ_H and κ_A from the code.
- `global_certified` is set, on the exact branch only, when every comparison that decided the HPM has a margin above this bound.
- The output must label the bound "heuristic (not a validated interval bound)" and report it with each certificate.
- State in the text that this is a numerical safety rule, not a statistical tuning constant.
