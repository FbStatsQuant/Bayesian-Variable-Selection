# R03 — Fresh cross-family review of lemmas/L2_robust_path_attempt.md (XA)

Reviewer: Claude Opus 5.5 (fresh seat, review sub-agent). Date 2026-11-09.
Read: XA STATEMENT.md; lemmas/L2_robust_path_attempt.md; numerics/N3_robust_path.py and
N3_robust_path_output.json; FAC-B lemmas L1 (cs_reduction), L3 (event), L4 (path); FAC-B cs_core.CS
(the scorer N3 imports); FAC-A L1 §L1.0–L1.1 (only to check L2's one remark about it).
NOT read: any LOG, lead conclusions, L1_geometry.md, other reviews' conclusions, W2-FAC-X.
No git operation, no other ticket contacted, no subagent. Files written: this file and
reviews/R03_scratch/R03_* (rerun of N3 with redirected output; an adversarial-oracle stress test).

## 0. Verdict summary

| Component | Verdict |
|---|---|
| §1 reference formulas (κ, q, τ, M_T, c, b, D, A, W, V) | VERIFIED (identical to FAC-B L1.3, L1.4, L4.0(a,b)) |
| §1 UP(ζ) | HYPOTHESIS ONLY, correctly labelled. "uniform score error r ⇒ UP(2r)": VERIFIED |
| §1 envelope ζ ≤ Cp²(log n)^C0/√n | UNPROVED CANDIDATE, correctly labelled; likely pessimistic (§6.3) |
| §2 finite certificate (C) | VERIFIED (deterministic); needs the general-bound form (Fix M1) |
| §2 AA incl. constant 20ζ | VERIFIED |
| §3 BAL | VERIFIED (deterministic, adversarial exceptions allowed); E5 instantiation VERIFIED |
| §3 FG | VERIFIED |
| §4 END, MAJ, MG, TOL, |I| propagation | VERIFIED |
| §5 conditional C1 path theorem (large branch) | VALID AS A CONDITIONAL THEOREM; every constant rechecked; Fix M1 needed for the end-phase swap step |
| §5 small branch p ≤ n^{1/200} | VALID, conditional on UP only (no geometry) |
| §6 gap list | ACCURATE. Gap 2 can be narrowed substantially in the bulk (§5.3 below) |
| §7 weighted-centre identities | VERIFIED (exact algebra; numerics 8.7e-15). No consequence claimed, correctly |
| §8 / N3 | REPRODUCED; evidentiary description must be tightened (Fix M2) |
| Counterexample search | NONE FOUND to any stated implication; the adversarial stress test (§7) finds no failure inside the theorem's regime |

Overall: **the finite certificates and the conditional path theorem are correct as conditional
mathematics. Neither open input (UP gain coupling, prefix geometry) is proved, and L2 says so.**
Recommended status label: "PROVED-CONDITIONAL (certificates C, AA, BAL, FG, END/MAJ/MG; Theorem §5
conditional on UP(ζ) + geometric hypotheses; small branch conditional on UP only). X2 OPEN."
L2 is safe for downstream use after M1–M3. The other items are recommendations, but HQ planning should note R1 and R3.

## 1. §1 reference and UP

Line-by-line against FAC-B:
* κ=(1−ρ)/ρ+1/[ρ(n²−1)] = α/β (L1.2, L4.0); q=k+κ, γ_k=1/q: correct.
* B = Σ_{S0}ξ − ϖ, x_T=(B+Σ_{T∖S0}ξ)/q: this is FAC-B L4.0(a) x_T=(s_T−ϱ)/(k+κ) with ϖ≡ϱ. The
  symbol ϖ is never defined in L2; it must be cited as FAC-B L4.0(a)'s ϱ (Fix M3).
