# PRE-LEAN PASS, T10: PACKET for the "break it" read (Astra only; no blind Sol read for this target)

Target: **Theorem 8, row 3.7 (certified screening: `W3-SCR:A1@1.0.0`, status "PROVED-CHECKED") with its master chain `W3-SCR:SCR-A`, `W3-SCR:A-inf` (Theorem 8′ of the reader) and `W3-SCR:SCR-M`, and the code meaning of "certified" (`W3-SCR:CC`).** Level-2 (probabilistic). Fixed design, Gaussian errors.
Snapshot: branch `theory/PRE-LEAN` (HEAD 2062fe7f; all W3-SCR files as on origin/main). All paths repo-relative. **Packet-only rule: read only what is listed. Do not open any `reviews/` folder, any `PRE_LEAN_PASS` folder, or any other file under `Theory_work/Wave3/` beyond the spans below.**

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`; look each id up)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-SCR:A1` (Corollary A1, "the PROGRAM statement") | 401 | 1.0.0 | PROVED-CHECKED; council cell `R3; MANIFEST 19847f54f60d58a7d7f8214004b09a41242492c1c7237dc60de42f2a6fbce5dc; sol=10.0 PASS; opus=9.4 PASS` |
| `W3-SCR:SCR-A`, `:A-inf`, `:SCR-M`, `:L1`, `:L2`, `:B1`, `:B2`, `:B2d`, `:B3` | 390, 391, 394, 388, 389, 396, 397, 399, 400 | 1.0.0 | PROVED-CHECKED |
| `W3-SCR:CC` (code facts CC1-CC6) | 387 | 1.0.0 | CHECKED; same council cell (R3, MANIFEST 19847f54…) |
`manifest.py verify Theory_work/Wave3/W3-SCR Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R3.txt` prints `verify: OK MANIFEST 19847f54f60d58a7d7f8214004b09a41242492c1c7237dc60de42f2a6fbce5dc` (run by the coordinator; do not run it yourself).

## Spans (read these; long files in chunks of 120 lines)
1. **Row 3.7 / Theorem 8 as the reader states it:** `Theory_work/Wave3/W3-READER/READER_VERSIONS.md:932-1047` (Theorem 8, abstract placement, Theorem 8′, "Why each assumption", "Honest limits"; the "Certification frequency" paragraph is numerics, not a theorem: out of scope), and `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:78` (row 3.7).
2. **The master** (`Theory_work/Wave3/W3-SCR/`): `STATEMENT.md:1-163` (§0 Model G :12-47; §1 quantities :49-75; SCR-A :79-85; A-inf :87-90; SCR-A° and A°-inf :92-101, context only; **SCR-M :103-130**; SCR-G :132-145, context only; B1-B3 :147-155; **A1 :158-163**), and :214-238 (§3 "what is and is not claimed").
3. **Proofs:** `lemmas/L1_score.md:1-82` (score algebra, deterministic), `lemmas/L2_noise.md:1-57` (probabilistic events E1-E4), `lemmas/L3_screening.md:1-86` (SCR-A, (A∞), and the explicit-constant Corollary A1 at :65-77), `lemmas/L4_bridges.md:1-68` (B1-B3: floors ⇒ visibility), `lemmas/L7_master.md:1-117` (SCR-M and its corollaries).
4. **Code meaning of "certified":** `Theory_work/Wave3/W3-SCR/CODE_CHECK.md:1-83` (CC1-CC6; recorded readings at the core pin; treat as hypotheses about the code, and say if the theorem's event {𝒪 ∩ certified ∩ |Ŝ| ≤ q_n} is not what the coded flag gives).

## What the claims say (paraphrase; the spans are authoritative)
Theorem 8 (row 3.7 = Corollary A1): fixed design, Gaussian errors σ² > 0, S₀ ≠ ∅; (A1) sparse eigenvalue floor κ on every S with |S| ≤ q_n + s₀; (A2) θ*_min ≥ b₀ > 0 and ‖θ*‖₁ ≤ M, with κ, b₀, M, σ² fixed in n; (A3) (q_n + 1) log p + log n ≤ c₁ n with c₁ := κ²b₀²/(200(M² + σ²)) and q_n ∈ {0, …, K − 1}, K = min(p, ⌊n/2⌋). Conclusion: P(output, Ŝ certified, |Ŝ| ≤ q_n, S₀ ⊄ Ŝ) → 0 (an intersection; no claim that a run certifies with probability → 1). "Certified" = the run's local-optimality flag is set for the reported model (no strictly better single deletion, addition or swap among the scanned neighbours). No start, leakage, block or visibility condition; p ≤ n^A is not needed. Theorem 8′ (master (A∞)): signals may vary with n; the liminf condition on Γ_n(q_n) against τ_n√(2 log p + log n) + σ√(2 q_n log p); Theorem 8 is its corollary under fixed constants.

## The single question
**Is there any genuine flaw in Theorem 8 / row 3.7: in the chain SCR-M → SCR-A → (A∞) → Corollary A1 (including the constant c₁ = κ²b₀²/(200(M²+σ²)), the passage from the full sparse floor to the directional floor and to the visibility Γ_n(q_n) through B1-B3, the union bound over models of size ≤ q_n, the Gaussian event bounds of L2 with the method's data-dependent response scaling τ̂), or in the link between the theorem's event and the coded output (the event 𝒪, the certified flag CC1-CC6, the reported model Ŝ, the cap q_n ≤ K − 1, EX-A real arithmetic)? Break it.**

Role: "break it". Look for: a wrong step; an unstated hypothesis; a constant or threshold that does not follow (recompute c₁ and the sufficient condition (A3) from the lemmas; check the strictness "> 1" and the factors 2, 3, 4 in the probabilities and the exponent x = ((q_n+1) log p + log n)-type choices); the handling of the random scaling τ̂ and of the centring (y_c = Cy^r) in the noise events; whether "every LO (locally optimal) model of size ≤ q contains S₀" implies the intersection statement for the reported model Ŝ (is Ŝ one of the scanned centres? which neighbourhood is scanned, and does the master's deterministic family 𝓗 cover exactly the neighbours the code scans?); the case q_n = 0 and the empty model; K − 1 versus K; s₀ possibly growing (not allowed in Theorem 8: check the statement does not need it); whether the standardisation (columns ‖x_j‖² = n − 1, prior constant 1/(n+1)) matches the form used; p ≥ 2 versus p = 1; whether the conclusion "→ 0" needs q_n log p = o(n) beyond (A3) (it follows from (A3) only if c₁ is a constant: check).
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks. Report only (a) genuine flaws or unstated hypotheses we missed, or (b) changes needed to compile in Lean (Level 2: name the probabilistic input each step needs). **If you find nothing, say so explicitly and list in `CHECKED:` one line per step or edge case you actually verified: an evidence trail is required.**

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T10-1, ...), class (FLAW / UNSTATED-HYPOTHESIS / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic). Then a `CHECKED:` section, one line per item verified (also when points were found).
Finish with one line: `COUNT: <number of numbered points>`.
