<!-- DRAFT 2026-11-03 by a chair helper (Opus 5.5, Claude Work), pending Round 3 and the ABL-START result. Items marked [R3] depend on Round 3. Not final. -->
# THEOREM_REVISION_INPUTS — MEET-v31 → the theorem meeting

**Draft for the chair of MEET-v31.** Written by the research sub-agent on 2026-11-03. Read-only: nothing in the repository was edited, committed or pushed, and no jobs, subagents or computations were run. The reader is the PI, through HQ. This file is the input to the **next** meeting, which decides the final theorem list.

**Status words** follow `theory_campaign/PROTOCOL.md`: PROVED, PROOF SKETCH, COUNTEREXAMPLE, CONJECTURE, OPEN. Registry words such as PROVED-LOCKED, PROVED-UNDER, XF VERIFIED and NONE are copied from their sources.
- Every PROVED here is a **candidate** (not reviewed, not adopted).
- No status is upgraded.
- "Seat-proved, unchecked" means a seat gave an argument and no proof check (PC1/PC2) has covered it yet.

**Sources and short names.**
- `TL` = `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md` @ fc712e7. `TL:n` is a line number.
- `INV` = `origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md` @ 440a38d. §1 is the component × property matrix: rows 1–14, columns **V** (validity), **A** (accuracy), **C** (cost), **F** (failure mode), plus a "Properties with NO theorem" column.
- `S1`, `S2` = `SYNTH_R1.md`, `SYNTH_R2.md`. `R2A`, `R2B`, `R2C` = the Round 2 seat files. `PC1`, `PC2` = `evidence/2026-11-03_PC1_proof_check.md` and `evidence/2026-11-03_PC2_certificate_card.md`. `AM01` = `evidence/AMEND_01_general_np.md`. All are under `theory_campaign/MEET-v31/` on `theory/MEET-v31` @ 29727bd. `file:n` is a line number.

**What is still pending when this was written** (S2 §4, STATUS.md):
- **Item 1, the block start:** waits on ABL-START, read against the fixed rule in S2 §2. §1.B below gives all three outcomes.
- **Round 3 (not yet held)** must still accept or amend: the certificate card per PC2, P-D6(i), P-D7 and the P-9 table.

Everything below that rests on those proposals is conditional on Round 3 accepting them, and is marked **[R3]**.

---

## 1. Method decisions that matter for theory

### 1.A Decided (closed in S1/S2), or proposed for Round 3

| # | Decision | What it means for theory | Source |
|---|---|---|---|
| M1 | **v3 is unchanged as a statistical method.** The target, prior, cap K, blocks, bridge, move round, calibration law and budgets all stay. Changing the counts, order or kernel of the move round is WORKHORSE. C8 (split N_e), C9 (shorter calibration) and C10 (particle-parallel kernel) are rejected. | Every v3 theorem stays about the shipped method. C10 is rejected partly because it breaks R5(b2), BG3 and V5. | dossier §2; S1 item 3; R1_B:64; R2C §4.1 row "Move round" |
| M2 | **LS0 is in the shipped core, run after the final local search.** It reads no uniforms. It gets its own provenance and an `ls0_improved` flag, and it must not fire E3. An LS0 stop means no complete output (OP-LS0). Correct wording: island outputs, Ẑ and PIPs are unchanged; the scored set is nested; the best score cannot fall; the top store is **𝒯_new = top_c(𝒯_old ∪ 𝒮_added), not a superset**; HPM unchanged in 2,394/2,394 fits. On truncation of the tie enumeration (cap 10⁶), use a deterministic tie-aware DP (e4). | Makes T38(b1)/(b1-LH) and LS-score theorems about the shipped method (TL:41, TL:686; INV row 11 "ID: LS0 is not in production"). | S1 item 2; S2 D3c (`SYNTH_R2.md:38`); R2B D3c; R2C D3c; R1_C item 8; S2 P-9 e4 |
| M3 | **HPM is the only decision rule.** An MPM is reported for each named PIP. There is no HPM-vs-MPM disagreement flag. `local_certified` is a 1-flip/swap local certificate only. | R2/R4/R5 stay the selection theorems. MPM results are descriptive. | S1 item 2 |
| M4 | **The Ẑ-weighted PIP is primary; equal-weight is the named secondary.** Both MPMs are reported, plus R_eff = (ΣW)²/ΣW² per fit. POST HOC, no re-run. | Objective-1 theorems (V3(ii), A1) are now about the **primary** quantity. A4 (equal-weight) is about a secondary one. | S2 D5 (`SYNTH_R2.md:43`); R2B D5 |
| M5 | **Parallel layer (a)–(h).** (a) Final islands as **process** workers, merged by Lemma S (Prop W). (b) Diagnostic islands run concurrently (W-cal); "bitwise" may not be claimed for (b) until W-cal is executed. (c) Parallel scans. (h) The block-table stage is the explicit parallel local step. "Bitwise" is scoped to one binary (`Makevars.v3`), single-thread BLAS and process workers. No change of floating-point summation order under a bitwise claim. Threads would need private counters merged deterministically (`cpp/v3_score.h:20–21, 231–236`). | V2 is restated with these scopes. The depth claims (D1) are about this execution level. | S1 item 3; S2 D3e, D3f; R2B D3f; R2C D3e |
| M6 | **GUARD under workers: "any worker stop ⇒ no output".** | Becomes premise (i) of every output-event statement (PC1 claim 2). | S1 item 3; R1/R2 all seats |
| M7 | **Stacking.** R′ = 4 by default; optionally R′ = 4k at **unchanged N_e**, declared before final randomness (before stream 10), on streams 10..9+R′. **N_e is never split.** The **extra local search from the R = 4 centre c₄ is kept.** Flags: a baseline record (islands 1–4, with the baseline HPM and search) and expanded flags over all R′ islands. | PC1 claim 6: with the extra search, the post-search scored set is nested and HPM(R′) ⪰ HPM(4); without it, monotonicity fails (COUNTEREXAMPLE). No listed theorem needs monotonicity; it matters only for nesting, "stacking never worsens Ŝ", or transferring R = 4 study measurements. | S1 item 3; S2 D3a, D3b, P-9 w7; PC1 claim 6 (`PC1:159–202`) |
| M8 | **Calibration is unchanged and gets a contract.** 𝓒 is frozen before final randomness; validity is conditional on any frozen 𝓒; Theorem G cap; ≤ ℓ rebuilds; restricted ESS on V only; statuses distinguished. Cost wording counts calibration: calibration/final work ≈ 0.05 + 0.2·I, with I the number of rebuilds. | Rebuild convergence, P(S₀ ∈ V) and P(schedule_limit) are **OPEN theorem obligations, not inherent** (all seats). | S1 item 4; S2 D4; R2A D4 (formula, seat-derived) |
| M9 **[R3]** | **General-h measured-round accumulator (P-D7).** 𝓗 is a list of bounded model-space functions declared from (X, y) before any randomness. H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi), with S_rqi taken after each complete measured round (`cpp/v3_engine.h:351–359`). Report μ̂(h) = Σ_r Ẑ_r H_r(h) / Σ_r Ẑ_r, plus the equal-weight version. Default 𝓗: the model-size distribution, pairwise inclusion on neighbour-graph edges (≤ 2pB pairs), and the terminal frequency of the returned HPM. Optional: archive the measured-round populations. Marginal RB-PIPs are never multiplied to estimate joint events. Continuous functionals need h̄(S) = E[h \| S, X, y]. ADDITIVE; joint summaries cannot be claimed for the 2,400 study fits. | Gives Theorem H (A1) a defined estimator. Its identity is the main new obligation (N1). | S2 P-D7 (`SYNTH_R2.md:69–74`); R2C D7; R2A D7; R2B D7 |
| M10 **[R3]** | **Certificate card, POST HOC: PC2's minimal card.** G1 (deterministic), G2 (one-sided, output-level), L1–L3 (local, subsets, best-of-scored), and R (optional box certificate with a declared region rule, node budget and τ). Until SC(η_F) is validated, every number carries the label "numerical implementation of an exact-arithmetic certificate", with η printed. A failed or unfinished certificate never changes the fit's status. Excluded: C2, C5, the "unscored mass" wording, and the B&B cost remark. `global_certified` is a labelled numerical flag. Z_𝒯 and MASKZPIP C1 (Ẑ < Z_𝒯 ⇒ Ẑ < Z) ship in any case. Flags E1–E3, ESS and grid flags stay as calibration triggers and labelled heuristics. The certificate must not feed back into calibration. | §2 (A2, A3) and §3 N7. | PC2 "Recommended minimal card" (`PC2:194–235`); S1 item 6; S2 D2 |
| M11 | **Output convention.** Guarantees are stated for the potential run and as **P{𝒪, ·}**, never P(· \| 𝒪). The allocation is reclassified as (c), a declared input that decides delivery only. Every estimate on 𝒪 is a function of (X, y, seed, binary). `fit$log_Z` = NA on stopped fits. | V4, R4, R5, N6 and the card. | dossier §2(g); S2 P-9 e8; R2A §4 "paper sentence"; R2C §4.4 |
| M12 **[R3]** | **Item-9 resolutions (P-9).** No setting is class (e) in the method's law. e1: B* = 16 re-labelled as a (c) table budget; W7-PART's g_max ≤ B < 2g_min is a **hypothesis of one theorem**, not a method parameter; the study's g = 5 is PART-pairing, a theorem obligation. e2: η-based near-tie list (POST HOC, heuristic label). e3: n = 2 extension. e4: LS0 tie DP. e5: `global_certified` labelled heuristic. e6/e7: engineering. e8: allocation as (c). Wording fixes w1–w7, including **r_n = √(2 log p / n)** (w1), "all p at n ≤ 5" (w2), the 1-NN fallback when p > e^{n/2} (w3), "no correlation cut" (w5) and the stream map 10..9+R′ (w7). No separate p ≪ n / p ≫ n rule. | §3 N8, N12; the hypotheses of S1/R5; IND-T must cover streams 10..9+R′. | S2 P-9 (`SYNTH_R2.md:76–103`) |
| M13 | **Declared v3.2 path.** C6: per-particle counter-based streams, LAW-PRESERVING. C7: Gram-free scorer, LAW-PRESERVING up to floating point. C6 is implemented and law-checked **iff** paper 1 claims particle-parallel depth. Island-parallel results may be reported at any p with their actual cost. "Free of N, H, R" is dropped for v3.1. C11 (clustering O(p²)–O(p³)), neighbour graph, grid bisection, convolution and pooling go into the cost account and the roadmap. | D1(c) and D3(b) must be restated (§2). | S2 D3d (`SYNTH_R2.md:39`), D3e |
| M14 | **Limitation wordings.** (ii) Literal "no run can upper-bound Z" is false; say "no *useful* upper bound from the run's record alone". (iii) "Markov is the only assumption-free probabilistic bound; max{Z_𝒯, 0.05Ẑ} keeps 95%". (iv) Masked weight variance: the mechanism is PROVED in kind, its severity on the production grid is OPEN (V11). (i) **[R3]** P-D6(i): access to all of X is inherent; a private 8p² Gram is not. | §4. | S2 D6 (`SYNTH_R2.md:44`), P-D6(i) (`:67`); PC1 claims 1–2 |

