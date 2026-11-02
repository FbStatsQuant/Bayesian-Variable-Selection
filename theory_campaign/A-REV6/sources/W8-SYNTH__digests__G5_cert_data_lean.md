# G5 digest: certificates, finite-n miss theory, start masking/fixes, masked-regime Ẑ/PIP, E_LS ledger, paper skeleton, Lean

Scope: O-CERT, O-VCERT, O-SWAP, O-DILUTE, O-MIX, F-SIGMA, F-MASKPIP, S-ELS, S-PAPER, L-LEAN, plus O-LS0 (no report).
Sources: scratchpad `src/<ID>/` snapshots (= `theory_campaign/<ID>/` on `origin/theory/<ID>`), LEDGER.md, THEORY_PRIORITIES.md §5,
HQ/SR_AUDIT.md. Statuses are copied verbatim; nothing upgraded. Every branch says "candidate / not reviewed / not adopted".
Quotes are in "…". "§" refers to the branch's REPORT.md unless another file is named.

## 0. Head hashes and one-line tasks (LEDGER wording)

| ID | head | model | task (LEDGER) |
|---|---|---|---|
| O-CERT | 17e7f15 (2026-11-02T13:16:47-06:00) | Opus high | "finite-n a posteriori certificates for each fit" |
| O-VCERT | 839bed5 (13:50:58) | Opus high | "same-family verification of O-CERT (Lemma M, C1–C6)" |
| O-SWAP | 5b9b506 (14:03:27) | Opus high | "finite-n prediction of the posterior-miss rates (swap/superset/subset) vs observed" |
| O-DILUTE | abedf99 (13:57:18) | Opus high | "finite-n theory of the study's start masking (dilution)" |
| O-MIX | 26b7708 (13:35:01) | Opus high | "LS0 vs mixture-of-block-starts vs common σ²: which fix proves T38(b)" (REPORT §12 line 8 cites content commit d1cc689) |
| F-SIGMA | e2a3481 (13:54:12) | Fable high | "theory of the common-σ² start (validity, start mass, T38 route (a) without LS0, pilot design)" (REPORT §12 cites content commit 025b8d6) |
| F-MASKPIP | dbe45fa (14:00:37) | Fable high | "what Ẑ / PIPs mean in the masked regime" (REPORT §10 cites content a2ed9b2, helper sim 4d82c31) |
| S-ELS | 90423b1 (13:58:16) | Sonnet (CW) | "E_LS ledger extraction from the laptop fit archive" |
| S-PAPER | 556be30 (13:04:33) | Sonnet high (CW) | "theory-section LaTeX skeleton with STATUS comments" |
| L-LEAN | 42f9de0 (14:13:54) | (laptop, Claude Work) | "Lean 4 formalisation of T21, T07, T11(iii), Theorem A" |
| O-LS0 | 2471709 (12:41:01) | Opus 5.5 xhigh (Owls) | "LS0 post hoc on the 2,400 regenerated datasets" |

**O-LS0 has NO report.** `src/O-LS0/` contains only `_HEAD`. `git ls-tree origin/theory/O-LS0 -- theory_campaign/O-LS0` lists only
`scripts/` (00_regen_data.sh, 01_verify_data.R, 02_g2_checks.sh, 10_ls0_fit.R, 11_run.R, 12_run2_owls.sh, 13_launch_job.sh,
20_aggregate.R, ls0_core.R, ls0_exports.cpp) and one result file `results/data_hash_check.csv` (7 data rows: the two "A: Owls dev"
rows match=TRUE; four "B: NOTS dev (bench_v2 checker)" rows and the one "C: NOTS production" row (p1000_S4_r001) match=FALSE — the
B/C `ref` values are 64-hex vs 8-hex for A, so this may be a hash-convention difference; not interpreted by any report). Last commit:
"O-LS0: aggregator (production comparison, lattice subsample, determinism check), job launcher". 20_aggregate.R would write
`results/ls0_per_fit.csv`, `cell_summary.csv`, `tables.md`, `determinism_check.txt`; none exist. So the LS0 approval condition
("APPROVED by Felipe (2026-11-02), conditional on O-LS0's data check", SR_AUDIT) is still unmet on the branches. S-PAPER README
agrees: "`theory/O-LS0` | `247170905d…` | scripts only, no results; LS0's data check is therefore still pending".

---

## 1. O-CERT — a-posteriori certificates for individual fits (17e7f15)

Header: "Lead: Opus 5.5. **Nothing here is reviewed.** Every PROVED is a candidate that I checked line by line; it is not adopted."
Branch files: REPORT.md + scripts (cert_lib.R, cert_run.R, gen_data.R, run_fit.R). **No `results/` directory is committed.**

Setting (§2): F(S) = log w(|S|) − log W_K + log C_n − ½ log D_S − ν log(2b₀ + Q_S); 𝒯 = any reported set of distinct scored
models (engine: top store, 40p+1 best, and local_search); Z_𝒯 = Σ_𝒯 e^F; g = top[1] − top[2] (best-of-scored gap); box [L,U];
Φ(L,U) and M(L,U) bounds. Hypotheses named: EX-A, EX-S, CAL, START, (H-T12)=T12(iii), GUARD; FP via VAL-FP(η, ε) and new
**SC(η_F)** ("Every score used by the card … is within η_F of its exact value … checkable by replay in higher precision").

| Label | § | Statement (one line) | Hypotheses / premises | Status (verbatim) |
|---|---|---|---|---|
| Lemma M | §3 | For S ⊆ S′: (a) Q_S ≥ Q_{S′}; (b) D_S ≤ D_{S′}; (c) w(k+1) ≤ w(k), k ≤ p−1; (d) Q_S = yᵀy/(n+1) + (n/(n+1))yᵀ(I+(n+1)M_S)⁻¹y, D_S = det(I+(n+1)M_S)/det(I+M_S) | none beyond the score definition; "no rank condition, so it holds at p ≫ n" | "PROVED." |
| Thm C1 | §3 | (a) deterministic π(S) ≤ e^{F(S)}/Z_𝒯, ratios exact, π(S)/π(Ŝ) ≤ e^{−g}; (b) simultaneous: 𝔅_α ∩ 𝒪_E = {Z < αẐ} ∩ 𝒪_E, P(𝒪_E ∩ 𝔅_α) ≤ α·P(𝒜) ≤ α, i.e. π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, αẐ) w.p. ≥ 1−α; "the posterior mass of the *unscored and unreported* models is at least 1 − Z_𝒯/(αẐ)"; (c) no lower bound P(π(Ŝ) ≥ c·e^{F(Ŝ)}/Ẑ) ≥ γ follows from unbiasedness | EX-A, EX-S, CAL, START, GUARD; locked T31(i)(a), T12(iii); W2-BOOK Lemma RO, Prop 2; (c) from locked T31(c) | "PROVED (candidate)." |
| Thm C2 | §3 | Under PW2 (locked T25(iv), Var_c(Ẑ/Z) ≤ B_T/4): P(𝒪_E, ∃S: π(S) < (1−ε)e^{F(S)}/Ẑ) ≤ E[1_𝒜 B_T/(B_T+4ε²)] (Cantelli); joint two-sided band; Corollary: if (1−ε)e^{F(Ŝ)}/Ẑ > ½ then π(Ŝ) > ½ (unique global HPM) | C1 hyps + PW2 | "PROVED (candidate), CONDITIONAL." Author: "Why this is not a data certificate. PW2's constants … are moments of the unknown particle law" — "C2 is a *what-if* statement" |
| Thm C3 | §3 | On any fully scored region R ∋ Ŝ: π(Ŝ\|R) and π(S)/π(Ŝ) exact; (a) local: g_add, g_del, g_swap, ρ_loc exact ("p + \|Ŝ\|(p − \|Ŝ\|) scores"); (b) subset class 2^{\|Ŝ\|}−1 ("16,383 scores at \|Ŝ\| = 14"); (c) best-of-scored π(S) ≤ e^{−g}π(Ŝ) on 𝒮̄∖{Ŝ} | EX-A (or SC(η_F): factors e^{±2η_F}, margin ≥ 2η_F); `local_certified` meaning from locked T20(i) | "PROVED." |
| Thm C4 (box certificate) | §3 | F(S) ≤ Φ(L,U) and Σ_{[L,U]} e^F ≤ e^{M(L,U)}; B&B partition of [∅,U]: (a) optimality "Ŝ is the exact HPM among all 2^{\|U\|} models built from U"; (b) π(Ŝ\|[∅,U]) ≥ (1 + Σ_leaves e^{M−F(Ŝ)})⁻¹; (c) constructive refutation / search-miss detection | EX-A (SC: F(Ŝ) − 2η_F); needs only (X, y, Ŝ); "valid for every choice of U, including a data-dependent one" | "PROVED." |
| Cor C5 (posterior-miss certificate) | §3 | In C4(a) setting, on {S₀ ⊆ U}: Ŝ ≠ S₀ ⇒ F(S₀) ≤ F(Ŝ) (posterior miss); P(𝒪, Ŝ ≠ S₀, F(S₀) > F(Ŝ)) ≤ P(𝒪, C4(a) fails for U) + P(𝒪, S₀ ⊄ U) | C4; the last term "is a screening probability … At n = 200 it is measured, not proved, in §4" | "PROVED." |
| Thm C6 (certificate card) | §3 | Card = L (local, deterministic), R (region, deterministic), G (global one-sided level α), C (conditional C2, "not counted as certified"); P(𝒪 and some L, R or G claim false) ≤ α·P(𝒜) ≤ α "for every n, p and data set, with no asymptotics, and without conditioning on completion"; with FP: α·e^η + ε | EX-A, EX-S, CAL, START, GUARD; VAL-FP, SC(η_F) | "PROVED (candidate)." Paper sentence: "*Each fit reports a certificate card whose claims hold simultaneously with probability at least 95%, at the actual n, whether or not the run completes.*" |

What the card does NOT say (§3): "It does not say that π(Ŝ) is large. That needs C2 (PW2) or enumeration." / "It does not say Ŝ = S₀." /
"It does not say that the global HPM was found. That needs [∅, U] = Ω, impossible at p = 500."

Numerics: §4 "Illustration (p = 500, n = 200, production engine)" contains only "(Filled in below from `results/cards.txt`.)" — **empty**;
headline item 5 claims "Illustration on 4 regenerated study datasets (p = 500, n = 200, production engine, study seeds): §4" but no numbers
exist on the branch. C4's cost remark ("tree's size grows like 2^{(number of ambiguous variables in U)}") and C5's "measured" screening
term are therefore unsupported (O-VCERT S4).

What fails (§5, verbatim heads): "A lower bound on π(Ŝ) from Ẑ alone. It is impossible (C1(c))." / "Making it two-sided with the 4-island
spread or the empirical ESS. This fails." / "T13 restricted ESS … cannot replace PW2 as a data certificate." / "Using islandwise
E[Ẑ_r q̂_r(1_{S})] = Zπ(S) to lower-bound π(Ŝ). It fails twice." / "A global box certificate. Q_{[p]} ≈ yᵀy/(n + 1) when p > n, so
Φ(∅, [p]) is astronomically large … |U| ≪ n."

Needs escalation (§6): "C1 and C6 rely on Lemma RO and GUARD (W2-BOOK, unreviewed). A cross-family check of the output-level step is
needed." / Lemma M(b) check and engine Q (§6.13 recomputation branch) identity / "SC(η_F): someone should replay the card's scores in
long double or mpfr to fix η_F for the paper."
Outside scope (§7): C4 as a method-agnostic certificate for SuSiE/SSL/lasso supports ("a fair, finite-n comparison of *posterior*
optimality (not of recovery)"); C4(c) "box scan" search-miss detector inside the engine = method change under the investment rule.

Confidence card (§8, abbreviated, verbatim cells): Lemma M "high | done (PROVED, 1 page)"; C1 "high | done (corollary of locked T12/T31 +
Lemma RO)"; C2 "high (as an implication) | done; **useful only if PW2 is proved**, which is open"; C3 "high | done (trivial, but it is the
only exact posterior statement at n = 200) | no (post-hoc rescoring, about 7k + 16k scores)"; C4/C5 "high | done; cost is empirical (§4)
| … P(S₀ ⊄ U) is statistical | no for post-hoc; yes if built into the engine"; C6 "high | done (candidate), modulo W2-BOOK review of Lemma
RO/GUARD"; "π(Ŝ) ≥ ½ certified" "**not possible** without PW2 or enumeration (C1(c))".
Overall: "It cannot turn any of this into "Ŝ is probably right", and the paper should say so."

