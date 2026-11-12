# R2 council review — W3-MISR, seat `opus` (Claude Opus 5.5, Claude Work, effort high; blind)

Package: STATEMENT v1.3, `lemmas/{R_reduction,M_misr,G_corollaries}.md`, ASSUMPTION_MAP, numerics, REPORT §1, §3–§7,
`reviews/CITECHECK.txt`, as frozen in MANIFEST 217d6708… (HEAD 0fd888a). Method: `git diff 2f360ed` over the five paths
in the brief (every hunk read), then one full read of STATEMENT and the three proof files, then targeted source checks.
No other review file, LOG, PLAN, CHECKPOINT or API_AUDIT file was opened. Transparency note: the mandated diff of
REPORT.md showed a few lines of §1/§2 that quote the R1 scores; I did not use them.

## Gate verdicts

1. **Correctness — PASS.** Invariance (R.1), reduction in law (R.4), projective form and total-variation bound (R.5),
   MIS-R (i) (M.1), the per-n assemblies of (i′)(a)–(d) (M.2), conditioning of (ii) (M.3), G, H, SNR, P, U are correct.
   The one restated clause, (i′)(a) over 𝒦⁰′_n with its own threshold, is proved: M_misr.md:77-88 uses only (I1)–(I4)
   and e^{ρ_n} ≤ 2. Their hypotheses in the source are G, (E), (F₀), the size conditions, and for (I4) only
   𝒪_n^{>0} ≤ C_OS r_n (A_occam.md:53, 66-67, the (C5′) statement and Lemma M); none uses (ID^M). So n₁ᵃ and
   C′_a = C′_a(s, M, φ₀, C_OS) do not depend on c, and n₁ᵃ ≤ n₁. The index rename in (b) (j → i, M_misr.md:99-101)
   removes a real clash with the fixed coordinate j; the bound is unchanged.
2. **Hypotheses used = hypotheses stated — PASS.** 𝒦⁰′_n (STATEMENT.md:62) is exactly what M.2(a) uses. "At that n" is
   respected throughout. In (a) the first (OS) inequality is the one used (through (I4) with j₁ = 0), and in (b)/(d) the
   second inequality is used through Υ′^{>j₀}. The margin enters only through (I5) per model.
3. **No hidden assumptions — PASS.** G.1 now defines κ_n off the null event (G_corollaries.md:32-34), which closes
   the measurability gap. Remark U's added parenthesis is a consequence, not an assumption: equal Gaussian contrast laws
   give Uᵀxβ = Uᵀxβ′ and v = v′, hence Cxβ = UUᵀxβ = Cxβ′.
4. **Cited inputs — PASS** (one MINOR). Every C-MIS status in §8 matches `claims.tsv` character for character, and so do
   W3-POST:Thm-1 and W3-POST2:A0/C/D. Nothing is upgraded. The "conditional on" lists in the three lemma headers match
   the inputs each proof uses. The SOP:TH128 / SOP:TH09 rows are quoted as prefixes ("status beginning …") and leave
   out qualifiers (F2).
5. **Constants / rates / thresholds — PASS.** The constants of (i) do not depend on v (table R.6: equivalences at each
   n). The (i′)(a) threshold does not depend on c (gate 1). c″ ≥ cn/(n − 1) is consistent with N = n − 1
   (M_misr.md:112). C_H = C_H(s, A) at σ*² = 1, and C_H′ = 1 + C_H/4 (G.3). Recomputed: c₁(1,1) = 160.77,
   c₁(2,1) = 258.90 (STATEMENT [POST2] line 130 formula, C_A = 8 + 3A), and c₀(2,1) = max{4C_*, 192} = 192 because
   C_* = 4 + 3(7 + 2 + log 8 + 1) ≈ 40.2 ([P3] STATEMENT line 21, j_* = 7). These match ASSUMPTION_MAP and the N5
   docstring.
6. **Fidelity to the code — PASS.** No file under `Scripts/SMC_BVS/core` has changed since 16a7f85 (last change
   72785fe; `git diff 16a7f85` is empty). The new pins are correct: `v3_preprocess.R:62-64` (the `centering` list),
   `:129-130` (`stable_centering`) and `v3_fit.R:98` (`fit$preprocessing` excludes only X, y). In real arithmetic the
   anchored branch (`:47-65`) gives uc/us = Cx/‖Cx‖·√N = Cy/s_y, and that metadata reaches no score (it is not passed
   to `v3_context`). The N0 observation is accurate: 3 × 7 + 4 = 25 fits, exact max|ΔPIP| = 1.304e-10, SMC
   1.037e-11, and the HPM is {} in data 12 and in the SMC data.

