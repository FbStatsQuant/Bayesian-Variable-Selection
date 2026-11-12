# LC2 disposition (lead) — lemma checks LC2-A, LC2-B, LC2-C and statement-change check SC2

Manifest of the round: b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6 (each review quotes it;
`verify` OK after the round and before any edit). The texts the reviewers read are kept in `as_reviewed_by_LC2/`
(STATEMENT, ASSUMPTION_MAP, L4, L5, L6). LC2-A, LC2-B, LC2-C were blind first reads. Cross-family: L4, L5 written
by Claude (lead), checked by OpenAI seats; L6 written by an OpenAI prover (PV1), checked by Claude Opus 5.5.
**No FATAL and no MAJOR mathematical finding in any of the four reviews.**

## LC2-A — `LC2A_L4_check_astra.md` (Codex gpt-6-astra high; L4, bridge (P7))
Verdicts: **Lemma SAND-R^b / (P7) VERIFIED-WITH-AMENDMENTS; Lemma 2 (product form) VERIFIED; Lemma 3
VERIFIED-WITH-AMENDMENTS; Lemma 4 VERIFIED; §7 item 1 VERIFIED.** "Neither the product-form step nor the slower
localisation rate introduces a missing hypothesis. The principal proof works for every X-measurable partition and
simultaneously for every maximiser."
| # | class | finding | action |
|---|---|---|---|
| 1 | MINOR | Lemma 3: "G a standard Gaussian vector of 𝕍, independent of 𝒢" is literally wrong (𝕍 is 𝒢-measurable); only the conditional law is needed and the unprojected innovation is independent | replaced by the reviewer's text: z := e/τ ~ N_n(0, I_n) independent of 𝒢, g = τΠz, conditional laws of ‖G‖² and Gᵀv [LC2A-1]; the tail bound is unchanged |
| 2 | NIT | STATEMENT pointer "L4 §6" should be "§7 item 1" | fixed (same as SC2-3) |
Independent stress test by the reviewer (slow localisation r_n = 1/log log n, leak d = r_n h_n, n up to 10¹⁰, all
(l, U), random and extreme response coefficients): no violation; max |ẑ_U − ẑ_{U₀}|/(ϖ_n + r_nh_n + h_n²) = 0.955.
**(P7): attempt 1 of 2 — verified. Riders P3 and T6: both verified as parts of the lemma.**

## LC2-B — `LC2B_L5_check_sol.md` (Codex gpt-6.1-sol high; L5)
Verdicts: **(S2)/(S3), P8, P9, D-loc^b, P10, Theorem RM2-R (conditional on W2-APP:POST@1.0.1), containment of RM-R:
VERIFIED; P9a VERIFIED-WITH-AMENDMENTS.**
| # | class | finding | action |
|---|---|---|---|
| 1 | MINOR | §2 uses residual vectors with iid centred entries, but Setting R allows a raw mean | the mean-zero reduction is stated at the head of §2, in the reviewer's words [LC2B-1] |
| 2 | MINOR | P9a writes log\|𝔓⁺\| without discharging 𝔓⁺ = ∅ | empty case discharged first [LC2B-2] |

## LC2-C — `LC2C_L6_check_opus.md` (Claude Opus 5.5 high, Claude Work; L6)
Verdicts: **§0, E4, E5 VERIFIED; E1, E2, E3 and the table VERIFIED-WITH-AMENDMENTS.** Nothing in L6 fails; no status
is stronger than what is shown; the ledger explaining why 17/2 disappears is correct.
| # | class | finding | action |
|---|---|---|---|
| 1 | MINOR (sharpness) | E5's range b < 3/10 is correct but not best: a size-by-size comparison gives (W) for b < 3/8, and a matching sketch suggests (W) fails beyond | **not adopted as a claim** (both halves are sketches); recorded in L6 E5 [LC2C-1], STATEMENT (C5), SHARPNESS §4 and open item O4′ |
| 2 | MINOR (record) | L6 cites RM2 STATEMENT by stale line numbers and misquotes its line 4 | citations by section; line 4 quoted verbatim; stale sentence removed [LC2C-2] |
| 3 | MINOR (status) | E2, E3 status lines and table rows must name their Lemma BC / Lemma IR conditions | added [LC2C-3] |
| 4 | NIT | E1: BM-∞ gives (BM-W) only under (N-χ) | reworded [LC2C-4] |
| 5 | NIT | §0: D needs α > 1, J needs α > 2 | sentence added [LC2C-5] |
| 6 | NIT | STATEMENT (C5) said "verified in" L6 | reworded: each example carries its own status |

## SC2 — `SC2_statement_change_sol.md` (Codex gpt-6.1-sol high; STATEMENT v1.3 → v1.4)
Verdict: **ACCEPT WITH CHANGES.** The implication v1.3 ⇒ v1.4 passes, including the constant 15/c; (L-R^b) is well
posed; the records match the lemma files.
| # | class | finding | action |
|---|---|---|---|
| 1 | MAJOR (notation) | the leak sequence was written ℓ_n, which is the LS0 move cap in §1 and (C1): contradictory literal reading | leak sequence renamed **ϖ_n** (ϖ′_n for its localised counterpart) in STATEMENT, L4, L5, SHARPNESS, and varpi_n in L6 [SC2-1]. (The reviewer proposed λ_n; λ_n is already the signal-floor quantity of `lemmas/L2_width.md` §4, so ϖ_n is used — a deviation of symbol only.) No cap, code option or pin changes |
| 2 | MINOR | §5 sentence said (C3) is conditional on SOP:TH09 and on nothing | replaced by the reviewer's sentence [SC2-2] |
| 3 | MINOR | wrong pointer (L4 §6 → §7 item 1) | fixed [SC2-3] |
| 4 | MINOR | "the v1.3 hypothesis is kept as the sufficient form" overstated: the sufficient form is more general; (C5) does change | reworded as required, three places [SC2-4] |

## Other edits made with these (record only)
Status headers of L4, L5, L6 cite their checks; `ASSUMPTION_MAP.md` row A:L-gain-R / A:L-loc-R / A:H-size-ρ rewritten
for v1.4; `SHARPNESS.md` added (new file, not part of the LC2 round). No hypothesis, claim, lemma statement, constant
or code pin changes after the round; the proof-text changes are [LC2A-1], [LC2B-1], [LC2B-2]. Per PROTOCOL rule 15
the diff is attested by an independent Sol reviewer in the next round (RC5), and every file is re-read blind by the
exhaustive sweep.