## 2. O-VCERT — referee report on O-CERT @ 17e7f15 (839bed5)

Method: "Independent code: `scripts/vcert_check.py`, written from `00_COMMON.md` only (not from O-CERT's `cert_lib.R`). Output:
`results/vcert_check.txt`. No helpers were spawned. Everything below is a referee verdict, not adoption." Also read engine source
`Scripts/SMC_BVS/core/cpp/` and SR_AUDIT.md. Same-family (Opus checking Opus).

### Verdict table (§1, verbatim)

| Item | Verdict | One-line reason |
|---|---|---|
| Lemma M (a) Q_S ↓ | **VERIFIED** | "Push-through identity ⇒ … Loewner order reverses under inversion. 0 violations in 476,160 exhaustive (S, S+j) pairs." |
| Lemma M (b) D_S ↑ | **VERIFIED** | "Determinant lemma; h(c) = 1 + c·xᵀ(I+cM)⁻¹x has h′ = xᵀ(I+cM)⁻²x ≥ 0 (derivative re-derived). log D rises by ≥ 5.6·10⁻³ per addition in every test, duplicates included." |
| Lemma M (c) w ↓ | **VERIFIED** | "w(k) = ½/C(2p−1,k) is exactly the BB(1,p) per-model prior; ratio (k+1)/(2p−1−k) ≤ 1 for k ≤ p−1, and K ≤ p." |
| Lemma M (d) | **VERIFIED** | "Both n×n forms agree with the k×k definitions to 8·10⁻¹³." |
| Thm C1 (a) | **VERIFIED** | "Z ≥ Z_𝒯 holds deterministically. The engine's 𝒯 has distinct models (TopStore keyed by (F, S), and F is a function of S)." |
| Thm C1 (b) identity and simultaneity | **VERIFIED** | "{∃S: π(S) > u_α(S)} = {Z < αẐ} does not depend on S, so selecting Ŝ costs nothing. 0 mismatches over a grid of (𝒯, Ẑ, α)." |
| Thm C1 (b) probability | **VERIFIED, conditional on W2-BOOK** | "It is exactly W2-BOOK Prop 2(e1). The Lemma RO inclusions are elementary and I re-checked them. GUARD is an implementation hypothesis, not checked here." |
| Thm C1 (b), last sentence ("unscored and unreported" mass) | **GAP (wording; counterexample)** | "The bound is on the mass **outside 𝒯**, not on the *unscored* mass. Counterexample in §2.1; repair R1." |
| Thm C1 (c) | **VERIFIED** (as a non-implication) | "Correct use of T31(c). The prose built on it in §1, §5 and C6 overreaches; see S2." |
| Thm C2 | **VERIFIED (conditional on PW2)** | "Cantelli is applied in the right direction. The bound is attained by a two-point law, so it is tight. Transfer to the output goes through Lemma RO(2)." |
| Thm C3 | **VERIFIED** | "Z cancels. (c) holds for 𝒮̄ = the ledger's logical scored set, checked in the code (§3)." |
| "Fully scored region" well defined | **VERIFIED, with a scope note** | "C3 allows post-hoc rescoring, so any R is admissible. The run exports only 𝒯, the leader stores, Ŝ and the flags, so "scored by the run" in practice means 𝒯 or a recomputed region." |
| Thm C4 | **VERIFIED** | "0 Φ-violations and 0 M-violations over all 285,712 boxes on 48 designs (including p > n, duplicate and factor designs, and the binding cap K). B&B agrees with brute force 80/80, and the mass lower bound is valid 40/40." |
| Cor C5 | **VERIFIED, with a tie caveat** | "Exact tie F(S₀) = F(Ŝ) with S₀ ≺ Ŝ: see S3. It also needs \|S₀\| ≤ K." |
| Thm C6 (card), exact arithmetic | **GAP (repairable)** | "The probability space is right: unconditional, output level, via Lemma RO. But the G item "unscored mass ≥ 1 − Z_𝒯/(αẐ)" can be false on the good event (§2.1). With R1 the theorem holds." |
| Thm C6, floating-point clause | **GAP (repairable)** | "It omits the SC(η_F) inflation of the G items: Z_𝒯^fp can exceed Z. Repair R2." |
| §4 illustration (p = 500) | **MISSING** | "`results/` is not on the branch and §4 is empty at `17e7f15`. There are no reported numbers to reproduce (S4)." |

"No ERROR was found in the mathematics of Lemma M or C1–C5. The two GAPs that affect a theorem statement (C1(b)'s last sentence, and C6) are
repaired below."

Overall per theorem (§6, verbatim): Lemma M **VERIFIED**; C1 "**VERIFIED** (conditional on W2-BOOK Lemma RO/GUARD), with the last sentence
replaced by R1"; C2 "**VERIFIED** as a conditional implication (PW2); not a data certificate, as O-CERT says"; C3 "**VERIFIED** (with 𝒮̄ read
as the SR logical scored set; code-checked)"; C4 "**VERIFIED**"; C5 "**VERIFIED** with the tie and K caveats (S3)"; C6 "**GAP → VERIFIED
after R1 and R2** (exact arithmetic: R1 only)".

Counterexample §2.1 (factor design, n = 40, p = 10, all models scored, Ẑ = Z): m = 3, α = 0.5 → claimed "unscored" ≥ 0.590, true unscored 0,
true mass outside 𝒯 0.795; m = 10, α = 0.5 → 0.007 / 0 / 0.504. "O-CERT's own `cert_run.R` prints the correct phrase ("posterior mass outside
the top store"). The REPORT text disagrees with its own code."
§2.2: FP "logical gap, not an observed failure: η_F is tiny in practice."

Repairs: **R1** replace "unscored and unreported" by "**not in 𝒯**"; optional unscored-mass bound
π(unscored) ≥ 1 − [Z_𝒯 + (N̄ − |𝒯|)₊·e^{F_min}]/(αẐ) with N̄ a reported count of distinct scored models; remark → "the reported store holds less
than α of the posterior". **R2** u_α^fp(S) := exp(F^fp(S) + η_F)/max(e^{−η_F}·Z_𝒯^fp, α·Ẑ^fp), failure prob ≤ α·e^η·P(𝒜) + ε.
Smaller points: S1 (C4 leaves with |L| > K vacuous; double counting conservative); **S2** "§1 item 1, §5 first bullet and C6 "cannot certify
confidence … without PW2 or enumeration" overstate C1(c)" — any certified upper bound on Z (inventory UB, Lemma-M box cover, T31's Ẑ ≥ e^{−Δ}Z)
gives a lower bound; reword "not from unbiasedness; it needs an upper bound on Z (PW2, UB, enumeration, or a bound on Δ)"; **S3** C5 needs
F(S₀) < F(Ŝ) strictly or tie order, plus |S₀| ≤ K; **S4** §4 empty, "Every numeric claim of O-CERT (tree sizes, "cost grows like
2^{#ambiguous}", P(S₀ ⊄ U) "measured") is therefore unsupported"; own B&B "visited a median of 272 nodes for |U| = 13 (8,192 leaves)"; "I did
not reproduce the p = 500 runs: R and the study datasets are not on this laptop."; **S5** C1/C6 inherit W2-BOOK's unreviewed status; "GUARD
itself is a code fact that I did not audit."
Free corollaries found: engine §6.13 Q branch "algebraically the same function"; "Lemma M(d) gives Q_S ≥ yᵀy/(n+1). So the trigger
Q < 10⁻⁸yᵀy can never fire in exact arithmetic when n + 1 < 10⁸; the branch is a pure floating-point safeguard." Also "HQ's premise needs a
correction. Under BB(1,p), **both** the per-model weight w(k) and the size marginal C(p,k)w(k) are non-increasing in k … The object that is
*not* monotone is the marginal likelihood m(S), and hence F. In the tests, m rises on 185,095 additions and falls on 291,065"; endpoint
evaluation max(F(L), F(U)) underestimates the box max "in 2,764 of 6,561 boxes".
Code checks (§3.4): TopStore::offer (`v3_ledger.h:47–55`) keeps the top-cap distinct models; evicted cannot re-enter; Ŝ = top[1];
calibration CalState top-(40p+1) and leader stores exported and offered as "inherited" (`v3_core.cpp:409–419`).
Reproduction: `python -I scripts/vcert_check.py 20261102 results/vcert_check.txt` (~5 min, 1 core); 150 designs (iid, AR(0.9), exact/near
duplicates, factor), n ∈ {5, 6, 12, 30, 40}, p ∈ {8, 9, 10}.

## 3. O-SWAP — finite-n theory of the posterior misses (5b9b506)

Headline status (verbatim): "Props 1–3 PROVED under the projection approximation PA (Lemma 0, PROVED; its error is O(10⁻³) nats). Thm 4,
Prop. 5 and Prop. 6 PROVED. Cor. 2.1 PROOF SKETCH. Predictor T2 is an approximation. The SuSiE/SSL link is a CONJECTURE."
Setting: n = 200, p ∈ {500, 1000}, s₀ = 14, θ = c·β, β pattern (1.4, −1, 1.8, −1.2, 0.8, −1.6) cycled, c ∈ {1, 0.5}, σ = 1; all
probabilities conditional on X. New quantities ρ_{jl} (partial correlation given other truths), δ_j = θ_j‖r_j‖/σ, κ⁺_l (add), γ_j (drop),
κ_{jl} (swap; size prior cancels exactly), ω₀ = pseudo-observation term (≈ 24 at c = 1, ≈ 6 at c = 0.5).

| Label | Statement | Hypotheses | Status (verbatim) |
|---|---|---|---|
| Lemma 0 (PA) | Q_S = Q̃_S + η_S, Q̃_S = E_S + W_S/(n+1), η_S ∈ [0, nW_S/((n+1)((n+1)λ_min+1))]; one-move error O(10⁻³) nats | any X | "PROVED." |
| Prop 1 (within-size swap) | exact event in (A, B, E_U, W_{T_j}); at κ_{jl} = 0: **P_swap = Φ(−d₋)Φ(d₊) + Φ(d₋)Φ(−d₊), d∓ = \|δ_j\|√((1∓ρ)/2)**; P_swap ≈ Φ̄(√(M_{jl}/(1+ρ))) with T37R margin M_{jl} = δ²(1−ρ²)/2 | PA | "PROVED under PA." |
| Prop 2 (superset by one null) | P_add(l) = P(χ²₁(1 − λ_l/(n+1)) > (λ_l − 1)(χ²_{n−2−s₀} + ω₀)); B_l central for every design | PA | "PROVED under PA." |
| Cor 2.1 | superset rate p-free: t_add² ≈ 2κ⁺(1+η), BB(1,p) term "cancels the multiplicity of the nulls almost exactly"; rises as SNR falls (ω₀) | PA | "PROOF SKETCH (expansion); the numbers are exact evaluations of Prop. 2." |
| Prop 3 (subset/drop) | P_drop(j) = E[Φ(t − \|δ_j\|) − Φ(−t − \|δ_j\|)] | PA | "PROVED under PA." |
| Thm 4 (first-order bracket) | max_e p_e ≤ P(L\|X) ≤ P(S₀ ≠ S†\|X); P(L\|X) ≤ Σ_e p_e | exact F, no PA | "PROVED (exact F, no PA needed for the inequalities)." |
| Prop 5 (swap ceiling, Le Cam) | any selector: ½[P_μ(Ŝ≠S₀) + P_{μ′}(Ŝ≠S′)] ≥ Φ(−\|δ_j\|√(1−ρ²)/2); exponent ratio vs HPM (1+ρ)/2 (0.93 at ρ = 0.85) | Gaussian | "PROVED (standard two-point bound)." |
| Prop 6 (cluster representation) | B_{jl} = ρ_{jl}A_j + √(1−ρ²)Z_{jl}, Z central, independent of A_j | — | "PROVED (exact, no PA). Predictor T2: approximation." |
| T1 / T1-lo / T2 predictors | independence / cluster-max / conditional-on-(A_j, E) | approximations (a)–(c) | "It is an approximation, not a bound." |
| SuSiE/SSL threshold story | higher threshold wins at c = 1, loses at c = 0.5 | — | "CONJECTURE" (thresholds not derived) |

Cor 2.1 table (leading-order): p = 500 c = 1: κ⁺ 6.84, t_add 3.85, q 1.51e−4, family-wise 0.071, t_drop 3.88; p = 500 c = 0.5: t_add 3.68,
q 3.03e−4, 0.137; p = 1000 c = 1: κ⁺ 7.54, t_add 4.05, q 6.88e−5, 0.066; p = 1000 c = 0.5: t_add 3.87, q 1.48e−4, 0.136.

**Numerics — on what data.** Study data regenerated in Python: `rgen.py` ports `gen_prod_data.R` and R's Mersenne-Twister/Inversion rnorm
"exactly" (matches `set.seed(1); rnorm(5)`, `set.seed(42); rnorm(3)`); "every one of the 1,200 study designs X, every ε, every S₀ and every
β is the study's own" (1,200 designs × 2 scales = the 2,400 fits). Per dataset: analytic Props 1–3 (exact κ's), T1, T1-lo, T2, Le Cam floor;
**realised check on the study's own y** under exact F (≈ 14p one-move neighbours + 91 double drops + hill-climb); conditional MC with
R = 40 fresh noise vectors given X ("8,000 draws per cell and scale"). Observed = SMC-BVS v3 HPM from
`Results/SMC_BVS_v3_production/p*/exact_recovery_long.csv`; "The 4 no-output fits are excluded, and their cells are rescaled to 100."
Runtime "4 cores, ≈ 35 min in total".

Key numbers (per 600 = 6 cells × 100):
- c = 1: observed 40 / 37 (p = 500 / 1000), realised 39 / 37, MC 41 / 38, **T2 43 / 40**, T1 46 / 43, T1-lo 10 / 9; RMS z (obs vs T2) 0.86,
  (obs vs MC) 0.93.
- c = 0.5: observed 230 / 259, realised 227 / 257, MC 230 / 249, **T2 251 / 271**, T1 326 / 383, T1-lo 118 / 141; RMS z 1.38 / 1.22.
- Largest cells: p500 S4 c0.5 observed 75 (5/5/65 extra/missed/mixed) vs T2 73.2, MC 65.3; p1000 S5 c0.5 observed 68 vs T2 59.4, MC 56.9
  (z +1.8 / +2.4); p500 S5 c0.5 observed 41 vs T2 52.4 (z −2.3).
- Le Cam floor ≤ 0.4% at c = 1; up to 9.1–9.2 (S4) at c = 0.5.
- §4.3(1): "The realised check on the study's own y reproduces the observed SMC-BVS count in every one of the 24 (p, S, c) cells to within ±1
  (the type split to within ±2)." Caveat: "Per-dataset SMC outputs are not on the laptop, so this is a match of counts per cell, not of
  datasets one by one."
- Validation: P_swap quadrature vs MC to 0.001 (δ = 4, ρ = 0.85, λ = 1.002: 0.1160 vs 0.1163); P_add 3.10e−4 vs 2.65e−4 ± 0.26e−4 (1.7 SE);
  fast scores vs brute-force F max |diff| 8.5e−13 over 60 comparisons.
- `out/TABLES_local.md` = the same two tables as REPORT §4.2 (identical numbers; checked).

Why modes switch (§5): adds face a nearly fixed prior threshold ("≈ 7 % per dataset, every scenario" at c = 1, "≈ 14 %" at c = 0.5); drops
and swaps exponential in δ² ∝ c². "So at c = 1, the only event with non-negligible probability in every scenario is the superset."
SuSiE/SSL (§5): "SuSiE goes from 585/600 to 220/600, SSL from 569 to 303, and SMC-BVS from 559 to 370" (exact recoveries at p = 500); the
theory "does **not** support … that SuSiE's or SSL's effective threshold actually is t′ ≈ 4.5–6" nor SuSiE's S5 collapse (3/100, 0/100).

What fails (§6): T1 independence overshoots at c = 0.5 by 40–50%; T1-lo far too low; "A rigorous upper bound via Šidák or Royen's Gaussian
correlation inequality was not obtained … OPEN."; L is only a lower bound for P(S₀ ≠ argmax F) — "That is empirical, not a theorem."; old
`run_cells.py` needs server .rds (superseded).
Needs escalation (§7): (1) Prop 1 step 2 + general-λ quadratic second reader; (2) rigorous T2 bracket; (3) PA error → probability via
anti-concentration "routine but unwritten"; (4) SuSiE/SSL thresholds.
Outside scope (§8): SuSiE S5 collapse; "**The HPM delivers what the posterior says.** … it means T38/T21's discovery term contributes
nothing at n = 200 for these cells. A natural target for T03/T02: report "P(posterior miss)" as a named quantity predicted by Props 1–3.";
"The τ = 1 pseudo-observation acts as an SNR-dependent size penalty".
Confidence card (§9): swap "high | done; second reader wanted"; superset/subset "high | high"; Prop 6 "high | done"; T2 "medium-high (as an
approximation) | medium (bracket)"; prediction vs observed "high | n/a (empirical)"; T07 link "high | a whole-model floor (Assouad over the
14 truths) is OPEN, medium"; SuSiE/SSL "medium | low-medium". No method change needed for any item.

