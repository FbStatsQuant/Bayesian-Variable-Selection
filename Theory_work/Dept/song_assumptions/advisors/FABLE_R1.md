# FABLE_R1 — Expert Advisor answer to DESIGN_MEMO_R0 (TH-SONG-ASSUMPTIONS)

Advisor: Fable 5.2. Date: 2026-11-27. Round R1. Scope: Q1–Q8 of the memo, then the final assumption lists.

**What I read.** DESIGN_MEMO_R0; TH_PREP; `or6_theorems.tex`, `s4_results.tex` (l.160–230), `supplement.tex`
(statements only — I did not see the proofs of thm:dist / prop:dist / thm:post-*); PRECEDENTS_2026-11-17; SL supplement
`32b.txt` (Thm 3, Thm 4, Thm S, Cor S1 proofs); worker tables `tables/e1_*.tsv`; the coded prior in `v3_score.h`
(w(k) = ½/C(2p−1,k), K = min(p, ⌊n/2⌋) — confirmed).

**Status tags used below.** [P] = I give the inequalities; a proof at this level should go through, constants to be
audited. [H] = heuristic / back-of-envelope. [C] = conjecture. [V] = literature item to verify (I give no page numbers
and vouch for no citation that is not in PRECEDENTS). [N] = my own scratch numerics (scripts in
`.rc_tmp/song/advisors/`: `swap_check.py`, `superset_term.py`, `greedy_tail.py`); small, unreviewed, not evidence of record.

## 0. Bottom line

1. **Memo's MARGIN is not provable by the memo's step (3), and is false for fixed j0 when log n = o(log p).** The
   cross term is not a constant problem, it is an entropy problem: how many distinct residual directions
   u_S = (I−P_S)μ/‖·‖ the nulls generate. I found no counterexample when j0 is the size-tail value ⌈(2A+1)s0⌉+1 and
   p ≤ n^A, and I give a reason why (multi-null rivals in MARGIN implicitly bound the entropy) — but that is [C].
2. **Two provable replacements.** MARGIN-U (design-free, constant 2(√d+√m)², attained in the worst case) and
   MARGIN* (constant 2+η, plus a leakage set Q_n and bounded leakage outside it — the in-house `asm:rf-leak` idea).
3. **Constant 2 is sharp for deletions, and multi-deletions must be in the condition** (they bind on S1). Proxy swaps
   (d = m) need only R → ∞, not d·price — which is why the worker's κ_pop predicts worse than κ_del.
4. **The "sufficiency gap" is not a missing assumption.** It is the finite-n superset term (s0+1)/√(2πL(n+1)) plus the
   Gaussian tail of the deletion statistic. It reproduces S1's 0.92–0.98 plateau and S2's 0.45 [H][N].
5. **S1 is covered only by a fixed-ratio (triangular-array) framing**: κ_n := min_D R_n(S0∖D)/(2σ²Pr_n(|D|)), theorem
   "liminf κ_n > 1 ⇒ π(S0|y) → 1; limsup κ_n < 1 ⇒ π(S0|y) → 0". Both of the memo's order forms exclude S1.
6. **Dimension.** As coded (cap n/2), every theorem needs log p·log(p∨n) ≤ c·n/M, i.e. (log p)² = O(n). The bottleneck
   is the size window q_n ≍ s0·log₂(p√n), not the IG envelope or the linearisation. log p = o(n) needs a cap
   K_n ≤ c·n/log p. Hidden coupling: j0 grows like s0(1 + 2log p/log n) outside the polynomial regime.
7. **Drop EFS and FLOOR-S0.** NEC (vanishing floor) + margin suffice; R-transfer needs only a lower sparse isometry.
8. **Misspecification.** f₀ is the KL projection under all three options. Grünwald–van Ommen bites exactly through the
   multiplicity: null gains become ϱ·χ²₁ and control fails when (ϱ̄−1)·log p > ½·log n. Recommend three tiers: T-MIS-a0
   (literal SL Thm 4, fixed dimension, second moments, a.s.), T-MIS-a/b under (iii), and an extension under (i) that
   needs a new size-cap condition because the Fubini size-tail device dies under misspecification.

## Notation

y = Xβ* + ε, μ = Xβ*, S0 = supp β*, s0 = |S0|. Rival S: D = S0∖S (d = |D|), N = S∖S0 (m = |N|), S⁻ = S0∖D.
price(k) = log[(2p−1−k)/(k+1)] + ½log(n+1). **Exact price of a rival** (prior × Occam at full Occam factor):

    Pr_n(d,m) := log[C(2p−1,s0)/C(2p−1,s0−d+m)] + ((d−m)/2)·log(n+1),   Pr_n(d) := Pr_n(d,0) = Σ_{k=s0−d}^{s0−1} price(k).

Pr_n(d,m) < 0 when m > d. R_n(S) = n·β_Dᵀ Σ_{DD·S} β_D; sample twin R̂(S) = ‖(I−P_S)μ‖²/σ². a_n denotes a sequence → ∞
arbitrarily slowly. log odds(S : S0) = Pr_n(d,m) − ½·(RSS_S − RSS_S0)/σ̂²·(1+o(1)) + (Occam and ridge corrections).

Three exact facts used repeatedly (fixed X, Gaussian ε):

- (F1) RSS_S − RSS_S0 = ‖P_G y‖² − σ²ω_N², where G = (I−P_S)span(X_D) ∋ (I−P_S)μ and ω_N² = ‖P_{(I−P_S0)X_N} ε‖²/σ² ~ χ²_m.
  Hence (RSS_S − RSS_S0)/σ² ≥ (√R̂(S) + z_S)² − ω_N², with z_S = ⟨u_S, ε⟩/σ ~ N(0,1) for each fixed S.
- (F2) RSS_S − RSS_S0 = ‖P_{F_D} y‖² − ‖P_{E_N} y‖², F_D = range(P_S0 − P_S⁻), E_N = (I−P_S⁻)span(X_N), and
  ‖P_{E_N} y‖/σ ≤ ρ̂_{D,N}·√R̂(S⁻) + χ_d + ω_N, where ρ̂²_{D,N} = 1 − R̂(S)/R̂(S⁻) (share of residual signal that N explains),
  χ_d = ‖P_{F_D}ε‖/σ does not depend on N, and ω_N is independent of P_S0 ε.
