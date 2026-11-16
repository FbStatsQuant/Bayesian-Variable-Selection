# W3-PSHARP-R — STATEMENT v1.1 (delta over W3-PSHARP; 2026-11-15; lead: Claude Opus 5.5, claudeAgent_claude_third, high; v1.1 = statement-lock amendments [L01-F#], `reviews/L01_disposition.md`; **locked**)

Ticket T12 of `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` (row W3-PSHARP:A, line 43; §2 row T12, line 80; §4,
line 111). Rider, Tier B.

**This is a delta statement.** PARENT := `Theory_work/Wave3/W3-PSHARP/`, statement `STATEMENT.md` (header v1.2.2;
registered claims `W3-PSHARP:S`@1.0.0, `W3-PSHARP:A`@1.0.0, `W3-PSHARP:B`@1.0.0, `W3-PSHARP:C`@1.0.0). Below,
"PARENT :a-b" means PARENT `STATEMENT.md` lines a-b. This file states **in full** every definition, hypothesis and
claim that differs from PARENT and takes everything else from PARENT by line. It **adds** two claims
(`W3-PSHARP-R:AE`, `W3-PSHARP-R:A2C`) and **corrects two readings** (PARENT :84-88 and :109). It changes no PARENT
claim text and **asserts no proof status**: the proofs belong in `lemmas/AE_expectation.md` and
`lemmas/A2C_critical.md` (routes: `PLAN.md` §2); whether they are written and checked is recorded outside this file.
No method change. All results are about the exact coded target π.

## 0. What changes, in one table

| item | this file | PARENT text it bears on | what is gained |
|---|---|---|---|
| C1 | Proposition A-E (§3.1) | Prop A, :62-69 (in probability; N_n → ∞) | an **expectation** lower bound for **every** null-block size N_n ≥ 1, with log(p√n/(s₀+1)) in place of log N_n |
| C2 | Corollary A1-E (§3.2) | Cor A1 second display, :72 | E δ_n ≥ (1 − o(1))(s₀+1)√((a+½)/π) r_n for p = n^a, in place of √(a/π); **fixed p included** |
| C3 | Corollary A2-E (§3.3) | Cor A2, :75-77; B2–B3, :103-111 | in expectation the growing-s₀ obstruction holds for **every p** (no log p ≍ log n) |
| C4 | Proposition A2C (§3.4) | Cor A2, :75-77 | on (W-orth) at the critical scale: limsup π(S₀) ≤ e^{−λ} in place of the implied 1/(1 + λ) |
| R1 | reading A3′ (§4.1) | Remark A3, :84-88 | the √(log n) expectation obstruction includes bounded p; r_n is exact in expectation where the quoted expectation upper bound applies [L01-F1] |
| R2 | reading B3′ (§4.2) | B3 parenthesis, :109 | "no claim when log p = o(log n)" becomes in-probability only |

Nothing else changes. In particular PARENT Prop A (in probability), Cor A1 first display and its p = n^a line, Lemma
S, Corollary B and Proposition C stand as recorded.

## 1. Base (taken from PARENT unchanged)

- Notation, the coded target π, δ_n, r_n, the truth (G), S₀, s₀, μ, θ*, γ_j, c(p, s): PARENT :16-30.
- Lemma S (consumed in proofs, `W3-PSHARP:S`@1.0.0): PARENT :32-44.
- Setting of Proposition A — sequence indexed by n → ∞ under (G), s₀ + 1 ≤ K, fixed σ*² > 0, M, M′ < ∞, (E)
  ‖μ‖² ≤ nM, (C) ‖θ*‖² ≤ nM′: PARENT :48-50, **except** the clause N_n → ∞, which §2 drops for the C1–C3 claims.
- Witness (W-orth): PARENT :54-55 verbatim. Witness (W-sph): PARENT :56-60. r₀ := rank X_{S₀} (PARENT :58).
- Λ_n := (s₀ + 1)·[2N_n/(2p − 1 − s₀)]·√(log N_n/(πn)) (PARENT :63).
- Proposition A, Corollaries A1, A2: PARENT :62-77 (unchanged; C4 only adds to Cor A2).

