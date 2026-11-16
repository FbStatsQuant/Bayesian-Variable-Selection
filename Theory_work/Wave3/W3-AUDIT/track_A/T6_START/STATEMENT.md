# T6 · Lemma START-X (the start sampler and its normaliser are exact) — STATEMENT v1 (draft, not locked)

Track A item T6 (`AUDIT.md` §6; CHECKPOINT_1 annex order 6). Tier B (second-seat re-check of N9 Claims S and Z against
the code of record). **Lean target: yes** (algorithm level: backward sampling from a (block, size) convolution table is
exact for a block-product weight under a global size cap; finite). Blocks rows 3.5, 3.6.

## Source of the premise
- "**START** `draw_pi0` returns exact π₀ draws and the reported Z̄₀ = Σ_Ω γ₀ (N9 Claims S, Z; status PROVED
  (candidate))" (`Theory_work/Wave1/W1-N1/STATEMENT.md:75`); T12's START also asks that "the independence proposals use
  the same exact sampler" (`Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md:48`).
- N9: Claims Z and S with proofs (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/PROOF.md:247-292`),
  verdict rows 7–8 "PROVED (candidate)", code-checked at commit 39db138
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/REPORT.md:23-24`); the report asks for "an
  independent line-by-line review … especially the telescoping in Claim S" (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/REPORT.md:65-66`).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core). `cpp/v3_start.h` lines 1–177 (tables, start object,
`build_tables`, `build_start`, `draw_pi0`) are identical at 39db138 and at the pin (`git diff 39db138 4676af6 --
cpp/v3_start.h` has its first hunk at line 178, after `draw_pi0`).

## Setting
The `Start` object `st` of T4 (ENC) on a run that reaches the islands: blocks C₁, …, C_J = C(X) (T2), K, ϖ(k) = e^{λ(k)},
r_b(U) = e^{ρ_b(U)} > 0 for every U ⊆ C_b. γ₀(S) := ϖ(|S|)∏_b r_b(S ∩ C_b) on Ω = {S ⊆ [p] : |S| ≤ K};
Z̄₀ := Σ_Ω γ₀; π₀ := γ₀/Z̄₀. EX-A (exact arithmetic) and H-U (the uniforms read by `draw_pi0` are i.i.d. U[0, 1)).

## Lemma START-X
- **(Z)** `st.logZbar0` = log Z̄₀ (`cpp/v3_start.h:133-135`), and this value is the reported normaliser: it initialises
  every island's log Ẑ (`cpp/v3_engine.h:299`) and is the fit's `log_Zbar0` (`v3_fit.R:140`; `v3_run.R:217`).
- **(S)** Each call `draw_pi0(st, vs, S)` returns S ∈ Ω with P(S = A) = π₀(A) for every A ∈ Ω, and consumes a number of
  uniforms that is a function of the returned draw (1 for the size, one per block visited, one per nonempty block).
- **(S′)** Every π₀ draw of the method — initial draws (`draw_start`, `cpp/v3_engine.h:289`) and independence proposals
  (`cpp/v3_engine.h:184`) — is this call on the same `st` (`cpp/v3_engine.h:108`).

## Not claimed
- Binary64 (N9 §5: categorical cumulatives of doubles, 2⁻⁵³ grid; quantified there, not re-checked here).
- That successive draws are independent: that is CC4 of `W3-SAMP:CC` (strong Markov property of the i.i.d. stream),
  "CODE-CHECKED".

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (re-states N9 rows 7–8 for the pin) | track A T6 | `AUDIT.md` §6 T6 | `CHECK.md` |
