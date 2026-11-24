# PRE-LEAN PASS, T5: PACKET for the "break it" read (Astra; the same packet goes to the blind Sol adversarial read)

Target (consistency tier): **Theorem 9 (the posterior recovers the true conditional law of y given x, in Hellinger distance averaged over x; card row 2.1) = `W3-DIST:Thm-A` (display (i)), `W3-DIST:Thm-B` (parametric rate), with Corollary 9C (`W3-DIST:Cor-C`) and the exact-posterior theorems DIST-1, DIST-2, DIST-3, the key lemmas and the bridges they consume.** Level-2 (probabilistic): look hardest at hypotheses, events, constants and quantifiers.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). All paths repo-relative, under `Theory_work/Wave3/W3-DIST/` unless stated. **Packet-only rule: read only what is listed.**
(Already read by the T3 call and not the focus here: Lemma H, Lemma P6, Lemma D0; the Cor-C deduction is in scope only for the probabilistic step "Theorem A ⇒ every completed run with π(T) ≥ n^{−cM/2}".)

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`; look each id up)
All carry version 1.0.2 and the status string `PROVED-CHECKED; council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS`, except where noted:
| id | line | file span | note |
|---|---|---|---|
| `W3-DIST:Thm-A` | 488 | `STATEMENT.md:185-207` (premises :136-183) | depends on DIST-1, DIST-2, B0, B1, B2 |
| `W3-DIST:Thm-B` | 489 | `STATEMENT.md:209-215` | depends on DIST-3, B0, B1, B2, B2core, B3 |
| `W3-DIST:DIST-1` | 484 | `:74-91` (premises :17-70) | depends on H, T, X |
| `W3-DIST:DIST-2` | 485 | `:93-98` | depends on H, T, X′ |
| `W3-DIST:DIST-3` | 486 | `:100-112` | depends on H |
| `W3-DIST:Cor-C` | 490 | `:217-238` | status adds "conditional on EX-A (exact arithmetic)" |
| `W3-DIST:T`, `:S`, `:V`, `:X`, `:X'`, `:NEC` | 492, 493, 494, 495, 496, 497 | `:328-340`, `:342-348`, `:350-353`, `:355-366`, `:368-370`, `:372-379` | key lemmas |
| `W3-DIST:B0`, `:B1`, `:B2core`, `:B2`, `:B3` | 499-503 | `:385-390`, `:391-395`, `:396-399`, `:400-408`, `:409-414` | bridges; B0 depends on `W3-MISR:R'`; **B3's status reads "PROVED-CHECKED, conditional on W3-POST:Thm-1 (for its last sentence); council R2, …"** |
Registry council cell: `R2; MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a; astra=9.3 PASS(reviews/R2r_record_astra.md); opus=9.2 PASS(reviews/R2r_record_opus.md)`. `manifest.py verify` of `reviews/MANIFEST_R2r.txt`: only difference is `EXT:Scripts/SMC_BVS/core/v3_run.R` (v3.1 list-PIP commit after the pin; additive); every DIST text file unchanged. `ingest.py convert` of `REPORT.md`: exit 0 (20 blocks).

## Spans (read these; long files in chunks of 120 lines)
1. `STATEMENT.md:17-70` (setting, notation, (S1), (S2), bad sets), `:72-125` (DIST-1, DIST-2, DIST-3), `:126-238` (§1R reader versions: assumptions (A1)–(A5), Theorem A, Theorem B, Corollary C), `:320-414` (key lemmas T, S, V, X, X′, NEC; bridges B0-B3).
2. Proofs: `lemmas/DIST12.md:1-97` (DIST-1 §D.0–D.5, DIST-2 §D.6); `work/B_transfer/DIST3.md:1-181`; `work/B_transfer/T.md:1-203`; `lemmas/X.md:1-234` (§0–§8 Lemma X, §9 Lemma X′); `work/C_size/S.md:1-184`; `work/C_size/V.md:1-152`; `work/E_bridges/ASSEMBLY.md:1-230`; `work/E_bridges/B0.md:1-120`, `B1.md:1-86`, `B2core.md:1-99`, `B2.md:1-100`, `B3.md:1-104`; `work/D_output/COR_C.md:41-135`.
3. Reader version of the row (statement fidelity only): `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:1052-1282` (thm9) and `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:63`.

