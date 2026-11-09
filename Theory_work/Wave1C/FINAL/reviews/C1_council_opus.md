# C1 — final council, consistency chapter (Wave 1C), round 1 — seat **opus** (Claude Opus 5.5)

Object: `Theory_work/Wave1C/FINAL/consistency.tex` + `sections/s1…s9` (commit 5bcde3b). Brief: `FINAL/reviews/COUNCIL_BRIEF.md`.
Scored independently; the sol seat's file was not read. No git commands; the chapter was not edited.

## What I checked (adversarially)

- **Lemma CAP**, line by line, against the coded `local_search` in both cores (`PROD/cpp/v3_engine.h:378-418`, the cap
  test at :408; `CORE/cpp/v3_engine.h:385-425`, the cap test at :415), the LS0 spec (`SoP/02_method.tex:463-506`), the
  final-search call and post-search guard in `PROD/cpp/v3_core.cpp:444-451`, W1-PXN's run/closure conventions
  (`W1C/C-PACK/item5_PXN_consolidated/00_statement_and_conventions.md:60-133`), W1-GEN (C2)/(C3)/(C6), C-GROW
  STATEMENT/METHOD_REQUIREMENTS, C-DLV L1/L4, and A1. I tried these attacks:
  - an off-by-one in the scan count: the code scans C_a and then stops at `moves>=ell`, so the scanned centres are C_0…C_min(a,m*). Holds.
  - a cap that changes anything before LS0: excluded by (L1)/(L2).
  - the exact branch and `schedule_limit` branches. Handled.
  - the guard, which is checked only after a completed search (`v3_core.cpp:450`). This makes U_n depend on the cap,
    which the chapter discloses.
  - non-integer caps. Handled.
  - certified-event identity. Holds.
  - reversed monotonicity for GEN (C6). Correctly not transferred.
  **Lemma CAP (a)–(c) is correct.** One entry of the transfer list is wrong (finding 1).
- **Proposition F (A1 corrected form)** against C-DLV STATEMENT/L1/L4, METHOD_REQUIREMENTS and A1:
  - the chapter's text matches A1's "Exact corrected statement" verbatim in substance.
  - W_G and M_G: the extra scans are |S̃₀| ≤ K, each with ≤ q(p) requests, at L1's per-request cost; the extra archive is
    K(K+1) words. At p ∝ n the old core term is n⁵log³n and the extra term is n⁶.
  - the fallback grid is complete (pilot or last success, ≤ T₁ strictly increasing intervals, ends at 1).
  - the consistency clause goes through the pathwise D′ argument plus CAP(a).
  - CAL and IND-T are not needed.
  **The assembly is correct** under its premises (finding 3 adds a missing qualification).
- **Song–Liang map** against the PDF, journal pp. 949–959, 968–970:
  - P_n ≻ n^θ (p.950); Thm 1 conditions (8)–(15) (p.952); Cond 1 and Thm 2 (p.953); Cor 1 and Cond 2/(16) (p.954).
  - Cond 3 (p.955); Thm 3 and ξ_q, plus "Theorem S … consistency of MAP models" and the specificity remark (p.956).
  - Cond 4, Thm 4/(18), Cor 2/(19) (p.957); Cond 5 and remark (c) (p.958); §6 time with K_n = O(√P_n) (p.968); §7 discussion (p.969).
- **G1/G2 spot checks** of every statement box against its source:
  - TH09 card (`SoP/04_theory.tex:760-811`), M1 and M5 cards (`:105-135`, `:460-490`).
  - I4 SL0/SL1/SL2; W1-GEN STATEMENT v2.3 §1–§3; C-GROW STATEMENT v2.5 §1–§3; the PXN consolidated §0.1–§0.5.
  - C-MIS STATEMENT §2–§4; C-DLV STATEMENT and L4; the REPORT status lines of W1-PXN, W1-N1, W1-N3, W1-GEN, C-PACK,
    C-MIS, C-GROW and C-DLV; W1-N3 (a)–(f).
  - F1's ten amendments: all are present in the compiled text.

