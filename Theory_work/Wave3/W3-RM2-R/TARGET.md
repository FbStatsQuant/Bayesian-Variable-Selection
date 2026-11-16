# W3-RM2-R — TARGET (CP1; one page; PROTOCOL_v4 §3.2, RIDER_RULES §2)

Statement: `STATEMENT.md` v1.0 (delta, locked). Only changed hypotheses and clauses are mapped; everything else is PARENT
`W3-RM2/ASSUMPTION_MAP.md`, `SHARPNESS.md`.

## 1. Assumption map of the changed hypotheses

| hypothesis | enters (lemma / step) | how | property used | necessity reading | signal |
|---|---|---|---|---|---|
| (T1-F♭): Theorem 1 with BM(c), c > c₀ | Q2 (Q3 part) | SOP:TH09 item 1 at its BM(c) branch | [POST] ⇒ [MODE] | HEURISTIC: the order √(log n/n) is suggested by numerics and a leading-order heuristic (W3-POST); necessity is not proved here; c₀ proof artefact [R1-sol-2] | artefact-threshold |
| (V♭): δ²_{U,j} ≥ M_V log n, M_V > M_V⁰ | Q1 Step 2(a) only | one comparison S̃ vs S̃ ∪ {j}: gain (√M_V − σ√(2A))² log n against prior + Occam (A + ½) log n, scaled by 2C_R | every truth in every start mode | order log n natural (one variable's cost); W3-RM SHARPNESS §2: masked truths show (V) not necessary for the conclusion on some designs; M_V⁰ artefact (C_R from a crude RSS bound) | artefact-threshold |
| (BM-W⁺): √λ_n ≥ 2(d_n + √(2 log n)), λ_n ≥ c_TL log n | Q2 (TL step) | exact identity (4.1) of PARENT L2: the truth's square ≥ σ²λ_n/4 beats the addition statistic (2A + 2)σ² log n and the score cost | [TL(Q)] | the additive floor at d_n² + log n is what the identity needs; c_TL⁰ artefact | artefact-threshold |
| (D) delivery premises | Q5, Q4(c⁺) | exit walk of `v3_fit` at the pin; fallback grid; resource envelopes | 𝒪 for every valid non-degenerate input | premises are idealisations (EX-A, IDEAL-W, MACH): engineering, not mathematics | — |
| 𝓜_n (replaces π(S₀) > ½) | Q4(b⁺) | only "F(S₀) > F(S), S ≠ S₀" is used | reported = scored F-max | weakest posterior input for this route: if S₀ is not the unique F-maximiser and the maximiser is scored, Ŝ⁺ ≠ S₀ (or a tie) | — |

Conclusion level: reported-model **+ delivery** (was reported-model on output). Rate: none for the reported model
(unchanged non-claim); P(Ŝ⁺ ≠ S₀) ≤ P(mode failure) + P(search failure) explicit. Scope: unchanged (fixed design /
Gaussian rows; p ≤ n^A; |Q| ≤ n^b).

## 2. Parity table (changed clauses)

| clause | (a) PROGRAM goals | (b) closest published theorem | (c) our best registered result | verdict |
|---|---|---|---|---|
| beta-min in RM2-F | design-agnostic, p ≫ n, method as coded: unchanged | Yang–Wainwright–Jordan (2016, Ann. Statist.), MCMC selection: θ²_min ≳ σ² log p/n with a constant [R1-sol-1: the Song–Liang (2015) and Narisetty–He (2014) comparisons are withdrawn — Song–Liang Thm 1–2 are Hellinger contraction results, and neither was re-verified here] | RM2-F: θ²_min n/log n → ∞ (BM-∞) and (BM-W) ratio → ∞ | **matches** YWJ's order and constant-level form; constants not sharp in either |
| visibility constant | as above | no published analogue for a search started at a block start mode; GROW/RM had M_n → ∞ | RM2-F: M_n → ∞ | **beats** our registered form; no published comparator |
| truth-removal floor at polynomial \|Q\| | as above | YWJ need θ²_min ≳ log p/n and bounded-size neighbourhoods; no lattice of size n^b | RM2-F: (BM-W), λ_n/(d_n² + log n) → ∞ | **beats** (c) (constant level); vs (b): our floor is ≍ (d_n² + log n)/n, equal to theirs when d_n² = O(log n) (Ex-Proxy-d: d_n = O(1)), larger when the removal directions are rich — **short** in that case, reason: the route must beat the removal width; recorded |
| delivery | method as coded | published MCMC theorems do not claim the algorithm returns (they analyse a chain, not code) | W2-UNI:F-UNI: P(no output) = 0 under model G on the instance classes | **beats** (c): every input, no law; n/a for (b) |
| mode interface | — | Johnson–Rossell (2012) and Castillo et al. (2015) state HPM/posterior concentration; mode consistency is the weaker standard target | RM-0: π(S₀) > ½ | **beats** (c); matches the literature's target |

## 3. Boundary numerics (weakened hypotheses (V♭), (BM-W⁺), (T1-F♭))

Done (`numerics/RESULTS.md`, `numerics/SPEC.md`; 336 runs) [R1-sol-5]: sweep θ_n² = κσ² log n/n, κ ∈ {0.5, …, 32}, on
Ex-Proxy (b ∈ {0.3, 0.45}) and one Gaussian-row design with a weak second truth; recorded start-mode inclusion, truth
removal and NA at visited sets, LS0 endpoint, and a mode-margin proxy on a candidate list (not the exact mode). Observed [R2-sol-F1, R2-opus-F3]: truth removal at S₀ and the LS0 endpoint fail only for κ ≤ 4 (n = 400) and κ ≤ 2
(n = 1600), in both designs. Start-mode inclusion follows the same pattern in design P, but in design G the weak truth
is not in the coded start mode up to κ = 16 (5/10 and 5/6 at κ = 32), while LS0 still recovers S₀. All of these levels
are far below κ₀. The constants are artefacts, and nothing here shows that the order is necessary.
No numerics are planned for (D) or 𝓜_n (deterministic code facts / an inclusion of events).

## 4. Better-theorem input

None run (RIDER_RULES §3: the sharp1/sharp1b/sharp2 blind audits are the better-theorem input). Their proposals for
this ticket and dispositions: T2(a), T2(b), T2(c), T4, sharp2 additive (BM-W) floor, Ex-Proxy decaying θ — **adopted**
(this statement); quantile (W) — **proposed open item O-Wq**; Ex-Equi 3/8 — optional / O4′; RM2-R aggregated leak —
open item; η_A exponent wording (sharp1b) — editorial, not adopted.
