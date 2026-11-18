# Helper A brief — W3-START2-R, T8 proofs (Opus 5.5, effort high, Claude Third) — saved before launch

You are a proof helper for ticket W3-START2-R (Theory Wave 3), working for the ticket lead. Repository root:
`/home/fb31/BVS-wt/W3-START2-R` (a git worktree). **Write only these two new files:**
`Theory_work/Wave3/W3-START2-R/lemmas/R1_VIS.md` and `Theory_work/Wave3/W3-START2-R/lemmas/R2_NEC.md`.
Do not edit any other file, change no git state, start no agents. Temp files (if any):
`export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261116-W3-START2-R-helperA; mkdir -p "$TMPDIR"`; remove when done.

## Read first
- `Theory_work/Wave3/W3-START2-R/STATEMENT.md` v1.5 (the target; locked). The claims you prove: (D3) and its relation
  paragraph (lines 51-69); [VIS-c], [VIS-m] (101-112); [START-F] (113-128); [F4] (134-144); [NEC-b] (145-153);
  [NEC] (154-166). Use `grep -n` to confirm line numbers; cite them in your files.
- `Theory_work/Wave3/W3-START2-R/PLAN.md` §2 rows R1, R2 (the intended route) and §6 risks.
- BASE = `Theory_work/Wave3/W3-START/` (v1.3.4, read-only): `STATEMENT.md`, `lemmas/L2_TK.md` (toolkit: (TK-a)–(TK-f),
  (f1)–(f3), κ_E, ω̄_n, ϑ̄_n, n₁), `lemmas/L4_VIS.md`, `lemmas/L7_NEC.md`, `lemmas/L3_LEAK.md` (L3.1, L3.5),
  `lemmas/L5_ASM_STARTF.md`, `lemmas/L6_COROLLARIES.md` (L6.0, L6.0′).
- PARENT = `Theory_work/Wave3/W3-START2/` (v1.4.1, read-only): `STATEMENT.md`, `lemmas/P1_LEADING.md` (P1.4, P1.5),
  `lemmas/P3_NEC.md`.
- Format model: any parent lemma file (header with Status line "PROVED (by this seat)", "Statement proved:", "Uses:").

## What to write
**R1_VIS.md** (claims VIS-c⁺⁺, VIS-m⁺⁺, START-F⁺⁺; and the relation remark of (D3)):
1. Relation: (V-c) with c_V > 1 + 2A ⇒ (V-cp) with c_V − 2A; (V-m) with (c_m, ε₀) ⇒ (V-mp) with the same constants for
   n ≥ 256s₀² (p/c_Q ≥ 1/(16s₀)).
2. A copy of BASE L4.1 (Proposition L4.1) under (V-mp), with every changed line marked `[R-1]`, `[R-2]`, …: Step 5 with
   the exact price (Π ≤ π_n/2 + C₂ for d ≥ a; Π ≤ π_n/2 for a > d, sign of log(p/c_Q) not used); Step 4/6 split by the
   sign of π_n + c_m log n and of π_n (for π_n < 0 the factor (1 − ε₁)/(1 + ω_n) ≤ 1 helps; for π_n ≥ 0 choose ε₁ as in
   BASE using p ≤ n^A). Unchanged steps may be cited by BASE line instead of copied, if clearer.
3. A copy of BASE L4.2 under (V-cp): keep log(2p) explicitly, κ_V = (c_V − 1)/2, choose ε₁ against (c_V + 2A).
4. The interface forms: VIS-c⁺⁺ and VIS-m⁺⁺ as stated (hypothesis [TK] in the quantitative form of BASE STATEMENT
   :187-191; the explicit thresholds n₃, n₄ as refinements under (E), (GF-16)); Corollary L4.3 analogue.
5. START-F⁺⁺: PARENT P1.4–P1.5 with the new bridges; state exactly which thresholds (n₃, n₄ via BASE L6.0) change and
   that nothing else does; (T1⁺⁺)(d) uniform constants depend on c_V or (c_m, ε₀) of (D3).
**R2_NEC.md** (claims NEC-b⁺⁺, NEC⁺⁺, F4⁺⁺):
1. Copy of BASE L7.1, L7.2 at the pointwise level G_n := c·log n + 2 log p (keep log((s₀+1)/(2p−1−s₀)) ≥ −log(2p) and
   log((2p − s₀)/s₀) ≥ log(p/s₀) exactly; ε₁ against (|c|/2 + A + 1)), marked `[R-#]`.
2. Drifting clauses: (i) (c_n − 1)√log n → ∞ ⇒ π₀(S₀) → 0 in probability, via (δ + σZ)² ≥ δ² − 2|δ|σ|Z| with
   |Z| ≤ M on an event of probability ≥ 1 − ε, handling gains much larger than log n separately with (f1) (no upper
   bound on the gain may be used); (ii) (1 − c_n)√log n → ∞, via (δ + σZ)² ≤ δ² + 2|δ|σ|Z| + σ²Z² and (f3).
3. (N2⁺⁺) via PARENT P3 pigeonhole; (N3⁺⁺) via (ii); (N1), (N4) by citation. Show that the old premises imply the new
   ones (for the supersession rows of STATEMENT §5).
4. F4⁺⁺: copy of BASE L3.5 with G_n ≤ (1 + 2A) log n for c_n ≤ 1, the explicit constant C_A = 2√(1 + 2A) + 1 and a
   threshold n_F depending only on A; (AL) consequence; old F4 ⇒ new F4 (supersession row).

## Rules
- Prove exactly the STATEMENT clauses, no more, no less. If a clause looks false or needs an unstated hypothesis,
  do not change it: write the issue at the top of the file under "ISSUES FOR THE LEAD" and say so in your final message.
- Every citation as `path:lines` (BASE/PARENT prefixes as in the parent files); no registry claim is consumed beyond
  those STATEMENT §5 lists.
- Final message: ≤ 15 lines: what each file proves, any issues, the [R-#] count, hours used.