## 2. New notation and changed hypotheses

**Notation.**
  c_n := (s₀ + 1)/((2p − 1 − s₀)√n),   ℓ_n := log( p√n/(s₀ + 1) ),
  Λ^E_n := (s₀ + 1)·[2N_n/(2p − 1 − s₀)]·√(ℓ_n/(πn))  ( = 2c_nN_n√(ℓ_n/π) ).
Since s₀ + 1 ≤ K ≤ p, ℓ_n ≥ ½ log n.

**Setting-E** (for C1–C3). The setting of PARENT :48-50 with **N_n ≥ 1** in place of N_n → ∞ (the null block 𝒩_n ⊆
[p]∖S₀ is nonempty; its size may stay bounded). S₀, p and 𝒩_n are deterministic.

**(W-orth-E)** := (W-orth) (PARENT :54-55) and (log p)² = o(n).
  (When 𝒩_n = [p]∖S₀, (W-orth) gives p ≤ n − 1 + s₀ − r₀ ≤ 2n, so (W-orth-E) = (W-orth).)

**(W-sph-E)** := X_{S₀} and θ* are deterministic; the directions ω_j := x_j/√(n − 1), j ∈ 𝒩_n, are iid uniform on the
unit sphere of 1^⊥ and independent of ε (PARENT :56-57, first sentence); and
  (log p)² = o(n),   (r₀ + 1)·log(pn) = o(n).
  (These replace (log N_n)² = o(n), (r₀ + 1) log N_n = o(n) of PARENT :57-58 for C1–C3. With s₀ fixed both reduce to
  (log p)² = o(n). Example as PARENT :59-60: raw null columns with iid N(0, 1) entries, independent of X^r_{S₀} and ε,
  now with any number N_n ≥ 1 of them.)

## 3. Claims

### 3.1 `W3-PSHARP-R:AE` — Proposition A-E (expectation lower bound, every N_n ≥ 1)

**Proposition A-E.** Under Setting-E and (W-orth-E) or (W-sph-E): for every ϵ ∈ (0, 1) there is n₀ such that for all
n ≥ n₀
  E δ_n ≥ (1 − ϵ − Λ^E_n)·Λ^E_n.
Here n₀ depends only on ϵ, (σ*², M, M′) and the o(·) sequences in (W-orth-E), resp. (W-sph-E) — i.e. on common
deterministic sequences bounding (log p)²/n, resp. (log p)²/n and (r₀ + 1) log(pn)/n, that tend to 0 [L01]; in
particular the bound is uniform over all designs, θ*, S₀ and 𝒩_n that satisfy the hypotheses with the same constants and
sequences (N_n is not restricted). Consequently, **if Λ^E_n → 0, then liminf E δ_n/Λ^E_n ≥ 1.**
*Random (X_{S₀}, θ*).* If (X_{S₀}, θ*) is random and the hypotheses hold conditionally on (X_{S₀}, θ*) on events 𝒜_n
with the same constants and sequences, then E δ_n ≥ P(𝒜_n)(1 − ϵ − Λ^E_n)Λ^E_n for n ≥ n₀; so the last conclusion
holds whenever P(𝒜_n) → 1.

### 3.2 Corollary A1-E (fixed s₀, all nulls; part of `W3-PSHARP-R:AE`)

Let s₀ be fixed, 𝒩_n = [p]∖S₀ (so N_n = p − s₀ ≥ 1), p = p_n bounded or not, under (W-orth) or (W-sph-E). Then
Λ^E_n → 0 and
  liminf_n  E δ_n / { (s₀ + 1)·[2(p − s₀)/(2p − 1 − s₀)]·√( log(p√n/(s₀ + 1)) / (πn) ) }  ≥ 1.
