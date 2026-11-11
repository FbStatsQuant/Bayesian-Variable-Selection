# API audit pass 1 — HQ triage (2026-11-11)

Batch msgbatch_0148MUMvKUm8r1au3Y6W7Xpk, Fable 5.2 effort high, blind. Usage: out 1.12 M, cache read 1.24 M, uncached in
0.04 M (+ cache writes) → ≈ $27 at batch rates.

| verdict | claims |
|---|---|
| OK | 86 |
| MINOR (local slips; claim unaffected) | 19 |
| GAP | 1 — C-DLV:Prop-F |
| no verdict (max_tokens 64k hit) | requests f17 (W2-FAC-B:Thm-FAC-CS), f26 (W2-FAC-X:Thm-FAC-CS-iid), f18 last claim (W2-FAC-PK:P5) → re-run pass1b at 128k |

## GAP — C-DLV:Prop-F (results/f07.md)
Second conclusion "P(Ŝ⁺ = S₀) → 1 unconditionally" is stated under Theorem D's premises only; the proof needs the
hypotheses of the consumed posterior-concentration and LS0-discovery results (W1-GEN (H0)–(H2), W1-PXN SIZE/(OP)), which
the proposition omits (STATEMENT C2 has "under their hypotheses"). Proposed repair: restate the conclusion under those
hypotheses. First conclusion P(𝒰_n) = 0 unaffected. HQ reading: statement-wording gap (missing hypothesis), not a false
result. → Sol confirmation (R-AUD1), then rule 11 (correction as a new version; dependents propagated).

## MINOR (no action now; batch for a later editorial pass with the chapter v2.0 work)
W1-N1:Thm-N1, C-DLV:Cor-R, C-DLV:L1-R, C-DLV:L3-3.3, C-DLV:Thm-D, C-GROW:Thm-GROW, C-GROW:L3, W2-APP:Thm-APP, W2-FAC-PK:Thm-FAC-PK, W2-FAC-PK:Thm-PATH, W2-FAC-S5:L4, W2-UNI:U-LOC, W2-UNI:UNI-1, W2-UNI:F-UNI, W3-RM:Examples, W3-RM:RM-R, W3-SAMP:Pkg, W3-SCR:L5.1, W3-SCR:SCR-M

## Disposition (HQ, after R-AUD1 Sol: CONFIRMED-WORDING)
C-DLV:Prop-F is **not** a mathematical gap: "on the classes above" imports Corollary D′'s statistical hypotheses, STATEMENT
C2 and the registry row carry them, and the chapter (`FINAL/sections/s6_delivery.tex:46`) and generated block state them
explicitly. No consumer relies on the over-strong reading (R-AUD1 consumer table). No LIFECYCLE §3 mark, no
propagation, no ticket notification. The standalone sentence at `C-DLV/lemmas/L4_delivery.md:83-84` gets Sol's minimal
restatement in the editorial pass with the 19 MINORs (chapter v2.0 work), as a wording-only version bump.

## pass1b (re-run of f17, f18, f26 at 128k; msgbatch_01CAKzGyfNsvvsGNnuf3x6ja, ≈ $5)
All three completed: W2-FAC-B:Thm-FAC-CS MINOR; W2-FAC-PK P1, Thm-NEG, Thm-PATH OK, Thm-FAC-PK, P5 MINOR;
W2-FAC-X:Thm-FAC-CS-iid MINOR. **Final pass-1 tally over all 109 PROVED-CHECKED claims: 87 OK, 21 MINOR, 1 wording
(C-DLV:Prop-F), 0 ERROR.** (pass1b supersedes pass1 for f17/f18/f26.)
