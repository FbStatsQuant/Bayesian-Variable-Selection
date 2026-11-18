# T8 · Lemma OVL — PROOF v4

## (OVL-a)
On 𝒜° the uninterrupted final run uses the frozen N_e = `b$tiers$N[tier + 1]` ∈ {N₀, 4N₀}, N₀ = max(2500, n, p), and L = `b$L` =
max(4, ⌈log₂(n + 1)⌉) (`Scripts/SMC_BVS/core/v3_run.R:88-92`; `Scripts/SMC_BVS/core/v3_preprocess.R:24-25, 30`; T5
CAL-c), and the frozen grid has T ≥ 1 intervals (`v3_final_run` checks it, `Scripts/SMC_BVS/core/v3_run.R:225`, with
`v3_check_grid`, `Scripts/SMC_BVS/core/v3_run.R:77-81`: length ≥ 2, from 0 to 1). So D_r = N_e(1 + T + L + 4) ≥ N₀(L + 6) ≥ n·10. This is the production corollary of `W3-SAMP:D` (D-iii)
(`Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:53-54`), read on 𝒜° (its proof uses only the budgets and T ≥ 1).

## (OVL-b)
Fix c > 0 and take n with 10n ≥ 2c. On 𝒜° ∩ {π₀(S₀) > ½}, D_r·π₀(S₀) > 10n/2 ≥ c by (OVL-a). Hence
𝒜° ∩ {D_rπ₀(S₀) ≤ c} ⊆ 𝒜° ∩ {π₀(S₀) ≤ ½}. Since o₀ = δ₀/(1 − δ₀) is increasing in δ₀ = 1 − π₀(S₀) and equals 1 at δ₀ = ½
(o₀ := ∞ at δ₀ = 1, and 1_𝒜°·o₀ := 0 off 𝒜°), {π₀(S₀) ≤ ½} = {o₀ ≥ 1}, so P(𝒜° ∩ {π₀(S₀) ≤ ½}) = P(1_𝒜°·o₀ ≥ 1) → 0 by P-START on 𝒜°. Thus
P(𝒜° ∩ {D_rπ₀(S₀) ≤ c}) → 0 for every c > 0, which is P-OVL's equivalent form (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:82-83`)
with 𝒜°. On 𝒜 the actual (N_e, T, L), hence D_r, equal the potential ones (T5 CAL-d), and 𝒜 ⊆ 𝒜°, so the probabilities
with 𝒜 are smaller. ∎

## (OVL-c)
`W3-START2-R:IF-START`: "for every event 𝒜 … 1_𝒜o₀ = O_P(r_n) … r_n → 0" (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`),
so P-START holds with 𝒜° under its hypotheses, which include (A5) (defined in the STATEMENT). The OVL route is quoted,
not re-proved.

## (OVL-d) the uninterrupted run
(i) π₀ is built in `cpp_setup` from (X, y) only, with no stream and no check (T4, T5 CAL-a), so o₀ = δ₀/(1 − δ₀) is a
function of (X, y), the same in the actual and the uninterrupted run. IF-START's interface proof reads "0 ≤ 1_𝒜o₀ ≤ o₀,
so 1_𝒜o₀ = O_P(r_n) … this is P-START" (`Theory_work/Wave3/W3-START/lemmas/L10_INTERFACES.md:14-15`; carried to
IF-START⁺⁺ with the rates of `Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`): it holds for every event, in
particular 𝒜°, which is measurable (T5 CAL-b). (ii) (OVL-a)–(OVL-b) are stated and proved on 𝒜° with the uninterrupted
run's frozen (N_e, T, L) (T5 CAL-c). Without (A5): `W3-START2-R:OVL` gives P(π₀(S₀) ≥ n^{−E_n−ε}) → 1 with no event, and on
𝒜° D_r ≥ max(2500, n, p)(L + 6) ≥ max(n, p)·log₂(n + 1) (since L + 6 > log₂(n + 1)), so the production form
max(n, p)·log₂(n + 1)·π₀(S₀) → ∞ gives P-OVL with 𝒜°. ∎

## Consequence for (D-iv)
(v4: council R1, Sol #2. W3-SAMP's (D-iii) integrates D-i over the actual 𝒜, which the T1/T5 correction does not allow,
because the actual 𝒜 depends on the clock. The bound is re-derived on the uninterrupted run.)

*Pathwise inclusion.* Let S† be the `hpm_better`-maximum of Ω and fix r ≤ 4. On {completed} = 𝒪 (sampler branch):
𝒪 ⊆ 𝒜 ⊆ 𝒜° (T1 GW-iv); the statistical record equals the uninterrupted one (T1 GW-iii), so island r's evaluated set
𝓜_r equals 𝓜°_r, the set evaluated by the uninterrupted island r (`W3-SAMP:PC` (i)); and Ŝ is the `hpm_better`-maximum of
the final ledger's set 𝓜 ⊇ 𝓜_r with 𝓜 ⊆ Ω (`W3-SAMP:PC` (iii); CC2, CC5). If S† = S₀ and S₀ ∈ 𝓜, then Ŝ = S₀
(`Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:40-42`). Hence
completed ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜° ∩ {S₀ ∉ 𝓜°_r}).

*Probability.* D-i (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:99-100`) is a statement about the potential island given
𝓒 on the success event; by T5 (CAL-b) it holds for the pair (𝒜°, 𝓒°): P(S₀ ∉ 𝓜°_r | data, 𝓒°) ≤ (1 − π₀(S₀))^{D_r} on
𝒜°, with D_r the frozen budget (a function of 𝓒°, T5 CAL-c). Since 𝒜° ∈ σ(𝓒°), integrating gives
P(𝒜° ∩ {S₀ ∉ 𝓜°_r}) ≤ E[1_𝒜°(1 − π₀(S₀))^{D_r}]. So
P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜°(1 − π₀(S₀))^{D_r}],
with no premise on the clock. Then (1 − x)^D ≤ e^{−Dx}, and E[1_𝒜°·e^{−D_rπ₀(S₀)}] ≤ e^{−c} + P(𝒜° ∩ {D_rπ₀(S₀) ≤ c})
for every c > 0, which → 0 under (OVL-b); P(S† ≠ S₀) → 0 under P-MAP. ∎
