# W3-POST — R02 adversarial re-check (Claude Opus 5.5, high, council level)

Scope: STATEMENT.md (v1.0, as on disk 2026-11-09 16:20, card ref `04_theory.tex:780-788`), lemmas/L1a_size_tail.md
(as on disk, Remarks 2/5 carrying [R01-*] tags), [T03R] PROOF.md (§§1–7, full), [P1] PROOF_v3.tex (full), [P3]
PROOF_v2.tex (full), [POST] L1_POST.md, [SL] I4_SL_corollaries.md §§0–2, [UNI] §3(i), 00_COMMON §1,
`v3_score.h:40-71,175-225`, `v3_preprocess.R:35-130`. No prior review verdict or status line was used as evidence. I did
not read R01/R03.
Numerics (mine, independent of `numerics/post_exact.py`): `R02_scratch/tail_checks.py` → `tail_checks_out.txt`;
`R02_scratch/post_checks.py` → `post_checks_out.txt`.

**Bottom line.** I tried to break the chain at every place listed in the brief and did not find a false load-bearing
step. Every "verbatim/unchanged" claim of [T03R] that I checked against [P1]/[P3] is true under the weakened hypotheses
SE_λ(j₀) and SE_w(m♯_n; g₀). The constants (C_A, τ_j, δ_n, ε_n, q_n, K_{s₀,j}, ρ_n) are uniform in m♯_n = O(log n).
All findings are about statement wording and scope: **0 FATAL, 0 MAJOR, 4 MINOR, 7 NIT**.

---

## 1. Verdicts per component

| Component | Verdict |
|---|---|
| [T03R] Lemma E1, E2 (exact tail, cutoff location) | **VERIFIED** (E2 needs ω ≥ 0 and s₀ ≥ 1; STATEMENT drops these, see F5) |
| [T03R] T02(i♯) (= Lemma 1a), incl. Lemma den′ | **VERIFIED** |
| [T03R] Lemma B (B1)–(B3) (and Lemma I) | **VERIFIED** |
| [T03R] T02(ii♯) | **VERIFIED** |
| [T03R] T03♯ (C1)–(C10) and Assembly | **VERIFIED** (NIT F7 on the wording of (C2)) |
| [P1]/[P3] steps relied on as "unchanged" | **VERIFIED**: each cited step uses at most R on S₀, (B1), (B2), or no eigenvalue condition |
| [POST] L1_POST (random-design bridge) | **VERIFIED-WITH-AMENDMENTS** (F4 scope of 5(b); F10 nit) |
| [SL] SL0, SL1, SL1′ | **VERIFIED** |
| L1a′ (new lemma) | **VERIFIED** (proof correct; F1 and F5 concern the statement and Remark 4) |
| STATEMENT fidelity (π vs code; hypotheses used vs hypotheses stated) | **VERIFIED-WITH-AMENDMENTS** (F1–F6, F8, F9, F11) |

---

## 2. Findings

### F1 — MINOR — STATEMENT.md:49-51 (Lemma 1a′, "every standardised design X whatsoever … s₀ may grow")
**What is wrong.** Condition (E) ‖μ‖² ≤ nM restricts the design jointly with θ*. Fixed s₀ and |θ*_j| ≤ θ_hi give
‖μ‖² ≤ (n−1)‖θ*‖₁² ≤ (n−1)s₀²θ_hi², so then M = s₀²θ_hi² works for every X. For growing s₀ this fails.
**Counterexample.** Make all s₀ columns of S₀ identical (standardised x) with θ*_j = θ_hi. L1a′ allows this: it has no
eigenvalue condition. Then μ = s₀θ_hi x and ‖μ‖² = (n−1)s₀²θ_hi². With s₀ → ∞, no fixed M satisfies (E). So the bold
claim "for every standardised design X whatsoever … for any s₀ ≤ K (s₀ may grow)" overstates the result. The lemma
itself (lemmas/L1a_size_tail.md:8-17) states (E) correctly.
**Fix.** "…for every standardised design X with ‖Xθ*‖² ≤ nM (automatic with M = s₀²θ_hi² when s₀ is fixed), uniformly
over such X for fixed (σ*², M, M′); s₀ may grow provided (E) holds."