## What the claims say (paraphrase; the spans are authoritative)
Theorem A (display (i)): there are c, M₀ such that for every M ≥ M₀ and all large n, except on a set of data of P*-probability ≤ n^{−cM}, the posterior puts mass ≤ n^{−cM} on laws (S, θ, v) whose joint distance d_H(f, f*) (conditional density times the design law, averaged over x) exceeds √(M log n/n); no beta-min and no fixed lower eigenvalue bound; rows i.i.d., Gaussian linear model, at most n^A predictors, sub-Gaussian predictors on sparse directions of size q_n(M) = min{p_raw, ⌈C_q M log n⌉}, smallest correlation eigenvalue ≥ c_ψ/n there (no near-exact collinearity); body: levels M₀ ≤ M ≤ √n/log n with posterior size ≤ s + C₁M, and the version without the collinearity condition with the radius larger by √(log(p_raw ∨ n)). Theorem B: rate M_n/√n under a fixed eigenvalue floor and detectable signals. Cor 9C: with probability ≥ 1 − n^{−cM} over the data, every completed run whose list T has π(T) ≥ n^{−cM/2} satisfies Π̂(d_H > √(M log n/n)) ≤ n^{−cM/2}.

## The single question
**Is there any genuine flaw in Theorem 9 as stated in §1R (Theorem A, Theorem B, Corollary C) and in the exact-posterior chain that proves it (DIST-1, DIST-2, DIST-3, Lemmas T, S, V, X, X′, the bridges B0–B3 and ASSEMBLY)? Break it.**

Role: "break it". Look for: a wrong step; an unstated hypothesis; a constant or threshold that does not follow (c, C, C′, M₀, n₀, the exponent n^{−cM}, the radius √(M log n/n), q_n(M), C_q, the level range M ≤ √n/log n; any "n₀ depends on" claim); an event that is not the one the statement claims (the success event of DIST-1 and its probability; "except on data sets of probability ≤ n^{−cM}" versus "for every data set in the success event, uniformly in the run"); a union bound or net argument (Lemma T's growth function, Lemma X's entropy count, the layer-cake step) that loses a factor not accounted for; the passage from the in-sample Hellinger distance (Lemma H, D0) to the joint distance averaged over x through Lemma T (the d ≤ n−1 constraint, "d must not depend on the sample", the constants η_n²(d, δ)); the plug-in intercept; rows with discrete or heavy-tailed predictors (only sub-Gaussian along sparse directions is assumed: which step needs more?); p_raw versus the retained p, dropped (constant) columns, p_raw > n; the dependence on s (fixed) versus the stated generality; the use of `W3-MISR:R'` in B0 (centring/scale equivariance) and of `W3-POST:Thm-1` in B3 (only for its last sentence: is it used anywhere else?); the claim that no beta-min is needed (Lemma V, X, X′ with ridge cost). Do NOT redo the locked [P1]/[P3] proofs they cite: check that each cited label says what the step needs.
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks. Report only (a) genuine flaws or unstated hypotheses we missed, or (b) changes needed to compile in Lean (Level 2: name the probabilistic input each step needs). **If you find nothing, say so explicitly and list in `CHECKED:` one line per step or edge case you actually verified: an evidence trail is required.**

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T5-1, ...), class (FLAW / UNSTATED-HYPOTHESIS / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic). Then a `CHECKED:` section, one line per item verified (also when points were found).
Finish with one line: `COUNT: <number of numbered points>`.
