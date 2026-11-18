# ADJ_MINORS_iii — independent adjudication of the 20 class-(iii) minors

Adjudicator: review sub-agent (Claude Opus 5.5), 2026-11-15. Read-only; this file is the only write. No git state changed.
Input: `W3-EDIT/Theory_work/Wave3/W3-EDIT/TRIAGE_MINORS.md:7-26` (class iii), finding texts in
`W3-EDIT/.../reviews/H1_minors_extract.tsv` (row n = I1-Mnn). All line references below are to the THEORY-DEPT worktree
(same files as main), path prefix `Theory_work/` omitted.

Dependents come from the registry `depends_on` edges (`INFRA/registry/claims.tsv`; the `consumes` column is empty for
these ids). Where a NARROW verdict has dependents, `propagate.py narrow <id> --still-covers <uses> --dry-run` was run
with the uses listed. It printed impact only and wrote nothing; `git status` was clean afterwards. Without
`--still-covers`, narrowing W1-GEN:Thm-GEN(C4) would mark 5 direct and 40 indirect dependents SUSPECT. With the uses
actually relied on (`stmt; proof:every-sequence argument`), the result is 0 direct and 0 indirect. The same 0/0 result
holds for W2-FAC-B:Thm-FAC-CS, W2-UNI:U-LOC and W2-FAC-XA:L2 with `stmt`.

Verdict key: **E** = editorial · **PATCH** = local proof/wording fix, claim unchanged (or only strengthened) ·
**NARROW** = statement claims more than proved / omits a used hypothesis · **REFUTED** = false.

## ★ rows (headline candidates) — detail