* truth shift √((n−1)(1−ρ))θ_j/σ = λ_θθ_j (L4.0(b)): correct.
* α, k1=κ₁, ψ_T, M_T=νnκ₁²/(αψ_T): correct. Since t_j=κ₁τ_j and ε_n=n/α,
  ν log(1+ε_n(1+γ_{k−1})t²/ψ) = ν log(1+(1+γ_{k−1})M_Tτ²/ν). So c=(1+1/(q−1))M_T and b=(1−1/(q+1))M_T are exact.
* D_j, A_l, W_jl, V_jl=τ_l²−τ_j²−(τ_l−τ_j)²/q: identical to L4.0(b). N3 also checks them against direct
  F differences (max error 9.2e-6 at n=10⁸, as expected from subtracting O(n log n) scores). Verified.

UP(ζ). This is a uniform gain-perturbation hypothesis over the whole reference lattice S0⊆T⊆S* and all
feasible neighbours, including truth moves and neighbours that leave the lattice (adding N0 nulls). That
is a legitimate hypothesis, and "uniform absolute score error r ⇒ UP(2r)" is immediate. Two remarks:
* The §5 theorem uses full-lattice UP, which is non-circular but probably stronger than needed. A clean,
  non-circular restriction is to fix a deterministic, reference-measurable family 𝒢 of states
  (e.g. all T in the lattice satisfying the geometric hypotheses) and require UP only on 𝒢 and its
  neighbours. The §5 induction then needs only "S*∈𝒢 and every AA-admissible safe deletion from a
  state in 𝒢 lands in 𝒢". That is exactly the geometry program (Rec R2).
* Random-design remark (not in L2): N0 is X-measurable. If the coupling builds the reference ξ,η from
  the noise conditionally on X (FAC-A L1.0: given X, g~N(0,R̂)), the reference's E_n has conditional
  probability →1 uniformly over |N0|≤15. Any UP proof should keep this conditional structure.

## 2. §2 finite certificate (C) and AA

(C): d = min over kept nulls of |τ|, R = max over outside nulls (N0 included) of |τ|.
* best reference null deletion ≥ Δ_k−c d² (log(1+u)≤u, at the minimiser): correct.
* additions ≤ −Δ_{k+1}+bR²/(1−bR²/ν) (−log(1−u)≤u/(1−u), monotone in τ_l²; needs bR²<ν): correct.
* null swaps: V≤τ_l²−τ_j²≤R²−d², and W is increasing in V; W<0 when V<0 ≤ Uswap: correct.
* Perturbation step: actual best null deletion ≥ L−ζ > 0, actual addition ≤ Uadd+ζ < L−ζ, and the
  same for swaps; truth moves ≤ −t+ζ < 0. So the actual argmax is a null deletion with positive gain.
  Correct. Only safety is certified, not which null is deleted. That is the right claim.
* m=0 clause: correct.

AA: from D_j ≥ D_{j*}−2ζ, exponentiating gives exactly
τ_j² ≤ d²+(e^{2ζ/ν}−1)(ν/c+d²). Simplification: u=2ζ/ν≤1, e^u−1≤2u (valid to u≈1.256), and
ν/c+d² ≤ 4ν+ν. So the excess is ≤ (4ζ/ν)(5ν)=20ζ. Correct. |τ_j| ≤ d+√(20ζ): correct.
Also |τ_j|−d ≤ 10ζ/d when d>0, which is far sharper when d≍H; the geometry program should use it.

**Fix M1 (mandatory).** §5's end phase does not literally use (C) with Uswap=MV/(1−MV/ν), V≤R²−d².
It uses a convexity bound for swaps and a majority-side point for the deletion lower bound. State (C)
in its general form: "if L ≤ (reference best null deletion), Uadd ≥ (every reference addition),
Uswap ≥ (every reference null swap), every reference truth move ≤ −t with t>ζ, and L>ζ,
L−Uadd>2ζ, L−Uswap>2ζ, then …". §5 then instantiates it. The proof is unchanged.

## 3. §3 BAL and FG

