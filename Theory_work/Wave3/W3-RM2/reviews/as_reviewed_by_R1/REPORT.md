# W3-RM2 — REPORT to Theory HQ (Theorem 3 at polynomial leakage: |Q| ≤ n^b, b < ½)

> **Flags (read first).**
> 1. **What is proved is "(V) + (L^b) + a lattice-width condition (W)", for every b < ½ (the brief asked b < ¼) — not
>    "(V) + (L)" alone.** (W) is a deterministic condition on (X, S₀, Q): the expected largest excess of a Gaussian
>    projection on the lattice's residual directions over a size-dependent level tends to −∞. It contains the
>    parent's lattice conditions, has primitive sufficient forms and verified examples at polynomial |Q|. For the
>    event the route uses it is sufficient when the gap → −∞ and obstructed when the gap → +∞; a bounded gap is
>    undetermined; nothing is claimed about its necessity for the reported model. Removing it is path-level (O1).
> 2. **The Gaussian-row form came out stronger than targeted** (HQ riders P3, T6, both succeeded): the leak bound
>    o(√(log n/n)) is asked at every conditioning set — the same quantifier as the fixed-design condition — and the
>    localisation clause needs no rate. Consequence for the examples: polynomial covariance decay needs **α > 2**
>    where W2-LOC2:Thm-Poly needs α > 17/2.
> 3. **The statement changed twice after the lock, each time by an HQ decision** (PROTOCOL item 3): v1.3 (CP1: signal
>    floor (BM-W), (W) as a diverging gap) and v1.4 (CP2 riders: Form R leak hypothesis). Each change weakens a
>    hypothesis; the locked v1.2 theorem is a special case. Each was checked by a fresh reviewer (SC1, SC2).
> 4. **Conditional:** (C1) on SOP:TH09@1.0.0 (Theorem 1) only; (C2) on W2-APP:POST@1.0.1 only; examples E2, E3 also
>    on W2-LOC2:Lemma-BC and Lemma-IR ("PROVED (by this seat, unchecked)"); all on the named implementation premises
>    (EX-A, EX-S, SR, GUARD-W, OP-LS0 in the shipped configuration, complete scans). No delivery claim. No method
>    change requested.
> 5. **RM2-F ⇒ RM-F and RM2-R ⇒ RM-R** (hypotheses and conclusions): the two theorems are CANDIDATES to supersede the
>    parent's (HQ decides at CP3; RM is a package headline, owner informed).
> 6. Limits observed in the boundary probes (LS0 re-implementation only): far outside the leak condition (nominal
>    η = 1, n = 1600) LS0 stopped at its shipped cap before S₀ in 4 of 6 runs. Everywhere else — b up to 0.75, a
>    nominal width-stress design, a weak truth, leak near the frontier — it ended at S₀ (202/202).

## 1. RESULT

**All claims (C1)–(C6) of `STATEMENT.md` v1.4 are proved, and every lemma has a blind cross-family check with no
FATAL or MAJOR finding** (LC1-A/B, LC2-A/B/C; independent mid-point MP1: "the key lemma stands"). Kill budgets: key
lemma attempt 1 of 3; (P7) attempt 1 of 2; riders P3 and T6 one attempt each, both succeeded. The exhaustive sweep
(SW1, Astra, blind) verified (C1)–(C4) and every bridge (P0)–(P10) as stated: 0 FATAL, 2 MAJOR — both on records (the
energy-constant range in the examples; the wording of the width-stress probe B2) — 4 MINOR, 1 NIT, all applied. The
better-theorem review on the final statement (BT2) found 5 adoptable refinements and 2 ticket-size ones, none
changing the headline; the lead recommends adopting them in one revision v1.5 with the riders T2/T4, so the claims
carry **headline-strength pending** (PROTOCOL rule 10) until HQ decides. The council is recorded in §4 when it
completes; until the council passes and HQ's acceptance audit runs, every status below is "PROVED (by this seat, unchecked)" with its
check record — not PROVED-CHECKED.