### 1.B Item 1 (block start): pending ABL-START. What each outcome changes

Rule, fixed before any result was read (S2 §2, `SYNTH_R2.md:48–63`). **v3.1 ships the block start under every outcome.** HPM counts are reported but do not decide.

| Outcome | Condition (S2 §2) | Theorem-list consequences |
|---|---|---|
| **1: keep, depth claim allowed** | Arm A has T ≤ min(T_B, T_C) and rebuilds ≤ min on ≥ 9/12 designs, and accuracy no worse than B or C by > σ_r on ≥ 9/12. | S1 and S2 stay as written. The paper may say the block start buys depth. **No theorem in TL compares A₀ or T across starts.** D2(c) gives T* = log₂A₀ + O(1) for *a* start, on the ideal two-state grid. Seats A and B computed that this law predicts only ≈ 1–1.2 stages saved (A₀ ≈ 36 vs ≈ 66–81 nats; `SYNTH_R1.md:17`), so any measured advantage must come from elsewhere (Seat B: the bulk spread of d(S)). So under Outcome 1 the depth claim is **empirical** (12 designs × 1 seed), or a **new obligation N18** (a depth comparison between starts) is opened, status OPEN, no route in the sources. D3(b) may cite the ablation, labelled empirical. |
| **2: keep, reframe** (also the result if inconclusive) | Accuracy no worse on ≥ 9/12, but Outcome 1's depth condition fails. | S1 and S2 are kept, framed as "the exactly computable, theorem-bearing local step (S1/S2) plus the parallel table stage (h)". There is **no depth or speed claim for the start.** D2(c) and D3(b) keep A₀ as a property of the shipped start, but the wording must not suggest the block start reduces depth versus a plain start. C1(e), "our blocks are used only for the start", stands. No new obligation. |
| **3: real issue flagged; block start still ships in paper 1** | B or C beats A on accuracy by > σ_r on ≥ 9/12 designs, including both S4 and both S5 designs, and is not worse on depth on any S4/S5 design. | Paper 1: as Outcome 2, plus the ablation is reported as a disclosed weakness, and a ≤ 20-seed paired check runs on the two worst designs. If that check confirms, a start change goes to Felipe as a **WORKHORSE v2 candidate.** Then the v2 list must re-prove, for the new start, everything that uses π₀: S1(a)–(d), S2, D2(c)'s A₀, C1(d), and above all **R5(b1)/(b1-LH)**, whose (M1) needs P₀(π₀(S°) > ½) → 1 for the *block* start, with LS0 centred on the start mode. My reading, not a source statement: DIL-E is stated "for any data and partition" (TL:432–433), so S1(a),(d) may cover arm B as the B = 1 partition; arm C (capped prior, no tables) is not a block product with tables. Paper-1 theorems are unchanged. |

---

## 2. Per item of THEOREM_LIST.md (in order)

"Current" is copied from TL. Actions: keep / restate / drop / split / merge / new hypothesis.

### G1. Validity under parallel execution