## 4. O-DILUTE — start masking by σ²-dilution (abedf99; REPORT.md + THEORY.md)

Run on "Felipe's laptop (Python 3.12; R is not available)". Status words "candidate … not reviewed or adopted".

### Named results (THEORY.md section; status verbatim from REPORT §2 table and THEORY headers)

| Label | THEORY § | Statement | Hypotheses | Status |
|---|---|---|---|---|
| Thm E | §1 | π₀(S) = ∏_b π_b^t(S_b)·A_t(\|S\|) for every t > 0; at S₀ A_t(s₀) = 1/E_t[e^{g_t(N)}1{N≤K}] | "any data, any partition, positive tables" | **PROVED** |
| Cor E1 | §1 | −log π₀(S₀) = V_t (visibility, Σ softplus(−λ_b)) + C_t (competition) − log A_t (size) | as Thm E | PROVED |
| Cor E2 | §1 | t ∈ I₀ ⇒ log π₀(S₀) ≤ −V_t − C_t − log P_t(N ≤ K); "sharpens W3-VEXP Prop D" | as Thm E | PROVED |
| Thm R | §2 | exact joint law of (#truths, #non-truths) under π₀; π₀(R_d) = P(M ≤ d), π₀(B_d); Markov π₀(R_d) ≥ 1 − E M/(d+1); "R_d ⊇ 2^{S₀}" | as Thm E | **PROVED** |
| Lemma N | §3 | Gaussian null independent of (y, X_{−l}): r_ly² ~ Beta(½, (n−2)/2) exactly — "the v3 table scores a null exactly as it would score it in a pure-noise data set" | x_l^r Gaussian, independent | **PROVED** |
| Cor N1 | §3 | expected null inclusions Θ(s₀√(log p)/√n) "about 1 at the study size, independent of c" | Lemma N | "PROVED for the expectation bound …; PROOF SKETCH for the in-probability constant" |
| Lemma L | §4 | common plug-in σ² multiplies every null's exponent by v/σ̂² (≈ 7 at c = 0.5, ≈ 25 at c = 1); oracle-σ² start fills to K; F-DRAFT Lemma W1 needs **in-sample** BO, the study has only **population** BO | Lemma N | "PROVED (identity) + PROOF SKETCH (extreme-value consequence)" |
| Prop S | §5 | π₀(S₀) ≤ 1/∏_i(1 + [M_{j(i)} − i + 1]₊) for v3 tables **and every common σ²** | any data, partition | **PROVED** |
| Prop D′ | §6 | λ_j ≈ ½χ²₁(nρ_j²) − ½ log n − log((2p−s₀−1)/(s₀+1)), ρ_j² = (1 − κ_j)x_j ≤ ω_j (saturating in c); assembled log π₀(S₀) formula | population BO, Gaussian design | "PROOF SKETCH (population limit)" — "Not every step is verified: the joint (not marginal) law of the λ_j and the treatment of the BB-size coupling … are approximations, checked numerically only." |
| Prop DM (paper wording) | §7 | (i) exact deficit decomposition + ceiling; (ii) ranking ceiling for v3 and any common σ²; (iii) π₀(R_d) = P(M ≤ d); dilution clause | (i)–(iii) any data; dilution clause population BO | "(i)–(iii) PROVED; dilution clause PROOF SKETCH" |
| Conj DM-asy | REPORT §2 | growing s₀ = s_n, n/(s_n log(pn)) → κ: visible fraction → limit in (0,1); π₀(S₀) → 0 while π₀(R_d) bounded below | population BO | CONJECTURE |

Proposed paper sentence (THEORY §7): "At the study's n = 200, s₀ = 14, p ∈ {500, 1000}, about half of the truths have λ_j < 0 (V_t ≈ 20–50
nats) while E_{π₀}[M] ≈ 0.7–3.8: the per-cell median π₀(S₀) is 10^{−11}–10^{−26} while π₀(R₂) has median 0.79 … This is the regime of T38(b):
the start is masked, but its mass is on the near-truth region R_d — through **subsets** of S₀ that are 6–11 additions from S₀ — so delivery
must come from the bridge and the Gibbs/addition moves, not from iid start draws."

