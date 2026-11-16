# W3-START2-R — PLAN (lead: Claude Opus 5.5, effort high, Claude Third; Tier B rider, NORMAL mode)

Brief: `BRIEF.md`; binding rules: `RIDER_RULES.md`, `Theory_work/Wave3/PROTOCOL_v4.md`, `Theory_work/Wave3/PROGRAM.md`.
PARENT := `Theory_work/Wave3/W3-START2/` (v1.4.1), BASE := `Theory_work/Wave3/W3-START/` (v1.3.4); both read-only.
Target: `STATEMENT.md` v1.5 (delta over v1.4.1). Motivation: `API_AUDIT/sharp2/TRIAGE.md` rows W3-START:START-F, :F4,
:NEC, :START-R, :EX, :MIS, W3-START2:TRANSFER, :IF-START, :START-R, and §2 rows T8, T10.

## 1. Targets and where the statement goes beyond the brief's wording (each implies the brief's clause)

| brief item | clause of v1.5 | beyond the wording? |
|---|---|---|
| T10 | (T3⁺⁺)(b)(iii): o₀ = O_P(√(log n/n)) at Q = S₀ | the premise is (L-gain-0) — leakage at most C₀(n log n)^{−1/2} given **proper subsets of the truth only** — not C_L = 0 in the full (L-R⁺⁺); C_L = 0 with Q = S₀ is the special case. The proof (L9.5 with the reference sets U ⊊ S₀) uses (L-gain-R) only for these sets, and a mean shift d̄ = O(1/√log n) leaves Φ_n = O(√log n) |
| T10 | (B-R⁺⁺)(ii), (T3⁺⁺)(b)(ii): C_L = 0, lattice rate (\|Q\| + 1)N̄_n√(log n/n) | writes the N_ref factor explicitly; gives the triage's G-2 row (bounded H_l ⇒ √(log n/n) on the lattice) and v1.4's polylog clause as special cases |
| T10 | (L-R⁺⁺): \|H_l\| ≤ H̄_n, log H̄_n ≤ κ_H√log n | as the brief (C_R depends on κ_H: C_B gets 15κ_H) |
| T10 | (T3⁺⁺)(a): (a1) conditional, (a2) random rate, (a3) old form | as the brief; \|S₀\| ≤ s̄ (triage row W3-START2:TRANSFER) |
| T8 | (D3): (V-cp) at c_V log n + 2 log p, c_V > 1; (V-mp) with the exact price π_n(d, a; Q) | as the brief; the a > d price keeps log(p/c_Q) exactly (BASE `lemmas/L4_VIS.md:49`) instead of the constant 15 log(16s₀) |
| T8 | (C2⁺⁺), (N2⁺⁺), (N3⁺⁺): pointwise level and drifting c_n with (c_n − 1)√log n → ∞ | drifting as in raw verdict f05 (`results/f05.md:52`); F4⁺⁺ gets an explicit bound valid for every c_n ≤ 1 (pointwise level; drifting is then automatic) |
| item 3 | F1⁺⁺, F2⁺⁺, F3⁺⁺, OVL⁺⁺ restated under (D3); MIS⁺⁺ with the Gaussian-row instance; EX⁺⁺ | F2⁺⁺ and OVL⁺⁺ are added (both use visibility only through (T1⁺)); the MIS instance goes through (T3⁺⁺)(a), since Setting R has θ* deterministic on the standardised scale and a candidate run has deterministic raw β^𝒞 |
| item 4 | §3.0 (LEAK-0 remark); REPORT will not sell P1 as a p ≫ n gain | — |
| item 5 | T9, T11: **not in v1.5**; proposed for CP1 decision (§5) | — |

## 2. Lemma files (proof plan; copies of parent lemmas with changed lines marked [R-#])