### F2 — MINOR — STATEMENT.md:61-64, 95-96 ("anchored" floors; interface property), ASSUMPTION_MAP rows POST-Fλ/Fw
**What is wrong (misleading, not false).** Interlacing (Lemma I, [T03R]:136) shows that "anchored" relaxes less than the
name suggests. Every S with |S| ≤ j₀ satisfies S ⊆ S₀ ∪ (S∖S₀) with |S∖S₀| ≤ j₀. So **(F_λ) implies λ_min(R_S) ≥ φ₀² for
every S with |S| ≤ j₀**, including sets that contain no truth. In the same way, **(F_w) implies λ_min(G_S) ≥ g₀ for
every |S| ≤ m♯_n**. The anchoring relaxes only the sets of size j₀+1 … s₀+j₀ (resp. m♯_n+1 … s₀+m♯_n).
**Concrete consequence.** Two exactly duplicated null columns x_a = x_b (a, b ∉ S₀) violate (F_λ) for every φ₀ > 0:
take J = {a, b}, |J| = 2 ≤ j₀. Hence Theorem 1 does not cover null–null duplicates or near-duplicates at any fixed
size ≤ j₀. This is consistent with ASSUMPTION_MAP E3 ("improvable on null-only directions"), but a reader of "anchored
floor" would expect such designs to be covered.
**Fix.** Add after (F_w): "By interlacing, (F_λ) ⇒ λ_min(R_S) ≥ φ₀² for all |S| ≤ j₀, and (F_w) ⇒ λ_min(G_S) ≥ g₀ for
all |S| ≤ m♯_n; anchoring relaxes only larger sets." State the same in ASSUMPTION_MAP POST-Fλ/POST-Fw.

### F3 — MINOR — STATEMENT.md:78-79 (item 5(a) title "No false positives beyond the truth")
**What is wrong.** T02(ii♯) controls only π(S ⊋ S₀). Under 5(a)'s hypotheses (no BM), the posterior can still put most
of its mass on models that contain a false positive and are not supersets, e.g. S₀∖{j} ∪ {k}. The lead's own E5
(ASSUMPTION_MAP, POST-BM′) has max_{j∉S₀} PIP_j → 0.99 with E, F_λ, F_w holding. The title says more than the result.
**Fix.** Retitle it "No strict-superset mass (no inflation of the true model)". Keep the "Not claimed" sentence.

### F4 — MINOR — STATEMENT.md:83-89 (item 6 includes 5(b)); L1_POST.md:31-33, 68
**What is wrong.** (i) Item 6 assumes fixed |β_j| ≥ b_lo > 0 (or θ*_j ≥ θ_lo). Then J_n(c) = S₀ for large n, and
5(b) adds nothing beyond item 1. (ii) The intended no-beta-min version, L1_POST(b) "without beta-min (θ*_j allowed to
vary, some → 0) the inclusion clause … holds likewise", is stated inside a Setting (L1_POST.md:11) that assumes
θ*_j ∈ [θ_lo, θ_hi]. The claim and the assumptions disagree. (iii) J_n(c) uses φ₀, and item 6 never says which φ₀ is
meant. [POST] uses φ₀² := φ²/2.
**Proof check.** Without θ_lo, steps (2)–(4) of [POST] still give (E) with M = s₀²θ_hi²+1, F_λ, and F_w on 𝒜_n, and
T03♯(iv) needs no beta-min. So the diagonal transfer does give the no-beta-min J_n(c) clause. The mathematics holds;
only the statement is wrong.
**Fix.** In item 6 add: "and, keeping only |β_j| ≤ b_hi (no lower bound), 5(a) and 5(b) hold with φ₀² := φ²/2 in
J_n(c)". In L1_POST(b), state the no-beta-min clause with θ_lo dropped from the Setting. (5(a) also transfers, since it
needs only E, F₀ and F_w; item 6 currently omits it.)

### F5 — NIT — STATEMENT.md:32-33 ("Always … m♯_n(ω) ≤ min{K, s₀ + ⌈…⌉}"); L1a_size_tail.md:56-57 (Remark 4)
[T03R] E2 (PROOF.md:50) assumes ω ≥ 0 and s₀ ≥ 1 for (ii). For ω < 0 the right side can fall below s₀ while
m♯_n ≥ s₀ by definition. Exact computation: n = 3, p = 2, s₀ = 1, ω = −20 gives m♯ = 1 > RHS = −25 (356 such cases
in `tail_checks_out.txt`, all with ω < 0). Remark 4 of L1a′ applies E2(ii) with t possibly 0, which E2 does not cover.
In 2100 cases I found no violation for s₀ = 0, ω ≥ 0, but nothing proves it.
**Fix.** "For ω ≥ 0 and s₀ ≥ 1 (E2(ii))". In Remark 4 add "t ≥ 1".

### F6 — NIT — STATEMENT.md:31 ("Size cutoff (data-free, computable)")
m♯_n is a deterministic function of (n, p, s₀, K). It is data-free but needs the unknown s₀, so a user cannot compute it.
**Fix.** "data-free (a deterministic function of n, p, s₀)".