## 2. The statement as proved (`STATEMENT.md` v1.4; proofs in `lemmas/`)

Setting, method objects, events and the core RM-0 are the parent's (W3-RM:RM-0@1.0.0, W3-RM:E4@1.0.0); code pins:
LS0's centre, cap and scan (CORE `cpp/v3_core.cpp:465-476`, `cpp/v3_engine.h:392-414`).
* **(C1) RM2-F, fixed design.** Theorem 1's conditions (T1-F), floors (FL), visibility (V), a deterministic leak set
  Q ⊇ S₀ with **|Q| ≤ n^b**, leak level η outside Q, **b < β(η, A) = ½ − η/2 − √(2Aη)**, the signal floor (BM-W)
  (nθ*²_min ≫ d_n² + log n, d_n the truth-removal width; implied by nθ*²_min ≫ |Q| + log n), and **(W)**: 𝔴⁰_n → −∞.
  Then there is one data event of probability → 1 on which every admissible output run reports Ŝ⁺ = S₀; LS0 makes
  |S̃₀ ∖ S₀| ≤ n^b deletions, its archive is certified, the shipped cap is never binding.
* **(C2) RM2-R, Gaussian rows.** (T1-R), (FL-R), (V-R) = PTV, a deterministic Q with |Q| ≤ n^b, **(L-gain-R)**:
  |Cov(W_l, W_j | W_U)| ≤ ϖ_n = o(√(log n/n)) for every l ∉ Q, |U| ≤ 15, truth j ∉ U; **(L-loc-R)**: neighbourhoods
  |H_l| ≤ n^ρ outside which columns are conditionally uncorrelated with l and with the truths up to r_n → 0;
  **15ρ + b < ½**; and (W-R): (W) on the realised design with probability → 1 (sufficient: the population
  reference/atom conditions (D-R^b), or local regressions (D-loc^b)). Same conclusions under the joint law.
* **(C3) Width lemmas.** (a) 𝔴⁰_n → −∞ ⇒ whole-lattice no-addition, failure probability ≤ exp(−(𝔴⁰_n)²/8) + o(1)
  (n^{−c*} under the fixed-fraction form); (b) 𝔴⁰_n → +∞ ⇒ whole-lattice no-addition has probability → 0;
  (c) sufficient forms (W-δ), (W-unif), (W-χ), (W-ref), (W-loc).
* **(C4)** RM-F and RM-R are special cases. **(C5)** Examples (`lemmas/L6_examples.md`): the parent's examples;
  polynomial decay α > 2 in both forms; one truth with n^b weak proxies (every b < ½); one equicorrelated group
  (b < 3/10). **(C6)** `SHARPNESS.md`.
Not claimed: STATEMENT §6 (no lattice condition; b ≥ ½; bounded width gap; necessity for the conclusion; delivery).

## 3. Status per clause

