# BT1 disposition (lead) — better-theorem review by Astra on STATEMENT v1.1

Review: `BT1_better_theorem_astra.md` (blind; gpt-6-astra, high). 3 class-A proposals, 2 class-B, 0 class-C, plus a
"Limits" section. Dispositions below are the lead's, under the pre-approval of legs CP1 → CP2; the two `ticket`
recommendations and the supersession question are HQ's to decide (LIFECYCLE §4.2(c), §5.3).

| label | proposal | axis | disposition | evidence |
|---|---|---|---|---|
| BT1-A1 | Replace GR^c by the law of the contrast direction T = zzᵀ/‖z‖² (the maximal invariant of shifts and rescalings); total-variation stability: E δ ≤ C r_n + d_TV | hypothesis (law) | **adopted** | STATEMENT v1.2 §1(c), §2 "Stability"; proof `lemmas/R_reduction.md` R.5, `lemmas/M_misr.md` M.1. Re-derived by the lead: the standardised response is √N·Uz/‖z‖, every response-dependent score term is linear in T. Restricted, as the reviewer says, to the model-space posterior (not Corollary H). |
| BT1-A3 | (i) localisation without a margin: E π(Ω∖𝒩_n) ≤ C r_n, 𝒩_n = target ∪ small-ridge-loss bounded-excess underfits; (ii) §3(a) needs only the first (OS) inequality | conclusion; hypothesis | **adopted** | STATEMENT v1.2 §3(a), §3(d); proof `lemmas/M_misr.md` M.2 (a) (last remark) and (d). (d) is the (b)-assembly applied to the far underfits; no new input. |
| BT1-A2 | Corollary H in expectation, uniformly over the class, with posterior-tail rates C(r_n + 1/t), C(r_n + 1/log n + 1/t²) | conclusion (mode, uniformity, rate) | **ticket (recommended), not adopted here** | It is an improvement of the input W3-POST2:D (its proofs D2, D3 redone with Gaussian/IG moment bounds), not of the reduction; once proved upstream it transfers through Lemma R′ verbatim (as Remark SNR does for D). W3-POST2:D has a repair history (`Theory_work/Wave3/HQ_DECISIONS.md:36-39, 48-50`), so the bookkeeping should get its own line check rather than ride on this ticket. Recorded in ASSUMPTION_MAP "Unharvested (4)". |
| BT1-B1 | The empty projection s = 0 under a null-anchored Occam sum only: E[1 − π(∅)] ≤ C r_n, growing p | scope | **ticket (recommended), not adopted here** | Needs a new lemma: W3-POST2:C/E assume s₀ ≥ 1, and C1/C2/(C4′)/(C5′) must be re-proved with anchor ∅ (reviewer's own classification: class B). Outside T1 items (a)–(d). Value: covers complete cancellation at growing p (C-MIS Lemma Z covers bounded p only). Also an upstream (well-specified) result first; the misspecified version then follows from Lemma R′. STATEMENT §9 keeps s = 0 under "Not claimed". |
| BT1-B2 | Fresh-covariate (integrated) Hellinger contraction under selection, with a second-moment transfer condition and an intercept condition | conclusion (out-of-sample) | **ticket (recommended, low priority), not adopted here** | New transfer lemma and two new hypotheses (reviewer: class B); it belongs with PROGRAM item 1b (W3-POST2:D). STATEMENT §9 keeps the out-of-sample statement under "Not claimed". |
| BT1-Limits | (E^σ) cannot be deleted: p = 2 orthogonal, θ₁ = n, θ₂² = c log n/n — all other hypotheses hold and π(S₀) → 0 | necessity | **recorded (not a proposal)** | Confirmed numerically: `numerics/N5_energy_obstruction.py` → `numerics/N5_out.txt` (E π(S₀): 0.87 → 0.003 for n = 100 … 102400 with θ₁ = n; = 1.0000 with θ₁ = 1 or √n). ASSUMPTION_MAP row A:MISR-ESNR changed from "improvable (artefact)" to "needed in some form; weakenable"; STATEMENT §9 "Not claimed". |
| BT1-other | F₀ weakening, (OS) removal, p range, growing s, heavy tails, a.s. contraction, an expectation rate in §4(c) | — | none proposed by the reviewer ("I have no checked low-cost replacement") | — |

Effect on the statement: v1.1 → v1.2 adds §1(c), the stability sentence of §2, §3(d), and one parenthesis in §3(a).
No hypothesis of a locked clause was strengthened and no locked conclusion was changed; the additions are new
clauses. They were not seen by the statement-lock reviewers (L01, L02): they are covered by the lemma line checks and
the council, which read v1.2. Whether the better-theorem review must be repeated (PROTOCOL rule 10, "statement changed
materially after CP1") is HQ's call; the lead's reading: the changes are the adoption of this review's own class-A
proposals, so a repeat would ask the same question of the same content.