### Numerics — on what data
"R is not on the laptop, so `scripts/dilute.py` reimplements `gen_prod_data.R` in law … The datasets are not bit-identical to the study
files, because numpy's RNG is used. 20 replicates per (p, S); c ∈ {1, 0.5}; 480 fits." (NOT the 2,400 fits; simulated equal-in-law.)
Method port: complete linkage on 1 − |r| (scipy), R13 left-child rule, left-first top-down cut, next-fit packing, B = 14, K = 100.
- Decomposition shares: "V carries 83% of −log π₀(S₀), C carries 11% and the size term 6%."
- Median π₀(S₀) 10^{−15.7} pooled; per cell 10^{−11.1} (p500 S1 c1) to 10^{−25.6} (p1000 S5 c0.5); study "≈ 10⁻¹² or smaller".
- Median π₀(R₂) 0.794 pooled (study ≈ 0.8); per cell 0.20 (p500 S4 c1) to 0.96; π₀(R₁) 0.52; π₀(Hamming ≤ 2) 8·10⁻¹¹.
- Favourable fits 0/480 (study 1/2,394). E[#truths] 2.4–6.6, E[#extras] 0.7–3.8 per cell; E|SΔS₀| 8.3–14.2; start mode 2.5–6 of 14 truths.
- Gain ratio table (table vs posterior keep-j): c = 1, β = 1.8: LO₀ 6.1 (0.92 > 0), LO₁ 127.6; ratio 0.099 vs population 0.094 … β = 0.8 at c = 0.5:
  LO₀ −4.9 (visible 4%), LO₁ 7.0 (0.96); "At c = 1 the table sees 6–10% of the posterior gain, and at c = 0.5 it sees 16–20%."
- c → ∞ ceiling: λ^∞ = {1.4, −2.7, 7.2, −0.8, −4.2, 4.1} for β = (1.4, −1.0, 1.8, −1.2, 0.8, −1.6) at p = 500: "7 of 14 truths stay invisible at
  *every* scale", Σ softplus = 19.9 nats (10^{−8.6}). Start favourable only at "n ≈ 590–730".
- Prediction vs exact (log₁₀ medians): within 0.1–1.3 in S1/S2/S5; S3/S4 underpredict by 1.0–1.6 (proxy competition, "C is 3.5–8.0 nats there,
  against 1.5 predicted"); S6 within 0.8.
- d(S₀) ≈ 105 nats (c = 0.5), ≈ 210 (c = 1); F-DRAFT W1 BO formula "undefined (Σ_b ξ_b ≥ 1) in 132 of 480 fits and off by a median of 57
  nats elsewhere".
- T27 bracket: overstates −V by 24–37 nats per fit (~3.5 nats per masked truth).

### Candidate fixes evaluated (REPORT §5, "pilot evidence only, no method change decided")

| variant | median log₁₀π₀(S₀) | median π₀(R₂) | median π₀(Ham ≤ 2) | favourable /480 | start mode |
|---|---|---|---|---|---|
| v3 (method) | −15.7 | 0.79 | 8·10⁻¹¹ | 0 | 2.5–6 truths, ≈ 1 extra |
| known_oracle (true σ², median σ̂² 0.086) | −690 | 0.00 | 0 | 0 | 8–14 truths + 86–90 nulls (cap K = 100) |
| known_mode1 (RSS of v3 start mode, median 0.50) | −18.8 | 0.00 | 5·10⁻¹⁴ | 0 | 3–12 truths; E[#extras] 3–37 |
| known_iter (fixed point, median 0.13) | −363 | 0.00 | 0 | 0 | to the cap except in S5 |
| resid (backfit; "not asked; added as a diagnostic") | −1.0 | 0.71 | 0.60 | 378 | 14/14 in most cells; S5 and S4 at c = 0.5 weaker |

- **Common plug-in σ²** — verdict verbatim: "The common plug-in σ² variant would **not** raise π₀(S₀). It lowers it by 3 orders with a realistic
  plug-in and by hundreds of orders with the oracle, and it destroys π₀(R_d). Do not adopt it." Prop S: per-cell median ceiling
  10^{−0.8}–10^{−4.8} (10^{−6.7}–10^{−10.6} in S5) for EVERY common σ². Confidence card: "**false** at the study size … | reject the change".
  (§7: "Prop S's numbers were first written as "10^{−3}–10^{−6}" before the run; they are corrected to the computed 10^{−0.8}–10^{−4.8}.")
- **Backfit (partial-residual) tables** — "raised the median π₀(S₀) to 10^{−1.0} (378 of 480 fits favourable) in a pilot. This is outside the
  asked variant and flagged for HQ." Weak in S5 (10^{−4.6} to 10^{−19}) and S4 at c = 0.5. Cost "(sweeps + 1) × the §6.3 table work".
  Validity: positive product-form, (X, y) + deterministic pilot ⇒ F-DRAFT Prop P(i); "T22(iii)'s regime conditions would need restating."
  "This is a candidate method change under the investment rule; it needs HQ's and Felipe's call and a pilot of the full sampler." Card:
  "medium (pilot only; S5 weak) | unknown | … | would be one (not decided)".
- **LS0 / T38(b) link** (§6): LH-iid "LS0 repairs in c moves"; dilution start mass is "|V| ≈ 7–10 additions away (median E|SΔS₀| = 8–14). The local
  search budget ℓ = 10–11 is borderline. This agrees with HQ's finding that delivery comes from Gibbs flips, not the local search." "T38(b)'s
  eligibility premise "π₀(R_d) ≥ b_n" therefore holds at the study size (Thm R + Lemma N). Its repair half must be an addition-path
  (T24/Gibbs-type) argument with |S₀ ∖ S| ≈ s₀/2, not a d-local one."
- T27 connection: three regimes on one axis W_j (favourable / cancellation masking T27(i), LH / **dilution masking**); "Dilution masking needs
  n·ω_min ≍ log(pn) … asymptotic home … a growing-s₀ (or local-alternative) family, not LH-iid".

What fails (§7): common σ² route; F-DRAFT d(S₀) BO formula as finite-n predictor ("undefined in 28% of fits"); single-variable λ_j in S3/S4;
Prop S as explanation of the 10⁻¹⁵ level ("only a ranking ceiling").
Needs escalation (§8): Prop D′ joint law ("candidate for a stronger prover"); Lemma L(b) extreme-value step; Conj DM-asy; "Independent check of the
port … A bit-exact check on the stored study `.rds` files with the R engine would confirm the per-cell medians. The study's own per-fit π₀ values
were not available locally."
Outside scope (§9): backfit tables; F-DRAFT Theorem W premises should say "in-sample BO" (Lemma N changes the p^{R²} factor); "Reporting π₀(B_d)
alongside π₀(R_d) in the paper would avoid overstating "near"."

## 5. O-MIX — LS0 vs mixture of block starts vs common σ² (26b7708)

Candidates: (A) LS0 (local search from S̃₀ = argmax π₀, centre emitted); (B) mixture start π₀^mix = Σλ_iπ₀^{(i)}, concrete **(B-merge)**:
m = 2, λ = (½, ½), 𝒫₁ = v3 partition, 𝒫₂ = 𝒫⁺ = merge link-graph components (τ_n = 3√(log p/n)), size cap B⁺ = 16; (C) common plug-in σ̂²
tables r_b^C(U) = D_U^{−1/2}exp{t_U/(2σ̂²)}, concrete (C-fix) fixed-point plug-in; (C-grid) mixture over a σ̂² grid.

| Label | Statement | Hypotheses | Status (verbatim) |
|---|---|---|---|
| Prop B1 | exact samplability + exact density of π₀^mix; T09(ii)–(iv), T12, T13, T22(iv) verbatim; T22(i) per component ×λ_i; T22(ii-a) becomes sandwich min_iρ_i ≤ … ≤ max_iρ_i; weight stability sup π/π₀^mix ≤ min_i λ_i⁻¹ sup π/π₀^{(i)} | partitions fixed before start randomness | "PROVED." (re-proves F-DRAFT Prop P(ii); "I read only the statements" of T09/T12 — escalation 2) |
| Prop B2 | random partitions do not undo LH masking: π₀^𝒫(S₀) ≤ e^{−cn} if hub separated from group-mate | LH exact Gram | "PROOF SKETCH (crux PROVED)." |
| Lemma B-link | link graph recovers exactly the linked pairs | LH | "PROVED (exact Gram); PROOF SKETCH (iid)." |
| Thm B3 | (B-merge) on LH exact Gram: π₀^mix(S₀) ≥ ½ − O_P(2^{2g}n^{−1/2}); Q_f ≥ 4N_e iid draws score S₀; P(𝒪 ∩ {Ŝ≠S₀}) → 0 **without LS0** (T38(b) via route (a)) | LH, exact Gram, p ≤ n−1, g ≤ B_n < 2g, 2g ≤ 16, ψ_i ≠ 0, \|ψ_i\| < min ρ, ≥ 2 signal blocks in 𝒫⁺ | "PROVED-UNDER the VERIFIED W1-EXP Thm 6, the locked T03, T11(iii) and T21, and Prop B1." LH-iid: "PROOF SKETCH". Hub-move variant: "PROOF SKETCH" |
| Prop C0 | (C) validity: T09, T12, T13, T21, T22(i)(ii)(iv) verbatim; table-specific expansions (EXP′, T22(iii), T27(i), W1-EXP Thms 3–6) need re-checking | σ̂² frozen before start randomness | "PROVED." |
| Thm C1 (O-MIX) | under in-sample BO: d^C(S) = h(t_S); π₀^C(S₀) ≥ π(S₀)·exp{−νψ(u)}; plug-in with \|Q_{S′} − Q_{S₀}\| = o(√n) ⇒ π₀^C(S₀) ≥ π(S₀)(1 − o_P(1)) | BO: X_{C_b}ᵀX_{C_b′} = 0 | "PROVED." ("That the (C-fix) iteration delivers such an S′ is CONJECTURE.") |
| Prop C2 | σ̂²-grid mixture: π₀^grid(S₀) ≥ π(S₀)e^{−η²/2(…)}/m, cost log m = ½ log n + log log n + O(1) | BO | "PROVED (under BO)." |
| Prop C3 | cancellation masking untouched by (C): π₀^C(S₀) ≤ p^{−c}n^{−c/2}e^{O_P(1)} on CL(0) chains | H1, CL(0), σ̂² ≥ σ_lo² | "PROVED." |
| §4.4 null inflation | start concentrated iff σ̂²/σ² > 2A/(2A+1); overfitting plug-in floods start | BO | "PROOF SKETCH." |

What each fix buys (recommendation table §8, verbatim cells):
- **Masking mechanism fixed**: (A) "cancellation (via lattice repair from S̃₀ = S°)"; (B) "**cancellation** (start mass ≥ ½ on S₀)"; (C) "**dilution**
  (BO: exact, Thm C1); **not** cancellation (Prop C3)".
- **T38(b) on LH without other method changes**: (A) "PROVED-UNDER verified/locked inputs (W4, b1-LH)"; (B) "**PROVED-UNDER** the verified W1-EXP Thm 6 +
  locked T03/T11(iii)/T21 (Thm B3), via **route (a)**, the strongest route"; (C) "**No** (route (a) fails, (b1′) unchanged)".
- **LH-iid (p ≫ n)**: (A) "W3-PXN, unverified"; (B) "PROOF SKETCH"; (C) "no".
- **Extra premises**: (A) "(M2) lattice progress, family-specific; ℓ ≥ Φ(S°) − 1"; (B) "link detection (τ_n), merged size ≤ 16, ≥ 2 signal blocks"; (C)
  "plug-in condition |Q_{S′} − Q_{S₀}| = o(√n) (CONJECTURE for C-fix); σ̂² floor".
- **Method-change size**: (A) "small, post hoc; no particle touched"; (B) "medium: start sampler + density (m = 2), link graph, engine change in d"; (C) "small in
  code (tables only), but changes *every* table and the start's character".
- **Score cost**: (A) "+(ℓ+1)·max_k[p + k(p−k)] ≈ 1.7·10⁵ at p = 1,000" (§5: "about 1–3 s"); (B) "+ ≤ |E|·2^{2B} table scores (capped at 16) + O(1) per
  score" (§3: "a few times the table cost (2.9 s at p = 1,000, B = 14) and < 5% on SMC scoring"; at B = 14 merged 10+10 capped → hub-move variant ≈
  |E|·2^{16} scores; S5 links every pair so "(B) degenerates to the base start (no harm, no help)"); (C) "≈ 0 (same table count); C-grid ×m ≈ ½√n·log n
  tables".
- **Risk to locked results**: (A) "none"; (B) "T09/T12/T13/T22(iv) verbatim; T22(i) ×λ; **T22(ii-a) becomes a sandwich**; T27(i)/W1-EXP chain results apply per
  component"; (C) "all locked identities verbatim; **T22(iii), T27, EXP′, W1-EXP Thms 3–6 need re-derivation** for the new tables".
- **Risk to performance**: (A) "O-LS0 data check pending"; (B) "bounded: π₀^mix ≥ ½π₀ everywhere (no-regret up to log 2)"; (C) "null-inflation if σ̂² is too
  small (§4.4); unbounded downside without a floor".
- **Needs new runs**: (A) "no (post hoc)"; (B) "yes (start changes)"; (C) "yes (start changes)".
- **Helps evidence / PIPs in masked regime**: (A) "no"; (B) "yes (the bridge starts near S₀; weight stability ×2 at worst, Prop B1(f))"; (C) "yes for dilution
  (π₀^C ≈ π under BO)".
- §5 LS0 weakness: "LS0 does not fix the *start*. Evidence and PIP accuracy in the masked regime are not improved … It also needs a lattice progress condition
  (M2), which is family-specific."

**Recommendation (verbatim):** "1. **Keep LS0 as the main theorem's route.** It is approved, post hoc, and touches nothing locked. 2. **If one start change is made,
choose (B-merge).** Of the candidates on the table, it is the only one that yields T38(b) on LH *without* LS0, and it does so through route (a), which needs no
lattice condition. Its downside is bounded by log 2. It does not need the 2,400 fits re-validated *for correctness*, because every identity transfers, but under the
investment rule it does need a pilot for performance. 3. **Treat (C) as a separate, study-motivated change**, for dilution at n = 200, not as a theorem enabler.
If it is pursued, use a floored plug-in and pair it with a pilot." Plus: "A combined "(B) + (C)" redeploy is coherent … the only option that addresses both
mechanisms, but its T27/EXP′ re-derivation cost is the sum of both."

Pilot evidence (§6, **exact small-p synthetic**, not study data; `scripts/mixnum.py`, imports W1-EXP's `bvs_exact.py`/`family.py`): families LH-A (p = 16,
c = 1, ρ = 0.7, ψ = 0.5), LH-B (p = 20, c = 2), BO-D (p = 16, truths 1.5, 1.5, 0.32). Medians log₁₀π₀(S₀):
- LH-A n = 200: base −2.18, 𝒫⁺ −0.09, **(B) mix −0.38**, C-fix −2.16, π(S₀) 0.78; n = 800 / 3200: (B) −0.33 / −0.32; base −2.45 / −2.73.
- LH-B (c = 2) n = 200/800/3200: base −4.33/−4.92/−5.53, (B) −0.44/−0.34/−0.32, C-fix −4.22/−4.84/−5.48.
- BO-D n = 200: base −1.51, (B) −1.51, **C-fix −0.27**, C-grid −0.74, π(S₀) 0.53, S₀ ⊆ C-fix mode 0.92; n = 3200 base −0.02 ("dilution masking is a finite-n
  phenomenon").
- "Thm C1's bound held in 100% of BO-D replicates. On LH, which is not BO, it held in only 42% at n = 200." "Not run (time box): LH-iid and the hub-move variant."
What fails (§7): random partitions; per-edge mixtures for c ≥ 2; (C) on LH; (B) on dilution; (C) null plug-in; "(C) asymptotically on BO with fixed β … (C)'s
advantage lives exactly where the locked posterior theorem is silent. This is the main reason (C) cannot carry T38(b)."
Needs escalation (§9): Thm 6 reuse at block size 2g; verbatim transfer of T09/T12 to non-product γ₀ against full proofs (`PROOF_v3.tex`, `PROOF_v6.tex`);
Prop C3/§4.4 remainders; C-fix convergence conjecture.
Outside scope (§10): "Whether the 2,400 fits' masking is cancellation or dilution decides which fix matters at n = 200. W3-VEXP Prop D says dilution, and that
would favour (C) for *performance*, even though (B) is what the theorem needs."
Confidence card: (B) validity "high | done (PROVED)"; Thm B3 "high | done modulo the Thm 6 reuse"; (B) LH-iid "medium-high | medium"; Thm C1 "high | done
(PROVED)"; Prop C3 "high | done (PROVED)"; "(C) ⇒ T38(b) | false on LH; on BO only in a weak-signal window where T03 is silent | low"; C-fix "CONJECTURE |
medium".

## 6. F-SIGMA — theory of the common-σ̂² start (e2a3481)

Starts from O-MIX §4. Variant: tables r_b^C only, "Everything else (target, partition, moves, calibration, final run, local search, decision rule) is unchanged."

| Label | Statement | Hypotheses | Status (verbatim) |
|---|---|---|---|
| Lemma S0 (variant invariance) | T09, T11(iii), T12, T13, T21, T22(i)(ii)(iv), T31(i) verbatim; σ̂² must be 𝓒-measurable (streams 0–9 at most) ("A σ̂² that depends on final-run states breaks T12"); **HPM ingestion must record log m(U)** (r_b^C(U) is not m(U)); table-specific results (EXP′, T22(iii), T27(i) H2, W1-EXP Thms 2–6, F-DRAFT W1/W2/W5/W/W′) must be re-derived | σ̂² from (X, y) + streams 0–9 | "PROVED." |
| Lemma S1 | under BO: odds transfer log[π₀^C(S)/π₀^C(S′)] = log[π(S)/π(S′)] − ν[ψ(u(S)) − ψ(u(S′))]; 1 − π₀^C(S₀) ≤ e^{νψ(u₀)}(1−π(S₀))/π(S₀); W2 analogue κ_b → ε₀ = 1 − σ̃²_{S₀}/σ̂²; EXP′ becomes identity | BO | "PROVED." (checked "to 10⁻¹³ by exact enumeration") |
| Thm S2 (dichotomy) | with a := σ²/σ̂², p ≍ n^A: concentration iff a < 1 + 1/(2A); rates (i) a₊ < 1: O_P(B2^B(1−a₊)^{−1/2}n^{−1/2}); (ii) a₊ = 1: √(log p + B) n^{−1/2}; (iii) 1 < a₊ < 1+1/(2A): p^{a₊−1}L(p)n^{−1/2}; (iv) a₋ > 1+1/(2A): π₀^C(S₀) → 0 (floods) | BO, SE-blk, s₀ fixed, \|C_b\| ≤ B ≤ 16, BM-blk with plug-in | "PROVED under BO (upper bounds (i)–(iii) and lower bound (iv)); the remainders are those of W1-EXP Lemma 1.1/1.4." At study size A = 1.17, a* = 1.43 |
| Thm S3 | cancellation (CL(L)) chains: π₀^C(S₀) ≤ p^{−c}n^{−c/2}e^{O_P(1)} (= O-MIX Prop C3 exact form) | H1, CL(L), SE | "PROVED." |
| Thm S4 | T38 route (a) under common σ̂², no LS0: Q_fπ₀^C(S₀) → ∞, P(Ŝ ≠ S₀) → 0 | S2 with a₊ < 1+1/(2A), T03 hyps, BO | "**PROVED-UNDER** Theorem S2 and the locked T03, T11(iii), T21." Card: "high asymptotically; **vacuous as an improvement** over v3 in the fixed-β regime" |
| Thm S6 (random-design catastrophe) | nulls independent of μ: exponent (v_∅/σ̂²)χ²₁/2, inflation 1/(1 − R²_pop) ≈ 26 at c = 1; S2 holds with a := v_∅/σ̂²; "**No single σ̂² serves truths and nulls at once.**" | random design (iid; study S1/S3/S4/S6 generators) | "PROVED (the mechanism is exact; the extreme-value step is that of S2(iv)); exact numerics." Card: "(exact numerics: 10^{−1303})" |
| C-E1 screening plug-in | underestimate risk | — | "(PROVED by S2(iv))" |
| C-E3 S5 common factor | proxies amplified | — | "PROOF SKETCH." |
| C-E4 C-fix runaway | second fixed point at \|mode\| = K | — | "COUNTEREXAMPLE (exact numerics) + PROOF SKETCH." |

Numerics (exact, synthetic): §3 p = 12, three BO blocks, n = 200, θ = (1.5, 1.5, 0.35): identities to 5·10⁻¹³; at σ̂² = σ̃²_{S₀}: π₀^C(S₀) = 0.737/0.805/0.815 vs
π(S₀) 0.733/0.804/0.815, v3 0.089/0.336/0.049. §8 study-size cells (2 replicates each, "medians are not meaningful"): **BO196** (exact BO, p = 196) and **IID500**
((n, p, s₀) = (200, 500, 14), study β pattern). Headline: IID500 c = 1 oracle σ̂² = σ²: −1302.69 / −1541.75 (mode size 100 = K) vs v3 −12.35 / −10.54; c = 0.5 oracle
−302.45 / −169.16 vs v3 −13.50 / −18.60; C-fix runs to |S_fix| = 100 in all four IID500 replicates; BO196 c = 1: v3 −7.47/−7.55 → σ̃²_{S₀} −0.52/−0.69 (IS π(S₀) −0.55/−0.74);
0.7σ² (a = 1.43) costs 0.4–2 decades → "the safe margin at the study's size is a ≲ 1.2, not a*". Finite-n quantification at study size: 7 of 14 truths
(|θ| ≤ 1.2) dilution-masked in v3, ≈ 21 nats ≈ 10^{−9}; cost per variable 6.83 nats.
**Recommendation (verbatim):** "The variant should **not** be deployed as specified. The mechanism identified here points to *residualised* tables (each block
scored against y minus the other blocks' fitted signal) as the fix that keeps the protection; that is a different method change (Outside scope, §9)." §12.7: "do
not deploy "common σ̂², everything else unchanged"; the dilution is the right null scale in non-orthogonal designs. Residualised tables (y minus other blocks'
fit) are the candidate that keeps the protection (outside scope). Pilot Step 0 (free, post hoc from saved tables) decides before any SMC run."
What it buys theoretically: T38 route (a) without LS0 under BO (Thm S4) — but "S4's asymptotic content coincides with T38(a) under v3"; not a cancellation fix (S3).
Cost: tables-only; HPM ingestion of log m(U) "costs one logarithm per entry"; residualised Step 2 "≈ 3 s per fit at p = 1,000, B = 14; no SMC runs".
Pilot design (§10): Step 0 free post-hoc recomputation from saved tables of the 2,400 fits for σ̂² ∈ {σ̃²_{S̃₀}, C-fix, s_y²} ("If Step 0 shows flooding, stop");
Step 1 only if Step 0 passes ("it should not"): S4 at (200, 500), c ∈ {1, 0.5}, 20 paired datasets, pass = median π₀^C(S₀) > 0.1 and HPM rate within 2 datasets,
plus S5 stress; Step 2 residualised tables recomputation.
Needs escalation (§9): heavy-tailed-sum step of S2(iii); O(1/n) remainders of S1(d)/(e); law of (u_lᵀμ)² for the actual S3/S4/S6 generators.

## 7. F-MASKPIP — what Ẑ and the PIPs mean in the masked regime (dbe45fa)

Notation: W_r := Ẑ_r/Z; f_{r,s} fraction off S₀ at terminal position τ_s; B̄_r (T23(ii)); err_r := max_j|PIP̂_rj − 1{j∈S₀}|; δ₁ = 1 − π(S₀); u_π = δ₁/π(S₀);
ρ̄ = one-round departure probability from S₀ ("W2-T26 Lemma 2 (candidate …) gives ρ̄ ≤ (B+3)u_π"); masked regime = π₀(S₀) → 0 while δ₁ → 0.

| Label | Statement | Inputs | Status (verbatim) |
|---|---|---|---|
| Prop M1 | (a) E_𝓒[W_r f_{r,s}] = δ₁, E_𝓒 W_r = 1; (b) E_𝓒[W_r B̄_r] ≤ δ₁ + ρ̄; (c) **E_𝓒[W_r err_r] ≤ δ₁ + ρ̄ + u_π** — "every regime, every frozen grid", "no premise on π₀(S₀), no bound on T, no condition on N" | locked T12(i.b), T23(ii-a,b); W2-T26 Lemma 3 (candidate); T12 (R3) | "PROVED." |
| Cor M2 | (a) P(f > ½ ∧ W_r ≥ c) ≤ 2δ₁/c (c = √δ₁: ≤ 2√δ₁); (b) P(err_r > ε ∧ W_r ≥ c) ≤ (δ₁+ρ̄+u_π)/(cε), MPM analogue; (c) secondary PIP; (d) primary PIP with min_r W_r; (e) E[W_r 1{f>½}] ≤ 2δ₁ | M1 + Markov | "PROVED." |
| Prop M3 | E_𝓒[W_r \| C] ≥ (1 − 2δ₁)/κ; abstract instance with P(W_r < c \| C) = 1 — "no first-moment "restart T26" for Ẑ" | M2-e | "PROVED." |
| Thm R (PIP restart, no evidence input) | E_𝓒 err_r ≤ δ_𝔛 + β_H + (L+4)ρ̄ + u_π; P(MPM̂ ≠ S₀) ≤ 2[…] | repair basin 𝔛, H rounds | "PROVED as a composition." |
| Cor R′ | PIP and MPM consistency in the masked regime under DELIV-POP, REP-ENT, (P), (P-ex) | DELIV-POP **OPEN**; REP from W1-T24G Thm B (candidate) | "PROVED as a composition, CONDITIONAL on its inputs." |
| Prop N-a | non-crossing w.p. ≥ κ ⇒ P(f > ½ ∧ W_r < √δ₁) ≥ κ − 2√δ₁: underestimation by ≥ δ₁^{−1/2} (≥ (n/log n)^{1/4} under T03); T31(i) stays valid but uninformative | M2-a | "PROVED (general)." |
| Prop N-b | W_r ≈ π(M)/π₀(M) on non-crossing | — | "PROOF SKETCH." |
| Prop N-c | LH-type omission masking, one-stage grid T = 1: W_r ≤ e^{−Θ(n)} w.p. → 1 while PIPs consistent | W1-EXP Thm 6, O-BGIBBS Prop LH, W4-SHARE Prop M(b) (candidates) | "PROOF SKETCH (deterministic core PROVED; family-level claims rest on candidates)." Caveat: "Whether the method's calibration produces T = 1 on such data is OPEN" |
| Prop W4 / split | Ẑ is an L²/χ² object; PIPs an L¹/occupancy object; 1 + χ²(π‖π₀) ≥ π(S₀)²/π₀(S₀) ≈ 10¹² at study scale | F-DRAFT W0/W4 | "interpretation; no new claim" |

**Meaning in the masked regime (verbatim):** "So in the masked regime **the reported PIPs can be wrong only on islands whose evidence is a gross underestimate**,
never the other way round." / "wrong PIPs and accurate evidence cannot coexist, while accurate PIPs with collapsed evidence can and do."
Paper at n = 200 (§7) — **can claim**: (1) E_𝓒 Ẑ = Z, E log Ẑ ≤ log Z, 0.05Ẑ is a 95% lower bound ("in the masked regime the bound is valid and expected to be loose by a
factor that can be astronomically large … the paper should say so"); (2) pathwise PIP bound err ≤ fraction of measured paths leaving S₀ + u_π (T23(ii)); (3) M1–M2
coupling; (4) Theorem R / R′ under delivery + repair + T03. **Cannot claim**: (1) "Ẑ/Z → 1, or any relative accuracy of Ẑ, in the masked regime"; "four islands that
all fail to cross agree with each other"; (2) "PIP accuracy from the evidence identity"; (3) "Any finite-n rate at n = 200. With median π₀(𝓡₂) ≈ 0.8, Theorem R's
bound is ≥ 0.2 before the repair and departure terms; it explains the mechanism, not the study's numbers."
Numerics (§4.1; helper "Opus 5.5 helper"; exact scores at **p = 18** synthetic, B = 4, s₀ = 3; designs `masked` (corr 0.6, β₃ = −0.6) and `masked8` (corr 0.8);
n ∈ {640, 5120}; N ∈ {2500 (20 reps), 50 (40 reps)}; grids G1 one-stage, G2 ideal full-space ESS, G3 blind restricted-ESS; "24 settings, 3,840 island-runs"):
(I2) max err_r − (B̄_r + u_π) = −0.047 (never positive); (I3) M1-c held in all 24 settings (closest 0.069 vs 0.372); (I1)/M2-a **not tested** ("no island ever had
f_r > ½ (max 0.44)"). G1: median log W_r −4.32 (n = 640) to −11.7 (n = 5120, N = 50), PIP error = exact posterior's (e.g. 0.0067), MPM 100%; G3 at n = 5120: −5.13
to −10.8; G2: |median log W_r| < 0.03. "in collapsed settings the top 5% of islands hold 99–100% of ΣW_r"; masked8 n = 5120 N = 50 mean W_r = 2·10⁻⁵.
Cited (not produced): W4-SHARE PB design "delivery 200/200 islands, median log Ẑ/Z = −67"; W2-T26 masked design |Ẑ/Z − 1| ≈ 1.4–2.1% with ideal grid.
What fails (§5): evidence restart conditioned on crossing; T15 for late delivery (vacuous); removing (L+4)ρ̄ ("at n = 200 it is the dominant term … (L+4)ρ* ≈ 10–13");
T = 1 family as the method's own.
Needs escalation (§6): M1(b) conditional step; ρ̄ ≤ (B+3)u_π (W2-T26 Lemma 2, candidate); entrance vs scored in Thm R; **DELIV-POP** "the one genuinely open input …
strictly stronger than T38's DELIV"; N-c family claims rest on candidates.
Outside scope (§8): free self-diagnostic "fraction of measured (particle, round) paths that leave the reported MPM̂ (or Ŝ)" — "Method change: reporting only"; secondary
PIP coupling cleanest (FROZEN_LIST drops it); exact ρ̄ form makes (L+4)ρ̄ "4–8× smaller".
Confidence cards: M1, M2, M3, N-a "high | PROVED here"; Theorem R/R′ "high (bound); medium (inputs hold on LH-type families) | … DELIV-POP OPEN"; N-c "medium-high for a
frozen grid; low-medium that the method's calibration realises T = 1". No method change (optional diagnostic). No mention of LS0 or common σ².

## 8. S-ELS — E_LS ledger extraction (PROD-H, 2,400 fits) (90423b1)

Data: "PROD-H run `20261030T0934Z_prodH` (records pulled and manifest-verified). H2 showed that these 2,400 records reproduce the 2026-10-23 fits exactly (max |diff| = 0
on 11 fields)". **This is the actual 2,400 production fits (per-fit `SMCBVS.rds`)**, extracted on the laptop (`extract_ledger.R`, 3 workers, ~28 min). F(S₀) from H2's
`F_truth` (not recomputed from X), validated against the fit's own top store.

Plain answer (verbatim): "**On the PROD-H ledgers there is no fit with F(S₀) > F(S_c), and no fit in which the local search did anything.**"
- "In **all 2,394 completed fits the final local search made 0 moves**: E3 never fired, the HPM never changed, and every search ended `no_improvement`,
  `local_certified = TRUE`, `local_limit = FALSE`."
- "**S₀ was scored by the fit in all 2,394 completed fits**: it is in the 20,001-model top store … The event E_LS … is **empty in the data (0 of 2,394)**."
- "For **all 565 posterior misses, F(S₀) < F(Ŝ) strictly**. The smallest margin is 0.0049 (23 fits are within 0.1). There are **0 search misses**, **0 ties**".
- 541 fits with S_c ∈ 𝓡₂∖{S₀}: "F(S₀) < F(S_c), median gap −1.33, range −9.05 to −0.0049" — "the "0/541 repaired" count **is forced by monotonicity (Lemma 0), in
  every one of the 541 cases**. W3-VT37R's repair R2 (CEX-2) is a valid logical correction, but its counterexample pattern does not occur in these data".
- "**The referee's sampled F(S₀) > F(S_c) cannot be reproduced from these ledgers.** … HQ should ask for the case IDs."
- "The production search is, empirically, a **pure certificate** that Ŝ is a 1-flip/swap local maximum (2,394/2,394)."

Classification (§3): p500 c0.5 370 exact / 230 posterior / 0 search / 0 stopped; p500 c1 559/40/0/1; p1000 c0.5 340/258/0/2; p1000 c1 560/37/0/3; **all 1,829 / 565 / 0 /
6**. 6 stopped (`resource_limit`, all S5): partial HPM F(Ŝ) ≥ F(S₀) in all (3 equal S₀; 3 below by 0.21, 3.39, 1.15). E1 0, E2 83 (10 among posterior misses), E3 0,
local_limit 0, one scan per fit. ℓ = 10 at both p.
541 breakdown (§4): 218 / 40 / 246 / 37 by cell; S₀ ∈ N(S_c) in 434 (267 single add/delete + 167 swaps); max moves to S₀ 4; by |S_cΔS₀| = 1..6: 267, 197, 39, 32, 4, 2;
regions: 133 in 𝓡₀∖{S₀} (all c = 0.5), 346 in 𝓡₁∖𝓡₀, 62 in 𝓡₂∖𝓡₁; 24 further misses outside 𝓡₂. Reason table: A (Lemma 0 forbids) 541; B (CEX-2) 0; C1/C2/C3 0/0/0.
Same-size strict posterior misses at c = 0.5 (§5): pooled 201 of 488 (161 single swaps, 30 two-swap, 6 three-swap, 4 four-swap); S4 101, S6 46, S3 25, S5 23, S1 4, S2 2;
size offsets −3..+2: 5, 21, 142, 201, 106, 13; at c = 1 only 6 (all S4).
Checks (`tables_checks.txt`, all PASS): S0 equals H2; F_smc_hpm = ledger F̂ (max diff 1.99e−12); S_c = hpm_before_local; F̂ ≥ F_c; S_hat = S_ret (0 differ); E3 never;
moves > 0 never; F_truth = top-store F(S₀) n = 2394 max diff 1.02e−12; = F̂ on 1,829 exact recoveries.
Limits (§7): F(S₀) not recomputed from X; final local search only (pilot/calibration searches not read); referee's sample unseen; 6 stopped not classified; PROD-H
design only ("says nothing about weaker regimes"). Relevance: answers S-PAPER disclosure item 5's "unextracted (OPEN)" E_LS question and O-CERT's C5 screening term
empirically for these fits (S₀ always scored). Supplies per-fit data that O-SWAP lacked ("Per-dataset SMC outputs are not on the laptop").

## 9. S-PAPER — theory-section LaTeX skeleton (556be30)

README: "**Nothing here is reviewed or adopted.** Every statement is a candidate. The status words are the campaign's and are never upgraded. No proofs are included".
Every statement is preceded by `% STATUS: <author status>; VERIFIED-BY: <branches>; SOURCE: <branch:file:label>` (grep: 57 lines containing "STATUS:", 2 of them the
header template). Status word tallies (leading token): PROVED 25, PROVED-LOCKED 3, PROVED-UNDER 2, IMPL 5, IDEAL 2, COUNTEREXAMPLE 1, plus definitions/
wording-constraint/empirical/disclosure lines. Built from F-REFINE CARDS/ARCHITECTURE (db708ca), W4-T38FULL, W2-BOOK, W2-T26, W1-T03R, W2-VT03R, W1-EXP, W1-T37R,
W3-VT37R, W3-PGD, W1-T24G, A-REV1, A-REV2 etc.; cut from theory/campaign @ b8811e2. **Does not use O-CERT, O-SWAP, O-DILUTE, O-MIX, F-SIGMA, F-MASKPIP, S-ELS, L-LEAN**
(all postdate it; head 13:04).
Structure: §Setting (defs incl. **Definition LS0** "the final local search from both the best-scored model and the start mode" — STATUS "IMPL (code reading) + method change
under the investment rule (pilot data pending)"); §Standing assumptions (EX-A, EX-S IDEAL; CAL; SR "IMPL (code reading); VERIFIED-BY: HQ read of v3_engine.h step_gibbs …
HQ's own read, not an independent audit"; GUARD "IMPL … VERIFIED-BY: none"); §Story; §Results: Thm 1 (T03♯) "PROVED (candidate)" VERIFIED-BY W2-VT03R, A-REV2; Prop 1
(T07) "PROVED-LOCKED"; Thm 2 (T22, EXP′ "PROVED", favourable (F1) "PROVED-LOCKED CONDITIONAL on EXP′ (now discharged)…", masked, LH); Thm 3 (Lemma literal TD "PROVED
(negative result)", Theorem A "PROVED", Lemma LS-score "PROVED; VERIFIED-BY: same-family referee inside W4-T38FULL", Lemma 0 restricted ("posterior-miss inference of the
source's Lemma 0(b) is an ERROR (A-REV2) and is NOT stated"), Theorem W "PROVED (candidate); VERIFIED-BY: none final", Thm B′ "PROVED (finite inequality, after the Lemma F′
repair); Proposition U … is an ERROR as written and is NOT cited"); Thm 4 (T21) "PROVED (composition …)"; Thm 5 (T38, main) "PROVED for (0), (a), (b1), (b1-LH)
(candidates); (b1-LH-iid) PROVED by one unverified run; (c) conditional on T32(i) = CONJECTURE"; routes (b1′)/(b2) in a Remark "not part of the theorem" ("T38(b)-R,
entire supplied statement: GAP" per A-REV1); Thm 6 (T26) "PROVED (composition …); VERIFIED-BY: none final"; Prop 2 (T12/T31(i)) "PROVED-LOCKED … + W2-BOOK restatement PROVED".
Thm 5 "Not claimed: … masked-regime consistency *without* LS0 on any explicit family (OPEN)".
**n = 200 disclosure section** ("What the theory does and does not say at n = 200"): "The theorems are statements about mechanism and about n → ∞; they are not statements
about the reported numbers at the study's size". Items (does not say): 1 "The start at n = 200 is dilution-masked, not cancellation-masked" (start mode misses 6–12 of 14,
disappears only for n ≈ 800–1600; "LH's cancellation cannot survive the study's partition"); 2 "Every completed wrong HPM is a posterior miss" (565 of 2,394; 6 resource stops,
all S5, counted as misses); 3 T03 thresholds n ≈ 2.1×10⁶–2.5×10⁶ ("earlier figure 1.2×10⁵ is an ERROR"), beta-min constant ≥ 43× executed signal; 4 start rates vacuous
(2^B√(log n/n) = 2.7×10³ at n = 200); 5 "The HPM at this size is found by Gibbs flips, a route with no completed theorem" — "whether the study's 541 final centres lay in E_LS
is unextracted (OPEN)" [now answered by S-ELS: 0 of 2,394]; 6 "LS0 does not change the picture at n = 200" — "post hoc on regenerated study data LS0 scored S₀ in 113/128
fits with |S̃₀ΔS₀| ≤ ℓ+1 and 13/32 beyond … The approval of LS0 is conditional on the O-LS0 data check … whose result was not available at drafting. LS0 buys the one
masked-regime consistency statement whose premises are all proved on an explicit family (Theorem T38(b1-LH)); it buys nothing for route (b2) or for evidence/PIP claims in
the masked regime." (STATUS "empirical (post hoc, W3-PXN) + OPEN (O-LS0 data check pending)"); 7 T26 silent at n = 200 (Δ_n ≈ 1); 8 statements the paper must not make
(i)–(xii), incl. (x) "the word "VERIFIED" as if it meant reviewed: all verification by the campaign is same-family (Claude checking Claude) except the two cross-family
reviews A-REV1 and A-REV2", (xii) ""no method change needed": true for everything except Theorem T38(b1), which is the headline and rests on LS0"; 9 implementation facts
(SR, GUARD, scan-before-limit, IND-T, LS0 emit_centre) "None has had an independent audit confirmed on these branches."
Pending edits (README): replace T38 with W6-FIXREV1's statement; Thm 3(iv) Prop U changes; W6-FIXREV2 STATEMENTS (tie-aware TD′, 0.51/c_*, Lemma U); re-check Lemma 0.
Judgement calls flagged: Thm 5 scope; Ŝ⁺ notation; LS0 approval conditional; F-REFINE internal conflict (ARCH §7(iv) "≥ 10³ at B = 14 for n ≤ 10⁴" vs CARDS 2.7·10³ /
497 / 61); EXP′ constant 0.52 vs 0.51; **Prop 2(f)**: W2-BOOK PROOF.md "α e^η P(𝒜) + ε" vs STATEMENTS.tex "α e^η + ε" (weaker used).
Compile: README "`theory_section.tex` compiles (two passes, via `owls_run -j 1`) with no errors and no undefined references; `theory_section.pdf` is committed." vs
`compile_status.txt`: "Output: theory_section.pdf (not committed; the .aux/.log/.pdf are untracked build files)." — **internal inconsistency** (the PDF IS on the branch,
524,258 bytes).
No mention of common σ², dilution fix, certificates, O-SWAP predictions (all predate integration).

## 10. L-LEAN — Lean 4 formalisation (42f9de0)

No REPORT.md on the branch. Files: ASSUMPTIONS.md, AXIOMS_RECORD.txt, FAILED_ATTEMPTS.md, MATHLIB_NOTES.md, T12_PLAN.md, build.sh, SmcBvs/ Lake package (Lean
v4.35.0-rc2, Mathlib rev 065356127b1d, shared `packagesDir = "C:/lean/packages/v4.35.0-rc2"`, autoImplicit = false), frozen/v1/ statement snapshots, fidelity/ (PROMPT,
packet, ASTRA_raw.md, ASTRA_stderr.txt). Commits: 1ea6ccc skeleton → 7823b4e "T21 (C1), T11(iii), T37 greedy core (A1-A4), T12(i.a) deterministic core: sorry-free, lake
build green" → bece139 T07 → f34bf6c "T37 lattice (Lemma 2(a), concrete A2/A3) proved by helper H1; integrated, stmtdiff OK" → 42f9de0 "T07 complete (H2 psi lemmas merged);
full package sorry-free; axioms record". Interpretation of LEDGER's "Theorem A" = **T37 Theorem A** (A1–A4), not W2-T26's Theorem A.

**Formalised theorems (names from the .lean files; main ones listed in Axioms.lean):**
- Basic.lean (10 thms): post, IsArgmax, IsLeastArgmax(.unique), exists_isLeastArgmax, IsArgmax.eq_of_strict, post_of_mem, post_of_not_mem, sum_exp_pos, post_nonneg,
  post_sum, post_le_one, strict_max_of_post_gt_half.
- T21HPM.lean (8): `hpm_eq_truth`, `t21_event_subset`, `t21_decomposition`, `t21_decomposition'`, `markov_half`, `measurable_post`, **`t21_C1`** (P(U ∨ Ŝ≠S₀) ≤ P(U) +
  2∫(1 − π(S₀)) + P(Uᶜ, S₀∉𝒮); hyps: measurable F, 𝒮 ⊆ A on Uᶜ, IsArgmax on Uᶜ), `integral_le_eps_add_prob`.
- T07Bayes.lean (28): `ceiling`, `no_size_prior_repairs`, `ceiling_sharp`, `risk01_eq`, `risk01_min_iff`, `hpm_min_risk01`, `riskH_eq`, `psi_Jplus_le`,
  `psi_Jplus_unique_iff`, `mpm_min_riskH`, `mpm_unique_iff`, `psi_capped_le`, `exists_capped`, `capped_mpm_min_riskH`, `reported_eq_hpm_iff`, `reported_min_risk01_iff`,
  `reported_truth_needs_unscored`, `excess_riskH_le`, `mpm_hat_eq_iff` + helpers (normW_pos, Ωf lemmas, mem_Jplus, psi_split, …).
- T11Miss.lean (4): `t11_pow_le_exp`, `t11_miss_pi`, `t11_miss_pi_real`, `t11_miss_iid`.
- T37Greedy.lean (15): `exists_bestImprovement`, `path_F_le/mono/strictMono`, `path_mem_of_TDinf`, **`theoremA1`**, **`theoremA1_converse`**, **`theoremA2`**,
  **`theoremA3`**, `pd_of_reach` (A4-PD), plus path lemmas.
- T37Lattice.lean (19): `progress_mem_Lat`, **`lemma2a`**, `TDP_of_TDP'`, **`theoremA2_lattice`**, **`theoremA3_lattice`**, `Φ_le_of_mem_Rad`, Φ insert/erase lemmas,
  Lat/Rad membership.
- T12Core.lean (3): `invariance_step`, `resample_move_step`, `unbiased_of_step` — header "**Status: partial.** … **Not formalised (TODO, see `T12_PLAN.md`)**: the
  derivation of the recursion hypothesis `hstep` from a probabilistic model of the island … it enters `unbiased_of_step` as an explicit hypothesis, never as an axiom."

**sorry/axiom counts (grep -w):** current SmcBvs files: `sorry` 0 occurrences in every file except T12Core.lean, where the single hit is the docstring word
("formalises, sorry-free") — **0 actual sorry**; `axiom` declarations 0 in all files (only hit: T12Core docstring "never as an axiom"); `admit` 0. Axioms.lean contains only
`#print axioms` lines (46). AXIOMS_RECORD.txt: all 46 main declarations "depends on axioms: [propext, Classical.choice, Quot.sound]" — no `sorryAx`. Frozen v1 statement
snapshots (not built): T07Bayes 12 sorry, T37Lattice 8 sorry, others 0 (expected: frozen statements with sorry proofs, used for stmtdiff).
Note the build itself was not rerun here; "sorry-free" rests on the commit message, the AXIOMS_RECORD and grep.

**ASSUMPTIONS.md (assumed/abstracted):** A-P1 location in `theory_campaign/L-LEAN/`; A-P2 shared Mathlib, nothing downloaded; A-P3 "no 5-agent Sol review round … the lead's
review, `stmtdiff`-style freezing and `#print axioms` stand in for it. Fable and Astra are used for the fidelity check (the protocol's main risk control)". T21: A-T21-1
abstract probability space, E₀δ₁ written ∫δ₁dP ("The Lean statement allows F to depend on all of ω, so it is more general"); A-T21-2 tie rule as IsArgmax ("C1 never uses
the tie rule"); A-T21-3 model space arbitrary Finset, "The regression score formula is not used by C1, so F is an arbitrary real score"; A-T21-4 measurability of ω ↦ F ω S;
A-T21-5 "**Routes (a)–(f) and the asymptotic H03 consequences** are not formalised". T07: A-T07-1 tie order = injective rank; A-T07-2 F arbitrary, (iii)(b) F = log(pw·m);
A-T07-3 action class any finite set. T11: A-T11-1 "A regular-conditional-probability version is not formalised" (identity for fixed Q, S*, π₀ applied pointwise in 𝓒).
T37: A-T37-1 abstract core, closure of R under greedy move a hypothesis (concrete R_{a,d} via Lemma 2(a)); A-T37-2 production search modelled as `path M S_c ℓ`. (No
ASSUMPTIONS entry for T12; its gap is documented in T12Core header/T12_PLAN.)
**Fidelity review:** `fidelity/ASTRA_raw.md` is **empty (0 bytes)**; `fidelity/ASTRA_stderr.txt` = "Reading additional input from stdin..." only. So the Astra
(cross-family) fidelity check produced no output — **fidelity review not done**; no Fable fidelity output on the branch either. PROMPT asks GREEN/RED per theorem and
`OVERALL:`; packet contains SOURCES.md, ASSUMPTIONS.md and lean/*.lean. PROMPT says "Proof bodies may contain `sorry` (still in progress)" (written before completion).
**FAILED_ATTEMPTS.md:** "(none yet)".
**T12 plan:** (i.a) E_c[Ẑ_t q̂_t(f)] = Z_t q_t(f) partially formalised (3 lemmas, no sorry); TODO derive `hstep` via PMF on histories, product law of iid ancestor+kernel draws
("Mathlib has no `PMF.pi`"), stage-0, round-kernel invariance; "Estimated effort: one focused session. The main cost is the product-law plumbing in step 2" (300–600 lines).
MATHLIB_NOTES: targeted imports (full import >30 min), deprecations (`push Not`, `Set.mem_ofPred_eq`, `Mathlib.Basic.Real.Basic`).
build.sh: `lake build` → filters log, prints `EXIT rc`.

---

## 11. Cross-branch: candidate method fixes (what each buys, cost, risk, evidence, recommendation)

| Fix | Theorem it makes provable | Cost | Risk | Pilot evidence | Recommendation (source, verbatim) |
|---|---|---|---|---|---|
| (A) LS0 | T38(b1) on LH exact Gram, PROVED-UNDER (W4-T38FULL; O-MIX table); S-PAPER Thm 5 rests on it | (ℓ+1)max_k[p + k(p−k)] ≈ 1.7·10⁵ scores at p = 1,000, ~1–3 s (O-MIX §5); post hoc | "none" to locked results; doesn't fix start/evidence/PIPs; needs (M2) family-specific; at n = 200 start mode 8–14 moves away, ℓ = 10–11 borderline (O-DILUTE, S-PAPER item 6) | W3-PXN post hoc: scored S₀ 113/128 within ℓ+1, 13/32 beyond (S-PAPER); **O-LS0 data check: no results** | O-MIX: "**Keep LS0 as the main theorem's route.**"; SR_AUDIT: APPROVED conditional on O-LS0 |
| (B-merge) mixture of block starts | T38(b) on LH **without LS0**, route (a), Thm B3 PROVED-UNDER; LH-iid PROOF SKETCH; does nothing for dilution | ≤ \|E\|·2^{2B} table scores (cap 16) + O(1)/score; < 5% SMC scoring; S5 degenerates | T22(ii-a) → sandwich; no-regret ≥ ½π₀ | exact p = 16/20: 10^{−0.32…−0.44} vs base 10^{−2.2…−5.5}; BO-D unchanged | O-MIX: "**If one start change is made, choose (B-merge).**" (needs performance pilot) |
| (C) common plug-in σ² tables | dilution cure **only under in-sample BO** (O-MIX Thm C1, F-SIGMA Lemma S1, Thm S4 route (a) w/o LS0 under BO — "vacuous as an improvement"); not cancellation (Prop C3 / Thm S3) | ≈ 0 extra scores; HPM must ingest log m(U) | null inflation/flooding; re-derive T22(iii), T27, EXP′, W1-EXP 3–6 | BO-D −0.27 vs −1.51 (O-MIX); BO196 −0.5 vs −7.5 (F-SIGMA); **study-like designs: oracle −690 median /480 (O-DILUTE), −1303 IID500 (F-SIGMA), π₀(R₂) → 0** | O-MIX: "Treat (C) as a separate, study-motivated change … floored plug-in … pilot"; O-DILUTE: "Do not adopt it."; F-SIGMA: "should **not** be deployed as specified" |
| (C-grid) | Prop C2 cost log m under BO | ×m ≈ ½√n log n tables | as (C) | BO-D −0.74 | not recommended separately |
| Backfit / residualised tables | none proved; validity via F-DRAFT Prop P(i)/Lemma S0; T22(iii) restatement needed | (sweeps+1)× table work (O-DILUTE); ≈ 3 s/fit recomputation (F-SIGMA Step 2) | S5 and S4 c = 0.5 weak; stability of pilot fit | O-DILUTE pilot 480 fits: median 10^{−1.0}, 378/480 favourable, π₀(R₂) 0.71, π₀(Ham≤2) 0.60 | O-DILUTE: "candidate method change … needs HQ's and Felipe's call and a pilot of the full sampler"; F-SIGMA: "the fix that keeps the protection … (outside scope)" |
| (B)+(C) combined | both mechanisms | sum of re-derivations | — | none | O-MIX: "coherent … only option that addresses both mechanisms" |
| F-MASKPIP diagnostic | — (reporting) | free | — | — | "reporting only; not pursued" |
| O-CERT card / box scan | C6 card post hoc; C4(c) in-engine = method change | ~7k + 16k scores post hoc; tree ~2^{#ambiguous} (unmeasured) | — | none committed | O-CERT §7: in-engine box scan "falls under the investment rule" |

## 12. Disagreements and inconsistencies noticed

1. **Common σ² at n = 200: O-MIX vs O-DILUTE + F-SIGMA.** O-MIX §1/§10: (C) "is the right tool for the n = 200 *dilution* masking" and "W3-VEXP Prop D says dilution,
   and that would favour (C) for *performance*" (evidence only on exact-BO synthetic BO-D). O-DILUTE (Lemma L, Prop S, 480 regenerated fits) and F-SIGMA (Thm S6, IID500)
   show the opposite in study-like random designs: in-sample BO fails, nulls inflated by v/σ̂² ≈ 7–26, oracle start floods to K, π₀(R₂) → 0. O-MIX did flag §4.4 null
   inflation ("unbounded downside without a floor"), but O-DILUTE/F-SIGMA show even the oracle σ² fails, so a floor at σ² does not save it (F-SIGMA: only σ̂² ≈ v_∅,
   which reproduces v3's dilution, avoids flooding). O-DILUTE and F-SIGMA independently converge on backfit/residualised tables.
2. **Stopped fits count:** O-SWAP "The 4 no-output fits are excluded" vs S-ELS 6 stopped (`resource_limit`, all S5: 1 at p500 c1, 2 at p1000 c0.5, 3 at p1000 c1);
   THEORY_PRIORITIES and S-PAPER also say 6. O-SWAP's observed p1000 c0.5 total 259 vs S-ELS 258 posterior misses (O-SWAP rescales cells to 100).
3. **O-CERT internal:** headline promises a p = 500 illustration on 4 datasets; §4 empty, no results/ (O-VCERT: MISSING). REPORT C1(b) "unscored" wording disagrees with
   its own `cert_run.R` (O-VCERT §2.1).
4. **O-VCERT S2 vs O-CERT** on "cannot certify confidence without PW2 or enumeration": O-VCERT says overstated; any certified upper bound on Z (UB, Δ bound) suffices.
5. **Prop 2(f) / C6 FP bound:** O-CERT C6 uses α·e^η + ε (STATEMENTS.tex form); O-VCERT R2 gives α·e^η·P(𝒜) + ε (PROOF.md form); S-PAPER notes the W2-BOOK discrepancy.
6. **S-PAPER README vs compile_status.txt** on whether the PDF is committed (it is on the branch).
7. **S-PAPER is stale vs this batch:** disclosure item 5 calls E_LS "unextracted (OPEN)" — S-ELS now: E_LS empty (0/2,394), all 541 forced by Lemma 0, 0 search misses;
   item 6 depends on O-LS0, still without results.
8. **S-ELS vs a referee claim:** "The referee's sampled F(S₀) > F(S_c) cannot be reproduced from these ledgers" (referee/case IDs unknown; W3-VT37R R2 CEX-2 pattern absent).
9. **Start-mode truth counts:** S-PAPER "start mode misses 6–12 of the 14 truths", n ≈ 800–1600 to disappear; O-DILUTE start mode holds 2.5–6 of 14 (misses 8–11.5),
   favourable at n ≈ 590–730; F-SIGMA 7 of 14 masked. Same mechanism, different numbers/sources.
10. **O-SWAP vs THEORY_PRIORITIES framing:** O-SWAP shows the observed miss rate equals the posterior one-move miss rate (24/24 cells ±1) — consistent with "0 search
    misses"; no conflict, but it makes T38's discovery term irrelevant at n = 200 for these cells ("contributes nothing").
11. **L-LEAN fidelity:** Astra fidelity output empty; ASSUMPTIONS A-P3 lists fidelity as "the protocol's main risk control", so the formalisation's statement fidelity is
    unreviewed. LEDGER's "Theorem A" was read as T37 Theorem A; T12(i.a) added as partial.
12. O-MIX and F-SIGMA cite content commits (d1cc689, 025b8d6) differing from branch heads (26b7708, e2a3481) — follow-up stamp commits, not a conflict.

## 13. What fails (collected)
- O-CERT: lower bound on π(Ŝ) from Ẑ alone (C1(c)); two-sidedness via island spread/empirical ESS; T13 as PW2 substitute; global box at p > n.
- O-SWAP: T1 independence (c = 0.5 overshoot 40–50%); T1-lo; Šidák/Royen rigorous bracket (OPEN); multi-move terms only empirically negligible.
- O-DILUTE: common plug-in σ²; F-DRAFT d(S₀) BO formula as predictor; single-variable λ_j in S3/S4; Prop S as level explanation.
- O-MIX: random partitions; per-edge mixtures for c ≥ 2; (C) on LH; (B) on dilution; (C) with null plug-in; (C) asymptotically on fixed-β BO.
- F-SIGMA: asymptotic "(C) beats v3" theorem (needs weak-signal window where T03 is silent); deployment in non-orthogonal designs (S6, C-E1–C-E5).
- F-MASKPIP: evidence restart conditioned on crossing (M3); T15 for late delivery; removing (L+4)ρ̄; T = 1 as method's own grid.

## 14. Needs escalation (collected)
- O-CERT: cross-family check of Lemma RO/GUARD output step; Lemma M(b) + engine Q identity (answered by O-VCERT: same function); SC(η_F) replay in mpfr.
- O-VCERT: GUARD code audit not done ("I did not audit"); p = 500 runs not reproduced.
- O-SWAP: Prop 1 step 2 second reader; rigorous T2 bracket; PA→probability anti-concentration; SuSiE/SSL thresholds.
- O-DILUTE: Prop D′ joint law ("candidate for a stronger prover"); Lemma L(b); Conj DM-asy; bit-exact R-engine port check.
- O-MIX: Thm 6 at block size 2g; T09/T12 full-proof transfer to non-product γ₀; Prop C3/§4.4 remainders; C-fix convergence.
- F-SIGMA: S2(iii) heavy-tail aggregation; S1(d)/(e) remainders; S6 leaked-energy law for S3/S4/S6 generators.
- F-MASKPIP: M1(b) conditional step; ρ̄ ≤ (B+3)u_π; entrance vs scored; **DELIV-POP**; N-c candidate inputs.
- S-ELS: referee case IDs for the F(S₀) > F(S_c) claim.
- S-PAPER: pending W6-FIXREV1/2 edits; LS0 condition.
- L-LEAN: fidelity check (empty); T12 `hstep` derivation.
- O-LS0: the whole data check (no results).

## 15. Outside scope (collected)
O-CERT: C4 as method-agnostic certificate for SuSiE/SSL/lasso; in-engine box scan. O-SWAP: SuSiE S5 collapse; "P(posterior miss)" as a named quantity; τ = 1 as SNR-dependent
size penalty. O-DILUTE: backfit tables; F-DRAFT Theorem W premises ("in-sample BO"); report π₀(B_d) with π₀(R_d). O-MIX: cancellation-vs-dilution question for the 2,400
fits; (B) bounds independence-sampler sup-ratio. F-SIGMA: residualised tables. F-MASKPIP: path-departure self-diagnostic; secondary PIP; exact ρ̄.

## 16. Mentions of LS0, common σ², n = 200 disclosure (index)
- **LS0:** O-MIX (option A, keep as main route; cost ≈ 1.7·10⁵ scores); F-SIGMA (Thm S4 "no LS0" under BO only); O-DILUTE §6 (ℓ = 10–11 borderline; repair must be
  addition-path); S-PAPER (Definition LS0, Thm 5 (b1) and item 6 of disclosure; approval conditional); SR_AUDIT (APPROVED conditional on O-LS0; emit centre via `eval`);
  S-ELS (indirect: production final search never moved, ℓ = 10); O-LS0 (scripts only, no results). Not mentioned: O-CERT, O-VCERT, O-SWAP, F-MASKPIP, L-LEAN.
- **Common σ²:** O-MIX (C), F-SIGMA (whole report), O-DILUTE (Lemma L, Prop S, §5). All three reject it as a T38(b) enabler; O-DILUTE and F-SIGMA reject it as a study fix too.
- **n = 200 disclosure:** S-PAPER §"What the theory does and does not say at n = 200" (9 items); F-MASKPIP §7 (can/cannot claim about Ẑ/PIPs); O-CERT C6 ("the right
  finite-n statement for n = 200"); O-SWAP (finite-n laws exact given X; T2 predictions); O-DILUTE Prop DM wording; F-SIGMA finite-n quantification §6.

## 17. Confidence cards (one-line each; see sections above for full cells)
- O-CERT: everything "high"; C2 useful only if PW2 proved; "π(Ŝ) ≥ ½ certified … not possible".
- O-VCERT: Lemma M, C3, C4 VERIFIED; C1 VERIFIED conditional on W2-BOOK; C2 VERIFIED conditional on PW2; C5 VERIFIED with caveats; C6 GAP → VERIFIED after R1, R2.
- O-SWAP: Props 1–3, 6, Thm 4, Prop 5 high/done; T2 medium-high (approximation); whole-model floor OPEN; SuSiE/SSL CONJECTURE medium.
- O-DILUTE: Thm E/R, Lemma N, Prop S high/done; dilution clause high/medium; common σ² false (reject); backfit medium (pilot only); Conj DM-asy medium/low-medium.
- O-MIX: Prop B1, Thm C1, Prop C3 high/done; Thm B3 high modulo Thm 6 reuse; (C) ⇒ T38(b) false on LH; C-fix CONJECTURE.
- F-SIGMA: S0, S1, S3, S6 high/done; S2 done modulo heavy-tail step; S4 "vacuous as an improvement"; (C) as deployed "fails … do not deploy".
- F-MASKPIP: M1–M3, N-a high/PROVED; Theorem R bound PROVED, DELIV-POP OPEN; N-c medium-high / low-medium.
- S-ELS, S-PAPER, L-LEAN: no confidence cards (data/skeleton/formalisation tasks).
