# L1 — Lemma LIST-K (deterministic list algebra) — proof

Claim: STATEMENT.md (C1), §2. Status: proof by the lead, not yet line-checked. Written for a Lean transcription:
finite sums over a finite set, real arithmetic, one inequality for log; no measure theory.

## Setting (all deterministic)
Ω is a finite set of models (subsets of [p] := {1, …, p}); F : Ω → ℝ (real-valued: (C1)'s hypothesis; STATEMENT §1 defines
F = log ϖ + log m, finite on Ω) [LC1-12]; w(S) := e^{F(S)} > 0; Z := Σ_{S∈Ω} w(S) ∈ (0, ∞).
π(S) := w(S)/Z; for 𝒜 ⊆ Ω, π(𝒜) := Σ_{S∈𝒜} π(S); PIP_j := π(𝒜_j) with 𝒜_j := {S ∈ Ω : j ∈ S}; MPM := {j ∈ [p] : PIP_j > ½}.
𝒯 ⊆ Ω with S₀ ∈ 𝒯 (so S₀ ∈ Ω). Z_𝒯 := Σ_{S∈𝒯} w(S); π_𝒯(S) := w(S)/Z_𝒯 for S ∈ 𝒯; for ℬ ⊆ 𝒯, π_𝒯(ℬ) := Σ_{S∈ℬ} π_𝒯(S);
pip_𝒯(j) := π_𝒯(𝒜_j ∩ 𝒯); mpm_𝒯 := {j ∈ [p] : pip_𝒯(j) > ½}; logZ_𝒯 := log Z_𝒯; ε := 1 − π(S₀). Write m := π(𝒯).

## Step 0 (elementary facts)
(0.1) Z_𝒯 ≥ w(S₀) > 0, so π_𝒯 is well defined, π_𝒯 ≥ 0 and π_𝒯(𝒯) = 1.
(0.2) Z_𝒯 = Σ_{S∈𝒯} Z·π(S) = Z·m, hence m = Z_𝒯/Z ∈ (0, 1] (𝒯 ⊆ Ω, all terms positive) and π_𝒯(S) = π(S)/m for S ∈ 𝒯.
(0.3) π(S₀) ≤ m ≤ 1 (S₀ ∈ 𝒯); hence 1 − m ≤ ε, and ε < 1 because π(S₀) > 0.
(0.4) π_𝒯(S₀) = π(S₀)/m ≥ π(S₀) (by (0.2), (0.3)); hence 1 − π_𝒯(S₀) ≤ ε.
(0.5) If 𝒯 = Ω, then m = 1 and π_Ω = π (by (0.2)); so pip_Ω(j) = π(𝒜_j) = PIP_j, mpm_Ω = MPM and Z_Ω = Z [LC1-12].

## (a)
Fix j ∈ [p]. Always 0 ≤ pip_𝒯(j) ≤ π_𝒯(𝒯) = 1.
- If j ∈ S₀: S₀ ∈ 𝒜_j ∩ 𝒯, so pip_𝒯(j) ≥ π_𝒯(S₀), and |pip_𝒯(j) − 1| = 1 − pip_𝒯(j) ≤ 1 − π_𝒯(S₀).
- If j ∉ S₀: 𝒜_j ∩ 𝒯 ⊆ 𝒯 ∖ {S₀}, so pip_𝒯(j) ≤ π_𝒯(𝒯) − π_𝒯(S₀) = 1 − π_𝒯(S₀), and |pip_𝒯(j) − 0| ≤ 1 − π_𝒯(S₀).
Taking the maximum over j ∈ [p] and using (0.4): max_j |pip_𝒯(j) − 1{j ∈ S₀}| ≤ 1 − π_𝒯(S₀) ≤ ε. ∎(a)

