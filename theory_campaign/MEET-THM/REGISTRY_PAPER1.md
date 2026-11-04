# REGISTRY_PAPER1 — registrar's registry of the paper-1 theorem list (MEET-THM, updated to the Round 3 decisions of MINUTES.md)

Registrar: Sonnet 5.5 (Claude Work). Date 2026-11-04. **Mechanical registry only: no proving, no judging, no status upgrade.** First built for the chair's proposal `SYNTH_R2.md` §2 (v2); **updated to the Round 3 decisions of `MINUTES.md` §2** (main M1–M8, supplement cards, FUTURE_WORK and drops, waves and lemma-pack HQs in §2.5). Every item that the first draft marked as still open under Round 3 is resolved in a paragraph headed **Round 3 resolution**. Each item carries an **HQ** line (wave, HQ name, charter file `HQ_CHARTERS/<name>.md`).

**Update note.** The first draft was built before `R3_B.md` was committed and did not follow the Round 3 files. This update follows `MINUTES.md` §2, citing the seats' Round 3 files (`R3_A.md` … `R3_D.md`: §S2 final cards, §S3(a) edge lists, §S3(c) charters) as sources. K-ID statuses, check history, Lean and fidelity entries are unchanged from the first draft. **No registry status is changed anywhere in this file.** The meeting's check verdicts remain statement-sanity / cross-family verdicts, never registry status changes; §9 lists the registry updates this file *recommends to the registry owner* (the registry owner decides). HQ names: M1…M8, LP-FOUND, LP-IDENT, LP-AUDIT, LP-REST, LP-REP; the clerk's `HQ_CHARTERS/` is the authority on file names (not yet present when this file was updated).

## 0. How to read this file

**Sources and citation tags** (all are `path:line` in this worktree unless stated):

| Tag | Source |
|---|---|
| `S2:n` | `theory_campaign/MEET-THM/SYNTH_R2.md` line n (chair's proposal) |
| `A:n` `B:n` `C:n` `D:n` | `R2_A.md` … `R2_D.md` line n (Round 2 seat cards) |
| `R0_DIFF:n` | `R0_DIFF.md` line n (K-ID table; its status cell is the verbatim registry/index status text that the meeting adopted) |
| `IDX:n` | registrar's earlier index `origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md` line n (flags are derived by the index's rule; they are flags, not verdicts) |
| `W1PC1:n` `W1PC2:n` `W2PC1:n` `W2PC2:n` | `evidence/W1_PC1/VERDICTS.md`, `W1_PC2`, `W2_PC1`, `W2_PC2` line n |
| `CHK:n` | `evidence/CHK_INHERITED/REPORT.md` line n |
| `METHOD:n` | `origin/theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md` line n |
| `FUTURE_WORK.md` | `theory_campaign/MEET-THM/FUTURE_WORK.md` |
| `R3_A:n` `R3_B:n` `R3_C:n` `R3_D:n` | `R3_A.md` … `R3_D.md` line n (Round 3 seat files, verbatim). In §5 the short forms `A3:n` `B3:n` `C3:n` `D3:n` mean the same, so that they do not clash with `A:n` = `R2_A.md` |
| `MINUTES §x` | `MINUTES.md` section x (the binding Round 3 decisions) |

**Rules followed.**
- **Status words are copied, never upgraded.** The block labelled *R0_DIFF status cell* is the verbatim cell of the K-ID row (R0_DIFF itself abbreviates a few long registry cells with '…'; that abbreviation is the source's). Qualifiers (AUTHOR-ONLY, SAME-FAMILY-ONLY, XF/SF history, ASTRA-ONLY, 'external review queued', 'candidate: not reviewed') come from the **index flag** of each registry ID (`IDX:n`) and from the quoted cell.
- Where the cell says *'D/E side: proposal (author’s PROOF SKETCH, unchecked)'* the K-ID has no registry row of its own; that wording is the status.
- **Check-history rows are statement-sanity verdicts, NOT proof statuses.** TRUE-AS-WRITTEN means 'no counterexample found in the stated search'. DESIGN-VERIFIED / PLAUSIBLE / GAP are non-vacuity and route verdicts of the checkers. Adverse rows (COUNTEREXAMPLE, NEEDS-HYPOTHESIS, AMBIGUOUS, route GAP/IMPLAUSIBLE, DESIGN-ASSERTED/FAILS, NOT REPAIRED) are listed per item. Each row is cited `file:line`; the row's own text names the card clause it judged.
- *Seat card status (verbatim)* is the seat's own statement of the status. Where it differs from the index, §7 lists it.
- **Fidelity to v3.1 as shipped** answers three questions per item: LS0 (METHOD:150 #8), the coded grid (METHOD:324–328), Ẑ-weighted pooling (METHOD:158 #11). Values: yes / no / n/a / unknown, each with its source. 'Not yet in the production core' for LS0 is METHOD:48, :399.
- **Flag vocabulary** (IDX conventions, REGISTRY_INDEX.md:22–27): `XF-VERIFIED` and `XF-VERIFIED*(qualified)` = a cross-family reviewer wrote VERIFIED (* with a stated qualification); `XF-ADVERSE:GAP` or `XF-ADVERSE:ERROR` = a cross-family reviewer wrote GAP or ERROR on that row; `FLAG SAME-FAMILY-ONLY` = only a same-model-family verifier; `FLAG AUTHOR-ONLY` = no verifier of any family; `ASTRA-ONLY` = Astra-written and Astra-checked. For **non-registry** results a bare `XF` means the source states a cross-family check history (read the quoted check text at the IDX line); `FLAG AUTHOR-ONLY` there means a candidate with no review.
- Lean status is from `REGISTRY_INDEX.md` §3 (`origin/theory/L-LEAN` is the only branch with `.lean` files; library `SmcBvs/SmcBvs/*.lean`: 8 files, 101 theorems/lemmas, 0 `sorry`; older copies under `frozen/v1/` and `fidelity/packet/` carry `sorry` in `T07Bayes.lean` (12) and `T37Lattice.lean` (8)). A Lean 'core' in a card is a proposal, not an existing certificate unless a file is named.

**Contents.** §1 main items M1–M8 · §2 supplement cards S-* (S-D removed: it is M8; S-LEAK added) · §3 cited lemmas · §4 FUTURE_WORK / drop / remark table · §5 dependency edge list (union of the four seats' R3 §S3(a) edges) · §6 registry CONFLICT rows touching the list · §7 status disagreements between sources, each with who resolves it · §8 named implementation premises / audit obligations · §9 registry updates recommended to the registry owner.

## 1. Main items (MINUTES §2.1; unanimous in Round 3)

### M1 — Theorem V/H — validity of v3.1 and accuracy of reported bounded functionals

**Round 3 resolution (MINUTES §2.1; R3-1, R3-2 unanimous):** one theorem V/H (no V+/H split). K-IDs on the card: K46, K32, K86, K35, K36, K50, K51, K52, K48, K62; cited K20, K21, K08, K47. Final card: `R3_A.md` §S2 M1. Growth-rate clause: the two optional stacking configurations of MINUTES §2.3 (R′_n = 4⌈log₂(n + p + 1)⌉ for a fixed finite set of declared summaries; R′_n = 4⌈(n + p)⁶/4⌉ for simultaneous control over ≤ (n + p)² declared summaries; both on families with D_* = O_P(1)); the shipped R′ = 4 carries only the fixed-R′ statements. K63 and K86 are premises named here and proved in S-OUT. Safeguard (binding §13.1): if N1's general record identity fails, the narrower theorem ships and §13.1 escalates (MINUTES §2.3).

**HQ:** wave 1 · HQ `M1` · charter `HQ_CHARTERS/M1.md` (seat charter text: `R3_A.md` §S3(c) 'Charter M1'). N1 is the longest pole and starts first (MINUTES §2.5). Premises carried: N1; GUARD-W; IND-T extension (§8). Escalation: N1 refuted or unclosed after one wave; GUARD-W or IND-T extension audit failing → (c),(d) revert to potential-run statements and N2 reopens (R3_A:192).

**Seat cards (R2):** A:40–58 (V+ (A:40–48), H (A:50–58)); B:81–99 (V+ (B:81–89), H (B:91–99)); C:68–77 (C1); D:55–63 (H′).

**K-IDs in this item:** K46 (core: general-h identity N1 (measured-endpoint, random-position RB)), K32 (core: frozen-𝒞 contract), K86 (core: stream separation / declared R′), K35 (core: Ẑ_r unbiased), K36 (core: Markov 0.05·Ẑ bound, output-event clause), K50 (core: pooled product not unbiased (B puts it in V+ (e), B:85)), K20 (cited (N9)), K21 (cited (N9)), K08 (cited (N9)), K47 (cited: fixed-grid N → ∞ convergence), K51 (H (b)–(f)), K52 (H (b): finite-R bound), K48 (H (e): SLLN in R), K62 (H: MPM margin transfer).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K46** `R0_DIFF:140` · class CONFIRMED-DE · For every island and measured round E[Ẑ_r·PIP̂_rj] = Z·PIP_j (Rao–Blackwell record before the Gibbs draw, at any random position) and E[Ẑ_r·H_r(h)] = Z·π(h) for bounded h measurable in (X, y, 𝓒).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)) [IDX 60; REG 260]; T26-Lemmas2-3: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED (A-REV4)) [IDX 149; REG 273]; N1: PROOF SKETCH; PC1 claim 3 takes it as a premise [INP 131]; PC1c3: PROVED (PC1 claim 3); 'E[W_r ĥ_r] = π(h) is still a premise' [IDX 114]
  - `Prop2(a,b,d,e)` — XF-ADVERSE:GAP (SF verified) (IDX:60)
  - `T26-Lemmas2-3` — XF-VERIFIED (IDX:149)
  - `PC1c3` — XF (IDX:114)
- **K32** `R0_DIFF:116` · class CONFIRMED-DE · Every final-run identity holds conditionally on any successful frozen calibration record (grid, tier, N, L, budgets) independent of the final streams, whereas an adaptively chosen schedule used directly would bias Ẑ.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T12: PROVED-LOCKED (THEOREM_LIST.md V1(iii); THM-INV §1 row 9) [IDX 68]; T31(i): PROVED-LOCKED (THEOREM_LIST.md V1(iii)) [IDX 69]; IND-T: PROVED (SF: none (authored by W2-PREM); XF: VERIFIED* (A-REV1)) [IDX 85; REG 190]; LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)) [IDX 127; REG 258]; N5(a): assembly of these [INP 160]
  - `LemmaRO` — XF-VERIFIED*(qualified) (IDX:127)
  - `T31(i)` — XF (IDX:69)
  - `IND-T` — XF-VERIFIED*(qualified) (IDX:85)
  - `T12` — XF (IDX:68)
- **K86** `R0_DIFF:195` · class CONFIRMED-DE · Final streams 10..9+R are independent of the calibration streams 0–9 and of each other, so every identity holds conditionally on calibration (stream separation).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). IND-T: PROVED (SF: none (authored by W2-PREM); XF: VERIFIED* (A-REV1)) [IDX 85; REG 190]; Lemma-STREAM: PROVED (SF: none (authored by W5-LOCKBOOK); XF: none) [IDX 86; REG 365]
  - `Lemma-STREAM` — FLAG AUTHOR-ONLY (IDX:86)
  - `IND-T` — XF-VERIFIED*(qualified) (IDX:85)
- **K35** `R0_DIFF:124` · class CONFIRMED-DE · Each island’s Ẑ_r is unbiased for Z (the evidence identity Z = m(∅)Z̄₀∏E[e^{Δφ·d}] counts W_K once) for every frozen grid, every N ≥ 1 and any invariant move kernels.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T12: PROVED-LOCKED (THEOREM_LIST.md V1(iii); THM-INV §1 row 9) [IDX 68]; T31(i): PROVED-LOCKED (THEOREM_LIST.md V1(iii)) [IDX 69]; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)) [IDX 60; REG 260]
  - `Prop2(a,b,d,e)` — XF-ADVERSE:GAP (SF verified) (IDX:60)
  - `T31(i)` — XF (IDX:69)
  - `T12` — XF (IDX:68)
- **K36** `R0_DIFF:125` · class CONFIRMED-DE · P(0.05·Ẑ > Z) ≤ 0.05 by Markov, and the average Ẑ̄ over R declared islands gives P(α·Ẑ̄ > Z) ≤ α.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T31(i): PROVED-LOCKED (THEOREM_LIST.md V1(iii)) [IDX 69]; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT) [INP 170]; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)) [IDX 60; REG 260]
  - `Prop2(a,b,d,e)` — XF-ADVERSE:GAP (SF verified) (IDX:60)
  - `T31(i)` — XF (IDX:69)
- **K50** `R0_DIFF:144` · class CONFIRMED-E · The product Ẑ̄·PIP^eq is not unbiased: E[Ẑ̄·PIP^eq_j] − Z·PIP_j = −(1−1/R)·Cov(Ẑ₁, PIP̂_1j | 𝓒).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). Prop2(c): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED (A-REV4)) [IDX 61; REG 261]; MA-PropP: PROVED (elementary) [IDX 70]; REG retired: “‘E[Ẑ | completed] = Z’ and ‘pooled Ẑ × pooled PIP is unbiased’ — both false (CEX-guard, Prop2(c))” [REG 818; IDX 1123]
  - `CEX-guard` — XF-VERIFIED*(qualified) (IDX:128)
  - `Prop2(c)` — XF-VERIFIED (IDX:61)
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **K20** `R0_DIFF:99` · class CONFIRMED-DE · The Gibbs flip (with cap), uniform swap, neighbour swap (Hastings ratio |N(j)∖S|/|N(l)∖S′|) and the π₀-independence step are each reversible with respect to q_φ at every φ.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]; V1(iii): V5 “has no registry row” [LST 77]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K21** `R0_DIFF:100` · class CONFIRMED-DE · The uniformly-random-order round kernel is q_φ-invariant and self-adjoint on L²(q_φ), so the bridge is a Feynman–Kac model with multinomial resampling.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]; V1(iii): V5 “has no registry row” [LST 77]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K08** `R0_DIFF:82` · class NEW-DE · The start normaliser Z̄₀ is computed exactly by size convolution and a backward sampler returns iid draws from π₀, invariant to block packing order.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N9: “by construction, consultant-checked, no registry row” [INP 192]; T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K47** `R0_DIFF:141` · class CONFIRMED-DE · At a fixed grid and R, Ẑ_r, PIP̂_rj and H_r(h) converge to Z, PIP_j, π(h) as N → ∞.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). ADRAFT-ThmA: PROVED (SF: VERIFIED* (A-REV4); XF: none) [IDX 62; REG 372]; ADRAFT-CorA1: PROVED (SF: VERIFIED* (A-REV4); XF: none) [IDX 63; REG 373]
  - `ADRAFT-CorA1` — ASTRA-ONLY (Astra-on-Astra; XF none) (IDX:63)
  - `ADRAFT-ThmA` — ASTRA-ONLY (Astra-on-Astra; XF none) (IDX:62)
- **K51** `R0_DIFF:145` · class DRAFT-ONLY · For any bounded h the Ẑ-weighted estimate is within 2δ₁ + c_h(ρ̄+u_π) of h(S₀) in W-weighted mean on every island, regime and frozen grid, with pooled tail bound exp{−R(1−s)²/(2E[W²])} + ε/(st).
  - *R0_DIFF status cell (verbatim):* A1new: PROOF SKETCH (NEW-SYNTH; 'this run; it is M1 + Prop P(iii) with h in place of the PIP') [IDX 155]; FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 107; REG 570]; FMP-M3: PROVED (SF: none; XF: ERROR (A-REV9)) [IDX 148; REG 572]
  - `FMP-M1` — XF-VERIFIED (IDX:107)
  - `FMP-M3` — XF-ADVERSE:ERROR (no clean SF) (IDX:148)
  - `A1new` — FLAG AUTHOR-ONLY (IDX:155)
- **K52** `R0_DIFF:146` · class NEW-DE · At finite R the Ẑ-weighted estimate satisfies P(|μ̂ − π(h)| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)} with M = E[(Ẑ_r/Z)²|𝓒]; E gives the analogue with M replaced by C_T/N.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). PC1c3: PROVED (PC1 claim 3); 'E[W_r ĥ_r] = π(h) is still a premise' [IDX 114]; N4(i): PROVED, given N1 for general h [INP 152]
  - `PC1c3` — XF (IDX:114)
- **K48** `R0_DIFF:142` · class CONFIRMED-DE · At fixed N the Ẑ-weighted pooled estimate Σ_rẐ_rĥ_r/Σ_rẐ_r converges a.s. to π(h) as R → ∞ (SLLN on unbiased numerators).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropP: PROVED (elementary) [IDX 70]; V3 draft status: PROVED (candidate, elementary; (iii) uses F-MASKPIP M1, XF VERIFIED A-REV9) [LST 23]
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **K62** `R0_DIFF:156` · class NEW-E · If every exact PIP is at least δ from ½ and the estimated PIPs err uniformly by less than δ, the reported MPM equals the exact MPM.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `PC1c2` — XF (IDX:187)
- `T03♯` — XF-VERIFIED (IDX:151)

**Seat card status (verbatim):**

- A:46 — T12: PROVED-LOCKED [IDX 68]; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N9K: PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT (registry row to be opened); N1: PROOF SKETCH [INP 131]; IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); streams 10..9+R′ audit pending; LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)); CEX-guard: COUNTEREXAMPLE.
- A:56 — A1new: PROOF SKETCH (NEW-SYNTH) [IDX 155]; FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), 'E[W_r ĥ_r] = π(h) is still a premise'; N1: PROOF SKETCH; (f): TRUE-AS-WRITTEN (PC1:120), this seat, unchecked; (g): PROVED (by this seat, unchecked), composition.
- B:87 — T12, T31(i): PROVED-LOCKED; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)); N1: PROOF SKETCH; N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); IND-T: PROVED (SF: none; XF: VERIFIED* (A-REV1)); PC1c2: PROVED for the potential run, output form CORRECT WITH AMENDMENT.
- B:97 — A1new: PROOF SKETCH (NEW-SYNTH); FMP-M1: PROVED (SF: none; XF: VERIFIED (A-REV9)); PC1c3: PROVED (PC1 claim 3), "E[W_r ĥ_r] = π(h) is still a premise"; MA-PropP: PROVED (elementary), author-only; T03♯ as in S2.
- C:72 — N1: **PROOF SKETCH**. PC1c3: **PROVED**, taking N1 as premise. FMP-M1: **PROVED; SF none; XF VERIFIED (A-REV9)**. Assembly: **PROOF SKETCH, unchecked**.
- D:58 — Status: N9K "PROVED (candidate)" + CHK §5 "VERIFIED WITH AMENDMENT"; T12, T31(i) "PROVED-LOCKED"; Prop2(a,b,d,e) "PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4))"; N1 "PROOF SKETCH"; PC1c3 "PROVED (PC1 claim 3)" with E[W_r ĥ_r] = π(h) a premise; FMP-M1 "PROVED (SF: none; XF: VERIFIED (A-REV9))"; A1new "PROOF SKETCH (NEW-SYNTH)"; MA-PropP "PROVED (elementary)"; IND-T "PROVED (SF: none; XF: VERIFIED* (A-REV1))"; (d′), (f) PROVED (by this seat, unchecked).

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :109 `A.C2(a); B.D1 kernels; D.M1(a)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :110 `A.C2(b,c); B.D1 identities; D.M1(b)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :111 `B.D1 final clause` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :112 `D.M1(c)` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :118 `A.C5(a,b,b′,c); B.D2(a–e); D.M2(a,b,c-joint,e)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :119 `A.C5(d); B.D2(f); D.M2(d)` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / GAP; :120 `A.C5(e); D.M2(c)-interval` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :101 `D1 · general-h identity (N1)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :102 `D1 · RB marginal records` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :103 `D1 · finite-R ratio bound (PC1c3)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :104 `D1 · class union + truth anchor` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :105 `D1 · MPM margin transfer (K62, E:T28)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :106 `D1 · IC3` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :92 `A.M1 · V+` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :93 `A.M2(a)–(f) · H` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :94 `A.M2(g) · H` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :106 `B.M1(b) · V+ RB wording` — AMBIGUOUS / DESIGN-ASSERTED / GAP / REPAIRED DIFFERENTLY; :107 `B.M1(a),(c)–(e) · V+` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :108 `B.M2 · H` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :120 `D.H′(a)–(c),(e),(f)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :121 `D.H′(d′)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY
- `W2_PC2` — :121 `C1 (K46…) · unchanged clauses` — as W1 (TRUE) / as W1 / as W1; :122 `C1 · repair: vacuous at R′ = 4` — REPAIRED; :123 `C1 · repair: stacking rate` — REPAIRED; :124 `C1 · IC3` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :168 `C1/H · R′_n = 4⌈s⁶/4⌉, s = n + p` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `CHK_INHERITED/REPORT.md:15` — N9-KERNEL §§0–3 **VERIFIED WITH AMENDMENT** (section verdict at CHK:134: claims G, U, N, I, R, Z, S check against code at the named commit; prose corrections CHK:155–161 adopted by A:44 and B:86). This is a statement/code check, not a registry status change; registry N9K stays `PROVED (candidate)`.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 16, TRUE 5, AMBIGUOUS 2, (repair-only or blank row) 2, as W1 (TRUE) 1.

*Adverse rows:* W1_PC1:112 (D.M1(c): AMBIGUOUS, DESIGN-VERIFIED, GAP); W1_PC1:119 (A.C5(d); B.D2(f); D.M2(d): TRUE-AS-WRITTEN, DESIGN-ASSERTED, GAP); W2_PC1:106 (B.M1(b) · V+ RB wording: AMBIGUOUS, DESIGN-ASSERTED, GAP, REPAIRED DIFFERENTLY).

**Lean:** `T12Core.lean` (`invariance_step`, `resample_move_step`, `unbiased_of_step`): 0 `sorry` in code, **PARTIAL** — the resample–move recursion `hstep` is an explicit hypothesis (L-LEAN STATUS.md row T12(i.a); REGISTRY_INDEX.md:929, §3.4). No Lean file for N1 itself, for N9 kernels, for the ratio bound or for the declared-R′ clauses. Cards name `T12Core.lean`/`hstep` as the Lean core (A:48, C:75, D:61).

**Fidelity to v3.1 as shipped:**
- LS0: n/a — LS0 not used by V1 (REGISTRY_INDEX.md:55); LS0 integration is separate (METHOD:48, 399).
- Coded grid: yes in statement: conditional on any frozen 𝒞 incl. the coded grid (A:44(d); METHOD:170 #18). Ẑ-weighted H clauses (b)–(c) are about the shipped estimator (METHOD:158–159).
- Ẑ-weighted pooling / partition: yes: μ̂(h)=Σ_rẐ_rH_r(h)/Σ_rẐ_r is the primary estimator (METHOD:158 #11, :159 #12). Accumulator H_r(h) is 'adopted text' (METHOD:159); whether it is coded: unknown (METHOD:45 lists full v3.1 records as not yet produced).

**Notes (with sources):**

- N1 (K46 general-h identity) is a binding obligation: PROOF SKETCH [INP 131]; PC1c3 takes it as a premise (R0_DIFF:140). Fallback if N1 fails: marginal records and fixed finite classes, and §13.1 escalates to HQ (S2:246).
- H (b) is vacuous at the shipped R′ = 4 (W2PC2:74; W2PC1 growth rows 215, 221); informative only under stacking (S2:238–242).
- H (g)/(d′)/(f) growth clause: A:54(g), B:95(f), D:56(d′); uses M₂ ≤ e^{osc d} from M2 (b)(iv) — see edge M2 → M1.

### M2 — Theorem WS — the §5.3 package (parts (a) discrepancy, (b) bridge-form stability, (c) one-shot refutation)

**Round 3 resolution (MINUTES §2.1, §2.2; R3-5 unanimous):** B's leakage clauses (F),(S) go to the supplement as corollary **S-LEAK**, not inside M2 (R3_B:142, :173). Part (b) carries the HQ Q5 stage-count content (sandwich + local constancy + continuous envelope) and the step-function statement of T (PC1's example {2,4} → 3 at ε = 10⁻⁵). Part (c) is Proposition ONE-SHOT (WS6(d), WS7 with the CHK amendments). K-IDs: K102, K10, K11, K25, K53; K103/K104 as used; K17, K105, K19 are used by (c) (M3, M6). Final card: `R3_B.md` §S2 M2. Disclosed scale: useful constants need ε ≲ n^{−1/2}/p on the exhibited family (MINUTES §3); a sharp necessity statement is FUTURE_WORK. Safeguard (binding §5.3): if both the D_* route and the correlated-family route fail, it escalates (MINUTES §2.3).

**HQ:** wave 2 · HQ `M2` · charter `HQ_CHARTERS/M2.md` (`R3_B.md` §S3(c)). Inputs: d_σ from M3, the count from M7, the lower bound from M6 (MINUTES §2.5). Premises: none of §8 is assigned to M2 by a seat.

**Seat cards (R2):** A:60–73 (M3 WS-ε card; §R3 A:151–188); B:101–103 (M3 → §R3 B:209–228); C:79–81 (C2 → §R3 C:259–288); D:77 (WS′ → §R3 D:118–146).

**K-IDs in this item:** K102 (core: weight stability (HQ Q1 package)), K10 (core: σ²-coupling, d = d_σ + d_X (OWS-WS3 in cards)), K11 (core: cross-block bound |d_X| ≤ b_X (OWS-WS4 in cards)), K25 (core: restricted/full ESS coverage identity), K53 (core: variance bounds / pathwise M₂ ≤ e^{D_*}), K103 (as used: Doeblin/minorisation constants), K104 (as used: exponential-family / KL–TV calculus), K17 (used by (c): masking law (WS7)), K105 (used by (c): KL lower bound (WS7(a))), K19 (used by (c): iid miss (C6 obstruction, C:263)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K102** `R0_DIFF:226` · class CONFIRMED-DE · Weight variance (incremental ESS/χ²) stays bounded under weak non-zero cross-block dependence for the actual block product with common noise integration (proposal §5.3, binding).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). S4 draft status: “O-WSTAB WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED under H-ORTH and an ideal grid; WS6e CONJECTURE, WS8d OPEN; FD-W(a) PROVED-UNDER, (b) PROOF SKETCH, (c) CONJECTURE” [LST 503–504]; OWS-WS6e: CONJECTURE (SF: none; XF: none) [IDX 412; REG 528]; OWS-WS8d: OPEN (SF: none; XF: none) [IDX 415; REG 531]; AREV9-OWSTAB: O-WSTAB W(a), W(b), W(c), W(d), W(e), W(f): 'VERIFIED under H-ORTH exactly as stated, including W(d)'s stronger upper-side premise'; O-WSTAB W prime: 'VERIFIED ideal full… [IDX 423]; FD-W2 (PROVED-UNDER): “XF: **ERROR** — A-REV4 · REVIEW.md verdict table: F-DRAFT W2 ERROR with an explicit feasible counterexample (n = 20, p = 4, G = 19I, blocks {1,3},{2,4}, S° = {1}, l = 2, ‖y‖² = 19, z² = (100,30,0,0): actual v3 log-odds difference…” [IDX 1030; REG 386]
  - `AREV9-OWSTAB` — XF (IDX:423)
  - `OWS-WS6e` — FLAG AUTHOR-ONLY (IDX:412)
  - `OWS-WS8d` — FLAG AUTHOR-ONLY (IDX:415)
  - `FD-W(a)` — FLAG AUTHOR-ONLY (IDX:417)
- **K10** `R0_DIFF:84` · class NEW-DE · Even with exactly orthogonal blocks the block-product start is wrong: d(S) = d_σ(S) ≥ 0, d_σ = −ν[log(1−Σu_b) − Σlog(1−u_b)], zero only if at most one block of S is active.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row found in the index for this decomposition. Nearest (a different identity): DIL-E: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 328; REG 709]
  - `DIL-E` — XF-VERIFIED (IDX:328)
- **K11** `R0_DIFF:85` · class NEW-DE · For cross-block correlation at most ε (or small relative operator norm), |d_X(S)| is bounded explicitly, linearly in ε through k·log(1+2kε/κ) and an n·R² fit term.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K25** `R0_DIFF:109` · class NEW-DE · The stage ESS fraction is 1/(1+χ²), and the full ESS equals the restricted-set ESS times the exact coverage factor a_u·a_w/a_v² (a_t = q_t(V), w = 2v−u), so a restricted ESS ≥ 0.9 certifies the full bridge only up to the missing m…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N5(b2) OPEN [INP 161]; INP I9(d) [INP 274]
  - no registry/index ID is named in the cell
- **K53** `R0_DIFF:147` · class NEW-DE · Without design conditions Var(Ẑ_r/Z|𝓒) ≤ C_T/N with C_T = (T+1)e^{2D}; with Dobrushin/minorisation constants or a semigroup-stability condition the factors become explicit or O(T/N), which would bound the weight second moment M.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N4(iii): OPEN/CONJECTURE (V11 “resolved grid ⇒ O_P(√(T/N))”); lower bound M ≳ 1/P_𝓒(cross) PROOF SKETCH [INP 154]; FMP-M3: PROVED (SF: none; XF: ERROR (A-REV9)) [IDX 148; REG 572]
  - `FMP-M3` — XF-ADVERSE:ERROR (no clean SF) (IDX:148)
- **K103** `R0_DIFF:232` · class NEW-DE · The independence step minorises every round, Q_φ(S,·) ≥ π_φ/(mM_φ) (D) or ≥ π_φ/M_φ (E), with M_φ ≤ exp{φ(d_max − E_{π₀}d)}, so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1−ε_φ)^k and the L terminal rounds have an explicit TV bound.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N10: NONE / OPEN (INV row 6) [INP 199].
  - no registry/index ID is named in the cell
- **K104** `R0_DIFF:233` · class NEW-DE · π_φ is an exponential family in d: (log Z_φ)′ = E d, (log Z_φ)″ = Var d, log(Z/(m(∅)Z̄₀)) = ∫E_{π_φ}d, KL(π‖π₀) + KL(π₀‖π) = J = ∫Var_{π_φ}(d)dφ, J = 0 iff π₀ = π, and Λ ≤ √J.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K17** `R0_DIFF:91` · class CONFIRMED-DE · On masked designs (true variables cancel along an addition chain) the start mass of S₀ is p^{−c}n^{−c/2}e^{O_P(1)}, so iid starts miss it.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T27(i): PROVED-LOCKED, CONDITIONAL (THEOREM_LIST.md S1(iii)) [IDX 339]; Thm3-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)) [IDX 321; REG 174]; Thm4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)) [IDX 322; REG 175]
  - `Thm3-EXP` — XF-VERIFIED (IDX:321)
  - `Thm4-EXP` — XF-VERIFIED (IDX:322)
  - `T27(i)` — XF (IDX:339)
- **K105** `R0_DIFF:234` · class DRAFT-ONLY · KL(π‖π₀) ≥ (1−δ₁)·log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size exp(KL) is at least ½·Q*^{1−δ₁}·e^{O_P(1)}.
  - *R0_DIFF status cell (verbatim):* KL: PROOF SKETCH (NEW-SYNTH: 'PROOF SKETCH only because unreviewed; the inequality is two lines') [IDX 369]
  - `KL` — FLAG AUTHOR-ONLY (IDX:369)
