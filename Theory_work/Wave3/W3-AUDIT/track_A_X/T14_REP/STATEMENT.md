# T14 · Lemma REP (IDEAL-W⁺ is vacuous on inputs R can represent) — STATEMENT v1 (DRAFT, post-freeze item; not locked; wording per manager 11-16: "IDEAL-W⁺ costs nothing on any input the software can receive (n, p ≤ 2³¹ − 1)")

HQ 11-16: approved as a small post-freeze item outside the track D cap; drafting allowed now; kill at 1 day; one Sol line
check. Tier B (code reading). **Lean target: no** (a code fact; the arithmetic is trivial).

## Source
- A:IDEAL-W⁺ (verbatim definition `Theory_work/Wave1C/C-DLV/INVENTORY.md:93`): IDEAL-W "and the two shipped rejection
  predicates `le > 10⁶` (`Scripts/SMC_BVS/core/v3_run.R:96`, … le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the shipped
  configuration) and `ℓ + |S̃₀| > INT_MAX` (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`, the disjunct
  `cap_ll > numeric_limits<int>::max()` …) are false."
- IDEAL-W: "an abstract unbounded-word/address machine: integer, index, stream-id and allocation arithmetic never
  overflow" (`Theory_work/Wave1C/C-DLV/STATEMENT.md:24-25`).
- The batch NARROW of 2026-11-16 (19 claims) to "A:IDEAL-W⁺ or (𝔇)" (`Theory_work/INFRA/DECISIONS.md:95`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6, shipped `v3_fit`, options `v3.ls0`, `v3.ls0_ell`, `v3.ls0_cap` unset.

## Definition
An input (X, y, seed, allocation) is **R-representable** if X is an R numeric matrix and y an R numeric vector. R stores a
matrix's dimensions in an integer `dim` attribute, so n := `nrow(X)` ≤ 2³¹ − 1 and p_raw := `ncol(X)` ≤ 2³¹ − 1 (long
vectors raise only the length bound n·p_raw); the core reads both as C++ `int` (`int n = X.nrow(), p = X.ncol()`,
`Scripts/SMC_BVS/core/cpp/v3_core.cpp:92`).

## Lemma REP
For every R-representable input of the shipped `v3_fit` that reaches the two sites:
- **(REP-a)** at `Scripts/SMC_BVS/core/v3_run.R:95-97`, `le` = ℓ_n = ⌈log₂(n + p + 1)⌉ ≤ 32, so `le > 1e6` is false (and the
  other conditions of that validator hold, so it does not stop);
- **(REP-b)** at `Scripts/SMC_BVS/core/cpp/v3_core.cpp:473-474`, `o.ls0_ell` = ℓ_n ∈ [3, 32] and
  `cap_ll` = ℓ_n + |S̃₀| ≤ 32 + ⌊n/2⌋ ≤ 2³⁰ + 31 < 2³¹ − 1 = INT_MAX, so neither disjunct of the guard holds.
Hence the two predicates that A:IDEAL-W⁺ lifts are false on every R-representable input: **IDEAL-W⁺ costs nothing on any input the software
can receive (n, p ≤ 2³¹ − 1)**: its two extra predicates are false there, so its extra clause holds vacuously.

## Not claimed
- Anything for inputs beyond R's limits (n or p_raw ≥ 2³¹), which exist only on IDEAL-W's abstract machine; there the
  two predicates can be true (n + p ≥ 2^(10⁶)), and A:IDEAL-W⁺ remains a genuine extra premise.
- That other `int` arithmetic is safe on all R-representable inputs (e.g. `2 * p - 1`, `cpp/v3_blocks.h:49`, overflows for
  p ≥ 2³⁰): that is IDEAL-W's own content, unchanged.
- Non-default options (a user setting `v3.ls0_ell` > 10⁶ makes X7 fire by design).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v0 | all | NEW-CLAIM | HQ 11-16 post-freeze item | manager message 11-16 | Sol line check VERIFIED (`reviews/LC1_reply_sol_T14.md`) |
| v1 | (REP-b) proof: structural size bound on the start mode (no T9, no EX-A/H2-FP); ℓ_n range [3, 32] | EQUAL (claim unchanged; proof made premise-free as stated) | XR1 Opus F1, E7, E8 | `reviews/XR1_council_opus.md` | diff round XR2 |
