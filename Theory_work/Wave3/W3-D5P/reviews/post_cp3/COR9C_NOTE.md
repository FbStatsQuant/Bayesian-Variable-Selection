# W3-D5P — implication note: Corollary 6L / LIST-CODE and the list-mass premise of Corollary 9C (H5 card 17 (b))

Lead note, 2026-11-17, after CP3 (outside the council manifest `reviews/MANIFEST_R3.txt`, which it does not change).
Tier B; one Opus check (`reviews/post_cp3/COR9C_check_opus.md`). Sources on main 7e7fafaa (W3-DIST, W3-RM, W3-READER
files identical to this branch).

## 1. The premise, quoted
`Theory_work/Wave3/W3-DIST/STATEMENT.md:227-231` (Corollary C = card Corollary 9C, `W3-DIST:Cor-C@1.0.1`, statement span
:217-238):
> "Under the conditions of Theorem A, with P*-probability at least 1 − n^{−cM} over the data, **every** completed run
> (whatever its random numbers) with π(𝒯) ≥ n^{−cM/2} satisfies Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}."
and :237-238: "Whether the list carries enough posterior probability is a property of the run: this corollary does not
assert it, and the output does not certify it."
Objects: 𝒯 = the list of a completed run (sampler branch; "small problems that it solves by exact enumeration are not
covered", :219), π(𝒯) its posterior probability; the conditions of Theorem A are (A1)–(A5) at level M (:174-187), with
(A1) "y = α* + xᵀβ* + ε" and D_n "n independent copies of a pair (x, y)" (:136).
Corollary C's 𝒯, completed run and π are the objects of W3-D5P (`STATEMENT.md` §1: 𝒯 = `fit$top_store`; π the coded
posterior on Ω; 40r + 1 = 40p_ret + 1).

## 2. The implication — three parts

**(N1) Pathwise, law-free — the premise holds on 𝓜_n ∩ 𝒦_n.** For every n with s₀ ≤ K, every data set in
𝓜_n ∩ 𝒦_n and every completed run (every seed, N_e, R′, calibration outcome): S₀ ∈ 𝒯, hence π(𝒯) ≥ π(S₀ | y); so the
run satisfies Corollary C's premise whenever π(S₀ | y) ≥ n^{−cM/2}, in particular whenever π(S₀ | y) > ½ (n^{−cM/2} ≤ 1).
*Source.* W3-D5P:LIST-CODE (i) and (v) (`STATEMENT.md:82-95`; proof `lemmas/L2_listCODE.md` B3–B4, F): on 𝒦_n every
completed run offers S₀ to its final-run ledger, and on 𝓜_n the top store keeps it. π(𝒯) ≥ π(S₀) because S₀ ∈ 𝒯 and
π ≥ 0. No data law, no IMPL-LIST (the list fields are not used; `top_store` exists at core 4676af6), no clause of
LIST-R beyond (i)'s list membership. 𝓜_n, 𝒦_n are data events (RM `STATEMENT.md:53-54`; RM2R `STATEMENT.md:55-56`).

**(N2) In probability, under one law carrying both inputs.** Let P be a law of the data under which (a) Theorem A's
conditions hold at level M (so Corollary C applies), (b) P(𝓜_n ∩ 𝒦_n) → 1, (c) π(S₀ | y) → 1 in P-probability. Then
with P-probability at least 1 − n^{−cM} − P(𝓜_nᶜ) − P(𝒦_nᶜ) − P(π(S₀ | y) < n^{−cM/2}) → 1, **every** completed run
satisfies Π̂( d_H(f, f*) > √(M log n/n) ) ≤ n^{−cM/2} — Corollary C without its list premise.
*Proof.* Intersect Corollary C's good data event (P ≥ 1 − n^{−cM}) with 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}} and apply
(N1); union bound. The last term → 0 by (c) since n^{−cM/2} → 0 (M ≥ M₀ > 0, c > 0).