## Gate verdicts

- **G1 — PASS (with finding 1 required before freeze).** Every theorem statement I checked matches its source:
  hypotheses, conclusion and scope. The F1 amendments are in place: Lemma Z's Gram floor, GEN's (H2a)/(H2c) written out,
  GROW's strict NA/TL and antecedents, the AR(1) piecewise relevance set, and PXN's constants.
  The one dropped scope item is the **LS0 cap ℓ_n in the setting of Theorem D / Corollary D′ / CONFIG** (finding 1). It
  is disclosed in §7 ("does not transfer"), so it is not silent, but the local statements must carry it.
- **G2 — PASS.** Statuses are verbatim, with nothing upgraded. "PROVED-CHECKED" is used only for ticket packages whose
  REPORT shows lock → checks → CONTINUE → sweep → same-round council. C-DLV is kept PARTIAL. Corrected Prop F and Lemma
  CAP are explicitly marked "not councilled". One map cell could be read as attaching C-DLV's PROVED-CHECKED to the
  corrected Prop F (finding 5): MINOR.
- **G3 — PASS.** Lemma CAP (a)–(c) and its proof are correct for finite integer caps a ≥ ℓ_n under (L1)–(L4).
  Proposition F (A1 form) is correct as an ideal-machine statement, and its consistency clause transfers by CAP(a). The
  "what survives" list has one over-transfer (finding 1, Cor. D′'s SL_n form). It needs one more qualification: the
  transfer covers only caps ≥ ℓ_n (finding 4).
- **G4 — PASS.** The map is accurate about Song–Liang. It quotes the p ≻ n^θ assumption, Thm 3's sensitivity-only
  nature, the withdrawal of Cor 2 under a cap (remark (c), p.958), §6/§7 and the uninspected Theorem S. It is also
  accurate about our results. There is one wording conflation in the Thm 4 row (finding 6) and two notation nits.
- **G5 — PASS.** The frontier list is complete. It covers: onsets (2·10⁶, ≈10¹⁰, n=200 margins, log n ≳ 96); polynomial
  p; S5/factor designs and growing s₀; delivery for the shipped calibration open (O); pooled R′=4 PIPs; misspecification
  (EP, approximate projection, τ_n²); Hellinger contraction; Θ(p²) Gram memory; EX-A/FP and IDEAL-W; implementation
  premises; LS0 and the fallback off the frozen core. Missing: Prop F's dependence on the code-reading audits (finding 3).
- **G6 — PASS.** Notation, cross-references and premise lists are consistent overall. Residual items: the "one-line"
  fallback contradicts Remark (2) (finding 2), the two MR1s appear unlabelled in three places (finding 7), and the
  e4 → e4′ replacement is not valid for GROW as phrased (finding 4).

## Findings

**1. MAJOR — Theorem D, Corollary D′ (delivery form) and CONFIG are cap-ℓ_n results. The chapter drops the cap and §7
transfers D′ "verbatim" to the MR1 method.**
Evidence:
- The source scope is "LS0 cap ℓ_n = ℓ": `W1C/C-DLV/STATEMENT.md:12`, `:32` (CONFIG "LS0 (cap ℓ)");
  `W1C/C-DLV/lemmas/L4_delivery.md:7` (OP-LS0 (cap ℓ_n = ℓ)), `:38`; and `L1_resources.md:24-25`.
- The chapter's §6 setting (`sections/s6_delivery.tex:6`) lists "OP-LS0" with no cap.
- §1's CONFIG paraphrase (`sections/s1_setting.tex:32`) omits "production core plus LS0 (cap ℓ) and the e4 fallback".
- `sections/s7_impl.tex:62` lists "C-DLV Corollary D′" among the conclusions that "hold verbatim for 𝔐(a_n)".

D′'s displayed form, P(𝒪∩{Ŝ⁺=S₀}) ≥ 1−o(1)−P(𝒮ℒ_n) (`s6_delivery.tex:17`), uses Theorem D(i): 𝒰_n ⊆ 𝒮ℒ_n ∪ 𝒩_n. That
inclusion rests on Lemma R / Corollary R with the cap-ℓ_n envelopes. With a_n and the old allocation, a guard stop
during the longer LS0 is not excluded (A1 MAJOR; `v3_core.cpp:450` shows the guard fires after a completed search ⇒
`resource_limit`). Only the pathwise half of D′ transfers verbatim. Replacements:
- `s6_delivery.tex:6`, after "\textbf{Setting.} Method $\mathfrak M$ = v3.1 + LS0 as specified": insert
  "with LS0 move cap $\ell_n$ (C-DLV's CONFIG; for the C-GROW cap $a_n$ see Proposition~\ref{prop:F} and §\ref{sec:cap})".
- `s1_setting.tex:32`: replace "\textbf{CONFIG} (default declared list, polynomial certificate budgets, fixed worker
  count)" with "\textbf{CONFIG} (production core plus LS0 with cap $\ell_n$ and the e4 fallback, default declared list,
  polynomial certificate budgets, fixed worker count)".