| Clause | Content | File | Check record (reviewer, file in `reviews/`) |
|---|---|---|---|
| (P0) Toolkit-b | score toolkit at actual cardinalities, self-contained | `lemmas/L0_toolkit_b.md` | LC1-A Sol: V-W-A (1 MINOR applied), `LC1A_L0L1_check_sol.md`; MP1 re-derived |
| (P1) SAND-F^b | fixed-design sandwich, b < β(η, A) | `lemmas/L1_sandF_b.md` | LC1-A Sol: VERIFIED; MP1 re-derived |
| (C3)(a) NA-W | no-addition from the width gap, with rate | `lemmas/L2_width.md` §1 | LC1-B Sol: VERIFIED, `LC1B_L2L3_check_sol.md`; MP1 re-derived |
| (C3)(b) W-conv | converse for no-addition | `lemmas/L2_width.md` §2 | LC1-B Sol: V-W-A (wording applied); MP1 re-derived |
| (C3)(c) W-suff | five sufficient forms | `lemmas/L2_width.md` §3 | LC1-B Sol: VERIFIED; MP1 re-derived |
| (P2) TL-F^b | truth removal under (BM-W) | `lemmas/L2_width.md` §4 | LC1-B Sol: VERIFIED; MP1 re-derived |
| (C1) RM2-F | assembly; conditional on SOP:TH09@1.0.0 | `lemmas/L3_assemblyF.md` | LC1-B Sol: VERIFIED; MP1 Astra: stands, `MP1_midpoint_astra.md` |
| (C4) Cont-F | RM2-F ⇒ RM-F | `lemmas/L3_assemblyF.md` | LC1-B Sol: VERIFIED |
| (P7) SAND-R^b | Gaussian-row sandwich, product-form leak condition | `lemmas/L4_sandR_b.md` | LC2-A Astra: V-W-A (1 MINOR applied), `LC2A_L4_check_astra.md`; reviewer's own stress test |
| (P8) F-to-R | no-addition and truth removal under Gaussian rows | `lemmas/L5_formR.md` §1 | LC2-B Sol: VERIFIED, `LC2B_L5_check_sol.md` |
| (P9) D-to-W | (D-loc^b) ⇒ (D-R^b) ⇒ (W-R) | `lemmas/L5_formR.md` §2 | LC2-B Sol: P9, D-loc^b VERIFIED; P9a V-W-A (2 MINOR applied) |
| (P10) POST-R | posterior input; p = 1 endpoint proved; conditional on W2-APP:POST@1.0.1 | `lemmas/L5_formR.md` §3 | LC2-B Sol: VERIFIED |
| (C2) RM2-R | assembly; conditional on W2-APP:POST@1.0.1 | `lemmas/L5_formR.md` §4 | LC2-B Sol: VERIFIED |
| (C4) Cont-R | RM2-R ⇒ RM-R | `lemmas/L5_formR.md` §4 | LC2-B Sol: VERIFIED |
| (C5) E2 Ex-PolyR | Gaussian rows, polynomial decay α > 2; conditional on Lemma-BC, Lemma-IR | `lemmas/L6_examples.md` E2 | prover Sol; LC2-C Opus: V-W-A (applied), `LC2C_L6_check_opus.md` |
| (C5) E3 Ex-PolyF | exact Gram, polynomial decay α > 2; conditional on Lemma-BC, Lemma-IR | `lemmas/L6_examples.md` E3 | prover Sol; LC2-C Opus: V-W-A (applied) |
| (C5) E4 Ex-Proxy | one truth, n^b weak proxies, b < ½ | `lemmas/L6_examples.md` E4 | prover Sol; LC2-C Opus: VERIFIED |
| (C5) E5 Ex-Equi | equicorrelated group, b < 3/10 | `lemmas/L6_examples.md` E5 | prover Sol; LC2-C Opus: VERIFIED (not sharp) |
| (C6) | sharpness record | `SHARPNESS.md`, `numerics/RESULTS.md` | numerics: 208 boundary runs; K1–K13 lemma checks, no violation |
Every lemma status is "PROVED (by this seat, unchecked)" plus the check record above; inherited inputs keep their
recorded statuses (STATEMENT §5). E1 (inherited examples) is (C4) applied to the parent's examples.

## 4. Review trail (replies verbatim in `reviews/`, each with a disposition file)

