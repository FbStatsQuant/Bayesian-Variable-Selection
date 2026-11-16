# W3-START2-R — REPORT (rider on the start-mass statement; STATEMENT v1.5)

Lead: Claude Opus 5.5 (effort high, Claude Third). Statement: `STATEMENT.md` v1.5, a delta over W3-START2 v1.4.1
(PARENT `STATEMENT.md`), itself a delta over W3-START v1.3.4 (BASE `STATEMENT.md`). Proofs: `lemmas/R1_VIS.md`,
`lemmas/R2_NEC.md`, `lemmas/R3_RATE.md`, `lemmas/R4_TRANSFER_COR.md`, `lemmas/R5_EX.md`. This file is part of the
frozen content read by the council. It restates no hypothesis or conclusion (PROTOCOL_v4 §3): it points to STATEMENT
lines. Sentences that are not in STATEMENT or a lemma are labelled HEURISTIC or OPEN. The review trail and the final
statuses are in the ticket's final checkpoint file (outside the frozen content).

## 1. What changes (pointers; the table of `STATEMENT.md:17-32` is the authoritative summary)

* **Gaussian-row rate (T10).** (T3⁺⁺)(b)(iii) (`STATEMENT.md:234-235`) with its new hypothesis (D5) (`:82-87`) and the
  bridge (B-R⁺⁺)(iii) (`:223`); the reference-set size of (D4) (`:70-81`) in (T3⁺⁺)(b)(i)–(ii) (`:228-233`); the rate of
  IF-START⁺⁺ (`:241-245`). The one new proof step is `lemmas/R3_RATE.md` R3.3 (the leading functional with the 2^{s₀} − 1
  proper subsets of S₀ as reference sets); R3.6 composes it with PARENT Proposition P1.4.