- `s7_impl.tex:62`: replace "C-DLV Corollary D′ and the consistency clause of Proposition~\ref{prop:F}" with
  "the pathwise part of C-DLV Corollary D′ ($\PP(\Ocal\cap\{\Shat\ne S_0\})\le2\EE[1-\pi(S_0)]+\PP(\mathcal K_n(\ell_n)^c)$)
  and the consistency clause of Proposition~\ref{prop:F}; D′'s delivery form ($\ge1-o(1)-\PP(\mathcal{SL}_n)$) and
  Theorem~\ref{thm:D}(i) hold for $\mathfrak M(a_n)$ only under A1's amended allocation ($W_G,M_G$)".

**2. MINOR — "one-line calibration fallback" contradicts A1 and the chapter's own Remark (2).**
`s6_delivery.tex:4` and `s2_map.tex:31` both say "one-line". A1 (`HQ_AUDIT/A1_propF_redteam.md:43`) and Remark (2)
(`s6_delivery.tex:43`) say that changing only the status line fails validation. The phrase echoes C-DLV REPORT:92
("one line in `v3_calibrate`"), which A1 superseded. The §2 plain-reading sentence also places "unconditionally
(Prop. F)" right after GROW and C-MIS, which Prop F does not cover (Remark (4)).
Replacements:
- In `s6_delivery.tex:4`, replace "with a one-line calibration fallback" with "with a total tier-1 calibration fallback".
- In `s2_map.tex:31`, replace "and — with a one-line calibration fallback — unconditionally (Prop.~F)" with
  "and, on LH, LH-iid and the GEN class, with a total tier-1 calibration fallback, unconditionally (Prop.~F; not
  checked for the GROW or C-MIS classes)".

**3. MINOR — Proposition F's "P(no output) = 0" is relative to two code-reading audits. The chapter does not say so.**
Theorem D is "PROVED-CHECKED (relative to the P1/P3 audits)" (`C-DLV/REPORT.md:66`). P1 (the exit inventory) and S.3
(unreachable internal errors) are "AUDITED (code reading)" of the *serial shipped* call graph, and the LS0, worker and
fallback paths are premises (A1 table, row "LS0, workers, merge…"). Remark (3) covers the machine idealisation and
Remark (5) covers the C-ENG implementation, but not this. Add to Remark (3) (`s6_delivery.tex:43`): "The exclusion of
every other no-output path is relative to the P1 exit inventory and Lemma S.3, both \st{AUDITED (code reading)} on the
serial shipped call graph."