**(N3) "On Theorem 6 designs" — not implied by the recorded results.** Theorem 6's master supplies (b) and (c)
(RM2-R-plus: [MODE], [SAND(Q)], [NA(Q)], [TL(Q)], [POST], RM0-plus (b⁺)) under **Setting R's law**: raw rows i.i.d.
N(m_n, Σ_n), and y = Xθ* + Cε with X the centred, *sample*-standardised design and θ* **deterministic** (RM
`STATEMENT.md:41-45`; READER Theorem 6 "with deterministic θ*", `READER_VERSIONS.md:666-668`). Under that law the pairs
(x_i, y_i) are not independent (y_i depends on all rows through the sample means and standard deviations), so it is not
a law of Theorem A's (A1) / :136 ("n independent copies"). Conversely, under an i.i.d. law of (A1) with Gaussian rows,
the standardised coefficients θ*_j = sd_n(x_j)·β*_j are random (sd_n(x_j) has a continuous law for n ≥ 2), so θ* is not
deterministic when s₀ ≥ 1. Hence **no data law satisfies both Theorem A's conditions and Setting R** (for s₀ ≥ 1), and
(N2)'s (b) is not available under any law where (a) holds. What is missing is exactly the raw-scale version of
P(𝒦_n) → 1 (the search event under fixed raw β*): READER bridge **B6.7** ("A raw-scale version (fixed β*) would need a
NEW bridge (medium …). Not proposed", `READER_VERSIONS.md:762`; `:1404` "NEW (optional) | not proposed |
low–medium"). Under the raw-scale convention, (c) is recorded (W2-APP:POST, raw-scale convention,
`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:12-18`) and gives P(𝓜_nᶜ) ≤ 2E[1 − π(S₀ | y)] → 0 by Markov (RM2R
`STATEMENT.md:60`), so only P(𝒦_n) → 1 under raw scale is open.

## 3. Verdict proposed (for the check)
(N1) IMPLIES. (N2) IMPLIES. (N3) the probability-level discharge "on Theorem 6 designs" DOES NOT follow from the recorded
results: the two corollaries are stated under different data laws (standardised-signal vs raw-scale convention), and the
raw-scale search bridge B6.7 is open. **What can be recorded now:** the pathwise edge (N1) and the conditional form
(N2).

## 4. Recording-package entry (proposal for HQ)
- **Edge.** `W3-D5P:LIST-CODE` (clauses (i), (v)) ⇒ the list-mass premise of `W3-DIST:Cor-C`, **pathwise on 𝓜_n ∩ 𝒦_n**
  (π(𝒯) ≥ π(S₀ | y) for every completed run), law-free; probability-level discharge **conditional on** P(𝓜_n ∩ 𝒦_n) → 1
  under Corollary C's own data law (raw-scale convention; READER B6.7, open). Edge type: implication of a premise
  (pathwise), not an `implies` between claims; it does not need IMPL-LIST.
- **W3-DIST:Cor-C status:** unchanged, verbatim ("PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact
  arithmetic); council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS,
  opus=9.2 PASS"): the corollary keeps its premise; nothing it states changes.
- **W3-DIST:Cor-C notes, append:** "List-mass premise π(𝒯) ≥ n^{−cM/2}: holds for every completed run on the data event
  𝓜_n ∩ 𝒦_n whenever π(S₀ | y) ≥ n^{−cM/2} (W3-D5P:LIST-CODE (i), (v); `Theory_work/Wave3/W3-D5P/reviews/post_cp3/COR9C_NOTE.md`).
  With probability → 1 under any data law carrying Theorem A's conditions and P(𝓜_n ∩ 𝒦_n) → 1. Theorem 6's recorded
  law (Setting R, deterministic standardised θ*) is not such a law; the raw-scale search bridge (READER B6.7) is open."
- **Card.** Row 2.1's sentence "(and, for Corollary 9C, given that the returned list carries posterior mass at least
  n^{−cM/2})" stays as is. A sentence "on Theorem 6 designs the premise holds with probability → 1" is **not** supported
  until B6.7; what can be said: "on the data event of Theorem 6's search argument, every completed run's list holds at
  least the posterior mass of the true model".
