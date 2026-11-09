# Final council round 3 — post-council editorial disposition (writer, 2026-11-09)

Round 3 PASSED: Sol 9.3 (ACCEPT, no findings), Opus 8.6; all six gates PASS in both seats (`C3_council_sol.md`,
`C3_council_opus.md`). Post-council editorial pass on HQ's instruction (as in the tickets' post-council fixes): Opus
findings 1–6 applied; no hypothesis or conclusion of any transcribed theorem changed. The one substantive addition
(finding 1) is an extra allocation condition for the C-ENG head code, using the reviewer's term.

| # | sev | exact change | location |
|---|---|---|---|
| 1 | MAJOR (non-gate) | Preflight facts updated to the current branch head `493579a`: commits `ef33f91`, `98fac03`, `72785fe` (reviews R07 REJECT→fixed, R08 APPROVE-WITH-FIXES, R09 APPROVE; no production change after `72785fe`) add an LS0 worst-case preflight charge (`ls0_archive` bytes; time estimate 2(ℓ_n+K+1)q(p)ŝ_K checked against `allocation$hours`); cited at `BRH/Theory_work/Wave1C/C-ENG/REPORT.md:63-81` and `BRH/Scripts/SMC_BVS/core/v3_fit.R:43-65`. The 8a27652 statement ("preflight does not include the LS0 term") is kept only as a historical claim, prefixed "At 8a27652". | s6_delivery.tex Remark (5); s7_impl.tex C-ENG MR1 bullet, intro sentence (reviewed vs current head), "Worst-case costs" bullet; s8_scope.tex implementation item |
| 1 | MAJOR (non-gate) | Proposition F allocation: added the reviewer's term, marked "Addition for the C-ENG head code (council round 3, Opus finding 1)": time_n ≥ P̄_LS0 := (ℓ_n+K+1)q(p)(τU_K+τ₀)/100 (U_K the operation count of the 200 timed size-K scores) and mem_n ≥ P_e + ls0_archive bytes (e = 0, 1). Remark (5) notes the new preflight exit lies outside C-DLV's P1 inventory and that an allocation also satisfying these terms is not refused by it. | s6_delivery.tex Proposition F, Allocation; Remark (5) |
| 2 | MINOR | Review trail and date through round 3: title source line lists drafts 5bcde3b, e95adc2, d315c1e and council rounds 1 (7481194), 2 (10b2090), 3 (25492e4, passed); agentnote and Lemma CAP reviewflag record rounds 1–2 not passed (round 2 Sol 7.9 / Opus 8.8) and round 3 passed (Sol 9.3 / Opus 8.6, all gates); provenance commit cell "5bcde3b (v1), e95adc2 (v2), d315c1e (v3)"; header date 2026-11-09 | consistency.tex \date and agentnote; s7_impl.tex reviewflag; s9_prov.tex Lemma CAP row; preamble.tex |
| 3 | MINOR | "model G is assumed on every realisation: … almost surely" → reviewer's text "model G is read as: X^r has nonconstant columns almost surely and ε ~ N_n(0, σ²I_n) is independent of X^r; Lemma S.1 verifies the first for fixed standardised designs and nonsingular Gaussian rows" | s6_delivery.tex Proposition F conclusion |
| 4 | NIT | 𝒮⁺ = "every model scored by the fit up to and including LS0, post-hoc certificate evaluations excluded" | s1_setting.tex §1.2 Reported HPM |
| 5 | NIT | (C6) bound → "$2(a_n+1)=2(\ell_n+|\tilde S_0|+1)$" | s7_impl.tex "Negative statements" |
| 6 | NIT | overfull boxes: the (H-MIS) and PXN (R) lines were already broken in v3 (d315c1e); the last one (provenance cell) fixed by rewording the C-ENG commit cell ("8a27652 493579a (reviewed / current head of the unmerged branch)"). Log: 0 overfull boxes. | s9_prov.tex C-ENG row |
| — | HQ item 3 | version tag → "v1.0 (final council passed, round 3)" | preamble.tex |

