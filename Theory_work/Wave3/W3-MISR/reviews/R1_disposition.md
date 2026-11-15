# Council R1 disposition (lead) — W3-MISR

Manifest `MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d` (`reviews/MANIFEST_R1.txt`; 36 files, 21 external inputs).
Seats, both blind: `sol` = gpt-6.1-sol (codex, high): **9.3, six gates PASS**, 0 FATAL / 0 MAJOR / 0 MINOR / 1 NIT
(`R1_council_sol.md`); `opus` = Claude Opus 5.5 (Claude Work, high): **8.7, six gates PASS**, 0 / 0 / 5 MINOR / 8 NIT
(`R1_council_opus.md`; relaunched once — the first launch died on the provider rate limit with no output).
`manifest.py bind`: OK. Council cell:
`R1; MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d; sol=9.3 PASS(reviews/R1_council_sol.md); opus=8.7 PASS(reviews/R1_council_opus.md)`
**Round R1 PASSED.** `manifest.py verify` passes on the tree at the end of this run.

**Nothing in the manifest was edited after the round.** The findings below are wording and bookkeeping; none changes
a hypothesis, a conclusion or a proof step. They are left for the CP3 step of HQ (apply, then an independent Sol diff
check attesting "editorial only", PROTOCOL rule 15), so that the frozen content and the verdicts stay bound.

| # | seat | grade | finding | proposed fix (not applied) |
|---|---|---|---|---|
| S1 | sol | NIT | `numerics/N5_energy_obstruction.py:5-6` docstring says c = 200 > c₁; c₁(2, 1) ≈ 258.9. The obstruction stands (c = 200 > c₀(2, 1) = 192; the ridge loss of every underfit diverges in the a = 1 arm). | Replace the two docstring lines with the reviewer's text. Outputs unchanged. |
| F1 | opus | MINOR | STATEMENT §8 summarises the C-MIS input statuses ("council R07/R08 PASS") although the header says statuses are verbatim. | Quote the registry status of each C-MIS row verbatim. |
| F2 | opus | MINOR | §8 omits inputs used at remark/lemma level: C-MIS Cor F(a), F(b), Lemma T, Cor H; the locked T03 proofs ([T03R], [P3]); the "conditional on" sentence omits W3-POST2:B, A0. | Complete the list (REPORT §5 already names Cor F(a), F(b)); add B and A0 to the sentence. |
| F3 | opus | MINOR | §9 "Not claimed" states the (E^σ) obstruction (π(S₀) → 0) as a fact; it rests on numerics N5 and a review's sketch. | Label it "numerical (N5) with an analytic sketch, unchecked"; the Sol seat re-derived the sketch (its review, last section). |
| F4 | opus | MINOR | The total-variation term of R′(c) does not vanish for ordinary non-Gaussian iid errors; the clause helps only for exact cases such as a random common scale. | Add one sentence to §1(c) / §2 saying so. |
| F5 | opus | MINOR | §3(a) is announced as needing only the first (OS) inequality but is stated over the full class 𝒦⁰_n. | Define the class with the first inequality only and state (a) over it (the proof M.2(a) already covers it). |
| F6–F13 | opus | NIT | wording of `v3_standardise`; κ_n defined on a probability-one event; GR with σ² > 0 in v1; "inclusion without a margin" phrasing; scope of Remark U; N0 data sets with HPM = ∅; index j reused in M.2(b); the beta-min of G(b) stronger than needed. | Editorial, as listed in the review. F13 is a possible small strengthening of an example (a constant-level relative beta-min suffices) — optional. |

For HQ: (1) the W3-POST2 inputs are declared hypotheses (statuses "conditional on …"); the checked label needs their
acceptance record first. (2) Layers: statement lock (2 rounds), better-theorem review, two line checks, council —
the mid-point and sweep layers were not run (not in the brief of this ticket); confirm or order them. (3) Supersession
of C-MIS:Thm-MIS(i)/(ii) and the three recommended tickets (BT1-A2, B1, B2) are decisions for HQ.
