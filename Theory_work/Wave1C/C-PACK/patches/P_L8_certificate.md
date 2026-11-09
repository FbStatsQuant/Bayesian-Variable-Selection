# Patch P-L8 — to `Theory_work/Wave1/W1-GEN/lemmas/L8_certificate.md` (and one line of L6_instances.md, STATEMENT.md)

Source: dedicated check R32 (`reviews/R32_L8_check_sol.md`, Codex gpt-6.1-sol xhigh), verdict VERIFIED-WITH-AMENDMENTS,
FATAL 0 / MAJOR 0 / MINOR 2 / NIT 1. All three accepted by the lead and independently re-checked by R37 (`reviews/R37_patch_recheck_sol.md`: P-L8.1–3 verified, incl. the W coefficient θ(1+ε_n/3) and the (ε₀, κ) range); texts below are R32's proposed repairs (verbatim where
quoted). The Wave1 files are not edited; HQ applies these when adopting W1-GEN.

## P-L8.1 (R32 #1, MINOR) — admissible (ε₀, κ) for "hence (H2c)"
Location: `L8_certificate.md:36` and `:40` ("Then S* := ∪_b supp(γ^L_b) satisfies (H2b) and NL_η(S*), hence (H2c).");
`STATEMENT.md:72`, `:75` (the NL_η parenthetical).
Append after the sentence at L8:40 and to STATEMENT's NL_η parenthetical:
> Here (H2c) is supplied with C_L = η and with ε₀ > 0 chosen sufficiently small that η/2 + √(2η(A + ε₀)) < 1/2; any
> fixed 0 < κ ≤ 1/2 − η/2 − √(2η(A + ε₀)) is then valid. For η = 0, any ε₀ > 0 and 0 < κ ≤ 1/2 are valid. If ε₀ and κ
> have already been prescribed, require this compatibility inequality.
Reason: with ε₀ held at an arbitrary fixed value the implication NL_η ⇒ NL_avg(κ) can fail (R32's 4-column construction:
E_{∅,3}/log n → 0.05 + √0.4 ≈ 0.682 > ½ with ε₀ = 1; passes with ε₀ = 0.001; `numerics/item3_L8_falsify_out.txt`). This
is not a counterexample to GEN: L2 already states "NL_η implies both for admissible κ and sufficiently small ε₀"
(`L2_centre.md:62`); the patch makes the constant contract explicit at the certificate.

## P-L8.2 (R32 #2, MINOR) — stale W parenthetical in L6
Location: `L6_instances.md:107`, text "(T22iii PROOF_v2.tex:404-425). (Also L8.2 with γ^L = θe_{j}.)".
Replace the parenthetical "(Also L8.2 with γ^L = θe_{j}.)" by:
> (Also L8.2 with γ^L = γ_j e_j = θ(1 + ε_n/3)e_j and γ^S equal to the actual coefficients on C ∖ {j}, as in L8.3.)
Reason: γ^L = θe_j leaves a nonzero small coefficient θε_n/3 on the same coordinate, violating L8.2's disjoint-support
hypothesis; L8.3 already has the corrected split (R10 item 3). L6's separate direct VIS/leakage proof is unaffected.

## P-L8.3 (R32 #3, NIT) — notation collision M
Location: `L8_certificate.md:7-8, 20, 23, 29-31, 44-45`.
Name the missing set D_{b,U} := U*_b ∖ U in both proofs; replace every set-indexed X_M, γ_{b,M}, γ^L_M, G_{U∪M} by
X_{D_{b,U}}, γ_{b,D_{b,U}}, γ^L_{D_{b,U}}, G_{U∪D_{b,U}}; reserve M for the scalar in ‖μ‖² ≤ Mn.

## Effect on W1-GEN
No hypothesis or conclusion of Theorem GEN changes. (C1′) status after this ticket: dedicated XF check VERIFIED-WITH-
AMENDMENTS (R32), amendments above; falsification numerics 12 seeds, 108 designs, 3,024 VIS checks + 6,480 leakage
triples, 0 falsifications of the correctly quantified certificate (`numerics/item3_L8_falsify_out.txt`).
