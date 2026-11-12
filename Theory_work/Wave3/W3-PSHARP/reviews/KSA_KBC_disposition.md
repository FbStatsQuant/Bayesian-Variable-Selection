# KSA / KBC disposition (line checks, gpt-6.1-sol high, codex, blind)

**KSA** (`KSA_check_sol.md`): `lemmas/S_one_step.md` VERIFIED; `lemmas/A_log_factor.md` VERIFIED; 0 findings. Every
display re-derived (Lemma V, S(1)–(4), Lemma W(i)–(ii), Lemma R, both witnesses, §5, A1, A2, Remark 2); "no uncovered
in-scope theorem items"; the rank formulation needs no eigenvalue floor. Nothing to apply.

**KBC** (`KBC_check_sol.md`): `lemmas/B_sparsity.md` VERIFIED; `lemmas/C_counterexample.md` VERIFIED-WITH-AMENDMENTS;
0 FATAL / 0 MAJOR / 3 MINOR / 1 NIT — all in commentary or numerical descriptions of C; Proposition C items 1–3 and
Corollary B stand as written.

| finding | disposition |
|---|---|
| 1 MINOR — "n²R^T_{m_n} … decreasing" is false for the exact quantity (ceiling/floor steps; max 5.2·10⁻⁴ at n = 225) | **Applied** (C §2): the exact values are not monotone; the decreasing upper envelope proves the bound. |
| 2 MINOR — "vacuous unless log L ≫ n³b²/k" confuses non-trivial with tending to zero | **Applied** (C §4) with the reviewer's sentence. |
| 3 MINOR — "not shown: that a cost of order (log n)² … breaks the conclusion" understates what is proved: a large constant multiple of (log n)² does break it (cost between 600V₀ and 1200V₀ times (log n)²) | **Applied** (C §4; STATEMENT remark → v1.2.1; REPORT; ASSUMPTION_MAP): open is only B_n = o((log n)²) and the sharp constant. No claim item changed (the item "any B_n with B_n/(log n)² → ∞ fails" was already valid). |
| 4 NIT — control-arm maximum is 3.149·10⁻¹³, not ≤ 3·10⁻¹³ | **Applied**: "≤ 3.2·10⁻¹³" (C §5, REPORT). |

Changes after these checks are editorial (commentary and one number); they are inside the manifest frozen for the
council, so the council reads the corrected text.
