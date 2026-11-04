# MEET-v31 · Amendment HQ-01 (2026-11-04)

Record of the changes made to the final MEET-v31 documents after two independent reviews. The amendment editor applied HQ's dispositions and decided nothing.

**Inputs.**
- HQ's dispositions (binding): `/home/fb31/hq_reviews/HQ_DISPOSITIONS.md`.
- Reviews: `/home/fb31/hq_reviews/SOL1_proof_check.md` (60 findings, audited at c3e18ee) and `/home/fb31/hq_reviews/SOL2_audit.md` (13 findings, at c3e18ee).
- HQ's own fix for F04: `evidence/item1_scripts/apply_rule_v2.py` and `evidence/item1_scripts/HQ_NOTE_v2.md` (commit 8f6051b).

**Documents edited** (each now carries the line "Amended by HQ on 2026-11-04 (AMENDMENT_HQ_01.md) after independent review."):
- **N** = `MINUTES.md`
- **M** = `METHOD_v3.1_FINAL.md`
- **T** = `THEOREM_REVISION_INPUTS.md`
- **A** = `ITEM1_ABL_START.md`
- **S** = `STATUS.md`

Seat files (`R*_*.md`), syntheses (`SYNTH_*.md`), `DOSSIER.md`, `FORMAT_NOTES.md` and `evidence/` are the record and were not edited.

**Rules followed.**
- Status words are preserved except where a disposition changes them; none is upgraded.
- A withdrawn sentence is replaced by the corrected statement.
- Numbers that come from a reviewer's own computation are tagged "review check, SOL1 #nn". They are not registry results.
- Item-1 numbers were re-checked against `evidence/item1_per_fit.csv`:
  - certified count: C 10/12, A 0/12, B 0/9;
  - max C/A spread: 76.08;
  - B, S5 r001: log Ẑ = −105.5146.

**Counts.**
- Changed: 45 findings (SOL1: 32; SOL2: 13).
- No change: 28 findings (SOL1: 26 TRUE, plus 2 UNCHECKABLE).
- Questions for HQ: 7.

---

## 1. SOL2 findings (F01–F13)