* **Visibility at the level of the actual p (T8).** (D3) (`STATEMENT.md:51-69`); START-F⁺⁺ (`:113-128`) with the bridges
  VIS-c⁺⁺, VIS-m⁺⁺ (`:101-112`); necessity at the same level, with drifting constants: NEC-b⁺⁺, NEC⁺⁺ (`:145-166`); F4⁺⁺
  (`:134-144`). Proofs: `lemmas/R1_VIS.md` (copies of BASE L4.1, L4.2 with the exact price) and `lemmas/R2_NEC.md`
  (copies of BASE L7.1, L7.2, L3.5; drifting clauses new; example R2.6 for the sentence "the constant 1 cannot be
  lowered" of (N3⁺⁺), `STATEMENT.md:162-163`).
* **Transfer and restatements.** TRANSFER⁺⁺ (`STATEMENT.md:167-188`), F1⁺⁺–F3⁺⁺ (`:129-133`), OVL⁺⁺ (`:212-214`), MIS⁺⁺
  (`:189-198`), EX⁺⁺ (`:199-211`). Proofs `lemmas/R4_TRANSFER_COR.md`, `lemmas/R5_EX.md`.
* **Wording.** The remark on Lemma LEAK-0 (`STATEMENT.md:92-97`).
* **Honest reading (brief item 4).** The leading-term change of version 1.4 (𝔏^♯_n in place of 𝔏⁰_n) is a rate gain only
  when p = O(√log n); in the regime p ≫ n version 1.4 and version 1.3.4 have the same rate (triage
  `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md:29-31`). The gains of version 1.5 that matter for p ≫ n are (T3⁺⁺)(b)(iii) and
  (D3).

## 2. Brief versus delivered

| brief item (`BRIEF.md`) | delivered | beyond the wording (approved at CP1) |
|---|---|---|
| T10 | (T3⁺⁺)(b)(i)–(iii), (B-R⁺⁺)(i)–(iii), IF-START⁺⁺, TRANSFER⁺⁺, EX⁺⁺ G-1/G-2 | (iii) under (D5) (leakage ≤ C₀(n log n)^{−1/2} given proper subsets of S₀) instead of C_L = 0; (ii) with the explicit factor N̄_n |
| T8 | (D3), VIS-c⁺⁺, VIS-m⁺⁺, START-F⁺⁺, NEC-b⁺⁺, NEC⁺⁺, F4⁺⁺, EX⁺⁺ F-2 | F4⁺⁺ as an explicit bound valid for every c_n ≤ 1 |
| item 3 | MIS⁺⁺ (with the Gaussian-row instance), EX⁺⁺, F1⁺⁺, F3⁺⁺, F4⁺⁺ | F2⁺⁺ and OVL⁺⁺ restated as well |
| item 4 | `STATEMENT.md:92-97`; §1 above | — |
| item 5 (T9, T11) | not adopted (CP1); named open items, §7 | — |

## 3. Claims, proofs and author status

| claim (W3-START2-R:…) | statement | proof | author status |
|---|---|---|---|
| VIS-c | `STATEMENT.md:101-107` | `lemmas/R1_VIS.md` R1.3–R1.4 | "PROVED (by this seat)" (`lemmas/R1_VIS.md:3`) |
| VIS-m | `STATEMENT.md:108-112` | `lemmas/R1_VIS.md` R1.2, R1.4 | "PROVED (by this seat)" |
| START-F | `STATEMENT.md:113-128` | `lemmas/R1_VIS.md` R1.5 | "PROVED (by this seat)" |
| F1, F2, F3 | `STATEMENT.md:129-133` | `lemmas/R4_TRANSFER_COR.md` R4.2 | "PROVED (by this seat)" (`lemmas/R4_TRANSFER_COR.md:3`) |
| F4 | `STATEMENT.md:134-144` | `lemmas/R2_NEC.md` R2.7 | "PROVED (by this seat)" (`lemmas/R2_NEC.md:3`) |
| NEC-b | `STATEMENT.md:145-153` | `lemmas/R2_NEC.md` R2.1–R2.4 | "PROVED (by this seat)" |
| NEC | `STATEMENT.md:154-166` | `lemmas/R2_NEC.md` R2.5–R2.6 | "PROVED (by this seat)" |
| TRANSFER | `STATEMENT.md:167-188` | `lemmas/R4_TRANSFER_COR.md` R4.1 | "PROVED (by this seat)" |
| MIS | `STATEMENT.md:189-198` | `lemmas/R4_TRANSFER_COR.md` R4.4 | "PROVED (by this seat)" |
| EX | `STATEMENT.md:199-211` | `lemmas/R5_EX.md` | "PROVED (by this seat)" (`lemmas/R5_EX.md:3`) |
| OVL | `STATEMENT.md:212-214` | `lemmas/R4_TRANSFER_COR.md` R4.3 | "PROVED (by this seat)" |
| BR | `STATEMENT.md:217-225` | `lemmas/R3_RATE.md` R3.0–R3.3 | "PROVED (by this seat)" (`lemmas/R3_RATE.md:3`) |
| START-R | `STATEMENT.md:226-240` | `lemmas/R3_RATE.md` R3.4–R3.6 | "PROVED (by this seat)" |
| IF-START | `STATEMENT.md:241-246` | `lemmas/R3_RATE.md` R3.7 | "PROVED (by this seat)" |

## 4. Assumptions, dependencies, supersession

New assumption ids: A:START2R-V ((D3), `STATEMENT.md:51-69`; implied by A:START-V), A:START2R-R-L ((D4), `:70-81`;
implied by A:START2-R-L), A:START2R-R-L0 ((D5), `:82-87`). Unchanged ids are listed at `STATEMENT.md:34-48`.
Consumed claims and the supersession table: `STATEMENT.md:258-286`. Proof steps of the parents are cited by line in the
lemma files; each lemma's header lists them.

## 5. Sharpness record

| item | reading | evidence |
|---|---|---|
| constant 1 in (V-cp) and in (V-mp) at D = {j}, N = ∅ | NECESSARY for every sequence p_n ≤ n^A (premise of (N3⁺⁺) non-vacuous together with the other hypotheses) | `lemmas/R2_NEC.md` R2.2, R2.6 |
| quantifier of (V-cp) (all 15-sets) vs (N3⁺⁺) (subsets of S₀) | OPEN, as in version 1.4 | — |
| rate √(log n/n) in (T3⁺⁺)(b)(iii) | optimal up to √log n against (T0) (`STATEMENT.md:236-237`); a matching lower bound √(log p/n) is not claimed (OPEN; BASE `STATEMENT.md:380`) | `lemmas/R3_RATE.md` R3.6 |
| scale C₀(n log n)^{−1/2} in (D5) | NECESSARY-FOR-ROUTE: a shift d̄ ≫ 1/√log n of the Gaussian score costs e^{O(d̄√log n)} in Φ_n; whether e^{C√log n} is attained at C_L > 0 is OPEN | `lemmas/R3_RATE.md` R3.3 |
| N̄_n in (T3⁺⁺)(b)(ii) | NECESSARY-FOR-ROUTE (first-moment union over reference sets); not needed at Q = S₀ | `lemmas/R3_RATE.md` R3.2, R3.3 |
| window (c_n − 1)√log n → ∞ in NEC-b⁺⁺ | matches the Gaussian cross term O_P(√log n) of one witness; HEURISTIC that it is the right width | `lemmas/R2_NEC.md` R2.3–R2.4 |
| F-2 first-order form only for A > 3/4 | a limit of the upper bound used, not of the design (OPEN below 3/4) | `lemmas/R5_EX.md` R5.2 |

## 6. Numerics (observations, not proofs; no statement cites them)

`numerics/RESULTS.md` (scripts `numerics/run_numerics.R`, `numerics/r_common.R`, `numerics/gens.R`, `numerics/summarise.R`,
`numerics/make_tables.R`; `numerics/summary.csv`; production core, 420 runs). G-1 (Σ = I, p = 2n, n = 200…3200):
o₀·√(n/log n) flat at about 1.9–2.2 — consistent with (T3⁺⁺)(b)(iii). Leakage 2/√(n log n) versus 2/√n: no visible
difference at these n. F-2 at A = 0.9: o₀/T₁ between about 1.2 and 1.9, no visible convergence (the predicted approach
is like n^{−0.06}, too slow to observe). (V-cp) switch at c = 1: **not resolved** at n ≤ 3200 (only c = 1.5 against
c = 0.6 separates, at both p regimes); the necessity statements are asymptotic and these runs neither support nor
contradict the location of the switch.

## 7. Open items

* W3-START2R-O1: Corollary MIS for a general deterministic μ ∉ span X_𝒞 without (GR) (`STATEMENT.md:253-254`).
* Named, not adopted at CP1: T9 (F1 with the exact Laplace exponent; F3 with G_n = o(log n), no growth premise; F4 at
  n^ι columns) and T11 (factorised OVL⁺; many leakers).
* Gaussian-row: a lattice rate without N̄_n for Q ⊋ S₀; the rate when (D5) fails; a lower bound √(log p/n).
* Inherited: PARENT `STATEMENT.md:191-201` as amended by `STATEMENT.md:247-256`.

## 8. Files (under `Theory_work/Wave3/W3-START2-R/`)

Frozen content: `STATEMENT.md`, `REPORT.md`, `TARGET.md`, `READER_DELTA.md`, `PLAN.md`, `BRIEF.md`, `RIDER_RULES.md`,
`citecheck.py`, `DEPS.tsv`, `lemmas/R1_VIS.md`–`lemmas/R5_EX.md`, `numerics/` (scripts, summary, RESULTS). Outside it:
`LOG.md`, the checkpoint files, `reviews/`.

## 9. Registry blocks

```
REGISTRY
claim: W3-START2-R:START-F | kind: theorem | statement: STATEMENT.md:113-128 | premises: STATEMENT.md:34-69
name: Theorem START-F (fixed design; visibility at the level of the actual p)
status: PROVED (by this seat) | status_source: lemmas/R1_VIS.md:3
assumptions: A:START-E ; A:START-GF ; A:START-AL ; A:START2R-V (new | visibility at c log n + 2 log p, or margin form with the exact prior price | STATEMENT.md:51-69 | shared yes)
conclusion: target: start mass on the lattice of Q and start odds against S0 as at STATEMENT.md:116-125 | rate: STATEMENT.md:116-118 | scope: fixed design; s0 fixed; p <= n^A (p >> n allowed)
depends_on: W3-START2-R:VIS-c@stmt ; W3-START2-R:VIS-m@stmt ; W3-START2:START-F@proof ; W3-START:ASM@stmt
implies: W3-START2:START-F ((V-c) and (V-m) imply (D3); conclusions identical)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better:PENDING(TARGET.md)

REGISTRY
claim: W3-START2-R:VIS-c | kind: lemma | statement: STATEMENT.md:101-107 | premises: STATEMENT.md:51-69
name: Bridge B-V1++ (constant-level visibility at c log n + 2 log p)
status: PROVED (by this seat) | status_source: lemmas/R1_VIS.md:3
conclusion: target: [VIS(kappa; Q)] for every kappa < (c_V - 1)/2 | scope: fixed design
depends_on: W3-START:VIS-c@proof ; W3-START:TK@stmt
implies: W3-START:VIS-c ((V-c) implies (V-cp) with c_V - 2A)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:VIS-m | kind: lemma | statement: STATEMENT.md:108-112 | premises: STATEMENT.md:51-69
name: Bridge B-V2++ (margin visibility with the exact prior price)
status: PROVED (by this seat) | status_source: lemmas/R1_VIS.md:3
conclusion: target: [VIS(kappa; Q)] for every kappa < c_m/2 | scope: fixed design
depends_on: W3-START:VIS-m@proof ; W3-START:TK@stmt
implies: W3-START:VIS-m ((V-m) implies (V-mp) for n >= 256 s0^2)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:F1 | kind: corollary | statement: STATEMENT.md:129-133 | premises: STATEMENT.md:51-69
name: Corollaries F1++, F2++, F3++ (under visibility at the level of the actual p)
status: PROVED (by this seat) | status_source: lemmas/R4_TRANSFER_COR.md:3
conclusion: target: as BASE F1, PARENT F2+, BASE F3 with (D3) | scope: fixed design
depends_on: W3-START2-R:START-F@stmt ; W3-START:F1@proof ; W3-START2:F2@proof ; W3-START:F3@proof
implies: W3-START:F1 ; W3-START2:F2 ; W3-START:F3 (visibility weaker)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:F4 | kind: corollary | statement: STATEMENT.md:134-144 | premises: STATEMENT.md:51-69
name: Corollary F4++ (isolated leaking columns at the pointwise level; explicit bound)
status: PROVED (by this seat) | status_source: lemmas/R2_NEC.md:3
conclusion: target: bound on rho_n(Q; h) at STATEMENT.md:139 | scope: fixed design; every c_n <= 1
depends_on: W3-START:F4@proof ; W3-START2-R:START-F@stmt
implies: W3-START:F4 (old premise gives the new one; new bound gives the old)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:NEC-b | kind: lemma | statement: STATEMENT.md:145-153 | premises: STATEMENT.md:34-48
name: Lemma NEC-b++ (component diagnostics at c log n + 2 log p; drifting constants)
status: PROVED (by this seat) | status_source: lemmas/R2_NEC.md:3
conclusion: negative: pi0(S0) -> 0 under one leaking null or one weakly visible truth on the actual partition | scope: fixed design
depends_on: W3-START:NEC-b@proof ; W3-START:TK@stmt
implies: W3-START:NEC-b (old premises give the new ones)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:NEC | kind: proposition | statement: STATEMENT.md:154-166 | premises: STATEMENT.md:34-48
name: Proposition NEC++ (limits at c log n + 2 log p for every p_n)
status: PROVED (by this seat) | status_source: lemmas/R2_NEC.md:3
conclusion: negative: STATEMENT.md:155-164 | scope: fixed design
depends_on: W3-START2-R:NEC-b@stmt ; W3-START2:NEC@proof ; W3-START:FLOOR@stmt
implies: W3-START2:NEC (clause by clause)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:TRANSFER | kind: theorem | statement: STATEMENT.md:167-188 | premises: STATEMENT.md:34-69
name: Theorem START-R (a), transfer in conditional and random-rate form
status: PROVED (by this seat) | status_source: lemmas/R4_TRANSFER_COR.md:3
conclusion: target: STATEMENT.md:175-185 | scope: random designs with design-measurable targets; |S0| <= s-bar
depends_on: W3-START2-R:START-F@stmt ; W3-START:TRANSFER@proof
implies: W3-START2:TRANSFER (STATEMENT.md:182-185)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:MIS | kind: corollary | statement: STATEMENT.md:189-198 | premises: STATEMENT.md:34-69
name: Corollary MIS++ (misspecified candidate set; Gaussian-row instance of (GR))
status: PROVED (by this seat) | status_source: lemmas/R4_TRANSFER_COR.md:3
conclusion: target: version-1.5 claims for the candidate start under (GR); jointly Gaussian rows give (GR) exactly | scope: STATEMENT.md:189-198
depends_on: W3-START2-R:TRANSFER@stmt ; W3-START:MIS@proof
implies: W3-START:MIS
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:EX | kind: proposition | statement: STATEMENT.md:199-211 | premises: STATEMENT.md:34-87
name: Examples table (T7++)
status: PROVED (by this seat) | status_source: lemmas/R5_EX.md:3
conclusion: target: rows F-1, F-3, F-2, G-1, G-2 as at STATEMENT.md:200-209 | scope: the listed families
depends_on: W3-START2-R:START-F@stmt ; W3-START2-R:F1@stmt ; W3-START2-R:F4@stmt ; W3-START2-R:START-R@stmt ; W3-START:EX@proof
implies: W3-START:EX
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:OVL | kind: proposition | statement: STATEMENT.md:212-214 | premises: STATEMENT.md:51-69
name: Proposition OVL++ (start mass under a bounded leakage set; visibility of (D3))
status: PROVED (by this seat) | status_source: lemmas/R4_TRANSFER_COR.md:3
conclusion: target: as PARENT OVL+ with (D3) | scope: fixed design
depends_on: W3-START2-R:START-F@stmt ; W3-START2:OVL@proof
implies: W3-START2:OVL
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:BR | kind: lemma | statement: STATEMENT.md:217-225 | premises: STATEMENT.md:70-87
name: Bridge B-R++ (Gaussian rows; reference sets up to exp(kappa_H sqrt log n); sharp leading functional O_P(sqrt log n))
status: PROVED (by this seat) | status_source: lemmas/R3_RATE.md:3
assumptions: A:START-R-FL ; A:START-R-V ; A:START2R-R-L (new | localised leakage with reference sets of size exp(kappa_H sqrt log n) | STATEMENT.md:70-81 | shared yes) ; A:START2R-R-L0 (new | null columns uncorrelated with true columns given proper subsets of S0, up to C0 (n log n)^(-1/2) | STATEMENT.md:82-87 | shared yes)
conclusion: target: STATEMENT.md:218-223 | scope: Gaussian rows; p <= n^A
depends_on: W3-START2:BR@proof ; W3-START:BR@proof
implies: W3-START2:BR ((L-R+) implies (L-R++))
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)

REGISTRY
claim: W3-START2-R:START-R | kind: theorem | statement: STATEMENT.md:226-240 | premises: STATEMENT.md:70-87
name: Theorem START-R (b), Gaussian rows: o0 = O_P(sqrt(log n / n)) with uncorrelated nulls
status: PROVED (by this seat) | status_source: lemmas/R3_RATE.md:3
assumptions: A:START-R-FL ; A:START-R-V ; A:START2R-R-L ; A:START2R-R-L0
conclusion: target: STATEMENT.md:228-235 | rate: sqrt(log n / n) under (D5) at Q = S0 (STATEMENT.md:234-235) | scope: Gaussian rows; p <= n^A (p >> n allowed)
depends_on: W3-START2-R:BR@stmt ; W3-START2:START-F@stmt ; W3-START2:TRANSFER@proof ; W3-START:FLOOR@stmt
implies: W3-START2:START-R (same conclusions under weaker hypotheses)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md) ; better:PENDING(TARGET.md)

REGISTRY
claim: W3-START2-R:IF-START | kind: corollary | statement: STATEMENT.md:241-246 | premises: STATEMENT.md:34-87
name: IF-START++ (start interface for the sampler theorems; Gaussian-row rate sqrt(log n / n))
status: PROVED (by this seat) | status_source: lemmas/R3_RATE.md:3
conclusion: target: 1_A o0 = O_P(r_n) with the rates at STATEMENT.md:242-243 | scope: fixed design and Gaussian rows
depends_on: W3-START2-R:START-F@stmt ; W3-START2-R:START-R@stmt
implies: W3-START2:IF-START (each rate at most the old one)
gates: correct:PENDING(reviews/BRIEF_R1_sol.md)
```

HQ notes for the ingest: F1, F2 and F3 are one STATEMENT clause and one registry row here (`W3-START2-R:F1` covers the
three restated corollaries); HQ may split it. Headline effect (PROTOCOL_v4 H5): START-F, START-R, IF-START. The
`council:` field and the `correct:` gate are filled from the council record at CP3.
