# T14 → row 3.1 delivery sentence: before / after (draft for the STRONGER H5 card; ≤ ½ page)

**Before** (claims card v1.8, row 3.1, delivery sentence): "delivery holds on the bounded domain 𝔇 = {⌈log₂(n + p_raw + 1)⌉
≤ 10⁶, ⌈log₂(n + p_raw + 1)⌉ + ⌊n/2⌋ ≤ 2³¹ − 1}, and with it (IDEAL-W⁺) for every n [RM2R-5]. Neither limit can bind
unless n + p + 1 > 2^(10⁶) or n ≳ 4 × 10⁹, that is, at no feasible problem size [RM2R-6]." The last sentence is an
informal remark; the proved statement for inputs of real size is the bounded-domain clause.

**After:** "Delivery holds for every input the software can receive: R limits each matrix dimension to 2³¹ − 1, and
every such input lies in 𝔇, so the two code limits (`v3_run.R:96`, `cpp/v3_core.cpp:474`) are provably inactive
(T14 REP). The idealisation IDEAL-W⁺ is needed only for the 'every n' form beyond R's limits, which is already an
idealised machine (IDEAL-W)."

**What changes.** STRONGER, by making a remark a proved statement: "at no feasible problem size" becomes "for every input
R can represent (n, p ≤ 2³¹ − 1), in the shipped default configuration". Proof: ℓ_raw ≤ 32 and ℓ_raw + ⌊n/2⌋ ≤ 2³⁰ + 31
(T14 REP (REP-a), (REP-b); Sol line check VERIFIED). No assumption is added or removed: the bounded-domain clause (a)
of `W2-UNI:F-UNI` already covered 𝔇; T14 shows every R-representable input is in 𝔇. The asymptotic clause (b) under
A:IDEAL-W⁺ is unchanged.
**What it buys the paper.** The delivery sentence can say "every run on any input the software accepts produces output
(under EX-A, IDEAL-W, MACH, sufficient allocation)" without the reader meeting IDEAL-W⁺ at all; IDEAL-W⁺ moves to the
remark on the asymptotic form.
**Scope kept.** Default options only; IDEAL-W's other integer obligations (e.g. `2 * p - 1` in `int` for p ≥ 2³⁰),
allocation and numerical failures are unchanged.

**Line for the 19-claim NARROW note:** "A:IDEAL-W⁺ is vacuous on representable inputs: for every input R can represent
(n, p ≤ 2³¹ − 1), the two predicates it lifts are false in the shipped default configuration (T14 REP, Sol VERIFIED);
the narrowing matters only for the 'every n' form beyond R's limits."
