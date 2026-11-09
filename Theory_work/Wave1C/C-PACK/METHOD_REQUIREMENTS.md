# C-PACK — METHOD_REQUIREMENTS (for C-ENG, via HQ)

These are requirements on not-yet-shipped components (LS0 integration, e4 fallback) under which item 1's premise
replacement e4 → e4′ (`lemmas/I1_e4_replacement.md` §4) is valid. No shipped component is changed.

- **MR1 (LS0 centre = coded start mode).** The integrated LS0 starts from, and emits (scores), the set
  `start_mode(st, cap).S` returned by the coded routine (`CODE/cpp/v3_start.h:183-240`) called on the run's own `Start`
  object as filled by `build_tables`/`build_start` (W1-N3 (H1)), with cap ≥ 1 (default 10⁶) and execution conditions (H4).
  Any replacement routine must return, under exact arithmetic, a maximiser of f whenever the maximiser is unique (TDP of
  W1-N3 (f) does; so does the current routine).
- **MR2 (fallback trigger).** If an e4 tie-aware fallback is added and triggered by `res.truncated`, keep cap ≥ 2: at
  cap = 1, `truncated` is true even when N = 1 (W1-N3 (b); observed in `numerics/item1_um_checks_out.txt` (A)). Under exact
  arithmetic this is harmless (TDP returns S* = R when N = 1), but the binary64 statement Lemma UM-FP is proved only for
  the current routine's evaluation path (N3 (e)); a fallback path would need its own floating-point analysis.
- **MR3 (no reliance on lex rule).** No consistency result of W1-PXN, W1-GEN or M5(b1-LH) needs the size-then-lex tie rule
  or the truncation fallback; C-ENG may choose them for reproducibility only.

`CODE/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`.
