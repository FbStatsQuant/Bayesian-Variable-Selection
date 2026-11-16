# W3-DIST — ERRATA (PROTOCOL_v4 §5.3: editorial findings; recorded, never blocking; applied later in one editorial batch)

None of these changes a statement, a hypothesis, a constant or a proof step. They are to be applied in one batch (in
the chapter transcription, or as one version bump with one "editorial only" diff check), not during a council round.

| # | source | place | erratum | correction |
|---|---|---|---|---|
| E1 | sweep SW1-06 | the proof files under `work/` (11 files, 63 pins) | bare line pins `STATEMENT.md:a-b` are pins to STATEMENT v1.3.1 | replace them by section and claim identifiers; until then `PINS.md` maps each pin to its object |
| E2 | council R1, astra, R1-astra-02 | `work/F_numerics/RESULTS.md:32` | "The size clause does fail in this regime": a table at fixed p = 12, n ≤ 1600 cannot show the failure of an asymptotic clause | say that the tables show persistent excess-size mass at the displayed cutoff, consistent with a geometric tail when (ND) fails; refer to Proposition NEC, with its fixed-design in-sample scope, for the proved obstruction |
| E3 | council R1, opus, E-01 | `STATEMENT.md` §4 (the W3-SAMP row), `REPORT.md` §5 | W3-SAMP:D, LT♯, C, TR are quoted at versions 2.1.1 / 2.0.1 / 1.1.1 / 2.1.1 as "PROVED-CHECKED"; the registry now lists 2.1.3 / 2.0.3 / 1.1.3 / 2.1.3 as "PROVED-CHECKED, conditional on SOP:TH09" (HQ relabel of 2026-11-16) | refresh the versions and quote the conditional form. The status of DIST-C is unchanged: it already carries "conditional on SOP:TH09" |
| E4 | council R1, opus, E-02 | `STATEMENT.md` §1R, Corollary C, "If a completed run scored the true model" | "scored" does not name the set | "scored in the final run or carried into it (the models offered to the final run, as in the description of the list)". The broader reading (scored anywhere, calibration included) rests on Remark 6.2 of `work/D_output/P6_DISTC.md`, which the seat confirmed in the code; proving it as a code lemma is a better-theorem proposal, not an erratum |
| E5 | council R1, opus, E-03 | `STATEMENT.md` §3, end of Lemma H's proof sketch | "(not line-checked.)" is stale: Lemma H is line-checked (`reviews/L3_sol_B.md`) | delete the annotation |
| E6 | council R1, opus, E-04 | `STATEMENT.md` §3, Lemma V (c) | "eᵀD′e ≤ σ*²χ²_{d_J} + ‖P_{S₀}e‖²" | use the proved wording of `work/C_size/V.md`: eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖² pathwise, the first term being σ*² times a χ²_{d_J} variable |
| E7 | council R1, opus, E-05 | `lemmas/NEC.md` §3, the row of the event 𝓔₂ | the probability of Σ_{j≤p′} z_j² > 2p′ is written as 2/p′ | it is at most 2(p′ + 1)/(p′ − 1)² by Chebyshev's inequality; both tend to 0 and nothing downstream changes |
| E8 | council R1, opus, E-06 | `STATEMENT.md` §3, bridge B2 | the chain drops the factor n/(n − 1) between Σ̂^z (normalised by n) and the sample correlation | write the chain as in `work/E_bridges/B2.md` (a); the displayed lower bound is true as it stands, since the omitted factor exceeds 1 |

Better-theorem proposals recorded for HQ (not errata; `TARGET.md` §4 and `reviews/R1_disposition.md`): the seven items of
the sweep; from council R1 (opus): an explicit dependence of the radius constant on A (C = O(A + 1) after tightening
the variance constant), and Corollary C with the broader retention premise proved as a code lemma.
