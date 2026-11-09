# L6 — Lemma ENUM: the exact-enumeration override (v2, after council round 2)

Status: **PROVED (by this seat, unchecked)**; added after council round 1 (C1 Sol issue 1); restated in v2 with the coded
inequality as the general condition (C2 Sol issue 1, C2 Opus issue 1). Checked by the round-2 council seats (C2 Sol:
"the new ENUM proof is correct"; C2 Opus: "correct and matches the production code"); council r3: both seats re-derived ENUM, all gates PASS (C3_council_*.md).

**Code facts.** After preprocessing (retained columns; for iid Gaussian columns no column is constant or duplicated,
almost surely, so p is the design's p a.s.), the production core decides the branch by the counting inequality
  (EXB)  Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)p,  N₀ = max(2500, n, p),  H₀ = ⌈512N₀/2500⌉,  K = min(p, ⌊n/2⌋)
(`Scripts/SMC_BVS/core/v3_preprocess.R:18-27`, counted by `cpp_exact_count`). On the exact branch it enumerates Ω,
scores every model and reports the maximiser of the all-scored set for the strict order (F, −|S|, lex), with provenance
`phase = exact, mechanism = enumeration`, and returns before LS0 (`Scripts/SMC_BVS/core/v3_fit.R:120-125`). Status
`exact` is part of the output event 𝒪 (FIN `s1_setting.tex:24`); a `resource_limit` stop on the exact branch is "no output"
(U_n) and does not affect the lemma, which is stated jointly with 𝒪 [C3-Opus-7].

**Lemma ENUM.** (i) **General override.** For any design sequence for which (EXB) holds for all large n (a condition
on (n, p_n) only), under EX-A: if 1 − π(S₀) < ½ then Ŝ⁺ = S₀ whenever the enumeration returns with output. Hence,
whenever POST's conclusion 1 − π(S₀) = o_P(1) holds under the joint law, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). (ii) **Sufficient conditions for (EXB).** (EXB) holds whenever
2^{p_n} ≤ 4n·p_n, i.e. p_n − log₂ p_n ≤ log₂ n + 2; in particular for every fixed p, for p_n ≤ c log n with c < 1/log 2,
and for 2^{p_n} ≤ n (e.g. p_n = 2⌊log n/(2 log 2)⌋, C2 Sol's example).

*Proof.* (ii) Σ_{k≤K}C(p,k) ≤ 2^p and (5H₀ + 4N₀)p ≥ 4N₀p ≥ 4np. For fixed p, 2^p ≤ 4np for n ≥ 2^p/4; for
p_n ≤ c log n, 2^{p_n} ≤ n^{c log 2} ≤ n eventually. (i) If 1 − π(S₀) < ½, S₀ is the unique maximiser of π, i.e.
F(S₀) > F(S) for every S ∈ Ω ∖ {S₀} (SL0(iv)); every model is scored, so the maximum of the all-scored set under
(F, −|S|, lex) is S₀. Thus 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {1 − π(S₀) ≥ ½} on the exact branch, and P(1 − π(S₀) ≥ ½) → 0. The liminf
identity is the algebra of FIN §5.1 (M5(0) with D_n = 0). ∎

**Effect on the map.** Every family row's reported-model status is "covered" for sequences on which (EXB) holds
eventually (given POST's hypotheses); the "unproved" and "route-obstructed" labels refer only to sequences on which
(EXB) fails infinitely often (for which necessarily 2^{p_n} > 4np_n, i.e. p_n ≥ log₂ n roughly, along those n).
LS0 and enumeration are different mechanisms: "LOC-B does not apply" ≠ "reported model unproved".