| file | claims | content | est. h | who |
|---|---|---|---|---|
| `lemmas/R1_VIS.md` | VIS-c⁺⁺, VIS-m⁺⁺, START-F⁺⁺ | copy of BASE `L4_VIS.md` L4.1–L4.2: Step 5 with the exact price (Π ≤ π_n/2 + C₂ for d ≥ a, Π ≤ π_n/2 for a > d), Step 6 split by the sign of π_n (for π_n < 0 the factor (1 − ε₁)/(1 + ω_n) ≤ 1 only helps); L4.2 with log(2p) kept (ε₁ ≤ (κ_V − κ)/(4(c_V + 2A))). START-F⁺⁺ = PARENT P1.4–P1.5 with these thresholds (no other change). Relation (V-c) ⇒ (V-cp), (V-m) ⇒ (V-mp) (n ≥ 256s₀²) | 2 | helper A |
| `lemmas/R2_NEC.md` | NEC-b⁺⁺, NEC⁺⁺, F4⁺⁺ | copy of BASE `L7_NEC.md` with log((s₀+1)/(2p − 1 − s₀)) ≥ −log(2p) kept and ε₁ against (c/2 + A); drifting: (δ + σZ)² ≥ δ² − 2\|δ\|σ\|Z\| with \|Z\| ≤ M_ε (tightness), and the converse bound in (ii); (N2⁺⁺) by PARENT `P3_NEC.md` pigeonhole; F4⁺⁺ = BASE L3.5 with G_n := c_n log n + 2 log p ≤ (1 + 2A) log n | 1.5 | helper A |
| `lemmas/R3_RATE.md` | BR⁺⁺, START-R⁺⁺, IF-START⁺⁺ | (i) PARENT P4.1 with N_ref ≤ 2^{15}e^{15κ_H√log n} in (9.2), P(Eᶜ) ≤ (4 + 3N̄_n)n^{−2} → 0; (ii) BASE L9.6(b) with N̄_n; (iii) **new step**: for U ⊊ S₀, BASE L9.5 with U₀ = U, D = S₀, ‖γ²‖ ≤ √s₀C₀/(c_Σ√(n log n)), so d̄ = O(1/√log n) and Φ_n = O(√log n); event E⁰ := CN ∩ ⋂_{l∉S₀, U⊊S₀} E_R(l, U) with P((E⁰)ᶜ) → 0; 𝔏^♯_n ≤ p⁻¹Σ_lΣ_U F·1 on E⁰; Markov. (T3⁺⁺)(b)(i)–(ii) = PARENT P4.2–P4.3 with the new constants; (iii): design set with 𝔏^♯_n ≤ D_ε√log n and 𝔏_n(S₀) ≤ e^{C_B√log n}, case split at each n, second display of (T1⁺⁺)(d) via PARENT P1.7. IF-START⁺⁺ from these | 3 | lead |
| `lemmas/R4_TRANSFER_COR.md` | TRANSFER⁺⁺, F1⁺⁺, F2⁺⁺, F3⁺⁺, OVL⁺⁺, MIS⁺⁺ | (a1) BASE L8.1 + PARENT P1.4 per design (max of constants over s₀ ≤ s̄); (a2) integrate (a1), E min(1, b_n(h)) → 0, P(ϱ_n > c₀) → 0; (a3) from (a2). F1–F3, OVL: the parent proofs use visibility only through (T1⁺), cite lines. MIS: Lemma R′ (BASE `L10_INTERFACES.md:71-75`) and the Gaussian conditional law of ω given X^r_𝒞 | 1.5 | lead |
| `lemmas/R5_EX.md` | EX⁺⁺ | copy of BASE `L11_EXAMPLES.md` rows F-1, F-3 (F2⁺⁺), F-2 ((V-mp) check for N = ∅, \|N\| = 1, \|N\| ≥ 2; rates with the F4⁺⁺ levels; A > 3/4 for (c)), G-1, G-2 | 1.5 | lead |

Numerics (`numerics/`; Sonnet 5.5 helper B, high, from BASE `numerics/start_common.R`, read-only copy): boundary runs of
TARGET.md §3. ≈ 1.5 h.

## 3. Review chain (RIDER_RULES §3; NORMAL mode; Sol = codex gpt-6.1-sol, high)
1. **SL1** statement lock (Sol, fresh, blind): STATEMENT, PLAN, the parent files consumed, triage rows. → CP1, end run.
2. **LC1** Sol line check: R1 + R2 (+ numerics if a statement cites them), plus the statement-change check of the
   SL1 changelog rows (PROTOCOL_v4 §4.2; STATEMENT changelog). **LC2** Sol line check: R3 + R4 + R5.
   New agent per batch, blind to LOG and earlier reviews. Repairs → re-check by a new Sol agent (repair + STALE rows).
3. citecheck (copy of BASE `citecheck.py`), 0 MISS; DEPS all OK; REPORT with registry block.
4. **Council R1**: Sol seat + Opus 5.5 high seat (Claude Third), fresh, blind, on `reviews/MANIFEST_R1.txt`; diff round if
   needed. → CP3, end run.
Expected OpenAI reviews: 4 (lock, 2 line checks, council seat), within the Tier B band 3–6.

## 4. Schedule (CST) and budget (~11–13 Opus h)
| when | step |
|---|---|
| Sun 11-15 evening | SL1, CP1 |
| Mon 11-16 | after CP1 go: helper A on R1–R2; lead R3, R4; helper B numerics |
| Mon night – Tue 11-17 | R5; LC1, LC2; repairs; REPORT, DEPS, citecheck |
| Tue night | freeze MANIFEST_R1, council R1 |
| Wed 11-18 by 12:00 | diff round if needed; **CP3 by 18:00** |
Kill budgets (BRIEF): 3 attempts per lemma; the (iii) step of R3 (the N_ref removal) gets 2 — two failed attempts ⇒
early checkpoint (it is the target clause).

## 5. Decisions asked at CP1
* T9 / T11: recommend **not** adopting them (named open items) — the cut-off leaves ≈ 1 day of slack for two line
  checks and a council; T9 would add three corollary rewrites (L3.1, L3.5, L6.1, L6.3) to LC1.
* Accept the two places where v1.5 goes beyond the brief's wording (§1): (L-gain-0) in (iii); F2⁺⁺ and OVL⁺⁺ added.

## 6. Risks
* (iii): the event E⁰ must not condition on anything that breaks the independence of the innovation e from W_{S₀}
  (BASE `L9_BR.md:125-126`); with U ⊊ S₀ the conditioning σ-field is σ(W_{S₀}) for every pair (l, U).
* (V-mp) for a > d: when \|Q\| is close to p, log(p/c_Q) < 0; the exact price is kept, the proof must not use a sign.
* Drifting NEC: uniformity of the toolkit remainder (ω̄_n·G_n) when the gain in (i) is much larger than log n: use
  (f1) with a factor ½ there, no upper bound on the gain.
* TRANSFER (a1): versions of conditional probabilities (BASE L8.1, Fubini); constants maximised over s₀ ≤ s̄.
* EX F-2: the claim (c) holds only for A > 3/4 (computed from the F4⁺⁺ bound); do not overstate.
