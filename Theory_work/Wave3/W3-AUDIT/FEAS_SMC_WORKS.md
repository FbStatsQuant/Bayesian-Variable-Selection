# Feasibility note — "the SMC does work": Result 4 under bounded leakage (audit Fable, 2026-11-17; for HQ and the consultant)

**Status (2026-11-17): the owner has deferred "the SMC does work" to the follow-up paper; this note is kept for HQ as
the record of what a route through existing lemmas would need.** Half-day note, no proving. Every argument below is a sketch [unchecked]; recorded results are cited with their status.
"Result 4" = core theorem 4: the printed PIPs, MPM and Ẑ are consistent (row 3.6), today proved only without leakage.

## 1. Answer to the question as asked

**Do the importance weights between the start law and the posterior stay polynomially bounded?** It depends on the level
of the leaks inside the leakage set Q, and the record already says which way:

| Leaks inside Q (bounded set, \|Q ∖ S₀\| ≤ q̄) | End-to-end weight at the truth, π(S₀)/π₀(S₀) | Source |
|---|---|---|
| gains at the logarithmic level, δ²_{U,l} ≤ a_l·τ²_U·log n | **polynomial**: ≤ n^{E_n+ε}, E_n = Σ_l [(a_l − 1)/2 − log p/log n]₊ | Proposition OVL⁺, `W3-START2/STATEMENT.md:181-189`; carried as `W3-START2-R:OVL@1.0.0`, "PROVED-CHECKED; council R2, …" |
| gains at a fixed level (AR neighbours, block-mates outside the truth's block; gain ≍ n) | **not polynomial**: above every power of n, exponential by the proof line | `W3-START:NEC-b`, "PROVED-CHECKED"; `reviews/AUDITCALC_check_opus.md` §1–§2 (asymptotic; silent at n ≤ 400, p = 10⁶) |

So "polynomial weights, hence n-many particles" is a true and cheap statement for weak leaks (§5), and false as a
mechanism for the designs HQ cares about (AR, BLK). There the sampler can only work through the tempered path: small
stage-to-stage weights plus moves that delete the spurious columns at the right temperature. That is the target of §2.

## 2. The statement it would be (target "SMC-L")

*Design.* Theorem 6's assumptions (Gaussian rows, fixed signals, visibility (A3), leakage set Q with locality (A4),
floors (A5), local regressions (A6)), with **\|Q ∖ S₀\| ≤ q̄ fixed**. Leaks inside Q may be of any level. (S3, S4, S6 and BLK
satisfy this; AR has \|Q ∖ S₀\| ≍ log n and would be a second step.)
*Method, as coded at 4676af6.* Exact start draws (track A T6); the four coded moves, each reversible for the tempered
target, one round per bridge stage and L = max(4, ⌈log₂(n + 1)⌉) rounds at the end (T7 KER; `W3-SAMP/STATEMENT.md:97-105`);
the island as the frozen-run model with (R1)–(R3) (track A X1, FR); N_e = max(2500, n, p); the grid frozen by the
calibration.
*Grid premise, to be proved or stated.* (GR): on calibration success, between consecutive grid points the tempered
targets restricted to the lattice 𝓛(Q) have χ²-distance at most a constant, and the number of stages is at most n^{o(1)}.
*Conclusion.* 1_𝒜·(|Ẑ/Z − 1| + max_j|pip_j − 1{j ∈ S₀}|) → 0 in probability, and P(𝒜 ∩ {MPM ≠ S₀}) → 0; intersections
with calibration success, as in Theorem 10. No start concentration is assumed.

## 3. Route and what it reuses

