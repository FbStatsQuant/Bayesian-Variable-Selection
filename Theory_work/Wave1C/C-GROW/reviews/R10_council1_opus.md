# R10 — Council round 1, Claude seat (Opus 5.5, effort high)

Scope read: Wave1/PROTOCOL.md (§ Independent final review), Wave1C/PROTOCOL.md (rigour rules; Method-side changes),
C-GROW STATEMENT.md v2.4, METHOD_REQUIREMENTS.md, lemmas/00_MAIN, L0–L6 in full. Sources consulted: GEN
L1_lemmaE.md (L1.1–L1.4, the toolkit L0 re-scales), GEN L5_assembly.md ([OP], L5.3 de-randomisation), SoP
02_method.tex (blocks/tables/start 187–211, start mode/e4 ~228–237, exact branch 167–170, local search/HPM 463–467,
LS0 490–506, cost 413), SoP 04_theory.tex (D0 69–74, premises 84, TH09/T03♯ status, TH05.0 status 489),
Scripts/Data_generators/gen_dev_data.R (truth() 33–42, generate_dev_dataset 49–61), numerics D3_summary.md,
D4_summary.md, F2_exact_tau0.txt, CITECHECK.txt. I read the review-file verdict lines only to check that the recorded
statuses match; my judgments below are independent. I tried to break every step; what follows is what survived.

## Step-by-step check (summary of what I verified)

* **L0.** Rank of 𝒟₂ projections grows to C_J log n; 2^{d/2} ≤ n^{C_J} is absorbed by t_n = 4(D+2+C_J) log n; L1.3's
  (n−1)φ₀² ≥ max(J,100) and J/((n−1)φ₀²) ≤ 1 still hold for J = O(log n). L0.2(a) arithmetic (2√((n−1)n^{1/3}) +
  2n^{1/3} ≤ 4n^{2/3}) and both displays of L0.2(b) (−log(1−x) ≤ x + x² on [0,½]; log u ≤ u−1 with the RSS floor)
  are correct. Prior ratios correct (w(k+1)/w(k) = (k+1)/(2p−1−k); 2p−1−k ≥ p for k ≤ p−1).
* **L1.** Neighbour case split is exhaustive (addition; truth deletion/truth-removing swap → TL; extra-removing swap
  (C∖{e})∪{l} → NA at (C∖{e}, l), beaten by the corresponding deletion). Saturated centres (|C| = K) are handled
  (no additions; swap case uses |C∖{e}| < K). Scoring at cap τ−1 vs certified endpoint at cap τ is right.
* **L2.** Family 𝔉 sizes and Gram floors (interlacing from (G2)) are right. TL: Schur complement gives
  Λ_A ≥ (n−1)φ₀²θ*²_min; the L1.4(a),(c) step and the (A+1) log n penalty budget are right. L2.2: c_n/2 cancels the
  prior and ½log(n+1) terms exactly, leaving −½. L2.3(a): (I−P_T)x_l = a + b with a ⊥ b; Cauchy–Schwarz gives
  Z²_{T,l} ≤ Z²_{Q_l,l} + χ²_Q, range inclusion P_{Q_l} − P_T ≼ P_Q − P_{S₀} correct, ≤ p reference normals, LM tail;
  the final inequality reduces correctly to |𝒫| + O(√(log n log log n)) ≤ log(n+1) under (G4-χ). L2.3(b) correct.
* **L3 (the hard lemma).** (3.1) per-block optimality; (3.2) counting (≤ s₀ bad blocks); "junk forces large W_b"
  — I re-derived (3.3) including the per-|N_b| division (2κ_E/|N_b| ≤ 2κ_E) and the NEG telescoping
  ‖Πμ‖² = Σ δ²_{U_{s−1},l_s}; the ε₁ optimisation (min = η/2 + √(2Aη) < ½ ⇔ η < η_A); τ_n(k) ≥ 3; (3.4) (√(eτ)
  bounded with the upper, e^{−τ/2} with the lower bound of τ — legitimate separately); the dyadic ladder
  (p ≤ n^A turns the exponent into −ξ/(1+ε₂), geometric sum uniformly bounded since ε₂ ≥ ε₁). Covers all maximisers
  simultaneously and near-saturated ones; no block independence. Step 2(a) feasibility (Q=[p] & k̃=K ⇒ S̃=[p]),
  TV + 𝓩 margin; Step 2(b) with NEG and the √(2ηL log n) cross term. Correct.