Status labels of A1's corrected Proposition F ("HOLDS-WITH-AMENDMENTS, not councilled") and of Proposition F-GROW
("PROVED (A2), checked by A3, not council-passed") are left verbatim; the chapter now records that the final council
(round 3) passed the chapter including them. Any relabelling is HQ's call. [Superseded: HQ decided to relabel; see the
section "HQ decision after round 3" below.]

Tooling: `citecheck.py` gains alias `BRH/` pinned to `493579a` (current head) beside `BR/` pinned to `8a27652` (reviewed
head, historical claims). Result: 186 citations, 0 problems. LuaLaTeX: 0 errors, 0 overfull boxes, 26 pages.

## HQ decision after round 3: relabelling (writer, 2026-11-09)
Rounds 2 and 3 of the final council were briefed to check Lemma CAP, Proposition F (A1's corrected form) and Proposition
F-GROW mathematically in full; round 3 passed (Sol 9.3, Opus 8.6, G3 PASS in both seats). Per HQ, every "not councilled" /
"not council-passed" label for these three items is replaced by the original audit verdict, kept verbatim, followed by
"; checked in full by the final council, round 3 PASSED (Sol 9.3, Opus 8.6)":
- consistency.tex agentnote (Lemma CAP; Prop F / F-GROW sentence);
- sections/s2_map.tex Thm S row (A1 HOLDS-WITH-AMENDMENTS; PROVED (A2), checked by A3);
- sections/s6_delivery.tex Prop F status box and Prop F-GROW status box; A3's inherited-qualification line now reads
  "A1's corrected statement was not councilled at the time of A3 (since checked in full by the final council, round 3)";
- sections/s7_impl.tex Lemma CAP review box; sections/s8_scope.tex delivery item;
- sections/s9_prov.tex council column of the A1, A2/A3 and Lemma CAP rows: "round 3 PASSED (9.3 / 8.6), checked in full".
The only remaining occurrence of "not council-passed" is the hidden citation token that verifies A3's own text
(A3_check_A2.md:31-39); it is not printed.

**Scope note.** The post-council allocation addition in Proposition F (the C-ENG head preflight term
time_n ≥ (ℓ_n+K+1)q(p)(τU_K+τ₀)/100 and mem_n ≥ P_e + ls0_archive bytes; Opus round-3 finding 1) and the
current-head preflight facts were added after round 3 and are **outside what round 3 checked**; HQ is spot-checking them.

## HQ audit A4 (post-council spot-check, OK-WITH-FIXES) — both MINOR fixes applied (writer, 2026-11-09)
1. `sections/s6_delivery.tex` Proposition F, "Addition for the C-ENG head code": U_K replaced by A4's text (deterministic
   polynomial upper bound on all operations between timing start and elapsed-time read in `cpp_time_scores(ctx,K,200)`,
   incl. model construction, sorting and scoring; MACH bounds the measured elapsed time by τU_K+τ₀); archive bytes defined
   explicitly, A = (2s+4)(12K+256) + 96s + 4(8W+4K+96) + 4096 with s = ℓ_n+K+1, W = ⌈p/64⌉; inserted the two-line
   inequality ŝ_K ≤ (τU_K+τ₀)/200 ⇒ 2sqŝ_K ≤ sq(τU_K+τ₀)/100 = P̄_LS0 ≤ time_n ≤ 3600·allocation$hours, with "strict >
   rejection tests, equality passes"; cites A4:7-25.
2. Scope sentence appended to the Proposition F status box, the Proposition F-GROW status box and the front-matter status
   summary (consistency.tex agentnote): "The full round-3 check applies to the d315c1e statements. The current-head
   preflight allocation addition was made after that council and is checked separately in HQ audit A4 (OK-WITH-FIXES,
   fixes applied)." (cites A4:1).