1. *The population stays on the lattice.* For a lattice state and any single move that leaves 𝓛(Q), the odds under the
   tempered target are a geometric mean of the odds at the two ends, so they are bounded by the larger end. The ends
   are recorded, uniformly over the block family: leak and visibility bounds at the start (`W3-START:LEAK`, `VIS-c`,
   "PROVED-CHECKED"), no-addition and truth-removal at the posterior (`W3-RM2:NA-W`, `TL-F-b`, "PROVED-CHECKED; council
   R1, …"). Start: `W3-START2-R:START-R` (i) puts π₀ on 𝓛(Q). This is gate G1 of `TRACK_D.md` §5a.
2. *On the lattice, a bounded problem.* 𝓛(Q) has at most 2^{q̄} states. Each spurious column switches off at its own
   temperature. Near a switch the target is a two-model family, for which the grid lemmas exist (`C-DLV:L5-5.1`, `L5-5.2`,
   `Cor-5.3`, "PROVED-CHECKED").
3. *Forgetting.* After one coded round at temperature φ, the lattice state of a particle is redrawn close to the
   tempered target on 𝓛(Q). This is new: a quantitative statement about the coded moves on a set of bounded size.
4. *Variance.* With 1–3, a second-moment bound for Ẑ_r/Z of order (number of stages)/N_e, from the frozen-run
   identities (`W3-SAMP:MR`, X1 FR). Then `W3-SAMP:LT#` (LT-e), "PROVED-CHECKED", gives the printed PIPs and MPM.
5. Not reused: T8 OVL (it is stated under no leakage) and route TR (its bound is empty here).

## 4. Main obstacle

**Step 3, and behind it the grid premise.** Without forgetting, the variance is governed by π/q_t on lattice states, which
is exponential in n for fixed-level leaks; with perfect forgetting it is the stage-to-stage χ². The proof has to place
the coded round between the two. Two concrete risks: (i) spurious columns that share a method block are substitutes
at small φ (the block prefers one proxy; states with two or none are separated by a gap of order n), so forgetting
inside a block rests on the coded within-block move, which no recorded result analyses; (ii) (GR) is a property of the
calibration's output; the recorded grid lemmas describe the construction, not the χ²-distances it achieves on the
realised lattice. If (GR) cannot be derived, it must be stated as a premise, and the theorem loses much of its point.
The record contains no mixing or variance statement for the coded sampler (`W3-SAMP/STATEMENT.md:183`).

## 5. Cost, kill budget, GO / NO-GO

- **Full target SMC-L:** Tier A (two new key lemmas: forgetting, variance), Fable on the key lemmas with HQ's OK, Opus
  lead about 8–10 days, then the usual reviews. Risk high. **NO-GO as a ticket now.**
- **Gate, GO (2 lead-days, hard stop):** G1, write step 1 as a lemma and check uniformity at the start end, including
  additions inside a block that already holds lattice extras; G2, exact computation on a toy lattice (one truth, two
  proxies in one block, one in another; coded moves and resampling; a grid from the two-model insertion rule): is
  Var(Ẑ_r/Z) = O(T/N_e), and does one round forget? **Kill:** either gate fails, or the within-block gap of risk (i) shows
  up in G2. Only if both pass does SMC-L become a ticket, with a kill budget of 3 attempts on step 3 and 10 lead-days.
- **Cheap adjacent result, GO (Tier B, 1–2 lead-days, kill 3 days): "weak-leak corollary".** Under a bounded leakage set
  with logarithmic gains and limsup(E_n − max(1, log p/log n)) < 0, OVL⁺ gives P-OVL, and `W3-SAMP:D` (D-iv),
  "PROVED-CHECKED", gives P(completed ∩ {S₀ ∉ models scored by the islands' start draws}) → 0: **the sampler itself finds
  S₀ with n-many particles, by its own draws, without the final search.** Recorded pieces only; the new work is the
  Gaussian-row bridge for OVL⁺ (it is a fixed-design proposition) and the reader statement. It says nothing on PIPs or Ẑ.

**Recommendation in one line:** GO for the weak-leak corollary and for the 2-day gate; NO-GO for SMC-L until the gate
passes; printed fields on AR and BLK stay scoped as now (Theorem 6, row 3.5, and #5′ for list-based summaries).

## 6. Two side questions

- **(a) Factor-adjusted start law (follow-up paper only).** With a pervasive factor every null leaks from every truth under
  the block start, so Q = [p] and core 3 and row 3.6 exclude S5, P6 and FAC. A start law computed on columns with the
  leading factors projected out would make the leakage set small again and could bring factor designs inside both. It
  changes the method, so none of the "as coded" results applies to it; `W2-FAC-PK:Thm-NEG` ("PROVED-CHECKED") is the
  recorded reason the coded search fails there for K < p ≤ n − 1.
- **(b) Evidence variance: what is cheap.** Three things, none of them a variance bound: the upper tail
  P(Ẑ_r/Z > u | calibration) ≤ 1/u (from unbiasedness, `W1-N1:Thm-N1`); the list sum Z^𝒯 ≤ Z, a lower bound on Z computed
  from the output (#5′); and E|Ẑ_r/Z − 1| ≤ 2·TV(π, π₀), free of T and N_e (queued rider SAMP-R1), which is small only
  without leakage. A bound of order T/N_e under leakage is step 4 above, i.e. not cheap.