* **L4.** [OP] is a pathwise statement about a deterministic LS0; its proof (GEN L5) does not use the cap value, so a
  data-dependent integer cap is fine. MR1 cap ≥ |S̃₀∖S₀|; (b): |𝒫| ≤ (1−δ₀) ln n < log₂ n ≤ ℓ_n. Bounded convergence
  for E₀[1−π(S₀)]. Correct.
* **L5(a).** P1 (spectral density extrema), P3, P4 (two-sided formula, factor (1−A)(1−B)/(1−BC) ∈ [0,1]; one-sided
  cases), TV (separation leaves ½|θ_j|(1−ρ²)/(1+ρ²); Var ≤ 1), NEG (O(1) leakage since ρ^{2d_n} ≤ 1/n),
  (G4-dir) via nearest-neighbour regression (≤ p(|Q|+1)² directions), piecewise (G1). Correct.
  **L5(b).** I re-derived the partition (within-group distance 0.3 < 0.7; lexicographic chain merges; top-down cut
  leaves {g₁,g₂} and singleton groups; next-fit pairs consecutive groups ⇒ {10b,…,10b+9}); truths 2, 26, 53, 75 in
  blocks 0, 2, 5, 7; the U = ∅ case for truth 26: Cov = 0.7·(−1) + 0.3·1 = −0.4, Cov² = 4/25. Correct.
* **L6.** L6.2 (entrywise event, operator norm ≤ size × max entry for O(log n)-size submatrices; m♯_n = O(log n) via
  C(p,k)/C(2p−1,k) ≤ (2/3)^k; TV uniform over |U| ≤ 15 with fixed θ on the standardized scale). L6.3 (population
  leakage ≤ n^{−2} beyond R_n; recursive partial-correlation formula; |z_U − z_0| = O(ħ²), |z_0| = O(ħ) ⇒
  n|z_U² − z_0²| = O((log n)^{3/2}/√n)). L6.4 (the key step: conditioning on (W_D, ε), D = U₀ ∪ S₀, fixes r_Y
  because the standardization of the true columns is W_D-measurable; g = (I−P_{U₀})Ce is isotropic in a
  W_{U₀}-measurable subspace containing r_Y; ‖m‖ = O(1) from ‖α‖ ≤ Cr^{d_n} ≤ Cn^{−1/2}; the CN_D device avoids a
  sphere law conditional on A_cov) — correct. L6.5 (count of junk blocks ≤ J(t_n(k)), distinct l per block; ladder
  O(log n)·n^{−1/2+o(1)}; exclusion via (6.7) giving ¼ log n − log k). L6.6 (exact innovation identity
  (I−P_T)CW_l = (I−P_T)g, e ⟂ W_T by the Markov property; Z vs Z⁰ error O(log n/√n); ≤ p(q+1)² reference
  normals). L6.7, assembly and the diagonal de-randomisation (GEN L5.3 pattern). L6.8 checked against
  gen_dev_data.R: active = 5·step·k + pos, gaps ≥ 5·7 − 4 = 31, |β| ∈ [0.8, 1.8]·c, signal on the scale()d X,
  eps ~ N(0,1) drawn independently after X. Correct.
* **Numerics cited in STATEMENT §0/(C6)** spot-checked against D3_summary.md (S5 p=100 cap ℓ_n: 2/40 and 0/40 at
  n = 3200, 12800; cap ℓ_n+|S̃₀|: 80/80; S2 120/120 and 160/160; S5 p=400 47/47 scored, 45/47 reached, 27/27 at
  n ≥ 800) and D4_summary.md (25 seed-0–4 fits with HPM = S₀; the two targeted seeds are separately labelled).
  All match.

I found no counterexample and no false step.

## Gates

**G1 — correctness of every step: PASS.** Every inequality in L0–L6 that I re-derived holds with the stated
constants (details above). The two places where I looked hardest — the global size ladder of L3 (all maximisers,
near-cap sizes, Markov over blocks without independence) and the L6.4 conditioning (what is fixed given (W_D, ε), and
why A_cov is not conditioned on) — are correct. The (C1) move count (exactly |C∖S₀|), the scoring-vs-certification
cap distinction, and the (C4)(b) production-cap claim under (G4-χ) are right. No step needs repair.