In particular:
- **(a)** if p → ∞: liminf E δ_n / [(s₀ + 1)√(log(p√n/(s₀ + 1))/(πn))] ≥ 1; with p = ⌊n^a⌋, a > 0 (under (W-orth):
  p = min(n − 1, ⌊n^a⌋), 0 < a ≤ 1):
    E δ_n ≥ (1 − o(1))·(s₀ + 1)·√((a + ½)/π)·r_n;
- **(b)** if p is fixed (p ≥ s₀ + 1):
    E δ_n ≥ (1 − o(1))·(s₀ + 1)·[2(p − s₀)/(2p − 1 − s₀)]·r_n/√(2π).

### 3.3 Corollary A2-E (growing s₀, expectation, every p; part of `W3-PSHARP-R:AE`)

Under Setting-E with 𝒩_n = [p]∖S₀ and s₀ ≤ p/2 (s₀ may grow), and (W-orth-E) or (W-sph-E) **without its rank
condition** (i.e. the spherical structure of (W-sph-E) with (log p)² = o(n) only) [L01-F3]:
- **(i)** E δ_n → 0 implies Λ^E_n → 0, i.e. (s₀ + 1)√(log(p√n/(s₀ + 1))/n) → 0;
- **(ii)** E δ_n = O(r_n) implies s₀ = O(1).
No relation between log p and log n is assumed; p may be bounded.

### 3.4 `W3-PSHARP-R:A2C` — Proposition A2C (critical scale on the orthogonal witness)

Setting of PARENT :48-50 (N_n → ∞ kept) with (W-orth), 𝒩_n = [p]∖S₀, p → ∞, s₀/p → 0, and Λ_n → λ ∈ [0, ∞)
(Λ_n as PARENT :63; under these hypotheses Λ_n = (1 + o(1))(s₀ + 1)√(log p/(πn)), PARENT `lemmas/A_log_factor.md:121`,
so the condition reads (s₀ + 1)√(log p/(πn)) → λ). Then for every η > 0
  P( δ_n/(1 − δ_n) ≥ e^λ − 1 − η ) → 1,  equivalently  P( π(S₀) ≤ e^{−λ} + η ) → 1.
Consequently (0 ≤ π(S₀) ≤ 1): limsup E π(S₀) ≤ e^{−λ} and liminf E δ_n ≥ 1 − e^{−λ} [L01-F4].

## 4. Corrected readings (not claims)

### 4.1 Reading A3′ (replaces the expectation reading of PARENT :84-88)
In probability, PARENT Remark A3 stands: on its two sequences (i), (ii) (PARENT :81-83), conditional on the two upper
bounds it quotes, (s₀ + 1)√(a/π)(1 − o_P(1)) ≤ δ_n/r_n = O_P(1). **In expectation**, Corollary A1-E gives on the same
sequences E δ_n ≥ (1 − o(1))(s₀ + 1)√((a + ½)/π) r_n (on (ii) through the random-(X_{S₀}, θ*) clause of §3.1, with
P(𝒜_n) → 1 as in PARENT `lemmas/A_log_factor.md:141-142`), and for fixed p the bound of A1-E(b). The √(log n) factor
in E δ_n is therefore present for every p, bounded p included: it comes from the upper tail of the single one-step
fit factors, not from the number of competitors. With `W3-POST2:C`@1.0.0 as quoted at PARENT :85-87, E δ_n ≍ r_n on
(i) for 0 < a ≤ 1, and on (ii) under the same proviso on P(𝒜_nᶜ) as there; for fixed p the upper half is not checked
here. PARENT's last sentence ("Not settled: an upper bound of order √((1 ∨ log p)/n) when log p = o(log n)") is
corrected to: **for E δ_n such an upper bound is false on the witness designs** (A1-E(b), A2-E); it remains open **in
probability** only.

### 4.2 Reading B3′ (replaces the parenthesis of PARENT :109)
"In probability the obstruction does not apply when log p = o(log n), and no claim is made there. For expectation-rate
targets it applies for every p: on the witness sequences of Corollary A2-E, E δ_n = O(r_n) forces s₀ = O(1), and
E δ_n → 0 forces (s₀ + 1)√(log(p√n/(s₀ + 1))/n) → 0."