## Verdict on the diff

Every change is correct. The changes that touch content:
- **§3(a) / M.2(a)** (conclusion extended to the larger class 𝒦⁰′_n, with a threshold and constant that do not depend
  on c). Correct and proved, see gate 1. This strengthens a conclusion, so "no conclusion changed" (STATEMENT.md:8) is
  slightly understated (F4).
- **§0 GR → GR^c sentence** (n-dependent σ², τ²) is correct. It matches [MIS1] lines 54-58: Gaussian ξ independent of
  ε, so ε + ξ ~ N(0, (σ² + τ²)I).
- **R′(c) caveat** ("not a robustness bound") is correct, and if anything understated. The direction law of an iid
  non-Gaussian vector keeps the shape of its coordinates, so its TV distance to the uniform direction does not vanish.
- **Remark U parenthesis** is correct (gate 3).
- **Code pins (a″), R.3** are correct (gate 6).
- **G.1 null event** is correct. **G.4 rename t → a_n** only resolves the clash with Claim B's t = |T|.
- **§8 inputs** are verbatim (F2 aside). **REPORT registry blocks**: the line ranges agree with v1.3 (R′ 70-106,
  MIS(i) 110-123, (i′) 127-140, (ii) 144-160, G 164-174, H 178-197, SNR 201-206, P 207-215, U 216-220, §8 222-245,
  A:MISR-GRC 36-43, ESNR 47, IDM 53-54; ASSUMPTION_MAP lines 15 and 20; N5_out.txt:14 is the a = 1, n = 100 row).
- **Numerics descriptions** (premise change only; the .py edits are print strings). I checked them against the outputs:
  - N1: regimes v_n ∈ {2, 1 + n, 1 + n², 2/n, n⁻²} (misr_numerics.py:99-103); δ/r_n from 1.068 to 1.418; CRN 4.74e-14;
    raw b² = 16 v log n/n in the code.
  - N2: 1.242 and 1.216 at n = 6400; for a = 0.4 the ratio is 0.53–0.66 and δ ≥ 0.982.
  - N3: (ii) 1.458, 1.711, 2.038, 2.588 with HPM 0.92–0.95; (i) 1.300, 1.427, 1.091, 1.234 with HPM 0.96–1.00;
    (iii) 0.232 → 0.018 and 0.490 → 0.929.
  - N4: b ∈ {½, 1, 2} gives 0.465–1.223 with HPM ≥ 0.98; all b gives up to 1.506 with HPM ≥ 0.97.
  - N5: 0.8702 … 0.0031; the control arms are 1.0000.

  The **N5 premise** (the SW1 "substantive" item) is now correct. On the orthogonal standardised design with
  H = (n + 1)G + I and G = N·I, the smoother eigenvalue is nN/n² = (n − 1)/n. So L_{0} = (1/n)·Nθ₁² + Nθ₂²
  = n(n − 1) + 200(n − 1)log n/n, and the other two underfits have L ≥ Nn² = (n − 1)n². (F₀) holds with φ₀ = 1, (OS) is
  void (p = s), (SZ) holds, and energy/(nv) ≍ n². Hence only (E^σ; M) fails for every fixed M, as stated at
  STATEMENT.md:260-264 and ASSUMPTION_MAP.md:17. Its classification as numerical evidence with an analytic sketch, not
  a proof, is honest.

There is no overclaim relative to SL §2.3 or [MIS1]. The differences (in-sample, in probability, s fixed) are stated
in STATEMENT.md:196-197 and in ASSUMPTION_MAP. The "Not claimed" list is honest and now flags the (E^σ) evidence as
unchecked.

## Findings

**F1 (MINOR) — the quantifiers of §3(a) do not say which threshold applies.** STATEMENT.md:127-130. The preamble binds
"every n ≥ n₀′ and every κ ∈ 𝒦⁰_n", and n₀′ depends on c. Clause (a) then rebinds κ to 𝒦⁰′_n and adds that "the
threshold and the constant do not involve c" without naming that threshold. The proof is right (n₁ᵃ, C′_a at
M_misr.md:78-85), but the statement does not tell the reader which threshold to use.
*Fix:* make (a) a standalone sentence: "(a) There are n₀ᵃ, C′_a depending only on (s, A, M, φ₀, C_OS) such that for
every n ≥ n₀ᵃ and every κ ∈ 𝒦⁰′_n(s, A, M, φ₀, C_OS): E_κ π_𝒞(S ⊋ S₀(κ)) ≤ C′_a r_n; n₀ᵃ ≤ n₀′, C′_a ≤ C′." Move
the remaining clauses under the existing preamble.