**I1-M61 · W1-GEN:Thm-GEN(C4) — NARROW (clause only).**
(C3) has two parts. One is a finite-n bound, "D_n ≤ P(S̃₀ ≠ S*) + P(Ω_nᶜ), P(Ω_nᶜ) = O(1/log n)" for n ≥ n₀
(`Wave1/W1-GEN/STATEMENT.md:108-110`). The other is the limit statements that follow ("Hence …", :110-111). (C4) says
"the conclusions of (C3) … hold under the joint law" (:119-120). L5.4 proves only the limits (`lemmas/L5_assembly.md:66-67`).
Its proof goes through the diagonal Lemma L5.3, which gives only sup_{𝒜_n} f_n → 0 (:57-64). No rate is available,
for two reasons:
- (C4) puts no rate on P(𝒜_nᶜ);
- the onsets n₀ (SEP, NL_avg, "eventually") may depend on the sequence (Remark, :79-81).
REPORT repeats the over-strong reading: "Random designs: the same holds" after the rate display
(`Wave1/W1-GEN/REPORT.md:39-41`). This is not a refutation: the rate is unproved, not shown false.
*Restatement:* "(C4) … Then D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n) hold under the
joint law of (X, ε) (resp. under (C3-fav)'s hypotheses); the finite-n bound and the O(1/log n) rate of (C3) are not claimed
for random designs." Make the same edit at REPORT:40-41.
*Consumers:* C5b, C5d-S1346, C-MIS:Cor-D, W2-FAC-A:L5 (@proof every-sequence argument) and C-PACK:SL1.I-c all use limits
only:
- `C-MIS/STATEMENT.md:116-120` (limits);
- `W2-FAC-A/lemmas/L5_random_instances.md:51-53` (limits);
- `C-PACK/lemmas/I4_SL_corollaries.md:57-60` (δ_n = O_P(r_n) via T03♯ plus the diagonal argument, not GEN's rate).
**None relies on the rate.** The headline row's main clause (C3, the registered lines 108-111) is untouched.

**I1-M35 · W2-FAC-B:Thm-FAC-CS (C1) — NARROW (sub-clause only).**
The statement defines S̃₀ as the **emitted** start-mode centre (`Wave2/W2-FAC-B/STATEMENT.md:53-54`). (C1) is stated
"Under G, (CS), (P), (θ), (FS)" (:105). Its first sentence, unique maximiser w.p. → 1, is proved from these alone
(`lemmas/L2_start.md:72-77`). Its second sentence, "on this event S̃₀ = S*", also needs e4′, "the emitted centre is the
unique maximiser of γ₀" (:66-67), which (C1) does not list. L5.2 invokes it explicitly (`lemmas/L5_assembly.md:32`).
*Restatement of :105-106:* "… P(S* is the unique maximiser of γ₀ on Ω) → 1. On this event, under the implementation premise
e4′ (§1), S̃₀ = S* ⊇ S₀ and |S̃₀ ∖ S₀| = m₀." (Alternative: state the second sentence for argmax γ₀ and add "= S̃₀ under e4′".)
*Consumers:* (C3) and (C4) already carry e4′/e4 (:124, :129). W2-FAC-X restates its premises "e4 read as e4′"
(`Wave2/W2-FAC-X/STATEMENT.md:35`). HQ_AUDIT-W2:B3 consumes the theorem. **No consumer relies on the e4′-free reading.**
The main theorem (C3) is unaffected.

**I1-M27 · W2-UNI:F-UNI — PATCH (hypothesis weakening; claim only strengthened).**
(S) requires "|Q_n| ≤ K_n" and 𝓛_n ⊆ Ω with no "eventually" (`Wave2/W2-UNI/lemmas/L5_delivery.md:17-18`). The instances
supply these only for large n (:36-37: UNI-0 via L2 §2, UNI-1 "K = p eventually"). For small n, K_n < s₀ can make (S)
unsatisfiable, so the instances do not literally meet the hypothesis as written. The proof uses (S) only in the limit:
- Step 3 concludes "P(𝒦_nᶜ) → 0 by (S)" (:28-31);
- the every-n conclusion P(no output) = 0 comes from Steps 1–2, which use (V) only (:23-27).
*Fix:* in (S) read "for all n ≥ some n₁: Q_n ⊇ S₀, |Q_n| ≤ K_n, 𝓛_n ⊆ Ω", and drop the redundant "(s₀ ≤ K eventually)"
at :33-34. The proof is unchanged. *Consumers:* UNI-0 and UNI-1 are only helped. The headline main clause is strengthened,
not narrowed.

**I1-M30 · W3-SAMP:Pkg (label in LT#(f)) — NARROW (label only; no theorem).**
The text says "In general no output certifies W_r ≥ η, because the top store … is a strict subset of Ω"
(`Wave3/W3-SAMP/lemmas/LT_theorem.md:98-99`). STATEMENT has it hedged (`STATEMENT.md:145-147`). REPORT has it unhedged:
"no output certifies W_r ≥ η unless the store holds all of Ω" (`REPORT.md:80`). "Store ⊊ Ω" shows only that the lower
bracket Z ≥ Σ_𝒯 e^F cannot be inverted. It does not show that no function of the outputs certifies the event, which
would need an indistinguishability pair (equal outputs, W_r on both sides of η). That argument is not given; the claim is
plausible but unproved.
*Restatement:* "The observable condition is one-sided: the stored quantities give a lower bound on Z only, so this ledger
bracket does not certify W_r ≥ η unless the store holds all of Ω." Make the same edit at REPORT:80.
*Consumers:* the label sits in registry row **W3-SAMP:LT#(f)** (STATEMENT:141-147), which no claim consumes. W3-SAMP:Pkg
(REPORT:15-29) has no dependents. The LT# main clauses (LT-a…LT-e′, STATEMENT:126-140) and C, D, TR are unaffected.

**I1-M57 · W2-APP:POST, J_n(c) sub-clause — PATCH (sub-clause only; main clause unaffected).**
The sub-clause reads "without beta-min … the inclusion clause for J_n(c) holds likewise" (`Wave2/W2-APP/lemmas/L1_POST.md:33`)
and its proof is one sentence (:68). J_n(c) is not defined in the ticket. The input is **not** an unstated variant: it is
T03♯'s own no-beta-min clause, π(S ⊉ J_n(c)) = O_P(√(log n/n)) with J_n(c) = {j ∈ S₀ : θ*²_j ≥ cσ² log n/(nφ₀²)} and
c > c₀ (`State_of_Project/sections/04_theory.tex` stmt "Final statement", THEOREM_LIST_FINAL:462). It is restated as C-PACK
SL1′ (`Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:65-68`), and POST already depends on C-PACK:I4. Steps (2)–(4) do not use
θ_lo. The transfer of step (5) applies verbatim to π(S ⊉ J_n(c)) with the common φ₀² = φ²/2. W3-POST has already written
this out (`Wave3/W3-POST/STATEMENT.md:114-118`, Cor 1R(b), checked R02-F4).
*Fix (2 lines at :33):* "…holds likewise: with J_n(c) as in T03♯ (TH09) / C-PACK SL1′ for c > c₀ and φ₀² := φ²/2,
π(S ⊉ J_n(c)) = O_P(√(log n/n)) and max_{J_n(c)}(1 − PIP_j) = O_P(√(log n/n)); in this regime (a) holds without its BM-∞
clause and the common BM envelope." Optionally add a one-line citation at :68.
*POST main clause:* **unaffected.** (a) with beta-min, and (b)'s 1 − π(S₀) = O_P(√(log n/n)) with SL1 (a)–(e), stand as
written. W3-RM2:RM2-R consumes POST @hyp under Setting R, which has |θ*_j| ∈ [θ_lo, θ_hi], i.e. beta-min, on the
standardised scale (`Wave3/W3-RM2/STATEMENT.md:52-53`, (P10) at :257). W3-RM:B9 uses POST(b) with Setting R's signal
bounds (`Wave3/W3-RM/lemmas/L4_formR.md:49-50`). W3-MISR does not consume W2-APP:POST directly: its edges run through
W3-POST2:A1/C/D/E and SOP:TH09 (registry rows 413-418). W3-POST2:A1 uses only POST's step-(5) diagonal transfer
(@proof). None of these uses the J_n(c) sub-clause.

**I1-M58 · W2-APP:POST, raw-scale parenthetical — PATCH (parenthetical only; main clause unaffected).**
(a) says 𝒜_n is X-measurable (:28). Under the raw-scale convention, the parenthetical's event 𝒢_n ∩ ℋ_n uses sample and
population sd ratios. These are removed by standardisation, so the event is raw-design-measurable, not X-measurable
(:12-15). The parenthetical already instructs "use the raw-design event … run the diagonal argument over raw-design
sequences". The transfer is valid:
- ε is independent of the raw design (:12);
- on ℋ_n, θ* = D_xβ ∈ [b_lo/2, 2b_hi];
- T03♯ is a fixed-design **triangular-array** statement (R1, TH09), so an n-dependent θ* with bounds fixed across n is
  already covered;
- P(ℋ_n) → 1 by χ² tails and a union bound over p ≤ n^A.
*Fix (1 line in (a), :28):* "X-measurable events 𝒜_n (raw-design-measurable under the raw-scale convention of the Setting)".
W3-POST Cor 1R(a) already cites it this way (`Wave3/W3-POST/STATEMENT.md:110-112`).
*POST main clause:* **unaffected.** RM2-R, RM:B9 and the W3-POST2/W3-MISR chain all use the standardised convention, or
only step (5), which is stated for "the joint law of (raw design, ε)" (:31). That is exactly the raw-design measurability
the fix records.

## Table (all 20)

| row | claim | verdict | evidence (file:line) | minimal fix / restatement | consumers affected |
|---|---|---|---|---|---|
| I1-M05 | C-DLV:L1-R | NARROW (constant-level) | `Wave1C/C-DLV/lemmas/L1_resources.md:70-81` ("absolute" C_M; N̄(W+K) not × w), :107-108 (only workspace × w) vs `Wave1C/C-DLV/STATEMENT.md:36-37` (CONFIG: "memory envelope multiplied by w") | "for w concurrent workers the words held are ≤ w·M̄(n,p) (CONFIG)", which keeps C_M absolute; or "C_M depends on the implementation and on w". O((n+p)²) unchanged for fixed w. (Not code-checked whether populations are per worker; if not, this is E.) | Cor-R (its allocation hypothesis reads mem_n ≥ β·w·M̄ + β₀; the sufficient allocation C(n+p)² stands with C depending on w), Thm-D, C-ENG:Impl-DLV-A2, HQ_AUDIT-W1C:A2: all use the polynomial form; none affected |
| I1-M08 | C-DLV:Cor-R | NARROW (hypothesis reading) | `Wave1C/C-DLV/STATEMENT.md:28` (MACH: "wall time ≤ τ·(operation count) + τ₀", scope unstated); applied to sub-segments at `L1_resources.md:127` (timed loop) and :135-136 (elapsed at checkpoint) | In MACH: "for every contiguous segment of the execution, its wall time ≤ τ·(operations in it) + τ₀". E1–E5 also hold under a whole-run reading (elapsed ≤ total). The P̄_t bound (:127), and with it the displayed sufficient time_n (:141), needs the segment reading; with W̄ instead of U₂₀₀ the allocation is still polynomial but larger than :141. | Thm-D, W2-FAC-A:Prop-F-FAC and the other Proposition F users name MACH, so they take on the explicit reading; none needs a whole-run-only MACH |
| I1-M10 | C-DLV:L3-3.3 | NARROW | `Wave1C/C-DLV/lemmas/L3_grid.md:30-32` (unconditional "φ_k = 1"); proof :33-39 reaches 1 only if the loop exits normally; guard/NumericalFailure pilot exits (INVENTORY E1/E2/C3) truncate | "At every tier e, every pilot prefix satisfies k ≤ T_e with non-final increments ≥ 1/T_e; if the pilot returns a schedule, it ends at φ_k = 1 and is the target list of every construction at that tier." | L1-R@stmt uses only the cap (holds for truncated pilots); Thm-D, Prop-F, L3-3.4 and L3-3.5a use "ends at 1" only after a returned pilot: none affected |
| I1-M11 | C-DLV:Thm-D | NARROW (a.s. form) | `Wave1C/C-DLV/lemmas/L4_delivery.md:15` (set identity); proof :24-34 uses Lemma S (null-set exclusions, e.g. yᵀy > 0) | "(ii) 𝒮ℒ_n Δ {calibration escalates to tier 1 and some tier-1 construction fails} ⊆ 𝒩_n (the null set of (i))" | Probability conclusions unchanged; Cor-Dp, C1-CondDelivery, Prop-F, O, HQ A1/A2 and FAC-A Prop-F-FAC use only probabilities: none affected |
| I1-M13 | C-DLV:Thm-D | NARROW (dup of M05) | `L1_resources.md:78-80` vs `STATEMENT.md:36-37` | As M05 (Thm-D inherits M̄ via Cor-R) | As M05: none |
| I1-M16 | W2-APP:Thm-APP | E | `Wave2/W2-APP/lemmas/L4_families.md:167-168` ("per FAC (pending)") vs :149 (FAC-A PROVED-CHECKED on its narrowed class) | Replace the cell with ":149's FAC-A entry (class 𝔉, p ≤ n^{1/6−}; CS needs (GC-CS))". "Pending" understates; nothing is over-claimed | none (Thm-APP gains a cell) |
| I1-M23 | W2-UNI:U-LOC | NARROW | `Wave2/W2-UNI/STATEMENT.md:168-169` ((d) "transfer to (E)/(R) … hence NA and TL") vs `lemmas/L3_ULOC.md:118-126` (transfer term L_ψδ√(5(p+1) log log n); "Under UNI-1's additional rate δ_n√(p log log n) → 0") and `lemmas/L4_k1.md:16` | "(d) transfer to (E) with ‖R̂ − Σ_n‖_op ≤ δ_n ≤ c/4 and δ_n√(p log log n) → 0, and to (R) as in L4_k1 L4.0, by FACA U(d); hence …" | U-LOC-Cor (`L3_ULOC.md:107-126`) states the rate itself; UNI-1 carries it (L4_k1:16). Dry-run with `stmt`: 0/0. None affected |
| I1-M27 ★ | W2-UNI:F-UNI | PATCH | `Wave2/W2-UNI/lemmas/L5_delivery.md:17-18` vs :36-37; (S) used only in the limit at :28-31 | (S) "for all n ≥ n₁"; delete "(s₀ ≤ K eventually)" at :33-34 | UNI-0, UNI-1 helped; none harmed. Headline main clause strengthened |
| I1-M30 ★ | W3-SAMP:Pkg / LT#(f) | NARROW (label) | `Wave3/W3-SAMP/lemmas/LT_theorem.md:98-99`; `STATEMENT.md:145-147`; `REPORT.md:80` | "The observable condition is one-sided; this ledger bracket does not certify W_r ≥ η unless the store holds all of Ω." | none (LT#(f) and Pkg have no dependents); LT#, C, D, TR main clauses untouched |
| I1-M35 ★ | W2-FAC-B:Thm-FAC-CS | NARROW (sub-clause) | `Wave2/W2-FAC-B/STATEMENT.md:53-54` (S̃₀ = emitted centre), :66-67 (e4′), :105-106; `lemmas/L5_assembly.md:32` | (C1): "On this event, under e4′ (§1), S̃₀ = S* …" | (C3)/(C4) carry e4′/e4; FAC-X carries e4′ (`W2-FAC-X/STATEMENT.md:35`); HQ_AUDIT-W2:B3: none. Dry-run with `stmt`: 0/0 |
| I1-M37 | W2-FAC-PK:Thm-FAC-PK | PATCH | `Wave2/W2-FAC-PK/lemmas/L4_assembly.md:32-33` (liminf identity; U_n undefined); proof :37-38 stops at P(𝒪∩{Ŝ⁺≠S₀}) → 0; registered statement `STATEMENT.md:73-87` omits it | Define U_n := 𝒪ᶜ (as `W2-FAC-B/STATEMENT.md:68`) and add "P(𝒪∩{Ŝ⁺=S₀}) = 1 − P(U_n) − P(𝒪∩{Ŝ⁺≠S₀}) = 1 − P(U_n) − o(1)". The identity is true | none (outside the registered statement) |
| I1-M48 | C-ENG:TDP_E | PATCH | `Wave1C/C-ENG/lemmas/TDP_E.md:40` cites N3-code (b), which is stated under (H1)–(H4) and is about the first min(N, cap) elements; :28-34 lists only (H1), (H2-FP), (H4) | Replace the citation with the direct argument: under exact arithmetic a path from r₀ = 0 has Σ mb = M[J][k̂] iff every edge is tight, so E = {size-k̂ maximisers of logprior[\|S\|] + Σ_b logr[b][code(S∩C_b)]} with k̂ the least maximising size, = 𝒜* of W1-N3 §1 under (H1). No (H3) and no cap ≥ N needed | C-ENG:Impl-DLV-A2 (`C-ENG/REPORT.md:54`) repeats "E = 𝒜* (W1-N3 (b))". It is covered by the patched argument; same fix there. Others (L1-R cost use, Impl-Merge, W3-RM:E4 @proof :28-36): none |
| I1-M50 | C-PACK:I1-audit | PATCH | `Wave1C/C-PACK/STATEMENT.md:10-16` (T1.a "catalogue every … substantive use"); table `lemmas/I1_e4_replacement.md:20-44` has the structural row G5 for GEN only | Add rows: P8 = PXN potential-run closure (`C-PACK/lemmas/I4_SL_corollaries.md:96`, W1-PXN FINAL_PROOF:75-79), kind D (structural), resolution e4′ (iii); M6 = the M5(0)/T38 analogue, same resolution. Audit conclusion (:46ff) unchanged | none |
| I1-M55 | C-PACK:I1-e4prime | NARROW (scope) | Registered span `lemmas/I1_e4_replacement.md:141-155` applies e4′ to "GEN (… premise list)" (:142), and e4′(i) allows MR1 routines (:145); the (C6) exclusion is at :159-160, **outside** the span; (C6) needs global maximality (row G8, :36) | :142: "GEN ((C1), (C3), (C3-fav), (C4); premise list for these claims; (C6) retains e4/N3(a) for the coded routine)". Or strengthen MR1 to "returns a maximiser of f on every input under exact arithmetic" | none registered; GEN (C6) keeps e4 |
| I1-M57 ★ | W2-APP:POST | PATCH (sub-clause) | `Wave2/W2-APP/lemmas/L1_POST.md:33`, :68; input in T03♯ (TH09 final statement) and `C-PACK/lemmas/I4_SL_corollaries.md:65-68`; already written out in `W3-POST/STATEMENT.md:114-118` | Define J_n(c) (TH09/SL1′, c > c₀, φ₀² = φ²/2); add "in this regime (a) holds without BM-∞ and the common envelope" | **POST main clause unaffected**; RM2-R, RM:B9 and the W3-MISR chain (via W3-POST2 step-(5) use) do not use the sub-clause |
| I1-M58 ★ | W2-APP:POST | PATCH (parenthetical) | `L1_POST.md:12-15` (raw-design event) vs :28 ("X-measurable"); :31 joint law of (raw design, ε) | (a): "X-measurable (raw-design-measurable under the raw-scale convention)" | **POST main clause unaffected**; consumers use the standardised convention or step (5) only |
| I1-M59 | W2-APP:VN-routes | E | `Wave2/W2-APP/lemmas/L5_VN.md:28-34`. GEN (C1) needs only G, R (bounded energy), p ≤ n^A, (H2), s* ≤ v̄, with no (H0)/(H1) (`Wave1/W1-GEN/STATEMENT.md:84-85`). GROW (C3) needs only ‖μ‖² ≤ Mn, p ≤ n^A, (G1), (G3) (`Wave1C/C-GROW/STATEMENT.md:111`) | The "hence" sentences name exactly the hypotheses that go beyond the standing energy and dimension bounds. Optional words: "(given ‖μ‖² ≤ Mn and p ≤ n^A)". The auditor lacked the GEN/GROW statements | none |
| I1-M61 ★ | W1-GEN:Thm-GEN(C4) | NARROW (clause) | `Wave1/W1-GEN/STATEMENT.md:108-111, 119-120`; `lemmas/L5_assembly.md:57-67, 79-81`; `REPORT.md:39-41` | "(C4) … Then D_n → 0, P(𝒪∩{Ŝ⁺≠S₀}) → 0 and the liminf identity hold under the joint law; the finite-n bound/O(1/log n) rate of (C3) is not claimed." Same at REPORT:40-41 | C5b, C5d-S1346, C-MIS:Cor-D, W2-FAC-A:L5, C-PACK:SL1.I-c use limits only. Dry-run with `stmt; proof:every-sequence argument`: 0/0. **Headline main clause (C3) unaffected** |
| I1-M69 | W2-FAC-XA:L2 | NARROW | `Wave2/W2-FAC-XA/lemmas/L2_robust_path_attempt.md:200` ("exactly \|S*\|−s safe deletions and stops at S0") vs hypothesis list :181-193: no start point stated; best-improving rule only implicit (method def. `W2-FAC-B/STATEMENT.md:56-57`) | Add to the hypotheses: "the actual search starts at S* (FAC-X X1 / FAC-B (C1) event) and is the method's best-improving §6.10 LS0" | W2-FAC-XA:L7 (`L7_shadow_midpoint_attempt.md:34-47`, "for all histories") must supply the start at S*. Not checked there; both are PROVED-CONDITIONAL "attempt" files. Dry-run with `stmt`: 0/0 |
| I1-M70 | W2-FAC-XA:L2 | NARROW | `L2_robust_path_attempt.md:186-193` (o(H), .04+o(1) per prefix); proof uses them uniformly (:213 "uniformly"; "eventually" at :210, :233) | ":186: … GEOMETRIC hypotheses, with all o(1), o(H) terms uniform over prefixes and states, on every prefix …" (L7 already states "o(H) is uniform in histories", L7:40) | W2-FAC-XA:L7 consistent; none affected |

## Summary
1. No ★ row's main clause is affected. GEN (C4) (M61) and FAC-CS (C1) (M35) are NARROW only in a clause or sub-clause, and no consumer uses the over-strong part (dry-runs 0/0). F-UNI (M27) needs a PATCH that only weakens a hypothesis.
2. W2-APP:POST (M57 J_n(c), M58 raw-scale) is PATCH in a sub-clause or parenthetical. Its main clause (a)+(b), consumed by W3-RM2:RM2-R and, through W3-POST2's step-(5) transfer, by W3-MISR, is unaffected, so POST can be recorded with the two wording fixes.
3. Counts: **E 2** (M16, M59) · **PATCH 6** (M27, M37, M48, M50, M57, M58) · **NARROW 12** (M05, M08, M10, M11, M13, M23, M30, M35, M55, M61, M69, M70) · **REFUTED 0**.
4. All 12 NARROW items are statement-precision fixes: a missing "under e4′", "a.s.", "eventually" or "rate" hypothesis, a scope word, or a constant's dependence. Every one has a one-line restatement, and no consumer anywhere relies on the over-strong reading.
5. Points to watch: M61 also needs the same edit in W1-GEN REPORT:40-41; M48's fix should be mirrored at C-ENG REPORT:54; M69 needs W2-FAC-XA:L7 to supply "start at S*"; M05 is E if populations are not per-worker (not code-checked).
