# BT2 disposition (lead) — better-theorem review on the final statement v1.4 (Codex gpt-6-astra high, blind)

Review: `BT2_better_theorem_astra.md`, manifest 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd
(quoted). Result: **5 ADOPT NOW, 2 WORTH A TICKET, 0 SPECULATIVE**; twelve directions examined with no credible
improvement (b ≥ ½ for the reporting theorems; removing (W); the bounded-gap regime; the count n^{15ρ}; the
conditioning size 15; a sharp Gaussian-row leak frontier; α ≤ 2 in the examples; the equicorrelated group beyond
3/8; a rate for the reported-model event; removing T1/POST, floors or visibility; the Form F η/b frontier; anything
more about delivery or the old cap).

None of the proposals changes the headline (the reported model at |Q| ≤ n^b, b < ½, under (V), (L^b), (W)); each
refines a sufficient condition, a range inside a lemma, or a rate. **Lead's recommendation (HQ decides at CP3):
adopt P1–P5 and P7 in one statement revision v1.5 together with the riders T2 and T4 that HQ has already scheduled
after the council** — not into v1.4 now. Reason: v1.4 has just been swept as a whole; every one of these edits
touches a checked proof (`lemmas/L2_width.md` §1, §2, §3(iv), §4; `L5_formR.md` §2; `L6_examples.md` E5) and would
need its own change check and a re-sweep of those files before the council, and PROTOCOL rule 10 would then ask
for a better-theorem review of the new final statement again. One revision after the council, with one change
check, costs less and ends the loop. Until then the claims carry **`headline-strength pending`** (rule 10).

| id | proposal | reviewer's class | lead's check | disposition |
|---|---|---|---|---|
| P1 | (BM-W) → additive margin (√λ_n − d_n)/√(log n) → ∞ (or with m_n, the smallest standardised signal over the truth-removal family, in place of √λ_n) | ADOPT NOW, HIGH | on ℬ_n the signal-plus-noise term is ≥ m_n − d_n − √(2 log n); the rest of Lemma TL-W is unchanged. Correct as sketched; the old condition implies the new one | **ADOPT in v1.5** (conservative λ_n version in the theorem; m_n version as a remark) |
| P2 | (C3): exponent s_n²/2 + O(1) in place of s_n²/8; under (W-δ) the rate n^{−δ₀²/(8(2A+2))}; converse with (1 − o(1))s_n²/2 | ADOPT NOW, HIGH | concentrate at −e_n, e_n = max[a − √(a² − 4κ_E − 2)] = O(1/√log n): Φ⁰_n ≤ −e_n gives Z² ≤ a² − 4κ_E − 2. Correct | **ADOPT in v1.5** (a rate; no hypothesis changes) |
| P3 | (C3)(a), (b) and TL-W for \|Q\| log n/n → 0 instead of a fixed power | ADOPT NOW, HIGH | (F0) of L2 already reads so; wrapper only | **ADOPT in v1.5** |
| P4 | (D-R^b), (D-loc^b): frame entropy log N_n ≤ log p + h log n + o(log n), h + b < ½, δ₀ < 1 − 2b − 2h | ADOPT NOW, HIGH | L5 P9a Steps 3–5 give max Z² ≤ 2 log p + 2h log n + o(log n); P9 with γ = 1 − 2b − 2h − δ₀. Correct | **ADOPT in v1.5** |
| P5 | (W-ref) as one quantitative budget min a⁰_n − B_n → ∞ (growing frame dimension, non-vanishing errors) | ADOPT NOW, HIGH | the first display of L2 §3(iv) is E max ≤ B_n; no new estimate | **ADOPT in v1.5** (the present (W-ref) kept as the corollary) |
| P6 | Form R leak at the exact scale: ϖ_n ≤ κ√(log n/n), b + 15ρ + Dκ < ½, D not sharp | WORTH A TICKET; HIGH for existence | consistent with L4 §7 item 4; needs one uniform D tracked through Lemmas 2–4 | **DEFER — open item O3′**, now with this concrete statement; attempt in the v1.5 leg only if HQ wants it |
| P7 | equicorrelated example: (W) for b < 3/8; width gap → +∞ for 3/8 < b < ½ | WORTH A TICKET; HIGH for the strict ranges | agrees with the sketch of the check LC2-C (two independent reviewers); proof needs the size-by-size comparison with a uniform union over subset sizes | **ADOPT in v1.5 if the proof closes (one attempt)**, else O4′ stays. Value: for 3/8 < b < ½ it would be a proved instance where the lattice route fails — the natural test case for O1 |

Evidence for each disposition is the reviewer's proof sketch (file above, (ii) of each proposal) plus the lead's
check in the table; nothing is claimed in v1.4 on the strength of these sketches.
