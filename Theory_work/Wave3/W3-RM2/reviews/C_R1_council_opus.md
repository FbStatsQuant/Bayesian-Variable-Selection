# W3-RM2 — council round R1, seat `opus` (Claude Opus 5.5, effort high) — blind first read

Reviewed content: `MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a`. I re-hashed every entry of
`reviews/MANIFEST_R1.txt` (ticket files and the 28 `EXT:` inputs) against the worktree with `sha256sum -c`: all match.
I read only manifest files and `reviews/INPUTS.txt`; no other file under `reviews/`, no `LOG.md`, no `CHECKPOINT*.md`.
I re-ran a copy of `citecheck.py` that writes to a scratch directory, not to `reviews/`: 92 citations, 0 MISS.
I checked the code pins against `Scripts/SMC_BVS/core/cpp/v3_core.cpp:394-404, 465-476` and
`v3_engine.h:385-418`: centre = `start_mode(...).S`; cap = `ls0_ell + |m.S|`; flips with `|C| < K` and swaps are
scanned; a move needs a strict improvement; ties go lexicographic; there are the certified and `move_limit`
branches. All match STATEMENT §1.

## 1. Gate verdicts

**G1 Correctness — PASS.** I re-derived every new step and found no false step.
* L0 Toolkit-b. Checked: the BB(1, p) prior identity w(k) = 1/(2·binom(2p−1, k)), `L0_toolkit_b.md:25`; the χ²
  Markov bound with t_n, `:82-84`; (E1), whose D_A factorisation gives (n+1)(1 − x_i), `:98-100`; and the (T5)(a)–(c)
  constants, `:118-124`.
* L1. The ladder exponent and geometric sum are correct (`L1_sandF_b.md:106-115`; ε₂ ≥ ε₁ because ϑ″_n ≥ 0). So is
  the junk-exclusion arithmetic down to [β(η, A) − b] log n (`:142-148`).
* L2.
  * NA-W (`L2_width.md:77-90`): s_n ≤ min level follows from Φ⁰ ≥ −a_min, and Z² ≤ a² − (3/4)as_n follows from it.
  * W-conv (`:100-109`): the ¼as_n margin closes against 1 + log 2 + 2κ_E.
  * (3.1) (`:134-148`): the Cauchy–Schwarz split with range(P_{Q_l} − P_T) ⊆ range(P_Q − P_{S₀}) holds.
  * (W-ref) ⇒ (W-unif) (`:151-163`): 1 − 2b − 2δ = 2h + 2δ, and the radicand is ≤ (2A + 1) log n.
  * (W-loc) ⇒ (W-ref) (`:166-180`): the atom bound is L_n/φ₀ because ‖x_t‖ = √(n − 1) and ‖a‖ ≥ φ₀√(n − 1).
  * TL-W: identity (4.1) is exact (`:204-209`), and it is cleanly the reason (BM-Q) can be weakened to (BM-W).
* L4 (new mathematics).
  * The product-form identity (★) (`L4_sandR_b.md:116-120`) is correct. S₀ ⊆ H_l gives S₀ ∖ U₀ = S₀ ∖ U, and V
    contains no truth. The leak bound is used at U₀ and at U.
  * The sample perturbation is O(h_n(r_n + h_n)) (`:123-133`).
  * Lemma 3 (`:150-177`). Conditioning on σ(W_D, ε) is legitimate: e ⊥ (W_D, ε), Y uses only W_{S₀} and ε, and the
    ratio bound with κ = 4/√c and the exponent with the mean shift both check.
  * Lemma 4, (4.2), (4.3) and the ladder (`:183-222`) hold. In particular t_n(k) ≥ ½ log n, T_n ≤ (2A + 1) log n, and
    there are at most log₂ n rungs.
  * 6(b) closes at ε*/2 (`:236-240`).
* L5.
  * (S2) is where b < ½ is used (`L5_formR.md:20-23`).
  * P8 conditions on a W-event with deterministic envelopes (`:33-46`).
  * P9a Step 4: ϵ_n = O((q + log n)/√n) (`:82-85`). E_e is correct as a law of 𝒲a given ε.
  * P9: the "probability ≥ ½ vs lower tail" argument closes (`:96-105`).
  * P10 at p = 1: D_A = n and Q_A = (n − 1)(1 − r̂²(n − 1)/n) are correct (`:126-133`).
* L6. E4's regression identity and E5's v_t, A_t and (5.1) are correct. The (5.2) comparison gives exactly b < 3/10
  (`L6_examples.md:417-462`).

**G2 Hypotheses used = stated — PASS.**
* L1 §0, L4 §7 item 5 and the L3/L5 assembly lines map every hypothesis of (C1)/(C2) to its single use:
  * (T1-F)/(T1-R) only for [POST] and the energy/size components;
  * (FL-Q) / (FL-R) on Q ∪ {l} for the lattice;
  * (L-feas) for feasibility;
  * (BM-W) only in TL-W.
* Nothing used is unstated. The two "automatic" items in Form R (energy, (BM-W)) are derived from fixed θ_lo, θ_hi and
  b < 1 (`L5_formR.md:18-26`), not assumed silently.

**G3 No hidden assumptions — PASS.**
* Partition: Form F uses only "a deterministic function of the fixed X, blocks ≤ 16" (`L1_sandF_b.md:24`). Form R
  uses only "measurable in W" (`L4_sandR_b.md:25`). The count J(t) is partition-free, and the random partition never
  enters a probability statement (`:272-274`).
* Every probabilistic statement is for deterministic (l, U₀) or is uniform on E_cov.
* Uniformity over maximisers is explicit in L1 §3 and L4 §6.
* n₀ dependence is tracked, including the envelope substitution in P8 (`L5_formR.md:37-38`).

**G4 Statuses — PASS.**
* STATEMENT §5 (`STATEMENT.md:292-310`) quotes the below-PROVED-CHECKED inputs verbatim and carries them:
  * (C1) is conditional on SOP:TH09@1.0.0;
  * (C2) is conditional on W2-APP:POST@1.0.1;
  * E2/E3 are conditional on Lemma-BC and Lemma-IR.
* W3-RM:B9 and W1-GEN:L1 are no longer consumed, with reasons (`L5_formR.md` §3; `L0_toolkit_b.md:7-11`).
* Every new lemma has a blind cross-family check on file per REPORT §3 (`REPORT.md:64-84`).
* No status is upgraded. Every row reads "PROVED (by this seat, unchecked)" + check record (`REPORT.md:36-38, 85`).
* Defect: the registry block's `status_source` line pointers are all wrong (F1). The status texts themselves are
  right, so this is a records defect, not an upgrade.

**G5 Constants and rates — PASS.**
* β(η, A) is carried consistently from the margin (`L1_sandF_b.md:144-148`) to STATEMENT `:35, :74-75, :114`.
* The ε* budget 15ρ + b < ½ carries from `L4_sandR_b.md:194-196, 238-240` to STATEMENT `:116, :184`.
* exp(−s²/8) and n^{−c*} with c* = δ₀²/(32(2A + 2)) are carried from L2 `:72-90` to STATEMENT (C3)(a).
* The δ-gaps √log n/(2√(2A + 2)) and (2A + 4) appear in both the statement and the proofs.
* The (W-ref) δ = (1 − 2b − 2h)/4 and the atom bound L_n/φ₀ match. The Form R mean-shift cost exp(C√(n log n)ϖ_n)
  is tracked to n^{o(1)}.
* Small wording slips only (F7).

**G6 Fidelity and program — PASS.**
* (C1)–(C4) contain no design family; families appear only in (C5)/L6, with their own statuses.
* Form F is partition-free with a block-relative variant; Form R allows any X-measurable partition.
* The code facts are pinned and correct.
* (W) is honestly presented: sufficient when the gap → −∞; a route obstruction when the gap → +∞; a bounded gap
  undetermined; no necessity for Ŝ⁺ = S₀ is claimed (`STATEMENT.md:40-41, 226-230, 320-322`; `SHARPNESS.md:53-56`;
  REPORT flag 1).
* The numerics are labelled as the LS0 re-implementation from the start mode, with nominal classification. Sampler,
  posterior and full method are untested (`numerics/RESULTS.md:7-10, 106-118`; STATEMENT `:286-288`).
* The record wording issues below do not amount to an overclaim.

## 2. Score: **8.8 / 10**

Deductions:
* **−0.4** registry block: every `status_source` pointer is off by four lines and points at the wrong clause (F1). The
  block is meant to be machine-ingested.
* **−0.3** strength, not correctness. The headline still needs (W), an abstract Gaussian-width condition on (X, Q).
  Its primitive forms reach strongly correlated polynomial groups only partially: the equicorrelated group is verified
  for b < 3/10, and by W-conv the route itself is likely obstructed beyond b ≈ 3/8 (O4′). The theorem is a clean
  strict extension of RM, not yet "(V) + (L^b)" alone.
* **−0.2** small cross-record inconsistencies (F2–F5, F10): table break, stale gate pointer, "median–mean" vs the proof,
  a stale equation number, and Lemma-BC with no version in one place and a version in another.
* **−0.2** imprecise wording in the sharpness record and the statement (F7, F11) and NITs (F6, F8, F9).
* **−0.1** no Form F example at p ≫ n with genuinely polynomial |Q| (E4, E5 have p = ⌊n/3⌋). That regime is covered
  only by Form R (E2). Not claimed otherwise; noted for the paper.

## 3. Findings

**No finding is REQUIRED for the council pass.** F1 is REQUIRED before registry ingest (HQ acceptance): it is a
mechanical fix but must not reach `claims.tsv` as is.

* **F1 — MINOR (records; REQUIRED before ingest).** `REPORT.md:162-234`. Every `status_source: REPORT.md:NN` points
  four lines too high. The §3 rows are at `REPORT.md:66-83`.
  * RM2-F → `:68` is the NA-W row (should be `:72`).
  * RM2-R → `:74` is the (P7) row (should be `:78`).
  * Toolkit-b `:62`→`:66`, SAND-F-b `:63`→`:67`, NA-W `:64`→`:68`, W-conv `:65`→`:69`, W-suff `:66`→`:70`,
    TL-F-b `:67`→`:71`, Cont-F `:69`→`:73`, SAND-R-b `:70`→`:74`, F-to-R `:71`→`:75`, D-to-W `:72`→`:76`,
    POST-R `:73`→`:77`, Cont-R `:75`→`:79`, Ex-PolyR `:76`→`:80`, Ex-PolyF `:77`→`:81`, Ex-Proxy `:78`→`:82`,
    Ex-Equi `:79`→`:83`.
  * `citecheck.py` cannot catch this, because it checks ranges only.
  * Fix: renumber, or cite the rows by clause id. Add a check in citecheck that `status_source` lines contain the
    claim's clause id.
* **F2 — MINOR (records).** `REPORT.md:102`. The "Dispositions: …" line sits inside the §4 table, so the rows RC5,
  SW1 and BT2 (`:103-105`) render outside it. The list also omits `SW1_disposition.md` and `BT2_disposition.md`. Fix:
  move the line below the table and complete the list.
* **F3 — MINOR (records).** `REPORT.md:170, 182`. `better:PENDING(reviews/BT1_better_theorem_astra.md)` cites the
  better-theorem review of v1.2. The review of the final statement v1.4 is BT2 (`REPORT.md:105`). Fix: cite BT2
  (BT1 optionally as well).
* **F4 — NIT.** `ASSUMPTION_MAP.md:27`. "P1: ladder (3.3)" — `L1_sandF_b.md` has no (3.3). The ladder is (2.2)–(2.3)
  and junk exclusion is Step 2(b). Fix the reference.
* **F5 — NIT.** `STATEMENT.md:256` ((P9) row: "median–mean for a Lipschitz functional") and `ASSUMPTION_MAP.md:34`
  ("a median–mean bound") disagree with the proof. `L5_formR.md:105-106` uses only lower-tail concentration about the
  mean ("no median bound is quoted"). Fix: "a probability-≥ ½ event plus lower-tail concentration about the mean".
* **F6 — NIT.** `L2_width.md:7` and `L3_assemblyF.md:7` cite "STATEMENT.md v1.3". It is now v1.4. Form F is unchanged,
  so this is harmless; update the header.
* **F7 — MINOR (sharpness wording).** `SHARPNESS.md:12` ("b enters each proof at exactly one line") and
  `REPORT.md:120` ("enters one line of each proof"). Strictly, Form R uses b < ½ in two further places, and both also
  break at b = ½: the sample floors on Q ∪ {l} (`L5_formR.md:22`) and P9a Step 4 (`:84-85`). The same SHARPNESS bullet
  lists them, so the lead sentence contradicts its own bullet. The registry's `A:L-size-b-R = ARTEFACT` cites only
  `L4 §6(b)` (`REPORT.md:180`). Fix: "the junk-exclusion margin is the only place where b is paid in the sandwich; in
  Form R b < ½ is also used by (S2) and P9a". Add those two to the evidence field.
* **F8 — NIT.** `L4_sandR_b.md:107` reuses ϑ_n for √n·ζ_n, while ϑ_n is the toolkit's likelihood-ratio slack
  (`L0_toolkit_b.md:38`). The two never meet in one display, but rename one (e.g. ϑ̃_n).
* **F9 — NIT.** `L1_sandF_b.md:129-130` and `L4_sandR_b.md:233-234` say "the right side is positive". What must be
  positive is the whole score difference: (½M_n log n − σ²z_n²)/(2C_R) − log(2p) − ½ log(n+1) − 2κ_E, and
  respectively with Na₀²/8. True for n ≥ n₀; state it that way.
* **F10 — NIT.** `STATEMENT.md:307` lists "W2-LOC2:Lemma-BC (LOC2 `lemmas/L6_poly.md:78-109`)" without a version.
  `REPORT.md:225, 228` writes "W2-LOC2:Lemma-BC@1.0.0". Harmonise the id@version (PROTOCOL rule 11).
* **F11 — NIT.** `STATEMENT.md:213`: "(the old cap `ell_n` is not covered beyond (W-χ))" implicitly asserts coverage
  under (W-χ), which no file of this ticket derives (`L3_assemblyF.md:55-56` explicitly does not). It is a one-liner:
  under (W-χ), |S̃₀ ∖ S₀| ≤ (1 − δ₁) log n < ℓ_n, then GROW L1.2 applies with cap ℓ_n. Fix: add that line to L3, or
  rephrase as "covered only by RM-F's remark under (N-χ)".
* **F12 — observation (no change required).** Form F examples at genuinely polynomial |Q| (E3–E5) all have p < n. The
  p ≫ n polynomial regime is exhibited only in Form R (E2). PLAN §4 records this; the paper should say it next to
  (C5).

## 4. Fitness to replace the parent's Theorem 3; most valuable missing strengthening

Yes. As stated in v1.4, RM2-F/RM2-R are fit to replace W3-RM's Theorem 3 as the paper's main reported-model theorem.
* They contain RM-F/RM-R at the level of hypotheses and conclusions (`L3_assemblyF.md:40-56`, `L5_formR.md:151-160`;
  re-checked).
* They keep exactly the same pathwise, common-good-event conclusion through the unchanged core RM-0.
* They move the leak set from polylogarithmic to n^b for every b < β(η, A) (b < ½ at η = 0). In Form R they also
  remove two artefacts of the parent: the n^{−1/2} leak scale and the localisation rate. This drops the polynomial-decay
  cutoff from α > 17/2 to α > 2.
* The mathematics is correct and the conditional statuses (SOP:TH09, W2-APP:POST, Lemma-BC/IR for E2/E3) are carried.

For the paper's headline I recommend stating the theorem with (W) and immediately giving the primitive form (W-loc) /
(D-loc^b), so that no reader takes (W) for a hidden assumption.

The single most valuable strengthening still missing is **O1: replacing whole-lattice no-addition by no-addition
along the realised deletion path** (path-level control of LS0 with cap accounting). This would remove (W) altogether.
Lemma W-conv shows that (W) is forced as long as the whole lattice is used, and the equicorrelated design (O4′:
threshold ≈ 3/8, sketched) is a natural instance where the route fails but nothing suggests the conclusion does.
Settling O4′ rigorously first would give the cleanest motivation and test case for that ticket.

COUNCIL-VERDICT round=R1 manifest=00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a seat=opus score=8.8 gates=PASS