- **K19** `R0_DIFF:93` · class CONFIRMED-DE · If Q independent π₀ draws are scored, the chance of never scoring a target model (or the HPM S*) is (1−π₀(·))^Q ≤ exp(−Qπ₀(S*)); on LH it switches sharply at Q* = p^c·n^{c/2}.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). SEP-A: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 352; REG 641]; SEP-A-iid: PROVED-UNDER (SF: none; XF: none) [IDX 353; REG 642]; T38-(a): PROVED-UNDER (SF: VERIFIED* (inputs); XF: none) [IDX 548; REG 325]
  - `SEP-A-iid` — FLAG AUTHOR-ONLY (IDX:353)
  - `T38-(a)` — FLAG SAME-FAMILY-ONLY (IDX:548)
  - `SEP-A` — XF-VERIFIED (IDX:352)

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `OWS-WS1` — FLAG AUTHOR-ONLY (IDX:402)
- `OWS-WS3` — FLAG AUTHOR-ONLY (IDX:404)
- `OWS-WS4` — FLAG AUTHOR-ONLY (IDX:405)
- `FD-W1` — XF-VERIFIED (IDX:416)
- `OWS-WS53F` — FLAG AUTHOR-ONLY (IDX:407)
- `OWS-WS6d` — FLAG AUTHOR-ONLY (IDX:411)
- `OWS-WS7` — FLAG AUTHOR-ONLY (IDX:413)

**Seat card status (verbatim):**

- A:68 — OWS-WS3, OWS-WS4: PROVED (SF: none; XF: none) [REG 520–521]; CHK_INHERITED: "VERIFIED (PC1, cross-family, line by line)" (CHK:13–14; registry rows not yet updated). OWS-WS1/WS2: PROVED (no review). OWS-WS6(d), WS7: PROVED (SF: none; XF: none); CHK_INHERITED: VERIFIED WITH AMENDMENT (CHK:11–12). FD-W1: PROVED, XF VERIFIED (A-REV4). AREV9-OWSTAB W(a)–(f): VERIFIED under H-ORTH only. C.D14 pathwise/M₂ clause: PROOF SKETCH (Seat C), TRUE-AS-WRITTEN (PC2:123–125). D.M10(ii),(iv): TRUE-AS-WRITTEN (PC1:149). (b)(ii),(iii), (N-d): PROVED (by this seat, unchecked).
- B:215 — (a1) OWS-WS3: PROVED (SF: none; XF: none) + CHK_INHERITED §3 VERIFIED (PC1, cross-family, line by line); FD-W1: PROVED, XF VERIFIED (A-REV4). (a2) Seat C D14: PROOF SKETCH (NEW-COMP), PC2 cluster 4 "D14 · deterministic bound" TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE (Appendix A route); my check 1 on Dε. (a3) PC2 "D14 · one-shot"; PC1 §16 rows (TI identity; KL ≤ osc d; TV ≤ tanh) TRUE-AS-WRITTEN. (a4) OWS-WS4: PROVED (SF: none; XF: none) + CHK_INHERITED §4 VERIFIED; PC1 §4 A.C9(a,b) TRUE on Dε.
- B:216 — (b1) PC1 §4 D.M10(ii), A.C9(b) TRUE-AS-WRITTEN on Dε; WS4(e) VERIFIED. (b2) PC1 D.M10(iii) COUNTEREXAMPLE repaired to this order. (b3) D.M10(iv) TRUE. (b4) A.C9(c) first equality TRUE; "hence within" COUNTEREXAMPLE repaired (transfer 1 + N_e Var). (b5) PC2 "D14 · one-shot / increment χ²" and "D14 · actual-grid moment" TRUE / DESIGN-VERIFIED (1,600 islands, good and poor V); OWS-WS6(b): PROVED (SF: none; XF: none), PC1 B.D6(S) TRUE; the m lower bound: PROVED (by this seat, unchecked; q₂(S₀)/π₀(S₀) = e^{2d(S₀)}/E_{π₀}e^{2d}). (b6) OWS-WS53F: PROVED-UNDER (SF: none; XF: none); PC1 B.D6(F) TRUE / DESIGN-VERIFIED (D_B). (b1)–(b4) are Seats A/D: PROVED (by that seat, unchecked).
- B:217 — OWS-WS6d, OWS-WS7: PROVED (SF: none; XF: none) + CHK_INHERITED §1, §2, §6 VERIFIED WITH AMENDMENT (PC1, cross-family): amendments above adopted verbatim; T03: PROVED-LOCKED; T27(i): PROVED-LOCKED, CONDITIONAL.
- C:265 — New assembly: **PROOF SKETCH, unchecked**. OWS-WS3/4/6d/7 registry: **PROVED; AUTHOR-ONLY; SF none; XF none**. New filed CHK verdicts: WS3/4 **VERIFIED**; WS6d/7 **VERIFIED WITH AMENDMENT**. These are separate review entries.
- D:140 — Status: OWS-WS3, OWS-WS4 "PROVED (SF: none; XF: none)" + CHK "VERIFIED (PC1, cross-family, line by line)"; OWS-WS6d, OWS-WS7 "PROVED (SF: none; XF: none)" + CHK "VERIFIED WITH AMENDMENT"; OWS-WS1 "PROVED" AUTHOR-ONLY; FD-W1 "PROVED (SF: none; XF: VERIFIED (A-REV4))"; AREV9-OWSTAB W(a–f) "VERIFIED under H-ORTH exactly as stated"; C's D_* bound PROOF SKETCH (PC2 TRUE-AS-WRITTEN); (b)(i)–(v) PROVED (by this seat, unchecked), (i),(ii),(iv) TRUE-AS-WRITTEN on Dε (PC1 cluster 4); OWS-WS6e "CONJECTURE"; OWS-WS8d "OPEN".

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :136 `A.C9(a,b); §E(a,b)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :137 `A.C9(c), first equality` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :138 `A.C9(c), “hence within”` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :139 `A.C9(d), comparison` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :140 `A.C9(d), uniform grid` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :141 `A.C9(e)` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :142 `A.C9 named IC3/numerical companion` — NEEDS-HYPOTHESIS / DESIGN-FAILS / PLAUSIBLE; :143 `B.D6(F)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :144 `B.D6(S)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :145 `B.D6 route/new q₂ lemma` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / IMPLAUSIBLE; :146 `B.D6(O); A.§E obstruction paragraphs` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :147 `B.D6(N)` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :148 `B.D6 local numerical check` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :149 `D.M10(i,ii,iv), §E` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :150 `D.M10(iii); D.M11(b)` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :151 `D.M10(v)` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / GAP; :152 `D.M10 named exhibit and numerical claims` — NEEDS-HYPOTHESIS / DESIGN-FAILS / PLAUSIBLE
- `W1_PC2` — :123 `D14 · deterministic bound` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :124 `D14 · one-shot / increment χ²` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :125 `D14 · actual-grid moment` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :126 `D14 · §E rates` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :127 `D14 · groups = blocks (§E)` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :128 `D14 · grid gap disappears` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :129 `D14 · budget consequence` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :130 `D14 · statuses` — consistent w
- `W2_PC1` — :53 `A.R3(a)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :54 `A.R3(b)(i),(ii),(v)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :55 `A.R3(b)(iii) · sandwich` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :56 `A.R3(b)(iii) · zero range` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :57 `A.R3(b)(iv) / guarantee` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / GAP / REPAIRED DIFFERENTLY; :58 `A.R3(c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :59 `A.R3 · N-d` — COUNTEREXAMPLE / DESIGN-VERIFIED / GAP; :60 `A.R3 · scale / growth exhibit` — NEEDS-HYPOTHESIS / DESIGN-FAILS / PLAUSIBLE / REPAIRED; :61 `A.R3 · IC3 / scripts` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :67 `B.R3(a)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :68 `B.R3(b)(1)–(4)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :69 `B.R3(b) · continuity sentence` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :70 `B.R3(b)(5),(6)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :71 `B.R3(c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :72 `B.R3 · NEC` — COUNTEREXAMPLE / DESIGN-VERIFIED / GAP; :73 `B.R3 · scale / IC3` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :79 `D.R3(a)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :80 `D.R3(b)(i),(ii),(iv)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :81 `D.R3(b)(iii) · sandwich` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :82 `D.R3(b)(iii) · jump corollary` — COUNTEREXAMPLE / DESIGN-VERIFIED / IMPLAUSIBLE; :83 `D.R3(b)(v)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :84 `D.R3(c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :85 `D.R3 · NEC` — COUNTEREXAMPLE / DESIGN-VERIFIED / GAP; :86 `D.R3 · scale / IC3` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :101 `C2(a) · split` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :102 `C2(a) · divergences` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :103 `C2(b) · increments` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :104 `C2(b) · weights` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :105 `C2(b) · stage count` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :106 `C2(b) · continuity` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :107 `C2(c) · one-shot refutation` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :108 `C2 · ε-scale` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :109 `C2 · IC3 W` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :110 `C2 · variance transfer` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :111 `C2 · necessity route` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :112 `C2 · not supplied` — n/a / n/a / n/a; :113 `C2 · statuses` — verbatim ✓ ( / REPAIRED
- `CHK_INHERITED/REPORT.md:13` — OWS-WS3 **VERIFIED** ('VERIFIED (PC1, cross-family, line by line)'; section verdict CHK:93).
- `CHK_INHERITED/REPORT.md:14` — OWS-WS4 **VERIFIED** (same wording; section verdict CHK:112).
- `CHK_INHERITED/REPORT.md:11` — OWS-WS6(d) **VERIFIED WITH AMENDMENT** (bounded-block TV scope; section verdict CHK:34).
- `CHK_INHERITED/REPORT.md:12` — OWS-WS7 **VERIFIED WITH AMENDMENT** (initial vs later presence; restricted-set stage count; section verdict CHK:70).
- `CHK_INHERITED/REPORT.md:177–195` §6 — one-shot refutation survives in the shipped bounded-block setting (HQ Q1(c) met; S2:29). These CHK verdicts are review entries; registry rows OWS-* still read `PROVED (SF: none; XF: none)`.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 33, NEEDS-HYPOTHESIS 9, COUNTEREXAMPLE 8, TRUE 7, AMBIGUOUS 2, consistent w 1, n/a 1, verbatim ✓ ( 1.

*Adverse rows:* W1_PC1:138 (A.C9(c), “hence within”: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:139 (A.C9(d), comparison: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:140 (A.C9(d), uniform grid: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:141 (A.C9(e): AMBIGUOUS, DESIGN-VERIFIED, GAP); W1_PC1:142 (A.C9 named IC3/numerical companion: NEEDS-HYPOTHESIS, DESIGN-FAILS, PLAUSIBLE); W1_PC1:145 (B.D6 route/new q₂ lemma: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, IMPLAUSIBLE); W1_PC1:146 (B.D6(O); A.§E obstruction paragraphs: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:147 (B.D6(N): COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:148 (B.D6 local numerical check: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:150 (D.M10(iii); D.M11(b): COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:151 (D.M10(v): NEEDS-HYPOTHESIS, DESIGN-VERIFIED, GAP); W1_PC1:152 (D.M10 named exhibit and numerical claims: NEEDS-HYPOTHESIS, DESIGN-FAILS, PLAUSIBLE); W1_PC2:127 (D14 · groups = blocks (§E): AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W2_PC1:56 (A.R3(b)(iii) · zero range: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE, REPAIRED); W2_PC1:57 (A.R3(b)(iv) / guarantee: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, GAP, REPAIRED DIFFERENTLY); W2_PC1:59 (A.R3 · N-d: COUNTEREXAMPLE, DESIGN-VERIFIED, GAP); W2_PC1:60 (A.R3 · scale / growth exhibit: NEEDS-HYPOTHESIS, DESIGN-FAILS, PLAUSIBLE, REPAIRED); W2_PC1:69 (B.R3(b) · continuity sentence: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE, REPAIRED); W2_PC1:72 (B.R3 · NEC: COUNTEREXAMPLE, DESIGN-VERIFIED, GAP); W2_PC1:82 (D.R3(b)(iii) · jump corollary: COUNTEREXAMPLE, DESIGN-VERIFIED, IMPLAUSIBLE); W2_PC1:85 (D.R3 · NEC: COUNTEREXAMPLE, DESIGN-VERIFIED, GAP).

**Lean:** No existing Lean file. Proposed cores only: WS3(c) scalar inequalities, WS4(b)–(d) given the Loewner sandwich, four-normaliser identity, pathwise W bounds (A:71; B:224; C:266; D:141).

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: partial: pathwise W ∈ [e^{−D_*}, e^{D_*}] and M₂ ≤ e^{D_*} are stated for every successful coded grid with kernels as coded and were run on a coded-grid replica (W1PC2:125; W2PC2:104); the stage-count sandwich T_bd(.9e^{−4η}) ≤ T ≤ T_bd(.9e^{4η}) is for **exact frontiers** with a coded caveat (2^{−60} bisection, 10^{−12} snap) (W2PC1:55, 81; S2:131–136); the envelope T ≤ 2⌈D_*/c_ρ⌉+2 was run against the coded pilot, 600 runs (W2PC2:105, 156).
- Ẑ-weighted pooling / partition: yes for the island moment M₂ = E[W_r²|𝒞] (W_r = Ẑ_r/Z, C:52). Partition: the IC3 exhibit uses the method's own computed partition (W2PC2 §0 item 3, scripts w_family.py).

**Notes (with sources):**

- Hypotheses (S2:108–120): C's computational specification A (C:50), matrix domain a, δ_A, δ_H, r < 1 (C:64). Useful constants need ε ≲ n^{−1/2}/p with signal energy O(√n) (W2PC2:60; scale disclosure, not a theorem; S2:158–160).
- Q5 condition (1): continuity/Lipschitz statements in ε on the fixed-partition family; condition (2): T(ε) is a step function that can jump (PC1 example {2,4} → 3 at ε = 10⁻⁵; W2PC1:82). Both are to be written (S2:143–146).
- Removed by W2PC1: A's zero-range clause (use max{1,·}), D's two-value jump corollary, B's 'every constant tends to its BO value' for T, A's growth exhibit; all necessity propositions (A.N-d W2PC1:59, B.NEC :72, D.NEC :85) are COUNTEREXAMPLE as stated. C's range-obstruction route is TRUE-AS-WRITTEN as a prediction only (W2PC2:111–112).
- K10/K11: R0_DIFF says 'No registry row' (R0_DIFF:84, :85); the R2 cards cite registry rows OWS-WS3/OWS-WS4 (A:68; B:215; D:140). Source disagreement — see §Status disagreements.
- IC3: SMC-dispatched exhibit = C's family (groups of nine, n ≥ 9⁶; ε = 1/(np) b_X ≈ 5·10⁻⁴–3·10⁻⁵; ε = n^{−1/2}/p b_X ≈ 0.35, D_* ≈ 1.73–1.90) (W2PC2:109, S2:42–46); A/B/D finite exhibits are component checks only (production dispatches the exact branch there; W2PC1:42).

### M3 — Theorem START — deterministic mass, σ²-coupling decomposition, masking law, dilution

**Round 3 resolution (MINUTES §2.1):** K16 is a supplementary clause of M3 (kept as a separate conditional citation: `R3_C.md` §S3 'M3 charter'). K-IDs: K15, K17, K18, K10 (K16 supplementary). Final card: `R3_C.md` §S2 M3.

**HQ:** wave 1 · HQ `M3` · charter `HQ_CHARTERS/M3.md` (`R3_C.md` §S3 'M3 charter'). Check flagged in the charter: Thm5-LH is SAME-FAMILY-ONLY (R3_C:297).

**Seat cards (R2):** A:75–83 (M4 START); B:105–113 (M4 Theorem 2); C:105–114 (C5); D:79 (M6 Theorem 2).

**K-IDs in this item:** K15 (core: π₀ mass bound, odds, bridge mass), K17 (core: masked law p^{−c}n^{−c/2}e^{O_P(1)}), K18 (core: dilution identity −log π₀(S₀)=V+C−log A), K10 (core: d = d_σ + d_X, σ²-coupling), K16 (supplementary clause: favourable rate).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K15** `R0_DIFF:89` · class DRAFT-ONLY · π₀ puts mass ≥ (1−q)^{s+1}/(1+e)^s on a reference model, the odds π₀(S₀)/π₀(S°) are exact, and the bridge never puts less mass on S₀ than min(π₀(S₀), π(S₀)).
  - *R0_DIFF status cell (verbatim):* T22(i)(ii)(iv): PROVED-LOCKED (THEOREM_LIST.md S1(iii)) [IDX 337]; S1 draft status [LST 33]
  - `T22(i)(ii)(iv)` — XF (IDX:337)
- **K17** `R0_DIFF:91` · class CONFIRMED-DE · On masked designs (true variables cancel along an addition chain) the start mass of S₀ is p^{−c}n^{−c/2}e^{O_P(1)}, so iid starts miss it.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T27(i): PROVED-LOCKED, CONDITIONAL (THEOREM_LIST.md S1(iii)) [IDX 339]; Thm3-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)) [IDX 321; REG 174]; Thm4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)) [IDX 322; REG 175]
  - `Thm3-EXP` — XF-VERIFIED (IDX:321)
  - `Thm4-EXP` — XF-VERIFIED (IDX:322)
  - `T27(i)` — XF (IDX:339)
- **K18** `R0_DIFF:92` · class DRAFT-ONLY · The dilution identity −log π₀(S₀) = V + C − log A holds for any data and partition (V: truths invisible to their own table).
  - *R0_DIFF status cell (verbatim):* DIL-E: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 328; REG 709]; DIL-E1: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 329; REG 710]; DIL-DM (PROVED): “XF: **ERROR** — A-REV9 · REVIEW.md: DM(i) size-sign ERROR (explicit construction)” [IDX 1039; REG 717]
  - `DIL-E1` — XF-VERIFIED*(qualified) (IDX:329)
  - `DIL-DM` — XF-ADVERSE:ERROR (no clean SF) (IDX:333)
  - `DIL-E` — XF-VERIFIED (IDX:328)
- **K10** `R0_DIFF:84` · class NEW-DE · Even with exactly orthogonal blocks the block-product start is wrong: d(S) = d_σ(S) ≥ 0, d_σ = −ν[log(1−Σu_b) − Σlog(1−u_b)], zero only if at most one block of S is active.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row found in the index for this decomposition. Nearest (a different identity): DIL-E: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 328; REG 709]
  - `DIL-E` — XF-VERIFIED (IDX:328)
- **K16** `R0_DIFF:90` · class DRAFT-ONLY · In the favourable regime 1 − π₀(S₀) → 0 at an explicit rate (O_P(2^B√log n·n^{−κ}) under EXP′, VIS, NL).
  - *R0_DIFF status cell (verbatim):* T22(iii): PROVED-LOCKED CONDITIONAL (THEOREM_LIST.md S1(iii)) [IDX 338]; EXP′: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED* (A-REV2)) [IDX 319; REG 168]; FAV-ThmA: PROVED (SF: none; XF: none) [IDX 326; REG 500]; FAV-ThmB: PROVED (SF: none; XF: none) [IDX 327; REG 503]
  - `FAV-ThmA` — FLAG AUTHOR-ONLY (IDX:326)
  - `FAV-ThmB` — FLAG AUTHOR-ONLY (IDX:327)
  - `T22(iii)` — XF (IDX:338)
  - `EXP′` — XF-VERIFIED*(qualified) (IDX:319)

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `Thm5-LH` — FLAG SAME-FAMILY-ONLY (IDX:325)
- `OWS-WS3` — FLAG AUTHOR-ONLY (IDX:404)
- `FD-W1` — XF-VERIFIED (IDX:416)
- `OWS-WS53F` — FLAG AUTHOR-ONLY (IDX:407)

**Seat card status (verbatim):**

- A:81 — T22(i)(ii)(iv): PROVED-LOCKED; T22(iii): PROVED-LOCKED CONDITIONAL; T27(i): PROVED-LOCKED, CONDITIONAL; Thm3-EXP/Thm4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none) (SAME-FAMILY-ONLY); DIL-E: PROVED (XF: VERIFIED (A-REV9)); OWS-WS3: PROVED (no review) + CHK VERIFIED (CHK:13); FD-W1: PROVED, XF VERIFIED.
- B:111 — T22(i)(ii)(iv): PROVED-LOCKED; T22(iii): PROVED-LOCKED CONDITIONAL; T27(i): PROVED-LOCKED, CONDITIONAL; Thm3/4-EXP: PROVED (SF: VERIFIED (W3-VEXP); XF: VERIFIED (A-REV2)); Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none) SAME-FAMILY-ONLY; DIL-E: PROVED (XF: VERIFIED (A-REV9)); OWS-WS3: PROVED (SF: none; XF: none) + CHK_INHERITED VERIFIED (PC1, cross-family); FD-W1: PROVED, XF VERIFIED (A-REV4); OWS-WS53F: PROVED-UNDER (SF: none; XF: none), PC1 B.D6(F) TRUE-AS-WRITTEN.
- C:109 — DIL-E: **PROVED; XF VERIFIED**. DIL-E1: **PROVED; XF VERIFIED***. T27(i): **PROVED-LOCKED, CONDITIONAL**. Thm3/4-EXP: **PROVED; SF VERIFIED (W3-VEXP); XF VERIFIED (A-REV2)**. Thm5-LH: **PROVED; SF VERIFIED (W3-VEXP); XF none; SAME-FAMILY-ONLY**.

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :158 `A.C8(a–e); B.D4(a–e); D.M6(a–e)` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :159 `A.C8(e); B.D4(b); D.M6(e), zero case` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :160 `A.C8 guarantee` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :136 `D2 · exact factorisation` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :137 `D2 · LH masking law` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :96 `A.M4 · START` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :110 `B.M4 · START` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :125 `D.M6 · START` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :131 `C5 (K18…) · statement` — as W1 (TRUE) / as W1 / as W1 / REPAIRED
- `CHK_INHERITED/REPORT.md:13` — OWS-WS3 VERIFIED (carries the BO d_σ clause (e) / K10).

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 4, TRUE 2, AMBIGUOUS 1, COUNTEREXAMPLE 1, as W1 (TRUE) 1.

*Adverse rows:* W1_PC1:158 (A.C8(a–e); B.D4(a–e); D.M6(a–e): TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:159 (A.C8(e); B.D4(b); D.M6(e), zero case: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:160 (A.C8 guarantee: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** No existing Lean file. Proposal: finite product/prior factorization (C:112).

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: n/a — start law as shipped: composite block start unchanged (METHOD:118 row 0; item 1 Outcome 2, no depth/speed claim). IC3 on LH uses blocks = groups for n ≥ 9⁶ (W2PC2:131, 158).

**Notes (with sources):**

- Thm5-LH is `PROVED (SF: VERIFIED (W3-VEXP); XF: none)` — flag SAME-FAMILY-ONLY (REGISTRY_INDEX); the qualifier was omitted in R1 and restored in R2 (W2PC2:131).
- T22/T27 are `PROVED-LOCKED` / `PROVED-LOCKED, CONDITIONAL` in THEOREM_LIST terms (R0_DIFF rows K15–K17), i.e. conditional on hypotheses; DIL-DM(i) is ERROR and must not be used (W2PC2:83).

### M4 — Theorem Z𝒯 and the certificate card, including the masked-regime statement (HQ Q3)

**Round 3 resolution (MINUTES §2.1, §2.2; R3-4 unanimous):** K95 (odds certificate) is placed in S-TARGET and only cited here. K36 and K78 are output-event clauses of M4. M4 = K42, K43, K45, K44 + the masked-regime statement (HQ Q3). Final card: `R3_B.md` §S2 M4. The masked final-estimate TV/KL is FW2 (not binding). Safeguard (MINUTES §2.3): loss of the masked statement without an approved replacement escalates (C §S5).

**HQ:** wave 3 · HQ `M4` · charter `HQ_CHARTERS/M4.md` (`R3_B.md` §S3(c)). M4(f) needs M5 (same wave; MINUTES §2.5). Premises carried: GUARD-W (N2(e)); N3 DP invariant as a hypothesis of (f) (R3_B:213). Fallback: (a)–(d) always ship; if the GUARD-W audit fails, (e) ships in potential-run form only (R3_B:214).

**Seat cards (R2):** A:85–93 (M5 Z𝒯/CARD; §R4 A:190–192); B:115–123 (M5 Z𝒯/CARD; §R4 B:232–234); C:94–103 (C4; §R4 C:282–288); D:71–75 (M3′ Z𝒯 + MASK-PIP; §R4 D:168–172).

**K-IDs in this item:** K42 (core: Z ≥ Z_𝒯, Ẑ < Z_𝒯 ⇒ Ẑ < Z), K43 (core: TV/PIP bounds from stored mass), K45 (core: retention S₀ ∈ 𝒮, δ₁ < ½ ⇒ S₀ ∈ 𝒯), K44 (core: analytic envelope Z ≤ C_n(…)^{−ν} (N17)), K36 (output-event clause), K78 (output-event clause (joint with 𝒪)), K95 (not an M4 clause: placed in S-TARGET by R3-4 and cited here).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K42** `R0_DIFF:131` · class CONFIRMED-DE · Z ≥ Z_𝒯 = Σ_{S∈𝒯}ϖ(S)m(S) deterministically for any scored set 𝒯, so max{Z_𝒯, 0.05·Ẑ} is a valid 95% lower bound and Ẑ < Z_𝒯 certifies underestimation.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MZ-C1: PROVED (C1-C3 per-fit, deterministic) [IDX 185]; MZ-P3: PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery [IDX 201]; PC1c2: PROVED for the potential run; output-event version CORRECT WITH AMENDMENT (PC1 claim 2) [IDX 187]; OCERT-C1: PROVED (SF: VERIFIED* (O-VCERT); XF: ERROR (A-REV9)) [IDX 745; REG 404]
  - `OCERT-C1` — XF-ADVERSE:ERROR (SF verified) (IDX:745)
  - `MZ-C1` — FLAG AUTHOR-ONLY (IDX:185)
  - `PC1c2` — XF (IDX:187)
  - `MZ-P3` — FLAG AUTHOR-ONLY (IDX:201)
- **K43** `R0_DIFF:132` · class CONFIRMED-E · If S₀ ∈ 𝒯 then 1−δ₁ ≤ Z_𝒯/Z ≤ 1 and |PIP^𝒯_j − PIP_j| ≤ δ₁, two-sided and deterministic; E adds a data-only bracket π(𝒯) ≥ Z_𝒯/(Z_𝒯 + U_rest).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MZ-P3: PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery [IDX 201]; PC1c5: (a) PROVED, ½ sharp; (b) 'needs ⅓' FALSE; amended: δ₁ < ½ suffices (PC1 claim 5) [IDX 202]
  - `MZ-P3` — FLAG AUTHOR-ONLY (IDX:201)
  - `PC1c5` — FLAG SAME-FAMILY-ONLY (IDX:202)
- **K45** `R0_DIFF:134` · class OBLIGATION-ONLY · If S₀ ∈ 𝒮 (scored) and δ₁ < ½ then S₀ ∈ 𝒯 = top_{40p+1}(𝒮), and the HPM and MPM^𝒯 certificates coincide.
  - *R0_DIFF status cell (verbatim):* N13: PROVED (PC1 claim 5; R2C D7); premises Lemma S and the inheritance merge (PC2 code facts) [INP 225]; PC1c5: (a) PROVED, ½ sharp; (b) 'needs ⅓' FALSE; amended: δ₁ < ½ suffices (PC1 claim 5) [IDX 202]
  - `PC1c5` — FLAG SAME-FAMILY-ONLY (IDX:202)
  - `PC2` — XF (IDX:731)
- **K44** `R0_DIFF:133` · class NEW-DE · Z and π(Ŝ) have computable analytic bounds: Z ≤ C_n(2b₀+yᵀy/(n+1))^{−ν}, and from a stored set Z ≤ Z_𝒯 + m(∅)e^{u}[1 − Σ_{S∈𝒯}ϖ(S)].
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N17: PROVED (PC1 claim 1; PC2 C1(c)) [INP 248; IDX 902]; no registry row for T24’s U_rest bracket
  - `PC2` — XF (IDX:731)
- **K36** `R0_DIFF:125` · class CONFIRMED-DE · P(0.05·Ẑ > Z) ≤ 0.05 by Markov, and the average Ẑ̄ over R declared islands gives P(α·Ẑ̄ > Z) ≤ α.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T31(i): PROVED-LOCKED (THEOREM_LIST.md V1(iii)) [IDX 69]; N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT) [INP 170]; Prop2(a,b,d,e): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)) [IDX 60; REG 260]
  - `Prop2(a,b,d,e)` — XF-ADVERSE:GAP (SF verified) (IDX:60)
  - `T31(i)` — XF (IDX:69)
- **K78** `R0_DIFF:182` · class CONFIRMED-E · Every certificate and coverage statement is joint with output: P(𝒪 ∩ {L > Z}) ≤ α·P(complete) ≤ α, never conditional on delivery (which can reach α/P(delivery)).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N6: (a) PROVED (potential run; output form CORRECT WITH AMENDMENT); (b) PROVED modulo premise (i) [INP 170]; PC1c2: PROVED for the potential run; output-event version CORRECT WITH AMENDMENT (PC1 claim 2) [IDX 187]
  - `PC1c2` — XF (IDX:187)
- **K95** `R0_DIFF:209` · class NEW-E · Finite-data posterior odds give exact certificates: π(S₀) = 1/(1+A(S₀)), and A(S₀) ≤ η < 1 implies HPM = MPM = S₀ with PIPs ≥ 1/(1+η) on true and ≤ η/(1+η) on false coordinates.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Seat card status (verbatim):**

- A:91 — MZ-P3: PROVED (P3 top store, deterministic), AUTHOR-ONLY, 'candidate: not reviewed, not adopted'; PC1c5: (a) PROVED, ½ sharp; N13: PROVED (PC1 claim 5); N17: PROVED (PC1 claim 1; PC2 C1(c)); N6(a): PROVED (potential run; output form CORRECT WITH AMENDMENT); (a) identities TRUE-AS-WRITTEN (PC1:128, 259); (d) island-minimum seat-derived, TRUE-AS-WRITTEN (PC1:126); (f) E proposal, TRUE-AS-WRITTEN (PC1:130).
- B:121 — MZ-P3: PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery; AUTHOR-ONLY; N13: PROVED (PC1 claim 5); PC1c5: PROVED, ½ sharp; PC1c2: PROVED for the potential run; N6 output form CORRECT WITH AMENDMENT; N17: PROVED (PC1 claim 1); OCERT-C1: XF ERROR as quantified (O-VCERT R1 wording).
- C:99 — N17/N13: **PROVED**. MZ-P3: **PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery; AUTHOR-ONLY**, candidate, not reviewed/not adopted. N6 output: **CORRECT WITH AMENDMENT**. Assembly: **PROOF SKETCH, unchecked**.
- D:74 — Status: MZ-C1 "PROVED (C1-C3 per-fit, deterministic)"; MZ-P3 "PROVED (P3 top store, deterministic)", candidate: not reviewed, AUTHOR-ONLY; N13 "PROVED (PC1 claim 5; R2C D7)"; PC1c5 "(a) PROVED, ½ sharp"; N6(a) "PROVED (potential run; output form CORRECT WITH AMENDMENT)"; N17 "PROVED (PC1 claim 1; PC2 C1(c))"; (e) composition PROVED (by this seat, unchecked).

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :126 `A.C3(a,b,c); B.D3(e); D.M3(c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :127 `A.C3(d); D.S4 adaptive-budget wording` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :128 `A.C7(a,b,c,e); B.D3(a–d); D.M3(a,b,d)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :129 `B.D3(b) bounded-h clause` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :130 `A.C7(d)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :112 `D5 · envelope` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :113 `D5 · TV certificate` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :114 `D5 · underestimation / LCB` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :115 `D5 · region certification` — TRUE / DESIGN-ASSERTED / GAP; :116 `D12 · joint failure bound` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :117 `D12 · no conditional claim` — TRUE / n/a / PLAUSIBLE
- `W2_PC1` — :97 `A.M5 · Z𝒯/CARD` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :111 `B.M5 · Z𝒯/CARD` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :123 `D.M3′ · Z𝒯/MASK-PIP` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :136 `A.R4 · Z𝒯 / weighted h` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :142 `B.R4 · Z𝒯/CARD` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :143 `B.R4 · M₂ aside` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / GAP; :149 `D.R4 · MASK-PIP` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :128 `C4 (K43…) · unchanged clauses` — as W1 (TRUE) / as W1 / as W1; :129 `C4 · retention` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :130 `C4 · repairs` — REPAIRED DIFFERENTLY; :139 `§R4 · named guarantee (K43/K45, C4 via C3)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :140 `§R4 · finite-run companion` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- No CHK_INHERITED section targets M4 directly (CHK covers WS6(d), WS7, WS3, WS4, N9-KERNEL only).

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 11, TRUE 7, AMBIGUOUS 1, COUNTEREXAMPLE 1, NEEDS-HYPOTHESIS 1, as W1 (TRUE) 1, (repair-only or blank row) 1.

*Adverse rows:* W1_PC1:127 (A.C3(d); D.S4 adaptive-budget wording: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:129 (B.D3(b) bounded-h clause: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC2:115 (D5 · region certification: TRUE, DESIGN-ASSERTED, GAP); W2_PC1:143 (B.R4 · M₂ aside: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, GAP).

**Lean:** No existing Lean file. Proposals: finite sums, event containment (A:93, C:101, D:75). T21HPM.lean (`t21_C1` etc.) concerns the HPM composition (M5), not M4.

**Fidelity to v3.1 as shipped:**
- LS0: yes — retention uses 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) under LS0 (METHOD:151 #9; B:119(c)). LS0 is **not yet in the production core** and the merged-LS0 replay is pending (METHOD:48, 399); W2PC2:126 GAP (integrated LS0, emitted centre, GUARD-W unaudited).
- Coded grid: n/a (deterministic store identities); masked statement uses LH and checked LS0 discovery.
- Ẑ-weighted pooling / partition: Ẑ vs Z_𝒯: only through the certificate max{Z_𝒯, 0.05Ẑ} (METHOD:161 #14, :229 G2). Output statements are joint with 𝒪 under GUARD-W, an unaudited code premise (METHOD:136, 400).

**Notes (with sources):**

- MZ-P3 is `PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery`, flag AUTHOR-ONLY, 'candidate: not reviewed, not adopted' (REGISTRY_INDEX.md:201). SYNTH_R2:266 requires D.M3′ to restore this qualifier; see §Status disagreements.
- K73's operational region certification was withdrawn from M4 (C:44, W2PC2:130 REPAIRED DIFFERENTLY).
- Masked non-vacuity: LH hubs, π₀(S₀) ≍ p⁻²n⁻¹ → 0 while π(S₀) → 1 (W2PC2:139). Stated under named implementation premises SR, GUARD-W, OP-LS0 (C:57).

### M5 — Theorem HPM — composition at every n and reported-HPM consistency with LS0 on LH

**Round 3 resolution (MINUTES §2.1, §2.2; R3-4, R3-8):** K63 is a hypothesis of M5 (named here, proved in S-OUT); K70 is the labelled no-LS0 variant clause. M5 = K72, K69, K65, K68 (Theorem A; composition at every n; reported-HPM consistency with LS0 on LH). Final card: `R3_D.md` §S2 M5.

**HQ:** wave 3 · HQ `M5` · charter `HQ_CHARTERS/M5.md` (`R3_D.md` §S3(c)). First lemma: the e4 tie-DP invariant N3 (OPEN; the only open mathematical obligation in the chain), in parallel the merged-LS0 replay N2(c) (R3_D:221). Fallback: (b1-LH) becomes 'conditional on N3' after one unproductive HQ cycle (R3_D:224). Premises carried: N3 DP invariant, N2(c), GUARD-W, LS0/OP-LS0 (§8).

**Seat cards (R2):** A:95–103 (M6 HPM); B:125–133 (M6 HPM); C:83–92 (C3); D:65–69 (5′ Theorem 5).

**K-IDs in this item:** K72 (core: composition at every n, N200), K69 (core: (b1-LH) with LS0 on exact-Gram LH), K65 (core: Theorem A / LS-score progress), K68 (core: iid favourable variant (a-fav)), K63 (named hypothesis; proved in S-OUT (R3-4)), K70 (labelled no-LS0 variant clause (R3-8, decided)), K07 (lemma with SIZE (A:99)), K62 (MINUTES §2.1 places it in M1; B's R2 card placed it here (B:125)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K72** `R0_DIFF:171` · class CONFIRMED-E · For every n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n and P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + Π(X) + P(𝒪, S₀ ∉ 𝒮), with a matching lower bracket: the HPM error splits into statistical, discovery and delivery terms.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). Thm4-C1: PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none) [IDX 527; REG 264]; T38-(0): PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)) [IDX 528; REG 324]; N200: PROVED (elementary, every n); Π(X) upper bound OPEN [IDX 534]; T21: PROVED-LOCKED, CONDITIONAL (THEOREM_LIST.md R4(iii)); registry row Thm4-C1 gives the post-lock record [IDX 533]
  - `Thm4-C1` — FLAG SAME-FAMILY-ONLY (IDX:527)
  - `T38-(0)` — XF-VERIFIED*(qualified) (IDX:528) — ⚑ registry CONFLICT C11 (IDX:1185)
  - `N200` — FLAG AUTHOR-ONLY (IDX:534)
  - `T21` — XF (IDX:533)
- **K69** `R0_DIFF:168` · class DRAFT-ONLY · With LS0 on LH exact Gram (p ≤ n−1, c linked pairs) P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with no open statistical hypothesis; in general under (M1)–(M3) and OP-LS0.
  - *R0_DIFF status cell (verbatim):* T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 438; REG 330]; Thm-b1: PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8)) [IDX 549; REG 328]; LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 508; REG 326]; T38-b1-LH-iidfail: — (SF: none; XF: ERROR (A-REV5)) [IDX 553; REG 788]
  - `T38-b1-LH-iidfail` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:553) — ⚑ registry CONFLICT C24 (IDX:1198)
  - `T38-b1-LH` — XF-VERIFIED*(qualified) (IDX:438) — ⚑ registry CONFLICT C24 (IDX:1198)
  - `LS-score` — XF-VERIFIED*(qualified) (IDX:508)
  - `Thm-b1` — XF-VERIFIED (IDX:549)
- **K65** `R0_DIFF:164` · class DRAFT-ONLY · Under TD′ (tie-broken progress-greedy dominance), from any centre in Lat(S°) the production local search reaches and scores S₀ in Φ moves, and LS0 scores S₀ within max{Φ(S°)−1, 0} moves.
  - *R0_DIFF status cell (verbatim):* TheoremA: PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)) [IDX 500; REG 150]; LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 508; REG 326]; Lemma0(b): PROVED (SF: GAP (W3-VT37R); XF: ERROR (A-REV2)) [IDX 502; REG 147]; Prop1-TD: PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED (A-REV2)) [IDX 510; REG 144] (retires literal T37/TD)
  - `Lemma0(b)` — XF-ADVERSE:ERROR (no clean SF) (IDX:502) — ⚑ registry CONFLICT C1 (IDX:1175)
  - `TheoremA` — XF-VERIFIED*(qualified) (IDX:500)
  - `LS-score` — XF-VERIFIED*(qualified) (IDX:508)
  - `Prop1-TD` — XF-VERIFIED (IDX:510)
