# Final council — consistency chapter (Wave 1C), round 1

**Object.** `Theory_work/Wave1C/FINAL/consistency.tex` (+ `sections/s1_setting.tex` … `s9_prov.tex`, compiled
`consistency.pdf`, 22 pp), committed at 5bcde3b. It is the final product of Theory Waves 1 + 1C for the SMC-BVS paper:
paper-ready statements of the consistency theory, Song–Liang (2015)-style, with pointers to proofs and review trails.

**Sources it must match.** `Theory_work/Wave1/*/` (REPORT.md, STATEMENT.md, proof files), `Theory_work/Wave1C/{C-PACK,
C-MIS,C-GROW,C-DLV}/` (REPORT.md, STATEMENT.md, lemmas/), `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md`,
`Theory_work/State_of_Project/sections/` (04_theory.tex cards TH01, TH05, TH09; 02_method.tex; A_notation.tex),
Song & Liang (2015) PDF: `C:\Users\felip\.t3\userdata\attachments\647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf`.
The writer's fidelity check and disposition: `FINAL/reviews/F1_fidelity_sol.md`, `F1_disposition.md`.

**Two items in the chapter have NOT been through any council and need a full mathematical check from you:**
1. **Lemma CAP** (§7.1, the chapter's only new mathematics): LS0 with cap ℓ_n is a prefix of LS0 with cap
   ℓ_n + |S̃₀|; consequences and the list of clauses that do / do not transfer. Check against the LS0 rules
   (02_method.tex §6.10; `Scripts/SMC_BVS/core/cpp/v3_engine.h:378-425`) and the theorem files it cites.
2. **Proposition F** in its corrected form (A1's "Exact corrected statement"): delivery P(no output) = 0 with the
   total tier-1 calibration fallback, and P(Ŝ⁺ = S₀) → 1 on LH, LH-iid and the W1-GEN class.

**Gates** (each PASS/FAIL with reasons):
- G1 Every theorem/lemma/corollary statement in the chapter matches its source: same hypotheses, same conclusion,
  same scope (nothing dropped, nothing added, no hypothesis silently weakened).
- G2 Statuses copied verbatim; nothing upgraded; "PROVED-CHECKED" used only where the source's review trail supports it.
- G3 The new mathematics (Lemma CAP, the Proposition F assembly) is correct.
- G4 The Song–Liang map is accurate about Song & Liang's results (read the PDF) and about ours.
- G5 Scope and frontier are honest and complete (asymptotics/onsets, polynomial p, S5/factor, finite n, delivery for
  the shipped calibration, reported PIPs, misspecification EP, Θ(p²) memory, EX-A/FP, LS0 not yet shipped).
- G6 Internal consistency: notation, cross-references, premise lists (e4 → e4′, the two "MR1"s, caps) agree throughout.

**Output.** Write only your file: `FINAL/reviews/C1_council_<seat>.md` (seat = sol or opus). Score independently;
do not read the other seat's file. Give: gate verdicts; a numbered list of findings (BLOCKING / MAJOR / MINOR /
NIT, with path:line evidence and exact replacement text where possible); then a final line
`SCORE: x.x/10; GATES: G1 … G6` (uncapped 0–10). Pass = both seats ≥ 8.0 with all gates passing.
No git commands. Do not edit the chapter.
