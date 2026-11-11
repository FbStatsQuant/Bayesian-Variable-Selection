# C1 disposition — council round 1, 2026-11-09

| Seat | Score | Gates G1–G6 | Blocking |
|---|---|---|---|
| gpt-6-astra (high), `C1_council_astra.md` | **9.1** | all PASS | none |
| Claude Opus 5.5 (high, claudeAgent), `C1_council_opus.md` | **8.8** | all PASS | none |

**Council PASSED in round 1** (both ≥ 8.0, all six gates PASS in the same round). Non-blocking items, all applied after the
vote (no claim changed; no re-vote needed under the protocol):
[HQ correction 2026-11-11: inaccurate. Several of the edits below are substantive (PC conclusion, D premise list,
LT-b display, among others). They were verified after the fact by `PC1_postcouncil_diff_sol.md`. The C1 scores are votes on
the pre-edit text.]

| Item | Disposition |
|---|---|
| Opus #1 PC scope vs 𝓜_r | PC(i) now includes 𝓜_r (STATEMENT; `PC_completed.md`). |
| Opus #2 D omits KERNEL | KERNEL added to D's premises (control-flow clause of Lemma B only). |
| Opus #3 TR-b endpoint slip | Endpoint bound derived from (TR-a) applied to K₁^{L+q} directly (`TR_theorem.md`). |
| Opus #4 stale status lines | All lemma headers updated to the final status; STATEMENT v3 references. |
| Opus #5 𝒜 in code terms | 𝒜 = {SMC branch and calibration status "ok", fallback included} (`v3_calib.R:144-183`, `v3_fit.R:154`). |
| Opus #6 wording | "no condition on 𝓒 beyond 𝒜"; {κ₀ > ε/3} ⊆ {o₁ > ε/3} made explicit. |
| Opus #7 joint-law idealisation | Final streams independent of the data stated in §0. |
| Opus #8 constant 19 vs B | LT-b states λ₀ ≤ (B+3)o₁ ≤ 19o₁; g ≤ (B+5)o₁ ≤ 21o₁. |
| Opus #9 TR non-nesting converse | Abstract converse example added (`TR_theorem.md`). |
| Astra #1 LT-b numerics label | LT-b displayed with exact λ₀ before the relaxation; numerics cells relabelled (LT file, README). |
| Astra #2 C-ii indexing | V_{−1} := 0, V_t := Σ_{v≤t}x_v defined (`C_theorem.md`). |