- **K68** `R0_DIFF:167` · class CONFIRMED-DE · In the favourable regime (iid π₀ draws score S₀) the reported HPM equals S₀ w.p. → 1 − limsup P(U), and generally the all-scored HPM succeeds with probability ≥ 1 − α_stat − exp(−Q·a_min).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T38-(a): PROVED-UNDER (SF: VERIFIED* (inputs); XF: none) [IDX 548; REG 325]; R5 draft: (a) PROVED-UNDER (F) (ORTH joint family PROOF SKETCH) [LST 41, 674]
  - `T38-(a)` — FLAG SAME-FAMILY-ONLY (IDX:548)
- **K63** `R0_DIFF:162` · class CONFIRMED-DE · The HPM is the maximum of F under the strict total order (F, −|S|, lex) over the scored set, independent of scoring order, and top-c stores merge by union-then-truncate: top_c(M) = top_c(∪_r top_c(M_r)).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-LemmaS: PROVED (candidate; 'Every item is a candidate: not reviewed, not adopted') [IDX 91]; V2 draft status: Lemma S PROVED [LST 22]
  - `MA-LemmaS` — FLAG AUTHOR-ONLY (IDX:91)
- **K70** `R0_DIFF:169` · class DRAFT-ONLY · Without LS0 (v3 as run) on the LH subfamily satisfying STAB-LH and any frozen grid, P(S₀ ∉ 𝒮 | 𝓒) → 0 and the reported HPM equals S₀ w.p. → 1 − limsup P(U).
  - *R0_DIFF status cell (verbatim):* B2E-B2LH: PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7)) [IDX 439; REG 547]; STAB-cert(A7): REFEREE (SF: n/a; XF: referee-authored (Astra-authored)) [IDX 568; REG 739]; VSTAB: STAB certificate PROVED (API-VSTAB §4.1); theorem B2-LH on STAB-LH: 'PROVED-UNDER STAB-LH' (T38-RECORD) [IDX 581]
  - `STAB-cert(A7)` — REFEREE-AUTHORED (author is a cross-family referee) (IDX:568)
  - `B2E-B2LH` — XF-VERIFIED*(qualified) (IDX:439)
  - `VSTAB` — XF (IDX:581)
- **K07** `R0_DIFF:81` · class NEW-DE · If every within-group distance is strictly below every between-group distance and groups have size ≤ B, complete linkage forms each group first and cutting/packing never splits a group, so cross-block |r| ≤ the largest between-gro…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 768; REG 660]; PART-pairing: OPEN (SF: none; XF: none) [IDX 773; REG 670]; PART-CE2 (COUNTEREXAMPLE): “Blocks ≠ groups surely when two groups fit in one block.” [IDX 1015; REG 668]
  - `PART-pairing` — FLAG AUTHOR-ONLY (IDX:773)
  - `PART-ThmA` — XF-VERIFIED*(qualified) (IDX:768)
  - `PART-CE2` — XF-ADVERSE:ERROR (no clean SF) (IDX:772)
- **K62** `R0_DIFF:156` · class NEW-E · If every exact PIP is at least δ from ½ and the estimated PIPs err uniformly by less than δ, the reported MPM equals the exact MPM.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `Thm5-LH` — FLAG SAME-FAMILY-ONLY (IDX:325)

**Seat card status (verbatim):**

- A:101 — unchanged from R1 §D C17/C18 lists (Thm4-C1; T38-(0); N200 author-only; TheoremA; LS-score; T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); B2E-B2LH: PROVED-UNDER (XF: VERIFIED* (A-REV7)); STAB-cert(A7) REFEREE; PART-ThmA: PROVED (XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; N3: OPEN; N2(c) pending).
- B:131 — T38-(0): PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5)); N200: PROVED (elementary, every n), author-only; TheoremA: PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2)); LS-score: PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8)); T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)); B2E-B2LH: PROVED-UNDER (XF: VERIFIED* (A-REV7)); general LH locking: XF ERROR (not used); Thm5-LH SAME-FAMILY-ONLY.
- C:87 — T38-b1-LH: **PROVED; SF VERIFIED*; XF VERIFIED***. TheoremA: **PROVED; SF VERIFIED; XF VERIFIED***. LS-score: **PROVED; SF VERIFIED; XF VERIFIED***. T38-(0): **PROVED; SF VERIFIED; XF VERIFIED***. Assembly: **PROOF SKETCH, unchecked**. Thm5-LH’s **SAME-FAMILY-ONLY** qualification is retained through C5.
- D:68 — Status: TheoremA "PROVED (SF: VERIFIED (W3-VT37R); XF: VERIFIED* (A-REV2))"; LS-score "PROVED (SF: VERIFIED (W5-VMASK); XF: VERIFIED* (A-REV8))"; T38-b1-LH "PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8))"; Thm-b1 "PROVED-UNDER (SF: VERIFIED (W5-VMASK); XF: VERIFIED (A-REV8))"; T38-(a) "PROVED-UNDER (SF: VERIFIED* (inputs); XF: none)"; B2E-B2LH "PROVED-UNDER (SF: none; XF: VERIFIED* (A-REV7))"; Thm4-C1 "PROVED (SF: VERIFIED* (W5-LOCKBOOK); XF: none)"; T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; N200 "PROVED (elementary, every n); Π(X) upper bound OPEN" (author-only); N3 "OPEN".

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :166 `A.C18(0,b1-LH); B.D8(0,2,5); D.M5(b1-LH)` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :167 `A.C18(a,b2-LH,b1-LH-iid); B.D8(3); D.M5(a-fav,b2-LH)` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :168 `D.M5(a), certification wording` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / PLAUSIBLE; :169 `A.C18 clustering lemma` — NEEDS-HYPOTHESIS / DESIGN-FAILS / PLAUSIBLE; :170 `A.C18/B.D8/D.M5 guarantees; A.C13(d)` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :176 `A.C17(a,b,c); B.D8(0); D.M4(a,b,c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :177 `A.C17(d,e); D.M4(d)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :143 `D4 · LS0 consistency on LH` — TRUE / DESIGN-VERIFIED / GAP; :144 `D4 · LS-score` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :98 `A.M6 · HPM` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED; :112 `B.M6 · HPM` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED; :122 `D.5′ · HPM/Theorem A` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED
- `W2_PC2` — :126 `C3 (K69…) · output form + SIZE` — TRUE / DESIGN-VERIFIED / GAP / REPAIRED; :127 `C3 · scoring vs certification` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :170 `C3/C4 · ℓ = ⌈log₂(n+p+1)⌉` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- No CHK_INHERITED section targets M5.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 9, NEEDS-HYPOTHESIS 3, TRUE 3.

