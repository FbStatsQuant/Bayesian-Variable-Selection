# W3-RM2-R — H5 summary for HQ (headline change card input; with the IDEAL-W⁺ engineering note)

**Before.** RM2-F (fixed design, leakage set of size n^b): visibility δ²_{U,j} ≥ M_n log n with M_n → ∞; beta-min
θ²_min n/log n → ∞; truth-removal floor λ_n/(d_n² + log n) → ∞. Conclusion of RM2-F and RM2-R: on a data event of
probability → 1, every run *that produces output* reports S₀; P(output and Ŝ ≠ S₀) → 0; no delivery claim.

**After (W3-RM2-R, STATEMENT v1.0).** RM2-F-plus: visibility at a fixed level M_V log n, M_V > (σ√(2A) + √((2A+1)C_R))²;
Theorem 1's beta-min at its constant level BM(c); the truth-removal floor additive at the constant level,
√λ_n ≥ 2(d_n + √(2 log n)) and λ_n ≥ c_TL log n. RM2-F-plus and RM2-R-plus: the same output-conditional conclusion, and
under the delivery premises (D) every run on every valid input produces output and P(Ŝ = S₀) → 1, with
P(Ŝ ≠ S₀) ≤ P(mode failure) + P(search failure). The posterior input is mode consistency (implied by [POST]).

**What it buys the paper.** Signal conditions at the standard σ√(log n/n) scale with constants, as in the comparable
literature (Yang–Wainwright–Jordan 2016, Narisetty–He 2014); a reported-model theorem without "on output"; a clean
error decomposition matching what experiment P6 measures (mode failures vs search failures).

**Assumptions that moved.** Weakened: (V), beta-min in (T1-F), (BM-W) (Form F only). Added for the delivery half only:
the delivery premises (D), incl. IDEAL-W⁺. Nothing else.

**Evidence.** Statement lock SL1 + SC1 (Sol); line checks LC-A, LC-B (Sol; pending at the time of writing); council R1
(Sol + Opus) before CP3. Conditional on SOP:TH09 (Form F) / W2-APP:POST (Form R), as the parents.

**Engineering note (IDEAL-W⁺; for HQ / Engineering, no method change requested).** The delivery theorem needs two fixed
upper bounds in the shipped code to be treated as lifted: (i) `v3_run.R:96` rejects the LS0 base cap `le > 1e6`, and
the default `le = ℓ_n = ⌈log₂(n + p + 1)⌉` exceeds 10⁶ only when n + p + 1 > 2^{10⁶} — astronomically large, but it makes
the code refuse those inputs; the bound guards a testing option (`v3.ls0_ell`) and could be applied to the option only
(not to the default ℓ_n), which would remove the need for this lift; (ii) `cpp/v3_core.cpp:474` rejects an LS0 cap above
INT_MAX (n ≳ 4·10⁹) — a genuine representability limit, covered by the unbounded-integer idealisation in the same way as
the rest of IDEAL-W. Without the lift, delivery is proved on the bounded domain 𝔇 (STATEMENT §2).