- (F3) Occam refund for deleting d variables is ≤ (n+1)^{d/2} for every design (Cauchy interlacing applied to
  f(λ) = ((n+1)λ+1)/(λ+1) ∈ [1, n+1], increasing). The full Occam factor (n+1)^{−m/2} on m added nulls needs
  λ_min(X_TᵀX_T) ≳ 1 on the sets involved — this is the only place NEC is needed.

---

## Q1. MARGIN form

### (1) Verdict

- **Unprovable as stated by the memo's route; false for fixed j0 in the super-polynomial regime; not falsified (and
  possibly true) with the size-tail j0 and p ≤ n^A.** Details in (3c)–(3d).
- (i) "a larger constant": yes if one wants a design-free statement — the right constant is 2(√d+√m)², not 2d, and it
  cannot be improved without design structure. (ii) "bounded confounding": yes, this is the condition that buys back
  the constant 2. (iii) Λ(S) → ∞: **not sufficient** (it ignores the cross term; the factor-proxy design below has
  Λ → ∞ and fails) and **not necessary** for isolated proxies (it charges m·log p where nothing is owed).
- Constant 2 **is sharp** for single deletions, in the strong sense given in (3a).

### (2) Recommended assumptions

**MARGIN\* (headline; constant 2+η).** There exist η > 0, sets Q_n ⊇ S0 with log|Q_n| = o(log(p∨n)), and ϑ_n ≥ 0 with
ϑ_n ≤ min{ η²/(64·j0·(1+η)²), log n/(5·log p) } such that, for all large n:

- (M1) for every B ⊆ Q_n with S0 ⊄ B and |B| ≤ s0 (so m_B ≤ d_B):
  R_n(B) ≥ (2+η)·σ*²·max{ Pr_n(d_B, m_B), ϖ_n },   with ϖ_n → ∞ and ϖ_n ≥ C₀·j0·log|Q_n|;
- (M2) for every B ⊆ Q_n with S0 ⊄ B, |B∖S0| ≤ j0, and every N ⊆ Q_nᶜ with |N| ≤ j0:  R_n(B ∪ N) ≥ (1 − ϑ_n)·R_n(B).

No condition is needed on rivals with m_B > d_B inside Q_n (by (F1) their likelihood gain is at most ½ω², which is
o(price) over Q_n, and they pay (m−d) prices). Reading: Q_n is the set of variables allowed to act as proxies for true
ones; outside Q_n nothing explains more than a ϑ_n share of any residual signal. Q_n = S0 gives "no proxies"; AR(1)
with parameter ρ: Q_n = S0 ± L neighbours, ϑ ≈ ρ^{2L} [H]. For the rate n^{−c} on the underfit mass take ϖ_n ≥ C·log n.

**MARGIN-U (fallback; design-free).** For every S with D ≠ ∅ and m ≤ j0:

    √R_n(S)/σ* ≥ (1+η)·[ √( (2·Pr_n(d) − m·log(n/(C·log p)))₊ ) + √(2m·log p) ],

implied by R_n(S) ≥ 2(1+η)²·(√d+√m)²·σ*²·price_n. This is the honest explicit replacement for c1(s0,A).

**Necessary condition [N1].** For every rival S with D ≠ ∅ and m ≤ d: √R_n(S)/σ* − √(2·Pr_n(d,m)) → ∞
(for d = m this reads R_n(S) → ∞). Nothing is necessary for m > d.

### (3) Proof steps

**(3a) Pure deletions — where constant 2 comes from, and why it is sharp [P].** For S = S0∖D,
(RSS_S − RSS_S0)/σ² = (√R̂_D + z_D)² + χ²_{d−1}, so log odds(S0∖D : S0) ≤ Pr_n(d) − ½(√R̂_D + z_D)²(1+o(1)) (refund ≤ (n+1)^{d/2}
by (F3)). There are only 2^{s0} − 1 directions u_D, so max_D |z_D| ≤ a_n w.h.p. Therefore:

- sufficient for the whole deletion family: √R_n(S0∖D)/σ − √(2Pr_n(d)) → ∞ for every nonempty D ⊆ S0;
- if some j has R_n(S0∖{j}) ≤ (2−η)σ²·price then odds(S0∖{j} : S0) → ∞, so π(S0|y) → 0 in probability;
- if √R_j/σ − √(2·price) → c ∈ ℝ then P(π(S0|y) ≤ ½) → Φ(−c) > 0.

So 2 is sharp, the sharp scale is √R − √(2Pr) (not (R − 2Pr)/log n, see Q2), and **all D, not only singletons**, must be
quantified: Pr_n(d) is superadditive-ish in d while R_n(S0∖D) can be far below Σ_{j∈D} R_n(S0∖{j}) for correlated true
predictors. The worker's S1 table shows exactly this (κ_multi < κ_del, binding rival "del3").
Linearisation needed: (n/2)·log(1 + W/n) = W/2 − W²/(4n) + …; for the fixed-η form log p = o(n) suffices, for the sharp
form (log(p∨n))^{3/2} = o(n).

**(3b) Supersets — design-free given NEC [P].** For S = S0 ∪ N, RSS_S/RSS_S0 ~ Beta((n−s0−m)/2, m/2) exactly. For m = 1 the
tail of the likelihood ratio is exactly Pareto in the exponent: P((RSS_S0/RSS_S)^{n/2} > x) ≍ x^{−(1−(s0+2)/n)}/√(log x), so the
expectation is infinite and the argument must be run on truncated sums, not on E. Results:

- P(some one-null extension beats S0) ≈ (s0+1)/√(2πL(n+1)), L = 2·log((2p−s0−1)/(s0+1)) + log(n+1);
- total mass of one-null supersets = O_P((s0+1)·√(log p/(πn))), matching `rem:sharp`'s lower bound;
- m-null supersets: mass ≲ [C·(s0+m)·√(log p/n)]^m/m! × exp(m(s0+m)·price/n) — the last factor is the Beta-vs-χ² correction
  and is e^{O(m)} as long as (s0+m)·price ≤ c·n. For fixed m this needs only log p = o(n).

**(3c) Mixed rivals — where the cross term bites [P].** Two routes, two different costs.

*Route U (uses F1).* Sum over N of size m with D fixed. On the event max_N |z_S| ≤ x_m := √(2m·log p) + a_n (union over
C(p,m) directions): Σ_N odds(S:S0) ≤ exp{Pr_n(d) − ½(min_N √R̂(S) − x_m)²} · Σ_N exp{−(m prices) + ½ω_N²}, and the last sum is
O_P((C·log p/n)^{m/2}) by (3b). This gives MARGIN-U. The cost √(2m·log p) is the Gaussian width of {u_S : |N| = m}.
**It is attained**: factor-proxy design, s0 = 1, x₁ = f, x_l = ρf + √(1−ρ²)w_l. Swap {l} beats S0 iff
g_l > (θ + z₁)·√((1−ρ)/(1+ρ)), θ² = R̂(∅), so the true threshold is R_n(S_swap) ≥ 2(1+ρ)²·log p, → 8·log p as ρ → 1
(per-rival exponent R/(2(1+ρ)²), down to R/8). Equicorrelated design: threshold R_n(∅) ≥ 2·log p/(1−ρ).
[N] `swap_check.py` (n = 200, p = 20000, 100 reps), P(some same-size swap beats S0) at κ_swap := R(S_swap)/(2·price) =
1.2, 1.6, 2.0, 2.6, 3.2: ρ = 0: 0.16, 0.03, 0, 0, 0; ρ = 0.5: 0.69, 0.37, 0.15, 0.05, 0; ρ = 0.8: 0.99, 0.84, 0.49, 0.14,
0.07 — with no deletion beating S0 at ρ = 0.8. Predicted κ_swap threshold at ρ = 0.8: 6.48·log p/(2·price) ≈ 2.4.

*Route L (uses F2).* With leakage ρ̂ ≤ ρ̄ for all N outside Q_n:
Σ_N odds ≤ exp{Pr_n(d,m_B) − ½R̂(B)(1−ρ̄²) + ρ̄·√R̂(B)·x_m + o(R̂)} · O_P((C·log p/n)^{m/2}). With R̂(B) ≥ (2+η)·Pr and Pr ≥ log p the cross
term is ≤ R̂·√(ϑ·j0), absorbed when ϑ ≤ η²/(64·j0·(1+η)²). When d_B = m_B (R may be ≪ log p) use
√(2ϑ·m·R·log p) ≤ R/4 + 2ϑ·m·log p and pay the second term from the Occam credit (m/2)·log(n/(C·log p)); this is the
ϑ_n ≤ log n/(5·log p) clause. Inside Q_n all unions cost only √(2·j0·log|Q_n|) = o(√log(p∨n)), absorbed by η or by ϖ_n.
Sample ρ̂ for pure-noise nulls is ≈ √(m·log p/n), giving a cross term m·(log p)^{3/2}/√n: absorbed by fixed η once
j0·√(log p/n) ≤ c(η). This gives MARGIN*.

**(3d) Status of the memo's literal MARGIN [C].** Because the memo quantifies over all |N| ≤ j0 and charges d·price with
no discount for m, it forbids designs in which j0 nulls jointly proxy a true variable. In the factor-proxy family
(multiple R² of f on m proxies = mρ²/(mρ²+1−ρ²)), MARGIN at m = j0 forces R_n(∅) ≥ (2+η)·price·(1 + j0ρ²/(1−ρ²)), and a
single swap still wins iff (1+ρ)²/(1+(j0−1)ρ²) > (1+η/2)·price/log p. The left side is maximised at ρ = 1/(j0−1) with
value j0/(j0−1). A second family (proxies sharing a common nuisance direction, idiosyncratic share γ²) gives the same
supremum j0/(j0−1). So in both families:

    memo's MARGIN is insufficient  ⇔  1/(j0−1) > η/2 + log n/(2·log p)   (up to 1+o(1)).

- Fixed j0, log n = o(log p), η < 2/(j0−1): **counterexample** (all other assumptions hold; eigenvalues ≥ 1−ρ²).
- p ≤ n^A and j0 − 1 ≥ (2A+1)·s0: 1/(j0−1) < 1/(2A), **no counterexample from these families**.

Why it may be true in general: for d = m = 1, either the proxy directions at confounding level ≥ ρ contain j0 that are
pairwise κ-separated — then their average is a strong joint proxy and MARGIN at m = j0 is violated — or a maximal
κ-separated set has < j0 elements, so all such directions lie in < j0 caps and their Gaussian width is at most
√(2(1−κ²)·log p) + O(√log j0). Optimising κ reproduces j0/(j0−1). I have **not** proved this for general (d,m) or without
the orthogonal idealisation. Recommendation: do not rest the headline theorem on it; record it as a remark/conjecture,
or as a proof-phase stretch goal ("separated proxies ⇒ joint proxy" dichotomy lemma).

**(3e) Hidden coupling to the dimension.** j0 is not free: rivals with m > j0 are handled without any signal, by
exp(d·price)·(C·log p/n)^{m/2} → 0, which requires m > s0·2·price/log(n/(C·log p)). So j0(n) ≈ s0·(1 + 2·log p/log(n/log p)) + 1:
fixed iff p ≤ n^A, growing otherwise. Outside the polynomial regime (M2)/(MARGIN-U) must be stated for |N| ≤ j0(n).

