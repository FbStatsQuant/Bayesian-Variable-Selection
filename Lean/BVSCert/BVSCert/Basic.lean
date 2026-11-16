import Mathlib

/-! Smoke file for the BVSCert project (SMC-BVS Lean certificates). Replace when work starts. -/

namespace BVSCert

/-- Smoke lemma: the toolchain and Mathlib import work. -/
theorem smoke (a b : ℝ) (h : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ a * b := mul_nonneg h hb

end BVSCert
