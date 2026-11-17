# W3-D5P — implication note: LIST-CODE (Corollary 6L) and the list-mass premise of Corollary 9C (H5 card 17 (b))

Lead note v1.1, 2026-11-17, after CP3 (outside the council manifest `reviews/MANIFEST_R3.txt`, which it does not change).
Tier B; one Opus check: `reviews/post_cp3/COR9C_check_opus.md` (N1 IMPLIES, N2 IMPLIES, N3 AGREE; ACCEPT-WITH-CHANGES),
whose findings F1–F8 are applied here (markers [F#]). Sources on main 7e7fafaa (the cited W3-DIST, W3-RM, W3-RM2(-R),
W3-READER and L1_POST files are identical on this branch).

## 1. The premise, quoted
`Theory_work/Wave3/W3-DIST/STATEMENT.md:227-231` (Corollary C = card Corollary 9C, `W3-DIST:Cor-C@1.0.1`, statement span
:217-238):
> "Under the conditions of Theorem A, with P*-probability at least 1 − n^{−cM} over the data, **every** completed run
> (whatever its random numbers) with π(𝒯) ≥ n^{−cM/2} satisfies Π̂( d_H(f, f*) > √(M·log n / n) ) ≤ n^{−cM/2}."
and :237-238: "Whether the list carries enough posterior probability is a property of the run: this corollary does not
assert it, and the output does not certify it."
Objects: 𝒯 = the list of a completed run (sampler branch; exact enumeration "not covered", :219); π(𝒯) its posterior
probability. The conditions of Theorem A are (A1)–(A5) (:174-180) at a level M ≥ 1 (:164, :185-187), with (A1)
"y = α* + xᵀβ* + ε" and D_n "n independent copies of a pair (x, y)" (:136).
**Same objects** [F7]: DIST's code facts (`W3-DIST/STATEMENT.md:273-283`) pin the same core 4676af6 and define 𝒯 =
`top_store` with values F(S) = log ϖ + log m and π_𝒯 ∝ e^F — those of W3-D5P `STATEMENT.md` §1 and LIST-CODE (iii);
Ω = {|S| ≤ min(p_ret, ⌊n/2⌋)} is DIST's cap min(r, ⌊n/2⌋); "completed" = status `completed` = output on the sampler
branch (LIST-CODE (i)).
**The true model** [F3]: under Theorem A's law, S₀ := {j : β*_j ≠ 0} (DIST's "true model", :233), in retained indices;
s₀ = |S₀|. 𝓜_n := {S₀ is the unique maximiser of F on Ω} and 𝒦_n := {the deterministic LS0 from the coded start mode
scores S₀} (RM `STATEMENT.md:53-54`; RM2R `STATEMENT.md:55-56`) are read with this S₀ (the search itself does not
depend on S₀); the convention of W3-D5P `STATEMENT.md` §1 for s₀ > K applies (𝓜_n = 𝒦_n = ∅).

## 2. The implication — three parts

**(N1) Pathwise — the premise holds on 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}.** Under LIST-CODE's premises [F2] (core
4676af6 = DIST's pin; shipped configuration `ls0 = TRUE`, cap `"ell_n_plus_mode"`, `ls0_ell` = ℓ_n, `ls0_tie_dp = TRUE`;
EX-A, EX-S, SR; admissible runs, RM `STATEMENT.md:55-65`), with no assumption on the law of the data and without
IMPL-LIST: for every n, every data set in 𝓜_n ∩ 𝒦_n and every completed run (every seed, N_e, R′, calibration outcome),
S₀ ∈ 𝒯, hence π(𝒯) ≥ π(S₀ | y); so the run satisfies Corollary C's premise whenever π(S₀ | y) ≥ n^{−cM/2}, in
particular whenever π(S₀ | y) > ½.
*Source.* W3-D5P:LIST-CODE (i) and (v) (`STATEMENT.md:82-95`; proof `lemmas/L2_listCODE.md` B2–B4, D2, F): on 𝒦_n every
completed run's LS0 is 𝒦_n's search, so S₀ is offered to the final-run ledger; on 𝓜_n it is the best offered model and
the top store keeps it. π(𝒯) ≥ π(S₀) because S₀ ∈ 𝒯 and π ≥ 0.

