# W3-POST — REPORT (to Theory HQ)

Ticket W3-POST (PROGRAM item 1 and 1a). Lead: Claude Opus 5.5 (claudeAgent, high). Folder:
`Theory_work/Wave3/W3-POST/`. No git state changes.

**RESULT.** **COUNCIL-PASSED in round C3** (seat A gpt-6-astra high 8.8, seat B Claude Opus 5.5 high 8.7; all six gates
PASS for both seats in the same round). Status category: the Theorem 1 chain is re-checked (no defect found by any of
two re-check reviewers and six council seats); new results Lemma 1a′ and Proposition LB are "PROVED (by this seat,
unchecked)" with check records. **PROVED-CHECKED** in the protocol's sense also needs mid-point and sweep layers, which this
ticket replaced by the R01/R02 whole-chain re-checks — **HQ to confirm** the substitution before the label is used [C3B-N7,
F2]. Input statuses unchanged. Council history: C1 not passed (A 7.5, gates G1/G2/G3/G5 FAIL — literature/sharpness
layer; B 8.4 PASS); C2 not passed (A 8.3, G1/G2/G3 FAIL — REPORT omitted Proposition LB's domain; B 8.8 PASS). No seat in
any round found a defect in the proof chain, Lemma 1a′ or Proposition LB. Dispositions: `reviews/C1_disposition.md`,
`C2_disposition.md`, `C3_disposition.md`.

Theorem 1 is posterior concentration for the coded target. Two fresh reviewers re-checked it adversarially: R01
(gpt-6-astra high; cross-family) and R02 (Claude Opus 5.5 high; same family as the lead) [C2B-F1]. Both found 0 FATAL / 0 MAJOR issues in the chain
[P1] → [P3] → [T03R] → [POST] → [SL]. Their 8 MINOR + 7 NIT findings concern wording and scope; all were applied or
recorded.

New in this ticket:
- **Lemma 1a′**: a design-free size tail, with no eigenvalue condition.
- **Proposition LB**: a deterministic lower bound 1 − π(S₀) ≥ 1/(1 + √(n+1)) whenever 1 ≤ s₀ < p and s₀ + 1 ≤ K (a feasible one-variable extension of S₀ exists) [C2A-F1], so on
  every design sequence with such extensions (e.g. p > s₀ and n ≥ 2(s₀ + 1)) the rate is sharp up to √log n.
- A numerical **counterexample** to specificity without beta-min.
- The sharpness record.

Input statuses are unchanged. The new lemmas are "PROVED (by this seat, unchecked)" with check records in their files.

## 1. Statement as checked (`STATEMENT.md` v1.4)

**Target π.** The exact real-arithmetic posterior of the code:
- capped BB(1,p) prior at K = min(p, ⌊n/2⌋) over the p retained (non-constant) columns;
- g = n ridge score with H = (n+1)G + I and A = G + I;
- IG(0.01, 0.01) with ν = 0.01 + n/2, under a working Gaussian likelihood on the standardised scale.

R01, R02 and both C1 seats matched it to `v3_score.h`/`v3_preprocess.R`.

**Cutoff.** m♯_n(ω) = min{m ≥ s₀ : Σ_{k=m+1}^{K} C(p,k)w(k)/w(s₀) ≤ n^{−(s₀+1)/2}e^{−ω}}, and m♯_n := m♯_n(½ log n)
[C1B-N2]. For fixed s₀ ≥ 1 and p ≤ n^A it is O(log n). For a general reference set T the same definition is used with
t = |T|, and it is O(log n) for fixed t [C1A-F4].

**Lemma 1a (T02(i♯)).** Assume p ≥ 2, G, ‖μ‖² ≤ nM, λ_min(R_{S₀}) ≥ φ₀² and s₀ ≤ K. Then
π(|S| > m♯_n(ω)) = O_P(e^{−ω}), with a non-asymptotic bound uniform in m.

**Lemma 1a′ (new).** Replace the eigenvalue condition by an exact representation μ = X_Tθ (T ∈ Ω) with
‖μ‖² ≤ nM and ‖θ‖² ≤ nM′. The same conclusion then holds with t = |T| in the cutoff. With T = S₀ and |θ*_j| ≤ θ_hi:
- models above the cutoff carry mass O_P(n^{−1/2}) for every X with ‖Xθ*‖² ≤ nM;
- that energy condition is automatic for fixed s₀ (M = s₀²θ_hi²) but a real condition for growing s₀ [C1A-F4, C1B-N3];
- the bound is uniform over such X.

**Theorem 1.** Setting R1: s₀ ≥ 1 fixed, 2 ≤ p ≤ n^A, G. Hypotheses on (X, θ*):
- (E) ‖μ‖² ≤ nM;
- (F_λ) λ_min(R_{S₀∪J}) ≥ φ₀² for |J| ≤ j₀ = ⌈(2A+1)s₀⌉+1;
- (F_w) λ_min(G_{S₀∪J}) ≥ g₀ for |J| ≤ m♯_n.

By interlacing, (F_λ) and (F_w) give the same floors on every set of size ≤ j₀, resp. ≤ m♯_n. Under BM(c > c₀) or
BM-∞:
1. δ_n = 1 − π(S₀) = O_P(√(log n/n)).
2. Exact HPM = S₀ and MPM = S₀ with probability → 1; ξ_{q_n} = S₀ with probability → 1 for deterministic q_n with
   r_n = o(min(q_n, 1 − q_n)) [C1B-N3].
3. max_j |PIP_j − 1{j ∈ S₀}| ≤ δ_n.
4. π(|S| = s₀) → 1 at rate r_n, and bounded functionals are within O_P(r_n) of their value at S₀.
5. Without beta-min:
   - (a) no strict-superset mass: π(S ⊋ S₀) = O_P(r_n);
   - (b) strong-signal recovery;
   - (c) the size tail (Lemma 1a / 1a′).

   Specificity without beta-min: **COUNTEREXAMPLE (numerical E5; leading-order sketch, unchecked)**.
6. Interface form for random (X, θ*), with ε independent of (X, θ*): if on (X, θ*)-measurable events of probability
   → 1, |supp θ*| = s₀ and (E), (F_λ), (F_w), (BM) hold with common constants [C3B-F1], then 1–4 hold under the joint law, and 5(a)–(b) hold without (BM) [C1A-F7].
7. Rate lower bound (Proposition LB): 1 − π(S₀) ≥ 1/(1 + √(n+1)) deterministically, for every data set and design,
   whenever 1 ≤ s₀ < p and s₀ + 1 ≤ K (a feasible one-variable extension of S₀ exists) [C2A-F1]. (Without such an extension it can fail: at p = s₀ = 2 with orthogonal
   columns δ ≈ 6.5·10⁻¹⁰ at n = 20, `numerics/lb_domain.py` → `lb_domain_out.txt` [C2B-N7].)

**Corollary 1R (bridge example: Gaussian rows).** iid raw rows N(m, Σ_n), ε independent of the design [C3B-F1].
Population floor LSF: a fixed floor at size s₀ + j₀, and
ψ_n ≫ (log n)^{3/2}/√n at size O(log n). With coefficient bounds 0 < θ_lo ≤ |θ*_j| ≤ θ_hi (or raw b_lo, b_hi plus the
raw-design event), the events of item 6 exist, so 1–4 hold. With the upper bound only, 5(a)–(b) hold [C1A-F4].

## 2. Review trail (verbatim reviewer replies in `reviews/`)

| Step | Reviewer | Verdict | File | Disposition |
|---|---|---|---|---|
| Adversarial re-check (whole chain, statement, code fidelity) | R01 gpt-6-astra high (codex) | chain VERIFIED; L1a′ and STATEMENT VERIFIED-WITH-AMENDMENTS; 0 FATAL/0 MAJOR/4 MINOR | `R01_recheck_astra.md` | `R01_disposition.md`: all 4 applied |
| Same, independent | R02 Opus 5.5 high (claudeAgent) | chain VERIFIED; L1_POST and STATEMENT VERIFIED-WITH-AMENDMENTS; L1a′ VERIFIED; 0/0/4 MINOR/7 NIT | `R02_recheck_opus.md`, `R02_scratch/` | `R02_disposition.md`: 9 applied, 2 recorded |
| "Better theorem" | R03 gpt-6-astra high | ranked proposals; specificity mechanism | `R03_better_theorem_astra.md` | §4; ASSUMPTION_MAP |
| Council C1 | seat A gpt-6-astra high / seat B Opus 5.5 high | A: 7.5, G1/G2/G3/G5 FAIL (0 FATAL/2 MAJOR/6 MINOR/1 NIT, all in the sharpness/literature/report layer); B: 8.4, all gates PASS (0/0/4 MINOR/7 NIT) | `C1_council_astra.md`, `C1_council_opus.md` | `C1_disposition.md`: all applied |
| Citation check | `citecheck.py` (selected range, token and status checks; see its docstring) | 0 failures | `CITECHECK.txt` | — |
| Council C2 | seat A gpt-6-astra high / seat B Opus 5.5 high | A: 8.3, G1/G2/G3 FAIL (0 FATAL/1 MAJOR: LB domain omitted in REPORT/1 MINOR/3 NIT); B: 8.8, all gates PASS (0/0/1 MINOR/7 NIT) | `C2_council_astra.md`, `C2_council_opus.md` | `C2_disposition.md`: all applied |
| Council C3 (final) | seat A gpt-6-astra high / seat B Opus 5.5 high | **A: 8.8, all gates PASS (0/0/0/2 NIT); B: 8.7, all gates PASS (0/0/2 MINOR/8 NIT) — PASSED** | `C3_council_astra.md`, `C3_council_opus.md` | `C3_disposition.md`: all applied post-council (wording only) |

Protocol layers [C3B-F2]: for this re-check of already-verified results, the statement lock, lemma-by-lemma checks,
mid-point and exhaustive sweep were **replaced** by the two independent whole-chain adversarial re-checks R01/R02
(PLAN step 2); no separate mid-point was run (HQ to confirm the substitution). New lemmas (L1a′, LB) had falsification
numerics and line checks by R01/R02 (L1a′) and both C2 seats (LB).

Coverage: the attack points of CRITIQUE_fable §2.1 and ADJ_opus risk 1 were all re-derived by R01 §3, R02 §3 and C1
seat B §1:
- the size tail above the sieve;
- response standardisation and the mixed-endpoint transfer;
- the IG(0.01, 0.01) term and the n vs n−1 dimension;
- rank-deficient and near-collinear ridge;
- **the middle range j₀ < |J| ≤ m♯_n: sound** (it needs only (F_w), with constants uniform in m♯_n = O(log n));
- large underfits;
- the random-design transfer, including the no-beta-min extension;
- SL0/SL1.

**Not checked:**
- Song–Liang's Theorem S (the supplement is unavailable).
- NH14 Theorem 4.2 and YWJ16 Theorem 2 (not re-read).
- UNI-P beyond §3(i).
- Proposition D and E3 (not used by Theorem 1).
- Floating-point fidelity.

## 3. Sharpness record (`ASSUMPTION_MAP.md` v1.2)

Numerics: `numerics/post_exact.py` → `post_exact_out.txt`. These are exact coded-posterior enumerations at p = 10
(protocol cap), 20 seeds, n ≤ 6400 (E5 up to 25600), with medians over seeds. They are empirical trends at fixed p
(the regime A → 0), not proved limits.

**Assumption ids:**
- POST-G, POST-E;
- POST-C (coefficient bound, L1a′);
- POST-F0, POST-Fλ, POST-Fw;
- POST-BM, POST-BM′;
- POST-DIM, POST-S;
- POST-LSF, POST-GR.

**Implications** (needed bounds kept, C1A-F4):
- Fλ ⇒ F0;
- F0 ∧ E ⇒ C;
- locked SE ⇒ Fλ ∧ Fw;
- LSF ∧ GR ∧ coefficient upper bound ⇒ E ∧ Fλ ∧ Fw on high-probability events, plus BM when θ_lo > 0;
- λ_min(Σ_n) ≥ c ⇒ LSF;
- items 2–4 ⇐ item 1.

**Findings:**
- **Rate — sharp up to √log n (proved; status PROVED (by this seat, unchecked), line-checked by both C2 seats) [C3B-N4].** Proposition LB gives 1 − π(S₀) ≥ (1 + √(n+1))⁻¹ for every design and data set whenever 1 ≤ s₀ < p and s₀ + 1 ≤ K (a feasible one-variable extension of S₀ exists) [C2A-F1], from
  the prior multiplicity and the per-variable Occam factor. The falsification check (34 920 cases) gives a minimum
  ratio of 1.013. At fixed p, median δ√n ≈ 2.1–2.6 (E0). Whether the √(log n) factor is attained for p = n^A is a
  **conjecture**. YWJ16's faster O(p⁻¹) uses a different prior, with per-variable penalty ≥ 2 log p [C1A-F1].
- **Beta-min — order necessary by numerics and a leading-order heuristic (not proved); constant improvable.**
  - E1 at fixed p: c = 0.5 and c = 1 fail (median δ 0.93–0.99); θ² = log log n/n fails; c = 2 is slow (δ 0.66 → 0.13);
    c = 4 reaches the rate (δ/r_n 1.54 → 0.70).
  - Deletion obstruction (R03 §1A, fixed margin η > 0, orthogonal true coordinate, log p = (a + o(1)) log n):
    c ≤ 2a + 1 − η breaks consistency and c ≤ 2a + 2 − η breaks the rate [C1A-F8].
  - c₀ = 128 at s₀ = A = 1 is 32–64× the rate obstruction.
- **Floor set size — improvable in strength (numerics; not proved).**
  - E2: (F_w) violated by an exact dependence among 5 null columns; still consistent (median δ/r_n 0.94 → 0.67; HPM
    correct in 100% of seeds).
  - E3: null-only duplicates violate (F_λ) but are harmless.
  - E4: a truth's near-duplicate (1 − corr² = n^{−γ}): consistent at γ = 0.5; slow at 0.8 (HPM wrong 10–20%); no
    convergence at γ = 1 (HPM wrong 25–30%). What appears to matter is θ²_min·n·φ₀²/log n (numerical trend, not proved) [C3B-N3].
  - NH14 split their design control into identifiability (Condition 4.4) and a minimum-*nonzero*-eigenvalue
    regularity condition (4.5) that allows exact singularity [C1A-F2]. R03's DG/VIS interfaces move ours that way.
  - L1a′ needs no floor at all.
- **Specificity without beta-min — COUNTEREXAMPLE (numerical, E5; leading-order sketch, unchecked).**
  - E5: four weak truths with θ² = 0.8 log n/n, and a null proxy with a fixed population floor ≈ 0.106. The median
    max-null PIP is 0.26, 0.49, 0.82, 0.92, 0.988 at n = 100 … 25600.
  - Leading order: the proxy beats every other model by ≥ 0.48 log n.
  - R03 §5A's p = 3 version is the same mechanism, but its margin is invisible at n ≤ 10⁶ (C1 seat B).
- **p ≤ n^A — open (technique).** Lemma 1a′ and LB are free of it.

**Literature**, read from the sources, condition numbers as printed:
- **Song–Liang (2015):** PDF, printed pp. 949–957. Theorems 1 and 2 have different settings [C1A-F3]. The Theorem S
  supplement is unavailable and was not read.
- **Narisetty–He (2014):** arXiv:1405.6545, pp. 5–6 and 10–12 (Conditions 4.1–4.5, Theorem 4.1).
- **Yang–Wainwright–Jordan (2016):** arXiv:1505.07925, pp. 6–9 (Assumptions A–D; Theorem 1 uses D(s*), with no cap).

**Comparison:**
- Ours puts a fixed floor on all sets of bounded size and a free floor at O(log n). NH14 has a residual-signal
  condition plus nonzero-eigenvalue regularity. Song–Liang have a vanishing floor on all (r̄_n + 1)-sets.
- Our cap violates Song–Liang's condition (10) when p ≥ n/2; Lemma 1a′ replaces it.
- Our exact-selection conclusions are stronger than Song–Liang's main-text sure-screening conclusion [C3A-N2]
  (NH14 and YWJ16 also prove posterior model concentration).
- Our dimension range is narrower: n^A vs log p = o(n) (NH14) or exp(Cn^α) (Song–Liang).

## 4. What could be strengthened (ranked; from R03 and the numerics — none done here)

1. **DG interface instead of (F_w):** D_{S₀∪J}/D_{S₀} ≥ [c_D(n+1)]^{|J|}; rank loss is absorbed by truncation.
   Risk low (R03 §2A).
2. **VIS interface instead of (F_λ) off S₀:** ‖(I − P_S)μ‖² ≥ Nφ²‖θ*_{S₀∖S}‖² for small underfits. This is NH14-like
   identifiability. Risk medium (R03 §2B).
3. **Lemma 1a′ with an approximate reference,** keeping √D_T. Risk low (R03 §6A).
4. **Expectation rate:** E[1 − π(S₀)] = O(n^{−q/2}) for q < 1. Risk low (R03 §6B). LB shows q ≤ 1 is necessary on sequences with a feasible one-variable extension of S₀ [C2A-F1].
5. **Smaller beta-min constant:** c_new = (√C_* + √(2(A+1)))². Risk low–medium (R03 §1B).
6. **Random-design bridges:** sub-Gaussian rows (risk low); for Gaussian rows, nψ_n ≥ C (risk low–medium) (R03 §4A).
7. **Dimension:** L_n = log 2p + log n = o(n^{1/3}), paying beta-min ≳ j_nL_n. Risk medium (R03 §3).
8. **Growing s₀** = o(log n/log log n). Risk medium (R03 §4B).
9. **Specificity without beta-min under block orthogonality.** Risk medium (R03 §5B).
10. **Lower bound for the √(log n) factor at p = n^A** (would close the rate question).
11. **1b Hellinger/predictive** contraction (R03 §6C) is PROGRAM item 1b.

Recommendation: items 1, 3 and 4 are cheap and make Theorem 1 more design-agnostic. Item 2 answers "is the floor set
size improvable" and matches NH14's split.

## 5. Files
- `STATEMENT.md` (v1.4), `lemmas/L1a_size_tail.md`, `lemmas/LB_rate_lower_bound.md`, `ASSUMPTION_MAP.md` (v1.2).
- `numerics/post_exact.py` → `post_exact_out.txt`; `numerics/lb_check.py` → `lb_check_out.txt`; `numerics/lb_domain.py` → `lb_domain_out.txt`.
- `citecheck.py`, `reviews/CITECHECK*`.
- `reviews/R01*`, `R02*`, `R03*`, `C1_*`, `C2_*`, `C3_*` (reviews, dispositions, reviewer scratch) [C3B-N2].
- `PLAN.md`, `LOG.md`.