**4. MINOR — two scope qualifications on the caps and centres that the transfer list and e4′ need.**
- (a) **Caps below ℓ_n.** `s7_impl.tex:15` says "any cap ≥|S̃₀| is accepted by the proof". That is true for GROW (and
  C-GROW METHOD_REQUIREMENTS:20 gives the sharper "≥ |S̃₀∖S₀|"). But Lemma CAP's transfer of PXN/GEN/C-MIS D needs
  a ≥ ℓ_n. A cap = |S̃₀| < ℓ_n would keep GROW and lose the GEN/PXN discovery guarantees (e.g. GEN (C3) needs a ≥ 2^{v̄}−2;
  PXN (T) needs a ≥ c). Append to that cell: "; all results simultaneously only for caps $\ge\max(\ell_n,|\tilde S_0|)$
  (Lemma~\ref{lem:cap} needs $a\ge\ell_n$)".
- (b) **e4′ does not cover GROW.** e4′(i) allows "a replacement returning the unique maximiser whenever it is unique"
  (`s5_hpm.tex:16`). GROW needs the emitted centre to be *some* maximiser of γ₀ even when ties exist: the sandwich gives
  S₀ ⊆ S̃ ⊆ Q for every maximiser, not uniqueness (`C-GROW/lemmas/00_MAIN.md:31-33`). A replacement admissible under e4′
  may return a non-maximiser under ties. The coded routine is fine (W1-N3 (a): `res.S` is always a smallest-size
  maximiser, truncated or not), and so is TDP. Yet `s1_setting.tex:32` says e4 is "replaced by the weaker e4′" without
  restriction. Replace the parenthesis with "(for PXN, GEN and M5(b1-LH) replaced by the weaker e4′, §\ref{sec:e4}; for
  GROW by `the emitted centre is some maximiser of $\gamma_0$', which the coded routine satisfies by W1-N3(a); delivery
  keeps e4 with TDP-IMPL)".

**5. MINOR — map cell `s2_map.tex:18` (Thm S row, status column).**
The cell "C-DLV \st{PARTIAL} (Prop.~F: \st{PROVED-CHECKED for the patched calibration law})" is attached to the analog
cell's "(Prop.~\ref{prop:F})". That label is the A1-corrected form, which is not councilled. Replace with
"C-DLV \st{PARTIAL}; Prop.~F with cap $\ell_n$ (C-DLV form): \st{PROVED-CHECKED for the patched calibration law};
corrected form with cap $a_n$ (Prop.~\ref{prop:F}): A1 \st{HOLDS-WITH-AMENDMENTS}, not councilled".

**6. MINOR — map row Thm 4 (`s2_map.tex:21`) conflates hypothesis and conclusion.**
"Condition 4: density consistency at the KL projection f_0, a.s." In SL (p.957), Condition 4 is the second-moment
range condition E{(aᵀx_s)²} < ∞ for |a_i| ≤ δ. The *conclusion* (18) is π[{f ∈ 𝒫_s : d(f₀,f) > ε} | D_n^s] → 0 a.s.
Replace with: "fixed candidate subset $\mathbf s$, Condition~4 (finite second moments of $a^\top x_{\mathbf s}$, $|a_i|\le\delta$),
prior positive on all models; conclusion (18): a.s.\ posterior consistency at the KL projection $f_0$".

**7. MINOR — the two "MR1"s are unlabelled in three places.**
`s5_hpm.tex:60` says "the \textbf{method requirement MR1}", which C-PACK uses for its MR1 = "LS0 centre = coded start
mode" (`s5_hpm.tex:16`, `s7_impl.tex:13`). `s7_impl.tex:57` ("What survives under MR1") and `s8_scope.tex:13` ("with
MR1") are also bare. Write "C-GROW MR1" in all three. Optionally add one sentence in §1.3: "C-PACK MR1 (LS0 centre) and
C-GROW MR1 (LS0 cap) are different requirements."

**8. MINOR — Lemma CAP's (L1) asserts more than its citation, and the metadata list omits the certificate card.**
`s7_impl.tex:28` says "only the HPM running best, the stores, flags and archives are updated after it [LS0]",
citing `SoP/02_method.tex:490-494`. Those lines fix LS0's position and say its scores join the scored set and stores.
They do not state the "only". The proof uses (L1) only for "nothing before LS0 depends on the cap, and the potential
status is fixed before LS0", which the citation does support. Also, the certificate card (`02_method.tex:538ff.`,
store-based Z_𝒯) is computed from the post-LS0 stores, so it can differ between caps. Fixes:
- Reword (L1) to "LS0 is the last search: it runs after the final local search and after the $c_4$ search ($R'>4$);
  nothing computed before it depends on its cap, and its outputs enter the HPM running best, the stores, flags,
  archives and the post-hoc card".
- Add "the certificate card's store-based quantities" to the "Flags and metadata" bullet (`s7_impl.tex:67`).

**9. MINOR — §1's definition of e4 drops its content.**
`s1_setting.tex:32` reads "e4 the emitted LS0 centre is the prescribed start-mode maximiser". The source
(`SoP/04_theory.tex:86`) is "= the prescribed **smallest-size, lexicographically smallest** start-mode maximiser (DP
invariant N3 OPEN)". Prop F and the GEN/GROW premise lists keep e4 verbatim, and TDP-IMPL is defined relative to this
choice, so restore the tie rule.

**10. NIT — SL0(vi) (`s3_posterior.tex:24`) omits the sharpness conditions.** The source requires "1 ≤ s₀ ≤ K and s₀ < p"
(`I4_SL_corollaries.md:26-27`). Insert "(when $1\le s_0\le K$ and $s_0<p$)".

**11. NIT — undefined symbols.**
- S†_𝒞 (exact HPM) in Thm MIS (i).
- N, μ_c and X_{c,𝒞} in Thm F (contrast coordinates, N = n − 1).
- s* in GEN (C1).
- In the map's Thm 1 row, "‖x_i‖ ≤ 1": SL write |x_i| ≤ 1, a uniform bound on each predictor, not a column norm.

**12. NIT — ξ_q row.** SL write "π(t ⊂ ξ_q) →^p 1" (p.956). The map's "P*(t ⊆ ξ_q) → 1" is a reasonable reading, but quote
SL's form and give the reading.

**13. NIT — PXN (C) drops the stronger conclusion.** It omits "P(𝒪∩{Ŝ⁺=S₀}) − (1−P(U)) → 0, and → 1−u whenever P(U)→u"
(`00_statement_and_conventions.md:116-118`). Dropping it is harmless, but the paper may want it.

**14. NIT — unsourced implementation-state claims.**
- "merged on branch `w1c/ls0-merge`" (`s1:20`, `s7:12,14,15`) and "adopted by HQ … behind a switch" (`s6:4`, `s7:16`)
  have no repository source. The writer did not read the branch, and no C-ENG folder exists in `Theory_work/Wave1C/`.
  Label them "per HQ; not verified by the writer" until the C-ENG report is folded in, as §7 already promises.
- `\sopdate` = 2026-11-09 is also used as the "state" date. Check it against the commit date.

## Summary

The chapter is careful, honest and faithful. Statements match their sources after F1's amendments, statuses are verbatim
with nothing upgraded, and the scope list is complete. The two new pieces hold up under attack:
- **Lemma CAP** is correct: the prefix, discovery monotonicity and the joint-with-output bound, with correct branch
  bookkeeping, and with GEN (C6) correctly not transferred.
- **The Proposition F assembly** is correct as an ideal-machine theorem: total fallback, A1's envelopes (with the
  n⁵log³n vs n⁶ comparison verified) and pathwise consistency through CAP(a).

The main defect (finding 1) is a scope slip: Theorem D, Cor. D′'s delivery form and CONFIG are cap-ℓ_n results. The
chapter drops that cap locally and over-transfers D′ to the MR1 method. §7 discloses the underlying fact, so this is
MAJOR, not BLOCKING, and it is fixed by three short insertions. Findings 2–9 are short wording and qualification fixes.

SCORE: 8.5/10; GATES: G1 PASS (finding 1 required) · G2 PASS · G3 PASS · G4 PASS · G5 PASS · G6 PASS
