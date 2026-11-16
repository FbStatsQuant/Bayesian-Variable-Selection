# W3-DIST — disposition of blind read S1 (`reviews/S1_astra.md`; gpt-6-astra, codex, high; manifest fb6d0dab…b62e)

Reviewer verdict: **GO-WITH-REPAIRS**. Per statement: DIST-1, DIST-2, DIST-3, DIST-C, X, X′, P6 REPAIRABLE; H and S
SOUND-AS-STATED (statement review, not a line check); **T FALSE-AS-STATED** on part of its stated range (repairable).
0 CRITICAL, 5 MAJOR, 5 MINOR, 1 NIT. No counterexample to DIST-1's display (1.1) on its stated interfaces.
All findings accepted; none disputed. Edits: STATEMENT v1.1, ROUTES v1.1, ASSUMPTION_MAP v1.1 (changelog at the foot
of STATEMENT.md). The S1 brief asked for a strictly better statement, so S1 is also the better-theorem review.

| id | sev. | finding (one line) | disposition | where |
|---|---|---|---|---|
| S1-01 | MAJOR | Lemma T false when d is beyond the growth bound's range (negative remainder at n = 100, p = d = 10⁴) | **ADOPT**: 1 ≤ d ≤ min(p_raw, n − 1); remainder with log(2en/(d+1)) ≥ 0; applications capped. Attribution/constant of the relative-deviation inequality to be verified or proved (proof-leg item, WS-B) | STATEMENT §3 Lemma T; ROUTES §2 Step 2 |
| S1-02 | MAJOR | p_raw vs retained p conflated; p_ret ∈ {0, 1} possible; cutoff not "data-free"; s₀ = 0 | **ADOPT**: p_raw and p = p_ret(X) separated; 𝒟_n = {p_ret ≥ 2} in every remainder; cutoff X-measurable; s₀ ∈ {0, …, s₀^r} covered | STATEMENT §0, (1.1), (1.2), Lemma X |
| S1-03 | MAJOR | "no exponential inner threshold possible" after DIST-3 is false as a blanket claim (p = s₀ = 2 counterexample) | **ADOPT**: parenthesis deleted; replaced by "δ_n → 0 gives no exponential control of δ_n" | STATEMENT DIST-3 note (iii) |
| S1-04 | MAJOR | [SL] comparison: Cor 1 has fixed α > 0 (cannot set α = 0); Thm 2 at polynomial p allows any r̄_n log n = o(nε_n²); (14) not literally satisfied; (ND) is an extra geometric interface; H1's "≺" prior-mass claim is a constant-factor statement | **ADOPT**: comparison rewritten (TARGET.md §2, CHECKPOINT §3); "short of [SL] by a logarithm" removed; (14) described through envelopes; (ND) labelled as absent from [SL]; H1's claim downgraded in the record (H1 report is helper material, not edited) | STATEMENT §0 (ND), DIST-2; ROUTES §1; TARGET.md |
| S1-05 | MAJOR | Bridge B1's exponential clause false (Bernoulli(q_n) cancelling pair; (C) fails w.p. ≍ 1/(n log n)) | **ADOPT**: B1 now requires uniformly sub-Gaussian coefficient-weighted true coordinates | STATEMENT §3 B1 |
| S1-06 | MINOR | X4 route omits the R₀ factor, union multiplicity, full variance surcharge; needs one n₀ for all t; X must conclude the size bound | **ADOPT** | STATEMENT Lemma X; ROUTES §2 X4 |
| S1-07 | MINOR | κ₀ unquantified in DIST-2; s₀ vs s₀^r; "1 + s₀"; log(p ∨ n) | **ADOPT** | STATEMENT §0, DIST-1(c), DIST-2, X′ |
| S1-08 | MINOR | DIST-C: joint law; DIST-3's other hypotheses must be imported; discovery from D-i + P-OVL | **ADOPT** | STATEMENT §2 |
| S1-09 | MINOR | flat-intercept remark: IG shape differs in a genuine flat-prior model | **ADOPT**: "post-processing extension" | STATEMENT Remark R1 |
| S1-10 | MINOR | numerics: N5 is still strictly sparse; pooled tails ≠ nested statement; N4 misses τ² ≍ log n/n² | **ADOPT**: relabelled; limits stated; two additions queued for the proof leg | ASSUMPTION_MAP §3 |
| S1-11 | NIT | manifest hashes are LF-normalised; P6 needs a > 0; "success event" wording | **ADOPT** (P6, wording). Manifest: `manifest.py` LF-normalises by design (INFRA R06, documented in the tool); no action | STATEMENT P6, DIST-1(e) |

## Better-theorem proposals
| id | proposal | disposition | evidence |
|---|---|---|---|
| BT1 | DIST-3 with (C) or L_{S₀} ≤ B in place of (F₀) | **ADOPT** ((L₀; B)) | reviewer's argument via [D] D1 (no floor used); lead re-derived the three bounds (ROUTES §3). No coefficient-recovery claim |
| BT2 | oracle exponential bound Π(d_H > C√(u/n)) ≤ δ_n + Ce^{−cu} | **ADOPT** as the form of DIST-3 | single support ⇒ no union, no logarithm; needs (TR₀) |
| BT3 | reference-adaptive size lemma without p ≤ n^A | **ADOPT** as the form of Lemma S | reviewer re-derived the slack of the 3t cutoff from `B_tail_approx.md`; supports S-APX and S-EXP |
| BT4 | one output-transfer theorem for any Q ≤ L_nπ | **ADOPT** as (C-0), with the λ-budget in (C-i) | deterministic one-line argument |
No proposal rejected; none deferred. Each adoption is a STRONGER or EQUAL row in the changelog; the statement-change
check of the tags (PROTOCOL_v4 §4.2) is pending and is requested from HQ at CP1 (one Sol read of the v1.0.2 → v1.1 diff).

## Not checked by S1 (its own statement)
The Anthony–Shawe-Taylor source; the numerics scripts and arrays; scoring/engine/preprocessing code beyond the three
pinned files; the RM2/START proof files and the registry. These stay cited conditional inputs.
