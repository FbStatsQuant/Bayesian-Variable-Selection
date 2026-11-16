# T8 · Lemma OVL — PROOF v1

## (OVL-a)
On 𝒜° the final run executes N_e = `b$tiers$N[tier + 1]` ∈ {N₀, 4N₀}, N₀ = max(2500, n, p), and L = `b$L` =
max(4, ⌈log₂(n + 1)⌉) (`Scripts/SMC_BVS/core/v3_run.R:88-92`; `Scripts/SMC_BVS/core/v3_preprocess.R:24-25, 30`; T5
CAL-c), and the frozen grid has T ≥ 1 intervals (`v3_check_grid`, `Scripts/SMC_BVS/core/v3_run.R:77-81`: length ≥ 2,
from 0 to 1). So D_r = N_e(1 + T + L + 4) ≥ N₀(L + 6) ≥ n·10. This is the production corollary of `W3-SAMP:D` (D-iii)
(`Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:53-54`), read on 𝒜° (its proof uses only the budgets and T ≥ 1).

## (OVL-b)
Fix c > 0 and take n with 10n ≥ 2c. On 𝒜° ∩ {π₀(S₀) > ½}, D_r·π₀(S₀) > 10n/2 ≥ c by (OVL-a). Hence
𝒜° ∩ {D_rπ₀(S₀) ≤ c} ⊆ 𝒜° ∩ {π₀(S₀) ≤ ½}. Since o₀ = δ₀/(1 − δ₀) is increasing in δ₀ = 1 − π₀(S₀) and equals 1 at δ₀ = ½
(o₀ := ∞ at δ₀ = 1), {π₀(S₀) ≤ ½} = {o₀ ≥ 1}, so P(𝒜° ∩ {π₀(S₀) ≤ ½}) = P(1_𝒜°·o₀ ≥ 1) → 0 by P-START on 𝒜°. Thus
P(𝒜° ∩ {D_rπ₀(S₀) ≤ c}) → 0 for every c > 0, which is P-OVL's equivalent form (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:82-83`)
with 𝒜°; for 𝒜 ⊆ 𝒜° the probabilities are smaller. ∎

## (OVL-c)
`W3-START2-R:IF-START`: "for every event 𝒜 … 1_𝒜o₀ = O_P(r_n) … r_n → 0" (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`),
so P-START holds with 𝒜° under its hypotheses, which include (A5) (AUDIT.md §6 correction 2). The OVL route is quoted,
not re-proved.

## Consequence for (D-iv)
(D-iii): P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) + E[1_𝒜(1 − π₀(S₀))^{D_r}] (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:102-103`);
1_𝒜 ≤ 1_𝒜°; (1 − x)^D ≤ e^{−Dx}; and E[1_𝒜°·e^{−D_rπ₀(S₀)}] ≤ e^{−c} + P(𝒜° ∩ {D_rπ₀(S₀) ≤ c}) for every c, so it → 0
under (OVL-b). ∎