| round | seat | object | verdict |
|---|---|---|---|
| SL1, RC1, RC2 | Sol | statement lock v1.0 → v1.2 | LOCK WITH CHANGES → reconciled → "editorial/record only — v1.2 can be locked" |
| BT1 | Astra, blind | better theorem on v1.2 | P1, P2 ADOPT (HQ, → v1.3); P3 worth a ticket (→ rider, done in v1.4) |
| SC1, RC3 | Sol | v1.2 → v1.3 | ACCEPT WITH CHANGES (records) → RESOLVED |
| LC1-A, LC1-B | Sol, blind | L0–L3 | no FATAL/MAJOR; 2 MINOR, 1 NIT applied |
| MP1, RC4 | Astra blind; Sol | independent mid-point on L0–L3, (C1) | CONTINUE WITH CHANGES (3 MINOR records, 1 NIT) → RESOLVED |
| PV1 | Sol (prover) | L6 examples | written; checked by LC2-C |
| LC2-A | Astra, blind | L4 (P7, with P3 and T6) | VERIFIED-WITH-AMENDMENTS; no FATAL/MAJOR |
| LC2-B | Sol, blind | L5 | VERIFIED (P9a with 2 MINOR); no FATAL/MAJOR |
| LC2-C | Opus (Claude Work), blind | L6 | VERIFIED / V-W-A (3 MINOR, 3 NIT); no FATAL/MAJOR |
| SC2 | Sol | v1.3 → v1.4 | ACCEPT WITH CHANGES (1 MAJOR notational, 3 MINOR), applied |
Dispositions: `SL1_`, `RC1_`, `BT1_`, `SC1_`, `LC1_`, `MP1_`, `LC2_disposition.md`. No review layer skipped.
| RC5 | Sol | diff check of the 13 LC2-round items | all RESOLVED; "editorial/record only" |
| SW1 | Astra, blind | exhaustive sweep of the whole package | (C1)–(C4), (P0)–(P10) VERIFIED; (C5), (C6) V-W-A: 0 FATAL, 2 MAJOR (records), 4 MINOR, 1 NIT, applied (`SW1_disposition.md`) |
| BT2 | Astra, blind | better theorem on the final statement v1.4 | 5 ADOPT NOW, 2 WORTH A TICKET, 0 SPECULATIVE; dispositions in `BT2_disposition.md` (recommended: v1.5 after the council) |
The council round is appended here when it completes.

## 5. Registry items (PROTOCOL item 7)

