# MEET-THM · Re-audit of SYNTH_R1 v2 (auditor: gpt-6.1-sol, Codex, high)

Verbatim final message, extracted by the chair from `/home/fb31/.codex/sessions/2026/11/03/rollout-2026-11-03T21-38-38-01a1a4a3-2848-7532-a146-62cb65725956.jsonl`. Audited: SYNTH_R1.md at commit 6a170f2. Corrections N1–N6 applied in v2.1 (correction log §5, last row).

---

Checked 50+ cited references. HQ rulings are now faithfully represented; no proof-status upgrades found.

| finding # | fixed / partly / not | note |
|---|---|---|
| 1 | fixed | Correlated-family scope and passing-check requirement separated. |
| 2 | fixed | Q1 requirements and both failure dispositions restored. |
| 3 | fixed | Q3 obligation, fallback, OPEN reasons and support obstruction restored. |
| 4 | fixed | Existing-input, randomness and feedback restrictions restored. |
| 5 | fixed | Scaling restricted to the examined family; numerical evidence distinguished from proof. |
| 6 | partly | C’s qualifications restored, but D15 still overstates A/B/D’s coverage verdicts; see N2. |
| 7 | fixed | D16 records K23/K80/K107 disagreements. |
| 8 | fixed | Standard identities distinguished from method-specific package content. |
| 9 | fixed | A’s explicit K71 deferral and extraction conflict recorded. |
| 10 | partly | Named exceptions restored, but D5’s “clause level” summary still mishandles K28 and B’s K29. |
| 11 | fixed | D17 includes all seven requested disputes and D’s barrier distinction. |
| 12 | partly | D18 adds groups but still lacks accurate four-seat dispositions; K06/K14/K33/K44/K83/K84 remain omitted. |
| 13 | fixed | All four missing adverse rows restored. |
| 14 | fixed | Aliases, adverse labels, finite-η checks and numerical hypotheses restored. |
| 15 | fixed | Quantile conditions and general duplicate-symmetry rule restored. |

| # | location | finding | evidence | correction |
|---|---|---|---|---|
| N1 | §0.4, line 85 | PC1 references are reversed: necessity is attributed to the q₂ row and vice versa. | PC1:145 concerns q₂; PC1:147 concerns necessity. | Cite necessity as PC1:147 and q₂ as PC1:145. |
| N2 | §2 D15, line 166 | Blanket “matched or exceeded” wording includes Thms 1–2, although A/B/D explicitly disclaim Hellinger contraction. This partially reintroduces finding 6. | A:34–35; B:36–37; D:51–52. | Give coverage verdicts by SL item; retain A/B/D’s own contraction qualifications alongside C’s objections. |
| N3 | §2 D5, line 156 | Despite the new “clause level” label, K28 is grouped as main for A/B/D, and K29 as main for B. | A:341,346; B:264,269; D:308,313 explicitly cite the fine-grid clause; B:264 marks favourable stages supplementary. | Record K28 as cited within those packages; B’s K29 is supplementary. |
| N4 | §2 D9, line 160 | Newly asserts “K70: A, B, D main,” suppressing B/D’s explicit supplementary-corollary dispositions. | B:100; D:109; SBS:121 flags B’s conflicting header extraction. | State B/D’s explicit supplementary placement and preserve conflicting package-header evidence separately. |
| N5 | §2 D18, line 169 | New omnibus pattern misrepresents positions: C’s target package is supplementary; K49/K62/K73 are main; K59 future; K103 supplementary. B also places K36/K78 in main. | C:107–111,153; SBS:87,100,110,113,124,129,154. | Replace the blanket pattern with actual A/B/C/D dispositions per K-ID or genuinely uniform subgroup; include the six omitted IDs identified above. |
| N6 | §0.4, line 72 | “M₂ … on every path” conflates a moment bound with the replica’s pathwise weight bounds. | PC2:53–55,125; PC2:238–239 distinguishes pathwise W bounds from the expectation argument. | State pathwise bounds for W, then M₂ ≤ e^{D_*} for every successful coded grid; retain PROOF SKETCH status. |

FAIL