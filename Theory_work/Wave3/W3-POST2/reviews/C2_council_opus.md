# W3-POST2 — Council diff round C2 (R2), seat B (Claude Opus 5.5, high, Claude Third)

Brief: `reviews/BRIEF_C2_B.md`. Protocol: `Theory_work/Wave3/PROTOCOL_v4.md` §5.5 with HQ amendments H1–H5.
Checkout `/home/fb31/BVS-wt/POST2-diff` (3333e0c). Manifest check, run from the checkout root:
`verify: OK MANIFEST 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a`.

What I read:
- my C1 review, `C1_disposition.md`, `C2_DIFF.md` (§1 first; both layers L1 and L2), `C2_diff.patch` and `C2_DEPENDENTS.md`;
- the frozen files, but only at the changed lines (C2_DIFF §3) and the dependent lines (C2_DEPENDENTS);
- the inherited sources those lines cite: [W3P] `STATEMENT.md:15-50` and `:75`; [T03R] `PROOF.md` §1 (E1(a), (c); the m♯_n
  definition; E2); [P3] `PROOF_v2.tex:179, 194` (C_*, (G4)).

The PC1/PC2 files are record only. I did not use their conclusions; every step below is my own check.

Scratch: `reviews/C2_scratch_opus/checks.py` → `checks_out.txt`. It covers three things:
- the c₀ < c₁ grid (#14);
- exact R_m / m♯_n enumeration against Lemma E0, including p = K = 2, s₀ = 1;
- the intercept orthogonality identity (#8).

No git operations, no subagents.

## (a) My C1 findings

| my C1 finding | resolved | file:line | note |
|---|---|---|---|
| F1 scope flag undercounts adoptions (E: (ID) → (ID^M), E1 v2) | yes | `REPORT.md:22-33`; `lemmas/E_visibility.md:3` | Items 3, 4 and 5 are listed. "No other ranked proposal was adopted" is now correct. The kill-budget ruling is left to HQ (flag 2). |
| F2 per-file check records empty | yes | `lemmas/A_occam.md:3`, `B_tail_approx.md:3`, `C_expectation.md:3`, `D_hellinger.md:3`, `E_visibility.md:3` | Records are written; status words are unchanged (verbatim). |
| F3 brief numbering in no file | yes | `STATEMENT.md:3-5`; `REPORT.md:41-42` | The map is as I proposed. |
| F4 Claim D distance is intercept-free | yes | `lemmas/D_hellinger.md:84-88`; `STATEMENT.md:118-119`; `REPORT.md:95-96` | Checked in (b)5. |
| F5 m♯_n ≥ min(j₀, K) used, not proved | yes | `lemmas/E_visibility.md:15-20` (Lemma E0), used at `:46` and `lemmas/D_hellinger.md:52-55` | Proof checked in (b)2. The first use in D3 (L1) was false for K < s₀ + j₀ − 1. L2 repairs it; checked in (b)1. |
| F6 two relation labels per registry row | yes | `REPORT.md:117-118`, `REPORT.md:212, 220` | A1 and A2 each carry one label. |
| F7 B implies Lemma 1a exactly | yes | `STATEMENT.md:79-80`; `REPORT.md:119, 228`; proof `lemmas/B_tail_approx.md:45-48` | The relation is correct, but by a different route than my C1 note gave; see (b)7. |
| F8 c₀ < c₁ only at s₀ = A = 1 | yes | `STATEMENT.md:136`; `REPORT.md:122` | Reproduced: min c₁/c₀ = 1.2278 at (s₀, A) = (1, 10) on s₀ = 1…20, A ∈ [1, 10] (step 0.01). See (b)8. |
| F9 housekeeping | yes | `REPORT.md:180` → `reviews/CITECHECK.txt:1` (136 / 0); `lemmas/A_occam.md:4`; `numerics/post2_checks.py:263`, `post2_checks_out.txt:58, 66`; `ASSUMPTION_MAP.md:44`; `lemmas/D_hellinger.md:91-92` | All four items are done. A_occam:4 points to v1.2; v1.2.1 changed no mathematics, so the pointer is accurate. |
| F10 two REPORT overstatements | yes | `REPORT.md:55-56`, `REPORT.md:161-162`; also `ASSUMPTION_MAP.md:59-60`, `lemmas/D_hellinger.md:96-98` | Both are reworded as proposed and propagated (L2). |
| F11 registry block, per-clause statuses | yes | `REPORT.md:202-254` | There are blocks for A1, A2, B, C, D and E. D(a) and D(b) share one block, with split premises (`:240`) and one status. That status is the same for both clauses, and the registry carries separate rows D.D(a) and D.D(b). |
| F12 B Remark 4 cites the wrong part of `lem:prior`(c) | yes | `lemmas/B_tail_approx.md:54` | It now cites the proof line Σ_{k>m} q_k ≤ 2^{−m}. |

## (b) Does the diff break anything?

### 1. D3 cutoff chain, `lemmas/D_hellinger.md:52-55` — correct

- **The chain.** An underfit S ∈ 𝔉 has S₀ ⊄ S, so |S ∩ S₀| ≤ s₀ − 1, and |S∖S₀| ≤ j₀. Hence |S| ≤ s₀ + j₀ − 1. Also
  S ∈ Ω gives |S| ≤ K. So |S| ≤ min(s₀ + j₀ − 1, K) ≤ min(s₀ + j₀, K), and Lemma E0 with B = s₀ + j₀ (≥ s₀ + 1) gives
  min(s₀ + j₀, K) ≤ m♯_n for n ≥ n₀(s₀, A). Every link holds.
- **What L2 repaired.** The L1 text asserted s₀ + j₀ − 1 ≤ min(s₀ + j₀, K). That is false when K < s₀ + j₀ − 1. The
  repair takes the min with K first, using S ∈ Ω.
- **Small fixed p, and K < s₀ + j₀ − 1.**
  - Then min(s₀ + j₀, K) = K. E0 gives m♯_n ≥ K, and m♯_n ≤ K always ([W3P] `STATEMENT.md:38`), so m♯_n = K and
    |S| ≤ K = m♯_n.
  - Exact enumeration at p = K = 2, s₀ = 1, n = 50 and 1000 gives (m♯_n, K) = (2, 2), as the chain predicts.
- **Is the chain needed? Yes, for one thing.** The decomposition Ω∖𝒮_n ⊆ {|S| > m♯_n} ∪ {S ⊋ S₀, |S| ≤ m♯_n} ∪ 𝒰_far
  is complete without the cutoff. The cutoff is needed so that near underfits have |S| ≤ m♯_n ≤ m♯_n + s₀. That puts
  them inside the size range of (G2*) (`STATEMENT.md:18-19`: 1 ≤ |T| ≤ m♯_n + s₀). The repaired chain delivers this.

### 2. Lemma E0, `lemmas/E_visibility.md:15-20` — correct (statement, proof, both uses)

- **The threshold.** By [W3P] `STATEMENT.md:36-38` and [T03R] §1, m♯_n = min{m ≥ s₀ : R_m ≤ n^{−(s₀+1)/2}e^{−ω}} with
  ω = ½ log n. The threshold is therefore n^{−(s₀+2)/2}, as E0 uses.
- **The lower bound on R_m.** Take s₀ ≤ m < min(B, K). Then m + 1 ≤ K, and every term of R_m is positive, so
  R_m ≥ q_{m+1}/w(s₀). This step does not need [T03R] E1(c)'s hypothesis s₀ ≥ 1. By [T03R] E1(a) with k = m + 1,
  q_{m+1}/w(s₀) = C(p, s₀)Π_{i=s₀}^{m} ρ_i.
- **The bound on each ρ_i.** For i ≤ m < K ≤ p we have p − i ≥ 1 and 2p − 1 − i < 2p.
  - If p ≥ 2B: ρ_i ≥ (p − B)/(2p) ≥ 1/4.
  - Otherwise: ρ_i ≥ 1/(2p) > 1/(4B).
- **The conclusion.** There are m − s₀ + 1 ≤ B − s₀ factors, each in [1/(4B), 1], and C(p, s₀) ≥ 1. So
  R_m ≥ (4B)^{−B} > n^{−(s₀+2)/2} for n ≥ n₀(s₀, B). Such m is therefore not admissible, and m♯_n ≥ min(B, K). The bound
  is uniform in p. If min(B, K) ≤ s₀, the claim is trivial, since m♯_n ≥ s₀.
- **Implicit hypotheses.**
  - s₀ ≤ K is needed for m♯_n to be defined. It holds in R1 for n ≥ 2s₀, because S₀ ⊆ [p].
  - n₀ depends on (s₀, A) through B = j₀(s₀, A) or s₀ + j₀. Its stated dependence on A is harmless.
- **Exact enumeration.** A ∈ {1, 2}, s₀ ≤ 3, B ∈ {s₀ + 1, j₀, s₀ + j₀}, n ≤ 5000, p ≤ 400, restricted to cases where
  (4B)^{−B} > n^{−(s₀+2)/2}: 0 violations.
- **Use 1: B = j₀ at `:46` (E1(b)).**
  - j₀ = ⌈(2A + 1)s₀⌉ + 1 ≥ s₀ + 1, so E0 applies.
  - |J′| ≤ j₀ (S ∈ 𝔉) and |J′| ≤ |S| ≤ K, so |J′| ≤ min(j₀, K) ≤ m♯_n.
  - s₀ + |J′| = |S′| ≤ p. Both conditions of (G3′) (`lemmas/A_occam.md:46`) therefore hold, and τ_{|J′|} ≤ C_A j₀ log n.
    Correct.
- **Use 2: B = s₀ + j₀ in D3.** See item 1.

### 3. The rest of D3, `lemmas/D_hellinger.md:55-81` — correct

- **Mass outside 𝒮_n (`:55-59`).** This part is unchanged. Its use of E1(b) at c₂ = c₁ + 1 for 𝒰_far ∩ 𝔉 now rests on a
  proved E0 with B = j₀.
- **Conditional bounds (`:60-71`).**
  - Each S ∈ 𝒮_n has |S| ≤ s₀ + j₀: S₀ trivially, and near underfits by the chain in item 1. Each such S also has
    |S| ≤ m♯_n + s₀, so (G2*) gives ‖P_Se‖² ≤ σ*²C_A(s₀ + j₀) log n.
  - 𝒢⁵_n covers 𝔉 ⊇ 𝒰_near, giving 2|cross| ≤ 2σ*²√(2C_x c₂) log n.
  - So m_n^{fit} and C_Q are as written.
- **The Markov step (`:73-75`).** It uses |S| ≤ s₀ + j₀ through tr(M_S) ≤ |S|, and E v ≤ (5/4)σ*² ≤ 2σ*².
  - C_H log n/2 = 2m_n^{fit} + (log n)/2 ≥ 2m_n^{fit}, so the split is valid.
  - The bound 8σ*²(s₀ + j₀)/(C_H log n) → 0 follows.
- **Constants.**
  - C_H = 8σ*²(C_A(s₀ + j₀) + c₂) + 1, with C_A = 8 + 3A, j₀ = j₀(s₀, A), c₂ = c₁(s₀, A) + 1. So C_H depends only on
    (s₀, A, σ*²).
  - C′_H = 1 + C_H/(4σ*²). Off Bad_b with M_n = √(log n): h̄_n² ≤ log n/n + C_H log n/(4nσ*²) = C′_H log n/n.
  - The repair changes none of these.

### 4. D(b) statement against D3, and its other appearances — consistent

- **The statement and D3 agree** (`STATEMENT.md:112-116` against `lemmas/D_hellinger.md:50, 72-79`):
  - Hypotheses are the same: R1, G, (E), (F₀), (OS). E1 is used as a lemma, so (ID^M) is not a hypothesis.
  - The constant is the same, C_H(s₀, A, σ*²), and C′_H is identical.
  - The quantifier is the same: "for every M_n → ∞".
  - The mode is the same: in probability.
  - D3's n₀ depends further on (M, φ₀, b₀, C_OS). That is allowed by an in-probability statement; only C_H is claimed
    to have the restricted dependence.
- **The summaries are consistent with this:**
  - `REPORT.md:99-100` and `:240-242`;
  - `ASSUMPTION_MAP.md:13` ((OS) enters D(b)), `:16` (E1 at c₁ + 1, no hypothesis), `:38` and `:46`.

### 5. Intercept remark, `lemmas/D_hellinger.md:84-88` and `STATEMENT.md:117-119` — correct, with the same constants

- **The orthogonality identity.** ȳ^r = α* + mean(X^rβ*) + ε̄ and μ_i = (X^rβ*)_i − mean(X^rβ*). So the mean error is
  ε̄1 + (μ̂ − μ). Because μ̂, μ ∈ 1^⊥, Σ_i(ε̄ + μ̂_i − μ_i)² = nε̄² + ‖μ̂ − μ‖². This is checked numerically, with error
  ≤ 1.2·10⁻¹³.
- **The bound.** Lemma D0's argument gives h̄²_int ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²) + ε̄²/(4σ*²). Here
  nε̄²/σ*² ~ χ²₁, and ε̄ is a function of the data, not of the posterior draw.
- **D(a).** Split the bound into thirds. The ε̄ event is a data event with probability → 0, since M_n → ∞. M_n is
  arbitrary, so D(a) holds verbatim.
- **D(b) with the same C′_H.**
  - D3's last line chooses M_n = √(log n) exactly. Off Bad_b that choice gives only
    h̄²_int ≤ C′_H log n/n + ε̄²/(4σ*²), which is not by itself ≤ C′_H log n/n.
  - But D(b)'s first display holds for every M_n → ∞. Take M_n = ½√(log n). Then
    Π(h̄²_int > C′_H log n/n | y) ≤ Π(Bad_b(M_n) | y) + 1{nε̄²/σ*² > 3 log n}, and both terms → 0 in probability.
  - So "D(b) holds verbatim (same C′_H)" follows from the D(b) statement itself; Remark 0's "the extra term is O_P(1/n)"
    is this absorption.
  - I count this as a complete argument, not a gap, because the slack is explicit in the statement's "for every M_n → ∞".

### 6. Registry premise use of `STATEMENT.md:117-119` (rows D.D(a), D.D(b)) — consistent

The added sentence on lines 118-119 states a fact proved in D4 Remark 0 (item 5). It adds no hypothesis.

### 7. #13 Claim B relation, `STATEMENT.md:79-80` — correct

- **Setup.** Take T = S₀ and ϑ = θ*. Under G, μ = X_{S₀}θ* exactly, so B_T(θ*) = (‖μ‖² + ‖θ*‖²)/n. (F₀) gives
  ‖θ*‖² ≤ nM/(Nφ₀²), so B ≤ M + M/(2φ₀²) for n ≥ 3.
- **Θ♯ ≤ Θ″.** R^{S₀}_m = R_m and √D_{S₀} ≤ (n + 1)^{s₀/2} ([P1] `lem:spec`(e)).
- **The constant: correcting my own C1 note.** C″_Λ(B) itself does **not** in general satisfy C″_Λ(B) ≤ C_Λ.
  - Write k = 1 + 1/(2φ₀²). The term √(2B/π)/σ* exceeds C_Λ's extra k/2 once M > πkσ*²/8.
  - The relation holds instead through the exact-reference improvement of B Remark 1 (`lemmas/B_tail_approx.md:45-48`):
    r = 0, so there is no εᵀr term and E Λ″ ≤ 1/√2 + 1/2 + B/(2σ*²) ≤ 1/√2 + 1/2 + kM/(2σ*²) ≤ C_Λ.
  - `REPORT.md:119` names this route ("exact reference: r = 0 recovers C′_Λ"). The first term
    (8 + 24M/σ*²)/(n − 1) and c♯ are the same in both. So B implies [W3P] Lemma 1a with its own constant.
- **Hypotheses.** Lemma 1a's hypotheses (p ≥ 2, s₀ ≤ K so S₀ ∈ Ω, (E), (F₀)) are covered.

### 8. #14 c₀ < c₁ grid, `STATEMENT.md:136` — correct

- **Formulas.** c₀ = max{4C_*, 32[s₀(A + 1) + 2]} ([W3P] `STATEMENT.md:75`), with
  C_* = 2s₀ + 3(Aj₀ + s₀ + log(j₀ + 1) + 1) ([P3] `PROOF_v2.tex:194`).
- **Reproduction.** On s₀ = 1…20, A ∈ [1, 10] (step 0.01), min c₁/c₀ = 1.2278 at (1, 10). This matches "1.23". At
  s₀ = A = 1: c₀ = 128, c₁ = 160.77.
- **s₀ = 0.** There c₁/c₀ = 0.91, but there are no underfits, so BM(c) and (ID^M; c) are vacuous and the coexist range
  has no content. The statement's grid evidently means s₀ ≥ 1.
- **What it supports.** The claim is labelled a numerical grid observation and is used only in the relation field. It
  supports non-emptiness of the coexist range there.

### 9. Dependents of E1(b) → E0 — correct, none broken

- **E2 assembly (`lemmas/E_visibility.md:56-70`).** It is unchanged and consumes E1(b) as stated. E1(b)'s n₀ now
  includes E0's n₀(s₀, A); the dependence is unchanged in kind.
- **Claim C case (iii) (`lemmas/C_expectation.md:52-54`).** κ̄_n = n^{−2} from E1(b) and P((𝒢⁵_n)ᶜ) ≤ 1/n from E1(a).
  E0 is deterministic and uniform in 2 ≤ p ≤ n^A, with n₀ depending only on (s₀, A). So Claim C's uniformity (n₀, C
  depending only on the listed constants, hypotheses "at that n") is preserved.
- **E3.1 (`lemmas/E_visibility.md:76-78`).** Its last clause uses Claim E, whose proof is now complete at E1(b). Its own
  implication (F_λ) ∧ BM(c) ⇒ (ID; c(1 − 1/n)) does not touch E0.

### 10. W/R-class changes — match the proofs

- **N2 qualification** (`lemmas/A_occam.md:33-34`, `ASSUMPTION_MAP.md:14, 27`, `REPORT.md:149-150, 193`). It weakens a
  remark; A0 and A1 do not use it.
- **N4** (`ASSUMPTION_MAP.md:28`, `REPORT.md:157-158`). Wording only.
- **D(a) scale** (`lemmas/D_hellinger.md:96-98`, `ASSUMPTION_MAP.md:59-60`). It now claims less (no lower bound), which
  matches the proof.
- **Rank-loss wording** (`REPORT.md:55-56`). Matches (OS).

Nothing in the diff breaks a proof, a statement or a constant.

## Findings

No C, S or F findings. Per the brief, no new E findings. I record one correction to my own C1 rationale, already
dispositioned in (b)7: the Lemma 1a relation holds via the exact-reference constant of B Remark 1, not via
C″_Λ(B) ≤ C_Λ. It requires no change to the frozen text.

## Gates (on the diff and its dependents, this manifest)

- **G1 correctness of every changed step — PASS.** The D3 cutoff chain, Lemma E0, E1(b)'s use of E0, intercept Remark 0,
  the B relation and the c₀ < c₁ grid were each re-derived or reproduced ((b)1–8).
- **G2 hypotheses used = stated — PASS.** D(b) uses R1, G, (E), (F₀), (OS), as stated. E0 needs only s₀ ≤ K, which is
  implied by R1. The intercept remark adds no hypothesis.
- **G3 no hidden assumptions — PASS.** The C1 hidden step (m♯_n ≥ min(j₀, K)) is now Lemma E0 with a proof. Its first
  D3 use, false for K < s₀ + j₀ − 1, is repaired.
- **G4 cited statuses — PASS.**
  - [T03R] E1(a) (PROVED) and [W3P] §0 definitions are cited correctly.
  - [P3] C_* is cited correctly.
  - New status words are verbatim, and the check records are filled.
- **G5 constants and rates tracked — PASS.**
  - C_H and C′_H are unchanged and depend on (s₀, A, σ*²), as stated.
  - The intercept term ε̄²/(4σ*²) is O_P(1/n), absorbed with the same constants.
  - The c₀ < c₁ grid is reproduced (min 1.2278).
- **G6 coded target — PASS.** The intercept-inclusive predictive law N(ȳ^r + μ̂_i, v) is the coded plug-in law. The
  centred distance is now named as such (`STATEMENT.md:118`).

Score: no C/S/F finding stands; the C1 loose ends (F4, F5) are closed and the one defect introduced in L1 is correctly
repaired in L2. **9.1 / 10.**

## (c) Per-claim table

| id | decision |
|---|---|
| W3-POST2:A0 | ACCEPT |
| W3-POST2:A1 | ACCEPT |
| W3-POST2:A2 | ACCEPT |
| W3-POST2:B | ACCEPT |
| W3-POST2:C | ACCEPT |
| W3-POST2:D | ACCEPT |
| W3-POST2:D.D(a) | ACCEPT |
| W3-POST2:D.D(b) | ACCEPT |
| W3-POST2:E | ACCEPT |
| W3-POST2:E3.1 | ACCEPT |

`COUNCIL-VERDICT round=R2 manifest=96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a seat=B score=9.1 gates=PASS`
