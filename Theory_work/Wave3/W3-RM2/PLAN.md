# W3-RM2 — PLAN (leg B: up to CP1; proof plan for later legs as sketch only)

Lead: Claude Fable 5.2 (Claude Work, effort high). Brief: `BRIEF.md`. Target: `STATEMENT.md`.

## 1. What changes at |Q| = n^b, step by step (the reading behind the target)

RM's proof has four inputs to the deterministic core RM-0 (which has no size restriction on Q).

| input | where |Q| enters in RM | at |Q| ≤ n^b |
|---|---|---|
| [POST] (Theorem 1) | nowhere | unchanged |
| [SAND(Q)] fixed design (GROW L3 / RM B2τ) | the size ladder uses only k₀ = |Q| + 16s₀ ≥ 1; junk exclusion has margin [½ − η/2 − √(2Aη)] log n − log k̃ with k̃ ≤ 2|Q| + 32s₀ | **survives with positive margin [β(η, A) − b] log n when b < β(η, A) = ½ − η/2 − √(2Aη)** (b < ½ at η = 0) — the margin of this proof, not a necessity statement [MP1-2]; heuristically, above √n the prior no longer pays for excluding the best of p noise columns |
| [SAND(Q)] Gaussian rows (RM SAND-R) | reference count per column = subsets of H_l of size ≤ 15 | with |H_l| ≤ n^ρ the count is n^{15ρ}: ladder needs 15ρ < ½, junk exclusion 15ρ + b < ½ |
| [TL(Q)] | toolkit union over the lattice family: t_n + h_n² = O(|Q| + log n) | survives under (BM-Q) (signal ≫ |Q| + log n) and |Q| log n/n → 0 |
| [NA(Q)] | (N-χ): one common χ²_{|Q∖S₀|} charge — only for |Q ∖ S₀| ≤ (1 − δ₀) log n; (N-D): ≤ p·n^h directions up to an ℓ² error charged to χ²_{|Q|+1} — needs ρ_n² |Q| = o(log n) | **(N-χ) is gone; (N-D)'s ℓ² charge becomes useless** (ρ_n = o(n^{−b/2})). The threshold itself loses 2 log(|T| + 1). What replaces (N): a Gaussian-width condition **(W)** on the lattice directions with size-dependent levels — a sufficient negative-gap condition, with primitive sufficient forms (frames + ℓ¹ atoms + ℓ² remainder; local regressions), a positive-gap obstruction (W-conv) and an unresolved bounded-gap regime [MP1-2] |

So the theorem is "(T1) + floors + (V) + (L^b) + (BM-Q) + (W)". (W) is not derived from (V), (L): a heuristic design
(RM SHARPNESS §4) has lattice width² ≈ 2 log p + 0.4|Q ∖ S₀|, so whole-lattice no-addition fails there once |Q| ≫ log n,
while LS0 is observed to descend anyway. Removing (W) = path-level control = not this ticket.

## 2. Deliverables of this leg (CP1)
1. `STATEMENT.md` v1.0 → statement-lock review SL1 (fresh Sol, blind) → disposition → lock (reconciliation Sol and a
   fresh blind Sol if the lock changes substantively).
2. `ASSUMPTION_MAP.md` (template of `Theory_work/INFRA/templates/`).
3. Boundary-violation numerics, local machine, `numerics/` (scripts + RESULTS.md). Experiments (details in
   `numerics/SPEC.md`): B1 size of the leak set, b ∈ {0.25, 0.375, 0.5, 0.625, 0.75} (inside, at and above ¼ and ½);
   B2 lattice width: a leak set whose columns load on a common direction (width condition violated) vs an
   orthogonal one; B3 signal floor (BM-Q) violated: |Q| ≫ nθ²_min ≫ log n; B4 leak level: b fixed, η across the
   frontier β(η, A) = b. For each run: start mode vs Q (sandwich), the realised maximum of Z²_{T,l} − c_n(|T|) along
   and around the path, LS0 moves by type, end point, old-cap result.
4. Better-theorem review BT1 (fresh Astra, blind): statement + assumption map + numerics.
5. `CHECKPOINT_1.md`; end of run.

## 3. Proof plan after CP1 (sketch only; nothing started before HQ's go)
* L0 `lemmas/L0_toolkit_b.md` — (P0): GEN-L1 / GROW L0.2 at actual cardinalities, self-contained.
* L1 `lemmas/L1_sandF_b.md` — (P1), delta to GROW L3 + RM B2τ.
* L2 `lemmas/L2_width.md` — **key lemma**: (P3) NA-W (size-dependent levels, Gaussian concentration), (P4) the
  sufficient forms, (P5) W-conv; (P2) TL-F^b.
* L3 `lemmas/L3_formR_b.md` — (P7) SAND-R^b (parallel prover Sol + cross-family check, as in RM), (P8), (P9), (P10).
* L4 examples; SHARPNESS.md; REPORT.md with registry block.
Review layers as PROTOCOL: lemma checks with falsification numerics, independent mid-point (CP2 after it), exhaustive
sweep, council (CP3). Kill budget (rule 14): 3 failed attempts on the key lemma → STUCK at CP2.

## 4. Risks seen now
* (W) may be judged "not primitive". Answer in the statement: it is a deterministic property of (X, Q), it contains
  RM's conditions, it has primitive sufficient forms, and W-conv shows that a positive diverging gap makes the
  whole-lattice event fail (the bounded-gap regime is unresolved) [MP1-2].
* Form R costs more than Form F (SAND-R^b is a long re-run). It is stated; HQ may defer it at CP1.
* Examples at p ≫ n exist only in Form R (exact-Gram designs have p < n).

## 5. After CP1 (HQ decision 2026-11-11)
Adopted into STATEMENT v1.3: (BM-Q) -> (BM-W) (BT1 P1: truth-removal width; the TL step uses an exact two-square
identity instead of the toolkit contrast bound); (W) as a diverging width gap with the converse "gap -> +infinity"
and a no-addition failure rate (BT1 P2 in the form G1). P3 (Form R scales): one attempt inside the Gaussian-row
sandwich lemma after CP2, else open item O3. Form R stays in the ticket, after Form F's key lemma. Order to CP2:
one fresh Sol check of the v1.3 change; L0 toolkit, L1 fixed-design sandwich, L2 width lemmas + truth removal (key
lemma); Sol lemma checks with falsification numerics; Astra mid-point; CP2.

## 6. After CP2 (HQ decision 2026-11-11, 23:10 CT)
Form R leg: `lemmas/L4_sandR_b.md` (P7, with riders P3 and T6 — both succeeded, STATEMENT v1.4), `L5_formR.md`
(P8–P10, (C2), containment of RM-R), `L6_examples.md` (parallel prover; (C5)), `SHARPNESS.md`, `REPORT.md`. (§3's file
names for L3–L4 were provisional: L3 is the Form F assembly.) Then: exhaustive sweep, better-theorem review on v1.4,
council, CP3.
