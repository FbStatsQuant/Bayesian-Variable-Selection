# T3 · Lemma OPC (OP-LS0: LS0 runs as specified on every completed sampler run) — STATEMENT v1 (draft, not locked)

Track A item T3 (`AUDIT.md` §6; CHECKPOINT_1 annex order 3). Tier B (re-check of `W1-GEN:L5` [OP] against the code of
record; no key lemma). **Lean target: no** (code fact). Blocks row 3.1.

## Source of the premise
- OP-LS0 as named: "**OP-LS0** LS0 integrated as specified (METHOD §2 #8)"; same line "**complete scans** no operational
  interruption of any search" (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86`).
- LS0 as specified (`Theory_work/State_of_Project/sections/02_method.tex:490-499`): after the final local search, one
  local search with the §6.10 rules from the start mode; "LS0 reads no uniforms. Every model it scores joins the
  all-scored set and the stores." Local-search rules: `Theory_work/Wave1C/C-GROW/STATEMENT.md:68-71`.
- As used in row 3.1 (`W3-RM:RM-0`, `W3-RM2:RM2-R`): "every successfully completed SMC output run in this configuration
  executes LS0 from `start_mode(...).S`" with the shipped options (`Theory_work/Wave3/W3-RM/STATEMENT.md:58-63`), and
  𝒦_n := "the deterministic LS0 (complete scans, cap ℓ_n + |S̃₀|) started from the coded start mode scores S₀ (a data
  event: LS0 reads no uniforms)" (`Theory_work/Wave3/W3-RM/STATEMENT.md:53-54`), giving
  𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ (`Theory_work/Wave3/W3-RM/STATEMENT.md:168-169`).
- Existing proof: `W1-GEN:L5` [OP], "PROVED (by this seat, unchecked)" (`Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md:11-16`).

## Code of record and configuration
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); paths relative to it. Shipped configuration: `v3_fit`
with `ls0 = TRUE` and the options `v3.ls0_ell`, `v3.ls0_tie_dp`, `v3.ls0_cap` unset (`v3_fit.R:73`; `v3_run.R:93-102`).
ℓ_n := ⌈log₂(n + p + 1)⌉ (`v3_preprocess.R:23`).

## Definitions
- **The abstract search** LS(c, ℓ) (C-GROW's rules): from a centre c ∈ Ω, a *scan* evaluates every feasible flip
  (deletion of j ∈ c; addition of j ∉ c only if |c| < K) and every swap (j ∈ c, l ∉ c); the best scanned neighbour has
  the largest F, exact F-ties broken by the lexicographically smallest index list; a *move* goes to it iff its F is
  strictly larger than F(c); after ℓ moves one further scan is made and the search stops; it stops earlier at the first
  scan with no strict improvement. Scored(c, ℓ) := c together with every model scanned. Both are functions of
  (X, y) given c, since they use only F = log ϖ(|·|) + log m(·), K and p.
- **The coded start mode** S̃₀ := `start_mode(st, 1000000, true).S` (`cpp/v3_start.h:271`), with `st` built from the
  partition C(X) of T2 (BLK).
- 𝒪, the potential fit P° and its output event 𝒪°: as in T1 (GW), `T1_GW/STATEMENT.md`. 𝓜 := the set of models offered
  to the final run's ledger (`W3-SAMP:CC` CC2).

## Lemma OPC
Assume EX-A. For every valid input on the sampler branch, in the shipped configuration, for the actual fit and for P°
alike, on {final-run status = "completed"} (so on 𝒪 and on 𝒪° restricted to the sampler branch):
- **(OPC-a) LS0 runs.** After the final local search, `cpp_final_run` computes S̃₀ and executes exactly one
  `local_search` from centre S̃₀, with the centre scored and emitted, and move cap ℓ_n + |S̃₀|.
- **(OPC-b) It is the abstract search, run to its own end.** That call reads no uniform, is not interrupted, and
  evaluates exactly the models of Scored(S̃₀, ℓ_n + |S̃₀|), in the order of LS(S̃₀, ℓ_n + |S̃₀|).
- **(OPC-c) Its models enter the final comparison.** Scored(S̃₀, ℓ_n + |S̃₀|) ⊆ 𝓜, and the reported HPM Ŝ⁺ is the
  `hpm_better`-maximum of 𝓜 (larger F, then smaller size, then lexicographic).
- **(OPC-d) Operational closure ([OP] of `W1-GEN:L5`).** Hence, on {status = "completed"},
  {S₀ ∈ Scored(S̃₀, ℓ_n + |S̃₀|)} ⊆ {S₀ ∈ 𝓜}, and on {S₀ ∈ 𝓜} ∩ {π(S₀) > ½}, Ŝ⁺ = S₀. In particular
  𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ on the sampler branch, with 𝒦_n := {S₀ ∈ Scored(S̃₀, ℓ_n + |S̃₀|)}, a function of
  (X, y) only.

## Not claimed
- That S̃₀ maximises γ₀ (that is `W3-RM:E4`, "PROVED-CHECKED", conditional on N3 (H1) strengthened = T4 ENC, and (H4)).
- The enumeration branch (no LS0 there; it scores every feasible model — `Theory_work/Wave3/W3-RM/STATEMENT.md:62-63`).
- Non-default options (`v3.ls0_ell`, `v3.ls0_tie_dp = FALSE`, `v3.ls0_cap = "ell_n"`, `ls0 = FALSE`); R′ > 4 (not in the
  core at the pin: `islands = 4L`, `v3_run.R:91`).
- Binary64 (EX-A).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (restates [OP] + OP-LS0 for the code of record) | track A T3 | `AUDIT.md` §6 T3 | `CHECK.md` |