## 5. What is not claimed
- No upper bound, and no matching upper constant for E δ_n (numerics: `numerics/ae_fixed_p_out.txt`, ratio
  E δ_n/Λ^E_n = 0.99–1.03 at n = 10⁶ for p ∈ {2, 3, 5}; an observation only).
- The in-probability constant of PARENT Cor A1 is not changed: in probability the constant stays √(a/π), and
  Proposition A-E says nothing about δ_n in probability. With N_n bounded, PARENT's in-probability log factor is not
  available (PARENT `ASSUMPTION_MAP.md:15`); the √(log n) in A1-E(b) is an expectation (tail) effect only.
- A2C is claimed on (W-orth) only; on (W-sph) it would need multi-step fit control (not attempted). Its expectation
  consequence follows by boundedness; no matching upper bound for E δ_n is claimed [L01-F4].
- Parked (named, no work): dropping (G) under (W-sph); a coherence witness replacing exact orthogonality.

## 6. Dependencies and supersession

Consumed in the proofs (cited, unchanged): `W3-PSHARP:S`@1.0.0 (Lemma V; Lemma S(1) incl. its equality case, S(2),
S(4)); `W3-PSHARP:B`@1.0.0, consequence (B1) (PARENT :99), in Corollary A2-E only [L01-F3]; inside the proof of
`W3-PSHARP:A`@1.0.0: PARENT `lemmas/A_log_factor.md` Lemma W(i) (:22-24), Lemma W(ii)(a)-(b)
(:26-37), the proof of Lemma R (:45-50), §3 identities and the bound on V (:53-63), §4 scores, law of the ζ_j and
bound on κ′_n (:75-99), §6 A2 asymptotics (:121). Copies with changed lines, where needed, are in this folder with
[R-#] marks.

| new claim | implies (PARENT claim, clause) | why (one line) |
|---|---|---|
| `W3-PSHARP-R:AE` (A1-E) | `W3-PSHARP:A`@1.0.0, Cor A1 second display (:72) | Cor A1's hypotheses give (W-orth) resp. (W-sph-E) (s₀ fixed); 2N_n/(2p − 1 − s₀) → 1 and ℓ_n ≥ log p once n ≥ (s₀ + 1)² |
| `W3-PSHARP-R:AE` | — (not the in-probability clauses :62-69, :72 first display, :73) | different mode of convergence; PARENT A stays the record for them |
| `W3-PSHARP-R:A2C` | `W3-PSHARP:A`@1.0.0, Cor A2 odds bound (:75-76), on (W-orth) with Λ_n → λ ∈ (0, ∞) | e^λ − 1 > λ; Λ_n → λ ∈ (0, ∞) gives (1 − ϵ)Λ_n ≤ e^λ − 1 − η eventually |
| readings A3′, B3′ | correct the readings at :84-88, :109 (not claims) | expectation now covered for every p by AE |

Supersession: none requested here. Whether `W3-PSHARP-R:AE` supersedes the expectation display of PARENT Cor A1 (a
headline statement) is HQ's decision through the HQ consultant (PROTOCOL_v4 H5).

## Changelog (PROTOCOL_v4 §4.2; rows after the lock)

| version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| 1.0 | all | — (draft for the lock) | — | — | — |
| 1.1 | §0 row R1 | EQUAL (summary narrowed to what §4.1 says) | overclaim in the summary table | `reviews/L01_statement_lock_sol.md` F1 | lock amendment |
| 1.1 | §3.1 "n₀ depends only on" | EQUAL (wording) | meaning of "same o(·) sequences" | L01, §Claim-by-claim | lock amendment |
| 1.1 | §3.3 A2-E hypotheses | STRONGER (rank condition of (W-sph-E) dropped) | removable via PARENT B1 | L01 F3 | lock amendment |
| 1.1 | §3.4 A2C | STRONGER (expectation consequence added) | free by boundedness | L01 F4 | lock amendment |