### F7 — NIT — [T03R] PROOF.md:174 ((C2) "(G3) uses (B1)")
The probability bound for (G3) needs only rank ≤ |J| (stochastic domination, [P3] lem:chi(a), last claim). The exact
χ²_{|J|} law from (B1) is needed only in (C5)(b), for the truncated MGF. Harmless, but it inflates what (B1) is used
for.

### F8 — NIT — STATEMENT.md:17-24 vs `v3_preprocess.R:111-112` and `v3_score.h:213-224`
The code silently drops exactly constant raw columns, so the theorem's p is the retained count. It also replaces Q by a
nonnegative recomputation when Q < 1e-8·yᵀy, and throws on numerical failure. These are EX-A idealisations. Otherwise π
matches the code exactly: K = min(p, n/2) with integer division, ν = a₀ + n/2, log w(k) = −log 2 − log C(2p−1, k),
W_K, H = (n+1)G + I, A = G + I, logm = logC_n − ½(log det H − log det A) − ν log(2b₀ + Q), and response sd with
divisor n − 1. **Fix.** One clause in §0: "p = number of non-constant raw columns; exact arithmetic (EX-A)".

### F9 — NIT — STATEMENT.md:78-79 (5(a) "needs only G, (E), λ_min(R_{S₀}) ≥ φ₀², (F_w)")
5(a) also uses p ≤ n^A (the union bounds of [P1] lem:good) and fixed s₀ (n₀). Both are in R1, which governs the whole
theorem. Saying "in R1" inside the parenthesis would make the list complete.

### F10 — NIT — L1_POST.md:63-65 (diagonal argument)
"Completing with arbitrary x_n ∈ 𝒜_n at the other indices" needs 𝒜_n ≠ ∅ for all n ≥ n₀. That holds because
P(𝒜_n) → 1, but it should be said. The argument is otherwise valid: the negation of "∃M_η, n_η: sup_{x∈𝒜_n} P(…) ≤ η"
does produce n_k ↑ ∞ with M = k.

### F11 — NIT — STATEMENT.md:95-96 (interface property)
"All design assumptions enter through AF (with (E))" is slightly overstated. (BM) and J_n(c) are also (X, θ*)
conditions, through φ₀ and, on the raw scale, θ* = D_xβ*. Lemma 1a′ bypasses AF entirely. **Fix.** "…enter through AF,
(E) and (BM)".

---

## 3. Steps checked and found correct (coverage)

**Target / reduction (brief items (b), (c), (i)).**
- [P1] lem:slab: completing the square, the variational form Q = min_θ{‖Y−Aθ‖² + θᵀ(G+I)θ/n}, the determinant
  factor D^{−1/2}.
- [P1] prop:closed and thm:T01i: the n-dim IG(0.01, b₀) likelihood factor equals the (n−1)-dim contrast factor times
  IG(0.51, b) times a constant. Hand-checked: (2πv)^{−n/2}IG(v; 0.01, b) = (2πv)^{−(n−1)/2}(2π)^{−1/2}Γ(0.51)b^{−1/2}/Γ(0.01)·IG(v; 0.51, b).
  ν = 0.51 + (n−1)/2 = 0.01 + n/2. **Numerically:** log m_code(S) − log m^c_{b₀s_y²}(S) is constant over all 2⁵
  feasible models, spread 2.5·10⁻¹⁴, on a design with a near-collinear pair (`post_checks_out.txt`).
- Data-dependent standardisation: Π(·|y) = Π_{b₀s_y²} exactly. thm:T01ii is pointwise in (y_c, b), so thm:Ta applies
  at the observed rate on 𝓑_n. lem:num is used only at the data-free rate b₋, and den′ only at the data-free b₊. T03♯
  and T02(ii♯) need no transfer: the rate is common to all models, and they use only 2b ≥ 0, the b = 0 monotonicity
  ([P1] lem:one), and b ≤ 6b₀(M+σ*²) on 𝒢_n. **Every use is legitimate.**
- thm:T01iii: Var(Δ_n), the symmetry argument for the cross moment, 𝓑_nᶜ ⊆ {|Δ_n| > σ*²/2}, and the constant
  (8 + 24M/σ*²)/(n−1).
- n vs n−1 in [P3]: νn/((n+1)N) = ½(1 + (0.02n+1)/(n²−1)) (checked by algebra), and [P1] lem:one's
  ϑ_n ≥ 1 ⟺ n(n+0.02) ≥ n²−1.
- Code fidelity: see F8. Everything else matches.

