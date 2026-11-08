# Repair of Theorem R's display (PROOF §1) and the exact-branch convention — from reviewer R14

Status: repair by this seat (wording largely proposed by R14); XF VERIFIED WITH MINOR FIXES (R21), fixes applied — v2, 2026-11-08.
PX = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md`; W7 = `.../W7-PART/PROOF.md`.

## 1. Theorem R display (R14 #1, ERROR; R14 #5, MINOR)
PX:79-84 asserted, for every t ∈ (ψ̄, ρ), P(𝒜_nᶜ) ≤ S(t) ≤ K_n, with S(t) the pair-tail sum and K_n the closed form; the
second inequality is false for t near ρ (R14: n = 10⁴, p = 90, t = .6999: one within-pair term ≈ .49 ≫ K_n ≈ 6.9·10⁻⁴⁹).
**Repaired Theorem R.** Under (SIZE) at n and n ≥ 5:
(R-a) for every t ∈ (ψ̄, ρ): P(𝒜_nᶜ) ≤ S(t) := Σ_{within} P_ρ(|r̂| ≤ t) + Σ_{cross} P_{|Σ_jk|}(|r̂| ≥ t);
(R-b) with t = t*: P(𝒜_nᶜ) ≤ S(t*) ≤ K_n := (2/(√π(1−ρ))) p²√n e^{−(n−4)I*}.
(R-c) For every fixed A ≥ 1, C > 0: P(𝒜_nᶜ) ≤ p^{−C} once n ≥ max(5, n₁) and (n−4)I* ≥ log(2/(√π(1−ρ))) + ((2+C)A + ½) log n;
and P(𝒜_nᶜ) ≤ (2/(√π(1−ρ))) e^{4I*} n^{2A+½} e^{−nI*}, which is summable in n with no lower growth bound on p.
R14 verified: Hotelling's density (W7:209), Lemma 2 steps 1–6, Corollary B's t*, I* and constant 2/(√π(1−ρ)), the
polynomial corollary. **Hence D2 is resolved: the explicit constant of (R) is VERIFIED (R14)**, conditional on this split.
The fallback (R′) of `lemmas/CR_corr_tails.md` (XF VERIFIED, R19) is kept as an independent, cruder route.
PX:98-100: the number "≈ 0.17" is not the displayed bound (which is ≈ 1.13·10⁶, vacuous, at (200, 500, ρ = .7, ψ̄ = .5));
delete it or label it as W7's finer bound with its source.

## 2. W7 Theorem A, A0(c) (R14 #2) — no change to the use
A0(c) as written is false for groups already absorbed into a full union (also noted by A-REV6/PARTITION.md:47). The use
here needs only: under the strict global margin (every within |r̂| > t > every cross |r̂|), every distance inside an
unfinished group is below every distance between different groups, so until all groups are complete an internal merge is
available and every cross merge loses; hence each group is a node of the dendrogram, and g_max ≤ B < 2g_min makes the
top-down cut retain exactly those nodes and next-fit pack each alone (R14 #2, direct argument; ties inside either class
allowed). A2 is not used.

## 3. Exact-branch convention (R14 #3)
The production dispatch (core/v3_preprocess.R:18-32; core/cpp/v3_core.cpp:69-81; core/v3_fit.R:93-106) runs exact
enumeration when Σ_{k≤K} C(p,k) ≤ (5H₀+4N₀)p, which can hold for p ≥ 18 when p_n grows very slowly (e.g. p_n = g⌈log₂log₂(n+4)⌉);
then no partition or block start is built. The locked statement allows such sequences and must not acquire a lower growth
bound on p. **Convention adopted.** In STATEMENT §2, "blocks", π₀, S̃₀ and "LS0 of R̄⁺" denote the deterministic
make_blocks / block-table / start-mode / local-search objects computed from the data on **every** branch (hypothetical when
the actual run takes the exact branch). (R), (S), (E), (T) are statements about these data functions and hold as proved
(no step uses the branch). For (C) (cases, every n; R21 #1): (a) for n with s₀ ≤ K, on the exact branch the run scores all of Ω (status exact ∈ 𝒪
under EX-A; core/cpp/v3_core.cpp:504-524), so S₀ ∈ 𝒮̄ and 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ∩ {exact branch} = ∅; on the SMC branch 𝒮̄⁺ ⊇ 𝒮_LS0;
(b) for n with s₀ > K, S₀ ∉ Ω, every feasible LS0 fails to score S₀, so the inclusion into {LS0 of R̄⁺ does not score S₀}
holds trivially, and π(S₀) := 0 (zero extension) makes the posterior term trivial; the composition inequality therefore holds for every n with D_n ≤ P(LS0 of R̄⁺ does not score S₀) (= 1 when s₀ > K), and,
for n with s₀ ≤ K only (R30 #1), with the sharper D_n ≤ P(SMC branch, LS0 of R̄⁺ does not score S₀), with no execution of LS0 needed on the exact branch (OP-LS0's requirement is
then vacuous for the conclusion). On that branch Ŝ⁺ is the global HPM S†, and the posterior term covers it.
