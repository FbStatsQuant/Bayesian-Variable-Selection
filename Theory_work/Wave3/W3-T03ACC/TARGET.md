# W3-T03ACC — TARGET (one page; Tier B acceptance: the target is the recorded statement, unchanged)

Target statement: `STATEMENT.md` v1.0 §3, claim ids `W3-T03ACC:T03S.1`–`T03S.5` (= SOP:TH09 = NBH TH128). No clause
is changed, weakened or strengthened; no better-theorem review is asked for (Tier B re-check; `BRIEF.md:3`).

## Assumption map (where each hypothesis enters the proof as written; `sources/W1-T03R/PROOF.md`)
| hypothesis | where it enters | how | necessity reading (from the sources; not re-proved here) |
|---|---|---|---|
| R1: s₀ fixed | (C1) `m♯_n ≤ C_m log n`; (C5)(b) constants K_{s₀,j}; (C8) 2^{s₀} multiplicity | constants depend on s₀ | growing s₀ not covered (card Repairs row, `sources/statement/TLF_434-499.md:30`) |
| R1: p ≤ n^A | (C8) `(2p)^{s₀}(n+1)^{s₀/2}Υ^{>j₀} = O_P((log n)^{(j₀+1)/2}/n)`; [P3] union bounds in `lem:Gprob`; j₀ | polynomial union bounds | "from the prior and proof technique; e^{Cn^α} OPEN" (`sources/statement/SoP_04_theory_767-812.tex:41`) |
| G (Gaussian noise, fixed design) | [P3] `lem:red`; exact χ² laws in (B1), (B2); [P1] `lem:num` | exact Gaussian computations | random design is outside this statement |
| R: ‖μ‖² ≤ Mn | [P1] `thm:T01iii` (scale event 𝓑_n), `lem:den` (E₀Λ_n ≤ C_Λ); [P3] `lem:ongood`(b) | scale of s_y² | proof artefact level; not examined |
| R: λ_min(R_{S₀}) ≥ φ₀² | den′; (B3) with S = S₀ in (C4) | denominator of the S₀ score | — |
| SE_λ(j₀) | (B2) → (C3), (C6)(b), (C7) `lem:signal`, (C10) | beta-min scale 1/φ₀² for S ∪ S₀ with ≤ j₀ extras | some SE needed: Prop. D (duplicate columns, `PROOF.md:103-121`) refutes the size-tail target under G, R alone |
| SE_w(m♯_n; g₀) | (B1) → (C2) exact χ²_J, (C4) determinant ratio, (C5) | rank and det ratio for supersets of size ≤ m♯_n | `PROOF.md:215` (Remark 3): a determinant-only condition would suffice (CONJECTURE, not pursued) |
| BM-∞ / BM(c), c > c₀ = L_* | (C10): Δ_S ≥ L_*σ*² log n; [P3] `lem:signalgain` | κ_n(𝒰) ≤ e^{ρ_n} n^{−2} | c₀ is "a proof artefact, not sharp" (record, `sources/statement/W6-FIXREV2_STATEMENTS.md:35`) |

Conclusion level: posterior (exact target π), plus the deterministic posterior-to-decision inequalities of clauses 2–3.
Rate: O_{P₀}(√(log n/n)). Scope: fixed design, s₀ fixed, p ≤ n^A (p ≫ n allowed), asymptotic along the triangular array.

## Parity
Unchanged from the record; the acceptance changes no clause. Literature position as recorded in the sources (NBH TH128:
"LIT-STAT: modest extension of Rossell 2022, clause (iii) known") — context only, not a gate of this ticket.

## Boundary numerics
None new (Tier B re-check; v4 §3.3 requires boundary numerics only with a target change). The proof's own numerics
are in `sources/W1-T03R/` (`tail_bound.py`, `duplicate_counterexample.py`, `proof_n0.py`, `se_n200.py`, `bm_constants.py`).