**G2 — hypotheses used = hypotheses stated: PASS.** (C2) lists the minimal hypotheses actually used by L2 (TL: G,
energy, p ≤ n^A, |Q| ≤ C_Q log n, |Q| ≤ K, (G2), BM-∞; NA: same without BM-∞ plus (G4-χ)/(G4-dir)); (C3) lists
exactly what L3 uses ((G3a) for the block Gram floor, TV, NEG(η) with η < η_A, (G1) feasibility, block size ≤ 16).
(C4) composes them with (H0) and the premises. (C5)(c) states that NEG and (G4-dir) are *not* verified and that the
three events are proved directly — consistent with L6. The only mismatch is benign and in the safe direction: the
stated premise e4 (prescribed smallest-size/lexicographic maximiser) is stronger than what L4 and L6.1 use (the
emitted centre is *some* γ₀-maximiser, since Sand_n covers every maximiser) — see suggestion S1.

**G3 — no hidden assumptions: PASS.** Partition: the fixed-design results are on the method's actual (deterministic)
partition; L6 allows any X-measurable partition and controls all conditioning sets of size ≤ 15 uniformly, so no
selection-independence is smuggled in. No population partition recovery, no start-size assumption, no mixing claim,
no conditioning on 𝒪. Exact ties (partition of L5(b), start-mode tie rule, scan ties) rest on EX-A, which is named.
Random design: ε ⟂ X and fixed standardized θ are stated and match the generator.

**G4 — cited inputs have adequate status: PASS.** I checked verbatim: T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF:
VERIFIED* (A-REV5))" (04_theory.tex:489); T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (TH09 row);
[OP] "PROVED (by this seat, unchecked)" inside Theorem GEN (GEN L5_assembly.md:3,11); GEN L1 "PROVED (by this seat,
unchecked)", R02 VERIFIED-WITH-AMENDMENTS (L1_lemmaE.md:3); N3 OPEN kept as premise e4. Each C-GROW lemma keeps its
author label "PROVED (by this seat, unchecked)" separate from the check record, and the recorded verdicts (R02
VERIFIED; R03 VERIFIED / VERIFIED-WITH-AMENDMENTS (2); R04 VERIFIED-WITH-AMENDMENTS; R06 VERIFIED-WITH-AMENDMENTS;
R07 VERIFIED) match the review files. Nothing is upgraded; L6.1 is explicitly conditional on its inputs.
CITECHECK.txt: 14 ok / 0 miss.

**G5 — constants/rates tracked: PASS.** Dependencies of n₀ are named (σ², M, φ₀, A, C_Q, s₀, BM/TV envelopes; ρ,
A, s₀, θ, σ for L6). Explicit rates exist where they matter: L3 C₂√(log n) n^{−ξ/(1+ε₂)} with ξ ≥ ξ₀ > 0;
P(𝓩ᶜ), the L2.3 maxima ≤ 1/log n; L6 sandwich O(log n)·n^{−1/2+o(1)}, (6.7) n^{−1/4+o(1)}, L6.3
ϖ_n = C(log n)^{3/2}/√n. The η_A threshold is derived, not asserted, and is the same constant in both steps of L3.
The theorem only claims → 0, so no rate is over-claimed. (Minor presentational point S3.)

**G6 — fidelity to the method: PASS.** Score (g = n ridge score, ν = 0.01 + n/2, response scaled to yᵀy = n−1),
capped BB prior with the exact ratio, K = min(p, ⌊n/2⌋), full-response block tables r_b(U) = m(U)/m(∅), complete
linkage on 1−|r| with lexicographic ties, size-only top-down cut at B = min(⌊√n⌋, ⌊√p⌋, 16), next-fit packing,
start mode = argmax γ₀ on Ω, §6.10 search (frozen-centre complete scans, strict improvement, plain-lexicographic scan
ties, ≤ ℓ moves then one further scan, `local_limit`), HPM over every scored model with size-then-lex ties, LS0
after the final search (and c₄), GUARD-W, OP-LS0, e4 — all as in SoP 02_method.tex. MR1 changes only the unshipped
LS0 cap, is explicit in STATEMENT §1, (C4), L4 and METHOD_REQUIREMENTS.md, and is permitted by Wave1C/PROTOCOL.md
"Method-side changes"; its worst-case cost bound matches 02_method.tex:413; the final local search keeps ℓ_n. The
exact-enumeration branch is handled (L4 Note 1 / GEN [OP]). One interpretive omission about that branch is a
required wording fix (F1) but does not make any claim false.

