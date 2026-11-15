# W3-RM2 — CHECKPOINT 2 (key lemma proved) — 2026-11-11

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-RM2`, no git state changed
(everything since 81ff7d6 is uncommitted; HQ commits). Run ends here; no work past this point without HQ's go.

## 0. Flags (read first)
1. **The Form F key lemma stands on its first attempt** (attempts used: 1 of 3, none failed). Independent mid-point
   MP1 (Astra, blind): **CONTINUE WITH CHANGES** — "The key lemma stands. I found no FATAL or MAJOR mathematical gap
   in L0–L3 or in (C1)". Its 3 MINOR + 1 NIT are record/wording corrections, all applied, and an independent
   Sol diff check (RC4) attests "editorial/record only — L0–L3 stand as reviewed by MP1".
2. **The fixed-design theorem (C1) RM2-F is proved and lemma-checked**, conditional on SOP:TH09 (Theorem 1) only:
   the toolkit is now self-contained, so the condition on W1-GEN:L1 drops. Not yet PROVED-CHECKED — the sweep and
   the council come at CP3.
3. **Nothing of Form R is written** ((C2), bridges P7–P10), nor the examples (C5), SHARPNESS, REPORT. The reviewer
   names P7 (Gaussian-row sandwich at n^{15ρ} references) as the step most at risk.
4. Wording discipline from MP1: (W) is a **sufficient** negative-gap condition with a positive-gap obstruction for
   whole-lattice no-addition; the bounded-gap regime is unresolved; no necessity for *reporting* is proved or
   refuted. b < β(η, A) is the margin of this proof, not a boundary. Supporting records now say exactly this.
5. Two HQ-side stops hit this leg (19:01 account fix, 19:06 interrupt). No work lost: the cancelled run had already
   applied the MP1 corrections; I re-verified them hunk by hunk against the saved reviewed texts.

## 1. Statement in force: `STATEMENT.md` v1.3
v1.2 LOCKED + HQ's two CP1 adoptions: **(BM-W)** (signal floor at the truth-removal width d_n, weaker than
(BM-Q)) and **(W) as a diverging width gap** 𝔴⁰_n → −∞, with the converse 𝔴⁰_n → +∞ and a no-addition failure rate.
Checked by SC1 (Sol): ACCEPT WITH CHANGES, both changes re-derived, four record corrections applied; RC3 (Sol diff
check): "editorial/record only — v1.3 stands as checked by SC1". No hypothesis or claim changed after SC1.

## 2. What is proved and checked (one status per claim; all files in `lemmas/`)
Every row: written by the lead ("PROVED (by this seat, unchecked)" in the file header), then a blind line-by-line
Sol lemma check, then the blind Astra mid-point. None is PROVED-CHECKED yet.

| claim / bridge | file | lemma check (Sol, blind) | mid-point MP1 (Astra, blind) |
|---|---|---|---|
| (P0) Toolkit-b: score toolkit at actual cardinalities, self-contained | `L0_toolkit_b.md` | LC1-A: VERIFIED-WITH-AMENDMENTS (1 MINOR: an unused elementary clause added) | re-derived; no finding |
| (P1) SAND-F^b: fixed-design sandwich at \|Q\| ≤ n^b, b < β(η, A); Lemma B1 | `L1_sandF_b.md` | LC1-A: VERIFIED (1 NIT). The bound on log k̃ is the only use of \|Q\| | re-derived ("every maximiser", common event); no finding |
| (C3)(a) / (P3) NA-W with NA-conv: gap → −∞ ⇒ whole-lattice no-addition, P(𝒵_nᶜ) ≤ exp(−(𝔴⁰_n)²/8); n^{−c*} under (W-δ) | `L2_width.md` §1 | LC1-B: VERIFIED | re-derived (factor 1/8, c*, exact cancellation); no finding |
| (C3)(b) / (P5) W-conv: gap → +∞ ⇒ P(NA(𝓛)) → 0 | `L2_width.md` §2 | LC1-B: VERIFIED-WITH-AMENDMENTS (1 MINOR, wording) | re-derived; "a converse for NA, not for reporting" |
| (C3)(c) / (P4) sufficient forms (W-δ), (W-unif), (W-χ), (W-ref), (W-loc) | `L2_width.md` §3 | LC1-B: VERIFIED (all five) | re-derived with constants; no finding |
| (P2) TL-W: truth removal under (BM-W), exact two-square identity; Lemma d | `L2_width.md` §4 | LC1-B: VERIFIED | re-derived incl. the cap endpoint \|T\| = K; no finding |
| **(C1) Theorem RM2-F** (assembly through W3-RM:RM-0, E4; conditional on SOP:TH09) | `L3_assemblyF.md` | LC1-B: VERIFIED | import of RM-0 at arbitrary q, LS0 pins, [POST], n₀ dependences checked; 1 NIT (wording of one sentence, fixed) |
| (C4), first half: RM2-F ⇒ RM-F | `L3_assemblyF.md` | LC1-B: VERIFIED | confirmed |

Also delivered, not a claim: an explicit bound for the search event P(𝒦_nᶜ) (CP1 item G2; `L3_assemblyF.md`).
Falsification numerics (`numerics/lemma_checks.R`, `check_identity.R`; RESULTS §5), K1–K7: **no violation** —
score remainders within the proved bounds on sets up to 400; production block tables obey the table expansion;
9600 lattice pairs: score increment = (Z² − a⁰²)/2 within [−0.69, 0.34]; the truth-removal identity to 1.2e-14
(re-run independently by LC1-B). They are attempts to break deterministic steps, not evidence for the asymptotics.

## 3. Review record of this leg
| round | seat | manifest | verdict | files (`reviews/`) |
|---|---|---|---|---|
| SC1 | Sol, statement change | 9af7889e… | ACCEPT WITH CHANGES; 2 MAJOR + 2 MINOR, records only | `SC1_statement_change_sol.md`, `SC1_disposition.md` |
| LC1-A | Sol, blind lemma check L0 + L1 | 0caea883… | no FATAL/MAJOR; 1 MINOR, 1 NIT | `LC1A_L0L1_check_sol.md`, `LC1_disposition.md` |
| LC1-B | Sol, blind lemma check L2 + L3 | 0caea883… | no FATAL/MAJOR; 1 MINOR | `LC1B_L2L3_check_sol.md`, `LC1_disposition.md` |
| RC3 | Sol, diff check of SC1 fixes | 0caea883… | SC1-1…4 RESOLVED; editorial/record only | `RC3_diffcheck_sol.md` |
| **MP1** | **Astra, blind mid-point** | 960c9069… | **CONTINUE WITH CHANGES**; 3 MINOR + 1 NIT; no FATAL/MAJOR | `MP1_midpoint_astra.md`, `MP1_disposition.md`, `as_reviewed_by_MP1/` |
| RC4 | Sol, diff check of MP1 fixes | b9c2675a… | 16 hunks, none substantive; MP1-1…4 RESOLVED; "editorial/record only — L0–L3 stand as reviewed by MP1" | `RC4_diffcheck_sol.md` |
Every review quotes its manifest digest; `manifest.py verify` passes on MANIFEST_RC4 (the tree as it stands now). No review layer skipped. Provers Claude, checkers OpenAI.

MP1's findings (all accepted): (1) "Gaussian floors iff b < ½" was a false necessity → sufficient bound only;
(2) "survives iff", "exact complexity condition", "route cannot do with less", unqualified "not necessary" in
PLAN/ASSUMPTION_MAP → margin-of-this-proof and sufficient-condition wording; (3) stale numerics counts in
ASSUMPTION_MAP → 208 runs, 204 at S₀, η = 1 cell 4 failures of 6, nominal classification, LS0-probe scope;
(4) "bounded convergence" in L3 → explicit ε-bound.

## 4. What MP1 adds beyond the verdict
* **(W) is not vacuous at polynomial |Q|**: the reviewer built a fixed-design witness — one truth with q = n^b weak
  proxies (correlation² ≍ log n/n with the truth), orthogonal outside columns — satisfying all of (C1)'s hypotheses
  with (W-loc), N_l = {truth}, L = 0, for every b < ½. A sketch; **candidate for the examples table, to verify.**
* A checklist for Form R (in `MP1_disposition.md`): P7 must redo selection removal uniformly over small conditioning
  sets through the deterministic references (citing the polylog theorem does not discharge it); P9 must write the
  passage from the joint crossing bound to the conditional mean; P8, P10 routine.

## 5. What is left
| item | content | risk |
|---|---|---|
| L4 (P7) SAND-R^b | Gaussian-row sandwich at \|H_l\| ≤ n^ρ, 15ρ + b < ½; parallel Sol prover + cross-family check, as in RM | **medium — the ticket's remaining risk** |
| P3 (HQ CP1 item 2) | Form R leak/localisation scales, one attempt inside L4; on failure → open item O3 | one-attempt budget |
| L5 (P8), (P9), (P10) → (C2), (C4) second half | conditional use of L0/L2 under Gaussian rows; (D-R^b) ⇒ (W-R); POST-R | low–medium (P9) |
| L6 (C5) examples | RM's examples by containment; exact-Gram polynomial decay α > 2; Form R α > 17/2; the MP1 witness; the equicorrelated candidate (verify or drop, O4) | low |
| SHARPNESS.md, REPORT.md + registry block | incl. status text "conditional on SOP:TH09"; W1-GEN:L1 edge dropped (toolkit self-contained) | low |
| reviews | Sol lemma checks of L4–L6; exhaustive sweep (Astra); council (one OpenAI seat + one Claude seat on Claude Work), ≤ 3 rounds; **better-theorem review repeated on the final statement** (v1.3 changed after CP1; rule 10 headline strength) | — |

**Estimate.** CP1 → CP2 took about 30 minutes of wall clock (three reviewer rounds) against my CP1 estimate of
4–6 h; I over-estimated. On that evidence: Form R proofs with their lemma checks ≈ 1–2 h wall clock if P7 goes
through on the first attempt; examples + SHARPNESS + REPORT + sweep + council + BT2 ≈ 1.5–3 h more, dominated by
reviewer rounds. Agents: 1 Sol prover, 3–4 Sol checks, 2 Astra (sweep, BT2), council 2 seats × ≤ 3 rounds, plus one
Claude cross-family check — every Claude agent on Claude Work at effort high.
**Fallback if P7 stalls** (kill budget for Form R to be set by HQ; I suggest 2 attempts): ship Form F alone —
(C1), (C3), (C4) first half are self-standing and checked — and record (C2) as OPEN. Cost: the only p ≫ n examples
live in Form R, so Form F alone is a weaker package item.

## 6. Decisions asked of HQ
1. **GO for the Form R leg** (L4 → L5, then L6, SHARPNESS, REPORT, sweep, council → CP3)? Recommended.
2. Kill budget for P7: **2 attempts**, then the fallback above? (P3 keeps its one-attempt budget.)
3. Add the MP1 witness (truth + n^b weak proxies) to (C5) as a Form F example once verified? Recommended: it is the
   simplest design showing the theorem at genuinely polynomial leakage.

## 7. Files (`Theory_work/Wave3/W3-RM2/`, uncommitted since 81ff7d6)
STATEMENT.md (v1.3), PLAN.md, ASSUMPTION_MAP.md, LOG.md, CHECKPOINT_2.md; lemmas/ (L0_toolkit_b, L1_sandF_b,
L2_width, L3_assemblyF); numerics/ (lemma_checks.R + out, check_identity.R + out, RESULTS §4–§5, all 208 runs);
reviews/ (briefs, manifests SC1/LC1/MP1/RC4, replies verbatim, dispositions SC1/LC1/MP1, reviewed-text snapshots,
INPUTS.txt per rule 15 as amended on main e52382f). HOLDS.md: no holds.
Agents in this leg: lead (Claude Fable 5.2, Claude Work); SC1, LC1-A, LC1-B, RC3, RC4 (Codex gpt-6.1-sol, high);
MP1 (Codex gpt-6-astra, high). Claude tally: CW 1 / CP 0. No NOTS use.
