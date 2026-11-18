# Inventory: citations of MEAS-D's h-clause, and whether each citing h has a data-dependent bound (manager check (iii), 11-18)

The clause (MEASD5): "1_{𝒜°}Z, 1_{𝒜°}Ẑ and 1_{𝒜°}Ẑ_r·H_r(h), for every h of §2 whose bound B_h does not depend on the data, are integrable under the joint law of §0, for every law of the data" (`STATEMENT.md:190`).

## Search
- Every file in the worktree (Theory_work/**, md/tsv/txt) for "MEAS-D" and "MEAS_D", and for "H_r(h)"; and `git grep` on `origin/main`, `origin/theory/PRE-LEAN-walkA..D`, `origin/theory/W3-D5P`, `origin/dept/theory`.
- **Citations of MEAS-D outside the pre-Lean pass and the department's own log/queue/cards: none.** `origin/main`, the four walk branches and `theory/W3-D5P` contain no occurrence of "MEAS-D" or "MEAS_D". `origin/dept/theory` has it only in `Theory_work/Dept/LOG.md`, `QUEUE.md` and the cards `pre_lean_cards/MEAS-D_*.md`, `T9*.md` (process records, no h). No file named NA_DROP exists on `origin/main`.
- "H_r(h)" occurs in many files (N1 and old research notes); those are N1's own definition of the accumulator, not citations of MEAS-D.

## The h's that MEAS-D's "serves" clauses actually use (W3-SAMP, via Lemma MR; `STATEMENT.md:107-116`)
| clause | h | B_h | data-dependent bound? |
|---|---|---|---|
| (LT-a)/(LT-b…) weighted (`lemmas/LT_theorem.md:26`) | 1{S ≠ S₀} | 1 | no |
| (LT-…) (`lemmas/LT_theorem.md:37`) | 1{S = S₀} | 1 | no |
| (C-ii)/(C-iii) (`lemmas/C_theorem.md:28`) | 1{S ≠ s}, s a fixed model | 1 | no |
| (C) evidence (`lemmas/C_theorem.md:47`), PoolZ | h ≡ 1 | 1 | no |
| pip_plain / PIP (N1 §1, `W1-N1/STATEMENT.md:51-56`) | 1{j ∈ S} | 1 | no |
| MR identities in general (`lemmas/MR_identities.md:25, 62`) | any jointly measurable h with deterministic sup bound B_h | B_h deterministic | `MR_identities.md:62` bounds the integrand g by B_h·C_d, where C_d is a constant of the fixed data: this bounds g, not h; B_h itself is data-free |
| DIST-C P⊗ clauses, Cor C (`W3-DIST/STATEMENT.md:293-317`, `COR_C.md`) | no h (events about {completed}, 𝓜, 𝒯) | none | n/a |

**Result: every h used by a clause that MEAS-D serves is an indicator or the constant 1 (B_h = 1), so no citing h has a data-dependent bound.** The stop condition ("if any citing h does have a data-dependent bound, stop and bring it to me") is not triggered. The only h with an unspecified B_h is the abstract class of Lemma MR (`MR_identities.md:25`), whose bound is "deterministic" in N1's sense (not random); the qualifier in the statement makes the data-independence explicit.