**(3f) The sufficiency gap [H][N].** P(report = S0) ≈ [1 − (s0+1)/√(2πL(n+1))] · Π_D Φ(√R̂_D − √(2Pr_n(d))) (lower bound:
1 − superset term − Σ_D Φ(−c_D)). `superset_term.py`, exact-Beta one-null term: S1-like (n,p,s0) = (500,500,10) 0.056;
(500,5000,10) 0.053; (1000,500,10) 0.036; (1000,5000,10) 0.033 — i.e. a ceiling of 0.94–0.97, against the observed
0.92–0.98. S2-like: (50,354,5) 0.22; (50,354,10) 0.57; (50,1012,10) 0.65; (100,1000,5) 0.10; (100,1000,10) 0.25 — against
P(exact | margin) = 0.45. Single-deletion factor Φ(√(2·price)(√κ−1)) at κ = 1, 1.25, 1.5, 2, 3: 0.50, 0.68, 0.81, 0.95,
0.998 (n = p = 500). So "min t² > 2·price necessary, not sufficient" is what the theory predicts; no extra assumption.

### (4) Referee risk
MARGIN*: **medium**. The constant is sharp and interpretable, but (M2) is a new-looking structural condition; mitigate
with worked examples (orthogonal, AR(1), block, equicorrelated with small ρ) and the necessity result [N1]. MARGIN-U:
**low** risk on correctness, **medium** on "constants far from the empirical transition" (factor up to 4 for single
swaps) — but the factor-proxy example shows it is unimprovable design-free, which is a publishable answer in itself.
Memo's literal MARGIN: **high** (proof route does not deliver it; false for fixed j0 at large p).

### (5) Precedent
In-house: `asm:reported-fixed` / `asm:rf-leak` (visibility + bounded leakage with a set Q). Literature, all [V]: Chen &
Chen (2008) EBIC identifiability condition (deletion-type margin over models up to a multiple of s0); NH14 Condition
4.4; YWJ15 (8) beta-min with explicit constant and their sparse-projection condition; Wainwright (2009, IEEE-IT) for
necessity of 2σ²·log p-scale signals. I know no precedent that states the swap threshold 2(1+ρ)²·log p.

---

## Q2. Order form vs explicit constant; covering S1

### (1) Verdict
An order-form theorem plus a calibrated companion is defensible in principle, but **the two order forms in the memo
are the wrong objects and both exclude S1**. Along S1, R/price is constant, so "ratio → ∞" (MARGIN-H) fails and
"(R − 2σ²d·price)/log n → ∞" either fails or holds only because of the fixed ratio. The second is also stronger than
needed: the sharp constant-free form is √R − √(2Pr) → ∞, equivalently (R − 2Pr)/√Pr → ∞.

### (2) Recommended framing
Triangular arrays (β*_n, Σ_n, p_n) with the **margin ratio**

    κ_n := min_{∅≠D⊆S0} R_n(S0∖D) / (2σ*²·Pr_n(|D|))      (plus the proxy part (M1)–(M2) of MARGIN*).

**Threshold theorem (T-SEL-b).** (A) liminf κ_n > 1 [+ (M1), (M2), NEC, DIM′] ⇒ π(S0|y) → 1 in probability,
P(HPM = MPM = S0) → 1, and 1 − π(S0|y) = O_P((s0+1)·√(log p/n)) + (p√n)^{−(κ_n−1)(1+o(1))}. (B) limsup κ_n < 1 ⇒ π(S0|y) → 0 in
probability. S1 is then a family of sequences with κ_n → κ_∞(SNR): the worker's cells give κ_del ≈ 0.19, 0.76
(SNR 0.5, 1; 0% exact) and ≈ 2.9–3.2, 6.5–7.2 (SNR 2, 3; 92–98% exact), i.e. S1 brackets the threshold from both
sides. The posterior rate √(log p/n) is kept whenever R ≥ 2Pr_n(d) + (1+η)·log n.

**Companion.** Not a fitted constant: the derived finite-n bound of (3f), stated as a proposition with explicit
remainder terms (superset term + Σ_D Φ(−(√R̂_D − √(2Pr_n(d))))). Suggested extra evidence: S1 cells at SNR 1.25 and 1.5
(κ just above 1), where the bound predicts 0.5–0.8, to show the transition is where the theorem says.

### (3) Proof step
(A) is (3a)–(3c) with fixed η = liminf κ_n − 1. (B): for the minimising D, χ′²_d(R̂_D) ≤ R̂_D + O_P(√R̂_D + d), so
log odds(S0∖D : S0) ≥ (1 − κ_n + o_P(1))·Pr_n(d) → +∞. Rate: odds = exp{−(κ_n−1)Pr_n(d) + O_P(√Pr_n)}.

**T-SEL-a is inherently constant-lossy.** For Gaussian x and any f supported on S (free σ_S), exact computation gives
d_H²(f, f*) ≥ 1 − (1 + R_n(S)/(2nσ*²))^{−1/4} ≈ R_n(S)/(8nσ*²) [P]. For sub-Gaussian x the same order holds by
Paley–Zygmund: d_H² ≥ c(L)·min{1, R_n(S)/(nσ*²)} [P, constant to audit] — so SL Condition 3 is *implied* by SUBG and need
not be assumed. Explicit MARGIN-H: for each j ∈ S0, inf{R_n(S) : j ∉ S, |S| ≤ q_n} ≥ C_H(L)·M·σ*²·log(p∨n). C_H comes from
the contraction/testing constants and is not sharp, so T-SEL-a covers S1 only above an inexplicit SNR. Say so plainly;
its role is "SL Thm 3 counterpart, per predictor, no proxy condition", and T-SEL-b carries the sharp claim.

### (4) Referee risk
Fixed-ratio framing: **low** (it is the standard phase-transition format). Order-form MARGIN-H with "→ ∞": **medium**
(a referee will ask whether the simulation design satisfies it; it does not).

### (5) Precedent
Threshold-style statements for exact support recovery: Wainwright (2009), Ji & Jin (2012), Butucea, Ndaoud, Stepanova &
Tsybakov (2018) — all [V]. SL Thm 3's proof (read): d² ≥ min{δ_n, β_t²δ_n/(20σ²), 1−√0.8}, same structure as ours.

---

## Q3. Dimension

