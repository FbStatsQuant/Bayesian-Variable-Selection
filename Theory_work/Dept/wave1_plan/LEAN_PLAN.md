# LEAN 4 PLAN: Wave 3 (Lead-L) — Lead-A v0.1, 2026-11-28

**Status: DRAFT v0.1 for the Plan Council.** Owner rule (`REVIEW_S3_HQ_OWNER_2026-11-28.md` point 2): every theorem we
prove gets Lean. The deterministic and combinatorial core is fully checked. Standard probability facts not in Mathlib
enter as **named, cited axioms**, listed and reviewed. No hidden `sorry`.
Gate: the Lean department is GATED until HQ sends GO (`Lean/BRIEF.md`). Lean starts only after a paper proof is
DEFINITIVE (council ≥ 8.5). This plan is what Lead-L receives at GO.

## 0. Environment and reuse
- Project: `Lean/BVSCert/` (a stub at present: `BVSCert/Basic.lean`). Toolchain `leanprover/lean4:v4.35.0-rc2`; Mathlib
  rev `065356127b1dc0016f66b7283ce0ce2c4055aa55`, shared cache (`Lean/BRIEF.md`). `lake build -j 8` at most;
  `nice -n 10` for long builds.
- Reuse the archived L-LEAN snapshot:
  `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/L-LEAN/SmcBvs/SmcBvs/`
  (`Axioms.lean`, `Basic.lean`, `T21HPM.lean` (majority mass ⇒ HPM), `T07Bayes.lean`, `T11Miss.lean`, `T12Core.lean`).
  Port it into `BVSCert` after an audit of its axioms against §2. Copy nothing that carries an unlisted axiom.

## 1. Modules, in build order

| # | Module | Content | Paper source | Tier | Effort (person-weeks; Astra's ranges) |
|---|---|---|---|---|---|
| 1 | `BVSCert.Posterior` | finite model space $\Omega=\{S:|S|\le K\}$, capped BB(1,p) prior; posterior summaries (L-POST): the PIP bound, HPM/MPM from $\pi(S_0)>\tfrac12$, the functional bound | L-POST; T21HPM | 1 | 1–2 |
| 2 | `BVSCert.SizeTail` | exact BB(1,p) tail E1, the bounds on $m^\sharp_n$ (E2) | L-SIZE ([T03R] §1) | 1 | 1–2 |
| 3 | `BVSCert.Score` | coded score algebra (L-SCORE): $D_S$ bounds, monotonicity of $Q_S$, interlacing, ridge; scale reduction (L-SCALE) | L-SCORE, L-SCALE | 1 | 2–4 |
| 4 | `BVSCert.Selection` | T03♯ in interface form: deterministic inequalities on the event $\mathcal G_n$; the event's probability from axioms P1, P2; the two-floor bridge L-FLOOR (deterministic part); the random-design transfer L-RAND | Thm S, L-T03♯, L-FLOOR, L-RAND | 3 | 6–12 (all of selection) |
| 5 | `BVSCert.Misspec` | Thm M: finite-model a.s. argument; SLLN from Mathlib (`ProbabilityTheory.strong_law_ae`); LIL as axiom P6; the NIG conditional concentration; Lemma H applied to $f_0$ | Thm M, L-FIX, L-LIL | 2–3 | 4–8 |
| 6 | `BVSCert.Density` | Thm D: Lemma H; Lemma X structure; Lemma T (class count proved, relative-deviation inequality as axiom P5); B2-core (axiom P3) | Thm D | 3 | 10–20 |
| 7 | `BVSCert.Corollaries` | Cor S1, Cor M1 (reductions) | Cor S1, Cor M1 | 1 | < 1 |

Order (packet §3.5): 1 → 2 → 3 → 4 (selection) → 5 (A8) → 6 (density) → 7. Modules 1–3 can start as soon as the
first paper proof is DEFINITIVE, since they are shared.

## 2. Named axioms (the complete list; adding to it needs a council review)

Each axiom sits in `BVSCert/Axioms.lean` with a docstring giving the exact citation, the statement in words, and the
consumers. It must be stated in the weakest form the proofs use.

| ID | Axiom | Citation | Consumers |
|---|---|---|---|
| G1 | Gaussian integral identities: the Hellinger affinity of two normals; normal–inverse-gamma marginal likelihood (if not derivable from Mathlib's `gaussianReal`) | standard; e.g. Gelman et al. (2013) for NIG | L-HELL, L-SCORE (posterior form), L-FIX |
| P1 | Cochran's theorem: quadratic forms of standard Gaussian vectors in orthogonal projections are independent $\chi^2$ with rank degrees of freedom | Cochran (1934) | L-T03♯ (event $\mathcal G_n$), Lemma X |
| P2 | Laurent–Massart $\chi^2$ tail bounds; the $\chi^2$ moment identities used in [P3] `lem:chi` | Laurent & Massart (2000), Lemma 1 | L-T03♯, Lemma X |
| P3 | Bernstein's inequality for sub-exponential sums (with the net argument proved in Lean) | Vershynin (2018), Thm 2.8.1 | L-DES (B1, B2-core) |
| P4 | inverse-gamma tail/density bounds, if not derivable | standard | Lemma X (variance clause) |
| P5 | relative-deviation VC inequality | Anthony & Shawe-Taylor (1993) | Lemma T (Thm D) |
| P6 | Hartman–Wintner law of the iterated logarithm (i.i.d., finite variance) | Hartman & Wintner (1941) | L-LIL (Thm M(iii)) |

SLLN is **not** an axiom: Mathlib has it. Lemma T's ghost-sample proof in `W3-DIST/work/B_transfer/T.md` is in-house.
Lead-L may derive it instead of using P5 (Astra's preference); P5 is the default (Fable Phase 2 §2).

## 3. Acceptance per theorem (Lean "done")
1. `#print axioms <Theorem>` lists only: Lean core (`propext`, `Classical.choice`, `Quot.sound`) plus §2 IDs.
2. CI greps `sorry`, `admit` and `native_decide` and fails on any hit.
3. The Lean statement is checked against [LS] by a fidelity review (statement ↔ Lean, line by line), with the same
   council rule (Opus + Sol + third seat; bar 8.5).
4. Probability-heavy statements may be certified in **interface form**: "if events with these probabilities exist, the
   conclusion follows", with the event probabilities discharged by §2 axioms. The paper says which theorems are
   certified in interface form.

## 4. Risks
- Mathlib matrix analysis (interlacing, Schur complements, determinant monotonicity) may need local lemmas: 1–3 weeks
  inside module 3.
- Lemma X (density) is long. Formalise its skeleton with tier-3 leaves first.
- Statement fidelity: raw vs standardised units, the plug-in intercept, $p_{\rm ret}$. The fidelity review in §3
  item 3 is the guard.