*Adverse rows:* W1_PC1:166 (A.C18(0,b1-LH); B.D8(0,2,5); D.M5(b1-LH): TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:167 (A.C18(a,b2-LH,b1-LH-iid); B.D8(3); D.M5(a-fav,b2-LH): TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:168 (D.M5(a), certification wording: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:169 (A.C18 clustering lemma: NEEDS-HYPOTHESIS, DESIGN-FAILS, PLAUSIBLE); W1_PC1:170 (A.C18/B.D8/D.M5 guarantees; A.C13(d): NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC2:143 (D4 · LS0 consistency on LH: TRUE, DESIGN-VERIFIED, GAP); W2_PC1:98 (A.M6 · HPM: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC1:112 (B.M6 · HPM: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC1:122 (D.5′ · HPM/Theorem A: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC2:126 (C3 (K69…) · output form + SIZE: TRUE, DESIGN-VERIFIED, GAP, REPAIRED).

**Lean:** `T21HPM.lean` (`t21_C1`, `t21_decomposition`, …): 0 `sorry`; routes (a)–(f) and H03 asymptotics NOT formalised. `T37Greedy.lean` + `T37Lattice.lean` (Theorem A, Lemma0(a,c) lattice forms): 0 `sorry` in SmcBvs/SmcBvs; A5, Theorems B, C not formalised. `LS-score`: **no Lean file stated** (REGISTRY_INDEX.md:931–932, :930, §3.5 last row). The older copies `frozen/v1/T37Lattice.lean` and `fidelity/packet/lean/T37Lattice.lean` contain 8 `sorry` (REGISTRY_INDEX.md §3.3); `fidelity/packet2` and `SmcBvs/SmcBvs` copies are sorry-free and sha1-identical. Fidelity: Fable 5.1 GREEN; Astra round 2 OVERALL (T37) GREEN (REGISTRY_v2 §G, quoted REGISTRY_INDEX.md §3.4). A green fidelity check changes no author status.

**Fidelity to v3.1 as shipped:**
- LS0: yes — (b1-LH) needs LS0 (METHOD:150 #8). Integrated LS0, emitted-centre (N2(c)/N3 tie-DP) and GUARD-W audits are OPEN: W2PC2:126 `GAP`, C:86; W2PC1:98, 112, 122 `GAP`. LS0 changed the HPM in 0 of 2,394 test-export fits (METHOD:48).
- Coded grid: any frozen grid (b2-LH, no-LS0 variant, STAB-LH) — variant labelled (A:99, B:129).
- Ẑ-weighted pooling / partition: n/a (HPM decision is the all-scored maximum, METHOD:94 row §6.10; K63 order-independence).

**Notes (with sources):**

- N3 (tie-DP invariant, e4 centre rule) is `OPEN` (R0_DIFF K09 row; C:170); carried as a hypothesis (B:129).
- T38-b1-LH carries a registry CONFLICT row (C24, iid sub-claim only; A-REV5 ERROR vs A-REV8 GAP; LS0 consistency conclusion VERIFIED by A-REV8) — REGISTRY_INDEX.md:1198 (C24).; W2PC2:88.
- K71 (b1-LH-iid) → FUTURE_WORK; K82 delivery → FUTURE_WORK; all output statements are joint with 𝒪 in liminf form (S2:52).

### M6 — Theorem SEP + Lemma KL — why the start/one-shot merge fails at the Q* scale

**Round 3 resolution (MINUTES §2.1, §2.3):** M6 = K19, K106, K105 (Theorem SEP + Lemma KL). Shared Song–Liang wording (R3-7): Thm 2 — "fixed-design, fixed-sparsity selection counterpart only; SL's predictor-tail and prior hypotheses are not transferred"; Cor 2 — "no analytic null-exclusion/FDR separation established; LIT-PAR G4 numerical evidence" (C's wording; the SL analytic separation K97 is FUTURE_WORK, R3-3). Final card: `R3_C.md` §S2 M6.

**HQ:** wave 2 · HQ `M6` · charter `HQ_CHARTERS/M6.md` (`R3_C.md` §S3 'M6 charter'). M6 supplies the lower bound used by M2.

**Seat cards (R2):** A:115–123 (M8 SEP + KL); B:145–153 (M8 SEP + KL); C:116–125 (C6); D:87–90 (SEP′).

**K-IDs in this item:** K19 (core: iid miss (1−π₀)^Q ≤ exp(−Qπ₀), switch at Q*), K106 (core: 1+χ² ≥ π(S₀)²/π₀(S₀); one-shot IS variance), K105 (Lemma KL: KL(π‖π₀) ≥ (1−δ₁)log(1/π₀(S₀)) − log 2).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K19** `R0_DIFF:93` · class CONFIRMED-DE · If Q independent π₀ draws are scored, the chance of never scoring a target model (or the HPM S*) is (1−π₀(·))^Q ≤ exp(−Qπ₀(S*)); on LH it switches sharply at Q* = p^c·n^{c/2}.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). SEP-A: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 352; REG 641]; SEP-A-iid: PROVED-UNDER (SF: none; XF: none) [IDX 353; REG 642]; T38-(a): PROVED-UNDER (SF: VERIFIED* (inputs); XF: none) [IDX 548; REG 325]
  - `SEP-A-iid` — FLAG AUTHOR-ONLY (IDX:353)
  - `T38-(a)` — FLAG SAME-FAMILY-ONLY (IDX:548)
  - `SEP-A` — XF-VERIFIED (IDX:352)
- **K106** `R0_DIFF:235` · class DRAFT-ONLY · One-shot importance correction from π₀ to π needs 1 + χ²(π‖π₀) ≥ Q*·e^{O_P(1)}: the self-normalised estimate has relative variance (Q*/Q)e^{O_P(1)} and equals 0 w.p. → 1 below Q*.
  - *R0_DIFF status cell (verbatim):* SEP-B: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 354; REG 643]; SEP-E: PROVED-UNDER (SF: none; XF: none) [IDX 357; REG 646]; SEP-A: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 352; REG 641]
  - `SEP-A` — XF-VERIFIED (IDX:352)
  - `SEP-B` — XF-VERIFIED (IDX:354)
  - `SEP-E` — FLAG AUTHOR-ONLY (IDX:357) — ⚑ registry CONFLICT C19 (IDX:1193)
- **K105** `R0_DIFF:234` · class DRAFT-ONLY · KL(π‖π₀) ≥ (1−δ₁)·log(1/π₀(S₀)) − log 2, so the Chatterjee–Diaconis sample size exp(KL) is at least ½·Q*^{1−δ₁}·e^{O_P(1)}.
  - *R0_DIFF status cell (verbatim):* KL: PROOF SKETCH (NEW-SYNTH: 'PROOF SKETCH only because unreviewed; the inequality is two lines') [IDX 369]
  - `KL` — FLAG AUTHOR-ONLY (IDX:369)

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `OWS-WS7` — FLAG AUTHOR-ONLY (IDX:413)

**Seat card status (verbatim):**

- A:121 — SEP-A, SEP-B: PROVED (SF: none; XF: VERIFIED (A-REV9)); KL: PROOF SKETCH (NEW-SYNTH); OWS-WS7(a): PROVED (no review) + CHK VERIFIED WITH AMENDMENT (CHK:12, 79).
- B:151 — SEP-A, SEP-B: PROVED (SF: none; XF: VERIFIED (A-REV9)); SEP-A-iid: PROVED-UNDER; KL: PROOF SKETCH (NEW-SYNTH); OWS-WS7(a): PROVED (SF: none; XF: none) + CHK_INHERITED VERIFIED WITH AMENDMENT.
- C:120 — SEP-A/SEP-B: **PROVED; SF none; XF VERIFIED**. KL addendum: **PROOF SKETCH**.
- D:89 — Status: SEP-A, SEP-B "PROVED (SF: none; XF: VERIFIED (A-REV9))"; KL "PROOF SKETCH (NEW-SYNTH)" (PC2 D3 TRUE, 0 failures).

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :183 `A.C10(a,b,c,d); B.D5(a–d); D.M7(a–d)` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :184 `A.C10/B.D5 guarantees; D.M7 bridge-cost sentence` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :150 `D3 · miss probability` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :151 `D3 · χ² bound` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :152 `D3 · KL bound` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :153 `D3 · IS variance` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :100 `A.M8 · SEP/KL` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :114 `B.M8 · SEP/KL` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :127 `D.SEP′` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :132 `C6 (K106…) · Q* scale` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `CHK_INHERITED/REPORT.md:12` — OWS-WS7 VERIFIED WITH AMENDMENT; the checked KL form with π(S₀) in place of 1−δ₁ is WS7(a) (A:119, CHK:79).

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 5, TRUE 4, NEEDS-HYPOTHESIS 1.

*Adverse rows:* W1_PC1:183 (A.C10(a,b,c,d); B.D5(a–d); D.M7(a–d): TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:184 (A.C10/B.D5 guarantees; D.M7 bridge-cost sentence: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** `T11Miss.lean` (`t11_miss_iid`, `t11_miss_pi`, `t11_pow_le_exp`) proves the iid-miss inequality; L-LEAN STATUS.md ties it to locked T11(iii) 'no registry row'. **No source maps K19/SEP-A to T11Miss** — registrar statement-match only, marked unmapped. 0 `sorry`. No Lean file for Lemma KL (REGISTRY_INDEX.md:928, §3.5).

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a — comparison objects are iid π₀ discovery and the one-shot unnormalised estimator, **not production SMC** (A:119, B:149, C:119; W1PC1 ledger S9, VERDICTS.md:87).
- Ẑ-weighted pooling / partition: n/a

**Notes (with sources):**

- SEP-taska is a registry COUNTEREXAMPLE (start + local search can succeed on LH): no universal lower bound on algorithms may be stated (A:119).

### M7 — Theorem STG — stage laws as coded, coverage identity

**Round 3 resolution (MINUTES §2.1, §2.2, §2.3; R3-4, R3-8):** M7 = K26, K25, K27, K30, K33; K28 cited. K33 is in M7 in its deterministic termination/count form (A, B, C; **dissent D: S-IDENT**, R3_D:25, :42, :131); rebuild convergence N5(b) is FUTURE_WORK either way. K30 is the labelled ideal-grid clause of M7 and is restated in S-STGI. K29 is not in M7 (S-STGI, cited conditional implication only). Final card: `R3_A.md` §S2 M7.

**HQ:** wave 2 · HQ `M7` · charter `HQ_CHARTERS/M7.md` (`R3_A.md` §S3(c) 'Charter M7'). Feeds M2(b) (count) and M8 (T). Fallback: (a),(b),(d),(e) with T ≤ T_e; drop the counts of (c)/(c′) if the resolution/progress lemma fails (R3_A charter M7).

**Seat cards (R2):** A:105–113 (M7 STG); B:135–143 (M7 STG); C:138–146 (C8 (supplement in C)); D:81–85 (STG′).

**K-IDs in this item:** K26 (core: monotone ESS, bisection, greedy shortest grid), K25 (core: ρ_full = ρ_V a_u a_w/a_v² (also M2, S-IDENT)), K27 (core (R3-8): accepted interval (v−u)²Var ≤ log(10/9); T ≤ P + ⌈2/h⌉ + 1), K30 (R3-8: ideal two-state crossing log₂A₀+O(1)), K28 (cited: Θ(Λ_V/0.3246)), K33 (R3-4: build_grid termination, ρ_V ≥ 0.9).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K26** `R0_DIFF:110` · class CONFIRMED-DE · The ESS criterion is monotone in both endpoints, so bisection finds the exact frontier, the greedy grid is the shortest valid grid, and the stage count is at most T_e on success.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). STG-G: PROVED (SF: none; XF: none) [IDX 257; REG 696]; STG-L0: PROVED (SF: none; XF: none) [IDX 255; REG 694]; STG-L1: PROVED (SF: none; XF: none) [IDX 256; REG 695]; T26BUD-G: PROVED, deterministic (Theorem G); Conjecture P (pilot stage count O_P(1)) CONJECTURED [IDX 268]
  - `T26BUD-G` — FLAG AUTHOR-ONLY (IDX:268)
  - `STG-L0` — FLAG AUTHOR-ONLY (IDX:255)
  - `STG-L1` — FLAG AUTHOR-ONLY (IDX:256)
  - `STG-G` — FLAG AUTHOR-ONLY (IDX:257)
- **K25** `R0_DIFF:109` · class NEW-DE · The stage ESS fraction is 1/(1+χ²), and the full ESS equals the restricted-set ESS times the exact coverage factor a_u·a_w/a_v² (a_t = q_t(V), w = 2v−u), so a restricted ESS ≥ 0.9 certifies the full bridge only up to the missing m…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N5(b2) OPEN [INP 161]; INP I9(d) [INP 274]
  - no registry/index ID is named in the cell
- **K27** `R0_DIFF:111` · class NEW-DE · Every grid interval obeys (v−u)²·Var_ξ(d) ≤ log(10/9), so the stage count is bounded by the maximal spread sd(d) (or the range D_V of d) plus the pilot targets.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K30** `R0_DIFF:114` · class CONFIRMED-DE · A pair-dominance crossing of gap D costs log₂(D) + O(1) ESS-0.9 stages, separated crossings add, and no V, N or seed removes this lower bound.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 261; REG 700]; D2: STG-M PROVED (ideal two-state grid), XF VERIFIED*; families PROOF SKETCH [LST 30]; STG-cexW2 (COUNTEREXAMPLE): “F-DRAFT's O(1) stage count is false.” [IDX 1019; REG 703]
  - `STG-cexW2` — FLAG AUTHOR-ONLY (IDX:264)
  - `STG-M` — XF-VERIFIED*(qualified) (IDX:261)
- **K28** `R0_DIFF:112` · class CONFIRMED-D · For regular spreads the stage count is Θ(Λ_V/0.3246) with Λ the thermodynamic length, and √c·T*(c) → Λ as c → 0, but Λ underestimates crossings.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). STG-L: PROVED (SF: none; XF: none) [IDX 258; REG 697]; D2(d) PROVED (two-sided κ-regularity) [LST 356]
  - `STG-L` — FLAG AUTHOR-ONLY (IDX:258)
- **K33** `R0_DIFF:117` · class NEW-DE · build_grid terminates, every appended point satisfies ρ_V ≥ 0.9, a forced pilot step certifies an empirical spread ≳ 0.32·T_e, and calibration termination and cost are bounded.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N15: calibration share seat-derived, not proof-checked [INP 238]
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `ConjP` — FLAG NONE-STATED (IDX:269)
- `STG-Wp` — FLAG AUTHOR-ONLY (IDX:260) — ⚑ registry CONFLICT C22 (IDX:1196)
- `STG-F` — FLAG AUTHOR-ONLY (IDX:259)

**Seat card status (verbatim):**

- A:111 — STG-G/L0/L1: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic; STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); STG-L: PROVED; ConjP: OPEN; STG-cexW2: COUNTEREXAMPLE; (b),(c): D/E proposals, TRUE-AS-WRITTEN (PC1:192–193); WS7(d): PROVED (no review) + CHK VERIFIED WITH AMENDMENT.
- B:141 — STG-G, STG-L0/L1/L: PROVED (SF: none; XF: none); T26BUD-G: PROVED, deterministic; STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); STG-F: PROVED (SF: none; XF: none); STG-Wp: PROVED-UNDER (C22); ConjP: OPEN; T26BUD/PC2 count replica: TRUE-AS-WRITTEN (statement sanity only).
- C:142 — PC2 cluster 9 corrects “at least.” STG-L0/L1/G: **PROVED; SF none; XF none; AUTHOR-ONLY**. T26BUD-G: **PROVED, deterministic**. Assembly and pilot extension: **PROOF SKETCH, unchecked**.
- D:84 — Status: STG-G, STG-L0, STG-L1 "PROVED (SF: none; XF: none)"; T26BUD-G "PROVED, deterministic (Theorem G)"; STG-M "PROVED (SF: none; XF: VERIFIED* (A-REV9))"; STG-F "PROVED (SF: none; XF: none)"; STG-L "PROVED (SF: none; XF: none)"; (b) PROVED (by this seat, unchecked), PC2 D7 TRUE-AS-WRITTEN to 1e−8; ConjP "OPEN".

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :190 `A.C11(a); B.D7(a); D.M9(a)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :191 `A.C11(a); B.D7(a); D.M9(a), exact/minimal wording` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :192 `A.C11(b); B.D19 coverage; D.M9(b)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :193 `A.C11(c); B.D7(b); D.S10 interval formula` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :194 `A.C11(c) stage-count conclusion` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :195 `B.D7(b) count; A.C11(c) range existence` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :196 `A.C11(d); B.D7(e); D.M9(c); thesis favourable clauses` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / GAP; :197 `A.C11(e,f,g); B.D7(c,d); D.M9(d,e), K31` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :198 `D.S10 remaining clauses` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :159 `D7 · missing-mass identity (E:T14)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :160 `D7 · transfer` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :161 `D7 · increment h (E:T13)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :162 `D7 · coded count` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :163 `D7 · statuses` — verbatim ✓; :164 `D13 · ideal crossing` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :99 `A.M7 · STG` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :113 `B.M7 · STG` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :126 `D.STG′` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :105 `C2(b) · stage count` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :155 `C8 · resolution` — TRUE / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :156 `C8 · pilot extension` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `CHK_INHERITED/REPORT.md:12` — OWS-WS7(d) halving inequality checks (section CHK:70); amendments CHK:83–84 adopted by A:109, A:169.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 10, TRUE 5, COUNTEREXAMPLE 2, NEEDS-HYPOTHESIS 2, AMBIGUOUS 1, verbatim ✓ 1.

*Adverse rows:* W1_PC1:191 (A.C11(a); B.D7(a); D.M9(a), exact/minimal wording: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:194 (A.C11(c) stage-count conclusion: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:195 (B.D7(b) count; A.C11(c) range existence: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:196 (A.C11(d); B.D7(e); D.M9(c); thesis favourable clauses: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, GAP); W1_PC1:197 (A.C11(e,f,g); B.D7(c,d); D.M9(d,e), K31: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC2:162 (D7 · coded count: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** No existing Lean file for STG. Proposed finite cores only (A: `—`; C:144 'add empirical-range bound and bisection progress invariant').

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: yes as coded for K26/K27/K33 (ESS 0.90, 60 halvings, snap 10⁻¹², pilot floor 1/T_e: METHOD:324–326 rows 27–29); 'exact/minimal' dropped (W1PC1:191 COUNTEREXAMPLE); optimality only among refinements of the retained pilot targets with 2^{−60} slack (A:109). K30 is an **ideal two-state grid** (labelled comparison, not the coded grid).
- Ẑ-weighted pooling / partition: n/a

**Notes (with sources):**

- As-coded masked stage count T_n is Conjecture P (OPEN) → FUTURE_WORK (K31); fallback T ≤ T_e in main (A:21, D:82). STG-cexW2 is a registry COUNTEREXAMPLE: 'F-DRAFT's O(1) stage count is false'.
- STG-Wp has a registry CONFLICT row (C22: (LL) may need restating for 2Ar > 1). STG-G/L0/L1/L/F: PROVED (SF none, XF none) — AUTHOR-ONLY; T26BUD-G flag AUTHOR-ONLY (omitted in C8, W2PC2:86).

### M8 — Proposition D — island-level work, depth and width (R3-1: main, unanimous; this item replaces the former supplement item S-D)

**Round 3 resolution (MINUTES §2.1; R3-1 unanimous: A:101; B:138; C:119; D:128):** Proposition D is the 8th main item (stated reason: IC5, objective (2)). K-IDs: K87, K88, K89, K06, K64; K90 as a remark. **S-D is not a separate item: it is M8** (the former S-D section is removed; K06's registry entry is in S-BLOCKS, K64's in S-CERT; their check rows are listed in the notes below). The Song–Liang §6 comparison is in the same units, with no speed claim. Final card: `R3_D.md` §S2 'Card Prop D'. Alternative recorded for Felipe (MINUTES §2.1; R3_D §S5): if objective (2) is served by an introduction sentence citing the supplement instead, Prop D moves to the supplement and main = 7; nothing else changes.

**HQ:** wave 3 · HQ `M8` · charter `HQ_CHARTERS/M8.md` (`R3_D.md` §S3(c) 'Charter Prop D'). First lemma: the trajectory inventory of the execution DAG (R3_D:230). Premises carried: execution DAG audit, LS0 (counted), N2(b) calibration islands (§8). Escalation: depth growing with R′ at w ≥ R′, or a non-trajectory calibration cost of the same order as the final run (R3_D:234).

**Seat cards (R2):** A:131 (S3 Proposition D); B:169–171 (S3 Theorem D); C:127–136 (C7 (main)); D:103 (M13 Proposition D).

**K-IDs in this item:** K87 (core: work R′N(T+L+4)m + tables + calibration + LS), K88 (core: island depth N(T+L+4)m, waves ⌈R′/w⌉), K89 (accounting (Brent, Ω-depth, memory)), K90 (accounting remark: SL §6 same units, no speed claim). K06 (block count and table cost; registry entry in S-BLOCKS), K64 (scan bound ≤ ℓ+1; registry entry in S-CERT).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K87** `R0_DIFF:196` · class CONFIRMED-DE · The work of v3.1 is tables + calibration + R·N·(T+L+4)·m·s̄ + local search + O(np²), polynomial in n under the v3 budgets, counted with m = p+B+2 steps per round, two tiers, summaries and certificates.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropD: PROVED (counting, given the code's structure) [IDX 242]; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none) [IDX 237; REG 252]; Cost-T38: PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5)) [IDX 238; REG 251]
  - `Cost-T38` — XF-ADVERSE:GAP (SF verified) (IDX:238) — ⚑ registry CONFLICT C18 (IDX:1192)
  - `MA-PropD` — FLAG AUTHOR-ONLY (IDX:242)
  - `T32(i)` — FLAG SAME-FAMILY-ONLY (IDX:237) — ⚑ registry CONFLICT C18 (IDX:1192)
- **K88** `R0_DIFF:197` · class CONFIRMED-DE · Island-parallel depth is setup + calibration + N(T+L+4)m score slots + local search, with width R; the particle-parallel critical path, free of N, H and R, is the declared v3.2 path.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropD: PROVED (counting, given the code's structure) [IDX 242]; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none) [IDX 237; REG 252]
  - `MA-PropD` — FLAG AUTHOR-ONLY (IDX:242)
  - `T32(i)` — FLAG SAME-FAMILY-ONLY (IDX:237) — ⚑ registry CONFLICT C18 (IDX:1192)
- **K89** `R0_DIFF:198` · class CONFIRMED-DE · Brent-type time ≤ W/P + D holds, depth is Ω((T+T_cal)·m·s) because a particle’s sweep is sequential, and Θ(p²) Gram memory and Ω(p²) clustering are ceilings that islands and particles do not remove.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). INP I1 (m = p+B+2 sequential steps per round, by definition) [INP 267]; I2 (full-coordinate round needs scoring access; private Gram copy not inherent) [INP 268]
  - no registry/index ID is named in the cell
- **K90** `R0_DIFF:199` · class DRAFT-ONLY · In the same units, Song–Liang §6 with K = √p processors has wall time O(p^{(1+α)/2}) + O(np) and output = merged-set posterior, while v3.1 has depth of the same order in p at α = 1 with far more width and work, and output π exactl…
  - *R0_DIFF status cell (verbatim):* D1 draft status: Prop D PROVED (counting); T32(i) PROVED (rate GAP; polynomial stands); SL §6 figures from the JRSS-B text [LST 29, 320]
  - `T32(i)` — FLAG SAME-FAMILY-ONLY (IDX:237) — ⚑ registry CONFLICT C18 (IDX:1192)

**Seat card status (verbatim):**

- A:131 — Status unchanged (MA-PropD: PROVED (counting, given the code's structure), author-only; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none), rate GAP; Cost-T38: PROVED-UNDER (XF: GAP); calibration share seat-derived, not proof-checked). Supplement.
- B:171 — Status: MA-PropD: PROVED (counting, given the code's structure), author-only candidate; T32(i): PROVED (SF: VERIFIED (W7-SEC); XF: none), displayed rate GAP (A-REV5); Cost-T38: PROVED-UNDER (XF: GAP). Rest unchanged.
- C:132 — MA-PropD: **PROVED (counting, given the code’s structure); AUTHOR-ONLY**. T32(i): **PROVED; SF VERIFIED (W7-SEC); XF none; SAME-FAMILY-ONLY**. Cost-T38: **PROVED-UNDER; XF GAP (A-REV5)**. Updated assembly: **PROOF SKETCH, unchecked**.
- D:103 — MA-PropD "PROVED (counting, given the code's structure)"; T32(i) "PROVED (SF: VERIFIED (W7-SEC); XF: none)"; rate GAP

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :228 `A.C12(a,b,c); B.D11 counts/depth; D.M13` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :229 `A.C12 polynomial/Brent; B.D8(5); D.M13 polynomial` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :230 `A.C12(d); B.D11 SL comparison; D.M13 SL clause` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / GAP
- `W1_PC2` — :177 `D6 · final run` — TRUE / DESIGN-VERIFIED / GAP; :178 `D6 · calibration and LS` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :181 `A.S3 · D` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED; :194 `B.S3 · D; S4 · Z` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED; :205 `D.M13 · D` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED
- `W2_PC2` — :133 `C7 (K87/K88) · calibration` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED
- No CHK_INHERITED section targets Proposition D.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 5, TRUE 2, AMBIGUOUS 1, NEEDS-HYPOTHESIS 1.

*Adverse rows:* W1_PC1:228 (A.C12(a,b,c); B.D11 counts/depth; D.M13: AMBIGUOUS, DESIGN-VERIFIED, GAP); W1_PC1:230 (A.C12(d); B.D11 SL comparison; D.M13 SL clause: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, GAP); W1_PC2:177 (D6 · final run: TRUE, DESIGN-VERIFIED, GAP); W2_PC1:181 (A.S3 · D: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC1:194 (B.S3 · D; S4 · Z: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC1:205 (D.M13 · D: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED); W2_PC2:133 (C7 (K87/K88) · calibration: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED).

**Lean:** No Lean file. Cards: 'finite counting' (C:134).

**Fidelity to v3.1 as shipped:**
- LS0: counted: each completed search incl. LS0 and the retained baseline search is counted separately (C:130; A:131). LS0 not yet in production core (METHOD:48).
- Coded grid: yes: calibration work Σ N_i(T_i+L_i+4)m over executed trajectories each with its own grid (C:129; W1PC1:228 AMBIGUOUS → repaired; W2PC2:133).
- Ẑ-weighted pooling / partition: n/a. Integrated execution-DAG audit: **NOT REPAIRED** (W2PC2:133 GAP; W2PC1:181, 194, 205 GAP). 'Depth free of N, H, R' is not claimed (METHOD:171 #19).

**Notes (with sources):**

- SYNTH_R2 options (ii) standalone V+ and (iii) none are closed by R3-1 (MINUTES §2.1). Check rows carried over from the former S-D for K06/K64: W1PC1:228–230 (counts), W1PC1:271–274 (scans), W2PC1:181, :194, :205, W2PC2:133 (integrated execution DAG: NOT REPAIRED / GAP). Lean: none. Fidelity: as above.
- MA-PropD `PROVED (counting, given the code's structure)` flag AUTHOR-ONLY; T32(i) `PROVED (SF: VERIFIED (W7-SEC); XF: none)` flag SAME-FAMILY-ONLY, displayed rate GAP; Cost-T38 `PROVED-UNDER (XF: GAP (A-REV5))`; registry CONFLICT C18 (T32(i), Cost-T38; recorded stale, not dissenting).

## 2. Supplement cards (MINUTES §2.2; statements as in the cited R2/R3 cards with the SYNTH_R2 §3 repairs)

### S-T — Supplement S-T — Theorem 1, target consistency (T03♯)

**Round 3 resolution (MINUTES §2.2):** unanimous since Round 2: supplement card S-T, cited in the main text (K93, K04). Statement flags to restate: T01–T03 SAME-FAMILY-ONLY, external review queued (§7).

**HQ:** wave 1 · HQ `LP-FOUND` · charter `HQ_CHARTERS/LP-FOUND.md` (cited only: S-T is registered in wave 1 with no HQ work of its own, R3_A:178, R3_B:224, R3_D:211).

**Seat cards (R2):** A:127 (S1 Theorem T); B:165–167 (S2 Theorem 1); C:155–164 (C9); D:102 (M12 Theorem 1).

**K-IDs in this item:** K93 (core: 1−π(S₀)=O_P(√(log n/n)); HPM/MPM consistency; large-signal inclusion), K04 (BB(1,p) mass / size law (D's card)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K93** `R0_DIFF:207` · class CONFIRMED-DE · Posterior mass off S₀ is O_P(√(log n/n)), HPM and MPM of π equal S₀ w.p. → 1, and large signals get PIP → 1 without beta-min (T03♯).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)) [IDX 151; REG 134]; T01-T03: PROVED-LOCKED (wave 3; external review queued) (THEOREM_LIST.md R1(iii)) [IDX 469]; T03-1.2e5 (—): “SF: **ERROR** — W2-VT03R row 29 ERROR (binding condition q_n ≤ ½ first holds at n ≈ 2.1·10⁶ / 2.5·10⁶) ⟂ XF: **ERROR** — A-REV2 §3.5 confirms: q ≈ 5.5·10²², 7.9·10²⁸ at n=130,328” [IDX 1040; REG 748]
  - `T03-1.2e5` — FLAGGED-SUBCLAIM (SF ERROR; XF ERROR) (IDX:465)
  - `T01-T03` — FLAG SAME-FAMILY-ONLY (IDX:469)
  - `T03♯` — XF-VERIFIED (IDX:151)
- **K04** `R0_DIFF:73` · class NEW-E · The BB(1,p) prior has total mass one, size law w(k) = 1/[2·C(2p−1,k)], cap conditioning divides by W_K exactly once, and size masses decay geometrically with ratio ≤ p/(2p−1).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `T02(ii♯)` — XF-VERIFIED (IDX:462)
- `T02(i♯)` — XF-VERIFIED (IDX:460)

**Seat card status (verbatim):**

- A:127 — Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement; cited in the main setup. Rest unchanged.
- B:167 — Status: T03♯: PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2)); T01–T03: PROVED-LOCKED (wave 3; external review queued) SAME-FAMILY-ONLY; onset n ≳ 2·10⁶ disclosed. Repairs: none needed (PC1 §12 TRUE). Rest unchanged.
- C:159 — T03♯: **PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)**. T02(i♯), T02(ii♯): **PROVED; SF/XF VERIFIED**.
- D:102 — "PROVED (SF: VERIFIED (W2-VT03R); XF: VERIFIED (A-REV2))"; T01-T03 "PROVED-LOCKED (wave 3; external review queued)"

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :220 `A.C15; B.D13; D.M12` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :221 `B.D20, first two inequalities` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :222 `B.D20 explicit envelope clause` — AMBIGUOUS / DESIGN-ASSERTED / GAP
- `W1_PC2` — :170 `D8 · T03♯ restatement` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :171 `D8 · no beta-min` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- No CHK_INHERITED section targets S-T.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 2, TRUE 2, AMBIGUOUS 1.

*Adverse rows:* W1_PC1:220 (A.C15; B.D13; D.M12: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:222 (B.D20 explicit envelope clause: AMBIGUOUS, DESIGN-ASSERTED, GAP).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: n/a — statement is about the exact posterior; onset n ≳ 2·10⁶ disclosed (T03-1.2e5 ERROR on a smaller onset, R0_DIFF:207).

**Notes (with sources):**

- T01–T03 flag SAME-FAMILY-ONLY (`PROVED-LOCKED (wave 3; external review queued)`), restored in W2PC2:159. Scope: fixed s₀, p ≤ n^A, polynomial p; e^{Cn^α} OPEN (N12).

### S-Z — Supplement S-Z — evidence variance and masked tails (Theorem Z)

**Round 3 resolution (MINUTES §2.2):** K37–K41, K53; the terminal-off clause only in the exception-probability form (SYNTH_R2 §3 repair).

**HQ:** wave 4 · HQ `LP-REST` · charter `HQ_CHARTERS/LP-REST.md`. The range corollary waits for the actual-grid envelope of M2(b) (R3_C:288); the inherited variance work can proceed independently.

**Seat cards (R2):** A:133 (S4 Proposition Z); B:173–175 (S4 Theorem Z); D:110 (S6 evidence variance).

**K-IDs in this item:** K37 (island-minimum bound, Hoeffding bracket), K38 (Jensen), K39 (exact variance identity), K40 (masked lower tail (exception-probability form ≤ 2√δ₁)), K41 (favourable Ẑ/Z → 1), K53 ((vii) Var ≤ (T+1)e^{2D}/N, D = osc_Ω d).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K37** `R0_DIFF:126` · class NEW-DE · Sharper valid lower bounds on Z exist: the island-minimum bound δ_R·min_r Ẑ_r with δ_R = 0.05^{1/R}, and a two-sided Hoeffding bracket for Ẑ̄ once d⁻, d⁺ are certified.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row for the island-minimum bound or the Hoeffding bracket. INP I8 (Markov the only assumption-free bound) is seat-derived, unchecked [INP 284].
  - no registry/index ID is named in the cell
- **K38** `R0_DIFF:127` · class CONFIRMED-DE · E[log Ẑ_r] ≤ log Z (Jensen), with equality only for constant Ẑ_r, and averaging log estimates is not unbiased evidence pooling.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T12: PROVED-LOCKED (THEOREM_LIST.md V1(iii); THM-INV §1 row 9) [IDX 68]; A2(i) lists E[log Ẑ_r] ≤ log Z [LST 223]
  - `T12` — XF (IDX:68)
- **K39** `R0_DIFF:128` · class CONFIRMED-DE · The exact variance identity N·Var(W_T|𝓒) = Σ_s(1−1/N)^{T−1−s}(E[W_s²μ_s(h²_{s,T})]−1) holds for invariant kernels, and under exact refresh Var(W) = ∏(1+χ²_t/N) − 1 ≤ exp(Σχ²_t/N) − 1.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)) [IDX 169; REG 600]; OPW2-ThmB: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 170; REG 601]; OPW2-cex (COUNTEREXAMPLE): “PW2 with a_t = χ²_t (the 'perfect-mixing' guess) is false: minimal a₄* = 0.90 against χ²₄ = 0.111; and the constants of helpers/OPTIONAL_PW2.md (B)–(C) make T25(iv)'s B_T vacuous (≈ 1–223 vs truth ≤ 0.1) in every case.” [IDX 1012; REG 603]; MA-CorV: PROOF SKETCH [IDX 306]
  - `OPW2-ThmA` — XF-VERIFIED (IDX:169)
  - `OPW2-ThmB` — XF-VERIFIED*(qualified) (IDX:170)
  - `MA-CorV` — FLAG AUTHOR-ONLY (IDX:306)
- **K40** `R0_DIFF:129` · class CONFIRMED-DE · In the masked regime Ẑ underestimates Z by the log-odds overshoot of a late crossing (lower tail for any kernel, grid, N), and if the terminal population is off S₀ w.p. ≥ κ then Ẑ_r ≤ √δ₁·Z there.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MZ-E1E2: PROVED (E1, E2); 'Everything here is a candidate: not reviewed, not adopted' [IDX 184]; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)) [IDX 172; REG 576]; PC1c4: PROVED (C's COUNTEREXAMPLE valid) (PC1 claim 4) [IDX 188]
  - `MZ-E1E2` — FLAG AUTHOR-ONLY (IDX:184)
  - `FMP-Na` — XF-ADVERSE:GAP (no clean SF) (IDX:172)
  - `PC1c4` — XF (IDX:188)
  - `E1` — XF-VERIFIED (IDX:456)
  - `E2` — XF-VERIFIED (IDX:457)
- **K41** `R0_DIFF:130` · class DRAFT-ONLY · Under EX-A, EX-S, CAL, START, OUT and (T_n+1)Δ_n → 0, Ẑ/Z → 1 in probability on the output event in the favourable regime.
  - *R0_DIFF status cell (verbatim):* T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) [IDX 173; REG 274]; A2: Thm 6 overall CONJECTURE [LST 242]; T26-shorthand: — (SF: none; XF: GAP (A-REV4)) [IDX 176; REG 783]
  - `T26-shorthand` — FLAGGED-SUBCLAIM (SF none; XF GAP) (IDX:176)
  - `T26-ThmA` — XF-VERIFIED*(qualified) (IDX:173)
- **K53** `R0_DIFF:147` · class NEW-DE · Without design conditions Var(Ẑ_r/Z|𝓒) ≤ C_T/N with C_T = (T+1)e^{2D}; with Dobrushin/minorisation constants or a semigroup-stability condition the factors become explicit or O(T/N), which would bound the weight second moment M.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N4(iii): OPEN/CONJECTURE (V11 “resolved grid ⇒ O_P(√(T/N))”); lower bound M ≳ 1/P_𝓒(cross) PROOF SKETCH [INP 154]; FMP-M3: PROVED (SF: none; XF: ERROR (A-REV9)) [IDX 148; REG 572]
  - `FMP-M3` — XF-ADVERSE:ERROR (no clean SF) (IDX:148)

**Seat card status (verbatim):**

- A:133 — Status unchanged from R1 §D C6 (FMP-Na: PROVED (XF: GAP (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; (vii) E proposal unchecked). Supplement.
- B:175 — Status: OPW2-ThmA: PROVED (SF: none; XF: VERIFIED (A-REV9)); MZ-E1E2: PROVED (E1, E2), candidate: not reviewed, not adopted; FMP-Na: PROVED (SF: none; XF: GAP (A-REV9)); PC1c4: PROVED; T26-ThmA: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)); T26 overall CONJECTURE. Novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 unchecked (LIT-SMC §3A: "needs escalation"). Rest unchanged.
- D:110 — OPW2-ThmA "PROVED (SF: none; XF: VERIFIED (A-REV9))"; MZ-E1E2 "PROVED (E1, E2)" candidate

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :246 `A.C6(i,ii,iv,v,vi); B.D12(i,iii,iv,v); D.S6 corresponding clauses` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :247 `A.C6(iii); B.D12(ii) terminal-off clause` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :248 `B.D12(ii) E1/E2 path-tail formula; D.S6 masked tails` — AMBIGUOUS / DESIGN-ASSERTED / GAP; :249 `A.C6(vii); B.D12(vi); D.S6 crude bound` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :250 `D.S6 U_rest bracket` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / PLAUSIBLE
- `W2_PC1` — :182 `A.S4 · Z` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :194 `B.S3 · D; S4 · Z` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / GAP / REPAIRED; :207 `D.S6 · evidence / envelope` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY
- No CHK_INHERITED section targets S-Z.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 4, NEEDS-HYPOTHESIS 2, COUNTEREXAMPLE 1, AMBIGUOUS 1.

*Adverse rows:* W1_PC1:246 (A.C6(i,ii,iv,v,vi); B.D12(i,iii,iv,v); D.S6 corresponding clauses: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:247 (A.C6(iii); B.D12(ii) terminal-off clause: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:248 (B.D12(ii) E1/E2 path-tail formula; D.S6 masked tails: AMBIGUOUS, DESIGN-ASSERTED, GAP); W1_PC1:249 (A.C6(vii); B.D12(vi); D.S6 crude bound: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:250 (D.S6 U_rest bracket: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, PLAUSIBLE); W2_PC1:194 (B.S3 · D; S4 · Z: TRUE-AS-WRITTEN, DESIGN-VERIFIED, GAP, REPAIRED).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: any frozen grid; D := osc_Ω d bounded by M2(a) (A:133(vii))
- Ẑ-weighted pooling / partition: Ẑ_r island evidence

**Notes (with sources):**

- FMP-M3 (K53 area) is `PROVED (SF: none; XF: ERROR (A-REV9))` and marked 'Do not cite M3' (R0_DIFF:147). OPW2-cex refutes the perfect-refresh product formula; PC1 claim 4 wording is mandatory for the terminal-off clause (A:133(iii)). Novelty of (i) vs Cérou–Del Moral–Guyader Thm 1.4 unchecked (B:175).

### S-TARGET — Supplement S-TARGET — propriety, invariance, envelopes, exact branch

**Round 3 resolution (MINUTES §2.2; R3-4 unanimous):** K95 (odds certificate) is placed here; K23 is not here (FUTURE_WORK).

**HQ:** wave 1 · HQ `LP-FOUND` · charter `HQ_CHARTERS/LP-FOUND.md` (S-TARGET + S-BLOCKS + S-KERNEL, S-T cited; MINUTES §2.5).

**Seat cards (R2):** A:135 (S5 TARGET); B:185–187 (S7 TARGET); C:193–202 (C12); D:105–107 (S1 target lemmas / S3 decision rules / S12).

**K-IDs in this item:** K01 (propriety, envelopes), K02 (invariance/equivariance (target only)), K03 (contrast regression, 2νb₀), K04 (BB(1,p) mass), K05 (monotone superset bound), K76 (eventual exact dispatch), K95 (odds certificate (η < 1)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K01** `R0_DIFF:70` · class NEW-DE · The posterior is a proper law for every admissible X, y (rank-deficient X_S included), with explicit envelopes on Q_S, the determinant term and log BF.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row for TG1/T02. Related: N17 PROVED (PC1 claim 1; PC2 C1(c)) [INP 248; IDX 902].
  - `PC2` — XF (IDX:731)
- **K02** `R0_DIFF:71` · class NEW-DE · The posterior, Z/m(∅) and PIPs are invariant under per-column and response affine maps and equivariant under column permutations; per-seed output is equivariant only in law, and dropped constants are outside the estimand.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N12 tiny n: n = 2 extension PROOF SKETCH (R2C E1), p-fold-tie statement “seat-derived, unchecked” [INP 213].
  - `E1` — XF-VERIFIED (IDX:456)
- **K03** `R0_DIFF:72` · class NEW-DE · The working posterior equals the contrast-regression posterior with IG(a₀+½, b₀s_y²) noise, and replacing b₀ by 0 shifts any pairwise log Bayes factor by at most 2νb₀|1/Q₁−1/Q₂|.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K04** `R0_DIFF:73` · class NEW-E · The BB(1,p) prior has total mass one, size law w(k) = 1/[2·C(2p−1,k)], cap conditioning divides by W_K exactly once, and size masses decay geometrically with ratio ≤ p/(2p−1).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K05** `R0_DIFF:74` · class NEW-D · For S ⊆ S′ the fit Q and the log-determinant term are monotone, giving a computable upper bound on every score between S and S∪R (leaps-and-bounds superset bound).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K76** `R0_DIFF:175` · class NEW-DE · For fixed p the exact branch is eventually taken (2^p-state enumeration below the (5H₀+4N₀)p threshold), returning exact Z, PIPs and HPM, and on that branch global_certified is exact modulo arithmetic.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T26-exact-branch-paren (—): “XF: **ERROR** — A-REV4 · REVIEW.md verdict table §7 ERROR: false under the actual budgets (p = 18, n = 2¹⁸: K = p, 2¹⁸ states, threshold (5H₀+4N₀)p exceeds the state count, so the exact branch IS taken); fixed p eventually enumera…” [IDX 1058; REG 784]; N12: eventual exact dispatch (R2C §4.4) seat-proved, unchecked [INP 214]
  - no registry/index ID is named in the cell
- **K95** `R0_DIFF:209` · class NEW-E · Finite-data posterior odds give exact certificates: π(S₀) = 1/(1+A(S₀)), and A(S₀) ≤ η < 1 implies HPM = MPM = S₀ with PIPs ≥ 1/(1+η) on true and ≤ η/(1+η) on false coordinates.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Seat card status (verbatim):**

- A:135 — Status: N17 PROVED; rest D/E proposals, TRUE-AS-WRITTEN (PC1:300); T01 reduction PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY. Supplement.
- B:187 — Status: N17: PROVED (PC1 claim 1); T01 reduction: PROVED-LOCKED (wave 3; external review queued); N12 eventual dispatch: seat-proved, unchecked; T26-exact-branch-paren: XF ERROR (corrected). Rest unchanged.
- C:198 — N17: **PROVED**. T01: **PROVED-LOCKED (wave 3; external review queued); SAME-FAMILY-ONLY**. Remaining assembly: **PROOF SKETCH, unchecked**.
- D:105 — unchanged
- D:107 — unchanged

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :300 `A.C1(i,iii,iv,v); B.D17 target/BB/reduction; D.S1 target/BB/reduction` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :301 `A.C1(ii); D.S1 permutation law; B.D17 tie caveat` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :302 `A.S5; D.S3; A.C7(d,e); B.D8(4)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :303 `A.S1(e); B.D17 fixed p; D.S12 fixed p/tiny n` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :304 `B.D17 odds certificate` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :212 `D11 · propriety and envelopes (E:T02)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :213 `D11 · invariance (E:T01)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :214 `D11 · contrast regression` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :215 `D11 · exact branch (E:T04)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :216 `D11 · IG perturbation` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :183 `A.S5 · TARGET; S7 · POOL` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :198 `B.S7 · TARGET; S8 · CERT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :206 `D.S1,S2,S4 · target/graph/output` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :159 `C12 · repairs` — statement ot / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- No CHK_INHERITED section targets S-TARGET.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 6, TRUE 5, AMBIGUOUS 1, NEEDS-HYPOTHESIS 1, statement ot 1.

*Adverse rows:* W1_PC1:301 (A.C1(ii); D.S1 permutation law; B.D17 tie caveat: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:304 (B.D17 odds certificate: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** `T07Bayes.lean` covers Prop1-T07 (Bayes rules, size-prior ceiling; K60) — 39 declarations, 28 theorems, 0 `sorry` in SmcBvs/SmcBvs; the `frozen/v1` and `fidelity/packet` copies have 12 `sorry` (REGISTRY_INDEX.md:927, :934, :943, §3.3). None of K01–K05, K76, K95 has a Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: target is M §5 as shipped (METHOD:298–300); exact branch threshold METHOD:318 row 21 (fixed-p eventually exact: W1PC1:303 TRUE).

**Notes (with sources):**

- N17 (K44) is `PROVED (PC1 claim 1; PC2 C1(c))` [R0_DIFF K44]. N12 eventual dispatch 'seat-proved, unchecked'; T26-exact-branch-paren XF ERROR (corrected). K02 equivariance is target-only: algorithmic output need not be equivariant even in law under ties (W1PC1:301 AMBIGUOUS).

### S-KERNEL — Supplement S-KERNEL — N9 kernel facts, neighbour graph, start sampler, tie-DP, minorisation

**Round 3 resolution (MINUTES §2.2, §2.3; R3-4):** N9 kernel facts with the CHK amendments; K09 is the tie-DP proposition (C10); **K23 is FUTURE_WORK** (A, B, D; the K23 entry below is kept for provenance). **Dissent C:** keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL (R3_C §S1); recorded; the HQ may cite it as an attributed lemma without a theorem number (MINUTES §2.3). The N3 DP invariant is a named premise (§8).

**HQ:** wave 1 · HQ `LP-FOUND` · charter `HQ_CHARTERS/LP-FOUND.md`

**Seat cards (R2):** A:137 (S6 PAR (K09 here); S10 (A:145)); B:177–179 (S5 KERNEL); C:166–175 (C10 (K09)); D:106 (S2 start machinery; S8 (D:112)).

**K-IDs in this item:** K20 (moves reversible), K21 (round invariant/self-adjoint), K08 (exact Z̄₀, backward sampler), K09 (tie-DP (N3 OPEN)), K22 (graph facts), K103 (minorisation (also M2)), K23 (Dirichlet comparison — FUTURE_WORK (R3-4); entry kept for provenance; C dissent recorded).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K20** `R0_DIFF:99` · class CONFIRMED-DE · The Gibbs flip (with cap), uniform swap, neighbour swap (Hastings ratio |N(j)∖S|/|N(l)∖S′|) and the π₀-independence step are each reversible with respect to q_φ at every φ.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]; V1(iii): V5 “has no registry row” [LST 77]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K21** `R0_DIFF:100` · class CONFIRMED-DE · The uniformly-random-order round kernel is q_φ-invariant and self-adjoint on L²(q_φ), so the bridge is a Feynman–Kac model with multinomial resampling.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]; V1(iii): V5 “has no registry row” [LST 77]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K08** `R0_DIFF:82` · class NEW-DE · The start normaliser Z̄₀ is computed exactly by size convolution and a backward sampler returns iid draws from π₀, invariant to block packing order.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N9: “by construction, consultant-checked, no registry row” [INP 192]; T09: PROVED-LOCKED (wave 1) -- THEOREM_LIST.md V1(iii) says V5 'has no registry row' [IDX 71]; N9K: Each of: Gibbs flip, uniform swap, neighbour swap, independence move γ_φ-reversible; uniform random order self-adjoint; draw_pi0 exact; Z̄₀ exact — all 'PROVED (candidate… [IDX 72]
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **K09** `R0_DIFF:83` · class NEW-DE · The max-plus DP over blocks returns the prescribed smallest-size, lexicographically smallest maximiser of π₀ without enumerating ties.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N3 sub-obligation (DP invariant): OPEN; R3A/R3B greedy-DP route unchecked [INP 146].
  - no registry/index ID is named in the cell
- **K22** `R0_DIFF:101` · class NEW-DE · The symmetrised capped neighbour graph has no isolated vertex, at most pB edges, positive reverse proposal probabilities, and about p/√(log p) spurious edges for independent Gaussian columns.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K103** `R0_DIFF:232` · class NEW-DE · The independence step minorises every round, Q_φ(S,·) ≥ π_φ/(mM_φ) (D) or ≥ π_φ/M_φ (E), with M_φ ≤ exp{φ(d_max − E_{π₀}d)}, so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1−ε_φ)^k and the L terminal rounds have an explicit TV bound.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N10: NONE / OPEN (INV row 6) [INP 199].
  - no registry/index ID is named in the cell
- **K23** `R0_DIFF:102` · class NEW-D · The random-order round has Dirichlet form ≥ ½ that of the random-scan mixture R₂, hence gap(Q_φ) ≥ ½·gap(R₂).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `MA-PropW` — FLAG AUTHOR-ONLY (IDX:92)
- `MA-Wcal` — FLAG AUTHOR-ONLY (IDX:93)
- `IND-T` — XF-VERIFIED*(qualified) (IDX:85)

**Seat card status (verbatim):**

- A:137 — **S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
- B:179 — Status: N9K: PROVED (candidate), N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT (PC1, cross-family); T09: PROVED-LOCKED (wave 1); N3: OPEN; K22, K23, K103: PROVED (by this seat, unchecked), PC1 §19 TRUE-AS-WRITTEN. Rest unchanged.
- C:170 — Proposed finite mathematical proposition: **PROOF SKETCH, unchecked**. Registry N3’s integrated tie-DP invariant remains **OPEN**; it is not being listed as a proved implementation theorem.
- D:106 — unchanged

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :289 `A.S6(a); B.D16 Dirichlet clause` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :290 `A.S6(b); B.D16 minorisation; D.S8 minorisation` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :291 `A.S6(c); B.D16 graph; D.S2 graph` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :292 `A.S1(d); B.D16 tie-DP; D.S2 tie-DP` — AMBIGUOUS / DESIGN-ASSERTED / GAP; :293 `B.D21; D.S2 block/table clauses` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :294 `A.S1(a,b,c); D.S4 worker/stacking clauses` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE
- `W1_PC2` — :198 `D9 · greedy tie DP` — TRUE / DESIGN-ASSERTED / PLAUSIBLE; :204 `D10 · separation (E:T05)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :205 `D10 · counting` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :206 `D10 · graph (E:T08)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :186 `A.S10 · KL/TV/BLOCKS` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :195 `B.S5 · KERNEL; S9 · IDENT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :206 `D.S1,S2,S4 · target/graph/output` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :157 `C10 · IC3 exhibit` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :158 `C11 · equality` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `CHK_INHERITED/REPORT.md:15` — N9-KERNEL §§0–3 **VERIFIED WITH AMENDMENT** (section CHK:130–176; verdict line CHK:134).

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 9, TRUE 4, NEEDS-HYPOTHESIS 1, AMBIGUOUS 1.

*Adverse rows:* W1_PC1:291 (A.S6(c); B.D16 graph; D.S2 graph: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:292 (A.S1(d); B.D16 tie-DP; D.S2 tie-DP: AMBIGUOUS, DESIGN-ASSERTED, GAP); W1_PC1:294 (A.S1(a,b,c); D.S4 worker/stacking clauses: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC2:198 (D9 · greedy tie DP: TRUE, DESIGN-ASSERTED, PLAUSIBLE).

**Lean:** No Lean file for kernel facts. Proposals: detailed balance of four kernels (D:61). T12Core is the island-recursion core, not N9.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: kernels/start as coded: CHK:134 checks claims G, U, N, I, R, Z, S against code at the named commit; no implementation change indicated. T09 `PROVED-LOCKED (wave 1)` supplies the abstract kernel core.

**Notes (with sources):**

- C10's IC3 tie exhibit (n = 40, p = 20, duplicated columns) reproduces the seat script exactly (W2PC2:157); N3 integrated tie-DP invariant stays OPEN (C:170).
- REGISTRY_INDEX §5.B B2 (C-V5): THEOREM_LIST says V5 has 'no registry row'; LOCKED_PROOFS row T09 states it; branch N9-KERNEL holds a candidate PROOF.md — recorded as a source CONFLICT.

### S-CERT — Supplement S-CERT — local search, certificate semantics, B&B soundness, perturbation

**Round 3 resolution (MINUTES §2.2; R3-8):** K73 is stated without the region-certification clause (C's withdrawal). K-IDs: K64, K73, K74, K05, K108.

**HQ:** wave 3 · HQ `LP-AUDIT` · charter `HQ_CHARTERS/LP-AUDIT.md` (S-CERT + S-OUT; MINUTES §2.5). Search semantics feed M5 and M8.

**Seat cards (R2):** A:141 (S8 CERT); B:189–191 (S8 CERT); D:113 (S9 search/certificates).

**K-IDs in this item:** K64 (scans ≤ ℓ+1, local_certified semantics), K73 (B&B soundness (no region certificate clause)), K74 (local ≠ global limitation), K05 (superset bound), K108 (perturbation lemma ε ⇒ TV ≤ tanh ε).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K64** `R0_DIFF:163` · class NEW-DE · Local search moves only on strict F improvement, makes at most ℓ+1 scans of at most p + |S|(p−|S|) models, and local_certified/local_limit have exact semantics (a flip/swap strict local maximum at the scanned centre).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N7: L1 (C3(a)) CORRECT WITH AMENDMENT; L2 PROVED [INP 176]; INP row 12 bound (ℓ+1)(p+k*(p−k*)), k* = min(K,⌊p/2⌋) [INP 305]
  - no registry/index ID is named in the cell
- **K73** `R0_DIFF:172` · class NEW-DE · Branch-and-bound over a declared region with a certified upper bound on subtree scores is exact when it completes, “unresolved” on budget exhaustion, and certifies nothing outside the region.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)) [IDX 744; REG 403]; OCERT-C4: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED* (A-REV9)) [IDX 748; REG 407]; N7: R (C4 + Lemma M) PROVED with amendments; “FALSE or not a theorem”: rigorous global_certified [INP 176, 178]
  - `OCERT-LemmaM` — XF-VERIFIED (IDX:744)
  - `OCERT-C4` — XF-VERIFIED*(qualified) (IDX:748)
- **K74** `R0_DIFF:173` · class NEW-DE · A strict flip/swap local maximum can lie far below the mode, a complete local scan does not certify proper-subset gaps (2^k − 1 subsets), and local success is not global success.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). CEX-localmax(A2) (COUNTEREXAMPLE): “A suppressor design (and a production-table-compatible variant) ends certified at an inferior local maximum: failures of delivery are not exhausted by 'posterior miss' or 'never in E_LS'.” [IDX 992; REG 162]; CEX2 (COUNTEREXAMPLE): “A search can start below S₀, climb to a superset and certify it: a final-search failure does not imply the initial centre already beat S₀.” [IDX 990; REG 160]
  - `CEX2` — XF-VERIFIED (IDX:513)
- **K05** `R0_DIFF:74` · class NEW-D · For S ⊆ S′ the fit Q and the log-determinant term are monotone, giving a computable upper bound on every score between S and S∪R (leaps-and-bounds superset bound).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K108** `R0_DIFF:242` · class NEW-E · If every log mass is perturbed by at most ε then Z̃/Z ∈ [e^{−ε}, e^{ε}], TV(π̃, π) ≤ tanh ε, a winner with gap > 2ε is unchanged, and kernel errors δ_t accumulate by path coupling as Σδ_t.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Seat card status (verbatim):**

- A:141 — Status unchanged from R1 §D C16/S4. Supplement.
- B:191 — Status: N7 L1: CORRECT WITH AMENDMENT; OCERT-LemmaM: PROVED (SF: VERIFIED (O-VCERT); XF: VERIFIED (A-REV9)); OCERT-C4: PROVED (XF: VERIFIED*). Rest unchanged.
- D:113 — N16 "OPEN"

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :271 `A.C16(a,b,d,e); B.D18 B&B; D.S9 L2/L3/R/local limitation` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE; :272 `A.C16(c); B.D18 local clause` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :273 `A.C16(c); B.D18 scan count; D.S9 count` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :274 `B.D18 rounding; D.S9 rounding` — NEEDS-HYPOTHESIS / NONE-GIVEN / GAP
- `W1_PC2` — :115 `D5 · region certification` — TRUE / DESIGN-ASSERTED / GAP
- `W2_PC1` — :184 `A.S8 · CERT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :198 `B.S7 · TARGET; S8 · CERT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :130 `C4 · repairs` — REPAIRED DIFFERENTLY
- No CHK_INHERITED section targets S-CERT.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 4, COUNTEREXAMPLE 1, NEEDS-HYPOTHESIS 1, TRUE 1, (repair-only or blank row) 1.

*Adverse rows:* W1_PC1:271 (A.C16(a,b,d,e); B.D18 B&B; D.S9 L2/L3/R/local limitation: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W1_PC1:272 (A.C16(c); B.D18 local clause: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:274 (B.D18 rounding; D.S9 rounding: NEEDS-HYPOTHESIS, NONE-GIVEN, GAP); W1_PC2:115 (D5 · region certification: TRUE, DESIGN-ASSERTED, GAP).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: yes — certificate attaches to the returned Ŝ from whichever search ended on it incl. LS0 (METHOD:152 #10); LS0 not yet in production core.
- Coded grid: n/a
- Ẑ-weighted pooling / partition: n/a. K107 (rounding bound) → FUTURE_WORK (N16 OPEN; T33-errbound COUNTEREXAMPLE). 'Certified' reserved for validated arithmetic (METHOD:184 e5).

**Notes (with sources):**

- K73 region certification: W1PC2 D5 DESIGN-ASSERTED/GAP → W2PC2:130 REPAIRED DIFFERENTLY (withdrawn). OCERT-C1 is `XF ERROR as quantified` (B:121). local_certified = no strictly improving neighbour at the scanned centre, ties allowed (A:141; W1PC1:272 COUNTEREXAMPLE of the 'strict local maximum' reading).

### S-LIM — Supplement S-LIM — limitations as theorems

**Round 3 resolution (MINUTES §2.2; R3-3):** K79, K81, K100, K101 as theorems; K99 as a qualitative remark (the quantitative k-way barrier is FUTURE_WORK). Duplicates: PIP = E[# selected in group]/d (d = number of interchangeable duplicates; NOTATION.md proposes s_dup); numeric limits only with their p qualification. K97 is FUTURE_WORK.

**HQ:** wave 4 · HQ `LP-REST` · charter `HQ_CHARTERS/LP-REST.md` (S-Z + S-POOL + S-LIM; MINUTES §2.5).

**Seat cards (R2):** A:143 (S9 LIM); B:181–183 (S6 LIM); D:115 (S11 limitations).

**K-IDs in this item:** K79 (no run diagnostic certifies absence of unseen modes), K81 (genealogical collapse with ESS = N), K100 (duplicates: PIP = E[#selected in group]/d (numeric 2/3 only for p = 2; 3/5 with an orthogonal null)), K101 (MPM may exceed K), K99 (qualitative barrier (remark); quantitative → FUTURE_WORK).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K79** `R0_DIFF:183` · class CONFIRMED-DE · No diagnostic computed from the run (island agreement, ESS, grid convergence, local-search flags) certifies the absence of unseen modes: changing an unqueried state’s mass leaves the whole transcript unchanged.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MZ-E1E2: PROVED (E1, E2); 'Everything here is a candidate: not reviewed, not adopted' [IDX 184]; INP I5: MASKZPIP E1c PROVED; V12 [INP 271]
  - `MZ-E1E2` — FLAG AUTHOR-ONLY (IDX:184)
  - `E1` — XF-VERIFIED (IDX:456)
  - `E2` — XF-VERIFIED (IDX:457)
- **K81** `R0_DIFF:185` · class NEW-E · Flat weights do not prevent genealogical collapse: with ESS = N throughout, two lineages coalesce within t resampling steps w.p. 1 − (1−1/N)^t.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). CEX-ESSneutral(A3) (COUNTEREXAMPLE): “Two states, d = 0, identity moves, multinomial resampling: every interval has ESS ratio one, yet for fixed N repeated neutral resampling loses one class: an ESS condition alone is not a delivery theorem (abstract, not BVS).” [IDX 1011; REG 564]
  - no registry/index ID is named in the cell
- **K100** `R0_DIFF:219` · class NEW-DE · For exact or near duplicate columns PIPs are equal; with d interchangeable predictors PIP → 1/d while group inclusion → 1 (the MPM excludes all for d ≥ 3), no estimator can tell which duplicate generated the data, and |S₀| > K has…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row; related (duplicates): PropD-T03 (COUNTEREXAMPLE): “With duplicated columns the posterior size-tail does not vanish at cutoff s₀+O(1): the target 'm_n = s₀+O(s₀ log n/log p)' is false without SE.” [IDX 987; REG 135]; CEX-ties(A2) (COUNTEREXAMPLE): “With duplicate columns (exact ties) TD′_P holds but the strict-separation event D_S fails: D_S is sufficient, not necessary.” [IDX 991; REG 161]
  - `PropD-T03` — XF-VERIFIED (IDX:464)
- **K101** `R0_DIFF:220` · class NEW-DE · The exact MPM can exceed K (size < 2K) and then is not a model in 𝕊_K; the cap-constrained Hamming action picks up to K largest PIPs above ½; HPM and MPM differ in general.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K99** `R0_DIFF:218` · class NEW-DE · Cross-block masked contrasts in a saturated cluster (> B members) of order k ≥ 4 are unreachable at the production budget (≤ W·(2p)^{−k}) while every diagnostic passes, and no fixed budget works uniformly over designs and signals.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row; related: SHARE-PB (COUNTEREXAMPLE): “A posterior barrier defeats (b2), LS0 and T39 alike: no method change helps.” [IDX 1001; REG 350]; INP I9(c),(d),(e) definitional limits [INP 274]
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `CEX2` — XF-VERIFIED (IDX:513)

**Seat card status (verbatim):**

- A:143 — **S9 · Proposition LIM (K79, K81, K100, K101).** (a), (b), (d) unchanged from R1 §D S3. (c) duplicates: d interchangeable columns have equal PIPs with PIP = E[number selected in the group]/d; the limit is 1/d only if exactly one is included asymptotically; under the ridge/BB target with two duplicates and fixed noise the limit is 2/3 (PC1:281); group inclusion → 1. Supplement.
- B:183 — Status: CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB: COUNTEREXAMPLE (constructions); INP I5 PROVED. Rest unchanged from R1 §D D15.
- D:115 — unchanged

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :280 `A.S3(a,b,d); B.D15(a,b,c,f); D.S11 except duplicates` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :281 `A.S3(c); B.D15(e); D.S11 duplicates` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :282 `B.D15(d)` — NEEDS-HYPOTHESIS / NONE-GIVEN / IMPLAUSIBLE; :283 `B.D15(g)` — NEEDS-HYPOTHESIS / NONE-GIVEN / GAP
- `W2_PC1` — :185 `A.S9 · duplicate numeric limit` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :196 `B.S6 · withdrawals` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :197 `B.S6 · duplicate numeric limit` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY; :209 `D.S9,S11 · rounding/duplicates` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- No CHK_INHERITED section targets S-LIM.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 3, COUNTEREXAMPLE 3, NEEDS-HYPOTHESIS 2.

*Adverse rows:* W1_PC1:281 (A.S3(c); B.D15(e); D.S11 duplicates: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:282 (B.D15(d): NEEDS-HYPOTHESIS, NONE-GIVEN, IMPLAUSIBLE); W1_PC1:283 (B.D15(g): NEEDS-HYPOTHESIS, NONE-GIVEN, GAP); W2_PC1:185 (A.S9 · duplicate numeric limit: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE, REPAIRED DIFFERENTLY); W2_PC1:197 (B.S6 · duplicate numeric limit: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE, REPAIRED DIFFERENTLY).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: n/a

**Notes (with sources):**

- Registry constructions (COUNTEREXAMPLE rows): CEX-localmax(A2), CEX2, CEX-ESSneutral(A3), PropD-T03, SHARE-PB (B:183). W2PC1 duplicate numeric limit COUNTEREXAMPLE without p = 2 (A.S9 :185, B.S6 :197) — repaired form in S2:265.

### S-POOL — Supplement S-POOL — pooling, equal-weight PIP, R_eff

**Round 3 resolution (MINUTES §2.2; R3-8):** pooling rules, the checked recording-marginal equal-weight bias comparison P1 (K57-P1), R_eff. **K57 is split:** P1 stays here; the general K57 accuracy statement is FUTURE_WORK (B, C). K-IDs: K49, K50, K54, K56, K57-P1 (K50 is also an M1 clause).

**HQ:** wave 4 · HQ `LP-REST` · charter `HQ_CHARTERS/LP-REST.md`

**Seat cards (R2):** A:139 (S7 POOL); B:197–199 (S10 PIP-eq); D:109–111 (S5 pooling; S7 equal-weight P1).

**K-IDs in this item:** K49 (equal-weight PIP bias), K50 (pooled product not unbiased), K54 (R_eff, ratio-sandwich variance), K56 (RB variance), K57 (split: P1 only — equal-weight bias ≤ TV of one-record marginal; general accuracy FUTURE_WORK (R3-8)), K55 (fixed-grid CLTs (cited in S-IDENT)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K49** `R0_DIFF:143` · class CONFIRMED-DE · The equal-weight PIP average converges to E[PIP̂_1j|𝓒], which differs from PIP_j at fixed N (bias of order 1/N that does not vanish in R).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropP: PROVED (elementary) [IDX 70]; INP I10: Prop P(i) PROVED (candidate) [INP 275]
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **K50** `R0_DIFF:144` · class CONFIRMED-E · The product Ẑ̄·PIP^eq is not unbiased: E[Ẑ̄·PIP^eq_j] − Z·PIP_j = −(1−1/R)·Cov(Ẑ₁, PIP̂_1j | 𝓒).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). Prop2(c): PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED (A-REV4)) [IDX 61; REG 261]; MA-PropP: PROVED (elementary) [IDX 70]; REG retired: “‘E[Ẑ | completed] = Z’ and ‘pooled Ẑ × pooled PIP is unbiased’ — both false (CEX-guard, Prop2(c))” [REG 818; IDX 1123]
  - `CEX-guard` — XF-VERIFIED*(qualified) (IDX:128)
  - `Prop2(c)` — XF-VERIFIED (IDX:61)
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **K54** `R0_DIFF:148` · class NEW-DE · R_eff = (ΣẐ_r)²/ΣẐ_r² is the Kish effective island number, R_eff/R → Z²/E[Ẑ²|𝓒], and a ratio-sandwich variance estimator is consistent as R grows.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. INP N4 “Supports: R_eff reporting” [INP 155].
  - no registry/index ID is named in the cell
- **K56** `R0_DIFF:150` · class NEW-DE · Rao–Blackwellised PIP records have variance no larger than the indicator average (one step), and under perfect mixing Var(PIP̂) ≤ PIP(1−PIP)/(4N).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K57** `R0_DIFF:151` · class DRAFT-ONLY · The equal-weight PIP’s bias is ≤ TV(law of the delivered population, π); after locking (all particles at S₀) the bias is ≤ δ₁ and the L¹ error ≤ (L+4)ρ̄ + u_π + δ₁.
  - *R0_DIFF status cell (verbatim):* MZ-P1P2: P1 PROVED; P2 PROVED as a composition of locked T23(ii) and T12 (R3) [IDX 224]; OBG-BG3: PROVED (SF: none; XF: VERIFIED (A-REV7)) [IDX 219; REG 612]; OBG-LH-lock: PROOF SKETCH (SF: none; XF: VERIFIED* (A-REV7)) [IDX 220; REG 614]; OBG-LH-lock-general (—): “XF: **ERROR** — A-REV7 · REVIEW.md §5: ERROR. One pair, g = 4, ρ = 0.85, ψ = 0.5, β_a = 1.4, β_b = −0.7: the swap 0 → 4 improves the population fit by 0.00479, so C2 fails for allowed LH parameters (also g = 9). It is not a counte…” [IDX 1061; REG 789]
  - `OBG-LH-lock-general` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:566)
  - `OBG-LH-lock` — XF-VERIFIED*(qualified) (IDX:220)
  - `OBG-BG3` — XF-VERIFIED (IDX:219)
  - `MZ-P1P2` — FLAG AUTHOR-ONLY (IDX:224)
  - `T12` — XF (IDX:68)
- **K55** `R0_DIFF:149` · class NEW-DE · For a fixed grid, √N(Ẑ_r/Z−1), √N(PIP̂−PIP) and ratio estimators are asymptotically normal in N (Feynman–Kac variances), and the stacked ratio estimator has a √R CLT.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `ADRAFT-ThmA` — ASTRA-ONLY (Astra-on-Astra; XF none) (IDX:62)
- `MA-CorV` — FLAG AUTHOR-ONLY (IDX:306)

**Seat card status (verbatim):**

- A:139 — Status unchanged (MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); ADRAFT-ThmA Astra-only, cite Del Moral; MZ-P1P2: P1 PROVED; OBG-LH-lock-general: XF ERROR). Supplement.
- B:199 — Status: MA-PropP: PROVED (elementary), author-only; Prop2(c): PROVED (XF VERIFIED); MZ-P1P2: P1 PROVED; MA-CorV: PROOF SKETCH. Rest unchanged.
- D:109 — unchanged
- D:111 — MZ-P1P2 "P1 PROVED; P2 PROVED as a composition"

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :236 `A.C4(i–vi); B.D14 first two clauses; D.S5` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :237 `A.S2; B.D14 TV clause; D.S7` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :238 `B.D14 final clause` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :239 `B.D19 R_eff/sandwich/CLT clauses` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :240 `A.C4(ii)` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :183 `A.S5 · TARGET; S7 · POOL` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :199 `B.S10 · PIP-eq` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- No CHK_INHERITED section targets S-POOL.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 5, AMBIGUOUS 1, NEEDS-HYPOTHESIS 1.

*Adverse rows:* W1_PC1:237 (A.S2; B.D14 TV clause; D.S7: AMBIGUOUS, DESIGN-VERIFIED, GAP); W1_PC1:240 (A.C4(ii): NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: yes: Ẑ-weighted primary PIP and equal-weight secondary are both shipped (METHOD:158 #11); 'neither normalised estimate is generally unbiased at finite budget'; R_eff reported.

**Notes (with sources):**

- MA-PropP `PROVED (elementary)` AUTHOR-ONLY candidate; ADRAFT-ThmA ASTRA-ONLY (Astra-on-Astra; citing a standard fixed-grid lemma does not upgrade it, W1PC1 ledger S14, VERDICTS.md:92); MZ-P1P2 `P1 PROVED; P2 PROVED as a composition`; OBG-LH-lock-general XF ERROR; FMP-DELIVPOP OPEN.

### S-IDENT — Supplement S-IDENT — restricted-ESS coverage identity, TI/KL/TV calculus, approximation corollaries

**Round 3 resolution (MINUTES §2.2, §2.3; R3-4):** K33 is in M7, not here (D's dissent recorded). S-IDENT carries the **C15-CI posterior-content credible-set clause, named** (seat B's 'missing' item 1, `R3_B.md` §S4; HQ ruling Q2: the §5.4 coverage reading is posterior-content / Monte Carlo error; the frequentist half is FW1), together with K25 (lemma), K104, K55, K103 (the TV/KL/TV calculus; C15-TV, C15-KL). Check row for the clause: W2_PC2:161 `C15-CI · new form` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED (statement-sanity verdict). Edge direction M2 ↔ S-IDENT differs between seats (§5).

**HQ:** wave 2 · HQ `LP-IDENT` · charter `HQ_CHARTERS/LP-IDENT.md` (S-IDENT; S-STGI dissolved, MINUTES §2.2).

**Seat cards (R2):** A:145 (S10 KL/TV and BLOCKS); B:193–195 (S9 IDENT); C:224–253 (C15-TV, C15-KL, C15-CI; C8 (C:138)); D:112 (S8 Doeblin/calculus).

**K-IDs in this item:** K25 (lemma), K104 (exponential-family identities, Λ_len = ∫sd dφ ≤ √J), K55 (fixed-grid CLTs), K103 (minorisation/TV ≤ (1−1/M_φ)^L; useful iff M₁ = O(1)). **C15-CI** (named clause: posterior-content credible-set; no K-ID; `R3_B.md` §S4 item 1).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K25** `R0_DIFF:109` · class NEW-DE · The stage ESS fraction is 1/(1+χ²), and the full ESS equals the restricted-set ESS times the exact coverage factor a_u·a_w/a_v² (a_t = q_t(V), w = 2v−u), so a restricted ESS ≥ 0.9 certifies the full bridge only up to the missing m…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N5(b2) OPEN [INP 161]; INP I9(d) [INP 274]
  - no registry/index ID is named in the cell
- **K104** `R0_DIFF:233` · class NEW-DE · π_φ is an exponential family in d: (log Z_φ)′ = E d, (log Z_φ)″ = Var d, log(Z/(m(∅)Z̄₀)) = ∫E_{π_φ}d, KL(π‖π₀) + KL(π₀‖π) = J = ∫Var_{π_φ}(d)dφ, J = 0 iff π₀ = π, and Λ ≤ √J.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K55** `R0_DIFF:149` · class NEW-DE · For a fixed grid, √N(Ẑ_r/Z−1), √N(PIP̂−PIP) and ratio estimators are asymptotically normal in N (Feynman–Kac variances), and the stacked ratio estimator has a √R CLT.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K103** `R0_DIFF:232` · class NEW-DE · The independence step minorises every round, Q_φ(S,·) ≥ π_φ/(mM_φ) (D) or ≥ π_φ/M_φ (E), with M_φ ≤ exp{φ(d_max − E_{π₀}d)}, so ‖Q_φ^k(S,·) − π_φ‖_TV ≤ (1−ε_φ)^k and the L terminal rounds have an explicit TV bound.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. N10: NONE / OPEN (INV row 6) [INP 199].
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `PART-ThmA` — XF-VERIFIED*(qualified) (IDX:768)
- `OWS-WS1` — FLAG AUTHOR-ONLY (IDX:402)

**Seat card status (verbatim):**

- A:145 — Status: D/E proposals TRUE-AS-WRITTEN at the cited rows; OWS-WS1 PROVED (no review).
- B:195 — Status: PROVED (by this seat, unchecked); OWS-WS1: PROVED (SF: none; XF: none); PC1 §14, §16 TRUE-AS-WRITTEN. Rest unchanged.
- C:228 — Production-round/record assembly: **PROOF SKETCH, unchecked**. Independence-sampler foundation: **KNOWN—CITE**.
- C:238 — **PROOF SKETCH, unchecked** assembly; elementary divergence foundations cited.
- C:249 — **PROOF SKETCH, unchecked**.
- D:112 — PC2 D15-TV TRUE

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :256 `A.S4(a); B.D19 calculus; D.S8 calculus; all §F KL identities` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :257 `A.S4(a); B.D19, Λ≤sqrt(J)` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :258 `A.S4(b); B.D18 perturbation; D.S9 perturbation; all §F` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :259 `A.§F restricted TV/KL and fixed-data limits` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :260 `A.§F reverse KL` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :261 `B.§F TV(b); D.§F particle TV` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :262 `A.§F credible intervals; D.§F F1 fixed interval` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :263 `A.§F “hence any interval/exact interval”; D.M2(c) coverage wording` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / GAP; :264 `B.§F KL/credible-interval discussion; D.§F F3` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :265 `B.§F WS6(c) KL upper bounds; D.F2 divergence bounds` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :184 `D15-TV · round minorisation (E:T10)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :185 `D15-TV · law TV` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :186 `D15-TV · realised cell TV` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :187 `D15-TV · IC3` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :188 `D15-KL · mixture KL` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :189 `D15-KL · forward empirical` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :190 `D15-KL · reverse obstruction` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :191 `D15-CI · set content` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :192 `D15-CI · size intervals` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :186 `A.S10 · KL/TV/BLOCKS` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :195 `B.S5 · KERNEL; S9 · IDENT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :208 `D.S8 · terminal-law TV` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC2` — :160 `C15-TV · repairs` — as W1 (TRUE) / as W1 / as W1 / REPAIRED; :161 `C15-CI · new form` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :162 `C9, C13, C14, C15-KL` — as W1 / as W1 / as W1 / REPAIRED
- No CHK_INHERITED section targets S-IDENT.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 9, TRUE 9, AMBIGUOUS 3, NEEDS-HYPOTHESIS 2, as W1 (TRUE) 1, as W1 1.

*Adverse rows:* W1_PC1:257 (A.S4(a); B.D19, Λ≤sqrt(J): AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:260 (A.§F reverse KL: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:263 (A.§F “hence any interval/exact interval”; D.M2(c) coverage wording: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, GAP); W1_PC1:264 (B.§F KL/credible-interval discussion; D.§F F3: AMBIGUOUS, DESIGN-VERIFIED, GAP); W2_PC1:208 (D.S8 · terminal-law TV: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: terminal-law TV uses shipped L = max{4,⌈log₂(n+1)⌉} (METHOD:310 row 13) — useful iff M₁ = O(1) (D:112, W2PC1:208 AMBIGUOUS 'iff' → item-7 wording).
- Ẑ-weighted pooling / partition: n/a. Default-4 bound is vacuous (W2PC2:74); reverse empirical KL(π‖π̂) = ∞ when a positive-mass state is unrecorded (C:236).

**Notes (with sources):**

- Λ naming: Λ_len := ∫sd_{q_φ}(d)dφ (length), not the cumulant Λ(1) (W1PC1:257 AMBIGUOUS → repaired in all seats).

### S-BLOCKS — Supplement S-BLOCKS — separation ⇒ groups kept; SIZE ⇒ equality

**Round 3 resolution (MINUTES §2.2):** K07, K14, K06 (separation ⇒ groups kept; SIZE ⇒ equality).

**HQ:** wave 1 · HQ `LP-FOUND` · charter `HQ_CHARTERS/LP-FOUND.md`

**Seat cards (R2):** A:145 (S10 BLOCKS part); B:201–203 (S11 BLOCKS); C:183–191 (C11); D:106 (S2).

**K-IDs in this item:** K07 (strict gap + size ≤ B preserves groups; equality needs g_max ≤ B < 2g_min), K14 (every block sub-model scored; masking ≤ B in a block costs nothing), K06 (⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉ blocks, table cost).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K07** `R0_DIFF:81` · class NEW-DE · If every within-group distance is strictly below every between-group distance and groups have size ≤ B, complete linkage forms each group first and cutting/packing never splits a group, so cross-block |r| ≤ the largest between-gro…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 768; REG 660]; PART-pairing: OPEN (SF: none; XF: none) [IDX 773; REG 670]; PART-CE2 (COUNTEREXAMPLE): “Blocks ≠ groups surely when two groups fit in one block.” [IDX 1015; REG 668]
  - `PART-pairing` — FLAG AUTHOR-ONLY (IDX:773)
  - `PART-ThmA` — XF-VERIFIED*(qualified) (IDX:768)
  - `PART-CE2` — XF-ADVERSE:ERROR (no clean SF) (IDX:772)
- **K14** `R0_DIFF:88` · class NEW-DE · Every sub-model inside a block is scored at table time, so the HPM beats every block-local model and masking of any order ≤ B inside one block costs nothing; the HPM equals S₀ after tables when S₀ sits in one block and the landsca…
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K06** `R0_DIFF:80` · class NEW-DE · Next-fit packing of the complete-linkage cut gives ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉ blocks and total table cost Σ_b 2^|C_b| ≤ p·2^B/B.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Further registry IDs cited in the seat cards' status lines for this item** (not named in the K-ID cells above):

- `OWS-WS1` — FLAG AUTHOR-ONLY (IDX:402)

**Seat card status (verbatim):**

- A:145 — Status: D/E proposals TRUE-AS-WRITTEN at the cited rows; OWS-WS1 PROVED (no review).
- B:203 — Status: PART-ThmA: PROVED (SF: none; XF: VERIFIED* (A-REV9)); PART-pairing: OPEN; PART-CE2: COUNTEREXAMPLE.
- C:187 — PART-ThmA: **PROVED; SF none; XF VERIFIED***. Counting/graph assembly: **PROOF SKETCH, unchecked**. PART-pairing remains **OPEN**, excluded.
- D:106 — unchanged

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :169 `A.C18 clustering lemma` — NEEDS-HYPOTHESIS / DESIGN-FAILS / PLAUSIBLE; :293 `B.D21; D.S2 block/table clauses` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- `W1_PC2` — :204 `D10 · separation (E:T05)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :205 `D10 · counting` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :206 `D10 · graph (E:T08)` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :186 `A.S10 · KL/TV/BLOCKS` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :195 `B.S5 · KERNEL; S9 · IDENT` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :158 `C11 · equality` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- No CHK_INHERITED section targets S-BLOCKS.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 4, TRUE 3, NEEDS-HYPOTHESIS 1.

*Adverse rows:* W1_PC1:169 (A.C18 clustering lemma: NEEDS-HYPOTHESIS, DESIGN-FAILS, PLAUSIBLE).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: n/a
- Ẑ-weighted pooling / partition: partition as coded: complete linkage on 1−|r|, size-only cut at B, next-fit packing (METHOD:319 row 22, :196 w5; W2PC2:158 'the coded top-down cut never splits a ≤ B subtree'; blocks = groups for n ≥ 9⁶).

**Notes (with sources):**

- PART-pairing OPEN (excluded); PART-CE2 COUNTEREXAMPLE for unequal sizes — the equal-size packing example survives (W1PC1 ledger S20, VERDICTS.md:98; W2PC2:84). W1PC1:169 NEEDS-HYPOTHESIS/DESIGN-FAILS for the equality lemma without SIZE.

### S-OUT — Supplement S-OUT — output-event validity, worker equivalence, stacking

**Round 3 resolution (MINUTES §2.2; R3-4):** K77, K78, K83–K86, K63. K63 and K86 are also named as premises in M1/M5 (proved here). The integrated streams, GUARD-W and IND-T extension audits are code-audit obligations carried by this pack (§8).

**HQ:** wave 3 · HQ `LP-AUDIT` · charter `HQ_CHARTERS/LP-AUDIT.md` (S-CERT + S-OUT). Wave note: M1 (wave 1) and M2-side clauses consume S-OUT, which launches in wave 3 (§5 wave check).

**Seat cards (R2):** A:137 (S6 PAR); C:204–212 (C13); D:108 (S4 worker/stacking/output).

**K-IDs in this item:** K77 (Lemma RO: stopped fit = no output; guard stop-only), K78 (joint-with-output certificate statements), K83 (concurrent = serial bitwise), K84 (stacking R′=4k keeps islands 1–4; nested search), K85 (R declared before randomness), K86 (stream separation), K63 (HPM strict order / union-then-truncate).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K77** `R0_DIFF:181` · class CONFIRMED-E · A stopped fit is no output (Lemma RO: outputs on {no resource_limit} equal the potential uninterrupted run; GUARD reads only the clock), while path-dependent stopping or conditioning on completion biases Ẑ.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). LemmaRO: PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV6)) [IDX 127; REG 258]; CEX-guard: COUNTEREXAMPLE (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) [IDX 128; REG 259]; BOOK-B1-GUARD: — (SF: none; XF: ERROR (A-REV4)) [IDX 130; REG 780]; N2(e): GUARD-W not audited [INP 138]
  - `BOOK-B1-GUARD` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:130)
  - `CEX-guard` — XF-VERIFIED*(qualified) (IDX:128)
  - `LemmaRO` — XF-VERIFIED*(qualified) (IDX:127)
- **K78** `R0_DIFF:182` · class CONFIRMED-E · Every certificate and coverage statement is joint with output: P(𝒪 ∩ {L > Z}) ≤ α·P(complete) ≤ α, never conditional on delivery (which can reach α/P(delivery)).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). N6: (a) PROVED (potential run; output form CORRECT WITH AMENDMENT); (b) PROVED modulo premise (i) [INP 170]; PC1c2: PROVED for the potential run; output-event version CORRECT WITH AMENDMENT (PC1 claim 2) [IDX 187]
  - `PC1c2` — XF (IDX:187)
- **K83** `R0_DIFF:192` · class CONFIRMED-DE · Concurrent islands, diagnostic islands and scans reproduce the serial run bit for bit (per-island streams, ordered reductions, canonical provenance), so the study’s fits are v3.1 fits.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropW: PROVED (code reading; executed check in REPORT §6) [IDX 92]; MA-Wcal: PROVED (code reading only; not executed) [IDX 93]; Lemma-STREAM: PROVED (SF: none (authored by W5-LOCKBOOK); XF: none) [IDX 86; REG 365]
  - `Lemma-STREAM` — FLAG AUTHOR-ONLY (IDX:86)
  - `MA-PropW` — FLAG AUTHOR-ONLY (IDX:92)
  - `MA-Wcal` — FLAG AUTHOR-ONLY (IDX:93)
- **K84** `R0_DIFF:193` · class CONFIRMED-DE · Stacking R′ = 4k islands on fresh streams leaves islands 1–4 unchanged and, when the extra local search from the R = 4 centre is kept, the post-search scored set and HPM score nest.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-CorWR: PROVED (by Proposition W(a, b) and the definition of the HPM) with a caveat (PROOFS.md); INPUTS: 'Cor W-R as written PROVED (PC1 claim 6)' [IDX 94]; PC1c6: Cor W-R with caveat PROVED; 'post-search HPM monotone in R′ without the extra local search' FALSE (COUNTEREXAMPLE) [IDX 652]
  - `MA-CorWR` — FLAG SAME-FAMILY-ONLY (IDX:94)
  - `PC1c6` — FLAG SAME-FAMILY-ONLY (IDX:652)
- **K85** `R0_DIFF:194` · class CONFIRMED-DE · Pooled Ẑ is unbiased and every bound holds for any R declared before final randomness; an adaptive R (add islands until the SE is small) or selecting islands breaks it.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-PropP: PROVED (elementary) [IDX 70]; CEX-guard: COUNTEREXAMPLE (SF: VERIFIED (W5-LOCKBOOK); XF: VERIFIED* (A-REV4)) [IDX 128; REG 259]; N14(b): per run for any R′ declared before final randomness [INP 229]
  - `CEX-guard` — XF-VERIFIED*(qualified) (IDX:128)
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **K86** `R0_DIFF:195` · class CONFIRMED-DE · Final streams 10..9+R are independent of the calibration streams 0–9 and of each other, so every identity holds conditionally on calibration (stream separation).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). IND-T: PROVED (SF: none (authored by W2-PREM); XF: VERIFIED* (A-REV1)) [IDX 85; REG 190]; Lemma-STREAM: PROVED (SF: none (authored by W5-LOCKBOOK); XF: none) [IDX 86; REG 365]
  - `Lemma-STREAM` — FLAG AUTHOR-ONLY (IDX:86)
  - `IND-T` — XF-VERIFIED*(qualified) (IDX:85)
- **K63** `R0_DIFF:162` · class CONFIRMED-DE · The HPM is the maximum of F under the strict total order (F, −|S|, lex) over the scored set, independent of scoring order, and top-c stores merge by union-then-truncate: top_c(M) = top_c(∪_r top_c(M_r)).
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-LemmaS: PROVED (candidate; 'Every item is a candidate: not reviewed, not adopted') [IDX 91]; V2 draft status: Lemma S PROVED [LST 22]
  - `MA-LemmaS` — FLAG AUTHOR-ONLY (IDX:91)

**Seat card status (verbatim):**

- A:137 — **S6 · Proposition PAR (K63, K83, K84, K86, K09).** Unchanged from R1 §D S1 (Lemma S candidate; MA-PropW: PROVED (code reading; executed check); MA-Wcal: PROVED (code reading only; not executed); IND-T extension audit pending; tie-DP invariant N3 OPEN; PC2:198 TRUE-AS-WRITTEN on random instances, DESIGN-ASSERTED). Supplement.
- C:208 — LemmaRO: **PROVED; SF VERIFIED; XF VERIFIED***. CEX-guard: **COUNTEREXAMPLE; XF VERIFIED***. N6 potential-run: **PROVED**; output form: **CORRECT WITH AMENDMENT**. GUARD-W: **not audited**.
- D:108 — unchanged

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :126 `A.C3(a,b,c); B.D3(e); D.M3(c)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :127 `A.C3(d); D.S4 adaptive-budget wording` — AMBIGUOUS / DESIGN-VERIFIED / PLAUSIBLE; :294 `A.S1(a,b,c); D.S4 worker/stacking clauses` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE
- `W1_PC2` — :116 `D12 · joint failure bound` — TRUE / DESIGN-VERIFIED / PLAUSIBLE; :117 `D12 · no conditional claim` — TRUE / n/a / PLAUSIBLE
- `W2_PC1` — :206 `D.S1,S2,S4 · target/graph/output` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED
- `W2_PC2` — :162 `C9, C13, C14, C15-KL` — as W1 / as W1 / as W1 / REPAIRED
- No CHK_INHERITED section targets S-OUT.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 3, TRUE 2, AMBIGUOUS 1, as W1 1.

*Adverse rows:* W1_PC1:127 (A.C3(d); D.S4 adaptive-budget wording: AMBIGUOUS, DESIGN-VERIFIED, PLAUSIBLE); W1_PC1:294 (A.S1(a,b,c); D.S4 worker/stacking clauses: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: LS0 stop = GUARD-W stop (METHOD:136 #6, :152).
- Coded grid: n/a
- Ẑ-weighted pooling / partition: GUARD-W (worker, merge and LS0 paths ⇒ no output on any stop) is a **code-audit obligation, unaudited** (METHOD:136, :400; C:51; W2PC2 §0 GAP). Lemma RO + GUARD-W transfer intersection inequalities, not expectations (D:56).

**Notes (with sources):**

- CEX-guard (registry COUNTEREXAMPLE) kills the completion-conditioned reading; BOOK-B1-GUARD XF ERROR (do not broaden bitwise equality to timing metadata, W1PC1 ledger S21, VERDICTS.md:99). MA-PropW code-reading + executed check (METHOD:46: executed bitwise on smoke + 3/3 study designs; REGISTRY_INDEX §5.B B1 records '1/1 vs 3/3' as a source CONFLICT); MA-Wcal code reading only, not executed.

### S-STGI — DISSOLVED (corrected MINUTES §2.2: K30 → M7(d); K29 → FUTURE_WORK FW23; dissent D). Record kept below for reference

**Round 3 resolution (MINUTES §2.2; R3-8):** ideal two-state crossing depth (K30 restated); **K29 only as a cited conditional implication** under (LL) or the over-tilted q_w bound; its unconditional favourable application is FUTURE_WORK. MINUTES: B (FW) and C (conditional cited) prevail over A and D (supplement conditional), whose substance is the same conditional implication. Seat positions on file differ (§7).

**HQ:** wave 2 · HQ `LP-IDENT` · charter `HQ_CHARTERS/LP-IDENT.md`

**Seat cards (R2):** A:147 (S11 STG-ideal); B:139 (M7 (f)); C:214–222 (C14); D:114 (S10 calibration).

**K-IDs in this item:** K29 (favourable O(1) stage count conditional on (LL) or over-tilted q_w bound), K30 (ideal two-state crossing log₂A₀ + O(1)).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K29** `R0_DIFF:113` · class DRAFT-ONLY · In the favourable regime the stage count is O(1) on BO designs with p ≤ n^A (two-sided through q_w(S₀), w ∈ [1,2]).
  - *R0_DIFF status cell (verbatim):* STG-F: PROVED (SF: none; XF: none) [IDX 259; REG 698]; STG-Wp: PROVED-UNDER (SF: none; XF: none) [IDX 260; REG 699]; STG-cexW2 (COUNTEREXAMPLE): “F-DRAFT's O(1) stage count is false.” [IDX 1019; REG 703]
  - `STG-cexW2` — FLAG AUTHOR-ONLY (IDX:264)
  - `STG-Wp` — FLAG AUTHOR-ONLY (IDX:260) — ⚑ registry CONFLICT C22 (IDX:1196)
  - `STG-F` — FLAG AUTHOR-ONLY (IDX:259)
- **K30** `R0_DIFF:114` · class CONFIRMED-DE · A pair-dominance crossing of gap D costs log₂(D) + O(1) ESS-0.9 stages, separated crossings add, and no V, N or seed removes this lower bound.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 261; REG 700]; D2: STG-M PROVED (ideal two-state grid), XF VERIFIED*; families PROOF SKETCH [LST 30]; STG-cexW2 (COUNTEREXAMPLE): “F-DRAFT's O(1) stage count is false.” [IDX 1019; REG 703]
  - `STG-cexW2` — FLAG AUTHOR-ONLY (IDX:264)
  - `STG-M` — XF-VERIFIED*(qualified) (IDX:261)

**Seat card status (verbatim):**

- A:147 — **S11 · STG-ideal (K29, K30).** K30: ideal two-state exact-frontier grid, log₂A₀ + O(1) (STG-M: PROVED (SF: none; XF: VERIFIED* (A-REV9)); crossings add only when separated and pair-dominant, PC1:197). K29: favourable T* = O(1) under STG-F **with (LL)** or the over-tilted q_w bound as hypothesis (PC1:196; STG-F: PROVED (SF: none; XF: none); STG-Wp: PROVED-UNDER, conflict C22). Supplement, labelled ideal grid.
- C:218 — STG-M: **PROVED; SF none; XF VERIFIED*** for logarithmic order; explicit decimal constants **GAP**.

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W1_PC1` — :196 `A.C11(d); B.D7(e); D.M9(c); thesis favourable clauses` — NEEDS-HYPOTHESIS / DESIGN-ASSERTED / GAP; :197 `A.C11(e,f,g); B.D7(c,d); D.M9(d,e), K31` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / PLAUSIBLE
- `W1_PC2` — :164 `D13 · ideal crossing` — TRUE / DESIGN-VERIFIED / PLAUSIBLE
- `W2_PC1` — :187 `A.S11 · STG-ideal` — TRUE-AS-WRITTEN / DESIGN-ASSERTED / GAP / REPAIRED
- `W2_PC2` — :162 `C9, C13, C14, C15-KL` — as W1 / as W1 / as W1 / REPAIRED
- No CHK_INHERITED section targets S-STGI.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 2, NEEDS-HYPOTHESIS 1, TRUE 1, as W1 1.

*Adverse rows:* W1_PC1:196 (A.C11(d); B.D7(e); D.M9(c); thesis favourable clauses: NEEDS-HYPOTHESIS, DESIGN-ASSERTED, GAP); W1_PC1:197 (A.C11(e,f,g); B.D7(c,d); D.M9(d,e), K31: TRUE-AS-WRITTEN, DESIGN-ASSERTED, PLAUSIBLE); W2_PC1:187 (A.S11 · STG-ideal: TRUE-AS-WRITTEN, DESIGN-ASSERTED, GAP, REPAIRED).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: **ideal** grid only (labelled); not the coded grid (A:147, C:222).
- Ẑ-weighted pooling / partition: n/a

**Notes (with sources):**

- STG-cexW2 (COUNTEREXAMPLE) and STG-Wp conflict C22 apply to K29; K29 has no verified (LL) family: A.S11 DESIGN-ASSERTED / GAP (W2PC1:187). Explicit decimal constants of STG-M are GAP (C:218).

### S-REP — Supplement S-REP — reporting corollaries for Ĵ and ε̂_× (HQ Q4)

**Round 3 resolution (MINUTES §2.2; R3-6 unanimous):** Ĵ in the B/C/D form (A withdrew its TI form); ε̂_× with companions κ̂, δ̂, ū̂. **ū̂ is D's global block-table envelope ū̂ = Σ_b max_{U⊆C_b} x_b(U), not a maximum over V** (C's objection, R3_C §S1, adopted). K34 is dropped as a theorem (Ĵ ships as reporting). Final card: `R3_C.md` §S2 S-REP. Definitions for HQ: `AMENDMENT_HQ_02_DEFINITIONS.md`.

**HQ:** wave 4 · HQ `LP-REP` · charter `HQ_CHARTERS/LP-REP.md` (S-REP + S-LEAK; MINUTES §2.5). Named premise: the read-only d accumulator, with d as a default member of the declared list 𝓗 (§8).

**Seat cards (R2):** A:194–200 (§R5); B:238–246 (§R5); C:290–310 (§R5 and C16); D:174–182 (§R5).

**K-IDs in this item:** K104 (J identity, ∫Var dφ), K11 (leakage proxy bound (δ_A, δ_H ≤ …)), K34 (Ĵ half ships as reporting; TI evidence dropped).

**Registry statuses per K-ID** (verbatim cell, then index flags for every registry ID the cell names):

- **K104** `R0_DIFF:233` · class NEW-DE · π_φ is an exponential family in d: (log Z_φ)′ = E d, (log Z_φ)″ = Var d, log(Z/(m(∅)Z̄₀)) = ∫E_{π_φ}d, KL(π‖π₀) + KL(π₀‖π) = J = ∫Var_{π_φ}(d)dφ, J = 0 iff π₀ = π, and Λ ≤ √J.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K11** `R0_DIFF:85` · class NEW-DE · For cross-block correlation at most ε (or small relative operator norm), |d_X(S)| is bounded explicitly, linearly in ε through k·log(1+2kε/κ) and an n·R² fit term.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell
- **K34** `R0_DIFF:118` · class NEW-D · The trapezoid thermodynamic-integration evidence and Ĵ = d̄_final − d̄_0 are consistent by-products, and disagreement between SMC and TI evidence is a run diagnostic.
  - *R0_DIFF status cell (verbatim):* D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row.
  - no registry/index ID is named in the cell

**Seat card status (verbatim):**

- B:245 — "ε̂_× ∈ [0,1]: maximum absolute cross-block sample correlation after blocking"; "η̂_V (nats): discrepancy from the block-orthogonal bridge on V".
- C:305 — HQ Q4 reporting-only scope; new corollary **PROOF SKETCH, unchecked**. No automatic diagnostic calibration or machine-certified inequality.

**Meeting's own check history — statement-sanity verdicts (NOT proof statuses):**

- `W2_PC1` — :155 `A.R5(i) · Ĵ definition / T-J1` — AMBIGUOUS / DESIGN-VERIFIED / GAP; :156 `A.R5(i) · T-J2,T-J3` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :157 `A.R5(ii) · leakage` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED; :163 `B.R5(i) · Ĵ` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :164 `B.R5(i) · T5 interpretation` — AMBIGUOUS / DESIGN-ASSERTED / GAP; :165 `B.R5(ii) · leakage T1–T6` — NEEDS-HYPOTHESIS / DESIGN-VERIFIED / PLAUSIBLE; :171 `D.R5(i) · Ĵ,T1–T3` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :172 `D.R5(i) · V rescaling` — COUNTEREXAMPLE / DESIGN-VERIFIED / PLAUSIBLE; :173 `D.R5(ii) · ε̂,η̂,T4,T5` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :174 `D.R5(ii) · T6` — COUNTEREXAMPLE / DESIGN-VERIFIED / GAP
- `W2_PC2` — :146 `§R5 · Ĵ definition` — COMPLIANT; :147 `C16 · Ĵ theorem` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :148 `§R5 · proxy definition` — COMPLIANT; :149 `C16 · proxy theorem` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE
- No CHK_INHERITED section targets S-REP.

*Tally of the rows above, 'true as written' column:* TRUE-AS-WRITTEN 7, AMBIGUOUS 2, COUNTEREXAMPLE 2, COMPLIANT 2, NEEDS-HYPOTHESIS 1.

*Adverse rows:* W2_PC1:155 (A.R5(i) · Ĵ definition / T-J1: AMBIGUOUS, DESIGN-VERIFIED, GAP); W2_PC1:164 (B.R5(i) · T5 interpretation: AMBIGUOUS, DESIGN-ASSERTED, GAP); W2_PC1:165 (B.R5(ii) · leakage T1–T6: NEEDS-HYPOTHESIS, DESIGN-VERIFIED, PLAUSIBLE); W2_PC1:172 (D.R5(i) · V rescaling: COUNTEREXAMPLE, DESIGN-VERIFIED, PLAUSIBLE); W2_PC1:174 (D.R5(ii) · T6: COUNTEREXAMPLE, DESIGN-VERIFIED, GAP).

**Lean:** No Lean file.

**Fidelity to v3.1 as shipped:**
- LS0: n/a
- Coded grid: reads per-particle d at init and after each measured round (`v3_engine.h:286–360`); **values are not retained today** — a read-only accumulator is needed (W2PC2:72, :146)
- Ẑ-weighted pooling / partition: yes: Ĵ weights final islands by Ẑ_r (S2:207–209).

**Notes (with sources):**

- Ĵ/ε̂_× are POST HOC reporting quantities (METHOD:158–160 reporting block); no RNG, no feedback. Ĵ is a 'post hoc Monte Carlo estimate' (C:296). C16's Ĵ tail bound is vacuous at R′ = 4 and at R′ = 50 (W2PC2:74); D's V-rescaling clause and T6 and A's TI form are removed/withdrawn (S2:211, 224–228).

### S-LEAK — Supplement S-LEAK — B's leakage clauses (F), (S), supplementary corollary to M2 (R3-5)

**Round 3 resolution (MINUTES §2.2; R3-5 unanimous):** the leakage clauses (F) and (S) of seat B are a supplementary corollary to M2, not part of HQ's (a)(b)(c) package; they are non-perturbative and at a different scale. The m-form of (S) and (F) go together; (b5)'s pathwise bound stays in M2 (R3_B:142, :173).

**Source cards:** B:216 (R2 clauses (b5) OWS-WS6(b) with the m lower bound, and (b6) OWS-WS53F); R3 statement in `R3_B.md` §S2 M2 (the leakage corollary is split from the main card).

**K-IDs in this item:** none of its own; clauses of the M2 item (K102 context).

**Registry IDs:** `OWS-WS53F` — PROVED-UNDER (SF: none; XF: none), FLAG AUTHOR-ONLY (IDX:407; B:216). `OWS-WS6(b)` — PROVED (SF: none; XF: none) as quoted at B:216; no index flag was read by the registrar for this ID.

**Check history (rows listed under M2, statement-sanity verdicts, not proof statuses):** W1_PC1:143 `B.D6(F)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; :144 `B.D6(S)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE; W2_PC1:70 `B.R3(b)(5),(6)` — TRUE-AS-WRITTEN / DESIGN-VERIFIED / PLAUSIBLE / REPAIRED DIFFERENTLY (these are the rows of M2's list that judge B's R2 clauses (b5),(b6); the mapping to (S),(F) is by B:216).

**Lean:** none. **Fidelity to v3.1 as shipped:** as M2 (LS0: n/a).

**Edges:** M2 → S-LEAK (D3:197); M3 → S-LEAK (B3:230); S-T → S-LEAK (B3:232). A3:170 writes 'S-LEAK → M2 (supplement corollary)', the opposite literal direction with the same substance (§5).

**HQ:** wave 4 · HQ `LP-REP` · charter `HQ_CHARTERS/LP-REP.md` (S-REP + S-LEAK; MINUTES §2.5).

## 3. Cited lemmas used by the list items

Each lemma is cited, not a numbered list claim (SYNTH_R2 R3-8, last sentence: 'Cited foundations … are not numbered supplement claims'). Statuses are those of the K-ID cells in §1/§2 plus the index flags below.

### L-N9 — N9 kernel facts (reversibility, random-order invariance, exact draw_pi0 and Z̄₀)

- **Used by:** M1 (A:44(a), B:85, D:56 cited); S-KERNEL
- **K-IDs:** K20 (R0_DIFF:99, class CONFIRMED-DE), K21 (R0_DIFF:100, class CONFIRMED-DE), K08 (R0_DIFF:82, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
  - `T09` — XF (IDX:71)
  - `N9K` — FLAG AUTHOR-ONLY (IDX:72)
- **Check rows (statement-sanity, not proof status):** `CHK_INHERITED/REPORT.md:15` VERIFIED WITH AMENDMENT (section CHK:130–176).
- **Lean:** none
- **Note:** Registry still `PROVED (candidate)` (flag AUTHOR-ONLY, REGISTRY_INDEX.md:72); T09 is `PROVED-LOCKED (wave 1)`. 'Registry row to be opened' (A:46).

### L-T12 — Island identities and Markov bound: T12, T31(i), Prop2(a,b,d,e), IND-T, FMP-M1

- **Used by:** M1; M4 (K36); S-POOL
- **K-IDs:** K35 (R0_DIFF:124, class CONFIRMED-DE), K36 (R0_DIFF:125, class CONFIRMED-DE), K46 (R0_DIFF:140, class CONFIRMED-DE), K86 (R0_DIFF:195, class CONFIRMED-DE)
- **Registry / non-registry IDs and index flags:**
  - `Prop2(a,b,d,e)` — XF-ADVERSE:GAP (SF verified) (IDX:60)
  - `T31(i)` — XF (IDX:69)
  - `T12` — XF (IDX:68)
  - `T26-Lemmas2-3` — XF-VERIFIED (IDX:149)
  - `PC1c3` — XF (IDX:114)
  - `Lemma-STREAM` — FLAG AUTHOR-ONLY (IDX:86)
  - `IND-T` — XF-VERIFIED*(qualified) (IDX:85)
  - `FMP-M1` — XF-VERIFIED (IDX:107)
  - `Prop2(c)` — XF-VERIFIED (IDX:61)
- **Check rows (statement-sanity, not proof status):** W1_PC1:110, :111 TRUE-AS-WRITTEN; W1_PC2:101–102 TRUE (statement sanity).
- **Lean:** `T12Core.lean` PARTIAL (`hstep` hypothesis).
- **Note:** Prop2(a,b,d,e) is `PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4))`; THEOREM_LIST writes 'PROVED-LOCKED' — registry CONFLICT B10 (REGISTRY_INDEX.md §5.B).

### L-RO — Lemma RO + CEX-guard (run/output split)

- **Used by:** M1, M4, S-OUT
- **K-IDs:** K77 (R0_DIFF:181, class CONFIRMED-E), K78 (R0_DIFF:182, class CONFIRMED-E), K85 (R0_DIFF:194, class CONFIRMED-DE)
- **Registry / non-registry IDs and index flags:**
  - `BOOK-B1-GUARD` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:130)
  - `CEX-guard` — XF-VERIFIED*(qualified) (IDX:128)
  - `LemmaRO` — XF-VERIFIED*(qualified) (IDX:127)
  - `PC1c2` — XF (IDX:187)
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
  - `Lemma-STREAM` — FLAG AUTHOR-ONLY (IDX:86)
- **Check rows (statement-sanity, not proof status):** W1_PC1:126–127; W1_PC2:116–117; W2_PC2:162 (C13).
- **Lean:** none
- **Note:** Requires GUARD-W (unaudited code premise).

### L-WS3 — OWS-WS3 / OWS-WS4 (block orthogonality; standardised cross-block perturbation) — as used in M2(a),(b)

- **Used by:** M2, M3 (clause (e)), S-REP (proxy)
- **K-IDs:** K10 (R0_DIFF:84, class NEW-DE), K11 (R0_DIFF:85, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
  - `DIL-E` — XF-VERIFIED (IDX:328)
  - `OWS-WS3` — FLAG AUTHOR-ONLY (IDX:404)
  - `OWS-WS4` — FLAG AUTHOR-ONLY (IDX:405)
  - `FD-W1` — XF-VERIFIED (IDX:416)
  - `AREV9-OWSTAB` — XF (IDX:423)
- **Check rows (statement-sanity, not proof status):** `CHK_INHERITED/REPORT.md:13` WS3 VERIFIED; `:14` WS4 VERIFIED.
- **Lean:** none
- **Note:** Registry: `PROVED (SF: none; XF: none)`, flag AUTHOR-ONLY; CHK verdicts are separate review entries (A:68).

### L-WS6 — OWS-WS6(d) / OWS-WS7 (noise-chasing obstruction; masked-regime weights)

- **Used by:** M2(c), M6 (K105 = WS7(a))
- **K-IDs:** K102 (R0_DIFF:226, class CONFIRMED-DE), K17 (R0_DIFF:91, class CONFIRMED-DE), K105 (R0_DIFF:234, class DRAFT-ONLY)
- **Registry / non-registry IDs and index flags:**
  - `AREV9-OWSTAB` — XF (IDX:423)
  - `OWS-WS6e` — FLAG AUTHOR-ONLY (IDX:412)
  - `OWS-WS8d` — FLAG AUTHOR-ONLY (IDX:415)
  - `FD-W(a)` — FLAG AUTHOR-ONLY (IDX:417)
  - `Thm3-EXP` — XF-VERIFIED (IDX:321)
  - `Thm4-EXP` — XF-VERIFIED (IDX:322)
  - `T27(i)` — XF (IDX:339)
  - `KL` — FLAG AUTHOR-ONLY (IDX:369)
  - `OWS-WS6d` — FLAG AUTHOR-ONLY (IDX:411)
  - `OWS-WS7` — FLAG AUTHOR-ONLY (IDX:413)
- **Check rows (statement-sanity, not proof status):** `CHK_INHERITED/REPORT.md:11` WS6(d) VERIFIED WITH AMENDMENT; `:12` WS7 VERIFIED WITH AMENDMENT.
- **Lean:** none
- **Note:** WS6(e) CONJECTURE and WS8(d) OPEN are not used.

### L-G — Theorem G / STG-G (greedy ESS grid optimality) and T26BUD-G

- **Used by:** M7; M2(b) sandwich
- **K-IDs:** K26 (R0_DIFF:110, class CONFIRMED-DE)
- **Registry / non-registry IDs and index flags:**
  - `T26BUD-G` — FLAG AUTHOR-ONLY (IDX:268)
  - `STG-L0` — FLAG AUTHOR-ONLY (IDX:255)
  - `STG-L1` — FLAG AUTHOR-ONLY (IDX:256)
  - `STG-G` — FLAG AUTHOR-ONLY (IDX:257)
- **Check rows (statement-sanity, not proof status):** W1_PC1:190–191.
- **Lean:** none
- **Note:** Optimality only among refinements of the retained pilot targets (2^{−60} slack); T26BUD-G flag AUTHOR-ONLY.

### L-T03 — T03♯ / T02(i♯),(ii♯) / T01 reduction (exact-posterior target theory)

- **Used by:** S-T; M1(g); M4, M5 (π(S₀) → 1 on LH); S-SL (FW)
- **K-IDs:** K93 (R0_DIFF:207, class CONFIRMED-DE), K04 (R0_DIFF:73, class NEW-E), K03 (R0_DIFF:72, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
  - `T03-1.2e5` — FLAGGED-SUBCLAIM (SF ERROR; XF ERROR) (IDX:465)
  - `T01-T03` — FLAG SAME-FAMILY-ONLY (IDX:469)
  - `T03♯` — XF-VERIFIED (IDX:151)
- **Check rows (statement-sanity, not proof status):** W1_PC1:220; W1_PC2:170.
- **Lean:** none
- **Note:** `T01-T03` SAME-FAMILY-ONLY, external review queued.

### L-MASK — Masking law on LH: Thm3/4-EXP, Thm5-LH, T22, T27(i)

- **Used by:** M3, M4, M5, M6
- **K-IDs:** K15 (R0_DIFF:89, class DRAFT-ONLY), K17 (R0_DIFF:91, class CONFIRMED-DE), K18 (R0_DIFF:92, class DRAFT-ONLY)
- **Registry / non-registry IDs and index flags:**
  - `T22(i)(ii)(iv)` — XF (IDX:337)
  - `Thm3-EXP` — XF-VERIFIED (IDX:321)
  - `Thm4-EXP` — XF-VERIFIED (IDX:322)
  - `T27(i)` — XF (IDX:339)
  - `DIL-E1` — XF-VERIFIED*(qualified) (IDX:329)
  - `DIL-DM` — XF-ADVERSE:ERROR (no clean SF) (IDX:333)
  - `DIL-E` — XF-VERIFIED (IDX:328)
  - `Thm5-LH` — FLAG SAME-FAMILY-ONLY (IDX:325)
  - `EXP′` — XF-VERIFIED*(qualified) (IDX:319)
- **Check rows (statement-sanity, not proof status):** W1_PC1:158; W1_PC2:136–137; W2_PC2:131.
- **Lean:** none
- **Note:** Thm5-LH SAME-FAMILY-ONLY. n ≥ 9⁶ for blocks = groups on the nine-variable exhibits.

### L-TA — Theorem A / LS-score / Lemma0(a,c) / T38-(0) / T38-b1-LH

- **Used by:** M5
- **K-IDs:** K65 (R0_DIFF:164, class DRAFT-ONLY), K68 (R0_DIFF:167, class CONFIRMED-DE), K69 (R0_DIFF:168, class DRAFT-ONLY), K72 (R0_DIFF:171, class CONFIRMED-E)
- **Registry / non-registry IDs and index flags:**
  - `Lemma0(b)` — XF-ADVERSE:ERROR (no clean SF) (IDX:502) — ⚑ registry CONFLICT C1 (IDX:1175)
  - `TheoremA` — XF-VERIFIED*(qualified) (IDX:500)
  - `LS-score` — XF-VERIFIED*(qualified) (IDX:508)
  - `Prop1-TD` — XF-VERIFIED (IDX:510)
  - `T38-(a)` — FLAG SAME-FAMILY-ONLY (IDX:548)
  - `T38-b1-LH-iidfail` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:553) — ⚑ registry CONFLICT C24 (IDX:1198)
  - `T38-b1-LH` — XF-VERIFIED*(qualified) (IDX:438) — ⚑ registry CONFLICT C24 (IDX:1198)
  - `Thm-b1` — XF-VERIFIED (IDX:549)
  - `Thm4-C1` — FLAG SAME-FAMILY-ONLY (IDX:527)
  - `T38-(0)` — XF-VERIFIED*(qualified) (IDX:528) — ⚑ registry CONFLICT C11 (IDX:1185)
  - `N200` — FLAG AUTHOR-ONLY (IDX:534)
  - `T21` — XF (IDX:533)
  - `Lemma0(a,c)` — XF-VERIFIED*(qualified) (IDX:501) — ⚑ registry CONFLICT C12 (IDX:1186)
- **Check rows (statement-sanity, not proof status):** W1_PC1:166–170, :176–177; W1_PC2:143–144.
- **Lean:** `T37Greedy.lean`, `T37Lattice.lean`, `T21HPM.lean` (0 sorry); LS-score no Lean file.
- **Note:** N200: `PROVED (elementary, every n); Π(X) upper bound OPEN` — AUTHOR-ONLY.

### L-DEC — Decision lemmas: HPM 0–1 rule, MPM Hamming rule, FDP (K60, K61), PC1c5 MPM threshold ½

- **Used by:** M1 (K62 margin), M4 (½ sharp), S-TARGET
- **K-IDs:** K60 (R0_DIFF:154, class CONFIRMED-DE), K61 (R0_DIFF:155, class NEW-D), K62 (R0_DIFF:156, class NEW-E)
- **Registry / non-registry IDs and index flags:**
  - `Prop1-wrongHPM` — FLAGGED-SUBCLAIM (SF none; XF ERROR) (IDX:483)
  - `Prop1-T07` — XF-VERIFIED*(qualified) (IDX:482)
  - `T07` — XF (IDX:487)
  - `PC1c5` — FLAG SAME-FAMILY-ONLY (IDX:202)
  - `N13` — no index row (id appears only inside the quoted cell)
- **Check rows (statement-sanity, not proof status):** W1_PC1:302 TRUE-AS-WRITTEN.
- **Lean:** `T07Bayes.lean` 28 theorems, 0 sorry (SmcBvs/SmcBvs); older copies 12 sorry.
- **Note:** K60 area: Prop1-wrongHPM is XF ERROR (a wrong report does not by itself prove a target-mode miss).

### L-N17 — Analytic upper envelope N17: Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}

- **Used by:** M4(e), S-TARGET, S-REP (envelope D̄_n in B:246)
- **K-IDs:** K44 (R0_DIFF:133, class NEW-DE), K01 (R0_DIFF:70, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
  - `PC2` — XF (IDX:731)
- **Check rows (statement-sanity, not proof status):** W1_PC2:212 TRUE.
- **Lean:** none
- **Note:** N17 `PROVED (PC1 claim 1; PC2 C1(c))`.

### L-SEP — SEP-A / SEP-B (iid miss; one-shot χ²)

- **Used by:** M6
- **K-IDs:** K19 (R0_DIFF:93, class CONFIRMED-DE), K106 (R0_DIFF:235, class DRAFT-ONLY)
- **Registry / non-registry IDs and index flags:**
  - `SEP-A-iid` — FLAG AUTHOR-ONLY (IDX:353)
  - `T38-(a)` — FLAG SAME-FAMILY-ONLY (IDX:548)
  - `SEP-A` — XF-VERIFIED (IDX:352)
  - `SEP-B` — XF-VERIFIED (IDX:354)
  - `SEP-E` — FLAG AUTHOR-ONLY (IDX:357) — ⚑ registry CONFLICT C19 (IDX:1193)
  - `SEP-taska` — FLAG AUTHOR-ONLY (IDX:356)
- **Check rows (statement-sanity, not proof status):** W1_PC1:183; W1_PC2:150–153.
- **Lean:** `T11Miss.lean` statement-match only (unmapped by source).
- **Note:** SEP-taska COUNTEREXAMPLE restricts the guarantee.

### L-ESS — Missing-mass identity ρ_full = ρ_V a_u a_w/a_v² (K25) and Popoviciu increment bound

- **Used by:** M2(b), M7, S-IDENT
- **K-IDs:** K25 (R0_DIFF:109, class NEW-DE), K27 (R0_DIFF:111, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
- **Check rows (statement-sanity, not proof status):** W1_PC2:159–161 TRUE; W1_PC1:192–193.
- **Lean:** none
- **Note:** Seat-derived (R0_DIFF: no registry row).

### L-DOEBLIN — Minorisation / Doeblin: Q_φ(S,·) ≥ π_φ/M_φ

- **Used by:** M2(b)(v); S-KERNEL; S-IDENT
- **K-IDs:** K103 (R0_DIFF:232, class NEW-DE)
- **Registry / non-registry IDs and index flags:**
- **Check rows (statement-sanity, not proof status):** W1_PC1:290; W1_PC2:184–185.
- **Lean:** none
- **Note:** Vacuous under masking (A:145).

### L-PROPP — Fixed-grid / fixed-R limit lemmas (Prop P(iii), Maurer-type SLLN; Del Moral, Whiteley–Lee–Heine) — KNOWN—CITE

- **Used by:** M1; S-POOL
- **K-IDs:** K47 (R0_DIFF:141, class CONFIRMED-DE), K48 (R0_DIFF:142, class CONFIRMED-DE)
- **Registry / non-registry IDs and index flags:**
  - `ADRAFT-CorA1` — ASTRA-ONLY (Astra-on-Astra; XF none) (IDX:63)
  - `ADRAFT-ThmA` — ASTRA-ONLY (Astra-on-Astra; XF none) (IDX:62)
  - `MA-PropP` — FLAG AUTHOR-ONLY (IDX:70)
- **Check rows (statement-sanity, not proof status):** W1_PC1:236 TRUE-AS-WRITTEN.
- **Lean:** none
- **Note:** MA-PropP AUTHOR-ONLY candidate; ADRAFT rows ASTRA-ONLY.

## 4. FUTURE_WORK, drop and remark table (MINUTES §2.3, §2.4; cross-reference to `FUTURE_WORK.md`)

| K-ID / item | Disposition | Reason | Source | Registry/index status of the K-ID (verbatim start of cell, ≤ 260 chars) |
|---|---|---|---|---|
| K13 | FUTURE_WORK | Needs TG4-type probability bounds not supplied (R0_DIFF K13) | S2:173 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K24 | FUTURE_WORK | Polynomial mixing of the φ=1 round (YWJ transfer); N10 OPEN | S2:174 | D/E side: proposal (author’s PROOF SKETCH, unchecked). N10: NONE / OPEN (INV row 6); YWJ/ZYVR route blocked as stated (INV §2 D1) [INP 199] |
| K23 | FUTURE_WORK (R3-4: A, B, D). **Dissent C:** keep the finite squared-kernel Dirichlet comparison as an attributed lemma in S-KERNEL, without a theorem number (R3_C §S1); recorded | Its only consumer K24 is deferred (R2 positions: FW for A and D, supplement for B, cited by C; decided in R3-4) | S2:175; R3-4 S2:276; MINUTES §2.3 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K31 | FUTURE_WORK | Conjecture P OPEN (as-coded masked stage count) | S2:176 | ConjP: Conjecture P — 'the as-coded grid's realised T_n in the masked regime is Conjecture P, OPEN' (THEOREM_LIST.md D2(iii)); registry has no row named Conjecture P (registry S… [IDX 269]; T26BUD-G: PROVED, deterministic (Theorem G); Conjecture P (pilot stage… |
| K58 | FUTURE_WORK | Reduces to population delivery; FMP-DELIVPOP OPEN | S2:177 | FMP-ThmR: PROVED (SF: none; XF: none) [IDX 215; REG 573]; FMP-DELIVPOP: OPEN (SF: none; XF: none) [IDX 217; REG 575]; ThmB-T24: PROVED (SF: VERIFIED* (W2-VT24G); XF: VERIFIED* (A-REV1)) [IDX 218; REG 210] |
| K59 | FUTURE_WORK | R vs N at fixed total particles: PROOF SKETCH only (A:240) | S2:178 | D/E side: proposal (author’s PROOF SKETCH, unchecked). MA-CorV: PROOF SKETCH [IDX 306]; OPW2-ThmB: PROVED (SF: none; XF: VERIFIED* (A-REV9)) [IDX 170; REG 601] |
| K71 | FUTURE_WORK | (b1-LH-iid) GAP | S2:179 | T38-b1-LH-iidfail: — (SF: none; XF: ERROR (A-REV5)) [IDX 553; REG 788]; R5 draft: (b1-LH-iid) XF GAP [LST 41] |
| K75 | FUTURE_WORK | NP-completeness needs a score-specific reduction not supplied | S2:180 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K92 | FUTURE_WORK | Moat construction and accuracy-matched comparator unproved; speed-up claims are empirical by decision (D:224) | S2:181 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K82 | FUTURE_WORK | Delivery P(U) → 0: no route; every output theorem is joint with 𝒪 in liminf form | S2:52, :182 | R6 draft status: NONE (THM-INV §5.4) [LST 42; IDX 587] |
| K94 | FUTURE_WORK | Finite-n Π(X) envelope GAP (W1PC1:222) | S2:183 | D/E side: proposal (author’s PROOF SKETCH, unchecked). R7 draft status: OPEN (API-N200) [LST 43; IDX 596]; N200: PROVED (elementary, every n); Π(X) upper bound OPEN [IDX 534]; N12: p ≤ e^{Cn^α}: no theorem; OPEN, not impossible [INP 218] |
| K99 (quantitative) | FUTURE_WORK | k-way barrier unproved (W1PC1:282 NEEDS-HYPOTHESIS; B's version IMPLAUSIBLE); qualitative barrier is a remark in S-LIM | S2:184 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row; related: SHARE-PB (COUNTEREXAMPLE): “A posterior barrier defeats (b2), LS0 and T39 alike: no method change helps.” [IDX 1001; REG 350]; INP I9(c),(d),(e) definitional limits [INP 274] |
| K107 | FUTURE_WORK | Validated arithmetic; N16 OPEN; T33-errbound COUNTEREXAMPLE | S2:185 | D/E side: proposal (author’s PROOF SKETCH, unchecked). N16: OPEN. VAL-FP MEASURED at p ≤ 40 only; η a documented heuristic [INP 243]; T33-errbound (COUNTEREXAMPLE): “The engine's error_bound() is not a bound at large n (ratio 1.17 at n = 10⁵, 6.2 at 4·10⁶); n … |
| K80 | FUTURE_WORK (R3-4: A, B, C, D) | Flags are heuristics by decision; no sampling law for the flags (W1PC1:283 NEEDS-HYPOTHESIS) | S2:186; MINUTES §2.3 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K97 (SL analytic separation) | FUTURE_WORK (R3-3: unanimous). LIT-PAR G4 is cited in the paper as labelled numerical evidence | W2PC1 SL cards NOT REPAIRED (:26, :31, :33): the iteration-uniform null-BF / prior-odds step is asserted, not established — a hypothesis about SL's algorithm, not a model/design condition. LIT-PAR G4 numerical comparison may be cited, labelled | S2:81–84, :191; W2PC1:26,31,33,129,180,193; MINUTES §2.3 | D/E side: proposal (author’s PROOF SKETCH, unchecked). C1new: COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH, this run; crux in §C1) [IDX 443]; Thm5-LH: PROVED (SF: VERIFIED (W3-VEXP); XF: none) [IDX 325; REG 179]; T38-b1-LH: PROVED (SF: VERI… |
| N12 / exponential p | FUTURE_WORK (scope) | N12 OPEN for BB(1,p) with g = n and cap ≍ n; the obstruction is the prior tail and the T02 technique (A:208; B:256; D:197) | S2:188 | — |
| Hellinger / predictive contraction (Song–Liang Thm 1) | FUTURE_WORK (scope) | Not delivered; selection counterpart only | S2:189, :57 | — |
| Sharp ε-scale necessity for §5.3 | FUTURE_WORK (new) | All three proposed necessity forms are COUNTEREXAMPLE (W2PC1:59, :72, :85); C's is a range obstruction for the D_* route only (W2PC2:111–112) | S2:38–41, :192 | — |
| FW1 (frequentist coverage of exact posterior CIs) | FUTURE_WORK (already listed) | Outside §5.4; HQ ruling Q2 | FUTURE_WORK.md:5 | — |
| FW2 (masked final-estimate TV/KL) | FUTURE_WORK (already listed) | Not binding (HQ Q3); needs V11 or N10, both OPEN | FUTURE_WORK.md:6 | — |
| K12 | DROP (R3-4: A, B, C, D in Round 3) | Test oracle, not a guarantee (A, B, D drop; C would defer) | S2:195; MINUTES §2.4 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K34 | DROP as a theorem (R3-4: A, B, C, D in Round 3); the Ĵ half ships as reporting in S-REP | TI evidence is not in the method; Ĵ half ships as reporting (S-REP). (A, B, D drop; C would defer) | S2:196; MINUTES §2.4 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. |
| K66 | DROP | HP3 landscape PARTLY-FALSE (C3-PGD, CEX-localmax(A2)) | S2:197; MINUTES §2.4 | D/E side: proposal (author’s PROOF SKETCH, unchecked). C3-PGD (COUNTEREXAMPLE): “SE and beta-min do not imply progress-greedy dominance: a null that looks like a combination of two truths is added first.” [IDX 988; REG 157]; VPGD-PropG (COUNTEREXAMPLE): “Group… |
| K67 | DROP | Relies on K66 | S2:198; MINUTES §2.4 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row for HP4; LH analogue: T38-b1-LH: PROVED (SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)) [IDX 438; REG 330]; C3-PGD (COUNTEREXAMPLE): “SE and beta-min do not imply progress-greedy dominan… |
| K91 | DROP | Particles-vs-depth speed-up: no accuracy-matched comparator; OPW2-cex refutes the perfect-mixing formula (D:224; A:240) | S2:199; MINUTES §2.4 | D/E side: proposal (author’s PROOF SKETCH, unchecked). No registry row. INP §5 row 8: speed-up vs sequential MCMC → “empty (empirical)” [INP 301]. |
| K98 | DROP | Naive merge KNOWN-FALSE (SHARE-M(b), FD-NM) | S2:200; MINUTES §2.4 | SHARE-M(a): PROVED (SF: VERIFIED (W5-B2ENV); XF: VERIFIED (A-REV3)) [IDX 382; REG 344]; SHARE-M(b) (PROOF SKETCH): “XF: **ERROR** — A-REV6 · REVIEW.md: original ERROR retained; Astra candidate M-star (exact log-RSS, normalised Gram eigenvalues, BM-∞) GAP pendi… |
| K96 (thesis CD) | REMARK (not a theorem): scoped remark after the main theorems, unanimous since Round 2 | No sentence of CD is a non-corollary of M1–M8 (all four agree; A:18, B:57, C:16, D:18) | S2:50, :85; MINUTES §2.1 | D/E side: proposal (author’s PROOF SKETCH, unchecked). D3 draft: “assembled from V1 (KNOWN—CITE + locked), A1 (PROOF SKETCH), D1 (PROVED counting), D2 (PROVED ideal grid / OPEN as-coded), M3 (PROVED), R5 …” [LST 31, 392]; FMP-M3: PROVED (SF: none; XF: ERROR (A… |
| K57 (general accuracy) | FUTURE_WORK (R3-8: B, C) | K57 is split: P1 (the recording-marginal equal-weight bias comparison) is in S-POOL; the general accuracy statement is FW | MINUTES §2.2, §2.3; R3_C:126 | K57 cell: see §2 S-POOL |
| K29 (unconditional favourable stage law) | FUTURE_WORK; the conditional implication is cited in S-STGI | (LL) or the over-tilted q_w input is not a model/design condition and is unexhibited (W2PC1:187 DESIGN-ASSERTED, GAP); IC3 fails | MINUTES §2.2; R3_B:61; R3_C:40, :324 | see §2 S-STGI |
| N5(b) rebuild convergence (with K33) | FUTURE_WORK | K33 ships only in its deterministic termination/count form (M7); rebuild convergence, P(S₀ ∈ V), P(schedule_limit) stay OPEN | MINUTES §2.3 (R3-4); R3_B:141; R3_D:247 | — |
| K73 region-certification clause | withdrawn clause (C, R3-8); K73 is stated without it in S-CERT | Operational region certification not supported | MINUTES §2.2 | see §2 S-CERT |

Dispositions follow MINUTES §2.3–§2.4 (Round 3); `FUTURE_WORK.md` (completed at close) is the authority for the FW list and this table is the registrar's cross-reference. Dissents recorded: K23 (C), K33 placement (D; M7 prevails). The earlier proposal text (SYNTH_R2 §2.4) listed K13, K24, K23, K31, K58, K59, K71, K75, K92, K82, K94, K99 (quantitative), K107, K80 and the scope items; §2.2 and §2.1 'Not main' added K97.

## 5. Dependency edge list (`X → Y`: Y uses X) — union of the four seats' Round 3 §S3(a) edge lists

Sources: `R3_A.md` §S3(a) (lines 168, 170, 172: three prose paragraphs), `R3_B.md` §S3(a) (lines 224–236: key-lemma list and a code block), `R3_C.md` §S3 (lines 247–281: edge table in C's own node names L-N9, L-FK, L-RO, L-DIL, L-WS3/4, L-ATOM, L-N1, L-RANGE, L-ESS, L-PILOT, L-TIE, L-LH, L-LS and engineering nodes A-STREAM, A-GUARD, A-LS0, A-DAG), `R3_D.md` §S3(a) (lines 183–204: cited lemmas and a code block). Cite format: `A3:n` = `R3_A.md` line n, likewise `B3`, `C3`, `D3`. The registrar merged the seats' node names into one vocabulary (a clause label after a node is the seat's own: A, B, C and D letter some clauses differently, e.g. M4(d) in A = M4(e) in B). Edges are deduplicated; a row lists every seat that states it. **Rows stated by one seat only are marked ⚠ (X only).** This list replaces the R2 edge list; R2 edges that no R3 seat restates are in the last subsection. Nothing here is inferred by the registrar.

| # | Edge (X → Y) | Stated by (seat:line) | Note |
|---|---|---|---|
| 1 | S-TARGET → M1 | A3:168 | ⚠ (A only) propriety |
| 2 | S-TARGET → M2 (Lemma 0) | A3:168 | ⚠ (A only) |
| 3 | S-TARGET → M3 | A3:168; B3:236; C3:259; D3:187 | envelopes; C via L-DIL (start normalisation, dilution) |
| 4 | S-TARGET → M4 (N17, K95) | A3:168; B3:236; C3:274; D3:187 | envelope, odds certificate |
| 5 | S-TARGET → M7 | A3:168; C3:267 | C via L-ESS |
| 6 | S-TARGET → S-Z | D3:187 | ⚠ (D only) |
| 7 | S-TARGET → S-REP | D3:187 | ⚠ (D only) |
| 8 | S-TARGET → S-T | C3:258 | ⚠ (C only) exact shipped prior/score in the selection theory |
| 9 | S-TARGET → S-KERNEL | C3:256 | ⚠ (C only) C: S-TARGET → L-N9 → S-KERNEL (match actual target, partition, start, moves) |
| 10 | S-TARGET (duplicates), S-Z (E1c) → S-LIM | A3:172 | ⚠ (A only) |
| 11 | S-KERNEL (N9) → M1(a) | A3:168; B3:227; C3:265; D3:186 | C via L-N9 → L-N1 → M1 |
| 12 | S-KERNEL → M3 | D3:186 | ⚠ (D only) |
| 13 | S-KERNEL → S-REP | D3:186 | ⚠ (D only) |
| 14 | S-KERNEL (K103 minorisation) → S-IDENT | A3:168; B3:233; C3:278 |  |
| 15 | S-KERNEL (K103 minorisation) → M2(b)(iv) (Doeblin constants) | B3:233 | ⚠ (B only) B's clause (b4) |
| 16 | S-KERNEL (tie-DP, L-TIE) → M5 | C3:262 | ⚠ (C only) mathematical launch centre; actual emission still audited |
| 17 | S-BLOCKS → S-KERNEL | C3:256 | ⚠ (C only) C: via L-N9 (actual partition) |
| 18 | S-BLOCKS (PART-ThmA, SIZE) → M3 | A3:168; B3:229; C3:260; D3:188 | C via L-LH → M3(f) |
| 19 | S-BLOCKS (PART-ThmA, SIZE) → M5 | A3:168; B3:229; D3:188 | lemma |
| 20 | S-BLOCKS → M2 (IC3 partition) | A3:168; D3:188 |  |
| 21 | S-BLOCKS → M8 | C3:272 | ⚠ (C only) setup / tables |
| 22 | S-OUT (Lemma RO, GUARD-W, IND-T) → M1 | A3:168; B3:227, 236; C3:266; D3:189 | A: M1(c,d); C: output clauses; B: also Lemma RO, GUARD-W separately |
| 23 | S-OUT (Lemma RO, GUARD-W) → M4 | A3:168; B3:236; C3:274; D3:189 | A: M4(d); B: M4(e); output-event clauses |
| 24 | S-OUT → M5 (0) | A3:168; C3:264; D3:189 | output event / delivered HPM fidelity |
| 25 | S-OUT (K63, K83–K86) → M8 | A3:172; C3:272; D3:189 |  |
| 26 | S-OUT → S-REP | C3:281 | ⚠ (C only) |
| 27 | S-CERT (Theorem A, LS-score, Lemma M, Lemma S; C: via L-LS) → M5 | A3:172; B3:234; C3:263; D3:190 |  |
| 28 | S-CERT (card semantics) → M4 | B3:235; C3:274; D3:190 |  |
| 29 | S-CERT (search cost, K64 scans) → M8 | B3:235; C3:272; D3:190 |  |
| 30 | S-T (T03♯) → M1 | A3:172; B3:232; D3:191 | A: M1(i); B: M1(f); D: M1(d′) |
| 31 | S-T → M2 (c1) | B3:232 | ⚠ (B only) |
| 32 | S-T → M3 | C3:260; D3:191 | C: M3(f) |
| 33 | S-T → M4 (masked statement) | A3:172; B3:232; C3:275; D3:191 | B: M4(f) |
| 34 | S-T → M5 | A3:172; B3:232; C3:263; D3:191 | δ₁ → 0 |
| 35 | S-T → M6 | A3:172; C3:270; D3:191 |  |
| 36 | S-T → S-LEAK | B3:232 | ⚠ (B only) |
| 37 | N1 (key lemma of M1) → S-REP | B3:228 | ⚠ (B only) |
| 38 | M1(a) (E W_r = 1) → M2(b)(iv) | A3:170; B3:228 | A: product-of-stage-averages; B: (b5) E W_r = 1 |
| 39 | M1 (T12 E[Ẑ_r∣𝒞]=Z; probabilistic certificate) → M4 | A3:170; B3:228; C3:274; D3:198 | A: M4(d); B: M4(e); C: probabilistic certificate; D: M1(f) → M4 |
| 40 | M1(f) (R′ declared) → M8 | A3:170; B3:235 | A: M1(f); B: M2(b5) + M1(b) (objective-2 composition) |
| 41 | M1 → S-POOL | A3:170; B3:228, 236; C3:277; D3:198 |  |
| 42 | M1 → S-REP | A3:170; B3:228; C3:281; D3:198 |  |
| 43 | M1 (TV cell bound) → S-IDENT | C3:278; D3:198 |  |
| 44 | S-POOL (K47 cited, K49, K50) → M1(b) | D3:202 | ⚠ (D only) D only; opposite direction to M1 → S-POOL (K50 is in both) |
| 45 | M2(b)(iv) (M₂ ≤ e^{D_*}) → M1 (growth / stacking-rate clause) | A3:170; B3:233; D3:197 | A: M1(i); B: M1 (f, stacking rate); D: M2(a) → M1(d′) |
| 46 | CHK WS3, WS4 (L-WS3/4) → M2(a),(b) | A3:170; B3:229, 231; C3:261; D3:194 |  |
| 47 | CHK WS3 → M3 (e) | A3:170; B3:229; C3:261 |  |
| 48 | FD-W1 → M3 | B3:229 | ⚠ (B only) |
| 49 | T27(i)/Thm5-LH (masking law) → M3 | B3:229 | ⚠ (B only) |
| 50 | M3 → M2(a) (d_σ; c2 masking law) | A3:170; B3:230; D3:192 |  |
| 51 | M7 (T, count, envelope) → M2(b) stage-count clauses | A3:170; B3:231; C3:269; D3:196 | A: sandwich, envelope; B: (b6),(b6′); D: (b)(iii) |
| 52 | S-IDENT (K25, K104) → M2 | A3:170; B3:231; D3:193 | A: M2; B: K25 → M2(b6); D: M2(b). C states the opposite direction (M2 → S-IDENT, below) |
| 53 | M2 (W rates) → S-IDENT | C3:278 | ⚠ (C only) C only; opposite direction to S-IDENT → M2 (A, B, D) |
| 54 | M6 / Lemma KL (K105) → M2 | A3:170; B3:232; D3:194, 195 | A: M2(a) lower bound; B: M2(c2); D: M2(c). C routes through L-ATOM instead (next rows) |
| 55 | L-ATOM (finite singleton algebra) → M6 | C3:270 | ⚠ (C only) |
| 56 | L-ATOM → M2(c) | C3:271 | ⚠ (C only) C: shared finite-law obstruction, not through a new M6 proof |
| 57 | CHK WS6(d), WS7 → M2(c) | C3:269; D3:194 |  |
| 58 | L-RANGE (D_*-lemma; C's decomposition) → M2(b) | B3:231; C3:268 | C: L-N9, L-FK → L-RANGE → M2(b) |
| 59 | K25 coverage identity → M2 (b6) | B3:231 | ⚠ (B only) |
| 60 | M3 → M6 | A3:170; B3:230; C3:270; D3:192 | π₀(S₀) law; C: M3(f) |
| 61 | M3 → M5 | A3:170; B3:230; C3:263; D3:192 | start mode, centre; C: M3(f) |
| 62 | M3 → M4(e) | D3:192 | ⚠ (D only) |
| 63 | M3 (A₀) → M7(d) | A3:170 | ⚠ (A only) |
| 64 | M3 → S-Z | A3:170; B3:236 |  |
| 65 | M3 → S-POOL | B3:236 | ⚠ (B only) |
| 66 | M3 → S-LEAK | B3:230 | ⚠ (B only) |
| 67 | M3 → S-REP | C3:281 | ⚠ (C only) |
| 68 | S-IDENT (K25, coverage identity; C: L-ESS) → M7 | A3:170; B3:231; C3:267; D3:193 |  |
| 69 | Theorem G → M7 | B3:231 | ⚠ (B only) |
| 70 | L-PILOT (coded bisection/progress invariant) → M7 | C3:267 | ⚠ (C only) |
| 71 | S-IDENT → M6 | D3:193 | ⚠ (D only) |
| 72 | S-IDENT → S-REP | A3:170; D3:193 |  |
| 73 | L-ESS (K25 coverage identity) → S-IDENT | C3:278 | ⚠ (C only) |
| 74 | M7 (K30 cited) → S-STGI | B3:231; C3:279 | B: K30 cited; C: STG-M recurrence, cited K28 → S-STGI. D states the opposite direction (S-STGI → M7(c), next row) |
| 75 | S-STGI (K29, K30) → M7(c) | D3:201 | ⚠ (D only) D only; opposite direction |
| 76 | M7 → M6(d) (comparison) | D3:196 | ⚠ (D only) |
| 77 | M7 (T) → M8 | A3:172; B3:235; C3:273; D3:196 | C: calibration simplification (each trajectory retains its own grid) |
| 78 | M5 (b1-LH; M5(2)) → M4 (masked statement) | A3:172; B3:234; C3:275; D3:199 | A: M4 masked; B: M4(f); D: M4(e) |
| 79 | N13 retention (+ Lemma S, inheritance merge) → M4(c) | A3:172; B3:234; C3:275 | C: retention lemma → M4 masked |
| 80 | T38-b1-LH, LS-score / Theorem A → M5 | B3:234; C3:263 |  |
| 81 | M5 (LS0 baseline search) → M8 | B3:234; D3:199 | B: LS0 cost; D: search term |
| 82 | M4 → S-REP (card labels) | A3:172 | ⚠ (A only) |
| 83 | M4 (envelope) → S-Z | D3:200 | ⚠ (D only) |
| 84 | M4 → S-LIM | B3:236 | ⚠ (B only) cited |
| 85 | M2(a) (D_* bound) → S-REP | A3:170; B3:233; C3:281; D3:197 | A: η̂ domain and Ĵ tail; B: η̂ domain, D_* in the Ĵ bound |
| 86 | M2(a) (D bound) → S-Z | A3:170; B3:233; C3:276; D3:197 | C: range corollary |
| 87 | M2(b) → M8 (remark) | B3:235; D3:197 | D: remark; B: M2(b5) + M1(b) objective-2 composition |
| 88 | M2 → S-LEAK (F, S) | D3:197 | ⚠ (D only) A's literal edge is 'S-LEAK → M2 (supplement corollary)' (A:170), i.e. the opposite direction; the substance is the same (corollary of M2) |
| 89 | L-FK / SMC-cited (Del Moral 2004; DDJ 2006; WLH 2016) → M1 | B3:227; C3:265; D3:183 | B: T12 → M1; C: L-FK → L-N1 |
| 90 | L-FK, OPW2 → S-Z | C3:276 | ⚠ (C only) |
| 91 | T12 → M1 | B3:227 | ⚠ (B only) |
| 92 | GUARD-W (audit) → M1, M4, S-OUT | B3:227 | ⚠ (B only) |
| 93 | A-GUARD (GUARD-W audit) → S-OUT, M5 | C3:257, 264 | ⚠ (C only) |
| 94 | A-STREAM (integrated streams audit) → S-OUT | C3:257 | ⚠ (C only) |
| 95 | A-LS0 (LS0 audit) → M5 | C3:264 | ⚠ (C only) |
| 96 | A-DAG (execution-DAG audit) → M8 | C3:272 | ⚠ (C only) |
| 97 | Filed counterexamples → S-LIM | A3:172; C3:280; D3:203 | A: S-LIM is a leaf; D: S-LIM → discussion only |
| 98 | cited SLLN / ratio lemmas → S-POOL | C3:277 | ⚠ (C only) |
| 99 | Chatterjee–Diaconis 2018 → M6 | D3:183 | ⚠ (D only) |
| 100 | Gelman–Meng 1998 → S-REP, M6 | D3:183 | ⚠ (D only) |
| 101 | Štefankovič–Vempala–Vigoda 2009 → M7 | D3:183 | ⚠ (D only) |
| 102 | Barbieri–Berger 2004 → M5, S-TARGET | D3:183 | ⚠ (D only) |
| 103 | Rossell 2022 → M5 | D3:183 | ⚠ (D only) |
| 104 | Brent 1974 → M8 | D3:183 | ⚠ (D only) |
| 105 | M8 and all main items → CD remark (K96) | D3:204 | ⚠ (D only) |

*Counts:* 105 edge rows after deduplication; stated by 4 seats: 21; by 3: 16; by 2: 14; by 1 (⚠): 54.

### 5.1 Direction and clause disagreements between the seats (not resolved here)

- **M2 ↔ S-IDENT.** A3:170, B3:231, D3:193: S-IDENT (K25, K104) → M2. C3:278: M2 (W rates) → S-IDENT. Different clauses of K25/K103 are probably involved (the coverage identity feeds M2(b); the W-rate bound feeds C's C15 clauses); the registrar does not decide. Resolve: HQ `M2` and HQ `LP-IDENT` (both wave 2) must state which clause each package owns.
- **M7 ↔ S-STGI.** B3:231 and C3:279: M7 (K30 cited) → S-STGI; D3:201: S-STGI (K29, K30) → M7(c). K30 is stated in M7 as a labelled ideal-grid clause and restated in S-STGI (MINUTES §2.1, §2.2). Resolve: HQ `M7` and HQ `LP-IDENT`.
- **M1 ↔ S-POOL.** A3:170, B3:228, C3:277, D3:198: M1 → S-POOL. D3:202 only: S-POOL (K47 cited, K49, K50) → M1(b). K50 is an M1 clause and is also in S-POOL. Resolve: HQ `M1` and HQ `LP-REST` (the clause-level reading, not a package cycle, is expected).
- **M6 → M2.** A3:170 puts Lemma KL on M2(a)'s lower bound; B3:232 and D3:194–195 put M6 / Lemma KL under M2(c). C3:270–271 routes M2(c) through L-ATOM and does not state M6 → M2(c) ("without depending on a new M6 proof"). Resolve: HQ `M2` and HQ `M6`.
- **M2 ↔ S-LEAK.** D3:197: M2 → S-LEAK (F,S). A3:170 writes 'S-LEAK → M2 (supplement corollary)', the opposite literal direction with the substance of D's edge. Resolve: HQ `LP-REP` (S-LEAK is a corollary of M2; MINUTES §2.2).
- **M1 ↔ M2 (clause level).** M1(a) → M2(b)(iv) (E W_r = 1; A3:170, B3:228) and M2(b)(iv) → M1 growth clause (A3:170, B3:233, D3:197). Not a package cycle if the clause order is kept; HQ `M1` and HQ `M2` should fix the order.
- **Clause labels.** The same edge carries different clause letters: S-OUT → M4(d) (A3:168) vs M4(e) (B3:236); M1 → M4(d) (A3:170) vs M4(e) (B3:228); M5 → M4(e) (D3:199) vs M4(f) (B3:234). Each HQ must map its own card's letters.

### 5.2 Wave check (mechanical: producer wave later than consumer wave, MINUTES §2.5)

Waves: 1 = M1, M3, LP-FOUND (S-TARGET, S-BLOCKS, S-KERNEL; S-T cited). 2 = M2, M7, M6, LP-IDENT (S-IDENT, S-STGI). 3 = M5, M4, M8, LP-AUDIT (S-CERT, S-OUT). 4 = LP-REST (S-Z, S-POOL, S-LIM), LP-REP (S-REP, S-LEAK). Rows above that put a later-wave producer under an earlier-wave consumer:
- **S-OUT (wave 3) → M1 (wave 1)**, stated by all four seats (A3:168; B3:227, :236; C3:266; D3:189). M1's clauses (c),(d) rest on Lemma RO, GUARD-W and the IND-T extension, whose audits are in LP-AUDIT. M1 carries them as named premises; its fallback is the potential-run statements (R3_A:192). In A's own wave plan S-KERNEL + S-OUT were wave 1 (A3:178). The chair's merged waves (MINUTES §2.5) differ; flagged for the chair/HQ, not changed here.
- **M2(b)(iv) (wave 2) → M1 growth clause (wave 1)** (A3:170; B3:233; D3:197). The M₂ ≤ e^{D_*} step is in M2; M1's growth clause (g)/(i) waits for it.
- **S-POOL (wave 4) → M1(b) (wave 1)**: D only (D3:202), a clause-level direction anomaly (see 5.1).
- Same-wave edges are not listed (e.g. M5 → M4(f), S-CERT → M5, S-IDENT ↔ M2, S-STGI ↔ M7).

### 5.3 R2 edges that no Round 3 §S3(a) restates (kept for provenance only; not part of the edge list)

- L-DEC (K62 MPM margin) → M1 clause (f)/(e) (R2: A:54(e); D:56(f); B:129(4)).
- L-WS6 (WS7(a)) → M6 Lemma KL (R2: A:119; CHK:79).
- M2(b)(iv) → S-POOL (R2: A:139 '(ii) moved to M2(b)'; B:199).
- M1 (frozen 𝒞, IND-T over streams 10..9+R′) → S-OUT / stacking K84 (R2: A:44; METHOD:142, :401).
- M5 (b1-LH) and S-T → the K97 FW entry (R2: A:129(d); B:159(c),(d); D:93(c),(d)); K97 is now FUTURE_WORK (R3-3).

## 6. Registry CONFLICT rows (⚑) touching the list

`REGISTRY_INDEX.md` §5.A (copied from `REGISTRY_v2.md` §A2): the registry records both sides; no resolution is proposed here. Rows that name an ID used by the list:

- **C18** (`IDX:1192`): IDs `Cost-T38`, `T32(i)`
  - v2. T32(i): W5-LOCKBOOK PROVED, W7-SEC re-count 'no error' (same family) vs W6-FIXREV1 T38 dependency k1 and W7-SEP input I11 'CONJECTURE'. The latter are stale (they predate or ignore W5-LOCKBOOK), not dissenting. Recorded PROVED (author W5-LOCKBOOK), same family only; T38 v3 cites PROVED-UNDER T32(i).
- **C12** (`IDX:1186`): IDs `Lemma0(a,c)`
  - A-REV2's table calls the case 'initial centre already is the truth' trivial success; W6-FIXREV2 §3.1 disputes the wording (CEX-2 design: a search started at S₀ moves to S₀+x₃). A-REV2's §4.2 text is consistent with W6's correct statement.
- **C1** (`IDX:1175`): IDs `Lemma0(b)`
  - W1-T37R Lemma 0(b) PROVED → W3-VT37R: inclusion VERIFIED but the 'posterior miss' inference ERROR (CEX-2), repair R2 stated PROVED → A-REV2: Lemma 0(b) as written ERROR **and** R2 itself ERROR (omits inferior local maxima / capped searches ending below the truth). Both recorded; W6-FIXREV2 (REPORT.md) replaces them by Lemma 0(b′) and the three-way Prop. F — same-family, unreviewed. W6-FIXREV2 §3.1 also disputes A-REV
- **C19** (`IDX:1193`): IDs `SEP-E`
  - v2. W7-SEP SEP(E)'s v3 row is conditional on T32(i) as a CONJECTURE (I11); W5-LOCKBOOK proves T32(i). Same staleness as the Cost-T38 conflict. W7-SEP also cites only O-BGIBBS BG1 (PROOF SKETCH), not BG3 (PROVED) + LH-lock (PROOF SKETCH).
- **C22** (`IDX:1196`): IDs `STG-Wp`
  - v2. O-STAGES Cor. W′ rests on (LL), F-DRAFT Theorem W's layer law, vs O-WSTAB's COUNTEREXAMPLE to F-DRAFT W(c) and W(b) on the divergent side (2Ar > 1). O-WSTAB's own W′ (ORTH, T_ideal ∈ {1, 2}) is PROVED independently and is consistent. (LL) may need restating for 2Ar > 1.
- **C11** (`IDX:1185`): IDs `T38-(0)`
  - Scope of A-REV1: it reviewed W1-T38E's T38(b)-R, not W4-T38FULL (W6-FIXREV1 §3.1: several A-REV1 §7 repairs were already in W4). A-REV1's GAP applies in full to W1-T38E's statement and only to residual items for W4; W6-FIXREV1's T38 files supersede both.
- **C24** (`IDX:1198`): IDs `T38-b1-LH`, `T38-b1-LH-iidfail`
  - v2 (cross-family vs cross-family). The (b1-LH) clause 'Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞': A-REV5 ERROR (slow-p counterexample, p ≍ log log n) vs A-REV8 GAP (the ceiling does not vanish, but this is not a counterexample to the actual production Q_f, which may run on the exact branch). Both give the same repair (n^{1−c/2}p^{−c}log²n → 0). Recorded at the weaker verdict, ERROR, on the clause only; the LS0 consistency 

## 7. Status disagreements between sources

Each line gives both sides with their sources. None is resolved here.

- **OWS-WS3, OWS-WS4.** Registry: `PROVED (SF: none; XF: none)`, flag AUTHOR-ONLY (IDX:404–405). Cards and checks: CHK:13–14 'VERIFIED (PC1, cross-family, line by line)'; A:68 notes the registry rows are not yet updated; W2PC1:44 keeps both as separate entries. **Resolve:** registry owner (status row update, recommended in §9); no HQ action.
- **OWS-WS6(d), OWS-WS7.** Registry: `PROVED (SF: none; XF: none)`, flag AUTHOR-ONLY (IDX:411, :413). CHK:11–12: VERIFIED WITH AMENDMENT (amendments adopted by all four seats). **Resolve:** registry owner (§9). HQ `M2` carries the CHK amendments in part (c) (Proposition ONE-SHOT).
- **N9K (kernel facts, start sampler).** Registry/index: `PROVED (candidate)`, flag AUTHOR-ONLY (IDX:72). CHK:15: VERIFIED WITH AMENDMENT; A:46 'registry row to be opened'. Also THEOREM_LIST 'no registry row' vs LOCKED_PROOFS row T09 vs branch N9-KERNEL: IDX §5.B B2. **Resolve:** registry owner (open the N9K row; §9) and the THEOREM_LIST/LOCKED_PROOFS/branch naming question (IDX §5.B B2). HQ `LP-FOUND` states S-KERNEL with the CHK amendments.
- **K10, K11 (σ²-coupling, cross-block bound).** R0_DIFF:84, :85: 'No registry row' for the decomposition / bound. R2 cards cite registry rows OWS-WS3 / OWS-WS4 for the same content (A:68; B:215; D:140). The registry rows exist in the index (IDX:404–405). R0_DIFF's cell and the cards' status lines therefore differ on whether a registry row exists. **Resolve:** registry owner (which registry row backs K10/K11). HQ `M2` and HQ `M3` cite OWS-WS3/OWS-WS4 as the rows of record.
- **Prop2(a,b,d,e).** THEOREM_LIST V1(iii): 'PROVED-LOCKED'. Registry: author PROVED, `SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4)`, not in the strict-lockable list; the locked wave-1 result is T12 (IDX §5.B B10). **Resolve:** registry owner (PROVED-LOCKED vs author-PROVED with XF GAP). HQ `M1` quotes the registry status, not the draft's.
- **T38-b1-LH (K69, K67).** Author PROVED, `SF: VERIFIED* (W5-VMASK); XF: VERIFIED* (A-REV8)` (index flag XF-VERIFIED*(qualified)); but the registry carries a CONFLICT (C24) on the iid sub-claim: A-REV5 ERROR vs A-REV8 GAP; LS0 consistency conclusion VERIFIED by A-REV8 (IDX:1198). W2PC2:88 notes the cards omit the ⚑ marker. **Resolve:** registry owner (CONFLICT C24); HQ `M5` restores the ⚑ marker in its card status (W2PC2:88). K67 is dropped.
- **T32(i), Cost-T38 (K87, K88).** T32(i): `PROVED (SF: VERIFIED (W7-SEC); XF: none)`, flag SAME-FAMILY-ONLY; Cost-T38: `PROVED-UNDER (SF: VERIFIED (W3-VT38E); XF: GAP (A-REV5))`. Registry CONFLICT C18: W6-FIXREV1 / W7-SEP 'CONJECTURE' dissent recorded as stale (IDX:1192). A:131 and B:171 omit the SAME-FAMILY-ONLY flag; C:132 states it; W2PC2:88 notes the ⚑ omission. **Resolve:** registry owner (CONFLICT C18); HQ `M8` restores the SAME-FAMILY-ONLY flag in its card status.
- **STG-Wp (K29).** `PROVED-UNDER (SF: none; XF: none)`; registry CONFLICT C22 with O-WSTAB's COUNTEREXAMPLE to F-DRAFT W(b),(c) on the divergent side (IDX:1196); STG-cexW2 COUNTEREXAMPLE: 'F-DRAFT's O(1) stage count is false'. **Resolve:** registry owner (CONFLICT C22); HQ `LP-IDENT` states K29 only as a cited conditional implication (MINUTES §2.2).
- **MZ-P3 (K42/K43/K45; M4).** Index: `PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery`, flag AUTHOR-ONLY, candidate: not reviewed (IDX:201). SYNTH_R2:266 requires D.M3′ to restore 'candidate, not reviewed, not adopted', AUTHOR-ONLY; D:74 writes MZ-C1 'PROVED (C1-C3 per-fit, deterministic)' with the qualifier only on MZ-P3. IDX §5.B B3: FMP-M3 `XF: ERROR (A-REV9)` vs D3(iii) citing M3 as PROVED. **Resolve:** registry owner; HQ `M4` restores 'candidate, not reviewed, not adopted', AUTHOR-ONLY in its card (SYNTH_R2:266).
- **T26BUD-G, DIL-E, T26 flags (M7, M3).** W2PC2:85–88: minor omissions remain in C's cards — T26BUD-G's own AUTHOR-ONLY flag (C8), 'SF none' on DIL-E (C5), registry ⚑ CONFLICT markers on T32(i) (C7) and T38-b1-LH (C3). **Resolve:** HQ `M7` (T26BUD-G's own AUTHOR-ONLY flag), HQ `M3` ('SF none' on DIL-E), HQ `M8` (⚑ on T32(i)), HQ `M5` (⚑ on T38-b1-LH); registry owner for the ⚑ rows themselves.
- **Thm5-LH (K17/K18, M3, S-T-adjacent).** `PROVED (SF: VERIFIED (W3-VEXP); XF: none)`, flag SAME-FAMILY-ONLY (IDX:325). Qualifier omitted in R1, restored in R2 (W2PC2:131, W1PC2:76 flag (b)). Consistent in all four R2 cards. **Resolve:** HQ `M3` and HQ `M5` carry the SAME-FAMILY-ONLY qualifier (R3_C:297; R3_D:223); registry owner: none.
- **T01–T03 (S-T).** `PROVED-LOCKED (wave 3; external review queued)`, flag SAME-FAMILY-ONLY (IDX:469). W2PC2:159 'T01 … external review queued; SAME-FAMILY-ONLY' — flag (b) minor in W1PC2 (omitted in R1). **Resolve:** registry owner (external review queued); HQ `LP-FOUND` states the flag where S-T is cited.
- **LS0 in the production core (M4, M5, S-CERT).** THM-INV §1 row 12 / METH-AUDIT: 'LS0 is not in the production core' vs REGISTRY_v2 §I: 'LS0 is part of the method' (IDX §5.B B4). METHOD:48, :399: not yet in the production core, merged-LS0 replay pending; LS0 changed the HPM in 0/2,394 test-export fits. **Resolve:** registry owner / METHOD owner (merged-LS0 replay); HQ `M5` and HQ `LP-AUDIT` carry it as the named premise N2(c) (§8).
- **MA-PropW (S-OUT).** THEOREM_LIST V2: executed check on '1/1 completed design'; METH-AUDIT: '3/3 study designs'; METHOD:46: 'executed bitwise on smoke + 3/3 study designs' (IDX §5.B B1). **Resolve:** registry owner (1/1 vs 3/3 designs); HQ `LP-AUDIT` (N2(a) replay count is part of its audit).
- **K97 SL (R3-3).** R0_DIFF class CONFIRMED-DE; registry C1new `COUNTEREXAMPLE (numerical, LIT-PAR G4) + PROOF SKETCH (NEW-SYNTH)` (cards A:129, B:161, D:95). W2PC1:26, :31, :33, :129, :180, :193: NEEDS-HYPOTHESIS, NOT REPAIRED in all three checked cards. Seat placements differ: C FUTURE_WORK (C:17), A, B supplement (A:19; B:58), D main (D:92) (S2:81). **Closed for placement by MINUTES §2.3 (R3-3): FUTURE_WORK, unanimous.** The status disagreement (registry COUNTEREXAMPLE numerical + PROOF SKETCH vs NOT REPAIRED) stays with the registry owner.
- **PC1 claim 3 / N1 (M1).** N1 `PROOF SKETCH` [INP 131]; PC1c3 `PROVED (PC1 claim 3)` with 'E[W_r ĥ_r] = π(h) is still a premise' (R0_DIFF:140). W1PC2:101 and W2PC2 §0 TRUE-AS-WRITTEN numerically on a coded-grid replica — sanity only; the status stays PROOF SKETCH. **Resolve:** registry owner (status stays PROOF SKETCH); HQ `M1` (N1 is the binding crux; §13.1 safeguard).
- **K95 placement.** A: main Z𝒯 (A:85, A:89(f)); B, D: supplement (B:187; D:107); C: cited (C:44). Proposal: supplement (S2:94). **Closed by MINUTES §2.1/§2.2 (R3-4 unanimous): S-TARGET.**
- **Song–Liang Thm 2 / Cor 2 wording (R3-7).** Thm 2: B 'not applicable, fixed design' (B:70), A 'selection matched' (A:31), C/D fixed-design selection counterpart (C:393; D:235). Cor 2: A 'a comparison', B 'SL's separate GAP', C 'no analytic null-exclusion/FDR separation established', D 'covered by SL′ only if it ships' (S2:60–62). **Closed by MINUTES §2.3 (R3-7): the wording adopted there is the one to use** (C's Cor 2 wording, adopted by B and D). HQ `M6`/`LP-FOUND` (S-T) apply it.

- **Lemma-pack count.** `MINUTES.md` §4 says '4 lemma-pack charters'; `MINUTES.md` §2.5 names five (LP-FOUND, LP-IDENT, LP-AUDIT, LP-REST, LP-REP). This registry uses five. **Resolve:** chair/clerk (`MINUTES.md` §4 and `HQ_CHARTERS/`). **Resolved by the chair 2026-11-04:** MINUTES §4 corrected to five.
- **S-STGI seat positions.** MINUTES §2.2: 'B (FW) and C (conditional cited) prevail over A and D (supplement conditional)'. R3_A:43, :67, :108: A objects to S-STGI ('dissolve: K30 → M7(d), K29 → FUTURE_WORK'); R3_D:45, :135: D keeps K29 conditional in S-STGI. A's position as filed matches B's, not D's. **Resolve:** chair (`MINUTES.md` §2.2 wording); the outcome (K29 only as a cited conditional implication; K30 in M7 and restated) is unchanged. **Resolved by the chair 2026-11-04:** MINUTES §2.2 corrected; S-STGI dissolved (A, B, C), dissent D.
- **N3 DP invariant.** R3_B:304: 'N3 → hypothesis in M5; DP invariant FW'. MINUTES §2.3: the N3 DP invariant is a named implementation premise in the charters; R3_D:221: it is the first lemma of the M5 charter. **Resolve:** chair (MINUTES prevails); HQ `M5` carries it (§8).
- **Which charters carry N2.** R3_B:304: N2 → M1, M4, M5 charters; R3_D:250: M1, M4, M5, Prop D charters, with S-OUT stating what is proved; R3_C:330, :377: S-KERNEL/S-OUT/M5/M8. **Resolve:** the clerk/chair in `HQ_CHARTERS/` (the registry's §8 lists the union).
- **K33 placement.** A, B, C: M7 (deterministic termination/count form); D: S-IDENT (R3_D:25, :42, :131). MINUTES §2.3 decides M7 by majority. **Resolve:** closed; D's dissent recorded.
- **K62 placement.** B's R2 card placed K62 in the HPM item (B:125); MINUTES §2.1 places it in M1. **Resolve:** closed by MINUTES; HQ `M1` and HQ `M5` note the use of the MPM margin.
- **ū̂ description.** S2:218 describes ū̂ as 'the maximal fit fraction on V (D:182)'; D:182 and AMENDMENT_HQ_02 §A2 define ū̂ = Σ_b max_{U⊆C_b} x_b(U) from the block tables. MINUTES §2.2 adopts D's. **Resolve:** closed for the definition; HQ `LP-REP` and the AMENDMENT owner keep SYNTH_R2:218 out of the charter.
- **Jeffreys-bound inequalities.** A:158: J ≤ osc(d)²/4; B:215 and C:261: J ≤ osc d; D:126: J ≤ 2·osc d (NOTATION.md §2 (iii)). The sources state different inequalities; the registrar does not judge them. **Resolve:** HQ `M2` / HQ `LP-IDENT` (K104 calculus) state the one the card uses.

## 8. Named implementation premises / audit obligations

These are neither theorems, nor FUTURE_WORK items, nor cited lemmas, nor drops, so the close rule has no slot for them. They are **named implementation premises in the HQ charters** (MINUTES §2.3, 'Audit obligations'; seat B's 'missing' item 2, R3_B:315, adopted). They are code-audit or execution facts, not model/design assumptions and not newly proved lemmas (R3_C:252). "Carried by" lists the HQ charters named by the seats; where seats name different charters the union is given and the clerk's `HQ_CHARTERS/` is the authority (§7, 'Which charters carry N2'). Status words are copied from the sources.

**Name map (the same obligation under several names; each name the chair listed appears in the first column of the row that carries it).** GUARD-W = N2(e) = C's A-GUARD. IND-T extension = N14(c) (IND-T for streams 10..9+R′). 'Integrated streams' = C's A-STREAM = N2(b) (persistent per-worker stream state) + N14(c). 'LS0' premise = N2(c) + OP-LS0 + the emitted centre (N3). 'Execution DAG' = C's A-DAG = D's trajectory inventory.

| Premise | Statement | Status (source wording) | Carried by (HQ charter) | Used by | Source |
|---|---|---|---|---|---|
| **N2(b)** (W-cal) | The 4 diagnostic (calibration) islands, with persistent per-worker stream state, are bitwise equal to the serial run | PROVED by code reading, **not executed** (INP N2) | LP-AUDIT (`HQ_CHARTERS/LP-AUDIT.md`: S-OUT K83); M8 (calibration trajectories of the DAG) | S-OUT K83; M8; Lemma-STREAM | INP N2 (`origin/theory/MEET-v31:…/THEOREM_REVISION_INPUTS.md:136–138`); R0_DIFF:192 (K83); R3_C:330, :377; R3_D:250 |
| **N2(c)** (LS0 integration) | LS0 leaves island outputs, Ẑ, PIPs bitwise unchanged; 𝒯_new = top_c(𝒯_old ∪ 𝒮_added); fires no E3 | **not in the production core**; merged-LS0 replay pending (INP N2; METHOD:48, :399); self-flag 'integrated LS0 … audits open' (R3_D:150) | M5 (first lemma in parallel with N3: R3_D:221); M4 (N13 retention under the coded LS0 rule: R3_B:262); M8 (LS0 counted); LP-AUDIT | M5, M4(c), M8 | INP N2; R3_A:180; R3_D:221, :225; R3_B:262 |
| **N2(e)** = **GUARD-W** (A-GUARD) | Any worker, merge or LS0 stop, or guard stop ⇒ no output (stop-only coupling) | **not audited** (API-AUDIT covered the serial v3 guard only; INP N2(e)). Lemma RO itself stays as recorded (XF VERIFIED* by A-REV6) | M1 (premise of (c),(d)); M4 (e) (R3_B:262, :265); M5; LP-AUDIT (S-OUT) | M1, M4(e), M5, S-OUT, S-REP (output form) | INP M6 (:31), N2 (:136–138); R0_DIFF:181 (K77); R3_A:119, :192; R3_B:213–214; R3_C:142, :257, :264; R3_D:139, :213 |
| **N14(c)** = **IND-T extension** | IND-T for streams 10..9+R′ (independence of the final streams from 𝒞 and each other for R′ = 4k > 4) | **code audit, not done** (INP N14(c)); audited for R′ = 4 only, extension pending (R3_A:119); registry: IND-T PROVED (SF: none; XF: VERIFIED* (A-REV1)); Lemma-STREAM AUTHOR-ONLY (IDX:85–86) | M1 (stacking clauses, (c),(d)); LP-AUDIT (S-OUT K86, K84) | M1, S-OUT K84/K85/K86, S-POOL | INP N14 (:228–231); R0_DIFF:195 (K86); R3_A:119, :192; R3_D:139 |
| **N3 DP invariant** (e4 tie-DP) | The max-plus DP returns the prescribed smallest-size, lexicographically smallest start-mode maximiser without enumerating ties | **OPEN** (INP N3; R0_DIFF:83 K09); W1PC2 D9: TRUE on 400 random instances, DESIGN-ASSERTED (R3_D:221) | M5 (first lemma; fallback: (b1-LH) conditional on N3 after one HQ cycle, R3_D:224); LP-FOUND (S-KERNEL K09 tie-DP proposition); M4 (hypothesis in (f), R3_B:213) | M5 (b1-LH), M4(f), S-KERNEL K09 | INP N3 (:143–146); R0_DIFF:83; R3_D:221, :224; R3_B:213, :304 (disagreement, §7) |
| **Integrated streams** (A-STREAM) | The integrated v3.1 core's stream layout (calibration streams 0–9, final streams 10..9+R′, per-worker state) matches the stream contract | audit obligation (R3_C:252); overlaps N2(b), N14(c) | LP-AUDIT (S-OUT); LP-FOUND (S-KERNEL: R3_C:330) | S-OUT K83–K86; M1 | R3_C:252, :257, :330 |
| **LS0** (A-LS0; OP-LS0; emitted centre) | The shipped LS0 is the specified local search from S̃₀ (reads no uniforms; completed scans; emitted centre = prescribed start mode) | not in the production core (METHOD:48, :399; registry §7 'LS0 in the production core'); LS0 changed the HPM in 0/2,394 test-export fits (METHOD) | M5; M4; M8; LP-AUDIT | M5 (reported-HPM consistency), M4(f), M8 | R3_C:252, :264; R3_D:150, :225; R3_A:180 |
| **Execution DAG** (A-DAG) | Trajectory inventory: every executed pilot, diagnostic, rebuild and final trajectory with its own (N_i, T_i, L_i); every completed search | **NOT REPAIRED / GAP** (W2PC2:133; W2PC1:181, :194, :205); 'the open audit' (R3_D:230) | M8 (first lemma: R3_D:230); LP-AUDIT | M8 (a)–(c) | R3_D:164–174, :230; R3_C:272; SYNTH_R2:267 |
| **Read-only d accumulator** (AMENDMENT_HQ_02 §A1) | Read-only record of the bridge potential d at initialisation and at the four measured endpoints; no new draws, transitions or scores; no feedback; d a default member of the declared list 𝓗 (fixed before stream 10, reads no uniforms) | per-particle d values exist during execution but **are not retained today** (SYNTH_R2:230; W2PC2:72, :146); historical fits report NA; HQ Q4 conditions met | LP-REP (S-REP; `HQ_CHARTERS/LP-REP.md`) | S-REP (Ĵ, ε̂_×) | AMENDMENT_HQ_02_DEFINITIONS.md §A1 (lines 36–41); SYNTH_R2:230; R3_A:77; R3_B:98, :323; R3_C:92, :214; R3_D:86 |

**Escalations tied to these premises** (MINUTES §2.3; seat charters): GUARD-W or IND-T extension audit fails → M1 (c),(d) revert to potential-run statements and N2 reopens (R3_A:192); GUARD-W audit fails → M4(e) in potential-run form only (R3_B:214); N3 fails outright or the integrated LS0 differs from the specified LS0 → HQ decides (R3_D:225); the DAG audit finds an uncounted serial component → M8 (a)/(b) restated, not dropped (R3_D:174). Other premises named inside the cards (EX-A exact arithmetic, EX-S/H-U exact iid uniforms, CAL frozen 𝒞, SR, Lemma S merge) are model/design or code facts stated in the cards and are not audit obligations of this table.

## 9. Registry updates recommended to the registry owner

The registry owner decides; **this file changes no registry status**. The right-hand column is the meeting's check verdict, i.e. a statement-sanity / cross-family review verdict (`evidence/CHK_INHERITED/REPORT.md`), not an adoption decision and not a proof status.

| Registry ID | Registry status now (index) | Meeting's check verdict (cross-family: PC1, gpt-6.1-sol, line by line) | Recommended entry | Source |
|---|---|---|---|---|
| OWS-WS3 | PROVED (SF: none; XF: none), FLAG AUTHOR-ONLY (IDX:404) | VERIFIED | **XF: VERIFIED (CHK, cross-family, line by line)** | CHK:13, :93 |
| OWS-WS4 | PROVED (SF: none; XF: none), FLAG AUTHOR-ONLY (IDX:405) | VERIFIED | **XF: VERIFIED (CHK, cross-family, line by line)** | CHK:14, :112 |
| OWS-WS6(d) | PROVED (SF: none; XF: none), FLAG AUTHOR-ONLY (IDX:411) | VERIFIED WITH AMENDMENT (bounded-block TV scope) | **XF: VERIFIED WITH AMENDMENT (CHK)**; amendment adopted by all four seats | CHK:11, :34 |
| OWS-WS7 | PROVED (SF: none; XF: none), FLAG AUTHOR-ONLY (IDX:413) | VERIFIED WITH AMENDMENT (initial vs later presence; restricted-set stage-count qualification) | **XF: VERIFIED WITH AMENDMENT (CHK)** | CHK:12, :70 |
| N9K (kernel facts, start sampler; N9-KERNEL §§0–3) | PROVED (candidate), FLAG AUTHOR-ONLY (IDX:72); A:46 'registry row to be opened' | VERIFIED WITH AMENDMENT (claims G, U, N, I, R, Z, S check against code; prose corrections CHK:155–161) | **XF: VERIFIED WITH AMENDMENT (CHK)**; open the registry row | CHK:15, :134 |

Related entries that need no status change:
- **One-shot refutation** (HQ Q1(c)): survives in the shipped bounded-block setting (CHK:177–195, §6); recorded on the OWS-WS6(d)/WS7 rows.
- **N1** (M1's binding crux): stays PROOF SKETCH; PC1c3 PROVED with 'E[W_r ĥ_r] = π(h)' as premise; the numerical checks (W1PC2:101, W2PC2 §0) are statement-sanity only.
- **Check wave results** (W1_PC1: 11 COUNTEREXAMPLE, 25 NEEDS-HYPOTHESIS on A, B, D; W1_PC2: 0 COUNTEREXAMPLE on C; W2_PC1: 9 COUNTEREXAMPLE; W2_PC2: 29/29 TRUE-AS-WRITTEN) concern seat-card clauses, not registry rows; they are listed per item above as statement-sanity verdicts. OWS-WS6e (CONJECTURE) and OWS-WS8d (OPEN) are unchanged.

*End of registry. No file other than this one and `NOTATION.md` was written; nothing was committed or pushed.*