### (1) Verdict
(a) log p = o(n) is **not** enough for T-SEL-b as coded. (b), (c): same for T-DIST and T-MIS. p ≤ n^A is not forced by
anything; what is forced, by the present proof route, is (log p)² = O(n).

### (2) Recommended DIM′ (all five theorems, as coded with K = n/2)

    DIM′:  s·M·log p·log(p∨n) ≤ c_dim·n     (headline form: (log p)² = o(n) for fixed s, M),

with rate ε_n = √(M·log(p∨n)/n) and window q_n ≍ s·M·log₂(p√n). This contains SL Cor S1's quasi-polynomial range
p < n^{κ·log n}, but not SL Cor 1's α ∈ [½, 1) — SL get that range only because they cap the model size (r̄_n).
**Optional DIM″ (if Engineering accepts a cap):** K_n ≤ c·n/log p gives log p = o(n) for T-DIST/T-SEL-a, and for T-SEL-b
with the margin quantified over |N| ≤ min{j0(n), K_n}. Note: S2 cells with s0·log p/n = 0.69 sit outside such a cap.

### (3) Where each candidate obstruction does or does not bite [P unless marked]
- IG(a0,b0) envelope: no constraint (only shifts n/2 to n/2 + a0 and adds 2b0 to Q_S).
- (n/2)·log RSS linearisation: log p = o(n) (fixed η) or (log(p∨n))^{3/2} = o(n) (sharp form).
- Supersets of fixed size: log p = o(n) (exact Beta law, (3b)).
- R-transfer on (s0+j0)-sets: (s0+j0)·log p = o(n). Gaussian rows: R̂(S) = R_n(S)·χ²_{n−|S|}/n exactly.
- **Size tail — the bottleneck.** Fubini: E*[m_S(y)/f*(y)] = 1 for every S, and m_S0/f* ≥ c·n^{−s0/2} w.h.p., so
  E*Π(|S| ≥ q | y) ≲ Π(|S| ≥ q)/(π(S0)·n^{−s0/2}) ≍ 2^{−q}·p^{s0}·n^{s0/2}: sizes are ≤ q_n ≍ s0·log₂(p√n) for any p. But for
  j0 < m ≤ q_n the Occam factor (F3) and the Beta correction need sample control on q_n-sets, i.e. q_n·log p ≤ c·n.
  That is DIM′. Without NEC (prop:dist(ii)) the rate² becomes M·(log p)²/n — the same restriction.
- A union-bound-only size tail fails altogether for sizes k ≳ n·log n/(2(log p)²) (the gain exponent k·log(ep/k)·
  (1 + k·log(p/k)/n) overtakes the prior), so the Fubini identity is essential with K = n/2. [N] `greedy_tail.py`
  (pure noise, greedy path, n = 400, p = 160000): log odds vs the empty model −2.9, −42.5, −212, −1077 at sizes
  1, 10, n/4, n/2 — no empirical sign of large-model dominance; the limit is of the proof, not of the method.
- j0(n) coupling (3e): under DIM′, j0(n) ≍ s0·log p/log n is allowed to grow; state it.

A "few lost Occam factors" small-ball lemma might relax q_n·log p ≲ n; I could not close it and it still leaves a gap
between n·log n/log p and s0·log p. [C] — do not promise it.

### (4) Referee risk
DIM′: **low–medium**. It is weaker than the current p ≤ n^A and honest; a referee comparing with SL Cor 1 will ask
about α ≥ ½ — answer with the cap remark. Claiming log p = o(n) without a cap: **high**.

### (5) Precedent
NH14 model-size cap m_n(ν) = p ∧ n/((2+ν)·log p) (PRECEDENTS); SL r̄_n and Cor S1 (read); YWJ15 [V for the journal
version]; Jiang (2007) for the prior-tail device [V].

---

## Q4. Eigenvalue conditions

### (1) Verdict
Yes: drop EFS and drop FLOOR-S0. Keep **NEC** and the margin. FLOOR-S0 is implied where it matters:
R_n(S0∖{j}) = n·β_j²·Var(x_j | x_{S0∖j}), so the margin already bounds every used conditional variance from below.

### (2) Recommended assumption
NEC: λ_min(Corr(x_T)) ≥ c_ψ/n for all |T| ≤ q_n (population), plus SUBG in **Σ-relative** form on q_n-sparse directions:
‖⟨x,v⟩‖_ψ₂ ≤ L·(vᵀΣv)^{1/2} for q_n-sparse v. Nothing else.

### (3) Proof steps
- R-transfer needs only a *lower* sparse isometry: R̂(S) = min_b ‖X(β_D, −b)‖²/σ² ≥ (1−δ)·R_n(S)/σ² on the event
  ‖Xv‖² ≥ (1−δ)·n·vᵀΣv for all (s0+j0)-sparse v, which holds w.h.p. when (s0+j0)·log p ≤ c·δ²·n under Σ-relative SUBG —
  no eigenvalue floor enters. ((M2) transfer also uses the upper isometry: ρ̂² ≤ ϑ + 2δ.)
- NEC is used once: the full Occam factor on added nulls, (F3). The floor is set by the unit ridge
  (need λ_min(X_TᵀX_T) ≳ 1), hence c_ψ/n in correlation scale. Without it, a null nearly collinear with the current
  model pays almost no Occam price and one-null supersets keep non-vanishing mass — so NEC is not removable.
- Deletions need no floor at all: the refund is ≤ (n+1)^{d/2} unconditionally (F3).

### (4) Referee risk
**Low.** A vanishing floor is weaker than everything in the literature; sample floors (thm:post-fixed) should be
demoted to a remark, with the S2 fact (greedy sample floor ≈ 1e−4/1e−5) as the reason — tag (b).

### (5) Precedent
SBJ Assumption 4, NH14 Condition 4.5 (PRECEDENTS); SL (22)→(26) (read: SL themselves call (22) "hardly satisfied");
RZ / RWY for the isometry transfer (arXiv versions verified in PRECEDENTS; journal versions [V]).

---

## Q5. Sparsity and signal size

### (1) Verdict
Keep s0 fixed in the headline; add a remark on growth. BS can be weakened.