**Size tail (brief item (a)).**
- E1(a)–(d) algebra, including the i = 0 factor and the sum Σ(i−1). **Numerically, exact log-sum:** E1(b) upper and
  E1(c) lower bounds hold in every one of ~2100 (n, p, s₀, m) cases, with n up to 10⁴ and p up to 2000.
- E2(i), (ii) under ω ≥ 0, s₀ ≥ 1 (numerically no violation; F5 for ω < 0).
- Lemma den′: the exponent lower bound (both inequalities, using 1/u ≥ 2 − u and 0 ≤ u−1 ≤ n^{−1/2}), restriction of
  the integral to [σ*², σ*²(1+n^{−1/2})] ⊆ [σ*², 2σ*²], the c_IG constant, D_{S₀} ≤ (n+1)^{s₀}, and EΛ_n ≤ C_Λ term
  by term.
- T02(i♯) assembly: v_m = R_mϖ(S₀), c♯ = κ²/(c_IGσ*²), the Markov split for L > c♯², the convention R_m = 0 ⇒ empty
  event, and the consequence at m = m♯_n(ω). The (1+1/n)^{s₀/2} factor is ≤ e^{1/4} since s₀ ≤ K ≤ n/2.
- **L1a′:** y_c − X_{c,T}θ = ε_c (since X_cθ* = Uᵀμ), Q^c_T ≤ σ*²E′ + (‖μ‖² + ‖θ‖²)/n, and Λ′ and EΛ′ ≤ C′_Λ. Only
  T ∈ Ω is needed in thm:Ta. **Numerically:** (i) the Q-bound held in every draw, max excess ≤ −0.04, on a
  near-collinear pair with θ = (L, −L) up to L = 300 and 1−corr down to 10⁻⁶. (ii) The full den′ inequality
  m^c_{b₊}(T)/f₀ ≥ D_T^{−1/2}c_IGσ*²n^{−1/2}e^{−Λ′} held by quadrature, minimum ratio 16.7 (n = 20), with no failure
  at larger n (`post_checks_out.txt`). Remark 1 (L1a′ ⇒ Lemma 1a with M′ = M/(2φ₀²)) is correct. Remark 3 (no
  diagonal argument needed) is correct: the bound is uniform in X and ε ⫫ X.

**Middle range j₀ < |J| ≤ m♯_n (brief item (e)).**
- Lemma B(B1): full rank from SE_w, projection rank |J|, exact χ²_{|J|}, and [P1] lem:spec(e) with g = g₀
  (interlacing proof re-done). **Numerically:** for a 6-column design with λ_min(G_{S₀∪J}) ≈ 2.2 (normalised ≈ 2.2/n),
  log D_{S₀∪J} − log D_{S₀} − |J| log((n+1)/(1+1/g₀)) ≥ 1.35 at n = 30, 100, 400.
- (B3): M_T ⪯ n/(n+1)·P_T always, and M_S ⪰ (1−η_n)n/(n+1)·P_S on S only. **Numerically:**
  t_S − t_{S₀} ≤ n/(n+1)[‖(P_S−P_{S₀})y_c‖² + η_n‖P_{S₀}y_c‖²] in 600 draws on that near-singular superset (max excess
  −2.5·10⁻⁵).
- (C4): the exact ratio identity from [P3] eq:score; the numerator from (B3) with R on S₀; the denominator from
  lem:ongood(b), which uses only (G1)–(G2) with rank ≤ |T|; log(1+x) ≤ x; lem:ongood(d), whose bound
  8n³/((n+1)²N²) ≤ 1/N I re-checked.
- (C5): the weights (n+1)^{−j/2}(1+1/g₀)^{j/2}e^{jε_n} are deterministic because m♯_n is. The term-wise expectation is
  2(j+1)^{s₀}q_n^j. q_n² = c_q²r_n²·(n/(n+1))·e^{2ε_n}/4. K_{s₀,j₁} is summed to ∞, so it is independent of m♯_n.
  The expectation uses linearity only (no union bound). Markov gives (c).
- (G1)–(G4) and lem:Gprob: the (G2) threshold 2k + 3x_k ≤ C_Ak log n with C_A = 8 + 3A; the (G3) union over ≤ p^j sets;
  the (G4) count (j₀+1)p^{j₀}2^{s₀}, with N_S/σ*² stochastically ≤ χ²_{s₀} without any eigenvalue condition. Total 5/n.
- Uniformity in m♯_n: m♯_n ≤ m_n(½ log n) ≤ C_m log n (E2(i)). δ_n log n → 0, ε_n → 0, q_n ≤ c_q r_n. Every n₀
  depends on (s₀, A, φ₀, σ*², M, g₀) and, under BM(c), on c.
