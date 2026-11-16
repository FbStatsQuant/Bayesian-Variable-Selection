# ERRATA — W3-PSHARP-R (editorial findings; never block; applied later in one editorial batch, PROTOCOL_v4 §5.3)

Source: council R1 (`reviews/R1_council_opus.md` E-1…E-8, `reviews/R1_council_sol.md` E1…E3), manifest fd8b32a5….
| id | place | item | proposed correction |
|---|---|---|---|
| R1-opus-E1 | `STATEMENT.md:122-123`; `lemmas/AE_expectation.md` §9 Remark 2 | "0.99–1.03 at n = 10⁶" (the 1.028 is at n = 10⁴) | "0.99–1.02 at n = 10⁶" |
| R1-opus-E2 / R1-sol-E1 | `TARGET.md:36-38` | "MC s.e. ≤ 5·10⁻⁴ relative"; p = 5, s₀ = 2 row omitted | "reported absolute MC s.e. ≤ 5·10⁻⁴ (relative ≤ 2.3·10⁻³)"; "p = 5: 1.01 → 1.02 (s₀ = 1), 0.97 → 1.01 (s₀ = 2)" |
| R1-opus-E3 | `STATEMENT.md:22` (row C4); `TARGET.md:30` | "limsup π(S₀) ≤ e^{−λ}" without mode | "π(S₀) ≤ e^{−λ} + o_P(1) and limsup E π(S₀) ≤ e^{−λ}" |
| R1-opus-E4 | `STATEMENT.md:133` | consumed list omits Lemma S(3) (used in A2C §2) | add S(3) |
| R1-opus-E5 | `STATEMENT.md:113` | attribution "(A1-E(b), A2-E)" | "(A1-E: main display with ℓ_n ≥ ½ log n, and (b))" |
| R1-opus-E6 / R1-sol-E2 | `READER_DELTA.md:6` vs `:62` | inconsistent proof-status wording | "proofs in lemmas/, each with status PROVED (by this seat, unchecked); independent council review pending" (until CP3) |
| R1-opus-E7 | `READER_DELTA.md:40` | "p = n^a" without the orthogonal cap | add "(under orthogonal null columns, p = min(n − 1, ⌊n^a⌋), a ≤ 1)" |
| R1-opus-E8 | `REPORT.md:57` | A2C premises omit in-line hypotheses | `premises: STATEMENT.md:33-37,96-98` |
| R1-sol-E3 | `READER_DELTA.md` "Why each assumption" | "their maximum gives the √(log p)" misdescribes the route | "used here (the sum of their truncated fit factors gives the √(log p))" |

Proposals (not findings, for HQ): a random-(X_{S₀}, θ*) clause for Cor A2-E (R1-opus, sketch in its F-2(b)); cross-reference
A2C's expectation form from the reader critical-scale remark.