### (2) Recommended assumptions
SPARSE: s0 fixed. Growth remark (T-SEL-b): s0²·log p = o(n), s0·(log p)² = o(n), log s0 = o(η·price).
**BS′:** (a) β*ᵀΣβ* ≤ M_μ·σ*² (allow M_μ ≍ log(p∨n) if the rate is restated); (b) max_j |β*_j|·sd(x_j) ≤ b̄_n·σ* with
s·b̄_n² = o(n).

### (3) What breaks with s0 → ∞ [P/H]
- Superset mass (s0+1)·√(log p/(πn)) → 0 forces s0²·log p = o(n); `rem:sharp`(a) alone forces s0 = o(√n). So
  π(S0|y) → 1 is impossible beyond s0 ≪ √(n/log p), whatever the proof. (MPM = S0 survives longer, see Q8.)
- Size window q_n ≍ s0·log₂(p√n) with q_n·log p ≲ n: s0·(log p)² = O(n).
- Union over the 2^{s0} deletion sets: max_D |z_D| ≲ √(2·log C(s0,d)) must be o(η·√price): log s0 = o(η²·price) per deleted
  variable — harmless.
- The 2^{−k} size prior is not the obstacle; BB(1,p) puts mass ≈ 2^{−s0−1} on size s0, which the Fubini bound absorbs.

BS′ use: (a) bounds m_S0/f* from below (Fubini denominator) and keeps σ̂² in a fixed range; (b) is needed only for the
unit-ridge term ‖β̂_S0‖²/(n+1) in Q_S. I could not see the proofs: **verify at proof audit** that no step uses
coordinatewise boundedness beyond this.

### (4) Referee risk
Fixed s0: **low** (SL (4), NH14 4.3). BS′: **low**; BS as coded: **low–medium** ("why bounded signals?").

### (5) Precedent
YWJ15 (7a) (PRECEDENTS, arXiv), NH14 Condition 4.3, CSV15 Thm 5 for growing s0 in a different prior class.

---

## Q6. Misspecification

### (1) Verdict
- f₀ = φ(y; β^{Cᵀ}x_C, σ_C) ⊗ ν is the KL projection under (i), (ii) and (iii) alike (second-moment identity).
  Note E[u·x_C] = 0 holds by definition of β^C, so option (ii) is "moments only".
- (iii) excludes Grünwald–van Ommen (GvO) trivially; T-MIS-a is literally T-DIST on the candidates.
- (i) excludes GvO (homoscedastic, ϱ ≡ 1). Reachable, but **not by the current route unchanged** — see (3c).
- (ii) does **not** exclude GvO. It is fine in fixed dimension and fails in high dimension beyond a computable budget.
- T-MIS-b survives option (i) with the same constant 2, under (log p)³ = o(n) and the size cap of (3c).

### (2) Recommended statements
- **T-MIS-a0 (literal SL Thm 4 counterpart).** Candidate dimension p_C fixed, i.i.d. rows, E‖x_C‖² < ∞, E y² < ∞, Σ_C
  nonsingular. Then Π(d_H(f, f₀) > ε | D_n^C) → 0 a.s. for every ε > 0. With E[x_j²·u²] < ∞ also π(supp β^C | y) → 1 a.s.
  (stronger than SL Cor 2's inclusion).
- **T-MIS-a / T-MIS-b under (iii)** (current): T-DIST / T-SEL-b assumptions on (x_C, β^C, σ_C²). In the omitted-variable
  setting (iii) holds iff (x_C, x_M) is such that x_M | x_C is Gaussian-linear-homoscedastic — jointly Gaussian is the
  natural case.
- **Extension under (i′)**: u independent of x_C, mean 0, sub-Gaussian with variance-proxy ratio
  ϱ̄ := ς²/σ_C² ≤ 1 + (1−ε)·log n/(2·log p); plus CAP: K_n ≤ c_K·n·log n/(log p)²; plus (log p)³ = o(n) for T-MIS-b.
  In the omitted-variable setting (i) holds iff x_M = Λx_C + ξ with ξ independent of x_C (non-Gaussian allowed).
- **Remark under (ii)** (heteroscedastic): with ϱ_l := E[ẽ_l²·u²]/(E ẽ_l²·E u²) and ϱ̄ = sup_l ϱ_l over null directions,
  selection survives iff (ϱ̄ − 1)·log p < ½·log n. State as a remark with the counter-calculation, not as a theorem.

### (3) Proof steps
**(3a) T-MIS-a0 [P].** 2^{p_C} models; log m_S(y) = −(n/2+a0)·log(2b0+Q_S) − (|S|/2)·log(n+1) + O(1) and Q_S/n → σ_S² :=
min_b E(y − x_Sᵀb)² a.s. (SLLN, second moments). Models not containing supp β^C have σ_S² > σ_C² and lose exponentially;
those containing it share the KL projection f₀, and within each the conjugate N–IG posterior concentrates at
(β^C, σ_C²). Extra variables: n(σ̂²_S̃ − σ̂²_S)/σ̂² = O(log log n) a.s. (LIL, needs E[x_j²u²] < ∞) against (m/2)·log n. This is a
direct proof and avoids De Blasi–Walker; SL's proof also uses "only a fixed number of possible models" (read).

**(3b) Why (ii) fails in high dimension [H].** For a null direction ẽ_l, the gain is T_l ≈ ϱ_l·χ²₁ (sandwich variance
over model variance). P(some null beats the price) ≈ p·exp(−L/(2ϱ̄)) = p·(p√n)^{−1/ϱ̄}, which → 0 iff
(ϱ̄−1)·log p < ½·log n; above that the posterior spreads over ≈ p^{1−1/ϱ̄}·n^{−1/(2ϱ̄)} nulls. The **robustness budget is the
Occam slack** ½·log(1+g)/log p = 1/(2A) for p = n^A, and zero for log n = o(log p). This is the mechanism of GvO in our
model (their examples are heteroscedastic) [V]. A learning rate η < 1/ϱ̄ (SafeBayes) would restore control — remark
only, not as coded. In fixed dimension there is no multiplicity and (3a) applies.

**(3c) What changes under (i) [P/H].**
- The Fubini size-tail **breaks**: E*[m_S/f*] = 1 still holds, but m_S0(y)/f*(y) ≈ exp(−n·KL(h‖φ)) is exponentially
  small for non-Gaussian error law h, so the bound only gives sizes ≲ n·KL/log 2. This is the standard reason
  misspecified contraction needs different tests (Kleijn & van der Vaart) [V].
- Replacement: direct union bound on exact marginals with ‖P_S u‖² ≤ ς²·(k + 2√(kt) + 2t) (Hsu–Kakade–Zhang-type tail
  for sub-Gaussian vectors [V]). It works for sizes k ≤ c·n·log n/(log p)² and needs gain constant ϱ̄ < 1 + log n/(2·log p):
  hence CAP and the budget in (i′). TH_PREP reports the cap never binds on S1/S2, so CAP is empirically free (b).
- Sharp constant for T-MIS-b: deletions use only 2^{s0} directions (CLT suffices); one-null gains need
  P(⟨ê_l, u⟩² > 2·price) ~ Gaussian tail at x ≍ √log p, i.e. Cramér moderate deviations for delocalised weights,
  valid for x = o(n^{1/6}): (log p)³ = o(n) [V for the exact range]. Then ϱ̄ can be taken as 1 for fixed-size rivals.
- T-MIS-b's margin is MARGIN* on (μ_C = X_Cβ^C, σ_C²): same form, noise inflated to σ_C². TH_PREP E6 (posterior σ² ratio
  median 0.99 / 0.94) supports the inflated-variance reading (b).

