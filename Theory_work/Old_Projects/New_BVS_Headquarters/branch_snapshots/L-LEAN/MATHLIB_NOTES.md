# MATHLIB_NOTES (Lean v4.35.0-rc2, Mathlib rev 065356127b1d)

- Use targeted imports, not `import Mathlib`. A full import takes >30 min to load on this laptop under memory pressure; targeted imports build a module in ~20–30 s.
- `push_neg` is deprecated: write `push Not at h`.
- `Set.mem_setOf_eq` is deprecated: write `Set.mem_ofPred_eq`. `if_true`/`if_false` are deprecated: write `↓reduceIte` in `simp only`.
- `Mathlib.Data.Real.Basic` is deprecated: write `Mathlib.Basic.Real.Basic`.
- `Finset.sum_div` needs `Mathlib.Algebra.BigOperators.Field`.
- `Measure.real`, `measureReal_def`, `measureReal_mono` are available. `Integrable.of_bound` takes `[IsFiniteMeasure μ]` and `(hf : AEStronglyMeasurable f μ) (C) (h : ∀ᵐ x ∂μ, ‖f x‖ ≤ C)`.
- `integral_indicator_one` is stated for `s.indicator 1`, not `s.indicator (fun _ => 1)`.
- `iIndepFun.meas_iInter (hf) (hs : ∀ i, MeasurableSet[(m i).comap (f i)] (s i))`: pass `⟨t, ht, rfl⟩`.
- No lemma named `isProbabilityMeasure_map`; it is an instance: `rw [← hlaw]; infer_instance`.
- `(fun S => g S) T` does not beta-reduce for `rw`: run `simp only at h` first.
- Unused section variables raise a linter warning: write `omit [DecidableEq M] in` before the theorem.