| ID | HQ disposition | Document § changed | Before → after |
|---|---|---|---|
| F01 | N9 is a **closure gate**; "Open method questions: none, conditional on N9 (running). If N9 fails, the method question reopens before the theorem meeting." Keep N9's status words. | N §9; S; T header "Meeting state", §3 N9; M header | "**None.** … Neither kind can change a decision taken here" → "Open method questions: none, **conditional on N9** (running). If N9 fails, …"; N9 named as a closure gate on branch `theory/N9-KERNEL`; §9 lists N9 and the binding goals as the two exceptions. S: "Open questions: none" → the same conditional sentence. T N9: "Closure gate" bullet added; its failure branch now ends "before the theorem meeting". N9's status ("by construction, consultant-checked, no registry row") is unchanged. |
| F02 | For obligations tied to a binding goal, the failure branch reads: "If it fails, the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change." | T §3 N1, §2 S4, §2 A1, §3 N9, §4.B, §5 (INV §3a targets); N §5 (Not-inherent list and closing sentence), §9; M header; S | T N1: "μ̂(h) is a descriptive summary, no theorem; … §13.1 stays LACK" → escalation sentence (§13.1), followed by the interim consequences "until that decision". T S4: "Keep v2; list as OPEN" + escalation sentence (§5.3). T N9: escalation sentence added (§5.1). T §5: binding-goal rule stated under the INV §3a targets. N §5: "why that decision survives if the obligation fails" → "what happens if it fails", plus the escalation rule. Binding obligations found: **N1 (§13.1), S4 (§5.3), N9 (§5.1)**. Others checked: Q3. |
| F03 | C6 trigger = **union**: particle-parallel depth claim **or** any demonstrated fit with p > 2,500. Felipe (2026-11-03): island-level depth only; study p ≤ 1,000, so neither fires. Record the seats' positions; no claim of unanimity. | N §2 dec. 6, §7 action 10, §9; M §2 #19, §3 C6, §5 row 14; T §1.A M13; S | "C6 … iff paper 1 claims particle-parallel depth" → "… iff paper 1 claims particle-parallel depth **or** demonstrates any fit with p > 2,500". The text records the union as HQ's disposition (A/B: R2_A:23, R2_B:21, R3_B:44; C: claim condition), states that the narrower trigger was not unanimously adopted, and records Felipe's 2026-11-03 scope. "Island-parallel results may be reported at any p" → "… with their actual cost" (the p > 2,500 trigger applies). N §7 action 10 → "Paper-scope decision (made)". |
| F04 | Done by HQ (`apply_rule_v2.py`, `HQ_NOTE_v2.md`, 8f6051b). Cite them; Outcome 2 unchanged. | N §3, §6 ABL-START row, §7 action 12; M §2 row 0 (Outcome 2 bullet); T §1.B conventions; A §1 outputs, §2; S | Added: "v1 lacked the absolute gate; v2 enforces need = max(9, ⌈0.75·complete⌉); same Outcome 2; v1 kept as the committed evidence". The re-run instructions now point to v2. |
| F05 | Use HQ_NOTE_v2's certified count (C 10/12; A and B 0). Reference-based wording: "below A on 12/12", "agrees with A"; "consistent with" the masked-crossing mechanism. | N §3; A §3; T §1.B; M §2 row 0; S | N: "C underestimated log Z on 12/12 … This is the masked-crossing … mechanism" → "below arm A's on 12/12 … certified Ẑ < Z on 10/12 (A, B: 0) … consistent with the masked-crossing mechanism; unbiasedness alone does not diagnose it". A: "Because Ẑ is unbiased, … is the … mechanism … clearly worse on objective 1" → a certified-underestimation paragraph (10/12; exceptions S4 r002 c050, S6 r002 c050; A 0/12, B 0/9) plus "consistent with". "B matches A on accuracy" → "B agrees with A on log Ẑ (not certified accuracy)". T: "B matched A" → "agreed with A"; "2.6–13.3 nats low" → "below A and B"; certified count added. |
| F06 | Restore "seat-derived, unchecked" at Markov sharpness (I8) and the n = 2 p-fold tie (N12). The chair's duplicate-retention code check is not a proof of the n = 2 output. | N §4 e3, §5 item 6; M §2 #25 (e3), §5 row 5; T §1.A M12, §3 N12, §4.A/4.B I8 | e3 everywhere: "All singletons tie exactly, because duplicates are kept (chair-checked)" → the tie statement attributed to R3B, **seat-derived, unchecked**, and the code check described as "not a proof of the n = 2 output". Markov sharpness labelled seat-derived, unchecked, and **moved** out of the inherent list (Q1). |
| F07 | Five of Seat C's corrections upheld; correction 3 concerns sharpness, not validity (withdrawn by C as a validity objection). | N §2 dec. 10 | "all six of Seat C's corrections upheld" → "five … upheld in their stated forms; correction 3 concerns sharpness, not validity, and was withdrawn by C as a validity objection". |
| F08 | 2,500 floor = a declared budget; "MC SD ≤ 0.01" is only an iid benchmark (resampling creates dependence), not a guarantee. | M §5 row 14 | "floor: per-island RB-PIP MC SD ≤ 0.01" → "the 2,500 is a declared budget. 'MC SD ≤ 0.01' is an iid-sampling benchmark only (1/(2√N)); resampling creates dependence, so it is not a guarantee". |
| F09 | Grid-equality stopping rule → class (b) (deterministic rule); cap (b)/(c). | M §5 row 31 | "stopping rule (a) (lead's ruling; R2_B row 20); cap (b), (c)" → "stopping rule (b), a deterministic rule (reclassified from the lead's (a) …; values unchanged); cap (b)/(c)". |
| F10 | Rule timing = "committed before any arm-C or S4/S5 result was read" everywhere; note that some A/B results were already filed. | T §1.B; N §2 dec. 1 evidence, §3, §6 ABL-START row; A §1 outputs | T: "Rule fixed before any result was read" → "committed before any arm-C or S4/S5 result was read; some arm-A/B results were already filed (pip_rescore REPORT, a240857; arm A bitwise check, S2 §0.3)". N dec. 1: "a rule fixed before the results" → narrow timing. N §6: "pre-registered before results" → narrow timing. A: filed-A/B note added, with "git establishes filing order, not reading time". The label "pre-registered rule" is kept as a name. |
| F11 | "No diagnostic from the observed record has a universal detection guarantee for never-visited modes"; positive one-sided certificates can still detect some failures. | N §5 item 4; T §4.A I5; M §4 (PSIS row) | "… can detect a never-visited mode" / "cannot see never-visited modes" → "… has no universal detection guarantee for never-visited modes"; certificates (Ẑ < Z_𝒯, card G1) "can still detect some failures". |
| F12 | −105.51; spread ratio max ≈ 76×; label seconds as calibration + final (setup excluded), or use totals. | A §3 table, bullets | −105.52 → −105.51; "1.5 to 74 times" → "1.5 to 76 times"; seconds column header → "seconds A / B / C (calibration + final; setup excluded)". |
| F13 | Stale "all items closed except item 1". | T header | "All items closed except item 1, which closes … when ABL-START finishes" → "All items closed; item 1 closed by the agreed rule as Outcome 2 (§1.B)", plus the N9 conditional sentence (F01). |

## 2. SOL1 findings that changed a document

"Correction" = "apply the reviewer's stated correction" (HQ's catch-all for TRUE WITH CORRECTION), unless HQ gave its own wording.

| ID | verdict | HQ disposition | Document § changed | Before → after |
|---|---|---|---|---|
| 04 | TWC | correction | M §2.1 L2 | Added: "With max ∅ = −∞: when Ŝ = ∅, g_sub = +∞ and the relative subset mass is 0." |
| 08 | GAP | Removing the numerical label needs validated arithmetic (SC) and VAL-FP; a long-double replay alone is not enough. | M §6 row 5, §2.1 header; N §2 dec. 10 | M §6: "gates … numerical label removal" → "removing the numerical label needs validated arithmetic (SC) **and** VAL-FP; a long-double replay alone is not enough". §2.1: "Until SC(η_F) is established by validated arithmetic" → "… and VAL-FP holds at production size". N dec. 10: "until validated arithmetic exists" → "until validated arithmetic (SC) and VAL-FP exist". |
| 09 | TWC | Distinguish an operational LS0 interruption (no output) from a completed capped search returning `local_limit` (L1 = n/a). | M §2 #6, #8, #10, §2.1 L1; T §1.A M2, M10, §3 N2(e); N §2 dec. 4 | "LS0 stop ⇒ no output" is now defined as an operational interruption. "An LS0 that stops on `local_limit` gives L1 = n/a" → "A completed LS0 that ends on its move cap (`local_limit`) gives L1 = n/a; output is still returned". |
| 14 | TWC | correction | M §2 #12; T §1.A M9, §2 A1 | "h measurable in (X, y, 𝓒), i.e. fixed before stream 10" → "… fixed before stream 10. An h defined from other calibration information is covered only if that information is included in 𝓒 before freezing (enlarge 𝓒 when necessary); streams-0–9 measurability need not imply measurability in the compressed 𝓒. No final-run selection." |
| 15 | TWC | correction | M §2 #11 | "Neither normalised estimate is unbiased" → "… is generally unbiased". |
| 16 | TWC | correction | M §5 row 18 | "stacking at N_e lowers variance ∝ 1/R′" → "exactly ∝ 1/R′ for the averaged evidence; for normalised PIPs and general h, an asymptotic (delta-method) rate under moment conditions, not finite-R monotonicity". |
| 18 | TWC | Rebuilds ≤ ℓ per tier (≤ 2ℓ with escalation); ratio 0.0512 + 0.2048·I for a single tier. | M §2 #18, #19, §5 row 15, "Points settled" 5; T §1.A M8, §2 D1, §3 N15, §6 E3; N §2 dec. 6, 7 | "≤ ℓ rebuilds" → "≤ ℓ rebuilds per tier (≤ 2ℓ with escalation)". "≈ (1 + 4I)H₀/(4N₀) ≈ 0.05 + 0.2·I" → "= 0.0512 + 0.2048·I (single tier); two tiers [H₀(1+4I₀)+H₁(1+4I₁)]/(4N₁); trajectory lengths only". The status "seat-derived, unchecked" is kept. |
| 19 | TWC | Depth counts sequential step slots, not seconds or scorer operations. | M §2 #19; T §2 D1, §3 N15 | "depth N_e(T+L+4)(p+B+2) per island" → "… sequential elementary-step slots at tier e (not scorer operations or seconds); score costs and finite-worker scheduling are added; R′ above the worker count runs in waves". "(1+I_e)·H₀" → "(1+I_e)·H_e". |
| 22 | TWC | correction | N §5 item 3; T §4.A I3 | "Masking of any product-of-blocks start" → "the product-of-blocks start …, under T27(i)'s hypotheses (H2, H3; verified on LH) … not every product start on every design". |
| 23 | TWC | correction | T §4.A I4 | "One-shot IS from π₀ needs ≈ Q*" → hypotheses restored (LH exact Gram, cancellation depth c, TL S2's discovery and IS losses, asymptotic Q/Q* regimes), plus "not a universal cost lower bound for arbitrary targets, summaries or one-shot algorithms". |
| 24 | TWC | = F11 | as F11 | as F11 |
| 25 | TWC | correction | N §5 item 7; T §4.A I6 | "565/2,400" → "565 strict competitor defeats among the 2,394 completed fits (six stops): at least 565 target-mode misses, not the exact count on all 2,400". |
| 26 | GAP | Drop the blanket "no useful upper bound on Z from the record" as an inherent limitation; state only what T31(c) and PC1 claim 1 prove. | N §5 item 5 and Not-inherent list; M §2 #21(ii); T §1.A M14(ii), §3 N17 cell, §4.A I7, §4.B; S | "No useful upper bound on Z from the run's record alone" → "T31(c) (PROVED-LOCKED; PC2 C1(c)): positivity and unbiasedness of Ẑ alone yield no upper bound on Z (a non-implication, not a data-specific impossibility)" plus "PC1 claim 1's analytic bound exists". The blanket wording is listed as withdrawn under "Not inherent". See Q7 on the T31(c) paraphrase. |
| 27 | FALSE | Remove "≈ ν log(n+1) / ≈ 530 nats loose" as a universal looseness. | N §5 item 5; M §2 #21(ii); T §3 N17 | "loose by ≈ ν log(n+1) nats" / "≈ 530 nats loose at n = 200" → "its gap to Z is data-dependent; the figure compares against m(∅), not Z" (T N17 adds the review's n = 200, p = 1 example, tagged). |
| 28 | TWC | Markov: "sharper bounds need information beyond positivity and the mean" (not "a variance hypothesis"). | N §5 item 6; T §1.A M14(iii), §4.B (I8) | "Anything sharper needs a variance hypothesis" → "Sharper bounds need information beyond positivity and the mean (not necessarily a variance hypothesis)". The re-check moved I8 (see F06 and Q1). |
| 30 | TWC | correction | T §4.A I9(g) | "without a bound on unscored mass" → "without excluding better unscored scores, by a maximum-score envelope or a sufficient mass bound". |
| 33 | TWC | correction | M §5 row 21 | "n ≥ 22: p ≤ 17" → "n ≥ 22: every p ≤ 17 is exact (uniform sufficient range; the maximum for n ≤ 2,500; larger n can admit more, e.g. n = 3,000, p = 18)". |
| 35 | TWC | correction | M §2 #25, §5 row 5; T §1.A M12, §3 N12; N §4 e3 | Added: "n = 2 is a proposed extension: current preprocessing still rejects n < 3 and raw p = 0 (`v3_preprocess.R:103–107`)". |
| 36 | TWC | correction | M §2 #32 (w3), §5 row 24 | "r_n ≥ 1 (p > e^{n/2})" → "r_n ≥ 1 (equivalently p ≥ e^{n/2}; equality impossible for positive integers, so p > e^{n/2}) … for p > 1". |
| 39 | TWC | correction | M §5 row 44 | "⇒ p ≲ 1.8·10⁴ at 8 GiB" → "setup component alone ⇒ p ≤ [−n + √(n² + 4·8·2³⁰/24)]/2 (18,818 at n = 200; 11,398 at n = 20,000); excludes other allocations and workers; not a feasible-fit threshold". |
| 40 | FALSE | N₀ = max(n, p) ⇒ Θ(p·max(n, p)) steps per stage; Θ(p²) only when n = O(p). | M §5 row 14, §5.1 (p ≫ n costs) | "⇒ Θ(p²) work per stage" → "⇒ Θ(p·max(n, p)) move steps per stage, Θ(p²) only when n = O(p); score-size costs extra". |
| 41 | GAP | = F08 | as F08 | as F08 |
| 42 | FALSE | Local-search scan size p + k*(p − k*), k* = min(K, ⌊p/2⌋), per scan, times (ℓ + 1). | M §1 (row §8.1–8.5); T §5 row 12 | "unchanged as formulas" → "except §8.5's bound p + K(p − K) → p + k*(p − k*) per scan, k* = min(K, ⌊p/2⌋), × (ℓ + 1)". T: "(ℓ+1)(p + K(p−K))" → "(ℓ+1)(p + k*(p − k*))". |
| 43 | FALSE | The IG(0.01, 0.01) effect is not uniformly negligible; it needs residual-scale assumptions. | M §5 row 2 | "vanishes relative to the gap" → "not uniformly negligible relative to the gap (nearly collinear example, tagged); negligibility needs residual-scale assumptions". |
| 44 | GAP | Correlation-scale and η-crossing wording. | M §2 #30 (w1), §5 row 36; N §4 e2 | "The two agree only under p ≤ n^A" → "agree (up to constants) only when log p = Θ(log n); p ≤ n^A alone is not enough". "falls below scorer error for n ≳ 10³" → "can fall below scorer error at large n; η depends on k, Q and conditioning, not on n alone; a crossing needs a specified design and model". |
| 46 | FALSE | "dominant practical storage limit" | M §5 row 49 | "the only hard size limit of v3.1" → "the dominant practical storage limit; integer, stream and allocation ranges and checked-arithmetic rejection are also hard implementation limits". |
| 53 | FALSE | = F12 | A §3 | 74 → 76 |
| 54 | GAP | = F05 | as F05 | as F05 |
| 55 | GAP | Withdraw "headline gain capped at 6/2,400". **Decision 1 unchanged** on its remaining reasons. Record the backfit start as future work. | N §2 dec. 1; M §4 (backfit row); T §5 row 4 | "…and its headline gain is capped at 6/2,400 (API-RESID §4)" → "no exact sampler with a known normaliser was exhibited for it (why arm D was dropped), so Ẑ unbiasedness is not available; the 6/2,400 rationale is withdrawn (a changed start does not nest scored sets); recorded as future work". Ground-rule references are unchanged (Q2). |
| 56 | FALSE | Replace "would break the frozen-𝓒 contract" (HQ text). | M §4 (certificate-feedback row) | "It would make 𝓒 depend on the certificate and break the frozen-𝓒 contract" → "POST HOC is the adopted policy; a certificate computed only during calibration could in principle be frozen into an enlarged 𝓒, while feedback from final-run information would break the contract". |
| 57 | TWC | = F07 (+ F13) | N §2 dec. 10; T header | as F07, F13 |
| 59 | TWC | correction | N §1; M §0; T §3 N2 (Supports) | "stands as v3.1 at R′ = 4" → "saved sampler estimates stand as v3.1, reusable with stated reporting limitations; full v3.1 records not yet produced (LS0 integration and flags, NA interface, certificates, primary rescoring pending; no statistical refit needed)". |

## 3. SOL1 findings with no change

- **TRUE (26), no change:** 01, 02, 03, 05, 06, 07, 10, 11, 12, 13, 17, 20, 21, 29, 31, 32, 34, 37, 38, 45, 47, 48, 49, 50, 51, 52. Some text near 51 and 52 was reworded under F04, F05 and F10. The counts those findings verified are unchanged.
- **UNCHECKABLE, no change:**
  - **58:** the documents already keep the recorded hypotheses, candidate statuses and GAP/OPEN labels.
  - **60:** HQ gave no disposition (Q4). Only the read-chronology part is touched, through F10's narrower timing and the A §1 note "git establishes filing order, not reading time".

## 4. Consistency check after editing (N, M, T, S)

| Point | N | M | T | S |
|---|---|---|---|---|
| N9 is a closure gate; "none, conditional on N9 (running)"; reopens before the theorem meeting | §9 | header | header; §3 N9 | yes |
| Binding-goal escalation (N1/§13.1, S4/§5.3, N9/§5.1) | §5, §9 | header | §2 A1, S4; §3 N1, N9; §4.B; §5 | yes |
| C6 union trigger; neither fires (island-level depth only; p ≤ 1,000) | dec. 6; §7 #10; §9 | §2 #19; §3 C6; §5 row 14 | M13 | yes |
| Item-1 certified count: C 10/12; A and B 0 | §3 | §2 row 0 | §1.B | yes |
| Inherent list = PROVED or by definition only. Markov sharpness and blanket "no useful upper bound" moved to "Not inherent" | §5 (items 5, 6; Not-inherent list) | #21(ii) restated; no separate list | §4.A (I7 narrowed; I8 moved); §4.B | yes |

Every other remaining item in the inherent lists was re-checked:
- I1, I2, I9 and I11 are true by definition.
- I3 is PROVED-LOCKED, conditional.
- I4 is PROVED, with its hypotheses now restored.
- I5 is PROVED.
- I6 is N200 PROVED plus a data fact.
- I7 is T31(c), PROVED-LOCKED.
- I10 is PROVED (candidate).

MINUTES items 1–5 and 7–9 map onto these.

## 5. Questions for HQ

1. **Markov sharpness (I8; MINUTES §5 item 6).**
   - F06 says to restore "seat-derived, unchecked" at I8.
   - The #26–28 rule says to move anything that is not PROVED or by definition out of the inherent list.
   - I applied both: the item is qualified **and** moved to "Not inherent". MINUTES item 6 keeps its number as a "moved" note, so item numbers stay stable.
   - Should it go back into the inherent list once a proof check covers it, or do you want it treated as classical and kept in place?
2. **Decision 1 ground rules.** Your disposition lists "ground rules 1 and 5" as the remaining reasons. MINUTES cites "1, 5 and 7" (keeping the block start) and M §4 cites "1, 5, 8" (rejecting backfit). I replaced only the withdrawn 6/2,400 clause and kept the recorded ground-rule numbers. Should they be harmonised?
3. **Other binding-goal mappings (F02).** I applied the escalation branch to N1 (§13.1), S4 (§5.3) and N9 (§5.1). I did not add it to these:
   - **§5.2 → V1.** Its open hypotheses are GUARD-W (N2(e)) and IND-T for streams 10..9+R′ (N14(c)). Their failure branch is an engineering fix, after which the goal is still met.
   - **§5.4 → S1/S2.** S2's Lemma KL is a PROOF SKETCH with no recorded failure branch, and it is not a §3 obligation.

   Should Lemma KL, or any of these, carry the escalation branch?
4. **SOL1 #60 (UNCHECKABLE).** The documents contain historical narrative that the record cannot verify: job-kill causes, CPU durations of the unfinished fits, spend, and who read results when. HQ gave no disposition, and nothing was changed beyond F10. Do you want an "unverified narrative" label on these?
5. **SOL1 #58 (UNCHECKABLE).** No change was made, because the imported TL conclusions already keep their recorded statuses and hypotheses. Please confirm that nothing further is wanted.
6. **F04: proportional vs absolute gate.** v2's need = max(9, ⌈0.75·complete⌉) means the absolute 9-design gate always binds for ≤ 12 designs. The proportional-completion sentence (T §1.B; SYNTH_R3:57) therefore never raises the requirement. T now says the absolute gate is "kept alongside" that sentence. Please confirm that this is the intended settlement.
7. **T31(c) wording.** The locked T31(c) text is not in this worktree. I stated it as "positivity and unbiasedness of Ẑ alone yield no upper bound on Z (a non-implication from the estimator's law, not a data-specific impossibility)", following SOL1 #26 and PC2 C1(c) ("no lower bound from unbiasedness"). Please check this paraphrase against the locked statement (collected proofs 4590ff) before it is printed.

## HQ answers to the editor's questions (2026-11-04)

1. **Markov sharpness (I8):** keep it moved to "Not inherent" with the "seat-derived, unchecked" label. The theorem meeting may restore it after a proof check (the two-point-law sharpness is classical, but it is not on record as checked).
2. **Decision 1 ground-rule numbers:** leave as recorded in each document (MINUTES 1, 5, 7; METHOD §4 1, 5, 8); both sets are correct in context.
3. **Other binding-goal mappings:** agreed: no escalation branch for §5.2 → V1 (its open items fail into engineering fixes) or for Lemma KL. Proposal §5.4 coverage is an agenda item of the theorem meeting (MEET-THM dossier §6 item 5).
4. **SOL1 #60:** the run-history narrative (job-kill causes, CPU durations, spend, who read which result when) is the chair's and HQ's record, not an independently verifiable log; this note is the label.
5. **SOL1 #58:** confirmed, no further change.
6. **F04 gate:** yes, that is the intended settlement.
7. **T31(c):** checked by HQ against the locked text (`origin/theory/T38-RECORD:Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex`, T31 conclusions (a)–(d), ≈ lines 4575–4600). The paraphrase was replaced everywhere by the locked content: "the properties of Ẑ behind the 95% bound (positive, finitely many values, mean Z, iid islands) imply no two-sided relative-error bound: for every c₀ > 0 and η ∈ (0, 1) some such law has P(Ẑ < c₀Z) ≥ 1 − η, so {Z ≥ αẐ} places no upper limit on Z/Ẑ". It remains a non-implication, not a data-specific impossibility (the locked text itself notes that for fixed data Ẑ lies surely within e^{±Δ}Z for a data-dependent Δ that is not reported).
