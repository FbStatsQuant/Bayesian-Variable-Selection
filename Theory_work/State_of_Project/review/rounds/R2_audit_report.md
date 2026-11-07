# Overreach audit after council round 2 (independent Opus auditor, 2026-11-07)

Scope: every summary-type text (plain / agentnote / notproved boxes, overview and map tables, regime map, agent brief, frontier summaries, history "current state" lines, EMP summaries, glossary, notation meanings, registry `short`/`regime` cells), checked against the card statement or status it summarises. `stmt` boxes and `\status{}` untouched.
Result: 63 summaries corrected in 8 section files and 4 registry TSVs; 8 notation rows added (A_notation.tex:113–120).

Key corrections (full list in the auditor's thread report; line numbers as of the audit):
- 04_theory TH05 plain: "reports S₀ jointly with output w.p. → 1" → joint-error form, liminf form, delivery not claimed; also "posterior miss" corrected to π(S₀) ≤ ½ (the card's meaning).
- 04_theory map rows TH01–TH09: added premises, regimes (H-DOM; LH exact Gram under G; p ≤ n^A; asymptotic; jointly with output), and the sketch/unchecked/CONDITIONAL/SAME-FAMILY-ONLY qualifiers; TH04 brackets only when S₀ is stored; TH06 L² obstruction with "no matching upper bound"; TH08 given the execution DAG (audit open).
- 04_theory plain boxes TH01–TH08 and the three-layer/regime map: same kinds of qualifiers; N200 described as "a lower bound plus a measured term".
- 00_agent_brief: recovery results each with family, joint-with-output form, no delivery; LH-iid unreviewed; T03♯ needs fixed-design hypotheses.
- 04b supplement plain boxes TH10–TH13, TH15, TH17–TH20, TH22: statuses/premises restored (e.g. TH11 "every group has size ≤ B"; TH12 TV bound useful only if M₁ = O(1); TH18 2/3 limit only for p = 2; TH22 Seat C's actual scopes).
- 03_empirics agentnote: "every wrong report among completed fits"; truth-first-scored provenance stated per regime; TD failure "in every checked case (196 …)"; N200 lower bound + measured term.
- 05_history: Theorem A conditions and Lean scope; Prop GU w.p. → 1 under its hypotheses with source; M6 L²-only qualifier; HQ quotes qualified.
- 06_open_and_plan: FR06 "validity under any correlation" qualified (M1(a) cited, premises, N1 sketch); FR07/FR13 qualified.
- D_glossary: "adopted" recorded for N9 only. A_notation: Ẑ_r unbiasedness with premises.
- Registry: TH01, TH05, TH05.a, TH05.b1LH, TH06, TH06.b regimes/shorts; TH18 short; DF13 short; CJ222 short.
Notation rows added: S°; M(S); TD′∞, TD′_P (TD′ unsubscripted defined only implicitly); Lat(S), R_{a,d}; C (implicit), Φ(C), τ(C); STAB-LH; L-DIL (node name only).
Left unchanged on purpose: verbatim card fields and HQ quotes that themselves overclaim (summaries around them qualified); verbatim archive descriptions in history.tsv `short` cells (status cells carry caveats); two verbatim source sentences (OB08 "outside every selection theorem", LIT-VENUE "genuinely ours").