BAL, line by line. In the case x>δ/2: a+b ≥ 2x−δ > 0, so b>|a|. Then {|ξ|≥|a|} = {ξ≤a}∪{ξ≥|a|} = Top(J)
(distinct |ξ|), and K0 = Top(J) minus the positives in [|a|,b). Negative count of K0 = that of Top(J).
J(½−β) ≤ #neg ≤ |K0| ≤ m+r. Also Σ_{K0} ≤ Σ_{Top(J)} ≤ βJH, and each of the ≤r symmetric-difference
changes raises the sum by ≤H. So qx ≤ B0+βH(m+r)/(½−β)+rH. Correct. J=0 is trivial. Reflection
(ξ,B,a,b ↦ −ξ,−B,−b,−a) preserves every hypothesis. Correct.
E5 instantiation: |D_J| ≤ H̄√(2Jx_J) gives β_J=√(2x_J/J), and the sign bound gives √(x_J/(2J)) = β_J/2: correct.
J ≥ |K0| ≥ m−r, so the supremum of β_J over J ≥ m−r is the right one. Correct.
Comment (not an error): "take r=o(loglog n)" is sufficient, not necessary. BAL only needs r ≤ c·m
for a small constant c (the term rH/q ≈ (r/m)H). Under the relaxed bulk target of §5.3 below,
c≈0.2 already suffices. The program should aim for r=o(m), not r=o(L_n).

FG: kept points have distance ≥ min(x−a,b−x)−w (band points: x≥a+w; non-band kept: beyond a or b).
Deleted N* points have distance ≤ max(x−a,b−x)+w. So max_deleted ≤ d+|a+b−2x|+2w. Correct, and no
witness is needed. Correctly described as an implication from band localisation, not a proof of it.

## 4. §4 END / MAJ / MG / TOL

* x=(IH+E)/q, |E| ≤ B0+mw: correct.
* |x|<H−w: |x| ≤ (mH+e)/q, so mH+e < q(H−w) ⟸ e+qw < (s+κ)H, implied by e+qw<H since s+κ>1. Correct
  (L2 states the conclusion; the one-line reason uses s≥1).
* MAJ: (H−w+x)²−(H−x)² = (2x−w)(2H−w) and x ≥ (H−e)/q for I≥1. So Jgap = [2(H−e)/q−w](2H−w) > 0
  when H−e>qw. Correct.
* MG: f(u)=ν log(1+cu/ν) has f′ ≥ c/(1+4cH²/ν) on [0,4H²], and all retained distances are ≤ H+|x| ≤ 2H.
  Correct.
* TOL: MG ≈ 2h/q·(1+o) ≥ 2h/(m_e+s+κ), so ζ=o(h/m_e) suffices. Correct.
* |I| dynamics and (|I|−1)/(q−1) ≤ |I|/q ⟺ |I| ≤ q: correct. Once |I|≤1 it alternates 1↔0, so the
  ratio bound is needed only on the initial |I|≥2 stretch. Correct.
Rec R4: retained magnitudes in [H−w,H] are inherited by subsets, and the imbalance bound propagates
by MAJ. So the §5 end-phase hypothesis is an entry-only condition. Say so; it halves the stated
geometric burden at the end.

## 5. §5 conditional theorem — every constant rechecked

### 5.1 Inputs
M_T=½+o(1) uniformly: upper bound M_T ≤ (1+1/n)n/(2r) with r ≥ (n−1−p)(1−n^{−1/3}) (E2), p=o(n);
lower bound from L1.5(b,c) and RSS_T ≤ ‖e‖². Correct (simpler than FAC-B because p=o(n)).
h=H̄² = 2log(2m0+2)+2L_n ≤ 2a log n+o(log n); B0=|s_{S0}−ϱ|=O(L_n) by E1 and (c1). Correct.
Δ_k ≥ ½log(n+1)−o(1) for k≤p, and Δ_{k+1} likewise when an addition exists (k+1≤p). Correct.