## (b)
Fix 𝒜 ⊆ Ω and put a := π(𝒜 ∩ 𝒯), b := π(𝒜 ∖ 𝒯). Then π(𝒜) = a + b and, by (0.2), π_𝒯(𝒜 ∩ 𝒯) = a/m. So
  D(𝒜) := π_𝒯(𝒜 ∩ 𝒯) − π(𝒜) = a(1 − m)/m − b.
Since 0 ≤ a ≤ m: 0 ≤ a(1 − m)/m ≤ 1 − m. Since 0 ≤ b ≤ π(Ω ∖ 𝒯) = 1 − m: −(1 − m) ≤ −b ≤ 0. Adding,
−(1 − m) ≤ D(𝒜) ≤ 1 − m, i.e. |D(𝒜)| ≤ 1 − m for every 𝒜 ⊆ Ω.
*Attainment.* For 𝒜 = Ω ∖ 𝒯: a = 0, b = 1 − m, so |D(𝒜)| = 1 − m. Hence sup_{𝒜⊆Ω} |D(𝒜)| = 1 − m (a maximum over the
finite power set of Ω), and 1 − m ≤ ε by (0.3).
*PIPs.* For 𝒜 = 𝒜_j: π_𝒯(𝒜_j ∩ 𝒯) = pip_𝒯(j) and π(𝒜_j) = PIP_j; so |pip_𝒯(j) − PIP_j| ≤ 1 − m ≤ ε for every j. ∎(b)

## (c)
Assume ε < ½. By (0.4), π_𝒯(S₀) ≥ π(S₀) = 1 − ε > ½.
- j ∈ S₀: pip_𝒯(j) ≥ π_𝒯(S₀) > ½ (proof of (a)), so j ∈ mpm_𝒯.
- j ∉ S₀: pip_𝒯(j) ≤ 1 − π_𝒯(S₀) < ½ (proof of (a)), so j ∉ mpm_𝒯.
Hence mpm_𝒯 = S₀ (both are subsets of [p]; S₀ ⊆ [p] because S₀ ∈ Ω). The same argument with 𝒯 = Ω (allowed: S₀ ∈ Ω),
where pip_Ω = PIP and mpm_Ω = MPM by (0.5), gives MPM = S₀. ∎(c)

## (d)
By (0.2), logZ_𝒯 = log(Z·m) = log Z + log m. By (0.3), log π(S₀) ≤ log m ≤ 0, i.e.
log Z + log(1 − ε) ≤ logZ_𝒯 ≤ log Z, and 0 ≤ log Z − logZ_𝒯 = −log m ≤ −log(1 − ε). For 0 ≤ ε < 1 (always, by (0.3)),
−log(1 − ε) = log(1 + ε/(1 − ε)) ≤ ε/(1 − ε), by log(1 + x) ≤ x for x ≥ 0. ∎(d)
*Corollary used in L3.* If ε ≤ t < ½ then |logZ_𝒯 − log Z| ≤ ε/(1 − ε) ≤ 2ε ≤ 2t (since 1 − ε > ½).

## (e)
For 𝒯 = Ω the identities are (0.5). Then (a) and (c) at 𝒯 = Ω
read max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π_Ω(S₀) = ε and, if ε < ½, MPM = S₀. ∎(e)

## Remarks for the checker
- Nothing uses the structure of Ω (any finite set of subsets of [p]) or of F (any real function). The lemma is applied in
  L3 with Ω = {S ⊆ [p_ret] : |S| ≤ K} and F the coded score.
- The strict rule "> ½" matters only in (c); (c) needs ε < ½ strictly (SL1-2: with masses (0.3, 0.5, 0.2) on
  {∅, {1}, {2}} and S₀ = {1}, MPM = ∅ ≠ S₀ at ε = ½).
- Falsification: `numerics/listk_check.py` → `numerics/listk_check_out.txt` (20 000 random cases; every inequality,
  and the identity sup|D| = 1 − m by brute force over all 𝒜 when |Ω| ≤ 12).
