# PRE-LEAN PASS, T3: PACKET for the Astra "break it" call

Target: **domination transfer (the deterministic core of Cor 9C / Cor-C) = `W3-DIST:P6` (a), (b) and the clause (C-0) / (C-i) threshold form / (C-ii)(α) / (C-iii) of `W3-DIST:DIST-C`; the Hellinger reduction `W3-DIST:H`; and Lemma D0 inside `W3-POST2:D`.** Lean shortlist item 3.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). All paths repo-relative.
Lean core: P6(a),(b) (finite sums); P6(c) (mixture convexity of d_H², used by the predictive bounds); H (pointwise inequality then integration against nu_x); D0 (the same inequality, averaged over i, for the one-dimensional normal closed form H² = 1 − A·B). The probabilistic parts of DIST-C ((C-i) with P⊗ events, (C-ii)(β), P-STORE, delivery premises) and Cor-C's probability statement are context.

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-DIST:P6` | 498 | 1.0.2 | PROVED-CHECKED; council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS |
| `W3-DIST:H` | 491 | 1.0.2 | same status string as P6 |
| `W3-DIST:DIST-C` | 487 | 1.0.2 | PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c817…, astra=9.3 PASS, opus=9.2 PASS (full string as in the registry) |
| `W3-DIST:Cor-C` | 490 | 1.0.2 | PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c817…, astra=9.3 PASS, opus=9.2 PASS. `depends_on` includes `W3-DIST:DIST-C@stmt:(C-0), (C-i) threshold form, (C-ii)(α) — deterministic clauses only (W3-DIST/STATEMENT.md:291-303, :314)` |
| `W3-POST2:D` (Lemma D0 is its step D0) | 363 | 1.1.7 | PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a, A=10.0 PASS, B=9.1 PASS |
Manifests: `Theory_work/Wave3/W3-DIST/reviews/MANIFEST_R2r.txt` verify: 1 difference, `EXT:Scripts/SMC_BVS/core/v3_run.R` (v3.1 list-PIP commit after the pin; additive, DIST's code pins quote `v3_run.R:142, 154, 159-163`, which the commit message says do not move); every DIST text file unchanged. `Theory_work/Wave3/W3-POST2/reviews/MANIFEST_C2.txt`: verify OK. `ingest.py convert` on `W3-DIST/REPORT.md`: exit 0 (20 blocks). `W3-POST2/REPORT.md` does not convert (2 PROBLEM lines on already-registered blocks A1 and B, unrelated to D).

## Spans (read these, nothing else; long files in chunks of 120 lines)
W3-DIST (`Theory_work/Wave3/W3-DIST/`):
1. `STATEMENT.md:17-70` (notation, (TP) tower identity Π(B|D_n) = Σ_S π(S)Π(B|S,D_n), the bad sets (1.1), (1.2), assumptions).
2. `STATEMENT.md:217-238` (Corollary C), `:266-318` (code facts, store/HPM/MPM laws, Theorem DIST-C (C-0)…(C-iv), honest label), `:322-326` (Lemma H, with its short proof), `:381-382` (Lemma P6).
3. Proofs: `work/D_output/P6_DISTC.md:1-10` header, `:40-93` (§0 scope/hypotheses, §1 objects), `:140-162` (§3 Lemma P6 (a), (b), (c)), `:287-318` ((C-0), Proposition C-i°, (C-i)), `:320-390` ((C-ii), (C-iii), (C-iv), honest label); `work/D_output/COR_C.md:41-135` (exact meanings, statement proved, proofs); `work/B_transfer/H.md:1-117` (Lemma H, full proof; H.0 objects).
W3-POST2 (`Theory_work/Wave3/W3-POST2/`):
4. `lemmas/D_hellinger.md:1-18` (D0 and Lemma D0 with its proof); `STATEMENT.md:99-119` (claim D; the display of the deterministic bound).

## What the claims say (paraphrase; the spans are authoritative)
P6(a): if Q is a law on Omega and Q(S) <= L·pi(S) for all S then QPi(B) := Σ Q(S) Pi(B|S,D_n) <= L·Pi(B|D_n). P6(b): for a > 0, π({S : Pi(B|S,D_n) > a}) <= Pi(B|D_n)/a. Store BMA: L = 1/π(T); single model: L = 1/π(S-hat). Cor-C: with prob >= 1 − n^{−cM} every completed run with π(T) >= n^{−cM/2} satisfies Pi-hat(d_H > √(M log n/n)) <= n^{−cM/2} (the pathwise form is C-i°: for a in (0,1] on the success event of DIST-1, every completed run with π(T) >= a has Pi-hat^T(B_n) <= ϱ_n/a).
H: for every (S, θ, v), v > 0: d_H²(f_{S,θ,v}, f*) <= (v/σ*² − 1)² + E_x[min{1, Δ(x)²/(4σ*²)}]. D0: n⁻¹Σ H²(N(μ̂_i, v), N(μ_i, σ*²)) <= (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²).

## The single question
**Is there any genuine flaw in P6 (a), (b), (c), in Lemma H, in Lemma D0, in the deterministic clauses of DIST-C ((C-0), C-i°, (C-ii)(α), (C-iii)) and in Cor-C's deduction from them (domination transfer then Theorem A)? Break it.**

Role: Astra, "break it". Look for: a wrong step; an unstated hypothesis; an edge case in the stated domain (pi(S) = 0 for some S, L = 0 or L < 1, Q not absolutely continuous w.r.t. pi, empty Omega-subset T, pi(T) = 0, a = 0, B non-measurable or Pi(B|S) undefined, v → 0 or ∞, sigma*² vs v + sigma*² in the denominators, Delta unbounded, E_x over a law without second moments, dropped columns); a wrong constant or direction in 1 − A·B <= (1 − A) + (1 − B), 1 − A <= (r − 1)², 1 − B <= min{1, Δ²/(4σ*²)} (check that min{1, ·} is justified: 1 − B <= 1 always and the bound Δ²/(4(v+σ*²)) <= Δ²/(4σ*²)); a mismatch between H.md's objects (plug-in intercept, the dropped-column case, the in-sample identity n⁻¹ΣΔ_i² = ε̄² + ‖μ̂ − μ‖²/n) and the display of D0 (which is stated for the centred, intercept-free distance); a mismatch between the quantifiers of Cor-C ("every completed run", "with P*-probability >= 1 − n^{−cM} over the data") and what C-i° proves; a step that would not compile in Lean (measurability of (ξ, x, y) ↦ g_ξ(x, y) on the disjoint union of the pieces {S}×R^S×(0,∞), Tonelli and Jensen steps in P6(c), definition of Pi(·|S,D_n) as a kernel, a sum over an arbitrary countable or finite Omega, a division by π(T) or by a, hidden nonemptiness).
Lean scope: P6(a),(b),(c) for a finite Omega and kernels; H and D0 as real-analysis inequalities (the closed form H² = 1 − A·B for 1-D normals is used as a given identity: say if it needs a proof step the text omits).
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks. Report only (a) genuine flaws we missed or (b) changes needed to compile in Lean, each with the exact line and a minimal fix. If you find nothing, say so explicitly **and list in one line each the edge cases you actually checked** (an evidence trail is required: a bare "no flaw" is not acceptable).

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T3-1, ...), class (FLAW / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic). Then a section `CHECKED:` with one line per edge case or step you verified (also when points were found).
Finish with one line: `COUNT: <number of numbered points>`.