### (4) Referee risk
T-MIS-a0: **low**. (iii): **low** on correctness, **medium** on "this is not really misspecification" — which is
why a0 and the (ii) remark should accompany it. (i′): **medium** (new CAP condition; variance-proxy budget).
Claiming anything under (ii) in high dimension: **high**.

### (5) Precedent (all [V] unless noted)
SL Thm 4 and supplement proof (read); De Blasi & Walker (2013); Kleijn & van der Vaart (2006, 2012); Berk (1966);
Grünwald & van Ommen (2017); Grünwald & Langford (2007); Grünwald & Mehta (2020, η-central condition);
Hsu, Kakade & Zhang (2012); Hanson–Wright (Rudelson & Vershynin 2013).

---

## Q7. SL items possibly missing

| SL item | Recommendation | Reason / how |
|---|---|---|
| Approximate sparsity (3) for T-DIST | **state as corollary** | change of measure: if the tail Σ_{j∉S_n} β_j x_j is sub-Gaussian with variance δ_n² ≤ c0·σ²·M·log n/n, the truth is within Hellinger c·ε_n of an s-sparse model; T-DIST then applies with f* replaced by its sparse surrogate [P, to audit] |
| Bounded predictors (Thm 1) | **dominated** | bounded ⇒ SUBG when variances are bounded below; one-line remark |
| a.s. mode (Thm 4) | **state** for T-MIS-a0; **remark** for T-DIST / T-SEL-a | Borel–Cantelli on a fixed-truth sequence when c_H·M > 1; not for T-SEL-b (superset mass is only O_P; SL Thm S is →_P too) |
| Condition 2 / (16) second-moment-only | **non-target with reason** | our rates use the exact-marginal route, which needs exponential tails on q_n-sets; T-MIS-a0 is the moments-only result we do state |
| Condition 5 / iterative screening | **non-target** | no screening step in the method as coded |
| Cor 1 rates | **target via DIM′** | matches n^{−(1−α)/2} up to logs for α < ½; state the gap α ∈ [½,1) and the cap remedy |
| Cor S1 | **dominated** | DIM′ ⊇ p < n^{κ·log n}; our conclusion π(S0|y) → 1 is stronger than pairwise MAP |
| Thm S pairwise MAP | **dominated** | by T-SEL-b |
| Cor 2 inclusion | **dominated** | by T-MIS-b (exact) |
| SAM consistency (informal, §3.1) | **dominated** | `lem:summaries` for HPM/MPM/PIP |
| §6 complexity; SAMC convergence | **deferred** | owner scope ruling on particle-limit results |

Risk: low. One caution: check that the approximate-sparsity corollary does not silently need p ≤ n^A.

---

## Q8. Engineering sensitivity

| Change | Form invariant? | What moves | New condition |
|---|---|---|---|
| Slab g (general) | yes | price_g(k) = log[(2p−1−k)/(k+1)] + ½·log(1+g); threshold 2·Pr scales with it; superset mass ≍ (s0+1)·√(log p/g); misspecification budget ϱ̄ < 1 + log(1+g)/(2·log p) | g/log p → ∞ (s0²·log p = o(g)). NEC floor stays c_ψ/n: it is set by the unit ridge, not by g |
| g = max(n, p²) | yes | price ≈ 2·log p when p² > n: required signal up by 2/(1 + 1/(2A)); superset mass ≍ √(log p)/p; budget ϱ̄ < 2 | none; a pure power-for-robustness trade |
| Size prior BB(1, b) | yes | odds of adding = (k+1)/(p−k−1+b), size ratio (p−k)/(p−k−1+b) | see next two rows |
| b = p^u, u < 1 | price changes by ≤ log 2 | **the 2^{−k} size tail is lost** (size ratio ≈ 1 − p^{u−1}) | Fubini size bound gone ⇒ need CAP K_n ≤ c·n·log n/(log p)² (union route) |
| b = p^u, u > 1 | yes | price up by (u−1)·log p; size tail p^{−(u−1)k} | none; DIM′ can relax toward log p = o(n) |
| PIP threshold q, HPM | yes | O(1) shift log(q/(1−q)) in the deletion statistic | none. MPM = S0 w.p. → 1 needs only s0/√(n·log p) → 0 + margin, weaker than π(S0|y) → 1 |
| Cap K | yes | must have K ≥ s0 + j0(n) | K_n ≤ c·n/log p unlocks DIM″ |