- (C8): each S′ = S₀ ∪ J′ arises from ≤ 2^{s₀}−1 underfitting S, |J′| ≤ |S| ≤ m♯_n, and the rate exponent satisfies
  (j₀+1)/2 ≥ s₀(A+½) + 1. So n^{As₀}(n+1)^{s₀/2}n^{−(j₀+1)/2} ≤ 2^{s₀/2}n^{−1}, and the term is o(r_n).
- Hidden-SE audit of [P3] and [P1]. The only uses of SE beyond S₀ are: the §sec:good paragraph (→ (B1), (B2));
  lem:ongood(c) (→ (C3), restricted to |J′| ≤ j₀, which is the only range where (C6)(b) and (C7) need it);
  lem:onesup (→ (C4)); cor:diff in lem:SvsSp (→ (B2)); lem:signal (→ (B2)); and [P1] lem:one's determinant (→ (B1)).
  No other step uses an eigenvalue condition. lem:ongood(a), (b), (d), lem:prior, lem:chi and lem:det (upper part)
  use none.
- Under F_w, every model of size ≤ m♯_n has λ_min(G_S) ≥ g₀ by interlacing (F2). So no rank-deficient model below the
  cutoff exists (brief item (d)). Rank deficiency above the cutoff is handled by T02(i♯), which needs no condition on
  those models. Rank deficiency on the S side of an underfitting comparison needs no condition, since
  D_{S′}/D_S ≤ (n+1)^{|J|} always ([P3] lem:det, first part).

**Underfitting and beta-min (brief item (f)).**
- (C6)(a): prior ratio ≤ (2p)^{|J|} ([P3] lem:prior(a), |S′| ≤ p), D_{S′}/D_S ≤ (n+1)^{|J|} unconditionally, and
  Q^c_{S′} ≤ Q^c_S; this holds for every data set.
- (C6)(b), (C7), (C10): lem:SvsSp (n ≥ 4 for n²/(4(n+1)) ≥ n/5; the δ″_n ≤ 1 step), lem:signalgain
  (log 2 + ½ log(n+1) ≤ log n for n ≥ 5), and Step 1 with L_* ≥ 4C_* and L_*/32 ≥ s₀(A+1) + 2. BM(c):
  (1−1/n)c ≥ L_* for n ≥ c/(c−L_*). c₀ = 128 at s₀ = A = 1 (4C_* ≈ 99.3), matching ASSUMPTION_MAP.
- (iv) without BM: U_j bounded via θ*_j alone, uniformly in j, with |J_n| ≤ s₀.

**Random design (brief item (g)).**
- [POST] step (1): C(p,k)/C(2p−1,k) ≤ (2/3)^k and R_m ≤ 2(2p)^{s₀}(2/3)^m. **Numerically,** m♯_n ≤ max(s₀, m̄_n) in
  every case with A ∈ {1, 1.5, 2}, n ≤ 10⁴, p ≤ 20000, s₀ ≤ 4. Also k̄_n ≥ s₀ + m♯_n because j₀ > s₀.
- Step (3): ‖·‖₂ ≤ |S|·max-entry, ε_n = O((log n)^{3/2}/√n) = o(ψ_n), and (n−1)ψ_n/2 ≥ 1.
- Step (4): ‖μ‖² ≤ (n−1)s₀‖θ*‖² ≤ ns₀²θ_hi², and H_n gives θ_lo = b_lo/2, θ_hi = 2b_hi.
- Step (5): ε ⫫ X gives the correct conditional law, and the diagonal argument is valid (F10). With unit population
  variances, raw β is on the population-standardised scale, which matches item 6.

**Corollaries (brief item (h)).**
- SL0(i)–(v), and SL1(a)–(e) under any law. STATEMENT items 2–4 are exactly SL1(a)–(e) with r_n = √(log n/n).
- Item 1 = T03♯(i), using F_λ (incl. J = ∅), F_w, E and BM. Item 5(a) = T02(ii♯): verified to need no SE_λ beyond S₀
  and no BM (F9). Item 5(b) = T03♯(iv). Item 5(c) = T02(i♯)/L1a′. Item 6 = [POST](b), with the scope remark F4.
  **Hypotheses used = hypotheses stated**, apart from F1, F4 and F9.

**Not checked.** The UNI-P restatement beyond §3(i) lines 86-91; GROW L6.2 beyond the entrywise-event paragraph
(standard Gaussian sample-correlation concentration); Proposition D and E3 (not used by Theorem 1).