| ID | Current status / tier (TL) | What the decisions change | Action | Source |
|---|---|---|---|---|
| **V1** Thm V | (a),(b) T12, T31(i) PROVED-LOCKED; (c) ADRAFT-ThmA PROVED (Astra only), Prop P(ii) PROVED (candidate); (d) Prop 2(c) PROVED-LOCKED / Prop P(iv) PROVED (candidate); V5 "no registry row". v1, cited lemma + Prop. (TL:21, 55–94) | (1) "R declared" becomes "R′ = 4k, the stacking schedule, N_e and 𝓒 declared before stream 10; streams 10..9+R′". EX-S/IND-T must be stated for the extended stream map (M7, w7). (2) **V1(a) is stated for a general bounded h with the measured-round estimate ĥ_r, but the locked identity covers Ẑ and the RB-PIP** (INV row 8: "islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j"). For a general h at the P-D7 accumulation point, the identity is still a PROOF SKETCH (R2C D7; PC1 claim 3, "still a premise"; TL A1(iii) calls it the "crux not verified"). (3) (b) in output-event form: P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜), with max{Z_𝒯, 0.05Ẑ} giving the same event (PC1 claim 2). (4) Add hypotheses GUARD-W ("any worker stop ⇒ no output") and process workers (M5, M6). (5) (c) is now the consistency of the **primary** estimator (M4). | **Split** (a) into (a1) Ẑ and RB-PIP (locked) and (a2) general bounded h (PROOF SKETCH, = N1). **New hypotheses** (stream map, GUARD-W). **Restate** (b) in output-event form. V5 becomes obligation N9. | S2 P-9 w7; PC1 `:41–76`, `:98`; R2C D7 |
| **V2** Prop W / W-cal / Lemma S / Cor W-R | Lemma S PROVED; Prop W PROVED (code reading), executed on "1/1 design + smoke"; W-cal PROVED (code reading only), not executed. v1, supplement. (TL:22, 96–121) | (1) Executed evidence is now **smoke + 3/3 study designs** (`SYNTH_R1.md:7`). The 1.9× is a 2-core number; **no 4-core speed-up may be printed** (R2A §2). (2) Bitwise scope: one binary, single-thread BLAS, process workers (M5). (3) W-cal must be executed before "bitwise" is claimed for (b). (4) LS0: "island outputs bitwise", **not** "stores nested". 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) (R2C D3c; seat-proved from `cpp/v3_ledger.h:41` and Lemma S, unchecked). LS0 must not fire E3. (5) Cor W-R as written is **PROVED** (PC1 claim 6), with one amendment: E3 and `local_certified` on islands 1–4 match only when evaluated on the search from c₄. Add **Cor W-R(b)**: with the extra search from c₄, the post-search scored set is nested and HPM(R′) ⪰ HPM(4) (PROVED, PC1). Without it, this is FALSE (COUNTEREXAMPLE `c6_ls.py`). | **Restate** (status line, scopes, LS0 wording); **add** Cor W-R(b). Prop W stays a code-audit fact (TL:119), not a theorem. | `SYNTH_R1.md:7`; S2 D3a–D3c, D3f; PC1 `:159–202` |
| **V3** Prop P | PROVED (candidate, elementary). v1. (TL:23, 123–149) | (1) (ii) is now about the **primary** PIP. (2) Add **PC1 claim 3** next to (iii): P(\|μ̂ − μ\| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, PROVED, needs W_r ≥ 0 stated, and takes E[W_r H_r] = μ as a premise. (3) (v) "R declared" covers R′ = 4k. (4) Caveat unchanged: E[W²\|𝓒] may be exponential; V11 OPEN. (5) The R = 32 × 312 concurrency runs are **population-splitting** experiments, not stacking at N_e. They must not be cited as validating M7 (R2C §2). | **Keep**; **restate** "secondary" → "primary"; **add** PC1 claim 3 as (iii′); merge (iii) into A1 as TL already plans. | S2 D5; PC1 `:79–100`; R2C `:236` |
| **V4** Lemma RO + GUARD + CEX-guard | Lemma RO PROVED, XF VERIFIED (A-REV6); GUARD fact HOLDS (literal ERROR); CEX-guard COUNTEREXAMPLE. v1, supplement. (TL:24, 151–168) | (1) GUARD-W ("any worker stop ⇒ no output") is a **new implementation premise** for v3.1 (M6). (2) OP-LS0: an LS0 stop counts as no output (M2). (3) Allocation as (c) (e8): Lemma RO is what makes "estimates are a function of (X, y, seed, binary)" true. (4) `fit$log_Z` = NA (M11). (5) **Conflict:** TL says Lemma RO is XF VERIFIED, while PC1 claim 2 and PC2 (`PC2:64`, `:152`) call "Lemma RO / GUARD" an **unreviewed (W2-BOOK) premise**. My reading: the implication is verified; GUARD as an implementation fact for the v3.1 worker and LS0 code is not. | **Split** into Lemma RO (keep, verified) and GUARD-W (new code-audit fact for workers and LS0). Then main-text use as premise (i) of N6/N7. | S1 item 3; PC1 `:63–69`; PC2 `:64` |

### G2. Posterior accuracy

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **A1** Thm H (NEW-SYNTH) | PROOF SKETCH; NEW-COMP; v1. (TL:25, 174–218) | (1) **The estimator is now defined by the spec** (P-D7; M9 [R3]): plain averages after complete measured rounds, Ẑ-weighted primary. (2) TL A1(i) allows "the Rao–Blackwellised version when h is a product of inclusion indicators", but **no such estimator is in P-D7**, which says "marginal RB-PIPs are not multiplied". So joint h is restricted to plain averages (c_h = 0), and RB applies to marginal PIPs only. (3) h must be in the declared 𝓗, fixed from (X, y) before any randomness. P-D7's default item "terminal frequency of the returned HPM" uses a **run-dependent** h = 1{S = Ŝ}, which (a)/(b) as stated do not cover (§5 conflicts). (4) Add the PC1 claim 3 Chebyshev bound (Monte Carlo error \|μ̂ − π(h)\|) alongside the Maurer/Hoeffding (b) (distance to h(S₀)). (5) A bound simultaneous over q_n summaries needs a multiplicity argument (R2C D7). (6) Continuous functionals need h̄ (P-D7). (7) Joint summaries cannot be claimed for the 2,400 fits. (8) Crux = **N1**. | **Restate** around the P-D7 estimator; **new hypothesis** "h ∈ 𝓗 declared before randomness"; keep v1 with N1 as the first obligation. If N1 fails, A1 shrinks to marginal PIPs, which rest on the locked Prop 2 identity. | S2 P-D7; R2C D7 (`R2_C.md:179–218`); PC1 claim 3 |
| **A2** Thm Z | (i) T12/T31(i) PROVED-LOCKED; (ii) O-PW2 Thm A PROVED, XF VERIFIED; (iii) E1/E2 PROVED (candidate); (iv) MASKZPIP C1 PROVED; (v) T26-ThmA PROVED, XF VERIFIED*. Two-sided masked: v2. (TL:26, 220–255) | (1) **PC1 claim 4:** the table row (TL:26) and the "Plainly" sentence (TL:236), "errs/can only fail downward", are **literally false** (COUNTEREXAMPLE; formal (iii) is not refuted). Use PC1's corrected wording (`PC1:124–126`): "underestimates with high probability; rare compensating overestimates of the same total mean; Markov caps them; Ẑ < Z_𝒯 detects underestimation only". (2) Add **PC1 claim 1** as a remark: Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}, PROVED, for any y, ≈ 530 nats loose at n = 200. Equivalently, a deterministic lower bound on π(Ŝ) (PC2 C1(c) note). (3) Add the max{Z_𝒯, 0.05Ẑ} coverage to (i), in output-event form (PC1 claim 2). (4) (iv) ships as card G1 (PC2 C1(a) amended). (5) Severity of masked variance stays OPEN (V11; M14(iv)). | **Restate** (wording, mandatory); **add** two PROVED clauses. Tiers unchanged. | PC1 claims 1, 2, 4; PC2 C1(a), C1(c) |
| **A3** Thm Z𝒯 | MASKZPIP P3 PROVED (candidate, deterministic). v1. (TL:27, 257–271) | (1) **PC1 claim 5 (amended, PROVED):** if S₀ ∈ 𝒯, then PIP^𝒯_j ≥ 1 − δ₁ on S₀ and ≤ δ₁ off it, so **δ₁ < ½ ⇒ MPM^𝒯 = S₀**, and ½ is sharp. Seat B's "needs δ₁ < ⅓" is FALSE. (2) **Retention:** under δ₁ < ½, S₀ ∈ 𝒮 ⇔ S₀ ∈ 𝒯 (PC1 `:155`; R2C D7 `:216`). This needs 𝒯 = top_{40p+1}(𝒮), which holds by Lemma S plus the final run re-offering calibration's stores (`v3_core.cpp:409–419`, PC2 code facts). It answers Seat C's "discovery ≠ retention" on the event {δ₁ < ½}; **unqualified** finite-sample retention remains false. (3) Under LS0, 𝒯 = top_c of the realised 𝒮 still holds (M2). (4) PIP^𝒯 is labelled "restricted" (R2C §4.1). (5) Floating point: labelled numerical until SC is validated. | **Restate:** add the MPM^𝒯 clause and a retention lemma (N13). Compose with R5 through retention on {δ₁ < ½}. | PC1 `:130–155`; PC2 `:22–25` |
| **A4** Thm PIP (equal-weight) | P1 PROVED; P2 PROVED (composition, LH fixed p); Thm R PROVED as composition, CONDITIONAL on DELIV-POP (OPEN). P1 v1, Thm R v2. (TL:28, 273–292) | The equal-weight PIP is now the **named secondary** (M4). A4 explains why it does not improve with R (V3(i)). Statuses unchanged. | **Keep;** move to the supplement (recommendation). Thm R stays v2. | S2 D5 |

### G3. Parallel work and depth

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **D1** Thm D | Prop D PROVED (counting); T32(i) PROVED, rate GAP. v1. (TL:29, 298–333) | (1) **D3d closed:** v3.1 is island-parallel. The v3.1 statement is D1(b): depth N_e(T+L+4)(p+B+2) plus setup, calibration, grid and population reductions. **"Free of N, H and R" (TL:29, 309) belongs to v3.2 only (C6).** The summary-table formula "(I+2)(T+L+4)(p+B+2) … free of N, H, R" (TL:29) is the particle-parallel one and must not headline v3.1. (2) Add explicit terms: (h) block tables (parallel), the LS0 term, the extra search from c₄ (≤ ℓ+1 scans), and R′ = 4k width. (3) Calibration on the critical path. Seat A's count gives calibration/final ≈ 0.05 + 0.2·I (predicted 0.46/0.67/1.69 vs observed 0.45/0.62/1.76; R2A D4; seat-derived, not proof-checked). Seat B's depth after (b) is (1+I_e)·H₀ (R2B D4). (4) No 4-core speed-up may be printed (1.9× on 2 cores). (5) Superiority over sequential MCMC is an **empirical** claim that needs a stated comparator (R2C D3d). | **Restate:** (b) is the v3.1 theorem, with the calibration, LS0 and stacking terms; (c) is a v3.2 remark, claimed only if C6 is implemented and law-checked; fix the TL:29 summary. | S2 D3d, D3e, D4; R2A D4; R2B D4; R2C D3d |
| **D2** Thm STG | Theorem G PROVED; STG-F PROVED; STG-M PROVED (ideal two-state grid), XF VERIFIED*; families PROOF SKETCH; as-coded masked T_n Conjecture P OPEN. v1 ideal grid + T_e cap; as-coded v2. (TL:30, 335–370) | (1) Calibration contract (M8): Theorem G's T ≤ T_e is the as-coded guarantee; Conjecture P is part of the P(schedule_limit) obligation (N5). (2) "Ideal two-state stage laws are not laws for the realised candidate-grid rebuild process" (R1_C §7 "Fourth"). TL already says "ideal grid"; keep that discipline in the text. (3) What may be said of A₀ *for the block start versus others* depends on item 1 (§1.B). | **Keep;** wording; tie Conjecture P to N5. | S1 item 4; R1_C:235–241 |
| **D3** Thm CD | Assembly; weakest links A1, C1 (PROOF SKETCH) and as-coded T_n (OPEN). v1 in the REPORT §3 scope. (TL:31, 372–398) | (1) (b) "critical path … free of N, H, R (D1(c))" (TL:378) must change to the island-level depth (M13). (2) (b) "costs depth through A₀" is outcome-dependent (§1.B). (3) (a) uses A1(a) with the P-D7 estimator. (4) (c) adds PC1 claim 3 and the stacking-at-N_e design (M7). (5) (d) uses R5(b1-LH) for the **shipped** method (M2). | **Restate** (b) and (d); conditional on item 1. | S2 D3d; §1.B |
| **D4** Cor V | PROOF SKETCH. v2. (TL:32, 400–415) | "Never split N_e" (C8 rejected) and stacking at fixed N_e are now the shipped design; Cor V is their motivation. The R = 32 × 312 runs are splitting experiments: empirical evidence bearing on Cor V's first-order neutrality, not on stacking. | **Keep v2;** v1 states Prop P(i)/(ii) plus the decision. | S1 item 3; R2C §2 |

### G4. Why the bridge

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **S1** Thm 2 (start) | T22(i)(ii)(iv) PROVED-LOCKED; T22(iii) PROVED-LOCKED CONDITIONAL; T27(i) PROVED-LOCKED CONDITIONAL, Thm3/4-EXP XF VERIFIED; DIL-E/E1/R/N PROVED, XF VERIFIED. v1. (TL:33, 423–455) | Outcome-dependent framing (§1.B); content unchanged under all three outcomes for paper 1. e1: B* = 16 is a (c) budget, and W7-PART's g_max ≤ B < 2g_min is a theorem hypothesis (covers g ∈ 8..14 at B = 14 and 9..16 at B = 16). The study's g = 5 is outside it (N8). | **Keep;** framing per outcome; state the SIZE hypothesis where W7-PART is used. | S2 §2, P-9 e1 |
| **S2** Thm SEP + Lemma KL | SEP-A/B PROVED, XF VERIFIED; Lemma KL PROOF SKETCH (NEW-SYNTH); (d) PROVED (candidate). v1. (TL:34, 457–492) | Independent of the outcome: it is about π₀ as a one-shot proposal. SEP-B is the cited mechanism for M14(iv), "masked variance PROVED in kind". (d)'s wording discipline ("moving off the start is needed", not "tempering is needed") matches M2 and R1_C §7. | **Keep.** Lemma KL is two lines; add it to the next proof-check batch. | S2 D6; R1_C:241 |
| **S3** Prop M | Dropped. (TL:35, 494–499) | No change. | **Keep dropped.** | — |
| **S4** Weight stability | Supplement remark; v2. (TL:501–509) | Seat C: §5.3 needs a theorem for the **actual** block product, including common noise integration. That is an **OPEN theorem obligation, not an inherent limitation** (R2C §3 row 5). | **Keep v2;** list as OPEN, never as a limitation. | R2C `:259` |

### G5. Correlation robustness vs split-and-merge

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **C1** Thm SL (NEW-SYNTH) | COUNTEREXAMPLE (numerical) + PROOF SKETCH. v1 on exact-Gram LH; LH-iid v2. (TL:36, 515–581) | (1) (d) is now about the shipped method (LS0 in the core): R5(b1-LH) applies directly. (2) (d)'s "joint inclusions satisfy A1" only holds through the P-D7 accumulator, for declared pairs, and is conditional on N1. (3) **Name clash:** "C1" also names MASKZPIP C1 (TL A2(iv)) and O-CERT C1 (PC2). Rename for the paper. | **Keep;** **restate** (d). | M2, M9 |

### G6. Selection accuracy

| ID | Current | What the decisions change | Action | Source |
|---|---|---|---|---|
| **R1** Thm 1 (T03♯) | T01–T03 PROVED-LOCKED; T03♯ PROVED, SF + XF VERIFIED. v1 (asymptotic; disclose n ≳ 2·10⁶). (TL:37, 587–604) | Scope sentence (P-9 theory scope): p ≤ n^A comes from the **target theory** (Felipe's prior and the proof technique), not from a sampler choice. Song–Liang's e^{Cn^α} cannot be imported; whether our prior admits it is **OPEN, not impossible**. | **Keep;** add the scope sentence (N12). | `SYNTH_R2.md:98–103`; R2A §4; R2C §4.5 |
| **R2** Prop 1 (Bayes rules) | PROVED-LOCKED; XF VERIFIED*. v1 remark. (TL:38, 606–613) | No change; it is about the true posterior. PC1 claim 5(a), "Ŝ = S₀ if S₀ ∈ 𝒮 and δ₁ < ½, sharp", is about the reported HPM and belongs in R4. | **Keep.** | PC1 `:132–138` |
| **R3** Thm 3 (Theorem A, LS-score) | Theorem A PROVED, XF VERIFIED*, Lean sorry-free; LS-score PROVED, XF VERIFIED (A-REV8); Lemma M PROVED, XF VERIFIED. v1. (TL:39, 615–634) | LS0 is shipped (M2), so LS-score is about the shipped method. **New hypotheses:** (1) the LS0 centre is the prescribed smallest-size lexicographic start mode, with the tie-aware DP on truncation (e4; DP invariant OPEN, R2C E2); (2) ℓ ≥ max{Φ(S°) − 1, 0} (N11); (3) completed scans / OP-LS0. | **Keep;** **new hypotheses** (1)–(3). | S2 P-9 e4; R2B row 7 |
| **R4** Thm 4 (T21(C1), T38(0), N200, RO) | T21(C1) PROVED-LOCKED; T38(0) PROVED, XF VERIFIED; N200 PROVED (author only); Π(X) upper bound OPEN. v1. (TL:40, 636–656) | (1) Already in output-event form; keep it so (M11). (2) **Add PC1 claim 5(a)** (PROVED, sharp). (3) Per-run bounds hold for any R′ declared before final randomness (PC1 claim 6 table). The **study measurement "0/2,394 S₀ ∉ 𝒮" transfers to R′ > 4 fits only because the extra search from c₄ is kept** (PC1 `:197–201`, item (iii)). (4) Lemma RO under GUARD-W (V4 split). (5) "Posterior misses at n = 200" are facts about those data and the fixed target, not a universal rate (R2C §3). | **Keep;** add clause (2) and the transfer caveat. | PC1 claims 5, 6 |
| **R5** Thm 5 (T38) | (0) PROVED, XF VERIFIED; (a) PROVED-UNDER (F); (b1) PROVED-UNDER (M1)–(M3), XF VERIFIED; (b1-LH) PROVED (candidate), XF VERIFIED; (b2-LH) PROVED-UNDER STAB-LH; (b1-LH-iid) XF GAP; (c) PROVED-UNDER T32(i). v1: (0),(a),(b1-LH),(b2-LH),(c). (TL:41, 658–692) | (1) M2 answers TL:686's "decision needed" in favour of **headline (b1-LH) for v3.1**, with (b2-LH) as the no-LS0 corollary for "v3 as run". (b1-LH) is a theorem about the shipped method only once the integrated core matches the export (N2(c)) and OP-LS0 and e4 hold (N3). (2) Routes carry to any R′ by scored-set nesting (PC1 claim 6 table). (3) (c) cost: add the LS0 term (already there) and the extra search from c₄. (4) Per-regime scope: exact-Gram LH needs p ≤ n − 1 and g_max ≤ B < 2g_min; LH-iid is XF GAP; the study generator (g = 5, 2g ≤ B, p ≫ n) is N8 OPEN. (5) Under Outcome 3 → v2, (M1) must be re-proved for any new start (§1.B). | **Restate** the headline; **new hypotheses** OP-LS0, e4 tie rule, SIZE. | S1 item 7; TL:686; PC1 `:181–193` |
| **R6** Delivery P(U) → 0 | NONE; "limitation in v1 … v3.1 lowers wall-time stops, Prop W, ≈ 4× headroom". (TL:42, 694–700) | (1) **P(U) → 0 is an OPEN theorem obligation, not an inherent limitation** (S1 item 4: rebuild convergence and P(schedule_limit) "OPEN, not inherent"; R2B §3(ii)). Only "a fixed allocation cannot support unrestricted growth" is by definition (V13). (2) **"≈ 4× headroom" is not measured.** The executed speed-up is 1.9× with 2 cores, and no 4-core figure may be printed (`SYNTH_R1.md:7`; R2A §2). (3) Replaying the 6 stopped fits is an optional operational step (D8), labelled as such, and cannot establish a delivery theorem. (4) Allocation as (c) (e8). | **Restate:** "OPEN (delivery)". Report 6/2,400 with the allocation. **Remove the 4× sentence.** | S2 D8, P-9 e8 |
| **R7** Π(X) upper bound | OPEN. v2. (TL:43, 702–708) | No change. | **Keep v2.** | — |
| Cited lemmas (TL:45–49) | — | No change from this meeting. INV D9's citation clashes still need a primary-source check before printing. | **Keep.** | INV §2 D9 |

---

## 3. New theorem obligations created by the decisions

Each entry gives: statement; hypotheses; status; the decision it supports; what happens if it fails; and its INV §1 cell(s), as row # (component) × column.

**N1. Measured-round island identity for general bounded h (Theorem H crux).**
- *Statement.* Conditional on a successful frozen 𝓒, for each final island r and each h ∈ 𝓗 with 0 ≤ h ≤ 1, declared from (X, y) before any randomness: E[Ẑ_r · H_r(h) | 𝓒] = Z·π(h). Here H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi), with S_rqi the particle after complete measured round q (`cpp/v3_engine.h:351–359`).
- *Hypotheses.* EX-A, EX-S, CAL, V5 (each φ = 1 round is π-invariant), multinomial resampling, R′ declared.
- *Route* (R2C `:200–204`): the finite-state resample–move recursion gives E[Ẑ_r η_{r,T}(f)] = Zπ(f); terminal rounds preserve π, so the identity holds at each measured endpoint and for their average.
- *Status:* **PROOF SKETCH** (R2C D7). PC1 claim 3 treats it as a premise.
- *Supports:* M9 (accumulator), A1, C1(d) joint clause, D3(a) for general h.
- *If it fails:* μ̂(h) is reported as a descriptive summary with no theorem. A1 shrinks to marginal PIPs (locked Prop 2 identity). M4 survives, because it rests on Prop P(ii) for PIPs (R2A §3). Proposal §13.1 stays LACK (INV §3a).
- *Cell:* row 8 × V (islandwise identity, extended); row 10 × "NONE: joint inclusion probabilities".

**N2. Prop W, W-cal, LS0 and stacking in the integrated v3.1 core.** A code-audit fact plus an executed replay, not a mathematical theorem (TL:119).
- *Statement.* For fixed (X, y, seed, binary), with process workers and Lemma S merges:
  - (a) final islands are bitwise equal to the serial run (Prop W);
  - (b) the 4 diagnostic islands, with persistent per-worker stream state, are bitwise equal to serial (W-cal);
  - (c) LS0, appended after the final local search, leaves island outputs, Ẑ and PIPs bitwise unchanged, gives 𝒯_new = top_c(𝒯_old ∪ 𝒮_added), and does not fire E3;
  - (d) R′ = 4k with the extra search from c₄ leaves islands 1–4 bitwise unchanged and nests the post-search scored set.
- *Status.* Lemma S PROVED. (a) PROVED by code reading and executed on smoke + 3/3 designs. (b) PROVED by code reading, **not executed**. (c) not in the production core. (d) PROVED (PC1 claim 6, deterministic).
- *Supports:* M2, M5, M7, and "the 2,394 study fits are v3.1 fits".
- *If it fails:* (b) drops to LAW-PRESERVING and the wall-clock claim is capped at the D4 table (R2B §5 item 4). V1 still holds at the level of the law, but "the study validates the shipped method bitwise" must be narrowed.
- *Cell:* row 8 × V; row 7 × V; row 12 × "NONE: LS0 absent from production"; row 14 × V.

**N3. LS0-based T38(b1-LH) about the shipped method.**
- *Statement.* For v3.1 with LS0 after the final local search, on LH exact Gram (p ≤ n − 1, c linked pairs, g_max ≤ B < 2g_min): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, with no open statistical hypothesis.
- *Hypotheses.* EX-A, EX-S, CAL, SR, GUARD + GUARD-W, (P), (M1)–(M3) (verified on LH), **OP-LS0** (LS0 completion counted in 𝒪), the **LS0 centre rule** (e4: prescribed smallest-size lexicographic start mode, tie-aware DP on truncation), and **ℓ ≥ max{Φ(S°) − 1, 0}** (N11).
- *Status.* (b1-LH) PROVED (candidate), XF VERIFIED (A-REV8), as a theorem about "v3 + LS0". The bridge to the code is N2(c) (not yet done). The e4 DP invariant is **OPEN** (R2C E2: "prove the score/order dynamic-programming invariant"). In the study, 0/2,400 starts were truncated and all 2,400 had exactly one tie.
- *Supports:* M2.
- *If it fails* (implementation mismatch): the headline falls back to (b2-LH) on the STAB-LH subfamily without LS0. M2 survives (ADDITIVE; HPM unchanged in 2,394/2,394) but loses its theorem motivation.
- *Cell:* row 11 × A; row 12 × V/A.

**N4. Ẑ-weighted PIP and μ̂(h) finite-R accuracy, and the constant M under masking (V11).**
- *Statements.*
  - (i) PC1 claim 3: P(|μ̂ − μ| > ε) ≤ min{1, 4(M−1)/R + 4M/(Rε²)}, with M = E[(Ẑ_r/Z)² | 𝓒]. **PROVED**, given N1 for general h, or the locked identity for PIPs.
  - (ii) Prop P(iii) with M1 (PROVED, candidate): regime-free distance to 1{j ∈ S₀}.
  - (iii) **Obligation:** an upper bound on M on the production (resolved) grid through a masked crossing. This is V11, "resolved grid ⇒ O_P(√(T/N))": CONJECTURE, OPEN for c ≥ 2. Known lower bound: M ≳ 1/P_𝓒(cross), PROOF SKETCH (TL A1(v)); do not cite F-MASKPIP M3, which is XF ERROR.
- *Supports:* M4, and M7's R′ guidance and R_eff reporting.
- *If (iii) fails* (M exponentially large): M4 survives, because R-consistency holds anyway and equal-weight has none. But the paper may claim correctness, not efficiency, and must disclose that the R needed may be huge. R_eff per fit makes this visible (R2B D5).
- *Cells:* row 10 × A; row 9 × "NONE: two-sided relative accuracy of Ẑ in the masked regime"; row 8 × "NONE: island variance vs correlation"; row 7 × A (V11).

**N5. Calibration contract.**
- *(a) Validity for any frozen 𝓒.*
  - Statement: every final-run identity (V1, N1, N6) holds conditional on any successful 𝓒 built on streams 0–9, with final streams ≥ 10 independent of it.
  - Status: assembly of T12/T31(i) (PROVED-LOCKED, conditional on 𝓒), IND-T (PROVED, XF VERIFIED*, A-REV1 only) and Lemma RO. The extension of IND-T to streams 10..9+R′ is a code-audit item.
  - Supports M8 directly.
- *(b) OPEN obligations*, all NONE in INV row 7 and §5 item 9:
  - (b1) rebuild-loop convergence (grid equality within ≤ ℓ rebuilds);
  - (b2) P(S₀ ∈ V) and "V contains the competing pair";
  - (b3) P(schedule_limit), P(grid_unconverged) → 0, including the as-coded masked T_n (Conjecture P, OPEN).
- *If any of (b) fails:* M8 **survives**, because validity is conditional on any frozen 𝓒 (R2A §3, T12/Prop 2). Failure affects only delivery probability and efficiency. The paper states each as OPEN, next to the POST HOC tabulation of rebuilds, tier, T and convergence (S1 item 4), and the cost formula 0.05 + 0.2·I.
- *Cells:* row 7 × V (a); row 7 × "NONE" (b1–b3, stay empty); row 14 × "NONE: P(schedule_limit)"; row 5 × "NONE: realised T_n".

**N6. Output-event coverage statements.**
- *Statements.*
  - (a) P(𝒪 ∩ {max(Z_𝒯, 0.05Ẑ) > Z}) ≤ 0.05·P(SMC ∩ 𝒜) ≤ 0.05. The two events {L > Z} and {0.05Ẑ > Z} are equal.
  - (b) Card level: P(𝒪 ∩ {some G2, L or R item false}) ≤ 0.05·P(SMC ∩ 𝒜).
  - (c) Every consistency result is stated jointly with 𝒪, never conditional on it. The paper sentence reads "the probability that a run returns a card with a false claim is at most 5%".
- *Hypotheses:* PC1 claim 2 (i)–(iv):
  - (i) Lemma RO + GUARD-W;
  - (ii) a successful 𝓒 with E[Ẑ̄ | 𝓒] ≤ Z;
  - (iii) CAL, EX-S;
  - (iv) Ẑ = Z on the exact branch;
  - plus EX-A and distinct store entries.
- *Status:* (a) **PROVED** (potential run; output form CORRECT WITH AMENDMENT, PC1 claim 2). (b) **PROVED modulo premise (i)**, which PC2 lists as unreviewed (PC2 C6 item 3).
- *Supports:* M11, M10.
- *If premise (i) fails* for the worker code: the CEX-guard mechanism applies and the output-event statements fail for v3.1. The fix is engineering (GUARD-W); the decision survives.
- *Cells:* row 9 × V; row 14 × V.

**N7. Certificate card G1/G2/L/R (PC2 verdicts).**
- *Status by item:*
  - **G1** (C1(a) amended, excluding Ŝ): PROVED, deterministic, EX-A.
  - **G2** (C1(b) set identity and bound): PROVED, output event, joint.
  - **L1** (C3(a), with empty maxima = +∞ and an fp margin of 2η_F): CORRECT WITH AMENDMENT.
  - **L2** (C3(b)): PROVED.
  - **L3** (C3(c), realised 𝒮 not 𝒮̄, |𝒯| ≥ 2): CORRECT WITH AMENDMENT; the amended form is PROVED.
  - **R** (C4 with Lemma M): PROVED with amendments (drop |L| > K leaves; S ⊆ U with |S| ≤ K; SC must cover Φ and M). C4(b) is PROVED as written: isolating {Ŝ} matters for sharpness, not truth.
  - Card bound (C6): CORRECT WITH AMENDMENT, PROVED modulo premise (i).
  - C6′: PROVED.
- *FALSE, or not a theorem:*
  - C1(a) third clause as written;
  - C1(b) "unscored mass" (COUNTEREXAMPLE `t4b`);
  - the conditional reading of the C6 paper sentence;
  - "SC checkable by replay";
  - any rigorous reading of `global_certified` (heuristic: η rests on a *lower* estimate of the condition number);
  - the C4 cost remark (empirical only).
- *Excluded from the output:* C2 (conditional on PW2), C5 (needs S₀; CORRECT WITH AMENDMENT as a study-level item).
- *Open sub-obligation:* SC(η_F) by validated arithmetic, and VAL-FP(η, ε) at production size. Both are unmeasured, so the floating-point card stays labelled numerical (see N16).
- *Supports:* M10.
- *If SC is never validated:* the card stays "numerical implementation of an exact-arithmetic certificate". The decision survives (POST HOC).
- *Cells:* row 13 × F (positive per-fit certificates; **not** a flag power result, so row 13 "NONE: positive power" stays empty); row 9 × F (C1); row 12 × "NONE: meaning of `local_certified`" (L1's exact gaps fill it in the deterministic sense); row 11 × F.

**N8. PART-pairing for the study generator g = 5 (2g ≤ B).**
- *Statement (as far as the sources go):* a partition law for complete linkage + size cut + next-fit packing when equal groups satisfy 2g ≤ B (study: g = 5, B = 14). Which groups are co-blocked, and does co-blocking remove the masking (Prop Q)?
- *Status:* **OPEN**; Prop Q **PROOF SKETCH** (R2B row 6′); W7-PART CE2 COUNTEREXAMPLE (unequal groups are not merged).
- *Supports:* M12 e1 (B* = 16 stays a budget; W7-PART's condition is a hypothesis, not a method parameter).
- *If it fails:* e1 survives. Changing B or the cut for group recovery would be WORKHORSE (R2C §4.3). The paper discloses that the study generator is outside every selection theorem.
- *Cells:* row 3 × "NONE: partition law for the study's packing"; row 11 × "NONE: study generator".

**N9. V5: kernel reversibility, self-adjointness, and exactness of the start sampler.**
- *Statement:* each elementary move (Gibbs flip, uniform swap, neighbour swap, independence move with a π₀ proposal) is γ_φ-reversible; a uniformly random order of reversible kernels is self-adjoint; the start sampler draws exactly from π₀ with exact Z̄₀.
- *Status:* by construction and consultant-checked, but **no registry row** (INV §5 item 12; TL:77). One-page route (TL V1(v)).
- *Supports:* M1, V1's hypothesis, N1, and the rejection of C10.
- *If it fails* (not expected): V1 fails and the method question reopens.
- *Cells:* row 6 × V; row 4 × V.

**N10. V10: L versus t_mix.**
- *Statement:* do L = max(4, ⌈log₂(n+1)⌉) terminal φ = 1 rounds give measured-round populations close to π (mixing or spectral gap of the φ = 1 round)?
- *Status:* **NONE / OPEN** (INV row 6). The YWJ/ZYVR route is blocked as stated (INV §2 D1).
- *Note:* validity (V1, N1) holds exactly at any L; L affects accuracy and variance (A4-P2's (L+4)ρ̄; DELIV).
- *Supports:* M1 and item 9's classification of L as (b)+(c).
- *If it fails:* no decision changes. Theorems needing mixing carry L as a hypothesis and the gap is disclosed.
- *Cell:* row 6 × "NONE: mixing / spectral gap (V10)".

**N11. ℓ versus the moves needed.**
- *Statement:* ℓ = ⌈log₂(n+p+1)⌉ is at least the number of moves LS0 needs (max{Φ(S°) − 1, 0}, LS-score), and the cap on the final local search and on rebuilds is not binding w.p. → 1.
- *Status:* on LH with c ≤ s₀ fixed, "eventually true" (R2B row 7; elementary, unchecked). For growing s₀: **OPEN**. R2B §3 lists "ℓ versus the moves BASIN needs", but **BASIN is not defined in any file read**.
- *Supports:* M2 and item 9's classification of ℓ.
- *If it fails:* R3/R5 carry ℓ as a hypothesis; ℓ stays. A growing-support theorem would need a bigger budget, which is a method-induced restriction (`SYNTH_R2.md:102`).
- *Cells:* row 12 × C/A; row 7 × C (rebuild cap).

**N12. General (n, p) scope, per regime** (S2 P-9 theory scope; R2A §4; R2B §4; R2C §4.5).

| Regime | What theory may claim | Cause of any restriction |
|---|---|---|
| Tiny n | No asymptotic claim. Exact target quantities on the exact branch: n ≤ 5 is exact for **all p** (chair-checked, `SYNTH_R2.md:26`). The n = 2 extension (e3) is a PROOF SKETCH (R2C E1). | None from the method; the data carry little information. |
| Fixed p, n → ∞ | Eventually exact dispatch (R2C §4.4, seat-proved, unchecked), so V2–V4 apply. | — |
| Growing p ≪ n | Polynomial-p target results under their assumptions. Logarithmic L and ℓ may be short (N10, N11). | Method budgets (theorem hypotheses). |
| p ≈ n | Exact-Gram LH results need p ≤ n − 1. Centred designs have rank ≤ n − 1. | The proof family's geometry, not the target. |
| Polynomial p ≫ n (p ≤ n^A) | T03/T03♯; T38(b1-LH-iid) is XF GAP; the study generator is N8. | **Prior and proof technique** (INV §3b), not the sampler. |
| p ≤ e^{Cn^α} | No theorem. Whether our prior admits it is **OPEN**, not impossible. Song–Liang's range rests on their own prior and conditions. | — |
| Joint growth | Budgets are polynomial. The by-definition limits are the fixed allocation and the Θ(p) round. | Method-induced: K excludes s₀ > K; fixed B limits whole-group recovery to g ≤ B; bounded stores; log ℓ and L; N₀ ≥ p (`SYNTH_R2.md:98–103`). |

Also: w1 (the neighbour scale is √(2 log p / n); spec §10's √(log n / n) agrees only under p ≤ n^A) and w3 (1-NN fallback when p > e^{n/2}). These affect proposal efficiency only; validity rests on the Hastings ratio (R2C §4.4).
- *Cells:* row 1 × A, and row 1 × "NONE: growing s₀"; INV §3b "p up to e^{Cn^α}: LACK".

**N13. Retention lemma.**
- *Statement:* if S₀ ∈ 𝒮 and δ₁ < ½, then S₀ ∈ 𝒯 = top_{40p+1}(𝒮), and the HPM and MPM^𝒯 certificates are equivalent.
- *Status:* **PROVED** (PC1 claim 5, last paragraph; R2C D7). Premises: Lemma S and the inheritance merge (PC2 code facts).
- *Supports:* A3's composition with R5, card L3, M2's eviction wording.
- *If it fails:* not applicable (PROVED). Unqualified retention stays false.
- *Cell:* row 11 × A.

**N14. Stacking statements.**
- *Statements:*
  - (a) Cor W-R(b): post-search nesting and HPM(R′) ⪰ HPM(4) with the extra search. PROVED (PC1 claim 6).
  - (b) Every listed bound holds per run for any R′ declared before final randomness (PC1 claim-6 table).
  - (c) IND-T for streams 10..9+R′: code audit, not done.
- *Supports:* M7.
- *If the extra search were dropped:* PC1's three uses (monotonicity, D_n(R′) ≤ D_n(4), and transfer of R = 4 study measurements) must be removed from the paper. No listed theorem is affected.
- *Cell:* row 8 × V; row 8 × "NONE: choice of R vs N" (D4 stays a PROOF SKETCH, v2).

**N15. Work and depth at the implemented level** (D1(b) restated).
- *Statement:* the depth and work count for island-parallel v3.1, including setup, the (h) tables, calibration ((1+4I)·H₀ work and (1+I_e)·H₀ depth), the final run N_e(T+L+4)m, LS0, the extra search, and population reductions.
- *Status:* Prop D PROVED (counting). The calibration share is seat-derived (R2A, R2B) and not proof-checked.
- *Supports:* M5, M8, M13.
- *If it fails:* a counting error would be fixed by counting again; no decision depends on it.
- *Cells:* row 8 × "NONE: parallel speed-up / work–depth theorem" (filled as a counting theorem; *speed-up versus sequential MCMC* stays empty: empirical, OPEN); row 7 × C; row 5 × "NONE: depth as a function of correlation" (filled only on the ideal grid via A₀; as-coded stays OPEN).

**N16. Floating-point contract.**
- *Statement:* validated SC(η_F) for scores, Φ, M and Z_𝒯⁻, and VAL-FP(η, ε) for Ẑ at production size.
- *Status:* **OPEN**. VAL-FP was MEASURED at p ≤ 40 only. η is a documented heuristic (`v3_score.h:240`). PC2's exact-rational test found no violation in 60 cases (max |error|/η = 0.069); that fails to refute the heuristic but does not prove it.
- *Supports:* M10's labels, e2, e5.
- *If it is never done:* labels stay "numerical". No decision changes.
- *Cell:* row 14 × "NONE: floating-point error theorem"; row 9 × "floating point: VAL-FP MEASURED at p ≤ 40 only".

**N17. Analytic bounds on Z and π(Ŝ).** Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν}, and equivalently π(Ŝ) ≥ e^{F(Ŝ)}(2b₀ + yᵀy/(n+1))^{ν}/C_n.
- *Status:* **PROVED** (PC1 claim 1; PC2 C1(c) note). About 530 nats loose at n = 200.
- *Supports:* M14(ii); it refutes a candidate limitation.
- *Cell:* row 9 × "NONE … an upper bound on Z is impossible from a run (MASKZPIP)". **INV's wording there is literally false** and must be corrected to "no useful upper bound".

**N18 (only under item-1 Outcome 1). Depth comparison between starts.**
- *Statement:* under stated conditions, the block start's A₀ (or its realised T) is ≤ that of the singleton or prior start.
- *Status:* **OPEN**, no route in the sources. The ideal two-state law predicts ≈ 1–1.2 stages (`SYNTH_R1.md:17`).
- *If it fails or is not attempted:* the Outcome-1 depth claim stays empirical and labelled as such.
- *Cell:* row 4 × "NONE"; row 5 × "NONE: depth as a function of correlation".

**Carried over, unchanged (already in TL):** DELIV-POP (A4, OPEN; row 10/11); Conjecture P (D2, inside N5(b3)); Π(X) upper bound (R7); LH-iid XF GAP (R5); S4 weight stability (§5.3).

---

## 4. Inherent limitations to state in the paper, and what is NOT inherent

### 4.A Inherent: PROVED impossible, or true by definition (cite the label)

| # | Limitation (narrow wording) | Why it is inherent | Source / label |
|---|---|---|---|
| I1 | Each move round has m = p + B + 2 sequential steps per particle. | By definition of the chosen single-site, full-coordinate round. It is inherent **to the kernel, not to SMC or BVS**. Changing it is C10 (WORKHORSE; breaks R5(b2), BG3, V5). | Prop D remark; S1 item 3; R1_B:72; R2C §3 row 8 |
| I2 **[R3]** | Every move round reads all p columns of X (or the Gram entries), so every worker needs **access** to all of X, local or shared/distributed at a communication cost. | By definition of a full-coordinate round. A private 8p² Gram per worker is **not** inherent (C7). | S2 P-D6(i) (`SYNTH_R2.md:67`) |
| I3 | A product-of-blocks start is masked under T27(i)'s hypotheses: π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}. | PROVED-LOCKED, CONDITIONAL (H2, H3); on LH, no open hypothesis. Scope: the specified product construction and designs, not "every conceivable start". | TL S1(c); R2C §3 |
| I4 | One-shot importance correction from π₀ needs ≈ Q* = p^c n^{c/2} draws. | SEP-A/B PROVED, XF VERIFIED; Chatterjee–Diaconis 2018 Thms 1.1/1.2 (exp(KL)). It is about one-shot IS and is the reason the bridge exists. | TL S2 |
| I5 | No diagnostic computed from the run's own weights or island agreement can detect a never-visited mode. | MASKZPIP E1c PROVED; V12; Chatterjee–Diaconis 2018 Thm 2.1. Scope: no *universal* guarantee from the observed record. A positive certificate (Ẑ < Z_𝒯) can still detect some failures. | INV rows 7, 13; R2C §3 |
| I6 | At n = 200 the exact posterior often misses S₀; selection accuracy there is limited by the statistics, not the sampler. | Thm N200 PROVED (author only); the Π(X) lower bracket PROVED. Scope: facts about those data and the fixed target (565/2,400, dossier §4), not a universal rate. | TL R4; R2C §3 |
| I7 | There is no *useful* upper bound on Z from the run's record alone. | The literal "no upper bound" is **false** (N17). What is proved: T31(c) (PROVED-LOCKED, as cited by R2A D6(ii)) and PC2 C1(c), "no lower bound on π(Ŝ) from unbiasedness", PROVED relative to T31(c). "Useful" is not a theorem word, so the paper should state T31(c) itself. | PC1 claim 1; PC2 C1(c) |
| I8 | Without further assumptions, Markov is the only assumption-free probabilistic lower bound on Z. | Markov is sharp given only nonnegativity and the mean (a two-point law attains it). This is elementary and Seat C's argument, **not covered by PC1**. Adding Z_𝒯 keeps 95% coverage (PC1 claim 2). | R2C D6(iii) |
| I9 | Definitional limits of the shipped settings: (a) the cap K excludes s₀ > K; (b) groups larger than B cannot be returned intact as one block; (c) bounded stores (40p+1) can omit posterior mass; (d) the restriction to V does not inspect V's complement; (e) a fixed allocation cannot support unrestricted growth (V13); (f) with a clock-based guard, *delivery* depends on hardware, and estimates are a function of (X, y, seed, binary) only on 𝒪; (g) no finite scored set certifies the global mode without a bound on unscored mass. For (g), the R box certificate supplies such a bound on [∅, U]. | By definition. | `SYNTH_R2.md:98–103`; R2B §3(iii); R2C §3 row 6, §4.4; PC2 C4 |
| I10 | The equal-weight PIP keeps the single-island bias for every R. | Prop P(i) PROVED (candidate). It is a property of the **secondary** estimator, which is why M4 holds. | TL V3 |
| I11 | Calibration rebuilds are sequential, so calibration depth grows with I ≤ ℓ. | By definition of the kept rebuild rule (each rebuild reads the previous grid). The cost consequence is measured (D4). | R2B D4; S2 D4 |

**Proposed as inherent, but no basis filed (do not print as a theorem):** Seat C's "finite-budget universal posterior accuracy without overlap/mixing/weight-moment conditions is unavailable" (R1_C §7, "INHERENT LIMITATION"). No proof or citation is given in the files read.

### 4.B NOT inherent: OPEN, so never present these as limitations

- Rebuild convergence; P(S₀ ∈ V); P(schedule_limit), P(grid_unconverged); the as-coded masked T_n (Conjecture P). (N5(b))
- P(U) → 0, delivery (R6). Only the fixed-allocation part is definitional (I9(e)).
- The severity of masked weight variance on the production grid: E[W²|𝓒] and two-sided masked Ẑ (V11). (N4(iii); M14(iv))
- Equal-weight PIP accuracy (DELIV-POP), Thm R. (A4)
- The measured-round identity for general h. (N1)
- Mixing of the φ = 1 round (V10). (N10)
- ℓ and L sufficiency for growing support. (N10, N11)
- The study generator (g = 5, PART-pairing); LH-iid (XF GAP). (N8, R5)
- p up to e^{Cn^α} under our prior. (N12)
- The finite-n upper bound on Π(X). (R7)
- Weight stability for the actual partition (proposal §5.3). (S4)
- The floating-point contract (SC, VAL-FP at production size). (N16)
- Positive power of any flag. (INV row 13)
- Memory: the private 8p² Gram (C7, engineering). (I2)
- Depth advantage of the block start (item 1); speed-up versus sequential MCMC (empirical, needs a stated comparator). (§1.B; R2C D3d)
- The e4 tie-DP invariant; W-cal executed; integrated-LS0 replay; GUARD-W code audit; IND-T for streams 10..9+R′. (N2, N3, N14)

---

## 5. Mapping: THM-INV §1 cells → what fills them after this meeting

"Filled" means by a TL item or a new obligation, at the status stated. "Empty" means no theorem is planned, with the reason.

| INV row | V | A | C | F | "NO theorem" column after the meeting |
|---|---|---|---|---|---|
| 1 Target | T01 (R1) | T03♯ (R1) + scope N12 | — | T07 (R2) | Π(X) upper bound → **R7 OPEN** (v2). Contraction rates → **empty** (not a v1 target). Growing s₀ and e^{Cn^α} → **N12 OPEN** |
| 2 Exact branch | by construction | V2–V4 | threshold; n ≤ 5 all p (w2); eventual exactness (N12, seat-proved) | W2-T26 remark ERROR | n = 2 extension (e3) PROOF SKETCH |
| 3 Blocks | — | W7-PART Thm B (S1/R5 hypothesis, e1) | tables ≤ p2^B/B; (h) stage (N15) | PART-CE2 | study packing → **N8 OPEN**. Adaptive or random partitions → **empty** (no decision needs it; any change is WORKHORSE) |
| 4 Start π₀ | exact sampler → **N9** | T22 (S1) | — | T27(i), DIL, SEP (S1, S2) | backfit start → **empty** (rejected for paper 1). Start depth comparison → **N18 only under Outcome 1** |
| 5 Bridge / schedule | by construction | T22(iv) | Theorem G, STG-M (D2) | Lemma J | as-coded masked T_n → **N5(b3) OPEN**. Depth vs correlation → D3(b) on the ideal grid; as-coded stays OPEN |
| 6 Kernel | → **N9** (V5 row) | B2-LH etc. (R5) | m = p + B + 2 (I1) | A-REV7 | mixing → **N10 OPEN** |
| 7 Calibration | → **N5(a)** contract | V11 → **N4(iii)** | Theorem G; calibration share (N15) | E1c (I5) | rebuild convergence, P(schedule_limit), V coverage → **N5(b) OPEN, stay empty**; the decision survives |
| 8 Islands / pooling | Prop 2 + **N1** + **N2** + **N14** | Prop P(ii)/(iii) + PC1 claim 3 (V3, A1, N4) | D1(b) restated (**N15**) | — | work–depth → N15 (counting). R vs N → D4 (v2, PROOF SKETCH). Island variance vs correlation → **N4(iii) OPEN**. Speed-up vs MCMC → **empty** (empirical) |
| 9 Ẑ | T12/T31 + **N6** (output event) | T26; P3 (A3); **N17** | — | E1a; C1 → card G1 (**N7**) | "upper bound impossible" → **corrected by N17**. Two-sided masked → **OPEN (V11, v2)**. fp → **N16 OPEN** |
| 10 PIPs (Ẑ-weighted now primary) | islandwise identity; N1 for h | Prop P(iii), PC1 claim 3, A1; P3 + MPM^𝒯 at δ₁ < ½ (A3) | — | O-CERT empirical | joint inclusion → **A1 + N1 (PROOF SKETCH; declared 𝓗, new runs only)**. Equal-weight at fixed R → A4 (secondary, DELIV-POP OPEN). Credible sets → **empty** (rejected as a target, INV row 10) |
| 11 HPM | T07, T21, N200 | R5 with LS0 → **N3**; **N13**; PC1 claim 5(a) (R4) | T32(i) + LS0 + extra search | N200; OSWAP | P(U) → **R6 OPEN**. Finite-n Gibbs-route discovery → **empty** (OPEN, no route). Study generator → **N8 OPEN** |
| 12 Local search | Theorem A, LS-score (R3) | ThmB-T37 | ≤ (ℓ+1)(p + K(p−K)); **N11** | literal T37 fails | meaning of `local_certified` → card L1 (deterministic gaps, **N7**). LS0 absent from production → **M2 + N2(c)/N3** |
| 13 Flags | — | — | — | V12, E1c; card G/L/R as certificates (**N7**) | positive power → **empty**: flags stay labelled heuristics (S1 item 6); no route |
| 14 Resources, GUARD, numerics | Lemma RO + GUARD-W (V4 split; N6 premise (i)) | — | T32(i) | CEX-guard; `log_Z` hazard → fixed by M11 | P(resource_limit), P(schedule_limit), P(numerical_failure) → **R6 / N5 OPEN**. fp theorem → **N16 OPEN** |

INV §3a proposal targets after the meeting:
- §5.1 → N9.
- §5.2 → V1 (cited).
- §5.3 → S4 (OPEN).
- §5.4 → S1/S2 (exceeded in kind).
- §13.1 → A1 + N1 (PROOF SKETCH).
- Diagnostics → the card (deterministic positive certificates, not diagnostic power).

---

## Conflicts and undecided points (also listed in the final message)

1. **V1(a) scope.** TL lists V1(a) for general bounded h under locked statuses (TL:63, 74). TL A1 (TL:202–203), R2C D7 and PC1 claim 3 treat the general-h measured-round identity as an unverified crux. I recommended a split.
2. **Lemma RO / GUARD status.** TL V4 says Lemma RO is XF VERIFIED. PC1 and PC2 call "Lemma RO / GUARD" an unreviewed W2-BOOK premise. I read the second as GUARD for the v3.1 worker code. Not settled.
3. **"Free of N, H, R".** TL D1 and D3 (TL:29, 309, 378) conflict with S2 D3d. The TL summary formula is the particle-parallel one.
4. **R6's "≈ 4× headroom"** (TL:42, 699) is not measured: 1.9× on 2 cores, and no 4-core figure may be printed.
5. **INV row 9's "an upper bound on Z is impossible from a run"** is literally false (PC1 claim 1). **INV row 10's "equal-weight primary"** predates M4.
6. **P-D7's default 𝓗 item "terminal frequency of the returned HPM"** is a run-dependent h, which N1/A1 as stated do not cover. Could not decide whether it should be dropped from 𝓗 or covered by a separate argument.
7. **A1's RB version for joint indicators** versus P-D7's plain averages only.
8. **Seat C's correction 3 on C4(b)** (isolate {Ŝ}): PC2 rules it a matter of sharpness, not validity. I followed PC2.
9. **R2B D3c still says "stores nested"**; S2 closed D3c with Seat C's correction. I followed S2.
10. **"BASIN"** (R2B §3) is not defined in any file read.
11. **"C1" names three different results** (Thm SL; MASKZPIP C1; O-CERT C1).
12. **Seat-level results not yet proof-checked:** the calibration ratio 0.05 + 0.2·I (R2A); eventual exact dispatch for fixed p and the n = 2 extension (R2C); the store-eviction identity (R2C); Markov sharpness (R2C); Lemma KL (TL). None is upgraded here.
13. **Item 1 is pending,** and the Round 3 proposals (card, P-D6(i), P-D7, P-9) are unaccepted. I did not read ABL-START results.
14. **My own reading, not a source statement:** that S1(a),(d) may cover arm B as the B = 1 partition (§1.B, Outcome 3).
