# W3-PSHARP — REPORT (to Theory HQ)

Ticket T3 of `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md`: three sharpness records for the posterior theorem.
Lead: Claude Fable 5.2 (claudeAgent, high). Branch `theory/W3-PSHARP`; folder `Theory_work/Wave3/W3-PSHARP/`.

**RESULT.** All three records are proved, each with its own status: **PROVED (by this seat, unchecked)** in the
protocol's wording, with the check record of §2 (statement lock, blind break review, two blind line checks; the
council verdict is recorded in `CHECKPOINT_2.md` and `reviews/`, outside this frozen file). They are lower bounds /
necessity statements, not new upper bounds, and all are asymptotic statements about the exact coded target π. No
claim of the registry is used in any proof (every proof starts from the definition of π), so nothing here is
conditional on a parent's status. The parents are only what is sharpened.

## 1. What is proved (`STATEMENT.md` v1.2.1)

**Lemma S** (`lemmas/S_one_step.md`; deterministic, any design, any data). Adding one column j to a model S:
D_{S∪{j}}/D_S ≤ n (equality iff x_j ⟂ col X_S — improves the n + 1 of Proposition LB), and
Q_S − Q_{S∪{j}} = n(x_jᵀρ̃_S)²/s_{S,j}. Hence, for every S₀ with s₀ + 1 ≤ K,
δ_n/(1 − δ_n) ≥ [(s₀+1)/(2p−1−s₀)] n^{−1/2} Σ_{j∈𝒩} e^{νγ_j} — the one-step superset mass **with the fit factor kept**.

**(a) Claim A — the √(log p) factor is attained** (`lemmas/A_log_factor.md`). Under G, (E) ‖μ‖² ≤ nM, (C) ‖θ*‖² ≤ nM′,
and a null block 𝒩_n (N_n → ∞) that is either
- (W-orth) orthogonal and orthogonal to col X_{S₀} (fixed design; N_n ≤ n − 1), or
- (W-sph) made of iid uniformly distributed directions independent of ε (e.g. iid Gaussian null columns; any p with
  (log N_n)² = o(n), (rank X_{S₀} + 1) log N_n = o(n) — **p ≫ n included**),