**(N2) In probability, under one law carrying the inputs.** Let P be a law of the data under which (a) Theorem A's
conditions hold at level M (so Corollary C applies), (b) P(𝓜_n ∩ 𝒦_n) → 1, (c) P(π(S₀ | y) < n^{−cM/2}) → 0 (e.g.
π(S₀ | y) → 1 in P-probability). Then, under LIST-CODE's premises, with P-probability at least
1 − n^{−cM} − P(𝓜_nᶜ) − P(𝒦_nᶜ) − P(π(S₀ | y) < n^{−cM/2}) → 1, **every** completed run satisfies
Π̂( d_H(f, f*) > √(M log n/n) ) ≤ n^{−cM/2} — Corollary C without its list premise.
*Proof.* Intersect Corollary C's good data event (probability ≥ 1 − n^{−cM}) with 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}
(all data events), apply (N1), union bound. (c) cannot be dropped: Theorem A has no beta-min condition, and on 𝓜_n
Theorem A (ii) alone gives π(S₀) only of order n^{−A(s + C₁M)}, far below n^{−cM/2} (checker's remark).

**(N3) "On Theorem 6 designs" — not implied by the recorded results.** Theorem 6's master supplies (b) and (c)
(RM2-R-plus: [MODE], [SAND(Q)], [NA(Q)], [TL(Q)], [POST], RM0-plus (b⁺)) under **Setting R's law**: raw rows i.i.d.
N(m_n, Σ_n) and, in READER's raw form, y^r = α1 + Xθ* + ε with X the centred, *sample*-standardised design and θ*
**deterministic** (RM `STATEMENT.md:41-45`; READER Theorem 6, `READER_VERSIONS.md:666-668`).
*Disjointness* [F4]. Under an i.i.d. law of (A1) with Gaussian rows, C y^r given X^r is N(X D_x β*, σ²C), where D_x holds
the sample standard deviations; Setting R would need X D_x β* = Xθ* almost surely with θ* fixed, which fails because
sd_n(x_j) has a continuous law whenever β*_j ≠ 0. Hence, for s₀ ≥ 1, no law satisfies both Theorem A's (A1) and
Setting R, and (N2)'s (b) **is not supplied by any recorded result** under a law where (a) holds.
*What is missing* is the raw-scale version of P(𝒦_n) → 1: READER bridge **B6.7** ("A raw-scale version (fixed β*) would
need a NEW bridge (medium …). Not proposed", `READER_VERSIONS.md:762`; `:1404` "NEW (optional) | not proposed |
low–medium"). W3-RM2 / W3-RM2-R state SAND-R, NA and TL under the joint law with θ* fixed only
(`Theory_work/Wave3/W3-RM2/lemmas/L4_sandR_b.md:21-41`). The fixed-design Setting F of RM2-F is a raw-scale model
(conditionally on X^r it is Theorem A's law), but its design hypotheses are deterministic and are not shown to hold with
probability → 1 for random designs; its leakage condition (L-gain) at η < η_A is expected to fail for Gaussian designs
with about n^A null columns (checker's rough calculation, not a recorded result) [F6]. Under POST's raw-scale hypotheses
(Gaussian rows, unit population variances, LSF, fixed s₀, |β_j| ∈ [b_lo, b_hi]; `L1_POST.md:12-18`, parenthetical
[R02-3]), (c) is recorded and P(𝓜_nᶜ) ≤ 2E[1 − π(S₀ | y)] → 0 by Markov (RM2R `STATEMENT.md:60`); within that class
only P(𝒦_n) → 1 is open [F5].

## 3. Verdict (checked)
(N1) IMPLIES. (N2) IMPLIES. (N3) AGREE: the probability-level discharge "on Theorem 6 designs" does not follow from the
recorded results (different data laws; raw-scale search bridge B6.7 open). **Recordable now:** the pathwise edge (N1) and
the conditional form (N2).

## 4. Recording-package entry (proposal for HQ)
- **Edge** [F1, F2]. `W3-D5P:LIST-CODE` (clauses (i), (v)) ⇒ the list-mass premise of `W3-DIST:Cor-C`, **pathwise on
  𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}** for every completed run, under LIST-CODE's premises (core 4676af6 = DIST's pin,
  shipped configuration, EX-A, EX-S, SR; admissible runs), no data law, no IMPL-LIST. Probability-level discharge
  **conditional on** P(𝓜_n ∩ 𝒦_n) → 1 and P(π(S₀ | y) < n^{−cM/2}) → 0 under Corollary C's own data law (raw-scale
  convention; READER B6.7 open). Edge type: implication of a premise (pathwise), not an `implies` between claims.
- **W3-DIST:Cor-C status:** unchanged, verbatim ("PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact
  arithmetic); council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS,
  opus=9.2 PASS"): the corollary keeps its premise; nothing it states changes.
- **W3-DIST:Cor-C notes, append** [F1, F2]: "List-mass premise π(𝒯) ≥ n^{−cM/2}: holds for every completed run on the
  data event 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}} (S₀ = {j : β*_j ≠ 0}), under W3-D5P:LIST-CODE's premises (core 4676af6,
  shipped configuration, EX-A, EX-S, SR) (W3-D5P:LIST-CODE (i), (v); `Theory_work/Wave3/W3-D5P/reviews/post_cp3/COR9C_NOTE.md`).
  With probability → 1 under any data law carrying Theorem A's conditions, P(𝓜_n ∩ 𝒦_n) → 1 and
  P(π(S₀ | y) < n^{−cM/2}) → 0. Theorem 6's recorded law (Setting R, deterministic standardised θ*) is not such a law;
  the raw-scale search bridge (READER B6.7) is open."
- **Card.** Row 2.1's sentence "(and, for Corollary 9C, given that the returned list carries posterior mass at least
  n^{−cM/2})" stays as is. A sentence "on Theorem 6 designs the premise holds with probability → 1" is **not** supported
  until B6.7; what can be said: "on the data event of Theorem 6's search argument, every completed run's list holds at
  least the posterior mass of the true model".
- **Errata for W3-D5P** [F8]: `STATEMENT.md` §5 remark 3 ("designs that satisfy both Theorem 9 and Theorem 6") describes
  an empty set for s₀ ≥ 1 (N3); reword at the next statement revision (added as E3 to the R3r correction's ERRATA.md).
