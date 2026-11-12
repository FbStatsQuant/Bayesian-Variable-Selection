# Council R1 + sweep SW1 — one-batch disposition (lead), STATEMENT v1.2 → v1.3

Inputs: `R1_council_sol.md` (9.3, PASS, 1 NIT), `R1_council_opus.md` (8.7, PASS, 5 MINOR + 8 NIT), `SW1_sweep_astra.md`
(0 FATAL / 0 MAJOR / 8 MINOR / 1 NIT, verdict SUBSTANTIVE for its item 1), all on
`MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d`. HQ's CP2 decision: apply everything in
one batch; if the sweep finds anything substantive, a short council re-round (both seats) on the new manifest replaces
the Sol diff check. The sweep classed one fix as substantive, so council R2 is run on the new manifest. This file
supersedes the "proposed fixes" table of `R1_disposition.md`.

No hypothesis was strengthened and no conclusion changed. One statement clause changed form: §3(a) is now stated
over the larger class 𝒦⁰′_n (first (OS) inequality only), which is what its proof already used.

| # | source | grade | item | what was done | where |
|---|---|---|---|---|---|
| S1 = SW1-1 | sol; sweep | NIT; MINOR (substantive per the sweep) | N5 docstring: "c = 200 > c₁" is false for s = 2 (c₁(2, 1) ≈ 258.9); the premise claim covered the control arms | Docstring rewritten: c = 200 > c₀(2, 1) = 192; in the arm a = 1 every underfit has ridge loss ≥ n(n − 1), so the margin holds eventually for any fixed constant; a = 0, ½ are controls. Same wording in ASSUMPTION_MAP and STATEMENT §9. Outputs unchanged (docstring only). | `numerics/N5_energy_obstruction.py`; `ASSUMPTION_MAP.md` row A:MISR-ESNR; `STATEMENT.md` §9 |
| F1 | opus | MINOR | C-MIS statuses in §8 not verbatim | each registry status quoted verbatim, one line per id | `STATEMENT.md` §8 |
| F2 | opus | MINOR | §8 incomplete | added C-MIS:Cor-F(a), Cor-F(b), Lemma-T, Cor-H; the locked [T03R]/[P3] inputs (SOP:TH128, SOP:TH09); all six W3-POST2 ids in the conditional sentence; `B_tail_approx.md` in the aliases; registry edges added | `STATEMENT.md` header, §8; `REPORT.md` §7 |
| F3 | opus | MINOR | (E^σ) obstruction stated as fact | labelled "numerical, with an analytic sketch; not a checked proof" | `STATEMENT.md` §9; `REPORT.md` §3 |
| F4 | opus | MINOR | TV term of R′(c) is not a robustness bound | one sentence in §1(c), a parenthesis in §2 | `STATEMENT.md` |
| F5 | opus | MINOR | §3(a) not formally stated over the trimmed class | class 𝒦⁰′_n defined; (a) stated over it, threshold and constant free of c; proof M.2(a) opens with that class and its own threshold n₁ᵃ | `STATEMENT.md` §0, §3(a); `lemmas/M_misr.md` M.2(a) |
| F6 | opus | NIT | `v3_standardise` description; anchored-branch metadata | described; metadata named, reaches no score | `STATEMENT.md` §1(a″); `lemmas/R_reduction.md` R.3 |
| F7 | opus | NIT | κ_n defined a.s. only | fixed reference configuration off the null event | `lemmas/G_corollaries.md` G.1 |
| F8 | opus | NIT | v1's GR has fixed σ² > 0, τ² | reworded | `STATEMENT.md` §0 |
| F9 | opus | NIT | "inclusion without a margin" | reworded (coordinate margin, no global margin) | `ASSUMPTION_MAP.md` |
| F10 | opus | NIT | scope of Remark U | clause added | `STATEMENT.md` §7 |
| F11 | opus | NIT | N0: two data sets have HPM = ∅ | stated | `STATEMENT.md` §1(a″) |
| F12 | opus | NIT | index j reused | summation index renamed i | `lemmas/M_misr.md` M.2(b) |
| F13 | opus | NIT | G(b)'s beta-min could be a fixed constant level | **not applied** (it would change a statement; recorded as a possible strengthening of an example) | — |
| SW1-2 | sweep | MINOR | "scalar covariance necessary" overstated | reworded: E2 excludes non-scalar laws for the same mean-only target; not necessary under (PR) | `ASSUMPTION_MAP.md`; `REPORT.md` §4 |
| SW1-3 | sweep | MINOR | N1 variances mislisted | actual five regimes listed (2, 1 + n, 1 + n², 2/n, n⁻²) | `ASSUMPTION_MAP.md`; `REPORT.md` §3; script docstring |
| SW1-4 | sweep | MINOR | N1/N3 headers call raw coefficients standardised | script print strings corrected; script re-run (deterministic seeds): data lines identical, only header lines differ | `numerics/misr_numerics.py`, `misr_numerics_out.txt` |
| SW1-5 | sweep | MINOR | finite simulations described as limits | finite-sample wording throughout | `ASSUMPTION_MAP.md`; `REPORT.md` §3 |
| SW1-6 | sweep | MINOR | HPM range 0.93–0.95 omits 0.92 | 0.92–0.95 | `ASSUMPTION_MAP.md` |
| SW1-7 | sweep | MINOR | registry pointers of two assumptions | recomputed from the v1.3 line numbers (all statement/premise spans too) | `REPORT.md` §7 |
| SW1-8 | sweep | MINOR | Corollary H rates: squared vs unsquared distance | stated explicitly | `REPORT.md` §1, §7; `ASSUMPTION_MAP.md` |
| SW1-9 | sweep | NIT | t used for two things in G.4 | scale written a_n | `lemmas/G_corollaries.md` G.4 |