**Assumption ids.** Inherited: T1-F, T1-R, FL-16, FL-Q, FL-R, V, V-R, V_b, L_b, L-gain, L-feas. New: L-size-b
(|Q| ≤ n^b, b < β(η, A)), L-size-b-R (|Q| ≤ n^b, b < ½), BM-W, W, W-delta, W-unif, W-chi (= parent's N-χ), W-ref, W-loc,
L-gain-R (v1.4: ϖ_n = o(√(log n/n)) at every conditioning set), L-loc-R (v1.4: r_n → 0), L-R-b-loc (the localised
sufficient form), H-size-rho (|H_l| ≤ n^ρ, 15ρ + b < ½), W-R, D-R-b, D-loc-b. Interface properties consumed: [POST],
[SAND(Q)], [TL(Q)], [NA(Q)], [E4]. Where each enters: `ASSUMPTION_MAP.md`.
**`implies`.** RM2-F ⇒ RM-F; RM2-R ⇒ RM-R; (BM-Q) ⇒ (BM-W); (W-loc) ⇒ (W-ref) ⇒ (W-unif) ⇒ (W-δ) ⇒ (W);
(W-χ) ⇒ (W-δ); parent's (N-χ) = (W-χ), (N-D)(i) ⊂ (W-ref); (D-loc^b) ⇒ (D-R^b) ⇒ (W-R); parent's (D-R) ⇒ (D-R^b);
(L-R-b-loc) ⇒ (L-gain-R) ∧ (L-loc-R); parent's (L-R) ⇒ (L-R-b-loc); the polynomial-decay class of W2-LOC2:Thm-Poly
(α > 17/2) ⊂ example E2 (α > 2).
**Sharpness record** (`SHARPNESS.md`; observations only where numerics are quoted).
* |Q| ≤ n^b: enters one line of each proof (junk-exclusion margin); sufficient budget; observed b up to 0.75: LS0 at
  S₀ 48/48. ARTEFACT of the route; the conclusion beyond ½ is open (O1).
* (W): sufficient (gap → −∞), obstructed for the route (gap → +∞), bounded gap undetermined; observed in a
  nominal width-stress design (improving additions found at probed lattice sets): LS0 at S₀ 48/48. Not derived from (V), (L). Open: O1, O5.
* (BM-W): sufficient; weaker than the parent's (BM-Q); necessity not studied.
* Form F leak level: as the parent; observed failure of the LS0 probe under the shipped cap at nominal η = 1.
* Form R leak scale o(√(log n/n)) and localisation r_n → 0: two artefacts of the parent removed; exact scale
  κ√(log n/n) open (O3′); the count n^{15ρ} is an artefact of reference counting.
* Examples: α > 2 is Lemma-IR's cutoff (budgets need α > 1): O6; equicorrelated group beyond 3/10: O4′.

## 6. Open items and recommended next steps

| id | item | recommendation |
|---|---|---|
| O1 | no lattice condition; b ≥ ½ (path-level control of LS0 with cap accounting) | the real next theorem; hard; separate ticket with a kill budget |
| O2 | counting form of (L) + RM-0 on a down-closed sub-lattice (rider T2(c)) | with the T2/T4 riders after the council |
| O3′ | Form R frontier at leak scale κ√(log n/n) | moderate; low priority |
| O4′ | equicorrelated group for 3/10 ≤ b < ½ (reviewer's sketch: (W) up to 3/8, fails beyond) | cheap; if confirmed, a clean instance where the lattice route fails and O1 is needed |
| O5 | bounded width gap | open |
| O6 | polynomial decay α ∈ (1, 2] | needs a Jaffard-type inverse-decay lemma |
**Recommended revision v1.5 (after the council, one change check):** BT2 P1 (additive signal margin), P2 (exponent
s²/2 in (C3)), P3 (width lemmas for |Q| log n/n → 0), P4 (entropy budget h in (D-R^b)), P5 (quantitative (W-ref)), P7
(equicorrelated example to b < 3/8, if the proof closes), together with the riders T2 (delivery wording, unique-mode
event, T2(c)) and T4 (constant-level (V)) that HQ scheduled after the council. Supersession of RM-F / RM-R by RM2-F / RM2-R: HQ at CP3.

## 7. Files (`Theory_work/Wave3/W3-RM2/`)

STATEMENT.md (v1.4), PLAN.md, ASSUMPTION_MAP.md, SHARPNESS.md, REPORT.md, LOG.md, CHECKPOINT_1–2.md;
lemmas/ L0_toolkit_b, L1_sandF_b, L2_width, L3_assemblyF, L4_sandR_b, L5_formR, L6_examples;
numerics/ (SPEC, RESULTS §1–§6, rm2_common.R, run_all.R, validate.R, summarise.R, lemma_checks.R, check_identity.R,
formR_checks.R and outputs; results_raw.csv, summary.csv); reviews/ (INPUTS.txt, manifests, briefs, replies
verbatim, dispositions, reviewed-text snapshots).

## Registry block

Registry state at ingest (HQ CP1 decision): W3-RM2:RM2-F and W3-RM2:RM2-R enter as CANDIDATES that imply
W3-RM:RM-F and W3-RM:RM-R; supersession is decided at CP3. One status per claim. `status_source` lines are the rows
of §3. Gates and `council` are filled from the council round.

```
REGISTRY
claim: W3-RM2:RM2-F | kind: theorem | statement: STATEMENT.md:(C1) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED; MP1 CONTINUE WITH CHANGES (no FATAL/MAJOR); conditional on SOP:TH09@1.0.0 | status_source: REPORT.md:68
assumptions: A:T1-F ; A:FL-16 ; A:FL-Q ; A:V ; A:L-gain ; A:L-feas ; A:BM-W (new | signal floor at the truth-removal width | theta_min^2 (n-1) phi0^2 / (sigma^2 (d_n^2 + log n)) -> infinity | STATEMENT.md §1,§3.1 | shared yes | P2 TL-F^b) ; A:L-size-b (new | polynomial leakage size | |Q| <= n^b, b < beta(eta,A) | STATEMENT.md §3.1 | shared yes | P1 SAND-F^b) ; A:W (new | lattice width gap | w0_n -> -infinity | STATEMENT.md §1,§3.1 | shared yes | P3 NA-W)
consumes: P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4
conclusion: reported-model: one data event of probability -> 1 on which every admissible output run reports S0 | rate: none claimed | scope: fixed design; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; SOP:TH09@hyp ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-F-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt ; W3-RM2:W-suff@stmt ; W3-RM2:W-conv@stmt
implies: W3-RM:RM-F (special case |Q| polylog, (W) from (N-chi) or (N-D)(i) through W3-RM2:W-suff; claim W3-RM2:Cont-F)
sharpness: A:W = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_width.md §2, Lemma W-conv: gap -> +infinity obstructs whole-lattice no-addition; not for reporting; bounded gap undetermined) ; A:L-size-b = ARTEFACT (evidence: lemmas/L1_sandF_b.md §3(b); sufficient budget of the junk-exclusion argument; necessity open) ; A:BM-W = NONE (sufficient; necessity not studied) ; A:V, A:L-gain, A:FL = as W3-RM
binding: A:W route obstruction via W3-RM2:W-conv: gap -> +infinity forces P(NA(Q)) -> 0; gap -> -infinity is sufficient; bounded gap undetermined [whole-lattice route only] ; A:L-size-b enters P:SAND(Q) via the junk-exclusion margin [artefact-threshold]
gates: correct:PENDING(reviews/LC1B_L2L3_check_sol.md) ; lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ; better:PENDING(reviews/BT1_better_theorem_astra.md)
council: none yet

claim: W3-RM2:RM2-R | kind: theorem | statement: STATEMENT.md:(C2) | premises: STATEMENT.md:§1,§3.2
status: PROVED (by this seat, unchecked); LC2-B VERIFIED; conditional on W2-APP:POST@1.0.1 | status_source: REPORT.md:74
assumptions: A:T1-R ; A:FL-R ; A:V-R ; A:L-feas ; A:L-gain-R (new in this form | leak bound at every conditioning set | |Cov(W_l, W_j | W_U)| <= varpi_n = o(sqrt(log n/n)), l outside Q, |U| <= 15, truth j outside U | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:L-loc-R (new in this form | localisation without rate | conditional covariances with columns outside H_l at most r_n -> 0 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:L-size-b-R (new | polynomial leakage size, Gaussian rows | |Q| <= n^b, b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:H-size-rho (new | reference neighbourhood size | |H_l| <= n^rho, 15 rho + b < 1/2 | STATEMENT.md §3.2 | shared no | P7 SAND-R^b) ; A:W-R (new | lattice width on the realised design | exists deterministic t_n -> infinity: P(W0_n intersect {w0_n <= -t_n}) -> 1 | STATEMENT.md §3.2 | shared yes | P8 F-to-R)
consumes: P:POST ; P:SAND(Q) ; P:TL(Q) ; P:NA(Q) ; P:E4
conclusion: reported-model: as RM2-F under the joint law of (X, eps) | rate: none claimed | scope: Gaussian rows; s0 fixed; p <= n^A (p >> n allowed); |Q| <= n^b, |H_l| <= n^rho
depends_on: W3-RM:RM-0@stmt ; W3-RM:E4@stmt ; W2-APP:POST@hyp ; W3-RM2:SAND-R-b@stmt ; W3-RM2:F-to-R@stmt ; W3-RM2:POST-R@stmt ; W3-RM2:D-to-W@stmt ; W3-RM2:W-conv@stmt
implies: W3-RM:RM-R (special case, (L-R) through the localised sufficient form, (W-R) from (D-R) through W3-RM2:D-to-W; claim W3-RM2:Cont-R)
sharpness: A:W-R = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_width.md §2 applied conditionally; positive diverging gaps obstruct whole-lattice no-addition; bounded gaps undetermined; no necessity for reporting claimed) ; A:H-size-rho = ARTEFACT (evidence: lemmas/L4_sandR_b.md §4; reference counting) ; A:L-size-b-R = ARTEFACT (evidence: lemmas/L4_sandR_b.md §6(b); sufficient budget; necessity open) ; A:L-gain-R = WEAKENABLE (evidence: lemmas/L4_sandR_b.md §7 item 4; exact scale kappa sqrt(log n/n) not derived) ; A:L-loc-R = NONE (evidence: SHARPNESS.md §3; needed by this proof at r_n -> 0 only)
binding: A:H-size-rho enters P:SAND(Q) via the reference count n^{15 rho} [artefact-threshold]
gates: correct:PENDING(reviews/LC2B_L5_check_sol.md) ; lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ; better:PENDING(reviews/BT1_better_theorem_astra.md)
council: none yet

claim: W3-RM2:Toolkit-b | kind: lemma | statement: STATEMENT.md:(P0) | premises: STATEMENT.md:§1
status: PROVED (by this seat, unchecked); LC1-A VERIFIED-WITH-AMENDMENTS, applied | status_source: REPORT.md:62
depends_on: C-GROW:L0.1@proof ; C-GROW:L0.2@proof
claim: W3-RM2:SAND-F-b | kind: lemma | statement: STATEMENT.md:(P1) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-A VERIFIED | status_source: REPORT.md:63
depends_on: C-GROW:L3@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:TL-F-b | kind: lemma | statement: STATEMENT.md:(P2) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED | status_source: REPORT.md:67
depends_on: C-GROW:L2.1@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:NA-W | kind: lemma | statement: STATEMENT.md:(C3)(a) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED | status_source: REPORT.md:64
depends_on: C-GROW:L2.2@proof ; W3-RM2:Toolkit-b@stmt
claim: W3-RM2:W-conv | kind: lemma | statement: STATEMENT.md:(C3)(b) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED-WITH-AMENDMENTS, applied | status_source: REPORT.md:65
depends_on: W3-RM2:Toolkit-b@stmt
claim: W3-RM2:W-suff | kind: lemma | statement: STATEMENT.md:(C3)(c) | premises: STATEMENT.md:§1,§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED | status_source: REPORT.md:66
assumptions: A:W-delta (new) ; A:W-unif (new) ; A:W-chi ; A:W-ref (new) ; A:W-loc (new)  [alternatives, not a conjunction: each implies A:W]
implies: A:W-delta => A:W ; A:W-unif => A:W-delta ; A:W-chi => A:W-delta ; A:W-ref => A:W-unif ; A:W-loc => A:W-ref ; A:BM-Q => A:BM-W
depends_on: C-GROW:L2.3@proof
claim: W3-RM2:Cont-F | kind: lemma | statement: STATEMENT.md:(C4) | premises: STATEMENT.md:§3.1
status: PROVED (by this seat, unchecked); LC1-B VERIFIED | status_source: REPORT.md:69
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt ; W3-RM:RM-F@stmt
claim: W3-RM2:SAND-R-b | kind: lemma | statement: STATEMENT.md:(P7) | premises: STATEMENT.md:§1,§3.2
status: PROVED (by this seat, unchecked); LC2-A VERIFIED-WITH-AMENDMENTS, applied | status_source: REPORT.md:70
depends_on: C-GROW:L6.4@proof ; W3-RM:SAND-R@proof ; W3-RM2:Toolkit-b@stmt ; W3-RM2:SAND-F-b@proof:per-block optimality (1.1) and count (2.1)
claim: W3-RM2:F-to-R | kind: lemma | statement: STATEMENT.md:(P8) | premises: STATEMENT.md:§1,§3.2
status: PROVED (by this seat, unchecked); LC2-B VERIFIED | status_source: REPORT.md:71
depends_on: W3-RM2:Toolkit-b@stmt ; W3-RM2:TL-F-b@stmt ; W3-RM2:NA-W@stmt
claim: W3-RM2:D-to-W | kind: lemma | statement: STATEMENT.md:(P9) | premises: STATEMENT.md:§1,§3.2
status: PROVED (by this seat, unchecked); LC2-B VERIFIED-WITH-AMENDMENTS, applied | status_source: REPORT.md:72
assumptions: A:D-R-b (new) ; A:D-loc-b (new)  [alternatives: A:D-loc-b => A:D-R-b => A:W-R for every delta0 in (0, 1 - 2b)]
depends_on: W2-LOC2:NA-R@proof ; W3-RM:D-loc@proof  [proof templates re-run at polynomial size; no conclusion of them is consumed outside its stated range]
claim: W3-RM2:POST-R | kind: lemma | statement: STATEMENT.md:(P10) | premises: STATEMENT.md:§1,§3.2
status: PROVED (by this seat, unchecked); LC2-B VERIFIED; conditional on W2-APP:POST@1.0.1 | status_source: REPORT.md:73
depends_on: W2-APP:POST@hyp
claim: W3-RM2:Cont-R | kind: lemma | statement: STATEMENT.md:(C4) | premises: STATEMENT.md:§3.2
status: PROVED (by this seat, unchecked); LC2-B VERIFIED | status_source: REPORT.md:75
depends_on: W3-RM2:RM2-R@stmt ; W3-RM2:SAND-R-b@proof:section 7 item 1 ; W3-RM2:D-to-W@stmt ; W3-RM:RM-R@stmt
claim: W3-RM2:Ex-PolyR | kind: proposition | statement: STATEMENT.md:(C5) | premises: lemmas/L6_examples.md:E2
status: PROVED (by this seat, unchecked); LC2-C VERIFIED-WITH-AMENDMENTS, applied; conditional on W2-APP:POST@1.0.1, W2-LOC2:Lemma-BC@1.0.0 and W2-LOC2:Lemma-IR@1.0.0 | status_source: REPORT.md:76
depends_on: W3-RM2:RM2-R@stmt ; W3-RM2:D-to-W@stmt ; W2-LOC2:Lemma-BC@hyp ; W2-LOC2:Lemma-IR@hyp
claim: W3-RM2:Ex-PolyF | kind: proposition | statement: STATEMENT.md:(C5) | premises: lemmas/L6_examples.md:E3
status: PROVED (by this seat, unchecked); LC2-C VERIFIED-WITH-AMENDMENTS, applied; conditional on SOP:TH09@1.0.0, W2-LOC2:Lemma-BC@1.0.0 and W2-LOC2:Lemma-IR@1.0.0 | status_source: REPORT.md:77
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt ; W2-LOC2:Lemma-BC@hyp ; W2-LOC2:Lemma-IR@hyp
claim: W3-RM2:Ex-Proxy | kind: proposition | statement: STATEMENT.md:(C5) | premises: lemmas/L6_examples.md:E4
status: PROVED (by this seat, unchecked); LC2-C VERIFIED; conditional on SOP:TH09@1.0.0 | status_source: REPORT.md:78
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt
claim: W3-RM2:Ex-Equi | kind: proposition | statement: STATEMENT.md:(C5) | premises: lemmas/L6_examples.md:E5
status: PROVED (by this seat, unchecked); LC2-C VERIFIED; conditional on SOP:TH09@1.0.0 | status_source: REPORT.md:79
depends_on: W3-RM2:RM2-F@stmt ; W3-RM2:W-suff@stmt
```