**F2 (MINOR) — the SOP:TH128 and SOP:TH09 statuses are quoted by prefix and drop qualifiers.** STATEMENT.md:231-234.
The registry status of SOP:TH128 continues "…; VERIFIED core (A-REV5, onset gloss ERROR); LIT-STAT: …". SOP:TH09
continues "… T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY". "Status beginning" is literally
true and nothing is upgraded. But the brief asks for verbatim statuses, and the omitted text contains an ERROR flag and
a same-family-only flag.
*Fix:* quote both statuses in full, or add one clause per row: "(the remaining text records … ; it does not concern
(C6)(a) / lines 39-41, 227-229, `lem:signal`)", after checking that this is true.

**F3 (NIT) — "none of these involves c" has no citation.** M_misr.md:78. The claim holds, but it is asserted where it
should be cited.
*Fix:* add "([A] line 53 and the statement of (C5′), lines 66-67: stated under G, (E), (F₀) and R1, without (ID^M); the
only c-dependent threshold of Claim C is that of (I5), [E] Lemma E1(b))".

**F4 (NIT) — "no conclusion changed" understates the change to §3(a).** STATEMENT.md:8. §3(a) now asserts its bound
over a strictly larger class, with a threshold that does not depend on c.
*Fix:* "no hypothesis strengthened, no conclusion weakened; §3(a) is now stated over the larger class 𝒦⁰′_n that its
proof uses".

**F5 (NIT) — the N5 docstring does not say why c₀(2, 1) = 192.** N5_energy_obstruction.py:5. "c_0(2, 1) = 192" holds
because 4C_* ≈ 161 < 32·6, which is not stated.
*Fix:* add "(4C_* ≈ 161 < 192, [P3] STATEMENT line 21)".

Counts: FATAL 0, MAJOR 0, MINOR 2, NIT 3.

## Score

The revision is clean. Each changed line is correct, the one substantive restatement ((i′)(a)) is proved at the
level of detail of the rest of M.2, and the numerics premise flagged by the sweep is now accurate. All quoted numbers
match the output files, and the code pins match the code. The remaining items are presentation and quotation
hygiene. **Score 8.9.**

COUNCIL-VERDICT round=R2 manifest=217d6708dfee945fa0416171268e08e359e0e7a3fde5bd169756431143c51103 seat=opus score=8.9 gates=PASS

## Addendum — per-claim decisions (seat opus, round R2; 2026-11-12; same seat model, fresh thread; no rescoring)

| id | decision |
|---|---|
| W3-MISR:R' | ACCEPT |
| W3-MISR:MIS(i) | ACCEPT |
| W3-MISR:MIS(i') | ACCEPT |
| W3-MISR:MIS(ii) | ACCEPT |
| W3-MISR:Cor-G(a) | ACCEPT |
| W3-MISR:Cor-G(b) | ACCEPT |
| W3-MISR:Cor-H | ACCEPT |

Where examined:
- W3-MISR:R' — gate 1 (line 11: invariance R.1, reduction in law R.4, projective form and TV bound R.5); gate 5 (line 28, constants of (i) independent of v, table R.6); diff verdict "R′(c) caveat" (line 49) and "Code pins (a″), R.3" (line 52).
- W3-MISR:MIS(i) — gate 1 (line 11, MIS-R (i), M.1); gate 5 (line 28); gate 4 (line 24, C-MIS / W3-POST2 inputs).
- W3-MISR:MIS(i') — gate 1 (lines 11–17, per-n assemblies of (i′)(a)–(d), M.2, incl. the restated (a) over 𝒦⁰′_n); gate 2 (line 18); diff verdict "§3(a) / M.2(a)" (line 44); F1 (MINOR, statement wording) and F2 (MINOR, SOP status quotes) non-blocking.
- W3-MISR:MIS(ii) — gate 1 (line 11, conditioning of (ii), M.3); gate 5 (line 28, c″ ≥ cn/(n − 1)).
- W3-MISR:Cor-G(a) — gate 1 (line 11, "G … correct"); gate 3 (line 21, G.1 κ_n defined off the null event); diff verdict "G.1 null event" (line 53).
- W3-MISR:Cor-G(b) — gate 1 (line 11, "G … correct"); gate 4 (line 24, C-MIS statuses and lemma-header inputs); diff verdict "G.4 rename t → a_n" (line 53).
- W3-MISR:Cor-H — gate 1 (line 11, "H … correct"); gate 5 (line 30, C_H = C_H(s, A), C_H′ = 1 + C_H/4, G.3).
