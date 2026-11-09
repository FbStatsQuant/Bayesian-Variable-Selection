# W2-FAC-A — CHECKPOINT (key lemma proved and checked)

Date: 2026-11-09 ~07:20 CST. Lead: Claude Opus 5.5 (Claude Personal).

## Where things stand
* **Diagnosis done** (numerics/: D1a/D1b iid rows at n ≤ 3200; D2 exact-Gram simulator up to n = 10⁷; D3 exact 1-D CS
  stress, 720 runs; summaries D1a_summary.md, D2_summary.md, D2_lattice.md, D3_summary.md). Findings: the start mode
  tends to all of [p] (extras of order p); MR1 scored S₀ in every tested run; NA over the whole lattice fails on one-sided
  sets once log p/log n is well above 1/6, while actual LS0 paths are pure deletions (D3: 720/720).
* **Statement locked** (STATEMENT.md v1.1; R01 Sol high LOCK-WITH-CHANGES, 10 changes applied). Target narrowed and
  flagged: Theorem FAC-L for the class "one global factor + block-local structure" (CS, block CS, S5; exact/approximate
  Gram; iid rows incl. study S5) under limsup log p/log n < α₀(κ̄) (= 1/6 for every block CS), + delivery; Proposition
  SHARP (1/6 optimal for the full-lattice route on exact CS); path route beyond 1/6, p > K, k ≥ 2: frontier.
* **Key lemma L1 (uniform factor-aware add bound) PROVED and checked:** R02 (Codex gpt-6.1-sol xhigh)
  VERIFIED-WITH-AMENDMENTS (5 MINOR, applied; the reviewer also ran an exhaustive independent numerical check). Mechanism:
  exact Gaussian decomposition of the add statistic into a T-independent idiosyncratic innovation (≤ p2^{γ̄} normals) and
  one residual-factor statistic per T, bounded uniformly via Cauchy–Schwarz in the Ψ-metric; perturbation to approximate
  Gram with constants depending only on ψ₀ (not on ‖Σ‖ ~ p). Falsification: FU_out.txt, FU5_out.txt (0 violations).
* **Drafted (PROVED by this seat, unchecked):** L2 sandwich (Q = [p]), L3 NA/TL on the full lattice (+ the α₀
  calculation), L4 assembly, L5 random design + instances (κ = 1 for all block CS; GC-CS → TV; Lemma P5 whole-group blocks
  for S5; certificate script running), L6 SHARP, L7 delivery (A2 template). Falsification for L3/L6: FNA_summary.md.

## Left
Lemma checks L2–L7 (cross-family), TV certificate output, mid-point review, sweep, council, CITECHECK, REPORT.

## Honest estimate
Part I + II + delivery should close (PROVED-CHECKED) if the remaining checks find no major gap. The brief's full target
(p ≤ n^A, fixed k ≥ 1) does NOT close by this route: Part II proves the lattice route stops at 1/6 for CS. The natural next
target is a path-restricted theorem for exact CS (exact 1-D reduction + gap invariant + count-balance), for which the
numerics are very strong (D3) — recommended as a follow-up ticket; I will write the tools and the precise obstruction in
Part III.
