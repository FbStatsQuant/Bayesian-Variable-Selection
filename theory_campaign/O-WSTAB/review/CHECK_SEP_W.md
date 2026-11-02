# O-WSTAB review — independent check of REPORT.md §3.2–3.7 (Lemma W2, Prop L, Prop G, Lemma SEP, Theorem W, Theorem W′)

Reviewer: independent checker (Opus 5.5, laptop, 1 core, seed 20261102). Object: `theory_campaign/O-WSTAB/REPORT.md` at
commit b3d89e2. Inputs read: REPORT.md; PROOF.md §0, §1 (WS1), §2 (read in passing, only WS2(c) used), §3 (WS3), §6 (WS6);
`Docs/Theory/theorems/00_COMMON.md` §1–3. Nothing else. I did **not** read [FD] (F-DRAFT), T13, T22, T03 or W1-EXP; any
step resting on them is marked "not seen".

Scripts (written for this review; they do not import `wstab_core.py`, so they are an independent implementation from
00_COMMON's definitions):
- `review/check_sep_w2.py` → `review/check_sep_w2.txt`: brute-force enumeration (p ≤ 10).
- `review/check_W_constants.py` → `review/check_W_constants.txt`: Mills/Chernoff/order-statistic constants, an
  independent large-(n, p) evaluation of the W(e) multi-extra bound, and the arithmetic for finding F1.

Severity scale: **fatal** (a stated result is false or its proof cannot be repaired locally), **gap** (a step does not
follow as written; the result may still be true), **exposition** (wrong or missing detail that does not affect the
result).

---

## 1. Findings

### F1 — Theorem W(d), upper side: the hypothesis p^r/√n → 0 does not give q(2) → 0. Severity: **gap**
*Location.* §3.6 (d), first line: "By (b) at w = 2, q(2) ≤ V_n p^r√(log p)/√n = o(1)." Statement §2 Theorem W(d) and
Headline item 3 ("if p^r/√n → 0, then p^{r−ε}/√n ≤ χ² ≤ p^{r+ε}/√n …, both sides PROVED").

*Claim.* The bound from (b) is V_n·ρ_n(2)·√(log p). The hypothesis of (d) is only ρ_n(2) = p^r/√n → 0. These do not
imply V_n p^r√(log p)/√n → 0. Take r ∈ (½, 1) fixed and p^r = √n/log log n. This is allowed by H-ORTH:
p ≤ n^{1/(2r)} with 1/(2r) < 1, so p log p = o(n). Then ρ_n(2) = 1/log log n → 0, but
ρ_n(2)√(log p) ≍ √(log n)/log log n → ∞. In this window Lemma SEP's
hypothesis q(2) < 1 is not established, (b) gives no finite bound on ℓ(2), and the upper half of (d) is not proved.

*Evidence.* `check_W_constants.txt` block (D), r = 0.9:

| log₁₀ n | ρ_n(2) = p^r/√n | ρ_n(2)·√(log p) |
|---|---|---|
| 10 | 0.319 | 1.08 |
| 40 | 0.221 | 1.56 |
| 160 | 0.169 | 2.41 |

*Scope.* The upper half of (d) is proved, by the report's own argument, under the stronger hypothesis
p^r√(log p)/√n → 0 (e.g. p ≤ n^{1/(2r)−δ}). The lower half of (d) is unaffected. Theorem W′ and W(f) do not use (d).
*Remark (not a fix; for the author).* The loss is in (HT): at a fixed exponent a > 1 the truncated moment is
m·E[e^{aZ²/2}1{Z² ≤ 2 log m}] ≍ m^a/((a−1)√(log m)), not m^a√(log m). Block (E) of `check_W_constants.txt` shows the
exact ratio to m^a falling like 1/√(log m) (0.266, 0.177, 0.122, 0.085 at m = 10³, 10⁶, 10¹², 10²⁴) while HT's factor
grows (2.97 → 8.39). So the window looks closable at w = 2, but HT's uniformity in a near 1 is then lost; that is the
author's call.

### F2 — Theorem W(d), upper side: e^x − 1 ≤ 2x is applied to a bound that need not be small. Severity: **exposition**
*Location.* §3.6 (d): "ℓ(2) ≤ … ≤ p^{r+ε/2}/√n … χ² ≤ e^{ℓ(2)+ℓ(0)} − 1 ≤ 2(ℓ(2) + ℓ(0))". Under p^r/√n → 0 the
quantity p^{r+ε/2}/√n can tend to ∞ (p^r = √n/log n), so "≤ 2(ℓ(2)+ℓ(0))" is not justified from the displayed
chain. It is justified from the sharper intermediate bound ℓ(2) ≤ O_P(p√n e^{−c₀n}) + 2(s₀+1)q(2) → 0 (when q(2) → 0,
i.e. outside F1's window), after which χ² ≤ 2(ℓ(2)+ℓ(0)) ≤ p^{r+ε}/√n follows. Order of the steps should be swapped.

### F3 — Theorem W(e): the displayed constant is not what the proof gives. Severity: **exposition**
*Location.* Statement (e) "log(1+χ²) ≥ e^{(L_n − C₁ − 1)/r}"; proof end of (e).
The proof gives log(1+χ²) ≥ ℓ(2) − 2ℓ* ≥ k_n(1 − o_P(1)) − o_P(1) with k_n = ⌊e^{(L_n−C₁−1)/r}⌋, which is
(1 − o_P(1))·e^{(L_n−C₁−1)/r}, strictly less than the stated right side in general. A correct form is, e.g.,
log(1+χ²) ≥ e^{(L_n−C₁−2)/r} w.p. → 1 (since e^{−1/r} < 1). The headline's "≥ c·e^{L_n/r}" and every asymptotic use
(n^{A−1/(2r)−o(1)}, the counterexample) are unaffected.

### F4 — Prop G: the upper bound is false as written when g₋ = ∞. Severity: **exposition**
*Location.* §2 Prop G, "T ≤ ⌈log₂(1 + 1/g₋)⌉ (with 1/∞ := 0)". If g₋ = ∞ the right side is ⌈log₂ 1⌉ = 0, but T ≥ 1.
(g₋ = ∞ is possible in principle: ℓ is convex and ≥ 0 and may stay ≤ c − ℓ* on [1, ∞) when S° maximises d.) The proof
gives T = 1 in that case (e₁ ≤ max{0, (1 − g₋)/2} = 0). Should read T ≤ max{1, ⌈log₂(1+1/g₋)⌉}. Only Theorem W′ uses
Prop G, and it only needs "g₋ ≥ 1 ⇒ T = 1" and "g₋ > 1/3 ⇒ T ≤ 2", which the proof gives, so W′ is unaffected.

### F5 — Lemma W2: y ≥ 0 is asserted without proof. Severity: **exposition**
*Location.* §2 Lemma W2 "y ∈ [0, 1)"; §3.2 proves only y < 1. y ≥ 0 needs t_{T+l} ≥ t_T. Verified here: by Woodbury (Lemma 0's proof) Q_S = yᵀ(I + nX_S(G_S+I)⁻¹X_Sᵀ)⁻¹y and
X_S(X_SᵀX_S+I)⁻¹X_Sᵀ = I − (I + X_SX_Sᵀ)⁻¹ is nondecreasing (Loewner) when columns are added, so Q_S is nonincreasing
and t_S = yᵀy − Q_S nondecreasing. So the claim is true; one line is missing. (Also κ ≥ 0 uses x̄ ≥ x_T, which is
x̄ = Σ_c x_c(S°) ≥ x_b(S°) = x_T: true, unstated.)

### F6 — Theorem W′, g₊ step: sign of the constant. Severity: **exposition (harmless)**
*Location.* §3.7 *g₊*: the condition for ρ_n(1+g)(log p)^{−(1+r)/2}e^{−U_n} > K, K := e^{c+2ℓ*} − 1, is
gr log p > ½ log n + ((1+r)/2) log log p + U_n + **log K**; the report writes + log(1/K). Since K < 1, log(1/K) > 0 >
log K, so the report's condition is stronger than needed and still sufficient. δ₊ = O_P(log log p/log p) unchanged.
Similarly, |δ₋| = O_P(log log p/log p) needs log V_n bounded below; take V_n ≥ 1 w.l.o.g. (it is an upper-bound
variable). Neither changes any conclusion.

### F7 — Lemma SEP proof: (F2) is cited where only g′ ≥ 1 is used. Severity: **exposition**
*Location.* §3.5, end of the w ∈ [1, 2] case: "− ν[g(s) − g(a)] ≤ − νX_M (F2)". This is g′ ≥ 1 on [a, s] (F1), not
(F2). Correct either way.

### F8 — Counterexample: the [FD] statement and hypotheses were not seen. Severity: **gap (scope of the claim only)**
*Location.* §2 "Counterexample W(c)"; Headline item 4.
What I verified: the formula **as quoted in REPORT** — log(1+χ²) = [r log p − ½ log n]₊ + O_P(log log p) — is
contradicted by Theorem W(e) (verified below) under H-ORTH with p = n^A, A ∈ (1/(2r), 1) (so r > ½; A = 1 is excluded
because H-ORTH needs p log p = o(n)): L_n = (Ar − ½) log n − ((1+r)/2) log log p → ∞, and W(e) gives
log(1+χ²) ≥ (1 − o_P(1))e^{(L_n−C₁−1)/r} = n^{A−1/(2r)−o(1)}, which is not [Ar − ½]log n + O_P(log log n). Likewise the
quoted W(b) bound 1+χ² ≤ 1 + p^{r+ε}/√n + o(1) fails there. What I could **not** verify: that [FD] W(c) is stated with
R² = r and under hypotheses that include H-ORTH (fixed s₀ and θ*, ORTH, p log p = o(n)); [FD] is not among my inputs.
Independent numerics agree with the direction: at n = 10¹⁶, p = n^{0.95}, r = 0.9, s₀ = 2, my own implementation
(singleton blocks, s = r, ζ_n = 0, top 20 000 order statistics) gives exact multi-extra lower bound
LB = 7 961 nats with k* = 9 267, against [FD]'s 13.08 (REPORT reports 8 770 with its own realisation and exact s, ζ;
same order). Note that the *rigorous* W(e) bound at this (n, p) is only e^{(L_n−C₁−1)/r} = 8.9 < 13.08: the finite-n
contradiction is numerical, the proved contradiction is asymptotic. (`check_W_constants.txt` block (C).)

---

## 2. Line-by-line record of the steps checked and verified

### §3.2 Lemma W2
- t_{S°+l} − t_{S°} = t_{T+l} − t_T under BO (WS3(a), seen) ✓. d = ν[g(x̄) − Σ_c g(x_c)] is WS3(b) rewritten ✓.
- g(a+δ) − g(a) = −log(1 − δ/(1−a)) = g(δ/(1−a)) ✓; δ/(1−x̄) = y ✓; δ/(1−x_T) = y(1−x̄)/(1−x_T) = (1−κ)y ✓.
- κ ∈ [0,1) (x̄ ≥ x_T, x̄ < 1) ✓; y < 1 ⇔ x_{S°+l} < 1 ✓; y ≥ 0: F5.
- G = νg(y): log BF difference = −½ log(D_{T+l}/D_T) + νg(y) by Lemma 0 + WS3(a) ✓.
- Lower bound: g convex, g(0) = 0 ⇒ g((1−κ)y) ≤ (1−κ)g(y) ✓. Upper: MVT with g′ increasing, then y ≤ g(y) ✓.
- Statistical reading: with T = ∅, κ = x_{S₀} = s; νy = νx_l/(1−s) = (Z_l²/2)(1+ζ_n) by (S2) (verified below), and
  g(y)/y = 1 + O(y), y = O_P(log p/n) uniformly ✓.
- Numerics (independent): 138 (S°, l) pairs, 6 BO designs with correlated within-block columns, n ∈ {60, 300, 2000}:
  0 sandwich violations; G = νg(y) and LR = ν[g(y) − g((1−κ)y)] reproduced to relative error 1.1·10⁻⁸.

### §3.3 Prop L
- (i) ℓ(φ) = Λ(φ) − φd(S°) + log(Z̄₀/γ₀(S°)) ✓ (from q_φ = γ₀e^{φd}/Z̄_φ); convex by Lemma Λ ✓; ℓ ≥ 0 ✓.
- (ii) WS1(a) at S = S° (seen, proof checked) ✓. V-restricted version: I did not see T13(iii), but the identity follows
  directly from 00_COMMON's ρ_V(u,v) = Z̄_v(V)²/(Z̄_u(V)Z̄_{2v−u}(V)) and q^V_φ(S°) = γ₀(S°)e^{φd(S°)}/Z̄_φ(V), since the
  γ₀e^{·d} factors cancel when u + w = 2v ✓.
- (iii) WS1(e) (concavity of log q_φ(S°)) ⇒ ℓ ≤ ℓ* on [0,1] ✓; both sides of the sandwich ✓.
- (iv) WS1(a)/WS6(a) at (0,1) ✓.
- Numerics: Prop L(ii) identity to 3.6·10⁻¹³ over 40 random (u, v) ∈ [−0.5, 1.5]² on a BO design.

### §3.4 Prop G
- Accept side: w ≤ 1 ⇒ ℓ(w) ≤ ℓ* < c − ℓ*; w ∈ [1, 1+g₋] ⇒ ℓ(w) ≤ max{ℓ(1), ℓ(1+g₋)} ≤ c − ℓ* (convexity, closed
  sublevel set) ✓; log(1+χ²) ≤ ℓ(u) + ℓ(w) ≤ c ✓ (ℓ(u) ≤ ℓ* since u ∈ [0,1]).
- v̄ > u accepted; maximum attained (continuity of ρ_Ω) ✓; e_t ≤ max{0, (e_{t−1} − g₋)/2} ✓;
  e_t + g₋ ≤ (e_{t−1}+g₋)/2 while e_t > 0 ✓; e_t ≤ (1+g₋)2^{−t} − g₋ ≤ 0 once 2^t ≥ 1 + 1/g₋ ✓ (edge case F4).
- Reject side: g₋, g₊ > 0 (ℓ(1) ≤ ℓ* < c − ℓ* by 2ℓ* < c, continuity) ✓; {w ≥ 1 : ℓ ≤ c+2ℓ*} = [1, 1+g₊] ✓;
  w > 1+g₊ ⇒ log(1+χ²) ≥ ℓ(w) − 2ℓ(v) ≥ ℓ(w) − 2ℓ* > c ✓; recursion and 2^T ≥ 1 + 1/g₊ ✓.
- Halving ✓.

### §3.5 Lemma SEP (crux 1)
- ORTH: H_S = ((n+1)(n−1)+1)I = n²I, G_S + I = nI, D_S = n^{|S|}, t_S = Σ_j z_j²/n ✓; log BF(U) =
  −(|U|/2)log n + νg(X_U) ✓; γ_w = ϖBF^w∏r_b^{1−w} ✓ and the log γ_w display ✓ (Σ_b|S_b| = |S|).
  Numerics: the display reproduces direct 00_COMMON scores to 3.4·10⁻¹¹ over 6 ORTH designs × 5 values of w × all 2^p S.
- (F1) ✓. (F2) left end: termwise g′ ≥ 1 ✓. Right end: X_{S₀∩C_b} ≤ s − M_{>b} because s ≥ X_{S₀∩C_b} +
  Σ_{c>b}X_{S₀∩C_c} ≥ X_{S₀∩C_b} + M_{>b} ✓; g′ increasing moves each length-X_{M∩C_b} interval right to
  [s − M_{≥b}, s − M_{>b}] ✓; these tile [s − X_M, s] = [a, s] ✓; all inside [0, s] ⊂ [0,1) ✓.
- (F3): h ≤ g(z+h) − g(z) ≤ h/(1−z−h), and 1 − z − h ≥ 1 − s − X_N = (1−s)(1−ū) ✓; applied with (z, h) = (a_b, e_b)
  and (a, X_E), both in range ✓.
- Exponent: Δ(S) display ✓ (|S| − s₀ = e − m). Case w ∈ [1,2]: rearrangement ✓, bound by (F2) right end and (F3) lower
  end ✓, then (F3) upper end with z = a and g(s) − g(a) ≥ X_M (F7) ✓, giving [w/((1−s)(1−ū)) − (w−1)]νX_E − νX_M =
  β(w)νX_E − νX_M ✓. Case w ∈ [0,1]: (F3) upper + (F2) left end on the block part, and the same on the w-part ✓;
  β(w) = 1/((1−s)(1−ū)) ✓; continuous at w = 1 ✓.
- Prior: w(k) = ½/C(2p−1,k) ⇒ ratio C(2p−1,s₀)/C(2p−1,s₀−m+e) ✓. First factor: the report's pairing
  ∏(2p−1−s₀+i)/(s₀−m+i) is not the termwise telescoping ∏(2p−s₀+m−i)/(s₀−m+i), but the two numerator multisets are
  both {2p−s₀, …, 2p−s₀+m−1}, so the products agree (checked: p = 5, s₀ = 3, m = 2 gives 56/6 = 84/9 both ways) ✓;
  each numerator ≤ 2p − 1 ⇒ ≤ (2p)^m ✓. Second factor: ∏_{i<e}(s₀−m+i+1)/(2p−1−s₀+m−i) ✓ (checked numerically for
  m = 2, e = 2: 6/56 = 9/84); denominators ≥ 2p − s₀ − e ≥ p iff e ≤ p − s₀ = |N| ✓.
- Sum: e^{Δ} ≤ ∏_{j∈M}(2p√n e^{−νx_j})·[(s₀+e)!/s₀!]∏_{j∈E}(c_j/p) ✓; extending from Ω to 2^{[p]} only adds positive
  terms ✓; Σ_M factorises ✓; e_e(x) ≤ (Σx)^e/e! for x ≥ 0 ✓; Σ_e C(s₀+e, e)q^e = (1−q)^{−(s₀+1)} ✓.
- s < 1 is automatic (s = x_{S₀} < 1 by Lemma 0); ū < 1 and q < 1 are hypotheses ✓.
- Numerics (independent): 30 (design, w) cases, all with finite bound; 0 violations (e.g. n = 40, p = 8: ℓ(2) = 0.673 ≤
  3.61; n = 20 000, p = 9: ℓ(2) = 0.104 ≤ 0.185).

### §3.6 Theorem W (crux 2)
- (S1): Z_j iid N(0,1) ✓; x_jᵀY = (n−1)θ*_j + σ*√(n−1)Z_j ✓; (n−1)s_y² = Σ_j(x_jᵀY)²/(n−1) + σ*²χ²_{n−1−p},
  independent ✓; s_y²Q̄(1−s) = 2b₀s_y² + σ*²W_n + Σ_{S₀}(x_jᵀY)²/(n(n−1)) — derived independently:
  s_y²Q̄(1−s) = 2b₀s_y² + (n−1)s_y² − Σ_{S₀}(x_jᵀY)²/n, and (x_jᵀY)²/(n−1) = σ*²Z_j² for nulls ✓; W_n ~ χ²_{n−1−s₀} ✓.
- (S2): νx_j/(1−s) = (Z_j²/2)·2ν(n−1)/[n(W_n + R_n)], R_n := [2b₀s_y² + Σ_{S₀}(x_jᵀY)²/(n(n−1))]/σ*² = O_P(1) ✓. ζ_n is
  one random variable for all nulls (it is **not** independent of the Z_j, since W_n contains them, but no step needs
  independence: it enters only through |ζ_n|) ✓. ζ_n = O_P(n^{−1/2}) ✓. s = r + O_P(n^{−1/2}) ✓. ū =
  (1+ζ_n)Σ_N Z_j²/(n+0.02) = O_P(p/n) ✓. Truth coordinates ✓.
- (S3): P(max_N Z² > 2 log m) ≤ (π log m)^{−1/2} → 0 ✓; Gumbel for N₀ ✓ (m₀ → ∞).
- (HT): E[e^{Z²/2}1{Z² ≤ τ}] = √(2τ/π) ✓; Markov ✓; on {max ≤ 2 log m}, e^{(a−1)Z²/2} ≤ m^{a−1} for every a ≥ 1, so the
  bound is simultaneous in a, which legitimately allows the random exponent a(w) + sup_w|η_n| ✓. (Loose by a factor
  ≍ log m at fixed a > 1 — see F1.)
- (a), (b): β(w)(1−s) = 1/(1−ū) (w ≤ 1) or w/(1−ū) − (w−1)(1−s) (w ≥ 1) — the displayed single formula
  "(1+ζ_n)[w/(1−ū) − (w−1)₊(1−s)]" is wrong for w < 1, but the next sentence corrects it (exposition, no effect) ✓;
  a_n(w) = 1 + (w−1)₊r + η_n(w), sup_w|η_n| = O_P(n^{−1/2} + p/n) ✓; m/p ≤ 1 and m^{(w−1)₊r} ≤ p^{(w−1)₊r} ✓;
  m^{|η_n|} → 1 needs (n^{−1/2} + p/n)log p → 0 ✓ (p log p = o(n)); single V_n for all w ✓; truth term
  O_P(p√n e^{−c₀n}) ✓; (a) via −log(1−q) ≤ 2q ✓.
- (c): ϖ ratio (s₀+1)/(2p−1−s₀) ✓; exact single-term ratio ✓; g(z) ≥ z and g(x) ≤ x/(1−x) used in the right
  directions for w ≥ 1 ✓; bracket ≥ 1 + (w−1)s − 2x_l (using (1−x_l)⁻¹ ≤ 1 + 2x_l for x_l ≤ ½ and w − 1 ≤ 1) ✓;
  argmax over N₀, Gumbel, m₀ ≥ p/2 ✓; constants (s₀+1)/(2·2^{a}) and (log m₀)^{−a/2} ≥ (log p)^{−a/2} absorbed in U_n,
  which does not depend on w (a(w)/2 ≤ (1+r)/2 bounds the Gumbel O_P(1)) ✓.
- (d) lower half: χ² ≥ π(S₀)²(1+O(2)) − 1 ≥ O(2) − 2(1−π(S₀))(1+O(2)) ✓; 1 − π(S₀) ≤ ℓ(1) ✓; O(2)/√(log p/n) ≥
  p^r(log p)^{−1−r/2}e^{−U_n} → ∞ ✓. Upper half: F1 (gap), F2 (exposition).
- (e) (crux): exact log-ratio ✓; ϖ-ratio ≥ k!/(2p)^k ✓; Σ_b g(X_{E∩C_b}) ≤ X_E/(1−X_E) ✓; bracket
  2 − (1−s)/(1−X_E) ≥ 1 + r − C(|ζ_n| + |s−r| + X_E) ✓; Σ_{E_k}Z² ≥ kZ²_{(k)} ✓.
  Order statistic: P(Z²_{(k)} < τ_k) = P(Bin(m₀, 2k/m₀) ≤ k−1) ≤ e^{−k/4} (Chernoff, δ = ½) ✓; τ_k ≤ 2 log m₀ ✓;
  Mills lower bound holds for τ ≥ 1 (proof: 1−Φ(t) ≥ φ(t)t/(1+t²)) ✓, and τ_k ≥ 2 because k_n = o(m₀) ✓;
  τ_k/2 ≥ log(m₀/(2k)) − ½ log(4π log m₀) ✓; Stirling ✓. I re-derived C₁ term by term:
  −1 (Stirling) − log 2 (from 2p) − (1+r)log 4 (m₀ ≥ p/2 and 2k) − ((1+r)/2)log(4π) = −C₁ ✓ exactly.
  k_n ≤ e^{L_n/r} = p n^{−1/(2r)}(log p)^{−(1+r)/(2r)} ≤ p n^{−1/(2r)} ≤ n^{1−1/(2r)} ≤ √n (r ≤ 1, p ≤ n) ✓;
  |η_{k_n}|log p ≤ C(n^{−1/2} + k_n log p/n)log p = o_P(1) ✓; s₀ + k_n ≤ K ✓; k_n ≤ m₀ ✓; probability
  1 − e^{−k_n/4} → 1 (k_n deterministic) ✓; final step via Prop L(iv) ✓. Constant in the statement: F3.
  Numerics: `check_W_constants.txt` (A) Mills margin ≥ 0.27 nats on [1, 400]; (B) Chernoff margin ≥ 1.75 nats,
  τ_k lower-bound margin ≥ 0.73, 2 log m − τ_k ≥ 4.27 over m ∈ {10³, 10⁵, 10⁸, 10¹²}, k ∈ {1,…,0.05m}.
- (f): TV ≤ ℓ* (WS1(d)) ✓; WS6(c) with θ = 1/log p ✓; ρ_n(1+θ) = e^r/√n ✓ so O(1+θ) = O_P(√(log p/n)) by (b), in
  every regime including (e) ✓; KL = O_P((log p)^{3/2}/√n) ✓.

### §3.7 Theorem W′ (crux 3)
- 2ℓ* < c w.p. → 1 from W(a) ✓.
- g₋: V_nρ_n(1+g)√log p ≤ c/(8(s₀+1)) ⇒ −(s₀+1)log(1−·) ≤ c/4 ⇒ ℓ(1+g) ≤ o_P(1) + c/4 ≤ c − ℓ* ✓, uniform in g because
  V_n and the o_P(1) do not depend on w ✓; solving for g gives G_n − δ₋ with the stated δ₋ ✓; restricted to 1+g ≤ 2 ✓.
- g₊: from W(c) with (log p)^{−(1+gr)/2} ≥ (log p)^{−(1+r)/2} ✓; condition (F6) ✓; sublevel-set argument ✓.
- Sandwich: G_n − δ₋ ≤ g₋ ≤ g₊ ≤ G_n + δ₊ ✓ (g₋ ≤ g₊ since c − ℓ* < c + 2ℓ*).
- Count: G_n ≥ 1/(2r) > ½ because p ≤ n − 1 and r < 1 ✓; min{1, G_n − δ₋} > 1/3 ⇒ T ≤ 2 ✓; 2Ar < 1 ⇒ g₋ ≥ 1 ⇒ T = 1 ✓;
  2Ar > 1 ⇒ g₊ < 1 ⇒ T ≥ 2 ✓. W′ uses W(b), W(c), W(a) and Prop G only, not W(d), so F1 does not reach it.
- The "ideal grid vs method grid" remark is labelled OPEN in the report and was not reviewed as a result.

---

## 3. Verdicts

| Result (REPORT §) | Verdict | Findings |
|---|---|---|
| Lemma W2 (§3.2), exact form and ORTH reading | **verified** | F5 (exposition) |
| Prop L (i)–(iv) (§3.3) | **verified** (V-restricted part checked from 00_COMMON's ρ_V definition, T13(iii) not seen) | — |
| Prop G (§3.4) | **verified**, with the upper bound read as max{1, ⌈log₂(1+1/g₋)⌉} | F4 (exposition) |
| Lemma SEP (§3.5) | **verified** | F7 (exposition) |
| Theorem W(a) | **verified** | — |
| Theorem W(b) | **verified** | — |
| Theorem W(c) | **verified** | — |
| Theorem W(d), lower half | **verified** | — |
| Theorem W(d), upper half | **not verified** as stated (verified under p^r√(log p)/√n → 0) | F1 (gap), F2 (exposition) |
| Theorem W(e) | **verified** in the form log(1+χ²) ≥ (1−o_P(1))e^{(L_n−C₁−1)/r} (stated constant off) | F3 (exposition) |
| Theorem W(f) | **verified** | — |
| Theorem W′ (§3.7) | **verified** | F6 (exposition) |
| Counterexample to [FD] W(c) | **verified** against the formula as quoted in REPORT, for A ∈ (1/(2r), 1); **not verified** that [FD]'s own statement/hypotheses cover H-ORTH ([FD] not seen) | F8 (gap, scope) |

No fatal findings.
