# K1 / K2 disposition (lead) — blind lemma line checks by Sol

Reviews: `K1_RM_check_sol.md` (R_reduction.md, M_misr.md) and `K2_G_check_sol.md` (G_corollaries.md), both
gpt-6.1-sol, reasoningEffort high, blind (briefs `BRIEF_K1_sol.md`, `BRIEF_K2_sol.md`), on STATEMENT v1.2.

| review | per-item verdicts | findings |
|---|---|---|
| K1 | R′(a), (a′), (a″), (b), (c), table R.6, MIS(i) (with consequences and stability), MIS(i′)(c), MIS(ii)(a), (b), (c): VERIFIED; MIS(i′)(a), (b), (d): VERIFIED-WITH-AMENDMENTS | 0 FATAL / 0 MAJOR / 1 MINOR / 0 NIT |
| K2 | G(a), H(a), H(b), reference law, Remark SNR, Remark P (MIS(i); MIS(ii), (ii′); Theorem F with F(a), F(b); example), Remark U: VERIFIED; G(b): VERIFIED-WITH-AMENDMENTS | 0 FATAL / 0 MAJOR / 2 MINOR / 0 NIT |

| # | grade | finding | disposition | where |
|---|---|---|---|---|
| K1-1 | MINOR | The input ledger (I1)–(I6) of M.2 names G, (E), (F₀) but not the per-n size conditions of R1 under which the sources state (I2)–(I5). | **Applied.** A standing assumption (s₀ = s ≥ 1, A ≥ 1 fixed; 2 ≤ p ≤ n^A; s₀ ≤ K; σ*² = 1) now precedes the ledger, with the remark that R1's asymptotic part enters only through the thresholds. No change to any bound. | `lemmas/M_misr.md` M.2, before (I1) |
| K2-1 | MINOR | G(b)'s status omitted its dependency on W3-POST2:A0 (the bridge (F_w) ⇒ (OS)). | **Applied.** Status of G(b): "conditional on W3-POST2:C, W3-POST2:A0". | `lemmas/G_corollaries.md` status lines |
| K2-2 | MINOR | G.2 step 2 attached the probability 1 − 2k_n n⁻² to the standardised bounds, which also need the SD event of step 1. | **Applied.** Step 2 is now the raw event λ_min(W_TᵀW_T) ≥ c_popN/2; the standardised bounds are derived on its intersection with step 1; 𝒜_n is defined from the SD, raw-eigenvalue and energy events; the union bound is unchanged. The threshold n* now also names n_OS, n_BM and the n₀ of MIS-R (i) (K2, §G.2 last paragraph). | `lemmas/G_corollaries.md` G.2 |

Also done after the checks (bookkeeping, no mathematical content): the status headers of `M_misr.md` and
`G_corollaries.md` are now one line per claim, so that each registry status is a verbatim single-line quotation.
Points the reviewers made without a finding, recorded for the council: (K1, M.1) the bounds for HPM hold for any
measurable tie rule through {HPM ≠ S₀} ⊆ {δ ≥ ½}; the stability clause is applied to the posterior functional
1{δ ≥ ½}. (K2, G.5) the synthetic C-MIS instances used in Remark P have zero omitted contribution or zero full-model
candidate coefficient, which C-MIS allows (τ² = 0).