### 5.2 Margin arithmetic (independently recomputed)
Bulk: d ≤ H+.01H; c=½+o(1) (q≥m_e). Deletion ≥ (.5−1.0201a) log n. R ≤ 1.03H gives
addition ≤ (−.5+1.0609a) log n. V ≤ .02H(2.04H)=.0408h gives swap ≤ .0408a log n (the N0 branch is
smaller). Margins at a<¼: del−add ≥ (1−2.081a) > .47; del−swap ≥ .5−1.0609a > .234. "Exceed .20 log n"
is correct.
End: t≥1 cost (h/2)(q−t)²/[q(q−1)] ≤ h/2, since t²−2qt+q ≤ t(t−q) ≤ 0. Correct. t=0 cost (h/2)q/(q−1):
L2 writes ≤h. In fact q−1 ≥ s+1+κ > 2 gives q/(q−1) < 3/2, so the cost is ≤ .75h.
Additions: t=0 ≤ h/2; t=1 ≤ (h/2)(1+1/q) ≤ .75h; t≥2 ≤ (h/2)(1.04)² = .5408h. Correct.
Swaps: convexity in τ_l ∈ [−H−x, H−x]. The same-side endpoint gives V=0. The opposite endpoint gives
V = 4σHx−4h/q = 4h(σI−1)/q (with x=IH/q). So swap ≤ 2h(t−1)₊/q + o. For t≥2 this is ≤ .08h = .16a log n.
Correct. Margins ≥ min(.20, .5−2a) log n: correct (actual minimum ≥ .21 for t≥2 and .5−2a for t≤1).
At m=0: x=B/(s+κ)=o(H), additions ≤ (−.5+a) log n, truth moves ≈ −n. Correct.
Truth moves: L4.0(e) holds on the whole lattice, with separation ≍ n (deletions, and swaps with
V ≤ −(7/16)τ_j²). Correct.
Small branch: L4.2's bounds (null deletion ≥ .29 log n, addition ≤ −.29, swap ≤ .11) hold at EVERY
lattice state (|τ|² ≤ .1 log n uniformly). With ζ=o(log n) any null deletion order is safe. Correct,
and this is a genuinely geometry-free conditional result.

**Rec R1 (important for HQ planning; not an error).** The restriction a<¼ is NOT produced by §5's
arithmetic. With q/(q−1)<3/2 the end phase works verbatim for a<⅓. With FAC-B L4.0(c)'s refined
Δ_k ≥ ½h+½log n−log k−L_n−2 (valid since k=O(L_n)≤p/2), the end phase works for every a<1.
The bulk crude bounds work for a<0.47. So the exponent ¼ comes only from the unproved UP envelope.
L2 §1 hints at this; state it explicitly in §5.

### 5.3 Bulk geometry can be weakened (new, verified algebra; Rec R3)
In the bulk the fuzzy-gap hypothesis ("outside distance ≤ d+.02H") is redundant, and the centre bound
can be relaxed from .01H to a constant fraction. Proof: for every kept null j and outside null l,
V ≤ R²−d², so

  best deletion − any null swap ≥ Δ_k − c d² − M(R²−d²)(1+O(log n/n)) = Δ_k − M R²(1+o) − (c−M)d²,