## Score

**9.0 / 10** (uncapped). The proof is correct, complete for its stated scope, honestly scoped, and the L6
random-design extension is a genuinely strong piece (selection-uniform reduction + joint-law spherical tail). The
deduction is for one material interpretive omission (F1) and small presentation items.

## Required fixes

**F1 — Exact-branch pre-emption of the fixed-p (and p ≲ log₂ n) instances is not disclosed.**
*Location:* STATEMENT.md (C5)(b) and the end of (C5)(a)/(c); lemmas/L5_instances.md (b) "Honest reading"; L6 §8
(Corollary L6.8: "applies both to either fixed-p sequence").
*Problem:* By SoP 02_method.tex:167 the production run enumerates every model with |S| ≤ K once
Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)p, with N₀ = max(2500, n, p) ≥ n, so every fixed-p problem is eventually exact (SoP
02_method.tex:635). For the S5 illustration (p = 100) this happens at ln n ≈ 63 (n ≈ 2.5·10²⁷; checked:
(5H₀+4N₀)·100 ≥ 2¹⁰⁰ at n = 2.6·10²⁷), whereas the only NA route proved for (b), (G4-χ), needs
ln n ≥ 96/(1−δ₀). So at every n at which the proof of (C5)(b) is operative, the method is on the exact branch,
S₀ is scored by enumeration, LS0/MR1 play no role, and the conclusion already follows from T03♯ alone (L4 Note 1).
The same holds formally for any fixed-p sequence in (C5)(a) and for the fixed p = 500/1000 sequences of L6.8, and
for p growing slower than about log₂ n. The current honest reading ("asymptotic in a strong sense") does not say
this, and a reader could take (b) as evidence that the LS0 descent mechanism is what delivers consistency on S5.
*Fix:* Add one sentence to L5(b)'s honest reading and to STATEMENT (C5)(b): "For fixed p the production run takes
the exact-enumeration branch once Σ_{k≤K}C(p,k) ≤ (5H₀+4N₀)p (SoP 02_method.tex:167); for p = 100 this is
n ≳ 2.5·10²⁷ (ln n ≈ 63), before the (G4-χ) onset ln n ≥ 96/(1−δ₀). On those n the conclusion follows from T03♯ and
exact enumeration; (b) shows only that S5's population covariance satisfies the hypotheses of Theorem GROW, not
that LS0 is the operative mechanism." Add the parallel caveat to L6.8 / (C5)(c) for the fixed-p sequences, and state
in 00_MAIN (Instances) that the content of Theorem GROW beyond T03♯ + enumeration lies in the regime where p grows
faster than log₂ n (which (C5)(a) with growing p and (C5)(c) with p ≤ n^A do cover).

## Optional suggestions

**S1 — Weaken the e4 premise to what is used.** L4 and L6.1 only need "the emitted LS0 centre is a maximiser of γ₀
on Ω" (Sand_n is proved for every maximiser). Saying so in STATEMENT §1/L4 makes Theorem GROW independent of the N3
tie-rule invariant (only "the coded start_mode returns some maximiser" remains), which aligns with C-PACK's "e4 not
needed" result and shrinks the premise list.

**S2 — Robustness of (C5)(b) to the coded tie-breaking.** The partition derivation relies on exact ties at
1−|r| = 0.7 (EX-A). In floating point the production linkage could pair groups differently. A short extra exact
computation of τ₀ over all pairings of the 20 groups into 10-blocks (or a remark that τ₀ > 0 for every such pairing,
including pairings that put two truths in one block) would make (b) independent of tie handling.

**S3 — Log convention and an overall rate.** State once (STATEMENT §1) that log = natural log ((G4-χ) and L4(b)
compare with log₂). Optionally record the composite fixed-design rate D_n ≤ O(1/log n) for n ≥ n₀ (dominated by the
P(𝓩ᶜ) and L2.3 terms), as GEN L5.1 does.

**S4 — L3 constant in 𝓩.** The pair count per block is ≤ 16·2¹⁵, so "≤ 2²⁰p" is generous; harmless, but
"≤ 2¹⁹p" with z²_n := 2 log(2²⁰p) + 2 log log n would match the count exactly.

**S5 — L1.2(ii) when C = S₀.** Say explicitly that "scored" for the centre relies on OP-LS0 (LS0 scores its
emitted centre), as GEN L5.2 does.

SCORE: 9.0; GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS
