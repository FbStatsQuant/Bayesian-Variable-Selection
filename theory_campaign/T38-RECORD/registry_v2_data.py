# -*- coding: utf-8 -*-
"""Registry v2 overlay (T38-RECORD).

Loads the S-REGISTRY rows unchanged (`registry_data.py`, a verbatim copy of theory/S-REGISTRY @ 3d88da6). Then it
1. annotates existing rows with later evidence: verdicts, data, superseding statements, review state;
2. adds rows for every branch that landed after the registry was built.

Rules (as in S-REGISTRY):
- the author status word `st` is copied from the source and is NEVER raised;
- a later SAME-family verdict is entered only in `sf`, and a CROSS-family verdict only in `cf`;
- conflicts are flagged, not resolved.

Text processing only.
"""
import registry_data as D  # noqa: F401  (verbatim S-REGISTRY rows)
from registry_data import ROWS, IMPL, RETIRED, r, upd, claim, N

# ===================================================================================================================
# 1. Annotations of existing rows
# ===================================================================================================================

# ---- Thm 5 (T38): the statement of record moves to T38-RECORD v3 --------------------------------------------------
upd("T38-(0)", rep="W6-FIXREV1 T38_STATEMENT (v2) applies A-REV1 §7 (execution, usability, K); carried into "
    "T38-RECORD v3. Same family; not re-reviewed (A-REV5 pending)", rs="applied")
upd("T38-b1′", rep="W6-FIXREV1 Cor. D2-∞ with rate margins (v2); masked instances: B2E-D2LH (LH exact Gram, c = 1) "
    "and VMASK-R1-NB (LH-iid, c = 1), both author or single run; A-REV7 pending", rs="applied")
upd("T38-b2", rep="W6-FIXREV1 eligible set 𝔛_n, repair certificates, capped β_H, boundary 𝔉_T (v2). DELIV stays OPEN "
    "in general; LH candidates FSH-F2, B2E-B2LH, OBG-BG3+OBG-LH-lock; A-REV7 pending", rs="applied")
upd("T38-b1-LH", prem="LH exact Gram (p ≤ n−1), |ψ|<ρ, g ≤ B < 2g; LS0, now PART OF THE METHOD (approval in effect: "
    "O-LS0 0/2,394 HPM changes). Search step re-proved by SEP-CorGULH (W7-SEP, candidate)")
upd("Cost-T38", prem="T32(i): PROVED by W5-LOCKBOOK; re-counted by W7-SEC (no error; same family). W6-FIXREV1 "
    "(dependency k1) and W7-SEP (input I11) still say CONJECTURE: stale", flags="CONFLICT")
upd("T32(i)", sf="V|W7-SEC · REPORT.md T32(i): 'independently re-checked here, no error in the count' "
    "(267,610,872,968 at (200, 500)); harmless slip in W5's corollary proof (1 + 4ℓ ≥ 5ℓ false for ℓ ≥ 2; "
    "conclusion stands)", flags="CONFLICT")
upd("W6F1-T38", cf="N|not yet reviewed: A-REV5 (sources pinned incl. W6-FIXREV1, W4-T38FULL) had pushed no verdict "
    "at the T38-RECORD fetch", rep="superseded as statement of record by T38-RECORD · T38_STATEMENT.md v3 "
    "(citations, review columns and candidate list only; no change of mathematics)")

# ---- O-BGIBBS: the registry read an earlier head (BG1 headline; §4.1 to be filled) ---------------------------------
upd("OBG-final-run", rep="superseded at head 55679ee on LH (p fixed) by OBG-BG3 + OBG-LH-lock: the final run alone, "
    "terminal rounds, no temperature condition (composite PROOF SKETCH). The OPEN status stays for the BG1-type "
    "bridge-stage route; §4.1 is now filled (c = 2 scored in pilot round 1 in 160/160 replicates)")

# ---- W3-PGD: REPORT.md is final now (head fdeaec3) ----------------------------------------------------------------
upd("ThmW", src="W3-PGD · REPORT.md §2 (final, head fdeaec3) + PROOF.md §4 · Theorem W")

# ---- O-CERT rows: same-family referee O-VCERT (839bed5) ------------------------------------------------------------
VC = "O-VCERT · REPORT.md §1, §6"
upd("OCERT-LemmaM", sf="V|" + VC + ": (a)–(d) VERIFIED (0 violations in 476,160 exhaustive pairs)")
upd("OCERT-C1", sf="V*|" + VC + ": (a), (b) identity and probability VERIFIED (conditional on W2-BOOK Lemma "
    "RO/GUARD); last sentence ('unscored and unreported' mass) GAP with a counterexample, repaired by R1 "
    "('not in 𝒯')", rep="O-VCERT R1 (written by the referee; O-CERT's text not edited)", rs="applied")
upd("OCERT-C2", sf="V|" + VC + ": VERIFIED as a conditional implication (PW2); Cantelli bound tight")
upd("OCERT-C3", sf="V|" + VC + ": VERIFIED (𝒮̄ read as the SR logical scored set; code-checked)")
upd("OCERT-C4", sf="V|" + VC + ": VERIFIED (0 violations over 285,712 boxes on 48 designs; B&B = brute force 80/80)")
upd("OCERT-C5", sf="V*|" + VC + ": VERIFIED with tie caveat (needs F(S₀) < F(Ŝ) strictly or tie order) and |S₀| ≤ K")
upd("OCERT-C6", sf="V*|" + VC + ": GAP → VERIFIED after R1 and R2 (exact arithmetic needs R1 only); O-CERT later "
    "added Remark C6′ (deterministic regime, PROVED, head 332bf3e, unreviewed)",
    rep="O-VCERT R1 (unscored → not in 𝒯) and R2 (floating-point inflation of the G items)", rs="applied")
claim("OCERT-§4", "OCERT-C6 (illustration)", "O-CERT · REPORT.md §4 (p = 500 illustration)",
      "G|" + VC + ": §4 empty and results/ absent at 17e7f15; 'every numeric claim of O-CERT … is therefore "
      "unsupported' (S4)", "N|none",
      "O-CERT 0edc58f/332bf3e added an illustration on 4 study fits AFTER O-VCERT's review; not re-reviewed",
      "applied", "The certificate numbers had no committed support when reviewed; a later illustration exists, unreviewed.",
      flags="CONFLICT")

# ---- W5-FAVIID: REPORT complete at head 31695b1 --------------------------------------------------------------------
upd("FAV-ThmA", src="W5-FAVIID · REPORT.md §1 (complete at head 31695b1) + PROOF.md · Theorem A")

# ---- Lemma 0(b): S-ELS supplies the per-fit data the registry marked OPEN --------------------------------------------
upd("Lemma0(b)", prem="S-ELS (PROD-H ledgers): all 541 unrepaired centres are forced by Lemma 0, and the final "
    "local search made 0 moves in 2,394/2,394 completed fits. True on the study data; false as a general logical "
    "claim (CEX-2). W3-VT37R's 233/234 refers to sampled centres on regenerated data (rerun on PROD-H: W8-SYNTH task 3)")

# ===================================================================================================================
# 2. New rows
# ===================================================================================================================

# ---- O-BGIBBS (head 55679ee): BG2, BG1′, LH-rate, BG3, LH-lock -----------------------------------------------------
OB = "O-BGIBBS · REPORT.md"
for pid, lab, st, prem, mean in [
    ("OBG-BG2", "§2 · Theorem BG2 (cumulative scoring hazard)", "PROVED",
     "SR; predictable good sets with scoring probabilities β_t; stopped-count argument",
     "P(S₀ never scored by round t₁) ≤ P(Λ_{t₁} < Λ) + e^{−Λ}, where Λ_t = Σ m_sβ_s: discovery is a hazard, not survival."),
    ("OBG-BG1′", "§2 · Corollary BG1′ (temperature-dependent constant; final-run version)", "PROVED",
     "BG1's premises with β(φ); uniform-in-φ selection bound, no floor needed",
     "Covers the final run's stage 1 at any φ₁ᶠ: stage-1 discovery for c = 1, and for c = 2 with p fixed."),
    ("OBG-LH-rate", "§2 · Proposition LH-rate (scoring rate on LH, exact Gram)", "PROOF SKETCH",
     "𝔅_M part PROOF SKETCH; uniform-in-φ proxy part CONJECTURE (author)",
     "One round at φ from the start mode scores S₀ with probability ≍ P_c·min(1, e^{φc₂n−λ_n})^{c−1}, λ_n = log(2p√(n+1))."),
    ("OBG-BG3", "§2 · Theorem BG3 (locked start set + terminal downhill: the final run alone)", "PROVED",
     "deterministic given (L1) lock ε_𝒰 and (L2) terminal downhill β₁; data and 𝓒 fixed; no resampling in the "
     "L + 4 terminal rounds (v3_engine.h:352–373)",
     "P(z not scored in the island) ≤ Nπ₀(𝒰ᶜ) + N(T + L + 4)ε_𝒰 + exp{−N(L+4)β₁}."),
    ("OBG-LH-lockC1p", "§3.7 · (C1′), (C2′): start-table keep gaps on LH", "PROVED",
     "LH exact Gram, every parameter value", "The group table sees μ only through β_i(1−ψ_i²)x_{a_i}, so the block-table "
     "deletion and swap gaps at supersets of S° are positive in closed form."),
    ("OBG-LH-lock", "§2 · Proposition LH-lock (premises of BG3 on LH exact Gram, p fixed)", "PROOF SKETCH",
     "γ₁ gaps (C1)–(C3) as checkable design conditions: verified by exhaustive enumeration for the two simulated "
     "designs only (c = 2: 0.218, 0.030, 0.086; c = 3: 0.238, 0.051, 0.093); score-level reduction routine but "
     "unreviewed; order constant 1/m! crude", "w.p. → 1: π₀(𝒰ᶜ) ≤ e^{−c₃n}, ε_𝒰 ≤ m·e^{−c₃n}, β₁ ≥ (1 − o_P(1))/m!."),
    ("OBG-T38b-BG3", "§1 headline 1 · T38(b) without LS0 on LH exact Gram, p fixed, every fixed c (final run alone)",
     "PROOF SKETCH", "BG3 (PROVED) + LH-lock (PROOF SKETCH) + T38(0) + (P) via W1-EXP Thm 5(d); the composite carries "
     "the weakest input's word; author P(true) 0.9, P(provable) 0.8",
     "P(𝒪 ∩ {Ŝ ≠ S₀}) → 0 for v3 as run (no LS0) on LH with p fixed, every fixed c. Candidate N4 of T38 v3."),
    ("OBG-pinf", "§2, §7 · LH-lock for p → ∞ (exact Gram p ≍ n, or LH-iid)", "CONJECTURE",
     "uniformity of (C1)–(C3) over 2^{p−s₀} supersets; polynomial order constant", "The p-fixed argument extends to growing p."),
]:
    r(pid, "Thm 5 (b) without LS0 (new)", OB + " " + lab, st, "N|none (author only; A-REV7 pending)", N, "none", prem, mean)

# ---- F-SHARE REPORT (head 13bc665; the registry saw BRIEF only) -----------------------------------------------------
FS = "F-SHARE · REPORT.md §2"
for pid, lab, st, prem, mean in [
    ("FSH-F1", "Theorem F1 (closed-class delivery)", "PROVED", "EX-A, EX-S, CAL, KEEP(W, η)",
     "P(some particle is ever outside W | 𝓒) ≤ Nπ₀(Ω∖W) + N(T+L+4)η per island; on the complement DELIV(W) holds with every particle eligible."),
    ("FSH-L1.2", "Lemma 1.2 (exit bound for the superset class)", "PROVED", "W = W(S°)",
     "One-round exit from W(S°) is bounded by endpoint deletion odds, swap-out odds and π₀(Ω∖W)."),
    ("FSH-F3", "Corollary F3 (no C1 under KEEP)", "PROVED", "KEEP with Nπ₀(Ω∖W) + N(T+L+4)η → 0",
     "The W-count is N at every stage w.p. → 1; the D4 envelope for h = 1_W is ∏(1−η_s); the C1 mechanism cannot start."),
    ("FSH-L3.1", "Lemma 3.1 (unit structure, LH exact Gram)", "PROVED", "LH exact Gram",
     "Unit residuals depend on the state only through its intersection with the unit, and are orthogonal to other units."),
    ("FSH-L3.2", "Lemma 3.2 (hub gain)", "PROVED", "LH exact Gram", "δ²_{x,b} ≥ θ_b²(n−1)λ_min(Σ_LH) for x ∈ W(S°), b ∈ M∖x."),
    ("FSH-PK", "PK(d*) (population proxy-keep)", "CONJECTURE",
     "checked exactly for (ρ, ψ, g) = (0.7, 0.5, 4) at every proxy configuration; general |ψ| < ρ < 1 CONJECTURE",
     "A truth is kept at every proxy configuration."),
    ("FSH-L3.3", "Lemma 3.3 (start keep odds)", "PROVED-UNDER", "W1-EXP Thm 1 and PK",
     "κ₀(x, j) ≤ 2p e^{−c₁n} uniformly over x ∈ W(S°), j ∈ S°."),
    ("FSH-L3.4", "Lemma 3.4 (posterior keep and swap margins)", "PROOF SKETCH", "DOM for the truth-for-hub swap",
     "F(x) − F(x − j) ≥ c₂n and F(x) − F(x − j + l) ≥ c₂n uniformly over supersets."),
    ("FSH-F2", "Theorem F2 (LH exact Gram: DELIV(W(S°)) with all particles)", "PROOF SKETCH",
     "structure PROVED, Gaussian estimates PROOF SKETCH; p ≤ (1 − c₀)n, PK(g−1), DOM (DOM failed by +4.7 nats in one "
     "LH20 replicate at n = 1,600)", "π₀(Ω∖W), π(Ω∖W) ≤ Cpe^{−cn}; KEEP with η ≤ Cp²e^{−cn}; no particle ever leaves W w.p. → 1."),
    ("FSH-S4", "§4 scoring on W(S°) (REP)", "PROOF SKETCH", "CONJECTURE 4.3 (extras across resampling)",
     "S₀ is scored at the first stage with φ_t ≥ 2φ_hub by an extra-free particle, or in the terminal rounds."),
    ("FSH-C4.3", "CONJECTURE 4.3 (extras count across resampling)", "CONJECTURE", "—",
     "Re-weighting does not let extra-carrying particles accumulate across stages."),
    ("FSH-F1′", "Theorem F1′ (reversible leaks)", "CONJECTURE", "author: 'routine from D4'",
     "A class whose exits land in a less-fit set that returns w.p. ≥ 1 − η′ is still delivered."),
    ("FSH-F2iid", "CONJECTURE F2-iid (LH-iid, p ≫ n)", "CONJECTURE", "uniform null leakage over W_d",
     "DELIV(W_d) → 1 on LH-iid for every fixed d ≥ 1."),
    ("FSH-T38b2", "§8 · T38(b2) on LH exact Gram, no tweak, every fixed c (F2 + §4 + T38(0))", "PROOF SKETCH",
     "composite of PROOF SKETCH inputs (no separate status word in the source); author P(true) 0.85, P(provable) 0.5",
     "The Gibbs-path route with delivery by closure. Candidate N5 of T38 v3."),
]:
    r(pid, "Thm 5 (b2) delivery, no LS0 (new)", FS + " · " + lab, st, "N|none (author run; A-REV7 pending)", N, "none", prem, mean)

# ---- W7-SEP (head 858004e) -----------------------------------------------------------------------------------------
SP = "W7-SEP · REPORT.md §2 / PROOF.md"
SPT = "Thm 5 motivation / separation (new; spine)"
for pid, lab, st, prem, mean, fl in [
    ("SEP-A", "Theorem SEP (A) (iid start discovery)", "PROVED", "EX-A; LH (W1-EXP Thm 5(b), Lemma 4.2)",
     "Q iid π₀ draws score S₀ w.p. → 0 or → 1 according as Q/Q* → 0 or ∞, with the sharp Q* = p^c n^{c/2}.", ""),
    ("SEP-A-iid", "Theorem SEP (A) on LH-iid", "PROVED-UNDER", "W3-PXN P1, P4 (XF: P1, P4 VERIFIED by A-REV3)",
     "The same threshold on the p ≫ n family.", ""),
    ("SEP-B", "Theorem SEP (B) (one-shot importance correction)", "PROVED", "(A)'s plus locked T03 via W1-EXP Thm 5(d)",
     "1 + χ²(π‖π₀) ≥ Q*e^{−Mstat}(1+o_P(1)); below Q* the corrected estimator of π(S₀) is 0 w.p. → 1 while π(S₀) → 1.", ""),
    ("SEP-C", "Theorem SEP (C) (start + search)", "PROVED",
     "Prop. GU; uses W4-T38FULL Lemma M (same-family VERIFIED only)",
     "On LH, LS0 and 'one iid draw + local search' score S₀ w.p. → 1 at cost O(p² log n): no super-polynomial "
     "separation in the frozen setting, and none between the bridge and one greedy search.", ""),
    ("SEP-taska", "task clause (a): start-only + search fails", "COUNTEREXAMPLE", "LH; by proof (Cor. GU-LH) and in 386/386 replicates",
     "The task's claim that start-only methods with local search fail on LH is false.", ""),
    ("SEP-E", "Theorem SEP (E) (exponents, p ≍ n^a)", "PROVED-UNDER",
     "v3 row conditional on T32(i), which W7-SEP lists as CONJECTURE (input I11) although W5-LOCKBOOK proves it",
     "iid/IS need c(a+½) (sharp); LS0 ≤ 2a (+log); v3 with LS0 ≤ a + max(1, a); separation iid vs v3 iff c ≥ 2.", "CONFLICT"),
    ("SEP-BASIN", "Proposition BASIN (deterministic)", "PROVED", "—",
     "LS0 scores S₀ iff S̃₀ lies in the scoring basin 𝔅_ℓ; exact answer to when LS0 alone suffices.", ""),
    ("SEP-GU", "Proposition GU (greedy universality)", "PROVED",
     "G; exact Gram; isolated R ⊇ S₀ (Σ_{R,Rᶜ} = 0, |R| ≤ r); λ_min(Σ_R) ≥ φ₀²; fixed signals; p ≤ n^A; uses Lemma M",
     "W.p. → 1, from every C ⊆ R the production search reaches, scores and certifies S₀ within τ_GU moves; no PGD needed "
     "(a version of W1-T37R Conjecture C4).", ""),
    ("SEP-GU1", "Lemma GU-1 (population descent)", "PROVED", "—", "The best truth addition reduces Δ by ≥ (φ₀²/s₀)Δ.", ""),
    ("SEP-GU2", "Lemma GU-2 (supersets of S₀ inside R)", "PROVED", "—",
     "Every deletion of an extra gains ≥ ¼ log n; every addition or swap loses.", ""),
    ("SEP-CorGULH", "Corollary GU-LH", "PROVED", "LH exact Gram",
     "On LH every C ⊆ R is in the basin: re-proves T38(b1-LH)'s search step (with LS0).", ""),
    ("SEP-GUiid", "Prop. GU on LH-iid", "PROOF SKETCH", "—", "The random-design version.", ""),
    ("SEP-GUnulls", "Prop. GU with data-chosen nulls in the centre", "OPEN", "—", "Centres outside R.", ""),
    ("SEP-noLS0", "§7 · no-LS0 T38(b) via GU (final local search from Ŝ_pre when Ŝ_pre ⊆ R)", "CONJECTURE",
     "needs the pre-search HPM inside R", "A no-LS0 route through the production final search. Candidate N6 of T38 v3 (no-LS0 use).", ""),
]:
    r(pid, SPT, SP + " · " + lab, st, "N|none (A-REV7 pending)", N, "none", prem, mean, flags=fl)

# ---- W7-PART (head b2aa940) ----------------------------------------------------------------------------------------
PT = "W7-PART · REPORT.md §1 / PROOF.md"
PTT = "Thm 2 / Thm 5 input: partition = groups (new)"
for pid, lab, st, prem, mean in [
    ("PART-ThmA", "Theorem A (deterministic: laminarity, blocks = groups)", "PROVED", "GRP(ρ, ψ̄); SIZE g_max ≤ B < 2g_min",
     "Complete linkage + cut + next-fit packing give blocks = groups iff the dendrogram is laminar (A0–A4)."),
    ("PART-L1", "Lemma L1 (pair-law representation)", "PROVED", "—", "Monotone in |r|."),
    ("PART-L2", "Lemma L2 (Hotelling-density tail)", "PROVED", "density cited; checked numerically two ways", "Tail bound for sample correlations."),
    ("PART-ThmB", "Theorem B", "PROVED", "iid Gaussian rows, GRP, SIZE",
     "P(blocks ≠ 𝒢) ≤ Σ_within P_ρ(|r̂| ≤ t) + Σ_cross P(|r̂| ≥ t), t ∈ (ψ̄, ρ)."),
    ("PART-CorB", "Corollary B", "PROVED", "as Theorem B; p ≤ n^A",
     "P(blocks ≠ 𝒢) ≤ (2/(√π(1−ρ)))p²√n e^{−(n−4)I*}; can replace W3-PXN P1's cited lemma. LH at n = 200: rigorous 0.17 (MC 1.5e-4)."),
    ("PART-ThmC", "Lemma L3, Theorem C, Corollary C (independent groups)", "PROVED", "IND", "Exponent 2I*."),
    ("PART-kappa", "κ_C = 2I* bookkeeping", "PROOF SKETCH", "identity PROVED; mesh-1/n bookkeeping sketched", "—"),
    ("PART-CE1", "CE1 (g_h > B)", "COUNTEREXAMPLE", "—", "A group larger than B is split w.p. 1."),
    ("PART-CE2", "CE2 (2g_min ≤ B)", "COUNTEREXAMPLE", "blocks are unions of whole groups (PROVED)", "Blocks ≠ groups surely when two groups fit in one block."),
    ("PART-CE3", "CE3 (|ψ| > ρ)", "COUNTEREXAMPLE", "mechanism PROVED; blocks ≠ 𝒢 by simulation", "Cross-group correlation above within-group breaks recovery."),
    ("PART-pairing", "which groups share a block when 2g ≤ B (the study's g = 5)", "OPEN", "—", "W3-VEXP GAP (b) still open."),
]:
    r(pid, PTT, PT + " · " + lab, st, "N|none (A-REV6 pending)", N, "none", prem, mean)

# ---- W7-SEC (head 7e33e8a): T05, T33, T32(i) recheck ------------------------------------------------------------------
SC = "W7-SEC · REPORT.md, PROOF_T05.md, PROOF_T33.md"
for pid, tgt, lab, st, prem, mean in [
    ("T05-R", "supplement (T05)", "Lemma T05-R + Cor. T05-R1", "PROVED", "G; ORTH", "Exact representation; the HPM is a top-k set (T05(i))."),
    ("T05-U", "supplement (T05)", "Theorem T05-U + Cor. T05-U∞", "PROVED", "G; ORTH", "Finite-n failure bound for the global HPM."),
    ("T05-Shat", "supplement (T05)", "Cor. T05-Ŝ (reported HPM)", "PROVED-UNDER", "the code reading of local_search", "P(Ŝ = S₀) ≤ bound(U) + P(final local limit)."),
    ("T05-L", "supplement (T05)", "Theorem T05-L", "PROVED", "limit", "liminf ≥ Φ(c)^{s₀} (T05(ii)); explicit n₀ useless (log n ≈ 227)."),
    ("T05-G", "supplement (T05)", "Prop. T05-O + Theorem T05-G", "PROVED", "p = n^a", "Gap [√(1+2a) − √(2a)]√log n (T05(iii))."),
    ("T05-wording", "supplement (T05, negative)", "'loses a √log n factor'", "COUNTEREXAMPLE", "p = n^a, a > 0",
     "False as a multiplicative statement; true additively in amplitude (a wording correction)."),
    ("T33-M", "supplement (T33)", "Lemmas T33-M, T33-Q", "PROVED", "—", "I ≼ H_S, A_S with explicit bounds; Q_S ≥ y′y/(n+1)."),
    ("T33-S", "supplement (T33)", "Theorem T33-S", "PROVED-UNDER", "Higham H1–H4 (cited from memory), FP, NOUF, LIB, SMALL", "Cholesky succeeds; explicit η bounds."),
    ("T33-NF", "supplement (T33)", "Cor. T33-NF", "PROVED", "T33-S", "numerical_failure is impossible at n = 200 for every p and y."),
    ("T33-H", "supplement (T33)", "Prop. T33-H", "PROVED", "—", "The computed HPM is within 2η̄′ of the exact HPM over a common scored set."),
    ("T33-Z", "Prop 2 (VAL-FP)", "Prop. T33-Z", "PROVED", "deterministic part; the a priori ε part is PROVED but vacuous at study budgets; ε must be measured by replay (OPEN)", "Floating-point error of Ẑ."),
    ("T33-errbound", "implementation (negative)", "engine error_bound() (v3_score.h:242)", "COUNTEREXAMPLE", "n ≥ 10⁵",
     "The engine's error_bound() is not a bound at large n (ratio 1.17 at n = 10⁵, 6.2 at 4·10⁶); n = 200 unaffected; implementation fix recommended."),
    ("T32-fp", "Thm 5 (c)", "T32(i) addendum (fp pilot)", "PROVED", "without EX-A", "The pilot has ≤ T_e + 1 stages: +1,320,960 on 2.676·10¹¹ at (200, 500)."),
]:
    r(pid, tgt, SC + " · " + lab, st, "N|author's own line-by-line check only", N, "none", prem, mean)

# ---- O-STAGES (head 8d3c142) -------------------------------------------------------------------------------------------
ST = "O-STAGES · REPORT.md"
STT = "Thm 5 (c) / Thm 6 (P1): stage count T_n (new)"
for pid, lab, st, prem, mean, fl in [
    ("STG-L0", "Lemma 0 (reference-state identity)", "PROVED", "—", "ρ_V(u, v) = q_u(R)q_w(R)/q_v(R)², w = 2v − u.", ""),
    ("STG-L1", "Lemma 1 (monotonicity)", "PROVED", "—", "Bisection finds the exact frontier.", ""),
    ("STG-G", "Theorem G (greedy optimality)", "PROVED", "—", "The greedy grid is the shortest valid grid.", ""),
    ("STG-L", "Theorem L (path length)", "PROVED", "c → 0", "√c·T*(c) → L; not the answer at production c.", ""),
    ("STG-F", "Theorem F (favourable sandwich)", "PROVED", "Δ ≤ 0.0513", "N(w₊) ≤ T* ≤ N(w₋).", ""),
    ("STG-Wp", "Corollary W′ (BO favourable)", "PROVED-UNDER", "(LL): F-DRAFT Theorem W's layer law, PROOF SKETCH; O-WSTAB has a COUNTEREXAMPLE to F-DRAFT W(c)/W(b) for 2Ar > 1",
     "T* = O(1) in the BO favourable regime.", "CONFLICT"),
    ("STG-M", "Theorem M (masked two-state crossing)", "PROVED", "—", "log₂(A₀ − 1.48) − 0.95 ≤ T* ≤ log₂(A₀ − 2.2) + 11: (P1) of Thm 6 fails in the masked regime.", ""),
    ("STG-P", "Lemma P (perturbation)", "PROVED", "—", "—", ""),
    ("STG-W3p", "Corollary W‴ (corrected W″)", "PROOF SKETCH", "PROVED given PAIR (unproven); LH c ≥ 2 OPEN", "T* = log₂A₀ + O(1).", ""),
    ("STG-cexW2", "W″ 'O(1) stages' (F-DRAFT)", "COUNTEREXAMPLE", "numerical: T* = log₂A₀ + 7.7 ± 0.4", "F-DRAFT's O(1) stage count is false.", ""),
]:
    r(pid, STT, ST + " · " + lab, st, "N|none", N, "none", prem, mean, flags=fl)

# ---- O-DILUTE (head abedf99) ------------------------------------------------------------------------------------------
DL = "O-DILUTE · THEORY.md / REPORT.md"
DLT = "Thm 2 / n = 200 disclosure: dilution masking (new)"
for pid, lab, st, prem, mean in [
    ("DIL-E", "Theorem E (exact start decomposition)", "PROVED", "any data, any partition, positive tables",
     "π₀(S) = ∏_b π_b^t(S_b)·A_t(|S|) for every t > 0."),
    ("DIL-E1", "Cor. E1, E2", "PROVED", "as Theorem E", "−log π₀(S₀) = visibility + competition − size; sharpens W3-VEXP Prop. D."),
    ("DIL-R", "Theorem R (exact law of #truths/#nulls under π₀)", "PROVED", "as Theorem E", "π₀(R_d) = P(M ≤ d)."),
    ("DIL-N", "Lemma N (null score law)", "PROVED", "Gaussian null independent of (y, X_{−l})", "r_ly² ~ Beta(½, (n−2)/2) exactly: the table scores a null as in pure noise."),
    ("DIL-N1", "Cor. N1 (expected null inclusions)", "PROVED", "expectation bound PROVED; in-probability constant PROOF SKETCH", "Θ(s₀√(log p)/√n) null inclusions, about 1 at the study size."),
    ("DIL-Lw", "Lemma L (common plug-in σ² multiplies null exponents)", "PROVED", "identity PROVED; extreme-value consequence PROOF SKETCH", "Oracle σ² floods the start (≈ ×7 at c = 0.5, ×25 at c = 1)."),
    ("DIL-S", "Prop. S (ranking ceiling)", "PROVED", "any data, partition", "π₀(S₀) ≤ 1/∏(1 + [M_{j(i)} − i + 1]₊) for v3 tables and every common σ²."),
    ("DIL-Dp", "Prop. D′ (population dilution formula)", "PROOF SKETCH", "population BO, Gaussian design; joint law approximated", "Assembled formula for log π₀(S₀)."),
    ("DIL-DM", "Prop. DM (i)–(iii) (paper wording)", "PROVED", "dilution clause PROOF SKETCH", "Exact deficit decomposition, ranking ceiling, π₀(R_d) = P(M ≤ d)."),
    ("DIL-DMasy", "Conj. DM-asy", "CONJECTURE", "growing s₀", "π₀(S₀) → 0 while π₀(R_d) stays bounded below."),
]:
    r(pid, DLT, DL + " · " + lab, st, "N|none (A-REV6 pending)", N, "none", prem, mean)

# ---- F-SIGMA (head e2a3481) --------------------------------------------------------------------------------------------
FG = "F-SIGMA · REPORT.md"
FGT = "start-law modification: common σ̂² (new; REJECTED as a method change)"
for pid, lab, st, prem, mean in [
    ("SIG-S0", "Lemma S0 (variant invariance)", "PROVED", "σ̂² 𝓒-measurable; HPM ingestion records log m(U)", "Locked identities hold verbatim; table-specific results must be re-derived."),
    ("SIG-S1", "Lemma S1 (odds transfer under BO)", "PROVED", "BO", "Under BO the common-σ̂² start inherits the posterior's odds up to ν[ψ(u(S)) − ψ(u(S′))]."),
    ("SIG-S2", "Theorem S2 (dichotomy)", "PROVED-UNDER", "BO, SE-blk, s₀ fixed, BM-blk with plug-in (author: 'PROVED under BO')", "Concentration iff σ²/σ̂² < 1 + 1/(2A); otherwise the start floods."),
    ("SIG-S3", "Theorem S3 (cancellation untouched)", "PROVED", "H1, CL(L), SE", "π₀^C(S₀) ≤ p^{−c}n^{−c/2}e^{O_P(1)}."),
    ("SIG-S4", "Theorem S4 (route (a) under common σ̂², no LS0)", "PROVED-UNDER", "Theorem S2 with a₊ < 1 + 1/(2A); locked T03, T11(iii), T21; BO", "Author card: 'vacuous as an improvement' over v3 in the fixed-β regime."),
    ("SIG-S6", "Theorem S6 (random-design catastrophe)", "PROVED", "random design; exact numerics", "No single σ̂² serves truths and nulls at once (10^{−1303} at IID500)."),
    ("SIG-CE1", "C-E1 (screening plug-in underestimate)", "PROVED", "by S2(iv)", "—"),
    ("SIG-CE3", "C-E3 (S5 common factor)", "PROOF SKETCH", "—", "Proxies amplified."),
    ("SIG-CE4", "C-E4 (C-fix runaway)", "COUNTEREXAMPLE", "exact numerics + PROOF SKETCH", "A second fixed point at |mode| = K."),
]:
    r(pid, FGT, FG + " · " + lab, st, "N|none", N, "none", prem, mean)
upd("OMIX-C1", flags="CONFLICT")

# ---- T38-RECORD (this run) -------------------------------------------------------------------------------------------
r("T38-v3", "Thm 5 (statement of record)", "T38-RECORD · T38_STATEMENT.md (v3)", "PROVED-UNDER",
  "N|none (merge of W4-T38FULL, W6-FIXREV1, A-REV1 §7, W5-VMASK, W3-PXN, W5-VPGD, T32(i); no new mathematics)",
  "N|A-REV5 / A-REV7 pending", "none", "as W6F1-T38; LS0 part of the method; candidates N1–N6 listed separately",
  "One citation target for Theorem 5: (0), (0_H), (a), (b1), (b1′), (b2), (b1-LH), (b1-LH-iid, XF GAP), (c), with every "
  "status copied from its source.")

# ===================================================================================================================
# 3. Data facts (not results; rendered in their own section)
# ===================================================================================================================
DATA = [
    ("ELS-1", "Final local search made 0 moves in 2,394/2,394 completed PROD-H fits; S₀ scored in every completed fit",
     "S-ELS · REPORT.md §1, §3 (head 90423b1)", "data from production ledgers"),
    ("ELS-2", "565 strict posterior misses (F(S₀) < F(Ŝ)), 0 search misses, 6 resource-limit stops, 1,829 exact",
     "S-ELS · REPORT.md §3", "data; O-SWAP's '4 no-output fits' is superseded"),
    ("ELS-3", "All 541 'unrepaired' centres are forced by Lemma 0; W3-VT37R's sampled F(S₀) > F(S_c) cannot be reproduced on the fits",
     "S-ELS · REPORT.md §5", "data (settles Lemma0(b) on the study data only)"),
    ("ELS-4", "201/488 strict same-size swaps at c = 0.5", "S-ELS · REPORT.md §5", "data (the audit A-REV4 B5 asked for)"),
    ("LS0-1", "LS0 post hoc on all 2,400 regenerated fits: best LS0 model never beats the production HPM (0/2,394); recovery "
     "unchanged (1,119/1,200 at c = 1, 710/1,200 at c = 0.5); job B reproduced job A exactly",
     "O-LS0 · REPORT.md §1 (head 02348e2)", "data; Owls regeneration ≠ NOTS bits (F(S₀) agrees to 5·10⁻⁸; every margin ≥ 0.002)"),
    ("LS0-2", "T38(b1) premises at n = 200: (M1) 18/2,400; (M2) without margin 17/168 (c = 1), 1/129 (c = 0.5); (M3) all; "
     "cap 1,968/2,400; LS-score's implication held in all 18 fits meeting its premise",
     "O-LS0 · REPORT.md §1 item 6, §4(d)", "data; (M1) evaluated at the data-dependent S̃₀"),
    ("LS0-3", "LS0 cost: median 0.17 s (p = 500), 0.37 s (p = 1000), ≈ 5·10⁴ / 1.1·10⁵ scores; < 0.1% of a fit",
     "O-LS0 · REPORT.md §1 item 5", "data"),
    ("LS0-4", "In-engine (integrated) LS0 test fit not run", "O-LS0 · REPORT.md §6 item 4", "OPEN implementation check"),
]

# ===================================================================================================================
# 4. Lean formalisation (L-LEAN head cfa78ed; code d58493b)
# ===================================================================================================================
LEAN = [
    ("T21 (C1) and decompositions", "Thm4-C1, T38-(0)", "t21_C1, t21_decomposition, t21_decomposition', hpm_eq_truth, markov_half",
     "sorry-free; abstract probability space; routes (a)–(f) and H03 asymptotics NOT formalised"),
    ("T07 (i), (i′), (ii), (iii), Lemma psi", "Prop1-T07", "ceiling, no_size_prior_repairs, ceiling_sharp, hpm_min_risk01, mpm_min_riskH, …",
     "sorry-free"),
    ("T11(iii)", "(locked T11)", "t11_miss_pi, t11_miss_iid, t11_miss_iid_real", "sorry-free"),
    ("T37(i) / Theorem A", "TheoremA, Lemma0(a,c)", "theoremA1–A3, theoremA3_hpm, lemma2a, lattice forms; after Astra round 1: Lemma 0(c) general + HPM clause, A2 move count, D_S",
     "sorry-free; A5, Theorems B and C not formalised"),
    ("T12(i.a)", "Prop2(a,b,d,e)", "invariance_step, resample_move_step, unbiased_of_step", "PARTIAL: hstep is an explicit hypothesis"),
]
LEAN_FIDELITY = ("Fidelity: Fable 5.1 GREEN (same family). Astra round 1 GREEN on T21, T07, T11, T12 and RED on T37 coverage; "
                 "new theorems added without changing a frozen statement; **Astra round 2 OVERALL (T37) GREEN** "
                 "(`fidelity/ASTRA_round2.md`, code d58493b). W8-SYNTH §7 ('Astra did not finish') predates this. "
                 "101 declarations, 0 sorry; axioms only propext, Classical.choice, Quot.sound. A green fidelity check "
                 "says the Lean statements match the frozen statements; it does not change any author status word.")

# ===================================================================================================================
# 5. F-REFEREE objections (head fae6b7f) and their state (W8-SYNTH §5 tags, updated)
# ===================================================================================================================
REFEREE = [
    ("M1", "All theory asymptotic; thresholds ≈ 2·10⁶; simulations at n = 200", "open (R2 LH-SCALE, R9 first-n table not started); S-ELS decomposition and O-LS0 data exist"),
    ("M2", "Headline needs LS0, which the simulations did not run", "answerable: LS0 is part of the method and outcome-neutral on the study (O-LS0: 0/2,394); A-REV7 VERIFIED a no-LS0 masked theorem (B2-LH under STAB-LH, with an Astra-authored analytic STAB certificate on an explicit growing-p LH subfamily) and D2-LH (c = 1, qualitative); the headline choice is HQ's"),
    ("M3", "No-LS0 routes (b1′), (b2) are hypotheses-as-conclusions", "answered on LH: (b1′) by D2-LH, (b2) by B2-LH (A-REV7 VERIFIED); F2 GAP; general DELIV OPEN"),
    ("M4", "Favourable regime is where the sampler is unnecessary; need separation and masked Ẑ/PIP statements", "in progress, with a twist: W7-SEP supports 'moving off the start is needed', not 'tempering is needed' (E-SPINE); F-MASKPIP M1–M3"),
    ("M5", "2^B factor; (P1) circular; ORTH sketch", "in progress: W5-FAVIID Theorem A/B 2^B-free (REPORT now complete, author only); O-STAGES Theorem M"),
    ("M6", "No positioning vs Yang–Wainwright–Jordan 2016, Zhou–Yang–Vats–Roberts 2022", "open (W8-SYNTH task 10)"),
    ("M7", "Ẑ/PIPs meaningless in the masked regime", "in progress: F-MASKPIP, O-PW2, O-CERT/O-VCERT"),
    ("M8", "All verification same-family; T32(i) conjecture; SR/GUARD as hypotheses", "largely answered: A-REV5–A-REV9 cross-family reviewed the W6 repairs, the LS0 route (A-REV8 VERIFIED Thm b1, Lemma M, LS-score, LH-LAT), the no-LS0 route (A-REV7) and the new results (A-REV6, A-REV9); GUARD read by A-REV5/A-REV8 (statistical scope); T32(i) still SF only (A-REV6 'supported', A-REV9 deferred)"),
]

# ===================================================================================================================
# 6. Proposed label renames (W8-SYNTH §4.15). Proposals only; old labels remain valid citations.
# ===================================================================================================================
RENAMES = [
    ("Lemma M", "W4-T38FULL §3.2 (score comparison)", "Lemma SC"),
    ("Lemma M", "W5-FAVIID (Mittag-Leffler aggregation)", "Lemma ML"),
    ("Lemma M", "O-CERT (Q_S ↓, D_S ↑)", "Lemma MON"),
    ("Prop. M", "A-DRAFT §3.1 (naive merge)", "Prop. NM-A"),
    ("Prop. M", "W4-SHARE (no posterior barrier near the truth)", "Prop. NB-SHARE"),
    ("Prop. M1–M3", "F-MASKPIP", "Prop. MP1–MP3"),
    ("Lemma S", "W1-T38E / W6-FIXREV1 (ESS share; S′)", "Lemma ESS"),
    ("Lemma S", "W3-PGD (superset states)", "Lemma SUP"),
    ("Lemma U", "W2-PREM / W6-FIXREV2 (uniform expansion)", "Lemma U (keep)"),
    ("Lemma U", "W3-PXN §9.1", "Lemma U-PXN"),
    ("Lemma 0", "W6-FIXREV2 (T37 inclusion)", "Lemma 0 (keep)"),
    ("Lemma 0", "O-STAGES (reference-state identity)", "Lemma RS"),
    ("Lemma 0", "O-WSTAB", "Lemma WS0"),
    ("Lemma P", "W1-T24G / W6-FIXREV1 (Gibbs path)", "Lemma P (keep)"),
    ("Lemma P", "O-STAGES (perturbation)", "Lemma PERT"),
    ("Theorem A/B/C", "W6-FIXREV2 (refined T37)", "Theorem 3A / 3B / 3C"),
    ("Theorem B", "W1-T24G (Gibbs path)", "Theorem GP"),
    ("Theorem A/B/C", "O-PW2", "Theorem PW-A / PW-B / PW-C"),
    ("Theorem A/B/C", "W7-PART", "Theorem PART-A / PART-B / PART-C"),
    ("Theorem A/B", "W2-T26", "Theorem 6A / 6B"),
    ("Theorem W", "W3-PGD (repair)", "Theorem PGD-W (lattice form: W_Lat)"),
    ("Theorem W", "F-DRAFT / O-WSTAB (weight stability)", "Theorem WS"),
    ("W′", "O-STAGES Cor. W′ vs O-WSTAB W′", "Cor. STG-W′ / Cor. WS-W′"),
    ("CE1", "W1-T24G (H24 obstruction) / W7-PART / O-VCERT-type uses", "CE-H24 / CE-PART1 / (context)"),
    ("(e′)", "FABLE_REVIEW (T37) vs Theorem B route", "route (e-T37) / route (e-B)"),
    ("Lemma R", "O-BGIBBS (multi-flip round) vs W3-PGD (score expansion)", "Lemma MF / Lemma R-PGD"),
]

# ===================================================================================================================
# 7. Retired statements (additions)
# ===================================================================================================================
RETIRED += [
    ("'Without LS0 the paper has no masked-regime consistency theorem' (W4-T38FULL II.9; W6-FIXREV1 Not claimed; F-REFINE)",
     "no-LS0 candidates on LH now exist (W5-B2ENV, W5-VMASK R1, O-BGIBBS BG3, F-SHARE F1/F2, W7-SEP)",
     "'candidates on LH, pending cross-family review (A-REV7)' (T38-RECORD v3 I.D; E-SPINE §2.4)"),
    ("'Tempering / the sampler is needed for discovery in the masked regime'",
     "W7-SEP Prop. GU / Cor. GU-LH: one greedy search from the start mode suffices on LH; no bridge-vs-search separation",
     "'moving off the start is needed' (E-SPINE; T38-RECORD v3 Remark 6)"),
    ("'LS0 is an optional tweak, needed only if eligibility cannot be proved otherwise'",
     "approval in effect after O-LS0 (0/2,394 HPM changes)", "LS0 is part of the method (E-SPINE §2.1)"),
    ("'T32(i) is a CONJECTURE' (W6-FIXREV1 k1; W7-SEP I11)", "W5-LOCKBOOK proves it; W7-SEC re-counted", "T32(i) PROVED (same family)"),
    ("'Common plug-in σ² is the right tool for the n = 200 dilution masking' (O-MIX §1/§10)",
     "floods the start in random designs, even with the oracle σ² (O-DILUTE §5; F-SIGMA Thm S6)", "rejected; residualised tables + F-SIGMA Step 0 if any start change"),
    ("F-DRAFT W″: 'O(1) stages' in the masked regime", "O-STAGES COUNTEREXAMPLE", "O-STAGES Theorem M: T* = log₂A₀ + O(1)"),
    ("'Favourable from n ≈ 800–1,600' (and other single thresholds)", "sources disagree: 590–730, 800–1,600, 1,050–3,200",
     "omit, or attribute the W5-FAVIID empirical first n (E-SPINE §2.3)"),
    ("'9 ≤ g ≤ 16' in the LH / LH-iid statements", "false at n < 256 (B = 14 at n = 200; W7-PART)", "g ≤ B_n < 2g eventually"),
    ("'4 no-output fits' (O-SWAP)", "S-ELS, W5-LOCKBOOK: 6 resource-limit stops", "6"),
]

IMPL.append(("LS0-EMIT", "LS0 must emit its centre S̃₀ as the first evaluation (emit_centre = true) and use the HPM tie rule "
             "for argmax π₀; post hoc union = integrated run is untested", "W5-LOCKBOOK IMPL-EMIT; A-REV1 §6; O-LS0 §6",
             "IMPLEMENTATION OBLIGATION (LS0 now part of the method)"))
IMPL.append(("error_bound", "engine error_bound() is not a bound for n ≥ 10⁵ (n = 200 unaffected)", "W7-SEC T33",
             "IMPLEMENTATION FIX RECOMMENDED (not a method change)"))

# ===================================================================================================================
# 8. Cross-family reviews that landed DURING T38-RECORD (re-fetch at the end of the run):
#    A-REV5 (189770c), A-REV6 (02d6a4a), A-REV7 (70eadf3), A-REV8 (6417192), A-REV9 (bbadda3).
#    Rule: the new verdict text is appended to the cross-family column. The code is set to the new code only if
#    the row had no cross-family verdict before; otherwise the WEAKER of old and new is kept (E < G < V* < V).
#    Repairs are reviewed on their own rows (W6F1-*, W6F2-*). The original text keeps its original verdict.
# ===================================================================================================================
R5 = "A-REV5 · REVIEW.md"
R6 = "A-REV6 · REVIEW.md"
R7 = "A-REV7 · REVIEW.md"
R8 = "A-REV8 · REVIEW.md"
R9 = "A-REV9 · REVIEW.md"
_RANK = {"E": 0, "G": 1, "V*": 2, "V": 3}


def xf(id, code, text, **kw):
    for row in ROWS:
        if row["id"] == id:
            old_code, _, old_txt = row["cf"].partition("|")
            if old_code == "N":
                new_code, new_txt = code, text
            else:
                new_code = old_code if _RANK.get(old_code, 3) <= _RANK.get(code, 3) else code
                new_txt = text + " [earlier: " + old_txt + "]"
            row["cf"] = new_code + "|" + new_txt
            row.update(kw)
            return
    raise KeyError(id)


# ---- Theorem 5 parts ------------------------------------------------------------------------------------------------
xf("T38-(0)", "V", R5 + ": T38 output/execution interface VERIFIED (strict and usable-HPM conventions; stop-only GUARD; no completion conditioning); " + R8 + ": W6 formulation versus A-REV1 §7 VERIFIED")
xf("W6F1-T38", "E", R5 + ": 'T38 statement' overall ERROR (unqualified c = 2 iid-budget clause in (b1-LH), slow-p counterexample); conditional interfaces (0), (0_H), b1, b1′, b2 VERIFIED; D3 surrogate conditioning GAP; cost must keep its T32(i) qualification (GAP). " + R8 + ": W6 vs A-REV1 §7 VERIFIED")
xf("T38-b1′", "G", R5 + ": the W6 rate-margin repair is VERIFIED (see W6F1-D2inf); the masked NB′ instance remains a sketch in the W4/W6 text (LH c = 1 instance: B2E-D2LH, A-REV7)")
xf("T38-b2", "G", R5 + ": the W6 eligible-set / repair-certificate interface is VERIFIED; genuine DELIV stays OPEN; the D3 surrogate's conditioning is a GAP (state SHARE/EXIT conditional on (data, 𝓒), or assume DELIV directly)")
xf("Thm-b1", "V", R8 + ": Thm 5(b1) conditional consistency VERIFIED (v3 + LS0, (P), (M1)–(M3), execution assumptions, ideal arithmetic); " + R5 + ": b1 direct route VERIFIED")
xf("LS-score", "V*", R8 + ": scoring of S₀ VERIFIED; the move count 'at most Φ(C₀)−1' is ERROR at C₀ = S₀ (n = 4, p = 1 counterexample E1); repair: max{Φ(C₀)−1, 0}")
xf("LemmaM", "V", R8 + ": Lemma M VERIFIED, including uniformity and standardisation (fixed k, polynomial p, fixed noise variance, eigenvalue floor on the preferred model); it does not use the quadratic expansion A-REV3 rejected in W4-SHARE")
xf("LH-LAT", "V*", R8 + ": Prop. LH-LAT VERIFIED for fixed exact-Gram LH parameters; m₀ is a valid lower bound, not a universal sharp margin")
xf("T38-b1-LH", "V*", R8 + ": exact-Gram b1-LH consistency VERIFIED with LS0 (fixed parameters; c = 1 needs only the initial scan); the joint exact-Gram eligibility and posterior premises VERIFIED. The iid-draw-failure clause is excluded (claim T38-b1-LH-iidfail)", flags="CONFLICT")
claim("T38-b1-LH-iidfail", "T38-b1-LH", "W4-T38FULL / W6-FIXREV1 T38_STATEMENT (b1-LH): 'Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞'", "N|none",
      "E|" + R5 + ": ERROR (c = 2, p ≍ log log n: Q_fπ₀(S₀) ≳ (log n)/p² → ∞); " + R8 + ": GAP (the ceiling O_P(n^{1−c/2}p^{−c}log²n) does not vanish for slow p; not a counterexample to actual production Q_f, which may be on the exact branch)",
      "referee repair (A-REV5, A-REV8): require n^{1−c/2}p^{−c}log²n → 0 (c = 2: p/log n → ∞); state SMC applicability separately. Applied as wording in T38-RECORD v3", "applied",
      "Only the claim that iid final draws miss S₀ needs a growth condition; masking and LS0 consistency are unaffected.", flags="CONFLICT")
xf("Cost-T38", "G", R5 + ": (c) must retain its T32(i) qualification (GAP); " + R6 + " BOOK: T32(c)'s stated O(max(n,p)p log²(n+p) + p²log²(n+p)) misses the calibration-iteration factor, GAP; direct bound O(max(n,p)p log³(n+p) + p²log²(n+p)) (Astra candidate R5); polynomiality survives")
xf("T32(i)", "N", R6 + " BOOK: T32-a count 'supported by loop accounting' in W5's exact-arithmetic scope (no verdict word; no adoption); W7's slack-inequality correction noted; " + R9 + ": W7-SEC T32(i) deferred (GAP in that review, no rejection)")
xf("PXN-P6", "G", R6 + " and " + R8 + ": GAP retained after W5-VMASK R2 (Λ(a)'s Tr(c) range and dimension not generalised)")
xf("PXN-P7", "G", R6 + " and " + R8 + ": GAP retained after W5-VMASK R1/R3/R6 (cap injection, summed tail and Beta shape repaired; Tr dimension must still be generalised; P7 prints (n−3−s)/2)")
xf("PXN-Cor", "G", R6 + " and " + R8 + ": joint LS0 route GAP retained; W7-PART B settles only the restricted partition-recovery premise")
xf("PXN-P1", "V", R6 + ": VERIFIED via W7-PART Theorem B on SIZE and a fixed correlation separation, including polynomial p ≫ n")
xf("VMASK-R1-NB", "G", R6 + ": P7 route GAP after R1 (Tr dimension); " + R8 + ": 'substantive repairs to the old sketch', but GAP retained")

# ---- W6-FIXREV1 / W6-FIXREV2 repair rows (A-REV5 re-review) --------------------------------------------------------
for cid, code, txt in [
    ("W6F1-PropU′", "V", "Prop. U′ (independence iff and extra-for-extra neutrality) VERIFIED"),
    ("W6F1-ThmB-conv", "V", "Theorem B finite inequality with F′ and the CON §2 conventions VERIFIED; statistical premises and delivery not established"),
    ("W6F1-LemmaP", "V", "Lemma P multi-target bound VERIFIED"),
    ("W6F1-LemmaS′", "V", "Lemma S′ VERIFIED (clipped bound; equality only for f > 1−e)"),
    ("W6F1-D2inf", "V", "finite D2 with r* and D2-∞ with explicit rate margins VERIFIED; masked NB′ instance remains a sketch"),
    ("W6F1-E3′", "V", "E3′ with q < 1, centre emission and +1 score call VERIFIED; F-REFINE Card 3(i) still repeats the false unrestricted bound (ERROR)"),
    ("W6F1-LemmaU′", "V*", "core (correct 0.51/c limit; budgeted family) VERIFIED; printed probability arrow '1 − o(1) → 0' ERROR (typographical; should tend to 1, eventual statement)"),
    ("W6F1-NL0′", "V", "NL0 sum-of-suprema form VERIFIED; PG(a) and its multiplicity cost are extra assumptions"),
    ("W6F1-CE1′", "V", "CE1-narrow VERIFIED as an explicit exact-Gram counterexample sequence (not universal failure of H24)"),
    ("W6F2-LemmaT", "V", "Lemma T VERIFIED"),
    ("W6F2-LemmaNT", "V", "Lemma NT VERIFIED under full-rank union and summed size < n−1"),
    ("W6F2-Lemma0′", "V", "Lemma 0(b′) VERIFIED"),
    ("W6F2-PropF", "V", "Prop. F VERIFIED (three categories, restricted to failed fits); F-REFINE Card 4 remains wrong"),
    ("W6F2-ThmA′", "E", "feasible-lattice core, POS-repaired A5 and tie-aware repair VERIFIED; the literal cap-free lattice/count assertion ERROR (ignores K)"),
    ("W6F2-rest", "V*", "T03♯ core, fixed-design EXP′ (0.51), deterministic-chain Theorems 3/4 with H3, budgeted Lemma U VERIFIED; replacement onset gloss ERROR; random-design EXP′ / packing and optional limit law GAP"),
]:
    xf(cid, code, R5 + ": " + txt)

# ---- no-LS0 candidates on LH (A-REV7) -------------------------------------------------------------------------------
xf("B2E-D2LH", "V*", R7 + ": VERIFIED for qualitative consistency (c = 1, p/√n → ∞, exact Gram, groups = blocks); GAP for the stated unconditional O(√n/p) rate (needs expectation/tail control of the data events)")
xf("B2E-NBLH", "V*", R7 + ": NB′ bound O_P(√n/p + n^{−1/2}) used in the verified D2-LH consistency; corrected NB′ (ESS ≥ 0.9H at 1/T₀) required")
xf("B2E-B2LH", "V*", R7 + ": VERIFIED conditional theorem under STAB-LH, with an Astra event-rate correction (U2 gives relative RSS error O(n^{−1/3}); use η_n = O(n^{−1/3} + √(log n/n)); conclusions survive). Integrate the bound truncated at one for unconditional convergence; the conditional O_P rate is not an unconditional numerical rate")
xf("B2E-CONF", "V*", R7 + ": confinement checked against actual moves (independence proposal predrawn; ≤ 17 swap additions; 40-extra envelope); a_n = O_P((log n/n)^{3/2}) VERIFIED")
xf("B2E-LemmaR1", "V*", R7 + ": repair order event VERIFIED with c_* = g^{−c}/C(2cg+19+B+2, B+2); stage T already suffices")
xf("B2E-LemmaJ", "V*", R7 + ": VERIFIED, with η_n corrected to O(n^{−1/3} + √(log n/n))")
xf("B2E-MLH", "V", R6 + ": VERIFIED restricted fixed-coefficient lattice replacement (not M(b)'s scope); " + R7 + ": exact log-RSS argument, unaffected by the A-REV3 quadratic-expansion ERROR; the '(1−o(1)) absorbed into g_*' step is fillable")
xf("OBG-BG3", "V", R7 + ": VERIFIED (abstract round-boundary lock and terminal scoring inequality given EX-A/EX-S/SR); " + R6 + ": conditional first-exit/terminal-hazard template")
xf("OBG-LH-lock", "V*", R7 + ": VERIFIED as a conditional fixed-p implication from strict C1–C3 and block keep margins (Astra-authored completion §3, one common data event); unrestricted LH locking is FALSE (claim OBG-LH-lock-general). Fixed p eventually takes exact enumeration: an SMC component result")
xf("OBG-LH-lockC1p", "V", R7 + ": block keep losses C1′/C2′ hold on LH (projection onto visible a-group β(1−ψ²)x_a, masked group zero)")
xf("OBG-T38b-BG3", "V*", R7 + ": BG3 + conditional LH-lock VERIFIED for fixed p with strict C1–C3 as hypotheses; recommended as a fixed-p component lemma, not the headline")
claim("OBG-LH-lock-general", "OBG-LH-lock", "O-BGIBBS · REPORT.md · LH-lock for general (ρ, ψ, g, c) with |ψ| < ρ", "N|none",
      "E|" + R7 + " §5: ERROR. One pair, g = 4, ρ = 0.85, ψ = 0.5, β_a = 1.4, β_b = −0.7: the swap 0 → 4 improves the population fit by 0.00479, so C2 fails for allowed LH parameters (also g = 9). It is not a counterexample to an end-of-round bound or to the algorithm",
      "keep C1–C3 as explicit hypotheses (A-REV7)", "none", "Strict locking gaps are a real restriction, not a regularity that follows from |ψ| < ρ.")
xf("FSH-F1", "V", R7 + ": VERIFIED (round-boundary closure given KEEP; does not supply repair); " + R6 + ": usable as a conditional template")
xf("FSH-L1.2", "G", R7 + " and " + R6 + ": the pointwise display is not the proved bound; use s·sup max(κ₀, κ₁) + (B+1)p·sup max(ρ₀, ρ₁) + π₀(Wᶜ) (intermediate-state suprema, swap Hastings factor)")
xf("FSH-F2", "G", R7 + ": GAP (PK counts 2(g−1) pair-unit proxies; cross-unit masked proxies need a swap comparison; Lemma 3.4's Schur formula has a factor error; y ↦ y ∪ S° can exceed K). F2 supplies delivery only")
xf("FSH-L3.4", "E", R7 + ": the displayed Schur increment is wrong by a factor (correct: [n/(n+1)](x′Ay)²/(x′Ax + 1/(n+1)); n = 10 example 0.1 vs 1.1); repairable with an additive bound")
xf("FSH-T38b2", "G", R7 + ": not to be cited as a growing-p no-LS0 guarantee; §4 scoring stays conjectural (4.3)")
claim("FSH-DOMc1", "FSH-F2", "F-SHARE · REPORT.md §2 · 'DOM … Void for c = 1'", "N|none",
      "E|" + R7 + " §5: ERROR with visible groups (g = 4, ρ = 0.4, ψ = 0.2, β_a = 1, visible hub β_h = 0.01: swap h → b lowers the residual from 0.0384 to 0.0001). The c = 1 no-visible-group case is unaffected",
      "none written", "none", "The DOM exemption for one masked hub fails when visible groups are present.")
claim("FSH-rareoutsider", "F-SHARE §2 sharpness", "F-SHARE · REPORT.md §2 · rare-outsider sharpness", "N|none",
      "E|" + R6 + ": π₀(o) = 1/N leaves probability → e^{−1} of no outsider at all", "none written", "none", "The sharpness remark needs Nπ₀(o) → ∞.")
claim("FSH-retention", "F-SHARE §5.2", "F-SHARE · PROOF §5.2 · retention inequality", "N|none",
      "E|" + R6 + ": at T = 1, η = ½, 1 − η < e^{−η}, opposite to the printed lower bound", "none written", "none", "A displayed inequality has the wrong direction.")
xf("SEP-GU", "V*", R7 + ": VERIFIED as a greedy best-neighbour theorem ('every swap loses' is stronger than needed: an extra swap is compared with its deletion); " + R9 + ": GAP in that review (imported Lemma M not re-audited there; A-REV8 verified Lemma M)", flags="CONFLICT")
xf("SEP-CorGULH", "V*", R7 + ": VERIFIED as greedy repair on LH (with LS0)")
xf("SEP-noLS0", "G", R7 + ": GAP: the actual best-scored search centre may contain nulls outside R; eligibility, or a search from S° (LS0), is still needed")
xf("SEP-A", "V", R9 + ": VERIFIED as an implication from its imported tight start-mass and posterior-concentration premises")
xf("SEP-B", "V", R9 + ": SEP(B1–B3) VERIFIED as implications from imported premises")
# Astra-authored results (referee-authored; not independently checked by a Claude run)
r("STAB-cert(A7)", "Thm 5 (b2) no LS0: explicit subfamily", R7 + " §4 · analytic STAB certificate", "REFEREE", "N|n/a",
  "N|Astra-authored; checked by a Sol reviewer; pending Claude verification", "none: finding",
  "λ₀ b_vis² > R_M, with R_M = Σβ_i²ψ_i²(1−ψ_i²), λ₀ = (1−max|ψ_i|)(1−ρ_max), b_vis² = min_{S°}θ_j²",
  "STAB-LH holds, with margin ≥ λ₀b_vis² − R_M, for every proxy configuration and any number of orthogonal null columns.")
r("B2LH-subfamily(A7)", "Thm 5 (b2) no LS0: explicit subfamily", R7 + " §4 · concrete growing-p subfamily", "REFEREE", "N|n/a",
  "N|Astra-authored; checked by a Sol reviewer; pending Claude verification", "none: finding",
  "g = 9, c = 2, no unlinked visible groups, ρ = 0.4, ψ = 0.2, β = 1, σ² = 1, null groups appended, p_n = 9⌊n/18⌋ (exact Gram, B = 16 eventually); STAB margin ≥ 0.4032",
  "With B2-LH: P(output and wrong) → 0 for the UNCHANGED method (no LS0) on an explicit, genuinely masked LH subfamily, with no numerical premise left. A-REV7's recommended no-LS0 masked theorem.")
r("LHlock-completion(A7)", "Thm 5 (b) no LS0, p fixed", R7 + " §3 · Astra-authored completion of conditional BG3/LH-lock", "REFEREE", "N|n/a",
  "N|Astra-authored", "none: finding", "fixed p; strict C1–C3", "One common data event gives fixed log-score margins a·n for every strict population gap; start mass, all move types and terminal repair follow; P(E_nᶜ) is added once.")

# ---- A-REV8 further findings ---------------------------------------------------------------------------------------
xf("VPGD-WLat", "V", R8 + ": W_Lat reduction VERIFIED in the stated lattice scope (no region-wide PGD claimed)")
xf("VPGD-LH-PGD", "V", R8 + ": LH-PGD lower bound VERIFIED for all non-truth lattice states incl. Φ = 1; sharpness numerical only")
claim("GUARD-diag(A8)", "GUARD (IMPL)", "W2-BOOK §0.1 literal claim 'every reported output equals the guard-free output'", "N|n/a",
      "E|" + R8 + " E2: RuntimeGuard::check appends a GuardRecord even when it does not stop, so operational diagnostics differ from the guard-free run; restrict the transfer to statistical outputs, scored sets, decisions and status semantics",
      "restrict GUARD to statistical fields (also A-REV4, A-REV6 BOOK R1)", "pending", "The stop-only coupling holds for statistics, not for run metadata.")

# ---- A-REV9: certificates, masked outputs, evidence variance, dilution, stages ---------------------------------------
xf("OCERT-LemmaM", "V", R9 + ": VERIFIED in exact arithmetic")
xf("OCERT-C1", "E", R9 + ": C1(a) ERROR as literally quantified (includes S = HPM: 1 ≤ e^{−g}); Z_𝒯 bound VERIFIED; C1(b) with R1 VERIFIED (original 'unscored' wording ERROR); C1(c) VERIFIED")
xf("OCERT-C2", "V", R9 + ": VERIFIED conditional PW2/Cantelli implication")
xf("OCERT-C3", "V*", R9 + ": exact ratios VERIFIED; GAP for identifying the locally returned centre with the HPM without an identity/tie check (v3_engine.h local_search)")
xf("OCERT-C4", "V*", R9 + ": exact boxes VERIFIED; floating-point clause GAP (needs interval bounds for the mixed ingredients of Φ)")
xf("OCERT-C5", "E", R9 + ": tie-insensitive prose ERROR (duplicate-column example); the displayed strict-score event inclusion VERIFIED")
xf("OCERT-C6", "G", R9 + ": original card GAP; the repaired exact implication holds with R1, R2 and explicit local/region checks")
xf("FMP-M1", "V", R9 + ": M1(a–c) VERIFIED under locked exact frozen-run assumptions")
xf("FMP-M2", "V", R9 + ": M2(a–e) VERIFIED as intersection bounds, not completion-conditioned guarantees")
xf("FMP-M3", "E", R9 + ": ERROR (probability-one counterexample); conditional means VERIFIED for 0 < κ < 1")
xf("FMP-Na", "G", R9 + ": literal finite-index/rate wording GAP; finite-index inequality with the actual non-crossing probability VERIFIED")
xf("OPW2-ThmA", "V", R9 + ": A1–A4 VERIFIED")
xf("OPW2-ThmB", "V*", R9 + ": B1–B3 VERIFIED; the O(N^{−3/2}) remainder only for fixed inputs/grid or uniform constants")
xf("DIL-E", "V", R9 + ": VERIFIED with feasibility/cap retained")
xf("DIL-E1", "V*", R9 + ": E1 three-term identity VERIFIED for production BF tables (GAP for arbitrary positive tables without normalisation); E2 VERIFIED with interior-size/end-point conventions")
xf("DIL-R", "V", R9 + ": VERIFIED (integer d ≥ 0, feasible supports)")
xf("DIL-N", "V*", R9 + ": VERIFIED under explicit joint independence; the parenthetical implication from zero truth correlation is ERROR")
xf("DIL-S", "G", R9 + ": GAP (the replacement assignments are not injective)")
xf("DIL-DM", "E", R9 + ": DM(i) size-sign ERROR (explicit construction)")
xf("STG-M", "V*", R9 + ": logarithmic order VERIFIED for the ideal two-state exact-frontier grid; explicit decimal constants GAP")
xf("PART-ThmA", "V*", R9 + ": A1–A4 VERIFIED (deterministic, no ties; A2's extra premise); " + R6 + ": A0(c) GAP (quantifier)")
xf("PART-ThmB", "V*", R6 + ": VERIFIED in restricted scope (SIZE, fixed correlation gap, Gaussian correlation-law input); " + R9 + ": B-exact VERIFIED; L2 density constants GAP")
xf("PART-CorB", "G", R9 + ": explicit constants not locked (L2 density normalisation not independently established)")
xf("PART-ThmC", "G", R6 + ": GAP (needs a corrected conditioning lemma; claim PART-L3)")
xf("PART-CE2", "E", R6 + ": unequal-size header ERROR (sizes 2 and 5, B = 5: next-fit cannot merge them); the equal-size study example survives")
claim("PART-L3", "PART-ThmC", "W7-PART · Lemma 3 (literal full-vector conditioning)", "N|none",
      "E|" + R6 + ": conditioning on both normalised vector collections fixes their cross inner products, so no nondegenerate Haar law remains; condition on within-group Gram matrices", "none written", "none", "A conditioning step is mis-stated; Theorem B does not use it.")
for cid in ("OSWAP-P1", "OSWAP-P2", "OSWAP-P3"):
    xf(cid, "G", R9 + ": predicted rates GAP (additional approximations and data reproduction remain; PA alone does not give the displayed add law)")
for cid in ("T05-R", "T05-U", "T05-Shat", "T05-L", "T05-G", "T33-M", "T33-S", "T33-NF", "T33-H", "T33-Z", "T32-fp"):
    xf(cid, "N", R9 + ": deferred (detailed proof/code audit not done; no mathematical rejection asserted)")

# ---- A-REV6: book-keeping, T26, SHARE (only rows whose state changes) --------------------------------------------------
xf("LemmaRO", "V*", R6 + ": VERIFIED conditional implication (nonnegative potential values; chosen output projection); BOOK R1 pending Claude")
xf("SHARE-M(b)", "E", R6 + ": original ERROR retained; Astra candidate M-star (exact log-RSS, normalised Gram eigenvalues, BM-∞) GAP pending Claude")
r("REV6-cands(A6)", "various (Astra-authored repairs)", R6 + " · SHARE.md, WEIGHTS.md, BOOK.md, PARTITION.md", "REFEREE", "N|n/a",
  "N|Astra-authored; pending Claude verification", "none: finding", "each with the restrictions in its file",
  "Candidate repairs M-star, EXIT-star, SH-star (W4-SHARE); NM-R, W2-R (F-DRAFT); BOOK R1–R5 (incl. R5: T32(c) with log³ calibration factor); a generalised Beta-tail lemma for W3-PXN P6/P7.")
claim("LOCKBOOK-exactexp(A6)", "Prop 2 (W5-LOCKBOOK STATEMENTS)", "W5-LOCKBOOK · full-output E[1_𝒪 Ẑ] ≤ Z·P(𝒜)", "N|n/a",
      "E|" + R6 + ": completed exact branch with 𝒜 defined SMC-only: Z > 0 on the left, zero on the right", "BOOK R2 (Astra) pending Claude", "pending",
      "The exact branch's evidence must be accounted for separately.")
claim("LOCKBOOK-tie(A6)", "Prop 1 (W5-LOCKBOOK paraphrase)", "W5-LOCKBOOK · 'same-size m ≥ m₀' certificate / Prop 1(iii) paraphrase", "N|n/a",
      "E|" + R6 + ": a tie with S₀ first in the prescribed order defeats the certificate", "BOOK R3 (Astra) pending Claude", "pending",
      "Tie order must be part of the certificate.")

# ---- implementation-fact rows --------------------------------------------------------------------------------------
for i, row in enumerate(IMPL):
    if row[0] == "GUARD":
        IMPL[i] = ("GUARD", row[1], row[2] + "; A-REV5: RuntimeGuard::check reads elapsed/operation time, uses no RNG and no statistical setting (supports the stop-only coupling); A-REV8 E2: diagnostics differ, so the transfer holds for statistical outputs only",
                   "IMPLEMENTATION FACT — statistical stop-only coupling supported by two cross-family code readings (A-REV5, A-REV8); literal 'every output equals' ERROR (A-REV4, A-REV8)")
    if row[0] == "SR":
        IMPL[i] = ("SR", row[1], row[2] + "; A-REV7: SR_AUDIT 'substantively correct'; its blanket 'no call passes emit = false' is too strong (v3_core.cpp:447,610,657 pass false for already-scored HPM centres)",
                   "IMPLEMENTATION FACT — HQ read, confirmed in substance by a cross-family reading (A-REV7)")
