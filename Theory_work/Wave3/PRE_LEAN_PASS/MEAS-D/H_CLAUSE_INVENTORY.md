# Inventory: citations of MEAS-D's h-clause, and whether each citing h has a data-dependent bound (manager check (iii), 11-18)

The clause (MEASD5): "1_{𝒜°}Z, 1_{𝒜°}Ẑ and 1_{𝒜°}Ẑ_r·H_r(h), for every h of §2 that is a Borel function of (data, S, c) with a bound B_h that does not depend on the data, are integrable under the joint law of §0, for every law of the data" (MEASD6) (`STATEMENT.md:190`).

## Search
- Every file in the worktree (Theory_work/**, md/tsv/txt) for "MEAS-D" and "MEAS_D", and for "H_r(h)"; and `git grep` on `origin/main`, `origin/theory/PRE-LEAN-walkA..D`, `origin/theory/W3-D5P`, `origin/dept/theory`.
- **Citations of MEAS-D outside the pre-Lean pass and the department's own log/queue/cards: none.** `origin/main`, the four walk branches and `theory/W3-D5P` contain no occurrence of "MEAS-D" or "MEAS_D". `origin/dept/theory` has it only in `Theory_work/Dept/LOG.md`, `QUEUE.md` and the cards `pre_lean_cards/MEAS-D_*.md`, `T9*.md` (process records, no h). No file named NA_DROP exists on `origin/main`.
- "H_r(h)" occurs in many files (N1 and old research notes); those are N1's own definition of the accumulator, not citations of MEAS-D.

## The h's that MEAS-D's "serves" clauses actually use (W3-SAMP, via Lemma MR; `STATEMENT.md:107-116`): why each is Borel in (data, S, c), and its B_h
(MEASD6 qualifier: h is a Borel function of (data, S, c) with a bound B_h that does not depend on the data. Ω is finite, so Borel in S is automatic; calibration coordinates c enter through 𝓒°, Borel by Step 3.)

| clause | h | Borel in (data, S, c): why (proved text) | B_h |
|---|---|---|---|
| LT weighted (`lemmas/LT_theorem.md:26`) | 1{S ≠ S₀} | S₀ is a fixed model (`STATEMENT.md:26`, "Truth"), so h depends on S only: a function on the finite set Ω, constant in (data, c) | 1 |
| LT (`lemmas/LT_theorem.md:37`) | 1{S = S₀} | same | 1 |
| (C-ii), (C-iii) (`lemmas/C_theorem.md:28`) | 1{S ≠ s}, s := S₀ (`C_theorem.md:8-9`) | same | 1 |
| (C) evidence (`lemmas/C_theorem.md:47`), PoolZ | h ≡ 1 | constant | 1 |
| pip_plain (N1 §1, `W1-N1/STATEMENT.md:51-56`) | 1{j ∈ S} | function of S only | 1 |
| (C-iii) loss per stage (`lemmas/C_theorem.md:37-40`) | f_t(S) = (1 − e^{Δ_t a(S)})⁺, a(S) = d(S) − d(S₀), d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b) (`STATEMENT.md:24`) | **depends on the data through d.** d is a Borel function of the data: log BF(S) = log m(S) − log m(∅) is continuous in the data on each cell and the block start tables r_b are among the data constants, Borel by Step 2 (`lemmas/MEAS_D.md:32, 37`); Δ_t = φ_t − φ_{t−1} is read from the grid values, which are coordinates of 𝓒° (CAL-c, Step 4); (·)⁺ and exp are continuous. So f_t is Borel in (data, S, c). `C_theorem.md:37` already calls it "data-and-c-measurable". | 1 |
| MR identities in general (`lemmas/MR_identities.md:25, 62`) | any h jointly measurable with deterministic bound B_h | the class of the clause itself; MEASD6 states the Borel-in-(data, S, c) hypothesis. `MR_identities.md:62` bounds the integrand g by B_h·C_d, with C_d a constant of the fixed data: this bounds g, not h | B_h |
| DIST-C P⊗ clauses, Cor C (`W3-DIST/STATEMENT.md:293-317`, `COR_C.md`) | no h (events about {completed}, 𝓜, 𝒯) | n/a | n/a |

**Corollary E's [0,1]-valued h** (`W1-N1/STATEMENT.md:108-109`; "as in §1") is not used by any clause that MEAS-D serves: a grep of `Theory_work/Wave3/W3-SAMP/` (STATEMENT.md, lemmas/), `W3-READER/STATEMENT.md`, `W3-READER/lemmas/` and `W3-DIST/STATEMENT.md` for "Corollary E" / "M1(e)" finds no occurrence (the only hit is `W3-SAMP/reviews/CITECHECK.txt`, a citation list). Its h is of N1 §1's class (jointly measurable in (S, c) at fixed data), so it is covered by MEAS-D's h-clause exactly when it is also Borel in the data, as the qualifier says.

**Result (MEASD6).** Every h used by a clause that MEAS-D serves is Borel in (data, S, c) by proved text (the functions of S alone are trivial; f_t by MEAS-D Step 2 and CAL-c), and has B_h = 1, independent of the data. The stop condition ("if any citing h cannot be shown Borel from proved text, stop") is not triggered. History: the first version of this table said "every h is an indicator or the constant 1", which was false (f_t depends on the data through d); R5 (F7) found the gap, and R5's list is now complete.
