# PRE-LEAN PASS, T4: PACKET for the "break it" read (Astra; the same packet goes to the blind Sol adversarial read)

Target (consistency tier): **Theorem 1 (true model; rows 1.1/1.2 of the card), Theorem 1′ (the variant with an identifiability margin), and the presented Theorem 2 (= Thm2SG, sub-Gaussian random rows).** Level-2 (probabilistic) results: the Lean value is the shape of the key-lemma chain, so look hardest at hypotheses, events, constants and quantifiers.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). All paths repo-relative. **Packet-only rule: read only what is listed; the locked proofs [P1], [P3] are read only at the cited labels.**

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-POST:Thm-1` (Theorem 1, items 1-6) | 344 | 1.0.1 | PROVED-CHECKED; council C3, MANIFEST 420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS |
| `SOP:TH09` (root T03♯) | 11 | 1.0.2 | PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C VERIFIED). Not upgraded (their statuses stay as at theory_main.tsv:68): T02(i♯) and T02(ii♯) PROVED, SF/XF VERIFIED; T01–T03 PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY |
| `W3-POST2:C` (Prop ER, expectation rate; card row 1.1 expectation form) | 362 | 1.0.7 | PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a, A=10.0 PASS, B=9.1 PASS |
| `W3-POST2:A1` (sufficiency, (OS) in place of (F_w)) | 359 | 1.0.7 | PROVED-CHECKED, conditional on W2-APP:POST; same council cell |
| `W3-POST2:E` (**Theorem 1′ = Theorem 1-VIS**) | 365 | 1.0.7 | PROVED-CHECKED, conditional on W2-APP:POST; same council cell |
| `W3-POST2:E3.1` (bridge (F_λ) ∧ BM ⇒ (ID) ⇒ (ID^M)) | 364 | 1.0.7 | PROVED-CHECKED; same council cell |
| `W3-D3:Thm2SG` (**presented Theorem 2**) | 549 | 1.0.0 | PROVED-CHECKED; council R2, MANIFEST 1c14a298ee1cea87f3ffcfbdd37b34985b9adc31c4d040a1c6a7b088fe2b406d, sol=8.5 PASS, opus=9.3 PASS |
| `W3-D3:B3w` (its master lemma), `W3-D3:ExSG` | 547, 548 | 1.0.0 | same status string |
Manifests verified OK locally: `W3-POST/reviews/MANIFEST_C3r.txt` (420c1cb0…), `W3-T03ACC/reviews/MANIFEST_R1.txt` (9714aea4…), `W3-POST2/reviews/MANIFEST_C2.txt` (96fd83cf…), `W3-D3/reviews/MANIFEST_R2g4.txt` (dff18ca9…). `ingest.py convert`: W3-D3/REPORT.md exit 0; W3-POST/REPORT.md has no REGISTRY block (registered earlier): not applicable.

## Spans (read these; long files in chunks of 120 lines)
Theorem 1 (W3-POST, `Theory_work/Wave3/W3-POST/`):
1. `STATEMENT.md:1-127`: §0 the target π and notation (:1-60), §2 Theorem 1 with regime R1, (E), (F_λ), (F_w), (BM) and items 1-6 (:61-100), Lemma 1a / 1a′ (:101-127). Premises of the claim: :16-39, :63-76.
2. `lemmas/L1a_size_tail.md:1-66` (Lemma 1a′, design-free size tail).
3. The proof chain of T03♯, T02(i♯), T02(ii♯) = [T03R]: `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md:1-215` (§1 exact size tail :13-73; §2 T02(i♯) :74-102; §4 hypotheses :127-146; §5 T02(ii♯) :147-159; §6 T03♯ :160-210). It is a proof by diff against [P1] and [P3]: read the locked originals ONLY at the labels it cites when a step depends on them: [P1] `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex:1-476` (`lem:spec`, `lem:prior`, `lem:chi`, `lem:num`, `lem:den`, `thm:Ta`, `thm:T02i`, `lem:good`, `lem:onG`, `thm:T02ii`); [P3] `.../T03_A2_selection_consistency/PROOF_v2.tex:1-396` (`lem:red`, `lem:smoother`, `lem:det`, `lem:signal`, `lem:Gprob`, `lem:ongood`, `lem:onesup`, `prop:sup`, `lem:signalgain`).
4. The restated record clauses: `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:1-80` (clauses T03S.1-T03S.5 and the clause map).
Expectation form and the variant (W3-POST2, `Theory_work/Wave3/W3-POST2/`):
5. `STATEMENT.md:1-142`: premises :11-48; A1 :54-56; B :68-77; C :83-94; E (Theorem 1′) :126-133.
6. `lemmas/C_expectation.md:1-66` (Prop ER); `lemmas/A_occam.md:36-88` (A1: (G3′), (C4′), (C5′), (C8′)); `lemmas/B_tail_approx.md:1-68` (Lemma 1a″); `lemmas/E_visibility.md:1-90` (E0, E1 floor-free comparison, E2 assembly, E3.1).
Presented Theorem 2 (W3-D3, `Theory_work/Wave3/W3-D3/`):
7. `STATEMENT.md:1-200` (Thm2SG :41-57, B3w :59-80, ExSG :82-90, premises :23-39, :154-157), `lemmas/ASSEMBLY.md:1-83`, `lemmas/B3w.md:1-134`. (B3w is the sub-Gaussian analogue of the transfer lemma; its template is `W3-DIST:B3`, `W3-DIST/STATEMENT.md:409-414`; read that only if a step needs it.)
Reader versions of the three rows (only for the statement fidelity question): `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:95-253` (thm1) and `:258-320` (thm2).

## What the claims say (paraphrase; the spans are authoritative)
Theorem 1, R1 (fixed s₀ ≥ 1, 2 ≤ p ≤ n^A, Gaussian noise), under (E) ‖μ‖² ≤ nM, (F_λ) anchored floor on S₀ ∪ J for |J| ≤ j₀, (F_w) anchored unnormalised floor on sets of size ≤ m♯_n, (BM): 1-δ_n = π-miss = O_P(√(log n/n)); P(HPM = MPM = S₀) → 1; every PIP within δ_n of 1{j ∈ S₀} for every data set; size and functionals; without (BM): no strict-superset mass 5(a) and strong-signal recovery 5(b); random design 6 (interface form). Expectation form (POST2:C): E[1 − π(S₀|y)] = O(√(log n/n)) uniformly over designs satisfying the stated floors. Theorem 1′ (POST2:E): (F_λ) away from S₀ and (BM) replaced by an identifiability margin (ID^M; c) with c > c₁(s₀, A). Theorem 2SG: rows i.i.d. with mean m_n and correlation matrix Σ_n, sub-Gaussian along 5(A+1)(s₀+1) log n-sparse directions with constant L, fixed signals b_lo ≤ |β*_j| ≤ b_hi, population sparse eigenvalue floor φ²: δ_n = O_P(√(log n/n)), P(HPM = MPM = S₀) → 1, max_j |PIP_j − 1{j ∈ S₀}| = O_P(√(log n/n)) under the joint law.

## The single question
**Is there any genuine flaw in Theorem 1 (statement and proof chain: T03♯, T02(i♯), T02(ii♯), Lemma 1a/1a′, the deterministic consequences SL0), in the expectation rate (POST2:C), in Theorem 1′ (POST2:E with A1's (G3′), (C4′), (C5′) and E1/E2), or in Theorem 2SG (with B3w, the transfer to sub-Gaussian rows, and the joint-law step)? Break it.**

Role: "break it". Look for: a wrong step; an unstated hypothesis; a constant that does not follow (the thresholds c₀(s₀, A) = max{4C_*, 32[s₀(A+1)+2]}, c₁(s₀, A), j₀ = ⌈(2A+1)s₀⌉ + 1, m♯_n; any "for n ≥ n₀" whose n₀ depends on something it must not); an event that is not the one the statement claims (the high-probability events 𝒢^sup_n, 𝒢^sel_n and their probabilities; quantifier order "for every sequence" versus "uniformly over designs"; the diagonal tightness transfer for random designs; the passage from conditional-on-design bounds to the joint law); a step where a hypothesis is used that is not in the statement, or stated but never used; a union bound that loses a factor not accounted for; the p ≥ 2 convention, s₀ ≥ 1, ties at ½, the edge K < s₀; a sub-Gaussian step that needs a lower moment or boundedness not assumed (mean m_n versus centred rows, the intercept, correlation-matrix normalisation, sparse directions of size 5(A+1)(s₀+1) log n versus the sizes the proof uses); statement text that says more than the proof delivers ((E) on the random design; "uniformly over such designs"). Do NOT redo the locked [P1]/[P3] proofs wholesale: they are SAME-FAMILY-ONLY locked inputs; check that each cited label says what the step needs.
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks. Report only (a) genuine flaws or unstated hypotheses we missed, or (b) changes needed to compile in Lean (Level 2: name the probabilistic input each step needs). **If you find nothing, say so explicitly and list in `CHECKED:` one line per step or edge case you actually verified: an evidence trail is required.**

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T4-1, ...), class (FLAW / UNSTATED-HYPOTHESIS / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic). Then a `CHECKED:` section, one line per item verified (also when points were found).
Finish with one line: `COUNT: <number of numbered points>`.