P(δ_n/(1 − δ_n) ≥ (1 − ϵ)Λ_n) → 1 for every ϵ, Λ_n = (s₀+1)[2N_n/(2p−1−s₀)]√(log N_n/(πn)), uniformly over the class.
With all nulls and fixed s₀: **δ_n ≥ (1 − o_P(1))(s₀+1)√(log p/(πn))** and liminf E δ_n/that ≥ 1.
Reading (Remark A3, conditional on `W3-POST:Thm-1`@1.0.0 and `W3-POST:Cor-1R`@1.0.0 for the upper bound): on the
orthogonal design with p = min(n−1, ⌊n^a⌋), a ≤ 1, and on iid Gaussian designs with p = ⌊n^a⌋, **any a > 0**,
(s₀+1)√(a/π)(1 − o_P(1)) ≤ δ_n/r_n = O_P(1). So Theorem 1's rate √(log n/n) is exact whenever log p ≍ log n; the
conjecture at W3-POST STATEMENT line 104 is true; the question "does the √(log n) factor appear in E δ_n" (W3-POST2
REPORT §6 item 6) is answered yes on these designs (lower bound proved here).
The brief asked for the orthogonal witness with a ≤ 1; the spherical witness (p ≫ n) was added at no extra cost.
The mechanism: the null scores are iid χ²₁-like, W = e^{χ²₁/2} has tail 1/(w√(π log w)), and its mean truncated at N is
exactly 2√(log N/π) (re-derived; the brief's three moment formulas are confirmed, `numerics/a_orth_out.txt` E3).

**(b) Claim B — a sparsity obstruction on every design** (`lemmas/B_sparsity.md`). For every design, every data set and
every S₀ with 0 ≤ s₀ ≤ K − 1 (no law, no truth):
δ_n/(1 − δ_n) ≥ 𝒪^{lb}_n = Σ_{j≥1} C(s₀+j, j) n^{−j/2} Π_{i<j}(p−s₀−i)/(2p−1−s₀−i) ≥ c(p, s₀)/√n,
c(p, s₀) = (s₀+1)(p−s₀)/(2p−1−s₀) ≥ (s₀+1)/3 for s₀ ≤ p/2 (→ (s₀+1)/2). Consequences:
- π(S₀) ≤ [1 + (s₀+1)/(3√n)]⁻¹ surely: **π(S₀) → 1 needs s₀ = o(√n)**; at s₀ ~ λ√n, limsup π(S₀) ≤ e^{−λ/2}; if
  s₀/√n → ∞, π(S₀) → 0 on every design and data set.
- a rate δ_n = O_P(ρ_n) needs s₀ + 1 = O(√n ρ_n): the rate r_n needs s₀ = O(√log n) on every design, and — by (a) —
  **bounded s₀ on the witness designs with log p ≍ log n**.
- **Target correction (for HQ; §4).** "Growing s₀ = o(log n/log log n)" (W3-POST REPORT §4 item 8) cannot keep the
  rate r_n on the witness sequences with log p ≍ log n.

Wording of the brief corrected: "rate r_n needs bounded s₀" holds on the witness designs; on every design the
corollary gives s₀ = O(√log n) (Sol's lock review gave an example with log p = o(log n) where r_n survives s₀ → ∞).

**(c) Claim C — ridge-cost control of the reference cannot be dropped** (`lemmas/C_counterexample.md`). On the design
𝔇_n (k = ⌈12 log n⌉ orthogonal signal columns; x₁ ⟂ them; x₂ ∝ x₁ − n⁻²·(their sum); μ ∝ their sum), the reference
T = {1, 2} represents μ **exactly** and (E) holds, but ‖θ‖²/n → ∞ and every ϑ has ridge cost B_T(ϑ) ≥ b_n²(n−1)/2.
The cutoff of Lemma 1a′ (t = 2, ω = ½ log n) is ≤ ⌊k/2⌋, and P(π(|S| ≤ ⌊k/2⌋) ≤ e^{−c₁nb_n²}) → 1: the posterior
mass above the cutoff tends to 1 instead of being O_P(n^{−1/2}). So in Lemma 1a′ the coefficient bound (A:COEF-REP)
is **necessary in kind** (its Remark 2, open, is settled), and in Lemma 1a″ the bounded reference cost cannot be
weakened to small approximation error, nor to any allowance B_n with B_n/(log n)² → ∞ (n b_n² ≥ 1200(σ*²+b̄²)(log n)²
suffices; so a large enough constant multiple of (log n)² already fails). Open: allowances B_n = o((log n)²).

## 2. Review trail (verbatim reviewer replies in `reviews/`)

| layer | reviewer | verdict | file | disposition |
|---|---|---|---|---|
| Statement lock L01 | gpt-6.1-sol high (codex), blind | LOCK-WITH-AMENDMENTS (0 FATAL / 1 MAJOR / 2 MINOR / 0 NIT); derived every item | `reviews/L01_statement_lock_sol.md` | `reviews/L01_disposition.md`: all applied → v1.1 |
| Break review K01 (+ stronger-record proposals) | gpt-6-astra high (codex), blind | no claim broken (12 items derived); 0 / 2 MAJOR (evidence layer) / 1 MINOR; proposals P1, P2 | `reviews/K01_break_astra.md` | `reviews/K01_disposition.md`: all applied; P1, P2 adopted → v1.2 |
| Line check KSA (Lemma V, S; Claim A) | gpt-6.1-sol high (codex), blind | both files **VERIFIED**; 0 FATAL / 0 MAJOR / 0 MINOR / 0 NIT | `reviews/KSA_check_sol.md` | none needed (`reviews/KSA_KBC_disposition.md`) |
| Line check KBC (Claims B, C) | gpt-6.1-sol high (codex), blind | B **VERIFIED**; C **VERIFIED-WITH-AMENDMENTS**; 0 / 0 / 3 MINOR / 1 NIT (commentary and one rounded number in C; no proof step) | `reviews/KBC_check_sol.md` | `reviews/KSA_KBC_disposition.md`: all applied → v1.2.1 |
| Citation check | `citecheck.py` (cited ranges and quoted output numbers) | 42 checks, 0 MISS | `reviews/CITECHECK.txt` | — |
| Council R1 | seat sol: gpt-6.1-sol high (codex); seat opus: Claude Opus 5.5 high (claudeAgent); blind | recorded in `CHECKPOINT_2.md` | `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md` | `CHECKPOINT_2.md` |

Layers used are those of the ticket brief (statement lock; numerics; break review; proofs; line checks; council).
No separate mid-point or exhaustive sweep was run: the brief defines CP2 as proofs + Sol checks + council for this
two-page ticket. HQ to confirm that this is the intended pipeline before any PROVED-CHECKED label is used.

**Not checked:** floating-point fidelity of the code; the upper bounds quoted in Remark A3 (parents' statuses apply);
the literature statements quoted from f17 (Yang–Wainwright–Jordan, Castillo–Schmidt-Hieber–van der Vaart) — not
re-read.

## 3. Numerics (local; `numerics/`, run with `py -3.13 -I`)

- **(a) orthogonal witness** — `a_orth.py` → `a_orth_out.txt`. Odds δ_n/(1−δ_n) by a Gamma-integral /
  elementary-symmetric DP: an exact formula evaluated by quadrature (brute-force agreement 1.4·10⁻¹³ at p ≤ 13; all
  sizes ≤ K against sizes ≤ s₀ + 60: 3·10⁻¹³). Median of odds/Λ_n: 1.2–1.5 at n = 100, falling to 1.003 (s₀ = 1) and
  1.007 (s₀ = 3) at n = 25600, p = n − 1; P(odds ≥ 0.75Λ_n) ≥ 0.93 in every row. Growing s₀ = n^{0.3} inside (E), (C):
  1.26–1.37 (min 0.98).
- **(a) spherical witness, p ≫ n** — `a_sph.py` → `a_sph_out.txt`. One-step odds (closed form of Lemma S; a lower
  bound for the odds) on iid Gaussian designs up to n = 25600, p = 4.1·10⁶ and n = 6400, p = 4.1·10⁷: median of
  L1/Λ_n between 0.97 and 1.09; P(L1 ≥ 0.75Λ_n) ≥ 0.99 in every row.
- **(a) boundary** — `a_boundary.py` → `a_boundary_out.txt`. Equicorrelated nulls (ρ = 0.5): one-step odds/Λ_n has
  median 0.71, 0.72, 0.61. This is evidence about the one-step mechanism only; it does not show that the full
  conclusion fails without the witness condition.
- **(b)** — `b_check.py` → `b_check_out.txt`. Lemma S identities on 8,064 pairs (rank-deficient designs included);
  Corollary B on 55,740 (design, data, S₀) triples: min odds/𝒪^{lb}_n = 1.033; equality case 1.000000000000; table of
  the cap on π(S₀) (λ = 4: 0.1353 = e^{−2}).
- **(c)** — `c_counter.py` → `c_counter_out.txt`. Exact enumeration at scaled-down k = 16–22 with exact cutoffs
  (the theorem's k = ⌈12 log n⌉ cannot be enumerated; these runs show the mechanism, not every hypothesis):
  π(|S| > cutoff) = 1.000 for n ≥ 100 on the counterexample arm against ≤ 3.2·10⁻¹³ on the control arm (bounded
  coefficients on the same T). Cutoff bound of item 2 at the theorem's k: n²R^T_{m_n} = 3.6·10⁻⁴ at n = 200.

## 4. Sharpness record and proposed corrections to recorded items (HQ applies; this ticket edits no other folder)

| recorded item | now |
|---|---|
| W3-POST Theorem 1 item 7 / REPORT §4 item 10: "whether the extra √(log n) is attained for p = n^A is a conjecture" | **Settled (attained)** on the witness classes of Claim A, for every p = n^a, a > 0, with constant (s₀+1)√(a/π). Open: an upper bound √((1 ∨ log p)/n) when log p = o(log n). |
| W3-POST2 REPORT §6 item 6, first bullet: "does the √(log n) factor in E δ_n appear?" | **Yes** (lower bound, Corollary A1). |
| W3-POST REPORT §4 item 8: "Growing s₀ = o(log n/log log n). Risk medium" | **Correct the target**: with s₀ → ∞ and log p ≍ log n the rate r_n is impossible on the witness designs; aim at (s₀+1)√(log p/n) for s₀ = o(√(n/log p)); beyond s₀ ≍ √n, π(S₀) ↛ 1 on every design, so only mode (HPM) consistency can be aimed at (TRIAGE T2(b)). |
| W3-POST:Prop-LB (δ ≥ 1/(1 + √(n+1)), 1 ≤ s₀) | Sharpened by Corollary B: n in place of n + 1; multiplicity kept; s₀ = 0 covered. |
| Registry sharpness row `W3-POST:Lemma-1a'` / A:COEF-REP = NONE ("open") | **NECESSARY** (in kind): Proposition C. |
| Registry sharpness row `W3-POST2:B` / A:POST2-AR = ARTEFACT ("bounded cost sufficient, not necessary") | Keep "boundedness not necessary" (N6b), add **FAILED-REMOVAL**: no control at all, or an allowance ≫ (log n)², fails (Proposition C). |

Assumption readings: `ASSUMPTION_MAP.md`. New assumption ids: A:PSHARP-WORTH, A:PSHARP-WSPH (witness conditions),
A:PSHARP-COEF (‖θ*‖² ≤ nM′ on S₀; the T = S₀ case of A:COEF-REP). `implies`: Claim B implies `W3-POST:Prop-LB`.

Open items (named): (O1) upper bound of order √((1 ∨ log p)/n) for sub-polynomial p; (O2) necessity of a
weak-dependence condition on the nulls for the log factor (one-step evidence only); (O3) the exact constant
δ_n = (1 + o_P(1))Λ_n on the orthogonal witness (numerics: ratio → 1.00); (O4) in (c), cost allowances B_n = o((log n)²) and
the sharp constant at order (log n)².

## 5. Files
`STATEMENT.md` (v1.2.1), `PLAN.md`, `ASSUMPTION_MAP.md`, `REPORT.md`, `citecheck.py`; `lemmas/S_one_step.md`,
`A_log_factor.md`, `B_sparsity.md`, `C_counterexample.md`; `numerics/core.py`, `a_orth.py`, `a_sph.py`,
`a_boundary.py`, `b_check.py`, `c_counter.py` and their `*_out.txt`; `reviews/` (briefs, reviewer replies, scratch,
dispositions, manifests, CITECHECK); `LOG.md`, `CHECKPOINT_1.md`, `CHECKPOINT_2.md`.

## 6. Registry blocks

```
REGISTRY
claim: W3-PSHARP:S | kind: lemma | statement: STATEMENT.md:32-44 | premises: STATEMENT.md:16-30
name: Lemma S (one-step supersets with the fit factor kept)
status: PROVED (by this seat, unchecked) | status_source: lemmas/S_one_step.md:3
conclusion: identity: D_{S+j}/D_S <= n (equality iff x_j orthogonal to col X_S); Q_S - Q_{S+j} = n (x_j'rho_S)^2/s_{S,j}; odds against S0 >= [(s0+1)/(2p-1-s0)] n^{-1/2} sum_j exp(nu gamma_j) | scope: any n >= 3, any design, any data, |S|+1 <= K
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-PSHARP:A | kind: proposition | statement: STATEMENT.md:46-77 | premises: STATEMENT.md:16-30
name: Proposition A (the sqrt(log p) factor is attained; rate lower bound on witness designs)
status: PROVED (by this seat, unchecked) | status_source: lemmas/A_log_factor.md:3
assumptions: A:GAUSS-NOISE ; A:ENERGY ; A:PSHARP-COEF (new | coefficient bound on S0 | squared norm of theta* at most n M' | STATEMENT.md:50 | shared no) ; A:PSHARP-WORTH (new | orthogonal null block | null columns of N_n mutually orthogonal and orthogonal to col X_S0 | STATEMENT.md:54-55 | shared no) ; A:PSHARP-WSPH (new | spherical null block | null directions iid uniform on the unit sphere of 1-perp, independent of eps; (log N)^2 = o(n), (rank X_S0 + 1) log N = o(n) | STATEMENT.md:56-60 | shared no)
conclusion: negative: P(delta/(1-delta) >= (1-eps) Lambda_n) -> 1 under A:PSHARP-WORTH or A:PSHARP-WSPH; with all nulls and fixed s0, delta_n >= (1-o_P(1))(s0+1) sqrt(log p/(pi n)) and liminf E delta_n/that >= 1 | rate: (s0+1) sqrt(log p/(pi n)) (lower bound) | scope: witness designs; p <= n-1 (orthogonal) or (log p)^2 = o(n) (spherical, p >> n)
depends_on: W3-PSHARP:S@proof:S(2),S(4)
sharpness: A:ENERGY = WEAKENABLE (evidence: ASSUMPTION_MAP.md:12) ; A:PSHARP-COEF = WEAKENABLE (evidence: ASSUMPTION_MAP.md:12) ; A:GAUSS-NOISE = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:11)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better-proposal:P2(reviews/K01_break_astra.md) ; better-disposition:P2=adopted(reviews/K01_disposition.md)

REGISTRY
claim: W3-PSHARP:B | kind: corollary | statement: STATEMENT.md:90-114 | premises: STATEMENT.md:16-30
name: Corollary B (sparsity obstruction on every design)
status: PROVED (by this seat, unchecked) | status_source: lemmas/B_sparsity.md:3
conclusion: negative: for every design and data set, delta/(1-delta) >= O_lb_n >= c(p,s0)/sqrt(n), c >= (s0+1)/3 for s0 <= p/2; pi(S0) -> 1 needs s0 = o(sqrt n); limsup pi(S0) <= exp(-lambda/2) at s0 ~ lambda sqrt n; rate r_n needs s0 = O(sqrt(log n)) | rate: (s0+1)/(2 sqrt n) (lower bound) | scope: any n >= 3, any design, any data, 0 <= s0 <= K-1
depends_on: W3-PSHARP:S@proof:S(1),S(2)
implies: W3-POST:Prop-LB (j = 1 term with c(p,s0) >= 1 and n <= n+1, on LB's domain)
sharpness: A:EXT-FEAS = NECESSARY (evidence: ASSUMPTION_MAP.md:9)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better-proposal:P1(reviews/K01_break_astra.md) ; better-disposition:P1=adopted(reviews/K01_disposition.md)

REGISTRY
claim: W3-PSHARP:C | kind: counterexample | statement: STATEMENT.md:116-145 | premises: STATEMENT.md:16-30
name: Proposition C (ridge-cost control of the reference cannot be dropped)
status: PROVED (by this seat, unchecked) | status_source: lemmas/C_counterexample.md:3
conclusion: negative: on the design D_n the reference T = {1,2} represents mu exactly and (E) holds, but pi(|S| > m^T_n(log n/2)) -> 1; Lemma 1a' fails without the coefficient bound, Lemma 1a'' fails with any cost allowance B_n >> (log n)^2 | scope: one design sequence, n >= 200, n b_n^2 >= 1200 (sigma*^2 + bbar^2)(log n)^2
depends_on: W3-PSHARP:S@proof:Lemma-V,S(1)
sharpness: A:COEF-REP = NECESSARY (evidence: lemmas/C_counterexample.md:100)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)
```

Notes for the ingest (HQ): the four claims are sharpness records (kind as above; `headline` no). Links to the
claims they sharpen: A → `W3-POST:Thm-1` (rate exact), `W3-POST2:C` (E δ_n); B → `W3-POST:Prop-LB`, `W3-POST2:A2`;
C → `W3-POST:Lemma-1a'`, `W3-POST2:B`. Proposed sharpness rows for those parents are in §4. The council record
(round, manifest digest, seats, scores) is in `CHECKPOINT_2.md`; the `council:` field and the `correct:` gate are to be
filled from it at CP3 (an editorial diff under rule 15), since this file is inside the frozen manifest.