**Flag for the Lead.** TH_PREP's sensitivity note and memo Q8 say u < 1 leaves an "uncancelled multiplicity" / needs
price ≥ (1+ε)·log p. For the beta-binomial BB(1, p^u) that is not what the formula gives: the per-variable prior odds stay
≈ (k+1)/p. The p^{(1−u)}-per-variable deficit belongs to an independent Bernoulli(p^{−u}) prior. Please verify which
prior Engineering means; the consequences are different (price deficit vs lost size tail).

Irreducible part: the log p in the price. Our single-deletion threshold 2σ²(log p + ½·log n) is within a factor
1 + 1/(2A) of the exact-recovery limit (√(2·log(p−s)) + √(2·log s))² for fixed s [V]. Risk: low.

---

## Final recommended assumption lists

Tags: (a) precedent, (b) empirical (S1/S2), (c) mild technical. "→" marks the proof step.

**T-DIST** — rate ε_n = √(M·log(p∨n)/n)
- GL: i.i.d. rows, Gaussian noise. (a) SL. → exact marginals; Fubini identity.
- SPARSE: ≤ s nonzeros, s fixed. (a) SL (4), NH14 4.3. Corollary: approximate sparsity (Q7).
- DIM′: s·M·log p·log(p∨n) ≤ c·n. (c); (a) contains SL Cor S1's range. → sample control on q_n-sets.
- SUBG (Σ-relative, q_n-sparse directions). (a) SL Condition 1; RZ/RWY. → isometry on sparse sets.
- NEC: λ_min(Corr(x_T)) ≥ c_ψ/n, |T| ≤ q_n. (c); (a) weaker than SBJ A4 / NH14 4.5 / SL (26). → Occam factor (F3).
- BS′: β*ᵀΣβ* ≤ M_μσ*², s·b̄_n² = o(n). (c); (a) YWJ15 (7a). → Fubini denominator, ridge term.
- Evidence (b): d_H < ε_n in all 136 settings (TH_PREP).

**T-SEL-a** — sure screening, per predictor j
- T-DIST assumptions, plus
- MARGIN-H (explicit): inf{R_n(S) : j ∉ S, |S| ≤ q_n} ≥ C_H(L)·M·σ*²·log(p∨n). (a) SL Condition 3 + Thm 3 proof (ours is
  implied by SUBG, so only the size of R is assumed). → d_H² ≥ c(L)·min{1, R/(nσ²)} + T-DIST + size window.
- No proxy condition, no FLOOR, constant inexplicit. Say that it does not cover S1's boundary cells.

**T-SEL-b** — π(S0|y) → 1, P(HPM = MPM = S0) → 1, rate O_P((s0+1)√(log p/n)) + (p√n)^{−(κ_n−1)(1+o(1))}
- GL, SPARSE (s0 fixed), DIM′, SUBG, NEC, BS′ as above.
- MARGIN*: liminf κ_n > 1 over **all** nonempty D ⊆ S0, with (M1) on the leakage set Q_n and (M2) bounded leakage
  outside it, for |N| ≤ j0(n). (b) S1 brackets κ = 1 (0% at κ ≤ 0.76; 92–98% at κ ≥ 2.9); multi-deletions bind on S1;
  (a) in-house asm:rf-leak; Chen–Chen / NH14 4.4 / YWJ (8) [V]. → (3a) deletions, (3c) mixed rivals.
- Alternative for a design-free statement: MARGIN-U with 2(1+η)²(√d+√m)². (c). → (3c) Route U; unimprovable.
- Converse (no extra assumption): limsup κ_n < 1 ⇒ π(S0|y) → 0. Finite-n companion: proposition of (3f).
- Removed: FSb, EFS, FLOOR-S0, sample floors, c1(s0,A). (b) sample floors are vacuous on S2.

**T-MIS-a0** — literal SL Thm 4 counterpart, a.s.
- p_C fixed; i.i.d.; E‖x_C‖² < ∞, E y² < ∞; Σ_C nonsingular; π(S) > 0. (a) SL Condition 4. For exact support selection
  add E[x_j²u²] < ∞. (c).

**T-MIS-a** — density consistency to f₀ at the T-DIST rate (high-dimensional candidates)
- Option (iii): T-DIST assumptions on (x_C, β^C, σ_C²) with a Gaussian-linear-homoscedastic working residual.
  (a) SL f₀; holds under joint Gaussianity (ex:omitted).
- Optional extension (i′): u ⟂ x_C sub-Gaussian with ϱ̄ ≤ 1 + (1−ε)·log n/(2·log p); CAP K_n ≤ c_K·n·log n/(log p)².
  (c); (b) cap never binds on S1/S2. Not as coded (cap is n/2): needs an Engineering decision or stays a remark.
- Remark, not theorem: under (ii) the budget (ϱ̄−1)·log p < ½·log n and the GvO mechanism.

**T-MIS-b** — exact selection of supp β^C
- T-SEL-b assumptions on the candidate problem with (μ_C, σ_C²): MARGIN* in σ_C² units. (b) posterior σ² ratio median
  0.99 (S1) / 0.94 (S2). Under (i′) add (log p)³ = o(n). Same constant 2.

## Items I could not verify — please route

1. Proofs of thm:dist / prop:dist were not visible to me: confirm the size tail is the Fubini argument and that BS is
   used only where Q5(3) says.
2. (3d) is a conjecture; (3f) and (3b)-under-(ii) are back-of-envelope; the three scripts are scratch.
3. Every item marked [V]; in particular the GvO setting, the Cramér range, the HKZ tail constant, and the
   exact-recovery threshold.
4. The BB(1, p^u) point in Q8 contradicts TH_PREP — needs a second pair of eyes.
5. Cheap worker checks that would strengthen the package: (i) S1 cells at SNR 1.25 / 1.5; (ii) per-cell comparison of
   observed exact share with the (3f) bound; (iii) κ over all D (not only singletons) as the reported margin statistic;
   (iv) a factor-proxy toy cell (ρ = 0.8) showing swaps beating S0 at κ_del ≫ 1.