with c−M = M/(q−1) = o(1) for q ≥ m_e. The d² terms cancel. With R, d ≤ H+|x| and |x| ≤ εH:
deletion ≥ [½−(1+ε)²a−o(1)] log n; del−add ≥ [1−2(1+ε)²a−o(1)] log n; del−swap ≥ [½−(1+ε)²a−o(1)] log n.
So **for m ≥ m_e the single hypothesis |x_T| ≤ εH with (1+ε)² < 1/(2a) − η (η>0 fixed) suffices.**
For a<¼, any ε ≤ 0.41 works. The open bulk geometry therefore reduces to a coarse centre bound along
AA-admissible paths. Via BAL it needs only straddling thresholds with δ ≲ .8H, β ≲ .05 and
r ≤ ~.2m — no band localisation of width o(H), and no FG. The scratch stress test (§7) agrees: under
ζ≈h/m_e the push adversary drives |x| to .24H (violating L2's .01H) while the reference safety
margin stays ≥ .40 log n.
(The end phase still needs MAJ-type structure, because there the coefficient (c−M) is not o(1).)

## 6. §6 gaps, design-agnostic framing, and the unproved inputs

### 6.1 What is valid, what is unproved
VALID (deterministic or conditional): §1 formulas; UP⇐uniform score error; (C); AA; BAL; FG; END/MAJ/MG/TOL;
§5 large-branch theorem GIVEN UP(ζ), ζ=o(h/m_e), and the two geometric hypotheses; §5 small branch
GIVEN UP(ζ), ζ=o(log n); §7 identities.
UNPROVED — gain coupling: UP at any rate, for the centred, sample-sd-standardised iid design, with one
CS/noise coupling, including determinant/prior terms, s_Y, ψ_T, truth neighbours and N0 additions.
The p²/√n envelope is a guess.
UNPROVED — geometry: (i) bulk centre bound along every AA-admissible prefix (reducible to |x|≤.41H by
§5.3); (ii) end-phase entry: retained magnitudes in [H−w,H] with m_e w=o(H), and |I|/q ≤ .04 at entry.
Item (ii) is genuinely delicate. AA's tolerance √(20ζ), or 10ζ/d, can exceed the top-order-statistic
spacing δ_e≍L_n/H when ζ ≫ L_n²/h. Then a small-|ξ| "left-behind" can survive into the end phase.
The scratch "far" adversary at ζ=3 does exactly this (min retained |ξ|/H̄ at entry 0.00–0.11, vs ≈.40–.55 on the exact path), yet the
path still ends at S0, because left-behinds are cheap to delete. So the END magnitude hypothesis is
stronger than what safety needs. A weaker end-phase invariant (majority dynamics on the near-top part
plus "every retained small-|ξ| point has deletion gain above every unsafe move") is a plausible repair.
This is a suggestion, not a proof.
L2's own counterexample (x=0; .1,.1001,2): verified. It refutes only the EXACT interval invariant, as
L2 says.

### 6.2 HQ design-agnostic framing — which hypotheses are CS-specific
GENERAL (any population covariance; no CS structure used):
* G1: the perturbation logic. UP(ζ) plus reference margins >2ζ between the best safe move and every unsafe
  move imply an actual safe move. Holds for any pair of score functions on any neighbourhood graph.
* G2: uniform score error r ⇒ UP(2r); induction "safe prefix ⇒ hypotheses ⇒ safe move"; exact count
  m0 and cap arithmetic ell_n+|S*| ≥ m0.
* G3: M_T=½+o(1) uniformly over T⊇S0 when p=o(n) (RSS_T/‖e‖² → 1 because Φ(T) ≤ Φ([p]) ~ χ²_p).
* G4: Δ_k = log((2p−k)/k)+½log n+o(1), under any lower bound on λ_min of the relevant Gram blocks
  (det-ratio → log(n+1)).
* G5: truth-move negativity at order n, under beta-min plus a lower bound on the partial variance of each
  truth given the other selected columns. FAC-B's proof is CS-written, but the mechanism is general.
* G6: BAL, FG, END/MAJ/MG as statements about real numbers (their USE is CS-specific).
* G7: the form of UP itself. For the random-design transfer, a relative (whitened) Gram deviation
  restricts automatically to every principal submatrix (Rayleigh quotients), so a lattice-uniform UP
  via a relative-norm bound is a design-agnostic statement.
CS-SPECIFIC (equal-loading one-factor structure is essential):
* S1: the one-dimensional reduction — all null gains depend on τ_j=ξ_j−x_T with ONE common centre
  x_T=(s_T−ϱ)/(k+κ) and ONE common multiplier c (or b, M) for all j (FAC-B L1.3–L1.4). (C), AA and MG
  rely on the common c. In general, deletion gains carry j-dependent leverage factors and
  j-dependent determinant terms.
* S2: the drift identity and BAL's application (x = shrunk mean of the retained ξ).
* S3: E3–E7. The ξ_j are iid N(0,1) innovations only because Σ=(1−ρ)I+ρ11′. Sign symmetry, top-J
  balance and order-statistic spacing all use independence.
* S4: the small-branch "every lattice state" bound |τ|² ≤ .1 log n. This rests on the bounded common
  centre (S1). For general Σ, uniform-over-2^{m0}-states control of partial statistics is the real
  obstruction, so even the geometry-free small branch is CS-specific in its proof.
* S5: the end-phase majority dynamics (sign counts I, the |I|/q ratio).
SEMI-GENERAL: §7's weighted centre (rank-one-plus-diagonal, unequal loadings). It extends to rank-r
factors via Woodbury with an r-vector centre, but BAL/MAJ analogues are absent.
Architecture suggestion for HQ: L2 cleanly splits into a design-agnostic TRANSFER PRINCIPLE (G1–G2,
G7: UP + robust reference margins) and a design-specific ROBUST EXACT-GRAM PATH LEMMA (safety margins
that survive ζ-reorderings). FAC-B L4 and analogous exact-Gram theorems (LOC etc.) prove only strict
inequalities along the EXACT argmin path, not ζ-robust safety. The general theorem template should
therefore require "ζ-robust safe-path margins" as its design-specific input.

### 6.3 On the UP envelope (reviewer conjecture, unverified)
§6.1 of L2 says a relative covariance bound alone is not a gain-perturbation proof. That is correct
as stated. Still, the route looks more favourable than the p²/√n candidate. For T⊇S0 the actual
residual statistics contain no signal (μ∈span X_T). Given X, g~N(0,R̂) (FAC-A L1.0). The whitened
deviation of the standardised R̂ is plausibly O_P(√(p/n)) despite the p/√n absolute scale (the 11′
direction is whitened away). And relative bounds pass to all principal submatrices. If gains are
then Lipschitz in the whitened deviation with constant O(log n), ζ=O_P(√(p/n)·log n) would follow.
Under R1 that would push the conditional theorem well beyond ¼. This is NOT verified here — the
standardisation, the ψ_T/s_Y terms and the determinant terms must be checked. It suggests the ¼
barrier should not be treated as structural.

## 7. Numerics

7.1 N3 reproduction. A copy run in reviews/R03_scratch (output path redirected; Python 3.13,
numpy 2.3.0) reproduces every recorded count exactly: 1260 scans, 1240 safe deletions, 48 reorders,
1240 certificates, 2000 BAL, 2000 FG, 1730 MAJ/MG, 0 failures, max direct gain error 9.167e-6. The only
difference is max weighted-identity error 8.66e-15 vs 8.88e-15 (float noise). cs_core hash unchanged.
I did not run the original script in place.

7.2 Code review of N3 (all correct, but weak as falsification). **Fix M2 (mandatory, §8 wording):**
* ζ=.001 ≈ 5e-5·log n. Every path is deep inside the margins, and certificate slack is ≥5.2. The oracle
  test cannot stress the geometry; 48 "reorders" are near-ties.
* BAL test: the anchor is set as B=qx−Σ_K ξ, so B absorbs whatever centre is drawn, and |B|/q appears in
  the bound. This checks the inequality but not the balance mechanism (no fixed-|B|, fixed-point
  configuration is tested). The 3 exceptions are random, not boundary-adversarial.
* FG test: x is always the midpoint (a+b)/2, so δ=|a+b−2x|=0 and FG's δ-term is never exercised.
* Path runs start at [p] with N0=∅. N0 handling (envelope max(d+.02H, L_n+.01H)) is untested.
* MAJ/MG: correct synthetic test, w=1e-5, H=8.
§8 should say these limits explicitly. Its current sentence ("tests exercise the conditional identities
and oracle paths") is true but does not convey how weak the stress is.

7.3 Adversarial stress (R03_scratch/R03_adversary.py, outputs R03_adversary_out.json and
R03_adversary_table.txt). Exact FAC-B CS reference, n=10¹², ρ=.5, θ=(1,1.3), p∈{1000,4000}, 3 seeds
(≤20 total). Worst-case per-scan oracle: any move with reference gain ≥ max−2ζ and >−ζ may win. The
adversary takes any unsafe move if one is feasible. Otherwise it picks a feasible null deletion by
"push" (maximise the signed centre) or "far" (largest |τ|, i.e. creates left-behinds). This is a
SUPERSET of UP adversaries (no score integrability).
Results (log n=27.6; h≈21.8–24.6; h/m_e≈1.1 at m_e=20):
* ζ ≤ 1 (≈ h/m_e): all 48 adversarial paths are safe and end at S0. The push adversary reaches
  max|x|/H̄ = .21–.24 in the bulk, and entry |I|/q up to .32. Both violate L2's .01H/.04 hypotheses at
  this finite n, yet the reference safety margin stays ≥ .40 log n. This supports R3.
* ζ=3 (≈ .11 log n ≫ h/m_e): push fails in 4/6 runs (unsafe swap in the bulk at m=129–1284). The
  centre drifted to .22–.32H̄ and the margin fell to .217 log n ≈ 2ζ. "far" stays safe but leaves
  small-|ξ| points retained at end-phase entry (see §6.1(ii)).
* ζ=10 (≈ .36 log n > margin): an immediate unsafe move, as the theory predicts.
* The exact control (ζ=0) has max|x|/H̄ up to .05 and entry |I|/q=.045. These are finite-n effects
  (asymptotic constants unreachable), not counterexamples.
No configuration violates any implication actually claimed in L2. The failure mechanism seen
(centre drift under ζ ≫ h/m_e) is exactly the open bulk-centre input of §5.3.

## 8. Fixes

Mandatory before downstream use:
* **M1.** State certificate (C) with arbitrary valid reference bounds (L, Uadd, Uswap), and cite that
  form in §5's end phase (convexity swap bound, majority-side deletion bound).
* **M2.** Rewrite §8 to state the N3 limits listed in §7.2: tiny ζ, the B-absorbs-centre BAL design,
  δ=0 in FG, N0=∅.
* **M3.** Define ϖ as FAC-B L4.0(a)'s ϱ. Rename §7's matrix H (it clashes with the magnitude bound H) and
  §7's d_j (it clashes with the distance d).
Recommended:
* R1. State that the §5 arithmetic holds for a<⅓ verbatim (q/(q−1)<3/2), and for larger a with FAC-B's
  refined Δ_k. The ¼ is the UP envelope's alone.
* R2. Formulate UP on a deterministic reference-measurable state family 𝒢 closed under AA-admissible
  safe deletions (non-circular reachable-state version).
* R3. Replace the bulk geometric hypotheses by the single centre bound |x_T| ≤ εH, (1+ε)²<1/(2a)
  (§5.3). Retarget BAL to r ≤ c·m and δ ≲ .8H.
* R4. Mark the end-phase hypotheses as entry-only (inherited by subsets / propagated by MAJ).
* R5. Add an adversarial-policy oracle test (as in R03_adversary.py) to N3 with ζ up to ≈ h/m_e and
  N0 ≠ ∅.
* R6. Use the sharper AA form |τ_j|−d ≤ 10ζ/d (d>0) in any band-localisation argument.

No counterexample to the method or to any stated L2 implication was found.
